"""Module contains methods for PCP"""
# p-ylint: disable=undefined-variable
# p-ylint: disable=invalid-name
__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import random

from jnpr.toby.utils import iputils

from jnpr.toby.services.cgnat import cgnat
from jnpr.toby.services import utils

class pcp(cgnat):
    """Class contains methods for PCP"""

    def __init__(self, **kwargs):
        """Constructor method for PCP class"""

        super().__init__(**kwargs)

        self.cmd_list = []
        self.pcp_rule = {}
        self.pcp_server = {}

        self.cmd = None
        self.ptr = None

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def _update(self, kwargs):
        """Update the object with the parameters passed"""

        for attr in kwargs:
            self.ptr[attr] = kwargs[attr]

    def set_pcp_rule(self, name='pcp_rule', **kwargs):
        """Configure PCP rule and other parameters

        Use the optional argument, 'count', to generate scaling config.
        For example, This will create 10 PCP rules from pcp_rule1 to pcp_rule9
            set_pcp_rule(name='pcp_rule', count=10)

        :param string name:
            **OPTIONAL** Name of PCP rule to be configured. Default is 'pcp_rule'

 	:param string action:
            **OPTIONAL** Valid values are set, delete, activate, deactivate. Default is 'set'

 	:param int count:
            **OPTIONAL** Number of PCP Rules. Default is 1

	:param int term:
            **OPTIONAL** Term name. Default is 0

        :param bool term_idx_reset:
            **OPTIONAL** Whether to reset term index for every rule. Default is False.

        :param string dir:
            **OPTIONAL** Rule direction. Default is 'input'

 	:param int num_terms:
            **OPTIONAL** Number of terms. Default is 1

        :param string pcp_server:
            **OPTIONAL** PCP Server name

 	:param string src_addr:
            **OPTIONAL** From Source IP Address. Default is None

 	:param int src_addr_nw_step:
            **OPTIONAL** Number by which source network address will be incremented. Default is 1

        Example::

            Python:
                pcp.set_pcp_rule(name='rule1')
                pcp.set_pcp_rule()
            Robot:
                pcp.Set PCP Rule   name=rule1
                pcp.Set PCP Rule
        """

        self.fn_checkin("Configuring PCP rule")

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'dir': 'input',
                                               'term': 0, 'num_terms': 1, 'term_idx_reset': False,
                                               'src_addr': None, 'src_addr_nw_step': 1
                                           })

        src_addr = this['src_addr']
        term = this['term']

        src_addr_cntr = 0

        for iter_rule in range(1, this['count']+1):
            rule_tag = name + str(iter_rule)
            if rule_tag not in self.pcp_rule:
                self.pcp_rule[rule_tag] = {}
            self.ptr = self.pcp_rule[rule_tag]
            # Update this config in the object for this rule
            self._update(this)

            self.cmd = "{} services pcp rule {}".format(this['action'], rule_tag)

            self.cmd_add("match-direction", 'dir')

            if this['term_idx_reset']:
                term = this['term']

            for _ in range(0, this['num_terms']):
                self.cmd = "{} services pcp rule {} term {}".format(this['action'], rule_tag, term)

                if src_addr is not None:
                    self.cmd_add("from source-address {}".format(src_addr))
                    self.ptr['src_addr'] = src_addr
                    src_addr_cntr += 1
                    src_addr = iputils.incr_ip_subnet(src_addr, this['src_addr_nw_step'])

                self.cmd_add("then pcp-server", 'pcp_server', tag=iter_rule)

                term += 1

        return self.fn_checkout(self.config())

    def set_pcp_server(self, name='pcp_server', **kwargs):
        """Configure PCP Server based on parameters passed

        Use the optional argument, 'count', to generate scaling config.

        :param string name:
            **OPTIONAL** Name of PCP Server to be configured. Default is 'pcp_server'

        :param string action:
            **OPTIONAL** Valid values are set,delete,activate,deactivate. Default is 'set'

        :param int count:
            **OPTIONAL** Number of PCP Servers to be configured. Default is 1.

        :param string v4_addr:
            **OPTIONAL** PCP Server IPv4 Address

        :param int v4_addr_nw_step:
            **OPTIONAL** Number by which Server IPv4 Address will be incremented. Default is 1

        :param string v6_addr:
            **OPTIONAL** PCP Server IPv6 Address

        :param int v6_addr_nw_step:
            **OPTIONAL** Number by which Server IPv6 Address will be incremented. Default is 1

        :param int min_map_life:
            **OPTIONAL** Minimum lifetime of a mapping (120-3600s). Default is 120

        :param int max_map_life:
            **OPTIONAL** Maximum lifetime of a mapping (120-2147483647s). Default is 300

        :param int max_clnt_maps:
            **OPTIONAL** Maximum mappings permitted per client (1..128). Default is 128

        :param list pcp_options_list:
            **OPTIONAL** PCP Server Options

        :param string sw_concentrator:
            **OPTIONAL** Softwire DS-Lite concentrator

        :param int pcp_nat_pool_name:
            **OPTIONAL** Point NAT POOL under nat options in PCP Server

        Example::

            Python:
                set_pcp_server(name='pcp_server')
            Robot:
                Set PCP Server   name=pcp_server
        """

        self.fn_checkin("Configuring PCP Server")

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'count': 1, 'action': 'set', 'max_clnt_maps': 128,
                                               'min_map_life': 120, 'max_map_life': 300,
                                               'v4_addr': None, 'v6_addr': None,
                                               'v4_addr_nw_step': 1, 'v6_addr_nw_step': 1,
                                           })

        (v4_addr, v6_addr) = (this['v4_addr'], this['v6_addr'])

        for iter_ii in range(1, this['count'] + 1):
            name_tag = name + str(iter_ii)
            if name_tag not in self.pcp_server:
                self.pcp_server[name_tag] = {}
            self.ptr = self.pcp_server[name_tag]
            self._update(this)
            self.cmd = "{} services pcp server {}".format(this['action'], name_tag)

            if v4_addr is not None:
                self.cmd_add("ipv4-address {}".format(iputils.strip_mask(v4_addr)))
                self.ptr['v4_addr'] = v4_addr
                if this['v4_addr_nw_step']:
                    v4_addr = iputils.incr_ip_subnet(this['v4_addr'], this['v4_addr_nw_step'])
            if v6_addr is not None:
                self.cmd_add("ipv6-address {}".format(v6_addr))
                self.ptr['v6_addr'] = v6_addr
                if this['v6_addr_nw_step']:
                    v6_addr = iputils.incr_ip_subnet(this['v6_addr'], this['v6_addr_nw_step'])

            self.cmd_add("softwire-concentrator", 'sw_concentrator')
            self.cmd_add("max-mappings-per-client", 'max_clnt_maps')
            self.cmd_add("mapping-lifetime-minimum", 'min_map_life')
            self.cmd_add("mapping-lifetime-maximum", 'max_map_life')

            self.cmd_add("pcp-options", 'pcp_options_list')
            self.cmd_add("nat-options pool", 'pcp_nat_pool_name')

            # when the action is not 'set' and there are no other command options to be executed
            if len(self.cmd_list) == 0 and this['action'] != 'set':
                self.cmd_add("")

        return self.fn_checkout(self.config())

    def clear_pcp_statistics(self, intf=None):
        """Clear PCP Statistics of the given interface

        :param string intf:
            **REQUIRED** Interface name

        :returns: True or raises an exception

        :rtype: bool

        Example::

            Python:
                obj.clear_pcp_statistics(intf='ms-1/0/0')
            Robot:
                obj.Clear PCP Statistics   intf='ms-1/0/0

        """

        if intf is None:
            raise self.MissingMandatoryArgument('intf')

        return self.dh.cli(command="clear services pcp statistics interface {}".format(intf))

    def verify(self, **kwargs):
        """Wrapper for minimum verifications to be done for PCP

        This will call services.verify() to do all basic Services verifications required.

        :return: True if successful else False

        :rtype: bool

        Example::

            Python:
                pcp.verify()
            Robot:
                pcp.Verify
        """

        self.fn_checkin("Verifying PCP")

        super().verify(**kwargs)

        # self.verify_pcp_mappings(**kwargs)

        self.fn_checkout()

    def get_pcp_mappings(self):
        """Return PCP mappings as dictionary

        PCP mappings output is parsed and dictionary is returned.
        An exception will be raised if there's no output.

        :return: Dictionary containing the PCP mappings data

        :rtype: dict

        Example::

            Python:
                pcp.get_pcp_mappings()
            Robot:
                pcp.Get PCP Mappings
        """

        self.fn_checkin("Retrieving PCP mappings")

        output = self.dh.cli(command="show services nat mappings pcp")
        if len(output.splitlines()) < 2:
            self.fn_checkout(False, "No valid output found")

        mapping = {}

        (spic, sset, nat_pool, pcp_ip, pcp_lifetime) = (None, None, None, None, None)

        self.data['pcp_maps'] = data = self.dd()

        for line in output.splitlines():
            if len(line) <= 2:
                continue

            match = re.search(r'Interface:\s*(.*), Service set:\s*(.*)', line, re.IGNORECASE)
            if match:
                spic, sset = match.group(1), match.group(2)
                self.log('INFO', 'Service pics:{} Service set:{}'.format(spic, sset))
                pcp_ip = None
                continue

            match = re.search(r'NAT pool:\s*(.*)', line, re.IGNORECASE)
            if match:
                nat_pool = match.group(1)
                continue

            match = re.search(r'PCP Client\s*:\s*(' + utils.get_regex_ip() + \
                              r')\s*PCP lifetime\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                pcp_ip = match.group(1)
                if iputils.is_ip_ipv6(pcp_ip):
                    pcp_ip = iputils.normalize_ipv6(pcp_ip)
                pcp_lifetime = match.group(1)
                continue

            match = re.search(r'Mapping\s*:\s*(' + utils.get_regex_ip() + \
                              r')\s*:\s*(\d+)\s*-->\s*(' + utils.get_regex_ip() + \
                              r')\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                int_ip, int_port = match.group(1), match.group(2)
                if pcp_ip is not None:
                    mapping = data[spic][sset][nat_pool][pcp_ip][int_ip][int_port] = {}
                    mapping['pcp_lifetime'] = pcp_lifetime
                else:
                    mapping = data[spic][sset][nat_pool][int_ip][int_port] = {}
                if iputils.is_ip_ipv6(int_ip):
                    int_ip = iputils.normalize_ipv6(int_ip)
                mapping['nat_ip'] = match.group(3)
                mapping['nat_port'] = match.group(4)
                continue

            match = re.search(r'Session Count\s*:\s*(\d+)', line, re.IGNORECASE)
            if match:
                mapping['sess_cnt'] = match.group(1)
                continue

            match = re.search(r'Mapping State\s*:\s+(\w+)', line, re.IGNORECASE)
            if match:
                mapping['state'] = match.group(1).lower()
                continue

            match = re.search(r'B4 Address\s+:\s+(' + utils.get_regex_ip() + ')', line,
                              re.IGNORECASE)
            if match:
                mapping['b4_ip'] = iputils.normalize_ipv6(match.group(1))
                continue

        self.log('INFO', 'PCP Mappings dump : {}'.format(data))

        self.fn_checkout()

        return data

    def verify_pcp_mappings(self, **kwargs):
        """Verify PCP mappings

        Fetches PCP data from the output by calling get_pcp_mappings.
        This data is verified against the data fetched from configuration and traffic generator.
        Number of mappings to be verified can be limited by 'limit' or 'limit_perc'.
        Random mappings, to be verified, are picked from sessions to be sent by TG.

        :param int limit:
            **OPTIONAL** Number of mappings to be verified.

        :param int limit_perc:
            **OPTIONAL** Percentage number of mappings to be verified. Default is 1

        :return: True on successful verification else False

        :rtype: bool

        Example::

            Python:
                pcp.verify_pcp_mappings()
            Robot:
                pcp.Verify PCP Mappings
        """

        self.fn_checkin("Verifying PCP mappings")

        result = True

        # Fetch PCP Mappings output as dictionary
        act_data = self.get_pcp_mappings()

        self._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            # Iterate over list of random mappings indices
            for req_idx in _cfg_map['rand_reqs_idx_list']:
                # We need to verify if theres a mapping for this session on the router
                _tg_data = self.tg_sess[tg_if]['pcp_maps_list'][req_idx]
                ext_port = _tg_data['ext_port']

                flow = self._get_pcp_ip_port_flow_from_data(_tg_data, _cfg_map, act_data)

                if flow is None or ('nat_ip' in flow and flow['nat_ip'] is None):
                    continue

                if not iputils.cmp_ip(_tg_data['ext_ip'], flow['nat_ip']):
                    result = False
                    continue

                result &= utils.cmp_dicts(exp_data={'state': 'active', 'nat_port': ext_port},
                                          act_data=flow)

        return self.fn_checkout(result)

    def get_pcp_statistics(self, spic=None, timeout=300):
        """Fetch PCP statistics as dictionary

        :param string spic:
            **REQUIRED** Service PIC interface

        :param int timeout:
            **OPTIONAL** Cli command timeout. Default is 300

        :return: Dictionary containing the PCP statistics data

        :rtype: dict

        Example::

            Python:
                pcp.get_pcp_statistics()
            Robot:
                pcp.Get PCP Statistics
        """

        self.fn_checkin("Retrieving PCP statistics")

        if spic is None:
            raise self.MissingMandatoryArgument('spic')

        cmd = 'show services pcp statistics interface ' + spic

        entry = self.get_xml_output(cmd=cmd, xpath='service-pcp-statistics-information',
                                    want_list=False, timeout=timeout)

        self.data['pcp_statistics'] = data = self.dd()
        data['spic'] = entry['flow-analysis-statistics-pic-info']['pic-name']
        entry = entry['pcp-protocol-statistics']

        utils.update_data_from_output(data, entry, {
            'map-request-received': 'map_req_rx',
            'peer-request-received': 'peer_req_rx',
            'other-operational-counters': 'other_oper_cntrs',
            'unprocessed-requests-received': 'unproc_reqs_rx',
            'third-party-requests-received': '3rd_party_reqs_rx',
            'prefer-fail-options-received': 'prefer_fail_opts_rx',
            'filter-option-received': 'filter_opt_rx',
            'other-options-counters': 'other_opts_cntrs',
            'option-optional-received': 'opt_optl_rx',
            'pcp-success': 'pcp_success',
            'pcp-unsupported-version': 'pcp_unsupp_ver',
            'not-authorized': 'not_auth',
            'bad-requests': 'bad_reqs',
            'unsupported-opcode': 'unsupp_opcode',
            'unsupported-option': 'unsupp_opt',
            'bad-option': 'bad_opt',
            'network-failure': 'nw_fail',
            'out-of-resources': 'out_of_res',
            'unsupported-protocol': 'unsupp_proto',
            'user-exceeded-quota': 'user_xcd_quota',
            'cannot-provide-external': 'cant_ext',
            'address-mismatch': 'addr_mismatch',
            'excessive-number-of-remote-peers': 'xcess_num_rmt_peers',
            'processing-error': 'proc_err',
            'other-result-counters': 'other_result_cntrs',
        })

        self.log('DEBUG', 'PCP statistics: {}'.format(data))

        self.fn_checkout()

        return data

    def verify_pcp_statistics(self, other_stats_zero=True, **kwargs):
        """Verify PCP statistics

        :param bool other_stats_zero:
            **OPTIONAL** Except for the stats passed, other stats will be default to 0.
                Default is False

        :return: True on successful verification else False

        :rtype: bool

        Example::

            Python:
                pcp.verify_pcp_statistics()
            Robot:
                pcp.Verify PCP Statistics
        """

        self.fn_checkin("Verifying PCP statistics")

        result = True

        self._get_tg_port_and_config_mapping(**kwargs)

        for spic in self.tg_sess_cnt:
            act_data = self.get_pcp_statistics(spic, **kwargs)
            exp_data = {}
            exp_data['map_req_rx'] = self.tg_sess_cnt[spic]['total_pcp_reqs']
            exp_data['pcp_success'] = self.tg_sess_cnt[spic]['total_pcp_reqs']
            for key in act_data:
                if key in kwargs:
                    exp_data[key] = kwargs[key]
                elif other_stats_zero:
                    exp_data[key] = 0
            result &= utils.cmp_dicts(exp_data=exp_data, act_data=act_data)

            result &= utils.cmp_dicts(exp_data=exp_data, act_data=act_data)

        return self.fn_checkout(result)

    def get_pcp_debug_statistics(self, spic=None, timeout=300):
        """Fetch PCP debug statistics as dictionary

        :param string spic:
            **REQUIRED** Service PIC interface

        :param int timeout:
            **OPTIONAL** Cli command timeout. Default is 300

        :return: Dictionary containing the PCP statistics data

        :rtype: dict

        Example::

            Python:
                pcp.get_pcp_debug_statistics()
            Robot:
                pcp.Get PCP Debug Statistics
        """

        self.fn_checkin("Retrieving PCP Debug statistics")

        if spic is None:
            raise self.MissingMandatoryArgument('spic')

        cmd = 'show services pcp statistics debug interface ' + spic

        entry = self.get_xml_output(cmd=cmd, xpath='service-pcp-statistics-information',
                                    want_list=False, timeout=timeout)

        self.data['pcp_stats_dbg'] = data = self.dd()
        data['spic'] = entry['flow-analysis-statistics-pic-info']['pic-name']
        entry = entry['pcp-debug-statistics']

        for key in entry:
            tmp_key = key
            tmp_key = tmp_key.replace('-', '_')
            data[tmp_key] = entry[key]

        self.log('DEBUG', 'PCP debug statistics: {}'.format(data))

        self.fn_checkout()

        return data

    def verify_pcp_debug_statistics(self, other_stats_zero=False, **kwargs):
        """Verify PCP Debug statistics

        :param bool other_stats_zero:
            **OPTIONAL** Except for the stats passed, Default other stats to 0.
            Default is False

        :return: True on successful verification else False

        :rtype: bool

        Example::

            Python:
                pcp.verify_pcp_debug_statistics()
            Robot:
                pcp.Verify PCP Debug Statistics
        """

        self.fn_checkin("Verifying PCP Debug statistics")

        result = True

        self._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_cfg_map:
            _cfg_map = self.tg_cfg_map[tg_if]
            act_data = self.get_pcp_debug_statistics(_cfg_map['spic'], **kwargs)
            exp_data = {}
            for key in act_data:
                if key in kwargs:
                    exp_data[key] = kwargs[key]
                elif other_stats_zero:
                    exp_data[key] = 0

            result &= utils.cmp_dicts(exp_data=exp_data, act_data=act_data)

        return self.fn_checkout(result)

    def _get_tg_port_and_config_mapping(self, **kwargs):
        """Determines sp,sset,rule,pool etc. thats going to service traffic for every tg port"""

        self.fn_checkin("Mapping TG Port and config")

        limit = kwargs.get('limit', None)
        limit_perc = kwargs.get('limit_perc', 1)

        if self.tg_sess_cnt is None:
            super()._get_tg_port_and_config_mapping(**kwargs)

        for tg_if in self.tg_sess:
            _conf_map = self.tg_cfg_map[tg_if]
            spic = _conf_map['spic']
            #_pcp_reqs = _conf_map['total_pcp_reqs'] = self.tg_sess[tg_if]['total_pcp_reqs']

            _max_reqs = _conf_map['total_pcp_reqs'] = self.tg_sess[tg_if]['total_pcp_reqs']
            if self.tg_sess_cnt is not None:
                self.tg_sess_cnt[spic]['total_pcp_reqs'] = _max_reqs

            if _max_reqs < 100:
                limit_perc = 100
            limit_num = int(float(_max_reqs) * (limit_perc / 100))
            if limit is not None:
                limit_num = limit
            # Pick random numbers
            _conf_map['rand_reqs_idx_list'] = random.sample(range(_max_reqs), limit_num)

        self.fn_checkout()

        #def _get_pcp_ip_port_flow_from_data(self, pcp_ip, int_ip, int_port, cfg_map, data):
    def _get_pcp_ip_port_flow_from_data(self, tg_data, cfg_map, data):
        """Return mapping from the actual data for the given Source ip and port.
        Service pic, service set, NAT pool are picked from the configuration map
        created by _get_tg_port_and_config_mapping
        """

        pcp_ip, int_ip, int_port = [tg_data[key] for key in ['pcp_ip', 'int_ip', 'int_port']]
        spic, sset, nat_pool = [cfg_map[key] for key in ['spic', 'sset', 'nat_pool']]
        _msg = "Flow(spic={}, sset={}, pool={}".format(spic, sset, nat_pool)
        _msg += ", pcp={}, int_ip={}, int_port={})".format(pcp_ip, int_ip, int_port)
        self.fn_checkin("Finding {}".format(_msg))
        self.log("Actual data: {}".format(data))
        try:
            _flow = data[spic][sset][nat_pool][pcp_ip][int_ip][int_port]
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

        nat_ip = None
        if 'nat_ip' in flow:
            nat_ip = flow['nat_ip']
        if 'eim_nat_ip' in flow:
            # NAT IP is saved as eim_nat_ip in nat mappings detail
            nat_ip = flow['eim_nat_ip']
        if nat_ip is None:
            self.log("nat_ip is not there in the flow({})".format(flow))
            return False

        act_nat_ip_str = "Actual NAT IP({})".format(nat_ip)
        nat_ip_str = "within expected NAT Pool({})".format(cfg_map['nat_ip'])
        if not iputils.is_ip_in_subnet(nat_ip, cfg_map['nat_ip']):
            self.log('ERROR', '{} is **NOT** {}'.format(act_nat_ip_str, nat_ip_str))
            return False

        self.log('INFO', '{} **IS** {}'.format(act_nat_ip_str, nat_ip_str))

        return True

    def _is_nat_port_in_pool(self, flow, cfg_map):
        """Verify if actual NAT Port is with in NAT Pool port range"""

        nat_port = None
        if 'nat_port' not in cfg_map or cfg_map['nat_port'] is None:
            self.log('ERROR', "nat_port is not there in the config({})".format(cfg_map))
            return False

        if 'nat_port' in flow:
            nat_port = flow['nat_port']
        if 'eim_nat_port' in flow:
            # NAT Port is saved as eim_nat_port in nat mappings detail
            nat_port = flow['eim_nat_port']

        if nat_port is None:
            self.log("nat_port is not there in the flow({})".format(flow))
            return False

        _act_port_str = "Actual NAT Port({})".format(nat_port)
        _range_str = "within expected NAT Pool Port Range({})".format(cfg_map['nat_port'])
        self.log('INFO', "Verifying if {} is {}".format(_act_port_str, _range_str))
        if nat_port > cfg_map['nat_port_low'] and nat_port < cfg_map['nat_port_high']:
            self.log('INFO', '{} **IS** {}'.format(_act_port_str, _range_str))
            return True

        self.log('ERROR', '{} is **NOT** {}'.format(_act_port_str, _range_str))

        return False

    """
    def _get_regex_match_vals(self, ptrn, line, flag=re.IGNORECASE):
        match = re.search(ptrn, line, flag)
        if match:
            return match.groups()
        else:
            return None
    """
