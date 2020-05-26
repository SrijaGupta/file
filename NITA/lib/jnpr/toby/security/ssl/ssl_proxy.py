#!/usr/bin/python3
"""
#  DESCRIPTION:  SSL Services forward and reverse proxy configuration APIs flat toby wrapper
#  AUTHOR:  Thyagarajan S Pasupathy (), thyag@juniper.net
"""
from jnpr.toby.security.ssl.sslservices import SslServices
from jnpr.toby.security.utils import get_vty_counters_as_dictionary


def conf_ssl_proxy_cert_identifier(device=None, *args, **kwargs):
    """
    SSL Services profile certificate identifier configuration
    Example :-
        conf_ssl_proxy_cert_identifier(device_handle=device_handle,
        sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
        conf_ssl_proxy_cert_identifier(device_handle=device_handle, mode="delete",
        sslprofile="sslprofile", certidentifier="ssl-inspect-ca")
    Robot example :-
        conf ssl proxy cert identifier    device=$(device)    sslprofile=sslprofile
        certidentifier="ssl-inspect-ca"

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name
    :param str sslplugin:
        **REQUIRED** ssl plugin type selection
            ``Supported values``: proxy, initiation or termination
    :param str certidentifier:
        **REQUIRED** Certificate identifier a mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_cert_identifier(*args, **kwargs)


def conf_ssl_proxy_crl(device=None, *args, **kwargs):
    """
    SSL CRL configuration
    Example :-
        conf_ssl_proxy_crl( device=device, sslprofile="sslprofile",
        crlaction="if-not-present",ifnotpresent="allow")
        conf_ssl_proxy_crl( device=device, sslprofile="sslprofile",
        crlaction="disable")
        conf_ssl_proxy_crl( device=device, sslprofile="sslprofile",
        crlaction="ignore-hold-instruction-code")
        conf_ssl_proxy_crl(device=device, mode="delete", sslprofile="sslprofile")
    Robot example :-
        conf ssl proxy crl    device=$(device)    sslprofile=sslprofile
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
            ``Default value``   : proxy
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
    :return: Returns "True"
    :rtype: bool
    """

    return SslServices(device).conf_ssl_crl(*args, **kwargs)


def conf_ssl_proxy_custom_cipher(device=None, *args, **kwargs):
    """
    SSL custom cipher suite configurations
    Example :-
        conf_ssl_proxy_custom_cipher( device=device, sslprofile="sslprofile",
        ciphersuite="rsa-with-rc4-128-md5 rsa-with-rc4-128-sha rsa-with-des-cbc-sha
         rsa-export-with-rc4-40-md5")
        conf_ssl_proxy_custom_cipher(device=device, mode="delete",
        sslprofile="sslprofile", ciphersuite="rsa-with-rc4-128-md5 rsa-with-rc4-128-sha")
        conf_ssl_proxy_custom_cipher(device=device, mode="delete" ,
        sslprofile="sslprofile")
    Robot example :-
        conf ssl proxy custom cipher    device=$(device)    sslprofile=sslprofile
        ciphersuite=rsa-with-rc4-128-md5 rsa-with-rc4-128-sha rsa-with-des-cbc-sha
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
            ``Default value``   : proxy
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """

    return SslServices(device).conf_ssl_custom_cipher(*args, **kwargs)


def conf_ssl_proxy_preferred_cipher(device=None, *args, **kwargs):
    """
    SSL preferred cipher suite configurations
    Example :-
        conf_ssl_proxy_preferred_cipher( device=device, sslprofile="sslprofile",
         ciphersuite="strong")
        conf_ssl_proxy_preferred_cipher(device=device, mode="delete",
         sslprofile="sslprofile")
    Robot example :-
        conf ssl proxy preferred cipher    device=$(device)
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
            ``Default value``   : proxy
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """

    return SslServices(device).conf_ssl_preferred_cipher(*args, **kwargs)


def conf_ssl_proxy_ignore_serv_auth(device=None, *args, **kwargs):
    """
    SSL server certificate authentification failure ignore configuration
    Example :-
        conf_ssl_proxy_ignore_serv_auth( device=device, sslprofile="sslprofile")
        conf_ssl_proxy_ignore_serv_auth(device=device, mode="delete",
         sslprofile="sslprofile")
    Robot example :-
        conf ssl proxy ignore serv auth    device=$(device)
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
            ``Default value``   : proxy
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_ignore_serv_auth(*args, **kwargs)


def conf_ssl_proxy_trusted_ca(device=None, *args, **kwargs):
    """
    Trusted certificate configuration
    Example :-
            conf_ssl_proxy_trusted_ca(device=device, trusted_ca_list="all",
            sslprofile ="sslprofile")
            conf_ssl_proxy_trusted_ca(device=device, mode="delete", trusted_ca_list="all",
            sslprofile = "sslprofile")
            conf_ssl_proxy_trusted_ca(device=device, trusted_ca_list="all test1 test2 test3",
            sslprofile = "sslprofile")
            conf_ssl_proxy_trusted_ca(device=device, mode="delete", trusted_ca_list="all test1
            test2 test3", sslprofile = "sslprofile")
            conf_ssl_proxy_trusted_ca(device=device, mode="delete", sslprofile = "sslprofile")
    Robot example :-
            conf ssl proxy trusted ca    device=$(device)    trusted_ca_list=all
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
            ``Default value``   : proxy
    :param str sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_trusted_ca(*args, **kwargs)


def conf_ssl_proxy_flow_trace(device=None, *args, **kwargs):
    """
    Flow trace configuration in global ssl service level
    Example :-
            conf_ssl_proxy_flow_trace(device=device, sslprofile ="sslprofile")
            conf_ssl_proxy_flow_trace(device=device, mode="delete", sslprofile ="sslprofile")
    Robot example :-
            conf ssl proxy flow trace    device=$(device)    sslprofile=sslprofile

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslplugin:
        *OPTIONAL* SSL plugin type selection
            ``Supported values``: proxy, initiation or termination
            ``Default value``   : proxy
    :param str sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_flow_trace(*args, **kwargs)


def conf_disable_ssl_proxy_resump(device=None, *args, **kwargs):
    """
    SSL session resumption configuration
    Example :-
            conf_disable_ssl_proxy_resump(device=device, sslprofile="sslprofile")
            conf_disable_ssl_proxy_resump(device=device, mode="delete",
            sslprofile="sslprofile")
    Robot example :-
            conf disable ssl proxy resump    device=$(device)    sslprofile=sslprofile

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslprofile:
        *REQUIRED* ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_disable_ssl_proxy_resump(*args, **kwargs)


def conf_ssl_proxy_renegotiation(device=None, *args, **kwargs):
    """
    SSL session renegotiation configuration
    Example :-
            conf_ssl_proxy_renegotiation(device=device, sslprofile="sslprofile",
            renegotiation="allow-secure")
            conf_ssl_proxy_renegotiation(device=device, mode="delete", sslprofile="sslprofile",
            renegotiation="allow")
    Robot example :-
            conf ssl proxy renegotiation    device=$(device)    sslprofile=sslprofile
            renegotiation=allow-secure

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslprofile:
        *REQUIRED* ssl proxy profile name mandatory option to be passed
    :param renegotiation:
        *REQUIRED* renegotiation configuration options "allow", "allow-secure" or "drop"
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_proxy_renegotiation(*args, **kwargs)


def conf_ssl_proxy_logging(device=None, *args, **kwargs):
    """
    SSLFP logging configuration
    Example: -
            conf_ssl_proxy_logging(device=device, sslprofile= "sslprofile",
            log="sessions-whitelisted")
            conf_ssl_proxy_logging(device=device, mode="delete", sslprofile="sslprofile",
             log = "all")
    Robot example :-
            conf ssl proxy logging    device=$(device)    sslprofile=sslprofile
            log=sessions-whitelisted

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param log:
        * REQUIRED * log action configuration options:
            ``Supported values``: all                  Log all events
                                  errors               Log all error events
                                  info                 Log all information events
                                  sessions-allowed     Log ssl session allow events after an error
                                  sessions-dropped     Log only ssl session drop events
                                  sessions-ignored     Log  session ignore events
                                  sessions-whitelisted  Log ssl session whitelist events
                                  warning              Log all warning events
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_proxy_logging(*args, **kwargs)


def conf_ssl_proxy_whitelist(device=None, *args, **kwargs):
    """
    Whitelist configuration with global address book
    Example :-
            conf_ssl_proxy_whitelist(device=device, whitelist="DNS-server DNS-server2",
            sslprofile="sslprofile")
            conf_ssl_proxy_whitelist(device=device, mode="delete",
            whitelist="DNS-server DNS-server2", sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist(device=device, mode="delete", sslprofile="sslprofile")
    Robot example :-
            conf ssl proxy whitelist    device=$(device)    whitelist=DNS-server DNS-server2
            sslprofile=sslprofile

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str whitelist:
        *REQUIRED* Configure whitelist with global address book
    : param str sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_proxy_whitelist(*args, **kwargs)


def conf_sslsp_server_cert_list(device=None, *args, **kwargs):
    """
    SSL Server protection Server certification list configuration
    Example :-
            conf_sslsp_server_cert_list(device=device, sslprofile="sslprofile",
            servercert="ssl-inspect-ca")
            conf_sslsp_server_cert_list(device=device, mode="delete", sslprofile="sslprofile",
            servercert="ssl-inspect-ca")
            conf_sslsp_server_cert_list(device=device, mode="delete", sslprofile="sslprofile")
    Robot example :-
            conf sslsp server cert list    device=$(device)    sslprofile=sslprofile
            servercert=ssl-inspect-ca

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslprofile:
        *REQUIRED* ssl proxy profile name mandatory option to be passed
    :param servercert:
        *REQUIRED* Server certification list profile a mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_sslsp_server_cert_list(*args, **kwargs)


def conf_ssl_proxy_protocol_version(device=None, *args, **kwargs):
    """
    SSL TLS version configuration
    Example :-
            conf_ssl_proxy_protocol_version(device=device, sslprofile="sslinit",
            tls_version="tls11")
            conf_ssl_proxy_protocol_version(device=device, mode="delete",
            sslprofile="sslinit", tls_version="tls11")
    Robot example :-
            conf ssl proxy protocol version    device=$(device)    sslprofile=sslinit
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
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_protocol_version(*args, **kwargs)


def conf_ssl_proxy_whitelist_url(device=None, *args, **kwargs):
    """
    Whitelist configuration with global address book
    Example :-
            conf_ssl_proxy_whitelist(device=device,
            whitelist="Enhanced_Financial_Data_and_Services", sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist(device=device, mode="delete",
            whitelist="Enhanced_Financial_Data_and_Services", sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist(device=device,  whitelist="Enhanced_Social_Web_Facebook",
             sslprofile = "sslprofile")
            conf_ssl_proxy_whitelist(device=device, mode="delete", sslprofile = "sslprofile")
    Robot example :-
            conf sslfp whitelist    device=$(device)    mode="delete"
            sslprofile = "sslprofile"

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param whitelist:
        *REQUIRED* Configure whitelist with global address book. Not mandatory when user wants\
        delete complete whitelist configuration from profile
    : param sslprofile:
        * REQUIRED * ssl proxy profile name mandatory option to be passed
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_proxy_whitelist_url(*args, **kwargs)


def conf_ssl_proxy(device=None, *args, **kwargs):
    """
    Configuring SSL proxy in either client or server protection mode
    Example :-
        conf_ssl_proxy(device=device,
                            sslplugin='forward_proxy',
                            sslprofile='sslprofile',
                            certidentifier='ssl-inspect-ca',
                            whitelist_url="Enhanced_Financial_Data_and_Services
                            Enhanced_Social_Web_Facebook",
                            log="all",
                            renegotiation="allow",
                            resumption="disable",
                            enable_flow_trace="true",
                            trusted_ca_list='all',
                            ignore_server_auth="true",
                            ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-sha',
                            crlaction='if-not-present',
                            ifnotpresent='allow',
                            tls_version='all'
                            )
        conf_ssl_proxy(sslprofile='sslprofile', mode='delete')
    Robot example :-
        conf ssl proxy    device=${handle}    sslprofile='sslprofile'    mode='delete'

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
    :param str sslplugin:
        **REQUIRED** ssl plugin type selection
            ``Supported values``: forward_proxy or reverse_proxy
    :param str whitelist_url:
        *OPTIONAL* Configure whitelist url categories
    :param str whitelist:
        *OPTIONAL* Configure whitelist with global address book. Not mandatory when user wants
        delete complete whitelist configuration from profile
    :param str log:
        *OPTIONAL* log action configuration options:
            ``Supported values``: all                  Log all events
                                  errors               Log all error events
                                  info                 Log all information events
                                  sessions-allowed     Log ssl session allow events after error
                                  sessions-dropped     Log only ssl session drop events
                                  sessions-ignored     Log  session ignore events
                                  sessions-whitelisted  Log ssl session whitelist events
                                  warning              Log all warning events
    :param str renegotiation:
        *OPTIONAL* renegotiation configuration options
            ``Supported values``: allow, allow-secure or drop
    :param str resumption:
        *OPTIONAL* disable resumption
            ``Supported values``: disable
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
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_proxy(*args, **kwargs)


def get_vty_jsf_ssl_counters(device=None, pic_name=None):
    """
    To get JSF SSL counter values
    Example:
        get_vty_jsf_ssl_counters(device=device_handle)
        get_vty_jsf_ssl_counters(device=device_handle, pic_name="FPC1.PIC1")
    ROBOT Example:
        Get vty jsf SSL counters   device=${device_handle}
        Get vty jsf SSL counters   device=${device_handle}   pic_name=FPC1.PIC1

    :param Device device:
        **REQUIRED** Device handle of the DUT
    :param str pic_name:
        *OPTIONAL* To get the Counter values of a particular PIC. If not provided, Added value of
        hit counts from all the PICs will be returned.
    :returns: Dictionary (key=counter name, value=hit count)
    :rtype: dict
    """
    if device is None:
        raise ValueError("device is a mandatory argument")

    return get_vty_counters_as_dictionary(device=device, pic_name=pic_name,
                                          command="show usp jsf counters junos-ssl-policy")


def conf_ssl_proxy_scale(device=None, *args, **kwargs):
    """
    Configuring SSL proxy in either client or server protection mode
    Example :-
        conf_ssl_proxy_scale(device=device_handle,
                            sslplugin='forward_proxy',
                            sslprofile='sslprofile',
                            certidentifier='ssl-inspect-ca',
                            whitelist_url="Enhanced_Financial_Data_and_Services
                                Enhanced_Social_Web_Facebook",
                            log="all",
                            renegotiation="allow",
                            resumption="disable",
                            enable_flow_trace="true",
                            trusted_ca_list='all',
                            ignore_server_auth="true",
                            ciphersuite='rsa-with-rc4-128-md5 rsa-with-rc4-128-sha',
                            crlaction='if-not-present',
                            ifnotpresent='allow',
                            tls_version='all',
                            count='250',
                            commitcount='50'
                            )
        conf_ssl_proxy_scale(device=device_handle, sslprofile='sslprofile', mode='deLeTe')
    Robot example :-
        conf ssl proxy scale    device=${handle}    sslprofile='sslprofile'    mode='delete'

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
    :param str sslplugin:
        **REQUIRED** ssl plugin type selection
            ``Supported values``: forward_proxy or reverse_proxy
    :param str whitelist_url:
        *OPTIONAL* Configure whitelist url categories
    :param str whitelist:
        *OPTIONAL* Configure whitelist with global address book. Not mandatory when user wants
        delete complete whitelist configuration from profile
    :param str log:
        *OPTIONAL* log action configuration options:
            ``Supported values``: all                  Log all events
                                  errors               Log all error events
                                  info                 Log all information events
                                  sessions-allowed     Log ssl session allow events after error
                                  sessions-dropped     Log only ssl session drop events
                                  sessions-ignored     Log  session ignore events
                                  sessions-whitelisted  Log ssl session whitelist events
                                  warning              Log all warning events
    :param str renegotiation:
        *OPTIONAL* renegotiation configuration options
            ``Supported values``: allow, allow-secure or drop
    :param str resumption:
        *OPTIONAL* disable resumption
            ``Supported values``: disable
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
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :param str count:
        *OPTIONAL* no of profiles to be configured
            ``Default value``   : 100
    :param str commitcount:
        *OPTIONAL* iteration limit count to commit
            ``Default value``   : 25
    :return: Returns "True"
    :rtype: bool
    """
    return SslServices(device).conf_ssl_proxy_scale(*args, **kwargs)
