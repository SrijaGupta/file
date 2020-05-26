*** Settings ***
Documentation
...            This resource file is collection of linux operation defined in VoIP ALG
...            
...            Author: Vincent Wang (wangdn@juniper.net)
...            
...            Keywords List:
...                Check Linux Tool WARP17-H323
...                Delete Linux Interface Namespace
...                Set Linux Service GNUGK Home Address
...                Set Linux WARP17-H323 Profile
...                Restore Linux Service GNUGK Config 
...                Start Linux Service GNUGK
...                Stop Linux Service GNUGK
...                Send Linux H323 WARP17 Traffic 
...                Stop Linux H323 WARP17 Traffic 
...

*** Keywords ***
Check Linux Tool WARP17-H323
    [Documentation]    H323 Traffic Start
    [Arguments]    ${device}=${linux0}
    ...            ${path}=${None}
    #Switch To Super User      ${device}
    Execute Shell Command on Device    ${device}    command=cd ${path}
    ${result}    Execute Shell Command on Device    ${device}    command=./warp17-h323-gen.sh
    Should Contain    ${result}    h323-profile

Delete Linux Interface Namespace
    [Documentation]    Delete the namespace on interface
    [Arguments]    ${device}=${linux0}
    ...            ${interface}=eth1
    
    Switch To Super User    ${device}
    ${intf_ns}    Catenate    SEPARATOR=-    ${interface}    ns
    #Switch To Super User      ${device}
    Execute Shell Command on Device    ${device}     command=ip netns del ${intf_ns}
    
Restore Linux Service GNUGK Config 
    [Documentation]    Restore the GNUGK config file
    [Arguments]    ${device}=${linux0}
    ...            ${config}=gatekeeper.ini
    
    ${config_bak}    Catenate    SEPARATOR=_    ${config}    bak
    #Switch To Super User      ${device}
    Execute Shell Command on Device    ${device}    command=cp -f ${config_bak} ${config}

Set Linux Service GNUGK Home Address
    [Documentation]    Set the home address in GNUGK config file
    [Arguments]    ${device}=${linux0}
    ...            ${config}=gatekeeper.ini
    ...            ${address}=${None}
    
    ${config_bak}    Catenate    SEPARATOR=_    ${config}    bak
    
    #Switch To Super User      ${device}
    Execute Shell Command on Device    ${device}    command=rm -f ${config_bak}
    Execute Shell Command on Device    ${device}    command=cp -f ${config} ${config_bak}
    Execute Shell Command on Device    ${device}    command=sed -i '/^Home=/'d ${config}
    Execute Shell Command on Device    ${device}    command=sed -i '/^EnableIPv6=/'d ${config}
    Execute Shell Command on Device    ${device}    command=sed -i '/^Name/a\Home=${address}' ${config}
    Run Keyword If    ":" in "${address}"    Execute Shell Command on Device    ${device}    command=sed -i '/^Name/a\EnableIPv6=1' ${config}

Set Linux WARP17-H323 Profile
    [Documentation]    Set the IP address in WARP17-h323 profile
    [Arguments]    ${device}=${linux0}
    ...            ${profile}=${None}
    ...            ${section}=outgoing
    ...            ${item}=dest_ipv6_base
    ...            ${value}=${None}
    ...            ${path}=/home/warp17/warp17-h323/userapps/warp17-h323
    
    ${profile_bak}    Catenate    SEPARATOR=_    ${profile}    bak
    
    #Switch To Super User      ${device}
    Execute Shell Command on Device    ${device}    command=cd ${path}
    Execute Shell Command on Device    ${device}    command=rm -f ${profile_bak}
    Execute Shell Command on Device    ${device}    command=cp -f ${profile} ${profile_bak}
    Execute Shell Command on Device    ${device}    command=sed -i '/^${item}=/'d ${profile}
    Execute Shell Command on Device    ${device}    command=sed -i '/^\\${section}/a\\${item}=${value}' ${profile}
    
Start Linux Service GNUGK
    [Documentation]    Start GNUGK
    [Arguments]    ${device}=${linux0}
    ...            ${config}=gatekeeper.ini
    ...            ${mode}=${None}
    
    #Switch To Super User      ${device}
    Execute Shell Command on Device    ${device}    command=source /root/.bash_profile
    Execute Shell Command on Device    ${device}    command=gnugk ${mode} -c ${config} &
    Sleep    3
    Execute Shell Command on Device    ${device}    command=whoami
    ${result}    Execute Shell Command on Device    ${device}    command=ps aux | grep gnugk
    Should Contain    ${result}    ${config}

Stop Linux Service GNUGK
    [Documentation]    Stop GNUGK
    [Arguments]    ${device}=${linux0}
    
    #Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}    command=ps aux | grep gnugk
    @{pid_list} =    Get Regexp Matches    ${result}    root\\s+(\\d+).+\-c    1
    ${pid_len}=    Get Length    ${pid_list}
    Run Keyword If    ${pid_len} is not 0    Execute Shell Command on Device    ${device}    command=kill -SIGINT @{pid_list}[0]
    
Send Linux H323 WARP17 Traffic
    [Documentation]    H323 Traffic Send
    [Arguments]    ${device}=${linux0}
    ...            ${role}=src
    ...            ${interface}=eth1  
    ...            ${profile}=${None}
    ...            ${path}=/home/warp17/warp17-h323/userapps/warp17-h323 
    
    #Switch To Super User      ${device}
    Delete Linux Interface Namespace    ${device}    {interface}
    Execute Shell Command on Device    ${device}    command=cd ${path}
    Execute Shell Command on Device    ${device}    command=echo "" >nohup.out
    Execute Shell Command on Device    ${device}    command=nohup ./warp17-h323-gen.sh -n ${role} -i ${interface} -f ${profile} &
    Sleep    2    
    ${result}    Execute Shell Command on Device    ${device}    command=ps aux | grep obj_linux_x86_64/warp17-h323-gen
    @{pid_list} =    Get Regexp Matches    ${result}    root\\s+(\\d+).+\-n    1
    ${pid_len}=    Get Length    ${pid_list}
    Run Keyword If    ${pid_len} == 0    Execute Shell Command on Device    ${device}    command=cat nohup.out
    [Return]    @{pid_list}[0]
    
Stop Linux H323 WARP17 Traffic 
    [Documentation]    H323 Traffic Stop
    [Arguments]    ${device}=${linux0}
    ...            ${pid}=${None}
    
    #Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}    command=ps aux | grep obj_linux_x86_64/warp17-h323-gen
    @{pid_list} =    Get Regexp Matches    ${result}    root\\s+(\\d+).+\-n    1
    #Run Keyword If    "${pid}" is not "${None}"    Log    ${pid}
    #...       ELSE                                 ${pid} =    Get Regexp Matches    ${result}    root\\s+(\\d+)    1
    ${pid_len}=    Get Length    ${pid_list}
    Run Keyword If    ${pid_len} is not 0    Execute Shell Command on Device    ${device}    command=kill -SIGINT @{pid_list}[0]
    
    