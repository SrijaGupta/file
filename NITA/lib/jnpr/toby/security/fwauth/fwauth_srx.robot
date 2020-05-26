*** Setting ***
Documentation
...     This file contains all the Firewall robot keyword for SRX
...
...     Author: Wentao Wu (wtwu@juniper.net)
...
...     Keyword list:
...             Config SRX Security Policies With Firewall Auth
...             Delete SRX Security Policies With Firewall Auth
...             Config SRX Access Profile
...             Delete SRX Access Profile
...             Config SRX Access Firewall Auth
...             Delete SRX Access Firewall Auth
...             Config SRX System Web-management Service
...             Config SRX Ssl Profile
...             Generate SRX Security Pki Certificate
#...             Check SRX Firewall Auth Table
...             Check SRX Firewall Auth History Table
...             Show SRX Firewall Auth Table All
...             Show SRX Firewall Auth History Table All
...             Clear SRX Firewall Auth Table All
...             Clear SRX Firewall Auth History Table All



*** Keywords ***

Config SRX Security Policies With Firewall Auth
    [Documentation]    Config SRX Security Policies With Firewall Auth
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=p1
    ...            ${from_zone}=trust
    ...            ${to_zone}=untrust
    ...            ${web_authentication}=${None}
    ...            ${pass_through}=${None}
    ...            ${push_to_identity_management}=${None}
    ...            ${access_profile}=${None}
    ...            ${web_redirect}=${None}
    ...            ${web_redirect_to_https}=${None}
    ...            ${client_match}=${None}
    ...            ${ssl_termination_profile}=${None}
    ...            ${auth_user_agent}=${None}
    ...            ${auth_only_browser}=${None}
    ...            ${domain}=${None}
    ...            ${auth_type}=pass-through
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    logical-systems ${logical_system} security policies
    ...         ELSE                                            Set Variable    security policies
    Log    ==> prefix is: ${prefix}

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${web_authentication}" is not "${None}"             Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication web-authentication
    Run Keyword If    "${pass_through}" is not "${None}"                   Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication pass-through
    Run Keyword If    "${push_to_identity_management}" is not "${None}"    Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication push-to-identity-management
    Run Keyword If    "${domain}" is not "${None}"                         Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication user-firewall domain ${domain}
    Run Keyword If    "${access_profile}" is not "${None}"                 Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} access-profile ${access_profile}
    Run Keyword If    "${web_redirect}" is not "${None}"                   Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} web-redirect
    Run Keyword If    "${web_redirect_to_https}" is not "${None}"          Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} web-redirect-to-https
    Run Keyword If    "${ssl_termination_profile}" is not "${None}"        Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} ssl-termination-profile ${ssl_termination_profile}
    Run Keyword If    "${auth_user_agent}" is not "${None}"                Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} auth-user-agent ${auth_user_agent}
    Run Keyword If    "${auth_only_browser}" is not "${None}"              Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} auth-only-browser
    Run Keyword If    "${client_match}" is not "${None}"                   Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication pass-through client-match ${client_match}
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

    #display result in log
    Append To List    ${cmd_list}    show ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} |display set
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

Delete SRX Security Policies With Firewall Auth
    [Documentation]    Delete SRX Security Policies With Firewall Auth
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=p1
    ...            ${from_zone}=trust
    ...            ${to_zone}=untrust
    ...            ${web_authentication}=${None}
    ...            ${push_to_identity_management}=${None}
    ...            ${access_profile}=${None}
    ...            ${web_redirect}=${None}
    ...            ${web_redirect_to_https}=${None}
    ...            ${client_match}=${None}
    ...            ${ssl_termination_profile}=${None}
    ...            ${auth_user_agent}=${None}
    ...            ${auth_only_browser}=${None}
    ...            ${domain}=${None}
    ...            ${auth_type}=pass-through
    ...            ${firewall_authentication}=${None}
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    logical-systems ${logical_system} security policies
    ...         ELSE                                            Set Variable    security policies
    Log    ==> prefix is: ${prefix}

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${web_authentication}" is not "${None}"             Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication web-authentication
    Run Keyword If    "${push_to_identity_management}" is not "${None}"    Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication push-to-identity-management
    Run Keyword If    "${domain}" is not "${None}"                         Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication user-firewall domain ${domain}
    Run Keyword If    "${access_profile}" is not "${None}"                 Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} access-profile ${access_profile}
    Run Keyword If    "${web_redirect}" is not "${None}"                   Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} web-redirect
    Run Keyword If    "${web_redirect_to_https}" is not "${None}"          Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} web-redirect-to-https
    Run Keyword If    "${ssl_termination_profile}" is not "${None}"        Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} ssl-termination-profile ${ssl_termination_profile}
    Run Keyword If    "${auth_user_agent}" is not "${None}"                Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} auth-user-agent ${auth_user_agent}
    Run Keyword If    "${auth_only_browser}" is not "${None}"              Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication ${auth_type} auth-only-browser
    Run Keyword If    "${client_match}" is not "${None}"                   Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication pass-through client-match ${client_match}
    Run Keyword If    "${firewall_authentication}" is not "${None}"        Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit firewall-authentication
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

    #display result in log
    Append To List    ${cmd_list}    show ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} |display set
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

