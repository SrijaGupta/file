*** Settings ***
Documentation
...     Resource file containing basic keywords to related to verification engine.
...
...     This resource file contains keywords to verify all the checks with given
...     input yaml file and additional features like single line feature veriifcation

Library      jnpr/toby/engines/verification/verifyEngine.py


*** Variables ***


*** Keywords ***
Jvision Verify
        [Documentation]         Verifying JSON result data compare with DUT value online
        [Arguments]    &{kwargs}

        ${status} =  jvision to ve converter  &{kwargs}
        Should Be True  '${status}' == 'True'

Jvision Verify Offline
        [Documentation]         Verifying JSON result data compare user value in offline
        [Arguments]    &{kwargs}

        ${status} =  verify jvision records api    &{kwargs}
        Should Be True  '${status}' == 'True'

Jvision Verify Specific Checks
        [Documentation]         Verifying JSON result data compare user value in offline
        [Arguments]    &{kwargs}

        ${status} =  verify specific jvision records api    &{kwargs}
        Should Be True  '${status}' == 'True'

Jvision get offline specific info
        [Documentation]         retrieves JSON result data 
        [Arguments]    &{kwargs}

        ${status} =  verify specific jvision records api   is_get=True    &{kwargs}
        [Return]    ${status}

Jvision Verify Offline Specific Checks
        [Documentation]         Verifying JSON result data compare user value in offline
        [Arguments]    &{kwargs}

        ${status} =  verify specific jvision records api    &{kwargs}
        Should Be True  '${status}' == 'True'


