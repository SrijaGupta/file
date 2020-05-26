"""
SSL Operational CLI

AUTHOR: aishan,ndahiya,mdabra
VERSION:  2.0

"""



import re
import time
import datetime
from pytz import timezone
from datetime import date, timedelta, time


####### PR 1416835
####### When there is NO output, PIC list SHOULD NOT BE SHOWN
####### keywords GET ALL CERTS and GET ALL PROFILES will fail if its EMPTY




##### Regarding session cache and cert cache ... as of now NO support of tenant
####### but given support in keyword

## https://gnats.juniper.net/web/default/1417614
##  https://gnats.juniper.net/web/default/1417613

# get cert names will fail in lsys. names appended with lsys a


def get_ssl_proxy_status(device=None, attribute=None, node="local", fpcpic=None):
    """
    Returns the SSL proxy status as Dictionary. In Multi PIC, if no fpc/pic value is provided,
    status of the 1st PIC is returned. Otherwise the specific fpc/pic value needs to be mentioned.

    Example:
        get_ssl_proxy_status(device=dut)
        get_ssl_proxy_status(device=dut, fpcpic=fpc1.pic2)

    ROBOT Example:
        Get ssl proxy status   device=${dut}
        Get ssl proxy status   device=${dut}    fpcpic=fpc1.pic2

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpcpic:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :return: returns SSL proxy status as dictionary
    :rtype: dict

    Example Returned Dictionary :

    {'ssl-status-async-crypto': 'disable',
     'ssl-status-cert-cache-activated': 'yes',
     'ssl-status-cert-nodes-in-use': '0',
     'ssl-status-invalidate-cert-cache-on-crl-update': 'Disabled',
     'ssl-status-local-logging': 'disable',
     'ssl-status-max-cert-cache-nodes': '4000',
     'ssl-status-max-sess-cache-nodes': '25000',
     'ssl-status-one-crypto': 'Enable',
     'ssl-status-pic-info': 'spu-6 fpc[1] pic[2]',
     'ssl-status-proxy-activation': 'Only if interested svcs configured',
     'ssl-status-sess-cache-activated': 'Activated',
     'ssl-status-sess-nodes-in-use': '0',
     'ssl-status-sslfp-pkid-link-status': 'UP'}
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    index = ''
    cmd = "show services ssl proxy status"
    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-status']['ssl-status']['ssl-status-pic']

    if not isinstance(status, list):
        status = [status]

    # to return specific fpc pic values
    if fpcpic is not None and len(fpcpic) > 4:
        flag = 0
        split_value = fpcpic.split('.')
        for item, value in zip(split_value, split_value):
            if 'FPC' in item:
                fpc = value.strip('FPCI')
            else:
                pic = value.strip('FPCI')
        for index in status:
            current_pic = index['ssl-status-pic-info']
            if re.match(".*fpc\[" + fpc + "\].*pic\[" + pic + "\].*", current_pic, re.DOTALL):
                flag = 1
                break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")
        return index

    # to return the cumulative value of the attribute in all pics
    if attribute is not None:
        value = 0
        for index in status:
            value = value + int(index['ssl-status-cert-nodes-in-use'])
        return value

    # to return 1st fpc pic values
    for index in status:
        return index


def get_ssl_cert_cache_stats(device=None, lsys=None, tenant=None, node="local", fpc=None, pic=None):
    """
    To get SSL Certificate cache statistics. In case of Multi PIC, a consolidated result is returned.
    If you want a per PIC result, pass 'fpc' and 'pic'.

    Example :
        get_ssl_cert_cache_stats(device=dut, fpc="1", pic="2")
        get_ssl_cert_cache_stats(device=dut)

    ROBOT Example :
        Get SSL Cert cache stats   device=${dut}  fpc=1  pic=2
        Get SSL Cert cache stats   device=${dut}


    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :return: Dictionary of stats as key value pairs.
    :rtype: dict

    Example Returned dictionary :

    {'cert_cache_miss': 1,
    'cert_cache_hit': 2,
    'cert_cache_full': 1}

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")


    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    dict_to_return = {}

    cmd = "show services ssl proxy certificate-cache statistics"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-proxy-cert-cache-statistics']['ssl-proxy-cert-cache-statistics']['ssl-proxy-cert-cache-statistics-pic']

    if not isinstance(status, list):
        status = [status]


    if fpc is not None:
        flag = 0
        for index in status:
            current_pic = index['ssl-proxy-cert-cache-statistics-pic-info']
            if re.match(r".*fpc\[" + fpc + r"\].*pic\[" + pic + r"\].*", current_pic, re.DOTALL):
                flag = 1
                ssl_statistics = index
                break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")

        dict_to_return['cert_cache_hit'] = int(ssl_statistics['ssl-proxy-cert-cache-statistics-sess-cache-hit'])
        dict_to_return['cert_cache_miss'] = int(ssl_statistics['ssl-proxy-cert-cache-statistics-sess-cache-miss'])
        dict_to_return['cert_cache_full'] = int(ssl_statistics['ssl-proxy-cert-cache-statistics-sess-cache-full'])

        return dict_to_return

    dict_to_return['cert_cache_hit'] = 0
    dict_to_return['cert_cache_miss'] = 0
    dict_to_return['cert_cache_full'] = 0

    for index in status:
        dict_to_return['cert_cache_hit'] = dict_to_return['cert_cache_hit'] + int(index['ssl-proxy-cert-cache-statistics-sess-cache-hit'])
        dict_to_return['cert_cache_miss'] = dict_to_return['cert_cache_miss'] + int(index['ssl-proxy-cert-cache-statistics-sess-cache-miss'])
        dict_to_return['cert_cache_full'] = dict_to_return['cert_cache_full'] + int(index['ssl-proxy-cert-cache-statistics-sess-cache-full'])

    return dict_to_return


