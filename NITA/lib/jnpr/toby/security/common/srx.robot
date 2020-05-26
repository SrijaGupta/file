*** Setting ***
Documentation
...     This file contains all the robot common keyword for SRX
...
...     Author: Wentao Wu (wtwu@juniper.net)
...
...     Keyword list:
#...             Config SRX Static Route
#...             Delete SRX Static Route
#...             Config SRX Interface IP Address
...             Delete SRX Interface IP Address
...             Delete SRX Interfaces
...             Config SRX Interface Redundant Parent
...             Config SRX Interface Redundancy Group
...             Config SRX Chassic Cluster
...             Delete SRX Chassis Cluster
...             Config SRX Security Zone Interface
...             Delete SRX Security Zone
...             Config SRX Security Address-Book
...             Delete SRX Security Address-Book
...             Config SRX Security Address-Set
...             Config SRX Security Policies
...             Config SRX Security Policies User Identity
...             Config SRX Security Policies With AppFW
...             Delete SRX Security Policies
...             Delete SRX Security Policies User Identity
...             Delete SRX Services
...             Show SRX Configuration
...             Show SRX Security Policies Hit Count
...             Check SRX Security Policies Hit Count
...             Clear SRX Security Policies Hit Count
...             Clear SRX Trace Log
...             Check SRX Flow Session
...             Clear SRX Flow Session
...             Show SRX Flow Session
...             Check SRX Ping Result
...             Check SRX Ping Timeout Result
...             Check SRX Chassis Fpc Pic status
...             Get SRX Chassis Cluster Status
...             Get SRX Chassis Cluster Node Name
...             Get SRX Chassis Cluster Node ID
...             Set SRX Chassis Cluster Status
...             Kill SRX Process
...             Config SRX System Service
...             Delete SRX Configuration
...             Check SRX Primary Node In RG
...             Config SRX L2 Vlans
...             Config SRX L2 Protocols
...             Config SRX L2 Interface
...             Config SRX Syslog
...             Check SRX Syslog

*** Keywords ***
#Config SRX Interface IP Address
#    [Documentation]    Config SRX Interface IP address
#    [Arguments]    ${device}=${srx0}
#    ...            ${interface}=${tv['srx0__intf1__pic']}
#    ...            ${unit}=${tv['srx0__intf1__unit']}
#    ...            ${ip}=1.2.3.1
#    ...            ${mask}=24
#    ...            ${web_authentication}=${None}     #   http   |  https   |  redirect-to-https
#    ...            ${inet}=inet
#
#    @{cmd_list} =    Create List   ${EMPTY}
#    Run Keyword If    "${web_authentication}" is not "${None}"   Append To List    ${cmd_list}     set interfaces ${interface} unit ${unit} family ${inet} address ${ip}/${mask} web-authentication ${web_authentication}
#    ...       ELSE                                               Append To List    ${cmd_list}     set interfaces ${interface} unit ${unit} family ${inet} address ${ip}/${mask}
#    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX Interface Redundant Parent
    [Documentation]    Config SRX Interface Redundant Parent
    [Arguments]    ${device}=${srx0}
    ...            ${interface}=${tv['srx0__intf1__pic']}
    ...            ${reth_interface}=reth0

    @{cmd_list} =    Create List    set interfaces ${interface} gigether-options redundant-parent ${reth_interface}
    ...                             show interfaces ${interface} |display set
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX Interface Redundancy Group
    [Documentation]    Config SRX Interface Redundancy Group
    [Arguments]    ${device}=${srx0}
    ...            ${interface}=reth0
    ...            ${group}=1

    @{cmd_list} =    Create List    set interfaces ${interface} redundant-ether-options redundancy-group ${group}
    ...                             show interfaces ${interface} |display set
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX Chassis Cluster
    [Documentation]    Config SRX SRX Chassis Cluster
    [Arguments]    ${device}=${srx0}
    ...            ${reth_count}=${None}
    ...            ${redundancy_group}=0
    ...            ${node}=0
    ...            ${priority}=${None}
    ...            ${preempt}=${None}
    ...            ${interface_monitor}=${None}
    ...            ${ip_monitor}=${None}
    ...            ${hold_down_interval}=${None}
    ...            ${gratuitous_arp_count}=${None}
    ...            ${control_link_recovery}=${None}
    ...            ${heartbeat_interval}=${None}
    ...            ${heartbeat_threshold}=${None}
    ...            ${configuration_synchronize}=${None}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${reth_count}" is not "${None}"                   Append To List    ${cmd_list}    set chassis cluster reth-count ${reth_count}
    Run Keyword If    "${priority}" is not "${None}"                     Append To List    ${cmd_list}    set chassis cluster redundancy-group ${redundancy_group} node ${node} priority ${priority}
    Run Keyword If    "${preempt}" is not "${None}"                      Append To List    ${cmd_list}    set chassis cluster redundancy-group ${redundancy_group} preempt
    Run Keyword If    "${interface_monitor}" is not "${None}"            Append To List    ${cmd_list}    set chassis cluster redundancy-group ${redundancy_group} interface-monitor ${interface_monitor}
    Run Keyword If    "${ip_monitor}" is not "${None}"                   Append To List    ${cmd_list}    set chassis cluster redundancy-group ${redundancy_group} ip-monitor family inet ${ip_monitor}
    Run Keyword If    "${hold_down_interval}" is not "${None}"           Append To List    ${cmd_list}    set chassis cluster redundancy-group ${redundancy_group} hold-down-interval ${hold_down_interval}
    Run Keyword If    "${gratuitous_arp_count}" is not "${None}"         Append To List    ${cmd_list}    set chassis cluster redundancy-group ${redundancy_group} gratuitous-arp-count ${gratuitous_arp_count}
    Run Keyword If    "${control_link_recovery}" is not "${None}"        Append To List    ${cmd_list}    set chassis cluster control-link-recovery
    Run Keyword If    "${heartbeat_interval}" is not "${None}"           Append To List    ${cmd_list}    set chassis cluster heartbeat-interval ${heartbeat_interval}
    Run Keyword If    "${heartbeat_threshold}" is not "${None}"          Append To List    ${cmd_list}    set chassis cluster heartbeat-threshold ${heartbeat_threshold}
    Run Keyword If    "${configuration_synchronize}" is not "${None}"    Append To List    ${cmd_list}    set chassis cluster configuration-synchronize no-secondary-bootup-auto
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

