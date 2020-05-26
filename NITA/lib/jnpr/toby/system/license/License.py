"""
#  DESCRIPTION:  Licensing related keywords
#       AUTHOR:  Radhakrishnan G
"""
import re
import jxmlease

def _validate_license_install(device, response, expected_status):

    if re.match(".*successfully\\s+added.*", response, re.DOTALL):
        device.log(level="INFO", message="License successfully added")
        status = "success"
    elif re.match(".*warning.*license\\s+already\\s+exists.*", response, re.DOTALL):
        device.log(level="INFO", message="License already exists")
        status = "exists"
    elif re.match(".*invalid\\s+license\\s+data.*", response, re.DOTALL):
        device.log(
            level="INFO", message="License add failed, invalid license data")
        status = "failure"
    else:
        device.log(level="INFO", message="Failed to add license")
        status = "failure"

    if expected_status == "success":
        if status == "success":
            device.log(
                level="INFO", message="Install of license is successful")
        else:
            device.log(level="ERROR", message="Install of license is failed")
            raise Exception("Failed to add license")
    elif expected_status == "exists":
        if status == "exists":
            device.log(level="INFO", message="License exists already")
        else:
            device.log(
                level="ERROR", message="License already exists message missing")
            raise Exception("License already exists message missing")
    else:
        if status == "failure":
            device.log(
                level="INFO", message="Adding license is failed as expected")
        else:
            device.log(
                level="ERROR", message="License load is successful when failure expected")
            raise Exception("License load is successful when failure expected")


def add_license_file(device=None, filename=None, expected_status=None):
    """
    Adding the license in the device using file

    Example :
    add_license_file(device=dh, filename="/var/home/regress/keys", expected_status="success")
    add_license_file(device=dh, filename ="/root/license", expected_status = "exists")
    Robot example:
    add license file    device=$(dh)   filename=/root/license  expected_status=failure

    :param Device device:
        **REQUIRED** Handle of the device
    :param str filename:
        **REQUIRED**  Path of the license file
    :param str expected_status:
        *OPTIONAL* ``Supported values``: "success", "failure", "exists" and "None"
         Default is None, where status message is not validated.
    :return: Returns license add status message
    :rtype: str
    """

    if filename == "" or device is None:
        raise ValueError("Missing device handle or filename argument")

    response = device.cli(
        command="request system license add " +
        filename).response()

    if expected_status is not None:
        _validate_license_install(device, response, expected_status)
    return response


def add_license_terminal(device=None, key=None, expected_status=None):
    """
    Adding the license in the device via terminal

    Example :
    add_license_terminal(device=dh, key="JUNOS860901 aeaqia gojrgr", expected_status="success")
    add_license_terminal(device=dh, key="JUNOS860901 aeaqia gojrgr", expected_status="exists")
    Robot example:
    add license terminal    device=$(dh)   key="JUNOS860901 aeaqia"  expected_status=failure

    :param Device device:
        **REQUIRED** Handle of the device
    :param str key:
        **REQUIRED**  License Key
    :param str expected_status:
        *OPTIONAL* ``Supported values``: "success", "failure", "exists" and "None"
         Default is None, where status message is not validated.
    :return: Returns license add status message
    :rtype: str
    """

    if key == "" or device is None:
        raise ValueError("Missing device handle or key argument")

    device.cli(command="request system license add terminal\r", pattern="key]")
    device.cli(command=key, pattern='')
    response = device.cli(command='\x04').response()

    if expected_status is not None:
        _validate_license_install(device, response, expected_status)
    return response


