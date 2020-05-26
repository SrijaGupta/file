*** Settings ***
Documentation    
...              UserFW keywords in SRX device
...              This resource file is collection of all resource files defined
...              in UserFW SRX device
...            
...              Author: Wentao Wu (wtwu@juniper.net)
...
...              Keywords List:
#...                     Config SRX UserFW Webapi
...                     Config SRX UserFW Active Directory Access
...                     Config SRX UserFW Aruba Clearpass
...                     Config SRX UserFW Aruba Clearpass Traceoptions
...                     Config SRX UserFW Identity Management
...                     Config SRX UserFW Identity Management Traceoptions
...                     Config SRX UserFW Identity Management Filter
#...                     Show SRX UserFW Auth Table All
...                     Show SRX UserFW Device-information Table All
...                     Clear SRX UserFW Auth Table All
...                     Clear SRX UserFW Identity Management Counter
...                     Check SRX UserFW Identity Management Status
...                     Check SRX UserFW Identity Management Counter
...                     Check SRX UserFW Auth Table With IP
...                     Check SRX UserFW Auth Table Not Match With IP
...                     Check SRX UserFW Auth Table Agetime With IP
...                     Check SRX UserFW Auth Table Group With IP
...                     Check SRX UserFW Auth Table Referenced Group With IP
...                     Check SRX UserFW Aruba ClearPass Status
#...                     Check SRX UserFW No User Auth Entry
...                     Check SRX UserFW No Device Auth Entry
...                     Check SRX UserFW No User Auth Entry With IP
...                     Check SRX UserFW No Device Auth Entry With IP
...                     Check SRX UserFW No User Auth Entry With Domain
...                     Check SRX UserFW Identity Management Trace Query Count
...                     Check SRX UserFW Firewall Auth JIMS Counter
...                     Check SRX UserFW Active Directory Domain-controller Status
...                     Config SRX UserFW Device End User Profile
...                     Delete SRX UserFW Device End User Profile
...                     Deactive SRX UserFW User Identification
...                     Active SRX UserFW User Identification
...                     Disable SRX UserID Daemon
...                     Enable SRX UserID Daemon
...                     Delete SRX UserFW
...                     Delete SRX UserFW Aruba Clearpass
#...                     Delete SRX UserFW Webapi
...                     Delete SRX UserFW Active Directory
...                     Delete SRX UserFW Identity Management
...                     Delete SRX UserFW Identity Management Filter
...                     Check SRX UserFW Active-directory-access Statistics Ip-user-probe
...                     Clear SRX UserFW Active-directory-access Statistics Ip-user-probe
...                     Add SRX Userfw Local Auth Entry Without Role
...                     Add SRX Userfw Local Auth Entry With Role
...                     Delete SRX Userfw Local Auth Entry
...                     Check SRX UserFW Local Auth Table With IP
...                     Check SRX UserFW Local Auth Table With IP On PFE
...                     Get SRX UserFW Policy User-id On PFE
...                     Check SRX UserFW AD Table With IP On PFE
...                     Get SRX UserFW Profile ID
...                     Check SRX UserFW Ipid-client With IP On PFE
...                     Config SRX Authentication-source Priority
...                     Delete SRX Authentication-source Priority
...                     Check SRX UserFW Device Table With IP


*** Keywords ***
#Config SRX UserFW Webapi
#    [Documentation]    Add UserFW webapi configuration in srx
#    [Arguments]    ${device}=${srx0}
#    ...            ${ip}=${None}
#    ...            ${user}=${None}
#    ...            ${password}=${None}
#    ...            ${http_port}=${None}
#    ...            ${https_port}=${None}
#    
#    ${cmd_list} =    Create List    ${EMPTY}
#    Run Keyword If    "${ip}" is not "${None}"               Append To List    ${cmd_list}    set system services webapi client ${ip}
#    Run Keyword If    "${user}" is not "${None}"             Append To List    ${cmd_list}    set system services webapi user ${user} 
#    Run Keyword If    "${password}" is not "${None}"         Append To List    ${cmd_list}    set system services webapi user password ${password} 
#    Run Keyword If    "${http_port}" is not "${None}"        Append To List    ${cmd_list}    set system services webapi http port ${http_port} 
#    Run Keyword If    "${https_port}" is not "${None}"       Append To List    ${cmd_list}    set system services webapi https port ${https_port} 
#    ...                                                                                       set system services webapi https default-certificate
#    Execute Config Command On Device    ${device}    command_list=${cmd_list} 

Config SRX UserFW Active Directory Access
    [Documentation]    Add UserFW active-directory-access configuration in srx
    [Arguments]    ${device}=${srx0}
    ...            ${domain}=ad03.net
    ...            ${user}=${None}
    ...            ${password}=${None}
    ...            ${dc_name}=mydc1
    ...            ${dc_address}=${None}
    ...            ${ldap_base}=${None}
    ...            ${ldap_address}=${None}
    ...            ${ldap_user}=${None}
    ...            ${ldap_password}=${None}
    ...            ${ldap_ssl}=${None}
    ...            ${authentication_algorithm}=${None}
    ...            ${scanning_interval}=${None}
    ...            ${initial_timespan}=${None}
    ...            ${entry_timeout}=${None}
    ...            ${wmi_timeout}=${None}
    ...            ${invalid_timeout}=${None}
    ...            ${force_timeout}=${None}
    ...            ${no_on_demand_probe}=${None} 
    ...            ${filter}=${None}           # include | exclude
    ...            ${filter_address}=1.2.3.4/24
    
    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${user}" is not "${None}"               Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user ${user} 
    Run Keyword If    "${password}" is not "${None}"           Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user password ${password} 
    Run Keyword If    "${dc_address}" is not "${None}"         Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} domain-controller ${dc_name} address ${dc_address} 
    Run Keyword If    "${ldap_base}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user-group-mapping ldap base ${ldap_base} 
    Run Keyword If    "${ldap_address}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user-group-mapping ldap address ${ldap_address} 
    Run Keyword If    "${ldap_user}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user-group-mapping ldap user ${ldap_user} 
    Run Keyword If    "${ldap_password}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user-group-mapping ldap user password ${ldap_password} 
    Run Keyword If    "${ldap_ssl}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user-group-mapping ldap ssl 
    Run Keyword If    "${authentication_algorithm}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} user-group-mapping ldap authentication-algorithm simple 
    Run Keyword If    "${scanning_interval}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} ip-user-mapping discovery-method wmi event-log-scanning-interval ${scanning_interval} 
    Run Keyword If    "${initial_timespan}" is not "${None}"          Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access domain ${domain} ip-user-mapping discovery-method wmi initial-event-log-timespan ${initial_timespan} 
    Run Keyword If    "${entry_timeout}" is not "${None}"      Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access authentication-entry-timeout ${entry_timeout}
    Run Keyword If    "${wmi_timeout}" is not "${None}"        Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access wmi-timeout ${wmi_timeout}
    Run Keyword If    "${invalid_timeout}" is not "${None}"    Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access invalid-authentication-entry-timeout ${invalid_timeout}
    Run Keyword If    "${force_timeout}" is not "${None}"     Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access firewall-authentication-forced-timeout ${force_timeout}
    Run Keyword If    "${no_on_demand_probe}" is not "${None}"      Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access no-on-demand-probe
    Run Keyword If    "${filter}" is not "${None}"            Append To List    ${cmd_list}
    ...               set services user-identification active-directory-access filter ${filter} ${filter_address} 
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
	

