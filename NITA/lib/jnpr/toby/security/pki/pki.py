"""
=============================================================================
         FILE:  pki.py
  DESCRIPTION:  PKI generic APIs
       AUTHOR:  Niketa Chellani, nchellani@juniper.net
=============================================================================
"""
import re
import time
import jxmlease

class Pki(object):
    """
    Pki library class to define pki related keywords for Toby
    """
    def __init__(self, device_handle):
        """
        :param host:
            **REQUIRED** device hostname
        :param user:
            **OPTIONAL** login username
        :param password:
            **OPTIONAL** login password
        """

        self.handle = device_handle

    def set_ca_profile(self, **kwargs):
        """
        Configures CA Profile on device
        Can be called using wrapper function configure_ca_profile
            :param ca_profile:
            **REQUIRED** Name of CA Profile
            :param url:
                **REQUIRED** Enrollment URL
            :param ca_identity:
                **OPTIONAL** Identity name of CA. Default is ca_profile
            :param retry:
                **OPTIONAL** No. of retries. Default is 5
            :param retry_interval:
                **OPTIONAL** Interval between retries. Default is 0
            :param revocation_check:
                **OPTIONAL** can be use-crl, use-ocsp, crl, ocsp, disable
            :param crl_url:
                **OPTIONAL** CRL URL
            :param refresh_interval:
                **OPTIONAL** Tells when to refresh the CRL
            :params timeout:
                ***OPTIONAL*** Timeout to commit the configuration. Default is 300

             === OCSP params===
            :param ocsp_url:
                **OPTIONAL** OCSP URL
            :param nonce_payload:
                **OPTIONAL**

            :param conection_failure:
                **OPTIONAL** OCSP Connnection failure: Values can be disable/ fallback-crl
                Example of config statements:
                set security pki ca-profile root1 revocation-check use-ocsp ocsp connection-failure disable  "or"
                set security pki ca-profile root1 revocation-check use-ocsp ocsp connection-failure fallback-crl

            :param nonce_payload
                ***OPTIONAL*** Value can be enable/disable
                Example of config statement:
                    set security pki ca-profile root1 revocation-check use-ocsp ocsp nonce-payload enable
                    set security pki ca-profile root1 revocation-check use-ocsp ocsp nonce-payload disable

            :param disable-responder-revocation-check
                ***OPTIONAL*** Value can be True (if this knob has to be configured. Otherwise, do not supply this to the kwargs)
                Example of config statement:
                    set security pki ca-profile root1 revocation-check use-ocsp ocsp disable-responder-revocation-check
            ===================
            :param routing_instance:
                **OPTIONAL** routing instance
            :param apply_groups:
                **OPTIONAL***
            :param apply_groups_except:
                **OPTIONAL**
            :param administrator:
                **OPTIONAL**
            :param traceoptions:
                **OPTIONAL**
            :param flag:
                **OPTIONAL** traceoption flag level
            :param file:
                **OPTIONAL** file where logs will be saved

            :returns
                True/ False
        """
        self.handle.log(level="INFO", message="----------------------------------\n")
        self.handle.log(level="INFO", message="\tCREATING NEW CA PROFILE")
        self.handle.log(level="INFO", message="----------------------------------\n")
        cmdlist = []
        response = False
        ca_profile = kwargs.get('ca_profile')
        ca_identity = kwargs.get('ca_identity', ca_profile)
        retry = kwargs.get('retry', 5)
        retry_interval = kwargs.get('retry_interval', 0)
        timeout = kwargs.get('timeout', 300)

        kwargs.get('url')
        kwargs.get('file')
        kwargs.get('administrator')
        kwargs.get('nonce_payload')
        kwargs.get('disable_responder_revocation_check')
        kwargs.get('apply_groups')
        kwargs.get('apply_groups_except')
        kwargs.get('connection_failure')
        kwargs.get('traceoptions')
        kwargs.get('routing_instance')

        cmd = "set security pki ca-profile "+ca_profile+" ca-identity "+ca_identity
        cmdlist.append(cmd)
        if 'url' in kwargs:
            cmdlist.append(cmd+" enrollment url "+kwargs['url']+" retry "+str(retry)+" retry-interval "+str(retry_interval))

        if 'revocation_check' in kwargs:
            if re.match('disable', kwargs['revocation_check'], re.IGNORECASE):
                cmdlist.append(cmd+' revocation-check disable')

            elif re.search('.*crl.*', kwargs['revocation_check'], re.IGNORECASE):
                self.handle.log(level="INFO", message="----CRL Revocation check is set -----\n")
                cmdlist.append(cmd+" revocation-check use-crl")

                if 'crl_url' in kwargs:
                    cmdlist.append(cmd+'  revocation-check crl url '+kwargs['crl_url'])
                if 'refresh_interval' in kwargs:
                    cmdlist.append(cmd+'  revocation-check crl refresh-interval '+str(kwargs['refresh_interval']))
            elif re.search('.*ocsp.*', kwargs['revocation_check'], re.IGNORECASE):
                self.handle.log(level="INFO", message="----OCSP Revocation check is set -----\n")
                revoc_ocsp = cmd +' '+ 'revocation-check use-ocsp ocsp '
                cmdlist.append(cmd+' '+'revocation-check use-ocsp ocsp')

                if 'ocsp_url' in kwargs:
                    cmdlist.append(revoc_ocsp +' '+'url'+' '+ kwargs['ocsp_url'])
                if 'nonce_payload' in kwargs:
                    cmdlist.append(revoc_ocsp +' '+'nonce-payload'+' '+kwargs['nonce_payload'])
                if 'disable_responder_revocation_check' in kwargs:
                    cmdlist.append(revoc_ocsp+' '+'disable-responder-revocation-check')
                if 'connection_failure' in kwargs:
                    conn_failure = revoc_ocsp+' '+'connection-failure'
                    if re.search('.*fallback.*', kwargs['connection_failure'], re.IGNORECASE):
                        cmdlist.append(conn_failure +' '+'fallback-crl')
                    elif re.search('.*disable.*', kwargs['connection_failure'], re.IGNORECASE):
                        cmdlist.append(conn_failure +' '+'disable')
                    else:
                        cmdlist.append(conn_failure)

        if 'apply_groups' in kwargs:
            cmdlist.append(cmd+' apply-groups '+kwargs['apply_groups'])
        if 'apply_groups_except' in kwargs:
            cmdlist.append(cmd+' apply-groups-except '+kwargs['apply_groups_except'])
        if 'administrator' in kwargs:
            cmdlist.append(cmd+' administrator '+kwargs['administrator'])
        if 'traceoptions' in kwargs:
            cmd = "set security pki traceoptions flag "
            if 'flag' in kwargs:
                if not isinstance(kwargs['flag'], (list, tuple)):
                    cmdlist.append(cmd +kwargs['flag'])
                elif isinstance(kwargs['flag'], (list, tuple)):
                    for val in kwargs['flag']:
                        cmdlist.append(cmd+str(val))
                else:
                    cmdlist.append(cmd+'all')
            if 'file' in kwargs:
                if not isinstance(kwargs['flag'], (list, tuple)):
                    cmdlist.append("set security pki traceoptions flag all")
                else:
                    for key in kwargs['file']:
                        cmdlist.append("set security pki traceoptions"+' file '+kwargs['file'][key])


        self.handle.log("Configuring ca profile "+str(cmdlist))
        self.handle.config(command_list=cmdlist)
        result = self.handle.commit(timeout=timeout)
        response = result
        return response

