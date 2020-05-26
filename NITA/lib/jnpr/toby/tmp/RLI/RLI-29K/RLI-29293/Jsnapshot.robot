*** Settings ***
Documentation
...     Robot Keyword file for Executejsnap.py

Library     jnpr/toby/tmp/RLI/RLI-29K/RLI-29293/Jsnapshot.py

*** Keywords ***

Get PreSnapshot For Config File ${conf} With Identifier ${identifier} On ${target:[.*]$}
    [Documentation]     Get snapshot on the file, Jsnap server used is vm44-04-vhost-03
    ${status}=  Get Snapshot    resource=${target}  test=${conf}    identifier=${identifier}   tag=pre  server=vm44-04-vhost-03
    Should Be True  '${status}' == 'True'

Get PostSnapshot For Config File ${conf} With Identifier ${identifier} On ${target:[.*]$}
    [Documentation]     Get snapshot on the file, Jsnap server used is vm44-04-vhost-03
    ${status}=  Get Snapshot    resource=${target}  test=${conf}    identifier=${identifier}   tag=post  server=vm44-04-vhost-03
    Should Be True  '${status}' == 'True'

Compare Snapshot For Config File ${conf} With Identifier ${identifier} On ${target:[.*]$}
    [Documentation]     Compare snapshot on the file, Jsnap server used is vm44-04-vhost-03
    ${status}=  Check Snapshot  resource=${target}  test=${conf}    identifier=${identifier}   server=vm44-04-vhost-03
    Should Be True  '${status}' == 'True'

Compare Snapshot For Config File ${conf} With Identifier ${identifier} On ${target} nocleanup
    [Documentation]     Compare snapshot on the file
    ${status}=  Check Snapshot  resource=${target}  test=${conf}    identifier=${identifier}   server=vm44-04-vhost-03  clean_jsnap=0
    Should Be True  '${status}' == 'True'

Get PreSnapshot For Config File ${conf} With Identifier ${identifier} On ${target} Using Server ${server}$
    [Documentation]     Get snapshot on the file
    ${status}=  Get Snapshot    resource=${target}  test=${conf}    identifier=${identifier}   tag=pre  server=${server}
    Should Be True  '${status}' == 'True'

Get PostSnapshot For Config File ${conf} With Identifier ${identifier} On ${target} Using Server ${server}$
    [Documentation]     Get snapshot on the file
    ${status}=  Get Snapshot    resource=${target}  test=${conf}    identifier=${identifier}   tag=post  server=${server}
    Should Be True  '${status}' == 'True'

Compare Snapshot For Config File ${conf} With Identifier ${identifier} On ${target} Using Server ${server}$
    [Documentation]     Compare snapshot on the file
    ${status}=  Check Snapshot  resource=${target}  test=${conf}    identifier=${identifier}   server=${server}
    Should Be True  '${status}' == 'True'

Compare Snapshot For Config File ${conf} With Identifier ${identifier} On ${target} using Server ${server} nocleanup
    [Documentation]     Compare snapshot on the file
    ${status}=  Check Snapshot  resource=${target}  test=${conf}    identifier=${identifier}   server=${server}  clean_jsnap=0
    Should Be True  '${status}' == 'True'

Cleanup Jsnap With Identifier ${identifier}
    [Documentation]     CleaningUp Jsnap files
    ${status}=  Jsnap Cleanup   identifier=${identifier}    server=vm44-04-vhost-03
    Should Be True  '${status}' == 'True'

Get JSnapshot
    [Documentation]     Get Snapshot on the file using args
    [Arguments]      &{kwargs}
    ${status}=  Get Snapshot    &{kwargs}
    Should Be True  '${status}' == 'True'

Compare JSnapshot
    [Documentation]     Compare Snapshot on the file using args
    [Arguments]      &{kwargs}
    ${status}=  Check Snapshot  &{kwargs}
    Should Be True  '${status}' == 'True'
