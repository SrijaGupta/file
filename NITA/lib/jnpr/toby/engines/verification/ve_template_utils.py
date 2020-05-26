#!usr/local/bin/python3
"""
 Copyright (C) 2015-2016, Juniper Networks, Inc.
 All rights reserved.

 Description: Util functions for VE Generic Template tool.
"""

import builtins
import re
import os
import sys
#import getopt
import getpass
import copy
#import pprint
from collections import OrderedDict
import yaml
#import ruamel.yaml as yaml
from lxml import etree
#from jnpr.toby.engines.verification.verifyEngine import verifyEngine as VE
import jnpr.toby.engines.config.config_utils as config_utils
#import config_utils as config_utils
import gitlab
#import pexpect
#import socket
import logging
from jnpr.toby.hldcl.device import Device
from jnpr.toby.init.init import init
#import get_dut_cmd_results as dut_connect

#logger = logging.getLogger('debug')
logger = logging.getLogger(__name__)

class Tobj(object):
    '''Global t object creation.'''
    def __init__(self):
        builtins.t = self
        t.is_robot = False
        #t._script_name = __file__
        t._script_name = ""
    def log(self, level=None, message=None):
        '''pass'''
        pass

class GetDevHandle(object):
    '''Provides device handle and also executes cli and config commands.'''

    def __init__(self, topo_file=None, dev=None):
        self.topo_file = topo_file
        self.dev = dev
        Tobj()
        if self.dev:
            if topo_file:
                init_obj = init()
                init_obj.Initialize(init_file=self.topo_file)
                self.dh = t.get_handle(resource=self.dev)
            else:
                self.dh = Device(host=dev, os='Junos', timeout=60)

    def set_get_cmd_results(self, show_cmds, config_cmds):
        """
          Parameters:
             show_cmds - Dictionary of keys containing show commands
          Return:
             return updated show_cmds dictionary containing output of each show command
        """
        if float(self.dh.get_version(major=True)) >= 16.1:
            if config_cmds:
                self.dh.config(command_list=config_cmds)
                self.dh.commit()
            cmd_results = ""
            for cmd in show_cmds:
                ###--- carriage_return: Carriage return for show commands with '?'. Default is True
                carriage_return = True
                if re.search(r' \?', cmd):
                    carriage_return = False
                resp = self.dh.cli(command=cmd, channel='text', carriage_return=carriage_return).response()

                ###--- Send ctrl+u to clear buffer if last command executed with carriage_return=False
                if not carriage_return:
                    ctrl_sig = self.dh.cli(command=chr(21), channel='text', carriage_return=carriage_return).response()

                cmd_results += "user@device>" + cmd + "\n" + self._get_reqd_resp(cmd, resp) +\
                               "\n" + "user@device>" + "\n"
            if config_cmds:
                config_cmds = [re.sub(r'^set', 'delete', x.strip()) for x in config_cmds]
                self.dh.config(command_list=config_cmds)
                self.dh.commit()
            return cmd_results
        else:
            msg = "\n  DUT provided is not running JUNOS 16.1 or above version!\n"\
                  "  Please provide DUT running JUNOS 16.1 or above.\n"
            raise Exception(msg)

    def _get_reqd_resp(self, cmd, resp):
        cmd = re.sub(r'\s+', ' ', cmd.strip())
        cmd = ' '.join(cmd.split()[:-1])
        #pattern = r'(.+)' + re.escape(cmd)
        pattern = r'(Possible completions:.+)' + re.escape(cmd)
        match = re.search(pattern, resp, re.S)
        if match:
            return match.group(1)
        else:
            return resp


def file_to_string(file):
    """
       Reads a file and returns the data in string format.
    """
    try:
        file_handle = open(file, 'r')
    except IOError as err:
        if file.endswith('template.yaml'):
            # create one if not exists
            ##logger.info('template file {} does not exist, create one'.format(file))
            string = 'VERIFY_TEMPLATE: '
        else:
            raise Exception(
                'Cannot open file: {} with error: {}'.format(file, str(err)))
    else:
        with file_handle:
            string = file_handle.read()

    return string