def add_to_trusted_ca_group(handle, **kwargs):
    """
        Adds given ca profiles to trusted ca group
        :param handle:
            **REQUIRED** device handle

        :param trusted_ca_group:
            **REQUIRED**  Trusted ca group name

        :param ca_profiles:
            **REQUIRED**  one or more ca-profile names

        :param commit:
            **OPTIONAL**  commit after configuring
            Supported values:  True/False , default: False

        :param err_level
                ***OPTIONAL*** Log Level while displaying log messages. Values can be INFO/ERROR. Default is ERROR.
        :return:
            True on Success
            Raise exception on Failure

        EXAMPLE::
            PYTHON:
              add_to_trusted_ca_group(device_handle, trusted_ca_group='TG1', ca_profiles='Root')

            ROBOT:
              add_to_trusted_ca_group   ${device_handle}  trusted_ca_group=TG1  ca_profiles=Root

              To add mulitple ca profiles to group

              ${ca_list} =  create list  comcast_root   verizon_root
              add_to_trusted_ca_group   ${device_handle}  trusted_ca_group=TG1  ca_profiles=${ca_list}
    """

    err_level = kwargs.get('err_level', 'ERROR')
    if 'trusted_ca_group' not in kwargs or 'ca_profiles' not in kwargs:
        raise Exception("Mandatory arguments 'trusted_ca_group' or 'ca_profiles'  missing")

    cmdlist = []
    commit = kwargs.get('commit', False)
    cmd = 'set security pki trusted-ca-group '+kwargs['trusted_ca_group']+' ca-profiles '
    if isinstance(kwargs['ca_profiles'], list):
        for ca_profile in kwargs['ca_profiles']:
            cmdlist.append(cmd+ca_profile)
    else:
        cmdlist.append(cmd+kwargs['ca_profiles'])

    try:
        handle.log("Configuring ca profile "+str(cmdlist))
        response = handle.config(command_list=cmdlist)
        if commit:
            return handle.commit()
        return  response
    except Exception as except_error:
        handle.log(level=err_level, message=except_error)
        raise Exception("error configuring: "+str(except_error))

def enroll_ca_cert(handle, **kwargs):
    """
        Requests CA certificate and enrolls it

        :param handle:
            **REQUIRED** Router handle

        :param
            ca_profile: **REQUIRED** Name of CA Profile.

        :param filename:
            **OPTIONAL** file CA certificate can be enrolled from

        :param wait_time:
            ***OPTIONAL*** Time (in sec) to wait before enrollment of certificate is attempted again. Default is 5s

        :param timeout:
            ***OPTIONAL**** Timeout (in sec) while enroling CA cert. Default value is 300s

         :param max_retries:
             ***OPTIONAL*** Maximum number of times, certificate enrollment is attempted. Default is 1

        :param err_level
                ***OPTIONAL*** Log Level while displaying log messages. Values can be INFO/ERROR. Default is ERROR.

        :return
               Returns true if enrolled successfully else False
        EXAMPLE::

            PYTHON:
              enroll_ca_cert(device_handle, ca_profile='Root')

            ROBOT:
              enroll ca cert   ${device_handle}  ca_profile=Root

                device>request security pki ca-certificate enroll ca-profile Root

                Fingerprint:
                  48:ad:39:fa:66:07:c2:f8:bb:ee:d8:f0:fa:68:dc:26:32:a5:b5:a8 (sha1)
                  cc:19:2c:fb:f1:de:ef:c5:78:03:ae:3d:d0:15:87:17 (md5)
                Do you want to load the above CA certificate ? [yes,no] (no) yes

                CA certificate for profile Root loaded successfully
    """

    handle.log(level="INFO", message="--------------------------------\n")
    handle.log(level="INFO", message="\tENROLLING CA CERTIFICATE")
    handle.log(level="INFO", message="---------------------------------\n")
    cmdlist = []
    response = True

    ca_profile = kwargs.get('ca_profile')
    filename = kwargs.get('filename')
    wait_time = kwargs.get('wait_time', 5)
    timeout = kwargs.get('timeout', 300)
    max_retries = kwargs.get('max_retries', 1)
    err_level = kwargs.get('err_level', 'ERROR')

    if 'ca_profile' in kwargs and 'filename' in kwargs:
        cmdlist.append(
            'request security pki ca-certificate load ca-profile '+ca_profile+' filename ' +
            filename)
    elif 'ca_profile' in kwargs and ca_profile != None:
        cmdlist.append('request security pki ca-certificate enroll ca-profile '+ca_profile)
    elif 'ca_profile' not in kwargs:
        response = False
        cmdlist.append('request security pki ca-certificate enroll ca-profile') 
    check_chassis = _check_chassis_cluster(handle)
    while max_retries:
        if check_chassis:
            handle.log(level="INFO", message="Device is in HA")
            result = handle.cli(command=cmdlist[0], timeout=timeout, format="text").response()
        else:
            handle.log(level="INFO", message="Device is not in HA")
            handle.cli(command=cmdlist[0], pattern="[yes,no]")
            result = handle.cli(command="yes").response()
        time.sleep(wait_time)
        max_retries -= 1

    if re.search('.*loaded successfully.*', str(result)):
        handle.log(level="INFO", message="--Enrolled CA certificate %s successfully--\n"%ca_profile)
        response = True
    elif re.search('.*already exists.*', str(result)):
        handle.log(level="INFO", message="-- CA certificate %s already exists. Please clear CA certs before trying to enroll again--\n"%ca_profile)
        response = False
    elif re.search('.*syntax error.*', str(result)):
        handle.log(level=err_level, message="--Syntax Error --\n")
        response = False
    else:
        handle.log(level=err_level, message="--Failed to enroll CA certificate %s --\n"%ca_profile)
        response = False

    return response

def verify_ca_cert(handle, **kwargs):
    """
        Verifies CA certificate

           :param handle:
               **REQUIRED** Router handle

           :param ca_profile:
               **REQUIRED** Name of CA Profile.

           :param wait_time:
               **OPTIONAL** Default value is 30

           :param max_retries:
               **OPTIONAL** Default value is 2

           :param timeout:
               **OPTIONAL** Default value is 120

           :param err_level
                ***OPTIONAL*** Log Level while displaying log messages. Values can be INFO/ERROR. Default is ERROR

           :param expect_string:
               **OPTIONAL** Default value is 'OCSP certificate validation successful'

           :return
               Returns true if verified successfully else False

           EXAMPLE::
                PYTHON:
                    verify_ca_cert(device_handle, ca_profile='Root')

                ROBOT:
                    verify ca cert  ${device_handle}  ca_profile=Root
                    device>request security pki ca-certificate verify ca-profile Root
                    CA certificate Root verified successfully
    """

    handle.log(level="INFO", message="----------------------------------\n")
    handle.log(level="INFO", message="\tVERIFYING CA CERTIFICATE")
    handle.log(level="INFO", message="----------------------------------\n")

    ca_profile = kwargs.get('ca_profile')
    max_retries = kwargs.get('max_retries', 2)
    wait_time = kwargs.get('wait_time', 5)
    timeout = kwargs.get('timeout', 120)
    err_level = kwargs.get('err_level', 'ERROR')
    expect_string = kwargs.get('expect_string', 'OCSP certificate validation successful')
    response = False

    handle.cli(command='clear log pkid', format='text')
    handle.cli(command='clear log messages', format='text')

    while max_retries > 0:
        cmd = 'request security pki ca-certificate verify ca-profile '+ca_profile
        result = handle.cli(dummy=None, command=cmd, timeout=timeout, format="text", pattern=None)

        result = result.response()
        if re.search('.*successfully.*', str(result)):
            handle.log(level="INFO", message="--Verified CA certificate %s successfully--n"%ca_profile)
            response = True
            break
        elif re.search(".*not configured.*", str(result)):
            handle.log(level=err_level, message="--CA Certificate %s verification failed because CA profile is not configured--\n"%ca_profile)
            response = False
            break
        elif re.search(".*doesn't exist.*", str(result)):
            handle.log(level=err_level, message="--CA Certificate %s verification failed. The certificate does not exist.--\n"%ca_profile)
            response = False
        elif re.search(".*Error: CRL download failed for certficate.*", str(result)):
            handle.log(level=err_level, message="--CA Certificate %s verification failed because CRL download failed--\n"%ca_profile)
            response = False
        elif re.search('.*Revocation check is in progress.*', str(result), re.IGNORECASE):
            time.sleep(wait_time)
            handle.log(level="INFO", message="--Checking PKID logs for completion status--\n")
            out = _verify_ocsp_cert(handle, expect_string, ca_profile=ca_profile)
            response = out

        max_retries -= 1
        handle.log(level="INFO", message="---Sleeping for %s seconds---\n"%str(wait_time))
        time.sleep(wait_time)

    return response

