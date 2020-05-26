#!/bin/bash

umask 0002

# Creating of result files and making them R/W by everybody
mkdir test/outputs
touch test/outputs/output.xml
touch test/outputs/log.html
touch test/outputs/report.html

export PYTHONPATH=libraries

(cd test && pybot -C ansi -L TRACE tests/)

chmod -R 777 test/tests
chmod -R 777 test/resource_files/tmp
chmod -R 777 test/outputs

