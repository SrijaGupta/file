*** Setting ***
Documentation  
...     This file contains all the robot common keyword for Windows 
...     Wentao Wu (wtwu@juniper.net)
...
...     Keyword list: 
...             #Config Windows Interface IP Address
...             Config Windows Static Route
...             #Delete Windows Interface IP Address
...             Delete Windows Static Route
...             Check Windows Ping Result
...             Check Windows Ping Timtout Result
...             Delete Windows File
...             Set Windows Firewall Status
...             Config Windows Telnet Service
...             Config Windows NTP Service
...             Set Windows Service Status
...             Restart Windows Service
...             Set Windows Interface Status
...             Restart Windows Interface
...             Get TimeZone And DateTime
...             Export Windows Trust Root Certification
...             Upload Windows File to FTP Server
...             Check Window Listen Port
...             Send Windows Ftp Traffic

*** Keywords ***
# replaced with python keywords
#Config Windows Interface IP Address
#    [Documentation]    Set Windows Interface IP address
#    [Arguments]    ${device}=${win0}
#    ...            ${interface}=${tv['win0_intf1_name']}
#    ...            ${ip}=1.2.3.4
#    ...            ${mask}=24
#    
#    Execute Shell Command on Device    ${device}     command=c:/windows/system32/cmd.exe
#    Run Keyword If   ":" in "${ip}"     Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv6" set address "${interface}" ${ip}/${mask}
#    ...       ELSE                      Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv4" set address "${interface}" static ${ip}/${mask}
#    Sleep    5s    Wait for address duplicate probe 
#    ${result} =    Run Keyword If    ":" in "${ip}"    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv6" show address "${interface}"
#    ...                      ELSE                      Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv4" show address "${interface}"
#    Should Contain    ${result}    ${ip}
    
Config Windows Static Route
    [Documentation]    Config Windows Static Route
    [Arguments]    ${device}=${win0}
    ...            ${net}=1.2.3.0/24
    ...            ${nexthop}=1.2.3.1
    ...            ${interface}=${None}
                                                                                            
    Run keyword if    "${interface}" is not "${None}"    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe interface ipv6 add route ${net} "${interface}" ${nexthop}
    ...      ELSE                                     Execute Shell Command on Device    ${device}     command=c:/windows/system32/route.exe add ${net} ${nexthop}
    ${result} =    Execute Shell Command on Device    ${device}     command=c:/windows/system32/route.exe print

Check Windows Ping Result
    [Documentation]    Do ping to check the connection on Windows host
    [Arguments]    ${device}=${win0} 
    ...            ${ip}=1.2.2.2
    ...            ${count}=2
    
    ${result}    Execute Shell Command on Device    ${device}     command=c:/windows/system32/ping.exe -n ${count} ${ip}
    Should Not Match Regexp    ${result}    100%\\s+loss
    #Should Match Regexp        ${result}    TTL=\\d+    # this check not pass for IPv6 address
 
Check Windows Ping Timeout Result
    [Documentation]    Do ping to check the connection on Windows host
    [Arguments]    ${device}=${win0} 
    ...            ${ip}=1.2.2.2
    ...            ${count}=2
    
    ${result}    Execute Shell Command on Device    ${device}     command=c:/windows/system32/ping.exe -n ${count} ${ip}
    #Should Not Match Regexp    ${result}    TTL=\\d+         # this check not pass for IPv6 address
    #Should Match Regexp    ${result}    Request\\s+timed\\s+out
    Should Match Regexp    ${result}    100%\\s+loss

#Delete Windows Interface IP Address
#    [Documentation]    Delete Windows Interface IP address
#    [Arguments]    ${device}=${win0}
#    ...            ${interface}=${tv['win0_intf1_name']}
#    ...            ${ip}=${None}
#    ...            ${mask}=${None}
#    
#    Execute Shell Command on Device    ${device}     command=c:/windows/system32/cmd.exe 
#    Run Keyword If    ":" in "${ip}"    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv6" delete address "${interface}" ${ip}
#    ...    ELSE IF    "." in "${ip}"    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv4" delete address "${interface}" ${ip} 
#    ...       ELSE                      Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv4" set address "${interface}" source=dhcp 
#    Sleep    5s    Wait for address clear 
#    ${result} =    Run Keyword If    ":" in "${ip}"    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv6" show address "${interface}"
#    ...                   ELSE IF    "." in "${ip}"    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv4" show address "${interface}"
#    ...                      ELSE                      Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe -c "interface ipv4" show address "${interface}"
#    Run Keyword If    ":" in "${ip}"    Should Not Contain    ${result}    ${ip}
#    ...    ELSE IF    "." in "${ip}"    Should Not Contain    ${result}    ${ip}
#    ...       ELSE                      Should Contain        ${result}    Yes
	    
