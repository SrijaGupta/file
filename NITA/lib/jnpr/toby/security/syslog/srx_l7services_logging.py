"""
To verify SSL logging
"""
import re
from jnpr.toby.utils.linux.syslog_utils import check_syslog
from jnpr.toby.utils.iputils import normalize_ipv6

def validate_ssl_proxy_syslog(device=None, negate=False, message=None, file="/var/log/messages",
                              junos_version=None, **kwargs):
    """
    To Validate SSL proxy syslog messages.
    Example:
        validate_ssl_proxy_syslog(device=device_handle,
                      message="revocation_reason:cessation_of_operation", file="/tmp/abc.txt",
                      destination_zone="trust", source_interface="ge-0/0/2.0",
                      syslog_src_ip="4.0.0.254")
        validate_ssl_proxy_syslog(device=device_handle, message="revocation_reason:remove_from_crl",
                      file="/tmp/abc.txt", source_zone="trust", destination_interface="ge-0/0/2.0",
                      nat_source_address="4.0.0.1")

    ROBOT Example:
        Validate SSL proxy syslog   device=${device_handle}
                    message=revocation_reason:cessation_of_operation   file=/tmp/abc.txt
                    destination_zone=trust   source_interface=ge-0/0/2.0   syslog_src_ip=4.0.0.254
        Validate SSL proxy syslog   device=${device_handle}
                    message=revocation_reason:remove_from_crl   file=/tmp/abc.txt
                    source_zone=trust   destination_interface=ge-0/0/2.0
                    nat_source_address=4.0.0.1

    :param Device device:
        **REQUIRED** Device Handle of the Syslog server
    :param str junos_version:
        *OPTIONAL* JunOS version information to support legacy SSL proxy syslog formats
    :param bool negate:
        *OPTIONAL* Argument to validate absence of a particular "message"
    :param str file:
        *OPTIONAL* Syslog logging filename. Default is "/var/log/messages"
    :param str source_address:
        *OPTIONAL* Source IP address (Both IPv4 and IPv6 formats are supported)
    :param str destination_address:
        *OPTIONAL* Destination IP address
    :param str nat_source_address:
        *OPTIONAL* Source NAT'ed IP address
    :param str nat_destination_address:
        *OPTIONAL* Destination NAT'ed IP address
    :param str source_port:
        *OPTIONAL* Source port
    :param str destination_port:
        *OPTIONAL* Destination port
    :param str nat_source_port:
        *OPTIONAL* Source NAT'ed port
    :param str nat_destination_port:
        *OPTIONAL* Destination NAT'ed port
    :param str source_zone:
        *OPTIONAL* Source/From zone
    :param str destination_zone:
        *OPTIONAL* Destination/To zone
    :param str source_interface:
        *OPTIONAL* Source Interface
    :param str destination_interface:
        *OPTIONAL* Destination Interface
    :param int count:
        *OPTIONAL* No. of times the log is expected. If not given, it looks for 1 or more.
    :param str syslog_src_ip:
        *OPTIONAL* IP address from where Syslog is generated.
    :param str message_type:
        *OPTIONAL* SSL message type.
        ``Supported values``:   DROP
                                ALLOW
                                INFO
                                IGNORE
                                WHITELIST
    :param str profile_name:
        *OPTIONAL* SSL Profile name
    :param str session_id:
        *OPTIONAL* Session ID
    :param str logical_system_name:
        *OPTIONAL* Logical system Name. Default is "root-logical-system"
    :param str syslog_mode:
        *OPTIONAL* Syslog mode in which logs are expected. Default is "event"
        ``Supported values``:   "event" & "structured"
    :param str message:
        **REQUIRED** SSL log message which is expected.
        ``Supported values``:
        "revocation_reason:unspecified"         - Server certificate revoked with unspecified code
        "revocation_reason:compromise"          - Server certificate revoked with compromised code
        "revocation_reason:ca_compromise"       - Server certificate revoked with ca compromised
                                                  code
        "revocation_reason:affiliation_changed" - Server certificate revoked with affilation
                                                  changed code
        "revocation_reason:superseded"          - Server certificate revoked with superseded code
        "revocation_reason:cessation_of_operation" - Server certificate revoked with cessation of
                                                     operation code
        "revocation_reason:certificate_hold"    - Server certificate revoked with certificiate on
                                                  hold
        "revocation_reason:"                    - Server certificate revoked with unknown reason
        "revocation_reason:remove_from_crl"     - Server certificate revoked with remove from crl
                                                  code
        "insecure_renegotiation_started"        - Session insecure renegotiation started
        "insecure_renegotiation_completed"      - Session insecure renegotiation completed
        "insecure_renegotiation_not_permitted"  - Session insecure renegotiation not permitted
        "secure_renegotiation_started"          - Session secure renegotiation started
        "secure_renegotiation_completed"        - Session secure renegotiation completed
        "renegotiation_server_cert_different"   - Received different server certificate in
                                                  renegotiation
        "cert_error:self_signed_cert"           - Self signed server certificate
        "cert_error:self_signed_chain_cert"     - Self signed chain server certificate
        "cert_error:subject_issuer_mismatch"    - Subject of the issuer mismatched
        "cert_error:unable_to_get_local_issuer_cert" - Unable to get local issuer certificate
        "whitelist"                             - Whitelisted session. In case of URL whitelisting,
                                                  'sni' or 'url_category', atleast one is mandatory
        "custom"                                - To give a custom message as argument (user
                                                  defined). Argument 'custom_message' is
                                                  mandatory in this case.
    :param str custom_message:
        *OPTIONAL* User defined message. It is mandatory if Argument 'message' = custom.
    :param str sni:
        *OPTIONAL* Server Name identifier
    :param str url_category:
        *OPTIONAL* URL Category
    :return: Boolean (True or False)
    :rtype: bool
    """
    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if message is None:
        device.log(level="ERROR", message="'message' is a mandatory argument")
        raise ValueError("'message' is a mandatory argument")

    logical_system_name = kwargs.get('logical_system_name', "root-logical-system")
    source_address = kwargs.get('source_address', ".*")
    destination_address = kwargs.get('destination_address', ".*")
    nat_source_address = kwargs.get('nat_source_address', ".*")
    nat_destination_address = kwargs.get('nat_destination_address', ".*")
    source_zone = kwargs.get('source_zone', ".*")
    destination_zone = kwargs.get('destination_zone', ".*")
    source_interface = kwargs.get('source_interface', ".*")
    destination_interface = kwargs.get('destination_interface', ".*")
    count = kwargs.get('count', None)
    syslog_src_ip = kwargs.get('syslog_src_ip', None)
    message_type = kwargs.get('message_type', ".*")
    profile_name = kwargs.get('profile_name', ".*")
    source_port = kwargs.get('source_port', "[0-9]*")
    destination_port = kwargs.get('destination_port', "443")
    nat_source_port = kwargs.get('nat_source_port', "[0-9]*")
    nat_destination_port = kwargs.get('nat_destination_port', "443")
    session_id = kwargs.get('session_id', "[0-9]*")
    syslog_mode = kwargs.get('syslog_mode', "event")
    custom_message = kwargs.get('custom_message', None)

    if junos_version is not None:
        device.log(level="ERROR", message="This 'if' branch is for later purposes")
        # CODE FOR LEGACY SSL syslog format
        # Will be Decided upon the JunOs version
        # return the keyword here itself
        return False

    if message_type == "ALLOW" or message_type == "DROP":
        message_type = "SSL_PROXY_SSL_SESSION_" + message_type
    elif message_type == "IGNORE" or message_type == "WHITELIST":
        message_type = "SSL_PROXY_SESSION_" + message_type
    elif message_type == "INFO":
        message_type = "SSL_PROXY_INFO"

    if re.search(".*revocation.*", message, re.DOTALL):
        message_complete = "Certificate\\s*error:CRL:\\s*certificate\\s*revoked\\s*" \
                  "cert-id:crl-ca-profile\\s*"
        if message == "revocation_reason:unspecified":
            message_complete = message_complete + "revocation-reason:0:Unspecified"
        elif message == "revocation_reason:compromise":
            message_complete = message_complete + "revocation-reason:1:Key\\s*Compromise"
        elif message == "revocation_reason:ca_compromise":
            message_complete = message_complete + "revocation-reason:2:CA\\s*Compromise"
        elif message == "revocation_reason:affiliation_changed":
            message_complete = message_complete + "revocation-reason:3:Affiliation\\s*Changed"
        elif message == "revocation_reason:superseded":
            message_complete = message_complete + "revocation-reason:4:Superseded"
        elif message == "revocation_reason:cessation_of_operation":
            message_complete = message_complete + "revocation-reason:5:Cessation\\s*Of\\s*Operation"
        elif message == "revocation_reason:certificate_hold":
            message_complete = message_complete + "revocation-reason:6:Certificate\\s*Hold"
        elif message == "revocation_reason:":
            message_complete = message_complete + "revocation-reason:[0-9]*:.*"
        elif message == "revocation_reason:remove_from_crl":
            message_complete = message_complete + "revocation-reason:8:Remove\\s*From\\s*CRL"
        else:
            device.log(level="ERROR", message="Invalid value of Argument 'message' passed")
            raise ValueError("Invalid value of Argument 'message' passed")

    elif re.search(".*renegotiation.*", message, re.DOTALL):
        message_complete = "ssl:\\s*renegotiation\\s*context\\s*(1):\\s*"
        if message == "insecure_renegotiation_started":
            message_complete = message_complete + "insecure\\s*renegotiation\\s*started"
        elif message == "insecure_renegotiation_completed":
            message_complete = message_complete + "insecure\\s*renegotiation\\s*completed"
        elif message == "secure_renegotiation_started":
            message_complete = message_complete + "secure\\s*renegotiation\\s*started"
        elif message == "secure_renegotiation_completed":
            message_complete = message_complete + "secure\\s*renegotiation\\s*completed"
        elif message == "insecure_renegotiation_not_permitted":
            message_complete = "policy\\s*violation:\\s*insecure\\s*renegotiation\\s*not\\s*" \
                               "permitted"
        elif message == "renegotiation_server_cert_different":
            message_complete = "ssl:\\s*renegotiation\\s*context\\s*(3):\\s*certificate\\s*" \
                               "chain\\s*in\\s*renegotiation\\s*context\\s*different\\s*" \
                               "from\\s*original"
        else:
            device.log(level="ERROR", message="Invalid value of Argument 'message' passed")
            raise ValueError("Invalid value of Argument 'message' passed")

    elif re.search(".*cert_error.*", message, re.DOTALL):
        message_complete = "certificate\\s*error:\\s*"
        if message == "cert_error:self_signed_cert":
            message_complete = message_complete + \
                               "self\\s*signed\\s*certificate\\s*in\\s*certificate\\s*chain"
        elif message == "cert_error:subject_issuer_mismatch":
            message_complete = message_complete + "subject\\s*issuer\\s*mismatch"
        elif message == "cert_error:self_signed_chain_cert":
            message_complete = message_complete + \
                               "renegotiation\\s*context\\s*(1):\\s*self\\s*signed\\s*" + \
                               "certificate\\s*in\\s*certificate\\s*chain"
        elif message == "cert_error:unable_to_get_local_issuer_cert":
            message_complete = message_complete + \
                               "unable\\s*to\\s*get\\s*local\\s*issuer\\s*certificate"
        else:
            device.log(level="ERROR", message="Invalid value of Argument 'message' passed")
            raise ValueError("Invalid value of Argument 'message' passed")

    elif message == "whitelist":
        sni = kwargs.get('sni', ".*")
        url_category = kwargs.get('url_category', ".*")
        if 'sni' not in kwargs and 'url_category' not in kwargs:
            message_complete = "System:\\s*session\\s*whitelisted"
        else:
            message_complete = "session\\s*whitelisted\\s*url\\s*category\\s*match\\s*SNI " + sni +\
                               " URL_CATEGORY " + url_category

    elif message == "custom":
        if custom_message is None:
            device.log(level="ERROR", message="Argument 'custom_message' is mandatory if " + \
                                              "message=custom")
            raise ValueError("Argument 'custom_message' is mandatory if message=custom")
        message_complete = str(custom_message)

    else:
        device.log(level="ERROR", message="Invalid value of Argument 'message' passed")
        raise ValueError("Invalid value of Argument 'message' passed")

    # Building the string
    if syslog_mode == "event":
        pattern = "\\s*" + message_type + ":\\s*lsys:\\s*" + logical_system_name \
        + "\\s*" + session_id + "\\s*<" + source_address + "/" + source_port + "->" + \
        destination_address + "/" + destination_port + ">\\s*NAT:<" + nat_source_address + "/" + \
        nat_source_port + "->" + nat_destination_address + "/" + nat_destination_port + ">\\s*" + \
        profile_name + "\\s*<" + source_zone + ":" + source_interface + "->" + destination_zone + \
        ":" + destination_interface + ">\\s*message:\\s*" + message_complete + "$"

    elif syslog_mode == "structured":
        pattern = "\\s*" + message_type + "\\s*\\[.*logical-system-name=\"" + \
        logical_system_name + "\"\\s*session-id=\"" + session_id + "\"\\s*source-address=\"" \
        + source_address +"\"\\s*source-port=\"" + source_port + "\"\\s*destination-address=\"" \
        + destination_address + "\"\\s*destination-port=\"" + destination_port + \
        "\"\\s*nat-source-address=\"" + nat_source_address +"\"\\s*nat-source-port=\"" + \
        nat_source_port + "\"\\s*nat-destination-address=\"" + nat_destination_address + \
        "\"\\s*nat-destination-port=\"" + nat_destination_port + "\"\\s*profile-name=\"" + \
        profile_name + "\"\\s*source-zone-name=\"" + source_zone + \
        "\"\\s*source-interface-name=\"" + source_interface + "\"\\s*destination-zone-name=\"" + \
        destination_zone + "\"\\s*destination-interface-name=\"" + destination_interface + \
        "\"\\s*message=\"" + message_complete + "\"\\]$"

    else:
        device.log(level="ERROR", message="Invalid value for Argument : syslog_mode")
        raise ValueError("Invalid value for Argument : syslog_mode")

    return check_syslog(device=device, pattern=pattern, file=file, syslog_src_ip=syslog_src_ip,
                        negate=negate, count=count, case_insensitive=True)



