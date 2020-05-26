*** Settings ***
Documentation  
...            This resource file is collection of linux operation defined in ALG
...            
...            Author: Vincent Wang (wangdn@juniper.net)
...            
...            Keywords List:
...                Check Ping
...

*** Keywords ***

Check Ping
    [Documentation]    Do ping to check the connection
    ...                Example:
    ...                    Check Ping    srx0    192.168.1.1
    ...                    Check Ping    linux1    ${h2_ip_addr}
    [Arguments]    ${device}=linux0    
    ...            ${ip}=1.2.3.4
    ...            ${count}=3
    
    ${device_model} =    GET T    resource=${device}    system_node=primary    attribute=model
    ${device_handle} =    Get Handle    resource=${device}
    
    Run Keyword If    '${device_model}' == 'linux'      Check Linux Ping Result    ${device_handle}    ${ip}    ${count}
    ...    ELSE IF    '${device_model}' == 'windows'    Check Windows Ping Result    ${device_handle}    ${ip}    ${count}
    ...    ELSE       Check SRX Ping Result    ${device_handle}    ${ip}    ${count}
    
    
    