Config SRX UserFW Aruba Clearpass
    [Documentation]    Add UserFW aruba-clearpass configuration in srx
    [Arguments]    ${device}=${srx0}
    ...            ${name}=${None}
    ...            ${address}=${None}
    ...            ${port}=${None}
    ...            ${connect_method}=${None}
    ...            ${client_id}=${None}
    ...            ${client_secret}=${None}
    ...            ${token_api}=${None}
    ...            ${query_api}=${None}
    ...            ${ca_certificate}=${None}
    ...            ${entry_timeout}=${None}
    ...            ${delay_query_timeout}=${None}
    ...            ${invalid_timeout}=${None}

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${name}" is not "${None}"               Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query web-server ${name}
    Run Keyword If    "${address}" is not "${None}"            Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query web-server address ${address}
    Run Keyword If    "${port}" is not "${None}"               Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query web-server port ${port}
    Run Keyword If    "${connect_method}" is not "${None}"     Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query web-server connect-method ${connect_method}
    Run Keyword If    "${client_id}" is not "${None}"          Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query client-id ${client_id}
    Run Keyword If    "${client_secret}" is not "${None}"      Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query client-secret ${client_secret}
    Run Keyword If    "${token_api}" is not "${None}"           Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query token-api ${token_api}
    Run Keyword If    "${query_api}" is not "${None}"           Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query query-api ${query_api}
    Run Keyword If    "${ca_certificate}" is not "${None}"      Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query ca-certificate ${ca_certificate}
    Run Keyword If    "${entry_timeout}" is not "${None}"      Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass authentication-entry-timeout ${entry_timeout}
    Run Keyword If    "${delay_query_timeout}" is not "${None}"    Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass user-query delay-query-time ${delay_query_timeout}
    Run Keyword If    "${invalid_timeout}" is not "${None}"      Append To List    ${cmd_list}     set services user-identification authentication-source aruba-clearpass invalid-authentication-entry-timeout ${invalid_timeout}
    Execute Config Command On Device    ${device}    command_list=${cmd_list} 

Config SRX UserFW Aruba Clearpass Traceoptions
    [Documentation]    Add UserFW aruba-clearpass traceoptions configuration in srx
    [Arguments]    ${device}=${srx0}
    ...            ${file}=cp_log
    
    ${cmd_list} =    Create List
    ...               set services user-identification authentication-source aruba-clearpass traceoptions file ${file}
    ...               set services user-identification authentication-source aruba-clearpass traceoptions file size 100m
    ...               set services user-identification authentication-source aruba-clearpass traceoptions flag all
    ...               set services user-identification authentication-source aruba-clearpass traceoptions level all
    Execute Config Command On Device    ${device}    command_list=${cmd_list}  
    #clear log
    Execute Cli Command On Device    ${device}    command=clear log ${file}

Config SRX UserFW Identity Management
    [Documentation]    Add UserFW identity-management configuration in srx
    [Arguments]    ${device}=${srx0}
    ...            ${port}=${None}
    ...            ${protocol}=${None}
    ...            ${primary_ip}=${None}
    ...            ${primary_user}=otest
    ...            ${primary_password}=test
    ...            ${primary_ca}=${None}
    ...            ${secondary_ip}=${None}
    ...            ${secondary_user}=otest
    ...            ${secondary_password}=test
    ...            ${secondary_ca}=${None}
    ...            ${query_api}=${None}
    ...            ${token_api}=${None}
    ...            ${entry_timeout}=${None}
    ...            ${invalid_timeout}=${None}
    ...            ${query_delay_time}=${None}
    ...            ${no_ip_query}=${None}
    ...            ${items_per_batch}=${None}
    ...            ${query_interval}=${None}
    ...            ${logical_systems}=${None}
    ...            ${reserved}=${None}
    ...            ${max}=${None}
 
    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    set logical-systems ${logical_systems} services user-identification identity-management
    ...         ELSE                                            Set Variable    set services user-identification identity-management
    Log    ==> prefix is: ${prefix}  
        
    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword IF    "${port}" is not "${None}"                    Append To List    ${cmd_list}    ${prefix} connection port ${port}
    Run Keyword IF    "${protocol}" is not "${None}"                Append To List    ${cmd_list}    ${prefix} connection connect-method ${protocol}
    Run Keyword IF    "${primary_ip}" is not "${None}"              Append To List    ${cmd_list}
    ...               ${prefix} connection primary address ${primary_ip}
    ...               ${prefix} connection primary client-id ${primary_user}
    ...               ${prefix} connection primary client-secret ${primary_password}
    Run Keyword If    "${secondary_ip}" is not "${None}"         Append To List    ${cmd_list}    
    ...               ${prefix} connection secondary address ${secondary_ip}
    ...               ${prefix} connection secondary client-id ${secondary_user}
    ...               ${prefix} connection secondary client-secret ${secondary_password}
    Run Keyword If    "${primary_ca}" is not "${None}"           Append To List    ${cmd_list}    ${prefix} connection connection primary ca-certificate ${primary_ca}
    Run Keyword If    "${secondary_ca}" is not "${None}"         Append To List    ${cmd_list}    ${prefix} connection connection secondary ca-certificate ${secondary_ca}
    Run Keyword If    "${token_api}" is not "${None}"            Append To List    ${cmd_list}    ${prefix} connection token-api ${token_api}
    Run Keyword If    "${query_api}" is not "${None}"            Append To List    ${cmd_list}    ${prefix} connection query-api ${query_api}
    Run Keyword If    "${entry_timeout}" is not "${None}"        Append To List    ${cmd_list}    ${prefix} authentication-entry-timeout ${entry_timeout}
    Run Keyword If    "${invalid_timeout}" is not "${None}"      Append To List    ${cmd_list}    ${prefix} invalid-authentication-entry-timeout ${invalid_timeout}
    Run Keyword If    "${query_delay_time}" is not "${None}"     Append To List    ${cmd_list}    ${prefix} ip-query query-delay-time ${query_delay_time}
    Run Keyword If    "${no_ip_query}" is not "${None}"          Append To List    ${cmd_list}    ${prefix} ip-query no-ip-query
    Run Keyword If    "${items_per_batch}" is not "${None}"      Append To List    ${cmd_list}    ${prefix} batch-query items-per-batch ${items_per_batch}
    Run Keyword If    "${query_interval}" is not "${None}"       Append To List    ${cmd_list}    ${prefix} batch-query query-interval ${query_interval}

    #the command "set services user-identification identity-management logic-domain xxxx" can't use ${prefix}, because they can only configure by "set services", can't configure by "set logical-systems"
    Run Keyword If    "${logical_systems}" is not "${None}" and ${reserved} is not "${None}"    Append To List    ${cmd_list}
    ...               set services user-identification identity-management logic-domain ${logical_systems} authentication-entry-capacity reserved ${reserved}
    Run Keyword If    "${logical_systems}" is not "${None}" and ${max} is not "${None}"    Append To List    ${cmd_list}
    ...               set services user-identification identity-management logic-domain ${logical_systems} authentication-entry-capacity max ${max}
    
    Execute Config Command On Device    ${device}    command_list=${cmd_list} 

Config SRX UserFW Identity Management Traceoptions
    [Documentation]    Add UserFW identity-management traceoptions configuration in srx
    [Arguments]    ${device}=${srx0}
    ...            ${file}=jims_log
    
    ${cmd_list} =    Create List
    ...               set services user-identification identity-management traceoptions file ${file}
    ...               set services user-identification identity-management traceoptions file size 100m
    ...               set services user-identification identity-management traceoptions flag all
    ...               set services user-identification identity-management traceoptions level all
    Execute Config Command On Device    ${device}    command_list=${cmd_list}  

