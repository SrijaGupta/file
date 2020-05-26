"""
openssl class and ROBOT keywords functions
"""
import os
import re
import time
#from jnpr.toby.hldcl.device import Device
#from jnpr.toby.hldcl.unix.unix import *

class Openssl:
    """
        Class Factory for openssl
    """
    def __init__(self, linux_handle, **kwargs):
        """

        :param linux_handle:
            **REQUIRED** linux handle object
        :param cert_name:
            **REQUIRED**  Certificate name
        :param key_size:
            **OPTIONAL** key size
            Supported values 256/1024/2048/
            Default: 1024
        :param key_type:
            **OPTIONAL** Algorithm for encrypting public private keys
            Supported values rsa/dsa/ecdsa256/ecdsa384
            Default : rsa
        :param crl_path:
            **OPTIONAL** crl directory on linux machine
            Default: /var/www/html/pki-ocsp-crl-req
        :param self_sign:
            **OPTIONAL** creates chain cert or self sign cert
            Supported values 1/0
            Default: 1 (self signed cert)
        :param days:
            **OPTIONAL** Validity of cert
            Default: 365
        :param port_number:
            **OPTIONAL**  port number for ocsp responder
            Default: 8400
        :param parent_cert:
            **OPTIONAL** parent cert for non self signed cert
            Parent cert is required if self_sign=0
        :return: Openssl object
        EXAMPLE::
             openssl_obj = Openssl(linux_handle , cert_name='test_root_ca', key_type='ecdsa', key_size='256')
        """
        if 'cert_name' in kwargs:
            self.ca_cert = kwargs.get('cert_name')
        else:
            raise Exception("cert_name parameter is mandatory")
        self.linux_handle = linux_handle
        self.openssl_dir = kwargs.get('openssl_dir', '/etc/pki/script_gen')
        self.key_size = kwargs.get('key_size', '1024')
        self.key_type = kwargs.get('key_type', 'rsa')
        self.crl_path = kwargs.get('crl_path', '/var/www/html/pki-ocsp-crl-req')
        self.sign = kwargs.get('self_sign', 1)
        self.days = str(kwargs.get('days', 365))
        self.port_number = str(kwargs.get('port_number', '8400'))
        self.subject = kwargs.get('subject', "/C=US/ST=CA/L=Sunnyvale/O=Juniper/CN=" + \
                                  self.ca_cert + "/OU=QA")
        self.ca_path = self.openssl_dir + '/' + self.ca_cert + '/'
        self.ca_openssl_cnf = self.ca_path + '/' + 'openssl.cnf'
        self.private = self.ca_path + '/' + 'private'
        self.cert_dir = self.ca_path + '/' + 'certs'
        #self.crl_dir = self.crl_path + '/' + 'crl'
        self.crl_dir = self.ca_path + '/' + 'crl'
        self.newcerts = self.ca_path + '/' + 'newcerts'
        self.key = self.private + '/' + self.ca_cert + '-key.pem'
        self.hash_algo = ''
        if self.key_size == '256':
            self.hash_algo = '-sha256'
        else:
            self.hash_algo = '-sha384'
        if self.sign:
            self.cert_file = self.ca_cert + '.pem'
        else:
            self.cert_file = self.ca_cert + '.csr'  #this is request file before generting child ca

        if self.sign != 1:
            if 'parent_cert' in kwargs:
                self.parent_cert = kwargs['parent_cert']
            else:
                raise Exception("parent_cert is required for non self signed cert")

        self.host_ip = self.linux_handle.shell(command="hostname -I |cut -d ' ' -f 1").response() #get liunx mgmt ip
        #self.linux_handle.su()
        m = re.search(r'(\d+.\d+.\d+.\d+).*', self.host_ip)
        self.host_ip = m.group(1)
        self.linux_handle.log("Switching user to root")
        self.linux_handle.su(password='Embe1mpls')
        #self.host_ip = '10.204.139.240'

    def gen_openssl_ca_cert(self, **kwargs):
        """
            This routine creates openssl ca certifciate
            :param hash_algo:
               *OPTIONAL*  applies only ofr rsa key type
               Supported values -md5|-sha1|-mdc2
            :return: True on Success , False on Failure
            EXAMPLE::
                openssl_obj.gen_openssl_ca_cert()
        """
        self.linux_handle.log("In gen_openssl_ca_cert")
        self.linux_handle.log("creating required directories and files")
        if self._chk_path(self.ca_path):
            self.linux_handle.log("Removing old ca path " + self.ca_path)
            self._invoke("rm -rf " + self.ca_path)

        if not self._chk_path(self.crl_path):
            self.linux_handle.log(self.crl_path + ' doesnot exists , creating one')
            self._invoke("mkdir -m 777 -p " + self.crl_path)

        for dir1 in (self.ca_path, self.private, self.cert_dir, self.newcerts, self.crl_dir, self.private):
            self._invoke("mkdir -m 777 -p " + dir1)

        self.linux_handle.log("Creating Initial files")
        self._invoke("touch " + self.ca_path + '/index.txt')
        self._invoke("echo '01' > " + self.ca_path + '/serial')
        self._invoke("echo '10' > " + self.ca_path + '/crlnumber')
        if hasattr(self, 'parent_cert'):
            cmd = 'cat ' + self.openssl_dir + '/' + self.parent_cert + '/openssl.cnf.FALSE |grep OCSP |cut -d : -f 4'
            try:
                resp = self.linux_handle.shell(command=cmd).response()
                #resp = self._invoke(cmd)
                print(resp)
                m = re.search(r'(\d+).*', resp)
                self.parent_port = m.group(1)
            except Exception as err:
                raise err
        self._edit_openssl_cnf()
        self._invoke(' yes | cp -rf ' + self.ca_path + '/' + 'openssl.cnf.TRUE' +  ' '  + self.ca_openssl_cnf)
        self.linux_handle.log("Generating key-pair for the cert")
        cmd = ''

        if self.key_type == 'ecdsa':
            if self.key_size == '256':
                cmd = 'openssl ecparam -genkey -name prime256v1 -out '+ self.key
                #self.hash_algo = '-sha256'
            else:
                cmd = 'openssl ecparam -genkey -name secp384r1 -out ' + self.key
                #self.hash_algo = '-sha384'
        elif self.key_type == 'dsa':
            cmd = 'openssl dsaparam -genkey ' + self.key_size + ' -out ' + self.key
        else:
            cmd = 'openssl genrsa -out ' +  self.key + ' ' + self.key_size
            if 'hash_algo' in kwargs:
                self.hash_algo = '-' + kwargs.get('hash_algo')
        self.linux_handle.log("Running: " + cmd)
        self._invoke(cmd)
        if not self._chk_path(self.key):
            self.linux_handle.log(level="ERROR", message="Didnot create private key path")
            raise Exception("Failed creating private key")
        self.linux_handle.log("Generated key pair for ca cert: " + self.key)
        if self.sign:
            self.linux_handle.log("Creating Self signed ca cert")
            cmd = 'openssl req -new -x509 -key ' +  self.key + ' -out ' +  self.cert_dir + '/' + \
                  self.cert_file + ' -config ' + self.ca_openssl_cnf + ' -days ' + self.days +' -subj '+\
                  self.subject + ' '  + self.hash_algo
        else:
            self.linux_handle.log("Creating CA certificate request")
            cmd = 'openssl req -new -key ' +  self.key + ' -out ' +  self.cert_dir + '/' + self.cert_file \
                  + ' -config ' + self.ca_openssl_cnf + ' -days ' + self.days +' -subj '+ self.subject
        self.linux_handle.log("Running : " + cmd)
        result = self._invoke(cmd)
        prog = re.compile(r'(:error:)|(unknown option)|(problems)')
        #import pdb
        #pdb.set_trace()
        #import sys, pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        if prog.search(result):
            self.linux_handle.log(level="ERROR", message="Creating cert failed: " + result)
            raise Exception("Creating cert failed")
        self.linux_handle.log("CA certifcate generation successful")
        if not self.linux_handle.download(remote_file=self.cert_dir + '/' + self.cert_file,
                                          local_file=self.cert_file, protocol='scp'):
            raise Exception('Downloading cert failed: ' + self.cert_file)
        #ocsp specific
        if self.sign:
            self.linux_handle.log("Updating index.txt file")
            update_index_file(self.linux_handle, self.cert_dir + '/' + self.ca_cert + '.pem', self.ca_path + '/index.txt')
        return True

    def gen_cert_req(self, handle, **kwargs):
        """
        This routine generates Local certifciate request
        :param router_handle/linux_handle:
            **REQUIRED** router handle object or linux_handle based on
            where to generate cert request
        :param cert_id:
            **REQUIRED** Local cert name
        :param gen_on:
            *OPTIONAL* where to generate certifcate request
            Supported values router/strongswan
            Default: router
        :param key_size:
            *OPTIONAL* key size
            Default: takes from init
        :param ip:
            *OPTIONAL* Static IP address of the device
            Gets added to alt subjectname
        :param domain_name:
            *OPTIONAL* FQDN to be added in SubjectAltName
        :return: True on Success , False on failure
        EXAMPLE::
             openssl_obj.gen_cert_req(rh, cert_id='local_neg')
        """
        self.gen_on = kwargs.get('gen_on', 'router')
        if self.gen_on == 'router':
            self._gen_cert_req_router(handle, **kwargs)
        elif self.gen_on == 'strongswan':
            self._gen_cert_req_strongswan(handle, **kwargs)
        elif self.gen_on == 'openssl':
            self._gen_cert_req_openssl(handle, **kwargs)
        return True

    def _gen_cert_req_router(self, rh, **kwargs):
        """

        :param rh:
        :param kwargs:
        :return:
        """
        self.rh = rh
        if 'cert_id' in kwargs:
            self.local_cert = kwargs.get('cert_id')
        else:
            raise Exception("cert_id parameter is mandatory")

        key_size = kwargs.get('key_size', self.key_size)
        self.ip = kwargs.get('ip', '0.0.0.0')
        self.domain_name = kwargs.get('domain_name', 'juniper.net')
        self.email = kwargs.get('email', 'test@juniper.net')
        key_type = kwargs.get('key_type', self.key_type)
        self.req_file = self.local_cert + '_req_file'
        subject = 'C=US,ST=CA,L=Sunnyvale,O=Juniper,CN=' + self.local_cert + \
                  ',emailAddress=test@juniper.net,OU=QA'
        subject = kwargs.get('subject', subject)

        self.rh.log("Generating key pair for local cert")
        cmd = 'request security pki generate-key-pair certificate-id ' + self.local_cert +\
               ' size ' + key_size + ' type ' + key_type
        result = self.rh.cli(command=cmd).response()
        if re.search(r'Generated|Generating', result):
            self.rh.log("Key-pair generation successful")
        else:
            self.rh.log(level='ERROR', message="Failed Generating key pair for local cert")
            raise Exception("Failed Generating key pair for local cert")

        self.rh.log("Generating certificate request")
        cmd = 'request security pki generate-certificate-request certificate-id '+ self.local_cert \
              + ' subject ' + subject  + ' ip-address ' + self.ip + ' domain-name ' + self.domain_name + \
              ' email ' + self.email + ' filename ' + '/var/home/regress/' + self.req_file
        self.rh.log("Ruunning " + cmd)
        result = self.rh.cli(command=cmd).response()
        if re.search(r'error', result):
            self.rh.log(level='ERROR', message="Failed Generating cert request " + result)
            raise Exception("Failed Generating cert request " + result)
        else:
            self.rh.log("Certifcate request generation successful")
        if not rh.download(remote_file='/var/home/regress/' + self.req_file, local_file=self.req_file):
            raise Exception("Downloading cert request file failed " + self.req_file)
        return True

    def _gen_cert_req_strongswan(self, linux_handle, **kwargs):
        """

        :return:
        """
        self.strongswan_handle = linux_handle
        if 'cert_id' in kwargs:
            self.local_cert = kwargs.get('cert_id')
        else:
            raise Exception("cert_id parameter is mandatory")
        cert_dir = '/var/tmp/'
        key_type = kwargs.get('key_type', self.key_type)
        key_size = kwargs.get('key_size', self.key_size)
        out_format = kwargs.get('output_format', 'pem')
        self.domain_name = kwargs.get('domain_name', 'juniper.net')
        conf_dir = linux_handle.shell(command='ipsec --confdir').response().rstrip()
        key_filename = kwargs.get('key_filename', self.local_cert)
        key_file = conf_dir + '/ipsec.d/private/' + key_filename + '.pem'
        self.req_file = self.local_cert + '_req.pem'
        subject = "DC=Common_component, CN=%s, OU=SLT_QA, O=Juniper, L=Sunnyvale, ST=CA, C=US" % self.local_cert
        subject = kwargs.get('subject', subject)
        if key_type == 'ecdsa':
            key_size = kwargs.get('key_size', 384)
        elif key_type == 'bliss':
            key_size = kwargs.get('key_size', 1)

        cmd = "ipsec pki --gen --type  %s --size %s --outform %s > %s" % (key_type, key_size, out_format, key_file)
        linux_handle.log("Generating key pair %s" % cmd)
        result = linux_handle.shell(command=cmd).response()
        if re.search(r'Error:|invalid', result, re.IGNORECASE):
            linux_handle.log(level="ERROR", message="Error in generating key pair %s" % result)
            raise Exception("Generating key pair failed" + result)
        else:
            linux_handle.log("Generating key pair successful")

        cmd = "ipsec pki --req --in %s --dn %s --type %s" % (key_file, subject, key_type)
        subject_altname = ''
        if 'ip' in kwargs:
            self.ip = kwargs.get('ip')
            subject_altname = self.ip
        elif 'email' in kwargs:
            self.email = kwargs.get('email')
            subject_altname = self.email
        else:
            self.domain_name = kwargs.get('domain_name', 'juniper.net')
            subject_altname = self.domain_name

        cmd = cmd + " --san %s" % subject_altname
        cmd = cmd + " --outform %s >%s" % (out_format, cert_dir+self.req_file)
        linux_handle.log("Generating cert request %s" % cmd)
        result = linux_handle.shell(command=cmd).response()
        if re.search(r'Error:|invalid', result, re.IGNORECASE):
            linux_handle.log(level="ERROR", message="Error in generating cert request %s" % result)
            raise Exception("Generating cert request failed" + result)
        else:
            linux_handle.log("Generating cert request successful")
        if not linux_handle.download(remote_file=cert_dir+self.req_file, local_file=self.local_cert + '_req.pem', protocol='scp'):
            raise Exception("Downloading cert request file failed " + self.req_file)
        return True


    def _gen_cert_req_openssl(self, linux_handle, **kwargs):
        """
        :return:
        """
        self.load_both = kwargs.get('load_both', 1)
        if 'router_handle' in kwargs:
            self.rh = kwargs.get('router_handle')
        #else:
            #raise Exception("router_handle parameter is mandatory")
        if 'cert_id' in kwargs:
            self.local_cert = kwargs.get('cert_id')
        else:
            raise Exception("cert_id parameter is mandatory")
        self.certreq = self.ca_path + '/' + 'certreq'
        key_type = kwargs.get('key_type', self.key_type)
        key_size = kwargs.get('key_size', self.key_size)
        out_format = kwargs.get('output_format', 'pem')
        key_file = self.certreq + '/' + self.local_cert + '_req.key'
        csr_file = self.certreq + '/' + self.local_cert + '_req.pem'
        cert_dir = self.ca_path + '/' + 'certreq/'
        self.req_file = self.local_cert + '_req.pem'
        #self.req_file = self.certreq + '/' + self.local_cert + '_req.pem'
        subject = "/C=US/ST=CA/L=Bangalore/O=Juniper/CN=%s/OU=QA" % self.local_cert
        subject = kwargs.get('subject', subject)
        if key_type == 'ecdsa':
            if self.sign:
                new_key = 'ec:' + self.cert_dir + '/' + self.cert_file
            else:
                new_key = 'ec:' + self.cert_dir + '/' + self.ca_cert + '.pem'
        elif key_type == 'rsa':
            new_key = 'rsa:' + str(key_size)

        self._invoke("mkdir -m 777 -p " + self.certreq)

        #if key_type == 'ecdsa':
        #    cmd = "openssl req -nodes -new -keyout %s -out %s -subj %s" % (key_file, csr_file, subject)
        #elif key_type == 'rsa':
        #   cmd = "openssl req -nodes -new -keyout %s -out %s -subj %s -newkey %s" % (key_file, csr_file, subject, new_key)

        cmd = "openssl req -nodes -new -keyout %s -out %s -subj %s -newkey %s" % (key_file, csr_file, subject, new_key)

        subject_altname = ''
        if 'ip' in kwargs:
            self.ip = kwargs.get('ip')
            subject_altname = self.ip
        elif 'email' in kwargs:
            self.email = kwargs.get('email')
            subject_altname = self.email
        else:
            self.domain_name = kwargs.get('domain_name', 'juniper.net')
            subject_altname = self.domain_name

        linux_handle.log("Generating cert request %s" % cmd)
        result = linux_handle.shell(command=cmd).response()
        if re.search(r'Error:|invalid', result, re.IGNORECASE):
            linux_handle.log(level="ERROR", message="Error in generating cert request %s" % result)
            raise Exception("Generating cert request failed" + result)
        else:
            linux_handle.log("Generating cert request successful")

        if not linux_handle.download(remote_file=cert_dir+self.req_file, local_file=self.local_cert + '_req.pem', protocol='scp'):
            raise Exception("Downloading cert request file failed " + self.req_file)
        return True


    def sign_cert(self, **kwargs):
        """
        This routine signs certifciate and loads the certs

        :param load_cert:
            *OPTIONAL*  sign and load both certs on router
            Supported values 1/0
            Default: 1
        :return: True on Success , False on Failure
        EXAMPLE::
            openssl_obj.sign_cert()
        """
        cert = ''
        sign_cert = ''
        load_cert = kwargs.get('load_cert', 1)
        if hasattr(self, 'domain_name'):
            self.domain_name = kwargs.get('domain_name', self.domain_name)
        else:
            self.domain_name = kwargs.get('domain_name', 'juniper.net')
        #import pdb
        #pdb.set_trace()
        if hasattr(self, 'local_cert'):
            self.linux_handle.log('Using openssl cnf from ' + self.ca_path + '/openssl.cnf.FALSE')
            cmd = 'yes | cp -rf ' + self.ca_path + '/openssl.cnf.FALSE' + ' ' + self.ca_path + '/openssl.cnf'
            self._invoke(cmd)
            self.linux_handle.log("Uploading request file" + self.req_file)
            if not self.linux_handle.upload(local_file=self.req_file, remote_file=self.ca_path + '/' + self.req_file,
                                            protocol='scp', user='root', password='Embe1mpls'):
                self.linux_handle.log("Uploading request file failed" + self.req_file)
                raise Exception("Uploading request file failed" + self.req_file)
            cert = self.cert_file
            sign_cert = self.local_cert + '.pem'
        else:
            self.linux_handle.log('Using openssl cnf from ' + self.ca_path + '/openssl.cnf.TRUE')
            cmd = 'yes | cp -rf ' + self.ca_path + '/openssl.cnf.TRUE' + ' ' + self.ca_path + '/openssl.cnf'
            self._invoke(cmd)
            self.linux_handle.log('Signing the child ca cert ' + self.ca_cert + ' with parent cert : ' + self.parent_cert)
            cert = self.openssl_dir + '/' + self.parent_cert + '/' + 'certs/'+ self.parent_cert + '.pem'
            sign_cert = self.ca_cert + '.pem'
        if not self.linux_handle.download(remote_file=self.ca_path + '/openssl.cnf',
                                          local_file='openssl.cnf', protocol='scp'):
            self.linux_handle.log("Download of openssl.cnf failed")
            raise Exception("Download of openssl.cnf failed")

        with open("openssl.cnf", "a") as myfile:
            subject_alt = 'subjectAltName=DNS:' + self.domain_name
            if hasattr(self, 'email'):
                subject_alt = subject_alt + ',' + 'email:' + self.email
            if hasattr(self, 'ip') and self.ip != '0.0.0.0':
                subject_alt = subject_alt + ',IP:' + self.ip
            self.linux_handle.log("Added subject alt name : " + subject_alt)
            myfile.write(subject_alt)
        myfile.close()

        #import pdb
        #pdb.set_trace()
        if not self.linux_handle.upload(local_file='openssl.cnf',
                                        remote_file=self.ca_path + '/openssl.cnf', protocol='scp', user='root', password='Embe1mpls'):
            self.linux_handle.log("Upload of openssl.cnf failed")
            raise Exception("Upload of openssl.cnf failed")

        self.linux_handle.log("Signing the cert")
        sign_cli = ''
        if hasattr(self, 'local_cert'):
            sign_cli = 'openssl x509 -req -days ' + self.days + ' -in ' + self.ca_path + '/' + self.req_file +\
                       ' -CA ' + self.cert_dir + '/' + self.ca_cert + '.pem' + ' -CAkey ' + self.key + \
                       ' -CAcreateserial -out ' + self.cert_dir + '/' + sign_cert + ' -extfile ' + self.ca_path + '/openssl.cnf ' + self.hash_algo
        else:
            private_key = self.openssl_dir + '/' + self.parent_cert + '/private/' + self.parent_cert + '-key.pem'
            sign_cli = 'openssl x509 -req -days ' + self.days + ' -in ' + self.cert_dir + '/' + \
            self.cert_file + ' -CA ' + cert + ' -CAkey ' + private_key + \
            ' -CAcreateserial -out ' + self.cert_dir + '/' + sign_cert + ' -extfile ' +  self.ca_path + '/openssl.cnf ' + self.hash_algo

        self.linux_handle.log("Running " + sign_cli)
        result = self._invoke(sign_cli)
        prog = re.compile(r'(error)|(unknown option)|(problems)')
        if prog.search(result):
            self.linux_handle.log(level="ERROR", message="Signing cert failed: " + result)
            raise Exception("Signing cert failed")
        self.linux_handle.log("Signing cert successful")
        #update_index_file
        if not self.linux_handle.download(remote_file=self.cert_dir + '/' + sign_cert,
                                          local_file=sign_cert, protocol='scp'):
            self.linux_handle.log("Download of" + sign_cert + " failed")
            raise Exception("Download of " + sign_cert + " failed")
        self.linux_handle.log("Generating crl for ca cert")
        if self.key_type == "ecdsa":
            gen_crl(self.linux_handle, cert_name=self.ca_cert, key_type=self.key_type)
        else:
            gen_crl(self.linux_handle, cert_name=self.ca_cert)

        self.linux_handle.log("Updating index files")

        if hasattr(self, 'local_cert'):
            update_index_file(self.linux_handle, self.cert_dir + '/' + sign_cert, self.ca_path + '/index.txt')
        else:
            update_index_file(self.linux_handle, self.cert_dir + '/' + self.ca_cert + '.pem',
                              self.openssl_dir + '/' + self.parent_cert + '/index.txt')

        if load_cert == 1:
            self.linux_handle.log("Loading cert on device")
            self.load_cert(**kwargs)
        return True

    def load_cert(self, **kwargs):
        """
            This routine loads  ca and local certifciate on router
        :param device_handle
             *OPTIONAL/REQUIRED*  this is a router handle required if gen_cert_request not called
        :param cert_file:
            *OPTIONAL* cert file name to be loaded

        :return: True on Success , False on Failure

        """
        #cert_path = kwargs.get('cert_path', self.cert_dir)
        cert = kwargs.get('cert_name', self.ca_cert + '.pem')
        load_both = kwargs.get('load_both', 1)
        load_cert = kwargs.get('load_cert', 1)
        if hasattr(self, 'rh'):
            self.rh = kwargs.get('device_handle', self.rh)
        elif 'device_handle' in kwargs:
            self.rh = kwargs.get('device_handle')
        elif not hasattr(self, 'strongswan_handle'):
            raise Exception("device_handle parameter is mandatory as cert_request not called")

        if hasattr(self, 'gen_on'):
            if load_both == 1 and self.gen_on == 'router':
                if not self.rh.upload(local_file=cert, remote_file='/var/home/regress/' + cert, user='root', password='Embe1mpls'):
                    self.linux_handle.log("Upload of " + cert + "failed")
                    raise Exception("Upload of " + cert + " failed")
                cmd = 'request security pki ca-certificate load ca-profile ' + self.ca_cert + \
                      ' filename /var/home/regress/' + cert
                self.rh.log("Running " + cmd)
                self.rh.cli(command=cmd, pattern="[yes,no]").response()
                response = self.rh.cli(command="yes").response()
                self.rh.log("Response: " + response)
                if hasattr(self, 'local_cert'):
                    if not self.rh.upload(local_file=self.local_cert + '.pem', remote_file='/var/home/regress/' + self.local_cert + '.pem',
                                          user='root', password='Embe1mpls'):
                        self.linux_handle.log("Upload of " + self.local_cert + "failed")
                        raise Exception("Upload of " + self.local_cert + " failed")
                    cmd = 'request security pki local-certificate load certificate-id ' \
                          + self.local_cert + ' filename /var/home/regress/' + self.local_cert + '.pem'
                    self.rh.log("Running " + cmd)
                    response = self.rh.cli(command=cmd).response()
                    self.rh.log("Response: " + response)
            elif load_both == 1 and self.gen_on == 'strongswan':
                self.strongswan_handle.log("creating required directories for copying certs")
                conf_dir = self.strongswan_handle.shell(command='ipsec --confdir').response().rstrip()
                ca_path = conf_dir + '/ipsec.d/cacerts'
                local_cert_path = conf_dir + '/ipsec.d/certs'
                if self.linux_handle is self.strongswan_handle:
                    if not self._chk_path(ca_path):
                        self.linux_handle.log("Creating ca dir" + ca_path)
                        cmd = "mkdir -m 777 -p "  + ca_path
                        response = self.linux_handle.shell(command=cmd).response()
                        self.linux_handle.log("Response: " + response)
                    if not self._chk_path(local_cert_path):
                        self.linux_handle.log("Creating ca dir " + local_cert_path)
                        cmd = "mkdir -m 777 -p " + local_cert_path
                        response = self.linux_handle.shell(command=cmd).response()
                        self.linux_handle.log("Response: " + response)
                    self.linux_handle.log("Copying the cacert and local cert to strongswan ipsec directory on the same Machines")
                    self.linux_handle.log("Copying ca cert " + cert)
                    self._invoke("yes | cp -rf %s %s" %(self.cert_dir + '/' + self.cert_file, ca_path))
                    self.linux_handle.log("Copying local cert " + self.local_cert)
                    self._invoke("yes | cp -rf %s %s" %(self.cert_dir + '/' + self.local_cert + '.pem', local_cert_path))
                else:
                    self.strongswan_handle.log("Uploading the cacert and local cert to strongswan ipsec directory on the different \
                                               Machines from local Execution server")
                    if not self.strongswan_handle.upload(local_file=self.local_cert + '.pem',\
                           remote_file=local_cert_path, user='root', password='Embe1mpls'):
                        self.strongswan_handle.log("Upload of " + self.local_cert + '.pem'+ "failed")
                        raise Exception("Upload of " + self.local_cert + " failed")
                    if not self.strongswan_handle.upload(local_file=self.cert_file, remote_file=ca_path, user='root', password='Embe1mpls'):
                        self.strongswan_handle.log("Upload of " + self.local_cert + "failed")
                        raise Exception("Upload of " + self.local_cert + " failed")
                    file1 = local_cert_path + "/" + self.local_cert + '.pem'
                    if not self._chk_path(file1, handle=self.strongswan_handle):
                        raise Exception("Upload of " + self.local_cert + " failed")
                    file2 = ca_path + "/" + self.cert_file
                    if not self._chk_path(file2, handle=self.strongswan_handle):
                        raise Exception("Upload of " + self.local_cert + " failed")
            elif self.gen_on == 'openssl':
                if not self.rh.upload(local_file=cert, remote_file='/var/home/regress/' + cert, user='root', password='Embe1mpls'):
                    self.linux_handle.log("Upload of " + cert + "failed")
                    raise Exception("Upload of " + cert + " failed")
                cmd = 'request security pki ca-certificate load ca-profile ' + self.ca_cert + \
                      ' filename /var/home/regress/' + cert
                self.rh.log("Running " + cmd)
                self.rh.cli(command=cmd, pattern="[yes,no]").response()
                response = self.rh.cli(command="yes").response()
                self.rh.log("Response: " + response)
        else:
            self.rh.log("Loading only ca " + cert + " on the router")
            if not self.rh.upload(local_file=cert, remote_file='/var/home/regress/' + cert, user='root',
                                  password='Embe1mpls'):
                self.linux_handle.log("Upload of " + cert + "failed")
                raise Exception("Upload of " + cert + " failed")
            cmd = 'request security pki ca-certificate load ca-profile ' + self.ca_cert + \
                  ' filename /var/home/regress/' + cert
            self.rh.log("Running " + cmd)
            self.rh.cli(command=cmd, pattern="[yes,no]").response()
            response = self.rh.cli(command="yes").response()
            self.rh.log("Response: " + response)
        return True


    def _invoke(self, cmd):
        self.linux_handle.log("Executing " + cmd)
        try:
            return  self.linux_handle.shell(command=cmd).response()
        except Exception as err:
            self.linux_handle.log(level="ERROR", message=err)
            raise err

    def _chk_path(self, file, handle="Default"):
        cmd = 'ls -l ' + file
        if handle is "Default":
            result = self.linux_handle.shell(command=cmd).response()
        else:
            result = handle.shell(command=cmd).response()
        if re.search('No such file or dir', result):
            return 0
        else:
            return 1


    def  _edit_openssl_cnf(self):
        #openssl_cnf_true = self.ca_path + 'openssl.cnf.TRUE'
        #openssl_cnf_false = self.ca_path + 'openssl.cnf.FALSE'
        self._invoke("cd " + self.ca_path)
        if os.path.isfile("openssl.cnf.TRUE"):
            os.unlink('openssl.cnf.TRUE')  #removes file form running directory
        crl_dist_points = ''
        ocsp_url = ''
        if hasattr(self, 'parent_cert'):
            crl_dist_points = 'crlDistributionPoints = URI:http://' + self.host_ip + '/pki-ocsp-crl-req/' \
                              + self.parent_cert +  '-crl.pem'
            ocsp_url = 'authorityInfoAccess = OCSP;URI:http://' + self.host_ip + ':' + self.parent_port

        openssl_cnf_template = """
        # OpenSSL example configuration file.
# This is mostly being used for generation of certificate requests.
#

# This definition stops the following lines choking if HOME isn't
# defined.
HOME			= .
RANDFILE		= $ENV::HOME/.rnd

# Extra OBJECT IDENTIFIER info:
#oid_file		= $ENV::HOME/.oid
oid_section		= new_oids

# To use this configuration file with the \"-extfile\" option of the
# \"openssl x509\" utility, name here the section containing the
# X.509v3 extensions to use:
extensions		= v3_sign
# (Alternatively, use a configuration file that has only
# X.509v3 extensions in its main [= default] section.)

[ new_oids ]

# We can add new OIDs in here for use by 'ca', 'req' and 'ts'.
# Add a simple OID like this:
# testoid1=1.2.3.4
# Or use config file substitution like this:
# testoid2=\$testoid1.5.6

# Policies used by the TSA examples.
tsa_policy1 = 1.2.3.4.1
tsa_policy2 = 1.2.3.4.5.6
tsa_policy3 = 1.2.3.4.5.7

####################################################################
[ ca ]
default_ca	= CA_default		# The default ca section

####################################################################
[ CA_default ]

dir		= ./	# Where everything is kept
certs		= $dir/certs		# Where the issued certs are kept
crl_dir		= $dir/crl		# Where the issued crl are kept
database	= $dir/index.txt	# database index file.
#unique_subject	= no			# Set to 'no' to allow creation of
					# several ctificates with same subject.
new_certs_dir	= $dir/newcerts		# default place for new certs.

certificate	=  $certs/{cert_pem} 	# The CA certificate
serial		=  $dir/serial 		# The current serial number
crlnumber	=  $dir/crlnumber	# the current crl number
					# must be commented out to leave a V1 CRL
crl		= $dir/crl.pem 		# The current CRL
private_key	= $dir/private/{private_key}	# The private key
RANDFILE	= $dir/private/.rand	# private random number file

x509_extensions	= usr_cert		# The extentions to add to the cert

# Comment out the following two lines for the \"traditional\"
# (and highly broken) format.
name_opt 	= ca_default		# Subject Name options
cert_opt 	= ca_default		# Certificate field options

# Extension copying option: use with caution.
# copy_extensions = copy

# Extensions to add to a CRL. Note: Netscape communicator chokes on V2 CRLs
# so this is commented out by default to leave a V1 CRL.
# crlnumber must also be commented out to leave a V1 CRL.
# crl_extensions	= crl_ext

default_days	= 365			# how long to certify for
default_crl_days= 365			# how long before next CRL
default_md	= sha1			# use public key default MD
preserve	= no			# keep passed DN ordering

# A few difference way of specifying how similar the request should look
# For type CA, the listed attributes must be the same, and the optional
# and supplied fields are just that :-)
policy		= policy_match

# For the CA policy
[ policy_match ]
countryName		= match
stateOrProvinceName	= match
organizationName	= match
organizationalUnitName	= optional
commonName		= supplied
emailAddress		= optional

# For the 'anything' policy
# At this point in time, you must list all acceptable 'object'
# types.
[ policy_anything ]
countryName		= optional
stateOrProvinceName	= optional
localityName		= optional
organizationName	= optional
organizationalUnitName	= optional
commonName		= supplied
emailAddress		= optional

####################################################################
[ req ]
default_bits		= 2048
default_keyfile 	= privkey.pem
distinguished_name	= req_distinguished_name
attributes		= req_attributes
x509_extensions	= v3_ca	# The extentions to add to the self signed cert

# Passwords for private keys if not present they will be prompted for
# input_password = secret
# output_password = secret

# This sets a mask for permitted string types. There are several options.
# default: PrintableString, T61String, BMPString.
# pkix	 : PrintableString, BMPString (PKIX recommendation before 2004)
# utf8only: only UTF8Strings (PKIX recommendation after 2004).
# nombstr : PrintableString, T61String (no BMPStrings or UTF8Strings).
# MASK:XXXX a literal mask value.
# WARNING: ancient versions of Netscape crash on BMPStrings or UTF8Strings.
string_mask = utf8only

req_extensions = v3_req # The extensions to add to a certificate request

[ req_distinguished_name ]
countryName			= Country Name (2 letter code)
countryName_default		= AU
countryName_min			= 2
countryName_max			= 2

stateOrProvinceName		= State or Province Name (full name)
stateOrProvinceName_default	= Some-State

localityName			= Locality Name (eg, city)

0.organizationName		= Organization Name (eg, company)
0.organizationName_default	= Internet Widgits Pty Ltd

# we can do this but it is not needed normally :-)
#1.organizationName		= Second Organization Name (eg, company)
#1.organizationName_default	= World Wide Web Pty Ltd

organizationalUnitName		= Organizational Unit Name (eg, section)
#organizationalUnitName_default	=

commonName			= Common Name (e.g. server FQDN or YOUR name)
commonName_max			= 64

emailAddress			= Email Address
emailAddress_max		= 64

# SET-ex3			= SET extension number 3

[ req_attributes ]
challengePassword		= A challenge password
challengePassword_min		= 4
challengePassword_max		= 20

unstructuredName		= An optional company name

[ usr_cert ]

# These extensions are added when 'ca' signs a request.

# This goes against PKIX guidelines but some CAs do it and some software
# requires this to avoid interpreting an end user certificate as a CA.

basicConstraints=CA:FALSE

# Here are some examples of the usage of nsCertType. If it is omitted
# the certificate can be used for anything *except* object signing.

# This is OK for an SSL server.
# nsCertType			= server

# For an object signing certificate this would be used.
# nsCertType = objsign

# For normal client use this is typical
# nsCertType = client, email

# and for everything including object signing:
# nsCertType = client, email, objsign

# This is typical in keyUsage for a client certificate.
# keyUsage = nonRepudiation, digitalSignature, keyEncipherment

# This will be displayed in Netscape's comment listbox.
nsComment			= \"OpenSSL Generated Certificate\"

# PKIX recommendations harmless if included in all certificates.
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer

# This stuff is for subjectAltName and issuerAltname.
# Import the email address.
# subjectAltName=email:copy
# An alternative to produce certificates that aren't
# deprecated according to PKIX.
# subjectAltName=email:move

# Copy subject details
# issuerAltName=issuer:copy

#nsCaRevocationUrl		=
#nsBaseUrl
#nsRevocationUrl
#nsRenewalUrl
#nsCaPolicyUrl
#nsSslServerName

# This is required for TSA certificates.
# extendedKeyUsage = critical,timeStamping

[ v3_req ]

# Extensions to add to a certificate request

basicConstraints = CA:FALSE
[ v3_ca ]


# Extensions for a typical CA


# PKIX recommendation.

subjectKeyIdentifier=hash

authorityKeyIdentifier=keyid:always,issuer

# This is what PKIX recommends but some broken software chokes on critical
# extensions.
#basicConstraints = critical,CA:true
# So we do this instead.
basicConstraints = CA:true

# Key usage: this is typical for a CA certificate. However since it will
# prevent it being used as an test self-signed certificate it is best
# left out by default.
# keyUsage = cRLSign, keyCertSign

# Some might want this also
# nsCertType = sslCA, emailCA

# Include email address in subject alt name: another PKIX recommendation
# subjectAltName=email:copy
# Copy issuer details
# issuerAltName=issuer:copy

# DER hex encoding of an extension: beware experts only!
# obj=DER:02:03
# Where 'obj' is a standard or added object
# You can even override a supported extension:
# basicConstraints= critical, DER:30:03:01:01:FF

[ crl_ext ]

# CRL extensions.
# Only issuerAltName and authorityKeyIdentifier make any sense in a CRL.

# issuerAltName=issuer:copy
authorityKeyIdentifier=keyid:always

[ proxy_cert_ext ]
# These extensions should be added when creating a proxy certificate

# This goes against PKIX guidelines but some CAs do it and some software
# requires this to avoid interpreting an end user certificate as a CA.

basicConstraints=CA:FALSE

# Here are some examples of the usage of nsCertType. If it is omitted
# the certificate can be used for anything *except* object signing.

# This is OK for an SSL server.
# nsCertType			= server

# For an object signing certificate this would be used.
# nsCertType = objsign

# For normal client use this is typical
# nsCertType = client, email

# and for everything including object signing:
# nsCertType = client, email, objsign

# This is typical in keyUsage for a client certificate.
# keyUsage = nonRepudiation, digitalSignature, keyEncipherment

# This will be displayed in Netscape's comment listbox.
nsComment			= \"OpenSSL Generated Certificate\"

# PKIX recommendations harmless if included in all certificates.
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer

# This stuff is for subjectAltName and issuerAltname.
# Import the email address.
# subjectAltName=email:copy
# An alternative to produce certificates that aren't
# deprecated according to PKIX.
# subjectAltName=email:move
subjectAltName=\@alt_names

# Copy subject details
# issuerAltName=issuer:copy

#nsCaRevocationUrl		=
#nsBaseUrl
#nsRevocationUrl
#nsRenewalUrl
#nsCaPolicyUrl
#nsSslServerName

# This really needs to be in place for it to be a proxy certificate.
proxyCertInfo=critical,language:id-ppl-anyLanguage,pathlen:3,policy:foo

####################################################################
[ tsa ]

default_tsa = tsa_config1	# the default TSA section

[ tsa_config1 ]

# These are used by the TSA reply generation only.
dir		= ./		# TSA root directory
serial		= $dir/tsaserial	# The current serial number (mandatory)
crypto_device	= builtin		# OpenSSL engine to use for signing
signer_cert	= $dir/tsacert.pem 	# The TSA signing certificate
					# (optional)
certs		= $dir/cacert.pem	# Certificate chain to include in reply
					# (optional)
signer_key	= $dir/private/tsakey.pem # The TSA private key (optional)

default_policy	= tsa_policy1		# Policy if request did not specify it
					# (optional)
other_policies	= tsa_policy2, tsa_policy3	# acceptable policies (optional)
digests		= md5, sha1		# Acceptable message digests (mandatory)
accuracy	= secs:1, millisecs:500, microsecs:100	# (optional)
clock_precision_digits  = 0	# number of digits after dot. (optional)
ordering		= yes	# Is ordering defined for timestamps?
				# (optional, default: no)
tsa_name		= yes	# Must the TSA name be included in the reply?
				# (optional, default: no)
ess_cert_id_chain	= no	# Must the ESS cert id chain be included?
				# (optional, default: no)
[v3_sign]
{ocsp_url}
{crl_dist_points}
{basic_constraints}
        """
        context = {
            'cert_pem': self.ca_cert + '.pem',
            'private_key' : self.ca_cert + '-key.pem',
            'rand_file' : self.private + '/.rand',
            'ocsp_url' : ocsp_url,
            'crl_dist_points' : crl_dist_points,
            'basic_constraints' : 'basicConstraints=CA:TRUE'
        }
        with open('openssl.cnf.TRUE', 'w') as outfile:
            outfile.write(openssl_cnf_template.format(**context))
        outfile.close()
        self.linux_handle.log("Upload the conf file to linux host")
        if not self.linux_handle.upload(local_file='openssl.cnf.TRUE',\
           remote_file=self.ca_path + 'openssl.cnf.TRUE', protocol='scp', user='root', password='Embe1mpls'):
            raise Exception('Uploading openssl.cnf.TRUE failed')

        self.linux_handle.log('** *Create openssl.cnf.FALSE ** * ')
        crl_dist_points = 'crlDistributionPoints = URI:http://' + self.host_ip + '/pki-ocsp-crl-req/' \
                          + self.ca_cert + '-crl.pem'
        ocsp_url = 'authorityInfoAccess = OCSP;URI:http://' + self.host_ip + ':' + self.port_number
        context = {
            'cert_pem': self.ca_cert + '.pem',
            'private_key': self.ca_cert + '-key.pem',
            'rand_file': self.private + '/.rand',
            'ocsp_url': ocsp_url,
            'crl_dist_points': crl_dist_points,
            'basic_constraints': 'basicConstraints=CA:FALSE'
        }
        with open('openssl.cnf.FALSE', 'w') as outfile:
            outfile.write(openssl_cnf_template.format(**context))
        outfile.close()
        self.linux_handle.log("Upload the conf file to linux host")
        if not self.linux_handle.upload(local_file='openssl.cnf.FALSE',\
               remote_file=self.ca_path + 'openssl.cnf.FALSE', protocol='scp', user='root', password='Embe1mpls'):
            raise Exception('Uploading openssl.cnf.FALSE failed')

        return True

