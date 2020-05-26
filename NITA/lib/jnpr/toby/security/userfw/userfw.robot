*** Settings ***
Documentation  Master Resource file for UserFW  Keyword
...            This resource file is collection of all resource files defined
...            in UserFW
...            
...            Author: Wentao Wu (wtwu@juniper.net)

Resource    jnpr/toby/security/userfw/userfw_windows.robot
Resource    jnpr/toby/security/userfw/userfw_linux.robot
Resource    jnpr/toby/security/userfw/userfw_srx.robot

Library     jnpr/toby/security/userfw/userfw_srx.py
Library     jnpr/toby/security/userfw/userfw_linux.py
Library     jnpr/toby/security/userfw/userfw_windows.py

*** Keywords ***

