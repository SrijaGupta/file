# coding: UTF-8
# pylint: disable=invalid-name,attribute-defined-outside-init
"""All unit test cases for linux_tool module"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import sys
import os
import time
import copy
from unittest import TestCase, mock

from jnpr.toby.exception import toby_exception
from jnpr.toby.hldcl import device as dev
from jnpr.toby.hldcl.juniper.security import robot_keyword
from jnpr.toby.utils.linux.linux_tool import linux_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool


class TestLinuxTool(TestCase):
    """All unit test cases for linux_tool module"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.ins = linux_tool()

        self.response = {}
        self.response["HOST_ONE_CMD_RESPONSE"] = "240K ."
        self.response["HOST_MULTI_CMD_RESPONSE"] = """
        total 10404
        -rwxrwxr-x 1 jonjiang jonjiang     2124 Apr  6 23:48 coremgt.py
        -rw-rw-r-- 1 jonjiang jonjiang    10651 Apr  6 23:48 flow_common_tool.py
        -rw-r--r-- 1 jonjiang jonjiang    12732 Apr 28 05:44 ftp_client.py
        -rw-rw-r-- 1 jonjiang jonjiang 10485760 Apr 28 05:45 ftp_file
        -rw-rw-r-- 1 jonjiang jonjiang     3007 Apr  6 23:48 ftp.py
        """

        self.response["HOSTNAME_INFO_FROM_CENTOS"] = "fnd-lnx31.englab.juniper.net"
        self.response["HOSTNAME_INFO_FROM_UBUNTU"] = "hutong-j"
        self.response["HOSTNAME_INFO_FROM_UNKNOWN"] = "unknown_host"
        self.response["HOST_UNAME_INFO_FROM_CENTOS"] = "2.6.32-71.el6.i686"
        self.response["HOST_UNAME_INFO_FROM_UBUNTU"] = "4.4.0-62-generic"
        self.response["HOST_UNAME_INFO_FROM_UNKNOWN"] = "whatever you don't know the OS"

        self.response["START_TCPDUMP_PROCESS"] = """[1] 31289"""
        self.response["START_TCPDUMP_PROCESS_INVALID_RESPONSE"] = """Something wrong happened"""

        self.response["NORMAL_STOP_TCPDUMP"] = """
        tcpdump  31421  0.4  0.0   9664  4992 pts/8    S+   15:04   0:00 tcpdump -nni eth1
        root     31423  0.0  0.0   4360   724 pts/9    S+   15:04   0:00 grep tcpdump
        """

        self.response["STOP_TCPDUMP_WITH_NO_PROCESSING"] = """
        something strange output
        root     31423  0.0  0.0   4360   724 pts/9    S+   15:04   0:00 grep tcpdump
        """

        self.response["NORMAL_STOP_TCPDUMP_RECORD"] = """
        15:09:08.187683 STP 802.1d, Config, Flags [none], bridge-id 8000.00:26:88:f7:5f:10.8203, length 47
        15:09:08.232692 IP 10.208.134.243.62628 > 224.0.0.252.5355: UDP, length 32
        15:09:08.241028 ARP, Request who-has 10.208.130.243 tell 10.208.132.245, length 46
        15:09:08.264219 IP 10.208.135.81.45688 > 228.208.135.80.45688: UDP, length 102
        15:09:08.269298 IP6 fe80::5b7:ce7e:59b4:8009.63729 > ff02::1:3.5355: UDP, length 90
        15:09:08.269367 IP 10.208.130.159.63729 > 224.0.0.252.5355: UDP, length 90
        15:09:08.272788 IP 10.208.128.151.45688 > 228.208.128.152.45688: UDP, length 76
        15:09:08.280607 ARP, Request who-has 10.208.135.120 tell 10.208.135.126, length 46
        15:09:08.289747 IP 10.208.2.15.11989 > 10.208.131.7.22: Flags [P.], seq 1041:1093, ack 3164, win 251, length 52
        """

        self.response["CREATE_FTP_CONNECTION_FOREGROUND_RESPONSE"] = """
        ftp: connect: Connection refused
        ftp> by
        """

        self.response["CREATE_FTP_CONNECTION_FOREGROUND_HOLDTIME_RESPONSE"] = """
        *resp* '220 "RLI36411 FTP service"'
        *cmd* 'USER regress'
        *resp* '331 Please specify the password.'
        *cmd* 'PASS *******'
        *resp* '230 Login successful.'
        *welcome* '220 "RLI36411 FTP service"'
        send cmd: dir
        *cmd* 'TYPE A'
        *resp* '200 Switching to ASCII mode.'
        *cmd* 'PORT 127,0,0,1,180,171'
        *resp* '200 PORT command successful. Consider using PASV.'
        *cmd* 'NLST'
        *resp* '150 Here comes the directory listing.'
        *resp* '226 Directory send OK.'
        send cmd: ls
        *cmd* 'TYPE A'
        *resp* '200 Switching to ASCII mode.'
        *cmd* 'PORT 127,0,0,1,210,177'
        *resp* '200 PORT command successful. Consider using PASV.'
        *cmd* 'NLST'
        *resp* '150 Here comes the directory listing.'
        *resp* '226 Directory send OK.'
        hold '5' secs.
        *cmd* 'QUIT'
        *resp* '221 Goodbye.'
        """

        self.response["CREATE_FTP_CONNECTION_BACKGROUND_RESPONSE"] = """[1] 31289"""
        self.response["CREATE_FTP_CONNECTION_BACKGROUND_INVALID_RESPONSE"] = """invalid response"""

        self.response["NORMAL_CLOSE_FTP_CONNECTION"] = """
        root     31598  0.0  0.0   4360   724 pts/9    S+   16:25   0:00 python ftp_client.py -t 30
        root     31423  0.0  0.0   4360   724 pts/9    S+   15:04   0:00 grep ftp_client.py
        """

        self.response["CLOSE_FTP_CONNECTION_WITH_NO_PROCESSING"] = """
        something strange output
        root     31423  0.0  0.0   4360   724 pts/9    S+   15:04   0:00 grep ftp_client.py
        """

        self.response["CREATE_TELNET_CONNECTION_FOREGROUND_RESPONSE"] = """
        Trying 127.0.0.1...
        Connected to 127.0.0.1.
        Escape character is '^]'.
        Password:
        Last login: Tue May  2 17:13:08 from ttsv-ubu16-18.juniper.net
        [regress@fnd-lnx31 ~]$
        telnet> quit
        Connection closed.
        """

        self.response["CREATE_TELNET_CONNECTION_BACKGROUND_RESPONSE"] = """[1] 31289"""
        self.response["CREATE_TELNET_CONNECTION_BACKGROUND_INVALID_RESPONSE"] = """invalid response"""

        self.response["NORMAL_CLOSE_TELNET_CONNECTION"] = """
        root     31598  0.0  0.0   4360   724 pts/9    S+   16:25   0:00 python telnet_client.py -t 30
        root     31423  0.0  0.0   4360   724 pts/9    S+   15:04   0:00 grep telnet_client.py
        """

        self.response["CLOSE_TELNET_CONNECTION_WITH_NO_PROCESSING"] = """
        something strange output
        root     31423  0.0  0.0   4360   724 pts/9    S+   15:04   0:00 grep telnet_client.py
        """


    def tearDown(self):
        """teardown after all cases"""
        pass

    @mock.patch("os.path.isdir")
    @mock.patch("os.getpid")
    def test_init(self, mock_getpid, mock_isdir):
        """UT"""
        print("Normal checking")
        mock_getpid.return_value = 10000
        mock_isdir.return_value = True

        ins = linux_tool()
        print(self.tool.pprint(ins.default))
        self.assertTrue(re.search(r".10000$", ins.default["ftp_local_tmp_file"]))
        self.assertTrue(re.search(r".10000$", ins.default["telnet_local_tmp_file"]))
        self.assertEqual(ins.default["ftp_local_tmp_file"], os.path.join(ins.default["memory_folder"], ins.default["ftp_script_tmp_filename"]))
        self.assertEqual(ins.default["telnet_local_tmp_file"], os.path.join(ins.default["memory_folder"], ins.default["telnet_script_tmp_filename"]))

        print("No memory folder")
        mock_isdir.return_value = False
        ins = linux_tool()
        print(self.tool.pprint(ins.default))
        self.assertEqual(ins.default["ftp_local_tmp_file"], os.path.join("/tmp", ins.default["ftp_script_tmp_filename"]))
        self.assertEqual(ins.default["telnet_local_tmp_file"], os.path.join("/tmp", ins.default["telnet_script_tmp_filename"]))


    def test_send_shell_cmd(self):
        """test init object with different option"""
        print("check send 1 cmd by string to device")
        mock_device_ins = mock.Mock()
        mock_device_ins.shell.return_value.response.return_value = self.response["HOST_ONE_CMD_RESPONSE"]
        mock_device_ins.log.return_value = True

        response = self.ins.send_shell_cmd(device=mock_device_ins, cmd="du -sh .")
        self.assertTrue(re.search(r"240", response))

        print("check send several cmd by string to device")
        mock_device_ins.shell.return_value.response.return_value = self.response["HOST_MULTI_CMD_RESPONSE"]
        response = self.ins.send_shell_cmd(device=mock_device_ins, cmd=("du -sh .", "ls -l"))
        self.assertTrue(re.search(r"coremgt.py", response))

        print("check invalid option")
        self.assertRaisesRegex(
            TypeError,
            r"'cmd' must be a str",
            self.ins.send_shell_cmd,
            device=mock_device_ins, cmd=None,
        )

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_get_host_info(self, mock_execute_shell_command_on_device):
        """test get host info"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = True

        print("check get host info from CentOS host")
        mock_execute_shell_command_on_device.side_effect = (
            self.response["HOSTNAME_INFO_FROM_CENTOS"],
            self.response["HOST_UNAME_INFO_FROM_CENTOS"],
        )

        response = self.ins.get_host_info(device=mock_device_ins)
        print("response: ", response)
        self.assertTrue(response["hostname"] == "fnd-lnx31.englab.juniper.net")
        self.assertTrue(response["kernel"] == "2.6.32-71")
        self.assertTrue(response["version"] == "el6")
        self.assertTrue(response["kernel_mode"] == "i686")

        print("check get host info from Ubuntu host")

        mock_execute_shell_command_on_device.side_effect = (
            self.response["HOSTNAME_INFO_FROM_UBUNTU"],
            self.response["HOST_UNAME_INFO_FROM_UBUNTU"],
        )
        response = self.ins.get_host_info(device=mock_device_ins)
        print("response: ", response)
        self.assertTrue(response["hostname"] == "hutong-j")
        self.assertTrue(response["kernel"] == "4.4.0")
        self.assertTrue(response["version"] == "62")
        self.assertTrue(response["kernel_mode"] == "generic")

        print("check get host info from unknown platform")

        mock_execute_shell_command_on_device.side_effect = (
            self.response["HOSTNAME_INFO_FROM_UNKNOWN"],
            self.response["HOST_UNAME_INFO_FROM_UNKNOWN"],
        )
        response = self.ins.get_host_info(device=mock_device_ins)
        print("response: ", response)
        self.assertTrue(response["hostname"] == "unknown_host")
        self.assertTrue(response["kernel"] == "")
        self.assertTrue(response["version"] == "")
        self.assertTrue(response["kernel_mode"] == "")

        print("check get host info from existing host")
        mock_execute_shell_command_on_device.side_effect = (
            self.response["HOSTNAME_INFO_FROM_UBUNTU"],
            self.response["HOST_UNAME_INFO_FROM_UBUNTU"],
        )
        response = self.ins.get_host_info(device=mock_device_ins)
        print("response: ", response)
        self.assertTrue(response["hostname"] == "hutong-j")
        self.assertTrue(response["kernel"] == "4.4.0")
        self.assertTrue(response["version"] == "62")
        self.assertTrue(response["kernel_mode"] == "generic")

    def test_su(self):
        """test su feature"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = True
        mock_device_ins.su.return_value = True

        print("1 host su")
        mock_device_ins.su.return_value = True
        status = self.ins.su(device=mock_device_ins)
        self.assertTrue(status)

        print("more hosts su in one shoot")
        mock_device_ins.su.side_effect = [True, True, True]
        status = self.ins.su(device=[mock_device_ins, mock_device_ins, mock_device_ins])
        self.assertTrue(status)

        print("more hosts su in one shoot but someone failed")
        mock_device_ins.su.side_effect = [True, False, True]
        status = self.ins.su(device=[mock_device_ins, mock_device_ins, mock_device_ins])
        self.assertFalse(status)

    def test_reconnect(self):
        """test reconnect"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.su.return_value = True
        mock_device_ins.reconnect.return_value = True

        print("reconnect 1 device succeed without su")
        mock_device_ins.reconnect.return_value = True
        result = self.ins.reconnect(device=mock_device_ins, su=False)
        self.assertTrue(result)

        print("reconnect more devices succeed without su")
        mock_device_ins.reconnect.side_effect = [True, True, True]
        result = self.ins.reconnect(device=[mock_device_ins, mock_device_ins, mock_device_ins], su=False)
        self.assertTrue(result)

        print("reconnect 1 device succeed and su succeed")
        mock_device_ins.reconnect.side_effect = [True, True]
        mock_device_ins.su.side_effect = [True, True]
        result = self.ins.reconnect(device=mock_device_ins)
        self.assertTrue(result)

        print("reconnect more devices succeed and su succeed")
        mock_device_ins.reconnect.side_effect = [True, True, True]
        mock_device_ins.su.side_effect = [True, True, True]
        result = self.ins.reconnect(device=[mock_device_ins, mock_device_ins, mock_device_ins], su=True)
        self.assertTrue(result)

        print("reconnect 1 devices failed")
        mock_device_ins.reconnect.side_effect = [False, True]
        mock_device_ins.su.return_value = True
        result = self.ins.reconnect(device=mock_device_ins, su=True)
        self.assertFalse(result)

        print("reconnect 1 devices succeed but su fail")
        mock_device_ins.reconnect.side_effect = [True, True]
        mock_device_ins.su.side_effect = [False, True]
        result = self.ins.reconnect(device=mock_device_ins, su=True)
        self.assertFalse(result)

        print("reconnect more devices succeed but su fail")
        mock_device_ins.reconnect.side_effect = [True, True, True, True]
        mock_device_ins.su.side_effect = [True, False, True, True]
        result = self.ins.reconnect(device=[mock_device_ins, mock_device_ins, mock_device_ins], su=True)
        self.assertFalse(result)

    def test_reboot(self):
        """test reboot"""
        mock_device_ins = mock.Mock()

        print("parallel reboot 3 hosts and all success")
        mock_device_ins.reboot.side_effect = [True, True, True]
        # mock_reboot.side_effect = [True, True, True]
        result = self.ins.reboot(device=[mock_device_ins, mock_device_ins, mock_device_ins], on_parallel=True)
        self.assertTrue(result)

        print("parallel reboot 1 hosts and False")
        mock_device_ins.reboot.return_value = False
        result = self.ins.reboot(device=mock_device_ins, on_parallel=True)
        self.assertFalse(result)

        print("parallel reboot 3 hosts and have Failure reboot")
        mock_device_ins.reboot.side_effect = [True, True, False]
        result = self.ins.reboot(device=[mock_device_ins, mock_device_ins, mock_device_ins], on_parallel=True)
        self.assertFalse(result)

        print("reboot 3 hosts one by one and have Failure reboot")
        mock_device_ins.reboot.side_effect = [True, True, False]
        result = self.ins.reboot(device=[mock_device_ins, mock_device_ins, mock_device_ins], on_parallel=False)
        self.assertFalse(result)

        print("reboot 3 hosts one by one and got Exception")
        mock_device_ins.reboot.side_effect = [True, True, Exception]
        result = self.ins.reboot(device=[mock_device_ins, mock_device_ins, mock_device_ins], on_parallel=False)
        self.assertFalse(result)

        print("reboot 3 hosts with normal on_parallel set")
        mock_device_ins.reboot.side_effect = [True, True, True]
        result = self.ins.reboot(device=[mock_device_ins, mock_device_ins, mock_device_ins])
        self.assertTrue(result)

        print("reboot 1 host with normal on_parallel set")
        mock_device_ins.reboot.side_effect = [True, None]
        result = self.ins.reboot(device=mock_device_ins, wait=10, timeout="50", check_interval="60")
        self.assertTrue(result)

    @mock.patch.object(linux_tool, "stop_tcpdump_on_host")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_start_tcpdump_on_host(self, mock_execute_shell_command_on_device, mock_stop_tcpdump_on_host):
        """test start tcpdump on host"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("check start tcpdump and clean previous tcpdump processing")
        mock_stop_tcpdump_on_host.return_value = True
        mock_execute_shell_command_on_device.return_value = self.response["START_TCPDUMP_PROCESS"]
        pid = self.ins.start_tcpdump_on_host(device=mock_device_ins, options="-nni eth1", record_file="/tmp/record.pcap", cleanup_previous=True)
        self.assertTrue(pid == 31289)


        print("check start tcpdump and clean previous tcpdump processing failed")
        mock_stop_tcpdump_on_host.return_value = False
        mock_execute_shell_command_on_device.return_value = self.response["START_TCPDUMP_PROCESS"]
        pid = self.ins.start_tcpdump_on_host(device=mock_device_ins, options="-nni eth1", record_file="/tmp/record.pcap", cleanup_previous=True)
        self.assertTrue(pid == 31289)


        print("check start tcpdump without previous tcpdump processing clean")
        mock_stop_tcpdump_on_host.return_value = True
        mock_execute_shell_command_on_device.return_value = self.response["START_TCPDUMP_PROCESS"]
        pid = self.ins.start_tcpdump_on_host(device=mock_device_ins, options="-nni eth1", record_file="/tmp/record.pcap", cleanup_previous=False)
        self.assertTrue(pid == 31289)


        print("check start tcpdump with invalid response")
        mock_stop_tcpdump_on_host.return_value = True
        mock_execute_shell_command_on_device.return_value = self.response["START_TCPDUMP_PROCESS_INVALID_RESPONSE"]

        self.assertRaisesRegex(
            RuntimeError,
            r"Unknown issue that cannot get PID number",
            self.ins.start_tcpdump_on_host,
            device=mock_device_ins, options="-nni eth1", record_file="/tmp/record.pcap", cleanup_previous=False,
        )

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_stop_tcpdump_on_host(self, mock_execute_shell_command_on_device):
        """test stop tcpdump on host"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("check stop tcpdump without pid")
        mock_execute_shell_command_on_device.side_effect = (
            self.response["NORMAL_STOP_TCPDUMP"],
            self.response["NORMAL_STOP_TCPDUMP_RECORD"],
            self.response["NORMAL_STOP_TCPDUMP_RECORD"],
        )

        response = self.ins.stop_tcpdump_on_host(device=mock_device_ins, get_response=True)
        self.assertTrue(re.search(r"10.208.134.243", response))


        print("check stop tcpdump with no processing")
        mock_execute_shell_command_on_device.side_effect = (
            self.response["STOP_TCPDUMP_WITH_NO_PROCESSING"],
            self.response["NORMAL_STOP_TCPDUMP_RECORD"],
            self.response["NORMAL_STOP_TCPDUMP_RECORD"],
        )

        response = self.ins.stop_tcpdump_on_host(device=mock_device_ins, get_response=True)
        self.assertTrue(response)


        print("check stop tcpdump with pid but don't need response")
        mock_execute_shell_command_on_device.side_effect = (
            self.response["NORMAL_STOP_TCPDUMP"],
            self.response["NORMAL_STOP_TCPDUMP_RECORD"],
            self.response["NORMAL_STOP_TCPDUMP_RECORD"],
        )

        response = self.ins.stop_tcpdump_on_host(device=mock_device_ins, pid="28173", get_response=False)
        self.assertTrue(response)

    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_create_ftp_connection_between_host(self, mock_execute_shell_command_on_device, mock_sleep):
        """test create ftp connection between host"""
        mock_device_ins = mock.Mock()
        mock_device_ins.upload.return_value = True

        print("check create connection in foreground as normal")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_FOREGROUND_RESPONSE"]
        response = self.ins.create_ftp_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1")
        self.assertTrue(re.search(r"Connection refused", response))

        print("check create connection in background as normal")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_BACKGROUND_RESPONSE"]
        pid = self.ins.create_ftp_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", mode="background")
        self.assertTrue(pid == 31289)

        print("check create connection but cannot upload ftp_client")
        mock_device_ins.upload.return_value = False
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_BACKGROUND_RESPONSE"]
        self.assertRaisesRegex(
            RuntimeError,
            r"Upload FTP client script failed",
            self.ins.create_ftp_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", mode="background",
        )

        print("check create connection but got invalid background pid response")
        mock_device_ins.upload.return_value = True
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_BACKGROUND_INVALID_RESPONSE"]
        self.assertRaisesRegex(
            RuntimeError,
            r"Cannot find FTP BACKGROUND PID number",
            self.ins.create_ftp_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", mode="background",
        )

        print("check add special option related firewall")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_BACKGROUND_RESPONSE"]
        response = self.ins.create_ftp_connection_between_host(
            device=mock_device_ins,
            remote_host="1.1.1.1",
            firewall_username="regress",
            firewall_password="MaRtInI",
            mode="background",
        )
        self.assertTrue(response)

        print("check invalid options")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_FOREGROUND_RESPONSE"]
        response = self.ins.create_ftp_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd=("put aaa", "get aaa"), mode="foreground")
        self.assertTrue(re.search(r"Connection refused", response))

        self.assertRaisesRegex(
            ValueError,
            r"Keyword 'cmd' must be a STR",
            self.ins.create_ftp_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", cmd=None, mode="foreground",
        )
        self.assertRaisesRegex(
            ValueError,
            r"'mode' must be one of",
            self.ins.create_ftp_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", mode="unknown",
        )

        self.assertRaisesRegex(
            ValueError,
            r"'python_interpreter' must be one of",
            self.ins.create_ftp_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", python_interpreter="python5",
        )

        print("check hold_time option")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_FOREGROUND_HOLDTIME_RESPONSE"]
        response = self.ins.create_ftp_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd="", hold_time=5, mode="foreground")
        self.assertRegex(response, r"hold '5' secs")

        print("Python3 environment: normal checking")
        mock_execute_shell_command_on_device.side_effect = ["Python 3.6.2", self.response["CREATE_FTP_CONNECTION_FOREGROUND_RESPONSE"]]
        del self.ins.hidden_info[str(mock_device_ins)]
        response = self.ins.create_ftp_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd="", mode="foreground")
        self.assertTrue(response)

        print("set specific python interpreter to python2")
        del self.ins.hidden_info[str(mock_device_ins)]
        mock_execute_shell_command_on_device.side_effect = [self.response["CREATE_FTP_CONNECTION_FOREGROUND_HOLDTIME_RESPONSE"], ]
        response = self.ins.create_ftp_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd="", python_interpreter="Python2")
        self.assertTrue(response)

        print("set specific python interpreter to python3")
        mock_execute_shell_command_on_device.side_effect = [self.response["CREATE_FTP_CONNECTION_FOREGROUND_RESPONSE"], ]
        response = self.ins.create_ftp_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd="", python_interpreter="3")
        self.assertTrue(response)

        print("Python3 environment: cannot find ftp_client from lib")
        del self.ins.hidden_info[str(mock_device_ins)]
        python3_ftp_client_file = self.ins.default["python3_ftp_client_file"]
        self.ins.default["python3_ftp_client_file"] = None
        self.assertRaisesRegex(
            RuntimeError,
            r"cannot find ftp_client.py from toby library",
            self.ins.create_ftp_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", cmd="", python_interpreter="3",
        )
        self.ins.default["python3_ftp_client_file"] = python3_ftp_client_file

        print("check cannot get pid from command response")
        mock_execute_shell_command_on_device.side_effect = ["", "12345"]
        response = self.ins.create_ftp_connection_between_host(
            device=mock_device_ins,
            remote_host="1.1.1.1",
            mode="background",
        )
        self.assertIsInstance(response, int)

        print("check if no need pid")
        mock_execute_shell_command_on_device.side_effect = ["", "12345"]
        response = self.ins.create_ftp_connection_between_host(
            device=mock_device_ins,
            remote_host="1.1.1.1",
            mode="background",
            no_need_pid=True,
        )
        self.assertTrue(response)

        print("check upload ftp_client file exception")
        mock_device_ins.upload.side_effect = FileNotFoundError
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_FTP_CONNECTION_BACKGROUND_INVALID_RESPONSE"]
        self.assertRaisesRegex(
            RuntimeError,
            r"Upload FTP client script failed",
            self.ins.create_ftp_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", mode="background",
        )

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_close_ftp_connection_between_host(self, mock_execute_shell_command_on_device):
        """test close ftp connection between host"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = True

        print("check close ftp connection as normal")
        mock_execute_shell_command_on_device.side_effect = (self.response["NORMAL_CLOSE_FTP_CONNECTION"], "")
        response = self.ins.close_ftp_connection_between_host(device=mock_device_ins)
        self.assertTrue(response)

        print("check close ftp connection but no process")
        mock_execute_shell_command_on_device.side_effect = (self.response["CLOSE_FTP_CONNECTION_WITH_NO_PROCESSING"], "")
        response = self.ins.close_ftp_connection_between_host(device=mock_device_ins)
        self.assertTrue(response)

        print("check close ftp connection with pid")
        mock_execute_shell_command_on_device.side_effect = (self.response["CLOSE_FTP_CONNECTION_WITH_NO_PROCESSING"], "")
        response = self.ins.close_ftp_connection_between_host(device=mock_device_ins, pid=11129)
        self.assertTrue(response)

    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_create_telnet_connection_between_host(self, mock_execute_shell_command_on_device, mock_sleep):
        """test create telnet connection between host"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.upload.return_value = True

        print("check create connection in foreground as normal")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_TELNET_CONNECTION_FOREGROUND_RESPONSE"]
        response = self.ins.create_telnet_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", mode="foreground")
        print(response)
        self.assertTrue(re.search(r"regress@fnd-lnx31", response))

        print("check create connection in background as normal")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_TELNET_CONNECTION_BACKGROUND_RESPONSE"]
        pid = self.ins.create_telnet_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", mode="background", cmd="ls -l")
        self.assertTrue(pid == 31289)

        print("check create connection in background as normal")
        pid = self.ins.create_telnet_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", mode="background", cmd=("ls -l", "du -h"))
        self.assertTrue(pid == 31289)

        print("check create connection but cannot upload telnet_client")
        mock_device_ins.upload.return_value = False
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_TELNET_CONNECTION_BACKGROUND_RESPONSE"]
        self.assertRaisesRegex(
            RuntimeError,
            r"Upload TELNET client script failed",
            self.ins.create_telnet_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", mode="background",
        )

        print("check create connection but got invalid background pid response")
        mock_device_ins.upload.return_value = True
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_TELNET_CONNECTION_BACKGROUND_INVALID_RESPONSE"]
        self.assertRaisesRegex(
            RuntimeError,
            r"Cannot find TELNET BACKGROUND PID number",
            self.ins.create_telnet_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", mode="background",
        )


        print("check add special option related firewall")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_TELNET_CONNECTION_BACKGROUND_RESPONSE"]
        response = self.ins.create_telnet_connection_between_host(
            device=mock_device_ins,
            remote_host="1.1.1.1",
            firewall_username="regress",
            firewall_password="MaRtInI",
            mode="background",
        )
        self.assertIsInstance(response, int)

        print("check invalid options")
        mock_execute_shell_command_on_device.return_value = self.response["CREATE_TELNET_CONNECTION_FOREGROUND_RESPONSE"]

        self.assertRaisesRegex(
            ValueError,
            r"Keyword 'cmd' must be a STR",
            self.ins.create_telnet_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", cmd=object, mode="foreground",
        )

        self.assertRaisesRegex(
            ValueError,
            r"'mode' must be one of",
            self.ins.create_telnet_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", mode="unknown",
        )

        self.assertRaisesRegex(
            ValueError,
            r"'python_interpreter' must be one of",
            self.ins.create_telnet_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", python_interpreter="python5",
        )

        print("check python_interpreter for python3 from python version auto check")
        mock_execute_shell_command_on_device.side_effect = ["Python 3.6.2", self.response["CREATE_TELNET_CONNECTION_FOREGROUND_RESPONSE"]]
        del self.ins.hidden_info[str(mock_device_ins)]
        response = self.ins.create_telnet_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd="", mode="foreground")
        self.assertTrue(response)

        print("check python_interpreter for python2")
        del self.ins.hidden_info[str(mock_device_ins)]
        mock_execute_shell_command_on_device.side_effect = [self.response["CREATE_TELNET_CONNECTION_BACKGROUND_RESPONSE"], ]
        response = self.ins.create_telnet_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd="", python_interpreter="Python2")
        self.assertTrue(response)

        print("check python_interpreter for python3 by user set")
        mock_execute_shell_command_on_device.side_effect = [self.response["CREATE_TELNET_CONNECTION_BACKGROUND_RESPONSE"], ]
        response = self.ins.create_telnet_connection_between_host(device=mock_device_ins, remote_host="1.1.1.1", cmd="", python_interpreter="3")
        self.assertTrue(response)

        print("check recreate device contain for python3")
        del self.ins.hidden_info[str(mock_device_ins)]
        default_telnet_client_file = copy.deepcopy(self.ins.default["python3_telnet_client_file"])
        self.ins.default["python3_telnet_client_file"] = None
        self.assertRaisesRegex(
            RuntimeError,
            r"cannot find telnet_client.py from toby library",
            self.ins.create_telnet_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", cmd="", python_interpreter="3",
        )
        self.ins.default["python3_telnet_client_file"] = default_telnet_client_file

        print("check option to_srx_device")
        mock_execute_shell_command_on_device.side_effect = [self.response["CREATE_TELNET_CONNECTION_BACKGROUND_RESPONSE"], ]
        response = self.ins.create_telnet_connection_between_host(
            device=mock_device_ins,
            remote_host="1.1.1.1",
            to_srx_device=True,
            mode="background",
        )
        self.assertIsInstance(response, int)

        print("check cannot get pid from command response")
        mock_execute_shell_command_on_device.side_effect = ["", "12345"]
        response = self.ins.create_telnet_connection_between_host(
            device=mock_device_ins,
            remote_host="1.1.1.1",
            firewall_username="regress",
            firewall_password="MaRtInI",
            mode="background",
        )
        self.assertIsInstance(response, int)

        print("check if don't need pid")
        mock_execute_shell_command_on_device.side_effect = ["", "12345"]
        response = self.ins.create_telnet_connection_between_host(
            device=mock_device_ins,
            remote_host="1.1.1.1",
            mode="background",
            no_need_pid=True,
        )
        self.assertTrue(response)

        print("Got exception during upload")
        mock_device_ins.upload.side_effect = FileNotFoundError
        self.assertRaisesRegex(
            RuntimeError,
            r"Upload TELNET client script failed",
            self.ins.create_telnet_connection_between_host,
            device=mock_device_ins, remote_host="1.1.1.1", cmd="", python_interpreter="3",
        )

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_close_telnet_connection_between_host(self, mock_execute_shell_command_on_device):
        """test close telnet connection between host"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("check close telnet connection as normal")
        mock_execute_shell_command_on_device.side_effect = (self.response["NORMAL_CLOSE_TELNET_CONNECTION"], "")
        response = self.ins.close_telnet_connection_between_host(device=mock_device_ins)
        self.assertTrue(response)

        print("check close telnet connection but no process")
        mock_execute_shell_command_on_device.side_effect = (self.response["CLOSE_TELNET_CONNECTION_WITH_NO_PROCESSING"], "")
        response = self.ins.close_telnet_connection_between_host(device=mock_device_ins)
        self.assertTrue(response)

        print("check close telnet connection with pid")
        mock_execute_shell_command_on_device.side_effect = (self.response["CLOSE_TELNET_CONNECTION_WITH_NO_PROCESSING"], "")
        response = self.ins.close_telnet_connection_between_host(device=mock_device_ins, pid=11129)
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_sendip_source_ip_increase(self, mock_execute_shell_command_on_device):
        """test create sendip script and execute"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Create sendip script and execute with IPv6 tcp")
        response = self.ins.sendip_source_ip_increase(device=mock_device_ins, ip_option="ipv6", src_ip="2000::2", dst_ip="2000:1::2",
        src_port=1, dst_port=1, total_count=6, port_count=3, re_send_time=1, ip_count=2,
        size="r64", protocol="tcp", timeout=1200, delete_file="no", file_name="sendip_script_v6.sh")
        self.assertTrue(response)

        print("Create sendip script and execute with IPv6 address 2000::1:2")
        response = self.ins.sendip_source_ip_increase(device=mock_device_ins, ip_option="ipv6", src_ip="2000::1:2", dst_ip="2000:1::2",
        src_port=1, dst_port=1, total_count=6, port_count=3, re_send_time=1, ip_count=2,
        size="r64", protocol="tcp", timeout=1200, delete_file="no", file_name="sendip_script_v6.sh")
        self.assertTrue(response)

        print("Create sendip script and execute with IPv6 address 2000::1:2:3")
        response = self.ins.sendip_source_ip_increase(device=mock_device_ins, ip_option="ipv6", src_ip="2000:1:2:3:4:5:6:a", dst_ip="2000:1::2",
        src_port=1, dst_port=1, total_count=6, port_count=3, re_send_time=1, ip_count=2,
        size="r64", protocol="tcp", timeout=1200, delete_file="no", file_name="sendip_script_v6.sh")
        self.assertTrue(response)

        print("Create sendip script and execute with IPv4 udp")
        response = self.ins.sendip_source_ip_increase(device=mock_device_ins, src_ip="1.1.1.2", dst_ip="2.2.2.2",
        re_send_time="2")
        self.assertTrue(response)

        print("Create sendip script and execute with IPv4 icmp")
        response = self.ins.sendip_source_ip_increase(device=mock_device_ins, src_ip="1.1.1.2", dst_ip="2.2.2.2", protocol="icmp",
        src_port=1, dst_port=1)
        self.assertTrue(response)

        print("Create sendip script and execute with IPv6 tcp with dst IP increase")
        response = self.ins.sendip_source_ip_increase(device=mock_device_ins, ip_option="ipv6", src_ip="2000::2", dst_ip="2000:1::2",
        src_port=1, dst_port=1, total_count=6, port_count=3, re_send_time=1, ip_count=2,
        size="r64", protocol="tcp", timeout=1200, delete_file="no", file_name="sendip_script_v6.sh",
        type_option="source_destination_ip_increase_both")
        self.assertTrue(response)

        print("Create sendip script and execute with IPv4 udp")
        response = self.ins.sendip_source_ip_increase(device=mock_device_ins, src_ip="1.1.1.2", dst_ip="2.2.2.2",
        re_send_time="2", type_option="source_destination_ip_increase_both")
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_send_packet_by_pktgen(self, mock_execute_shell_command_on_device):
        """UT Case"""
        device_object = mock.Mock()
        device_object.log = mock.Mock()

        pktgen_mode_loaded_output = """pktgen                 49097  0"""
        pktgen_folder_ls_output_without_intf = """
