*** Settings ***
Documentation  
...            This resource file is collection of SRX operation defined in ALG
...            
...            Author: Vincent Wang (wangdn@juniper.net)
...
...            Keywords List:
...                Show SRX ALG Status
...                Show SRX NAT PST Binding
...                Clear SRX NAT PST Binding
...                Config SRX Service TWAMP Client
...                Config SRX Service TWAMP Server
...                Check SRX Service TWAMP Client Results

*** Keywords ***

Show SRX ALG Status
    [Documentation]    Execute cli command: show security alg status
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
    
    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=show security alg status node ${node} | no-more
    ...       ELSE                                  Execute cli command on device    ${device}    command=show security alg status | no-more

Show SRX NAT PST Binding
    [Documentation]    Execute cli command: show security nat source persistent-nat-table all
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
    
    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=show security nat source persistent-nat-table all node ${node} | no-more
    ...       ELSE                                  Execute cli command on device    ${device}    command=show security nat source persistent-nat-table all | no-more
    
Clear SRX NAT PST Binding
    [Documentation]    Execute cli command: clear security nat source persistent-nat-table all
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
    
    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=clear security nat source persistent-nat-table all node ${node}
    ...       ELSE                                  Execute cli command on device    ${device}    command=clear security nat source persistent-nat-table all 

Config SRX Service TWAMP Client
    [Documentation]    Set TWAMP client configuration on SRX
    [Arguments]    ${device}=${srx0}
    ...            ${target_address}=${None}
    ...            ${probe_count}=2000
    ...            ${control}=c1
    ...            ${test}=t1
    ...            ${commit}=True
    
    ## Set service twamp client
    @{conf_list} =    Set Variable
    ...               delete services rpm twamp
    ...               set services rpm twamp client control-connection ${control} authentication-mode none
    ...               set services rpm twamp client control-connection ${control} target-address ${target_address}
    ...               set services rpm twamp client control-connection ${control} test-session ${test} target-address ${target_address}
    ...               set services rpm twamp client control-connection ${control} test-session ${test} probe-count ${probe_count}
    
    Config Engine    device_list=${device}    cmd_list=@{conf_list}    commit=${commit}
    
    
Config SRX Service TWAMP Server
    [Documentation]    Set TWAMP server configuration on SRX
    [Arguments]    ${device}=${srx0}
    ...            ${client_prefix}=${None}
    ...            ${client_list}=client1
    ...            ${commit}=True
    
    ## Set service twamp server
    @{conf_list} =    Set Variable
    ...               delete services rpm twamp
    ...               set services rpm twamp server authentication-mode none
    ...               set services rpm twamp server client-list ${client_list} address ${client_prefix}
    
    Config Engine    device_list=${device}    cmd_list=@{conf_list}    commit=${commit}
       
Check SRX Service TWAMP Client Results
    [Documentation]    Execute cli command to check twamp results: show services rpm twamp client history-results
    [Arguments]    ${device}=${srx0}
    ...            ${control_connection}=${None}
    ...            ${test_session}=${None}

    ${command} =    show services rpm twamp client history-results
    Run Keyword If    "${control_connection}" is not "${None}"    ${command} =    Catenate    ${command}    control-connection    ${control_connection}
    Run Keyword If    "${test_session}" is not "${None}"          ${command} =    Catenate    ${command}    test-session    ${test_session}
    
    ${result}    Execute cli command on device    ${device}    command=${command}
    Should Contain    ${result}    usec
    
    