# Copyright 2016- Juniper Networks
# Toby BBE development team
"""
A subscriber class used to initialize the subscriber attributes in bbe yaml file
"""
import abc
import collections
from jnpr.toby.bbe.version import get_bbe_version
import os


__author__ = ['Yong Wang/Donald/Subramani Sadasivam']
__credits__ = ['Benjamin Schurman']
__contact__ = 'ywang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()

# For robot framework
ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
ROBOT_LIBRARY_VERSION = get_bbe_version()

McastRange = collections.namedtuple('McastRange', 'start, step, count')

VlanRange = collections.namedtuple('VlanRange', 'start, \
                                                 step, \
                                                 repeat, \
                                                 length')
VlanRange.__doc__ = """Vlan range for inner or outer vlans.

Fields:
    start: integer, VLAN start id
    step: integer, VLAN id step
    repeat: integer, VLAN id repeat. E.g., if start=1, step=1, repeat=2,
            VLAN ids is like 1122334455...
    length: vlan sequence length
"""

DHCPOption = collections.namedtuple('DHCPOption', 'id, \
                                                   start, \
                                                   step, \
                                                   repeat, \
                                                   length, \
                                                   messages, \
                                                   entid, \
                                                   entid_step')
DHCPOption.__doc__ = """DHCP option class.

This class is used for DHCPv4 option 82 circuit_id and remote_id, option 60
as well ass DHCPv6 option 18 interface_id

Fields:
    id: string, option base name
    start: integer, option start id
    step: integer, option id step
    repeat: integer, option id repeat.
    messages: string, tlv include in messages
    entid: enterprise id for v6 remoteid
    entid_step: enterprise id step for v6 remote id
"""

class SubscriberDefault:
    """Default values for subscribers

    """
    # for both vlan and svlan
    VLAN_START = 1
    VLAN_STEP = 1
    VLAN_REPEAT = 1
    VLAN_LENGTH = 4094

    PPP_USERNAME = 'DEFAULTUSER'
    PPP_PASSWORD = 'joshua'
    PPP_DOMAINNAME = ''
    PPP_AUTH_METHOD = 'pap_or_chap'  # ixia support chap |pap |none| chap_or_pap
    PPP_KA_INTERVAL = 120
    PPP_TERMINATION = 'local'  # user config could be l2tp

    # for all options: option82, option37, option18, option60, option72, option23
    OPTION_CIRCUIT_ID = 'circuit'
    OPTION_REMOTE_ID = 'remote'
    OPTION_SUBSCRIBER_ID = 'subscriber'
    OPTION_VENDOR_CLASS_ID = 'vendorid'
    OPTION_WWW_SERVER = '0.0.0.0'
    OPTION_DNS_SERVER = '0.0.0.0.0.0.0.0'
    OPTION_START = 1
    OPTION_STEP = 1
    OPTION_REPEAT = 1
    OPTION_LENGTH = ''
    OPTION_ENTERPRISE_ID = '1'
    OPTION_ENTERPRISE_ID_STEP = '0'
    OPTION_TLV_INCLUDE_IN_MESSAGES = 'kDiscover kRequest'


