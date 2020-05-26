"""
Python Code for handling ODL Related functions. Code that talks to ODL REST Interface
via HTTP Request commands.

Author(s): Sudhir Akondi (sudhira)

Dependencies:
  * ODL

"""

from lxml import etree

import re, json, requests, time

def mount_junos_device_on_odl(odl_ip, hostname, ip, user="root", password="Embe1mpls",
                              netconf_port=830, auth_user="admin", auth_password="admin",
                              cache_dir_name=""):

    """
    Function to Add a new Junos Device on the ODL. This function forms the necessary http headers,
    content and form data to be sent via a PUT request to the ODL.

    Python Example:
        mount_junos_device_on_odl("10.204.34.121", "porter3c-ae-p1b-ft-03", "10.204.41.77")
        mount_junos_device_on_odl("10.204.34.121", "porter3c-ae-p1b-ft-03", "10.204.41.77", netconf_port=831)

    Robot Example:
        Mount Junos Device On ODL   odl_ip=10.204.34.121   hostname=porter3c-ae-p1b-ft-03  ip=10.204.40.77

    :param str odl_ip:
      **MANDATORY** IP Address / Hostname of the Open DayLight Controller

    :param str hostname:
      **MANDATORY** Hostname of the Junos Device (this will be the name by which ODL will refer to the Device

    :param str ip:
      **MANDATORY** IP Address of the Junos Device

    :param str user:
      **OPTIONAL** Junos Device Login User used for opening an netconf session to the device
                   Default: root

    :param str password:
      **OPTIONAL** Junos Device Login Password used for opening an netconf session to the device
                   Default: Embe1mpls

    :param str auth_user:
      **OPTIONAL** User credentials for the REST request sent to the ODL
                   Default: admin

    :param str auth_user:
      **OPTIONAL** Password for user used in the REST request sent to the ODL
                   Default: admin

    :param str netconf_port:
      **OPTIONAL** TCP Port on which netconf service is running on the Junos Device
                   Default: 830

    :return bool: True on Success, Raises Exception on Failure
 
    """

    t.log("INFO", "Attempting to Mount Junos Device on ODL")

    _data_ = """
<node xmlns="urn:TBD:params:xml:ns:yang:network-topology">
   <node-id>{0}</node-id>
   <host xmlns="urn:opendaylight:netconf-node-topology">{1}</host>
   <port xmlns="urn:opendaylight:netconf-node-topology">{2}</port>
   <username xmlns="urn:opendaylight:netconf-node-topology">{3}</username>
   <password xmlns="urn:opendaylight:netconf-node-topology">{4}</password>
   <tcp-only xmlns="urn:opendaylight:netconf-node-topology">false</tcp-only>
   <schema-cache-directory xmlns="urn:opendaylight:netconf-node-topology">{5}</schema-cache-directory>
   <keepalive-delay xmlns="urn:opendaylight:netconf-node-topology">120</keepalive-delay>
</node>
        """

    try:
        if cache_dir_name == "":
            cache_dir_name = hostname
        _data_ = str.format(_data_, hostname, ip, netconf_port, user, password, cache_dir_name)
        _http_url_ = 'http://%s:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/%s' % (odl_ip, hostname)
        t.log("INFO", "URL: %s" % _http_url_)
        t.log("INFO", "POST data: %s" % _data_)

        res = requests.put(_http_url_, data=_data_,
                           headers={'Content-Type': 'application/xml', 'Accept' : 'application/xml'},
                           auth=(auth_user, auth_password))
        t.log("INFO", "Response Code: %s" % res.status_code)
        t.log("INFO", "Response Content: %s" % res.content)
    except Exception as _exception_:
        raise Exception("mount_junos_device_on_odl: %s : %s" % (type(_exception_), _exception_))

    if res.status_code == 201:
        t.log("INFO", "Device Mounted on ODL successfully. (Response 201: Created)")
        return True
    elif res.status_code == 200:
        t.log("INFO", "(Response 200: OK). Device already mounted on ODL")
        return True
    else:
        raise Exception("Response Code is not 201 while adding new device to ODL")

