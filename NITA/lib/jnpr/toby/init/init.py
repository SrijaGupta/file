"""
    Initialization class and methods
"""

#import threading
import datetime
import os
import pwd
import re
import ruamel.yaml as yaml
import logging
import xml.dom.minidom as minidom
import platform
import time
import sys
import pprint
import pdb
import socket
from lxml import etree
from jnpr.toby.logger.logger import Logger
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.logger.logger import get_script_name
from jnpr.toby.hldcl.device import Device
from jnpr.toby.utils.utils import server_cpu_usage
from jnpr.toby.utils.utils import log_file_version, add_to_toby_exec
from jnpr.toby.utils.Vars import Vars
from jnpr.toby.utils.utils import run_multiple
from robotbackgroundlogger import BackgroundLogger

import jnpr.toby.frameworkDefaults.credentials as credentials
from collections import defaultdict
from jnpr.toby.exception.toby_exception import TobyException, TobyLinkFail,SpirentConnectError, SpirentLicenseError, TobySpirentLabserverConnectException, TobySpirentChassisConnectException, TobySpirentException,TobyIxiaException,TobyIxiaAppserverConnectException,TobyIxiaChassisConnectException
from jnpr.toby  import __version__ as toby_version
# pylint: disable=too-many-nested-blocks,no-else-raise,import-error,bad-indentation,unbalanced-tuple-unpacking,no-name-in-module 
try:
    import builtins
except ImportError:
    import builtin as builtins

ROBOT = True
try:
    from robot.libraries.BuiltIn import BuiltIn
    from robot.libraries.BuiltIn import _Misc
    import robot.api.logger as robot_logger
    BuiltIn().set_library_search_order('init')
except Exception:
    ROBOT = False


class init(object): # pylint: disable=invalid-name
    """
       Initialize class for Toby
    """
    t_dict = dict()
    tv_dict = dict()
    logger = None
    codecoverage_dict = dict()
    ft_codecoverage_dict = dict()
    core = defaultdict(lambda: defaultdict(dict))
    core_list = defaultdict(list)
    cores = {}

    def __init__(self, initialize_t=False):
        """
            Initialize class for Toby is the entry point class for Toby.
            Initialize will be the Keyword exposed to user to instantiate the object.
            Initialize keyword takes YML filename sent as command line argument and
            generates testbed info data 't' and also creates connection handles for each device.
            Initialize keyword  creates connection handles for Python HLDCL APIs
            It also takes cares for RT connections.
            Initialize class also initializes the logger object for Toby framework. Initialize
            class exposes set of APIs to interact with 't' var.
            Following code demonstrate the usage of Init library in robot testcase

                *** Settings ***
                Library init.py

                *** Test Cases ***
                SampleTest
                        Initialize
                        ${handle} =  Get handle   resource=device0
                        @{intf} =    Get Interface List      resource=device0
            The above robot test (lets say tobySample.robot) can be executed like following;

                #robot -V toby.yml tobySample.robot

        """
        if ROBOT:
            self.is_robot = True
        else:
            self.is_robot = False
        self._script_name = get_script_name()
        self._script_start_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S.%f")
        self._script_start_epoch_time = time.time()
        tzone, self._timezone = time.tzname
        self._log_dir = get_log_dir()
        self._stage = None

        self.background_logger = None

        if self.is_robot is True:
            self.logger = Logger(self._script_name, console=False)
        else:
            self.logger = Logger(self._script_name, console=True)

        if initialize_t:
            builtins.t = self
            
        self.console_log_flag = Vars().get_global_variable('${console_log}')
        self.robot_log_level = Vars().get_global_variable('${LOG_LEVEL}')
        if self.robot_log_level == "NONE": #This is to handle NONE passed from toby CLI Argument
            self.robot_log_level = 'ERROR'

        if self.robot_log_level == "TRACE": #This is to handle TRACE passed from toby CLI Argument
            self.robot_log_level = 'DEBUG'

    def toby_suite_setup(self, force=False):
        """
        A suite setup runs exactly once at the start of a suite

        DESCRIPTION:
            "Toby suite setup" is a master and mandatory keyword for any suite.
            This keyword will initialize device object
            for all the resources, and also will do the following based on
            framework variaables set to it in topology.yaml
                1.Loads base Line config
                2.checks for interfaces Status
                3.detect core on junos devices
                4.intialization code coverage
                5.intialization of Monitor engine
                6.intialization Macro engine
                7.check for device response

        ARGUMENTS:
            [force=False]
            :param BOOLEAN force:
                *OPTIONAL* If the initialization not done, call toby_initialize.
                             Default force is False

        ROBOT USAGE:
            *** Settings ***
            Suite Setup    Toby Suite Setup

        :return:None
        """
        # If the initialization not done, call toby_initialize
        self.log(level="INFO", message="Toby Suite Setup Started")
        self._toby_suite_setup_start = time.time()
        if force != True:
            if hasattr(builtins, 't'):
                self.log(level="WARN", message="Device connectivity already established. Skipping procedure to connect to devices...")
            else:
                self.toby_initialize()
        else:
            self.toby_initialize()
        if 'framework_variables' in self and self['framework_variables'] is not None and \
                'fv-epoch-pre-exec' in self['framework_variables']:
            self._script_start_epoch_time = float(self['framework_variables']['fv-epoch-pre-exec'])
        self._stage = "Toby Suite Setup"
        self._load_baseline_config()
        self.check_interface_status()
        self.detect_core_on_junos_device()
        self._code_coverage_init()
        self._monitoring_engine_init()
        self._macro_engine_init()
        self._device_response_check()
        self.log(level="INFO", message="Toby Suite Setup Completed")

    def toby_suite_teardown(self):
        """
        A suite teardown runs exactly once at the end of a suite.

        DESCRIPTION:
            "Toby suite teardown" is a recamondaded keyword for any suite.
            It is executed end of a suit.it is executed also when a test case fails,
            so it can be used for clean-up activities that must be done regardless of
            the test case status.

        ARGUMENTS:
            [ ]

        ROBOT USAGE:
            *** Settings ***
            Suite Teardown    Toby Suite Teardown

        :return:None
        """
        self.log(level="INFO", message="Toby Suite Teardown Started")
        self._check_and_reconnect()
        self._stage = "Toby Suite Teardown"
        self.detect_core_on_junos_device()
        self._reset_jpg_config()
        self._code_coverage_close()
        self._monitoring_engine_close()
        self.log(level="INFO", message="Toby Suite Teardown Completed")

    def toby_test_setup(self):
        """
        A test setup runs at the start of a test case.

        DESCRIPTION:
            If you define a test setup in the settings section of the suite,
            it will run at the start of each test in the suite (ie: if you have 5 tests,
            it will run five times). If you define it in a specific test, it will only run for
            that test where it is defined.

        ARGUMENTS:
            []

        ROBOT USAGE:
            *** Settings ***
            Test Setup    Toby test setup

        :return:None
        """
        self.log(level="INFO", message="Test case '" + BuiltIn().get_variable_value('${TEST_NAME}') + "' Started")
        self.log(level="INFO", message="Toby Test Setup Started")
        self._ft_code_coverage_data_initialize()
        junos_resources = self.get_junos_resources()
        self.log(level="DEBUG", message="Toby Test Setup is staged with : "+ str(junos_resources)+" resources")
        for resource in junos_resources:
            reconnect = False
            system = self.get_system(resource=resource)
            if 'fv-connect-controllers' in system['primary'] and \
                re.search('none', system['primary']['fv-connect-controllers'], re.I):
                self.log(level="DEBUG", message="Skipping Toby test setup for "+ str(resource)+ \
		" due to fv-connect-controller set to None")
                continue
            self.log(level="DEBUG", message="Toby Test Setup is going to held on : "+ str(resource))
            try:
                handle = self.get_handle(resource)
                prompt_status = handle.cli(command="\n")
            except Exception as err:
                t.log('WARN', 'Error ' + str(err) + ' found during prompt check. Issuing reconnect..')
                reconnect = True
            if reconnect:
                handle.reconnect(force=True)
            self.log(level="DEBUG", message="Necessary test setup has been done for "+ str(resource))

#        self.detect_core_on_junos_device()
        self.log(level="INFO", message="Toby Test Setup Completed")

    def _check_and_reconnect(self):

        code_coverage = True if hasattr(t, 'code_coverage') and t.code_coverage else False
        for resource in self.get_junos_resources():
            system = self.get_system(resource=resource)
            if ('core-check' in system['primary'] and system['primary']['core-check'] == 'enable') or code_coverage:
                if 'fv-connect-controllers' in system['primary'] and \
                    re.search('none', system['primary']['fv-connect-controllers'], re.I):
                    continue
                self.log(level="DEBUG", message="Teardown is checking for the reconnection "+str(resource.upper()))
                handle = self.get_handle(resource=resource)
                reconnect_status = handle.reconnect(force=False, all=True)
                if reconnect_status is False:
                    raise TobyException("Teardown is not able to recreate neccessary reconnection for "+resource)
        self.log(level="INFO", message="Neccessary Reconnections done")

    def toby_test_teardown(self):
        """
        It will run at the end of each test

        DESCRIPTION:
            If you define a test teardown in the settings section of the suite,
            it will run at the end of each test in the suite (ie: if you have 5 tests,
            it will run five times). If you define it in a specific test, it will only
            run for that test where it is defined.

        ARGUMENTS:
            []

        ROBOT USAGE:
            *** Settings ***
            Test teardown   Toby test teardown

        :return:None
        """
        self.log(level="INFO", message="Toby Test Teardown Started")
        self._check_and_reconnect()
        from jnpr.toby.engines.macro.cmd_macro import cmd_macro
        robot_variables = BuiltIn().get_variables()

        if BuiltIn().get_variable_value('${TEST_STATUS}') == 'FAIL' and '${macro_engine}' in robot_variables:
             cb_obj = cmd_macro()
             cb_obj.load_macros(macro_lib=robot_variables['${macro_lib}']) 
             cb_obj.run_macros(macros=robot_variables['${macro}'], targets=robot_variables.get('${macro_targets}', 'all'),resources=robot_variables.get('${macro_resources}', 'all'), message=robot_variables.get('${macro_message}', None))
             BuiltIn().set_suite_variable('${macro_already_run}', True)

        self.log(level="INFO", message="Toby Test Teardown '" + BuiltIn().get_variable_value('${TEST_NAME}') + "' Started")
        self.detect_core_on_junos_device()
        self.log(level="INFO", message="Toby Test Teardown Completed")
        self.log(level="INFO", message="Test case '" + BuiltIn().get_variable_value('${TEST_NAME}') + "' Completed")
        ## code coverage API needs be invoked at the end in teardown
        self._code_coverage_dump()


    def toby_initialize(self, init_file=None):
        """
        Toby initialize keyword, calls Initialize.

        ARGUMENTS:
            [init_file=None]

            :param STR init_file:
                *OPTIONAL*  Default init_file is None

        return:None
        """
        self.Initialize(init_file=init_file)

    def Initialize(self, init_file=None, force=False, osname_filter=None):
        """
        Initialize keyword creates testbed object ${t} from YAML file and creates connection handles for each device.

        DESCRIPTION:

            Toby framework initialize keyword
            Initialize keyword creates testbed object ${t} from YAML file and creates connection
            handles for each device.
            It also sets this t variable as global variable to be able to access across test suite.
            Usage in robot tstcase:

        ARGUMENTS:

            [init_file=None, force=False, osname_filter=None]

            :param STR init_file:
                *OPTIONAL*  Default init_file is None
            :param BOOLEAN force:
                *OPTIONAL*  Default force is False
            :param STR osname_filter:
                *OPTIONAL*  Default osname_filter is None


        ROBOT USAGE:

            *** Settings ***
            Library init.py

            *** Test Cases ***
            SampleTest
                    Initialize

        :return: None
    """
        # Avoid rerunning Initialize
        if force != True:
            if hasattr(builtins, 't'):
                self.log(level="WARN", message="Device connectivity already established. Skipping procedure to connect to devices...")
                return

        # Make t global at the beginning only to let HLDCL use for logging.
        builtins.t = self

        # Make tv global
        builtins.tv = self.tv_dict

        # User is calling Initialize(init_file=<some file>) directly from python
        if init_file is not None:
            try:
                list_config_input = init_file.split(":")
                init_data = yaml.safe_load(open(list_config_input[0]))
                log_file_version(list_config_input[0])
                if 't' not in init_data:
                    raise TobyException("No mandatory 't' object in file " + init_file)

                self.t_dict = init_data['t']
            except Exception as error:
                raise TobyException("Error loading file " + init_file + " :" + str(error))
            if len(list_config_input) > 1:
                list_config_input = list_config_input[1:]
                for input_file in list_config_input:
                    init_data = yaml.safe_load(open(input_file))
                    log_file_version(input_file)
                    if 't' in init_data:
                        self._merge_additional_resources(init_data['t'])
                        self._merge_fv_uv_yaml_content_in_t(init_data['t'])

        elif Vars().get_global_variable('${config}'):
            config_input = Vars().get_global_variable('${config}')
            list_config_input = config_input.split(":")
            init_data = yaml.safe_load(open(list_config_input[0]))
            if self.is_robot is True:
                log_file_version(list_config_input[0])
            if not init_data:
                raise TobyException("Topology file " + list_config_input[0] + " is either malformatted or empty")
            try:
                if 't' not in init_data:
                    raise TobyException("No mandatory 't' object in file " + list_config_input[0])
                self.t_dict = init_data['t']
            except Exception as error:
                raise TobyException("Error loading file " + list_config_input[0] + " :" + str(error))
            if len(list_config_input) > 1:
                list_config_input = list_config_input[1:]
                for input_file in list_config_input:
                    init_data = yaml.safe_load(open(input_file))
                    log_file_version(input_file)
                    if 't' in init_data:
                        self._merge_additional_resources(init_data['t'])
                        self._merge_fv_uv_yaml_content_in_t(init_data['t'])

        # User suplied '-V' option to point to variable file while calling toby/robot cmd line
        else:
            raise TobyException("No Input Params/Toby YAML File: Please use -p <Script_Params_Yaml>:<Additional_Yaml(if required)> to pass same.")

        #log server where Toby suite is running
        self.log(level="INFO", message="ROBOT VERSION :: " + BuiltIn().ROBOT_LIBRARY_VERSION)
        self.log(level="INFO", message="PYTHON VERSION :: " + str(" ".join(sys.version.split('\n'))))

        python_path = os.environ.get('PYTHONPATH', None)
        if python_path:
            self.log(level="INFO", message="########################################\n")
            self.log(level="INFO", message="    WARNING     WARNING     WARNING     \n")
            self.log(level="WARN", message="PYTHONPATH is set to :: " + str(python_path.split(os.pathsep)[0]) + "\n")
            self.log(level="WARN", message="    You are running non-production Toby libraries   \n")
            self.log(level="INFO", message="########################################")

        else:
            self.log(level="INFO", message="TOBY VERSION :: " + toby_version)
            if re.search(r'\-dev', toby_version):
                self.log(level="INFO", message="########################################\n")
                self.log(level="INFO", message="    WARNING     WARNING     WARNING     \n")
                self.log(level="WARN", message="    You are running a pre-production version of Toby  \n")
                self.log(level="INFO", message="########################################")
            else:
                self.log(level="INFO", message="PYTHONPATH is not set. Hence default production path")
        self.log_console("EXECUTION HOST :: " + socket.gethostname())
        self.log(level="INFO", message="EXECUTION HOST :: " + socket.gethostname() + " Process ID:: " + str(os.getpid()) +
                 " Parent Process ID:: " + str(os.getppid()))
        self.log(level="INFO", message="SCRIPT NAME :: " + self._script_name)
        self.log(level="INFO", message="LOG DIR :: " + self._log_dir)
        self.log(level="INFO", message="CURRENT WORKING DIR :: " + os.getcwd())

        #print CPU utilization information
        server_cpu_usage()

        self._validate_t_data()
        self._process_spirent_appserver()
        self._process_ixia_appserver()
        self._validate_and_handle_framework_variables()
        self._process_proxy_resource_aliases()
        self._print_topology_info()
        render_topology_success = False
        try:
            self._render_topology()
            render_topology_success = True
        except Exception as exp:
            self.log(level="DEBUG", message="Unable to create topology.png\n" + str(exp))

        if Vars().get_global_variable('${console_log}'):
            if Vars().get_global_variable('${console_log}') == 'enable':
                self.t_dict['console_log'] = True
            else:
                self.t_dict['console_log'] = False
        self.log_console("\nToby device initialization in progress...")
        try:
            resource_list_threaded = []
	    # list of resources to connect in parallel
            if self.t_dict['resources']:
                for resource_name in self.t_dict['resources']:
                    if osname_filter and self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() != osname_filter.upper():
                        continue
                    if self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper().startswith('IX') \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'SPIRENT' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'BREAKINGPOINT' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'UNIX' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'LINUX' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'PARAGON' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'CENTOS' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'FREEBSD' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'WINDOWS' \
                        or self.t_dict['resources'][resource_name]['system']['primary']['osname'].upper() == 'UBUNTU':
                        self._connect_device(resource=resource_name)
                    else:
                        resource_list_threaded.append({'fname': self._connect_device, 'kwargs': {'resource': resource_name}})
            if resource_list_threaded:
                run_multiple(resource_list_threaded)
        except KeyError:
            raise TobyException("'t' data not complete - missing critical information in t hierarchy1")
        self._print_topology_info(connect_success=True)
        self.__dict__.update(self.t_dict)
        Vars().set_global_variable("${t}", self.t_dict)
        Vars().set_global_variable("${tv}", self.tv_dict)
        pid_fh = open(self.logger.log_dir() + "/" + self._script_name + ".pid", 'w')
        pid_fh.write(str(os.getpid()))
        pid_fh.close()

        user = ''
        client_os = platform.system()
        if client_os == 'Windows':
            user = os.environ.get('USERNAME', '')
        else:
            user = pwd.getpwuid(os.getuid()).pw_name

        #  print log information
        if self.is_robot and os.path.isdir('/homes/' + user + '/public_html'):
            #  must take tzname as tuple despite not needing timezone_daylight
            timezone, timezone_daylight = time.tzname # pylint: disable=unused-variable
            web_prefix = None
            if timezone == 'PST' or timezone == 'EST':
                web_prefix = 'http://eng-homes.juniper.net/~' + user + '/'
            elif timezone == 'IST':
                web_prefix = 'http://ttbg-ubu16-03.juniper.net/~' + user + '/'
            if web_prefix:
                if 'framework_variables' in self and self['framework_variables'] \
                        is not None and 'fv-monitoring-engine' in self['framework_variables']:
                    self.log_console('Monitoring Engine Results: ' + web_prefix + re.sub(r"^.*toby_logs", "toby_logs",
                                                                                         self.logger.log_dir()) + "/monitor_data")
                    self.log(level="INFO", message='Monitoring Engine Results: ' + web_prefix + re.sub(r"^.*toby_logs", "toby_logs",
                                                                                 self.logger.log_dir()) + "/monitor_data")
                self.log_console("\n")

        #print CPU utilization information
