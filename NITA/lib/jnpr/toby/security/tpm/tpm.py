"""
=============================================================================
         FILE:  tpm.py
  DESCRIPTION:  Trusted Platform Module (TPM) generic APIs
       AUTHOR:  Niketa Chellani, nchellani@juniper.net
=============================================================================
"""
import re
import jxmlease
from jnpr.toby.hldcl import device as dev
from jnpr.toby.security.HA.HA import HA

class Tpm(object):
    """
        Tpm keywords for testing TPM on SRX5K with RE3 and SRX300/SRX320/SRX340
        -> get_tpm_status
        -> verity_tpm_status
        -> set_mek
        -> change_mek
        -> delete_mek
        -> list_keypair
        -> delete_keypair
        -> get_keypair_checksum
        -> verify keypair_is_encrypted
    """
    def __init__(self, device_handle):
        """
           Method to initialize tpm device object
        """

        self.device_handle = device_handle


# Method to change Master Encryption Password
# --------------------------------------------
def change_mek(device_handle, current_pswd, new_pswd, **kwargs):
    """
    :param device_handle:
        **REQUIRED** device object
    :param current_pswd:
        ***REQUIRED*** Current Master Encryption Password
    :param new_pswd:
        ***REQUIRED*** New Master Encryption Password
    :param node:
        ***OPTIONAL*** can be 'node0', 'node1' or 'both' if device is in HA. Default is both.

    :return True if Master Encryption Password is set/changed successfully

    Python Examples:
        change_mek(srx0, current_pswd=ddhhkkslwjcngh!!!, new_pswd=xkjdfkejfns$@!)
        change_mek(srx0, current_pswd=ddhhkkslwjcngh!!!, new_pswd=xkjdfkejfns$@!, node=node0)

    Robot Examples:
        Change Mek    ${srx0}   current_pswd=ddhhkcngh!!!    new_pswd=xkjdfke$@!
        Change Mek    ${srx0}   current_pswd=ddhhkjcngh!!!   new_pswd=xkjdfns$@!   node=node0
    """
    ha_dev = HA()
    result = False
    chassis_cluster = _check_chassis_cluster(device_handle)
    cmd = 'request security tpm master-encryption-password set plain-text-password'
    error_msgs = ["error: Password entered does not match with old password",
                  "error: Passwords do not match",
                  "Recommend at least length 12 and use of 3 character classes"]
    flag = 1 if new_pswd == current_pswd else 0
    if flag:
        raise Exception("error: Password entered is same as old password.")
    if chassis_cluster:
        node = kwargs.get('node', 'both')
        node_list = ['node0', 'node1'] if node == 'both' else [node]
        for node in node_list:
            ha_dev.execute_cli_on_node(device=device_handle, node=node,
                                       command=cmd, pattern="password: ")
            ha_dev.execute_cli_on_node(device=device_handle, node=node,
                                       command=current_pswd, pattern="password: ")
            ha_dev.execute_cli_on_node(device=device_handle, node=node,
                                       command=new_pswd, pattern="password: ")
            response = ha_dev.execute_cli_on_node(device=device_handle, node=node,
                                                  command=new_pswd)
            if re.search("successfully generated", str(response).lower()):
                result = True
            elif str(response) in error_msgs:
                raise Exception(str(response))
            else:
                raise Exception("Master Encryption Password could not be changed")
    else:
        dev.execute_cli_command_on_device(device=device_handle,
                                          command=cmd, pattern="password: ")
        dev.execute_cli_command_on_device(device=device_handle,
                                          command=current_pswd, pattern="password: ")
        dev.execute_cli_command_on_device(device=device_handle,
                                          command=new_pswd, pattern="password: ")
        response = dev.execute_cli_command_on_device(device=device_handle,
                                          command=new_pswd)
        if re.search("successfully generated", str(response).lower()):
            result = True
        elif str(response) in error_msgs:
            raise Exception(str(response))
        else:
            raise Exception("Master Encryption Password could not be changed")

    return result

