
class MailServerAct:
    STOP = 0
    START = 1
    RESTART = 2


def mail_server_action(server_handle, action=MailServerAct.RESTART,
                       prog_dir='/mailtemp/mail-tools', timeout=60):
    if action == MailServerAct.STOP:
        server_handle.log('Going to STOP mail server')
    elif action == MailServerAct.START:
        server_handle.log('Going to START mail server')
    elif action == MailServerAct.RESTART:
        server_handle.log('Going to RESTART mail server')
    else:
        assert False, 'Unexpected mail server action value: %s' % action

    server_handle.shell(command='{prog_dir}/mail_server -action '
                                '{action}'.format(prog_dir=prog_dir,
                                                  action=action),
                        timeout=timeout)


def add_mail_users(server_handle, usr_pwd_dict):

    for usr, pwd in usr_pwd_dict.items():
        assert usr and pwd, 'Unexpected user:password value: %s: %s' % \
                            (usr, pwd)
        server_handle.log('Going to add user: %s with password: %s'
                          % (usr, pwd))
    add_usr = ' '.join(['-add_user %s -pass %s' % usr_pwd
                       for usr_pwd in usr_pwd_dict.items()])
    _stop_mail_services(server_handle)
    res = server_handle.shell(command='/mailtemp/mail-tools/mail_server '
                                      '%s' % add_usr,
                              timeout=300).response()
    _start_mail_services(server_handle)
    server_handle.log('Response when adding user: %s' % res)


def del_mail_users(server_handle, usr_set):

    for usr in usr_set:
        server_handle.log('Going to delete user: %s ' % usr)
    del_usr = ' '.join(['-del_user %s' % usr for usr in usr_set])
    _stop_mail_services(server_handle)
    res = server_handle.shell(command='/mailtemp/mail-tools/mail_server '
                                      '%s' % del_usr,
                              timeout=300).response()
    _start_mail_services(server_handle)
    server_handle.log('Response when adding deleting: %s' % res)


def clear_mail_box(server_handle, server_ip, user_pwd_dict,
                   prog_dir=None):
    cyrus, port = 0, 143
    prog_dir = '/mailtemp/mail-tools' if prog_dir is None else prog_dir

    server_handle.log('Clearing mail boxes')
    for usr, pwd in user_pwd_dict.items():
        server_handle.log('User: %s password: %s' % (usr, pwd))

    usr_pwd_str = ' '.join(['-user %s -pass %s' % item for item in
                            user_pwd_dict.items()])
    cmd = '{prog_dir}/mail_box -cyrus {cyrus} -clean 1 -server ' \
          '{server_ip} -port {port} ' \
          '{usr_pwd_str}'.format(prog_dir=prog_dir, cyrus=cyrus,
                                 server_ip=server_ip, port=port,
                                 usr_pwd_str=usr_pwd_str)
    ret = server_handle.shell(command=cmd, timeout=60).response()
    assert not ret, 'Unexpected response for clean mail boxes: %s' % ret
    server_handle.log('Mail boxes cleaned successfully')


def _stop_mail_services(server_handle):
    server_handle.su()
    server_handle.shell(command='/sbin/service ypbind stop', timeout=60)
    server_handle.shell(command='/sbin/service autofs stop', timeout=60)


def _start_mail_services(server_handle):
    server_handle.su()
    server_handle.shell(command='/sbin/service ypbind start', timeout=60)
    server_handle.shell(command='/usr/bin/ypwhich -m | grep homes', timeout=60)
    server_handle.shell(command='/sbin/service autofs start', timeout=60)
