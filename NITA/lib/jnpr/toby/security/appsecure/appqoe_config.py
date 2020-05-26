"""
Appqoe config keywords

Keywords written for
1: configure_sla_rule
2: configure_active_probe_params
3: configure_sla_options
4: configure_probe_path
5: configure_overlay_path
6: configure_metrics_profile
"""
__author__ = ['Sharanagoud B D']
__contact__ = ''
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2018'

from jnpr.toby.hldcl.device import Device
from jnpr.toby.init.init import init
from jnpr.toby.hldcl.juniper.security.srx import Srx


"""
Advance policy based routing(APBR) SLA Rule Configuration
"""


def configure_sla_rule(device=None, mode="set", commit=True, **kwargs):
    """
    Configure the Advance policy based routing(APBR) SLA Rule

    Example:

        configure_sla_rule(device=dh, sla_rule="sla1", metrics_profile="profile1",
                            sampling_percentage="5", sampling_period="1000",
                            sla_export_interval="60", violation_count="10",
                            switch_idle_time="60", active_probe_params=probe1)

        configure_sla_rule(device=dh, sla-rule="sla1", mode="delete", commit=False)

        #To configure only passive probing
        apbr_obj = configure_sla_rule(dev_obj, sla_rule='sla_rule1',metrics_profile='profile1',
        active_probe_params='probe1', switch_idle_time="10")

        #To configure passive probing and all other probe params
        apbr_obj = configure_sla_rule(dev_obj, sla_rule='sla_rule1',metrics_profile='profile1',
        sampling_percentage="5", sampling_period="2000",sla_export_factor="10",
        violation_count="10", switch_idle_time="10", active_probe_params='probe1')

    ROBOT Example:

        Configure Sla Rule   device=${dh}   sla_rule=sla1   metrics_profile=profile1
                sampling_percentage=5   sampling_period=1000
                  violation_count=10    switch_idle_time=10     passive_probing=probe1

        Configure Sla Rule   device=${dh}   sla_rule=sla_rule1   mode=delete   commit=${False}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str sla_rule:
        **REQUIRED** Advance policy based routing(APBR) Sla rule name
    :param str metrics_profile:
        **REQUIRED** Advance policy based routing(APBR) metric profiles
    :param str passive_probe_params:
        **REQUIRED** Advance policy based routing(APBR) Passive probe params
    :param str active_probe_params:
        **REQUIRED** Advance policy based routing(APBR) Active probe params
    :param str sampling_percentage:
        **OPTIONAL** Min percentage of sessions to be evaluated for an app for passive probing
    :param str sampling_period:
        **OPTIONAL** Time period in which the sampling is done for passive probing
    :param str sla_export_factor:
        **OPTIONAL** Enable time based SLA exporting for passive probing
    :param str violation_count:
        **OPTIONAL** Number of SLA violations within sampling period to be considered as a violation
    :param str switch_idle_time:
        **OPTIONAL** Idle timeout period where no SLA violation will be detected 
        once path switch has happened
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: "True" or "False"
        ``Default value``   : "True"
    :param str mode:
        *OPTIONAL* Set or Delete mode
        ``Supported values``: "set" or "delete"
        ``Default value``   : "set"
    :return: True if successful
    :rtype bool
    """

    #Initialize variables.
    metrics_profile = kwargs.get('metrics_profile', None)
    passive_probe_params = kwargs.get('passive_probe_params', "1")
    active_probe_params = kwargs.get('active_probe_params', None)
    sampling_percentage = kwargs.get('sampling_percentage', None)
    sampling_period = kwargs.get('sampling_period', None)
    sla_export_factor = kwargs.get('sla_export_factor', None)
    violation_count = kwargs.get('violation_count', None)
    switch_idle_time = kwargs.get('switch_idle_time')
    probe_type = kwargs.get('probe_type', "book-ended")
    sla_rule = kwargs.get('sla_rule')
    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    if sla_rule is None:
        device.log(level="ERROR", message="SLA rule name is a mandatory argument")
        raise ValueError("SLA rule name is a mandatory argument")

    if mode == "set":
        if metrics_profile is None:
            device.log(level="ERROR", message="Metrics profile is a mandatory argument")
            raise ValueError("Metrics profile is a mandatory argument")

        #if passive_probe_params is None:
        #    device.log(level="ERROR", message="Passive probe params is a mandatory argument")
        #   raise ValueError("Passive probe params is a mandatory argument")

        if active_probe_params is None:
            device.log(level="ERROR", message="Active probe params is a mandatory argument")
            raise ValueError("Active probe params is a mandatory argument")

    cmdlist = []
    base_cmd = mode + " security advance-policy-based-routing sla-rule " + sla_rule

    if kwargs.get('metrics_profile') is not None:
        metrics_cmd = base_cmd + " metrics-profile " + metrics_profile
        cmdlist.append(metrics_cmd)

    if kwargs.get('active_probe_params') is not None:
        metrics_cmd = base_cmd + " active-probe-params " + active_probe_params
        cmdlist.append(metrics_cmd)

    if kwargs.get('switch_idle_time') is not None:
        cmdlist.append(base_cmd + " switch-idle-time " + switch_idle_time)

    if passive_probe_params is not  None:
        passive_probe_cmd = base_cmd + ' passive-probe-params '
        cmdlist.append(passive_probe_cmd)
        if kwargs.get('sampling_percentage') is not None:
            cmdlist.append(passive_probe_cmd + ' sampling-percentage  ' + sampling_percentage)

        if kwargs.get('sampling_period') is not None:
            cmdlist.append(passive_probe_cmd + ' sampling-period ' + sampling_period)

        if violation_count is not None:
            cmdlist.append(passive_probe_cmd + ' violation-count ' + violation_count)

        if sla_export_factor is not None:
            cmdlist.append(passive_probe_cmd + ' sla_export_factor ' + sla_export_factor)

        if probe_type is not None:
            cmdlist.append(passive_probe_cmd + ' type ' + probe_type)

    if len(cmdlist) == 0 and mode == "delete":
        cmdlist.append(base_cmd)

    #configure and commit the configuration.
    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()

    return True