def get_ca_cert(handle, **kwargs):
    """
            Shows CA certificate details

            :param handle:
                **REQUIRED** Router handle

            :param ca_profile:
                 **OPTIONAL** Name of CA Profile.

            :param detail:
                **OPTIONAL** Default value is terse i.e. 0. To enable detailed certificate assign 1

            :return
               Returns dictionary with each parameter of the certificate
                or a list of certificate dictonaries if the ca_profile is not mentioned and more than one
                ca-profiles are configured on device

            EXAMPLE::

                PYTHON:
                    get_ca_cert(device_handle, ca_profile='Root', detail=1)

                ROBOT:
                    get ca cert   ${device_handle}  ca_profile=Root  detail=1

                Parses below output into a dictonary

                device>show security pki ca-certificate ca-profile Root detail|display xml
                <rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1X49/junos">
                    <x509-pki-certificate-info-list xmlns="http://xml.juniper.net/junos/15.1X49/junos-pki">
                        <pkid-x509-certificate-information junos:style="detail">
                            <identifier>Root</identifier>
                            <version>3</version>
                            <serial-number-list>
                                <serial-number-x509>00000d5f</serial-number-x509>
                            </serial-number-list>
                            <issuer-name>
                                <distinguished-name>
                                    <organization-name>juniper</organization-name>
                                    <common-name>Root</common-name>
                                    <country-name>us</country-name>
                                </distinguished-name>
                            </issuer-name>
                            <subject-name>
                                <distinguished-name>
                                    <organization-name>juniper</organization-name>
                                    <common-name>Root</common-name>
                                    <country-name>us</country-name>
                                </distinguished-name>
                            </subject-name>
                            <subject-string-list>
                                <subject-string>C=us, O=juniper, CN=Root</subject-string>
                            </subject-string-list>
                            <validity>
                                <not-before>04- 3-2017 09:13 UTC</not-before>
                                <not-after>04- 3-2018 09:13 UTC</not-after>
                            </validity>
                            <public-key>
                                <public-key-algorithm>rsaEncryption</public-key-algorithm>
                                <public-key-length>2048</public-key-length>
                            </public-key>
                            <public-key-contents-list>
                                <key-contents>30:82:01:0a:02:82:01:01:00:cb:a1:46:43:7c:dc:50:6e:02:31:1e
                                    39:3f:bc:41:fc:e5:f9:2d:11:97:05:b5:8a:16:43:79:cf:87:87:0f
                                    d0:08:a4:6c:60:5d:08:e5:34:f7:aa:03:27:67:93:bc:a0:be:c2:95
                                    24:6c:00:31:51:68:f0:a6:d5:c1:87:c5:33:e2:84:75:6a:5e:11:6c
                                    45:d3:da:87:c1:a9:13:d1:ab:bc:14:3c:53:09:ef:5d:52:65:df:d3
                                    5d:c6:2f:c8:dc:2d:fb:19:08:5c:10:5e:32:fe:ae:c2:a7:16:5e:9a
                                    8d:cb:3e:f7:6b:92:2f:8b:54:7b:55:bb:40:c2:0a:99:ec:f0:ec:56
                                    ee:74:29:29:0a:a0:ac:b0:e7:01:ea:fe:99:fc:3c:ca:a0:92:80:4b
                                    25:53:e6:1c:0d:34:b1:6f:13:67:cf:1b:c7:84:7d:f2:f8:57:35:03
                                    17:40:47:3a:9d:d1:1c:88:a7:fe:3d:0b:80:9c:86:b7:e1:71:44:df
                                    9a:0b:25:05:a3:f6:08:e4:b9:d8:f3:f7:31:7a:dd:ac:01:5c:27:25
                                    26:89:0f:53:95:2a:5b:28:d3:b7:02:a5:3a:7a:13:8b:44:23:98:7c
                                    4a:e7:59:04:d5:a1:61:bd:62:15:7d:7a:18:82:b0:26:f4:7e:4c:50
                                    74:43:9c:eb:55:02:03:01:00:01</key-contents>
                                </public-key-contents-list>
                                <signature-algorithm>sha256WithRSAEncryption</signature-algorithm>
                                <distribution-crl-list>
                                    <distribution-crl>http://10.204.128.120:8080/crl-as-der/currentcrl-292.crl?id=292</distribution-crl>
                                </distribution-crl-list>
                                <authority-information-access-ocsp-list>
                                    <authority-information-access-ocsp>http://10.204.128.120:8090/Root/</authority-information-access-ocsp>
                                </authority-information-access-ocsp-list>
                                <key-usage-list>
                                    <key-usage>CRL signing</key-usage>
                                    <key-usage>Certificate signing</key-usage>
                                    <key-usage>Key encipherment</key-usage>
                                    <key-usage>Digital signature</key-usage>
                                </key-usage-list>
                                <fingerprint>
                                    <fingerprint-content>48:ad:39:fa:66:07:c2:f8:bb:ee:d8:f0:fa:68:dc:26:32:a5:b5:a8</fingerprint-content>
                                    <fingerprint-hash-algorithm>sha1</fingerprint-hash-algorithm>
                                    <fingerprint-content>cc:19:2c:fb:f1:de:ef:c5:78:03:ae:3d:d0:15:87:17</fingerprint-content>
                                    <fingerprint-hash-algorithm>md5</fingerprint-hash-algorithm>
                                </fingerprint>
                            </pkid-x509-certificate-information>
                        </x509-pki-certificate-info-list>
                        <cli>
                            <banner></banner>
                        </cli>
                    </rpc-reply>

                    =============================================================================
                    Returned Dictionary:

                    {'Root': {'validity-not-after': '04- 3-2018 09:13 UTC', 'recipient': '',
                    'public-key-algorithm': 'rsaEncryption', 'signature-algorithm': 'sha256WithRSAEncryption',
                    'public-key-length': '2048', 'serial-number': '00000d5f', 'validity-not-before': '04- 3-2017 09:13 UTC', 'issued-by': ''}}

    """

    handle.log(level="INFO", message="---------------------------------------\n")
    handle.log(level="INFO", message="\tDISPLAYING CA CERTIFCATE DETAILS")
    handle.log(level="INFO", message="---------------------------------------\n")

    if 'ca_profile' in kwargs:
        cmd = 'show security pki ca-certificate ca-profile '+kwargs['ca_profile']
        ca_profile = kwargs['ca_profile']
    else:
        cmd = 'show security pki ca-certificate'
        ca_profile = None

    if 'detail' in kwargs:
        if kwargs['detail'] == 1:
            cmd = cmd+' detail'

    ca_xml = handle.cli(command=cmd, format="xml").response()
    ca_dict = jxmlease.parse(ca_xml)

    try:
        if 'ca_profile' in kwargs:
            #=======================================================================
            #       For device in cluster mode and ca-profile is given
            #=======================================================================
            if 'multi-routing-engine-results' in ca_dict['rpc-reply']:
                if str(ca_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['x509-pki-certificate-info-list']) != '':
                    extracted_cert = (ca_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['x509-pki-certificate-info-list']['pkid-x509-certificate-information'])
                    extracted_cert = dict(extracted_cert)
                    ca_id_dict = _generating_cert_details(ca_profile, extracted_cert)
                    handle.log(level="INFO", message="--CA profile %s details:--\n"%kwargs['ca_profile'])
                    return ca_id_dict

            #=======================================================================
            #      For device in non-cluster mode and ca-profile is given
            #=======================================================================
            else:
                if str(ca_dict['rpc-reply']['x509-pki-certificate-info-list']) != '':
                    extracted_cert = (ca_dict['rpc-reply']['x509-pki-certificate-info-list']['pkid-x509-certificate-information'])
                    extracted_cert = dict(extracted_cert)
                    ca_id_dict = _generating_cert_details(ca_profile, extracted_cert)
                    handle.log(level="INFO", message="--CA profile %s details:--\n"%kwargs['ca_profile'])
                    return ca_id_dict

        else:
            ca_cert_list = []
            ca_id_list = []
            ca_dict = dict(ca_dict)
            #=======================================================================
            #     For device in cluster mode and ca-profile not given in kwargs
            #=======================================================================
            if 'multi-routing-engine-results' in ca_dict['rpc-reply']:
                extracted_dict = ca_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['x509-pki-certificate-info-list']['pkid-x509-certificate-information']
                if 'list' in str(type(extracted_dict)):
                    ca_cert_list = extracted_dict
                else:
                    ca_cert_list.append(extracted_dict)
                for item in ca_cert_list:
                    item = dict(item)
                    ca_identifier = item['identifier']
                    ca_id_list.append(_generating_cert_details(ca_identifier, item))

                handle.log(level="INFO", message="--CA profile details:--\n")
                return ca_id_list

            #=======================================================================
            #     For device in non-cluster mode ca-profile not given in kwargs
            #=======================================================================
            else:
                extracted_dict = (ca_dict['rpc-reply']['x509-pki-certificate-info-list']['pkid-x509-certificate-information'])
                if 'list' in str(type(extracted_dict)):
                    ca_cert_list = extracted_dict
                else:
                    ca_cert_list.append(extracted_dict)

                for item in ca_cert_list:
                    item = dict(item)
                    ca_identifier = item['identifier']
                    ca_id_list.append(_generating_cert_details(ca_identifier, item))

                handle.log(level="INFO", message="--CA profile details:--\n")
                return ca_id_list
    except Exception as err:
        raise Exception(err)