class Subscribers(abc.ABC):
    """Abstract Base Class of subscribers.

    This class and its child classes wrap the data from bbevar (which is
    the result of parsing topology and BBE configuration file). Subscriber
    classes provides properties to access subscriber related configuration
    data.

    Subclass inherits properties defined in this abstract base class,
    and defines new properties. When needed, child classes should override
    properties in this class if inherited one is inappropriate.

    """

    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Common initialization

        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe'
        :param tag: subscriber group tag
        """
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        self.__device_id = rinterface.device_id
        self.__device_name = rinterface.device_name
        self.__interface_id = rinterface.interface_id
        self.__subscribers_type = protocol
        self.__tag = group_config.get('tag', 'unknown')
        self.__count = group_config.get('count', 0)
        if 'SUB_COUNT' in os.environ:
            self.__count = int(os.environ['SUB_COUNT'])
        self.__family = group_config.get('family', 'unknown')
        if 'SUB_FAMILY' in os.environ:
            self.__family = os.environ['SUB_FAMILY']
        self.__rt_device_id = rtinterface.device_id
        self.__rt_port = rtinterface.interface_pic
        self.__ri = group_config.get('ri', 'default')
        self.__csr = group_config.get('csr', 0)
        if 'SUB_CSR' in os.environ:
            self.__csr = int(os.environ['SUB_CSR'])
        self.__clr = group_config.get('clr', 0)
        if 'SUB_CLR' in os.environ:
            self.__clr = int(os.environ['SUB_CLR'])
        self.has_igmp = group_config.get('igmp', None)
        self.single_session = group_config.get('single-session', None)
        self.dhcpv6_gateway = group_config.get('dhcpv6-gateway', None)
        # custom config, overides single value gateway if exists. it is a dict.
        self.dhcpv6_gateway_custom = group_config.get('dhcpv6-gateway-custom', None)
        self.dhcpv4_gateway = group_config.get('dhcpv4-gateway', None)
        self.rapid_commit = group_config.get('rapid-commit', None)
        # custom config, overides single value gateway if exists. it is a dict.
        self.dhcpv4_gateway_custom = group_config.get('dhcpv4-gateway-custom', None)
        self.rt_state = 'stopped'
        self.subinfo = group_config.get('subscriber-info', None)
        if self.has_igmp:
            self.rt_igmp_handle = None
            self.rt_igmp_group_handle = None
            self.rt_igmp_source_handle = None
            self.igmp_version = self.has_igmp.get('version', '2')
            self.igmp_filter_mode = self.has_igmp.get('filter-mode', 'include')
            self.igmp_iptv = self.has_igmp.get('iptv', None)
            self.igmp_group_enable = self.has_igmp.get('group', None)
            if self.igmp_group_enable:
                igmp_group_start = self.igmp_group_enable.get('start', '234.0.0.1')
                igmp_group_step = self.igmp_group_enable.get('step', '0.0.0.1')
                igmp_group_count = self.igmp_group_enable.get('count', '1')
                self.igmp_mcast_group_range = McastRange(igmp_group_start, igmp_group_step, igmp_group_count)
                self.igmp_one_group_per_sub = self.igmp_group_enable.get('one-group-per-sub', False)
                self.igmp_group_range_count = self.igmp_group_enable.get('range-count', '1')

            self.igmp_source_enable = self.has_igmp.get('source', None)
            if self.igmp_source_enable:
                igmp_src_start = self.igmp_source_enable.get('start', '234.0.0.1')
                igmp_src_step = self.igmp_source_enable.get('step', '0.0.0.1')
                igmp_src_count = self.igmp_source_enable.get('count', '1')
                self.igmp_mcast_source_range = McastRange(igmp_src_start, igmp_src_step, igmp_src_count)
                self.igmp_source_range_count = self.igmp_source_enable.get('range-count', '1')
        self.has_mld = group_config.get('mld', None)
        if self.has_mld:
            self.rt_mld_handle = None
            self.rt_mld_group_handle = None
            self.rt_mld_source_handle = None
            self.mld_version = self.has_mld.get('version', '1')
            self.mld_filter_mode = self.has_mld.get('filter-mode', 'include')
            self.mld_iptv = self.has_mld.get('iptv', None)
            self.mld_group_enable = self.has_mld.get('group', None)
            if self.mld_group_enable:
                mld_group_start = self.mld_group_enable.get('start', 'FF02::1')
                mld_group_step = self.mld_group_enable.get('step', '::1')
                mld_group_count = self.mld_group_enable.get('count', '1')
                self.mld_mcast_group_range = McastRange(mld_group_start, mld_group_step, mld_group_count)
                self.mld_one_group_per_sub = self.mld_group_enable.get('one-group-per-sub', False)
                self.mld_group_range_count = self.mld_group_enable.get('range-count', '1')
            self.mld_source_enable = self.has_mld.get('source', None)
            if self.mld_source_enable:
                mld_src_start = self.mld_source_enable.get('start', '1000::1')
                mld_src_step = self.mld_source_enable.get('step', '::1')
                mld_src_count = self.mld_source_enable.get('count', '1')
                self.mld_mcast_source_range = McastRange(mld_src_start, mld_src_step, mld_src_count)
                self.mld_source_group_range_count = self.mld_source_enable.get('range-count', '1')
        self.mac = group_config.get('mac', None)
        self.mac_step = group_config.get('mac_step', None)
        self.has_ancp = group_config.get('ancp', None)
        if self.has_ancp:
            self.ancp_count = self.has_ancp.get('count', '1')
            self.ancp_lines_per_node = self.has_ancp.get('lines-per-node', '1')
            self.ancp_dsl_type = self.has_ancp.get('dsl-type', None)
            self.ancp_pon_type = self.has_ancp.get('pon-type', None)
            self.ancp_dut_ip = self.has_ancp.get('dut-ip', '100.0.0.1')
            self.ancp_ip = self.has_ancp.get('ip', '20.20.0.2/24')
            self.ancp_ip_step = self.has_ancp.get('ip-step', '0.0.0.1')
            #self.ancp_mask = self.has_ancp.get('mask', '24')
            self.ancp_gateway = self.has_ancp.get('gateway', '20.20.0.1')
            self.ancp_gateway_step = self.has_ancp.get('gateway-step', None)
            self.ancp_vlan_allocation_model = self.has_ancp.get('vlan-allocation-model', '1_1')
            self.ancp_enable_remoteid = self.has_ancp.get('remote-id-enable', None)
            self.ancp_flap_mode = self.has_ancp.get('flap-mode', None)
            self.ancp_vlan_enable = self.has_ancp.get('vlan', None)
            self.ancp_svlan_enable = self.has_ancp.get('svlan', None)
            self.ancp_vlan_range = None
            self.ancp_svlan_range = None
            self.ancp_start_rate = self.has_ancp.get('start-rate', 200)
            self.ancp_stop_rate = self.has_ancp.get('stop-rate', 200)
            self.ancp_port_up_rate = self.has_ancp.get('port-up-rate', 200)
            self.ancp_port_down_rate = self.has_ancp.get('port-down-rate', 200)
            if self.ancp_vlan_enable:
                vlan_start = self.ancp_vlan_enable.get('start', '1')
                vlan_step = self.ancp_vlan_enable.get('step', '1')
                vlan_repeat = self.ancp_vlan_enable.get('repeat', '1')
                vlan_length = self.ancp_vlan_enable.get('length', '4000')
                vlan_range = VlanRange(vlan_start, vlan_step, vlan_repeat, vlan_length)
                self.ancp_vlan_range = vlan_range
                self.ancp_vlan_tpid = self.ancp_vlan_enable.get('tpid', '0x8100')
            if self.ancp_svlan_enable:
                vlan_start = self.ancp_svlan_enable.get('start', '1')
                vlan_step = self.ancp_svlan_enable.get('step', '1')
                vlan_repeat = self.ancp_svlan_enable.get('repeat', '1')
                vlan_length = self.ancp_svlan_enable.get('length', '4000')
                vlan_range = VlanRange(vlan_start, vlan_step, vlan_repeat, vlan_length)
                self.ancp_svlan_range = vlan_range
                self.ancp_svlan_tpid = self.ancp_svlan_enable.get('tpid', '0x8100')
            self.rt_ancp_handle = None
            self.rt_ancp_line_handle = None

        self.__outstanding = group_config.get('outstanding', '1000')
        if 'SUB_OUTSTANDING' in os.environ:
            self.__outstanding = os.environ['SUB_OUTSTANDING']
        if 'v6' in self.__family or 'dual' in self.__family:
            self.__dhcpv6_ia_type = group_config.get('dhcpv6-ia-type', 'iana_iapd').lower()
            if 'SUB_DHCPV6_IA_TYPE' in os.environ:
                self.__dhcpv6_ia_type = os.environ['SUB_DHCPV6_IA_TYPE'].lower()
            self.__dhcpv6_iana_count = group_config.get('dhcpv6-iana-count', '1')
            self.__dhcpv6_iapd_count = group_config.get('dhcpv6-iapd-count', '1')
        else:
            self.__dhcpv6_ia_type = None
            self.__dhcpv6_iana_count = None
            self.__dhcpv6_iapd_count = None

        self.__on_ae = isinstance(rinterface.interface_config.get('ae', None), dict)
        if self.__on_ae:
            self.__ae_bundle = rinterface.interface_config['ae'].get('bundle', '')
            self.__ae_active = rinterface.interface_config['ae'].get('active', False)
            self.__ae_enable = rinterface.interface_config['ae'].get('enable', False)
        else:
            self.__ae_bundle = ''
            self.__ae_active = False
            self.__ae_enable = False

        self.__router_port = self.__ae_bundle if self.__on_ae and self.__ae_active else rinterface.interface_pic

        self.__vlan_encap = group_config.get('vlan-encap', 'none')

        if self.__vlan_encap == 'none':
            self.__vlan_range = None
        else:
            if isinstance(group_config.get('vlan', None), dict):
                vlan_start = group_config['vlan'].get('start', SubscriberDefault.VLAN_START)
                if 'SUB_VLAN_START' in os.environ:
                    vlan_start = os.environ['SUB_VLAN_START']
                vlan_step = group_config['vlan'].get('step', SubscriberDefault.VLAN_STEP)
                if 'SUB_VLAN_STEP' in os.environ:
                    vlan_step = os.environ['SUB_VLAN_STEP']
                vlan_repeat = group_config['vlan'].get('repeat', SubscriberDefault.VLAN_REPEAT)
                if 'SUB_VLAN_REPEAT' in os.environ:
                    vlan_repeat = os.environ['SUB_VLAN_REPEAT']
                vlan_length = group_config['vlan'].get('length', SubscriberDefault.VLAN_LENGTH)
                if 'SUB_VLAN_LENGTH' in os.environ:
                    vlan_length = os.environ['SUB_VLAN_LENGTH']
                vlan_range = VlanRange(vlan_start, vlan_step, vlan_repeat, vlan_length)
                self.vlan_tpid = group_config['vlan'].get('tpid', '0x8100')
            else:
                vlan_range = VlanRange(SubscriberDefault.VLAN_START, SubscriberDefault.VLAN_STEP,
                                       SubscriberDefault.VLAN_REPEAT, SubscriberDefault.VLAN_LENGTH)
            self.__vlan_range = vlan_range


        if self.__vlan_encap == 'svlan' or self.__vlan_encap == 'dsvlan':
            if isinstance(group_config.get('svlan', None), dict):
                svlan_start = group_config['svlan'].get('start', SubscriberDefault.VLAN_START)
                if 'SUB_SVLAN_START' in os.environ:
                    svlan_start = os.environ['SUB_SVLAN_START']
                svlan_step = group_config['svlan'].get('step', SubscriberDefault.VLAN_STEP)
                if 'SUB_SVLAN_STEP' in os.environ:
                    svlan_step = os.environ['SUB_SVLAN_STEP']
                svlan_repeat = group_config['svlan'].get('repeat', SubscriberDefault.VLAN_REPEAT)
                if 'SUB_SVLAN_REPEAT' in os.environ:
                    svlan_repeat = os.environ['SUB_SVLAN_REPEAT']
                svlan_length = group_config['svlan'].get('length', SubscriberDefault.VLAN_LENGTH)
                if 'SUB_SVLAN_LENGTH' in os.environ:
                    svlan_length = os.environ['SUB_SVLAN_LENGTH']
                svlan_range = VlanRange(svlan_start, svlan_step, svlan_repeat, svlan_length)
                self.svlan_tpid = group_config['svlan'].get('tpid', '0x8100')
            else:
                svlan_range = VlanRange(SubscriberDefault.VLAN_START, SubscriberDefault.VLAN_STEP,
                                        SubscriberDefault.VLAN_REPEAT, SubscriberDefault.VLAN_LENGTH)
            self.__svlan_range = svlan_range
        else:
            self.__svlan_range = None

        ##DHCPv6 option reuqest(option 6)
        if self.__family != 'ipv4' and 'option6' in group_config.keys():
            self.has_option6 = True
            self.option6 = group_config['option6']
        else:
            self.has_option6 = False

        ##DHCPv6 option reconfigure accept(option 20)
        if self.__family != 'ipv4' and 'option20' in group_config.keys():
            if group_config['option20']:
                self.has_option20 = True
            else:
                self.has_option20 = False
        else:
            self.has_option20 = False
        # Support having option18 and option37 kwys in config without values, using defaults.
        # DHCPv6 option 18 interface-id
        if self.__family != 'ipv4' and 'option18' in group_config.keys():
            self.__has_option18 = True
        else:
            self.__has_option18 = False

        if self.__has_option18:
            if isinstance(group_config.get('option18', None), dict):  # config exists
                op_id = group_config['option18'].get('interface-id', SubscriberDefault.OPTION_CIRCUIT_ID)
                op_start = group_config['option18'].get('interface-id-start', SubscriberDefault.OPTION_START)
                op_step = group_config['option18'].get('interface-id-step', SubscriberDefault.OPTION_STEP)
                op_repeat = group_config['option18'].get('interface-id-repeat', SubscriberDefault.OPTION_REPEAT)
                op_length = group_config['option18'].get('interface-id-length', SubscriberDefault.OPTION_LENGTH)
                op_tlv_include_in_messages = group_config['option18'].get('tlv-include-in-messages', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES)
                self.__option18 = DHCPOption(op_id, op_start, op_step, op_repeat, op_length, op_tlv_include_in_messages, '0', '0')
            else:
                self.__option18 = DHCPOption(SubscriberDefault.OPTION_CIRCUIT_ID,
                                             SubscriberDefault.OPTION_START,
                                             SubscriberDefault.OPTION_STEP,
                                             SubscriberDefault.OPTION_REPEAT,
                                             SubscriberDefault.OPTION_LENGTH,
                                             SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES,
                                             '0',
                                             '0')
        else:
            self.__option18 = None

        # DHCPv6 option 37 remote-id
        if self.__family != 'ipv4' and 'option37' in group_config.keys():
            self.__has_option37 = True
        else:
            self.__has_option37 = False

        if self.__has_option37:
            if isinstance(group_config.get('option37', None), dict):  # config exists
                op_id = group_config['option37'].get('remote-id', SubscriberDefault.OPTION_REMOTE_ID)
                op_start = group_config['option37'].get('remote-id-start', SubscriberDefault.OPTION_START)
                op_step = group_config['option37'].get('remote-id-step', SubscriberDefault.OPTION_STEP)
                op_repeat = group_config['option37'].get('remote-id-repeat', SubscriberDefault.OPTION_REPEAT)
                op_length = group_config['option37'].get('remote-id-length', SubscriberDefault.OPTION_LENGTH)
                op_tlv_include_in_messages = group_config['option37'].get('tlv-include-in-messages', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES)
                op_entid = group_config['option37'].get('enterprise-id', SubscriberDefault.OPTION_ENTERPRISE_ID)
                op_entid_step = group_config['option37'].get('enterprise-id-step',
                                                             SubscriberDefault.OPTION_ENTERPRISE_ID_STEP)
                self.__option37 = DHCPOption(op_id, op_start, op_step, op_repeat, op_length, op_tlv_include_in_messages, op_entid, op_entid_step)
            else:
                self.__option37 = DHCPOption(SubscriberDefault.OPTION_REMOTE_ID,
                                             SubscriberDefault.OPTION_START,
                                             SubscriberDefault.OPTION_STEP,
                                             SubscriberDefault.OPTION_REPEAT,
                                             SubscriberDefault.OPTION_LENGTH,
                                             SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES,
                                             SubscriberDefault.OPTION_ENTERPRISE_ID,
                                             SubscriberDefault.OPTION_ENTERPRISE_ID_STEP)
        else:
            self.__option37 = None

        # Option 23 DNS Recursive Name Server
        self.__has_option23 = True if 'option23' in group_config.keys() else False
        if self.__has_option23:
            if isinstance(group_config.get('option23', None), dict): # config exists
                op_id = group_config['option23'].get('dns-server', SubscriberDefault.OPTION_DNS_SERVER)
                self.__option23 = DHCPOption(op_id, '0', '0', '0', '0', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES, '0', '0')
            else:
                self.__option23 = DHCPOption(SubscriberDefault.OPTION_DNS_SERVER,'0', '0', '0', '0', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES, '0', '0')
        else:
            self.__option23 = None

        # DHCPv6 option 38 subscriber-id
        if self.__family != 'ipv4' and 'option38' in group_config.keys():
            self.has_option38 = True
        else:
            self.has_option38 = False
        if self.has_option38:
            if isinstance(group_config.get('option38', None), dict):  # config exists
                op_id = group_config['option38'].get('subscriber-id', SubscriberDefault.OPTION_SUBSCRIBER_ID)
                op_start = group_config['option38'].get('subscriber-id-start', SubscriberDefault.OPTION_START)
                op_step = group_config['option38'].get('subscriber-id-step', SubscriberDefault.OPTION_STEP)
                op_repeat = group_config['option38'].get('subscriber-id-repeat', SubscriberDefault.OPTION_REPEAT)
                op_length = group_config['option38'].get('subscriber-id-length', SubscriberDefault.OPTION_LENGTH)
                op_tlv_include_in_messages = group_config['option38'].get('tlv-include-in-messages', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES)
                self.option38 = DHCPOption(op_id, op_start, op_step, op_repeat, op_length, op_tlv_include_in_messages, '0', '0')
            else:
                self.option38 = DHCPOption(SubscriberDefault.OPTION_SUBSCRIBER_ID,
                                           SubscriberDefault.OPTION_START,
                                           SubscriberDefault.OPTION_STEP,
                                           SubscriberDefault.OPTION_REPEAT,
                                           SubscriberDefault.OPTION_LENGTH,
                                           SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES,
                                           '0',
                                           '0')

        # DHCPv4 option 60 Vendor Class Identifier
        self.__has_option60 = True if 'option60' in group_config.keys() else False
        if self.__has_option60:
            if isinstance(group_config.get('option60', None), dict): # config exists
                op_id = group_config['option60'].get('vendor-class-id', SubscriberDefault.OPTION_VENDOR_CLASS_ID)
                op_start = group_config['option60'].get('vendor-class-id-start', SubscriberDefault.OPTION_START)
                op_step = group_config['option60'].get('vendor-class-id-step', SubscriberDefault.OPTION_STEP)
                op_repeat = group_config['option60'].get('vendor-class-id-repeat', SubscriberDefault.OPTION_REPEAT)
                op_length = group_config['option60'].get('vendor-class-id-length', SubscriberDefault.OPTION_LENGTH)
                op_tlv_include_in_messages = group_config['option60'].get('tlv-include-in-messages', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES)
                self.__option60 = DHCPOption(op_id, op_start, op_step, op_repeat, op_length, op_tlv_include_in_messages, '0', '0')
            else:
                self.__option60 = DHCPOption(SubscriberDefault.OPTION_VENDOR_CLASS_ID,
                                                 SubscriberDefault.OPTION_START,
                                                 SubscriberDefault.OPTION_STEP,
                                                 SubscriberDefault.OPTION_REPEAT,
                                                 SubscriberDefault.OPTION_LENGTH,
                                                 SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES,
                                                 '0',
                                                 '0')
        else:
            self.__option60 = None

        # DHCPv4 option 72 WWW Server
        self.__has_option72 = True if 'option72' in group_config.keys() else False
        if self.__has_option72:
            if isinstance(group_config.get('option72', None), dict): # config exists
                op_id = group_config['option72'].get('www-server', SubscriberDefault.OPTION_WWW_SERVER)
                self.__option72 = DHCPOption(op_id, '0', '0', '0', '0', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES, '0', '0')
            else:
                self.__option72 = DHCPOption(SubscriberDefault.OPTION_WWW_SERVER,'0', '0', '0', '0', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES, '0', '0')
        else:
            self.__option72 = None

        self.__rt_device_group_handle = None
        self.__rt_ethernet_handle = None

    def start(self):
        """
        start subscriber
        :return:
        """
        rt_handle = t.get_handle(resource=self.rt_device_id)
        handles = self.rt_device_group_handle
        if not isinstance(handles, list):
            handles = [handles]
        # if self.has_ancp:
        #     handles.append(self.rt_ancp_handle)
        for handle in handles:
            rt_handle.invoke('client_action', handle=handle, action='start')
        self.rt_state = 'started'

    def stop(self):
        """
        stop subscriber
        :return:
        """
        rt_handle = t.get_handle(resource=self.rt_device_id)
        handles = self.rt_device_group_handle
        if not isinstance(handles, list):
            handles = [handles]
        # if self.has_ancp:
        #     handles.append(self.rt_ancp_handle)
        for handle in handles:
            rt_handle.invoke('client_action', handle=handle, action='stop')
        self.rt_state = 'stopped'

    def restart_down(self):
        """
        restart subs in down state
        :return:
        """
        rt_handle = t.get_handle(resource=self.rt_device_id)
        handles = self.rt_device_group_handle
        if not isinstance(handles, list):
            handles = [handles]
        if self.has_ancp:
            handles.append(self.rt_ancp_handle)
        for handle in handles:
            rt_handle.invoke('client_action', handle=handle, action='restart_down')

    def abort(self):
        """
        abort subs simulation
        :return:
        """
        rt_handle = t.get_handle(resource=self.rt_device_id)
        handles = self.rt_device_group_handle
        if not isinstance(handles, list):
            handles = [handles]
        if self.has_ancp:
            handles.append(self.rt_ancp_handle)
        for handle in handles:
            rt_handle.invoke('client_action', handle=handle, action='abort')
        self.rt_state = 'stopped'

    @property
    def rt_device_group_handle(self):
        """Get RT device group handle.

        :return: RT device group handle or None if not exist
        """
        return self.__rt_device_group_handle

    @rt_device_group_handle.setter
    def rt_device_group_handle(self, handle):
        """Set RT device group handle.

        :param h: RT device group handle.
        :return: None
        """
        self.__rt_device_group_handle = handle

    @property
    def rt_ethernet_handle(self):
        """Get RT ethernet handle.

        :return: RT ethernet handle or None if not exist
        """
        return self.__rt_ethernet_handle

    @rt_ethernet_handle.setter
    def rt_ethernet_handle(self, handle):
        """Set RT ethernet handle.

        :param h: RT ethernet handle.
        :return: None
        """
        self.__rt_ethernet_handle = handle

    @property
    def vlan_encap(self):
        """Het VLAN encapsulation

        VLAN encapsulation can be one of vlan | svlan | dvlan | dsvlan | none

        :return: string. VLAN encapsulation type.
        """
        return self.__vlan_encap


    @property
    def has_option18(self):
        """If subscriber has DHCPv6 option 18 interface-id

        :return: boolean
        """
        return self.__has_option18

    @property
    def option18(self):
        """Get DHCPv6 option 18 interface-id

        Usage:
            Tell if subscribers have option18 by calling obj.has_option18
            Or expect None return value.

        :return: DHCPOption object or None
        """
        return self.__option18

    @property
    def has_option60(self):
        """If subscriber has DHCPv4 option 60 vendor-class-id

        :return: boolean
        """
        return self.__has_option60

    @property
    def option60(self):
        """Get DHCPv4 option 60 vendor-class-id

        Usage:
            Tell if subscribers have option60 by calling obj.has_option60
            Or expect None return value.

        :return: DHCPOption object or None
        """
        return self.__option60

    @property
    def has_option72(self):
        """If subscriber has DHCPv4 option 72 Default WWW Server

        :return: boolean
        """
        return self.__has_option72

    @property
    def option72(self):
        """Get DHCPv4 option 72 Default WWW Server

        Usage:
            Tell if subscribers have option72 by calling obj.has_option72
            Or expect None return value.

        :return: DHCPOption object or None
        """
        return self.__option72

    @property
    def has_option23(self):
        """If subscriber has DHCPv6 option 23 DNS Recursive Name Server

        :return: boolean
        """
        return self.__has_option23

    @property
    def option23(self):
        """Get DHCPv6 option 23 DNS Recursive Name Server

        Usage:
            Tell if subscribers have option23 by calling obj.has_option23
            Or expect None return value.

        :return: DHCPOption object or None
        """
        return self.__option23
    
    @property
    def has_option37(self):
        """Subscirber has DHCPv6 option 37 remote-id

        :return: boolean
        """
        return self.__has_option37

    @property
    def option37(self):
        """Get DHCPv6 option 37 remote-id

        Usage:
            Tell if subscribers have option37 by calling obj.has_option37
            Or expect None return value.

        :return: DHCPOption object or None
        """
        return self.__option37

    @property
    def device_id(self):
        """Device id (e.g., 'r0') on which subscriber is defined

        :return: string tag name
        """
        return self.__device_id

    @property
    def device_name(self):
        """Physical device name (e.g., 'r1mx960wf') on which subscriber is defined

        :return: string tag name
        """
        return self.__device_name

    @property
    def interface_id(self):
        """Interface id (e.g., 'access0') on which subscriber is defined

        :return: string tag name
        """
        return self.__interface_id

    @property
    def tag(self):
        """Subscriber group tag as configured in BBE config yaml

        :return: string tag name
        """
        return self.__tag

    @property
    def count(self):
        """Subscriber count

        :return: 0 or positive integer of subscribers count
        """
        return self.__count

    @property
    def subscribers_type(self):
        """Subscriber type

        :return: String subscriber type -- 'dhcp', 'pppoe',' l2tp'
        """
        return self.__subscribers_type

    @property
    def protocol(self):
        """Protocol is the same as subscriber type

        subscribers_type is newly added. Leave protocol here for
        backward compatibility.

        :return: String subscriber type -- 'dhcp', 'pppoe',' l2tp'
        """
        return self.__subscribers_type

    @property
    def family(self):
        """Subscriber address family

        :return: String address family -- 'inet', 'inet6', 'dual'
        """
        return self.__family

    @property
    def router_port(self):
        """Subscriber router port

        :return: string router port without unit number, .e.g, 'xe-1/0/0'
        """
        return self.__router_port

    @property
    def rt_device_id(self):
        """Subscriber rt device id

        :return: string rt device id, .e.g, 'rt0'
        """
        return self.__rt_device_id

    @property
    def rt_port(self):
        """Subscriber rt port

        :return: string rt port, .e.g, '9/2'
        """
        return self.__rt_port

    @property
    def ri(self):
        """Subscriber routing instance

        :return: string routing instance name
        """
        return self.__ri

    @property
    def vlan_range(self):
        """Subscriber inner vlan range

        :return: VlanRange object of current vlan range. None if no VLAN is needed.
        """
        return self.__vlan_range

    @property
    def svlan_range(self):
        """Subscriber outer vlan range

        :return: VlanRange object of current svlan range. None if no SVLAN is needed.
        """
        return self.__svlan_range

    @property
    def csr(self):
        """Call setup rate

        :return: integer current csr value
        """
        return self.__csr

    @csr.setter
    def csr(self, new_csr):
        """Change csr to new_csr

        :param new_csr: integer rate
        :return: None
        """
        self.__csr = new_csr
        # ? we need to call rt to change right now
        #

    @property
    def clr(self):
        """Call release rate

        :return: integer current clr value
        """
        return self.__clr

    @clr.setter
    def clr(self, new_clr):
        """Change clr to new_clr

        :param new_clr: integer rate
        :return: None
        """
        self.__clr = new_clr
        #  if we need to call rt to change right now
        #

    @property
    def outstanding(self):
        """ outstanding count for login rate
        :return: integer
        """
        return self.__outstanding

    @outstanding.setter
    def outstanding(self, outstanding):
        """
        :param outstanding: change the value to the new
        :return: None
        """
        self.__outstanding = outstanding

    @property
    def on_ae(self):
        """If subscribers are on ae interface

        :return: boolean. True if using ae.
        """
        return self.__on_ae

    @property
    def dhcpv6_ia_type(self):
        """
        subscriber dhcpv6 IA type,
        :return: IA type
        """
        return self.__dhcpv6_ia_type

    @dhcpv6_ia_type.setter
    def dhcpv6_ia_type(self, iatype):
        """
        set dhcpv6_ia_type
        :param iatype:
        :return:
        """
        self.__dhcpv6_ia_type = iatype

    @property
    def dhcpv6_iana_count(self):
        """
        subscriber dhcpv6 IANA count,
        :return: IANA count
        """
        return self.__dhcpv6_iana_count

    @property
    def dhcpv6_iapd_count(self):
        """
        subscriber dhcpv6 IAPD count,
        :return: IAPD count
        """
        return self.__dhcpv6_iapd_count

    @property
    def ae_bundle(self):
        """AE bundle name

        :return: string. AE bundle name or empty string if not using ae
        """
        return self.__ae_bundle

    @property
    def is_ae_active(self):
        """If the interface is active ae member

        :return: boolean. True if active.
        """
        return self.__ae_enable


class DHCPSubscribers(Subscribers):
    """DHCP subscribers.

    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar

        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)

        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        self.has_softgre = True if 'softgre' in group_config.keys() else False
        if self.has_softgre:
            self.rt_gre_handle = None
            if isinstance(group_config.get('softgre', None), dict):  # config exists
                self.softgre_vlan_id = group_config['softgre'].get('vlan-id', None)
                self.softgre_vlan_id_step = group_config['softgre'].get('vlan-id-step', None)
                self.softgre_vlan_id_repeat = group_config['softgre'].get('vlan-id-repeat', None)
                self.softgre_source = group_config['softgre']['source']
                self.softgre_destination = group_config['softgre']['destination']
                self.softgre_gateway = group_config['softgre']['gateway']
                #self.softgre_mask = group_config['softgre']['mask']
                self.softgre_count = group_config['softgre']['count']
        # Support having only option82 key without customized values, using defaults
        self.__has_option82 = True if 'option82' in group_config.keys() else False
        if self.__has_option82:
            if isinstance(group_config.get('option82', None), dict): # config exists
                op_id = group_config['option82'].get('circuit-id', SubscriberDefault.OPTION_CIRCUIT_ID)
                op_start = group_config['option82'].get('circuit-id-start', SubscriberDefault.OPTION_START)
                op_step = group_config['option82'].get('circuit-id-step', SubscriberDefault.OPTION_STEP)
                op_repeat = group_config['option82'].get('circuit-id-repeat', SubscriberDefault.OPTION_REPEAT)
                op_length = group_config['option82'].get('circuit-id-length', SubscriberDefault.OPTION_LENGTH)
                op_tlv_include_in_messages = group_config['option82'].get('tlv-include-in-messages', SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES)
                self.__option82_aci = DHCPOption(op_id, op_start, op_step, op_repeat, op_length, op_tlv_include_in_messages, '0', '0')

                op_id = group_config['option82'].get('remote-id', SubscriberDefault.OPTION_REMOTE_ID)
                op_start = group_config['option82'].get('remote-id-start', SubscriberDefault.OPTION_START)
                op_step = group_config['option82'].get('remote-id-step', SubscriberDefault.OPTION_STEP)
                op_repeat = group_config['option82'].get('remote-id-repeat', SubscriberDefault.OPTION_REPEAT)
                op_length = group_config['option82'].get('remote-id-length', SubscriberDefault.OPTION_LENGTH)
                self.__option82_ari = DHCPOption(op_id, op_start, op_step, op_repeat, op_length, op_tlv_include_in_messages, '0', '0')
            else:
                self.__option82_aci = DHCPOption(SubscriberDefault.OPTION_CIRCUIT_ID,
                                                 SubscriberDefault.OPTION_START,
                                                 SubscriberDefault.OPTION_STEP,
                                                 SubscriberDefault.OPTION_REPEAT,
                                                 SubscriberDefault.OPTION_LENGTH,
                                                 SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES,
                                                 '0',
                                                 '0')

                self.__option82_ari = DHCPOption(SubscriberDefault.OPTION_REMOTE_ID,
                                                 SubscriberDefault.OPTION_START,
                                                 SubscriberDefault.OPTION_STEP,
                                                 SubscriberDefault.OPTION_REPEAT,
                                                 SubscriberDefault.OPTION_LENGTH,
                                                 SubscriberDefault.OPTION_TLV_INCLUDE_IN_MESSAGES,
                                                 '0',
                                                 '0')
        else:
            self.__option82_aci = None
            self.__option82_ari = None

        self.__rt_dhcpv4_handle = None
        self.__rt_dhcpv6_handle = None

    @property
    def rt_dhcpv4_handle(self):
        """Get DHCPv4 or DHCP dual stack subscribers dhcpv4 RT handle.

        DHVPv4 subscribers have ipv4 handle only.
        DHCPv6 subscribers have ipv6 handle only
        DHCP dual subscribers stack have both ipv4 and ipv6 handle

        :return: DHCPv4 or DHCP dual stack subscribers dhcpv4 RT handle or None if not exist
        """
        return self.__rt_dhcpv4_handle

    @rt_dhcpv4_handle.setter
    def rt_dhcpv4_handle(self, handle):
        """Set DHCPv4 or DHCP dual stack subscribers dhcpv4 RT handle.

        DHVPv4 subscribers have ipv4 handle only.
        DHCPv6 subscribers have ipv6 handle only
        DHCP dual subscribers stack have both ipv4 and ipv6 handle

        :param h: dhcpv4 handle returned from rt.add_dhcp_client()
        :return: None
        """
        self.__rt_dhcpv4_handle = handle

    @property
    def rt_dhcpv6_handle(self):
        """Get DHCPv6 or DHCP dual stack subscribers dhcpv6 RT handle.

        DHVPv4 subscribers have ipv4 handle only.
        DHCPv6 subscribers have ipv6 handle only
        DHCP dual subscribers stack have both ipv4 and ipv6 handle

        :return: DHCPv6 or DHCP dual stack subscribers dhcpv6 RT handle or None if not exist
        """
        return self.__rt_dhcpv6_handle

    @rt_dhcpv6_handle.setter
    def rt_dhcpv6_handle(self, handle):
        """Set DHCPv6 or DHCP dual stack subscribers dhcpv6 RT handle.

        DHVPv4 subscribers have ipv4 handle only.
        DHCPv6 subscribers have ipv6 handle only
        DHCP dual subscribers stack have both ipv4 and ipv6 handle

        :param h: dhcpv6 handle returned from rt.add_dhcp_client()
        :return: None
        """
        self.__rt_dhcpv6_handle = handle

    @property
    def has_option82(self):
        """If subscriber has DHCPv4 option 82 interface-id and remote-id

        :return: boolean
        """
        return self.__has_option82

    @property
    def option82_aci(self):
        """Get DHCPv4 option 82 circuit-id

        Usage:
            Tell if subscribers have option 82 by calling obj.has_option82
            Or expect None return value.

        :return: DHCPOption object or None
        """
        return self.__option82_aci

    @property
    def option82_ari(self):
        """Get DHCPv4 option 82 remote-id

        Usage:
            Tell if subscribers have option 82 by calling obj.has_option82
            Or expect None return value.

        :return: DHCPOption object or None
        """
        return self.__option82_ari

    def __str__(self):
        return 'DHCPSubscribers with tag {} on {} of {}'.format(self.tag, self.interface_id, self.device_id)