Config SRX Access Profile
    [Documentation]    Config SRX Access Profile
    [Arguments]    ${device}=${srx0}
    ...            ${profile}=myprofile1
    ...            ${user}=myuser1
    ...            ${password}=${None}
    ...            ${domain}=${None}
    ...            ${pap_password}=${None}
    ...            ${chap_secret}=${None}
    ...            ${xauth}=${None}
    ...            ${authentication_order}=${None}
    ...            ${ldap_server}=${None}
    ...            ${ldap_options}=${None}
    ...            ${radius_server}=${None}
    ...            ${radius_secret}=juniper
    ...            ${securid_server}=${None}
    ...            ${client_idle_timeout}=${None}
    ...            ${client_session_timeout}=${None}
    ...            ${client_group}=${None}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${password}" is not "${None}"        Append To List    ${cmd_list}    set access profile ${profile} client ${user} firewall-user password ${password}
    Run Keyword If    "${domain}" is not "${None}"          Append To List    ${cmd_list}    set access profile ${profile} client ${domain}\\${user} firewall-user password ${password}
#    Run Keyword If    "${pap_password}" is not "${None}"    Append To List    ${cmd_list}    set access profile ${profile} client ${user} pap-password ${pap_password}
#    Run Keyword If    "${chap_secret}" is not "${None}"     Append To List    ${cmd_list}    set access profile ${profile} client ${user} chap-secret ${chap_secret}
#    Run Keyword If    "${xauth}" is not "${None}"           Append To List    ${cmd_list}    set access profile ${profile} client ${user} xauth ip-address ${xauth}
    Run Keyword If    "${authentication_order}" is not "${None}"    Append To List    ${cmd_list}    set access profile ${profile} authentication-order ${authentication_order}
    Run Keyword If    "${ldap_server}" is not "${None}"     Append To List    ${cmd_list}    set access profile ${profile} ldap-server ${ldap_server}
    Run Keyword If    "${ldap_options}" is not "${None}"    Append To List    ${cmd_list}    set access profile ${profile} ldap-options base-distinguished-name ${ldap_options}
    Run Keyword If    "${radius_server}" is not "${None}"    Append To List    ${cmd_list}    set access profile ${profile} radius-server ${radius_server} secret ${radius_secret}
    Run Keyword If    "${securid_server}" is not "${None}"   Append To List    ${cmd_list}    set access securid-server ace configuration-file /var/db/ace/sdconf.rec
    Run Keyword If    "${client_idle_timeout}" is not "${None}"    Append To List    ${cmd_list}    set access profile ${profile} session-options client-idle-timeout ${client_idle_timeout}
    Run Keyword If    "${client_session_timeout}" is not "${None}"    Append To List    ${cmd_list}    set access profile ${profile} session-options client-session-timeout ${client_session_timeout}
    Run Keyword If    "${client_group}" is not "${None}"     Append To List    ${cmd_list}    set access profile ${profile} client ${user} client-group ${client_group}
    #display result in log
    Append To List    ${cmd_list}    show access | display set
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Delete SRX Access Profile
    [Documentation]    Delete SRX Access Profile
    [Arguments]    ${device}=${srx0}
    ...            ${profile}=${None}
    ...            ${user}=${None}
    ...            ${password}=${None}
    ...            ${domain}=${None}
    ...            ${pap_password}=${None}
    ...            ${chap_secret}=${None}
    ...            ${xauth}=${None}
    ...            ${authentication_order}=${None}
    ...            ${ldap_server}=${None}
    ...            ${ldap_options}=${None}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${password}" is not "${None}"                Append To List    ${cmd_list}    delete access profile ${profile} client ${user} firewall-user password
    ...    ELSE IF    "${domain}" is not "${None}"                  Append To List    ${cmd_list}    delete access profile ${profile} client ${domain}\\${user} firewall-user password