def generate_key_pair(handle, **kwargs):
    """
       Generates Key Pair
       Arguments:
               handle: **REQUIRED** Router handle
               certificate_id: **REQUIRED** Name of the certificate for which the key pair is generated.
               size: **OPTIONAL** Default is 1024
               type: **OPTIONAL** Default is RSA
               timeout: ***OPTIONAL*** Timeout (in sec) while generating key pair. Default value is 120s
               err_level: ***OPTIONAL*** Log Level while displaying log messages. Values can be INFO/ERROR. Default is ERROR.
       Returns:
               Returns True if generated successfully else False
    """

    size = kwargs.get('size', 1024)
    size = str(size)
    encr_type = kwargs.get('type', 'rsa')
    timeout = kwargs.get('timeout', 120)
    certificate_id = kwargs.get('certificate_id')
    err_level = kwargs.get('err_level', 'ERROR')

    handle.log(level="INFO", message="--Generating key-pair %s--\n"%certificate_id)

    cmd = 'request security pki generate-key-pair certificate-id '+certificate_id+' size '+size+' type '+str(encr_type)
    result = handle.cli(command=cmd, timeout=timeout, format="text")

    result = result.response()
    if re.search('.*Generated.*', str(result), re.IGNORECASE):
        handle.log(level="INFO", message="--Generated key pair for %s successfully--\n" %certificate_id)
        return True
    else:
        handle.log(level=err_level, message="--Failed to generate key pair %s--\n" %certificate_id)
        handle.log(level=err_level, message="--Failed to generate key-pair for %s--\n"%certificate_id)
        return False

def enroll_local_cert(handle, **kwargs):
    """
        Generates key-pair and Enrolls local certificate

        :param handle:
            **REQUIRED** Router handle

        :param certificate_id:
            **REQUIRED** Name of the certificate

        :param ca_profile:
            **REQUIRED** Name of the CA Profile

       :param domain_name:
           **OPTIONAL** Default is juniper.net

       :param digest:
           **OPTIONAL** Values can be sha-1 and sha-256. Default is sha-1

       :param subject:
           **OPTIONAL** Default is DC=juniper,CN=local,OU=marketing,O=juniper,L=sunnyvale,ST=california,C=us

       :param challenge_password:
           **OPTIONAL** Default is abc

       :param email:
           **OPTIONAL** default is test@juniper.net

       :param filename:
           **OPTIONAL** file from where the certificate needs to be loaded from
           
        :param key_file:
           **OPTIONAL** Private key file to load local certificate 
           
       :param ip_address:
           **OPTIONAL**

       :param ipv6_address:
           **OPTIONAL**

        :param size:
          **OPTIONAL**  public private key-size(1024/2048/4096 for rsa and dsa, 256,384 for ecdsa), default is 2048

        :param type
            **OPTIONAL**  type of key (rsa/dsa/ecdsa), default is rsa

        :param timeout
            **OPTIONAL**  timeout in seconds. default is 300s

        :param max_retries
            ***OPTIONAL*** maximum number of times enrollment of certificate is tried before it successfull; default is 5

        :param wait_time
            ***OPTIONAL*** amount of time to wait before enrollment of certificate is tried again; default is 5 seconds

        :param err_level
            ***OPTIONAL*** Log Level while displaying log messages. Values can be INFO/ERROR. Default is ERROR.

        : param gen_key_pair
            ***OPTINAL*** generates key pair automatically if set to True. 

       :return

           Returns True if enrolled successfully else False

       EXAMPLE::

            PYTHON:
               enroll_local_cert(device_handle, certificate_id='mynewcert', ca_profile='Root')

            ROBOT:
               enroll local cert  ${device_handle}  certificate_id=mynewcert  ca_profile=Root

                device>request security pki generate-key-pair certificate-id mynewcert
                Generated key pair mynewcert, key size 2048 bits

                device> request security pki local-certificate enroll certificate-id  mynewcert challenge-password
                        abc domain-name juniper.net email test@juniper.net subject
                        DC=juniper,CN=local,OU=marketing,O=juniper,L=sunnyvale,ST=california,C=us ca-profile Root
    """
    handle.log(level="INFO", message="------------------------------------\n")
    handle.log(level="INFO", message="\tENROLLING LOCAL CERTIFICATE")
    handle.log(level="INFO", message="------------------------------------\n")

    ca_profile = kwargs.get('ca_profile')
    cert_id = kwargs.get('certificate_id')
    filename = kwargs.get('filename')
    key_file = kwargs.get('key_file')
    subject = kwargs.get('subject', 'DC=juniper,CN=local,OU=marketing,O=juniper,L=sunnyvale,ST=california,C=us')
    domain_name = kwargs.get('domain_name', 'juniper.net')
    challenge_password = kwargs.get('challenge_password', 'abc')
    email = kwargs.get('email', 'test@juniper.net')
    ip_address = kwargs.get('ip_address')
    ipv6_address = kwargs.get('ipv6_address')
    size = kwargs.get('size', 2048)
    encr_type = kwargs.get('type', 'rsa')
    timeout = kwargs.get('timeout', 300)
    size = str(size)
    response = False
    max_retries = kwargs.get('max_retries', 5)
    wait_time = kwargs.get('wait_time', 5)
    err_level = kwargs.get('err_level', 'ERROR')
    digest = kwargs.get('digest', 'sha-1')
    gen_key_pair = kwargs.get('gen_key_pair', True)

    handle.log("Enrolling local certificate %s "%cert_id)

    if 'filename' in kwargs:
        cmd = 'request security pki local-certificate load certificate-id '+cert_id+' filename '+filename+' key '+key_file
    elif 'ca_profile' in kwargs and 'certificate_id' in kwargs:
        cmd = 'request security pki local-certificate enroll certificate-id  '+cert_id+' challenge-password '+challenge_password+' domain-name '+domain_name+' email '+email+' subject '+subject+' ca-profile '+ca_profile
        if 'ip_address' in kwargs:
            cmd += ' ip-address '+ip_address
        if 'ipv6_address' in kwargs:
            cmd += ' ipv6-address '+ipv6_address
        if 'digest' in kwargs:
            cmd += ' digest '+digest
    else:
        raise KeyError("Missing mandatory arguments")

    # generate key-pair
    if gen_key_pair:
        generate_key_pair(handle, certificate_id=cert_id, size=size, type=encr_type, timeout=timeout)

    result = handle.cli(command=cmd, timeout=timeout, format="text").response()
    if re.search('.*already exists.*', str(result)):
        handle.log(level=err_level,
                   message="--Local certificate %s already exists. Please clear local-certs before trying to enroll again--" % cert_id)
        response = False
    elif re.search(".*Keypair doesn't exist for certificate.*", str(result)):
        handle.log(level=err_level,
                   message="--eypair doesn't exist for certificate %s--" % cert_id)
        response = False
    elif re.search(".*missing argument.*", str(result)):
        handle.log(level=err_level,
                   message="--Missing argument. Please check and try again--")
        response = False
    else:
        loop_cnt = 1
        cmd_str = "show security pki local-certificate certificate-id "+cert_id
        while loop_cnt <= max_retries:
            time.sleep(wait_time)
            cert_id_resp = handle.cli(command=cmd_str).response()
            if cert_id in str(cert_id_resp):
                handle.log(level="INFO", message="--Certificate found, Enrolled local certificate %s successfully--" % cert_id)
                response = True
                break
            else:
                handle.log(level="INFO", message="Certificate not found, retrying...")
                loop_cnt += 1
                if loop_cnt > max_retries:
                    handle.log(level=err_level, message="--Failed to enroll Local certificate %s--"%cert_id)
                    response = False
    return response