def gen_crl(linux_handle, **kwargs):
    """
    Generates crl for the given cert

    :param linux_handle:
        **REQUIRED** linux handle object

    :param cert_name:
        **REQUIRED** cert name

    :param days:
        *OPTIONAL* crl validity

    :param key_type:
        *OPTIONAL*  key_type (used in case of ecdsa)

    :param key_size:
        *OPTIONAL*  key_type (for ecdsa supported values, sha256/sha512)

        Default: sha256 (For ECDSA),  sha1(for RSA)

    :return: True on success, False on Failure

    EXAMPLE::

        Python:

           gen_crl(linux_handle, cert_name='test_root_ca')

        Robot:

           gen crl   ${linux_handle}  cert_name=test_root_ca
    """
    cert_name = ''
    if 'cert_name' in kwargs:
        cert_name = kwargs.get('cert_name')
    else:
        raise Exception("Missing required argument 'cert_name'")

    linux_handle.log("Switching user to root")
    linux_handle.su(password='Embe1mpls')
    certs = list()
    if isinstance(cert_name, list):
        certs.extend(cert_name)
    else:
        certs.append(cert_name)

    openssl_dir = kwargs.get('openssl_dir', '/etc/pki/script_gen')
    key_size = None
    if 'key_type' in kwargs and kwargs['key_type'] == 'ecdsa':
        key_size = kwargs.get('key_size', 'sha256')
    else:
        key_size = kwargs.get('key_size', 'sha1')

    crl_path = kwargs.get('crl_path', '/var/www/html/pki-ocsp-crl-req')
    days = kwargs.get('days', 365)

    for cert in certs:
        linux_handle.log("Modifying key size for crl")
        ca_openssl_cnf = openssl_dir + '/' + cert + '/openssl.cnf'
        if key_size is not None:
            cmd = "sed -i 's/default_md.*/default_md = " + key_size + "/g' " + ca_openssl_cnf
            linux_handle.log("Running " + cmd)
            linux_handle.shell(command=cmd)

        linux_handle.shell(command='cd ' + openssl_dir + '/' + cert)
        cmd = 'openssl ca -gencrl -out ' + crl_path + '/' + cert + '-crl.pem' +\
              ' -config ' + ca_openssl_cnf + ' -days ' + str(days)
        result = linux_handle.shell(command=cmd).response()
        if re.search(r'error', result):
            linux_handle.log(level='ERROR', message="Failed Generating crl " + result)
            raise Exception("Failed Generating cert request " + result)
        else:
            linux_handle.log("Crl generation successful for " + cert)
    linux_handle.shell(command='pushd ' + crl_path)
    linux_handle.shell(command='/etc/init.d/httpd stop')
    linux_handle.shell(command='/etc/init.d/httpd start')
    return True

