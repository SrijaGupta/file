#!/usr/bin/env python3
# coding: UTF-8
"""TELNET client to create telnet session for Python3


Options:
    -i --ipaddr     <required> remote host ipaddr or name
    -c --commands   <optional> command which separated by comma or colon.
    -u --username   <optional> login username. default: regress
    -p --password   <optional> login password. default: MaRtInI
    -t --timeout    <optional> login connection timeout. default: 30

       --port       <optional> telnet service port. default: 23
       --hold-time  <optional> after all cmds send, wait for a while to keep session. default: 0
       --debug-level <optional> set 1 to see telnet details. default: 0

       --firewall-username  <optional> Special case to do Firewall authentication before TELNET login
       --firewall-password  <optional> Special case to do Firewall authentication before TELNET login
       --to-srx-device      <optional> Special case to do TELNET from HOST to SRX device

Return:
    Just print all cmds' response on sys.stdout channel.

Example:
    python telnet_client.py             \
        -i 10.208.132.127               \
        -c "ls -l:df -h"                \
        -u regress                      \
        -p MaRtInI                      \
        --port 2323                     \
        --hold-time 10                  \
        --firewall-username fw_user1    \
        --firewall-password fw_pass1

Use below command to show help:
    python telnet_client.py -h
"""
import sys
import re
import argparse
import time
import telnetlib

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

