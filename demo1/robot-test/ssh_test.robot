***Settings***
Suite Setup    SSH Open Connection    ${device}
Suite Teardown    SSH Close Connection    ${device}
Library     pybot_connections.py    user=jcluser    password=Juniper!1     target=vsrx1     port=22    log=${log}    WITH NAME    switch
Library     pybot_connections.py    user=jcluser    password=Juniper!1     target=vsrx2     port=22    log=${log}    WITH NAME    router
Resource    version_resources.txt

*** Variables ***
${log}    /dev/null

*** Test Case ***
SSH Version Check
    SSH Check Version    ${device}    {OS_version}

