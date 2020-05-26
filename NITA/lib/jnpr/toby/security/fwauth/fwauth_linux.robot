*** Setting ***
Documentation  
...     This file contains all the fwauth robot keyword for linux 
...     
...     Author: Linjing Liu (ljliu@juniper.net)
...
...     Keyword list: 
...             Send Linux HTTP Firewall Auth Traffic
...             Send Linux Web-auth Firewall Auth Traffic
...             Send Linux Web-redirect Firewall Auth Traffic
...             Send Linux Ftp Firewall Auth Traffic
...             Send Linux Telnet Firewall Auth Traffic


*** Keywords ***
		

Send Linux HTTP Firewall Auth Traffic
    [Documentation]    Send Linux HTTP Fwauth Traffic
    [Arguments]    ${device}=${linux0}
    ...            ${server}=1.2.3.4
    ...            ${auth_username}=test
    ...            ${auth_password}=test
    ...            ${protocol}=http
    ...            ${expect}=Firewall User Authentication: Accepted
	Log    \n----------from client ${protocol} to http/https server----------
    ${result}    Run Keyword If    ":" in "${server}"    Execute Shell Command on Device    ${device}    command=curl -k -u ${auth_username}:${auth_password} ${protocol}://[${server}]
    ...                  ELSE                        Execute Shell Command on Device    ${device}    command=curl -k -u ${auth_username}:${auth_password} ${protocol}://${server}
    Should Contain    ${result}    ${expect}
	
Send Linux Web-auth Firewall Auth Traffic
    [Documentation]    Send Linux Web-redirect Fwauth Traffic
    [Arguments]    ${device}=${linux0}
    ...            ${server}=1.2.3.4
    ...            ${auth_username}=test
    ...            ${auth_password}=test
    ...            ${protocol}=http
    ...            ${expect}=User Authentication : Success
	Execute Shell Command on Device    ${device}    command=rm -f index.html*
    Run Keyword If    ":" in "${server}"    Execute Shell Command on Device    ${device}    command=wget --no-check-certificate ${protocol}://[${server}] --post-data="username=${auth_username}&password=${auth_password}"
    ...                    ELSE            	Execute Shell Command on Device    ${device}    command=wget --no-check-certificate ${protocol}://${server} --post-data="username=${auth_username}&password=${auth_password}"
	${result}    Execute Shell Command on Device    ${device}    command=cat index.html
    Should Contain    ${result}    ${expect}

Send Linux Web-redirect Firewall Auth Traffic
    [Documentation]    Send Linux Web-redirect Fwauth Traffic
    [Arguments]    ${device}=${linux0}
    ...            ${server}=1.2.3.4
    ...            ${auth_username}=test
    ...            ${auth_password}=test
    ...            ${protocol}=http
    ...            ${expect}=User Authentication : Success
	Execute Shell Command on Device    ${device}    command=rm -f output.txt
	Execute Shell Command on Device    ${device}    command=rm -f redirect-url.txt
    Run Keyword If    ":" in "${server}"    Execute Shell Command on Device    ${device}    command=wget --no-check-certificate ${protocol}://[${server}] -o output.txt
    ...                  ELSE               Execute Shell Command on Device    ${device}    command=wget --no-check-certificate ${protocol}://${server} -o output.txt
    Execute Shell Command on Device    ${device}    command=awk -F 'Location: | following]' '{print $2}' output.txt | awk NF | awk '{print $1}' > redirect-url.txt
	Execute Shell Command on Device    ${device}    command=rm -f webauth*
    Execute Shell Command on Device    ${device}    command=wget -i redirect-url.txt --post-data="username=${auth_username}&password=${auth_password}"
	${result}    Execute Shell Command on Device    ${device}    command=cat webauth*
    Should Contain    ${result}    ${expect}

	
Send Linux Ftp Firewall Auth Traffic
    [Documentation]    Send Linux Ftp Auth Traffic
    [Arguments]   ${device}=${linux0}
    ...           ${server}=1.2.3.4
    ...           ${auth_username}=test
    ...           ${auth_password}=test
    ...           ${username}=regress
    ...           ${password}=MaRtInI
    ...           ${command}=pwd
    ...           ${ftp_banner}=Authentication - Accepted    # Authentication - Failed  |  Authentication - Accepted  |  customized banner
    ...           ${success}=${True}         # True for success scenario  | False for fail scenario
    ...           ${close}=${True}        # True -- close    False -- not to close
	
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Name.*?    command=/usr/bin/ftp ${server}
    Should Contain    ${result}    220
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${auth_username}
    Should Contain    ${result}    331
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${auth_password}
    Should Contain    ${result}    ${ftp_banner}
    Sleep    10
    ${result} =    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=Name.*?    command=open ${server}
    Run Keyword If    ${success}    Should Contain    ${result}    220
    ${result} =    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${username}
    Run Keyword If    ${success}    Should Contain    ${result}    331
    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${password}
#    Should Contain    ${result}    230
    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${command}
    Run Keyword If    ${close}    Execute Shell Command on Device    ${device}    command=bye


Send Linux Telnet Firewall Auth Traffic	
    [Documentation]    Send Linux Telnet Auth Traffic
    [Arguments]   ${device}=${linux0}
    ...           ${server}=1.2.3.4
    ...           ${auth_username}=test
    ...           ${auth_password}=test
    ...           ${username}=regress
    ...           ${password}=MaRtInI
    ...           ${command}=pwd
    ...           ${telnet_banner}=Authentication - Accepted    # Authentication - Failed  |  Authentication - Accepted  |  customized banner
    ...           ${banner2}=Authentication - Accepted
    ...           ${success}=${True}         # True for success scenario  | False for fail scenario
    ...           ${close}=${True}        # True -- close    False -- not to close
    

    Execute Shell Command on Device    ${device}    pattern=Username.*?    command=/usr/bin/telnet ${server}
#    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${auth_username}
    ${response} =    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${auth_username}
    ...              ELSE    Execute Shell Command on Device    ${device}    command=${auth_username}
    ${result} =    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=login.*?|Username.*?    command=${auth_password}
    ...            ELSE IF    "closed" in '''${response}'''    Log    This is Firewall Auth Fail Error scenario    
    ...            ELSE      Execute Shell Command on Device    ${device}    pattern=closed.*?    command=${auth_password}
    Run Keyword If    ${success}    Should Contain    ${result}    ${telnet_banner}
    Sleep    3
    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${username}
    ${result} =    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=Last login.*?|login.*?    command=${password}
    Run Keyword If    "${banner2}" in '''${result}'''    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=regress
    Run Keyword If    "${banner2}" in '''${result}'''    Execute Shell Command on Device    ${device}    pattern=Last login.*?    command=MaRtInI
    Run Keyword If    ${success}    Execute Shell Command on Device    ${device}    pattern=/home/regress    command=${command}
    Run Keyword If    ${close}    Execute Shell Command on Device    ${device}    command=exit

