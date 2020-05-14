#!/usr/bin/env python
# coding: utf-8
# Authors: psagrera@juniper.net
# Version: 1.0 20150122
# <*******************
#
# Copyright 2016 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# *******************>


# xml specific
from lxml import etree
from lxml.builder import E
import xml.etree.ElementTree as ET
import xml.dom.minidom
import lxml

# stdlib
import StringIO
import re
import subprocess as sub
from subprocess import Popen, PIPE
from subprocess import check_call
import os
import sys
import pdb
import errno
import time
from datetime import datetime
from datetime import date, timedelta
from time import sleep
from pprint import pprint
import logging
import hashlib
from socket import error as SocketError
import errno
import signal
from itertools import *
import csv

#third-party
import xmltodict
import yaml
import paramiko
#import ncclient.transport.errors as NcErrors
#import ncclient.operations.errors as TError
import jinja2
import csv
from select import select
import ftplib
import logging.handlers

# junos-ez
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.fs import FS
from jnpr.junos.exception import *
from jnpr.junos.utils.config import Config
from jnpr.junos.utils.sw import SW
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.factory import loadyaml
from jnpr.junos import Device
from jnpr.junos import *

# Robot libraries

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.OperatingSystem import OperatingSystem
from robot.api import logger

# Global Variables
timestamp =  datetime.now().strftime("%Y-%m-%d")
timestamp2 =  datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")[:-3]
timestamp3 = datetime.now().strftime ("%H_%M_%S")
timestamp4 = datetime.now().strftime ("%Y_%m_%d_%H_%M_%S")

# Global variables for shell connection

_SHELL_PROMPT = '% '
_JUNOS_PROMPT = '> '
_BASH_PROMPT = '?'
_SELECT_WAIT = 0.1
_RECVSZ = 1024