Delete Windows Static Route
    [Documentation]    Delete Windows Static Route
    [Arguments]    ${device}=${win0}
    ...            ${net}=1.2.3.0
    
    ${result} =    Execute Shell Command on Device    ${device}     command=c:/windows/system32/route.exe delete ${net}
    Should Contain    ${result}    OK

Delete Windows File
    [Documentation]    Delete windows file
    [Arguments]    ${device}=${jims0}
    ...            ${file}=c:\\jims.cer
    ${result} =    Execute Shell Command on Device    ${device}    command=del ${file}

Set Windows Interface Status
    [Documentation]   Set Enable/Disable Windows Interface
    [Arguments]    ${device}=${win0}
    ...            ${interface}=trf
    ...            ${status}=enabled    # enabled | disabled
	
    Run Keyword If    "${status}" is "disabled"    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe interface set interface ${interface} disabled    timeout=${150}
    ...       ELSE                                 Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe interface set interface ${interface} enabled     timeout=${150}

Restart Windows Interface
    [Documentation]    Disable And Enable Windows Interface
    [Arguments]    ${device}=${win0}
    ...            ${interface}=trf
	
    Execute Shell Command on Device    ${device}     command=ipconfig/all
    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe interface set interface ${interface} disabled    timeout=${150}
    sleep    5
    Execute Shell Command on Device    ${device}     command=c:/windows/system32/netsh.exe interface set interface ${interface} enabled    timeout=${150}	

Set Windows Service Status
    [Documentation]    Start/Stop Windows Service
    [Arguments]    ${device}=${win0}
    ...            ${service}=jims
    ...            ${status}=start    # start  | stop
    ...            ${retry}=10
    ...            ${interval}=10
    
    :FOR    ${index}    IN RANGE    ${retry}
    \    Sleep    ${interval}
    \    ${result}    Execute Shell Command on Device    ${device}    command=c:/windows/system32/net.exe ${status} ${service}    timeout=${300}
    \    Run Keyword If    'could not be started' in '''${result}'''    Continue For Loop
    \     ...    ELSE IF    'could not be stopped' in '''${result}'''    Continue For Loop
    \     ...    ELSE IF    'stopped' in '''${result}'''    Exit For Loop
    \     ...    ELSE IF    'started' in '''${result}'''    Exit For Loop
    \     ...    ELSE IF    'starting' in '''${result}'''    Continue For Loop
    \     ...    ELSE IF    'stopping' in '''${result}'''    Continue For Loop

Restart Windows Service
    [Documentation]    Restart Windows Service
    [Arguments]    ${device}=${win0}
    ...            ${service}=jims

    Set Windows Service Status    ${device}    service=${service}    status=stop
    Set Windows Service Status    ${device}    service=${service}    status=start

Config Windows Telnet Service
    [Documentation]    Change Windows Telnet Service Config
    [Arguments]    ${device}=${win0}
    ...            ${key}=maxconn      # maxconn  |  maxfail  |  port
    ...            ${value}=5
	
    Execute Shell Command on Device    ${device}    command=c:/windows/system32/tlntadmn.exe config ${key}=${value}    timeout=${150}

Get TimeZone And DateTime
    [Documentation]    Show TimeZone And Date Time
    [Arguments]    ${device}=${win0}
    ...            ${item}=all      #  all  |  timezone  |  date  |  time
    
    ${timezone} =   Execute Shell Command on Device    ${device}    command=c:/windows/system32/tzutil.exe /g    timeout=${150}
    ${date} =       Execute Shell Command on Device    ${device}    command=date/t    timeout=${150}
    ${time} =       Execute Shell Command on Device    ${device}    command=time/t    timeout=${150}
    ${all} =        Catenate    ${timezone}    ${date}    ${time}
    Log             Timezone is : ${timezone} ,Date is : ${date} ,Time is : ${time}
    
    Run Keyword If   '${item}'=='timezone'    Return From Keyword    ${timezone}
    ...    ELSE IF    '${item}'=='date'       Return From Keyword    ${date}
    ...    ELSE IF    '${item}'=='time'       Return From Keyword    ${time}
    ...    ELSE                               Return From Keyword    ${all}

