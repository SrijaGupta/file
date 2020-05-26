import os
import re
import time

class Strongswan:
    """
        Class Factory for strongswan
    """
    def __init__(self, linux_handle, **kwargs):
        """
            :param linux_handle:
                **REQUIRED** linux handle where strongswan is installed
            :param kwargs: connection_name:
                **REQUIRED* ipsec connection name
            :return class instance
            EXAMPLE::

                Python:
                   sobj = Strongswan(linux_handle, connection_name='net-net')
                ROBOT:
                   ${sobj} =  create strongswan object  linux_handle  connection_name=mytest
        """
        self.linux_handle = linux_handle
        if not 'connection_name' in kwargs:
            raise Exception("Mandatory argument 'connection_name' missing")
        self.conn_name = kwargs.get('connection_name')
        #import sys, pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        self.linux_handle.log("Switching user to root")
        self.linux_handle.su()
        self.linux_handle.log("Getting conf dir")
        self.conf_dir = self.linux_handle.shell(command='ipsec --confdir').response().rstrip()

    def create_ipsec_conf(self, **kwargs):
        """
            Creates  ipsec.conf for strongSwan

            :param ipsec_conf_dict
                **REQUIRED** ipsec config parameters as dictonary
            :param append
                *OPTIONAL*  append to the existing ipsec.conf file
                Default: 0 , Supported values 0/1
            :return True on success
                Raise exception on failure
            EXAMPLE::

                Python:
                   Sample user dict and connection_name=mytest
                   user_dict = {'leftsubnet': '10.1.0.0/16',
                     'leftcert': 'moonCert.pem',
                     'leftid': '@moon.strongswan.org',
                     'right': '%any',
                     'auto': 'add'
                     }
                   sobj.create_ipsec_conf(ipsec_conf_dict=user_dict)
                ROBOT:
                  &{user_dict} = leftsubnet=10.1.0.0/16  leftcert=moonCert.pem  leftid=@moon.strongswan.org right=%any auto=add
                  sobj.create_ipsec_conf(ipsec_conf_dict=user_dict)
                  generate ipsec conf  ${sobj}  append=1  ipsec_conf_dict=&{user_dict}

                ipsec.conf file will be created as below
                config setup
                   cachecrls=yes
                   strictcrlpolicy=yes

                conn %default
                       keyingtries=1
                       keyexchange=ikev2

                conn roadwarrior
                       leftsubnet=10.1.0.0/16
                       leftcert=moonCert.pem
                       leftid=@moon.strongswan.org
                       right=%any
                       auto=add

                For different key values refer to
                https://wiki.strongswan.org/projects/strongswan/wiki/ConnSection
        """

        crl_check = kwargs.get('crl_check', 1)
        if crl_check:
            default_ipsec_conf = {
                                'config setup': {
                                    'cachecrls': 'yes',
                                    'strictcrlpolicy': 'yes'
                                },
                                'conn %default': {
                                    'keyingtries': '1',
                                    'keyexchange': 'ikev2'
                                }
            }
        else:
            default_ipsec_conf = {
                                'config setup': {
                                    'cachecrls': 'no',
                                    'strictcrlpolicy': 'no'
                                },
                                'conn %default': {
                                    'keyingtries': '1',
                                    'keyexchange': 'ikev2'
                                }
            }
        #self.linux_handle.log("Switching user to root")
        #self.linux_handle.su(password='Embe1mpls')
        self.conf_path = self.conf_dir + '/ipsec.conf'
        if 'ipsec_conf_dict' not in kwargs:
            raise Exception("ipsec_dict is a mandatory argument")
        self.ipsec_dict = kwargs.get('ipsec_conf_dict')
        append = kwargs.get('append', 0)
        user_config = 'conn ' + self.conn_name

        if append:
            dict_from_file = self._create_dict_from_file()
            if user_config in dict_from_file:
                for key, value in self.ipsec_dict.items():
                    dict_from_file[user_config][key] = value
            else:
                dict_from_file[user_config] = self.ipsec_dict
            default_ipsec_conf = dict_from_file
        else:
            default_ipsec_conf[user_config] = self.ipsec_dict

        result = self.linux_handle.shell(command='ls ' + self.conf_path).response()
        if not re.search(r'No such file or directory', result):
            self.linux_handle.log("Moving existing %s to %s.orig" %(self.conf_path, self.conf_path))
            cmd = "mv -f %s %s.orig" %(self.conf_path, self.conf_path)
            self.linux_handle.shell(command=cmd)


        self.linux_handle.log("creating %s with provided parameters: %s" %(self.conf_path, default_ipsec_conf))
        with open('ipsec.conf', 'w') as out:
            out.write('# ipsec.conf - strongSwan IPsec configuration file\n')
            for key, value in default_ipsec_conf.items():
                out.write(key + "\n")
                for child_key, child_value in default_ipsec_conf[key].items():
                    out.write("\t\t" + child_key + "=" + child_value + "\n")
        out.close()

        if not self.linux_handle.upload(local_file='ipsec.conf', remote_file=self.conf_path, protocol='scp', user='root', password='Embe1mpls'):
            self.linux_handle.log("Uploading ipsec.conf file failed")
            raise Exception("Uploading ipsec.conf file failed")

        return True

    def ipsec_up(self, **kwargs):
        """
            Will start ipsec on Strongswan
            :param connection_name
                *OPTIONAL* ipsec connection name to start
                Default will take from the connection name provided in init
            :param restart
                *OPTIONAL* restart ipsec before making up
                Default: 1, supported values 1/0
            :param  timeout
                *OPTIONAL*  timeout for ipsec up.
                Default 60 secs
            :return True on success
              Raise exception on failure
            EXAMPLE::

              Python:
                 sobj.ipsec_up()
              ROBOT:
                 ipsec up  ${sobj}
        """

        conn_name = kwargs.get('connection_name', self.conn_name)
        restart = int(kwargs.get('restart', 1))
        timeout = kwargs.get('timeout', 60)
        starter = '/var/run/starter.charon.pid'
        #import sys, pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        result = self.linux_handle.shell(command='ls ' + starter).response()
        if  not re.search(r'No such file or directory', result) and restart:
            self.linux_handle.log("Restarting ipsec")
            result = self.linux_handle.shell(command="ipsec restart").response()
            if re.search(r'unable to start|error', result):
                self.linux_handle.log(level='ERROR', message='ipsec restart failed: ' + result)
                raise Exception('ipsec start failed: ' + result)
            self.linux_handle.log("Restarted ipsec: " + result)
        elif re.search(r'No such file or directory', result):
            self.linux_handle.log("Ipsec not running starting ipsec")
            result = self.linux_handle.shell(command="ipsec start").response()
            if re.search(r'unable to start|error', result):
                self.linux_handle.log(level='ERROR', message='ipsec start failed: ' + result)
                raise Exception('ipsec start failed: ' + result)
            self.linux_handle.log("started ipsec: " + result)
        time.sleep(10)

        cmd = 'ipsec up ' + conn_name
        self.linux_handle.log("Running ipsec up : " + cmd)
        result = self.linux_handle.shell(command=cmd, timeout=timeout).response()
        if re.search(r'connection .* successfully', result):
            self.linux_handle.log("ipsec up successful: " + result)
            return True
        else:
            self.linux_handle.log(level='ERROR', message='ipsec up failed: ' + result)
            raise Exception('ipsec up failed: ' + result)


    def ipsec_down(self, **kwargs):
        """
            Stops ipsec connection by running "ipsec down <connname>"

            :param connection_name
                *OPTIONAL* ipsec connection name to start
                Default will take from the connection name provided in init
            :return True on success
              Raise exception on failure
            EXAMPLE::

              Python:
                 sobj.ipsec_down()
              ROBOT:
                 ipsec down  ${sobj}
        """

        conn_name = kwargs.get('connection_name', self.conn_name)
        cmd = 'ipsec down ' + conn_name
        self.linux_handle.log("Stoping ipsec connection : " + cmd)
        result = self.linux_handle.shell(command=cmd).response()
        if re.search(r'successfully', result):
            self.linux_handle.log("ipsec connection closed successful: " + result)
            return True
        else:
            self.linux_handle.log(level='ERROR', message='ipsec stop connection failed: ' + result)
            raise Exception('ipsec stop failed: ' + result)

    def ipsec_status_check(self, **kwargs):
        """
            Checks ipsec status
            :param pattern
                *OPTIONAL*  string to grep from status output.
                Default: INSTALLED
            :param connection_name
                *OPTIONAL* ipsec connection name to start
                Default will take from the connection name provided in init
            :param err_level
                *OPTIONAL* Error level, used in case of negative test case
                Default: ERROR, Supported : INFO, DEBUG
            :return: True on success
              Raise exception on failure
            EXAMPLE::

              Python:
                 sobj.ipsec_status_check()
              ROBOT:
                 ipsec status check  ${sobj}
        """

        pattern = kwargs.get('pattern', 'INSTALLED')
        err_level = kwargs.get('err_level', 'ERROR')
        cmd = 'ipsec status ' + self.conn_name + ' |grep -i ' + pattern
        result = self.linux_handle.shell(command=cmd).response()
        if re.search(r"%s" %pattern, result):
            self.linux_handle.log("Connection up: " + result)
            return True
        else:
            self.linux_handle.log(level=err_level, message='connection not up: ' + result)
            raise Exception('connection not up: ' + result)


    def add_ipsec_secrets(self, **kwargs):
        """
             Adds given data to secrets file

             :param: auth_type
                **REQUIRED**  Authentication type to add

                Supported Values PSK/RSA/ECDSA

             For PSK host_id  or peer_id are mandatory

             :param  preshared_key
                **REQUIRED**  pre shared key to be updated

             :param host_id:
                 *OPTIONAL*  ip address

             :param peer_id
                 *OPTIONAL*  ip address

             For RSA and ECDSA below is mandatory

             :param local_cert
                 *OPTIONAL* Local certificate name

             : param passphrase
                 *OPTIONAL* key password for local cert

             :param xauth_user
                 *OPTIONAL* xauth username

             :param xauth_pwd
                 *OPTIONAL* xauth password

            :return:
                 True on Success

                 Raise exception on failure

             EXAMPLE::

               Python:
                 sobj.add_ipsec_secrets(auth_type='PSK', preshared_key='ike123', host_id='11.0.1.1', peer_id='11.0.1.2')

        """

        if 'auth_type' not in kwargs:
            self.linux_handle.log(level='ERROR', message="Mandatory Argument 'auth_type' is missing")
            raise Exception("Mandatory Argument 'auth_type' is missing")
        auth_type = kwargs.get('auth_type')
        ipsec_secret_file = self.conf_dir + '/ipsec.secrets'
        result = self.linux_handle.shell(command='ls ' + ipsec_secret_file).response()
        if not re.search(r'No such file or directory', result):
            self.linux_handle.log("Moving existing %s to %s.orig" % (ipsec_secret_file, ipsec_secret_file))
            cmd = "mv -f %s %s.orig" % (ipsec_secret_file, ipsec_secret_file)
            self.linux_handle.shell(command=cmd)
        line = ''
        if auth_type.lower() == 'PSK'.lower():
            if 'preshared_key' not in kwargs:
                self.linux_handle.log(level='ERROR', message="For auth_type=psk, argument 'preshared_key' is mandatory")
                raise Exception("Missing argument: For auth_type=psk, argument 'preshared_key' is mandatory")
            if 'host_id' in kwargs:
                line = kwargs.get('host_id') + ' '
            if 'peer_id' in kwargs:
                line = line + ' ' + kwargs.get('peer_id') + ' '
            line = line + '  :  PSK "' + kwargs.get('preshared_key') + '"'
        else:
            if 'local_cert' not in kwargs:
                self.linux_handle.log(level='ERROR', message=" 'local_cert' is mandatory argument")
                raise Exception("'local_cert' is mandatory argument")
            line = ' : ' +  auth_type.upper() + ' ' + kwargs.get('local_cert')
            if 'passphrase' in kwargs:
                line = line + ' ' + kwargs.get('passphrase')
        self.linux_handle.log('Adding %s into secrets file' %line)

        xauth = None
        if 'xauth_user' in kwargs and 'xauth_pwd' in kwargs:
            xauth = kwargs.get('xauth_user') + ' : XAUTH ' + kwargs.get('xauth_pwd')

        with open('ipsec.secrets', 'w') as out:
            out.write(line + "\n")
            if xauth is not None:
                out.write(xauth + "\n")
        out.close()

        if not self.linux_handle.upload(local_file='ipsec.secrets', remote_file=ipsec_secret_file,
                                        protocol='scp'):
            self.linux_handle.log("Uploading ipsec.secrets file failed")
            raise Exception("Uploading ipsec.secrets file failed")

        self.linux_handle.log("Updating ipsec.secrets file successfull")
        return True

    def _create_dict_from_file(self, **kwargs):
        """
           Internal funtion created dict from ipsec.conf file
        """

        if not self.linux_handle.download(local_file='ipsec.conf', remote_file=self.conf_path, protocol='scp'):
            self.linux_handle.log("Downloading ipsec.conf file failed")
            raise Exception("Downloading ipsec.conf file failed ")
        self.linux_handle.log("Reading ipsec.conf file")
        try:
            with open('ipsec.conf', 'r') as f:
                lines = f.readlines()
        except  Exception as err:
            self.linux_handle.log(level='ERROR', messsage="Unable to open file ipsec.conf")
            raise err
        ipsec_conf_dict = dict()
        line_key = ''
        for line in lines:
            line = line.strip()
            if re.match('#', line) or not line:
                next
            elif re.match('conn ', line) or re.match('config setup', line):
                # (conn_string, conn_name) = line.split()
                ipsec_conf_dict[line] = dict()
                line_key = line
            elif re.search('=', line):
                (key, value) = line.split('=', 1)
                ipsec_conf_dict[line_key][key] = value
            else:
                print("\n None matched line: %s" % line)
        print(ipsec_conf_dict)
        return  ipsec_conf_dict