class PPPoESubscribers(Subscribers):
    """PPPoE subscribers.

    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar

        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)

        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        self.__username = group_config.get('username', SubscriberDefault.PPP_USERNAME)
        if 'SUB_USERNAME' in os.environ:
            self.__username = os.environ['SUB_USERNAME']
        self.__password = group_config.get('password', SubscriberDefault.PPP_PASSWORD)
        if 'SUB_PASSWORD' in os.environ:
            self.__password = os.environ['SUB_PASSWORD']
        self.__domain = group_config.get('domain', SubscriberDefault.PPP_DOMAINNAME)
        if 'SUB_DOMAIN' in os.environ:
            self.__domain = os.environ['SUB_DOMAIN']
        self.__auth_method = group_config.get('authentication', SubscriberDefault.PPP_AUTH_METHOD)
        if 'SUB_AUTHENTICATION' in os.environ:
            self.__auth_method = os.environ['SUB_AUTHENTICATION']
        self.__keep_alive = group_config.get('ppp-ka-interval', SubscriberDefault.PPP_KA_INTERVAL)
        self.__termination = group_config.get('termination', SubscriberDefault.PPP_TERMINATION)
        self.circuit_id = group_config.get('circuit-id', None)
        self.circuit_id_start = group_config.get('circuit-id-start', None)
        self.circuit_id_step = group_config.get('circuit-id-step', None)
        self.circuit_id_repeat = group_config.get('circuit-id-repeat', None)
        self.circuit_id_length = group_config.get('circuit-id-length', None)
        self.remote_id = group_config.get('remote-id', None)
        self.remote_id_start = group_config.get('remote-id-start', None)
        self.remote_id_step = group_config.get('remote-id-step', None)
        self.remote_id_repeat = group_config.get('remote-id-repeat', None)
        self.remote_id_length = group_config.get('remote-id-length', None)
        self.ncp_retry = group_config.get('ncp-retry', None)
        self.essm_count = group_config.get('essm-count', None)
        if self.essm_count:
            self.dhcpv6_ia_type = None
        self.__rt_pppox_handle = None
        self.__rt_dhcpv6_handle = None

    @property
    def rt_pppox_handle(self):
        """Get PPPoE subscribers pppox RT handle.

        PPPoEv4 subscribers have pppox handle only.
        PPPoEv6 subscribers have pppox and dhcpv6 handle
        PPPoE dual stack subscribers stack have both pppox and dhcpv6 handle

        :return: PPPoE subscribers pppox RT handle or None if not exist
        """
        return self.__rt_pppox_handle

    @rt_pppox_handle.setter
    def rt_pppox_handle(self, handle):
        """Set PPPoE subscribers pppox RT handle.

        PPPoEv4 subscribers have pppox handle only.
        PPPoEv6 subscribers have pppox and dhcpv6 handle
        PPPoE dual stack subscribers stack have both pppox and dhcpv6 handle

        :param h: pppox handle returned from rt.add_pppoe_client()
        :return: None
        """
        self.__rt_pppox_handle = handle

    @property
    def rt_dhcpv6_handle(self):
        """Get PPPoEv6 or dual stack subscribers DHCPv6 RT handle.

        PPPoEv4 subscribers have pppox handle only.
        PPPoEv6 subscribers have pppox and dhcpv6 handle
        PPPoE dual stack subscribers stack have both pppox and dhcpv6 handle

        :return: PPPoE subscribers DHCPv6 RT handle or None if not exist
        """
        return self.__rt_dhcpv6_handle

    @rt_dhcpv6_handle.setter
    def rt_dhcpv6_handle(self, handle):
        """Set PPPoEv6 or dual stack subscribers DHCPv6 RT handle.

        DHVPv4 subscribers have ipv4 handle only.
        DHCPv6 subscribers have ipv6 handle only
        DHCP dual subscribers stack have both ipv4 and ipv6 handle

        :param h: dhcpv6 handle returned from rt.add_pppoe_client()
        :return: None
        """
        self.__rt_dhcpv6_handle = handle

    @property
    def username(self):
        """PPP username

        :return: string, username
        """
        return self.__username

    @property
    def password(self):
        """PPP password

        :return: string, password
        """
        return self.__password

    @property
    def domain(self):
        """PPP domain name

        :return: string, domain name
        """
        return self.__domain

    @property
    def auth_method(self):
        """PPP authentication method

        :return: string, authentication method, eg., 'pap', 'chap'
        """
        return self.__auth_method

    @property
    def keep_alive(self):
        """PPP keepalive interval

        :return: integer, ka interval in seconds
        """
        return self.__keep_alive

    @property
    def termination(self):
        """PPP termination method, e.g., l2tp.

        Default is local.

        :return: string. Default is 'local'. Could be 'l2tp' if configured.
        """
        return self.__termination

    def __str__(self):
        return 'PPPoESubscribers with tag {} on {} of {}'.format(self.tag, self.interface_id, self.device_id)


class L2TPSubscribers(PPPoESubscribers):
    """L2TP subscribers, which use the RT to simulate pppoeOverLAC
    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar
        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe', 'l2tp'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        self.__num_of_lac = group_config.get('num-of-lac', '1')
        self.__tunnels_per_lac = group_config.get('num-tunnels-per-lac', '1')
        self.__sessions_per_tunnel = group_config.get('sessions-per-tunnel', '1')
        self.__tunnel_vlan_id = group_config.get('tunnel-vlan-id', '1')
        self.__tunnel_vlan_step = group_config.get('tunnel-vlan-step', '1')
        self.__tunnel_auth_enable = group_config.get('tunnel-auth-enable', '1')
        self.__tunnel_secret = group_config.get('tunnel-secret', 'joshua')
        self.__tunnel_destination_ip = group_config.get('tunnel-destination-ip', '100.0.0.1')
        self.__tunnel_source_ip = group_config['tunnel-source-ip']
        self.__tunnel_source_gateway = group_config['tunnel-source-gateway']
        self.__tunnel_prefix_length = group_config.get('tunnel-prefix-length', '24')
        self.__tunnel_source_step = group_config.get('tunnel-source-step', None)
        self.__tunnel_destination_step = group_config.get('tunnel-destination-step', None)
        self.__tunnel_hello_req = group_config.get('tunnel-hello-req', None)
        self.__tunnel_hello_interval = group_config.get('tunnel-hello-interval', None)
        self.__lac_hostname = group_config.get('lac-hostname', 'lac')
        self.__rt_lac_handle = None

    @property
    def tunnel_hello_req(self):
        """

        :return: enable lac to send tunnel hello request
        """
        return self.__tunnel_hello_req

    @property
    def tunnel_hello_interval(self):
        """

        :return: tunnel hello interval
        """
        return self.__tunnel_hello_interval

    @property
    def lac_hostname(self):
        """
        :return:   LAC hostname
        """
        return self.__lac_hostname

    @property
    def num_of_lac(self):
        """
        :return: the number of LACs that RT simulate
        """
        return self.__num_of_lac

    @property
    def tunnels_per_lac(self):
        """
        :return: tunnel numbers per lac
        """
        return self.__tunnels_per_lac

    @property
    def sessions_per_tunnel(self):
        """
        :return: session number per l2tp tunnel
        """
        return self.__sessions_per_tunnel

    @property
    def tunnel_vlan_id(self):
        """
        :return: the vlan start id used by the l2tp tunnel
        """
        return self.__tunnel_vlan_id

    @property
    def tunnel_vlan_step(self):
        """
        :return: the l2tp vlan increasing pattern
        """
        return self.__tunnel_vlan_step

    @property
    def tunnel_auth_enable(self):
        """
        :return: tunnel authentication enable/disable
        """
        return self.__tunnel_auth_enable

    @property
    def tunnel_secret(self):
        """
        :return: tunnel authentication secret
        """
        return self.__tunnel_secret

    @property
    def tunnel_destination_ip(self):
        """
        :return: tunnel destination ip address
        """
        return self.__tunnel_destination_ip

    @property
    def tunnel_source_ip(self):
        """
        :return: tunnel source ip address
        """
        return self.__tunnel_source_ip

    @property
    def tunnel_source_gateway(self):
        """
        :return: gateway address for tunnel source ip
        """
        return self.__tunnel_source_gateway

    @property
    def tunnel_prefix_length(self):
        """
        :return: tunnel address mask length
        """
        return self.__tunnel_prefix_length

    @property
    def tunnel_source_step(self):
        """
        :return: tunnel source ip address increase pattern
        """
        return self.__tunnel_source_step

    @property
    def tunnel_destination_step(self):
        """
        :return: tunnel destination i address increase pattern
        """
        return self.__tunnel_destination_step

    @property
    def rt_lac_handle(self):
        """
        :return: RT lac handle
        """
        return self.__rt_lac_handle

    @rt_lac_handle.setter
    def rt_lac_handle(self, handle):
        """
        :param handle:
        :return:
        """
        self.__rt_lac_handle = handle