Config SRX UserFW Identity Management Filter
    [Documentation]    Add UserFW identity-management filter configuration in srx
    ...                filter=domain|include|exclude
    [Arguments]    ${device}=${srx0}
    ...            ${filter}=include    # domain | include | exclude
    ...            ${domain}=${None}
    ...            ${address_book}=${None}
    ...            ${address_set}=${None}
    ...            ${logical_systems}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    set logical-systems ${logical_systems} services user-identification identity-management
    ...         ELSE                                            Set Variable    set services user-identification identity-management
    Log    ==> prefix is: ${prefix}
    
    ${cmd_list} =      Create List    ${EMPTY}
    Run Keyword If    "${filter}" == "domain"        Append To List    ${cmd_list}    ${prefix} filter domain ${domain}
    ...    ELSE IF    "${filter}" == "include"       Append To List    ${cmd_list}    ${prefix} filter include-ip address-book ${address_book} address-set ${address_set}
    ...    ELSE IF    "${filter}" == "exclude"       Append To List    ${cmd_list}    ${prefix} filter exclude-ip address-book ${address_book} address-set ${address_set}
    ...       ELSE                                   Append To List    ${cmd_list}    ${EMPTY}
    Execute Config Command On Device    ${device}    command_list=${cmd_list} 
	
Config SRX UserFW Device Authentication Source
    [Documentation]    Config SRX UserFW Device Authentication Source
    [Arguments]    ${device}=${srx0}
    ...            ${source}=network-access-controller

    ${cmd_list} =    Create List
    ...               set services user-identification device-information authentication-source ${source}
    Execute Config Command On Device    ${device}    command_list=${cmd_list} 
	
Config SRX UserFW Device End User Profile
    [Documentation]    Config SRX UserFW Device End User Profile
    [Arguments]    ${device}=${srx0}
    ...            ${profile}=${None}
    ...            ${domain}=${None}
    ...            ${attribute}=device-identity
    ...            ${value}=${None}

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${domain}" is not "${None}"       Append To List    ${cmd_list}    set services user-identification device-information end-user-profile profile-name ${profile} domain-name ${domain} 
    Run Keyword If    "${value}" is not "${None}"        Append To List    ${cmd_list}    set services user-identification device-information end-user-profile profile-name ${profile} attribute ${attribute} string ${value}
    Execute Config Command On Device    ${device}    command_list=${cmd_list} 
	
Delete SRX UserFW Device End User Profile
    [Documentation]    Delete SRX UserFW Device End User Profile
    [Arguments]    ${device}=${srx0}
    ...            ${profile}=${None}
    ...            ${domain}=${None}
    ...            ${attribute}=${None}
    ...            ${value}=${None}

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${value}" is not "${None}"                  Append To List    ${cmd_list}    delete services user-identification device-information end-user-profile profile-name ${profile} attribute ${attribute} string ${value} 
    ...    ELSE IF    "${attribute}" is not "${None}"              Append To List    ${cmd_list}    delete services user-identification device-information end-user-profile profile-name ${profile} attribute ${attribute}
    ...    ELSE IF    "${domain}" is not "${None}"                 Append To List    ${cmd_list}    delete services user-identification device-information end-user-profile profile-name ${profile} domain-name ${domain}
    ...    ELSE IF    "${profile}" is not "${None}"                Append To List    ${cmd_list}    delete services user-identification device-information end-user-profile profile-name ${profile}
    ...       ELSE                                                 Append To List    ${cmd_list}    delete services user-identification device-information end-user-profile
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
	
#passed  wtwu
#Show SRX UserFW Auth Table All
#    [Documentation]    Show SRX UserFW Auth Table All
#    [Arguments]    ${device}=${srx0}
#    ...            ${node}=${None}
#   
#    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=show services user-identification authentication-table authentication-source all node ${node}
#    ...       ELSE                                  Execute cli command on device    ${device}    command=show services user-identification authentication-table authentication-source all

Show SRX UserFW Device-information Table All
    [Documentation]    Show SRX UserFW Device-information Table All
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
   
    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=show services user-identification device-information table all node ${node}
    ...       ELSE                                  Execute cli command on device    ${device}    command=show services user-identification device-information table all
	
Check SRX UserFW Active-directory-access Statistics Ip-user-probe
    [Documentation]    Check SRX UserFW Active-directory-access Statistics Ip-user-probe
    [Arguments]    ${device}=${srx0}
    ...            ${domain}=test
    ...            ${total_number}=1
    ...            ${failed_number}=1
	
    :FOR    ${index}    IN RANGE    4
    \    sleep    20
    \    ${result}    Execute cli command on device    ${device}    command=show services user-identification active-directory-access statistics ip-user-probe
    \    Run Keyword If    '${domain}' in '''${result}'''    Exit For Loop   
    \     ...    ELSE    Continue For Loop	
	
    ${match_result}    ${get_total_number}    ${get_failed_number}
    ...          Should Match Regexp      ${result}    (?is)Total user probe number\\s*:\\s*(\\d*).*?Failed user probe number\\s*:\\s*(\\d*)
	
    Log    ${get_total_number}
    Log    ${get_failed_number}
	
    Run Keyword If    ${total_number} >= ${get_total_number} > 0    Log    Total user probe number is expected value
    ...    ELSE IF    ${total_number}==0 and ${get_total_number}==0    Log    Total user probe number is 0, this's expected value
    ...    ELSE    Fail    Total user probe number isn't expected value
	
    Run Keyword If    ${failed_number} >= ${get_failed_number} > 0   Log    Failed user probe number is expected value
    ...    ELSE IF    ${failed_number}==0 and ${get_failed_number}==0    Log    Failed user probe number is 0, this's expected value
    ...    ELSE    Fail    Failed user probe number isn't expected value
	
Check SRX UserFW Auth Table Agetime With IP
    [Documentation]    Check SRX UserFW Auth Table Agetime With IP
    [Arguments]    ${device}=${srx0}
    ...            ${domain_name}=test.com
    ...            ${ip}=1
    ...            ${user_name}=${None}
    ...            ${group_name}=${None}
    ...            ${state}=Valid
    ...            ${source}=wmic
    ...            ${agetime}=0
    ...            ${node}=${None}
    ...            ${logical_system}=${None}
    ...            ${ref_group_name}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification authentication-table ip-address ${ip} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show services user-identification authentication-table ip-address ${ip}
    Log    ==> prefix is: ${prefix}
	
    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node}
    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix}
	
    Run Keyword If    '${domain_name}' in '''${result}'''    Log    domain name is expected value
    ...    ELSE    Fail    domain name isn't expected value
	
    Run Keyword If    "${user_name}" is not "${None}"             Should Match Regexp    ${result}   (?is)Username:\\s*${user_name}
    Run Keyword If    "${group_name}" is not "${None}"            Should Match Regexp    ${result}   (?is)Groups:\\s*${group_name}
    Run Keyword If    "${ref_group_name}" is not "${None}"            Should Match Regexp    ${result}   (?is)Groups referenced by policy:\\s*${ref_group_name}
	
    Run Keyword If    '${state}' in '''${result}'''    Log    state is expected value
    ...    ELSE    Fail    state isn't expected value
	
    Run Keyword If    '${source}' in '''${result}'''    Log    source is expected value
    ...    ELSE    Fail    source isn't expected value
	
    ${match_result}    ${get_agetime}
    ...          Should Match Regexp      ${result}    (?is)Age time:\\s*(\\w*)
	
    Log    ${get_agetime}
	
    Run Keyword If    '${get_agetime}'=='infinite' and '${agetime}'=='infinite'    Log    agetime is infinite, this's expected value
    ...    ELSE IF    ${get_agetime}==0 and ${agetime}==0    Log    agetime is 0, this's expected value
    ...    ELSE IF    "${agetime}" is not "infinite" and "${agetime}" is not "0" and ${agetime} -3 <= ${get_agetime} <= ${agetime} + 3     Log    agetime is expected value
    ...    ELSE    Fail    agetime isn't expected value	