"""
Advance policy based routing(APBR) Active Probe Params
"""

def configure_active_probe(device=None, probe_params=None, mode="set", commit=True, **kwargs):
    """
    Configure the Advance policy based routing(APBR) Active probe params

    Example:

        configure_active_probe(device=dh, probe_params="probe1",  data_fill="juniper",
                            data_size="100", probe_interval="5",
                            probe_count="10", burst_size="10",
                            sla_export_interval="60", dscp_code_points="000110")

        configure_active_probe(device=dh, probe_params="probe_params1", mode="delete", commit=False)

    ROBOT Example:

        Configure Active Probe Params   device=${dh}   probe_params=probe_params1
                data_fill=juniper    data_size=100
                probe_interval=5    probe_count=10
                burst_size=10    sla_export_interval=60    dscp_code_points=000110

        Configure Active Probe Params   device=${dh}   probe_params=probe_params1 
        ...   mode=delete   commit=${False}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str probe-params:
        **REQUIRED** Advance policy based routing(APBR) Active Probe Params
    :param str data-fill:
        **OPTIONAL** Probe Data Payload content
    :param str data-size:
        **OPTIONAL** Probe data size
    :param str probe-interval:
        **OPTIONAL** Enable time based SLA exporting for passive probing
    :param str probe-count:
        **OPTIONAL** Minimum number of samples to be collected to evaluate SLA measurement
    :param str burst-size:
        **OPTIONAL** Number of probes out of probe count to be sent as a burst
    :param str sla-export-interval:
        **OPTIONAL** Enabled time based SLA exporting
    :param str dscp-code-points:
        **OPTIONAL** Mapping of code point aliases to bit strings
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: "True" or "False"
        ``Default value``   : "True"
    :param str mode:
        *OPTIONAL* Set or Delete mode
        ``Supported values``: "set" or "delete"
        ``Default value``   : "set"
    :return: True if successful
    :rtype bool
    """

    #Initialize variables.
    data_fill = kwargs.get('data_fill', None)
    data_size = kwargs.get('data_size', None)
    probe_interval = kwargs.get('probe_interval', None)
    probe_count = kwargs.get('probe_count', None)
    burst_size = kwargs.get('burst_size', None)
    sla_export_interval = kwargs.get('sla_export_interval', None)
    dscp_code_points = kwargs.get('dscp_code_points', None)

    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    if probe_params is None:
        device.log(level="ERROR", message="Active probe setting name is mandatory")
        raise ValueError("Active probe setting name is mandatory")
    if data_fill is None:
        device.log(level="ERROR", message="Data fill is mandatory")
    if data_size is None:
        device.log(level="ERROR", message="Data size is mandatory")

    cmdlist = []
    base_cmd = mode + " security advance-policy-based-routing active-probe-params " + probe_params

    if probe_params is not None:
        probe_params_settings = base_cmd
        cmdlist.append(probe_params_settings)

        if kwargs.get('data_fill') is not None:
            cmdlist.append(probe_params_settings + ' settings ' + ' data-fill  ' \
                    + kwargs.get('data_fill'))

        if kwargs.get('data_size') is not None:
            cmdlist.append(probe_params_settings + ' settings ' + ' data-size '\
                    + kwargs.get('data_size'))

        if probe_interval is not None:
            cmdlist.append(probe_params_settings + ' settings ' + ' probe-interval '\
                    + probe_interval)

        if probe_count is not None:
            cmdlist.append(probe_params_settings + ' settings ' + ' probe-count '\
                    + probe_count)

        if burst_size is not None:
            cmdlist.append(probe_params_settings + ' settings ' + ' burst-size '\
                    + burst_size)

        if sla_export_interval is not None:
            cmdlist.append(probe_params_settings + ' settings ' + ' sla-export-interval '\
                    + sla_export_interval)

        if dscp_code_points is not None:
            cmdlist.append(probe_params_settings + ' settings ' + ' dscp-code-points '\
                    + dscp_code_points)

    if len(cmdlist) == 0 and mode == "delete":
        cmdlist.append(base_cmd)

    #configure and commit the configuration.
    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()

    return True