# wrapper functions for robo keywords
def create_strongswan_object(linux_handle, **kwargs):
    """
        Wrapper function calls Strongswan init class

        :param linux_handle:
                **REQUIRED** linux handle where strongswan is installed

        :param kwargs: connection_name:
                **REQUIRED* ipsec connection name

        :return class instance

            EXAMPLE::

            ${sobj} =  create strongswan object  linux_handle  connection_name=mytest
    """

    return Strongswan(linux_handle, **kwargs)

def generate_ipsec_conf(strongswan_obj, **kwargs):
    """
        Creates  ipsec.conf for strongSwan

        :param ipsec_conf_dict
                **REQUIRED** ipsec config parameters as dictonary

        :param append
                *OPTIONAL*  append to the existing ipsec.conf file

                Default: 0 , Supported values 0/1

        :return True on success

                Raise exception on failure

            EXAMPLE::
               &{user_dict} = leftsubnet=10.1.0.0/16  leftcert=moonCert.pem  leftid=@moon.strongswan.org right=%any auto=add

               generate ipsec conf  ${sobj}  append=1  ipsec_conf_dict=&{user_dict}

                ipsec.conf file will be created as below

                config setup

                   cachecrls=yes

                   strictcrlpolicy=yes

                conn %default

                       keyingtries=1

                       keyexchange=ikev2

                conn roadwarrior

                       leftsubnet=10.1.0.0/16

                       leftcert=moonCert.pem

                       leftid=@moon.strongswan.org

                       right=%any

                       auto=add

                For different key values refer to

                https://wiki.strongswan.org/projects/strongswan/wiki/ConnSection

    """
    return strongswan_obj.create_ipsec_conf(**kwargs)

