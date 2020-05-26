# pylint: disable=undefined-variable
# p-ylint: disable=invalid-name
"""Module contains methods for CGNAT"""
__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re

from jnpr.toby.utils import iputils
from jnpr.toby.services import utils

from jnpr.toby.services.services import services


class cgnat(services):
    """Class contains methods for CGNAT"""

    def __init__(self, **kwargs):
        """Constructor method for cgnat class"""

        super().__init__(**kwargs)

        self.cmd_list = []
        self.nat_rule = {}
        self.nat_pool = {}
        self.port_fwd = {}
        self.ss_profile = {}
        self.tg_sess = None
        self.cmd = None
        self.ptr = None
        self.num_sess = None
        self.pool_map = {}
        #self.sset_map = {}
        self.nat_pool_rule_map = {}

        self.ss_map['nat_pool'] = {}

        self.data['nat_pool'] = {}
        self.data['sess_xtnsv'] = {}

        for key in kwargs:
            setattr(self, key, kwargs[key])

    ################################################################
    # set methods
    ################################################################
    def set_nat_rule(self, name='nat_rule', **kwargs):
        """Configure NAT rule based on parameters passed

        Use the optional argument, 'count', to generate scaling config.
        For example, This will create 10 NAT rules from nat_rule1 to nat_rule9::

            set_nat_rule(name='nat_rule', count=10)

        To delete a config, call set_nat_rule with action='delete'
        For example, To delete translation type::

            set_nat_rule(name='nat_rule', action='delete', term=1, trans_type='basic-nat44')
            This API will execute
            'delete services nat rule nat_rule1 term 1 then translated translation-type basic-nat44'

        :param string name:
            **OPTIONAL** NAT rule name. Default is 'nat_rule'

        :param string action:
            **OPTIONAL** Valid values are set,delete,activate,deactivate. Default value is 'set'

        :param int count:
            **OPTIONAL** Number of NAT Rules to be configured. Default is 1

        :param int term:
            **OPTIONAL** Term name. Default value is 0

        :param int index:
            **OPTIONAL** Rule starting index. Default value is 1

        :param string dir:
            **OPTIONAL** NAT direction. Defaul value is 'input'

        :param int num_terms:
            **OPTIONAL** Number of terms. Default is 1

        :param bool pool_scale_term:
            **OPTIONAL** Whether to scale poolnames per term. Default is False.

        :param bool term_idx_reset:
            **OPTIONAL** Whether to reset term index for every rule. Default is False.

        :param string src_addr:
            **OPTIONAL** From Source IP Address. Default is None

        :param int src_addr_step:
            **OPTIONAL** From Source IP Address step. Default is 1

        :param int src_addr_nw_step:
            **OPTIONAL** Number by which source network address will be incremented.

        :param int src_addr_nw_step_cnt:
            **OPTIONAL** Number of SrcIP network increments after which Src Network address
            will be incremented by src_addr_nw_step.

        :param string src_low:
            **OPTIONAL** Lower limit of the Source IP Addr Range

        :param string src_high:
            **OPTIONAL** Higher limit of the Source IP Addr Range

        :param string src_pfx:
            **OPTIONAL** NAT prefix for source translation. Default is None.

        :param int src_pfx_step:
            **OPTIONAL** Number by which source prefix will be incremented by. Default is 1

        :param string list src_pfx_list:
            **OPTIONAL** Source Prefix List

        :param string dst_addr:
            **OPTIONAL** From Destination IP Address. Default is None

        :param int dst_addr_step:
            **OPTIONAL** From Destination IP Address step. Default is 1

        :param string dst_low:
            **OPTIONAL** Lower limit of the Destination IP Addr Range

        :param string dst_high:
            **OPTIONAL** Higher limit of the Destination IP Addr Range

        :param int dst_port_low:
            **OPTIONAL** Lower limit of the Destination Port Addr Range

        :param int dst_port_high:
            **OPTIONAL** Higher limit of the Destination Port Addr Range

        :param int dst_pfx:
            **OPTIONAL** NAT prefix for Destination translation

        :param int dst_pfx_step:
            **OPTIONAL** Number by which destination prefix will be incremented by. Default is 1

        :param string list dst_pfx_list:
            **OPTIONAL** Destination Prefix List

        :param string clat_pfx:
            **OPTIONAL** CLAT prefix

        :param int clat_pfx_step:
            **OPTIONAL** Number by which clat prefix will be incremented by. Default is 1

        :param int rs_name:
            **OPTIONAL** Rule-set name

        :param int rs_scaling:
            **OPTIONAL** To scale rule-set name or not

        :param string list from_apps_list:
            **OPTIONAL** List of applications to be matched

        :param string list from_appsets_list:
            **OPTIONAL** List of application sets to be matched

        :param string src_pool:
            **OPTIONAL** NAT Pool for Source translation

        :param string dst_pool:
            **OPTIONAL** NAT Pool for Destination translation

        :param string dns_alg_pfx:
            **OPTIONAL** DNS ALG Prefix

        :param string trans_type:
            **OPTIONAL** NAT Translation type

        :param boot trans_eim:
            **OPTIONAL** Flag to set mapping type as EIM.

        :param bool trans_eif:
            **OPTIONAL** Flat to set filtering type as EIF.

        :param bool addr_pool:
            **OPTIONAL** Flag to enable address pooling as paired.

        :param list trans_eif_pfx_list:
            **OPTIONAL** Source prefixes to match for EIF


        :param string snat_map_refresh:
            **OPTIONAL** Secure NAT Mapping refresh type.
            Valid values are inbound, outbound, inbound-outbound


        :param int snat_eif_flow_limit:
            **OPTIONAL** Secure NAT Mapping EIF Flow limit.
            Number of inbound flows to be allowed for a EIF mapping (0..65534)


        :param string port_fwd_map:
            **OPTIONAL** Port forward mapping


        :param bool allow_overlap:
            **OPTIONAL** Flag to allow overlapping nat pools

        :param bool ams_warm_standby:
            **OPTIONAL** Flag to allow NAT on AMS warm standby

        :param bool then_syslog:
            **OPTIONAL** Flag to enable syslog

        :param bool no_trans:
            **OPTIONAL** To enable no-translations

        :param bool src_any_ucast:
            **OPTIONAL** From Source address as any-unicast instead of IP address

        :param bool dst_any_ucast:
            **OPTIONAL** From Destination address as any-unicast instead of IP address


        :return: True if config is successful else False
        :rtype: bool

        Example::

            Python:
                hCgn.set_nat_rule(name='rule', **kwargs)
                To create rule with all default options:
                hCgn.set_nat_rule()
                To create rule2:
                hCgn.set_nat_rule(name='rule', index=2, **kwargs)
            Robot:
                hCgn.Set NAT Rule   name=rule
                hCgn.Set NAT Rule
                hCgn.Set NAT Rule  name=rule   index=2
        """

        self.fn_checkin("Configuring NAT Rule")

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'dir': 'input',
                                               'term': 0, 'num_terms': 1, 'rs_name': None,
                                               'pool_scale_term': False, 'term_idx_reset': False,
                                               'src_addr': None, 'src_addr_step': 1,
                                               'src_addr_nw_step': 1, 'src_addr_nw_step_cnt': None,
                                               'src_pfx': None, 'src_pfx_step': 1, 'index': 1,
                                               'dst_addr': None, 'dst_addr_step': 1,
                                               'dst_pfx': None, 'dst_pfx_step': 1,
                                               'clat_pfx': None, 'clat_pfx_step': 1,
                                           })

        src_addr = this['src_addr']
        dst_addr = this['dst_addr']
        src_pfx = this['src_pfx']
        dst_pfx = this['dst_pfx']
        clat_pfx = this['clat_pfx']
        term = this['term']
        rule_idx = this['index']

        src_addr_cntr = 0

        for _ in range(1, this['count']+1):
            rule_tag = name + str(rule_idx)
            if rule_tag not in self.nat_rule:
                self.nat_rule[rule_tag] = {}
            self.ptr = self.nat_rule[rule_tag]
            #self._update(this)
            #self.ptr = this

            pool_tag = rule_idx
            self.cmd = "{} services nat".format(this['action'])
            if this['rs_name']:
                self.cmd_add("rule-set {}{} rule {}".format(this['rs_name'], rule_idx, rule_tag))

            self.cmd_add("rule {} match-direction {}".format(rule_tag, this['dir']))
            self.cmd_add("allow-overlapping-nat-pools", 'allow_overlap', opt='flag')
            self.cmd_add("allow-all-nat-on-ams-warm-standby", 'ams_warm_standby', opt='flag')

            if this['term_idx_reset']:
                term = int(this['term'])

            for _ in range(0, this['num_terms']):
                self.cmd = "{} services nat rule {} term {}".format(this['action'], rule_tag, term)
                if term not in self.nat_rule[rule_tag]:
                    self.nat_rule[rule_tag][term] = {}
                self.ptr = self.nat_rule[rule_tag][term]
                self._update(this)
                #self.ptr = this
                self._cmd_name_tag = rule_tag
                self._cmd_mapping = self.nat_pool_rule_map

                self.cmd_add("then syslog", 'then_syslog', opt='flag')
                self.cmd_add("then no-translation", 'no_trans', opt='flag')
                self.cmd_add("from source-address any-unicast", 'src_any_ucast', opt='flag')
                self.cmd_add("from destination-address any-unicast", 'dst_any_ucast', opt='flag')

                if src_addr is not None:
                    self.cmd_add("from source-address {}".format(src_addr))
                    self.ptr['src_addr'] = src_addr
                    src_addr_cntr += 1
                    if this['src_addr_nw_step_cnt'] and \
                       src_addr_cntr % this['src_addr_nw_step_cnt'] == 0:
                        _src_addr_step_idx = (src_addr_cntr / this['src_addr_nw_step_cnt'])
                        _src_addr_step = (_src_addr_step_idx * this['src_addr_nw_step'])
                        src_addr = iputils.incr_ip_subnet(this['src_addr'], _src_addr_step)
                    else:
                        src_addr = iputils.incr_ip_subnet(src_addr, this['src_addr_step'])

                if dst_addr is not None:
                    self.cmd_add("from destination-address {}".format(dst_addr))
                    self.ptr['dst_addr'] = dst_addr
                    dst_addr = iputils.incr_ip_subnet(dst_addr, this['dst_addr_step'])

                if 'src_low' in this and 'src_high' in this:
                    _range_str = "low {} high {}".format(this['src_low'], this['src_high'])
                    self.cmd_add("from source-address-range {}".format(_range_str))

                if 'dst_low' in this and 'dst_high' in this:
                    _range_str = "low {} high {}".format(this['dst_low'], this['dst_high'])
                    self.cmd_add("from destination-address-range {}".format(_range_str))

                if 'dst_port_low' in this and 'dst_port_high' in this:
                    _dst_str = "low {} high {}".format(this['dst_port_low'], this['dst_port_high'])
                    self.cmd_add("from destination-port range {}".format(_dst_str))

                self.cmd_add("from applications", 'from_apps_list')
                self.cmd_add("from application-sets", 'from_appsets_list')

                self.cmd_add("from source-prefix-list", 'src_pfx_list')
                self.cmd_add("from destination-prefix-list", 'dst_pfx_list')

                self.cmd_add("then translated source-pool", 'src_pool', tag=pool_tag,
                             mapping=True)
                self.cmd_add("then translated destination-pool", 'dst_pool', tag=pool_tag,
                             mapping=True)
                self.cmd_add("then translated dns-alg-prefix", 'dns_alg_pfx', tag=pool_tag)
                pool_tag += 1

                if src_pfx is not None:
                    self.cmd_add("then translated source-prefix {}".format(src_pfx))
                    self.ptr['src_pfx'] = src_pfx
                    src_pfx = iputils.incr_ip_subnet(src_pfx, this['src_pfx_step'])

                if clat_pfx is not None:
                    self.cmd_add("then translated destination-prefix {}".format(clat_pfx))
                    self.ptr['clat_pfx'] = clat_pfx
                    clat_pfx = iputils.incr_ip_subnet(clat_pfx, this['clat_pfx_step'])

                if dst_pfx is not None:
                    self.cmd_add("then translated destination-prefix {}".format(dst_pfx))
                    self.ptr['dst_pfx'] = dst_pfx
                    dst_pfx = iputils.incr_ip_subnet(dst_pfx, this['dst_pfx_step'])

                self.cmd_add("then translated translation-type", 'trans_type')
                self.cmd_add("then translated mapping-type endpoint-independent", 'trans_eim',
                             opt='flag')
                self.cmd_add("then translated filtering-type endpoint-independent", 'trans_eif',
                             opt='flag')
                self.cmd_add("then translated address-pooling paired", 'addr_pool', opt='flag')
                self.cmd_add("then translated filtering-type endpoint-independent prefix-list",
                             'trans_eif_pfx_list')
                self.cmd_add("then port-forwarding-mappings", 'port_fwd_map')
                self.cmd_add("then translated secure-nat-mapping mapping-refresh",
                             'snat_map_refresh')
                self.cmd_add("then translated secure-nat-mapping eif-flow-limit",
                             'snat_eif_flow_limit')

                term += 1

            rule_idx += 1

        result = self.config()

        return self.fn_checkout(result)

    def set_nat_pool(self, name='nat_pool', **kwargs):
        """Configure NAT pool based on parameters passed

        Use the optional argument, 'count', to generate scaling config.
        For example, This will create 10 NAT pools from nat_pool1 to nat_pool9::

            set_nat_pool('nat_pool', count=10)

        :param string name:
            **OPTIONAL** Name of NAT pool to be configured. Default is 'nat_pool'

        :param string action:
            **OPTIONAL** Valid values are set,delete,activate,deactivate. Default is 'set'

        :param int count:
            **OPTIONAL** Number of NAT Pools to be configured. Default is 1.

        :param string addr:
            **OPTIONAL** Pool address

        :param string addr_low:
            **OPTIONAL** Pool address range - low

        :param string addr_high:
            **OPTIONAL** Pool address range - high

        :param int addr_range_step:
            **OPTIONAL** Step by which pool address low and high ips need to be incremented

        :param int port_low:
            **OPTIONAL** Pool port range - low

        :param int port_high:
            **OPTIONAL** Pool port range - high

        :param bool port_range_random:
            **OPTIONAL** Flag for Pool port range random allocation

        :param int port_limit:
            **OPTIONAL** Port limit per address

        :param int map_to:
            **OPTIONAL** Default Mapping timeout (120s-86400s)

        :param int app_to:
            **OPTIONAL** APP Mapping timeout (120s-86400s)

        :param int eim_to:
            **OPTIONAL** EIM timeout (120s-86400s)

        :param bool addr_alloc_rr:
            **OPTIONAL** Flag to set Address-allocation to round-robin

        :param bool port_pres_parity:
            **OPTIONAL** Flag to set port preserve parity
            (set services nat pool <pool> port preserve-parity)

        :param bool port_pres_range:
            **OPTIONAL** Flag to set port preserve range
            (set services nat pool <pool> port preserve-range)

        :param bool port_auto:
            **OPTIONAL** Flag to set automatic port allocation
            (set services nat pool <pool> port automatic)

        :param bool port_auto_auto:
            **OPTIONAL** Flag to set automatic port allocation
            (set services nat pool <pool> port automatic auto)

        :param bool port_auto_random:
            **OPTIONAL** Flag to set automatic port random allocation
            (set services nat pool <pool> port automatic random-allocation)

        :param bool port_pba:
            **OPTIONAL** Flag to set port to secured port block allocation

        :param int port_pba_blk_to:
            **OPTIONAL** Sets PBA active block timeout

        :param int port_pba_blk_size:
            **OPTIONAL** Sets PBA block size

        :param int port_pba_max_blks:
            **OPTIONAL** Sets PBA max blocks per address

        :param bool port_detnat:
            **OPTIONAL** Flag to enable port deterministic-PBA

        :param string port_detnat_blk_size:
            **OPTIONAL** Sets port deterministic-PBA block size

        :param bool port_detnat_incl_bndry_addrs:
            **OPTIONAL** Flag to include port deterministic-PBA boundary addresses

        :param int snmp_trap_low:
            **OPTIONAL** SNMP Trap Address port range - low

        :param int snmp_trap_high:
            **OPTIONAL** SNMP Trap Address port range - high


        :return: True if config is successful else False

        :rtype: bool

        Example::

            Python:
                set_nat_pool(name='nat_pool', **kwargs)
            Robot:
                Set NAT Pool   name=nat_pool

        """

        self.fn_checkin("Configuring NAT pool")

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set',
                                               'addr': None, 'addr_range_step': 1,
                                               'addr_low': None, 'addr_high': None,
                                               'port_low': None, 'port_high': None
                                           })

        (addr, addr_low, addr_high) = (this['addr'], this['addr_low'], this['addr_high'])

        for iter_ii in range(1, this['count'] + 1):
            # rule_tag = name + iter_ii
            #tag = iter_ii
            pool_name = name + str(iter_ii)
            if pool_name not in self.nat_pool:
                self.nat_pool[pool_name] = {}
            self.ptr = self.nat_pool[pool_name]
            self._update(this)
            self.cmd = "{} services nat pool {}".format(this['action'], pool_name)

            if addr is not None:
                self.cmd_add("address {}".format(addr))
                self.ptr['addr'] = addr
                addr = iputils.incr_ip_subnet(this['addr'], iter_ii)
            if addr_low is not None and addr_high is not None:
                self.cmd_add("address-range low {} high {}".format(addr_low, addr_high))
                self.ptr['addr_low'] = addr_low
                self.ptr['addr_high'] = addr_high
                addr_low = iputils.incr_ip(this['addr_low'], iter_ii * this['addr_range_step'])
                addr_high = iputils.incr_ip(this['addr_high'], iter_ii * this['addr_range_step'])
            if this['port_low'] is not None and this['port_high'] is not None:
                if 'port_range_random' in this and this['port_range_random']:
                    _range_str = "low {} high {}".format(this['port_low'], this['port_high'])
                    self.cmd_add("port range {} random-allocation".format(_range_str))
                else:
                    self.cmd_add("port range low {} high {}".format(this['port_low'],
                                                                    this['port_high']))

            self.cmd_add("limit-ports-per-address", 'port_limit')
            self.cmd_add("mapping-timeout", 'map_to')
            self.cmd_add("app-mapping-timeout", 'app_to')
            self.cmd_add("ei-mapping-timeout", 'eim_to')
            self.cmd_add("address-allocation round-robin", 'addr_alloc_rr', opt='flag')

            self.cmd_add("port preserve-parity", 'port_pres_parity', opt='flag')
            self.cmd_add("port preserve-range", 'port_pres_range', opt='flag')
            self.cmd_add("port automatic", 'port_auto', opt='flag')
            self.cmd_add("port automatic auto", 'port_auto_auto', opt='flag')
            self.cmd_add("port automatic random-allocation", 'port_auto_random', opt='flag')
            if 'snmp_trap_low' in this and 'snmp_trap_high' in this:
                _snmp_str = "low {} high {}".format(this['snmp_trap_low'], this['snmp_trap_high'])
                self.cmd_add("snmp-trap-thresholds address-port {}".format(_snmp_str))

            #self.cmd_add("port secured-port-block-allocation", 'port_pba', opt='flag')

            #_cmd = self.cmd = "{} services nat pool {}".format(this['action'], pool_name)
            _cmd = self.cmd
            self.cmd = _cmd + " port secured-port-block-allocation"

            self.cmd_add("", 'port_pba', opt='flag')
            self.cmd_add("active-block-timeout", 'port_pba_blk_to')
            self.cmd_add("block-size", 'port_pba_blk_size')
            self.cmd_add("max-blocks-per-address", 'port_pba_max_blks')

            #self.cmd_add("port deterministic-port-block-allocation", 'port_detnat', opt='flag')
            self.cmd = _cmd + " port deterministic-port-block-allocation"
            self.cmd_add("", 'port_detnat', opt='flag')
            self.cmd_add("block-size", 'port_detnat_blk_size')
            self.cmd_add("include-boundary-addresses", 'port_detnat_incl_bndry_addrs', opt='flag')

            # when the action is not 'set' and there are no other command
            # options to be executed
            if len(self.cmd_list) == 0 and this['action'] != 'set':
                self.cmd_add("")

        result = self.config()

        self.log('INFO', "NAT Pool: {}".format(self.nat_pool))

        return self.fn_checkout(result)

    def set_port_forward_rule(self, name='port_fwd_rule', **kwargs):
        """Configure Port Forward Rule based on the parameters passed.

        :param string name:
            **OPTIONAL** Name of Port Forward Rule to be configured. Default is 'port_fwd_rule'

        :param string action:
            **OPTIONAL** Valid values are set,delete,activate,deactivate. Default value is 'set'

        :param int dst_port:
            **OPTIONAL** Destined port

        :param int trans_port:
            **OPTIONAL** Translated port


        :return: True if config is successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.set_port_forward(name='port_fwd_rule', **kwargs)
                hCgn.set_port_forward()
            Robot:
                hCgn.Set Port Forward   name=port_fwd_rule  dst_port=1234  trans_port=23
        """

        self.fn_checkin("Configuring Port Forward Rule")

        this = utils.update_opts_from_args(kwargs, defaults={'action': 'set'})

        if 'dst_port' not in this or 'trans_port' not in this:
            raise MissingMandatoryArgument('dst_port/trans_port')

        if name not in self.port_fwd:
            self.port_fwd[name] = {}
        self.ptr = self.port_fwd[name]
        self._update(this)

        self.cmd = "{} services nat port-forwarding {}".format(this['action'], name)

        self.cmd_add("destined-port {} translated-port {}".format(this['dst_port'],
                                                                  this['trans_port']))

        result = self.config()

        return self.fn_checkout(result)

    ################################################################
    # Get/Verify methods
    ################################################################
    def verify(self, **kwargs):
        """Wrapper for minimum verifications to be done for CGNAT

        This will call services.verify() to do all basic Services verifications required.

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.verify()
            Robot:
                hCgn.Verify
        """

        self.fn_checkin("Verifying CGNAT")

        #self._get_tg_sess(**kwargs)
        #self._get_tg_port_and_config_mapping(**kwargs)
        self._get_tg_port_and_config_mapping(**kwargs)

        super().verify(**kwargs)

        # self.verify_sess_count(**kwargs)
        # self.tg_sess = kwargs.pop('tg_sess')
        self.verify_nat_pool_detail(**kwargs)
        self.verify_sessions_extensive(**kwargs)
        # self.verify_nat_eim(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_mappings_detail(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_app_mappings(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_mappings_summary(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_statistics(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_syslogs(tg_sess=self.tg_sess, **kwargs)

        return self.fn_checkout()

    def get_nat_pool_detail(self, name=None):
        """Fetch NAT Pool details as dictionary

        :param string name:
            **OPTIONAL** Name of the NAT pool. If name is passed, details of that NAT Pool
                are fetched. Else, details for all the pools configured (saved in the object)
                will be fetched. Default is None

        :return: True if command output is processed successfully

        :rtype: bool

        Example::

            Python:
                hCgn.get_nat_pool_detail()
                hCgn.get_nat_pool_detail(name='pool1')
            Robot:
                hCgn.Get NAT Pool Detail
                hCgn.Get NAT Pool Detail   name=pool1
        """

        self.fn_checkin("Fetching NAT Pool detail")

        if 'nat_pool' not in self.data:
            self.data['nat_pool'] = {}

        # If name is specified, get details for that pool else for all the pools configured
        # Need to take care of scaling scenarios. Don't need to get details of
        # all the pools
        names = [name] if name is not None else self.nat_pool.keys()

        _xpath = 'service-nat-pool-information/sfw-per-service-set-nat-pool'
        for pool_name in names:
            cmd = 'show services nat pool {} detail'.format(pool_name)
            entry = self.get_xml_output(cmd, xpath=_xpath)
            if pool_name not in self.data['nat_pool']:
                self.data['nat_pool'][pool_name] = {}
            self.data['nat_pool'][pool_name]['spic'] = str(entry['interface-name'])
            self.data['nat_pool'][pool_name]['sset'] = str(entry['service-set-name'])
            ptr = self.data['nat_pool'][pool_name]

            pool = entry['service-nat-pool']

            ptr['addr_range'] = str(pool['pool-address-range-list']['pool-address-range'])
            ptr['addr_range_low'], ptr['addr_range_high'] = ptr['addr_range'].split('-')
            ptr['trans_type'] = str(pool['translation-type'])

            utils.update_data_from_output(ptr, pool, {
                'pool-addresses-in-use': 'addrs_in_use',
                'pool-out-of-address-errors': 'out_of_addr_errs',
                'pool-port-range': 'port_range',
                'pool-ports-in-use': 'ports_in_use',
                'pool-out-of-port-errors': 'out_of_port_errs',
                'pool-max-ports-in-use': 'max_ports_in_use',
                'max-port-blocks-used': 'max_blks_used',
                'port-blocks-in-use': 'ports_blks_in_use',
                'port-block-allocation-errors': 'port_blk_alloc_errs',
                'port-block-mem-alloc-failure-errors': 'port_blk_mem_alloc_fail_errs',
                'pool-parity-port-errors': 'parity_port_errs',
                'pool-preserve-range-errors': 'preserve_range_errs',
                'pool-configured-port-range': 'configured_port_range',
                'pool-preserve-range-enabled': 'preserve_range_enabled',
                'pool-app-port-errors': 'app_errs',
                'pool-app-exceed-port-limit-errors': 'app_xcd_port_lmt_errs',
                'port-block-type': 'blk_type',
                'port-blocks-limit-exceeded-errors': 'port_blk_limit_exceed_errs',
                'detnat-subscriber-exceeded-port-limits': 'detnat_subs_exceed_port_limits',
                'pool-users': 'pool_users',
                'pool-mem-alloc-errors': 'pool_mem_alloc_err',
                'eif-inbound-session-count': 'eif_in_sess_cnt',
                'eif-inbound-session-limit-exceed-drop': 'eif_in_sess_lmt_xcd_drop',
            })

        self.log('INFO', "NAT pool detail: {}".format(self.data['nat_pool']))

        return self.fn_checkout(True)

    def verify_nat_pool_detail(self, name=None, **kwargs):
        """Verify NAT pool detail

        :param string name:
            **OPTIONAL** Name of NAT pool. If name is passed, details for that NAT Pool
            are verified, else details for all pools configured (saved in object)
            will be verified. Default is None

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.verify_nat_pool_detail(name='nat_pool1')
                hCgn.verify_nat_pool_detail()
            Robot:
                hCgn.Verify NAT Pool Detail   name=nat_pool1
                hCgn.Verify NAT Pool Detail
        """

        self.fn_checkin("Verifying NAT pool detail")

        self.get_nat_pool_detail(name)

        self._get_tg_port_and_config_mapping(**kwargs)
        self._get_ss_from_pool()

        result = True
        pool_names = [name] if name is not None else self.data['nat_pool'].keys()

        self.log('INFO', "Verifying details for pools: {}".format(pool_names))
        for pool_name in pool_names:
            # for tg_if in self.tg_cfg_map:
            #_cfg_map = self.tg_cfg_map[tg_if]
            self.log('INFO', "Verifying details for pool, {}".format(pool_name))

            #pool_data = self.data['nat_pool'][_cfg_map['nat_pool']]
            pool_data = self.data['nat_pool'][pool_name]
            #_pool_sess_cnt = self.tg_sess_cnt['nat_pool'][pool_name]['tot_sess']
            #sset = self.pool_map[pool_name]['sset']
            #spic = self.pool_map[pool_name]['spic']
            _pool_sess_cnt = self.pool_map[pool_name]['total_sess']
            if re.search(r'twice.napt', pool_data['trans_type'], re.IGNORECASE):
                exp_data = {}
            elif re.search(r'deterministic.napt', pool_data['trans_type'], re.IGNORECASE):
                exp_data = {
                    'out_of_port_errs': 0,
                    #'ports_in_use': self.pool_map[pool_name]['tot_sess'],
                    'ports_in_use': _pool_sess_cnt, 'max_ports_in_use': _pool_sess_cnt,
                    'parity_port_errs': 0, 'preserve_range_errs': 0, 'app_errs': 0,
                    'app_xcd_port_lmt_errs': 0, 'detnat_subs_xcd_port_lmts': 0,
                    'eif_in_sess_lmt_xcd_drop': 0, 'port_blk_alloc_errs': 0,
                    'pool_mem_alloc_err': 0, 'out_of_port_errs': 0,
                }
            elif re.search(r'napt|nat64', pool_data['trans_type'], re.IGNORECASE):
                exp_data = {'out_of_port_errs': 0,
                            #'ports_in_use': self.pool_map[pool_name]['tot_sess'],
                            'ports_in_use': _pool_sess_cnt, 'max_ports_in_use': _pool_sess_cnt}
            elif re.search(r'dynamic', pool_data['trans_type'], re.IGNORECASE):
                exp_data = {'out_of_addr_errs': 0, 'addrs_in_use': _pool_sess_cnt}

            if 'addr' in self.nat_pool[pool_name]:
                pool_addr = self.nat_pool[pool_name]['addr']
                addr_range = iputils.get_network_ip_range(pool_addr)
                exp_data['addr_range_low'], exp_data['addr_range_high'] = addr_range.split('-')

            if pool_name in self.pool_map:
                exp_data['spic'] = self.pool_map[pool_name]['spic']
                exp_data['sset'] = self.pool_map[pool_name]['sset']

            for key in kwargs:
                if 'tg_sess' in key:
                    continue
                exp_data[key] = kwargs[key]

            self.log('INFO', "Verifying expected({}) and actual({}) data".format(exp_data,
                                                                                 pool_data))
            #result &= utils.cmp_dicts(exp_data, pool_data)
            if utils.cmp_dicts(exp_data, pool_data):
                self.log('INFO', "Verification details for pool, {}, PASSED".format(pool_name))
            else:
                self.log('INFO', "Verification for pool, {}, FAILED".format(pool_name))
                result = False

        return self.fn_checkout(result)

    def get_nat_eim_mappings(self, **kwargs):
        """Return NAT EIM mappings as dictionary

        NAT eim mappings output is parsed and dictionary is returned.
        An exception will be raised if there's no output.

        :param string private_ip:
            **OPTIONAL** Private IP to be used for filtering the mappings output

        :param string public_ip:
            **OPTIONAL** Public IP to be used for filtering the mappings output

        :return: Dictionary containing the NAT EIM mappings data

        :rtype: dict

        Example::

            Python:
                hCgn.get_nat_eim_mappings()
            Robot:
                hCgn.Get NAT EIM Mappings
        """

        self.fn_checkin("Retrieving NAT EIM mappings")

        cmd = 'show services nat mappings endpoint-independent'
        if 'private_ip' in kwargs and kwargs['private_ip'] is not None:
            cmd += ' private {}'.format(kwargs['private_ip'])
        if 'public_ip' in kwargs and kwargs['public_ip'] is not None:
            cmd += ' public {}'.format(kwargs['public_ip'])

        output = self.dh.cli(command=cmd).response()
        if len(output.splitlines()) < 2:
            self.fn_checkout(False, err_msg="No valid output found")

        mapping = {}

        (pcp_ip, b4_ip) = (None, None)
        (spic, sset, nat_pool, int_ip, int_port) = (None, None, None, None, None)

        self.data['eim_maps'] = data = self.dd()

        for line in output.splitlines():
            if len(line) <= 0:
                continue

            match = re.search(r'Interface:\s*(.*), Service set:\s*(.*)', line, re.IGNORECASE)
            if match:
                # Do we have any data to be stored? Store it first
                if 'nat_ip' in mapping and mapping['nat_ip'] is not None:
                    # Do we have PCP Mapping, then PCP IP is also a key
                    if pcp_ip is not None:
                        _map_ptr = data[spic][sset][nat_pool][pcp_ip][int_ip][int_port] = {}
                    elif b4_ip is not None:
                        _map_ptr = data[spic][sset][nat_pool][b4_ip][int_ip][int_port] = {}
                    else:
                        _map_ptr = data[spic][sset][nat_pool][int_ip][int_port] = {}
                    for key in mapping:
                        _map_ptr[key] = mapping[key]
                    mapping = {}
                    pcp_ip = b4_ip = None

                spic, sset = match.group(1), match.group(2)
                self.log('INFO', 'Service pics:{} Service set:{}'.format(spic, sset))
                continue

            match = re.search(r'NAT pool:\s*(.*)', line, re.IGNORECASE)
            if match:
                nat_pool = match.group(1)
                continue

            match = re.search(r'PCP Client\s*:\s*(' + utils.get_regex_ip() +
                              r')\s*PCP lifetime\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                # Do we have any data to be stored (Non-PCP output)
                if 'nat_ip' in mapping and mapping['nat_ip'] is not None:
                    if pcp_ip is not None:  # Do we have PCP Mapping, then PCP IP is also a key
                        _map_ptr = data[spic][sset][nat_pool][pcp_ip][int_ip][int_port] = {}
                    else:
                        _map_ptr = data[spic][sset][nat_pool][int_ip][int_port] = {}
                    for key in mapping:
                        _map_ptr[key] = mapping[key]
                    mapping = {}
                    pcp_ip = None
                pcp_ip = match.group(1)
                if iputils.is_ip_ipv6(pcp_ip):
                    pcp_ip = iputils.normalize_ipv6(pcp_ip)
                mapping['pcp_lifetime'] = match.group(1)
                continue

            match = re.search(r'Mapping\s*:\s*(' + utils.get_regex_ip() +
                              r')\s*:\s*(\d+)\s*-->\s*(' + utils.get_regex_ip() +
                              r')\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                # Do we have any data to be stored(Non-PCP output)? Store it
                # first
                if 'nat_ip' in mapping and mapping['nat_ip'] is not None:
                    # Do we have SW flow, then B4 IP is also a key
                    if b4_ip is not None:
                        _map_str = data[spic][sset][nat_pool][b4_ip][int_ip][int_port] = {}
                    else:
                        _map_str = data[spic][sset][nat_pool][int_ip][int_port] = {}
                    for key in mapping:
                        _map_str[key] = mapping[key]
                    mapping = {}
                    b4_ip = None
                int_ip, int_port = match.group(1), match.group(2)
                if iputils.is_ip_ipv6(int_ip):
                    int_ip = iputils.normalize_ipv6(int_ip)
                mapping['nat_ip'] = match.group(3)
                mapping['nat_port'] = match.group(4)
                continue

            match = re.search(r'Session Count\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                mapping['sess_cnt'] = match.group(1)
                continue

            match = re.search(r'Mapping State\s*:\s+((\w+)\s+\((\d+)s\)|(\w+))', line,
                              re.IGNORECASE)
            if match:
                if match.group(3) is not None:
                    mapping['state'] = match.group(2).lower()
                    mapping['state_to'] = match.group(3)
                else:
                    mapping['state'] = match.group(1).lower()

            match = re.search(r'B4 Address\s+:\s+(' + utils.get_regex_ip() + ')', line,
                              re.IGNORECASE)
            if match:
                mapping['b4_ip'] = b4_ip = iputils.normalize_ipv6(match.group(1))
                continue

        if pcp_ip is not None:
            _map_str = data[spic][sset][nat_pool][pcp_ip][int_ip][int_port] = {}
        elif b4_ip is not None:
            _map_str = data[spic][sset][nat_pool][b4_ip][int_ip][int_port] = {}
        else:
            _map_str = data[spic][sset][nat_pool][int_ip][int_port] = {}
        for key in mapping:
            _map_str[key] = mapping[key]

        self.log('INFO', 'NAT EIM mappings dump : {}'.format(data))

        self.fn_checkout()

        return data

    def verify_nat_eim_mappings(self, **kwargs):
        """Verify NAT EIM mappings

        Fetches NAT EIM data from the output by calling get_nat_eim_mappings.
        This data is verified against the data fetched from configuration and traffic generator.
        Number of mappings to be verified can be limited by 'limit' or 'limit_perc'.
        Random mappings, to be verified, are picked from sessions to be sent by TG.

        :param int limit:
            **OPTIONAL** Number of mappings to be verified.

        :param int limit_perc:
            **OPTIONAL** Percentage number of mappings to be verified. Default is 1

        :return: True on successful verification else raises an exception

        :rtype: True or exception

        Example::

            Python:
                hCgn.verify_nat_eim_mappings()
            Robot:
                hCgn.Verify NAT EIM Mappings
        """

        self.fn_checkin("Verifying NAT mappings EIM")

        result = True

        # Fetch NAT EIM output as dictionary
        act_data = self.get_nat_eim_mappings()

        self._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            # Iterate over list of random mappings indices
            for sess_idx in _cfg_map['rand_sess_idx_list']:
                # We need to verify if theres a mapping for this session on router

                src_ip = self.tg_sess[tg_if]['sess_list'][sess_idx]['src_ip']
                src_port = str(self.tg_sess[tg_if]['sess_list'][sess_idx]['src_port'])

                flow = self._get_src_ip_port_flow_from_data(src_ip, src_port, _cfg_map, act_data)
                if flow is None:
                    continue

                if 'nat_ip' in flow and flow['nat_ip'] is None:
                    continue

                result &= self._is_nat_ip_in_pool(flow, _cfg_map)
                result &= self._is_nat_port_in_pool(flow, _cfg_map)

                result &= utils.cmp_dicts(exp_data={'state': 'active'}, act_data=flow)

        return self.fn_checkout(result)

    def get_nat_app_mappings(self, **kwargs):
        """Return NAT APP mappings as dictionary

        :param string private_ip:
            **OPTIONAL** Private IP to be used for filtering the mappings output

        :param string public_ip:
            **OPTIONAL** Public IP to be used for filtering the mappings output

        :return: Dictionary containing the NAT APP mappings data

        :rtype: dict

        Example::

            Python:
                hCgn.get_nat_app_mappings()
            Robot:
                hCgn.Get NAT APP Mappings
        """

        self.fn_checkin("Retrieving NAT APP mappings")

        cmd = 'show services nat mappings address-pooling-paired'
        if 'private_ip' in kwargs and kwargs['private_ip'] is not None:
            cmd += ' private {}'.format(kwargs['private_ip'])
        if 'public_ip' in kwargs and kwargs['public_ip'] is not None:
            cmd += ' public {}'.format(kwargs['public_ip'])

        output = self.dh.cli(command=cmd).response()
        if len(output.splitlines()) < 2:
            return self.fn_checkout(False, "No valid output found")

        mapping = {}

        (spic, sset, nat_pool, int_ip, b4_ip) = (None, None, None, None, None)

        self.data['app_maps'] = data = self.dd()

        for line in output.splitlines():
            if len(line) <= 0:
                continue

            match = re.search(r'Interface:\s*(.*), Service set:\s*(.*)', line, re.IGNORECASE)
            if match:
                if 'nat_ip' in mapping and mapping['nat_ip'] is not None:
                    # Do we have SW flow, then B4 IP is also a key
                    if b4_ip is not None:
                        _map_ptr = data[spic][sset][nat_pool][b4_ip][int_ip] = {}
                    else:
                        _map_ptr = data[spic][sset][nat_pool][int_ip] = {}
                    for key in mapping:
                        _map_ptr[key] = mapping[key]
                    mapping = {}
                    b4_ip = None
                spic, sset = match.group(1), match.group(2)
                continue

            match = re.search(r'NAT pool:\s*(.*)', line, re.IGNORECASE)
            if match:
                if 'nat_ip' in mapping and mapping['nat_ip'] is not None:
                    # Do we have SW flow, then B4 IP is also a key
                    if b4_ip is not None:
                        _map_ptr = data[spic][sset][nat_pool][b4_ip][int_ip] = {}
                    else:
                        _map_ptr = data[spic][sset][nat_pool][int_ip] = {}
                    for key in mapping:
                        _map_ptr[key] = mapping[key]
                    mapping = {}
                    b4_ip = None

                nat_pool = match.group(1)
                continue

            match = re.search(r'Mapping\s*:\s*(' + utils.get_regex_ip() + r')\s*-->\s*(' +
                              utils.get_regex_ip() + r')\s*', line, re.IGNORECASE)
            if match:
                if 'nat_ip' in mapping and mapping['nat_ip'] is not None:
                    # Do we have SW flow, then B4 IP is also a key
                    if b4_ip is not None:
                        _map_ptr = data[spic][sset][nat_pool][b4_ip][int_ip] = {}
                    else:
                        _map_ptr = data[spic][sset][nat_pool][int_ip] = {}
                    for key in mapping:
                        _map_ptr[key] = mapping[key]
                    mapping = {}
                    b4_ip = None
                int_ip = iputils.normalize_ipv6(match.group(1)) \
                    if iputils.is_ip_ipv6(match.group(1)) else match.group(1)
                mapping['nat_ip'] = match.group(2)
                continue

            match = re.search(r'Ports In Use\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                mapping['ports_in_use'] = match.group(1)
                continue

            match = re.search(r'Session Count\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                mapping['sess_cnt'] = match.group(1)
                continue

            match = re.search(r'Mapping State\s*:\s+((\w+)\s+\((\d+)s\)|(\w+))', line,
                              re.IGNORECASE)
            if match:
                if match.group(3) is not None:
                    mapping['state'] = match.group(2).lower()
                    mapping['state_to'] = match.group(3)
                else:
                    mapping['state'] = match.group(1).lower()
                continue

            match = re.search(r'B4 Address\s+:\s+(' + utils.get_regex_ip() + r')', line,
                              re.IGNORECASE)
            if match:
                mapping['b4_ip'] = b4_ip = iputils.normalize_ipv6(match.group(1))
            continue

        if spic is not None:
            if b4_ip is not None:
                _map_ptr = data[spic][sset][nat_pool][b4_ip][int_ip] = {}
            else:
                _map_ptr = data[spic][sset][nat_pool][int_ip] = {}
        for key in mapping:
            _map_ptr[key] = mapping[key]

        self.log('INFO', "NAT APP mappings dump : {}".format(data))

        self.fn_checkout()

        return data

    def verify_nat_app_mappings(self, **kwargs):
        """Verify NAT APP mappings

        Fetches NAT APP data from the output by calling get_nat_app_mappings.
        This data is verified against the data fetched from configuration and traffic generator.
        Number of mappings to be verified can be limited by 'limit' or 'limit_perc'.
        Random mappings, to be verified, are picked from sessions to be sent by TG.

        :param int limit:
            **OPTIONAL** Number of mappings to be verified.

        :param int limit_perc:
            **OPTIONAL** Percentage number of mappings to be verified. Default is 1

        :return: True on successful verification else raises an exception

        :rtype: True or exception

        Example::

            Python:
                hCgn.verify_nat_app_mappings()
            Robot:
                hCgn.Verify NAT APP Mappings
        """

        self.fn_checkin("Verifying NAT APP mappings")

        result = True

        # Fetch NAT APP output as dictionary
        act_data = self.get_nat_app_mappings()

        self._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            # Iterate over list of random mappings indices
            for sess_idx in _cfg_map['rand_sess_idx_list']:
                # We need to verify if theres a mapping for this session on the
                # router
                src_ip = self.tg_sess[tg_if]['sess_list'][sess_idx]['src_ip']

                flow = self._get_src_ip_flow_from_data(src_ip, _cfg_map, act_data)

                if flow is None:
                    continue
                exp_app_data = {'state': 'active'}
                exp_app_data['ports_in_use'] = exp_app_data['sess_cnt'] = _cfg_map['tot_sess']
                result &= utils.cmp_dicts(exp_data=exp_app_data, act_data=flow)

                result &= self._is_nat_ip_in_pool(flow, _cfg_map)

        return self.fn_checkout(result)

    # def get_nat_mappings_detail(self, **kwargs):
    def get_nat_mappings_detail(self, pool_name=None):
        """Return NAT mappings detail as dictionary

        :param string pool_name:
            **OPTIONAL** NAT Pool name to be used for filtering the output

        :return: Dictionary containing the NAT mappings detail data

        :rtype: dict

        Example::

            Python:
                hCgn.get_nat_mappings_detail()
            Robot:
                hCgn.Get NAT Mappings Detail
        """

        self.fn_checkin("Retrieving NAT mappings detail")

        cmd = 'show services nat mappings detail'
        if pool_name is not None:
            cmd += ' {}'.format(pool_name)

        output = self.dh.cli(command=cmd).response().splitlines()

        if len(output) < 2:
            return self.fn_checkout(False, "No valid output found")

        data = self.dd()
        count = -1

        for line in output:
            count += 1
            if len(line) <= 0:
                continue
            match = re.search(r'Interface:\s*(.*), Service set:\s*(\w+)', line, re.IGNORECASE)
            if match:
                spic, sset = match.group(1), match.group(2)
                continue
            match = re.search(r'NAT pool:\s*(\w+)', line, re.IGNORECASE)
            if match:
                nat_pool = match.group(1)
                continue
            match = re.search(r'Mapping\s*:\s*(' + utils.get_regex_ip() +
                              r')\s*:\s*(\d+)\s*-->\s*(' + utils.get_regex_ip() +
                              r')\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                int_ip = iputils.normalize_ipv6(match.group(1)) \
                    if iputils.is_ip_ipv6(match.group(1)) else match.group(1)
                int_port = match.group(2)
                data[spic][sset][nat_pool][int_ip][int_port]['eim_nat_ip'] = match.group(3)
                data[spic][sset][nat_pool][int_ip][int_port]['eim_nat_port'] = match.group(4)
                match = re.search(r'Session Count\s*:\s*(\d+)', output[count + 1], re.IGNORECASE)
                if match:
                    data[spic][sset][nat_pool][int_ip][int_port]['eim_sess_cnt'] = match.group(1)
                match = re.search(r'Mapping State\s*:\s+((\w+)\s+\((\d+)s\)|(\w+)\s*)',
                                  output[count + 2], re.IGNORECASE)
                if match:
                    if match.group(3) is not None:
                        data[spic][sset][nat_pool][int_ip][int_port]['eim_state'] = \
                            match.group(2).lower()
                        data[spic][sset][nat_pool][int_ip][int_port]['eim_state_to'] = \
                            match.group(3)
                    else:
                        data[spic][sset][nat_pool][int_ip][int_port]['eim_state'] = \
                            match.group(1).lower()

            match = re.search(r'Ports In Use\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                data[spic][sset][nat_pool][int_ip]['app_ports_in_use'] = match.group(1)
                continue
            match = re.search(r'Session Count\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                data[spic][sset][nat_pool][int_ip]['app_sess_cnt'] = match.group(1)
                continue
            match = re.search(r'Mapping State\s*:\s+((\w+)\s+\((\d+)s\)|(\w+)\s*)', line,
                              re.IGNORECASE)
            if match:
                if match.group(3) is not None:
                    data[spic][sset][nat_pool][int_ip]['app_state'] = match.group(2).lower()
                    data[spic][sset][nat_pool][int_ip]['app_state_to'] = match.group(3)
                else:
                    data[spic][sset][nat_pool][int_ip]['app_state'] = match.group(1).lower()
                continue

        self.log('INFO', "NAT mappings detail data dump: {}".format(data))

        self.fn_checkout()

        return data

    def verify_nat_mappings_detail(self, **kwargs):
        """Verify NAT Mappings detail

        Fetches NAT mappings data from the output by calling get_nat_mappings_detail
        This data is verified against the data fetched from configuration and traffic generator.
        Number of mappings to be verified can be limited by 'limit' or 'limit_perc'.
        Random mappings, to be verified, are picked from sessions to be sent by TG.

        :param int limit:
            **OPTIONAL** Number of mappings to be verified.

        :param int limit_perc:
            **OPTIONAL** Percentage number of mappings to be verified. Default is 1

        :return: True on successful verification else raises an exception

        :rtype: True or exception

        Example::

            Python:
                hCgn.verify_nat_mappings_detail()
            Robot:
                hCgn.Verify Mappings Detail
        """

        self.fn_checkin("Verifying NAT mappings detail")

        result = True

        # Fetch Mappings details
        act_data = self.get_nat_mappings_detail()

        self._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            for sess_idx in _cfg_map['rand_sess_idx_list']:
                # We need to verify if theres a mapping for this session on the
                # router
                src_ip = self.tg_sess[tg_if]['sess_list'][sess_idx]['src_ip']
                src_port = str(self.tg_sess[tg_if]['sess_list'][sess_idx]['src_port'])

                # Verify APP
                flow = self._get_src_ip_flow_from_data(src_ip, _cfg_map, act_data)
                exp_app_data = {'app_state': 'active'}
                exp_app_data['app_ports_in_use'] = _cfg_map['tot_sess']
                exp_app_data['app_sess_cnt'] = _cfg_map['tot_sess']

                result &= utils.cmp_dicts(exp_data=exp_app_data, act_data=flow)

                flow = self._get_src_ip_port_flow_from_data(src_ip, src_port, _cfg_map, act_data)

                if flow is None:
                    continue

                # Verify EIM
                act_eim_data = {}
                for key in flow:
                    if 'eim_' in key:
                        act_eim_data[key] = flow[key]
                result &= self._is_nat_ip_in_pool(flow, _cfg_map)
                if 'nat_port' in _cfg_map:
                    result &= self._is_nat_port_in_pool(flow, _cfg_map)

        return self.fn_checkout(result)

    def get_nat_mappings_summary(self):
        """Return NAT mappings summary data as dictionary

        This will parse the mappings summary output and builds a dictionary.

        :return: dictionary on successful parsing or raises an excepion if theres no output

        :rtype: dict or exception

        Example::

            Python:
                hCgn.get_nat_mappings_summary()
            Robot:
                hCgn.Get NAT Mappings Summary
        """

        self.fn_checkin("Retrieving NAT mappings summary")

        output = self.dh.cli(command='show services nat mappings summary').response().splitlines()

        data = self.dd()
        spic = None

        for line in output:
            match = re.search(r'Service Interface:\s*(\w*.\w*\/\w*\/\w*)\s*', line)
            if match:
                spic = match.group(1)
            else:
                match = re.search(r'Service Interface:\s*(\w*)\s*', line)
                if match:
                    spic = match.group(1)
            match = re.search(r'Total number of address mappings:\s*(\d+)', line)
            if match:
                data[spic]['addr_map'] = int(match.group(1))
            match = re.search(r'Total number of endpoint independent port mappings:\s*(\d+)', line)
            if match:
                data[spic]['eim_map'] = int(match.group(1))
            match = re.search(r'Total number of endpoint independent filters:\s*(\d+)', line)
            if match:
                data[spic]['eif_map'] = int(match.group(1))

        self.log('DEBUG', 'NAT mappings summary : {}'.format(data))

        self.fn_checkout()

        return data

    def verify_nat_mappings_summary(self, **kwargs):
        """Verify NAT mappings summary

        This will call get_nat_mappings_summary for fetching the mappings summary output.
        This data will be verified against the data from TG Sessions and configuration
        data that is already saved in the object.

        :return: Dictionary containing the NAT mappings summary data

        :rtype: dict

        Example::

            Python:
                hCgn.verify_nat_mappings_summary()
            Robot:
                hCgn.Verify Mappings Summary
        """

        self.fn_checkin("Verifying NAT mappings summary")

        act_data = self.get_nat_mappings_summary()

        result = True

        self._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            rule_cfg = self.nat_rule[_cfg_map['nat_rule']]
            trans_type = rule_cfg['trans_type']
            exp_data = {}

            if trans_type.startswith('dnat'):
                exp_data['addr_map'] = len(self.tg_sess[tg_if]['dst_ips_list'])
            else:
                exp_data['addr_map'] = len(self.tg_sess[tg_if]['src_ips_list'])

            if 'trans_eim' in rule_cfg and rule_cfg['trans_eim'] is not None:
                exp_data['eim_map'] = _cfg_map['tot_sess']
            if 'trans_eif' in rule_cfg and rule_cfg['trans_eif'] is not None:
                exp_data['eif_map'] = _cfg_map['tot_sess']

            result &= utils.cmp_dicts(exp_data=exp_data, act_data=act_data)

        return self.fn_checkout(result)

    def get_nat_statistics(self, spic=None, timeout=300):
        """Fetch NAT statistics as dictionary

        :param string spic:
            **REQUIRED** Service PIC interface

        :param int timeout:
            **OPTIONAL** Cli command timeout. Default is 300

        :return: Dictionary containing the NAT statistics data

        :rtype: dict

        Example::

            Python:
                hCgn.get_nat_statistics()
            Robot:
                hCgn.Get NAT Statistics
        """

        self.fn_checkin("Retrieving NAT statistics")

        if spic is None:
            raise MissingMandatoryArgument('spic')

        cmd = 'show services nat statistics interface ' + spic

        entry = self.get_xml_output(cmd=cmd, xpath='service-nat-statistics-information',
                                    want_list=False, timeout=timeout)

        data = self.dd()
        data['spic'] = entry.pop('interface-name', None)

        for key in entry:
            if 'query-unsupported-msg' in key:
                continue
            tmp_key = key
            tmp_key = tmp_key.replace('-', '_')
            data[tmp_key] = entry[key]

        self.log('DEBUG', 'NAT statistics: {}'.format(data))

        self.fn_checkout()

        return data

    def verify_nat_statistics(self, **kwargs):
        """Verify NAT statistics

        :return: Dictionary containing the NAT statistics data

        :rtype: dict

        Example::

            Python:
                hCgn.verify_nat_statistics()
            Robot:
                hCgn.Verify NAT Statistics
        """

        self.fn_checkin("Verifying NAT statistics")

        result = True

        self._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            act_data = self.get_nat_statistics(_cfg_map['spic'], **kwargs)
            exp_data = {}
            exp_data['nat_total_pkts_translated'] = self.tg_sess[tg_if]['total']
            exp_data['nat_map_allocation_successes'] = self.tg_sess[tg_if]['total']

            result &= utils.cmp_dicts(exp_data=exp_data, act_data=act_data)

        return self.fn_checkout(result)

    def get_sessions_extensive(self, **kwargs):
        """Fetch session extensive as dictionary

        :return: Dictionary containing the session extensive data

        :rtype: dict

        Example::

            Python:
                hCgn.get_sessions_extensive()
            Robot:
                hCgn.Get Sessions Extensive
        """

        self.fn_checkin("Retrieving session extensive")

        is_nat = None

        cmd = 'show services sessions extensive'
        if 'ss' in kwargs:
            cmd += ' service-set {}'.format(kwargs['ss'])
        if 'sp' in kwargs:
            cmd += ' interface {}'.format(kwargs['sp'])
        if 'app_proto' in kwargs:
            cmd += ' application-protocol {}'.format(kwargs['app_proto'])
        if 'src_pfx' in kwargs:
            cmd += ' source-prefix {}'.format(kwargs['src_pfx'])
        if 'dst_pfx' in kwargs:
            cmd += ' destination-prefix {}'.format(kwargs['dst_pfx'])
        if 'src_port' in kwargs:
            cmd += ' source-port {}'.format(kwargs['src_port'])
        if 'limit' in kwargs:
            cmd += ' limit {}'.format(kwargs['limit'])

        output = self.dh.cli(command=cmd).response()
        # data = {}
        self.data['sess_xtnsv'] = {}
        # conv = {}
        for line in output.splitlines():
            match = re.search(r'(^.*-\d+\/\d+\/\d+)', line)
            if match:
                spic = match.group(1)
                if spic not in self.data['sess_xtnsv']:
                    self.data['sess_xtnsv'][spic] = {}
                continue

            match = re.search(
                r'Service Set:\s*(.*),\s*Session:\s*(\d+),\s*ALG:\s*(.*),\s*Flags:\s*(.*),\s*'
                r'IP Action:\s*(.*),\s*Offload:\s*(.*),\s*Asymmetric:\s*(.*)', line, re.IGNORECASE)
            if match:
                (sset, sess_id, alg, flags, action, offload, assym) = match.groups()
                if sset not in self.data['sess_xtnsv'][spic]:
                    self.data['sess_xtnsv'][spic][sset] = {}
                try:
                    src_ip
                except NameError:
                    src_ip = src_port = None
                # if src_ip:
                    # src_ip = src_port = None
                is_nat = False
                continue
            match = re.search(r'NAT Action:\s*Translation Type\s*-\s*(.*)', line)
            if match:
                is_nat = True
                trans_type = match.group(1)
                continue
            match = re.search(r'^\s*NAT (\w+)\s+(' + utils.get_regex_ip()
                              + r'):(\d+)\s*->\s*(' +
                              utils.get_regex_ip()
                              + r'):\s*(\d+)', line, re.IGNORECASE)
            if match:
                nat_type = match.group(1)
                (src_ip, src_port, nat_ip, nat_port) = match.groups()[1:]
                if src_ip not in self.data['sess_xtnsv'][spic][sset]:
                    self.data['sess_xtnsv'][spic][sset][src_ip] = {}
                if src_port not in self.data['sess_xtnsv'][spic][sset][src_ip]:
                    self.data['sess_xtnsv'][spic][sset][src_ip][src_port] = {}
                if re.search(r'destination', nat_type, re.IGNORECASE) and \
                                                re.search(r'nat64', trans_type, re.IGNORECASE):
                    # Ignore the destination flow for NAT64
                    continue

                self.data['sess_xtnsv'][spic][sset][src_ip][src_port]['nat_ip'] = nat_ip
                self.data['sess_xtnsv'][spic][sset][src_ip][src_port]['nat_port'] = nat_port
                conv = self.data['sess_xtnsv'][spic][sset][src_ip][src_port]
                conv['trans_type'] = trans_type.lower()
                conv['nat_type'] = nat_type.lower()
                conv['sess_id'] = sess_id
                conv['alg'] = alg
                conv['flags'] = flags
                conv['ip_action'] = action
                conv['offload'] = offload
                conv['assym'] = assym
                continue
            match = re.search(r'^\s*NAT (\w+)\s+(' + utils.get_regex_ip() +
                              r')\s*->\s*(' + utils.get_regex_ip() + ')', line, re.IGNORECASE)
            if match:
                nat_type = match.group(1)
                (src_ip, nat_ip) = match.groups()[1:]
                if src_ip not in self.data['sess_xtnsv'][spic][sset]:
                    self.data['sess_xtnsv'][spic][sset][src_ip] = {}

                if re.search(r'destination', nat_type, re.IGNORECASE) and \
                   re.search(r'nat64', trans_type, re.IGNORECASE):
                    # Ignore the destination flow for NAT64
                    continue

                self.data['sess_xtnsv'][spic][sset][src_ip]['nat_ip'] = nat_ip
                conv = self.data['sess_xtnsv'][spic][sset][src_ip]
                trans_type = re.sub(r'\s', '-', trans_type).lower()
                conv['trans_type'] = trans_type.lower()
                conv['nat_type'] = nat_type.lower()
                conv['sess_id'] = sess_id
                conv['alg'] = alg
                conv['flags'] = flags
                conv['ip_action'] = action
                conv['offload'] = offload
                conv['assym'] = assym
                continue
            match = re.search(r'(\w+)\s+(' + utils.get_regex_ip() + r'):(\d+)\s*->\s*(' +
                              utils.get_regex_ip() +
                              r'):(\d+)\s* (\w+) \s*([I|O])\s*(\d+)', line, re.IGNORECASE)
            if match:
                flow_type = 'iflow' if match.group(7) == 'I' else 'rflow'
                if not is_nat:
                    if not src_ip:
                        (src_ip, src_port) = match.groups()[2:4]
                    # Non-NAT (SFW)
                    if src_ip not in self.data['sess_xtnsv'][spic][sset]:
                        self.data['sess_xtnsv'][spic][sset][src_ip] = {}
                    if src_port not in self.data['sess_xtnsv'][spic][sset][src_ip]:
                        self.data['sess_xtnsv'][spic][sset][src_ip][src_port] = {}
                    self.data['sess_xtnsv'][spic][sset][src_ip][src_port][
                        flow_type + '_proto'] = match.group(1).lower()
                    conv = self.data['sess_xtnsv'][spic][sset][src_ip][src_port]
                    conv['sess_id'] = sess_id
                    conv['alg'] = alg
                    conv['flags'] = flags
                    conv['ip_action'] = action
                    conv['offload'] = offload
                    conv['assym'] = assym
                conv[flow_type + '_proto'] = match.group(1).lower()
                conv[flow_type + '_src_ip'] = match.group(2)
                conv[flow_type + '_src_port'] = match.group(3)
                conv[flow_type + '_dst_ip'] = match.group(4)
                conv[flow_type + '_dst_port'] = match.group(5)
                conv[flow_type + '_state'] = match.group(6)
                conv[flow_type + '_dir'] = match.group(7)
                conv[flow_type + '_frm_cnt'] = match.group(8)
                continue
            match = re.search(r'(\w+)\s+(' + utils.get_regex_ip() + r')\s*->\s*(' +
                              utils.get_regex_ip() +
                              r')\s* (\w+) \s*([I|O])\s*(\d+)', line, re.IGNORECASE)
            if match:
                flow_type = 'iflow' if match.group(5) == 'I' else 'rflow'
                if not is_nat:
                    if not src_ip:
                        src_ip = match.groups()[2]
                    # # Non-NAT (SFW)
                    if src_ip not in self.data['sess_xtnsv'][spic][sset]:
                        self.data['sess_xtnsv'][spic][sset][src_ip] = {}
                    self.data['sess_xtnsv'][spic][sset][src_ip][
                        flow_type + '_proto'] = match.group(1).lower()
                    conv = self.data['sess_xtnsv'][spic][sset][src_ip]
                    conv['sess_id'] = sess_id
                    conv['alg'] = alg
                    conv['flags'] = flags
                    conv['ip_action'] = action
                    conv['offload'] = offload
                    conv['assym'] = assym

                conv[flow_type + '_proto'] = match.group(1).lower()
                conv[flow_type + '_src_ip'] = match.group(2)
                conv[flow_type + '_dst_ip'] = match.group(3)
                conv[flow_type + '_state'] = match.group(4)
                conv[flow_type + '_dir'] = match.group(5)
                conv[flow_type + '_frm_cnt'] = match.group(6)
                continue

            match = re.search(r'Byte count:\s*(\d+)', line, re.IGNORECASE)
            if match:
                conv[flow_type + '_byte_count'] = match.group(1)
                continue
            match = re.search(r'Flow role:\s*(.*),\s*Timeout:\s*(\d+)', line, re.IGNORECASE)

            if match:
                conv[flow_type + '_role'] = match.group(1)
                conv[flow_type + '_timeout'] = match.group(2)
                continue

        self.log('INFO', "session extensive dump:{}".format(self.data['sess_xtnsv']))
        self.fn_checkout()

        return self.data['sess_xtnsv']

    def verify_sessions_extensive(self, **kwargs):
        """Verify sessions extensive

        :return: Dictionary containing the sessions extensive data

        :rtype: dict

        Example::

            Python:
                hCgn.verify_sessions_extensive()
            Robot:
                hCgn.Verify Sessions Extensive
        """

        self.fn_checkin("Verifying session extensive")

        self.get_sessions_extensive(**kwargs)

        self.data = self.data['sess_xtnsv']
        result = True

        self._get_tg_port_and_config_mapping(**kwargs)
        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            for sess_idx in _cfg_map['rand_sess_idx_list']:
                # We need to verify if theres a mapping for this session on the
                # router
                src_ip = self.tg_sess[tg_if]['sess_list'][sess_idx]['src_ip']
                src_port = str(self.tg_sess[tg_if]['sess_list'][sess_idx]['src_port'])
                spic = _cfg_map['spic']
                sset = _cfg_map['sset']

                try:
                    flow = self.data[spic][sset][src_ip][src_port]
                except (TypeError, KeyError):
                    self.log('INFO', "Error while retrieving flow")
                    continue
                if flow is None:
                    self.log('INFO', "Flow is none")
                    continue
                self.log('INFO', "flow is {}".format(flow))
                result &= self._is_nat_ip_in_pool(flow, _cfg_map)
                result &= self._is_nat_port_in_pool(flow, _cfg_map)
                ss_name = _cfg_map['sset']
                if 'sl_class_list' in self.sset[ss_name]:
                    if self.sset[ss_name]['sl_class_list'] is not None:
                        exp_data = {}
                        exp_data['src_ip'] = src_ip
                        exp_data['dst_ip'] = self.tg_sess[tg_if]['sess_list'][sess_idx]['dst_ip']
                        exp_data['proto'] = self.tg_sess[tg_if]['sess_list'][sess_idx][
                            'protocol'].lower()
                        if 'stateful-firewall-logs' in self.sset[ss_name]['sl_class_list']:
                            msg = 'JSERVICES_SFW_RULE_ACCEPT'
                        if 'nat-logs' in self.sset[ss_name]['sl_class_list']:
                            msg = 'JSERVICES_NAT_RULE_MATCH'
                        if 'session-logs' in self.sset[ss_name]['sl_class_list']:

                            exp_data['nat_ip'] = flow['nat_ip']
                            exp_data['nat_port'] = flow['nat_port']
                            msg = 'JSERVICES_SESSION_OPEN'
                        result &= self._verify_syslogs(msg=msg, src_port=src_port, xtnsv=exp_data)

        return self.fn_checkout(result)

    def get_nat_pool_ips(self):
        """Return Pool IPs configured

        :return: list of Pool IPs configured
        :rtype: list

        Example::

            Python:
                hCgn.get_nat_pool_ips()
            Robot:
                hCgn.Get NAT Pool IPs
        """

        self.fn_checkin("Retrieving configured pool ips")

        #pools = self.nat_pool.keys()
        pool_ips = []
        for pool in self.nat_pool:
            pool_ips.append(self.nat_pool[pool]['addr'])

        self.fn_checkout()

        return pool_ips

    def get_detnat_port_block(self, internal_ip=None):
        """Return Deterministic NAT Port Block output as dictionary

        :param string internal_ip:
            **OPTIONAL** Internal IP

        :param string err_lvl:
            **OPTIONAL** Error Level. Default is 'ERROR'

        :returns: Dictionary

        :rtype: dict

        Example::

            Python:
                cgn.get_detnat_port_blocks()
            Robot:
                Get DetNAT Port Blocks
        """

        self.fn_checkin("Retrieving DetNAT Port Blocks output")

        cmd = "show services nat deterministic-nat nat-port-block {}".format(internal_ip)
        _xpath = 'service-detnat-information'
        #_xpath = 'service-detnat-information'
        #dinfo = self.get_xml_output(cmd, xpath=_xpath)
        detnat_output = self.get_xml_output(cmd, xpath=_xpath)

        data = self.data['detnat_port_blk'] = self.dd()
        #int_ip = dinfo['detnat-internal-host']
        #denat_output = dinfo['detnat-internal-host']
        # for entry in detnat_output:
        int_ip = detnat_output['detnat-internal-host']
        if iputils.is_ip_ipv6(int_ip):
            int_ip = iputils.normalize_ipv6(int_ip)
        data[int_ip]['sset'] = detnat_output['service-set-name']
        data[int_ip]['spic'] = detnat_output['interface-name']
        data[int_ip]['nat_pool'] = detnat_output['pool-name']
        data[int_ip]['nat_ip'] = detnat_output['detnat-nat-ip']
        data[int_ip]['nat_port_low'] = detnat_output['detnat-nat-port-low']
        data[int_ip]['nat_port_high'] = detnat_output['detnat-nat-port-high']

        self.log('INFO', "Det NAT info: {}".format(data))

        self.fn_checkout()

        return data

    def verify_detnat_port_block(self, **kwargs):
        """Verify DetNAT Port blocks

        :paran string internal_ip:
            **MANDATORY** Internal IP

        :param string err_lvl:
            **OPTIONAL** Error Level. Default is 'ERROR'

        :returns: True or False

        :rtype: bool

        Example::

            Python:
                cgn.verify_detnat_port_blocks()
            Robot:
                Verify DetNAT Port Blocks
        """

        act_data = self.get_detnat_port_block(**kwargs)
        internal_ip = kwargs.pop('internal_ip')
        # Compare the expected values against the actual values
        return utils.cmp_dicts(exp_data=kwargs, act_data=act_data[internal_ip])


    ################################################################
    # local methods
    ################################################################
    def _get_syslogs(self, ptrn, **kwargs):
        """Parse NAT/SFW related logs from 'show log messages' and return as dictionary """

        self.fn_checkin("Retrieving NAT log messages")

        if 'src_ip' in kwargs and kwargs['src_ip'] is not None:
            ptrn += " | match " + str(kwargs['src_ip'])
        if 'src_port' in kwargs and kwargs['src_port'] is not None:
            ptrn += ":" + str(kwargs['src_port'])
        cmd = 'show log messages | match ' + ptrn
        data = self.dd()

        output = self.dh.cli(command=cmd).response()

        pr_ptrn1 = re.compile(r'proto (\d+)\s*\((.+)\)')
        pr_ptrn = re.compile(r'proto (\d+)\s*\((\w+)\)')
        ip_ptrn = re.compile(r'('+utils.get_regex_ip() +
                             r')[:|\/](\d+)\s*->\s*('+utils.get_regex_ip()+r')[:|\/](\d+)')
        ptrn2 = re.compile(r'('+utils.get_regex_ip()+r'):(\d+)')
        ptrn3 = re.compile(r'(MSVCS_LOG_.*|JSERVICES]_LOG_.*)')

        regex_ipaddr = utils.get_regex_ip()
        pr_ptrn1 = r'proto (\d+)\s*\((.+)\)'
        pr_ptrn = r'proto (\d+)\s*\((\w+)\)'
        ip_ptrn = r'('+regex_ipaddr + r')[:|\/](\d+)\s*->\s*('+regex_ipaddr+r')[:|\/](\d+)'
        ptrn2 = r'('+regex_ipaddr+r'):(\d+)'
        ptrn3 = r'(MSVCS_LOG_.*|JSERVICES]_LOG_.*)'
        reg_ex_if = utils.get_regex_if()

        for line in output.splitlines():

            # ALG64 Control session
            match = re.search(r'' + ptrn3 + r':\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s+->\s+' + ptrn2 +
                              r'\s*\[('+regex_ipaddr+r')\]\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['nat_port'] = match.group(7)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['srvr_ip'] = match.group(10)
                ptr['proto'] = match.group(11).lower()

            # ALG64 Data session
            match = re.search(r'' + ptrn3 + r':\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*\[('+regex_ipaddr+r')\]\s+->\s+' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]

                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                # Nat port is same as the source port
                ptr['nat_port'] = match.group(5)
                ptr['dst_ip'] = match.group(7)
                ptr['dst_port'] = match.group(8)
                ptr['srvr_ip'] = match.group(9)
                ptr['srvr_port'] = match.group(1)
                ptr['proto'] = match.group(11).lower()

            # new message
            match = re.search(r'' + ptrn3 + r':\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s+->\s+' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['nat_port'] = match.group(7)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['proto'] = match.group(10).lower()

            # Basic NAT
            match = re.search(r'' + ptrn3 + r':\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*\[('+regex_ipaddr+r')\]\s+->\s+' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['dst_ip'] = match.group(7)
                ptr['dst_port'] = match.group(8)
                ptr['proto'] = match.group(9).lower()

            # new message Without NAT
            match = re.search(r'' + ptrn3 + r':\s+App:(.*),\s+('+reg_ex_if+r')\s+' +
                              ptrn2 + r'\s*->\s+' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['dst_ip'] = match.group(6)
                ptr['dst_port'] = match.group(7)
                ptr['proto'] = match.group(8).lower()

            # Without NAT
            match = re.search(r'' + ptrn3 + r':\s*' + ptrn2 +
                              r'\s*->\s*' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(2)][match.group(3)]
                ptr['dst_ip'] = match.group(4)
                ptr['dst_port'] = match.group(5)
                ptr['proto'] = match.group(6).lower()

            # NAT44
            match = re.search(r'' + ptrn3 + r':\s*' + ptrn2 +
                              r'\s*\[('+regex_ipaddr+r')\]\s*->\s*' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(2)][match.group(3)]
                ptr['nat_ip'] = match.group(4)
                ptr['dst_ip'] = match.group(5)
                ptr['dst_port'] = match.group(6)
                ptr['proto'] = match.group(7).lower()

            # Source NAT
            match = re.search(r'' + ptrn3 + r':\s*' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s*->\s*' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(2)][match.group(3)]
                ptr['nat_ip'] = match.group(4)
                ptr['nat_port'] = match.group(5)
                ptr['dst_ip'] = match.group(6)
                ptr['dst_port'] = match.group(7)
                ptr['proto'] = match.group(8).lower()

            # Destination NAT
            match = re.search(r'' + ptrn3 + r':\s*' + ptrn2 + r'\s*->\s*' + ptrn2 +
                              r'\s*\[('+regex_ipaddr+r')\]\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(2)][match.group(3)]
                ptr['dst_ip'] = match.group(4)
                ptr['dst_port'] = match.group(5)
                ptr['nat_ip'] = match.group(6)
                ptr['proto'] = match.group(7).lower()

            match = re.search(r'(JSERVICES.*):\s*' + pr_ptrn + r'\s*application: (.*),\s*' +
                              ip_ptrn +
                              r',\s*Match (.*) rule-set:\s*(.*), rule:\s*(.*), term:\s*(\d+)', line)
            if match:
                ptr = data[match.group(1)][match.group(5)][match.group(6)]
                ptr['proto_num'] = match.group(2)
                ptr['proto'] = match.group(3).lower()
                ptr['app'] = match.group(4)
                ptr['dst_ip'] = match.group(7)
                ptr['dst_port'] = match.group(8)
                ptr['match'] = match.group(9)
                ptr['ruleset_name'] = match.group(10)
                ptr['rule_name'] = match.group(11)
                ptr['term'] = match.group(12)

            match = re.search(r'(JSERVICES.*):\s*' +
                              pr_ptrn + r'\s*app: (.*),\s*('+reg_ex_if+r')\s*' +
                              ip_ptrn +
                              r',\s*Match (.*) rule-set\s*(.*) rule\s*(.*) term\s*(\d+)', line)
            if match:
                ptr = data[match.group(1)][match.group(6)][match.group(7)]
                ptr['proto_num'] = match.group(2)
                ptr['proto'] = match.group(3).lower()
                ptr['app'] = match.group(4)
                ptr['intf'] = match.group(5)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['match'] = match.group(10)
                ptr['ruleset_name'] = match.group(11)
                ptr['rule_name'] = match.group(12)
                ptr['term'] = match.group(13)

            # ICMP64 session where source is not predictable, hence not using port
            # as a KEY
            match = re.search(r'(JSERVICES.*):\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s+->\s+' + ptrn2 +
                              r'\s*\[('+regex_ipaddr+r')\]\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['nat_port'] = match.group(7)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['srvr_ip'] = match.group(10)
                ptr['proto'] = match.group(11).lower()

            # For ICMP case where source port is not predictable
            match = re.search(r'(JSERVICES.*):\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s+->\s+' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['nat_port'] = match.group(7)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['proto'] = match.group(10).lower()

            # new message for SFW44/SFW66
            match = re.search(r'(JSERVICES.*):\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*->\s*' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['dst_ip'] = match.group(6)
                ptr['dst_port'] = match.group(7)
                ptr['proto'] = match.group(8).lower()

            # new message for SFW44/SFW66, SESSION_OPEN LOGS
            match = re.search(r'(JSERVICES.*):\s+App:(.*),\s+('+reg_ex_if+r')\s+' + ptrn2 +
                              r'\s*->\s*' +
                              ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['dst_ip'] = match.group(6)
                ptr['dst_port'] = match.group(7)
                ptr['proto'] = match.group(8).lower()

            # NEW for SFW
            match = re.search(r'(JSERVICES.*):\s*' + pr_ptrn1 +
                              r'\s*app: (.*),\s*('+reg_ex_if+r')\s*' +
                              ip_ptrn +
                              r',\s*Match (.*) rule-set\s*(.*) rule\s*(.*) term\s*(\d+)', line)
            if match:
                ptr = data[match.group(1)][match.group(6)]
                ptr['proto_num'] = match.group(2)
                ptr['proto'] = match.group(3).lower()
                ptr['app'] = match.group(4)
                ptr['intf'] = match.group(5)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['match'] = match.group(10)
                ptr['ruleset_name'] = match.group(11)
                ptr['rule_name'] = match.group(12)
                ptr['term'] = match.group(13)

            # NEW for NAT RULE MATCH 14.2 latest
            match = re.search(r'(JSERVICES.*):\s*' + pr_ptrn1 +
                              r'\s*application: (.*),\s*('+reg_ex_if+'):' + ip_ptrn +
                              r',\s*Match (.*) rule-set:\s*(.*), rule:\s*(.*), term:\s*(.*)', line)
            if match:
                ptr = data[match.group(1)][match.group(6)]
                ptr['proto_num'] = match.group(2)
                ptr['proto'] = match.group(3).lower()
                ptr['app'] = match.group(4)
                ptr['intf'] = match.group(5)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['match'] = match.group(10)
                ptr['ruleset_name'] = match.group(11)
                ptr['rule_name'] = match.group(12)
                ptr['term'] = match.group(13)

            # NEW for SFW
            match = re.search(r'(JSERVICES.*):\s*' + pr_ptrn1 +
                              r'\s*application: (.*),\s*' + ip_ptrn +
                              r',\s*Match (.*) rule-set:\s*(.*), rule:\s*(.*), term:\s*(\d+)', line)
            if match:
                ptr = data[match.group(1)][match.group(5)]
                ptr['proto_num'] = match.group(2)
                ptr['proto'] = match.group(3).lower()
                ptr['app'] = match.group(4)
                ptr['dst_ip'] = match.group(7)
                ptr['dst_port'] = match.group(8)
                ptr['match'] = match.group(9)
                ptr['ruleset_name'] = match.group(10)
                ptr['rule_name'] = match.group(11)
                ptr['term'] = match.group(12)

            # new for session log
            match = re.search(r'' + ptrn3 + r':\s+application:(.*),\s+('+reg_ex_if+r')\s+' +
                              ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s+->\s+\[('+regex_ipaddr+r')\]\s+' +
                              ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['nat_port'] = match.group(7)
                ptr['dst_ip'] = match.group(9)
                ptr['dst_port'] = match.group(10)
                ptr['srvr_ip'] = match.group(8)
                ptr['proto'] = match.group(11).lower()

            # new for session log
            match = re.search(r'(JSERVICES.*):\s*application:(.*),\s+('+reg_ex_if+r')\s*' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s*->\s*' + ptrn2 + r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['nat_port'] = match.group(7)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['srvr_ip'] = match.group(4)
                ptr['proto'] = match.group(10).lower()

            # new for nat rule
            match = re.search(r'(JSERVICES.*):\s*' + pr_ptrn +
                              r'\s*application: (.*),\s*('+reg_ex_if+'):' +
                              ip_ptrn +
                              r',\s*Match (.*) rule-set:\s*(.*), rule:\s*(.*), term:\s*(.*)', line)
            if match:
                ptr = data[match.group(1)][match.group(6)][match.group(7)]
                ptr['proto_num'] = match.group(2)
                ptr['proto'] = match.group(3).lower()
                ptr['app'] = match.group(4)
                ptr['intf'] = match.group(5)
                ptr['dst_ip'] = match.group(8)
                ptr['dst_port'] = match.group(9)
                ptr['match'] = match.group(10)
                ptr['ruleset_name'] = match.group(11)
                ptr['rule_name'] = match.group(12)
                ptr['term'] = match.group(13)

            # new for session log NAT64
            match = re.search(r'(JSERVICES.*):\s*application:(.*),\s+('+reg_ex_if+r')\s*' + ptrn2 +
                              r'\s*\[' + ptrn2 + r'\]\s*->\s*\[('+regex_ipaddr+r')\]\s*' + ptrn2 +
                              r'\s*\((.*)\)', line)
            if match:
                ptr = data[match.group(1)][match.group(4)][match.group(5)]
                ptr['app'] = match.group(2)
                ptr['intf'] = match.group(3)
                ptr['nat_ip'] = match.group(6)
                ptr['nat_port'] = match.group(7)
                ptr['dst_ip_v4'] = match.group(8)
                ptr['dst_ip'] = match.group(9)
                ptr['dst_port'] = match.group(10)
                ptr['proto'] = match.group(11).lower()

        self.log('INFO', 'NAT log messages: {}'.format(data))

        self.fn_checkout()

        return data

    def _verify_syslogs(self, **kwargs):
        """Verify NAT/SFW related logs from 'show log messages' """

        self.fn_checkin("Verifying NAT log messages")

        result = True

        if 'then_syslog' in self.nat_rule and self.nat_rule['then_syslog'] is None:
            self.log('INFO', "Nothing to do as Syslog is not enabled in the configurtion.")
            return False

        if 'xtnsv' in kwargs and kwargs['xtnsv'] is not None:
            exp_data = kwargs['xtnsv']
            msg = kwargs['msg']
            src_ip = exp_data['src_ip']
            # src_ip              = exp_data['src_ip']
            # src_ip              = exp_data.pop('src_ip')
            # exp_data['srvr_ip'] = src_ip
            src_port = kwargs['src_port']

            act_value = self._get_syslogs(msg, **exp_data)
            act_val = ''
            if src_port is not None:
                try:
                    act_val = act_value[msg][src_ip][src_port]
                    # act_val['src_ip']  = act_val.pop('srvr_ip')
                except (TypeError, KeyError):
                    self.fn_checkout(False, "No syslog message({}) found for {} {}".format(
                        msg, src_ip, src_port))
            else:
                try:
                    act_val = act_value[msg][src_ip]
                    # act_val['src_ip']  = act_val.pop('srvr_ip')
                except (TypeError, KeyError):
                    self.fn_checkout(False, "No syslog message({}) found for {}".format(msg,
                                                                                        src_ip))
            # act_val['src_ip']  = act_val.pop('srvr_ip')
            exp = {}
            for key in exp_data:
                if key == 'src_ip':
                    if 'srvr_ip' in act_val:
                        exp['srvr_ip'] = exp_data[key]
                else:
                    exp[key] = exp_data[key]
            # self.log('INFO', 'Expected data is:{} and actual data is {}'.format(exp, act_val))
            result &= utils.cmp_dicts(exp_data=exp, act_data=act_val)

        # self._get_intf_ss()

        # for tg_if in self.tg_sess:
        #   path      = self.topo['intf'][tg_if]['path']
        #   intf_list = self.topo['path_res'][self.resource][path]
        #   for r_if in intf_list:
        #     r_if = t['resources'][self.resource]['interfaces'][r_if]['pic']
        #     if r_if in self.intf_ss:
        #       sset       = self.intf_ss[r_if]
        #       sp       = self.sset[sset]['sp']
        #       nat_rule = self.sset[sset]['nat_rules']
        #       nat_rule = nat_rule[0]
        #       nat_pool = self.nat_rule[nat_rule]['src_pool']
        #       nat_ip   = self.nat_pool[nat_pool]['addr']
        #       nat_port = self.nat_pool[nat_pool]['nat_port']
        #       max_sess = len(self.tg_sess[tg_if]['sess'])
        #       if max_sess < 100:
        #         limit_perc = 100
        #       limit_final = int(float(max_sess) * (limit_perc/100))
        #       if limit is not None:
        #         limit_final = limit
        #       Range       = random.sample(range(max_sess), limit_final)
        #       for sess_idx in Range:
        #         sess = self.tg_sess[tg_if]['sess'][sess_idx]
        #         if nat_port is not None:
        #           ports = nat_port.split("-")
        #           nat_port_low, nat_port_high = ports[0] , ports[1]
        #         src_ips = []
        #         if limit is not None:
        #           src_ips.append(act_value[sp][sset].keys())
        #         else:
        #           src_ips.append(sess['src_ip'])
        #         # self.log('INFO', 'sess{} , src_ips{}'.format(pp(sess), pp(src_ips)))
        #         for s_ip in src_ips:
        #             s_prt = str(sess['src_prt'])
        #             # if 'sl_class_list' in self.sset[sset] or 'syslog_class' in self.sset[sset]:
        #             if 'sl_class_list' in self.sset[sset]:
        #               if self.sset[sset]['sl_class_list'] is not None:
        #                 exp_data           = {}
        #                 exp_data['src_ip'] = s_ip
        #                 exp_data['dst_ip'] = sess['dst_ip']
        #                 exp_data['proto']  = sess['protocol'].lower()
        #                 if 'stateful-firewall-logs' in self.sset[sset]['sl_class_list']:
        #                   msg = 'JSERVICES_SFW_RULE_ACCEPT'
        #                   act_value = self.get_syslogs(msg, src_ip=s_ip, src_port=s_prt, **kwargs)
        #                 if 'nat-logs' in self.sset[sset]['sl_class_list']:
        #                   msg = 'JSERVICES_NAT_RULE_MATCH'
        #                   act_value = self.get_syslogs(msg, src_ip=s_ip, src_port=s_prt, **kwargs)
        #                 if 'session-logs' in self.sset[sset]['sl_class_list']:
        #                   msg = 'JSERVICES_SESSION_OPEN'
        #                 act_value  = self.get_syslogs(msg, src_ip=s_ip, src_port=s_prt, **kwargs)
        #                   act_val    = act_value[msg][s_ip][s_prt]
        #                   act_nat_ip = act_val['nat_ip']
        #                   if utils.is_ip_in_subnet(act_nat_ip, nat_ip) == False:
        #                     self.log('ERROR', 'Actual NAT IP({}) is **NOT** within expected NAT
            # Pool({})'.format(act_nat_ip, nat_ip))
        #                     result = False
        #                     continue
        #                   else:
        #                     self.log('INFO', ' Actual NAT IP({}) is **IS** within expected NAT \
            # Pool({})'.format(act_nat_ip, nat_ip))
        #                   if nat_port is not None:
        #                     act_nat_port = act_val['nat_port']
        #                     if act_nat_port < nat_port_low and  act_nat_port > nat_port_high:
        #                       self.log('ERROR', 'Actual NAT Port({}) is **NOT** within \
            # expected NAT Port Range({})'.format(act_nat_port, nat_port))
        #                       result = False
        #                       continue
        #                     else:
        #                       self.log('INFO', 'Actual NAT Port({}) **IS** within\
            # expected NAT Port Range({}))'.format(act_nat_port, nat_port))
        #                 if s_prt is not None:
        #                   try:
        #                     act_val = act_value[msg][s_ip][s_prt]
        #                   except:
        #                     self.log('ERROR', 'No syslog message({}) found for {}'.format(
            # msg, s_ip))
        #                     result &= False
        #                     continue
        #                 else:
        #                   try:
        #                     act_val = act_value[msg][s_ip]
        #                   except:
        #                     self.log('ERROR', 'No syslog message({}) found for {}'.format(
            # msg, s_ip))
        #                     result &= False
        #                     continue
        #                 # self.log('INFO', '{} , {}'.format(pp(act_val), pp(act_value)))
        #                 if act_val is None:
        #                   self.log('ERROR', 'Unable to find data for src_ip and src_port in
            # actual data')
        #                   return False

        #                 result &= utils.cmp_dicts(exp_data=exp_data, act_data=act_val)

        return self.fn_checkout(result)

    def _get_ss_from_pool(self, **kwargs):
        """Get SS/SP from pool name"""

        self.fn_checkin("Building required mappings")
        # Build pool name to service set mapping
        for pool_name in self.nat_pool:
            if pool_name not in self.pool_map:
                self.pool_map[pool_name] = {}
            if pool_name in self.nat_pool_rule_map['src_pool']:
                _nat_rule = self.nat_pool_rule_map['src_pool'][pool_name]
            elif pool_name in self.nat_pool_rule_map['dst_pool']:
                _nat_rule = self.nat_pool_rule_map['dst_pool'][pool_name]
            else:
                #Adding print as without it continue not show as executed in unit testing coverage
                print
                continue
            _ss_name = self.ss_map['nat_rules'][_nat_rule]
            sset = self.pool_map[pool_name]['sset'] = _ss_name
            spic = self.pool_map[pool_name]['spic'] = self.sset[_ss_name]['intf']
            self.pool_map[pool_name]['total_sess'] = self.tg_sess_cnt[spic][sset]
            self.ss_map['nat_pool'][pool_name] = _ss_name

        #self._get_ss_for_intf()
        self._get_tg_port_and_config_mapping(**kwargs)
        self.log('INFO', "Pool-ss map: {}".format(self.pool_map))

        return self.fn_checkout()

    def _get_tg_port_and_config_mapping(self, **kwargs):
        """Determines sp,sset,rule,pool etc. thats going to service traffic for every tg port"""

        self.fn_checkin("Mapping TG Port and config")

        if self.tg_sess_cnt is None:
            super()._get_tg_port_and_config_mapping(**kwargs)

        #_pool_cnt = self.tg_sess_cnt['nat_pool'] = {}
        for tg_if in self.tg_cfg_map:
            _conf_map = self.tg_cfg_map[tg_if]
            nat_rule = _conf_map['nat_rules'] = self.sset[_conf_map['sset']]['nat_rules']
            if nat_rule is not None:
                # todo Will handle only one NAT Rule for now
                nat_rule = nat_rule[0]
                nat_pool = None
                self.log("NAT Rule, {}: {}".format(nat_rule, self.nat_rule[nat_rule]))
                # Check if NAT Pool is configured
                if 'src_pool' in self.nat_rule[nat_rule]:
                    nat_pool = _conf_map['nat_pool'] = self.nat_rule[nat_rule]['src_pool']
                    #_conf_map['nat_ip'] = self.nat_pool[nat_pool]['addr']
                    pool_cfg = self.nat_pool[nat_pool]
                    if 'port_low' in pool_cfg:
                        _conf_map['nat_port_low'] = pool_cfg['port_low']
                        _conf_map['nat_port_high'] = pool_cfg['port_high']
                        _conf_map['nat_port'] = pool_cfg['port_low'] + '-' + pool_cfg['port_high']
                    elif ('port_auto' in pool_cfg and pool_cfg['port_auto']) or \
                          ('port_auto_auto' in pool_cfg and pool_cfg['port_auto_auto']) or\
                          ('port_auto_random' in pool_cfg and \
                           pool_cfg['port_auto_random']):
                        _conf_map['nat_port_low'] = 1024
                        _conf_map['nat_port_high'] = 65535
                        _conf_map['nat_port'] = '1024-65535'
                if 'dst_pool' in self.nat_rule[nat_rule]:
                    nat_pool = _conf_map['nat_pool'] = self.nat_rule[nat_rule]['dst_pool']
                    #_conf_map['nat_ip'] = self.nat_pool[nat_pool]['addr']

                if nat_pool is not None:
                    _conf_map['nat_ip'] = self.nat_pool[nat_pool]['addr']
                    #if nat_pool not in _pool_cnt:
                        #_pool_cnt[nat_pool] = {}
                    #_pool_cnt[nat_pool]['tot_sess'] = self.tg_sess[tg_if]['total']

        self.log('INFO', "TG Port and config mapping: {}".format(self.tg_cfg_map))

        self.fn_checkout()

    def _get_src_ip_flow_from_data(self, src_ip, cfg_map, data):
        """Return mapping from the actual data for the given Source ip.
        Service pic, service set, NAT pool are picked from the configuration map
        created by _get_tg_port_and_config_mapping
        """

        spic, sset, nat_pool = [cfg_map[key] for key in ['spic', 'sset', 'nat_pool']]

        _msg = "Flow(spic={}, sset={}, pool={}".format(spic, sset, nat_pool)
        _msg += ", ip={})".format(src_ip)

        self.fn_checkin("Finding {}".format(_msg))
        self.log("Actual data: {}".format(data))
        try:
            _flow = data[spic][sset][nat_pool][src_ip]
        except (TypeError, KeyError):
            self.log('ERROR', '{} not found in actual data({})'.format(_msg, data))
            return None

        if _flow is None:
            self.log('ERROR', '{} not found in actual data({})'.format(_msg, data))
            return None

        self.log("Flow: {}".format(_flow))
        self.log("Actual data: {}".format(data))

        self.fn_checkout()

        return _flow

    def _get_src_ip_port_flow_from_data(self, src_ip, src_port, cfg_map, data):
        """Return mapping from the actual data for the given Source ip and port.
        Service pic, service set, NAT pool are picked from the configuration map
        created by _get_tg_port_and_config_mapping
        """

        spic, sset, nat_pool = [cfg_map[key] for key in ['spic', 'sset', 'nat_pool']]
        _msg = "Flow(spic={}, sset={}, pool={}".format(spic, sset, nat_pool)
        _msg += ", ip={}, port={})".format(src_ip, src_port)
        self.fn_checkin("Finding {}".format(_msg))
        self.log("Actual data: {}".format(data))
        try:
            _flow = data[spic][sset][nat_pool][src_ip][src_port]
        except (TypeError, KeyError):
            self.log('ERROR', '{} not found in actual data({})'.format(_msg, data))
            return None

        if _flow is None:
            self.log('ERROR', '{} not found in actual data({})'.format(_msg, data))
            return None

        self.log("Flow: {}".format(_flow))
        self.log("Actual data: {}".format(data))

        self.fn_checkout()

        return _flow

    def _is_nat_ip_in_pool(self, flow, cfg_map):
        """Verify if actual NAT IP is with in NAT Pool IP range"""

        self.fn_checkin("Checking if given nat ip is in flow: {}".format(flow))
        nat_ip = None
        if 'nat_ip' in flow:
            nat_ip = flow['nat_ip']
        if 'eim_nat_ip' in flow:
            # NAT IP is saved as eim_nat_ip in nat mappings detail
            nat_ip = flow['eim_nat_ip']
        if nat_ip is None:
            self.log("{} is not there in the flow({})".format(nat_ip, flow))
            return False

        act_nat_ip_str = "Actual NAT IP({})".format(nat_ip)
        nat_ip_str = "within expected NAT Pool({})".format(cfg_map['nat_ip'])
        if not iputils.is_ip_in_subnet(nat_ip, cfg_map['nat_ip']):
            self.log('ERROR', '{} is **NOT** {}'.format(act_nat_ip_str, nat_ip_str))
            return False

        self.log('INFO', '{} **IS** {}'.format(act_nat_ip_str, nat_ip_str))

        return self.fn_checkout(True)

    def _is_nat_port_in_pool(self, flow, cfg_map):
        """Verify if actual NAT Port is with in NAT Pool port range"""

        nat_port = None
        if 'nat_port' not in cfg_map or cfg_map['nat_port'] is None:
            self.log('ERROR', "nat_port is not there in the config({})".format(cfg_map))
            #print("nat_port is not there in the config({})".format(cfg_map))
            return False
        if 'nat_port' in flow:
            nat_port = int(flow['nat_port'])
        if 'eim_nat_port' in flow:
            # NAT Port is saved as eim_nat_port in nat mappings detail
            nat_port = int(flow['eim_nat_port'])

        if nat_port is None:
            self.log('ERROR', "nat_port is not there in the flow({})".format(flow))
            #print("nat_port is not there in the flow({})".format(flow))
            return False

        _act_port_str = "Actual NAT Port({})".format(nat_port)
        _range_str = "within expected NAT Pool Port Range({})".format(cfg_map['nat_port'])
        self.log('INFO', "Verifying if {} is {}".format(_act_port_str, _range_str))
        if nat_port > int(cfg_map['nat_port_low']) and nat_port < int(cfg_map['nat_port_high']):
            self.log('INFO', '{} **IS** {}'.format(_act_port_str, _range_str))
            return True

        self.log('ERROR', '{} is **NOT** {}'.format(_act_port_str, _range_str))

        return False

    def _get_profile_from_pool(self, sset, pool):
        """Update the service set profile pool address"""

        if 'addr' in self.nat_pool[pool]:
            self.ss_profile[self.nat_pool[pool]['addr']] = sset

    def _get_profile_from_ss(self, sset=None):
        """Update the object with the service set profile"""

        self.fn_checkin("Retrieving profile from sset")
        ss_names = [sset] if sset is not None else self.sset.keys()

        for ss_name in ss_names:
            if 'nat_rules' in self.sset[ss_name]:
                # Fetch NAT Rule/pool info
                for nat_rule in self.sset[ss_name]['nat_rules']:
                    if 'src_pool' in self.nat_rule[nat_rule]:
                        self._get_profile_from_pool(ss_name, self.nat_rule[nat_rule]['src_pool'])

        self.fn_checkout()