"""
Advance policy based routing(APBR) SLA Options
"""


def configure_sla_options(device=None, mode="set", commit=True, **kwargs):
    """
    Configure the Advance policy based routing(APBR) Active probe params

    Example:

        configure_sla_options(device=dh, sla_options=1,
                            local_route_switch="enabled")

        configure_sla_options(device=dh, sla_options=1,
                            local_route_switch="disabled")

        configure_sla_options(device=dh, sla_options=1, mode="delete", commit=False)

    ROBOT Example:

        Configure Sla Options   device=${dh}   sla_options=1
                local_route_switch=enabled

        Configure Sla Options   device=${dh}   sla_options=1   mode=delete   commit=${False}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str sla-options:
        **REQUIRED** Advance policy based routing(APBR) Global SLA options
    :param str local-route-switch:
        **OPTIONAL** Enable/disable Automatic local route switching
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: "True" or "False"
        ``Default value``   : "True"
    :param str mode:
        *OPTIONAL* Set or Delete mode
        ``Supported values``: "set" or "delete"
        ``Default value``   : "set"
    :return: True if successful
    :rtype bool
    """
    #Initialize variables.
    sla_options = kwargs.get('sla_options', 1)
    local_route_switch = kwargs.get('local_route_switch', None)

    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    cmdlist = []
    base_cmd = mode + " security advance-policy-based-routing "

    if sla_options == 1:
        sla_options_cmd = base_cmd + ' sla-options '
        cmdlist.append(sla_options_cmd)
        if local_route_switch is not None:
            cmdlist.append(sla_options_cmd + ' local-route-switch  ' + local_route_switch)

    if len(cmdlist) == 0 and mode == "delete":
        cmdlist.append(base_cmd + ' sla-options ')

    #configure and commit the configuration.
    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()

    return True