# Method to delete Master Encryption Key
# ---------------------------------------
def delete_mek(device_handle, **kwargs):
    """
    :param device_handle:
        **REQUIRED** device object
    :param node:
        ***OPTIONAL*** can be 'node0', 'node1' or 'both' if device is in HA. Default is both.

    :return: True if MEK has been deleted successfully, else returns False
    """
    chassis_cluster = _check_chassis_cluster(device_handle)
    cmd_list = ["chflags 0 /var/db/mek.bin", "chflags 0 /var/db/mbk.bin",
                "chflags 0 /var/db/juniper.conf.sha256",
                "rm -rf /var/db/mek.bin", "rm -rf /var/db/mbk.bin",
                "rm -rf /var/db/juniper.conf.sha256"]
    try:
        if chassis_cluster:
            node = kwargs.get('node', 'both')
            if node == 'node0' or node == 'both':
                for cmd in cmd_list:
                    device_handle.node0.shell(command=cmd)
            if node == 'node1' or node == 'both':
                for cmd in cmd_list:
                    device_handle.node1.shell(command=cmd)
        else:
            for cmd in cmd_list:
                device_handle.shell(command=cmd)
        result = True
    except Exception as except_error:
        raise Exception("Could not delete the Master Encryption Key. Error msg: "
                        + str(except_error))

    return result


# Method to delete all key-pairs in /var/db/certs/common/keypair
# ----------------------------------------------------------------
def delete_keypair(device_handle, **kwargs):
    """
    :param device_handle:
        **REQUIRED** device object
    :param  filetype:
        ***OPTIONAL***  possible values can be 'priv', 'privenc' or 'all'. Default is 'all'
    :param node:
        ***OPTIONAL*** can be 'node0', 'node1' or 'both' if device is in HA. Default is node0.

    :return: True if command is executed successfully

    Python Examples:
        delete_keypair(srx0)
        delete_keypair(srx0, node=node0)
        delete_keypair(srx0, node=node0), filetype=privenc
    Robot Examples:
        Delete Keypair    ${srx0}
        Delete Keypair    ${srx0}    node=node0
        Delete Keypair    ${srx0}    node=node0    filetype=privenc
    """
    chassis_cluster = _check_chassis_cluster(device_handle)
    filetype = kwargs.get('filetype', 'all')
    cmd_list = ["rm -rf /var/db/certs/common/key-pair *privenc",
                "rm -rf /var/db/certs/common/key-pair *priv"] if filetype == 'all' else \
                        ["rm -rf /var/db/certs/common/key-pair *%s" % filetype]

    if chassis_cluster:
        node = kwargs.get('node', 'both')
        if node == 'node0' or node == 'both':
            for cmd in cmd_list:
                device_handle.node0.shell(command=cmd)
        if node == 'node1' or node == 'both':
            for cmd in cmd_list:
                device_handle.node1.shell(command=cmd)
    else:
        for cmd in cmd_list:
            device_handle.shell(command=cmd)

    return True


