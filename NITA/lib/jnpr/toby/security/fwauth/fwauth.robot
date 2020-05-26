*** Settings ***
Documentation  Master Resource file for fwauth  Keyword
...            This resource file is collection of all resource files defined
...            in fwauth.
...            
...            Author: Linjing Liu (ljliu@juniper.net)

Resource    jnpr/toby/security/fwauth/fwauth_srx.robot
Resource    jnpr/toby/security/fwauth/fwauth_linux.robot
Library     jnpr/toby/security/fwauth/fwauth_srx.py

