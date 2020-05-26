"""
IDP Operational commands
Author : Elango K <elango>
         Mohammad Ismail Qureshi <mqureshi>
"""

import re
import time
from jnpr.toby.security.idp.idp_config import configure_idp_security_package


def idp_remove_attack_in_sig_xml(device=None, attackname=None):
    """
    To remove signature from the signature update xml
    Example :-
        idp_remove_attack_in_sig_xml(device=dh, attackname="SPYWARE:RAT:BIFROSE")
    Robot Example :-
        idp remove attack in sig xml  device=${dh}  attackname=SPYWARE:RAT:BIFROSE
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str attackname:
        **REQUIRED** Attack to be removed from SignatureUpdate.xml
    :return Returns true or false on successful removing of the attack
    :rtype bool
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    if attackname is None:
        device.log(level="ERROR", message="Missing mandatory argument attackname")
        raise Exception("Missing mandatory argument attackname")

    file = "/var/db/idpd/sec-download/SignatureUpdate.xml"
    # Print the line number of the tag for the attack from update.xml
    cmd = "grep -B50 -A250 -n '<Name>%s</Name>' %s | grep -e '<Name>%s</Name>' -e 'Entry>' | " \
          "grep -A1 -B1 -e '<Name>%s</Name>'" % (attackname, file, attackname, attackname)
    rval = device.shell(command=cmd).response()

    # Get the line number of the attack tag
    match = re.search(r'([0-9]+)-\s+<Entry.* ?\n([0-9]+).* ?\n([0-9]+)', rval, re.DOTALL)
    if match is None:
        device.log(level="ERROR", message="grep command output is not as expected: " + rval)
        raise Exception("grep command output is not as expected: %s, hence not able to remove the "
                        "attack : %s" % (rval, attackname))
    start_line = match.group(1)
    atk_line = match.group(2)
    end_line = match.group(3)

    # Dump the lines in temp file excluding start to end to eliminate the attack in update.xml
    cmd = "awk 'NR<%s || NR>%s' %s > %s.tmp" % (start_line, end_line, file, file)
    device.shell(command=cmd)
    # Replace the update.xml with temp file
    cmd = "mv -f %s.tmp %s" % (file, file)
    device.shell(command=cmd)
    return True


def get_idp_security_pkg_details(device=None, node="local"):
    """
    Get the idp signature package details installed on the RE
    Example :-
        get_idp_security_pkg_details(device=dh)
    Robot Example :-
        get idp security pkg details  device=${dh}  node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: local, node0 or node1
        ``Default value``   : local
    :return: Returns the version of the sub components of idp signature package. The return
            values includes version/date/detector/templates
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    cmd = 'show security idp security-package-version'
    status = device.execute_as_rpc_command(command=cmd, node=node)
    values = {}

    # Return N/A if no signature package installed
    match = re.match('^[0-9N/A]*', status['idp-security-package-information'][ \
        'security-package-version'])
    values['version'] = match.group()
    # Return N/A if no signature package installed
    match = re.search(r'\(([A-Za-z]+)\s+([A-Za-z0-9\s:]+\s+)(.*?)\)',
                      status['idp-security-package-information']['security-package-version'])
    if match is None:
        values['date'] = "N/A"
    else:
        values['date'] = match.group(2)
    values['detector'] = str(status['idp-security-package-information']['detector-version'])
    values['templates'] = str(status['idp-security-package-information'][ \
                                  'policy-template-version'])
    return values


def get_idp_security_package_list(device=None, url=""):
    """
    Get the IDP signature package versions on the Live sig db server. The current one is at index 0,
    one before latest will be in index 1 and etc... in the order newest to oldest
    Example :-
        get_idp_security_package_list(device=dh)
        get_idp_security_package_list(device=dh, url="https://devdb.juniper.net/cgi-bin/index.cgi")
    Robot Example :-
        get idp security package list  device=${dh}
        get idp security package list  device=${dh}
        url=https://devdb.juniper.net/cgi-bin/index.cgi
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str url:
        *OPTIONAL* Sigdb URL to get the previous IDP signature package version. Default is live
        sigdb
                (not configured)
    :return: Returns the list of IDP signature package version available in the sig db server.
    :rtype: list
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    # Configure the sig db url before checking IDP signature version.
    configure_idp_security_package(device=device, url=url, commit=True)
    cmd = "show security idp recent-security-package-versions"
    sigpacks = device.execute_as_rpc_command(command=cmd)
    # Get the list of IDP signature packages
    sigpack_versions = sigpacks['idp-recent-security-package-information'][
        'recent-security-package-version']
    device.log(level="DEBUG", message="IDP Signature package list %s" % str(sigpack_versions))
    return sigpack_versions


def get_idp_prev_sec_pkg_version(device=None, url=""):
    """
    Get the previous (last) IDP signature package version
    Example :-
        get_idp_prev_sec_pkg_version(device=dh)
        get_idp_prev_sec_pkg_version(device=dh, url="https://devdb.juniper.net/cgi-bin/index.cgi")
    Robot Example :-
        get idp prev sec pkg version  device=${dh}
        get idp prev sec pkg version  device=${dh}  url=https://devdb.juniper.net/cgi-bin/index.cgi
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str url:
        *OPTIONAL* Sigdb URL to get the previous IDP signature package version. Default is live
                    sigdb (not configured)
    :return: Returns the last (previous) IDP signature package version available in the sig db
    server.
    :rtype: str
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    ver_list = get_idp_security_package_list(device=device, url=url)
    if len(ver_list) < 2:
        # List is empty or has only one IDP signature package
        version = "0"
    else:
        version = ver_list[1]
    device.log(level="INFO", message="Last IDP signature package version: " + version)
    return version


