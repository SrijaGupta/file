*** Settings ***
Documentation    Master Resource file for Toby Keyword
...              This resource file is collection of all resource files defined
...              in UserFW Windows PC
...
...              Author: Wentao Wu (wtwu@juniper.net)
...
...              Keywords List:
...                     Clear Windows DC Eventlog
...                     Generate Windows DC Eventlog
...                     Add Windows DC User
...                     Add Windows DC Computer
...                     Add Windows DC Group
...                     Add Windows DC User To Group
...                     Add Windows DC Computer To Group
...                     Delete Windows DC User From Group
...                     Delete Windows DC Computer From Group
...                     Delete Windows DC User
...                     Delete Windows DC Computer
...                     Delete Windows DC Group
...                     Restart Windows JIMS Service
...                     Add JIMS Management Client In Windows
...                     Add JIMS SRX Client In Windows
...                     Add JIMS Active Directory In Windows
...                     Add JIMS Event Source In Windows
...                     Add JIMS Session Logoff Time In Windows
...                     Check Windows DC Eventlog Tool
...                     Add JIMS SRX Clients Start In Windows
...                     Add JIMS SRX Clients Midbody In Windows
...                     Add JIMS SRX Clients End In Windows
...                     Add JIMS Client Https Connection In Windows
...                     Add JIMS Client Http Connection In Windows

*** Keywords ***
Clear Windows DC Eventlog
    [Documentation]    Clear windows eventlog in dc
    [Arguments]    ${device}=${dc0}
    Execute Shell Command on Device    ${device}    command=c:\\Windows\\System32\\wevtutil.exe cl security

Generate Windows DC EventLog
    [Documentation]  generate event log
    [Arguments]   ${device}=${dc0}
    ...           ${type}=user          #type canbe user|computer|all
    ...           ${domain_name}=test.com
    ...           ${user_name}=myuser
    ...           ${computer_name}=mypc
    ...           ${initial_ip}=1.1.1.0
    ...           ${event_count}=1
    ...           ${username_change_flag}=1     # 0|1
    ...           ${exefile}=c:\\Test\\SELG_RT.exe
    ...           ${format_flag}=0              # 0|1
    Run Keyword If   'user'=='${type}'    Execute Shell Command on Device    ${device}    command=${exefile} -domainname ${domain_name} -totaleventcount ${event_count} -username_wordpart ${user_name} -initialip ${initial_ip} -makeusernamechange ${username_change_flag} -formatsequencenumber ${format_flag}
    ...    ELSE IF   'computer'=='${type}'    Execute Shell Command on Device    ${device}    command=${exefile} -domainname ${domain_name} -totaleventcount ${event_count} -machineidwordpart ${computer_name} -initialip ${initial_ip} -makeusernamechange ${username_change_flag} -formatsequencenumber ${format_flag}
    ...       ELSE    Execute Shell Command on Device    ${device}    command=${exefile} -domainname ${domain_name} -totaleventcount ${event_count} -username_wordpart ${user_name} -machineidwordpart ${computer_name} -initialip ${initial_ip} -makeusernamechange ${username_change_flag} -formatsequencenumber ${format_flag}

Add Windows DC User
    [Documentation]    add user on DC
    [Arguments]    ${device}=${dc0}
    ...            ${password}=Netscreen1
    ...            ${user_list}=${None}
    @{user_list} =   Run Keyword If    isinstance($user_list,list)     Copy List    ${user_list}
    ...                        ELSE                                  Create List    ${user_list}
    :FOR    ${arg}    IN    @{user_list}
    \    Execute Shell Command on Device    ${device}    command=net user "${arg}" ${password} /add /domain

Add Windows DC Computer
    [Documentation]    add computer on DC
    [Arguments]    ${device}=${dc0}
    ...            ${computer_list}=${None}
    @{computer_list} =   Run Keyword If    isinstance($computer_list,list)     Copy List    ${computer_list}
    ...                            ELSE                                      Create List    ${computer_list}
    :FOR    ${arg}    IN    @{computer_list}
    \    Execute Shell Command on Device    ${device}    command=net computer \\\\${arg} /add

Add Windows DC Group
    [Documentation]    add group on DC
    [Arguments]    ${device}=${dc0}
    ...            ${group_list}=${None}
    @{group_list} =   Run Keyword If    isinstance($group_list,list)      Copy List    ${group_list}
    ...                         ELSE                                    Create List    ${group_list}
    :FOR    ${arg}    IN    @{group_list}
    \    Execute Shell Command on Device    ${device}    command=net group "${arg}" /add /domain