# Method to fetch key-pair checksum
# ----------------------------------
def get_keypair_checksum(device_handle, filename, **kwargs):
    """
    :param device_handle:
        **REQUIRED** device object
    :param filename:
        **REQUIRED** name of encrypted key-pair file.
                    Possible values: <filename>.privenc or *privenc
                    Examples: filename=*priv, filename=r0__name.priv,
                              filename=*privenc, filename=r0__name.privenc
    :param path:
        ***OPTIONAL*** path to file can be specified. Default is /var/db/certs/common/key-pair/
    :param node:
        ***OPTIONAL*** can be 'node0' or 'node1' if device is in HA.
                        Default is node0. Example: node=node0

    :return: key-pair checksum for the file if filename is specifically provided,
            else it returns a list of checksums if the filename is given as *priv or *privenc.

    Python Examples:
        get_keypair_checksum(srx0, filename=*privenc)
        ### Mentioning filename beginning with * will return a list of
        checksums of all files of type privenc

        get_keypair_checksum(srx0, filename=r0__name.privenc, path=/var/db/certs/common/keypair)
        get_keypair_checksum(srx0, filename=*priv, path=/var/db/certs/common/keypair, node=node1)

    Robot Examples:
        Get Keypair Checksum    ${srx0}    filename=*privenc    node=node0
        Get Keypair Checksum    ${srx0}    filename=r0__name   path=/var/db/certs/common/keypair
    """
    chassis_cluster = _check_chassis_cluster(device_handle)
    path = kwargs.get('path', '/var/db/certs/common/key-pair/')
    checksum_list = []
    key_pair_list = []
    if chassis_cluster:
        node = kwargs.get('node', 'node0')
    if '*' in filename:
        if chassis_cluster:
            key_pair_list += list_keypair(device_handle, node=node, filetype='privenc')
        else:
            key_pair_list += list_keypair(device_handle, filetype='privenc')
        cmd_list = ['file checksum md5 ' + str(path) + ((str(key_pair)).lstrip(' '))
                    for key_pair in key_pair_list]
    else:
        cmd_list = ['file checksum md5 ' + str(path) + str(filename)]

    for cmd in cmd_list:
        if chassis_cluster:
            if node == 'node0':
                response = device_handle.node0.cli(command=cmd).response()
            if node == 'node1':
                response = device_handle.node1.cli(command=cmd).response()
        else:
            response = device_handle.cli(command=cmd).response()

        if re.search("No such file or directory.", str(response)):
            raise Exception("No such file or directory")
        else:
            checksum_list.append((str(str(response).split('=')[1])).lstrip(' '))

    return checksum_list[0] if len(checksum_list) == 1 else checksum_list


# Method to get TPM Status from device Cli
# ---------------------------------------------
def get_tpm_status(device_handle, **kwargs):
    """
        :param device_handle:
            **REQUIRED** device object

        :param parameter
            ***OPTIONAL*** specify the parameter name from table below
                           for which the status has to be fetched
            Parameter 	| Parameter as it appears on RE  |Possible status values
            ------------|--------------------------------|----------------------
            TPM			| Enabled						 | yes/ no
            MEK		    | Master Encryption Key			 | configured/ not-configured
            MBK			| Master Binding Key			 | created/ not-created

        :param node:
        ***OPTIONAL*** can be 'node0', 'node1' or 'both' if device is in HA.
                       Default is node0.

        :return dictionary with the parameter name and value if the parameter is not specified
                else only the status if the parameter is given as argument

        Python Examples:
            tpm_status = get_tpm_status (srx0)
            tpm_status = get_tpm_status (srx0, parameter=TPM)

        Robot Examples:
            tpm_status = Get Tpm Status     ${srx0}
            tpm_status = Get Tpm Status     ${srx0}    parameter=TPM
    """
    chassis_cluster = _check_chassis_cluster(device_handle)
    cmd = "show security tpm status"

    if chassis_cluster:
        node = kwargs.get('node', 'node0')
        if node == 'node0':
            xml_response = device_handle.node0.cli(command=cmd, format="xml").response()
        else:
            xml_response = device_handle.node1.cli(command=cmd, format="xml").response()
    else:
        xml_response = (device_handle.cli(command=cmd, format="xml")).response()

    xml_dict = (jxmlease.parse(xml_response))['rpc-reply']['tpm-status']
    tpm_status = {'TPM': str(xml_dict['tpm-enable-status']),
                  'MEK': str(xml_dict['tpm-master-encryption-key-status']),
                  'MBK': str(xml_dict['tpm-binding-key-status'])}

    return tpm_status[kwargs.get('parameter')] if 'parameter' in kwargs else tpm_status


