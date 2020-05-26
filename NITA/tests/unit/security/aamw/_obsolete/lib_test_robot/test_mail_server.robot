*** Settings ***
Resource  jnpr/toby/toby.robot
Library   Collections

Library   aamw_server_init.py
Library   aamw_traffic_cmd.py
Suite Setup    Initialize

*** Variables ***

*** Test Cases ***
AAMW Mail Server Test
    Log    Start

    ${client_handle}=   Get Handle  resource=h0
    ${server_handle}=   Get Handle  resource=h1

    # SMTP/SMTPS/SMTP_TLS
    Init AAMW Linux     client_handle=${client_handle}  server_handle=${server_handle}  protocol=smtp
    @{test_user_list}=  Create List     test_usr_0     test_usr_1
    Send Email Traffic  client_handle=${client_handle}  server_handle=${server_handle}  protocol=smtp   sender=whatever@whatever.com    receiver_list=${test_user_list}     server_ip=14.0.0.1      subject=ThisIsATestingEmail

    # Fetch Email
    Fetch Mail  device_handle=${client_handle}  protocol=imap  host=14.0.0.1  user=test_usr_0  password=123456  mail_num=1

    Log    End