*** Settings ***
Documentation  Master Resource file for Toby common Keyword
...            This resource file is collection of all resource files defined
...            in common/basic function
...            
...            Author: Wentao Wu (wtwu@juniper.net)

#public Library/Resource will be used in all keyword
Library     Collections
Library     String
Library     ipaddress
Resource    jnpr/toby/Master.robot

#Resource will be used in common keyword
Resource    jnpr/toby/security/common/linux.robot
Resource    jnpr/toby/security/common/windows.robot
Resource    jnpr/toby/security/common/srx.robot

Library     jnpr/toby/security/common/common_srx.py
Library     jnpr/toby/security/common/common_windows.py
Library     jnpr/toby/security/common/common_linux.py

#library file for linux.robot
Library     jnpr/toby/utils/setup_server.py
Library     jnpr/toby/utils/linux/linux_tool.py

#Import SRX HA Keywords
Resource     jnpr/toby/security/HA/HA.robot

*** Keywords ***

