*** Settings ***
Resource  jnpr/toby/toby.robot
Library   Collections

# Initialize UI API
Library   UIAPIClient.py   url=https://portal.dep4.argonqa.junipersecurity.net   email_addr=haochen@juniper.net   realm=haochen    pwd=ArgonTest123*

# Suite Setup    Initialize

*** Variables ***

*** Test Cases ***
UI API Test
    Log    Start

    # Change email action
    Set Email Action    smtp      tag-and-deliver

    # Update blacklist/whitelist
    Add One Xlist       category=ips   list_type=blacklist     server=15.1.2.3
    Delete One Xlist    category=ips   list_type=blacklist     server=15.1.2.3

    # Set Host Analyzer IP status
    Set HA IP Status    ip=13.0.0.1

    Log    End