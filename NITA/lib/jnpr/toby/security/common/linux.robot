*** Setting ***
Documentation  
...     This file contains all the robot common keyword for Linux 
...     
...     Author: Wentao Wu (wtwu@juniper.net)
...
...     Keyword list: 
...             Config Linux Interface IP Address
...             Config Linux Static Route
...             Check Linux Ping Result
...             Check Linux Ping Timtout Result
...             Delete Linux Interface IP Address
...             Delete Linux Static Route
...             Set Linux Service Status
...             Set Linux Interface Status
...             Generate Linux File
...             Send Linux HTTP Traffic
...             Send Linux Ftp Traffic
...             Stop Linux Ftp Traffic
...             Send Linux Telnet Traffic
...             Stop Linux Telnet Traffic
...             Send Linux Ssh Traffic
...             Stop Linux Ssh Traffic
...             Config Linux Telnet Server
...             Config Linux Ftp Server 
...             Install Linux Openssl
...             Install Linux Apache
...             Set Linux Apache Status

*** Keywords ***
Config Linux Interface IP Address
    [Documentation]    Set Linux Interface IP address
    [Arguments]    ${device}=${linux0}
    ...            ${interface}=${tv[linux_intf1_name]}
    ...            ${ip}=1.2.3.2
    ...            ${mask}=24
    
    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    Execute Shell Command on Device    ${device}     command=/sbin/ip link set ${interface} up
    Run Keyword If    ":" in "${ip}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 addr flush dev ${interface}
    ...      ELSE                       Execute Shell Command on Device    ${device}     command=/sbin/ip -4 addr flush dev ${interface}
    ${result}    Run Keyword If    ":" in "${ip}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 addr add ${ip}/${mask} dev ${interface}
    ...      ELSE                       Execute Shell Command on Device    ${device}     command=/sbin/ip addr add ${ip}/${mask} dev ${interface}
    Should Not Contain Any   ${result}    Error    Invalid
    ${result}    Run Keyword If    ":" in "${ip}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 addr show dev ${interface}
    ...       ELSE                      Execute Shell Command on Device    ${device}     command=/sbin/ip addr show dev ${interface}
    Should Contain    ${result}    ${ip}
    
Config Linux Static Route
    [Documentation]    Config Linux Static Route
    [Arguments]    ${device}=${linux0}
    ...            ${net}=1.2.3.0/24
    ...            ${nexthop}=1.2.3.1
    
    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    ${result}    Run Keyword If    ":" in "${net}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 route add ${net} via ${nexthop}
    ...       ELSE                      Execute Shell Command on Device    ${device}     command=/sbin/ip route add ${net} via ${nexthop}
    Should Not Contain Any   ${result}    Invalid    unreachable
    ${result}    Run Keyword If    ":" in "${net}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 route list ${net}
    ...       ELSE                      Execute Shell Command on Device    ${device}     command=/sbin/ip route list ${net}
    ${net} =    ipaddress.ip_network    ${net}
    ${net} =    Convert To String       ${net}
    Should Contain    ${result}    ${net}

Check Linux Ping Result
    [Documentation]    Do ping to check the connection on Linux host
    [Arguments]    ${device}=${linux0} 
    ...            ${ip}=1.2.3.2
    ...            ${count}=2
    ${result} =    Run Keyword If    ":" in "${ip}"     Execute Shell Command on Device    ${device}     command=ping6 -c ${count} ${ip}
    ...                      ELSE                       Execute Shell Command on Device    ${device}     command=ping -c ${count} ${ip}
    Should Not Match Regexp    ${result}    100%\\s+packet\\s+loss
    Should Match Regexp        ${result}    ttl=\\d+
    ${match_str}    ${received}    Should Match Regexp    ${result}   (?is)${count} packets transmitted, (\\d+) received
    [Return]    ${received}

Check Linux Ping Timeout Result
    [Documentation]    Do ping to check the connection on Linux host
    [Arguments]    ${device}=${linux0} 
    ...            ${ip}=1.2.3.2
    ...            ${count}=2
    ${result} =    Run Keyword If    ":" in "${ip}"     Execute Shell Command on Device    ${device}     command=ping6 -c ${count} ${ip}
    ...                      ELSE                       Execute Shell Command on Device    ${device}     command=ping -c ${count} ${ip}
    Should Not Match Regexp    ${result}    ttl=\\d+
    Should Match Regexp        ${result}    100%\\s+packet\\s+loss


