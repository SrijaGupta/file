# coding: UTF-8
# pylint: disable=invalid-name
"""Linux HOST related methods"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import os
import sys
import re
import threading
import shutil
from queue import Queue

from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.frameworkDefaults import credentials
from jnpr.toby.hldcl import device as dev
from jnpr.toby.hldcl.juniper.security import robot_keyword
from jnpr.toby.utils.flow_common_tool import flow_common_tool


class linux_tool(object):
    """Device related methods"""
    def __init__(self):
        """Init processing"""
        self.tool = flow_common_tool()

        self.default = {
            "timeout": 300,
            "tcpdump_record_file": "/tmp/tcpdump_record_file",
            "ftp_netrc_file": "~/.netrc",
            "memory_folder": "/dev/shm",
            "regress_username": credentials.Unix["USERNAME"],
            "regress_password": credentials.Unix["PASSWORD"],
            "root_username": credentials.Unix["SU"],
            "root_password": credentials.Unix["SUPASSWORD"],
            "pid": os.getpid(),
        }

        # prefer put temporary file to memory
        self.default["ftp_script_filename"] = "ftp_client.py"
        self.default["ftp_script_tmp_filename"] = "{}.{}".format(self.default["ftp_script_filename"], self.default["pid"])
        self.default["ftp_local_tmp_file"] = os.path.join(self.default["memory_folder"], self.default["ftp_script_tmp_filename"])

        self.default["telnet_script_filename"] = "telnet_client.py"
        self.default["telnet_script_tmp_filename"] = "{}.{}".format(self.default["telnet_script_filename"], self.default["pid"])
        self.default["telnet_local_tmp_file"] = os.path.join(self.default["memory_folder"], self.default["telnet_script_tmp_filename"])

        if not os.path.isdir(self.default["memory_folder"]):    # pragma: no cover
            self.default["ftp_local_tmp_file"] = os.path.join("/tmp", self.default["ftp_script_tmp_filename"])
            self.default["telnet_local_tmp_file"] = os.path.join("/tmp", self.default["telnet_script_tmp_filename"])

        # python2 and python3 compatible ftp/telnet script have different locations
        self.default["python3_ftp_client_file"] = None
        self.default["python3_telnet_client_file"] = None
        for path in sys.path:
            ftp_client = os.path.join(path, "jnpr/toby/utils", self.default["ftp_script_filename"])
            telnet_client = os.path.join(path, "jnpr/toby/utils", self.default["telnet_script_filename"])
            if os.path.isfile(ftp_client):
                self.default["python3_ftp_client_file"] = ftp_client

            if os.path.isfile(telnet_client):
                self.default["python3_telnet_client_file"] = telnet_client

        self.dev_info = {}
        self.hidden_info = {}
        self.hidden_info["pktgen_pid_list"] = []
        self.hidden_info["service_management_tool"] = {}

        # From URL: https://git.juniper.net/jonjiang/CommonTool/raw/master/python/ftp_client.py
        self.default["ftp_script_content"] = r"""#!/usr/bin/env python
# coding: UTF-8
import os
import re
import time
import optparse
import ftplib

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


class FTPClient(object):
    def __init__(self):
        self.options = {}
        self.ftp = None

        self.bufsize = 8192
        self.actions  = {}
        self.log_level = 1

    def user_option_parser(self):
        parser = optparse.OptionParser()

        parser.add_option(
            '-i',
            '--ipaddr',
            action="store",
            dest="ipaddr",
            default=None,
            help=u"host ipaddr",
        )

        parser.add_option(
            '-u',
            '--username',
            action="store",
            dest="username",
            default="regress",
            help=u"login username",
        )

        parser.add_option(
            '-p',
            '--password',
            action="store",
            dest="password",
            default="MaRtInI",
            help=u"login password",
        )

        parser.add_option(
            '-t',
            '--timeout',
            action="store",
            dest="timeout",
            default="60",
            help=u"cmd execution timeout",
        )

        parser.add_option(
            '',
            '--login-timeout',
            action="store",
            dest="login_timeout",
            default="30",
            help=u"Timeout for login",
        )

        parser.add_option(
            '-c',
            '--commands',
            action="store",
            dest="commands",
            default=None,
            help=u"command list separated by comma (,) to run at remote host",
        )

        parser.add_option(
            '',
            '--port',
            action="store",
            dest="port",
            default="21",
            help=u"FTP port",
        )

        parser.add_option(
            '',
            '--passive-mode',
            action="store_true",
            dest="passive",
            default=False,
            help=u"",
        )

        parser.add_option(
            '',
            '--hold-time',
            action="store",
            default="0",
            dest="hold_time",
            help=u"Hold FTP connection for given seconds before terminated",
        )

        parser.add_option(
            '',
            '--firewall-username',
            action="store",
            default=None,
            dest="firewall_username",
            help=u"For firewall authentication",
        )

        parser.add_option(
            '',
            '--firewall-password',
            action="store",
            default=None,
            dest="firewall_password",
            help=u"For firewall authentication",
        )

        options, _ = parser.parse_args()
        if options.ipaddr is None:
            print "At least remote host ipaddr must given."
            parser.print_help()
            return False

        self.options["ipaddr"] = options.ipaddr
        self.options['username'] = options.username
        self.options['password'] = options.password
        self.options['port'] = int(options.port)
        self.options['hold_time'] = int(options.hold_time)
        self.options['timeout'] = float(options.timeout)
        self.options['login_timeout'] = float(options.login_timeout)
        self.options['passive'] = options.passive
        self.options['firewall_username'] = options.firewall_username
        self.options['firewall_password'] = options.firewall_password

        if options.commands is None:
            self.options["cmd_list"] = []
        elif isinstance(options.commands, str):
            self.options["cmd_list"] = re.split(r"\s*[,:]\s*", options.commands)
        elif isinstance(options.commands, (list, tuple)):
            self.options["cmd_list"] = options.commands
        else:
            print "option '-c' or '--commands' must be a str, list or tuple but got '%s'" % type(options.commands)
            return False

        return self.options

    def firewall_login(self, ipaddr, port, username, password):
        try:
            ftp = ftplib.FTP()
            ftp.set_debuglevel(self.log_level)
            ftp.connect(host=ipaddr, port=port)
            ftp.login(user=username, passwd=password)
        except (Exception, ftplib.error_perm), err:
            if re.search(r"Authentication\s+\-\s+Accepted", str(err), re.I):
                return True
            else:
                print "Error to login host '%s:%s': %s" % (ipaddr, port, err)
                return False

    def ftp_login(self, ipaddr, port, username, password):
        try:
            ftp = ftplib.FTP()
            ftp.set_debuglevel(self.log_level)
            ftp.connect(host=ipaddr, port=port)
            ftp.login(user=username, passwd=password)
        except (Exception, ftplib.error_perm), err:
	    print "Error to login host '%s:%s': %s" % (ipaddr, port, err)
            return False

        ftp.getwelcome()

        self.ftp = ftp
        self.actions  = {
            'pwd':      self.pwd,
            'get':      self.get,
            'put':      self.put,
            'size':     self.size,
            'dir':      self.ftp.dir,
            'cd':       self.ftp.cwd,
            'ls':       self.ftp.nlst,
            'rmdir':    self.ftp.rmd,
            'mkdir':    self.ftp.mkd,
            'delete':   self.ftp.delete,
            'rename':   self.ftp.rename,
            'quit':     self.ftp.quit,
        }
        return ftp

    def get(self, filepath):
        if re.search(r"/", filepath):
            folder, filename = os.path.split(filepath)
            self.actions["cd"](folder)
        else:
            filename = filepath

        cmd = 'RETR ' + filename
        self.ftp.retrbinary(cmd, open(filename, 'wb').write, self.bufsize)
        print "'%s' download complete" % filename
        return True

    def put(self, filepath):
        folder, filename = os.path.split(filepath)
        fileHandler = open(filepath, 'rb')
        cmd = 'STOR ' + filename

        self.ftp.storbinary(cmd, fileHandler, self.bufsize)
        fileHandler.close()
        print "'%s' upload complete" % filepath
        return True

    def pwd(self):
        dirname = self.ftp.pwd()
        return dirname

    def size(self, filename):
        size = self.ftp.size(filename)
        return size

    def execute_cmd(self):
        cmd_list = self.options["cmd_list"]
        for cmd in cmd_list:
            print "send cmd: %s" % cmd
            try:
                if cmd == "pwd":
                    self.actions["pwd"]()

                elif re.match(r"get", cmd):
                    match = re.match(r"get\s+(\S+)", cmd)
                    self.actions["get"](match.group(1))

                elif re.match(r"put", cmd):
                    match = re.match(r"put\s+(\S+)", cmd)
                    self.actions["put"](match.group(1))

                elif re.match(r"size", cmd):
                    match = re.match(r"size\s+(\S+)", cmd)
                    self.actions["size"](match.group(1))

                elif re.match(r"cd", cmd):
                    match = re.match(r"cd\s+(\S+)", cmd)
                    self.actions["cd"](match.group(1))

                elif cmd in ("ls", "dir"):
                    self.actions["ls"]()

                elif re.match(r"rmdir", cmd):
                    match = re.match(r"rmdir\s+(\S+)", cmd)
                    self.actions["rmdir"](match.group(1))

                elif re.match(r"mkdir", cmd):
                    match = re.match(r"mkdir\s+(\S+)", cmd)
                    self.actions["mkdir"](match.group(1))

                elif re.match(r"delete", cmd):
                    match = re.match(r"delete\s+(\S+)", cmd)
                    filepath = match.group(1)
                    if re.search(r"/", filepath):
                        folder, filename = os.path.split(filepath)
                        self.actions["cd"](folder)
                    else:
                        filename = filepath

                    self.actions["delete"](filename)

                else:
                    print "unknown cmd '%s'" % cmd
                    return False

            except Exception, err:
                print err

        return True

    def run(self):
        self.user_option_parser()

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

        # Normal login
        status = self.ftp_login(
            ipaddr=self.options["ipaddr"],
            port=self.options["port"],
            username=self.options["username"],
            password=self.options["password"],
        )
        if status is False:
            return False

        # passive mode related
        if self.options["passive"] is True:
            self.ftp.set_pasv(True)
        else:
            self.ftp.set_pasv(False)

        self.execute_cmd()

        if self.options["hold_time"] != 0:
            print "hold '%d' secs." % self.options["hold_time"]
            time.sleep(self.options["hold_time"])

        return self.actions["quit"]()

if __name__ == "__main__":
    INS = FTPClient()
    try:
        INS.run()
    except KeyboardInterrupt, err:
        print err
        exit(1)

        """

        # From URL: https://git.juniper.net/jonjiang/CommonTool/raw/master/python/telnet_client.py
        self.default["telnet_script_content"] = r"""#!/usr/bin/env python
# coding: UTF-8

import sys
import re
import optparse
import time
import telnetlib

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

