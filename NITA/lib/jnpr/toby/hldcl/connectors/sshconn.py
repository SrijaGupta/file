"""
Class for sshconn
"""
import re
import logging
import time
from select import select
from jnpr.toby.exception.toby_exception import TobyException, TobyConnectLost, raise_toby_exception
from jnpr.toby.utils.utils import check_device_scan, prepare_log_message
# paramiko is importing with no problem, but pylint reports error, so disabling check
import paramiko

class SshConn(paramiko.client.SSHClient):
    """
    Class to ssh to a device.
    """

    def __init__(self, host, user, password, port=None, ssh_key_file=None, initialize_command='start shell'):
        """
        Static method that returns an object of class Paramiko.SSHClient

        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            **REQUIRED** Login user name.
        :param password:
            **REQUIRED** Login Password.
        :param port:
            *OPTIONAL* Port on device to which connection needs to made.
            Default: port=22
        :return: object of class Paramiko.SSHClient
        """

        try:
            super(SshConn, self).__init__()
            self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        except Exception as error:
            raise TobyException("Cannot establish SshConn and set missing host key policy on Device "
                                "%s: %s: username=%s" % (host, error, user))
        try:
            if port is None:
                if ssh_key_file is None:
                    self.connect(hostname=host, username=user, password=password, banner_timeout=60)
                else:
                    self.connect(hostname=host, username=user, key_filename=ssh_key_file, banner_timeout=60)
                self.port = 22
            else:
                if ssh_key_file is None:
                    self.connect(hostname=host, username=user, password=password, port=port, banner_timeout=60)
                else:
                    self.connect(hostname=host, username=user, port=port, key_filename=ssh_key_file, banner_timeout=60)
                self.port = port
        except Exception as error:
            self.host = host
            device_args = dict()
            device_args['host'] = host
            device_args['channel'] = 'text'
            device_args['port'] = port if port else 22
            device_health = check_device_scan(None, channels_check=False, **device_args)
            message = "Cannot connect via SSH to Device %s: %s: username=%s, password=%s" % (host, error.__str__(), user, password)
            raise_toby_exception(device_health, message=message, host_obj=None, connect_fail=True)

        self.transport = self.get_transport()
        self.transport.set_keepalive(200)

        try:
            tnh = self.invoke_shell(width=160)
            self.client = tnh
            got = []
            while True:
                read, _wr, _err = select([tnh], [], [], 10)
                if read:
                    data = tnh.recv(1024)
                    try:
                        data = data.decode('utf-8')
                    except UnicodeDecodeError:
                        data = data.decode('iso-8859-1')
                    got.append(data)
                    if re.search('> ', data):
                        cmd = " %s\n" % initialize_command
                        tnh.send(cmd.encode('utf-8'))
                        data = tnh.recv(1024)
                        try:
                            data = data.decode('utf-8')
                        except UnicodeDecodeError:
                            data = data.decode('iso-8859-1')
                    if re.search(r'{0}\s?$'.format(r'(\$|>|#|%)'), data):
                        break
        except Exception as error:
            raise TobyException("Cannot determine prompt for Device "
                                "%s: %s: username=%s" % (host, str(error), user))

    def execute(self, cmd, pattern, device, timeout=60, raw_output=False, no_response=False, carriage_return=True, user_pattern=False, show_error=False):
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
        if isinstance(pattern, str):
            pattern = [pattern]
        pattern.append(r'---\(more\)---')
        pattern_new = ''
        device.response = ''
        for pat in pattern[:-1]:
            pattern_new = pattern_new + pat + ","
        pattern_new = pattern_new[:-1]
        tnh = self.client
        cmd_send = cmd
        if carriage_return:
            cmd_send = cmd + '\r'
        if not hasattr(device, 'shelltype'):
            device.shelltype = 'sh'
