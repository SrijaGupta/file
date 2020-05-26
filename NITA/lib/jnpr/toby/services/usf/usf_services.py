# pylint: disable=undefined-variable
# -*- coding: utf-8 -*-
"""Module contains the Services class for Services methods"""
import copy
import random

from jnpr.toby.utils import iputils
from jnpr.toby.services import utils
from jnpr.toby.services.usf.usf_rutils import usf_rutils

#"""Module contains the Services class for Services methods"""
__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


class usf_services(usf_rutils):
    """Class contains methods to configure and verify usf_services"""

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, **kwargs):
        """Constructor method to update the usf_services instance"""

        self.intf = {}
        self.vlan = {}
        self.sset = {}
        self.sp_intf = {}
        self.svc_intf = {}
        self.data = {}
        self.cmd = None
        self.ptr = None
        self.ch_svc = {}
        self.apps = {}
        self.tg = None
        self.sfw_policy = {}
        self.sfw_rules = {}
        self.rt_opts = {}
        self.fw_filter = {}
        self.appset = {}
        self.rt_inst = {}
        self.tg_sess = None
        self.num_sess = {}

        self.pol_opts = {}
        self.if_ri_map = {}
        #self.intf_ss = None
        #self.sp_ss_map = {}
        #self.if_ss_map = {}
        #self.nat_rule_ss_map = {}
        self.ss_map = {}
        self.ss_map['intf'] = {}
        self.ss_map['spic'] = {}
        self.ss_map['nat_rule_set'] = {}
        self.ss_map['pcp_rules'] = {}
        #self.tg_sess_map = {}
        self.tg_sess_cnt = None
        self.tg_cfg_map = {}
        self.intf_ss = {}

        super(usf_services, self).__init__(**kwargs)


    ##########################################################################
    # Config methods
    ##########################################################################
    def set_service_pic(self, name=None, **kwargs):
        """Configures SP interface and other parameters available for this set command.

        :param string name:
            **REQUIRED** SP interface name

        :param string action:
            **OPTIONAL** Valid values are set, elete, ctivate, eactivate. Default is 'set'

        :param bool count:
           **OPTIONAL** Number of Units/address to be created for scaling config

        :param int unit:
           **OPTIONAL** Unit Number. Default is 0 for intf style and 1 for NH style

        :param int unit_step:
           **OPTIONAL** Unit step. Default is 1

        :param bool inet6:
           **OPTIONAL** Enable family INET6

        :param bool next_hop:
           **OPTIONAL** Configures next hop style

        :param bool options:
           **OPTIONAL** Configures Trace/syslog options

        :param string sl_host:
           **OPTIONAL** Syslog host name. Default is 'local'

        :param string log_prefix:
           **OPTIONAL** Log prefix. Default is 'xxxxxxx'

        :param string trace_flag:
           **OPTIONAL** Trace options <all|event|ipc|media|0>. Default is 'all'.
                When set to None, this option is not configured.

        :param string rsp_primary:
           **OPTIONAL** RSP Primary

        :param string rsp_secondary:
           **OPTIONAL** RSP Secondary

        :param string rsp_peer_ip:
           **OPTIONAL** RSP Peer IP Address

        :param string rsp_local_ip:
           **OPTIONAL** RSP Local Data IP Address

        :param string rsp_rt_inst:
           **OPTIONAL** RSP Routing instance name

        :param int inactive_to_tcp:
           **OPTIONAL** Inactivity timeout period for TCP established sessions (4..86400 seconds)

        :param int inactive_to_asymm_tcp:
           **OPTIONAL** Inactivity timeout period for Asymmetric TCP established
                sessions (4..86400 seconds)

        :param int inactive_to_non_tcp:
           **OPTIONAL** Inactivity timeout period for non-TCP established sessions
                (4..86400 seconds)

        :param int inactive_to:
           **OPTIONAL** Inactivity timeout period for established sessions (4..86400 seconds)

        :param int close_to:
           **OPTIONAL** Timeout period for TCP session tear-down (4..300 seconds)

        :param int open_to:
           **OPTIONAL** Timeout period for TCP session establishment (4..300 seconds)

        :param bool cgn_pic:
           **OPTIONAL** enable CGN on this Pic

        :param int reassembly_to:
           **OPTIONAL** Reassembly timeout (1-60secs)

        :param frag_lmt:
           **OPTIONAL** Fragement limit

        :param int pba_interim_log_interval:
           **OPTIONAL** PBA Interim Logging interval (0, 1800-86400s)

        :param int disable_global_to_override:
           **OPTIONAL** PBA Interim Logging interval (0, 1800-86400s)

        :param int ignore_errs:
           **OPTIONAL** Ignore anomalies or Errors

        :param int sess_lmt:
           **OPTIONAL** Session Limit

        :param int sess_to:
           **OPTIONAL** Session timeout period for established sessions (4..86400 seconds)

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
               set_service_pic(name='ms-0/0/0')
            Robot:
               Set Service Pic  name=ms-0/0/0

        """

        self.fn_checkin("Configuring sevice pic")

        if name is None:
            raise self.MissingMandatoryArgument('name')

        self.sp_intf[name] = {}
        #self.sp_intf[name]['action'] = kwargs.get('action', 'set')
        this = self.ptr = self.sp_intf[name]

        this['unit'] = 1 if 'next_hop' in kwargs and kwargs['next_hop'] else 0

        utils.update_opts_from_args(kwargs,
                                    defaults={
                                        'count': 1, 'action': 'set', 'unit_step': 1,
                                        'log_prefix': name, 'trace_flag': 'all',
                                        'options': True, 'next_hop': False,
                                        'inet': True, 'inet6': True, 'mpls': False,
                                        'sl_host': 'local', 'service_opts': False,
                                        'ams': None, 'ingress_key_list': None,
                                        'egress_key_list': None
                                    }, opts=this)
        ams = this['ams']
        self.cmd = "{} interfaces {}".format(this['action'], name)
        self.cmd_add("description", 'if_descr')

        if this['service_opts']:
            self.cmd = "{} interfaces {} services-options".format(this['action'], name)
            if this['options']:
                if this['trace_flag'] is not None:
                    self.cmd = "{} interfaces {}".format(this['action'], name)
                    self.cmd_add("traceoptions flag", 'trace_flag')
                    self.cmd = "{} interfaces {} services-options".format(this['action'], name)

                self.cmd_add("syslog host {} services any".format(this['sl_host']))
                self.cmd_add("syslog host {} log-prefix {}".format(this['sl_host'],
                                                                   this['log_prefix']))
                if 'sl_src_addr' in this:
                    self.cmd_add("syslog host {} services source-address {}"
                                 .format(this['sl_host'], this['sl_src_addr']))
                self.cmd_add("capture capture-size", 'capture_size')
                self.cmd_add("capture pkt-size", 'pkt_size')
                self.cmd_add("capture logs-per-packet", 'logs_per_packet')
                self.cmd_add("capture max-log-line-size", 'max_log_line_size')

                if 'src_ip' in this and this['src_ip'] is not None:
                    if 'src_wc' in this and this['src_wc'] is not None:
                        self.cmd_add("capture filter source-ip {} wildcard {}"
                                     .format(this['src_ip'], this['src_wc']))
                    else:
                        self.cmd_add("capture filter source-ip {}".format(this['src_ip']))

                if 'sw_sip' in this and this['sw_sip'] is not None:
                    if 'sw_sip_wc' in this and this['sw_sip_wc'] is not None:
                        self.cmd_add("capture filter sw-sip {} wildcard {}"
                                     .format(this['sw_sip'], this['sw_sip_wc']))
                    else:
                        self.cmd_add("capture filter sw-sip {}".format(this['sw_sip']))

                if 'dst_ip' in this and this['dst_ip'] is not None:
                    if 'dst_wc' in this and this['dst_wc'] is not None:
                        self.cmd_add("capture filter destination-ip {} wildcard {}"
                                     .format(this['dst_ip'], this['dst_wc']))
                    else:
                        self.cmd_add("capture filter destination-ip {}".format(this['dst_ip']))

                if 'sw_dip' in this and this['sw_dip'] is not None:
                    if 'sw_dip_wc' in this and this['sw_dip_wc'] is not None:
                        self.cmd_add("capture filter sw-dip {} wildcard {}"
                                     .format(this['sw_dip'], this['sw_dip_wc']))
                    else:
                        self.cmd_add("capture filter sw-dip {}".format(this['sw_dip']))

                self.cmd_add("capture filter sport-range low", 'sport_range_low')
                self.cmd_add("capture filter sport-range high", 'sport_range_high')
                self.cmd_add("capture filter dport-range low", 'dport_range_low')
                self.cmd_add("capture filter dport-range high", 'dport_range_high')
                self.cmd_add("capture filter proto", 'proto')
                self.cmd_add("capture filter flow-type", 'flow_type')

            self.cmd_add("inactivity-asymm-tcp-timeout", 'inactive_to_asymm_tcp')
            self.cmd_add("inactivity-tcp-timeout", 'inactive_to_tcp')
            self.cmd_add("inactivity-non-tcp-timeout", 'inactive_to_non_tcp')
            self.cmd_add("inactivity-timeout", 'inactive_to')
            self.cmd_add("close-timeout", 'close_to')
            self.cmd_add("open-timeout", 'open_to')
            self.cmd_add("cgn-pic", 'cgn_pic', opt='flag')
            self.cmd_add("reassembly-timeout", 'reassembly_to')
            self.cmd_add("fragment-limit", 'frag_lmt')
            self.cmd_add("pba-interim-logging-interval", 'pba_interim_log_interval')
            self.cmd_add("disable-global-timeout-override", 'disable_global_to_override')
            self.cmd_add("ignore-errors", 'ignore_errs')
            self.cmd_add("session-limit rate", 'sess_lmt')
            self.cmd_add("session-timeout", 'sess_to')

            self.cmd_add("tcp-tickles", 'tcp_tickles')
            # End no-services-options

        self.cmd = "{} interfaces {}".format(this['action'], name)
        # Configure Redundancy options
        self.cmd_add("redundancy-options primary", 'rsp_primary')
        self.cmd_add("redundancy-options secondary", 'rsp_secondary')
        self.cmd_add("redundancy-options", 'rsp_mode')
        self.cmd_add("redundancy-options redundancy-peer ipaddress", 'rsp_peer_ip')
        self.cmd_add("redundancy-options redundancy-local data-address", 'rsp_local_ip')
        self.cmd_add("redundancy-options routing-instance", 'rsp_rt_inst')
        self.cmd_add("redundancy-options replication-threshold", 'rep_thr')

        unit = this['unit']
        ingress_key_list = ["source-ip"]
        egress_key_list = ["destination-ip"]
        if not this['ingress_key_list']:    this['ingress_key_list'] = ingress_key_list
        if not this['egress_key_list']:    this['egress_key_list'] = egress_key_list

        for _ii in range(1, this['count'] + 1):
            self.cmd = "{} interfaces {} unit {}".format(this['action'], name, unit)
            #self.cmd_add("ip-address-owner service-plane", 'ip_ownr_sp', opt='flag')

            if this['next_hop']:
                self.cmd_add("family inet", 'inet', opt='flag')
                self.cmd_add("family inet6", 'inet6', opt='flag')
                if this['ams']:
                    self.cmd = "{} interfaces".format(this['action'])
                    ams_cmd = "{} unit {} service-domain inside".format(ams, unit)
                    self.cmd_add(ams_cmd)
                    for ingress_key in this['ingress_key_list']:
                        ams_cmd = "{} unit {} load-balancing-options hash-keys ingress-key {}".format(ams, unit, ingress_key)
                        self.cmd_add(ams_cmd)
                else:
                    self.cmd_add("service-domain inside")
                self.cmd_add("service-domain inside")
                unit += this['unit_step']
                self.cmd = "{} interfaces {} unit {}".format(this['action'], name, unit)
                self.cmd_add("family inet", 'inet', opt='flag')
                self.cmd_add("family inet6", 'inet6', opt='flag')
                if this['ams']:
                    self.cmd = "{} interfaces".format(this['action'])
                    ams_cmd = "{} unit {} service-domain outside".format(ams, unit)
                    self.cmd_add(ams_cmd)
                    for egress_key in this['egress_key_list']:
                        ams_cmd = "{} unit {} load-balancing-options hash-keys ingress-key {}".format(ams, unit, egress_key)
                        self.cmd_add(ams_cmd)
                else:
                    self.cmd_add("service-domain outside")
                unit += this['unit_step']

                self.cmd_add("service-domain outside")
                unit += this['unit_step']
            else:
                if this['inet']:
                    self.cmd_add("family inet")
                if this['inet6']:
                    self.cmd_add("family inet6")
                if this['mpls']:
                    self.cmd_add("family mpls")
                unit += this['unit_step']

        status = self.config()

        return self.fn_checkout(status)

    def set_vlan(self, name, **kwargs):
        """Configures VLAN and other parameters available for this set command

        By specifying the number of VLANs, this routine can also be used for generating config
        If the number of VLANs are more than 20, instead of issuing set commands on to the router
        It saves the commands in a local file and then uploads the locally saved config file
        Issues load set command to load this config from the file
        Stacked Vlans:
        When 'outer_id' is specified, stacked vlans are configured.
        'id' will be treated as inner vlan.

        :param string name:
          **REQUIRED** Interfaces Name on which VLAN will be configured

        :param count:
          **OPTIONAL** Number of VLANs. Default is 1.

        :param int unit:
          **OPTIONAL** Unit Number. Default is 0

        :param bool encap:
          **OPTIONAL** Configures interface encapsulation. Default is True

        :param bool unit_encap:
          **OPTIONAL** Configures interface encapsulation under an unit. Default is True

        :param int flex_tag:
          **OPTIONAL** Configures flexible vlan tagging

        :param string encap_type:
          **OPTIONAL** Interface encapsulation type. Default is 'flexible-ethernet-services'

        :param string unit_encap_type:
          **OPTIONAL** Interface encapsulation type under an unit. Default is 'vlan-bridge'

        :param int id:
          **OPTIONAL** Starting VLAN ID or Inner VLAN ID for stacked VLANs. Default is 1.

        :param int outer_id:
          **OPTIONAL** Outer vlan id with optional tpid. Eg 0x9100.100

        :param int range:
          **OPTIONAL** Range of VLANs to be created

        :param string ip:
          **OPTIONAL** Starting IP.

        :param string ipv6:
          **OPTIONAL** Starting IPv6.

        :param string outer_tpid:
          **OPTIONAL** Outer TPID. Default is 0x9100

        :param string inner_tpid:
          **OPTIONAL** Inner TPID. Default is 0x8100

        :param string lr:
          **OPTIONAL** Logical router name

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
              set_vlan(name="ge-0/0/0")
            Robot:
              Set Vlan  name=ge-0/0/0
        """

        self.fn_checkin("Configuring vlan")

        self.vlan[name] = {}
        self.vlan[name]['action'] = kwargs.get('action', 'set')
        this = self.ptr = self.vlan[name]

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set',
                                               'unit': 0, 'encap': True, 'unit_encap': True,
                                               'encap_type': 'flexible-ethernet-services',
                                               'unit_encap_type': 'vlan-bridge', 'id': 1,
                                               'outer_tpid': '0x9100', 'inner_tpid': '0x8100',
                                               'range': None, 'outer_id': None,
                                               'ip': None, 'ipv6': None,
                                           })
        unit = this['unit']
        vlan_id = this['id']
        ipv4 = this['ip']
        ipv6 = this['ipv6']

        if 'lr' in this:
            self.cmd = "{} logical-systems {}".format(this['action'], this['lr'])
            self.cmd_add('delete interfaces {}'.format(name))
        else:
            self.cmd = "{}".format(this['action'])

        if not this['outer_id']:
            self.cmd_add('interfaces {} vlan-tagging'.format(name))
        if this['encap']:
            self.cmd_add('interfaces {} encapsulation {}'.format(name, this['encap_type']))
        if this['outer_id'] is not None or ('flex_tag' in this and this['flex_tag']):
            self.cmd_add('interfaces {} flexible-vlan-tagging'.format(name))
        if this['outer_id'] is not None:
            self.cmd_add('interfaces {} gigether-options ethernet-switch-profile \
                         tag-protocol-id [{} {}]'.format(name, this['inner_tpid'],
                                                         this['outer_tpid']))

        for iter_ii in range(1, this['count'] + 1):
            self.cmd += "interfaces {} unit {}".format(name, unit)
            if this['range'] is not None:
                _range = int(this['range'])
                if this['outer_id'] is not None:
                    self.cmd_add('vlan-tags outer {}.{} inner-range {}.{}-{}'.format(
                        this['outer_tpid'], this['outer_id'], this['inner_tpid'],
                        vlan_id, (vlan_id + _range - 1)))
                else:
                    self.cmd_add('vlan-id-range {}-{}'.format(vlan_id, (vlan_id + _range - 1)))
                    vlan_id += _range - 1
            else:
                if this['outer_id'] is not None:
                    self.cmd_add('vlan-tags outer {}.{} inner-range {}.{}'.format(
                        this['outer_tpid'], this['outer_id'], this['inner_tpid'], vlan_id))
                else:
                    self.cmd_add('vlan-id-range {}'.format(vlan_id))

            if this['unit_encap']:
                self.cmd_add('encapsulation', 'unit_encap_type')

            if ipv4 is not None:
                self.cmd_add('family inet address {}'.format(ipv4))
                ipv4 = iputils.incr_ip(this['ip'], iter_ii)
            if ipv6 is not None:
                self.cmd_add('family inet6 address {}'.format(ipv6))
                ipv6 = iputils.incr_ip(this['ipv6'], iter_ii)

        status = self.config()

        return self.fn_checkout(status)

    def set_service_set(self, name, intf, **kwargs):
        """Configures service set and other parameters available for this set command.

        :param string name:
          **REQUIRED** Service Set Name

        :param string intf:
          **REQUIRED** Interface Name

        :param string action:
          **OPTIONAL** Valid values are set, elete, ctivate, eactivate. Default is 'set'

        :param int base_ifl:
          **OPTIONAL** Base ifl of service interface.Default is 0 for intf style and 1 for NH.

        :param int ifl_step:
          **OPTIONAL** Step by which ifls are incremented for each service-interface. Default 1.

        :param int syslog:
          **OPTIONAL** Configures Syslog

        :param string sl_host:
          **OPTIONAL** Syslog Host. Default is 'local'

        :param string sl_log_pfx:
          **OPTIONAL** Syslog log-prefix

        :param list sl_class_list:
          **OPTIONAL** Reference to an array of Syslog Class names. eg.  ['nat-logs', 'ids_logs']

        :param bool next_hop:
          **OPTIONAL** Configures next hop style

        :param int index:
          **OPTIONAL** Index for scaling rules in scaling config. Default is 1

        :param int ss_idx:
          **OPTIONAL** Index for service-set name for scaling config. Default is $index

        :param int count:
          **OPTIONAL** Number of service-sets to be created for scaling config

        :param bool rule_scaling:
          **OPTIONAL** Whether to scale rules or not. Default is 1

        :param string dslite_v6_pfx_len:
          **OPTIONAL** DSLite IPv6 Prefix length for softwire-options

        :param string sw_rules:
          **OPTIONAL** Softwire Rule name

        :param string sw_rule_set:
          **OPTIONAL** Softwire Rule set name


        :param string sfw_rules:
          **OPTIONAL** Stateful-firewall Rule name

        :param string sfw_rule_sets:
          **OPTIONAL** Stateful-firewall Rule set name

        :param string sfw_policy:
          **OPTIONAL** Softwire-firewall Rule name

        :param string nat_rules:
          **OPTIONAL** NAT Rule name

        :param string nat_rule_set:
          **OPTIONAL** NAT Rule set name

        :param string pcp_rules:
          **OPTIONAL** PCP Rule name

        :param string ids_rules:
          **OPTIONAL** IDS Rule name

        :param string ipsec_rules:
          **OPTIONAL** IPSec VPN Rule name

        :param string ipsec_gw:
          **OPTIONAL** IPSec VPN Local Gateway

        :param string ike_profile:
          **OPTIONAL** IKE Access profile name

        :param int nat64_clr_df:
          **OPTIONAL** clear df bit for NAT Options Stateful NAT64

        :param int nat64_mtu:
          **OPTIONAL** ipv6 mtu for NAT Options Stateful NAT64

        :param int max_flows:
          **OPTIONAL** Maximum flows allowed for this service-set.
                          Eg. Integer, 1000 or string '4M' for 4million flows

        :param int max_drop_flows_ingr:
          **OPTIONAL** Maximum ingress drop flows.

        :param int max_drop_flows_egr:
          **OPTIONAL** Maximum egress drop flows.

        :param int max_sessions_per_subscriber:
          **OPTIONAL** Maximum Sessions Limit per subscriber [1-32K]

        :param int rep_thr:
          **OPTIONAL** Replication threshold for replication services

        :param int rep_sfw:
          **OPTIONAL** [1,0] Configures stateful-firewall for replication services

        :param int rep_nat:
          **OPTIONAL** 1,0] Configures NAT for replication services

        :param list tag_rules:
          **OPTIONAL** Reference to an Array of HCM tag rules

        :param list tag_rule_sets:
          **OPTIONAL** Reference to an Array of HCM tag rule sets

        :param int inactive_to_non_tcp:
           **OPTIONAL** Inactivity timeout period for non-TCP established sessions
                (4..86400 seconds)
        :param int sess_lmt:
           **OPTIONAL** session-limit
           Session limit

        :param int sess_to:
           **OPTIONAL** session-timeout
           Session timeout period for established sessions (4..86400 seconds)

        :param bool bypass_on_flow:
          **OPTIONAL** bypass-traffic-on-exceeding-flow-limits
          Bypass traffic when exceeding the max flow limit

        :param bool bypass_on_pic:
          **OPTIONAL** bypass-traffic-on-pic-failure
          Bypass traffic on service PIC failure

        :param bool enable_asymm_taffic:
          **OPTIONAL** enable-asymmetric-traffic-processing
          Enable service-processing for asymmetric traffic
        :param int inactive_to_tcp:
          **OPTIONAL** inactivity-tcp-timeout
          Inactivity timeout period for TCP established sessions (4..86400 seconds)

        :param int inactive_to_asymm_tcp:
           **OPTIONAL** inactivity-asymm-tcp-timeout
           Inactivity timeout period for asymmetric TCP established sessions (4..86400 seconds)
                sessions (4..86400 seconds)

        :param int close_to:
           **OPTIONAL** close-timeout
           Timeout period for TCP session tear-down (2..300 seconds)

        :param string ignore_errors:
          **OPTIONAL** ignore-errors Ignore anomalies or errors.

        :param string tcp_non_syn:
          **OPTIONAL** tcp-non-syn
          Deny session creation on receiving first non SYN pkt

        :param int tcp_mss:
          **OPTIONAL**   tcp-mss
          Enable the limit on TCP Max. Seg. Size in SYN packets (536..65535)
        :param string tfo_opt:
          **OPTIONAL** tcp-fast-open
          Tcp-fast-Open enabled paclets will be handled accordingly
        :param string tcp_tickles:
          **OPTIONAL**   tcp-tickles
          Number of TCP keep-alive packets to be sent for bi-directional TCP flows (0..30)
        :param int open_to:
           **OPTIONAL** open-timeout
           Timeout period for TCP session establishment (4..300 seconds)
        :return: True if successful else False

        :rtype: bool

        Example::

           Python:
              set_service_set(name='ss1', intf='ms-0/0/0')
           Robot:
              Set Service Set  name=ss1  intf=ms-0/0/0
	"""

        self.fn_checkin("Configuring the service set")

        base_ifl = 1 if 'next_hop' in kwargs and kwargs['next_hop'] else 0
        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'sl_host': 'local',
                                               'sl_file': 'messages', 'rule_scaling': True,
                                               'same_ss': False, 'ifl_step': 1, 'index': 1,
                                               'ss_idx': 1, 'num_rule_set': 1, 'rule_set_idx': 1,
                                               'base_ifl': base_ifl, 'syslog': False,
                                               'sset_opts': False,
                                               'del_rule':None, 'sfw_rule_sets':None,
                                               'ams':None, 'ams_unit':None,
                                               'ingress_key_list': None,
                                               'egress_key_list': None,
                                           })

        this['intf'] = intf
        #this['base_ifl'] = 1 if 'next_hop' in kwargs and kwargs['next_hop'] else 0

        spic = intf.split('.')[0]
        ss_idx = this['ss_idx'] if 'ss_idx' in this else this['index']
        rule_set_idx = this['rule_set_idx'] if 'rule_set_idx' in this else this['index']
        ifl = this['base_ifl']
        ifl_step = this['ifl_step']

        for iter_ii in range(1, this['count'] + 1):
            name_tag = name + str(ss_idx)
            nat_rule_set = []
            if name_tag not in self.sset:
                self.sset[name_tag] = {}
            self.ptr = self.sset[name_tag]
            self._update(this)

            # Cross link this info to service interface
            if intf not in self.svc_intf:
                self.svc_intf[intf] = {}
            self.svc_intf[intf][name_tag] = {}
            self.svc_intf[intf][name_tag]['count'] = this['count']
            self.svc_intf[intf][name_tag]['index'] = this['index']

            #if 'syslog' in this and this['syslog']:
            if this['syslog']:
                self.cmd = '{} services service-set {}'.format(this['action'], name_tag)
                self.cmd_add('syslog host {} services any'.format(this['sl_host']))
                self.cmd = '{} system syslog'.format(this['action'])
                self.cmd_add('host {} any any'.format(this['sl_host']))
                self.cmd_add('file {} any any'.format(this['sl_file']))
                self.cmd_add('archive size', 'sl_arc_size')
                self.cmd_add('archive files', 'sl_arc_files')

            if 'sl_host' in kwargs:
                self.cmd = '{} services service-set {} syslog host {}'.format(
                    this['action'], name_tag, this['sl_host'])
                self.cmd_add("services any")
                # self.cmd_add("class", 'syslog_class')
                self.cmd_add("log-prefix", 'sl_log_pfx')
                self.cmd_add("source-address", 'sl_src_addr')
                self.cmd_add("services", 'ss_severity')
                self.cmd_add("facility-override", 'facility_ovrd')
                self.cmd_add("class", 'sl_class_list')

            self.cmd = '{} services service-set {}'.format(this['action'], name_tag)
            self._cmd_name_tag = name_tag
            self._cmd_mapping = self.ss_map

            #self.cmd_add("softwire-options dslite-ipv6-prefix-length", 'dslite_v6_pfx_len')

            #self.cmd_add("softwire-rules", 'sw_rules', tag=iter_ii)
            #self.cmd_add("softwire-rule-set", 'sw_rule_set', tag=iter_ii)
            #self.cmd_add("stateful-firewall-rules", 'sfw_rules', tag=iter_ii)
            if this['del_rule'] is not None and this['action'] is "delete":
                if this['sfw_rule_sets'] is not None:
                    self.cmd_add("stateful-firewall-rule-sets", 'sfw_rule_sets', tag=iter_ii)
                    continue
                else:
                    self.cmd_add("stateful-firewall-rules", 'sfw_rules', tag=iter_ii)
                    continue
            else:
                if this['sfw_rule_sets'] is None:
                    self.cmd_add("stateful-firewall-rules", 'sfw_rules', tag=iter_ii)

            if this['sfw_rule_sets'] is not None:
                self.cmd_add("stateful-firewall-rule-sets", 'sfw_rule_sets', tag=iter_ii)

            #self.cmd_add("jflow-log template-profile", 'jflow_log_temp_prof')
            #self.cmd_add("nat-rule-sets", 'nat_rule_set', tag=iter_ii)
            if 'nat_rule_set' in this and this['nat_rule_set'] is not None:
                for _kk in range(1, this['num_rule_set'] + 1):
                    self.cmd_add("nat-rule-set", 'nat_rule_set', tag=rule_set_idx, update=False,
                                 mapping=True)
                    nat_rule_set.append(self.ptr['nat_rule_set'] + str(rule_set_idx))
                    rule_set_idx += 1

            #self.cmd_add("ids-rules", 'ids_rules', tag=iter_ii)
            #self.cmd_add("ipsec-vpn-rules", 'ipsec_rules', tag=iter_ii)
            if 'snmp_addr_port_low' in this and 'snmp_addr_port_high' in this:
                self.cmd_add("snmp-trap-thresholds nat-address-port low {} high {}".format(
                    this['snmp_addr_port_low'], this['snmp_addr_port_high']))
            if 'snmp_flow_low' in this and 'snmp_flow_high' in this:
                self.cmd_add("snmp-trap-thresholds flow low {} high {}".format(
                    this['snmp_flow_low'], this['snmp_flow_high']))

            if this['sset_opts']:
                self.cmd_add("service-set-options session-limit maximum ", 'sess_lmt')
                self.cmd_add("service-set-options session-timeout", 'sess_to')
                self.cmd_add("service-set-options inactivity-non-tcp-timeout",
                             'inactive_to_non_tcp')
                self.cmd_add("service-set-options bypass-traffic-on-exceeding-flow-limits",
                             'bypass_on_flow', opt='flag')
                self.cmd_add("service-set-options bypass-traffic-on-pic-failure",
                             'bypass_on_pic', opt='flag')
                self.cmd_add("service-set-options enable-asymmetric-traffic-processing",
                             'enable_asymm_taffic', opt='flag')
                # Adding tcp-session options
                self.cmd_add("service-set-options tcp-session inactivity-tcp-timeout",
                             'inactive_to_tcp')
                self.cmd_add("service-set-options tcp-session inactivity-asymm-tcp-timeout",
                             'inactive_to_asymm_tcp')
                self.cmd_add("service-set-options tcp-session close-timeout", 'close_to')
                self.cmd_add("service-set-options tcp-session ignore-errors", 'ignore_errors')
                self.cmd_add("service-set-options tcp-session tcp-non-syn", 'tcp_non_syn')
                self.cmd_add("service-set-options tcp-session tcp-mss", 'tcp_mss')
                self.cmd_add("service-set-options tcp-session tcp-fast-open", 'tfo_opt')
                self.cmd_add("service-set-options tcp-session tcp-tickles", 'tcp_tickles')
                self.cmd_add("service-set-options tcp-session open-timeout", 'open_to')
            #self.cmd_add("max-flows", 'max_flows')
            #self.cmd_add("max-drop-flows ingress", 'max_drop_flows_ingr')
            #self.cmd_add("max-drop-flows egress", 'max_drop_flows_egr')
            #self.cmd_add("service-set-options tcp-fast-open", 'tfo_opt')
            #self.cmd_add("tcp-mss", 'tcp_mss')
            #self.cmd_add("softwire-options dslite-ipv6-prefix-length", 'dslite_v6_pfx_len')
            #self.cmd_add("nat-options stateful-nat64 clear-df-bit", 'nat64_clr_df', opt='flag')
            #self.cmd_add("nat-options stateful-nat64 ipv6-mtu", 'nat64_mtu')
            #self.cmd_add("nat-options max-sessions-per-subscriber", 'max_sessions_per_subscriber')
            self.ss_map['spic'][spic] = name_tag
            if this['del_rule'] is None:
                if 'next_hop' in this and this['next_hop']:
                    self.cmd_add(
                        "next-hop-service inside-service-interface {}.{}".format(spic, ifl))
                    ifl += ifl_step
                    self.cmd_add(
                        "next-hop-service outside-service-interface {}.{}".format(spic, ifl))
                    ifl += ifl_step
                else:
                    if this['action'] == 'set':
                        if this['ams'] and this['ams_unit']:
                            ingress_key_list = ["source-ip"]
                            egress_key_list = ["destination-ip"]
                            if not this['ingress_key_list']:	this['ingress_key_list'] = ingress_key_list
                            if not this['egress_key_list']:    this['egress_key_list'] = egress_key_list
                            self.ptr['sp'] = '{}.{}'.format(this['ams'], this['ams_unit'])
                            for ingress_key in this['ingress_key_list']:
                                self.cmd_add("interface-service load-balancing-options hash-keys ingress-key {}".format(ingress_key))
                            for egress_key in this['egress_key_list']:
                                self.cmd_add("interface-service load-balancing-options hash-keys egress-key {}".format(egress_key))
                        elif 'base_ifl' in kwargs:
                            self.ptr['sp'] = '{}.{}'.format(spic, ifl)
                            ifl += ifl_step
                        else:
                            self.ptr['sp'] = spic
                        self.cmd_add(
                            "interface-service service-interface {}".format(self.ptr['sp']))
                    else:
                        if 'base_ifl' in kwargs:
                            self.ptr['sp'] = '{}.{}'.format(spic, ifl)
                            ifl += ifl_step
                        else:
                            self.ptr['sp'] = spic
                        self.cmd_add(
                            "interface-service service-interface {}".format(self.ptr['sp']))

            if len(self.cmd_list) == 0 and this['action'] != 'set':
                self.cmd_add(" ")

            if not this['same_ss']:
                ss_idx += 1

            if len(nat_rule_set) > 0:
                self.ptr['nat_rule_set'] = copy.deepcopy(nat_rule_set)

        status = self.config()

        return self.fn_checkout(status)

    def set_interface(self, name=None, **kwargs):
        """Configures interface and other parameters available for this set command.

        :param int unit:
           **OPTIONAL** Unit Number. This is base unit for scaling config. Default is 0

        :param int unit_incr:
           **OPTIONAL** Step by which to increment unit. Default is 1.

        :param int index:
           **OPTIONAL** Starting instance tag. Default is 1

        :param set action:
           **OPTIONAL** Valid values are set,delete,activate,deactivate.Default 'set?

        :param bool inet:
           **OPTIONAL** Enable/Disable IPv4

        :param bool inet6:
           **OPTIONAL** Enable/Disable IPv6

        :param bool encap_vpls:
           **OPTIONAL** Enable/Disable VPLS Ethernet Encapsulation

        :param bool mpls:
           **OPTIONAL** Enable/Disable MPLS

        :param string inet_addr:
           **OPTIONAL** Inet IPv4 Address

        :param int count:
           **OPTIONAL** Number of Units/address to be created for scaling config

        :param string inet6_addr:
           **OPTIONAL** Inet IPv6 Address

        :param string inet_ss:
           **OPTIONAL** Inet Service set

        :param string inet6_ss:
           **OPTIONAL** Inet6 Service set

        :param bool inet_ss_filter_in:
           **OPTIONAL** IPv4 inside  Service-set service-filter

        :param bool inet_ss_filter_out:
           **OPTIONAL** IPv4 outside Service-set service-filter

        :param bool inet6_ss_filter_in:
           **OPTIONAL** IPv6 inside  Service-set service-filter

        :param bool inet6_ss_filter_out:
           **OPTIONAL** IPv6 outside Service-set service-filter

        :param bool inet_filter_in:
           **OPTIONAL** IPv4 input Filter

        :param bool inet6_filter_in:
           **OPTIONAL** IPv6 input Filter

        :param bool mpls_filter_in:
           **OPTIONAL** MPLS input Filter

        :param bool inet_filter_out:
           **OPTIONAL** IPv4 output Filter

        :param bool inet6_filter_out:
           **OPTIONAL** IPv4 output Filter

        :param bool mpls_filter_out:
           **OPTIONAL** MPLS output Filter

        :param bool inet_sample_in:
           **OPTIONAL** Configures input  sampling for family inet

        :param bool inet_sample_out:
           **OPTIONAL** Configures output sampling for family inet

        :param bool inet6_sample_in:
           **OPTIONAL** Configures input  sampling for family inet6

        :param bool inet6_sample_out:
           **OPTIONAL** Configures output sampling for family inet6

        :param int mtu:
           **OPTIONAL** MTU Size

        :param int inet_mtu:
           **OPTIONAL** INET MTU Size

        :param int inet6_mtu:
           **OPTIONAL** INET6 MTU Size

        :param string lr:
           **OPTIONAL** Logical router name

        :param string arp_ip:
           **OPTIONAL** Destination IP for static ARP

        :param string arp_mac:
           **OPTIONAL** Destination MAC for static ARP

        :param bool disable:
           **OPTIONAL** Disable Interface/Subunit

        :param bool enable:
           **OPTIONAL** Enable Interface/Subunit

        :param bool grat_arp:
           **OPTIONAL** Configures gratuitous ARP reply

        :param string proxy_arp:
           **OPTIONAL** Config proxy ARP reply.Values are "", restricted, unrestricted

        :param bool twamp_srvr:
           **OPTIONAL** Configures TWAMP Server

        :param string if_descr:
           **OPTIONAL** Description name

        :param bool encap_ppp:
           **OPTIONAL** Enables Encapsulation PPP over Ethernet

        :param bool pppoe_options:
           **OPTIONAL** Enables PPPoE underlying Options

        :param string dyn_profile:
           **OPTIONAL** Dynamic Profile name for PPPoE underlying Options

        :param int max_sessions:
           **OPTIONAL** Max Sessions for PPPoE underlying Options

        :param string svc_name_tbl:
           **OPTIONAL** service-name-table for PPPoE underlying Options

        :return: True if successful else False

        :rtype: bool

         Example::

             Python:
                set_interface(inet_ss='ipsec_nat')
             Robot:
                Set Interface  inet_ss=ipsec_nat

	"""

        self.fn_checkin("Configuring interface")

        if name is None:
            raise self.MissingMandatoryArgument('name')

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'filter_incr': True,
                                               'inet_addr': None, 'inet6_addr': None,
                                               'unit': 0, 'unit_incr': 1, 'index': 1,
                                               'ams': None, 'mams':None, 'ams_unit':0
                                           })

        if name not in self.intf:
            self.intf[name] = {}
        self.ptr = self.intf[name]
        self._update(this)

        v4_addr = this['inet_addr']
        v6_addr = this['inet6_addr']
        unit = this['unit']
        ams = this['ams']
        ams_unit = this['ams_unit']
        
        if isinstance(this['mams'], str):
            this['mams'] = this['mams'].split()
        
        self.cmd = "{} interfaces {}".format(this['action'], name)
        self.cmd_add("description", 'if_descr')
        self.cmd_add("gratuitous-arp-reply", 'grat_arp', opt='flag')
        self.cmd_add("mtu", 'mtu')
        if 'unit' in kwargs:
            self.cmd += " unit {}".format(this['unit'])
        self.cmd_add("disable", 'disable', opt='flag')
        self.cmd_add("enable", 'enable', opt='flag')
        self.cmd_add("rpm twamp-server", 'twamp_srvr', opt='flag')
        tag = this['index']
        for iter_ii in range(1, this['count'] + 1):
            self.cmd = "{} interfaces {} unit {}".format(this['action'], name, unit)
            self.cmd_add('proxy-arp', 'proxy_arp')
            #self.cmd = "{} interfaces {} unit {} family".format(this['action'], name, unit)
            self.cmd += " family"

            if v4_addr is not None:
                tmp_cmd = "inet address {}".format(v4_addr)
                if 'arp_ip' in this:
                    tmp_cmd += "arp {} mac {}".format(this['arp_ip'], this['arp_mac'])
                self.cmd_add(tmp_cmd)
                v4_addr = iputils.incr_ip_subnet(this['inet_addr'], iter_ii)
            if v6_addr:
                self.cmd_add("inet6 address {}".format(v6_addr))
                v6_addr = iputils.incr_ip_subnet(this['inet6_addr'], iter_ii)

            self.cmd_add("inet", 'inet', opt='flag')
            self.cmd_add("inet6", 'inet6', opt='flag')
            self.cmd_add("vpls", 'vpls', opt='flag')
            self.cmd_add("mpls", 'mpls', opt='flag')
            self.cmd_add("mpls maximum-labels", 'mpls_label')

            self.cmd_add("inet mtu", 'inet_mtu')
            self.cmd_add("inet6 mtu", 'inet6_mtu')

            self.cmd_add("{} interfaces {} encapsulation ethernet-vpls unit {} family vpls".format(
                this['action'], name, unit), 'encap_vpls')
            self.cmd_add("{} interfaces {} unit {} encapsulation ppp-over-ether".format(
                this['action'], name, unit), 'encap_ppp')

            if 'inet_ss' in this and this['inet_ss'] is not None:
                inp_cmd = "inet service input service-set {}{}".format(this['inet_ss'], tag)
                out_cmd = "inet service output service-set {}{}".format(this['inet_ss'], tag)
                if 'inet_ss_filter_in' in this and this['inet_ss_filter_in']:
                    inp_cmd += " service-filter {}{}".format(this['inet_ss_filter_in'], tag)
                if 'inet_ss_filter_out' in this and this['inet_ss_filter_out']:
                    out_cmd += " service-filter {}{}".format(this['inet_ss_filter_out'], tag)
                self.cmd_add(inp_cmd)
                self.cmd_add(out_cmd)
                self.ptr['inet_ss'] = this['inet_ss'] + str(tag)
                self.ss_map['intf'][name] = this['inet_ss'] + str(tag)
            if 'inet6_ss' in this and this['inet6_ss'] is not None:
                inp_cmd = "inet6 service input service-set {}{}".format(this['inet6_ss'], tag)
                out_cmd = "inet6 service output service-set {}{}".format(this['inet6_ss'], tag)
                if 'inet6_ss_filter_in' in this and this['inet6_ss_filter_in']:
                    inp_cmd += " service-filter {}{}".format(this['inet6_ss_filter_in'], tag)
                if 'inet6_ss_filter_out' in this and this['inet6_ss_filter_out']:
                    out_cmd += " service-filter {}{}".format(this['inet6_ss_filter_out'], tag)
                self.cmd_add(inp_cmd)
                self.cmd_add(out_cmd)
                self.ptr['inet6_ss'] = this['inet6_ss'] + str(tag)
                self.ss_map['intf'][name] = this['inet6_ss'] + str(tag)

            self.cmd_add("inet filter input", 'inet_filter_in', tag=tag)
            self.cmd_add("inet filter output", 'inet_filter_out', tag=tag)
            self.cmd_add("inet6 filter input", 'inet6_filter_in', tag=tag)
            self.cmd_add("inet6 filter output", 'inet6_filter_out', tag=tag)
            self.cmd_add("mpls filter input", 'mpls_filter_in', tag=tag)
            self.cmd_add("mpls filter output", 'mpls_filter_out', tag=tag)
            self.cmd_add("vpls filter input", 'vpls_filter_in', tag=tag)
            self.cmd_add("vpls filter output", 'vpls_filter_out', tag=tag)

            self.cmd_add("inet sampling input", 'inet_sample_in', tag=tag)
            self.cmd_add("inet sampling output", 'inet_sample_out', tag=tag)
            self.cmd_add("inet6 sampling input", 'inet6_sample_in', tag=tag)
            self.cmd_add("inet6 sampling output", 'inet6_sample_out', tag=tag)

            unit += this['unit_incr']
            tag += 1

        if len(self.cmd_list) == 0 and this['action'] != 'set':
            self.cmd_list.append("{} interfaces {}".format(this['action'], name)) 
 
        if 'ams' in kwargs:
            self.cmd = "{} interfaces".format(this['action'])
            for mams_interface in this['mams']:
                ams_cmd = "{} load-balancing-options member-interface {}".format(this['ams'], mams_interface)
                self.cmd_add(ams_cmd)
            int_cmd = "{} unit {} family inet".format(this['ams'], ams_unit)
            self.cmd_add(int_cmd)

        status = self.config()

        return self.fn_checkout(status)

    def set_sfw_policy(self, name='sfw_policy', **kwargs):
        """Configure Stateful firewall policy and other parameters available for this set command.

        :param string name:
            **OPTIONAL** SFW policy name. Default is 'sfw_policy'

        :param int count:
           **OPTIONAL** Number of rules to be created for scaling config. Default is 1

 	:param string action:
            **OPTIONAL** Valid values are set, delete, activate, deactivate. Default is 'set'

        :param string unit:
           **OPTIONAL** Rule direction. Default is 'input-output'

        :param int term:
           **OPTIONAL** Term name. Default is 0

        :param int num_terms:
           **OPTIONAL** Number of terms. Default is 1

        :param string src_addr:
           **OPTIONAL** Source Address to be matched

        :param int src_addr_step:
           **OPTIONAL** Step by which Src Addr to be matched has to be incr per rule

        :param int src_addr_term_step:
           **OPTIONAL** Step by which Src Addr to be matched has to be incr per term

        :param string dst_addr:
           **OPTIONAL** Destination Address to be matched

        :param int dst_addr_step:
           **OPTIONAL** Step by which Dst Addr to be matched has to be incr per rule

        :param int dst_addr_term_step:
           **OPTIONAL** Step by which Dst Addr to be matched has to be incr per term

        :param int dst_port_low:
           **OPTIONAL** Destination Port Range - low to be matched

        :param int dst_port_high:
           **OPTIONAL** Destination Port Range - high to be matched

        :param list from_apps_list:
           **OPTIONAL** List of applications to be matched

        :param list from_appsets_list:
           **OPTIONAL** List of application-sets to be matched

        :param list from_src_pfx_list:
           **OPTIONAL** From source-prefix-list to be matched

        :param list action_list:
           **OPTIONAL** List of actions to be taken

        :return: True if successful else False

        :rtype: bool

         Example::

             Python:
               set_sfw_policy(name='sfw_policy1', action_list=['accept'], syslog=1)
             Robot:
                @{sfw_action_list} = BuiltIn.Create List  accept
               Set SFW Policy  name=sfw_policy1  action_list=@{sfw_action_list}  syslog=1
        """

        self.fn_checkin("Configuring SFW Policy")

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'dir': 'input',
                                               'sfw_rule_set_name': None,
                                               'src_addr': None, 'src_addr_step': 0,
                                               'dst_addr': None, 'dst_addr_step': 0,
                                               'src_addr_term_step': 0, 'dst_addr_term_step': 0,
                                               'src_exclude':None, 'dst_exclude':None,
                                               'del_policy':None, 'sfw_rule_name':'R1',
                                               'del_rule':None, 'del_rule_set':None,})

        src_addr = this['src_addr']
        dst_addr = this['dst_addr']

        _cmd = "{} services policies".format(this['action'])

        for iter_ii in range(1, this['count'] + 1):
            policy_tag = name + str(iter_ii)
            if policy_tag not in self.sfw_policy:
                self.sfw_policy[policy_tag] = {}
            self.ptr = self.sfw_policy[policy_tag]
            self._update(this)
            self.cmd = "{} services policies".format(this['action'])

            if this['del_rule'] is None and this['del_policy'] is None and this['del_rule_set'] is None:
                self.cmd_add(
                    " stateful-firewall-rule {} match-direction {}".
                    format(this['sfw_rule_name'] + str(iter_ii), this['dir']))

            if this['del_rule_set'] is not None and this['sfw_rule_set_name'] is not None and this['sfw_rule_name'] is not None and this['del_rule'] is not None:
                self.cmd_add(
                    "stateful-firewall-rule-set {} stateful-firewall-rule {}".
                    format(this['sfw_rule_set_name'], this['sfw_rule_name'] + str(iter_ii)))
                continue
            if this['del_rule_set'] is not None and this['sfw_rule_set_name'] is not None:
                self.cmd_add("stateful-firewall-rule-set {}" .format(this['sfw_rule_set_name']))
                continue
            if this['del_rule'] is not None and this['sfw_rule_name'] is not None:
                self.cmd_add(" stateful-firewall-rule {}".format(this['sfw_rule_name'] + str(iter_ii)))
                continue

            if this['sfw_rule_set_name'] is not None:
                self.cmd_add(
                    "stateful-firewall-rule-set {} stateful-firewall-rule {}".
                    format(this['sfw_rule_set_name'], this['sfw_rule_name'] + str(iter_ii)))

            self.cmd += " stateful-firewall-rule {} policy {}".format(this['sfw_rule_name'] + str(iter_ii), policy_tag)

            if this['del_policy'] is not None:
                self.cmd_add(" ")
                continue
            if this['src_exclude'] is not None:
                self.cmd_add("match source-address-excluded")

            if this['dst_exclude'] is not None:
                self.cmd_add("match destination-address-excluded")

            self.cmd_add("match application", 'app_list')

            if src_addr is not None:
                self.cmd_add("match source-address {}".format(src_addr))
                if this['src_addr_term_step']:
                    src_addr = iputils.incr_ip_subnet(src_addr, this['src_addr_term_step'])
            if dst_addr is not None:
                self.cmd_add("match destination-address {}".format(dst_addr))
                if this['dst_addr_term_step']:
                    dst_addr = iputils.incr_ip_subnet(dst_addr, this['dst_addr_term_step'])
            if 'dst_port_low' in this and 'dst_port_high' in this:
                self.cmd_add("from destination-port range low {} high {}".format(
                    this['dst_port_low'], this['dst_port_high']))
            self.cmd_add('then', 'action_list')

            if iputils.is_ip(src_addr):
                src_addr = iputils.incr_ip_subnet(src_addr, this['src_addr_step'])

            if iputils.is_ip(dst_addr):
                dst_addr = iputils.incr_ip_subnet(dst_addr, this['dst_addr_step'])

        status = self.config()

        return self.fn_checkout(status)

    def set_address_book_address(self, name, addr, **kwargs):
        """Configure the address in address book
        """
        self.fn_checkin("Configuring Address book")

        #this = utils.update_opts_from_args(kwargs, defaults={ 'action': 'set' })
        action = kwargs.get('action', 'set')

        _cmd = "{} services address-book global address {} {}".format(action, name, addr)
        self.cmd_add(_cmd)
        status = self.config()
        return self.fn_checkout(status)
        #return self.fn_checkout(self.dh.cli(cmd=_cmd))

    def set_route_instance(self, name, inst_type, **kwargs):
        """Configures Routing instance and other parameters available for this set command.

        :param list if:
           **OPTIONAL** list of interfaces to be configured for this routing instance

        :param int num_ifls:
           **OPTIONAL** Number of IFLs to be created for interface under an instance.

        :param int ifl_step:
           **OPTIONAL** Step by which ifl will be incremented when num_ifls is used.

        :param list sp_intf:
           **OPTIONAL** Reference to the list of sp intfs

        :param int num_sp_ifls:
           **OPTIONAL** Number of IFLs to be created for SP interface under instance

        :param int sp_ifl_step:
           **OPTIONAL** Step by which sp ifl will be incremented when num_sp_ifl used

        :param bool sp_intf_nh:
           **OPTIONAL** SP NH Style

        :param string rd:
           **OPTIONAL** Routing instance distinguisher.

        :param bool import:
           **OPTIONAL** VRF import

        :param bool export:
           **OPTIONAL** VRF export

        :param list options_list:
           **OPTIONAL** Routing options for this routing instance

        :param int index:
           **OPTIONAL** Starting instance tag. Default is 1

        :param int count:
           **OPTIONAL** Number of instances

        :param int base_ifl:
           **OPTIONAL** Base IFL. Default is 1.

        :param int sp_base_ifl:
           **OPTIONAL** SP Base IFL. Default is 1.

        :param string lr:
           **OPTIONAL** Logical router name

        :param string tbl_lbl:
           **OPTIONAL** VRF Table Label

        :param string target:
           **OPTIONAL** VRF Target

        :param int max_pfxs_lmt:
           **OPTIONAL** Maximum number of prefixes (1..4294967295)

        :param int max_pfxs_thold:
           **OPTIONAL** Percentage of limit at which to start generating warnings

        :param string vpls_site_range:
           **OPTIONAL** VPLS Site range

        :param bool vpls_no_tun:
           **OPTIONAL** Enable vpls no tunnel services

        :param string vpls_site:
           **OPTIONAL** VPLS site name

        :param int vpls_site_id:
           **OPTIONAL** VPLS Site ID

        :param bool fwd_inet_filter_in:
           **OPTIONAL** Input inet filter for forwarding options

        :param bool fwd_inet_filter_out:
           **OPTIONAL** Output inet filter for forwarding options

        :param bool fwd_inet6_filter_in:
           **OPTIONAL** Input inet6 filter for forwarding options

        :param bool fwd_inet6_filter_out:
           **OPTIONAL** Output inet6 filter for forwarding options

        :return: True if successful else False

        :rtype: bool

        Example::

              Python:
                 set_route_instance(name='vrf', inst_type='vrf', sp_intf='ms-11/0/0',
                                    sp_base_ifl=2, num_sp_ifls=3, sp_ifl_step=2)
              Robot:
                 Set Route Instance  name=vrf  inst_type=vrf  sp_intf=ms-11/0/0  sp_base_ifl=2
                                     num_sp_ifls=3   sp_ifl_step=2
        """

        self.fn_checkin("Configuring route instance")

        if name is None:
            raise self.MissingMandatoryArgument('name')

        self.rt_inst[name] = {}
        self.rt_inst[name]['type'] = inst_type
        #this = self.ptr = self.rt_inst[name]

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'index': 1,
                                               'base_ifl': 1, 'num_ifls': 0, 'ifl_step': 1,
                                               'if_list': None,
                                               'sp_base_ifl': 1, 'sp_ifl_step': 1,
                                               'num_sp_ifls': 0, 'sp_if_list': None,
                                               'ams_base_ifl': 1, 'ams_ifl_step': 1,
                                               'num_ams_ifls': 0, 'ams_if_list': None,
                                           })

        idx = this['index']
        ifl = this['base_ifl'] if 'base_ifl' in this else idx
        sp_ifl = this['sp_base_ifl']
        ams_ifl = this['ams_base_ifl']

        if 'lr' in this:
            _cmd = "{} logical-systems {}".format(this['action'], this['lr'])
        else:
            _cmd = "{}".format(this['action'])

        for _ii in range(1, this['count'] + 1):
            inst_name = '{}{}'.format(name, idx)
            #self.cmd += " routing-instances {}{}".format(name, idx)
            self.cmd = _cmd + " routing-instances {}".format(inst_name)
            if inst_name not in self.rt_inst:
                self.rt_inst[inst_name] = {}
            self.ptr = self.rt_inst[inst_name]
            self._update(this)

            if this['if_list'] is not None:
                for intf in this['if_list']:
                    #if intf not in self.if_ri_map:
                        #self.if_ri_map[intf] = {}
                    self.if_ri_map[intf] = "{}{}".format(name, idx)
                    if this['num_ifls']:
                        ifl1 = this['base_ifl'] if 'base_ifl' in this else this['index']
                        for _ in range(1, this['num_ifls'] + 1):
                            self.cmd_add("interface {}.{}".format(intf, ifl1))
                            ifl1 += this['ifl_step']
                    else:
                        self.cmd_add("interface {}.{}".format(intf, ifl))

            if this['sp_if_list'] is not None:
                for intf in this['sp_if_list']:
                    if this['num_sp_ifls']:
                        ifl1 = this['sp_base_ifl']
                        for _ in range(1, this['num_sp_ifls'] + 1):
                            self.cmd_add("interface {}.{}".format(intf, ifl1))
                            ifl1 += this['sp_ifl_step']
                    else:
                        self.cmd_add("interface {}.{}".format(intf, sp_ifl))
                        if 'sp_intf_nh' in this and this['sp_intf_nh']:
                            self.cmd_add("interface {}.{}".format(intf, sp_ifl + 1))

                sp_ifl += 2

            if this['ams_if_list'] is not None:
                for intf in this['ams_if_list']:
                    if this['num_ams_ifls']:
                        ifl1 = this['ams_base_ifl']
                        for _ in range(1, this['num_ams_ifls'] + 1):
                            self.cmd_add("interface {}.{}".format(intf, ifl1))
                            ifl1 += this['ams_ifl_step']
                    else:
                        self.cmd_add("interface {}.{}".format(intf, ams_ifl))
                        if 'ams_intf_nh' in this and this['ams_intf_nh']:
                            self.cmd_add("interface {}.{}".format(intf, ams_ifl + 1))

                ams_ifl += 2


            self.cmd_add("forwarding-options family inet filter input", 'fwd_inet_filter_in')
            self.cmd_add("forwarding-options family inet filter output", 'fwd_inet_filter_out')
            self.cmd_add("forwarding-options family inet6 filter input", 'fwd_inet6_filter_in')
            self.cmd_add("forwarding-options family inet6 filter output", 'fwd_inet6_filter_out')

            self.cmd_add("instance-type {}".format(inst_type))

            imp_tag = idx if 'import_incr' in this and this['import_incr'] else None
            self.cmd_add("vrf-import", 'import', tag=imp_tag)
            exp_tag = idx if 'export_incr' in this and this['export_incr'] else None
            self.cmd_add("vrf-export", 'export', tag=exp_tag)

            self.cmd_add("vrf-table-label", 'tbl_lbl', opt='flag')

            self.cmd_add("route-distinguisher", 'rd', tag=":{}".format(idx))
            self.cmd_add("vrf-target", 'target', tag=":{}".format(idx))

            # Configure L2VPN under this instance, if specified
            self.cmd_add("protocols l2vpn encapsulation-type", 'l2vpn_encap')
            if 'l2vpn_site' in this:
                self.cmd_add("protocols l2vpn site {} site-identifier".format(
                    this['l2vpn_site']), 'l2vpn_site_identifier')
                if 'l2vpn_interface' in this and 'l2vpn_remote_site_id' in this:
                    self.cmd_add("protocols l2vpn site {} interface {} remote-site-id {}".format(
                        this['l2vpn_site'], this['l2vpn_interface'], this['l2vpn_remote_site_id']))

            # Configure VPLS under this instance, if specified
            self.cmd_add("protocols vpls site-range", 'vpls_site_range')
            if 'vpls_site' in this:
                if 'vpls_auto_site_id' in this and this['vpls_auto_site_id']:
                    self.cmd_add("protocols vpls site {} automatic-site-id".format(
                        this['vpls_site']))
                    self.cmd_add("protocols vpls site {} site-identifier".format(
                        this['vpls_site']), 'vpls_site_id')
            self.cmd_add("protocols vpls mac-table-aging-time", 'vpls_mac_aging_time')
            self.cmd_add("protocols vpls no-tunnel-services", 'vpls_no_tun', opt='flag')

            # Configure BGP under this instance,if specified
            if 'bgp_grp_name' in this:
                self.cmd_add("protocols bgp group {} type".format(this['bgp_grp_name']),
                             'bgp_peer_type')
                self.cmd_add("protocols bgp group {} local-address".format(this['bgp_grp_name']),
                             'bgp_local_addr')
                self.cmd_add("protocols bgp group {} neighbor".format(this['bgp_grp_name']),
                             'bgp_neighbor_addr')

            self.cmd_add("routing-options maximum-prefixes", 'max_pfxs_lmt')
            self.cmd_add("routing-options maximum-prefixes threshold", 'max_pfxs_thold')

            self.cmd_add("routing-options", 'options_list')
            self.cmd_add("access address-assignment mobile-pools", 'pool_list')
            idx += 1
            ifl += 1

        status = self.config()

        return self.fn_checkout(status)

    def set_firewall_filter(self, name, **kwargs):
        """Configures Firewall Filter options and other parameters for this set command

        :param int count:
           **OPTIONAL** Number of filters to be created for scaling config

        :param int index:
           **OPTIONAL** Starting index to be tagged with filter name for scaling scenarios

        :param string family:
           **OPTIONAL** Protocol Family. (any | ccc | inet | inet6 | mpls | vpls)

        :param string ftype:
           **OPTIONAL** Filter type. (filter | service-filter). Default is 'filter'

        :param int term:
           **OPTIONAL** Term name . Default is 0

        :param bool if_specific:
           **OPTIONAL** default is False

        :param string fltr_specific:
           **OPTIONAL**

        :param int if_ex_bw_lmt:
           **OPTIONAL** Bandwidth limit

        :param int if_ex_burst_lmt:
           **OPTIONAL** Burst limit

        :param string pol_action:
           **OPTIONAL* Policer action

        :param string src_addr:
           **OPTIONAL** Source Address to be matched

        :param int src_port:
           **OPTIONAL** Source Port to be matched per filter

        :param string dst_addr:
           **OPTIONAL** Destination Address to be matched

        :param int dst_port:
           **OPTIONAL** Destination port to be matched per filter

        :return: True if successful else False

        :rtype: bool

        Example::

             Python:
                set_firewall_filter(name=flt_in)
             Robot:
                Set Firewall Filter  name=flt_in
        """

        self.fn_checkin("Configuring firewall filter")

        #self.fw_filter[name] = {}
        #self.fw_filter[name]['ftype'] = 'filter'
        #this = self.ptr = self.fw_filter[name]

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'index': 1,
                                               'if_specific': False, 'fltr_specific': False,
                                               'policer': False, 'in_if_specific': False,
                                               'ftype': 'filter',
                                               'src_addr': None, 'src_port': None,
                                               'dst_addr': None, 'dst_port': None,
                                           })

        self.cmd = "{} firewall".format(this['action'])
        if this['family']:
            self.cmd += ' family {}'.format(this['family'])

        self.cmd_add("interface_specific", 'if_specific', opt='flag')

        if this['policer']:
            if name not in self.fw_filter:
                self.fw_filter[name] = {}
            #self.fw_filter[name]['ftype'] = 'filter'
            self.ptr = self.fw_filter[name]
            self._update(this)
            self.cmd_add("policer {} filter-specific".format(name), 'fltr_specific', opt='flag')
            self.cmd_add("policer {} if-exceeding bandwidth-limit".format(name), 'if_ex_bw_lmt')
            self.cmd_add("policer {} if-exceeding burst-size-limit".format(name),
                         'if_ex_burst_lmt')
            self.cmd_add("policer {} then".format(name), 'pol_action')
        else:
            _cmd = '{} {}'.format(self.cmd, this['ftype'])
            for iter_ii in range(1, this['count'] + 1):
                name_tag = name + str(iter_ii)
                if name_tag not in self.fw_filter:
                    self.fw_filter[name_tag] = {}
                self.ptr = self.fw_filter[name_tag]
                self._update(this)
                self.cmd_add("{} interface-specific".format(name_tag), 'in_if_specific',
                             opt='flag')

                self.cmd = _cmd + ' {} term {}'.format(name_tag, this['term'])
                for key in kwargs:
                    if key == 'action_list':
                        action_tag = ".{}".format(iter_ii) if key == 'routing-instance' or \
                                                          key == 'count' else None
                        self.cmd_add('then', 'action_list', tag=action_tag)
                        continue

                    self.cmd_add("from source-address", 'src_addr')
                    self.cmd_add("from source-port", 'src_port')
                    self.cmd_add("from destination-port", 'dst_port')
                    self.cmd_add("from destination-address", 'dst_addr')

        status = self.config()

        return self.fn_checkout(status)

    def set_static_route(self, **kwargs):
        """Configures Static route """
        return self.set_route_options(**kwargs)

    def set_route_options(self, **kwargs):
        """Configures routing options

        :param string lr:
           **OPTIONAL** Logical router name

        :param string action:
           **OPTIONAL** Valid values are set,delete,activate,deactivate. Default is 'set'

        :param string rid:
           **OPTIONAL** Route distinguisher

        :param string instance:
          **OPTIONAL** Routing instance name

        :param string dest:
           **OPTIONAL** Destination IP of the static route to be configured

        :param string nh:
           **OPTIONAL** Next hop of the static route to be configured

        :param string lnh:
           **OPTIONAL** LSP Next hop of the static route to be configured

        :param string qnh:
           **OPTIONAL** Qualified Next hop of the static route to be configured

        :param string qnh_pref:
           **OPTIONAL** Preference for qualified next hop

        :param int dest_incr:
           **OPTIONAL** For scaling, number by which next destination IP will be incremented.
                               Default is 1.
        :param int dest_count:
           **OPTIONAL** For scaling, number of static routes to be created. Default is 1.

        :param int nh_incr:
           **OPTIONAL** For scaling, the number by which the next-hop will be incremented.
                               Default is 0 (no increment).

        :param int nh_incr_after:
           **OPTIONAL** For scaling, the number of iterations after which the next-hop will
                               be incremented using 'nh_incr'. Default is 0
        :param int nh_base_ifl:
           **OPTIONAL** Base IFL if next-hop is an intf. Default is 1

        :param string nt:
           **OPTIONAL** Next-table name

        :param string if_inet_export:
           **OPTIONAL** Export policy for ipv4 interface route. Values are 'lan', 'point-to-point'

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
               set_route_options(dest="40.0.0.0/8",nh="50.50.50.1")
            Robot:
               Set Route Options  dest=40.0.0.0/8  nh=50.50.50.1
	   """

        self.fn_checkin("Configuring routes")

        action = kwargs.get('action', 'set')
        self.cmd = "{}".format(action)
        if 'lr' in kwargs:
            self.cmd += "logical-systems {}".format(kwargs['lr'])
        setlr = self.cmd
        self.cmd += " routing-options"

        if 'if_inet_export' in kwargs:
            self.cmd_add("interface-routes family inet export {}".format(kwargs['if_inet_export']))
        if 'family' in kwargs and 'rib_grp' in kwargs:
            self.cmd_add("interface-routes rib-group {} {}".format(kwargs['family'],
                                                                   kwargs['rib_grp']))
        if 'rid' in kwargs:
            self.cmd_add("router-id {}".format(kwargs['rid']))
        if 'as' in kwargs:
            self.cmd_add("autonomous-system {}".format(kwargs['as']))

        if 'dest' not in kwargs:
            return self.config()

        dest = kwargs['dest']

        self.rt_opts[dest] = {}
        self.rt_opts[dest]['action'] = kwargs.get('action', 'set')
        self.rt_opts[dest]['type'] = 'filter'
        this = self.ptr = self.rt_opts[dest]

        utils.update_opts_from_args(kwargs,
                                    defaults={
                                        'dest_incr': 1, 'action': 'set', 'index': 1,
                                        'nh_step': 0, 'nh_incr_after': 0,
                                        'inst_incr_after': 0, 'inst_step': 0,
                                        'nh_base_ifl': 1, 'dest_count': 1,
                                        'lnh': None, 'qnh': None, 'nt': None,
                                        'count': 1, 'tag': '.', 'rib': 'inet6.0',
                                    }, opts=this)

        idx = this['index']
        nh_ifl = this['nh_base_ifl']
        lnh = this['lnh']
        qnh = this['qnh']

        if not len(dest.split('/')) > 1:
            # Assign a default mask, if not specified
            dest += '/64' if iputils.is_ip_ipv6(dest) else '/8'

        net = iputils.get_network_address(dest)
        mask = iputils.get_mask(dest)

        for iter_ii in range(1, this['count'] + 1):
            self.cmd = setlr
            if 'instance' in this and this['instance'] is not None:
                self.cmd += ' routing-instances {}'.format(this['instance'])
                if this['inst_step']:
                    self.cmd += '{}{}'.format(this['tag'], idx)
                if this['inst_incr_after']:
                    if iter_ii % this['inst_incr_after'] == 0:
                        idx += this['inst_step']
                else:
                    idx += this['inst_step']

            self.cmd += ' routing-options'
            if iputils.is_ip_ipv6(dest):
                self.cmd += ' rib {}'.format(this['rib'])

            if 'nh' in this and this['nh'] is not None:
                if iputils.is_ip(iputils.strip_mask(this['nh'])):
                    next_hop = this['nh']
                    self.cmd_add(
                        'static route {} next-hop {}'.format(net, iputils.strip_mask(next_hop)))
                    if this['nh_incr_after']:
                        if iter_ii % this['nh_incr_after'] == 0:
                            next_hop = iputils.incr_ip_subnet(next_hop, this['nh_step'])
                    else:
                        if this['nh_step']:
                            next_hop = iputils.incr_ip_subnet(next_hop, this['nh_step'])
                else:
                    # Presuming the next-hop to be interface
                    self.cmd_add('static route {}/{} next-hop {}.{}'.format(net, mask,
                                                                            this['nh'], nh_ifl))
                    nh_ifl += this['nh_step']

            if 'nt' in this and this['nt'] is not None:
                self.cmd_add('static route {} next-table'.format(net), 'nt')
            if lnh:
                self.cmd_add('static route {} lsp-next-hop {}'.format(net, lnh))
                if iputils.is_ip(lnh):
                    lnh = iputils.incr_ip_subnet(lnh)
            if qnh:
                self.cmd_add('static route {} qualified-next-hop {}'.format(net, qnh))
                if iputils.is_ip(qnh):
                    qnh = iputils.incr_ip_subnet(qnh)
                self.cmd_add('static route {} qualified-next-hop {} preference'.format(net, qnh),
                             'qnh_pref')
            if net != '::':
                if iputils.get_mask(net) != 0:
                    # Just ignoring the scenarios with /0 mask
                    net = iputils.incr_ip_subnet(net, this['dest_incr'])

        status = self.config()

        return self.fn_checkout(status)

    def set_application(self, name=None, **kwargs):
        """Configures application

        :param string name:
           **OPTIONAL** Application name to be configured

        :param string proto:
           **OPTIONAL** Protocol

        :param string app_proto:
           **OPTIONAL** Application Protocol

        :param string ttl_thr:
           **OPTIONAL** TTL Threshold

        :param int src_port:
           **OPTIONAL** Source port

        :param int dst_port:
           **OPTIONAL** Destination port

        :param int inactive_to:
           **OPTIONAL** Inactivity timeout (seconds)

        :return: True if successful else False

        :rtype: bool

        Example::

             Python:
                set_application(name=app1)
             Robot:
                Set Application  name=app1
        """

        self.fn_checkin("Configuring apps")

        if name is None:
            raise self.MissingMandatoryArgument('name')

        self.apps[name] = {}
        self.apps[name]['action'] = kwargs.get('action', 'set')
        this = self.ptr = self.apps[name]

        for attr in kwargs:
            this[attr] = kwargs[attr]

        self.cmd = "{} applications application {}".format(this['action'], name)

        self.cmd_add('protocol', 'proto')
        self.cmd_add('ttl-threshold', 'ttl_thr')
        self.cmd_add('application-protocol', 'app_proto')
        self.cmd_add('destination-port', 'dst_port')
        self.cmd_add('source-port', 'src_port')
        self.cmd_add('inactivity-timeout', 'inactive_to')
        self.cmd_add('learn-sip-register', 'learn_sip_register', opt='flag')
        self.cmd_add('snmp-command', 'snmp_cmd')

        status = self.config()

        return self.fn_checkout(status)

    def set_application_set(self, name=None, **kwargs):
        """Configures application-set

        :param string name:
           **OPTIONAL** Application-set name to be configured

        :param list app_list:
           **OPTIONAL** Reference to the list of applications to be configured for this set

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
               set_application_set(name=appset1)
            Robot:
               Set Application Set  name=appset1

        """

        self.fn_checkin("Configuring appset")

        if name is None:
            raise self.MissingMandatoryArgument('name')

        self.appset[name] = {}
        self.appset[name]['action'] = kwargs.get('action', 'set')
        this = self.ptr = self.appset[name]

        this['count'] = 1
        this['index'] = 1

        for attr in kwargs:
            this[attr] = kwargs[attr]

        for iter_ii in range(1, this['count'] + 1):
            self.cmd = "{} applications application-set {}{}".format(
                this['action'], name, iter_ii)
            self.cmd_add('application', 'app_list')

        status = self.config()

        return self.fn_checkout(status)

    ##########################################################################
    # Clear methods
    ##########################################################################




    ##########################################################################
    # Get/Verify methods
    ##########################################################################

    def verify(self, **kwargs):
        """ Routine to verify sessions extensive

        :return: True if successful else False

        :rtype: bool

        Example:::

            Python:
                verify()
            Robot:
                Verify

        """

        self.fn_checkin("Verifying services")

        #self._get_tg_port_and_config_mapping(**kwargs)

        #self.verify_sessions_count(**kwargs)

        self.fn_checkout()

    ##########################################################################
    # Get/Verify methods
    ##########################################################################
    def _get_tg_port_and_config_mapping(self, **kwargs):
        """Determines sp,sset etc. thats going to service traffic for every tg port"""

        self.fn_checkin("Mapping TG Port and config")

        limit = kwargs.get('limit', None)
        limit_perc = kwargs.get('limit_perc', 1)

        self._get_tg_sess(**kwargs)

        self._get_ss_for_intf()

        self.tg_cfg_map = {}
        #self.pool_map = {}
        #self.sset_map = {}
        #_pool_cnt = self.tg_sess_cnt['nat_pool'] = {}
        #_sset_cnt = self.tg_sess_cnt['sset'] = {}
        self.tg_sess_cnt = self.dd()

        for tg_if in self.tg_sess:
            if tg_if == 'total':
                continue
            _conf_map = self.tg_cfg_map[tg_if] = {}
            path = self.topo['intf'][tg_if]['path']
            intf_list = self.topo['path_res'][self.resource][path]
            for r_if in intf_list:
                r_if = t['resources'][self.resource]['interfaces'][r_if]['pic']
                if r_if in self.ss_map['intf']:
                    sset = _conf_map['sset'] = self.ss_map['intf'][r_if]
                    spic = _conf_map['spic'] = self.sset[sset]['intf']
                    self.tg_sess_cnt[spic][sset] = self.tg_sess[tg_if]['total']
                    if 'nat_rule_set' in self.sset[sset]:
                        _conf_map['nat_rule_set'] = self.sset[sset]['nat_rule_set']

            _max_sess = _conf_map['tot_sess'] = self.tg_sess[tg_if]['total']

            if _max_sess < 100:
                limit_perc = 100
            limit_num = int(float(_max_sess) * (limit_perc / 100))
            if limit is not None:
                limit_num = limit
            # Pick random numbers
            _conf_map['rand_sess_idx_list'] = random.sample(range(_max_sess), limit_num)

        # Now, Find sessions count per service pic
        for spic in self.tg_sess_cnt:
            self.tg_sess_cnt[spic]['total'] = 0
            for sset in self.tg_sess_cnt[spic]:
                self.tg_sess_cnt[spic]['total'] += self.tg_sess_cnt[spic][sset]


        self.fn_checkout()

    def _get_ss_for_intf(self):
        """Update the object intf_ss variable with interface and respective service set name """

        self.fn_checkin("Retrieving interface sset")
        self.intf_ss = {}
        for if_name in self.intf:
            # For interface style service-set
            if 'inet_ss' in self.intf[if_name]:
                self.intf_ss[if_name] = self.intf[if_name]['inet_ss']
            elif 'inet6_ss' in self.intf[if_name]:
                self.intf_ss[if_name] = self.intf[if_name]['inet6_ss']
            elif if_name in self.if_ri_map:
                # Get the routing instance name
                ri_name = self.if_ri_map[if_name]
                # Get the corresponding ms interface
                # Right now, only one ms interface is supported
                ms_if = self.rt_inst[ri_name]['sp_if_list'][0]
                # Fetch the service-set
                self.intf_ss[if_name] = self.ss_map['spic'][ms_if]

        self.log('INFO', "intf_ss: {}".format(self.intf_ss))
        self.fn_checkout()

        return self.intf_ss

    def _get_tg_sess(self, **kwargs):
        """Return tg_sess either from input or from object"""

        self.fn_checkin("Retrieving TG Sessions")

        self.tg_sess = kwargs.get('tg_sess', self.tg_sess)

        if 'tg_sess' in kwargs:
            kwargs.pop('tg_sess')

        if self.tg_sess is None:
            raise self.MissingMandatoryArgument('tg_sess')

        self.fn_checkout()

    def _update(self, kwargs):
        """Update the object variable(ptr) with the keyword args"""

        for attr in kwargs:
            self.ptr[attr] = kwargs[attr]

    def get_usf_sfw_policy(self, policy_name=None):
        """Fetch SFW policy details as dictionary
        :rtype: bool
        """
        self.fn_checkin("Get SFW Policy detail")
        _xpath = 'security-policies/security-context'
        cmd = 'show services policies policy-name {}'.format(policy_name)

        entry = self.get_xml_output(cmd, xpath=_xpath)
        if entry is None:
            return self.fn_checkout(False, err_msg="Not able to retrieve SFW Policy details")
        else:
            self.fn_checkout(True)
            return entry

    def verify_usf_sfw_policy(self, expected_dict, act_dict=None, policy_name=None):
        """Fetch SFW policy details as dictionary

        :rtype: bool

        """
        self.fn_checkin("Verifying SFW Policy detail")

