*** Settings ***
Documentation
...     Resource file containing keywords to do Radius {Free Radius} specific tasks over a
...     SSH session.

Library     jnpr.toby.bbe.radius.radius.Radius

*** Variables ***

*** Keywords ***

configure certificates
    [Documentation]    
    ...                PURPOSE:
    ...                Configure certificates and load onto device
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                | -N/A
    ...             
    ...                ARGUMENTS:
    ...                | -tag : Radius server resource handle (MANDATORY)
    ...
    ...                RETURNS:
    ...                |  ${result}: True/False 
    ...                |  Returns True if certificates have been successfully configured and loaded onto the switch
    ...
    ...                EXAMPLE USAGE:  
    ...                |  e.g.     
    ...                |  configure certificates        h0
    ...

    [Arguments]         ${tag}
    [Return]            True or False
    
    ${result}   configure certificates   ${tag}
    Should be True      ${result}
       

add user config to radius server
    
    [Documentation]    
    ...                PURPOSE:
    ...                Add user config or coa user config to radius server users profile
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...             
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address   (MANDATORY)    
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - user_data: User information to be updated in the radius server (MANDATORY)
    ...                 | - filepath: Path of Files to be modified/added  (MANDATORY)
    ...                 | - usertype: if usertype = user then User details in "Users" file AND if usertype = coa then user for generation CoA request (MANDATORY)
    ...                 | - dm_param: if 'acct' - get Acct-Session-Id, if 'calling' - get Calling-Station-Id, if 'acct_calling" - get Acct-Session-Id and Calling-Station-Id; else ignore this arguments (MANDATORY)
    ...                 | - radius_logpath: Radius Logs File Path   (MANDATORY)
    ...
    ...                RETURNS:
    ...                |  ${value}: Returns True if radius user or coa user  has been added successfully to radius server
    ...                |          : Returns False if there was an error in adding radius server user or coa user 
    ...
    ...                EXAMPLE USAGE:  
    ...                |  e.g.     
    ...                |  To add radius user to radius server
    ...                |  add user config to radius server    ${tv['h0__if0__mgt-ip']}    ${tv['uv-radius-username']}    ${tv['uv-radius-password']}    ${user_data0}    ${tv['uv-radius-filepath']}/users    user    no   ${tv['uv-radius-logpath']}
    ...                |  
    ...                |  To add COA user to radius server
    ...                |  add user config to radius server           ${tv['h0__if0__mgt-ip']}    ${tv['uv-radius-username']}    ${tv['uv-radius-password']}     ${coa_session}    ${tv['uv-radius-filepath']}    coa   no  ${tv['uv-radius-logpath']}

    ...

    [Arguments]         ${hostip}   ${username}   ${password}   ${user_data}   ${filepath}   ${usertype}   ${dm_param}   ${radius_logpath}
    [Return]            True or False
    
    ${result}   add radius server user   ${hostip}   ${username}   ${password}   ${user_data}   ${filepath}   ${usertype}   ${dm_param}   ${radius_logpath}
    Should be True      ${result}


remove user config from radius server
    [Documentation]    
    ...                PURPOSE:
    ...                Remove user config or coa config from radius server users profile
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                           
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - radius_user: User information to be updated in the radius server (MANDATORY)
    ...                 | - attribute_num: Number for Attributed configured with User (MANDATORY)
    ...                 | - filepath: Path of Files to be modified/added  (MANDATORY)
    ...                 | - usertype: if usertype = user then User details in "Users" file AND if usertype = coa then user for generation CoA request (MANDATORY)
    ...
    ...                RETURNS:
    ...                |  ${result}: Returns Returns True if radius user or coa user  has been successfully removed from radius server
    ...                |          : Returns False if there was an error in removing radius server user or coa user from  radius server 
    ...
    ...                EXAMPLE USAGE:  
    ...                |  e.g.     
    ...                |  To remove radius user config 
    ...                |  remove user config from radius server    ${tv['h0__if0__mgt-ip']}    ${tv['uv-radius-username']}    ${tv['uv-radius-password']}    ${user1}     ${tv['uv-radius-filepath']}/users    user    1
    ...                |
    ...                |  To remove coa user config
    ...                |  remove user config from radius server      ${tv['h0__if0__mgt-ip']}    ${tv['uv-radius-username']}    ${tv['uv-radius-password']}   ${user0}    ${tv['uv-radius-filepath']}    coa   6

    [Arguments]         ${hostip}   ${username}   ${password}   ${radius_user}   ${filepath}   ${usertype}   ${attribute_num}
    [Return]            True or False
    
    ${result}   remove radius server user   ${hostip}   ${username}   ${password}   ${radius_user}   ${filepath}   ${usertype}   ${attribute_num}
    Should be True   ${result}

