*** Settings ***
Documentation    Keyword Used to zeroize the system
...       Parameters 
...              :param resource: 
...		 **REQUIRED** resource name
...              :param user:
...		 	**OPTIONAL** Username. Default is root. Password to be given along with the user
...		 :param password:
...		 	**OPTIONAL** Password to the provided user. 
...		 :param re:
...		 	**OPTIONAL** routing engines to be zeroized. Default is dual
...				     supported values are dual and single
...		 :param cipher:
...		 	**OPTIONAL** validation of cipher keys. Default is no
...				     supported values are yes and no
...		 :param fips:
...			**OPTIONAL** whether the router in FIPS enable. Used for cipher validation. Default is no.
...				     supported values are yes and no
...		 :params config:
...			**OPTIONAL** Add the router configuration on the router after zeroization. Default is yes.
...				     supported values are yes and no.

Library    String
Resource   jnpr/toby/Master.robot
Library    DateTime

*** Variables ***
@{mem}    limit datasize unlimited    limit stacksize unlimited    limit memoryuse unlimited    limit descriptors unlimited    limit memorylocked unlimited
          ...    limit maxproc unlimited
${pass}    Embe1mpls

@{root_auth}    set system root-authentication plain-text-password    ${pass}    ${pass}

@{auto_image_upgrade}    delete chassis auto-image-upgrade

*** Keywords  ***
Zeroize Single RE
    [Arguments]   ${user}     ${password}   
    [Documentation]     Zeroize local RE 
    ${conip}=    Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re0']['con-ip']}
    ${model}=    Set Variable    ${t['resources']['r0']['system']['primary']['model']}
    ${device}=    connect to device   host=${conip}     model=${model}   connect_targets=console   user=${user}    password=${password}    connect_mode=telnet 
    Log to console     \n"Zeroizing.... This will take about 45 minutes.. Please Be patient"
    Execute CLI Command on Device     ${device}   command=request system zeroize local   pattern=warning:(.*)
    ${output} =     Execute CLI Command On Device     ${device}     command=yes    pattern=(.*)

Zeroize Dual RE
    [Arguments]    ${user}   ${password}
    [Documentation]    Zeroizes both REs given they have connection established
    ${conip}=    Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re0']['con-ip']}
    ${model}=    Set Variable    ${t['resources']['r0']['system']['primary']['model']}
    ${device}=    connect to device   host=${conip}     model=${model}   connect_targets=console   user=${user}    password=${password}    connect_mode=telnet
    Log to console    \n"Zeroizing.... This will take about 45 minutes.. Please Be patient"
    Execute CLI command on device     ${device}   command=request system zeroize    pattern=warning:(.*)
    ${output} =    Execute CLI Command On Device     ${device}     command=yes    pattern=(.*)

Calculate time
    [Arguments]    ${t1}    ${t2}
    [Documentation]     This keyword is used to calculate time taken for Zeroization
    ${g1}   ${g2}   ${g3}   should match regexp    ${t1}    \\d\\d\\d\\d(.*)\\s(.*)
    ${t1}    convert time   ${g3}
    ${t1}=    convert to integer    ${t1}
    ${g4}   ${g5}   ${g6}   should match regexp    ${t2}    \\d\\d\\d\\d(.*)\\s(.*)
    ${t2}    convert time   ${g6}
    ${t2}=    convert to integer    ${t2}
    ${td}=    Evaluate    ${t2}-${t1}
    ${time}=   convert time    ${td}    verbose
    [return]    ${time}

Create Dummy Files
    [Arguments]    ${device}
    [Documentation]    Create sample files on devices.
    Execute shell command on device    ${device}    command=touch /var/tmp/dummyfile1.txt
    Execute shell command on device    ${device}    command=touch /var/home/regress/dummyfile2.txt

