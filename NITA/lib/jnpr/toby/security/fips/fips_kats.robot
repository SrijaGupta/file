***settings***
Resource   jnpr/toby/Master.robot
Library    String
Documentation    Keyword Used to validate KATS have passed in FIPS mode
...              Parameters
...              :param resource:
...                 **REQUIRED** resource name
...              :param user:
...                 **OPTIONAL** Username. Default is regress.
...             :param password:
...                 **OPTIONAL** MaRtInI


*** Variables ***
${counter}    ${0}

*** Keywords ***
FIPS Self Tests KATS
    [Arguments]    ${resource}    ${user}=regress    ${password}=MaRtInI
    [Documentation]    Validates KATS tests
    ${conip}=    Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re0']['con-ip']}
    ${model}=    Set Variable    ${t['resources']['r0']['system']['primary']['model']} 
    ${device}=    connect to device   host=${conip}   model=${model}    connect_targets=console    user=${user}    password=${password}    connect_mode=telnet
    Execute cli command on device    ${device}    command= request system reboot    pattern=(.*)
    ${console_log}=    Execute cli command on device    ${device}    command= yes    pattern=(.*)login(.*)    timeout=${900}
    @{lines}=    split to Lines    ${console_log}
    
    ${list_len}=    Get Length    ${lines}
    ${counter}     Set Variable    0
    :FOR    ${i}    in   @{lines}
    \    ${ss}=    Get Lines Containing String   ${i}    Running FIPS Self-tests
    \    ${slen}=    Get length    ${ss}
    \    Run keyword If    ${slen}>10      Log    \nRunning FIPS Self-tests
    \    ${counter}=    Evaluate   ${counter}+1
    \    Exit For Loop If    ${slen}>0    
    
    :FOR    ${j}    in Range    ${counter}    ${list_len}
    \    ${check_string}=    set variable    @{lines}[${j}]
    \    ${loop_exit}=   Set Variable    ${check_string.find("commit complete")}
    \    Exit For Loop If    ${loop_exit}>0
    \    ${kat}=    Set Variable    ${check_string.find("Known Answer Test")}
    \    ${str}=    Set Variable If    ${kat}>0     @{lines}[${j}]    x 
    \    ${test}=    Get Substring    @{lines}[${j}]    7
    \    ${sub_str}    Get Substring    ${str}     -6
    \    Run Keyword If    '${sub_str}'=='Failed'    Fail    ${test}
    \    Log    @{lines}[${j}]
