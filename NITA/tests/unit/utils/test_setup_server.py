# coding: UTF-8
"""All unit test cases for setup_server module"""
# pylint: disable=invalid-name,attribute-defined-outside-init

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
from unittest import TestCase, mock
import unittest
from mock import MagicMock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.linux.linux_tool import linux_tool
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.setup_server import setup_server


class TestSetupServer(TestCase):
    """All unit test cases for setup_server module"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.ins = setup_server()
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    def tearDown(self):
        """teardown after all cases"""
        pass

    @mock.patch.object(linux_tool, "get_service_management_tool")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_start_ftp_service(self, mock_execute_shell_command_on_device, mock_get_service_management_tool):
        """test init object with different option"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("start vsftpd service with default configuration by systemctl tool")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            "",
            """
            vsftpd.service - Vsftpd ftp daemon
            Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; disabled)
            Active: active (running) since Fri 2017-03-10 01:22:02 EST; 41s ago
            Process: 9227 ExecStart=/usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf (code=exited, status=0/SUCCESS)
            Main PID: 9228 (vsftpd)
            CGroup: /system.slice/vsftpd.service
                    └─9228 /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf

            Mar 10 01:22:02 NET-VM33 systemd[1]: Started Vsftpd ftp daemon.
            """,
        )

        response = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="systemctl", return_conf=True)
        self.assertTrue(response["status"])
        lines = response["conf"]
        self.assertTrue(re.search(r"anonymous_enable=YES", lines))
        self.assertTrue(re.search(r"anon_mkdir_write_enable=YES", lines))
        self.assertTrue(re.search(r"anon_upload_enable=YES", lines))
        self.assertTrue(re.search(r"anon_other_write_enable=YES", lines))
        self.assertTrue(re.search(r"local_enable=YES", lines))
        self.assertTrue(re.search(r"write_enable=YES", lines))
        self.assertTrue(re.search(r"local_umask=022", lines))
        self.assertTrue(re.search(r"dirmessage_enable=YES", lines))
        self.assertTrue(re.search(r"xferlog_enable=YES", lines))
        self.assertTrue(re.search(r"xferlog_std_format=YES", lines))
        # self.assertTrue(re.search(r"userlist_enable=YES", lines))
        self.assertTrue(re.search(r"tcp_wrappers=YES", lines))
        self.assertTrue(re.search(r"connect_from_port_20=YES", lines))
        self.assertTrue(re.search(r"listen=YES", lines))
        self.assertTrue(re.search(r"pasv_enable=YES", lines))

        print("start vsftpd service by service tool")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            """
            Shutting down vsftpd:                                      [  OK  ]
            Starting vsftpd for vsftpd:                                [  OK  ]
            """,
            """
            vsftpd (pid 31976) is running...
            """,
        )

        mock_get_service_management_tool.return_value = "service"
        banner = "This is UNIT TEST ftp server"
        response = self.ins.start_ftp_service(
            device=mock_device_ins,
            listen_port=2121,
            ipv6_support=True,
            passive_mode=False,
            banner=banner,
            max_rate=10240,         # 10K/s
            return_conf=True,
        )
        self.assertTrue(response["status"])

        print("checking option 'more_configuration'")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            """
            Shutting down vsftpd:                                      [  OK  ]
            Starting vsftpd for vsftpd:                                [  OK  ]
            """,
            """
            vsftpd (pid 31976) is running...
            """,
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, more_configuration="new_config=YES")
        self.assertTrue(status)

        mock_get_service_management_tool.return_value = "unknown"
        print("checking option 'more_configuration'")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            """
            Shutting down vsftpd:                                      [  OK  ]
            Starting vsftpd for vsftpd:                                [  OK  ]
            """,
            """
            vsftpd (pid 31976) is running...
            """,
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, more_configuration=["new_config=YES", "new_config1=YES"])
        self.assertTrue(status)

        mock_get_service_management_tool.return_value = "service"
        print("checking option 'more_configuration'")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            """
            Shutting down vsftpd:                                      [  OK  ]
            Starting vsftpd for vsftpd:                                [  OK  ]
            """,
            """
            vsftpd (pid 31976) is running...
            """,
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, more_configuration=object)
        self.assertTrue(status)

        lines = response["conf"]
        self.assertTrue(re.search(r"listen_port=2121", lines))
        self.assertTrue(re.search(r"connect_from_port_20=YES", lines))
        self.assertTrue(re.search(r"listen_ipv6=YES", lines))
        self.assertTrue(re.search(r"pasv_enable=NO", lines))
        self.assertTrue(re.search(banner, lines))
        self.assertTrue(re.search(r"local_max_rate=10240", lines))
        self.assertTrue(re.search(r"anon_max_rate=10240", lines))

        print("start vsftpd service only restart status")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            """
            Shutting down vsftpd:                                      [  OK  ]
            Starting vsftpd for vsftpd:                                [  OK  ]
            """,
            """
            vsftpd (pid 31976) is running...
            """,
        )
        status = self.ins.start_ftp_service(device=mock_device_ins)
        self.assertTrue(status)

        print("start vsftpd service with invalid option")
        status = False
        try:
            self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="whatever")
        except ValueError as err:
            print(err)
            status = True
        self.assertTrue(status)

        print("Use systemctl start vsftpd service with runtime error")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            "",
            """Failed to issue method call: Access denied""",
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(status)

        print("Use service start vsftpd service with runtime error")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            """
            Shutting down vsftpd:                                      [FAILED]
            Starting vsftpd for vsftpd: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd.conf
                                                                       [FAILED]
            Starting vsftpd for vsftpd_ipv6: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd_ipv6.conf
                                                                       [FAILED]
            """,
            """vsftpd is not running...""",
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="service")
        self.assertFalse(status)

        print("Use service start vsftpd service with runtime error")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            """
            Shutting down vsftpd:                                      [FAILED]
            Starting vsftpd for vsftpd: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd.conf
                                                                       [FAILED]
            Starting vsftpd for vsftpd_ipv6: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd_ipv6.conf
                                                                       [FAILED]
            """,
            """vsftpd is stopped""",
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="service")
        self.assertFalse(status)


        print("Use systemctl start vsftpd service with runtime error")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            "",
            """
            vsftpd.service - Vsftpd ftp daemon
               Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; disabled)
               Active: inactive (dead)

            Mar 10 01:22:02 NET-VM33 systemd[1]: Starting Vsftpd ftp daemon...
            Mar 10 01:22:02 NET-VM33 systemd[1]: Started Vsftpd ftp daemon.
            Mar 10 02:37:06 NET-VM33 systemd[1]: Stopping Vsftpd ftp daemon...
            Mar 10 02:37:06 NET-VM33 systemd[1]: Stopped Vsftpd ftp daemon.
            """,
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(status)

        print("checking no backup vsftpd configuration file and re-created...")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            "",
            "",
            """ls: cannot access 'vsftpd.conf': No such file or directory""",
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="service")
        self.assertFalse(status)

        print("checking restart vsftpd failed by service...")
        mock_execute_shell_command_on_device.side_effect = (
            """ls: cannot access 'vsftpd.conf': No such file or directory""",
            "",
            "",
            """
            Shutting down vsftpd:                                      [FAILED]
            Starting vsftpd for vsftpd: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd.conf
                                                                       [FAILED]
            Starting vsftpd for vsftpd_ipv6: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd_ipv6.conf
                                                                       [FAILED]
            """,
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="service")
        self.assertFalse(status)

        print("checking start vsftpd failed by systemctl...")
        mock_execute_shell_command_on_device.side_effect = (
            """""",
            """""",
            """Permission denied""",
            """
            Shutting down vsftpd:                                      [FAILED]
            Starting vsftpd for vsftpd: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd.conf
                                                                       [FAILED]
            Starting vsftpd for vsftpd_ipv6: 500 OOPS: cannot read config file: /etc/vsftpd/vsftpd_ipv6.conf
                                                                       [FAILED]
            """,
        )
        status = self.ins.start_ftp_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(status)

    @mock.patch.object(linux_tool, "get_service_management_tool")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_stop_ftp_service(self, mock_execute_shell_command_on_device, mock_get_service_management_tool):
        """test init object with different option"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_get_service_management_tool.return_value = "service"

        print("stop FTP service by systemctl")
        mock_execute_shell_command_on_device.side_effect = (
            "",
            """
            vsftpd.service - Vsftpd ftp daemon
               Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; disabled)
               Active: inactive (dead)

            Mar 10 01:22:02 NET-VM33 systemd[1]: Starting Vsftpd ftp daemon...
            Mar 10 01:22:02 NET-VM33 systemd[1]: Started Vsftpd ftp daemon.
            Mar 10 02:37:06 NET-VM33 systemd[1]: Stopping Vsftpd ftp daemon...
            Mar 10 02:37:06 NET-VM33 systemd[1]: Stopped Vsftpd ftp daemon.
            """,
        )
        result = self.ins.stop_ftp_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertTrue(result)

        mock_execute_shell_command_on_device.side_effect = [
            "",
            """
            vsftpd.service - Vsftpd ftp daemon
               Loaded: loaded (/usr/lib/systemd/system/vsftpd.service; disabled)
               Active: active

            Mar 10 01:22:02 NET-VM33 systemd[1]: Starting Vsftpd ftp daemon...
            Mar 10 01:22:02 NET-VM33 systemd[1]: Started Vsftpd ftp daemon.
            Mar 10 02:37:06 NET-VM33 systemd[1]: Stopping Vsftpd ftp daemon...
            Mar 10 02:37:06 NET-VM33 systemd[1]: Stopped Vsftpd ftp daemon.
            """,
        ]

        result = self.ins.stop_ftp_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(result)


        print("stop FTP service by service")
        mock_execute_shell_command_on_device.side_effect = [
            "",
            """vsftpd is stopped""",
        ]
        result = self.ins.stop_ftp_service(device=mock_device_ins, service_control_tool="service")
        self.assertTrue(result)


        print("stop FTP service with invalid option")
        status = False
        try:
            self.ins.stop_ftp_service(device=mock_device_ins, service_control_tool="whatever")
        except ValueError as err:
            print("Error with invalid option: ", err)
            status = True
        self.assertTrue(status)

        print("stop FTP service by systemctl with wrong output")
        mock_execute_shell_command_on_device.side_effect = [
            "",
            """Failed to issue method call: Access denied""",
        ]
        result = self.ins.stop_ftp_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(result)

        mock_execute_shell_command_on_device.side_effect = [
            """Shutting down vsftpd:                                      [FAILED]""",
            "",
        ]

        print("stop FTP service by service with wrong output")
        result = self.ins.stop_ftp_service(device=mock_device_ins, service_control_tool="service")
        self.assertFalse(result)

        mock_execute_shell_command_on_device.side_effect = [
            """Permission denied""",
            """""",
        ]

        print("stop FTP service by systemctl with wrong output")
        result = self.ins.stop_ftp_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(result)

    @mock.patch.object(linux_tool, "get_service_management_tool")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_start_telnet_service_by_default_option(self, mock_send_shell_cmd, mock_get_service_management_tool):
        """test init object with different option"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_get_service_management_tool.return_value = "service"

        print("checking start TELNET service with invalid option")

        status = False
        mock_send_shell_cmd.return_value = ""
        try:
            self.ins.start_telnet_service(device=mock_device_ins, service_control_tool="whatever")
        except ValueError as err:
            print("checking with invalid option: ", err)
            status = True
        self.assertTrue(status)

        print("start TELNET service by systemctl")
        mock_send_shell_cmd.return_value = "No such file or directory"
        result = self.ins.start_telnet_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(result)

        print("checking start TELNET service by systemctl and create backup file")
        mock_send_shell_cmd.return_value = ""
        result = self.ins.start_telnet_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(result)


        print("checking start TELNET service by systemctl")
        mock_send_shell_cmd.return_value = """
            (No info could be read for "-p": geteuid()=1000 but you should be root.)
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
            tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -
            tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
            tcp        0      0 192.168.122.1:53        0.0.0.0:*               LISTEN      -
            tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
            tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      -
            tcp6       0      0 :::22                   :::*                    LISTEN      -
            tcp6       0      0 :::23                   :::*                    LISTEN      -
            tcp6       0      0 ::1:25                  :::*                    LISTEN      -
            tcp6       0      0 :::443                  :::*                    LISTEN      -
            tcp6       0      0 :::8000                 :::*                    LISTEN      -
            udp        0      0 192.168.122.1:53        0.0.0.0:*                           -
            udp        0      0 0.0.0.0:67              0.0.0.0:*                           -
            udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
            udp        0      0 0.0.0.0:123             0.0.0.0:*                           -
            udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
            udp        0      0 127.0.0.1:323           0.0.0.0:*                           -
            udp        0      0 0.0.0.0:36421           0.0.0.0:*                           -
            udp        0      0 0.0.0.0:28284           0.0.0.0:*                           -
            udp6       0      0 :::123                  :::*                                -
            udp6       0      0 :::36109                :::*                                -
            udp6       0      0 ::1:323                 :::*                                -
        """
        result = self.ins.start_telnet_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertTrue(result)


        print("checking TELNET configuration by systemctl")
        response = self.ins.start_telnet_service(device=mock_device_ins, service_control_tool="systemctl", return_conf=True)
        lines = response["conf"]
        self.assertTrue(re.search(r"Unit", lines))
        self.assertTrue(re.search(r"ListenStream=23", lines))
        self.assertTrue(response["status"])

        print("checking start TELNET service by service")
        mock_send_shell_cmd.return_value = """
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address               Foreign Address             State       PID/Program name
            tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN      1283/rsyslogd
            tcp        0      0 0.0.0.0:111                 0.0.0.0:*                   LISTEN      1351/rpcbind
            tcp        0      0 0.0.0.0:35765               0.0.0.0:*                   LISTEN      1369/rpc.statd
            tcp        0      0 0.0.0.0:22                  0.0.0.0:*                   LISTEN      1612/sshd
            tcp        0      0 127.0.0.1:25                0.0.0.0:*                   LISTEN      1707/master
            tcp        0      0 :::514                      :::*                        LISTEN      1283/rsyslogd
            tcp        0      0 :::111                      :::*                        LISTEN      1351/rpcbind
            tcp        0      0 :::21                       :::*                        LISTEN      11293/vsftpd
            tcp        0      0 :::22                       :::*                        LISTEN      1612/sshd
            tcp        0      0 :::23                       :::*                        LISTEN      22399/xinetd
            tcp        0      0 :::38743                    :::*                        LISTEN      1369/rpc.statd
            tcp        0      0 ::1:25                      :::*                        LISTEN      1707/master
            udp        0      0 0.0.0.0:514                 0.0.0.0:*                               1283/rsyslogd
            udp        0      0 0.0.0.0:678                 0.0.0.0:*                               1351/rpcbind
            udp        0      0 0.0.0.0:697                 0.0.0.0:*                               1369/rpc.statd
            udp        0      0 0.0.0.0:46027               0.0.0.0:*                               1369/rpc.statd
            udp        0      0 0.0.0.0:111                 0.0.0.0:*                               1351/rpcbind
            udp        0      0 :::514                      :::*                                    1283/rsyslogd
            udp        0      0 :::678                      :::*                                    1351/rpcbind
            udp        0      0 :::38753                    :::*                                    1369/rpc.statd
            udp        0      0 :::111                      :::*                                    1351/rpcbind
        """
        result = self.ins.start_telnet_service(device=mock_device_ins, service_control_tool="service")
        self.assertTrue(result)

        print("checking TELNET configuration by service")
        response = self.ins.start_telnet_service(device=mock_device_ins, service_control_tool="service", return_conf=True)
        lines = response["conf"]
        self.assertTrue(re.search(r"flags\s+=\s+IPv6", lines, re.I))
        self.assertTrue(response["status"])

    @mock.patch.object(linux_tool, "get_service_management_tool")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_stop_telnet_service(self, mock_send_shell_cmd, mock_get_service_management_tool):
        """test init object with different option"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_get_service_management_tool.return_value = "service"

        print("checking invalid option")
        mock_send_shell_cmd.return_value = ""
        status = False
        try:
            self.ins.stop_telnet_service(device=mock_device_ins, service_control_tool="whatever")
        except ValueError as err:
            print("checking invalid option error msg: ", err)
            status = True
        self.assertTrue(status)


        print("checking invalid output by systemctl")
        mock_send_shell_cmd.return_value = """
            (No info could be read for "-p": geteuid()=1000 but you should be root.)
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
            tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -
            tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
            tcp        0      0 192.168.122.1:53        0.0.0.0:*               LISTEN      -
            tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
            tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      -
            tcp6       0      0 :::22                   :::*                    LISTEN      -
            tcp6       0      0 :::23                   :::*                    LISTEN      -
            tcp6       0      0 ::1:25                  :::*                    LISTEN      -
            tcp6       0      0 :::443                  :::*                    LISTEN      -
            tcp6       0      0 :::8000                 :::*                    LISTEN      -
            udp        0      0 192.168.122.1:53        0.0.0.0:*                           -
            udp        0      0 0.0.0.0:67              0.0.0.0:*                           -
            udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
            udp        0      0 0.0.0.0:123             0.0.0.0:*                           -
            udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
            udp        0      0 127.0.0.1:323           0.0.0.0:*                           -
            udp        0      0 0.0.0.0:36421           0.0.0.0:*                           -
            udp        0      0 0.0.0.0:28284           0.0.0.0:*                           -
            udp6       0      0 :::123                  :::*                                -
            udp6       0      0 :::36109                :::*                                -
            udp6       0      0 ::1:323                 :::*                                -
        """
        status = self.ins.stop_telnet_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertFalse(status)

        print("checking right output by systemctl")
        mock_send_shell_cmd.return_value = """
            (No info could be read for "-p": geteuid()=1000 but you should be root.)
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
            tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -
            tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
            tcp        0      0 192.168.122.1:53        0.0.0.0:*               LISTEN      -
            tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
            tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      -
            tcp6       0      0 :::22                   :::*                    LISTEN      -
            tcp6       0      0 ::1:25                  :::*                    LISTEN      -
            tcp6       0      0 :::443                  :::*                    LISTEN      -
            tcp6       0      0 :::8000                 :::*                    LISTEN      -
            udp        0      0 192.168.122.1:53        0.0.0.0:*                           -
            udp        0      0 0.0.0.0:67              0.0.0.0:*                           -
            udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
            udp        0      0 0.0.0.0:123             0.0.0.0:*                           -
            udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
            udp        0      0 127.0.0.1:323           0.0.0.0:*                           -
            udp        0      0 0.0.0.0:36421           0.0.0.0:*                           -
            udp        0      0 0.0.0.0:28284           0.0.0.0:*                           -
            udp6       0      0 :::123                  :::*                                -
            udp6       0      0 :::36109                :::*                                -
            udp6       0      0 ::1:323                 :::*                                -
        """
        status = self.ins.stop_telnet_service(device=mock_device_ins, service_control_tool="systemctl")
        self.assertTrue(status)


        print("checking right output by service")
        mock_send_shell_cmd.return_value = """
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address               Foreign Address             State       PID/Program name
            tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN      1283/rsyslogd
            tcp        0      0 0.0.0.0:111                 0.0.0.0:*                   LISTEN      1351/rpcbind
            tcp        0      0 0.0.0.0:35765               0.0.0.0:*                   LISTEN      1369/rpc.statd
            tcp        0      0 0.0.0.0:22                  0.0.0.0:*                   LISTEN      1612/sshd
            tcp        0      0 127.0.0.1:25                0.0.0.0:*                   LISTEN      1707/master
            tcp        0      0 :::514                      :::*                        LISTEN      1283/rsyslogd
            tcp        0      0 :::111                      :::*                        LISTEN      1351/rpcbind
            tcp        0      0 :::21                       :::*                        LISTEN      11293/vsftpd
            tcp        0      0 :::22                       :::*                        LISTEN      1612/sshd
            tcp        0      0 :::38743                    :::*                        LISTEN      1369/rpc.statd
            tcp        0      0 ::1:25                      :::*                        LISTEN      1707/master
            udp        0      0 0.0.0.0:514                 0.0.0.0:*                               1283/rsyslogd
            udp        0      0 0.0.0.0:678                 0.0.0.0:*                               1351/rpcbind
            udp        0      0 0.0.0.0:697                 0.0.0.0:*                               1369/rpc.statd
            udp        0      0 0.0.0.0:46027               0.0.0.0:*                               1369/rpc.statd
            udp        0      0 0.0.0.0:111                 0.0.0.0:*                               1351/rpcbind
            udp        0      0 :::514                      :::*                                    1283/rsyslogd
            udp        0      0 :::678                      :::*                                    1351/rpcbind
            udp        0      0 :::38753                    :::*                                    1369/rpc.statd
            udp        0      0 :::111                      :::*                                    1351/rpcbind
        """
        status = self.ins.stop_telnet_service(device=mock_device_ins, service_control_tool="service")
        self.assertTrue(status)

        print("checking invalid output by service")
        mock_send_shell_cmd.return_value = """
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address               Foreign Address             State       PID/Program name
            tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN      1283/rsyslogd
            tcp        0      0 0.0.0.0:111                 0.0.0.0:*                   LISTEN      1351/rpcbind
            tcp        0      0 0.0.0.0:35765               0.0.0.0:*                   LISTEN      1369/rpc.statd
            tcp        0      0 0.0.0.0:22                  0.0.0.0:*                   LISTEN      1612/sshd
            tcp        0      0 127.0.0.1:25                0.0.0.0:*                   LISTEN      1707/master
            tcp        0      0 :::514                      :::*                        LISTEN      1283/rsyslogd
            tcp        0      0 :::111                      :::*                        LISTEN      1351/rpcbind
            tcp        0      0 :::21                       :::*                        LISTEN      11293/vsftpd
            tcp        0      0 :::22                       :::*                        LISTEN      1612/sshd
            tcp        0      0 :::23                       :::*                        LISTEN      -
            tcp        0      0 :::38743                    :::*                        LISTEN      1369/rpc.statd
            tcp        0      0 ::1:25                      :::*                        LISTEN      1707/master
            udp        0      0 0.0.0.0:514                 0.0.0.0:*                               1283/rsyslogd
            udp        0      0 0.0.0.0:678                 0.0.0.0:*                               1351/rpcbind
            udp        0      0 0.0.0.0:697                 0.0.0.0:*                               1369/rpc.statd
            udp        0      0 0.0.0.0:46027               0.0.0.0:*                               1369/rpc.statd
            udp        0      0 0.0.0.0:111                 0.0.0.0:*                               1351/rpcbind
            udp        0      0 :::514                      :::*                                    1283/rsyslogd
            udp        0      0 :::678                      :::*                                    1351/rpcbind
            udp        0      0 :::38753                    :::*                                    1369/rpc.statd
            udp        0      0 :::111                      :::*                                    1351/rpcbind
        """
        status = self.ins.stop_telnet_service(device=mock_device_ins, service_control_tool="service")
        self.assertFalse(status)

    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_start_named_service(self, mock_send_shell_cmd):
        """test start named service"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        msg = "Start named service with CMD named"
        reponse1= "root     25386     1  0 11:30 ?        00:00:00 named"
        mock_send_shell_cmd.return_value = reponse1
        result = self.ins.start_named_service(device=mock_device_ins)
        self.assertTrue(result)

        msg = "Start named service with CMD named"
        reponse2= "none"
        mock_send_shell_cmd.return_value = reponse2
        result = self.ins.start_named_service(
            device=mock_device_ins,
            timeout=120,
            named_service_folder="/var/named",
            named_conf_folder="/etc/",
            named_chroot_service_folder="/var/named/chroot/var/named/",
            named_chroot_conf_folder="/var/named/chroot/etc/",
            named_conf_file_name="named.conf",
            named_conf_zone_file_name_v4="testv4.zone",
            named_conf_zone_file_name_v6="testv6.zone",
            pre_location_cmd_named="/usr/local/sbin/",
            pre_location_cmd_service="/sbin/",
        )
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse1,
        reponse1,
        )
        result = self.ins.start_named_service(device=mock_device_ins)
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        reponse2,
        )
        result = self.ins.start_named_service(device=mock_device_ins)
        self.assertFalse(result)


    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_stop_named_service(self, mock_send_shell_cmd):
        """test start named service"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        msg = "Stop named service with multi named stated"
        reponse1= "root     25386     1  0 11:30 ?        00:00:00 named"
        mock_send_shell_cmd.return_value = reponse1
        result = self.ins.stop_named_service(device=mock_device_ins)
        self.assertFalse(result)

        msg = "Stop named service"
        reponse2= "333\n333"
        mock_send_shell_cmd.return_value = reponse2
        result = self.ins.stop_named_service(
            device=mock_device_ins,
            timeout=120,
        )
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse2,
        reponse1,
        )
        result = self.ins.stop_named_service(device=mock_device_ins)
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse1,
        reponse2,
        reponse2,
        )
        result = self.ins.stop_named_service(device=mock_device_ins)
        self.assertTrue(result)

    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_config_rsyslog_cfg(self, mock_send_shell_cmd, mock_sleep):
        """test config and start rsyslog service"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        msg = "Start rsyslog service with tcpudp"
        reponse1= """
        tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN
        tcp        0      0 :::514                      :::*                        LISTEN
        udp        0      0 0.0.0.0:514                 0.0.0.0:*
        udp        0      0 :::514                      :::*
        """
        msg = "Start rsyslog service with tcpudp"
        reponse_tcp= """
        tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN
        tcp        0      0 :::514                      :::*                        LISTEN
        """
        reponse_udp= """
        udp        0      0 0.0.0.0:514                 0.0.0.0:*
        udp        0      0 :::514                      :::*
        """

        reponse_rsyslog= """
        rsyslog-3.21.3-4.fc10.i386
        """

        reponse_tls= """
        rsyslog-gnutls-4.6.2-12.el6.i686
        rsyslog-4.6.2-12.el6.i686
        """
        reponse3= "none"

        mock_send_shell_cmd.return_value = reponse1
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, operation="restart", restart="True", config_file="no")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse_tcp
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp", operation="restart", restart="True", config_file="no")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse_tcp
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp_ipv4", operation="restart", restart="True", config_file="no")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse_udp
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp", operation="restart", restart="True", config_file="no")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse_udp
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp_ipv4", operation="restart", restart="True", config_file="no")
        self.assertTrue(result)

        msg = "Start rsyslog service with CMD tls"
        reponse2= """
        tcp        0      0 0.0.0.0:6514                 0.0.0.0:*                   LISTEN
        tcp        0      0 :::6514                      :::*                        LISTEN
        """
        mock_send_shell_cmd.return_value = reponse_tls
        result = self.ins.config_rsyslog_cfg(
            device=mock_device_ins,
            timeout=120,
            cfg_name="aaa",
            cfg_tls_name="bbb",
            cfg_name_bak="ccc",
            cfg_tls_name_bak="ddd",
            syslog_port=6514,
            pro_option="tls",
            operation="start",
            config_file="no",
        )
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse_tls,
        reponse_tls,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse2,
        )
        result = self.ins.config_rsyslog_cfg(
            device=mock_device_ins,
            timeout=120,
            cfg_name="aaa",
            cfg_tls_name="bbb",
            cfg_name_bak="ccc",
            cfg_tls_name_bak="ddd",
            syslog_port=6514,
            pro_option="tls",
            operation="restart",
            restart="True"
        )
        self.assertTrue(result)





        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse1,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_tcp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_tcp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp_ipv4", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_udp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_udp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp_ipv4", operation="restart", restart="True")
        self.assertTrue(result)



        self.assertTrue(result)
        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, operation="restart",restart="True")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse_tls,
        reponse_tls,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse2,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, operation="restart", restart="True",syslog_port=6514,pro_option="tls")
        self.assertTrue(result)

        self.assertTrue(result)
        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp_ipv4", operation="restart",restart="True")
        self.assertFalse(result)


        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp", operation="restart",restart="True")
        self.assertFalse(result)


        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp", operation="restart",restart="True")
        self.assertFalse(result)


        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp_ipv4", operation="restart",restart="True")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, operation="restart", restart="True",syslog_port=6514,pro_option="tls")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse1,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_tcp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_tcp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp_ipv4", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_udp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_udp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp_ipv4", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, operation="restart", restart="True")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp_ipv4", operation="restart", restart="True")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp", operation="restart", restart="True")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp_ipv4", operation="restart", restart="True")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp", operation="restart", restart="True")
        self.assertFalse(result)

        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcpudp", operation="restart", restart="True")
        self.assertFalse(result)
        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tc", operation="restart", restart="True")
        self.assertFalse(result)
        mock_send_shell_cmd.side_effect = (
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tc", operation="restart", restart="True")
        self.assertFalse(result)
        mock_send_shell_cmd.side_effect = (
        reponse_rsyslog,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse1,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcpudp", operation="restart", restart="True")
        self.assertTrue(result)
        mock_send_shell_cmd.side_effect = (
        reponse_rsyslog,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_tcp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp", operation="restart", restart="True")
        self.assertTrue(result)
        mock_send_shell_cmd.side_effect = (
        reponse_rsyslog,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_tcp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tcp_ipv4", operation="restart", restart="True")
        self.assertTrue(result)
        mock_send_shell_cmd.side_effect = (
        reponse_rsyslog,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_udp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp", operation="restart", restart="True")
        self.assertTrue(result)

        mock_send_shell_cmd.side_effect = (
        reponse_rsyslog,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse_udp,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="udp_ipv4", operation="restart", restart="True")
        self.assertTrue(result)
        mock_send_shell_cmd.side_effect = (
        reponse_tls,
        reponse_tls,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse3,
        reponse2,
        )
        result = self.ins.config_rsyslog_cfg(device=mock_device_ins, pro_option="tls", syslog_port=6514, operation="restart", restart="True")
        self.assertTrue(result)


    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_rollback_rsyslog_cfg(self, mock_send_shell_cmd):
        """test config and start rsyslog service"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        msg = "Start rsyslog service with tcpudp"
        reponse1= "none"
        reponse_rsyslog= """
        rsyslog-3.21.3-4.fc10.i386
        """
        mock_send_shell_cmd.return_value = reponse1
        result = self.ins.rollback_rsyslog_cfg(device=mock_device_ins, delete_file="yes")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse1
        result = self.ins.rollback_rsyslog_cfg(device=mock_device_ins, rollback_file="yes")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse1
        result = self.ins.rollback_rsyslog_cfg(device=mock_device_ins,
            timeout=120,
            cfg_name="aaa",
            cfg_tls_name="bbb",
            cfg_name_bak="ccc",
            cfg_tls_name_bak="ddd",
            rollback_file="yes")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse_rsyslog
        result = self.ins.rollback_rsyslog_cfg(device=mock_device_ins, delete_file="yes")
        self.assertTrue(result)
        mock_send_shell_cmd.return_value = reponse_rsyslog
        result = self.ins.rollback_rsyslog_cfg(device=mock_device_ins, rollback_file="yes")
        self.assertTrue(result)

    @mock.patch.object(linux_tool, "get_service_management_tool")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_start_nfs_service(self, mock_send_shell_cmd, mock_get_service_management_tool):
        """UT CASE"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_get_service_management_tool.return_value = "service"

        print("Normal testing")
        mock_send_shell_cmd.side_effect = [
            """
total 0
drwxr-xr-x 2 regress regress 40 Apr 26 07:20 nfs
            """,
            """
Export list for 127.0.0.1:
/dev/shm/nfs *
/tmp         *
            """
        ]
        status = self.ins.start_nfs_service(device=mock_device_ins, service_control_tool="service")
        self.assertTrue(status)

        print("Specific mount folder")
        mock_send_shell_cmd.side_effect = [
            """
total 32
lrwxrwxrwx.   1 root root    7 Jan 28 20:52 bin -> usr/bin
dr-xr-xr-x.   5 root root 4096 Apr 26 03:19 boot
drwxr-xr-x   19 root root 3000 Apr 26 05:05 dev
drwxr-xr-x.  90 root root 8192 Apr 26 04:57 etc
drwxr-xr-x    4 root root 4096 Apr 25 08:01 home
lrwxrwxrwx.   1 root root    7 Jan 28 20:52 lib -> usr/lib
lrwxrwxrwx.   1 root root    9 Jan 28 20:52 lib64 -> usr/lib64
drwxr-xr-x.   2 root root    6 Apr 11  2018 media
drwxr-xr-x.   2 root root    6 Apr 11  2018 mnt
drwxr-xr-x.   2 root root    6 Apr 11  2018 opt
dr-xr-xr-x  137 root root    0 Apr 26 05:05 proc
dr-xr-x---.  11 root root 4096 Mar  5 12:44 root
drwxr-xr-x   29 root root  820 Apr 26 08:23 run
lrwxrwxrwx.   1 root root    8 Jan 28 20:52 sbin -> usr/sbin
drwxr-xr-x.   2 root root    6 Apr 11  2018 srv
dr-xr-xr-x   13 root root    0 Apr 26 08:18 sys
drwxrwxrwx.  11 root root 4096 Apr 26 06:38 tmp
drwxr-xr-x.  15 root root  205 Mar  5 09:04 usr
drwxr-xr-x.  23 root root 4096 Mar  5 11:35 var
drwxr-xr-x.   5 root root   58 Mar 12 06:08 volume
            """,
            """
Export list for 127.0.0.1:
/tmp         *
/tmp         *
            """
        ]
        status = self.ins.start_nfs_service(device=mock_device_ins, add_firewall_rule=True, service_control_tool="systemctl", mount_folder="/tmp")
        self.assertTrue(status)

        print("Invalid option")
        self.assertRaisesRegex(
            ValueError,
            r"option 'service_control_tool' must be",
            self.ins.start_nfs_service,
            device=mock_device_ins, service_control_tool="whatever",
        )

        print("Mount folder not found on server")
        mock_send_shell_cmd.side_effect = [
            """
total 0
drwxr-xr-x 2 regress regress 40 Apr 26 07:20 aaa
            """,
            """
Export list for 127.0.0.1:
/tmp         *
            """
        ]
        self.assertRaisesRegex(
            RuntimeError,
            r"Create mount folder failed",
            self.ins.start_nfs_service,
            device=mock_device_ins,
        )

        print("Mount failed")
        mock_send_shell_cmd.side_effect = [
            """
total 0
drwxr-xr-x 2 regress regress 40 Apr 26 07:20 nfs
            """,
            """
Export list for 127.0.0.1:
/tmp         *
            """
        ]
        self.assertRaisesRegex(
            RuntimeError,
            r"Given mount path",
            self.ins.start_nfs_service,
            device=mock_device_ins,
        )

    @mock.patch.object(linux_tool, "get_service_management_tool")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_stop_nfs_service(self, mock_send_shell_cmd, mock_get_service_management_tool):
        """UT CASE"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_get_service_management_tool.return_value = "service"

        self.ins.stop_nfs_service(device=mock_device_ins, service_control_tool="systemctl", del_firewall_rule=True)
        self.ins.stop_nfs_service(device=mock_device_ins)

        print("Invalid option")
        self.assertRaisesRegex(
            ValueError,
            r"option 'service_control_tool' must be",
            self.ins.stop_nfs_service,
            device=mock_device_ins, service_control_tool="whatever",
        )


    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_start_tftp_service(self, mock_execute_shell_command_on_device):
        """test init object with different option"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.upload.return_value = True

        print("start tftp service with by normal configuration")
        mock_device_ins.upload.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            "", # find conf file
            "", # find conf backup file
            "", # find systemd file
            "", # find systemd backup file
            "", # create /tftpboot folder
            "", # restart xinted and tftp service
            """
            ● xinetd.service - Xinetd A Powerful Replacement For Inetd
            Loaded: loaded (/usr/lib/systemd/system/xinetd.service; disabled; vendor preset: enabled)
            Active: active (running) since Thu 2020-02-20 17:56:26 CST; 16h ago
            Process: 21055 ExecStart=/usr/sbin/xinetd -stayalive -pidfile /var/run/xinetd.pid $EXTRAOPTIONS (code=exited, status=0/SUCCESS)
            Main PID: 21058 (xinetd)
            CGroup: /system.slice/xinetd.service
                    └─21058 /usr/sbin/xinetd -stayalive -pidfile /var/run/xinetd.pid
            """, # xinted service status
            """
            Warning: tftp.service changed on disk. Run 'systemctl daemon-reload' to reload units.
            ● tftp.service - Tftp Server
            Loaded: loaded (/usr/lib/systemd/system/tftp.service; disabled; vendor preset: disabled)
            Active: active (running) since Fri 2020-02-21 10:46:46 CST; 7s ago
                Docs: man:in.tftpd
            Main PID: 5167 (in.tftpd)
            CGroup: /system.slice/tftp.service
                    └─5167 /usr/sbin/in.tftpd -c -s /tftpboot
            """, # tftpd service status
            """
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
            udp        0      0 0.0.0.0:69              0.0.0.0:*                           21058/xinetd
            udp6       0      0 :::69                   :::*                                1/systemd
            """, # netstat output
        )

        response = self.ins.start_tftp_service(device=mock_device_ins, return_conf=True)
        self.assertTrue(response["status"])
        self.assertTrue(re.search(r"service tftp", response["conf"]))
        self.assertTrue(re.search(r"user\s+=\s+root", response["conf"]))
        self.assertTrue(re.search(r"server_args\s+=\s+-c -s /tftpboot", response["conf"]))
        self.assertTrue(re.search(r"disable\s+=\s+no", response["conf"]))
        self.assertTrue(re.search(r"flags\s+= IPv4", response["conf"]))
        self.assertTrue(re.search(r"WantedBy=multi-user.target", response["systemd_conf"]))
        self.assertTrue(re.search(r"ExecStart=/usr/sbin/in.tftpd -c -s /tftpboot", response["systemd_conf"]))

        print("start tftp service but daemon package not installed")
        mock_device_ins.upload.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """No such file or directory""", # find conf file
            """""", # find conf backup file
            """""", # find systemd file
            """""", # find systemd backup file
            """""", # create /tftpboot folder
            """""", # restart xinted and tftp service
            """""", # xinted service status
            """""", # tftpd service status
            """""", # netstats output
        )
        self.assertRaisesRegex(
            RuntimeError,
            r"Needed configuration file not found",
            self.ins.start_tftp_service,
            device=mock_device_ins
        )

        print("start tftp service but service not active")
        mock_device_ins.upload.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """""", # find conf file
            """No such file or directory""", # find conf backup file
            """""", # create backup file
            """""", # find systemd file
            """""", # find systemd backup file
            """""", # create /tftpboot folder
            """""", # restart xinted and tftp service
            """""", # xinted service status
            """
            Warning: tftp.service changed on disk. Run 'systemctl daemon-reload' to reload units.
            ● tftp.service - Tftp Server
            Loaded: loaded (/usr/lib/systemd/system/tftp.service; disabled; vendor preset: disabled)
            Active: inactive (dead) since Thu 2020-02-20 18:11:26 CST; 16h ago
                Docs: man:in.tftpd
            Process: 21066 ExecStart=/usr/sbin/in.tftpd -c -s /tftpboot (code=exited, status=0/SUCCESS)
            Main PID: 21066 (code=exited, status=0/SUCCESS)
            """, # tftpd service status
            """""", # netstats output
        )

        response = self.ins.start_tftp_service(device=mock_device_ins)
        self.assertFalse(response)

        print("start tftp service but upload failed")
        mock_device_ins.upload.return_value = False
        mock_execute_shell_command_on_device.side_effect = (
            """""", # find conf file
            """""", # find conf backup file
            """""", # find systemd file
            """""", # find systemd backup file
            """""", # create /tftpboot folder
            """""", # restart xinted and tftp service
            """""", # xinted service status
            """""", # tftpd service status
            """""", # netstats output
        )
        self.assertRaisesRegex(
            RuntimeError,
            r"Failed to upload configure file to remote path",
            self.ins.start_tftp_service,
            device=mock_device_ins, upload_support=False
        )

        print("start tftp service without upload support")
        mock_device_ins.upload.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """""", # find conf file
            """""", # find conf backup file
            """""", # find systemd file
            """""", # find systemd backup file
            """""", # create /tftpboot folder
            """""", # restart xinted and tftp service
            """
            ● xinetd.service - Xinetd A Powerful Replacement For Inetd
            Loaded: loaded (/usr/lib/systemd/system/xinetd.service; disabled; vendor preset: enabled)
            Active: active (running) since Thu 2020-02-20 17:56:26 CST; 16h ago
            Process: 21055 ExecStart=/usr/sbin/xinetd -stayalive -pidfile /var/run/xinetd.pid $EXTRAOPTIONS (code=exited, status=0/SUCCESS)
            Main PID: 21058 (xinetd)
            CGroup: /system.slice/xinetd.service
                    └─21058 /usr/sbin/xinetd -stayalive -pidfile /var/run/xinetd.pid
            """, # xinted service status
            """
            Warning: tftp.service changed on disk. Run 'systemctl daemon-reload' to reload units.
            ● tftp.service - Tftp Server
            Loaded: loaded (/usr/lib/systemd/system/tftp.service; disabled; vendor preset: disabled)
            Active: active (running) since Fri 2020-02-21 10:46:46 CST; 7s ago
                Docs: man:in.tftpd
            Main PID: 5167 (in.tftpd)
            CGroup: /system.slice/tftp.service
                    └─5167 /usr/sbin/in.tftpd -c -s /tftpboot
            """, # tftpd service status
            """
            Active Internet connections (only servers)
            Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
            udp        0      0 0.0.0.0:69              0.0.0.0:*                           21058/xinetd
            udp6       0      0 :::69                   :::*                                1/systemd
            """, # netstat output
        )
        response = self.ins.start_tftp_service(device=mock_device_ins, upload_support=False, return_conf=True)
        self.assertTrue(response["status"])
        self.assertTrue(re.search(r"server_args\s+=\s+-s /tftpboot", response["conf"]))
        self.assertTrue(re.search(r"ExecStart=/usr/sbin/in.tftpd -s /tftpboot", response["systemd_conf"]))





if __name__ == '__main__':
    unittest.main()