def unmount_junos_device_on_odl(odl_ip, hostname, auth_user="admin", auth_password="admin"):
    """
    Function to Delete a Junos Device on the ODL. This function forms the necessary http headers,
    content and form data to be sent via a DELETE request to the ODL.

    Python Example:
        unmount_junos_device_on_odl("10.204.34.121", "porter3c-ae-p1b-ft-03")

    Robot Example:
        Unmount Junos Device On ODL   odl_ip=10.204.34.121   hostname=porter3c-ae-p1b-ft-03

    :param str odl_ip:
      **MANDATORY** IP Address / Hostname of the Open DayLight Controller

    :param str hostname:
      **MANDATORY** Hostname of the Junos Device (this will be the name by which ODL will refer to the Device

    :param str auth_user:
      **OPTIONAL** User credentials for the REST request sent to the ODL
                   Default: admin

    :param str auth_user:
      **OPTIONAL** Password for user used in the REST request sent to the ODL
                   Default: admin

    :return bool: True on Success, Raises Exception on Failure

    """
    try:
        t.log("INFO", "Attempting to unmount junos device from ODL")
        _http_url_ = "http://%s:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/%s"  % (odl_ip, hostname)
        t.log("INFO", "Http URL in rest: %s" % _http_url_)
        res = requests.delete(_http_url_, auth=(auth_user, auth_password))
    except Exception as _exception_:
        raise Exception("unmount_junos_device_on_odl: %s : %s" % (type(_exception_), _exception_))

    if res.status_code == 200:
        t.log("INFO", "Device was found on the ODL and deleted")
    elif res.status_code == 404:
        t.log("INFO", "Device was not found on the ODL")
    else:
        raise Exception("Failed to delete device from ODL")

    return True

def get_mount_status_of_junos_device_on_odl(odl_ip, hostname, auth_user="admin", auth_password="admin"):

    """
    Function to get the status of a Junos Device on the ODL. This function forms the necessary http headers,
    content and form data to be sent via a GET request to the ODL.

    Python Example:
        status = get_mount_status_of_junos_device_on_odl("10.204.34.121", "porter3c-ae-p1b-ft-03")

    Robot Example:
        ${status}   Get Mount Status Of Junos Device On ODL   odl_ip=10.204.34.121   hostname=porter3c-ae-p1b-ft-03

    :param str odl_ip:
      **MANDATORY** IP Address / Hostname of the Open DayLight Controller

    :param str hostname:
      **MANDATORY** Hostname of the Junos Device (this will be the name by which ODL will refer to the Device

    :param str auth_user:
      **OPTIONAL** User credentials for the REST request sent to the ODL
                   Default: admin

    :param str auth_user:
      **OPTIONAL** Password for user used in the REST request sent to the ODL
                   Default: admin

    :return str: Status of the Device. Text as returned by the ODL.
    """
    try:

        t.log("INFO", "Attempting to get status of junos device from ODL")
        _http_url_ = "http://%s:8181/restconf/operational/network-topology:network-topology/topology/topology-netconf/node/%s" \
                     % (odl_ip, hostname)
        t.log("INFO", "Http URL in rest: %s" % _http_url_)
        res = requests.get(_http_url_, auth=(auth_user, auth_password))

        if res.status_code == 404:
            raise Exception("Device Not found mounted on ODL. Mount it first. (Response Code: 404)")

        _content_ = res.content
        if isinstance(_content_, bytes):
            _content_ = _content_.decode("utf-8")
        _dict_ = json.loads(_content_)

    except Exception as _exception_:
        raise Exception("get_mount_status_of_junos_device_on_odl: %s : %s" % (type(_exception_), _exception_))

    if 'errors' in _dict_:
        raise Exception("Error in fetching status of Device on ODL: %s" %_dict_['errors']['error'][0]['error-message'])

    try:
        _status_ = _dict_['node'][0]['netconf-node-topology:connection-status']
    except Exception as _exception_:
        raise Exception("Response does not contain error, but doesn't match expected JSON")

    return _status_

def poll_mount_status_of_junos_device_on_odl(odl_ip, hostname, interval=10, until=120, status="connected"):

    """
    Function to poll until the status of a Junos Device on the ODL reaches the expected value

    Python Example:
        status = poll_mount_status_of_junos_device_on_odl("10.204.34.121", "porter3c-ae-p1b-ft-03", until=200, status="connected")

    Robot Example:
        ${status}   Poll Mount Status Of Junos Device On ODL   odl_ip=10.204.34.121   hostname=porter3c-ae-p1b-ft-03  until=${300}

    :param str odl_ip:
      **MANDATORY** IP Address / Hostname of the Open DayLight Controller

    :param str hostname:
      **MANDATORY** Hostname of the Junos Device (this will be the name by which ODL will refer to the Device

    :param str interval:
      **OPTIONAL** Polling interval in seconds
                   Default: 10

    :param str until:
      **OPTIONAL** Maximum Polling time in secnds
                   Default: 120 second

    :return bool: True if the Status reaches expected value within the time period specified by until
    """
    t.log("INFO", "Polling once every %s seconds until %s seconds or till status == %s" % (interval, until, status))

    _timer_ = 1
    while _timer_ <= until:
        t.log("INFO", "Iteration: %s seconds" % _timer_)
        _rx_status_ = get_mount_status_of_junos_device_on_odl(odl_ip=odl_ip, hostname=hostname)
        t.log("INFO", "Expected Status: %s, Received Status: %s" % (status, _rx_status_))
        if status == _rx_status_:
            t.log("INFO", "Reached Status as expected")
            return True

        _timer_ += interval
        time.sleep(interval)

    raise Exception("Timer UP. Status is not equal to %s" % status)