# Method to list all key-pairs in /var/db/certs/common/keypair
# -------------------------------------------------------------
def list_keypair(device_handle, **kwargs):
    """
    :param device_handle:
        **REQUIRED** device object
    :param  filetype:
        ***OPTIONAL***  possible values can be 'priv', 'privenc' or 'all'. Default is 'all'.
    :param node:
        ***OPTIONAL*** can be 'node0' or 'node1' if device is in HA. Default is node0.

    :return: List of the filenames

    Python Examples:
        list_keypair(srx0)
        list_keypair(srx0, node=node0)
        list_keypair(srx0, node=node0), filetype=privenc
    Robot Examples:
        List Keypair    ${srx0}
        List Keypair    ${srx0}    node=node0
        List Keypair    ${srx0}    node=node0    filetype=privenc
    """
    chassis_cluster = _check_chassis_cluster(device_handle)
    filetype = kwargs.get('filetype', 'all')
    file_list=[]
    cmd_list = ["cd /var/db/certs/common/key-pair/", "ls *privenc",
                "ls *priv"] if filetype == 'all' else \
                        ["cd /var/db/certs/common/key-pair/", "ls *%s" %filetype]
    if chassis_cluster:
        node = kwargs.get('node', 'node0')
        if node == 'node0':
            for cmd in cmd_list:
                response = device_handle.node0.shell(command=cmd).response()
                file_list += response.split() if 'ls: No match.' not in str(response) else []
        if node == 'node1':
            for cmd in cmd_list:
                response = device_handle.node1.shell(command=cmd).response()
                file_list += response.split() if 'ls: No match.' not in str(response) else []
    else:
        for cmd in cmd_list:
            response = device_handle.shell(command=cmd).response()
            file_list += response.split() if 'ls: No match.' not in str(response) else []

    return [file_name.lstrip() for file_name in file_list]


# Method to set Master Encryption Password
# ---------------------------------------------
def set_mek(device_handle, new_pswd, **kwargs):
    """

    :param device_handle:
        **REQUIRED** device object
    :param new_pswd:
        ***REQUIRED*** New Master Encryption Password
    :param node:
        ***OPTIONAL*** can be 'node0', 'node1' or 'both' if device is in HA. Default is both.

    :return True if Master Encryption Password is set/changed successfully

    Python Examples:
        set_mek(srx0, new_pswd=xkjdfkejfns$@!)
        set_mek(srx0, new_pswd=xkjdfkejfns$@!, node=node0)

    Robot Examples:
        Set Mek    ${srx0}    new_pswd=xkjdfkejfns$@!
        Set Mek    ${srx0}    new_pswd=xkjdfkejfns$@!    node=node0
    """
    ha_dev = HA()
    chassis_cluster = _check_chassis_cluster(device_handle)
    cmd = 'request security tpm master-encryption-password set plain-text-password'

    if chassis_cluster:
        node = kwargs.get('node', 'both')
        node_list = ['node0', 'node1'] if node == 'both' else [node]
        for node in node_list:
            ha_dev.execute_cli_on_node(device=device_handle, node=node,
                                       command=cmd, pattern="password: ")
            ha_dev.execute_cli_on_node(device=device_handle, node=node,
                                       command=new_pswd, pattern="password: ")
            response = ha_dev.execute_cli_on_node(device=device_handle, node=node,
                                                  command=new_pswd)
            if re.search("successfully", (str(response)).lower()):
                result = True
            elif re.search("error: Passwords do not match", str(response)):
                raise Exception("error: Passwords do not match")
            elif re.search("Recommend at least length 12 and use of 3 character classes",
                           str(response)):
                raise Exception("error: Password does not meet required criteria.")
            else:
                raise Exception("Master Encryption Password could not be set")
    else:
        dev.execute_cli_command_on_device(device=device_handle,
                                          command=cmd, pattern="password: ")
        dev.execute_cli_command_on_device(device=device_handle,
                                          command=new_pswd, pattern="password: ")
        response = dev.execute_cli_command_on_device(device=device_handle,
                                                     command=new_pswd)
        if re.search("successfully", (str(response)).lower()):
            result = True
        elif re.search("error: Passwords do not match", str(response)):
            raise Exception("error: Passwords do not match")
        elif re.search("Recommend at least length 12 and use of 3 character classes",
                       str(response)):
            raise Exception("error: Password does not meet required criteria. "
                            "Recommend at least length 12 and use of 3 character classes")
        else:
            raise Exception("Master Encryption Password could not be set")

    return result



