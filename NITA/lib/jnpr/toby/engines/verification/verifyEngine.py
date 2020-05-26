#!/usr/bin/env python
# coding=utf-8
"""
 Copyright (C) 2015-2016, Juniper Networks, Inc.
 All rights reserved.
 Author:
 Description:
 Usage:

"""
# pylint: disable=locally-disabled,undefined-variable,too-many-branches,too-many-nested-blocks,eval-used,superfluous-parens,bad-indentation,dangerous-default-value
import copy
import re
from io import BytesIO
import time
import threading
from threading import Thread
import datetime
import os
import fnmatch
import sys
import json
import lxml
import string
#import inspect
from collections import OrderedDict, Iterable
from lxml import etree
from lxml.etree import tostring
from yaml import dump, load
import ruamel.yaml
# import config_utils as config_utils
import jnpr.toby.engines.config.config_utils as config_utils
from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.utils.Vars import Vars
from jnpr.toby.exception.toby_exception import TobyException
import jnpr.toby.engines.verification.verify_utils as verify_utils
#import verify_utils as verify_utils
from ncclient.xml_ import to_ele
from netaddr import IPNetwork, IPAddress
from jnpr.toby.utils.utils import log_file_version

ROBOT = True
try:
    from robot.libraries.BuiltIn import BuiltIn
    BuiltIn().get_variable_value('${TRUE}')
except Exception:
    ROBOT = False

VE_COMMON_TEMPLATES_PATH_PRO = "/volume/regressions/toby/generic-templates"
VE_COMMON_TEMPLATES_PATH = os.path.join(
    VE_COMMON_TEMPLATES_PATH_PRO, 'prod/verify_templates/jnpr/')


