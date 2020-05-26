*** Settings ***
Documentation    Keyword used to enable FIPS on router
...              Parameters
...              :param resource:
...		 	**REQUIRED** resource name
...		 :param boundary:
...		 	**OPTIONAL** Module on which FIPS needs to be enabled. Default is re
...				     Supported values are - re and chassis
...		 :param controller:
...			**OPTIONAL** Routing Engine on which the FIPS needs to be enabled. Default is re0
...				     Supported values are re0 and re1 in dual RE machine

Resource   jnpr/toby/Master.robot 
Resource   secure_copy_fips.robot

*** Variables ***

${pass}     Embe1mpls
${rpass}    MaRtInI
@{root_auth}     set system root-authentication plain-text-password    ${pass}    ${pass}
@{regress}     set groups global system login user regress class super-user authentication plain-text-password    ${rpass}    ${rpass}
@{comm}     commit
@{re_fips_level}      set system fips level 1
@{chassis_fips_level}     set system fips chassis level 1

*** Keywords ***

FIPS Image Install
    [Arguments]    ${device}
    [Documentation]   Install FIPS Image
    Execute shell command on device    ${device}    command= cd /var/tmp
    ${res}=    Execute shell command on device    ${device}    command=ls | grep fips-mode
    ${reslen}=    Get Length    ${res}
    ${image}=    set Variable If    ${reslen}>0    ${res}
    Run Keyword If    ${reslen}>0    Execute Cli command on device    ${device}       command=request system software add ${image}

Optional Fips
    [Arguments]    ${device}
    [Documentation]    Adds fips-mode package on occam 
    Execute CLI command on Device     ${device}       command=request system software add optional://fips-mode.tgz

Delete CSP IPSEC shared keys set passwords and enable fips
    [Arguments]    ${device}
    [Documentation]    Deletes unsupported CSPs 
    ${delete_csps}    Create List    delete groups global system root-authentication     delete groups global system radius-server     delete groups global system login user fregress    delete groups global system login user regress    delete interfaces    delete services
    Execute Config Command On Device     ${device}     command_list=@{delete_csps}
    Execute Config Command On Device     ${device}     command_list=@{root_auth}   pattern=(.*)password(.*)
    Execute Config Command On Device     ${device}     command_list=@{regress}    pattern=(.*)password(.*)
    Execute Config Command On Device     ${device}     command_list=@{re_fips_level}
    Execute Config Command On Device     ${device}     command_list=@{comm}     pattern=(.*)


Re Fips
    [Arguments]   ${conip}    ${model}
    [Documentation]    Enable FIPS mode on RE
    ${device}=    connect to device    host=${conip}    model=${model}     connect_targets=console     user=root    password=Embe1mpls    connect_mode=telnet
    ${image}=    secure copy Fips    ${device}
    Run Keyword if    '${image}'=='occam'    Optional Fips     ${device}
    ...    ELSE    FIPS Image Install    ${device}
    Delete CSP IPSEC shared keys set passwords and enable fips    ${device}
    Reboot Device    ${device}
    Log    Sleeping because Reboot device sometimes pre-maturely reports reboot success
    sleep    10m 

Fips Mode Enable
    [Documentation]    Enables FIPS mode on specified devices
    [Arguments]    ${resource}    ${boundary}=re    ${controller}=re0 
    ${boundary}=    convert to lowercase    ${boundary}
    ${re0-conip}=   Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re0']['con-ip']}
    ${model}=   Set Variable    ${t['resources']['r0']['system']['primary']['model']}
    ${re1-conip}=   Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re1']['con-ip']}
    
    Run keyword if    '${boundary}'=='re' and '${controller}'=='re0'    Re Fips    ${re0-conip}    ${model}
    ...    ELSE IF    '${boundary}'=='re' and '${controller}'=='re1'    Re Fips    ${re1-conip}    ${model}
    
