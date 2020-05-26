"""
AppID Operational commands

AUTHOR:  Elango K / Ishan Arora
VERSION:  1.0
"""

import re
import time
import jxmlease 
from jnpr.toby.security.appsecure.appid_config import configure_appid_sig_package
from jnpr.toby.utils.iputils import normalize_ipv6

def get_appid_sig_package_version(device=None, node="local"):
    """
    Get the AppID signature package details installed on the RE
    Example :-
        get_appid_signature_package_version(device=dh)
    Robot Example :-
        get appid signature package version  device=${dh}  node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the version of the appid signature package
    :rtype: str
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    cmd = 'show services application-identification version'
    status = device.execute_as_rpc_command(command=cmd, node=node)
    version = status['appid-package-version']['version-detail']
    return version


def check_app_sig_installed(device=None, node="local"):
    """
    Check application signature installed on the device
    Example :-
        check_app_sig_installed(device=dh)
    Robot Example :-
        check app sig installed  device=${dh}  node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns True if application signature installed.
    :rtype: bool
    """
    version = get_appid_sig_package_version(device, node)
    if version == "0":
        device.log(level="ERROR", message="Application signature package is not installed")
        raise Exception("Application signature package is not installed")
    else:
        device.log(level="INFO", message="Device has application signature package " + version)
    return True


def download_appid_sig_package(device=None, update_type="signature", validate=True, **kwargs):
    """
    To download the idp security package
    Example :-
        download_appid_sig_package(device=dh)
        download_appid_sig_package(device=dh,
                                    url="https://devdb.juniper.net/cgi-bin/index.cgi", version=3000)
        download_appid_sig_package(device=dh, timeout=300)
        download_appid_sig_package(device=dh, type="check")
    Robot Example :-
        download appid sig package  device=${dh}
        download appid sig package  device=${dh}  version=${3000}
                                            url=https://devdb.juniper.net/cgi-bin/index.cgi
        download appid sig package  device=${dh}  timeout=${300}
        download appid sig package  device=${dh}  type=check
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str update_type:
        *OPTIONAL* Download options to perform.
        ``Supported Values``: check or signature
        ``Default Value``   : signature
    :param str url:
        *OPTIONAL* Sigdb URL to configure and do download. Default is live sigdb (not configured)
    :param int version:
        *OPTIONAL* The application signature package version to download.
        Default latest signature package will be downloaded
    :param int timeout:
        *OPTIONAL* Time out for the signature download.
        ``Default value`` : 600 seconds
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the signature update. Validates by default
    :param bool ignore_server_validation:
        *OPTIONAL* Pass True if want to ignore server validation while downloading
    :return: Returns the dict object with status of the sub modules. The return includes values of
            check : version/url/protobundle/date/status/message
            download : version/status/message
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    url = kwargs.get('url', "")
    timeout = kwargs.get('timeout', 600)
    version = kwargs.get('version', "")
    ignore_server_validation = kwargs.get('ignore_server_validation', False)

    base_cmd = " request services application-identification download "
    # Configure the sigdb url
    configure_appid_sig_package(device=device, url=url, commit=True,
                                ignore_server_validation=ignore_server_validation)
    values = {}
    if update_type == "check":
        response = device.execute_as_rpc_command(command=base_cmd + "check-server",node=None)
        status_msg = response["apppack-server-status"]["apppack-server-status-detail"]
        values['message'] = str(status_msg)
        if re.match(r'^error*', status_msg):
            values['status'] = "error"
        elif re.match('Download server URL*', status_msg):
            match = re.search(
                r"URL:\s+([a-z0-9:/.-]+).*Sigpack\s+Version:\s+([0-9]+).*Protobundle\s"
                r"version:\s+([a-z0-9.-]+).*Time.*\s+([A-Za-z]+[0-9: ]+)", status_msg, re.DOTALL)
            values['url'] = match.group(1)
            values['version'] = match.group(2)
            values['protobundle'] = match.group(3)
            values['date'] = match.group(4)
            values['status'] = "success"
        else:
            values['status'] = "error"
        if values['status'] == 'error':
            if validate is True:
                device.log(level="ERROR", message="Check server is failed")
                device.log(level="ERROR", message=values['message'])
                raise Exception("Check server is failed. Message - " + values['message'])
            else:
                device.log(level="INFO", message="Check server is failed")
                device.log(level="INFO", message=values['message'])
        else:
            device.log(level="INFO", message="Check server successful")
            device.log(level="INFO", message=values['message'])
        return values
    elif update_type == "signature":
        download_option = ""
        if version != "":
            download_option = "version " + str(version)
        download_resp = device.cli(command=base_cmd + download_option).response()
        if re.search(r"Error", download_resp, re.IGNORECASE):
            values['status'] = "error"
            values['message'] = download_resp
            if validate is True:
                device.log(level='ERROR', message="Application Signature download failed : %s" %
                                                  download_resp)
                raise Exception ("Application Signature download failed : %s" % download_resp)
            else:
                device.log(level='INFO', message="Application Signature download failed : %s" % \
                                download_resp)
            return values

    else:
        values['status'] = "error"
        raise ValueError("Incorrect value for AppID signature package download update_type")

    # Wait till the signature download completes and get the status message
    status_rpc_str = device.get_rpc_equivalent(command=base_cmd + 'status')
    sleep_time = 0
    while sleep_time < timeout:
        response = device.execute_as_rpc_command(command=status_rpc_str, command_type="rpc",node=None)
        status_msg = response["apppack-download-status"]["apppack-download-status-detail"]
        values['message'] = str(status_msg)
        if re.search(r"succeeded", status_msg):
            values['status'] = "success"
            match = re.search(r"package\s+([0-9]+)\s+succeeded", status_msg)
            values['version'] = match.group(1)
            break
        elif re.search(r"failed", status_msg):
            values['status'] = "error"
            break
        elif re.search(r'Downloading|Fetching', status_msg):
            device.log(level="INFO", message="(%d/%d secs) Sleeping 30 seconds..." %(sleep_time,
                                                                                     timeout))
            time.sleep(30)
            sleep_time += 30
        else:
            values['status'] = "error"
            raise NotImplementedError("Unexpected status messsage: " + status_msg)
    if sleep_time == timeout:
        values['status'] = 'error'
        device.log(level="ERROR", message="Application Signature package download timed out")
        raise Exception("Application Signature package download timed out")
    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="Application Signature package download is failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("Application Signature package download is failed. Message - " + values[
                'message'])
        else:
            device.log(level="INFO", message="Application Signature package download is failed")
            device.log(level="INFO", message=values['message'])
    else:
        device.log(level="INFO", message="Application Signature package download is successful")
        device.log(level="INFO", message=values['message'])
    return values


