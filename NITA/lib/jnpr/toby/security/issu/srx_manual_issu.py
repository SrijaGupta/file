#!/usr/bin/env python3
# coding: UTF-8
# pylint: disable=invalid-name
"""Use pexpect module to support SRX ISSU upgrade"""
from jnpr.toby.frameworkDefaults import credentials
from jnpr.toby.utils.flow_common_tool import flow_common_tool

import sys
import re
import time
import pexpect


class srx_manual_issu():
    """SRX platform ISSU upgrade"""
    def __init__(self):
        """Initialization"""
        self.tool = flow_common_tool()

        self.default = {
            "username": credentials.Junos["USERNAME"],
            "password": credentials.Junos["PASSWORD"],
            "cli_cmd_timeout": 300,
            "issu_finish_timeout": 43200,      # 12 hours
        }

        self.prompt = {
            "shell":    re.compile(r'\%\s+'),
            "cli":      re.compile(r'\w+@\S+\>\s+'),
            "conf":     re.compile(r'\w+@\S+\#\s+'),
        }
        self.hdl = None

    @staticmethod
    def print_log(device, message, level="INFO"):
        """Print log"""
        if device is None:
            print(message, flush=True)
        else:
            device.log(message=message, level=level)

    def login(self, device=None, **kwargs):
        """Login to device by ssh or telnet

        :param IPADDR ipaddr:
            *OPTIONAL* Device object

        :param STR username:
            *OPTIONAL* login username. default: regress

        :param STR password:
            *OPTIONAL* login password. default: MaRtInI

        :param INT login_timeout:
            *OPTIONAL* timeout to login device. default: 60

        :param BOOL show_process:
            *OPTIONAL* show login output. default: False

        :param STR login_failed_log_level:
            *OPTIONAL* default: ERROR

        Return:
            True/False or raise Exception for invalid option value

        Example:
            status = self.login()

        """
        options = {}
        options["device"] = device
        options["ipaddr"] = kwargs.pop("ipaddr", None)
        options["username"] = kwargs.pop("username", self.default["username"])
        options["password"] = kwargs.pop("password", self.default["password"])
        options["login_timeout"] = int(kwargs.pop("login_timeout", 60))
        options["show_process"] = self.tool.check_boolean(kwargs.get("show_process", False))
        options["login_failed_log_level"] = kwargs.get("login_failed_log_level", "ERROR")

        if options["device"] is None and options["ipaddr"] is None:
            raise RuntimeError("One of option 'device' or 'ipaddr' must be")

        if options["device"] is not None:
            hostname = options["device"].get_host_name().strip()

        if options["ipaddr"] is None:
            options["ipaddr"] = hostname

        self.print_log(device=options["device"], message=self.tool.print_title("Login: {}".format(options["ipaddr"])))
        try:
            hdl = pexpect.spawnu(
                'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -l {} {}'.format(options['username'], options["ipaddr"]),
                timeout=options["login_timeout"]
            )
        except pexpect.TIMEOUT as err: #pragma: no cover
            self.print_log(
                device=options["device"],
                message="Loging to device '{}' failed, output is:\n{}".format(options['ipaddr'], err),
                level=options["login_failed_log_level"],
            )
            return False

        hdl.logfile = None
        hdl.logfile_send = None
        hdl.logfile_read = None

        if options["show_process"] is True:
            hdl.logfile_read = sys.stdout

        index = hdl.expect([
            r'[Pp]assword:',
            pexpect.TIMEOUT,
            r"Operation timed out",
            r"Connection refused",
            r"not known",
            r"No route to host",
        ])
        if index == 0:
            hdl.sendline()
        elif index == 1:
            self.print_log(device=options["device"], message="login timeout.", level=options["login_failed_log_level"])
            return False
        else:
            self.print_log(device=options["device"], message="login failed.", level=options["login_failed_log_level"])
            return False

        hdl.expect(r'[Pp]assword:')
        hdl.sendline(options['password'])
        index = hdl.expect([
            self.prompt['shell'],
            self.prompt['cli'],
            r"incorrect",
            r"Permission denied",
        ])

        login_succeed = False
        if index in (0, 1):
            login_succeed = True
            self.hdl = hdl
        elif index == 2:
            message = "Password for '{}' is incorrect".format(options['username'])
        elif index == 3:
            message = "Permission denied while login to device '{}'.".format(options["ipaddr"])
        else:
            message = "unknown error about: \n{}".format(hdl)

        if login_succeed is False:
            self.print_log(device=options["device"], message=message, level=options["login_failed_log_level"])

        return login_succeed

    def mode_change(self, mode="cli", show_process=False):
        """Exchange to different cli mode

        :param STR mode:
            *OPTIONAL*  switch to JunOS prompt mode, must be one of 'cli', 'conf' or 'root'. default: cli

        :param BOOL show_process:
            *OPTIONAL*  whether show mode exchange output. default: False

        :return:
            True or False
        """
        self.hdl.logfile = None
        self.hdl.logfile_read = None
        self.hdl.logfile_send = None
        self.hdl.timeout = 60
        self.hdl.before = ""
        self.hdl.sendline()

        mode = mode.upper()

        if show_process is True:
            self.hdl.logfile_read = sys.stdout

        if mode == "SHELL":
            index = self.hdl.expect([
                self.prompt['shell'],
                self.prompt['cli'],
                self.prompt['conf'],
            ])

            if index == 0:
                return True
            elif index == 1:
                self.hdl.sendline("exit")
                self.hdl.expect(self.prompt['shell'])
            elif index == 2:
                self.hdl.sendline("exit")
                sub_index = self.hdl.expect([
                    self.prompt['cli'],
                    r"Exit with uncommitted changes",
                ])
                if sub_index == 0:
                    self.hdl.sendline("exit")
                    self.hdl.expect(self.prompt['shell'])
                elif sub_index == 1:
                    self.hdl.sendline("yes")
                    self.hdl.expect(self.prompt['cli'])
                    self.hdl.sendline("exit")
                    self.hdl.expect(self.prompt['shell'])
            else:
                pass

        if mode == "CLI":
            index = self.hdl.expect([
                self.prompt['shell'],
                self.prompt['cli'],
                self.prompt['conf'],
            ])

            if index == 0:
                self.hdl.sendline("cli")
                self.hdl.expect(self.prompt['cli'])
            elif index == 1:
                return True
            elif index == 2:
                self.hdl.sendline("exit")
                sub_index = self.hdl.expect([
                    self.prompt['cli'],
                    r"Exit with uncommitted changes",
                ])
                if sub_index == 0:
                    pass
                if sub_index == 1:
                    self.hdl.sendline("yes")
            else:
                pass

        if mode == "CONF":
            index = self.hdl.expect([
                self.prompt['shell'],
                self.prompt['cli'],
                self.prompt['conf'],
            ])

            if index == 0:
                self.hdl.sendline("cli")
                self.hdl.expect(self.prompt['cli'])
                self.hdl.sendline("conf")
                self.hdl.expect(self.prompt['conf'])
            elif index == 1:
                self.hdl.sendline("conf")
                self.hdl.expect(self.prompt['conf'])
            elif index == 2:
                return True
            else:
                pass

        return True

    def send(self, cmd, **kwargs):
        """Send command to device

        :param STR|LIST|TUPLE cmd:
            **REQUIRED**    single command string or mutil commands in LIST or TUPLE

        :param STR mode:
            *OPTIONAL*      command running mode. default: cli

        :param BOOL show_process:
            *OPTIONAL*      whether show command and it's output. default: True

        :param BOOL get_response:
            *OPTIONAL*      set True to get all cmds output. or False to return whether cmd send ok. default: True

        :param INT timeout:
            *OPTIONAL*      timeout to send cmd. default: 300

        :return:
            if get_response is True, will return a list which contain all cmds' output. otherwise return True/False
        """
        options = {}
        options["device"] = kwargs.pop("device", None)
        options["mode"] = kwargs.pop("mode", "cli")
        options["show_process"] = kwargs.pop("show_process", True)
        options["get_response"] = kwargs.pop("get_response", True)
        options["timeout"] = int(kwargs.pop("timeout", self.default["cli_cmd_timeout"]))

        self.mode_change(mode=options["mode"])
        self.hdl.before = ""
        self.hdl.timeout = options["timeout"]
        self.hdl.logfile = None
        self.hdl.logfile_read = None
        self.hdl.logfile_send = None

        if options["show_process"] is True:
            self.hdl.logfile_read = sys.stdout

        if isinstance(cmd, str):
            cmds = (cmd, )
        elif isinstance(cmd, (list, tuple)):
            cmds = cmd
        else:
            raise Exception("option 'cmd' must be a string or list but got '{}'".format(type(cmd)))

        lines = None
        for _cmd in cmds:
            _cmd = _cmd.strip()
            if re.match(r'show', _cmd) and not re.search(r"\|\s*no\-more$", _cmd):
                _cmd += " | no-more"

            self.print_log(device=options["device"], message="send cmd: {}".format(_cmd))
            self.hdl.sendline(_cmd)
            index = self.hdl.expect([
                self.prompt[options["mode"]],
                pexpect.TIMEOUT,
                pexpect.EOF,
                r"(?i)Do you want to continue with these actions being taken",
            ])
            if index == 0:
                pass
            elif index == 1:
                self.print_log(device=options["device"], message="Timeout to send command '{}'".format(cmd))
                return self.hdl.before
            elif index == 2:
                self.print_log(device=options["device"], message="Connection breaked.")
                return self.hdl.before
            elif index == 3:
                self.hdl.sendline("yes")
                sub_index = self.hdl.expect([
                    self.prompt[options["mode"]],
                    pexpect.TIMEOUT,
                    pexpect.EOF,
                ])
                if sub_index == 0:
                    pass
                return self.hdl.before
            else:
                self.print_log(device=options["device"], message="Unknown error occurred while sent '{}'".format(cmd))
                return self.hdl.before

            lines = re.split(r"\r\n|\r|\n", self.hdl.before)
            # For conf mode, [edit] line need to delete
            if options["mode"] == "conf": #pragma: no cover
                lines = lines[1:-2]
            else:
                lines = lines[1:]

        if options["get_response"] is True:
            response = "\n".join(lines)
        else: #pragma: no cover
            response = True

        return response

    def do_issu(self, **kwargs):
        """Main function

        :param STR package:
            **REQUIRED** package local path on device

        :param OBJECT device:
            *OPTIONAL* device object

        :param IP|DNS device_ipaddr:
            *OPTIONAL* primary node control ipaddress or DNS address. Notics: not primary device handler, just IP address.

        :param BOOL storage_cleanup_before_issu:
            *OPTIONAL*   cleanup all nodes' storage before issu. default: False

        :param STR username:
            *OPTIONAL*   device login username. default: regress

        :param STR password:
            *OPTIONAL*   device login password. default: MaRtInI

        :param INT login_timeout:
            *OPTIONAL*   timeout to connect device. default: 120 secs

        :param STR system:
            *OPTIONAL* system string for "system" or "vmhost". default: system

        :param BOOL no_copy:
            *OPTIONAL*   whether add 'no-copy' option while do ISSU. default: True

        :param STR more_options:
            *OPTIONAL*   tail more string to issu upgrade cmd. this is useful to add hidden options such as "no-validate", "no-compatibility-check"
                         etc... default: None

        :param INT reconnection_counter:
            *OPTIONAL*   during ISSU, connection to primary device will break and need to reconnect.
                         "reconnection_counter" and "reconnect_interval" option used for loop reconnection device.

                         default: 30

        :param INT reconnection_interval:
            *OPTIONAL*   default: 60

        :param INT cluster_checking_counter:
            *OPTIONAL*   after primary node rebooting, script will checking cluster state to make sure priority > 0 and cluster status is
                         'primary' or 'secondary'. option 'cluster_checking_counter' and 'cluster_checking_interval' used for loop checking
                         them. default: 20

        :param INT cluster_checking_interval:
            *OPTIONAL*   default: 60

        :return:
            True/False
        """
        options = {}
        options["package"] = kwargs.pop("package", None)
        options["device"] = kwargs.pop("device", None)
        options["device_ipaddr"] = kwargs.pop("device_ipaddr", None)
        options["username"] = kwargs.pop("username", self.default["username"])
        options["password"] = kwargs.pop("password", self.default["password"])
        options["login_timeout"] = int(kwargs.pop("login_timeout", 120))
        options["reconnection_interval"] = int(kwargs.pop("reconnection_interval", 60))
        options["reconnection_counter"] = int(kwargs.pop("reconnection_counter", 30))
        options["system"] = kwargs.pop("system", "system")
        options["no_copy"] = self.tool.check_boolean(kwargs.pop("no_copy", True))
        options["more_options"] = kwargs.pop("more_options", None)

        if options["package"] is None:
            raise RuntimeError("option 'package' must be set.")

        # login and initialize device
        status = self.login(
            device=options["device"],
            ipaddr=options["device_ipaddr"],
            username=options["username"],
            password=options["password"],
            login_timeout=options["login_timeout"],
            show_process=True,
            login_failed_log_level="ERROR",
        )
        if status is False:
            return status

        cmds = (
            "set cli screen-length 0",
            "set cli screen-width 0",
            "request chassis cluster in-service-upgrade abort",
        )
        self.send(device=options["device"], mode="cli", cmd=cmds, show_process=False)
        time.sleep(5)

        # send issu cmd to device and waiting for primary device reboot
        cmd_element_list = []
        cmd_element_list.append("request {} software in-service-upgrade {}".format(options["system"], options["package"]))
        if options["no_copy"] is True:
            cmd_element_list.append("no-copy")

        if options["more_options"] is not None:
            cmd_element_list.append(options["more_options"])

        cmd_element_list.append("reboot")
        issu_cmd = " ".join(cmd_element_list)

        self.print_log(device=options["device"], message="send cmd: {}".format(issu_cmd))
        result = self.send(device=options["device"], mode="cli", cmd=issu_cmd, timeout=self.default["issu_finish_timeout"])

        # if ISSU got error
        if not re.search(r"System going down IMMEDIATELY", result, re.I):
            self.print_log(device=options["device"], message="ISSU breaked with:\n{}".format(result), level="ERROR")
            return False

        # sleeping here prevent reconnect success even device is not rebooting
        self.print_log(device=options["device"], message="waiting '120' secs for device rebooting...")
        time.sleep(120)

        reconnection_success = False
        for index in range(1, options["reconnection_counter"] + 1):
            self.print_log(device=options["device"], message="{:02d}: reconnecting device '{}'".format(index, options["device_ipaddr"]))
            status = self.login(
                device=options["device"],
                ipaddr=options["device_ipaddr"],
                username=options["username"],
                password=options["password"],
                login_timeout=options["login_timeout"],
                show_process=True,
                login_failed_log_level="INFO",
            )
            if status is True:
                reconnection_success = True
                break

            self.print_log(device=options["device"], message="waiting '{}' secs for next reconnection...".format(options["reconnection_interval"]))
            time.sleep(options["reconnection_interval"])

        if reconnection_success is False:
            self.print_log(
                device=options["device"],
                message="reconnect failed after '{}' secs".format(options["reconnection_interval"] * options["reconnection_counter"]),
            )
            return False

        self.print_log(device=options["device"], message="ISSU Finished and devices reconnected.")
        return True
