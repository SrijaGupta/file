#!/usr/bin/python3
"""
#  DESCRIPTION:  SSL Services common APIs flat toby wrapper
#  AUTHOR:  Thyagarajan S Pasupathy (), thyag@juniper.net
"""
import re
from jnpr.toby.security.ssl.sslservices import SslServices


def get_ssl_statistics(device=None, *args, **kwargs):
    """
    Keyword to fetch ssl proxy statistics
    Example :-
        get_ssl_statistics(device=device, )
        get_ssl_statistics(device=device, node="node0")
        get_ssl_statistics( pic="fpc1 pic1")
    Robot example :-
        get ssl statistics    device=$(device)    node="node0"

    :param str device:
        **REQUIRED** Handle of the device
    :param str node:
        *OPTIONAL*  HA node selection
            ``Supported values``: node0 or node1
            ``Default value``   : local
    :param str pic:
        *OPTIONAL* Pass pic value to fetch details for the respective pic alone
            ``Supported values``: "fpc1 pic0", "fpc2 pic1" etc as per requirement
    :return: Returns the dict object with values of each of the counters from statistics output
    :rtype: dict
    """
    return SslServices(device).get_ssl_statistics(*args, **kwargs)


def clear_ssl_statistics(device=None, *args, **kwargs):
    """
    Keyword to clear ssl proxy statistics
    Example :-
        clear_ssl_statistics( device=device)
        clear_ssl_statistics( device=device, node="node0")
    Robot example :-
        clear ssl statistics    device=$(device)    node="node0"

    :param str device:
        **REQUIRED** Handle of the device
    :param str node:
        *OPTIONAL*  HA node selection
            ``Supported values``: node0 or node1
            ``Default value``   : local
    """
    return SslServices(device).clear_ssl_statistics(*args, **kwargs)


def conf_ssl_trace_options(device=None, *args, **kwargs):
    """
    ssl proxy/init/terminate trace options configuration
    Example :-
        configure_ssl_trace_options(device=device,  filename="ssl-userfile",
        maxfiles="10", size="100", worldreadable="yes",flag="cli-configuration",
         level="extensive", noremotetrace="yes")
        configure_ssl_trace_options(device=device, mode="delete",
        filename="ssl-userfile", maxfiles="10", size="100", worldreadable="yes",
        flag="cli-configuration", level="extensive", noremotetrace="yes")
    Robot example :-
        configure ssl trace options    device=$(device)    mode=delete
        filename=ssl-userfile    maxfiles=10    size=100    worldreadable=yes
        flag=cli-configuration    level=extensive    noremotetrace=yes

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str filename:
        *OPTIONAL* Name of the ssl traceoptions file to log traces
            ``Default value``   : ssl_trace
    :param int maxfiles:
        *OPTIONAL* Maximum no of trace files to be created on system
            ``Default value``   : 3
    :param int size:
        *OPTIONAL* Maximum size of the trace file
            ``Default value``   : 128000
    :param str worldreadable:
        *OPTIONAL* world-readable configuration
            ``Supported values``: true or false
    :param str flag:
        *OPTIONAL* Configure trace flag options
            ``Supported values``: all, cli-configuration, initiation, proxy,
            selected-profile or termination
    :param str level:
        *OPTIONAL* Configure trace level options
            ``Supported values``: brief, detail, extensive or verbose
            ``Default value``   : brief
    :param str noremotetrace:
        *OPTIONAL* Disable remote tracing
            ``Supported values``: yes or no
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """

    return SslServices(device).conf_ssl_trace_options(*args, **kwargs)


