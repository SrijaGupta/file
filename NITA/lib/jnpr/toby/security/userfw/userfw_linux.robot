*** Settings ***
Documentation   
...              Master Resource file for Toby Keyword
...              This resource file is collection of all resource files defined
...              in UserFW Linux PC
...              
...              Author: Wentao Wu (wtwu@juniper.net)
...              
...              Keywords List:
...                     Add JIMS SRX Client From Linux
...                     Add JIMS Event Source From Linux
...                     Add JIMS Active Directory From Linux
...                     Add JIMS Session Logoff Time From Linux
...                     Send Linux Web-redirect Auth Traffic 

*** Keywords ***
Add JIMS Session Logoff Time From Linux
    [Documentation]    Add JIMS Session Logoff Time From Linux
    [Arguments]    ${device}=${linux0}
    ...            ${jims_ip}=10.208.164.71
    ...            ${logoff_time}=60
    ...            ${jims_username}=Administrator
    ...            ${jims_password}=Netscreen1
    ...            ${jims_port}=1505

    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    Execute Shell Command on Device    ${device}    command=cd /var/tmp
    Execute Shell Command on Device    ${device}    command=rm -rf srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<?xml version=\"1.0\"?>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<cache>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<config probe_timeout="${logoff_time}" state_timeout="120" incomplete_timeout_ms="0"/>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '</cache>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=more /var/tmp/srx_interface.xml
    Log    ==!!! Linux curl MUST suport --tlsv1.2 option
    ${result}    Execute Shell Command on Device    ${device}    command=curl --insecure --tlsv1.2 -u ${jims_username}:${jims_password} -X PUT -d "@srx_interface.xml" https://${jims_ip}:${jims_port}/config/cache -v
    Should Contain    ${result}    HTTP/1.1 200 OK	
	
Add JIMS SRX Client From Linux
    [Documentation]    Add JIMS SRX Client From Linux
    [Arguments]    ${device}=${linux0}
    ...            ${srx_id}=SRX1
    ...            ${srx_name}=e03-39
    ...            ${srx_ip}=10.208.164.70
    ...            ${client_id}=otest
    ...            ${client_secret}=c3eb4bc2fcf153aaf54aa3fcdc65ee615319769686153411e75774114890c8a71ee94933b8cd6973894c7a41334a098a
    ...            ${token_lifetime}=28800
    ...            ${jims_ip}=10.208.164.71
    ...            ${jims_username}=Administrator
    ...            ${jims_password}=Netscreen1
    ...            ${jims_port}=1505

    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    Execute Shell Command on Device    ${device}    command=cd /var/tmp
    Execute Shell Command on Device    ${device}    command=rm -rf srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<?xml version=\"1.0\"?>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<SRXes>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<SRX id="${srx_id}" description="${srx_name}" address="${srx_ip}">' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<oAuth id="${client_id}" token_lifetime="${token_lifetime}">' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<password fswSpi1="{fsw} 1,${client_secret}"> </password>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '</oAuth>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '<query response_timeout_ms="2500" cert_hash=""> </query>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '</SRX>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=echo '</SRXes>' >> srx_interface.xml
    Execute Shell Command on Device    ${device}    command=more /var/tmp/srx_interface.xml
    Log    ==!!! Linux curl MUST suport --tlsv1.2 option
    ${result}    Execute Shell Command on Device    ${device}    command=curl --insecure --tlsv1.2 -u ${jims_username}:${jims_password} -X PUT -d "@srx_interface.xml" https://${jims_ip}:${jims_port}/config/srx_interface -v
    Should Contain    ${result}    HTTP/1.1 200 OK
	