#        if act_dict == None:
        if act_dict is None:
            entry = self.get_usf_sfw_policy(policy_name)
        else:
            entry = act_dict
        dir_flag = False
        result = True
        exp_dict = copy.deepcopy(expected_dict)
        exp_dict_direction = str(exp_dict['match_direction'])
        self.log('INFO', "exp_dict_direction {}".format(exp_dict_direction))

        if isinstance(entry, list) is True:
        #if exp_dict_direction == "input-output":

            for each_dict in entry:
                self.log('INFO', "Expected dict {}".format(each_dict))

            for each_dict in entry:
                rec_dict = {}
                rec_dict['applications'] = []
                rec_dict['sfw_rule_name'] = str(each_dict['policies']['policy-information']['sfw-rule-name'])
                rec_dict['policy_name'] = str(each_dict['policies']['policy-information']['policy-name'])
                rec_dict['policy_state'] = str(each_dict['policies']['policy-information']['policy-state'])
                rec_dict['service_set_name'] = str(each_dict['policies']['policy-information']['service-set-name'])
                rec_dict['interface_name'] = str(each_dict['policies']['policy-information']['interface-name'])
                rec_dict['source_addresses'] = str(each_dict['policies']['policy-information']['source-addresses']['source-address']['address-name'])
                rec_dict['destination_addresses'] = str(each_dict['policies']['policy-information']['destination-addresses']['destination-address']['address-name'])
                rec_dict['policy_action'] = str(each_dict['policies']['policy-information']['policy-action']['action-type'])
                self.log('INFO', "exp_dict_direction {}".format(exp_dict_direction))
                if exp_dict_direction != "input-output":
                    rec_dict['match_direction'] = str(each_dict['policies']['policy-information']['match-direction'])
