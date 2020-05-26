#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Test Linux userfw keywords
Author: Ruby Wu, rubywu@juniper.net
"""

import unittest
import mock

from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.security.userfw.userfw_linux import userfw_linux

# pylint: disable=line-too-long
# pylint: disable=invalid-name


class test_userfw_linux(unittest.TestCase):
    """
    Description: Linux userfw keywords unit test
    """
    def setUp(self):
        """
        Description: setUp unit test
        """
        self.device = mock.Mock()(spec=UnixHost)
        self.device.log = mock.Mock()
        self.linux = userfw_linux()

    def test_generate_linux_clearpass_post_authentry(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: generate_linux_clearpass_post_authentry unit test
        """

        # device is none
        self.assertRaises(Exception, self.linux.generate_linux_clearpass_post_authentry)
        # simulator_path is none and gen_jar_file is none
        self.assertRaises(Exception, self.linux.generate_linux_clearpass_post_authentry, device=self.device)

        self.device.shell().response.side_effect = ["file.xml", "No such file or directory", "built failed"]
        # delete xml file failed
        self.assertRaises(Exception, self.linux.generate_linux_clearpass_post_authentry, device=self.device, simulator_path="/cppm/", gen_jar_file="gen.jar")
        # build authentry failed
        self.assertRaises(Exception, self.linux.generate_linux_clearpass_post_authentry, device=self.device, simulator_path="/cppm/", gen_jar_file="gen.jar")

        # query table failed
        self.device.shell().response.side_effect = ["No such file or directory", "Entries have been built", "test"]
        self.assertRaises(Exception, self.linux.generate_linux_clearpass_post_authentry, device=self.device, simulator_path="/cppm/", gen_jar_file="gen.jar", save_jar_file='save.jar')

        # normal test
        self.device.shell().response.side_effect = ["No such file or directory", "Entries have been built"]
        self.assertTrue(self.linux.generate_linux_clearpass_post_authentry(device=self.device, simulator_path="/cppm/", gen_jar_file="gen.jar", xml_file='test.xml', kwargs_value='simulator generate command'))
        self.device.shell().response.side_effect = ["No such file or directory", "Entries have been built", "update"]
        self.assertTrue(self.linux.generate_linux_clearpass_post_authentry(device=self.device, simulator_path="/cppm/", gen_jar_file="gen.jar", save_jar_file='save.jar', xml_file='file.xml', kwargs_value='simulator generate command'))

    @mock.patch("time.sleep")
    def test_send_linux_clearpass_post_authentry(self, mock_sleep):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: send_linux_clearpass_post_authentry unit test
        """

        # device is none
        self.assertRaises(Exception, self.linux.send_linux_clearpass_post_authentry)
        # simulator_path is none or post_jar_file is none or user is none
        self.assertRaises(Exception, self.linux.send_linux_clearpass_post_authentry, device=self.device, simulator_path=None)
        # password is none or srx_ip is none or source_ip is none
        self.assertRaises(Exception, self.linux.send_linux_clearpass_post_authentry, device=self.device, simulator_path="/cppm/", post_jar_file="post.jar", user="test")

        self.device.shell().response.side_effect = ["no file", "5 XML.xml", "100"]
        # xml file doesn't exist
        self.assertRaises(Exception, self.linux.send_linux_clearpass_post_authentry, device=self.device, simulator_path="/cppm/", post_jar_file="post.jar", user="test", password="123", srx_ip="1.1.1.1", source_ip="2.2.2.2")
        # post authentry failed
        self.assertRaises(Exception, self.linux.send_linux_clearpass_post_authentry, device=self.device, simulator_path="/cppm/", post_jar_file="post.jar", user="test", password="123", srx_ip="1.1.1.1", source_ip="2.2.2.2")

        # normal test
        self.device.shell().response.side_effect = ["5 XML.xml", "200 OK", "5 test.xml", "200 OK"]
        self.assertTrue(self.linux.send_linux_clearpass_post_authentry(device=self.device, simulator_path="/cppm/", post_jar_file="post.jar", user="test", password="123", srx_ip="1.1.1.1", source_ip="2.2.2.2"))
        self.assertTrue(self.linux.send_linux_clearpass_post_authentry(device=self.device, simulator_path="/cppm/", post_jar_file="post.jar", user="test", password="123", srx_ip="1::1", source_ip="2::2", post_number=2, xml_file="test.xml", protocol="https", port="8888"))

    def test_config_linux_mysql_database_for_clearpass(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: config_linux_mysql_database_for_clearpass unit test
        """

        # device is none
        self.assertRaises(Exception, self.linux.config_linux_mysql_database_for_clearpass)

        self.device.shell().response.side_effect = ["ERROR", "correct", "Query failed", "Query failed"]
        # change database failed
        self.assertRaises(Exception, self.linux.config_linux_mysql_database_for_clearpass, device=self.device)
        # handle access table failed
        self.assertRaises(Exception, self.linux.config_linux_mysql_database_for_clearpass, device=self.device)

        self.device.shell().response.side_effect = ["correct", "Query OK", "Query OK", "Query failed", "correct", "Query OK", "Query OK", "Query OK", "count(*)abc 1"]
        # handle query table failed
        self.assertRaises(Exception, self.linux.config_linux_mysql_database_for_clearpass, device=self.device)
        # delete record failed
        self.assertRaises(Exception, self.linux.config_linux_mysql_database_for_clearpass, device=self.device)

        self.device.shell().response.side_effect = ["correct", "Query OK", "Query OK", "Query OK", "count(*)abc 0", "exit"]
        # exit mysql database failed
        self.assertRaises(Exception, self.linux.config_linux_mysql_database_for_clearpass, device=self.device)

        # normal test
        self.device.shell().response.side_effect = ["correct", "Query OK", "Query OK", "Query OK", "count(*)abc 0", "Bye", "correct", "Query OK", "Query OK", "Query OK", "count(*)abc 0", "Bye"]
        self.assertTrue(self.linux.config_linux_mysql_database_for_clearpass(device=self.device))
        self.assertTrue(self.linux.config_linux_mysql_database_for_clearpass(device=self.device, password='123abc', db_name='test', access_table_name='access', client_id='client', client_secret='Embe1mpls', query_table_name='query'))

    def test_export_linux_keystore_to_certificate(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: export_linux_keystore_to_certificate unit test
        """

        # device is none
        self.assertRaises(Exception, self.linux.export_linux_keystore_to_certificate)
        # Certificate stored failed
        self.device.shell().response.return_value = "no Certificate file"
        self.assertRaises(Exception, self.linux.export_linux_keystore_to_certificate, device=self.device)

        # normal test
        self.device.shell().response.side_effect = ["Certificate stored in file </root/my.crt>", "Certificate stored in file </root/my.crt>"]
        self.assertTrue(self.linux.export_linux_keystore_to_certificate(device=self.device))
        self.assertTrue(self.linux.export_linux_keystore_to_certificate(device=self.device, path="/root/", password="123abc"))

    def test_set_linux_tomcat_config(self):
        """
        Author: Ruby Wu, rubywu@juniper.net
        Description: set_linux_tomcat_config unit test
        """

        # device is none
        self.assertRaises(Exception, self.linux.set_linux_tomcat_config)
        self.device.shell().response.side_effect = ["No such file or directory", "query_extend.war", "tomcat stop"]
        # query_extend.war file doesn't exist
        self.assertRaises(Exception, self.linux.set_linux_tomcat_config, device=self.device)
        # start tomcat failed
        self.assertRaises(Exception, self.linux.set_linux_tomcat_config, device=self.device)

        # normal test
        self.device.shell().response.side_effect = ["query_extend.war", "Tomcat started", "query_extend.war", "Tomcat started"]
        self.assertTrue(self.linux.set_linux_tomcat_config(device=self.device))
        self.assertTrue(self.linux.set_linux_tomcat_config(device=self.device, path="/root", src_file="abc.war", dst_file="server_test"))


if __name__ == '__main__':
    unittest.main()