def _process_install_status_msg(device, timeout, node, mode="install"):
    """
    To process the install status messages
    :param: node
        *OPTIONAL* To get the node specific information
    :return: Returns install status as success or error
    :rtype: dict
    """
    values = {}
    cmd = "request service application-identification install status"
    if mode == "uninstall":
        cmd = "request service application-identification uninstall status"
    status_rpc_str = device.get_rpc_equivalent(command=cmd)
    sleep_time = 0
    while sleep_time < timeout:
        response = device.execute_as_rpc_command(command=status_rpc_str, command_type="rpc",
                                                 node=node)
        if mode == "uninstall":
            status_msg = response["apppack-uninstall-status"]["apppack-uninstall-status-detail"]
        else:
            status_msg = response["apppack-install-status"]["apppack-install-status-detail"]
        values['message'] = str(status_msg)
        if re.search(r'in\sprogress', status_msg, re.DOTALL|re.IGNORECASE):
            device.log(level="INFO", message="(%d/%d secs) Sleeping 30 seconds..." %(sleep_time,
                                                                                     timeout))
            time.sleep(30)
            sleep_time += 30
        elif re.search(r'checking|cleaning', status_msg, re.IGNORECASE):
            device.log(level="INFO", message="(%d/%d secs) Sleeping 30 seconds..." %(sleep_time,
                                                                                     timeout))
            time.sleep(30)
            sleep_time += 30
        elif re.search(r'Installed.*Application\spackage.*and\sProtocol\sbundle\ssuccessfully',
                       status_msg, re.DOTALL):
            values['status'] = 'success'
            break
        elif re.search(r'Uninstalled.*Application\spackage.*and\sProtocol\sbundle\ssuccessfully',
                       status_msg, re.DOTALL):
            values['status'] = 'success'
            break
        elif re.search(r'error|failed', status_msg, re.IGNORECASE):
            values['status'] = "error"
            break
        else:
            values['status'] = "error"
            raise NotImplementedError("Unexpected status message: " + status_msg)
    if sleep_time == timeout:
        values['status'] = 'error'
        if mode == "uninstall":
            values['message'] = "Application signature package uninstall timed out"
            device.log(level="ERROR", message="Application signature package uninstall timed out")
        else:
            values['message'] = "Application signature package install timed out"
            device.log(level="ERROR", message="Application signature package install timed out")
    return values


