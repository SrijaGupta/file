*** Settings ***
Resource  jnpr/toby/toby.robot
Library   Collections

Library   aamw_verification.py
Library   aamw_helper.py
Suite Setup    Initialize

*** Variables ***

*** Test Cases ***
AAMW VTY Prefix
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Get VTY CMD Prefix  srx_handle=${device_handle}

    Log    Result: ${res}
    Log to console  Result: ${res}
    Log    End

AAMW VTY Category Count
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Get VTY Category Cnt  srx_handle=${device_handle}

    Log    Result: ${res}
    Log to console  Result: ${res}
    Log    End

AAMW VTY Application Count
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Get VTY Application Cnt  srx_handle=${device_handle}

    Log    Result: ${res}
    Log to console  Result: ${res}
    Log    End

AAMW VTY Web Xlist Count
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Get VTY Web Xlist Cnt  srx_handle=${device_handle}

    Log    Result: ${res}
    Log to console  Result: ${res}
    Log    End