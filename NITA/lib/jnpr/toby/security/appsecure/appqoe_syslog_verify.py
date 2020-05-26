"""
    APPQOE sysylog verification keywords
"""
__author__ = ['Sharanagoud B D']
__contact__ = ''
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2018'

from jnpr.toby.utils.linux.syslog_utils import check_syslog
from jnpr.toby.hldcl.device import Device
from jnpr.toby.init.init import init
from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.utils.iputils import normalize_ipv6
import re
import time
import jxmlease

"""
To verify APPQOE logging
"""

def validate_appqoe_metric_syslog(device=None, message=None, file="/var/log/messages", **kwargs):
    """
    To validate Appqoe metric syslog
    Example:
        validate_appqoe_metric_syslog(dev_obj, message="ACTIVE", syslog_mode="structured",
                                file="/var/tmp/syslog_test.txt", source_address="19.0.0.2", source_port="46965",
                                destination_address="9.0.0.2", destination_port="22", destination_interface="gr-0/0/0.0")

        validate_appqoe_metric_syslog(dev_obj, message="PASSIVE", syslog_mode="structured",
                                file="/var/tmp/syslog_test.txt", source_address="19.0.0.2", source_port="46965",
                                destination_address="9.0.0.2", destination_port="22", destination_interface="gr-0/0/0.0")

    ROBOT Example:
        Validate Appqoe Metric Syslog    device=${spoke}    message=ACTIVE     syslog_mode=structured
        ...  source_address=19.0.0.2  destination_address=9.0.0.2  destination_group_name=site1
        ...  active_probe_params=probe2    routing_instance=appqoe-vrf  application=UDP    ip_dscp=0

        Validate Appqoe Metric Syslog    device=${spoke}    message=PASSIVE    syslog_mode=structured
        ...  source_address=19.0.0.2    destination_address=9.0.0.2  apbr_rule=rule2    application=HTTP
        ...  source_zone=trust    destination_zone=untrust1    protocol_id=6  apbr_profile=apbr1
        ...  routing_instance=appqoe-vrf    sla_rule=sla3    ip_dscp=0  active_probe_params=probe3
        ...  destination_group_name=site1    destination_port=300

    :param Device device:
        **REQUIRED** Device handle of the syslog server.
    :param bool negate:
        *OPTIONAL* Argument to validate absence of a particular "message"
    :param str message:
        **REQUIRED** Apptrack log message which is expected
        ``Supported values``:   "PASSIVE"
                                "ACTIVE"
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
    :param str service_name:
        *OPTIONAL* Service name
    :param str application:
    `   *OPTIONAL* Application name
    :param str nested_application:
        *OPTIONAL* Nested Application name
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
    :param str monitoring_time:
        *OPTIONAL* Monitoring time
    :param str username:
        *OPTIONAL* Username
    :param str roles:
        *OPTIONAL* Roles
    :param str ip_dscp:
        *OPTIONAL* IP DSCP value
    :param str syslog_src_ip:
        *OPTIONAL* IP address from where Syslog is generated.
    :param str profile_name:
        *OPTIONAL* Profile Name
    :param str rule_name:
        *OPTIONAL Rule Name
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
    :param str ingress_jitter:
        *OPTIONAL* Ingress Jitter measured
    :param str egress_jitter:
        *OPTIONAL* Egress Jitter measured
    :param str rtt_jitter:
        *OPTIONAL* Rtt jitter measured
    :param str rtt:
        *OPTIONAL* RTT measured
    :param str pkt_loss:
        *OPTIONAL Packet loss measured
    :param str destination_group_name:
        *OPTIONAL* Destination Group Name
    :param str sla_rule:
        *OPTIONAL* LSA rule name
    :param str active_probe_params:
        *OPTIONAL Active Probe Name
    :param str get:
        *OPTIONAL* To get the syslog

    :return: Boolean (True or False)
    :rtype: bool
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
    application = kwargs.get('application', ".*")
    protocol_id = kwargs.get('protocol_id', "[0-9]*")
    destination_zone = kwargs.get('destination_zone', "untrust1")
    session_id = kwargs.get('session_id', "[0-9]*")
    packets_from_client = kwargs.get('packets_from_client', "[0-9]*")
    bytes_from_client = kwargs.get('bytes_from_client', "[0-9]*")
    packets_from_server = kwargs.get('packets_from_server', "[0-9]*")
    bytes_from_server = kwargs.get('bytes_from_server', "[0-9]*")
    rtt = kwargs.get('rtt', "[0-9]*")
    syslog_src_ip = kwargs.get('syslog_src_ip', None)
    syslog_mode = kwargs.get('syslog_mode', "*")
    count = kwargs.get('count', None)
    reason = kwargs.get('reason', ".*")
    destination_interface = kwargs.get('destination_interface', ".*")
    routing_instance = kwargs.get('routing_instance', ".*")
    ip_dscp = kwargs.get('ip_dscp', "[0-9]*")
    ingress_jitter = kwargs.get('ingress_jitter', "[0-9]*")
    egress_jitter = kwargs.get('egress_jitter', "[0-9]*")
    rtt_jitter = kwargs.get('rtt_jitter', "[0-9]*")
    monitoring_time = kwargs.get('monitoring_time', "[0-9]*")
    active_probe_params = kwargs.get('active_probe_params', ".*")
    pkt_loss = kwargs.get('pkt_loss', ".*")
    apbr_profile = kwargs.get('apbr_profile', ".*")
    apbr_rule = kwargs.get('apbr_rule', ".*")
    group_name = kwargs.get('group_name', ".*")
    service_name = kwargs.get('service_name', ".*")
    source_zone = kwargs.get('source_zone', ".*")
    session_id = kwargs.get('session_id', "[0-9]*")
    username = kwargs.get('username', ".*")
    roles = kwargs.get('roles', ".*")
    sla_rule = kwargs.get('sla_rule', ".*")
    destination_group_name = kwargs.get('destination_group_name', ".*")
    nested_application = kwargs.get('nested_application', ".*")
    get = int(kwargs.get('get', 0))

    nat_source_address = ''
    nat_source_port = ''
    nat_destination_address = ''
    nat_destination_port = ''
    src_nat_rule_name = ''
    dst_nat_rule_name = ''
    policy_name = ''
    # Building pattern for Event Mode
    if syslog_mode == "event":
        pattern = ".*" + message + ":\\s*" + source_address + "/" + \
                  source_port + "->" + destination_address + "/" + destination_port + "\\s*" + service_name \
                  + "\\s*" + application + "\\s*" + nested_application + "\\s*" + nat_source_address + \
                  "/" + nat_source_port + "->" + nat_destination_address + "/" + nat_destination_port + \
                  "\\s*" + src_nat_rule_name + "\\s*" + dst_nat_rule_name + "\\s*" + protocol_id + "\\s*" + \
                  policy_name + "\\s*" + source_zone + "\\s*" + destination_zone + "\\s*" + session_id + \
                  "\\s*"

        # Building pattern for Structured Mode
    elif syslog_mode == "structured":
        if message == "ACTIVE":
            message = "APPQOE_ACTIVE_SLA_METRIC_REPORT"
            pattern = ".*" + message + "[^\s]*\\[.*"
            pattern = pattern + "[^\s]*" + "source-address=\"" + source_address + "\"[^\\s]*source-port=\"" \
                      + source_port + "\"[^\\s]*destination-address=\"" + destination_address + "\"[^\\s]*" \
                      + "destination-port=\"" + destination_port + "\"[^\\s]*application=\"UDP\"[^\\s]*protocol-id=\"" + protocol_id \
                      + "\"[^\\s]*destination-zone-name=\"" + destination_zone + "\"[^\\s]*routing-instance=\"" \
                      + routing_instance + "\"[^\\s]*destination-interface-name=\"" + destination_interface + "\"[^\\s]*" \
                      + "ip-dscp=\"" + ip_dscp + "\"[^\\s]*ingress-jitter=\"" + ingress_jitter + "\"[^\\s]*egress-jitter=\"" + egress_jitter \
                      + "\"[^\\s]*rtt-jitter=\"" \
                      + rtt_jitter + "\"[^\\s]*rtt=\"" + rtt + "\"[^\\s]*pkt-loss=\"" \
                      + pkt_loss + "\"[^\\s]*bytes-from-client=\"" + bytes_from_client + "\"[^\\s]*bytes-from-server=\"" + bytes_from_server \
                      + "\"[^\\s]*packets-from-client=\"" \
                      + packets_from_client + "\"[^\\s]*packets-from-server=\"" + packets_from_server \
                      + "\"[^\\s]*monitoring-time=\"" + monitoring_time + "\"[^\\s]*active-probe-params=\"" + active_probe_params \
                      + "\"[^\\s]*destination-group-name=\"" + destination_group_name + "\"[^\\s]*]"

        elif message == "PASSIVE":
            message = "APPQOE_PASSIVE_SLA_METRIC_REPORT"
            pattern = ".*" + message + "[^\\s]*\\[.*"
            pattern = pattern + "[^\\s]*" + "source-address=\"" + source_address + "\"[^\\s]*source-port=\"" \
                      + source_port + "\"[^\\s]*destination-address=\"" + destination_address + "\"[^\\s]*" \
                      + "destination-port=\"" + destination_port + "\"[^\\s]*apbr-profile=\"" + apbr_profile \
                      + "\"[^\\s]*apbr-rule=\"" + apbr_rule + "\"[^\\s]*application=\"" + application \
                      + "\"[^\\s]*nested-application=\"" + nested_application \
                      + "\"[^\\s]*group-name=\"" + group_name + "\"[^\\s]*service-name=\"" + service_name \
                      + "\"[^\\s]*protocol-id=\"" + protocol_id + "\"[^\\s]*source-zone-name=\"" + source_zone \
                      + "\"[^\\s]*destination-zone-name=\"" + destination_zone + "\"[^\\s]*session-id-32=\"" \
                      + session_id + "\"[^\\s]*username=\"" + username + "\"[^\\s]*" \
                      + "roles=\"" + roles + "\"[^\\s]*routing-instance=\"" + routing_instance \
                      + "\"[^\\s]*destination-interface-name=\"" + destination_interface \
                      + "\"[^\\s]*ip-dscp=\"" + ip_dscp + "\"[^\\s]*sla-rule=\"" + sla_rule \
                      + "\"[^\\s]*ingress-jitter=\"" + ingress_jitter \
                      + "\"[^\\s]*egress-jitter=\"" + egress_jitter \
                      + "\"[^\\s]*rtt-jitter=\"" \
                      + rtt_jitter + "\"[^\\s]*rtt=\"" + rtt + "\"[^\\s]*pkt-loss=\"" \
                      + pkt_loss + "\"[^\\s]*bytes-from-client=\"" + bytes_from_client + "\"[^\\s]*bytes-from-server=\"" \
                      + bytes_from_server + "\"[^\\s]*packets-from-client=\"" \
                      + packets_from_client + "\"[^\\s]*packets-from-server=\"" + packets_from_server \
                      + "\"[^\\s]*monitoring-time=\"" + monitoring_time + "\"[^\\s]*active-probe-params=\"" + active_probe_params \
                      + "\"[^\\s]*destination-group-name=\"" + destination_group_name + "\"[^\\s]*]"

        else:
            device.log(level="ERROR", message="'message' received a wrong value")
            raise ValueError("'message' can have 'PASSIVE' or 'ACTIVE' as their value")
        # Invalid Mode Branch
    else:
        device.log(level="ERROR", message="INVALID syslog mode")
        raise Exception("INVALID syslog mode")

    if get:
        device.log(level="INFO", message="In GET state")
        return get_syslog(device=device, pattern=pattern)
    else:
        device.log(level="INFO", message="In Verify state")
        negate = kwargs.get('negate')
        print("value is " + str(negate))
        #import pdb
        #pdb.set_trace()
        if negate == "True":
            return check_syslog(device=device, pattern=pattern, file=file, syslog_src_ip=syslog_src_ip,
                                negate=True, count=count, case_insensitive=True)
        else:
            return check_syslog(device=device, pattern=pattern, file=file, syslog_src_ip=syslog_src_ip,
                                negate=negate, count=count, case_insensitive=True)

def get_syslog(device=None, **kwargs):
    """
         to get syslog matched
    """
    pattern = kwargs.get('pattern', ".*")
    grep_command = "grep -E "
    response = device.shell(command="cat /var/log/messages | " + grep_command + "'" + pattern + "'").response()
    output = response.splitlines()
    if len(output) <= 1:
        device.log(level="ERROR", message="No match in the syslog")
    else:
        if output[1]:
            return output[1]
        else:
            return output[2]


def validate_appqoe_path_violation_syslog(device=None, message=None, file="/var/log/messages", **kwargs):
    """
    To validate Appqoe Syslog messages
    Example:
        validate_appqoe_path_violation_syslog(dev_obj, message="APPQOE_SLA_METRIC_VIOLATION", syslog_mode="structured",
                                file="/var/tmp/syslog_test.txt", source_address="19.0.0.2", source_port="46965",
                                destination_address="9.0.0.2", destination_port="22", destination_interface="gr-0/0/0.0")

        validate_appqoe_path_violation_syslog(dev_obj, message="APPQOE_BEST_PATH_SELECTED", syslog_mode="structured",
                                file="/var/tmp/syslog_test.txt", source_address="19.0.0.2", source_port="46965",
                                destination_address="9.0.0.2", destination_port="22", previous_interface="gr-0/0/0.1")

    ROBOT Example:
        Validate Appqoe Path Violation Syslog     device=${spoke}    message=APPQOE_BEST_PATH_SELECTED    application=HTTP
        ...  ip_dscp=0    syslog_mode=structured    active_probe_params=probe1  destination_group_name=site1
        ...  file=/var/log/messages  sla_rule=sla1    source_address=${client-ipv4}  destination_address=${server-ipv4}
        ...  apbr_profile=apbr1    apbr_rule=rule1    source_zone=trust    destination_zone=untrust1
        ...  routing_instance=appqoe-vrf    nested_application=FACEBOOK-ACCESS

        Validate Appqoe Path Violation Syslog  device=${spoke}  message=APPQOE_SLA_METRIC_VIOLATION  file=/var/log/messages
        ...  source_address=${client-ipv4}    syslog_mode=structured    violation_reason=2
        ...  application=HTTP    nested_application=FACEBOOK-ACCESS    ip_dscp=0    active_probe_params=probe1
        ...  destination_group_name=site1    sla_rule=sla1    source_address=${client-ipv4}    destination_address=${server-ipv4}
        ...  apbr_profile=apbr1    apbr_rule=rule1    source_zone=trust    destination_zone=untrust1
        ...  routing_instance=appqoe-vrf    group_name=web:social-networking    target_jitter=10000    target_rtt=200000
        ...  target_pkt_loss=10    target_jitter_type=1    jitter_violation_count=2    destination_interface=${gre-spoke-int1}
        ...  destination_port=250

    :param Device device:
        **REQUIRED** Device handle of the syslog server.
    :param bool negate:
        *OPTIONAL* Argument to validate absence of a particular "message"
    :param str message:
        **REQUIRED** Appqoe log message which is expected
        ``Supported values``:   "APPQOE_SLA_METRIC_VIOLATION"
                                "APPQOE_BEST_PATH_SELECTED"

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
        ``Supported values``:   "non-structured" & "structured"
    :param int count:
        *OPTIONAL* No. of times the log is expected. If not given, it looks for 1 or more.
    :param str reason:
        *OPTIONAL* Reason mentioned in the syslog
    :return: Boolean (True or False)
    :rtype: bool
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
    apbr_profile = kwargs.get('apbr_profile', ".*")
    apbr_rule = kwargs.get('apbr_rule', ".*")
    application = kwargs.get('application', ".*")
    group_name = kwargs.get('group_name', ".*")
    service_name = kwargs.get('service_name', ".*")
    protocol_id = kwargs.get('protocol_id', "[0-9]*")
    source_zone = kwargs.get('source_zone', "trust")
    destination_zone = kwargs.get('destination_zone', "untrust1")
    session_id = kwargs.get('session_id', "[0-9]*")
    username = kwargs.get('username', ".*")
    roles = kwargs.get('roles', ".*")
    routing_instance = kwargs.get('routing_instance', ".*")
    destination_interface = kwargs.get('destination_interface', ".*")
    ip_dscp = kwargs.get('ip_dscp', "[0-9]*")
    sla_rule = kwargs.get('sla_rule', ".*")
    ingress_jitter = kwargs.get('ingress_jitter', "[0-9]*")
    egress_jitter = kwargs.get('egress_jitter', "[0-9]*")
    rtt_jitter = kwargs.get('rtt_jitter', "[0-9]*")
    rtt = kwargs.get('rtt', "[0-9]*")
    pkt_loss = kwargs.get('pkt_loss', "[0-9]*")
    target_jitter_type = kwargs.get('target_jitter_type', "[0-9]*")
    target_jitter = kwargs.get('target_jitter', "[0-9]*")
    target_rtt = kwargs.get('target_rtt', "[0-9]*")
    target_pkt_loss = kwargs.get('target_pkt_loss', "[0-9]*")
    violation_reason = kwargs.get('violation_reason', "[0-9]*")
    jitter_violation_count = kwargs.get('jitter_violation_count', "[0-9]*")
    pkt_loss_violation_count = kwargs.get('pkt_loss_violation_count', "[0-9]*")
    rtt_violation_count = kwargs.get('rtt_violation_count', "[0-9]*")
    violation_duration = kwargs.get('violation_duration', "[0-9]*")
    bytes_from_client = kwargs.get('bytes_from_client', "[0-9]*")
    bytes_from_server = kwargs.get('bytes_from_server', "[0-9]*")
    packets_from_client = kwargs.get('packets_from_client', "[0-9]*")
    packets_from_server = kwargs.get('packets_from_server', "[0-9]*")
    monitoring_time = kwargs.get('monitoring_time', "[0-9]*")
    elapsed_time = kwargs.get('elapsed_time', "[0-9]*")
    previous_interface = kwargs.get('previous_interface', ".*")
    syslog_mode = kwargs.get('syslog_mode', ".*")
    syslog_src_ip = kwargs.get('syslog_src_ip', None)
    count = kwargs.get('count', None)
    destination_group_name = kwargs.get('destination_group_name', ".*")
    active_probe_params = kwargs.get('active_probe_params', ".*")
    nested_application = kwargs.get('nested_application', ".*")
    get = int(kwargs.get('get', 0))
    reason = kwargs.get('reason', ".*")
    nat_source_address = ''
    nat_source_port = ''
    nat_destination_address = ''
    nat_destination_port = ''
    src_nat_rule_name = ''
    dst_nat_rule_name = ''
    policy_name = ''
    #Building pattern for Event Mode
    if syslog_mode == "event":
        message_suffix = ""
        if "VIOLATION" in message:
            message_suffix = "AppQoE SLA Violation happened"
        elif "BEST" in message:
            message_suffix = "AppQoE Best path selected"
        else:
            device.log(level="INFO", message="INVALID message value")
            raise Exception("INVALID message value")
        ## Remove this reason option here.
        message_suffix = message_suffix + "[^\\s]*" + reason
        if "VIOLATION" not in message:
            message_suffix = message_suffix + ":"

        pattern = ".*" + message + ":[^\\s]*" + message_suffix + "[^\\s]*" + source_address + "/" + \
        source_port + "->" + destination_address + "/" + destination_port + "[^\\s]*" + service_name \
        + "[^\\s]*" + application + "[^\\s]*" + nested_application + "[^\\s]*" + nat_source_address + \
        "/" + nat_source_port + "->" + nat_destination_address + "/" + nat_destination_port + \
        "[^\\s]*" + src_nat_rule_name + "[^\\s]*" + dst_nat_rule_name + "[^\\s]*" + protocol_id + "[^\\s]*" + \
        policy_name + "[^\\s]*" + source_zone + "[^\\s]*" + destination_zone + "[^\\s]*" + session_id + \
        "[^\\s]*"

    #Building pattern for Structured Mode
    elif syslog_mode == "structured":
        message_suffix = ""
        if "APPQOE_SLA_METRIC_VIOLATION" in message:
            message_suffix = "AppQoE SLA Violation happened"
            pattern = ".*" + message + "[^\\s]*\\[.*"

            pattern = pattern + "[^\\s]*" + "source-address=\"" + source_address + "\"[^\\s]*source-port=\"" \
            + source_port + "\"[^\\s]*destination-address=\"" + \
            destination_address + "\"[^\\s]*" + "destination-port=\"" + destination_port + \
            "\"[^\\s]*apbr-profile=\"" + apbr_profile + "\"[^\\s]*apbr-rule=\"" + apbr_rule + \
            "\"[^\\s]*application=\"" + application + "\"[^\\s]*nested-application=\"" + nested_application + \
            "\"[^\\s]*group-name=\"" + group_name + \
            "\"[^\\s]*service-name=\"" + service_name + "\"[^\\s]*protocol-id=\"" + protocol_id + \
            "\"[^\\s]*source-zone-name=\"" + source_zone + "\"[^\\s]*destination-zone-name=\"" + \
            destination_zone + "\"[^\\s]*session-id-32" + "=\"" + session_id + "\"[^\\s]*username=\"" \
            + username + "\"[^\\s]*roles=\"" + roles + "\"[^\\s]*routing-instance=\"" + routing_instance + \
            "\"[^\\s]*destination-interface-name=\"" + destination_interface + "\"[^\\s]*ip-dscp=\"" + \
            ip_dscp + "\"[^\\s]*sla-rule=\"" + sla_rule + "\"[^\\s]*ingress-jitter=\"" + ingress_jitter + \
            "\"[^\\s]*egress-jitter=\"" + egress_jitter + "\"[^\\s]*rtt-jitter=\"" + rtt_jitter + \
            "\"[^\\s]*rtt=\"" + rtt + "\"[^\\s]*pkt-loss=\"" + pkt_loss + "\"[^\\s]*target-jitter-type=\"" + \
            target_jitter_type + "\"[^\\s]*target-jitter=\"" + target_jitter + \
            "\"[^\\s]*target-rtt=\"" + target_rtt + "\"[^\\s]*target-pkt-loss=\"" + target_pkt_loss + \
            "\"[^\\s]*violation-reason=\"" + violation_reason + "\"[^\\s]*jitter-violation-count=\"" + \
            jitter_violation_count + "\"[^\\s]*pkt-loss-violation-count=\"" + pkt_loss_violation_count + \
            "\"[^\\s]*rtt-violation-count=\"" + rtt_violation_count + "\"[^\\s]*violation-duration=\"" + \
            violation_duration + "\"[^\\s]*bytes-from-client=\"" + bytes_from_client + \
            "\"[^\\s]*bytes-from-server=\"" + bytes_from_server + "\"[^\\s]*packets-from-client=\"" + \
            packets_from_client + "\"[^\\s]*packets-from-server=\"" + packets_from_server + \
            "\"[^\\s]*monitoring-time=\"" + monitoring_time \
            + "\"[^\\s]*active-probe-params=\"" + active_probe_params \
            + "\"[^\\s]*destination-group-name=\"" + destination_group_name + "\"[^\\s]*]"

        elif "APPQOE_BEST_PATH_SELECTED" in message:
            message_suffix = "AppQoE Best path selected"
            pattern = ".*" + message + "[^\\s]*\\[.*"

            pattern = pattern + "[^\\s]*" + "source-address=\"" + source_address + "\"[^\\s]*source-port=\"" \
            + source_port + "\"[^\\s]*destination-address=\"" + \
            destination_address + "\"[^\\s]*" + "destination-port=\"" + destination_port + \
            "\"[^\\s]*apbr-profile=\"" + apbr_profile + "\"[^\\s]*apbr-rule=\"" + apbr_rule + \
            "\"[^\\s]*application=\"" + application + "\"[^\\s]*nested-application=\"" + nested_application + \
            "\"[^\\s]*group-name=\"" + group_name + \
            "\"[^\\s]*service-name=\"" + service_name + "\"[^\\s]*protocol-id=\"" + protocol_id + \
            "\"[^\\s]*source-zone-name=\"" + source_zone + "\"[^\\s]*destination-zone-name=\"" + \
            destination_zone + "\"[^\\s]*session-id-32" + "=\"" + session_id + "\"[^\\s]*username=\"" \
            + username + "\"[^\\s]*roles=\"" + roles + "\"[^\\s]*routing-instance=\"" + routing_instance + \
            "\"[^\\s]*destination-interface-name=\"" + destination_interface + "\"[^\\s]*ip-dscp=\"" + \
            ip_dscp + "\"[^\\s]*sla-rule=\"" + sla_rule + "\"[^\\s]*elapsed-time=\"" + elapsed_time + \
            "\"[^\\s]*bytes-from-client=\"" + bytes_from_client + \
            "\"[^\\s]*bytes-from-server=\"" + bytes_from_server + "\"[^\\s]*packets-from-client=\"" + \
            packets_from_client + "\"[^\\s]*packets-from-server=\"" + packets_from_server + \
            "\"[^\\s]*previous-interface=\"" + previous_interface  \
            + "\"[^\\s]*active-probe-params=\""+ active_probe_params \
            + "\"[^\\s]*destination-group-name=\""+ destination_group_name + "\"[^\\s]*reason=\""+ reason + "\"[^\\s]*]"

        else:
            device.log(level="INFO", message="INVALID message value")
            raise Exception("INVALID message value")

    #Invalid Mode Branch
    else:
        device.log(level="ERROR", message="INVALID syslog mode")
        raise Exception("INVALID syslog mode")
    if get == 2:
        # when we grep a syslog from linux vm, response has some special characters. When we split the output using splitlines, output is not parsed properly.
        # To avoid this adding a new keyword to grep syslog from the linux machine
        device.log(level="INFO", message="In GET state")
        return get_syslog_from_linux(device=device, pattern=pattern)
    elif get:
        device.log(level="INFO", message="In GET state")
        return get_syslog(device=device, pattern=pattern)
    else:
        device.log(level="INFO", message="In Verify state")
        negate = kwargs.get('negate')
        print("value is " + str(negate))
        if negate == "True":
            return check_syslog(device=device, pattern=pattern, file=file, syslog_src_ip=syslog_src_ip,
                                negate=True, count=count, case_insensitive=True)
        else:
            return check_syslog(device=device, pattern=pattern, file=file, syslog_src_ip=syslog_src_ip,
                                negate=negate, count=count, case_insensitive=True)