def install_app_sig_package(device=None, node=None, validate=True, **kwargs):
    """
    To install the application signature package
    Example :-
        install_app_sig_package(device=dh)
        install_app_sig_package(device=dh, node="node1", validate=False)
    Robot Example :-
        install app sig package  device=${dh}
        install app sig package  device=${dh}  node=node1 validate=False
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param int timeout:
        *OPTIONAL* Time out for the signature install.
        ``Default value`` : 600 seconds
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the signature update. Validates by default
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: Returns the status of the install with dict having
            signature : version/status/message
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    timeout = kwargs.get('timeout', 600)
    cmd = "request services application-identification install "
    values = {'status': 'success'}

    # Execute the install command and check for license error
    if device.is_ha() is False or node is not None:
        install_status = device.cli(command=cmd, node=node).response()
        if re.search(r'Require application identification license|failed', install_status):
            values['message'] = install_status
            values['status'] = "error"
    else:
        resp = device.execute_as_rpc_command(command=cmd, node="all")
        install_status1 = str(resp[0]["apppack-install-status"]['apppack-install-status-detail'])
        install_status2 = str(resp[1]["apppack-install-status"]['apppack-install-status-detail'])
        if re.search(r'Require application identification license|failed', install_status1):
            values['message'] = install_status1
            values['status'] = "error"
            values['node'] = "node0"
        elif re.search(r'Require application identification license|failed', install_status2):
            values['message'] = install_status2
            values['status'] = "error"
            values['node'] = "node1"
    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="Application Signature update failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("Application Signature update failed - " + values['message'])
        else:
            device.log(level="INFO", message="Application Signature update failed")
            device.log(level="INFO", message=values['message'])
        return values

    # Wait till the signature install completes and get the status message
    if device.is_ha() is False or node is not None:
        # To handle SA or node specific info
        values = _process_install_status_msg(device, timeout, node)
        if values['status'] == 'error':
            device.log(level="INFO", message="Application Signature update install failed ")
    else:
        # To handle both HA node status
        values = _process_install_status_msg(device, timeout, "node0")
        values['node'] = "node0"
        if values['status'] == 'error':
            device.log(level="INFO", message="AppID Signature update install failed on" + "node0")

        values = _process_install_status_msg(device, timeout, "node1")
        values['node'] = "node1"
        if values['status'] == 'error':
            device.log(level="INFO", message="AppID Signature update install failed on" + "node1")

    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="AppID Signature update install failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("AppID Signature update install failed - " + values['message'])
        else:
            device.log(level="INFO", message="AppID Signature update install failed")
            device.log(level="INFO", message=values['message'])
    else:
        device.log(level="INFO", message="AppID Signature update install is successful")
        device.log(level="INFO", message=values['message'])
        match = re.search(r'package\s+\(([0-9]+)\)', values['message'], re.DOTALL)
        if match is not None:
            values['version'] = match.group(1)
        else:
            values['status'] = "error"
            device.log(level="ERROR", message="Unknown version of application signature ")
            raise NotImplementedError("Unknown version of application signature: " + values[
                'message'])
    return values


def uninstall_app_sig_package(device=None, node=None, timeout=600, validate=True):
    """
    To uninstall the application signature package
    Example :-
        uninstall_app_sig_package(device=dh)
        uninstall_app_sig_package(device=dh, node="node1", validate=False)
    Robot Example :-
        uninstall app sig package  device=${dh}
        uninstall app sig package  device=${dh}  node=node1 validate=False
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param int timeout:
        *OPTIONAL* Time out for the signature uninstall.
        ``Default value`` : 600 seconds
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the signature uninstall. Validates by default
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: Returns the status of the install with dict having
            signature : version/status/message
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    cmd = "request services application-identification uninstall "
    values = {'status': 'success'}

    if device.is_ha() is False or node is not None:
        install_status = device.cli(command=cmd, node=node).response()
        if re.search(r'Uninstall Application package and Protocol bundle failed', install_status):
            values['message'] = install_status
            values['status'] = "error"
    else:
        res = device.execute_as_rpc_command(command=cmd, node="all")
        install_status1 = str(res[0]["apppack-uninstall-status"]['apppack-uninstall-status-detail'])
        install_status2 = str(res[1]["apppack-uninstall-status"]['apppack-uninstall-status-detail'])
        if re.search(r'Uninstall Application package and Protocol bundle failed', install_status1):
            values['message'] = install_status1
            values['status'] = "error"
            values['node'] = "node0"
        elif re.search(r'Uninstall Application package and Protocol bundle failed',
                       install_status2):
            values['message'] = install_status2
            values['status'] = "error"
            values['node'] = "node1"
    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="Application Signature uninstall failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("Application Signature uninstall failed - " + values['message'])
        else:
            device.log(level="INFO", message="Application Signature uninstall failed")
            device.log(level="INFO", message=values['message'])
        return values

    # Wait till the signature uninstall completes and get the status message
    if device.is_ha() is False or node is not None:
        # To handle SA or node specific info
        values = _process_install_status_msg(device, timeout, node, mode="uninstall")
        if values['status'] == 'error':
            device.log(level="INFO", message="Application Signature update uninstall failed ")
    else:
        # To handle both HA node status
        values = _process_install_status_msg(device, timeout, "node0", mode="uninstall")
        values['node'] = "node0"
        if values['status'] == 'error':
            device.log(level="INFO", message="AppID Signature update uninstall failed on" + "node0")

        values = _process_install_status_msg(device, timeout, "node1", mode="uninstall")
        values['node'] = "node1"
        if values['status'] == 'error':
            device.log(level="INFO", message="AppID Signature update uninstall failed on" + "node1")

    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="AppID Signature update uninstall failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("AppID Signature update uninstall failed - " + values['message'])
        else:
            device.log(level="INFO", message="AppID Signature update uninstall failed")
            device.log(level="INFO", message=values['message'])
    else:
        device.log(level="INFO", message="AppID Signature update uninstall is successful")
        device.log(level="INFO", message=values['message'])
        match = re.search(r'package\s+\(([0-9]+)\)', values['message'], re.DOTALL)
        if match is not None:
            values['version'] = match.group(1)
        else:
            values['status'] = "error"
            device.log(level="ERROR", message="Unknown version of application package ")
            raise NotImplementedError("Unknown version of application package: " + values[
                'message'])
    return values


