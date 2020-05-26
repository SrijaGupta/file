# pylint: disable=invalid-name,anomalous-backslash-in-string
# coding: UTF-8

"""Create or stop FTP, TELNET server on host

+ **start_ftp_service** - Edit FTP server's configuration file and then start the server
+ **stop_ftp_service**  - Stop FTP server
+ **start_telnet_service** - Edit TELNET server's configuration file and then start the server
+ **stop_telnet_service**  - Stop TELNET server
+ **start_named_service** - Edit named server's configuration file and then start the server
+ **stop_named_service**  - Stop named server
+ **start_nfs_service** - Edit NFS server's configuration and then start the server
+ **stop_nfs_service** - Stop NFS server
+ **start_tftp_service** - Edit TFTP server's configuration and then start the server
+ **stop_tftp_service** - Stop TFTP server
"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import os
import re
import time

from jnpr.toby.frameworkDefaults import credentials
from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.linux.linux_tool import linux_tool


class setup_server():
    """All server related functions"""
    def __init__(self):
        """"INIT"""
        self.tool = flow_common_tool()
        self.host = linux_tool()

        self.default = {
            "regress_username":             credentials.Unix["USERNAME"],
            "regress_password":             credentials.Unix["PASSWORD"],
            "root_username":                credentials.Unix["SU"],
            "root_password":                credentials.Unix["SUPASSWORD"],
        }

        self.path = {}
        # whatever systemctl implement, FTP conf path are same
        self.path["ftp_root_folder"] = "/etc/vsftpd"
        self.path["ftp_conf_file_name"] = "vsftpd.conf"
        self.path["ftp_conf_file_path"] = os.path.join(self.path['ftp_root_folder'], self.path["ftp_conf_file_name"])

        self.ftp_service_issue_pattern_list = (
            r"Access denied",
            r"Permission denied",
            r"command not found",
            r"cannot read",
        )

        # before CentOS7, telnet server controled by xinetd.d
        self.path["telnet_xinetd_root_folder"] = "/etc/xinetd.d"
        self.path["telnet_xinetd_file_name"] = "telnet"
        self.path["telnet_xinetd_file_path"] = os.path.join(self.path["telnet_xinetd_root_folder"], self.path["telnet_xinetd_file_name"])

        # from CentOS7, telnet server have individual service controled by systemctl
        self.path["telnet_systemctl_root_folder"] = "/usr/lib/systemd/system"
        self.path["telnet_systemctl_file_name"] = "telnet.socket"
        self.path["telnet_systemctl_file_path"] = os.path.join(self.path["telnet_systemctl_root_folder"], self.path["telnet_systemctl_file_name"])

        # for CentOS7, tftp server controled by xinetd.d
        self.path["tftp_xinetd_file_name"] = "tftp"
        self.path["tftp_systemd_file_name"] = "tftp.service"
        self.path["tftp_xinetd_file_path"] = os.path.join(self.path["telnet_xinetd_root_folder"], self.path["tftp_xinetd_file_name"])
        self.path["tftp_systemd_file_path"] = os.path.join(self.path["telnet_systemctl_root_folder"], self.path["tftp_systemd_file_name"])


    def start_ftp_service(self, device, **kwargs):
        """Edit FTP server's configuration file and then start the server

        :param INT max_rate:
            *OPTIONAL* Set download speed rate as byte, For example: 8192 means 1KB/s (1024 * 8). Default: None

        :param INT listen_port:
            *OPTIONAL* As default, FTP server listened on port 21 both for IPv4/6 and work in Daemon mode. If you set this option to other port
                       number, it means *NOT* support IPv6, and server worked by standalone mode.

        :param BOOL ipv6_support:
            *OPTIONAL* As default, FTP only support IPv4, but you can set True to support IPv6. Default: False

        :param BOOL passive_mode:
            *OPTIONAL* Support passive mode. Default: True

        :param STR banner:
            *OPTIONAL* FTP server banner

        :param STR service_control_tool:
            *OPTIONAL* Modern OS use "systemctl" to manage each service so far, but older OS such as 'CentOS 6', 'Ubuntu 14' use "service". This
                       option should be "systemctl" or "service" or get automatically. Default: "service"

        :param STR connect_from_port_20:
            *OPTIONAL* set connect_from_port_20. default: YES

        :param STR|LIST more_configuration:
            *OPTIONAL* A vsftpd configuration string or list need add to configure file. default: None

        :param INT timeout:
            *OPTIONAL* Server start timeout. Default: 300

        :param BOOL return_conf:
            *OPTIONAL* For unit test. Set True to return vsftpd's configuration

        :return:
            Return True if FTP service start success. Or False if start failed.
            If given option is wrong, raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["max_rate"] = kwargs.pop("max_rate", None)
        options["listen_port"] = kwargs.pop("listen_port", None)
        options["passive_mode"] = self.tool.check_boolean(kwargs.pop("passive_mode", True))
        options["banner"] = kwargs.pop("banner", None)
        options["ipv6_support"] = self.tool.check_boolean(kwargs.pop("ipv6_support", False))
        options["service_control_tool"] = kwargs.pop("service_control_tool", self.host.get_service_management_tool(device=device)).strip().lower()
        options["connect_from_port_20"] = kwargs.pop("connect_from_port_20", "YES").strip().upper()
        options["more_configuration"] = kwargs.pop("more_configuration", None)
        options["timeout"] = kwargs.pop("timeout", 300)
        options["return_conf"] = self.tool.check_boolean(kwargs.pop("return_conf", None))

        # default is 'service' for compatibility
        options["service_control_tool"] = "service" if options["service_control_tool"] == "unknown" else options["service_control_tool"]

        # user option checkout
        if options["service_control_tool"] not in ("service", "systemctl"):
            raise ValueError("option 'service_control_tool' must be 'service' or 'systemctl' but got '{}'".format(options["service_control_tool"]))

        # create backup file
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="/bin/ls -l {}.bak".format(self.path["ftp_conf_file_path"])
        )
        if re.search(r'No such file or directory', result, re.I):
            dev.execute_shell_command_on_device(
                device=device,
                timeout=options["timeout"],
                command="/bin/cp {0} {0}.bak".format(self.path["ftp_conf_file_path"]),
            )

        conf_lines = []
        conf_lines.append("anonymous_enable=YES")
        conf_lines.append("anon_mkdir_write_enable=YES")
        conf_lines.append("anon_upload_enable=YES")
        conf_lines.append("anon_other_write_enable=YES")
        conf_lines.append("local_enable=YES")
        conf_lines.append("write_enable=YES")
        conf_lines.append("local_umask=022")
        conf_lines.append("dirmessage_enable=YES")
        conf_lines.append("xferlog_enable=YES")
        conf_lines.append("xferlog_std_format=YES")
        conf_lines.append("pam_service_name=vsftpd")
        # conf_lines.append("userlist_enable=YES")
        conf_lines.append("tcp_wrappers=YES")
        conf_lines.append("connect_from_port_20={}".format(options["connect_from_port_20"]))

        if options["listen_port"] is not None:
            conf_lines.append("listen_port={}".format(options["listen_port"]))


        if options["ipv6_support"] is True:
            conf_lines.append("listen=NO")
            conf_lines.append("listen_ipv6=YES")
        else:
            conf_lines.append("listen=YES")

        if options["passive_mode"] is True:
            conf_lines.append("pasv_enable=YES")
            conf_lines.append("pasv_promiscuous=YES")
        else:
            conf_lines.append("pasv_enable=NO")

        if options["banner"] is not None:
            conf_lines.append('ftpd_banner="{}"'.format(options["banner"]))

        if options["max_rate"] is not None:
            conf_lines.append("local_max_rate={}".format(options["max_rate"]))
            conf_lines.append("anon_max_rate={}".format(options["max_rate"]))

        if options["more_configuration"] is not None:
            if isinstance(options["more_configuration"], str):
                conf_lines.append(options["more_configuration"])
            elif isinstance(options["more_configuration"], (list, tuple)):
                conf_lines.extend(options["more_configuration"])
            else:
                device.log(
                    message="Option 'more_configuration' must be STR or LIST but got '{}'".format(type(options["more_configuration"])),
                    level="ERROR",
                )

        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="echo '{}' > {}".format("\n".join(conf_lines), self.path["ftp_conf_file_path"])
        )

        # restart FTP server
        ftp_service_restart_result = True
        if options["service_control_tool"] == "systemctl":
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="systemctl restart vsftpd | cat")
            for pattern in self.ftp_service_issue_pattern_list:
                if re.search(pattern, result, re.I):
                    device.log(message="Error keyword found: {}".format(pattern), level="ERROR")
                    return False

            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="systemctl status vsftpd | cat")
            if re.search(r"active\s+\(running\)", result, re.I):
                ftp_service_restart_result = True
            else:
                ftp_service_restart_result = False
        else:
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="service vsftpd restart | cat")
            for pattern in self.ftp_service_issue_pattern_list:
                if re.search(pattern, result, re.I):
                    device.log(message="Error keyword found: {}".format(pattern), level="ERROR")
                    return False

            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="service vsftpd status | cat")
            if re.search(r"is running", result, re.I):
                ftp_service_restart_result = True
            else:
                ftp_service_restart_result = False

        if ftp_service_restart_result is True:
            device.log(message="Start FTP server success", level="INFO")
        else:
            device.log(message="Start FTP server failed", level="ERROR")

        if options["return_conf"] is True:
            return_value = {
                "conf":     "\n".join(conf_lines),
                "status":   ftp_service_restart_result,
            }
        else:
            return_value = ftp_service_restart_result

        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def stop_ftp_service(self, device, **kwargs):
        """Stop FTP service

        :param INT timeout:
            *OPTIONAL* Stop timeout

        :param STR service_control_tool:
            *OPTIONAL* This option should be "systemctl", "service" or find automatically. Default: "service".
                       More detail please see 'start_ftp_service'

        :return:
            Return True if FTP service start success. Or False if start failed. If given option is wrong, raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["service_control_tool"] = kwargs.pop("service_control_tool", self.host.get_service_management_tool(device=device)).strip().lower()
        options["timeout"] = kwargs.pop("timeout", 180)

        # default is 'service' for compatibility
        options["service_control_tool"] = "service" if options["service_control_tool"] == "unknown" else options["service_control_tool"]

        # user option checkout
        if options["service_control_tool"] not in ("service", "systemctl"):
            raise ValueError("option 'service_control_tool' must be 'service' or 'systemctl' but got '{}'".format(options["service_control_tool"]))

        ftp_service_stop_result = False
        if options["service_control_tool"] == "systemctl":
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="systemctl stop vsftpd | cat")
            for pattern in self.ftp_service_issue_pattern_list:
                if re.search(pattern, result, re.I):
                    device.log(message="Error keyword found: {}".format(pattern), level="ERROR")
                    return False

            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="systemctl status vsftpd | cat")
            if re.search(r"inactive\s+\(dead\)", result, re.I):
                ftp_service_stop_result = True
        else:
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="service vsftpd stop | cat")
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="service vsftpd status | cat")
            if re.search(r"is stopped", result, re.I):
                ftp_service_stop_result = True

        if ftp_service_stop_result is True:
            device.log(message="Stop FTP server success", level="INFO")
        else:
            device.log(message="Stop FTP server failed", level="WARN")

        device.log(message="{} return value: {}".format(func_name, ftp_service_stop_result), level="INFO")
        return ftp_service_stop_result

    def start_telnet_service(self, device, **kwargs):
        """Edit telnet configuration file and start services

        TELNET service support IPv4/v6 both.

        :param INT port:
            *OPTIONAL* Customize telnet port number

        :param STR service_control_tool:
            *OPTIONAL* Modern OS use "systemctl" to manage each service so far, but older OS such as 'CentOS 6', 'Ubuntu 14' use "service". This
                       option should be "systemctl" or "service". Default: "service"

        :param INT timeout:
            *OPTIONAL* Server start timeout. Default: 300

        :param BOOL return_conf:
            *OPTIONAL* For unit test. Set True to return configuration

        :return:
            Return True if TELNET service start success. Or False if start failed.
            For invalid option will raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options['port'] = kwargs.pop("port", 23)
        options["service_control_tool"] = kwargs.pop("service_control_tool", self.host.get_service_management_tool(device=device)).strip().lower()
        options["timeout"] = kwargs.pop("timeout", 300)
        options["return_conf"] = self.tool.check_boolean(kwargs.pop("return_conf", None))

        # default is 'service' for compatibility
        options["service_control_tool"] = "service" if options["service_control_tool"] == "unknown" else options["service_control_tool"]

        # user option checkout
        if options["service_control_tool"] not in ("service", "systemctl"):
            raise ValueError("option 'service_control_tool' must be 'service' or 'systemctl' but got '{}'".format(options["service_control_tool"]))

        start_telnet_service_status = True

        # telnet server controled by systemctl
        conf_lines = []
        if options["service_control_tool"] == "systemctl":
            cmd = "/bin/ls -l {}".format(self.path["telnet_systemctl_file_path"])
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)
            if re.search('No such file', result, re.I):
                device.log(message="No telnet config file found in '{}'".format(self.path["telnet_systemctl_file_path"]), level="ERROR")
                return False

            # should backup conf file
            cmd = "/bin/ls -l {}.bak".format(self.path["telnet_systemctl_file_path"])
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)
            if re.search('No such file', result, re.I):   # pragma: no cover
                cmd = "/bin/cp {} {}.bak".format(self.path["telnet_systemctl_file_path"], self.path["telnet_systemctl_file_path"])
                dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)

            conf_lines = []
            conf_lines.append("[Unit]")
            conf_lines.append("Description=Telnet Server Activation Socket")
            conf_lines.append("Documentation=man:telnetd(8)")
            conf_lines.append("")
            conf_lines.append("[Socket]")
            conf_lines.append("ListenStream={}".format(options['port']))
            conf_lines.append("Accept=true")
            conf_lines.append("")
            conf_lines.append("[Install]")
            conf_lines.append("WantedBy=sockets.target")

            cmds = (
                "/bin/echo '{}' > {}".format("\n".join(conf_lines), self.path["telnet_systemctl_file_path"]),
                "systemctl daemon-reload",
                "systemctl restart telnet.socket",
                "systemctl restart xinetd",
                "/bin/netstat -tnulp | /bin/grep 23 | cat",
            )
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmds)
            start_telnet_service_status = bool(re.search(r"tcp\d*\s+\d+\s+\d+\s+:::23\s+.*LISTEN", result, re.I))

        # telnet server controled by xinetd.d
        if options["service_control_tool"] == "service":
            cmd = "/bin/ls -l {}".format(self.path["telnet_xinetd_file_path"])
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)
            if re.search('No such file', result, re.I):     # pragma: no cover
                device.log(message="No telnet config file found in '{}'".format(self.path["telnet_xinetd_file_path"]), level="ERROR")
                return False

            # should backup conf file
            cmd = "/bin/ls -l {}.bak".format(self.path["telnet_xinetd_file_path"])
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)
            if re.search('No such file', result, re.I):     # pragma: no cover
                cmd = "/bin/cp {} {}.bak".format(self.path["telnet_xinetd_file_path"], self.path["telnet_xinetd_file_path"])
                dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)

            conf_lines = []
            conf_lines.append("service telnet")
            conf_lines.append("{")
            conf_lines.append("        flags           = IPv6")
            conf_lines.append("        socket_type     = stream")
            conf_lines.append("        wait            = no")
            conf_lines.append("        user            = root")
            conf_lines.append("        server          = /usr/sbin/in.telnetd")
            conf_lines.append("        log_on_failure  += USERID")
            conf_lines.append("        disable         = no")
            conf_lines.append("}")

            # So far daemon port number cannot customized
            cmds = (
                "/bin/echo '{}' > {}".format("\n".join(conf_lines), self.path["telnet_xinetd_file_path"]),
                "service xinetd restart",
                "/bin/netstat -tnulp | /bin/grep 23 | cat",
            )
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmds)
            start_telnet_service_status = bool(re.search(r"tcp\s+\d+\s+\d+\s+:::23\s+.*LISTEN", result, re.I))

        if start_telnet_service_status is True:
            device.log(message="Start TELNET service success", level="INFO")
        else:
            device.log(message="Start TELNET service failed", level="ERROR")

        if options["return_conf"] is True:
            return_value = {"conf": "\n".join(conf_lines), "status": start_telnet_service_status}
        else:
            return_value = start_telnet_service_status

        device.log(message="{} return value:\n{}".format(self.tool.get_current_function_name(), return_value), level="INFO")
        return return_value

    def stop_telnet_service(self, device, **kwargs):
        """Stop TELNET service
        :param INT timeout:
            *OPTIONAL* timeout for each command

        :param STR service_control_tool:
            *OPTIONAL* Modern OS use "systemctl" to manage each service so far, but older OS such as 'CentOS 6', 'Ubuntu 14' use "service". This
                       option should be "systemctl" or "service". Default: "service"

        :return:
            True/False. If given option is wrong, raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["service_control_tool"] = kwargs.pop("service_control_tool", self.host.get_service_management_tool(device=device)).strip().lower()
        options["timeout"] = kwargs.pop("timeout", 180)

        # default is 'service' for compatibility
        options["service_control_tool"] = "service" if options["service_control_tool"] == "unknown" else options["service_control_tool"]

        # user option checkout
        if options["service_control_tool"] not in ("service", "systemctl"):
            raise ValueError("option 'service_control_tool' must be 'service' or 'systemctl' but got '{}'".format(options["service_control_tool"]))

        # stop service by systemctl
        if options["service_control_tool"] == "systemctl":
            cmds = (
                "systemctl stop telnet.socket",
                "/bin/netstat -tnulp | /bin/grep 23 | cat",
            )
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmds)
            if re.search(r"tcp\d*\s+\d+\s+\d+\s+:::23\s+.*LISTEN", result, re.I):
                stop_telnet_service_status = False
            else:
                stop_telnet_service_status = True

        # for service mode, need disable in conf file and restart xinetd
        if options["service_control_tool"] == "service":
            conf_lines = []
            conf_lines.append("service telnet")
            conf_lines.append("{")
            conf_lines.append("        flags           = IPv6")
            conf_lines.append("        socket_type     = stream")
            conf_lines.append("        wait            = no")
            conf_lines.append("        user            = root")
            conf_lines.append("        server          = /usr/sbin/in.telnetd")
            conf_lines.append("        log_on_failure  += USERID")
            conf_lines.append("        disable         = yes")
            conf_lines.append("}")

            cmds = (
                "/bin/echo '{}' > {}".format("\n".join(conf_lines), self.path["telnet_xinetd_file_path"]),
                "service xinetd restart",
                "/bin/netstat -tnulp | /bin/grep 23 | cat",
            )
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmds)
            if re.search(r"tcp\s+\d+\s+\d+\s+:::23\s+.*LISTEN", result, re.I):
                stop_telnet_service_status = False
            else:
                stop_telnet_service_status = True

        if stop_telnet_service_status is True:
            device.log(message="Stop TELNET service success", level="INFO")
        else:
            device.log(message="Stop TELNET service failed", level="WARN")

        device.log(message="{} return value: {}".format(func_name, stop_telnet_service_status), level="INFO")
        return stop_telnet_service_status

    def start_named_service(self, device, **kwargs):
        """Edit named configuration file and start services

        named service support IPv4/v6 both.

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param STR named_service_folder:
            *OPTIONAL* named service folder name, default is /var/named/

        :param STR named_conf_folder:
            *OPTIONAL* named service system folder name, default is /etc/

        :param STR named_chroot_service_folder:
            *OPTIONAL* named service chroot folder name, default is /var/named/chroot/var/named/

        :param STR named_chroot_conf_folder:
            *OPTIONAL* named service system chroot folder name, default is /var/named/chroot/etc/

        :param STR named_conf_file_name:
            *OPTIONAL* named service folder name, default is /var/named/

        :param STR named_conf_zone_file_name_v4:
            *OPTIONAL* named zone config IPv4 file name

        :param STR named_conf_zone_file_name_v6:
            *OPTIONAL* named zone config IPv6 file name

        :param STR pre_location_cmd_named:
            *OPTIONAL* named CMD prefix location, default is /usr/local/sbin/

        :param STR pre_location_cmd_service:
            *OPTIONAL* service named start CMD prefix location, default is /sbin/

        :param INT timeout:
            *OPTIONAL* Server start timeout. Default: 300

        :return:
            Return True if named service start success. Or False if start failed.
            For invalid option will raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        all_option_list = (
            "named_service_folder", "named_conf_folder", "named_chroot_service_folder", "named_chroot_conf_folder",
            "named_conf_file_name", "named_conf_zone_file_name_v4", "named_conf_zone_file_name_v6", "timeout",
            "pre_location_cmd_named", "pre_location_cmd_service",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        if options['timeout'] is None:
            options['timeout'] = kwargs.get('timeout', 300)
        if options['named_service_folder'] is None:
            options['named_service_folder'] = "/var/named/"
        if options['named_conf_folder'] is None:
            options['named_conf_folder'] = "/etc/"
        if options['named_chroot_service_folder'] is None:
            options['named_chroot_service_folder'] = "/var/named/chroot/var/named/"
        if options['named_chroot_conf_folder'] is None:
            options['named_chroot_conf_folder'] = "/var/named/chroot/etc/"
        if options['named_conf_file_name'] is None:
            options['named_conf_file_name'] = "named.conf"
        if options['named_conf_zone_file_name_v4'] is None:
            options['named_conf_zone_file_name_v4'] = "testv4.zone"
        if options['named_conf_zone_file_name_v6'] is None:
            options['named_conf_zone_file_name_v6'] = "testv6.zone"
        if options['pre_location_cmd_named'] is None:
            options['pre_location_cmd_named'] = "/usr/local/sbin/"
        if options['pre_location_cmd_service'] is None:
            options['pre_location_cmd_service'] = "/sbin/"
        # create backup file


        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_service_folder'], options['named_conf_file_name'])
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_conf_folder'], options['named_conf_file_name'])
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_chroot_service_folder'], options['named_conf_file_name'])
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_chroot_conf_folder'], options['named_conf_file_name'])
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_service_folder'], options['named_conf_zone_file_name_v4'])
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_service_folder'], options['named_conf_zone_file_name_v6'])
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_chroot_service_folder'], options['named_conf_zone_file_name_v4'])
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options['timeout'],
            command="/bin/rm -rf {}{}".format(options['named_chroot_service_folder'], options['named_conf_zone_file_name_v6'])
        )



        named_conf_content = """

        //
        // named.conf for Red Hat caching-nameserver
        //

        options {
        directory "/var/named";
        dump-file "/var/named/data/cache_dump.db";
            statistics-file "/var/named/data/named_stats.txt";
            listen-on-v6 {any;};
            forwarders {
                    10.208.0.50;
            };
        /*
         * If there is a firewall between you and nameservers you want
         * to talk to, you might need to uncomment the query-source
         * directive below.  Previous versions of BIND always asked
         * questions using port 53, but BIND 8.1 uses an unprivileged
         * port by default.
         */
         // query-source address * port 53;
        };

        /*
        * log option
        */
        logging {
                channel default_syslog { syslog local2; severity error; };
                channel audit_log { file "/var/log/named.log"; severity error; print-time yes; };
                category default { default_syslog; };
                category general { default_syslog; };
                category security { audit_log; default_syslog; };
                category config { default_syslog; };
                category resolver { audit_log; };
                category xfer-in { audit_log; };
                category xfer-out { audit_log; };
                category notify { audit_log; };
                category client { audit_log; };
                category network { audit_log; };
                category update { audit_log; };
                category queries { audit_log; };
                category lame-servers { audit_log; };
        };




        //
        // a caching only nameserver config
        //
        controls {
        //        inet 100.10.10.2 allow { localhost; } keys { rndckey; };
        //        inet 10.208.128.55 allow { localhost; } keys { rndckey; };
        //        inet 127.0.0.1 allow { localhost; } keys { rndckey; };
        };

        zone "." IN {
        type hint;
        file "named.ca";
        };

        zone "localdomain" IN {
        type master;
        file "localdomain.zone";
        allow-update { none; };
        };

        zone "localhost" IN {
        type master;
        file "localhost.zone";
        allow-update { none; };
        };

        zone "0.0.127.in-addr.arpa" IN {
        type master;
        file "named.local";
        allow-update { none; };
        };

        zone "0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
            type master;
        file "named.ip6.local";
        allow-update { none; };
        };

        zone "255.in-addr.arpa" IN {
        type master;
        file "named.broadcast";
        allow-update { none; };
        };

        zone "0.in-addr.arpa" IN {
        type master;
        file "named.zero";
        allow-update { none; };
        };


        //
        //      Defind zone by tonyli
        //
        zone testv4.net IN {
                type master;
                file "testv4.zone";
                allow-update { none; };
        };
        zone "testv6.net" IN {
                type master;
                file "testv6.zone";
                allow-update { none; };
        };
        //include "/etc/rndc.key";
        """

        testv4_zone_content = """
        $TTL    86400

        @               IN SOA  ns.testv4.net.   root.testv4.net. (
                        42              ; serial (d. adams)
                        3H              ; refresh
                        15M             ; retry
                        1W              ; expiry
                        1D )            ; minimum

        ; Internal
                        IN NS           ns.testv4.net.
                        IN A            100.10.10.2
                        IN A            10.208.128.55
                        IN AAAA         2000::2
                        IN MX           10 mail.testv4.net.

        ns              IN A            100.10.10.2
        mail            IN CNAME        ns.testv4.net.
        probe           IN CNAME        ns.testv4.net.
        probev6         IN AAAA         2000::2

        ; Public

        plat-vm37       IN A            200.20.20.2
        plat-vm36       IN A            200.20.20.3
        plat-vm37v6     IN AAAA         2001::2


        ns1             IN CNAME        ns.testv4.net.
        ns2             IN A            100.10.10.4
        ns3             IN A            100.10.10.5
        ns4             IN A            100.10.10.6
        ns5             IN A            100.10.10.7
        ns6             IN A            100.10.10.8
        ns7             IN A            100.10.10.9
        ns8             IN A            100.10.10.10

        a               IN A            1.1.1.10
        aaaa            IN AAAA         3001::1
        a-aaaa          IN A            1.1.1.131
        a-aaaa          IN AAAA         3001::2
        """

        testv6_zone_content = """
        $TTL    86400
        ;This file is added by tonyli
        @               IN SOA  ns.testv6.net.   root.testv6.net (
                        42              ; serial (d. adams)
                        3H              ; refresh
                        15M             ; retry
                        1W              ; expiry
                        1D )            ; minimum

                        IN NS           ns.testv6.net.
                        IN A            127.0.0.1
                        IN AAAA         ::1

        ns                        IN A          100.10.10.2
        ns                              IN AAAA         2000::2
        probe                         IN CNAME        ns.testv6.net.
        plat-vm36       IN AAAA         2001::2
        plat-vm37       IN AAAA         2001::3
        logv6           IN AAAA         2000::3
        a               IN A            1.1.1.10
        aaaa            IN AAAA         3001::1
        a-aaaa          IN A            1.1.1.131
        a-aaaa          IN AAAA         3001::2
        b               IN A            1.1.1.20
        """

        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="echo '{}' > {}{}".format(named_conf_content, options['named_service_folder'], options['named_conf_file_name'])
        )
        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="echo '{}' > {}{}".format(testv4_zone_content, options['named_service_folder'], options['named_conf_zone_file_name_v4'])
        )
        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="echo '{}' > {}{}".format(testv6_zone_content, options['named_service_folder'], options['named_conf_zone_file_name_v6'])
        )
        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="cp {}{} {}{}".format(
                options['named_service_folder'],
                options['named_conf_file_name'],
                options['named_conf_folder'],
                options['named_conf_file_name'],
            ),
        )
        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="cp {}{} {}{}".format(
                options['named_service_folder'],
                options['named_conf_file_name'],
                options['named_chroot_service_folder'],
                options['named_conf_file_name'],
            ),
        )
        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="cp {}{} {}{}".format(
                options['named_service_folder'],
                options['named_conf_zone_file_name_v4'],
                options['named_chroot_service_folder'],
                options['named_conf_zone_file_name_v4'],
            ),
        )
        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="cp {}{} {}{}".format(
                options['named_service_folder'],
                options['named_conf_zone_file_name_v6'],
                options['named_chroot_service_folder'],
                options['named_conf_zone_file_name_v6'],
            ),
        )

        # start named server
        named_service_start_result = True

        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="{}named".format(options['pre_location_cmd_named']),
        )
        result = dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="ps -ef | grep named | grep -v grep",
        )
        if re.search(r"named", result, re.I):
            named_service_start_result = True
            device.log(message="Success to start named service", level="INFO")
        else:
            result = dev.execute_shell_command_on_device(
                device=device,
                timeout=options["timeout"],
                command="{}service named restart".format(options['pre_location_cmd_service']),
            )
            result = dev.execute_shell_command_on_device(
                device=device,
                timeout=options["timeout"],
                command="ps -ef | grep named | grep -v grep",
            )
            if re.search(r"named", result, re.I):
                named_service_start_result = True
                device.log(message="Success to start named service", level="INFO")
            else:
                device.log(message="NOT found named", level="ERROR")
                device.log(message="Fail to start named service", level="ERROR")
                named_service_start_result = False

        device.log(message="{} return value: {}".format(func_name, named_service_start_result), level="INFO")
        return named_service_start_result

    def stop_named_service(self, device, **kwargs):
        """Stop named service

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param INT timeout:
            *OPTIONAL* Stop timeout

        :param STR service_control_tool:
            *OPTIONAL* This option should be "systemctl" or "service". Default: "service". More detail please see 'start_ftp_service'

        :return:
            Return True if FTP service start success. Or False if start failed. If given option is wrong, raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        all_option_list = (
            "timeout",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        if options['timeout'] is None:
            options['timeout'] = kwargs.get('timeout', 300)

        named_service_stop_result = False

        result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="ps -ef | grep named | grep -v grep")
        named_result = result.splitlines()
        for named_detail in named_result:
            if re.search(r"named", named_detail, re.I):
                named_pid = re.findall(r"^[A-Za-z]+\s*(\d+).*named", named_detail, re.I)
                device.log(str(named_pid), level="INFO")
                result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="kill -9 {}".format(named_pid[0]))
                device.log(message="Success to stop named service", level="INFO")
            else:
                device.log(message="No named service started", level="INFO")
        result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="ps -ef | grep named | grep -v grep")
        if re.search(r"named", result, re.I):
            device.log(message="Failed to stop named service", level="ERROR")
            named_service_stop_result = False
        else:
            named_service_stop_result = True
            device.log(message="Success to stop named service", level="INFO")

        device.log(message="{} return value: {}".format(func_name, named_service_stop_result), level="INFO")
        return named_service_stop_result

    def config_rsyslog_cfg(self, device, **kwargs):
        """Configure rsyslog cfg file
        Robot example:
        ${result}=    setup_server.config rsyslog cfg    device=${h1}    operation=restart    restart=True
        ${result}=    setup_server.config rsyslog cfg    device=${h1}    operation=stop

        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param STR cfg_name:
            *OPTIONAL* rsyslog cfg file name, default is rsyslog.conf

        :param STR cfg_tls_name:
            *OPTIONAL* rsyslog tls cfg file name, default is rsyslog.conf.tls

        :param STR cfg_name_bak:
            *OPTIONAL* rsyslog cfg backup file name, default is rsyslog.conf.bak

        :param STR cfg_tls_name_bak:
            *OPTIONAL* rsyslog cfg backup file name, default is rsyslog.conf.tls.bak

        :param int syslog_port:
            *OPTIONAL* syslog port, default is 514

        :param STR pro_option:
            *OPTIONAL* protocol option, default is tcpudp

        :param STR config_fie:
            *OPTIONAL* config rsyslog cfg option, default is yes

        :param STR operation:
            *OPTIONAL* operation of rsyslog service, one of start, stop or restart, default is None

        :param STR restart:
            *OPTIONAL* restart option, default is False

        :param INT timeout:
            *OPTIONAL* Server start timeout. Default: 300

        :return:
            Return True if rsyslog service start success. Or False if start failed.
            For invalid option will raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        all_option_list = (
            "cfg_name", "cfg_tls_name", "cfg_name_bak", "cfg_tls_name_bak", "restart",
            "syslog_port", "timeout", "pro_option", "operation", "config_file",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        if options['timeout'] is None:
            options['timeout'] = kwargs.get('timeout', 300)
        if options['cfg_name'] is None:
            options['cfg_name'] = "rsyslog.conf"
        if options['cfg_tls_name'] is None:
            options['cfg_tls_name'] = "rsyslog.conf.tls"
        if options['cfg_name_bak'] is None:
            options['cfg_name_bak'] = "rsyslog.conf.bak"
        if options['cfg_tls_name_bak'] is None:
            options['cfg_tls_name_bak'] = "rsyslog.conf.tls.bak"
        if options['syslog_port'] is None:
            options['syslog_port'] = kwargs.get('syslog_port', 514)
        if options['pro_option'] is None:
            options['pro_option'] = "tcpudp"
        if options['config_file'] is None:
            options['config_file'] = "yes"
        if options['restart'] is None:
            options['restart'] = "False"
        # create backup file

        rsyslog_conf_content = """
        #rsyslog v3 config file

        # if you experience problems, check
        # http://www.rsyslog.com/troubleshoot for assistance

        #### MODULES ####

        \$ModLoad imuxsock.so    # provides support for local system logging (e.g. via logger command)
        \$ModLoad imklog.so      # provides kernel logging support (previously done by rklogd)
        #$ModLoad immark.so     # provides --MARK-- message capability

        # Provides UDP syslog reception
        \$ModLoad imudp.so
        \$UDPServerRun {syslog_port}

        # Provides TCP syslog reception
        \$ModLoad imtcp.so
        \$InputTCPServerRun {syslog_port}


        #### GLOBAL DIRECTIVES ####

        # Use default timestamp format
        \$ActionFileDefaultTemplate RSYSLOG_SyslogProtocol23Format

        # File syncing capability is disabled by default. This feature is usually not required,
        # not useful and an extreme performance hit
        #\$ActionFileEnableSync on


        #### RULES ####

        # Log all kernel messages to the console.
        # Logging much else clutters up the screen.
        #kern.*                                                 /dev/console

        # Log anything (except mail) of level info or higher.
        # Don't log private authentication messages!
        *.info;mail.none;authpriv.none;cron.none;*.debug;*.*                /var/log/messages

        # The authpriv file has restricted access.
        authpriv.*                                              /var/log/secure

        # Log all the mail messages in one place.
        mail.*                                                  -/var/log/maillog


        # Log cron stuff
        cron.*                                                  /var/log/cron

        # Everybody gets emergency messages
        *.emerg                                                 *

        # Save news errors of level crit and higher in a special file.
        uucp,news.crit                                          /var/log/spooler

        # Save boot messages also to boot.log
        local7.*                                                /var/log/boot.log



        # ### begin forwarding rule ###
        # The statement between the begin ... end define a SINGLE forwarding
        # rule. They belong together, do NOT split them. If you create multiple
        # forwarding rules, duplicate the whole block!
        # Remote Logging (we use TCP for reliable delivery)
        #
        # An on-disk queue is created for this action. If the remote host is
        # down, messages are spooled to disk and sent when it is up again.
        #$WorkDirectory /var/spppl/rsyslog # where to place spool files
        #$ActionQueueFileName fwdRule1 # unique name prefix for spool files
        #$ActionQueueMaxDiskSpace 1g   # 1gb space limit (use as much as possible)
        #$ActionQueueSaveOnShutdown on # save messages to disk on shutdown
        #$ActionQueueType LinkedList   # run asynchronously
        #$ActionResumeRetryCount -1    # infinite retries if host is down
        # remote host is: name/ip:port, e.g. 192.168.0.1:{syslog_port}, port optional
        #*.* @@remote-host:{syslog_port}
        ### end of the forwarding rule ###
        """.format(syslog_port=options['syslog_port'])

        rsyslog_tls_conf_content = """

        #rsyslog v3 config file
        #
        # if you experience problems, check
        # http://www.rsyslog.com/troubleshoot for assistance

        #### MODULES ####

        #\$ModLoad imuxsock.so  # provides support for local system logging (e.g. via logger command)
        #\$ModLoad imklog.so    # provides kernel logging support (previously done by rklogd)
        #\$ModLoad immark.so    # provides --MARK-- message capability
        \$ModLoad imtcp.so

        # Make gtls driver the default
        \$DefaultNetstreamDriver gtls


        # Certificate files
        \$DefaultNetstreamDriverCAFile /root/ca.pem
        \$DefaultNetstreamDriverCertFile /root/cert.pem
        \$DefaultNetstreamDriverKeyFile /root/key.pem


        # Provides UDP syslog reception
        #\$ModLoad imudp.so
        #\$UDPServerRun 514

        # Provides TCP syslog reception
        #\$ModLoad imtcp.soi

        # Provides TCP syslog reception
        \$InputTCPServerStreamDriverMode 1 # run driver in TLS-only mode
        \$InputTCPServerStreamDriverAuthMode anon # client is NOT authenticated
        #\$InputTCPServerStreamDriverPermittedPeer *.herotest.net
        \$InputTCPServerRun {syslog_port}

        #### GLOBAL DIRECTIVES ####

        # Use default timestamp format
        \$ActionFileDefaultTemplate RSYSLOG_SyslogProtocol23Format

        # File syncing capability is disabled by default. This feature is usually not required,
        # not useful and an extreme performance hit
        #\$ActionFileEnableSync on


        #### RULES ####

        # Log all kernel messages to the console.
        # Logging much else clutters up the screen.
        #kern.*                                                 /dev/console

        # Log anything (except mail) of level info or higher.
        # Don't log private authentication messages!
        *.info;mail.none;authpriv.none;cron.none;*.debug;*.*                /var/log/messages

        # The authpriv file has restricted access.
        authpriv.*                                              /var/log/secure

        # Log all the mail messages in one place.
        mail.*                                                  -/var/log/maillog


        # Log cron stuff
        cron.*                                                  /var/log/cron

        # Everybody gets emergency messages
        *.emerg                                                 *

        # Save news errors of level crit and higher in a special file.
        uucp,news.crit                                          /var/log/spooler

        # Save boot messages also to boot.log
        local7.*                                                /var/log/boot.log



        # ### begin forwarding rule ###
        # The statement between the begin ... end define a SINGLE forwarding
        # rule. They belong together, do NOT split them. If you create multiple
        # forwarding rules, duplicate the whole block!
        # Remote Logging (we use TCP for reliable delivery)
        #
        # An on-disk queue is created for this action. If the remote host is
        # down, messages are spooled to disk and sent when it is up again.
        #$WorkDirectory /var/spppl/rsyslog # where to place spool files
        #$ActionQueueFileName fwdRule1 # unique name prefix for spool files
        #$ActionQueueMaxDiskSpace 1g   # 1gb space limit (use as much as possible)
        #$ActionQueueSaveOnShutdown on # save messages to disk on shutdown
        #$ActionQueueType LinkedList   # run asynchronously
        #$ActionResumeRetryCount -1    # infinite retries if host is down
        # remote host is: name/ip:port, e.g. 192.168.0.1:{syslog_port}, port optional
        #*.* @@remote-host:{syslog_port}
        # ### end of the forwarding rule ###
        """.format(syslog_port=options['syslog_port'])

        sysconfig_syslog_conf_content = """
        SYSLOGD_OPTIONS=\\"-m 0 -r -x\\"
        KLOGD_OPTIONS=\\"-x\\"
        SYSLOG_UMASK=077
        """
        etc_syslog_conf_content = """
        # Log all kernel messages to the console.
        # Logging much else clutters up the screen.
        #kern.*                                                 /dev/console

        # Log anything (except mail) of level info or higher.
        # Don't log private authentication messages!
        *.info;mail.none;news.none;authpriv.none;cron.none;*.debug;*.*              /var/log/messages

        # The authpriv file has restricted access.
        authpriv.*                                              /var/log/secure

        # Log all the mail messages in one place.
        mail.*                                                  -/var/log/maillog


        # Log cron stuff
        cron.*                                                  /var/log/cron

        # Everybody gets emergency messages
        *.emerg                                                 *

        # Save news errors of level crit and higher in a special file.
        uucp,news.crit                                          /var/log/spooler

        # Save boot messages also to boot.log
        local7.*                                                /var/log/boot.log

        #
        # INN
        #
        news.crit                                        /var/log/news/news.crit
        news.err                                         /var/log/news/news.err
        news.notice                                       /var/log/news/news.notice
        """


        # check rsyslog or syslog
        result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/bin/rpm -qa|/bin/grep rsyslog")
        if re.search(r"rsyslog-\d+", result, re.I):
            service_name = "rsyslog"
        else:
            service_name = "syslog"
        # check rsyslog tls
        rsyslog_tls_start_result = True
        if options['pro_option'] == 'tls':
            result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/bin/rpm -qa|/bin/grep rsyslog")
            if re.search(r"rsyslog-gnutls-\d+", result, re.I) and re.search(r"rsyslog-\d+", result, re.I):
                rsyslog_tls_start_result = True
            else:
                device.log(message="Fail to install rsyslog TLS related rpm rsyslog and rsyslog-gnutls", level="ERROR")
                rsyslog_tls_start_result = False

        if options['config_file'] == 'yes':
            if service_name == "rsyslog":
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}".format(options['cfg_name'])
                )
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}".format(options['cfg_tls_name'])
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="/bin/mv -f /etc/{} /etc/{}".format(options['cfg_name'], options['cfg_name_bak'])
                )
                if options['pro_option'] == 'tls':
                    dev.execute_shell_command_on_device(
                        device=device,
                        timeout=options["timeout"],
                        command="""echo "{}" >  /root/{}""".format(rsyslog_tls_conf_content, options['cfg_tls_name'])
                    )
                    dev.execute_shell_command_on_device(
                        device=device,
                        timeout=options["timeout"],
                        command="chmod 755 /root/{}".format(options['cfg_tls_name'])
                    )
                    dev.execute_shell_command_on_device(
                        device=device,
                        timeout=options["timeout"],
                        command="/bin/cp -f /root/{} /etc/{}".format(options['cfg_tls_name'], options['cfg_name'])
                    )
                else:
                    dev.execute_shell_command_on_device(
                        device=device,
                        timeout=options["timeout"],
                        command="""echo "{}" >  /root/{}""".format(rsyslog_conf_content, options['cfg_name'])
                    )
                    dev.execute_shell_command_on_device(
                        device=device,
                        timeout=options["timeout"],
                        command="chmod 755 /root/{}".format(options['cfg_name'])
                    )
                    dev.execute_shell_command_on_device(
                        device=device,
                        timeout=options["timeout"],
                        command="/bin/cp -f /root/{} /etc/{}".format(options['cfg_name'], options['cfg_name'])
                    )

            else:
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}".format(service_name)
                )
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}.conf".format(service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="/bin/mv -f /etc/sysconfig/{0} /etc/sysconfig/{0}.bak".format(service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="/bin/mv -f /etc/{0}.conf /etc/{0}.conf.bak".format(service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="""echo "{}" >  /root/{}""".format(sysconfig_syslog_conf_content, service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="""echo "{}" >  /root/{}.conf""".format(etc_syslog_conf_content, service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="chmod 755 /root/{}".format(service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="chmod 755 /root/{}.conf".format(service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="/bin/cp -f /root/{0} /etc/sysconfig/{0}".format(service_name)
                )
                dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options["timeout"],
                    command="/bin/cp -f /root/{0}.conf /etc/{0}.conf".format(service_name)
                )
        else:
            device.log(message="Not configure rsyslog/syslog config file", level="INFO")

        # start rsyslog server
        rsyslog_service_start_result = True
        if options['operation'] is not None:
            if options['restart'] == 'True':
                result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="service syslog stop")
                result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="service rsyslog stop")
                for i in range(1, 10):
                    result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/sbin/service {} restart".format(service_name))
                    time.sleep(2)
                    result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/bin/netstat -an | /bin/grep {}".format(options['syslog_port']))

                    if options['pro_option'] == 'tcpudp':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"udp.*0.0.0.0:{}".format(options['syslog_port']), result, re.I) and re.search(r"tcp.*:::{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"udp.*:::{}".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog service", level="INFO")
                            break
                        else:
                            device.log(message="Fail to restart rsyslog/syslog tcp and udp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'tcp':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"tcp.*:::{}.*LISTEN".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog tcp service", level="INFO")
                            break
                        else:
                            device.log(message="Fail to restart rsyslog/syslog tcp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'tcp_ipv4':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog IPv4 tcp service", level="INFO")
                            break
                        else:
                            device.log(message="Fail to restart rsyslog/syslog IPv4 tcp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'udp':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"udp.*0.0.0.0:{}".format(options['syslog_port']), result, re.I) and re.search(r"udp.*:::{}".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog udp service", level="INFO")
                            break
                        else:
                            device.log(message="Fail to restart rsyslog/syslog udp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'udp_ipv4':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"udp.*0.0.0.0:{}".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog IPv4 udp service", level="INFO")
                            break
                        else:
                            device.log(message="Fail to restart rsyslog/syslog IPv4 udp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'tls':
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"tcp.*:::{}.*LISTEN".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog tls service", level="INFO")
                            break
                        else:
                            device.log(message="Fail to restart rsyslog/syslog tls service", level="INFO")
                            rsyslog_service_start_result = False
                    else:
                        device.log(message="Not supported protocol type", level="INFO")
                        rsyslog_service_start_result = False
                        break

                else:
                    result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/sbin/service {} restart".format(service_name))
                    time.sleep(1)
                    result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/bin/netstat -an | /bin/grep {}".format(options['syslog_port']))

                    if options['pro_option'] == 'tcpudp':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"udp.*0.0.0.0:{}".format(options['syslog_port']), result, re.I) and re.search(r"tcp.*:::{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"udp.*:::{}".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog tcp and udp service", level="INFO")
                        else:
                            device.log(message="Fail to restart rsyslog/syslog tcp and udp service", level="ERROR")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'tcp':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"tcp.*:::{}.*LISTEN".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog tcp service", level="INFO")
                        else:
                            device.log(message="Fail to restart rsyslog/syslog tcp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'tcp_ipv4':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog IPv4 tcp service", level="INFO")
                        else:
                            device.log(message="Fail to restart rsyslog/syslog IPv4 tcp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'udp':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"udp.*0.0.0.0:{}".format(options['syslog_port']), result, re.I) and re.search(r"udp.*:::{}".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog udp service", level="INFO")
                        else:
                            device.log(message="Fail to restart rsyslog/syslog udp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'udp_ipv4':
                        syslog_port_int = str(options['syslog_port'])
                        port_count = result.count(syslog_port_int)
                        if re.search(r"udp.*0.0.0.0:{}".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog IPv4 udp service", level="INFO")
                        else:
                            device.log(message="Fail to restart rsyslog/syslog IPv4 udp service", level="INFO")
                            rsyslog_service_start_result = False
                    elif options['pro_option'] == 'tls':
                        if re.search(r"tcp.*0.0.0.0:{}.*LISTEN".format(options['syslog_port']), result, re.I) and re.search(r"tcp.*:::{}.*LISTEN".format(options['syslog_port']), result, re.I):
                            rsyslog_service_start_result = True
                            device.log(message="Success to restart rsyslog/syslog tls service", level="INFO")
                        else:
                            device.log(message="Fail to restart rsyslog/syslog tls service", level="ERROR")
                            rsyslog_service_start_result = False
            else:
                result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="service {} {}".format(service_name, options['operation']))
        if rsyslog_tls_start_result is False:
            rsyslog_service_start_result = False

        device.log(message="{} return value: {}".format(func_name, rsyslog_service_start_result), level="INFO")
        return rsyslog_service_start_result

    def rollback_rsyslog_cfg(self, device, **kwargs):
        """Configure rsyslog cfg file
        Robot example:
        setup_server.Rollback rsyslog cfg    device=${h1}


        :param Device device:
        **REQUIRED** Handle of the device on which commands have to be executed.

        :param STR cfg_name:
            *OPTIONAL* rsyslog cfg file name, default is rsyslog.conf

        :param STR cfg_tls_name:
            *OPTIONAL* rsyslog tls cfg file name, default is rsyslog.conf.tls

        :param STR cfg_name_bak:
            *OPTIONAL* rsyslog cfg backup file name, default is rsyslog.conf.bak

        :param STR cfg_tls_name_bak:
            *OPTIONAL* rsyslog cfg backup file name, default is rsyslog.conf.tls.bak

        :param STR delete_file:
            *OPTIONAL* delete rsyslog cfg file, default is yes

        :param STR rollback_file:
            *OPTIONAL* rollback rsyslog cfg file, default is yes

        :param INT timeout:
            *OPTIONAL* Server start timeout. Default: 300

        :return:
            Return True if rsyslog service start success. Or False if start failed.
            For invalid option will raise "ValueError"
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        all_option_list = (
            "cfg_name", "cfg_tls_name", "cfg_name_bak", "cfg_tls_name_bak",
            "syslog_port", "delete_file", "rollback_file", "timeout", "pro_option",
        )
        options = {}
        for keyword in all_option_list:
            options[keyword] = kwargs.get(keyword, None)
        if options['timeout'] is None:
            options['timeout'] = kwargs.get('timeout', 300)
        if options['cfg_name'] is None:
            options['cfg_name'] = "rsyslog.conf"
        if options['cfg_tls_name'] is None:
            options['cfg_tls_name'] = "rsyslog.conf.tls"
        if options['cfg_name_bak'] is None:
            options['cfg_name_bak'] = "rsyslog.conf.bak"
        if options['cfg_tls_name_bak'] is None:
            options['cfg_tls_name_bak'] = "rsyslog.conf.tls.bak"
        if options['delete_file'] is None:
            options['delete_file'] = "yes"
        if options['rollback_file'] is None:
            options['rollback_file'] = "yes"
        # create backup file

        # check rsyslog or syslog
        result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/bin/rpm -qa|/bin/grep rsyslog")
        if re.search(r"rsyslog-\d+", result, re.I):
            service_name = "rsyslog"
        else:
            service_name = "syslog"

        if service_name == "rsyslog":
            if options['delete_file'] == 'yes':
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}".format(options['cfg_name'])
                )
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}".format(options['cfg_tls_name'])
                )
            if options['rollback_file'] == 'yes':
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/mv -f /etc/{} /etc/{}".format(options['cfg_name_bak'], options['cfg_name'])
                )
        else:
            if options['delete_file'] == 'yes':
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}".format(service_name)
                )
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/rm -rf /root/{}.conf".format(service_name)
                )
            if options['rollback_file'] == 'yes':
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/mv -f /etc/sysconfig/{0}.bak /etc/sysconfig/{0}".format(service_name)
                )
                result = dev.execute_shell_command_on_device(
                    device=device,
                    timeout=options['timeout'],
                    command="/bin/mv -f /etc/{0}.conf.bak /etc/{0}.conf".format(service_name)
                )

        return True

    def start_nfs_service(self, device, **kwargs):
        """Configure nfs cfg file

        Robot example:
        setup_server.Start NFS Service    device=${h1}

        :param Device device:
            **REQUIRED** Handle of the device on which commands have to be executed.

        :param STR mount_folder:
            *OPTIONAL* NFS root directory path. Default: /dev/shm/nfs

        :param BOOL add_firewall_rule:
            *OPTIONAL* Add firewall rule. Default: False

        :param STR firewall_zone_name:
            *OPTIONAL* Firewall rule's specific zone name. Only implemented for add_firewall_rule=True. Default: public

        :param STR service_control_tool:
            *OPTIONAL* Modern OS use "systemctl" to manage each service so far, but older OS such as 'CentOS 6', 'Ubuntu 14' use "service". This
                       option should be "systemctl" or "service". Default: "service"

        :return:
            Return True if nfs service start success. Or False if start failed.
            Raise "ValueError" for invalid option
            Raise "RuntimeError" for service start failed
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}

        # delete last '/' for given folder path
        options["mount_folder"] = re.sub(r"/$", "", kwargs.pop("mount_folder", "/dev/shm/nfs"))
        options["add_firewall_rule"] = self.tool.check_boolean(kwargs.pop("add_firewall_rule", False))
        options["firewall_zone_name"] = str(kwargs.pop("firewall_zone_name", "public"))
        options["service_control_tool"] = kwargs.get("service_control_tool", self.host.get_service_management_tool(device=device)).strip().lower()

        # default is 'service' for compatibility
        options["service_control_tool"] = "service" if options["service_control_tool"] == "unknown" else options["service_control_tool"]

        if options["service_control_tool"] not in ("systemctl", "service"):
            raise ValueError("option 'service_control_tool' must be 'systemctl' or 'service', but got '{}'".format(options["service_control_tool"]))

        folder_path, folder_name = os.path.split(options["mount_folder"])
        cmds = []
        if options["mount_folder"] not in ("/tmp", "/mnt"):
            cmds.append("/bin/mkdir -p {}".format(options["mount_folder"]))
            cmds.append("/bin/chmod 755 {}".format(options["mount_folder"]))
        cmds.append("/bin/ls -l {}".format(folder_path))

        response = dev.execute_shell_command_on_device(device=device, command=cmds)
        found_mount_folder = False
        for line in response.splitlines():
            if re.search(r"drwx.*\s+{}".format(folder_name), line):
                found_mount_folder = True
                break

        if found_mount_folder is False:
            device.log(message=response, level="ERROR")
            raise RuntimeError("Create mount folder failed...")

        cmds = []
        if options["add_firewall_rule"] is True:
            cmds.append("firewall-cmd --zone={} --add-service=rpc-bind".format(options["firewall_zone_name"]))
            cmds.append("firewall-cmd --zone={} --add-service=mountd".format(options["firewall_zone_name"]))
            cmds.append("firewall-cmd --zone={} --add-service=nfs".format(options["firewall_zone_name"]))
            cmds.append("firewall-cmd --reload")

        cmds.append("""/bin/echo '/tmp    *(rw,insecure)' > /etc/exports""")
        cmds.append("""/bin/echo '{}    *(rw,sync,no_root_squash,no_all_squash,insecure,fsid=0)' >> /etc/exports""".format(options["mount_folder"]))

        if options["service_control_tool"] == "systemctl":
            cmds.append("systemctl restart nfs")
            cmds.append("systemctl restart rpcbind")
        else:
            cmds.append("service nfs restart")
            cmds.append("service rpcbind restart")

        cmds.append("showmount -e 127.0.0.1")

        response = dev.execute_shell_command_on_device(device=device, command=cmds)
        if not re.search(r"{}\s+\*".format(options["mount_folder"]), response):
            raise RuntimeError("Given mount path '{}' is not implemented".format(options["mount_folder"]))

        device.log(message="{} return value: True".format(func_name), level="INFO")
        return True

    def stop_nfs_service(self, device, **kwargs):
        """Stop NFS service

        Robot example:
        setup_server.Stop NFS Service    device=${h1}

        :param Device device:
            **REQUIRED** Handle of the device on which commands have to be executed.

        :param STR mount_folder:
            *OPTIONAL* NFS root directory path. Default: /dev/shm/nfs

        :param BOOL del_firewall_rule:
            *OPTIONAL* Delete firewall rule. Default: False

        :param STR firewall_zone_name:
            *OPTIONAL* Firewall rule's specific zone name. Only implemented for add_firewall_rule=True. Default: public

        :param STR service_control_tool:
            *OPTIONAL* Modern OS use "systemctl" to manage each service so far, but older OS such as 'CentOS 6', 'Ubuntu 14' use "service". This
                       option should be "systemctl" or "service". Default: "service"

        :return:
            Return True if nfs service stop success. Or False if stop failed.
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["mount_folder"] = re.sub(r"/$", "", kwargs.pop("mount_folder", "/dev/shm/nfs"))
        options["del_firewall_rule"] = self.tool.check_boolean(kwargs.pop("del_firewall_rule", False))
        options["firewall_zone_name"] = str(kwargs.pop("firewall_zone_name", "public"))
        options["service_control_tool"] = kwargs.get("service_control_tool", self.host.get_service_management_tool(device=device)).strip().lower()

        # default is 'service' for compatibility
        options["service_control_tool"] = "service" if options["service_control_tool"] == "unknown" else options["service_control_tool"]

        if options["service_control_tool"] not in ("systemctl", "service"):
            raise ValueError("option 'service_control_tool' must be 'systemctl' or 'service', but got '{}'".format(options["service_control_tool"]))

        cmds = []
        cmds.append("/bin/rm -rf {}".format(options["mount_folder"]))
        if options["del_firewall_rule"] is True:
            cmds.append("firewall-cmd --zone={} --remove-service=rpc-bind".format(options["firewall_zone_name"]))
            cmds.append("firewall-cmd --zone={} --remove-service=mountd".format(options["firewall_zone_name"]))
            cmds.append("firewall-cmd --zone={} --remove-service=nfs".format(options["firewall_zone_name"]))
            cmds.append("firewall-cmd --reload")

        if options["service_control_tool"] == "systemctl":
            cmds.append("systemctl stop nfs")
            cmds.append("systemctl stop rpcbind")
        else:
            cmds.append("service nfs stop")
            cmds.append("service rpcbind stop")

        dev.execute_shell_command_on_device(device=device, command=cmds)
        device.log(message="{} return value: True".format(func_name), level="INFO")
        return True

    def start_tftp_service(self, device, **kwargs):
        """Start TFTP service on CentOS 7 host

        Currently only support CentOS 7+ or controled by 'systemctl' platform

        Robot example:
        setup_server.Start TFTP Service    device=${h1}

        :param Device device:
            **REQUIRED** Handle of the device on which commands have to be executed.

        :param STR tftp_boot_folder:
            *OPTIONAL* tftp upload/download folder. default: /tftpboot

        :param BOOL upload_support:
            *OPTIONAL* Whether support upload file to tftp server. default: True

        :param STR scp_upload_username:
            *OPTIONAL* Upload configure file account. default: root

        :param STR scp_upload_password:
            *OPTIONAL* Upload configure file password.

        :param BOOL return_conf:
            *OPTIONAL* Return tftp configuration and systemd service configuraion like below instead of return True/False. default: False

            {
                "conf": "all tftp configuration lines",
                "systemd_conf": "all systemd configuration lines",
                "status": True or False,
            }

        :return:
            Return True if TFTP service start success. Or False if start failed.
            Raise "ValueError" for invalid option
            Raise "RuntimeError" for service start failed
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["upload_support"] = self.tool.check_boolean(kwargs.pop("upload_support", True))
        options["tftp_boot_folder"] = kwargs.pop("tftp_boot_folder", "/tftpboot")
        options["return_conf"] = self.tool.check_boolean(kwargs.pop("return_conf", False))
        options["scp_upload_username"] = kwargs.pop("scp_upload_username", self.default["root_username"])
        options["scp_upload_password"] = kwargs.pop("scp_upload_password", self.default["root_password"])

        # checking tftp configure file and backup
        for file_path in (self.path["tftp_xinetd_file_path"], self.path["tftp_systemd_file_path"]):
            response = dev.execute_shell_command_on_device(device=device, command="/bin/ls -l {}".format(file_path))
            if re.search(r"No such file", response, re.I):
                raise RuntimeError("Needed configuration file not found in {}".format(file_path))

            response = dev.execute_shell_command_on_device(device=device, command="/bin/ls -l {}.bak".format(file_path))
            if re.search(r"No such file", response, re.I):
                dev.execute_shell_command_on_device(device=device, command="/bin/cp {0} {0}.bak".format(file_path))

        cmds = [
            "/bin/mkdir -p {}".format(options["tftp_boot_folder"]),
            "/bin/chmod 777 {}".format(options["tftp_boot_folder"]),
        ]
        dev.execute_shell_command_on_device(device=device, command=cmds)

        tftp_conf_lines = []
        tftp_conf_lines.append("""service tftp""")
        tftp_conf_lines.append("""{""")
        tftp_conf_lines.append("""    socket_type     = dgram""")
        tftp_conf_lines.append("""    protocol        = udp""")
        tftp_conf_lines.append("""    wait            = yes""")
        tftp_conf_lines.append("""    user            = root""")
        tftp_conf_lines.append("""    server          = /usr/sbin/in.tftpd""")

        if options["upload_support"] is True:
            tftp_conf_lines.append("""    server_args     = -c -s {}""".format(options["tftp_boot_folder"]))
        else:
            tftp_conf_lines.append("""    server_args     = -s {}""".format(options["tftp_boot_folder"]))

        tftp_conf_lines.append("""    disable         = no""")
        tftp_conf_lines.append("""    per_source      = 11""")
        tftp_conf_lines.append("""    cps             = 100 2""")
        tftp_conf_lines.append("""    flags           = IPv4""")
        tftp_conf_lines.append("""}""")
        tftp_conf_lines.append("""""")

        tftp_systemd_conf_lines = []
        tftp_systemd_conf_lines.append("""[Unit]""")
        tftp_systemd_conf_lines.append("""Description=Tftp Server""")
        tftp_systemd_conf_lines.append("""Requires=tftp.socket""")
        tftp_systemd_conf_lines.append("""Documentation=man:in.tftpd""")
        tftp_systemd_conf_lines.append("""""")
        tftp_systemd_conf_lines.append("""[Service]""")

        if options["upload_support"] is True:
            tftp_systemd_conf_lines.append("""ExecStart=/usr/sbin/in.tftpd -c -s {}""".format(options["tftp_boot_folder"]))
        else:
            tftp_systemd_conf_lines.append("""ExecStart=/usr/sbin/in.tftpd -s {}""".format(options["tftp_boot_folder"]))

        tftp_systemd_conf_lines.append("""StandardInput=socket""")
        tftp_systemd_conf_lines.append("""""")
        tftp_systemd_conf_lines.append("""[Install]""")
        tftp_systemd_conf_lines.append("""Also=tftp.socket""")
        tftp_systemd_conf_lines.append("""WantedBy=multi-user.target""")
        tftp_systemd_conf_lines.append("""""")

        element_list = (
            # local_tmp_file_path, conf_content, remote_file_path
            ("/tmp/tftp.{}".format(os.getpid()), tftp_conf_lines, self.path["tftp_xinetd_file_path"]),
            ("/tmp/tftp.service.{}".format(os.getpid()), tftp_systemd_conf_lines, self.path["tftp_systemd_file_path"]),
        )

        for local_tmp_file_path, conf_content, remote_file_path in element_list:
            with open(local_tmp_file_path, "w") as fid:
                fid.write("\n".join(conf_content))

            status = device.upload(
                local_file=local_tmp_file_path,
                remote_file=remote_file_path,
                user=options["scp_upload_username"],
                password=options["scp_upload_password"],
                protocol="scp",
            )
            if os.path.isfile(local_tmp_file_path):
                os.remove(local_tmp_file_path)

            if status is False:
                raise RuntimeError("Failed to upload configure file to remote path: {}".format(remote_file_path))

            device.log(message="upload configure file to remote path complete: {}".format(remote_file_path), level="INFO")

        # restart xinetd and tftp service and checking
        cmds = [
            "/bin/systemctl daemon-reload",
            "/bin/systemctl restart xinetd",
            "/bin/systemctl restart tftp",
        ]
        dev.execute_shell_command_on_device(device=device, command=cmds)

        no_error = True
        for service in ("xinetd", "tftp"):
            response = dev.execute_shell_command_on_device(device=device, command="/bin/systemctl status {} | /bin/cat".format(service))
            if not re.search(r"Active:\s+active\s+\(running\)", response, re.I):
                no_error = False
                device.log(message="{} service is not running".format(service), level="ERROR")

        netstat_pattern_list = [
            re.compile(r"\s+0.0.0.0:69\s+"),
            re.compile(r"\s+:::69\s+"),
        ]

        response = dev.execute_shell_command_on_device(device=device, command="/bin/netstat -tnulp")
        for pattern in netstat_pattern_list:
            if not re.search(pattern, response):
                no_error = False
                device.log(message="port 69 is not listened on host", level="ERROR")

        if options["return_conf"] is True:
            return_value = {
                "status": no_error,
                "conf": "\n".join(tftp_conf_lines),
                "systemd_conf": "\n".join(tftp_systemd_conf_lines),
            }
        else:
            return_value = no_error

        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value
