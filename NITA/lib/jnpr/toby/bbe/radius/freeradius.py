""" This module defines the FreeRADIUS class and class methods.
"""

from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.bbe.version import get_bbe_version
from jnpr.toby.bbe.errors import BBEConfigError
import datetime
import os
import re



__author__ = ['Dan Bond']
__contact__ = 'dbond@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()


class FreeRadius:
    """This class provides methods for configuring a FreeRadius server.

    The constructor requires the Toby-generated device handle as its only argument. The device handle is primarily
    used for sending configuration commands to the device.

    """

    def __init__(self, dev_handle):
        self.device_handle = dev_handle
        self.sbr = False
        if 'sbr' in dev_handle.get_model():
            self.sbr = True
            from ldap3 import Server, Connection, ALL
        self.host = dev_handle.current_node.current_controller.host
        if self.sbr:
            while True:
                try:
                    self.server = Server(self.host, port=667, get_info=ALL)
                    self.conn = Connection(self.server, 'cn=admin,o=radius', 'radius', version=2, auto_bind=True)
                    break
                except:
                    dev_handle.shell(command="/opt/JNPRsbr/radius/sbrd start")
                    resp = dev_handle.shell(command='ps aux |grep sbr.xml').resp
                    if not re.search(r'radius.*sbr.xml', resp):
                        raise Exception("failed to start SteelBelt radius before connection, please check the server")
        else:
            self.config_files = {"server": 'radiusd.conf',
                                 "clients": 'clients.conf',
                                 "users": 'users'}
            # self.sbin_directory = '/usr/local/sbin'
            self.config_directory = '/usr/local/etc/raddb'
            self.candidate_configs = {"server": '',
                                      "clients": '',
                                      "users": ''}
            cmd = dev_handle.shell(command="which radiusd").resp
            # For tolerance of mail output together with radius
            for line in cmd.split('\n'):
                if 'radiusd' in line:
                    cmd = line.strip()
                    break
            self.sbin = cmd
            resp = dev_handle.shell(command=cmd +" -v").resp
            match = re.match(r'.*Version\s(\d+).\d+.\d+', resp)
            if not match:
                raise Exception("not found radius version info")
            self.version = match.group(1)
            if self.version == '3':
                dev_handle.su()
                command = 'find / -name raddb |grep "etc/raddb" --color=never'
                resp = dev_handle.shell(command=command).resp
                if '/usr/local/etc/raddb' in resp:
                    self.config_directory = '/usr/local/etc/raddb'
                else:
                    self.config_directory = resp

                    # TODO: Check status of FTP, start if not running, fail if FTP can't be started

        # TODO: Check headers of config_files for different script ID. Issue warning if different than current run

        # TODO: Save config files to local log directory (involves FTP from host to machine running script).
        # Do we still want to do this?

        # TODO: Sanity check on existing config files (rs_init() for reference)
        # 5. Copy dictionary file from CVS repo (change to GIT?) unless user provides their own

    def start_radius_server(self):
        """ Starts FreeRadius process on the radius server.

        :return:
            True if radius server start command is issued on the server
            Throws BBEConfigError otherwise
        """
        # check if already root before su
        user = self.device_handle.shell(command='whoami')
        if 'root' not in user.resp:
            self.device_handle.su()
        if self.sbr:
            resp = self.device_handle.shell(command='ps aux |grep sbr.xml').resp
            if re.search(r'radius.*sbr.xml', resp):
                self.device_handle.shell(command="/opt/JNPRsbr/radius/sbrd restart")
            else:
                self.device_handle.shell(command="/opt/JNPRsbr/radius/sbrd start")
            resp = self.device_handle.shell(command='ps aux |grep sbr.xml').resp
            if not re.search(r'radius.*sbr.xml', resp):
                raise Exception("failed to start SteelBelt radius")
            else:
                pid = self.device_handle.shell(command='cat /opt/JNPRsbr/radius/radius.pid').resp.strip()
                t.log("Steel Belt radius is started, pid is {}".format(pid))
                return True
        # verify FreeRadius is running before starting
        pid = self.device_handle.shell(command='pgrep radius', timeout=10)
        if pid.resp != '':
            t.log('info', 'radius process already running as pid ' + pid.resp)
            return True
        else:
            radius_start_command = self.sbin + ' -d ' + self.config_directory

            # start the radius process
            reply = self.device_handle.shell(command=radius_start_command, timeout=60)
            if reply.resp != '':
                t.log('error', 'An unknown response was encountered while starting the radius process.' + reply.resp)
                raise BBEConfigError("Error while starting FreeRadius --- unknown response")

            # verify FreeRadius is running
            pid = self.device_handle.shell(command='pgrep radius', timeout=10)
            if pid.resp == '':
                t.log('error', 'Radius process failed to start!')
                raise BBEConfigError(
                    "Error while starting radius --- radiusd process is not running on " + self.device_handle.current_node.current_controller.host)
            else:
                t.log('info', 'Radius started as pid ' + pid.resp)
                return True

    def stop_radius_server(self):
        """ Stops FreeRadius process on the radius server.

        :return:
            True if radius server stop command is issued on the server
            Throws BBEConfigError otherwise
        """

        # check if already root before su
        user = self.device_handle.shell(command='whoami')
        if 'root' not in user.resp:
            self.device_handle.su()
        if self.sbr:
            self.device_handle.shell(command="/opt/JNPRsbr/radius/sbrd stop")
            resp = self.device_handle.shell(command='ps aux |grep sbr.xml').resp
            if re.search(r'radius.*sbr.xml', resp):
                raise Exception("failed to stop SteelBelt radius")
            else:
                t.log("steelbelt radius was shutdown")
                return True

        # Get process kill command
        pid = self.device_handle.shell(command='pgrep radius', timeout=10)

        # Verify FreeRadius is running before executing process kill
        if pid.resp == '':
            t.log('info', 'NO radius process found running!')
            return True
        else:
            radius_stop_command = 'kill -9 ' + pid.resp
            self.device_handle.shell(command=radius_stop_command, timeout=30)

            # check that the radius process has been killed
            pid = self.device_handle.shell(command='pgrep radius', timeout=10)
            if pid.resp == '':
                t.log('Radius process successfully terminated')
                return True
            else:
                raise BBEConfigError("radius process could not be terminated on " + self.device_handle.current_node.current_controller.host)

    def restart_radius_server(self):
        """ Restarts FreeRadius process on the radius server.

        :return:
            True if radius server stop command is issued on the server
            Throws BBEConfigError otherwise
        """
        if self.sbr:
            self.device_handle.su()
            self.device_handle.shell(command="/opt/JNPRsbr/radius/sbrd restart")
            pid = self.device_handle.shell(command='cat /opt/JNPRsbr/radius/radius.pid').resp.strip()
            if re.match(r'\d+', pid):
                t.log("Steel Belt radius is started, pid is {}".format(pid))
                return True
            else:
                raise Exception("failed to restart SteelBelt radius")
        status = self.stop_radius_server()
        # Check stop_radius() status
        if not status:
            t.log('error', 'Aborting restart_radius() due to a bad status return by stop_radius()')
            raise BBEConfigError("Error encountered while restarting FreeRadius process on " + self.device_handle.current_node.current_controller.host)
        else:
            status = self.start_radius_server()

        # Check start_radius() status
        if not status:
            t.log('error', 'Aborting restart_radius() due to a bad status return by start_radius()')
            raise BBEConfigError("Error encountered while restarting FreeRadius process on " + self.device_handle.current_node.current_controller.host)
        else:
            t.log('Radius process successfully restarted')
            return True

    def add_radius_user(self, user: str, request_avp: str, reply_avp: str, commit: bool, new=False):
        """Add radius user to the 'users' file on a FreeRadius server

        :param user:
            **REQUIRED** FreeRadius user string. Examples are DEFAULTUSER, WHOLESALEUSER, PPPWHOLESALEUSER
        :param request_avp:
            *OPTIONAL*
        :param reply_avp:
            *OPTIONAL*
        :param commit:
            *OPTIONAL* Boolean which sets whether added user is committed to file referenced by config_files["users"].
            If adding many users, you may want to consider setting commit to True on the last call to add_user().
        :return:
            True or False based on status of commit_file_on_radius_server() call. If user cannot be committed for
            any reason, add_user() returns False.
        """
        if self.sbr:
            request_avp = request_avp.strip()
            reply_avp = reply_avp.strip()
            avp_dict = {}
            for avp in re.split(r',\s|\n', reply_avp):
                pattern1 = re.compile(r'^\s+|\s+$|\"')
                avp = pattern1.sub('', avp)
                pattern2 = re.compile(r'\+=|:=|==')
                avp = pattern2.sub('=', avp)
                if len(avp.split('=')) != 2:
                    raise Exception("the reply attribute {} is not correct".format(avp))
                #pattern3 = re.compile(r'^\s+|\s+$|[\'\"]|[:]\d+')
                pattern3 = re.compile(r'^\s+|\s+$|[\'\"]')
                avp_key = pattern3.sub('', avp.split('=')[0])
                if avp_key in ['Auth-Type', 'Service-Type', 'Fall-Through']:
                    t.log("ignore the attribute {}".format(avp))
                    continue
                avp_key = re.sub(r'X-Ascend-Data-Filter', 'Ascend-Data-Filter', avp_key)
                avp_key = re.sub(r'ERX-Service-AcctInt:', 'Unisphere-Service-AcctInt-tag', avp_key)
                avp_key = re.sub(r'ERX-Service-Activate:', 'Unisphere-Activate-Service-tag', avp_key)
                avp_key = re.sub(r'ERX-Service-Deactivate', 'Unisphere-Deactivate-Service', avp_key)
                avp_key = re.sub(r'ERX-Service-Statistics:', 'Unisphere-Service-Stats-tag', avp_key)
                avp_key = re.sub(r'ERX-Egress-Policy-Name', 'Unisphere-Egress-Policy-Name', avp_key)
                avp_key = re.sub(r'ERX-Ingress-Policy-Name', 'Unisphere-Ingress-Policy-Name', avp_key)
                avp_value = pattern1.sub('', avp.split('=')[1])
                if avp_key in avp_dict:
                    avp_dict[avp_key].append(avp_value)
                else:
                    avp_dict[avp_key] = [avp_value]

            password = 'joshua'
            match = re.search(r'User-Password[\s]*:?[=]+[\s]*[\"]?([\w\d]*)', request_avp)
            if match:
                password = match.group(1)
            userstring = "radiusname={},radiusclass=Native-User,o=radius".format(user)
            if self.conn.search('radiusclass=Native-User,o=radius', '(radiusname={})'.format(user)):
                t.log("user {} already exist in server, will delete it first ".format(user))
                self.conn.delete(userstring)

            attributes = {'objectclass':['top', 'Native-User', 'user'], 'password':['{x-clear}'+password],
                          'description':['Created by automation.'], 'radiusname':[user], 'login-limit':['none']}
            try:
                self.conn.add(userstring, attributes=attributes)
                ## to add avps
                self.conn.add("radiuslist=reply,"+userstring, object_class="radiuslist", attributes=avp_dict)
            except:
                t.log("failed to add user {} or its attributes {}".format(user, avp_dict))
                return False
            t.log("user {} or its attributes {} was added successfully".format(user, avp_dict))
            return True

        # TODO: Create a backup of users

        # Instantiate config_string and remove trailing/leading whitespace from avp strings
        config_string = user + "\t"
        file_path = self.config_directory + '/' + self.config_files["users"]
        request_avp = request_avp.strip()
        reply_avp = reply_avp.strip()

        # Parse request_avp
        for line in request_avp.splitlines():
            line = line.strip()
            if self.version == '3'and 'User-Password' in line:
                line = re.sub('User-Password', 'Cleartext-Password', line)
            config_string += line

        # Parse reply_avp
        config_string += "\n"  # Put a newline before concatenating reply_avp
        for line in reply_avp.split(sep=", "):
            line = line.strip()
            config_string = config_string + "\t" + line + ",\n"

        config_string = reverse_replace(config_string, ",", "", 1)  # Remove trailing separator (comma) if any

        # Commit changes to users
        # TODO: Allow for candidate configs. This means modifying commit_file_on_radius_server() param 'new'
        if commit:
            self.set_radius_users_candidate_config(config=config_string, new=False)
            status = self.commit_file_on_radius_server(host_name=self.host, config=self.candidate_configs["users"],\
                     new=new, file_name=file_path)
            self.set_radius_users_candidate_config(config='', new=True)
        else:
            self.set_radius_users_candidate_config(config=config_string, new=new)
            t.log('Commit set to false, so user has been added to candidate config')
            return True

        if status:
            t.log('add_user() successful. Change successfully committed to users')
            return True
        else:
            t.log('error', 'add_user() failed! Change to users could not be saved due to a failed '
                           'commit_file_on_radius_server()')
            return False

    def commit_radius_user(self, new=False):
        """Add radius user to the 'users' file on a FreeRadius server

        :return:
            True or False based on status of commit_file_on_radius_server() call. If user cannot be committed for
            any reason, add_user() returns False.
        """
        if self.sbr:
            return
        file_path = self.config_directory + '/' + self.config_files["users"]
        status = self.commit_file_on_radius_server(host_name=self.host, config=self.candidate_configs["users"],\
                 new=new, file_name=file_path)
        self.set_radius_users_candidate_config(config='', new=True)

        if status:
            t.log('commit_user() successful. Change successfully committed to users')
            return True
        else:
            t.log('error', 'commit_user() failed! Change to users could not be saved due to a failed '
                           'commit_file_on_radius_server()')
            return False

    def delete_radius_user(self, user: str):
        """This method deletes a user from the FreeRADIUS's users file

        :param user:
            **REQUIRED**            Name of the user you want to delete. Example: 'DEFAULTUSER'
        :return:
        """
        if self.sbr:
            userstring = "radiusname={},radiusclass=Native-User,o=radius".format(user)
            try:
                self.conn.delete(userstring)
            except:
                t.log('ERROR', "failed to delete user {}".format(user))
                return False
            t.log("user {} was deleted successfully".format(user))
            return True

        # Open file and read into a list of strings
        file_path = self.config_directory + "/" + self.config_files["users"]
        ssh_connection = SshConn(host=self.host, user='root', password='Embe1mpls')
        sftp_client = ssh_connection.open_sftp()

        with sftp_client.open(file_path) as users_file:
            config_strings = users_file.readlines()

        # Verify that param 'user' exists in 'config_strings'
        user_key = [item for item in config_strings if user in item]

        if user_key.__len__() < 1:
            t.log('error', 'The user you requested to delete was not found in: ' + file_path)
            return False

        # TODO: This is a stupidly obfuscated way of dealing with radius user strings which are subsets
        # TODO: (cont) of one another (i.e. DEFAULT and DEFAULTUSER). Consider rewriting for clarity
        if user_key.__len__() > 1:
            for item in user_key:
                split_list = item.split()
                if user in split_list:
                    user_key = item

        # Generate dictionary which associates tabbed reply_avp attributes with line containing the radius user string
        # and request_avp attributes
        current_key = ""
        user_dictionary = dict()
        for item in config_strings:
            if not item.startswith("\t"):
                current_key = item
                user_dictionary[item] = []
            else:
                user_dictionary[current_key].append(item)

        # Iterate over strings until 'user' is found. Remove this entry.
        user_key_to_remove = ''.join(user_key)
        config_strings.remove(user_key_to_remove)
        # Remove entries associated with 'user' by referencing generated dictionary
        for item in user_dictionary[user_key_to_remove]:
            config_strings.remove(item)

        # TODO: Cleanup leading newlines in new config_strings, dump list contents into 'config'
        config = ''

        status = self.commit_file_on_radius_server(host_name=self.host, config=config, new=True, file_name=file_path)
        if status:
            t.log('delete_user() successful. Change successfully committed to users.')
            return True
        else:
            t.log('error', 'delete_user() failed! Change to users could not be saved due to a failed '
                           'commit_file_on_radius_server()')
            return False

    def add_radius_client(self, client: str, secret: str, short_name: str, commit=True, new=False, **kwargs):
        """This method adds a client to the FreeRADIUS's clients.conf file

        :param client:
            **REQUIRED** Hostname or IP of RADIUS client
        :param secret:
            **REQUIRED** The shared secret used to "encrypt" and "sign" packets between NAS and FreeRADIUS
        :param short_name:
            **REQUIRED** The short name is used as an alias for the fully qualified domain name, or the IP address
        :param commit:
            *OPTIONAL* If set to True or not specified, update clients.conf immediately. If set to false, changes
            are made only to the local work file, awaiting a subsequent commit_file_on_radius_server() call to push
            changes
        :param new:
            *OPTIONAL* If this is True, then this method will create a new clients.conf with only the newly added
            entries. By default this knob is false and script will maintain all original data in clients.conf
        :param kwargs:
        nastype:
            *OPTIONAL*
        password:
            *OPTIONAL*
        login:
            *OPTIONAL*
        :return:
            True if the client is added to clients.conf, False in all other cases
        """
        if self.sbr:
            server_ldap_entry = "radiusname={},radiusclass=Client,o=radius".format(short_name)
            if self.conn.search('radiusclass=Client,o=radius', '(radiusname={})'.format(short_name)):
                if not new:
                    t.log("radius client {} already exists".format(short_name))
                    return True
                else:
                    t.log("remove existing client first")
                    self.conn.delete(server_ldap_entry)
            try:
                self.conn.add(server_ldap_entry, attributes={'objectclass': ['top', 'Client'],
                                                             'radiusname': [short_name], 'ip-address-range': ['1'],
                                                             'inactivity-timeout': ['0'], 'product': ['Juniper-ERX'],
                                                             'shared-secret': [secret], 'ip-address': client})
            except:
                raise Exception("failed to add radius client {}".format(short_name))
            t.log("radius client {} was added successfully".format(short_name))
            return True
        # TODO: Create a backup of clients.conf

        # Initialize config string by creating client stanza
        config_string = 'client ' + client + " { \n"
        config_string += "\tsecret    = " + secret + "\n"
        config_string += "\tshortname = " + short_name + "\n"

        # Check status of optional arguments and append config as needed
        if 'nastype' in kwargs:
            nastype = kwargs['nastype']
            config_string += "\tnastype   = " + nastype + "\n"
        if 'password' in kwargs:
            password = kwargs['password']
            config_string += "\tpassword  = " + password + "\n"
        if 'login' in kwargs:
            login = kwargs['login']
            config_string += "\tlogin     = " + login + "\n"

        config_string += "}\n"

        # Commit changes to clients.conf
        file_path = self.config_directory + '/' + self.config_files["clients"]

        # TODO: Allow for candidate configs. This means modifying commit_file_on_radius_server() param 'new'
        if commit:
            status = self.commit_file_on_radius_server(host_name=self.host, config=config_string, new=new,
                                                       file_name=file_path)
        else:
            t.log('Commit set to false, so client has been added to candidate config')
            # TODO: Append candidate config
            return True

        if status:
            t.log('add_client() successful. Change successfully committed to clients.conf')
            return True
        else:
            t.log('error', 'add_client() failed! Change to clients.conf could not be saved due to a failed '
                           'commit_file_on_radius_server()')
            return False

    def modify_radius_auth(self, auth_order):
        """
        only work for sbr
        :param auth_order:  e.g. 'Native-User;Unix-User'
        :return:
        """
        if self.sbr:
            self.conn.modify('radiusclass=server,o=radius', {'auth-methods':[('MODIFY_REPLACE', [auth_order])]})

    def delete_radius_client(self, client: str):
        """This method deletes a client from the FreeRADIUS file clients.conf

        :param client:
            **REQUIRED** Name of the client you want to delete from clients.conf
        :return:
            True if the radius client is successfully deleted. False otherwise. If there are issues operating on the
            file, an Exception may be thrown before False can be returned.
        """
        if self.sbr:
            if self.conn.delete('radiusname={},radiusclass=Client,o=radius'.format(client)):
                t.log("radius client {} was removed".format(client))
                return True
            else:
                return False
        # Open file and read into a list of strings
        file_path = self.config_directory + "/" + self.config_files["clients"]
        ssh_connection = SshConn(host=self.host, user='root', password='Embe1mpls')
        sftp_client = ssh_connection.open_sftp()

        with sftp_client.open(file_path) as clients_file:
            config_strings = clients_file.readlines()

        # Verify that param 'user' exists in 'config_strings'
        client_key = [item for item in config_strings if client in item]
        if client_key.__len__() < 1:
            t.log('error', 'The user you requested to delete was not found in: ' + file_path)
            return False

        # TODO: This is a stupidly obfuscated way of dealing with user strings which are subsets
        # TODO: (cont) of one another (i.e. DEFAULT and DEFAULTUSER). Consider rewriting for clarity
        if client_key.__len__() > 1:
            for item in client_key:
                split_list = item.split()
                if client in split_list:
                    client_key = item

        # Generate dictionary which associates tabbed client attributes with line containing the client string
        current_key = ""
        client_dictionary = dict()
        for item in config_strings:
            if not item.startswith("\t") and not item.startswith("}"):
                current_key = item
                client_dictionary[item] = []
            else:
                client_dictionary[current_key].append(item)

        # Iterate over strings until 'user' is found. Remove this entry.
        client_key_to_remove = ''.join(client_key)
        config_strings.remove(client_key_to_remove)
        # Remove entries associated with 'user' by referencing generated dictionary
        for item in client_dictionary[client_key_to_remove]:
            config_strings.remove(item)

        # Dump list contents into 'config' and commit to clients.conf
        config = ''.join(config_strings)

        # TODO: Prepend the config with some script watermark
        status = self.commit_file_on_radius_server(host_name=self.host, config=config, new=True, file_name=file_path)
        if status:
            t.log('delete_client() successful. Change successfully committed to clients.conf')
            return True
        else:
            t.log('error', 'delete_client() failed! Change to clients.conf could not be saved due to a failed '
                           'commit_file_on_radius_server()')
            return False

    # def change_of_authorization_radius_server(self):
    #     """Performs change of authorization action
    #
    #     :return:
    #     """
    #
    #     return True
    #
    # def cleanup_radius_server(self):
    #     """Cleanup radius server
    #
    #     :return:
    #     """
    #     return True

    def commit_file_on_radius_server(self, host_name, config, new, file_name):
        """Commits changes in 'config' string to a new file, or appends an existing one

        :param host_name:
            **REQUIRED** Full hostname of device which has the file you want to modify
        :param config:
            **REQUIRED** String containing config you want to commit
        :param new:
            *OPTIONAL* Boolean indicating whether you want to create a new file or append an existing one
        :param file_name:
            **REQUIRED** File name (full path on the device) that you wish to modify
        :return:
            True if write operation is successful
            False otherwise
        """
        # Establish SshConn for remote file operations. Write config to specified file
        if self.sbr:
            return
        if not self.host:
            raise BBEConfigError("Attempting to commit config with undefined hostname!")
        else:
            ssh_connection = SshConn(host=host_name, user='root', password='Embe1mpls')
            sftp_client = ssh_connection.open_sftp()

        # Conditional to select between new file or append existing
        if new:
            t.log('Committing config to new file: ' + file_name)
            users_file_handle = sftp_client.open(file_name, mode='w')
        else:
            t.log('Committing config to existing file: ' + file_name)
            users_file_handle = sftp_client.open(file_name, mode='a')

        # Write to file
        try:
            users_file_handle.write(config)
        finally:
            users_file_handle.close()

        # verify config was added to the saved file
        users_file_handle = sftp_client.open(file_name)
        # convert bytestring back to str for compare
        radius_config = users_file_handle.read().decode('utf-8')

        if config not in radius_config:
            t.log('error', 'Commit failed! Config not found in {0}'.format(file_name))
            t.log('debug', 'expected: {0} \n found: {1}'.format(config, radius_config))
            return False

        return True

    # def disconnect_radius_server(self):
    #     """Issues command to disconnect FreeRADIUS server.
    #
    #     :return:
    #     """
    #     return True
    #
    # def get_user_from_radius_server(self):
    #     """Returns specified user from the FreeRADIUS server
    #
    #     :return:
    #     """
    #     return True
    #
    # def radzap(self):
    #     """Radzap
    #
    #     :return:
    #     """
    #     return True
    #
    # def set_udp_port_on_radius_server(self):
    #     """Sets UDP port for FreeRADIUS server
    #
    #     :return:
    #     """
    #     return True
    #
    # def get_radius_version(self):
    #     """Acquires FreeRADIUS version running on the server
    #
    #     :return:
    #     """
    #     return True
    #
    # def load_dictionary_to_radius(self):
    #     """Loads the default dictionary to FreeRADIUS server
    #
    #     :return:
    #     """
    #     return True
    def set_file_watermark(self, file: str):
        """Prepends a file on a FreeRADIUS server with a watermark containing user, script, and time information.

        :param file:
            **REQUIRED** Full file path of the file you would like to watermark.
        :return:
            True if file write is successful, false otherwise.
        """

        # Acquire filename, username, and timestamp
        # TODO: Test with Builtin generated from Robot
        # suite_file = BuiltIn().get_variables()['${SUITE_SOURCE}']
        suite_file = "my_sample_script.robot"
        user = os.getenv('USER')
        time = datetime.datetime.now()

        watermark = "# File modified by: " + user + "\n"
        watermark += "# Script: " + suite_file + "\n"
        watermark += "# Time: " + str(time) + "\n\n"

        # TODO: Prepend file with watermark
        ssh_connection = SshConn(host=self.host, user='root', password='Embe1mpls')
        sftp_client = ssh_connection.open_sftp()

        with sftp_client.open(file, mode='r') as handle:
            previous_contents = handle.read()

        # TODO: Parse previous contents for another watermark. If there is a user mismatch, issue warning and proceed

        with sftp_client.open(file, mode='w') as handle:
            handle.write(watermark)
            handle.write(previous_contents)

        return True

    # Helper/Access methods
    def get_radius_configuration_filename(self):
        """Returns filename for FreeRADIUS file 'radiusd' (in case default name is overwritten)

        :return:
        """
        return self.config_files['server']

    def get_radius_clients_configuration_filename(self):
        """Returns filename for FreeRADIUS file 'clients.conf' (in case default name is overwritten)

        :return:
        """
        return self.config_files['clients']

    def get_radius_users_configuration_filename(self):
        """Returns filename for FreeRADIUS file 'users' (in case default name is overwritten)

        :return:
        """
        return self.config_files['users']

    def set_radius_users_candidate_config(self, config: str, new: bool):
        """Maintains the candidate config for FreeRADIUS file 'users'

        :param config:
            **REQUIRED** String you want to add to 'users' candidate config
        :param new:
            **REQUIRED** Boolean True/False. If True, current 'users' will be overwritten. If False, config is
            added to current candidate config contents.
        :return:
            True when candidate config has been updated.
        """
        if new:
            self.candidate_configs["users"] = config
        else:
            self.candidate_configs["users"] += config
        return True

    def get_radius_users_candidate_config(self):
        """Returns candidate config for FreeRADIUS file 'users'

        :return:
        """
        return self.candidate_configs["users"]

    def set_radius_clients_candidate_config(self, config: str, new: bool):
        """Maintains the candidate config for FreeRADIUS file 'clients.conf'

        :param config:
            **REQUIRED** String you want to add to 'clients.conf' candidate config
        :param new:
            **REQUIRED** Boolean True/False. If True, current 'clients.conf' will be overwritten. If False, config is
            added to current candidate config contents.
        :return:
            True when candidate config has been updated.
        """
        if new:
            self.candidate_configs["clients"] = config
        else:
            self.candidate_configs["clients"] += config
        return True

    def get_radius_clients_candidate_config(self):
        """Returns candidate config for FreeRADIUS file 'clients.conf'

        :return:
        """
        return self.candidate_configs["clients"]

    def set_radius_candidate_config(self, config: str, new: bool):
        """Maintains the candidate config for FreeRADIUS file 'radius.conf'

        :param config:
            **REQUIRED** String you want to add to 'radiusd.conf' candidate config
        :param new:
            **REQUIRED** Boolean True/False. If True, current 'radiusd.conf' will be overwritten. If False, config is
            added to current candidate config contents.
        :return:
            True when candidate config has been updated.
        """
        if new:
            self.candidate_configs["server"] = config
        else:
            self.candidate_configs["server"] += config
        return True

    def get_radius_candidate_config(self):
        """Returns candidate config for FreeRADIUS file 'radiusd'

        :return:
        """
        return self.candidate_configs["server"]


def reverse_replace(item: str, old: str, new: str, occurrence: int):
    """Performs a reverse replace (starts from the end of the string) and replaces 'old' with
    'new'. Can specify 'occurrences' to select number of replacements made.

    :param item: String you want to operate on
    :param old: Character string that you want removed
    :param new: Character string that you want to replace 'old'
    :param occurrence: Number of occurrences of 'old removed from 'item' that are replaced with 'new'
    :return: String with 'new' substituted where 'old' used to be.
    """
    intermediate_string = item.rsplit(old, occurrence)
    return new.join(intermediate_string)
