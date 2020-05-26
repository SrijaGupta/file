#!/usr/bin/env python3
'''
    New template format support in ConfigEngine
'''
# pylint: disable=import-error,locally-disabled
import ruamel.yaml as yaml
import jnpr.toby.engines.config.config_utils as config_utils
import re
#import copy

class ConfigEngine():
    '''
        Config Engine Class
    '''

    def __init__(self):
        '''
            Initial initialization of ConfigEngine
        '''
        self.templates = {}

    def process_template_files(self, template_files):
        '''
            Process Template Files
        '''
        for template_file in template_files:
            template_file = config_utils.find_file(template_file)
            template_file_content = open(template_file).read()
            #print("******************************\nDEBUG - Orig yaml content:\n" + template_file_content)
            template_file_dict = yaml.safe_load(template_file_content)
            global_vars = None

            #process global variables
            try:
                global_vars = template_file_dict['global_vars']
            except Exception:
                pass

            if not global_vars or type(global_vars) is not dict: #pylint: disable=unidiomatic-typecheck
                global_vars = {}

            for template in template_file_dict['templates']:
                self.templates[template] = template_file_dict['templates'][template]
                for variable in global_vars:
                    if type(global_vars[variable]) is bool:
                        if global_vars[variable]:
                            global_vars[variable] = 'TRUE'
                        else:
                            global_vars[variable] = 'FALSE'
                    if not global_vars[variable]:
                        global_vars[variable] = ''
                    self.templates[template]['config'] = re.sub(r'var\[(\')?' + variable + '(\')?\]', #pylint: disable=anomalous-backslash-in-string
                                                                '__' + str(global_vars[variable]) + '__',
                                                                self.templates[template]['config'])
    def config(self, template, args): #pylint: disable=too-many-locals
        '''
            Build Config 'set' lines
        '''
        if not template:
            raise Exception("'template' argument required for Config Engine keyword when using Config Engine V2")
#        arguments = {}
#        if args:
#            arguments = args
        local_vars = {}
        if isinstance(self.templates[template], dict) and 'vars' in self.templates[template]:
            local_vars = self.templates[template]['vars']
        local_vars.update(args)
        for variable in local_vars:
            if type(local_vars[variable]) is bool:
                if local_vars[variable]:
                    local_vars[variable] = 'TRUE'
                else:
                    local_vars[variable] = 'FALSE'
#            local_vars[variable] = re.sub(r'\s+', '__blank__', str(local_vars[variable]))
            self.templates[template]['config'] = re.sub(r'var\[(\')?' + variable + '(\')?\]', #pylint: disable=anomalous-backslash-in-string
                                                        '__' + str(local_vars[variable]) + '__',
                                                        self.templates[template]['config'])

        lines = self.templates[template]['config'].split("\n")