def start_ocsp_responder(linux_handle, cert_name=None):
    """
    Starts oscp service for the cert

    :param linux_handle:
        **REQUIRED** linux handle object

    :param cert_name:
        **REQUIRED** cert_name

    :return: True on Success, False on Failure

    EXAMPLE::

         Python:

            start_ocsp_responder(linux_handle,cert_name='test_root_ca')

         Robot:

            start ocsp responder  ${linux_handle}  cert_name=test_root_ca
    """
    linux_handle.log("Switching user to root")
    linux_handle.su(password='Embe1mpls')
    cmd = 'cat  /etc/pki/script_gen/' + cert_name + '/openssl.cnf.FALSE |grep OCSP |cut -d : -f 4'
    result = linux_handle.shell(command=cmd).response()
    port = result.rstrip()
    linux_handle.log("Checking if responder is running with " + port + " number and killing it")
    cmd = "ps -ef | grep 'openssl ocsp' |grep " + port + " | awk {'print $2'} | xargs kill -9"
    linux_handle.shell(command=cmd)
    time.sleep(5) # so that port is free
    linux_handle.log("Starting ocsp responder")
    linux_handle.shell(command='cd /etc/pki/script_gen/'+ cert_name)
    cmd = 'openssl ocsp -index index.txt -CA ' + 'certs/' + cert_name + '.pem' + ' -rsigner certs/'\
          + cert_name + '.pem -rkey private/' + cert_name + '-key.pem -port ' + port + ' -text ' +\
          ' -out ocsp_' + cert_name + '.log &'
    result = linux_handle.shell(command=cmd, pattern=['-re',\
                       '(?:\e\[m)?[a-zA-Z0-9]+:\s*$', 'OCSP client connections']).response()
    if re.search(r'error', result):
        linux_handle.log(level='ERROR', message="Failed starting ocsp responder " + result)
        raise Exception("Failed starting ocsp responder " + result)
    return True

