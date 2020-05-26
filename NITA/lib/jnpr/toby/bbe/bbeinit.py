# Copyright 2016- Juniper Networks
# Toby BBE development team

""" This module initializes Toby BBE.

Refer to BBEInit.bbe_initialize for detail usage information.
"""

import re
import os
import datetime
import yaml
from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.bbe.bbevar.bbevars import BBEVars
from jnpr.toby.bbe.errors import BBEInitError
from jnpr.toby.bbe.version import get_bbe_version, log_bbe_version


__author__ = ['Yong Wang']
__credits__ = ['Benjamin Schurman']
__contact__ = 'ywang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()

YAML_BBE_ROOT_KEY = 'bbevar'    # root key in BBE configuration yaml file
T_BBE_KEY = 'uv-bbevar' # merged yaml file with bbe feature key
BBE_VAR = '${bbevar}'  # global bbe variable name
BBE_CONFIG_FILE_POSTFIX_DEFAULT = '.cfg.yaml'   # e.g., xyz.cfg.yaml


class BBEInit:
    """Initializes Toby BBE.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """Initializee.

        BBE initialization functions are mostly performed by bbe_initialize.
        """
        self.log_tag = '[BBEINIT]'

    def bbe_initialize(self, config_file=None):
        """Initializes BBE variable and Creates router tester handle.

        BBE initialization load BBE configuration YAML file and initialize bbevar.
        bbevar is made to Python builtins by jnpr.toby.utils.bbevars.

        This method also creates connection handles for tester device.

        Robot example usage:
            # bbemaster.robot
            *** Settings ***
            Documentation    Master resource file for Toby BBE

            Library          jnpr.toby.init.init.py
            Library          jnpr.toby.engines.config.config.py
            Library          jnpr.toby.bbe.bbeinit.BBEInit
            Resource         jnpr/toby/Master.robot

            *** Keywords ***
            Test Initialize
                Initialize                            # toby initialize
                BBE Initialize    ${BBECONFIGFILE}    # bbe initialize with yaml ${BBECONFIGFILE}

            *** Variables ***
            # To specify non-default configuration file, set this variable in your test suite robot file..
            # If this variable is not set, there must be a default file named yourtest.cfg.yaml in the
            # same directory as you test suite robot file yourtest.robot
            ${BBECONFIGFILE}


        :param config_file: BBE configuration yaml file.
        Can be passed in from keyword parameter or use default which resides in the same directory
        as your test suite robot file, with the same name but different postfix. For example.
        if your test suite robot file is /path/yourtest.robot, the configuration file should be
        /path/yourtest.cfg.yaml.

        :return: None
        """

        t.log('{} Initializing BBE'.format(self.log_tag))

        # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

        log_bbe_version()

        # Derive config file name from robot file name
        if 'user_variables' in t.t_dict:
            if T_BBE_KEY in t.user_variables:
                BBEVars().initialize(t)
                no_rt = t.user_variables[T_BBE_KEY].get('debug', {})
        else:
            if not config_file:
                try:
                    suite_file = BuiltIn().get_variables()['${SUITE_SOURCE}']
                except:
                    raise BBEInitError("Cannot find Robot SUITE_SOURCE")

                if not re.match(r'.*\.robot$', suite_file):
                    raise BBEInitError("SUITE_SOURCE file must have postfix .robot")

                cf_dir = os.path.dirname(suite_file)
                cf_base = os.path.basename(suite_file)
                cf_base_new = cf_base.split('.robot')[0] + BBE_CONFIG_FILE_POSTFIX_DEFAULT
                config_file = os.path.join(cf_dir, cf_base_new)

                if not os.path.isfile(config_file):
                    raise BBEInitError("Missing BBE configuration file {}".format(config_file))

            t.log('{} Use BBE configuration file: {}'.format(self.log_tag, config_file))

            # open and load bbe config file

            with open(config_file, encoding='utf-8') as bbe_file:
                t.log('{} Opened BBE configuration file {} for legacy support'.format(self.log_tag, config_file))

                # yaml load config file
                bbe_config = yaml.load(bbe_file)

                if YAML_BBE_ROOT_KEY not in bbe_config:
                    raise BBEInitError("No mandatory %s key in BBE configuration file %s\n"
                                       % (YAML_BBE_ROOT_KEY, config_file))

                t.log('{} YAML Loaded BBE configuration file {}'.format(self.log_tag, config_file))

                bbe_var = bbe_config[YAML_BBE_ROOT_KEY]

                if not isinstance(bbe_var, dict):
                    raise BBEInitError("YAML loaded BBE configuration file %s is not a Python dict\n"
                                       % config_file)

                # initialize bbevar
                BBEVars().initialize(bbe_var)
                no_rt = bbe.bbevar.get('debug', {})

        # For ease of testing non-rt related stuff, can ignore it with bbevar setting
        no_rt = no_rt.get('do-not-init-rt', False)
        if not no_rt:
            import jnpr.toby.bbe.testers.bbert as bbert
            # Create RT
            # bbert.bbe_create_tester()
            # attach method to RT object
            #bbert.bbe_add_methods_to_rt()
            # Init RT: add subscribers, uplinks, and dhcp servers, will move to bbeConfig
            bbert.bbe_rt_init()

        # log test
        self.log_test_info()

        t.log('{} Initialized BBE'.format(self.log_tag))

    def log_test_info(self):
        """Log basic test information

        :return: None
        """
        try:
            assert isinstance(bbe.bbevar['test'], dict)
        except (KeyError, TypeError, AssertionError):
            return None

        this_test = bbe.bbevar.get('test', None)
        if not this_test:
            return

        test_description = this_test.get('description', None)
        test_type = this_test.get('type', None)
        test_id = this_test.get('id', None)

        t.log('{} Test information from configuration file:'.format(self.log_tag))
        t.log(' ')
        t.log('#' * 50)
        t.log('#')
        t.log('# {0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        t.log('#')
        t.log('# Test Description'.upper())
        t.log('#')
        if test_description:
            t.log('# {}'.format(test_description.upper()))
            t.log('#')
        if test_type:
            t.log('# {}'.format(test_type).upper())
            t.log('#')
        if test_id:
            t.log('# {}'.format(test_id))
            t.log('#')
        t.log('#' * 50)
        t.log(' ')