#                elif dir_flag == False:
                elif dir_flag is False:
                    exp_dict['match_direction'] = "input"
                    rec_dict['match_direction'] = str(each_dict['policies']['policy-information']['match-direction'])
                    dir_flag = True
                else:
                    exp_dict['match_direction'] = "output"
                    rec_dict['match_direction'] = str(each_dict['policies']['policy-information']['match-direction'])
                for each_dict1 in each_dict['policies']['policy-information']['applications']['application']:
                    rec_dict['applications'].append(str(each_dict1['application-name']))
                    self.log('INFO', "appname: {}".format(each_dict1['application-name']))
            if not utils.cmp_dicts(exp_dict, rec_dict):
                result = False
        else:
            each_dict = entry
            rec_dict = {}
            rec_dict['applications'] = []
            rec_dict['sfw_rule_name'] = str(each_dict['policies']['policy-information']['sfw-rule-name'])
            rec_dict['policy_name'] = str(each_dict['policies']['policy-information']['policy-name'])
            rec_dict['policy_state'] = str(each_dict['policies']['policy-information']['policy-state'])
            rec_dict['service_set_name'] = str(each_dict['policies']['policy-information']['service-set-name'])
            rec_dict['interface_name'] = str(each_dict['policies']['policy-information']['interface-name'])
            rec_dict['source_addresses'] = str(each_dict['policies']['policy-information']['source-addresses']['source-address']['address-name'])
            rec_dict['destination_addresses'] = str(each_dict['policies']['policy-information']['destination-addresses']['destination-address']['address-name'])
            rec_dict['policy_action'] = str(each_dict['policies']['policy-information']['policy-action']['action-type'])
            rec_dict['match_direction'] = str(each_dict['policies']['policy-information']['match-direction'])
            for each_dict1 in each_dict['policies']['policy-information']['applications']['application']:
                rec_dict['applications'].append(str(each_dict1['application-name']))
                self.log('INFO', "appname: {}".format(each_dict1['application-name']))
            if not utils.cmp_dicts(exp_dict, rec_dict):
                result = False
        del exp_dict