def get_device_capability_list_from_odl(odl_ip, hostname, auth_user="admin", auth_password="admin"):

    """
    Function to get a list of netconf capabilities sent by the Junos Device and as recorded by the ODL

    Python Example:
        cap_list = get_device_capability_list_from_odl("10.204.34.121", "porter3c-ae-p1b-ft-03")

    Robot Example:
        ${cap_list}   Get Device Capability List From ODL   odl_ip=10.204.34.121   hostname=porter3c-ae-p1b-ft-03

    :param str odl_ip:
      **MANDATORY** IP Address / Hostname of the Open DayLight Controller

    :param str hostname:
      **MANDATORY** Hostname of the Junos Device (this will be the name by which ODL will refer to the Device

    :param str auth_user:
      **OPTIONAL** User credentials for the REST request sent to the ODL
                   Default: admin

    :param str auth_user:
      **OPTIONAL** Password for user used in the REST request sent to the ODL
                   Default: admin

    :return bool: List of items that are listed as capabilities of the device
    """
    try:
        t.log("INFO", "Attempting to get capabilities list from junos device from ODL")
        _http_url_ = "http://%s:8181/restconf/operational/network-topology:network-topology/topology/topology-netconf/node/%s" \
                     % (odl_ip, hostname)
        t.log("INFO", "Http URL in rest: %s" % _http_url_)
        res = requests.get(_http_url_, auth=(auth_user, auth_password))
        _content_ = res.content
        t.log("INFO", "Response Code: %s" % res.status_code)
        t.log("INFO", "Response Content: %s" % _content_)
        if isinstance(_content_, bytes):
            _content_ = _content_.decode("utf-8")

        _dict_ = json.loads(_content_)
    except Exception as _exception_:
        raise Exception("get_device_capability_list_from_odl: Fetch Fail: %s : %s" % (type(_exception_), _exception_))

    if 'errors' in _dict_:
        raise Exception("Error in fetching status of Device on ODL: %s" %_dict_['errors']['error'][0]['error-message'])

    _cap_list_ = []
    try:
        _caps_ = _dict_['node'][0]['netconf-node-topology:available-capabilities']['available-capability']
        for _c_ in _caps_:
            t.log("INFO", "Array Element: %s" % _c_)
            #_cap_list_.append(_c_['capability'])
            _cap_list_.append(_c_)
    except Exception as _exception_:
        raise Exception("get_device_capability_list_from_odl: Parse Fail: %s : %s" % (type(_exception_), _exception_))

    return _cap_list_

