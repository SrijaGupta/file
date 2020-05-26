#!/usr/bin/env python

import imp

juniper_common = imp.load_source("juniper_common", "variables_file/juniper_common.py")
import juniper_common as juniper_common

import os
cwd = os.getcwd()

# import ansible variables
group_vars = cwd + "/../group_vars"
host_vars = cwd + "/../host_vars"

# barf if you can't find the directories
if (os.path.isdir(group_vars) == False) :
	raise Exception("Error, can't find directory: " + group_vars + " in " + cwd)
if (os.path.isdir(host_vars) == False) :
	raise Exception("Error, can't find directory: " + host_vars + " in " + cwd)

# parse the files
av = juniper_common.parse_ansible_vars(group_vars, host_vars)

# network client variables
client_user = av['group_vars']['all.yaml']['client_user']
client_password = av['group_vars']['all.yaml']['client_password']

for i in av['group_vars']['all.yaml']['clients']:
    exec(i['name'] + '_mgmt_ip = "' + i['mgmt_ip'] + '"')
    exec(i['name'] + '_ip = "' + i['ip'] + '"')
    exec(i['name'] + '_subnet = "' + i['subnet'] + '"')
    exec(i['name'] + '_gateway = "' + i['gateway'] + '"')