def validate_appqoe_apptrack_syslog(device=None, negate=False, message=None, file="/var/log/messages", **kwargs):
    """
    To validate AppQoE Apptrack Syslog messages
    Example:
        validate_appqoe_apptrack_syslog(device=device_handle, message="CREATE", file="/tmp/abc.txt",
                source_address="2001:1000:1111:2222:3333:4444:5555:6666", source_port="33606",
                destination_address="2002:1000:1111:2222:3333:4444:5555:6666",
                service_name="junos-http", application="HTTP", protocol_id="6", policy_name="1",
                source_zone="untrust1", destination_zone="trust", session_id="13071", encrypted="No")
    ROBOT Example:
        Validate AppQoE Apptrack Syslog   device=${device_handle}   message=CREATE   file=/tmp/abc.txt
                source_address=2001:1000:1111:2222:3333:4444:5555:6666   source_port=33606
                destination_address=2002:1000:1111:2222:3333:4444:5555:6666
                service_name=junos-http   application=HTTP   protocol_id=6   policy_name=1
                source_zone=untrust1   destination_zone=trust   session_id=13071   encrypted=No

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
    source_zone = kwargs.get('source_zone', ".*")
    destination_zone = kwargs.get('destination_zone', ".*")
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
    get = int(kwargs.get('get', 0))

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

    if lsys is True:
        message = message + "_LS"+ ":\\s*" + ".*"

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
            pattern = pattern + "\\s+" + destination_interface
        if "APBR_ZONE_MISMATCH" in message:
            pattern = pattern + "\\s+" + action
        if 'category' in kwargs or 'subcategory' in kwargs:
            pattern = pattern + "\\s+" + category + "\\s+" + subcategory


    # Building pattern for Structured Mode
    elif syslog_mode == "structured":
        pattern = ".*" + message + "[^\s]*\\[.*"

        pattern = pattern + "[^\\s]*" + "source-address=\"" + source_address + "\"[^\\s]*source-port=\"" \
          + source_port + "\"[^\\s]*destination-address=\"" + destination_address + "\"[^\\s]*" + \
          "destination-port=\"" + destination_port + "\"[^\\s]*service-name=\"" + service_name + \
          "\"[^\\s]*application=\"" + application + "\"[^\\s]*nested-application=\"" + nested_application \
          + "\"[^\\s]*nat-source-address=\"" + nat_source_address + "\"[^\\s]*nat-source-port=\"" + \
          nat_source_port + "\"[^\\s]*nat-destination-address=\"" + nat_destination_address + "\"[^\\s]*" \
          + "nat-destination-port=\"" + nat_destination_port + "\"[^\\s]*src-nat-rule-name=\"" + \
          src_nat_rule_name + "\"[^\\s]*dst-nat-rule-name=\"" + dst_nat_rule_name + "\"[^\\s]*protocol-id" \
          + "=\"" + protocol_id + "\"[^\\s]*policy-name=\"" + policy_name + "\"[^\\s]*source-zone-name=\"" \
          + source_zone + "\"[^\\s]*destination-zone-name=\"" + destination_zone + "\"[^\\s]*session-id-32" \
          + "=\"" + session_id + "\"[^\\s]*"

        if "VOL_UPDATE" in message or "CLOSE" in message:
            pattern = pattern + "packets-from-client=\"" + packets_from_client + "\"[^\\s]*" + \
                      "bytes-from-client=\"" + bytes_from_client + "\"[^\\s]*packets-from-server=\"" + \
                      packets_from_server + "\"[^\\s]*bytes-from-server=\"" + bytes_from_server + "\"[^\\s]*" + \
                      "elapsed-time=\"" + elapsed_time + "\"[^\\s]*"

        pattern = pattern + "username=\"" + username + "\"[^\\s]*roles=\"" + roles + "\"[^\\s]*" + \
                  "encrypted=\"" + encrypted + "\""

        if "ROUTE_UPDATE" in message or "APBR_ZONE_MISMATCH" in message or "CLOSE" in message:
            pattern = pattern + "[^\\s]*profile-name=\"" + profile_name + "\"[^\\s]*rule-name=\"" + \
                      rule_name + "\"[^\\s]*routing-instance=\"" + routing_instance + "\""

        if 'destination_interface' in kwargs:
            pattern = pattern + "[^\\s]*destination-interface-name=\"" + destination_interface + "\""
        if "APBR_ZONE_MISMATCH" in message:
            pattern = pattern + "[^\\s]*action=\"" + action + "\""

        if 'category' in kwargs or 'subcategory' in kwargs:
            pattern = pattern + "[^\\s]*category=\"" + category + "\"[^\\s]*subcategory=\"" \
                      + subcategory + "\""

        # Invalid Mode Branch
    else:
        device.log(level="ERROR", message="INVALID syslog mode")
        raise Exception("INVALID syslog mode")

    if get:
        device.log(level="INFO", message="In GET state")
        return get_syslog_close(device=device, pattern=pattern)
    else:
        device.log(level="INFO", message="In Verify state")
        return check_syslog(device=device, pattern=pattern, file=file, syslog_src_ip=syslog_src_ip, negate=negate,
                            count=count, case_insensitive=True)

def get_syslog_close(device=None, **kwargs):
    """  get syslog close """
    pattern = kwargs.get('pattern', ".*")
    grep_command = "grep -E "
    response = device.shell(command="cat /var/log/messages | " + grep_command + "'" + pattern + "'").response()
    output = response.splitlines()
    if len(output) <= 1:
        device.log(level="ERROR", message="No match in the syslog")
    else:
        if output[1]:
            return output[1]
        else:
            return output[2]

def get_syslog_from_linux(device=None, **kwargs):
    """
         to get syslog matched
    """
    pattern = kwargs.get('pattern', ".*")
    grep_command = "grep -E "
    response = device.shell(command="cat /var/log/messages | " + grep_command + "'" + pattern + "'").response()
    output = response.split('RT_FLOW')
    if len(output) <= 1:
        device.log(level="ERROR", message="No match in the syslog")
    else:
        if output[1]:
            return output[1]
        else:
            return output[0]


#if __name__ == '__main__':
#    srx = Device(host="10.209.82.220", os="JUNOS", connect_mode="ssh", user="root", password="Embe1mpls")
#    validate_appqoe_metric_syslog(device=srx, message="ACTIVE", syslog_mode="structured", file="/var/tmp/abc.txt", source_address="3.1.1.2")