def verify_local_cert(handle, **kwargs):
    """
           Verifies Local Certificate

           :param handle:
               **REQUIRED** Router handle

           :param certificate_id:
               **Required** Name of the certificate

           :param wait_time:
               **OPTIONAL** Default value is 30

           :param max_retries:
               **OPTIONAL** Default value is 2

           :param timeout:
               **OPTIONAL** Default value is 120

           :param err_val:
               **OPTIONAL** Error value. Default value is E

           :param expect_string:
               **OPTIONAL** Default value is 'OCSP certificate validation successful'

            :param err_level
                ***OPTIONAL*** Log Level while displaying log messages. Values can be INFO/ERROR. Default is ERROR.

           :return
               Returns true if verified successfully else raises Error

           EXAMPLE::

                PYTHON:
                    verify_local_cert(device_handle, certificate_id='mynewcert')

                ROBOT:
                    verify local cert  ${device_handle}  certificate_id='mynewcert'

                device> request security pki local-certificate verify certificate-id mynewcert

                Local certificate mynewcert verification success
    """
    handle.log(level="INFO", message="------------------------------------\n")
    handle.log(level="INFO", message="\tVERIFYING LOCAL CERTIFICATE")
    handle.log(level="INFO", message="------------------------------------\n")
    certificate_id = kwargs.get('certificate_id')
    wait_time = kwargs.get('wait_time', 5)
    max_retries = kwargs.get('max_retries', 2)
    expect_string = kwargs.get('expect_string', 'OCSP certificate validation successful')
    timeout = kwargs.get('timeout', 120)
    err_level = kwargs.get('err_level', 'ERROR')

    response = False

    handle.cli(command='clear log pkid', format='text')
    handle.cli(command='clear log messages', format='text')

    while max_retries > 0:
        cmd = 'request security pki local-certificate verify certificate-id  '+certificate_id
        handle.log(level="INFO", message="Verifying local certificate %s..." % certificate_id)
        result = handle.cli(command=cmd, timeout=timeout, format='text').response()

        if re.search('.*success.*', str(result), re.IGNORECASE):
            handle.log(level="INFO",
                       message="--Verified local certificate %s successfully--\n" % certificate_id)
            response = True
            break
        elif re.search('.*Revocation check is in progress.*', str(result), re.IGNORECASE):
            handle.log(level="INFO", message="Checking PKID logs for completion status")
            out = _verify_ocsp_cert(handle, expect_string, certificate_id=certificate_id)
            if out:
                response = out
                break
        elif re.search('.*not found in local database.*', str(result), re.IGNORECASE):
            handle.log(level=err_level,
                       message="--Could not find local certificate %s in local database--\n" % certificate_id)
            response = False
        elif re.search('.*is not valid yet.*', str(result), re.IGNORECASE):
            handle.log(level=err_level,
                       message="--Local Certificate %s is not valid yet. Please check the validity of the certificate on the device--\n" % certificate_id)
            response = False
        elif re.search(".*doesn't exist.*", str(result)):
            handle.log(level=err_level, message="--Local certificate %s does not exist--\n" % certificate_id)
            response = False
        elif re.search(".*CRL download failed for certficate.*", str(result)):
            handle.log(level=err_level, message="--Local certificate %s verification failed because CRL download failed--\n" % certificate_id)
            response = False
        max_retries -= 1
        handle.log(level="INFO", message="--Sleeping for %s seconds--\n"%str(wait_time))
        time.sleep(wait_time)

    return response