class verifyEngine(object):
    """
        Class of  Verify Engine
        - Protocol/feature independent Design
        - Generic verifyEngine can handle verifications  without requiring backend coding.
        - Supports xml output verification using xpath and operators
            - Any device which supports xml output
            - Supports single value or multiple values verification under the same hierarchy and
              sub-branches
            - Supports values verification even across multiple hierarchies (sub-trees)
            - Powerful operators support to compare the obtained value with expected values.

        - Supports non-xml output verification
            - shell, vty commands  (NEED TO implement)
            - Even some junos commands does not support xml outputs
            - Non-junos device commands like servers
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, offline=False):
        self.t_handle = None
        self.verification_file = None
        self._showdump = None
        self.tmpl_data = []
        self.pylib = []
        self.ve_data = []
        self.tmpl_file = []
        self.vars = {}
        self.is_VE_offline = offline
        self.offline_data = None
        self._is_VE_parallel = False
        self._is_tc_parallel = False
        self.process_tmpl_file = []
        self.process_tmpl_data = []
        self.process_data = []
        self.process_pylib = []
        self.skip = []
        self.iterator_id = 0
        self.get_response_id = 0
        self.response_optimize_iterator = False
        self.iterate_until_present = False
        self.user_optimized = False
        self.global_args = []
        self.init_global_args = []
        self.final_args = []
        self.dh_count = 0
        self._device_handle = []
        self._last_verify_result = {}
        self._last_verify_device_name = ""
        self._default_failmsg = ""
        self._last_verify_tc_name = ""

        self.suppress_log = True
        self.global_suppress_log = True
        self.suppress_overlimit_log = False
        self.suppress_log_limit = None

        self.log_text_output = False
        self.global_log_text_output = False

        # Generic Template Enhancement
        self._common_template_file_names_sourced = []
        self._use_common_templates = True

        # Iterator global variables
        self.iterate_tc_data = []
        self.noiterate_tc_data = {}
        self.noiterate_results = []
        self.iterate_results = []
        self.error_message = None

        if ROBOT:
            self._is_robot = True
        else:
            self._is_robot = False

        self.lock = threading.Lock()

        if self._is_robot:
            self._suite_source_path = os.path.dirname(
                Vars().get_global_variable('${SUITE_SOURCE}'))
        else:
            self._suite_source_path = "./"

        self.VE_KEYS_WITH_VALUE_AS_DICT = ['value', 'iterate_for',
                                           'iterate_until', 'args', 'execute_on', '_all_parameters']

        #print("SUITE_SOURCE_PATH: " + str(self._suite_source_path))

        self.last_xml_execution_data = {
            'last_cmd': None,
            'last_device_handle': None,
            'last_cmd_response': None
        }

        self.last_text_execution_data = {
            'last_cmd': None,
            'last_device_handle': None,
            'last_cmd_response': None
        }

        self.keywords = {
            'verify',
            'use_template',
            'use_library',
            'devices',
            'cmd',
            'include_all',
            'skip',
            'mode',
            'tag',
            'parameters',
            'xpath',
            'operator',
            'value',
            'verify_tmpl',
            'regexp',
            'group',
            'format',
            'type',
            'execute_on',
            'grep',
            'match_all',
            'iterator',
            'iterate_until',
            'func',
            'interval',
            'timeout',
            'verify_template',
            'args',
            'iterate_for',
            'preq',
            'expr',
            'template',
            'regexp_flags',
            'grep_flags',
            'cmd_timeout',
            'cmd_pattern',
            'failmsg',
            'passmsg',
            'xpath_filter',
            'info',
            'suppress_log',
            'config_mode'}

        self.yaml_file_data = {}

        # Vars().set_global_variable("${VE_LAST_VERIFY_RESULT}", self._last_verify_result)

    def initialize_verify_engine(self, **kwargs):
        """
        Initialize the verification engine with the file name to verify.

        DESCRIPTION:
            Advantage of initialize is user no need to give the file name for each execution throughout
            robot.
            User can invoke initialize at any point and override the previous initialize file.

        ARGUMENTS:
            [file=None]
            :param STR file:
                *OPTIONAL* file to verify. Default file is None.
            :param BOOL suppress_log:
                *OPTIONAL* Command response suppressed due to suppress_log flag Set to TRUE.
                        Default suppress_log is False.
            :param BOOL do_parallel:
                *OPTIONAL* For verification of all checks in a file. Default do_parallel is False.
            :param BOOL log_text_output:
                *OPTIONAL* text output to logs
            :param STR is_robot:
                *OPTIONAL* robot call. Default is_robot is None.

        ROBOT USAGE:
            Initialize Verify Engine     file=verify_ospf_interface.yaml

        returns: TRUE if succesfully otherwise FALSE
        """

        # Reinitialize all the data every time initialize called

        self.__init__()
        self.init_global_args = []
        self._is_VE_parallel = kwargs.get("do_parallel", False)
        self.global_suppress_log = kwargs.get("suppress_log", True)
        self.global_log_text_output = kwargs.get("log_text_output", False)

        # Used to setup environment variables
        self._setup()

        # Get process all the files and store the in common place
        self.verification_file = kwargs.get('file', None)
        if self.verification_file is None:
            t.log(level="info", message="File argument is missing to Initialize Verify Engine ")
            if kwargs.get('is_robot', None) is not None:
                raise Exception(
                    "File argument is missing to Initialize Verify Engine")
            return False

        # For each file process the data and update the class variables
        verification_file_pool = self.verification_file.split(',')
        for each_file in verification_file_pool:
            log_file_version(each_file)
            pre_result = self._pre_process_testcases(
                each_file)  # pre-process all the files
            if pre_result['result'] is False:
                t.log(level="error",
                      message="Unable to pre-process the file : " + each_file)
                if kwargs.get('is_robot', None) is not None:
                    raise TobyException("In Initialize Verify Engine, Unable to pre-process the file : " + each_file)
                return False
            temp_global_args = pre_result.get("args", [])
            if not temp_global_args:
                pre_result.pop("args", temp_global_args)
                for index in range(0, len(temp_global_args)):
                    if not isinstance(temp_global_args[index], dict):
                        temp_global_args[index] = {
                            temp_global_args[index]: None}
            self.init_global_args = self._sub_merge_args_list(
                self.init_global_args, temp_global_args)
            self.ve_data.extend(pre_result.get('data', list()))
        self.tmpl_data = copy.deepcopy(self.process_tmpl_data)
        self.pylib = copy.deepcopy(self.process_pylib)
        self.tmpl_file = self.process_tmpl_file

        # Reinitialize the process data...
        self.process_tmpl_file = []
        self.process_tmpl_data = []
        self.process_pylib = []
        t.log(level="debug", message="Initialized with " + self.verification_file + " files")
        return True

    class MyThread(threading.Thread):

        '''General Thread class for multi-threading.'''

        def __init__(
                self,
                group=None,
                target=None,
                name=None,
                args=(),
                kwargs=None,
                # *,
                daemon=None):
            threading.Thread.__init__(
                self, group, target, name, args, kwargs, daemon=daemon)

            self._return = None

        def run(self):
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)

        def join(self):
            Thread.join(self)
            return self._return

    def _execute_testcase(
            self,
            data,
            pre_res_data,
            is_testcase_executed,
            return_result,
            device_list,
            is_get,
            device=None,
            each_tag=False,
            cli_args=[],
            global_args=[],
            checks_robot_arg=None):

        for each_data in data:
            if device is None:
                each_data_key = list(each_data.keys())
                each_device = each_data_key[0]
            else:
                each_device = device
            var = re.search(r'dh\[(\d+)\]', each_device)
            if var is not None:
                device_handle = self._device_handle[int(var.group(1))]
                device_name = each_device
            else:
                device_name = verify_utils.get_key_value(
                    data=self.t_handle,
                    key=each_device +
                    "/system/primary/name",
                    message=", unable to find the device name " +
                    each_device,
                    if_false="")
                if self.is_VE_offline is True:
                    device_handle = True
                else:
                    try:
                        device_handle = t.get_handle(resource=each_device)
                    except BaseException:
                        t.log(level="error",
                              message="UNABLE TO FIND THE DEVICE NAME OF " +
                              each_device)
                        device_handle = False
                    if device_handle is False:
                        if self._is_tc_parallel:
                            return_result.append(False)
                        else:
                            return_result = False
                        continue

            # For each device hierarchy
            if device_name not in pre_res_data.keys():
                pre_res_data.update({device_name: {}})
            if device_name not in self._last_verify_result.keys():
                self._last_verify_result.update({device_name: {}})
            self._last_verify_device_name = device_name
            if each_device in device_list or len(device_list) == 0:
                # check to see if the run is parallel to fetch the device
                # specific data
                if self._is_tc_parallel:
                    device_data = data[each_device]
                else:
                    device_data = each_data[each_device]
                if isinstance(device_data, OrderedDict):
                    device_data_keys = device_data.keys()
                else:
                    device_data_keys = sorted(device_data)

                if not device_data_keys:
                    t.log(level="error", message="No testcases found for device : " +
                          str(each_device)+" in the yaml data")
                    if self._is_tc_parallel:
                        return True
                    else:
                        return_result = False
                        is_testcase_executed = False
                        return is_testcase_executed, return_result

                # For each testcase hierarchy
                for each_tc in device_data_keys:
                    each_tc_data = device_data[each_tc]
                    result = ''
                    if each_tc_data.get('skip', None):
                        # verify if the check name is in the skip list
                        if each_tc in each_tc_data['skip']:
                            t.log(level="debug", message="SKIPPING THE CHECK: "+str(each_tc))
                            # Verify if skipped check name is the only check being called from robot
                            if checks_robot_arg == each_tc:
                                self._last_verify_result = None
                            continue
                    if each_tag is not False:
                        present_tags = each_tc_data.get('tag', [])
                        is_testcase_executed = True
                        if each_tag.upper() in present_tags or each_tag.lower() in present_tags:
                            is_testcase_executed = True
                            result = self._process_testcase(each_tc_data, each_tc, device_handle,
                                                            each_device, device_name, is_get,
                                                            cli_args=cli_args, global_args=global_args)
                    else:
                        is_testcase_executed = True
                        result = self._process_testcase(
                            each_tc_data, each_tc, device_handle, each_device, device_name, is_get,
                            cli_args=cli_args, global_args=global_args)
                    if result is not None:
                        if is_get is True:
                            pre_res_data[device_name].update(result)
                        else:
                            if result is False:
                                t.log(level="info", message="False")
                                if self._is_tc_parallel:
                                    return_result.append(False)
                                else:
                                    return_result = False
                            else:
                                t.log(level="info", message="True")
                                if self._is_tc_parallel:
                                    return_result.append(True)

        if self._is_tc_parallel:
            # Threads expect a boolean value to check
            # if the thread completed successfully.
            return True
        return is_testcase_executed, return_result

    def _execute_testcase_parallel(
            self,
            data,
            pre_res_data,
            is_testcase_executed,
            device_list,
            is_get,
            each_tag=False,
            cli_args=[],
            global_args=[],
            checks_robot_arg=None):
        """
           This function is an intermediate function when that is executed only
           when the VE runs in parallel mode. It creates a thread for each device
           and starts the thread with the target as execute testcase. After the
           execution it joins all the threads.
        """

        thread_list = []
        return_list = []
        self._last_verify_result = {}

        for testcase_data in data:
            device = list(testcase_data)[0]
            try:
                thread_object = self.MyThread(target=self._execute_testcase, args=(
                    testcase_data,
                    pre_res_data,
                    is_testcase_executed,
                    return_list,
                    device_list,
                    is_get, device,
                    each_tag,
                    cli_args,
                    global_args,
                    checks_robot_arg), name=device)

                thread_list.append(thread_object)
                thread_object.start()
            except Exception as e:
                t.log(level="error", message="The thread failed with an exception.")
                raise Exception(e)

        for thread in thread_list:
            thread.join()

        if not return_list and not pre_res_data:
            is_testcase_executed = False
            return is_testcase_executed, False

        if False in return_list:
            return is_testcase_executed, False
        return is_testcase_executed, True

    def verify_all_checks_api(self, **kwargs):
        """
    Verifies all the checks under devices in a text file in Yaml format.

    DESCRIPTION:
        user needs to mention the testcase name which needs to be executed. Specific sub
        testcases/parameter can be invoked using concatenation using : ( colon)

    ARGUMENTS:
        [**kwargs]
        :param STR file:
            *OPTIONAL* Main yaml file to be executed, Will override the initialize file
                if value given. Default file is None.
        :param tag:
            *OPTIONAL* Will be Used for executing subset of testcases
                      #TO DO. Default data is str()[empty STR]
        :param LIST devices:
            *OPTIONAL* Subset the execution based on the device list.
                       Default device is str()[empty STR]
        :param STR data:
            *OPTIONAL* Verify all jvision checks under user given Jvision Data/ Jvision File.
                     Default data is None.
        :param STR specific_test_data:
            *OPTIONAL* verifies the specified test data.Default is set to None.
        :param STR checks_robot_arg:
            *OPTIONAL* checks robot arguments.Default is set to None.
        :param BOOL suppress_log:
            *OPTIONAL* Command response suppressed due to suppress_log
            flag Set to TRUE. Default suppress_log is self.global_suppress_log.
        param suppress_log_limit:
            *OPTIONAL* supresses the logs.

    ROBOT USAGE:
        ${status} =  verify all checks api      file=${verify_file}

    :return: returns Final result as True/False based on all the verification
        """
        # Used to setup environment variables
        self._setup()

        # Initialize the variables
        self.iterator_id += 1
        self._last_verify_result = {}
        self._is_tc_parallel = False
        # Vars().set_global_variable("${VE_LAST_VERIFY_RESULT}", self._last_verify_result)
        verify_file = kwargs.get('file', None)
        verify_data = kwargs.get('data', None)
        verify_specific_data = kwargs.get('specific_test_data', None)
        tag = kwargs.get('tag', str())
        devices_list = kwargs.get('devices', str())
        checks_robot_arg = kwargs.get('checks_robot_arg', None)
        self.suppress_log = kwargs.get(
            'suppress_log', self.global_suppress_log)
        self.suppress_overlimit_log = kwargs.get(
            'suppress_overlimit_log', False)
        self.suppress_log_limit = kwargs.get('suppress_log_limit', 100)
        is_get = False
        if kwargs.get('type', False) == 'get':
            is_get = True

        if not self.log_text_output:
            self.log_text_output = kwargs.get(
                "log_text_output", self.global_log_text_output)

        # Initialize the file to be verified
        self.process_tmpl_data = []
        self.process_data = []
        self.process_pylib = []
        self.global_args = []
        global_args = []

        # Fetching the command line arguments and processing them for
        # substituting in the test case data.

        args = kwargs.get('args', [])
        new_args = {}
        if isinstance(args, dict):
            if len(args.keys()) == 1 and list(args.keys())[0] == 'args':
                new_args = args
            else:
                new_args = {'args': []}
                for key, value in args.items():
                    new_args['args'].append({key: value})
        elif isinstance(args, list):
            new_args = {'args': args}
        cli_args = new_args['args']

        if verify_file is None and verify_data is None and verify_specific_data is None and self.verification_file is None:
            t.log(
                level='error',
                message="file argument is mandatory in 'verify_all_checks_api'\n")
            return False
        data = list()
        if verify_file is None and verify_data is None and verify_specific_data is None:
            verify_file = copy.deepcopy(self.verification_file)
            self.process_data = copy.deepcopy(self.ve_data)
            self.process_pylib = copy.deepcopy(self.pylib)
            self.global_args = copy.deepcopy(self.init_global_args)
        elif verify_file:
            verify_file = verify_file.split(',')
            for each_file in verify_file:
                log_file_version(each_file)
                pre_result = self._pre_process_testcases(
                    file_to_process=each_file)
                if pre_result['result'] is False:
                    return False
                self.process_data.extend(pre_result.get('data', list()))
                temp_global_args = pre_result.get("args", [])
                if temp_global_args != []:
                    pre_result.pop("args", temp_global_args)
                    for index in range(0, len(temp_global_args)):
                        if not isinstance(temp_global_args[index], dict):
                            temp_global_args[index] = {
                                temp_global_args[index]: None}
                self.global_args = self._sub_merge_args_list(
                    self.global_args, temp_global_args)

        elif verify_data:
            src_path = get_log_dir()
            verify_data_file = os.path.join(src_path, 'userdata.yaml')
            with open(verify_data_file, 'w') as outfile:
                outfile.write(verify_data)
            outfile.close()
            pre_result = self._pre_process_testcases(verify_data_file)
            if pre_result['result'] is False:
                return False
            self.process_data.extend(pre_result.get('data', list()))
            self.global_args = pre_result.get("args", [])

        elif verify_specific_data:
            self.process_data.extend(verify_specific_data.get('data', list()))
            self.global_args = verify_specific_data.get("args", [])

        data = copy.deepcopy(self.process_data)
        t.log(level='debug', message="processed data ")
        t.log(level='debug', message=data)

        do_parallel = kwargs.get('do_parallel', None)
        if do_parallel is None:
            self._is_tc_parallel = self._is_VE_parallel
        else:
            self._is_tc_parallel = do_parallel

        device_list = verify_utils.expand_alpha_numeric_string(devices_list)
        tag_list = verify_utils.expand_alpha_numeric_string(tag)
        if not self.t_handle:
            self.t_handle = t.t_dict['resources'].copy()

        if kwargs.get('is_robot', False) is not False:
            '''
               setting default value to fail msg
            '''
            if not device_list:
                self._default_failmsg = "+ VERIFY FAILED: " + \
                    "checks in " + str(verify_file) + " file"
            else:
                self._default_failmsg = "+ VERIFY FAILED: " + \
                    str(device_list) + " specific checks in " + \
                    str(verify_file) + " file"

        # for all testcases
        return_result = True
        is_testcase_executed = True
        start_time = time.time()
        pre_res_data = dict()
        global_args = copy.deepcopy(self.global_args)
        if len(tag_list) == 0:
            if self._is_tc_parallel:
                t.set_background_logger()
                is_testcase_executed, return_result = self._execute_testcase_parallel(
                    data, pre_res_data, is_testcase_executed, device_list, is_get,
                    cli_args=cli_args, global_args=global_args, checks_robot_arg=checks_robot_arg)
                t.process_background_logger()
            else:
                is_testcase_executed, return_result = self._execute_testcase(
                    data, pre_res_data, is_testcase_executed, return_result, device_list,
                    is_get, cli_args=cli_args, global_args=global_args, checks_robot_arg=checks_robot_arg)

        else:
            for each_tag in tag_list:
                t.log(level="debug", message='TAG : ' + each_tag)
                if self._is_tc_parallel is True:
                    t.set_background_logger()
                    is_testcase_executed, return_result = self._execute_testcase_parallel(
                        data, pre_res_data, is_testcase_executed, device_list, is_get,
                        each_tag=each_tag, cli_args=cli_args, global_args=global_args)
                    t.process_background_logger()
                else:
                    is_testcase_executed, return_result = self._execute_testcase(
                        data, pre_res_data, is_testcase_executed, return_result, device_list,
                        is_get, each_tag=each_tag, cli_args=cli_args, global_args=global_args)

        t.log(level="info", message="------ Time taken for the tests to run : %s seconds ------" % (time.time() - start_time))
        global_args = []
        cli_args = []
        self.global_args = []
        t.log(level='debug', message="LAST_VERIFY_RESULT: " + str(self._last_verify_result))
        self._last_verify_result = verify_utils.extract_data(
            self._last_verify_result, 'value')
        t.log(level='debug', message="LAST RESULT:")
        t.log(level='debug', message=self._last_verify_result)
        # Vars().set_global_variable("${VE_LAST_VERIFY_RESULT}", self._last_verify_result)
        if is_testcase_executed is False:
            t.log(level='error', message="No Testcase Executed")
            return_result = False
        if is_get is True:
            return pre_res_data

        if not return_result:
            fail_message = "Verify_All_Check_API: failed testcase data."
            verify_utils.create_ve_debug_log(data, fail_message)

        # Raise exeception if it is a robot call
        if kwargs.get('is_robot', False) is not False:
            '''
            #   print fail message if verify fails
            #   do not print fail message if type is get
            '''
            failmsg = kwargs.get('failmsg', self._default_failmsg)
            if isinstance(return_result, bool) and return_result is False:
                raise TobyException(failmsg)

        return return_result

    def verify_specific_checks_in_parallel(self, **kwargs):
        """
        Verifies all the checks parallely for each device.

        DESCRIPTION:
            Verification Engine provides an option to run tests in parallel to reduce the
            time of execution to a great extent. Essentially the underlying mechanism is to
            execute the tests on different devices at the same point of time which reduces
            over all execution time.
            To verify specific checks in parallel mode the checks need to be a list of
            dictionaries with each dictionary containing device and the checks that need
            to be run on that device.

        ARGUMENTS:
            [kwargs]
            :param STR test_data:
                *OPTIONAL* List of checks in the format{'devices':'d1,d2','checks':'c1,c2'}.
                Default test_data is None.
            :param STR file:
                *OPTIONAL* Main yaml file to be executed, Will override the initialize file
                if value given. Default File is None.
            :param BOOL suppress_log:
                *OPTIONAL* Command response suppressed due to suppress_log flag Set to TRUE.
                Default suppress_log is False.
            :params BOOL suppress_overlimit_log:
                *OPTIONAL* Supress the log limits.Default is set to False.
            :param INT suppress_log_limit:
                *OPTIONAL* supress line number of log limit.
                            Deafult us set to 100
            :param BOOLEAN is_robot:
                *OPTIONAL*Raise exeception if it is a robot call.
                          Default is set to False.
            :param STR verify_file:
                *OPTIONAL* verification file name.

        ROBOT USAGE:
            Verify Specific Checks In Parallel     test_data=List of checks.

       :return: returns Final result as True/False based on all the verification
        """
        # Used to setup environment variables
        self._setup()
        device_list = []
        self.dh_count = -1
        self._device_handle = []
        failmsg1 = None

        verify_parallel = True
        do_parallel = True
        yaml_data = {}
        specific_yaml_data = OrderedDict({"data": [], "args": {}})
        test_data = kwargs.get('list_checks', None)
        verify_main_file = kwargs.get('file', None)
        self.suppress_log = kwargs.get(
            'suppress_log', self.global_suppress_log)
        self.log_text_output = kwargs.get(
            "log_text_output", self.global_log_text_output)
        self.suppress_overlimit_log = kwargs.get(
            'suppress_overlimit_log', False)
        self.suppress_log_limit = kwargs.get('suppress_log_limit', 100)
        if test_data is None:  # omkar isn't the log statement redundant here?
            failmsg = "Mandatory argument list_checks not provided."
            t.log(level="error", message=failmsg)
            raise Exception(failmsg)

        for data in test_data:
            device = data.get("device", None)
            device_handle = data.get("device_handle", None)
            if not device and not device_handle:
                message = "device parameter not provided for the element: "+str(data)
                t.log(level='error', message=message)
                return False
            elif device:
                if ',' in device or device[0] == '[' and device[-1] == ']':
                    message = "only one device allowed for the argument 'device'"
                    t.log(level='error', message=message)
                    return False
            else:
                self.dh_count = self.dh_count + 1
            if device in device_list:
                message = 'A thread with the same device already started, '+\
                          'threads with same device are strongly discouraged.'
                t.log(level='error', message=message)
            if device:
                device_list.append(device)
            checks = data.get("checks", None)
            if not checks:
                message = "checks parameter not provided for the element: "+str(data)
                t.log(level='error', message=message)
                return False
            args = data.get("args", None)
            verify_file = data.get("file",verify_main_file)
            value = data.get('value', None)
            operator = data.get('operator', None)
            _parameters = data.get('parameters', None)
            _parameters = copy.deepcopy(_parameters)
            cmd = data.get('cmd', None)
            xpath_filter = data.get('xpath_filter', None)
            iterate_data = data.get('dict',None)

            yaml_data = self.verify_specific_checks_api(
                devices=device,
                device_handle=device_handle,
                checks=checks,
                verify_parallel=verify_parallel,
                suppress_log=self.suppress_log,
                suppress_overlimit_log=self.suppress_overlimit_log,
                suppress_log_limit=self.suppress_log_limit,
                args=args,
                file=verify_file,
                value=value,
                operator=operator,
                parameters=_parameters,
                cmd=cmd,
                dict=iterate_data,
                xpath_filter=xpath_filter)

            specific_yaml_data["args"] = self._merge_args_list(
                specific_yaml_data["args"], yaml_data["args"])
            specific_yaml_data["data"].extend(yaml_data["data"])

        result = self.verify_all_checks_api(
            specific_test_data=specific_yaml_data,
            do_parallel=do_parallel)

        if not result:
            failmsg1 = "verify_specific_checks_in_parallel_API: failed testcase data."

        # Raise exeception if it is a robot call
        if kwargs.get('is_robot', False) is not False:
            '''
            #   print fail message if verify fails
            #   do not print fail message if type is get
            '''
            failmsg = kwargs.get('failmsg', failmsg1)
            if isinstance(result, bool) and result is False:
                raise Exception(failmsg)
        self.dh_count = 0
        self._device_handle = []
        return result

    def _get_testcase_result(self, segregated_data, device_handle, tc_name, is_get,
                             cli_args=[], global_args=[], expanded_tc_datas=[]):
        """
           Takes the segregated data from self._process_testcase and calls
           self._verify_testcase or self._iterator depending on the presence
           of iterator in the testcase data.
        """
        value = True
        if is_get:
            value = {}
        self.iterate_until_present = False
        t.log(level='debug', message="segregated data: "+str(segregated_data))
        if isinstance(segregated_data, list):
            for data in segregated_data:
                # If the data variable is a list, then it is a list of
                # dictionaries, which are individual testcases that
                # have iterator in it.
                if isinstance(data, list):
                    self.iterate_until_present = True
                    # Iterate testcase Dictionary
                    for dicts in data:
                        # pop the iterator from the testcase and pass the
                        # iterator value and tc_data to self._iterator
                        iterate, tc_dict = self._pop_iterator_data(dicts)
                        iterate_type = list(iterate)[0]
                        if is_get:
                            expected_return = "_ANY_DATA"
                        else:
                            expected_return = True
                        kwargs = {"function": self._verify_testcase, "iterate_type": iterate_type,
                                  "tc_data": tc_dict, "expected_return": expected_return,
                                  "device_handle": device_handle, "tc_name": tc_name, "is_get": is_get,
                                  "is_iterate": True, "cli_args": cli_args, "global_args": global_args,
                                  "expanded_tc_datas":expanded_tc_datas}
                        kwargs.update(iterate[iterate_type])
                        iterator_value = self._iterator(**kwargs)
                        if is_get:
                            # Merging the previous is_get result with the new one.
                            value = verify_utils.merge_dicts(
                                value, iterator_value)
                        else:
                            value = value and iterator_value
                # If the data variable is a dictionary, then it is a
                # dictionary of all the testcases and sub testcases
                # that do not have iterator in it.
                if isinstance(data, dict):
                    self.iterate_until_present = False
                    if not data:
                        continue
                    kwargs = {"tc_data": data, "device_handle": device_handle,
                              "tc_name": tc_name, "is_get": is_get,
                              "cli_args": cli_args, "global_args": global_args,
                              "expanded_tc_datas":expanded_tc_datas}
                    result_value = self._verify_testcase(**kwargs)
                    if is_get:
                        value = verify_utils.merge_dicts(value, result_value)
                    else:
                        value = value and result_value
        return value

    def _process_testcase(
            self,
            tc_data,
            tc_name,
            device_handle,
            device,
            device_name,
            is_get,
            cli_args=None,
            global_args=None):
        self.response_optimize_iterator = False
        expanded_tc_datas = []
        return_dict = {}
        final_result = True
        if 'iterator' in list(tc_data.keys()):
            self.response_optimize_iterator = True
            # Get the height of iterator.
            height = self._get_iterator_height(tc_data['iterator'])
            # Generate dataset.
            self._generate_dataset(
                tc_data['iterator'], height, [], [], tc_data, expanded_tc_datas)
        else:
            expanded_tc_datas.append(tc_data)
        for index, each_tc in enumerate(expanded_tc_datas):
            t.log(level='debug', message="testcase data :")
            t.log(level='debug', message=dict(each_tc))
            if is_get and each_tc.get('type', None) is None:
                return None

            if len(expanded_tc_datas) == 1:
                t.log(level="info", message="Executing Testcase  :" + tc_name + ", On device :" + device + " [" + device_name + "]")
                t.log(level="info", message="-------------------------------------------------------------------------")
            else:
                t.log(level="info", message="Executing Testcase  :" + tc_name +
                    "[ " + str(index) + " ]"
                    ", On device :" + device + " [" + device_name + "]")
                t.log(level="info", message="-------------------------------------------------------------------------")
                tc_name = tc_name + str(index)

            if each_tc.get('expr', None) and not (each_tc.get('iterate_until', None)
                                                  or each_tc.get('iterate_for', None)):
                segregated_data = [[], each_tc]
            else:
                segregated_data = self._segregate_tc_data(each_tc)
            # Clear these global variables to avoid corruption of tc_data in the next testcase.
            self.iterate_tc_data = []
            self.noiterate_tc_data = {}
            self.noiterate_results = []
            self.iterate_results = []
            result = self._get_testcase_result(
                segregated_data, device_handle, tc_name, is_get,
                cli_args=cli_args, global_args=global_args,
                expanded_tc_datas=expanded_tc_datas)
            if isinstance(result, bool) and (not result):
                fail_message = " Process_Testcase: failed testcase data on device: " + \
                    str(device)
                verify_utils.create_ve_debug_log(each_tc, fail_message)
            tc_message_data = {'passmsg': each_tc.get('passmsg', None),
                               'failmsg': each_tc.get('failmsg', None)}
            self._substitute_variables(tc_message_data, self.final_args)
            self._put_tc_result_msg(
                tc_name, tc_message_data, device_name, result)

            if result is False:
                final_result = False
            elif is_get and each_tc.get('type', None) == 'get':
                return_dict.update(result)

        if is_get is True and tc_data.get('type', None) == 'get':
            return return_dict
        else:
            self._put_tc_result_msg(
                tc_name, tc_data, device_name, final_result)
            return final_result

    def _put_tc_result_msg(self, tc_name, tc_data, device_name, result):

        if isinstance(result, bool):
            if result is False and tc_data.get('failmsg', None) is not None:
                t.log(level="info", message="CHECKS FAILED: " + str(tc_data['failmsg']) + " on " + device_name)
                self._default_failmsg = self._default_failmsg + "\n    ++ CHECKS FAILED: " + \
                    str(tc_data['failmsg']) + \
                    " ( " + tc_name + " on " + device_name + " )"
                # t.log_console("\n    TEST FAILED: " + str(tc_data['failmsg']) )
            elif result is False and tc_data.get('failmsg', None) is not None:
                t.log(level="info", message="CHECKS FAILED: " + tc_name + " on " + device_name)
                self._default_failmsg = self._default_failmsg + \
                    "\n    ++ CHECKS FAILED: " + tc_name + " on " + device_name
                # t.log_console("\n    TEST FAILED: " + "verification of "+ tc_name+ " failed" )
            elif result is True and tc_data.get('passmsg', None) is not None:
                t.log(level="info", message="CHECKS PASSED: " + str(tc_data['passmsg']) + " ( on " + device_name + " )")
                # t.log_console("\n    TEST PASSED: " + str(tc_data['passmsg']) )
            elif result is True and tc_data.get('passmsg', None) is None:
                t.log(level="info", message="CHECKS PASSED: " + tc_name + " on " + device_name)
                # t.log_console("\n    TEST PASSED: " + "verification of "+ tc_name+ " passed")

    def _put_sub_tc_result_msg(self, tc_name, tc_data, result):

        if isinstance(result, bool):
            if result is False and tc_data.get('failmsg', None) is not None:
                t.log(level="info", message="SUBCHECKS FAILED: " + str(tc_data['failmsg']))
            elif result is False and tc_data.get('failmsg', None) is None:
                t.log(level="info", message="SUBCHECKS FAILED: " + tc_name)
            elif result is True and tc_data.get('passmsg', None) is not None:
                t.log(level="info", message="SUBCHECKS PASSED: " + str(tc_data['passmsg']))
            elif result is True and tc_data.get('passmsg', None) is None:
                t.log(level="info", message="SUBCHECKS PASSED: " + tc_name)

    def _merge_template_data(self, tmpl_data, tc_data, tc_name, nested=False):
        """
        build the new testcase from a given template
        :param tmpl_data: Testcase data from template data
        :param tc_data: Available testcase Data In main yaml data
        :param tc_name: Testcase Name
        :return:
        """
        if not nested:
            t.log(level='debug', message="template data :")
            t.log(level='debug', message=tmpl_data)
            t.log(level='debug', message="Testcase data :")
            t.log(level='debug', message=dict(tc_data))

        include_all = tc_data.get("include_all", None)
        tm_data = tmpl_data[tc_name]
        if isinstance(tc_data, OrderedDict):
            final_yaml = OrderedDict()
        else:
            final_yaml = {}
        if bool(tc_data) is False:
            final_yaml = tm_data

        process_list = [
            'template',
            'group',
            'tag',
            'cmd',
            'include_all',
            'skip',
            'type',
            'value',
            'operator',
            'return_type',
            'xpath',
            'iterator',
            'cmd_timeout',
            'cmd_pattern',
            'format',
            'regexp',
            'grep',
            'match_all',
            'regexp_flags',
            'grep_flags',
            'execute_on',
            'iterate_until',
            'iterate_for',
            'func',
            'preq',
            'expr',
            'xpath_filter',
            'failmsg',
            'passmsg',
            'suppress_log']

        for each_process in process_list:
            if each_process in list(tc_data.keys()):
                final_yaml[each_process] = tc_data[each_process]
            elif each_process in list(tm_data.keys()):
                final_yaml[each_process] = tm_data[each_process]

        merged_args = []
        all_tc_keys = []
        tc_args = []
        tm_args = []
        if 'args' in list(tc_data.keys()):
            tc_args = tc_data['args']
        if 'args' in list(tm_data.keys()):
            tm_args = tm_data['args']

        for each_element in tm_args:
            if isinstance(each_element, dict):
                merged_args.append(each_element)
        for each_dict in merged_args:
            all_tc_keys.extend(list(each_dict.keys()))

        for each_arg_dict in tc_args:
            if isinstance(each_arg_dict, dict):
                (key, val), = each_arg_dict.items()
                if key not in all_tc_keys:
                    merged_args.append(each_arg_dict)
                else:
                    for each_x in range(0, len(merged_args)):
                        (key_merged_args,
                         val_merged_args), = merged_args[each_x].items()
                        if key == key_merged_args:
                            merged_args[each_x] = {key: val}

        final_yaml['args'] = merged_args
        is_testcase_present = False
        for each_test_key in list(tc_data.keys()):
            if isinstance(
                    tc_data[each_test_key],
                    dict) and each_test_key not in [
                        'iterate_until',
                        'iterate_for']:
                is_testcase_present = True
                if each_test_key not in list(
                        tm_data.keys()) and each_test_key in list(
                            tc_data.keys()):
                    # Copy testcase data from data
                    final_yaml[each_test_key] = tc_data[
                        each_test_key]
                if each_test_key in list(
                        tm_data.keys()) and each_test_key in list(
                            tc_data.keys()):

                    # If :{} the just copy all from tmp file
                    if len(list(tc_data[each_test_key].keys())) == 0:
                        final_yaml[each_test_key] = tm_data[
                            each_test_key]
                    # proceeding for parameters
                    if each_test_key == 'parameters':
                        if isinstance(tc_data, OrderedDict):
                            final_yaml[each_test_key] = OrderedDict()
                        else:
                            final_yaml[each_test_key] = {}
                        if tm_data.get('_all_parameters', None) is not None:
                            final_yaml['_all_parameters'] = tm_data['_all_parameters']
                        else:
                            final_yaml['_all_parameters'] = tm_data[each_test_key]

                        element_data = tc_data.get(each_test_key, None)
                        if element_data is None:
                            final_yaml[each_test_key] = tc_data[
                                each_test_key]
                        else:

                            for each_element_testcase in list(element_data.keys()):
                                # Make sub-testcase
                                sub_tc_data = tm_data[each_test_key].get(
                                    each_element_testcase, None)
                                if sub_tc_data is None:
                                    final_yaml[each_test_key][each_element_testcase] = tc_data[
                                        each_test_key][each_element_testcase]
                                else:
                                    if tm_data.get('_all_parameters', None):
                                        final_yaml[each_test_key][each_element_testcase] = tm_data['_all_parameters'][
                                            each_element_testcase]
                                    else:
                                        final_yaml[each_test_key][each_element_testcase] = tm_data[each_test_key][
                                            each_element_testcase]

                                    # For each sub-testcase place the values for the
                                    # operator and value
                                    for each_element_testcase_keys in list(element_data[each_element_testcase].keys()):
                                        final_yaml[each_test_key][each_element_testcase][each_element_testcase_keys] = \
                                            element_data[each_element_testcase][
                                                each_element_testcase_keys]  # replace the user given value
                                        final_yaml['_all_parameters'][each_element_testcase][each_element_testcase_keys] = \
                                            element_data[each_element_testcase][
                                                each_element_testcase_keys]  # replace the user given value
                            # check if include_all is set and include all parameters accordingly
                            template_parameters = final_yaml.get(
                                "_all_parameters", None)
                            if include_all == "all" or include_all == "parameters":
                                if template_parameters:
                                    for each_template_parameter in list(template_parameters.keys()):
                                        if each_template_parameter not in list(element_data.keys()):
                                            final_yaml["parameters"][each_template_parameter] = \
                                                final_yaml["_all_parameters"][each_template_parameter]
                                final_yaml.pop("include_all")
                            if len(list(element_data.keys())) == 0:
                                final_yaml[each_test_key] = tm_data[
                                    each_test_key]
                    # If parameters is inside the sub-testcase
                    elif 'parameters' in tc_data[each_test_key]:
                        non_element_tc_data = tc_data[
                            each_test_key]
                        non_keys = list(non_element_tc_data.keys())
                        element_data = tc_data[
                            each_test_key]['parameters']
                        if isinstance(tc_data, OrderedDict):
                            final_yaml[each_test_key] = OrderedDict(
                                {'parameters': {}})
                        else:
                            final_yaml[each_test_key] = {'parameters': {}}

                        # If Local xpath is present
                        if tm_data.get(each_test_key, None) is None:
                            final_yaml[each_test_key] = tc_data[
                                each_test_key]
                        else:

                            if 'xpath' in list(tm_data[each_test_key].keys()):
                                final_yaml[each_test_key]['xpath'] = tm_data[
                                    each_test_key]['xpath']
                            if 'xpath' in non_keys:
                                final_yaml[each_test_key]['xpath'] = tc_data[
                                    each_test_key]['xpath']
                            # Copy each testcase inside the parameters

                            for each_element_testcase in list(
                                    element_data.keys()):
                                if tm_data[each_test_key]['parameters'].get(
                                        each_element_testcase, None) is None:
                                    final_yaml[each_test_key]['parameters'][
                                        each_element_testcase] = tm_data[each_test_key][
                                            'parameters'][each_element_testcase]
                                else:
                                    final_yaml[each_test_key]['parameters'][
                                        each_element_testcase] = tm_data[each_test_key][
                                            'parameters'][each_element_testcase]
                                    # Replace the value and operator
                                    for each_element_testcase_keys in list(
                                            element_data[each_element_testcase].keys()):
                                        final_yaml[each_test_key]['parameters'][each_element_testcase][
                                            each_element_testcase_keys] = \
                                            element_data[each_element_testcase][
                                                each_element_testcase_keys]
                            if len(list(element_data.keys())) == 0:
                                final_yaml[each_test_key]['parameters'] = tm_data[
                                    each_test_key]['parameters']

                    else:

                        # Direct Sub-testcase call is there
                        if tm_data.get(each_test_key, None) is None:
                            final_yaml[each_test_key] = tc_data[
                                each_test_key]
                        else:
                            final_yaml[each_test_key] = tm_data[each_test_key]
                            for each_parameter in list(
                                    tc_data[each_test_key].keys()):
                                final_yaml[each_test_key][each_parameter] = tc_data[
                                    each_test_key][each_parameter]
        if is_testcase_present is False:
            for each_test_key in list(tm_data.keys()):
                if isinstance(tm_data[each_test_key], dict):
                    final_yaml[each_test_key] = tm_data[each_test_key]
        if not nested:
            t.log(
                level='debug',
                message="YAML data formed after merging template data and test case data.")
            t.log(level='debug', message=dict(final_yaml))
        return final_yaml

    def _substitute_variables(self, tc_data, tc_args):
        global tv
        if isinstance(tc_data, dict):
            for key, value in tc_data.items():
                if (isinstance(value, dict) or
                        isinstance(value, list) or
                        isinstance(value, tuple)):
                    self._substitute_variables(value, tc_args)
                else:
                    temp_args = verify_utils._get_temp_args(tc_args)
                    for each_arg in list(temp_args.keys()):

                        if "var['" + each_arg + "']" in str(value):
                            t.log(level='debug', message="Arg value:")
                            t.log(level='debug', message=temp_args[each_arg])
                            val_type = type(temp_args[each_arg])
                            temp_val = str(temp_args[each_arg])
                            # if k == "jkey_pattern":
                            #    temp_val = re.escape(temp_value)
                            value = value.replace(
                                "var['" + each_arg + "']", temp_val)
                            t.log(level='debug',
                                  message="Value after substituting Arg value:")
                            t.log(level='debug', message=value)
                            if val_type in [float, int] and value == temp_val:
                                tc_data[key] = val_type(value)
                            else:
                                tc_data[key] = value
                    var = re.findall(r'tv\[.*?\]', str(value), re.I)
                    for i in range(0, len(var)):
                        if not re.search(r'<<.+>>', var[i]):
                            # Trying replacing tv vars.
                            try:
                                if key == "jkey_pattern":
                                    line = re.sub(
                                        r"tv\[.*?\]", re.escape(str(eval(var[i]))), str(value), 1)
                                else:
                                    line = re.sub(
                                        r"tv\[.*?\]", str(eval(var[i])), str(value), 1)
                                value = line
                                tc_data[key] = line
                            except KeyError:
                                t.log(level="warn", message="wrong tv var "
                                      + var[i])

                    # Used to replace ROBOT Variables
                    if self._is_robot is True:
                        var = re.findall(r'\$\{.*?\}', str(value), re.I)
                        for i in range(0, len(var)):
                            robot_var = var[i]
                            robot_value = BuiltIn().get_variable_value(str(robot_var))

                            if value is not None:
                                line = re.sub(
                                    re.escape(robot_var), robot_value, str(value), 1)
                                value = line
                                tc_data[key] = line
                            else:
                                t.log(level="debug", message="ROBOT VARIABLE ( " + robot_var + " )  IS NOT FOUND ")

        elif isinstance(tc_data, list) or isinstance(tc_data, tuple):

            for item_index in range(0, len(tc_data)):
                if isinstance(tc_data[item_index], str):
                    temp_args = verify_utils._get_temp_args(tc_args)
                    for each_arg in list(temp_args.keys()):
                        if "var['" + each_arg + "']" in str(tc_data[item_index]):
                            temp_val = str(temp_args[each_arg])
                            tc_data[item_index] = tc_data[item_index].replace(
                                "var['" + each_arg + "']", temp_val)
                    var = re.findall(
                        r'tv\[.*?\]', str(tc_data[item_index]), re.I)
                    for i in range(0, len(var)):
                        if not re.search(r'<<.+>>', var[i]):
                            # Trying replacing tv vars.
                            try:
                                line = re.sub("tv\[.*?\]", str(eval(var[i])), str(tc_data[item_index]), 1)
                                tc_data[item_index] = line
                            except KeyError:
                                t.log(level="warn", message="wrong tv var "
                                      + var[i])
                else:
                    self._substitute_variables(tc_data[item_index], tc_args)

    def _form_device_specific_testcase(self, tc_data, device_list):
        """
        makes Every separate to device and make list of all testcases
        """
        device_specific_data = []
        device_pool = verify_utils.expand_alpha_numeric_string(device_list)
        for each_device in device_pool:
            device_specific_data.append({each_device: tc_data})
        return device_specific_data

    def _expand_file_list(self, file_list):
        # file_list = verify_data.get('use_template', [])
        t.log(level='info', message='Files before expansion.')
        t.log(level='info', message=file_list)
        keys_list = []
        for i in range(0, len(file_list)):
            keys_list.append(str(i))
        file_dict = dict(zip(keys_list, file_list))
        self._substitute_variables(file_dict, [])
        file_list = []
        for key in keys_list:
            if '/' in file_dict[key]:
                exp = file_dict[key].split('/')[-1]
                path = file_dict[key].replace(exp, '')
                for files in fnmatch.filter(os.listdir(path), exp):
                    file_list.append(os.path.join(path, files))
            else:
                file_list.append(file_dict[key])
        t.log(level='info', message='Files after expansion.')
        t.log(level='info', message=file_list)
        return file_list

    def _source_templates(self, verify_data, file=None, level=0):
        """
        find the particular template data from the list of files and return the template data

        """
        self.process_pylib.extend(verify_data.get('use_library', []))
        file_list = self._expand_file_list(verify_data.get('use_template', []))
        self.process_tmpl_file.extend(file_list)
        is_tmpl_present_in_file = None
        nested_tmpl_data = None
        temp_global_args = []
        nested_tmpl_args = []
        if file is not None:
            is_tmpl_present_in_file = file.get('verify_tmpl', None)
            if is_tmpl_present_in_file is None:
                is_tmpl_present_in_file = file.get('verify_template', None)
        source_file_data = []

        if is_tmpl_present_in_file is not None:
            # Look for any Generic templates being used under each check of user template
            self._merge_generic_tmpl(is_tmpl_present_in_file)

            source_file_data.append(is_tmpl_present_in_file)

        for each in range(0, len(file_list)):
            t.log(level='debug', message="Looping through the file list...")
            tmpdata = verify_utils.get_yaml_data_as_dict(
                file_list[each], self.keywords, self.yaml_file_data)
            if not tmpdata:
                t.log(level='error', message='Unable to fetch the yaml data of '+str(file_list[each]))
            else:
                if tmpdata.get('verify_tmpl') or tmpdata.get('verify_template'):
                    if tmpdata.get('verify_tmpl'):
                        if tmpdata['verify_tmpl'].get('use_template'):
                            nested_tmpl_data, nested_tmpl_args = self._source_templates(
                                tmpdata['verify_tmpl'],
                                level=level+1)
                    elif tmpdata.get('verify_template'):
                        if tmpdata['verify_template'].get('use_template'):
                            nested_tmpl_data, nested_tmpl_args = self._source_templates(
                                tmpdata['verify_template'],
                                level=level+1)

            tmp_file_data_tmpl = verify_utils.get_key_value(
                data=tmpdata, key='verify_tmpl', message="in " + file_list[each], if_false=False)
            tmp_file_data_verify = verify_utils.get_key_value(
                data=tmpdata, key='verify', message="in " + file_list[each], if_false=False)
            if tmp_file_data_tmpl is not False:
                t.log(level='debug', message="User tmpl data: " +
                      str(tmp_file_data_tmpl))

                # Look for any Generic templates being used under each check of user template
                self._merge_generic_tmpl(tmp_file_data_tmpl)

                if not nested_tmpl_data:
                    source_file_data.append(tmp_file_data_tmpl)
                temp_global_args = tmp_file_data_tmpl.get('args', [])
                if temp_global_args != []:
                    tmp_file_data_tmpl.pop("args", temp_global_args)
                    for index in range(0, len(temp_global_args)):
                        if not isinstance(temp_global_args[index], dict):
                            temp_global_args[index] = {
                                temp_global_args[index]: None}
            else:
                tmp_file_data_tmpl = verify_utils.get_key_value(
                    data=tmpdata,
                    key='verify_template',
                    message="in " + file_list[each],
                    if_false=False)
                if tmp_file_data_tmpl is not False:
                    t.log(level='debug', message="User Template data: " +
                          str(tmp_file_data_tmpl))

                    # Look for any Generic templates being used under each check of user template
                    self._merge_generic_tmpl(tmp_file_data_tmpl)

                    if not nested_tmpl_data:
                        source_file_data.append(tmp_file_data_tmpl)
                    temp_global_args = tmp_file_data_tmpl.get('args', [])
                    if temp_global_args != []:
                        tmp_file_data_tmpl.pop("args", temp_global_args)
                        for index in range(0, len(temp_global_args)):
                            if not isinstance(temp_global_args[index], dict):
                                temp_global_args[index] = {
                                    temp_global_args[index]: None}

            if nested_tmpl_data:
                final_yaml_data = []
                t.log(level='debug', message=str(file_list[each]) +
                      " template data before merging:")
                t.log(level='debug', message=dict(tmp_file_data_tmpl))
                t.log(level='debug', message=str(file_list[each]) +
                      " template's nested data before merging:")
                t.log(level='debug', message=nested_tmpl_data)

                for each_nested_data in nested_tmpl_data:
                    merged_data = self._merge_nested_template_data(
                        tmp_file_data_tmpl, each_nested_data)
                    final_yaml_data.append(merged_data)

                t.log(level='debug', message=str(file_list[each]) +
                      " template data after merging with the nested templates:")
                t.log(level='debug', message=final_yaml_data)
                source_file_data.extend(final_yaml_data)

            if tmp_file_data_verify is False and tmp_file_data_tmpl is False:
                t.log(level='debug', message="NO data found in " +
                      file_list[each])
                continue

            if tmp_file_data_verify is not False:
                t.log(level='debug', message="Template verify data: " +
                      str(tmp_file_data_verify))

                # Look for any Generic templates being used under each check of user template
                self._merge_generic_tmpl(tmp_file_data_verify)

                source_file_data.append(tmp_file_data_verify)

            if nested_tmpl_args:
                temp_global_args = self._sub_merge_args_list(
                    temp_global_args, nested_tmpl_args)
            if level == 0:
                self.global_args = self._sub_merge_args_list(
                    self.global_args, temp_global_args)

        if level == 0:
            self.process_tmpl_data.extend(source_file_data)
        else:
            return source_file_data, temp_global_args

    def _merge_nested_template_data(self, tmpl_data, nested_tmpl_data):
        """
           Merges the template data with it's nested template.

           Parameters:
               tmpl_data - User template data
               nested_tmpl_data - template data of the template defined
                                  in the user template.
           Return:
               User template data after merging with the nested template data.
        """
        temp_nested_tmpl_data = copy.deepcopy(nested_tmpl_data)
        for nested_key in nested_tmpl_data:
            if nested_key in tmpl_data:
                each_nested_template_data = nested_tmpl_data[nested_key]
                temp_nested_tmpl_data.pop(nested_key)
                t.log(level='debug', message="template testcase :")
                t.log(level='debug', message={
                    nested_key: tmpl_data[nested_key]})
                t.log(level='debug', message="nested template testcase :")
                t.log(level='debug', message={
                    nested_key: each_nested_template_data})

                tmpl_data[nested_key] = self._merge_template_data(
                    {nested_key: each_nested_template_data},
                    tmpl_data[nested_key],
                    nested_key,
                    nested=True)
                t.log(
                    level='debug',
                    message="YAML data formed after merging template and nested template test case")
                t.log(level='debug', message=tmpl_data[nested_key])

        tmpl_data.update(temp_nested_tmpl_data)
        return tmpl_data

    def _merge_generic_tmpl(self, tmpl_data):
        '''Support for usage of generic template from user template.

           Parameters:
                 tmpl_data - User template data
           Return:
                 None. This method will only update the tmpl_data.'''

        t.log(level='debug',
              message="Looking for any Generic template used under user template...")
        usr_tmpl_tc_list = [key for key in list(
            tmpl_data.keys()) if isinstance(tmpl_data[key], dict)]
        t.log(level='debug', message="usr_tmpl_tc_list: " + str(usr_tmpl_tc_list))
        for each_tc in usr_tmpl_tc_list:
            each_tc_keys = list(tmpl_data[each_tc].keys())
            t.log(level='debug', message="Testcase '" +
                  each_tc + "' attrs: " + str(each_tc_keys))
            if 'template' not in each_tc_keys:
                continue
            tmpl_name = tmpl_data[each_tc]['template']
            #gen_tmpl_data = self._search_template(tmpl_name)
            # if gen_tmpl_data is False and re.match(r'^j_check_.*', tmpl_name) is not None:
            if re.match(r'^j_check_.*', tmpl_name) is not None:
                t.log(level='debug',
                      message="From user template, proceeding with Generic Template Search for " + tmpl_name)
                gen_tmpl_data = self._check_generic_template(tmpl_name)
            else:
                t.log(level='error',
                      message="Usage of non-generic template in user template in check '"
                      + each_tc + "'")
                continue
            # if gen_tmpl_data is False:
            #    t.log(level='debug', message="Proceeding with next one...")
            #    continue
            formed_gen_tmpl_data = self._merge_template_data(
                gen_tmpl_data, tmpl_data[each_tc], tmpl_name)
            verify_utils._replace_value(tmpl_data,
                                        formed_gen_tmpl_data,
                                        each_tc)  # replace for the normal flow

    def _search_template(self, template_name, template_data=None):
        """
        Returns the template data from all tamplate data
        :param template_name: testcase data to be find
        :param template_data: explicitly giving data
        :return:
        """
        if not self.t_handle:
            self.t_handle = t.t_dict['resources'].copy()
            self._make_ifd_tvar()
            # self.t_handle = t.t_dict.copy()
        # device_list = list(self.t_handle['resources'].keys())
        device_list = list(self.t_handle.keys())
        tmpl_file = None
        if template_data is None:
            template_data = copy.deepcopy(self.process_tmpl_data)
        is_device_present = False
        device = None

        for each_data in range(0, len(template_data)):
            tmp_keys = list(template_data[each_data].keys())
            for each_test in tmp_keys:
                device_expand = verify_utils.expand_alpha_numeric_string(
                    each_test)

                # if device present
                for each_device in device_expand:
                    if each_device in device_list:
                        new_tmp_keys = list(
                            template_data[each_data][each_test].keys())
                        if template_name in new_tmp_keys:
                            tmpl_file = each_data
                            device = each_test
                            is_device_present = True
                            break
                    if is_device_present is True:
                        break

            if is_device_present is True:
                break
            if template_name in tmp_keys:
                tmpl_file = each_data
                break
        if tmpl_file is None:
            t.log(level='debug', message="TAMPLATE DATA NOT FOUND FOR " +
                  template_name + " with CMD IN INCLUDE TMPL FILES")
            return False

        if is_device_present is False:
            return {template_name: template_data[tmpl_file][template_name]}
        else:
            return {
                template_name: template_data[tmpl_file][device][template_name]}

    def _pre_process_testcases(self, file_to_process):
        """
        This Method pre-process the testcases like form testcase for template and makes device
        specific value n operator
        :param file_to_process: Yaml file to process
        :return: return the final list to be processed
        """

        # Fetch the file data
        file_data = verify_utils.get_yaml_data_as_dict(
            file_to_process, self.keywords, self.yaml_file_data)
        if file_data is False:
            return {'result': False}

        # Get the verify : data
        data = verify_utils.get_key_value(data=file_data, key='verify',
                                          message="not found", if_false=False)
        if data is False:
            return {'result': False}
        global_args = data.get("args", [])
        if global_args != []:
            data.pop("args", global_args)

        each_device_specific_data = []

        # Get the template data and store in global template data including the
        # temp data in the file itself,if present
        self._source_templates(data, file=file_data)

        if not self.t_handle:
            self.t_handle = t.t_dict['resources'].copy()
            self._make_ifd_tvar()
            # self.t_handle = t.t_dict.copy()
        data_keys = list(data.keys())
        for each_data_key in data_keys:
            # check for testcases
            if isinstance(
                    data[each_data_key],
                    dict) and each_data_key not in [
                        'use_template',
                        'use_lib']:

                # Find device specific or not i.e. device_<device_name>
                devices = verify_utils.get_devices(each_data_key)
                is_protocol_centric = False

                # if device centric approach is not there, Dynamically
                # determine the its a device list or not
                if devices is False:
                    data_keys_list = verify_utils.expand_alpha_numeric_string(
                        each_data_key)
                    is_device_list_present = True

                    # Check each device is present in resources or not
                    for each_device in data_keys_list:
                        if re.search(r'dh\[\d+\]', each_device) is not None:
                            continue
                        #if each_device not in list(self.t_handle.keys()):
                        #    is_device_list_present = False

                    if is_device_list_present is True:
                        devices = each_data_key
                    else:

                        devices = verify_utils.get_key_value(
                            data=data,
                            key=each_data_key +
                            '/devices',
                            message="no device found for execution for " +
                            each_data_key,
                            if_false=False)
                        if devices is False:
                            return {'result': False}

                        is_protocol_centric = True
                # if protocol centric
                if is_protocol_centric is True:

                    # Check for template[''] or look for source_template
                    var = re.findall(
                        r'template\[\'(.*?)\'\]', each_data_key, re.I)
                    all_keys_in_each_data = data[each_data_key].keys()
                    if 'template' in all_keys_in_each_data or len(var) > 0:
                        if len(var) > 0:
                            tmpl_name = var[0]
                        else:
                            tmpl_name = data[each_data_key]['template']

                        # Find the template data from the template decleared
                        tmpl_data = self._search_template(tmpl_name)
                        if tmpl_data is False:
                            t.log(
                                level='debug',
                                message=tmpl_name +
                                " Not found in templates, Proceeding with next one")
                            continue

                        # Build the template from main data and template data
                        formed_tmpl_data = self._merge_template_data(
                            tmpl_data, data[each_data_key], tmpl_name)

                        # replace the value in the main data
                        verify_utils._replace_value(
                            data, formed_tmpl_data, each_data_key)
                    device_specific_data = copy.deepcopy(data[each_data_key])
                    each_device_specific_data.extend(self._form_device_specific_testcase(
                        {each_data_key: device_specific_data}, devices))
                else:
                    # For each device need to check for template is there or
                    # not
                    testcase_list = list(data[each_data_key].keys())
                    for each_testcase in testcase_list:
                        var = re.findall(
                            r'template\[\'(.*?)\'\]', each_testcase, re.I)
                        all_keys_in_each_data = list(
                            data[each_data_key][each_testcase].keys())

                        # Source template is present in testcases or not
                        if 'template' in all_keys_in_each_data or len(var) > 0:
                            if len(var) > 0:
                                tmpl_name = var[0]
                            else:
                                tmpl_name = data[each_data_key][
                                    each_testcase]['template']

                            # Find the template data and build the data from
                            # the main data and template data
                            tmpl_data = self._search_template(tmpl_name)
                            if tmpl_data is False and re.match(r'^j_check_.*', tmpl_name) is not None:
                                t.log(level='debug',
                                      message="Proceeding with Generic Template Search for " + tmpl_name)
                                tmpl_data = self._check_generic_template(
                                    tmpl_name)
                            if tmpl_data is False:
                                t.log(level='debug',
                                      message="Proceeding with next one")
                                continue
                            formed_tmpl_data = self._merge_template_data(
                                tmpl_data, data[each_data_key][each_testcase], tmpl_name)
                            verify_utils._replace_value(
                                data[each_data_key],
                                formed_tmpl_data,
                                each_testcase)  # replace for the normal flow
                    device_specific_data = copy.deepcopy(data[each_data_key])
                    each_device_specific_data.extend(
                        self._form_device_specific_testcase(
                            device_specific_data, devices))

        return {
            'data': each_device_specific_data,
            'result': True,
            'args': global_args}

    def _expand_modifiers(self, data):
        """
        method process the modifiers and return the list of modifier and
        """
        cmd = verify_utils.get_key_value(
            data=data,
            key='cmd',
            message="unable to find the command, please check the yaml file.",
            if_false=False)
        if cmd is False:
            return False

        path = None
        value = list()
        if 'xpath' in list(data.keys()):
            path = data['xpath']

        if re.search(r'<<.+>>', cmd):
            value = config_utils.expand_to_list(base=cmd)
        else:
            value.append(cmd)

        final_data = {'command': cmd, 'xpath': path,
                      'cmd_list': value}
        return final_data

    def _get_iterator_height(self, tc_data):
        '''
        Returns the height of tree rooted at tc_data.
        '''
        height = 0
        if isinstance(tc_data, dict):
            # If nested dictionary then recursively call function with
            # Nested dictionary.
            height += 1
            tc_data = tc_data[list(tc_data.keys())[0]]
            height = height + self._get_iterator_height(tc_data)
        else:
            # Reached at leaf.
            height += 1
        return height

    def _extract_value_from_path(self, data, each_item, values):
        # Take the original data.
        path_to_subtc = copy.deepcopy(data)
        # Convert given path to list.
        path = [x.strip() for x in each_item.split(':')]

        # Iterating over path to get the final hierarchy value.
        for sub_path in path:
            # If key is args.
            if isinstance(path_to_subtc, list):
                # Then iterate over entire args to find a key.
                for each_item_index in range(len(path_to_subtc)):
                    try:
                        path_to_subtc = path_to_subtc[each_item_index][sub_path.lower(
                        )]
                        continue
                    except BaseException:
                        continue
            else:
                path_to_subtc = path_to_subtc[verify_utils.convert_str_to_num_or_bool(
                    sub_path)]
                if isinstance(path_to_subtc, str):
                    path_to_subtc = path_to_subtc.lower()
        self._expand_and_append(values, path_to_subtc, each_item, data)

    def _expand_and_append(self, values, path_to_subtc, each_item, data):
        # Substituting variable.
        dummy_dict = {'dummy_key': path_to_subtc}
        self._substitute_variables(dummy_dict, data.get('args', []))

        # Expand it if it contains expansion modifier.
        expand_each_item = self._expand_ce_modifier(dummy_dict['dummy_key'])
        # Append the expnaded value.
        values.append(expand_each_item)

    def _generate_dataset(
            self,
            iterator,
            height,
            mapping_vars_values,
            mapping_vars_paths,
            data,
            expanded_tc_datas):
        '''
        It generates the list of test case data from the iterator mapping given by the user.
        '''
        # Value collection.
        values = []

        if height > 1:

            # Take the root element.
            loop_key = list(iterator.keys())[0].lower()

            if loop_key.startswith('loop('):

                # Get the looping variables.
                loop_vars = re.sub(r'^\s*loop', '', loop_key)
                loop_vars = loop_vars.strip('() ')

                # Variable collections.
                loop_vars_list = [x.strip() for x in loop_vars.split(',')]

                # Path collection
                path_tup = ()

                # Iterate over each variable
                for each_item in loop_vars_list:
                    # If nested path is given.
                    if ':' in each_item:
                        self._extract_value_from_path(data, each_item, values)
                    else:
                        self._expand_and_append(
                            values, data[each_item], each_item, data)
                    # Append current variables's path.
                    path_tup = path_tup + (each_item,)
                mapping_vars_paths.append(path_tup)
                try:
                    first_expansion_len = len(values[0])
                except KeyError:
                    first_expansion_len = 0
                if not all(len(x) == first_expansion_len for x in values):
                    t.log(
                        level='warn',
                        message='lengh mismatch of loop variables ' +
                        loop_key +
                        "\nstill will continue" +
                        "will iterate til shorter lenght of variable.")
                for i in zip(*values):
                    # Take i'th value from each list and keep it.
                    mapping_vars_values.append(i)
                    self._generate_dataset(iterator[list(iterator.keys())[0]], height - 1,
                                           mapping_vars_values, mapping_vars_paths, data,
                                           expanded_tc_datas)
                    # Remove i'th value from storage.
                    mapping_vars_values.pop()
                mapping_vars_paths.pop()
        else:
            # Take the leaf element.
            try:
                loop_key = iterator.values()[0].lower()
            except BaseException:
                # This is for handling of one element tree.
                loop_key = iterator.lower()
            if loop_key.startswith('loop('):

                # Get the looping variables.
                loop_vars = re.sub(r'^\s*loop', '', loop_key)
                loop_vars = loop_vars.strip('() ')
                # Variable collections.
                loop_vars_list = [x.strip() for x in loop_vars.split(',')]

                # Path collection.
                path_tup = ()

                # Iterate over each looping variable.
                for each_item in loop_vars_list:
                    if ':' in each_item:
                        self._extract_value_from_path(data, each_item, values)
                    else:
                        loop_variable_data = data.get(each_item, None)
                        if loop_variable_data:
                            self._expand_and_append(
                                values, data[each_item], each_item, data)
                        else:
                            t.log(level="error", message="key "+each_item +
                                  " is not found in the testcase data.")
                    # Append current variables's path.
                    path_tup = path_tup + (each_item,)

                mapping_vars_paths.append(path_tup)
                for i in zip(*values):
                    mapping_vars_values.append(i)
                    # Dictionary of test case.
                    testcase_dict = {}
                    # Take all value and path from root that we initially
                    # appended.
                    for index in range(len(mapping_vars_values)):
                        one_to_one_values = mapping_vars_values[index]
                        one_to_one_paths = mapping_vars_paths[index]
                        # iterate over onetoone mapping.
                        for nested_index in range(len(one_to_one_values)):
                            # Take the path.
                            input_str = one_to_one_paths[nested_index]
                            # Testcase creation start.
                            # If nested path is given.
                            if ":" in input_str:

                                # Constructing dictionary from leaf to root.
                                # So, Extractiong value.
                                final_colon = input_str.rfind(":")

                                # Removing value from string.
                                modified_str = input_str[:final_colon]

                                # Temp dict for bottom up construction.
                                temp_dict = {}

                                # Assigining value first.
                                temp_dict[input_str[final_colon + 1:]] = one_to_one_values[nested_index]

                                # input_str = one_to_one_paths[nested_index]

                                # Taking entire path to value.
                                splitted_str = modified_str.split(":")

                                # Flag for whether to append to test case
                                # dictionary or not.
                                is_append = False

                                # Iterating from right to left because our
                                # Approach is bottom up.
                                for each_item in splitted_str[::-1]:
                                    # If args found that put it in the list whatever
                                    # Is contructed till now.
                                    if each_item.lower() == "args":
                                        try:
                                            is_append = True
                                            testcase_dict['args'].append(
                                                temp_dict)
                                        except BaseException:
                                            testcase_dict['args'] = []
                                            testcase_dict['args'].append(
                                                temp_dict)
                                        continue
                                    # Putting into dictionary.
                                    temp_dict = {each_item: temp_dict}
                                if not is_append:
                                    # If there is no args then putting temp_dict into
                                    # The test_case dictionary.
                                    if list(temp_dict.keys())[0] not in list(
                                            testcase_dict.keys()):
                                        testcase_dict[list(temp_dict.keys())[
                                            0]] = temp_dict[list(temp_dict.keys())[0]]
                                    else:
                                        testcase_dict = verify_utils.merge_dicts(
                                            testcase_dict, temp_dict)
                                continue

                            testcase_dict[one_to_one_paths[nested_index]      \
                                          ] = one_to_one_values[nested_index]
                    mapping_vars_values.pop()

                    # Merging args start.
                    try:
                        new_args = testcase_dict['args']
                        old_args = data['args']
                        for old_item in range(len(old_args)):
                            found = False
                            for new_item in range(len(new_args)):
                                    # To identify which elements won't
                                    # override.
                                if list(
                                        new_args[new_item].keys())[0] == list(
                                            old_args[old_item].keys())[0]:
                                    found = True
                                    continue
                            if not found:
                                # If New args doesn't contain arg element
                                # include it.
                                testcase_dict['args'].append(
                                    old_args[old_item])

                    except BaseException:
                        try:
                            # If new data don't contains an args assign old
                            # args.
                            testcase_dict['args'] = data['args']
                        except BaseException:
                            # If new data and old data don't contains an args
                            # do nothing.
                            pass
                    # Merge args end
                    # Merging nested dictionaries.
                    testcase_dict = verify_utils.merge_dicts(
                        copy.deepcopy(data), testcase_dict)
                    del testcase_dict['iterator']
                    expanded_tc_datas.append(copy.deepcopy(testcase_dict))
                mapping_vars_paths.pop()

    def _expand_ce_modifier(self, input_str):
        """
        method expand
        """

        return_value = list()
        if isinstance(input_str, int):
            return_value.append(input_str)
            return return_value
        if not isinstance(input_str, str):
            return input_str
        if re.search(r'<<.+>>', input_str):
            return_value = config_utils.expand_to_list(base=input_str)
        else:
            return_value.append(input_str)
        return return_value

    def _is_valid_operator(self, operator):
        """
           Checks if the operator and the constraint is valid.

           Parameters:
               operator - input operator
           Return:
               Boolean, true if valid and false otherwise.
        """
        operators_list = ['is-equal', 'not-equal', 'regexp', 'non-regexp', \
                      'is-gt-or-equal', 'is-lt-or-equal', 'in-range', \
                      'is-gt', 'is-lt', 'not-range', 'contains', \
                      'is-in', 'not-in', 'exists', 'not-exists', \
                      'is-there', 'count-is-equal', 'count-is-gt', \
                      'count-is-lt', 'count-is-lt-or-equal', \
                      'count-is-gt-or-equal', 'not-contains', 'switch-value',\
                      'is-odd', 'is-even', 'is-number', 'is-string',\
                      'is-subset', 'is-superset', 'is-disjoint', 'is-none', 'match-substring', 'not-match-substring']

        operator_constraints_list = ['unordered', 'ignorecase', 'loose', 'strict', 'stripspace', 'acceptnone']
        operator.encode('utf-8').strip()
        operator = "".join(list(filter(lambda char: char in string.printable, operator)))
        if re.match(r'var\[.*\]', operator):
            return True
        if '[' in operator:
            operator_constraint = operator[operator.find("[")+1:operator.find("]")].lower()
            if "," in operator_constraint:
                for each_operator_constraint in operator_constraint.split(','):
                    if re.match(r'.*\(.*\)', operator_constraint) is None:
                        if each_operator_constraint not in operator_constraints_list:
                            t.log(level="error", message="Operator constraint "+each_operator_constraint+\
                                   " in the operator "+operator+" is not valid.")
                            return False
            else:
                if re.match(r'.*\(.*\)', operator_constraint) is None:
                    if operator_constraint not in operator_constraints_list:
                        t.log(level="error", message="Operator constraint "+operator_constraint+" in the operator "+operator+" is not valid.")
                        return False
            operator = operator[0:operator.find("[")]

        if operator.lower() not in operators_list:
            t.log(level="error", message="Operator "+str(operator)+" is not valid.")
            return False
        return True

    def _evaluate(
            self,
            expect_value=None,
            obtained_value=None,
            opr='is-equal',
            atr_constraint=None,
            is_iterate=False):
        """
        End operation based on the operator provided and return true or false
        """
        opr = opr.lower()
        opr = opr.strip()
        if not self._is_valid_operator(opr):
            return False
        if expect_value is None and opr not in ["not-exists", "exists", 'is-number', 'is-string',
                                                'is-odd', 'is-even', 'is-none']:
            t.log(
                level='debug',
                message="EXPECTED VALUE iS NONE .!!, CHECK THE VALUE")
            return False

        if obtained_value is None and (opr in ["is-none"] or 'acceptnone' in opr.lower()):
            return True

        if obtained_value is None or (isinstance(obtained_value, list)
                                      and len(obtained_value) == 0) or (  \
                isinstance(obtained_value, list) and obtained_value[0] == '_NONE'):
            t.log(
                level='debug',
                message="OBTAINED VALUE is NONE .!!, CHECK THE VALUE")
            if "count" not in opr and opr != "not-exists" and opr != "exists":
                if 'acceptnone' in opr.lower():
                    return True
                else:
                    return False
            elif "count" in opr or opr == "not-exists" or opr == "exists":
                t.log(
                    level='debug',
                    message="Setting obtained_value as empty list...")
                obtained_value = []

        temp_value = verify_utils._convert_lxml_to_data(obtained_value)

        obtained_value = temp_value
        if 'count' not in opr and len(temp_value) == 1:
            obtained_value = temp_value[0]

        try:
            if isinstance(expect_value, str):
                if isinstance(
                        eval(expect_value),
                        list) or isinstance(
                            eval(expect_value),
                            dict):
                    expect_value = eval(expect_value)
        except BaseException:
            expect_value = expect_value

        try:
            if isinstance(obtained_value, str):
                if isinstance(
                        eval(obtained_value),
                        list) or isinstance(
                            eval(obtained_value),
                            dict):
                    obtained_value = eval(obtained_value)
        except BaseException:
            obtained_value = obtained_value

        # constraints CODE like is-equal['UNORDERED']
        if atr_constraint is not None:
            obtained_value = verify_utils._process_obtained_value_constraints(
                obtained_value, atr_constraint)

        obtained_value, expect_value, opr, opr_constraint = verify_utils.process_constraints(
            obtained_value, expect_value, opr)

        if opr in ["is-lt", "is-gt"] and atr_constraint in ["delta"]:
            result = False
            if not isinstance(obtained_value, int):
                if len(obtained_value) < 2:
                    message = "More than one record expected for the constraint: " +\
                        atr_constraint
                    if is_iterate:
                        self.error_message = message
                    else:
                        t.log(level="error", message=message)
                else:
                    for index in range(0, len(obtained_value)):
                        if index == len(obtained_value) - 1:
                            break
                        else:
                            delta = int(
                                obtained_value[index + 1]) - int(obtained_value[index])
                            if(delta < expect_value and opr == "is-lt") or (
                                    delta > expect_value and opr == "is-gt"):
                                result = True
                            else:
                                return False
            else:
                message = "Operator <is-lt/is-gt>[delta] expects a list of records but \
                         only one record found."
                if is_iterate:
                    self.error_message = message
                else:
                    t.log(level="error", message=message)
            return result

        if opr in ["switch-value"]:
            if opr_constraint is None:
                opr_constraint = "strict"
            else:
                opr_constraint = opr_constraint.lower()
            result = False
            index1 = 0
            index2 = 0
            if len(obtained_value) < len(expect_value):
                return False
            if obtained_value[0] != expect_value[0]:
                return False
            if expect_value == obtained_value:
                return True
            while index2 < (
                    len(obtained_value)) and index1 < (
                        len(expect_value)):
                temp_expect_value = expect_value[index1]
                temp_obtained_value = obtained_value[index2]
                if temp_expect_value == temp_obtained_value:
                    index2 = index2 + 1
                    result = True
                elif opr_constraint == "strict":
                    index1 = index1 + 1
                    result = False
                elif opr_constraint == "loose":
                    if (index2 + 1 < len(obtained_value)) and (
                            index1 + 1 < len(expect_value)):
                        if (obtained_value[index2 + 1]
                                == expect_value[index1 + 1]):
                            index1 = index1 + 1
                    if (index2 + 1 >= len(obtained_value)) and (
                            index1 + 1 < len(expect_value)) and (
                                obtained_value[index2] == expect_value[index1 + 1]):
                        index1 = index1 + 2
                        result = True
                    index2 = index2 + 1
                else:
                    message = "Operator switch-value works with the constraint 'strict'(default)\
                               or 'loose', but constraint provided : " + opr_constraint
                    if is_iterate:
                        self.error_message = message
                    else:
                        t.log(level="error", message=message)
                    break
            if (index1 + 1) < len(expect_value):
                result = False
            if index1 >= len(expect_value) and index2 < (len(obtained_value)):
                result = False
            return result

        if opr in [
                "not-equal",
                "is-equal",
                "is-gt",
                "is-gt-or-equal",
                "is-lt",
                "is-lt-or-equal"]:
            if isinstance(obtained_value, list):
                if isinstance(expect_value, list):
                    if len(expect_value) == 1 or len(
                            expect_value) == len(obtained_value):
                        if len(expect_value) == 1:
                            for each_value in obtained_value:
                                ob_val = verify_utils.convert_str_to_num_or_bool(
                                    each_value)
                                ex_val = verify_utils.convert_str_to_num_or_bool(
                                    expect_value[0])
                                if (opr == "not-equal" and ob_val == ex_val) or (
                                        opr == "is-equal" and ob_val != ex_val) or (
                                            opr == "is-gt" and ob_val <= ex_val) or (
                                                opr == "is-gt-or-equal" and ob_val < ex_val) or (
                                                    opr == "is-lt" and ob_val >= ex_val) or (
                                                        opr == "is-lt-or-equal" and ob_val > ex_val):
                                    return False
                            return True
                        else:
                            for each_value in range(0, len(obtained_value)):
                                ob_val = verify_utils.convert_str_to_num_or_bool(
                                    obtained_value[each_value])
                                ex_val = verify_utils.convert_str_to_num_or_bool(
                                    expect_value[each_value])
                                if (opr == "not-equal" and ob_val == ex_val) or (
                                        opr == "is-equal" and ob_val != ex_val) or (
                                            opr == "is-gt" and ob_val <= ex_val) or (
                                                opr == "is-gt-or-equal" and ob_val < ex_val) or (
                                                    opr == "is-lt" and ob_val >= ex_val) or (
                                                        opr == "is-lt-or-equal" and ob_val > ex_val):
                                    return False
                            return True
                    else:
                        t.log(level='debug',
                              message="Number of values are not equal")
                        return False
                elif isinstance(expect_value, float) or isinstance(expect_value, int) or \
                        isinstance(expect_value, str):
                    ex_val = verify_utils.convert_str_to_num_or_bool(
                        expect_value)
                    for each_value in obtained_value:
                        ob_val = verify_utils.convert_str_to_num_or_bool(
                            each_value)
                        if (opr == "not-equal" and ob_val == ex_val) or (
                                opr == "is-equal" and ob_val != ex_val) or (
                                    opr == "is-gt" and ob_val <= ex_val) or (
                                        opr == "is-gt-or-equal" and ob_val < ex_val) or (
                                            opr == "is-lt" and ob_val >= ex_val) or (
                                                opr == "is-lt-or-equal" and ob_val > ex_val):
                            return False
                    return True
                else:
                    t.log(
                        level='info',
                        message="LENGTH OF OBTAIN VALUE AND EXCEPTED VALUE VARIES")
                    return False
            else:
                if isinstance(obtained_value, str):
                    obtained_value = obtained_value.strip()
                if isinstance(expect_value, list):
                    if len(expect_value) == 1:
                        ex_val = verify_utils.convert_str_to_num_or_bool(
                            expect_value[0])
                    else:
                        t.log(
                            level='info',
                            message="LENGTH OF OBTAIN VALUE AND EXCEPTED VALUE VARIES")
                        return False
                else:
                    ex_val = verify_utils.convert_str_to_num_or_bool(
                        expect_value)
                ob_val = verify_utils.convert_str_to_num_or_bool(
                    obtained_value)
                if (opr == "not-equal" and ob_val == ex_val) or (
                        opr == "is-equal" and ob_val != ex_val) or (
                            opr == "is-gt" and ob_val <= ex_val) or (
                                opr == "is-gt-or-equal" and ob_val < ex_val) or (
                                    opr == "is-lt" and ob_val >= ex_val) or (
                                        opr == "is-lt-or-equal" and ob_val > ex_val):
                    return False
                return True
        elif opr in ['count-is-equal', 'count-is-gt', 'count-is-gt-or-equal', 'count-is-lt',
                     'count-is-lt-or-equal']:
            if (int(expect_value) == len(obtained_value) and opr == 'count-is-equal') or \
                    (int(expect_value) < len(obtained_value) and opr == 'count-is-gt') or \
                    (int(expect_value) <= len(obtained_value) and opr == 'count-is-gt-or-equal') or\
                    (int(expect_value) > len(obtained_value) and opr == 'count-is-lt') or \
                    (int(expect_value) >= len(obtained_value) and opr == 'count-is-lt-or-equal'):
                return True
            else:
                return False

        elif opr in ["regexp", "non-regexp"]:
            var = re.search(str(expect_value), str(obtained_value), re.I)
            if (var is None and opr == "regexp") or (
                    var is not None and opr == 'non-regexp'):
                return False
            else:
                return True

        elif opr in ['in-range', 'not-range']:
            iplist = []
            flag = False
            if isinstance(expect_value, list):
                for each_expect_value in expect_value:
                    if isinstance(each_expect_value, str):
                        each_expect_value = each_expect_value.lower()
                    range_value = each_expect_value.split('to')
                    if len(range_value) == 1:
                        range_value = each_expect_value.split(':')
                    if len(range_value) == 1:
                        range_value = each_expect_value.split('-')
                    if len(range_value) != 2:
                        t.log(level="info", 
                              message="Given Input format is not correct.\nPlease check format of given value with respect to in-range operator")
                        return False
                    range_value[0] = str(range_value[0]).strip()
                    range_value[1] = str(range_value[1]).strip()
                    if config_utils.is_ip(range_value[0]):
                        iplist.extend(config_utils.make_list(first=range_value[0], step=1, last=range_value[1]))

                if isinstance(obtained_value, list):
                    if config_utils.is_ip(obtained_value[0]):
                        return_result = []
                        for each_obtained_value in obtained_value:
                            if (each_obtained_value in iplist and opr == 'in-range') \
                                    or (each_obtained_value not in iplist and opr == 'not-range'):
                                    return_result.append(True)
                            else:
                                return_result.append(False)
                            return not(False in return_result)
                    else:
                        return_result = []
                        for each_obtained_value in obtained_value:
                            for each_expect_value in expect_value:
                                if isinstance(each_expect_value, str):
                                    each_expect_value = each_expect_value.lower()
                                range_value = each_expect_value.split('to')
                                if len(range_value) == 1:
                                    range_value = each_expect_value.split(':')
                                if len(range_value) == 1:
                                    range_value = each_expect_value.split('-')
                                if len(range_value) != 2:
                                    t.log(level="info", 
                                          message="Given Input format is not correct.\nPlease check format of given value with respect to in-range operator")
                                    return False
                                srt_val = verify_utils.convert_str_to_num_or_bool(range_value[0])
                                end_val = verify_utils.convert_str_to_num_or_bool(range_value[1])
                                if (srt_val <= each_obtained_value <= end_val and opr == 'in-range') or \
                                        ((srt_val > each_obtained_value or each_obtained_value > end_val) and
                                         opr == 'not-range'):
                                    return_result.append(True)
                                    flag = True
                            if not flag:
                                return_result.append(False)
                        return not(False in return_result)

                else:
                    if config_utils.is_ip(obtained_value):
                        if(obtained_value in iplist and opr == 'in-range') or (obtained_value not in iplist and opr == 'not-range'):
                            return True
                        else:
                            return False
                    else:
                        return_result = []
                        for each_expect_value in expect_value:
                            if isinstance(each_expect_value, str):
                                each_expect_value = each_expect_value.lower()
                            range_value = each_expect_value.split('to')
                            if len(range_value) == 1:
                                range_value = each_expect_value.split(':')
                            if len(range_value) == 1:
                                range_value = each_expect_value.split('-')
                            if len(range_value) != 2:
                                t.log(level="info",
                                      message="Given Input format is not correct.\nPlease check format of given value with respect to in-range operator")
                                return False
                            srt_val = verify_utils.convert_str_to_num_or_bool(range_value[0])
                            end_val = verify_utils.convert_str_to_num_or_bool(range_value[1])
                            if(srt_val <= obtained_value <= end_val and opr == 'in-range') or \
                                        ((srt_val > obtained_value or obtained_value > end_val) and
                                         opr == 'not-range'):
                                return_result.append(True)
                                flag = True
                        if not flag:
                            return_result.append(False)

                return flag


            elif isinstance(expect_value, str):
                expect_value = expect_value.lower()
                range_value = expect_value.split('to')
                if len(range_value) == 1:
                    range_value = expect_value.split(':')
                if len(range_value) == 1:
                    range_value = expect_value.split('-')
                if len(range_value) != 2:
                    t.log(level="info", 
                          message="Given Input format is not correct.\nPlease check format of given value with respect to in-range operator")
                    return False
                range_value[0] = str(range_value[0]).strip()
                range_value[1] = str(range_value[1]).strip()
                if config_utils.is_ip(range_value[0]):
                    iplist = array()
                    iplist.extend(config_utils.make_list(first=range_value[0], step=1, last=range_value[1]))
                    if isinstance(obtained_value, list):
                        return_result = []
                        for each_obtained_value in obtained_value:
                            if (IPAddress(each_obtained_value) in IPNetwork(iplist) and opr == 'in-range') \
                                    or (IPAddress(each_obtained_value) not in IPNetwork(iplist) and opr == 'not-range'):
                                    return_result.append(True)
                            else:     
                                return_result.append(False)
                            return not(False in return_result)
                    else:      
                        if (IPAddress(obtained_value) in IPNetwork(iplist) and opr == 'in-range') \
                                    or (IPAddress(obtained_value) not in IPNetwork(iplist) and opr == 'not-range'):
                            return True
                        else:
                            return False

                else:
                    srt_val = verify_utils.convert_str_to_num_or_bool(range_value[0])
                    end_val = verify_utils.convert_str_to_num_or_bool(range_value[1])
                    t.log(level="info", message=srt_val)
                    t.log(level="info", message=end_val)
                    if isinstance(obtained_value, list):
                        return_result = []
                        for each_obtained_value in obtained_value:
                            if (srt_val <= each_obtained_value <= end_val and opr == 'in-range') or \
                                    ((srt_val > each_obtained_value or each_obtained_value > end_val) and
                                     opr == 'not-range'):
                                return_result.append(True)
                            else:
                                return_result.append(False)
                        return not(False in return_result)
                    else:         
                        if (srt_val <= obtained_value <= end_val and opr == 'in-range') or \
                                ((srt_val > obtained_value or obtained_value > end_val) and
                                 opr == 'not-range'):
                            return True
                        else:
                            return False

        elif opr in ["contains", "not-contains"]:
            if expect_value in obtained_value and opr == "contains":
                return True
            elif expect_value not in obtained_value and opr == "not-contains":
                return True
            else:
                return False

        elif opr in ["match-substring", "not-match-substring"]:
            if(isinstance(obtained_value,str)):
                if expect_value in obtained_value and opr == "match-substring":
                    return True
                elif expect_value not in obtained_value and opr == "not-match-substring":
                    return True
                else:
                    return False
            elif(isinstance(obtained_value,list)):
                for each in obtained_value:
                    if expect_value in each and opr == "match-substring":
                        return True
                    elif expect_value in each and opr == "not-match-substring":
                        return False
                res=True if opr == "not-match-substring" else False
                return res

        elif opr in ["is-subset", "is-superset", "is-disjoint"]:
            if isinstance(expect_value, Iterable) and isinstance(obtained_value, Iterable):
                if (opr == "is-subset" and set(obtained_value).issubset(expect_value)) or\
                   (opr == "is-superset" and set(obtained_value).issuperset(expect_value)) or\
                   (opr == "is-disjoint" and set(obtained_value).isdisjoint(expect_value)):
                    return True
                else:
                    return False
            else:
                return False

        elif opr in ['is-in', 'not-in']:
            if isinstance(expect_value, list):
                expect_value = verify_utils._convert_list_to_datatype(
                    expect_value)
            if isinstance(expect_value, str) and config_utils.is_ip(
                    expect_value) is False:
                if not '-' in expect_value:
                    obtained_value = str(obtained_value)
            if config_utils.is_ip(obtained_value):
                if isinstance(expect_value, str):
                    if '-' in expect_value:
                        expect_value = config_utils.expand_to_list(
                            "<<" + expect_value.replace('-', '..') + ">>")
                    else:
                        if(IPAddress(obtained_value) in IPNetwork(expect_value) and opr == 'is-in')\
                                or (IPAddress(obtained_value) not in IPNetwork(expect_value) and  \
                                    opr == 'not-in'):
                            return True
                        else:
                            return False
                elif isinstance(expect_value, list):
                    for each_expect_value in expect_value:
                        if opr == 'is-in':
                            return_result = True
                            if IPAddress(obtained_value) in IPNetwork(each_expect_value):
                                return return_result
                        elif opr == 'not-in':
                            return_result = False
                            if IPAddress(obtained_value) in IPNetwork(each_expect_value):
                                return return_result
                    return return_result

            if isinstance(
                    obtained_value,
                    list) and config_utils.is_ip(
                        obtained_value[0]):
                return_result = True
                if isinstance(expect_value, str):
                    if '-' in expect_value:
                        expect_value = config_utils.expand_to_list(
                            "<<" + expect_value.replace('-', '..') + ">>")
                        for each_obtained_value in obtained_value:
                            if (each_obtained_value in expect_value and opr == 'not-in') or\
                                    (each_obtained_value not in expect_value and opr == 'is-in'):
                                return_result = False
                    else:
                        for each_obtained_value in obtained_value:
                            if (IPAddress(each_obtained_value) in IPNetwork(expect_value) and
                                    opr == 'not-in') or \
                                    (IPAddress(each_obtained_value) not in IPNetwork(expect_value) and opr == 'is-in'):
                                return_result = False
                    return  return_result
                elif isinstance(expect_value, list):
                    return_result = []
                    for each_obtained_value in obtained_value:
                        found = False

                        for each_expect_value in expect_value:
                            if (IPAddress(each_obtained_value) in IPNetwork(each_expect_value) and opr == 'is-in') or \
                                    (IPAddress(each_obtained_value) not in IPNetwork(each_expect_value) and opr == 'not-in'):
                                    found = True
                                    break     
                        if found:    
                            return_result.append('True')
                        else:
                            return_result.append('False')
                    return  not('False' in return_result)

            if (obtained_value in expect_value and opr == 'is-in') or\
                    (obtained_value not in expect_value and opr == 'not-in'):
                return True
            else:
                t.log(
                    level='debug',
                    message="OBTAINED_VALUE AND EXPECTED_VALUE")
                t.log(level='debug', message=obtained_value)
                t.log(level='debug', message=expect_value)
                return False

        elif opr in ['not-exists', 'exists']:
            if (obtained_value == [] and opr ==
                    'not-exists') or (obtained_value != [] and opr == 'exists'):
                return True
            else:
                return False
        elif opr in ['is-number', 'is-string']:
            if (opr == 'is-number' and isinstance(obtained_value, (int, float))) or\
               (opr == 'is-string' and isinstance(obtained_value, str)):
                return True
            else:
                return False
        elif opr in ['is-odd', 'is-even']:
            if isinstance(obtained_value, int):
                if (opr == 'is-odd' and (obtained_value % 2 != 0)) or\
                   (opr == 'is-even' and (obtained_value % 2 == 0)):
                    return True
                else:
                    return False
            elif isinstance(obtained_value, list):
                if len(obtained_value) == 0:
                    return False
                elif opr == 'is-odd' and all(isinstance(item, int)
                                             and (item % 2 != 0) for item in obtained_value) or\
                    opr == 'is-even' and all(isinstance(item, int)
                                             and (item % 2 == 0) for item in obtained_value):
                    return True
                else:
                    return False
            else:
                t.log(
                    level='INFO', message='Obtained value is neither an Integer nor list of Integers')
                return False
        else:
            t.log(
                level='debug',
                message="\t\tNO MATCHING OPERATOR FOUND ..!!!CHECK OPERATOR LIST")
            return False

    def _verify_parameters(
            self,
            xpath_result,
            element_data,
            element_data_keys,
            tag,
            is_ex_get=False,
            is_get=None,
            return_type=None,
            return_result=None,
            root_xpath=None,
            xpath_filter_dict=None,
            is_iterate=False):
        """
            Recursively process the testcases
        """
        if len(element_data_keys) == 0:
            tag_list = tag.split('/')
            next_data = xpath_result
            if isinstance(next_data, lxml.etree._Element):
                obtain_value = next_data.text
            else:
                obtain_value = next_data
            if is_get is not None and return_type is not None and return_type != 'bool' \
                    and is_ex_get is True:
                return_result.update(
                    {tag_list[-1]: verify_utils.convert_str_to_num_or_bool(obtain_value)})
            else:
                t.log(level='info', 
                      message="No value found to verify... Dumping the output.\n" + str(obtain_value) + "\n")

        xpath_hit = False
        if xpath_filter_dict or isinstance(root_xpath, list):
            #valid_root_xpath_list = verify_utils._get_valid_xpaths(xpath_result,root_xpath)
            if element_data.get('xpath', None) is not None:
                parameter_xpath = element_data['xpath']
                _parameter_xpath_elements = parameter_xpath.split('/')
                for each_parameter_xpath_element_index in range(0, len(_parameter_xpath_elements)):
                    if _parameter_xpath_elements[each_parameter_xpath_element_index] in xpath_filter_dict.keys():
                        _parameter_xpath_elements[each_parameter_xpath_element_index] = _parameter_xpath_elements[each_parameter_xpath_element_index] + '[' + \
                            str(xpath_filter_dict[_parameter_xpath_elements[each_parameter_xpath_element_index]]) + ']'
                parameter_xpath = '/'.join(_parameter_xpath_elements)
            else:
                parameter_xpath = tag
            for each_valid_root_xpath in root_xpath:
                t.log(level='debug', message="Trying...Root Path with Parameter( " +
                      each_valid_root_xpath + '/' + parameter_xpath+" )")
                xpath_result_after_params = verify_utils.get_xpath_result(
                    data=xpath_result, xpath=each_valid_root_xpath+'/'+parameter_xpath)
                t.log(level='debug', message="Xpath Result : " +
                      str(xpath_result_after_params))
                if xpath_result_after_params != ['_NONE'] and xpath_result_after_params != []:
                    t.log(level='debug', message="Xpath Hit Success  Xpath Result")
                    xpath_hit = True
                    break
            if xpath_hit is False:
                xpath_result_after_params = ['_NONE']
            t.log(level='debug', message="Xpath Result After Parameter Xpath  : " +
                  str(xpath_result_after_params))
        else:
            xpath_result_after_params = xpath_result

        for each_element_data_key in element_data_keys:

            if each_element_data_key in [
                    'operator',
                    'value',
                    'include_all',
                    'skip',
                    'iterate_until',
                    'iterate_for',
                    'xpath',
                    'passmsg',
                    'failmsg',
                    'xpath_filter']:
                tag_list = tag.split('/')
                next_data = xpath_result_after_params
                result = self._evaluate(
                    element_data.get(
                        'value', None), next_data, element_data.get(
                            'operator', 'is-equal'), is_iterate=is_iterate)
                obtain_value = verify_utils._convert_lxml_to_data(next_data)
                if len(obtain_value) == 1:
                    obtain_value = obtain_value[0]
                if is_get is not None and return_type is not None and return_type != 'bool' \
                        and is_ex_get:
                    return_result.update(
                        {tag_list[-1]: verify_utils.convert_str_to_num_or_bool(obtain_value)})
                else:
                    self._put_verify_log(testcase=tag_list[-1],
                                         expect=element_data.get('value',
                                                                 None),
                                         obtain=obtain_value,
                                         opr=element_data.get('operator',
                                                              'is-equal'),
                                         result=result,
                                         tc_data=element_data)

                if is_get is not None and return_type == 'bool' and is_ex_get:
                    return_result.update({tag_list[-1]: result})
                else:
                    if isinstance(return_result, bool) and result is False:
                        return_result = False
                return return_result
            else:
                if not isinstance(root_xpath, list):
                    tag = each_element_data_key
                    next_xpath_result = verify_utils.get_xpath_result(
                        xpath_result, tag)

                    return_result = self._verify_parameters(
                        next_xpath_result,
                        element_data[each_element_data_key],
                        list(
                            element_data[each_element_data_key].keys()),
                        each_element_data_key,
                        is_ex_get=is_ex_get,
                        is_get=is_get,
                        return_type=return_type,
                        return_result=return_result,
                        is_iterate=is_iterate)
                else:
                    return_result = self._verify_parameters(
                        xpath_result,
                        element_data[each_element_data_key],
                        list(
                            element_data[each_element_data_key].keys()),
                        tag+'/'+each_element_data_key,
                        is_ex_get=is_ex_get,
                        is_get=is_get,
                        return_type=return_type,
                        return_result=return_result,
                        root_xpath=root_xpath,
                        is_iterate=is_iterate)

        return return_result

    def get_t_var(
            self,
            tv=None,
            delimiter='__',
            return_path=None,
            fail_ok=True):
        """
        Dynamic method to retrieve value inside t in a flaaterned, concise format.

        DESCRIPTION:
            Taken from config engine
            Dynamic method to retrieve value inside t in a flaaterned, concise format
            (default delimiter of knobs in t is '__' double underscore)

            used internally in verify engine for now, will make it as a toby util.

            for example, a pic in t is:

              t[resources][device0][interfaces][link1][pic]

            The t_var expression:

              tv['device0__link1__pic']

            is equivalent to:

              tv['resources__device0__interfaces__link1__pic']

        ARGUMENTS:
            [tv=None,delimiter='__',return_path=None,fail_ok=True]
            :param STR tv:
                *MANDATORY* finds out if tvars is available in params. Default tv is None.
            :param STR delimiter:
                *OPTIONAL* Delimeter type.
            :param STR return_path:
                *OPTIONAL* retrived value storing PATH
            :param BOOLEAN fail_ok:
                *OPTIONAL* by Default fail ok is set to True.

        ROBOT USAGE:
            ${var} =   verifyEngine.Get T var      tv=${intf}

        :return t_var or path
        """
        if tv is None:
            raise Exception("Mandatory arg 'tv' is missing")
        if not self.t_handle:
            self.t_handle = t.t_dict['resources'].copy()
            self._make_ifd_tvar()

        key_list = tv.split(delimiter)
        listitem = re.match(r'.+\[(.*)\]', key_list[-1])
        index = None
        if listitem is not None:
            index = listitem.group(1)
            key_list[-1] = re.sub(r'\[.*\]\s*$', '', key_list[-1])
        t_var, path = verify_utils.find_dict_data(
            data=self.t_handle, key_list=key_list)
        if t_var is None:
            t.log(level='warn', message='cannot find {} in tvars'.format(tv))
        elif isinstance(t_var, list) and index is None:
            # assuming you are looking for the first element
            # you might not aware it is a list
            t_var = t_var[0]
        elif isinstance(t_var, list) and index is not None:
            try:
                t_var = eval('t_var[{}]'.format(index))
            except Exception as err:
                t.log(
                    level='error',
                    message='t var {} might be out of range: {}'. format(
                        tv,
                        str(t_var)))
                t.log(level='error', message=err)
                t_var = tv
        elif (index is not None) and (index not in ('0', '-1')):
            raise Exception('tvar {} can not be accessed as a list'.format(tv))

        if return_path is None:
            return t_var
        else:
            return t_var, path

    def _cleanup_xml_namespace(self, data):
        '''
           Removes all the namespaces from the input xml data.
        '''
        response = data
        xml_string = data
        xml_string = re.sub('.*?(\<rpc\-reply.*\<\/rpc\-reply\>).*', '\\1', xml_string, 0, re.S)
        if to_ele(xml_string) is not None:
            namespace_list = re.findall('xmlns:(.*)\=', xml_string)
            t.log(level='debug', message="Namespace List:")
            t.log(level='debug', message=namespace_list)
            xml_string = re.sub('\sxmlns[^"]+"[^"]+"', '', xml_string)
            for namespace in namespace_list:
                pattern1 = '(\\s+)(' + namespace + '\\:)(.*?\\=)'
                pattern2 = '([\<\/]+)(' + namespace + '\\:)(.*?((\\s+)|\>))'
                xml_string = re.sub(pattern1, '\\1\\3', xml_string)
                xml_string = re.sub(pattern2, '\\1\\3', xml_string)
            # xml_string = re.sub('(\s+)(junos\:)(.*?\=)','\\1\\3',xml_string)
            xml_object = to_ele(xml_string)
            for cli in xml_object.xpath("//cli"):
                cli.getparent().remove(cli)
            if len(xml_object) == 1:
                response = xml_object[0]
            elif len(xml_object) > 1:
                response = xml_object
        else:
            response = ''
            t.log(
                level='error',
                message="\nOutput is not in XML format..please check command response\n")
            return response
        if not self.suppress_log and (not self.suppress_overlimit_log):
            t.log(level="info", message="XML OUTPUT: START\n")
            t.log(level="info", message=tostring(response).decode())
            t.log(level="info", message="XML OUTPUT: END\n")

        elif self.suppress_overlimit_log:
            response_lines = len(response)
            if response_lines <= self.suppress_log_limit:
                t.log(level="info", message="XML OUTPUT: START\n")
                t.log(level="info", message=tostring(response).decode())
                t.log(level="info", message="XML OUTPUT: END\n")
            else:
                t.log(
                    level="debug", message="Command response exceeded the supress limit and hence suppressing it.")
        else:
            t.log(
                level="debug", message="Command response suppressed due to suppress_log flag.")
        return response

    def _store_last_cmd_response(self, response, form):
        if form == "text":
            self.last_text_execution_data["last_cmd_response"] = response
        else:
            self.last_xml_execution_data["last_cmd_response"] = response

    def _get_response(
            self,
            cmd,
            format,
            execute_on,
            device_handle,
            cmd_timeout=120,
            cmd_pattern=None):
        if self.is_VE_offline is True:
            if self.offline_data is None:
                t.log(
                    level='error',
                    message="\nThe Offline data is not found\n")
                return False
            else:
                if format.lower() == 'xml':
                    return self._cleanup_xml_namespace(self.offline_data)
                else:
                    return self.offline_data

        format = format.lower()
        last_cmd = None
        last_device_handle = None
        if format == "text":
            last_cmd = self.last_text_execution_data['last_cmd']
            last_device_handle = self.last_text_execution_data['last_device_handle']
        else:
            last_cmd = self.last_xml_execution_data['last_cmd']
            last_device_handle = self.last_xml_execution_data['last_device_handle']

        if self._showdump is not None:
            t.log(
                level="info",
                message="Using showdump data as response from DUT.")
            if format.lower() == 'xml':
                return self._cleanup_xml_namespace(self._showdump)
            else:
                t.log(level="info", message="TEXT OUTPUT: START\n")
                t.log(level="info", message=self._showdump)
                t.log(level="info", message="TEXT OUTPUT: END\n")
                return self._showdump

        if self.user_optimized and cmd == last_cmd and device_handle == last_device_handle:
            t.log(level="info", message="Optimized cmd execution...")
            if format == "text":
                return self.last_text_execution_data['last_cmd_response']
            else:
                return self.last_xml_execution_data['last_cmd_response']

        if cmd == last_cmd and device_handle == last_device_handle and \
                self.iterate_until_present is False and self.response_optimize_iterator \
                and self.user_optimized and self.iterator_id == self.get_response_id:
            t.log(level="info", message="Optimized cmd execution...")
            if format == "text":
                return self.last_text_execution_data['last_cmd_response']
            else:
                return self.last_xml_execution_data['last_cmd_response']

        if format == "text":
            self.last_text_execution_data['last_cmd'] = cmd
            self.last_text_execution_data['last_device_handle'] = device_handle
        else:
            self.last_xml_execution_data['last_cmd'] = cmd
            self.last_xml_execution_data['last_device_handle'] = device_handle

        self.get_response_id = self.iterator_id
        connect_dict = {}
        connect_dict.update({'cmd': cmd})
        connect_dict.update({'format': format})
        if execute_on is not None:
            connect_dict.update(execute_on)
        connect_dict.update({'device_handle': device_handle})

        dev_handle = connect_dict['device_handle']

        keys = [x.lower() for x in list(connect_dict.keys())]

        response = ''

        if isinstance(dev_handle, JuniperSystem):

            if "mode" in keys:

                cmd_mode = str(connect_dict["mode"]).lower()
            else:
                cmd_mode = 'cli'

            if cmd_mode == 'cty' or cmd_mode == 'vty':
                if "destination" not in keys:
                    raise Exception(
                        "for cty and vty destintion key is required")

            if cmd_mode == 'cty':
                if "node" in keys and "controller" in keys:
                    if cmd_pattern is not None:
                        response = dev_handle.nodes[
                            connect_dict["node"]].controllers[connect_dict["controller"]].cty(
                                command=connect_dict['cmd'], destination=connect_dict['destination'],
                                timeout=cmd_timeout, pattern=cmd_pattern).response()
                        self._store_last_cmd_response(response, format)
                        return response
                    response = dev_handle.nodes[connect_dict[
                        "node"]].controllers[connect_dict["controller"]].cty(
                            command=connect_dict['cmd'], destination=connect_dict['destination'],
                            timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response
                elif "node" in keys:
                    if cmd_pattern is not None:
                        response = dev_handle.nodes[
                            connect_dict["node"]].current_controller.cty(
                                command=connect_dict['cmd'], destination=connect_dict['destination'],
                                timeout=cmd_timeout, pattern=cmd_pattern).response()
                        self._store_last_cmd_response(response, format)
                        return response
                    response = dev_handle.nodes[connect_dict[
                        "node"]].current_controller.cty(command=connect_dict['cmd'],
                                                        destination=connect_dict['destination'],
                                                        timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response
                elif "controller" in keys:
                    if cmd_pattern is not None:
                        response = \
                            dev_handle.current_node.controllers[connect_dict["controller"]].cty(
                                command=connect_dict['cmd'], destination=connect_dict[
                                    'destination'], timeout=cmd_timeout,
                                pattern=cmd_pattern).response()
                        self._store_last_cmd_response(response, format)
                        return response
                    response = \
                        dev_handle.current_node.controllers[connect_dict["controller"]].cty(
                            command=connect_dict['cmd'], destination=connect_dict['destination'],
                            timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response
                if cmd_pattern is not None:
                    response = dev_handle.cty(
                        command=connect_dict['cmd'],
                        destination=connect_dict['destination'],
                        timeout=cmd_timeout,
                        pattern=cmd_pattern).response()
                    self._store_last_cmd_response(response, format)
                    return response
                response = dev_handle.cty(
                    command=connect_dict['cmd'],
                    destination=connect_dict['destination'],
                    timeout=cmd_timeout).response()
                self._store_last_cmd_response(response, format)
                return response

            elif cmd_mode == 'vty':
                cmd_format = "xml"
                if "node" in keys and "controller" in keys:
                    if "disable_syslog" in keys and str(connect_dict['disable_syslog']).lower() == 'true':
                        response = dev_handle.nodes[connect_dict[
                            "node"]].controllers[connect_dict["controller"]].vty(
                                command="set syslog level 0", destination=connect_dict['destination'],
                                timeout=cmd_timeout).response()
                    if cmd_pattern is not None:
                        response = dev_handle.nodes[
                            connect_dict["node"]].controllers[connect_dict["controller"]].vty(
                                command=connect_dict['cmd'], destination=connect_dict['destination'],
                                timeout=cmd_timeout, pattern=cmd_pattern).response()
                        self._store_last_cmd_response(response, format)
                        return response
                    response = dev_handle.nodes[connect_dict[
                        "node"]].controllers[connect_dict["controller"]].vty(
                            command=connect_dict['cmd'], destination=connect_dict['destination'],
                            timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response
                elif "node" in keys:
                    if "disable_syslog" in keys and str(connect_dict['disable_syslog']).lower() == 'true':
                        response = \
                            dev_handle.nodes[connect_dict["node"]].current_controller.vty(
                                command="set syslog level 0", destination=connect_dict[
                                    'destination'], timeout=cmd_timeout).response()
                    if cmd_pattern is not None:
                        response = dev_handle.nodes[
                            connect_dict["node"]].current_controller.vty(
                                command=connect_dict['cmd'], destination=connect_dict['destination'],
                                timeout=cmd_timeout, pattern=cmd_pattern).response()
                        self._store_last_cmd_response(response, format)
                        return response
                    response = \
                        dev_handle.nodes[connect_dict["node"]].current_controller.vty(
                            command=connect_dict['cmd'], destination=connect_dict[
                                'destination'], timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response
                elif "controller" in keys:
                    if "disable_syslog" in keys and str(connect_dict['disable_syslog']).lower() == 'true':
                        response = \
                            dev_handle.current_node.controllers[connect_dict["controller"]].vty(
                                command="set syslog level 0", destination=connect_dict['destination'],
                                timeout=cmd_timeout).response()
                    if cmd_pattern is not None:
                        response = \
                            dev_handle.current_node.controllers[connect_dict["controller"]].vty(
                                command=connect_dict['cmd'], destination=connect_dict[
                                    'destination'], timeout=cmd_timeout,
                                pattern=cmd_pattern).response()
                        self._store_last_cmd_response(response, format)
                        return response
                    response = \
                        dev_handle.current_node.controllers[connect_dict["controller"]].vty(
                            command=connect_dict['cmd'], destination=connect_dict['destination'],
                            timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response
                if "disable_syslog" in keys and str(connect_dict['disable_syslog']).lower() == 'true':
                    response = dev_handle.vty(
                          command="set syslog level 0",
                          destination=connect_dict['destination'],
                          timeout=cmd_timeout).response()
                if cmd_pattern is not None:
                    response = dev_handle.vty(
                        command=connect_dict['cmd'],
                        destination=connect_dict['destination'],
                        timeout=cmd_timeout,
                        pattern=cmd_pattern).response()
                    self._store_last_cmd_response(response, format)
                    return response
                response = dev_handle.vty(
                    command=connect_dict['cmd'],
                    destination=connect_dict['destination'],
                    timeout=cmd_timeout).response()
                if "format" in keys:
                    cmd_format = connect_dict['format']
                if cmd_format is not None and cmd_format.lower() == 'xml':
                    response = self._cleanup_xml_namespace(response)

                self._store_last_cmd_response(response, format)
                return response

            elif cmd_mode == 'shell':
                if "user" in keys:
                    if connect_dict["user"] == 'su' and "password" in keys:
                        dev_handle.su(password=connect_dict['password'])
                    elif connect_dict["user"] == 'su':
                        dev_handle.su()
                if "node" in keys and "controller" in keys:
                    if cmd_pattern is not None:
                        response = \
                            dev_handle.nodes[connect_dict["node"]].controllers[connect_dict[
                                "controller"]].shell(command=connect_dict['cmd'],
                                                     timeout=cmd_timeout,
                                                     pattern=cmd_pattern).response()
                        # return response
                    else:
                        response = \
                            dev_handle.nodes[connect_dict["node"]].controllers[connect_dict[
                                "controller"]].shell(command=connect_dict['cmd'],
                                                     timeout=cmd_timeout).response()
                    # return response
                elif "node" in keys:
                    if cmd_pattern is not None:
                        response = \
                            dev_handle.nodes[connect_dict["node"]].current_controller.shell(
                                command=connect_dict['cmd'], timeout=cmd_timeout,
                                pattern=cmd_pattern).response()
                    else:
                        # return response
                        response = dev_handle.nodes[connect_dict[
                            "node"]].current_controller.shell(command=connect_dict['cmd'],
                                                              timeout=cmd_timeout).response()
                    # return response
                elif "controller" in keys:
                    if cmd_pattern is not None:
                        response = \
                            dev_handle.current_node.controllers[connect_dict["controller"]].shell(
                                command=connect_dict['cmd'], timeout=cmd_timeout,
                                pattern=cmd_pattern).response()
                    else:
                        # return response
                        response = \
                            dev_handle.current_node.controllers[connect_dict["controller"]].shell(
                                command=connect_dict['cmd'], timeout=cmd_timeout).response()
                    # return response
                elif cmd_pattern is not None:
                    response = dev_handle.shell(
                        command=connect_dict['cmd'], timeout=cmd_timeout,
                        pattern=cmd_pattern).response()
                    # return response
                else:
                    response = dev_handle.shell(
                        command=connect_dict['cmd'], timeout=cmd_timeout).response()

                if "format" in keys:
                    cmd_format = connect_dict['format']
                else:
                    cmd_format = "xml"

                if cmd_format == 'xml':
                    response = self._cleanup_xml_namespace(
                        response)

                self._store_last_cmd_response(response, format)
                return response

            elif cmd_mode == 'config':
                if "format" in keys:
                    cmd_format = connect_dict['format']
                else:
                    cmd_format = "text"
                if "config_mode" in keys:
                    config_mode = connect_dict['config_mode']
                else:
                    config_mode = ''
                if isinstance(connect_dict['cmd'], str):
                    connect_dict['cmd'] = [str(connect_dict['cmd'])]
                if "node" in keys and "controller" in keys:
                    response = dev_handle.nodes[connect_dict[
                        "node"]].controllers[connect_dict["controller"]].config(
                            command_list=connect_dict['cmd'], timeout=cmd_timeout, mode=config_mode).response()
                elif "node" in keys:
                    response = dev_handle.nodes[connect_dict[
                        "node"]].current_controller.config(command_list=connect_dict['cmd'],
                                                           timeout=cmd_timeout, mode=config_mode).response()
                elif "controller" in keys:
                    response = \
                        dev_handle.current_node.controllers[connect_dict["controller"]].config(
                            command_list=connect_dict['cmd'], timeout=cmd_timeout, mode=config_mode).response()
                elif cmd_pattern is not None:
                    response = dev_handle.config(
                        command_list=connect_dict['cmd'], timeout=cmd_timeout,
                        pattern=cmd_pattern, mode=config_mode).response()
                else:
                    response = dev_handle.config(
                        command_list=connect_dict['cmd'], timeout=cmd_timeout, mode=config_mode).response()

                if cmd_format == 'xml':
                    response = self._cleanup_xml_namespace(
                        response)
                    self._store_last_cmd_response(response, format)
                    return response

                self._store_last_cmd_response(response, format)
                return response

            elif cmd_mode == 'xml-rpc':

                cmd_str = connect_dict['cmd']

                if "node" in keys and "controller" in keys:
                    rpc_str = dev_handle.nodes[connect_dict["node"]].controllers[
                        connect_dict["controller"]].get_rpc_equivalent(command=cmd_str)
                    response = dev_handle.nodes[connect_dict[
                        "node"]].controllers[connect_dict["controller"]].execute_rpc(
                            command=rpc_str, timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response
                elif "node" in keys:
                    rpc_str = dev_handle.nodes[connect_dict[
                        "node"]].current_controller.get_rpc_equivalent(command=cmd_str)
                    response = dev_handle.nodes[connect_dict[
                        "node"]].current_controller.execute_rpc(command=rpc_str,
                                                                timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response

                elif "controller" in keys:
                    rpc_str = dev_handle.current_node.controllers[
                        connect_dict["controller"]].get_rpc_equivalent(
                            command=cmd_str)
                    response = \
                        dev_handle.current_node.controllers[connect_dict["controller"]].execute_rpc(
                            command=rpc_str, timeout=cmd_timeout).response()
                    self._store_last_cmd_response(response, format)
                    return response

                rpc_str = dev_handle.get_rpc_equivalent(
                    command=cmd_str)
                response = dev_handle.execute_rpc(
                    command=rpc_str, timeout=cmd_timeout).response()
                self._store_last_cmd_response(response, format)
                return response

            elif cmd_mode == 'cli':

                cmd_str = connect_dict['cmd']

                if "format" in keys:
                    cmd_format = connect_dict['format']
                else:
                    cmd_format = "xml"

                if "node" in keys and "controller" in keys:
                    if cmd_pattern is not None:
                        response = dev_handle.nodes[connect_dict["node"]].controllers[connect_dict[
                            "controller"]].cli(command=connect_dict['cmd'], format=cmd_format,
                                               timeout=cmd_timeout, pattern=cmd_pattern)
                    else:
                        response = dev_handle.nodes[connect_dict["node"]].controllers[connect_dict[
                            "controller"]].cli(command=connect_dict['cmd'], format=cmd_format,
                                               timeout=cmd_timeout)
                elif "node" in keys:
                    if cmd_pattern is not None:
                        response = dev_handle.nodes[connect_dict["node"]].current_controller.cli(
                            command=connect_dict['cmd'], format=cmd_format, timeout=cmd_timeout,
                            pattern=cmd_pattern)
                    else:
                        response = dev_handle.nodes[connect_dict["node"]].current_controller.cli(
                            command=connect_dict['cmd'], format=cmd_format,
                            timeout=cmd_timeout)
                elif "controller" in keys:
                    if cmd_pattern is not None:
                        response = dev_handle.current_node.controllers[connect_dict[
                            "controller"]].cli(command=connect_dict['cmd'], format=cmd_format,
                                               timeout=cmd_timeout, pattern=cmd_pattern)
                    else:
                        response = dev_handle.current_node.controllers[connect_dict["controller"]].cli(
                            command=connect_dict['cmd'], format=cmd_format,
                            timeout=cmd_timeout)
                else:
                    if cmd_pattern is not None:
                        response = dev_handle.cli(
                            command=connect_dict['cmd'],
                            format=cmd_format,
                            timeout=cmd_timeout,
                            pattern=cmd_pattern)
                    else:
                        response = dev_handle.cli(
                            command=connect_dict['cmd'],
                            format=cmd_format,
                            timeout=cmd_timeout)


                if (not isinstance(response, str)) and response.status():
                    response = response.response()
                else:
                    t.log(level='DEBUG', message="cannot execute the command")
                    raise Exception("Command execution has failed :"+response.response())

                if cmd_format == 'text':
                    if (not self.suppress_log) and (not self.suppress_overlimit_log):
                        t.log(level="info", message="Response: START\n")
                        t.log(level="info", message=response)
                        t.log(level="info", message="Response: END\n")
                    elif self.suppress_overlimit_log:
                        response_lines = len(response.split("\n"))
                        if response_lines <= self.suppress_log_limit:
                            t.log(level="info", message="Response: START\n")
                            t.log(level="info", message=response)
                            t.log(level="info", message="Response: END\n")
                        else:
                            t.log(
                                level="debug", message="Command response exceeded the supress limit and hence suppressing it.")
                    else:
                        t.log(
                            level="debug", message="Command reponse suppressed due to suppress_log flag.")

                elif cmd_format == 'xml':
                    response = self._cleanup_xml_namespace(response)
                    if (not self.suppress_log) and (not self.suppress_overlimit_log):
                        t.log(level="info", message="Response: START\n")
                        t.log(level="info", message=response)
                        t.log(level="info", message="Response: END\n")
                    elif self.suppress_overlimit_log:
                        response_lines = len(response)
                        if response_lines <= self.suppress_log_limit:
                            t.log(level="info", message="Response: START\n")
                            t.log(level="info", message=response)
                            t.log(level="info", message="Response: END\n")
                        else:
                            t.log(
                                level="debug", message="Command response exceeded the supress limit and hence suppressing it.")
                    else:
                        t.log(
                            level="debug", message="Command reponse suppressed due to suppress_log flag.")

                self._store_last_cmd_response(response, format)
                return response
            else:
                if "format" in keys:
                    cmd_format = connect_dict['format']
                else:
                    cmd_format = "xml"

                if cmd_pattern != None:
                    response = dev_handle.execute_command(mode=cmd_mode,
                                                          command=connect_dict['cmd'],
                                                          timeout=cmd_timeout, pattern=cmd_pattern).response()
                else:
                    response = dev_handle.execute_command(mode=cmd_mode,
                                                          command=connect_dict['cmd'],
                                                          timeout=cmd_timeout).response()

                if cmd_format == 'text':
                    if not self.suppress_log  and (not self.suppress_overlimit_log):
                        t.log(level="info", message="Response: START\n")
                        t.log(level="info", message=response)
                        t.log(level="info", message="Response: END\n")
                    elif self.suppress_overlimit_log:
                        response_lines = len(response.split("\n"))
                        if response_lines <= self.suppress_log_limit:
                            t.log(level="info", message="Response: START\n")
                            t.log(level="info", message=response)
                            t.log(level="info", message="Response: END\n")
                        else:
                            t.log(
                                level="debug", message="Command response exceeded the supress limit and hence suppressing it.")
                    else:
                        t.log(
                            level="debug", message="Command reponse suppressed due to suppress_log flag.")

                elif cmd_format == 'xml':
                    response = self._cleanup_xml_namespace(response)
                    if not self.suppress_log and (not self.suppress_overlimit_log):
                        t.log(level="info", message="Response: START\n")
                        t.log(level="info", message=response)
                        t.log(level="info", message="Response: END\n")
                    elif self.suppress_overlimit_log:
                        response_lines = len(response)
                        if response_lines <= self.suppress_log_limit:
                            t.log(level="info", message="Response: START\n")
                            t.log(level="info", message=response)
                            t.log(level="info", message="Response: END\n")
                        else:
                            t.log(
                                level="debug", message="Command response exceeded the supress limit and hence suppressing it.")
                    else:
                        t.log(
                            level="debug", message="Command reponse suppressed due to suppress_log flag.")


                self._store_last_cmd_response(response, format)
                return response

            self._store_last_cmd_response(response, format)
            return response

        else:
            if "user" in keys:
                if (connect_dict["user"] == 'su') and ("password" in keys):
                    dev_handle.su(password=connect_dict["password"])
                elif connect_dict["user"] == 'su' and "password" not in keys:
                    dev_handle.su()
            if cmd_pattern is not None:
                response = dev_handle.shell(
                    command=connect_dict['cmd'], timeout=cmd_timeout,
                    pattern=cmd_pattern).response()
                self._store_last_cmd_response(response, format)
                return response
            response = dev_handle.shell(
                command=connect_dict['cmd'], timeout=cmd_timeout).response()
            self._store_last_cmd_response(response, format)
            return response

    def _make_ifd_tvar(self):
        '''
        add more useful tvars from params
        '''
        t.log(level="debug", message="in make_ifd_tvar")
        for dev in self.t_handle:
            if self.t_handle[dev].get('interfaces'):
                for intf_tag in self.t_handle[dev]['interfaces']:
                    intf_data = self.t_handle[dev]['interfaces'][intf_tag]
                    # add ifd slot tvars
                    ifd = re.match(r'\w+-(\d+)/(\d+)/(\d+)', intf_data['pic'])
                    if ifd:
                        intf_data['fpcslot'] = ifd.group(1)
                        intf_data['picslot'] = ifd.group(2)
                        intf_data['portslot'] = ifd.group(3)
                        intf_data['slot'] = '/'.join(
                            [ifd.group(1), ifd.group(2), ifd.group(3)])
                        # if ifd.group(4):
                        #    intf_data['portchannel'] = ifd.group(4)
                        t.log(level="debug", message="intf_data  ::--\n" + str(intf_data))

        self.vars['ifd_desc'] = {}
        for dev in self.t_handle:
            if self.t_handle[dev].get('interfaces'):
                for intf_tag in self.t_handle[dev]['interfaces']:
                    intf_data = self.t_handle[dev]['interfaces'][intf_tag]
                    # add remote ifd tvars
                    link = intf_data['link']
                    find_remote = False
                    rdev = rintf_tag = None
                    for rdev in self.t_handle:
                        if self.t_handle[rdev].get('interfaces'):
                            for rintf_tag in self.t_handle[rdev]['interfaces']:
                                if rdev == dev:  # local device
                                    if rintf_tag == intf_tag:   # exclude itself
                                        continue
                                if self.t_handle[rdev]['interfaces'][rintf_tag]['link'] == link:
                                    find_remote = True
                                    break     # assuming no ethernet connections for now
                            else:
                                continue
                            break  # no remote enf found, for this interface, skip

                    if find_remote:
                        # use deepcopy for now.
                        # use reference instead can have the benefit of dynamic updates
                        # when the other side changes, but can get messy ( recursive mapping etc)
                        # intf_data['remote'] = self.tvar[rdev]['interfaces'][rintf_tag]
                        intf_data['remote'] = copy.deepcopy(
                            self.t_handle[rdev]['interfaces'][rintf_tag])
                        if intf_data['remote'].get('remote'):
                            del intf_data['remote']['remote']
                        intf_data['remote']['device_tag'] = rdev
                        intf_data['remote']['ifd_tag'] = rintf_tag

                        # build ifd description:
                        rdev_name = self.get_t_var(tv=rdev + '__primary__name')
                        rintf_name = self.get_ifd_from_tag(rdev, rintf_tag)
                        desc = 'link to {}: {} ({}: {})'.\
                            format(rdev_name, rintf_name, rdev, rintf_tag)
                        verify_utils.nested_set(
                            self.vars, ['ifd_desc', dev, intf_tag], desc)

        # lab assigned loop-ip processing? TBD

    def get_ifd_from_tag(self, device_tag, ifd_tag):
        '''
        Gives ifd name with give device_tag and ifd_tag in params

        ARGUMENTS:
            [device_tag, ifd_tag]
            :param STR device_tag:
                *MANDATORY* Device tag Name.
            :param STR ifd_tag:
                *MANDATORY* ifd tag name.

        ROBOT USAGE:
            Get Ifd From Tag      device_tag=Device_tag_name       ifd_tag=ifd_tag_name

        :return ifd otherwise cannot find ifd tag `ifd_tag` in `device_tag'
        '''
        ifd_tvar = device_tag.lower() + '__interfaces__' + ifd_tag.lower() + '__pic'
        ifd = self.get_t_var(tv=ifd_tvar)
        if ifd is None:
            raise Exception(
                'cannot find ifd tag {} in {}'.format(
                    ifd_tag, device_tag))

        # if ifd == ifd_tvar:
        #    raise Exception('cannot find ifd tag {} in {}'.format(ifd_tag, device_tag))

        return ifd

    def _get_xml_response(
            self,
            each_cmd,
            form,
            each_proto_data,
            dev,
            cmd_timeout=120,
            cmd_pattern=None):
        try:
            processed_data = self._get_response(
                each_cmd, form, each_proto_data.get(
                    'execute_on', None), dev, cmd_timeout, cmd_pattern)
            if self.log_text_output:
                t.log(level="info", message="Logging text output:")
                temp_suppress_log = self.suppress_log
                self.suppress_log = True
                self._get_response(
                    each_cmd, "text", each_proto_data.get(
                        'execute_on', None), dev, cmd_timeout, cmd_pattern)
                self.suppress_log = temp_suppress_log
        except Exception as ecp:
            t.log(level='warn', message="Unable to process the cmd due to"+str(ecp))
            #t.log(ecp)
            return False
        if isinstance(processed_data, str):
            t.log(
                level='debug',
                message="UNABLE TO PROCESS THE COMMAND PLEASE CHECK THAT COMMAND RETURN XML OUTPUT")
            return False
        else:
            tree = etree.parse(BytesIO(tostring(processed_data)))
            return tree

    def _execute_xpath(self, input_xml, tc_data):
        xpath_result = verify_utils.get_xpath_result(
            data=input_xml, xpath=tc_data['xpath'])
        temp_value = verify_utils._convert_lxml_to_data(xpath_result)
        if len(temp_value) == 1:
            return temp_value[0]
        else:
            return temp_value

    def _process_regex_match(self, match):
        '''
           Converts a list of tuples to a list of lists.
        '''
        return_value = []
        if not isinstance(match[0], tuple):
            return_value.append(match)
            return return_value
        tup_data_struct = False
        for tup in match:
            for tup_index in range(0, len(tup)):
                if not tup_data_struct:
                    return_value.append([])
                if tup[tup_index] != '':
                    return_value[tup_index].append(tup[tup_index])
            tup_data_struct = True
        return return_value
    def _execute_regexp(self, regexp, regexp_flags, processed_data, match_all):
        if regexp_flags is not None:
            regexp_flags = eval(regexp_flags)
            if match_all:
                var = re.findall(
                    regexp, processed_data, regexp_flags)
            else:
                var = re.search(
                    regexp, processed_data, regexp_flags)
        else:
            if match_all:
                var = re.findall(
                    regexp, processed_data)
            else:
                var = re.search(
                    regexp, processed_data)
        return var

    def _execute_grep(self, grep, grep_flags, processed_data):
        process_line = processed_data.splitlines()
        if isinstance(grep, list) is not True:
            grep = [grep]
        obtain_value = list()
        for each_grep in grep:
            for each_line in process_line:
                if grep_flags is not None:
                    grep_flags = eval(str(grep_flags))
                    if re.search(each_grep, each_line, grep_flags) is not None:
                        obtain_value.append(each_line)
                else:
                    if re.search(each_grep, each_line) is not None:
                        obtain_value.append(each_line)
        process_line = copy.deepcopy(obtain_value)
        return process_line

    def _execute_regexp_grep(
            self,
            tc_data,
            input_text,
            re_flag,
            re_flag_constant):
        if not self.suppress_log:
            t.log(level='debug', message="Data to process in  non-xml ...")
            t.log(level='debug', message=input_text)
        regx = tc_data.get('regexp', None)
        grepx = tc_data.get('grep', None)
        group = tc_data.get('group', 1)
        regexp_flags = tc_data.get('regexp_flags', None)
        grep_flags = tc_data.get('grep_flags', None)
        match_all = tc_data.get('match_all', False)
        operator = tc_data.get('operator', 'is-equal')

        obtain_value = ['_NONE']
        if regx is not None and grepx is not None:
            t.log(
                level='debug',
                message="Both Regexp and grep cant executed at the global level")
            return False
        if regx is not None:
            var = self._execute_regexp(regx, regexp_flags, input_text, match_all)
            if var is not None:
                try:
                    if isinstance(var, list):
                        var = self._process_regex_match(var)
                        obtain_value = var[group-1]
                    else:
                        obtain_value = var.group(group)
                except IndexError:
                    message = "Group index "+str(group)+" doesn't exist check your regex " +\
                        str(regx)+" with regexp_flags: "+repr(regexp_flags)+" and text" + str(input_text)
                    if operator == 'exists' or operator == 'not-exists':
                        t.log(level="debug",
                              message=message)
                    else:
                        t.log(level="error",
                              message=message)
                    obtain_value = ['_NONE']
            else:
                message = "regexp "+str(regx)+" with regexp_flags: "+repr(regexp_flags) +\
                    " failed for input text: "+str(input_text)+",does not return any value"
                if operator == 'exists' or operator == 'not-exists':
                    t.log(level="debug",
                          message=message)
                else:
                    t.log(level="error",
                          message=message)
                obtain_value = ['_NONE']

        if grepx is not None:
            t.log(level='debug', message="Entering into Grep...")
            obtain_value = self._execute_grep(grepx, grep_flags, input_text)

        if not self.suppress_log:
            t.log(level='debug', message="Obtained Value in non-xml process...")
            t.log(level='debug', message=obtain_value)
        if len(obtain_value) == 0:
            return ['_NONE']
        return obtain_value

    def _process_xpath_filter(self, xpath_filter, tc_data):
        xpath_filter_dict = {}
        if xpath_filter is None:
            return xpath_filter_dict

        _all_parameters = list(tc_data['_all_parameters'].keys())[:]
        t.log(level='debug', message="Before Sorting the all_paramters {}".format(
            str(_all_parameters)))
        _all_parameters.sort(key=len, reverse=True)
        t.log(level='debug', message="After Sorting the all_paramters {}".format(
            str(_all_parameters)))
        for each_filter in xpath_filter:
            _is_parameter_found = False
            t.log(level='debug', message="In filter Loop, Filter: " + each_filter)
            for each_parameter in _all_parameters:
                pattern = r'((\(\s*)|(\s+)|^)' + re.escape(each_parameter)
                if re.search(pattern, each_filter) is not None:
                    _is_parameter_found = True
                    t.log(
                        level='debug', message="Filter matching with parameter: " + each_parameter)
                    if tc_data['_all_parameters'][each_parameter].get('xpath', None) is not None:
                        xpath = tc_data['_all_parameters'][each_parameter].get(
                            'xpath', None)
                        parent_element_name = xpath.split('/')[-2]
                        actual_element_name = xpath.split('/')[-1]
                        each_filter = re.sub(
                            re.escape(each_parameter), actual_element_name, each_filter)
                        t.log(level='info', message="actual_element_name {}".format(
                            actual_element_name))
                    else:
                        xpath = tc_data['xpath']
                        parent_element_name = '_root_xpath'
                        actual_element_name = each_parameter
                        each_filter = re.sub(
                            re.escape(each_parameter), actual_element_name, each_filter)
                    t.log(level='debug', message="parent_element_name: " +
                          parent_element_name)
                    t.log(level='debug', message="filter : " + each_filter)
                    xpath_filter_dict.update(
                        {parent_element_name: each_filter})
                    break
            if _is_parameter_found is False:
                t.log(level='error', message="Filter {} Not Found..".format(
                    str(each_filter)))

        t.log(level='debug', message="xpath filter dict after processing  {}".format(
            str(xpath_filter_dict)))
        return xpath_filter_dict

    def _process_parameters(
            self,
            tc_data,
            test_data,
            tree,
            small_testcase_data,
            cmd,
            start_time,
            device_handle,
            is_get,
            is_ex_get,
            return_type,
            is_iterate=False):

        # Global iterate_for present or not.
        return_value = {}
        small_testcase_keys = list(small_testcase_data.keys())
        form = tc_data.get('format', 'xml')

        # common_template
        # support of xpath predicate and list of xpath values
        path_filter = small_testcase_data.get('xpath_filter', None)
        if path_filter is None:
            path_filter = tc_data.get('xpath_filter', None)

        path_filter_dict = self._process_xpath_filter(path_filter, tc_data)
        path = small_testcase_data.get('xpath', None)
        if path is None:
            path = test_data.get('xpath', None)
        if path and not isinstance(path, list):
            t.log(level="debug", message="\tpath=" + path)
            xpath_result = verify_utils.get_xpath_result(
                data=tree, xpath=path)
        else:
            xpath_result = tree

        if isinstance(path, list):
            t.log(level='debug', message="Root Path List: " + str(path))
            path = verify_utils.get_valid_xpaths(tree, path)
            t.log(level='debug', message="Valid Root Path List: " + str(path))

        if '_root_xpath' in path_filter_dict.keys():
            if isinstance(path, list):
                for index in range(len(path)):
                    path[index] = str(path[index]) + '[' + \
                        str(path_filter_dict['_root_xpath']) + ']'
            else:
                path = str(path) + str(path_filter_dict['_root_xpath'])

        t.log(level='debug', message="Valid Path with path_filter: " + str(path))

        # Result for iterate_for
        sub_result = False
        if not isinstance(small_testcase_data, OrderedDict):
            small_testcase_keys.sort()
        sub_result = True
        for small_values in small_testcase_keys:
            # Locally iterate for present or not.
            if small_values not in [
                    'iterate_until',
                    'iterate_for',
                    'xpath',
                    'include_all',
                    'skip',
                    'failmsg',
                    'passmsg',
                    'xpath_filter']:
                element_data = small_testcase_data[
                    small_values]
                element_data_keys = list(
                    element_data.keys())
                # check if the parameter name is in the skip list
                if small_values in self.skip:
                    t.log(level="debug", message="SKIPPING THE PARAMETER: "+str(small_values))
                    continue

                if not(path_filter_dict or isinstance(path, list)):
                    parameter_xpath = element_data.get('xpath', None)
                    if parameter_xpath is not None:
                        t.log(level="debug", message="parameter xpath: " + parameter_xpath)
                        xpath_results = verify_utils.get_xpath_result(
                            data=xpath_result, xpath=parameter_xpath)
                    else:
                        xpath_results = verify_utils.get_xpath_result(
                            data=xpath_result, xpath=small_values)
                else:
                    xpath_results = xpath_result

                subtest_spend_time = 0
                is_until_subtest_process = True
                subtest_result = True
                if is_get is not None:
                    temp_return = dict()
                else:
                    temp_return = True
                result = self._verify_parameters(
                    xpath_results,
                    element_data,
                    element_data_keys,
                    small_values,
                    is_get=is_get,
                    is_ex_get=is_ex_get,
                    return_type=return_type,
                    return_result=temp_return,
                    root_xpath=path,
                    xpath_filter_dict=path_filter_dict,
                    is_iterate=is_iterate)
                if is_get is not None and is_ex_get:
                    return_value.update(result)
                else:
                    if result is False:
                        subtest_result = False

                if result is False:
                    sub_result = False

        if is_get is not None and is_ex_get:
            return return_value
        if sub_result is False:
            return False
            # return_result = False

    def _verify_expression_testcase(self, tc_data, tc_name, device_handle, is_get,
                                    cli_args=[], global_args=[], expanded_tc_datas=[]):
        pre_res_data = dict()
        func = tc_data.get('func', None)
        expression = tc_data.get('expr', None)
        pre_req = sorted(tc_data.get('preq', []))
        is_get = tc_data.get('type', None)
        final_result = True
        return_dict = {}

        for each_req in pre_req:
            if each_req in list(tc_data.keys()):
                tc_data[each_req].update(
                    {'args': tc_data.get('args', None)})

                # segregating testcase data into iterate and non_iterate testcase data
                segregated_data = self._segregate_tc_data(tc_data[each_req])

                # Clear these global variables to avoid corruption of tc_data in the next testcase.
                self.iterate_tc_data = []
                self.noiterate_tc_data = {}
                self.noiterate_results = []
                self.iterate_results = []
                value = self._get_testcase_result(
                    segregated_data, device_handle, each_req, is_get=True,
                    cli_args=cli_args, global_args=global_args,
                    expanded_tc_datas=expanded_tc_datas)
            else:
                tmpl_data = self._search_template(each_req)
                if tmpl_data is False:
                    t.log(level='debug',
                          message="Proceeding with nextone")
                    continue
                formed_tmpl_data = self._merge_template_data(
                    tmpl_data, tc_data["template['" + each_req + "']"], each_req)
                verify_utils._replace_value(
                    tc_data, formed_tmpl_data, "template['" + each_req + "']")
                tc_data["template['" + each_req +
                        "']"].update({'args': tc_data.get('args', None)})

                # segregating testcase data into iterate and non_iterate testcase data
                segregated_data = self._segregate_tc_data(
                    tc_data["template['" + each_req + "']"])

                # Clear these global variables to avoid corruption of tc_data in the next testcase.
                self.iterate_tc_data = []
                self.noiterate_tc_data = {}
                self.noiterate_results = []
                self.iterate_results = []
                value = self._get_testcase_result(
                    segregated_data, device_handle, each_req, is_get=True,
                    cli_args=cli_args, global_args=global_args,
                    expanded_tc_datas=expanded_tc_datas)
            t.log(level='debug',
                  message="value for " +
                  each_req + " : ")
            t.log(level='debug', message=value)
            pre_res_data.update(value)

            if len(pre_res_data[each_req]) == 1:
                exec(each_req + "=pre_res_data['" + each_req + "'][0]")
            else:
                exec(each_req + "=pre_res_data['" + each_req + "']")

        if expression is not None:
            try:
                result = eval(expression)
            except Exception as ecp:
                t.log(level='error', message=ecp)
                result = False
        elif func is not None:
            sys.path.append(os.getcwd())

            for each_lib in self.process_pylib:
                try:
                    exec('from ' + each_lib + ' import *')
                except BaseException:
                    sys.path.append(self._suite_source_path)
                    exec('from ' + each_lib + ' import *')
            try:
                result = eval(func)
            except Exception as ecp:
                t.log(level='error', message=ecp)
                result = False

        t.log(level="info", message="\t\tTESTCASE :: " + tc_name)
        t.log(level="debug", message="\t\t==============================")
        t.log(level="debug", message="\t\tDATA FORMED :: " + str(pre_res_data))
        if expression is not None:
            t.log(level="debug", message="\t\tEXPRESSION :: " + expression)
        else:
            t.log(level="debug", message="\t\tfunction :: " + func)
        t.log(level="info", message="\t\tRESULT :: " + str(result))
        if is_get and tc_data.get('type', None) == 'get':
            if len(expanded_tc_datas) == 1:
                return {tc_name: [{'val': result}]}
            else:
                return_dict.update(
                    {tc_name: [{'val': result}]})
        # elif len(self.expanded_tc_datas) == 1:
        #    return result
        elif result is False:
            final_result = False

        if is_get is True and tc_data.get('type', None) == 'get':
            return return_dict
        else:
            self._put_tc_result_msg(
                tc_name, tc_data, str(device_handle), final_result)  # omkar should be device_name
            return final_result

    def _verify_testcase(self, tc_data, device_handle, tc_name, is_get=False, is_iterate=False,
                         cli_args=[], global_args=[], expanded_tc_datas=[]):
        """
        Process The each testcases further
        :param tc_data: Testcase data
        :param device_handle: device_handle handle
        :return:
        """

        t.log(level="debug", message="verify testcase data: ")
        t.log(level="debug", message=dict(tc_data))
        # initialize with default values
        self._last_verify_tc_name = tc_name
        if tc_name not in self._last_verify_result[self._last_verify_device_name].keys():
            self._last_verify_result[self._last_verify_device_name].update({
                tc_name: {}})
        self.error_message = None
        return_value = None
        return_result = True
        return_for_result = True
        is_until_process = True            # Used for process at least once
        is_until_present = False           # If if_utill present or not
        return_type = 'value'
        is_tc_type = tc_data.get('type', None)
        if is_tc_type is not None:
            is_tc_type = True
            return_type = tc_data.get('return_type', 'value')
        tc_data_keys = list(tc_data.keys())
        form = tc_data.get('format', 'xml')
        self.skip = tc_data.get("skip", [])
        temp_suppress_log = self.suppress_log
        self.suppress_log = tc_data.get('suppress_log', self.suppress_log)
        # TODO: Add limited suppression also here.
        timestamp = datetime.datetime.now()

        # replace var and tv variables in the all tc
        local_args = tc_data.get("args", [])
        if local_args == [] and global_args == [] and cli_args == []:
            args = []
        else:
            t.log(
                level="debug",
                message="Args before merging with cli args and global args: " +
                str(local_args))
            t.log(level="debug", message="Global args : " + str(global_args))
            t.log(level="debug", message="Command Line args : " + str(cli_args))
            local_args = self._sub_merge_args_list(cli_args, local_args)
            args = self._sub_merge_args_list(local_args, global_args)
            t.log(
                level="debug", message="Args after merging with cli args and global args: " + str(args))
        self.final_args = args
        self._substitute_variables(
            tc_data, args)

        cmd_timeout = verify_utils.convert_str_to_num_or_bool(
            tc_data.get('cmd_timeout', 120))
        if not isinstance(
                cmd_timeout,
                int) and not isinstance(
                    cmd_timeout,
                    float):
            t.log(level='error', message='Timeout must be either INT or FLOAT!')
            return False
        cmd_pattern = tc_data.get('cmd_pattern', None)

        # process modifier expands <<x..y>> and returns list of cmd to process
        test_data = self._expand_modifiers(tc_data)
        if test_data is False:
            t.log(level="error",
                  message="keyword 'cmd' not found in the testcase data.")
            return False
        test_data['cmd_list'] = str(test_data['cmd_list'])
        self._substitute_variables(
            test_data, verify_utils._get_temp_args(tc_data.get('args', [])))
        test_data['cmd_list'] = eval(test_data['cmd_list'])
        if len(test_data['cmd_list']) > 1:
            return_value = {tc_name: []}

        if 'expr' in tc_data_keys or 'func' in tc_data_keys:
            return self._verify_expression_testcase(tc_data, tc_name, device_handle, is_get,
                                                    cli_args=cli_args, global_args=global_args,
                                                    expanded_tc_datas=expanded_tc_datas)

        is_sub_testcase_exist = False

        # Check any verification present or not e.g. cmd and xpath
        # Present and called to get values
        for keys in tc_data_keys:
            if isinstance(
                    tc_data[keys],
                    dict) is True and keys not in [
                        'value',
                        'iterate_for',
                        'iterate_until',
                        'args',
                        'include_all',
                        'skip',
                        'execute_on',
                        'xpath_filter']:
                is_sub_testcase_exist = True
                break

        if "operator" in tc_data and "value" not in tc_data:
            tc_data["value"] = None

        # Process the xml data
        if form.lower() == 'xml':
            for each_cmd in test_data.get('cmd_list'):
                if each_cmd is None:
                    t.log(level='error', message='No command found in the testcase.')
                t.log(level="info", message="\tcmd = " + each_cmd)
                return_result = True

                # get_response to the command
                tree = self._get_xml_response(
                    each_cmd, form, tc_data, device_handle, cmd_timeout)
                if tree is False:  # omkar raise exception
                    t.log(level="info", message="No XML response received for the command: "+str(each_cmd))
                    return False

                # If only cmd and xpath present and called for get function
                if is_tc_type is not None and return_type != bool and is_sub_testcase_exist \
                        is not True:
                    if return_value is None:
                        return_value = {tc_name: []}
                    if isinstance(return_value[tc_name], list):
                        xpath_result = self._execute_xpath(tree, test_data)
                        if xpath_result is None or xpath_result == []:
                            return_value = {tc_name: '_NONE'}
                        else:
                            return_value[tc_name].append(xpath_result)
                    else:
                        t.log(
                            level='error',
                            message="Not able to Update result value of: " +
                            tc_name)
                # simple single TCs contain value at the same level as
                # command
                elif 'value' in tc_data.keys():
                    if test_data['xpath'] is not None:
                        t.log(level="debug", message="\tpath=" + str(test_data['xpath']))
                        try:
                            xpath_result = tree.xpath(test_data['xpath'])

                        except BaseException:
                            xpath_result = ['_NONE']
                        if len(xpath_result) == 0:
                            t.log(level="debug", message="\tpath:" +
                                test_data['xpath'] +
                                "\nELEMENT XPATH IS NOT RETURNING ANYTHING ,PLEASE CHECK CMD "
                                "AND XPATH")
                            xpath_result = ['_NONE']
                        obtain_value = xpath_result

                        # If get info is called
                        if is_tc_type is not None and return_type != 'bool' and is_get is True:
                            if return_value is None:
                                return_value = {tc_name: []}
                            if isinstance(return_value[tc_name], list):
                                xpath_result = self._execute_xpath(tree, test_data)
                                if xpath_result is None or xpath_result == []:
                                    return_value = {tc_name: '_NONE'}
                                else:
                                    return_value[tc_name].append(xpath_result)
                            else:
                                t.log(
                                    level='error',
                                    message="Not able to Update result value of : " +
                                    tc_name)
                        else:
                            result = self._evaluate(
                                tc_data.get(
                                    'value', None), obtain_value, tc_data.get(
                                        'operator', 'is-equal'), is_iterate=is_iterate)

                            # Printing the logs
                            self._put_verify_log(
                                testcase=tc_name, expect=tc_data.get(
                                    'value', None), obtain=obtain_value, opr=tc_data.get(
                                        'operator', 'is-equal'), result=result)

                        if result is False:
                            return_result = False
                        if is_tc_type is not None and return_type == 'bool' and is_get is True:
                            return_value.update({tc_name: result})

                # Process all the sub-TCs and parameter values
                if not isinstance(tc_data, OrderedDict):
                    tc_data_keys.sort()
                for keys in tc_data_keys:

                    if isinstance(
                            tc_data[keys],
                            dict) is True and keys not in [
                                'iterate_for',
                                'execute_on',
                                'iterate_until',
                                'include_all',
                                'skip',
                                'args',
                                '_all_parameters',
                                'failmsg',
                                'passmsg',
                                'xpath_filter']:
                        small_testcase_data = tc_data[keys]

                        #check if the sub-check is in the skip list.
                        if keys in self.skip:
                            t.log(level="debug", message="SKIPPING THE SUB-CHECK: "+str(keys))
                            continue

                        # Process the parameters
                        if keys == 'parameters':
                            temp_result = self._process_parameters(
                                tc_data,
                                test_data,
                                tree,
                                small_testcase_data,
                                each_cmd,
                                timestamp,
                                device_handle,
                                is_tc_type,
                                is_get,
                                return_type)
                            # If get is present update the value and else
                            # update the True or False
                            if is_tc_type is not None and is_get is True:
                                # if len(test_data['cmd_list']) == 1:
                                if return_value is None:
                                    return_value = {tc_name: {}}
                                if isinstance(return_value[tc_name], list):
                                    return_value[tc_name].append(
                                        temp_result)
                                else:
                                    return_value[tc_name].update(
                                        temp_result)
                            else:
                                if temp_result is False:
                                    return_result = False

                        # process sub testcase with parameters
                        elif 'parameters' in small_testcase_data.keys():

                            path = small_testcase_data.get('xpath', None)
                            it_for = small_testcase_data.get(
                                'iterate_for', None)
                            it_until = small_testcase_data.get(
                                'iterate_until', None)
                            small_testcase_data = tc_data[keys]['parameters']
                            if path is not None:
                                small_testcase_data.update({'xpath': path})
                            if it_for is not None:
                                small_testcase_data.update(
                                    {'iterate_for': it_for})
                            if it_until is not None:
                                small_testcase_data.update(
                                    {'iterate_for': it_until})
                            temp_result = self._process_parameters(
                                tc_data,
                                test_data,
                                tree,
                                small_testcase_data,
                                each_cmd,
                                timestamp,
                                device_handle,
                                is_tc_type,
                                is_get,
                                return_type)
                            if is_tc_type is not None and is_get is True:

                                if return_value is None:
                                    return_value = {tc_name: {}}
                                if isinstance(return_value[tc_name], list):
                                    return_value[tc_name].append(
                                        temp_result)
                                else:
                                    return_value[tc_name].update(
                                        temp_result)
                            else:
                                if temp_result is False:
                                    return_result = False

                        # precess testcase without parameters
                        else:
                            is_until_sub_process = True
                            is_until_sub_present = False
                            xpath_result = []
                            path_list = []
                            sub_result = False
                            sub_result = True
                            path = small_testcase_data.get(
                                'xpath', test_data['xpath'])
                            t.log(level="info", message="XPATH :" + str(path))
                            try:
                                if (isinstance(path, ruamel.yaml.comments.CommentedSeq)):
                                    path_list = path.copy()
                                elif isinstance(path, str):
                                    path_list.append(path)
                                t.log(level="debug", message=type(path))

                                if len(path_list) == 1:
                                    xpath_result = tree.xpath(path)
                                else:
                                    count = len(path_list)
                                    index = 1
                                    for path1 in path_list:
                                        try:
                                            xpath_result = tree.xpath(path1)
                                            if (len(xpath_result) == 0 and (index != count)):
                                                index += 1
                                                continue
                                            t.log(level="debug", message=xpath_result)
                                            break
                                        except:
                                            if index == count:
                                                raise BaseException
                                            else:
                                                index += 1
                                                continue


                            except BaseException:
                                xpath_result = ['_NONE']
                            if len(xpath_result) == 0:
                                t.log(level="info", message="\tpath:" + path +
                                    "\nELEMENT XPATH IS NOT RETURNING ANYTHING ,PLEASE "
                                    "CHECK CMD AND XPATH")
                                xpath_result = ['_NONE']
                            obtain_value = xpath_result
                            t.log(level="debug", message=obtain_value)
                            if is_tc_type is not None and return_type != 'bool' and is_get:
                                temp_value = list()
                                for each_xpath_result in xpath_result:
                                    try:
                                        temp_value.append(
                                            each_xpath_result.text)
                                    except BaseException:
                                        t.log(level="debug", message="NOT ABLE TO FIND THE TEXT ,RETURNING LXML object")
                                        temp_value.append(
                                            each_xpath_result)
                                if len(temp_value) == 1:
                                    tmp_result = temp_value[0]
                                else:
                                    tmp_result = temp_value
                                if return_value is None:
                                    return_value = {tc_name: {}}
                                if isinstance(
                                        return_value[tc_name], list):
                                    return_value[tc_name].append(
                                        {keys: tmp_result})
                                else:
                                    return_value[tc_name].update(
                                        {keys: tmp_result})
                            else:
                                result = self._evaluate(
                                    small_testcase_data.get(
                                        'value', None), obtain_value,
                                    small_testcase_data.get(
                                        'operator', 'is-equal'),
                                    is_iterate=is_iterate)
                                self._put_verify_log(
                                    testcase=keys, expect=small_testcase_data.get(
                                        'value', None), obtain=obtain_value,
                                    opr=small_testcase_data.get(
                                        'operator', 'is-equal'),
                                    result=result, tc_data=small_testcase_data)
                            if is_tc_type is not None and is_get:
                                if return_type == 'bool':
                                    if return_value is None:
                                        return_value = {tc_name: {}}
                                    if isinstance(
                                            return_value[tc_name], list):
                                        return_value[tc_name].append(
                                            {keys: result})
                                    else:
                                        return_value[tc_name].update(
                                            {keys: result})
                            else:
                                if result is False:
                                    sub_result = False

                            if sub_result is False:
                                return_result = False

        elif form.lower() == 'text':

            re_flag_constant = {
                'I': 2,
                'L': 4,
                'M': 8,
                'S': 16,
                'X': 64,
                'U': 32}
            re_flag = tc_data.get('regexp_flags', None)
            for each_cmd in test_data['cmd_list']:
                t.log(level='info', message="\tcmd = " + each_cmd)
                spend_time = 0
                is_until_process = True
                return_result = True
                try:
                    processed_data = self._get_response(each_cmd, form, tc_data.get(
                        ('execute_on'), None), device_handle, cmd_timeout, cmd_pattern)
                except Exception as ecp:
                    t.log(level='warn', message="Unable to process the cmd due to"+str(ecp))
                    #t.log(ecp)
                    return False
                # Execute this if get function is present and sub testcase is not present.
                # Testcase format is simple.
                # is_tc_type is yaml get function flag and is_get is robot
                # get function flag.
                if is_tc_type is not None and return_type != bool and is_sub_testcase_exist \
                        is False and is_get:
                    obtain_value = self._execute_regexp_grep(
                        tc_data, processed_data, re_flag, re_flag_constant)

                    if len(obtain_value) == 1:
                        tmp_ob_val = obtain_value[0]
                    else:
                        tmp_ob_val = obtain_value

                    if return_value is None:
                        return_value = {tc_name: []}
                    if isinstance(return_value[tc_name], list):
                        return_value[tc_name].append(tmp_ob_val)
                    else:
                        t.log(
                            level='error',
                            message="Not able to Update result value of : " +
                            tc_name)
                elif 'value' in tc_data.keys():
                    obtain_value = self._execute_regexp_grep(
                        tc_data, processed_data, re_flag, re_flag_constant)
                    if is_tc_type is not None and return_type != bool and is_get:
                        if len(obtain_value) == 1:
                            tmp_ob_val = obtain_value[0]
                        else:
                            tmp_ob_val = obtain_value
                        if return_value is None:
                            return_value = {tc_name: []}
                        if isinstance(return_value[tc_name], list):
                            return_value[tc_name].append(
                                tmp_ob_val)
                        else:
                            t.log(
                                level='error',
                                message="Not able to Update result value of : " +
                                tc_name)
                    else:
                        op_value = tc_data.get(
                            'operator', 'is-equal')
                        ex_value = tc_data.get('value', None)
                        result = self._evaluate(expect_value=ex_value,
                                                obtained_value=obtain_value,
                                                opr=op_value, is_iterate=is_iterate)

                        self._put_verify_log(
                            testcase=tc_name,
                            expect=ex_value,
                            obtain=obtain_value,
                            opr=op_value,
                            result=result)
                        if is_tc_type is not None and return_type == bool and is_get:
                            if return_value is None:
                                return_value = {tc_name: []}
                            if isinstance(return_value[tc_name], list):
                                return_value[tc_name].append(result)
                            else:
                                t.log(
                                    level='error',
                                    message="Not able to Update result value of : " +
                                    tc_name)
                        if result is False:
                            return_result = False
                else:
                    tc_data_keys = tc_data.keys()
                    if not isinstance(tc_data, OrderedDict):
                        tc_data_keys = sorted(tc_data.keys())
                    for each_test_case in tc_data_keys:
                        regx = tc_data.get('regexp', None)
                        grepx = tc_data.get('grep', None)
                        regexp_flags = tc_data.get('regexp_flags', None)
                        grep_flags = tc_data.get('grep_flags', None)
                        match_all = tc_data.get('match_all', False)
                        obtain_value = ['_NONE']
                        if regx is not None and grepx is not None:
                            t.log(level="info", message="Both Regexp and grep cant executed at the global level")
                            return False
                        if regx is not None:
                            var = self._execute_regexp(
                                regx, regexp_flags, processed_data, match_all)

                        if grepx is not None:
                            obtain_value = self._execute_grep(
                                grepx, grep_flags, processed_data)
                            if len(obtain_value) == 0:
                                obtain_value = ['_NONE']

                        if isinstance(
                                tc_data[each_test_case],
                                dict) and each_test_case not in [
                                    'iterate_for',
                                    'iterate_until',
                                    'execute_on',
                                    'include_all',
                                    'match_all',
                                    'skip',
                                    'args',
                                    '_all_parameters',
                                    'failmsg',
                                    'passmsg']:

                            is_until_sub_process = True
                            sub_result = True
                            var = None
                            sub_result = True
                            if 'regexp' in list(
                                    tc_data[each_test_case].keys()) or 'regexp' in list(
                                        tc_data.keys()):
                                if 'regexp' in list(
                                        tc_data[each_test_case].keys()):
                                    regx = tc_data[
                                        each_test_case]['regexp']
                                    regexp_flags = tc_data[each_test_case].get(
                                        'regexp_flags', None)
                                elif 'regexp' in list(tc_data.keys()):
                                    regx = tc_data['regexp']
                                    regexp_flags = tc_data.get(
                                        'regexp_flags', None)
                                var = self._execute_regexp(
                                    regx, regexp_flags, processed_data, match_all)

                            if 'grep' in list(
                                    tc_data[each_test_case].keys()):
                                grepx = tc_data[
                                    each_test_case]['grep']
                                grep_flags = tc_data[each_test_case].get(
                                    'grep_flags', None)
                                obtain_value = self._execute_grep(
                                    grepx, grep_flags, processed_data)
                                if len(obtain_value) == 0:
                                    obtain_value = ['_NONE']
                            ex_value = tc_data[
                                each_test_case].get('value', None)
                            op_value = tc_data[each_test_case].get(
                                'operator', 'is-equal')
                            group = tc_data[
                                each_test_case].get('group', 1)
                            if regx is not None:
                                try:
                                    if var is not None:
                                        if isinstance(var, list):
                                            var = self._process_regex_match(var)
                                            obtain_value = var[group-1]
                                        else:
                                            obtain_value = var.group(group)
                                    else:
                                        obtain_value = ['_NONE']
                                        message = "regexp \""+str(regx)+"\" with regexp_flags \"" +\
                                            repr(regexp_flags) + \
                                            "\" failed, please check."
                                        if is_iterate:
                                            self.error_message = message
                                        else:
                                            if op_value == 'exists' or op_value == 'not-exists' or 'acceptnone' in op_value.lower():
                                                t.log(level="debug",
                                                      message=message)
                                            else:
                                                t.log(level="error",
                                                      message=message)
                                except IndexError:
                                    message = "regexp \""+str(regx)+"\" with regexp_flags \"" +\
                                        repr(regexp_flags)+"\" failed, does not" +\
                                        " return any value for the group " + \
                                        str(group)
                                    if is_iterate:
                                        self.error_message = message
                                    else:
                                        if op_value == 'exists' or op_value == 'not-exists' or 'acceptnone' in op_value.lower():
                                            t.log(level="debug",
                                                  message=message)
                                        else:
                                            t.log(level="error",
                                                  message=message)
                            if is_tc_type is not None and return_type != bool and is_get:
                                if len(obtain_value) == 1:
                                    tmp_ob_val = obtain_value[0]
                                else:
                                    tmp_ob_val = obtain_value
                                if return_value is None:
                                    return_value = {tc_name: {}}
                                if isinstance(
                                        return_value[tc_name], list):
                                    return_value[tc_name].append(
                                        {each_test_case: tmp_ob_val})
                                else:
                                    return_value[tc_name].update(
                                        {each_test_case: tmp_ob_val})

                            else:
                                result = self._evaluate(
                                    expect_value=ex_value, obtained_value=obtain_value,
                                    opr=op_value, is_iterate=is_iterate)

                                self._put_verify_log(
                                    testcase=each_test_case,
                                    expect=ex_value,
                                    obtain=obtain_value,
                                    opr=op_value,
                                    result=result,
                                    tc_data=tc_data[each_test_case])

                                if is_tc_type is not None and return_type == bool \
                                        and is_get:

                                    if return_value is None:
                                        return_value = {tc_name: {}}
                                    if isinstance(
                                            return_value[tc_name], list):
                                        return_value[tc_name].append(
                                            {each_test_case: result})
                                    else:
                                        return_value[tc_name].update(
                                            {each_test_case: result})
                                if result is False:
                                    sub_result = False

                            if sub_result is False:
                                return_result = False

        self.suppress_log = temp_suppress_log
        if is_tc_type is not None:
            return return_value
        # TODO: Add limited suppression also here.
        if not return_result:
            fail_message = "Verify_Testcase: failed testcase data."
            verify_utils.create_ve_debug_log(tc_data, fail_message)
        return return_result

    def _update_convergence(
            self,
            convergence_time,
            is_get,
            return_value,
            tc_name):
        if convergence_time is not None:
            hours, minutes, seconds = re.split(':', convergence_time)
            self._last_verify_result[self._last_verify_device_name][
                self._last_verify_tc_name].update({"convergence_time": float(datetime.timedelta(
                    hours=float(hours), minutes=float(minutes),
                    seconds=float(seconds)).total_seconds())})

        return None, None

        # if is_get is not None:
        #    if isinstance(return_value[tc_name], list):
        #        if convergence_time is not None:
        #            h, m, s = re.split(':', convergence_time)
        #            return "append",{"convergence_time": float(datetime.timedelta(hours=float(h),
        #               minutes=float(m), seconds=float(s)).total_seconds())}
        #        else:
        #            return None,None
        #    else:
        #        if convergence_time is not None:
        #            h, m, s = re.split(':', convergence_time)
        #            return "update", {"convergence_time": float(datetime.timedelta(hours=float(h),
        #               minutes=float(m), seconds=float(s)).total_seconds())}
        #        else:
        #            return None,None
        # else:
        #    return None,None

    def _get_monotonic_time(self):
        #  Get Monotonic Raw time. This method is used to calculate convergence time
        #  provides access to a raw hardware-based time that is not subject to NTP adjustments
        now = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
        mlsec = repr(now).split('.')[1][:3]
        dd = time.strftime("%Y-%m-%d %H:%M:%S.{}".format(mlsec), time.localtime(now))
        t = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S.%f")
        return t

    def _update_until(self, it_count, interval, spend_time):
        it_count += 1
        t.log_interval = str(interval)
        t.log(level='debug', message="sleeping for " + t.log_interval)
        time.sleep(interval)
        spend_time += interval
        return it_count, spend_time

    def _is_converge(
            self,
            is_until_present,
            spent_time,
            timeout,
            tc_result,
            is_until_for_present,
            timestamp1):
        '''
           Check if convergence happened or not.
           and based on that it will return
           convergence_result, convergence_time
        '''

        if is_until_present is False or spent_time >= timeout or tc_result is True:
            if is_until_for_present is True and spent_time >= timeout:
                timestamp2 = self._get_monotonic_time()
                delta = timestamp2 - timestamp1
                t.log_delta = str(delta)
                t.log(level='debug', message="\t\tCONVERGENCE TIME : " + t.log_delta)
                return True, t.log_delta
            elif is_until_for_present is True:
                return False, None
            else:
                if tc_result is True and is_until_present is True:
                    timestamp2 = self._get_monotonic_time()
                    t.log_delta = str(timestamp2 - timestamp1)
                    t.log(level='debug', message="\t\tCONVERGENCE TIME : " + t.log_delta)
                    return True, t.log_delta
                return True, None
        return False, None

    def _put_verify_log(
            self,
            testcase=None,
            expect=None,
            obtain=None,
            opr=None,
            result=None,
            extra_dict=None,
            tc_data=None):
        obtain_str = ""
        obtain_val = ""
        if tc_data is None:
            tc_data = dict()
        if 'count' in opr:
            if (len(obtain) == 1 and obtain[0] ==
                    '_NONE') or str(obtain) == "_NONE":
                obtain_str = str('0')
                obtain_val = 0
            else:
                obtain_str = str(len(obtain))
                obtain_val = len(obtain)
        else:
            if isinstance(obtain, list):
                for each_value in range(0, len(obtain)):
                    if isinstance(obtain[each_value], etree._Element):
                        obtain[each_value] = obtain[each_value].text
                if len(obtain) == 1 and obtain[0] == '_NONE':
                    obtain_str = '_NONE'
                    obtain_val = '_NONE'
                elif len(obtain) == 1:
                    obtain_str = str(obtain[0])
                    obtain_val = obtain[0]
                else:
                    obtain_str = str(obtain)
                    obtain_val = obtain
            else:
                obtain_str = str(obtain)
                obtain_val = obtain
        test_str = str(testcase)
        expect_str = str(expect)
        res_str = str(result)

        verify_result = {
            'expected_value': expect,
            'result': result,
            'obtained_value': obtain_val}

        if result is False:
            t.log(level="info", message="\t**********************")
        t.log(level="info", message="\t" + test_str)
        if result is False:
            t.log(level="info", message="\t**********************")
        else:
            t.log(level="info", message="\t----------------------")
        t.log(level="info", message="\t\tEXPECTED VALUE :'" + expect_str + "'")
        t.log(level="info", message="\t\tOBTAINED VALUE : '" + obtain_str + "'")
        t.log(level="info", message="\t\tOPERATOR : '" + opr + "'")
        t.log(level="info", message="\t\tRESULT : " + res_str)

        if extra_dict is not None:
            ex_me_str = str(extra_dict.message)
            ex_re_str = str(extra_dict.result)
            t.log(level="info", message="\t\t" + ex_me_str + " :" + ex_re_str)

        if isinstance(self._last_verify_result, dict):
            if self._last_verify_device_name in self._last_verify_result.keys() \
                    and self._last_verify_tc_name in \
                    self._last_verify_result[self._last_verify_device_name].keys():
                if self._last_verify_tc_name == testcase:
                    self._last_verify_result[self._last_verify_device_name][
                        self._last_verify_tc_name].update(verify_result)
                else:
                    self._put_sub_tc_result_msg(testcase, tc_data, result)
                    verify_result = {testcase: verify_result}
                    self._last_verify_result[self._last_verify_device_name][
                        self._last_verify_tc_name].update(verify_result)

    def _search_and_retrieve_tc_data(self, data, device, test_data, testcase):
        '''
           Retrieves the relevant test data for the keys in test_data.
        '''
        is_present_in_yaml = False
        temp_data_result = None
        temp_data_value = None
        path = ""

        for each_data in data:
            device_name = list(each_data.keys())
            device_name = device_name[0]
            if device_name == device:
                temp_data_result, path = verify_utils.find_dict_data(
                    data=each_data, key_list=test_data)
                temp_test_data = testcase.split(':')
                if temp_data_result is not None:
                    path_test_data = list(temp_test_data)
                    path_test_data = path[
                        :(path.index(path_test_data[0])) + 1]
                    temp_data_value, path = verify_utils.find_dict_data(
                        data=each_data, key_list=path_test_data)
                    is_present_in_yaml = True

        if is_present_in_yaml is False:
            path_test_data = list(test_data)
            for each_data in data:
                temp_data_result, path = verify_utils.find_dict_data(
                    data=each_data, key_list=test_data)
                if temp_data_result is not None:
                    path_test_data = path[
                        :(path.index(path_test_data[0])) + 1]
                    temp_data_value, path = verify_utils.find_dict_data(
                        data=each_data, key_list=path_test_data)
                    break
        return temp_data_result, temp_data_value, path

    def verify_specific_checks_api(self, **kwargs):
        """
        Helps user to directly call the test case name from robot file.

        DESCRIPTION:
        1.verify ospf_interface_check on device1
        2.verify ospf_interface_check:check_interface_metric on device0


        ARGUMENTS:
            [kwargs]
                :param STR testcases:
                    *OPTIONAL* statement to call the testcase name.Default is set to None.
                :param STR devices:
                    *MANADATORY* Device name.
                :param STR cheks:
                    *OPTIONAL* checks name.

        ROBOT USAGE:
            ${status} =     Verify Specific Checks Api   checks=check_if_vc     devices=r0

        :return:result or False.
        """
        # Used to setup environment variables
        self._setup()

       # Vars().set_global_variable("${VE_LAST_VERIFY_RESULT}", {})
        self._showdump = None
        if self.is_VE_offline is True:
            self.offline_data = kwargs.get('offline_data', None)
            if self.offline_data is None:
                t.log(level='error', message="Unable to find the offline data")
                return False
            self.t_handle = kwargs.get('t_handle', None)
            if self.t_handle is None:
                t.log(level='error', message="Unable to find the t data")
                return False

        # Default condition for every testcase.
        self.user_optimized = kwargs.get("optimize", False)

        testcases = kwargs.get('checks', None)
        if testcases is None:
            testcases = kwargs.get('info', None)

        ## Pass 'testcases' to _execute_testcase via verify_all_checks_api
        ## This is needed for skipping verification when specific check called itself is being skipped
        checks_robot_arg = testcases

        devices_arg = kwargs.get('devices', None)
        verify_dh = kwargs.get('device_handle', None)
        verify_file = kwargs.get('file', None)
        verify_data = kwargs.get('data', None)
        is_get = kwargs.get('type', None)
        stanza = kwargs.get('args', None)
        val = kwargs.get('value', None)
        opr = kwargs.get('operator', None)
        _parameters = kwargs.get('parameters', None)
        _parameters = copy.deepcopy(_parameters)
        add_data = kwargs.get('dict', None)
        # common_template
        # parse cmc argument from Robot Keyword
        cmd = kwargs.get('cmd', None)
        do_parallel = kwargs.get('do_parallel', False)
        verify_parallel = kwargs.get('verify_parallel', False)
        new_args = None
        params_dict = kwargs.get('params_dict', None)
        iterator_data = kwargs.get('iterator', None)
        self._showdump = kwargs.get('showdump', None)
        self.suppress_log = kwargs.get('suppress_log', True)
        self.log_text_output = kwargs.get(
            "log_text_output", self.global_log_text_output)
        self.suppress_overlimit_log = kwargs.get(
            'suppress_overlimit_log', False)
        self.suppress_log_limit = kwargs.get('suppress_log_limit', 100)
        xpath_filter = kwargs.get('xpath_filter', None)

        if self.is_VE_offline is True and isinstance(stanza, str):
            stanza = eval(stanza)
        if isinstance(stanza, dict):
            if len(stanza.keys()) == 1 and list(stanza.keys())[0] == 'args':
                new_args = stanza
            else:
                new_args = {'args': []}
                for k, v in stanza.items():
                    temp_dict = {k: v}
                    new_args['args'].append({k: v})
        elif isinstance(stanza, list):
            new_args = {'args': stanza}
        elif stanza is not None:
            arg_values = stanza.split(' and ')
            new_args = {'args': []}
            for each_args in arg_values:
                new_value_key = each_args.split(' as ')
                if ':' in new_value_key[0]:
                    tmp_value = new_value_key[0].split(':')
                    if tmp_value[0].lower() == 'args':
                        new_args['args'].append(
                            {tmp_value[1]: new_value_key[1]})
                    else:
                        if tmp_value[0] not in list(new_args.keys()):
                            new_args.update({tmp_value[0]: {}})

                        new_args[tmp_value[0]].update(
                            {tmp_value[1]: new_value_key[1]})
                else:
                    new_args['args'].append(
                        {new_value_key[0]: new_value_key[1]})
        if (devices_arg is None and verify_dh is None) or testcases is None:
            if devices_arg is None and verify_dh is None:
                t.log(
                    level='error',
                    message="Mandatory argument \"devices/device_handle\" not provided.")
            elif testcases is None:
                t.log(
                    level='error',
                    message="Mandatory argument \"checks\" not provided.")
            self._showdump = None
            return False

        if devices_arg is not None:
            devices = devices_arg.split(",")
            for i in range(0, len(devices)):
                device_arg_list = devices[i].split("__")
                execute_on = {}
                if len(device_arg_list) > 1:
                    for arg_index in range(1, len(device_arg_list)):
                        regex = re.search(
                            r'(\w+)\[(.*)\]', device_arg_list[arg_index], re.I)
                        execute_on.update({regex.group(1): regex.group(2)})
        else:
            devices = []
            if not verify_parallel:
                self._device_handle = []
            self._device_handle.append(verify_dh)

        self.process_tmpl_data = []
        self.process_tmpl_file = []
        self.process_data = []
        self.process_pylib = []
        global_args = []
        use_tmpl = []

        if kwargs.get('is_robot', False):
            # --------------------------------------
            #   print fail message if verify fails
            #   do not print fail message if type is get
            # --------------------------------------
            self._default_failmsg = "+ VERIFY FAILED: " + \
                testcases + " On Devices: " + str(devices)

        """
           Checking if the testcase is of the format :
                <testcaseName>:parameters:[parmeter1, parameter2]
           and converting them into :
                <testcaseName>:parameters:parmeter1
                <testcaseName>:parameters:parameter2
        """
        while True:
            var = re.search(r'(^|\,)*([^,]*?\:\[.*?\])', testcases)
            # print(var.group(2))
            if var is not None:
                if var.group(0)[0] == ',':
                    expand_testcase = ',' + \
                        verify_utils.expand_sub_testcases(var.group(0))
                else:
                    expand_testcase = verify_utils.expand_sub_testcases(
                        var.group(0))
                testcases = re.sub(
                    r'(^|\,)*([^,]*?\:\[.*?\,*.*?])',
                    expand_testcase,
                    testcases,
                    1)
            else:
                break

        tmp_tcs = testcases.split(',')
        if verify_file is None and verify_data is None and self.verification_file is None and\
           not all(tc.startswith('j_check_') for tc in tmp_tcs):
            t.log(level='error', message=" No file found for verification ")
            self._showdump = None
            return False
        elif verify_file is None and verify_data is None:
            verify_file = self.verification_file
            self.process_tmpl_data = copy.deepcopy(self.tmpl_data)
            self.process_pylib = copy.deepcopy(self.pylib)
            self.process_data = copy.deepcopy(self.ve_data)
            use_tmpl = self.tmpl_file
            global_args = copy.deepcopy(self.init_global_args)
        elif verify_data is None:
            verify_file_data = None
            verify_file = verify_file.split(',')
            for each_file in verify_file:
                log_file_version(each_file)
                file_data = verify_utils.get_yaml_data_as_dict(
                    each_file, self.keywords, self.yaml_file_data)
                if isinstance(file_data, dict):
                    if 'verify' in file_data:
                        verify_file_data = file_data['verify']
                        global_args.extend(verify_file_data.get('args', []))
                        self.process_tmpl_file.extend(
                            self._expand_file_list(
                                verify_file_data.get(
                                    'use_template', [])))
                        self.process_pylib.extend(
                            verify_file_data.get('use_library', list()))
                        pre_result = self._pre_process_testcases(each_file)
                    elif 'verify_tmpl' in file_data or 'verify_template' in file_data:
                        self.process_tmpl_file.append(each_file)
                        self._source_templates({}, file_data)
                        pre_result = {}
                    if pre_result.get('result', None) is False:
                        self._showdump = None
                        return False
                    self.process_data.extend(pre_result.get('data', list()))
            use_tmpl = self.process_tmpl_file
        elif verify_file is None:
            verify_file_data = None
            src_path = get_log_dir()
            if isinstance(verify_data, str):
                verify_data_file = os.path.join(src_path, 'userdata.yaml')
                with open(verify_data_file, 'w') as outfile:
                    outfile.write(verify_data)
                outfile.close()
                file_data = verify_utils.get_yaml_data_as_dict(
                    verify_data_file, self.keywords, self.yaml_file_data)
            elif isinstance(verify_data, dict):
                file_data = verify_utils.replace_with_case(
                    verify_data, self.keywords)
            else:
                t.log(
                    level="error", message="Parameter 'verify_data' should be either a string or dictionary")
                return False
            if isinstance(file_data, dict):
                if 'verify' in file_data:
                    verify_file_data = file_data['verify']
                    global_args = verify_file_data.get('args', [])
                    self.process_tmpl_file.extend(
                        self._expand_file_list(
                            verify_file_data.get(
                                'use_template', [])))
                    self.process_pylib.extend(
                        verify_file_data.get('use_library', list()))

                pre_result = self._pre_process_testcases(verify_data_file)
                if pre_result['result'] is False:
                    self._showdump = None
                    return False
                self.process_data.extend(pre_result.get('data', list()))
            use_tmpl = self.process_tmpl_file

        if not self.t_handle:
            self.t_handle = t.t_dict['resources'].copy()
            self._make_ifd_tvar()
        use_lib = copy.deepcopy(self.process_pylib)
        data = copy.deepcopy(self.process_data)

        if len(use_tmpl) > 0:
            temp_var_data = copy.deepcopy(self.process_tmpl_data)
            dummy_hash = {}
            for x in range(0, len(temp_var_data)):
                dummy_hash.update(temp_var_data[x])
            data.extend([{'device_template': dummy_hash}])

        if devices_arg is None:
            if verify_parallel:
                devices = ["dh["+str(self.dh_count)+"]"]
            else:
                devices = ["dh[0]"]
        yaml_data = OrderedDict()
        for each_devices in devices:
            yaml_data[each_devices] = OrderedDict()

        t.log(level="debug", message="testcase...\n" + str(testcases))
        all_test_cases = testcases.split(',')
        parameter = None

        """
           For each test case get the specific data and save it to tmpdata.yaml
        """
        for each_testcase in all_test_cases:
            is_present_in_yaml = False
            test_data = each_testcase.split(':')
            for each_device in devices:
                temp_data_result, temp_data_value, path = self._search_and_retrieve_tc_data(
                    data, each_device, test_data, each_testcase)
                """
                    check that given testcase is available in common templates
                """
                if temp_data_result is None:
                    if self._check_generic_template(test_data[0]) is not False:
                        temp_var_data = copy.deepcopy(self.process_tmpl_data)
                        dummy_hash = {}
                        for x in range(0, len(temp_var_data)):
                            dummy_hash.update(temp_var_data[x])
                            data.extend([{'common_template': dummy_hash}])

                        temp_data_result, temp_data_value, path = self._search_and_retrieve_tc_data(data, each_device,
                                                                                                    test_data, each_testcase)

                """
                   If the test case if the format : <testcase>:parameters:parmeter1
                   and the parameter does not exist in the test data add it from user
                   provided params_dict.
                """
                if temp_data_result is None:
                    if "parameters" in each_testcase:
                        test_data = each_testcase.split(':')
                        parameter = test_data.pop()
                        temp_data_result, temp_data_value, path = self._search_and_retrieve_tc_data(
                            data, each_device, test_data, each_testcase)
                        if temp_data_result is not None:
                            if params_dict is not None:
                                temp_data_result = params_dict.get(
                                    parameter, None)
                                if temp_data_result is None:
                                    t.log(
                                        level="debug",
                                        message="Parameter data for " +
                                        parameter +
                                        " not provided in params_dict.")
                            else:
                                temp_data_result = {}
                """
                   If the test case if the format : <testcase>:parameters:parmeter1
                   and the parameter attribute itself does not exist in the test_data
                   add it first and add the prameter data from user provided params_dict.
                """
                if temp_data_result is None:
                    if "parameters" in each_testcase:
                        test_data = each_testcase.split(':')
                        parameter = test_data.pop()
                        parameters = test_data.pop()
                        temp_data_result, temp_data_value, path = self._search_and_retrieve_tc_data(
                            data, each_device, test_data, each_testcase)
                        if temp_data_result is not None:
                            if params_dict is not None:
                                temp_data_result = params_dict.get(
                                    parameter, None)
                                if temp_data_result is None:
                                    t.log(
                                        level="debug",
                                        message="Parameter data for " +
                                        parameter +
                                        " not provided in params_dict.")
                            else:
                                temp_data_result = {}

                test_data = each_testcase.split(':')
                """
                   The specific test case data will be stored in temp_data_result, the higher
                   hierarchial level yaml test data will be stored in temp_data_value and
                   will be merged at the end.
                """
                if temp_data_result is not None:
                    _params_dict = dict()
                    temp_data = copy.deepcopy(temp_data_result)
                    if _parameters is not None:
                        if isinstance(_parameters, str):
                            if val is not None:
                                _params_dict['value'] = val
                            if opr is not None:
                                _params_dict['operator'] = opr
                        elif isinstance(_parameters, list):
                            for each_param_dict in _parameters:
                                param_name = each_param_dict.get('name', None)
                                if param_name is not None:
                                    param_name = each_param_dict.pop('name')
                                    temp_param_dict = copy.deepcopy(each_param_dict)
                                    _params_dict.update(
                                        {param_name: temp_param_dict})
                                    each_param_dict['name'] = param_name

                    if _parameters is None and val is not None:
                        temp_data.update({'value': val})
                    if _parameters is None and opr is not None:
                        temp_data.update({'operator': opr})
                    if add_data is not None:
                        temp_data.update(add_data)
                    for each in reversed(test_data):
                        temp_data = OrderedDict({each: temp_data})

                    #merge the parameters provided via the robot file.
                    if 'parameters' not in test_data and _params_dict:
                        if temp_data[test_data[0]].get('parameters', None):
                            verify_utils.merge_dicts(temp_data.get('parameters'), _params_dict)
                        else:
                            temp_data[test_data[0]].update({'parameters': _params_dict})
                    elif 'parameters' in test_data and _params_dict:
                        temp_parameter = {}
                        if test_data[2] in _params_dict.keys():
                            temp_parameter = {test_data[2]:_params_dict.get(test_data[2])}
                        if temp_parameter and temp_data[test_data[0]].get('parameters', None):
                            verify_utils.merge_dicts(temp_data[test_data[0]].get('parameters'), temp_parameter)
                        elif temp_parameter:
                            temp_data[test_data[0]].update({'parameters': temp_parameter})

                    # update execute_on only if user provide execute_on as part
                    # of input
                    if devices_arg is not None and len(execute_on) != 0:
                        temp_data[test_data[0]].update(
                            {'execute_on': execute_on})
                    if new_args is not None:
                        temp_data[test_data[0]].update(new_args)

                    # common_template
                    # parse command argument and added it on testcase data
                    if xpath_filter is not None:
                        temp_data[test_data[0]].update(
                            {'xpath_filter': xpath_filter})
                    if cmd is not None:
                        temp_data[test_data[0]].update({'cmd': cmd})

                    if iterator_data is not None:
                        temp_data[test_data[0]].update(
                            {'iterator': iterator_data})
                    if add_data is not None:
                        temp_data[test_data[0]].update(
                            add_data)
                    if is_get is not None:
                        temp_data[test_data[0]].update({'type': 'get'})
                        temp_data[test_data[0]].update(
                            {'return_type': 'value'})
                    temp_data = self._merge_template_data(
                        {path[-1]: temp_data_value}, temp_data[test_data[0]], test_data[0])
                    temp_data = OrderedDict(temp_data)
                    yaml_data[each_device] = verify_utils.merge_dicts(
                        yaml_data[each_device], OrderedDict({test_data[0]: temp_data}))
                else:
                    t.log(
                        level='error',
                        message='Testcase ' +
                        each_testcase +
                        ' not found for ' +
                        each_device)

        device_specific_tcs = []
        for each_device in devices:
            temp_dict = OrderedDict({each_device: yaml_data[each_device]})
            device_specific_tcs.append(temp_dict)

        specific_test_data = {'data': device_specific_tcs, 'args': global_args}

        if verify_parallel:
            return specific_test_data

        result = self.verify_all_checks_api(
            specific_test_data=specific_test_data,
            type=is_get,
            suppress_log=self.suppress_log,
            suppress_overlimit_log=self.suppress_overlimit_log,
            suppress_log_limit=self.suppress_log_limit,
            do_parallel=do_parallel,
            checks_robot_arg=checks_robot_arg)
        self._showdump = None

        if not result:
            fail_message = "Verify_Specific_Checks_API: failed testcase data."
            verify_utils.create_ve_debug_log(specific_test_data, fail_message)

        # Raise exeception if it is a robot call
        if kwargs.get('is_robot', False):
            '''
               print fail message if verify fails
               do not print fail message if type is get
            '''
            failmsg = kwargs.get('failmsg', self._default_failmsg)
            if isinstance(result, bool) and result is False and is_get is None:
                raise TobyException(failmsg)
        return result

    def verify_statement_checks(self, **kwargs):
        """
        Verify interval statement checks

        DESCRIPTION:
            Verify hello-interval is-equal 20 and dead-interval is-equal 80 using ospf_interface on
            device1 hello-interval is-equal 20 and interface-type is-equal BDR with args:intf as ae0.4
            and intf2 as 30 and iterate_utill:interval as 5 and iterate_utill:timeout as 30

        ARGUMENTS:
            [kwargs]
            :param STR stanzas :
                *OPTIONAL* testcase value and operator as a string. Default stanzas is EMPTY STR
            :param STR template:
                *OPTIONAL* tamplate name or testcase name under which the values will verify.
                           Default template is EMPTY STR
            :param OBJECT devices:
                *OPTIONAL* devices under which the stanza will verify.Default devices is EMPTY STR
            :param STR file :
                *OPTIONAL* file contain templates. Default file is EMPTY STR.

        ROBOT USAGE:
            ${status} =  verify statement checks   stanzas=${attsVals}       template=${tmpl}     devices=${router}

        :return: Final result True/False based on all verifications
        """
        # Used to setup environment variables
        self._setup()

        # initialise With value from the robot
        stanzas = kwargs.get('stanzas', "")
        template = kwargs.get('template', "")
        devices = kwargs.get('devices', "")
        verify_file = kwargs.get('file', None)

        # Default condition for every testcase.
        self.user_optimized = kwargs.get("optimize", False)
        # If direct argument is passed as a dict
        args_value = kwargs.get('args', None)

        # if both initialise and give file is None then return False
        if verify_file is None and self.verification_file is None:
            t.log(level="debug", message=" FILE NOT FOUND FOR VERIFICATION ")
            if kwargs.get('is_robot', None) is not None:
                raise TobyException("File Not found for verification")
            return False
        self.process_tmpl_data = []
        self.process_data = []
        self.process_pylib = []
        # If current file is None then take the initialized datas...
        if verify_file is None:
            verify_file = self.verification_file
            self.process_tmpl_data = copy.deepcopy(self.tmpl_data)
            self.process_pylib = copy.deepcopy(self.pylib)
            self.process_data = copy.deepcopy(self.ve_data)
            use_tmpl = self.tmpl_file
        else:
            # Multiple files to process
            verify_file = verify_file.split(',')
            for each_file in verify_file:
                pre_result = self._pre_process_testcases(
                    each_file)  # pre-process all the files
                if pre_result['result'] is False:
                    if kwargs.get('is_robot', None) is not None:
                        raise TobyException("Pre process testcase failed")
                    return False
                # Keep adding all the processed TCs to data
                self.process_data.extend(pre_result.get('data', list()))

                # get normal data from each file and update the
                # use_template,use_library and self.tmpl_data
                file_data = verify_utils.get_yaml_data_as_dict(
                    each_file, self.keywords, self.yaml_file_data)
                if file_data is False:
                    if kwargs.get('is_robot', None) is not None:
                        raise Exception("file data is false")
                    return False
                if isinstance(file_data, dict):
                    if 'verify' in file_data:
                        verify_file_data = file_data['verify']
                        self.process_tmpl_data.extend(
                            self._expand_file_list(
                                verify_file_data.get(
                                    'use_template', [])))
                        self.process_pylib.extend(
                            verify_file_data.get('use_library', list()))
                        self._source_templates(verify_file_data)
            use_tmpl = self.process_tmpl_file
        use_lib = copy.deepcopy(self.process_pylib)
        data = copy.deepcopy(self.process_data)

        # Update the handle
        if not self.t_handle:
            self.t_handle = t.t_dict['resources'].copy()
            self._make_ifd_tvar()
            # self.t_handle = t.t_dict.copy()

        # If data present in main data
        data = self._search_template(
            template, template_data=data)

        # if template not present in main data , search in template data
        if data is False:
            data = self._search_template(template)

        # if template not found in main data or in USE_template data return
        # false
        if data is False:
            t.log(level="debug", message="Template data not found")
            if kwargs.get('is_robot', None) is not None:
                raise Exception("Template data not found")
            return False

        # store the template data in another variable for future merging.
        temp_data = data

        data = data[template]
        #t_data_format = data.get('format', 'xml')

        # create sample to append the values
        tmp_data_file = {
            "VERIFY": {
                "use_template": use_tmpl,
                "use_library": use_lib,
                devices: {
                    template: {
                    }
                }
            }
        }
        #interface_value = str()

        # If {} is passed ,take the dict directly or go for args parsing

        new_args = {'args': []}
        if args_value is not None:
            new_args = args_value

        arg_tmp = stanzas.split(' with ')
        if len(arg_tmp) == 1:
            arg_tmp = arg_tmp[0].split(' at ')
        if len(arg_tmp) == 1:
            arg_tmp = arg_tmp[0].split(' on ')

        # if with/at/on present
        if len(arg_tmp) > 1:

            # For multiple argument
            arg_values = arg_tmp[1].split(' and ')
            # new_args = {'args': []}
            for each_args in arg_values:

                # for each argument decide key or value e.g. args:intf as ae0.4
                # and intf2 as 30
                new_value_key = each_args.split(' as ')
                # try:
                #    temp_new_value_key = eval(new_value_key[1])
                # except:
                #    temp_new_value_key = new_value_key[1]

                if ':' in new_value_key[0]:
                    tmp_value = new_value_key[0].split(':')
                    # IF args is present , then push into the argument
                    if tmp_value[0].lower() == 'args':
                        new_args['args'].append(
                            {tmp_value[1]: new_value_key[1]})
                    else:
                        # IF args not present,  Merge at the first level
                        if tmp_value[0] not in list(new_args.keys()):
                            new_args.update({tmp_value[0]: {}})

                        new_args[tmp_value[0]].update(
                            {tmp_value[1]: new_value_key[1]})
                else:
                    # IF no ':' is present the put it Under the ARGS
                    new_args['args'].append(
                        {new_value_key[0]: new_value_key[1]})

        # split of small testcases e.g. hello-interval is-equal 20 and ...
        tc_data = {}
        total_testcases = arg_tmp[0].split(' and ')
        for each_tc in range(0, len(total_testcases)):
            val_op = total_testcases[each_tc].split(' ')
            if len(val_op) < 3:
                t.log(level='info', message=total_testcases[each_tc] + " is not in correct format")
                continue
            # temp_val=""
            try:
                    # if isinstance(' '.join(val_op[2:]),str):
                    # eval(' '.join(val_op[2:]))
                if isinstance(eval(' '.join(val_op[2:])), dict) or isinstance(
                        eval(' '.join(val_op[2:])), list):
                    temp_val = eval(' '.join(val_op[2:]))
                else:
                    temp_val = ' '.join(val_op[2:])

            except BaseException:
                temp_val = ' '.join(val_op[2:])

            testcase = {"operator": val_op[1], "value": temp_val}
            tc_data = tmp_data_file['VERIFY']
            tc_data = tc_data[devices]

            # Find the TC(e.g. hello-interval) in the main data
            path = verify_utils.find_key(temp_data, val_op[0])
            if path is None:
                t.log(level="debug", message="Unable to find " + val_op[0])
                if kwargs.get('is_robot', None) is not None:
                    raise Exception("Unable to find " + val_op[0])
                return False
            temp_dict = dict(testcase)

            # reversely form the data from path of the TC
            for each_element in reversed(path):
                temp_dict = {each_element: temp_dict}
            tc_data = verify_utils.merge_dicts(tc_data, temp_dict)

        t.log(level="DEBUG", message="Given data is :")
        t.log(level="DEBUG", message=tc_data)
        # Update the value in main testcase
        tmp_data_file['VERIFY'][devices].update(tc_data)

        # if argument(args) present in the file then Update in data
        if len(new_args['args']) > 0:
            tmp_data_file['VERIFY'][devices][template].update(new_args)

        # Still we need the cmd,xpath and other things.... for Will do a
        # template merge
        tmp_data_file['VERIFY'][devices][template] = self._merge_template_data(
            temp_data, tmp_data_file['VERIFY'][devices][template], template)
        t.log(level="DEBUG", message="Final data to process :")
        t.log(level="DEBUG", message=tmp_data_file)

        #device_specific_tcs = []
        # for each_device in devices:
        #    temp_dict = OrderedDict({each_device: yaml_data[each_device]})
        #    device_specific_tcs.append(temp_dict)

        #specific_test_data = {'data': device_specific_tcs, 'args': global_args}

        # Data is Formed, so just dump the data into a file and process with
        # regular function
        with open(get_log_dir() + '/tmpdata.yaml', 'w') as outfile:
            ruamel.yaml.dump(tmp_data_file, outfile,
                             Dumper=ruamel.yaml.RoundTripDumper)

        result = self.verify_all_checks_api(
            file=get_log_dir() + "/tmpdata.yaml")
        if isinstance(
                result,
                bool) and result is False and kwargs.get(
                    'is_robot',
                    None) is not None:
            raise Exception("checks failed")

        return result

    def _jvision_records_slicer(self, records, obtained_value):
        '''Slices the records of the form (.+):(.+), there are three possible
           scenarios :
             - records pattern : (.+):(.+) Example : '1:-1'
             - records pattern : (.+):     Example : '1:'
             - records pattern : :(.+)     Example : ':-1'
        '''
        if obtained_value == [] or obtained_value is None:
            return obtained_value
        records = str(records)
        if ':' in records:
            if re.match('(.+):(.+)', records) is not None:
                records = records.split(':')
                start = int(records[0])
                end = int(records[1])
                obtained_value = obtained_value[start:end]
            elif re.match(':(.+)', records) is not None:
                records = records.split(':')
                end = int(records[1])
                obtained_value = obtained_value[:end]
            elif re.match('(.+):', records):
                records = records.split(':')
                start = int(records[0])
                obtained_value = obtained_value[start:]
            else:
                t.log(
                    level="debug",
                    message="Invalid records pattern found, please check your records keyword.")
        else:
            obtained_value = obtained_value[int(records)]
        return obtained_value

    def _sub_merge_args_list(self, prior_args=[], non_prior_args=[]):
        # if prior_args is None or non_prior_args is None:
        # omkar    t.log(level="error", message="Arguments missing.")
        prior_keys = []
        prior_args = copy.deepcopy(prior_args)
        non_prior_args = copy.deepcopy(non_prior_args)
        for index in range(0, len(prior_args)):
            prior_keys.extend(prior_args[index].keys())
        for index in range(0, len(non_prior_args)):
            keys = list(non_prior_args[index].keys())
            key = keys[0]
            if key not in prior_keys:
                prior_args.append(non_prior_args[index])
        return prior_args

    def _merge_args_list(self, local_args=[], global_args=[], cli_args=[]):
        # if local_args is None or global_args is None or cli_args is None:
        # omkar    t.log(level="error", message="Arguments missing.")
        local_args = copy.deepcopy(local_args)
        global_args = copy.deepcopy(global_args)
        cli_args = copy.deepcopy(cli_args)
        if local_args == [] and global_args == [] and cli_args == []:
            return []
        else:
            local_args = self._sub_merge_args_list(cli_args, local_args)
            return self._sub_merge_args_list(local_args, global_args)

    def _specific_jvision_records_fetcher(
            self,
            jvision_records,
            verify_data,
            attribute=None,
            slicer=False):
        """
        Matches the jkey of the test case to the jkey of the records and
        fetch the attribute values. The attribute is retrieved from the
        verify file. The retrieved attribute value are stored in list obtined_value.
        """
        jkey_dict = OrderedDict()
        record_found = False
        filtered_records = []
        slice_value = verify_data.get('records', 'all')
        verify_jkey_regexp = None

        key_id = verify_data.get('key_id', 'jkey')
        verify_jkey = verify_data.get('key_value', None)
        if verify_jkey is None:
            verify_jkey = verify_data.get('jkey', None)
        if verify_jkey is None:
            verify_jkey_regexp = verify_data.get('key_pattern', None)
            if verify_jkey_regexp is None:
                verify_jkey_regexp = verify_data.get('jkey_pattern', None)

        for each_jvision_record in jvision_records:
            jvision_record_jkey = each_jvision_record.get(key_id, None)
            if jvision_record_jkey is None:
                continue
            match = None
            if verify_jkey is not None:
                match = re.match("".join((re.escape(verify_jkey), "$")), jvision_record_jkey)
            elif verify_jkey_regexp is not None:
                match = re.match(verify_jkey_regexp, jvision_record_jkey)
            elif slicer is not False:
                match = re.match(
                    re.escape(jvision_record_jkey),
                    jvision_record_jkey)
            else:
                t.log(
                    level="debug",
                    message="Either jkey or jkey_pattern keyword is mandaroty.")
            if match is not None:
                record_found = True
                match_jkey = match.group(0)
                temp = jkey_dict.get(match_jkey, None)
                if temp is None:
                    jkey_dict.update({match_jkey: []})
                if attribute is not None:
                    temp_obtained_value = each_jvision_record[attribute]
                    temp_obtained_value = str(temp_obtained_value)
                    jkey_dict[match_jkey].append(temp_obtained_value)
                else:
                    jkey_dict[match_jkey].append(each_jvision_record)

        if record_found is False:
            if verify_jkey is not None:
                t.log(
                    level="info",
                    message="No matching records found for the jkey : " +
                    str(verify_jkey))
            elif verify_jkey_regexp is not None:
                t.log(
                    level="info",
                    message="No matching records found for the jkey_pattern : " +
                    str(verify_jkey_regexp))
        if attribute is not None:
            return jkey_dict
        else:
            if slicer is False or str(slice_value) == 'all':
                for each_jkey in jkey_dict.keys():
                    filtered_records.extend(jkey_dict[each_jkey])
                return filtered_records
            else:
                for each_jkey in jkey_dict.keys():
                    sliced_records = self._jvision_records_slicer(
                        slice_value, jkey_dict[each_jkey])
                    if isinstance(sliced_records, list):
                        filtered_records.extend(sliced_records)
                    else:
                        filtered_records.append(sliced_records)
                return filtered_records

    def verify_jvision_records_api(self, **kwargs):
        """ Verifies Jvision records for jkey_pattern.

        ARGUMENTS:
            :param STR jvision_file:
                *MANDATORY* jvision_file name.Default is set to None.
            :param STR verify_file:
                *OPTIONAL* verify_file name.Default is set to None.
            :param STR jvision_data:
                *OPTIONAL* jvision data name to get verified. Default is set to None.
            :param STR is_key_specific:
                *OPTIONAL* key name to get verified.Default is set to None.
            :param STR is_get:
                *OPTIONAL* verify the mentioned jkey.Default is set to None.
            :param STR verify_string_data:
                *OPTIONAL* verify the specific data.Default is set to None.

        ROBOT USAGE:
             ${status} =  verify jvision records api    &{kwargs}

        :return:returns the JVISION RECORD API else raise an exception.
        """
        self._setup()

        jvision_file = kwargs.get('jvision_file', None)
        verify_file = kwargs.get('verify_file', None)
        verify_string_data = kwargs.get('verify_data', None)
        jvision_data = kwargs.get('jvision_data', None)
        is_key_specific = kwargs.get('key_specific', True)
        is_get = kwargs.get('is_get', None)
        return_value = {}
        jvision_records = {}

        if jvision_file is not None:
            with open(jvision_file, "r") as json_handle:
                try:
                    jvision_records = json.load(json_handle)
                except ValueError as error:
                    t.log(
                        level="error",
                        message="Error while reading the jvision data.")
                    t.log(level="error", message=str(error))
                    raise error
        elif jvision_data is not None:
            try:
                jvision_records = json.loads(jvision_data)
            except ValueError as error:
                t.log(
                    level="error",
                    message="Error while reading the jvision data.")
                t.log(level="error", message=str(error))
                raise error
        else:
            t.log(
                level='error',
                message='jvision data file or jvision data string is  mandatory.')
            return False

        verify_data = None
        if verify_file is not None:
            verify_data = verify_utils.get_yaml_data_as_dict(
                verify_file, self.keywords)
            verify_data = verify_data.get('verify_jvision', None)
        elif verify_string_data is not None:
            src_path = get_log_dir()
            verify_data_file = os.path.join(src_path, 'userdata.yaml')
            with open(verify_data_file, 'w') as outfile:
                outfile.write(verify_string_data)
            outfile.close()
            verify_data = verify_utils.get_yaml_data_as_dict(
                verify_data_file, self.keywords)
        else:
            t.log(
                level='error',
                message='verify data or verify file is mandatory.')
            return False

        attr_constraint = None
        result = True
        is_glob_args_list = False
        # Supporting non-default value in global arguments
        # Example : [k1, {k2:v2}, k3]
        glob_args = verify_data.get("args", [])
        if glob_args != []:
            verify_data.pop("args", glob_args)
            for index in range(0, len(glob_args)):
                if not isinstance(glob_args[index], dict):
                    glob_args[index] = {glob_args[index]: None}

        # Supporting all formats of command line argument inputs from robot.
        # Example : {args:[{k1:v1}, {k2:v2}]}, [{k1:v1},{k2:v2}] and {k1:v1,
        # k2:v2}
        stanza = kwargs.get("args", [])
        new_args = []
        if isinstance(stanza, dict):
            if len(stanza.keys()) == 1 and list(stanza.keys())[0] == 'args':
                new_args = stanza
            else:
                new_args = {'args': []}
                for key, value in stanza.items():
                    new_args['args'].append({key: value})
        elif isinstance(stanza, list):
            new_args = {'args': stanza}
        cli_args = new_args['args']

        for tc_name in verify_data.keys():
            attr_constraint = None
            args = verify_data[tc_name].get('args', [])
            # temp_local_args = []
            # Supporting non-default value in global arguments
            # Example : [k1, {k2:v2}, k3]
            for index in range(0, len(args)):
                if not isinstance(args[index], dict):
                    args[index] = {args[index]: None}
            if isinstance(args, list):
                if is_glob_args_list is True and isinstance(cli_args, list):
                    t.log(
                        level="error",
                        message="No default values found for global, local and command line args.")

            args = self._merge_args_list(
                local_args=args,
                global_args=glob_args,
                cli_args=cli_args)
            t.log(
                level="debug",
                message="Arguments after merging local global and command line arguments : " +
                str(args))
            if "None" in str(args):
                t.log(
                    level="debug",
                    message="Some of the values in args are None, please check.")
            self._substitute_variables(verify_data[tc_name], args)
            attribute = verify_data[tc_name].get('attribute', 'jvalue')
            regexp_result = re.search(r'(.*)\[(.*)\]', attribute)
            if regexp_result is not None:
                attribute = regexp_result.group(1)
                attr_constraint = regexp_result.group(2)
            expected_value = verify_data[tc_name].get('value', None)
            operator = verify_data[tc_name].get('operator', None)
            if operator is None:
                t.log(
                    level="error",
                    message="Operator not found for testcase: " +
                    str(tc_name))
                result = False

            records = verify_data[tc_name].get('records', 'all')
            # key_id = verify_data[tc_name].get('key_id', 'jkey')

            verify_jkey = verify_data[tc_name].get('key_value', None)
            if verify_jkey is None:
                verify_jkey = verify_data[tc_name].get('jkey', None)

            verify_jkey_regexp = verify_data[tc_name].get('key_pattern', None)
            if verify_jkey_regexp is None:
                verify_jkey_regexp = verify_data[tc_name].get(
                    'jkey_pattern', None)

            obtained_dict = self._specific_jvision_records_fetcher(
                jvision_records, verify_data[tc_name], attribute)
            if is_get is None:
                if obtained_dict == {}:
                    if operator.lower() == 'not-exists':
                        if verify_jkey is not None:
                            obtained_dict = {verify_jkey: None}
                        else:
                            obtained_dict = {verify_jkey_regexp: None}
                    elif obtained_dict == {}:
                        if verify_jkey is not None:
                            t.log(
                                level="error",
                                message="No matching records found for the jkey : " +
                                str(verify_jkey))
                        elif verify_jkey_regexp is not None:
                            t.log(
                                level="error",
                                message="No matching records found for the jkey_pattern : " +
                                str(verify_jkey_regexp))
                        result = False
                # check verification to be done based on key specific values
                if is_key_specific is True:
                    for jkey, obtained_value in obtained_dict.items():
                        if records != "all":
                            obtained_value = self._jvision_records_slicer(
                                records, obtained_value)
                        temp_result = self._evaluate(
                            expect_value=expected_value,
                            obtained_value=obtained_value,
                            opr=operator,
                            atr_constraint=attr_constraint)
                        self._put_verify_log(
                            testcase=tc_name + ":" + jkey,
                            expect=expected_value,
                            obtain=obtained_value,
                            opr=operator,
                            result=temp_result)
                        result = temp_result & result
                # else verification to be done across different key values (
                # not key speific values )
                else:
                    obtained_value = []
                    for jkey, ob_value in obtained_dict.items():
                        obtained_value.extend(ob_value)
                    if records != "all":
                        obtained_value = self._jvision_records_slicer(
                            records, obtained_value)
                    temp_result = self._evaluate(
                        expect_value=expected_value,
                        obtained_value=obtained_value,
                        opr=operator,
                        atr_constraint=attr_constraint)
                    self._put_verify_log(
                        testcase=tc_name,
                        expect=expected_value,
                        obtain=obtained_value,
                        opr=operator,
                        result=temp_result)
                    result = temp_result & result

            if is_get is not None:
                return_value.update({tc_name: {}})
                for jkey, obtained_value in obtained_dict.items():
                    if records != "all":
                        obtained_value = self._jvision_records_slicer(
                            records, obtained_value)
                    return_value[tc_name].update({jkey: obtained_value})
        if is_get is not None:
            return verify_utils.extract_data(
                return_value, kwargs.get(
                    'return_type', 'value'))
        return result

    def verify_specific_jvision_records_api(self, **kwargs):
        """
        Verifies Jvision records for specific jkey_pattern.

        ARGUMENTS:
            [kwargs]
            :param STR jvision_file:
                *MANDATORY/OPTIONAL* Not MANDATORY if jvision_data is present.jvision_file name.
                                    Default is set to None.
            :param STR verify_file:
                *OPTIONAL* verify_file name.Default is set to None.
            :param STR jvision_data:
                *MANDATORY/OPTIONAL* Not MANDATORY if jvision_file is present.jvision data name to get verified.
                                    Default is set to None.
            :param STR is_key_specific:
                *OPTIONAL* key name to get verified.Default is set to None.
            :param STR is_get:
                *OPTIONAL* verify the mentioned jkey.Default is set to None.
            :param STR verify_string_data:
                *OPTIONAL* verify the specific data.Default is set to None.

        ROBOT USAGE:
            ${status} =  verify specific jvision records api    &{kwargs}

        :return:return jvision recors or raises an exception
        """

        #Used to setup environment variables
        
        self._setup()
        jvision_file = kwargs.get('jvision_file', None)
        jvision_data = kwargs.get('jvision_data', None)
        verify_file = kwargs.get('verify_file', None)
        is_get = kwargs.get('is_get', None)
        verify_string_data = kwargs.get('verify_data', None)
        is_key_specific = kwargs.get('key_specific', True)

        if jvision_file is None and jvision_data is None:
            t.log(
                level='error',
                message='jvision file or jvision data is mandatory.')
            return False

        value = kwargs.get('value', None)
        operator = kwargs.get('operator', None)
        attribute = kwargs.get('attribute', None)
        records = kwargs.get('records', None)
        specific_tc = kwargs.get('checks', None)
        if specific_tc is None:
            t.log(
                level="error",
                message="Checks are mandatory but none provided.")
            return False

        specific_tcs = specific_tc.split(",")

        verify_data = None
        if verify_file is not None:
            verify_data = verify_utils.get_yaml_data_as_dict(
                verify_file, self.keywords)
            verify_data = verify_data.get('verify_jvision', None)
        elif verify_string_data is not None:
            src_path = get_log_dir()
            verify_data_file = os.path.join(src_path, 'userdata.yaml')
            with open(verify_data_file, 'w') as outfile:
                outfile.write(verify_string_data)
            outfile.close()
            verify_data = verify_utils.get_yaml_data_as_dict(
                verify_data_file, self.keywords)
        else:
            t.log(
                level='error',
                message='verify data or verify file is mandatory.')
            return False

        cli_args = kwargs.get('args', [])

        temp_tc_dict = dict()
        for tc_name in specific_tcs:
            tc_data = verify_data.get(tc_name, None)
            if tc_data is None:
                t.log(level="error", message="Testcase : " + tc_name +
                      " not found. Please check your verify yaml file.")
                return False
            else:
                if value is not None:
                    tc_data.update({"value": value})
                if operator is not None:
                    tc_data.update({"operator": operator})
                if attribute is not None:
                    tc_data.update({"attribute": attribute})
                if records is not None:
                    tc_data.update({"records": records})
                temp_tc_dict[tc_name] = tc_data

        global_args = verify_data.get('args', None)
        if global_args is not None:
            temp_tc_dict['args'] = global_args
        verify_yaml_data = dict()
        verify_yaml_data["verify_jvision"] = temp_tc_dict
        tmp_data_file = get_log_dir() + '/tmp_jvision_data.yaml'
        with open(tmp_data_file, 'w') as outfile:
            ruamel.yaml.dump(verify_yaml_data, outfile,
                             Dumper=ruamel.yaml.RoundTripDumper)
        return self.verify_jvision_records_api(
            verify_file=tmp_data_file,
            jvision_file=jvision_file,
            jvision_data=jvision_data,
            args=cli_args,
            is_get=is_get,
            key_specific=is_key_specific)

    def get_specific_data(self, **kwargs):
        """
        Get specified data.

        ARGUMENTS:
            [kwargs]
            :param STR type:
                *OPTIONAL* type to get update.default is set to "get".

        ROBOT USAGE:
            ${status} =     get specific data         &{kwargs}

        :return:None
        """
        self._setup()
        kwargs.update({'type': 'get'})
        return_value = self.verify_specific_checks_api(**kwargs)
        t.log(level="info", message="GET DATA RESULT: "+str(return_value))
        return verify_utils.extract_data(
            return_value, kwargs.get(
                'return_type', 'value'))

    def verify_dict(self, **kwargs):
        """
        Verify Dict Format.

        ARGUMENTS:
            [kwargs]
            :param DICT input_dict:
                *MANDATORY* dict type.

        ROBOT USAGE:
            ${status} =  verify dict     input_dict=${dict_input}

        """
        dict_input = kwargs.get('input_dict', None)
        if isinstance(dict_input, dict) is not True:
            t.log(level="info", message="Given Input is Not in dict format")
            return False
        try:
            with open(get_log_dir() + '/tmpdata.yaml', 'w') as outfile:
                dump(dict_input, outfile, default_flow_style=True)
        except Exception as exc:
            t.log(level="error", message=exc)
            t.log(level="error", message="\n Unable to write in file")
            raise exc
        return self.verify_all_checks_api(file=get_log_dir() + "/tmpdata.yaml")

    def jvision_to_ve_converter(
            self,
            json_file,
            mapping_file,
            record_filter={}):
        """
        Converting Jvison to VE.

        ARGUMENTS:
            [json_file,mapping_file,record_filter={}]
            :param STR json_file:
                *MANDATORY* Will hold the json data.
            :param STR mapping_file:
                *MANDATORY* Will hold the mapping defined by user.
            :param DICT record_filter:
                *MANDATORY* record filters in dict form.

        ROBOT USAGE:
            ${status} =  jvision to ve converter  &{kwargs}

        :return:return restult else False.
        """
        # Will hold the json data.
        # data = []
        # Will hold the mapping defined by user.
        # mapping = []
        record_filter_dict = copy.deepcopy(record_filter)
        if verifyEngine._is_file_exists(json_file):
            with open(json_file, "r") as json_handle:
                try:
                    data = json.load(json_handle)
                except BaseException:
                    t.log(level='error', message="Invalid json in file "
                          + json_file)
                    return False
        else:
            return False

        if os.path.exists(mapping_file):
            with open(mapping_file, "r") as mapping_handle:
                try:
                    mapping = load(mapping_handle)
                    mapping = mapping.get('mapping_db', None)
                except:
                    t.log(level='error', message="Invalid yaml in file "
                          + mapping_file)
                    return False
        elif os.path.exists(os.path.join(self._suite_source_path, mapping_file)):
            mapping_file = os.path.join(self._suite_source_path, mapping_file)
            with open(mapping_file, "r") as mapping_handle:
                try:
                    mapping = load(mapping_handle)
                    mapping = mapping.get('mapping_db', None)
                except:
                    t.log(level='error', message="Invalid yaml in file "
                          + mapping_file)
                    return False
        else:
            t.log(level='error', message="Error: Input file " + mapping_file +
                  " not found.\n")
            return False

        # Sorting the data via jkey to avoid same command execution.
        if not data:
            t.log(
                level='error',
                message="json file " +
                json_file +
                " does NOT contain any records")
            return False
        data = sorted(data, key=lambda k: k['jkey'])
        return_result = []
        if len(record_filter_dict.keys()) != 0:
            data_raw = copy.deepcopy(data)
            data = self._specific_jvision_records_fetcher(
                data_raw, record_filter_dict, attribute=None, slicer=True)
            if not data:
                t.log(
                    level='error',
                    message="NO Records matched with given 'record_filter' value")
                return False

        for each_jvision_data in data:
            mapping_found = False
            for each_mapping_entry in mapping:
                match = re.search(
                    each_mapping_entry['jkey'],
                    each_jvision_data['jkey'])
                if match:
                    t.log(level='info', message="MATCH Found for JVISION RECORD:")
                    t.log(level='info', message=each_jvision_data)
                    t.log(level='info', message="Corresponding MAPPING ENTRY:")
                    t.log(level='info', message=each_mapping_entry)
                    mapping_found = True
                    sys_name = each_jvision_data.get("system_id", None)
                    logical_name = verifyEngine._get_logical_name(sys_name)

                    # to execute pre-requisite
                    pre_req = copy.deepcopy(
                        each_mapping_entry.get("PREQ", None))
                    if pre_req is not None:

                        t.log(level='info', message="PREQ is exists")
                        for each_req in pre_req:
                            pre_req_args = copy.deepcopy(
                                pre_req[each_req].get("VE_ARGS", None))
                            if pre_req_args is not None:
                                for each_pre_req_arg_index in range(
                                        len(pre_req_args)):
                                    arg_dict = pre_req_args[each_pre_req_arg_index]
                                    if re.search(
                                            r'match.group', arg_dict[list(arg_dict.keys())[0]]):
                                        arg_dict[list(arg_dict.keys())[0]] = eval(
                                            arg_dict[list(arg_dict.keys())[0]])
                            pre_res_data_value = self.get_specific_data(
                                info=pre_req[each_req].get(
                                    "VE_TEMPLATE", None), devices=logical_name, file=pre_req[
                                        each_req].get("VE_TEMPLATE_FILE", None), args=pre_req_args)
                            t.log(
                                level='debug',
                                message="value for" +
                                each_req +
                                " : ")
                            t.log(level='debug', message=pre_res_data_value)
                            exec(each_req + "=pre_res_data_value")

                    jvision_args = copy.deepcopy(
                        each_mapping_entry.get("VE_ARGS", None))
                    if jvision_args is not None:
                        for jvision_arg_index in range(len(jvision_args)):
                            jvision_dict = jvision_args[jvision_arg_index]
                            if re.search(r'match.group',
                                         jvision_dict[list(jvision_dict.keys())[0]]):
                                jvision_dict[list(jvision_dict.keys())[0]] = eval(
                                    jvision_dict[list(jvision_dict.keys())[0]])
                            if re.search(
                                    r'PREQ\[(.*)\]', jvision_dict[list(jvision_dict.keys())[0]]):
                                preq_var_name = re.sub(
                                    r'PREQ\[\'(.*)\'\]', "\\1", jvision_dict[list(
                                        jvision_dict.keys())[0]])
                                jvision_dict[list(jvision_dict.keys())[
                                    0]] = eval(preq_var_name)

                    return_result.append(
                        self.verify_specific_checks_api(
                            checks=each_mapping_entry.get("VE_TEMPLATE", None),
                            devices=logical_name,
                            file=each_mapping_entry.get(
                                "VE_TEMPLATE_FILE", None),
                            args=jvision_args, value=each_jvision_data.get(
                                "jvalue", None),
                            optimize=True))
            if mapping_found is False:
                t.log(
                    level='error',
                    message="jvision record key: " +
                    each_jvision_data['jkey'] +
                    " is NOT found in mapping file " +
                    mapping_file)
                return_result.append(False)

        return not(False in return_result)

    def _get_logical_name(system_name):
        devices_info = t.t_dict['resources'].copy()
        for each_device in devices_info:
            if devices_info[each_device]['system']['primary']['name'] == system_name:
                return each_device
        t.log(level='error', message="Error: Device " + str(system_name) +
              " not found in topology file.\n")

    def _is_file_exists(filename):
        if not os.path.exists(filename):
            t.log(level='error', message="Error: Input file " + str(filename) +
                  " not found.\n")
            return False
        return True

    def get_last_verify_result(self):
        """
        Helps user to directly call the test case name from robot file

        DESCRIPTION:
            1.verify ospf_interface_check on device1
            2.verify ospf_interface_check:check_interface_metric on device0

        ROBOT USAGE:
            ${result} =     get last verify result        &{kwargs}

        :return:None
        """
        return self._last_verify_result

    def _segregate_tc_data(self, tc_data):
        """
        It recursively splits the tc_data into different dictionaries based
        on the iterate TC and non-iterate TC.

        return_value: [list_of_dicts_with_iterator, dict_with_non_iterate_tc_data]
        """

        sub_tc_present = False

        parent_data = OrderedDict()
        iterate_data = []
        non_iterate_data = OrderedDict()
        iterate_result = []
        non_iterate_result = OrderedDict()

        tc_data_keys = tc_data.keys()

        # Termination condition for the recursion function.
        # Checking for the simplest lowest form of the testcase
        if 'value' in tc_data_keys or 'operator' in tc_data_keys:
            if 'iterate_for' in tc_data_keys or 'iterate_until' in tc_data_keys:
                iterate_data.append(tc_data)
            else:
                non_iterate_data = tc_data
            return [iterate_data, non_iterate_data]

        # Checking if the iterator is in the testcase level rather
        # than at the individual parameter level
        if 'iterate_for' in tc_data_keys or 'iterate_until' in tc_data_keys:
            iterate_data.append(tc_data)
            return [iterate_data, non_iterate_data]

        # Checking if there is a sub testcase present in the tc_data
        # Also storing the parent data in this level of recursion the
        # append the result from the next recursion level.
        for key in tc_data_keys:
            # check for sub testcase(s) present in each key
            if isinstance(tc_data[key], dict) and key not in self.VE_KEYS_WITH_VALUE_AS_DICT:
                sub_tc_present = True
            else:
                # save parent data if present
                parent_data[key] = copy.deepcopy(tc_data[key])

        if sub_tc_present:
            for key in tc_data_keys:
                # Recurse for the sub testcase
                if isinstance(tc_data[key], dict) and key not in self.VE_KEYS_WITH_VALUE_AS_DICT:
                    sub_tc_data = tc_data[key]
                    result = self._segregate_tc_data(sub_tc_data)
                    if result[0]:
                        if isinstance(result[0], list):
                            for each_tc in result[0]:
                                iterate_result.append({key: each_tc})
                    if result[1]:
                        non_iterate_result.update({key: result[1]})
                    if result[1] == {} and result[0] == []:
                        non_iterate_result.update({key: result[1]})

            # Append the result from the recursed function to the parent
            # data while checking if it is iterate or non-iterate data.
            if iterate_result:
                for each_tc in iterate_result:
                    temp_parent_data = copy.deepcopy(parent_data)
                    temp_parent_data.update(each_tc)
                    iterate_data.append(temp_parent_data)
            if non_iterate_result:
                non_iterate_data = copy.deepcopy(parent_data)
                non_iterate_data.update(non_iterate_result)
            return [iterate_data, non_iterate_data]
        else:
            # If there is no subtestcase present and there is not value or
            # operator in the keys return the data as it is depending on
            # the presence of the iterator in the data.
            if 'iterate_for' in tc_data_keys or 'iterate_until' in tc_data_keys:
                iterate_data.append(tc_data)
            else:
                non_iterate_data = tc_data
            return [iterate_data, non_iterate_data]

    def _iterator(self, *args, **kwargs):
        """
        It takes a function, fucntion arguments and iteration values as
        input and iterates the function till the conditions satisfied.
        """
        # get the function to be iterated and iteration values from kwargs
        func = kwargs.pop("function")
        iterate_type = kwargs.pop("iterate_type", None)
        expected_result = kwargs.pop("expected_return")
        tc_name = kwargs.get("tc_name")
        is_tc_type = kwargs.get("tc_data").get('type', None)
        cli_args = copy.deepcopy(kwargs.get("cli_args", []))
        global_args = copy.deepcopy(kwargs.get("global_args", []))

        # replace var and tv variables in the interval and timeout
        interval = kwargs.pop("interval", 1)
        timeout = kwargs.pop("timeout", 1)
        local_args = kwargs.get("tc_data").get("args", [])
        if local_args == [] and global_args == [] and cli_args == []:
            args = []
        else:
            t.log(
                level="debug",
                message="Args before merging with cli args and global args: " +
                str(local_args))
            t.log(level="debug", message="Global args : " + str(global_args))
            t.log(level="debug", message="Command Line args : " + str(cli_args))
            local_args = self._sub_merge_args_list(cli_args, local_args)
            args = self._sub_merge_args_list(local_args, global_args)
            t.log(level="debug", message="Args after merging : " + str(args))
        dummy_dict = {'interval': interval, 'timeout': timeout}
        t.log(level="debug",
              message="Interval and timeout values before Substitute : " + str(dummy_dict))
        self._substitute_variables(dummy_dict, args)
        t.log(level="debug",
              message="Interval and timeout values after Substitute : " + str(dummy_dict))
        interval = verify_utils.convert_str_to_num_or_bool(
            dummy_dict['interval'])
        timeout = verify_utils.convert_str_to_num_or_bool(
            dummy_dict['timeout'])

        function_return = None
        #opr = None
        convergence_result = False
        timestamp = self._get_monotonic_time()
        spend_time = 0
        prev_function_return = expected_result
        optimize_value = self.user_optimized

        is_iterate_until = False
        is_iterate_for = False
        iteration_count = 1
        if iterate_type == "iterate_until":
            is_iterate_until = True
        if iterate_type == "iterate_for":
            is_iterate_for = True

        while timeout >= spend_time:
            t.log(level="info", message="ITERATION NUMBER: "+str(iteration_count))
            # Call the function 'func' with the kwargs
            try:
                function_return = func(**kwargs)
            except Exception as err:  # omkar relook
                t.log(level='error', message="Exception occured"+str(err))
                raise
            if isinstance(function_return, bool):
                convergence_result, convergence_time = self._is_converge(
                    is_iterate_until, spend_time, timeout, function_return,
                    is_iterate_for, timestamp)
                t.log(level="debug", message="convergence_result: " +
                      str(convergence_result)+" convergence time: "+str(convergence_time))
                if convergence_result:
                    self._update_convergence(
                        convergence_time, is_tc_type, function_return, tc_name)

            # iterate until returns when it gets the expected value
            if is_iterate_until:
                if expected_result == "_ANY_DATA" or function_return == expected_result:
                    self.user_optimized = optimize_value
                    return function_return

            # iterate for continues till it gets the expected value
            if is_iterate_for:
                function_return = prev_function_return and function_return
                prev_function_return = function_return
            if timeout >= spend_time+interval:
                t.log(level="debug", message="Sleeping for: "+str(interval))
                time.sleep(interval)
            spend_time += interval
            if iteration_count == 1:
                self.user_optimized = False
            iteration_count += 1

        self.user_optimized = optimize_value
        if self.error_message:
            t.log(level="error", message=self.error_message)
        return function_return

    def _pop_iterator_data(self, tc_dict):
        """
        returns the keys and its values(if present) with the remaing dictionary data
        """
        parent_data = {}
        sub_tc_present = False

        if not isinstance(tc_dict, dict):
            return None, None
        tc_dict_keys = tc_dict.keys()

        # return the key:iterator_value and dictionary
        if "iterate_for" in tc_dict_keys:
            return {"iterate_for": tc_dict.pop("iterate_for")}, tc_dict

        if "iterate_until" in tc_dict_keys:
            return {"iterate_until": tc_dict.pop("iterate_until")}, tc_dict

        for key in tc_dict_keys:
            # check for sub testcase(s) present in each key
            if isinstance(tc_dict[key], dict) and key not in self.VE_KEYS_WITH_VALUE_AS_DICT:
                sub_tc_present = True
            else:
                # save parent data if present
                parent_data[key] = copy.deepcopy(tc_dict[key])

        if sub_tc_present:
            for key in tc_dict_keys:
                if isinstance(tc_dict[key], dict) and key not in self.VE_KEYS_WITH_VALUE_AS_DICT:
                    sub_dict = copy.deepcopy(tc_dict[key])
                    # recursive call for checking in nested dictionaries
                    iterator, dict_data = self._pop_iterator_data(sub_dict)
                    if iterator and dict_data:
                        parent_data.update({key: dict_data})
                    return iterator, parent_data

    def _check_generic_template(self, template_name):
        """
         Sources the common template file based on template_name and returns template data if it exists in that file
         otherwise returns false
        """
        match = re.match(r'j_check_([^_]+)', template_name)
        if match is None:
            t.log(level='debug', message='Given template name  is not a common template')
            return False
        t.log(level='debug', message='Generic Template Sub Folder Name: ' +
              str(match.group(1)))
        template_file_name = template_name.strip()+'.yaml'
        template_file_name_with_path = os.path.join(os.path.dirname(
            VE_COMMON_TEMPLATES_PATH+str(match.group(1))+'/'), template_file_name)
        t.log(level='debug', message='Searching... Generic Template File: ' +
              template_file_name_with_path)
        if verifyEngine._is_file_exists(template_file_name_with_path):
            t.log(level='debug', message='Generic Template File: ' +
                  template_file_name_with_path + ' is FOUND')
            if template_file_name not in self._common_template_file_names_sourced:
                template_data = verify_utils.get_yaml_data_as_dict(
                    template_file_name_with_path, self.keywords, self.yaml_file_data)
                t.log(level='debug', message='Sourcing Generic Template file: ' +
                      template_file_name_with_path + ' into VE database')
                self._source_templates({}, file=template_data)
                self._common_template_file_names_sourced.extend(
                    template_file_name)
            return self._search_template(template_name)
        else:
            t.log(level='debug', message='common template file: ' +
                  template_file_name_with_path + ' is NOT FOUND')
            return False

    def _setup(self):
        """
           Check for 'fv-verify-templates-location' framework variable usage
           If used, update VE_COMMON_TEMPLATES_PATH accordingly.
        """
        global VE_COMMON_TEMPLATES_PATH
        global VE_COMMON_TEMPLATES_PATH_PRO
        try:
            if 'fv-verify-templates-location' in t.t_dict.get('framework_variables', dict()):
                if t.t_dict['framework_variables']['fv-verify-templates-location'].lower() == 'dev':
                    VE_COMMON_TEMPLATES_PATH = os.path.join(
                        VE_COMMON_TEMPLATES_PATH_PRO, 'dev/verify_templates/jnpr/')
                elif t.t_dict['framework_variables']['fv-verify-templates-location'].lower() == 'stage':
                    VE_COMMON_TEMPLATES_PATH = os.path.join(
                        VE_COMMON_TEMPLATES_PATH_PRO, 'stage/verify_templates/jnpr/')
                elif os.path.exists(t.t_dict['framework_variables']['fv-verify-templates-location']) and\
                     re.search(r'verify_templates\/jnpr\/?$', t.t_dict['framework_variables']['fv-verify-templates-location']):
                    VE_COMMON_TEMPLATES_PATH = os.path.join(
                        VE_COMMON_TEMPLATES_PATH_PRO, t.t_dict['framework_variables']['fv-verify-templates-location'])
                else:
                    VE_COMMON_TEMPLATES_PATH = os.path.join(
                        VE_COMMON_TEMPLATES_PATH_PRO, 'prod/verify_templates/jnpr/')
            else:
                VE_COMMON_TEMPLATES_PATH = os.path.join(
                    VE_COMMON_TEMPLATES_PATH_PRO, 'prod/verify_templates/jnpr/')
        except:
            VE_COMMON_TEMPLATES_PATH = os.path.join(
                VE_COMMON_TEMPLATES_PATH_PRO, 'prod/verify_templates/jnpr/')
        t.log(level='debug', message="VE GENERIC TEMPLATES PATH (if used): " +
              VE_COMMON_TEMPLATES_PATH)
