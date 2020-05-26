*** Settings ***
Resource  jnpr/toby/toby.robot
Library   Collections

Library   aamw_server_init.py
Library   aamw_traffic_cmd.py
Suite Setup    Initialize

*** Test Cases ***
AAMW HTTP Server Init test
    Log    Start

    ${client_handle}=   Get Handle  resource=h0
    ${server_handle}=   Get Handle  resource=h1

    Init AAMW Linux     client_handle=${client_handle}  server_handle=${server_handle}  protocol=http


    Log    End

AAMW Web traffic test
    Log    Start

    ${client_handle}=   Get Handle  resource=h0
    ${server_handle}=   Get Handle  resource=h1

    Send Web Traffic    device_handle=${client_handle}  protocol=http   host=eng-homes.juniper.net  file_name=~haochen
    Send Web Traffic    device_handle=${client_handle}  protocol=https   host=eng-homes.juniper.net  file_name=~haochen

    Log    End