#Config SRX Static Route
#    [Documentation]    Config SRX Static Route
#    [Arguments]    ${device}=${srx0}
#    ...            ${subnet}=0.0.0.0
#    ...            ${mask}=0.0.0.0
#    ...            ${nexthop}=1.2.3.1
#
#    @{cmd_list} =    Create List    set routing-options static route ${subnet}/${mask} next-hop ${nexthop}
#    ...                             show routing-options | display set
#    Execute Config Command On Device   ${device}     command_list=@{cmd_list}

Config SRX Security Zone Interface
    [Documentation]    Config SRX Security Zone Interface
    [Arguments]    ${device}=${srx0}
    ...            ${zone}=trust
    ...            ${interface}=${tv['srx0__intf1__name']}
    ...            ${logical_systems}=${None}

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    logical-systems ${logical_systems} security zones
    ...         ELSE                                            Set Variable    security zones
    Log    ==> prefix is: ${prefix}

    @{cmd_list} =    Create List    set ${prefix} security-zone ${zone} interfaces ${interface} host-inbound-traffic system-services all
    ...                             set ${prefix} security-zone ${zone} interfaces ${interface} host-inbound-traffic protocols all
    ...                             show ${prefix} security-zone ${zone} |display set
    Execute Config Command On Device   ${device}     command_list=@{cmd_list}

Config SRX Security Address-Book
    [Documentation]    Config SRX Security Address-Book
    [Arguments]    ${device}=${srx0}
    ...            ${address_book_name}=my-book-name
    ...            ${address_name}=my-addr-name
    ...            ${ip_prefix}=${None}
    ...            ${ip_start}=${None}
    ...            ${ip_end}=${None}
    ...            ${wildcard_address}=${None}
    ...            ${logical_systems}=${None}

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    logical-systems ${logical_systems} security address-book
    ...         ELSE                                            Set Variable    security address-book
    Log    ==> prefix is: ${prefix}
    @{cmd_list} =    Create List   ${EMPTY} 
    Run Keyword If   "${ip_prefix}" is not "${None}"             Append To List    ${cmd_list}    set ${prefix} ${address_book_name} address ${address_name} ${ip_prefix}
    Run Keyword If   "${ip_end}" is not "${None}"                Append To List    ${cmd_list}    set ${prefix} ${address_book_name} address ${address_name} range-address ${ip_start} to ${ip_end}
    Run Keyword If   "${wildcard_address}" is not "${None}"      Append To List    ${cmd_list}    set ${prefix} ${address_book_name} address ${address_name} wildcard-address ${wildcard_address}
    Append To List    ${cmd_list}    show ${prefix} ${address_book_name} address ${address_name} |display set
    Execute Config Command On Device   ${device}     command_list=@{cmd_list}

