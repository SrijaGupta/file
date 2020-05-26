"""
Copyright (C) 2015-2016, Juniper Networks, Inc.
All rights reserved.
Authors:
    jpzhao, ajaykv, hgona, mvmohan, jhayes, ckaushik
Description:
    Toby Config Engine

"""
# pylint: disable=locally-disabled,undefined-variable,too-many-branches,too-many-nested-blocks,eval-used,superfluous-parens,import-error,too-many-statements,unused-variable,too-many-locals,          
import re
import copy
import os
import sys
from jnpr.toby.engines.config.config_template_v2 import ConfigEngine as ConfigEngine2
from collections import OrderedDict, defaultdict
#import builtins
import pprint
from jnpr.toby.logger.logger import get_script_name
from jnpr.toby.utils.Vars import Vars
from jnpr.toby.hldcl.device import Device
from jnpr.toby.utils.utils import run_multiple
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.scp import SCP
import jnpr.toby.engines.config.config_utils as config_utils
import ruamel.yaml as yaml
import sys
from jnpr.toby.utils.utils import log_file_version
# import config_utils

NONE_DEVICE_KNOBS = ('TEMPLATES', 'TEMPLATE_FILES', 'VARS', 'CONFIG')
TV_DELIMITER = (r"\$?[tc]v\[\\*'", r"\\*'\]")
#ARG_REG = r"(var\[\\*[\'\"]([-\w]+)\\*[\'\"]\])"
#ARG_REG = r"(var\[\\*\'(\S+?)\\*\'\])"
ARG_REG = r"(var\[\\*[\'\"]([-\w]+)\\*[\'\"]\]((?:\[[^\]]+\])*))"

TEMPLATE_REG = r"template\[\\*'([-\w]+)\\*'\]$"
ROLE_REG = r"(tag\[\\*'([@\-\.\:\w]+)\\*'\])"
LOOP_REG = r"(LOOP\((.+)\))"
LOOPVAR_REG = r"([-\w]+:\s*<<.+?>>)"

# need to add all top knobs in config mode
# if a key in config yaml data is one of the followings, hold as action and apply after the whole
# config sentence is built
# todo!!: the 'load' action needs to be treated differently, it cannot be 'loaded' as 'set' string
TOP_KNOBS = ('set', 'edit', 'delete', 'activate', 'deactivate', 'disable', 'enable',
             'top', 'up', 'annotate', 'insert', 'rename', 'replace', 'load', 'rollback', 'wildcard')
# if find the following word in front of a config, do not prepand 'set'
NO_SET = r'({})'.format("|".join(TOP_KNOBS))

MYHEX = r'[A-Fa-f\d]'
# iso mininum (in bytes) is 2 4 4 4 4 2
REGEX_ISOADDR = r'{0}{{2}}(?:\.{0}{{4}}){{4}}(?:\.{0}{{2,4}}){{1,6}}'.format(MYHEX)
# mac address
REGEX_MAC = r'({0}{0}[:-]){{5}}{0}{0}'.format(MYHEX)
# ESI
REGEX_ESI = r'00:({0}{0}[:-]){{8}}{0}{0}'.format(MYHEX)

# ipv4
REGEX_IPV4ADDR = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
REGEX_IPV4BLOCK = r'({0})(?:/(\d{{1,2}}))?'.format(REGEX_IPV4ADDR)

# rfc2372 valid IPv6 address
HEX4 = r'[A-Fa-f\d]{0,4}'
REGEX_IPV6ADDR = r'(?:{0}:{{1,2}}?){{2,7}}(?:{1}|{0})?'.format(HEX4, REGEX_IPV4ADDR)
REGEX_IPV6BLOCK = r'({})(?:/(\d{{1,3}}))*'.format(REGEX_IPV6ADDR)

# any ip address / network
REGEX_IPADDR = r'{0}|{1}'.format(REGEX_IPV4ADDR, REGEX_IPV6ADDR)
REGEX_IPBLOCK = r'{0}|{1}'.format(REGEX_IPV4BLOCK, REGEX_IPV6BLOCK)

# set order to load config. Junos/linux before spirent/ixia
# todo: add use interface to change the default order
LOAD_CONFIG_ORDER = ['Junos', 'Linux', 'FreeBSD', 'Spirent', 'Ix']
#LOAD_CONFIG_ORDER = ['Junos', 'Linux', '.+']
REGEX_LINUX = r'linux|unix|centos|ubuntu|freebsd'

