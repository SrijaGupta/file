#!/usr/bin/python3
""" Keyword to send and fetch email """
#=========================================================================
#
#         FILE:  email_traffic.py
#  DESCRIPTION:  Keywords to send mail using SMTP and fetch mail using IMAP and POP3
#       AUTHOR:  Mohammad Ismail Qureshi ( mqureshi)
#      COMPANY:  Juniper Networks
#      VERSION:  1.0
#=========================================================================

import re
import time
from jnpr.toby.hldcl.host import upload_file


def smtp_send_mail(device=None, server=None, to_address=None, **kwargs):
    """
    To send mail .
    Example:
      smtp_send_mail(device=linux, server="5.0.0.1" ,to_address="abc@xyz.com" ,\
                     from_address="a@test.com", cc_address="b@test.com" ,bcc_address="c@test.com" \
                     ,subject="test mail",  mail_message="message_file" ,\
                     attachment="attach_file@text/plain" ,encoding="basec64"
      smtp_send_mail(device=linux, server="5.0.0.1" ,auth_type="auth-login", user="test" ,\
                    password="netscreen" , to_address="abc@xyz.com" ,from_address="a@test.com"\
                    , cc_address="b@test.com" ,bcc_address="c@test.com" ,subject="test mail"
              mail_message="message_file" ,attachment="attach_file@text/plain" ,encoding="basec64"
    Robot example:
     Smtp Send Mail  device=linux  server=5.0.0.1  to_address=abc@xyz.com  from_address=a@test.com
                cc_address=b@test.com  bcc_address=c@test.com  subject=test mail
                mail_message=message_file  attachment=attach_file@text/plain  encoding=basec64
     Smtp Send Mail  device=linux  server=5.0.0.1 auth_type=auth-plain   user=test  password=netscr
                to_address=abc@xyz.com  from_address=a@test.com  cc_address=b@test.com
                bcc_address=c@test.com  subject=test mail  mail_message=message_file
                subject=test mail  mail_message=message_file  attachment=attach_file@text/plain
                encoding=basec64

    :param Device device:
         **REQUIRED** Device handle for Linux host
    :param str server:
         **REQUIRED** SMTP server IP
    :param str to_address:
         **REQUIRED** TO recipient address for email
    :param str auth_type:
         *OPTIONAL* To enable auth for smtp session , possible values are -
                    auth-login , auth-plain , auth-cram-md5  and auth
    :param str user:
         *OPTIONAL* User name , mandatory if auth-login is passed
    :param str password:
         *OPTIONAL* Password of user, mandatory if auth-login is passed
    :param str cc_address:
         *OPTIONAL* CC recipient address for email
    :param str bcc_address:
         *OPTIONAL* BCC recipient address for email
    :param str subject:
         *OPTIONAL* Subject of email
    :param str mail_message:
         *OPTIONAL* Mail matter it should be file name containing mail matter
    :param str attachment:
         *OPTIONAL* Attachment file name , it should be file name of attachment
                    MIME/type of file can be passed along with filename
                    attachment=attach_file@text/plain
                    attachment=attach_file.pdf@application/pdf
    :param str encoding:
         *OPTIONAL* Encoding type for body and attachment , possible values are -
                    7bit, 8bit, binary, base64 and quoted-printable
    :return: True if successful.
              In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device argument is mandatory")
    if server is None or to_address is None:
        device.log(level='ERROR', message="server and to_address are mandatory argument")
        raise ValueError("server and to_address are mandatory argument")

    # Copy required smtp tool to send mail
    program_dir = "/volume/labtools/lib/Testsuites/SRX/IPS/programs/"
    local_file = program_dir + "smtp-cli.pl"
    upload_file(device, local_file=local_file, remote_file="/tmp/")

    to_address = to_address.replace('\r', "")

    mail_cmd = '/tmp/smtp-cli.pl --server ' + server + ' --to ' + to_address
    if 'auth_type' in kwargs:
        if 'user' not in kwargs or 'password' not in kwargs:
            device.log(level='ERROR', message="user and password is mandatory with auth_type")
            raise ValueError("user and password is mandatory with auth_type")
        auth_type = kwargs.get('auth_type')
        user = kwargs.get('user')
        password = kwargs.get('password')
        mail_cmd = mail_cmd + ' --user ' + user + ' --pass ' + password + ' --' + auth_type
    if 'from_address' in kwargs:
        from_address = kwargs.get('from_address')
        mail_cmd = mail_cmd + ' --from ' + from_address
    if 'cc_address' in kwargs:
        cc_address = kwargs.get('cc_address')
        mail_cmd = mail_cmd + ' --cc ' + cc_address
    if 'bcc_address' in kwargs:
        bcc_address = kwargs.get('bcc_address')
        mail_cmd = mail_cmd + ' --bcc ' + bcc_address
    if 'subject' in kwargs:
        subject = kwargs.get('subject')
        mail_cmd = mail_cmd + ' --subject ' + subject
    if 'mail_message' in kwargs:
        mail_message = kwargs.get('mail_message')
        mail_cmd = mail_cmd + ' --body-plain ' + mail_message
    if 'attachment' in kwargs:
        attachment = kwargs.get('attachment')
        mail_cmd = mail_cmd + ' --attach ' + attachment
    if 'encoding' in kwargs:
        encoding = kwargs.get('encoding')
        mail_cmd = mail_cmd + ' --text-encoding ' + encoding
    if 'auth_type' not in kwargs:
        mail_cmd = mail_cmd + ' --disable-starttls  --ipv4 --missing-modules-ok --verbose'
    else:
        mail_cmd = mail_cmd + ' --ipv4 --missing-modules-ok --verbose'

    mail_cmd = mail_cmd.replace('\r', "")
    device.log(level='INFO', message=mail_cmd)
    response = device.shell(command=mail_cmd)
    if 'QUIT' in response.response():
        device.log(level='INFO', message="Mail sent successfuly")
        return True
    else:
        device.log(level='ERROR', message="Failed to send mail")
        raise Exception("Failed to send mail")


def imap_fetch_mail(device=None, server=None, user_name=None, password=None, starttls=None):
    """
    To fetch mail using IMAP protocol

    Example:
      imap_fetch_mail (device=linux, server="5.0.0.1", user_name="test", password="netscreen"
                       starttls="yes")
    Robot example:
      imap fetch mail  device=linux  server=5.0.0.1  user_name=test  password=netscreen
                       starttls=yes

    :param Device device:
         **REQUIRED** Device handle for Linux host
    :param str server:
         **REQUIRED** IMAP server IP
    :param str user_name:
         **REQUIRED**  User name , required login to server
    :param str password:
         **REQUIRED** Password of user, required to login to server
    :param str starttls:
         *OPTIONAL* Flas to send starttls command , its valuse should be "yes"
    :return: True if successful.
              In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if server is None or user_name is None or password is None:
        device.log(level='ERROR', message="server ,user_name and password are mandatory arguments")
        raise ValueError("server ,user_name and password are mandatory arguments")

    # Copy required imap tool to fetch mail
    program_dir = "/volume/labtools/lib/Testsuites/SRX/IPS/programs/"
    local_file = program_dir + "imap.py"
    upload_file(device, local_file=local_file, remote_file="/tmp/")

    cmd = '/tmp/imap.py -s ' + server + ' -u ' + user_name + ' -p ' + password

    if starttls is not None:
        cmd = cmd + ' -t ' + starttls
    cmd = cmd.replace('\r', "")
    response = device.shell(command=cmd)
    if "Unable to fetch mail" in response.response():
        device.log(level='ERROR', message="Failed to fetch mail")
        raise Exception("Failed to fetch mail")
    else:
        return True


