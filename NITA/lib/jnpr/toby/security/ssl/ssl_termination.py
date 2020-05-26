#!/usr/bin/python3
"""
#  DESCRIPTION:  SSL Termination Services configuration APIs flat toby wrapper
#  AUTHOR:  Thyagarajan S Pasupathy (), thyag@juniper.net
"""
from jnpr.toby.security.ssl.sslservices import SslServices


def conf_ssl_term_cert_identifier(device=None, *args, **kwargs):
    """
    SSL Services profile certificate identifier configuration
    Example :-
        conf_ssl_term_cert_identifier(device_handle=device_handle, \
        sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
        conf_ssl_term_cert_identifier(device_handle=device_handle, mode="delete", \
        sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
    Robot example :-
        conf ssl term cert identifier    device_handle=device_handle    sslprofile=sslprofile
        certidentifier=ssl-inspect-ca

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
            ``Default value``   : termination
    :param str certidentifier:
        **REQUIRED** Certificate identifier a mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_cert_identifier(sslplugin="termination", *args, **kwargs)


def conf_ssl_term_custom_cipher(device=None, *args, **kwargs):
    """
    SSL custom cipher suite configurations
    Example :-
        conf_ssl_term_custom_cipher( device=device, sslprofile="sslprofile", \
        ciphersuite="rsa-with-rc4-128-md5 rsa-with-rc4-128-sha rsa-with-des-cbc-sha\
         rsa-export-with-rc4-40-md5")
        conf_ssl_term_custom_cipher(device=device, mode="delete", \
        sslprofile="sslprofile", ciphersuite="rsa-with-rc4-128-md5 rsa-with-rc4-128-sha")
        conf_ssl_term_custom_cipher(device=device, mode="delete" , \
        sslprofile="sslprofile")
    Robot example :-
        config ssl term custom cipher    device=$(device)    sslprofile=sslprofile    \
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
            ``Default value``   : termination
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_custom_cipher(sslplugin="termination", *args, **kwargs)


def conf_ssl_term_preferred_cipher(device=None, *args, **kwargs):
    """
    SSL preferred cipher suite configurations
    Example :-
        conf_ssl_term_preferred_cipher( device=device, sslprofile="sslprofile",
         ciphersuite="strong")
        conf_ssl_term_preferred_cipher(device=device, mode="delete",
         sslprofile="sslprofile")
    Robot example :-
        config ssl term preferred cipher    device=$(device)
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
            ``Default value``   : termination
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """

    return SslServices(device).conf_ssl_preferred_cipher(sslplugin="termination", *args, **kwargs)


def conf_ssl_term_flow_trace(device=None, *args, **kwargs):
    """
    Flow trace configuration in global ssl service level
    Example :-
            conf_ssl_term_flow_trace(device=device, sslprofile ="sslprofile")
            conf_ssl_term_flow_trace(device=device, mode="delete", sslprofile ="sslprofile")
    Robot example :-
            config ssl term flow trace    device=$(device)    sslprofile=sslprofile

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : termination
    :param str sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_flow_trace(sslplugin="termination", *args, **kwargs)


def conf_ssl_term_protocol_version(device=None, *args, **kwargs):
    """
    SSL TLS version configuration
    Example :-
            conf_ssl_term_protocol_version(device=device, sslprofile="sslinit", tls_version="tls11")
            conf_ssl_term_protocol_version(device=device, mode="delete", sslprofile="sslinit",
             tls_version="tls11")
    Robot example :-
            config ssl term  protocol version    device=$(device)    sslprofile=sslinit
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
            ``Default value``   : termination
    :param str sslprofile:
        *REQUIRED* ssl proxy profile name mandatory option to be passed
    :param str tls_version:
        *REQUIRED* TLS version for ssl initiation profile "all", "tls11", "tls12" & "tls1"
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_protocol_version(sslplugin="termination", *args, **kwargs)


def conf_ssl_term_enable_sess_cache(device=None, *args, **kwargs):
    """
    SSL TLS initiation and termination plugin session cache enabling configuration
    Example :-
            conf_ssl_term_enable_sess_cache(device=device, sslprofile="sslinit")
            conf_ssl_term_enable_sess_cache(device=device, mode="delete", sslprofile="sslinit")
    Robot example :-
        conf ssl enable sess cache    device=$(device)    mode="delete"    sslprofile="sslinit"

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *REQUIRED* SSL plugin type selection
            ``Supported values``: initiation or termination
            ``Default value``   : termination
    :param str sslprofile:
        *REQUIRED* ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    """
    return SslServices(device).conf_ssl_enable_sess_cache(sslplugin="termination", *args, **kwargs)


def conf_ssl_termination(device=None, *args, **kwargs):
    """
    Configuring SSL proxy in either client or server protection mode
    Example :-
        conf_ssl_termination(device=device,
                                sslprofile='sslterm',
                                certidentifier='ssl-inspect-ca',
                                enable_flow_trace="TrUe",
                                ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-shA',
                                tls_version='all',
                                enable_session_cache='true'
                                )
        conf_ssl_termination(mode='delete', sslprofile='sslterm')
    Robot example :-
        conf ssl termination    sslprofile='sslterm'    mode='delete'

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
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_termination(*args, **kwargs)