Config SRX Security Address-Set
    [Documentation]    Config SRX Security Address-Set
    [Arguments]    ${device}=${srx0}
    ...            ${address_book_name}=my-book-name
    ...            ${address_set_name}=my-set-name
    ...            ${address_name}=my-addr-name
   ...             ${mode}=address          #mode can be [address|address-set]

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${mode}" == "address-set"    Append To List    ${cmd_list}    set security address-book ${address_book_name} address-set ${address_set_name} address-set ${address_name}
    ...       ELSE                                  Append To List    ${cmd_list}    set security address-book ${address_book_name} address-set ${address_set_name} address ${address_name}
    Append To List    ${cmd_list}    show security address-book ${address_book_name} address-set ${address_set_name} |display set
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

Config SRX Security Policies
    [Documentation]    Config SRX Security Policies
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=p1
    ...            ${from_zone}=trust
    ...            ${to_zone}=untrust
    ...            ${src_address}=any
    ...            ${dst_address}=any
    ...            ${application}=any
    ...            ${action}=permit
    ...            ${end_user_profile}=${None}
    ...            ${domain}=${None}
    ...            ${source_id}=${None}
    ...            ${session_init}=${None}
    ...            ${session_close}=${None}
    ...            ${logical_systems}=${None}
    ...            ${default_policy}=${None}    #[permit-all | deny-all]
    ...            ${policy_rematch}=${True}

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    logical-systems ${logical_systems} security policies
    ...         ELSE                                            Set Variable    security policies
    Log    ==> prefix is: ${prefix}

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${src_address}" is not "${None}"             Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-address ${src_address}
    Run Keyword If    "${dst_address}" is not "${None}"             Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match destination-address ${dst_address}
    Run Keyword If    "${application}" is not "${None}"             Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match application ${application}
    Run Keyword If    "${action}" is not "${None}"                  Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then ${action}
    Run Keyword If    "${end_user_profile}" is not "${None}"        Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-end-user-profile ${end_user_profile}
    Run Keyword If    '${domain}' is not '${None}' and '${source_id}' is not '${None}'
    ...                                                             Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-identity "${domain}\\${source_id}"
    Run Keyword If    '${domain}' is '${None}' and '${source_id}' is not '${None}'
    ...                                                             Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-identity ${source_id}
    Run Keyword If    "${session_init}" is not "${None}"            Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then log session-init
    Run Keyword If    "${session_close}" is not "${None}"           Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then log session-close
    Run Keyword If    "${default_policy}" is not "${None}"          Append To List    ${cmd_list}    set ${prefix} default-policy ${default_policy}
    Run Keyword If    ${policy_rematch}                             Append To List    ${cmd_list}    set ${prefix} policy-rematch

    #display result in log
    Append To List    ${cmd_list}    show ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} |display set
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

Config SRX Security Policies User Identity
    [Documentation]    Config SRX Security Policies User Identity
    [Tags]    srx    security    policies    user    identity
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=p1
    ...            ${from_zone}=trust
    ...            ${to_zone}=untrust
    ...            ${domain}=test.com
    ...            ${source_id}=${None}
    ...            ${logical_systems}=${None}

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    logical-systems ${logical_systems} security policies
    ...         ELSE                                            Set Variable    security policies
    Log    ==> prefix is: ${prefix}

    ${cmd_list} =    Create List    ${EMPTY}
    :FOR    ${id}    IN    @{source_id}
    \    Append To List    ${cmd_list}    set ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-identity "${domain}\\${id}"
    #display result in log
    Append To List    ${cmd_list}    show ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} |display set
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