Delete Linux Interface IP Address
    [Documentation]    Delete Linux Interface IP address
    [Arguments]    ${device}=${linux0}
    ...            ${interface}=eth1
    ...            ${ip}=${None}
    ...            ${mask}=24
    
    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    Run Keyword If    ":" in "${ip}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 addr del ${ip}/${mask} dev ${interface}
    ...    ELSE IF    "." in "${ip}"    Execute Shell Command on Device    ${device}     command=/sbin/ip addr del ${ip}/${mask} dev ${interface}
    ...       ELSE                      Execute Shell Command on Device    ${device}     command=/sbin/ip addr flush dev ${interface}
    ${result} =    Execute Shell Command on Device    ${device}     command=/sbin/ip addr show dev ${interface}
    
Delete Linux Static Route
    [Documentation]    Delete Linux Static Route
    [Arguments]    ${device}=${linux0}
    ...            ${net}=1.2.3.0/24
    
    Switch To Super User      ${device}
    ${result}    Execute Shell Command on Device    ${device}     command=whoami
    Should Contain    ${result}    root
    Run Keyword If    ":" in "${net}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 route del ${net}
    ...       ELSE                      Execute Shell Command on Device    ${device}     command=/sbin/ip route del ${net}
    Run Keyword If    ":" in "${net}"    Execute Shell Command on Device    ${device}     command=/sbin/ip -6 route list
    ...       ELSE                      Execute Shell Command on Device    ${device}     command=/sbin/ip route list

Set Linux Service Status
    [Documentation]    start or stop service for linux PC
    [Arguments]    ${device}=${linux0}
    ...            ${service}=httpd
    ...            ${action}=restart       # stop | start | restart
    Execute Shell Command on Device    ${device}     command=/sbin/service ${service} ${action}    timeout=${150}	

Set Linux Interface Status
    [Documentation]    up/down Interface For Linux PC
    [Arguments]    ${device}=${linux0}
    ...            ${interface}=eth1
    ...            ${action}=up        # up | down
	
    Switch To Super User      ${device}
    Execute Shell Command on Device    ${device}     command=/sbin/ifconfig ${interface} ${action}    timeout=${150}

Check Linux Listen Port
    [Documentation]    Check Linux Listen Port
    [Arguments]    ${device}=${linux0}
    ...            ${protocol}=tcp
    ...            ${port}=23
    ${response}    Execute Shell Command on Device    ${device}    command= netstat -antp | grep ":${port} "    timeout=${150}
    Should Match Regexp    ${response}    (?is).*?${protocol}.*?:${port}.*?LISTEN

Generate Linux File
    [Documentation]    Generate Linux File
    [Arguments]    ${device}=${linux0}
    ...            ${file}=ftp_test_file
    ...            ${path}=/home/regress/
    ...            ${bs}=10240
    ...            ${count}=1024
    ${response}    Execute Shell Command on Device    ${device}    command=/bin/dd if=/dev/zero of=${path}${file} bs=${bs} count=${count}
    Should Match Regexp    ${response}    (?is)records

Send Linux HTTP Traffic
    [Documentation]    Send Linux HTTP Traffic
    [Arguments]    ${device}=${linux0}
    ...            ${server}=1.2.3.4
    ...            ${protocol}=http       #http     https
    ...            ${expect}=It works
    ${result} =    Run Keyword If    ":" in "${server}"     Execute Shell Command on Device    ${device}     command=curl -k -g ${protocol}://[${server}]
    ...            ELSE                             Execute Shell Command on Device    ${device}    command=curl -k -g ${protocol}://${server}
    Should Contain    ${result}    ${expect}
	