def read_xml_file(xml_file):
    """
       Reads an xml file and returns the xmlobject(xml data).
    """
    # open xml output file, and turn it into an lxml object ( check XML syntax at the same time)
    # handle xml namespace
    xmlstr = xml_file
    if not re.search(r'\<rpc-reply', xml_file):
        xmlstr = file_to_string(xml_file)

    # rename xmlns to avoid lxml handling of xmlns.
    xmlstr = xmlstr.replace('xmlns="', 'xmlnamespace="')
    #logger.info("mmohan xmlstr: " + str(xmlstr))
    # parse xml string
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        xmlobj = etree.fromstring(xmlstr, parser=parser)
    except:
        raise Exception(
            'failed to parse content in xml file {}'.format(xml_file))

    return xmlobj


def write_template_file(temp_data, temp_file=None):
    '''
        write OrderedDict back to yaml file, keep original order
        and keep space between each template ( use ruamel would be better )
    '''
    # set YAML to handle OderedDict
    def represent_order(dump, data):
        '''
           Util function to get yaml dictionary in ordered fashion.
        '''

        return dump.represent_mapping(u'tag:yaml.org,2002:map', data.items(), flow_style=False)
    yaml.add_representer(OrderedDict, represent_order)

    if temp_file:
        os.makedirs(os.path.dirname(temp_file), exist_ok=True)
        with open(temp_file, 'w') as file_handle:
            file_handle.write('VERIFY_TEMPLATE:\n')
            for name, temp in temp_data.items():
                file_handle.write('\n  ' + yaml.dump({name: temp},
                                                     default_flow_style=False, indent=4))
    else:
        yaml_str = yaml.dump(temp_data, default_flow_style=False, indent=4)
        #logger.info(yaml_str)
        logger.info('\t' + yaml_str.replace('\n', '\n\t'))
        #logger.info(yaml.dump(temp_data, default_flow_style=None, indent=4))
        return yaml_str


def get_existing_templates(template_file):
    """
       Check if the template file(with different combinations of the keywords
       in the template file name) already exists and returns them.
    """
    tdata = OrderedDict()
    template_files = []
    try:
        #template_dir = os.path.dirname(template_file)
        template_dir = template_file
        #template_files = [f for f in os.listdir(
        #    template_dir) if os.path.isfile(os.path.join(template_dir, f))]
        template_files = [f for f in os.listdir(
            template_dir) if f.endswith('.yaml') and os.path.isfile(os.path.join(template_dir, f))]
    except Exception:
        logger.debug('Templete module directory {} itself is not exists and to be created...'.format(
            template_dir))
        # input()
    for each_yaml_file in template_files:
        try:
            yamlstr = file_to_string(
                os.path.join(template_dir, each_yaml_file))
            yaml_data = config_utils.read_yaml(string=yamlstr, ordered=True)
            tdata.update(yaml_data['VERIFY_TEMPLATE'])
        except Exception:
            logger.info('Cannot open template file {}...please check the file content...'.format(
                each_yaml_file))
            # input()

    #logger.info("Existing Templates: " + str(tdata))
    return tdata


def get_template_name_from_show_cmd(show_cmd):
    """
       Returns the VE common template name format from the
       input show command.
    """
    temp_name = 'j_check_' + '_'.join(show_cmd.split()[1:])
    return temp_name


def get_template_directory_name_from_show_cmd(template_path, show_cmd):
    """
       Returns the template directory name from the
       template path and show command provided.
    """
    template_dir = template_path + '/' + show_cmd.split()[1] + '/'
    return template_dir


