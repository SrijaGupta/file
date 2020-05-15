***Settings***
Documentation    Example Test case
Suite Setup      Device Open Connection    ${device}
Suite Teardown   Device Close Connection   ${device}
Library    OperatingSystem
Library    pybot_jrouter.py    user=jcluser    target=vsrx1   password=Juniper!1    WITH NAME    vsrx1
Library    pybot_jrouter.py    user=jcluser    target=vsrx2   password=Juniper!1    WITH NAME    vsrx2
Resource   device.txt
Resource   version_resources.txt
***Variables***
${device}    vsrx1
${device}    vsrx2
${path}      robot-test
***Test Case***
Hello World
    [Documentation]    Example test
    [Tags]    example
    Should be equal    Hello,world!    Hello,world!
Check Software Version
    [Documentation]    Version check
    [Tags]    version
    Check Software Version    ${device}    ${OS_version}