#        server_cpu_usage()
        self.log_console("\nToby device initialization complete\n")
        self._create_global_tv_dictionary()
        self._dump_global_t_and_tv_dictionary_to_log_directory()

    def _get_associated_systems(self, resource, key, t_dict):
        """
        Returns the systems associated with the given resource based on key
        """
        mapped_devices = []
        for asso_res in self.t_dict['resources']:
            if key == self.t_dict['resources'][asso_res]['system']['primary'].get('system_id') and asso_res != resource:
                mapped_devices.append(asso_res)
        return mapped_devices

    def _merge_additional_resources(self, input_data):
        """
        There are times when nodes in the topology are NOT in LRM, but need to be nodes in the user's topology.
        Often, these are hosted within another resource as a virtual instance of something.
        This merges those resources
        :param input_data:
        :return:
        """
        if 'resources' in input_data:
            for resource in input_data['resources']:
                if resource not in self.t_dict['resources']:
                    self.t_dict['resources'][resource] = input_data['resources'][resource]

    def _merge_fv_uv_yaml_content_in_t(self, input_data):
        """
            Takes input_data as dictionary and merges it with t
        :param input_data:
        :return:
        """
        if 'user_variables' in input_data and isinstance(input_data['user_variables'], dict):
            if 'user_variables' not in self.t_dict or not isinstance(self.t_dict['user_variables'], dict):
                self.t_dict['user_variables'] = dict()
            for user_variable in input_data['user_variables']:
                self.t_dict['user_variables'][user_variable] = input_data['user_variables'][user_variable]
        if 'framework_variables' in input_data and isinstance(input_data['framework_variables'], dict):
            if 'framework_variables' not in self.t_dict or not isinstance(self.t_dict['framework_variables'], dict):
                self.t_dict['framework_variables'] = dict()
            for framework_variables in input_data['framework_variables']:
                self.t_dict['framework_variables'][framework_variables] = input_data['framework_variables'][framework_variables]

        if 'resources' in input_data:
            for resource in self.t_dict['resources']:
                if resource in input_data['resources']:
                    if 'primary' in self.t_dict['resources'][resource]['system'] and \
                                    'system' in input_data['resources'][resource] and \
                                    'primary' in input_data['resources'][resource]['system']:
                        if isinstance(input_data['resources'][resource]['system']['primary'], dict):
                            for system_key in input_data['resources'][resource]['system']['primary']:
                                if system_key.startswith('fv-') or system_key.startswith('uv-'):
                                    if system_key == 'fv-tags' and 'fv-tags' in self.t_dict['resources'][resource]['system']['primary']:
                                            current_fv_tags = self.t_dict['resources'][resource]['system']['primary']['fv-tags']
                                            to_add = input_data['resources'][resource]['system']['primary']['fv-tags']
                                            self.t_dict['resources'][resource]['system']['primary']['fv-tags'] = current_fv_tags + ':' + to_add
                                    else:
                                        self.t_dict['resources'][resource]['system']['primary'][system_key] = \
                                            input_data['resources'][resource]['system']['primary'][system_key]
                    if 'interfaces' in input_data['resources'][resource] and isinstance(input_data['resources'][resource]['interfaces'], dict):
                        for interface in input_data['resources'][resource]['interfaces']:
                            if 'interfaces' in self.t_dict['resources'][resource] and \
                                    isinstance(self.t_dict['resources'][resource]['interfaces'], dict):
                                if interface in self.t_dict['resources'][resource]['interfaces'] and \
                                        isinstance(input_data['resources'][resource]['interfaces'][interface], dict) and \
                                        isinstance(self.t_dict['resources'][resource]['interfaces'][interface], dict):
                                    for interface_key in input_data['resources'][resource]['interfaces'][interface]:
                                        if interface_key.startswith('fv-') or interface_key.startswith('uv-'):
                                            self.t_dict['resources'][resource]['interfaces'][interface][interface_key] = \
                                                input_data['resources'][resource]['interfaces'][interface][interface_key]


    def _dump_global_t_and_tv_dictionary_to_log_directory(self):
        """
            Dumps processed t and flatten tv dictionary to log path
        :return:
        """
        t_filename = os.path.join(self.logger.log_dir(), '.'.join([self._script_name, 'yaml']))
        output_stream = open(t_filename, "w")

        # Here we add a multi representer for the System class & Host class (base class for most devices) so that
        # when yaml tries to dump the device object we handle it ourselves, otherwise it crashes.
        from jnpr.toby.hldcl.system import System
        from jnpr.toby.hldcl.host import Host

        # Here we have a small function that just returns the object as a string
        def multi_representer(dumper, data):
            return dumper.represent_mapping(u'device_object', {'device_object': repr(data)})

        yaml.add_multi_representer(System, multi_representer)
        yaml.add_multi_representer(Host, multi_representer)
        yaml.dump(self.t_dict, output_stream, default_flow_style=False)
        output_stream.close()
        tv_file = '_'.join([self._script_name, 'tv'])
        tv_filename = os.path.join(self.logger.log_dir(), '.'.join([tv_file, 'yaml']))
        output_stream = open(tv_filename, "w")
        yaml.dump(self.tv_dict, output_stream, default_flow_style=False)
        output_stream.close()
        self.log(level="INFO", message="Topology Yaml File used for Toby : "+t_filename)

    def _create_global_tv_dictionary(self):
        """
            Creates flattened global tv dictionary
        :return:
        """

        if 'user_variables' in self.t_dict:
            for user_variable in self.t_dict['user_variables']:
                self.tv_dict[user_variable] = self.t_dict['user_variables'][user_variable]
        for resource in self.t_dict['resources']:
            for system in self.t_dict['resources'][resource]['system']:
                if system == 'primary':
                    for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                        for controller_key in self.t_dict['resources'][resource]['system'][system]['controllers'][controller]:
                            key = '__'.join([resource, controller, controller_key])
                            self.tv_dict[key] = self.t_dict['resources'][resource]['system'][system]['controllers'][controller][controller_key]
                    for system_key in self.t_dict['resources'][resource]['system'][system]:
                        if system_key != 'controllers' and not system_key.startswith('fv-'):
                            key = '__'.join([resource, system_key])
                            self.tv_dict[key] = self.t_dict['resources'][resource]['system'][system][system_key]
                elif system != 'dh':
                    for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                        for controller_key in self.t_dict['resources'][resource]['system'][system]['controllers'][controller]:
                            key = '__'.join([resource, system, controller, controller_key])
                            self.tv_dict[key] = self.t_dict['resources'][resource]['system'][system]['controllers'][controller][controller_key]
                    for system_key in self.t_dict['resources'][resource]['system'][system]:
                        if system_key != 'controllers' and not system_key.startswith('fv-'):
                            key = '__'.join([resource, system, system_key])
                            self.tv_dict[key] = self.t_dict['resources'][resource]['system'][system][system_key]
            if 'interfaces' in self.t_dict['resources'][resource]:
                for interface in self.t_dict['resources'][resource]['interfaces']:
                    for interface_key in self.t_dict['resources'][resource]['interfaces'][interface]:
                        key = '__'.join([resource, interface, interface_key])
                        self.tv_dict[key] = self.t_dict['resources'][resource]['interfaces'][interface][interface_key]
                        if interface_key == 'name':
                            ifd = re.match(r'\w+-(\d+)/(\d+)/(\d+)(.*)', self.t_dict['resources'][resource]['interfaces'][interface][interface_key])
                            if ifd:
                                key = '__'.join([resource, interface, 'fpcslot'])
                                self.tv_dict[key] = ifd.group(1)
                                key = '__'.join([resource, interface, 'picslot'])
                                self.tv_dict[key] = ifd.group(2)
                                key = '__'.join([resource, interface, 'portslot'])
                                self.tv_dict[key] = ifd.group(3)
                                if ifd.group(4) and not ifd.group(4).startswith('.'):
                                    portchannel = ifd.group(4)[1:]
                                    channel = portchannel.split('.')
                                    if channel[0]:
                                        key = '__'.join([resource, interface, 'portchannel'])
                                        self.tv_dict[key] = channel[0]

    def _validate_and_handle_framework_variables(self):
        """
            Validate all supported framework variables and update t_dict
        :return:
        """
        import jnpr.toby.frameworkDefaults.credentials as credentials
        framework_variables = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__),\
                                       "frameworkVariables.yaml")))
        for resource in self.t_dict['resources']:
            f_vars = {}
            if 'framework_variables' in self.t_dict and isinstance(self.t_dict['framework_variables'], dict):
                for global_fv in self.t_dict['framework_variables']:
                    if global_fv.startswith('fv-'):
                        f_vars[global_fv] = self.t_dict['framework_variables'][global_fv]
            for attribute in self.t_dict['resources'][resource]['system']['primary']:
                if attribute.startswith('fv-'):
                    f_vars[attribute] = self.t_dict['resources'][resource]['system']['primary'][attribute]

            #Now I have all the framework variables needs to be handlled for this resource.
            for f_var in f_vars:
                if f_var in framework_variables:
                    self._validate_allowed_values_for_fvar(f_var, f_vars[f_var], framework_variables[f_var])
                    # added this part for TOBY-1226 - fv w/ destination as interface not trickling down to
                    # interfaces
                    fvar_structure = framework_variables[f_var]
                    if fvar_structure['destination'] == 'interfaces':
                        for interface in self.t_dict['resources'][resource]['interfaces']:
                            self._update_t_dict_with_framework_variable(resource, f_var, f_vars[f_var],\
                                    framework_variables[f_var], interface=interface)
                    else:
                        self._update_t_dict_with_framework_variable(resource, f_var, f_vars[f_var],\
                                framework_variables[f_var])
                    add_to_toby_exec("framework_variables", {f_var:str(f_vars[f_var])})
                    self.log(level="DEBUG", message="Validation complete for "+f_var+" :: "+ str(f_vars[f_var]))
                else:
                    raise TobyException("Framework variable: " + f_var + " is not supported in Toby.")

            if 'interfaces' in self.t_dict['resources'][resource]:
                for interface in self.t_dict['resources'][resource]['interfaces']:
                    f_vars = {}
                    for attribute in self.t_dict['resources'][resource]['interfaces'][interface]:
                        if attribute.startswith('fv-'):
                            f_vars[attribute] = self.t_dict['resources'][resource]['interfaces'][interface][attribute]
                    # Now I have all the framework variables needs to be handlled for interface block
                    for f_var in f_vars:
                        if f_var in framework_variables:
                            self._validate_allowed_values_for_fvar(f_var, f_vars[f_var], framework_variables[f_var])
                            self._update_t_dict_with_framework_variable(resource, f_var, f_vars[f_var],\
                                    framework_variables[f_var], interface=interface)
                            add_to_toby_exec("framework_variables", {f_var:str(f_vars[f_var])})
                            self.log(level="DEBUG", message="Validation complete for "+f_var+" :: "+ str(f_vars[f_var]))
                        else:
                            raise TobyException("Framework variable: " + f_var + " is not supported in Toby under Interface.")

    def _update_t_dict_with_framework_variable(self, resource, f_var, fvar_value, fvar_structure, interface=None):
        """

        :param resource:
        :param f_var:
        :param fvar_value:
        :param fvar_structure:
        :return:
        """
        if fvar_structure['type'] == 'string':
            key = fvar_structure['content']['key']
            if fvar_structure['destination'] == 'controllers':
                for system in self.t_dict['resources'][resource]['system']:
                    for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                        self.t_dict['resources'][resource]['system'][system]['controllers'][controller][key]\
                                = fvar_value
            elif fvar_structure['destination'] == 'system-nodes':
                for system in self.t_dict['resources'][resource]['system']:
                    self.t_dict['resources'][resource]['system'][system][key] = fvar_value
            elif fvar_structure['destination'] == 'interfaces':
                if interface:
                    self.t_dict['resources'][resource]['interfaces'][interface][key] = fvar_value
        elif fvar_structure['type'] == 'boolean':
            key = fvar_structure['content']['key']
            value = fvar_structure['content']['value']
            fvarvalueas_list = fvar_value.split(':')
            if fvar_structure['destination'] == 'system-nodes':
                for system in self.t_dict['resources'][resource]['system']:
                    if fvar_value == 'none':
                        self.t_dict['resources'][resource]['system'][system][key] = False
                    elif fvar_value == 'all':
                        self.t_dict['resources'][resource]['system'][system][key] = value
                    else:
                        if system in fvarvalueas_list:
                            self.t_dict['resources'][resource]['system'][system][key] = value
            elif fvar_structure['destination'] == 'controllers':
                for system in self.t_dict['resources'][resource]['system']:
                    for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                        if fvar_value == 'none':
                            self.t_dict['resources'][resource]['system'][system]['controllers'][controller][key] = False
                        elif fvar_value == 'all':
                            self.t_dict['resources'][resource]['system'][system]['controllers'][controller][key] = value
                        elif controller in fvarvalueas_list:
                            self.t_dict['resources'][resource]['system'][system]['controllers'][controller][key] = value
        elif fvar_structure['type'] == 'list':
            key = fvar_structure['content']['key']
            value = fvar_value.split(':')
            if fvar_structure['destination'] == 'system-nodes':
                for system in self.t_dict['resources'][resource]['system']:
                    self.t_dict['resources'][resource]['system'][system][key] = value
            elif fvar_structure['destination'] == 'controllers':
                for system in self.t_dict['resources'][resource]['system']:
                    for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                        self.t_dict['resources'][resource]['system'][system]['controllers'][controller][key] = value
            elif fvar_structure['destination'] == 'same':
                if interface:
                    self.t_dict['resources'][resource]['interfaces'][interface][key] = value
                else:
                    for system in self.t_dict['resources'][resource]['system']:
                        self.t_dict['resources'][resource]['system'][system][key] = value
        elif fvar_structure['type'] == 'dictionary':
            tmp_dict = None
            if type(fvar_value) is dict:  #already a dictionary
                tmp_dict = fvar_value
            else:
                tmp_dict = {}
                fvarvalueas_list = fvar_value.split(':')
                for item in fvarvalueas_list:
                    tmp_var = item.split('=', 1)
                    tmp_dict[tmp_var[0]] = tmp_var[1]
            if fvar_structure['destination'] == 'controllers':
                for system in self.t_dict['resources'][resource]['system']:
                    for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                        for content in fvar_structure['content']:
                            if content in tmp_dict:
                                key = fvar_structure['content'][content]
                                value = tmp_dict[content]
                                self.t_dict['resources'][resource]['system'][system]['controllers'][controller][key] = value
            elif fvar_structure['destination'] == 'system-nodes':
                for system in self.t_dict['resources'][resource]['system']:
                    key = fvar_structure['content']['key']
                    self.t_dict['resources'][resource]['system'][system][key] = tmp_dict
        elif fvar_structure['type'] == 'complex':
            key = fvar_structure['content']['key']
            if fvar_structure['destination'] == 'global':
                if 'framework_variables' not in self.t_dict or not isinstance(self.t_dict['framework_variables'], dict):
                    self.t_dict['framework_variables'] = dict()
                self.t_dict['framework_variables'][key] = fvar_value
                if f_var in self.t_dict['framework_variables']:
                    del self.t_dict['framework_variables'][f_var]

    def _validate_allowed_values_for_fvar(self, f_var, fvar_value, fvar_structure):
        """

        :param f_var:
        :param fvar_value:
        :param fvar_structure:
        :return:
        """
        if 'allowed-values' in fvar_structure:
            #Validate values
            value_list = fvar_value.split(':')
            for value in value_list:
                if value not in fvar_structure['allowed-values']:
                    raise TobyException("Value: " + value + " supplied with Framework variable: " + f_var +\
                          " is not in one of the allowed values." + " Allowed values are: " +\
                          str(fvar_structure['allowed-values']))

    def _validate_t_data(self):
        """
            Validate all mandatory attribute in t
        :return:
        """
        if 'resources' not in self.t_dict:
            raise TobyException("Missing mandatory information: 'resources' Dictionary is not present.")
        elif not isinstance(self.t_dict['resources'], dict):
            raise TobyException("Missing mandatory information: 'resources' is not Dictionary type.")
        for resource in self.t_dict['resources']:
            if not isinstance(self.t_dict['resources'][resource], dict):
                raise TobyException("Missing mandatory information: resource: " + resource + " is not Dictionary type.")
            elif 'system' not in self.t_dict['resources'][resource]:
                raise TobyException("Missing mandatory information: system data not present for resource: " + resource)
            elif not isinstance(self.t_dict['resources'][resource]['system'], dict):
                raise TobyException("Missing mandatory information: system data is not Dictionary type for resource: " + resource)
            elif 'primary' not in self.t_dict['resources'][resource]['system']:
                raise TobyException("Missing mandatory information: primary system not present for resource: " + resource)

            for system in self.t_dict['resources'][resource]['system']:
                if not isinstance(self.t_dict['resources'][resource]['system'][system], dict):
                    raise TobyException("Missing mandatory information: system node " + system + " is not Dictionary type for resource: " + resource)
                elif 'controllers' not in self.t_dict['resources'][resource]['system'][system]:
                    raise TobyException("Missing mandatory information: system node " + system +
                                        " does not have controllers for resource: " + resource)
                elif not isinstance(self.t_dict['resources'][resource]['system'][system]['controllers'], dict):
                    raise TobyException("Missing mandatory information: controllers of system node " +
                                        system + " is not Dictionary type for resource: " + resource)
                elif 'name' not in self.t_dict['resources'][resource]['system'][system]:
                    raise TobyException("Missing mandatory information: system node " + system +
                                        ' does not have name attribute for resource: ' + resource)
                elif 'model' not in self.t_dict['resources'][resource]['system'][system]:
                    raise TobyException("Missing mandatory information: system node " + system +
                                        " does not have model attribute for resource: " + resource)
                elif 'osname' not in self.t_dict['resources'][resource]['system'][system]:
                    raise TobyException("Missing mandatory information: system node " + system +
                                        " does not have osname attribute for resource: " + resource)
                for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                    if not isinstance(self.t_dict['resources'][resource]['system'][system]['controllers'][controller], dict):
                        raise TobyException("Missing mandatory information: controller " + controller + " of system node "
                                            + system + " is not Dictionary type for resource: " + resource)
                    elif 'hostname' not in self.t_dict['resources'][resource]['system'][system]['controllers'][controller] and\
                        'mgt-ip' not in self.t_dict['resources'][resource]['system'][system]['controllers'][controller]:
                        raise TobyException("Missing mandatory information: hostname/mgt-ip under controller " + controller +
                                            " of system node " + system + " is not present for resource: " + resource)
            if 'interfaces' in self.t_dict['resources'][resource] and isinstance(self.t_dict['resources'][resource]['interfaces'], dict):
                for interface in self.t_dict['resources'][resource]['interfaces']:
                    if interface in self.t_dict['resources'][resource]['system']:
                        raise TobyException("Interface name: " + interface + " can not be same as on of the system nodes.")
                    if not isinstance(self.t_dict['resources'][resource]['interfaces'][interface], dict):
                        raise TobyException("Missing mandatory information: interface " + interface +
                                            " is not Dictionary type for resource: " + resource)
                    elif 'name' not in self.t_dict['resources'][resource]['interfaces'][interface]:
                        raise TobyException("Missing mandatory information: interface " + interface +
                                            " does not have name attribute for resource: " + resource)

    def _print_topology_info(self, connect_success=False):
        """
            Prints Topology Data in log and console
        :return:
        """
        if connect_success:
            topology = "TOPOLOGY (with OS Version) ::\n"
        else:
            topology = "TOPOLOGY ::\n"
        for resource in self.t_dict['resources']:
            topology += "  " + resource + ":\n"
            topology += "    " + "system:\n"
            for system in self.t_dict['resources'][resource]['system']:
                if system == 'dh':
                    continue
                if 'fv-tags' in self.t_dict['resources'][resource]['system'][system].keys() and \
                   re.match('dut', self.t_dict['resources'][resource]['system'][system]['fv-tags'], re.I):
                    topology += "      " + system + "\t\t" + self.t_dict['resources'][resource]['system'][system]['name'] + \
                    "(" + str(self.t_dict['resources'][resource]['system'][system]['model']) + ")"\
                    "(" + str(self.t_dict['resources'][resource]['system'][system]['fv-tags']) + ")"
                else:
                    topology += "      " + system + "\t\t" + self.t_dict['resources'][resource]['system'][system]['name'] + \
                    "(" + str(self.t_dict['resources'][resource]['system'][system]['model']) + ")"

                if 'os-ver' in self.t_dict['resources'][resource]['system'][system].keys():
                    if self.t_dict['resources'][resource]['system'][system]['os-ver']:
                        topology += "   os_version:" + str(self.t_dict['resources'][resource]['system'][system]['os-ver']) + "\n"
                    else:
                        topology += "\n"
                else:
                    topology += "\n"

            if 'interfaces' in self.t_dict['resources'][resource]:
                topology += "    " + "interfaces:\n"
                for interface in self.t_dict['resources'][resource]['interfaces']:
                    topology += "      " + interface + "\t\t" + \
                                self.t_dict['resources'][resource]['interfaces'][interface]['name']
                    if 'link' in self.t_dict['resources'][resource]['interfaces'][interface]:
                        topology += "(" + self.t_dict['resources'][resource]['interfaces'][interface]['link'] + ")\n"
                    else:
                        topology += "\n"
        self.log(topology)
        if Vars().get_global_variable('${console_log}') is None:
            self.log_console(topology)

    def _render_topology(self):
        from graphviz import Graph

        graph = Graph(format='png')
        links = {}
        for resource in self.t_dict['resources']:
            resource_name = None
            for system in self.t_dict['resources'][resource]['system']:
                if system == 'primary':
                    make = self.t_dict['resources'][resource]['system'][system]['make']
                    model = self.t_dict['resources'][resource]['system'][system]['model']
                    resource_name = self.t_dict['resources'][resource]['system'][system]['name']
                    label = resource + ':' + resource_name + ' (' + model + ')'
                    style = ''
                if make.upper() == 'JUNIPER':
                    style = 'filled'
                graph.node(resource_name, label, shape='box', style=style, fillcolor='lightblue')
            if 'interfaces' in self.t_dict['resources'][resource]:
                for interface in self.t_dict['resources'][resource]['interfaces']:
                    if 'link' in self.t_dict['resources'][resource]['interfaces'][interface]:
                        link_name = self.t_dict['resources'][resource]['interfaces'][interface]['link']
                        if link_name not in links:
                            link = []
                            links[link_name] = link
                        links[link_name].append(resource_name)

        for link in links:
            if len(links[link]) == 2:
                graph.edge(links[link][0], links[link][1], label=link)
            elif len(links[link]) >= 2:
                graph.node(link, 'lan:' + link, shape='diamond')
                for resource in links[link]:
                    graph.edge(link, resource)

        #print(graph.source)
        png_file = self._log_dir + '/topology'
        graph.render(png_file, cleanup=True)


    def _process_proxy_resource_aliases(self):
        """
            If fv-proxy used, and resource specified instead of host for a given proxy, set 'host' key based on
            mgt-ip from controller in resource alias
            :return:
        """
        for resource in self.t_dict['resources']:
            for system in self.t_dict['resources'][resource]['system']:
                for controller in self.t_dict['resources'][resource]['system'][system]['controllers']:
                    if 'proxy_hosts' in self.t_dict['resources'][resource]['system'][system]['controllers'][controller]:
                        for proxy_host in self.t_dict['resources'][resource]['system'][system]['controllers'][controller]['proxy_hosts']:
                            if 'resource' in proxy_host:
                                proxy_resource = proxy_host['resource'] #ex: h0
                                if proxy_resource in self.t_dict['resources']:
                                    if 'controller' in proxy_host:
                                        proxy_host['host'] = self.t_dict['resources'][proxy_resource]['system']['primary'] \
                                                             ['controllers'][proxy_host['controller']]['mgt-ip']
                                        break
                                    for proxy_controller in self.t_dict['resources'][proxy_resource]['system']['primary']['controllers']:
                                        proxy_host['host'] = self.t_dict['resources'][proxy_resource]['system']['primary'] \
                                                             ['controllers'][proxy_controller]['mgt-ip']
                                        break
                                else:
                                    raise TobyException("resource " + proxy_resource + " specified in fv-proxy host is not a node in the topology")



    def _process_ixia_appserver(self):
        """
            Takes an ixia appserver as a resource and sets it to fv-ixia-appserver within ixia resource
            :return:
        """
        appserver = None
        ixia_ref = None
        appserver_name = 'Unknown'
        chassis_name = 'Unknown'
        username = None
        password = None
        port = None

        for resource in self.t_dict['resources']:
            if str(self.t_dict['resources'][resource]['system']['primary']['model']).upper().endswith('APPSERVER'):
                appserver_name = resource
                appserver = self.t_dict['resources'][resource]['system']['primary']['controllers']['if0']['mgt-ip']
                if re.search('linux', str(self.t_dict['resources'][resource]['system']['primary']['osname']), re.I):
                    port = 443
                    username, password = credentials.get_credentials(os='IxiaAppserver')
            elif self.t_dict['resources'][resource]['system']['primary']['make'].upper().startswith('IX') and not \
                    self.t_dict['resources'][resource]['system']['primary']['make'].upper().startswith('IXS'):
                chassis_name = resource
                ixia_ref = self.t_dict['resources'][resource]['system']['primary']
        if appserver:
            # remove the appserver to avoid confusion with IXIA chassis during Device processing
            del self.t_dict['resources'][appserver_name]
            # assign appserver
            if ixia_ref and 'fv-ixia-appserver' not in ixia_ref.keys():
                self.log(level="DEBUG", message="Assigning mgt-ip from resource " + appserver_name + " to fv-ixia-appserver within resource " + chassis_name)
                ixia_ref['fv-ixia-appserver'] = appserver
        if username:
            if ixia_ref and 'fv-ixia-appserver-username' not in ixia_ref.keys():
                self.log(level="DEBUG", message="Assigning username to fv-ixia-appserver-username within resource " + chassis_name)
                ixia_ref['fv-ixia-appserver-username'] = username
        if password:
            if ixia_ref and 'fv-ixia-appserver-password' not in ixia_ref.keys():
                self.log(level="DEBUG", message="Assigning password to fv-ixia-appserver-password within resource " + chassis_name)
                ixia_ref['fv-ixia-appserver-password'] = password
        if port:
            if ixia_ref and 'fv-ixia-appserver-port' not in ixia_ref.keys():
                self.log(level="DEBUG", message="Assigning port to fv-ixia-appserver-port within resource " + chassis_name)
                ixia_ref['fv-ixia-appserver-port'] = port

    def _process_spirent_appserver(self):
        """
            Takes an spirent appserver as a resource and sets it to fv-spirent-labserver within spirent resource
            :return:
        """
        appserver = None
        spirent_ref = None
        appserver_name = 'Unknown'
        chassis_name = 'Unknown'

        for resource in self.t_dict['resources']:
            if str(self.t_dict['resources'][resource]['system']['primary']['model']).upper().endswith('APPSERVER') and  \
                self.t_dict['resources'][resource]['system']['primary']['make'].upper().startswith('SPIRENT'):
                appserver_name = resource
                appserver = self.t_dict['resources'][resource]['system']['primary']['controllers']['if0']['mgt-ip']
            elif self.t_dict['resources'][resource]['system']['primary']['make'].upper().startswith('SPIRENT'):
                chassis_name = resource
                spirent_ref = self.t_dict['resources'][resource]['system']['primary']
        if appserver:
            # remove the appserver to avoid confusion with SPIRENT chassis during Device processing
            del self.t_dict['resources'][appserver_name]
            # assign appserver
            if spirent_ref and 'fv-spirent-labserver' not in spirent_ref.keys():
                self.log(level="DEBUG", message="Assigning mgt-ip from resource " + appserver_name + " to fv-spirent-labserver within resource " + chassis_name)
                spirent_ref['fv-spirent-labserver'] = appserver

    def _connect_device(self, resource):
        """
            Connect to device
            Connect engine creates connection object and refills it back to testbed object.

            :param system:
                *MANDATORY* mandatory system object
            :param dev:
                *MANDATORY* mandatory Device object name
            :return:  Testbed object with connection handles populated
        """
        system = self.t_dict['resources'][resource]['system']
        interfaces = None
        if 'system_id' in system['primary']:
            key = system['primary'].get('system_id')
            systems = self._get_associated_systems(resource, key, self.t_dict)
            system['primary']['associated_devices'] = systems

        if 'interfaces' in self.t_dict['resources'][resource]:
            interfaces = self.t_dict['resources'][resource]['interfaces']

        # Getting device object handle
        try:
            for system_node in system.keys():
                if 'osname' not in system[system_node] and 'model' in system[system_node]:
                    if re.match(r'nix', str(system[system_node]['model']).lower()) or \
                            re.match(r'nux', str(system[system_node]['model']).lower()):
                        system[system_node]['osname'] = 'unix'
            for system_node in system.keys():
                system[system_node]['tag_name'] = resource
                system[system_node]['flavor'] = 'unknown' # default flavor for OS

            system['dh'] = Device(system=system)
        except (TobyLinkFail,TobyIxiaException,TobyIxiaAppserverConnectException,TobyIxiaChassisConnectException,SpirentConnectError, SpirentLicenseError, TobySpirentLabserverConnectException, TobySpirentChassisConnectException, TobySpirentException) as error:
            raise
        except Exception as error:
            osname = system['primary']['osname']
            device = system['primary']['name']
            if osname == 'JunOS':
                raise TobyException("ERROR: "+str(error))
            else:
                raise TobyException("ERROR: "+str(error)+"\n Could not establish connection to "+str(osname)+" device '"+str(device)+"'")

        # Fill 't' with additional information
        try:
            os_ver = 'unknown_version'
            # Adding information only specific to Junos
            if re.match(r'junos', system['primary']['osname'].lower()):
                self.t_dict['resources'][resource]['system']['primary']['os-ver'] = 'unknown_version'
                try:
                    system['dh'].current_node.current_controller.channels['pyez'].facts_refresh()
                    os_ver = system['dh'].current_node.current_controller.channels['pyez'].facts['version']
                    if os_ver is None or os_ver is 'unknown_version':
                        os_ver = system['dh'].current_node.current_controller.get_facts(attribute='version')
                    self.log(resource + "__VERSION=" + str(os_ver))
                    self.t_dict['resources'][resource]['system']['primary']['os-ver'] = str(os_ver)
                except Exception:
                    self.log(level="INFO", message="Could not refresh facts for pyez channel")
                try:
                    resp = system['dh'].current_node.current_controller.cli(command='show chassis hardware').response()
                    self.log(resource + "__HARDWARE_DETAILS=" + resp)
                except Exception:
                    self.log(level="INFO", message='Could not get hardware details')
                # Checking to see if device is classic Junos flavor or is evo and then storing that information
                for system_node in system.keys():
                    # Need to skip device handle since that has been added as a key to 'system' dict earlier
                    if system_node != 'dh':
                        try:
                            res = system['dh'].nodes[system_node].current_controller.shell(command='ls /usr/share/cevo/').response()
                            if re.search('cevo_version', res):
                                self.t_dict['resources'][resource]['system'][system_node]['flavor'] = 'evo'
                            else:
                                self.t_dict['resources'][resource]['system'][system_node]['flavor'] = 'classic'
                        except Exception:
                            pass

        except Exception as error:
            device = system['primary']['name']
            raise TobyException("ERROR: "+str(error)+"\n Unable not get additional JUNOS information on device '"+str(device)+"'")

        # For jpg device
        try:
            if system['primary']['osname'].upper() == 'JUNOS' and \
                    str(system['primary']['model']).upper() == 'JPG':
                system['dh'].current_node.current_controller.set_jpg_interfaces(intf=self.t_dict['resources'][resource]['interfaces'])
                system['dh'].current_node.current_controller.configure_jpg()

        except Exception as error:
            device = system['primary']['name']
            raise TobyException("ERROR: "+str(error)+"\n Unable to configure JPG on device '"+str(device)+"'")

        # For ixia and spirent, connect needs ports as well
        try:
            if system['primary']['osname'].upper().startswith('IX') or \
                    system['primary']['osname'].upper() == 'SPIRENT' or \
                    system['primary']['osname'].upper() == 'BREAKINGPOINT' or \
                    system['primary']['osname'].upper() == 'PARAGON' or \
                    'warp17' in system['primary']:

                # Connect to IxVeriwave chassis without any port list
                if system['primary']['osname'].upper() == 'IXVERIWAVE':
                    session_info = system['dh'].connect()
                    self.log('INFO', session_info)

                # For all the other devices, IxVeriwave may come under here later
                else:
                    intf_to_port_map = dict()
                    intf_list = list()
                    if 'interfaces' in self.t_dict['resources'][resource]:
                        for intf_alias in sorted(self.t_dict['resources'][resource]['interfaces'].keys()):
                            port_name = self.t_dict['resources'][resource]['interfaces'][intf_alias]['name']
                            #address issue where port documented as 0/#/# instead of #/#
                            if re.search(r"^\d+\/\d+\/\d+", port_name):
                                port_name = re.sub(r"^\d+\/", "", port_name)
                            elif re.search(r"^[a-z]+-\d+\/\d+\/\d+", port_name):
                                port_name = re.sub(r"^[a-z]+-\d+\/", "", port_name)
                            intf_to_port_map[intf_alias] = port_name
                            intf_list.append(port_name)
                    try:
                        system['dh'].add_interfaces(interfaces=interfaces)
                    except Exception:
                        pass

                    system['dh'].add_intf_to_port_map(intf_to_port_map)
                    #Toby Users can disable traffic generator port handle reservation and creation by passing
                    #fv-connect-controllers == none in params file or yaml file
                    if 'fv-connect-controllers' in system['primary'] and \
                        re.search('none', system['primary']['fv-connect-controllers'], re.I):
                        self.log(level="WARN", message="fv-connect-controllers is set to NONE for Traffic Generators,Skipping connection")
                    else:
                        session_info = system['dh'].connect(port_list=intf_list)
                        self.log(level='INFO', message = session_info)

        except Exception as error:
            device = system['primary']['name']
            raise TobyException("ERROR: "+str(error)+"\n Unable to map trafficgen ports on device '"+str(device)+"'")

    def _get_package_details(self, release, remote_path):
        """
        :return:
        """
        package_type = 'jinstall'
        arch = None
        path = '.'
        issu = False
        nssu = False
        tag = None
        suffix = None
        package = None

        if 'framework_variables' in t and 'software-install' in t['framework_variables']\
                and 'package' in t['framework_variables']['software-install']:
            issu = t['framework_variables']['software-install']['package'].get('issu', False)
            nssu = t['framework_variables']['software-install']['package'].get('nssu', False)
            arch = t['framework_variables']['software-install']['package'].get('arch', None)
            package_type = t['framework_variables']['software-install']['package'].get('type', 'jinstall')
            path = t['framework_variables']['software-install']['package'].get('path', '.')
            remote_path = t['framework_variables']['software-install']['package'].get('remote_path', remote_path)
            tag = t['framework_variables']['software-install']['package'].get('tags', None)
            suffix = t['framework_variables']['software-install']['package'].get('suffix', None)
            #Update data from from structure#
            if 'from' in t['framework_variables']['software-install']['package']:
                for from_list in t['framework_variables']['software-install']['package']['from']:
                    if str(from_list['release']).upper() == str(release).upper():
                        issu = from_list.get('issu', issu)
                        nssu = from_list.get('nssu', nssu)
                        arch = from_list.get('arch', arch)
                        package_type = from_list.get('type', package_type)
                        path = from_list.get('path', path)
                        remote_path = from_list.get('remote_path', remote_path)
                        tag = from_list.get('tags', tag)
                        suffix = from_list.get('suffix', suffix)
                        package = from_list.get('build', package)
            #Update data from to structure#
            if 'to' in t['framework_variables']['software-install']['package']:
                if str(t['framework_variables']['software-install']['package']['to']['release']).upper() == str(release).upper():
                    issu = t['framework_variables']['software-install']['package']['to'].get('issu', issu)
                    nssu = t['framework_variables']['software-install']['package']['to'].get('nssu', nssu)
                    arch = t['framework_variables']['software-install']['package']['to'].get('arch', arch)
                    package_type = t['framework_variables']['software-install']['package']['to'].get('type', package_type)
                    path = t['framework_variables']['software-install']['package']['to'].get('path', path)
                    remote_path = t['framework_variables']['software-install']['package']['to'].get('remote_path', remote_path)
                    tag = t['framework_variables']['software-install']['package']['to'].get('tags', tag)
                    suffix = t['framework_variables']['software-install']['package']['to'].get('suffix', suffix)
                    package = t['framework_variables']['software-install']['package']['to'].get('build', package)

        if package is not None and not re.search(release, package, re.I):
            raise TobyException("ERROR: Release verion (%s) is not matching with the build specified(%s)"
                                % (release, package))

        return (package_type, arch, path, issu, tag, remote_path, nssu, suffix, package)

    def install_package(self, release=None, tag='dut', cleanfs=False, remote_path='/var/tmp', release_set=None, reboot=True, issu=None, nssu=None, timeout=1800, issu_options=None, no_copy=False, force_host=False):
        """
        Performs the complete installation of the **package**

        ARGUMENTS:

            [release=None, tag='dut', cleanfs=False, remote_path='/var/tmp',
            release_set=None, reboot=True, issu=None, nssu=None, timeout=1800, issu_options=None,
             no_copy=False, force_host=False]

            :param STR release:
                *OPTIONAL* it will have the pacakage or build version

            :param STR tag:
                *OPTIONAL* user sepcified. Default Tag is dut

            :param BOOLEAN cleanfs:
                *OPTIONAL* 'storage cleanup' before copying the file to the device.
                         Default cleanfs is False

            :param STR remote_path:
                *OPTIONAL* the image is copied from the local filesystem to the :remote_path: directory
                        on the target Junos device. The default is ``/var/tmp``

            :param STR release_set:
                    release_set = [{'release':'15.1', 'tag':'abc'}, {'release':'15.1R5.5', 'tag':'xyz'}]
                    t.install_package(release_set=release_set, remote_path='/tmp')

            :param BOOLEAN reboot:
                *OPTIONAL* Perform a system reboot. Default reboot is ``True``

            :param BOOLEAN issu:
                *OPTIONAL* When ``True`` allows unified in-service software upgrade (ISSU)
                    feature enables you to upgrade between two different Junos OS
                    releases with no disruption on the control plane and with minimal
                    disruption of traffic.

            :param BOOLEAN nssu:
                *OPTIONAL*  When ``True`` allows nonstop software upgrade (NSSU) enables you
                        to upgrade the software running on a Juniper Networks EX Series
                        Virtual     Chassis or a Juniper Networks EX Series Ethernet Switch
                        with redundant Routing Engines with a single command and puminimal
                         disruption to          network traffic.

            :param BOOLEAN timeout:
                *OPTIONAL* The amount of time (seconds) required to install_package.
                        Default is set to 1800

            :param STR issu_options:
                *OPTIONAL* extra CLI arguments for the ISSU.

            :param BOOLEAN no_copy:
                *OPTIONAL* When the value of :package: or :pkg_set is not a URL, and the value of
                        :no_copy: is ``True`` the software package will not be copied to the device
                        and is presumed to already exist on the :remote_path: directory of the target
                        Junos device. When the value of :no_copy: is ``False`` (the default), then the
                        package is copied from the local PyEZ host to the :remote_path: directory of the
                        target Junos device.If the value of :package: or :pkg_set: is a URL,
                        then the value of :no_copy: is unused.

            :param BOOLEAN force_host:
                *OPTIONAL*  When ``True`` perform the copy even if :package: is already present
                        at the :remote_path: directory on the remote Junos device. When ``False`` (default)
                        if the :package: is already present at the :remote_path:, AND the local checksum matches
                        the remote checksum, then skip the copy to optimize time.

        ROBOT USAGE:
            Install Package         release_set=${release_set}     issu=${False}   cleanfs=${True}    no_copy=${False}

        :return:None
        """
        install_list = []
        issu_option = issu
        nssu_option = nssu
        vmhost = False

        if release_set is not None and isinstance(release_set, list):
            for rset in release_set:
                if 'release' not in rset:
                    raise TobyException("release is mandatory under release_set list")
                release = rset['release']
                res_list = []
                (package_type, arch, path, issu, in_tag, remote_path, nssu, suffix, package) \
                    = self._get_package_details(release=release, remote_path=remote_path)

                if issu_option is not None:
                    issu = issu_option
                if nssu_option is not None:
                    nssu = nssu_option
                if issu == True and nssu == True:
                    self.log(level="WARN", message="Both NSSU and ISSU cannot be set to True. Resetting ISSU to False.")
                    issu = False
                if package_type == 'vmhost':
                    vmhost = True
                if in_tag is not None:
                    if not isinstance(in_tag, list) and in_tag.upper() == 'ALL':
                        res_list = self.get_resource_list()
                    else:
                        res_list = self.get_resource_list(tag=in_tag)
                elif 'tag' in rset:
                    res_list = self.get_resource_list(tag=rset['tag'])

                if not res_list:
                    raise TobyException("ERROR: Device list is empty for Software Install, please check your input.")

                for res in res_list:
                    if t['resources'][res]['system']['primary']['osname'].upper() == 'JUNOS':
                        model = t['resources'][res]['system']['primary']['model']
                        handle = self.get_handle(resource=res)
                        if not package:
                            package = self.get_package_name(release=release, model=model, package_type=package_type,
                                                            arch=arch, suffix=suffix, resource_handle=handle)
                            if no_copy:
                                package = remote_path + '/' + package
                            else:
                                package = path + '/' + package
                        self.log_console("Installing Software: " + package + " On device: " + res)
                        install_list.append(
                            {'fname': handle.software_install, 'parent_thread': True,
                             'kwargs': {'issu': issu, 'package': package, 'cleanfs': cleanfs, 'reboot': reboot, 'nssu':nssu, \
                                        'remote_path': remote_path, 'release': release, 'timeout': timeout, 'vmhost': vmhost, \
                                          'issu_options': issu_options, 'no_copy': no_copy, 'force_host': force_host}})
        else:
            res_list = []
            (package_type, arch, path, issu, in_tag, remote_path, nssu, suffix, package) = self._get_package_details(release=release, remote_path=remote_path)
            if issu_option is not None:
                issu = issu_option
            if nssu_option is not None:
                nssu = nssu_option

            if issu == True and nssu == True:
                self.log(level="WARN", message="Both NSSU and ISSU cannot be set to True. Resetting ISSU to False.")
                issu = False

            if package_type == 'vmhost':
                vmhost = True
            if in_tag is not None:
                if not isinstance(in_tag, list) and in_tag.upper() == 'ALL':
                    res_list = self.get_resource_list()
                else:
                    res_list = self.get_resource_list(tag=in_tag)
            else:
                res_list = self.get_resource_list(tag=tag)

            if not res_list:
                raise TobyException("ERROR: Device list is empty for Software Install, please check your input.")

            for res in res_list:
                if t['resources'][res]['system']['primary']['osname'].upper() == 'JUNOS':
                    model = t['resources'][res]['system']['primary']['model']
                    handle = self.get_handle(resource=res)
                    if not package:
                        package = self.get_package_name(release=release, model=model, package_type=package_type, arch=arch,  \
                                                         suffix=suffix, resource_handle=handle)
                        if no_copy:
                            package = remote_path + '/' + package
                        else:
                            package = path + '/' + package
                    self.log_console("Installing Software: " + package + " On device: " + res)
                    install_list.append(
                        {'fname': handle.software_install, 'parent_thread': True,
                         'kwargs': {'issu': issu, 'package': package, 'cleanfs': cleanfs, 'reboot': reboot, 'nssu':nssu,
                                    'remote_path': remote_path, 'release': release, 'timeout': timeout, 'vmhost': vmhost, 'issu_options': issu_options, 'no_copy': no_copy, 'force_host': force_host}})
        if install_list:
            run_multiple(install_list)

    def get_package_name(self, release, model, package_type='jinstall', arch=None, suffix=None, resource_handle=None):
        """
        Takes release name and model as input and returns Package name

        ARGUMENTS:
            [release, model, package_type='jinstall', arch=None, suffix=None, resource_handle=None]

            :param STR release:
                *MANDATORY* release version Eg: 17.1R1
            :param STR model:
                *MANDATORY*  Device model Name  Eg: mx240
            :param STR package_type:
                *OPTIONAL* Type of package.Deafult is set to jinstall
            :param STR arch:
                *OPTIONAL* arch name.Default is set to None
            :param STR suffix:
                *OPTIONAL* Image suffix (Ex: controlled-signed.tgz / secure-signed.tgz /
                domestic-signed.tgz/ signed-tgz). Default is set to None.
            :param STR resource_handle:
                *OPTIONAL* name of the resource handle. Default is set to None.

        ROBOT USAGE:
            ${model}=          GET T     resource=r0   attribute=model
            ${arch} =        Set Variable If    '${ret}' == 'True'
            ${image} =   Get Package Name    release=${to_release}   model=${model}     package_type=occam  arch=${arch}

        :return: Name of the framed package name

        """
        release = str(release)
        model = str(model).lower()
        bit_type = arch
        if arch is None and resource_handle is not None:
            arch = resource_handle.get_package_architecture()
        arch = str(arch)
        major_release = re.match(r"^(\d+\.\d+)", release).group(1)
        # determine package prefix
        model_suffix = suffix
        prefix = ''
        suffix = ''

        if arch == 'ppc':
            prefix = 'jinstall-ppc'
        elif float(major_release) < 15.1:
            if arch == '64':
                prefix = 'jinstall64'
            else:
                prefix = 'jinstall'
        else:  # major_release >= 15.1
            if package_type == 'vmhost':
                prefix = 'junos-vmhost-install'
            elif package_type == 'occam':
                prefix = 'junos-install'
            elif package_type == 'jinstall' or package_type == 'jinstall-host':
                if re.search(r"mx|ex92", model):
                    prefix = 'junos-install'
                elif re.search(r"ex|qfx", model):
                    prefix = package_type
                    suffix = "-signed.tgz"
                elif re.search(r"srx|vsrx", model):
                    suffix = '.tgz'
                    if re.search(r"srx5\d\d\d|vsrx\d+", model):
                        prefix = 'junos-install'
                    elif re.search(r"srx[0-4]\d+|srx550m", model):
                        prefix = 'junos'

                else:
                    if arch == '64':
                        prefix = 'jinstall64'
                    else:
                        prefix = 'jinstall'
            elif package_type == 'evo':
                prefix = 'junos-evo-install'
            elif package_type == 'arm':
                if re.search(r"^ex\d+", model):
                    prefix = 'junos'
                elif re.search(r"^(r\d+|acx\d+)", model):
                    prefix = 'junos-install'
                suffix = '.tgz'
        #self.log_console("Prefix set to " + prefix)

        if model_suffix is not None:
            suffix = model_suffix

        # determine package suffix
        if not suffix:
            if prefix == 'jinstall' or prefix == 'jinstall64':
                suffix = '-domestic-signed.tgz'
            elif prefix == 'junos-install' or prefix == 'junos-vmhost':
                suffix = '.tgz'
            elif prefix == 'junos-upgrade':
                suffix = '-domestic.tgz'
            elif prefix == 'junos-evo-install':
                suffix = '.iso'
            else:
                suffix = '.tgz'
        if not re.search(r"^\.tgz", suffix) and not re.search(r"^-", suffix) and not re.search(r"^\.iso", suffix):
            suffix = '-' + suffix

        # put it all together
        package_name = ''

        if package_type == 'vmhost' and (
                re.search(r"mx(240|480|960|2008|2010|2020|10003|204|10008|10016)", model) or
                re.search(r"ptx(5000|1000|10002|10008|10016)", model) or
                re.search(r"acx(5448)", model)):
            #arch = "64";
            model_prefix = re.match(r"^(\D+)", model).group(1)
            package_name = prefix + '-' + model_prefix + '-x86-' + arch + '-' + release + suffix
        elif package_type == 'evo':
            if re.search(r"qfx(5220-128c|5220-32cd|5130-32cd)", model):
                model_prefix = re.match(r"^(\D+)", model).group(1)
                model_prefix = model_prefix + '-ms-fixed'
            elif re.search(r"qfx(10003)", model) or re.search(r"ptx(10003)", model):
                model_prefix = re.match(r"^(\D+)", model).group(1)
                model_prefix = model_prefix + '-fixed'
            else:
                model_prefix = re.match(r"^(\D+)", model).group(1)
            package_name = prefix + '-' + model_prefix + '-x86-' + arch + '-' + release + suffix
        elif package_type == 'arm':
            if re.search(r"^ex\d+", model):
                model_prefix = 'arm'
            elif re.search(r"^(r\d+|acx\d+)", model):
                model_prefix = 'acx-arm'
            package_name = prefix + '-' + model_prefix + '-' + arch + '-' + release + suffix
        elif re.search(r"^junos", prefix) and (
                re.search(r"mx(240|480|960|2008|2010|2020|10003|204|10008|10016)", model) or
                model.startswith('ex92') or
                re.search(r"^ptx(5000|1000|10002|10008|10016)", model), re.search(r"srx", model)):
            #arch = "32";
            if prefix == "junos-install":
                if re.search(r"srx5600|srx5400", model):
                    model_prefix = 'srx5000'
                elif re.search(r"vsrx3.0", model):
                    model_prefix = 'vsrx3'
                else:
                    model_prefix = re.match(r"^(\D+)", model).group(1)
                arch = '-x86-' + arch
            elif prefix == "junos":
                if re.search(r"srx1500", model):
                    model_prefix = 'srxentedge'
                    arch = '-x86-' + arch
                elif re.search(r"srx4600", model):
                    model_prefix = 'srxhe'
                    arch = '-x86-' + arch
                elif re.search(r"srx320|srx345|srx550m", model):
                    model_prefix = 'srxsme'
                    arch = ''
            package_name = prefix + '-' + model_prefix + arch + '-' + release + suffix
        elif re.search(r'^ex\d+', model):
            if re.search(r"^ex(4300-mp|4300-48mp)", model):
                match = re.search(r'^(ex)(\d+)-(\d+)?(.*)', model)
                model_prefix = match.group(1) + '-' + match.group(2) + match.group(4) + '-x86-' + arch
            else:
                match = re.search(r'^(ex)(\d+)', model)
                model_prefix = match.group(1) + '-' + match.group(2)
            package_name = prefix + '-' + model_prefix + '-' + release + suffix
        elif re.search(r'^qfx\d+', model):
            match = re.search(r'^(qfx)(\d+)', model)

            model_prefix = match.group(1) + '-'
            model_number = match.group(2)

            if re.search(r'^5100', model_number):
                model_prefix = model_prefix + '5-flex'
            elif re.search(r'^5\d+', model_number):
                model_prefix = model_prefix + '5e-flex'
            elif re.search(r'^10002', model_number):
                model_prefix = model_prefix + '10-f-flex'
            elif re.search(r'^10008', model_number):
                model_prefix = model_prefix + '10-m-flex'
            if bit_type is not None:
                model_prefix = model_prefix + '-x86-' + arch

            package_name = prefix + '-' + model_prefix + '-' + release + suffix

        if package_name == '':
            raise TobyException("Unsupported model (%s) to construct the package/image name" %model)

        self.log(level="INFO", message="Exiting 'get_package_name' with return value/code :\n"+str(package_name))
        return package_name

    def get_session_id(self):
        """
            Obtains unique session id - same as log subfolder
        """
        self.log(level="DEBUG", message="Inside get_session_id")
        if Vars().get_global_variable('${session_id}'):
            return Vars().get_global_variable('${session_id}')
        else:
            raise TobyException("No Session ID Available")


    def get_handle(self, resource, system_node=None, controller=None):
        """
        Get current connection handle

        ARGUMENTS:
            [resource, system_node=None, controller=None]

            :param STR resource:
                *MANDATORY* resource name of connection handle needed.
            :param STR system_node:
                *OPTIONAL* system_node name of connection handle needed.Default system_node is None
            :param STR controller:
                *OPTIONAL* controller name of connection handle needed.Default controller is None

        ROBOT USAGE:
                ${device0-dh} = Get Handle    resource=device0
                ${device0-dh} = Get Handle    resource=device0   system_node=current
                ${device0-dh} = Get Handle    resource=device0   controller=current
                ${device0-dh} = Get Handle    resource=device0   system_node=current   controller=current
                ${device0-dh} = Get Handle    resource=device0   system_node=primary   controller=re0
                ${device0-dh} = Get Handle    resource=device0   system_node=member1   controller=re0

        :return: Device/Node/Controller object
        """
        self.log(level='debug', message='Get the connection handle')
        if not isinstance(resource, str):
            raise TobyException("[Get Handle keyword usage error] Argument 'resource' type must be a string type but got "+(str(type(resource))))
        try:
            if system_node is None and controller is None:
                return_value = t['resources'][resource]['system']['dh']
            elif system_node is not None and controller is None:
                if system_node == 'current':
                    return_value = t['resources'][resource]['system']['dh'].current_node
                else:
                    return_value = t['resources'][resource]['system']['dh'].nodes[system_node]
            elif system_node is None and controller is not None:
                if controller == 'current':
                    return_value = t['resources'][resource]['system']['dh'].current_node.current_controller
                else:
                    return_value = t['resources'][resource]['system']['dh'].current_node.controllers[controller]
            else:
                if system_node == 'current':
                    if controller == 'current':
                        return_value = t['resources'][resource]['system']['dh'].current_node.current_controller
                    else:
                        return_value = t['resources'][resource]['system']['dh'].current_node.controllers[controller]
                else:
                    if controller == 'current':
                        return_value = t['resources'][resource]['system']['dh'].nodes[system_node].current_controller
                    else:
                        return_value = t['resources'][resource]['system']['dh'].nodes[system_node].controllers[controller]
            return return_value
        except KeyError as key_error:
            raise TobyException("Could not get Device object for resource:" +
                                resource + "\nError: " + str(key_error))

    def pause(self):
        """
            Allows users to pause in Robot
        """
        self.log_console('\n\nTest Suite Paused. Press  c <Enter>  to continue.\n')
        pdb.Pdb(stdout=sys.__stdout__).set_trace()

    def log(self, level=None, message=None, console=False):
        """
        Create a log entry

        ARGUMENTS:
            :param STR level:
                *OPTIONAL* log level. Eg: error,warn,info
            :param STR message:
                *MANDATORY* message to write to log
            :param BOOLEAN console:
                *OPTIONAL* prints to the console

        ROBOT USAGE:
            To simply log a message:

            Log     This is my message!

            To log to a particular level:

            Log     level=error   message=This is an error message!
            Log     level=warn    message=This is a warn message!

            In order to log to the console:

            Log     level=error   message=This is an error message!
            ...     console=True

            :return: None
        """
        if level is None and message is None:
            raise TobyException("Issued 'log' without arguments. t.log() Requires min 1 argument.")

        if level is not None and message is None:
            #User didn't pass in level; default to INFO
            message = level
            level = 'INFO'

        if type(message) is dict or type(message) is list:
            message = "\n" + pprint.pformat(message, indent=4)

        if self.is_robot:
            if self.robot_log_level:
                global_robot_log_level_int = getattr(logging, self.robot_log_level.upper())
                func_robot_log_level_int = getattr(logging, level.upper())
                if func_robot_log_level_int >= global_robot_log_level_int:
                    log_func = getattr(robot_logger, level.lower())
                    log_func(message)
                    if self.background_logger:
                        self.background_logger.write(message, level.upper())
            else:
                log_func = getattr(robot_logger, level.lower())
                log_func(message)
                if self.background_logger:
                    self.background_logger.write(message, level.upper())

        if isinstance(message, etree._Element):
            res = etree.tounicode(message, pretty_print=True)
            res = minidom.parseString(res).toprettyxml()
            message = res
        if not self.logger:
            if self.is_robot is True:
                self.logger = Logger(self._script_name, console=False)
            else:
                self.logger = Logger(self._script_name, console=True)

        if level.lower() == "warn" or level.lower() == "error":
            if console:
                console = False

        if self.console_log_flag == 'enable' or console:
            self.log_console(message=message, level=level)
        self.logger._log(getattr(logging, level.upper()), message, ())

    def log_console(self, message, level='INFO'):
        """
        Create a log entry on the console

        ARGUMENTS:
            [message]
            :param STR message:
                *MANDATORY* message to write to log

        ROBOT USAGE:
            Log Console    Your message goes here
            Log console    message = your message

        :return: None
        """
        level = logging.getLevelName(level.upper())
        if self.is_robot and level >= int(logging.getLogger().level):
            robot_misc = _Misc()
            robot_misc.log_to_console(message=message)
        else:
            print(message)

    def set_background_logger(self):
        """
           creates BackgroundLogger object
        """
        self.background_logger = BackgroundLogger()

    def process_background_logger(self, thread_name=None):
        """
           logs all the threads messages and then clears them
        """
        if self.background_logger is not None:
            self.log(self.background_logger.LOGGING_THREADS)
            if thread_name is not None:
                self.background_logger.log_background_messages(thread_name)
            else:
                self.background_logger.log_background_messages()
                self.background_logger.reset_background_messages()
                self.background_logger = None

    def get_system(self, resource=None):
        """
        Get System bundle

        ROBOT USAGE:
            ${system} = Get System    resource=device0

        Arguments:
            [resource=None]
            :param resource:
                *MANDATORY* resource name. Default resource is None

        :return: return system object
        """
        if resource is None:
            raise TobyException("Argument 'resource' is mandatory!")
        try:
            return t['resources'][resource]['system']
        except KeyError as error:
            self.log(level='error', message=str(error) + ' does not exists!')

    def get_resource_list(self, tag=None, all_data=False):
        """
        Get resource list from t object

        ARGUMENTS:
           [tag=None, all_data=False]
           :param STR tag:
               *OPTIONAL* tag name.Default is set to None
           :param BOOLEAN all_data:
               *OPTIONAL* all the data to inside resource.Default is set to False.
        ROBOT USAGE:
           @{resources} = Get Resource List
        :return: Resource object keys as list
        """
        self.log(level='debug', message='get the resource list')
        if tag:
            resource_list = list()
            if not isinstance(tag, list):
                tag = [tag]
            for resource in t['resources']:
                if 'tags' in t['resources'][resource]['system']['primary']:
                    resource_tag = t['resources'][resource]['system']['primary']['tags']
                    if set(list(set(resource_tag).intersection(tag))) == set(tag):
                        if all_data:
                            resource_list.append({resource: t['resources'][resource]})
                        else:
                            resource_list.append(resource)
            return resource_list
        else:
            if all_data:
                resource_list = list()
                for resource in t['resources']:
                    resource_list.append({resource: t['resources'][resource]})
                return resource_list
            else:
                return list(t['resources'].keys())

    def get_resource(self, resource=None):
        """
        Get resource from t object. Resource will have system & interfaces object

        ARGUMENTS:
            [resource=None]
            :param STR resource:
                *MANDATORY* resource name. Default resource is None

        ROBOT USAGE:
            @{resources} = Get Resources  resource=r0

        :return: Resource object keys as list.
        """
        if resource is None:
            raise TobyException("Argument 'resource' is mandatory!")
        try:
            return t['resources'][resource]
        except KeyError as error:
            self.log(level='error', message=str(error) + ' does not exists!')

    def get_interface_list(self, resource=None, tag=None, all_data=False):
        """
        Get interfaces as list

        ARGUMENTS:
            [resource=None, tag=None, all_data=False]

            :param STR resource:
                *OPTIONAL* resource name. Default resource is None
            :param STR tag:
                *OPTIONAL* tag name. Default tag is None
            :param BOOLEAN all_data:
                *OPTIONAL* all data inside the interface. Default all_data is False

        ROBOT USAGE:
            EX.1 @{intf} = Get Interface List    resource=device0
            EX.2 @{intf} = Get Interface List    resource=device0    tag=ae30     all_data=${true}

        :return: interface keys as list
        """
        self.log(level='debug', message='Get the interfaces as list')
        if tag:
            if not isinstance(tag, list):
                tag = [tag]
            if resource:
                interface_list = list()
                if 'interfaces' in t['resources'][resource]:
                    for interface in t['resources'][resource]['interfaces']:
                        if 'tags' in t['resources'][resource]['interfaces'][interface]:
                            interface_tag = t['resources'][resource]['interfaces'][interface]['tags']
                            if set(list(set(interface_tag).intersection(tag))) == set(tag):
                                if all_data:
                                    interface_list.append({interface: t['resources'][resource]['interfaces'][interface]})
                                else:
                                    interface_list.append(interface)
                return interface_list
            else:
                resource_list = list()
                for resource in t['resources']:
                    if 'interfaces' in t['resources'][resource]:
                        interface_list = list()
                        for interface in t['resources'][resource]['interfaces']:
                            if 'tags' in t['resources'][resource]['interfaces'][interface]:
                                interface_tag = t['resources'][resource]['interfaces'][interface]['tags']
                                if set(list(set(interface_tag).intersection(tag))) == set(tag):
                                    if all_data:
                                        interface_list.append({interface: t['resources'][resource]['interfaces'][interface]})
                                    else:
                                        interface_list.append(interface)
                        if interface_list:
                            resource_list.append({resource: interface_list})
                return resource_list
        else:
            if resource:
                if all_data:
                    interface_list = list()
                    if 'interfaces' in t['resources'][resource]:
                        for interface in t['resources'][resource]['interfaces']:
                            if all_data:
                                interface_list.append({interface: t['resources'][resource]['interfaces'][interface]})
                            else:
                                interface_list.append(interface)
                    return interface_list
                else:
                    return list(t['resources'][resource]['interfaces'].keys())
            else:
                resource_list = list()
                for resource in t['resources']:
                    if 'interfaces' in t['resources'][resource]:
                        interface_list = list()
                        for interface in t['resources'][resource]['interfaces']:
                            if all_data:
                                interface_list.append({interface: t['resources'][resource]['interfaces'][interface]})
                            else:
                                interface_list.append(interface)
                        resource_list.append({resource: interface_list})
                return resource_list

    def get_interface(self, resource=None, intf=None):
        """
        Get the interface for the specified resource.

        ARGUMENTS:
            [resource=None, intf=None]
            :param STR resource:
                *MANDATORY* resource name. Default resource is None.
            :param STR intf:
                *Optional* interface key value to be fetched. Default intf is None.

        ROBOT USAGE:
            ${intf_obj} = Get Interface    resource=device0   intf=intf0

        :return: interface object
        """
        self.log(level='debug', message='Get interface object for specified resource and interface')
        if resource is None:
            raise TobyException("Argument 'resource' is mandatory!")
        try:
            return t['resources'][resource]['interfaces'][intf]
        except KeyError:
            raise TobyException("Could not get interface for resource:" + resource + " interface:" + intf)

    def get_t_link(self, link):
        """
        Get interface link

        ARGUMENTS:
            [link]
            :param STR link:
                *MANDATORY* Link name.

        ROBOT USAGE:
            get t link    link=connect1

        :return: returns interface Link
        """
        self.log(level='debug', message='Get the T link')
        link_data = dict()
        for resource in t['resources']:
            if 'interfaces' in t['resources'][resource]:
                for interface in t['resources'][resource]['interfaces']:
                    if t['resources'][resource]['interfaces'][interface]['link'] == link:
                        if resource not in link_data:
                            link_data[resource] = []
                        link_data[resource].append(interface)
        return link_data

    def get_t(self, resource, system_node='primary', controller=None, interface=None, attribute=None, error_on_missing=True):
        """
        Generic accessor method to access data from t

        ARGUMENTS:
            [resource, system_node='primary', controller=None, interface=None, attribute=None, error_on_missing=True]

            :param STR resource:
                *MANDATORY* resource name one or more
            :param STR system_node:
                *OPTIONAL* node name, default system_node is Primary
            :param STR controller:
                *OPTIONAL* controller name. Default controller is None
            :param STR interface:
                *OPTIONAL* interface name. Default interface is None.
            :param STR attribute:
                *OPTIONAL* attribute Name. Default attribute is None.
            :param BOOLEAN error_on_missing:
                *OPTIONAL* error_on_missing will be True or False, Default error_on_missing is True.

        ROBOT USAGE:
            ${data} =  Get T     resource=r0
            ${data} =  Get T     resource=r0    system_node='PRIMARY'
            ${intf_name} =    GET T     resource=r3    interface=intf${INDEX}     attribute=pic
                .... system_node='PRIMARY'    error_on_missing=${False}

        :return: data from t
        """
        if interface is None:
            if type(resource) is tuple:
                system_data = dict()
                for resource_name in resource:
                    system_data[resource_name] = self._get_system(resource=resource_name, system_node=system_node,\
                            controller=controller, attribute=attribute, error_on_missing=error_on_missing)
                return_value = system_data
            else:
                return_value = self._get_system(resource=resource, system_node=system_node, controller=controller, \
                            attribute=attribute, error_on_missing=error_on_missing)
        else:
            if type(interface) is tuple:
                interface_data = dict()
                for interface_name in interface:
                    interface_data[interface_name] = self._get_interface(resource=resource, interface=interface_name, \
                            attribute=attribute, error_on_missing=error_on_missing)
                return_value = interface_data
            else:
                return_value = self._get_interface(resource=resource, interface=interface, attribute=attribute, \
                            error_on_missing=error_on_missing)
        return return_value

    def _get_system(self, resource, system_node, controller, attribute, error_on_missing=True):
        """
            Private accessor method to fetch data under system block
        :param resource:
        :param system_node:
        :param controller:
        :param attribute:
        :return:
        """
        if controller is None:
            if attribute is None:
                try:
                    return_value = t['resources'][resource]['system'][system_node]
                except KeyError:
                    if error_on_missing:
                        raise TobyException("Could not get system_node: '%s' for resource: '%s'" % (system_node, resource))
                    else:
                        self.log(level="DEBUG",
                                 message="Could not get system_node: '%s' for resource: '%s'. Returning value as 'None'"
                                 % (system_node, resource))
                        return_value = None
            else:
                try:
                    return_value = t['resources'][resource]['system'][system_node][attribute]
                except KeyError:
                    if error_on_missing:
                        raise TobyException("Could not get attribute: '%s' in system_node: '%s' for resource: '%s'"
                                            % (attribute, system_node, resource))
                    else:
                        self.log(level="DEBUG", message="Could not get attribute: '%s' in system_node: '%s' for resource: "
                                                       "'%s'. Returning value as 'None'" % (attribute, system_node, resource))
                        return_value = None
        else:
            if attribute is None:
                try:
                    return_value = t['resources'][resource]['system'][system_node]['controllers'][controller]
                except KeyError:
                    if error_on_missing:
                        raise TobyException("Could not get controller: '%s' in system_node: '%s' for resource: '%s'"
                                            % (controller, system_node, resource))
                    else:
                        self.log(level="DEBUG", message="Could not get controller: '%s' in system_node: '%s' for resource: "
                                                       "'%s'. Returning value as 'None'" %(controller, system_node, resource))
                        return_value = None
            else:
                try:
                    return_value = t['resources'][resource]['system'][system_node]['controllers'][controller][attribute]
                except KeyError:
                    if error_on_missing:
                        raise TobyException("Could not get attribute: '%s' in controller: '%s' in system_node: '%s'"
                                            " for resource: '%s'" %(attribute, controller, system_node, resource))
                    else:
                        self.log(level="DEBUG", message="Could not get attribute: '%s' in controller: '%s' in system_node: '%s'"
                                                       " for resource: '%s'. Returning value as 'None'" %(attribute, controller, system_node, resource))
                        return_value = None
        return return_value

    def _get_interface(self, resource, interface, attribute, error_on_missing=True):
        """
            Private accessor method to fetch data under interfaces block
        :param resource:
        :param interface:
        :param attribute:
        :return:
        """
        if attribute is None:
            try:
                return t['resources'][resource]['interfaces'][interface]
            except KeyError:
                if error_on_missing:
                    raise TobyException("Could not get interface: '%s'  for resource: '%s'" %(interface, resource))
                else:
                    self.log(level="DEBUG", message="Could not get interface: '%s'  for resource: '%s'"
                                                   ". Returning value as 'None'" %(interface, resource))
                    return None
        else:
            try:
                return t['resources'][resource]['interfaces'][interface][attribute]
            except KeyError:
                if error_on_missing:
                    raise TobyException("Could not get attribute: '%s' in interface: '%s' for resource: '%s'"
                                        %(attribute, interface, resource))
                else:
                    self.log(level="DEBUG", message="Could not get attribute: '%s' in interface: '%s' for resource: '%s'"
                                                   ". Returning value as 'None'" %(attribute, interface, resource))
                    return None

    def __getitem__(self, key):
        return self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __repr__(self):
        return repr(self.__dict__)

    def get_interfaces_name(self, resource, tags=None):
        """
            Get all the interfaces pic name associated with the resource in t topology.

            DESCRIPTION:

                Get all the interfaces pic name associated with the resource in t topology.
                Optional tags to get list of interface names based on tag contents.

            ARGUMENTS:
                [resource, tags=None]
                :param STR resource:
                    * MANDATORY* logical name of the resource
                :param STR tags:
                    * OPTIONAL* interface tag contents.Default tags is None.


            ROBOT USAGE:
                Ex. 1: Get the interfaces pic name associated with all the interfaces in t topology
                @{intf} = Get Interfaces Name     resource=r0

                Ex. 2: Get the interfaces pic name associated with the interfaces filtered
                        by interface tag contents
                NOTE : Do not enclose tags in quotes while passing it as STRING as shown below
                @{intf} = Get Interfaces Name    resource=r0    tags=abc

                Ex. 3: Get the interfaces pic name associated with the interfaces filtered
                         by interface tag contents as LIST
                @{value} =   Create List  ae0child     ae03
                @{intf} =   Get Interfaces Name    resource=router0    tags=@{value}

                Ex. 4 Get the interfaces pic name associated with the interfaces
                     filtered by interface tag contents as LIST
                @{value} =   Create List  ae0child     ae03
                @{intf} =   Get Interfaces Name    resource=router0    tags=@{value}

            :return: Returns the list of interfaces that belongs to the resource name passed
        """
        self.log(level="DEBUG", message='get the interface names from interfaces block')
        self.log(level="DEBUG", message=tags)
        intf_list = list()
        if resource in t['resources']:
            if 'interfaces' in t['resources'][resource]:
                for interface in t['resources'][resource]['interfaces']:
                    if tags is not None:
                        data = set()
                        if isinstance(tags, str):
                            data.add(tags)
                        elif isinstance(tags, list):
                            data = set(tags)
                        if 'tags' in t['resources'][resource]['interfaces'][interface] and len(set(t['resources'][resource]['interfaces'][interface]['tags']).intersection(data)) > 0:
                            intf = t['resources'][resource]['interfaces'][interface]['pic']
                            intf_list.append(intf)
                    else:
                        intf = t['resources'][resource]['interfaces'][interface]['pic']
                        intf_list.append(intf)
        if intf_list:
            return intf_list


    def get_junos_resources(self):
        """
        Get all junos resource list

        ARGUMENTS:
            []

        ROBOT USAGE:
            @{junos_res} =  Get Junos Resources

        :return: Returns the logical resource names of the junos devices
        """
        junos_res = []
        res_list = self.get_resource_list()

        for res in res_list:
            if t['resources'][res]['system']['primary']['osname'].upper() == 'JUNOS':
                junos_res.append(res)
        return junos_res

    def core_info(self):
        """
            Dumps the core details found
        """
        if t.core and t._stage in t.core:
            import json
            self.log(level='WARN', message="Core details found @stage(%s) : %s" %(t._stage, json.dumps(t.core[t._stage], indent=4, sort_keys=True)))
            self.log(level='INFO', message="Toby_Core_Dump | %s | Toby_Core_Dump" %json.dumps(t.core[t._stage], sort_keys=True))

    def get_core_list_from_device(self, resource=None, core_path=None):
        """
        print core list from the device

        ARGUMENTS:
            [resource=None, core_path=None]

            :param STR core_path
            *OPTIONAL* Path as a list ( where cores to be found). Default core_path is
                  '/var/crash/*core*' , '/var/tmp/*core*', '/var/tmp/pics/*core*'

            :param STR resource
            *OPTIONAL* Logical name of the resource. If not passed,
                       detect_core will be performed on all junos devices
                       based on "core-check" enabled in yaml file

        ROBOT USAGE
            ${data} =  Get Core List From Device
            ${data} =  Get Core List From Device      resource=r0
            ${data} =  Get Core List From Device      resource=r0     core_path=/var/crash/*core*


        :return: Return the core list from the device
        """
        system_name = t.get_t(resource=resource, attribute='name')
        if resource in t['resources']:
            system = t['resources'][resource]['system']
            hostname = system['dh'].current_node.current_controller.get_host_name()
        self.log(level="DEBUG", message="Gathering core list from device: " + resource + "[" + system_name + "]")

        if hasattr(t, 'cores'):
            if system_name in t.cores.keys():
                self.log(level="DEBUG", message="core_full_path_list of resource : " + resource + "is" + str(t.cores[system_name][hostname]['core_full_path_list']))
                return t.cores[system_name][hostname]['core_full_path_list']
        return False

    def get_core_count_from_device(self, resource=None, core_path=None):
        """
        Get the core count from the device

        ARGUMENTS:
            [resource=None, core_path=None]

            :param STR core_path
            *OPTIONAL* Path as a list ( where cores to be found). Default core_path is
               '/var/crash/*core*' , '/var/tmp/*core*', '/var/tmp/pics/*core*'

            :param STR resource
             *OPTIONAL* Logical name of the resource. If not passed,
                        detect_core will be performed on all junos devices
                        based on "core-check" enabled in yaml file.
                        Default is set to None.

        ROBOT USAGE:
            ${data} =   Get Core Count From Device
            ${data} =   Get Core Count From Device     resource=r0
            ${data} =   Get Core Count From Device     resource=r0
                        ...          core_path=/var/crash/*core*

        :return: Return the core count from the device
        """
        system_name = t.get_t(resource=resource, attribute='name')
        if resource in t['resources']:
            system = t['resources'][resource]['system']
            hostname = system['dh'].current_node.current_controller.get_host_name()
        self.log(level="DEBUG", message="Getting core count from device: " + resource + "[" + system_name + "]")
        if hasattr(t, 'cores'):
            if system_name in t.cores.keys():
                return len(t.cores[system_name][hostname]['core_full_path_list'])
        return 0

    def detect_core_on_junos_device(self, core_path=None, resource=None):
        """
        Detect core on all junos devices

        ARGUMENTS:
            [core_path=None, resource=None]
            :param STR core_path
            *OPTIONAL* Path as a list ( where cores to be found). Default core_path is
            '/var/crash/*core*' , '/var/tmp/*core*', '/var/tmp/pics/*core*'
            :param STR resource
            *OPTIONAL* Logical name of the resource. If not passed,
            detect_core will be performed on all junos devices based on "core-check" enabled in yaml file

        ROBOT USAGE:
            ${data} =  Detect Core On Junos Device
            ${data} =  Detect Core On Junos Device       core_path=/var/tmp/pics/*core*
            ${data} =  Detect Core On Junos Device       core_path=/var/tmp/pics/*core*    resource=r0

        :return: Return True (if core is found) otherwise False. Return value will be a list
        """
        junos_res = []
        if resource is None:
            junos_res = self.get_junos_resources()
        else:
            if resource in self.get_junos_resources():
                junos_res = [resource]
            else:
                raise TobyException("Could not get resource:" + resource + " as JunOS.")

        list_of_dicts = []
        for junos_key in junos_res:
            if 'core-check' in t['resources'][junos_key]['system']['primary'] and \
                            t['resources'][junos_key]['system']['primary']['core-check'] == 'enable':
                handle = self.get_handle(resource=junos_key)
                if core_path is not None:
                    list_of_dicts.append(
                        {'fname': handle.detect_core, 'kwargs': {'core_path': core_path, 'resource': junos_key}})
                else:
                    list_of_dicts.append(
                        {'fname': handle.detect_core, 'kwargs': {'resource': junos_key}})

        if list_of_dicts:
            core_result = run_multiple(list_of_dicts)
            self.core_info()
            return core_result

    def _device_response_check(self, resource=None):
        if 'framework_variables' in self and 'fv-device-response-check' in self['framework_variables']:
            if self['framework_variables']['fv-device-response-check'] == 'disable':
                return True
        self.log(level="DEBUG", message="Enabling device response check")
        import jnpr.toby.frameworkDefaults.credentials as credentials
        dict_instr = yaml.safe_load(open(os.path.join(os.path.dirname(credentials.__file__),\
                               "device_response_check.yaml")))
        junos_res = []
        junos_res = self.get_junos_resources()
        for junos_key in junos_res:
            dev_handle = self.get_handle(resource=junos_key)
            for node_name in dev_handle.nodes:
                for controller_name in dev_handle.nodes[node_name].controllers.keys():
                    setattr(dev_handle.nodes[node_name].controllers[controller_name], 'response_instructions', dict_instr)

    def keys(self):
        """
            When t called like dictionary with no keys, use this keys() instead

            :param NONE
            :return: Keys of t
        """
        return self.__dict__.keys()

    def save_current_config(self, resource=None, config_id=None):
        """
        saves the configuration with the <script_name>_id_pid.conf

        DESCRIPTION:
            This saves the configuration with the <script_name>_id_pid.conf
            on all junos resources or on specified resource_device

        ARGUMENTS:
            [resource=None, config_id=None]
            :param STR resource:
            *OPTIONAL* logical name of the resource.
                      If this argument is not passed then it saves
                      config on all junos resources
            :param STR config_id:
            *Optional* unique identifier for the file.
                       If not passed, id will be set to PID

        ROBOT USAGE:
            save current config      resource=r<n>    id=125
            save current config      id=123
            save current config      resource=r<n>
            save current config

        :returns: True if saving the configuration is successful,
                                      else an Exception is raised
        """
        pid = os.getppid()
        if config_id is None:
            config_id = pid

        file = self._script_name + '_' + str(config_id) + '_' + str(pid) + '.conf'

        junos_res = []
        if resource is None:
            junos_res = self.get_junos_resources()
        else:
            if resource in self.get_junos_resources():
                junos_res = [resource]
            else:
                raise TobyException("Could not get resource:" + resource + " as JunOS.")

        for junos_key in junos_res:
            handle = self.get_handle(resource=junos_key)
            handle.save_current_config(file=file)
        return True

    def load_saved_config(self, resource=None, config_id=None):
        """
        loads the configuration from the file (<script_name>_id_pid.conf)

        DESCRIPTION:
            This loads the configuration from the file (<script_name>_id_pid.conf)
            on all junos resources or specified resource

        ARGUMENTS:
            [resource=None, config_id=None]

            :param STR resource
            *OPTIONAL* logical name of the resource. If this argument is not passed
                        then it loads saved config on all junos resources
            :param STR config_id:
            *Optional* unique identifier for the file. If not passed, id will be set to PID

        ROBOT USAGE:
            load saved config        resource=r<n>     id=125
            load saved config        resource=r<n>
            load saved config        id=123
            load saved config

        :returns: True if loading the configuration is successful, else an Exception is raised
        """
        pid = os.getppid()
        if config_id is None:
            config_id = pid

        file = self._script_name + '_' + str(config_id) + '_' + str(pid) + '.conf'

        junos_res = []
        if resource is None:
            junos_res = self.get_junos_resources()
        else:
            if resource in self.get_junos_resources():
                junos_res = [resource]
            else:
                raise TobyException("Could not get resource:" + resource + " as JunOS.")
        for junos_key in junos_res:
            handle = self.get_handle(resource=junos_key)
            handle.load_saved_config(file=file)
        return True

    def _load_baseline_config(self, config_timeout=None):
        """
            This loads the config file on the device in suite setup state
            on all or specified resource from the user location or default path(/var/tmp/baseline-config.conf)
            :Returns: True if loading the configuration is successful, else an Exception is raised
        """
        junos_res = []
        junos_res = self.get_junos_resources()

        for junos_key in junos_res:
            if 'load-baseline-config-from' in t['resources'][junos_key]['system']['primary'] and \
                    t['resources'][junos_key]['system']['primary']['load-baseline-config-from'].upper() != "NONE":
                if 'fv-connect-controllers' in t['resources'][junos_key]['system']['primary'] and \
                    re.search('none', t['resources'][junos_key]['system']['primary']['fv-connect-controllers'], re.I):
                    continue
                load_config_from = t['resources'][junos_key]['system']['primary']['load-baseline-config-from']

                if load_config_from == "default":
                    load_config_from = '/var/tmp/baseline-config.conf'

                if 'load-baseline-config-timeout' in t['resources'][junos_key]['system']['primary']:
                    config_timeout = t['resources'][junos_key]['system']['primary']['load-baseline-config-timeout']

                handle = self.get_handle(resource=junos_key)
                self.log(level="DEBUG", message="Loading baseline configuration for "+ str(junos_key))
                handle.load_baseline_config(load_config_from=load_config_from, config_timeout=config_timeout)

        return True

    def check_interface_status(self):
        """
        keyword used to check the interface status on all JUNOS devices.

        DESCRIPTION:
            'Check Interface Status' is a keyword used to check the interface status
             on all JUNOS devices.

        ARGUMENTS:
            []

        ROBOT USAGE:
            Ex. Running Check Interface Status on the all the available devices in the Topology.yaml file
            ${response} =  Check Interface Status

        returns: True if all the interfaces are Up, else raises an Exception.
        """
        junos_res = list()
        junos_res = self.get_junos_resources()

        list_of_dicts = list()
        for junos_key in junos_res:
            if 'interface-status-check' in t['resources'][junos_key]['system']['primary'] and \
                     t['resources'][junos_key]['system']['primary']['interface-status-check'] == 'enable':
                if 'fv-connect-controllers' in t['resources'][junos_key]['system']['primary'] and \
                    re.search('none', t['resources'][junos_key]['system']['primary']['fv-connect-controllers'], re.I):
                    continue
                interfaces = self.get_interfaces_name(resource=junos_key)
                self.log(level="info", message='interfaces' + str(interfaces))

                if interfaces:
                    handle = self.get_handle(resource=junos_key)
                    list_of_dicts.append(
                        {'fname': handle.check_interface_status, 'kwargs':{'interfaces': interfaces}})
                else:
                    raise TobyException('Interfaces are not found in yaml file for the resource ' + str(junos_key))

        if list_of_dicts:
            result = run_multiple(list_of_dicts)
            self.log(level="info", message='result' + str(result))
            if False in result:
                raise TobyLinkFail('One or more interfaces are down OR the interfaces are not found in the router')

        return True

    def _monitoring_engine_init(self):
        if 'framework_variables' in self and self['framework_variables'] is not None and 'fv-monitoring-engine' in self['framework_variables']:
            try:
                self.monitor = BuiltIn().get_library_instance('MonitoringEngine')
            except:
                from jnpr.toby.engines.monitor.MonitoringEngine import MonitoringEngine
                self.monitor = MonitoringEngine()

            interval = 5
            infile = 'monitor.yaml'
            kw_options = self['framework_variables']['fv-monitoring-engine'].split(':')
            kw_args = {}
            for key_value in kw_options:
                if '=' in key_value:
                    option = key_value.split('=')
                    kw_args[option[0]] = option[1]

            self.monitor.monitoring_engine_start_monitor(**kw_args)

    def _macro_engine_init(self):
        if 'framework_variables' in self and self['framework_variables'] is not None \
          and 'fv-macro-engine' in self['framework_variables']:
            t.log_console('Initializing Macro Engine')
            macro_instr = self['framework_variables']['fv-macro-engine']
            from jnpr.toby.engines.macro.cmd_macro import cmd_macro
            cb_obj = cmd_macro()
            cb_obj.run_macros_on_failure(**macro_instr)

    def _monitoring_engine_close(self):
        if 'framework_variables' in self and self['framework_variables'] is not None and 'fv-monitoring-engine' in self['framework_variables']:
            self.monitor.monitoring_engine_stop_monitor()

    def _code_coverage_init(self):

        if 'framework_variables' in self and self['framework_variables'] is not None and 'code_coverage' in self['framework_variables']:
            cc_params = {}
            registration_data = dict()
            filters = dict()
            component = []
            code_coverage_objects = dict()
            ft_code_coverage_objects = dict()

            self.log(level="INFO", message="Code coverage is enabled of the script")
            from jnpr.codecoverage.codecoverage import CodeCoverage, FtCodeCoverage
            cc_params = self['framework_variables']['code_coverage']
            self.log(level='DEBUG', message="code coverage inputss: %s" % cc_params)
            t.ft_code_coverage = False
            t.code_coverage = False
            daemons = None
            sandbox_path = None
            sandbox_host = None
            gcov_prefix = None
            profile_id = None
            test_script_id = None
            script_path = None
            filters = None
            ignore_warnings = None
            data_registration = None
            location = None
            if  'registration' in self['framework_variables']['code_coverage']:
                registration_data = self['framework_variables']['code_coverage']['registration']
            if 'filters' in self['framework_variables']['code_coverage']:
                filters = self['framework_variables']['code_coverage']['filters']
            if 'data_registration' in self['framework_variables']['code_coverage']:
                data_registration = self['framework_variables']['code_coverage']['data_registration']
            if 'component' in self['framework_variables']['code_coverage']:
                component = self['framework_variables']['code_coverage']['component']
            if 'ignore_warnings' in self['framework_variables']['code_coverage']:
                ignore_warnings = self['framework_variables']['code_coverage']['ignore_warnings']
            if 'daemons' in self['framework_variables']['code_coverage']:
                daemons = self['framework_variables']['code_coverage']['daemons']
            if 'data_path' in self['framework_variables']['code_coverage']:
                data_path = self['framework_variables']['code_coverage']['data_path']
            if 'sandbox_path' in self['framework_variables']['code_coverage']:
                sandbox_path = self['framework_variables']['code_coverage']['sandbox_path']
            if 'sandbox_host' in self['framework_variables']['code_coverage']:
                sandbox_host = self['framework_variables']['code_coverage']['sandbox_host']
            if 'gcov_prefix' in self['framework_variables']['code_coverage']:
                gcov_prefix = self['framework_variables']['code_coverage']['gcov_prefix']
            if 'profile_id' in self['framework_variables']['code_coverage']:
                profile_id = self['framework_variables']['code_coverage']['profile_id']
            if 'test_script_id' in self['framework_variables']['code_coverage']:
                test_script_id = self['framework_variables']['code_coverage']['test_script_id']
            if 'script_path' in self['framework_variables']['code_coverage']:
                script_path = self['framework_variables']['code_coverage']['script_path']
            else:
                script_path = BuiltIn().get_variable_value('${SUITE_SOURCE}')
            if 'location' in self['framework_variables']['code_coverage']:
                location = self['framework_variables']['code_coverage']['location'].lower()
            activity_type = registration_data.pop('activity_type')
            if 'rli' in registration_data:
                registration_data['rli'] = int(registration_data['rli'])
            if 'rli_number' in registration_data:
                registration_data['rli_number'] = int(registration_data['rli_number'])
            if 'PR' in registration_data:
                registration_data['PR'] = int(registration_data['PR'])
            if 'user_id' in self['framework_variables']['code_coverage']:
                registration_data['user_id'] = self['framework_variables']['code_coverage']['user_id']
            else:
                client_os = platform.system()
                if client_os == 'Windows':
                    registration_data['user_id'] = os.environ.get('USERNAME', '')
                else:
                    registration_data['user_id'] = pwd.getpwuid(os.getuid()).pw_name
        else:
            return True

        if component:
            if 'ft_cov' in component:
                #setattr(self, 'FT_COVERAGE', component['ft_cov'])
                t.ft_code_coverage = component['ft_cov']
            if 'gcov' in component:
                #setattr(self, 'GCOV_COVERAGE', component['gcov'])
                t.code_coverage = component['gcov']

        if t.code_coverage :
            ### Validating and setting gcov data path
            ### Gcov attributes validation
            registration_updated = dict()
            if (data_path is not None and not re.match(r'^\/volume\/(cbrimage*|testtech*)', data_path)) or data_path is None:
                result_hash = CodeCoverage.get_gcov_data_path(activity_type, location=location, **registration_data)
                if result_hash:
                    registration_updated = result_hash
                    data_path = registration_updated['gcov_data_path']
                    self.log(level="info", message="Gcov data path set to : %s" % data_path)
                else:
                    self.log(level="error", message="could not get gcov data path: %s" % result_hash['msg'])
                    return False
            else:
                result_hash = CodeCoverage.cc_attributes_valiation(activity_type, location=location, **registration_data)
                if result_hash:
                    self.log(level="info", message="Code coverage attributes validation success")
                    registration_updated = result_hash
                else:
                    self.log(level="error", message="Code coverage attributes validation failed")
                    return False

        ### Filter code coverage devices before creating code coveage objects
        code_coverge_device_list = None
        if filters is not None and len(filters.keys()) > 0:
            router_list = t.get_junos_resources()
            code_coverge_device_list = CodeCoverage.filter_coverage_routes(router_list, filters)
        else:
            code_coverge_device_list = t.get_junos_resources()

        if len(code_coverge_device_list) > 0:
            self.log(level="DEBUG", message="Router selected for code coverage")
            self.log(level="DEBUG", message="%s" % code_coverge_device_list)
        else:
            self.log(level="warn", message="No routers selected for code coverage")
            return False

        registration_data['activity_type'] = activity_type
        cc_inputs = {'registration':registration_data, 'code_coverage':True, \
                     'component':t.code_coverage, 'ignore_warnings':ignore_warnings, \
                     'daemons':daemons, 'data_path': data_path, 'sandbox_path':sandbox_path,\
                     'data_registration':data_registration, 'sandbox_host':sandbox_host, \
                     'gcov_prefix':gcov_prefix, 'profile_id':profile_id, 'test_script_id':test_script_id, 'script_path' : script_path}
        ft_cc_inputs = { 'component':t.ft_code_coverage, 'ft_code_coverage': True, \
                         'data_path': data_path, 'profile_id':profile_id, 'test_script_id':test_script_id, \
                         'script_path' : script_path}
        self.log(level="info", message="Creating code coverage objects")
        for junos_key in code_coverge_device_list:
            router_handle = t.get_handle(resource=junos_key)
            system_info = t.get_resource(resource=junos_key)
            model = router_handle.get_model()
            if t.code_coverage:
                code_coverage_objects[junos_key] = dict()
            if t.ft_code_coverage:
                ft_code_coverage_objects[junos_key] = dict()
            for node_name in router_handle.nodes.keys():
                for controller_name in router_handle.nodes[node_name].controllers.keys():
                    controller_handle = router_handle.nodes[node_name].controllers[controller_name]
                    cc_inputs['device_info'] = system_info
                    if t.code_coverage:
                        coverage_obj = CodeCoverage(controller_handle, model, **cc_inputs)
                        code_coverage_objects[junos_key][controller_name] = coverage_obj
                    if t.ft_code_coverage:
                        ft_coverage_obj = FtCodeCoverage(controller_handle, model, **ft_cc_inputs)
                        ft_code_coverage_objects[junos_key][controller_name] = ft_coverage_obj

        if len(code_coverage_objects.keys()) > 0:
            self.log(level="INFO", message="Invoking code coverage initialize for all routers")
            result = CodeCoverage.code_coverage_initialize(code_coverage_objects)
            if result:
                self.log(level="INFO", message="Code Coverage initialization successfull")
                t.codecoverage_dict['objects'] = code_coverage_objects
                t.codecoverage_dict['registration_data'] = registration_updated
                t.codecoverage_dict['location'] = location
                return (code_coverage_objects, registration_updated)
            else:
                self.log(level="ERROR", message="Code Coverage initialization Failed")
                return False
        if len(ft_code_coverage_objects.keys()) > 0:
            self.log(level="INFO", message="Invoking functional code coverage initialize for all routers")
            result = FtCodeCoverage.ft_code_coverage_initialize(ft_code_coverage_objects)
            if result:
                self.log(level="INFO", message="Functional Code Coverage initialization successfull")
                t.ft_codecoverage_dict['objects'] = ft_code_coverage_objects
                return True
            else:
                self.log(level="ERROR", message="Code Coverage initialization Failed")
                return False

    def _code_coverage_dump(self):
        testcase_info = {}
        if (hasattr(t, 'code_coverage') and t.code_coverage) or \
           (hasattr(t, 'ft_code_coverage') and t.ft_code_coverage):
            self.log(level="info", message="Inside _code_coverage_dump %s" % t.code_coverage)
            _builtin = BuiltIn()
            suite_name = _builtin.get_variable_value("${TEST_NAME}")
            suite_status = _builtin.get_variable_value('${TEST_STATUS}')
            testcase_info = {'tc': suite_name, 'tc_result': suite_status}
            from jnpr.codecoverage.codecoverage import CodeCoverage, FtCodeCoverage
        else:
            return True
        if 'collect_gcov_data_for' in t['framework_variables']['code_coverage']:
            collect_gcov_data_for = t['framework_variables']['code_coverage']['collect_gcov_data_for']
            if testcase_info['tc_result'] not in collect_gcov_data_for:
                self.log(level="INFO", message="Gcov data enabled only for %s" % collect_gcov_data_for)
                self.log(level="INFO", message="Skipping gcov dump for testcase %s" % testcase_info['tc'])
                return True
        if t.code_coverage:
            code_coverage_objects = self.codecoverage_dict['objects']
            registration_data = self.codecoverage_dict['registration_data']
            location = self.codecoverage_dict['location']
            result = CodeCoverage.code_coverage_dump(code_coverage_objects, testcase_info)
            if result:
                data_registration = t['framework_variables']['code_coverage']['data_registration']
                if data_registration:
                    reg_result = CodeCoverage.register_coverage_data(code_coverage_objects, registration_data, location=location)
                    if reg_result:
                        self.log(level="DEBUG", message="Gcov data registration successfull")
                    else:
                        self.log(level="ERROR", message="registration failed")
                else:
                    self.log(level="DEBUG", message="Gcov registration is not enabled, skipping registration")
            else:
                self.log(level="ERROR", message="Code coverage dump failed")

        if t.ft_code_coverage:
            ft_code_coverage_objects = self.ft_codecoverage_dict['objects']
            ft_result = FtCodeCoverage.ft_code_coverage_dump(ft_code_coverage_objects, testcase_info)
            if ft_result:
                self.log(level="INFO", message="Functional coverage data dump successfull")
            else:
                self.log(level="ERROR", message="Functional coverage data dump failed")


    def _code_coverage_close(self):
        testcase_info = {}
        if (hasattr(t, 'code_coverage') and t.code_coverage) or \
            (hasattr(t, 'ft_code_coverage') and t.ft_code_coverage):
            self.log(level="info", message="In _code_coverage_close %s" % t.code_coverage)
            _builtin = BuiltIn()
            suite_name = _builtin.get_variable_value("${SUITE_NAME}")
            suite_status = _builtin.get_variable_value('${SUITE_STATUS}')
            testcase_info = {'tc': suite_name, 'tc_result': suite_status}
            from jnpr.codecoverage.codecoverage import CodeCoverage, FtCodeCoverage
        else:
            return True
        if t.code_coverage:
            code_coverage_objects = self.codecoverage_dict['objects']
            registration_data = self.codecoverage_dict['registration_data']
            result = CodeCoverage.code_coverage_close(code_coverage_objects, testcase_info)
            if result:
                data_registration = t['framework_variables']['code_coverage']['data_registration']
                if data_registration:
                    reg_result = CodeCoverage.register_coverage_data(code_coverage_objects, registration_data)
                    if reg_result:
                        self.log(level="INFO", message="Gcov data registration successfull")
                    else:
                        self.log(level="ERROR", message="registration failed")
                else:
                    self.log(level="INFO", message="Gcov registration is not enabled, skipping registration")
            else:
                self.log(level="error", message="Code coverage dump failed")
        if t.ft_code_coverage:
            ft_code_coverage_objects = self.ft_codecoverage_dict['objects']
            ft_result = FtCodeCoverage.ft_code_coverage_close(ft_code_coverage_objects, testcase_info)
            if ft_result:
                self.log(level="INFO", message="Functional code coverage dump successfull")
            else:
                self.log(level="ERROR", message="Functional code coverage dump failed")

    def _ft_code_coverage_data_initialize(self):
        testcase_info = {}
        if (hasattr(t, 'ft_code_coverage') and t.ft_code_coverage):
            self.log(level="info", message="Inside _ft_code_coverage_data_initialize %s" % t.ft_code_coverage)
            sys.path.append('/homes/sreenig/codecoverage_sb/code-coverage/lib')
            from jnpr.codecoverage.codecoverage import FtCodeCoverage
        else:
            return True
        if t.ft_code_coverage:
            ft_code_coverage_objects = self.ft_codecoverage_dict['objects']
            ft_result = FtCodeCoverage.ft_code_coverage_data_initialize(ft_code_coverage_objects)
            if ft_result:
                self.log(level="INFO", message="Functional coverage data initialize successfull")
            else:
                self.log(level="error", message="Functional coverage data initialize failed")

    def _reset_jpg_config(self):
        """
        reset_jpg_config
        """
        for resource_name in self.t_dict['resources']:
            system = self.t_dict['resources'][resource_name]['system']
            if system['primary']['osname'].upper() == 'JUNOS' and str(system['primary']['model']).upper() == 'JPG':
                system['dh'].current_node.current_controller.set_jpg_interfaces(
                    intf=self.t_dict['resources'][resource_name]['interfaces'])
                system['dh'].current_node.current_controller.reset_jpg_config()