Config SRX Security Policies With AppFW
    [Documentation]    Config SRX Security Policies With AppFW
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=p1
    ...            ${from_zone}=trust
    ...            ${to_zone}=untrust
    ...            ${rule_set}=${None}

    ${cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${rule_set}" is not "${None}"                     Append To List    ${cmd_list}    set security policies from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then permit application-services application-firewall rule-set ${rule_set}
    Execute Config Command On Device   ${device}     command_list=${cmd_list}


Delete SRX Security Policies
    [Documentation]    Delete SRX Security Policies Config
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=${None}
    ...            ${from_zone}=${None}
    ...            ${to_zone}=${None}
    ...            ${src_address}=${None}
    ...            ${dst_address}=${None}
    ...            ${application}=${None}
    ...            ${application_all}=${None}
    ...            ${action}=${None}
    ...            ${end_user_profile}=${None}
    ...            ${domain}=${None}
    ...            ${source_id}=${None}
    ...            ${source_id_all}=${None}
    ...            ${session_init}=${None}
    ...            ${session_close}=${None}
    ...            ${logical_systems}=${None}
    ...            ${default_policy}=${None}    #[permit-all | deny-all]

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    logical-systems ${logical_systems} security policies
    ...         ELSE                                            Set Variable    security policies
    Log    ==> prefix is: ${prefix}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${action}" is not "${None}"              Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then ${action}
    ...    ELSE IF    "${session_init}" is not "${None}"        Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then log session-init
    ...    ELSE IF    "${session_close}" is not "${None}"       Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} then log session-close
    ...    ELSE IF    "${src_address}" is not "${None}"         Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-address ${src_address}
    ...    ELSE IF    "${dst_address}" is not "${None}"         Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match destination-address ${dst_address}
    ...    ELSE IF    "${application}" is not "${None}"         Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match application ${application}
    ...    ELSE IF    "${application_all}" is not "${None}"     Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match application
    ...    ELSE IF    "${domain}" is not "${None}"              Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-identity "${domain}\\${source_id}"
    ...    ELSE IF    "${source_id}" is not "${None}"           Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-identity ${source_id}
    ...    ELSE IF    "${source_id_all}" is not "${None}"       Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-identity
    ...    ELSE IF    "${end_user_profile}" is not "${None}"    Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-end-user-profile
    ...    ELSE IF    "${policy_name}" is not "${None}"         Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name}
    ...    ELSE IF    "${to_zone}" is not "${None}"             Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone}
    ...    ELSE IF    "${default_policy}" is not "${None}"      Append To List    ${cmd_list}    delete ${prefix} default-policy ${default_policy}
    ...       ELSE                                              Append To List    ${cmd_list}    delete ${prefix}
    #display result in log
    Append To List    ${cmd_list}    show ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} |display set
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

Delete SRX Security Policies User Identity
    [Documentation]    Delete SRX Security Policies User Identity
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=p1
    ...            ${from_zone}=trust
    ...            ${to_zone}=untrust
    ...            ${domain}=test.com
    ...            ${source_id}=${None}
    ...            ${logical_systems}=${None}

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    logical-systems ${logical_systems} security policies
    ...         ELSE                                            Set Variable    security policies
    Log    ==> prefix is: ${prefix}

    @{source_id} =   Run Keyword If    isinstance($source_id,list)     Copy List    ${source_id}
    ...                        ELSE                                  Create List    ${source_id}
    ${cmd_list} =    Create List    ${EMPTY}
    :FOR    ${id}    IN    @{source_id}
    \    Append To List    ${cmd_list}    delete ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} match source-identity "${domain}\\${id}"
    #display result in log
    Append To List    ${cmd_list}    show ${prefix} from-zone ${from_zone} to-zone ${to_zone} policy ${policy_name} |display set
    Execute Config Command On Device   ${device}     command_list=${cmd_list}

