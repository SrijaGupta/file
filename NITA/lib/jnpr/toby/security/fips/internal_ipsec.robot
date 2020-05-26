*** Settings ***
Resource       jnpr/toby/Master.robot
Documentation    Keyword Used to configure internal IPSEC
...       Parameters
...              :param resource:
...      **REQUIRED** resource name
...              :param user:
...         **OPTIONAL** Username. Default is regress. 
...      :param password:
...         **OPTIONAL** Password to the provided user. Default is MaRtInI
...      :param protocol:
...         **OPTIONAL**: Protocol. Default is esp
...      :param spi:
...         **OPTIONAL**: Default is 512
...      :param auth_alg:
...         **OPTIONAL**: Authorization algorithm. Default is hmac-sha2-256
...      :param enc_alg:
...         **OPTIONAL**: Encryption algorithm. Default is aes-128-cbc
...      :param auth_key:
...         **OPTIONAL**: Authorization key. Default is Qwerty1234567890Qwerty123456789

*** Keywords ***

Configure Internal Ipsec
    [Arguments]    ${resource}    ${user}=regress    ${password}=MaRtInI    ${protocol}=esp    ${spi}=512   ${auth_alg}=hmac-sha2-256   ${enc_alg}=aes-128-cbc   ${auth_key}=Qwerty1234567890Qwerty1234567890   ${enc_key}=1234567890Qwerty
    
    ${re0-mgtip}=   Set Variable   ${t['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip']}
    ${re1-mgtip}=   Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re1']['mgt-ip']}    
    ${r0}=     connect to device    host=${re0-mgtip}    user=${user}    password=${password}    connect_mode=ssh
    ${r1}=     connect to device    host=${re1-mgtip}    user=${user}    password=${password}   connect_mode=ssh
    
    @{p1}   Create List    prompt security ipsec internal security-association manual direction bidirectional authentication key ascii-text
    @{p2}   Create List    prompt security ipsec internal security-association manual direction bidirectional encryption key ascii-text
    @{ipsec_config}   Create List   set security ipsec internal security-association manual direction bidirectional protocol ${protocol}
                                 ...    set security ipsec internal security-association manual direction bidirectional spi ${spi}
                                 ...    set security ipsec internal security-association manual direction bidirectional authentication algorithm ${auth_alg}
                                 ...    set security ipsec internal security-association manual direction bidirectional encryption algorithm ${enc_alg}
    @{auth}   Create List   ${auth_key}
    @{enc}   Create List   ${enc_key}
    @{comm}    Create List    commit synchronize
    
    ${result}=   Execute config command on device    ${r0}    command_list=@{comm}
    log to console    \n Commit Synchronize Given
    Log to console    \n before configuring IPSec :
    log to console    \n ${result}
    log to console    \n ------------------------
    
    Execute config command on device    ${r0}    command_list=@{ipsec_config}
    Execute config command on device    ${r0}    command_list=@{p1}    pattern=(.*)New(.*)
    Execute config command on device    ${r0}    command_list=@{auth}    pattern=(.*)Retype(.*)
    Execute config command on device    ${r0}    command_list=@{auth}
    ${b}=   Execute config command on device    ${r0}    command_list=@{p2}    pattern=(.*)New(.*)
    Execute config command on device    ${r0}    command_list=@{enc}    pattern=(.*)Retype(.*)
    Execute config command on device    ${r0}    command_list=@{enc}
    Commit configuration         device=${r0}      comment = commit successful      full=${TRUE}     detail=${TRUE}     response=${FALSE}

    Execute config command on device    ${r1}    command_list=@{ipsec_config}
    Execute config command on device    ${r1}    command_list=@{p1}    pattern=(.*)New(.*)
    Execute config command on device    ${r1}    command_list=@{auth}    pattern=(.*)Retype(.*)
    Execute config command on device    ${r1}    command_list=@{auth}
    ${b}=   Execute config command on device    ${r1}    command_list=@{p2}    pattern=(.*)New(.*)
    Execute config command on device    ${r1}    command_list=@{enc}    pattern=(.*)Retype(.*)
    Execute config command on device    ${r1}    command_list=@{enc}
    Commit configuration         device=${r1}      comment = commit successful

    disconnect from device    ${r0}
    ${r0}     connect to device    host=${re0-mgtip}  user=${user}     password=${password}   connect_mode=ssh
    ${result1}=   Execute config command on device    ${r0}    command_list=@{comm}
    log to console    \n Commit Synchronize Given
    Log to console    \n After Configuring IPSec :
    log to console    \n ${result1}
   
    Should contain    ${result1}    commit complete   msg=Commit synchronize not worked    values=False
    

