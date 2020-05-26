""" This module contains methods useful for performing remote file operations without explicitly downloading or
uploading the entire file.

NOTE: SSH must be enabled on your remote device. Methods require an SSH connection.
"""


from jnpr.toby.hldcl.connectors.sshconn import SshConn

__author__ = ['Dan Bond']
__contact__ = 'dbond@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'

def clobber_remote_file(host_name: str, string_to_write: str, file_name: str):
    """ This function clobbers an existing file stored on a remote host with a user supplied string.
    If the file does not exist, it will be created and populated with said string.
    :param host_name:
        **REQUIRED** Full host name of remote host.
        Example input: 'wfce99@englab.juniper.net'
    :param string_to_write:
        **REQUIRED** The string you want written to the remote file.
    :param file_name:
        **REQUIRED** The full path of the file as it is stored on the remote host.
        Example input: '/usr/local/etc/raddb/sample.txt'
    :return: True if file operation is successful. In the event of failure, an exception is thrown.
    """
    # Establish SshConn for remote file operations. Write config to specified file
    ssh_connection = SshConn(host=host_name, user='root', password='Embe1mpls')
    sftp_client = ssh_connection.open_sftp()
    file_handle = sftp_client.open(file_name, mode='w')

    # Write to file
    try:
        file_handle.write(string_to_write)
    finally:
        file_handle.close()

    return True


def append_remote_file(host_name: str, string_to_write: str, file_name: str):
    """ This function appends a file stored on a remote host with a user supplied string.
    :param host_name:
        **REQUIRED** Full host name of remote host.
        Example input: 'wfce99@englab.juniper.net'
    :param string_to_write:
        **REQUIRED** The string you want written to the remote file.
    :param file_name:
        **REQUIRED** The full path of the file as it is stored on the remote host.
        Example input: '/usr/local/etc/raddb/sample.txt
    :return: True if file operation is successful. In the event of failure, an exception is thrown.
    """
    # Establish SshConn for remote file operations. Write config to specified file
    ssh_connection = SshConn(host=host_name, user='root', password='Embe1mpls')
    sftp_client = ssh_connection.open_sftp()
    users_file_handle = sftp_client.open(file_name, mode='a')

    # Write to file
    try:
        users_file_handle.write(string_to_write)
    finally:
        users_file_handle.close()

    return True


def prepend_remote_file(host_name: str, string_to_write: str, file_name: str):
    """Prepends a string to an existing remote file.
    :param host_name:
        **REQUIRED** Full host name of remote host.
        Example input: 'wfce99@englab.juniper.net'
    :param string_to_write:
        **REQUIRED** The string you want written to the remote file.
    :param file_name:
        **REQUIRED** The full path of the file as it is stored on the remote host.
        Example input: '/usr/local/etc/raddb/sample.txt'
    :return:
        True if file operation is successful. In the event of failure, an exception is thrown.
    """
    # Prepend operation is heavier than overwrite/append. Must read in file beforehand, then regenerate.
    ssh_connection = SshConn(host=host_name, user='root', password='Embe1mpls')
    sftp_client = ssh_connection.open_sftp()

    # Read in the previous contents of the file
    with sftp_client.open(file_name, mode='r') as file_handle:
        previous_contents = file_handle.read()

    with sftp_client.open(file_name, mode='w') as handle:
        handle.write(string_to_write)
        handle.write(previous_contents)

    return True

def read_remote_file_to_string(host_name: str, file_name: str):
    """Reads a remote file and returns a string containing the contents of that remote file.
        :param host_name:
            **REQUIRED** Full host name of remote host.
            Example input: 'wfce99@englab.juniper.net'
        :param file_name:
            **REQUIRED** The full path of the file as it is stored on the remote host.
            Example input: '/usr/local/etc/raddb/sample.txt'
        :return:
            String containing the current contents of the file
        """
    # Prepend operation is heavier than overwrite/append. Must read in file beforehand, then regenerate.
    ssh_connection = SshConn(host=host_name, user='root', password='Embe1mpls')
    sftp_client = ssh_connection.open_sftp()

    # Read in the previous contents of the file
    with sftp_client.open(file_name, mode='r') as file_handle:
        current_contents = file_handle.read()

    # Return the byte string as a decoded string
    return current_contents.decode("utf-8")
