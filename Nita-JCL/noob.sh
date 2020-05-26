#!/bin/bash
# <*******************
# 
# Copyright 2016 Juniper Networks, Inc. All rights reserved.
# 
# *******************>
rm -f ~/.ssh/known_hosts
temp_dir=$1
build_dir=/var/tmp/build

if [ $# -ne 0 ] && [ "$temp_dir" !=  "None" ]; then
        build_dir=$temp_dir
fi

ansible-playbook -i hosts noob/sites.yaml  --extra-vars "build_dir=$build_dir"
touch $build_dir/ansible-run.log
sudo chmod 664 $build_dir/ansible-run.log