Clear SRX UserFW Auth Table All
    [Documentation]    Clear UserFW auth table all in srx
    [Arguments]    ${device}=${srx0}
    ...            ${authentication_source}=all    #[active-directory | aruba-clearpass | identity-management |all]
    
    Execute cli command on device    ${device}    command=clear services user-identification authentication-table authentication-source ${authentication_source}
    sleep    3
    #Check result
    Execute cli command on device    ${device}    command=show services user-identification authentication-table authentication-source ${authentication_source}
	
Clear SRX UserFW Active-directory-access Statistics Ip-user-probe
    [Documentation]    Clear SRX UserFW Active-directory-access Statistics Ip-user-probe
    [Arguments]    ${device}=${srx0}
    
    Execute cli command on device    ${device}    command=clear services user-identification active-directory-access statistics ip-user-probe
    sleep    1
    #Check result
    Execute cli command on device    ${device}    command=show services user-identification active-directory-access statistics ip-user-probe

Clear SRX UserFW Identity Management Counter
    [Documentation]    Clear UserFW identity-management counter in srx
    [Arguments]    ${device}=${srx0}
    ...            ${logical_systems}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    clear logical-systems ${logical_systems} services
    ...         ELSE                                            Set Variable    clear services
    Log    ==> prefix is: ${prefix}
    
    Execute cli command on device    ${device}    command=${prefix} user-identification identity-management counters

Check SRX UserFW Identity Management Status
    [Documentation]    Check SRX UserFW Identity Management Status
    [Arguments]   ${device}=${srx0}
    ...           ${primary_address}=${None}
    ...           ${primary_port}=${None}
    ...           ${primary_protocol}=${None}
    ...           ${primary_status}=${None}    # Online | Offline
    ...           ${primary_message}=${None}   # OK     | Error
    ...           ${primary_token}=${None}     # NULL   | any
    ...           ${primary_expire}=${None}
    ...           ${secondary_address}=${None}
    ...           ${secondary_port}=${None}
    ...           ${secondary_protocol}=${None}
    ...           ${secondary_status}=${None}    # Online | Offline
    ...           ${secondary_message}=${None}   # OK     | Error
    ...           ${secondary_token}=${None}     # NULL   | any
    ...           ${logical_systems}=${None}

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    show logical-systems ${logical_systems} services
    ...         ELSE                                            Set Variable    show services
    Log    ==> prefix is: ${prefix}    
    
    ${result}    Execute cli command on device    ${device}    command=${prefix} user-identification identity-management status |display xml
    Run Keyword If    "${primary_address}" is not "${None}"       Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<server-address>${primary_address}.*?<server-type>Secondary 
    Run Keyword If    "${primary_port}" is not "${None}"          Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<server-port>${primary_port}.*?<server-type>Secondary 
    Run Keyword If    "${primary_protocol}" is not "${None}"      Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<connect-method>${primary_protocl}.*?<server-type>Secondary 
    Run Keyword If    "${primary_status}" is not "${None}"        Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<connect-status>${primary_status}.*?<server-type>Secondary 
    Run Keyword If    "${primary_message}" is not "${None}"       Should Match Regexp    ${result}   (?is)Primary</server-type>.*?\\(${primary_message}\\)</recv-status-msg>.*?<server-type>Secondary 
    Run Keyword If    "${primary_token}" is "NULL"                Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<token-string>NULL.*?<server-type>Secondary 
    ...       ELSE                                            Should Not Match Regexp    ${result}   (?is)Primary</server-type>.*?<token-string>NULL.*?<server-type>Secondary 
    Run Keyword If    "${secondary_address}" is not "${None}"     Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<server-address>${secondary_address}.*?</jims-query-status> 
    Run Keyword If    "${secondary_port}" is not "${None}"        Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<server-port>${secondary_port}.*?</jims-query-status>
    Run Keyword If    "${secondary_protocol}" is not "${None}"    Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<connect-method>${secondary_protocl}.*?</jims-query-status>
    Run Keyword If    "${secondary_status}" is not "${None}"      Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<connect-status>${secondary_status}.*?</jims-query-status>
    Run Keyword If    "${secondary_message}" is not "${None}"     Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?\\(${secondary_message}\\)</recv-status-msg>.*?</jims-query-status>
    Run Keyword If    "${secondary_token}" is "NULL"              Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<token-string>NULL.*?</jims-query-status>
    ...       ELSE                                            Should Not Match Regexp    ${result}   (?is)Secondary</server-type>.*?<token-string>NULL.*?</jims-query-status> 

Check SRX UserFW Identity Management Counter
    [Documentation]    Check SRX UserFW Identity Management Status
    [Arguments]   ${device}=${srx0}
    ...           ${primary_address}=${None}
    ...           ${primary_batch_query_sent}=${None}
    ...           ${primary_batch_query_response}=${None}
    ...           ${primary_batch_query_error}=${None}
    ...           ${primary_ip_query_sent}=${None}
    ...           ${primary_ip_query_response}=${None}
    ...           ${primary_ip_query_error}=${None}
    ...           ${secondary_address}=${None}
    ...           ${secondary_batch_query_sent}=${None}
    ...           ${secondary_batch_query_response}=${None}
    ...           ${secondary_batch_query_error}=${None}
    ...           ${secondary_ip_query_sent}=${None}
    ...           ${secondary_ip_query_response}=${None}
    ...           ${secondary_ip_query_error}=${None}
    ${result}    Execute cli command on device    ${device}    command=show services user-identification identity-management counter |display xml
    Run Keyword If    "${primary_address}" is not "${None}"                   Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<server-address>${primary_address}.*?<server-type>Secondary 
    Run Keyword If    "${primary_batch_query_sent}" is not "${None}"          Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<batch-query-sent-number>${primary_batch_query_sent}.*?<server-type>Secondary 
    Run Keyword If    "${primary_batch_query_response}" is not "${None}"      Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<batch-response-recv-number>${primary_batch_query_response}.*?<server-type>Secondary 
    Run Keyword If    "${primary_batch_query_error}" is not "${None}"         Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<batch-error-response-number>${primary_batch_query_error}.*?<server-type>Secondary 
    Run Keyword If    "${primary_ip_query_sent}" is not "${None}"             Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<ip-query-sent-number>${primary_ip_query_sent}.*?<server-type>Secondary 
    Run Keyword If    "${primary_ip_query_response}" is not "${None}"         Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<ip-response-recv-number>${primary_ip_query_response}.*?<server-type>Secondary 
    Run Keyword If    "${primary_ip_query_error}" is not "${None}"            Should Match Regexp    ${result}   (?is)Primary</server-type>.*?<ip-error-response-number>${primary_ip_query_error}.*?<server-type>Secondary 
    Run Keyword If    "${secondary_address}" is not "${None}"                 Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<server-address>${secondary_address}.*?</jims-query-statistics> 
    Run Keyword If    "${secondary_batch_query_sent}" is not "${None}"        Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<batch-query-sent-number>${secondary_batch_query_sent}.*?</jims-query-statistics> 
    Run Keyword If    "${secondary_batch_query_response}" is not "${None}"    Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<batch-response-recv-number>${secondary_batch_query_response}.*?</jims-query-statistics> 
    Run Keyword If    "${secondary_batch_query_error}" is not "${None}"       Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<batch-error-response-number>${secondary_batch_query_error}.*?</jims-query-statistics> 
    Run Keyword If    "${secondary_ip_query_sent}" is not "${None}"           Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<ip-query-sent-number>${secondary_ip_query_sent}.*?</jims-query-statistics> 
    Run Keyword If    "${secondary_ip_query_response}" is not "${None}"       Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<ip-response-recv-number>${secondary_ip_query_response}.*?</jims-query-statistics> 
    Run Keyword If    "${secondary_ip_query_error}" is not "${None}"          Should Match Regexp    ${result}   (?is)Secondary</server-type>.*?<ip-error-response-number>${secondary_ip_query_error}.*?</jims-query-statistics> 
 