def revoke_cert(linux_handle, **kwargs):
    """
    Revokes the given cert

    :param linux_handle:
        **REQUIRED** linux handle object

    :param cert_name:
        **REQUIRED** cert name to be revoked

        Used to revoke ca cert

    :param local_cert:
        **OPTIONAL** local cert name to be revoked.

        Used to revoke only revoke local cert

    :return: True on Success , Raise exception on failure

    EXAMPLE::
        revoke cert  ${linux_handle}  cert_name=test_root_ca
    """
    parent_cert = ''
    if 'cert_name' not in kwargs:
        raise Exception("required argument missing 'cert_name'")
    linux_handle.log("Switching user to root")
    linux_handle.su(password='Embe1mpls')
    cert_name = kwargs.get('cert_name')
    ocsp = kwargs.get('ocsp', 0)
    crl_path = "/var/www/html/pki-ocsp-crl-req"
    openssl_dir = kwargs.get('openssl_dir', '/etc/pki/script_gen')
    ca_openssl_cnf = openssl_dir + '/' + cert_name + '/' + 'openssl.cnf'
    cert_file_path = openssl_dir + '/' + cert_name + '/' + 'certs/' + cert_name + '.pem'
    cert_key = openssl_dir + '/' + cert_name + '/' + 'private/' + cert_name + '-key.pem'

    if 'local_cert' in kwargs:
        local_cert = kwargs['local_cert']
        index_file = openssl_dir + '/' + cert_name + '/' + 'index.txt'
        linux_handle.shell(command='cd ' + openssl_dir + '/' + cert_name)
        if not linux_handle.download(remote_file=index_file, local_file='index.txt', protocol='scp'):
            raise Exception('Downloading index file failed: ' + index_file)
        try:
            OUT = open("newindex.txt", "w")  # or "a+", whatever you need
        except IOError:
            linux_handle.log("Could not open file newindex.txt")
            raise
        try:
            IN = open("index.txt", "r")  # or "a+", whatever you need
        except IOError:
            linux_handle.log("Could not open file index.txt")
            raise
        for line in  IN.readlines():
            if local_cert in line:
                (status, not_after, serial_num, unknown, subject, empty) = re.split(r'\s+', line)
                date = linux_handle.shell(command='date +%y%m%d%H%M%S').response()
                date = date.rstrip()
                if 'date' in date:
                    date = date.split("\n")[1]
                OUT.write("R\t" + not_after + "\t" + date + "\t" + serial_num + "\t" + \
                          "unknown\t" + subject + "\n")
            else:
                OUT.write(line)
        IN.close()
        OUT.close()
        new_index = openssl_dir + '/' + cert_name + '/' + 'newindex.txt'
        if not linux_handle.upload(local_file='newindex.txt', remote_file=new_index,
                                   protocol='scp', user='root', password='Embe1mpls'):
            linux_handle.log("Uploading newindex file failed" + new_index)
            raise Exception("Uploading request file failed " + new_index)
        linux_handle.shell(command='mv -f index.txt index.txt.old')
        linux_handle.shell(command='mv -f newindex.txt index.txt')
        linux_handle.shell(command="echo 'unique_subject = yes' > index.txt.attr")
        parent_cert = cert_name
    else:
        cmd = 'openssl x509 -in ' + cert_file_path + ' -noout -issuer'
        result = linux_handle.shell(command=cmd).response()
        m = re.search("issuer=.*CN=(.*)", result)
        parent_cert = m.group(1)
        linux_handle.log("Parent cert for the " + cert_name + 'is ' + parent_cert)
        linux_handle.shell(command='cd ' + openssl_dir + '/' + parent_cert)
        cmd = 'openssl ca -config ' + ca_openssl_cnf + ' -revoke ' + cert_file_path + \
              ' -keyfile ' + cert_key + ' -cert ' + cert_file_path
        result = linux_handle.shell(command=cmd).response()
        if re.search(r'error', result):
            linux_handle.log(level='ERROR', message="Failed to revoke cert " + result)
            raise Exception("Failed to revoke cert " + result)

    linux_handle.log("Regnerating the crl")
    cmd = 'openssl ca -gencrl -out ' + crl_path + '/' + parent_cert + '-crl.pem' + \
          ' -config ' + openssl_dir + '/' + parent_cert + '/' + 'openssl.cnf'
    linux_handle.log('Running ' + cmd)
    result = linux_handle.shell(command=cmd).response()
    if re.search(r'error', result):
        linux_handle.log(level='ERROR', message="Failed to re-generate crl " + result)
        raise Exception("Failed to re-generate crl " + result)

    linux_handle.shell(command='pushd ' + crl_path)
    linux_handle.shell(command='/etc/init.d/httpd restart')
    if ocsp == 1:
        start_ocsp_responder(linux_handle, parent_cert)
    return True

