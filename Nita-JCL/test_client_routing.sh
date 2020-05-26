#!/bin/bash

umask 0002

BASE=test_client_routing

# Creating of result files and making them R/W by everybody
mkdir $BASE/outputs
touch $BASE/outputs/output.xml
touch $BASE/outputs/log.html
touch $BASE/outputs/report.html

export PYTHONPATH=libraries

(cd $BASE && pybot -L TRACE tests/)

chmod -R 777 $BASE/tests
chmod -R 777 $BASE/resource_files/tmp
chmod -R 777 $BASE/outputs

