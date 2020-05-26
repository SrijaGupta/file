#!/bin/bash
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

rm -f ~/.ssh/known_hosts
temp_dir=$1
build_dir=/var/tmp/build

if [ $# -ne 0 ] && [ "$temp_dir" !=  "None" ]; then
        build_dir=$temp_dir
fi

ansible-playbook -i hosts build/sites.yaml  --extra-vars "build_dir=$build_dir"
touch $build_dir/ansible-run.log
sudo chmod 664 $build_dir/ansible-run.log
