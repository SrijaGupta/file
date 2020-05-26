*** Settings ***
Resource  jnpr/toby/toby.robot
Library   Collections

Library   aamw_verification.py
Library   aamw_helper.py
Suite Setup    Initialize

*** Variables ***

*** Test Cases ***
AAMW Get HA Dynamic Address
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Get HA Dynamic Address  srx_handle=${device_handle}     start_ip=1.228.203.66

    Log    Result: ${res}
    Log to console  Result: ${res}
    Log    End

AAMW Get HA IP in File
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Is IP in DB File  srx_handle=${device_handle}   ip=1.228.203.66

    Log    Result: ${res}
    Log to console  Result: ${res}
    Log    End

AAMW Verify IP in HA
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Verify IP in HA  srx_handle=${device_handle}    ip=1.228.203.66

    Log    Result: ${res}
    Log to console  Result: ${res}
    Log    End