def delete_license(device=None, key_identifiers=None):
    """
    Deleting the licenses in the device

    Example :
    delete_license(device=dh, key_identifiers=["JUNOS271878"])
    delete_license(device=dh, key_identifiers=["all"])
    delete_license(device=dh, key_identifiers=["JUNOS860902","JUNOS860903"])
    Robot example:
    delete license    device=$(dh)   key_identifiers="JUNOS860901"
    delete license    device=$(dh)   key_identifiers=["JUNOS860902","JUNOS860903"]

    :param Device device:
        **REQUIRED** Handle of the device
    :param str key_identifiers:
        **REQUIRED** License key identifiers to be deleted or "all". Should be a list
    :return: Returns license deletion status
    :rtype : str
    """

    if device is None and key_identifiers is None:
        raise ValueError("Missing device handle or key identifiers argument")
    if not isinstance(key_identifiers, list):
        raise ValueError("Keyidentifier has to be list")

    if len(key_identifiers) == 0:
        raise ValueError("Size of key identifier list is zero")
    if len(key_identifiers) == 1:
        device.cli(
            command="request system license delete " +
            key_identifiers[0],
            pattern="(no)")
        response = device.cli(command='yes').response()
    else:
        identifier = str(key_identifiers).replace(",", " ").replace("'", " ")
        device.cli(
            command="request system license delete license-identifier-list " +
            identifier,
            pattern="(no)")
        response = device.cli(command='yes').response()

    if re.match(".*license\\s+key\\s+does\\s+not\\s+exist.*", response, re.DOTALL):
        device.log(level="INFO", message="License key does not exist")
    else:
        device.log(level="INFO", message="License deleted successfully")

    return response


def save_license_keys(device=None, filename=""):
    """
    Saving the license keys in the Device
    Example :
    save_license_keys(device=dh, filename="keys")
    save_license_keys(device=dh, filename="/var/home/regress/keys")
    Robot Example:
    save license keys    device=$(dh)   filename="keys"

    :param Device device:
        **REQUIRED** Handle of the device
    :param str filename:
        *OPTIONAL* Path of the filename. If filename not given, license keys dumped on terminal
    :return: Returns license saved status
    :rtype : str
    """

    if device is None:
        raise ValueError("Missing device handle argument")

    if filename == "":
        response = device.cli(command="request system license save terminal")
        return response
    else:
        response = device.cli(
            command="request system license save " +
            filename).response()

    if re.match(".*Wrote.*lines\\s+of\\s+license\\s+data", response, re.DOTALL):
        device.log(level="INFO", message="License successfully saved")
    else:
        device.log(level="ERROR", message="Failed to save license")
        raise Exception("Failed to save license")
    return response


def configure_license_traceoptions(
        device=None,
        mode="set",
        filename="",
        flag="all",
        **kwargs):
    """
    Configuring license traceoptions

    Example:
    configure_license_traceoptions(device=dh, filename="license")
    configure_license_traceoptions(device=dh, filename="license",flag="events")
    configure_license_traceoptions(device=dh, mode="set",filename="license",flag="all",
    commit="yes",max_no_files="4",size="1000000")
    configure license_traceoptions    device=$(dh)   filename="license"

    :param Device device:
        **REQUIRED** Handle of the device
    :param str filename:
       **REQUIRED** Name of the file to be created
    :param str mode:
        *OPTIONAL* ``Supported options``:  "set", "delete". Default value is set
    :param str flag:
        *OPTIONAL* ``Supported options``: "all", "config", "events". Default value is all
    :param str commit:
        *OPTIONAL* ``Supported options``:  "yes", "no". Default value is yes
    :param int max_no_files:
        *OPTIONAL* Maximum no of trace files to be created on system. Default number of files 2
    :param int size:
        *OPTIONAL* Maximum size of the trace file. Default size of the file is 10000000 bytes
    """
    commit = kwargs.get('commit', "yes")
    max_no_files = kwargs.get('max_no_files', "2")
    size = kwargs.get('size', "10000000")

    if filename == "" or device is None:
        raise ValueError("Missing filename or device handle argument")

    cfg_node = mode + " system license traceoptions "
    cmdlist = []

    if mode == "set":
        cmdlist.append(
            cfg_node +
            " file " +
            filename +
            " files " +
            max_no_files +
            " size " +
            size)
        cmdlist.append(cfg_node + " flag " + flag)
    elif mode == "delete":
        cmdlist.append("delete system license traceoptions ")

    # Configure and commit the configuration
    if len(cmdlist) != 0:
        device.config(command_list=cmdlist)
    if commit == "yes" and len(cmdlist) != 0:
        device.commit()


