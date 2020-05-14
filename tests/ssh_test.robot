***Settings***
Suite Setup    SSH Open Connection    ${device}
Suite Teardown    SSH Close Connection    ${device}
Library    /Users/srigupta/Desktop/NitaDemo/juniper_route/pybot_connections.py    user=northstar    password=Embe1mpls    target=10.102.164.218     port=22    log=${log}    WITH NAME    switch
Resources    /Users/srigupta/Desktop/NitaDemo/Test_Suites/device.txt
Resources    /Users/srigupta/Desktop/NitaDemo/Test_Suites/version_resources.txt

*** Variables ***
${log}    /dev/null

*** Test Case ***
SSH Version Check
    SSH Check Version    ${device}    {OS_version}

