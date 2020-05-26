"""
Class for TelnetConn
"""
import re
import time
from telnetlib import Telnet, IAC, NOP
import logging
from jnpr.toby.exception.toby_exception import TobyException, TobyConnectLost, raise_toby_exception
from jnpr.toby.utils.utils import check_device_scan, prepare_log_message
# pylint: disable=protected-access

class TelnetConn(Telnet):
    """
    Class to telnet to a device.
    """
    def __init__(self, **kwargs):
        """
        Static method that returns an object of class telnetlib.Telnet
        :param host:
            **REQUIRED** hostname or IP address of device to telnet to
        :param user:
            **REQUIRED** Login user name.
        :param password:
            **REQUIRED** Login Password.
        :param port:
            *OPTIONAL* Port on device to which connection needs to made.
            Default: port = 23
        :param console:
            *OPTIONAL* Is true if establishing a console connection.
            Default: console = False
        :return: object of class telnetlib.Telnet
        """
        host = kwargs['host']
        user = kwargs['user'] + '\r\n'
        user = user.encode(encoding='ascii')
        password = kwargs['password'] + '\r\n'
        password = password.encode(encoding='ascii')
        port = kwargs.get('port', None)
        console = kwargs.get('console', False)
        kill_sessions = kwargs.get('kill_sessions', 'yes')
        expect_timeout = kwargs.get('connect_timeout', 20)
        empty_line = False  # used to see if 'enter' needs to be hit upon empty line
        skip_user = False  # used to see if only password is asked for
        already_logged_in = False  # set to True if device goes straight into prompt and is not console
        if port is None:
            super(TelnetConn, self).__init__(host=host)
            self.port = 23
        else:
            super(TelnetConn, self).__init__(host=host, port=port)
            self.port = port
        # self.set_debuglevel(1)    #uncomment this line to see extensive send/recieve information from telnetlib
        self.write(b'\r\n')  # typing \r to initiate regular session
        prompt = self.expect([br'[Ll]ogin:[\s]?', br'Enter your option[\s]?:[\s]?',
                              b'Type the hot key to suspend the connection: <CTRL>Z',
                              b'Connect to Port read/write',
                              b'Entering server port,', br'(%|>|#)[\s]?',
                              b'User Access Verification',
                              b'There is no hot key to close the connection'
                              b'Escape character is'], timeout=expect_timeout)
        if prompt[0] == -1:
            raise TobyException("Expected 'login', 'Enter your option', 'Type the hot key to "
                                "suspend the connection:', 'Connect to Port read/write', "
                                "'Entering server port', 'User Access Verification',"
                                "'There is no hot key to close the connection', 'Escape character is' "
                                "from "+host+", but instead got:\r\n'"+prompt[2].decode('ascii')+"'")
        # Handles cisco device
        if prompt[0] == 6:
            inner_prompt = self.expect([br'[Uu]sername:[\s]?', br'[Pp]assword:[\s]?'], timeout=expect_timeout)
            if inner_prompt[0] == -1:
                raise TobyException("Expected 'Username:' or 'Password:' from "+host+", but instead "
                                    "got:\r\n'"+inner_prompt[2].decode('ascii')+"'")
            if inner_prompt[0] == 1:
                skip_user = True  # skips entering user if password prompt appears
        # If you go straight to the prompt make sure you exit to login
        if prompt[0] == 5:
            # If device is not console we are already logged in and no need to do anything else
            if console:
                empty_line = True
            else:
                already_logged_in = True
        # Server port with menu
        if prompt[0] == 3:
            inner_prompt = self.expect([br'>>[\s]?'], timeout=expect_timeout)
            if inner_prompt[0] == -1:
                raise TobyException("Expected '>> ' but instead got:\r\n'"
                                    + inner_prompt[2].decode('ascii')+"'")
            self.write(b'a')  # Enter option for connecting to port
            time.sleep(1)
            empty_line = True
        # If multi session menu then choose appropiate option
        if prompt[0] == 1:
            if kill_sessions == 'yes':
                self.write(b'4')  # typing 4 to kill all processes
                inner_prompt1 = self.expect([br'Enter session PID or \'all\'[\s]?:[\s]?'], timeout=2)
                # If you do not get a prompt right away it is the menu which requires
                # you to hit enter first
                if inner_prompt1[0] == -1:
                    self.write(b'\r\n')  # hit enter if next prompt does not show
                    inner_prompt2 = self.expect([br'Kill session \(id or all\):[\s]?',
                                                 br'Enter your option[\s]?:[\s]?'],
                                                timeout=expect_timeout)
                    # You should get option to kill menu or go back to main menu
                    if inner_prompt2[0] == -1:
                        raise TobyException("Expected 'Kill session (id or all)' or 'Enter your option' "
                                            "from "+host+", but instead got:\r\n'" +
                                            inner_prompt2[2].decode('ascii') + "'")
                    if inner_prompt2[0] == 0:
                        self.write(b'all\r\n')  # type all to kill all other sessions
                        inner_prompt2 = self.expect([br'Enter your option[\s]?:[\s]?'], timeout=expect_timeout)
                        if inner_prompt2[0] == -1:
                            raise TobyException("Expected 'Enter your option:' from " + host + ", but instead "
                                                "got:\r\n'" + inner_prompt2[2].decode('ascii') + "'")
                if inner_prompt1[0] == 0:  # type 'all' with enter if prompt comes up
                    self.write(b'all\r\n')
                    empty_line = True
            # If already has not moved onto login phase, enter 1 to initiate regular session
            if not empty_line:
                self.write(b'1\r\n')  # typing 1 to initiate regular session
                inner_prompt1 = self.expect([b'Type the hot key to suspend the connection:',
                                             br'[Ll]ogin:[\s]?',
                                             br'(\%|\>|\#|\$)[\s]?$'],
                                            timeout=expect_timeout)
                if inner_prompt1[0] == -1:
                    raise TobyException("Expected 'Type the hot key...', 'login', "
                                        "or 'shell/config/cli prompt' from " + host + ", "
                                        "but instead got:\r\n'" + inner_prompt1[2].decode('ascii')+"'")
                empty_line = True
        # If various prompts comes up and then it hangs, we need to hit
        # enter to proceed
        # Prompt 2: 'Type the hot key to suspend the connection:'
        # Prompt 4: 'Entering server port,'
        # Prompt 7: 'There is no hot key to close the connection'
        # Prompt 8: 'Escape character is'
        if prompt[0] == 2 or prompt[0] == 4 or prompt[0] == 7 or prompt[0] == 8:
            time.sleep(1)
            empty_line = True
        # Reusable block of code for when 'enter' needs to be hit based on prompts
        if empty_line:
            self.write(b'\r\n')  # typing enter
            # Keep 'exit'-ing until login state is reached
            login_reached = False
            while not login_reached:
                inner_prompt = self.expect([br'[Ll]ogin:[\s]?', br'(\%|\>|\#|\$)[\s]?$', b'logout'],
                                           timeout=expect_timeout)
                if inner_prompt[0] == -1:
                    logging.error("Expected 'login' or 'shell/config/cli prompt' from " + host + ", but instead "
                                  "got:\r\n'" + inner_prompt[2].decode('ascii')+"'")
                    raise TobyException("Expected 'login' or 'shell/config/cli prompt' from " + host + ", but instead "
                                        "got:\r\n'" + inner_prompt[2].decode('ascii')+"'")
                # for when you exit and logout appears but login is taking a while to come up
                if inner_prompt[0] == 2:
                    inner_prompt = self.expect([br'[Ll]ogin:[\s]?'], timeout=60)
                    if inner_prompt[0] == -1:
                        logging.error("Expected 'login' from " + host + ", but instead "
                                      "got:\r\n'" + inner_prompt[2].decode('ascii')+"'")
                        raise TobyException("Expected 'login' from " + host + ", but instead "
                                            "got:\r\n'" + inner_prompt[2].decode('ascii')+"'")
                if inner_prompt[0] == 0:
                    login_reached = True
                # Already logged in (meaning shared users) and so need to exit
                # out before relogging in
                else:
                    self.write(b'exit\r\n')  # typing exit
                    time.sleep(1)  # need to wait or 'exit' ends up in login or password value
        if not already_logged_in:
            # Log in with credentials - skips password entry if root user after zeroization (device in amnesiac mode)
            if not skip_user:
                time.sleep(1)
                self.write(user)
                prompt = self.expect([br'\$\s$', br'\%[\s]?$', br'\#[\s]?$', br'\>[\s]?$',
                                      br'[Pp]assword:[\s]?'], timeout=expect_timeout)
                if prompt[0] == -1:
                    raise TobyException("Sent '"+user.decode('ascii') + "' to "+host+", expected 'Password: '"
                                        " or 'shell/cli prompt', but got:\r\n'"+prompt[2].decode('ascii') + "'")
            if prompt[0] == 4 or skip_user:
                self.write(password)
                prompt = self.expect([br'\$\s$', br'\%[\s]?$', br'\#[\s]?$', br'\>[\s]?$'], timeout=expect_timeout)
                if prompt[0] == -1:
                    raise TobyException("Sent '" + password.decode('ascii') + "' to " + host + ", expected "
                                        "'shell/cli prompt', but got:\n'" + prompt[2].decode('ascii') + "'")
            # Once you enter device, make sure that it is in shell mode
            if prompt[0] == 3:
                self.write(b'start shell\r\n')
                prompt = self.expect([br'\$\s$', br'\%[\s]?$', br'\#[\s]?$', br'\>[\s]?$'], timeout=expect_timeout)
            # Making sure in shell mode and then setting column width
            if prompt[0] == 0 or prompt[0] == 1 or prompt[0] == 2:  # pragma: no branch
                self.write(b'stty cols 160\n')
                prompt = self.expect([br'\$\s$', br'\%[\s]?$', br'\#[\s]?$'], timeout=expect_timeout)
                if prompt[0] == -1:  # pragma: no branch
                    logging.error("Not able to set column width to 160")
        else:
            pass  # do not try to enter usename or password if already logged into device

    def execute(self, **kwargs):
        """
        Method to send a string command to the device and store its response in
        response attribute of device
        :param cmd:
            **REQUIRED** Command to be sent to device.
        :param pattern:
            **REQUIRED** Output will be collected till this pattern is found.
        :param device:
            **REQUIRED** Device object
        :param timeout:
            *OPTIONAL* Time by which output is expected. Default is
            60 seconds
        :param raw_output:
            *OPTIONAL* Returns raw output of the command. Default is False
        :return: Index of the pattern matched
        """
        command = kwargs['cmd']
        carriage_return = kwargs.get('carriage_return', True)
        # If command is not CTL-C, add a new line to it
        if command is not '\x03':
            if carriage_return:
                command += '\r'
        # Convert unicode to bytes
        cmd = command.encode(encoding='ascii')
        device = kwargs['device']
        expect_timeout = kwargs.get('timeout', 60)
        raw_output = kwargs.get('raw_output', 0)
        show_error = kwargs.get('show_error', False)
        time_start = None
        time_end = None
        resp_time = None

        # If the specified pattern is a scalar, convert it to a list.
        if isinstance(kwargs['pattern'], str):
            kwargs['pattern'] = [kwargs['pattern']]

        # Add possible expected pattern '---(more)---' for paged vty and cty output
        kwargs['pattern'].append(r'---\(more\)---')

        # Send command to device
        try:
            self.write(cmd)
            time_start = time.time()
        except Exception:
            message = "Failed to send command '%s' to %s" % (cmd, device.host)
            if show_error:
                device.log(level='WARN', message=message)
            else:
                device.log(level='ERROR', message=message)
            message += "\n.  Target device may be offline, or connection may have dropped."
            device_args = dict()
            device_args['channel'] = 'text'
            device_args['host'] = str(device._kwargs.get('con-ip')) \
                if device._kwargs.get('connect_targets', '') == 'console' \
                else str(device._kwargs.get('hostname') or device.host)
            device_args['port'] = device._kwargs.get('text_port') if device._kwargs.get('text_port') else 23
            device.log(level='INFO',
                       message='Generating diagnostic report since text channel '
                               'creation failed for %s' % device_args['host'])
            check_device_scan(None, channels_check=False, **device_args)
            raise TobyConnectLost(message=message)
        device.log("Executing command (timeout %ss): %s" % (expect_timeout, command))

        if expect_timeout > 1:
            time.sleep(1)
            tmp_expect_timeout = expect_timeout -1
        else:
            tmp_expect_timeout = expect_timeout

        # Need to investigate whether we need no_response
        no_response = kwargs.get('no_response', 0)
        user_pattern = kwargs.get('user_pattern', False)
        output = []
        response = ''
        if not no_response:
            pattern_bytes = []
            pattern_new = ''
            for pattern in kwargs['pattern']:
                pattern += "$"
                pattern_bytes.append(pattern.encode('ascii'))
                # pattern_new = pattern_new + pattern + ","
                if not re.search(r'---\\\(more\\\)---', pattern):
                    pattern_new = pattern_new + pattern + ","
            output = self.expect(pattern_bytes, timeout=tmp_expect_timeout)
            last_index = len(pattern_bytes) - 1

            # # Added code to get the resonse time in sec
            time_end = time.time()
            resp_time = time_end - time_start
            resp_time = "{:.2f} seconds".format(resp_time)
            resp_out = "\n----------------------------------------\n"
            try:
                resp_out += "==> " + output[2].decode('ascii') + " "
            except:
                try:
                    resp_out += "==> " + output[2].decode('utf-8') + " "
                except:
                    resp_out += "==> " + output[2].decode('iso-8859-1') + " "
            resp_out += "\n----------------------------------------"
            device.log(resp_out)
            device.log("Command execution completed (" + resp_time + ")")
            if output[0] == -1:
                resp_lines = output[2].decode('ascii').split("\r\n")
                last_line_resp = resp_lines[len(resp_lines)-1]
                log_message = prepare_log_message(command, device.mode, pattern_new, last_line_resp, expect_timeout)
                if user_pattern:
                    message = "User supplied pattern '%s' not seen within '%s' seconds after issuing " \
                              "command on device" \
                              % (pattern_new, expect_timeout)
                    message += log_message
                    if show_error:
                        device.log(level='ERROR', message=message)
                    else:
                        device.log(level='WARN', message=message)
                else:
                    message = "Device prompt '%s' did not return within '%s' seconds after issuing command on device" \
                              % (pattern_new, expect_timeout)
                    message += log_message
                    if show_error:
                        device.log(level='ERROR', message=message)
                    else:
                        device.log(level='WARN', message=message)
                temp_resp = output[2].decode('ascii')
                temp_resp.replace(kwargs['cmd'] + '\r\n', '', 1)
                device_health = dict()
                message = prepare_log_message(command, device.mode, pattern_new, last_line_resp, expect_timeout)
                if show_error:
                    device.log(level='WARN', message=message)
                else:
                    device.log(level='ERROR', message=message)
                message = ''
                if temp_resp == '':
                    device.log(level='INFO', message="No response from device after issuing command")
                    device.log(level='INFO', message="Initiating device connectivity checks…")
                    device_health = check_device_scan(device)
                    message = "Device prompt did not return " \
                              "within " + str(expect_timeout) + " seconds after issuing command on device"
                    raise_toby_exception(device_health, message=message, host_obj=device)
                else:
                    message = "Device prompt did not return within " + str(expect_timeout)
                    message += " seconds after issuing command on device  Target device may be hung"
                    raise_toby_exception(device_health, message=message, host_obj=device)
                return output[0]

            # If the matched pattern was '---(more)---'
            elif output[0] == last_index:
                while output[0] == last_index:
                    try:
                        response += output[2].decode('utf-8').replace('\n---(more)---', '')
                    except UnicodeDecodeError:
                        response += output[2].decode('iso-8859-1').replace('\n---(more)---', '')
                    output = self.write(b'\r\n')
                    output = self.expect(pattern_bytes, timeout=expect_timeout)
                try:
                    hey = re.sub('\n.*' + pattern_bytes[output[0]].decode('utf-8')[:-1], '',
                                 output[2].decode('utf-8'), 2)
                except UnicodeDecodeError:
                    hey = re.sub('\n.*' + pattern_bytes[output[0]].decode('iso-8859-1')[:-1], '',
                                 output[2].decode('iso-8859-1'), 2)
                response += hey
                device.response = response

            else:
                pattern_new = pattern_new[:-1]
                # elif re.search("Toby", command):
                try:
                    hey = re.sub(' set', 'set', output[2].decode('utf-8'))
                except UnicodeDecodeError:
                    hey = re.sub(' set', 'set', output[2].decode('iso-8859-1'))
                if command is not '\x03' and hey == command[:-2]:
                    # If device prompt is part of sent command
                    output = self.expect([pattern_bytes[output[0]]], timeout=3)
                # device.response = x[2].decode('utf-8').replace('\n' +
                #                                               device.prompt, '',
                #                                               1)
                try:
                    decode_resp = output[2].decode('utf-8')
                except:
                    decode_resp = output[2].decode('iso-8859-1')
                if command is not '\x03':
                    try:
                        if not raw_output:
                            device.response = output[2].decode('utf-8').replace('\n' + str(device.prompt[0]), '')
                        else:
                            device.response = output[2]
                    except UnicodeDecodeError:
                        device.response = output[2].decode('iso-8859-1').replace('\n' + device.prompt[0], '')
                        device.matched_pattern_index = output[0]
                    # device.response = x[2].decode('utf-8').replace(pattern, '')
                    # device.response = re.sub(pattern_new, '', x[2], 1)
            if not raw_output:
                device.response = device.response.replace(kwargs['cmd'] + '\r\n', '', 1)
                device.response = device.response.replace(kwargs['cmd'] + ' \r\n', '', 1)
                device.response = device.response.replace(kwargs['cmd'] + '\r\r\n', '', 1) #added
                # cmd_repl_arr = kwargs['cmd'].split('\n')
                # for cmd_repl in cmd_repl_arr:
                #     device.response = device.response.replace(cmd_repl +
                #                                               '\r\n', '', 1)
                #     device.response = device.response.replace(cmd_repl +
                #                                               ' \r\n', '', 1)
            return output[0]
        return 1

    def is_active(self):
        """
        check to see if socket is listening
        no parameters
        """
        try:
            if self.sock:  # this way, we've taken care of problem if the .close() was called
                self.sock.send(IAC+NOP)  # first try
                self.sock.send(IAC+NOP)  # second try - sometimes connection loss take multiple try to confirm
                return True
            else:
                return False
        except Exception:
            return False