def pop3_fetch_mail(device=None, server=None, user_name=None, password=None, starttls=None):
    """
    To fetch mail using IMAP protocol

    Example:
      pop3_fetch_mail (device=linux, server="5.0.0.1", user_name="test", password="netscreen"
                       starttls="yes")
    Robot example:
      pop3 fetch mail  device=linux  server=5.0.0.1  user_name=test  password=netscreen
                       starttls=yes

    :param Device device:
         **REQUIRED** Device handle for Linux host
    :param str server:
         **REQUIRED** IMAP server IP
    :param str user_name:
         **REQUIRED**  User name , required login to server
    :param str password:
         **REQUIRED** Password of user, required to login to server
    :param str starttls:
         *OPTIONAL* Flas to send starttls command , its valuse should be "yes"
    :return: True if successful.
              In all other cases Exception is raised
    :rtype: bool
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if server is None or user_name is None or password is None:
        device.log(level='ERROR', message="server ,user_name and password are mandatory arguments")
        raise ValueError("server ,user_name and password are mandatory arguments")

    # Copy required pop3 tool to fetch mail
    program_dir = "/volume/labtools/lib/Testsuites/SRX/IPS/programs/"
    local_file = program_dir + "pop3.py"
    upload_file(device, local_file=local_file, remote_file="/tmp/")

    cmd = '/tmp/pop3.py -s ' + server + ' -u ' + user_name + ' -p ' + password

    if starttls is not None:
        cmd = cmd + ' -t ' + starttls

    cmd = cmd.replace('\r', "")
    response = device.shell(command=cmd)
    if "Unable to fetch mail" in response.response():
        device.log(level='ERROR', message="Failed to fetch mail")
        raise Exception("Failed to fetch mail")
    else:
        return True

def execute_interactive_commands(device=None, command=None, pattern=None, timeout=5):
    """
    To execute shell command in interactive way by sending command and receiving expected pattern
    Example -
       cmd_lst=['gnutls-cli --crlf --starttls --port 25 --insecure 5.0.0.1', 'EHLO 5.0.0.1',\
               'STARTTLS', '\x04', 'MAIL FROM: <abc@xyz.com>', \
               'RCPT TO: regress@srxdpi-lnx4.englab.juniper.net', 'DATA','this is test mail data',\
                'abcd1234abcd1234', '.', 'QUIT']
       ptrn_lst=['0530', '\r\n', '\r\n', '\r\n', '\r\n', '\r\n', '\r\n', '\r\n', '\r\n', '\r\n', \
              '\r\n']
       execute_shell_commands(device=dut, Command=cmd_list, pattern=ptrn_lst, timeout=5)
    ROBOT Example -
      Set Test Variable cmd_lst =
             gnutls-cli --crlf --starttls --port 25 --insecure 5.0.0.1  EHLO 5.0.0.1  STARTTLS  \x04
             MAIL FROM: <abc@xyz.com>  RCPT TO: regress@srxdpi-lnx4.englab.juniper.net  DATA
             this is test mail data  abcd1234abcd1234  .  QUIT
      Set Test Variable ptrn_lst = 0530  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n
      execute shell commands  device=${dut}  Command=${cmd_list}  pattern=${ptrn_lst}

     :param Device device:
         **REQUIRED** Device handle for the Linux host
     :param lst command:
         **REQUIRED** Commands to be executed , Need to be pass in same order as they need to
                      be executed
     :param lst pattern:
         **REQUIRED** Pattern expected in executing command , Need to be passed in same order
                      for respected command
     :param str timeout:
         **REQUIRED** Timeout for command
     :return: True if successful.
                 In all other cases Exception is raised
     :rtype: bool
    """
    # Checking for mandatory arguments
    if device is None:
        raise ValueError("device is mandatory argument")
    if command is None or pattern is None:
        device.log(level='ERROR', message="command_pattern and command sequence are mandatory \
                  argument")
        raise Exception("command and pattern are mandatory argument")

    # Checking if same number of command and pattern passed by user
    if len(command) != len(pattern):
        device.log(level='ERROR', message="Number of command and pattern should be same")
        raise Exception("Number of command and pattern should be same")

    # Executing command  sequentially
    print(timeout)
    count = range(len(command))
    for iteam in count:
        time.sleep(2)
        device.shell(command=command[iteam], pattern=pattern[iteam], timeout=timeout)
    return True