class L2BSASubscribers(Subscribers):
    """ L2BSA subscribers
    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar
        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe', 'l2tp'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        self.mac_resolve = group_config.get('mac-resolve', None)
        self.gateway_mac = group_config.get('gateway-mac', None)
        self.ip_addr = group_config.get('ip', None)
        self.ip_addr_step = group_config.get('ip-step', None)
        self.gateway = group_config.get('gateway', None)
        self.gateway_step = group_config.get('gateway-step', None)
        self.ipv6_addr = group_config.get('ipv6', None)
        self.ipv6_addr_step = group_config.get('ipv6-step', None)
        self.ipv6_gateway = group_config.get('ipv6-gateway', None)
        self.ipv6_gateway_step = group_config.get('ipv6-gateway-step', None)
        self.rt_ip_handle = None
        self.rt_ipv6_handle = None
        self.circuit_id = group_config.get('circuit-id', None)
        self.circuit_id_start = group_config.get('circuit-id-start', None)
        self.circuit_id_step = group_config.get('circuit-id-step', None)
        self.circuit_id_repeat = group_config.get('circuit-id-repeat', None)
        self.circuit_id_length = group_config.get('circuit-id-length', None)
        self.remote_id = group_config.get('remote-id', None)
        self.remote_id_start = group_config.get('remote-id-start', None)
        self.remote_id_step = group_config.get('remote-id-step', None)
        self.remote_id_repeat = group_config.get('remote-id-repeat', None)
        self.remote_id_length = group_config.get('remote-id-length', None)


class StaticSubscribers(Subscribers):
    """ Static subscribers
    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar
        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe', 'l2tp'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        self.mac_resolve = group_config.get('mac-resolve', None)
        self.gateway_mac = group_config.get('gateway-mac', None)
        self.ip_addr = group_config.get('ip', None)
        self.ip_addr_step = group_config.get('ip-step', None)
        self.ip_gateway = group_config.get('ip-gateway', None)
        self.ipv6_addr = group_config.get('ipv6', None)
        self.ipv6_addr_step = group_config.get('ipv6-step', None)
        self.ipv6_gateway = group_config.get('ipv6-gateway', None)
        self.rt_ip_handle = None
        self.rt_ipv6_handle = None