Send Linux Ftp Traffic
    [Documentation]    generate ftp traffic
    [Arguments]    ${device}=${linux0}
    ...            ${server}=1.2.3.4
    ...            ${user}=regress
    ...            ${password}=MaRtInI
    ...            ${command}=pwd
    ...            ${close}=${True}       # True -- close      False -- don't close
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Name.*?    command=/usr/bin/ftp ${server}
    Should Contain    ${result}    220
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${user}
    Should Contain    ${result}    331
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${password}
    Should Contain    ${result}    230
    ${result} =    Execute Shell Command on Device    ${device}    pattern=ftp>.*?    command=${command}
    Run Keyword If    ${close}    Execute Shell Command on Device    ${device}    command=bye
    
Stop Linux Ftp Traffic
    [Documentation]    stop ftp traffic
    [Arguments]    ${device}=${linux0}
    Execute Shell Command on Device    ${device}    command=bye
    
Send Linux Telnet Traffic
    [Documentation]     Send Linux Telnet Traffic  
    [Arguments]    ${device}=${linux0}
    ...            ${server}=1.2.3.4
    ...            ${user}=regress
    ...            ${password}=MaRtInI
    ...            ${command}=pwd
    ...            ${timeout}=${300}    
    ...            ${close}=${True}       # True -- close      False -- don't close
    ${result} =    Execute Shell Command on Device    ${device}    pattern=login.*?    command=/usr/bin/telnet ${server}
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Password.*?    command=${user}
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Last login.*?    command=${password}
    Execute Shell Command on Device    ${device}    pattern=/home/regress    command=${command}    timeout=${timeout}
    Run Keyword If    ${close}    Execute Shell Command on Device    ${device}    command=exit
    
Stop Linux Telnet Traffic    
    [Documentation]     stop Telnet Traffic  
    [Arguments]    ${device}=${linux0}
    Execute Shell Command on Device    ${device}    command=exit

Send Linux Ssh Traffic
    [Documentation]     Send Linux Ssh Traffic  
    [Arguments]    ${device}=${linux0}
    ...            ${server}=1.2.3.4
    ...            ${user}=regress
    ...            ${password}=MaRtInI
    ...            ${command}=pwd
    ...            ${timeout}=${300}
    ...            ${source_address}=None	
    ...            ${close}=${True}       # True -- close      False -- don't close
    ${cmd} =  Set Variable If    "${source_address}"=='None'    ssh -o StrictHostKeyChecking=no ${user}@${server}    ssh -o StrictHostKeyChecking=no ${user}@${server} -b ${source_address}
    ${result} =    Execute Shell Command on Device    ${device}    pattern=established.*?|password.*?    command=${cmd}
    ${count} =    Get Count    ${result}    authenticity
    Run Keyword If    ${count}==1    Execute Shell Command on Device    ${device}    pattern=password.*?    command=yes
    ${result} =    Execute Shell Command on Device    ${device}    pattern=Last login.*?    command=${password}
    Execute Shell Command on Device    ${device}    pattern=${user}.*?    command=${command}    timeout=${timeout}
    Run Keyword If    ${close}    Execute Shell Command on Device    ${device}    command=exit

Stop Linux Ssh Traffic
    [Documentation]     stop Ssh Traffic  
    [Arguments]    ${device}=${linux0}
    Execute Shell Command on Device    ${device}    command=exit

Config Linux Telnet Server
    [Documentation]     Config Linux Telnet Server
    [Arguments]    ${device}=${server0}
    ...            ${flag}=IPV4        #IPV4      IPV6

    Execute Shell Command on Device    ${device}    command=/bin/echo "service telnet" > /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo "{" >> /etc/xinetd.d/telnet
    Run Keyword If    '${flag}' == 'IPV4'    Execute Shell Command on Device    ${device}    command=/bin/echo flags = REUSE >> /etc/xinetd.d/telnet
    ...    ELSE    Execute Shell Command on Device    ${device}    command=/bin/echo flags =REUSE IPV6 >> /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo socket_type = stream >> /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo wait = no >> /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo user = root >> /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo server = /usr/sbin/in.telnetd >> /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo log_on_failure += USERID >> /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo disable = no >> /etc/xinetd.d/telnet
    Execute Shell Command on Device    ${device}    command=/bin/echo "}" >> /etc/xinetd.d/telnet
    ${result}    Execute Shell Command on Device    ${device}    command=/sbin/service xinetd stop
    ${result}    Execute Shell Command on Device    ${device}    command=/sbin/service xinetd start
    Should Contain    ${result}    OK
	