def _process_offline_download(device, timeout, node):
    """
    To process the offline download status messages
    :param: node
        *OPTIONAL* To get the node specific information
    :return: Returns install status as success or error
    :rtype: dict
    """
    values = {}
    cmd = "request security idp security-package offline-download status"
    rpc_str = device.get_rpc_equivalent(command=cmd)
    sleep_time = 0
    while sleep_time < timeout:
        response = device.execute_as_rpc_command(command=rpc_str, command_type="rpc", node=node)
        status_msg = response["offline-download-status"]["offline-download-status-detail"]
        values['message'] = str(status_msg)
        if re.search(r'Done;.*Successful.', status_msg, re.IGNORECASE):
            values['status'] = 'success'
            break
        elif re.search(r'Done;Attack DB update : not performed', status_msg, re.IGNORECASE):
            values['status'] = 'success'
            break
        elif re.search(r'Done;|error', status_msg, re.IGNORECASE):
            values['status'] = 'error'
            break
        elif re.search(r'Ready to accept a new request', status_msg, re.IGNORECASE):
            values['status'] = "error"
            break
        else:
            device.log(level="INFO", message="(%d/%d secs) Sleeping 15 seconds..." %(sleep_time,
                                                                                     timeout))
            time.sleep(15)
            sleep_time += 15
    if sleep_time == timeout:
        values['status'] = 'error'
        values['message'] = "Security package download timed out"
        device.log(level="ERROR", message="Security package download timed out")
    return values