class config(object):
    """
    Class of Toby Config Engine

    - Generic ConfigEngine can handle all config  without requiring backend coding.
      . keep the JUNOS ( or other OS) look and feel, and mimnimize the 'code' feeling

    - Uses JUNOS (set) config as data model.
      . If you know how to configure JUNOS, you can use the Config Engine to configure it.

    - use JUNOS config knobs as keys, do not reinvent new keys to represent knobs
      . exceptions:
         - a few reserved keys (SET/DELETE/DEACTIVATE/LOAD_FILE/TAGS)
         - template names and args  that are not in JUNOS ( number of vrfs, for example)

    - Added flexibility to deal with scaled / repeated ( incremented) /topology related setup
      . Define multiple lines in one line
      . templates (accepts Jinja2 format)
      . The TAGS model with the tagging system  to make feature setup topology-neutral

    - Load part of the config in file ( policy /firewall for example, SET or JUNOS)
      . can embed some variables in the file ( can be compatible with Jinja2)

    - Extensible to other test gears: Ixia, Spirent, Linux/Unix servers
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.c_dict = {}  # build on top of t_dict in C.E., keep t immutable.
        self.cv_flat = {}
        self.roles = {}      # role tags in the yaml config file
        self.response = ''
        self.status = ''
        self.templates = {}
        self.vars = {}      # configuration/toplogy data
        self.cfg = defaultdict(list)
        self.cached = False
        self.device_list = []
        self.device_handle_map = {}
        self.cv_file = get_script_name() +'.cv'
        self.script_name = get_script_name()
        self.cached_cfg = {}   # used when disable_load is set[True]
        self.timeout = None

        self.src_path = None
        if Vars().get_global_variable('${SUITE_SOURCE}'):
            self.src_path = os.path.dirname(Vars().get_global_variable('${SUITE_SOURCE}'))
        else:
            self.src_path = os.getcwd()

    def config_engine(self, config_file=None, cmd_list=None, load_file=None, config_data=None,
                      device_list=None, commit=None, offline=None, do_parallel=None, load='config', **kwargs):
        '''
        Configure devices with a text file in Yaml format.

        DESCRIPTION:
            Configure devices with a text file in Yaml format.  The Yaml config file
            uses  device's config syntax as templating language(JUNOS set cmd for
            example). This makes the config engine  'neutral' to the content of the
            config, and can be extended to other types of devices as well.
            Details of the yaml config file can be found in:
            link to be added

            Here is an example:

                ##user configuration file

                r0:
                  TAGS: [core, pe]
                  LOAD: [firewall.conf, policy.set]
                  CONFIG:
                    protocols:
                      - ospf:
                          - area 0:
                              interface:
                                - tv['r0__r0r1_1__name']
                                - cv['r0__r0r1_2__name']
                    routing-options:
                      autonomous-system: 100

                  interfaces:
                       r0r1_1:
                          TAGS: [ospf, rsvp, mpls, mytag1]
                          CONFIG:
                            SET: [vlan-tagging, ]
                            unit 1:
                              family inet: address 12.1.1.1/30
                              vlan-id: 1

                       r0r1_2:
                          TAGS: [to_ce]
                          CONFIG:
                            SET: [vlan-tagging,]
                            unit 3:
                              vlan-id: 3
                              family inet: address 12.2.1.1/30
                              family inet6: address abcd::12:2:1:1/12

        ARGUMENTS:
            [config_file=None, cmd_list=None, load_file=None, config_data=None,
                device_list=None, commit=None, offline=None, do_parallel=None]
            :param STR device_list:
                *MANDATORY* A list of device tags.
                If it is one device, it can be in string form
            :param cmd_list:
                *MANDATORY* A list of set command
                the flatterned t_vars can be used in the set commands to  avoid
                hard coded components/parameters, such as interface names
                ( Config Engine dynamically resolves the t_vars, and turn them
                into actual values in the device)
            :param STR config_file:
                *MANDATORY* The name of the config yaml file with path.
                            Default is set to None.
            :param STR load_file:
                *OPTIONAL* commands that loaded on the device.Default is set to None.
            :param STR config_data:
                *OPTIONAL* configure data on device.Default is set to None.
            :param BOOLEAN commit:
                *OPTIONAL* commit on device.Default is set to None.
            :param BOOLEAN offline:
                *OPTIONAL*offline config check.Default is set to None.
            :param BOOLEAN do_parallel:
                *OPTIONAL* perform the task parallel.Default is set to None.
            :param STR option:
                *OPTIONAL* user defined options ex. merge,override
        ROBOT USAGE:
            EX 1: config engine    device_list=r0    commit=1    load_file=local:/var/tmp/
            EX 2: config engine    device_list=r1    commit=1    option=merge 

            Ex 3: Config Engine    device_list=r1    config_file=${tv['uv-bbevar']['routerconfig']['router-lns-yaml']}   
                vars=${vars}    format=set    commit=${True}     resolve_vars=${True}
        :return:
            device config list if config is loaded successful
            raise Exception if failed, with response from load_config()
        '''
        if kwargs.get('get_config'):
            return self.cfg

        if kwargs.get('get_response'):
            t.log(level='debug', message='response message caught by config engine:\n{}\n'. \
                            format(self.response))
            return self.response

        # make_ifd_cvar
        if not self.c_dict:
            self.__make_c_dict()

        # argument processing
        if kwargs:
            kwargs = self._process_cv(data=kwargs)

        for arg in kwargs:
            if re.match(r'timeout|load_timeout|commit_timeout', arg):
                kwargs[arg] = float(kwargs[arg])

        self.timeout = kwargs.get('timeout', None)
        no_log_config = kwargs.get('no_log_config', False)

        if not self.cached:
            if not self.cached_cfg:
                self.cfg = defaultdict(list)    # clean up previous cfg data
        ce_version = 'v1'
        if device_list is not None:
            if not isinstance(device_list, list):
                if isinstance(device_list, str):
                    # if the device_list is comma separated, break it into a list
                    device_list = [dev.strip() for dev in device_list.split(',')]
                else:
                    device_list = [device_list]
            # handle device list with handles here:
            # start a new device_list each time config_engine is called.
            # if there is a handle in the list, find the host name from the handle,
            # and replace it in device_list.
            # mapping to name as tag to handles. ( not in tv) !!!
            for i, dev in enumerate(device_list):
                if self.cached_cfg:
                    if dev not in self.cached_cfg.keys():
                        self.cfg[dev] = []
                if isinstance(dev, str):
                    if not tv.get(dev + '__name'):
                        # dev is not a device alias, could be a device name
                        try:
                            dev_h = self._get_dev_handle(dev)
                            self.device_handle_map[dev] = dev_h
                            t.log(level='debug', message='{} in device_list  is a name rather than an alias' \
                                  .format(dev))
                            self.cv_flat[dev + '__osname'] = \
                                dev_h.current_node.current_controller.os
                        except:
                            raise Exception('{} in device_list cannot be found in params' \
                                            .format(dev))
                else:
                    # could be a device handle
                    try:
                        if hasattr(dev, 'host'):
                            dev_host = dev.host
                            self.cv_flat[dev_host + '__osname'] = dev.os
                        elif hasattr(dev, 'current_controller'):
                            dev_host = dev.current_controller.host
                            self.cv_flat[dev_host + '__osname'] = dev.current_controller.os
                            dev = dev.current_controller
                        else:
                            dev_host = dev.current_node.current_controller.host
                            self.cv_flat[dev_host + '__osname'] = \
                                dev.current_node.current_controller.os

                        self.device_handle_map[dev_host] = dev
                        # replace device_list with the host ( an ip address in most cases)
                        device_list[i] = dev_host
                        t.log(level='debug', message='device_list has a handle, replace it with its host {}' \
                              .format(dev_host))
                    except:
                        raise Exception('device_list accepts only device alias, \
                            device name or device handle')

            check_version_file = config_file

            #check for ce version
            if 'template_files' in kwargs and not config_file:
                file_list = kwargs['template_files']
                if isinstance(file_list, str):
                    file_list = [file.strip() for file in file_list.split(',')]
                check_version_file = file_list[0]

            if check_version_file:
                log_file_version(check_version_file)
                check_version_file = config_utils.find_file(check_version_file)
                template_file_dict = yaml.safe_load(open(check_version_file, 'r').read())

                if 'filetype' in template_file_dict:
                    if template_file_dict['filetype'] is not None and template_file_dict['filetype'] == 'config_template_v2':
                        ce_version = 'v2'
                print("CE template file: " + check_version_file + "(CE" + ce_version + ")")                

        if ce_version == 'v1':
            self._load_template_v1_and_get_commands(config_file=config_file, cmd_list=cmd_list, load_file=load_file,
                                                    config_data=config_data, device_list=device_list, commit=commit, 
                                                    offline=offline, do_parallel=do_parallel, load=load, **kwargs)
        elif ce_version == 'v2' and device_list is not None:
            config_file = check_version_file
            variables = kwargs.get('vars', None)
            if kwargs.get('config_templates'):
                template = kwargs['config_templates']
                if isinstance(template, str):
                    template = [temp.strip() for temp in template.split(',')]
            self._load_template_v2_and_get_commands(device_list=device_list, config_file=config_file, variables=variables, template=template)
            if 'vars' in kwargs:
                del kwargs['vars']
            if 'config_templates' in kwargs:
                del kwargs['config_templates']
        else:
            raise Exception("Config Engine V2 requires a device_list")

        self._load_config(device_list=device_list, offline=offline, commit=commit, do_parallel=do_parallel, load=load, **kwargs)

        return True
 
    def _load_template_v2_and_get_commands(self, device_list=None, config_file=None, template=None, variables=None, **kwargs):
        ce2 = ConfigEngine2()
        #read template files
        template_file_name = config_file
        template_file_list = [template_file_name]
        ce2.process_template_files(template_file_list)
        cfg_set = []
        for ce2_template in template:
            template_cfg_set = ce2.config(template=ce2_template, args=variables)
            cfg_set.extend(template_cfg_set)
        cfg_set = self._expand_config(cfg_set)
        #t.log_console(cfg_set)
        self.device_list = device_list
        for device in self.device_list:
            if device not in self.cached_cfg.keys():
                self.cfg[device] = cfg_set
            else:
                self.cfg[device].extend(cfg_set)  # append

    #existing ce code lies here:
    def _load_template_v1_and_get_commands(self, config_file=None, cmd_list=None, load_file=None, config_data=None,
                      device_list=None, commit=None, offline=None, do_parallel=None, load='config', **kwargs):
        '''
        existing ce code lies here 
        '''
        if kwargs.get('template_files'):
            file_list = kwargs['template_files']
            if isinstance(file_list, str):
                file_list = [file.strip() for file in file_list.split(',')]
            for temp_file in file_list:
                self.templates.update(self.read_template_files(files=temp_file))
        if kwargs.get('templates'):
            try:
                templates = config_utils.read_yaml(kwargs.pop('templates'))
            except Exception as err:
                t.log(level='error', message='failed to parse \"templates\" string:' + str(err))
                raise Exception('failed to parse \"templates\" string: ' + str(err))
            self.templates.update(templates)
            templates = None
        if load_file is not None:
            t.log(level='info', message='== Config Engine: load config file ' + load_file)
            if device_list is None:
                raise Exception('missing device_list for load_file')
            if kwargs.get('load_timeout'):
                kwargs['timeout'] = kwargs['load_timeout']
            elif self.timeout is not None:
                kwargs['timeout'] = self.timeout

            # check if it is local file on device:
            mat = re.match(r'local:(.+)', load_file)
            remote = re.match(r'(.+)/(.+)@(.+):((.+/)*(.+))', load_file)
            if mat:
                load_file = str(mat.group(1))
                kwargs['remote_file'] = load_file

            if remote:
                remote_user = str(remote.group(1))
                remote_pass = str(remote.group(2))
                remote_host = str(remote.group(3)).lower()
                remote_file = str(remote.group(4))
                load_file = str(remote.group(6))
                if remote_host == 'cvs':
                    try:
                       remote_pass = os.environ[remote_pass]
                    except:
                       raise Exception('CVS password can only be passed as an environment variable for security')
                    link = 'https://cvs-bn.juniper.net/cgi-bin/viewcvs.cgi/'+remote_file+'?view=co'
                    http_req = flow_common_tool()
                    res = http_req.download_file_by_http(link, load_file, username=remote_user, password=remote_pass, verify=True)
                else:
                    scp_client = SCP(remote_host, user=remote_user, password=remote_pass)
                    res = scp_client.get_file(remote_file, load_file)
                if not res:
                    raise Exception("Failed to download config file from "+ remote_host)

            if do_parallel is not None:
                do_parallel = bool(re.match(r'true|1', str(do_parallel), re.IGNORECASE))

            if do_parallel:
                kwargs['load_file'] = load_file
                targets = []
                for dev_tag in device_list:
                    targets.append({'target': self._load_onto_device, 'args': [dev_tag], 'kwargs': kwargs})
                run_multiple(targets=targets)
            else:
                for dev_tag in device_list:
                    self._load_onto_device(device=dev_tag, load_file=load_file, **kwargs)

        if kwargs.get('load_string'):
            load_string = kwargs['load_string']
            t.log(level='debug', message='== Config Engine: load config string: ')
            if device_list is None:
                raise Exception('missing device_list for load_string')
            if kwargs.get('load_timeout'):
                kwargs['timeout'] = kwargs['load_timeout']
            elif self.timeout is not None:
                kwargs['timeout'] = self.timeout
            if re.search(r'^{} [-\w]+'.format(NO_SET), load_string, re.MULTILINE):
                kwargs['option'] = 'set'
            if do_parallel is not None:
                do_parallel = bool(re.match(r'true|1', str(do_parallel), re.IGNORECASE))

            if do_parallel:
                kwargs['cfg_list'] = load_string
                targets = []
                for dev_tag in device_list:
                    targets.append({'target': self._load_onto_device, 'args': [dev_tag], 'kwargs': kwargs})
                run_multiple(targets=targets)
            else:
                for dev_tag in device_list:
                    self._load_onto_device(device=dev_tag, cfg_list=load_string, **kwargs)

        # - turn yaml to data
        if config_file is not None:
            t.log(level='info', message='== build config on yaml config file: ' + config_file)
            data = config_utils.read_yaml(file=config_file)
            if device_list is None:
                device_list = [dev_tag for dev_tag in data
                               if dev_tag not in NONE_DEVICE_KNOBS]
            self._config_data(cfg_data=data, **kwargs)
        # config data
        if config_data is not None:
            t.log(level='debug', message='== build config on yaml config string:')
            if isinstance(config_data, str):
                try:
                    config_data = config_utils.read_yaml(config_data)
                except Exception as err:
                    t.log(level='error', message='failed to parse yaml config string:' + str(err))
                    raise Exception('failed to parse yaml config string: ' + str(err))

            if device_list is None:
                device_list = [dev_tag for dev_tag in config_data
                               if dev_tag not in NONE_DEVICE_KNOBS]
            self._config_data(cfg_data=config_data, **kwargs)
        # configure list of templates
        if kwargs.get('config_templates'):
            t.log(level='debug', message='== build config on list of templates:')
            if device_list is None:
                raise Exception('missing device_list for templates')
            cfg_templates = kwargs['config_templates']
            if isinstance(cfg_templates, str):
                cfg_templates = [temp.strip() for temp in cfg_templates.split(',')]
            # passing template args in vars
            temp_args = {}
            if kwargs.get('vars'):
                temp_args.update(kwargs['vars'])
            data = {}
            for dev in device_list:
                for templ in cfg_templates:
                    config_utils.nested_set(data, [dev, 'CONFIG'], \
                        [{"template['{}']".format(templ): temp_args}], append=True)
            self._config_data(cfg_data=data, **kwargs)

        # list of set cmds
        if cmd_list is not None:
            t.log(level='debug', message='== build config on list of set cmds:')
            if device_list is None:
                raise Exception('missing device_list for cmd_list')
            if isinstance(cmd_list, str):
                cmd_list = [cmd.strip() for cmd in cmd_list.split(',')]
            #elif isinstance(cmd_list, (list, tuple)):
                #cmd_list = cmd_list

            data = {}
            for dev in device_list:
                config_utils.nested_set(data, [dev, 'CONFIG'], cmd_list)
            self._config_data(cfg_data=data, **kwargs)
        self.device_list = device_list

    def _load_config(self, device_list=None, offline=None, commit=None, do_parallel=False, **kwargs):
        # rpc calls:
        if kwargs.get('rpc'):
            t.log(level='debug', message='== build config with an RPC:')
            if device_list is None:
                raise Exception('missing device_list for rpc')
            for device in self.device_list:
                rpc = kwargs.pop('rpc')
                rpc = rpc.strip('\"\' ')
                self._load_rpc(device=device, rpc=rpc, **kwargs)
                rpc = '<commit/>'
                rpc = rpc.strip('\' ')
                self._load_rpc(device=device, rpc=rpc, **kwargs)
            self.status = True
            return self.status


        # nothing in argument?
        # warning and return None. probably OK.

        # save config file to log: todo( or leave it to offline tool?)
        # junos.load_confg() does that
        #if kwargs.get('save_config', True):
            #for dev in self.cfg:
                #print('save cfg on: ', dev)

        # now we have built up set cmds for all devices, load them:
        # parallel: to do.
        if kwargs.get('disable_load'):
            for dev_cache in self.device_list:
                msg = '== Config Engine: disable_load is set to True, not loading config on the device.' 
                t.log(level='debug', message=msg + '....')
                msg = '== Config Engine:Cache config as below:'
                cmd_log = self.cfg[dev_cache]
                if dev_cache in self.cached_cfg.keys():
                    cache_log = cmd_log[self.cached_cfg[dev_cache]:]
                else:
                    cache_log = cmd_log
                self.cached_cfg[dev_cache] = len(cmd_log)
                if len(cache_log) > 1:
                    pp_width = len(str(cache_log)) - 1
                else:
                    pp_width = 1000
                pp = pprint.PrettyPrinter(width=pp_width)
                cache_log = pp.pformat(cache_log)
                t.log(level='info', message='\n======\n' + cache_log + '\n======') 
            self.cached = True

        elif offline is None:
            self.cached = False  # config to be loaded, clear up cached config
            if commit is not None:
                commit = bool(re.match(r'true|1', str(commit), re.IGNORECASE))
            if do_parallel is not None:
                do_parallel = bool(re.match(r'true|1', str(do_parallel), re.IGNORECASE))
            for load_os in LOAD_CONFIG_ORDER:
                targets = []
                for dev_tag in self.device_list:
                    osname = self.__get_cvar(cv_name=dev_tag + '__osname')
                    if not re.match(r'{}'.format(load_os), osname, re.I):
                        continue
                    if do_parallel and load_os in LOAD_CONFIG_ORDER[:2]:
                        targets.append({'target': self._load_device_config, 'args': [dev_tag, osname, commit],
                                            'kwargs': kwargs})
                    else:
                        self._load_device_config(dev_tag, osname, commit, **kwargs)
                if targets:
                    run_multiple(targets=targets)

        # save cv file
        if kwargs.get('save_cv'):
            config_utils.write_to_yaml(self.cv_flat, file=self.cv_file)

        self.status = True
        return self.status

    def _load_device_config(self, device=None, osname=None, commit=None, **kwargs):
        #timeout = kwargs.get('timeout', None)
        no_log_config = kwargs.get('no_log_config', False)
        if self.cfg.get(device):
            t.log(level='debug', message='== load config on: ' + device)
            cmds = self.cfg[device]
            if kwargs.get('load_timeout'):
                kwargs['timeout'] = kwargs['load_timeout']                     
            elif self.timeout is not None:                                          
                kwargs['timeout'] = self.timeout                                    
            #load config file:                                                         
            msg = '== Config Engine: load cfg on device ' + device                     
            t.log(level='debug', message=msg + '....')                                                        
            if not no_log_config:    # default is to log cfg                          
                cmd_log = self.cfg[device]
                if device in self.cached_cfg.keys():    # log if cached config is set
                    c_log = cmd_log[self.cached_cfg[device]:len(cmd_log)]
                    if len(c_log) > 1:
                       pp_width = len(str(c_log)) - 1
                    else:
                       pp_width = 1000
                    pp = pprint.PrettyPrinter(width=pp_width)
                    c_log = pp.pformat(c_log)
                    msg = '== Config Engine: disable_load is set to false.'
                    t.log(level='info', message=msg)
                    msg = '== Config Engine: Current config as below:'
                    t.log(level='info', message=msg +'....')
                    t.log(level='info', message='\n======\n' + c_log + '\n======\n')
                    del self.cached_cfg[device]
                    del self.cfg[device]
                    msg = '== Config Engine: Loading cache config + current config'
                    t.log(level='info', message=msg +'....')
                if len(cmd_log) > 1:
                   pp_width = len(str(cmd_log)) - 1
                else:
                   pp_width = 1000
                pp = pprint.PrettyPrinter(width=pp_width)
                cmd_log = pp.pformat(cmd_log)
                t.log(level='info', message='\n======\n' + cmd_log + '\n======\n')
            t.log(level='debug', message='with args: ' + str(kwargs))
            self._load_onto_device(device=device, cfg_list=cmds, **kwargs)
        if (re.match(r'junos', osname, re.I)) and commit:
            dev_hdl = self._get_dev_handle(device)
            t.log(level='info', message='== commit config on: ' + device)
            if kwargs.get('commit_timeout'):
                kwargs['timeout'] = kwargs['commit_timeout']
            elif self.timeout is not None:
                kwargs['timeout'] = self.timeout
            try:
                msg = '== Config Engine: commit on device: ' + device
                t.log(level='info', message=msg + '...')
                res = dev_hdl.commit(**kwargs)
                                                                               
                if res.status() is True:                                           
                    self.response = msg + ' successful:\n' + res.response()
                    t.log(level='debug', message=self.response)
                    self.status = True
                else:
                    # current commit() will never get here
                    self.response = msg + ' failed:\n' + res.response()
                    t.log(level='error', message=self.response)
                    self.status = False
                    raise Exception(self.response)
                                                                               
            except Exception as err:
                self.response = "== Config Engine: commit failed on " + device + ': ' + str(err)
                t.log(level='error', message=self.response)
                self.status = False
                raise Exception(self.response)
        return self.status
    
    def __copy_t_dict(self):
        '''
        make a deep copy of t_dict, so  config data mining will not affect t data
        '''
        for device in t.t_dict['resources']:
            if t.t_dict['resources'][device].get('interfaces'):
                intf = copy.deepcopy(t.t_dict['resources'][device]['interfaces'])
                config_utils.nested_set(self.c_dict, [device, 'interfaces'], intf)

                # remove the useless 'unit' knob  will add back if ip config is added
                # in junos interface config
                try:
                    for ifkey in self.c_dict[device]['interfaces']:
                        del self.c_dict[device]['interfaces'][ifkey]['unit']
                except:
                    pass
            for topkey in t.t_dict['resources'][device]['system']:
                # donot copy device handles
                if topkey != 'dh':
                    config_utils.nested_set(self.c_dict, \
                        [device, 'system', topkey], \
                        copy.deepcopy(t.t_dict['resources'][device]['system'][topkey]))
            # 'user_variables' in params are availavle in tv
            # do not copy them to cd_dict for now, unless we need it

    def register_device_methods(self, **kwargs):
        '''
        pacth device specific methods for config engine.
        '''
        # default: look for py files under /toby/engines/config/
        pass

        # user register

    def __make_c_dict(self, **kwargs):
        '''
        copy t_dict over, leave t data immutable.
        and add more data inside the config engine object.(cv)
        '''

        self.__copy_t_dict()
        for dev_tag in self.c_dict:
            osname = self.__get_cvar(cv_name=dev_tag + '__osname')
            if re.match(r'Spirent|Ix.+', osname, re.I):
                try:
                    dev_hdl = self._get_dev_handle(dev_tag)
                    dev_hdl.osname = self.__get_cvar(cv_name=dev_tag + '__osname')
                    # add port handles to cv data for easy access
                    for intf_tag, port_name in dev_hdl.intf_to_port_map.items():
                        config_utils.nested_set(self.c_dict,
                                                [dev_tag, 'interfaces', intf_tag, 'porthandle'],
                                                dev_hdl.port_to_handle_map[port_name])
                        self.cv_flat['__'.join([dev_tag, intf_tag, 'porthandle'])] \
                        = dev_hdl.port_to_handle_map[port_name]
                except Exception as err:
                    #if the device handle does not have handle maps, skip
                    t.log(level='debug', message='no spirent/ixia device or port_to_handle_map available:'\
                            + str(err))
                    t.log(level='debug', message='ignore the above error, skip adding port_to_handle_map to cv')

        self._make_ifd_cvar()

    def _make_virtual_c_dict(self, data):
        '''
        check for virtual node/links: logical system, ae, lo0 etc...
        process and add them into c_dict
        '''

        if not isinstance(data, dict):
            t.log(level='debug', message='data is not a dict, return as is')
            return data

        found_virtual = False
        for dev_tag in data:

            # check for virtual node (logical systems)
            # todo
            '''
            lr1:
                TAG: [logical-system]
                HOST: r0
                CONFIG:
            '''

            # check for virtual interfaces in 'interfaces' config:
            if data[dev_tag].get('interfaces'):
                for intf_tag in data[dev_tag]['interfaces']:
                    if tv.get('__'.join([dev_tag, intf_tag, 'pic'])):
                        continue
                    else:
                        vintf = data[dev_tag]['interfaces'][intf_tag]
                        config_utils.nested_set(self.c_dict, [dev_tag, 'interfaces', intf_tag], {})
                        intf = self.c_dict[dev_tag]['interfaces'][intf_tag]
                        if not vintf.get('link'):
                            # todo: lo0 interface might be OK
                            raise Exception('define interface {} / {} without "link" attr'.\
                                    format(dev_tag, intf_tag))
                        intf['link'] = vintf.get('link')
                        intf['pic'] = vintf.get('pic', intf_tag)
                        intf['name'] = vintf.get('name', intf_tag + '.0')
                        intf['type'] = vintf.get('type', re.sub(r'^([a-zA-Z]+).*', r'\1', intf_tag))
                        # other parameters?
                        found_virtual = True

            if found_virtual:
                self._make_ifd_cvar()


    def _config_data(self, cfg_data=None, **kwargs):
        '''
        internal config method
        process config python data derived from yaml
        '''
        self._process_role_tags(cfg_data=cfg_data)
        cfg_data = self._process_cv(data=cfg_data)
        # check if templates are defined:
        if 'TEMPLATE_FILES' in cfg_data:
            for temp_file in cfg_data.pop('TEMPLATE_FILES'):
                temps = config_utils.read_yaml(file=temp_file)
                if temps.get('TEMPLATES'):
                    # in case the 'TEMPLATES' knob is put at the top of a template file')
                    temps = temps['TEMPLATES']
                self.templates.update(temps)
                #self.templates.update(config_utils.read_yaml(file=temp_file))
        if 'TEMPLATES' in cfg_data:
            if not isinstance(cfg_data['TEMPLATES'], dict):
                raise Exception("Possible YAML syntax errors under 'TEMPLATES' in config yaml")
            self.templates.update(cfg_data.pop('TEMPLATES'))
        if 'CONFIG' in cfg_data:
            cfg_data.pop('CONFIG')
            # Todo
            print("\n === Global CONFIG is not ready yet")

        # handle global YAML config vars
        gvars = {}
        if 'VARS' in cfg_data:
            # process yaml file vars
            if not isinstance(cfg_data['VARS'], list):
                raise Exception('VARS in config yaml file should be a list')

            for var in cfg_data['VARS']:
                if isinstance(var, dict):
                    gvars.update(var)
                elif isinstance(var, str):
                    gvars.update({var:None})
                else:
                    raise Exception('Wrong type of var {}'.format(str(var)))
            cfg_data.pop('VARS')

        #check if 'vars' args is available.
        if kwargs.get('vars'):
            if not isinstance(kwargs['vars'], dict):
                err = "**** Config Engine yaml 'vars' should be in dict format:" \
                      + str(kwargs['vars'])
                err += "\n vars type is now: " + type(kwargs['vars']).__name__
                err += "\n Check your Robot file for 'vars'"
                raise Exception(err)
            gvars.update(kwargs['vars'])

        if gvars:
            # check for any undefined vars
            undef_vars = [var for var in gvars if gvars[var] is None]
            if undef_vars:
                raise Exception('undefinded config yaml vars: {}'.\
                        format(str(undef_vars)))

            gvars = self._process_cv(data=gvars)

            # now replace global vars with values passed into config engine
            cfg_data = self._process_config_vars(data=cfg_data, vars=gvars, no_warn=True)

        # check for virtual node/links: logical system, ae, lo0 etc...
        self._make_virtual_c_dict(data=cfg_data)

        # go through interface config on all devices first
        # JUNOS device with interfaces/r0r1/CONFIG for now.
        # Todo: check all interface config
        # Todo: make sure to configure JUNOS devices before testers.
        # Todo: tester/linux needs to have consistant syntax for IP config first
        for dev_tag in cfg_data:
            # start device config
            dev_cfg = cfg_data[dev_tag]
            if dev_cfg.get('interfaces'):
                self._config_interfaces(dev_tag, data=dev_cfg['interfaces'])
        for dev_tag in cfg_data:
            # start device config
            if self.cached_cfg:
                if dev_tag not in self.cached_cfg.keys():
                     self.cfg[dev_tag] = []
            cfg_set = []
            dev_cfg = cfg_data[dev_tag]
            if dev_cfg.get('CONFIG'):
                cfg_set.extend(self._build_config(device=dev_tag, config_data=dev_cfg['CONFIG']))
                # expand config
                cfg_set = self._expand_config(config_list=cfg_set, device=dev_tag)
            self.cfg[dev_tag].extend(cfg_set)
        return self.cfg


    def _config_interfaces(self, dev_tag=None, data=None):
        '''
        build interface config,
        - build extra c_dict in self.c_dict, including all IP setup
        - deal with lo0: todo
        - deal with AE/AS/ls... links that cannot be defined in params: todo
        - add cvar equivalent vars to be globally available
        '''
        # make list of ifd for each device, lo0 be the frist

        # build set cmd list for each ifd
        # todo: coc, ls link processing

        osname = self.__get_cvar(cv_name=dev_tag + '__osname')
        cfg_set = []
        for intf_tag in data.keys():
            if not data[intf_tag].get('CONFIG'):
                continue

            cmd_list = []
            t.log(level='debug', message='==Config Engine: build config for {} {}'.format(dev_tag, intf_tag))
            cmd_list = self._build_config(device=dev_tag,
                                          config_data=data[intf_tag]['CONFIG'],
                                          ifd_tag=intf_tag)
            cmd_list = self._expand_config(config_list=cmd_list, device=dev_tag)
            cfg_set.extend(cmd_list)

            # add cvar
            if osname.lower() == 'junos':
                self._make_ifl_cvar(dev_tag=dev_tag, ifd_tag=intf_tag, cmd_list=cmd_list)

        self.cfg[dev_tag].extend(cfg_set)

        # optional, load config and ping?

        return self.cfg


    def CONFIG_SET(self, device_list=None, cmd_list=None, commit=None, **kwargs):
        '''

        Configure a list of 'set' commands on devices.
        
        DESCRIPTION:
            This method will soon be obsolete. use config_engine with same
            arguments instead
        
        ARGUMENTS:
            [device_list=None, cmd_list=None, commit=None]
            :param STR device_list:
                *MANDATORY* A list of device tags.
                If it is one device, it can be in string form
            :param cmd_list:
                *MANDATORY* A list of set command
                the flatterned t_vars can be used in the set commands to  avoid
                hard coded components/parameters, such as interface names
                ( Config Engine dynamically resolves the t_vars, and turn them
                into actual values in the device)
            :param BOOLEAN commit:
                *OPTIONAL*commit changes.Default is set to None. 

        ROBOT USAGE:
            Config Set    device_list=r3    cmd_list=${cmds}   commit=True

        :return:
            True if config is loaded successful
            raise exception if failed, with response from HLDCL config() call

        '''
        return self.config_engine(device_list=device_list, cmd_list=cmd_list, \
                                  commit=commit, **kwargs)


    def CONFIG_LOAD(self, commit=None, device=None, file=None, **kwargs):
        '''

        Load a saved config file onto a device.

        DESCRIPTION:
            This method will soon be obsolete. use config_engine with same
            arguments instead

            You'll be able to insert t_vars inside the config to add some flexibility.(todo)

            cfg.CONFIG_LOAD(device='r0', file='config1.txt')
        
        ARGUMENTS:
            :param STR device:
                *device tag as shown in teh topology yaml file, or in t.Default is set to None.
            :param STR file:
                *MANDATORY*The name of the config file with path.Default is set to None.
            :param BOOLEAN commit:
                *OPTIONAL*commit changes.Default is set to None.Default is set to None. 

        ROBOT USAGE:
            config load         device=${dut}        file="/var/tmp/.CONF"

        :return:
            True if config is loaded successful
            raise exception if failed, with response from HLDCL load_config() call

        '''

        return self.config_engine(device_list=device, load_file=file, commit=commit, **kwargs)


    def _get_template_args(self, temp_args=None, default=None, temp_name=''):
        '''
        internal function to get template args in list/dict , and turn them into a dict
        '''
        arg_dict = {}
        if isinstance(temp_args, dict):
            arg_dict.update(temp_args)
        elif isinstance(temp_args, list):
            for arg in temp_args:
                if isinstance(arg, dict):
                    arg_dict.update(arg)
                elif isinstance(arg, str):
                    if default is not None:
                        # get all args from template, even if not assigned yet
                        arg_dict[arg] = None
                else:
                    raise Exception('wrong arg format in template {}: {}' \
                                    .format(temp_name, type(arg)))
        else:
            raise Exception('wrong template arg format in template {}: {}' \
                            .format(temp_name, type(temp_args)))

        return arg_dict

    def read_template_files(self, files):
        '''
    A template file may include a list of templates in diffrent form.

    DESCRIPTION:
        A template file may include a list of templates directly,
        OR uder the 'TEMPLATES' keyword.
        AND/OR has a 'TEMPLATE_FILEs' knob that points to other template files.

    ARGUMENTS:
        [files]
        :param STR files:
            *MANDATORY* files name.

    ROBOT USAGE:
        read Template Files    files=FILE_NAME
        '''
        templates = {}
        if isinstance(files, str):
            files = [file.strip() for file in files.split(',')]
 
        for template_file in files:
            temp_data = config_utils.read_yaml(file=template_file)
            if 'TEMPLATE_FILES' in temp_data:
                for temp_file in temp_data.pop('TEMPLATE_FILES'):
                    temps = config_utils.read_yaml(file=temp_file)
                    if temps.get('TEMPLATE_FILES'):
                        templates.update(self.read_template_files(temps.pop('TEMPLATE_FILES')))

                    if temps.get('TEMPLATES'):
                        # in case the 'TEMPLATES' knob is put at the top of a template file')
                        temps = temps['TEMPLATES']
                    templates.update(temps)
                    #self.templates.update(config_utils.read_yaml(file=temp_file))
            if 'TEMPLATES' in temp_data:
                # remove 'TEMPLATES' key
                temp_data = temp_data['TEMPLATES']
            if temp_data:
                templates.update(temp_data)
            else:
                raise Exception('failed to get templates from file {}'.format(template_file))

        return templates

    def _config_template(self, device=None, template=None, args=None, path='', \
            action='set', **kwargs):
        '''
        buld configuration from a template for a specific device
        mainly for internal use
        '''
        cmd_set = []
        # check if the template is defined
        if template is None:
            raise Exception('arg "template" is mandatory')
        if template not in self.templates:
            raise Exception('template {} is not defined'.format(template))

        cfg_temp = self.templates[template]

        # get default args from template
        temp_args = {}
        if cfg_temp.get('ARGS'):
            temp_args = self._get_template_args(cfg_temp['ARGS'], default=1, temp_name=template)

        # update with user args
        if args is not None:
            temp_args.update(self._get_template_args(args, temp_name=template))

            #replace tv/cv value
            #do not expand list <<  >>  now
        temp_args = self._process_cv(data=temp_args)
        temp_args = self._process_args(data=temp_args, device=device)

        # makesure all args are defined before applying template
        # and save them as config vars
        if temp_args:
            undef_arg = [arg for arg in temp_args if temp_args[arg] is None]
            if undef_arg:
                raise Exception('template {} has undefined args: {}'.  \
                        format(template, str(undef_arg)))
            cmd = self._process_args(data=cfg_temp['CONFIG'], device=device, vars=temp_args)
        else:
            cmd = cfg_temp['CONFIG']

        # start building config:
        tmp = self._build_config(device=device, config_data=cmd,
                                 action=action, path=path, **kwargs)
        if tmp:
            cmd_set.extend(tmp)
        else:
            t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                    format(device, path, str(cmd)))


        return cmd_set

    def _build_config(self, device=None, config_data=None, path='', action='set', **kwargs):
        '''
        Usually used internally with config engine.

        Take a piece of yaml config and compile it into actual device config list.
        This is the work horse of the config engine that traverse the yaml config
        content and process tags/templates.

        '''

        ifd = None
        if kwargs.get('ifd_tag'):
            ifd = self._get_ifd_from_tag(device, kwargs.get('ifd_tag'))
            kwargs['ifd'] = ifd

        osname = self.__get_cvar(cv_name=device + '__osname')
        if re.match(r'junos', osname, re.I):
            if ifd:
                #path = ' interfaces ' + ifd
                path = 'interfaces ' + ifd
                kwargs.pop('ifd_tag')
                t.log(level='debug', message='build config for {} {}'.format(device, ifd))
            return self._build_junos_config(device=device, config_data=config_data,
                                            path=path, action=action, **kwargs)
        elif re.match(REGEX_LINUX, osname, re.I):
            if not isinstance(config_data, list):
                raise Exception('linux config needs to be in list format on: ' + device)
            return self._build_linux_config(device=device, config_data=config_data,
                                            path=path, action=action, **kwargs)
        elif re.match(r'(ix|spi)', osname, re.I):
        #else:
            if not isinstance(config_data, list):
                raise Exception('For {}, Top level config needs to be in list format on {}' \
                                .format(osname, device))
            return self._build_rt_config(device=device, config_data=config_data, path=path, \
                                         action=action, **kwargs)

        else:
            raise Exception('The OS {} is not yet supported in config engine'.format(osname))


    def _build_junos_config(self, device=None, config_data=None, path='', action='set', **kwargs):
        '''
        Usually used internally with config engine.

        Take a piece of yaml config and compile it into actual device config list.
        This is the work horse of the config engine that traverse the yaml config
        content and process tags/templates.

        '''
        cmd_set = []
        cfg = config_data
        if isinstance(cfg, list):
            for cmd in cfg:
                tmp = self._build_junos_config(device=device, config_data=cmd, action=action, path=path, **kwargs)
                if tmp:
                    cmd_set.extend(tmp)
                else:
                    t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                         format(device, path, str(cmd)))
        elif isinstance(cfg, dict):
            for knob in cfg.keys():
                if not isinstance(knob, str):
                    raise Exception("dict config: knob is not a string: " + str(knob))

                # handle nested loops: LOOP(id:<<1..10>>, ip:<<>>):
                elif knob.startswith('LOOP('):
                    cmd = cfg[knob]
                    loop_iter = iter(config_utils.expand_to_list(base=knob.strip('LOOP() ')))
                    # start loops
                    for iloop in loop_iter:
                        largs = {}
                        for lvar in iloop.split(','):
                            lkey, val = lvar.split(':', 1)
                            largs[lkey.strip()] = val.strip()
                        icmd = self._process_config_vars(data=cmd, vars=largs, no_warn=True)
                        tmp = self._build_junos_config(device=device, config_data=icmd,
                                                       action=action, path=path)
                        if tmp:
                            cmd_set.extend(tmp)
                        else:
                            t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                                format(device, path, str(icmd)))

                elif re.match(TEMPLATE_REG, knob):
                    matched = re.match(TEMPLATE_REG, knob)
                    template = matched.group(1)
                    args = cfg[knob]
                    tmp = self._config_template(device=device, template=template, path=path,
                                                action=action, args=args, **kwargs)

                    if tmp:
                        cmd_set.extend(tmp)
                    else:
                        t.log(level='debug', message='On {}, turn off cfg temp under {}:\n{}'.\
                                format(device, path, str(template)))

                # in ('set:', 'delete:', 'deactivate:'......):
                # in this case, these top knobs appear as a single key
                # it can be in any location of the path, CE will remember that
                # and prepand the top knob to the expanded config
                elif knob.lower() in TOP_KNOBS:
                    action = knob.lower()
                    cmd = cfg[knob]

                    tmp = self._build_junos_config(device=device, config_data=cmd,
                                                   action=action, path=path, **kwargs)
                    if tmp:
                        cmd_set.extend(tmp)
                    else:
                        t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                             format(device, path, str(cmd)))
                else:
                    cmd = cfg[knob]
                    subpath = path + " " +  knob
                    tmp = self._build_junos_config(device=device, config_data=cmd, \
                                action=action, path=subpath.strip(), **kwargs)

                    if tmp:
                        cmd_set.extend(tmp)
                    else:
                        t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                             format(device, path, str(cmd)))

        elif isinstance(cfg, (str, int, type(None))):
            if cfg is None:
                cfg = ''
            cfg = str(cfg)
            if re.match(r'template\[\'\w+\'\]$', cfg):
                matched = re.match(r'template\[\'(\w+)\'\]$', cfg)
                template = matched.group(1)

                tmp = self._config_template(device=device, template=template, path=path,
                                            action=action, **kwargs)
                if tmp:
                    cmd_set.extend(tmp)
                else:
                    t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                            format(device, path, str(cmd)))
            else:
                if not re.match(r'\s*{}\s+'.format(NO_SET), cfg):
                    cfg = path.strip() + " " + cfg.strip()
                    cfg = action.lower() + ' ' + cfg.strip()
                cfg = cfg.strip()
                cmd_set.append(cfg)

        else:
            raise Exception("config format unknown: " + str(cfg) + ' type: ' + str(type(cfg)))

        cmd_set = [re.sub(r'( *bool:True\[.+?\] *)+', ' ', cmd)
                   for cmd in cmd_set if not re.search(r'bool:False', cmd)]
        return cmd_set



    def _build_linux_config(self, device=None, config_data=None, path='', action='set', **kwargs):
        '''
        Usually used internally with config engine.

        take a piece of yaml config and compile it into actual device config list.
        This is the work horse of the config engine that traverse the yaml config
        content and process tags/templates.

        '''
        cmd_set = []
        cfg = config_data
        if isinstance(cfg, list):
            for cmd in cfg:
                tmp = self._build_linux_config(device=device, config_data=cmd,
                                               action=action, path=path)
                if tmp:
                    cmd_set.extend(tmp)
                else:
                    t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                         format(device, path, str(cmd)))

        elif isinstance(cfg, dict):
            for knob in cfg.keys():
                if not isinstance(knob, str):
                    raise Exception("dict config: knob is not a string: " + str(knob))

                # handle nested loops: LOOP(id:<<1..10>>, ip:<<>>):
                elif knob.startswith('LOOP('):
                    cmd = cfg[knob]
                    loop_iter = iter(config_utils.expand_to_list(base=knob.strip('LOOP() ')))
                    # start loops
                    for iloop in loop_iter:
                        largs = {}
                        for lvar in iloop.split(','):
                            lkey, val = lvar.split(':', 1)
                            largs[lkey.strip()] = val.strip()
                        icmd = self._process_config_vars(data=cmd, vars=largs, no_warn=True)
                        tmp = self._build_config(device=device, config_data=icmd,
                                                 action=action, path=path)
                        if tmp:
                            cmd_set.extend(tmp)
                        else:
                            t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                                format(device, path, str(icmd)))

                elif re.match(TEMPLATE_REG, knob):
                    matched = re.match(TEMPLATE_REG, knob)
                    template = matched.group(1)
                    args = cfg[knob]
                    tmp = self._config_template(device=device, template=template, path=path,
                                                action=action, args=args)
                    if tmp:
                        cmd_set.extend(tmp)
                    else:
                        t.log(level='debug', message='On {}, turn off cfg temp under {}:\n{}'.\
                                format(device, path, str(template)))
                elif re.match(r'bool:(False|True)', knob):
                    if re.match(r'bool:True', knob):
                        tmp = self._build_config(device=device, config_data=cfg[knob],
                                                 action=action, path=path)
                        if tmp:
                            cmd_set.extend(tmp)
                else:
                    args = cfg[knob]
                    toby_args = {'device_tag': device}
                    if kwargs.get('ifd_tag'):
                        toby_args['port_tag'] = kwargs['ifd_tag']
                        toby_args['port'] = kwargs['ifd']
                    tmp = OrderedDict([('cmd', knob), ('args', args), ('toby_args', toby_args)])
                    cmd_set.append(tmp)

        elif isinstance(cfg, (str, int, type(None))):
            if cfg is None:
                cfg = ''
            cfg = str(cfg)
            cfg = cfg.strip()
            if re.match(r'template\[\'\w+\'\]$', cfg):
                matched = re.match(r'template\[\'(\w+)\'\]$', cfg)
                template = matched.group(1)

                tmp = self._config_template(device=device, template=template, path=path,
                                            action=action)
                if tmp:
                    cmd_set.extend(tmp)
                else:
                    t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                            format(device, path, str(cmd)))
            else:
                cmd_set.append(cfg)


        else:
            raise Exception("config format unknown: " + str(cfg) + ' type: ' + str(type(cfg)))

        return cmd_set


    def _build_rt_config(self, device=None, config_data=None, path='', action='set', **kwargs):
        '''
        Usually used internally with config engine.

        take a piece of yaml config and compile it into actual device config list.
        This is the work horse of the config engine that traverse the yaml config
        content and process tags/templates.

        '''
        cmd_set = []
        cfg = config_data
        if isinstance(cfg, list):
            for cmd in cfg:
                tmp = self._build_rt_config(device=device, config_data=cmd, action=action,
                                            path=path, **kwargs)
                if tmp:
                    cmd_set.extend(tmp)
                else:
                    t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                         format(device, path, str(cmd)))

        elif isinstance(cfg, dict):
            for knob in cfg.keys():
                if not isinstance(knob, str):
                    raise Exception("dict config: knob is not a string: " + str(knob))

                # handle nested loops: LOOP(id:<<1..10>>, ip:<<>>):
                elif knob.startswith('LOOP('):
                    cmd = cfg[knob]
                    loop_iter = iter(config_utils.expand_to_list(base=knob.strip('LOOP() ')))
                    # start loops
                    for iloop in loop_iter:
                        largs = {}
                        for lvar in iloop.split(','):
                            lkey, val = lvar.split(':', 1)
                            largs[lkey.strip()] = val.strip()
                        icmd = self._process_config_vars(data=cmd, vars=largs, no_warn=True)
                        tmp = self._build_config(device=device, config_data=icmd,
                                                 action=action, path=path, **kwargs)
                        if tmp:
                            cmd_set.extend(tmp)
                        else:
                            t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                                format(device, path, str(icmd)))

                elif re.match(TEMPLATE_REG, knob):
                    matched = re.match(TEMPLATE_REG, knob)
                    template = matched.group(1)
                    args = cfg[knob]
                    tmp = self._config_template(device=device, template=template, path=path,
                                                action=action, args=args, **kwargs)
                    if tmp:
                        cmd_set.extend(tmp)
                    else:
                        t.log(level='debug', message='On {}, turn off cfg temp under {}:\n{}'.\
                                format(device, path, str(template)))
                elif re.match(r'bool:(False|True)', knob):
                    if re.match(r'bool:True', knob):
                        tmp = self._build_config(device=device, config_data=cfg[knob],
                                                 action=action, path=path, **kwargs)
                        if tmp:
                            cmd_set.extend(tmp)

                else:
                    args = {}
                    # args processing
                    for arg, val in cfg[knob].items():
                        # If the arg value is boolean Fasle, skip the arg
                        if not re.match(r'bool:False', str(val)):
                            args[arg] = val
                        # expand the arg data in case there are <<>>
                    toby_args = {'device_tag': device}
                    if kwargs.get('ifd_tag'):
                        toby_args['port_tag'] = kwargs['ifd_tag']
                        toby_args['port'] = kwargs['ifd']
                    #tmp = OrderedDict([('cmd', knob), ('args', args), ('toby_args', toby_args)])
                    tmp = {'cmd': knob, 'args': args, 'toby_args': toby_args}
                    cmd_set.append(tmp)

        elif isinstance(cfg, str):
            if re.match(r'template\[\'\w+\'\]$', cfg):
                matched = re.match(r'template\[\'(\w+)\'\]$', cfg)
                template = matched.group(1)

                tmp = self._config_template(device=device, template=template, path=path,
                                            action=action, **kwargs)
                if tmp:
                    cmd_set.extend(tmp)
                else:
                    t.log(level='debug', message='On {} turn off cfg under {}:\n {}'.\
                            format(device, path, str(cmd)))
            else:
                # probably user's high level method without args
                cfg = cfg.strip()
                cmd_set.append(cfg)

        else:
            raise Exception("config format unknown: " + str(cfg) + ' type: ' + str(type(cfg)))

        return cmd_set


    def _resolve_vars_in_file(self, load_file, **kwargs):
        '''
        config file may have tv/cv, yaml vars in it, resolve them
        upon request.
        '''
        with open(load_file, 'r') as f:
            old = f.read()
            try:
                res = self._process_cv(data=old, fail_nok=True)
            except:
                raise Exception('Unresolved tv/cv in config file {}'.format(load_file))

            res_file = 'res_' + load_file
        with open(res_file, 'w') as rf:
            rf.write(res)
            res = None
        return res_file


    def _load_rpc(self, device=None, rpc=None, **kwargs):
        '''
        load rpc onto device
        '''
        dev_hdl = self._get_dev_handle(device)   # from INIT Engine.
        try:
            res = dev_hdl.execute_rpc(command=rpc, **kwargs)
            self.status = res.status()
            self.response = 'On device {}, loaded RPC:\n {}\n Results: {}'.\
                    format(device, rpc, res.response())

            if self.status is True:
                t.log(level='debug', message='PASS: {}'.format(self.response))
            else:
                #raise Exception(self.response)
                raise Exception()
        except Exception as err:
            raise Exception('==Config Engine: ' + str(err) +'\n' + self.response)

        return self.status


    def _load_onto_device(self, device=None, **kwargs):
        '''
        Choose the right method to load config on various devices
        based on the handle type ( todo)

        .TBD: check size of config and decide if the string needs to be segmented to avoid
        scaling issues ( 20MB?)
        .other options.. save config to log, to device, , parallel, etc
        '''
        dev_hdl = self._get_dev_handle(device)   # from INIT Engine.
        osname = self.__get_cvar(cv_name=device + '__osname')
        #load file
        load_file = kwargs.get('load_file', None)
        cfg_list = kwargs.get('cfg_list', None)
        if (load_file is None) and (cfg_list is None):
            raise Exception('load_file/cfg_list is mandatory')


        if kwargs.get('resolve_vars'):
            if load_file is not None:
                # only do it if sepecifically asked to
                load_file = config_utils.find_file(load_file)
                with open(load_file, 'r') as f:
                    cfg_list = f.read()
            try:
                cfg_list = self._process_cv(data=cfg_list, fail_nok=True)
                # todo: process user VARS ?
            except:
                if load_file is not None:
                    raise Exception('Unresolved tv/cv in config file {}'.format(load_file))
                else:
                    raise Exception('Unresolved tv/cv in config string {}'.format(cfg_list))
            kwargs['cfg_list'] = cfg_list
            # tv/cv resolved and become a string. load directly as string
            load_file = None
            kwargs.pop('load_file', None)

        if (load_file is not None) and kwargs.get('remote_file'):
            msg = '== Config Engine: load local cfg {} on device {}'.\
                   format(load_file, device)
        elif load_file is not None:
            load_file = config_utils.find_file(load_file)
            kwargs['load_file'] = load_file
            msg = '== Config Engine: load cfg file {} to device {}'.\
                   format(load_file, device)
        elif cfg_list is not None:
            msg = '== Config Engine: load cfg string to device {}'.\
                   format(device)
            # log cfg_list here? it can be too long. TBD

        t.log(level='debug', message=msg + '....')
        kwargs['msg'] = msg
        if re.match(r'junos', osname, re.I):
            self._load_junos_cfg(device, **kwargs)
        elif re.match(REGEX_LINUX, osname, re.I):
            self._load_linux_cfg(device, **kwargs)
        elif re.match(r'Ix|Spirent', osname, re.I):
            self._load_tester_cfg(device, **kwargs)

        return self.status


    def _load_junos_cfg(self, device, *args, **kwargs):
        '''
        load JUNOS config
        '''

        dev_hdl = self._get_dev_handle(device)   # from INIT Engine.
        load_file = kwargs.get('load_file', None)
        cfg_list = kwargs.get('cfg_list', None)
        msg = kwargs.get('msg', 'load junos config')
        if cfg_list:
            if isinstance(cfg_list, list):
                cmd_str = '\n'.join(cfg_list)
            else:
                cmd_str = str(cfg_list)
            if re.search(r'^{} [-\w]+'.format(NO_SET), cmd_str, re.MULTILINE):
                kwargs['option'] = 'set'
        try:
            if kwargs.get('load') == 'config':
                if kwargs.get('remote_file'):
                    res = dev_hdl.load_config(**kwargs)
                elif load_file is not None:
                    res = dev_hdl.load_config(local_file=load_file, **kwargs)
                elif cmd_str is not None:
                    res = dev_hdl.load_config(cmd_str, **kwargs)
            elif kwargs.get('load') == 'terminal':
                dev_hdl.config(command_list=['load set terminal'], pattern='at a new line to end input')
                res = dev_hdl.config(command_list=[cmd_str + "\n"])
                if res.status() is True:                                           
                    self.response = msg + ' successful:\n' + res.response()        
                    t.log(level='debug', message=self.response)                                           
                    self.status = True                                             
                else:                                                              
                    self.response = msg + ' failed:\n' + res.response()            
                    t.log(level='error', message=self.response)                                  
                    self.status = False                                            
                    raise Exception(self.response)                                 

            cmd_str = None      # it can be a huge string. clean it up just in case.
            self.response = msg + ': successful'
            t.log(level='debug', message=self.response)
            self.status = True
        except Exception as err:
            if re.search(r'severity:\s+(warning|None).+bad_element: None', str(err)):
                self.response = (msg + "\nConfig warning on device: " + device + \
                      ":\n" + str(err))
                t.log(level='warn', message=self.response)
                self.status = True
            else:
                self.response = ("\nConfig failed on device: " + device + \
                      " with error:\n" + str(err))
                t.log(level='debug', message=self.response)
                self.status = False
                raise Exception('Failed to load config on ' + device + \
                        ' with error:\n' + str(err))

        return self.status

    def _load_linux_cfg(self, device, *args, **kwargs):
        '''
        load JUNOS config
        '''
        dev_hdl = self._get_dev_handle(device)   # from INIT Engine.

        # load_file:
        if kwargs.get('load_file'):
            #load saved config
            raise Exception('laod_file is not supported on linux server')

        # list of config APIs
        if kwargs.get('cfg_list'):
            for cmd in kwargs['cfg_list']:
                res = None
                if isinstance(cmd, str) and cmd.endswith(')'):
                    # either hldcl method or user added method if imported via hldcl handle
                    cmd = cmd.strip(r'() ')

                    if hasattr(dev_hdl, cmd):
                        cmd_method = getattr(dev_hdl, cmd.strip(r'() '))
                    else:
                        raise Exception('cannot find method {} for the linux object'.format(cmd))
                    try:
                        res = cmd_method()
                    except:
                        raise Exception('on {}, this cmd failed: {}'.format(device, cmd))

                elif isinstance(cmd, str):
                    # linux/unix shell commmand
                    # only available exception from hldcl is timeout, need more (To do)
                    res = dev_hdl.shell(command=cmd)
                elif isinstance(cmd, dict):
                    # methods from hldcl with args in dict form
                    api = cmd['cmd']
                    args = cmd.get('args')
                    toby_args = cmd.get('toby_args')
                    Save_in_cv = args.pop('_save_to_cv_', None)
                    pattern = args.pop('_pattern_', None)
                    if args:
                        args = self._process_rt_vars(data=args, **toby_args)
                    if api.endswith(')'):
                        if hassattr(dev_hdl, cmd):
                            cmd_method = getattr(dev_hdl, cmd.strip(r'() '))
                        else:
                            raise Exception('cannot find method {} for the linux object' \
                                            .format(api))
                        try:
                            res = cmd_method(**args)
                        except:
                            raise Exception('on {}, this cmd failed: {}'.format(device, api))
                    else:
                        #shell cmd with some toby args:
                        shell_args = {'command':api}
                        if pattern is not None:
                            shell_args['pattern'] = pattern
                            res = dev_hdl.shell(**shell_args)
                            # issue with manual 'su', that changes prompt from $ to #
                            # need a better way to handle prompt changes in unix
                            # dev_hdl.current_node.current_controller.set_prompt = '# '
                        else:
                            res = dev_hdl.shell(**shell_args)

                    if Save_in_cv:
                        local_path = []
                        if toby_args.get('device_tag'):
                            local_path.append(toby_args['device_tag'])
                        if toby_args.get('port_tag'):
                            local_path.extend(['interfaces', toby_args['port_tag']])

                        for retvar in Save_in_cv.keys():
                            key_path = Save_in_cv[retvar].strip('\"\' ')
                            # this will only work with return teh output as a dict
                            # todo: handle regex in linux output
                            retval = eval('res' + key_path)
                            cv_path = local_path + [retvar]
                            # store this result to self.c_dict:
                            config_utils.nested_set(self.c_dict, cv_path, retval, append=True)
                            cvkey = '__'.join([path for path in cv_path if path != 'interfaces'])
                            self.cv_flat[cvkey] = retval

        self.status = True
        return self.status


    def _load_tester_cfg(self, device, *args, **kwargs):
        '''
        load router tester config
        - as a saved file with load-file
        - or as a list of apis with cfg_list

        TODO: make it for each device type, and patch it to the device handle/class.
        '''
        dev_hdl = self._get_dev_handle(device)   # from INIT Engine.
        osname = self.__get_cvar(cv_name=device + '__osname')
        load_file = kwargs.get('load_file', None)
        cfg_list = kwargs.get('cfg_list', None)
        msg = kwargs.get('msg', 'load tseter config')
        if cfg_list:
            if isinstance(cfg_list, str):
                t.log(level='debug', message="split apis into a list: todo")
        try:
            if kwargs.get('remote_file'):
                #res =  dev_hdl.load_config(**kwargs)
                if re.match('SPIRENT', osname, re.I):
                    self._load_spirent_config(device=device, **kwargs)
                elif re.match('IxOS', osname, re.I):
                    self._load_ixia_config(device=device, **kwargs)
            elif load_file is not None:
                #res =  dev_hdl.load_config(local_file=load_file, **kwargs)
                if re.match('SPIRENT', osname, re.I):
                    self._load_spirent_config(device=device, local_file=load_file, **kwargs)
                elif re.match('IxOS', osname, re.I):
                    self._load_ixia_config(device=device, local_file=load_file, **kwargs)
            elif cfg_list is not None:
                #res = dev_hdl.load_config(dev_hdl, cfg_list, **kwargs)
                if re.match('SPIRENT', osname, re.I):
                    self._load_spirent_config(device=device, cfg=cfg_list, **kwargs)
                elif re.match('IxOS', osname, re.I):
                    self._load_ixia_config(device=device, cfg=cfg_list, **kwargs)
            cfg_list = None      # it can be a huge string. clean it up just in case.
            self.response = msg + ': successful'
            t.log(level='debug', message=self.response)
            self.status = True
        except Exception as err:
            self.response = ("\nConfig failed on device: " + device + \
                  " with error:\n" + str(err))
            t.log(level='debug', message=self.response)
            self.status = False
            raise Exception('Failed to load config on ' + device)

        return self.status


    def _load_spirent_config(self, device, **kwargs):
        '''
        temp. method, will be moved to a separate file, and patched into
        config engine  ( or by inheriting device class)
        '''

        dev_hdl = self._get_dev_handle(device)

        # load_file:
        if kwargs.get('load_file'):
            # find port list:
            if kwargs.get('port_list'):
                port_list = kwargs['port_list']
            else:
                port_list = dev_hdl.port_list
            #load saved config
            res = dev_hdl.invoke('load_xml', filename=kwargs['load_file'])
            #reconnect:
            res = dev_hdl.invoke('connect', device=dev_hdl.chassis, port_list=port_list)
            dev_hdl.session_info = res
            dev_hdl.port_to_handle_map = res['port_handle'][dev_hdl.chassis]
            for port in dev_hdl.port_to_handle_map:
                dev_hdl.handle_to_port_map[dev_hdl.port_to_handle_map[port]] = port

            for intf_tag, port_name in dev_hdl.intf_to_port_map.items():
                config_utils.nested_set(self.c_dict, [device, 'interfaces', intf_tag, 'porthandle'],
                                        dev_hdl.port_to_handle_map[port_name])

        # list of config APIs
        if kwargs.get('cfg_list'):
            # HLTAPI optimization: avoid 'apply' for each API call
            if kwargs.get('no_stc_optimization') is None:
                dev_hdl.invoke('test_control', action='enable')
            for cmd in kwargs['cfg_list']:
                api = cmd['cmd']
                args = cmd.get('args')
                toby_args = cmd.get('toby_args')
                Save_in_cv = args.pop('_save_to_cv_', None)
                if args:
                    args = self._process_rt_vars(data=args, **toby_args)
                    res = dev_hdl.invoke(api, **args)
                else:
                    # could be a high level user API without args
                    res = dev_hdl.invoke(api)
                if Save_in_cv:
                    local_path = []
                    if toby_args.get('device_tag'):
                        local_path.append(toby_args['device_tag'])
                    if toby_args.get('port_tag'):
                        local_path.extend(['interfaces', toby_args['port_tag']])

                    for retvar in Save_in_cv.keys():
                        key_path = Save_in_cv[retvar].strip('\"\' ')
                        retval = eval('res' + key_path)
                        if isinstance(retval, str) and re.search(r'\S+\s+\S+', retval):
                            dev_hdl.log('returned value is space sperated, convert to list')
                            retval = [handle.strip() for handle in retval.split()]
                        cv_path = local_path + [retvar]
                        # store this (handle) to self.c_dict:
                        config_utils.nested_set(self.c_dict, cv_path, retval, append=True)
                        cvkey = '__'.join([path for path in cv_path if path != 'interfaces'])
                        #self.cv_flat[cvkey] = retval
                        self.cv_flat[cvkey] = config_utils.nested_get(self.c_dict, *cv_path)

            if kwargs.get('save_config'):
                dev_hdl.invoke('save_xml', filename=device + '.' + kwargs['save_config'])

            if kwargs.get('no_stc_optimization') is None:
                # now apply all API calls on STC:
                dev_hdl.invoke('test_control', action='sync')
                # reset to per API apply before leaving CE.
                dev_hdl.invoke('test_control', action='disable')



    def _load_ixia_config(self, device, **kwargs):
        '''
        temp. method, will be moved to a separate file, and patched into
        config engine  ( or by inheriting device class)
        '''

        dev_hdl = self._get_dev_handle(device)

        # load saved file:
        if kwargs.get('load_file'):
            # find port list:
            if kwargs.get('port_list'):
                port_list = kwargs['port_list']
            else:
                port_list = dev_hdl.port_list

            #reconnect to load saved config:
            load_file = kwargs['load_file']
            if kwargs.get('remote_file'):
                raise Exception('cannot do load_file locally on device for ixia')
                #load_file = kwargs['remote_file']

            t.log(level='debug', message='Cleanup existing ixia session:')
            old_dh = dev_hdl
            res = dev_hdl.cleanup()

            t.log(level='debug', message='Recreate ixia handle:')
            system = self.c_dict[device]['system']
            dev_hdl = Device(system=system)
            dev_hdl.add_intf_to_port_map(old_dh.intf_to_port_map)
            dev_hdl.add_interfaces(old_dh.interfaces)
            dev_hdl.global_logger = old_dh.global_logger
            dev_hdl.device_logger = old_dh.device_logger
            dev_hdl.connect_args['config_file'] = load_file
            dev_hdl.connect_args.pop('reset', None)

            t.log(level='debug', message='Reconnect and load ixia config file:')
            dev_hdl.connect(port_list=port_list)
            t.t_dict['resources'][device]['system']['dh'] = dev_hdl

            # re-populate port handles to CV
            for intf_tag, port_name in dev_hdl.intf_to_port_map.items():
                config_utils.nested_set(self.c_dict, [device, 'interfaces', intf_tag, 'porthandle'],
                                        dev_hdl.port_to_handle_map[port_name])
                self.cv_flat['__'.join([device, intf_tag, 'porthandle'])] = \
                    dev_hdl.port_to_handle_map[port_name]

        # list of config APIs
        if kwargs.get('cfg_list'):
            for cmd in kwargs['cfg_list']:
                api = cmd['cmd']
                args = cmd.get('args')
                toby_args = cmd.get('toby_args')
                Save_in_cv = args.pop('_save_to_cv_', None)
                if args:
                    args = self._process_rt_vars(data=args, **toby_args)
                    res = dev_hdl.invoke(api, **args)
                else:
                    # could be a user high level API without args
                    res = dev_hdl.invoke(api)
                if Save_in_cv:
                    local_path = []
                    if toby_args.get('device_tag'):
                        local_path.append(toby_args['device_tag'])
                    if toby_args.get('port_tag'):
                        local_path.extend(['interfaces', toby_args['port_tag']])
                    t.log(level='debug', message='retrieve data from API result, save under {}:' \
                          .format('__'.join(local_path)))
                    for retvar in Save_in_cv.keys():
                        key_path = Save_in_cv[retvar].strip('\"\' ')
                        try:
                            retval = eval('res' + key_path)
                        except KeyError:
                            raise Exception('can not find handle {} from API result' \
                                            .format(key_path))
                        cv_path = local_path + [retvar]
                        # store this (handle) to self.c_dict:
                        config_utils.nested_set(self.c_dict, cv_path, retval, append=True)
                        cvkey = '__'.join([path for path in cv_path if path != 'interfaces'])
                        #self.cv_flat[cvkey] = retval
                        self.cv_flat[cvkey] = config_utils.nested_get(self.c_dict, *cv_path)
            if kwargs.get('save_config'):
                ## Todo
                pass

    #### utils . ####

    def _process_rt_vars(self, data, device_tag, port_tag=None, **kwargs):
        '''
        resolve cv variables that dynamically generated during RT API calls,
        such as handles.
        it may just have the name such as cv['bgphandle'],
        look for local cv with device/port tag first,
        if not resovled, look for cv under device_tag, at last, look for 'global cv's
        '''
        kwargs['device_tag'] = device_tag
        if port_tag is not None:
            kwargs['port_tag'] = port_tag

        '''
        # check local port cv first
        if port_tag is not None:
            cv_path = '{}__{}'.format(device_tag, port_tag)
            data = self._process_cv(data=data, prepend_path=cv_path)

        # then check device node cv (do not go down to other interfaces)
        cv_path = device_tag
        data = self._process_cv(data=data, prepend_path=cv_path, exact_match=True)
        '''
        # at last, check global cv.
        #data = self._process_cv(data=data, exact_match=True)
        data = self._process_cv(data=data, **kwargs)


        return data

    def _get_ifd_from_tag(self, device_tag, ifd_tag):
        '''
        return ifd name with give device_tag and ifd_tag in params
        '''

        ifd_cvar = device_tag.lower() + '__interfaces__' + ifd_tag.lower() +'__pic'
        ifd = self.__get_cvar(cv_name=ifd_cvar)
        if ifd is None:
            raise Exception('cannot find ifd tag {} in {}'.format(ifd_tag, device_tag))

        return ifd


    def _get_dev_handle(self, resource):
        '''
        retrieve device handle from t

        :param resource:
            **REQUIRED** device tag/name as shown in the t (or toby yaml file)
                         is also accepts a host description( IP) if available in device_handle_map
        :return: device handle

        '''

        # Most probably it is a device alias  in params / t (r0, ht0, ..)
        try:
            dev_os = tv[resource + '__osname']
            dev_hdl = t.get_handle(resource=resource)
            return dev_hdl
        except:
            t.log(level='debug', message='cannot find device handle for {} in t'.format(resource))

        # if not, it might be a host mapped to a device handle
        if self.device_handle_map.get(resource):
            dev_hdl = self.device_handle_map[resource]
        else:
            # last try, it might be a device name
            for dev in t.resources:
                if t.resources[dev]['system']['primary']['name'] == resource:
                    dev_hdl = t.get_handle(resource=dev)
                    break
            else:
                # out of luck, cannot find a handle
                raise Exception('cannot find device handle for {}'.format(resource))

        return dev_hdl


    def _get_role_value(self, role=None):
        '''
        get role value from a given role tag
        '''
        if isinstance(role, str):
            (role_name, role_value) = (role, '')
        elif isinstance(role, dict):
            (role_name, role_value), = role.items()
        else:
            role_type = type(role)
            raise Exception('Wrong Tagging Format: {}. \
                    only str or dict allowed'.format(role_type))

        return (role_name, role_value)


    def _save_interface_role_tags(self, role_tags=None, device_tag=None, ifd_tag=None):
        '''
        save interface role tags for a given device/ifd
        '''

        #tags = dev_cfg['interfaces'][intf_tag]['TAGS']
        if not isinstance(role_tags, dict):
            msg = '''
            Wrong Interface Tagging Format on {}, {}: {}
            only dict allowed.
            interfdace role tag format should use either ifd or ifl_xx as key:
             r0r1_2:
                TAGS:
                  ifd: [rsvp, mpls, isis]
                  ifl_<<1..8>>: [ospf]

            '''.format(device_tag, ifd_tag, role_tags)
            raise Exception(msg)

        for if_group, role_list in role_tags.items():
            if not re.match(r'^ifd|ifl_(.+)$', if_group.lower()):
                raise Exception('Wrong Interface TAG format on device {} ifd {}: {}'. \
                        format(device_tag, ifd_tag, if_group))
            for role in role_list:
                (role_name, role_value) = self._get_role_value(role=role)
                config_utils.nested_set(self.roles, ['INTERFACE', role_name, device_tag,
                                                     ifd_tag, if_group], role_value)


    def _process_role_tags(self, cfg_data=None):
        '''
        process/save role tags from the user yaml config file
        '''

        # TBD: global role tags outside devices

        for level in ('NODE', 'INTERFACE'):
            if self.roles.get(level) is None:
                self.roles[level] = {}

        # get role tags from each device
        for device_tag in  cfg_data.keys():
            if device_tag in NONE_DEVICE_KNOBS:
                continue
            dev_cfg = cfg_data[device_tag]

            # node level tags
            if dev_cfg.get('TAGS'):
                for role in dev_cfg['TAGS']:
                    (role_name, role_value) = self._get_role_value(role=role)
                    config_utils.nested_set(self.roles,
                                            ['NODE', role_name, device_tag], role_value)

            # interface level tags
            if dev_cfg.get('interfaces'):
                for intf_tag in dev_cfg['interfaces']:
                    if dev_cfg['interfaces'][intf_tag].get('TAGS'):
                        tags = dev_cfg['interfaces'][intf_tag]['TAGS']
                        self._save_interface_role_tags(device_tag=device_tag, \
                                ifd_tag=intf_tag, role_tags=tags)

        # now make tags available in CV
        for node_tag in self.roles['NODE']:
            self.cv_flat[node_tag + '__list'] = list(self.roles['NODE'][node_tag].keys())

        for intf_tag in self.roles['INTERFACE']:
            if_tag_list = []
            for dev_tag in self.roles['INTERFACE'][intf_tag]:
                if_tag_list += list(dev_tag + '__' + if_tag \
                    for if_tag in self.roles['INTERFACE'][intf_tag][dev_tag].keys())

            self.cv_flat[intf_tag + '__list'] = if_tag_list

            # treat 'load'
        #for tag in self.roles
    def _process_cv(self, data=None, var_delimiter=TV_DELIMITER, **kwargs):
        '''
        Translate flatterned tv/cv into actual value
        used internally in config engine for now

        '''

        if data is None:
            return data

        if not re.search(r'{0[0]}(.+?){0[1]}'.format(var_delimiter), str(data)):
            return data

        if isinstance(data, list):
            newdata = []
            for elm in data:
                newelm = self._process_cv(data=elm, **kwargs)
                if isinstance(newelm, list):
                    newdata.extend(newelm)
                else:
                    newdata.append(newelm)
        elif isinstance(data, dict):
            newdata = OrderedDict()
            for key, value in data.items():
                newkey = self._process_cv(data=key, **kwargs)
                newval = self._process_cv(data=value, **kwargs)
                if isinstance(newkey, (str, int, float)):
                    newdata[str(newkey)] = newval
                elif isinstance(newkey, list):
                    for nkey in newkey:
                        newdata[str(nkey)] = newval
                elif isinstance(newkey, dict):
                    for nkey, nvalue in newkey.items():
                        ## take the value comes with the key dit, ignore existing dict value.
                        newdata[nkey] = nvalue

        else:
            # get down to a single string now, resolve cv's in it
            newdata = self._resolve_cv(data, **kwargs)
        return newdata

    def _resolve_cv(self, data, var_delimiter=TV_DELIMITER, **kwargs):
        '''
        resolve all tv/cv in a string
        '''

        # if no tv/cv pattern found, return original data
        if not re.search(r'{0[0]}(.+?){0[1]}'.format(var_delimiter), str(data)):
            return data

        # search cv['xxx'] / cv[\'xxx\'] in strings
        # each element in list_cv is a tuple (cv['r0__r0r1__pic'], 'r0_r0r1_pic')
        ##listp = re.compile(r'({0[0]}(.+?){0[1]})'.format(var_delimiter))
        listp = re.compile(r'({0[0]}(.+?){0[1]}((?:\[[^\]]+\])*))'.format(var_delimiter))
        list_cv = listp.findall(str(data))
        # remove duplicated tags:
        list_cv = list(OrderedDict.fromkeys(list_cv))
        key_disp = {}
        for cvar in list_cv:
            fail_ok = True
            ###
            new_key = cvar[1]

            if cvar[2]:
                # for legacy cv['device0__link1__unit__0__ip[2]'], rip the list part into index
                # so that __get_cvar() doesn't need to woory about it.
                kwargs['index'] = cvar[2]
            else:
                kwargs['index'] = None
            #if kwargs.get('prepend_path') and (not re.search('__', new_key)):
                #new_key = kwargs['prepend_path'] + '__' + new_key

            # handle tv first:
            if cvar[0].startswith('tv['):
                # allow legacy tv in config engine to avoid breaking scripts in regression
                # but block future use of tv in new script via ETRANS checking..
                t.log(level='warn', message="ETRANS: do not use {} in config engine. use cv['{}'] instead" \
                      .format(cvar[0], cvar[1]))
                try:
                    key_disp[cvar[0]] = tv[cvar[1]]
                except Exception as err:
                    t.log(level='debug', message='cannot find {} in tv:\n{}'.format(cvar[0], str(err)))

                continue

            #matched = re.match(r'(localport|localsystem):\s*(.+)', new_key)
            matched = re.match(r'([-\w]+):\s*(.+)', new_key)
            if matched:
                local_search = matched.group(1)
                new_key = matched.group(2)
                if local_search.lower() == 'localport':
                    if kwargs.get('port_tag') and kwargs.get('device_tag'):
                        new_key = '__'.join([kwargs['device_tag'], kwargs['port_tag'], new_key])
                        val = self.__get_cvar(cv_name=new_key, **kwargs)
                    else:
                        t.log(level='debug', message='missing port_tag and/or device_tag for ' + cvar[0])
                        val = None
                elif local_search.lower() == 'localsystem':
                    if kwargs.get('device_tag'):
                        new_key = '__'.join([kwargs['device_tag'], new_key])
                        kwargs['exact_match'] = True
                        val = self.__get_cvar(cv_name=new_key, **kwargs)
                    else:
                        t.log(level='debug', message='missing device_tag for ' + cvar[0])
                        val = None
            else:
                val = self.__get_cvar(cv_name=new_key, **kwargs)

            if val is None:     # cannot find cvar
                if kwargs.get('fail_nok'):
                    raise Exception('cannot find {} in c_dict'.format(cvar[0]))
                else:
                    continue

            key_disp[cvar[0]] = val

        # replace cvars in data with values found in tdict(self.c_dict)

        for cvar, val in key_disp.items():
            raw_cvar = re.escape(cvar)
            if data.strip() == cvar:
                # if the value is a single cv, it can take any data structure
                # for example, in case of tester API args: handles: [1,2,3]
                data = val
            elif isinstance(val, (str, int)):
                data = re.sub(raw_cvar, str(val), data)

            else:
                # if a cv in embeded in a string, and even with other cvs
                # it is ambigeous if one of the cvs is a data structure
                t.log(level='warn', message='{} returned a data structure, not a value in:\n{}'.\
                                format(cvar, data))
                continue
        return data

    def __get_cvar(self, cv_name=None, delimiter='__', return_path=None, **kwargs):
        '''
        cvar is a super set of t.t_dict, with more config related data added to it.
        This method originally retrieved data from t directly as 'tv'. With tv moved up
        to toby framewokr (mostly topology related), 'cv' is introduced in config engine.
        with 'cv', all 'tv', t_dict data are still available.

        Dynamic  data driven method to retrieve value inside config engine object
        in a flatterned, concise format.(default delimiter of knobs is '__'
        double underscores)

        used intervally in config engine.

        for example, a pic can be found in the data structure as:

          obj.c_dict[device0][interfaces][link1][pic]

        The cvar expression:

          cv['device0__link1__pic']

        is equivalent to:

          cv['device0__interfaces__link1__pic']

          Legacy CE supports only a list format in CV
          if the returned value is a list, you can use python's list expression to
          get any data from the list
          cv['device0__link1__unit__0__ip[:]']  # get whole list
          cv['device0__link1__unit__0__ip[0]']  # get first element, also works if ip is not a list
          cv['device0__link1__unit__0__ip[2]']  # get 3rd element, fail if ip is not a list
          cv['device0__link1__unit__0__ip[-1]']  # get last element
          # tv['device0__link1__unit__0__ip']  # still get first element if ip is a list
          # change this behavior by taking the whole list for simplicity and making no assumption
          # This will also take ANY data structure.as part of fix to toby-2283 and 3020
          !!!!
          Now CE supports uv/cv/args in any data format, and can be accesse in config yaml:
          cv['device0']['interfaces']['link1']['unit'][0]['ip'][1]
          cv['r0__uv-abc']['key1']['key2']['lsit1'][-1]
          ...
         '''

        if cv_name is None:
            raise Exception("Mandatory arg 'cv' is missing")
        if not self.c_dict:
            self.__make_c_dict()

        key_list = cv_name.split(delimiter)
        if kwargs.get('index') and kwargs['index'] is not None:
            # syntax of cv['my_uv_dict']['as'][0] has the index part passed in as '['as'][0]'
            # the legacy cv['my_cv_list[0]'] syntax is also accepted here, but the format is
            # now '[0]', instead of '0'
            index = kwargs['index']
        else:
            index = None
            # legacy syntax of dealing with list dat in cv cv['uv_my_ip[2]']
            # for backward compatibility. should better be cv['uv_my_ip'][2]
            listitem = re.match(r'[-\w]+(\[(?:.*)\])', key_list[-1])
            if listitem is not None:
                index = listitem.group(1)
                key_list[-1] = re.sub(r'\[.*\]\s*$', '', key_list[-1])

        c_var = None
        t_key = '__'.join(key_list)
        if t_key in tv.keys() and tv[t_key] is not None:
            c_var = tv['__'.join(key_list)]
        elif self.cv_flat.get('__'.join(key_list)):
            c_var = self.cv_flat['__'.join(key_list)]
        else:
            if kwargs.get('exact_match'):
                path = key_list
                c_var = config_utils.nested_get(self.c_dict, *path)
            else:
                c_var, path = self._find_dict_data(data=self.c_dict, key_list=key_list)

        if c_var is None:
            if kwargs.get('exact_match'):
                t.log(level='debug', message='cannot find exact match for {} in c_dict' \
                      .format(cv_name))
            else:
                t.log(level='debug', message='cannot find {} in c_dict'.format(cv_name))

        #elif isinstance(c_var, list) and index is None:
            # assuming you are looking for the first element
            # you might not aware it is a list
            # change this behavior by taking the whole list for simplicity and making no assumption
            # This will also take ANY data structure.as part of fix to toby-2283 and 3020
            #!!!!
            #c_var = c_var[0]

        elif isinstance(c_var, (list, dict)) and index is not None:
            try:
                c_var = eval('c_var{}'.format(index))
            except Exception as err:
                t.log(level='error', message=err)
                t.log(level='error', message='cv {} might be out of range: {}'.\
                        format(cv_name, str(c_var)))
                c_var = cv_name
        elif (index is not None) and (str(index) not in ('[0]', '[-1]')):
            # if c_var is not a list, cvar[0], cvar[-1] still work in case the output
            # may be a list or a single value, but if index is other than this, don't take it
            raise Exception('cvar {} can not be accessed as a list'.format(cv_name))

        return c_var if return_path is None else (cvar, path)


    def _get_config_var(self, var=None, device=None, index=None, **kwargs):
        '''
        internal use to find value of defined vars
        '''
        if var is None:
            raise Exception("Mandatory arg 'var' is missing")
        if kwargs.get('vars'):
            defined_vars = kwargs['vars']
        else:
            defined_vars = self.vars
        listitem = re.match(r'([-\w]+)(\[(?:.*)\]\s*$)', var)
        var_name = var

        if (device is not None) and defined_vars.get(device):
            val = defined_vars[device].get(var_name)
            if val is None:
                val = defined_vars.get(var_name)
        else:
            val = defined_vars.get(var_name)
        # if accessing a data structure:
        if val is None:
            t.log(level='debug', message='cannot find {} in VARS'.format(var))
        elif isinstance(val, (list, dict)) and index is not None:
            try:
                val = eval('val{}'.format(index))
            except Exception as err:
                t.log(level='error', message=err)
                t.log(level='error', message='var {} cannot get data from: {}'.\
                        format(var, str(val)))
                val = var

        # todo: more exception handling
        return val




    def _process_config_vars(self, device=None, data=None, var_delimiter=ARG_REG, **kwargs):
        '''
        internal function
        resolve config vars var['xxx'] in config data
        '''

        if data is None:
            #return ''
            return data
            #raise Exception("mandatory 'data' is missing")

        #if no var['xx'] in the data, return as is
        if not re.search(ARG_REG, str(data)):
            return data
        if isinstance(data, list):
            newdata = []
            for elm in data:
                newelm = self._process_config_vars(data=elm, device=device, **kwargs)
                if isinstance(newelm, list):
                    newdata.extend(newelm)
                else:
                    newdata.append(newelm)
        elif isinstance(data, dict):
            newdata = OrderedDict()
            for key, value in data.items():
                newkey = self._process_config_vars(data=key, device=device, **kwargs)
                newval = self._process_config_vars(data=value, device=device, **kwargs)
                if isinstance(newkey, (str, int, float)):
                    newdata[str(newkey)] = newval
                elif isinstance(newkey, list):
                    for nkey in newkey:
                        newdata[str(nkey)] = newval
                elif isinstance(newkey, dict):
                    for nkey, nvalue in newkey.items():
                        ## take the value comes with the key dit, ignore existing dict value.
                        newdata[nkey] = nvalue

                else:
                    raise Exception('key {} is not a str or list'.format(str(newkey)))

        else:
            c_dict = re.findall(ARG_REG, str(data))

            data_set = [data]
            val_set = []
            for var_tag, var, subkey in c_dict:
                raw_var_tag = re.escape(var_tag)
                val = self._get_config_var(var=var, device=device, index=subkey, **kwargs)
                new_set = []
                for elem in data_set:
                    if val is None:
                        if kwargs.get('no_warn'):
                            t.log(level='debug', message="cannot resolve var['{}'] yet, leave it as is" \
                                  .format(var))
                        else:
                            pass
                            #t.log(level='warn', message="cannot resolve var['{}'], leave it as is".format(var))
                        new_set.append(elem)
                    elif isinstance(val, bool):
                        val = 'bool:{}[{}]'.format(str(val), var)
                        new_set.append(re.sub(raw_var_tag, str(val), str(elem)))
                        val_set.append(val)
                    elif isinstance(val, (str, int, float)):
                        new_set.append(re.sub(raw_var_tag, str(val), str(elem)))
                        val_set.append(val)
                    elif elem.strip() == var_tag:
                        # if the element is a single var, it can take any data structure
                        # for example, in case of tester API args: handles: [1,2,3]
                        new_set.append(val)
                        val_set.append(val)
                    elif isinstance(val, list):
                        new_set.extend([re.sub(raw_var_tag, str(ele), str(elem)) for ele in val])
                        val_set.append(val)
                    else:
                        err_msg = 'template args accept on str/int or list, ' + \
                                    'check "{}" in "{}"\n'.format(str(var), str(data)) + \
                                    'if a variable inside a string is a dict,' + \
                                    "it is ambigeous.  dict is acceptable only when a varaible" + \
                                    " is a single key or value"
                        # ,
                        t.log(level='error', message='args value accepts only str/int or list')
                        raise Exception(err_msg)
                data_set = new_set

            if len(data_set) == 1:
                newdata = data_set[0]
                #newdata = data_set
            else:
                newdata = data_set
            if re.search(ARG_REG, str(newdata)) and val_set:
               newdata = self._process_config_vars(data=newdata, device=device, **kwargs)

        return newdata



    def _process_args(self, device=None, data=None, **kwargs):
        '''
        internal function
        process arguments to resolve cvar, config/template vars
        '''
        if data is None:
            return data

        newdata = data
        # get config/template vars
        newdata = self._process_config_vars(data=newdata, device=device, **kwargs)
        # get c_dict
        #newdata = self._process_cv(data=newdata)

        return newdata

    def _get_role_attr(self, device_tag=None, tag=None, role_type=None):
        '''
        get attributes defined under TAGS in config yaml file
        tag['ospf'], tag['pe@neighbor:loop-ip'], etc
        translate and expand the tags into a dict of valules
        based on TAGS defined in config yaml file
        '''
        role_pat = r'(\w+)(?:@(\w+))?(?::(.+))?'
        mat = re.match(role_pat, tag)
        if mat:
            role = mat.group(1)
            scope = mat.group(2) if mat.group(2) else None
            var = mat.group(3) if mat.group(3) else None
        else:
            t.log(message='role tag {} should have only letter, number and _'.format(tag), level='error')
            raise Exception('role tag {} syntax error in {}'.format(tag, device_tag))

        if role_type is None:
            type_list = ['INTERFACE', 'NODE']
        else:
            type_list = [role_type.upper()]
            role_type = None

        # check role tag is defined in TAGS
        for ttype in type_list:
            if self.roles[ttype].get(role):
                role_type = ttype
                break

        if role_type is None:
            raise Exception('undefined role TAG {} in role types: [{}]'.format(tag, str(type_list)))

        # use deepcopy to avoid affecting self.roles.
        attr_nodes = copy.deepcopy(self.roles[role_type][role])
        attr_dict = {}
        if role_type == 'NODE':
            # handling scope first, reduce device list with scope
            if scope is not None:
                if scope.lower() == 'neighbor':
                    if device_tag in attr_nodes:
                        attr_nodes.pop(device_tag)
                if scope.lower() == 'local':
                    if device_tag in attr_nodes:
                        attr_nodes = {device_tag: attr_nodes[device_tag]}

            if var is None:
                # take the node tag by default
                attr_dict.update(attr_nodes)
            else:
                for dev in attr_nodes:
                    cv_name = '{}__{}'.format(dev, var)
                    cvar = self.__get_cvar(cv_name=cv_name)
                    if cvar is None:
                        raise Exception('cannot find value for role tag {} in {}'.\
                                format(tag, device_tag))
                    attr_dict[cvar] = attr_nodes[dev]

        elif role_type == 'INTERFACE':
            if scope is not None:
                if scope.lower() == 'neighbor':
                    if device_tag in attr_nodes:
                        attr_nodes.pop(device_tag)
                elif scope.lower() == 'remote':
                    # interface role tag pointing to remote, todo
                    # can be tag['ebgp@remote:unit__0__ip_addr']
                    # need to pass ifd tag ? or let the specific role tag handles it
                    pass
                else:
                    # probably a (list of) device tag(s): tbd
                    # can be tag['ebgp@r1:unit__0__ip_addr']
                    # probably don't need to do this since it is hard coding
                    # not tagging.
                    pass
            else:
                # deafult is local INTERFACE level tag
                if device_tag is not None:
                    attr_nodes = {device_tag: self.roles['INTERFACE'][role].get(device_tag, {})}
                    # ok if the tag is removed from the device,
                    # will skip configure if attr_nodes is empty

            if var is None:
                # ospf:pic (default), ebgp:ip_addr
                var = 'pic'

            for dev in attr_nodes:
                for ifd_tag in attr_nodes[dev]:

                    for if_group, options in attr_nodes[dev][ifd_tag].items():
                        if if_group.lower() == 'ifd':
                            cv_name = '{}__{}__{}'.format(dev, ifd_tag, var)
                            cvar = self.__get_cvar(cv_name=cv_name)
                            if cvar is None:
                                raise Exception('cannot find value for role tag {} in {} {}'. \
                                                format(tag, dev, ifd_tag))
                            attr_dict[cvar] = attr_nodes[dev][ifd_tag]['ifd']
                        elif re.match(r'ifl_(.+)', if_group.lower()):
                            # expand the if_group to list of ifls
                            ifl_range = re.match(r'ifl_(.+)', if_group.lower())
                            if re.search(r'<<.+>>', ifl_range.group(1)):
                                ifl_list = config_utils.expand_to_list(base=ifl_range.group(1))
                            else:
                                ifl_list = [ifl_range.group(1)]

                            for ifl in ifl_list:
                                if re.match(r'ip.*', var):
                                    cv_name = '{}__{}__unit__{}__{}'.format(dev, ifd_tag, ifl, var)
                                    cvar = self.__get_cvar(cv_name=cv_name)
                                    if cvar is None:
                                        raise Exception('cannot find value for role tag \
                                                {} in {} {}'.format(tag, dev, ifd_tag))
                                    #attr_dict[cvar] = attr_nodes[dev][ifd_tag][if_group]
                                    attr_dict[cvar] = options
                                else:
                                    cv_name = '{}__{}__{}'.format(dev, ifd_tag, var)
                                    cvar = self.__get_cvar(cv_name=cv_name)
                                    if cvar is None:
                                        raise Exception('cannot find value for role tag \
                                                {} in {} {}'.format(tag, dev, ifd_tag))
                                    #attr_dict[cvar+'.'+ifl] = attr_nodes[dev][ifd_tag][if_group]
                                    attr_dict[cvar+'.'+ifl] = options




        return attr_dict




    def _role_expand(self, device=None, base=None, tag_regex=ROLE_REG):
        '''
        expand set cmd if there is role tag in it.
        '''
        #get list of role tags
        listp = re.compile(tag_regex)
        list_tags = listp.findall(base)
        if not list_tags:
            return [base]
        # remove duplicated tags:
        list_tags = list(OrderedDict.fromkeys(list_tags))
        key_disp = {}
        #get attr for each role
        for tag, role in list_tags:
            attr = self._get_role_attr(tag=role, device_tag=device)
            key_disp[tag] = []
            for key, val in attr.items():
                if isinstance(val, str):
                    val = [val]
                for ele in val:
                    if ele == '':
                        key_disp[tag].append(key)
                    else:
                        key_disp[tag].append(key + ' ' + str(ele))

        # replace role in base with expand attributes
        exp_cfg = []
        for tag in key_disp:
            raw_tag = re.escape(tag)
            for ele in key_disp[tag]:
                newdata = re.sub(raw_tag, str(ele), base)   ###
                exp_cfg.append(newdata)

        exp_cfg.sort(key=config_utils.str_sort_key)

        return exp_cfg

    def _expand_config(self, config_list=None, device=None):
        '''
        expand config with scaling tools, mainly for internal use
        '''
        # todo:  Rx in cv, user functions? etc
        # going through each cmd and expand
        exp_cmds = []
        for cfg in config_list:
            if isinstance(cfg, str):
                temp_list = config_utils.expand_to_list(base=cfg)
                if isinstance(temp_list, list):
                    exp_cmds.extend(temp_list)
                else:
                    exp_cmds.append(str(temp_list))
            elif isinstance(cfg, dict):
                if cfg.get('args'):
                    for arg in cfg['args']:
                        # assuming a flat key/value structure for args
                        # ( todo: deal with complex data)
                        if isinstance(cfg['args'][arg], str) and \
                                      re.search(r'<<.+>>', cfg['args'][arg]):
                            cfg['args'][arg] = config_utils.expand_to_list(base=cfg['args'][arg])
                        if isinstance(cfg['args'][arg], list):
                            val_list = []
                            for val in cfg['args'][arg]:
                                if isinstance(val, str) and re.search(r'<<.+>>', val):
                                    new_val = config_utils.expand_to_list(base=val)
                                    val_list.append(new_val)
                                else:
                                    val_list.append(val)
                            cfg['args'][arg] = val_list
                exp_cmds.append(cfg)

            else:
                exp_cmds.append(cfg)
        # expand ROLE TAGs
        cfg_list = []
        exp_cmds = self._process_cv(data=exp_cmds)

        for cfg in exp_cmds:
            if isinstance(cfg, str):
                temp_list = self._role_expand(device=device, base=cfg)
                cfg_list.extend(temp_list)
            else:
                cfg_list.append(cfg)

        return cfg_list

    def _find_dict_data(self, data, key_list, path=None):
        '''
        used internally to dynamically retrieve t_vars from t dictionary
        the key_list can be a subset of the complete tree that traverse
        from root to the leaf value, as long as the list is unique, this makes
        the dynamic t_var expression concise.
        '''
        if path is None:
            path = []
        value = None
        first_key = key_list[0]
        if first_key in data.keys():
            path.append(key_list.pop(0))
            if key_list:
                if isinstance(data, dict):
                    value, path = self._find_dict_data(data=data[first_key],
                                                       key_list=key_list, path=path)
            else:
                # find it.
                value = data[first_key]
        else:
            for subkey in data.keys():
                if isinstance(data[subkey], dict):
                    path.append(subkey)
                    value, path = self._find_dict_data(data=data[subkey],
                                                       key_list=key_list, path=path)
                    if value is None:
                        path.pop()
                    else:
                        # find it
                        break

        return value, path



    def get_cv(self, cv=None, reconnect=False, cv_file=None):
        '''
        share flat cv in robot
        
        DESCRIPTION:
            recoonect is for spirent reconnect, when you can get the CV
            data with all handles back after reconnect.

        ARGUMENTS:
            [cv=None, reconnect=False, cv_file=None]
            :param STR cv:
                *OPTIONAL*cv name.
            :param BOOLEAN reconnect:
                *OPTIONAL* reconnect is set to False.
            :param STR cv_file:
                *OPTIONAL* cv file name.default is set to None.

        ROBOT USAGE:
            ${cv} =      GET CV

        :return:cv else raise an exception
        '''
        if not self.c_dict:
            self.__make_c_dict()

        if reconnect:
            cv_file = self.cv_file if cv_file is None else cv_file
            self.cv_flat = config_utils.read_yaml(file=cv_file)
        if cv is None:
            return self.cv_flat
        else:
            return self.cv_flat[cv]

    def add_cv(self, key, value, reconnect=False, cv_file=None):
        '''
        add user cv to config engine object's cv database
        
        ARGUMENTS:
            [key, value, reconnect=False, cv_file=None]
            :param STR key:
                *MANDATORY*key value
            :param STR value:
                *MANDATORY*value for key
            :param BOOLEAN reconnect:
                *OPTIONAL* reconnect to device.Default is set to False.
            :param STR cv_file:
                *OPTIONAL*cv file name.Default is set to None.

        ROBOT USAGE:
            Add CV        key=rsvp_session_handle_${role}_${num}    value=${rsvp_session_handle}

        :return:None
        '''
        if not self.c_dict:
            self.__make_c_dict()

        if reconnect:
            cv_file = self.cv_file if cv_file is None else cv_file
            self.cv_flat = config_utils.read_yaml(file=cv_file)

        self.cv_flat[key] = value


    def _make_ifd_cvar(self):

        '''
        add more useful c_dict from params
        '''

        for dev in self.c_dict:
            if self.c_dict[dev].get('interfaces'):
                for intf_tag in  self.c_dict[dev]['interfaces']:
                    intf_data = self.c_dict[dev]['interfaces'][intf_tag]
                    # add ifd slot c_dict
                    ifd = re.match(r'\w+-(\d+)/(\d+)/(\d+)(.*)', intf_data['pic'])
                    if ifd:
                        intf_data['fpcslot'] = ifd.group(1)
                        intf_data['picslot'] = ifd.group(2)
                        intf_data['portslot'] = ifd.group(3)
                        intf_data['slot'] = '/'.join([ifd.group(1), ifd.group(2), ifd.group(3)])
                        if ifd.group(4):
                            # from et-1/2/3:0.1:  get port channel '0'
                            intf_data['portchannel'] = re.sub(r'\.\d+$', '',
                                                              ifd.group(4).strip(':'))

        for dev in self.c_dict:
            dev_name = self.__get_cvar(cv_name='__'.join([dev, 'name']))
            if self.c_dict[dev].get('interfaces'):
                for intf_tag in  self.c_dict[dev]['interfaces']:
                    intf_name = self.__get_cvar(cv_name='__'.join([dev, intf_tag, 'pic']))
                    intf_data = self.c_dict[dev]['interfaces'][intf_tag]
                    # add remote ifd c_dict
                    link = intf_data['link']
                    find_remote = False
                    rdev = rintf_tag = None
                    for rdev in self.c_dict:
                        if self.c_dict[rdev].get('interfaces'):
                            for rintf_tag in  self.c_dict[rdev]['interfaces']:
                                if rdev == dev:  # local device
                                    if rintf_tag == intf_tag:   # exclude itself
                                        continue
                                if self.c_dict[rdev]['interfaces'][rintf_tag]['link'] == link:
                                    find_remote = True
                                    break   #assuming no multi-access ethernet connections for now
                            else:
                                continue
                            break  # no remote enf found for this interface, skip

                    if find_remote:
                        # use deepcopy for now.
                        # use reference instead can have the benefit of dynamic updates
                        # when the other side changes, but can get messy ( recursive mapping etc)
                        #intf_data['remote'] = self.c_dict[rdev]['interfaces'][rintf_tag]
                        intf_data['remote'] = \
                            copy.deepcopy(self.c_dict[rdev]['interfaces'][rintf_tag])
                        if intf_data['remote'].get('remote'):
                            del intf_data['remote']['remote']
                        intf_data['remote']['device_tag'] = rdev
                        intf_data['remote']['ifd_tag'] = rintf_tag

                    # build ifd description:
                    rdev_name = self.__get_cvar(cv_name=rdev + '__primary__name')
                    if find_remote  and (rdev_name is not None):
                        intf_data['remote']['device_name'] = rdev_name
                        rintf_name = self._get_ifd_from_tag(rdev, rintf_tag)
                        desc = 'link from {} {} to {}: {} ({}: {})'.\
                               format(dev_name, intf_name, rdev_name, rintf_name, rdev, rintf_tag)
                        config_utils.nested_set(self.c_dict,
                                                [dev, 'interfaces', intf_tag, 'desc'], desc)
                        self.cv_flat['__'.join([dev, intf_tag, 'desc'])] = desc
                    else:
                        desc = 'stand alone link: {} {}'.format(dev_name, intf_name)
                        self.cv_flat['__'.join([dev, intf_tag, 'desc'])] = desc

                    # add to cv_flat:( data that is not available in tv)
                    for intf_key in intf_data.keys():
                        if isinstance(intf_data[intf_key], dict):
                            for subkey in intf_data[intf_key].keys():
                                if tv.get('__'.join([dev, intf_tag, intf_key, subkey])) is None:
                                    self.cv_flat['__'.join([dev, intf_tag, intf_key, subkey])] \
                                    = intf_data[intf_key][subkey]

                        else:
                            if tv.get('__'.join([dev, intf_tag, intf_key])) is None:
                                self.cv_flat['__'.join([dev, intf_tag, intf_key])] = \
                                    intf_data[intf_key]


        # lab assigned loop-ip processing? TBD


    def _make_ifl_cvar(self, dev_tag=None, ifd_tag=None, cmd_list=None):

        '''
        add more useful c_dict from interface set cmd built in config engine
        - ip/v6 addresses
        - lo0 address: todo
        - AE/AS and coc/ls links: todo
        '''
        regex_set_intf = r'set\s+interfaces\s+([\S]+).*\s+unit\s+'
        regex_set_intf += r'(\d+).*\s+family\s+(\w+).*\s+address '
        regex_set_intf += r'({})\s*(.+)?$'.format(REGEX_IPBLOCK)
        # TBD: add units without IP? only L2 vland-id etc ?

        # params-find by defaul add a 'unit: 0' in the topy yaml,
        # need to handle this correctly in config engine
        # tempaerary add 'unit', need to sync with tt.

        units_cv = {}
        for cmd in cmd_list:
            match = re.match(regex_set_intf, cmd)
            if match is None:
                continue
            #pic = match.group(1)   # will need it if ifd_tag is not specified
            unit = match.group(2)
            #family = match.group(3)
            ip = match.group(4)


            valid_ip = config_utils.is_ip(ip)
            if not valid_ip:
                t.log(level='warn', message='invaild IP in interface config:\n' + cmd)
                raise Exception('invaild IP in interface config, check your config yaml file')
                #continue
            if re.match(r'IPv4', valid_ip):
                config_utils.nested_set(units_cv, [str(unit), 'ip'], ip, append=True)
                config_utils.nested_set(units_cv, [str(unit), 'ip_addr'], \
                        match.group(5), append=True)
                config_utils.nested_set(units_cv, [str(unit), 'ip_netlen'], \
                        match.group(6), append=True)
                config_utils.nested_set(units_cv, [str(unit), 'ip_options'], \
                        match.group(9), append=True)

            elif re.match(r'IPv6', valid_ip):
                config_utils.nested_set(units_cv, [str(unit), 'ipv6'], ip, append=True)
                config_utils.nested_set(units_cv, [str(unit), 'ipv6_addr'], \
                        match.group(7), append=True)
                config_utils.nested_set(units_cv, [str(unit), 'ipv6_netlen'], \
                        match.group(8), append=True)
                config_utils.nested_set(units_cv, [str(unit), 'ipv6_options'], \
                        match.group(9), append=True)
        if units_cv:
            config_utils.nested_update(self.c_dict[dev_tag]['interfaces'][ifd_tag],
                                       {'unit': units_cv})

            # add to cv_flat:( data that is not available in tv)
            for unitkey in units_cv:
                for subkey in units_cv[unitkey]:
                    self.cv_flat['__'.join([dev_tag, ifd_tag, 'unit', unitkey, subkey])] \
                    = units_cv[unitkey][subkey]

        if units_cv.get('0'):
            # 'unit 0' is the default ip address of the ifd,
            # make them outside units for easy access.
            self.c_dict[dev_tag]['interfaces'][ifd_tag].update(units_cv['0'])

            # add to cv_flat:( data that is not available in tv)
            for subkey in units_cv['0']:
                self.cv_flat['__'.join([dev_tag, ifd_tag, subkey])] = units_cv['0'][subkey]

        # add to cv_flat:  ToDo

        # add to remote end :
        try:
            rdev_tag = self.c_dict[dev_tag]['interfaces'][ifd_tag]['remote']['device_tag']
            rifd_tag = self.c_dict[dev_tag]['interfaces'][ifd_tag]['remote']['ifd_tag']
            if units_cv:
                self.c_dict[rdev_tag]['interfaces'][rifd_tag]['remote']['unit'] = units_cv
                for unitkey in units_cv:
                    for subkey in units_cv[unitkey]:
                        self.cv_flat['__'.join( \
                            [rdev_tag, rifd_tag, 'remote', 'unit', unitkey, subkey])] \
                            = units_cv[unitkey][subkey]
            if units_cv.get('0'):
                # 'unit 0' is the default ip address of the ifd,
                # make them outside units for easy access.
                self.c_dict[rdev_tag]['interfaces'][rifd_tag]['remote'].update(units_cv['0'])

                # add to cv_flat:( data that is not available in tv)
                for subkey in units_cv['0']:
                    self.cv_flat['__'.join([rdev_tag, rifd_tag, 'remote', subkey])] \
                        = units_cv['0'][subkey]


        except KeyError as err:
            t.log(level='debug', message='no remote end of link {} on {}: {}'.\
                  format(ifd_tag, dev_tag, err))