class TelnetClient(object):
    def __init__(self):
        self.options = {}
        self.prompt = re.compile(r"\S+\s+\S+\$\s")
        self.hdl = None

    def user_option_parser(self):
        parser = optparse.OptionParser()

        parser.add_option(
            '-i',
            '--ipaddr',
            action="store",
            dest="ipaddr",
            default=None,
            help=u"host ipaddr",
        )

        parser.add_option(
            '-u',
            '--username',
            action="store",
            dest="username",
            default="regress",
            help=u"login username",
        )

        parser.add_option(
            '-p',
            '--password',
            action="store",
            dest="password",
            default="MaRtInI",
            help=u"login password",
        )

        parser.add_option(
            '-t',
            '--timeout',
            action="store",
            dest="timeout",
            default="30",
            help=u"telnet timeout",
        )

        parser.add_option(
            '-c',
            '--commands',
            action="store",
            dest="commands",
            default=None,
            help=u"command list separated by comma (,) to run at remote host",
        )

        parser.add_option(
            '',
            '--port',
            action="store",
            dest="port",
            default="23",
            help=u"TELNET port",
        )

        parser.add_option(
            '',
            '--hold-time',
            action="store",
            default="0",
            dest="hold_time",
            help=u"telnet hold time before terminated",
        )

        parser.add_option(
            '',
            '--debug-level',
            action="store",
            default="0",
            dest="debuglevel",
            help=u"debug trace log",
        )

        parser.add_option(
            '',
            '--firewall-username',
            action="store",
            default=None,
            dest="firewall_username",
            help=u"For firewall authentication",
        )

        parser.add_option(
            '',
            '--firewall-password',
            action="store",
            default=None,
            dest="firewall_password",
            help=u"For firewall authentication",
        )

        parser.add_option(
            '',
            '--to-srx-device',
            action="store_true",
            default=False,
            dest="to_srx_device",
            help=u"From HOST do telnet to SRX device",
        )

        options, _ = parser.parse_args()
        if options.ipaddr is None:
            print "At least remote host ipaddr must given."
            parser.print_help()
            return False

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

        if options.commands is None:
            self.options["cmd_list"] = []
        elif isinstance(options.commands, str):
            self.options["cmd_list"] = re.split(r"\s*[,:]\s*", options.commands)
        elif isinstance(options.commands, (list, tuple)):
            self.options["cmd_list"] = options.commands
        else:
            print "option '-c' or '--commands' must be a str, list or tuple but got '%s'" % type(options.commands)
            return False

        return self.options

    def firewall_login(self, ipaddr, port, username, password):
        print "Firewall login ..."
        hdl = telnetlib.Telnet(ipaddr, port)
        hdl.set_debuglevel(self.options["debuglevel"])

        match = hdl.expect([r"[uU]sername:\s+", r"[lL]ogin:\s+"])
        # If match "login: ", it means do not need do firewall login
        if match[0] == 1:
             print match[2]
             return True

        time.sleep(0.5)
        print "send firewall username: %s" % username
        hdl.write(username + "\r\n")

        hdl.expect([r"[pP]assword: ", ])

        time.sleep(0.5)
        print "send firewall password: %s" % password
        hdl.write(password + '\r\n')
        match = hdl.expect([
            "Accepted",
            "Failed",
        ])
        print match[2]
        if match[0] == 0:
            return True
        return False

    def login(self, ipaddr, port, username, password):
        print "Telnet login ..."
        hdl = telnetlib.Telnet(ipaddr, port)
        hdl.set_debuglevel(self.options["debuglevel"])

        hdl.expect([r"[lL]ogin:\s+", ])
        time.sleep(0.5)
        print "send telnet username: %s" % username
        hdl.write(username + "\r\n")

        if self.options["to_srx_device"] is True:
            hdl.expect([r"[pP]assword:", ])
        else:
            hdl.expect([r"[pP]assword:\s+", ])

        time.sleep(0.5)
        print "send telnet password: %s" % password
        hdl.write(password + '\r\n')
        match = hdl.expect([self.prompt, "incorrect"])
        print match[2]
        if match[0] != 0:
            return False

        self.hdl = hdl
        return True

    def execute_cmd(self):
        all_response_lines = []
        for cmd in self.options["cmd_list"]:
            cmd_response = []
            cmd_response.append("send cmd: %s" % cmd)

            cmd += "\r\n"
            self.hdl.write(cmd)
            _, _, response = self.hdl.expect([self.prompt, ], self.options["timeout"])

            # delete first line about origin cmd
            cmd_response.extend(response.splitlines())
            cmd_response[-1] = ""
            for line in cmd_response:
                print line
            all_response_lines.extend(response)

        if self.options["hold_time"] != 0:
            print "hold '%s' secs" % self.options["hold_time"]
            while self.options["hold_time"]:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(1)
                self.options["hold_time"] -= 1

            sys.stdout.write("\r\n")
            sys.stdout.flush()

        return all_response_lines

    def run(self):
        # analyse user options
        result = self.user_option_parser()
        assert result is not False, "Analyse user option failed."

        if self.options["to_srx_device"] is True:
            self.prompt = re.compile(r"\%\s")

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