def find_parameter_xpath(old_xpath, new_xpath):
    """
       TODO: Add documentation
    """
    #logger.info('\n\n====look for xpath match: ', old_xpath, new_xpath)
    oldpathlist = old_xpath.lstrip('/').split('/')
    newpathlist = new_xpath.lstrip('/').split('/')

    oldlen = len(oldpathlist)
    newlen = len(newpathlist)
    oldsublist = oldpathlist
    newsublist = newpathlist
    #logger.info('+++sublist,', oldsublist, newsublist)
    newroot = []
    moreroot = []
    found = dict()
    if newlen > oldlen:
        newsublist = newpathlist[-oldlen:]
        newroot = newpathlist[:(newlen-oldlen+1)]
        found['longer'] = 'new'
        #logger.info('newsub: ', newsublist, moreroot)
    elif newlen < oldlen:
        oldsublist = oldpathlist[-newlen:]
        moreroot = oldpathlist[:(oldlen-newlen+1)]
        newroot = [newpathlist[0]]
        found['longer'] = 'old'
        #logger.info('oldsub: ', oldsublist, moreroot)

    if oldsublist == newsublist:
        #logger.info('++++ find matching sub path.', old_xpath, new_xpath, oldsublist)
        # both add new root xpath
        found['xpath'] = '/'.join(newsublist[1:])
        if newroot:
            found['newroot'] = '/' + '/'.join(newroot)
        if moreroot:
            found['moreroot'] = '/' + '/'.join(moreroot)
            #logger.info('add root:', moreroot)
        else:
            #logger.info('no new root: identical')
            pass
        #logger.info('\n=====FOUND! ',  found)
        # input()
    else:
        return False
        #logger.info('**** Do not find matching sub path.', oldsublist,  newsublist)

    return found


def add_a_parameter(template, new_xpath):
    '''
    update a template's parameters with a leaf xpath
    '''

    rootxpath = template['xpath']
    param_map = OrderedDict([(template['parameters'][param]['xpath'], param)
                             for param in template['parameters'].keys()])

    if isinstance(rootxpath, str):
        rootxpath = [rootxpath]

    for rxpath in rootxpath:
        aparam_xpath_map = OrderedDict(
            [('/'.join([rxpath, xpath]), param_map[xpath]) for xpath in param_map])

        if new_xpath in aparam_xpath_map:
            # we got lucky, it's already there
            # param_name = aparam_xpath_map[new_xpath]
            #logger.info('\n++++ {} already defined in parameter {}\n'.format(new_xpath, param_name))
            break
        else:
            # looking for a xpath that may be a subset of the other xpath
            found = None
            for old_xpath in aparam_xpath_map:
                found = find_parameter_xpath(old_xpath, new_xpath)
                if found:
                    #logger.info('find partially matched xpath:', found)
                    if found.get('newroot') and (found['newroot'] not in template['xpath']):
                        if isinstance(template['xpath'], str):
                            template['xpath'] = [template['xpath']]
                        # todo: reorder the root xpath to make the 'inner, shortest' frist
                        template['xpath'].append(found['newroot'])
                    if found.get('longer') and (found['longer'] == 'old'):
                        # the new xpath is shorter than the old one.
                        pname = aparam_xpath_map[old_xpath]
                        template['parameters'][pname] = OrderedDict(
                            [('xpath', found['xpath'])])
                        # add the new xpath root
                        if isinstance(template['xpath'], str):
                            template['xpath'] = [template['xpath']]
                        # todo: reorder the root xpath to make the 'inner, shortest' frist
                        if found['moreroot'] not in template['xpath']:
                            template['xpath'].append(found['moreroot'])

                    break
            if found:
                break
    else:
        #logger.info('\n*** adding new xpath {} to existing parameters.'.format(new_xpath))
        # root path
        new_xpath_list = new_xpath.lstrip('/').split('/')
        #logger.info('new list:', new_xpath_list)
        new_root = '/' + new_xpath_list.pop(0)
        if new_root not in rootxpath:
            rootxpath.append(new_root)
            if isinstance(template['xpath'], str):
                template['xpath'] = [template['xpath']]

            # todo: reorder the root xpath to make the 'inner, shortest' frist

            # template['xpath'].append(new_root)
            template['xpath'] = rootxpath
        new_name = find_unique_parameter_name(template, new_xpath)
        new_path = '/'.join(new_xpath_list)
        template['parameters'][new_name] = OrderedDict([('xpath', new_path)])


def find_unique_parameter_name(template=None, new_xpath=None):
    '''
    update a template's parameters with a leaf xpath
    '''
    leaf = None
    for node in reversed(new_xpath.split('/')):
        if leaf is None:
            leaf = node
        else:
            leaf = '/'.join((node, leaf))

        if leaf in template['parameters']:
            # need to add parent
            ##logger.info('leaf name {} already taken, add parent to the name'.format(leaf))
            continue
        else:
            #logger.info('** find unique leaf name {} with xpath {}'.format(leaf, new_xpath))
            return leaf
    else:
        logger.info('weird, the whole xpath {} has been taken as a leaf name'.format(new_xpath))
        input()