#        if device.shelltype == 'sh':
#            cmd_re = cmd + '\s?\r\n'
#        else:
        cmd_re = re.escape(cmd) + r'(\s*)?\r{1,2}?\n?'
        # cmd_re = re.sub('\$', '\\$', cmd_re)
        # cmd_re = re.sub('\|', '\\|', cmd_re)
        # cmd_re = re.sub('-', '\-', cmd_re)
        device.log("Executing command (timeout %ss): %s" % (timeout, cmd_send))
        time_start = None
        time_end = None
        resp_time = None
        try:
            if tnh.recv_ready():
                tnh.in_buffer.empty()
            time_start = time.time()
            tnh.send(cmd_send)
        except Exception as error:
            message = "Failed to send command '%s' to %s" % (cmd, device.host)
            if show_error:
                device.log(level='ERROR', message=message)
            else:
                device.log(level='WARN', message=message)
            message += "\n.  Target device may be offline, or connection may have dropped."
            device_args = dict()
            device_args['channel'] = 'text'
            device_args['host'] = str(device._kwargs.get('hostname') or device.host)
            device_args['port'] = device._kwargs.get('text_port') if device._kwargs.get('text_port') else 22
            device.log(level='INFO',
                       message='Generating diagnostic report since text channel '
                               'creation failed for %s' % device_args['host'])
            check_device_scan(None, channels_check=False, **device_args)
            raise TobyConnectLost(message=message)
        match = -1
        if no_response:
            device.response = ''
            match = 1
        else:
            (output, resp) = self.wait_for(expected=pattern, shell=device.shelltype, timeout=timeout)
            response = ''
            while '---(more)---' in resp:
                response += re.sub(r'\n---\(more\)---', '', resp, 1)
                tnh.send('\r\n')
                (output, resp) = self.wait_for(expected=pattern, shell=device.shelltype, timeout=timeout)
            response += resp
            time_end = time.time()
            resp_time = time_end - time_start
            resp_time = "{:.2f} seconds".format(resp_time)
            tmp_resp = response
            resp_out = "\n----------------------------------------\n"
            resp_out += "==> " + response + " "
            resp_out += "\n----------------------------------------"
            device.log(resp_out)
            device.log("Command execution completed (" + resp_time + ")")
            tmp_resp = re.sub(cmd_re, '', tmp_resp)
            if not output:
                resp_lines = response.split("\r\n")
                last_line_resp = resp_lines[len(resp_lines)-1]
                log_message = prepare_log_message(cmd, device.mode, pattern_new, last_line_resp, timeout)
                user_pattern_not_found = False
                if user_pattern:
                    message = "User supplied pattern '%s' not seen within '%s' seconds after issuing command on device"\
                              % (pattern_new, timeout)
                    message += log_message
                    user_pattern_not_found = True
                    if show_error:
                        device.log(level='ERROR', message=message)
                    else:
                        device.log(level='WARN', message=message)
                else:
                    message = "Device prompt '%s' did not return within '%s' seconds after issuing command on device" \
                              % (pattern_new, timeout)
                    message += log_message
                    if show_error:
                        device.log(level='ERROR', message=message)
                    else:
                        device.log(level='WARN', message=message)
                device_health = dict()
                if tmp_resp == '':
                    device.log(level='INFO', message="No response from device after issuing command")
                    device.log(level='INFO', message="Initiating device connectivity checks…")
                    device_health = check_device_scan(device)
                    device_health['user_pattern_not_found'] = user_pattern_not_found
                    raise_toby_exception(device_health, message=message, host_obj=device)
                else:
                    message += "  % (pattern_new, timeout)"
                    raise_toby_exception(device_health, message=message, host_obj=device)
                match = -1
            else:
                for pat in pattern:
                    match += 1
                    if re.search(pat, response):
                        break
            if not raw_output:
                response = re.sub(cmd_re, '', response)
                for pat in pattern:
                    if re.search('\n', response):
                        response = re.sub('\n.*'+pat, '', response)
                    else:
                        response = re.sub(pat, '', response)
                response = re.sub('\r\n$', '', response)
                response = re.sub(r'\r$', '', response)
            device.response = response
        return match

    def wait_for(self, expected=r'\s\$', timeout=60, shell='sh'):
        """
        Method to receiving output from paramiko object.

        :param expected: Pattern expected in output.
        :param timeout: Timeout waiting for pattern in output. Default 60 sec
        :param shell: mode of shell in device
        :return: Output from paramiko object.##TIMEOUT## if pattern not seen.
        """
        start_time = time.time()
        time.sleep(0.5)
        #timeout -= 1 #with latest changes in timout calc this logic is not needed
        tnh = self.client
        # this is so retrieving output does not take longer than timeout
        if timeout <= 0:
            time_int = 0
        elif timeout < 10:
            time_int = timeout
        else:
            time_int = 10
        time_out = 0
        got = ''
        data = ''
        timeout_occ = 0
        if isinstance(expected, list):
            if shell == 'csh':
                # _j_ even though unused, needs to be assigned as tuple
                for i, _j_ in enumerate(expected):  # pylint: disable=unused-variable
                    expected[i] = re.sub(r'\s$', r'(\s|\t)', expected[i])
            expected = '|'.join(expected)
        old_4k = ''
        new_4k = ''
        while True:
            # #sleep is added so that in case of (end_time-start_time) = 0 time_out counter should increase instead of going in infinite loop
            time.sleep(0.01)
            _rd, _wr, _err = select([tnh], [], [], time_int)
            if _rd:
                data = tnh.recv(4096)
                try:
                    data = data.decode('utf-8')
                except UnicodeDecodeError:
                    data = data.decode('iso-8859-1')
                got = got + data
            end_time = time.time()
            new_4k = old_4k+data
            old_4k = data
            if re.search(r'{0}\s?$'.format(expected), new_4k):
                break
            time_out = (end_time - start_time)
            if time_out > timeout or timeout <= 0:
                timeout_occ = 1
                break
            diff = timeout-int(time_out)
            # calculates difference between time spent and timeout
            if diff < 10:
                time_int = diff
            # changes select function's timeout if < 10 left in timeout

        if timeout_occ:
            return False, got
        return True, got

    def is_active(self):
        """
        This is internal method where we check whether transport is active or not.
        """
        if self.transport:
            if self.transport.is_active():
                # is_active can sometime be incorrect if connection was severed at other end
                # this will do additional checking
                try:
                    self.transport.send_ignore()
                    return True
                except EOFError as err:
                    # connection is closed
                    return False
            else:
                # connection is closed
                return False
        else:
           return False