#        if result == False:
        if result is False:
            return self.fn_checkout(False, err_msg="Verification of SFW Policy failed")
        else:
            return self.fn_checkout(True)

    def get_usf_sfw_policy_hit_count(self):
        """Fetch SFW policy hit_count details as dictionary

        :rtype: bool

        """
        self.fn_checkin("Get SFW Policy hit-count detail")
        _xpath = 'policy-hit-count-service-router/policy-hit-count-service-router-entry'
        cmd = 'show services policies hit-count'
        entry = self.get_xml_output(cmd, xpath=_xpath)
        if entry is None:
            return self.fn_checkout(False, err_msg="Not able to retrieve SFW Policy hit_count details")
        else:
            self.fn_checkout(True)
            return entry

    def verify_usf_sfw_policy_hit_count(self, exp_dict, act_dict=None):
        """Fetch SFW policy hit_count details as dictionary
           :rtype: bool
        """
        self.fn_checkin("Verifying SFW Policy hit_count detail")

#        if act_dict == None:
        if act_dict is None:
            entry = self.get_usf_sfw_policy_hit_count()
        else:
            entry = act_dict

        for key in exp_dict:
            if key.startswith('min__') or key.startswith('max__') or key.startswith('neg__'):
                exp_dict[key] = int(exp_dict[key])
        if isinstance(entry, list) is True:
            self.log('INFO', "entry is list")
            for each_dict in entry:
                self.log('INFO', "Expected dict {}".format(each_dict))
            for each_dict in entry:
                if str(each_dict['policy-hit-count-service-router-direction']) == exp_dict['policy_direction'] and str(each_dict['policy-hit-count-service-router-policy-name']) == exp_dict['policy_name']:
                    rec_dict = {}
                    rec_dict['policy_name'] = str(each_dict['policy-hit-count-service-router-policy-name'])
                    rec_dict['policy_rule'] = str(each_dict['policy-hit-count-service-router-sfw-rule-name'])
                    rec_dict['policy_ss'] = str(each_dict['policy-hit-count-service-router-service-set'])
                    rec_dict['policy_interface'] = str(each_dict['policy-hit-count-service-router-interface'])
                    rec_dict['policy_direction'] = str(each_dict['policy-hit-count-service-router-direction'])
                    rec_dict['policy_count'] = int(each_dict['policy-hit-count-service-router-count'])

                    if not utils.cmp_dicts(exp_dict, rec_dict):
                        return self.fn_checkout(False, err_msg="Verification of SFW Policy failed")
                    else:
                        return self.fn_checkout(True)
                else:
                    continue

        else:
            self.log('INFO', "entry is dict")
            each_dict = entry
            if str(each_dict['policy-hit-count-service-router-direction']) == exp_dict['policy_direction'] and str(each_dict['policy-hit-count-service-router-policy-name']) == exp_dict['policy_name']:
                rec_dict = {}
                rec_dict['policy_name'] = str(each_dict['policy-hit-count-service-router-policy-name'])
                rec_dict['policy_rule'] = str(each_dict['policy-hit-count-service-router-sfw-rule-name'])
                rec_dict['policy_ss'] = str(each_dict['policy-hit-count-service-router-service-set'])
                rec_dict['policy_interface'] = str(each_dict['policy-hit-count-service-router-interface'])
                rec_dict['policy_direction'] = str(each_dict['policy-hit-count-service-router-direction'])
                rec_dict['policy_count'] = int(each_dict['policy-hit-count-service-router-count'])
                if not utils.cmp_dicts(exp_dict, rec_dict):
                    return self.fn_checkout(False, err_msg="Verification of SFW Policy failed")
                else:
                    return self.fn_checkout(True)
        return self.fn_checkout(False, err_msg="Verification of SFW Policy failed")