Delete SRX Services
    [Documentation]    Delete SRX Services Config
    [Arguments]    ${device}=${srx0}

    @{cmd_list} =    Create List    delete services
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Delete SRX Security Zone
    [Documentation]    Delete SRX Security Zone Config
    [Arguments]    ${device}=${srx0}

    @{cmd_list} =    Create List    delete security zone
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Delete SRX Security Address-Book
    [Documentation]    Delete SRX Security Address-Book Config
    [Arguments]    ${device}=${srx0}
    ...            ${address_book_name}=${None}
    ...            ${address_name}=${None}
    ...            ${address_set_name}=${None}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${address_book_name}" is not "${None}"    Append To List    ${cmd_list}    delete security address-book ${address_book_name}
    ...    ELSE IF    "${address_name}" is not "${None}"         Append To List    ${cmd_list}    delete security address-book ${address_book_name} address ${address_name}
    ...    ELSE IF    "${address_set_name}" is not "${None}"     Append To List    ${cmd_list}    delete security address-book ${address_book_name} address-set ${address_set_name}
    ...       ELSE                                               Append To List    ${cmd_list}    delete security address-book
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Delete SRX Configuration
    [Documentation]    Delete SRX Configuration
    [Arguments]    ${device}=${srx0}
    ...            ${item}=protocols

    @{cmd_list} =    Create List    ${EMPTY}
    Append To List    ${cmd_list}    delete ${item}

    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Delete SRX Interfaces
    [Documentation]    Delete SRX Interface Config
    [Arguments]    ${device}=${srx0}
    ...            ${interface}=${None}
    ...            ${unit}=${None}
    ...            ${logical_systems}=${None}

    ${prefix}=    Run Keyword If    "${logical_systems}" is not "${None}"    Set Variable    delete logical-systems ${logical_systems} interfaces
    ...         ELSE                                            Set Variable    delete interfaces
    Log    ==> prefix is: ${prefix}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${interface}" is not "${None}"                                        Append To List    ${cmd_list}    ${prefix} ${interface}
    ...    ELSE IF    "${interface}" is not "${None}" and "${unit}" is not "${None}"         Append To List    ${cmd_list}    ${prefix} ${interface} unit ${unit}
    ...       ELSE                                                                           Append To List    ${cmd_list}    ${prefix}
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Delete SRX Chassis Cluster
    [Documentation]    Delete SRX SRX Chassis Cluster
    [Arguments]    ${device}=${srx0}
    ...            ${reth_count}=${None}
    ...            ${redundancy_group}=${None}
    ...            ${node}=${None}
    ...            ${priority}=${None}
    ...            ${preempt}=${None}
    ...            ${interface_monitor}=${None}
    ...            ${ip_monitor}=${None}
    ...            ${hold_down_interval}=${None}
    ...            ${gratuitous_arp_count}=${None}
    ...            ${control_link_recovery}=${None}
    ...            ${heartbeat_interval}=${None}
    ...            ${heartbeat_threshold}=${None}
    ...            ${configuration_synchronize}=${None}

    @{cmd_list} =    Create List    ${EMPTY}
    Run Keyword If    "${reth_count}" is not "${None}"                   Append To List    ${cmd_list}    delete chassis cluster reth-count
    ...    ELSE IF    "${priority}" is not "${None}"                     Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group} node ${node} priority ${priority}
    ...    ELSE IF    "${node}" is not "${None}"                         Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group} node ${node}
    ...    ELSE IF   "${redundancy_group}" is not "${None}"              Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group}
    ...    ELSE IF    "${preempt}" is not "${None}"                      Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group} preempt
    ...    ELSE IF    "${interface_monitor}" is not "${None}"            Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group} interface-monitor ${interface_monitor}
    ...    ELSE IF    "${ip_monitor}" is not "${None}"                   Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group} ip-monitor family inet ${ip_monitor}
    ...    ELSE IF    "${hold_down_interval}" is not "${None}"           Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group} hold-down-interval ${hold_down_interval}
    ...    ELSE IF    "${gratuitous_arp_count}" is not "${None}"         Append To List    ${cmd_list}    delete chassis cluster redundancy-group ${redundancy_group} gratuitous-arp-count ${gratuitous_arp_count}
    ...    ELSE IF    "${control_link_recovery}" is not "${None}"        Append To List    ${cmd_list}    delete chassis cluster control-link-recovery
    ...    ELSE IF    "${heartbeat_interval}" is not "${None}"           Append To List    ${cmd_list}    delete chassis cluster heartbeat-interval ${heartbeat_interval}
    ...    ELSE IF    "${heartbeat_threshold}" is not "${None}"          Append To List    ${cmd_list}    delete chassis cluster heartbeat-threshold ${heartbeat_threshold}
    ...    ELSE IF    "${configuration_synchronize}" is not "${None}"    Append To List    ${cmd_list}    delete chassis cluster configuration-synchronize no-secondary-bootup-auto
    ...       ELSE                                                       Append To List    ${cmd_list}    delete chassis cluster
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

#Delete SRX Static Route
#    [Documentation]    Delete SRX Static Route Config
#    [Arguments]    ${device}=${srx0}
#    ...            ${subnet}=${None}
#    ...            ${mask}=${None}
#    ...            ${nexthop}=${None}
#
#
#    @{cmd_list} =    Create List    ${EMPTY}
#    Run Keyword If    "${nexthop}" is not "${None}"    Append To List    ${cmd_list}    delete routing-options static route ${subnet}/${mask} next-hop ${nexthop}
#    ...    ELSE IF    "${mask}" is not "${None}"       Append To List    ${cmd_list}    delete routing-options static route ${subnet}/${mask}
#    ...       ELSE                                     Append To List    ${cmd_list}    delete routing-options static
#    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Delete SRX Interface IP Address
    [Documentation]    Delete SRX Interface IP address
    [Arguments]    ${device}=${srx0}
    ...            ${interface}=${tv['srx0__intf1__pic']}
    ...            ${unit}=${tv['srx0__intf1__unit']}
    ...            ${ip}=1.2.3.4
    ...            ${mask}=255.255.255.0

    @{cmd_list} =    Create List    delete interfaces ${interface} unit ${unit} family inet address ${ip}/${mask}
    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Show SRX Configuration
    [Documentation]    Check SRX Configuration
    [Arguments]    ${device}=${srx0}
    Execute Cli Command On Device    ${device}     command=show configuration |display set |except groups

