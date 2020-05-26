#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Userfw SRX keywords
Author: Wentao Wu, wtwu@juniper.net
"""

import re
import time
import ipaddress


# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments

class userfw_linux(object):
    """
    Description: Userfw SRX linux keywords

    keywords list:
    * generate_linux_clearpass_post_authentry
    * send_linux_clearpass_post_authentry
    * config_linux_mysql_database_for_clearpass
    * export_linux_keystore_to_certificate
    * set_linux_tomcat_config
    """

    def __init__(self, device=None):
        """
        device handle
        """
        self.device = device
        self.shell_timeout = 60

    def generate_linux_clearpass_post_authentry(self, device=None, simulator_path=None, gen_jar_file=None, save_jar_file=None, xml_file='XML.xml', **kwargs):

        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
            **REQUIRED** handle of linux PC

        :param str simulator_path:
            **REQUIRED** path of simulator tool

        :param str gen_jar_file:
            **REQUIRED** name of genearte jar file

        :param str save_jar_file:
            *OPTIONAL* name of save jar file

        :param str xml_file:
        *OPTIONAL* name of xml_file

        #java -jar GenerateXML_0822.jar -n 1 -s Aruba ClearPass -non 200 -noff 0 -v true -ipon 4000:5a:6b:8c:9d:10:3e:8 -ipoff 4000:5a:6b:8c:9d:10:3e:8 -user ipv4_user -role ipv6_group -rolen 50 -d Juniper.net -posture Healthy -userm 10000 -rolem 50 -did dev -dgrp dev_grp -dgrpn 3 -devm 100 -dgrpm 300 -dcat laptop -dvendor Lenovo -dtype ThinkPadT430 -dos Windows -dosv 7.1 -ctag_name ctag_name -ctag_val ctag_val -ctagn 3 -ctagm 15
        """

        if device is None:
            raise Exception("------device handle is None!------\n")

        if simulator_path is not None and gen_jar_file is not None:
            command_line = 'java ' + '-jar ' + gen_jar_file
        else:
            raise Exception("------simulator path is None or jar file is None!-------\n")

        kwargs_value = kwargs.get("kwargs_value", ' ')
        command_line = command_line + ' ' + kwargs_value
        device.log(level='INFO', message=command_line)

        device.su()
        device.shell(command='cd ' + simulator_path)
        device.shell(command='pwd')
        device.shell(command="rm -rf {}".format(xml_file))
        response = device.shell(command="ls -alt {}".format(xml_file)).response()
        if re.search('No such file or directory', response) is None:
            raise Exception("------delete xml file file failed!------\n")

        device.log(level='INFO', message="------get generation command line is: ")
        device.log(level='INFO', message=command_line)
        response = device.shell(command=command_line).response()
        if re.search('Entries have been built', response) is None:
            raise Exception("------generate linux clearpass post authentry failed!------\n")

        if save_jar_file is not None:
            response = device.shell(command='java -jar ' + save_jar_file + ' -f ' + xml_file + ' -t 10', timeout=self.shell_timeout).response()
            if re.search(r'(?:insert into|update)', response) is None:
                raise Exception("------save authentry to query table failed!------\n")
        return True

    def send_linux_clearpass_post_authentry(self, device=None, **kwargs):

        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** handle of linux PC

        :param str simulator_path:
        **REQUIRED** path of simulator tool

        :param str post_jar_file:
        **REQUIRED** name of post jar file

        :param str user:
        **REQUIRED** user

        :param str password:
        **REQUIRED** password

        :param str srx_ip:
        **REQUIRED** srx_ip

        :param str source_ip:
         **REQUIRED** source_ip

        :param int post_number:
        *OPTIONAL* post_number

        :param str xml_file:
        *OPTIONAL* name of xml_file

        :param str port:
        *OPTIONAL* port

        :param int post_number:
        *OPTIONAL* post_number

        #java -jar Post_v6_0908.jar -u cp_user -p Netscreen1 -postNumber 1 -e XML.xml -destURL http://20.0.0.50:8080/api/userfw/v1/post-entry -sourceIP 20.0.0.100
        #java -jar Post_v6_0908.jar -u cp_user -p Netscreen1 -postNumber 1 -e XML.xml -destURL https://[a000::50]:443/api/userfw/v1/post-entry -sourceIP a000::100

        """

        simulator_path = kwargs.get("simulator_path")
        post_jar_file = kwargs.get("post_jar_file")
        user = kwargs.get("user")
        password = kwargs.get("password")
        srx_ip = kwargs.get("srx_ip")
        source_ip = kwargs.get("source_ip")
        post_number = kwargs.get("post_number", 1)
        xml_file = kwargs.get("xml_file", 'XML.xml')
        protocol = kwargs.get("protocol", 'http')
        port = kwargs.get("port", 8080)

        if device is None:
            raise Exception("------device handle is None!------\n")

        if simulator_path is None or post_jar_file is None or user is None:
            raise Exception("------simulator_path/post_jar_file/user is None-------\n")

        if password is None or srx_ip is None or source_ip is None:
            raise Exception("------password/srx_ip/source_ip is None------\n")

        if ipaddress.ip_address(srx_ip).version == 4 and ipaddress.ip_address(source_ip).version == 4:
            command_line = 'java -jar ' + post_jar_file + ' -u ' + user + ' -p ' + password + ' -postNumber ' + str(post_number) + ' -e ' + xml_file + ' -destURL ' + protocol + '://' + srx_ip + ':' + str(port) + '/api/userfw/v1/post-entry -sourceIP ' + source_ip
        elif ipaddress.ip_address(srx_ip).version == 6 and ipaddress.ip_address(source_ip).version == 6:
            command_line = 'java -jar ' + post_jar_file + ' -u ' + user + ' -p ' + password + ' -postNumber ' + str(post_number) + ' -e ' + xml_file + ' -destURL ' + protocol + '://[' + srx_ip + ']:' + str(port) + '/api/userfw/v1/post-entry -sourceIP ' + source_ip

        device.su()
        device.shell(command='cd ' + simulator_path)
        device.shell(command='pwd')

        response = device.shell(command="ls -alt {}".format(xml_file)).response()
        if re.search(r"\d+\s*{}".format(xml_file), response) is None:
            raise Exception("------xml file doesn't exist, it's unexpected!------\n")

        device.log(level='INFO', message="------get post command line is: ")
        device.log(level='INFO', message=command_line)
        response = device.shell(command=command_line, timeout=self.shell_timeout).response()
        time.sleep(5)

        if re.search('200 OK', response) is None:
            raise Exception("------send linux clearpass post authentry failed!------\n")

        return True

    def config_linux_mysql_database_for_clearpass(self, device=None, **kwargs):

        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** handle of linux PC

        :param str password:
        **REQUIRED** password

        :param str db_name:
        **REQUIRED** db name

        :param str access_table_name:
        **REQUIRED** access table name

        :param str client_id:
        **REQUIRED** client id

        :param str client_secret:
        **REQUIRED** client secret

        """

        password = kwargs.get("password", '123456')                           # please use default value
        db_name = kwargs.get("db_name", 'TEST')                               # please use default value
        access_table_name = kwargs.get("access_table_name", 'AccessClient')   # please use default value
        client_id = kwargs.get("client_id", 'Client1')                        # please keep correspondence with query configuration on srx
        client_secret = kwargs.get("client_secret", 'Netscreen1')             # please keep correspondence with query configuration on srx
        query_table_name = kwargs.get("query_table_name", 'query_extend')     # please use default value

        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.log(level='INFO', message="------operater database step 1: enter into mysql database------")
        device.shell(command='mysql -u root -p' + password, pattern='mysql>', timeout=self.shell_timeout)
        response = device.shell(command='use ' + db_name + ';', pattern='mysql>').response()
        if re.search('ERROR', response):
            raise Exception("------change database failed!------\n")

        device.log(level='INFO', message="------operater database step 2: insert into the correct client id and client secrect to access table:------")
        device.shell(command='delete from ' + access_table_name + ';', pattern='mysql>')
        command_line = 'insert into ' + access_table_name + ' (client_id, client_secret) values ("' + client_id + '","' + client_secret + '");'
        device.log(level='INFO', message=command_line)
        response1 = device.shell(command=command_line, pattern='mysql>').response()
        response2 = device.shell(command='SET GLOBAL event_scheduler = ON;', pattern='mysql>').response()
        if re.search('Query OK', response1) is None or re.search('Query OK', response2) is None:
            raise Exception("------handle access table failed!------\n")

        device.log(level='INFO', message="------operater database step 3: create query table and delete record in the table:------")
        command_line = 'CREATE TABLE IF NOT EXISTS `' + db_name + '`.`' + query_table_name + '` \
        (`ip` VARCHAR(64) NOT NULL,`ip4` LONG DEFAULT NULL, `ip6` BINARY(16) NULL DEFAULT NULL,\
        `user` VARCHAR(64) NULL DEFAULT NULL,`domain` VARCHAR(64) NULL DEFAULT NULL, \
        `roles` VARCHAR(16384) NULL DEFAULT NULL,`source` VARCHAR(64) NULL DEFAULT NULL,\
        `spt` VARCHAR(45) NULL DEFAULT NULL,`updated_at` VARCHAR(45) NULL DEFAULT NULL,\
        `is_online` INTEGER NULL DEFAULT NULL,`device` VARCHAR(64) NULL DEFAULT NULL,\
        `device_group` VARCHAR(16384) NULL DEFAULT NULL,`device_category` \
        VARCHAR(45) NULL DEFAULT NULL,`device_vendor` VARCHAR(45) NULL DEFAULT NULL,\
        `device_type` VARCHAR(45) NULL DEFAULT NULL,`device_os` VARCHAR(45) NULL DEFAULT NULL,\
        `device_os_version` VARCHAR(45) NULL DEFAULT NULL,`custom_tag1` \
        VARCHAR(45) NULL DEFAULT NULL,`custom_tag2` VARCHAR(45) NULL DEFAULT NULL,\
        `custom_tag3` VARCHAR(45) NULL DEFAULT NULL,PRIMARY KEY (`ip`),\
        UNIQUE INDEX `ip_UNIQUE` (`ip` ASC)) ENGINE = InnoDB DEFAULT CHARACTER SET = latin1;'

        device.log(level='INFO', message=command_line)
        response = device.shell(command=command_line, pattern='mysql>').response()
        if re.search('Query OK', response) is None:
            raise Exception("------handle query table failed!------\n")

        device.shell(command='delete from ' + query_table_name + ';', pattern='mysql>')
        response = device.shell(command='select count(*) from ' + query_table_name + ';', pattern='mysql>', timeout=self.shell_timeout).response()

        result = re.search(r"count\(\*\).*?(\d+)", response, re.S)
        count = result.group(1)
        if int(count) != 0:
            raise Exception("------ delete record failed!------\n")

        device.log(level='INFO', message="------operater database step 4: exit mysql database------")
        response = device.shell(command='exit').response()
        if re.search('Bye', response) is None:
            raise Exception("------exit mysql database failed!------\n")

        return True

    def export_linux_keystore_to_certificate(self, device=None, **kwargs):

        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** handle of linux PC

        :param str path:
        **REQUIRED** path name

        :param str password:
        **REQUIRED** password

        """

        path = kwargs.get("path", '/usr/java/default/bin')
        password = kwargs.get("password", '123456')

        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.shell(command='cd ' + path)
        command_line = './keytool -export -alias "tomcat" -keystore /root/.keystore -file /root/my.crt'
        device.shell(command=command_line, pattern='Enter keystore password:', timeout=self.shell_timeout)
        response = device.shell(command=password, timeout=self.shell_timeout).response()
        if re.search(r'Certificate stored in file </root/my.crt>', response) is None:
            raise Exception("------Certificate stored failed!------\n")
        return True

    def set_linux_tomcat_config(self, device=None, **kwargs):

        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** handle of linux PC

        :param str path:
        **REQUIRED** path name

        :param str src_file:
        **REQUIRED** src file name

        :param str dst_file:
        **REQUIRED** dst file name

        """

        path = kwargs.get("path", '/usr/local/tomcat7/webapps')
        src_file = kwargs.get("src_file", 'query_extend.war')
        dst_file = kwargs.get("dst_file", 'server')

        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.shell(command='cd ' + path)
        device.shell(command='rm -rf ' + dst_file + '.war')
        device.shell(command='rm -rf ' + dst_file)
        response = device.shell(command='cp -f /root/' + src_file + ' ' + dst_file + '.war').response()

        if re.search('No such file or directory', response):
            raise Exception("------query_extend.war file doesn't exist in root directory, please copy this source file to this directory!------\n")

        device.shell(command='sh ../bin/shutdown.sh', timeout=self.shell_timeout)
        response = device.shell(command='sh ../bin/startup.sh', timeout=self.shell_timeout).response()
        if re.search('Tomcat started', response) is None:
            raise Exception("------start tomcat failed!------\n")
        return True