def find_equivalent_template(temp_name, templates):
    '''
        find out if there is a template name that has the same components, but
        in different order
    '''
    found = None
    temp_name_set = set(temp_name.split('_'))
    for existing_temp_name in templates:
        if temp_name_set == set(existing_temp_name.split('_')):
            found = existing_temp_name
            logger.info('\n\n**** Found an equivalent template with difference component order')
            logger.info('==== {} ====='.format(found))
            break
    # else:
        #logger.info('Cannot find {} in existing template file'.format(temp_name))

    return found


def update_template(xml_file, show_cmd, template_directory=None):
    '''
    generate or update a template in a given template file
    - template name is derived from the show cmd.
    - new entries are from the xml output file of the show command
    '''
    try:
        xmlobj = read_xml_file(xml_file)
        #input('find xml:' + xml_file)
    except Exception:
        logger.info("=== ERROR: Invalid xml file used: {}\n".format(xml_file))
        sys.exit()
    if xmlobj.tag != 'rpc-reply':
        raise Exception(
            'NO_RPC_REPLY:the xml output {} does not have '\
            'root as rpc-reply, it has: {}'.format(xml_file, xmlobj.tag))

    if len(xmlobj) > 2:
        # per Stacy, there can be only one under rpc-reply
        raise Exception(
            'MANY_TOPS:the xml output {} has more than one '\
            'top knobs, excluding "cli"'.format(xml_file))

    # remove the rpc-reply root
    # get the subtree under <rpc-reply>, but not the <cli> part ( [1])
    xmltop = xmlobj[0]
    rootpath = '/' + xmltop.tag
    tree = etree.ElementTree(xmltop)
    leaf_xpath_list = []

    if re.match(r'(cli|output)$|\{.+?\}(warning|eror).*$', xmltop.tag):
        #raise Exception(' only cli knob is available. ')
        #logger.info("=== cli/warning/error skipped: {}".format(xml_file));
        # return
        rootpath = ''
    #########
    # find all unique leaf node path in the xml output
    #########
    elif len(xmltop) > 0:
        for ele in tree.iter('*'):
            if len(ele) == 0:
                # an absolute xpath for a leaf node
                xpath = tree.getpath(ele)

                # remove duplicated knobs( in xml tables)
                xpath = re.sub(r'\[\d+\]', '', xpath)
                if xpath not in leaf_xpath_list:
                    leaf_xpath_list.append(xpath)
        #logger.info('xpath:', leaf_xpath_list)

    ##########
    # read in template YAML file
    # from the show_cmd,get corresponding check_xx template name
    ##########
    if template_directory is None:
        template_directory = get_template_directory_name_from_show_cmd(
            os.getcwd(), show_cmd)

    base_temp = get_existing_templates(template_directory)
    #base_temp = origin_temp['VERIFY_TEMPLATE']
    temp_name = get_template_name_from_show_cmd(show_cmd)
    template_action = 'create'

    if temp_name not in base_temp:
        found = find_equivalent_template(temp_name, base_temp)
        #logger.info('found:', found); input()
        if found:
            temp_name = found
            template_action = 'update'
            input('find duplate {}'.format(temp_name))
        else:
            #logger.info('template {} does not exist, create one'.format(temp_name))
            base_temp[temp_name] = OrderedDict([
                ('cmd', show_cmd),
                ('xpath', rootpath),
                ('parameters', OrderedDict())

            ])
    else:
        template_action = 'update'

    this_temp = base_temp[temp_name]
    #logger.info('*** existing template {}:\n'.format(temp_name)); input()
    # write_template_file(this_temp)

    ##logger.info('=== Adding parameters to template {}  =='.format(temp_name))
    for leaf_xpath in leaf_xpath_list:
        add_a_parameter(base_temp[temp_name], leaf_xpath)

    if len(this_temp['xpath']) == 1:
        this_temp['xpath'] = this_temp['xpath'][0]

    ##logger.info('\n=====\n new template file: test_temp.yaml\n')
    ##write_template_file({temp_name: this_temp})
    template = {temp_name: base_temp[temp_name]}
    write_template_file(template, template_directory+'/'+temp_name+'.yaml')

    # send update email to the community and gate keepers
    user = getpass.getuser()
    subject = 'VE template "{}" has been updated by {}'.format(temp_name, user)
    message = '*** This email is sent automatcally by update_template.py, on behalf of the user ***\n\n'
    message += subject + ' in ' + template_directory + \
        '\n the show cmd is :\n "' + show_cmd + '"\n'
    message += '\n\n==== Updated template has the following parameters:\n'
    message += '\n' + write_template_file({temp_name: this_temp})
    message += '\n==== For your reference, the xml output of the show cmd is:\n'
    message += etree.tostring(xmlobj, pretty_print=True, encoding='unicode')
    #sendfrom = user + '@juniper.net'
    #sendto = sendfrom + ', rrussman@juniper.net, atjain@juniper.net'
    #sendto = sendfrom
    template_file_data = {'VERIFY_TEMPLATE': template}
    return temp_name, template_directory, template_action, template_file_data
    #config_utils.send_email(sendfrom, sendto, subject, message)