def conf_ssl_cache_timeout(device=None, *args, **kwargs):
    """
    SSL session cache timeout configuration
    Example :-
        configure_ssl_cache_timeout( device=device, sslprofile = "sslprofile",
         timeout="300")
        configure_ssl_cache_timeout(device=device, mode="delete",
        sslprofile = "sslprofile", timeout="300")
    Robot example :-
        configure ssl cache timeout    device=$(device)    sslprofile=sslprofile
            timeout=300

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str sslprofile:
        **REQUIRED** ssl proxy profile name mandatory option to be passed
    :param str timeout:
        **REQUIRED** cache timeout for ssl session
            ``Supported values``: 300 to 3600 seconds
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """

    return SslServices(device).conf_ssl_cache_timeout(*args, **kwargs)


def conf_cert_cache_config(device=None, **kwargs):
    """
    SSL session cache timeout configuration
    Example :-
        conf_cert_cache_config( device=device, cmd = "certificate-cache-timeout",
         timeout="300")
        conf_cert_cache_config(device=device, mode="delete",
        cmd = "certificate-cache-timeout", timeout="300")
        conf_cert_cache_config( device=device, cmd = "disable-cert-cache")
        conf_cert_cache_config(device=device, mode="delete",
        cmd = "disable-cert-cache")

    Robot example :-
        conf cert cache config    device=$(device)    cmd=certificate-cache-timeout
            timeout=300
        conf cert cache config    device=$(device)    cmd=disable-cert-cache

    :param str device:
        **REQUIRED** Handle of the device
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str cmd:
        **REQUIRED** cmd name mandatory argument to be passed
    :param str timeout:
        **REQUIRED** cache timeout for cert cache if cmd is certificate-cache-timeout
            ``Supported values``: 300 to 3600 seconds
    :param str commit:
        *OPTIONAL* commit configuration option
            ``Supported values``: yes or no
            ``Default value``   : yes
    :return: Returns "True"
    :rtype: bool
    """

    return SslServices(device).conf_cert_cache_config( **kwargs)



def enroll_local_ca_cert_key(device=None, **kwargs):
    """
    Requests local CA certificate and enrolls it
    Example :-
        enroll_local_ca_cert_key( device=device, filename = "test.crt",
         key="test.key", certid = "test")

    Robot example :-
        enroll local ca cert key    device=device    filename=test.crt    key="test.key
        certid=test

    :param device:
        **REQUIRED** Router handle
    :param filename:
        **REQUIRED** file CA certificate can be enrolled from
    :param key:
        **REQUIRED** key file of certificate can be enrolled from
    :param certid:
        **REQUIRED** certid to enroll certificate and key into
    return:
           Returns true if enrolled successfully else False
    """

    device.log(level="INFO",
               message="-------------------------------------------------------------\n")
    device.log(level="INFO", message="\t\t\tENROLLING CA CERTIFICATE")
    device.log(level="INFO",
               message="-------------------------------------------------------------\n")
    cmdlist = []
    response = None

    filename = kwargs.get('filename')
    key = kwargs.get('key')
    certid = kwargs.get('certid')

    if kwargs.get('filename') is not None and kwargs.get('key') is not None and kwargs.get(
            'certid') is not None:
        cmdlist.append(
            'request security pki local-certificate load filename ' + filename + ' key ' + key +
            ' certificate-id ' + certid)
    else:
        device.log(level="ERROR", message="Arguments: filename, key and certid are mandatory")
        raise ValueError("Arguments: filename, key and certid are mandatory")

    result = device.cli(command=cmdlist[0])
    result = (result.response())

    if re.search('.*successfully.*', str(result)):
        device.log(level="INFO",
                   message="---------Enrolled Local certificate %s successfully-------\n" % certid)
        response = True
    elif re.search('.*already exists.*', str(result)):
        device.log(level="INFO",
                   message="--------- CA certificate %s already exists. Please clear CA certs "
                           "before trying to enroll again-------\n" % certid)
        response = False
    elif re.search('.*syntax error.*', str(result)):
        device.log(level="ERROR", message="--------- Syntax Error -------\n")
        response = False
    else:
        device.log(level="ERROR",
                   message="---------Failed to enroll CA certificate %s -------\n" % certid)
        response = False

    return response
