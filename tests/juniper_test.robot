***Settings***
Documentation    Example Test case
Suite Setup      Device Open Connection    ${device}
Suite Teardown   Device Close Connection   ${device}
Library    OperatingSystem
Library    /Users/srigupta/Desktop/NitaDemo/juniper_route/pybot_jrouter.py    user=jcluster    target=vsrx1    password=Juniper!1    WITH NAME    ${device}
Resource   /Users/srigupta/Desktop/NitaDemo/Test_Suites/device.txt
Resource    /Users/srigupta/Desktop/NitaDemo/Test_Suites/version_resources.txt
***Variables***
${device}    switch
${path}      /Users/srigupta/Desktop/NitaDemo/tests
***Test Case***
Hello World
    [Documentaion]    Example test
    [Tags]    example
    Should be equal    Hello,world!    Hello,world!
Check Software Version
    [Documentation]    Version check
    [Tags]    version
    Check Software Version    ${device}    ${OS_version}