def download_idp_offline_sec_pkg(device=None, file=None, timeout=180, node=None, validate=True):
    """
    To download the idp security package offline by providing offline security package
    Example :-
        download_idp_offline_sec_pkg(device=dh, path="/var/tmp/SignatureUpdate.zip")
    Robot example :-
        download idp offline sec pkg  device=${dh} path=/var/tmp/SignatureUpdate.zip
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str file:
        **REQUIRED** Path of the offline IDP signature update package file
    :param str node:
        *OPTIONAL* Node on which the command to be executed, Default executed on primary
        ``Supported Values``: None, node0 or node1
        ``Default Value``   : None, check status on both nodes
    :param int timeout:
        *OPTIONAL* Time out for the IDP signature download. Default is 120 seconds
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the IDP signature update. Validates by default
    :return: Returns the dict object with status of the sub modules. The return object includes
            values of download : status/message
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    if file is None:
        device.log(level="ERROR", message="Missing IDP signature update file name")
        raise Exception("Missing IDP signature update file name")

    values = {'status': 'error', 'message': ""}
    cmd = "request security idp security-package offline-download package-path " + file
    device.cli(command=cmd, node=node)

    # Wait till the IDP signature download completes and get the status message
    if device.is_ha() is False or node is not None:
        # To handle SA or node specific info
        values = _process_offline_download(device, timeout, node)
        if values['status'] == 'error':
            device.log(level="INFO", message="Offline IDP signature package download failed")
    else:
        # To handle both HA node status
        values = _process_offline_download(device, timeout, "node0")
        values['node'] = "node0"
        if values['status'] == 'error':
            device.log(level="INFO", message="Offline IDP signature package download failed: on "
                                             "node0")
        else:
            values = _process_offline_download(device, timeout, "node1")
            values['node'] = "node1"
            if values['status'] == 'error':
                device.log(level="INFO", message="Offline IDP signature package download failed: "
                                                 "on node1")

    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="Offline IDP Signature download failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("Offline IDP Signature download failed. Message - " + values['message'])
        else:
            device.log(level="INFO", message="Offline IDP Signature download failed")
            device.log(level="INFO", message=values['message'])
    else:
        device.log(level="INFO", message="Offline IDP Signature download successful")
        device.log(level="INFO", message=values['message'])
    return values


def download_idp_security_package(device=None, version=None, validate=True, **kwargs):
    """
    To download the idp security package
    Example :-
        download_idp_security_package(device=dh)
        download_idp_security_package(device=dh,
                                url="https://devdb.juniper.net/cgi-bin/index.cgi", version="3000")
        download_idp_security_package(device=dh, version="full-update", timeout=300)
        download_idp_security_package(device=dh, update_type="check")
        download_idp_security_package(device=dh, update_type="templates",
                                      url="https://devdb.juniper.net/cgi-bin/index.cgi")
    Robot Example :-
        download idp security package  device=${dh}
        download idp security package  device=${dh}  version=3000
                                            url=https://devdb.juniper.net/cgi-bin/index.cgi
        download idp security package  device=${dh}  version=full-update timeout=${300}
        download idp security package  device=${dh}  update type=check
        download idp security package  device=${dh}  update type=templates
                                         url=https://devdb.juniper.net/cgi-bin/index.cgi

    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str update_type:
        *OPTIONAL* Download options to perform.
        ``Supported Values``: check, signature or templates
        ``Default Value``   : signature
    :param str url:
        *OPTIONAL* Sigdb URL to configure and do download. Default is live sigdb (not configured)
    :param str version:
        *OPTIONAL* The IDP signature package version to download.
        ``Supported Values``: full-update or specific version
        ``Default Value``: latest IDP signature package will be downloaded
    :param int timeout:
        *OPTIONAL* Time out for the IDP signature download.
        ``Default value`` : 600 seconds
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the IDP signature update. Validates by default
    :return: Returns the dict object with status of the sub modules. The return object has values of
            check : version/url/detector/templates/status/message
            download : version/url/detector/date/status/message
            templates : version/url/status/message
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    url = kwargs.get('url', "")
    update_type = kwargs.get('update_type', "signature")
    timeout = kwargs.get('timeout', 600)

    base_cmd = "request security idp security-package download "
    # Configure the sigdb url
    configure_idp_security_package(device=device, url=url, commit=True)
    values = {}
    if update_type == "check":
        response = device.execute_as_rpc_command(command=base_cmd + "check-server")
        status_msg = response["secpack-download-status"]["secpack-download-status-detail"]
        values['message'] = str(status_msg)
        if re.match('^Successful*', status_msg):
            match = re.search(r'\(([a-z0-9:/.-]+)\).*:([0-9]*)\(Detector=([0-9.]*).*Templates=(['
                              r'0-9]*)\)', status_msg, re.DOTALL)
            values['url'] = match.group(1)
            values['version'] = match.group(2)
            values['detector'] = match.group(3)
            values['templates'] = match.group(4)
            values['status'] = "success"
        else:
            values['status'] = "error"
        if values['status'] == 'error':
            if validate is True:
                device.log(level="ERROR", message="Check server is failed")
                device.log(level="ERROR", message=values['message'])
                raise Exception("Check server is failed. Message " + values['message'])
            else:
                device.log(level="INFO", message="Check server is failed")
                device.log(level="INFO", message=values['message'])
        else:
            device.log(level="INFO", message="Check server successful")
            device.log(level="INFO", message=values['message'])
        return values
    elif update_type == "signature":
        if version is None:
            version = ""
        if version == "full-update":
            download_option = "full-update"
        elif version != "":
            if isinstance(version, int):
                version = str(version)
            download_option = "version " + version
        else:
            download_option = ""
        device.cli(command=base_cmd + download_option)
    elif update_type == "templates":
        device.cli(command=base_cmd + "policy-templates")
    else:
        values['status'] = "error"
        raise ValueError("Incorrect value for idp signature package download type")

    # Wait till the signature download completes and get the status message
    status_rpc_str = device.get_rpc_equivalent(command=base_cmd + 'status')
    sleep_time = 0
    while sleep_time < timeout:
        response = device.execute_as_rpc_command(command=status_rpc_str, command_type="rpc")
        status_msg = response["secpack-download-status"]["secpack-download-status-detail"]
        values['message'] = str(status_msg)
        if re.search(r'In\sprogress', status_msg):
            device.log(level="INFO", message="(%d/%d secs) Sleeping 30 seconds..." %(sleep_time,
                                                                                     timeout))
            time.sleep(30)
            sleep_time += 30
        elif re.search(r'Done;Successfully downloaded', status_msg, re.IGNORECASE):
            # Check sync message to secondary for HA
            if device.is_ha():
                if re.search(r'synchronized to backup', status_msg, re.IGNORECASE) is None:
                    values['status'] = "error"
                    device.log(level="INFO", message="HA back up sync is not successful")
                    break
            if update_type == "signature":
                match = re.search(r'\(([a-z0-9:/.-]+)\).*:([0-9]*)\((.*),\s+Detector=([0-9.]*)*\)',
                                  status_msg, re.DOTALL)
                values['url'] = match.group(1)
                values['version'] = match.group(2)
                values['date'] = match.group(3)
                values['detector'] = match.group(4)
            elif update_type == "templates":
                match = re.search(r'\(([a-z0-9:/.-]+)\).*:([0-9]*)', status_msg, re.DOTALL)
                values['url'] = match.group(1)
                values['version'] = match.group(2)
            values['status'] = "success"
            break
        elif re.search(r'Done;No Newer version available', status_msg, re.IGNORECASE):
            values['status'] = "success"
            break
        elif re.search(r'Ready to accept a new request', status_msg, re.IGNORECASE):
            values['status'] = "error"
            break
        elif re.search(r'error', status_msg, re.IGNORECASE):
            values['status'] = "error"
            break
        else:
            values['status'] = "error"
            raise NotImplementedError("Unexpected status message: " + status_msg)
    if sleep_time == timeout:
        values['status'] = 'error'
        device.log(level="ERROR", message="Security package download timed out")
        raise Exception("Security package download timed out")
    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="IDP Signature/template download is failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("IDP Signature/template download is failed. Message " + values[
                'message'])
        else:
            device.log(level="INFO", message="IDP Signature/template download is failed")
            device.log(level="INFO", message=values['message'])
    else:
        device.log(level="INFO", message="IDP Signature/Template download is successful")
        device.log(level="INFO", message=values['message'])
    return values


def _process_install_status_msg(device, timeout, node):
    """
    To process the install status messages
    :param: node
        *OPTIONAL* To get the node specific information
    :return: Returns install status as success or error
    :rtype: dict
    """
    values = {}
    cmd = "request security idp security-package install status"
    status_rpc_str = device.get_rpc_equivalent(command=cmd)
    sleep_time = 0
    while sleep_time < timeout:
        response = device.execute_as_rpc_command(command=status_rpc_str, command_type="rpc",
                                                 node=node)
        status_msg = response["secpack-update-status"]["secpack-status-detail"]
        values['message'] = str(status_msg)
        if re.search(r'In\sprogress', status_msg):
            device.log(level="INFO", message="(%d/%d secs) Sleeping 30 seconds..." %(sleep_time,
                                                                                     timeout))
            time.sleep(30)
            sleep_time += 30
        elif re.search(r'Done;', status_msg, re.IGNORECASE):
            values['status'] = 'success'
            break
        elif re.search(r'error', status_msg, re.IGNORECASE):
            values['status'] = "error"
            break
        else:
            values['status'] = "error"
            raise NotImplementedError("Unexpected status message: " + status_msg)
    if sleep_time == timeout:
        values['status'] = 'error'
        values['message'] = "IDP Security package install timed out"
        device.log(level="ERROR", message="Security package install timed out")
    return values