#update_index_file(linux_handle,'cert','index file')
def update_index_file(linux_handle, cert_file, index_file):
    """
        Updates index file (index.txt)
    :param linux_handle:
    :param cert_file:
    :param index_file:
    :return:
    """
    linux_handle.log("Updating index file")
    linux_handle.log("Switching user to root")
    linux_handle.su(password='Embe1mpls')
    cmd = 'openssl x509 -in ' + cert_file + ' -noout  -dates -serial -subject'
    linux_handle.log("Running " + cmd)
    result = linux_handle.shell(command=cmd).response()
    linux_handle.log(result)
    #mat = re.match('notBefore=(.*)\r\nnotAfter=(.*)\r\nserial=(.*)\r\nsubject= (.*)\r', result)
    mat = re.match('notBefore=(.*)[\r\n]?notAfter=(.*)[\r\n]?serial=(.*)[\r\n]?subject= (.*)', result)
    if not mat:
        linux_handle.log('Didnot match result from cert : ' + result)
        raise Exception('Matching cert content failed: ' + result)
    not_before = mat.group(1).rstrip()
    not_after = mat.group(2).rstrip()
    serial = mat.group(3).rstrip()
    subject = mat.group(4).rstrip()
    not_before = get_timestamp(not_before)
    not_after = get_timestamp(not_after)
    linux_handle.log("Downloading index.txt")
    if not linux_handle.download(remote_file=index_file, local_file='index.txt', protocol='scp'):
        linux_handle.log('Downloading index file failed: ' + index_file)
        raise Exception('Downloading index file failed: ' + index_file)
    with open("index.txt", "a") as myfile:
        myfile.write("V\t"+ not_after + "\t\t" + serial + "\tunknown\t" + subject + "\n")
    myfile.close()
    if not linux_handle.upload(local_file='index.txt', remote_file=index_file, protocol='scp', user='root', password='Embe1mpls'):
        linux_handle.log("Uploading index file failed" + index_file)
        raise Exception("Uploading request file failed" + index_file)
    return True