Add Windows DC User To Group
    [Documentation]    add one user into group on DC
    [Arguments]    ${device}=${dc0}
    ...            ${user_name}=myuser1
    ...            ${group_list}=${None}
    @{group_list} =   Run Keyword If    isinstance($group_list,list)     Copy List    ${group_list}
    ...                         ELSE                                   Create List    ${group_list}
    :FOR    ${arg}    IN    @{group_list}
    \    Execute Shell Command on Device    ${device}    command=net group "${arg}" ${user_name} /add /domain

Add Windows DC Computer To Group
    [Documentation]    add one computer into group on DC
    [Arguments]    ${device}=${dc0}
    ...            ${computer_name}=mypc1
    ...            ${group_list}=${None}
    @{group_list} =   Run Keyword If    isinstance($group_list,list)     Copy List    ${group_list}
    ...                         ELSE                                   Create List    ${group_list}
    :FOR    ${arg}    IN    @{group_list}
    \    Execute Shell Command on Device    ${device}    command=net group "${arg}" ${computer_name}\$ /add /domain

Delete Windows DC User From Group
    [Documentation]    delete one user into group on DC
    [Arguments]    ${device}=${dc0}
    ...            ${user_name}=myuser1
    ...            ${group_list}=${None}
    @{group_list} =   Run Keyword If    isinstance($group_list,list)     Copy List    ${group_list}
    ...                         ELSE                                   Create List    ${group_list}
    :FOR    ${arg}    IN    @{group_list}
    \    Execute Shell Command on Device    ${device}    command=net group "${arg}" ${user_name} /delete /domain


Delete Windows DC Computer From Group
    [Documentation]    delete one computer into group on DC
    [Arguments]    ${device}=${dc0}
    ...            ${computer_name}=mypc1
    ...            ${group_list}=${None}
    @{group_list} =   Run Keyword If    isinstance($group_list,list)     Copy List    ${group_list}
    ...                         ELSE                                   Create List    ${group_list}
    :FOR    ${arg}    IN    @{group_list}
    \    Execute Shell Command on Device    ${device}    command=net group "${arg}" ${computer_name}\$ /delete /domain

Delete Windows DC User
    [Documentation]    delete user on DC
    [Arguments]    ${device}=${dc0}
    ...            ${user_list}=${None}
    @{user_list} =   Run Keyword If    isinstance($user_list,list)     Copy List    ${user_list}
    ...                         ELSE                                 Create List    ${user_list}
    :FOR    ${arg}    IN    @{user_list}
    \    Execute Shell Command on Device    ${device}    command=net user "${arg}" /delete /domain

Delete Windows DC Computer
    [Documentation]    delete computer on DC
    [Arguments]    ${device}=${dc0}
    ...            ${computer_list}=${None}

    @{computer_ist} =   Run Keyword If    isinstance($computer_list,list)     Copy List    ${computer_list}
    ...                         ELSE                                       Create List    ${computer_list}
    :FOR    ${arg}    IN    @{computer_list}
    \    Execute Shell Command on Device    ${device}    command=net computer \\\\${arg} /del

Delete Windows DC Group
    [Documentation]    delete group on DC
    [Arguments]    ${device}=${dc0}
    ...            ${group_list}=${None}
    @{group_list} =   Run Keyword If    isinstance($group_list,list)     Copy List    ${group_list}
    ...                         ELSE                                   Create List    ${group_list}
    :FOR    ${arg}    IN    @{group_list}
    \    Execute Shell Command on Device    ${device}    command=net group "${arg}" /delete /domain

Stop Windows JIMS Service
    [Documentation]    stop jims service
    [Arguments]    ${device}=${jims0}
    ${result} =    Execute Shell Command on Device    ${device}    command=net stop jims
    Should Contain    ${result}    stopped

Start Windows JIMS Service
    [Documentation]    stop jims service
    [Arguments]    ${device}=${jims0}
    ${result} =    Execute Shell Command on Device    ${device}    command=net start jims
    Should Contain    ${result}    started

Restart Windows JIMS Service
    [Documentation]    restart jims service
    [Arguments]    ${device}=${jims0}
    Stop Windows UserFW JIMS Service     device=${device}
    Start Windows UserFW JIMS Service    device=${device}