def validate_apptrack_syslog(device=None, negate=False, message=None, file="/var/log/messages",
                             **kwargs):
    """
    To validate Apptrack Syslog messages
    Example:
        validate_apptrack_syslog(device=device_handle, message="CREATE", file="/tmp/abc.txt",
                source_address="2001:1000:1111:2222:3333:4444:5555:6666", source_port="33606",
                destination_address="2002:1000:1111:2222:3333:4444:5555:6666",
                service_name="junos-http", application="HTTP", protocol_id="6", policy_name="1",
                source_zone="untrust", destination_zone="trust", session_id="13071", encrypted="No")
    ROBOT Example:
        Validate Apptrack Syslog   device=${device_handle}   message=CREATE   file=/tmp/abc.txt
                source_address=2001:1000:1111:2222:3333:4444:5555:6666   source_port=33606
                destination_address=2002:1000:1111:2222:3333:4444:5555:6666
                service_name=junos-http   application=HTTP   protocol_id=6   policy_name=1
                source_zone=untrust   destination_zone=trust   session_id=13071   encrypted=No

    :param Device device:
        **REQUIRED** Device handle of the syslog server.
    :param bool negate:
        *OPTIONAL* Argument to validate absence of a particular "message"
    :param str message:
        **REQUIRED** Apptrack log message which is expected
        ``Supported values``:   "CREATE"
                                "VOL_UPDATE"
                                "CLOSE"
                                "ROUTE_UPDATE"
                                "APBR_ZONE_CHANGE"
    :param str file:
        *OPTIONAL* Syslog logging filename. Default is "/var/log/messages"
    :param str source_address:
        *OPTIONAL* Source IP address (Both IPv4 and IPv6 formats are supported)
    :param str destination_address
        *OPTIONAL* Destination IP address
    :param str source_port:
        *OPTIONAL* Source Port
    :param str destination_port:
        *OPTIONAL* Destination Port
    :param str nat_source_address:
        *OPTIONAL* Source NAT'ed IP address
    :param str nat_destination_address:
        *OPTIONAL* Destination NAT'ed IP address
    :param str nat_source_port
        *OPTIONAL* Source NAT'ed port
    :param str nat_destination_port:
        *OPTIONAL* Destination NAT'ed port
    :param str service_name:
        *OPTIONAL* Service name
    :param str application:
    `   *OPTIONAL* Application name
    :param str nested_application:
        *OPTIONAL* Nested Application name
    :param str src_nat_rule_name:
        *OPTIONAL* Source NAT Rule name
    :param str dst_nat_rule_name:
        *OPTIONAL* Destination NAT Rule name
    :param str protocol_id:
        *OPTIONAL* Protocol ID
    :param str policy_name:
        *OPTIONAL* Policy name
    :param str source_zone:
        *OPTIONAL* Source/From zone
    :param str destination_zone:
        *OPTIONAL* Destination/To zone
    :param str session_id:
        *OPTIONAL* Session ID
    :param str packets_from_client:
        *OPTIONAL* No. of packets from client
    :param str bytes_from_client:
        *OPTIONAL* Bytes from Client
    :param str packets_from_server:
        *OPTIONAL* Packets from server
    :param str bytes_from_server:
        *OPTIONAL* bytes from server
    :param str elapsed_time:
        *OPTIONAL* Elapsed time
    :param str username:
        *OPTIONAL* Username
    :param str roles:
        *OPTIONAL* Roles
    :param str encrypted:
        *OPTIONAL* Encryption is there or not.
        `Supported values``:    "Yes"
                                "No"
    :param str syslog_src_ip:
        *OPTIONAL* IP address from where Syslog is generated.
    :param str profile_name:
        *OPTIONAL* Profile Name
    :param str rule_name:
        *OPTIONAL Rule Name
    :param str action:
        *OPTIONAL* Action taken
    :param bool lsys:
        *OPTIONAL* Pass True if LSYS mode is there. By default, it is False.
    :param str category:
        *OPTIONAL* Category in APPID
    :param str subcategory:
        *OPTIONAL* Sub Category in APPID
    :param str destination_interface:
        *OPTIONAL* Destination Interface
    :param str routing_instance:
        *OPTIONAL* Name of Routing Instance
    :param str syslog_mode:
        *OPTIONAL* Syslog mode in which logs are expected. Default is "event"
        ``Supported values``:   "event" & "structured"
    :param int count:
        *OPTIONAL* No. of times the log is expected. If not given, it looks for 1 or more.
    :param str reason:
        *OPTIONAL* Reason mentioned in the syslog
    :return: Boolean (True or False)
    :rtype: bool
    :param uplink_interface:
        *OPTIONAL* Uplink interface name in close log
    :param uplink_tx_bytes:
        *OPTIONAL* Uplink Tx bytes in close log
    :param uplink_rx_bytes:
        *OPTIONAL* Uplink Rx bytes in close log
    :param apbr_policy_name:
        *OPTIONAL* sla policy name in close and route update log
    :param wf_category:
        *OPTIONAL* web filtering category in route update log
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")

    if message is None:
        device.log(level="ERROR", message="'message' is a mandatory argument")
        raise ValueError("'message' is a mandatory argument")

    source_address = kwargs.get('source_address', ".*")
    destination_address = kwargs.get('destination_address', ".*")
    source_port = kwargs.get('source_port', "[0-9]*")
    destination_port = kwargs.get('destination_port', "[0-9]*")
    nat_source_address = kwargs.get('nat_source_address', ".*")
    nat_destination_address = kwargs.get('nat_destination_address', ".*")
    nat_source_port = kwargs.get('nat_source_port', "[0-9]*")
    nat_destination_port = kwargs.get('nat_destination_port', "[0-9]*")
    service_name = kwargs.get('service_name', ".*")
    application = kwargs.get('application', ".*")
    nested_application = kwargs.get('nested_application', ".*")
    src_nat_rule_name = kwargs.get('src_nat_rule_name', ".*")
    dst_nat_rule_name = kwargs.get('dst_nat_rule_name', ".*")
    protocol_id = kwargs.get('protocol_id', ".*")
    policy_name = kwargs.get('policy_name', ".*")
    source_zone = kwargs.get('source_zone', "untrust")
    destination_zone = kwargs.get('destination_zone', "trust")
    session_id = kwargs.get('session_id', "[0-9]*")
    packets_from_client = kwargs.get('packets_from_client', "[0-9]*")
    bytes_from_client = kwargs.get('bytes_from_client', "[0-9]*")
    packets_from_server = kwargs.get('packets_from_server', "[0-9]*")
    bytes_from_server = kwargs.get('bytes_from_server', "[0-9]*")
    elapsed_time = kwargs.get('elapsed_time', "[0-9]*")
    username = kwargs.get('username', ".*")
    roles = kwargs.get('roles', ".*")
    encrypted = kwargs.get('encrypted', ".*")
    syslog_src_ip = kwargs.get('syslog_src_ip', None)
    syslog_mode = kwargs.get('syslog_mode', "event")
    count = kwargs.get('count', None)
    reason = kwargs.get('reason', ".*")
    destination_interface = kwargs.get('destination_interface', ".*")
    category = kwargs.get('category', ".*")
    subcategory = kwargs.get('subcategory', ".*")
    lsys = kwargs.get('lsys', False)
    action = kwargs.get('action', ".*")
    profile_name = kwargs.get('profile_name', ".*")
    rule_name = kwargs.get('rule_name', ".*")
    routing_instance = kwargs.get('routing_instance', ".*")
    uplink_interface = kwargs.get('uplink_interface', ".*")
    uplink_tx_bytes = kwargs.get('uplink_tx_bytes', ".*")
    uplink_rx_bytes = kwargs.get('uplink_rx_bytes', ".*")
    apbr_policy_name = kwargs.get('apbr_policy_name', "N/A")
    wf_category = kwargs.get('wf_category', "N/A")
    bypass = kwargs.get('bypass', "N/A")
    src_vrf_grp = kwargs.get('src_vrf_grp', "N/A")
    dst_vrf_grp = kwargs.get('dst_vrf_grp', "N/A")
    dscp_value = kwargs.get('dscp_value', ".*")
    apbr_rule_type = kwargs.get('apbr_rule_type', ".*")
    multipath_rule_name = kwargs.get('multipath_rule_name', ".*")

    # Convert IPv6 compressed format
    if source_address != ".*":
        source_address = normalize_ipv6(source_address, compress_zero=True)
    if destination_address != ".*":
        destination_address = normalize_ipv6(destination_address, compress_zero=True)
    if nat_source_address != ".*":
        nat_source_address = normalize_ipv6(nat_source_address, compress_zero=True)
    if nat_destination_address != ".*":
        nat_destination_address = normalize_ipv6(nat_destination_address, compress_zero=True)


    if message != "APBR_ZONE_MISMATCH":
        message = "APPTRACK_SESSION_" + message

    if lsys is True and syslog_mode == "event":
        message = message + "_LS"+ ":\\s*" + ".*"
    elif lsys is True and syslog_mode == "structured":
        message = message + "_LS"+ "\\s*" + ".*"
    else:
        message = message
    resource_list = t.get_junos_resources()
    dut_name = ''
    for resource in resource_list:
        if t['resources'][resource]['system']['primary'].get('uv-syslog-host', 'False') != 'False':
            dut_name = resource
            break
    dut_handle = t.get_handle(resource=dut_name)
    version = dut_handle.get_version()
    if service_name == 'junos-https':
        if application == 'HTTPS' and float(19.4) <= float(version[:4]) or float(18.2) > float(version[:4]):
            application = application.replace('HTTPS', 'HTTP')
        else:
            if application == 'HTTP' and float(18.2) <= float(version[:4]) <= float(19.3):
                application = application.replace('HTTP', 'HTTPS')

    # Building pattern for Event Mode
    if syslog_mode == "event":
        message_suffix = ""
        if "CLOSE" in message:
            message_suffix = "AppTrack session closed"
        elif "CREATE" in message:
            message_suffix = "AppTrack session created"
        elif "VOL_UPDATE" in message:
            message_suffix = "AppTrack volume update"
        elif "ROUTE_UPDATE" in message:
            message_suffix = "AppTrack route update"
        elif "APBR_ZONE_MISMATCH" in message:
            message_suffix = "APBR zone mismatch"
        else:
            device.log(level="INFO", message="INVALID message value")
            raise Exception("INVALID message value")

        message_suffix = message_suffix + "\\s*" + reason
        if "CREATE" not in message:
            message_suffix = message_suffix + ":"

        pattern = ".*" + message + ":\\s*" + message_suffix + "\\s*" + source_address + "/" + \
        source_port + "->" + destination_address + "/" + destination_port + "\\s*" + service_name \
        + "\\s*" + application + "\\s*" + nested_application + "\\s*" + nat_source_address + \
        "/" + nat_source_port + "->" + nat_destination_address + "/" + nat_destination_port + \
        "\\s*" + src_nat_rule_name + "\\s*" + dst_nat_rule_name + "\\s*" + protocol_id + "\\s*" + \
        policy_name + "\\s*" + source_zone + "\\s*" + destination_zone + "\\s*" + session_id + \
        "\\s*"

        if "VOL_UPDATE" in message or "CLOSE" in message:
            pattern = pattern + packets_from_client + "(" + bytes_from_client + ")" + "\\s*" + \
            packets_from_server + "(" + bytes_from_server + ")" + "\\s*" + elapsed_time + "\\s*"

        pattern = pattern + username + "\\s*" + roles + "\\s*" + encrypted

        if "ROUTE_UPDATE" in message or "ZONE_CHANGE" in message or "CLOSE" in message:
            pattern = pattern + "\\s+" + profile_name + "\\s+" + rule_name + "\\s+" \
                      + routing_instance

        if 'destination_interface' in kwargs:
            if "CLOSE" in message and 'uplink_interface' in kwargs:
                pattern = pattern + "\\s+" + destination_interface + "\\s+" + uplink_interface +  "\\s+" + uplink_tx_bytes +  "\\s" + uplink_rx_bytes + "\\s*"
            else:
                pattern = pattern + "\\s+" + destination_interface + "\\s.*"    

        if "APBR_ZONE_MISMATCH" in message:
            pattern = pattern + "\\s+" + action
        if 'category' in kwargs or 'subcategory' in kwargs:
            pattern = pattern + category + "\\s+" + subcategory
        if "ROUTE_UPDATE" in message or "CLOSE" in message:
            if 'apbr_policy_name' in kwargs or 'wf_category' in kwargs or 'bypass' in kwargs:
                pattern = pattern + "\\s+" + apbr_policy_name
                if ("ROUTE_UPDATE" in message and 'wf_category' in kwargs and 'bypass' in kwargs) or ("ROUTE_UPDATE" in message and 'wf_category' not in kwargs and 'bypass' in kwargs):
                    pattern = pattern + "\\s+" + wf_category + "\\s+" + bypass
                elif "ROUTE_UPDATE" in message and 'wf_category' in kwargs and 'bypass' not in kwargs:
                    pattern = pattern + "\\s+" + wf_category

    # Building pattern for Structured Mode
    elif syslog_mode == "structured":
        pattern = ".*" + message + "\\s*\\[.*"
        if 'reason' in kwargs:
            pattern = pattern + "reason=\"" + reason + "\""

        pattern = pattern + "\\s*" + "source-address=\"" + source_address + "\"\\s*source-port=\"" \
        + source_port + "\"\\s*destination-address=\"" + destination_address + "\"\\s*" + \
        "destination-port=\"" + destination_port + "\"\\s*service-name=\"" + service_name + \
        "\"\\s*application=\"" + application + "\"\\s*nested-application=\"" + nested_application \
        + "\"\\s*nat-source-address=\"" + nat_source_address + "\"\\s*nat-source-port=\"" + \
        nat_source_port + "\"\\s*nat-destination-address=\"" + nat_destination_address + "\"\\s*" \
        + "nat-destination-port=\"" + nat_destination_port + "\"\\s*src-nat-rule-name=\"" + \
        src_nat_rule_name + "\"\\s*dst-nat-rule-name=\"" + dst_nat_rule_name + "\"\\s*protocol-id" \
        + "=\"" + protocol_id + "\"\\s*policy-name=\"" + policy_name + "\"\\s*source-zone-name=\"" \
        + source_zone + "\"\\s*destination-zone-name=\"" + destination_zone + "\"\\s*session-id-32" \
        + "=\"" + session_id + "\"\\s*"

        if "VOL_UPDATE" in message or "CLOSE" in message:
            pattern = pattern + "packets-from-client=\"" + packets_from_client + "\"\\s*" + \
            "bytes-from-client=\"" + bytes_from_client + "\"\\s*packets-from-server=\"" + \
            packets_from_server + "\"\\s*bytes-from-server=\"" + bytes_from_server + "\"\\s*" + \
            "elapsed-time=\"" + elapsed_time + "\"\\s*"

        pattern = pattern + "username=\"" + username + "\"\\s*roles=\"" + roles + "\"\\s*" + \
        "encrypted=\"" + encrypted + "\""

        if "ROUTE_UPDATE" in message or "APBR_ZONE_MISMATCH" in message or "CLOSE" in message:
            pattern = pattern + "\\s*profile-name=\"" + profile_name + "\"\\s*rule-name=\"" + \
            rule_name + "\"\\s*routing-instance=\"" + routing_instance + "\""

        if 'destination_interface' in kwargs:
            if "CLOSE" in message and 'uplink_interface' in kwargs:
                pattern = pattern + "\\s*destination-interface-name=\"" + destination_interface + "\"\\s*uplink-incoming-interface-name=\"" +  uplink_interface + "\"\\s*uplink-tx-bytes=\"" + uplink_tx_bytes + "\"\\s*uplink-rx-bytes=\"" + uplink_rx_bytes + "\\s*"
            else:
                pattern = pattern + "\\s*destination-interface-name=\"" + destination_interface + "\".*"
        if "APBR_ZONE_MISMATCH" in message:
            pattern = pattern + "\\s*action=\"" + action + "\""

        if 'category' in kwargs or 'subcategory' in kwargs:
            if float(version[:4]) >= 18.2:
                subcategory_field = "sub-category"
            else:
                subcategory_field = "subcategory"
            pattern = pattern + "category=\"" + category + "\"\\s*" + subcategory_field + "=\"" + subcategory + "\""

        if "ROUTE_UPDATE" in message or "CLOSE" in message:
            if 'apbr_policy_name' in kwargs or 'wf_category' in kwargs or 'bypass' in kwargs:
                pattern = pattern + "\\s*apbr-policy-name=\"" + apbr_policy_name + "\""
                if ("ROUTE_UPDATE" in message and 'wf_category' in kwargs and 'bypass' in kwargs) or ("ROUTE_UPDATE" in message and 'wf_category' not in kwargs and 'bypass' in kwargs):
                    pattern = pattern + "\\s*webfilter-category=\"" + wf_category + "\"" + "\\s*bypass-status=\"" + bypass + "\""
                elif "ROUTE_UPDATE" in message and 'wf_category' in kwargs and 'bypass' not in kwargs:
                    pattern = pattern + "\\s*webfilter-category=\"" + wf_category + "\""
        if "CLOSE" in message:
            if 'multipath_rule_name' in kwargs:
                pattern = pattern + "\\s*multipath-rule-name=\"" + multipath_rule_name + "\""
        if 'dscp_value' in kwargs and 'apbr_rule_type' in kwargs:
            pattern = pattern + "\\s*src-vrf-grp=\"" + src_vrf_grp + "\"\\s*dst-vrf-grp=\"" + dst_vrf_grp + "\"\\s*dscp-value=\"" + dscp_value + "\"\\s*apbr-rule-type=\"" + apbr_rule_type + "\""

    # Invalid Mode Branch
    else:
        device.log(level="ERROR", message="INVALID syslog mode")
        raise Exception("INVALID syslog mode")

    return check_syslog(device=device, pattern=pattern, file=file, syslog_src_ip=syslog_src_ip,
                        negate=negate, count=count, case_insensitive=True)