def strip_cmd_values(cmd):
    """
       TODO: Add documentation
    """
    cmd = re.sub(r'\s<.*?>', '', cmd)
    return cmd


def get_list_of_show_cmds(cmd):
    """
       TODO: Add documentation
    """
    cmd_keys = cmd.split()
    all_cmd_list = []
    cmd_list = ['show']
    logger.debug('comd keys' + str(cmd_keys))
    logger.debug('keys' + str(cmd_keys[1:-1]))
    for each_key in cmd_keys[1:-1]:
        cmd_list.append(each_key)
        cmd_list.append('?')
        all_cmd_list.append(' '.join(copy.deepcopy(cmd_list)))
        cmd_list.pop()
    logger.debug('all command list' +  str(all_cmd_list))
    # logger.info(all_cmd_list)
    return all_cmd_list


def get_bulk_input():
    """
       TODO: Add documentation
    """
    logger.info("\n\tPress Ctrl-D to complete it.\n")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    logger.debug('\n'.join(contents))
    return contents


def escape_values_in_cmd(cmd, cmd_output_list):
    """
       TODO: Add documentation
    """
    cmd_keys = cmd.split()
    cmd_list = []
    cmd_list.extend(cmd_keys[:2])
    cmd_output_list_index = 0
    for each_key in cmd_keys[2:]:
        #logger.info('each key : ' + each_key)
        _is_value = True
        for each_output_line in cmd_output_list[cmd_output_list_index]:
            match_expr = r'\s*' + each_key + r'\s+.*'
            #logger.info('match expr : ' + match_expr)
            match = re.match(match_expr, each_output_line)
            if match is not None:
                _is_value = False
                break
        if _is_value is True:
            cmd_list.append('<' + each_key + '>')
        else:
            cmd_list.append(each_key)
        cmd_output_list_index += 1
    # cmd_list.append(cmd_keys[-1])
    cmd_after_escape = ' '.join(cmd_list)
    logger.info('\n\tThe command after putting values within angle brackets <> \n')
    logger.info('\t' + cmd_after_escape + '\n')
    return cmd_after_escape


def split_cmd_outputs(output, cmd_list):
    """
       TODO: Add documentation
    """
    cmd_output_list = []
    output = '\n'.join(output)
    for cmd_index in range(0, len(cmd_list)):
        cmd = cmd_list[cmd_index]
        # expr = re.escape(cmd) + r'(.*?)' + '(' + re.escape(cmd.strip('? ')) +')'
        expr = re.escape(cmd) + r'(.*?)' + r'(' + r'\w+\@.*?(>|#)' + r')'
        # logger.info(expr)
        # logger.info(output)
        match = re.search(expr, output, re.DOTALL)
        if match is None:
            message = color_formatter(
                message='\n\n\t*** ERROR: Given input does not contain output of command '\
                '" {} "\n'.format(cmd), color="RED")
            logger.info(message)
            sys.exit()

        cmd_output_list.append(match.group(1).split('\n'))
        #logger.info('\n\tcommand and outputs')
        # logger.info(cmd)
        # logger.info(match.group(1))
        #logger.info('\n\toutput list:')
        # logger.info(cmd_output_list)
    return cmd_output_list

