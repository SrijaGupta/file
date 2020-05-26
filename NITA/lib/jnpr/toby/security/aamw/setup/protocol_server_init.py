import re

import jnpr.toby.security.aamw.util.mail_util as mail_util

MAIL_SERVER_USR_PWD_DICT = {'test_usr_%s' % x: 'Jnpr123*' for x in range(20)}


def init_http_server(server_handle,
                     http_config_dir='/etc/httpd/conf/httpd.conf',
                     ssl_config_dir='/etc/httpd/conf.d/ssl.conf'):
    """
    Init HTTP server
    :param server_handle:
    :param http_config_dir:
    :param ssl_config_dir:
    :return:
    """
    server_handle.su()

    # http settings
    server_handle.log('Processing HTTP config: %s' % http_config_dir)
    server_handle.shell(command='chmod 777 %s' % http_config_dir)
    res = server_handle.shell(command='cat %s | grep Listen'
                                      % http_config_dir).response()
    if not re.search('(\n|^)Listen\s+\[::\]:8080', res):
        if not re.search('(\n|^)Listen', res):
            server_handle.log('Adding listen port for 8000 and 8080')
            server_handle.shell(
                command='echo \"Listen [::]:8080\" >> %s' % http_config_dir)
            server_handle.shell(
                command='echo \"Listen [::]:8000\" >> %s' % http_config_dir)
        else:
            server_handle.log('Adding listen port for 80, 8000 and 8080')
            server_handle.shell(
                command='echo \"Listen [::]:8080\" >> %s' % http_config_dir)
            server_handle.shell(
                command='echo \"Listen [::]:8000\" >> %s' % http_config_dir)
            server_handle.shell(
                command='echo \"Listen [::]:80\" >> %s' % http_config_dir)

    # ssl settings
    server_handle.log('Processing SSL config: %s' % ssl_config_dir)
    server_handle.shell(command='chmod 777 %s' % ssl_config_dir)
    res = server_handle.shell(command='cat %s | grep Listen'
                                      % ssl_config_dir).response()
    if not re.search('(\n|^)Listen\s+\[::\]:443', res):
        server_handle.shell(
            command='echo \"Listen [::]:443\" >> %s' % ssl_config_dir)


def init_smtp_server(server_handle,
                     mail_usr_pwd_dict=MAIL_SERVER_USR_PWD_DICT,
                     add_usr=True):
    if not add_usr:
        mail_usr_pwd_dict = None
    return _init_smtp_server_with_arg(server_handle, 'SMTP', mail_usr_pwd_dict)


def init_smtps_server(server_handle,
                      mail_usr_pwd_dict=MAIL_SERVER_USR_PWD_DICT,
                      add_usr=True):
    """
    Init SMTP server
    :param server_handle:
    :param mail_usr_pwd_dict:
    :param add_usr:
    :return:
    """
    if not add_usr:
        mail_usr_pwd_dict = None
    return _init_smtp_server_with_arg(server_handle, 'SMTPS',
                                      mail_usr_pwd_dict)


def init_smtp_tls_server(server_handle,
                         mail_usr_pwd_dict=MAIL_SERVER_USR_PWD_DICT,
                         add_usr=True):
    """
    Init SMTP TLS server
    :param server_handle:
    :param mail_usr_pwd_dict:
    :param add_usr:
    :return:
    """
    if not add_usr:
        mail_usr_pwd_dict = None
    return _init_smtp_server_with_arg(server_handle, 'SMTP_TLS',
                                      mail_usr_pwd_dict)


def init_imap_server(server_handle,
                     mail_usr_pwd_dict=MAIL_SERVER_USR_PWD_DICT,
                     add_usr=True):
    """
    Init IMAP server
    :param server_handle:
    :param mail_usr_pwd_dict:
    :param add_usr:
    :return:
    """
    if not add_usr:
        mail_usr_pwd_dict = None
    server_handle.log('Configuring SMTP server for IMAP')
    return _init_smtp_server_with_arg(server_handle, 'SMTP', mail_usr_pwd_dict)


def init_imaps_server(server_handle,
                      mail_usr_pwd_dict=MAIL_SERVER_USR_PWD_DICT,
                      add_usr=True):
    """
    Init IMAPS Server
    :param server_handle:
    :param mail_usr_pwd_dict:
    :param add_usr:
    :return:
    """
    if not add_usr:
        mail_usr_pwd_dict = None
    server_handle.log('Configuring SMTP server for IMAPS')
    return _init_smtp_server_with_arg(server_handle, 'SMTP', mail_usr_pwd_dict)


def init_imap_tls_server(server_handle,
                         mail_usr_pwd_dict=MAIL_SERVER_USR_PWD_DICT,
                         add_usr=True):
    """
    Init IMAP TLS server
    :param server_handle:
    :param mail_usr_pwd_dict:
    :param add_usr:
    :return:
    """
    server_handle.log('Configuring SMTP server for IMAP_TLS')
    if not add_usr:
        mail_usr_pwd_dict = None
    return _init_smtp_server_with_arg(server_handle, 'SMTP', mail_usr_pwd_dict)


def _init_smtp_server_with_arg(server_handle, protocol, mail_usr_pwd_dict):
    """
    Private func for init SMTP server
    :param server_handle:
    :param protocol:
    :param mail_usr_pwd_dict:
    :return:
    """
    smtp_config_dict = {
        'smtp': '/volume/argon/argon_traffic_files/test/sendmail.mc.org',
        'smtps': '/volume/argon/argon_traffic_files/test/sendmail_smtps.mc',
        'smtp_tls': '/volume/argon/argon_traffic_files/test/sendmail_tls.mc'
    }
    smtp_config_dir = smtp_config_dict.get(protocol.lower(), None)
    assert smtp_config_dir, 'Unexpected protocol: %s for SMTP server ' \
                            'initiation' % protocol

    # config sendmail file
    server_handle.log('Going to upload local file %s to server: '
                      '/etc/mail/sendmail.mc' % smtp_config_dir)
    server_handle.upload(local_file=smtp_config_dir,
                         remote_file='/etc/mail/sendmail.mc',
                         protocol='scp', user='root', password='Embe1mpls')

    # server_handle.shell(command="m4 /etc/mail/sendmail.mc > "
    #                             "/etc/mail/sendmail.cf",
    #                     timeout=120)
    server_handle.shell(command='cd /etc/mail', timeout=120)
    server_handle.shell(command='make', timeout=120)
    server_handle.shell(command="service sendmail restart", timeout=120)

    # restart mail server
    mail_util.mail_server_action(server_handle,
                                 action=mail_util.MailServerAct.RESTART)
    # add user
    if not mail_usr_pwd_dict:
        server_handle.log('Not adding mail server users')
    else:
        server_handle.log('Adding mail server users')
        mail_util.add_mail_users(server_handle, usr_pwd_dict=mail_usr_pwd_dict)