def add_to_ipsec_secrets(strongswan_obj, **kwargs):
    """
            Adds given data to secrets file

             :param: auth_type
                **REQUIRED**  Authentication type to add

                Supported Values PSK/RSA/ECDSA

             For PSK host_id  or peer_id are mandatory

             :param  preshared_key
                **REQUIRED**  pre shared key to be updated

             :param host_id:
                 *OPTIONAL*  ip address

             :param peer_id
                 *OPTIONAL*  ip address

             For RSA and ECDSA below is mandatory

             :param local_cert
                 *OPTIONAL* Local certificate name

             :param xauth_user
                 *OPTIONAL* xauth username

             :param xauth_pwd
                 *OPTIONAL* xauth password

             :param crl_check
                 *OPTIONAL* cerificate crl check, 0 for disable, 1 for enable - default is 1

            :return:
                 True on Success

                 Raise exception on failure

             EXAMPLE::

               Python:
                 sobj.add_ipsec_secrets(auth_type='PSK', preshared_key='juniper123', host_id='11.0.1.1', peer_id='11.0.1.2')

               Robot:
                 For preshared key

                 add to ipsec secrets  ${sobj}   auth_type=PSK  preshared_key=juniper123  host_id=11.0.1.1  peer_id=11.0.1.2

                 For RSA

                 add to ipsec secrets   ${sobj}  auth_type=RSA   local_cert=moonCert.pem

                 For preshared key xauth

                 add to ipsec secrets  ${sobj}   auth_type=PSK  preshared_key=juniper123  xauth_user=user1  xauth_pwd=password1
    """

    return strongswan_obj.add_ipsec_secrets(**kwargs)