# Method to verify TPM Status on device Cli
# ---------------------------------------------------
def verify_tpm_status(device_handle, tpm_dict, **kwargs):
    """
    :param device_handle:
        ***REQUIRED*** device object
    :param tpm_dict:
        ***REQUIRED***
            dictionary with tpm status parameter as key and the expected status as value.
            Refer to table in get_tpm_status for possible parameter names and their status values
            Example: {TPM=enabled, MEK=configured, MBK=created}
    :param node:
        ***OPTIONAL*** can be 'node0', 'node1' or 'both' if device is in HA.
                       Default is both. node=node0

    :return: True if the status of the parameter given by user matches the actual status

    Python Examples:
        result = verify_tpm_status(srx0, tpm_dict = {TPM:yes})
        result = verify_tpm_status(srx0, tpm_dict = {TPM:yes, MEK:not-configured})

    Robot Example:
        &{tpm_dict} =  Create Dictionary    TPM=yes    MEK=not-configured
        result = Verify Tpm Status    ${srx0}    tpm_dict=${tpm_dict}
    """
    chassis_cluster = _check_chassis_cluster(device_handle)
    for item in tpm_dict.keys():
        if chassis_cluster:
            node = kwargs.get('node', 'both')
            if node == 'both':
                node0_result = True if str((get_tpm_status(device_handle, parameter=item,
                                                           node='node0'))) == str(tpm_dict[item]) else False
                node1_result = True if str((get_tpm_status(device_handle, parameter=item,
                                                           node='node1'))) == str(tpm_dict[item]) else False
                result = True if node0_result is True and node1_result is True else False
            else:
                result = True if str((get_tpm_status(device_handle, parameter=item,
                                                     node=node))) == str(tpm_dict[item]) else False
        else:
            result = True if str((get_tpm_status(device_handle,
                                                 parameter=item))) == str(tpm_dict[item]) else False
    return result


# Method to verify that all key-pairs in /var/db/certs/common/key-pair are encrypted
# --------------------------------------------------------------------------------------
def verify_keypair_is_encrypted(device_handle, **kwargs):
    """
    :param device_handle:
        ***REQUIRED*** device object
    :param node:
        ***OPTIONAL*** can be 'node0', 'node1' or 'both' if device is in HA.
                       Default is both. node=node0

    :return: True if key-pair is encrypted, else False

    Python Examples:
        verify_keypair_is_encrypted(srx0)
        verify_keypair_is_encrypted(srx0, node=node0)

    Robot Examples:
        Verify Keypair Is Encrypted    ${srx0}
        Verify Keypair Is Encrypted    ${srx0}    node=node0
    """
    chassis_cluster = _check_chassis_cluster(device_handle)
    result = False
    node0_list = []
    node1_list = []
    if chassis_cluster:
        node = kwargs.get('node', 'both')
        if chassis_cluster:
            if node == 'node0' or node == 'both':
                node0_list = str(device_handle.node0.shell(command=
                                                           "ls /var/db/certs/common/key-pair").response()).split()
            if node == 'node1' or node == 'both':
                node0_list = str(device_handle.node1.shell(command=
                                                           "ls /var/db/certs/common/key-pair").response()).split()
            key_pair_list = node0_list + node1_list
    else:
        key_pair_list = str(device_handle.shell(command=
                                                "ls /var/db/certs/common/key-pair").response()).split()

    for elem in key_pair_list:
        if str((elem.split('.'))[1]) == 'privenc':
            result = True
        else:
            break
    return result


def _check_chassis_cluster(handle):
    """
        This is a private method used by the library to check if the device is in HA/non-HA mode
        It returns True if the device is in HA and False if the device is in standalone
    """
    out = handle.cli(command="show chassis cluster status").response()
    return False if re.search("Chassis cluster is not enabled", str(out)) else True