Add JIMS Event Source From Linux
    [Documentation]    Add JIMS Event Source From Linux
    [Arguments]    ${device}=${linux0}
    ...            ${dc_id}=DC1
    ...            ${dc_name}=bjnet2
    ...            ${dc_ip}=10.208.164.70
    ...            ${dc_username}=Administrator
    ...            ${dc_password}=Netscreen1
    ...            ${start_event_time}=1
    ...            ${jims_ip}=10.208.164.71
    ...            ${jims_username}=Administrator
    ...            ${jims_password}=Netscreen1
    ...            ${jims_port}=1505

    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    Execute Shell Command on Device    ${device}    command=cd /var/tmp
    Execute Shell Command on Device    ${device}    command=rm -rf event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=echo '<?xml version="1.0"?>' >> event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=echo '<event_sources>' >> event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=echo '<event_source description="${dc_name}" id="${dc_id}">' >> event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=echo '<domain_controller username="${dc_username}" server="${dc_ip}" password="${dc_password}" initial_timespan="${start_event_time}">' >> event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=echo '</domain_controller>' >> event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=echo '</event_source>' >> event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=echo '</event_sources>' >> event_log_reader.xml
    Execute Shell Command on Device    ${device}    command=more /var/tmp/event_log_reader.xml
    Log    ==!!! Linux curl MUST suport --tlsv1.2 option
    ${result}    Execute Shell Command on Device    ${device}    command=curl --insecure --tlsv1.2 -u ${jims_username}:${jims_password} -X PUT -d "@event_log_reader.xml" https://${jims_ip}:${jims_port}/config/event_log_reader -v
    Should Contain    ${result}    HTTP/1.1 200 OK
	
Add JIMS Active Directory From Linux
    [Documentation]    Add JIMS Active Directory Source From Linux
    [Arguments]    ${device}=${linux0}
    ...            ${dc_id}=AD1
    ...            ${dc_name}=mydc
    ...            ${dc_ip}=10.208.164.70
    ...            ${dc_username}=Administrator
    ...            ${dc_password}=Netscreen1
    ...            ${jims_ip}=10.208.164.71
    ...            ${jims_username}=Administrator
    ...            ${jims_password}=Netscreen1
    ...            ${jims_port}=1505

    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    Execute Shell Command on Device    ${device}    command=cd /var/tmp
    Execute Shell Command on Device    ${device}    command=rm -rf user_directory.xml
    Execute Shell Command on Device    ${device}    command=echo '<?xml version="1.0"?>' >> user_directory.xml
    Execute Shell Command on Device    ${device}    command=echo '<user_info_sources>' >> user_directory.xml
    Execute Shell Command on Device    ${device}    command=echo '<user_info_source description="${dc_name}" id="${dc_id}">' >> user_directory.xml
    Execute Shell Command on Device    ${device}    command=echo '<active_directory username="${dc_username}" ssl="off" server="${dc_ip}" priority="0" password="${dc_password}">' >> user_directory.xml
    Execute Shell Command on Device    ${device}    command=echo '</active_directory>' >> user_directory.xml
    Execute Shell Command on Device    ${device}    command=echo '</user_info_source>' >> user_directory.xml
    Execute Shell Command on Device    ${device}    command=echo '</user_info_sources>' >> user_directory.xml
    Execute Shell Command on Device    ${device}    command=more /var/tmp/user_directory.xml
    Log    ==!!! Linux curl MUST suport --tlsv1.2 option
    ${result}    Execute Shell Command on Device    ${device}    command=curl --insecure --tlsv1.2 -u ${jims_username}:${jims_password} -X PUT -d "@user_directory.xml" https://${jims_ip}:${jims_port}/config/user_directory -v
    Should Contain    ${result}    HTTP/1.1 200 OK

Send Linux Web-redirect Auth Traffic
    [Documentation]    Send Linux Web-redirect Auth Traffic
    [Arguments]   ${device}=${linux0}
    ...           ${server}=1.2.3.4
    ...           ${user}=myuser
    ...           ${password}=mypassword
	Execute Shell Command on Device    ${device}    command=wget --no-check-certificate http://${server} -o output.txt
    Execute Shell Command on Device    ${device}    command=awk -F 'Location: | following]' '{print $2}' output.txt | awk NF | awk '{print $1}' > redirect-url.txt
    Execute Shell Command on Device    ${device}    command=wget -i redirect-url.txt --post-data="username=${user}&password=${password}"


