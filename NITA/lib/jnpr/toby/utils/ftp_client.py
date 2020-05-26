#!/usr/bin/env python3
# coding: UTF-8
"""FTP client to create FTP session with Python3.4+

:Options:
    -i --ipaddr     <required> remote host ipaddr or name
    -c --commands   <optional> command which separated by comma or colon. "," or ":"
    -u --username   <optional> login username. default: regress
    -p --password   <optional> login password. default: MaRtInI
    -t --timeout    <optional> command execution timeout. default: 60

       --passive-mode       <optional> passive mode transit
       --hold-time          <optional> after all cmds send, wait for a while to keep session. default: 0
       --login-timeout      <optional> login connection timeout. default: 30
       --port               <optional> FTP port. default: 21
       --firewall-username  <optional> Special case to do Firewall authentication before FTP login
       --firewall-password  <optional> Special case to do Firewall authentication before FTP login

:Return:
    Just print all cmds' response on sys.stdout channel.

:Example:
    option "-c" in below example are well-designed. The steps include:

    +   pwd:     Get current FTP server's directory
    +   mkdir    Create a new folder 'ftp_tmp_folder' on FTP server
    +   cd       Change to 'ftp_tmp_folder' on server. This is important cmd which means all rest cmds based on this folder
    +   put      Upload local '/tmp/ftp_file' file to 'ftp_tmp_folder/ftp_file'
    +   size     Get file size of 'ftp_tmp_folder/ftp_file' on server
    +   get      Download 'ftp_tmp_folder/ftp_file' to local ./ftp_file
    +   delete   Delete 'ftp_tmp_folder/ftp_file' on server
    +   cd       Change back
    +   rmdir    Remove ftp_tmp_folder

    python ftp_client.py
        -i 127.0.0.1            \
        -u regress              \
        -p MaRtInI              \
        -t 30                   \
        --passive-mode          \
        --login-timeout 10      \
        --port 2121             \
        --hold_time 0           \
        --firewall-username firewall \
        --firewall-password firewall \
        -c "pwd,mkdir ftp_tmp_folder:cd ftp_tmp_folder, put /tmp/ftp_file:size ftp_file, get ftp_file,delete ftp_file,cd ..,rmdir ftp_tmp_folder"

:cmd list:
    ==================================
        Simple Python FTP
    ==================================

    cd          - cd to given folder
    delete      - Delete a file. (cannot delete folder)
    dir         - List folder
    ls          - List folder
    get         - Download file from server
    put         - Upload file to server
    pwd         - Get server's current folder
    rmdir       - Delete a folder. (cannot delete file)
    mkdir       - Create a folder.
    size        - Get file size from server

Use below command to show help:
    python ftp_client.py -h
"""
import os
import sys
import re
import time
import argparse
import ftplib

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