def show_license(device=None, what=None):
    """
    Display licenses installed in the device
    Example :-
    show_license(device=dh)
    show_license(device=dh, what="installed")
    show_license(device=dh, what="keys")
    show_license(device=dh, what="usage")
    Robot Example:
    show license     device=$(dh)  what="keys"
    show license     device=$(dh)  what="installed"
    show license     device=$(dh)  what="keys"

    :param Device device:
        **REQUIRED** Handle of the device
    :param str what:
        *OPTIONAL* ``Supported values``: "installed", "keys", "usage", and "None"
    :return: Returns license installed, keys and usage details in the DUT
    :rtype : str
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    base_cmd = "show system license "

    if what == "installed":
        response = device.cli(command=base_cmd + "installed")
    elif what == "keys":
        response = device.cli(command=base_cmd + "keys")
    elif what == "usage":
        response = device.cli(command=base_cmd + "usage")
    else:
        response = device.cli(command=base_cmd)

    return response


def get_license_installed(device=None):
    """
    Get license installed details in the device
    Example :-
    get_license_installed(device=dh)
    Robot Example:
    get license installed     device=$(dh)

    :param Device device:
        **REQUIRED** Handle of the device
    :return: Returns license installed details from the device
    :rtype : list
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    rpc_str = device.get_rpc_equivalent(command="show system license installed")
    etree_obj = device.execute_rpc(command=rpc_str).response()
    response = jxmlease.parse_etree(etree_obj)['license-information']['license']

    list_of_licenses = []
    if isinstance(response, list):
        list_of_licenses = response
    else:
        list_of_licenses.append(response)

    return list_of_licenses


def get_license_usage(device=None):
    """
    Get license usage details in the device
    Example :-
    get_license_usage(device=dh)
    Robot Example:
    get license usage     device=$(dh)

    :param Device device:
        **REQUIRED** Handle of the device
    :return: Returns license usage details from the device
    :rtype : list
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    rpc_str = device.get_rpc_equivalent(command="show system license usage")
    etree_obj = device.execute_rpc(command=rpc_str).response()
    response = jxmlease.parse_etree(etree_obj)['license-usage-summary']['feature-summary']

    list_of_licenses = []
    if isinstance(response, list):
        list_of_licenses = response
    else:
        list_of_licenses.append(response)

    return list_of_licenses


def get_id_from_key(device=None, key=None):
    """
    To get license identifier from the key
    Example:-
    get_id_from_key(device=None, key="170412921;SW-SRX1500-CS-BUN-3-3;1;2")
    Robot Example:
    get id from key     device=$(dh)    key=15_MINS 5;reserved;ACME1;1;2;170412921

    :param Device device:
        **REQUIRED** Handle of the device
    :param str key:
        **REQUIRED** License key
    :return: Returns license identifier from the key
    :rtype : int
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    if key is None:
        raise ValueError("key is a mandatory argument")

    identifier = 0
    match = re.search(";([0-9]{9});", key, re.DOTALL)
    if match:
        identifier = match.group(1)

    if int(identifier) == 0:
        raise Exception("Not able to fetch ID")

    return identifier