def get_local_cert(handle, **kwargs):
    """
       Shows Local certificate details

        :param handle:
            **REQUIRED** Router handle

        :param certificate_id:
            **Required** Name of the certificate

        :param detail:
            **OPTIONAL** Default value is terse i.e. 0. To enable detailed certificate assign 1

        :return
            Returns dictionary with each parameter of the certificate

        EXAMPLE::
            PYTHON:
                get_local_cert(device_handle, certificate_id='mynewcert', detail=1)

            ROBOT:
                get local cert  ${device_handle}  certificate_id='mynewcert'  detail=1

            device> show security pki local-certificate certificate-id mynewcert detail

                Certificate identifier: mynewcert
                  Certificate version: 3
                  Serial number: 00043da0
                  Issuer:
                    Organization: juniper, Country: us, Common name: Root
                  Subject:
                    Organization: juniper, Organizational unit: marketing, State: california, Locality: sunnyvale, Common name: local, Domain component: juniper
                  Subject string:
                    DC=juniper, CN=local, OU=marketing, O=juniper, L=sunnyvale, ST=california, C=us
                  Alternate subject: "test@juniper.net", juniper.net, ipv4 empty, ipv6 empty
                  Validity:
                    Not before: 04-21-2017 19:22 UTC
                    Not after: 04- 3-2018 09:13 UTC
                  Public key algorithm: rsaEncryption(1024 bits)
                    30:81:89:02:81:81:00:b4:af:4d:d4:52:aa:89:16:98:ee:98:b3:e9
                    da:e3:6f:ef:09:c0:85:00:90:8f:78:48:da:5d:46:47:3c:28:3e:d0
                    c1:f7:e5:65:5f:b5:a4:97:f1:16:83:59:94:7d:ee:16:d7:00:14:8a
                    46:fe:86:d2:da:49:41:15:71:14:b7:6c:bd:8f:11:32:f7:2d:7f:fa
                    05:51:6d:c5:2e:88:d3:1a:22:67:fc:d9:08:51:fa:90:65:dd:24:e6
                    0b:74:47:7b:30:9b:0d:ab:c7:40:92:ae:d8:70:a3:d7:a9:61:9f:50
                    d9:35:f8:d6:6c:ed:a5:c3:7e:c2:37:ec:00:49:39:02:03:01:00:01
                  Signature algorithm: sha256WithRSAEncryption
                  Distribution CRL:
                    http://10.204.128.120:8080/crl-as-der/currentcrl-292.crl?id=292
                  Authority Information Access OCSP:
                    http://10.204.128.120:8090/Root/
                  Fingerprint:
                    a2:95:2f:e5:db:7b:45:42:70:3a:61:1b:5d:aa:63:3f:73:b5:3d:5d (sha1)
                    84:0e:ab:53:dc:aa:e1:4a:1a:6e:4e:ab:bc:87:af:4d (md5)
                  Auto-re-enrollment:
                    Status: Disabled
                    Next trigger time: Timer not started

                =================================================================================

                Returned Dictionary:

                    {'mynewcert': {'validity-not-after': '04- 3-2018 09:13 UTC', 'subject-email': '"test@juniper.net"',
                    'validity-not-before': '04-21-2017 19:22 UTC', 'recipient': '', 'signature-algorithm': 'sha256WithRSAEncryption',
                    'serial-number': '00043da0', 'issued-by': '', 'subject-domain': 'juniper.net', 'public-key-algorithm': 'rsaEncryption',
                    'public-key-length': '1024'}}

    """
    handle = handle
    handle.log(level="INFO", message="-------------------------------------------\n")
    handle.log(level="INFO", message="\tDISPLAYING LOCAL CERTIFICATE DETAILS")
    handle.log(level="INFO", message="-------------------------------------------\n")

    if 'certificate_id' in kwargs:
        certificate_id = kwargs['certificate_id']
        cmd = 'show security pki local-certificate certificate-id '+kwargs['certificate_id']
    else:
        cmd = 'show security pki local-certificate'

    if 'detail' in kwargs:
        if kwargs['detail'] == 1:
            cmd = cmd+' detail'

    local_xml = handle.cli(command=cmd, format='xml').response()
    local_dict = jxmlease.parse(local_xml)

    try:
        if 'certificate_id' in kwargs:
            #=======================================================================
            #   For device in cluster mode and certificate id is given
            #=======================================================================
            if 'multi-routing-engine-results' in local_dict['rpc-reply']:
                if str(local_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['x509-pki-certificate-info-list']) != '':
                    extracted_cert = (local_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['x509-pki-certificate-info-list']['pkid-x509-certificate-information'])
                    extracted_cert = dict(extracted_cert)
                    local_id_dict = _generating_cert_details(certificate_id, extracted_cert)
                    handle.log(level="INFO", message="--Local Certificate %s details:--\n"%kwargs['certificate_id'])
                    return local_id_dict

            #=======================================================================
            #   For device in non-cluster mode and certificate id is given
            #=======================================================================
            else:
                if str(local_dict['rpc-reply']['x509-pki-certificate-info-list']) != '':
                    extracted_cert = (local_dict['rpc-reply']['x509-pki-certificate-info-list']['pkid-x509-certificate-information'])
                    extracted_cert = dict(extracted_cert)
                    local_id_dict = _generating_cert_details(certificate_id, extracted_cert)
                    handle.log(level="INFO", message="--Local Certificate %s details:--\n"%kwargs['certificate_id'])
                    return local_id_dict

        else:
            local_cert_list = []
            local_id_list = []
            local_dict = dict(local_dict)
            extracted_dict = {}
            #=======================================================================
            #     For device in cluster mode and certificate id not given in kwargs
            #=======================================================================
            if 'multi-routing-engine-results' in local_dict['rpc-reply']:
                local_dict = dict(local_dict)
                extracted_dict = dict(extracted_dict)
                extracted_dict = local_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['x509-pki-certificate-info-list']['pkid-x509-certificate-information']
                if 'list' in str(type(extracted_dict)):
                    local_cert_list = extracted_dict
                else:
                    local_cert_list.append(extracted_dict)
                for item in local_cert_list:
                    item = dict(item)
                    local_identifier = item['identifier']
                    local_id_list.append(_generating_cert_details(local_identifier, item))

                handle.log(level="INFO", message="--Local Certificate  details:--\n")
                return local_id_list
            #=======================================================================
            #     For device in non-cluster mode certificate id not given in kwargs
            #=======================================================================
            else:
                extracted_dict = (local_dict['rpc-reply']['x509-pki-certificate-info-list']['pkid-x509-certificate-information'])
                if 'list' in str(type(extracted_dict)):
                    local_cert_list = extracted_dict
                else:
                    local_cert_list.append(extracted_dict)
                for item in local_cert_list:
                    item = dict(item)
                    local_identifier = item['identifier']
                    local_id_list.append(_generating_cert_details(local_identifier, item))

                handle.log(level="INFO", message="--Local Certificate details:--\n")
                return local_id_list
    except Exception as err:
        raise Exception(err)

def enroll_cmpv2_cert(handle, **kwargs):
    """
    Enrolls CMPv2 certificate

    :param ca_profile
        **REQUIRED** CA profile

    :param certificate_id
        **REQUIRED** Certificate ID

    :param ca_secret
        **REQUIRED** CA secret
    
    :param ca_reference
        **REQUIRED** CA Reference

    :param ca_dn
        **OPTIONAL** CA domanin name

    : param domain_name
        ***OPTIONAL*** Fully qualified domain name for subject-alt-name

    :param size
        **OPTIONAL**  public private key-size(1024/2048/4096 for rsa and dsa, 256,384 for ecdsa), default is 2048

    :param type
        **OPTIONAL**  type of key (rsa/dsa/ecdsa), default is rsa

    :param ip_address
        **OPTIONAL** IP address of device

    :param ipv6_address
        **OPTIONAL** IPv6 address of device

    :param email
        **OPTIONAL** Email address

    :param timeout
        **OPTIONAL** Timeout in seconds. Default value is 300s

    :param max_retries
        **OPTIONAL*** The max number of times, the script tries to looking for successful enrollment of cmpv2 certificate. Default value is 5

    :param wait_time
        ***OPTIONAL*** Time (in seconds) to wait, before enrollment of certificat is attempted again. Default is 5s

    :param err_level
                ***OPTIONAL*** Log Level while displaying log messages. Values can be INFO/ERROR. Default is ERROR.

    *** Either ip_address or email is required ***

    EXAMPLE::

        PYTHON:
            enroll_cmpv2_cert(dev_obj, ca_profile='root-ecdsa-ca-256-sha256', ca_secret='emergency_fix_psk', ca_reference='51899', size='256', certificate_id='myecdsa256', email='test@juniper.net')

        ROBOT:
            enroll cmpv2 cert   ${dev_obj}  ca_profile=root-ecdsa-ca-256-sha256  ca_secret=emergency_fix_psk  ca_reference=51899  size=256  certificate_id=myecdsa256  email=test@juniper.net

        request security pki local-certificate enroll cmpv2 ca-profile root-ecdsa-ca-256-sha256 ca-dn DC=Juniper,
        CN=root-ecdsa-ca-256-sha256 ca-secret emergency_fix_psk ca-reference 51899 certificate-id myecdsa256 email
        vpnqa-seige01@juniper.net ip-address 23.1.1.3 subject CN=vpnqa-seige01,OU=SBU,O=Juniper

    """
    handle.log(level="INFO", message="------------------------------------\n")
    handle.log(level="INFO", message="\tENROLLING CMPv2 CERTIFICATE")
    handle.log(level="INFO", message="-------------------------------------\n")

    ca_profile = kwargs.get('ca_profile')
    cert_id = kwargs.get('certificate_id')
    ca_secret = kwargs.get('ca_secret')
    ca_dn = kwargs.get('ca_dn', 'DC=juniper,C=US')
    ca_reference = str(kwargs.get('ca_reference'))
    domain_name = kwargs.get('domain_name', '%s_domain.com'%ca_profile)
    subject = kwargs.get('subject', 'DC=juniper,CN=local,OU=marketing,O=juniper,L=sunnyvale,ST=california,C=us')
    email = kwargs.get('email', 'test@juniper.net')
    ip_address = kwargs.get('ip_address')
    ipv6_address = kwargs.get('ipv6_address')
    size = kwargs.get('size', 2048)
    encr_type = kwargs.get('type', 'rsa')
    timeout = kwargs.get('timeout', 300)
    max_retries = kwargs.get('max_retries', 5)
    wait_time = kwargs.get('wait_time', 5)
    err_level = kwargs.get('err_level', 'ERROR')
    response = False

    handle.log("Enrolling ca/local certificate using cmpv2")

    if 'ca_profile' in kwargs and 'certificate_id' and 'ca_secret' and 'ca_reference' in kwargs:
        cmd = 'request security pki local-certificate enroll cmpv2  ca-profile '+ ca_profile+' ca-dn '+ca_dn  +' ca-secret '+ ca_secret+' ca-reference '+ ca_reference+' certificate-id '+ cert_id+' subject '+subject+ ' domain-name '+domain_name
        if 'ip_address' in kwargs:
            cmd += ' ip-address '+ip_address
        if 'ipv6_address' in kwargs:
            cmd += ' ipv6-address '+ipv6_address
        if 'email' in kwargs:
            cmd += ' email '+email
    else:
        raise KeyError("Missing Mandatory Arguments")

    # generate key-pair
    generate_key_pair(handle, certificate_id=cert_id, size=size, type=encr_type, timeout=timeout)

    # enroll cert using cmpv2 cli
    result = handle.cli(command=cmd, format="text").response()
    if re.search('.*already exists.*', str(result)):
        handle.log(level=err_level,
                   message="Local certificate %s already exists. Please clear local-certs before trying to enroll again" % cert_id)
        response = False
    elif re.search(".*Keypair doesn't exist.*", str(result)):
        handle.log(level=err_level, message="---Keypair doesn't exist for certificate-id %s. Please generate key-pair first.--"%cert_id)
        response = False
    else:
        loop_cnt = 1
        cmd_str = "show security pki local-certificate certificate-id "+cert_id
        while loop_cnt <= max_retries:
            time.sleep(wait_time)
            cert_id_resp = handle.cli(command=cmd_str).response()
            if cert_id in str(cert_id_resp):
                handle.log(level="INFO", message="--Certificate found, Enrolled local certificate %s successfully--" % cert_id)
                response = True
                break
            else:
                handle.log(level="INFO", message="Certificate not found, retrying...")
                loop_cnt += 1
                if loop_cnt > max_retries:
                    handle.log(level=err_level, message="--Failed to enroll Local certificate %s--"%cert_id)
                    response = False
    return response