def install_idp_security_package(device=None, node=None, validate=True, **kwargs):
    """
    To install the idp security package
    Example :-
        install_idp_security_package(device=dh)
        install_idp_security_package(device=dh, update_type="templates)
        install_idp_security_package(device=dh, option="update-db-only")
        install_idp_security_package(device=dh, node="node1", validate=False)
    Robot Example :-
        install idp security package  device=${dh}
        install idp security package  device=${dh}  update type=templates
        install idp security package  device=${dh}  option=update-db-only
        install idp security package  device=${dh}  node=node1 validate=False
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str update_type:
        *OPTIONAL* Installation type to perform.
        ``Supported Values`` signature or templates,
        ``Default Value`` signature
    :param str option:
        *OPTIONAL* Install options. Supported value is update-db-only
    :param int timeout:
        *OPTIONAL* Time out for the IDP signature install.
        ``Default value`` : 900 seconds
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the IDP signature update. Validates by default
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: Returns the status of the install.
            templates : status/message
            signature : version/date/detector/cp-status/dp-status/status/message
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    option = kwargs.get('option', "")
    timeout = kwargs.get('timeout', 900)
    cmd = base_cmd = "request security idp security-package install "
    values = {'status': 'success'}
    update_type = kwargs.get('update_type', "signature")

    # use the install option only if install type is for IDP signature/package
    if update_type == "signature":
        option = option
        if option == "update-db-only":
            cmd = base_cmd + "update-attack-database-only"
    elif update_type == "templates":
        cmd = base_cmd + "policy-templates"
    else:
        raise ValueError("Incorrect value for idp signature package install type")

    # Execute the install command and check for license error
    if device.is_ha() is False or node is not None:
        install_status = device.cli(command=cmd, node=node).response()
        if re.search(r'invalid license', install_status):
            values['message'] = install_status
            values['status'] = "error"
    else:
        install_resp = device.execute_as_rpc_command(command=cmd, node="all")
        install_status1 = str(install_resp[0]["secpack-update-status"])
        install_status2 = str(install_resp[1]["secpack-update-status"])
        if re.search(r'invalid license', install_status1):
            values['message'] = install_status1
            values['status'] = "error"
            values['node'] = "node0"
        elif re.search(r'invalid license', install_status2):
            values['message'] = install_status2
            values['status'] = "error"
            values['node'] = "node1"
    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="IDP Signature update failed due to license error")
            device.log(level="ERROR", message=values['message'])
            raise Exception("IDP Signature update failed due to license error - " + values[
                'message'])
        else:
            device.log(level="INFO", message="IDP Signature update failed due to license error")
            device.log(level="INFO", message=values['message'])
        return values
    # Wait till the signature install completes and get the status message
    if device.is_ha() is False or node is not None:
        # To handle SA or node specific info
        values = _process_install_status_msg(device, timeout, node)
        if values['status'] == 'error':
            device.log(level="INFO", message="IDP Signature update install failed ")
    else:
        # To handle both HA node status
        values = _process_install_status_msg(device, timeout, "node0")
        values['node'] = "node0"
        if values['status'] == 'error':
            device.log(level="INFO", message="IDP Signature update install failed on" + "node0")
        else:
            values = _process_install_status_msg(device, timeout, "node1")
            values['node'] = "node1"
            if values['status'] == 'error':
                device.log(level="INFO", message="IDP Signature update install failed on" + "node1")

    if values['status'] == 'error':
        if validate is True:
            device.log(level="ERROR", message="IDP Signature update install failed")
            device.log(level="ERROR", message=values['message'])
            raise Exception("IDP Signature update install failed - " + values['message'])
        else:
            device.log(level="INFO", message="IDP Signature update install failed")
            device.log(level="INFO", message=values['message'])
        return values
    if values['status'] == 'success':
        device.log(level="INFO", message="IDP Signature update install is successful")
        device.log(level="INFO", message=values['message'])

    # Return the status and message if it is policy templates install. Continue to parse status
    # message for sigs
    if update_type == "templates":
        return values
    if re.search(r'Attack\sDB\supdate\s:\ssuccessful', values['message'], re.DOTALL):
        regex = r'UpdateNumber=([0-9]+).*ExportDate=(.*),Detector=([0-9.]*).*control-plane.*:\s([' \
                r'a-z]+).*data-plane.*:\s([a-z]+)'
        if option == "update-db-only":
            regex = r'UpdateNumber=([0-9]+).*ExportDate=(.*),Detector=([' \
                    r'0-9.]*).*control-plane.*:\s([a-z]+)'
        match = re.search(regex, values['message'], re.DOTALL)
        values['version'] = match.group(1)
        values['date'] = match.group(2)
        values['detector'] = match.group(3)
        values['cp-status'] = match.group(4)
        if option != "update-db-only":
            values['dp-status'] = match.group(5)
    elif re.search(r'Attack\sDB\supdate\s:\snot\sperformed', values['message'], re.DOTALL):
        values['status'] = 'not performed'
    elif re.search(r'AI installation failed', values['message'], re.DOTALL):
        values['status'] = "error"
        if validate is True:
            device.log(level="ERROR", message="IDP Signature update install failed on AI "
                                              "installation")
            device.log(level="ERROR", message=values['message'])
            raise Exception("IDP Signature update install failed on AI installation - " +
                            values['message'])
        else:
            device.log(level="INFO", message="IDP Signature update install failed on AI "
                                             "installation")
            device.log(level="INFO", message=values['message'])
    else:
        values['status'] = "error"
        device.log(level="ERROR", message="Unexpected install message, not implemented")
        raise NotImplementedError("Unexpected status message: " + values['message'])
    return values


def update_idp_signature_package(device=None, update_type="signature", validate=True, **kwargs):
    """
    TO download and install the signature package or templates.
    Example :-
        update_idp_signature_package(device=dh)
        update_idp_signature_package(device=dh, version="3000", option="update-db-only",
        validate=False)
        update_idp_signature_package(device=dh, update_type="templates)
        update_idp_signature_package(device=dh, url="https://devdb.juniper.net/cgi-bin/index.cgi",
        overwrite=True)
    Robot Example :-
        update idp signature package device=${dh}
        update idp signature package device=${dh} version=3000 option=update-db-only validate={
        False}
        update idp signature package device=${dh} update type=templates
        update idp signature package device=${dh} url=https://devdb.juniper.net/cgi-bin/index.cgi
        overwrite={True}
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str update_type:
        *OPTIONAL* Installation type to perform.
        ``Supported values``: signature or templates
        ``Default Value`` : signature
    :param str url:
        *OPTIONAL* Sigdb URL to configure and do download/install. Default is live sigdb (not
        configured)
    :param str version:
        *OPTIONAL* The idp signature package version to download.
        ``Supported Values``: full-update or specific version
        ``Default Value``: Lastest idp signature package will be downloaded
    :param bool validate:
        *OPTIONAL* Validate the success or failure of the idp signature update. Validates by default
    :param bool overwrite:
        *OPTIONAL* To overwrite the idp signature package even if installed is same.
        ``Supported Values``: True or False. Default is False
    :param str option:
        *OPTIONAL* Install options.
        ``Supported Value``: update-db-only
        ``Default Value``: None, update both db & data plane
    :return: returns True if successful
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    url = kwargs.get('url', "")
    option = kwargs.get('option', "")
    overwrite = kwargs.get('overwrite', False)
    version = kwargs.get('version', "")
    if isinstance(version, int):
        version = str(version)

    if update_type == "templates":
        # if override do not check for installed version
        if overwrite is False:
            re_template_version = get_idp_security_pkg_details(device=device).get('templates')
            if version != "":
                if version == re_template_version:
                    device.log(level="INFO", message="Template requested version and installed in "
                                                     "RE are same")
                    return True
            else:
                live_version = download_idp_security_package(device=device, update_type="check",
                                                             url=url).get("templates")
                if re_template_version == live_version:
                    device.log(level="INFO", message="Template RE version and available in live "
                                                     "url are same")
                    return True
        device.log(level="INFO", message="Downloading and installing the policy templates")
        download_idp_security_package(device=device, update_type=update_type, url=url,
                                      validate=validate)
        install_idp_security_package(device=device, update_type=update_type, validate=validate)
    elif update_type == "signature":
        # if override do not check for installed version
        if overwrite is False:
            re_sigpack_version = get_idp_security_pkg_details(device=device).get('version')
            if version != "" and version != "full-update":
                if version == re_sigpack_version:
                    device.log(level="INFO", message="IDP Signature package requested version and \
                                                     installed in RE are same")
                    return True
            else:
                rval = download_idp_security_package(device=device, update_type="check", url=url,
                                                     validate=validate)
                download_version = rval.get('version')
                if re_sigpack_version == download_version:
                    device.log(level="INFO", message="IDP Signature package version in RE and "
                                                     "available in live url are same")
                    return True
        device.log(level="INFO", message="Downloading and installing the idp signature package")
        if version != "":
            # if it is to download version or full-update
            download_idp_security_package(device=device, version=version, url=url,
                                          validate=validate)
        else:
            download_idp_security_package(device=device, url=url, validate=validate)
        if option == "update-db-only":
            install_idp_security_package(device=device, option=option, validate=validate)
        else:
            install_idp_security_package(device=device, validate=validate)
    else:
        raise ValueError("Incorrect value for idp signature package type.")
    return True


def get_idp_policy_commit_status(device=None, node=None):
    """
    Get the IDP policy installation status.
    Example :
        get_idp_policy_commit_status(device=dh)
        get_idp_policy_commit_status(device=dh, node="primary")
    Robot Example :-
        get idp policy commit status  device=${dh)
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: Returns dictionary containing status(started, compiling, loading, unloaded,
    success & error) and message, policy name and policy size
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    cmd = "show security idp policy-commit-status"
    response = device.execute_as_rpc_command(command=cmd, node=node)
    message = str(response['idp-policy-commit-status']['policy-commit-status-detail'])
    status = "error"
    if re.search(r'Beginning policy compilation', message, re.DOTALL):
        status = "started"
    elif re.search(r'Reading set file for compilation', message, re.DOTALL):
        status = "started"
    elif re.search(r'Reading prereq sensor config', message, re.DOTALL):
        status = "started"
    elif re.search(r'Compiling policy', message, re.DOTALL):
        status = "compiling"
    elif re.search(r'Generating compiled binary', message, re.DOTALL):
        status = "compiling"
    elif re.search(r'Starting policy package', message, re.DOTALL):
        status = "loading"
    elif re.search(r'Policy packaging completed successfully', message, re.DOTALL):
        status = "loading"
    elif re.search(r'Starting policy load', message, re.DOTALL):
        status = "loading"
    elif re.search(r'loaded successfully', message, re.DOTALL):
        status = "success"
    elif re.search(r'Active policy not configured or Active policy not modified', message,
                   re.DOTALL):
        status = "nochange"
    elif re.search(r'Running policy unloaded', message, re.DOTALL):
        status = "unloaded"
    elif re.search(r'error', message, re.DOTALL|re.IGNORECASE):
        status = "error"
    else:
        status = "error"
        device.log(level="ERROR", message="Policy commit status message not implemented: %s" %
                                          message)
        raise NotImplementedError("Policy commit status message not implemented: %s" % message)

    policy_status = {'message': message, 'status': status}
    # if success get the policy name & policy size
    if status == "success":
        match = re.search(r"IDP policy.*/([a-zA-Z0-9-_]+).bin.gz.v.*size\sis:([0-9]+)", message,
                          re.DOTALL)
        if match is not None:
            policy_status['name'] = match.group(1)
            policy_status['size'] = match.group(2)
    return policy_status


def get_idp_policy_status_detail(device=None, node=None):
    """
    Get the policy commit status details
    Example:
        get_idp_policy_status_detail(device=dh)
        get_idp_policy_status_detail(device=dh, node="node0")
    Robot Example :-
        get idp policy status detail  device=${dh}
        get idp policy status detail  device=${dh} node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: Returns commit status details messages
    :rtype: str
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    cmd = "show security idp policy-commit-status detail"
    response = device.execute_as_rpc_command(command=cmd, node=node)
    message = str(response['idp-policy-commit-status']['policy-commit-status-detail'])
    if re.search(r'loaded successfully', message, re.DOTALL):
        status = "success"
    else:
        status = "error"

    policy_status = {'message': message, 'status': status}
    # if success get the policy name & policy size
    if status == "success":
        match = re.search(r"IDP policy.*/([a-zA-Z0-9-_]+).bin.gz.v.*size\sis:([0-9]+).*DFA:\s+"
                          r"([A-Z]+).*PCRE\sconverted\spatterns:\s([0-9]+).*RSS:([0-9]+)",
                          message, re.DOTALL)
        if match is not None:
            policy_status['name'] = match.group(1)
            policy_status['size'] = match.group(2)
            policy_status['pattern'] = match.group(3)
            policy_status['converted'] = match.group(4)
            policy_status['max_rss'] = match.group(5)
    return policy_status


def clear_idp_policy_commit_status(device=None, node=None):
    """
    Clears the policy commit status
    Example:
        clear_idp_policy_commit_status(device=dh)
        clear_idp_policy_commit_status(device=dh, node="node0")
    Robot Example :-
        clear idp policy commit status  device=${dh}
        clear idp policy commit status  device=${dh} node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    device.cli(command="show security idp policy-commit-status clear", node=node)


def clear_idp(device=None, what="all", counter_names=None, node=None):
    """
    To clear IDP attack table, application statistics, counters, SSL session IDP cache,
    IDP status or all together.
    Example:
        clear_idp(device=dh)
        clear_idp(device=dh, what="attack-table", node="node0")
        clear_idp(device=dh, what="counter", counter_names=["flow", "ips"])
    Robot Example :-
        clear idp  device=${dh)
        clear idp  device=${dh)  what=attack-table  node=node0
        clear idp  device=${dh)  what=counter  counter_names=${["flow", "ips"]}
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str what:
        *OPTIONAL* Defines what to clear. Default value is "all".
        ``Supported values``: all, application-statistics, attack-table, ssl-session-id-cache,
        status, counter
        ``Default value``   : all
    :param list counter_names:
        *OPTIONAL* Defines which counter needs to be cleared. Necessary to pass the argument if
        argument what=>"counters"
        ``Supported values``: dfa, ips, flow, log, packet, memory, action, packet-log,
        application-identification, http-decoder, policy-manager, ssl-inspection, tcp-reassembler
        ``Default value``   : clears all the counters
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    base_cmd = "clear security idp "
    base_cmd_counters = "clear security idp counters "
    counters_list_all = ['action', 'application-identification', 'dfa', 'flow', 'http-decoder',
                         'ips', 'log', 'memory', 'packet', 'packet-log', 'policy-manager',
                         'ssl-inspection', 'tcp-reassembler']

    if what == "all":
        # Status clearing is not included all since it is not recommended to use in traffic
        # conditions
        device.cli(command=base_cmd + "attack table", node=node)
        device.cli(command=base_cmd + "application-statistics", node=node)
        device.cli(command=base_cmd + "ssl-inspection session-id-cache", node=node)
        # iterate all the counters to clear
        for name in counters_list_all:
            device.cli(command=base_cmd_counters + name, node=node)
    elif what == "counter":
        if counter_names is None:
            device.log(level="ERROR", messsage="counter_names liest is mandatory argument with " \
                                               "what is passed with value counter")
            raise Exception("counter_names liest is mandatory argument with what is passed with "
                            "value counter")
        if len(counter_names) == 0:
            device.log(level="ERROR", messsage="counter_names list doesn't have any value")
            raise ValueError("counter_names list doesn't have any value")
        for name in counter_names:
            device.cli(command=base_cmd_counters + name, node=node)
    elif what == "attack-table":
        device.cli(command=base_cmd + "attack table", node=node)
    elif what == "ssl-session-id-cache":
        device.cli(command=base_cmd + "ssl-inspection session-id-cache", node=node)
    else:
        device.cli(command=base_cmd + what, node=node)


def get_idp_attack_table(device=None, lsys=None, node=None):
    """
    To get the attack table and attack count
    Example:
        get_idp_attack_table(device=dh)
        get_idp_attack_table(device=dh, node="node0")
    Robot Example :-
        get idp attack table  device=${dh}
        get idp attack table  device=${dh} node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str lsys:
        *OPTIONAL* Name of the logical system for which you want to check
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: Returns attacks and count
    :rtype: str
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    attack_dict = {}

    cmd = "show security idp attack table"
    if lsys is not None:
        cmd = cmd + " logical-system " + lsys

    attacks = device.execute_as_rpc_command(command=cmd, node=node)
    if attacks is None:
        device.log(level="INFO", message="Attack table is empty")
        return attack_dict

    if len(attacks['idp-attack-information']) == 0 :
        device.log(level="INFO", message="Attack table is empty")
        return attack_dict
    attacks_detected = attacks['idp-attack-information']['idp-attack-statistics']
    # attacks_detected is list of dictionaries`, each dictionary will have attack and count as its
    #  element
    if isinstance(attacks_detected, dict):
        attacks_detected = [attacks_detected]
    for single_attack in attacks_detected:
        key = str(single_attack['name'])
        value = int(single_attack['value'])
        attack_dict[key] = value
    # returning dictionary containing attacks and their hit count
    return attack_dict


def verify_idp_attack(device=None, attacks=None, count=0, negate=False, node=None, lsys=None):
    """
    To verify the attack detection and attack count
    Example:
        verify_idp_attack(device=dh, attacks=["icmp-attack","tcp-attack"])
        verify_idp_attack(device=dh, attacks=["icmp-attack","tcp-attack"], negate=True)
        verify_idp_attack(device=dh, attacks=["icmp-attack","tcp-attack"], count=5)
        verify_idp_attack(device=dh, attacks=["icmp-attack","tcp-attack"], count=2, negate=True)
        verify_idp_attack(device=dh, attacks=["icmp-attack","tcp-attack"], count=5, node="node0")
    Robot Example:
        verify idp attack  device=${dh}  attacks=${["icmp-attack","tcp-attack"]}
        verify idp attack  device=${dh}  attacks=${["icmp-attack","tcp-attack"]}  negate=${True}
        verify idp attack  device=${dh}  attacks=${["icmp-attack","tcp-attack"]}  count=${5}
        verify idp attack  device=${dh}  attacks=${["icmp-attack","tcp-attack"]}  count=${2}
        negate=${True}
        verify idp attack  device=${dh}  attacks=${["icmp-attack","tcp-attack"]}  count=${5}
        node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str lsys:
        *OPTIONAL* Name of the logical system for which you want to check
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :param list attacks:
            **REQUIRED** attacks to be checked, should be passed as list
    :param int count:
        *OPTIONAL* Attack count to validate
        ``Default value``   : Default value is 0, i.e. count is ignored
    :param bool negate:
            *OPTIONAL*  negate , if True negate condition will be checked
        ``Supported values``: True or False
        ``Default value``   : False
    :param node:
            *OPTIONAL*  node , if HA device provide node0/node1,default value is local
    :return:
        Default - will return True if attack is detected
        detect & count - will rerun True if attack detected and count matches
        if negate & count not passed - will return True if attack not detected
        if negate & count is passed  - will return True if attack is detected but count does not
        match
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    if attacks is None:
        device.log(level="ERROR", message="attacks variable is None, it is mandatory argument")
        raise ValueError("attacks variable is None, it is mandatory argument")
    if isinstance(attacks, str):
        attacks=[attacks]
    if not isinstance(attacks, list):
        device.log(level="ERROR", message="attacks variable is not type of list")
        raise ValueError("attacks variable is not type of list")
    if len(attacks) < 1:
        device.log(level="ERROR", message="attack list is empty, minimum one attack is requried")
        raise ValueError("attack list is empty, minimum one attack is requried")
    attacks_detected = get_idp_attack_table(device=device, node=node, lsys=lsys)
    # if flag  got set "False" anywhere in code , attack match would be considered failed
    flag = True
    # Below code handling the case when we get empty attack table
    if len(attacks_detected) == 0 and negate is True:
        if count != 0:
            device.log(level='ERROR', message="Attack table is empty and Attack is not detected. "
                                              "Count mismatch for negate : Count - %d" % count)
            raise Exception("Attack table is empty and Attack is not detected. Count mismatch "
                            "for negatee : Count - %d" % count)
        else:
            device.log(level='INFO', message="Attack table is empty and Attack is not detected")
            return True
    elif len(attacks_detected) == 0:
        device.log(level='ERROR', message="Attack table is empty and Attack is not detected.")
        device.log(level="ERROR", message="Attacks list : " + str(attacks))
        raise Exception("Attack table is empty and Attack is not detected.")

    # If attack table has data ,we will check for all negative condition and set flag accordingly
    for attack in attacks:
        atk_count = attacks_detected.get(attack, -1)
        if negate is False:
            # handling case when attack not detected and negate is false
            if attack not in attacks_detected:
                device.log(level="ERROR", message="%s attack is not detected")
                flag = False
            # handling case when attack detected but hit count is not equal to count passed by user
            elif count == 0:
                device.log(level="INFO", message="%s Attack is detected" % attack)
            elif atk_count != count:
                device.log(level="ERROR", message="%s attack detected %d times. expected count - "
                                                  "%d" % (attack, atk_count, count))
                flag = False
            else:
                device.log(level="INFO", message="%s Attack is detected %d times" % (attack,
                                                                                     atk_count))
        else:
            if attack in attacks_detected:
                if count == 0:
                    # handling case attack detected and count is not passed by user, negate is true
                    device.log(level="ERROR",message="%s attack detected, but not expected to "
                                                     "detect" % attack)
                    flag = False
                elif atk_count == count:
                    # handling case when attack detected and hit count is equal to count passed by
                    # user but negate is true
                    device.log(level="ERROR", message="%s Attack detected %d times, Count mismatch "
                                                      "for negate, Count - %d" % (attack, atk_count,
                                                                                  count))
                    flag = False
                else:
                    device.log(level="INFO", message="%s attack count %d is not macthing detected "
                                                     "count %d" % (attack, count, atk_count))
            else:
                if count != 0:
                    # handling case attack not detected and count is passed by user, negate is true
                    device.log(level="ERROR", message="%s attack not detected, Count mismatch for "
                                                      "negate, Count - %d" % (attack, count))
                    flag = False
                else:
                    device.log(level="INFO", message="Attack %s is not detected" % attack)

    if flag is False:
        device.log(level="ERROR", message="Attack Detection failed")
        raise Exception("Attack Detection failed")
    return flag


def get_idp_counter(device=None, counter_name=None, node=None):
    """
    To get idp specific counters and their values
    Example:
        get_idp_counter (device=dh, counter_name="flow")
    Robot Example :-
        get idp counter  device=${dh}  counter_name=flow
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str counter_name:
        **REQUIRED** counter name to fetch the values
        ``Supported values``: action , application-ddos , application-identification , dfa , flow ,
                              http-decoder , ips , logs, memory , packet , packet-log ,
                              pdf-decoder , policy-manager , tcp-reassembler
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return:  counters and their values
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    if counter_name is None:
        device.log(level="ERROR", message="counter_name is mandatory argument")
        raise ValueError("counter_name is mandatory argument")

    cmd = "show security idp counter " + counter_name
    counter_xml = device.execute_as_rpc_command(command=cmd, node=node)
    counters = counter_xml['idp-counter-information']['idp-counter-statistics']
    counter_dict = {}
    for counter in counters:
        key = str(counter['name'])
        value = int(counter['value'])
        counter_dict[key] = value
    return counter_dict


def verify_idp_counter(device=None, counter_name=None, counter_values=None, node=None):
    """
    To verify the IDP counters
    Example:
        verify_idp_counter(device=dh, counter_name="packet", counter_values={'GTP flows':'10})
        verify_idp_counter(device=dh, counter_name="flow", counter_values={'Gates added':'3',
        'Sessions deleted':'5'},node="node0")
    Robot Example:-
        verify idp counter  device=${dh}  counter_name=packet  counter_values=${{'GTP flows':'10})
        verify idp counter  device=${dh}  counter_name=flow  counter_values=${{'Gates added':'3',
        'Sessions deleted':'5'}}  node=node0
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str counter_name:
        **REQUIRED** counter name to fetch the values
        ``Supported values``: action , application-ddos , application-identification , dfa , flow ,
                              http-decoder , ips , logs, memory , packet , packet-log ,
                              pdf-decoder , policy-manager , tcp-reassembler
    :param dict counter_values:
        **REQUIRED** counters and their valve to be matched , it can be defined as below
              match_counter ={'DFA Matches':'10','DFA compressed':'5',.....}
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: True/False , based on verification status
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")
    if counter_name is None:
        device.log(level="ERROR", message="counter_name is mandatory argument")
        raise ValueError("counter_name is mandatory argument")
    if counter_values is None:
        device.log(level="ERROR", message="counter_values is None, it is mandatory argument")
        raise ValueError("counter_values is None, it is mandatory argument")
    if not isinstance(counter_values, dict):
        device.log(level="ERROR", message="counter_values is not dict type")
        raise ValueError("counter_values is not dict type")
    if len(counter_values) == 0:
        device.log(level="ERROR", message="counter_values is empty, it is mandatory argument")
        raise ValueError("counter_values are empty, it is mandatory argument")

    counters_in_device = get_idp_counter(device=device, counter_name=counter_name, node=node)
    # Will start matching counters passed by users  with device counters
    keys = counter_values.keys()
    flag = True
    for counter in keys:
        if counter in counters_in_device:
            if counter_values[counter] == counters_in_device[counter]:
                device.log(level="INFO", message="%s has value %s , match successful" % (
                    counter, counters_in_device[counter]))
            else:
                flag = False
                device.log(level="ERROR", message="%s has value %s , match is not successful" % (
                    counter, counters_in_device[counter]))
        else:
            flag = False
            device.log(level="ERROR", message="%s counter not found in IDP counters" % counter)
    if flag is False:
        device.log(level="ERROR", messsage="IDP counter validation failed")
        raise Exception("IDP Counter validation failed")
    return flag


def get_idp_policy_templates_list(device=None, node=None):
    """
    Get the IDP policy templates installed on the RE
    Example :
        get_idp_policy_templates_list(device=dh)
        get_idp_policy_templates_list(device=dh, node="node1")
    Robot Example :-
        get idp policy templates list  device=${dh}
        get idp policy templates list  device=${dh} node=node1
    :param Device device:
        **REQUIRED** SRX Device handle.
    :param str node:
        *OPTIONAL* Output of the HA Node required, Ignored for non HA devices
        ``Supported values``: node0 or node1
        ``Default value``   : primary device if it is HA
    :return: Returns the list of policy templates installed on the device
    :rtype: list
    """
    if device is None:
        raise Exception("Device handle is mandatory argument")

    cmd = 'show security idp policy-templates-list'
    rval = device.execute_as_rpc_command(command=cmd, node=node)
    # Output comes as string, hence split by lines
    templates_list = rval['output'].splitlines()
    return templates_list