remove client from radius server
    [Documentation]    
    ...                PURPOSE:
    ...                Remove user client config from radius server clients.conf profile
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - filepath: Path of Files to be modified/added (MANDATORY)
    ...                 | - clientip: Radius client IP address ((MANDATORY))
    ...
    ...                RETURNS:
    ...                 |  ${result}:Returns True if radius client has been successfully removed from radius server
    ...                 |          : Returns False if there was an error in removing radius client config from radius server 
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |   remove client from radius server    ${tv['h0__if0__mgt-ip']}    ${tv['uv-radius-username']}    ${tv['uv-radius-password']}    ${tv['uv-radius-filepath']}/clients.conf    ${tv['r0__re0__mgt-ip']}

  
    [Arguments]         ${hostip}   ${username}   ${password}   ${filepath}   ${clientip}
    [Return]            True or False
   
    ${result}   remove radius server client   ${hostip}   ${username}   ${password}   ${filepath}   ${clientip}
    Should be True   ${result}


radius daemon process
    [Documentation]    
    ...                PURPOSE:
    ...                Start/stopr/restart of the radiusd process on the server
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                           
    ...                ARGUMENTS:
    ...                 | - tag: Radius server resource handle    (MANDATORY)
    ...                 | - stop_start_rad: Input parameter to start, stop or restart radiusd process (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}:Returns True if radiusd process has been started/stopped/restarted
    ...                 |          : Returns False if there was an error in starting/stopping/restarting radiusd process
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |  Radius daemon start/stop process
    ...                 |  radius daemon process  h0   stop
    ...                 |  radius daemon process  h0   start
    
    [Arguments]         ${tag}   ${stop_start_rad}
    [Return]            True or False
  
    ${result}   restart radius server   ${tag}   ${stop_start_rad}
    Should be True      ${result}