def clear_pki(handle, **kwargs):
    """
    Clears certificates & key-pairs

    :param ca_profile
        **OPTIONAL** Possible values:
                            all: Clear all CA certificates
                            ca-profile: Clear given ca-profile certificate
    :param certificate_id
        **OPTIONAL** Possible values:
                            all: Clear all local certificates
                            certificate_id: Clear certificate for given certificate_id
    :param ca_certificate
        **OPTIONAL** Possible values:
                            1: Clear ca_profile (ca_profile is given as next parameter or not given to clear all ca_certificates)
                   
    :param local_certificate
        **OPTIONAL** Possible values:
                            1: Clear certificate_id (certificate_id given as next parameter or not given to clear all local-certificates)

    :param certificate_request
        **OPTIONAL** Possible values:
                            1: Clear certificate_id (certificate_id given as next parameter or not given to clear all certificate_requests)
    :param key_pair
        **OPTIONAL** Possible values:
                             1: Clear certificate_id (certificate_id given as next parameter or not given to clear all key-pairs)

    :param crl
            **OPTIONAL** Possible values:
                             1: Clear ca_profile crl (clears all crl for given ca_profile or all crls if ca_profile is not given)
    :return
        True if successful else False

    EXAMPLE::

        PYTHON:

            clear_pki(device_handle, ca_certificate=1, ca_profile='Root')

            clear_pki(device_handle, crl=1, ca_profile='Root')

            clear_pki(device_handle, ca_certificate=1, crl=1, ca_profile='Root')

            clear_pki(device_handle, key_pair=1, certificate_id='mynewcert')

            clear_pki(device_handle, local_certificate=1, certificate_id='mynewcert')

            clear_pki(device_handle, local_certificate=1, key_pair=1, certificate_id='mynewcert')

        ROBOT:

            clear pki  ${device_handle}  ca_certificate=1  ca_profile=Root

            clear pki  ${device_handle}  crl=1  ca_profile=Root

            clear pki  ${device_handle}  ca_certificate=1  crl=1  ca_profile=Root

            clear pki  ${device_handle}  key_pair=1  certificate_id=mynewcert

            clear pki  ${device_handle}  local_certificate=1  certificate_id=mynewcert

            clear pki  ${device_handle}  local_certificate=1 key_pair=1  certificate_id=mynewcert

    """
    handle = handle
    handle.log(level="INFO", message="-----------------------\n")
    handle.log(level="INFO", message="\tCLEARING PKI")
    handle.log(level="INFO", message="-----------------------\n")

    clear_cmd = 'clear security pki '

    kwargs.get('ca_certificate')
    kwargs.get('local_certificate')
    kwargs.get('certificate_request')
    kwargs.get('key_pair')
    kwargs.get('crl')
    ca_profile = kwargs.get('ca_profile')
    certificate_id = kwargs.get('certificate_id')
    response = False

    if 'ca_certificate' in kwargs and ca_profile != None:
        cmd = clear_cmd+' ca-certificate ca-profile '+ca_profile
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared ca-profile %s--\n"%ca_profile)
        response = True
    elif 'ca_certificate' in kwargs and 'ca_profile' not in kwargs:
        cmd = clear_cmd+' ca-certificate ca-profile all '
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared ca-certificates for all ca-profiles--\n")
        response = True

    if 'certificate_request' in kwargs and certificate_id != None:
        cmd = clear_cmd+'certificate-request certificate-id '+certificate_id
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared certificate request for certificate-id %s--\n"%certificate_id)
        response = True
    elif 'certificate_request' in kwargs and 'certificate_id' not in kwargs:
        cmd = clear_cmd+'certificate-request certificate-id all'
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all certificate requests --\n")
        response = True

    if 'local_certificate' in kwargs and certificate_id != None:
        cmd = clear_cmd+' local-certificate certificate-id '+certificate_id
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared local-certificate certificate-id %s--\n"%certificate_id)
        response = True
    elif 'local_certificate' in kwargs and 'certificate_id' not in kwargs:
        cmd = clear_cmd+' local-certificate certificate-id all'
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all local-certificates--\n")
        response = True

    if 'key_pair' in kwargs and certificate_id != None:
        cmd = clear_cmd+' key-pair certificate-id '+certificate_id
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared key-pair certificate-id %s--\n"%certificate_id)
        response = True
    elif 'key_pair' in kwargs and 'certificate_id' not in kwargs:
        cmd = clear_cmd+' key-pair certificate-id all '
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all key-pairs--\n")
        response = True

    if 'crl' in kwargs and ca_profile != None:
        cmd = clear_cmd+' crl ca-profile '+ca_profile
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared CRL for ca-profile %s--\n"%ca_profile)
        response = True
    elif 'crl' in kwargs and 'ca_profile' not in kwargs:
        cmd = clear_cmd+' crl all'
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all CRLs--\n")
        response = True

    if 'ca_certificate' not in kwargs and 'certificate_request' not in kwargs and 'local_certificate' not in kwargs and 'key_pair' not in kwargs and 'crl' not in kwargs:
        cmd = (clear_cmd+ ' ca-certificate all')
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all ca-certificates--\n")

        cmd = (clear_cmd+ ' local-certificate all')
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all local certificates--\n")

        cmd = (clear_cmd+ ' certificate-request all')
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all certificate requests--\n")

        cmd = (clear_cmd+ ' key-pair all')
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all key-pairs--\n")

        cmd = (clear_cmd+ ' crl all')
        handle.cli(command=cmd)
        handle.log(level="INFO", message="--Cleared all CRLs--\n")
        response = True

    return response

def clear_pki_all(device_handle, **kwargs):
    """clear pki certs and logs
    :param device_handle:
        **REQUIRED** device object lists
    :param ca:
        **OPTIONAL** default clear all ca certs
    :param local:
        **OPTIONAL** default clear all local certs
    :param keys:
        **OPTIONAL** default clear all key-pairs
    :param crl:
        **OPTIONAL** default clear all crls
    :param cert_request:
        **OPTIONAL** default clear all cerificate requests

    :return: True upon executing all cli commands
    Example P: clear_pki_all(R0)
            R: Clear Pki  All    R0
    """

    ca_cert = kwargs.get('ca', True)
    local = kwargs.get('local', True)
    keys = kwargs.get('keys', True)
    crl = kwargs.get('crl', True)
    cert_request = kwargs.get('cert_request', True)
    logs = kwargs.get('logs', True)
    device_handle.log(message="clear pki logs and information")
    if ca_cert:
        device_handle.cli(command='clear security pki ca-certificate all')
    if local:
        device_handle.cli(command='clear security pki local-certificate all')
    if crl:
        device_handle.cli(command='clear security pki crl all')
    if cert_request:
        device_handle.cli(command='clear security pki certificate-request all')
    if keys:
        device_handle.cli(command='clear security pki key-pair all')
    if logs:
        device_handle.cli(command='clear log pkid')

    return True