#function gets time stamp in format index.txt accepts
def get_timestamp(date_str):
    """
        Converts Date into the format required by index.txt
    :param date_str:
    :return:
    """
    (month, date, time, year, zone) = re.split(" +", date_str)
    print(zone)
    monthDict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    month_num = monthDict[month]
    time = time.replace(':', '')
    if len(date) < 2:
        date = '0' + date
    timestamp = year[2:] + month_num + date + time + 'Z'
    return  timestamp

# wrapper functions for robo keywords
def create_openssl_object(linux_handle, **kwargs):
    """
        creates openssl object

        :param linux_handle:
            **REQUIRED** linux handle object

        :param cert_name:
            **REQUIRED**  Certificate name

        :param key_size:
            **OPTIONAL** key size

            Supported values 256/1024/2048/

            Default: 1024

        :param key_type:
            **OPTIONAL** Algorithm for encrypting public private keys

            Supported values rsa/dsa/ecdsa256/ecdsa384

            Default : rsa

        :param crl_path:
            **OPTIONAL** crl directory on linux machine

            Default: /var/www/html/pki-ocsp-crl-req

        :param self_sign:
            **OPTIONAL** creates chain cert or self sign cert

            Supported values 1/0

            Default: 1 (self signed cert)

        :param days:
            **OPTIONAL** Validity of cert

            Default: 365

        :param port_number:
            **OPTIONAL**  port number for ocsp responder

            Default: 8400

        :param parent_cert:
            **OPTIONAL** parent cert for non self signed cert

            Parent cert is required if self_sign=0

        :return: Openssl object

        EXAMPLE::

             ${openssl_obj} =  Create openssl object  ${lnx_handle}  cert_name=ecdsa_256_cert  key_size=256  key_type=ecdsa  port_number=8401

    """
    return Openssl(linux_handle, **kwargs)