total 0
-rw------- 1 root root 0 Nov 12 09:45 kpktgend_0
-rw------- 1 root root 0 Nov 12 09:45 kpktgend_1
-rw------- 1 root root 0 Nov 12 09:45 kpktgend_2
-rw------- 1 root root 0 Nov 12 09:45 kpktgend_3
-rw------- 1 root root 0 Nov 12 09:45 pgctrl
        """

        pktgen_folder_ls_output_with_intf = """
total 0
-rw------- 1 root root 0 Nov 12 09:43 eth1
-rw------- 1 root root 0 Nov 12 09:43 kpktgend_0
-rw------- 1 root root 0 Nov 12 09:43 kpktgend_1
-rw------- 1 root root 0 Nov 12 09:43 kpktgend_2
-rw------- 1 root root 0 Nov 12 09:43 kpktgend_3
-rw------- 1 root root 0 Nov 12 09:43 pgctrl
        """

        pktgen_show_configred_intf_output = """
Params: count 100  min_pkt_size: 46  max_pkt_size: 150
     frags: 0  delay: 1000  clone_skb: 0  ifname: eth1
     flows: 0 flowlen: 0
     queue_map_min: 0  queue_map_max: 0
     dst_min: 110.1.1.2  dst_max:
        src_min:   src_max:
     src_mac: 00:50:56:b0:f9:9b dst_mac: 00:50:56:b0:ff:32
     udp_src_min: 7  udp_src_max: 7  udp_dst_min: 7  udp_dst_max: 7
     src_mac_count: 0  dst_mac_count: 0
     Flags: TXSIZE_RND
