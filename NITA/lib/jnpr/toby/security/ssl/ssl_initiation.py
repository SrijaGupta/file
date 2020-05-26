#!/usr/bin/python3
"""
#  DESCRIPTION:  SSL initiation Service configuration APIs flat toby wrapper
#  AUTHOR:  Thyagarajan S Pasupathy (), thyag@juniper.net
"""
from jnpr.toby.security.ssl.sslservices import SslServices

def conf_ssl_init_cert_identifier(device=None, *args, **kwargs):
    """
    SSL Services profile certificate identifier configuration
    Example :-
        conf_ssl_init_cert_identifier(device_handle=device_handle, \
        sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
        conf_ssl_init_cert_identifier(device_handle=device_handle, mode="delete", \
        sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
    Robot example :-
        conf ssl init cert identifier    device_handle=device_handle    mode=delete
        sslprofile="sslprofile    certidentifier=ssl-inspect-ca

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str sslplugin:
        **REQUIRED** SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str certidentifier:
        **REQUIRED** Certificate identifier a mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_cert_identifier(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_crl(device=None, *args, **kwargs):
    """
    SSL CRL configuration
    Example :-
        conf_ssl_crl( device=device, sslprofile="sslprofile", \
        crlaction="if-not-present",ifnotpresent="allow")
        conf_ssl_crl( device=device, sslprofile="sslprofile", \
        crlaction="disable")
        conf_ssl_crl( device=device, sslprofile="sslprofile", \
        crlaction="ignore-hold-instruction-code")
        conf_ssl_crl(device=device, mode="delete", sslprofile="sslprofile")
    Robot example :-
        conf ssl init crl    device=$(device)    sslprofile=sslprofile    \
        crlaction=if-not-present    ifnotpresent=allow


    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str crlaction:
        **REQUIRED** crl action configuration options
            ``Supported values``: disable, if-not-present or ignore-hold-instruction-code
    :param str ifnotpresent:
        **REQUIRED** if-not-present action should be parsed when crlaction is "if-not-present"
            ``Supported values``: allow or drop
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_crl(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_custom_cipher(device=None, *args, **kwargs):
    """
    SSL custom cipher suite configurations
    Example :-
        conf_ssl_init_custom_cipher( device=device, sslprofile="sslprofile", \
        ciphersuite="rsa-with-rc4-128-md5 rsa-with-rc4-128-sha rsa-with-des-cbc-sha\
         rsa-export-with-rc4-40-md5")
        conf_ssl_init_custom_cipher(device=device, mode="delete", \
        sslprofile="sslprofile", ciphersuite="rsa-with-rc4-128-md5 rsa-with-rc4-128-sha")
        conf_ssl_init_custom_cipher(device=device, mode="delete" , \
        sslprofile="sslprofile")
    Robot example :-
        conf ssl init custom cipher    device=$(device)    sslprofile=sslprofile    \
        ciphersuite=rsa-with-rc4-128-md5 rsa-with-rc4-128-sha rsa-with-des-cbc-sha\
         rsa-export-with-rc4-40-md5

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str ciphersuite:
        **REQUIRED** custom cipher suite to be configured
            ``Supported values``:   rsa-with-rc4-128-md5            RSA, 128bit rc4, md5 hash
                                    rsa-with-rc4-128-sha            RSA, 128bit rc4, sha hash
                                    rsa-with-des-cbc-sha            RSA, des cbc, sha hash
                                    rsa-with-3des-ede-cbc-sha       RSA, 3des ede/cbc, sha hash
                                    rsa-with-aes-128-cbc-sha        RSA, 128 bit aes/cbc, sha hash
                                    rsa-with-aes-256-cbc-sha        RSA, 256 bit aes/cbc, sha hash
                                    rsa-export-with-rc4-40-md5      RSA-export, 40 bit rc4, md5 hash
                                    rsa-export-with-des40-cbc-sha   RSA-export, 40 bit des/cbc, sha
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_custom_cipher(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_preferred_cipher(device=None, *args, **kwargs):
    """
    SSL preferred cipher suite configurations
    Example :-
        conf_ssl_init_preferred_cipher( device=device, sslprofile="sslprofile",\
         ciphersuite="strong")
        conf_ssl_init_preferred_cipher(device=device, mode="delete",\
         sslprofile="sslprofile")
    Robot example :-
        conf ssl init preferred cipher    device=$(device)    \
        sslprofile="sslprofile"    ciphersuite="strong"


    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str ciphersuite:
        **REQUIRED** custom cipher suite to be configured
            ``Supported values``:   custom     Configure custom cipher suite and order of preference
                                    medium     Use ciphers with key strength of 128-bits or greater
                                    strong     Use ciphers with key strength of 168-bits or greater
                                    weak       Use ciphers with key strength of 40-bits or greater
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_preferred_cipher(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_ignore_serv_auth(device=None, *args, **kwargs):
    """
    SSL server certificate authentification failure ignore configuration
    Example :-
        conf_ssl_init_ignore_serv_auth( device=device, sslprofile="sslprofile")
        conf_ssl_init_ignore_serv_auth(device=device, mode="delete",\
         sslprofile="sslprofile")
    Robot example :-
        conf ssl init ignore server auth    device=$(device)    \
        sslprofile=sslprofile


    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_ignore_serv_auth(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_trusted_ca(device=None, *args, **kwargs):
    """
    Trusted certificate configuration
    Example :-
            conf_ssl_init_trusted_ca(device=device, trusted_ca_list="all", sslprofile ="sslprofile")
            conf_ssl_init_trusted_ca(device=device, mode="delete", trusted_ca_list="all", \
            sslprofile = "sslprofile")
            conf_ssl_init_trusted_ca(device=device, trusted_ca_list="all test1 test2 test3", \
            sslprofile = "sslprofile")
            conf_ssl_init_trusted_ca(device=device, mode="delete", trusted_ca_list="all test1 \
            test2 test3", sslprofile = "sslprofile")
            conf_ssl_init_trusted_ca(device=device, mode="delete", sslprofile = "sslprofile")
    Robot example :-
            conf ssl init trusted ca    device=$(device)    trusted_ca_list=all    \
            sslprofile =sslprofile

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str trusted_ca_list:
        *REQUIRED* Configure trusted CAs
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_trusted_ca(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_flow_trace(device=None, *args, **kwargs):
    """
    Flow trace configuration in global ssl service level
    Example :-
            conf_ssl_init_flow_trace(device=device, sslprofile ="sslprofile")
            conf_ssl_init_flow_trace(device=device, mode="delete", sslprofile ="sslprofile")
    Robot example :-
            conf ssl init flow trace    device=$(device)    sslprofile=sslprofile

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_flow_trace(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_protocol_version(device=None, *args, **kwargs):
    """
    SSL TLS version configuration
    Example :-
            conf_ssl_init_protocol_version(device=device, sslprofile="sslinit", tls_version="tls11")
            conf_ssl_init_protocol_version(device=device, mode="delete", sslprofile="sslinit",\
             tls_version="tls11")
    Robot example :-
            conf ssl init protocol version    device=$(device)    sslprofile=sslinit    \
            tls_version=tls11

    :param str device:
        **REQUIRED** Handle of the device
    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        *REQUIRED* ssl proxy profile name mandatory option to be passed
    :param str tls_version:
        *REQUIRED* TLS version for ssl initiation profile "all", "tls11", "tls12" & "tls1"
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_protocol_version(sslplugin="initiation", *args, **kwargs)


def conf_ssl_init_enable_sess_cache(device=None, *args, **kwargs):
    """
    SSL TLS initiation and termination plugin session cache enabling configuration
    Example :-
            conf_ssl_init_enable_sess_cache(device=device, sslprofile="sslinit")
            conf_ssl_init_enable_sess_cache(device=device, mode="delete", sslprofile="sslinit")
    Robot example :-
        conf ssl init enable sess cache    device=$(device)    mode="delete"    sslprofile="sslinit"

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *REQUIRED* SSL plugin type selection
            ``Supported values``: initiation or termination
            ``Default value``   : initiation
    :param str sslprofile:
        *REQUIRED* ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_enable_sess_cache(*args, **kwargs)


def conf_ssl_init_profile(device=None, *args, **kwargs):
    """
    Configuring SSL proxy in either client or server protection mode
    Example :-
        conf_ssl_init_profile(device=device,
                                sslprofile='sslinit',
                                certidentifier='ssl-inspect-ca',
                                enable_flow_trace="TrUe",
                                trusted_ca_list='all',
                                ignore_server_auth="true",
                                ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                crlaction='if-not-present',
                                ifnotpresent='aLLow',
                                tls_version='all',
                                enable_session_cache='true'
                                )
        conf_ssl_init_profile(mode='delete', sslprofile='sslinit')
    Robot example :-
        conf ssl init profile    sslprofile='sslinit'    mode='delete'

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param sslprofile:
        * REQUIRED * ssl proxy profile name
    :param str certidentifier:
        **REQUIRED** Certificate identifier a mandatory option to be passed
    :param str enable_flow_trace:
        *OPTIONAL* Enable flow trace for the ssl profile
            ``Supported values``: True
    :param str trusted_ca_list:
        *OPTIONAL*  trusted CAs list
    :param str ignore_server_auth:
        *OPTIONAL* Enabling ignore server certificate authentication
            ``Supported values``: True
    :param str ciphersuite:
        *OPTIONAL* cipher suite
            ``Supported values``:
                    Values for preferred cipher suite
                            medium      Use ciphers with key strength of 128-bits or greater
                            strong      Use ciphers with key strength of 168-bits or greater
                            weak        Use ciphers with key strength of 40-bits or greater
                    Values for custom cipher suite
                            rsa-with-rc4-128-md5            RSA, 128bit rc4, md5 hash
                            rsa-with-rc4-128-sha            RSA, 128bit rc4, sha hash
                            rsa-with-des-cbc-sha            RSA, des cbc, sha hash
                            rsa-with-3des-ede-cbc-sha       RSA, 3des ede/cbc, sha hash
                            rsa-with-aes-128-cbc-sha        RSA, 128 bit aes/cbc, sha hash
                            rsa-with-aes-256-cbc-sha        RSA, 256 bit aes/cbc, sha hash
                            rsa-export-with-rc4-40-md5      RSA-export, 40 bit rc4, md5 hash
                            rsa-export-with-des40-cbc-sha   RSA-export, 40 bit des/cbc, sha
    :param str crlaction:
        *OPTIONAL* crl action configuration options
            ``Supported values``: disable, if-not-present or ignore-hold-instruction-code
    :param str ifnotpresent:
        *OPTIONAL* if "if-not-present" action is parsed with crlaction then "if-not-present"
         argument is REQUIRED
            ``Supported values``: allow or drop
    :param str tls_version:
        *OPTIONAL* TLS version for ssl profile
            ``Supported values``: all, tls11, tls12 or tls1
    :param str enable_session_cache:
        *OPTIONAL* enable session cache
            ``Supported values``: true
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_initiation(*args, **kwargs)
