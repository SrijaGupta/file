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
               print ("WARN Connection problems %s" %c_error)
               raise ContinuableError("Connection problems %s" %c_error)

        def close_connection (self):

            try:
                self._conn.close()
                return self
            except ConnectError as c_error:
               print ("WARN Connection problems %s" %c_error)
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
                print ("*WARN* Problems locking configuration: %s" % (l_error))
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
                print ("*WARN* Problems loading configuration: %s" % (error))
                raise FatalError("Unable to load configuration.....exiting")

            print ('*INFO* Configuration to be commited  %s' % (self._conn.candidate.diff()))

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

                        print ("*WARN* Problems locking configuration: %s" % (l_error))
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
                        print ("*WARN* Problems loading configuration: %s" % (error))
                        raise FatalError("Problems loading configuration,exiting...")


                    print '*INFO* Configuration to be commited  %s' % (self._conn.candidate.diff())
                    try:
                         self._conn.candidate.commit(comment=commit_comment)
                         self._conn.candidate.unlock()
                         return True
                    except (CommitError,LockError) as err:
                        #print err
                        self._conn.candidate.rollback()
                        print ("*WARN* Problems commiting configuration: %s" % (err))
                        raise FatalError("Error commiting configuration, exiting....")
                else:
                    raise FatalError("Expected result is True but was False,test will go on")
                    return False

       