def generate_openssl_ca_cert(openssl_obj, **kwargs):
    """
        This routine creates openssl ca certifciate

        :param hash_algo:
            *OPTIONAL*  applies only ofr rsa key type

            Supported values -md5|-sha1|-mdc2

        :return: True on Success , False on Failure

        EXAMPLE::
             Generate openssl ca cert   ${openssl_obj}
    """
    return openssl_obj.gen_openssl_ca_cert(**kwargs)

def generate_cert_request(openssl_obj, rh, **kwargs):
    """
        This routine generates Local certifciate request

        :param router_handle/linux_handle:

            **REQUIRED** router handle object or linux_handle based on
            where to generate cert request

        :param cert_id:
            **REQUIRED** Local cert name

        :param gen_on:
            *OPTIONAL* where to generate certifcate request

            Supported values router/strongswan/openssl

            Default: router

        :param key_size:
            *OPTIONAL* key size

            Default: takes from create_openssl_object

        :param ip:
            *OPTIONAL* Static IP address of the device

            Gets added to alt subjectname

        :param domain_name:
            *OPTIONAL* FQDN to be added in SubjectAltName

        :return: True on Success , False on failure

        EXAMPLE::
              In case of Router:

                Generate_cert_request   ${device_handle}  cert_id=local_certmx  domain_name=test.juniper.net

              In case of Strongswan:

               Generate_cert_request   ${openssl_obj}  ${linux_handle}  cert_id=local_certmx  domain_name=test.juniper.net  gen_on=strongswan
    """
    return  openssl_obj.gen_cert_req(rh, **kwargs)

