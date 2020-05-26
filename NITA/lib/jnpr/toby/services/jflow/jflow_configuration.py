#!/usr/bin/python3
"""
This module contains API's for Inline Jflow configuration

__author__ = [''Manoj Kumar V']
__contact__ = 'vmanoj@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2018'

"""
import re
import pprint
import time
from jnpr.toby.services.services import services

class jflow_configuration(services):
    """
    Class for configuration of the inline jflow on any of the routers
    """

    def __init__(self, **kwargs):
        """
         Constructor to initialize all the attributes to None
        """
        super().__init__(**kwargs)

    def configure_inline_jflow(self, name=None, template_type=None, \
            template_version=None, flow_collector_ips=[], \
            flow_collector_src=None, family=None, \
            sampling_intf=[], **kwargs):
        """
        Configure Inline Jflow on the router

        This is a public routine used to configure/modify inline jflow configurations on a router.
        It will be a one line call from the robot file to configure/modify the inline jflow
        configurations. It will be helpful in case the user is trying to implement multiple
        jflow templates within the same topology in different test cases. This will avoid the
        confusion of multiple config yaml files for different test cases. Note that, user may
        still have to use the config yaml approach for protocols configurations.

        :param obj device
          **REQUIRED** device handle of the JFlow collector

        :param str name
          **REQUIRED** name of the inline jflow template being configured

        :param str template_type
          **REQUIRED** it is the name of the template being configured
             the structure should be same as that of RE-CLI. For example,
             ipv4-template needs to be parsed to configure ipv4 inline jflow template

        :param str template_version
          **REQUIRED** it is the inline jflow version
            User may parse 9 or 10, version9/ipfix will be choosen accordingly

        :param list flow_collector_ips
          **REQUIRED** list of flow collector IPs

        :param str flow_collector_src
          **REQUIRED** source address of export records

        :param str family
          **REQUIRED**  family to be sampled.
            For example, "inet" needs to be parsed to sample ipv4 traffic

        :param list sampling_intf
          **REQUIRED** list of sampling IFLs. Note that, a list to be parsed
            even if there is only one sampling interface

        :param list sampling_protocol_list
          **OPTIONAL** protocols to be sampled. List parsed will be used in
            firewall configuration

        :param str active_to
          **OPTIONAL** active timeout of the template being configured

        :param str inactive_to
          **OPTIONAL** inactive timeout of the template being configured

        :param str template_refresh_seconds
          **OPTIONAL** interval for template refresh packets in seconds

        :param str template_refresh_packets
          **OPTIONAL** interval for template refresh packets in packets

        :param str option_refresh_packets
          **OPTIONAL** interval for option refresh packets in packets

        :param str option_refresh_seconds
          **OPTIONAL** interval for option refresh packets in seconds

        :param str vlan_flow_key
          **OPTIONAL** set it to 1 if vlan needs to be configured as flow-key

        :param str oif_flow_key
          **OPTIONAL** set it to 1 if OIF needs to be configured as flow-key

        :param str direction_flow_key
          **OPTIONAL** set it to 1 if direction needs to be configured as
            flow-key

        :param str configured_domain_id
          **OPTIONAL** used to configure user-defined value for observation-domain-id

        :param str configured_template_id
          **OPTIONAL** used to configure user-defined value for template-id

        :param str configured_option_template_id
          **OPTIONAL** used to configure user-defined value for options-template-id

        :param str enable_nexthop_learning
          **OPTIONAL** set it to 1 if nexthop learning needs to be enabled

        :param str cflow_port
          **OPTIONAL** destination UDP port for export records, defaulted to 2055 if not parsed

        :param str instance_name
          **OPTIONAL** sampling instance name, defaulted to instance-1 if not parsed

        :param str instance_sampling_rate
          **OPTIONAL** sampling rate at instance level, defauled to 1 if not parsed

        :param str family_sampling_rate
          **OPTIONAL** sampling rate at family level, sampling rate at instance level is not
            configured if a value for this is parsed

        :param str direction
          **OPTIONAL** direction to apply for sampling, defaulted to ingress if not parsed

        :param str enable_zero_oif_gw_on_discard_knob
          **OPTIONAL** set it to 1 if zero-oif-gw-on-discard knob needs to be enabled

        :param str enable_sample_once_knob
          **OPTIONAL** set it to 1 if sample-once knob needs to be enabled

        :param str enable_flex_flow_sizing
          **OPTIONAL** set it to 1 if flex-flow-sizing needs to be enabled

        :param str bridge-flow-table-size
          **OPTIONAL** parse a value to set bridge-flow-table-size

        :param str vpls-flow-table-size
          **OPTIONAL** parse a value to set vpls-flow-table-size

        :param str ipv4-flow-table-size
          **OPTIONAL** parse a value to set ipv4-flow-table-size

        :param str ipv6-flow-table-size
          **OPTIONAL** parse a value to set ipv6-flow-table-size

        :param str mpls-flow-table-size
          **OPTIONAL** parse a value to set mpls-flow-table-size

        :param str sample_without_firewall 
          **OPTIONAL** set to 1 to enable sampling directly on the interface

        :param str export_rate
          **OPTIONAL** parse a value to set the flow-export-rate

        :param str action
          **OPTIONAL** parse the action of configuration, defauled to 'set' if not parsed
                    parse 'set' to configure
                    parse 'delete' to 'delete'
                    parse 'modify' to modify

        :param str commit_configs
          **OPTIONAL** set it to 'False' if configuarations need not be committed, defauled to
                       'True'

        :param str interface_family
          **OPTIONAL** parse appropriate family on which sampling needs to be enabled, if not parsed,
                       sampling will be enabled under 'family' argument which was parsed as a
                       mandatory argument. For example, bridge template can sample both vpls and
                       bridge families. If beidge template needs to sample vpls family, then parse
                       interface_family=vpls    family=bridge

        :param str enable_collector_vrf
          **OPTIONAL** set it to 1 if collector used is in user-defined-vrf

        :param dict collector_vrf_dict
          **OPTIONAL** created and parse a collector<-->vrf dictionary

        :param list fpc_slot_list
          **OPTIONAL** list of FPCs used by AE/IRB interfaces

        :param list sampling_source_ip_list
          **OPTIONAL** list of sampling source IPs under firewall

        :param list sampling_dst_ip_list
          **OPTIONAL** list of sampling destination IPs under firewall

        :param list sampling_source_port_list
          **OPTIONAL** list of sampling source ports under firewall

        :param list sampling_dst_port_list
          **OPTIONAL** list of sampling destination ports under firewall
        """

        if name is None:
            raise self.MissingMandatoryArgument('name')

        if not hasattr(self, 'template'):
            self.template = {}

        if name not in self.template.keys():
            self.template[name] = {}
        
        this = self.ptr = self.template[name]
        self.platform = self.get_chassis_platform_info()

        if template_type is not None and 'template_type' not in this.keys():
            this['template_type'] = template_type + '-template'
        elif template_type is None and 'template_type' not in this.keys():
            raise self.MissingMandatoryArgument('template_type')

        if template_version is not None and 'template_version' not in this.keys():
            if template_version == '9':
                this['template_version'] = 'version9'
            elif template_version == '10':
                this['template_version'] = 'version-ipfix'
        elif template_version is None and 'template_version' not in this.keys():
            raise self.MissingMandatoryArgument('template_version')

        if 'flow_collector_ips' not in this.keys() and not len(flow_collector_ips) == 0:
            this['flow_collector_ips'] = flow_collector_ips
        elif 'flow_collector_ips' not in this.keys() and len(flow_collector_ips) == 0:
            raise ValueError("Atleast one flow collector IP has to be parsed")

        if flow_collector_src is not None and 'flow_collector_src' not in this.keys():
            this['flow_collector_src'] = flow_collector_src
        elif flow_collector_src is not None and not this['flow_collector_src'] == flow_collector_src:
            this['flow_collector_src'] = flow_collector_src
        elif flow_collector_src is None and 'flow_collector_src' not in this.keys():
            raise self.MissingMandatoryArgument('flow_collector_src')

        if family is not None and 'family' not in this.keys():
            this['family'] = family
        elif family is None and 'family' not in this.keys():
            raise self.MissingMandatoryArgument('family')

        if 'sampling_intf' not in this.keys() and not len(sampling_intf) == 0:
            this['sampling_intf'] = sampling_intf
        elif 'sampling_intf' not in this.keys() and len(sampling_intf) == 0:
            raise ValueError("Atleast one sampling interface has to be parsed")


        this['jflow_type'] = 'inline_jflow'
        this['mode'] = kwargs.get('mode', 'enable')

        if this['mode'] == 'enable':
            this['sampling_protocol_list'] = kwargs.get('sampling_protocol_list', [])
            this['active_to'] = kwargs.get('active_to', 120)
            this['inactive_to'] = kwargs.get('inactive_to', 60)
            this['template_refresh_seconds'] = kwargs.get('template_refresh_seconds', None)
            this['template_refresh_packets'] = kwargs.get('template_refresh_packets', None)
            this['option_refresh_packets'] = kwargs.get('option_refresh_packets', None)
            this['option_refresh_seconds'] = kwargs.get('option_refresh_seconds', None)
            this['vlan_flow_key'] = kwargs.get('vlan_flow_key', False)
            this['oif_flow_key'] = kwargs.get('oif_flow_key', False)
            this['direction_flow_key'] = kwargs.get('direction_flow_key', False)
            this['configured_domain_id'] = kwargs.get('configured_domain_id', None)
            this['configured_template_id'] = kwargs.get('configured_template_id', None)
            this['configured_option_template_id'] = kwargs.get('configured_option_template_id', None)
            this['enable_tunnel_observation'] = kwargs.get('enable_tunnel_observation', False)
            this['enable_nexthop_learning'] = kwargs.get('enable_nexthop_learning', False)
            this['cflow_port'] = kwargs.get('cflow_port', 2055)
            this['instance_name'] = kwargs.get('instance_name', 'instance-1')
            this['instance_sampling_rate'] = kwargs.get('instance_sampling_rate', 1)
            this['family_sampling_rate'] = kwargs.get('family_sampling_rate', None)
            this['enable_bidirection_sampling'] = kwargs.get('enable_bidirection_sampling', False)
            this['direction'] = kwargs.get('direction', 'ingress')
            this['enable_zero_oif_gw_on_discard_knob'] = kwargs.get('enable_zero_oif_gw_on_discard_knob', False)
            this['enable_sample_once_knob'] = kwargs.get('enable_sample_once_knob', False)
            this['enable_flex_flow_sizing'] = kwargs.get('enable_flex_flow_sizing', False)
            this['bridge-flow-table-size'] = kwargs.get('bridge-flow-table-size', None)
            this['vpls-flow-table-size'] = kwargs.get('vpls-flow-table-size', None)
            this['ipv4-flow-table-size'] = kwargs.get('ipv4-flow-table-size', None)
            this['ipv6-flow-table-size'] = kwargs.get('ipv6-flow-table-size', None)
            this['mpls-flow-table-size'] = kwargs.get('mpls-flow-table-size', None)
            this['sample_without_firewall'] = kwargs.get('sample_without_firewall', False)
            this['export_rate'] = kwargs.get('export_rate', None)
            this['action'] = str(kwargs.get('action', 'set'))
            this['commit_configs'] = kwargs.get('commit_configs', True)
            this['interface_family'] = kwargs.get('interface_family', None)
            this['enable_collector_vrf'] = kwargs.get('enable_collector_vrf', False)
            this['collector_vrf_dict'] = kwargs.get('collector_vrf_dict', {})
            this['fpc_slot_list'] = kwargs.get('fpc_slot_list', [])
            this['sampling_source_ip_list'] = kwargs.get('sampling_source_ip_list', [])
            this['sampling_dst_ip_list'] = kwargs.get('sampling_dst_ip_list', [])
            this['sampling_source_port_list'] = kwargs.get('sampling_source_port_list', [])
            this['sampling_dst_port_list'] = kwargs.get('sampling_dst_port_list', [])
        elif this['mode'] == 'modify':
            for arg in kwargs:
                this[arg] = kwargs.get(arg)

        pprint.pprint(self.template)

        self._configure_template(name=name, **kwargs)
        self._configure_forwarding_options(name=name)
        self._configure_sampling_instance(name=name, **kwargs)
        self._configure_sampling_on_interfaces(name=name)
        self._configure_firewall_filter(name=name)
    
        self.log("command list is:")
        self.log(self.cmd_list)

        if this['commit_configs'] is not True:
            return self.config()
        else:
            self.config()
            return self.commit()

    def _configure_template(self, name=None, **kwargs):
        """
        Configures inline-jflow template under 'set services' hierarchy

        :param str name
          **REQUIRED** the template name that is being configured
        """
        this = self.template[name]

        delete_template_refresh_seconds = kwargs.get('delete_template_refresh_seconds', False)
        delete_template_refresh_packets = kwargs.get('delete_template_refresh_packets', False)
        delete_option_refresh_packets = kwargs.get('delete_option_refresh_packets', False)
        delete_option_refresh_seconds = kwargs.get('delete_option_refresh_seconds', False)
        delete_vlan_flow_key = kwargs.get('delete_vlan_flow_key', False)
        delete_oif_flow_key = kwargs.get('delete_oif_flow_key', False)
        delete_direction_flow_key = kwargs.get('delete_direction_flow_key', False)
        delete_configured_template_id = kwargs.get('delete_configured_template_id', False)
        delete_configured_domain_id = kwargs.get('delete_configured_domain_id', False)
        delete_configured_option_template_id = kwargs.get('delete_configured_option_template_id', False)
        delete_enable_nexthop_learning = kwargs.get('delete_enable_nexthop_learning', False)

        if this['action'] is 'set':
            cmd_str = "{} services flow-monitoring {} template {}".format(this['action'], this['template_version'], name)
            self.cmd_add("{} flow-active-timeout {}".format(cmd_str, this['active_to']))
            self.cmd_add("{} flow-inactive-timeout {}".format(cmd_str, this['inactive_to']))
            self.cmd_add("{} {}".format(cmd_str, this['template_type']))

            if this['template_refresh_seconds'] is not None:
                self.cmd_add("{} template-refresh-rate seconds {}".format(cmd_str, this['template_refresh_seconds']))
            if this['template_refresh_packets'] is not None:
                self.cmd_add("{} template-refresh-rate packets {}".format(cmd_str, this['template_refresh_packets']))
            if this['option_refresh_packets'] is not None:
                self.cmd_add("{} option-refresh-rate packets {}".format(cmd_str, this['option_refresh_packets']))
            if this['option_refresh_seconds'] is not None:
                self.cmd_add("{} option-refresh-rate seconds {}".format(cmd_str, this['option_refresh_seconds']))
            if this['vlan_flow_key'] is not False:
                self.cmd_add("{} flow-key vlan-id".format(cmd_str))
            if this['oif_flow_key'] is not False:
                self.cmd_add("{} flow-key output-interface".format(cmd_str))
            if this['direction_flow_key'] is not False:
                self.cmd_add("{} flow-key flow-direction".format(cmd_str))
            if this['enable_nexthop_learning'] is not False:
                self.cmd_add("{} nexthop-learning enable".format(cmd_str))
            if this['configured_template_id'] is not None:
                self.cmd_add("{} template-id {}".format(cmd_str, this['configured_template_id']))
            if this['configured_domain_id'] is not None and this['template_version'] == 'version-ipfix':
                self.cmd_add("{} observation-domain-id {}".format(cmd_str, this['configured_domain_id']))
            if this['configured_domain_id'] is not None and this['template_version'] == 'version9':
                self.cmd_add("{} source-id {}".format(cmd_str, this['configured_domain_id']))
            if this['configured_option_template_id'] is not None:
                self.cmd_add("{} option-template-id {}".format(cmd_str, this['configured_option_template_id']))
            if this['enable_nexthop_learning'] is not False:
                self.cmd_add("{} nexthop-learning enable".format(cmd_str))
        else:
            cmd_str = "{} services flow-monitoring {} template {}".format(this['action'], this['template_version'], name)

            if delete_template_refresh_seconds:
                self.cmd_add("{} template-refresh-rate seconds".format(cmd_str))
                this['template_refresh_seconds'] = None
            if delete_template_refresh_packets:
                self.cmd_add("{} template-refresh-rate packets".format(cmd_str))
                this['template_refresh_packets'] = None
            if delete_option_refresh_packets:
                self.cmd_add("{} option-refresh-rate packets".format(cmd_str))
                this['option_refresh_packets'] = None
            if delete_option_refresh_seconds:
                self.cmd_add("{} option-refresh-rate seconds".format(cmd_str))
                this['option_refresh_seconds'] = None
            if delete_vlan_flow_key:
                self.cmd_add("{} flow-key vlan-id".format(cmd_str))
                this['vlan_flow_key'] = False
            if delete_oif_flow_key:
                self.cmd_add("{} flow-key output-interface".format(cmd_str))
                this['oif_flow_key'] = False
            if delete_direction_flow_key:
                self.cmd_add("{} flow-key flow-direction".format(cmd_str))
                this['direction_flow_key'] = False
            if delete_configured_template_id:
                self.cmd_add("{} template-id".format(cmd_str))
                this['configured_template_id'] = None
            if delete_configured_domain_id and this['template_version'] is 'version-ipfix':
                self.cmd_add("{} observation-domain-id".format(cmd_str))
                this['configured_domain_id'] = None
            if delete_configured_domain_id and this['template_version'] is 'version9':
                self.cmd_add("{} source-id".format(cmd_str))
                this['configured_domain_id'] = None
            if delete_configured_option_template_id:
                self.cmd_add("{} option-template-id".format(cmd_str))
                this['configured_option_template_id'] = None
            if delete_enable_nexthop_learning:
                self.cmd_add("{} nexthop-learning".format(cmd_str))
                this['enable_nexthop_learning'] = False


    def _configure_forwarding_options(self, name=None):
        """
        Configured inline jflow 'set forwarding-options' hierarchy

        :param str name
          **REQUIRED** name of the inline jflow template
        """
        this = self.template[name]
        cmd_str = "{} forwarding-options sampling instance {}".format(this['action'], this['instance_name'])

        if this['action'] is 'set':
            if this['family_sampling_rate'] is not None:
                self.cmd_add("{} family {} input rate {}".format(cmd_str, this['family'], this['family_sampling_rate']))
            else:
                self.cmd_add("{} input rate {}".format(cmd_str, this['instance_sampling_rate']))

            cmd_str = "{} family {} output".format(cmd_str, this['family'])

            self.cmd_add("{} inline-jflow source-address {}".format(cmd_str, this['flow_collector_src']))
        
            if this['export_rate'] is not None:
                self.cmd_add("{} inline-jflow flow-export-rate {}".format(cmd_str, this['export_rate']))

            if this['enable_collector_vrf'] is not False:
                for ip in this['collector_vrf_dict'].keys():
                    cmd_str_ip = "{} flow-server {}".format(cmd_str, ip)
                    self.cmd_add("{} port {}".format(cmd_str_ip, this['cflow_port']))
                    self.cmd_add("{} {} template {}".format(cmd_str_ip, this['template_version'], name))
                    self.cmd_add("{} routing-instance {}".format(cmd_str_ip, this['collector_vrf_dict'][ip]))
            else:
                for ip in this['flow_collector_ips']:
                    cmd_str_ip = "{} flow-server {}".format(cmd_str, ip)
                    self.cmd_add("{} port {}".format(cmd_str_ip, this['cflow_port']))
                    self.cmd_add("{} {} template {}".format(cmd_str_ip, this['template_version'], name))

    def _configure_sampling_instance(self, name=None, **kwargs):
        """
        Maps the sampling instance to appropriate FPC slot

        :param str name
          **REQUIRED** name of the inline jflow template
        """
        this = self.template[name]

        delete_enable_flex_flow_sizing = kwargs.get('delete_enable_flex_flow_sizing', False)
        delete_enable_zero_oif_gw_on_discard_knob = kwargs.get('delete_enable_zero_oif_gw_on_discard_knob', False)
        delete_bridge_flow_table_size = kwargs.get('delete_bridge_flow_table_size', False)
        delete_vpls_flow_table_size = kwargs.get('delete_vpls_flow_table_size', False)
        delete_ipv4_flow_table_size = kwargs.get('delete_ipv4_flow_table_size', False)
        delete_ipv6_flow_table_size = kwargs.get('delete_ipv6_flow_table_size', False)
        delete_mpls_flow_table_size = kwargs.get('delete_mpls_flow_table_size', False)

        for intf_index in range(len(this['sampling_intf'])):
            if re.search(r'ae', this['sampling_intf'][intf_index]) or re.search(r'irb', this['sampling_intf'][intf_index]):
                if len(this['fpc_slot_list']) == 0:
                    raise Exception('fpc_slot_list can not be none when sampling interface is ae/irb')

                for fpc_slot in this['fpc_slot_list']:
                    cmd_str = "{} chassis".format(this['action'])
                    if self.platform == 'MX104':
                        cmd_str = "{} afeb slot 0".format(cmd_str)
                    elif self.platform == 'MX80':
                        cmd_str = "{} tfeb slot 0".format(cmd_str)
                    else:
                        cmd_str = "{} fpc {}".format(cmd_str, fpc_slot)

                    if this['action'] is 'set':
                        self.cmd_add("{} sampling-instance {}".format(cmd_str, this['instance_name']))
                        if this['enable_flex_flow_sizing'] is not False:
                            self.cmd_add("{} inline-services flex-flow-sizing".format(cmd_str))
                        if this['enable_zero_oif_gw_on_discard_knob'] is not False:
                            self.cmd_add("{} inline-services report-zero-oif-gw-on-discard".format(cmd_str))
                        if this['bridge-flow-table-size'] is not None:
                            self.cmd_add("{} inline-services flow-table-size bridge-flow-table-size {}".format(cmd_str, this['bridge-flow-table-size']))
                        if this['vpls-flow-table-size'] is not None:
                            self.cmd_add("{} inline-services flow-table-size vpls-flow-table-size {}".format(cmd_str, this['vpls-flow-table-size']))
                        if this['ipv4-flow-table-size'] is not None:
                            self.cmd_add("{} inline-services flow-table-size ipv4-flow-table-size {}".format(cmd_str, this['ipv4-flow-table-size']))
                        if this['ipv6-flow-table-size'] is not None:
                            self.cmd_add("{} inline-services flow-table-size ipv6-flow-table-size {}".format(cmd_str, this['ipv6-flow-table-size']))
                        if this['mpls-flow-table-size'] is not None:
                            self.cmd_add("{} inline-services flow-table-size mpls-flow-table-size {}".format(cmd_str, this['mpls-flow-table-size']))
                    else:
                        if delete_enable_flex_flow_sizing is not False:
                            self.cmd_add("{} inline-services flex-flow-sizing".format(cmd_str))
                            this['enable_flex_flow_sizing'] = False
                        if delete_enable_zero_oif_gw_on_discard_knob is not False:
                            self.cmd_add("{} inline-services report-zero-oif-gw-on-discard".format(cmd_str))
                            this['enable_zero_oif_gw_on_discard_knob'] = False
                        if delete_bridge_flow_table_size is not False:
                            self.cmd_add("{} inline-services flow-table-size bridge-flow-table-size".format(cmd_str))
                            this['bridge-flow-table-size'] = None
                        if delete_vpls_flow_table_size is not False:
                            self.cmd_add("{} inline-services flow-table-size vpls-flow-table-size".format(cmd_str))
                            this['vpls-flow-table-size'] = None
                        if delete_ipv4_flow_table_size is not False:
                            self.cmd_add("{} inline-services flow-table-size ipv4-flow-table-size".format(cmd_str))
                            this['ipv4-flow-table-size'] = None
                        if delete_ipv6_flow_table_size is not False:
                            self.cmd_add("{} inline-services flow-table-size ipv6-flow-table-size".format(cmd_str))
                            this['ipv6-flow-table-size'] = None
                        if delete_mpls_flow_table_size is not False:
                            self.cmd_add("{} inline-services flow-table-size mpls-flow-table-size".format(cmd_str))

            else:
                fpc_slot, pic_slot, port = self.get_fpc_pic_port_from_ifname(this['sampling_intf'][intf_index])
                cmd_str = "{} chassis".format(this['action'])
                if self.platform == 'MX104':
                    cmd_str = "{} afeb slot 0".format(cmd_str)
                elif self.platform == 'MX80':
                    cmd_str = "{} tfeb slot 0".format(cmd_str)
                else:
                    cmd_str = "{} fpc {}".format(cmd_str, fpc_slot)

                if this['action'] is 'set':
                    self.cmd_add("{} sampling-instance {}".format(cmd_str, this['instance_name']))
                    if this['enable_flex_flow_sizing'] is not False:
                        self.cmd_add("{} inline-services flex-flow-sizing".format(cmd_str))
                    if this['enable_zero_oif_gw_on_discard_knob'] is not False:
                        self.cmd_add("{} inline-services report-zero-oif-gw-on-discard".format(cmd_str))
                    if this['bridge-flow-table-size'] is not None:
                        self.cmd_add("{} inline-services flow-table-size bridge-flow-table-size {}".format(cmd_str, this['bridge-flow-table-size']))
                    if this['vpls-flow-table-size'] is not None:
                        self.cmd_add("{} inline-services flow-table-size vpls-flow-table-size {}".format(cmd_str, this['vpls-flow-table-size']))
                    if this['ipv4-flow-table-size'] is not None:
                        self.cmd_add("{} inline-services flow-table-size ipv4-flow-table-size {}".format(cmd_str, this['ipv4-flow-table-size']))
                    if this['ipv6-flow-table-size'] is not None:
                        self.cmd_add("{} inline-services flow-table-size ipv6-flow-table-size {}".format(cmd_str, this['ipv6-flow-table-size']))
                    if this['mpls-flow-table-size'] is not None:
                        self.cmd_add("{} inline-services flow-table-size mpls-flow-table-size {}".format(cmd_str, this['mpls-flow-table-size']))
                else:
                    if delete_enable_flex_flow_sizing is not False:
                        self.cmd_add("{} inline-services flex-flow-sizing".format(cmd_str))
                        this['enable_flex_flow_sizing'] = False
                    if delete_enable_zero_oif_gw_on_discard_knob is not False:
                        self.cmd_add("{} inline-services report-zero-oif-gw-on-discard".format(cmd_str))
                        this['enable_zero_oif_gw_on_discard_knob'] = False
                    if delete_bridge_flow_table_size is not False:
                        self.cmd_add("{} inline-services flow-table-size bridge-flow-table-size".format(cmd_str))
                        this['bridge-flow-table-size'] = None
                    if delete_vpls_flow_table_size is not False:
                        self.cmd_add("{} inline-services flow-table-size vpls-flow-table-size".format(cmd_str))
                        this['vpls-flow-table-size'] = None
                    if delete_ipv4_flow_table_size is not False:
                        self.cmd_add("{} inline-services flow-table-size ipv4-flow-table-size".format(cmd_str))
                        this['ipv4-flow-table-size'] = None
                    if delete_ipv6_flow_table_size is not False:
                        self.cmd_add("{} inline-services flow-table-size ipv6-flow-table-size".format(cmd_str))
                        this['ipv6-flow-table-size'] = None
                    if delete_mpls_flow_table_size is not False:
                        self.cmd_add("{} inline-services flow-table-size mpls-flow-table-size".format(cmd_str))
                        this['mpls-flow-table-size'] = None

    def _configure_sampling_on_interfaces(self, name=None):
        """
        This is a private routine which enabled sampling on the IFL parsed

        :param str name
          **REQUIRED** name of the inline jflow template
        """
        this = self.template[name]
        direction = None

        if this['interface_family'] is not None:
            family = this['interface_family']
        else:
            family = this['family']

        if this['action'] is 'set':
            if this['direction'] == 'ingress':
                direction = 'input'
            else:
                direction = 'output'

            for intf_index in range(len(this['sampling_intf'])):
                cmd_str = "{} interfaces {} family {}".format(this['action'], this['sampling_intf'][intf_index], family)
                if this['sample_without_firewall'] is not False:
                    self.cmd_add("{} sampling {}".format(cmd_str, direction))
                else:
                    filter_name = family + "_sample"
                    self.cmd_add("{} filter {} {}".format(cmd_str, direction, filter_name))

    def _configure_firewall_filter(self, name=None):
        """
        This is a private routine which configures the firewall filter

        :param str name
          **REQUIRED** name of the inline jflow template
        """
        this = self.template[name]

        if this['interface_family'] is not None:
            family = this['interface_family']
        else:
            family = this['family']

        filter_name = family + "_sample"
        counter_name = family + "_counter"

        if this['action'] is 'set':
            cmd_str = "{} firewall family {} filter {}".format(this['action'], family, filter_name)
        
            if not len(this['sampling_protocol_list']) == 0:
                for protocol_index in range(len(this['sampling_protocol_list'])):
                    if family == 'inet6':
                        self.cmd_add("{} term 0 from next-header {}".format(cmd_str, this['sampling_protocol_list'][protocol_index]))
                        self.cmd_add("{} term 1 then accept".format(cmd_str))
                    else:
                        self.cmd_add("{} term 0 from protocol {}".format(cmd_str, this['sampling_protocol_list'][protocol_index]))
                        self.cmd_add("{} term 1 then accept".format(cmd_str))
            if not len(this['sampling_source_ip_list']) == 0:
                for ip_index in range(len(this['sampling_source_ip_list'])):
                    self.cmd_add("{} term 0 from source-address {}".format(cmd_str, this['sampling_source_ip_list'][ip_index]))
                    self.cmd_add("{} term 1 then accept".format(cmd_str))
            if not len(this['sampling_dst_ip_list']) == 0:
                for ip_index in range(len(this['sampling_dst_ip_list'])):
                    self.cmd_add("{} term 0 from destination-address {}".format(cmd_str, this['sampling_dst_ip_list'][ip_index]))
                    self.cmd_add("{} term 1 then accept".format(cmd_str))
            if not len(this['sampling_source_port_list']) == 0:
                for port_index in range(len(this['sampling_source_port_list'])):
                    self.cmd_add("{} term 0 from source-port {}".format(cmd_str, this['sampling_source_port_list'][port_index]))
                    self.cmd_add("{} term 1 then accept".format(cmd_str))
            if not len(this['sampling_dst_port_list']) == 0:
                for port_index in range(len(this['sampling_dst_port_list'])):
                    self.cmd_add("{} term 0 from destination-port {}".format(cmd_str, this['sampling_dst_port_list'][port_index]))
                    self.cmd_add("{} term 1 then accept".format(cmd_str))
            self.cmd_add("{} term 0 then accept sample count {}".format(cmd_str, counter_name))

    def sleep_for_active_time_out(self, name=None):
        """
        Makes the script to sleep for configured value of active timeout of a particular template

        :param str name
          **REQUIRED** name of the inline jflow template
        """
        if name is None:
            raise ValueError("name is a mandatory argument")

        self.log("sleeping for active timeout")
        time.sleep(int(self.template[name]['active_to']))

    def sleep_for_inactive_time_out(self, name=None):
        """
        Makes the script to sleep for configured value of inactive timeout of a particular template

        :param str name
          **REQUIRED** name of the inline jflow template
        """
        if name is None:
            raise ValueError("name is a mandatory argument")

        self.log("sleeping for inactive timeout")
        time.sleep(int(self.template[name]['inactive_to']))

    def get_configured_value_in_template(self, name=None, key=None):
        """
        Returns the configured value of a particular key of the configured inline jflow template

        :param str name
          **REQUIRED** name of the inline jflow template

        :param key
          **REQUIRED** key for which value has to be returned
        """
        if name is None:
            raise ValueError("name is a mandatory argument")
        if key is None:
            raise ValueError("key is a mandatory argument")

        return self.template[name][key]
                
    def get_chassis_platform_info(self):
        """
         This method will get the platform of router on
         which sampling is applied.

        :return: String type , returns the chassis platform type

        :rtype: string

        """

        output = self.dh.cli(
            command='show chassis hardware | match chassis').response().replace('\r\n', '\n')
        return output.split()[-1]