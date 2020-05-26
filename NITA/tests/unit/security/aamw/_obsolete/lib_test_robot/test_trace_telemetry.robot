*** Settings ***
Resource  jnpr/toby/toby.robot
Library   Collections

Library   aamw_verification.py
Suite Setup    Initialize

*** Variables ***

*** Test Cases ***
AAMW Trace Telemetry JSON
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    ${res} =    Get Trace Telemetry Json  srx_handle=${device_handle}   trace_file_path=/var/log/argon_traces

    Log    Result: ${res}
    Log    End


AAMW Trace Telemetry Verification
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    @{key_list} =   Create List     aamw    http    objs_blocked
    ${res} =    Verify Telemetry Item  srx_handle=${device_handle}   trace_file_path=/var/log/argon_traces     key_list=${key_list}   exp_val=0

    Log    Result: ${res}
    Log    End


AAMW Trace Telemetry Verification Suppose to Fail
    Log    Start

    ${device_handle} =  Get Handle  resource=r0

    @{key_list} =   Create List     aamw    http    objs_blocked
    ${res} =    Verify Telemetry Item  srx_handle=${device_handle}   trace_file_path=/var/log/argon_traces     key_list=${key_list}   exp_val=20

    Log    Result: ${res}
    Log    End