#    ...    ELSE IF    "${pap_password}" is not "${None}"            Append To List    ${cmd_list}    delete access profile ${profile} client ${user} pap-password
#    ...    ELSE IF    "${chap_secret}" is not "${None}"             Append To List    ${cmd_list}    delete access profile ${profile} client ${user} chap-secret
#    ...    ELSE IF    "${xauth}" is not "${None}"                   Append To List    ${cmd_list}    delete access profile ${profile} client ${user xauth ip-address
    ...    ELSE IF    "${user}" is not "${None}"                    Append To List    ${cmd_list}    delete access profile ${profile} client ${user}
    ...    ELSE IF    "${ldap_server}" is not "${None}"             Append To List    ${cmd_list}    delete access profile ${profile} ldap-server
    ...    ELSE IF    "${ldap_options}" is not "${None}"            Append To List    ${cmd_list}    delete access profile ${profile} ldap-options
    ...    ELSE IF    "${authentication_order}" is not "${None}"    Append To List    ${cmd_list}    delete access profile ${profile} authentication-order
    ...    ELSE IF    "${profile}" is not "${None}"                 Append To List    ${cmd_list}    delete access profile ${profile}
    ...       ELSE                                                  Append To List    ${cmd_list}    delete access
    #display result in log
    Append To List    ${cmd_list}    show access | display set
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX Access Firewall Auth
    [Documentation]    Config SRX Access Firewall Auth
    [Arguments]    ${device}=${srx0}
    ...            ${web_auth_profile}=${None}
    ...            ${web_auth_banner}=${None}
    ...            ${pass_through_profile}=${None}
    ...            ${pass_through}=${None}     # ftp | http | telnet
    ...            ${success_banner}=${None}
    ...            ${login_banner}=${None}
    ...            ${fail_banner}=${None}
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    logical-systems ${logical_system} access firewall-authentication
    ...         ELSE                                            Set Variable    access firewall-authentication
    Log    ==> prefix is: ${prefix}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${web_auth_profile}" is not "${None}"        Append To List    ${cmd_list}    set ${prefix} web-authentication default-profile ${web_auth_profile}
    Run Keyword If    "${web_auth_banner}" is not "${None}"         Append To List    ${cmd_list}    set ${prefix} web-authentication banner success ${web_auth_banner}
    Run Keyword If    "${pass_through_profile}" is not "${None}"    Append To List    ${cmd_list}    set ${prefix} pass-through default-profile ${pass_through_profile}
    Run Keyword If    "${login_banner}" is not "${None}"       Append To List    ${cmd_list}    set ${prefix} pass-through ${pass_through} banner login ${login_banner}
    Run Keyword If    "${success_banner}" is not "${None}"     Append To List    ${cmd_list}    set ${prefix} pass-through ${pass_through} banner success ${success_banner}
    Run Keyword If    "${fail_banner}" is not "${None}"        Append To List    ${cmd_list}    set ${prefix} pass-through ${pass_through} banner fail ${fail_banner}
    #display result in log
    Append To List    ${cmd_list}    show ${prefix} |display set
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}
    
Delete SRX Access Firewall Auth
    [Documentation]    Delete SRX Access Firewall Auth
    [Arguments]    ${device}=${srx0}
    ...            ${web_auth}=${None}
    ...            ${pass_through}=${None}
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    logical-systems ${logical_system} access firewall-authentication
    ...         ELSE                                            Set Variable    access firewall-authentication
    Log    ==> prefix is: ${prefix}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${web_auth}" is not "${None}"               Append To List    ${cmd_list}    delete ${prefix} web-authentication
    ...    ELSE IF    "${pass_through}" is not "${None}"           Append To List    ${cmd_list}    delete ${prefix} pass-through
    ...       ELSE                                                 Append To List    ${cmd_list}    delete ${prefix}
    #display result in log
    Append To List    ${cmd_list}    show ${prefix} |display set
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX System Web-management Service
    [Documentation]    Config SRX System Web-management Service
    [Arguments]   ${device}=${srx0}
    ...           ${service}=${None}    # ftp | telnet | http | https
    ...           ${pki_certificate}=${None}
    ...           ${interface}=${None}

    @{cmd_list} =    Create List   ${EMPTY}
    Run Keyword If    "${service}" is "http" or "${service}" is "https"   Append To List    ${cmd_list}    set system services web-management ${service}
    ...    ELSE IF    "${service}" is not"${None}"   Append To List    ${cmd_list}    set system services ${service}
    ...       ELSE                                   Append To List    ${cmd_list}    set system services
    Run Keyword If    "${pki_certificate}" is not"${None}"    Append To List    ${cmd_list}   set system services web-management ${service} pki-local-certificate ${pki_certificate}
    Run Keyword If    "${interface}" is not"${None}"    Append To List    ${cmd_list}   set system services web-management ${service} interface ${interface}
    Execute config command on device    ${device}    command_list=@{cmd_list}