def get_license_identifiers(device=None, feature_name=None, validate=False):
    """
    To get license identifiers for the feature specified
    Example:-
    get_license_identifier(device=None, feature_name="idp-sig")
    ROBOT example:
    get license identifiers    device=$(dh) feature_name="idp-sig"
    :param Device device:
        **REQUIRED** Handle of the device
    :param str feature_name:
        **REQUIRED** Name of the licensed feature
    :param bool validate
        *OPTIONAL* Validates the license installed or not. Doesn't Validate by default
    :return: Returns license identifier
    :rtype : list
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    if feature_name is None:
        device.log(level="ERROR", message="feature_name is a mandatory argument")
        raise ValueError("Missing feature_name argument")

    identifier_list = []
    list_of_licenses = get_license_installed(device=device)

    for license in list_of_licenses:
        license_detail = license['feature-block']['feature']
        if isinstance(license_detail, dict):
            license_detail = [license_detail]
        for sub_license in license_detail:
            if sub_license['name'] == feature_name:
                identifier_list.append(str(license['name']))
                break

    if len(identifier_list) == 0 and validate is True:
        device.log(level="ERROR", message="Feature : " + feature_name + " not found")
        raise ValueError("Licensed feature : " + feature_name + " not found")

    return identifier_list


def check_license_directory(device=None, license_id=None, file_exist=None):
    """
    To check the license identifier present in the safenet license directory
    Example:-
    check_license_directory(device=None, license_id="170412921", file_exist="yes")
    check_license_directory(device=None, license_id="170412921", file_exist="no")
    Robot example:
    check license directory    device=$(dh)   license_id=170412921    file_exist=yes
    :param Device device:
        **REQUIRED** Handle of the device
    :param str license_id:
        **REQUIRED** License key Identifier
    :param str file_exist:
        *OPTIONAL* Checks license file exists or not.
    :return: Returns license file name 
    :return str
    """
    if device is None:
        raise ValueError("Missing device handle argument")

    if license_id is None:
        device.log(level="ERROR", message="license_id is mandatory")
        raise ValueError("Missing license_id which is mandatory")

    device.shell(command="cd /config/license/safenet")
    response = device.shell(command="ls " + license_id).response()

    if file_exist == "yes":
        if response == license_id:
            device.log(level="INFO", message="File " + license_id + " found")
        else:
            device.log(level="ERROR", message="File : " + license_id + " not found")
            raise ValueError("File : " + license_id + " not found")
    else:
        if response == license_id:
            device.log(level="ERROR", message="File : " + license_id + " found")
            raise ValueError("File : " + license_id + " found")
        else:
            device.log(level="INFO", message="File " + license_id + " not found")

    return response


def verify_license_installed(device=None, license_id=None, **kwargs):
    """
    To verify License installed details in the device
    Example:-
    verify_license_installed(device=dh, license_id="RMS000000010", feature_name="appid-sig")
    verify_license_installed(device=dh, feature_name="appid-sig", license_id="RMS00109"
                             license_version="1")
    verify_license_installed(device=dh, feature_name="wf_key_websense_ewf",
                             license_id="RMS000000010", license_state="valid")
    verify_license_installed(device=dh, feature_name="av_key_sophos_engine"
                             license_id="RMS000000010", license_version="1")
    verify_license_installed(device=dh, feature_name="anti_spam_key_sbl", license_id="RMS000000010",
                             license_version="1", license_state="valid")
    ROBOT Example:
    verify license installed    device=$(dh) feature_name="idp-sig"  license_id="RMS000000010"
    verify license installed    device=$(dh) feature_name="idp-sig" license_version="1"
    verify license installed    device=$(dh) feature_name="idp-sig"  license_state="valid"

    :param Device device:
        **REQUIRED** Handle of the device
    :param str feature_name:
        **REQUIRED** Name of the licensed feature
    :param str license_id:
        *OPTIONAL* License key Identifier
    :param str license_state:
        *OPTIONAL* State of the license. ``Supported values``: "valid" and "expired"
    :param str license_version:
        *OPTIONAL* Version of the license. ``Supported values``: "1", "2", "3", "4"
    :return: true or false
    :rtype: bool
    """
    feature_name = kwargs.get('feature_name', None)
    license_state = kwargs.get('license_state', None)
    license_version = kwargs.get('license_version', None)
    license_expiry = kwargs.get('license_expiry', None)

    if device is None:
        raise ValueError("Missing device handle argument")

    if license_id is None:
        device.log(level="ERROR", message="license_id is mandatory")
        raise ValueError("Missing license_id which is mandatory")

    # Building a list for installed licenses with the given license name
    installed_licenses = get_license_installed(device=device)

    license_id_found = 0
    for licensing in installed_licenses:
        if licensing['name'] == license_id:
            license_id_found = 1
            break

    if license_id_found == 0:
        device.log(level="ERROR", message="License Identifier : " + license_id + " not found")
        raise ValueError("License Identifier : " + license_id + " not found")

    # Verification part
    test_fail = 0
    if feature_name is not None:
        if licensing['feature-block']['feature']['name'] == feature_name:
            device.log(level="INFO", message="Feature name matched successfully")
        else:
            test_fail = 1
            device.log(level="ERROR", message="Feature name couldn't be matched")

    if license_state is not None:
        if licensing['license-state'] == license_state:
            device.log(level="INFO", message="License State matched successfully")
        else:
            test_fail = 1
            device.log(level="ERROR", message="License State couldn't be matched")

    if license_version is not None:
        if licensing['license-version'] == license_version:
            device.log(level="INFO", message="License Version matched successfully")
        else:
            test_fail = 1
            device.log(level="ERROR", message="License Version couldn't be matched")

    if license_expiry is not None:
        if licensing['feature-block']['feature']['validity-information']['end-date'] == license_expiry:
            device.log(level="INFO", message="License expiry matched successfully")
        else:
            test_fail = 1
            device.log(level="ERROR", message="License expiry couldn't be matched")

    if test_fail == 1:
        device.log(level="ERROR", message="Verify license installed failed")
        raise ValueError("Verify license installed failed")

    return True


def verify_license_usage(device=None, feature_name=None, license_used=None, **kwargs):
    """
    To verify License usage details in the device
    Example:-
    verify_license_usage(device=dh, feature_name="Virtual Appliance", license_used="1")
    verify_license_usage(device=dh, feature_name="idp-sig", license_installed="2")
    verify_license_usage(device=dh, feature_name="appid-sig", license_needed="0")
    verify_license_usage(device=dh, feature_name="wf_key_websense_ewf", license_used="1",
                         license_installed="2")
    verify_license_usage(device=dh, feature_name="av_key_sophos_engine", license_needed="0"
                         license_installed="2", license_used="1")
    ROBOT Example:
    verify license usage    device=$(dh) feature_name="idp-sig"  license_used="1"
    verify license usage    device=$(dh) feature_name="idp-sig"  license_installed="2"
    verify license usage    device=$(dh) feature_name="idp-sig"  license_needed="0"
                            license_installed="2" license_used="1"

    :param Device device:
        **REQUIRED** Handle of the device
    :param str feature_name:
        **REQUIRED** Name of the licensed feature
    :param str license_used:
        *OPTIONAL* Number of licenses being used
    :param str license_installed:
        *OPTIONAL* Number of licenses installed
    :param str license_needed:
        *OPTIONAL* Number of licenses needed
    :return: true or false
    :rtype: bool
    """
    license_installed = kwargs.get('license_installed', None)
    license_needed = kwargs.get('license_needed', None)

    if device is None:
        raise ValueError("Missing device handle argument")

    if feature_name is None:
        device.log(level="ERROR", message="feature_name is a mandatory argument")
        raise ValueError("Missing license_name argument")

    if license_used is None and license_needed is None and license_installed is None:
        device.log(
            level="ERROR",
            message="license_used or license_needed or license_installed is mandatory")
        raise ValueError("Missing license_used or license_needed or license_installed argument")

    # Building a dictionary for installed licenses with the given license name
    installed_licenses = get_license_usage(device=device)

    feature_name_found = 0
    for licensing in installed_licenses:
        if licensing['name'] == feature_name:
            feature_name_found = 1
            license_dict = licensing
            break

    if feature_name_found == 0:
        device.log(level="ERROR", message="License for : " + feature_name + " not found")
        raise ValueError("License for : " + feature_name + " not found")

    # Verification Part
    test_fail = 0
    if license_used is not None:
        if license_used == license_dict['used-licensed']:
            device.log(level="INFO", message="License Used is matched successfully")
        else:
            test_fail = 1
            device.log(level="ERROR", message="License used couldn't be matched")

    if license_needed is not None:
        if license_needed == license_dict['needed']:
            device.log(level="INFO", message="License Needed is matched successfully")
        else:
            test_fail = 1
            device.log(level="ERROR", message="License Needed couldn't be matched")

    if license_installed is not None:
        if license_installed == license_dict['licensed']:
            device.log(level="INFO", message="License Installed is matched successfully")
        else:
            test_fail = 1
            device.log(level="ERROR", message="License Installed couldn't be matched")

    if test_fail == 1:
        device.log(level="ERROR", message="Verify license usage failed")
        raise ValueError("Verify license usage failed")

    return True


def verify_utm_license_status(device=None, utm_feature=None, license_valid=True):
    """
    TO verify UTM feature status in case of Valid or Invalid license.
    Example:
        verify_utm_license_status(device=dh, utm_feature="web-filtering")
        verify_utm_license_status(device=dh, utm_feature="anti-spam", license_valid=False)

    ROBOT Example:
        Verify UTM License Status   device=${dh}   utm_feature=web-filtering
        Verify UTM License Status   device=${dh}   utm_feature=anti-spam   license_valid=${False}

    :param Device device:
        **REQUIRED** Device handle of the DUT
    :param str utm_feature:
        **REQUIRED** Name of the UTM feature.
        ``Supported values``:   "anti-virus"
                                "web-filtering"
                                "anti-spam"
    :param bool license_valid:
        *OPTIONAL* Pass if a valid license is installed or not.
    :return: Boolean (True or False)
    :rtype: bool
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if utm_feature is None:
        device.log(level="ERROR", message="'utm_feature' is a mandatory argument")
        raise ValueError("'utm_feature' is a mandatory argument")

    if utm_feature == "anti-virus":
        status = device.cli(command="show security utm anti-virus status").response()
        alarm_status = device.cli(command="show system alarms").response()
        device.cli(command="request security utm anti-virus sophos-engine pattern-delete")
        update_status = device.cli(
            command="request security utm anti-virus sophos-engine pattern-update").response()

        match = re.search(".*update disabled due to license invalidity.*", status, re.DOTALL)
        match_alarm = re.search(
            ".*Anti Virus with Sophos Engine usage requires a license.*",
            alarm_status,
            re.DOTALL)
        match_update = re.search(".*license invalidity.*", update_status, re.DOTALL)
        if license_valid is False:
            if not match:
                device.log(
                    level="ERROR",
                    message="Antivirus Update not disabled in case of Invalid license")
                raise ValueError("Antivirus Update not disabled in case of Invalid license")
            if not match_alarm:
                device.log(
                    level="ERROR",
                    message="Antivirus alarm not active in case of Invalid license")
                raise ValueError("Antivirus alarm not active in case of Invalid license")
            if not match_update:
                device.log(level="ERROR", message="Update not disabled in case of Invalid license")
                raise ValueError("Update not disabled in case of Invalid license")
        else:
            if match:
                device.log(
                    level="ERROR",
                    message="Antivirus status showing disabled in case of Valid license")
                raise ValueError("Antivirus status showing disabled in case of Valid license")
            if match_alarm:
                device.log(level="ERROR", message="Antivirus alarm active in case of Valid license")
                raise ValueError("Antivirus alarm active in case of Valid license")
            if match_update:
                device.log(level="ERROR", message="Update disabled in case of Valid license")
                raise ValueError("Update disabled in case of Valid license")

    elif utm_feature == "web-filtering":
        status = device.cli(command="show security utm web-filtering status").response()
        alarm_status = device.cli(command="show system alarms").response()
        match = re.search(".*Server\\s*status:.*UP.*", status, re.DOTALL)
        match_alarm = re.search(
            ".*Web Filtering EWF usage requires a license.*",
            alarm_status,
            re.DOTALL)
        if license_valid is False:
            if match:
                device.log(
                    level="ERROR",
                    message="Web Filtering Status shows UP in case of Invalid license")
                raise ValueError("Web Filtering Status shows UP in case of Invalid license")
            if not match_alarm:
                device.log(
                    level="ERROR",
                    message="Web filtering alarm not active in case of Invalid license")
                raise ValueError("Web filtering alarm not active in case of Invalid license")
        else:
            if not match:
                device.log(
                    level="ERROR",
                    message="Web Filtering Status does not show UP in case of Valid license")
                raise ValueError("Web Filtering Status does not show UP in case of Valid license")
            if match_alarm:
                device.log(
                    level="ERROR",
                    message="Web filtering alarm active in case of valid license")
                raise ValueError("Web filtering alarm active in case of valid license")

    elif utm_feature == "anti-spam":
        alarm_status = device.cli(command="show system alarms").response()
        match_alarm = re.search(".*Anti-Spam usage requires a license.*", alarm_status, re.DOTALL)
        if license_valid is False:
            if not match_alarm:
                device.log(
                    level="ERROR",
                    message="Anti-spam alarm not active in case of Invalid license")
                raise ValueError("Anti-spam alarm not active in case of Invalid license")
        else:
            if match_alarm:
                device.log(level="ERROR", message="Anti-spam alarm active in case of valid license")
                raise ValueError("Anti-spam alarm active in case of valid license")

    else:
        device.log(level="ERROR", message="Invalid utm_feature name")
        raise ValueError("Invalid utm_feature name")

    if license_valid:
        msg = " Feature verified for Valid License"
    else:
        msg = " Feature verified for Invalid License"
    device.log(level="INFO", message=utm_feature + msg)
    return True
