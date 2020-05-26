*** Settings ***
Documentation    Master resource file for Toby BBE
Library          jnpr.toby.bbe.bbeinit.BBEInit
Library          jnpr.toby.bbe.bbeconfig.BBEConfig
Library          jnpr.toby.bbe.bbeactions.BBEActions
Library          jnpr/toby/bbe/bbekeywords.py
Library          jnpr/toby/system/license/License.py
Library          OperatingSystem
Library          jnpr/toby/utils/utils.py

Resource         jnpr/toby/Master.robot
Resource         jnpr/toby/bbe/radius/radius.robot

*** Keywords ***
BBE Test Setup
    [Documentation]    Handles BBE test setup
    Initialize                            # toby initialize
    BBE Initialize    ${BBECONFIGFILE}    # bbe initialize with yaml ${BBECONFIGFILE}
    Configure bbe licenses                 # Configure default BBE licenses on Tomcat routers
    configure tomcat                      # Configure tomcat on tomcat tagged routers
    #BBE config                           # BBE configuration

Configure bbe licenses
    [Documentation]     configure BBE license
    [Arguments]     ${device}=${None}
    ${result} =     parse bbe license file      ${MX_LICENSE_FILE}
    run keyword and return if  ${result} == False    Log   skip configuring license, please make sure license installed on DUT before test
    ${routers} =    BBE Get Devices     device_tags=tomcat      id_only=True
    ${routerlist} =      create list  ${device}

    ${device} =    set variable if    ${device == None}   ${routers}     ${device}
    ${device} =     set variable if   ${device.__class__ is type(${routerlist})}   ${device}     ${routerlist}

    Log     device is @{device}
    ${all} =    create list  all
    :FOR    ${router}    IN      @{device}
    \   Log     router is ${router}
    \   ${time} =   Get Time    epoch
    \   ${filename} =   catenate  SEPARATOR=    /tmp/bbe_license_      ${time}     .txt
    \   Log     filename is ${filename}
    \   ${router_handle} =       Get Handle      resource=${router}
    \   ${router_model} =        get model for device    device=${router_handle}
    \   ${status} =      run keyword and return status   should start with     ${router_model}      mx      ignore_case=True
    \   run keyword if   ${status}  create file  ${filename}    content=${result['mx']}
    \   ${vmxstatus} =      run keyword and return status   should start with     ${router_model}      vmx      ignore_case=True
    \   ${verstat} =       run keyword if    ${vmxstatus}    utils.Check Version    device=${router_handle}    version=19.2    operator=ge
    \   run keyword if      ${vmxstatus} and not ${verstat}   create file  ${filename}    content=${result['vmx']}
    \   run keyword if      ${vmxstatus} and ${verstat}   create file  ${filename}    content=${result['vmx192']}
    \   run keyword if     '${router_model}' == 'MX104'    append to file    ${filename}    content=${\n}${\n}
    \   run keyword if     '${router_model}' == 'MX104'    append to file    ${filename}    content=${result['mx104']}
    \   upload file     ${router_handle}     local_file=${filename}     remote_file=${filename}
    \   delete license      device=${router_handle}     key_identifiers=${all}
    \   Log     remove local file ${filename}
    \   remove file     ${filename}
    \   add license file        ${router_handle}     filename=${filename}      expected_status=success

BBE Radius Setup

    [Documentation]   Radius setup
    [Arguments]    ${host_resource}=h0
    ...            ${vlan_id}=1
    ...            ${host_ip}=9.0.0.9
    ...            ${host_netmask}=24
    ...            ${loopback}=100.0.0.1
    ...            ${gateway-ip}=9.0.0.1
    ...            ${intf_name}=radius0

    Log To Console    \nRadius Setup

    ${host_handle} =      Get handle     resource=${host_resource}
    &{radius_intf} =    Get Interface    resource=${host_resource}    intf=${intf_name}
    ${radius_port} =    Get From Dictionary    ${radius_intf}     name
    Switch to superuser    device=${host_handle}
    Execute Shell Command On Device    device=${host_handle}    command=/sbin/ifconfig ${radius_port} up
    Execute Shell Command On Device    device=${host_handle}    command=/sbin/vconfig rem ${radius_port}.${vlan_id}
    Execute Shell Command On Device    device=${host_handle}    command=/sbin/vconfig add ${radius_port} ${vlan_id}
    Execute Shell Command On Device    device=${host_handle}    command=/sbin/ifconfig ${radius_port}.${vlan_id} ${host_ip} netmask ${host_netmask} up
    Execute Shell Command On Device    device=${host_handle}    command=/sbin/route add -host ${loopback} gw ${gateway-ip}

*** Variables ***
# To specify non-default conCeserfiguration file, set the following BBECONFIGFILE
#     variable to the desired BBE configuration file in your test suite robot file.
# If this variable is not set, there must be a default file named yourtest.cfg.yaml 
#     in the same directory as you test suite robot file yourtest.robot
# Donot remove this variable even if you don't use it. It's value is None which is desired.
${BBECONFIGFILE}
${MX_LICENSE_FILE}    /volume/labtools/lib/Testsuites/BRAS/bbe_license.yaml