#=====================================
#    Private Methods
#=====================================

def _check_chassis_cluster(handle):
    """
        This is a private method used by the library to check if the device is in HA/non-HA mode
        It returns 1 if the device is in HA and 0 if the device is in non-HA
    """
    out = handle.cli(command="show chassis cluster status").response()
    #Check for Mx devices
    model = handle.cli(command="show version |grep model").response()
    if re.search("Chassis cluster is not enabled", str(out)):
        check_chassis = 0
    elif re.search("mx", str(model), re.IGNORECASE):
        check_chassis = 0
    else:
        check_chassis = 1
    return check_chassis

def _verify_ocsp_cert(handle, expect_string, **kwargs):
    certificate_id = kwargs.get('certificate_id')
    ca_profile = kwargs.get('ca_profile')
    verified_ok = "cert verified ok:"
    err_level = kwargs.get('err_level', 'INFO')
    if 'certificate_id' in kwargs:
        handle.log(level="INFO", message="----Getting serial number of Local certificate----\n")
        local_cert_dict = get_local_cert(handle, certificate_id=certificate_id, detail=1)
        serial_num = local_cert_dict[certificate_id]['serial-number']
        cert = certificate_id
    if 'ca_profile' in kwargs:
        handle.log(level="INFO", message="----Getting serial number of CA certificate----\n")
        ca_cert_dict = get_ca_cert(handle, ca_profile=ca_profile, detail=1)
        serial_num = ca_cert_dict[ca_profile]['serial-number']
        cert = ca_profile

    result = _get_match_from_log(handle, expect_string)

    if expect_string in result:
        if re.search("certificate revoked", result):
            handle.log(level=err_level, message="--Certificate %s has been revoked--\n" % cert)
            raise Exception("Certificate %s has been revoked"%cert)
        elif re.search(serial_num, result):
            handle.log(level="INFO", message="--Certificate %s validation successful--\n" % cert)
            return True
    else:
        handle.log("Verification information not found in pkid logs about this cert")
        return False
    result = _get_match_from_log(handle, verified_ok)
    if re.search(verified_ok, result):
        handle.log(level="INFO", message="--Certificate %s validation successful--\n" % cert)
        return True
    else:
        handle.log(level=err_level, message="Expected string not found in pkid log")
        raise Exception("Expected string not found in pkid log")

def _get_match_from_log(handle, expect_string):
    """
    This is a private method used by the library to find an expected string in pkid logs
    It returns the matched string
    """
    expect_str = '"'+expect_string+'"'
    matched_str = handle.cli(command="show log pkid |grep %s"%expect_str).response()
    return matched_str

def _generating_cert_details(cert_profile, extracted_cert):
    """
        This is a private method used by the library to create a dicitionary from xml input,
        which contans results for cli output for pki show commands
        It returns a dictionary with key-values contatining details about CA/Local certificate
    """
    cert_identifier = str(extracted_cert['identifier'])
    cert_id_dict = {}
    cert_details_dict = {}
    cert_id_dict[cert_identifier] = cert_details_dict

    if 'public-key' in extracted_cert.keys():
        cert_pub_key_algo = str(extracted_cert['public-key']['public-key-algorithm'])
        cert_pub_key_len = str(extracted_cert['public-key']['public-key-length'])
        cert_details_dict['public-key-algorithm'] = cert_pub_key_algo
        cert_details_dict['public-key-length'] = cert_pub_key_len
    else:
        cert_details_dict['public-key-algorithm'] = ''
        cert_details_dict['public-key-length'] = ''

    if 'serial-number-list' in extracted_cert.keys():
        cert_ser_num = str(extracted_cert['serial-number-list']['serial-number-x509'])
        cert_details_dict['serial-number'] = cert_ser_num
    else:
        cert_details_dict['serial-number'] = ''

    if 'validity' in extracted_cert.keys():
        cert_val_start = str(extracted_cert['validity']['not-before'])
        cert_val_end = str(extracted_cert['validity']['not-after'])
        cert_details_dict['validity-not-before'] = cert_val_start
        cert_details_dict['validity-not-after'] = cert_val_end
    else:
        cert_details_dict['validity-not-before'] = ''
        cert_details_dict['validity-not-after'] = ''

    if 'signature-algorithm' in extracted_cert.keys():
        cert_sign_algo = str(extracted_cert['signature-algorithm'])
        cert_details_dict['signature-algorithm'] = cert_sign_algo
    else:
        cert_details_dict['signature-algorithm'] = ''

    if 'issue-info' in extracted_cert.keys():
        cert_recipient = str(extracted_cert['issue-info']['recipient'])
        cert_issued_by = str(extracted_cert['issue-info']['issued-by'])
        cert_details_dict['recipient'] = cert_recipient
        cert_details_dict['issued-by'] = cert_issued_by
    else:
        cert_details_dict['recipient'] = ''
        cert_details_dict['issued-by'] = ''

    if 'alternate-subject-list' in extracted_cert.keys():
        #subject domain
        domain_list = list(extracted_cert['alternate-subject-list']['alternate-subject'])
        tld_list = ['.gov', '.net', '.edu', '.com', '.in', '.uk', '.org']
        for i in tld_list:
            for j in domain_list:
                if i in j:
                    cert_details_dict['subject-domain'] = str(j)

        for element in extracted_cert['alternate-subject-list']['alternate-subject']:
            #subject email
            if '@' in element:
                cert_details_dict['subject-email'] = str(element)
            #subject ipv4 address
            elif re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", element):
                cert_details_dict['subject-ipv4-addr'] = str(element)
                #subject ipv6 address
            elif ':' in  str(extracted_cert['alternate-subject-list']['alternate-subject']):
                cert_details_dict['subject-ipv6-addr'] = str(element)


    cert_dict = {}
    cert_dict[str(cert_profile)] = cert_details_dict
    return cert_dict

#========================================
#    Wrapper Functions
#========================================

def create_pki_object(device_handle):
    """
        Creates pki object, used to access pki keywords

        :param device_handle:
            **REQUIRED** device handle

        :param user:
            **OPTIONAL** login username

        :param password:
            **OPTIONAL** login password

        EXAMPLE::
             ${pki_obj} =  Create Pki Object  ${dh0}
    """

    return Pki(device_handle)

def configure_ca_profile(pki_obj, **kwargs):
    """
            Configures CA Profile on device

            Can be called using wrapper function configure_ca_profile

            :param ca_profile:
                **REQUIRED** Name of CA Profile.

            :param url:
                 **REQUIRED** Enrollment URL

            :param ca_identity:
                **OPTIONAL** Identity name of CA. Default is ca_profile

            :param retry:
                **OPTIONAL** No. of retries. Default is 5

            :param retry_interval:
                **OPTIONAL** Interval between retries. Default is 0

            :param revocation_check:
                **OPTIONAL** can be use-crl, use-ocsp, crl, ocsp, disable

            :param crl_url:
                **OPTIONAL** CRL URL

            :param refresh_interval:
                **OPTIONAL** Tells when to refresh the CRL

            :param ocsp_url:
                **OPTIONAL** OCSP URL

            :param nonce_payload:
                **OPTIONAL**

            :param conection_failure:
                **OPTIONAL** OCSP Connnection failure

            :param routing_instance:
                **OPTIONAL** routing instance

            :param apply_groups:
                **OPTIONAL**

            :param apply_groups_except:
                **OPTIONAL**

            :param administrator:
                **OPTIONAL**

            :param traceoptions:
                **OPTIONAL**

            :param flag:
                **OPTIONAL** traceoption flag level

            :param file:
                **OPTIONAL** file where logs will be saved

            :returns
                True/ False

            EXAMPLE::

                configure ca profile   ${pki_obj}  ca_profile=ecdsa_256_cert  revocation_check=use-ocsp  traceoptions=1  flag=all  file=pkid
    """
    return pki_obj.set_ca_profile(**kwargs)