class FTPClient(object):
    """FTP client class"""
    def __init__(self):
        """INIT"""
        self.options = {}
        self.ftp = None

        self.bufsize = 8192
        self.actions = {}
        self.log_level = 1

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
            help="host ipaddr",
        )

        parser.add_argument(
            '-u',
            '--username',
            action="store",
            dest="username",
            default="regress",
            help="login username",
        )

        parser.add_argument(
            '-p',
            '--password',
            action="store",
            dest="password",
            default="MaRtInI",
            help="login password",
        )

        parser.add_argument(
            '-t',
            '--timeout',
            action="store",
            dest="timeout",
            default="60",
            help="cmd execution timeout",
        )

        parser.add_argument(
            '--login-timeout',
            action="store",
            dest="login_timeout",
            default="30",
            help="Timeout for login",
        )

        parser.add_argument(
            '-c',
            '--commands',
            action="store",
            dest="commands",
            default=None,
            help="command list separated by comma (,) to run at remote host",
        )

        parser.add_argument(
            '--port',
            action="store",
            dest="port",
            default="21",
            help="FTP port",
        )

        parser.add_argument(
            '--passive-mode',
            action="store_true",
            dest="passive",
            default=False,
            help="INTO FTP passive mode",
        )

        parser.add_argument(
            '--hold-time',
            action="store",
            default="0",
            dest="hold_time",
            help="Hold FTP connection for given seconds before terminated",
        )

        parser.add_argument(
            '--firewall-username',
            action="store",
            default=None,
            dest="firewall_username",
            help="For firewall authentication",
        )

        parser.add_argument(
            '--firewall-password',
            action="store",
            default=None,
            dest="firewall_password",
            help="For firewall authentication",
        )

        options = parser.parse_args(args=user_options)
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

        if isinstance(options.commands, str):
            self.options["cmd_list"] = re.split(r"\s*[,:]\s*", options.commands)
        elif isinstance(options.commands, (list, tuple)):
            self.options["cmd_list"] = options.commands
        else:
            self.options["cmd_list"] = []

        return self.options

    def firewall_login(self, ipaddr, port, username, password):
        """Firewall authentication"""
        try:
            ftp = ftplib.FTP()
            ftp.set_debuglevel(self.log_level)
            ftp.connect(host=ipaddr, port=port)
            ftp.login(user=username, passwd=password)
        except (BaseException, ftplib.error_perm) as err:
            if not re.search(r"Authentication\s+\-\s+Accepted", str(err), re.I):
                print("Error to login host '{}:{}': {}".format(ipaddr, port, err))
                return False

        return True

    def ftp_login(self, ipaddr, port, username, password):
        """FTP Login"""
        try:
            ftp = ftplib.FTP()
            ftp.set_debuglevel(self.log_level)
            ftp.connect(host=ipaddr, port=port)
            ftp.login(user=username, passwd=password)
        except (BaseException, ftplib.error_perm) as err:
            print("Error to login host '{}:{}': {}".format(ipaddr, port, err))
            return False

        ftp.getwelcome()

        self.ftp = ftp
        self.actions = {
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
        """Download file from remote host

        option 'filepath' should be a abspath on FTP server, this method will:

        1.  split 'filepath' to folder and filename
        2.  on FTP server, cd to folder
        3.  download filename to local, it named ./${filename}
        """
        if re.search(r"/", filepath):
            folder, filename = os.path.split(filepath)
            self.actions["cd"](folder)
        else:
            filename = filepath

        cmd = 'RETR ' + filename
        self.ftp.retrbinary(cmd, open(filename, 'wb').write, self.bufsize)
        print("'{}' download complete".format(filename))
        return True

    def put(self, filepath):
        """Upload local file

        option 'filepath' should be abspath in local, this method will:

        1.  split 'filepath' to local folder and filename
        2.  upload local file to FTP server ./${filename}
        """
        _, filename = os.path.split(filepath)
        cmd = 'STOR ' + filename

        with open(filepath, "rb") as fhld:
            self.ftp.storbinary(cmd, fhld, self.bufsize)

        print("'{}' upload complete".format(filepath))
        return True

    def pwd(self):
        """Get current FTP path"""
        dirname = self.ftp.pwd()
        return dirname

    def size(self, filename):
        """Get server's file size"""
        size = self.ftp.size(filename)
        return size

    def execute_cmd(self):
        """Execute command list"""
        cmd_list = self.options["cmd_list"]
        for cmd in cmd_list:
            print("send cmd:", cmd)
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
                    print("unknown cmd:", cmd)
                    return False

            except Exception as err:
                print(err)

        return True

    def run(self):      # pragma: no cover
        """Entrance"""
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
            print("hold '{}' secs.".format(self.options["hold_time"]))
            time.sleep(self.options["hold_time"])

        return self.actions["quit"]()

if __name__ == "__main__":  # pragma: no cover
    INS = FTPClient()
    try:
        INS.run()
    except KeyboardInterrupt as err:
        print(err)
        exit(1)
