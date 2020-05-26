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

# ANSIBLE variables
import yaml
from os import walk

def parse_ansible_vars(group_vars, host_vars):
    gf = []
    for (dirpath, dirnames, filenames) in walk(group_vars):
	gf.extend(filenames)
	break

    hf = []
    for (dirpath, dirnames, filenames) in walk(host_vars):
	hf.extend(filenames)
	break

    av = {}
    av['group_vars'] = {}
    for i in gf:
	f = open(group_vars + "/" + i, "r")
	y = yaml.load(f)
	f.close()
	av['group_vars'][i] = y
    av['host_vars'] = {}
    for i in hf:
	f = open(host_vars + "/" + i, "r")
	y = yaml.load(f)
	f.close()
	av['host_vars'][i] = y

    return av