################ changed code ########################
        preceding_spaces = None
        new_yaml = ''
        loop_flag = 0
        prior_index = 0
        indent = None
        index = 0
        loop_op = []
        loop_lines = []
        for line in lines:
            if not re.search(r'\.\.#', line):
                line = re.sub(r'#[^{].*$', '', line) #remove comments
            if not re.search(r'\w', line):
                continue
            line = re.sub(r'[\s\t]*$', '', line) #remove trailing spaces
            if '\t' in line:
                raise Exception("Please remove tabs from template " + template)

            if 'LOOP(' in line:
               # print(prior_index)
                loop_flag = 1
                space_match = re.match(r'^(\s*)(.*)', line)
                preceding_spaces = space_match.groups()[0]
                content = space_match.groups()[1]
                #establish indentation width
                prior_index = len(preceding_spaces)
                #print("new pr", prior_index)
                line = line.replace('__', '')
                loop_op = config_utils.expand_to_list(line.strip('LOOP() '))
            elif loop_flag == 1:
                space_match = re.match(r'^(\s*)(.*)', line)
                preceding_spaces = space_match.groups()[0]
                content = space_match.groups()[1]
                if len(preceding_spaces) > prior_index:
                    line = line.replace('__', '')
                    loop_lines.append(line)
                    if line == lines[-2].replace('__', '') and len(lines[-1]) == 0:
                        for iloop in loop_op:
                            largs = {}
                            for lvar in iloop.split(','):
                                lkey, val = lvar.split(':', 1)
                                largs[lkey.strip()] = val.strip()
                            for loop_line in loop_lines:
                                for variable in largs:
                                    loop_line = re.sub(r'var\[(\')?' + variable + '(\')?\]', #pylint: disable=anomalous-backslash-in-string
                                                       str(largs[variable]), loop_line)
                                new_yaml = new_yaml + loop_line[2:] + "\n"
                else:
                    #print("loop lines>>>>>>", str(loop_lines))
                    #print("line ******", str(line))
                    if loop_lines:
                        for iloop in loop_op:
                            largs = {}
                            for lvar in iloop.split(','):
                                lkey, val = lvar.split(':', 1)
                                largs[lkey.strip()] = val.strip()
                            for loop_line in loop_lines:
                                for variable in largs:
                                    loop_line = re.sub(r'var\[(\')?' + variable + '(\')?\]', #pylint: disable=anomalous-backslash-in-string
                                                       str(largs[variable]), loop_line)
                                new_yaml = new_yaml + loop_line[2:] + "\n"
                    loop_flag = 0
                    new_yaml = new_yaml + line + "\n"
            else:
                new_yaml = new_yaml + line + "\n"