Add router Config
    [Arguments]    ${resource}    ${config}
    [Documentation]    Adds saved config on device
    ${conip}=    Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re0']['con-ip']}
    ${conip_re1}=    Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re1']['con-ip']}
    ${model}=    Set Variable    ${t['resources']['r0']['system']['primary']['model']}
    @{commit}=    Create List    commit
    ${device}=    connect to device    host=${conip}     model=${model}    connect_targets=console    user=root    password=Embe1mpls    connect_mode=telnet

    @{load_config}    Create List     load override terminal
    @{r_config}    Create List     ${config}
    ${ctrl_d} =         Evaluate        chr(int(4))
    @{ctrl}    Create List    ${ctrl_d}
    Execute config command on device    ${device}    command_list=@{load_config}    pattern=(.*)end input(.*)
    Execute config command on device    ${device}    command_list=@{r_config}    pattern=(.*)
    Execute config command on device    ${device}    command_list=@{ctrl}
    ${output}    Execute config command on device    ${device}    command_list=@{commit}    pattern=(.*)
    
    ${device_re1}    connect to device    host=${conip_re1}     model=${model}    connect_targets=console    user=root    password=Embe1mpls    connect_mode=telnet
    Execute config command on device    ${device_re1}    command_list=@{load_config}    pattern=(.*)end input(.*)
    Execute config command on device    ${device_re1}    command_list=@{r_config}    pattern=(.*)
    Execute config command on device    ${device_re1}    command_list=@{ctrl}
    ${output}     Execute config command on device    ${device_re1}    command_list=@{commit}    pattern=(.*)

check for dummy files
    [Arguments]    ${device}
    [Documentation]    Check if sample files created by Create Dummy Files keywords exist
    Execute Shell command on device    ${device}    command=cd /var/tmp
    ${d1}=    Execute Shell command on device    ${device}    command=ls -l dummyfile1.txt
    Execute Shell command on device    ${device}    command=cd /var/home/regress
    ${d2}=    Execute Shell command on device    ${device}    command=ls -l dummyfile2.txt
    ${check}=   set variable if   'No such file' in '${d1}'    1    0
    ${check2}=   set variable if   'No such file' in '${d2}'    1    0
    Run Keyword If    ${check}==0 or ${check2}==0    Fail
    Log    \n No Dummy Files Found

Zeroize 
    [Arguments]    ${resource}   ${user}=root    ${password}=Embe1mpls   ${re}=dual   ${fips}=no    ${config}=yes
    [Documentation]    Zeroizes the device
    ${re}=     Convert to Lowercase    ${re}
    ${config}=    Convert to Lowercase    ${config}
    @{commit}=    Create List    commit    

    ${conip}=    Set Variable    ${t['resources']['r0']['system']['primary']['controllers']['re0']['con-ip']}
    ${model}=    Set Variable    ${t['resources']['r0']['system']['primary']['model']}
    ${device}=    connect to device   host=${conip}     model=${model}   connect_targets=console   user=${user}    password=${password}    connect_mode=telnet  

    Create Dummy Files    ${device}
    
    ${saved_config}=    Execute shell command on device    ${device}    command=cat /var/tmp/baseline-config.conf   
    ${show_config}=    Execute cli command on device    ${device}    command=show configuration
    ${router_conf}=    Set variable if   ${saved_config.startswith("cat:")}    ${show_config}    ${saved_config}
    
    ${t1}=    get time
    Run keyword If   '${re}'=='single'    Zeroize Single RE   ${user}     ${password} 
    ...   ELSE IF    '${re}'=='dual'      Zeroize Dual RE    ${user}    ${password}
    ...   ELSE     Fail   Error! : Invalid Keyword Argument 're' Passed: re = ${re}
    sleep    30m
    
    ${device}    connect to device    host=${conip}     model=${model}    connect_targets=console    user=root    password=Embe1mpls    connect_mode=telnet
    ${t2}=    get time
    ${time}=    Calculate time    ${t1}    ${t2}
    Log to console    Time taken to Zeroize : ${time}

    Run Keyword and Ignore Error    Execute config command on device    ${device}    command_list=@{root_auth}    pattern=(.*)password(.*)
    Run Keyword and Ignore Error    Execute config command on device    ${device}    command_list=@{auto_image_upgrade}       
    ${output} =    Execute config command on device    ${device}    command_list=@{commit}     pattern=(.*)


    check for dummy files    ${device}
    
    Run keyword If   '${config}'=='yes'   add router config    ${resource}    ${router_conf}
    ...    ELSE    Log to Console    Not adding Router Config