def get_ssl_session_cache_stats(device=None, lsys=None, tenant=None, node="local", fpc=None, pic=None):
    """
    To get SSL Session cache statistics. In case of Multi PIC, a consolidated result is returned.
    If you want a per PIC result, pass 'fpc' and 'pic'.

    Example :
        get_ssl_session_cache_stats(device=dut, fpc="1", pic="2")
        get_ssl_session_cache_stats(device=dut)

    ROBOT Example :
        Get SSL Session cache stats   device=${dut}  fpc=1  pic=2
        Get SSL Session cache stats   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :return: Dictionary of stats as key value pairs.
    :rtype: dict

    Example Returned dictionary :

    {'session_cache_miss': 1,
    'session_cache_hit': 2,
    'session_cache_full': 1}

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")


    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    dict_to_return = {}

    cmd = "show services ssl proxy session-cache statistics"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-proxy-sess-cache-statistics']['ssl-proxy-sess-cache-statistics']['ssl-proxy-sess-cache-statistics-pic']

    if not isinstance(status, list):
        status = [status]


    if fpc is not None:
        flag = 0
        for index in status:
            current_pic = index['ssl-proxy-sess-cache-statistics-pic-info']
            if re.match(r".*fpc\[" + fpc + r"\].*pic\[" + pic + r"\].*", current_pic, re.DOTALL):
                flag = 1
                ssl_proxy_statistics = index
                break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")

        dict_to_return['session_cache_hit'] = int(ssl_proxy_statistics['ssl-proxy-sess-cache-statistics-sess-cache-hit'])
        dict_to_return['session_cache_miss'] = int(ssl_proxy_statistics['ssl-proxy-sess-cache-statistics-sess-cache-miss'])
        dict_to_return['session_cache_full'] = int(ssl_proxy_statistics['ssl-proxy-sess-cache-statistics-sess-cache-full'])

        return dict_to_return

    dict_to_return['session_cache_hit'] = 0
    dict_to_return['session_cache_miss'] = 0
    dict_to_return['session_cache_full'] = 0

    for index in status:
        dict_to_return['session_cache_hit'] = dict_to_return['session_cache_hit'] + int(index['ssl-proxy-sess-cache-statistics-sess-cache-hit'])
        dict_to_return['session_cache_miss'] = dict_to_return['session_cache_miss'] + int(index['ssl-proxy-sess-cache-statistics-sess-cache-miss'])
        dict_to_return['session_cache_full'] = dict_to_return['session_cache_full'] + int(index['ssl-proxy-sess-cache-statistics-sess-cache-full'])

    return dict_to_return


def get_all_ssl_cert(device=None, lsys=None, tenant=None, node="local"):
    """
    Returns the all the certificate names present. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_all_ssl_cert(device=dut)

    ROBOT Example:
        GET all SSL Cert   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: List of Certificate names
    :rtype: list

    Example Returned list :
    ['ssl_inspect_ca1', 'ssl_inspect_ca3']

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")


    cmd = "show services ssl certificate all"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant


    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-certificate']['ssl-certificate']
    if not isinstance(status, dict):
        device.log(level="INFO", message="No SSL certificates present. Returning Empty list")
        return []

    status = status['ssl-certificate-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    for index in status:
        for index1 in status:
            if isinstance(index['ssl-cert-id'], list):
                if len(index['ssl-cert-id']) != len(index1['ssl-cert-id']):
                    flag = 0
                    break
                for a in index1['ssl-cert-id']:
                    if a not in index['ssl-cert-id']:
                        flag = 0
                        break
            else:
                if index['ssl-cert-id'] != index1['ssl-cert-id']:
                    flag = 0
                    break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    if isinstance(index['ssl-cert-id'], list):
        index2 = []
        for val in index['ssl-cert-id']:
            index2.append(str(val))
        return index2

    return [str(index['ssl-cert-id'])]


def get_all_ssl_profile(device=None, lsys=None, tenant=None, node="local"):
    """
    Returns the all the Profile names with profile IDs. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_all_ssl_profile(device=dut)

    ROBOT Example:
        GET all SSL Profile   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dict with profile IDs as values and profile name as keys
    :rtype: dict

    Example Returned dictionary :

    {'p1': '10',
     'p3': '11'}

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    cmd = "show services ssl proxy profile all"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-profile-list']
    if not isinstance(status, dict):
        device.log(level="INFO", message="No SSL Profiles present. Returning Empty list")
        return []

    status = status['ssl-profile-list-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # With this for loop, checking the values across PICS are same
    for x in status:
        for y in status:
            if isinstance(x['ssl-profile-id'], list):
                if len(x['ssl-profile-id']) != len(y['ssl-profile-id']):
                    flag = 0
                    break
                if len(x['ssl-profile-name']) != len(y['ssl-profile-name']):
                    flag = 0
                    break
                for a in y['ssl-profile-id']:
                    if a not in x['ssl-profile-id']:
                        flag = 0
                        break
                for a in y['ssl-profile-name']:
                    if a not in x['ssl-profile-name']:
                        flag = 0
                        break
            else:
                if x['ssl-profile-id'] != y['ssl-profile-id']:
                    flag = 0
                    break
                if x['ssl-profile-name'] != y['ssl-profile-name']:
                    flag = 0
                    break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    dict_to_return = {}

    if not isinstance(x['ssl-profile-id'], list):
        dict_to_return[str(x['ssl-profile-name'])] = str(x['ssl-profile-id'])

    else:
        for val1, val2 in zip(x['ssl-profile-name'], x['ssl-profile-id']):
            dict_to_return[str(val1)] = str(val2)

    return dict_to_return


def get_ssl_profile(device=None, lsys=None, tenant=None, node="local", profile=None):
    """
    Returns the details of the SSL Profile required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_ssl_profile(device=dut, profile="p1")

    ROBOT Example:
        Get SSL Profile   device=${dut}   profile=p1

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str profile:
        **REQUIRED** Profile name whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dictionary with details of Profile as key value pairs
    :rtype: dict

    Example Returned Dictionary :

    {'ssl-profile-allow-non-ssl-session': 'true',
     'ssl-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
     'ssl-profile-initiation-profile-id': '65537',
     'ssl-profile-nof-whitelist-entries': '0',
     'ssl-profile-profile': 'p1',
     'ssl-profile-root-ca': 'false',
     'ssl-profile-termination-profile-id': '65537',
     'ssl-profile-trace': 'false'}

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if profile is None:
        device.log(level="ERROR", message="'profile' is a mandatory argument")
        raise ValueError("'profile' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    cmd = "show services ssl proxy profile profile-name " + profile
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-profile-detail']['ssl-profile-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given Profile name is not configured on DUT")
        raise ValueError("Given Profile name is not configured on DUT")

    status = status['ssl-profile-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for x in status:
        for y in status:
            if x['ssl-profile-allow-non-ssl-session'] != y['ssl-profile-allow-non-ssl-session']:
                flag = 0
                break
            if x['ssl-profile-initiation-profile-id'] != y['ssl-profile-initiation-profile-id']:
                flag = 0
                break
            if x['ssl-profile-nof-whitelist-entries'] != y['ssl-profile-nof-whitelist-entries']:
                flag = 0
                break
            if x['ssl-profile-profile'] != y['ssl-profile-profile']:
                flag = 0
                break
            if x['ssl-profile-root-ca'] != y['ssl-profile-root-ca']:
                flag = 0
                break
            if x['ssl-profile-termination-profile-id'] != y['ssl-profile-termination-profile-id']:
                flag = 0
                break
            if x['ssl-profile-trace'] != y['ssl-profile-trace']:
                flag = 0
                break

        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return x


def get_ssl_local_cert_detail(device=None, lsys=None, tenant=None, node="local", cert_id=None, pic_info=None):
    """
    Returns the details of the Certificate required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_ssl_local_cert_detail(device=dut, cert_id="ssl_inspect_ca")

    ROBOT Example:
        get SSL Local Cert Detail  device=${dut}   cert_id=ssl_inspect_ca

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str cert_id:
        **REQUIRED** Certificate Identifier whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str pic_info:
        *OPTIONAL* Name of the pic.
    :return: Dictionary with details of Certificate as key value pair
    :rtype: dict

    Example Returned Dictionary :

    {   'ssl-cert-modify-time': 'Wed 01/30/2019 10:00:27 AM',
        'ssl-cert-type' : 'LOCAL-CERT',
        'ssl-certificate-id': 'ssl_inspect_ca1',
        'ssl-certificate-id-detail-pic-info': 'spu-5 fpc[1] pic[1]',
        'ssl-certificate-version': '3',
        'ssl-issuer': '/CN=www.juniper2_self.net/OU=IT/O=Juniper',
        'ssl-key-modify-time': 'Wed 01/30/2019 10:00:27 AM',
        'ssl-public-key-algorithm': 'rsaEncryption',
        'ssl-serial-number': '62 3a f4 f4 52 e2 9b 56 3e bf ea 01 59 b0 6d 71',
        'ssl-signature-algorithm': 'sha256WithRSAEncryption',
        'ssl-subject': '/CN=www.juniper2_self.net/OU=IT/O=Juniper',
        'ssl-validity-not-after': 'Mon 01/29/2024 10:00:27 AM',
        'ssl-validity-not-before': 'Wed 01/30/2019 10:00:27 AM'}

    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if cert_id is None:
        device.log(level="ERROR", message="'cert_id' is a mandatory argument")
        raise ValueError("'cert_id' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    cmd = "show services ssl certificate detail certificate-id " + cert_id
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant
    if pic_info is not None:
        cmd = cmd + " pic-info " + pic_info

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-certificate-id-detail']['ssl-certificate-id-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given cert_id is not loaded on the DUT")
        raise ValueError("Given cert_id is not loaded on the DUT")

    status = status['ssl-certificate-id-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for x in status:
        for y in status:
            if  x['ssl-cert-modify-time'] != y['ssl-cert-modify-time']:
                flag = 0
                break
            if  x['ssl-cert-type'] != y['ssl-cert-type']:
                flag = 0
                break
            if  x['ssl-certificate-id'] != y['ssl-certificate-id']:
                flag = 0
                break
            if  x['ssl-certificate-version'] != y['ssl-certificate-version']:
                flag = 0
                break
            if  x['ssl-issuer'] != y['ssl-issuer']:
                flag = 0
                break
            if  x['ssl-key-modify-time'] != y['ssl-key-modify-time']:
                flag = 0
                break
            if  x['ssl-public-key-algorithm'] != y['ssl-public-key-algorithm']:
                flag = 0
                break
            if  x['ssl-serial-number'] != y['ssl-serial-number']:
                flag = 0
                break
            if  x['ssl-signature-algorithm'] != y['ssl-signature-algorithm']:
                flag = 0
                break
            if  x['ssl-subject'] != y['ssl-subject']:
                flag = 0
                break
            if  x['ssl-validity-not-after'] != y['ssl-validity-not-after']:
                flag = 0
                break
            if  x['ssl-validity-not-before'] != y['ssl-validity-not-before']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return x



def get_ssl_ca_cert_detail(device=None, lsys=None, tenant=None, node="local", cert_id=None, pic_info=None):
    """
    Returns the details of the Certificate required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_ssl_ca_cert_detail(device=dut, cert_id="ssl_inspect_ca")

    ROBOT Example:
        get SSL CA Cert Detail  device=${dut}   cert_id=ssl_inspect_ca

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str cert_id:
        **REQUIRED** Certificate Identifier whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str pic_info:
        *OPTIONAL* Name of the pic.
    :return: Dictionary with details of Certificate as key value pair
    :rtype: dict

    Example Returned Dictionary :

    {   'ssl-cert-modify-time': 'Wed 01/30/2019 10:00:27 AM',
        'ssl-cert-type' : 'CA-CERT',
        'ssl-certificate-id': 'ssl_inspect_ca1',
        'ssl-certificate-id-detail-pic-info': 'spu-5 fpc[1] pic[1]',
        'ssl-certificate-version': '3',
        'ssl-crl-check': 'enabled',
        'ssl-crl-check-on-download-failed': 'enabled',
        'ssl-crl-download-failed': 'true',
        'ssl-crl-present': 'no',
        'ssl-issuer': '/CN=www.juniper2_self.net/OU=IT/O=Juniper',
        'ssl-public-key-algorithm': 'rsaEncryption',
        'ssl-serial-number': '62 3a f4 f4 52 e2 9b 56 3e bf ea 01 59 b0 6d 71',
        'ssl-signature-algorithm': 'sha256WithRSAEncryption',
        'ssl-subject': '/CN=www.juniper2_self.net/OU=IT/O=Juniper'}

    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if cert_id is None:
        device.log(level="ERROR", message="'cert_id' is a mandatory argument")
        raise ValueError("'cert_id' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    cmd = "show services ssl certificate detail certificate-id " + cert_id
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant
    if pic_info is not None:
        cmd = cmd + " pic-info " + pic_info

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-certificate-id-detail']['ssl-certificate-id-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given cert_id is not loaded on the DUT")
        raise ValueError("Given cert_id is not loaded on the DUT")

    status = status['ssl-certificate-id-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for x in status:
        for y in status:
            if  x['ssl-cert-modify-time'] != y['ssl-cert-modify-time']:
                flag = 0
                break
            if  x['ssl-cert-type'] != y['ssl-cert-type']:
                flag = 0
                break
            if  x['ssl-certificate-id'] != y['ssl-certificate-id']:
                flag = 0
                break
            if  x['ssl-certificate-version'] != y['ssl-certificate-version']:
                flag = 0
                break
            if  x['ssl-crl-check'] != y['ssl-crl-check']:
                flag = 0
                break
            if  x['ssl-crl-check-on-download-failed'] != y['ssl-crl-check-on-download-failed']:
                flag = 0
                break
            if  x['ssl-crl-download-failed'] != y['ssl-crl-download-failed']:
                flag = 0
                break
            if  x['ssl-crl-present'] != y['ssl-crl-present']:
                flag = 0
                break
            if  x['ssl-issuer'] != y['ssl-issuer']:
                flag = 0
                break
            if  x['ssl-public-key-algorithm'] != y['ssl-public-key-algorithm']:
                flag = 0
                break
            if  x['ssl-serial-number'] != y['ssl-serial-number']:
                flag = 0
                break
            if  x['ssl-signature-algorithm'] != y['ssl-signature-algorithm']:
                flag = 0
                break
            if  x['ssl-subject'] != y['ssl-subject']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return x



def get_ssl_local_cert_brief(device=None, lsys=None, tenant=None, node="local", cert_id=None, pic_info=None):
    """
    Returns the details of the Certificate required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_ssl_local_cert_brief(device=dut, cert_id="ssl_inspect_ca")

    ROBOT Example:
        get SSL Local Cert Brief  device=${dut}   cert_id=ssl_inspect_ca

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str cert_id:
        **REQUIRED** Certificate Identifier whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str pic_info:
        *OPTIONAL* Name of the pic.
    :return: Dictionary with details of Certificate as key value pair
    :rtype: dict

    Example Returned Dictionary :

    {   'ssl-certificate-id': 'ssl_inspect_ca1',
        'ssl-cert-type' : 'LOCAL-CERT',
        'ssl-issuer': '/CN=www.juniper2_self.net/OU=IT/O=Juniper',
        'ssl-public-key-algorithm': 'rsaEncryption',
        'ssl-subject': '/CN=www.juniper2_self.net/OU=IT/O=Juniper',
        'ssl-validity-not-after': 'Mon 01/29/2024 10:00:27 AM',
        'ssl-validity-not-before': 'Wed 01/30/2019 10:00:27 AM'}

    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if cert_id is None:
        device.log(level="ERROR", message="'cert_id' is a mandatory argument")
        raise ValueError("'cert_id' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    cmd = "show services ssl certificate brief certificate-id " + cert_id
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant
    if pic_info is not None:
        cmd = cmd + " pic-info " + pic_info

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-certificate-id-detail']['ssl-certificate-id-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given cert_id is not loaded on the DUT")
        raise ValueError("Given cert_id is not loaded on the DUT")

    status = status['ssl-certificate-id-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for x in status:
        for y in status:
            if x['ssl-certificate-id'] != y['ssl-certificate-id']:
                flag = 0
                break
            if x['ssl-cert-type'] != y['ssl-cert-type']:
                flag = 0
                break
            if x['ssl-issuer'] != y['ssl-issuer']:
                flag = 0
                break
            if x['ssl-public-key-algorithm'] != y['ssl-public-key-algorithm']:
                flag = 0
                break
            if x['ssl-subject'] != y['ssl-subject']:
                flag = 0
                break
            if x['ssl-validity-not-after'] != y['ssl-validity-not-after']:
                flag = 0
                break
            if x['ssl-validity-not-before'] != y['ssl-validity-not-before']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return x


def get_ssl_ca_cert_brief(device=None, lsys=None, tenant=None, node="local", cert_id=None, pic_info=None):
    """
    Returns the details of the Certificate required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_ssl_ca_cert_brief(device=dut, cert_id="ssl_inspect_ca")

    ROBOT Example:
        get SSL CA Cert Brief  device=${dut}   cert_id=ssl_inspect_ca

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str cert_id:
        **REQUIRED** Certificate Identifier whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str pic_info:
        *OPTIONAL* Name of the pic.
    :return: Dictionary with details of Certificate as key value pair
    :rtype: dict

    Example Returned Dictionary :

    {   'ssl-certificate-id': 'ssl_inspect_ca1',
        'ssl-cert-type' : 'CA-CERT',
        'ssl-issuer': '/CN=www.juniper2_self.net/OU=IT/O=Juniper',
        'ssl-public-key-algorithm': 'rsaEncryption',
        'ssl-subject': '/CN=www.juniper2_self.net/OU=IT/O=Juniper'}

    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if cert_id is None:
        device.log(level="ERROR", message="'cert_id' is a mandatory argument")
        raise ValueError("'cert_id' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    cmd = "show services ssl certificate brief certificate-id " + cert_id
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant
    if pic_info is not None:
        cmd = cmd + " pic-info " + pic_info

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-certificate-id-detail']['ssl-certificate-id-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given cert_id is not loaded on the DUT")
        raise ValueError("Given cert_id is not loaded on the DUT")

    status = status['ssl-certificate-id-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for x in status:
        for y in status:
            if x['ssl-certificate-id'] != y['ssl-certificate-id']:
                flag = 0
                break
            if x['ssl-cert-type'] != y['ssl-cert-type']:
                flag = 0
                break
            if x['ssl-issuer'] != y['ssl-issuer']:
                flag = 0
                break
            if x['ssl-public-key-algorithm'] != y['ssl-public-key-algorithm']:
                flag = 0
                break
            if x['ssl-subject'] != y['ssl-subject']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return x



def get_ssl_cert_details(device=None, lsys=None, tenant=None, node="local", cert_id=None, type="local"):
    """
    Returns the details of the Certificate required.
    Example:
        get_ssl_cert_details(device=dut, cert_id="ssl_inspect_ca", type="local")

    ROBOT Example:
        get SSL Cert Details  device=${dut}   cert_id=ssl_inspect_ca    type=local

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str cert_id:
        **REQUIRED** Certificate Identifier whose details are required
    :param str type:
        **REQUIRED** Type of certificate whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dictionary with details of Certificate as key value pair
    :rtype: dict

    Example Returned Dictionary :

    {   'identifier' : 'p_1',
        'version' : '3',
    'serial-number' : 'bcb426cc9145eb836c798ec50531d433',
    'issuer-name-organization-name' : 'Juniper networks',
    'issuer-name-organizational-unit-name' : 'IT',
    'issuer-name-common-name' : 'www.myearth.net',
    'issuer-name-country-name' : 'IN',
    'issuer-name-state-or-province-name' : 'DL',
    'issuer-name-locality-name' : 'Delhi',
    'subject-name-organization-name' : 'Juniper networks',
    'subject-name-organizational-unit-name' : 'IT',
    'subject-name-common-name' : 'www.myearth.net',
    'subject-name-country-name' : 'IN',
    'subject-name-state-or-province-name' : 'DL',
    'subject-name-locality-name' : 'Delhi',
    'subject-string' : 'CN=www.myearth.net, OU=IT, O=Juniper networks, L=Delhi, ST=DL, C=IN',
    'not-before' : '04-29-2019 15:41 UTC',
    'not-after' : '04-27-2024 15:41 UTC',
    'public-key-algorithm' : 'rsaEncryption',
    'public-key-length' : '2048',
    'signature-algorithm' : 'sha256WithRSAEncryption' }

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if cert_id is None:
        raise ValueError("'cert_id' is a mandatory argument")

    if type is None:
        raise ValueError("'type' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    dict_to_return = {}

    if type == "local":
        cmd = "show security pki local-certificate detail certificate-id " + cert_id
    elif type == "ca":
        cmd = "show security pki ca-certificate detail ca-profile " + cert_id
    else:
        device.log(level="INFO", message="type should be either 'local' or 'ca'")
        raise ValueError("type should be either 'local' or 'ca'")

    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['x509-pki-certificate-info-list']['pkid-x509-certificate-information']

    if not isinstance(status, list):
        status = [status]

    for x in status:
        dict_to_return['identifier'] = x['identifier']
        dict_to_return['version'] = x['version']
        dict_to_return['serial-number'] = x['serial-number-list']['serial-number-x509']
        dict_to_return['issuer-name-organization-name'] = x['issuer-name']['distinguished-name']['organization-name']
        dict_to_return['issuer-name-organizational-unit-name'] = x['issuer-name']['distinguished-name']['organizational-unit-name']
        dict_to_return['issuer-name-common-name'] = x['issuer-name']['distinguished-name']['common-name']
        dict_to_return['issuer-name-country-name'] = x['issuer-name']['distinguished-name']['country-name']
        dict_to_return['issuer-name-state-or-province-name'] = x['issuer-name']['distinguished-name']['state-or-province-name']
        dict_to_return['issuer-name-locality-name'] = x['issuer-name']['distinguished-name']['locality-name']
        dict_to_return['subject-name-organization-name'] = x['subject-name']['distinguished-name']['organization-name']
        dict_to_return['subject-name-organizational-unit-name'] = x['subject-name']['distinguished-name']['organizational-unit-name']
        dict_to_return['subject-name-common-name'] = x['subject-name']['distinguished-name']['common-name']
        dict_to_return['subject-name-country-name'] = x['subject-name']['distinguished-name']['country-name']
        dict_to_return['subject-name-state-or-province-name'] = x['issuer-name']['distinguished-name']['state-or-province-name']
        dict_to_return['subject-name-locality-name'] = x['subject-name']['distinguished-name']['locality-name']
        dict_to_return['subject-string'] = x['subject-string-list']['subject-string']
        dict_to_return['not-before'] = x['validity']['not-before']
        dict_to_return['not-after'] = x['validity']['not-after']
        dict_to_return['public-key-algorithm'] = x['public-key']['public-key-algorithm']
        dict_to_return['public-key-length'] = x['public-key']['public-key-length']
        dict_to_return['signature-algorithm'] = x['signature-algorithm']

        return dict_to_return


def get_ssl_cert_cache_entries(device=None, lsys=None, tenant=None, node="local", fpc=None, pic=None):
    """
    To get SSL Certificate cache entries detail. In case of Multi PIC, a consolidated result is returned.
    If you want a per PIC result, pass 'fpc' and 'pic'.

    Example :
        get_ssl_cert_cache_entries(device=dut, fpc="1", pic="2")
        get_ssl_cert_cache_entries(device=dut)

    ROBOT Example :
        Get SSL Cert cache entries   device=${dut}  fpc=1  pic=2
        Get SSL Cert cache entries   device=${dut}


    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :return: Dictionary of stats as key value pairs.
    :rtype: dict

    Example Returned dictionary :

    {'cert-cache-entry': '1',
    'cert-cache-serial-number': '01',
    'cert-cache-init-profile-id': '77',
    'cert-cache-num-of-crl-update': '0',
    'cert-cache-status': 'Active: Time to expire 552 seconds',
    'cert-cache-interdicted-cert-type': '[0x1]: CA issued, Authentication Successful',
    'cert-cache-server-cert-verification-result': 'ok [0x0]',
    'cert-cache-cert-ref-count': '2',
    'cert-cache-subject': '/C=IN/ST=Karnataka/O=JuniperServer Inc/OU=JuniperServer/CN=JuniperServer Inc Root CA/emailAddress=mdabra@juniper.com',
    'cert-cache-issuer': '/CN=www.myearth.net/OU=IT/O=Juniper networks/L=Delhi/ST=DL/C=IN'}

    """
    index = ''

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    dict_to_return = {}

    cmd = "show services ssl proxy certificate-cache entries detail"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-proxy-cert-cache-entries']['ssl-proxy-cert-cache-entries']['ssl-proxy-cert-cache-entries-pic']

    if not isinstance(status, list):
        status = [status]

    if fpc is not None:
        flag = 0
        for index in status:
            if isinstance(index, dict):
                current_pic = index['ssl-proxy-cert-cache-entries-pic-info']
                if re.match(r".*fpc\[" + fpc + r"\].*pic\[" + pic + r"\].*", current_pic, re.DOTALL):
                    flag = 1
                    break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")

        dict_to_return['cert-cache-entry'] = index['ssl-proxy-cert-cache-entry']
        dict_to_return['cert-cache-serial-number'] = index['ssl-proxy-cert-cache-serial-number']
        dict_to_return['cert-cache-init-profile-id'] = index['ssl-proxy-cert-cache-init-profile-id']
        dict_to_return['cert-cache-num-of-crl-update'] = index['ssl-proxy-cert-cache-num-of-crl-update']
        dict_to_return['cert-cache-status'] = index['ssl-proxy-cert-cache-status']
        dict_to_return['cert-cache-interdicted-cert-type'] = index['ssl-proxy-cert-cache-interdicted-cert-type']
        dict_to_return['cert-cache-server-cert-verification-result'] = index['ssl-proxy-cert-cache-server-cert-verification-result']
        dict_to_return['cert-cache-cert-ref-count'] = index['ssl-proxy-cert-cache-cert-ref-count']
        dict_to_return['cert-cache-subject'] = index['ssl-proxy-cert-cache-subject']
        dict_to_return['cert-cache-issuer'] = index['ssl-proxy-cert-cache-issuer']

        return dict_to_return

    for index in status:
        dict_to_return['cert-cache-entry'] = index['ssl-proxy-cert-cache-entry']
        dict_to_return['cert-cache-serial-number'] = index['ssl-proxy-cert-cache-serial-number']
        dict_to_return['cert-cache-init-profile-id'] = index['ssl-proxy-cert-cache-init-profile-id']
        dict_to_return['cert-cache-num-of-crl-update'] = index['ssl-proxy-cert-cache-num-of-crl-update']
        dict_to_return['cert-cache-status'] = index['ssl-proxy-cert-cache-status']
        dict_to_return['cert-cache-interdicted-cert-type'] = index['ssl-proxy-cert-cache-interdicted-cert-type']
        dict_to_return['cert-cache-server-cert-verification-result'] = index['ssl-proxy-cert-cache-server-cert-verification-result']
        dict_to_return['cert-cache-cert-ref-count'] = index['ssl-proxy-cert-cache-cert-ref-count']
        dict_to_return['cert-cache-subject'] = index['ssl-proxy-cert-cache-subject']
        dict_to_return['cert-cache-issuer'] = index['ssl-proxy-cert-cache-issuer']

        return dict_to_return




def get_ssl_cert_cache_entries_summary(device=None, lsys=None, tenant=None, node="local", fpc=None, pic=None):
    """
    To get SSL Certificate cache entries summary. In case of Multi PIC, a consolidated result is returned.
    If you want a per PIC result, pass 'fpc' and 'pic'.

    Example :
        get_ssl_cert_cache_entries_summary(device=dut, fpc="1", pic="2")
        get_ssl_cert_cache_entries_summary(device=dut)

    ROBOT Example :
        Get SSL Cert cache entries summary  device=${dut}  fpc=1  pic=2
        Get SSL Cert cache entries summary  device=${dut}


    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :return: Dictionary of stats as key value pairs.
    :rtype: dict

    Example Returned dictionary :

    {'cert-cache-entry': '1',
    'cert-cache-serial-number': '01',
    'cert-cache-init-profile-id': '77',
    'cert-cache-num-of-crl-update': '0'}

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    dict_to_return = {}

    cmd = "show services ssl proxy certificate-cache entries summary"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-proxy-cert-cache-entries']['ssl-proxy-cert-cache-entries']['ssl-proxy-cert-cache-entries-pic']

    if not isinstance(status, list):
        status = [status]

    if fpc is not None:
        flag = 0
        for x in status:
            if isinstance(x, dict):
                current_pic = x['ssl-proxy-cert-cache-entries-pic-info']
                if re.match(r".*fpc\[" + fpc + r"\].*pic\[" + pic + r"\].*", current_pic, re.DOTALL):
                    flag = 1
                    break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")


        dict_to_return['cert-cache-entry'] = x['ssl-proxy-cert-cache-entry']
        dict_to_return['cert-cache-serial-number'] = x['ssl-proxy-cert-cache-serial-number']
        dict_to_return['cert-cache-init-profile-id'] = x['ssl-proxy-cert-cache-init-profile-id']
        dict_to_return['cert-cache-num-of-crl-update'] = x['ssl-proxy-cert-cache-num-of-crl-update']

        return dict_to_return

    for x in status:
        dict_to_return['cert-cache-entry'] = x['ssl-proxy-cert-cache-entry']
        dict_to_return['cert-cache-serial-number'] = x['ssl-proxy-cert-cache-serial-number']
        dict_to_return['cert-cache-init-profile-id'] = x['ssl-proxy-cert-cache-init-profile-id']
        dict_to_return['cert-cache-num-of-crl-update'] = x['ssl-proxy-cert-cache-num-of-crl-update']

        return dict_to_return



def get_ssl_sess_cache_entries(device=None, lsys=None, tenant=None, node="local", fpc=None, pic=None):
    """
    To get SSL Session cache entries detail. In case of Multi PIC, a consolidated result is returned.
    If you want a per PIC result, pass 'fpc' and 'pic'.

    Example :
        get_ssl_sess_cache_entries(device=dut, fpc="1", pic="2")
        get_ssl_sess_cache_entries(device=dut)

    ROBOT Example :
        Get SSL Sess cache entries   device=${dut}  fpc=1  pic=2
        Get SSL Sess cache entries   device=${dut}


    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :return: Dictionary of stats as key value pairs.
    :rtype: dict

    Example Returned dictionary :

    {'sess-cache-hash-entry':'1',
    'sess-cache-status':'Already Expired',
    'sess-cache-sess-id-len':'32',
    'sess-cache-sess-id':'1e 2d e0 0b 92 ce f7 a6 00 bb 94 f4 ee 33 2e 44 7f 3e 9f 51 8f c9 fd 25 70 31 1f 83 7f 64 0d f4',
    'sess-cache-dest-ip':'5.0.0.1',
    'sess-cache-dest-port':'47873',
    'sess-cache-term-profile-id':'134',
    'sess-cache-init-profile-id':'161',
    'sess-cache-interdicted-cert-type':'[0x1]: CA issued, Authentication Successful',
    'sess-cache-server-cert-verification-result':'ok [0x0]',
    'sess-cache-server-name-extn-len':'0',
    'sess-cache-server-name-extn-name':'None',
    'sess-cache-server-cert-chain-hash':'63 c2 af c4 2b e5 42 42 60 ff 01 3e da d2 bc 94',
    'sess-cache-term-ssl-version':'0x303',
    'sess-cache-term-compression-method':'0',
    'sess-cache-term-cipher-id':'0x300009c',
    'sess-cache-term-master-key-len':'48',
    'sess-cache-init-ssl-version':'0x303',
    'sess-cache-init-compression-method':'0',
    'sess-cache-init-cipher-id':'0x300009c',
    'sess-cache-init-master-key-len':'48'}

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    dict_to_return = {}

    cmd = "show services ssl proxy session-cache entries detail"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-proxy-sess-cache-entries']['ssl-proxy-sess-cache-entries']['ssl-proxy-sess-cache-entries-pic']

    if not isinstance(status, list):
        status = [status]

    if fpc is not None:
        flag = 0
        for x in status:
            if isinstance(x, dict):
                current_pic = x['ssl-proxy-sess-cache-entries-pic-info']
                if re.match(r".*fpc\[" + fpc + r"\].*pic\[" + pic + r"\].*", current_pic, re.DOTALL):
                    flag = 1
                    break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")

        dict_to_return['sess-cache-hash-entry'] = x['ssl-proxy-sess-cache-hash-entry']
        dict_to_return['sess-cache-status'] = x['ssl-proxy-sess-cache-status']
        dict_to_return['sess-cache-sess-id-len'] = x['ssl-proxy-sess-cache-sess-id-len']
        dict_to_return['sess-cache-sess-id'] = x['ssl-proxy-sess-cache-sess-id']
        dict_to_return['sess-cache-dest-ip'] = x['ssl-proxy-sess-cache-dest-ip']
        dict_to_return['sess-cache-dest-port'] = x['ssl-proxy-sess-cache-dest-port']
        dict_to_return['sess-cache-term-profile-id'] = x['ssl-proxy-sess-cache-term-profile-id']
        dict_to_return['sess-cache-init-profile-id'] = x['ssl-proxy-sess-cache-init-profile-id']
        dict_to_return['sess-cache-interdicted-cert-type'] = x['ssl-proxy-sess-cache-interdicted-cert-type']
        dict_to_return['sess-cache-server-cert-verification-result'] = x['ssl-proxy-sess-cache-server-cert-verification-result']
        dict_to_return['sess-cache-server-name-extn-len'] = x['ssl-proxy-sess-cache-server-name-extn-len']
        dict_to_return['sess-cache-server-name-extn-name'] = x['ssl-proxy-sess-cache-server-name-extn-name']
        dict_to_return['sess-cache-server-cert-chain-hash'] = x['ssl-proxy-sess-cache-server-cert-chain-hash']
        dict_to_return['sess-cache-term-ssl-version'] = x['ssl-proxy-sess-cache-term-ssl-version']
        dict_to_return['sess-cache-term-compression-method'] = x['ssl-proxy-sess-cache-term-compression-method']
        dict_to_return['sess-cache-term-cipher-id'] = x['ssl-proxy-sess-cache-term-cipher-id']
        dict_to_return['sess-cache-term-master-key-len'] = x['ssl-proxy-sess-cache-term-master-key-len']
        dict_to_return['sess-cache-init-ssl-version'] = x['ssl-proxy-sess-cache-init-ssl-version']
        dict_to_return['sess-cache-init-compression-method'] = x['ssl-proxy-sess-cache-init-compression-method']
        dict_to_return['sess-cache-init-cipher-id'] = x['ssl-proxy-sess-cache-init-cipher-id']
        dict_to_return['sess-cache-init-master-key-len'] = x['ssl-proxy-sess-cache-init-master-key-len']

        return dict_to_return

    for x in status:
        dict_to_return['sess-cache-hash-entry'] = x['ssl-proxy-sess-cache-hash-entry']
        dict_to_return['sess-cache-status'] = x['ssl-proxy-sess-cache-status']
        dict_to_return['sess-cache-sess-id-len'] = x['ssl-proxy-sess-cache-sess-id-len']
        dict_to_return['sess-cache-sess-id'] = x['ssl-proxy-sess-cache-sess-id']
        dict_to_return['sess-cache-dest-ip'] = x['ssl-proxy-sess-cache-dest-ip']
        dict_to_return['sess-cache-dest-port'] = x['ssl-proxy-sess-cache-dest-port']
        dict_to_return['sess-cache-term-profile-id'] = x['ssl-proxy-sess-cache-term-profile-id']
        dict_to_return['sess-cache-init-profile-id'] = x['ssl-proxy-sess-cache-init-profile-id']
        dict_to_return['sess-cache-interdicted-cert-type'] = x['ssl-proxy-sess-cache-interdicted-cert-type']
        dict_to_return['sess-cache-server-cert-verification-result'] = x['ssl-proxy-sess-cache-server-cert-verification-result']
        dict_to_return['sess-cache-server-name-extn-len'] = x['ssl-proxy-sess-cache-server-name-extn-len']
        dict_to_return['sess-cache-server-name-extn-name'] = x['ssl-proxy-sess-cache-server-name-extn-name']
        dict_to_return['sess-cache-server-cert-chain-hash'] = x['ssl-proxy-sess-cache-server-cert-chain-hash']
        dict_to_return['sess-cache-term-ssl-version'] = x['ssl-proxy-sess-cache-term-ssl-version']
        dict_to_return['sess-cache-term-compression-method'] = x['ssl-proxy-sess-cache-term-compression-method']
        dict_to_return['sess-cache-term-cipher-id'] = x['ssl-proxy-sess-cache-term-cipher-id']
        dict_to_return['sess-cache-term-master-key-len'] = x['ssl-proxy-sess-cache-term-master-key-len']
        dict_to_return['sess-cache-init-ssl-version'] = x['ssl-proxy-sess-cache-init-ssl-version']
        dict_to_return['sess-cache-init-compression-method'] = x['ssl-proxy-sess-cache-init-compression-method']
        dict_to_return['sess-cache-init-cipher-id'] = x['ssl-proxy-sess-cache-init-cipher-id']
        dict_to_return['sess-cache-init-master-key-len'] = x['ssl-proxy-sess-cache-init-master-key-len']

        return dict_to_return


def get_ssl_sess_cache_entries_summary(device=None, lsys=None, tenant=None, node="local", fpc=None, pic=None):
    """
    To get SSL Session cache entries summary. In case of Multi PIC, a consolidated result is returned.
    If you want a per PIC result, pass 'fpc' and 'pic'.

    Example :
        get_ssl_sess_cache_entries_summary(device=dut, fpc="1", pic="2")
        get_ssl_sess_cache_entries_summary(device=dut)

    ROBOT Example :
        Get SSL Sess cache entries summary  device=${dut}  fpc=1  pic=2
        Get SSL Sess cache entries summary  device=${dut}


    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :return: Dictionary of stats as key value pairs.
    :rtype: dict

    Example Returned dictionary :

    {'sess-cache-hash-entry':'1',
    'sess-cache-status':'Already Expired',
    'sess-cache-sess-id-len':'32',
    'sess-cache-sess-id':'1e 2d e0 0b 92 ce f7 a6 00 bb 94 f4 ee 33 2e 44 7f 3e 9f 51 8f c9 fd 25 70 31 1f 83 7f 64 0d f4',
    'sess-cache-dest-ip':'5.0.0.1',
    'sess-cache-dest-port':'47873',
    'sess-cache-term-profile-id':'134',
    'sess-cache-init-profile-id':'161'}

    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    dict_to_return = {}

    cmd = "show services ssl proxy session-cache entries summary"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-proxy-sess-cache-entries']['ssl-proxy-sess-cache-entries']['ssl-proxy-sess-cache-entries-pic']

    if not isinstance(status, list):
        status = [status]

    if fpc is not None:
        flag = 0
        for index in status:
            if isinstance(index, dict):
                current_pic = index['ssl-proxy-sess-cache-entries-pic-info']
                if re.match(r".*fpc\[" + fpc + r"\].*pic\[" + pic + r"\].*", current_pic, re.DOTALL):
                    flag = 1
                    break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")

        dict_to_return['sess-cache-hash-entry'] = index['ssl-proxy-sess-cache-hash-entry']
        dict_to_return['sess-cache-status'] = index['ssl-proxy-sess-cache-status']
        dict_to_return['sess-cache-sess-id-len'] = index['ssl-proxy-sess-cache-sess-id-len']
        dict_to_return['sess-cache-sess-id'] = index['ssl-proxy-sess-cache-sess-id']
        dict_to_return['sess-cache-dest-ip'] = index['ssl-proxy-sess-cache-dest-ip']
        dict_to_return['sess-cache-dest-port'] = index['ssl-proxy-sess-cache-dest-port']
        dict_to_return['sess-cache-term-profile-id'] = index['ssl-proxy-sess-cache-term-profile-id']
        dict_to_return['sess-cache-init-profile-id'] = index['ssl-proxy-sess-cache-init-profile-id']

        return dict_to_return

    for index in status:
        dict_to_return['sess-cache-hash-entry'] = index['ssl-proxy-sess-cache-hash-entry']
        dict_to_return['sess-cache-status'] = index['ssl-proxy-sess-cache-status']
        dict_to_return['sess-cache-sess-id-len'] = index['ssl-proxy-sess-cache-sess-id-len']
        dict_to_return['sess-cache-sess-id'] = index['ssl-proxy-sess-cache-sess-id']
        dict_to_return['sess-cache-dest-ip'] = index['ssl-proxy-sess-cache-dest-ip']
        dict_to_return['sess-cache-dest-port'] = index['ssl-proxy-sess-cache-dest-port']
        dict_to_return['sess-cache-term-profile-id'] = index['ssl-proxy-sess-cache-term-profile-id']
        dict_to_return['sess-cache-init-profile-id'] = index['ssl-proxy-sess-cache-init-profile-id']

        return dict_to_return



def get_ssl_initiator_counters(device=None, lsys=None, tenant=None, what_counters="all",
                               fpc=None, pic=None, node="local"):
    """
    Returns A dictionary of SSL initiator counters. Will return a consolidated counter sum from
    all PICs on the device, if no specific 'fpc' - 'pic' value.

    Example :
        get_ssl_initiator_counters(device=dut)

    ROBOT Example :
        Get SSL Initiator Counters   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
               or 'tenant'. NOT both
    :param str what_counters:
        *OPTIONAL* Supported values are : 'all', 'errors', 'info', 'handshake', 'memory'
                   Default value is : 'all'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: dictionary of counters, with key as counter name(str) and value as the counter value(int)
    :rtype: dict
    """


    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    cmd = "show services ssl initiation counters " + what_counters
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    return _get_counters(device=device, cmd=cmd, fpc=fpc, pic=pic, node=node)


def get_ssl_terminator_counters(device=None, lsys=None, tenant=None, what_counters="all", \
                                fpc=None, pic=None, node="local"):
    """
    Returns A dictionary of SSL Terminator counters. Will return a consolidated counter sum from
    all PICs on the device, if no specific 'fpc' - 'pic' value.

    Example :
        get_ssl_terminator_counters(device=dut)

    ROBOT Example :
        Get SSL Terminator Counters   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
               or 'tenant'. NOT both
    :param str what_counters:
        *OPTIONAL* Supported values are : 'all', 'errors', 'info', 'handshake', 'memory'
                   Default value is : 'all'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: dictionary of counters, with key as counter name(str) and value as the counter value(int)
    :rtype: dict
    """


    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    cmd = "show services ssl termination counters " + what_counters
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    return _get_counters(device=device, cmd=cmd, fpc=fpc, pic=pic, node=node)


def get_ssl_proxy_counters(device=None, lsys=None, tenant=None, what_counters="all", \
                           fpc=None, pic=None, node="local"):
    """
    Returns A dictionary of SSL Proxy counters. Will return a consolidated counter sum from
    all PICs on the device, if no specific 'fpc' - 'pic' value.

    Example :
        get_ssl_proxy_counters(device=dut)

    ROBOT Example :
        Get SSL Proxy Counters   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str tenant:
        *OPTIONAL* Name of the tenant whose output you're looking for. Either define 'lsys'
               or 'tenant'. NOT both
    :param str what_counters:
        *OPTIONAL* Supported values are : 'all', 'errors', 'info'
                   Default value is : 'all'
    :param str fpc:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :param str pic:
        *OPTIONAL* PIC value if per PIC outut is needed. With 'pic', 'fpc' is also mandatory
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: dictionary of counters, with key as counter name(str) and value as the counter value(int)
    :rtype: dict
    """


    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if lsys is not None and tenant is not None:
        device.log(level="INFO", message="Both'tenant' and 'lsys' should not be passed together")
        raise ValueError("Both'tenant' and 'lsys' should not be passed together")

    if (fpc is None and pic is not None) or (pic is None and fpc is not None):
        device.log(level="INFO", message="Either both or none should be given as arguments : 'fpc' and 'pic'")
        raise ValueError("Either both or none should be given as arguments : 'fpc' and 'pic'")

    cmd = "show services ssl proxy counters " + what_counters
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys
    if tenant is not None:
        cmd = cmd + " tenant " + tenant

    return _get_counters(device=device, cmd=cmd, fpc=fpc, pic=pic, node=node)


def _get_counters(device, node, cmd, fpc, pic):
    """

    :param device:
    :param node:
    :param cmd:
    :param fpc:
    :param pic:
    :return:
    """
    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-counters']['ssl-counters']['ssl-counters-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 0

    dict_to_return = {}

    # in case of specified fpc/pic value
    if fpc is not None:
        for x in status:
            current_pic = x['ssl-counters-pic-info']
            if re.match(r".*fpc\[" + fpc + r"\].*pic\[" + pic + r"\].*", current_pic, re.DOTALL):
                flag = 1
                break

        if flag == 0:
            device.log(level="INFO", message="Invalid FPC-PIC value, Keyword failing")
            raise ValueError("Invalid FPC-PIC value, Keyword failing")

        for a, b in zip(x['ssl-counters-name'], x['ssl-counters-value']):
            dict_to_return[str(a)] = int(b)

        return dict_to_return

    #Intialising with 0 for consolidated result
    for x in status:
        for y in x['ssl-counters-name']:
            dict_to_return[str(y)] = 0
        break

    for x in status:
        for a, b in zip(x['ssl-counters-name'], x['ssl-counters-value']):
            dict_to_return[str(a)] = dict_to_return[a] + int(b)

    return dict_to_return

def is_datetime_between(begin_time, end_time, check_time, check_date, ref_date):
    """
    date and time checker
    """
    begin_time = begin_time.split(':')
    hours = int(begin_time[0])
    mins = int(begin_time[1])
    secs = int(begin_time[2])
    begin_time = time(hours, mins, secs)
    end_time = end_time.split(':')
    hours = int(end_time[0])
    mins = int(end_time[1])
    secs = int(end_time[2])
    end_time = time(hours, mins, secs)
    time_result = False
    date_result = False
    check_time = check_time.split(':')
    hours = int(check_time[0])
    mins = int(check_time[1])
    secs = int(check_time[2])
    check_time = time(hours, mins, secs)
    check_date = check_date.split('/')
    month1 = int(check_date[0])
    day1 = int(check_date[1])
    year1 = int(check_date[2])
    ref_date = ref_date.split('/')
    month2 = int(ref_date[0])
    day2 = int(ref_date[1])
    year2 = int(ref_date[2])
    if begin_time < end_time:
        time_result = check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        time_result = check_time >= begin_time or check_time <= end_time
    date_result = (-timedelta(days=1) <= (date(year1, month1, day1) - date(year2, month2, day2)) <= timedelta(days=1))
    if time_result is True and date_result is True:
        return True
    else:
        return False

def convert_datetime_timezone(date1, timezone1, timezone2):
    """
    TimeZone coversion method
    """
    timezone1 = timezone(timezone1)
    timezone2 = timezone(timezone2)

    date1 = datetime.datetime.strptime(date1, "%m-%d-%Y %H:%M")
    date1 = timezone1.localize(date1)
    date1 = date1.astimezone(timezone2)
    date1 = date1.strftime("%a %m/%d/%Y %I:%M %p")
    return date1

def get_ssl_session_details(device=None, sessionid=None, node="local", fpcpic=None):
    """
    Returns the SSL proxy status as Dictionary. In Multi PIC, if no fpc/pic value is provided,
    status of the 1st PIC is returned. Otherwise the specific fpc/pic value needs to be mentioned.

    Example:
        get_ssl_proxy_status(device=dut)
        get_ssl_proxy_status(device=dut, fpcpic=fpc1.pic2)

    ROBOT Example:
        Get ssl proxy status   device=${dut}
        Get ssl proxy status   device=${dut}    fpcpic=fpc1.pic2

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :param str fpcpic:
        *OPTIONAL* FPC value if per PIC output is needed. With 'fpc', 'pic' is also mandatory
    :return: returns SSL proxy status as dictionary
    :rtype: dict


    Example Returned Dictionary :
    {'ssl-session-async-crypto': 'Disabled',
     'ssl-session-cert': '/C=--/ST=SomeState/L=SomeCity/O=SomeOrganization/OU=SomeOrganizationalUnit/CN=localhost.localdomain/emailAddress=root@localhost.localdomIgnore '
                     'Server Authentication failure',
    'ssl-session-cert-action': 'Ignore Server Authentication failure',
    'ssl-session-cert-crl-check': 'Not configured',
    'ssl-session-cert-status': 'Failed',
    'ssl-session-connection-type': 'PROXY',
    'ssl-session-init-cipher': 'ECDHE-RSA-AES256-GCM-SHA384',
    'ssl-session-init-key-size': '2048',
    'ssl-session-init-tls-version': '1.2',
    'ssl-session-lsys-name': 'root-logical-system',
    'ssl-session-one-crypto': 'Disabled',
    'ssl-session-pic-info': 'spu-5 fpc[1] pic[1]',
    'ssl-session-reneg-count': '0',
    'ssl-session-resumed-session': 'No',
    'ssl-session-session-id': '6',
    'ssl-session-ssl-profile': 'root_profile',
    'ssl-session-term-cipher': 'ECDHE-RSA-AES256-GCM-SHA384',
    'ssl-session-term-key-size': '2048',
    'ssl-session-term-tls-version': '1.2'}
    """
    if (device is None) or (sessionid is None):
        raise ValueError("'device' and 'sessionid' are  mandatory arguments")

    cmd = "show services ssl session " + str(sessionid)
    if fpcpic is not None:
        cmd = cmd + ' pic-info ' + fpcpic
    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-session']['ssl-session']
    return status

def get_brief_term_profile(device=None, lsys=None, node="local", profile=None):
    """
    Returns the details of the SSL Profile required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_brief_term_profile(device=dut, profile="p1")

    ROBOT Example:
        Get Brief Term Profile   device=${dut}   profile=p1

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str profile:
        **REQUIRED** Profile name whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dictionary with details of Profile as key value pairs
    :rtype: dict

    Example Returned Dictionary :

    {'ssl-term-profile-detail-allow-non-ssl-sess': 'true',
     'ssl-term-profile-detail-nof-url-categories-conf': '0',
     'ssl-term-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
     'ssl-term-profile-detail-preferred-ciphers': 'medium',
     'ssl-term-profile-detail-profile': 'root_profile_65536_proxy_t'}
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if profile is None:
        device.log(level="ERROR", message="'profile' is a mandatory argument")
        raise ValueError("'profile' is a mandatory argument")

    cmd = "show services ssl termination profile brief profile-name " + profile
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-term-profile-detail']['ssl-term-profile-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given Profile name is not configured on DUT")
        raise ValueError("Given Profile name is not configured on DUT")

    status = status['ssl-term-profile-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for index1 in status:
        for index2 in status:
            if index1['ssl-term-profile-detail-allow-non-ssl-sess'] != index2['ssl-term-profile-detail-allow-non-ssl-sess']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-preferred-ciphers'] != index2['ssl-term-profile-detail-preferred-ciphers']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-profile'] != index2['ssl-term-profile-detail-profile']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-nof-url-categories-conf'] != index2['ssl-term-profile-detail-nof-url-categories-conf']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return index1

def get_detail_term_profile(device=None, lsys=None, node="local", profile=None):
    """
    Returns the details of the SSL Profile required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_detail_term_profile(device=dut, profile="p1")

    ROBOT Example:
        Get Detail Term Profile   device=${dut}   profile=p1

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str profile:
        **REQUIRED** Profile name whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dictionary with details of Profile as key value pairs
    :rtype: dict

    Example Returned Dictionary :

    {'ssl-term-profile-detail-allow-non-ssl-sess': 'true',
     'ssl-term-profile-detail-nof-url-categories-conf': '0',
     'ssl-term-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
     'ssl-term-profile-detail-preferred-ciphers': 'medium',
     'ssl-term-profile-detail-profile': 'root_profile_65536_proxy_t'}
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if profile is None:
        device.log(level="ERROR", message="'profile' is a mandatory argument")
        raise ValueError("'profile' is a mandatory argument")

    cmd = "show services ssl termination profile detail profile-name " + profile
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-term-profile-detail']['ssl-term-profile-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given Profile name is not configured on DUT")
        raise ValueError("Given Profile name is not configured on DUT")

    status = status['ssl-term-profile-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for index1 in status:
        for index2 in status:
            if index1['ssl-term-profile-detail-allow-non-ssl-sess'] != index2['ssl-term-profile-detail-allow-non-ssl-sess']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-preferred-ciphers'] != index2['ssl-term-profile-detail-preferred-ciphers']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-profile'] != index2['ssl-term-profile-detail-profile']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-nof-url-categories-conf'] != index2['ssl-term-profile-detail-nof-url-categories-conf']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-protocol-version'] != index2['ssl-term-profile-detail-protocol-version']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-client-auth'] != index2['ssl-term-profile-detail-client-auth']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-server-auth'] != index2['ssl-term-profile-detail-server-auth']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-crypto-mode'] != index2['ssl-term-profile-detail-crypto-mode']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-sess-resumption'] != index2['ssl-term-profile-detail-sess-resumption']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-crl-check'] != index2['ssl-term-profile-detail-crl-check']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-cert-rsa'] != index2['ssl-term-profile-detail-cert-rsa']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-renegotiation'] != index2['ssl-term-profile-detail-renegotiation']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-custom-ciphers'] != index2['ssl-term-profile-detail-custom-ciphers']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-server-cert'] != index2['ssl-term-profile-detail-server-cert']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-decrypt-mirror'] != index2['ssl-term-profile-detail-decrypt-mirror']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-trusted-ca'] != index2['ssl-term-profile-detail-trusted-ca']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return index1

def get_all_term_profile(device=None, lsys=None, node="local"):
    """
    Returns the all the Profile names with profile IDs. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_all_term_profile(device=dut)

    ROBOT Example:
        GET all Term Profile   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dict with profile IDs as values and profile name as keys
    :rtype: dict

    Example Returned dictionary :

    {'p1': '10',
     'p3': '11'}
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    cmd = "show services ssl termination profile all"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-profile-list']
    if not isinstance(status, dict):
        device.log(level="INFO", message="No SSL Term Profiles present. Returning Empty list")
        return []

    status = status['ssl-profile-list-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # With this for loop, checking the values across PICS are same
    for index1 in status:
        for index2 in status:
            if isinstance(index1['ssl-profile-id'], list):
                if len(index1['ssl-profile-id']) != len(index2['ssl-profile-id']):
                    flag = 0
                    break
                if len(index1['ssl-profile-name']) != len(index2['ssl-profile-name']):
                    flag = 0
                    break
                for index3 in index2['ssl-profile-id']:
                    if index3 not in index1['ssl-profile-id']:
                        flag = 0
                        break
                for index3 in index2['ssl-profile-name']:
                    if index3 not in index1['ssl-profile-name']:
                        flag = 0
                        break
            else:
                if index1['ssl-profile-id'] != index2['ssl-profile-id']:
                    flag = 0
                    break
                if index1['ssl-profile-name'] != index2['ssl-profile-name']:
                    flag = 0
                    break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    dict_to_return = {}

    if not isinstance(index1['ssl-profile-id'], list):
        dict_to_return[str(index1['ssl-profile-name'])] = str(index1['ssl-profile-id'])

    else:
        for val1, val2 in zip(index1['ssl-profile-name'], index2['ssl-profile-id']):
            dict_to_return[str(val1)] = str(val2)

    return(dict_to_return)

def get_brief_init_profile(device=None, lsys=None, node="local", profile=None):
    """
    Returns the details of the SSL Profile required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_brief_init_profile(device=dut, profile="p1")

    ROBOT Example:
        Get Brief Init Profile   device=${dut}   profile=p1

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str profile:
        **REQUIRED** Profile name whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dictionary with details of Profile as key value pairs
    :rtype: dict

    Example Returned Dictionary :

    {'ssl-term-profile-detail-allow-non-ssl-sess': 'true',
     'ssl-term-profile-detail-nof-url-categories-conf': '0',
     'ssl-term-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
     'ssl-term-profile-detail-preferred-ciphers': 'medium',
     'ssl-term-profile-detail-profile': 'root_profile_65536_proxy_t'}
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if profile is None:
        device.log(level="ERROR", message="'profile' is a mandatory argument")
        raise ValueError("'profile' is a mandatory argument")

    cmd = "show services ssl initiation profile brief profile-name " + profile
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-term-profile-detail']['ssl-term-profile-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given Profile name is not configured on DUT")
        raise ValueError("Given Profile name is not configured on DUT")

    status = status['ssl-term-profile-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for index1 in status:
        for index2 in status:
            if index1['ssl-term-profile-detail-allow-non-ssl-sess'] != index2['ssl-term-profile-detail-allow-non-ssl-sess']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-preferred-ciphers'] != index2['ssl-term-profile-detail-preferred-ciphers']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-profile'] != index2['ssl-term-profile-detail-profile']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-nof-url-categories-conf'] != index2['ssl-term-profile-detail-nof-url-categories-conf']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return index1

def get_all_init_profile(device=None, lsys=None, node="local"):
    """
    Returns the all the Profile names with profile IDs. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_all_term_profile(device=dut)

    ROBOT Example:
        GET all Term Profile   device=${dut}

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dict with profile IDs as values and profile name as keys
    :rtype: dict

    Example Returned dictionary :

    {'p1': '10',
     'p3': '11'}
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    cmd = "show services ssl initiation profile all"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys

    status = device.execute_as_rpc_command(command=cmd, node=node)

    status = status['ssl-profile-list']
    if not isinstance(status, dict):
        device.log(level="INFO", message="No SSL Term Profiles present. Returning Empty list")
        return []

    status = status['ssl-profile-list-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # With this for loop, checking the values across PICS are same
    for index1 in status:
        for index2 in status:
            if isinstance(index1['ssl-profile-id'], list):
                if len(index1['ssl-profile-id']) != len(index2['ssl-profile-id']):
                    flag = 0
                    break
                if len(index1['ssl-profile-name']) != len(index2['ssl-profile-name']):
                    flag = 0
                    break
                for index3 in index2['ssl-profile-id']:
                    if index3 not in index1['ssl-profile-id']:
                        flag = 0
                        break
                for index3 in index2['ssl-profile-name']:
                    if index3 not in index1['ssl-profile-name']:
                        flag = 0
                        break
            else:
                if index1['ssl-profile-id'] != index2['ssl-profile-id']:
                    flag = 0
                    break
                if index1['ssl-profile-name'] != index2['ssl-profile-name']:
                    flag = 0
                    break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    dict_to_return = {}

    if not isinstance(index1['ssl-profile-id'], list):
        dict_to_return[str(index1['ssl-profile-name'])] = str(index1['ssl-profile-id'])

    else:
        for val1, val2 in zip(index1['ssl-profile-name'], index2['ssl-profile-id']):
            dict_to_return[str(val1)] = str(val2)

    return(dict_to_return)


def get_detail_init_profile(device=None, lsys=None, node="local", profile=None):
    """
    Returns the details of the SSL Profile required. In case of Multi PIC, it will return the values
    from 1st PIC and check for values to be same across PICs

    Example:
        get_detail_term_profile(device=dut, profile="p1")

    ROBOT Example:
        Get Detail Term Profile   device=${dut}   profile=p1

    :param str device:
        **REQUIRED** Device handle of the DUT
    :param str profile:
        **REQUIRED** Profile name whose details are required
    :param str lsys:
        *OPTIONAL* Name of the logical system whose output you're looking for. Either define 'lsys'
                   or 'tenant'. NOT both
    :param str node:
        *OPTIONAL* To be defined in case of HA. Default value is 'local'
    :return: Dictionary with details of Profile as key value pairs
    :rtype: dict

    Example Returned Dictionary :

    {'ssl-term-profile-detail-allow-non-ssl-sess': 'true',
     'ssl-term-profile-detail-nof-url-categories-conf': '0',
     'ssl-term-profile-detail-pic-info': 'spu-5 fpc[1] pic[1]',
     'ssl-term-profile-detail-preferred-ciphers': 'medium',
     'ssl-term-profile-detail-profile': 'root_profile_65536_proxy_t'}
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if profile is None:
        device.log(level="ERROR", message="'profile' is a mandatory argument")
        raise ValueError("'profile' is a mandatory argument")

    cmd = "show services ssl initiation profile detail profile-name " + profile
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys

    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['ssl-term-profile-detail']['ssl-term-profile-detail']
    if not isinstance(status, dict):
        device.log(level="ERROR", message="Given Profile name is not configured on DUT")
        raise ValueError("Given Profile name is not configured on DUT")

    status = status['ssl-term-profile-detail-pic']

    if not isinstance(status, list):
        status = [status]

    flag = 1

    # checking all PICs have same values in Multi PIC devices, checking through flag
    for index1 in status:
        for index2 in status:
            if index1['ssl-term-profile-detail-allow-non-ssl-sess'] != index2['ssl-term-profile-detail-allow-non-ssl-sess']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-preferred-ciphers'] != index2['ssl-term-profile-detail-preferred-ciphers']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-profile'] != index2['ssl-term-profile-detail-profile']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-nof-url-categories-conf'] != index2['ssl-term-profile-detail-nof-url-categories-conf']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-protocol-version'] != index2['ssl-term-profile-detail-protocol-version']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-client-auth'] != index2['ssl-term-profile-detail-client-auth']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-server-auth'] != index2['ssl-term-profile-detail-server-auth']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-crypto-mode'] != index2['ssl-term-profile-detail-crypto-mode']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-sess-resumption'] != index2['ssl-term-profile-detail-sess-resumption']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-crl-check'] != index2['ssl-term-profile-detail-crl-check']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-cert-rsa'] != index2['ssl-term-profile-detail-cert-rsa']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-renegotiation'] != index2['ssl-term-profile-detail-renegotiation']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-custom-ciphers'] != index2['ssl-term-profile-detail-custom-ciphers']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-server-cert'] != index2['ssl-term-profile-detail-server-cert']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-decrypt-mirror'] != index2['ssl-term-profile-detail-decrypt-mirror']:
                flag = 0
                break
            if index1['ssl-term-profile-detail-trusted-ca'] != index2['ssl-term-profile-detail-trusted-ca']:
                flag = 0
                break
        break

    if flag == 0:
        device.log(level="INFO", message="Mismatch in values across PICs")
        raise ValueError("Mismatch in values across PICs")

    return index1