Check SRX UserFW Auth Table With IP
    [Documentation]    Check SRX UserFW Auth Table With IP
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.0
    ...           ${domain_name}=${None}
    ...           ${user_name}=${None}
    ...           ${group_name}=${None}
    ...           ${ref_group_name}=${None}
    ...           ${state}=Valid
    ...           ${source}=${None}
    ...           ${node}=${None}
    ...           ${logical_system}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification authentication-table ip-address ${ip} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show services user-identification authentication-table ip-address ${ip}
    Log    ==> prefix is: ${prefix}     

    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node} |display xml
    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix} |display xml
    Run Keyword If    "${domain_name}" is not "${None}"           Should Match Regexp    ${result}   (?is)<ad-auth-table.*?<domain>${domain_name}</domain>.*?<ad-authentication-info> 
    Run Keyword If    "${user_name}" is not "${None}"             Should Match Regexp    ${result}   (?is)</source-ip>.*?<user-name>${user_name}</user-name>.*?<group-name-list>
    Run Keyword If    "${group_name}" is not "${None}"            Should Match Regexp    ${result}   (?is)<group-name-list>.*?<group-name>${group_name}</group-name>.*?</group-name-list>
    Run Keyword If    "${ref_group_name}" is 'N/A'                Should Match Regexp    ${result}   (?is)<ref-group-name-list></ref-group-name-list>
    ...    ELSE IF    "${ref_group_name}" is not "${None}"        Should Match Regexp    ${result}   (?is)<ref-group-name-list>.*?<ref-group-name>${ref_group_name}</ref-group-name>.*?</ref-group-name-list>
    Run Keyword If    "${state}" == "Valid"                       Should Match Regexp    ${result}   (?is)</ref-group-name-list>.*?<state>Valid</state>.*?<src-type>
    ...       ELSE                                                Should Match Regexp    ${result}   (?is)</ref-group-name-list>.*?<state>${state}</state>.*?<src-type>
    Run Keyword If    "${source}" is not "${None}"                Should Match Regexp    ${result}   (?is)</state>.*?<src-type>${source}</src-type>.*?<start-date>

Check SRX UserFW Auth Table Not Match With IP
    [Documentation]    Check SRX UserFW Auth Table With IP
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.0
    ...           ${domain_name}=${None}
    ...           ${user_name}=${None}
    ...           ${group_name}=${None}
    ...           ${ref_group_name}=${None}
    ...           ${state}=${None}
    ...           ${source}=${None}
    ...           ${node}=${None}
    ...           ${logical_system}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification authentication-table ip-address ${ip} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show services user-identification authentication-table ip-address ${ip}
    Log    ==> prefix is: ${prefix}  
    
    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node} |display xml
    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix} |display xml
    Run Keyword If    "${domain_name}" is not "${None}"           Should Not Match Regexp    ${result}   (?is)<ad-auth-table.*?<domain>${domain_name}</domain>.*?<ad-authentication-info> 
    Run Keyword If    "${user_name}" is not "${None}"             Should Not Match Regexp    ${result}   (?is)</source-ip>.*?<user-name>${user_name}</user-name>.*?<group-name-list>
    Run Keyword If    "${group_name}" is not "${None}"            Should Not Match Regexp    ${result}   (?is)<group-name-list>.*?<group-name>${group_name}</group-name>.*?</group-name-list>
    Run Keyword If    "${ref_group_name}" is not "${None}"        Should Not Match Regexp    ${result}   (?is)<ref-group-name-list>.*?<ref-group-name>${ref_group_name}</ref-group-name>.*?</ref-group-name-list>
    Run Keyword If    "${state}" is not "${None}"                 Should Not Match Regexp    ${result}   (?is)</ref-group-name-list>.*?<state>${state}</state>.*?<src-type>
    Run Keyword If    "${source}" is not "${None}"                Should Not Match Regexp    ${result}   (?is)</ref-group-name-list>.*?<state>${source}</state>.*?<src-type>
	
Check SRX UserFW Device Table With IP
    [Documentation]    Check SRX UserFW Device Table With IP
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.0
    ...           ${domain_name}=${None}
    ...           ${device_id}=${None}
    ...           ${device_groups}=${None}
    ...           ${profile}=${None}
    ...           ${node}=${None}
    ...           ${logical_system}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification device-information table ip-address ${ip} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show services user-identification device-information table ip-address ${ip}
    Log    ==> prefix is: ${prefix}
    
    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node} |display xml
    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix} |display xml
    Run Keyword If    "${domain_name}" is not "${None}"           Should Match Regexp    ${result}   (?is)<device-id-table.*?<domain>${domain_name}</domain>.*?<device-info> 
    Run Keyword If    "${device_id}" is 'N/A'                     Should Match Regexp    ${result}   (?is)<device-info.*?<device-name>${device_id}</device-name>.*?<device-group-name-list>
    ...    ELSE IF    "${device_id}" is not "${None}"             Should Match Regexp    ${result}   (?is)<device-info.*?<device-name>${device_id}\\$|${device_id}</device-name>.*?<device-group-name-list>
    Run Keyword If    "${device_groups}" is not "${None}"         Should Match Regexp    ${result}   (?is)<device-group-name-list>.*?<device-group-name>${device_groups}</device-group-name>.*?</device-group-name-list>
    Run Keyword If    "${profile}" is not "${None}"               Should Match Regexp    ${result}   (?is)<ref-profile-list>.*?<ref-profile>${profile}</ref-profile>.*?</ref-profile-list>

Check SRX UserFW Auth Table Group With IP
    [Documentation]    Check SRX UserFW Auth Table Group With IP
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.0
    ...           ${group}=${None}
    ...           ${node}=${None}
    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=show services user-identification authentication-table ip-address ${ip} node ${node}
    ...                      ELSE                                  Execute cli command on device    ${device}    command=show services user-identification authentication-table ip-address ${ip} 
    ${match_result}    ${group_list}
    ...          Should Match Regexp      ${result}    (?is)Groups:(.*)State
    Log    ==> Found group result: ${group_list}
    Log    ==> Need to verify group result: @{group}
    :FOR    ${group_name}     IN    @{group}
    \    Should Contain    ${group_list}    ${group_name}

Check SRX UserFW Auth Table Referenced Group With IP
    [Documentation]    Check SRX UserFW Auth Table Referrenced Group With IP
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.0
    ...           ${referenced_group}=${None}
    ...           ${node}=${None}
    ...           ${logical_system}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification authentication-table ip-address ${ip} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show services user-identification authentication-table ip-address ${ip}
    Log    ==> prefix is: ${prefix}
     
    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node}
    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix}
    ${match_result}    ${group_list}
    ...          Should Match Regexp      ${result}    (?is)Groups\\s+referenced\\s+by\\s+policy:(.*?)State
    Log    ==> Found referenced group result: ${group_list}
    Log    ==> Need to verify group result: @{referenced_group}
    :FOR    ${group}     IN    @{referenced_group}
    \    Should Contain    ${group_list}    ${group}
   
Check SRX UserFW Aruba ClearPass Status
    [Documentation]    Check SRX UserFW Aruba ClearPass Status
    [Arguments]   ${device}=${srx0} 
    ${result}    Execute cli command on device    ${device}    command=show services user-identification authentication-source aruba-clearpass user-query status |display xml
    Should Contain    ${result}    <server-status>Online</server-status> 