class HAGSubscribers(Subscribers):
    """ Hag subscribers, which represent HAG subscriber and testcase in spirent
    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar
        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe', 'l2tp'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group
        self.test_session_handle = None
        self.isactive = False
        self.test_activity = "Capacity Test"
        self.test_session_name = ""
        self.libname = ""
        self.tsname = ""
        self.access_interface = ""
        self.uplink_interface = ""
        self.external_data = group_config.get('external-data', 0)
        self.traffic = group_config.get('traffic', None)
        self.tunnel_type = group_config.get('tunnel-type', "GREL3")
        self.hybrid_access = True
        if 'lte-node' in group_config['devices']:
            self.lte_node_ip = group_config['devices']['lte-node']['start-ip']
            self.lte_node_nexthop = group_config['devices']['gateway']
            self.lte_activation_rate = group_config['devices']['lte-node']['activation-rate']
            self.lte_deactivation_rate = group_config['devices']['lte-node']['deactivation-rate']
            self.lte_node_count = group_config['devices']['lte-node'].get('count', '1')
            self.dsl_node_ip = group_config['devices']['dsl-node']['start-ip']
        if 'sut-loopback' in group_config:
            self.sut_loopback_ip = group_config['sut-loopback']
        if 'hybrid-access' in group_config:
            self.hag_client_id = group_config['hybrid-access']['client-id']
            self.hag_bypass_rate = group_config['hybrid-access'].get('bypass-traffic-rate', '750')
            self.hag_ipv6_prefix_th = group_config['hybrid-access'].get('ipv6-prefix-th', '1002::1')
            self.hag_ipv6_prefix_haap = group_config['hybrid-access'].get('ipv6-prefix-haap', '1002::1')
            self.hag_gre_pkt_reorder = group_config['hybrid-access'].get('packet-reorder', '0')
            self.hag_lte_pkt_distribution = group_config['hybrid-access']['lte'].get('packet-distribution', '1')
            self.hag_lte_request_timeout = group_config['hybrid-access']['lte'].get('setup-request-timeout', '10')
            self.hag_lte_no_answer_retry = group_config['hybrid-access']['lte'].get('no-answer-retries', '3')
            self.hag_lte_setup_deny_retry = group_config['hybrid-access']['lte'].get('setup-deny-retries', '3')
            self.hag_lte_setup_retry_interval = group_config['hybrid-access']['lte'].get('setup-retry-interval', '30')
            self.hag_dsl_pkt_distribution = group_config['hybrid-access']['dsl'].get('packet-distribution', '1')
            self.hag_dsl_request_timeout = group_config['hybrid-access']['dsl'].get('setup-request-timeout', '10')
            self.hag_dsl_no_answer_retry = group_config['hybrid-access']['dsl'].get('no-answer-retries', '3')
            self.hag_dsl_setup_deny_retry = group_config['hybrid-access']['dsl'].get('setup-deny-retries', '3')
            self.hag_dsl_setup_retry_interval = group_config['hybrid-access']['dsl'].get('setup-retry-interval', '30')
            self.hag_dsl_sync_enable = "false"
            if 'sync-rate' in group_config['hybrid-access']['dsl']:
                self.hag_dsl_sync_enable = "true"
                self.hag_dsl_sync_rate = group_config['hybrid-access']['dsl']['sync-rate']
            if 'protocol' in group_config['hybrid-access']['dsl']:
                self.hag_dsl_protocol = group_config['hybrid-access']['dsl']['protocol']
        if 'dhcp' in group_config:
            self.dhcp_client_id = group_config['dhcp']['client-id']
            self.dhcp_retries = group_config['dhcp'].get('retries', '30')
            self.dhcp_v6_ia_type = group_config['dhcp'].get('v6-ia-type', 'IA_TA')
        self.has_li = False
        if 'li' in group_config:
            self.has_li = True
            self.li_ipaddr = group_config['li'].get('start-ip', '192.0.0.2')
            self.li_gateway = group_config['li'].get('nexthop-ip', '192.0.0.3')
        if self.traffic:
            self.traffic_vlan_enable = False
            if 'vlan-id' in self.traffic:
                self.traffic_vlan_enable = True
                self.traffic_vlan_id = self.traffic['vlan-id']
            if 'svlan-id' in self.traffic:
                self.traffic_svlan_id = self.traffic['svlan-id']
            self.traffic_network_host_type = self.traffic.get('network-host-type', 'local')
            self.traffic_dualstack = self.traffic.get('dualstack', False)
            if self.traffic_dualstack:
                self.v6_traffic_start_ip = self.traffic['v6-start-ip']
                self.v6_traffic_node_count = self.traffic.get('v6-node-count', '1')
                self.v6_traffic_gateway = self.traffic['v6-gateway']
            self.traffic_start_ip = self.traffic['start-ip']
            self.traffic_node_count = self.traffic.get('node-count', '1')
            self.traffic_gateway = self.traffic['gateway']
            self.traffic_start_when = self.traffic.get('start-when', 'all')
            self.traffic_start_delay = self.traffic.get('start-delay', '0')
            self.traffic_mtu = self.traffic.get('mtu', '1450')
            self.traffic_do_not_fragment = self.traffic.get('do-not-fragment', False)
            if 'error-injection' in self.traffic:
                self.traffic_error_injection_type = self.traffic['error-injection'].get('type', 'none')
                self.traffic_error_injection_distribution = self.traffic['error-injection'].get('distribution', 'fixed')
                if 'inbound-rate' in self.traffic['error-injection']:
                    self.traffic_error_injection_inbound = self.traffic['error-injection']['inbound-rate']
                if 'outbound-rate' in self.traffic['error-injection']:
                    self.traffic_error_injection_inbound = self.traffic['error-injection']['outbound-rate']
                if 'bad-source-ip' in self.traffic['error-injection']:
                    self.traffic_error_injection_bad_source = self.traffic['error-injection']['bad-source-ip']
            data_profiles = self.traffic['data-profile']
            self.traffic_profile = {}
            for profile in data_profiles:
                name = profile['name']
                self.traffic_profile[name] = {}
                self.traffic_profile[name]['type'] = profile['type']
                self.traffic_profile[name]['start'] = profile.get('start', 'on')
                transaction_count = profile.get('transaction', '0')
                if transaction_count == "continuous":
                    transaction_count = '0'
                self.traffic_profile[name]['transaction'] = transaction_count
                self.traffic_profile[name]['rate'] = profile.get('transaction-rate', '1000')
                self.traffic_profile[name]['packet_size'] = profile.get('packet-size', '1450')
                self.traffic_profile[name]['segment_size'] = profile.get('segment-size', '1000')
                self.traffic_profile[name]['ratio'] = profile.get('host-expension-ratio', '1')
                self.traffic_profile[name]['initiate_side'] = profile.get('initiate-side', 'client')
                self.traffic_profile[name]['ttl'] = profile.get('ttl', '64')
                self.traffic_profile[name]['client_port_mode'] = profile.get('client-port-mode', 'random')
                self.traffic_profile[name]['role'] = profile.get('role', 'client')
                self.traffic_profile[name]['preferred_transport'] = profile.get('preferred-transport', 'any')
                if 'server-port' in profile:
                    self.traffic_profile[name]['server_port'] = profile['server-port']
                if 'tos' in profile:
                    self.traffic_profile[name]['tos'] = profile['tos']
                if 'udp-burst-transaction-count' in profile:
                    if int(self.traffic_profile[name]['segment_size']) >= \
                            int(self.traffic_profile[name]['packet_size']):
                        self.traffic_profile[name]['udp_burst_count'] = profile['udp-burst-transaction-count']
                    else:
                        t.log("Burst Mode cannot be used when known to be fragmenting"
                              " (segment size < packet size + header size)")
                if 'socket-disc-side' in profile:
                    self.traffic_profile[name]['tcp_socket_disc_side'] = profile['socket-disc-side']
                if 'disconnect-type' in profile:
                    self.traffic_profile[name]['tcp_disconnect_type'] = profile['disconnect-type']
                if '3way-handshake' in profile:
                    self.traffic_profile[name]['tcp_3way_handshake'] = profile['3way-handshake']
                if 'slowstart-congestionavoid' in profile:
                    self.traffic_profile[name]['tcp_congestion_avoid'] = profile['slowstart-congestionavoid']
                if 'max-packets-before-ack' in profile:
                    self.traffic_profile[name]['tcp_max_packets_before_ack'] = profile['max-packets-before-ack']
                if 'min-tcp-header-size' in profile:
                    self.traffic_profile[name]['tcp_min_header_size'] = profile['min-tcp-header-size']
                if 'window-size' in profile:
                    self.traffic_profile[name]['tcp_window_size'] = profile['window-size']
                if 'max-segment-size' in profile:
                    self.traffic_profile[name]['tcp_max_segment_size'] = profile['max-segment-size']
                if 'client-port' in profile:
                    self.traffic_profile[name]['client_port'] = profile['client-port']

    def action(self, action='start', **kwargs):
        """
        kwargs:
        port:    access/uplink port
        filename:   filename for captured file
        :return:
        """
        #import jnpr.toby.bbe.testers.ls as ls
        rt_device = self.rt_device_id
        rt_handle = t.get_handle(rt_device)
        if action not in ['start', 'stop', 'abort', 'results', 'logout', 'continue', 'report',
                          'delete', 'capture_start', 'capture_stop', 'capture_save', 'check_session_status']:
            raise Exception("action {} is not supported".format(action))
        if action in ['capture_start', 'capture_stop', 'capture_save']:
            port_type = kwargs.get('port', 'access')
            interface_list = []
            if port_type == 'access':
                interface_list.append(self.access_interface)
            if port_type == 'uplink':
                interface_list.append(self.uplink_interface)
            if port_type == 'all':
                interface_list.append(self.access_interface)
                interface_list.append(self.uplink_interface)
            if action == 'capture_start':
                if not self.isactive:
                    t.log("starting testsession {} before doing capture_start action".format(self.test_session_name))
                    self.action(action='start')
                rt_handle.invoke('capture_action', tsName=self.tsname, action='start', intfList=interface_list, useActs=1, testSessionHandle=self.test_session_handle)
                t.log("starting capturing packets on interface {}".format(interface_list))
                return
            if action == 'capture_stop':
                rt_handle.invoke('capture_action', tsName=self.tsname, action='stop', intfList=interface_list, useActs=1, testSessionHandle=self.test_session_handle)
                t.log("stopped capturing packets on interface {}".format(interface_list))
                return
            if action == 'capture_save':
                filename = rt_handle.invoke('capture_action', tsName=self.tsname, action='Retrieve',
                                            intfList=interface_list, pcapDir='/tmp', useActs=1, testSessionHandle=self.test_session_handle)
                #t.log("saved captured file to user log firectory {}, file list is {}".format(t._log_dir, filename))
                t.log("saved captured file in /tmp, file list is {}".format(filename))
                return filename
        if action == 'start':
            if not self.isactive:
                response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Run')
                self.isactive = True
            t.log("test session {} is started ".format(self.test_session_name))
            return
        if action == 'start_with_auto_pcap':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Run',
                                        autoCaptureOnStart='true')
            self.isactive = True
            t.log("test session {} is started with auto packet capture option ".format(self.test_session_name))
            return
        if action == 'stop':
            if self.isactive:
                response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Stop')
                self.isactive = False
            t.log("test session {} is stopped ".format(self.test_session_name))
            return
        if action == 'continue':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Continue')
            return
        if action == 'abort':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Abort')
            self.isactive = False
            t.log("test session {} is aborted".format(self.test_session_name))
            return
        if action == 'report':
            response = rt_handle.invoke('generate_tac_report', testSessionHandle=self.test_session_handle,
                                        reportDir='/tmp/{}.zip'.format(self.test_session_name))
            t.log("saved report file /tmp/{}.zip".format(self.test_session_name))
            return
        if action == 'results':
            response = rt_handle.invoke('get_test_results', testSessionHandle=self.test_session_handle)
            return response
        if action == 'logout':
            response = rt_handle.invoke('logout_from_server')
            t.log("disconnected from tester")
            return
        if action == 'delete':
            response = rt_handle.invoke('delete_test_session', testSessionName=self.test_session_name,
                                        libraryName=self.libname)
            t.log("deleted test session {}".format(self.test_session_name))
            return
        if action == 'check_session_status':
            if 'state' not in kwargs:
                raise Exception('kwargs[\'state\'] is a required parameter for this action.\nSupported states are: '
                                'running/complete/waiting')
            invoke_command = 'ls::get ' + self.test_session_handle + ' -TestStateOrStep'
            result = rt_handle.invoke('invoke', cmd=invoke_command)

            if kwargs['state'].lower() in result.lower():
                t.log('Desired state \'{}\' reached\n'.format(kwargs['state']))
                return
            else:
                raise Exception('Test Session state is not \'{}\' yet!\n'.format(kwargs['state']))


class CUPSSubscribers(Subscribers):
    """ 5G CUPS subscribers, which represent CUPS subscriber and testcase in spirent
    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar
        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe', 'l2tp'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        # Take from HAG since we do not need their WiFi offload attributes
        self.test_session_handle = None
        self.isactive = False
        self.test_session_name = ""
        self.libname = ""
        self.tsname = ""
        self.access_interface = ""
        self.uplink_interface = ""
        self.control_interface = ""
        self.subscriber_group_indices = {}
        self.node_test_case_name = ""
        self.nodal_test_case_name = ""

        self.test_activity = group_config.get('test-activity', 'Capacity Test')
        self.session_count = group_config.get('session-count', '1')
        self.bearer_per_session = group_config.get('default-bearers', '1')
        self.dedicated_bearers = group_config.get('dedicated-bearers', '0')
        self.activation_rate = group_config.get('activation-rate', '1')
        self.deactivation_rate = group_config.get('deactivation-rate', '1')
        self.bearer_ipv6_addr_pool = group_config.get('bearer-ipv6-addr-pool', 'DB43:2019::0/64')
        self.bearer_ipv4_addr_pool = group_config.get('bearer-ipv4-addr-pool', '91.0.0.1')
        self.data_mtu = group_config.get('data-mtu', '1400')
        self.apn_name = group_config.get('apn-name', 'mx-upf')
        self.user_initiated_association = group_config.get('user-init-association', False)
        self.home_address_type = group_config.get('home-addr-type', '1')    # 1 for ipv4, 2 for ipv6, 3 for both
        self.sut_loopback_ipv6 = group_config.get('sut-loopback-v6', 'FEED:D00D::1')
        self.sut_loopback_ip = group_config.get('sut-loopback', '100.0.0.1')
        self.use_loopback_access = group_config.get('use-loopback-access', False)
        self.use_loopback_control = group_config.get('use-loopback-control', False)
        self.use_static_address = group_config.get('use-static-addr', False)
        self.heartbeat_retries = group_config.get('heartbeat-retries', '3')
        self.heartbeat_interval = group_config.get('heartbeat-interval', '20')
        self.sx_node_retries = group_config.get('sx-node-retries', '3')
        self.sx_node_retry_interval = group_config.get('sx-node-retry-interval', '5')
        self.sx_session_retries = group_config.get('sx-session-retries', '3')
        self.sx_session_retry_interval = group_config.get('sx-session-retry-interval', '5')
        # Control node counts
        self.mme_control_node_count = group_config.get('mme-control-node-count', '1')
        self.sgw_control_node_count = group_config.get('sxab-control-node-count', '1')
        self.enodeb_user_node_count = group_config.get('enodeb-user-node-count', '1')

        import ipaddress

        self.user_base_address = group_config.get('user-base-address', '10.1.1.1/24')
        self.control_base_address = group_config.get('control-base-address', '20.2.2.1/24')
        self.uplink_base_address = group_config.get('uplink-base-address', '30.3.3.1/24')

        if 'user-v6-base-address' in group_config:
            self.user_v6_base_address = group_config.get('user-v6-base-address')
        if 'control-v6-base-address' in group_config:
            self.control_v6_base_address = group_config.get('control-v6-base-address')
        if 'uplink-v6-base-address' in group_config:
            self.uplink_v6_base_address = group_config.get('uplink-v6-base-address')

        # Logic for consolidating S1U + SGi. Need further granularity on individual interface
        # Get integer 'n' from rinterface.interface_link = 'accessn' ie. access0, access1, access2, etc.
        interface_index = [int(z) for z in list(rtinterface.interface_link) if z.isdigit()][0]
        access_interface_list = bbe.get_interfaces(rtinterface.device_id, interfaces=rinterface.interface_link)
        control_interface_list = bbe.get_interfaces(rtinterface.device_id, interfaces='control'+str(interface_index))
        uplink_interface_list = bbe.get_interfaces(rtinterface.device_id, interfaces='uplink'+str(interface_index))

        if len(access_interface_list) < 1 or len(uplink_interface_list) < 1:
            raise Exception('Must have minimum of 1 access and 1 uplink interface present to initialize a '
                            'CUPSSubscriber object!\n')

        # Check Home Addr type to see if we need v6 uplink network, since decapsulated traffic will be IPv6
        if self.home_address_type == 2 or self.home_address_type == 3:
            self.uplink_v6_base_address = group_config.get('uplink-v6-base-address', 'FEED:BABE::1/64')

        # Assign interfaces to subscriber while we have them anyways. List will have 1 entry due to required
        # unique link names in params.yaml
        self.access_interface = access_interface_list[0].interface_pic
        if hasattr(self, 'user_v6_base_address'):
            self.access_v6_interface = self.access_interface + 'v6'
        self.uplink_interface = uplink_interface_list[0].interface_pic
        if hasattr(self, 'uplink_v6_base_address'):
            self.uplink_v6_interface = self.uplink_interface + 'v6'

        # Can generate IPs dynamically, since many required LS IPs do not matter to DUT. Let user pick their
        # desired base address and we will handle the rest. Next IP is retrieved from next() function applied
        # to appropriate IP iterator
        self.access_ip_generator = iter(ipaddress.IPv4Network(self.user_base_address, strict=False).hosts())
        if hasattr(self, 'user_v6_base_address'):
            self.access_ipv6_generator = iter(ipaddress.IPv6Network(self.user_v6_base_address, strict=False).hosts())
        if len(control_interface_list) == 0:
            t.log('No control interface found. Attaching control-base-network to the access RT port!\n')
            self.control_ip_generator = self.access_ip_generator
            self.control_interface = self.access_interface
            if self.user_base_address != self.control_base_address:
                self.control_ip_generator = iter(ipaddress.IPv4Network(self.control_base_address, strict=False).hosts())
                self.control_interface = str(self.access_interface) + '_1'
            if hasattr(self, 'user_v6_base_address'):
                self.control_ipv6_generator = self.access_ipv6_generator
                self.control_v6_interface = self.access_v6_interface
                if not hasattr(self, 'control_v6_base_address'):
                    self.control_v6_base_address = self.user_v6_base_address
                if (self.user_v6_base_address != self.control_v6_base_address):
                    self.control_ipv6_generator = iter(ipaddress.IPv6Network(
                        self.control_v6_base_address, strict=False).hosts())
                    self.control_v6_interface = str(self.access_v6_interface) + '_1'
        else:
            self.control_ip_generator = iter(ipaddress.IPv4Network(self.control_base_address, strict=False).hosts())
            self.control_interface = control_interface_list[0].interface_pic
            if hasattr(self, 'control_v6_base_address'):
                self.control_ipv6_generator = iter(ipaddress.IPv6Network(
                    self.control_v6_base_address, strict=False).hosts())
                self.control_v6_interface = self.control_interface + 'v6'
        self.uplink_ip_generator = iter(ipaddress.IPv4Network(self.uplink_base_address, strict=False).hosts())
        if hasattr(self, 'uplink_v6_base_address'):
            self.uplink_ipv6_generator = iter(ipaddress.IPv6Network(self.uplink_v6_base_address, strict=False).hosts())


        self.sgw_user_address = str(next(self.access_ip_generator)) # DUT local address for ANP
        self.access_gateway = self.sgw_user_address
        if self.use_loopback_access:
            self.sgw_user_address = self.sut_loopback_ip

        self.sxa_sxb_to_up_sgw_user_node = str(next(self.access_ip_generator))
        self.pgw_address = str(next(self.access_ip_generator))

        self.enodeb_user_node_start_ip = str(next(self.access_ip_generator))
        self.target_enodeb_user_node = str(next(self.access_ip_generator))

        if hasattr(self, 'user_v6_base_address'):
            self.sgw_v6_user_address = str(next(self.access_ipv6_generator)) # DUT local address for ANP
            self.v6_access_gateway = self.sgw_v6_user_address
            if self.use_loopback_access:
                self.sgw_v6_user_address = self.sut_loopback_ipv6

            self.sxa_sxb_to_up_sgw_v6_user_node = str(next(self.access_ipv6_generator))
            self.pgw_v6_address = str(next(self.access_ipv6_generator))

            self.enodeb_user_node_start_ipv6 = str(next(self.access_ipv6_generator))
            self.target_enodeb_user_node_v6 = str(next(self.access_ipv6_generator))

        # eNodeB User Node IPs should be consumed in sequence when multiple eNodeB in use
        if int(self.enodeb_user_node_count) > 1:
            self.enodeb_user_node_ip_list = []
            self.enodeb_user_node_ip_list.append(self.enodeb_user_node_start_ip)
            for count in range(self.enodeb_user_node_count - 1):
                self.enodeb_user_node_ip_list.append(str(next(self.access_ip_generator)))
            self.target_enodeb_user_node = str(next(self.access_ip_generator))
            self.target_enodeb_user_node_ip_list = []
            self.target_enodeb_user_node_ip_list.append(self.target_enodeb_user_node)
            for count in range(self.enodeb_user_node_count - 1):
                self.target_enodeb_user_node_ip_list.append(str(next(self.access_ip_generator)))
            if hasattr(self, 'user_v6_base_address'):
                self.enodeb_user_node_ipv6_list = []
                self.enodeb_user_node_ipv6_list.append(self.enodeb_user_node_start_ipv6)
                for count in range(self.enodeb_user_node_count - 1):
                    self.enodeb_user_node_ipv6_list.append(str(next(self.access_ipv6_generator)))
                self.target_enodeb_user_node_v6 = str(next(self.access_ipv6_generator))
                self.target_enodeb_user_node_ipv6_list = []
                self.target_enodeb_user_node_ipv6_list.append(self.target_enodeb_user_node_v6)
                for count in range(self.enodeb_user_node_count - 1):
                    self.target_enodeb_user_node_ipv6_list.append(str(next(self.access_ipv6_generator)))

        # self.sxa_sxb_to_up_sgw_user_node = str(next(self.access_ip_generator))
        # self.pgw_address = str(next(self.access_ip_generator))
        # self.target_enodeb_user_node = str(next(self.access_ip_generator))
        self.sxa_sxb_to_up_port = '8805'

        # Generate control IPs
        self.sxa_sxb_to_up_user_node = str(next(self.control_ip_generator))  # DUT local address for CPP
        if self.user_base_address == self.control_base_address:
            self.sxa_sxb_to_up_user_node = self.sgw_user_address
        self.control_gateway = self.sxa_sxb_to_up_user_node
        if self.use_loopback_control:
            self.sxa_sxb_to_up_user_node = self.sut_loopback_ip
        self.sgw_control_address = str(next(self.control_ip_generator))
        self.sgw_control_node_start_ip = self.sgw_control_address

        # SGW-C IPs should be consumed in sequence when multiple CPF in use
        if int(self.sgw_control_node_count) > 1:
            self.sgw_control_node_ip_list = []
            self.sgw_control_node_ip_list.append(self.sgw_control_address)
            for count in range(self.sgw_control_node_count - 1):
                self.sgw_control_node_ip_list.append(str(next(self.control_ip_generator)))

        self.mme_control_node_start_ip = str(next(self.control_ip_generator))
        self.sxa_sxb_control_node_start_ip = str(next(self.control_ip_generator))

        # Sxab control IPs should be consumed in sequence when multiple CPF in use
        if int(self.sgw_control_node_count) > 1:
            self.sxab_control_node_ip_list = []
            self.sxab_control_node_ip_list.append(self.sxa_sxb_control_node_start_ip)
            for count in range(self.sgw_control_node_count - 1):
                self.sxab_control_node_ip_list.append(str(next(self.control_ip_generator)))

        self.sxa_sxb_control_gtp_node_start_ip = str(next(self.control_ip_generator))
        self.sxa_sxb_to_up_gtp_node = self.sxa_sxb_to_up_user_node

        if hasattr(self, 'control_v6_base_address'):
            # Generate control IPs
            self.sxa_sxb_to_up_v6_user_node = str(next(self.control_ipv6_generator))  # DUT local address for CPP
            if self.user_v6_base_address == self.control_v6_base_address:
                self.sxa_sxb_to_up_v6_user_node = self.sgw_v6_user_address
            self.v6_control_gateway = self.sxa_sxb_to_up_v6_user_node
            if self.use_loopback_control:
                self.sxa_sxb_to_up_v6_user_node = self.sut_loopback_ipv6
            self.sgw_v6_control_address = str(next(self.control_ipv6_generator))
            self.sgw_control_node_start_ipv6 = self.sgw_v6_control_address

            # SGW-C IPs should be consumed in sequence when multiple CPF in use
            if int(self.sgw_control_node_count) > 1:
                self.sgw_control_node_ipv6_list = []
                self.sgw_control_node_ipv6_list.append(self.sgw_v6_control_address)
                for count in range(self.sgw_control_node_count - 1):
                    self.sgw_control_node_ipv6_list.append(str(next(self.control_ipv6_generator)))

            self.mme_control_node_start_ipv6 = str(next(self.control_ipv6_generator))
            self.sxa_sxb_control_node_start_ipv6 = str(next(self.control_ipv6_generator))

            # Sxab control IPs should be consumed in sequence when multiple CPF in use
            if int(self.sgw_control_node_count) > 1:
                self.sxab_control_node_ipv6_list = []
                self.sxab_control_node_ipv6_list.append(self.sxa_sxb_control_node_start_ipv6)
                for count in range(self.sgw_control_node_count - 1):
                    self.sxab_control_node_ipv6_list.append(str(next(self.control_ipv6_generator)))

            self.sxa_sxb_control_gtp_node_start_ipv6 = str(next(self.control_ipv6_generator))
            self.sxa_sxb_to_up_gtp_node_v6 = self.sxa_sxb_to_up_v6_user_node

        # Generate uplink IPs
        self.uplink_gateway = str(next(self.uplink_ip_generator))
        self.traffic_start_ip = str(next(self.uplink_ip_generator))
        if hasattr(self, 'uplink_v6_base_address'):
            self.v6_uplink_gateway = str(next(self.uplink_ipv6_generator))
            self.traffic_start_ipv6 = str(next(self.uplink_ipv6_generator))

        # SGW Nodal S11
        self.s11_gtpv2_version = group_config.get('gtpv2-version', '15.2.0')
        self.s11_total_apns = group_config.get('total-apns', '1')
        self.s11_start_imsi = group_config.get('start-imsi', '505024101215074')
        self.s11_start_imei = group_config.get('start-imei', '50502410121507')
        self.s11_radio_access_type = group_config.get('radio-access-type', 'eutran')
        self.s11_gtp_c_tunnel_id = group_config.get('start-gtp-c-tunnel-id', '1000000')
        self.s11_gtp_u_tunnel_id = group_config.get('start-gtp-u-tunnel-id', '1048576')
        self.s11_total_apns = group_config.get('total-apns', '1')
        self.s11_n3_requests = group_config.get('s11-n3-requests', '5')
        self.s11_t3_response_time = group_config.get('s11-t3-response-time', '20')

        # SGW Node S11
        self.node_start_imsi = group_config.get('start-imsi', '505024101215074')
        self.node_start_imei = group_config.get('start-imei', '50502410121507')
        self.node_radio_access_type = group_config.get('radio-access-type', 'eutran')
        self.node_gtp_c_tunnel_id = group_config.get('start-gtp-c-tunnel-id', '1000000')
        self.node_gtp_u_tunnel_id = group_config.get('start-gtp-u-tunnel-id', '1048576')
        self.node_start_s5_gtp_c_teid = group_config.get('start-s5-gtp-c-teid', '3000000')
        self.node_start_s5_gtp_u_teid = group_config.get('start-s5-gtp-u-teid', '4000000')
        self.node_start_fwd_gtp_u_teid = group_config.get('start-fwd-gtp-u-teid', '5000000')
        self.node_total_apns = group_config.get('total-apns', '1')
        self.node_gtpv2_version = group_config.get('gtpv2-version', '15.2.0')

        # VLANs
        if group_config.get('access-vlan-id') is not None:
            self.access_vlan_id = group_config.get('access-vlan-id')
        if group_config.get('control-vlan-id') is not None:
            self.control_vlan_id = group_config.get('control-vlan-id')
        if group_config.get('uplink-vlan-id') is not None:
            self.uplink_vlan_id = group_config.get('uplink-vlan-id')

        # Creates data structure allowing user to have different login groups within single Test Session
        if 'Command Mode' in self.test_activity and group_config.get('session-groups') is not None:
            count = 1
            for group in sorted(group_config['session-groups']):
                start_index = count
                stop_index = count + group_config['session-groups'][group] - 1
                self.subscriber_group_indices[group] = (start_index, int(stop_index))
                count += int(group_config['session-groups'][group])
        self.subscriber_group_indices['default'] = (1, self.session_count)

    def action(self, action='start', **kwargs):
        """
        kwargs:
        port:    access/uplink port
        filename:   filename for captured file
        :return:
        """
        #import jnpr.toby.bbe.testers.ls as ls
        rt_device = self.rt_device_id
        rt_handle = t.get_handle(rt_device)
        if action not in ['start', 'stop', 'abort', 'results', 'logout', 'continue', 'report',
                          'delete', 'capture_start', 'capture_stop', 'capture_save', 'start_with_auto_pcap',
                          'automation_control', 'check_session_status', 'capture_config', 'is_fireball']:
            raise Exception("action {} is not supported".format(action))
        if action in ['capture_start', 'capture_stop', 'capture_save']:
            port_type = kwargs.get('port', 'access')
            interface_list = []
            if port_type == 'access':
                interface_list.append(self.access_interface)
            if port_type == 'uplink':
                interface_list.append(self.uplink_interface)
            if port_type == 'control':
                # Remove any underscores from subscriber.control_interface that were required for reserve_ports.
                # This will only change the control_interface string for port capture if separate networks were needed
                # for controlcand access in a two port setup
                interface_list.append(self.control_interface.split('_', 1)[0])
            if port_type == 'all':
                interface_list.append(self.access_interface)
                interface_list.append(self.uplink_interface)
                interface_list.append(self.control_interface.split('_', 1)[0])
            if action == 'capture_start':
                if not self.isactive:
                    t.log("starting testsession {} before doing capture_start action".format(self.test_session_name))
                    self.action(action='start')
                rt_handle.invoke('capture_action', tsName=self.tsname, action='start', intfList=interface_list, useActs=1, testSessionHandle=self.test_session_handle)
                t.log("starting capturing packets on interface {}".format(interface_list))
                return
            if action == 'capture_stop':
                rt_handle.invoke('capture_action', tsName=self.tsname, action='stop', intfList=interface_list, useActs=1, testSessionHandle=self.test_session_handle)
                t.log("stopped capturing packets on interface {}".format(interface_list))
                return
            if action == 'capture_save':
                filename = rt_handle.invoke('capture_action', tsName=self.tsname, action='Retrieve',
                                            intfList=interface_list, pcapDir='/tmp', useActs=1, testSessionHandle=self.test_session_handle)
                #t.log("saved captured file to user log firectory {}, file list is {}".format(t._log_dir, filename))
                t.log("saved captured file in /tmp, file list is {}".format(filename))
                return filename
        if action == 'start':
            if not self.isactive:
                response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Run')
                self.isactive = True
            t.log("test session {} is started ".format(self.test_session_name))
            return
        if action == 'start_with_auto_pcap':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Run',
                                        autoCaptureOnStart='true')
            self.isactive = True
            t.log("test session {} is started with auto packet capture option ".format(self.test_session_name))
            return
        if action == 'stop':
            if self.isactive:
                response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Stop')
                self.isactive = False
            t.log("test session {} is stopped ".format(self.test_session_name))
            return
        if action == 'continue':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Continue')
            return
        if action == 'abort':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Abort')
            self.isactive = False
            t.log("test session {} is aborted".format(self.test_session_name))
            return
        if action == 'report':
            response = rt_handle.invoke('generate_tac_report', testSessionHandle=self.test_session_handle,
                                        reportDir='/tmp/{}.zip'.format(self.test_session_name))
            t.log("saved report file /tmp/{}.zip".format(self.test_session_name))
            return
        if action == 'results':
            response = rt_handle.invoke('get_test_results', testSessionHandle=self.test_session_handle, **kwargs)
            return response
        if action == 'logout':
            response = rt_handle.invoke('logout_from_server')
            t.log("disconnected from tester")
            return
        if action == 'delete':
            response = rt_handle.invoke('delete_test_session', testSessionName=self.test_session_name,
                                        libraryName=self.libname)
            t.log("deleted test session {}".format(self.test_session_name))
            return
        if action == 'automation_control':
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Init', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Start', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName='Wait')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Init', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Start', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName='Wait')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Stop', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.nodal_test_case_name,
                             predecessorState='RUNNING')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Cleanup', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.nodal_test_case_name,
                             predecessorState='STOPPED')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Stop', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.node_test_case_name,
                             predecessorState='RUNNING')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Cleanup', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.node_test_case_name,
                             predecessorState='STOPPED')
            validation_status = rt_handle.invoke('validate_test_configuration',
                                                 testSessionHandle=self.test_session_handle)
            t.log("Validation Status after automation_control: {}".format(validation_status))
            rt_handle.invoke('save_config', instance=self.test_session_handle, overwrite=1)
            return
        if action == 'check_session_status':
            if 'state' not in kwargs:
                raise Exception('kwargs[\'state\'] is a required parameter for this action.\nSupported states are: '
                                'running/complete/waiting')
            invoke_command = 'ls::get ' + self.test_session_handle + ' -TestStateOrStep'
            result = rt_handle.invoke('invoke', cmd=invoke_command)

            if kwargs['state'].lower() in result.lower():
                t.log('Desired state \'{}\' reached\n'.format(kwargs['state']))
                return
            else:
                raise Exception('Test Session state is not \'{}\' yet!\n'.format(kwargs['state']))
        if action == 'capture_config':
            port_type = kwargs.get('port', 'access')
            if port_type == 'access':
                intf = self.access_interface
            elif port_type == 'control':
                intf = self.control_interface.split('_', 1)[0]
            elif port_type == 'uplink':
                intf = self.uplink_interface
            del kwargs['port']
            rt_handle.invoke('capture_config', testSessionHandle=self.test_session_handle, tsName=self.tsname, intf=intf, **kwargs)
            rt_handle.invoke('save_config', instance=self.test_session_handle, overwrite=1)
            return
        if action == 'is_fireball':
            result = rt_handle.invoke('get_test_server_info', tsName=self.tsname, infoList=['DataGenPerformance'])
            return result['DataGenPerformance'] == 'Fireball'