def execute_rpc_from_odl(odl_ip, hostname, yang_name, rpc, args_dict, input_format="json",
                         auth_user="admin", auth_password="admin", input_present_for_rpc=False):

    """
    Python function to execute an RPC from the ODL. This is done by sending a REST POST request to the ODL
    with the necessary details of rpc, yang name etc as a REST request

    Python Example:
        rpc = "get-virtual-network-functions-information"
        yang_name = "junos-rpc-virtual-network-functions"
        args = { "vnf-name" : "vjunos0" }
        response = execute_rpc_from_odl(odl_ip="10.204.43.121", hostname="porter3c-ae-p1b-ft-03",
                                        rpc=rpc, yang_name=yang_name, args_dict=args)

    Robot Example:
        ${rpc}       Set Variable   get-virtual-network-functions-information
        ${yangname}  Set Variable   junos-rpc-virtual-network-functions"
        ${args}      Evaluate       { "vnf-name" : "vjunos0" }
        ${response}  Execute RPC From ODL   odl_ip=10.204.43.121", hostname"porter3c-ae-p1b-ft-03
                     ...                    rpc=${rpc}  yang_name=${yangname}   args_dict=${args}

    :param str odl_ip:
      **MANDATORY** IP Address / Hostname of the Open DayLight Controller

    :param str hostname:
      **MANDATORY** Hostname of the Junos Device (this will be the name by which ODL will refer to the Device

    :param str yang_name:
       **MANDATORY** Name of the Yang Module that contains the RPC definition.
 
    :param str rpc:
       **MANDATORY** XML RPC tag that needs to be executed

    :param str args_dict:
       **MANDATORY** Arguments that are to be sent to the RPC, listed as disctionary with keys and values

    :param str input_format:
        **OPTIONAL** Format of the data that needs to be sent in the Body of the REST Request
                     Only 'json' supported as of now. Code needs to be enhanced to include XML

    :param str auth_user:
      **OPTIONAL** User credentials for the REST request sent to the ODL
                   Default: admin

    :param str auth_user:
      **OPTIONAL** Password for user used in the REST request sent to the ODL
                   Default: admin

    :return str: Text Response as received from the ODL in response to the POST

    """
    try:
        t.log("INFO", "Attempting to execute RPC on a Junos Device from ODL")
        _http_url_ = "http://%s:8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/%s/yang-ext:mount/%s:%s" \
                     %(odl_ip, hostname, yang_name, rpc)
        t.log("INFO", "Http URL in rest: %s" % _http_url_)

        _data_ = None
        if input_present_for_rpc is True:
            _data_ = { "input" : args_dict }
        else:
            _data_ = None

        _content_type_ = "application/%s" % input_format
        _headers_ = {'Content-Type': _content_type_, 'Accept' : 'application/xml'}

        t.log("INFO", "POST data: %s, Type: %s" %(_data_, type(_data_)))
        t.log("INFO", "Headers: %s, Type: %s" %(_headers_, type(_headers_)))

        res = requests.post(_http_url_,
                            json=_data_,
                            headers=_headers_, 
                            auth=(auth_user, auth_password))
        t.log("INFO", "Response Code   : %s" % res.status_code)
        t.log("INFO", "Response Content: %s" % res.content)
    except Exception as _exception_:
        raise Exception("execute_rpc_from_odl: %s : %s" % (type(_exception_), _exception_))

    _return_ = res.content
    if isinstance(_return_, bytes):
        _return_ = _return_.decode("utf-8")

    return _return_

def compare_xml_responses_between_odl_junos(odl_response, junos_response, compare_values=True):

    """
    Compare two XML strings and verify if they are equal. This is implicitly used by other functions
    within the code that needs to compare xml responses of ODL and Junos device
    """

    try:
        t.log("INFO", "Comparing two XML Strings: \n---\n%s\n---\nAND\n---\n%s\n---" %(odl_response, junos_response))
        _odl_xml_ = etree.fromstring(odl_response)
        _odl_xml_ = list(_odl_xml_)[0]
        _junos_xml_ = etree.fromstring(junos_response)
        _junos_xml_ = list(_junos_xml_)[0]
    except Exception as _exception_:
        raise Exception("compare_xml_responses_between_odl_junos: %s : %s" % (type(_exception_), _exception_))

    try:
        _result_ = True
        for _element_1_, _element_2_ in zip( _odl_xml_.iter(), _junos_xml_.iter()):

            # match the tags
            _tag_1_ = _element_1_.tag
            _mt_ = re.match(r"\{.*\}(.*)", _tag_1_)
            t.log("DEBUG", "Checking if tag contains namespace: tag: '%s'" % _tag_1_)
            if _mt_ is not None:
                _tag_1_ = _mt_.group(1)
                t.log("DEBUG", "Namespace found, removed it: tag: '%s'" % _tag_1_)

            _tag_2_ = _element_2_.tag
            _mt_ = re.match(r"\{.*\}(.*)", _tag_2_)
            t.log("DEBUG", "Checking if tag contains namespace: tag: '%s'" % _tag_2_)
            if _mt_ is not None:
                _tag_2_ = _mt_.group(1)
                t.log("DEBUG", "Namespace found, removed it: tag: '%s'" % _tag_2_)

            if _tag_1_ != _tag_2_:
                t.log("ERROR", "Tag-Name : 1 => '%s', 2 => '%s' : MISMATCH" % (_element_1_.tag, _element_2_.tag))
                _result_ = False
            else:
                t.log("DEBUG", "Tag-Name : 1 => '%s', 2 => '%s' : MATCH" % (_element_1_.tag, _element_2_.tag))

            if _element_1_.text is None:
                _text_1_ = ""
            else:
                _text_1_ = _element_1_.text
            
            if _element_2_.text is None:
                _text_2_ = ""
            else:
                _text_2_ = _element_2_.text

            if compare_values is True:
                if _text_1_ != _text_2_:
                    t.log("ERROR", "Tag-Text: 1 => '%s', 2 => '%s' : MISMATCH" % (_text_1_, _text_2_))
                    _result_ = False
                else:
                    t.log("DEBUG", "Tag-Text: 1 => '%s', 2 => '%s' : MATCH" % (_text_1_, _text_2_))
            else:
                t.log("DEBUG", "Tag-Text: 1 => %s, 2 => %s : Skipping Text Match as requested" % (_text_1_, _text_2_))

    except Exception as _exception_:
        raise Exception("compare_xml_responses_between_odl_junos: %s : %s" % (type(_exception_), _exception_))

    if _result_ is False:
        raise Exception("One or more tags / text does not match between the XML strings")

    return True