Config Linux Ftp Server 
    [Documentation]     Config Linux Ipv6 Ftp Server 
    [Arguments]    ${device}=${server0}
    ...            ${flag}=IPV4                  #IPV4             IPV6
    ...            ${file}=vsftpd.conf           #vsftpd.conf      vsftpd_v6.conf for ipv6

    Execute Shell Command on Device    ${device}    command=/bin/echo "anonymous_enable=YES" > /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo local_enable=YES >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo write_enable=YES >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo local_umask=022 >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo dirmessage_enable=YES >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo connect_from_port_20=YES >> /etc/vsftpd/${file}
    Run Keyword If    '${flag}' == 'IPV4'    Execute Shell Command on Device    ${device}    command=/bin/echo listen=YES >> /etc/vsftpd/${file}
    ...    ELSE    Execute Shell Command on Device    ${device}    command=/bin/echo listen_ipv6=YES >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo pasv_enable=YES >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo ftpd_banner="For DEMO FTP service" >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo pam_service_name=vsftpd >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo userlist_enable=YES >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo tcp_wrappers=YES >> /etc/vsftpd/${file}
    Execute Shell Command on Device    ${device}    command=/bin/echo local_root=/home/regress >> /etc/vsftpd/${file}
    ${result}    Execute Shell Command on Device    ${device}    command=service vsftpd stop
    ${result}    Execute Shell Command on Device    ${device}    command=service vsftpd start
    Should Contain    ${result}    OK
	
Install Linux Openssl	
    [Documentation]    install openssl on pc
    [Arguments]    ${device}=${linux0}
    ...            ${path}=/volume/labtools/lib/Testsuites/Viking/config_files/tools
    ...            ${file}=openssl-1.0.2l.tar.gz  #the openssl tar file name
    
    Switch To Super User      ${device}
    Upload File     dev=${device}    local_file=${path}/${file}    remote_file=/tmp/${file}    user=root    password=Embe1mpls
    Execute Shell Command on Device    ${device}    command=cd /tmp/
    Execute Shell Command on Device    ${device}    command=tar -vzxf ${file}
    ${match}    ${dir}    Should Match Regexp    ${file}    (.*?).tar.gz
    Execute Shell Command on Device    ${device}    command=cd /tmp/${dir}
    Execute Shell Command on Device    ${device}    command=./config shared zlib-dynamic -fPIC -DOPENSSL_PIC --prefix=/usr/local     timeout=${3000}
    Execute Shell Command on Device    ${device}    command=make    timeout=${3000}
    Execute Shell Command on Device    ${device}    command=make install    timeout=${3000}
    Execute Shell Command on Device    ${device}    command=/bin/mv -f /usr/bin/openssl /usr/bin/openssl.old
    Execute Shell Command on Device    ${device}    command=/bin/mv -f /usr/include/openssl /usr/include/openssl.old
    Execute Shell Command on Device    ${device}    command=ln -s /usr/local/bin/openssl /usr/bin/openssl
    Execute Shell Command on Device    ${device}    command=ln -s /usr/local/include/openssl /usr/include/openssl
    Update Linux Openssl Lib Files     ${device}
    Execute Shell Command on Device    ${device}    command=/bin/cp -f /etc/ld.so.conf /etc/ld.so.conf.back
    Execute Shell Command on Device    ${device}    command=echo "/usr/local/lib64" >> /etc/ld.so.conf
    Execute Shell Command on Device    ${device}    command=ldconfig -v    timeout=${300}
    #------- to check if openssl has been installed successfully ----------
    ${match}    ${install_version}     Should Match Regexp     ${file}    openssl-(\\d.\\d.\\d\\w).tar.gz
    ${result}    Execute Shell Command on Device    ${device}    command=openssl version
    ${count} =    Get Count    ${result}    OpenSSL ${install_version}
    Run Keyword If   ${count}==1    Log To Console    openssl has been installed successfully
	