class PGWSubscribers(Subscribers):
    """ 5G CUPS subscribers from PGW, which represent PGW subscriber and testcase in spirent
    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar
        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe', 'l2tp'
        :param tag: subscriber group tag
        """
        super().__init__(rinterface, rtinterface, protocol, tag)
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group

        # Taken from CUPSSubscribers
        self.test_session_handle = None
        self.isactive = False
        self.test_session_name = ""
        self.libname = ""
        self.tsname = ""
        self.access_interface = ""
        self.uplink_interface = ""
        self.control_interface = ""
        self.subscriber_group_indices = {}
        self.node_test_case_name = ""
        self.nodal_test_case_name = ""

        self.test_activity = group_config.get('test-activity', 'Command Mode')
        self.session_retries = group_config.get('session-retries', True)
        self.session_count = group_config.get('session-count', '1')
        self.bearer_per_session = group_config.get('default-bearers', '1')
        self.dedicated_bearers = group_config.get('dedicated-bearers', '0')
        # In Nodal this is called the Starting IPv6 Home Address, but in Node this is the Bearer IPv6 Address Pool
        self.bearer_ipv6_addr_pool = group_config.get('bearer-ipv6-addr-pool', 'DB43:2019::0/64')
        # In Nodal this is called the Starting IPv4 Home Address, but in Node this is the Bearer IPv4 Address Pool
        self.bearer_ipv4_addr_pool = group_config.get('bearer-ipv4-addr-pool', '91.0.0.1')
        self.data_mtu = group_config.get('data-mtu', '1400')
        self.apn_name = group_config.get('apn-name', 'mx-upf')
        self.user_initiated_association = group_config.get('user-init-association', False)
        self.home_address_type = group_config.get('home-addr-type', '1')    # 1 for ipv4, 2 for ipv6, 3 for both
        self.sut_loopback_ipv6 = group_config.get('sut-loopback-v6', 'FEED:D00D::1')
        self.sut_loopback_ip = group_config.get('sut-loopback', '100.0.0.1')
        self.use_loopback_access = group_config.get('use-loopback-access', False)
        self.use_loopback_control = group_config.get('use-loopback-control', False)
        self.use_static_address = group_config.get('use-static-addr', False)
        self.heartbeat_retries = group_config.get('heartbeat-retries', '3')
        self.heartbeat_interval = group_config.get('heartbeat-interval', '20')
        self.sx_node_retries = group_config.get('sx-node-retries', '3')
        self.sx_node_retry_interval = group_config.get('sx-node-retry-interval', '5')
        self.sx_session_retries = group_config.get('sx-session-retries', '3')
        self.sx_session_retry_interval = group_config.get('sx-session-retry-interval', '5')
        # Control node counts
        self.sgw_control_node_count = group_config.get('sgw-control-node-count', '1')
        self.pgw_control_node_count = group_config.get('sxb-control-node-count', '1')

        import ipaddress

        self.user_base_address = group_config.get('user-base-address', '10.1.1.1/24')
        self.control_base_address = group_config.get('control-base-address', '20.2.2.1/24')
        self.uplink_base_address = group_config.get('uplink-base-address', '30.3.3.1/24')

        if 'user-v6-base-address' in group_config:
            self.user_v6_base_address = group_config.get('user-v6-base-address')
        if 'control-v6-base-address' in group_config:
            self.control_v6_base_address = group_config.get('control-v6-base-address')
        if 'uplink-v6-base-address' in group_config:
            self.uplink_v6_base_address = group_config.get('uplink-v6-base-address')

        # Logic for consolidating S1U + SGi. Need further granularity on individual interface
        # Get integer 'n' from rinterface.interface_link = 'accessn' ie. access0, access1, access2, etc.
        interface_index = [int(z) for z in list(rtinterface.interface_link) if z.isdigit()][0]
        access_interface_list = bbe.get_interfaces(rtinterface.device_id, interfaces=rinterface.interface_link)
        control_interface_list = bbe.get_interfaces(rtinterface.device_id, interfaces='control'+str(interface_index))
        uplink_interface_list = bbe.get_interfaces(rtinterface.device_id, interfaces='uplink'+str(interface_index))

        if len(access_interface_list) < 1 or len(uplink_interface_list) < 1:
            raise Exception('Must have minimum of 1 access and 1 uplink interface present to initialize a '
                            'CUPSSubscriber object!\n')

        # Check Home Addr type to see if we need v6 uplink network, since decapsulated traffic will be IPv6
        if self.home_address_type == 2 or self.home_address_type == 3:
            self.uplink_v6_base_address = group_config.get('uplink-v6-base-address', 'FEED:BABE::1/64')

        # Assign interfaces to subscriber while we have them anyways. List will have 1 entry due to required
        # unique link names in params.yaml
        self.access_interface = access_interface_list[0].interface_pic
        if hasattr(self, 'user_v6_base_address'):
            self.access_v6_interface = self.access_interface + 'v6'
        self.uplink_interface = uplink_interface_list[0].interface_pic
        if hasattr(self, 'uplink_v6_base_address'):
            self.uplink_v6_interface = self.uplink_interface + 'v6'

        # Can generate IPs dynamically, since many required LS IPs do not matter to DUT. Let user pick their
        # desired base address and we will handle the rest. Next IP is retrieved from next() function applied
        # to appropriate IP iterator
        self.access_ip_generator = iter(ipaddress.IPv4Network(self.user_base_address, strict=False).hosts())
        if hasattr(self, 'user_v6_base_address'):
            self.access_ipv6_generator = iter(ipaddress.IPv6Network(self.user_v6_base_address, strict=False).hosts())
        if len(control_interface_list) == 0:
            t.log('No control interface found. Attaching control-base-network to the access RT port!\n')
            self.control_ip_generator = self.access_ip_generator
            self.control_interface = self.access_interface
            if self.user_base_address != self.control_base_address:
                self.control_ip_generator = iter(ipaddress.IPv4Network(self.control_base_address, strict=False).hosts())
                self.control_interface = str(self.access_interface) + '_1'
            if hasattr(self, 'user_v6_base_address'):
                self.control_ipv6_generator = self.access_ipv6_generator
                self.control_v6_interface = self.access_v6_interface
                if not hasattr(self, 'control_v6_base_address'):
                    self.control_v6_base_address = self.user_v6_base_address
                if (self.user_v6_base_address != self.control_v6_base_address):
                    self.control_ipv6_generator = iter(ipaddress.IPv6Network(
                        self.control_v6_base_address, strict=False).hosts())
                    self.control_v6_interface = str(self.access_v6_interface) + '_1'
        else:
            self.control_ip_generator = iter(ipaddress.IPv4Network(self.control_base_address, strict=False).hosts())
            self.control_interface = control_interface_list[0].interface_pic
            if hasattr(self, 'control_v6_base_address'):
                self.control_ipv6_generator = iter(ipaddress.IPv6Network(
                    self.control_v6_base_address, strict=False).hosts())
                self.control_v6_interface = self.control_interface + 'v6'
        self.uplink_ip_generator = iter(ipaddress.IPv4Network(self.uplink_base_address, strict=False).hosts())
        if hasattr(self, 'uplink_v6_base_address'):
            self.uplink_ipv6_generator = iter(ipaddress.IPv6Network(self.uplink_v6_base_address, strict=False).hosts())


        self.pgw_user_address = str(next(self.access_ip_generator)) # DUT local address for ANP
        self.access_gateway = self.pgw_user_address
        if self.use_loopback_access:
            self.pgw_user_address = self.sut_loopback_ip

        self.sxb_to_up_pgw_user_node = str(next(self.access_ip_generator))

        self.sgw_user_node_start_ip = str(next(self.access_ip_generator))
        self.target_sgw_user_node = str(next(self.access_ip_generator))
        self.sgw_control_node_start_ip = str(next(self.control_ip_generator))
        self.target_sgw_control_node = str(next(self.control_ip_generator))


        if hasattr(self, 'user_v6_base_address'):
            self.pgw_v6_user_address = str(next(self.access_ipv6_generator)) # DUT local address for ANP
            self.v6_access_gateway = self.pgw_v6_user_address
            if self.use_loopback_access:
                self.pgw_v6_user_address = self.sut_loopback_ipv6

            self.sxb_to_up_pgw_v6_user_node = str(next(self.access_ipv6_generator))

            self.sgw_user_node_start_ipv6 = str(next(self.access_ipv6_generator))
            self.target_sgw_user_node_v6 = str(next(self.access_ipv6_generator))
            self.sgw_control_node_start_ipv6 = str(next(self.control_ipv6_generator))
            self.target_sgw_control_node_v6 = str(next(self.control_ipv6_generator))

        # SGW User Node IPs should be consumed in sequence when multiple SGW in use
        if int(self.sgw_control_node_count) > 1:
            self.sgw_user_node_ip_list = []
            self.sgw_user_node_ip_list.append(self.sgw_user_node_start_ip)
            for count in range(self.sgw_control_node_count - 1):
                self.sgw_user_node_ip_list.append(str(next(self.access_ip_generator)))
            self.target_sgw_user_node = str(next(self.access_ip_generator))
            self.target_sgw_user_node_ip_list = []
            self.target_sgw_user_node_ip_list.append(self.target_sgw_user_node)
            for count in range(self.sgw_control_node_count - 1):
                self.target_sgw_user_node_ip_list.append(str(next(self.access_ip_generator)))

            self.sgw_control_node_ip_list = []
            self.sgw_control_node_ip_list.append(self.sgw_control_node_start_ip)
            for count in range(self.sgw_control_node_count - 1):
                self.sgw_control_node_ip_list.append(str(next(self.control_ip_generator)))
            self.target_sgw_control_node = str(next(self.control_ip_generator))
            self.target_sgw_control_node_ip_list = []
            self.target_sgw_control_node_ip_list.append(self.target_sgw_control_node)
            for count in range(self.sgw_control_node_count - 1):
                self.target_sgw_control_node_ip_list.append(str(next(self.control_ip_generator)))
            if hasattr(self, 'user_v6_base_address'):
                self.sgw_user_node_ipv6_list = []
                self.sgw_user_node_ipv6_list.append(self.sgw_user_node_start_ipv6)
                for count in range(self.sgw_control_node_count - 1):
                    self.sgw_user_node_ipv6_list.append(str(next(self.access_ipv6_generator)))
                self.target_sgw_user_node_v6 = str(next(self.access_ipv6_generator))
                self.target_sgw_user_node_ipv6_list = []
                self.target_sgw_user_node_ipv6_list.append(self.target_sgw_user_node_v6)
                for count in range(self.sgw_control_node_count - 1):
                    self.target_sgw_user_node_ipv6_list.append(str(next(self.access_ipv6_generator)))

                self.sgw_control_node_ipv6_list = []
                self.sgw_control_node_ipv6_list.append(self.sgw_control_node_start_ipv6)
                for count in range(self.sgw_control_node_count - 1):
                    self.sgw_control_node_ipv6_list.append(str(next(self.control_ipv6_generator)))
                self.target_sgw_control_node_v6 = str(next(self.control_ipv6_generator))
                self.target_sgw_control_node_ipv6_list = []
                self.target_sgw_control_node_ipv6_list.append(self.target_sgw_control_node_v6)
                for count in range(self.sgw_control_node_count - 1):
                    self.target_sgw_control_node_ipv6_list.append(str(next(self.control_ipv6_generator)))

        self.sxb_to_up_port = '8805'

        # Generate control IPs
        self.sxb_to_up_user_node = str(next(self.control_ip_generator))  # DUT local address for CPP
        if self.user_base_address == self.control_base_address:
            self.sxb_to_up_user_node = self.pgw_user_address
        self.control_gateway = self.sxb_to_up_user_node
        if self.use_loopback_control:
            self.sxb_to_up_user_node = self.sut_loopback_ip
        self.pgw_control_address = str(next(self.control_ip_generator))
        self.pgw_control_node_start_ip = self.pgw_control_address

        # PGW-C IPs should be consumed in sequence when multiple CPF in use
        if int(self.pgw_control_node_count) > 1:
            self.pgw_control_node_ip_list = []
            self.pgw_control_node_ip_list.append(self.pgw_control_address)
            for count in range(self.pgw_control_node_count - 1):
                self.pgw_control_node_ip_list.append(str(next(self.control_ip_generator)))

        self.sgw_control_node_start_ip = str(next(self.control_ip_generator))
        self.sxb_control_node_start_ip = str(next(self.control_ip_generator))

        # Sxab control IPs should be consumed in sequence when multiple CPF in use
        if int(self.pgw_control_node_count) > 1:
            self.sxb_control_node_ip_list = []
            self.sxb_control_node_ip_list.append(self.sxb_control_node_start_ip)
            for count in range(self.pgw_control_node_count - 1):
                self.sxb_control_node_ip_list.append(str(next(self.control_ip_generator)))

        self.sxb_control_gtp_node_start_ip = str(next(self.control_ip_generator))
        self.sxb_to_up_gtp_node = self.sxb_to_up_user_node

        if hasattr(self, 'control_v6_base_address'):
            # Generate control IPs
            self.sxb_to_up_v6_user_node = str(next(self.control_ipv6_generator))  # DUT local address for CPP
            if self.user_v6_base_address == self.control_v6_base_address:
                self.sxb_to_up_v6_user_node = self.pgw_v6_user_address
            self.v6_control_gateway = self.sxb_to_up_v6_user_node
            if self.use_loopback_control:
                self.sxb_to_up_v6_user_node = self.sut_loopback_ipv6
            self.pgw_v6_control_address = str(next(self.control_ipv6_generator))
            self.pgw_control_node_start_ipv6 = self.pgw_v6_control_address

            # PGW-C IPs should be consumed in sequence when multiple CPF in use
            if int(self.pgw_control_node_count) > 1:
                self.pgw_control_node_ipv6_list = []
                self.pgw_control_node_ipv6_list.append(self.pgw_v6_control_address)
                for count in range(self.pgw_control_node_count - 1):
                    self.pgw_control_node_ipv6_list.append(str(next(self.control_ipv6_generator)))

            self.sgw_control_node_start_ipv6 = str(next(self.control_ipv6_generator))
            self.sxb_control_node_start_ipv6 = str(next(self.control_ipv6_generator))

            # Sxab control IPs should be consumed in sequence when multiple CPF in use
            if int(self.pgw_control_node_count) > 1:
                self.sxb_control_node_ipv6_list = []
                self.sxb_control_node_ipv6_list.append(self.sxb_control_node_start_ipv6)
                for count in range(self.pgw_control_node_count - 1):
                    self.sxb_control_node_ipv6_list.append(str(next(self.control_ipv6_generator)))

            self.sxb_control_gtp_node_start_ipv6 = str(next(self.control_ipv6_generator))
            self.sxb_to_up_gtp_node_v6 = self.sxb_to_up_v6_user_node

        # Generate uplink IPs
        self.uplink_gateway = str(next(self.uplink_ip_generator))
        self.traffic_start_ip = str(next(self.uplink_ip_generator))
        if hasattr(self, 'uplink_v6_base_address'):
            self.v6_uplink_gateway = str(next(self.uplink_ipv6_generator))
            self.traffic_start_ipv6 = str(next(self.uplink_ipv6_generator))

        # PGW Nodal S11
        self.s11_gtpv2_version = group_config.get('gtpv2-version', '15.2.0')
        self.s11_total_apns = group_config.get('total-apns', '1')
        self.s11_start_imsi = group_config.get('start-imsi', '505024101215074')
        self.s11_start_imei = group_config.get('start-imei', '50502410121507')
        self.s11_radio_access_type = group_config.get('radio-access-type', 'eutran')
        self.s11_gtp_c_tunnel_id = group_config.get('start-gtp-c-tunnel-id', '1000000')
        self.s11_gtp_u_tunnel_id = group_config.get('start-gtp-u-tunnel-id', '1048576')
        self.s11_total_apns = group_config.get('total-apns', '1')

        # PGW Node S11
        self.node_start_imsi = group_config.get('start-imsi', '505024101215074')
        self.node_start_imei = group_config.get('start-imei', '50502410121507')
        self.node_radio_access_type = group_config.get('radio-access-type', 'eutran')
        self.node_gtp_c_tunnel_id = group_config.get('start-gtp-c-tunnel-id', '1000000')
        self.node_gtp_u_tunnel_id = group_config.get('start-gtp-u-tunnel-id', '1048576')
        self.node_total_apns = group_config.get('total-apns', '1')
        self.node_gtpv2_version = group_config.get('gtpv2-version', '15.2.0')

        # VLANs
        if group_config.get('access-vlan-id') is not None:
            self.access_vlan_id = group_config.get('access-vlan-id')
        if group_config.get('control-vlan-id') is not None:
            self.control_vlan_id = group_config.get('control-vlan-id')
        if group_config.get('uplink-vlan-id') is not None:
            self.uplink_vlan_id = group_config.get('uplink-vlan-id')

        # Creates data structure allowing user to have different login groups within single Test Session
        if 'Command Mode' in self.test_activity and group_config.get('session-groups') is not None:
            count = 1
            for group in sorted(group_config['session-groups']):
                start_index = count
                stop_index = count + group_config['session-groups'][group] - 1
                self.subscriber_group_indices[group] = (start_index, int(stop_index))
                count += int(group_config['session-groups'][group])
        self.subscriber_group_indices['default'] = (1, self.session_count)

    def action(self, action='start', **kwargs):
        """
        kwargs:
        port:    access/uplink port
        filename:   filename for captured file
        :return:
        """
        #import jnpr.toby.bbe.testers.ls as ls
        rt_device = self.rt_device_id
        rt_handle = t.get_handle(rt_device)
        if action not in ['start', 'stop', 'abort', 'results', 'logout', 'continue', 'report',
                          'delete', 'capture_start', 'capture_stop', 'capture_save', 'start_with_auto_pcap',
                          'automation_control', 'check_session_status', 'capture_config', 'is_fireball']:
            raise Exception("action {} is not supported".format(action))
        if action in ['capture_start', 'capture_stop', 'capture_save']:
            port_type = kwargs.get('port', 'access')
            interface_list = []
            if port_type == 'access':
                interface_list.append(self.access_interface)
            if port_type == 'uplink':
                interface_list.append(self.uplink_interface)
            if port_type == 'control':
                # Remove any underscores from subscriber.control_interface that were required for reserve_ports.
                # This will only change the control_interface string for port capture if separate networks were needed
                # for controlcand access in a two port setup
                interface_list.append(self.control_interface.split('_', 1)[0])
            if port_type == 'all':
                interface_list.append(self.access_interface)
                interface_list.append(self.uplink_interface)
                interface_list.append(self.control_interface.split('_', 1)[0])
            if action == 'capture_start':
                if not self.isactive:
                    t.log("starting testsession {} before doing capture_start action".format(self.test_session_name))
                    self.action(action='start')
                rt_handle.invoke('capture_action', tsName=self.tsname, action='start', intfList=interface_list)
                t.log("starting capturing packets on interface {}".format(interface_list))
                return
            if action == 'capture_stop':
                rt_handle.invoke('capture_action', tsName=self.tsname, action='stop', intfList=interface_list)
                t.log("stopped capturing packets on interface {}".format(interface_list))
                return
            if action == 'capture_save':
                filename = rt_handle.invoke('capture_action', tsName=self.tsname, action='Retrieve',
                                            intfList=interface_list, pcapDir='/tmp')
                #t.log("saved captured file to user log firectory {}, file list is {}".format(t._log_dir, filename))
                t.log("saved captured file in /tmp, file list is {}".format(filename))
                return filename
        if action == 'start':
            if not self.isactive:
                response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Run')
                self.isactive = True
            t.log("test session {} is started ".format(self.test_session_name))
            return
        if action == 'start_with_auto_pcap':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Run',
                                        autoCaptureOnStart='true')
            self.isactive = True
            t.log("test session {} is started with auto packet capture option ".format(self.test_session_name))
            return
        if action == 'stop':
            if self.isactive:
                response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Stop')
                self.isactive = False
            t.log("test session {} is stopped ".format(self.test_session_name))
            return
        if action == 'continue':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Continue')
            return
        if action == 'abort':
            response = rt_handle.invoke('test_control', testSessionHandle=self.test_session_handle, action='Abort')
            self.isactive = False
            t.log("test session {} is aborted".format(self.test_session_name))
            return
        if action == 'report':
            response = rt_handle.invoke('generate_tac_report', testSessionHandle=self.test_session_handle,
                                        reportDir='/tmp/{}.zip'.format(self.test_session_name))
            t.log("saved report file /tmp/{}.zip".format(self.test_session_name))
            return
        if action == 'results':
            response = rt_handle.invoke('get_test_results', testSessionHandle=self.test_session_handle, **kwargs)
            return response
        if action == 'logout':
            response = rt_handle.invoke('logout_from_server')
            t.log("disconnected from tester")
            return
        if action == 'delete':
            response = rt_handle.invoke('delete_test_session', testSessionName=self.test_session_name,
                                        libraryName=self.libname)
            t.log("deleted test session {}".format(self.test_session_name))
            return
        if action == 'automation_control':
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Init', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Start', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName='Wait')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Init', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Start', tsName=self.tsname)
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName='Wait')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Stop', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.nodal_test_case_name,
                             predecessorState='RUNNING')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.nodal_test_case_name, tcActivity='Cleanup', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.nodal_test_case_name,
                             predecessorState='STOPPED')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Stop', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.node_test_case_name,
                             predecessorState='RUNNING')
            rt_handle.invoke('automation_control', mode='create', testSessionHandle=self.test_session_handle,
                             functionTcName=self.node_test_case_name, tcActivity='Cleanup', tsName=self.tsname,
                             predecessorTsName=self.tsname, predecessorTcName=self.node_test_case_name,
                             predecessorState='STOPPED')
            validation_status = rt_handle.invoke('validate_test_configuration',
                                                 testSessionHandle=self.test_session_handle)
            t.log("Validation Status after automation_control: {}".format(validation_status))
            rt_handle.invoke('save_config', instance=self.test_session_handle, overwrite=1)
            return
        if action == 'check_session_status':
            if 'state' not in kwargs:
                raise Exception('kwargs[\'state\'] is a required parameter for this action.\nSupported states are: '
                                'running/complete/waiting')
            invoke_command = 'ls::get ' + self.test_session_handle + ' -TestStateOrStep'
            result = rt_handle.invoke('invoke', cmd=invoke_command)

            if kwargs['state'].lower() in result.lower():
                t.log('Desired state \'{}\' reached\n'.format(kwargs['state']))
                return
            else:
                raise Exception('Test Session state is not \'{}\' yet!\n'.format(kwargs['state']))
        if action == 'capture_config':
            port_type = kwargs.get('port', 'access')
            if port_type == 'access':
                intf = self.access_interface
            elif port_type == 'control':
                intf = self.control_interface.split('_', 1)[0]
            elif port_type == 'uplink':
                intf = self.uplink_interface
            del kwargs['port']
            rt_handle.invoke('capture_config', testSessionHandle=self.test_session_handle, intf=intf, **kwargs)
            rt_handle.invoke('save_config', instance=self.test_session_handle, overwrite=1)
            return
        if action == 'is_fireball':
            result = rt_handle.invoke('get_test_server_info', tsName=self.tsname, infoList=['DataGenPerformance'])
            return result['DataGenPerformance'] == 'Fireball'