Config SRX Ssl Profile
    [Documentation]    Config SRX Ssl Profile
    [Arguments]   ${device}=${srx0}
    ...           ${termination_profile}=fwauthhttpspf    # ftp | telnet | http | https
    ...           ${pki_certificate}=device
    ...           ${proxy_profile}=ssl_inspect_profile

    @{cmd_list} =    Create List   ${EMPTY}
    Append To List    ${cmd_list}   set services ssl termination profile ${termination_profile} server-certificate ${pki_certificate}
    Append To List    ${cmd_list}   set services ssl proxy profile ${proxy_profile} root-ca ${pki_certificate}
    Append To List    ${cmd_list}   set services ssl proxy profile ${proxy_profile} actions ignore-server-auth-failure
    Execute config command on device    ${device}    command_list=@{cmd_list}

Generate SRX Security Pki Certificate
    [Documentation]    Generate Security Pki Certificate
    [Arguments]   ${device}=${srx0}
    ...           ${pki_certificate}=device

    Execute Cli Command on Device    ${device}    command=clear security pki local-certificate all
    Execute Cli Command on Device    ${device}    command=clear security pki key-pair all
    Execute Cli Command on Device    ${device}    command=request security pki generate-key-pair certificate-id ${pki_certificate} size 2048 type rsa
    Execute Cli Command on Device    ${device}    command=request security pki local-certificate generate-self-signed certificate-id ${pki_certificate} domain-name www.juniper.net subject "CN=www.juniper.net,OU=IT,O=Juniper networks,L=Sunnyvale,ST=CA,C=US" email security-admin@juniper.net


#Check SRX Firewall Auth Table
#    [Documentation]    Check SRX Firewall Auth Table
#    [Arguments]   ${device}=${srx0}
#    ...           ${ip}=1.2.3.4
#    ...           ${user_name}=${None}
#    ...           ${status}=${None}
#    ...           ${method}=${None}
#    ...           ${src_zone}=${None}
#    ...           ${dst_zone}=Valid
#    ...           ${profile}=${None}
#    ...           ${node}=${None}
#    ...           ${client_groups}=${None}
#    ...           ${logical_system}=${None}

#    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"     Set Variable    show security firewall-authentication users logical-system ${logical_system}
#    ...         ELSE                                            Set Variable    show security firewall-authentication users
#    Log    ==> prefix is: ${prefix}
#    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} address ${ip} node ${node} |display xml
#    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix} address ${ip} |display xml
#    Run Keyword If    "${user_name}" is not "${None}"    Should Match Regexp    ${result}   (?is)<user-info.*?<user-name>${user_name}</user-name>
#    Run Keyword If    "${ip}" is not "${None}"           Should Match Regexp    ${result}   (?is)<src-ip>${ip}</src-ip>
#    Run Keyword If    "${status}" is not "${None}"       Should Match Regexp    ${result}   (?is)<status>${status} </status>
#    Run Keyword If    "${method}" is not "${None}"       Should Match Regexp    ${result}   (?is)<method>${method}</method>
#    Run Keyword If    "${src_zone}" is not "${None}"     Should Match Regexp    ${result}   (?is)<src-zone>${src_zone}</src-zone>
#    Run Keyword If    "${dst_zone}" is not "${None}"     Should Match Regexp    ${result}   (?is)<dst-zone>${dst_zone}</dst-zone>
#    Run Keyword If    "${profile}" is not "${None}"     Should Match Regexp    ${result}   (?is)<access-profile>${profile}</access-profile>
#    Run Keyword If    "${client_groups}" is not "${None}"     Should Match Regexp    ${result}   (?is)<client-groups>${client_groups}</client-groups>
#    Run Keyword If    "${logical_system}" is not "${None}"     Should Match Regexp    ${result}   (?is)<lsys-name>${logical_system}</lsys-name>

