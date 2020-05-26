"""
Module to ssh through proxy to a device.
"""
import re
import paramiko
import logging
from select import select
import time
from jnpr.toby.exception.toby_exception import TobyException


class Proxysshconn(object):
    """
    Class to ssh through proxy to a device.
    """
    def __init__(self, *args, **kvargs):
        """
        Static method that returns an object of class Paramiko.Transport
        Object is connected over ssh from host to destination host(Jump host/ Bastion Host)

        :param proxy_host:
            **REQUIRED** hostname or IP address of the proxy.
        :param proxy_user:
            **REQUIRED** Login user name of the proxy.
        :param proxy_password:
            **REQUIRED** Login Password of the proxy.
        :param proxy_port:
            *OPTIONAL* Port on device to which connection needs to made to the proxy.
            Default: port=22
        :param host:
            **REQUIRED** hostname or IP address of destination device to connect to.
        :param user:
            **REQUIRED** Login user name of destination device.
        :param password:
            **REQUIRED** Login Password of destination device.
        :param port:
            *OPTIONAL* Port on device to which connection needs to made to destination device.
            Default: port=22
        :return: object of class Paramiko.Transport connected to the destination device.
        """
        self.proxy_host = kvargs.get('proxy_host')
        self.proxy_user = kvargs.get('proxy_user')
        self.proxy_password = kvargs.get('proxy_password')
        self.proxy_port = kvargs.get('proxy_port')
        self.proxy_ssh_key_file = kvargs.get('proxy_ssh_key')
        self.proxy_connection = False
        self.host = kvargs.get('host')
        self.user = kvargs.get('user')
        self.password = kvargs.get('password')
        self.port = kvargs.get('port')
        self.dest_connection = False

        try:
            # Add host key policy
            if self.proxy_port is None:
                self.proxy_port = 22
            self.transport = paramiko.Transport((self.proxy_host, self.proxy_port))
            self.transport.start_client()
            if self.proxy_ssh_key_file:
                self.proxy_ssh_key = paramiko.RSAKey.from_private_key_file(self.proxy_ssh_key_file)
                conn_result = self.transport.auth_publickey(username=self.proxy_user, key=self.proxy_ssh_key)
            else:
                conn_result = self.transport.auth_password(username=self.proxy_user, password=self.proxy_password)
            if len(conn_result) == 0:
                self.proxy_connection = True
            else:
                logging.error('Unable to connect to proxy host. Authentication failed.')
                raise TobyException('Unable to connect to proxy host. Authentication failed.')
        except Exception as exp:
            logging.error('Unable to connect to proxy host: %s' % exp)
            raise TobyException('Unable to connect to proxy host: %s' % exp)

        try:
            if self.port is None:
                self.port = 22
            self.tunnel = paramiko.Transport(self.transport.open_channel(
                kind='direct-tcpip',
                dest_addr=(self.host, self.port),
                src_addr=('127.0.0.1', 0)))
            self.tunnel.start_client()
            conn_result = self.tunnel.auth_password(username=self.user, password=self.password)
            if len(conn_result) == 0:
                self.dest_connection = True
            else:
                logging.error('Unable to connect to destination host. Authentication failed.')
                raise TobyException('Unable to connect to destination host. Authentication failed.')
        except Exception as exp:
            logging.error('Unable to connect to destination host: %s' % exp)
            raise TobyException('Unable to connect to destination host: %s' % exp)

        try:
            self.handle = self.tunnel.open_session(20)
            self.handle.get_pty(width=160, height=0)
            self.handle.invoke_shell()
            self.handle.set_combine_stderr(True)
            self.handle.settimeout(60)
            tnh = self.handle
            got = []
            while True:
                _rd, _wr, _err = select([tnh], [], [], 10)
                if _rd:
                    data = tnh.recv(1024)
                    data = data.decode("utf-8")
                    got.append(data)
                    if re.search('> ', data):
                        tnh.send(b' start shell\n')
                        data = tnh.recv(1024)
                        data = data.decode("utf-8")
                    if re.search(r'(\$|>|#|%)[\s\t]?', data):
                        break
        except Exception as exp:
            logging.error(
                'Unable to fetch the prompt on destination host: %s' % exp)
            raise TobyException(
                'Unable to fetch the prompt on destination host: %s' % exp)

    def close(self):
        """
        This method closes the closes the ssh connections established.
        All Proxysshconn connections should be closed at the end of the script.

        """
        try:
            self.tunnel.close()
            self.transport.close()
        except Exception as exp:
            logging.error('Unable to close the device handle: %s' % exp)
            raise TobyException('Unable to close the device handle: %s' % exp)
        return True

    def execute(self, **kvargs):
        """
        Method to send a string command to the device and store its response in
        response attribute of device

        :param cmd:
            **REQUIRED** Command to be sent to device.
        :param pattern:
            **REQUIRED** Output will be collected till this pattern is found.
        :param timeout:
            *OPTIONAL* Time by which output is expected. Default is
            60 seconds
        :param device:
            **REQUIRED** Device object
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False
        :return: Index of the pattern matched
        """
        cmd = kvargs.get('cmd')
        pattern = kvargs.get('pattern')
        device = kvargs['device']
        timeout = kvargs.get('timeout', 60)
        raw_output = kvargs.get('raw_output', 0)
        if isinstance(pattern, str):
            pattern = [pattern]
        pattern.append(r'---\(more\)---')
        pattern_new = ''
        for pat in pattern:
            pattern_new = pattern_new + pat + ","
        pattern_new = pattern_new[:-1]
        tnh = self.handle
        cmd_send = cmd + '\n'
        if not hasattr(device, 'shelltype'):
            device.shelltype = 'sh'
            #        if device.shelltype == 'sh':
            #            cmd_re = cmd + '\s?\r\n'
            #        else:
        cmd_re = cmd + r'\s?\r{1,2}\n'
        cmd_re = re.sub(r'\$', '\\$', cmd_re)
        cmd_re = re.sub(r'\|', '\\|', cmd_re)
        device.log("Executing command: "+cmd_send)
        tnh.send(cmd_send)
        match = -1
        if 'no_response' in kvargs and kvargs['no_response']:
            device.response = ''
            match = 1
        else:
            (output, resp) = self.wait_for(expected=pattern,
                                           shell=device.shelltype,
                                           timeout=timeout)
            response = ''
            while '---(more)---' in resp:
                response += re.sub(r'\n---\(more\)---', '', resp, 1)
                tnh.send('\r\n')
                (output, resp) = self.wait_for(expected=pattern,
                                               shell=device.shelltype,
                                               timeout=timeout)
            response += resp
            if not raw_output:
                response = re.sub(cmd_re, '', response)
            if not output:
                device.log(level='ERROR',
                           message="Sent '%s' to %s, expected '%s', "
                                   "but got:\n'%s'" % (cmd, device.host,
                                                       pattern_new,
                                                       response))
                match = -1
            else:
                for pat in pattern:
                    match += 1
                    if re.search(pat, response):
                        break
            if not raw_output:
                for pat in pattern:
                    response = re.sub('\n.*' + pat, '', response)
                response = re.sub('\r\n$', '', response)
            device.response = response
            device.log(response)
        return match

    def wait_for(self, expected=r'\s\$', timeout=60, shell='sh'):
        """
        Method to recieve output from paramiko object.

        :param expected: Pattern expected in output.
        :param timeout: Timeout waiting for pattern in output. Default 60 sec
        :param shell: mode of shell in device
        :return: Output from paramiko object.##TIMEOUT## if pattern not seen.
        """
        time.sleep(1)
        timeout -= 2
        tnh = self.handle
        time_int = 10
        time_out = 0
        got = ''
        timeout_occ = 0
        if isinstance(expected, list):
            if shell == 'csh':
                for _ele_i, _ele_j in enumerate(expected):
                    expected[_ele_i] = re.sub(r'\s$', r'(\s|\t)',
                                              expected[_ele_i])
            expected = '|'.join(expected)
        while True:
            start_time = time.time()
            _rd, _wr, _err = select([tnh], [], [], time_int)
            if _rd:
                data = tnh.recv(4096)
                data = data.decode("utf-8")
                got = got + data
            end_time = time.time()
            if re.search(r'{0}\s?$'.format(expected), got):
                break
            time_out += (end_time - start_time)
            if int(time_out) > timeout:
                timeout_occ = 1
                break
        if timeout_occ:
            return False, got
        return True, got