def update_app_sig_package(device=None, validate=True, overwrite=False, **kwargs):
    """
    TO download and install the signature package or templates.
    Example :-
        update_app_sig_package(device=dh)
        update_app_sig_package(device=dh, version="3000", validate=False)
        update_app_sig_package(device=dh, url="https://devdb.juniper.net/cgi-bin/index.cgi",
        action="override")
    Robot Example :-
        update app sig package device=${dh}
        update app sig package device=${dh} version=3000 validate={False}
        update app sig package device=${dh} url=https://devdb.juniper.net/cgi-bin/index.cgi
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str url:
        *OPTIONAL* Sigdb URL to configure and do download/install. Default is live sigdb (not
        configured)
    :param str version:
        *OPTIONAL* The appid signature package version to download.
        ``Default Value``: Lastest appid signature package will be downloaded
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the appid signature update. Validates by
        default
    :param str overwrite:
        *OPTIONAL* To overwrite the appid signature package even if installed is same.
        ``Supported Values``: True or False, Default is False
    :return: returns True if successful
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    url = kwargs.get('url', "")
    version = kwargs.get('version', "")
    if isinstance(version, int):
        version = str(version)

    # if override do not check for installed version

    re_sigpack_version = str(get_appid_sig_package_version(device=device))
    if version != "":
        if version == re_sigpack_version:
            if overwrite is True:
                uninstall_app_sig_package(device=device, validate=validate)
            else:
                device.log(level="INFO", message="Application Signature package requested version \
                                                 and installed in RE are same")
                return True
    else:
        rval = download_appid_sig_package(device=device, update_type="check", url=url,
                                          validate=validate)
        download_version = rval.get('version')
        if re_sigpack_version == download_version:
            if overwrite is True:
                uninstall_app_sig_package(device=device, validate=validate)
            else:
                device.log(level="INFO", message="Application Signature package version in RE and "
                                                 "available in live url are same")
                return True

    device.log(level="INFO", message="Downloading and installing the idp signature package")
    download_appid_sig_package(device=device, version=version, url=url, validate=validate)
    install_app_sig_package(device=device, validate=validate)

    return True


def get_appid_stats_application(device=None, node="local"):
    """
    To get the AppID application statistics as dictionary
    Example:
        get_appid_stats_application(device=device)

    ROBOT Example:
        Get Appid Stats Application   device=${device}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :return: Returns the dictionary for applications statistics
    :rtype: dict
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    version = device.get_version()
    status = device.execute_as_rpc_command(command="show services application-identification " + \
                                                   "statistics applications", node=node)

    if float(version[:4]) >= 18.3:
        status = status['appid-application-statistics-information']['logical-system-app-stats']
    else:
        status = status['appid-application-statistics-information']
    return status