Set Windows Firewall Status
    [Documentation]    Turn On Or Turn Off Windows Firewall
    [Arguments]    ${device}=${win0}
    ...            ${status}=off
              
    Run Keyword If    '${status}'=='on'     Execute Shell Command on Device    ${device}    command=c:/windows/system32/netsh.exe firewall set opmode mode=enable    timeout=${150}
    ...    ELSE IF    '${status}'=='off'    Execute Shell Command on Device    ${device}    command=c:/windows/system32/netsh.exe firewall set opmode mode=disable    timeout=${150}    
    ...       ELSE                          Execute Shell Command on Device    ${device}    command=c:/windows/system32/netsh.exe firewall set opmode mode=disable    timeout=${150}   

Export Windows Trust Root Certification
    [Documentation]    export Windows trust root ca to file
    [Arguments]    ${device}=${win0}
    ...            ${name}="JIMS Auto Generated Root CA"
    ...            ${output}=c:\\jims.cer
    Execute Shell Command on Device    ${device}    command=del c:\\*.cer
    ${export} =    Execute Shell Command on Device    ${device}    command=c:\\windows\\system32\\certutil.exe -store Root ${name} c:\\test.cer
    Should Contain    ${export}    successfully
    ${result} =    Execute Shell Command on Device    ${device}    command=c:\\windows\\system32\\certutil.exe -encode c:\\test.cer ${output}
    Should Contain    ${result}    successfully
    Execute Shell Command on Device    ${device}    command=del c:\\test.cer

Upload Windows File to FTP Server
    [Documentation]    Upload windows file to ftp server
    [Arguments]    ${device}=${win0}
    ...            ${local_path}=c:\\
    ...            ${local_file}=jims.cer
    ...            ${remote_path}=/var/tmp/
    ...            ${server}=1.2.3.4
    ...            ${port}=21    #not work for windows now
    ...            ${user}=regress
    ...            ${password}=MaRtInI
    ${result} =    Execute Shell Command on Device    ${device}    pattern=User.*?    command=ftp ${server}
    Should Contain    ${result}    220
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${user}
    Should Contain    ${result}    331
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${password}
    Should Contain    ${result}    230
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=bin
    Should Contain    ${result}    200
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=lcd ${local_path}
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=cd ${remote_path}
    Should Contain    ${result}    250
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=put ${local_file}
    Should Contain    ${result}    226
    ${result} =    Execute Shell Command on Device    ${device}    command=bye
    Should Contain    ${result}    221

Check Windows Listen Port
    [Documentation]    Check Windows Listen Port
    [Arguments]    ${device}=${win0}
    ...            ${protocol}=TCP
    ...            ${port}=80
    ...            ${version}=ipv4       #   ipv4  |  ipv6
    ${result}    Execute Shell Command on Device    ${device}    command=c:\\windows\\system32\\netstat.exe -an | find ":${port} "    timeout=${150}
    Run Keyword If   '${version}'=='ipv6'    Should Match Regexp    ${result}    (?is).*?${protocol}\\s*\\[::\\]:${port}.*?LISTENIN    timeout=${150}
    ...       ELSE                          Should Match Regexp    ${result}    (?is).*?${protocol}\\s*0.0.0.0:${port}.*?LISTENING    timeout=${150}

Config Windows NTP Service
    [Documentation]    Configure Windows NTP Time Sync
    [Arguments]    ${device}=${win0}
    ...            ${server}=66.129.233.81
	Set Windows Service Status         ${device}    service=w32time    status=start	
	Check Windows Ping Result          ${device}    ip=${server}    
    Execute Shell Command on Device    ${device}    command=c:/windows/system32/w32tm.exe /config /manualpeerlist:"${server}" /syncfromflags:manual /update    timeout=${150}
	Execute Shell Command on Device    ${device}    command=c:/windows/system32/w32tm.exe /resync

Send Windows Ftp Traffic
    [Documentation]    Send Windows Ftp Traffic
    [Arguments]    ${device}=${win0}
    ...            ${server}=1.2.3.4
    ...            ${user}=regress
    ...            ${password}=MaRtInI
    ...            ${command}=pwd
    ...            ${close}=${None}
	
    ${result} =    Execute Shell Command on Device    ${device}    pattern=User.*?    command=ftp ${server}
    Should Contain    ${result}    220
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${user}
    Should Contain    ${result}    331
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${password}
    Should Contain    ${result}    230
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${command}
    Run Keyword If    "${close}" is not "${None}"    Execute Shell Command on Device    ${device}    command=bye
	