"""
Advance policy based routing(APBR) Metrics profile
"""


def configure_metrics_profile(device=None, metrics_profile=None, mode="set", commit=True, **kwargs):
    """
    Configure the Advance policy based routing(APBR) Metrics Profile

    Example:

        configure_metrics_profile(device=dh, metrics_profile="metric1", delay_round_trip="10000",
        jitter="1000", jitter_type="ingress-jitter/egress-jitter/two-way-jitter",
        match="all/any", packet_loss="5")

        configure_metrics_profile(device=dh, metrics_profile="metric1", mode="delete", commit=False)

    ROBOT Example:

        Configure Metrics Profile   device=${dh}   metrics_profile=metric1   delay_round_trip=10000
                jitter=1000   jitter_type=two-way-jitter
                match=all     packet_loss=5

        Configure Metrics Profile   device=${dh}   metrics_profile=metrics_profile1
        ...   mode=delete   commit=${False}

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str metrics-profile:
        **REQUIRED** Advance policy based routing(APBR) metric profiles
    :param str delay_round_trip:
        **OPTIONAL** Maximum acceptable delay
    :param str jitter:
        **OPTIONAL** Maximum acceptable jitter
    :param str jitter_type:
        **OPTIONAL** Type of Jitter
    :param str match:
        **OPTIONAL** Type of SLA match/Default is all
    :param str packet_loss:
        **OPTIONAL** Maximum acceptable packet-loss
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: "True" or "False"
        ``Default value``   : "True"
    :param str mode:
        *OPTIONAL* Set or Delete mode
        ``Supported values``: "set" or "delete"
        ``Default value``   : "set"
    :return: True if successful
    :rtype bool
    """
    #Initialize variables.
    delay_round_trip = kwargs.get('delay_round_trip', None)
    jitter = kwargs.get('jitter', None)
    jitter_type = kwargs.get('jitter_type', None)
    match = kwargs.get('match', None)
    packet_loss = kwargs.get('packet_loss', None)

    if device is None:
        raise ValueError("Device handle is a mandatory argument")

    if metrics_profile is None:
        device.log(level="ERROR", message="Metrics profile is a mandatory argument")
        raise ValueError("Metrics profile is a mandatory argument")

    cmdlist = []
    base_cmd = mode + " security advance-policy-based-routing metrics-profile " + metrics_profile

    if delay_round_trip is not None:
        cmdlist.append(base_cmd + ' sla-threshold ' + ' delay-round-trip  ' + delay_round_trip)

    if jitter is not None:
        cmdlist.append(base_cmd + ' sla-threshold ' + ' jitter ' + jitter)

    if jitter_type is not None:
        cmdlist.append(base_cmd + ' sla-threshold ' + ' jitter-type ' + jitter_type)

    if match is not None:
        cmdlist.append(base_cmd + ' sla-threshold ' + ' match ' + match)

    if packet_loss is not None:
        cmdlist.append(base_cmd + ' sla-threshold ' + ' packet-loss ' + packet_loss)

    if len(cmdlist) == 0 and mode == "delete":
        cmdlist.append(base_cmd)

    #configure and commit the configuration.
    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()

    return True

#if __name__ == '__main__':
#    srx = Device(host="10.209.82.220", os="JUNOS", connect_mode="ssh", user="root", password="Embe1mpls")
#    configure_metrics_profile(device=srx, delay_round_trip="20000", jitter="100000", jitter_type="ingress-jitter", match="all")