def verify_appid_stats_application(device=None, application=None, session_count=None, bytes=None,
                                   encrypted=None, bytes_tolerance=0, validate=True,
                                   statistics_dict=None, node="local"):
    """
    To verify AppID application statistics.
    Example:
        verify_appid_stats_application(device=dt, application="xx", session_count="10",
            bytes="10", encrypted="Yes", statistics_dict=dict_to_return)

    ROBOT Example:
        Verify Appid Stats Application   device=${dt}   application=http
            session_count=10   bytes=10   encrypted=Yes   statistics_dict=${dict_to_return}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str application:
        **REQUIRED** Application Name
    :param str session_count:
        *OPTIONAL* Session Count
    :param str bytes:
        *OPTIONAL Bytes used by the app
    :param str bytes_tolerance:
        *OPTIONAL* Percentage tolerance for bytes
    :param str encrypted:
        *OPTIONAL*
        ``Supported values``:   "yes" , "no"
    :param bool validate:
        *OPTIONAL* Pass True if you want to raise exceptions if the function fails.
    :param dict statistics_dict:
        *OPTIONAL* AppID application statistics as dictionary on which verification takes place.
        get_appid_stats_application() returns this.
    :return: Boolean (True or False)
    :rtype: bool
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if application is None:
        device.log(level="INFO", message="'application' is a mandatory argument")
        raise ValueError("'application' is a mandatory argument")

    if statistics_dict is None:
        statistics_dict = get_appid_stats_application(device=device, node=node)

    list_of_dicts = []
    bytes_min = 0
    bytes_max = 0

    appid_stats_tag = "appid-application-statistics"

    if "appid-application-statistics" not in statistics_dict.keys() and \
                    "appid-application-statistics-usp" not in statistics_dict.keys():
        device.log(level="ERROR", message="No application Statistics Info available")
        if validate:
            raise Exception("No application Statistics Info available")
        return False

    #From 17.3 "-usp" is extra in the tag. Taking care of that here.
    if "appid-application-statistics-usp" in statistics_dict.keys():
        appid_stats_tag = appid_stats_tag + "-usp"


    if isinstance(statistics_dict[appid_stats_tag], list):
        application_found_flag = 0
        for x in statistics_dict[appid_stats_tag]:
            if x["application-name"] == application:
                application_found_flag = 1
                list_of_dicts.append(x)
        if application_found_flag == 0:
            device.log(level="ERROR", message="Application name not found")
            if validate:
                raise Exception("Application name not found")
            return False

    else:
        if statistics_dict[appid_stats_tag]["application-name"] == application:
            list_of_dicts.append(statistics_dict[appid_stats_tag])
        else:
            device.log(level="ERROR", message="Application name not found")
            if validate:
                raise Exception("Application name not found")
            return False

    if bytes is not None:
        bytes_delta = int(bytes)*int(bytes_tolerance)/100
        bytes_min = int(bytes) - bytes_delta
        bytes_max = int(bytes) + bytes_delta

    fail_flag = 1
    for x in list_of_dicts:
        if session_count is not None:
            if session_count != x['sessions']:
                continue
        if bytes is not None:
            if int(x['bytes']) > bytes_max or int(x['bytes']) < bytes_min:
                continue
        if encrypted is not None:
            if x['is_encrypted'] != encrypted:
                continue
        fail_flag = 0
        device.log(level="INFO", message="Statistics are successfully matched")
        break

    if fail_flag == 1:
        if validate:
            raise Exception("Statistics are not matching")
        return False
    return True


def get_appid_stats_application_grp(device=None, node="local"):
    """
    To get the AppID application Group statistics as dictionary
    Example:
        get_appid_stats_application_grp(device=device)

    ROBOT Example:
        Get Appid Stats Application Grp   device=${device}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :return: Returns the dictionary for application Group statistics
    :rtype: dict
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    version = device.get_version()
    status = device.execute_as_rpc_command(command="show services application-identification " + \
                                                   "statistics application-groups", node=node)
    if float(version[:4]) >= 18.3:
        status = status['appid-application-group-statistics-information']['logical-system-group-stats']
    else:
        status = status['appid-application-group-statistics-information']
    return status


def verify_appid_stats_application_grp(device=None, application_group=None, session_count=None,
                                       bytes=None, bytes_tolerance=0, validate=True,
                                       statistics_dict=None, node="local"):
    """
    To verify AppID application statistics.
    Example:
        verify_appid_stats_application_grp(device=dt, application_group="xx",
            session_count="10", bytes="10", statistics_dict=dict_to_return, bytes_tolerance="5")

    ROBOT Example:
        Verify Appid Stats Application Grp   device=${dt}   application_group=xx
            session_count=10   bytes=10   statistics_dict=${dict_to_return}   bytes_tolerance=5

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str application_group:
        **REQUIRED** Application Group Name
    :param str session_count:
        *OPTIONAL* Session Count
    :param str bytes:
        *OPTIONAL Bytes used by the application group
    :param str bytes_tolerance:
        *OPTIONAL* Percentage tolerance for bytes
    :param bool validate:
        *OPTIONAL* Pass True if you want to raise exceptions if the function fails.
    :param dict statistics_dict:
        *OPTIONAL* AppID application Group statistics as dictionary on which verification takes
        place. get_appid_stats_application_grp() returns this.
    :return: Boolean (True or False)
    :rtype: bool
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if application_group is None:
        device.log(level="INFO", message="'application_group' is a mandatory argument")
        raise ValueError("'application_group' is a mandatory argument")

    if statistics_dict is None:
        statistics_dict = get_appid_stats_application_grp(device=device, node=node)

    dict_to_check = {}
    bytes_min = 0
    bytes_max = 0

    appid_stats_tag = "appid-application-group-statistics"

    if "appid-application-group-statistics" not in statistics_dict.keys() and \
                    "appid-application-group-statistics-usp" not in statistics_dict.keys():
        device.log(level="ERROR", message="No application group Statistics Info available")
        if validate:
            raise Exception("No application group Statistics Info available")
        return False

    # From 17.3 "-usp" is extra in the tag. Taking care of that here.
    if "appid-application-group-statistics-usp" in statistics_dict.keys():
        appid_stats_tag = appid_stats_tag + "-usp"

    if isinstance(statistics_dict[appid_stats_tag], list):
        application_found_flag = 0
        for x in statistics_dict[appid_stats_tag]:
            if x["application-name"] == application_group:
                application_found_flag = 1
                dict_to_check = x
                break
        if application_found_flag == 0:
            device.log(level="ERROR", message="Application Group name not found")
            if validate:
                raise Exception("Application Group name not found")
            return False

    else:
        if statistics_dict[appid_stats_tag]["application-name"] == \
        application_group:
            dict_to_check = statistics_dict[appid_stats_tag]
        else:
            device.log(level="ERROR", message="Application Group name not found")
            if validate:
                raise Exception("Application Group name not found")
            return False

    if bytes is not None:
        bytes_delta = int(bytes)*int(bytes_tolerance)/100
        bytes_min = int(bytes) - bytes_delta
        bytes_max = int(bytes) + bytes_delta

    fail_flag = 0
    if session_count is not None:
        if session_count != dict_to_check['sessions']:
            fail_flag = 1
            device.log(level="ERROR", message="Session Count not matching")

    if bytes is not None:
        if int(dict_to_check['bytes']) > bytes_max or int(dict_to_check['bytes']) < bytes_min:
            fail_flag = 1
            device.log(level="ERROR", message="Bytes not matching with tolerance % = " + \
                                              str(bytes_tolerance))

    if fail_flag == 1:
        if validate:
            raise Exception("Statistics are not matching")
        return False
    device.log(level="INFO", message="Statistics are successfully matched")
    return True



def verify_apptrack_counters(device=None, counter_values=None, node="local"):
    """
    To verify Apptrack counters. (show security application-tracking counters)
    Example:
        verify_apptrack_counters(device=dt, counter_values={'Session create messages':1,
        'Session close messages':1}, node="node0")

    ROBOT Example:
        Verify Apptrack Counters   device=${dt}   counter_values=${{{'Session volume updates':1,
        'Session route updates':1}}}    node=node0

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param dict counter_values:
        **REQUIRED** Dictionary of counter names (key) and their expected values (value of the key).
        ``Supported values of counter names (key for dict)``:   'Session create messages'
                                                                'Session close messages'
                                                                'Session volume updates'
                                                                'Failed messages'
                                                                'Session route updates'
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: True/False , based on verification status
    :rtype: bool
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if counter_values is None:
        device.log(level="ERROR", message="counter_values is None, it is mandatory argument")
        raise ValueError("counter_values is None, it is mandatory argument")

    cmd = "show security application-tracking counters"
    status = device.execute_as_rpc_command(command=cmd, node=node)
    status = status['avt-counters']['avt-counter-statistics']

    fail_flag = 0
    list_of_names_in_device = status['name']
    list_of_values_in_device = status['value']

    for counter_name in counter_values.keys():
        if counter_name in list_of_names_in_device:
            index = list_of_names_in_device.index(counter_name)
            if int(counter_values[counter_name]) != int(list_of_values_in_device[index]):
                device.log(level="ERROR", message="Value mismatch for counter - " + counter_name)
                fail_flag = 1
        else:
            device.log(level="ERROR", message="Following counter name not found on device - "
                                              + counter_name)
            fail_flag = 1

    if fail_flag == 1:
        device.log(level="ERROR", message="Apptrack Counter verification failed")
        raise Exception("Apptrack Counter verification failed")

    device.log(level="INFO", message="Apptrack Counter verification passed")
    return True


