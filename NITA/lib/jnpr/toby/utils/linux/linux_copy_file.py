#! /usr/local/bin/python3

"""
 DESCRIPTION:   To copy files from linux VM to any remote host
     COMPANY:   Juniper Networks
"""


def linux_copy_file(**kwargs):
    """
    Copy file from linux Host to any remote device
    Example:
        linux_copy_file(linux_host=unix, remote_ip="10.209.86.23", local_file="server.pem")
        linux_copy_file(linux_host=unix, remote_ip="10.209.86.23", local_file="server.pem",
                                                                            passwd="Embe1mpls")
    Robot Example:
        linux copy file    linux_host=${dut}    remote_ip=${dut_mgt_ip}    local_file=server.pem

    :param device linux_host:
        **REQUIRED** linux handle
    :param str remote_ip:
        **REQUIRED** Remote IP of the device where file should be copied
    :param str local_file:
        **REQUIRED** Name of the file which to be copied from linux host along with path.
    :param str remote_file:
        *OPTIONAL* file path(if any) and file name(if any except the local file name) in the remote
        host. Default path is /tmp.
    :param str user_name:
        *OPTIONAL* user name for the remote host.
    :param str passwd:
        *OPTIONAL* password for the remote host.
    :param str action:
        *OPTIONAL* to download from or upload into the remote host
    :return: True
    :rtype: bool
    """
    linux_host = kwargs.get('linux_host', None)
    remote_ip = kwargs.get('remote_ip', None)
    local_file = kwargs.get('local_file', "/tmp/test.txt")
    remote_file = kwargs.get('remote_file', "/tmp")
    user_name = kwargs.get('user_name', "root")
    passwd = kwargs.get('passwd', "Embe1mpls")
    action = kwargs.get('action', "upload")

    if linux_host is None or remote_ip is None or local_file is None:
        linux_host.log(level='ERROR', message="linux_host, remote ip and local_file are "
                                              "mandatory arguments")
        raise Exception("linux_host, remote ip and local_file are mandatory arguments")

    if action == "upload":
        output = linux_host.shell(command='sshpass -p "%s" scp -o LogLevel=info -o '
                              'UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no %s '
                              '%s@%s:%s' % (passwd, local_file, user_name, remote_ip, remote_file))
    elif action == "download":
        output = linux_host.shell(command='sshpass -p "%s" scp -o LogLevel=info -o '
                              'UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no %s@%s:%s '
                              '%s' % (passwd, user_name, remote_ip, remote_file, local_file))

    if 'Permission denied' in output.response() or 'No such file or directory' in \
            output.response() or 'No route to host' in output.response() or 'command not found' \
            in output.response():
        linux_host.log(level='ERROR', message="could not copy the file. " + output.response())
        raise Exception("Could not copy the file")
    else:
        linux_host.log(level='INFO', message="file coped successfully")
        return True