def find_yang_module_name_for_rpc(device, rpc, yang_files_dir):

    """
    Function to find the yang module that contains the required RPC. This is done by a search within the 
    directory on a Junos device that contains all the yang modules readable format.

    Python Example;
        dh = get_handle(resource=r0)
        yangname = find_yang_module_name_for_rpc(device=dh, rpc='get-virtual-network-functions', yang_files_dir='/var/tmp/rpc-yang')

    Robot Example:
        ${dh}   Get Handle   resource=r0
        ${yang}  Find Yang Module Name for RPC    device=${dh}  rpc=get-virtual-network-functions  yang_files_dir=/var/tmp/rpc-yang
    """
    try:

        _cmd_ = "grep %s %s/*.yang" %(rpc, yang_files_dir)
        _tmp_ = device.shell(command=_cmd_)
        _response_ = _tmp_.response()
 
        _yang_file_name_ = ""
        for _row_ in _response_.split("\n"):
            _mt_ = re.match(r"(\S+):.*", _row_)
            if _mt_ is not None:
                _yang_file_name_ = _mt_.group(1)
                break

        if _yang_file_name_ == "":
            raise Exception("No yang file found under %s with rpc: %s" % (yang_files_dir, rpc))

        _cmd_ = "egrep 'module.*{' %s" % _yang_file_name_
        _tmp_ = device.shell(command=_cmd_)
        _response_ = _tmp_.response()
  
        _yang_module_name_ = ""
        for _row_ in _response_.split("\n"):
            _mt_ = re.match(r"\s+module\s+(\S+)\s+\{.*", _row_)
            if _mt_ is not None:
                _yang_module_name_ = _mt_.group(1)
                break

        if _yang_module_name_ == "":
            raise Exception("No yang module name found under %s with rpc: %s" % (yang_files_dir, rpc))

        return _yang_module_name_

    except Exception as _exception_:
        raise Exception("Exception raised in compare_xml_responses_odl_junos: %s : %s"
                        % (type(_exception_), _exception_))

def is_input_defined_for_rpc(device, rpc, yang_files_dir):
    """
    Function to find the if a specific rpc defined in the yang files, contains an input element or not.
    This function runs by executing commands in a directory on a Junos device that contains all the yang modules
    in readable format.

    Python Example;
        dh = get_handle(resource=r0)
        input_present = is_input_defined_for_rpc(device=dh, rpc='get-virtual-network-functions', yang_files_dir='/var/tmp/rpc-yang')

    Robot Example:
        ${dh}   Get Handle   resource=r0
        ${yang}  Is Input Present For RPC    device=${dh}  rpc=get-virtual-network-functions  yang_files_dir=/var/tmp/rpc-yang
    """
    try:

        _cmd_ = "grep %s %s/*.yang" %(rpc, yang_files_dir)
        _tmp_ = device.shell(command=_cmd_)
        _response_ = _tmp_.response()

        _yang_file_name_ = ""
        for _row_ in _response_.split("\n"):
            _mt_ = re.match(r"(\S+):.*", _row_)
            if _mt_ is not None:
                _yang_file_name_ = _mt_.group(1)
                break

        if _yang_file_name_ == "":
            raise Exception("No yang file found under %s with rpc: %s" % (yang_files_dir, rpc))

        _cmd_ = "egrep 'rpc|input' %s" % _yang_file_name_
        _tmp_ = device.shell(command=_cmd_)
        _response_ = _tmp_.response()

        _input_present_ = False
        _rpc_found_ = False
        for _row_ in _response_.split("\n"):
            _mt_ = re.match(r"\s+rpc\s+(\S+)\s+\{.*", _row_)
            if _mt_ is not None:
                if _mt_.group(1) == rpc:
                    _rpc_found_ = True
                else:
                    _rpc_found_ = False
 
            _mt_ = re.match(r"\s+input\s+\{.*", _row_)
            if _mt_ is not None and _rpc_found_ == True:
                _input_present_ = True
                break

        return _input_present_

    except Exception as _exception_:
        raise Exception("Exception raised in compare_xml_responses_odl_junos: %s : %s"
                        % (type(_exception_), _exception_))