Check SRX UserFW Aruba ClearPass Access Token
    [Documentation]    Check SRX UserFW Aruba ClearPass Counter
    [Arguments]   ${device}=${srx0}
    ${result}    Execute cli command on device    ${device}    command=show services user-identification authentication-source aruba-clearpass user-query counter |display xml
    Should Not Contain    ${result}    <access-token>NULL</access-token> 

#Check SRX UserFW No User Auth Entry
#    [Documentation]    check no this IP user auth entry
#    [Arguments]    ${device}=${srx0}
#    ...            ${logical_system}=${None}
#                   
#    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification authentication-table authentication-source all logical-system ${logical_system}
#    ...         ELSE                                            Set Variable    show services user-identification authentication-table authentication-source all
#    Log    ==> prefix is: ${prefix}      
#    
#    ${result}    Execute cli command on device    ${device}    command=${prefix} 
#    Should Match Regexp    ${result}    (There is no authentication-table entry.|user-ad-authentication subsystem has been disabled)

Check SRX UserFW No Device Auth Entry
    [Documentation]    check no this IP device auth entry
    [Arguments]    ${device}=${srx0}
    ${response}    Execute cli command on device    ${device}    command=show services user-identification device-information table all 
    Should Match Regexp    ${response}    (There is no device-identity-table entry.)