Current:
     pkts-sofar: 100  errors: 0
     started: 237805446054us  stopped: 237805446284us idle: 131us
     seq_num: 101  cur_dst_mac_offset: 0  cur_src_mac_offset: 0
     cur_saddr: 110.1.1.1  cur_daddr: 110.1.1.2
     cur_udp_dst: 7  cur_udp_src: 7
     cur_queue_map: 0
     flows: 0
Result: OK: 229(c98+d131) usec, 100 (96byte,0frags)
  435153pps 334Mb/sec (334197504bps) errors: 0
        """

        print("Most default arguments")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            pktgen_mode_loaded_output,
            pktgen_folder_ls_output_without_intf,
            "", # reset
            "", # add_device
            pktgen_folder_ls_output_with_intf,
            "", "", "", "", "", "", "", "",
            pktgen_show_configred_intf_output,
            "",
        )

        response = self.ins.send_packet_by_pktgen(device=device_object, dst_mac="00:00:00:00:00:01")
        self.assertTrue(response)

        print("background and other arguments")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            pktgen_mode_loaded_output,
            pktgen_folder_ls_output_without_intf,
            "", # reset
            "", # add_device
            pktgen_folder_ls_output_with_intf,
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
            pktgen_show_configred_intf_output,
            "[1] 9520",
        )
        response = self.ins.send_packet_by_pktgen(
            device=device_object, dst_mac="00:00:00:00:00:01", count="0",
            src_min="192.168.1.10", src_max="192.168.1.100",
            dst_min="192.168.2.10", dst_max="192.168.2.100",
            dst6_min="2000:121:11:10::1", dst6_max="2000:121:11:10::f",
            udp_src_min="1024", udp_src_max="65535",
            udp_dst_min="1024", udp_dst_max="65535",
            min_pkt_size="46", max_pkt_size="1500",
        )
        self.assertTrue(response)


        print("error situation 1")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
        )
        response = self.ins.send_packet_by_pktgen(device=device_object, dst_mac="00:00:00:00:00:01")
        self.assertFalse(response)

        print("error situation 2")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            pktgen_mode_loaded_output,
            "",
        )
        response = self.ins.send_packet_by_pktgen(device=device_object, dst_mac="00:00:00:00:00:01")
        self.assertFalse(response)

        print("error situation 3")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            pktgen_mode_loaded_output,
            pktgen_folder_ls_output_without_intf,
            "", # reset
            "", # add_device
            "",
        )
        response = self.ins.send_packet_by_pktgen(device=device_object, dst_mac="00:00:00:00:00:01")
        self.assertFalse(response)

    @mock.patch("jnpr.toby.hldcl.juniper.security.robot_keyword.loop_ping")
    def test_loop_ping(self, mock_loop_ping):
        """UT Case"""
        mock_loop_ping.return_value = True
        response = self.ins.loop_ping(device=None, dst_addr=None)
        self.assertTrue(response)

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_create_nfs_connection_between_host(self, mock_execute_shell_command):
        """UT Case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = True

        print("Normal testing")

        mock_execute_shell_command.return_value = """
tmpfs on /run/user/500 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700,uid=500,gid=500)
tmpfs on /run/user/0 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700)
121.11.20.2:/tmp on /dev/shm/nfs type nfs4 (rw,relatime,vers=4.1,rsize=262144,wsize=262144,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=10.208.129.115,local_lock=none,addr=10.208.129.147)
       """
        status = self.ins.create_nfs_connection_between_host(
            device=mock_device_ins,
            remote_host="121.11.20.2",
            remote_path="/tmp",
            local_path="/dev/shm/nfs",
            service_control_tool="SYSTEMCTL",
        )
        self.assertTrue(status)

        print("Invalid options")
        self.assertRaisesRegex(
            ValueError,
            r"option 'service_control_tool' must be",
            self.ins.create_nfs_connection_between_host,
            device=mock_device_ins, remote_host="121.11.20.2", service_control_tool="unknown",
        )

        print("Mount failed")
        mock_execute_shell_command.return_value = """
tmpfs on /run/user/500 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700,uid=500,gid=500)
tmpfs on /run/user/0 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700)
       """
        status = self.ins.create_nfs_connection_between_host(
            device=mock_device_ins,
            remote_host="121.11.20.2",
            remote_path="/tmp",
            local_path="/dev/shm/nfs",
            service_control_tool="service",
        )
        self.assertFalse(status)

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_close_nfs_connection_between_host(self, mock_execute_shell_command):
        """UT Case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = True

        print("Normal testing")

        mock_execute_shell_command.return_value = """