Update Linux Openssl Lib Files
    [Documentation]    Get Two Matched Item
    [Arguments]    ${device}=${linux0}
    
    Switch To Super User      ${device}
    #get current openssl version
    ${result}    Execute Shell Command on Device    ${device}    command=openssl version
    ${match}    ${version}     Should Match Regexp     ${result}    OpenSSL (\\d.\\d.\\d\\w*)
    Execute Shell Command on Device    ${device}    command=cd /usr/lib64
    #backup the old libssl file, and replace it with the new one
    ${result}    Execute Shell Command on Device    ${device}    command=ls -alt libssl.so.${version}
    ${match}    ${file}    Should Match Regexp    ${result}    (libssl.so.${version})
    Execute Shell Command on Device    ${device}    command=/bin/mv -f /usr/lib64/${file} /usr/lib64/${file}.old
    Execute Shell Command on Device    ${device}    command=/bin/cp -f /usr/local/lib64/libssl.so.1.0.0 /usr/lib64/libssl.so.1.0.0
    #backup the old libcrypto file, and replace it with the new one
    ${result}    Execute Shell Command on Device    ${device}    command=ls -alt libcrypto.so.${version}
    ${match}    ${file}    Should Match Regexp	   ${result}    (libcrypto.so.${version})
    Execute Shell Command on Device    ${device}    command=/bin/mv -f /usr/lib64/${file} /usr/lib64/${file}.old
    Execute Shell Command on Device    ${device}    command=/bin/cp -f /usr/local/lib64/libcrypto.so.1.0.0 /usr/lib64/libcrypto.so.1.0.0

Set Linux Apache Status
    [Documentation]    start or stop service for linux PC
    [Arguments]    ${device}=${server0}
    ...            ${action}=restart       # stop | start | restart
    ...            ${service}=/usr/local/apache-2.2.21/bin/httpd
    
    Execute Shell Command on Device    ${device}     command=${service} -k ${action}    timeout=${150}	

Install Linux Apache
    [Documentation]    install Apache to support https on pc
    [Arguments]    ${device}=${server0}
    ...            ${path}=/volume/labtools/lib/Testsuites/Viking/config_files/tools
    ...            ${install_dir}=/usr/local/apache-2.2.21
    ...            ${file}=httpd-2.2.21.tar.gz
    
    Upload File     dev=${device}    local_file=${path}/${file}    remote_file=/tmp/${file}    user=root    password=Embe1mpls
    Execute Shell Command on Device    ${device}    command=cd /tmp/
    Execute Shell Command on Device    ${device}    command=tar -vzxf ${file}
    Execute Shell Command on Device    ${device}    command=cd /tmp/httpd-2.2.21
    Execute Shell Command on Device    ${device}    command=./configure --enable-ssl --enable-so --prefix ${install_dir}    timeout=${3000}
    Execute Shell Command on Device    ${device}    command=make    timeout=${3000}
    Execute Shell Command on Device    ${device}    command=make install    timeout=${3000}
    Execute Shell Command on Device    ${device}    command=/bin/cp -f ${install_dir}/conf/httpd.conf ${install_dir}/conf/httpd.conf.back
    Execute Shell Command on Device    ${device}    command=sed -i '/httpd-ssl/s/^#Include/Include/g' ${install_dir}/conf/httpd.conf
    Execute Shell Command on Device    ${device}    command=openssl genrsa -out ${install_dir}/conf/server.key 1024    timeout=${3000}
    Execute Shell Command on Device    ${device}    command=openssl req -new -x509 -days 365 -key ${install_dir}/conf/server.key -out ${install_dir}/conf/server.crt -subj "/C=CN/ST=BJ/L=BJ/O=JNPR/OU=CNRD/CN=2.2.2.10/emailAddress=https_server@juniper.net"    timeout=${3000}    
    Execute Shell Command on Device    ${device}    command=sed -i 's/^#ServerName www.example.com:80/ServerName 127.0.0.1:80/g' /usr/local/apache-2.2.21/conf/httpd.conf
    Execute Shell Command on Device    ${device}    command=sed -i 's/^#Listen 80/Listen 80/g' ${install_dir}/conf/httpd.conf
    Execute Shell Command on Device    ${device}    command=sed -i 's/^#Listen 443/Listen 443/g' ${install_dir}/conf/extra/httpd-ssl.conf
    Set Linux Apache Status    device=${device}    action=stop
    Set Linux Apache Status    device=${device}    action=start
    Check Linux Listen Port    device=${device}    port=443
	