Check SRX UserFW No User Auth Entry With IP
    [Documentation]    check no this IP user auth entry
    [Arguments]    ${device}=${srx0}
    ...            ${ip}=1.2.3.4
    ...            ${logical_system}=${None}
                   
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification authentication-table ip-address ${ip} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show services user-identification authentication-table ip-address ${ip}
    Log    ==> prefix is: ${prefix}      

    ${result}    Execute cli command on device    ${device}    command=${prefix} 
    Should Match Regexp    ${result}    (There is no authentication-table entry|This IP address isn't in authentication table)

Check SRX UserFW No Device Auth Entry With IP
    [Documentation]    check no this IP device auth entry
    [Arguments]    ${device}=${srx0}
    ...            ${ip}=1.2.3.4
    ${result}    Execute cli command on device    ${device}    command=show services user-identification device-information table ip-address ${ip} 
    Should Match Regexp    ${result}    (There is no device-identity-table entry|This IP address isn't in device-identity table)

Check SRX UserFW No User Auth Entry With Domain
    [Documentation]    check no this domain auth entry
    [Arguments]    ${device}=${srx0}
    ...            ${domain}=ad03.net
    ...            ${logical_system}=${None}
                   
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show services user-identification authentication-table authentication-source all domain ${domain} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show services user-identification authentication-table authentication-source all domain ${domain}
    Log    ==> prefix is: ${prefix} 
    
    ${result}    Execute cli command on device    ${device}    command=${prefix} 
    Should Match Regexp    ${result}    (There is no related auth entry in authentication-table|There is no authentication-table entry)

Check SRX UserFW Firewall Authe JIMS Counter
    [Documentation]    check SRX UserFW Firewall Auth JIMS counter
    [Arguments]    ${device}=${srx0}
    ...            ${success}=${None}
    ...            ${failure}=${None}
    ${result}    Execute cli command on device    ${device}    command=show security firewall-authentication jims statistics |display xml 
    Run Keyword If    "${success}" is not "${None}"     Should Match Regexp    ${result}    (?is)<jims-stat>.*?<jims-succ>${success}</jims-succ>
    Run Keyword If    "${failure}" is not "${None}"     Should Match Regexp    ${result}    (?is)<jims-fail>${failure}</jims-fail>.*?</jims-stat>
	
Check SRX UserFW Active Directory Domain-controller Status
    [Documentation]    Check SRX UserFW Active Directory Domain-controller Status
    [Arguments]    ${device}=${srx0}
    ...            ${domain}=test.com
    ...            ${dc_name}=test_dc
    ...            ${ip}=1.1.1.1
    ...            ${status}=Connected       #Connected | Disconnected
    ...            ${looptime}=4

    :FOR    ${index}    IN RANGE    ${loop_time}
    \    ${result}    Execute cli command on device    ${device}    command=show services user-identification active-directory-access domain-controller status domain ${domain}
    \    sleep    30
    \    Run Keyword If    '${status}' in '''${result}'''    Exit For Loop
    \     ...    ELSE    Continue For Loop
    Should Match Regexp    ${result}    (?is)${dc_name}\\s*${ip}\\s*${status}    timeout=${150}
	
Deactive SRX UserFW User Identification
    [Documentation]    Deactive SRX UserFW User Identity
    [Arguments]    ${device}=${srx0}
    ${cmd_list} =    Create List        deactivate services user-identification
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
    Commit Configuration                ${device}

Active SRX UserFW User Identification
    [Documentation]    Deactive SRX UserFW User Identity
    [Arguments]    ${device}=${srx0}
    ${cmd_list} =    Create List        activate services user-identification
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
    Commit Configuration                ${device}

Delete SRX UserFW
    [Documentation]    Delete UserFW configuration in srx
    [Arguments]    ${device}=${srx0}
    
    ${cmd_list} =    Create List
    ...               delete services user-identification
    Execute Config Command On Device    ${device}    command_list=${cmd_list}

Delete SRX UserFW Aruba Clearpass
    [Documentation]    Delete UserFW aruba-clearpass configuration in srx
    [Arguments]    ${device}=${srx0}
    
    ${cmd_list} =    Create List
    ...               delete services user-identification authentication-source aruba-clearpass
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
 
#Delete SRX UserFW Webapi
#    [Documentation]    Delete UserFW webapi configuration in srx
#    [Arguments]    ${device}=${srx0}
#    
#    ${cmd_list} =    Create List
#    ...               delete system services webapi
#    Execute Config Command On Device    ${device}    command_list=${cmd_list}
 	
Delete SRX UserFW Active Directory Access
    [Documentation]    Add UserFW active-directory-access configuration in srx
    [Arguments]    ${device}=${srx0}
    ...            ${domain}=ad03.net
    ...            ${user}=${None}
    ...            ${password}=${None}
    ...            ${dc_name}=mydc1
    ...            ${dc_address}=${None}
    ...            ${ldap_base}=${None}
    ...            ${ldap_address}=${None}
    ...            ${ldap_user}=${None}
    ...            ${ldap_password}=${None}
    ...            ${ldap_ssl}=${None}
    ...            ${authentication_algorithm}=${None}
    ...            ${scanning_interval}=${None}
    ...            ${initial_timespan}=${None}
    ...            ${entry_timeout}=${None}
    ...            ${wmi_timeout}=${None}
    ...            ${invalid_timeout}=${None}
    ...            ${force_timeout}=${None}
    ...            ${no_on_demand_probe}=${None} 
    ...            ${filter}=${None}           # include | exclude
    ...            ${filter_all}=${None}
    ...            ${filter_address}=1.2.3.4/24
    
    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${user}" is not "${None}"               Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user ${user} 
    Run Keyword If    "${password}" is not "${None}"           Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user password ${password} 
    Run Keyword If    "${dc_address}" is not "${None}"         Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} domain-controller ${dc_name} address ${dc_address} 
    Run Keyword If    "${ldap_base}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user-group-mapping ldap base ${ldap_base} 
    Run Keyword If    "${ldap_address}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user-group-mapping ldap address ${ldap_address} 
    Run Keyword If    "${ldap_user}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user-group-mapping ldap user ${ldap_user} 
    Run Keyword If    "${ldap_password}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user-group-mapping ldap user password ${ldap_password} 
    Run Keyword If    "${ldap_ssl}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user-group-mapping ldap ssl 
    Run Keyword If    "${authentication_algorithm}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} user-group-mapping ldap authentication-algorithm simple 
    Run Keyword If    "${scanning_interval}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} ip-user-mapping discovery-method wmi event-log-scanning-interval ${scanning_interval} 
    Run Keyword If    "${initial_timespan}" is not "${None}"          Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access domain ${domain} ip-user-mapping discovery-method wmi initial-event-log-timespan ${initial_timespan} 
    Run Keyword If    "${entry_timeout}" is not "${None}"      Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access authentication-entry-timeout
    Run Keyword If    "${wmi_timeout}" is not "${None}"        Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access wmi-timeout ${wmi_timeout}
    Run Keyword If    "${invalid_timeout}" is not "${None}"    Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access invalid-authentication-entry-timeout
    Run Keyword If    "${force_timeout}" is not "${None}"     Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access firewall-authentication-forced-timeout
    Run Keyword If    "${no_on_demand_probe}" is not "${None}"      Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access no-on-demand-probe
    Run Keyword If    "${filter}" is not "${None}"            Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access filter ${filter}
    Run Keyword If    "${filter_address}" is not "${None}"            Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access filter ${filter}  ${filter_address}
    Run Keyword If    "${filter_all}" is not "${None}"            Append To List    ${cmd_list}
    ...               delete services user-identification active-directory-access filter 
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
  
Delete SRX UserFW Identity Management
    [Documentation]    Delete UserFW identity-management configuration in srx
    [Arguments]    ${device}=${srx0}
    ...            ${items_per_batch}=${None}
    ...            ${query_interval}=${None}
    ...            ${entry_timeout}=${None}
    ...            ${query_api}=${None}
    ...            ${token_api}=${None}
    ...            ${invalid_timeout}=${None}
    ...            ${traceoptions}=${None}
    ...            ${logical_systems}=${None}
    ...            ${reserved}=${None}
    ...            ${max}=${None}
    
    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    delete logical-systems ${logical_systems} services user-identification identity-management
    ...         ELSE                                            Set Variable    delete services user-identification identity-management
    Log    ==> prefix is: ${prefix} 
    
    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${items_per_batch}" is not "${None}"        Append To List    ${cmd_list}    ${prefix} batch-query items-per-batch ${items_per_batch} 
    ...    ELSE IF    "${query_interval}" is not "${None}"         Append To List    ${cmd_list}    ${prefix} batch-query query-interval ${query_interval}
    ...    ELSE IF    "${traceoptions}" is not "${None}"           Append To List    ${cmd_list}    ${prefix} traceoptions
    ...    ELSE IF    "${query_api}" is not "${None}"              Append To List    ${cmd_list}    ${prefix} connection query-api ${query_api}
    ...    ELSE IF    "${token_api}" is not "${None}"              Append To List    ${cmd_list}    ${prefix} connection token-api ${token_api}
    ...    ELSE IF    "${entry_timeout}" is not "${None}"          Append To List    ${cmd_list}    ${prefix} authentication-entry-timeout ${entry_timeout}
    ...    ELSE IF    "${invalid_timeout}" is not "${None}"        Append To List    ${cmd_list}    ${prefix} invalid-authentication-entry-timeout ${invalid_timeout}
    #the command "delete services user-identification identity-management logic-domain xxxx" can't use ${prefix}, because they can only configure by "delete services", can't configure by "delete logical-systems"
    ...    ELSE IF    "${logical_systems}" is not "${None}" and ${max} is not "${None}"         Append To List    ${cmd_list}    delete services user-identification identity-management logic-domain ${logical_systems} authentication-entry-capacity max ${max}
    ...    ELSE IF    "${logical_systems}" is not "${None}" and ${reserved} is not "${None}"    Append To List    ${cmd_list}    delete services user-identification identity-management logic-domain ${logical_systems} authentication-entry-capacity reserved ${reserved}
    ...       ELSE                                                 Append To List    ${cmd_list}    ${prefix}
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
 
Delete SRX UserFW Identity Management Filter
    [Documentation]    Delete UserFW identity-management filter configuration in srx
    [Arguments]    ${device}=${srx0}
    
    ${cmd_list} =    Create List
    ...               delete services user-identification identity-management filter
    Execute Config Command On Device    ${device}    command_list=${cmd_list}

Check SRX UserFW Identity Management Trace Query Count
    [Documentation]    Check JIMS Batch Query Count In Trace Log
    [Arguments]    ${device}=${srx0}
    ...            ${log}=jims_log
    ...            ${count}=200
     
    ${response}    Execute Cli Command on Device    ${srx_handle}    command=show log ${log} | grep -i "uid_set_batch_query_url: batch query url"    timeout=${150}
    Should Match Regexp    ${response}    entry_count=${count}

Disable SRX UserID Daemon    
    [Documentation]    Disable UserID Deamon
    [Arguments]    ${device}=${srx0}
	
    @{cmd_list} =    Create List
    ...               set system processes user-ad-authentication disable
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
    Commit Configuration                ${device}	

Enable SRX UserID Daemon    
    [Documentation]    Enable SRX UserID Deamon
    [Arguments]    ${device}=${srx0}
	
    @{cmd_list} =    Create List
    ...               delete system processes user-ad-authentication disable
    Execute Config Command On Device    ${device}    command_list=${cmd_list}
    Commit Configuration    	        ${device}

Add SRX Userfw Local Auth Entry Without Role
    [Documentation]    Add UserFW local auth entry in srx
    [Arguments]    ${device}=${srx0}
    ...            ${ip}=1::1
    ...            ${user}=${None}

    Execute cli command on device    ${device}    command=request security user-identification local-authentication-table add ip-address ${ip} user-name ${user}
    Execute cli command on device    ${device}    command=show security user-identification local-authentication-table all

Add SRX Userfw Local Auth Entry With Role
    [Documentation]    Add UserFW local auth entry in srx
    [Arguments]    ${device}=${srx0}
    ...            ${ip}=1::1
    ...            ${user}=${None}
    ...            ${role}=${None}

    @{role} =   Run Keyword If    isinstance($role,list)     Copy List    ${role}
    ...                   ELSE                             Create List    ${role}
    :FOR    ${arg}    IN    @{role}
    \    Execute cli command on device    ${device}    command=request security user-identification local-authentication-table add ip-address ${ip} user-name ${user} roles ${arg}
    #Check result
    Execute cli command on device    ${device}    command=show security user-identification local-authentication-table all

Delete SRX Userfw Local Auth Entry
    [Documentation]    Add UserFW local auth entry in srx
    [Arguments]    ${device}=${srx0}
    ...            ${ip}=${None}
    ...            ${user}=${None}

    Run Keyword If    "${ip}" is not "${None}"      Execute cli command on device    ${device}    command=request security user-identification local-authentication-table delete ip-address ${ip}
    ...    ELSE IF    "${user}" is not "${None}"    Execute cli command on device    ${device}    command=request security user-identification local-authentication-table delete user ${user}
    ...       ELSE                                  Execute cli command on device    ${device}    command=clear security user-identification local-authentication-table

    ${response}    Run Keyword If    "${ip}" is not "${None}"      Execute cli command on device    ${device}    command=show security user-identification local-authentication-table ip-address ${ip}
    ...                   ELSE IF    "${user}" is not "${None}"    Execute cli command on device    ${device}    command=show security user-identification local-authentication-table user ${user}
    ...                      ELSE                                  Execute cli command on device    ${device}    command=show security user-identification local-authentication-table all

    Run Keyword If    "${ip}" is not "${None}"      Should Not Contain    ${response}    ${ip}
    ...    ELSE IF    "${user}" is not "${None}"    Should Not Contain    ${response}    ${user}
    ...       ELSE                                  Should Contain        ${response}    Total entries: 0


Check SRX UserFW Local Auth Table With IP
    [Documentation]    Check SRX UserFW Auth Table With IP
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.0
    ...           ${user}=${None}
    ...           ${group}=${None}

    ${result}    Execute cli command on device    ${device}    command=show security user-identification local-authentication-table ip-address ${ip}|display xml
    Run Keyword If    "${ip}" is not "${None}"                 Should Match Regexp    ${result}   (?is)<local-authentication-info>.*?<ip-address>${ip}</ip-address>.*?</local-authentication-info>
    Run Keyword If    "${user}" is not "${None}"               Should Match Regexp    ${result}   (?is)</ip-address>.*?<user-name>${user}</user-name>.*?<role-name-list>
    Run Keyword If    "${group}" is not "${None}"              Should Match Regexp    ${result}   (?is)<role-name-list>.*?<role-name>${group}</role-name>.*?</role-name-list>

Check SRX UserFW Local Auth Table With IP On PFE
    [Documentation]    Check SRX UserFW Auth Table With IP
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=${None}
    ...           ${user}=${None}
    ...           ${exist}=${None}
    ...           ${node}=${None}

    Log    ==> Found ip: ${ip}
    @{cmd_list}     Create List    plugin jsf_userfw show local-auth-table
    ${result}    send vty cmd    ${device}    node=${node}    component=SPU    send_cnt=1    cmd=@{cmd_list}

    Run Keyword If    "${exist}" is "${None}"     Should Not Contain     ${result}    (?is)User Name\\s+:\\s+${user}.*?Ip address.*?${ip}

    ${match_result}    ${ip-address}    Run Keyword If    "${exist}" is not "${None}"
    ...          Should Match Regexp      ${result}    (?i)User Name\\s+:\\s+${user}[\\r\\n]{1,2}Ip address\\s+:\\s+(.*?)[\\r\\n]{1,2}

    Log    ==> Found ip result: ${ip-address}
    ${match_ip}=    Run Keyword If    "${ip-address}" is not "${None}"      ipaddress.IP Address    ${ip-address}
    Log    ==> Found ip result: ${match_ip}

    ${result}     Run Keyword If    "${match_ip}" is not "${None}"    CMP IP    ${ip}    ${match_ip}
    Run Keyword If    "${match_ip}" is not "${None}"    Should Be True    ${result}    ${TRUE}

	
Check SRX UserFW AD Table With IP On PFE
    [Documentation]    Check SRX UserFW AD Table With IP On PFE
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=${None}
    ...           ${user}=${None}
    ...           ${domain}=${None}
    ...           ${state}=${None}
    ...           ${group_number}=${None}
    ...           ${group_list}=${None}
    ...           ${node}=${None}

    @{cmd_list}     Create List    plugin jsf_userfw show ad-auth ip-address ${ip} 
    ${result}    send vty cmd    ${device}    node=${node}    component=SPU    send_cnt=1    cmd=@{cmd_list}
	
    ${match_result}    ${ip-address}    
    ...          Should Match Regexp      ${result}     (?i)Ip address:\\s+(.*?)[\\r\\n]{1,2}
	
    Log    ==> Found ip result: ${ip-address}
    ${match_ip}=    Run Keyword If    "${ip-address}" is not "${None}"      ipaddress.IP Address    ${ip-address}
    Log    ==> Found ip result: ${match_ip}

    ${response}     Run Keyword If    "${match_ip}" is not "${None}"    CMP IP    ${ip}    ${match_ip}
    Run Keyword If     "${match_ip}" is not "${None}"     Should Be True    ${response}    ${TRUE}
	
    Run Keyword If    "${user}" is not "${None}"             Should Match Regexp     ${result}    (?is)User Name:\\s*${user}
    Run Keyword If    "${domain}" is not "${None}"           Should Match Regexp     ${result}    (?is)Domain Name:\\s*${domain}
    Run Keyword If    "${ip}" is not "${None}"               Should Match Regexp     ${result}    (?is)IP address:\\s*${ip-address}
    Run Keyword If    "${state}" is not "${None}"            Should Match Regexp     ${result}    (?is)State:\\s*${state}
    Run Keyword If    "${group_number}" is not "${None}"     Should Match Regexp     ${result}    (?is)Group number:\\s+${group_number}
    Run Keyword If    "${group_list}" is not "${None}"       Should Match Regexp     ${result}    (?is)Group list:.*?${group_list}

	
Get SRX UserFW Policy User-id On PFE
    [Documentation]    Get SRX UserFW Policy User-id On PFE
	...           return: number(1,2,40...)
    [Arguments]   ${device}=${srx0}
    ...           ${domain}=${None}
    ...           ${user_id}=${None}
    ...           ${node}=${None}
    [Return]      ${result}

    @{cmd_list}     Create List    show usp policy user-id
    ${response}    send vty cmd    ${device}    node=${node}    component=SPU    send_cnt=1    cmd=@{cmd_list}
	
    ${match_result}    ${result}    Run Keyword If    "${domain}" is "${None}"
    ...          Should Match Regexp      ${response}    (?is)(\\d*):\\s*-->\\s*${user_id}
	
    ${match_result}    ${result}    Run Keyword If    "${domain}" is not "${None}"
    ...          Should Match Regexp      ${response}    (?is)(\\d*):\\s*-->\\s*${domain}\\\\${user_id}
	
    Log    ${result}

	
Get SRX UserFW Profile ID
    [Documentation]    Get SRX UserFW Profile ID
	...           return: number(1,2,40...)
    [Arguments]   ${device}=${srx0}
    ...           ${profile}={None}
    [Return]      ${result}

    ${response}    Execute shell command on device    ${device}    command=cat /var/etc/userid_end_user_profile.id

    ${match_result}    ${result}    Run Keyword If    "${profile}" is not "${None}"
    ...          Should Match Regexp      ${response}    (?is)(\\d*)\\s*${profile}
	
    Log    ${result}	
	
	
Check SRX UserFW Ipid-client With IP On PFE
    [Documentation]    Check SRX UserFW Ipid-client With IP On PFE
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=${None}
    ...           ${profile_id}={None}
    ...           ${node}=${None}

    @{cmd_list}     Create List    show usp ipid-client name userid range ${ip} 
    ${result}    send vty cmd    ${device}    node=${node}    component=SPU    send_cnt=1    cmd=@{cmd_list}
	
    Run Keyword If    "${profile_id}" is not "${None}"    Should Match Regexp    ${result}    (?is)\\)\\s*:\\s*${profile_id}

	
Config SRX Authentication-source Priority
    [Documentation]    Config SRX Authentication-source Priority
    [Arguments]    ${device}=${srx0}
    ...            ${source}=active-directory-authentication-table
    ...            ${priority}=100
    
    ${cmd_list} =      Create List    ${EMPTY}
    Append To List    ${cmd_list}    set security user-identification authentication-source ${source} priority ${priority}

    Execute Config Command On Device    ${device}    command_list=${cmd_list}
	
Delete SRX Authentication-source Priority
    [Documentation]    Delete SRX Authentication-source Priority
    [Arguments]    ${device}=${srx0}
    ...            ${source}=active-directory-authentication-table
    ...            ${priority}=100
    
    ${cmd_list} =      Create List    ${EMPTY}
    Append To List    ${cmd_list}    delete security user-identification authentication-source ${source} priority ${priority}

    Execute Config Command On Device    ${device}    command_list=${cmd_list} 