def get_show_cmd_input(show_cmd, action='search'):
    '''Get show command input interactively.'''
    if show_cmd is None:
        if action == 'search':
            show_cmd = input(
                "\n\tEnter the show command to be searched: ").strip()
        else:
            show_cmd = input(
                "\n\tEnter the show command to be updated: ").strip()
    return show_cmd

def get_show_cmd_interactively(show_cmd, auto_esc_values=False, force_get_output=False, action='search',
                               topo_yaml=None, device=None):
    """
       TODO: Add documentation
    """
    logger.debug("force_get_output:" + str(force_get_output))

    ## 'show_cmd_xml_output' contains the cmd xml results as a string
    show_cmd_xml_output = None

    contain_angle_brackets = re.search(r'\s\<.*\>', show_cmd)

    if (action == "update" and device is None) or (not auto_esc_values and action == 'search'):
        _is_cmd_not_contains_variable = input(
            "\n\tPlease Confirm all the Values (if any) are enclosed in angle brackets ? [y/n] (n) ").strip().lower()
        if _is_cmd_not_contains_variable in ('n', ''):
            message = color_formatter(
                message="\n\tERROR: Please make sure all the values are enclosed within angle brackets!"\
                "\n\tExample:\n\t\tshow interfaces <ge-0/0/0> detail\n", color="RED")
            logger.info(message)
            sys.exit()
    elif auto_esc_values or (action == "update" and device is not None):
        list_of_cmds = get_list_of_show_cmds(show_cmd)
        if list_of_cmds:
            if device is None:
                ver_16_1 = True if input("\n\tAre you using JUNOS version 16.1 or above? [y/n] (y) ").lower() in ('y', '')\
                                else None
                if not ver_16_1:
                    #logger.info(
                    #  "\n\tPlease enclose values in angle brackats <> and re-try\n\n\t\tEx: show fpc <0> pic <1>\n")
                    #sys.exit()
                    logger.info("\n\tPlease set and commit below command on the similar device running Junos 16.1 or above...")
                    logger.info("\n\t\tset system no-auto-expansion\n\t\tcommit")
                if ver_16_1:
                    logger.info("\n\tPlease set and commit below command on your Device...")
                    logger.info("\n\t\tset system no-auto-expansion\n\t\tcommit")
                logger.info('\n\tGet the outputs of below commands and paste it...')
                sys_cmd = 'show configuration system | match no-auto-expansion'
                logger.info('\n\t\t' + sys_cmd)
                for each_cmd in list_of_cmds:
                    logger.info('\t\t'+ each_cmd)
                all_cmds_output = get_bulk_input()
            else:
                ## Connect to device and fetch show command results
                try:
                    nae_config = \
                      input("\n\tNeed to configure 'set system no-auto-expansion' on device '{}'".format(device) +\
                      "\n\tHave you already configured no-auto-expansion on '{}'? [y/n] (n) ".format(device)).strip().lower()

                    logger.info('\nConnecting to device and executing commands...\n')
                    dev_obj = GetDevHandle(topo_file=topo_yaml, dev=device)
                    set_cmds = []
                    if nae_config in ('n', ''):
                        set_cmds = ['set system no-auto-expansion']
                    final_list_of_cmds = ['show configuration system | display inheritance | match no-auto-expansion']
                    final_list_of_cmds.extend(list_of_cmds)
                    all_cmds_output = dev_obj.set_get_cmd_results(show_cmds=final_list_of_cmds, config_cmds=set_cmds)
                    logger.info("\n" + "="*20 + " Show Command Results " + "="*20)
                    logger.info(all_cmds_output)
                    logger.info("="*62 + "\n")
                    all_cmds_output = all_cmds_output.split('\n')

                    ## Execute Given show command and get XML results as a string
                    logger.info("Executing show command to get results in XML format...\n")
                    show_cmd_xml_output = dev_obj.dh.cli(command=show_cmd, format='xml').response()

                except Exception as err:
                    message = color_formatter(message="\nERROR: "+ str(err) + "\n", color="RED")
                    logger.info(message)
                    sys.exit()

            expr = r'^\s*no-auto-expansion;\s*$'
            if not re.search(expr, '\n'.join(all_cmds_output), re.M):
                #logger.info(
                #    '\n\n\t*** ERROR: Given input does not contain output of command " {} "\n'.format(sys_cmd))
                message = color_formatter(
                    message="\n\n\t*** ERROR: 'set system no-auto-expansion' is missing. "\
                    "Please re-try after configuring it", color="RED")
                logger.info(message)
                message = color_formatter(
                    message="\t*** Please note that above command requires Junos version 16.1 or above\n", color="YELLOW")
                logger.info(message)
                sys.exit()

            cmd_output_list = split_cmd_outputs(all_cmds_output, list_of_cmds)
            show_cmd = escape_values_in_cmd(show_cmd, cmd_output_list)
        else:
            ## Connect to device and fetch show command XML response as a string
            try:
                logger.info('\nConnecting to device and executing given show command...\n')
                dev_obj = GetDevHandle(topo_file=topo_yaml, dev=device)
                show_cmd_xml_output = dev_obj.dh.cli(command=show_cmd, format='xml').response()
            except Exception as err:
                message = color_formatter(message="\nERROR: "+ str(err) + "\n", color="RED")
                logger.info(message)
                sys.exit()
    return show_cmd, show_cmd_xml_output