def get_appid_status(device=None):
    """
    Get application identification status
    Example :-
        get_appid_status(device=dh)
    Robot Example:
        get appid status     device=$(dh)

    :param Device device:
        **REQUIRED** Handle of the device
    :return: Returns application identification status from the device
    :rtype : list
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    rpc_str = device.get_rpc_equivalent(command="show services application-identification status")
    etree_obj = device.execute_rpc(command=rpc_str).response()
    response = jxmlease.parse_etree(etree_obj)['appid-status-information']['appid-pic-status']

    status = []
    status = response
    return status


def split_get_protostate(device=None):
    """
    Get application identification protobundle state on both slots in split scenario
    Example :-
        split_get_protostate(device=dh)
    Robot Example:
        split get protostate     device=$(dh)

    :param Device device:
        **REQUIRED** Handle of the device
    :return: Returns protobundle state on both slots
    :rtype : list
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    appidstatus = []
    response = []
    response1 = []
    pbulist = []
    appidstatus = get_appid_status(device=device)

    for i in appidstatus:
        response = i['appid-protobundle-slot1-status']['status']
        for j in response:
            if j['status-name'] == 'Status':
                tmpslot1state = j['status-value']
            if j['status-name'] == 'Sessions':
                tmpslot1sessions = j['status-value']
        response1 = i['appid-protobundle-slot2-status']['status']
        for k in response1:
            if k['status-name'] == 'Status':
                tmpslot2state = k['status-value']
            if k['status-name'] == 'Sessions':
                tmpslot2sessions = k['status-value']

        if int(tmpslot1sessions) > 0:
            slot1session = 1
        else:
            slot1session = 0

        if int(tmpslot2sessions) > 0:
            slot2session = 1
        else:
            slot2session = 0

        if tmpslot1state == 'Active':
            slot1state = 1
        elif tmpslot1state == 'Free':
            slot1state = 0
        elif tmpslot1state == 'Deactivated':
            slot1state = 3
        else:
            slot1state = 2

        if tmpslot2state == 'Active':
            slot2state = 1
        elif tmpslot2state == 'Free':
            slot2state = 0
        elif tmpslot2state == 'Deactivated':
            slot2state = 3
        else:
            slot2state = 2

        pbulist.append(
            str(slot1state) +
            "-" +
            str(slot1session) +
            "-" +
            str(slot2state) +
            "-" +
            str(slot2session))

    return pbulist