Add JIMS Management Client In Windows
    [Documentation]    add jims management client ip config
    [Arguments]    ${device}=${jims0}
    ...            ${ip}=101.0.1.131
    ...            ${name}=linux0
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"
    ...            ${file_name}=admin_whitelist_static.xml
    Execute Shell Command on Device    ${device}    command=echo ^<?xml version=^"1.0^"?^> >c:\\${file_name}
    Execute Shell Command on Device    ${device}    command=echo ^<clients^> >>c:\\${file_name}
    Execute Shell Command on Device    ${device}    command=echo ^<client id=^"local^" address=^"127.0.0.1^"/^> >>c:\\${file_name}
    Execute Shell Command on Device    ${device}    command=echo ^<client id=^"${name}^" address=^"${ip}^"/^> >>c:\\${file_name}
    Execute Shell Command on Device    ${device}    command=echo ^</clients^> >>c:\\${file_name}
    Execute Shell Command on Device    ${device}    command=more c:\\${file_name}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=move /Y c:\\${file_name} cwd\\system\\init\\
    Restart Windows Service            ${device}    service=jims

Add JIMS SRX Client In Windows
    [Documentation]    Add SRX Client on JIMS
    [Arguments]    ${device}=${jims0}
    ...            ${id}=srx0
    ...            ${ip}=101.1.0.31
    ...            ${name}=e02-18
    ...            ${client_id}=otest
    ...            ${client_secret}=c3eb4bc2fcf153aaf54aa3fcdc65ee615319769686153411e75774114890c8a71ee94933b8cd6973894c7a41334a098a
    ...            ${token_lifetime}=28800
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"
    ...            ${ipv6}=false    #enable or disable push ipv6 auth entry to DUT, default is false
    ...            ${webapi}=false   #please use true or false
    ...            ${webapi_user}=otest
    ...            ${webapi_secret}=01000000d08c9ddf0115d1118c7a00c04fc297eb0100000082069e0d670de8479282c0a087c8e52a040000000800000046005300570000001066000000010000200000005fa9aff713c87a8e958513499b228d81f876657c7df7c2327c38a4afc0ac7080000000000e800000000200002000000059b25af195e1ddf2114925a642d6565ef820ca8615af380a65e8e887f8207808100000007b6cfc1ca108246eaad94ef4fb20bb3c4000000006ea8f31b7ddcb9e272696b2c2077a5de612d05a552983baea75c99c11de842a2ec6807e5670a2bbcaacb1836852128027b7db6f2353facab9feedc37f910b60
    ...            ${http_port}=8080
    ...            ${https}=true    #enable https connection
    ...            ${https_port}=8443
    ...            ${webapi_exclude_device}=false
    ...            ${max_rate}=100

    Execute Shell Command on Device    ${device}    command=echo ^<SRXes^> > C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<SRX address = '${ip}' description = '${name}' id = '${id}' ipv6_reports = '${ipv6}'^> >> C:\\srx_interface.xml    timeout=${150}
    Run Keyword If    "${webapi}" is "true"    Execute Shell Command on Device    ${device}    command=echo ^<webapi exclude_device_only = '${webapi_exclude_device}' http_port = '${http_port}' https = '${https}' https_port = '${https_port}' max_rate = '${max_rate}' timeout_ms = '' user = '${webapi_user}'^> >> C:\\srx_interface.xml    timeout=${150}
    Run Keyword If    "${webapi}" is "true"    Execute Shell Command on Device    ${device}    command=echo ^<password fswSpi1 = '{capi} 1,${webapi_secret}'^> >> C:\\srx_interface.xml    timeout=${150}
    Run Keyword If    "${webapi}" is "true"    Execute Shell Command on Device    ${device}    command=echo ^</password^> >> C:\\srx_interface.xml    timeout=${150}
    Run Keyword If    "${webapi}" is "true"    Execute Shell Command on Device    ${device}    command=echo ^</webapi^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<oAuth id = '${client_id}' token_lifetime = '${token_lifetime}'^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<password fswSpi1 = '{fsw} 1,${client_secret}'^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</password^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</oAuth^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<query cert_hash = '' response_timeout_ms = '2500'^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</query^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</SRX^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</SRXes^> >> C:\\srx_interface.xml    timeout=${150}
	sleep    5
    Execute Shell Command on Device    ${device}    command=more C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=move /Y C:\\srx_interface.xml cwd\\config\\    timeout=${150}
    Execute Shell Command on Device    ${device}    command=bin\\resetConfig.cmd    timeout=${150}

