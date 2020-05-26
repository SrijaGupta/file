*** Settings ***
Resource  jnpr/toby/toby.robot
Library   Collections

Library   aamw_helper.py
Suite Setup    Initialize

*** Variables ***

*** Test Cases ***
AAMW Create New EICAR
    Log    Start

    ${device_handle} =  Get Handle  resource=h0

    Generate New EICAR File  device_handle=${device_handle}
    ${res}=     Execute Shell Command on Device    ${device_handle}     command=cat /var/www/html/new_eicar.exe
    Log to Console  ${res}
    Log    End