if __name__ == "__main__":
    INS = TelnetClient()
    try:
        INS.run()
    except KeyboardInterrupt, err:
        print err
        exit(1)

        """

    def get_service_management_tool(self, device, **kwargs):
        """Get service management tool name for specific host

        Read /etc/redhat_release or 'uname -r' command to see OS version and return service management tool used on this host

        :param BOOL force:
            *OPTIONAL* force get service management tool name without get from cache. default: False

        :return: Return 'systemctl', 'service' or 'unknown'
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["force"] = self.tool.check_boolean(kwargs.pop("force", False))

        if str(device) not in self.hidden_info["service_management_tool"]:
            self.hidden_info["service_management_tool"][str(device)] = None

        # return from cache if option 'force' is False
        if options["force"] is False and self.hidden_info["service_management_tool"][str(device)] is not None:
            device.log(message="{} return value:\n{}".format(func_name, self.hidden_info["service_management_tool"][str(device)]), level="INFO")
            return self.hidden_info["service_management_tool"][str(device)]

        info = self.get_host_info(device=device)

        # for ubuntu and CentOS 6, return 'service'
        # for CentOS 7, return 'systemctl'
        # others return 'unknown'
        if re.search(r"el7", info["version"], re.I):
            return_value = "systemctl"
        elif re.search(r"el6|generic", info["version"], re.I):
            return_value = "service"
        else:
            device.log(message="unknown host kernel '{}'".format(info["version"]), level="WARN")
            return_value = "unknown"

        self.hidden_info["service_management_tool"][str(device)] = return_value
        device.log(message="{} return value:\n{}".format(func_name, return_value), level="INFO")
        return return_value

    def send_shell_cmd(self, device, cmd, **kwargs):
        """Send command to host and get response

        This method has deprecated. You can use jnpr.toby.hldcl.device.execute_shell_command_on_device instead.
        Make sure option 'cmd' changed to 'command'

        Pay attention: option 'cmd' should be just one command or command list, but only last
        command's output return.

        :param str/list/tuple cmd:
            **REQUIRED** command string or command list to execute on host

        :param int timeout:
            *OPTIONAL* command run timeout

        :return:
            Return **last** command's output
        """
        func_name = self.tool.get_current_function_name()
        print(self.tool.print_title(func_name))

        options = {}
        options["timeout"] = int(kwargs.get("timeout", self.default["timeout"]))

        if isinstance(cmd, str):
            cmd_list = [cmd, ]
        elif isinstance(cmd, (list, tuple)):
            cmd_list = cmd
        else:
            raise TypeError("'cmd' must be a str, list or tuple, not '{}'".format(type(cmd)))

        for host_cmd in cmd_list:
            result = device.shell(command=host_cmd, timeout=options["timeout"]).response()

        device.log(message="{} return value:\n{}".format(func_name, result), level="INFO")
        return result

    def get_host_info(self, device, **kwargs):
        """Get LINUX host information

        :param int timeout:
            *REQUIRE* timeout to get device info. Default: 180

        :return:
            Return a DICT contain all LINUX Host info, otherwise return False. Example:

            {
                hostname:       "fnd-lnx31",
                kernel:         "2.6.32-71.el6",
                version:        "el6",
                kernel_mode:    "i686",
            }
        """
        options = {}
        options["timeout"] = int(kwargs.get("timeout", 180))

        response = dev.execute_shell_command_on_device(device=device, command="/bin/hostname", timeout=options["timeout"])
        hostname = response.strip()

        # if already have in previous
        if hostname in self.dev_info:
            return self.dev_info[hostname]

        response = dev.execute_shell_command_on_device(device=device, command="/bin/uname -r", timeout=options["timeout"])
        self.dev_info[hostname] = {}
        self.dev_info[hostname]['hostname'] = hostname

        if re.search(r"el\d+", response):
            # CentOS response
            elements = re.split(r"\.", response.strip())
            self.dev_info[hostname]['kernel'] = ".".join(elements[:-2])
            self.dev_info[hostname]['version'] = elements[-2]
            self.dev_info[hostname]['kernel_mode'] = elements[-1]

        elif re.search(r"generic", response):
            # Ubuntu response
            elements = re.split(r"\-", response.strip())
            self.dev_info[hostname]['kernel'] = elements[0]
            self.dev_info[hostname]['version'] = elements[1]
            self.dev_info[hostname]['kernel_mode'] = elements[2]
        else:
            device.log(message="Unknown host OS", level="WARN")
            self.dev_info[hostname]['kernel'] = ""
            self.dev_info[hostname]['version'] = ""
            self.dev_info[hostname]['kernel_mode'] = ""

        return self.dev_info[hostname]

    def su(self, device, **kwargs):
        """SU to superuser account

        :param str password:
            *OPTIONAL* superuser's password

        :return:
            True/False
        """
        func_name = self.tool.get_current_function_name()
        print(self.tool.print_title(func_name))

        options = {}
        options["password"] = kwargs.get("password", self.default["root_password"])
        options["su_command"] = kwargs.get("su_command", "su -")

        if isinstance(device, (list, tuple)):
            options["device"] = device
        else:
            options["device"] = (device, )

        result_list = []
        for dev_hdl in options["device"]:
            result_list.append(dev_hdl.su(password=options["password"], su_command=options["su_command"]))

        return_value = False not in result_list
        print("{} return value: {}".format(func_name, return_value))
        return return_value

    def reboot(self, device, **kwargs):
        """reboot device

        this method can reboot device in parallel and return reboot status (True or False) or reboot stdout.
        if option "on_parallel" is True and

        :param OBJ|OBJ_LIST device:
            **REQUIRED** device object or device object list.

        :param STR|INT wait:
            *OPTIONAL* wait time before reconnect host. default: 30

        :param STR|INT timeout:
            *OPTIONAL* timeout of rebooting. default: 1200

        :param STR|INT check_interval:
            *OPTIONAL* device reconnect interval (sec). default: 20

        :param BOOL on_parallel:
            *OPTIONAL* if device object is a list and this option set True, will reboot and checking device in parallel. default: True

                +  for 1 device, rebooting it as normal
                +  for 2+ devices, rebooting device on parallel as default.
                +  if on_parallel set True or False, force rebooting device on or not on parallel

            **Pay attention:** parallel reboot device will no reboot processing output logged.

        :return:
            return True|False to indicate all devices whether reboot succeed.
        """
        func_name = self.tool.get_current_function_name()
        print(self.tool.print_title(func_name))

        options = {}
        options["device"] = device
        options["wait"] = int(kwargs.get("wait", 30))
        options["timeout"] = int(kwargs.get("timeout", 1200))
        options["check_interval"] = int(kwargs.get("check_interval", 20))
        options["on_parallel"] = self.tool.check_boolean(kwargs.get("on_parallel", None))

        if not isinstance(options["device"], (list, tuple)):
            options["device"] = (options["device"], )

        dev_cnt = len(options["device"])
        if options["on_parallel"] is None:
            if dev_cnt == 1:
                options["on_parallel"] = False
            else:
                options["on_parallel"] = True

        queue = Queue(32)
        def run_function(dev_hdl, target, wait, timeout, interval):
            """run function and put output to queue"""
            try:
                dev_hdl.log("now rebooting '{}'".format(target), level="INFO")
                result = target(wait=wait, timeout=timeout, interval=interval)
                queue.put(result)
            except (Exception, RuntimeError) as err:
                queue.put(False)
                dev_hdl.log("Got error while rebooting device '{}' with err: {}".format(target, err), level="ERROR")

        if options["on_parallel"] is False:
            for dev_hdl in options["device"]:
                try:
                    dev_hdl.log("rebooting '{}' ...".format(dev_hdl), level="INFO")
                    queue.put(dev_hdl.reboot(wait=options["wait"], timeout=options["timeout"], interval=options["check_interval"]))
                except (Exception, RuntimeError) as err:
                    queue.put(False)
                    dev_hdl.log("Got err: {}".format(err), level="ERROR")
        else:
            thread_list = []
            for dev_hdl in options["device"]:
                thread_list.append(threading.Thread(
                    target=run_function,
                    name=str(dev_hdl),
                    args=(dev_hdl, dev_hdl.reboot, options["wait"], options["timeout"], options["check_interval"]),
                ))

            for thread in thread_list:
                print("parallel rebooting '{}' ...".format(thread))
                thread.start()

            for thread in thread_list:
                print("waiting for '{}' online...".format(thread))
                thread.join(timeout=options["timeout"] + 10)

        reboot_result_list = []
        while True:
            if queue.empty():
                break
            reboot_result_list.append(queue.get())

        print("all device reboot status: {}".format(reboot_result_list))
        return False not in reboot_result_list and len(reboot_result_list) == dev_cnt

    @staticmethod
    def loop_ping(device, dst_addr, **kwargs):
        """Do ping in loop by time interval

        Sometimes we need do loop ping. For example:

        1.  IPSec tunnel need first packet to start tunnel establishment
        2.  Boardcard is in restarting but not sure when finished, because low-end need more time
            than high-end

        This method do loop ping by option dst_addr, "dst_addr" should be one IPv4/v6 IP address or LIST of IPs, and then return ping result.
        Both support Linux and SRX device

        Please see **Example** section to know more

        :param OBJECT device:
            **REQUIRED** Source HOST's handle to do ping

        :param IP|LIST dst_addr:
            **REQUIRED** Destination IP address or hostname, should be a LIST to ping several IPs in one shoot

        :param INT ping_counter:
            *OPTIONAL* ping packet counter. Default: 4

        :param STR ping_option:
            *OPTIONAL* ping cmd's option such as '-c 5' or '-f', it will concatenate to ping cmd.
                        Default: None

        :param INT timeout:
            *OPTIONAL* Each ping check timeout. Default: default timeout in __init__

        :param STR ipv4_ping_cmd:
            *OPTIONAL* IPv4 ping command's path. default: /bin/ping (Linux) or /sbin/ping (SRX)

        :param STR ipv6_ping_cmd:
            *OPTIONAL* IPv6 ping command's path. default: /bin/ping6 (Linux) or /sbin/ping6 (SRX)

        :param INT loop_cnt:
            *OPTIONAL* Loop times to do ping check. Default: 1

        :param INT loop_interval:
            *OPTIONAL* sleep second between each loop. Default: 10

        :param STR device_type:
            *OPTIONAL* One of "SRX" or "LINUX". Default: None

            "SRX" and "LINUX" device have different behavior to ping. As default, this method decide device type automatically, or you can set
            device_type manually.

        :param STR get_detail:
            *OPTIONAL* As default the method return True/False to indicate ping success or failed. But set this option to True to get a DICT value For
                        one ping result like below:

                        return_value = {
                            "lost_rate":        10,
                            "lost_packet":      1,
                            "received_rate":    90,
                            "received_packet":  9,
                            ....
                        }

                        If "dst_addr" is IP list, will return a DICT like this:

                        return_value = {
                            "192.168.1.2":  {
                                "lost_rate":        10,
                                "lost_packet":      1,
                                "received_rate":    90,
                                "received_packet":  9,
                                ....
                            }
                            "192.168.1.3":  {
                                ...
                            }
                        }

                        Default: None

        :return:
            +   "dst_addr" contain 1 IP and no "get_detail"     - return True/False
            +   "dst_addr" contain 1+ IP and not "get_detail"   - return LIST like: [True, True, False]
            +   "dst_addr" contain 1 IP and "get_detail"=True   - return DICT contain all details
            +   "dst_addr" contain 1+ IP and "get_detail"=True  - return DICT contain all IPs detail

        :Example:

            1.  1 IP and get_detail=None or False

                loop_ping(device=h0, dst_addr="192.168.100.2")
                => True

            2.  1+ IP and get_detail=None or False

                loop_ping(device=h0, dst_addr=("192.168.100.2", "2000:200::2"))
                > [True, False]

            3.  1 IP and get_detail=True

                loop_ping(device=h0, dst_addr="192.168.100.2", get_detail=True)
                => {
                    "lost_rate":        10,
                    "lost_packet":      1,
                    "received_rate":    90,
                    "received_packet":  9,
                    ....
                }

            4.  1+ IP and get_detail=True

                loop_ping(device=h0, dst_addr=("192.168.100.2", "2000:200::2"), get_detail=True)
                => {
                    "192.168.100.2":    {
                        "lost_rate":        10,
                        "lost_packet":      1,
                        "received_rate":    90,
                        "received_packet":  9,
                        ....
                    },
                    "2000:200::2":      {
                        "lost_rate":        10,
                        "lost_packet":      1,
                        "received_rate":    90,
                        "received_packet":  9,
                        ....
                    },
                }

        """
        return robot_keyword.loop_ping(device=device, dst_addr=dst_addr, **kwargs)

    def reconnect(self, device, **kwargs):
        """Reconnect Linux host and switch to root

        Due to TOBY platform have keepalive issue, this method used to reconnect DEVICE and switch to root permission.
        Support both SRX and HOST

        :param STR|LIST device:
            **REQUIRED** device handler or device handler list.

        :param BOOL su:
            *OPTIONAL*   set True to force su root account. default: True

        :param INT timeout:
            *OPTIONAL*   reconnect and su timeout. default: 300

        :return:
            return True if all host reconnect succeed. otherwise return False
        """
        func_name = self.tool.get_current_function_name()
        print(self.tool.print_title(func_name))

        options = {}
        options["device"] = device
        options["su"] = self.tool.check_boolean(kwargs.get("su", True))
        options["timeout"] = int(kwargs.get("timeout", self.default["timeout"]))

        if not isinstance(options["device"], (list, tuple)):
            options["device"] = (options["device"], )

        all_result = []
        for hdl in options["device"]:
            status = hdl.reconnect()
            if status is False:
                hdl.log("Host '{}': Failed to reconnect host".format(str(hdl)), level="WARN")
                all_result.append(False)
                continue

            if options["su"] is True:
                status = hdl.su()
                if status is False:
                    hdl.log("Host '{}': Failed to switch to root".format(str(hdl)), level="WARN")
                    all_result.append(False)

        return_value = False not in all_result
        print("{} return value: {}".format(func_name, return_value))
        return return_value

    def start_tcpdump_on_host(self, device, options, **kwargs):
        """Start tcpdump processing in background

        :param str options:
            *OPTIONAL* tcpdump filter string such as '-nni eth1 tcp' or
                       '-nni eth1 udp and port 8000', etc...

        :param str record_file:
            *OPTIONAL* tcpdump output record file. Default: /tmp/tcpdump_record_file

        :param bool cleanup_previous:
            *OPTIONAL* set True will invoke ps command to list all existing tcpdump threading and
                       kill them all. Or set False just start new one. Default: True

        :param int timeout:
            *OPTIONAL* execute tcpdump command timeout, not tcpdump waiting time. Default: 300

        :return:
            Return PID number if tcpdump start success
        """
        func_name = self.tool.get_current_function_name()
        print(self.tool.print_title(func_name))

        para = {}
        para["options"] = options
        para["record_file"] = kwargs.get("record_file", self.default["tcpdump_record_file"])
        para["cleanup_previous"] = self.tool.check_boolean(kwargs.get("cleanup_previous", True))
        para["timeout"] = int(kwargs.get("timeout", self.default["timeout"]))

        if para["cleanup_previous"] is True:
            status = self.stop_tcpdump_on_host(device=device, return_mode="status")
            if status is False:
                device.log(message="cleanup previous tcpdump threading failed.", level="WARN")

        cmd = "/usr/bin/nohup /usr/sbin/tcpdump -w {} {} > /dev/null 2>&1 &".format(para["record_file"], para["options"])
        result = dev.execute_shell_command_on_device(device=device, command=cmd, timeout=para["timeout"])
        match = re.search(r"\[\d+\]\s+(\d+)", str(result).strip())
        if not match:
            raise RuntimeError("Unknown issue that cannot get PID number.")

        return_value = int(match.group(1))
        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def stop_tcpdump_on_host(self, device, pid=None, **kwargs):
        """Stop tcpdump processing

        :param int pid"
            *OPTIONAL* Stop specific tcpdump. As default will stop all of existing tcpdump
                       processing.

        :param int timeout:
            *OPTIONAL* Stop processing's waiting timeout. Default: 60

        :param bool resolve_ip_and_port:
            *OPTIONAL* As default will not resolve IP and port, but you can set False to transit IP
                       and port to name or protocol name. Default: False

        :param str record_file:
            *OPTIONAL* Read tcpdump's output from given file. Default: "/tmp/tcpdump_record_file"

        :param BOOL get_response:
            *OPTIONAL* Set True to get response that same as return_mode="get_response"

        :return:
            True/False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["pid"] = pid
        options["record_file"] = kwargs.get("record_file", self.default["tcpdump_record_file"])
        options["resolve_ip_and_port"] = self.tool.check_boolean(kwargs.get("resolve_ip_and_port", False))
        options["get_response"] = self.tool.check_boolean(kwargs.get("get_response", True))
        options["timeout"] = int(kwargs.get("timeout", self.default["timeout"]))

        pid_list = []
        if options["pid"] is None:
            response = dev.execute_shell_command_on_device(
                device=device,
                command="/bin/ps aux | /usr/bin/grep tcpdump",
                timeout=options["timeout"]
            )
            device.log(response, level="INFO")
            for line in str(response).splitlines():
                match = re.search(r"\w+\s+(\d+)\s+\d+\.\d+\s+\d+\.\d+\s+", line)
                if not match:
                    continue

                pid_list.append(str(match.group(1)))

            # last one is grep command itself need to delete
            if len(pid_list) >= 1:
                del pid_list[-1]
        else:
            pid_list = [str(options["pid"]), ]

        if not pid_list:
            device.log(message="No TCPDUMP processing need to kill.", level="INFO")
            return True

        all_pid = " ".join(pid_list)
        device.log(message="PID '{}' need to kill".format(all_pid), level="INFO")
        cmd = "/bin/kill -15 {}".format(all_pid)
        dev.execute_shell_command_on_device(device=device, command=cmd, timeout=options["timeout"])

        tcpdump_options = []
        if options["resolve_ip_and_port"] is False:
            tcpdump_options.append("-nn", )

        get_response_cmds = []
        get_response_cmds.append("clear")
        get_response_cmds.append("/usr/sbin/tcpdump -r {} {}".format(
            options["record_file"], " ".join(tcpdump_options)
        ))

        if options["get_response"] is True:
            response = dev.execute_shell_command_on_device(device=device, command=get_response_cmds, timeout=options["timeout"])
            device.log(message="return value: {}".format(response), level="INFO")
            return response

        print("{} return value: True".format(func_name))
        return True

    def create_ftp_connection_between_host(self, device, remote_host, **kwargs):
        """Create FTP connection between 2 host

        This method will create FTP connection by steps:

        1.  checking python interpreter about Python2 or Python3 on device if option "python_interpreter" is "AUTO"
        2.  upload "ftp_client" to client host
        3.  run "ftp_client" on client host

        :param IP remote_host:
            **REQUIRED** Remote host's ipaddress

        :param STR|LIST|TUPLE cmd:
            *OPTIONAL* Operate command list like: ["lcd /var/log", 'put /pub/message']

        :param INT port:
            *OPTIONAL* FTP connection port. Default: 21

        :param BOOL passive_mode:
            *OPTIONAL* True/False to set passive_mode. Default: True

        :param STR username:
            *OPTIONAL* FTP login username. Default: anonymous

                       If username have '\' character, for instance: 'juniper.com\ftp_user' , you should set value arround '', for example:
                       'juniper.com\\ftp_user' in .robot file.

        :param STR password:
            *OPTIONAL* FTP login password. Default: anonymous

        :param INT|STR hold_time:
            *OPTIONAL* Hold FTP session for a while (secs) before terminated. Default: 0

        :param STR scp_upload_username:
            *OPTIONAL* Username to upload ftp_client.py to host. Default: regress

        :param STR scp_upload_password:
            *OPTIONAL* Password to upload ftp_client.py to host. Default: MaRtInI

        :param STR firewall_username:
            *OPTIONAL* For Authentication device testing. Default: None

        :param STR firewall_password:
            *OPTIONAL* For Authentication device testing. Default: None

        :param STR mode:
            *OPTIONAL* As default, FTP connection running in foreground and finished before timeout.
                       If you want do FTP in background, set this option to "Background".
                       Default: "Foreground" and case insensitive

        :param STR logfile:
            *OPTIONAL* Only for mode is "background" to redirect stdout to a file. default: /dev/null

        :param INT|STR timeout:
            *OPTIONAL* FTP transit command timeout. Default: 300

        :param INT|STR ftp_timeout:
            *OPTIONAL* FTP transit processing timeout. Used for FTP server have speed rate need long time to transit. Default: 60

        :param STR python_interpreter:
            *OPTIONAL* One of "python2", "python3", "2", "3", or "auto". default: auto

        :param BOOL no_need_pid:
            *OPTIONAL* Only for mode="Foreground". default: False. As default, if run telnet processing in background mode, it will be return pid or
                       raise RuntimeError if cannot get pid number. If set this option to True, will just return True without pid number

        :param BOOL skip_client_script_upload:
            *OPTIONAL* As default, will upload FTP client script to client host. Set True will not upload this script.
                       default: False

        :return:
            Different success output due to below situations:

            1. if mode is "Foreground" (default action), whole ftp processing output will return
            2. if mode is "Background", return PID number, but cannot get processing output. PID
               number can be used for stop FTP connection

            Any invalid option will raise ValueError or RuntimeError
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options['remote_host'] = remote_host
        options['cmd'] = kwargs.get("cmd", "")
        options["port"] = int(kwargs.get("port", 21))
        options["passive_mode"] = self.tool.check_boolean(kwargs.get("passive_mode", True))
        options["scp_upload_username"] = kwargs.get("scp_upload_username", self.default["regress_username"])
        options["scp_upload_password"] = kwargs.get("scp_upload_username", self.default["regress_password"])
        options["username"] = kwargs.get("username", "anonymous")
        options["password"] = kwargs.get("password", "anonymous")
        options["firewall_username"] = kwargs.get("firewall_username", None)
        options["firewall_password"] = kwargs.get("firewall_password", None)
        options["mode"] = kwargs.get("mode", "FOREGROUND").strip().upper()
        options["logfile"] = kwargs.get("logfile", "/dev/null")
        options["hold_time"] = int(kwargs.get("hold_time", 0))
        options["ftp_timeout"] = int(kwargs.get("ftp_timeout", 60))
        options["timeout"] = int(kwargs.get("timeout", 300))
        options["python_interpreter"] = str(kwargs.get("python_interpreter", "AUTO")).strip().upper()
        options["no_need_pid"] = self.tool.check_boolean(kwargs.get("no_need_pid", False))
        options["skip_client_script_upload"] = self.tool.check_boolean(kwargs.get("skip_client_script_upload", False))

        if isinstance(options["cmd"], str):
            pass
        elif isinstance(options["cmd"], (list, tuple)):
            options["cmd"] = ":".join(options["cmd"])
        else:
            raise ValueError("Keyword 'cmd' must be a STR, LIST or TUPLE, but got '{}'".format(type(options['cmd'])))

        if options["mode"] not in ("FOREGROUND", "BACKGROUND"):
            raise ValueError("'mode' must be one of 'FOREGROUND', 'BACKGROUND' but got '{}'".format(options["mode"]))

        valid_python_interpreter = ("PYTHON2", "PYTHON3", "2", "3", "AUTO")
        if options["python_interpreter"] not in valid_python_interpreter:
            raise ValueError("'python_interpreter' must be one of '{}' but got '{}'".format(valid_python_interpreter, options["python_interpreter"]))

        # Get python interpreter info
        if options["python_interpreter"] == "AUTO":
            try:
                options["python_interpreter"] = self.hidden_info[str(device)]["python_interpreter"]
            except KeyError:
                response = dev.execute_shell_command_on_device(device=device, command="python --version")
                match = re.search(r"python\s+(\d+)\.\d+", response, re.I)
                if match:
                    options["python_interpreter"] = str(match.group(1))
                else:
                    options["python_interpreter"] = "2"

        elif options["python_interpreter"] in ("2", "PYTHON2"):
            options["python_interpreter"] = "2"
        else:
            options["python_interpreter"] = "3"

        if str(device) not in self.hidden_info:
            self.hidden_info[str(device)] = {}
        self.hidden_info[str(device)]["python_interpreter"] = options["python_interpreter"]

        if options["python_interpreter"] == "2":
            with open(self.default["ftp_local_tmp_file"], "w") as fid:
                fid.write(self.default["ftp_script_content"])
        else:
            if self.default["python3_ftp_client_file"] is None:
                raise RuntimeError("cannot find ftp_client.py from toby library.")

            shutil.copy(self.default["python3_ftp_client_file"], self.default["ftp_local_tmp_file"])
            device.log(message="Get ftp_client.py from '{}' complete".format(self.default["python3_ftp_client_file"]), level="INFO")

        # upload FTP client script to src host
        if options["skip_client_script_upload"] is False:
            try:
                result = device.upload(
                    local_file=self.default["ftp_local_tmp_file"],
                    remote_file=self.default["ftp_script_filename"],
                    user=options["scp_upload_username"],
                    password=options["scp_upload_password"],
                    protocol="scp",
                )
            except (Exception, TobyException) as err:
                print("Got error: " + str(err))
                device.log(message=err, level="ERROR")
                result = False
            finally:
                if os.path.exists(self.default["ftp_local_tmp_file"]):
                    os.remove(self.default["ftp_local_tmp_file"])

            if result is False:
                raise RuntimeError("Upload FTP client script failed")

            device.log(message="upload ftp_client.py to remote host complete", level="INFO")

        # from src host to create TELNET connection to dst host
        cmd_element = []
        cmd_element.append("python ~{}/{}".format(options["scp_upload_username"], self.default["ftp_script_filename"]))
        cmd_element.append("-i {}".format(remote_host))
        cmd_element.append("-u {}".format(options["username"]))
        cmd_element.append("-p {}".format(options["password"]))
        cmd_element.append("-t {}".format(options["ftp_timeout"]))

        if options["passive_mode"] is True:
            cmd_element.append("--passive-mode")

        if options["hold_time"] != 0:
            cmd_element.append("--hold-time {}".format(options["hold_time"]))

        cmd_element.append("--port {}".format(options["port"]))

        if options["firewall_username"] is not None and options["firewall_password"] is not None:
            cmd_element.append("--firewall-username {}".format(options["firewall_username"]))
            cmd_element.append("--firewall-password {}".format(options["firewall_password"]))

        cmd_element.append('-c "{}"'.format(options["cmd"]))
        if options["mode"] == "BACKGROUND":
            cmd_element.append("> {} 2>&1 &".format(options["logfile"]))

        cmd = " ".join(cmd_element)
        device.log(message="send cmd: {}".format(cmd), level="INFO")
        result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)

        if options["mode"] == "BACKGROUND":
            if options["no_need_pid"] is True:
                result = True
            else:
                # get pid from command result
                pid = ""
                match = re.search(r"\[\d+\]\s+(\d+)", result)
                if match:
                    pid = match.group(1)

                # if cannot get pid from command result
                if not pid.isdigit():
                    pid = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="echo $!")

                # if cannot get pid from command result and last background variable
                if not pid.isdigit():
                    raise RuntimeError("Cannot find FTP BACKGROUND PID number")

                result = int(pid)

        device.log(message="{} return value: {}".format(func_name, result))
        return result

    def close_ftp_connection_between_host(self, device, **kwargs):
        """Close FTP connection between host

        :param int/all pid:
            *OPTIONAL* PID for FTP connection. Default: None

        :param int signal:
            *OPTIONAL* Should be 9 (force kill) or 15 (terminate) but you can give other number for /bin/kill. Default: 15

        :param int timeout:
            *OPTIONAL* Stop FTP connection timeout. Default: 120

        :return:
            Any method invoke issue will return False, otherwise always return True.
            **CAUTION:** Even PID is wrong or not killed, still retrun True
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["pid"] = kwargs.get("pid", None)
        options["signal"] = kwargs.get("signal", 15)
        options["timeout"] = kwargs.get("timeout", 120)

        if options["pid"] is None:
            all_pid_list = []
            lines = dev.execute_shell_command_on_device(
                device=device,
                timeout=options["timeout"],
                command="/bin/ps aux | /usr/bin/grep ftp_client.py"
            )
            device.log(lines, level="INFO")

            for line in lines.splitlines():
                match = re.match(r"^\w+\s+(\d+)\s+.*ftp_client.py\s+\S+", line.strip())
                if match:
                    all_pid_list.append(match.group(1))

            if all_pid_list:
                device.log(message="kill pid: {}".format(all_pid_list), level="INFO")
                dev.execute_shell_command_on_device(
                    device=device,
                    command="/bin/kill -{} {}".format(options["signal"], " ".join(all_pid_list)),
                    timeout=options["timeout"],
                )

        else:
            dev.execute_shell_command_on_device(
                device=device,
                command="/bin/kill -{} {}".format(options["signal"], options["pid"]),
                timeout=options["timeout"],
            )

        return True

    def create_telnet_connection_between_host(self, device, remote_host, **kwargs):
        """Create TELNET session between 2 hosts

        This method do the step as below:

        1. Upload utils/telnet_client.py file to source host. Because need upload file, must given host handler, not IP address

        2. According to mode to start telnet connection in foreground or background. Because need create telnet connection in testing
           topo (not manage topo), destination host address must be IP address, not handler.

        3. return result

        If want create telnet session on DUT but do not interested telnet result between 2 hosts, you should invoke this method like:
            self.create_telnet_session_between_host(
                device=$h0,
                remote_host= "192.168.1.2",
                mode="Background",                  <=== will not block rest sentence to show DUT session, but cannot get telnet output
                hold_time=20,                       <=== hold 20 secs to let telnet session alive
            )
        If want run telnet command on dst host, and get command output, invoke this method like:
            self.create_telnet_session_between_host(
                device=$h0,
                remote_host= "192.168.1.2",
                mode="Foreground",                  <=== block rest sentence and waiting for telnet session close
                hold_time=0,                        <=== don't hold telnet connection
            )

        :param IPADDR remote_host:
            **REQUIRED** Destination host's IP address

        :param INT hold_time:
            *OPTIONAL* As default, telnet session created and close in short time, but you can set this option to hold session for a while. Default: 0

        :param STR username:
            *OPTIONAL* Please avoide 'root' user because telnet server denied as default. Default: regress

        :param STR password:
            *OPTIONAL* Default: MaRtInI

        :param STR|INT port:
            *OPTIONAL* default: 23

        :param STR cmd:
            *OPTIONAL* Command string to run command on dst host. You can give more commands that separated by comma (,). Default: ""

            Example:

                cmd="ls -l, du -sh, ifconfig"

        :param STR scp_upload_username:
            *OPTIONAL* Username for upload telnet_client script to host. Default: same as option "username"

        :param STR scp_upload_password:
            *OPTIONAL* Password for upload telnet_client script to host. Default: same as option "password"

        :param STR firewall_username:
            *OPTIONAL* For Authentication device testing. Default: None

        :param STR firewall_password:
            *OPTIONAL* For Authentication device testing. Default: None

        :param STR mode:
            *OPTIONAL* Do telnet in "foreground" or "background". Default: "background"

        :param STR logfile:
            *OPTIONAL* Only for mode is "background" to redirect stdout to a file. default: /dev/null

        :param INT telnet_timeout:
            *OPTIONAL* Timeout telnet interact. Default: 60

        :param INT timeout:
            *OPTIONAL* Timeout to send command to foreign host. Default: 180

        :param STR python_interpreter:
            *OPTIONAL* One of "python2", "python3", "2", "3", or "auto". default: auto

        :param BOOL to_srx_device:
            *OPTIONAL* Used for do telnet from HOST to SRX device. default: False

        :param BOOL no_need_pid:
            *OPTIONAL* Only for mode="Foreground". default: False. As default, if run telnet processing in background mode, it will be return pid or
                       raise RuntimeError if cannot get pid number. If set this option to True, will just return True without pid number

        :param BOOL skip_client_script_upload:
            *OPTIONAL* As default, will upload FTP client script to client host. Set True will not upload this script.
                       default: False

        :return:
            If mode is "Foreground", return all output during telnet session.
            If mode is "Background", return pid for background job

            Any issue return False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["remote_host"] = remote_host
        options["port"] = int(kwargs.get("port", 23))
        options["hold_time"] = int(kwargs.get("hold_time", 0))
        options["mode"] = kwargs.get("mode", "BACKGROUND").strip().upper()
        options["logfile"] = kwargs.get("logfile", "/dev/null")
        options["username"] = kwargs.get("username", self.default["regress_username"])
        options["password"] = kwargs.get("password", self.default["regress_password"])
        options["cmd"] = kwargs.get("cmd", "")
        options["scp_upload_username"] = kwargs.get("scp_upload_username", options["username"])
        options["scp_upload_password"] = kwargs.get("scp_upload_password", options["password"])
        options["firewall_username"] = kwargs.get("firewall_username", None)
        options["firewall_password"] = kwargs.get("firewall_password", None)
        options["telnet_timeout"] = int(kwargs.get("telnet_timeout", 60))
        options["timeout"] = int(kwargs.get("timeout", 180))
        options["python_interpreter"] = str(kwargs.get("python_interpreter", "AUTO")).strip().upper()
        options["to_srx_device"] = self.tool.check_boolean(kwargs.get("to_srx_device", False))
        options["no_need_pid"] = self.tool.check_boolean(kwargs.get("no_need_pid", False))
        options["skip_client_script_upload"] = self.tool.check_boolean(kwargs.get("skip_client_script_upload", False))

        if isinstance(options["cmd"], str):
            pass
        elif isinstance(options["cmd"], (list, tuple)):
            options["cmd"] = ":".join(options["cmd"])
        else:
            raise ValueError("Keyword 'cmd' must be a STR, LIST or TUPLE, but got '{}'".format(type(options['cmd'])))

        if options["mode"] not in ("FOREGROUND", "BACKGROUND"):
            raise ValueError("'mode' must be one of 'FOREGROUND', 'BACKGROUND' but got '{}'".format(options["mode"]))

        valid_python_interpreter = ("PYTHON2", "PYTHON3", "2", "3", "AUTO")
        if options["python_interpreter"] not in valid_python_interpreter:
            raise ValueError("'python_interpreter' must be one of '{}' but got '{}'".format(valid_python_interpreter, options["python_interpreter"]))

        # Get python interpreter info
        if options["python_interpreter"] == "AUTO":
            try:
                options["python_interpreter"] = self.hidden_info[str(device)]["python_interpreter"]
            except KeyError:
                response = dev.execute_shell_command_on_device(device=device, command="python --version")
                match = re.search(r"python\s+(\d+)\.\d+", response, re.I)
                if match:
                    options["python_interpreter"] = str(match.group(1))
                else:
                    options["python_interpreter"] = "2"

        elif options["python_interpreter"] in ("2", "PYTHON2"):
            options["python_interpreter"] = "2"
        else:
            options["python_interpreter"] = "3"

        if str(device) not in self.hidden_info:
            self.hidden_info[str(device)] = {}
        self.hidden_info[str(device)]["python_interpreter"] = options["python_interpreter"]

        if options["python_interpreter"] == "2":
            with open(self.default["telnet_local_tmp_file"], "w") as fid:
                fid.write(self.default["telnet_script_content"])
        else:
            if self.default["python3_telnet_client_file"] is None:
                raise RuntimeError("cannot find telnet_client.py from toby library.")

            shutil.copy(self.default["python3_telnet_client_file"], self.default["telnet_local_tmp_file"])
            device.log(message="Get telnet_client.py from '{}' complete".format(self.default["python3_telnet_client_file"]), level="INFO")
        # upload TELNET client script to src host
        if options["skip_client_script_upload"] is False:
            try:
                result = device.upload(
                    local_file=self.default["telnet_local_tmp_file"],
                    remote_file=self.default["telnet_script_filename"],
                    user=options["scp_upload_username"],
                    password=options["scp_upload_password"],
                    protocol="scp",
                )
            except (Exception, TobyException):
                result = False

            finally:
                if os.path.exists(self.default["telnet_local_tmp_file"]):
                    os.remove(self.default["telnet_local_tmp_file"])

            if result is False:
                raise RuntimeError("Upload TELNET client script failed")

            device.log(message="upload telnet_client.py to remote host complete", level="INFO")

        # from src host to create TELNET connection to dst host
        cmd_element = []
        cmd_element.append("python ~{}/{}".format(options["scp_upload_username"], self.default["telnet_script_filename"]))
        cmd_element.append("-i {}".format(options["remote_host"]))
        cmd_element.append("-u {}".format(options["username"]))
        cmd_element.append("-p {}".format(options["password"]))
        cmd_element.append("-t {}".format(options["telnet_timeout"]))

        if options["cmd"]:
            cmd_element.append('-c "{}"'.format(options["cmd"]))

        cmd_element.append("--port {}".format(options["port"]))
        cmd_element.append("--hold-time {}".format(options["hold_time"]))

        if options["firewall_username"] is not None:
            cmd_element.append("--firewall-username {}".format(options["firewall_username"]))

        if options["firewall_username"] is not None:
            cmd_element.append("--firewall-password {}".format(options["firewall_password"]))

        if options["to_srx_device"] is True:
            cmd_element.append("--to-srx-device")

        if options["mode"] == "BACKGROUND":
            cmd_element.append("> {} 2>&1 &".format(options["logfile"]))

        cmd = " ".join(cmd_element)
        device.log(message="send cmd: {}".format(cmd), level="INFO")
        result = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command=cmd)

        if options["mode"] == "BACKGROUND":
            if options["no_need_pid"] is True:
                result = True
            else:
                # get pid from command result
                pid = ""
                match = re.search(r"\[\d+\]\s+(\d+)", result)
                if match:
                    pid = match.group(1)

                # if cannot get pid from command result
                if not pid.isdigit():
                    pid = dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="echo $!")

                # if cannot get pid from command result and last background variable
                if not pid.isdigit():
                    raise RuntimeError("Cannot find TELNET BACKGROUND PID number")

                result = int(pid)

        device.log(message="{} return value: {}".format(func_name, result), level="INFO")
        return result

    def close_telnet_connection_between_host(self, device, **kwargs):
        """Kill telnet connection

        As default, this method will get all telnet related processing and kill them all, but you can give a pid number to kill specific one

        :param int pid:
            *OPTIONAL* pid number. Default: None

        :param int timeout:
            *OPTIONAL* kill processing's timeout. Default: 180

        :return:
            True/False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["pid"] = kwargs.get("pid", None)
        options["timeout"] = kwargs.get("timeout", 180)

        pid_list = []
        if options["pid"] is None:
            result = dev.execute_shell_command_on_device(
                device=device,
                timeout=options["timeout"],
                command="/bin/ps aux | /usr/bin/grep telnet_client.py"
            )
            for line in result.splitlines():
                match = re.search(r"\w+\s+(\d+)\s+\d+\.\d+\s+\d+\.\d+\s+", line)
                if not match:
                    continue

                pid_list.append(match.group(1))

            # last one is grep command itself need to delete
            if len(pid_list) >= 1:
                del pid_list[-1]
        else:
            pid_list.append(str(options["pid"]))

        if not pid_list:
            device.log(message="No TELNET connection need to kill.", level="INFO")
            return True

        device.log(message="PID '{}' need to kill".format(pid_list), level="INFO")
        dev.execute_shell_command_on_device(device=device, timeout=options["timeout"], command="/bin/kill -9 {}".format(" ".join(pid_list)))
        return True

    def sendip_source_ip_increase(self, device, **kwargs):
        """Generate sendip script and send

        linux_tool.sendip source ip increase    device=${h0}    ip_option=ipv6    src_ip=2000::2    dst_ip=2000:1::2
        ...    src_port=1    dst_port=1    total_count=6    port_count=3    re_send_time=1    ip_count=2
        ...    delete_file=no    file_name=sendip_script_v6.sh

        :param Device device:
            **REQUIRED** Handle of the device on which commands have to be executed.

        :param str file_name:
            *OPTIONAL* file_name parameter. Default: sendip_script.sh.

        :param str size:
            *OPTIONAL* size parameter. Default: r32. Could be r32 or r64 and etc.

        :param str ip_option:
            *OPTIONAL* ip_option parameter. Default: ipv4. Could be ipv4 or ipv6

        :param str src_ip:
            **REQUIRED** src_ip parameter. Default: none. Could be any IPv4 or IPv6 IP address.
            IPv4 IP address max is x.255.255.255.
            IPv6 IP address, the hex number after last ":" will be increase, max is ffff.

        :param str dst_ip:
            **REQUIRED** dst_ip parameter. Default: none. Could be any IPv4 or IPv6 IP address.

        :param str src_port:
            *OPTIONAL* src_port parameter. Default: none. Could be any number in (0-65535)

        :param str dst_port:
            *OPTIONAL* dst_port parameter. Default: none. Could be any number in (0-65535)

        :param str protocol:
            *OPTIONAL* protocol parameter. Default: udp. Could be udp or tcp or icmp.

        :param str args_option:
            *OPTIONAL* args_option parameter. Default: none. Could be any info plus at the end of sendip

        :param int total_count:
            *OPTIONAL* total_count number. Default: 1. Could be any number

        :param int re_send_time:
            *OPTIONAL* re_send_time number. Default: 0. Could be any number

        :param int ip_count:
            *OPTIONAL* ip_count number. Default: 1. Source IP address increase count, could be any number.

        :param int port_count:
            *OPTIONAL* port_count number. Default: 1. Source port increase count, could be any number.

        :param str delete_file:
            *OPTIONAL* delete_file parameter. Default: yes. Could be yes or no.

        :param int timeout:
            *OPTIONAL* Execuse command timeout time. Default: 1200

        :param str type_option:
            *OPTIONAL* type_option parameter. Default: source_ip_increase.
            Should be one of "source_ip_increase" and "source_destination_ip_increase_both".

        :return:
            True/False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        # all_option_list = (
        #     "file_name", "size", "ip_option", "src_ip", "dst_ip", "src_port", "dst_port", "protocol", "args_option",
        #     "total_count", "re_send_time", "ip_count", "port_count", "delete_file", "timeout", "type_option",
        # )
        options = {}

        options["file_name"] = kwargs.get("file_name", "sendip_script.sh")
        options["size"] = kwargs.get("size", "r32")
        options["ip_option"] = kwargs.get("ip_option", "ipv4")
        options["protocol"] = kwargs.get("protocol", "udp")
        options["src_ip"] = kwargs.get("src_ip", None)
        options["dst_ip"] = kwargs.get("dst_ip", None)
        options["src_port"] = kwargs.get("src_port", 1)
        options["dst_port"] = kwargs.get("dst_port", 1)
        options["total_count"] = kwargs.get("total_count", 1)
        options["re_send_time"] = kwargs.get("re_send_time", 0)
        options["ip_count"] = kwargs.get("ip_count", 1)
        options["port_count"] = kwargs.get("port_count", 1)
        options["args_option"] = kwargs.get("args_option", "")
        options["delete_file"] = kwargs.get("delete_file", "yes")
        options["timeout"] = kwargs.get("timeout", 1200)
        options["type_option"] = kwargs.get("type_option", "source_ip_increase")

        if options['ip_option'] == "ipv4":
            src_ip_prefix1 = re.findall(r"(\d+)\.\d+\.\d+\.\d+", options['src_ip'], re.I)
            src_ip_prefix2 = re.findall(r"\d+\.(\d+)\.\d+\.\d+", options['src_ip'], re.I)
            src_ip_prefix3 = re.findall(r"\d+\.\d+\.(\d+)\.\d+", options['src_ip'], re.I)
            src_ip_last = re.findall(r"\d+\.\d+\.\d+\.(\d+)", options['src_ip'], re.I)
            src_ip_prefix1 = int(src_ip_prefix1[0])
            src_ip_prefix2 = int(src_ip_prefix2[0])
            src_ip_prefix3 = int(src_ip_prefix3[0])
            src_ip_last = int(src_ip_last[0])
            dst_ip_prefix1 = re.findall(r"(\d+)\.\d+\.\d+\.\d+", options['dst_ip'], re.I)
            dst_ip_prefix2 = re.findall(r"\d+\.(\d+)\.\d+\.\d+", options['dst_ip'], re.I)
            dst_ip_prefix3 = re.findall(r"\d+\.\d+\.(\d+)\.\d+", options['dst_ip'], re.I)
            dst_ip_last = re.findall(r"\d+\.\d+\.\d+\.(\d+)", options['dst_ip'], re.I)
            dst_ip_prefix1 = int(dst_ip_prefix1[0])
            dst_ip_prefix2 = int(dst_ip_prefix2[0])
            dst_ip_prefix3 = int(dst_ip_prefix3[0])
            dst_ip_last = int(dst_ip_last[0])
        else:
            src_ip_content = re.findall(r":([A-Za-z0-9]+)", options['src_ip'], re.I)
            src_ip_last = str(src_ip_content[-1])
            src_ip_prefix = re.findall(r"(.*){}".format(src_ip_last), options['src_ip'], re.I)
            src_ip_prefix = str(src_ip_prefix[0])
            src_ip_hex = ("0x{}".format(src_ip_last))
            device.log(message="mix IPv6 src address = {}{}".format(src_ip_prefix, src_ip_last), level="INFO")
            device.log(message="src_ip = {}".format(src_ip_last), level="INFO")
            dst_ip_content = re.findall(r":([A-Za-z0-9]+)", options['dst_ip'], re.I)
            dst_ip_last = str(dst_ip_content[-1])
            dst_ip_prefix = re.findall(r"(.*){}".format(dst_ip_last), options['dst_ip'], re.I)
            dst_ip_prefix = str(dst_ip_prefix[0])
            dst_ip_hex = ("0x{}".format(dst_ip_last))
            device.log(message="mix IPv6 dst address = {}{}".format(dst_ip_prefix, dst_ip_last), level="INFO")
            device.log(message="dst_ip = {}".format(dst_ip_last), level="INFO")


        if options['protocol'] == "udp":
            variable = "-us $src_port -ud $dst_port"
        elif options['protocol'] == "tcp":
            variable = "-ts $src_port -td $dst_port"
        else:
            variable = ""


        if options['ip_option'] == "ipv4":
            if options['type_option'] == "source_ip_increase":
                sendip_script = """
                #!/bin/sh
                src_port={sport}
                dst_port={dport}
                src_pre_ip1={src_ip1}
                src_pre_ip2={src_ip2}
                src_pre_ip3={src_ip3}
                src_pre_ip4={src_ip4}
                send_count={count}
                b=1
                for ((i=0;i<{ip_count};i++))
                 do
                 src_port={sport}
                 dst_port={dport}
                 for ((a=0;a<{port_count};a++))
                 do
                  sendip -d {size} -p {ip_option} -is $src_pre_ip1.$src_pre_ip2.$src_pre_ip3.$src_pre_ip4 -id {dip} -p {pro} {var} {opt} {dip}
                  src_port=`expr $src_port + 1`
                  dst_port=`expr $dst_port + 1`
                  if [ $src_pre_ip4 -eq 255 ]
                   then
                   src_pre_ip3=`expr $src_pre_ip3 + 1`
                   src_pre_ip4=0
                  fi
                  if ([ $src_pre_ip3 -eq 255 ] && [ $src_pre_ip4 -eq 255 ])
                   then
                   src_pre_ip2=`expr $src_pre_ip2 + 1`
                   src_pre_ip3=0
                   src_pre_ip4=0
                  fi
                  if [ $b -eq $send_count ]
                   then
                   break 7
                  fi
                  if [ $src_pre_ip2 -eq 255 ]
                   then
                   break 7
                  fi
                  b=`expr $b + 1`
                 done
                 src_pre_ip4=`expr $src_pre_ip4 + 1`
                done
                """.format(sport=options['src_port'], dport=options['dst_port'], ip_count=options['ip_count'], port_count=options['port_count'],
                           size=options['size'], ip_option=options['ip_option'], var=variable, opt=options["args_option"], src_ip1=src_ip_prefix1,
                           src_ip2=src_ip_prefix2, src_ip3=src_ip_prefix3, src_ip4=src_ip_last, count=options['total_count'], dip=options['dst_ip'],
                           pro=options['protocol'])
            elif options['type_option'] == "source_destination_ip_increase_both":
                sendip_script = """
                #!/bin/sh
                src_port={sport}
                dst_port={dport}
                src_pre_ip1={src_ip1}
                src_pre_ip2={src_ip2}
                src_pre_ip3={src_ip3}
                src_pre_ip4={src_ip4}
                dst_pre_ip1={dst_ip1}
                dst_pre_ip2={dst_ip2}
                dst_pre_ip3={dst_ip3}
                dst_pre_ip4={dst_ip4}
                send_count={count}
                b=1
                for ((i=0;i<{ip_count};i++))
                 do
                 src_port={sport}
                 dst_port={dport}
                 for ((a=0;a<{port_count};a++))
                 do
                  sendip -d {size} -p {ip_option} -is $src_pre_ip1.$src_pre_ip2.$src_pre_ip3.$src_pre_ip4 -id $dst_pre_ip1.$dst_pre_ip2.$dst_pre_ip3.$dst_pre_ip4 -p {pro} {var} {opt} $dst_pre_ip1.$dst_pre_ip2.$dst_pre_ip3.$dst_pre_ip4
                  src_port=`expr $src_port + 1`
                  dst_port=`expr $dst_port + 1`
                  if [ $src_pre_ip4 -eq 255 ]
                   then
                   src_pre_ip3=`expr $src_pre_ip3 + 1`
                   src_pre_ip4=0
                  fi
                  if ([ $src_pre_ip3 -eq 255 ] && [ $src_pre_ip4 -eq 255 ])
                   then
                   src_pre_ip2=`expr $src_pre_ip2 + 1`
                   src_pre_ip3=0
                   src_pre_ip4=0
                  fi
                  if [ $dst_pre_ip4 -eq 255 ]
                   then
                   dst_pre_ip3=`expr $dst_pre_ip3 + 1`
                   dst_pre_ip4=0
                  fi
                  if ([ $dst_pre_ip3 -eq 255 ] && [ $dst_pre_ip4 -eq 255 ])
                   then
                   dst_pre_ip2=`expr $dst_pre_ip2 + 1`
                   dst_pre_ip3=0
                   dst_pre_ip4=0
                  fi
                  if [ $b -eq $send_count ]
                   then
                   break 7
                  fi
                  if ([ $src_pre_ip2 -eq 255 ]&&[ $src_pre_ip3 -eq 255 ] && [ $src_pre_ip4 -eq 255 ])
                   then
                   break 7
                  fi
                  if ([ $dst_pre_ip2 -eq 255 ]&&[ $dst_pre_ip3 -eq 255 ] && [ $dst_pre_ip4 -eq 255 ])
                   then
                   break 7
                  fi
                  b=`expr $b + 1`
                 done
                 src_pre_ip4=`expr $src_pre_ip4 + 1`
                 dst_pre_ip4=`expr $dst_pre_ip4 + 1`
                done
                """.format(sport=options['src_port'], dport=options['dst_port'], ip_count=options['ip_count'], port_count=options['port_count'],
                           size=options['size'], ip_option=options['ip_option'], var=variable, opt=options["args_option"],
                           src_ip1=src_ip_prefix1, src_ip2=src_ip_prefix2, src_ip3=src_ip_prefix3, src_ip4=src_ip_last, count=options['total_count'],
                           dst_ip1=dst_ip_prefix1, dst_ip2=dst_ip_prefix2, dst_ip3=dst_ip_prefix3, dst_ip4=dst_ip_last, pro=options['protocol'])

        if options['ip_option'] == "ipv6":
            if options['type_option'] == "source_ip_increase":
                sendip_script = """
                #!/bin/sh
                src_port={sport}
                dst_port={dport}
                src_pre_ip={src_ip_prefix}
                src_ip={src_ip_last}
                src_ip_hex={src_ip_hex}
                send_count={count}
                b=1
                src_ip_int=$((16#$src_ip))
                for ((i=0;i<{ip_count};i++))
                 do
                 src_port={sport}
                 dst_port={dport}
                 src_ip_increase=$((10#$src_ip_int))
                 for ((a=0;a<{port_count};a++))
                 do
                  sendip -d {size} -p {ip_option} -6s $src_pre_ip$src_ip_increase -6d {dip} -p {pro} {var} {opt} {dip}
                  src_port=`expr $src_port + 1`
                  dst_port=`expr $dst_port + 1`
                  if [ $b -eq $send_count ]
                   then
                   break 7
                  fi
                  b=`expr $b + 1`
                 done
                 if [ $src_ip_int -eq 65535 ]
                   then
                   break 7
                 fi
                 src_ip_int=`expr $src_ip_int + 1`
                done
                """.format(sport=options['src_port'], dport=options['dst_port'], ip_count=options['ip_count'], port_count=options['port_count'],
                           size=options['size'], ip_option=options['ip_option'], var=variable, opt=options["args_option"],
                           src_ip_prefix=src_ip_prefix, src_ip_last=src_ip_last, src_ip_hex=src_ip_hex, count=options['total_count'],
                           dip=options['dst_ip'], pro=options['protocol'])

            elif options['type_option'] == "source_destination_ip_increase_both":
                sendip_script = """
                #!/bin/sh
                src_port={sport}
                dst_port={dport}
                src_pre_ip={src_ip_prefix}
                src_ip={src_ip_last}
                src_ip_hex={src_ip_hex}
                dst_pre_ip={dst_ip_prefix}
                dst_ip={dst_ip_last}
                dst_ip_hex={dst_ip_hex}
                send_count={count}
                b=1
                src_ip_int=$((16#$src_ip))
                dst_ip_int=$((16#$dst_ip))
                for ((i=0;i<{ip_count};i++))
                 do
                 src_port={sport}
                 dst_port={dport}
                 src_ip_increase=$((10#$src_ip_int))
                 dst_ip_increase=$((10#$dst_ip_int))
                 for ((a=0;a<{port_count};a++))
                 do
                  sendip -d {size} -p {ip_option}  -6s $src_pre_ip$src_ip_increase -6d $dst_pre_ip$dst_ip_increase -p {pro} {var} {opt} $dst_pre_ip$dst_ip_increase
                  src_port=`expr $src_port + 1`
                  dst_port=`expr $dst_port + 1`
                  if [ $b -eq $send_count ]
                   then
                   break 7
                  fi
                  b=`expr $b + 1`
                 done
                 if ([ $src_ip_int -eq 65535 ]|| [ $dst_ip_int -eq 65535 ])
                   then
                   break 7
                 fi
                 src_ip_int=`expr $src_ip_int + 1`
                 dst_ip_int=`expr $dst_ip_int + 1`
                done
                """.format(sport=options['src_port'], dport=options['dst_port'], ip_count=options['ip_count'], port_count=options['port_count'],
                           size=options['size'], ip_option=options['ip_option'], var=variable, opt=options["args_option"],
                           src_ip_prefix=src_ip_prefix, src_ip_last=src_ip_last, src_ip_hex=src_ip_hex, count=options['total_count'],
                           dst_ip_prefix=dst_ip_prefix, dst_ip_last=dst_ip_last, dst_ip_hex=dst_ip_hex, pro=options['protocol'])



        dev.execute_shell_command_on_device(device=device, command="rm -rf /root/{}".format(options['file_name']), timeout=options["timeout"])

        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="echo '{}' > /root/{}".format(sendip_script, options['file_name'])
        )


        dev.execute_shell_command_on_device(
            device=device,
            timeout=options["timeout"],
            command="chmod 755 /root/{}".format(options['file_name'])
        )
        if isinstance(options['re_send_time'], str):
            options['re_send_time'] = int(options['re_send_time'])
        send = options['re_send_time']+1
        for _ in range(0, send):
            dev.execute_shell_command_on_device(
                device=device,
                timeout=options["timeout"],
                command="/root/{}".format(options['file_name'])
            )

        if options['delete_file'] == "yes":
            dev.execute_shell_command_on_device(
                device=device, command="rm -rf /root/{}".format(options['file_name']), timeout=options["timeout"]
            )

        return True

    def send_packet_by_pktgen(self, device, dst_mac, interface="eth1", **kwargs):
        """Send UDP packet by pktgen

        A UDP packet traffic generator in kernel space for testing network throughput. This method only well tested on CentOS 7.

        For more detail, see: https://www.kernel.org/doc/Documentation/networking/pktgen.txt

        :param MAC dst_mac:
            **REQUIRED** Destination MAC Address such as 00:00:00:00:00:01

        :param STR interface:
            *OPTIONAL* Interface name such as eth1, em1, etc... packet will be sent from this interface. default: eth1

        :param IP dst:
            *OPTIONAL* Permanent destination IPv4 (not for IPv6) address. default: 127.0.0.1

        :param INT count:
            *OPTIONAL* How many packets want to send. 0 means send consistently. default: 10

        :param INT delay:
            *OPTIONAL* Packet send interval. Unit: nanosecond. 1,000,000,000 ns == 1s. default: 1000000000 (1 packet/s)

        :param INT pkt_size:
            *OPTIONAL* Consistent packet size. Unit: byte. pkt_size=46 means all packets' size are 50bytes (46 bytes + 4 CRC bytes). default: None

        :param INT min_pkt_size/max_pkt_size:
            *OPTIONAL* Range of random packet size. Unit: byte. min_pkt_size=46 and max_pkt_size=1472 means packet size randomly between 46 and 1472
                       default: None

        :param INT frags:
            *OPTIONAL* Normally working with option "pkt_size". Split packet in frags. e.g: pkt_size=3000 and frags=5 means split every packet in 5
                       frags that every packet length is 600bytes. default: None

        :param INT udp_src_min/udp_src_max:
            *OPTIONAL* Range of UDP packet source port. udp_src_min=1024 and udp_src_max=2000 means packet src_port is randomly between 1024 and 2000
                       defalt: 7 (echo)

        :param INT udp_dst_min/udp_dst_max:
            *OPTIONAL* Range of UDP packet destination port. default: 7 (echo)

        :param IP src:
            *OPTIONAL* Permanent source IPv4 (not for IPv6) address. default: interface first address

        :param IP src_min/src_max:
            *OPTIONAL* Range of random source IP address (not for IPv6). default: None

        :param IP dst_min/dst_max:
            *OPTIONAL* Range of random destination IP address (not for IPv6). default: None

        :param IP src6/dst6_min/dst6_max:
            *OPTIONAL* Like src/dst for IPv4, src6 is for IPv6. There is no dst6, but you can set dst6_min and dst6_max for random or permentent
                       address. default: None

        :param MAC src_mac:
            *OPTIONAL* Source MAC address

        :param INT rate:
            *OPTIONAL* Traffic throughput. Unit: bits/s (not bytes). default: 0. set "1,000,000,000" means 1Gb

            We have 3 solutions to control traffic rate:

            1. set "pkt_size" and "delay": it continuous send packets but packet interval controlled by "delay". it is useful for backgroud traffic.
            2. set "rate" only: send packet in burst, then wait until next second.
            3. set "ratep" only: set PPS similar with "pkt_size" and "delay".

        :param INT ratep:
            *OPTIONAL* PPS number. Unit: packet count per second. 10000 means 10000 packets/s

        :param STR mode:
            *OPTIONAL* Running mode of "foreground" or "background". If option "count=0", mode will be "background".  default: foreground

        :return:
            Return True if packet send success, otherwise return False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["dst_mac"] = dst_mac
        options["interface"] = interface
        options["dst"] = kwargs.pop("dst", "127.0.0.1")
        options["count"] = int(kwargs.pop("count", 10))
        options["delay"] = kwargs.pop("delay", 1000000000)
        options["pkt_size"] = kwargs.pop("pkt_size", None)
        options["min_pkt_size"] = kwargs.pop("min_pkt_size", None)
        options["max_pkt_size"] = kwargs.pop("max_pkt_size", None)
        options["frags"] = kwargs.pop("frags", None)
        options["udp_src_min"] = kwargs.pop("udp_src_min", 7)
        options["udp_src_max"] = kwargs.pop("udp_src_max", 7)
        options["udp_dst_min"] = kwargs.pop("udp_dst_min", 7)
        options["udp_dst_max"] = kwargs.pop("udp_dst_max", 7)
        options["src"] = kwargs.pop("src", None)
        options["src_min"] = kwargs.pop("src_min", None)
        options["src_max"] = kwargs.pop("src_max", None)
        options["dst_min"] = kwargs.pop("dst_min", None)
        options["dst_max"] = kwargs.pop("dst_max", None)
        options["src6"] = kwargs.pop("src6", None)
        options["dst6_min"] = kwargs.pop("dst6_min", None)
        options["dst6_max"] = kwargs.pop("dst6_max", None)
        options["src_mac"] = kwargs.pop("src_mac", None)
        options["rate"] = kwargs.pop("rate", None)
        options["ratep"] = kwargs.pop("ratep", None)
        options["mode"] = str(kwargs.pop("mode", "foreground")).upper()

        if options["count"] == 0:
            options["mode"] = "background".upper()

        path = {}
        path["pktgen_folder"] = "/proc/net/pktgen"
        path["pktgen_process"] = os.path.join(path["pktgen_folder"], "kpktgend_0")
        path["pktgen_ctrl"] = os.path.join(path["pktgen_folder"], "pgctrl")


        def write_cmd(cmds, dst_dev=path["pktgen_ctrl"], mode="FOREGROUND"):
            """write command to dst device"""
            if not isinstance(cmds, (list, tuple)):
                cmds = [cmds, ]

            for cmd in cmds:
                cmd = """/bin/echo "{}" > {}""".format(cmd, dst_dev)
                if mode == "BACKGROUND":
                    cmd += " &"

                device.log(message="send cmd: {}".format(cmd), level="INFO")
                response = dev.execute_shell_command_on_device(device=device, command=cmd)

            return response

        load_response = dev.execute_shell_command_on_device(device=device, command="modprobe pktgen")
        response = dev.execute_shell_command_on_device(device=device, command="lsmod | /bin/grep -i pktgen")
        if not re.search(r"pktgen\s+\d+", response):
            device.log(message="cannot load pktgen module to kernal. error msg:\n{}".format(load_response), level="ERROR")
            return False

        response = dev.execute_shell_command_on_device(device=device, command="/bin/ls -l {}".format(path["pktgen_folder"]))
        if not re.search(r"kpktgend_0", response) or not re.search(r"pgctrl", response):
            device.log(message="load pktgen component to kernal failed", level="ERROR")
            return False

        write_cmd(cmds="reset", dst_dev=path["pktgen_ctrl"])
        write_cmd(cmds="add_device {}".format(options["interface"]), dst_dev=path["pktgen_process"])
        response = dev.execute_shell_command_on_device(device=device, command="""/bin/ls -l {}""".format(path["pktgen_folder"]))
        if not re.search(options["interface"], response):
            device.log(message="add interface '{}' to pktgen kernal failed".format(options["interface"]), level="ERROR")
            return False

        # pktgen configuration.
        conf_keyword_list = list(options.keys())
        conf_keyword_list.remove("interface")
        conf_keyword_list.remove("mode")

        cmds = []
        for keyword in conf_keyword_list:
            if options[keyword] is not None:
                cmds.append("{} {}".format(keyword, options[keyword]))

        if options["src_min"] is not None and options["src_max"] is not None:
            cmds.append("flag IPSRC_RND")

        if options["dst_min"] is not None and options["dst_max"] is not None:
            cmds.append("flag IPDST_RND")

        if options["dst6_min"] is not None and options["dst6_max"] is not None:
            cmds.append("flag IPDST_RND")

        if options["udp_src_min"] is not None and options["udp_src_max"] is not None and options["udp_src_min"] != options["udp_src_max"]:
            cmds.append("flag UDPSRC_RND")

        if options["udp_dst_min"] is not None and options["udp_dst_max"] is not None and options["udp_dst_min"] != options["udp_dst_max"]:
            cmds.append("flag UDPDST_RND")

        if options["min_pkt_size"] is not None and options["max_pkt_size"] is not None and options["min_pkt_size"] != options["max_pkt_size"]:
            cmds.append("flag TXSIZE_RND")

        interface_path = os.path.join(path["pktgen_folder"], options["interface"])
        device.log(message="pktgen configuration cmds:\n{}".format(self.tool.pprint(cmds)), level="INFO")
        response = write_cmd(cmds=cmds, dst_dev=interface_path)

        response = dev.execute_shell_command_on_device(device=device, command="cat {}".format(interface_path))
        device.log(message="pktgen configuration:\n{}".format(response), level="INFO")

        device.log(message="pktgen send package starting...", level="INFO")
        response = write_cmd(cmds="start", mode=options["mode"])

        device.log(message="response: {}".format(response), level="DEBUG")
        if options["mode"] == "BACKGROUND":
            match = re.search(r"\[\d+\]\s+(\d+)", response)
            if match:
                self.hidden_info["pktgen_pid_list"].append(match.group(1))

        # while self.hidden_info["pktgen_pid_list"]:
        #     dev.execute_shell_command_on_device(device=device, command="kill -9 {}".format(self.hidden_info["pktgen_pid_list"].pop()))

        return True

    def create_nfs_connection_between_host(self, device, remote_host, **kwargs):
        """Create NFS connection between 2 host

        :param IP remote_host:
            **REQUIRED** Remote host's ipaddress

        :param STR remote_path:
            *OPTIONAL* Remote host's shared path. Default: /dev/shm/nfs

        :param STR local_path:
            *OPTIONAL* Local mount path. Default: same as remote_path

        :param STR service_control_tool:
            *OPTIONAL* Modern OS use "systemctl" to manage each service so far, but older OS such as 'CentOS 6', 'Ubuntu 14' use "service". This
                       option should be "systemctl" or "service". Default: "service"

        :param INT|STR timeout:
            *OPTIONAL* Command timeout. Default: 30

        :return:
            Return True if mount succeed. Any invalid option will raise ValueError or RuntimeError
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["remote_host"] = remote_host
        options["remote_path"] = re.sub(r"/$", "", kwargs.pop("remote_path", "{}/nfs".format(self.default["memory_folder"])))
        options["local_path"] = kwargs.pop("local_path", options["remote_path"])
        options["service_control_tool"] = str(kwargs.pop("service_control_tool", "service")).upper()
        options["timeout"] = int(kwargs.pop("timeout", 30))

        if options["service_control_tool"] not in ("SYSTEMCTL", "SERVICE"):
            raise ValueError("option 'service_control_tool' must be 'systemctl' or 'service', but got '{}'".format(
                options["service_control_tool"].lower()
            ))

        cmds = []
        if options["service_control_tool"] == "SYSTEMCTL":
            cmds.append("systemctl restart rpcbind")
        else:
            cmds.append("service rpcbind restart")

        cmds.append("/bin/mkdir -p {}".format(options["local_path"]))
        cmds.append("/bin/mount -t nfs {}:{} {}".format(options["remote_host"], options["remote_path"], options["local_path"]))
        cmds.append("/bin/cd {}".format(options["local_path"]))
        cmds.append("/bin/mount")

        return_value = True
        try:
            response = dev.execute_shell_command_on_device(device=device, command=cmds, timeout=options["timeout"])
            if not re.search(r"{}:{}\s+on\s+{}\s+".format(options["remote_host"], options["remote_path"], options["local_path"]), response):
                device.log(message="Mount path '{}' not found.".format(options["local_path"]), level="ERROR")
                return_value = False
        except TobyException as err:     # pragma: no cover
            device.log(message=err, level="ERROR")
            return_value = False

        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value

    def close_nfs_connection_between_host(self, device, remote_host, **kwargs):
        """Close NFS connection between 2 host and delete local mount folder

        :param IP remote_host:
            **REQUIRED** Remote host's ipaddress

        :param STR remote_path:
            *OPTIONAL* Remote host's shared path. Default: /dev/shm/nfs

        :param STR local_path:
            *OPTIONAL* Local mount path. Default: same as remote_path

        :param str service_control_tool:
            *OPTIONAL* Modern OS use "systemctl" to manage each service so far, but older OS such as 'CentOS 6', 'Ubuntu 14' use "service". This
                       option should be "systemctl" or "service". Default: "service"

        :param INT|STR timeout:
            *OPTIONAL* Command timeout. Default: 300

        :return:
            Return True if unmount succeed. Any invalid option will raise ValueError or RuntimeError
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["remote_host"] = remote_host
        options["remote_path"] = re.sub(r"/$", "", kwargs.pop("remote_path", "{}/nfs".format(self.default["memory_folder"])))
        options["local_path"] = kwargs.pop("local_path", options["remote_path"])
        options["service_control_tool"] = str(kwargs.pop("service_control_tool", "service")).upper()
        options["timeout"] = int(kwargs.pop("timeout", 300))

        if options["service_control_tool"] not in ("SYSTEMCTL", "SERVICE"):
            raise ValueError("option 'service_control_tool' must be 'systemctl' or 'service', but got '{}'".format(
                options["service_control_tool"].lower()
            ))

        cmds = []
        if options["service_control_tool"] == "SYSTEMCTL":
            cmds.append("systemctl stop rpcbind")
            cmds.append("systemctl stop nfs")
        else:
            cmds.append("service stop rpcbind")
            cmds.append("service stop nfs")

        cmds.append("/bin/cd")
        cmds.append("/bin/umount -f {}".format(options["local_path"]))

        # do not delete folder that in '/'
        folder_path = os.path.split(options["local_path"])[0]
        if folder_path != "/":
            cmds.append("/bin/rm -rf {}".format(options["local_path"]))

        cmds.append("/bin/mount")

        return_value = True
        try:
            response = dev.execute_shell_command_on_device(device=device, command=cmds, timeout=options["timeout"])
        except TobyException as err:     # pragma: no cover
            device.log(message=err, level="ERROR")
            return_value = False

        if re.search(r"{}:{}\s+on\s+{}\s+".format(options["remote_host"], options["remote_path"], options["local_path"]), response):
            device.log(message="Mount path {} still alive".format(options["local_path"]), level="ERROR")
            return_value = False

        device.log(message="{} return value: {}".format(func_name, return_value), level="INFO")
        return return_value