def split_compare_states(device=None, oldstate=None, newstate=None):
    """
    Comparing protobundle state on all pics
    Example :-
        get_appid_status(device=dh)
    Robot Example:
        get appid status     device=$(dh)

    :param Device device:
        **REQUIRED** Handle of the device
    :param oldstate:
        **REQUIRED** Protobundle state of all pics before upgrade
    :param newstate:
        **REQUIRED** Protobundle state of all pics after upgrade
    :return: Returns application identification details from the device
    :rtype : bool
    """
    if device is None or oldstate is None or newstate is None:
        raise ValueError("Missing device handle or oldstate or newstate argument")

    if not isinstance(oldstate, list):
        raise ValueError("oldstate has to be list")

    if not isinstance(newstate, list):
        raise ValueError("newstate has to be list")

    values = []

    # These are the possible states of protobundle slots on system
    # state{'A-B-C-D'} = 'E-F-G-H' ; A,C,E,G are the state of pic and B,D,F,G
    # are state of traffic on system
    state = {'1-0-2-1': '1-0-2-1',
             '1-1-0-0': '2-1-1-0',
             '2-0-1-1': '1-0-2-1',
             '1-1-2-0': '2-1-1-0',
             '2-0-0-0': '2-0-1-0',
             '0-0-2-0': '1-0-2-0',
             '0-0-1-0': '1-0-0-0',
             '2-1-1-0': '2-1-1-0',
             '2-1-0-0': '2-1-1-0',
             '0-0-2-1': '1-0-2-1',
             '0-0-1-1': '1-0-2-1',
             '2-1-1-1': '1-0-2-1',
             '1-1-2-1': '2-1-1-0',
             '2-0-1-0': '1-0-0-0',
             '1-0-2-0': '0-0-1-0',
             '1-0-0-0': '0-0-1-0'}

    for i in oldstate:
        values.append(state[i])

    if newstate == values:
        device.log(
            level="INFO",
            message="Protobundle loading and change happened correctly")
        return True
    else:
        device.log(
            level="ERROR",
            message="Protobundle loading and change failed")
        raise Exception("Protobundle loading and change failed")


