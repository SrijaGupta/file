#!/usr/bin/env python

import imp

juniper_common = imp.load_source("juniper_common", "juniper_common.py")
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

# populate variables
#user = av['group_vars']['all.yaml']['netconf_user']
#password = av['group_vars']['all.yaml']['netconf_passwd']

# set the management ip variables i.e. vmx1_mgmt_ip = "100.123.1.0"
for key, value in av['host_vars'].iteritems():
    ip = value['management_interface']['ip']
    exec(key.replace(".yaml","") + '_mgmt_ip = "' + ip + '"')

# core interface ip variables for use in tests
# create ci_vmx1_ge_0_0_0, etc
for key0, value0 in av['host_vars'].iteritems():
    for i in value0['core_interfaces']:
        hname = key0.replace("-","_").replace(".yaml", "")
        iname = i['int'].replace("/","_").replace("-","_")
        ip = i['ip']
        exec('ci_' + hname + '_' + iname + '=' + '"' + ip + '"')
