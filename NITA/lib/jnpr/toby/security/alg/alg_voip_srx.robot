*** Settings ***
Documentation   
...            This resource file is collection of SRX operation defined in VoIP ALG
...            
...            Author: Vincent Wang (wangdn@juniper.net)
...            
...            Keywords List:
...
...                Clear SRX ALG H323 Counter
...
...


*** Keywords ***
Clear SRX ALG H323 Counter
    [Documentation]    Execute cli command: clear security alg h323 counters
    [Arguments]    ${device}=${srx0}
    ...            ${node}=${None}
    
    Run Keyword If    "${node}" is not "${None}"    Execute cli command on device    ${device}    command=clear security alg h323 counters node ${node}
    ...       ELSE                                  Execute cli command on device    ${device}    command=clear security alg h323 counters