import os
import re

import jnpr.toby.security.aamw.util.helper_util as helper


SMTP_MAIL_TRAFFIC_CMD = '{prog_dir}/send -server {server_ip} -port {port} ' \
                        '-from {sender} {receiver_str} -subject \'{subject}\''\
                        ' {att_str} -debug {debug} -out {output} -timeout ' \
                        '{api_timeout} -content \'{content}\''
SMTPS_MAIL_TRAFFIC_CMD = '{prog_dir}/smtp-cli.pl --server {server_ip} --port '\
                         '{port} {option} --from {sender} {receiver_str} ' \
                         '--subject \'{subject}\' --verbose --ipv4 {att_str} '\
                         '--body-plain \'{content}\''


def send_email_traffic(client_handle, server_handle, protocol, sender,
                       receiver_list, server_ip, port=25, subject='',
                       content=None, attachment_list=None, debug=1,
                       output=None):
    """
    Send Email traffic
    :param client_handle:
    :param server_handle:
    :param protocol:
    :param sender:
    :param receiver_list:
    :param server_ip:
    :param port:
    :param subject:
    :param content:
    :param attachment_list:
    :param debug:
    :param output:
    :return:
    """
    # initialize and log
    protocol = protocol.lower()
    assert receiver_list, \
        "Receiver list must non-less than 1: %s" % receiver_list
    attachment_list = [] if attachment_list is None else attachment_list
    output = '%s_log' % protocol if output is None else output
    api_timeout = 600
    send_timeout = 660
    lab_domain = '.englab.juniper.net'

    if protocol != 'smtp':
        # get server hostname
        helper.log_break('Getting server hostname')
        hostname = server_handle.shell(
            command='hostname', timeout=send_timeout).response().strip()
        server_handle.log("Server hostname: %s" % hostname)
        assert hostname, "Server hostname is empty"
        if lab_domain in hostname:
            receiver_list = [x + '@' + hostname for x in receiver_list]
        else:
            receiver_list = [x + '@' + hostname + lab_domain \
                for x in receiver_list]

    # log initial
    helper.log_break('Sending email with following params')
    client_handle.log('Protocol: %s' % protocol)
    client_handle.log('Sender: %s' % sender)
    client_handle.log('Receiver(s): %s' % str(receiver_list))
    client_handle.log('Server IP: %s' % server_ip)
    client_handle.log('Port: %s' % port)
    client_handle.log('Subject: %s' % subject)
    client_handle.log('Content: %s' % content)
    client_handle.log('Attachment(s): %s' % str(attachment_list))
    client_handle.log('Debug: %s' % str(debug))
    client_handle.log('Output: %s' % str(output))

    # construct send email command
    if protocol == 'smtp':
        prog_dir = '/mailtemp/mail-tools'
        mail_traffic_cmd = SMTP_MAIL_TRAFFIC_CMD.format(
            prog_dir=prog_dir, server_ip=server_ip, port=port, sender=sender,
            subject=subject, debug=debug, output=output,
            api_timeout=api_timeout, content=content,
            att_str=' '.join(['-att %s' % att for att in attachment_list]),
            receiver_str=' '.join(['-to %s' % recv for recv in receiver_list]))
    elif protocol == 'smtps':
        prog_dir = '/root/Downloads'
        option = '--ssl'
        mail_traffic_cmd = SMTPS_MAIL_TRAFFIC_CMD.format(
            prog_dir=prog_dir, server_ip=server_ip, port=port, sender=sender,
            subject=subject, debug=debug, content=content, option=option,
            att_str=' '.join(['--attach %s' % att for att in attachment_list]),
            receiver_str=' '.join(
                ['--to %s' % recv for recv in receiver_list]))
    elif protocol == 'smtp_tls':
        prog_dir = '/root/Downloads'
        option = ''
        mail_traffic_cmd = SMTPS_MAIL_TRAFFIC_CMD.format(
            prog_dir=prog_dir, server_ip=server_ip, port=port, sender=sender,
            subject=subject, debug=debug, content=content, option=option,
            att_str=' '.join(['--attach %s' % att for att in attachment_list]),
            receiver_str=' '.join(
                ['--to %s' % recv for recv in receiver_list]))
    else:
        err_msg = 'Unexpected protocol: %s' % protocol
        client_handle.log('ERROR', err_msg)
        raise AssertionError(err_msg)

    # send email
    client_handle.log('Send email shell cmd: %s' % mail_traffic_cmd)
    client_handle.shell(command=mail_traffic_cmd, timeout=send_timeout)
    helper.log_break('Sending email complete')

    # if smtp show result else already printed out
    if protocol == 'smtp':
        helper.log_break('Email sending log %s' % output)
        res_list = client_handle.shell(command='/usr/bin/strings %s' % output,
                                       timeout=60).response().split('\n')
        if not res_list or (len(res_list) == 1 and any([
                re.search('No such file or directory', res_list[0]),
                re.search('cannot open.?for reading', res_list[0])])):
            client_handle.log('ERROR', 'Email sending fail')
            raise AssertionError('Email sending fail')
        for res in res_list:
            client_handle.log(res)
        helper.log_break('Email sending log %s over' % output)


def send_web_traffic(device_handle, protocol, host, file_name, inet6=False):
    """
    Send HTTP/HTTPS traffic
    :param device_handle:
    :param protocol:
    :param host:
    :param file_name:
    :param inet6:
    :return:
    """
    protocol = protocol.lower()

    assert protocol in ['http', 'https'], 'Unexpected protocol: %s' % protocol

    cmd_list = ['curl', '-v']
    prefix = 'http://'
    if protocol == 'https':
        cmd_list += ['-k', '-i']
        prefix = 'https://'

    if inet6:
        host = '[%s]' % host

    cmd_list += [prefix+os.path.join(host, file_name), '-o', 'aa']
    helper.log_break('Sending web traffic for protocol %s' % protocol)
    try:
        device_handle.shell(command=' '.join(cmd_list), timeout=300)
    except Exception as e:
        device_handle.log("Exception occurred and suppressed: %s" % str(e))
        pass