tmpfs on /run/user/500 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700,uid=500,gid=500)
tmpfs on /run/user/0 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700)
       """
        status = self.ins.close_nfs_connection_between_host(
            device=mock_device_ins,
            remote_host="121.11.20.2",
            remote_path="/tmp",
            local_path="/dev/shm/nfs",
            service_control_tool="SYSTEMCTL",
        )
        self.assertTrue(status)

        print("Invalid options")
        self.assertRaisesRegex(
            ValueError,
            r"option 'service_control_tool' must be",
            self.ins.close_nfs_connection_between_host,
            device=mock_device_ins, remote_host="121.11.20.2", service_control_tool="unknown",
        )

        print("Mount failed")
        mock_execute_shell_command.return_value = """
tmpfs on /run/user/500 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700,uid=500,gid=500)
tmpfs on /run/user/0 type tmpfs (rw,nosuid,nodev,relatime,size=186328k,mode=700)
121.11.20.2:/tmp on /dev/shm/nfs type nfs4 (rw,relatime,vers=4.1,rsize=262144,wsize=262144,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=10.208.129.115,local_lock=none,addr=10.208.129.147)
       """
        status = self.ins.close_nfs_connection_between_host(
            device=mock_device_ins,
            remote_host="121.11.20.2",
            remote_path="/tmp",
            local_path="/dev/shm/nfs",
            service_control_tool="service",
        )
        self.assertFalse(status)

    @mock.patch.object(linux_tool, "get_host_info")
    def test_get_service_management_tool(self, mock_get_host_info):
        """UT case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = True

        mock_get_host_info.return_value = {"version": "el6", }
        self.assertEqual(self.ins.get_service_management_tool(device=mock_device_ins), "service")

        # get from cache
        self.assertEqual(self.ins.get_service_management_tool(device=mock_device_ins), "service")

        # force get
        mock_get_host_info.return_value = {"version": "el7", }
        self.assertEqual(self.ins.get_service_management_tool(device=mock_device_ins, force=True), "systemctl")

        # force get for ubuntu
        mock_get_host_info.return_value = {"version": "2.4.3-1.generic", }
        self.assertEqual(self.ins.get_service_management_tool(device=mock_device_ins, force=True), "service")

        # force get for unknown
        mock_get_host_info.return_value = {"version": "2.4.3-1.fedro", }
        self.assertEqual(self.ins.get_service_management_tool(device=mock_device_ins, force=True), "unknown")