Show SRX Security Policies Hit Count
    [Documentation]    show policied hit-count  on SRX device
    [Arguments]    ${device}=${srx0}
    Execute Cli Command On Device    ${device}     command=show security policies hit-count

Check SRX Security Policies Hit Count
    [Documentation]    Check SRX Security Policies Hit Count
    [Arguments]    ${device}=${srx0}
    ...            ${policy_name}=p1
    ...            ${count}=1
    ...            ${from_zone}=${None}
    ...            ${to_zone}=${None}
    ${result}    Execute cli command on device    ${device}    command=show security policies hit-count | match ${policy_name}
    Run Keyword If    "${from_zone}" is not "${None}"     Should Match Regexp    ${result}    ${from_zone}\\s+${to_zone}\\s+${policy_name}\\s+${count}
    ...      ELSE                                         Should Match Regexp    ${result}    ${policy_name}\\s+${count}

Check SRX Ping Result
    [Documentation]    Do ping to check the connection on SRX device
    [Arguments]    ${device}=${srx0}
    ...            ${ip}=1.2.3.4
    ...            ${count}=2
    ${result}    Execute Shell Command on Device    ${device}     command=ping -c ${count} ${ip}
    Should Not Match Regexp    ${result}    100%\\s+packet\\s+loss
#    Should Match Regexp        ${result}    ttl=\\d+

Check SRX Ping Timeout Result
    [Documentation]    Do ping to check the connection on SRX device
    [Arguments]    ${device}=${srx0}
    ...            ${ip}=1.2.3.4
    ...            ${count}=2
    ${result}    Execute Shell Command on Device    ${device}     command=ping -c ${count} ${ip}
    Should Not Match Regexp    ${result}    ttl=\\d+
    Should Match Regexp        ${result}    100%\\s+packet\\s+loss

Get SRX Chassis Cluster Status
    [Documentation]   Get SRX Standalone/HA mode
    ...               return    1     HA mode
    ...               return    0     Standalone mode
    [Arguments]    ${device}=${srx0}
    ${result}    Execute Cli Command on Device    ${device}     command=show chassis cluster status
    Return From Keyword If    'cluster is not enabled' in '''${result}'''    ${0}
    Return From Keyword If    'command is not valid' in '''${result}'''    ${0}
    Return From Keyword       ${1}

Get SRX Chassis Cluster Node Name
    [Documentation]   Get SRX Chassis Cluster Node Name
    ...               return    node0     #node name
    ...               return    node1     #node name
    [Arguments]    ${device}=${srx0}
    ...            ${rg}=0
    ...            ${status}=primary
    [Return]       ${result}
    ${result} =    Get HA Node Name    device=${device}    rg=${rg}    status=${status}

Get SRX Chassis Cluster Node ID
    [Documentation]   Get SRX Chassis Cluster Node ID
    ...               return    1     #node id 1
    ...               return    0     #node id 0
    [Arguments]    ${device}=${srx0}
    ...            ${rg}=0
    ...            ${status}=primary
    ${result} =    Get HA Node Name    device=${device}    rg=${rg}    status=${status}
    Return From Keyword If    'node0' in '''${result}'''    ${0}
    Return From Keyword       ${1}

Set SRX Chassis Cluster Status
    [Documentation]    Set SRX Chassis Cluster Status
    [Arguments]    ${device}=${srx0}
    ...            ${rg}=0
    ...            ${node}=0
    ${result} =    Get HA Node Name    device=${device}    rg=${rg}    status=primary
    Run Keyword If    "${node}" in "${result}"    Log    $result is primary node
    ...       ELSE               Do Manual Failover    ${device}    rg=${rg}

Check SRX Chassis Fpc Pic status
    [Documentation]    Check SRX Chassis Fpc Pic status
    [Arguments]    ${device}=${srx0}
    ${result}    Execute Cli Command on Device    ${device}     command=show chassis fpc pic-status
    Should Not Match Regexp    ${result}    (Offline|Ready|Present)

Clear SRX Security Policies Hit Count
    [Documentation]    Clear SRX Security Policies Hit Count
    [Arguments]    ${device}=${srx0}
    Execute cli command on device    ${device}    command=clear security policies hit-count

Kill SRX Process
    [Documentation]    Kill SRX Process
    [Arguments]   ${device}=${srx0}
    ...           ${process}=useridd
    ...           ${path}=/usr/sbin/
    ...           ${user}=root

    ${result}    Execute shell command on device    ${device}    command=ps aux |grep ${process}
    ${match_result}    ${pid}
    ...          Should Match Regexp      ${result}    (?i)${user}\\s+(\\d+)\\s+.*?${path}${process}
    Log    ==> Found process ${process} pid is: ${pid}
    Execute shell command on device    ${device}    command=kill -9 ${pid}

