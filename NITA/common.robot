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
*** Settings ***
Documentation     Suites of tests to be executed on all devices of the NITA topology.

#execute from /project
Resource              lib/jnpr/toby/Master.robot
Library               DateTime
Library              jnpr/toby/hardware/chassis/chassis.py
Suite Setup           Toby Suite Setup
Suite Teardown        Toby Suite Teardown

*** Variables ***
${SUITE_DIRECTORY}                      /suites

#${dut}                                  device0
${minimum_system_users}                 0
${minimum_pfe_local_traffic}            0
${maximum_time_offset}                  5minutes
${minimum_free_space}                   818956
${login_message}                        "Lasciate_ogni_speranza_o_voi_che_entrate"


*** Keywords ***

*** Test Cases ***

T1.1: CHECK SYSTEM USER
    [Tags]  SYSTEM  COMMON  USER
    [Documentation]     Objective: Check there are users in the system
    ${args}=    Evaluate     { 'minimum_system_users': ${minimum_system_users} }
    verify           devices=${dut}     checks=system_users_check      args=${args}     file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml


T1.2: CHECK CONFIGURATION
    [Documentation]     Objective: Check configuration for the device
    [Tags]  SYSTEM  COMMON  CONFIGURATION
    verify           devices=${dut}     checks=check_configuration      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml


T1.3: SHOW PFE STATISTICS LOCAL TRAFFIC
    [Documentation]     Objective: Check PFE statistics
    [Tags]  SYSTEM  COMMON
    ${args}=    Evaluate     { 'minimum_pfe_loal_traffic': ${minimum_pfe_local_traffic} }
    verify           devices=${dut}     checks=check_pfe_stats_local_traffic     args=${args}      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

# T1.4: CHECK SYSTEM CURRENT TIME
#     # [Documentation]     Objective: Check system current time
#     [Tags]  SYSTEM  COMMON  NTP
#     ${date} =     Get Current Date
#     ${current_date} =   Convert Date      ${date}     epoch

#     ${upper_system_time} =    Add Time To Date               ${current_date}      ${maximum_time_offset}
#     ${upper_system_time} =    Convert Date      ${upper_system_time}      epoch

#     ${lower_system_time} =    Subtract Time From Date           ${current_date}      ${maximum_time_offset}
#     ${lower_system_time} =    Convert Date      ${lower_system_time}      epoch

#     ${args}=    Evaluate     { 'lower_system_time': ${lower_system_time} , 'upper_system_time': ${upper_system_time}}
#     verify           devices=${dut}     checks=check_system_local_time      args=${args}    file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml


T1.5: CHECK NO CHASSIS ALARMS
    [Documentation]     Objective: Check there are no chassis alarms
    [Tags]  SYSTEM  COMMON  ALARMS
    verify           devices=${dut}     checks=check_no_chassis_alarms       file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

T1.6: CHECK NO SYSTEM ALARMS
    [Documentation]     Objective: Check there are no system alarms
    [Tags]  SYSTEM  COMMON  ALARMS  RESEARCH
    verify           devices=${dut}     checks=check_no_system_alarms       file=common_suite_template.yaml

T1.7: CHECK NO CORE DUMPS PRESENT
    [Documentation]     Objective: Check there are no core dumps present
    [Tags]  SYSTEM  COMMON  ALARMS  CORE_DUMPS
    verify           devices=${dut}     checks=check_no_core_dumps       file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

# T1.7 comma A: CHECK NO CORE DUMPS PRESENT
#     # [Documentation] Objective: Check there are no core dumps present
#     [Tags]  SYSTEM  COMMON  ALARMS  CORE_DUMPS  RESEARCH
#     ${dh}=    Get Handle    resource=${dut}
#     ${result}=    Detect Core On Junos Device    resource=${dh}

T1.8: CHECK '/dev/ad0s1a' PARTITION HAVE ENOUGH FREE SPACE FOR UPGRADE
    [Documentation]     Objective: Check '/dev/ad0s1a' partition have at least 400MB for upgrade
    [Tags]  SYSTEM  COMMON
    ${args}=    Evaluate     { 'minimum_free_space' : ${minimum_free_space} }
    verify           devices=${dut}     checks=check_partition     args=${args}    file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

T1.9: CHECK FPC IS ONLINE
    [Documentation]     Objective: Check FPC is Online
    [Tags]  SYSTEM  COMMON
    verify           devices=${dut}     checks=check_FPC_online      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

