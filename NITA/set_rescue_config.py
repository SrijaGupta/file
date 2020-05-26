# <*******************
#
# Copyright 2016-18 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# *******************>
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos import Device

import yaml


# import ansible variables
host_vars = "../host_vars/"
group_vars = "../group_vars/"

all_vars = group_vars + 'all.yaml'
firewall_vars = host_vars + 'fw-vdc-001.yaml'

f_group = open(all_vars, 'r')
group_dict = yaml.load(f_group)
f_group.close()

f_fw = open(firewall_vars, 'r')
fw_dict = yaml.load(f_fw)
f_fw.close()

user = group_dict.get('netconf_user')
password = group_dict.get('netconf_passwd')
firewall_mgmt_ip = fw_dict.get('node').get('oob').get('re0').get('address')

dev = Device(host=firewall_mgmt_ip, user=user, password=password)
dev.open()

ss = StartShell(dev)
ss.open()
ss.run('cli -c "request system configuration rescue save"')
ss.close()