Clear SRX Trace Log
    [Documentation]    Clear SRX Trace Log
    [Arguments]    ${device}=${srx0}
    ...            ${file}=jims_log

    Execute cli command on device    ${device}    command=clear log ${file}

Config SRX System Service
    [Documentation]    Config SRX System Service
    [Arguments]   ${device}=${srx0}
    ...           ${service}=${None}    # ftp | telnet | http | https
    @{cmd_list} =    Create List   ${EMPTY}
    Run Keyword If    "${service}" is not"${None}"   Append To List    ${cmd_list}    set system services ${service}
    ...       ELSE                                   Append To List    ${cmd_list}    set system services
    Execute config command on device    ${device}    command_list=@{cmd_list}

Check SRX Flow Session
    [Documentation]    Check Flow Session On SRX
    [Arguments]    ${device}=${srx0}
    ...            ${source}=1.2.3.4
    ...            ${dst}=4.3.2.1
    ...            ${dst_port}=23
    ...            ${policy}=mypolicy1
    ...            ${protocol}=tcp
    ...            ${node}=${None}       #   0   |   1
    ...            ${logical_system}=${None}
    ...            ${have_session}=${True}

    ${prefix}=    Run Keyword If    "${logical_system}" is not "${None}"    Set Variable    show security flow session source-prefix ${source} logical-system ${logical_system}
    ...         ELSE                                            Set Variable    show security flow session source-prefix ${source}
    Log    ==> prefix is: ${prefix}

    ${result} =    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=${prefix} node ${node}
    ...                      ELSE                          Execute Cli Command On Device    ${device}    command=${prefix}

    Run Keyword If    ${have_session}   Should Match Regexp    ${result}    (?is)Session\\s*ID:\\s*\\d+,\\s*Policy\\s*name:\\s*${policy}/\\d*.*?In:\\s*${source}/\\d*\\s*-->\\s*${dst}/${dst_port};${protocol}.*?Out:\\s*${dst}/${dst_port}\\s*-->\\s*${source}/\\d*;${protocol}
    ...                      ELSE             Should Match Regexp    ${result}    (?is)Total sessions: 0

Clear SRX Flow Session
    [Documentation]    Execute cli command: clear security flow session
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
    ...            ${src_prefix}=${None}
    ...            ${dst_prefix}={None}

    ${cmd_list}=    Set Variable    clear security flow session
    Run Keyword If    "${node}" is not "${None}"    Catenate    ${cmd_list}   node ${node}
    Run Keyword If    "{src_prefix}" is not "${None}"    Catenate    ${cmd_list}    source-prefix ${src_prefix}
    Run Keyword If    "{dst_prefix}" is not "${None}"    Catenate    ${cmd_list}    destination-prefix ${dst_prefix}
    Execute cli command on device    ${device}    command=${cmd_list}

Show SRX Flow Session
    [Documentation]    Execute cli command: show security flow session
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}

    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=show security flow session node ${node} | no-more
    ...       ELSE                                  Execute cli command on device    ${device}    command=show security flow session | no-more


Check SRX Primary Node In RG
    [Documentation]    Check SRX Primary Node In RG
    [Arguments]    ${device}=${srx0}
    ...            ${group}=0
    ...            ${primary_node}=node0

    ${response}    Execute cli command on device    ${device}    command=show chassis cluster status redundancy-group ${group}
    Should Match Regexp     ${response}     (?i)${primary_node}\\s+\\d+\\s+primary\\s+