Add JIMS Event Source In Windows
    [Documentation]    Add Event Source on JIMS
    [Arguments]    ${device}=${jims0}
    ...            ${id}=DC1
    ...            ${name}=bjnet2
    ...            ${ip}=101.1.0.21
    ...            ${username}=Administrator
    ...            ${password}=Netscreen1
    ...            ${eventlog_catchup_time}=1
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"

    Execute Shell Command on Device    ${device}    command=echo ^<event_sources^> > C:\\event_log_reader.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<event_source id='${id}'^> >> C:\\event_log_reader.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<domain_controller username=^"${username}^" server=^"${ip}^" password=^"${password}^" initial_timespan=^"${eventlog_catchup_time}^"^> >> C:\\event_log_reader.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</domain_controller^> >> C:\\event_log_reader.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</event_source^> >> C:\\event_log_reader.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</event_sources^> >> C:\\event_log_reader.xml    timeout=${150}
	sleep    5
    Execute Shell Command on Device    ${device}    command=more C:\\event_log_reader.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=move /Y C:\\event_log_reader.xml cwd\\config\\    timeout=${150}
    Execute Shell Command on Device    ${device}    command=bin\\resetConfig.cmd    timeout=${150}


Add JIMS Active Directory In Windows
    [Documentation]    Add Active Directory on JIMS
    [Arguments]    ${device}=${jims0}
    ...            ${ip}=101.1.0.121
    ...            ${id}=DC1
    ...            ${name}=bjnet2
    ...            ${username}=Administrator
    ...            ${password}=Netscreen1
    ...            ${ssl}=off     # on  | off
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"

    Execute Shell Command on Device    ${device}    command=echo ^<user_info_sources^> > C:\\user_directory.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<user_info_source id='${id}'^> >> C:\\user_directory.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<active_directory username=^"${username}^" ssl=^"${ssl}^" server=^"${ip}^" priority=^"0^" password=^"${password}^"^> >> C:\\user_directory.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</active_directory^> >> C:\\user_directory.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</user_info_source^> >> C:\\user_directory.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</user_info_sources^> >> C:\\user_directory.xml    timeout=${150}
	sleep    5
    Execute Shell Command on Device    ${device}    command=more C:\\user_directory.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=move /Y C:\\user_directory.xml ${path}cwd\\config\\    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=bin\\resetConfig.cmd    timeout=${150}

Add JIMS Session Logoff Time In Windows
    [Documentation]    Add Session Logoff Time on JIMS
    [Arguments]    ${device}=${jims0}
    ...            ${logoff_time}=1440
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"

    Execute Shell Command on Device    ${device}    command=echo ^<cache^> > C:\\cache.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<config incomplete_timeout_ms = '0' probe_timeout = '${logoff_time}' state_timeout = '120'^> >> C:\\cache.xml    timeout=${150}
	Execute Shell Command on Device    ${device}    command=echo ^</config^> >> C:\\cache.xml    timeout=${150}
	Execute Shell Command on Device    ${device}    command=echo ^</cache^> >> C:\\cache.xml    timeout=${150}
	sleep    5
    Execute Shell Command on Device    ${device}    command=more C:\\cache.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=move /Y C:\\cache.xml cwd\\config\\    timeout=${150}
    Execute Shell Command on Device    ${device}    command=bin\\resetConfig.cmd    timeout=${150}

Check Windows DC Eventlog Tool
    [Documentation]    Check Whether Exist Eventlog Tool On DC
    [Arguments]    ${device}=${dc0}
    ...            ${path}=c:\\test\\
    ...            ${file}=SELG_RT.exe

    Execute Shell Command on Device    ${device}     command=cd ${path}    timeout=${150}
    ${result}    Execute Shell Command on Device    ${device}     command=dir    timeout=${150}
	Should Contain    ${result}    ${file}

Add JIMS SRX Clients Start In Windows
    [Documentation]    Add multi SRX clients on JIMS Start
    [Arguments]    ${device}=${jims0}

    Execute Shell Command on Device    ${device}    command=del C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<SRXes^> >> C:\\srx_interface.xml    timeout=${150}

