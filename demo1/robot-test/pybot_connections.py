#!/usr/bin/env python
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
import paramiko
import re
import os
import sys
import logging

class pybot_connections(object):
    '''
    Defines vendor independent methods.
    Otherwise method left as a stub method.
    '''

    def __init__(self,**kvargs):

        #import pdb; pdb.set_trace()

        # Setting credentials
        self.user = kvargs['user']
        self.password = kvargs['password']
        self.target = kvargs['target']
        self.port = kvargs['port']
        self.log  = kvargs['log']
        self.connect()

    def __repr__ (self):

            return "pybot_connection: username=%s, target=%s, port=%s, password=%s, prompt=%s, device_type=%s, log=%s" %(self.username, self.target, self.port, self.password, self.prompt, self.device_type, self.log)

    def connect (self):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #In case the server's key is unknown,
            #we will be adding it automatically to the list of known hosts

            self.client.connect(self.target, port=int(self.port), username=self.user, password=self.password)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            self.client.close()
            raise

    def disconnect (self):
        try:
            self.client.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            self.client.close()
            raise

    def execute_command(self, cli_command):
        paramiko.util.log_to_file(self.log)
        stdin, stdout, stderr = self.client.exec_command(cli_command)
        return stdout.read()


# Continue with this:    https://github.com/ktbyers/netmiko/blob/master/netmiko/base_connection.py