#######################################################
           # new_yaml = new_yaml + line + "\n"


        #change all remaining variables to __FALSE__
        new_yaml = re.sub(r'var\[(\')?\S+(\')?\]', '__FALSE__', new_yaml)

        #t.log_console("*********************************\nDEBUG - Final yaml content:\n" + new_yaml)

        #build 'set' lines
        lines = new_yaml.split('\n')
        new_yaml = '' #reinitialize new_yaml
        set_list = None
        cmd = None
        cmd_set = []
        indent = None
        index = 0
        prior_index = 0
        for line in lines:
            #determine indent
            space_match = re.match(r'^(\s*)(.*)', line)
            preceding_spaces = space_match.groups()[0]
            content = space_match.groups()[1]
            #building list
            if preceding_spaces == '':
                set_list = []
            #establish indentation width
            if not indent and preceding_spaces != '':
                indent = len(preceding_spaces)
            if indent:
                index = int(len(preceding_spaces)/indent)

            #preceding_spaces has not gotten shorter on this line indicating time to print prior cmd
            if (cmd and index <= prior_index) or (cmd and str(cmd).endswith('__TRUE__')):
                cmd = re.sub(r'None', '__FALSE__', cmd)
                cmd_set.append(cmd)
                del set_list[index:]
            #append new content
            set_list.append(content)
            #build cmd string to potentially be printed next iteration through lines
            cmd = ' '.join(set_list)
            #set prior_index for comparison during next iteration
            prior_index = index


        #Clean up commands
        new_cmd_set = []
        cache_cmd = ''
        cmd_set.append('')
        for cmd in cmd_set:
            cmd = re.sub("\s*$", '', cmd) #Remove trailing spaces
            cmd = re.sub(r'__.*__FALSE__.*$', '', cmd, 1) #If __FALSE__ exists after another __TRUE|FALSE__, then remove suffix
            cmd = re.sub(r'^.*__FALSE(__)?.*$', '', cmd, 1) #If the entire line starts with a __FALSE__, then remove the line completely
            if not cmd.startswith(cache_cmd):
                cache_cmd = re.sub(r'__TRUE(__)?', '', cache_cmd) #Replace __TRUE__ with empty string
                cache_cmd = re.sub(r'(__|__)', '', cache_cmd) #This line doesn't seem necessary
                cache_cmd = re.sub("\s\s+", ' ', cache_cmd) #change multiple spaces into one space
                new_cmd_set.append(cache_cmd)
            cache_cmd = cmd

        #process vars that are lists or dicts
        final_cmd_set = []
        list_vars_exist = True
        for cmd in new_cmd_set:
            dict_search_obj = re.search(r'\{\'(\w+)\':\s*\'?([^\'\}]*)?\'?\}\s*(.+)?', cmd)
            #list present
            if re.search(r'\[\'?', cmd):
                cmd_list_vars = [cmd]
                while len(cmd_list_vars):
                    cmd_list_vars, cmd_list_no_vars = self._process_list_vars(cmd_list=cmd_list_vars)
                    final_cmd_set.extend(cmd_list_no_vars)
            #dict present
            elif dict_search_obj:
                cmd = re.sub('^\w+', dict_search_obj.group(1), cmd)
                cmd = re.sub('\'', '', cmd)
                value = ''
                if dict_search_obj.group(2):
                    value = ' ' + str(dict_search_obj.group(2))
                elif dict_search_obj.group(3) is not None:
                    value = ' ' + str(dict_search_obj.group(3))
                else:
                    value = ' '
                cmd = re.sub(' {.*', value, cmd)
                final_cmd_set.append(cmd)
            else:
                final_cmd_set.append(cmd)
        return final_cmd_set

    def _process_list_vars(self, cmd_list=None):
        cmd_list_no_vars = []
        cmd_list_vars = []
        for cmd in cmd_list:
            var_list = None
            list_start = None
            list_end = None
            search_start = re.search(r'\[\'?', cmd, re.I)
            if search_start:
                list_start = search_start.start()
            search_end = re.search(r"\'?\]", cmd, re.I)
            if search_end:
                list_end = search_end.end()
            if list_start and list_end:
                cmd_list_val = (cmd[list_start:list_end])
                cmd_list_val.strip(" ")
                if cmd_list_val.find(",") != -1:
                    #t.log_console("LIST WITH MORE THAN 1 ELEMENTS ........")
                    var_list = eval((cmd[list_start:list_end]))
                elif cmd_list_val.find(" ") != -1:
                    if cmd_list_val.find("'") != -1 or cmd_list_val.find('"') != -1:
                        var_list = eval((cmd[list_start:list_end]))
                    else:
                        #t.log_console("SPACE SEPARATED STRING WITH SQUARE BRACES ........")
                        cmd_list_no_vars.append(cmd)
                else:
                    #t.log_console("LIST WITH 1 ELEMENT ........")
                    var_list = eval((cmd[list_start:list_end]))
            if var_list:
                for var in var_list:
                    new_cmd = cmd[0:list_start] + str(var) + cmd[list_end::]
                    if re.search(r'\[\'?', new_cmd):
                        cmd_list_vars.append(new_cmd)
                    else:
                        cmd_list_no_vars.append(new_cmd)
        return cmd_list_vars, cmd_list_no_vars


#test routines to be used when ConfigEngine not used as library/module....
#if __name__ == "__main__":
#    ce = ConfigEngine()
#
#    #read template files
#    template_file_name = './bgp.yaml'
#    template_file_list = [template_file_name]
#    ce.process_template_files(template_file_list)
#
#    #build config yaml
#    template_name = 'config_bgp'
#    variables = {'action': 'set',
#                 'groups': 'abc',
#                 'logical-systems': 'test',
#                 'routing-instances': 'rv',
#                 'description': 'my_BGP_description'}
#    #arguments = {}
#    print("\n******************************\nDEBUG - Calling...\nconfig(template=" + template_name + ", " + str(variables) + ")\n")
#    ce.config(template=template_name, args=variables)


#tagging code - SAVED FOR LATER
#saved code - hard to rewrite...
#            line = re.sub(r':\s*#\s*(toby_tags\[(\w+,)*?' + tag + '(,|\]).*)', r' toby_tag[' + tag + ']\1:', line)
#            line = re.sub(r'\s*#\s*(toby_tags\[(\w+,)*?' + tag + '(,|\]).*)', r' toby_tag[' + tag + ']\1', line)

