#!/usr/bin/python
# <*******************
# 
# Copyright 2016 Juniper Networks, Inc. All rights reserved.
# 
# *******************>

import sys
import yaml
import json
from yaml import SafeDumper
import os 
import stat

try:
	
	with open('data.json') as data_file:
		data = json.load(data_file)
	SafeDumper.add_representer(
	    type(None),
	    lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
	)

	for filename,conf in data.iteritems():
		if ("group_vars/" in filename or "host_vars/" in filename) and (".yaml" in filename or ".yml" in filename):
			try:
				yaml_content = yaml.safe_dump(conf,default_flow_style=False,explicit_start = True)
				with open(filename, 'w') as outfile:
   					outfile.write(yaml_content)
					os.chmod(filename,0775)
			except:
				print "Yaml is not generated"
		else:
			print "Inavalid File Name Found =====> "+filename
except: 
	print "************** No configuration data is received **************************"
	pass