def ipsec_up(strongswan_obj, **kwargs):
    """
            Wrapper function calls ipsec_up  class method

            Will start ipsec on Strongswan

            :param connection_name
                *OPTIONAL* ipsec connection name to start

                Default will take from the connection name provided in init

            :param restart

                *OPTIONAL* restart ipsec before making up

                Default: 1, supported values 1/0

            :param  timeout

                *OPTIONAL*  timeout for ipsec up.

                Default 60 secs

            :return True on success

                Raise exception on failure

                EXAMPLE::

                ipsec up  ${sobj}
    """

    return strongswan_obj.ipsec_up(**kwargs)

def ipsec_status(strongswan_obj, **kwargs):
    """
            Wrapper function calls ipsec_status_check  class method

            Checks ipsec status

            :param pattern
                *OPTIONAL*  string to grep from status output.

                Default: INSTALLED

            :param connection_name
                *OPTIONAL* ipsec connection name to start

                Default will take from the connection name provided in init

            :param err_level
                *OPTIONAL* Error level, used in case of negative test case

                Default: ERROR, Supported : INFO, DEBUG

            :return: True on success

                Raise exception on failure
                EXAMPLE::

                ipsec status check  ${sobj}
    """
    return strongswan_obj.ipsec_status_check(**kwargs)

def ipsec_down(strongswan_obj, **kwargs):
    """
            Wrapper function calls ipsec_down  class method

            Stops ipsec connection by running "ipsec down <connname>"

            :param connection_name
                *OPTIONAL* ipsec connection name to start

                Default will take from the connection name provided in init

            :return True on success

              Raise exception on failure

                EXAMPLE::

              ipsec down  ${sobj}
    """

    return strongswan_obj.ipsec_down(**kwargs)