Add JIMS SRX Clients Midbody In Windows
    [Documentation]    Add multi SRX clients on JIMS Midbody
    [Arguments]    ${device}=${jims0}
    ...            ${id}=srx0    #using different id when add more than two clients
    ...            ${ip}=101.1.0.21
    ...            ${name}=e02-18
    ...            ${client_id}=otest
    ...            ${client_secret}=c3eb4bc2fcf153aaf54aa3fcdc65ee615319769686153411e75774114890c8a71ee94933b8cd6973894c7a41334a098a
    ...            ${token_lifetime}=28800
    ...            ${ipv6}=false    #true | false enable or disable push ipv6 auth entry to DUT, default is false

    Execute Shell Command on Device    ${device}    command=echo ^<SRX address = '${ip}' description = '${name}' id = '${id}' ipv6_reports = '${ipv6}'^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<oAuth id = '${client_id}' token_lifetime = '${token_lifetime}'^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<password fswSpi1 = '{fsw} 1,${client_secret}'^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</password^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</oAuth^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<query cert_hash = '' response_timeout_ms = '2500'^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</query^> >> C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</SRX^> >> C:\\srx_interface.xml    timeout=${150}

Add JIMS SRX Clients End In Windows
    [Documentation]    Add multi SRX clients on JIMS End
    [Arguments]    ${device}=${jims0}
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"

    Execute Shell Command on Device    ${device}    command=echo ^</SRXes^> >> C:\\srx_interface.xml    timeout=${150}
    sleep    5
    Execute Shell Command on Device    ${device}    command=type C:\\srx_interface.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}cwd\\config\\    timeout=${150}
    Execute Shell Command on Device    ${device}    command=del srx_interface.xml.backup    timeout=${150}
    Execute Shell Command on Device    ${device}    command=ren srx_interface.xml srx_interface.xml.backup    timeout=${150}
    Execute Shell Command on Device    ${device}    command=copy C:\\srx_interface.xml srx_interface.xml /y    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=bin\\resetConfig.cmd    timeout=${150}

Add JIMS Client Https Connection In Windows
    [Documentation]    JIMS support IPv4 and IPv6 connection with SRX by using https method
    [Arguments]    ${device}=${jims0}
    ...            ${dual_stack}=true    #true | false ipv4 and ipv6 connection
    ...            ${ipv6}=true    #true | false if true just only support ipv6 connection
    ...            ${port}=443
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"

    Execute Shell Command on Device    ${device}    command=echo ^<xports^> >> C:\\clients_https.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<transport address = '' connections_per_thread = '1' disabled = 'false' dual_stack = '${dual_stack}' force_listen = 'true' id = 'clients_https' ipv6 = '${ipv6}' keep_alive = 'true' max_active_messengers = '1000' port = '${port}' port_environment_variable = 'JNPR_JIMS_SRX_PORT'^> >> C:\\clients_https.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</transport^> >> C:\\clients_https.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</xports^> >> C:\\clients_https.xml    timeout=${150}
    sleep    5
    Execute Shell Command on Device    ${device}    command=more C:\\clients_https.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=move /Y C:\\clients_https.xml ${path}cwd\\config\\    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=bin\\resetConfig.cmd    timeout=${150}

Add JIMS Client Http Connection In Windows
    [Documentation]    JIMS support IPv4 and IPv6 connection with SRX by using http method
    [Arguments]    ${device}=${jims0}
    ...            ${dual_stack}=true    #true | false ipv4 and ipv6 connection
    ...            ${ipv6}=true    #true | false  if true just only support ipv6 connection
    ...            ${port}=8082
    ...            ${path}="C:\\Program Files (x86)\\Juniper Networks\\Juniper Identity Management Service\\"

    Execute Shell Command on Device    ${device}    command=echo ^<xports^> >> C:\\clients_http.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^<transport address = '' connections_per_thread = '1' disabled = 'false' dual_stack = '${dual_stack}' force_listen = 'true' id = 'clients_http' ipv6 = '${ipv6}' keep_alive = 'true' max_active_messengers = '1000' port = '${port}' port_environment_variable = ''^> >> C:\\clients_http.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</transport^> >> C:\\clients_http.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=echo ^</xports^> >> C:\\clients_http.xml    timeout=${150}
    sleep    5
    Execute Shell Command on Device    ${device}    command=more C:\\clients_http.xml    timeout=${150}
    Execute Shell Command on Device    ${device}    command=move /Y C:\\clients_http.xml ${path}cwd\\config\\    timeout=${150}
    Execute Shell Command on Device    ${device}    command=cd ${path}    timeout=${150}
    Execute Shell Command on Device    ${device}    command=bin\\resetConfig.cmd    timeout=${150}