*** Settings ***
Resource       juniper/toby/bbe/bbemaster.robot
Suite Setup    BBE Test Setup
Library        bbevartest.py

*** Test Cases ***
Testcase 1 - bbevar get device
    ${device} =   bbevar get device
    Log    ${device}

Testcase 2 - bbevar get interface
    ${intf} =    bbevar get interface
    Log    ${intf}
Testcase 3 - bbevar get vrfs
    @{vrfs} =    bbevar get vrf
    Log    ${vrfs}[0]
Testcase 4 - bbevar get tr handle
    ${rth} =    bbevar get rt handle
    Log    ${rth}

#*** Variables ***
#${BBECONFIGFILE}    bbe1.yaml