class FWASubscribers(HAGSubscribers):
    """ Fixed Wireless Access (FWA) subscribers, which represent FWA subscriber and testcase in spirent
    """
    def __init__(self, rinterface, rtinterface, protocol, tag):
        """Initialize instance and store the instance object into bbevar
        :param rinterface: router BBEVarInterface
        :param rtinterface: rt BBEVarInterface
        :param protocol: subscriber protocol, e.g. 'dhcp', 'pppoe', 'l2tp'
        :param tag: subscriber group tag
        """
        ##Group Config
        super().__init__(rinterface, rtinterface, protocol, tag)
        # Find the relevant group
        for group in rinterface.interface_config['subscribers'][protocol]:
            if tag == group['tag']:
                group_config = group
        self.bearer_per_session = group_config.get('bearer-per-session', '1')
        self.dedicated_bearers = group_config.get('dedicated-bearers', '0')
        self.activation_rate = group_config.get('activation-rate', '1')
        self.deactivation_rate = group_config.get('deactivation-rate', '1')
        self.bearer_ipv6_addr_pool = group_config.get('bearer-ipv6-addr-pool', '1::0')
        self.bearer_ipv4_addr_pool = group_config.get('bearer-ipv4-addr-pool', '91.0.0.1')

        self.sgw_control_address = group_config['devices']['sgw']['control-address']
        self.sgw_user_address = group_config['devices']['sgw']['user-address']

        self.pgw_address = group_config['devices']['pgw']['address']
        self.mme_control_node_start_ip = group_config['devices']['mme-control-node']['start-ip']
        self.mme_control_node_count = group_config['devices']['mme-control-node'].get('count', '1')

        self.enodeb_user_node_start_ip = group_config['devices']['enodeb-user-node']['start-ip']

        self.data_mtu = group_config['devices'].get('data-mtu', '1400')

        self.dhcp_client_id = group_config['dhcp'].get('client-id', 'DEFAULTUSER')
        self.dhcp_retries = group_config['dhcp'].get('retries', '3')
        self.dhcp_v6_ia_type = group_config['dhcp'].get('v6-ia-type', 'IA_PD')
        self.dhcp_mac = group_config['dhcp'].get('mac', '00:11:22:33:44:55')
        
        # define s11 for Nodal
        if 's11' in group_config:
            self.s11_gtpv2_version = group_config['s11'].get('gtpv2-version', '13.6.0')
            self.s11_start_imsi = group_config['s11'].get('start-imsi', '505024101215074')
            self.s11_start_imei = group_config['s11'].get('start-imei', '50502410121507')
            self.s11_radio_access_type = group_config['s11'].get('radio-access-type', 'eutran')
            self.s11_gtp_c_tunnel_id = group_config['s11'].get('start-gtp-c-tunnel-id', '1000000')
            self.s11_gtp_u_tunnel_id = group_config['s11'].get('start-gtp-u-tunnel-id', '2000000')
            self.s11_total_apns = group_config['s11'].get('total-apns', '1')
            self.apn_name = group_config['s11'].get('apn-name', 'ssenoauth146')
        else:
            self.s11_gtpv2_version = '13.6.0'
            self.s11_start_imsi = '505024101215074'
            self.s11_start_imei = '50502410121507'
            self.s11_radio_access_type = 'eutran'
            self.s11_gtp_c_tunnel_id = '1000000'
            self.s11_gtp_u_tunnel_id = '2000000'
            self.s11_total_apns = '1'
            self.apn_name = 'ssenoauth146'