def send_web_traffic_via_proxy(device_handle, protocol, host, file_name,
                               proxy_ip, proxy_port, inet6=False):
    protocol = protocol.lower()

    if protocol not in ['http', 'https']:
        raise ValueError('Unexpected protocol: %s' % protocol)

    proxy_url = 'http://%s:%s' % (proxy_ip, proxy_port)

    cmd_list = ['curl', '-v', '--proxy', proxy_url]
    prefix = 'http://'
    if protocol == 'https':
        cmd_list += ['-k', '-i']
        prefix = 'https://'

    if inet6:
        host = '[%s]' % host

    cmd_list += [prefix+os.path.join(host, file_name), '-o', 'aa']
    helper.log_break('Sending web traffic for protocol %s' % protocol)
    try:
        device_handle.shell(command=' '.join(cmd_list), timeout=300)
    except Exception as e:
        device_handle.log("Exception occurred and suppressed: %s" % str(e))
        pass


def fetch_mail(device_handle, protocol, host, user, password, mail_num=1,
               header=True, body=True):
    """
    Fetch email
    :param device_handle:
    :param protocol:
    :param host:
    :param user:
    :param password:
    :param mail_num:
    :param header:
    :param body:
    :return:
    """
    protocol = protocol.lower()

    assert protocol in ['imap', 'imaps', 'imap_tls']

    helper.log_break('Start fetching email(s)')
    device_handle.log("Protocol: %s" % protocol)
    device_handle.log("Host: %s" % host)
    device_handle.log("User: %s" % user)
    device_handle.log("Password: %s" % password)
    device_handle.log("Mail number: %s" % mail_num)
    device_handle.log("Fetch header: %s" % header)
    device_handle.log("Fetch body: %s" % body)
    res = dict()

    cmd_template = "curl --insecure --verbose {ssl} --url \"{protocol}:" \
                   "//{server_ip}/INBOX\" --user \"{receiver}:{password}\"" \
                   " --request \"%s\"".format(server_ip=host, receiver=user,
                                              password=password,
                                              ssl='--ssl' if
                                              protocol == 'imap_tls' else '',
                                              protocol='imap' if
                                              protocol != 'imaps' else 'imaps')

    tmp = device_handle.shell(command=cmd_template %
                                      ('fetch %s uid' % mail_num),
                              timeout=30).response()
    uid = re.search('FETCH \(UID (\\d+)\)', tmp)
    assert uid, 'UID not found for email'
    uid = uid.group(1)
    device_handle.log('Email UID: %s' % uid)

    if header:
        request = "UID fetch %s RFC822.HEADER" % uid
        device_handle.log("Fetching header")
        tmp = device_handle.shell(command=cmd_template % request,
                                  timeout=30).response()
        res['header'] = tmp

        if 'OK Fetch completed' in tmp:
            device_handle.log('Email header fetched successfully')
        else:
            device_handle.log(level='WARN',
                              message='Email header fetch failed')

    if body:
        request = "UID fetch %s RFC822.TEXT" % uid
        device_handle.log("Fetching body text")
        tmp = device_handle.shell(command=cmd_template % request,
                                  timeout=30).response()
        res['body'] = tmp

        if 'OK Fetch completed' in tmp:
            device_handle.log('Email body text fetched successfully')
        else:
            device_handle.log(level='WARN',
                              message='Email body text fetch failed')
    device_handle.log('Email fetch completed: %s' % res)
    return res

def fetch_newest_mail(device_handle, protocol, host, user, password):
    """
    Fetch email
    :param device_handle:
    :param protocol:
    :param host:
    :param user:
    :param password:
    :return:
    """
    protocol = protocol.lower()

    assert protocol in ['imap', 'imaps', 'imap_tls']

    helper.log_break('Start newest fetching email(s)')
    device_handle.log("Protocol: %s" % protocol)
    device_handle.log("Host: %s" % host)
    device_handle.log("User: %s" % user)
    device_handle.log("Password: %s" % password)

    cmd_template = "curl --insecure --verbose {ssl} --url \"{protocol}:" \
                   "//{server_ip}/INBOX\" --user \"{receiver}:{password}\"" \
                   " --request \"%s\"".format(server_ip=host, receiver=user,
                                              password=password,
                                              ssl='--ssl' if
                                              protocol == 'imap_tls' else '',
                                              protocol='imap' if
                                              protocol != 'imaps' else 'imaps')

    tmp = device_handle.shell(command=cmd_template % ('fetch 1 uid'),
                              timeout=30).response()
    device_handle.log('Response for fetch 1 uid: %s' % tmp)
    uid = re.search('(\\d+) EXISTS', tmp)
    assert uid, 'UID not found for email'
    uid = uid.group(1)
    device_handle.log('Email UID: %s' % uid)
    request = "uid fetch %s body[]" % uid
    device_handle.log("Fetching mail via IMAP")
    tmp = device_handle.shell(command=cmd_template % request,
                              timeout=30).response()
    if 'OK Fetch completed' in tmp:
        device_handle.log('Email body text fetched successfully')
    else:
        device_handle.log(level='WARN', message='Email fetch failed')
    device_handle.log('Email fetch completed: %s' % tmp)
    return tmp