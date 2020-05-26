*** Settings ***
Documentation
...      Testsuite for JVISION
...      Author: Amarnath Kanadam (akanadam@juniper.net)

Library	   jvision.py
Library    jnpr/toby/engines/config/config.py
Library    jnpr/toby/init/init.py
Library    jnpr/toby/hldcl/device.py
Library    BuiltIn
Library    Collections
Library    String
Resource    jnpr/toby/hldcl/device.robot
Resource    jnpr/toby/engines/verification/verification.robot
Resource    jnpr/toby/hldcl/trafficgen/spirent/spirent.robot
Resource    jnpr/toby/Master.robot

Suite Setup  MyInit

*** Variables ***

${interface} =   eth1
${server_ip_address} =   120.1.1.180/24
${dut_ip_address} =  120.1.1.1/24
${db_measurement} =  hanoi
${sort_key} =  jkey

*** Test Cases ***

Start_Stop decoder
	Start Jvision decoder    server_handle=${h0}    decoder_type=grpc    decoder_command=python grpc_oc_db.py 

  Sleep    10s

	Stop Jvision decoder    server_handle=${h0}    decoder_type=grpc


*** Keywords ***

MyInit
    Set Log Level  DEBUG
    Initialize
    ${DECODER_PATH}=    Create Dictionary    grpc=/opt/jvision/grpc/oc/    udp=/opt/jvision/
    ${DECODER_PORT}=    Create Dictionary    grpc=4321    udp=1234
    ${h0} =  Get Handle    resource=h0
    Set Suite Variable  ${h0}
    jvision init    device=${h0}    interface=${interface}    server_ip_address=${server_ip_address}    dut_ip_address=${dut_ip_address}    decoder_path=${DECODER_PATH}    
    ...             decoder_port=${DECODER_PORT}    db_query_measure=${db_measurement}    db_sort_key=${sort_key}

