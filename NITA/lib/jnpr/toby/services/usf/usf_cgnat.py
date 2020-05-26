# pylint: disable=undefined-variable
# p-ylint: disable=invalid-name
"""Module contains methods for CGNAT"""

__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

from jnpr.toby.utils import iputils
from jnpr.toby.services import utils
from jnpr.toby.services.usf.usf_services import usf_services


class usf_cgnat(usf_services):
    """Class contains methods for CGNAT"""

    def __init__(self, **kwargs):
        """Constructor method for cgnat class"""

        super(usf_cgnat, self).__init__(**kwargs)

        self.cmd_list = []
        self.nat_rule_set = {}
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
        self.data['nat_rule_set'] = {}
        self.data['sess_xtnsv'] = {}
        self.pool_name = None
        self.rule_name = None
        self.rule_info = {}
        self.nat_type = None
        self.vrf_dict = {}
        self.expected_output = {}
        self.application_dict = {}
        self.transport = None

        for key in kwargs:
            setattr(self, key, kwargs[key])

    ################################################################
    # set methods
    ################################################################
    def set_nat_rule_set(self, name='nat_rule_set', **kwargs):
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

        :param string nat_type:
            **OPTIONAL** NAT Type. Default is 'source'. Valid values source, destination, static

        :param int index:
            **OPTIONAL** Rule starting index. Default value is 1

        :param string dir:
            **OPTIONAL** NAT direction. Defaul value is 'input'

        :param int num_rules:
            **OPTIONAL** Number of terms. Default is 1

        :param bool same_rule_set:
            **OPTIONAL** Should be set if the rule set name should remain the same on scaling config. Default is False

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
        :param string src_addr_name:
            **OPTIONAL** From source-address-name, which points to an address book.
        :param string dst_addr_name:
            **OPTIONAL** From destination-address-name, which points to an address book.
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

        :param bool snat_off:
            **OPTIONAL** Flag to enable source_nat off option.

        :param bool dnat_off:
            **OPTIONAL** Flag to enable source_nat off option.
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
                                               'num_rules': 1, 'rule_name': 'nr',
                                               'index': 1, 'nat_type': 'source',
                                               'rs_idx_reset': False, 'rs_idx': 1,
                                               'src_addr': None, 'src_addr_step': 1,
                                               'src_addr_name': None, 'dst_addr_name': None,
                                               'src_addr_nw_step': 1, 'src_addr_nw_step_cnt': None,
                                               'dst_addr': None, 'dst_addr_step': 1, 'same_rule_set': False,
                                           })

        src_addr = this['src_addr']
        dst_addr = this['dst_addr']
        src_addr_name = this['src_addr_name']
        dst_addr_name = this['dst_addr_name']

        #term = this['term']
        rs_idx = this['index']

        src_addr_cntr = 0

        for iter_ii in range(1, this['count']+1):
            if this['same_rule_set'] == 1:
                rs_tag = name + "1"
            else:
                rs_tag = name + str(rs_idx)
            if rs_tag not in self.nat_rule_set:
                self.nat_rule_set[rs_tag] = {}
            self.ptr = self.nat_rule_set[rs_tag]
            #self._update(this)
            #self.ptr = this

            pool_tag = rs_idx
            _cmd = "{} services nat {} rule-set {}".format(this['action'], this['nat_type'],
                                                           rs_tag)
            self.cmd_add("{} match-direction {}".format(_cmd, this['dir']))

            #self.cmd_add("allow-overlapping-nat-pools", 'allow_overlap', opt='flag')
            #self.cmd_add("allow-all-nat-on-ams-warm-standby", 'ams_warm_standby', opt='flag')

            if this['rs_idx_reset']:
                rs_idx = this['rs_idx']

            #for _ in range(0, this['num_rules']):
            rule_tag = this['rule_name'] + str(rs_idx)

            for _ in range(0, this['num_rules']):
                self.cmd = "{} rule {}".format(_cmd, rule_tag)
                if rule_tag not in self.nat_rule_set[rs_tag]:
                    self.nat_rule_set[rs_tag][rule_tag] = {}
                self.ptr = self.nat_rule_set[rs_tag][rule_tag]
                self._update(this)
                self._cmd_name_tag = rs_tag
                self._cmd_mapping = self.nat_pool_rule_map

            #self.cmd_add("then syslog", 'then_syslog', opt='flag')
            #self.cmd_add("then no-translation", 'no_trans', opt='flag')
            #self.cmd_add("from source-address any-unicast", 'src_any_ucast', opt='flag')
            #self.cmd_add("from destination-address any-unicast", 'dst_any_ucast', opt='flag')
            if src_addr is not None:
                self.cmd_add("match source-address {}".format(src_addr))
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
                self.cmd_add("match destination-address {}".format(dst_addr))
                self.ptr['dst_addr'] = dst_addr
                dst_addr = iputils.incr_ip_subnet(dst_addr, this['dst_addr_step'])

            if 'src_low' in this:
                if 'src_high' in this:
                    _range_str = "{} to {}".format(this['src_low'], this['src_high'])
                else:
                    _range_str = "{}".format(this['src_low'])
                self.cmd_add("match source-port {}".format(_range_str))

            self.cmd_add("match application", 'from_apps_list')
            if 'dst_low' in this:
                if 'dst_high' in this:
                    _range_str = "{} to {}".format(this['dst_low'], this['dst_high'])
                else:
                    _range_str = "{}".format(this['dst_low'])
                self.cmd_add("match destination-port {}".format(_range_str))

            if dst_addr_name is not None:
                self.cmd_add("match destination-address-name {}".format(dst_addr_name))
                self.ptr['dst_addr_name'] = dst_addr_name

            if src_addr_name is not None:
                self.cmd_add("match source-address-name {}".format(src_addr_name))
                self.ptr['src_addr_name'] = src_addr_name

            #self.cmd_add("from applications", 'from_apps_list')
            #self.cmd_add("from application-sets", 'from_appsets_list')

            #self.cmd_add("from source-prefix-list", 'src_pfx_list')
            #self.cmd_add("from destination-prefix-list", 'dst_pfx_list')
            self.cmd_add("then source-nat pool", 'src_pool', tag=pool_tag,
                         mapping=True)
            self.cmd_add("then destination-nat pool", 'dst_pool', tag=pool_tag,
                         mapping=True)
            if 'snat_off' in this:
                self.cmd_add("then source-nat off", 'snat_off', opt='flag')
            if 'dnat_off' in this:
                self.cmd_add("then destination-nat off", 'dnat_off', opt='flag')
            pool_tag += 1

            rs_idx += 1

        result = self.config()

        return self.fn_checkout(result)

    def set_nat_pool(self, name='nat_pool', **kwargs):
        """Configure NAT pool based on parameters passed

        Use the optional argument, 'count', to generate scaling config.
        For example, This will create 10 NAT pools from nat_pool1 to nat_pool9::

            set_nat_pool('nat_pool', count=10)

        :param string name:
            **OPTIONAL** Name of NAT pool to be configured. Default is 'nat_pool'

        :param string pool_type:
            **OPTIONAL** Type of NAT pool to be configured. Default is 'source'.
            Valid values are source, destination, static.

        :param string action:
            **OPTIONAL** Valid values are set,delete,activate,deactivate. Default is 'set'

        :param int count:
            **OPTIONAL** Number of NAT Pools to be configured. Default is 1.

        :param string addr:
            **OPTIONAL** Pool address
        :param string host_addr_base:
            **OPTIONAL** Host address base
        :param int port_low:
            **OPTIONAL** Pool port range - low

        :param int port_high:
            **OPTIONAL** Pool port range - high

        :param int port_limit:
            **OPTIONAL** Port limit per address

        :param int map_to:
            **OPTIONAL** Default Mapping timeout (120s-86400s)

        :param int app_to:
            **OPTIONAL** APP Mapping timeout (120s-86400s)

        :param int eim_to:
            **OPTIONAL** EIM timeout (120s-86400s)

        :param bool pool_overflow:
            **OPTIONAL** Pool overflow. Valid options are interface, pool name
            (set services nat pool <pool> over-flow <>)

        :param bool port_no_trans:
            **OPTIONAL** Flag to disable port translation
            (set services nat pool <pool> port no-translation)

        :param bool pba:
            **OPTIONAL** Flag to enable port block allocation

        :param bool addr_step:
            **OPTIONAL** Increment the address by step. Default is 1

        :param int pba_blk_to:
            **OPTIONAL** Sets PBA active block timeout

        :param int pba_blk_size:
            **OPTIONAL** Sets PBA block size

        :param int pba_max_blks:
            **OPTIONAL** Sets PBA max blocks per address

        :param bool detnat:
            **OPTIONAL** Flag to enable deterministic-PBA

        :param string detnat_blk_size:
            **OPTIONAL** Sets deterministic-PBA block size

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
                                               'pool_type': 'source', 'addr': None,
                                               'port_low': None, 'port_high': None,
                                               'addr_low':None, 'addr_high':None,
                                               'addr_step':1,
                                           })
        (addr, addr_low, addr_high) = (this['addr'], this['addr_low'], this['addr_high'])
        for iter_ii in range(1, this['count'] + 1):
            pool_name = name + str(iter_ii)
            if pool_name not in self.nat_pool:
                self.nat_pool[pool_name] = {}
            self.ptr = self.nat_pool[pool_name]
            self._update(this)
            self.cmd = "{} services nat {} pool {}".format(this['action'],
                                                           this['pool_type'], pool_name)
            if 'host_addr_base' in this and this['host_addr_base'] is not None:
                self.cmd_add("host-address-base {}".format(this['host_addr_base']))

            if addr is not None or addr_low is not None:
                if addr_low and addr_high:
                    self.cmd_add("address {} to {}".format(addr_low, addr_high))
                else:
                    self.cmd_add("address {}".format(addr))
                    self.ptr['addr'] = addr
                    addr = iputils.incr_ip_subnet(this['addr'], this['addr_step'])

            if this['port_low'] is not None and this['port_high'] is not None:
                self.cmd_add("port range {} to {}".format(this['port_low'],
                                                          this['port_high']))
            self.cmd_add("port no-translation", 'port_no_trans', opt='flag')

            #self.cmd = _cmd + " port block-allocation"

            self.cmd_add("", 'pba', opt='flag')
            self.cmd_add("active-block-timeout", 'pba_blk_to')
            self.cmd_add("block-size", 'pba_blk_size')
            self.cmd_add("max-blocks-per-address", 'pba_max_blks')
            self.cmd_add("interim-logging-interval", 'pba_interim_log_interval')
            self.cmd_add("last-block-recycle-timeout", 'pba_blk_recycle_to')

            #self.cmd_add("port deterministic-port-block-allocation", 'port_detnat', opt='flag')
            #self.cmd = _cmd + " port deterministic"
            self.cmd_add("", 'detnat', opt='flag')
            self.cmd_add("block-size", 'detnat_blk_size')
            #self.cmd_add("include-boundary-addresses", 'port_detnat_incl_bndry_addrs', opt='flag')

            # when the action is not 'set' and there are no other command
            # options to be executed
            if len(self.cmd_list) == 0 and this['action'] != 'set':
                self.cmd_add("")

        result = self.config()

        self.log('INFO', "NAT Pool: {}".format(self.nat_pool))

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
        #self._get_tg_port_and_config_mapping(**kwargs)

        super(usf_cgnat, self).verify(**kwargs)

        # self.verify_sess_count(**kwargs)
        # self.tg_sess = kwargs.pop('tg_sess')
        #self.verify_nat_pool_detail(**kwargs)
        #self.verify_sessions_extensive(**kwargs)
        # self.verify_nat_eim(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_mappings_detail(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_app_mappings(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_mappings_summary(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_statistics(tg_sess=self.tg_sess, **kwargs)
        # self.verify_nat_syslogs(tg_sess=self.tg_sess, **kwargs)

        return self.fn_checkout()

    def _get_ss_from_pool(self, **kwargs):
        """Get SS/SP from pool name"""

        self.fn_checkin("Building required mappings")
        # Build pool name to service set mapping
        for pool_name in self.nat_pool:
            if pool_name not in self.pool_map:
                self.pool_map[pool_name] = {}
            if pool_name in self.nat_pool_rule_map['src_pool']:
                _nat_rule_set = self.nat_pool_rule_map['src_pool'][pool_name]
            elif pool_name in self.nat_pool_rule_map['dst_pool']:
                _nat_rule_set = self.nat_pool_rule_map['dst_pool'][pool_name]
            else:
                continue
            _ss_name = self.ss_map['nat_rule_set'][_nat_rule_set]
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
            super(usf_cgnat, self)._get_tg_port_and_config_mapping(**kwargs)

        #_pool_cnt = self.tg_sess_cnt['nat_pool'] = {}
        for tg_if in self.tg_cfg_map:
            _conf_map = self.tg_cfg_map[tg_if]
            nat_rule_set = _conf_map['nat_rule_set'] = self.sset[_conf_map['sset']]['nat_rule_set']
            if nat_rule_set is not None:
                # todo Will handle only one NAT Rule for now
                nat_rule_set = nat_rule_set[0] #[Nithy: The _conf_map does not return nat_rule_set as LIST]
                nat_pool = None
                self.log("NAT Rule Set, {}: {}".format(nat_rule_set, self.nat_rule_set[nat_rule_set]))
                # Check if NAT Pool is configured
                if 'src_pool' in self.nat_rule_set[nat_rule_set]:
                    nat_pool = _conf_map['nat_pool'] = self.nat_rule_set[nat_rule_set]['src_pool']
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
                if 'dst_pool' in self.nat_rule_set[nat_rule_set]:
                    nat_pool = _conf_map['nat_pool'] = self.nat_rule_set[nat_rule_set]['dst_pool']
                    #_conf_map['nat_ip'] = self.nat_pool[nat_pool]['addr']

                if nat_pool is not None:
                    _conf_map['nat_ip'] = self.nat_pool[nat_pool]['addr']
                    #if nat_pool not in _pool_cnt:
                        #_pool_cnt[nat_pool] = {}
                    #_pool_cnt[nat_pool]['tot_sess'] = self.tg_sess[tg_if]['total']

        self.log('INFO', "TG Port and config mapping: {}".format(self.tg_cfg_map))

        self.fn_checkout()

    def get_usf_nat_pool_detail(self, name=None):
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

        #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        for pool_name in names:
            _pool_type = self.nat_pool[pool_name]['pool_type']
            _xpath = '{}-nat-pool-detail-information/{}-nat-pool-info-entry'.format(_pool_type, _pool_type)
            cmd = 'show services nat {} pool {}'.format(_pool_type, pool_name)
            entry = self.get_xml_output(cmd, xpath=_xpath)
            if pool_name not in self.data['nat_pool']:
                self.data['nat_pool'][pool_name] = {}
            self.data['nat_pool'][pool_name]['spic'] = str(entry['interface-name'])
            self.data['nat_pool'][pool_name]['sset'] = str(entry['service-set-name'])
            ptr = self.data['nat_pool'][pool_name]

            pool = entry

            ptr['addr_range_low'] = str(pool['source-pool-address-range']['address-range-low'])
            ptr['addr_range_high'] = str(pool['source-pool-address-range']['address-range-high'])
            ptr['single_ports_in_use'] = str(pool['source-pool-address-range']['single-port'])
            ptr['twin_ports_in_use'] = str(pool['source-pool-address-range']['twin-port'])
            ptr['tot_single_ports_in_use'] = str(pool['source-pool-address-range-sum']['single-port-sum'])
            ptr['tot_twin_ports_in_use'] = str(pool['source-pool-address-range-sum']['single-port-sum'])

            utils.update_data_from_output(ptr, pool, {
                'pool-id': 'pool_id',
                'routing-instance-name': 'ri_name',
                'host-address-base': 'host_addr_base',
                'source-pool-port-translation': 'ports_range',
                'source-pool-twin-port': 'twin_port_range',
                'port-overloading-factor': 'port_overloading_factor',
                'source-pool-address-assignment': 'addr_assignment',
                'total-pool-address': 'total_addr',
                'address-pool-hits': 'addr_pool_hits',
                'source-pool-blk-size': 'port_blk_mem_alloc_fail_errs',
                'source-pool-blk-max-per-host': 'parity_port_errs',
                'source-pool-blk-atv-timeout': 'preserve_range_errs',
                'source-pool-last-blk-rccl-timeout': 'configured_port_range',
                'source-pool-blk-interim-log-cycle': 'preserve_range_enabled',
                'source-pool-blk-log': 'app_errs',
                'source-pool-blk-used': 'app_xcd_port_lmt_errs',
                'source-pool-blk-total': 'blk_type',
            })

        self.log('INFO', "NAT pool detail: {}".format(self.data['nat_pool']))

        return self.fn_checkout(True)

    def verify_usf_nat_pool_detail(self, name=None, **kwargs):
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

        self._get_tg_port_and_config_mapping(**kwargs)
        self._get_ss_from_pool()

        self.get_usf_nat_pool_detail(name)

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
            exp_data = {
                'ri_name': 'default',
                'host_addr_base': '0.0.0.0', 'single_ports_in_use': _pool_sess_cnt,
                'tot_single_ports_in_use': _pool_sess_cnt, 'twin_ports_in_use':0,
                'ports_range': '[1024, 63487]', 'port_overloading_factor':1,
                'addr_assignment':'no-paired', 'twin_port_range': '[63488, 65535]'
            }
            #iputils.get_subnet_total_address is not defined: verify later if this block is necessary
            #if 'addr' in self.nat_pool[pool_name]:
            #    pool_addr = self.nat_pool[pool_name]['addr']
            #    addr_range = iputils.get_network_ip_range(pool_addr)
            #    exp_data['addr_range_low'], exp_data['addr_range_high'] = addr_range.split('-')
            #    exp_data['total_addr'] = iputils.get_subnet_total_address(pool_addr)
            if pool_name in self.pool_map:
                exp_data['spic'] = self.pool_map[pool_name]['spic']
                exp_data['sset'] = self.pool_map[pool_name]['sset']

            for key in kwargs:
                if 'tg_sess' in key:
                    continue
                exp_data[key] = kwargs[key]

            self.log('INFO', "Verifying expected({}) and actual({}) data".format(exp_data,
                                                                                 pool_data))
            if utils.cmp_dicts(exp_data, pool_data):
                self.log('INFO', "Verification details for pool, {}, PASSED".format(pool_name))
            else:
                self.log('INFO', "Verification for pool, {}, FAILED".format(pool_name))
                result = False

        return self.fn_checkout(result)

    def get_usf_nat_rule(self, rs_name=None, r_name=None):
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

        self.fn_checkin("Fetching NAT Rule")

        if 'nat_rule_set' not in self.data:
            self.data['nat_rule_set'] = {}

        # If name is specified, get details for that pool else for all the pools configured
        # Need to take care of scaling scenarios. Don't need to get details of
        # all the pools
        #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        rs_names = [rs_name] if rs_name is not None else self.nat_rule_set.keys()
        r_names = [r_name] if r_name is not None else self.nat_rule_set[rs_name].keys()

        #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        for rule_sets in rs_names:
            for rule_name in r_names:
                _nat_type = self.nat_rule_set[rule_sets][rule_name]['nat_type']
                _xpath = '{}-nat-rule-detail-information/{}-nat-rule-entry'.format(_nat_type, _nat_type)
                cmd = 'show services nat {} rule {}'.format(_nat_type, rule_name)
                entry = self.get_xml_output(cmd, xpath=_xpath)
                if rule_sets not in self.data['nat_rule_set']:
                    self.data['nat_rule_set'][rule_sets] = {}
                    self.data['nat_rule_set'][rule_sets][rule_name] = {}
                self.data['nat_rule_set'][rule_sets][rule_name]['spic'] = str(entry['interface-name'])
                self.data['nat_rule_set'][rule_sets][rule_name]['sset'] = str(entry['service-set-name'])
                self.data['nat_rule_set'][rule_sets][rule_name]['rule'] = str(entry['rule-name'])
                self.data['nat_rule_set'][rule_sets][rule_name]['rule_set'] = str(entry['rule-set-name'])
                ptr = self.data['nat_rule_set'][rule_sets][rule_name]

                rule = entry

                ptr['src_addr_range_low'] = str(rule['source-address-range-entry']['rule-source-address-low-range'])
                ptr['src_addr_range_high'] = str(rule['source-address-range-entry']['rule-source-address-high-range'])
                ptr['dst_addr_range_low'] = str(rule['destination-address-range-entry']['rule-destination-address-low-range'])
                ptr['dst_addr_range_high'] = str(rule['destination-address-range-entry']['rule-destination-address-high-range'])
                ptr['app'] = str(rule['src-nat-app-entry']['src-nat-application'])
                ptr['action'] = str(rule['source-nat-rule-action-entry']['source-nat-rule-action'])
#check later if it has to be enabled
            #    ptr['per_nat_type'] = str(rule['source-nat-rule-action-entry']['persistent-nat-type'])
            #    ptr['per_map_type'] = str(rule['source-nat-rule-action-entry']['persistent-nat-mapping-type'])

             #   '''
             #   utils.update_data_from_output(ptr, rule, {
             #      'interface-name': 'if_name',
             #       'service-set-name': 'ss_name',
             #       'rule-name': 'rule_name',
             #       'rule-set-name': 'rs_name',
             #   })
             #   '''

                self.log('INFO', "NAT Rule Set : {} NAT Rule : {}".format(rule_sets, self.data['nat_rule_set'][rule_sets][rule_name]))

        return self.fn_checkout(True)

    def verify_usf_nat_rule(self, rs_name=None, r_name=None, **kwargs):
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

        self._get_tg_port_and_config_mapping(**kwargs)
        #self._get_ss_from_pool()

        self.get_usf_nat_rule(rs_name, r_name)

        result = True
        rs_names = [rs_name] if rs_name is not None else self.nat_rule_set.keys()
        r_names = [r_name] if r_name is not None else self.nat_rule_set[rs_name].keys()

        #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        for rs_name in rs_names:
            for r_name in r_names:
                self.log('INFO', "Verifying details for Rule Set : {}, Rule, {}".format(rs_name, r_name))

                rule_data = self.data['nat_rule_set'][rs_name][r_name]

            exp_data = {
                'app': 'configured', 'per_nat_type': 'N/A',
                'per_map_type': 'address-port-mapping'
                }
            #iputils.iputils.get_network_address is not defined:
            #iputils.get_broadcast_address  is not defined:
            #verify later if this block is necessary
#############
            #if 'src_addr' in self.nat_rule_set[rs_name][r_name]:
            #    src_addr = self.nat_rule_set[rs_name][r_name]['src_addr']
            #    exp_data['src_addr_range_low'] = iputils.get_network_address(src_addr)
            #    exp_data['src_addr_range_high'] = iputils.get_broadcast_address(src_addr)

            #if 'dst_addr' in self.nat_rule_set[rs_name][r_name]:
            #    dst_addr = self.nat_rule_set[rs_name][r_name]['dst_addr']
            #    exp_data['dst_addr_range_low'] = iputils.get_network_address(dst_addr)
            #    exp_data['dst_addr_range_high'] = iputils.get_broadcast_address(dst_addr)
            #exp_data['spic'] = self.ss_map['nat_rule_set']
#############
            exp_data['sset'] = self.ss_map['nat_rule_set'][rs_name]
            exp_data['rule'] = r_name
            exp_data['rule_set'] = rs_name

            for key in kwargs:
                if 'tg_sess' in key:
                    continue
                exp_data[key] = kwargs[key]

            self.log('INFO', "Verifying expected({}) and actual({}) data".format(exp_data,
                                                                                 rule_data))
            if utils.cmp_dicts(exp_data, rule_data):
                self.log('INFO', "Verification details for pool, {}, PASSED".format(r_name))
            else:
                self.log('INFO', "Verification for pool, {}, FAILED".format(r_name))
                result = False

        return self.fn_checkout(result)

    def verify_nat_rule(self, name, expected_output, **kwargs):
        """Verify NAT rule

        :param string name:
          **OPTIONAL** Name of NAT rule.

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.verify_nat_rule(name='nat_rule1', nat_type='source')

            Robot:
                hCgn.Verify NAT Rule   name=nat_rule1    nat_type=source
        """

        self.fn_checkin("Verifying NAT rule")

        self.nat_type = kwargs.get('nat_type', self.nat_type)

        if self.nat_type == 'source':
            _xpath = 'source-nat-rule-detail-information/source-nat-rule-entry'
        elif self.nat_type == 'destination':
            _xpath = 'destination-nat-rule-information/destination-nat-rule-entry'
        cmd = 'show services nat {} rule {}'.format(self.nat_type, name)
        entry = self.get_xml_output(cmd, xpath=_xpath)
        result = True

        entry = self.get_xml_output(cmd, xpath=_xpath)
        nat_rule_dic = {}
        if 'interface-name' in expected_output:
            nat_rule_dic['interface-name'] = entry['interface-name']
        if 'rule-set-name' in expected_output:
            nat_rule_dic['rule-set-name'] = entry['rule-set-name']
        if 'service-set-name' in expected_output:
            nat_rule_dic['service-set-name'] = entry['service-set-name']
        if 'rule-source-address-low-range' in expected_output:
            range_entry = "source-address-range-entry" if self.nat_type == 'source' else 'rule-source-address-range-entry'
            nat_rule_dic['rule-source-address-low-range'] = entry[range_entry]['rule-source-address-low-range']
        if 'rule-source-address-high-range' in expected_output:
            range_entry = "source-address-range-entry" if self.nat_type == 'source' else 'rule-source-address-range-entry'
            nat_rule_dic['rule-source-address-high-range'] = entry[range_entry]['rule-source-address-high-range']
        if 'rule-source-address' in expected_output:
            range_entry = "source-address-range-entry" if self.nat_type == 'source' else 'rule-source-address-range-entry'
            nat_rule_dic['rule-source-address'] = entry[range_entry]['rule-source-address']
        if 'rule-destination-address-low-range' in expected_output:
            range_entry = "destination-address-range-entry" if self.nat_type == 'source' else 'rule-destination-address-range-entry'
            nat_rule_dic['rule-destination-address-low-range'] = entry[range_entry]['rule-destination-address-low-range']
        if 'rule-destination-address' in expected_output:
            range_entry = "destination-address-range-entry" if self.nat_type == 'source' else 'rule-destination-address-range-entry'
            nat_rule_dic['rule-destination-address'] = entry[range_entry]['rule-destination-address']
        if 'rule-destination-address-high-range' in expected_output:
            range_entry = "destination-address-range-entry" if self.nat_type == 'source' else 'rule-destination-address-range-entry'
            nat_rule_dic['rule-destination-address-high-range'] = entry[range_entry]['rule-destination-address-high-range']

        if utils.cmp_dicts(nat_rule_dic, expected_output):
            self.log('INFO', "Verification details for rule, {}, PASSED".format(name))
        else:
            self.log('INFO', "Verification for rule, {}, FAILED".format(name))
            result = False

        return self.fn_checkout(result)


    def verify_nat_pool(self, name, expected_output, **kwargs):
        """Verify NAT pool

        :param string name:
            **OPTIONAL** Name of NAT pool.

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.verify_nat_pool(name='nat_pool1', nat_type='source')

            Robot:
                hCgn.Verify NAT Rule   name=nat_pool1    nat_type=source
        """

        self.fn_checkin("Verifying NAT pool")
        result = True
        self.nat_type = kwargs.get('nat_type', self.nat_type)

        if self.nat_type == 'source':
            _xpath = '{}-nat-pool-detail-information/{}-nat-pool-info-entry'.format(self.nat_type, self.nat_type)
        elif self.nat_type == 'destination':
            _xpath = '{}-nat-pool-information/{}-nat-pool-entry'.format(self.nat_type, self.nat_type)

        cmd = 'show services nat {} pool {}'.format(self.nat_type, name)
        entry = self.get_xml_output(cmd, xpath=_xpath)

        nat_pool_dic = {}
        if 'interface-name' in expected_output:
            nat_pool_dic['interface-name'] = entry['interface-name']
        if 'service-set-name' in expected_output:
            nat_pool_dic['pool-name'] = entry['pool-name']
        if 'service-set-name' in expected_output:
            nat_pool_dic['service-set-name'] = entry['service-set-name']
        if 'address-range-high' in expected_output:
            range_name = 'source-pool-address-range' if self.nat_type == 'source' else 'pool-address-range'
            nat_pool_dic['address-range-high'] = entry[range_name]['address-range-high']
        if 'address-range-low' in expected_output:
            range_name = 'source-pool-address-range' if self.nat_type == 'source' else 'pool-address-range'
            nat_pool_dic['address-range-low'] = entry[range_name]['address-range-low']
        if 'total-pool-address' in expected_output:
            nat_pool_dic['total-pool-address'] = entry['total-pool-address']
        if utils.cmp_dicts(nat_pool_dic, expected_output):
            self.log('INFO', "Verification details for pool, {}, PASSED".format(name))
        else:
            self.log('INFO', "Verification for pool, {}, FAILED".format(name))
            result = False

        return self.fn_checkout(result)

    def verify_clear_commands_for_nat(self, **kwargs):
        """Verify clear commands for NAT

        :param nat_type:
            **REQUIRED** Type of NAT

        :param pool_name:
            **OPTIONAL** NAT pool name

        :param rule_name:
           **OPTIONAL** NAT rule name


        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.verify_clear_commands_for_nat(nat_type='source', pool_name='src_pool1')
            Robot:
                hCgn.Verify Clear Commands For Nat   nat_type=source

        """
        self.fn_checkin("Verify clear commands for NAT")
        self.pool_name = kwargs.get('pool_name', self.pool_name)
        self.rule_name = kwargs.get('rule_name', self.rule_name)
        self.nat_type = kwargs.get('nat_type', self.nat_type)
        result = True

        if self.pool_name:
            if self.nat_type == 'source':
                _xpath = '{}-nat-pool-detail-information/{}-nat-pool-info-entry'.format(self.nat_type, self.nat_type)
            elif self.nat_type == 'destination':
                _xpath = '{}-nat-pool-information/{}-nat-pool-entry'.format(self.nat_type, self.nat_type)
            cmd = 'show services nat {} pool {}'.format(self.nat_type, self.pool_name)
            entry = self.get_xml_output(cmd, xpath=_xpath)
            if entry['address-pool-hits'] != '0':
                result = False
        if self.rule_name:
            if self.nat_type == "source":
                _xpath = '{}-nat-rule-detail-information/{}-nat-rule-entry'.format(self.nat_type, self.nat_type)
                cmd = 'show services nat {} rule {}'.format(self.nat_type, self.rule_name)
                entry = self.get_xml_output(cmd, xpath=_xpath)

                if entry['source-nat-rule-hits-entry']['failed-hits'] != '0'           or\
                   entry['source-nat-rule-hits-entry']['rule-translation-hits'] != '0' or\
                   entry['source-nat-rule-hits-entry']['succ-hits'] != '0':
                    self.log('INFO', "Verification for clear commands for rule_name {}, FAILED".format(self.rule_name))
                    result = False
            else:
                _xpath = '{}-nat-rule-information/{}-nat-rule-entry'.format(self.nat_type, self.nat_type)
                cmd = 'show services nat {} rule {}'.format(self.nat_type, self.rule_name)
                entry = self.get_xml_output(cmd, xpath=_xpath)
                if self.nat_type == "destination" and\
                   entry['failed-hits'] != '0'           or\
                   entry['rule-translation-hits'] != '0' or\
                   entry['succ-hits'] != '0':
                    self.log('INFO', "Verification for clear commands for rule_name {}, FAILED".format(self.rule_name))
                    result = False
        return self.fn_checkout(result)

    def verify_session_count(self, **kwargs):
        """Verify session count for protocol

        :param application_dict:
            **REQUIRED** List of all applications to be verified

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.verify_session_count(application_dict='udp')
            Robot:
                hCgn.Verify Session Count    application_dict=${applicatoin_dict}

        """
        self.fn_checkin("Verify session count for the given application")
        self.application_dict = kwargs.get('application_dict', self.application_dict)
        result = True

        for protocol, value in  self.application_dict.items():
            _xpath = 'usf-session-count-information/usf-session-count'
            cmd = 'show services sessions count protocol {}'.format(protocol)
            entry = self.get_xml_output(cmd, xpath=_xpath)
            if entry['valid-session-count'] != value:
                result = False

        return self.fn_checkout(result)


    def verify_static_routes_in_routing_instances(self, **kwargs):
        """Verify if static routes are added in routing instances

        :param vrf_dict:
            **REQUIRED** Dictionary that has vrf-name as key and a list that has static route details

        :param transport:
            **REQUIRED** String that tells if the transport is v4 or v6

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                hCgn.verify_routing_instances(vrf_dict={'client_vrf1':['0.0.0.0/0','vms-0/2/0.1']})
            Robot:
                hCgn.Verify Routing Instances    vrf_dict=${vrf_dict}

        """
        self.fn_checkin("Verify if static routes are added correctly in VRFs given")
        self.vrf_dict = kwargs.get('vrf_dict', self.vrf_dict)
        self.transport = kwargs.get('transport', self.transport)
        result = True

        for vrf in self.vrf_dict.keys():
            _xpath = 'configuration/routing-instances/instance/routing-options/static/route'
            if self.transport == "v6":
                _xpath = 'configuration/routing-instances/instance/routing-options/rib/static/route'
            cmd = 'show configuration routing-instances {}'.format(vrf)
            entry = self.get_xml_output(cmd, xpath=_xpath)
            print("Entry", entry)
            if entry['name'] != self.vrf_dict[vrf][0] or \
               entry['next-hop'] != self.vrf_dict[vrf][1]:
                result = False
        return self.fn_checkout(result)