class TelnetClient(object):
    """TELNET client class"""
    def __init__(self):
        self.options = {}
        self.prompt = re.compile(rb"\S+\s+\S+\$\s")
        self.hdl = None
        self.code = "UTF-8"

    def user_option_parser(self, user_options=sys.argv[1:]):
        """To parser user options"""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-i',
            '--ipaddr',
            action="store",
            dest="ipaddr",
            default=None,
            required=True,
            help=u"host ipaddr",
        )

        parser.add_argument(
            '-u',
            '--username',
            action="store",
            dest="username",
            default="regress",
            help=u"login username",
        )

        parser.add_argument(
            '-p',
            '--password',
            action="store",
            dest="password",
            default="MaRtInI",
            help=u"login password",
        )

        parser.add_argument(
            '-t',
            '--timeout',
            action="store",
            dest="timeout",
            default="30",
            help=u"telnet timeout",
        )

        parser.add_argument(
            '-c',
            '--commands',
            action="store",
            dest="commands",
            default=None,
            help=u"command list separated by comma (,) to run at remote host",
        )

        parser.add_argument(
            '--port',
            action="store",
            dest="port",
            default="23",
            help=u"TELNET port",
        )

        parser.add_argument(
            '--hold-time',
            action="store",
            default="0",
            dest="hold_time",
            help=u"telnet hold time before terminated",
        )

        parser.add_argument(
            '--debug-level',
            action="store",
            default="0",
            dest="debuglevel",
            help=u"debug trace log",
        )

        parser.add_argument(
            '--firewall-username',
            action="store",
            default=None,
            dest="firewall_username",
            help=u"For firewall authentication",
        )

        parser.add_argument(
            '--firewall-password',
            action="store",
            default=None,
            dest="firewall_password",
            help=u"For firewall authentication",
        )

        parser.add_argument(
            '--to-srx-device',
            action="store_true",
            default=False,
            dest="to_srx_device",
            help=u"Do TELNET from HOST to SRX device",
        )


        options = parser.parse_args(args=user_options)
        self.options["ipaddr"] = options.ipaddr
        self.options['username'] = options.username
        self.options['password'] = options.password
        self.options['port'] = int(options.port)
        self.options['timeout'] = float(options.timeout)
        self.options['hold_time'] = int(options.hold_time)
        self.options['debuglevel'] = int(options.debuglevel)
        self.options['firewall_username'] = options.firewall_username
        self.options['firewall_password'] = options.firewall_password
        self.options['to_srx_device'] = options.to_srx_device

        if isinstance(options.commands, str):
            self.options["cmd_list"] = re.split(r"\s*[,:]\s*", options.commands)
        elif isinstance(options.commands, (list, tuple)):
            self.options["cmd_list"] = options.commands
        else:
            self.options["cmd_list"] = []

        return self.options

    def firewall_login(self, ipaddr, port, username, password):
        """Firewall authentication"""
        print("Firewall login ...")
        hdl = telnetlib.Telnet()
        hdl.set_debuglevel(self.options["debuglevel"])

        hdl.open(ipaddr, port)
        match = hdl.expect([rb"[uU]sername:\s+", rb"[lL]ogin:\s+"])
        # If match "login: ", it means do not need do firewall login
        if match[0] == 1:
            print(match[2])
            return True

        time.sleep(0.5)
        print("send firewall username: {}".format(username))
        cmd = username + "\r\n"
        hdl.write(cmd.encode(self.code))

        hdl.expect([rb"[pP]assword: ", ])

        time.sleep(0.5)
        print("send firewall password: {}".format(password))
        cmd = password + "\r\n"
        hdl.write(cmd.encode(self.code))
        match = hdl.expect([
            rb"Accepted",
            rb"Failed",
        ])
        print(match[2])
        if match[0] == 0:
            return True
        return False

    def login(self, ipaddr, port, username, password):
        """Normal login"""
        print("Telnet login ...")
        hdl = telnetlib.Telnet()
        hdl.set_debuglevel(self.options["debuglevel"])

        hdl.open(ipaddr, port)
        hdl.expect([rb"[lL]ogin:\s+", ])

        time.sleep(0.5)
        print("send telnet username: {}".format(username))
        cmd = username + "\r\n"
        hdl.write(cmd.encode(self.code))

        if self.options["to_srx_device"] is True:
            hdl.expect([rb"[pP]assword:", ])
        else:
            hdl.expect([rb"[pP]assword:\s+", ])

        time.sleep(0.5)
        print("send telnet password: {}".format(password))
        cmd = password + "\r\n"
        hdl.write(cmd.encode(self.code))
        match = hdl.expect([self.prompt, rb"incorrect"])
        if match[0] != 0:
            print(match[2].decode(self.code))
            return False

        self.hdl = hdl
        return True

    def execute_cmd(self):
        """send cmd to remote host and return cmd's stdout response"""
        all_response_lines = []
        for cmd in self.options["cmd_list"]:
            cmd_response = []
            cmd_response.append("send cmd: {}".format(cmd))

            cmd += "\r\n"
            self.hdl.write(cmd.encode(self.code))
            _, _, response = self.hdl.expect([self.prompt, ], self.options["timeout"])

            # delete first line about origin cmd
            cmd_response.extend(response.decode(self.code).splitlines())
            cmd_response[-1] = ""
            for line in cmd_response:
                print(line)
            all_response_lines.extend(response)

        if self.options["hold_time"] != 0:
            print("hold '{}' secs".format(self.options["hold_time"]))
            while self.options["hold_time"]:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(1)
                self.options["hold_time"] -= 1

            sys.stdout.write("\r\n")
            sys.stdout.flush()

        return all_response_lines

    def run(self):      # pragma: no cover
        """Entrance"""
        # analyse user options
        result = self.user_option_parser()
        assert result is not False, "Analyse user option failed."
        if self.options["to_srx_device"] is True:
            self.prompt = re.compile(rb"\%\s")

        # For special case if need do firewall login
        if self.options["firewall_username"] is not None and self.options["firewall_password"] is not None:
            status = self.firewall_login(
                ipaddr=self.options["ipaddr"],
                port=self.options["port"],
                username=self.options["firewall_username"],
                password=self.options["firewall_password"],
            )
            if status is False:
                return False

        # login
        status = self.login(
            ipaddr=self.options["ipaddr"],
            port=self.options["port"],
            username=self.options["username"],
            password=self.options["password"],
        )
        if status is False:
            return False

        # send command
        lines = self.execute_cmd()

        # terminate
        self.hdl.close()
        return lines

if __name__ == "__main__":      # pragma: no cover
    INS = TelnetClient()
    try:
        INS.run()
    except KeyboardInterrupt as err:
        print(err)
        exit(1)