class ContinuableError(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True

class FatalError(RuntimeError):
    ROBOT_EXIT_ON_FAILURE = True

class pybot_jrouter (object):


        ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

        ROBOT_LISTENER_API_VERSION = 2

    # -----------------------------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------------------------
        def __init__(self,**kvargs):

                # Setting credentials

                self.user = kvargs['user']
                self.target = kvargs['target']
                self.password = kvargs['password']
                self.ROBOT_LIBRARY_LISTENER = self
                self.max_retries = 2
                self._conn = Device (user=self.user, host=self.target, password=self.password,port=22,gather_facts=False)
                self.max_retries = 5

    # -----------------------------------------------------------------------
    # FUNCTIONS START HERE
    # -----------------------------------------------------------------------

        def open_connection (self):

            try:
                self._conn.open(auto_probe=10)
                self._conn.timeout = 120*120
                return self
            except ConnectError as c_error:
               print "WARN Connection problems %s" %c_error
               raise ContinuableError("Connection problems %s" %c_error)

        def close_connection (self):

            try:
                self._conn.close()
                return self
            except ConnectError as c_error:
               print "WARN Connection problems %s" %c_error
               raise ContinuableError("Connection problems %s" %c_error)

        def load_configuration_from_file (self,synchronize=True,overwrite=False,**kvargs):

            """
                Function that load configuration on router from a file

                path : where the configuration file is located

                format:  possible values 'set' or 'xml' or 'bracket'  (so far only format 'set' is supported)

            """
            #overwrite = kvargs.pop ('overwrite',False)
            args = dict (data = '')
            args.update (kvargs)
            if overwrite:
                return self.load_configuration(overwrite=True,**args)
            else:
                return self.load_configuration(overwrite=False,**args)

        def load_configuration_from_template (self,commit_comment ='__JRouter__',format='set',overwrite=False,synchronize=True,**kvargs):


            yaml_file = kvargs['template_vars']

            # Checking if this attribute was already attached to Device
            if hasattr(self._conn, "candidate"):
                pass
            else:
                self._conn.bind( candidate = Config )
            # Locking configuration
            try:
                self._conn.candidate.lock()
            except LockError as l_error:
                print "*WARN* Problems locking configuration: %s" % (l_error)
                raise FatalError("Unable to lock configuration.....exiting")
            try:
                # Loading files and rendering
                if isinstance(yaml_file, dict):
                    myvars = dict(yaml_file)
                else:
                    myvars = yaml.load(open(yaml_file).read())
                if overwrite:
                    self._conn.candidate.load(template_path=kvargs['jinja2_file'],template_vars=myvars,format=format,overwrite=True)
                else:
                    self._conn.candidate.load(template_path=kvargs['jinja2_file'],template_vars=myvars,format=format,overwrite=False)
            except ConfigLoadError as error:
                if error.rpc_error['severity'] == 'warning':
                    print error.rpc_error['severity']
                    pass
                    return True
                print "*WARN* Problems loading configuration: %s" % (error)
                raise FatalError("Unable to load configuration.....exiting")

            print '*INFO* Configuration to be commited  %s' % (self._conn.candidate.diff())

            try:
                self._conn.candidate.commit(comment=commit_comment)
                self._conn.candidate.unlock()
                return True

            except (CommitError,LockError) as err:
                print err
                raise FatalError("Unable to commit or unlock configuration......exiting")
            except Exception as error:
                if 'Opening and ending tag mismatch: routing-engine ' in error:
                    print error
                    pass
                    self._conn.candidate.unlock()
                    return True
                else:
                    print error
                    return False

        def load_configuration (self,commit_comment ='__JRouter__',path=None,overwrite=False,**kvargs):

                """
                    Function that load configuration on router

                    **kvargs format:set|text|xml
                             data: data to load in the router
                """

                data = kvargs['data']
                format = kvargs['format']


                if ((format == "set") or (format == "xml") or (format == "conf") or (format == "text") or (format == "txt")):
                    # Checking if this attribute was already attached to Device

                    # This is required if we are going to change configuration several times
                    if hasattr(self._conn, "candidate"):
                        pass
                    else:
                        self._conn.bind( candidate = Config )
                    try:
                        self._conn.candidate.lock()
                    except LockError as l_error:

                        print "*WARN* Problems locking configuration: %s" % (l_error)
                        raise FatalError("Problems locking configuration,exiting...")
                        return False
                    try:
                        if ((data == "") and (path != None)):
                            if overwrite:
                                self._conn.candidate.load(path=path,format=format,overwrite=True)  # Load configuration from file
                            else:
                                self._conn.candidate.load(path=path,format=format)
                        else:
                            if overwrite:
                                self._conn.candidate.load(data,format=format,overwrite=True)  # Load configuration from file
                            else:
                                self._conn.candidate.load(data,format=format)
                    except ConfigLoadError as error:

                        # hack to avoid return an error whenever config load get a warning
                        if error.rpc_error['severity'] == 'warning':
                            print "*INFO* Problems loading configuration: %s" % (error.rpc_error['message'])

                    except lxml.etree.XMLSyntaxError as error:
                        print "*WARN* Problems loading configuration: %s" % (error)
                        raise FatalError("Problems loading configuration,exiting...")


                    print '*INFO* Configuration to be commited  %s' % (self._conn.candidate.diff())
                    try:
                         self._conn.candidate.commit(comment=commit_comment)
                         self._conn.candidate.unlock()
                         return True
                    except (CommitError,LockError) as err:
                        #print err
                        self._conn.candidate.rollback()
                        print "*WARN* Problems commiting configuration: %s" % (err)
                        raise FatalError("Error commiting configuration, exiting....")
                else:
                    raise FatalError("Expected result is True but was False,test will go on")
                    return False

        def jsnap (self,**kvargs):


                variables = BuiltIn().get_variables()

                # Assigning kvargs

                section=None


                if 'section' in kvargs.keys():
                    section = kvargs['section']
                tag = kvargs['tag']
                snaptype = kvargs['snaptype']
                test = kvargs['test']
                mode = kvargs ['mode']
                output_directory = variables['${path}']
                test_case = variables ['${testname}']

                dirpath = output_directory + "/" + test_case.replace(" ","_") + "/" + self.target + "/snapshot/"

                #PARENT_ROOT=os.path.abspath(os.path.join(self.logdir, os.pardir))
                #GRANDPA=os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))

                if not os.path.exists (dirpath):
                     os.makedirs (dirpath,mode=0777)

                timestamp =  datetime.now().strftime("%Y-%m-%d")

                if snaptype == "snap":

                    if section:
                        cmd = 'jsnap --'+ snaptype + " " + timestamp + '_'+ tag + ' -l ' + self.user + ' -p ' + self.password + ' -t ' + self.target + ' -s' + section + ' ' + test
                    else:
                        cmd = 'jsnap --'+ snaptype + " " + timestamp + '_'+ tag + ' -l ' + self.user + ' -p ' + self.password + ' -t ' + self.target + ' ' + test
                    print "Executing: %s" %cmd
                    jsnap_command = sub.Popen (cmd,stdout=sub.PIPE,stderr=sub.PIPE, shell=True,cwd=dirpath)
                    output, errors = jsnap_command.communicate()
                    if ((("Exiting." in errors)) or("Unable to connect to device: " in errors) or ("jsnap: not found" in errors) or ("appears to be missing" in output)):
                        print output
                        print errors
                        raise FatalError("Unable to execute jsnap.....exiting")
                    else:
                        return True
                    print output,errors
                    return True

                elif snaptype == "snapcheck":

                    if section:
                        cmd = 'jsnap --'+ snaptype + " " + timestamp + '_'+ tag + ' -l ' + self.user + ' -p ' + self.password + ' -t ' + self.target + ' -s' + section + ' ' + test
                    else:
                        cmd = 'jsnap --'+ snaptype + " " + timestamp + '_'+ tag + ' -l ' + self.user + ' -p ' + self.password + ' -t ' + self.target  + ' ' + test
                    print "Executing: %s" %cmd
                    jsnap_command = sub.Popen (cmd,stdout=sub.PIPE,stderr=sub.PIPE, shell=True,cwd=dirpath)
                    output, errors = jsnap_command.communicate()

                    print output
                    print errors

                    if ((("Exiting." in errors)) or("Unable to connect to device: " in errors) or ("jsnap: not found" in errors) or ("appears to be missing" in output)):

                        print output
                        print errors
                        raise FatalError("Unable to execute jsnap.....exiting")

                    else:
                      if mode == "strict":
                        if "ERROR" in output or "ERROR" in errors:
                          raise FatalError("ERROR found in jsnap mode strict.....exiting")
                        else:
                          return True
                      else:
                        return True

                elif snaptype == "check":

                    if section:
                        cmd_check = 'jsnap --'+ snaptype + " " + timestamp + '_pre' + ',' +  timestamp + '_post' + ' -l ' + self.user + ' -p ' + self.password + ' -t ' + self.target  + ' -s' + section + ' ' + test
                    else:
                        cmd_check = 'jsnap --'+ snaptype + " " + timestamp + '_pre' + ',' +  timestamp + '_post' + ' -l ' + self.user + ' -p ' + self.password + ' -t ' + self.target  + ' '  + test
                    print "Executing: %s" %cmd_check
                    jsnap_command = sub.Popen (cmd_check,stdout=sub.PIPE,stderr=sub.PIPE, shell=True,cwd=dirpath)
                    output, errors = jsnap_command.communicate()
                    print output
                    print errors

                    if ((("Exiting." in errors)) or("Unable to connect to device: " in errors) or ("jsnap: not found" in errors) or ("appears to be missing" in output)):

                        print output
                        print errors
                        raise FatalError("Unable to execute jsnap.....exiting")

                    else:
                        if mode == "strict":
                            if "ERROR" in output or "ERROR" in errors:
                                raise FatalError("ERROR found in jsnap mode strict.....exiting")
                            else:
                                return True
                        else:

                            return True
                else:
                    raise FatalError("Invalid snap type.....exiting")

        def rescue_configuration(self,**kvargs):

            """
                Function that issues Save/Load a Rescue Configuration

            """

            if 'action' in kvargs.keys():
                action = kvargs['action']

            # Saving rescue configuration
            if action == 'save':
                try:
                    self._conn.rpc.request_save_rescue_configuration()
                except RpcError as err:
                    rpc_error = err.__repr__()
                    print rpc_error
                return self
            # Checking if this attribute was already attached to Device
            if hasattr(self._conn, "candidate"):
                pass
            else:
                self._conn.bind( candidate = Config )

            # Locking configuration
            try:
                self._conn.candidate.lock()
            except LockError as l_error:
                print "*WARN* Problems locking configuration: %s" % (l_error)
                raise FatalError("Unable to lock configuration.....exiting")

            # Loading rescue configuration
            if action == 'load':
                try:
                    self._conn.rpc.load_configuration({'rescue': 'rescue'})
                except RpcError as err:
                   rpc_error = err.__repr__()
                   print rpc_error
                except ConfigLoadError as error:
                    print "*WARN* Problems loading configuration: %s" % (error)
                    raise FatalError("Unable to load configuration.....exiting")
                print '*INFO* Configuration to be commited  %s' % (self._conn.candidate.diff())

                try:
                    self._conn.candidate.commit(comment='loading rescue configuration')
                    self._conn.candidate.unlock()
                    return True

                except (CommitError,LockError) as err:
                    print err
                    raise FatalError("Unable to commit or unlock configuration......exiting")

        def commands_executor (self,**kvargs):

            """
                Function that issues commands

            """

            # Getting built-in variables

            variables = BuiltIn().get_variables()

            regex=''
            xpath=''
            if 'xpath' in kvargs.keys():
                xpath = kvargs['xpath']

            if 'regex' in kvargs.keys():
                regex = kvargs['regex']

            command = kvargs['command']
            format = kvargs['format']
            output_directory = variables['${path}']
            root_dir = variables['${OUTPUT_DIR}']
            test_case = variables ['${testname}']

            if output_directory == None:
                dirpath = "/collector/" + timestamp + "/"
            else:
                dirpath = output_directory + "/" + test_case.replace(" ","_") + "/commands"

            # Create directory if does not exist
            if not os.path.exists (dirpath):
                os.makedirs (dirpath,mode=0777)

            if format == "text":

                if regex:

                    try:
                        cmd_to_execute = self._conn.rpc.cli (command)
                    except RpcError as err:
                        rpc_error = err.__repr__()
                        print xmltodict.parse(rpc_error)['rpc-error']['error-message']
                        raise FatalError("Error executing RPC,exiting...")

                    operations = command.split("|")[1:]
                    result_tmp = cmd_to_execute.text
                    lines=result_tmp.strip().split('\n')
                    for operation in operations:
                        if re.search("count", operation, re.IGNORECASE):
                            print '*INFO* Count: %s lines' % len(lines)
                            return len(lines)
                        match = re.search('match "?(.*)"?', operation, re.IGNORECASE)
                        if match:
                            regex = match.group(1).strip()
                            lines_filtered = []
                            for line in lines:
                                if re.search(regex, line, re.IGNORECASE):
                                    lines_filtered.append(line)
                            lines = lines_filtered
                        match = re.search('except "?(.*)"?', operation, re.IGNORECASE)
                        if match:
                            regex = match.group(1).strip()
                            lines_filtered = []
                            for line in lines:
                                if re.search(regex, line, re.IGNORECASE):
                                    pass
                                else:
                                    lines_filtered.append(line)
                            lines = lines_filtered

                    text_matches = re.search(regex,cmd_to_execute.text,re.MULTILINE)

                    if text_matches:
                        print text_matches.groups()
                        return text_matches.groups()
                else:
                    print "Executing: %s" %command

                    try:
                        cmd_to_execute = self._conn.rpc.cli (command)

                    except RpcError as err:
                        rpc_error = err.__repr__()
                        print xmltodict.parse(rpc_error)['rpc-error']['error-message']
                        raise FatalError("Error executing RPC,exiting...")

                    #print type(cmd_to_execute)
                    if (isinstance(cmd_to_execute, bool)):
                        return True
                    else:
                        cmd_clean = command.replace(" ","_").replace('_"','_').replace('"_','_').replace('"','').replace("/","_")
                        filename = timestamp2 + '_'+ self.target  + "_" + cmd_clean + "." + "txt"
                        path = os.path.join (dirpath,filename).replace(root_dir,'.')
                        print "Saving file as: %s" %path
                        print '*HTML* <a href="%s" target="_blank">%s</a>' % (path, path)
                        try:
                            with open (path,'w') as file_to_save:
                                file_to_save.write(cmd_to_execute)
                            return True
                        except IOError as err:
                            print err.errno,err.strerror
                            raise FatalError("Error opening File,exiting...")

            elif format == "xml":

                if xpath:
                    print "Executing: %s [%s]" %(command,xpath)

                    try:
                        cmd_to_execute = self._conn.rpc.cli (command,format='xml')
                        xml_result = etree.tostring( cmd_to_execute)

                    except RpcError as err:
                        rpc_error = err.__repr__()
                        print xmltodict.parse(rpc_error)['rpc-error']['error-message']
                        raise FatalError("Error executing RPC,exiting...")

                    xpath_result = cmd_to_execute.xpath(xpath)[0].text.strip()

                    if xpath_result == None:
                        raise FatalError("XPATH malformed,exiting...")
                    else:
                        print xpath_result
                        return xpath_result
                else:
                    try:
                        cmd_to_execute = self._conn.rpc.cli (command,format='xml')
                        xml_result = etree.tostring( cmd_to_execute)

                    except RpcError as err:
                        rpc_error = err.__repr__()
                        print xmltodict.parse(rpc_error)['rpc-error']['error-message']
                        raise FatalError("Error executing RPC,exiting...")
                    return xml_result
            else:
                raise FatalError("Format not valid,exiting...")


        def shell_cli_command_executor(self, **kvargs):
            # Checking if connection is alive
            self._is_connection_alive()
            command = ""
            if kvargs.has_key('command'):
                command = kvargs.get('command')
            if kvargs.has_key('shelltimeout'):
                shelltimeout = kvargs.get('shelltimeout')
            else:
                shelltimeout = 30
            if kvargs.has_key('timeout'):
                timeout = kvargs.get('timeout')
            else:
                timeout = 30
            shell = StartShell(self._conn, timeout=int(shelltimeout))
            shell.open()
            got = shell.run("cli -c '"+command+" | no-more'", timeout=int(timeout))
            shell.close()
            if not got[0]:
                print "*WARN* %s" % (str(got[1]))
#                raise FatalError("Error executing CLI command, exiting...")
            line = re.sub('(\r\n)+', '\n', got[1])
            line = re.sub('(\r)+', '\n', line)
            line = re.sub('(\n)+', '\n', line)
            return line

        def save_config_to_file (self,**kvargs):

            directory = kvargs['directory'] + '/' + timestamp4
            print "*INFO* Saving current configuration..."
            file_obj = StartShell(self._conn)
            file_obj.open()
            got = file_obj.run ("cli -c 'show configuration | save "+ directory +"_config.txt' ")
            file_obj.close()
            print "*INFO* %s" % (got)
            return got[-2].split("'")[1]

        def rollback (self,commit_comment='__JRouter__',**kvargs):

            """
                Function that performs rollback
                 rollback_num = number

            """
            rollback_num = kvargs['rollback_num']

            try:
                rollback_num = int(rollback_num)
                if rollback_num > 50:
                    raise FatalError("Sorry. 'rollback_num' must lower than 50")
            except Exception as e:
                raise FatalError("Sorry. 'rollback_num' must be an integer.")

            if hasattr(self._conn, "candidate"):
                pass
            else:
                self._conn.bind( candidate = Config )
            try:
                self._conn.candidate.lock()
            except LockError as l_error:
                print "*WARN* Problems locking configuration: %s" % (l_error)
                raise FatalError("Unable to lock configuration.....exiting")

            try:
                print "Rolling back configuration...."
                self._conn.candidate.rollback(rollback_num)
                self._conn.candidate.commit(comment=commit_comment)
                self._conn.candidate.unlock()
                return True
            except RpcError as err:
                rpc_error = err.__repr__()
                raise FatalError(xmltodict.parse(rpc_error)['rpc-error']['error-message'])

        def switchover (self):
            """
                Function to perfom RE switchover
            """
            # We need to verify that backup RE is ready before proceed
            b_slot = self.get_slot('backup')
            b_state = self._conn.rpc.get_route_engine_information(slot=b_slot)
            state = b_state.findtext ('route-engine/mastership-state')

            if (state != "backup"):
                raise FatalError("Backup RE is not ready")

            try:
                self.open_connection()
                print 'Executing switchover to complete the SW upgrade !!!'
                switchover_cmd = self._conn.cli ("request chassis routing-engine master switch no-confirm",format='xml',warning=False)
                self.close_connection()
            except ConnectError as c_error:
                raise FatalError(c_error)
            except TError.TimeoutExpiredError as Terr:
                print Terr
                pass
            except NcErrors.SessionCloseError as Serr:
                print Serr
                pass
            except SocketError as S_err:
                print S_err
                pass
            except ConnectClosedError as CC_error:
                print CC_error
                pass

            sleep (60)
            try:
                # WA for dealing with in band connections
                print "Re-opening connection......."
                self._conn.open(auto_probe=900)
                return True
            except ConnectError as c_error:
                raise FatalError (c_error)
#kk = pybot_jrouter (user='lab',password='lab123',target='172.70.63.21')
#kk.open_connection()
#kk.save_config_to_file(directory='/var/tmp')

        def _is_connection_alive(self):
            """
                Function that checks if connection is open. In case of connection is closed, it will try to reconnect
            """
            max_connection_retries = self.max_retries
            try:
                self._conn.rpc.ping(host=self.target)
            except (ConnectError,ConnectClosedError) as c_error:
                BuiltIn().log_to_console("\nConnection to %s closed unexpectedly, %s" % (self.target, c_error))
                self._conn.connected = False # When this exception is thrown self._conn.connected is set to False
                pass
            if self._conn.connected:
                pass
            else:
                # Retry mechanism
                for i in range(1, max_connection_retries+1):
                    try:
                        BuiltIn().log_to_console("\nConnection to %s closed... trying to reopen..." % (self.target))
                        self._conn.open(auto_probe=120)
                        self._conn.timeout = 240*240
                        # Allow a little extra time in case routing engine has just been rebooted
                        sleep(30)
                        BuiltIn().log_to_console("\nConnection to %s reopened" % (self.target))
                        break
                    except (ConnectError,ConnectClosedError) as c_error:
                        if i < max_connection_retries:
                            BuiltIn().log_to_console("\nConnection to %s not open %s in iteration %d,retrying in 20 seconds" % (self.target, c_error, i))
                            # Retry delay
                            sleep(20)
                            continue
                        else:
                            raise ContinuableError('ERROR:Connection lost, unable to reconnect to %s' % self.target)

        def junos_rpc(self,**kvargs):

            """
                Function that executes and RPC on JUNOS device
                robot example : Execute    Junos Rpc    ${target}    rpc=request-snapshot    format=json    kwargs='routing_engine=master'
            """

            args = kvargs
            results = {}
            if 'kwargs' in kvargs.keys():
                kwargs = args['kwargs']
            else:
                kwargs = None
            rpc = args['rpc']
            results['rpc'] = rpc
            results['kwargs'] = kwargs
            results['changed'] = False

            #logger.console ('\ncalling RPC: {0}'.format(rpc)) if self.console else None
            try:
                if kwargs is None:
                    values = {}
                elif re.search(r'\{.*\}', kwargs):
                    values = {k:v for k,v in re.findall(r'([\w-]+)\s?:\s?\'?\"?([\w\.-]+)\'?\"?',kwargs)}
                elif re.search(r'[\w-]+=[\w\.-]+\/\d\/\d.\d',kwargs):
                    values = values = {k:v for k,v in re.findall('([\w-]+)=([\w\.-]+\/\d\/\d.\d)',kwargs)}
                elif re.search(r'[\w-]+=[\w\.-]+\/\d\/\d',kwargs):
                    values = {k:v for k,v in re.findall('([\w-]+)=([\w\.-]+\/\d\/\d)', kwargs)}
                else:
                    values = {k:v for k,v in re.findall('([\w-]+)=([\w\.-]+)', kwargs)}
                for k,v in values.items():
                    if v in ['True', 'true']:
                        values[k]=True
                    elif v in ['False', 'false']:
                        values[k]=False
                if rpc in ['get-config', 'get_config']:
                    filter_xml = args['filter_xml']
                    if filter_xml is not None:
                        filter_xml = etree.XML(filter_xml)
                    values['format'] = args['format']
                    rpc_reply = getattr(self._conn.rpc, rpc.replace('-','_'))(filter_xml, options=values)
                else:
                    rpc_reply = getattr(self._conn.rpc, rpc.replace('-','_'))({'format':args['format']}, **values)

                if isinstance(rpc_reply, etree._Element):
                    if args.get('format') == 'text':
                        #logger.info (rpc_reply.text,also_console=self.console)
                        results['text']=rpc_reply.text
                    elif args.get('format') == 'set':
                        results['text']=rpc_reply.text
                    else:
                        #logger.info(etree.tostring(rpc_reply),also_console=self.console)
                        results['xml']=etree.tostring(rpc_reply)
                else:
                    if args.get('format') == 'json':
                        results['json'] = rpc_reply
                        logger.info(str(rpc_reply))

#                    else:
#                        logger.info(rpc_reply,also_console=self.console)
                results['changed'] = True
            except Exception as err:
                results['failed'] = True
                raise ContinuableError(err)
            return results

        def junos_rpc_text(self,**kvargs):

            """
                Function that executes and RPC on JUNOS device returning the results as text only
                robot example : Execute    Junos Rpc    ${target}    rpc=get-configuration    format=set    kwargs='routing_engine=master'
            """

            args = kvargs
            if 'kwargs' in kvargs.keys():
                kwargs = args['kwargs']
            else:
                kwargs = None
            rpc = args['rpc']

            try:
                if kwargs is None:
                    values = {}
                elif re.search(r'\{.*\}', kwargs):
                    values = {k:v for k,v in re.findall(r'([\w-]+)\s?:\s?\'?\"?([\w\.-]+)\'?\"?',kwargs)}
                elif re.search(r'[\w-]+=[\w\.-]+\/\d\/\d.\d',kwargs):
                    values = values = {k:v for k,v in re.findall('([\w-]+)=([\w\.-]+\/\d\/\d.\d)',kwargs)}
                elif re.search(r'[\w-]+=[\w\.-]+\/\d\/\d',kwargs):
                    values = {k:v for k,v in re.findall('([\w-]+)=([\w\.-]+\/\d\/\d)', kwargs)}
                else:
                    values = {k:v for k,v in re.findall('([\w-]+)=([\w\.-]+)', kwargs)}
                for k,v in values.items():
                    if v in ['True', 'true']:
                        values[k]=True
                    elif v in ['False', 'false']:
                        values[k]=False
                if rpc in ['get-config', 'get_config']:
                    filter_xml = args['filter_xml']
                    if filter_xml is not None:
                        filter_xml = etree.XML(filter_xml)
                    values['format'] = args['format']
                    rpc_reply = getattr(self._conn.rpc, rpc.replace('-','_'))(filter_xml, options=values)
                else:
                    rpc_reply = getattr(self._conn.rpc, rpc.replace('-','_'))({'format':args['format']}, **values)

                if isinstance(rpc_reply, etree._Element):
                    if args.get('format') == 'text':
                        results = rpc_reply.text
                    elif args.get('format') == 'set':
                        results = rpc_reply.text
                    else:
                        results = etree.tostring(rpc_reply)
                else:
                    if args.get('format') == 'json':
                        results  = rpc_reply
                        logger.info(str(rpc_reply))

            except Exception as err:
                raise ContinuableError(err)
            return results