T1.10: ADD TOBY USER
    [Documentation]     Objective: Add new user Toby with password NitaToby
    [Tags]  SYSTEM  COMMON  ALE
    @{cmd_list} =  Set Variable
    ...     set system login user Toby full-name "Toby"
    ...     set system login user Toby authentication encrypted-password "$1$cxYCj59X$TxadTJZMepeHlEyknEIjF1"
    ...     set system login class TestClass permissions all
    ...     set system login user Toby class TestClass
    Config Engine    device_list=${dut}     cmd_list=@{cmd_list}        commit=True     load_option=merge
    verify           devices=${dut}     checks=check_toby_user_exists      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

# T1.12: SET TIMEZONE
#     # [Documentation]     Objective: Set Europe/Prague timezone to JunOS
#     [Tags]  SYSTEM  COMMON  TIMEZONE
#     Config Engine     device_list=${dut}     load_option=merge     commit=True   load_file=${SUITE_DIRECTORY}/config/timezone.conf

# T1.13: CHECK TIMEZONE
#     # [Documentation]     Objective: Check Europe/Prague timezone is set on JunOS
#     [Tags]  SYSTEM  COMMON  ALE
#     verify           devices=${dut}     checks=check_timezone      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

# T1.14: SET CUSTOMIZED LOGIN MESSAGE
#     [Tags]  SYSTEM  COMMON  MESSAGE  ALE
#     # from configuration snippet
#     # Config Load    device=device1     load_option=merge     commit=True   file=/project/test/suites/config/login_message.conf
#     # from YAML parameter file
#     ${args}=    Evaluate     { 'login_message' : ${login_message} }
#     @{config} =         create list     ${SUITE_DIRECTORY}/config/param_login_msg.yaml
#     @{template} =         create list     set_login_message
#     Config Engine   device_list=${dut}     template_files=${config}     config_templates=${template}      vars=${args}     commit=1         


T1.15: CREATE NEW SYSLOG FILE FOR ALL EVENTS OF ALL PRIORITIES
    [Documentation]     Objective: Create my_toby_log.txt to store all syslog messages of JunOS device and limit rollback to 5 configurations
   [Tags]  SYSTEM  COMMON  SYSLOG  ROLLBACK
    @{cmd_list} =  Create List         set system syslog file my_toby_log.txt any any
    Config Engine    device_list=${dut}     cmd_list=@{cmd_list}        commit=True     load_option=merge
    verify           devices=${dut}     checks=check_my_toby_log_exists      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

# T1.17: SET ALTITUDE AND COUNTRY CODE
#     # [Documentation]     Objective: Set location altitude and country-code
#    [Tags]  SYSTEM  COMMON  LOCATION
#     @{cmd_list} =  Set Variable
#     ...     set system location altitude -7
#     ...     set system location country-code NL
#     Config Engine    device_list=${dut}     cmd_list=@{cmd_list}        commit=True     load_option=merge

# T1.18: SAVE AT MOST 5 CONFIGURATIONS ON FLASH
#     # [Documentation]     Objective:  limit flash storage to 5 configurations
#    [Tags]  SYSTEM  COMMON  SYSLOG  FLASH
#     @{cmd_list} =  Create List         set system max-configurations-on-flash 5
#     Config Engine    device_list=${dut}     cmd_list=@{cmd_list}        commit=True     load_option=merge
#     verify           devices=${dut}     checks=check_max_configurations_on_flash      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

# T1.20: SET SERIAL ALARM
#     # [Documentation]     Objective: Set chassis serial alarm to red for both tx and rx
#    [Tags]  SYSTEM  COMMON  SERIAL
#     @{cmd_list} =  Create List     set chassis alarm serial loss-of-rx-clock red loss-of-tx-clock red
#     Config Engine    device_list=${dut}     cmd_list=@{cmd_list}        commit=True     load_option=merge
#     verify           devices=${dut}     checks=check_serial_alarms      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml

# T1.22: CHECK FPC AND PIC STATUS
#     # [Documentation]     Objective: Check FPC and PIC status
#    [Tags]  SYSTEM  COMMON  SERIAL
#    verify           devices=${dut}     checks=check_fpc_pic_status      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml


T1.23: CHECK PACKET FORWARDING ENGINE TERSE
    [Documentation]     Objective: Check pfe terse statistics
    [Tags]  SYSTEM  COMMON  SERIAL
    verify           devices=${dut}     checks=check_pfe_terse      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml


# T1.24: CHECK PFE STATISTICS
#     [Documentation]     Objective: Check pfe statistics
#     [Tags]  SYSTEM  COMMON  SERIAL
#     verify           devices=${dut}     checks=check_pfe_statistics      file=${SUITE_DIRECTORY}/verify/common_suite_template.yaml