def get_appid_application_system_cache(device=None, node="local"):
    """
    To get the AppID application statistics as dictionary
    Example:
        get_appid_application_system_cache(device=device)

    ROBOT Example:
        Get Appid Application System Cache   device=${device}

    :param Device device:
        **REQUIRED** Device Handle of the dut®
    :return: Returns the dictionary for applications statistics®
    :rtype: list
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    status = device.execute_as_rpc_command(command="show services application-identification " +\
                                                   "application-system-cache", node=node)


    appcache_output = status['appid-application-system-cache-information']

    if "appid-application-system-cache" not in str(appcache_output) and \
            "appid-application-system-cache-usp" not in str(appcache_output):
        device.log(level="INFO", message="No application system cache Info available")

    appid_cache_tag = "appid-application-system-cache"
    # From 17.3 "-usp" is extra in the tag. Taking care of that here.
    if "appid-application-system-cache-usp" in str(appcache_output):
        appid_cache_tag = appid_cache_tag + "-usp"


    appcache_data = status['appid-application-system-cache-information']

    # Returning Empty dictionary, since there is no Cache data present
    if 'appid-application-system-cache-pic' not in appcache_data :
        device.log(level="INFO", message="No AppCache present")
        return {}

    appcache_data = appcache_data['appid-application-system-cache-pic']
    cache_list = []
    if isinstance(appcache_data, dict):
        appcache_data = [appcache_data]

    for cache_per_pic in appcache_data:
        pic_name = str(cache_per_pic['pic'])
        cache_pic_list = cache_per_pic[appid_cache_tag]
        if isinstance(cache_pic_list, dict):
            cache_pic_list = [cache_pic_list]
        for cache_entry in cache_pic_list:
            cache = {}
            cache['pic'] = pic_name
            cache['ipv6-address'] = cache_entry['ipv6-address']
            cache['appid-application'] = cache_entry['appid-application']
            cache['classification-path'] = cache_entry['classification-path']
            cache['is_encrypted'] = cache_entry['is_encrypted']
            cache['port'] = cache_entry['port']
            cache['protocol'] = cache_entry['protocol']
            cache['virtual-system-identifier'] = cache_entry['virtual-system-identifier']
            cache_list.append(cache)

    return cache_list


def verify_appid_application_system_cache(device=None, application=None, ip_adress=None, port=None,
                                   encrypted=None, proto=None, negate=False, virtual_sysid=None, pic=None,
                                   classification_path=None, appcache_dict=None, node="local"):
    """
    To verify AppID application system cache.
    Example:
        verify_appid_application_system_cache(device=None, application=None, ip_adress=None, port=None,
                                   encrypted=None, proto=None, negate=False, virtual_sysid=root-logical-system
                                   classification_path=None, appcache_dict=dict_to_return)

    ROBOT Example:
        Verify Appid Application System Cache   device=${dt}   application=http
            ip_adress=5.0.0.1   port=80   encrypted=Yes   proto=TCP   virtual_sysid=root-logical-system
            classification_path=IP:TCP:HTTP    appcache_dict=${dict_to_return}

    :param Device device:
        **REQUIRED** Device Handle of the dut
    :param str application:
        **REQUIRED** Application Name
    :param str ip_adress:
        *OPTIONAL*IP address
    :param str port:
        *OPTIONAL* Port used by the app
    :param str classification_path:
        *OPTIONAL* it shows the classification path of the app
    :param str proto:
        *OPTIONAL*  protocol used by the application
    :param str bytes_tolerance:
        *OPTIONAL* Percentage tolerance for bytes
    :param str encrypted:
        *OPTIONAL*
        ``Supported values``:   "yes" , "no"
    :param str virtual_sysid:
        *OPTIONAL* To give the system identifier value (eg: root, LSYS1)
    :param str pic:
        *OPTIONAL* To give the pic value
    :param bool negate:
        *OPTIONAL* Pass True if the cache for specific application is not present
    :param dict appcache_dict:
        *OPTIONAL* AppID application cache as dictionary on which verification takes place.
        get_appid_application_system_cache() returns this.
    :return: Boolean (True or False)
    :rtype: bool
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if application is None:
        device.log(level="INFO", message="'application' is a mandatory argument")
        raise ValueError("'application' is a mandatory argument")

    if appcache_dict is None:
        appcache_dict = get_appid_application_system_cache(device=device, node=node)

    # If returned dictionary is empty
    if not appcache_dict:
        if negate:
            device.log(level="INFO", message="Application is not found in cache, AS EXPECTED")
            return True
        else:
            device.log(level="ERROR", message="Application is not found in cache")
            raise Exception("Application is not found in cache")

    device.log(level="INFO", message="Verifying the application cache")
    
    # Adding the below code to update the argument values application and classification_path when application is SSL and dutr version is 18.2&above
    #Updated the below code to make changes from HTTPS to HTTP
    if classification_path is not None: 
        if 'SSL:HTTP' in classification_path or 'SSL:HTTPS' in classification_path:
            version = device.get_version()
            if float(version[:4]) >= 19.4 or float(version[:4]) < 18.2:
                if 'SSL:HTTPS' in classification_path:
                    classification_path = classification_path.replace('SSL:HTTPS', 'SSL:HTTP')
                    if 'HTTPS' in application:
                        application = re.sub('^HTTPS', 'HTTP', application)
            else:
                if 'SSL:HTTP' in classification_path and 'SSL:HTTPS' not in classification_path:
                    classification_path = classification_path.replace('SSL:HTTP', 'SSL:HTTPS')
                    if 'HTTP' in application  and 'HTTPS' not in application:
                        application = re.sub('^HTTP', 'HTTPS', application)

    list_of_dicts = []

    application_found_flag = 0

    for entry in appcache_dict:
        if isinstance (entry, dict):
            if entry["appid-application"] == application:
                application_found_flag = 1
                list_of_dicts.append(entry)

    if application_found_flag == 0:
        if negate:
            device.log(level="INFO", message="Application {0} is not found in cache, AS EXPECTED" .format(application))
            return True
        else:
            device.log(level="ERROR", message="Application {0} is not found in cache".format(application))
            raise Exception("Application is not found in cache")

    fail_flag = 1
    count = 0
    for x in list_of_dicts:
        if ip_adress is not None:
            if normalize_ipv6(ip_adress, compress_zero=True) != x['ipv6-address']:
                device.log(level="INFO", message="Incorrect IP address {0}" .format(ip_adress))
                continue
        if encrypted is not None:
            if x['is_encrypted'] != encrypted:
                device.log(level="INFO", message="Incorrect Encrypted field value {0}" .format(encrypted))
                continue
        if port is not None:
            if x['port'] != port:
                device.log(level="INFO", message="Incorrect Port value {0}" .format(port))
                continue
        if pic is not None:
            if x['pic'] != pic:
                device.log(level="INFO", message="Incorrect Pic value {0}" .format(pic))
                continue
        if proto is not None:
            if x['protocol'] != proto:
                device.log(level="ERROR", message="Incorrect Protocol value {0}" .format(proto))
                continue
        if classification_path is not None:
            if x['classification-path'] != classification_path:
                device.log(level="INFO", message="Incorrect Classification path {0}".format(classification_path))
                continue
        if virtual_sysid is not None:
            if x['virtual-system-identifier'] != virtual_sysid:
                device.log(level="INFO", message="Incorrect virtual system identifier {0}" .format(virtual_sysid))
                continue
        count += 1
        fail_flag = 0

    if fail_flag == 0:
        device.log(level="INFO", message="Application cache are successfully matched with details application {0}" .format(application))
        device.log(level="INFO", message="The Cache is found %d times" % count)
    else:
        if negate:
            device.log(level="INFO", message="Application system caches are not matching")
        else:
            device.log(level="ERROR", message="Application system caches are not matching")
            raise Exception("Application system caches are not matching")

    return True
