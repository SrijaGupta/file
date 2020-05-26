*** Settings ***
Documentation  Master Resource file for ALG Keyword
...            This resource file is collection of all resource files defined
...            in ALG
...            
...            Author: Vincent Wang (wangdn@juniper.net)

Resource    jnpr/toby/security/alg/alg_linux.robot
Resource    jnpr/toby/security/alg/alg_srx.robot
Resource    jnpr/toby/security/alg/alg_windows.robot

Resource    jnpr/toby/security/alg/alg_voip_linux.robot
Resource    jnpr/toby/security/alg/alg_voip_srx.robot
Resource    jnpr/toby/security/alg/alg_voip_windows.robot

Library     jnpr/toby/security/alg/alg_srx.py
Library     jnpr/toby/security/alg/alg_linux.py
Library     jnpr/toby/security/alg/alg_voip_linux.py

*** Keywords ***