def load_ca_cert(openssl_obj, **kwargs):
    """
        This routine loads  ca certifciate on router
        :param device_handle
             *OPTIONAL/REQUIRED*  this is a router handle required if generate_cert_request not called
        :param cert_file:
            *OPTIONAL* cert file name to be loaded

        :return: True on Success , False on Failure

        EXAMPLE::
           1) Not called generate_cert_request

             load ca cert    ${openssl_obj}  device_handle=${router_handle}
    """
    return  openssl_obj.load_cert(**kwargs)


def sign_and_load_cert(openssl_obj, **kwargs):
    """
        This routine signs certifciate and loads the certs

        :param device_handle

             *OPTIONAL/REQUIRED*  this is a router handle required if gen_cert_request not called

        :param load_cert:

            *OPTIONAL*  sign and load both certs on router

            Supported values 1/0

            Default: 1

        :return: True on Success , False on Failure

        EXAMPLE::

             Sign_and_load_cert   ${openssl_obj}
    """
    return  openssl_obj.sign_cert(**kwargs)

"""
#if __name__ == '__main__':
#    linux_handle = Unix(host='vpn-lnx9', user='root', password='Embe1mpls')
#    rh = Device(host='mojito', os='JUNOS', user='regress', password='MaRtInI')

    #import pdb
    #pdb.set_trace()
#    cmdlist = ['clear security pki ca-certificate all',
#               'clear security pki local-certificate all',
#               'clear security pki certificate-request all',
#              'clear security pki key-pair all']

#    config_cmd = ['set security pki ca-profile test_root_ca ca-identity test_root_ca',
#               'set security pki traceoptions flag all',
#                'set security pki ca-profile test_root_ca revocation-check use-ocsp',
#               'commit']

#    for cmd in cmdlist:
#        rh.cli(command=cmd)

#    rh.config(command_list=config_cmd)

    #openssl_obj = Openssl(linux_handle , cert_name='test_root_ca', key_type='ecdsa', key_size='256')
    #openssl_obj = Openssl(linux_handle, cert_name='test_ca_check', self_sign=0, parent_cert='openssl_root1')
#    openssl_obj = Openssl(linux_handle, cert_name='test_root_ca', self_sign=1)
#    openssl_obj.gen_openssl_ca_cert()
#    openssl_obj.gen_cert_req(rh, cert_id='local_mojito', domain_name='test.juniper.net')
#    openssl_obj.sign_cert()


#    rh_amrut = Device(host='negroni', os='JUNOS', user='regress', password='MaRtInI')
#    for cmd in cmdlist:
#        rh_amrut.cli(command=cmd)

#    rh.config(command_list=config_cmd)

#    openssl_obj = Openssl(linux_handle, cert_name='test_root_ca', self_sign=1)
#    openssl_obj.gen_cert_req(rh_amrut, cert_id='local_neg', domain_name='test.juniper.net')
#    openssl_obj.sign_cert()
    #import pdb
    #pdb.set_trace()
#    gen_crl(linux_handle,cert_name='test_root_ca')
    #import pdb
    #pdb.set_trace()
#    start_ocsp_responder(linux_handle,'test_root_ca')

    #import pdb
    #pdb.set_trace()
    #revoke_cert(linux_handle,local_cert='local_test1', cert_name='test_root_ca1', ocsp=1)

    #openssl_obj.load_cert()

    #update_index_file(linux_handle,'/etc/pki/script_gen/test_root_ca1/certs/test_root_ca1.pem',
    #              '/etc/pki/script_gen/test_root_ca1/index.txt')
    #gen_crl(linux_handle,cert_name=['test_root_ca'])
"""