capture dot1x packets
    [Documentation]    
    ...                PURPOSE:
    ...                Capture radius authentication/accounting debugs based on client MAC and put it into a file.
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - tag: Radius server resource handle (MANDATORY)
    ...                 | - supplicant_name: supplicant user name (MANDATORY)
    ...                 | - capture_action: Input parameter to start, stop dot1x packet capture on the radius server (MANDATORY)
    ...                 | - radius_logpath: Radius Logs File Path (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if it is able to capture packets for a given MAC address
    ...                 |           : Returns False if it is unable to capture packets for a given MAC address
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |  capture dot1x packets     h0    00:11:22:33:44:55   start   /var/log/mschap.log  
    ...
    
    [Arguments]         ${tag}   ${supplicant_name}   ${capture_action}   ${radius_logpath}
    [Return]            True or False
 
    ${result}   packet capture radius   ${tag}   ${supplicant_name}   ${capture_action}   ${radius_logpath}
    Should be True    ${result}

send radius coa or disconnect
    [Documentation]    
    ...                PURPOSE:
    ...                Generate/Verify coa/disconnect from radius server to DUT
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address  (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - nasip: IP Address of Network Device/Switch (MANDATORY)
    ...                 | - secret: Secret key configured between Radius and NAS to communicate (MANDATORY)
    ...                 | - radiustype: if type = user then User details in "Users" file AND if type = coa then user for generation CoA request (MANDATORY)
    ...                 | - filepath: Path of Files to be modified/added (MANDATORY)
    ...                 | - attr_list:  CoA attribute list expected in CoA response output (MANDATORY)
    ...                 | - prot : Used to indicate protocol (ipv4/ipv6)
    ...                 | - nak: value 0 or 1 - 0 means verification without NAK and 1 means Verification with NA
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if radius CoA has been sent with all required attributes
    ...                 |           : Returns False if radius CoA has not been sent or not sent with the required attributes.
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |  send radius coa or disconnect  h0   ${tv['h0__if0__mgt-ip']}   ${tv['uv-radius-username']}    ${tv['uv-radius-password']}   ${tv['r0__re0__mgt-ip']}   ${tv['uv-radius-secret']}   coa   ${tv['uv-radius-filepath']}   ${attr_list}   ipv4    no   



    [Arguments]         ${tag}   ${hostip}   ${username}   ${password}   ${nasip}   ${secret}   ${radiustype}   ${filepath}   ${attr_list}   ${prot}   ${nak}
    [Return]            True or False

    ${result}   send coa dm   ${tag}   ${hostip}   ${username}   ${password}   ${nasip}   ${secret}   ${radiustype}   ${filepath}   ${attr_list}   ${prot}   ${nak}
    Should be True    ${result}



configure ethernet ipaddress
    [Documentation]    
    ...                PURPOSE:
    ...                Configure IPv4/IPv6 Address on Host/Radius Server
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - tag: Radius server/Host handle   (MANDATORY)
    ...                 | - ethernet: ethernet interface name  eg : eth1/ens34 (MANDATORY)
    ...                 | - addrtype: IPv4 or IPV6 (MANDATORY)
    ...                 | - ipaddr: IP Address to be  modified/added (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if ethernet address has been configured
    ...                 |           : Returns False if ethernet address has not been configured or there was an error
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |  configure ethernet ipaddress  h0   eth1  ipv4  192.168.20.1
    ...

    [Arguments]         ${tag}   ${ethernet}   ${addrtype}   ${ipaddr}
    [Return]            True or False
   
    ${result}   config eth ipaddr   ${tag}   ${ethernet}   ${addrtype}   ${ipaddr}
    Should be True      ${result}


get station ids
    [Documentation]    
    ...                PURPOSE:
    ...                Getting Station ID's like Calling/Called/Accounting from Host/Radius Server
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address  (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - value: Input parameter to fetch value of which ID e.g : called, calling or acct (MANDATORY)
    ...                 | - radius_logpath: Radius Logs File Path (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if Output successfully returns calling/called/accounting station ID's from  Radius Server
    ...                 |           : Returns False if station ID's cannot be retrieved from  radius server
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |  get station ids     ${tv['h0__if0__mgt-ip']}   ${tv['uv-radius-username']}    ${tv['uv-radius-password']}   called /var/log/mschap.log


    [Arguments]         ${hostip}   ${username}   ${password}   ${value}   ${radius_logpath}
    [Return]            True or False
 
    ${result}   get st id   ${hostip}   ${username}   ${password}   ${value}   ${radius_logpath}
    Should be True      ${result}


Restart Service
    [Documentation]    
    ...                PURPOSE:
    ...                Restarting Any Services on Host/Radius Server
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - tag: Radius server/Host handle (MANDATORY)
    ...                 | - servicename: Radius/Host server service name to restart (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if the given service could be restarted successfully
    ...                 |           : Returns False if there was an error in restarting service or service does not exist
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |  restart service      h0   network
    ...

    [Arguments]         ${tag}   ${servicename}
    [Return]            True or False
 
    ${result}   restart services   ${tag}   ${servicename}
    Should be True      ${result}

authenticate cwauser
    [Documentation]    
    ...                PURPOSE:
    ...                Verify CWA user
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - username_vm: Client username (MANDATORY)
    ...                 | - password_vm: Client VM password (MANDATORY)
    ...                 | - username: CWA user username  (MANDATORY)
    ...                 | - password: CWA user password  (MANDATORY)
    ...                 | - url: Redirect URL (MANDATORY)
    ...                 | - filepath: Path of selenium login script (MANDATORY)
    ...                 | - file_name: selenium login script name (MANDATORY)
    ...                 | - hostip: Client VM IP address  (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if client is authenticated successfully using CoA
    ...                 |           : Returns False if client is not authenticated using CoA
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g. authenticate cwauser       root    Embe1mpls    WEB_AUTH    Cisco123     https://9.9.9.1    /root/switch_connect/    switch_connect3.py      selenuim-vm 
    ...                 |  
    ...

    [Arguments]      ${username_vm}    ${password_vm}   ${username}    ${password}    ${url}      ${filepath}    ${file_name}     ${hostip}
    [Return]            True or False

    ${result}    authentication user   ${username_vm}    ${password_vm}   ${username}    ${password}    ${url}      ${filepath}    ${file_name}     ${hostip}
    Should be true    ${result}


check dot1x protocol messages
    [Documentation]    
    ...                PURPOSE:
    ...                Verify that client is authenticated and verify different dot1x attributes
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A
    ...                             
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - deviceip: IP of the device communicating with radius server (MANDATORY)
    ...                 | - proto_type: Protocol Type based verification (MANDATORY)
    ...                 | - tlv_list: List of TLV fields to be verified  (MANDATORY)
    ...                 | - radius_logpath: Radius Logs File Path  (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if client is authenticated successfully using CoA
    ...                 |           : Returns False if client is not authenticated using CoA
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g. 
    ...                 |  check dot1x protocol messages    ${tv['h0__if0__mgt-ip']}   ${tv['uv-radius-username']}    ${tv['uv-radius-password']}   ${tv['r0__re0__mgt-ip']}   ${tv['uv-radius-secret']}
    ...                 |
    
    [Arguments]         ${hostip}    ${username}    ${password}    ${deviceip}   ${proto_type}    ${tlv_list}   ${accounting_on}   ${radius_logpath}
    [Return]            True or False
 

    ${result}   verify dot1x msgs    ${hostip}     ${username}    ${password}    ${deviceip}   ${proto_type}   ${tlv_list}   ${accounting_on}   ${radius_logpath}
    Should be True      ${result}


generate and verify captive portal
    [Documentation]    
    ...                PURPOSE:
    ...                Generating and Verifying Captive Portal from Host/Radius Server
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A                
    ...
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - clientuser: Client Username  to login into captive portal (MANDATORY)
    ...                 | - clientpasswd: Client User Password to login into captive portal (MANDATORY)
    ...                 | - complete_url: Captive Portal URL to be send, for example: http://1.1.1.1/login.html (MANDATORY)
    ...                 | - attr_value: Attributes to be verified after sending captive portal url, for example: success, failures. (MANDATORY)
    ...
    ...                RETURNS:
    ...                 |  ${result}: Returns True if captive portal client authentication is successful 
    ...                 |           : Returns False if captive portal client authentication is not successful
    ...
    ...                EXAMPLE USAGE:  
    ...                |  e.g.     
    ...                |  Verify successful captive portal client authentication
    ...                |  generate and verify captive portal     h0   ${tv['h0__if0__mgt-ip']}   ${tv['uv-radius-username']}    ${tv['uv-radius-password']}   ${client_user}   ${client_password}   http://1.1.1.1/login.html   success
    ...

    ${result}   send verify cp   ${tag}   ${hostip}   ${username}   ${password}   ${clientuser}   ${clientpasswd}   ${complete_url}   ${attr_value}
    Should be True      ${result}



add captive portal user
    [Documentation]    
    ...                PURPOSE:
    ...                Add captive portal user to radius server
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A     
    ...
    ...                ARGUMENTS:
    ...                 | - hostip: Radius server IP address (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - user_data: Client Username  to login into captive portal (MANDATORY)
    ...                 | - filepath: Captive Portal file path  (MANDATORY)
    ...                 | - filename: Captive Portal File    (MANDATORY)
    ... 
    ...                RETURNS:
    ...                 |  ${result}: Returns True if captive portal client addition in radius server user config file is successful
    ...                 |           : Returns False if captive portal client addition in radius server user config file is not successful
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |  add captive portal user    ${tv['h0__if0__mgt-ip']}    ${tv['uv-radius-username']}    ${tv['uv-radius-password']}    ${user_data0}    ${tv['uv-radius-filepath']}   users
   
    [Arguments]         ${hostip}   ${username}   ${password}   ${user_data}   ${filepath}   ${filename}
    [Return]            True or False
  

    ${result}   add cp user   ${hostip}   ${username}   ${password}   ${user_data}   ${filepath}   ${filename}
    Should be True      ${result}
    
    
check wpa supplicant server
    [Documentation]    
    ...                PURPOSE:
    ...                Check if wpa_supplicant is installed on radius server
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A     
    ...
    ...                ARGUMENTS:
    ...                 | - tag : Radius server handle name (MANDATORY)
    ... 
    ...                RETURNS:
    ...                 |  ${result}: Returns True if wpa_supplicant is installed on radius server
    ...                 |           : Returns False wpa_supplicant is not installed on radius server
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    ...                 |   check wpa supplicant server         h0
   
    [Arguments]         ${tag}
    [Return]            True or False
    
    ${result}   check wpa supplicant    ${tag}
    Should be True      ${result} 
	
verify wpa authenitication 
    [Documentation]    
    ...                PURPOSE:
    ...                Verify if client is authenticated using wpa authentication
    ...
    ...                PLATFORMS vs RELEASE SUPPORT              
    ...                 | -N/A     
    ...
    ...                ARGUMENTS:
    ...                 | - tag : Radius server handle name (MANDATORY)
    ...                 | - hostip: Radius server IP address (MANDATORY)
    ...                 | - username: Radius server login username (MANDATORY)
    ...                 | - password: Radius server login password (MANDATORY)
    ...                 | - radius_user: Radius user name for client authentication
    ...                 | - radius_pwd: Radius user password for client authentication
    ...                 | - filepath_wpa: FilePath for wpa_supplicant.conf file
    ...                 | - eth_interface: Ethernet interface for client authentication  ex: eth1/ens34
    ... 
    ...                RETURNS:
    ...                 |  ${result}: Returns True if client authentication is successful using wpa_supplicant
    ...                 |           : Returns False if client authentication is not successful using wpa_supplicant
    ...
    ...                EXAMPLE USAGE:  
    ...                 |  e.g.     
    
    [Arguments]         ${tag}   ${hostip}   ${username}   ${password}   ${radius_user}    ${radius_pwd}    ${filepath_wpa}     ${eth_interface}
    [Return]            True or False
   
    ${result}   verify wpa supplicant     ${tag}    ${hostip}   ${username}   ${password}   ${radius_user}    ${radius_pwd}    ${filepath_wpa}     ${eth_interface}
    Should be True      ${result}

Verify Accounting
    [Documentation]
    ...                PURPOSE
    ...                |   Verifies attributes in accounting request packet on the radius server/switch 
    ...                |
    ...                PLATFORMS vs RELEASE SUPPORT :
    ...                |   This keyword supports on Junos platforms ex,qfx,mx.
    ...                |
    ...                Arguments:
    ...                | - device: [MANDATORY]
    ...                |   resource name
    ...                |
    ...                | - filename: [MANDATORY]
    ...                |   Filename for accounting info
    ...                |
    ...                | - ip: [MANDATORY]
    ...                |   Host IP Address 
    ...                |      
    ...                | - request_type: [MANDATORY]
    ...                |   request type === Access request/Accounting request /Access Accept 
    ...                |
    ...                | -attribute: [OPTIONAL]
    ...                |     attribute to be verified 
    ...                |
    ...                | -value: [OPTIONAL]
    ...                |     value to be verified against the attribute
    ...                |
    ...                | -interval: [OPTIONAL]
    ...                |     interval for iterating the show output if check fails
    ...                |
    ...                | -timeout: [OPTIONAL]
    ...                |     Max time after which the check will stop retrying
    
    
    ...                Returns:
    ...                | -  Attrubite value 
    ...
    ...                EXAMPLE USAGE:
    ...                |  e.g.
    ...                |  ${acc_status} =  Verify Accounting         filename=${TEXT_FILE}_tc5   ip=10.20.254.19  request_type=Accounting-Request   attribute=${attribute_list[${i}]}   value=${value_list[${i}]}  



    [Arguments]     ${filename}  ${ip}  ${request_type}  ${attribute}  ${value}   
    ${status} =    accounting keyword
    ...               filename=${filename}
    ...               ip=${ip}
    ...               request_type=${request_type}
    ...               attribute=${attribute}
    ...               value=${value}

    [return]      ${status}
    
UserFileBackup
    [Documentation]    
    ...                PURPOSE:
    ...                Creating backup of users file for raddb directory
    [Arguments]     ${tag}  ${hostip}  ${username}  ${password}  ${filepath}  ${option}
    [Return]        True or False
    
    ${status}       userfilebackup_keyword    tag=${tag}    hostip=${hostip}   username=${username}    password=${password}    filepath=${filepath}     option=${option}
    Should be True      ${status}    