def git_update(branch, file_path, commit_message, content, action, project_id):
    """
       Commits the changes to the branch specified in git.
    """
    try:
        git_lab = gitlab.Gitlab("https://ssd-git.juniper.net",
                                private_token='ZehmGwHL6SZt7EgxVk1Z')
        project = git_lab.projects.get(project_id)
        data = {
            'branch': branch,
            'commit_message': commit_message,
            'actions': [
                {
                    'action': action,
                    'file_path': file_path,
                    'content': content
                }
            ]
        }
        logger.debug(str(data))
        project.commits.create(data)
        return True
    except Exception as excep:
        message = color_formatter(
            message='ERROR: Git Update Failed with message ' + str(excep), color="RED")
        logger.info(message)
        return False

def verify_xml_file(xml_file, show_cmd, LOG_DIR):
    """
      Check for show command in the xml_file.
      If Found, capture only XML content, create new file and return.
    """
    try:
        show_cmd = re.sub(r'\s+', ' ', show_cmd.strip())
        with open(xml_file) as fh:
            pattern = re.escape(show_cmd) + r'\s*\|\s*display xml'
            xml_content = fh.read()
            if re.search(pattern, xml_content, re.M):
                new_xml_file = os.path.join(LOG_DIR, os.path.splitext(xml_file)[0] + '_tmp.xml')
                with open(new_xml_file, 'w') as nfh:
                    match = re.search(r'(\<rpc\-reply.*\<\/rpc\-reply\>)', xml_content, re.M|re.S)
                    if match:
                        nfh.write(match.group(1))
                        return new_xml_file
                    else:
                        raise Exception("Invalid XML output. "
                                        "Please make sure that rpc-reply is captured properly.")
            else:
                raise Exception("Given show command is missing or doesn't match in the input XML file")
    except Exception as err:
        message = color_formatter(message="\n\tERROR: " + str(err) + "\n", color="RED")
        logger.info(message)
        sys.exit()

def color_formatter(message, color):
    """
      Color code the text based on the input 'color'
      Return: Color formatted message
    """
    color = color.upper()
    if color == "RED":
        message = "\x1b[1;31;40m" + message + "\x1b[0m"
    elif color == "GREEN":
        message = "\x1b[1;32;40m" + message + "\x1b[0m"
    elif color == "YELLOW":
        message = "\x1b[1;33;40m" + message + "\x1b[0m"
    elif color == "BLUE":
        message = "\x1b[1;34;40m" + message + "\x1b[0m"
    elif color == "PINK":
        message = "\x1b[1;35;40m" + message + "\x1b[0m"
    elif color == "SKYBLUE":
        message = "\x1b[1;36;40m" + message + "\x1b[0m"

    return message