Check SRX Firewall Auth Table Client Group
    [Documentation]    Check SRX Firewall Auth Table Client Group
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.4
    ...           ${group}=${None}
    ...           ${node}=${None}
    ...           ${logical_system}=${None}
    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"     Set Variable    show security firewall-authentication users logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show security firewall-authentication users
    Log    ==> prefix is: ${prefix}
    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} address ${ip} node ${node} |display xml
    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix} address ${ip} |display xml
    ${match_result}    ${group_list}
    ...          Should Match Regexp      ${result}    (?is)<client-groups>(.*)</client-groups>
    Log    ==> Found group result: ${group_list}
    Log    ==> Need to verify group result: @{group}
    :FOR    ${group_name}     IN    @{group}
    \    Should Contain    ${group_list}    ${group_name}
	
Check SRX Firewall Auth History Table
    [Documentation]    Check SRX Firewall History Table
    [Arguments]   ${device}=${srx0}
    ...           ${ip}=1.2.3.4
    ...           ${user_name}=${None}
    ...           ${status}=${None}
    ...           ${method}=${None}
    ...           ${src_zone}=${None}
    ...           ${dst_zone}=Valid
    ...           ${profile}=${None}
    ...           ${node}=${None}
    ...           ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"     Set Variable    show security firewall-authentication history logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show security firewall-authentication history
    Log    ==> prefix is: ${prefix}
    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} address ${ip} node ${node} |display xml
    ...                      ELSE                                  Execute cli command on device    ${device}    command=${prefix} address ${ip} |display xml
    Run Keyword If    "${user_name}" is not "${None}"    Should Match Regexp    ${result}   (?is)<user-history-info.*?<user-name>${user_name}</user-name>
    Run Keyword If    "${ip}" is not "${None}"           Should Match Regexp    ${result}   (?is)<src-ip>${ip}</src-ip>
    Run Keyword If    "${status}" is not "${None}"       Should Match Regexp    ${result}   (?is)<status>${status} </status>
    Run Keyword If    "${method}" is not "${None}"       Should Match Regexp    ${result}   (?is)<method>${method}.*</method>
    Run Keyword If    "${src_zone}" is not "${None}"     Should Match Regexp    ${result}   (?is)<src-zone>${src_zone}</src-zone>
    Run Keyword If    "${dst_zone}" is not "${None}"     Should Match Regexp    ${result}   (?is)<dst-zone>${dst_zone}</dst-zone>
    Run Keyword If    "${profile}" is not "${None}"     Should Match Regexp    ${result}   (?is)<access-profile>${profile}</access-profile>
    Run Keyword If    "${logical_system}" is not "${None}"     Should Match Regexp    ${result}   (?is)<lsys-name>${logical_system}</lsys-name>

Show SRX Firewall Auth Table All
    [Documentation]    Clear Firewall auth table all in srx
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"     Set Variable    show security firewall-authentication users logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show security firewall-authentication users
    Log    ==> prefix is: ${prefix}
   
    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node}
    ...       ELSE                                  Execute cli command on device    ${device}    command=${prefix}

Show SRX Firewall Auth History Table All
    [Documentation]    Clear Firewall auth history all in srx
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"     Set Variable    show security firewall-authentication history logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show security firewall-authentication history
    Log    ==> prefix is: ${prefix}

    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node}
    ...       ELSE                                  Execute cli command on device    ${device}    command=${prefix}

Clear SRX Firewall Auth Table All
    [Documentation]    Clear SRX Firewall Auth Table All
    [Arguments]    ${device}=${srx0}
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"     Set Variable    security firewall-authentication users logical-system ${logical_system}
    ...         ELSE                                            Set Variable    security firewall-authentication users
    Log    ==> prefix is: ${prefix}

    Execute cli command on device    ${device}    command=clear ${prefix}
    #Check result
    Execute cli command on device    ${device}    command=show ${prefix}

Clear SRX Firewall Auth History Table All
    [Documentation]    Clear SRX Firewall Auth History Table All
    [Arguments]    ${device}=${srx0}
    ...            ${logical_system}=${None}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"     Set Variable    security firewall-authentication history logical-system ${logical_system}
    ...         ELSE                                            Set Variable    security firewall-authentication history
    Log    ==> prefix is: ${prefix}

    Execute cli command on device    ${device}    command=clear ${prefix}
    #Check result
    Execute cli command on device    ${device}    command=show ${prefix}