Config SRX L2 Vlans
    [Documentation]    Config SRX L2 Vlans
    [Arguments]    ${device}=${srx0}
    ...            ${bd_vlan}=${None}
    ...            ${vlan_id}=${None}

    @{cmd_list} =    Create List   ${EMPTY}
    Run Keyword If    "${vlan_id}" is not "${None}"               Append To List    ${cmd_list}     set vlans ${bd_vlan} vlan-id ${vlan_id}
    Run Keyword If    "${bd_vlan}" is not "${None}"               Append To List    ${cmd_list}     set vlans ${bd_vlan} l3-interface irb.0

    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX L2 Protocols
    [Documentation]    Config SRX L2 Protocols
    [Arguments]    ${device}=${srx0}

    @{cmd_list} =    Create List   ${EMPTY}
    Append To List    ${cmd_list}     set protocols l2-learning global-mode transparent-bridge

    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX L2 Interface
    [Documentation]    Config SRX L2 Interface
    [Arguments]    ${device}=${srx0}
    ...            ${unit}=0
    ...            ${ip}=${None}
    ...            ${mask}=24
    ...            ${inet}=inet
    ...            ${reth_interface}={None}
    ...            ${mode}=${None}
    ...            ${bd_vlan}=${None}
    ...            ${vlan_id}=${None}
    ...            ${irb}=${None}

    @{cmd_list} =    Create List   ${EMPTY}
    Run Keyword If    "${ip}" is not "${None}"            Append To List    ${cmd_list}     set interfaces irb unit ${unit} family ${inet} address ${ip}/${mask}
    Run Keyword If    "${mode}" is not "${None}"          Append To List    ${cmd_list}     set interfaces ${reth_interface} unit ${unit} family ethernet-switching interface-mode ${mode}
    Run Keyword If    "${bd_vlan}" is not "${None}"       Append To List    ${cmd_list}     set interfaces ${reth_interface} unit ${unit} family ethernet-switching vlan members ${bd_vlan}
    Run Keyword If    "${vlan_id}" is not "${None}"       Append To List    ${cmd_list}     set vlans ${bd_vlan} vlan-id ${vlan_id}
    Run Keyword If    "${irb}" is not "${None}"           Append To List    ${cmd_list}     set vlans ${bd_vlan} l3-interface irb.0

    Execute Config Command On Device    ${device}     command_list=@{cmd_list}

Config SRX Syslog
    [Documentation]    Config SRX Syslog
    [Arguments]    ${device}=${srx0}
    ...            ${file}=${None}

    @{cmd_list} =    Create List    set system syslog file ${file} any any
    ...                             set system syslog file ${file} structured-data
    ...                             set security log mode event
    ...                             run show configuration | display set | match syslog
    Execute Config Command On Device   ${device}     command_list=@{cmd_list}

Check SRX Syslog
    [Documentation]    Check Syslog
    [Arguments]    ${device}=${srx0}
    ...            ${log_type}=create
    ...            ${policy}=policy1
    ...            ${src_address}=${None}
    ...            ${dst_address}=${None}
    ...            ${domain}=${EMPTY}
    ...            ${user}=UNKNOWN
    ...            ${role}=${None}
    ...            ${application}=UNKNOWN
    ...            ${nested_application}=UNKNOWN
    ...            ${file}=${None}
    ...            ${type}=${None}      #    jims    |   cp

    ${response}    Execute cli command on device    ${device}    command=show log ${file} | match rt_flow_session_${log_type}
    Run Keyword If    "${policy}" is not "${None}"                 Should Match Regexp    ${response}    policy-name="${policy}"
    Run Keyword If    "${application}" is not "${None}"            Should Match Regexp    ${response}    application="${application}"
    Run Keyword If    "${nested_application}" is not "${None}"     Should Match Regexp    ${response}    nested-application="${nested_application}"
    Run Keyword If    "${domain}" is not "${None}"                 Should Match Regexp    ${response}    username=.${domain}
    Run Keyword If    "${user}" is not "${None}"                   Should Match Regexp    ${response}    username=.*?${user}

    @{role} =   Run Keyword If    isinstance($role,list)     Copy List    ${role}
    ...                   ELSE                             Create List    ${role}
    :FOR    ${arg}    IN    @{role}
    \    Should Match Regexp    ${response}    roles=.*?${arg}

    Log    ==> Original user: ${user}
    ${new_user}=    Replace String    ${user}    ${user}    ${domain}\\\\\\\\${user}
    Log    ==> New user: ${new_user}
    ${user}=    Run Keyword If    "${type}" is not "${None}"    Set Variable    ${new_user}
    ...         ELSE                                            Set Variable    ${user}
    Log    ==> the latest user: ${user}

    Log    ==> Found ip: ${src_address} ${dst_address}
    ${response}    Execute cli command on device    ${device}    command=show log ${file} | match rt_flow_session_${log_type}
    ${match_result}    ${source_address}    ${destination_address}
    ...          Should Match Regexp      ${response}    (?i)source\-address=\"(.*?)\".*?destination\-address=\"(.*?)\".*?policy\-name=\"${policy}\".*?username=\"${user}\"

    Log    ==> Found source ip result: ${source_address}
    Log    ==> Found des ip result: ${destination_address}
    ${match_src_ip}=    ipaddress.IP Address    ${source_address}
    ${match_des_ip}=    ipaddress.IP Address    ${destination_address}

    Log    ==> Found ip result: ${match_src_ip} ${match_des_ip}
    ${result}     CMP IP    ${src_address}    ${match_src_ip}
    Should Be True    ${result}    ${TRUE}

    ${result}     CMP IP    ${dst_address}    ${match_des_ip}
    Should Be True    ${result}    ${TRUE}

