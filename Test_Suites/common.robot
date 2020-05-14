*** Variables ***
${SUITE_DIRECTORY}                      /Users/srigupta/Desktop/NitaDemo/Test_Suites


*** Test Cases ***

T1.1: CHECK Device OPEN CONNECTION
    [Documentation]     Objective: Check there are no pending commits
    [Tags]  SYSTEM  COMMON  COMMITS PENDING
    Device Open Connection    devices=${devices}  file=${SUITE_DIRECTORY}/device.txt
