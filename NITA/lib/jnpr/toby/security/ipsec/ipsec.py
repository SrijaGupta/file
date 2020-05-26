"""
IPSec class and ROBOT keywords functions
"""

from jnpr.toby.utils.iputils import *
import time

class IPSec:
    """
    Class factory to configure  vpn
    """

    def __init__(self, device_handle, **kwargs):
        """
            Intializes vpn object based on remote gateway
            and sp interface

            :param device_handle:
                **REQUIRED** device object
            :param svc_intf:
                **REQUIRED** service interface
            :param ss:
                **OPTIONAL** service set name
                Default is ipsec_ss1
            :param local_gw:
                **REQUIRED**  Local IP address for IKE negotiations
            :param remote_gw:
                **REQUIRED**  Remote IP address of the peer
            :param vpn_name:
                **OPTIONAL** vpn rule name
                Default is vpn_rule1
            :param tunnels:
                *OPTIONAL*  Number of tunnels. Default is 1
            :param num_terms:
                *OPTIONAL*  Number of terms per rule
                 Default is 1
            :param num_rules:
                *OPTIONAL* Number of rules.
                Default is 1
            :param ipsec_policy:
                *OPTIONAL* IPSec Policy Name
                Default is ipsec_policy
            :param ipsec_proposal:
                *OPTIONAL* IPSec Proposal Name
                Default is ipsec_prop
            :param ike_profile:
                *OPTIONAL* IKE Profile Name
                Default is ike_access
            :param ike_proposal:
                *OPTIONAL* IKE Proposal Name
                Default is ike_proposal
            :param ike_policy:
                *OPTIONAL* IKE Policy Name
                Default is ike_policy
            :param ike_auth:
                *OPTIONAL* IKE Authentication type
                Default is 'pre-shared-keys'
            :param ike_version:
                *OPTIONAL* IKE Version
                Default is 2
            :param ike_mode:
                *OPTIONAL* IKE Mode
                Default is 'main'
                Supported values main/aggresive
            :param ike_clnt:
                *OPTIONAL* IKE Client
                 Default is '*'
            :param ike_group:
                *OPTIONAL*  Define Diffie-Hellman group
                Default is 'group2'
            :param group_name:
                *OPTIONAL* Group Name
                Default  is 'ipsec-changes'
            :param protocol:
                *OPTIONAL* Protocol [ESP|AH]
                Default is 'esp'
            :param ipsec_auth_algo:
                *OPTIONAL* Authentication algorithm for IPSec
                Default is 'hmac-sha1-96'
            :param ipsec_encr_algo:
                *OPTIONAL*Encryption algorithm for IPSec
                Default is '3des-cbc'
            :param ike_auth_algo:
                *OPTIONAL* IKE Authentication algorithm:
                Default is 'sha1'
            :param ike_encr_algo:
                *OPTIONAL* IKE Encryption algorithm
                Default is '3des-cbc'
            :param estd_tun:
                *OPTIONAL* Establish tunnels immediately. default is 0
                Supported values 0/1
            :return: IPSec object
            EXAMPLE::
             Python:

             ipsec_obj = IPSec(dev_obj,svc_intf='ms-1/0/0',local_gw='10.0.1.1',
                          remote_gw='10.0.1.2',ext_intf='ge-0/2/1')

             Robot:

               ${ipsec_obj} =  Create Ipsec Object  ${dh0}  local_gw=${t['resources']['r0']['interfaces']['r0-r1']['uv-ip']}
                              remote_gw=${t['resources']['r1']['interfaces']['r0-r1']['uv-ip']}  svc_intf=${t['resources']['r0']['interfaces']['r0-ms0-0']['pic']}

        """

        self.dh = device_handle
        if 'svc_intf' in kwargs:
            self.svc_intf = kwargs.get('svc_intf')
        else:
            raise Exception("'svc_intf' parameter is mandatory")

        self.ss = kwargs.get('ss', 'ipsec_ss')
        self.ike_gw = kwargs.get('ike_gw', "ike_gateway_")
        self.vpn_name = kwargs.get('vpn_name', 'vpn_')
        self.local_gw = kwargs.get('local_gw', 0)
        self.remote_gw = kwargs.get('remote_gw', 0)
        #self.ext_intf = kwargs.get('ext_intf')
        self.tunnels = int(kwargs.get('tunnels', 1))
        self.num_terms = kwargs.get('num_terms', 1)
        self.num_rules = kwargs.get('num_rules', 1)
        self.ipsec_policy = kwargs.get('ipsec_policy', 'ipsec_policy')
        self.ipsec_proposal = kwargs.get('ipsec_proposal', 'ipsec_prop')
        self.ike_profile = kwargs.get('ike_profile', 'ike_access')
        self.ike_proposal = kwargs.get('ike_proposal', 'ike_proposal')
        self.ike_policy = kwargs.get('ike_policy', 'ike_policy')
        self.ike_auth = kwargs.get('ike_auth', 'pre-shared-keys')
        self.ike_version = str(kwargs.get('ike_version', '2'))
        self.ike_mode = kwargs.get('ike_mode', 'main')
        self.ike_clnt = kwargs.get('ike_clnt', '*')
        self.ike_group = kwargs.get('ike_group', 'group2')
        self.if_id = kwargs.get('if_id', 'if_id')
        # self.vpn_rule = kwargs.get('vpn_rule','vpn_rule')
        self.group_name = kwargs.get('group_name', 'ipsec_changes')
        self.protocol = kwargs.get('protocol', 'esp')
        self.auth_algo = kwargs.get('ipsec_auth_algo', 'hmac-sha1-96')
        self.encro_algo = kwargs.get('ipsec_encr_algo', '3des-cbc')
        self.ike_auth_algo = kwargs.get('ike_auth_algo', 'sha1')
        self.ike_encr_algo = kwargs.get('ike_encr_algo', '3des-cbc')
        if 'estd_tun' in kwargs: 
            self.estd_tun = kwargs.get('estd_tun')

    def set_access(self, **kwargs):
        """

            :param init_dpd:
                *OPTIONAL* Configure inititiate-dead-peer-detection
                Supported values 1/0
            :param dpd_interval:
                *OPTIONAL* Dead peer detection interval
            :param dpd_threshold:
                *OPTIONAL* Dead peer detection threshold
            :param ipsec_policy:
                *OPTIONAL*  Configure IPSec Policy
                Supported values 1/0
            :param ike_policy:
                *OPTIONAL*   Configure IKE Policy
                Supported values 1/0
            :param apply-groups:
                *OPTIONAL*  Apply groups config to access profile
            :param proxy-pair:
                *OPTIONAL* Configure local and remote proxy pairs
                Eg: [30.0.0.0/16, 80.0.0.0/16]

            :return: True on success, Raise exception on Failure

            EXAMPLE::
                Python:
                    ipsec_obj.set_access()

                Robot:
                    configure access  ${ipsec_obj}

        """
        cmdlist = []
        self.dh.log(" Configuring access profiles for tunnel(s)")
        i = 1
        while i <= self.tunnels:
            access_str = 'set access profile ' + self.ike_profile + str(i) + ' client ' + \
                  self.ike_clnt + ' ike '
            cmdlist.append(access_str + ' pre-shared-key ascii-text ' + self.ascii_key)
            cmdlist.append(access_str + ' interface-id  ' + self.if_id + str(i))
            if 'init_dpd' in kwargs:
                cmdlist.append(access_str + ' initiate-dead-peer-detection')
            if 'dpd_interval' in kwargs:
                cmdlist.append(access_str + ' dead-peer-detection interval ' + \
                               str(kwargs.get('dpd_interval')))
            if 'dpd_threshold' in kwargs:
                cmdlist.append(access_str + ' dead-peer-detection threshold ' + \
                               str(kwargs.get('dpd_threshold')))
            if 'ipsec_policy' in kwargs:
                cmdlist.append(access_str + ' ipsec-policy ' + self.ipsec_policy)
            if 'ike_policy' in kwargs:
                cmdlist.append(access_str + ' ike-policy ' + self.ike_policy)
            if 'proxy_pair' in kwargs:
                cmdlist.append(access_str + ' allowed-proxy-pair local ' + ' remote '.join(kwargs.get('proxy_pair')))
            if 'apply-groups' in kwargs:
                cmdlist.append('set access apply-groups ' + kwargs.get('apply-groups'))
            i = i +1
        try:
            self.dh.log('IPSec config: ' + str(cmdlist))
            if self.tunnels > 5:
                return _load_set_config(self.dh, command_list=cmdlist)
            else:
                return self.dh.config(command_list=cmdlist).status()
        except Exception as error:
            self.dh.log(level="ERROR", message=error)
            raise error

    def set_ipsec_config(self, **kwargs):
        """
            Configure ipsec knob under set services ipsec-vpnm

            :param ipsec_lifetime:
                *OPTIONAL* Ipsec Lifetime, in seconds
                  Range 180..86400 seconds
            :param ipsec_prop_desc:
                *OPTIONAL* Text description of IPSec proposal
            :param ipsec_protocol:
                *OPTIONAL* Define an IPSec protocol for the proposal
                Supported values are ah/esp
            :param ipsec_prop_set:
                *OPTIONAL* Types of default IPSEC proposal-set
                 Supported values are basic/compatible/standard/suiteb-gcm-128/suiteb-gcm-256
            :param estd_tun:
                *OPTIONAL* Establish tunnels immediately. default is 0
                Suppoted values 0/1
            :param ike_lifetime:
                *OPTIONAL* IKE Proposal lifetime in seconds
            :param ascii_text:
                *OPTIONAL*  ascii key for authentication pre-shared key
                Default is "juniper123"
            :param hexa_key:
                *OPTIONAL*  hexa key for authentication pre-shared key
            :param pfs:
                *OPTIONAL* Define perfect forward secrecy
                Supported values group1/group14/group19/group2/
                group20/group24/group5
            :param local_cert:
                *OPTIONAL* Local certificate name if ike_auth specified as rsa
            :param local_id_fqdn:
                *OPTIONAL* Use a fully-qualified domain name in local certificate
            :param local_id_inet:
                *OPTIONAL* Use an IPv4 address
            :param local_id_inet6:
                *OPTIONAL* Use an IPv6 address
            :param local_id_key:
                *OPTIONAL* Use an key-id
            :param remote_id_fqdn:
                *OPTIONAL*  Use a fully-qualified domain name specified in remote certificate
            :param remote_id_inet:
                *OPTIONAL* Use an IPv4 address
            :param remote_id_inet6:
                *OPTIONAL* Use an IPv6 address
            :param remote_id_key_id:
                *OPTIONAL* Use an  key-id
            :param peer_cert_type:
                *OPTIONAL* Peer certificate type
            :param ipsec_trace:
                *OPTIONAL* Trace options for IPSec data-plane debug. Default is All
                 Supported values are next-hop-tunnel-binding/packet-drops/
                 packet-processing/security-associations
            :param ipsec_level:
                *OPTIONAL* ipsec trace level
                Default is 'all'
            :return:
            EXAMPLE::

              Python:
                  ipsec_obj.set_ipsec_config()

              Robot:
                  configure ipsec   ${ipsec_obj}

        """
        self.dh.log("Starting IPSec config")
        #import sys, pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        ipsec_trace = kwargs.get('ipsec_trace', 'all')
        ipsec_level = kwargs.get('ipsec_level', 'all')
        estd_tun = kwargs.get('estd_tun', 0)
        if hasattr(self, 'estd_tun'):
            estd_tun = self.estd_tun
        #self.ts_local_ip = kwargs.get('ts_local_ip')
        #self.ts_remote_ip = kwargs.get('ts_remote_ip')
        self.ascii_key = kwargs.get('ascii_text', 'juniper123')

        cmdlist = []
        if self.ipsec_proposal is not None:
            ipsec_str = 'set services ipsec-vpn ipsec proposal ' + self.ipsec_proposal
            cmdlist.append(ipsec_str + ' authentication-algorithm ' + self.auth_algo)
            cmdlist.append(ipsec_str + ' encryption-algorithm ' + self.encro_algo)
            if 'ipsec_lifetime' in kwargs:
                cmdlist.append(ipsec_str + ' lifetime-seconds ' + kwargs.get('ipsec_lifetime'))
            if 'ipsec_prop_desc' in kwargs:
                cmdlist.append(ipsec_str + ' description ' + kwargs.get('ipsec_prop_desc'))
            if self.protocol:
                cmdlist.append(ipsec_str + ' protocol ' + self.protocol)

        # ipsec policy
        ipsec_policy_str = 'set services ipsec-vpn ipsec policy ' + self.ipsec_policy
        cmdlist.append(ipsec_policy_str + ' proposals ' + self.ipsec_proposal)
        if 'pfs' in kwargs:
            cmdlist.append(ipsec_policy_str + ' perfect-forward-secrecy keys ' + kwargs.get('pfs'))

        ike_str = 'set services ipsec-vpn ike'
        # setting ike proposal
        prop = ike_str + ' proposal ' + self.ike_proposal
        cmdlist.append(prop + ' authentication-method ' + self.ike_auth)
        cmdlist.append(prop + ' authentication-algorithm ' + self.ike_auth_algo)
        cmdlist.append(prop + ' encryption-algorithm ' + self.ike_encr_algo)
        cmdlist.append(prop + ' dh-group ' + self.ike_group)
        if 'ike_lifetime' in kwargs:
            cmdlist.append(prop + ' lifetime-seconds  ' + str(kwargs.get('ike_lifetime')))
        if 'ike_prop_desc' in kwargs:
            cmdlist.append(prop + ' description ' + kwargs['ike_prop_desc'])

        # setting ike policy
        ike_policy_str = ike_str + ' policy ' + self.ike_policy
        if 'pre-shared-keys' in self.ike_auth:
            if 'hexa_key' in kwargs:
                cmdlist.append(ike_policy_str + ' pre-shared-key hexadecimal ' + \
                               kwargs.get('hexa_key'))
            else:
                cmdlist.append(ike_policy_str + ' pre-shared-key ascii-text ' + \
                               self.ascii_key)
        else:
            if 'local_cert' in kwargs:
                cmdlist.append(ike_policy_str + ' local-certificate ' + \
                               kwargs.get('local_cert'))

        cmdlist.append(ike_policy_str + ' proposals ' + self.ike_proposal)
        if self.ike_version == '1':
            cmdlist.append(ike_policy_str + ' mode ' + self.ike_mode)
        cmdlist.append(ike_policy_str + ' version ' + self.ike_version)
        if 'local_id_fqdn' in kwargs:
            cmdlist.append(ike_policy_str + ' local-id fqdn ' + kwargs.get('local_id_fqdn'))
        elif 'local_id_key' in kwargs:
            cmdlist.append(ike_policy_str + ' local-id key-id ' + kwargs.get('local_id_key'))
        elif 'local_id_inet' in kwargs:
            cmdlist.append(ike_policy_str + ' local-id ipv4_addr ' + kwargs.get('local_id_inet'))
        elif 'local_id_inet6' in kwargs:
            cmdlist.append(ike_policy_str + ' local-id ipv6-addr ' + kwargs.get('local_id_inet6'))

        # remote identity
        if 'remote_id_fqdn' in kwargs:
            cmdlist.append(ike_policy_str + ' remote-id fqdn ' + \
                           kwargs.get('remote_id_fqdn'))
        elif 'remote_id_key' in kwargs:
            cmdlist.append(ike_policy_str + ' remote-id key-id ' + \
                           kwargs.get('remote_id_key'))
        elif 'remote_id_inet' in kwargs:
            cmdlist.append(ike_policy_str + ' remote-id ipv4_addr ' + \
                           kwargs.get('remote_id_inet'))
        elif 'remote_id_inet6' in kwargs:
            cmdlist.append(ike_policy_str + ' remote-id ipv6-addr ' + \
                           kwargs.get('remote_id_inet6'))

        if 'peer_cert_type' in kwargs:
            cmdlist.append(ike_policy_str + ' peer-certificate-type ' + \
                           kwargs.get('peer_cert_type'))
        if 'resp_bad_spi' in kwargs:
            cmdlist.append(ike_policy_str + ' respond-bad-spi ' + \
                           str(kwargs.get('resp_bad_spi')))
        if int(estd_tun) == 1:
            cmdlist.append('set services ipsec-vpn establish-tunnels immediately')

        cmdlist.append('set services ipsec-vpn traceoptions flag ' + ipsec_trace)
        cmdlist.append('set services ipsec-vpn traceoptions level ' + ipsec_level)

        try:
            self.dh.log("IPSec config: " + str(cmdlist))
            if self.tunnels > 5:
                return _load_set_config(self.dh, command_list=cmdlist)
            else:
                return self.dh.config(command_list=cmdlist).status()
        except Exception as error:
            self.dh.log(level="ERROR", message=error)
            raise error

    def set_ss(self, **kwargs):
        """
        Configure knobs under set services service-set
        :param ike_access
             *OPTIONAL*  Configures IKE access profile
             Supported values 1/0
        :param int base_if:
            *OPTIONAL* Define base ifl. Default is 1
        :param int sp_nh_style:
            *OPTIONAL* Configures Next hop style. default 1
            Supported values are 0/1
        :param int index:
            *OPTIONAL* Index from which service-set names tagging will start. Default is 1
        :param int dial_options:
            *OPTIONAL* Configure dial options. For DEP use in-conjunction with ike_access=1
             Supported values are 1/0
        :param str dial_mode:
            *OPTIONAL* Configures dail mode. Default shared
             Supported values are 'dedicated'/'shared'
        :param sp_inside_ip:
            *OPTIONAL* SP Inside IP Address
        :param sp_inside_ipv6:
            *OPTIONAL* SP Inside IPv6 Address
        :param sp_outside_ip:
            *OPTIONAL* SP Outside IP Address
        :param sp_outside_ipv6:
            *OPTIONAL* SP Outside IPv6 Address
        :param ike_access:
            *OPTIONAL* Configures IKE access profile.For DEP tunnels use dial_options=1
            Supported values are 1/0
        :param instance:
            *OPTIONAL* Routing instance to be configured for local gateway
        :param vpn_rule str:
            *OPTIONAL* Configure IPSec VPN rule.
        :param vpn_clr_df_bit:
            *OPTIONAL* Configures VPN options Clear DF bit
             Supported values are 1/0
        :param vpn_cp_df_bit:
            *OPTIONAL* Configures VPN options copy DF bit
            Supported values are 1/0
        :param vpn_mtu:
            *OPTIONAL* Configures VPN options Tunnel MTU
        :param arw_size:
            *OPTIONAL*  Size of the anti-replay window (64..4096)
        :param no_ar:
            *OPTIONAL* Disable the anti-replay check
        :param psv_mode:
            *OPTIONAL*  passive mode tunneling
        :param udp_encap:
            *OPTIONAL*  UDP encapsulation of IPsec data traffic
        :param dst_port:
            *OPTIONAL*  UDP destination port
        :param lgw_step:
                *OPTIONAL* Step by which local gw needs to be incremented per rule.
                Default is 0
                When this is used,  local_gw should not be an array of IPs
        :param tcp_mss:
            *OPTIONAL*  Enable the limit on TCP Max. Seg.
             Size in SYN packets (536..65535)
        :param no_nat_traversal:
            *OPTIONAL* Disable NAT traversal for this service-set even if NAT is detected
             Supported value: 1
        :param nat-keepalive:
            *OPTIONAL* NAT-T keepalive interval in secs (1..300)
        EXAMPLE::

           Python:
              ipsec_obj.set_ss()

           Robot:
              configure service set  ${ipsec_obj}
        """
        ifl = kwargs.get('base_ifl', 1)
        next_hop = int(kwargs.get('sp_nh_style', 1))
        lgw_step = int(kwargs.get('lgw_step', 0))
        action = kwargs.get('action', 'set')
        index = kwargs.get('index', 1)
        #rule_idx = kwargs.get('rule_idx', '1')
        #num_rules = kwargs.get('num_rules', self.num_rules)
        self.ss_index = index
        cmdlist = []
        i = 1
        # import sys, pdb
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        gw = ''
        if isinstance(self.local_gw, list):
            gw = self.local_gw.pop()
        else:
            gw = self.local_gw

        while i <= self.tunnels:
            ss_str = action + ' services service-set ' + self.ss + str(i)
            intf_str = action + ' interfaces ' + self.svc_intf + ' unit '
            cmdlist.append(intf_str + str(ifl) + ' family inet')
            #cmdlist.append(intf_str + str(ifl) + ' family inet6')
            #cmdlist.append(ss_str + ' ipsec-vpn-rules ' + self.vpn_name + str(i))
            if int(next_hop) == 1:
                if 'dial_options' in kwargs:
                    if 'dial_mode' in kwargs and 'dedicated' in kwargs.get('dial_options'):
                        cmdlist.append(intf_str + str(ifl) + ' dial-options ipsec-interface-id ' +\
                                       self.if_id + str(index))  # check on self.if_id
                        cmdlist.append(intf_str + str(ifl) + ' dial-options dedicated')
                    else:
                        cmdlist.append(intf_str + str(ifl) + ' dial-options ipsec-interface-id '+ \
                                       self.if_id + str(index))
                        cmdlist.append(intf_str + str(ifl) + ' dial-options shared')
                cmdlist.append(intf_str + str(ifl) + ' service-domain inside')
                cmdlist.append(ss_str + ' next-hop-service inside-service-interface ' + \
                               self.svc_intf + '.' + str(index))
                # add route options to destination ip
                # cmdlist.append('set routing-options static route ' + ts_remote_ip  +
                # ' next-hop ' + self.svc_intf + '.' + str(index))
                # ts_remote_ip = incr_ip_subnet(ts_remote_ip)
                cmdlist.append(ss_str + ' next-hop-service outside-service-interface ' + \
                               self.svc_intf + '.' + str(index + 1))
                cmdlist.append(intf_str + str(ifl + 1) + ' family inet ')
                cmdlist.append(intf_str + str(ifl + 1) + ' service-domain outside')
                if 'sp_inside_ip' in kwargs:
                    cmdlist.append(intf_str + str(ifl) + ' family inet address ' + \
                                   kwargs.get('sp_inside_ip'))
                    # kwargs['sp_inside_ip'] = Utils::incr_ip_subnet(kwargs.get('sp_inside_ip'), i)

                if 'sp_inside_ipv6' in kwargs:
                    cmdlist.append(intf_str + str(ifl) + ' family inet6 address ' + \
                                   kwargs.get('sp_inside_ipv6'))
                # kwargs['sp_inside_ip'] = Utils::incr_ip_subnet(kwargs.get('sp_inside_ipv6'), i)
                # ifl = ifl + 1
                # file related config
                # cmdlist.append(intf_str + ifl + ' family inet')
                if 'sp_outside_ip' in kwargs:
                    cmdlist.append(intf_str + str(ifl) + ' family inet address ' + \
                                   kwargs.get('sp_outside_ip'))
                # kwargs['sp_outside_ip'] = Utils::incr_ip_subnet(kwargs.get('sp_outside_ip'), i)

                if 'sp_outside_ipv6' in kwargs:
                    cmdlist.append(intf_str + str(ifl) + ' family inet6 address ' +\
                                   kwargs.get('sp_outside_ipv6'))
                # kwargs['sp_outside_ip'] = Utils::incr_ip_subnet(kwargs.get('sp_outside_ipv6'), i)
            else:
                cmdlist.append(ss_str + ' interface-service service-interface ' + \
                               self.svc_intf + '.' + str(ifl))

            if 'ike_access' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options ike-access-profile ' + \
                               self.ike_profile + str(i))
            else:
                if self.vpn_name is not None:
                    cmdlist.append(ss_str + ' ipsec-vpn-rules ' + self.vpn_name + str(i))

            cmdlist.append(ss_str + '  ipsec-vpn-options local-gateway ' + strip_mask(gw))
            if 'instance' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options local-gateway routing-instance ' + \
                               kwargs.get('instance') + str(i))
            if 'vpn_clr_df_bit' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options clear-dont-fragment-bit')
            if 'vpn_cp_df_bit' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options set-dont-fragment-bit')
            if 'vpn_mtu' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options tunnel-mtu ' + str(kwargs.get('vpn_mtu')))
            if 'arw_size' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options anti-replay-window-size ' +\
                               kwargs.get('arw_size'))
            if 'no_ar' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options no-anti-replay')
            if 'psv_mode' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options passive-mode-tunneling')
            if 'udp_encap' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options udp-encapsulate')
            if 'dst_port' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options udp-encapsulate dest-port ' + \
                               kwargs.get('dst_port'))
            if 'tcp_mss' in kwargs:
                cmdlist.append(ss_str + ' tcp-mss ' + str(kwargs.get('tcp_mss')))

            if 'no_nat_traversal' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options no-nat-traversal')

            if 'nat_keepalive' in kwargs:
                cmdlist.append(ss_str + ' ipsec-vpn-options nat-keepalive ' + kwargs.get('nat_keepalive'))
 

            if isinstance(self.local_gw, list) and self.local_gw:
                gw = self.local_gw.pop()
            elif lgw_step:
                gw = incr_ip_subnet(gw, lgw_step)
            else:
                gw = self.local_gw

            i = i + 1
            index = index + 2
            ifl = index
        try:
            self.dh.log("Service set: " + str(cmdlist))
            if self.tunnels > 5:
                return _load_set_config(self.dh, command_list=cmdlist)
            else:
                return self.dh.config(command_list=cmdlist).status()
        except Exception as error:
            self.dh.log(level="ERROR", message=error)
            raise error

    def set_rule(self, **kwargs):
        """
            Routine for configuring IPSec VPN rule
            :param term:
                *OPTIONAL* Term name.
                Default is 'term1'
            :param term_idx:
                *OPTIONAL* Index from which the term will start.
                Default is '1'
            :param index:
                *OPTIONAL* Index from which the rule tagging will start.
                Default is '1'
            :param direction:
                *OPTIONAL* Match direction.
                Default is 'input'
            :param from_src:
                *OPTIONAL* Source Address
            :param from_src_incr:
                *OPTIONAL*  Boolean flag whether to increment Host part of Src IP.
                Default is 1
            :param from_src_nw_incr:
                *OPTIONAL* Boolean flag whether to increment Network part of Src IP.
                Default is 0
            :param from_dst:
                *OPTIONAL* Destination Address
            :param from_dst_incr:
                *OPTIONAL*  Boolean flag whether to increment Host part of Dst IP.
                Default is 1.
            :param  from_dst_nw_incr:
                *OPTIONAL* Boolean flag whether to increment Network part of Dst IP.
                Default is 0.
            :param rgw_step:
                *OPTIONAL* Step by which remote gw needs to be incremented per rule.
                Default is 0
                When this is used,  remote_gw should not be an array of IPs
            :param rgw_step_term:
                *OPTIONAL* Step by which remote gw needs to be incremented per term.
                Default is 0.
            :param base_ifl:
                *OPTIONAL* Base IFL.
                Default is 1
            :param ifl_step:
                *OPTIONAL* IFL Step for every tunnel.
                Default is 2
            :return:
                True on success , Raise exception on failure
            EXAMPLE::

                Python:
                   ipsec_obj.set_rule()
                Robot:
                   configure ipsec vpn rule  ${ipsec_obj}
        """
        #import sys, pdb
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        term = kwargs.get('term', 'term1')
        tidx = kwargs.get('term_idx', 1)
        rule_dir = kwargs.get('direction', 'input')
        src_incr = int(kwargs.get('from_src_incr', 1))
        src_nw_incr = int(kwargs.get('from_src_nw__incr', 1))
        dst_incr = int(kwargs.get('from_dst_incr', 1))
        dst_nw_incr = int(kwargs.get('from_dst_nw_incr', 1))
        num_terms = kwargs.get('num_terms', self.num_terms)
        rgw_step = int(kwargs.get('rgw_step', '0'))
        rgw_step_term = int(kwargs.get('rgw_step_term', '0'))
        ifl = kwargs.get('base_ifl', 1)
        ifl_step = kwargs.get('ifl_step', 1)
        index = kwargs.get('index', 1)
        src = kwargs.get('from_src', None)
        dst = kwargs.get('from_dst', None)
        cmdlist = []

        self.dh.log("Configuring IPSec VPN rule for " + str(self.tunnels) + " tunnels")
        gw = ''
        if isinstance(self.remote_gw, list):
            gw = self.remote_gw.pop()
        else:
            gw = self.remote_gw

        i = index
        while i <= self.tunnels:
            j = tidx
            k = 1
            while k <= num_terms:
                strng = "set services ipsec-vpn rule " + self.vpn_name + str(i) + \
                        " term " + str(term) + str(j)
                if src is not None:
                    cmdlist.append(strng + ' from source-address ' + src)
                    if src_nw_incr:
                        src = incr_ip_subnet(src)
                    elif src_incr:
                        src = incr_ip(src)
                if dst is not None:
                    cmdlist.append(strng + ' from destination-address ' + dst)
                    if dst_nw_incr:
                        dst = incr_ip_subnet(dst)
                    elif dst_incr:
                        dst = incr_ip(dst)

                if 'ipsec_ins_intf' in kwargs:
                    cmdlist.append(strng + ' from ipsec-inside-interface ' \
                                   + self.svc_intf + '.' + str(ifl))
                if 'arw_size' in kwargs:
                    cmdlist.append(strng + 'then anti-replay-window-size ' + \
                                   kwargs.get('arw_size'))
                cmdlist.append(strng + '  then remote-gateway ' + strip_mask(gw))
                cmdlist.append(strng + ' then dynamic ike-policy ' + self.ike_policy)
                cmdlist.append(strng + ' then dynamic ipsec-policy ' + self.ipsec_policy)
                if 'init_dpd' in kwargs:
                    cmdlist.append(strng + ' then initiate-dead-peer-detection')
                if 'dpd_interval' in kwargs:
                    cmdlist.append(strng + ' then dead-peer-detection interval ' + \
                                   str(kwargs.get('dpd_interval')))
                if 'dpd_threshold' in kwargs:
                    cmdlist.append(strng + ' then dead-peer-detection threshold ' + \
                                   str(kwargs.get('dpd_threshold')))
                if 'clr_df_bit' in kwargs:
                    cmdlist.append(strng + ' then clear-dont-fragment-bit')
                if 'cp_df_bit' in kwargs:
                    cmdlist.append(strng + ' then copy-dont-fragment-bit')
                if 'set_df_bit' in kwargs:
                    cmdlist.append(strng + ' then copy-dont-fragment-bit')
                if 'bkup_rgw' in kwargs:
                    cmdlist.append(strng + ' then backup-remote-gateway ' + kwargs.get('bkup_rgw'))
                if 'mtu' in kwargs:
                    cmdlist.append(strng + ' then tunnel-mtu ' + str(kwargs.get('mtu')))
                cmdlist.append('set services ipsec-vpn rule ' + self.vpn_name \
                               + str(i) + ' match-direction ' + rule_dir)
                if rgw_step_term:
                    gw = incr_ip_subnet(gw, rgw_step_term)
                k = k + 1
                j = j + 1
            if isinstance(self.remote_gw, list) and self.remote_gw:
                gw = strip_mask(self.remote_gw.pop())
            elif rgw_step:
                gw = incr_ip_subnet(gw, rgw_step)
            else:
                gw = self.remote_gw

            ifl = int(ifl) + ifl_step
            i = i + 1
        try:
            self.dh.log('Set rule: ' + str(cmdlist))
            if self.tunnels > 5:
                return _load_set_config(self.dh, command_list=cmdlist)
            else:
                return self.dh.config(command_list=cmdlist).status()
        except Exception as error:
            self.dh.log(level="ERROR", message=error)
            raise error



def get_ike_values(device_handle, **kwargs):
    """
        Gets requested ike values from the
         show services ipsec-vpn ike sa detail |display xml command

        :param device_handle:
            **REQUIRED** device object

        :param remote_gw:
            **REQUIRED**  Remote gateway Ip

        :param key:
            **REQUIRED**  Single value or list of values from show output

        :return: dictonary  of  values requested

        EXAMPLE::

         regress@kaalia>  show services ipsec-vpn ike sa detail |display xml

          <ike-security-associations-block>
            <ike-sa-remote-address>10.0.1.2</ike-sa-remote-address>
            <ike-security-associations>
                <ike-sa-role>initiator</ike-sa-role>
                <ike-sa-state>matured</ike-sa-state>
                <ike-sa-initiator-cookie>16ac5f588b934e91</ike-sa-initiator-cookie>
                <ike-sa-responder-cookie>5fccb149f6fd6c4e</ike-sa-responder-cookie>
                <ike-sa-exchange-type>IKEv2</ike-sa-exchange-type>
                <ike-sa-authentication-method>Pre-shared-keys</ike-sa-authentication-method>
                <ike-sa-local-gateway-interface>ge-0/2/1</ike-sa-local-gateway-interface>
                <ike-sa-routing-instance></ike-sa-routing-instance>
                <ike-sa-local-address>10.0.1.1</ike-sa-local-address>
                <ike-sa-remote-address>10.0.1.2</ike-sa-remote-address>
                <ike-sa-lifetime>Expires in 2214 seconds</ike-sa-lifetime>
                <ike-sa-algorithms>
                    <ike-sa-authentication-algorithm>hmac-sha1-96</ike-sa-authentication-algorithm>
                    <ike-sa-encryption-algorithm>3des-cbc</ike-sa-encryption-algorithm>
                    <ike-sa-prf-algorithm>hmac-sha1</ike-sa-prf-algorithm>
                    <ike-sa-dhgroup>2</ike-sa-dhgroup>
                </ike-sa-algorithms>
                <ike-sa-traffic-statistics>
                    <ike-sa-input-bytes>8388</ike-sa-input-bytes>
                    <ike-sa-output-bytes>8388</ike-sa-output-bytes>
                    <ike-sa-input-packets>125</ike-sa-input-packets>
                    <ike-sa-output-packets>125</ike-sa-output-packets>
                    <ike-sa-output-invalid-spi-packets>0</ike-sa-output-invalid-spi-packets>
                    <ike-sa-input-invalid-spi-packets>0</ike-sa-input-invalid-spi-packets>
                </ike-sa-traffic-statistics>
                <ike-sa-misc>
                    <ike-sa-flags>IKE SA created</ike-sa-flags>
                    <ike-sa-num-ipsec-sas-created>14</ike-sa-num-ipsec-sas-created>
                    <ike-sa-num-ipsec-sas-deleted>12</ike-sa-num-ipsec-sas-deleted>
                </ike-sa-misc>
            </ike-security-associations>
        </ike-security-associations-block>

         To get ike-sa-index and ike-sa-initiator-cookie values

         ======================================================

         Python:
             dict1 = get_ike_values(dev_obj, remote_gw='10.0.2.2',
                                   key=['ike-sa-state', 'ike-sa-initiator-cookie'])

             Returns dictonary

             {'ike-sa-state: 'matured','ike-sa-initiator-cookie': '16ac5f588b934e91'}

         Robot:
             set test variable  @{key}    ike-sa-state   ike-sa-initiator-cookie
             
             ${dict1} =  get ike values  ${dev_obj}  remote_gw=10.0.2.2  key=@{key}

    """
    rw_address = kwargs.get('remote_gw')
    key_names = []
    if isinstance(kwargs.get('key'), str):
        key_names.append(kwargs.get('key'))
    else:
        key_names = kwargs.get('key')

    # import sys, pdb
    # pdb.Pdb(stdout=sys.__stdout__).set_trace()
    show_cmd = "show services ipsec-vpn ike sa detail"
    rpc_eq = device_handle.get_rpc_equivalent(command=show_cmd)
    root_elem = device_handle.execute_rpc(command=rpc_eq).response()

    # root_elem = device_handle.cli(command=show_cmd, format='xml').response()
    # root_elem = device_handle.cli(command=show_cmd, format='xml')
    dict1 = {}
    #print (ET.tostring(root_elem, pretty_print=True))
    #print(jxmlease.parse_etree(root_elem))
    if isinstance(root_elem, str) and 'rpcerror' in root_elem.lower():
        dict1['error'] = root_elem
        return dict1
    for elem_name in key_names:
        ret = _parse_ike_value(root_elem, elem_name, rw_address)
        if ret is not None:
            dict1[elem_name] = ret
    return dict1


# looks for element in intrest from ike xml output
def _parse_ike_value(root_elem, elem_name, rw_address):
    rw_address = strip_mask(rw_address)
    for child in root_elem.findall('.//ike-security-associations-block'):
        if child.find('.//ike-sa-remote-address').text.strip('\n') == rw_address:
            if child.find(elem_name) is not None:
                return child.find(elem_name).text.strip('\n')
        for subchild in child.findall('.//ike-security-associations'):
            if child.find('.//ike-sa-remote-address').text.strip('\n') == rw_address:
                if subchild.find('.//' + elem_name) is not None:
                    return subchild.find('.//' + elem_name).text.strip('\n')
                else:
                    dic = _check_recur(subchild, elem_name)
                    if elem_name in dic:
                        return dic[elem_name]


def get_ipsec_values(device_handle, **kwargs):
    """

        Gets requested ipsec values from the

        show services ipsec-vpn ipsec sa detail |display xml  command

        :param device_handle:
            **REQUIRED** device object

        :param remote_gw:
            **REQUIRED**  Remote gateway Ip

        :param key:
            **REQUIRED**  Single value or list of values from show output

        :param direction:
            *OPTIONAL* ipsec direction. default is inbound
            Supported values inbound/outbound

        :return: dictonary  of  values requested

        EXAMPLE::

         regress@kaalia>show services ipsec-vpn ipsec sa detail |display xml
           <services-security-associations-block>
            <svc-set-name>ipsec_ss1</svc-set-name>
            <outside-service-interface-routing-instance>default</outside-service-interface-routing-instance>
            <sa-tunnel-information>
                <sa-rule-name>vpn_1</sa-rule-name>
                <sa-term-name>term11</sa-term-name>
                <sa-tunnel-index>1</sa-tunnel-index>
                <sa-local-gateway>10.0.1.1</sa-local-gateway>
                <sa-remote-gateway>10.0.1.2</sa-remote-gateway>
                <sa-inside-interface>ms-1/0/0.1</sa-inside-interface>
                <sa-tunnel-mtu>2000</sa-tunnel-mtu>
                <sa-udp-encapsulate>Disabled</sa-udp-encapsulate>
                <sa-udp-dst-port>0</sa-udp-dst-port>
                <sa-local-identity>ipv4_subnet(any:0,[0..7]=0.0.0.0/0)</sa-local-identity>
                <sa-remote-identity>ipv4_subnet(any:0,[0..7]=0.0.0.0/0)</sa-remote-identity>
            </sa-tunnel-information>
            <security-associations>
                <sa-direction>inbound</sa-direction>
                <sa-spi>3991417868</sa-spi>
                <sa-aux-spi>0</sa-aux-spi>
                <sa-mode>tunnel</sa-mode>
                <sa-type>dynamic</sa-type>
                <sa-state>installed</sa-state>
                <sa-protocol>ESP</sa-protocol>
                <sa-authentication-algorithm>hmac-sha1-96</sa-authentication-algorithm>
                <sa-encryption-algorithm>3des-cbc</sa-encryption-algorithm>
                <sa-soft-lifetime>Expires in 16 seconds</sa-soft-lifetime>
                <sa-hard-lifetime>Expires in 96 seconds</sa-hard-lifetime>
                <sa-anti-replay-service>enabled</sa-anti-replay-service>
                <sa-replay-window-size>4096</sa-replay-window-size>
                <sa-copy-tos-from-inner-ip-header>enabled</sa-copy-tos-from-inner-ip-header>
                <sa-copy-ttl-from-inner-ip-header>disabled</sa-copy-ttl-from-inner-ip-header>
                <sa-ttl-value>64</sa-ttl-value>
            </security-associations>


         To get sa-block-state and sa-bind-interface

         ===========================================

         Python:
             ipsec_values = get_ipsec_values(dev_obj, remote_gw='10.0.1.2',
                            key=['sa-state', 'sa-tunnel-mtu'])

         Robot:
             set test variable  @{key}    sa-state   sa-tunnel-mtu

             ${ipsec_values} =  get ipsec values  ${dev_obj}  remote_gw=10.0.1.2  key=@{key}

         Returns dictonary
            {'sa-state': 'installed','sa-tunnel-mtu': '2000'}

    """
    rw_address = kwargs.get('remote_gw')
    key_names = []
    if isinstance(kwargs.get('key'), str):
        key_names.append(kwargs.get('key'))
    else:
        key_names = kwargs.get('key')

    direction = 'inbound'
    if 'direction' in kwargs:
        direction = kwargs.get('direction')

    show_cmd = "show services ipsec-vpn ipsec  sa detail"
    rpc_eq = device_handle.get_rpc_equivalent(command=show_cmd)
    root_elem = device_handle.execute_rpc(command=rpc_eq).response()
    dict1 = {}
    if isinstance(root_elem, str) and 'rpcerror' in root_elem.lower():
        dict1['error'] = root_elem
        return dict1

    for elem_name in key_names:
        ret = _parse_ipsec_value(root_elem, elem_name, rw_address, direction)
        if ret is not None:
            dict1[elem_name] = ret
    return dict1

    # looks for element in intrest from ipsec xml output


def _parse_ipsec_value(root_elem, elem_name, rw_address, direction):
    rw_address = strip_mask(rw_address)
    for child in root_elem.findall('.//services-security-associations-block'):
        if child.find('.//sa-remote-gateway') is None:
            return ''
        if child.find('.//sa-remote-gateway').text.strip('\n') == rw_address:
            if child.find(elem_name) is not None:
                return child.find(elem_name).text.strip('\n')
        for subchild in child.findall('.//security-associations'):
            if child.find('.//sa-remote-gateway').text.strip('\n') == rw_address:
                if subchild.find('.//sa-direction').text.strip('\n') == direction:
                    if subchild.find('.//' + elem_name) is not None:
                        if subchild.find('.//' + elem_name).text is not None:
                            return subchild.find('.//' + elem_name).text.strip('\n')
                    else:
                        dic = _check_recur(subchild, elem_name)
                        if elem_name in dic:
                            return dic[elem_name]
        # check at security-association-block level recuressively
        if child.find('.//sa-remote-gateway').text.strip('\n') == rw_address:
            dic = _check_recur(child, elem_name)
            if elem_name in dic:
                return dic[elem_name]
    return ''


def get_ipsec_stats(device_handle, **kwargs):
    """
     Gets requested ipsec values from the
        show security ipsec statistics detail |display xml

    :param device_handle:
        **REQUIRED**  device handle

    :param key:
        **REQUIRED**  Single value or list of values from show output

    :return: dictonary of requested values

    EXAMPLE::

     regress@kaalia> show security ipsec statistics |display xml

     <usp-ipsec-total-statistics-information>

        <esp-statistics>

            <esp-encrypted-bytes>0</esp-encrypted-bytes>

            <esp-decrypted-bytes>0</esp-decrypted-bytes>

            <esp-encrypted-packets>0</esp-encrypted-packets>

            <esp-decrypted-packets>0</esp-decrypted-packets>

        </esp-statistics>

        <ah-statistics>

            <ah-input-bytes>0</ah-input-bytes>

            <ah-output-bytes>0</ah-output-bytes>

            <ah-input-packets>0</ah-input-packets>

            <ah-output-packets>0</ah-output-packets>

        </ah-statistics>

        <error-statistics>

            <ah-authentication-failures>0</ah-authentication-failures>

            <replay-errors>0</replay-errors>

            <esp-authentication-failures>0</esp-authentication-failures>

            <esp-decryption-failures>0</esp-decryption-failures>

            <bad-headers>0</bad-headers>

            <bad-trailers>0</bad-trailers>

        </error-statistics>

     </usp-ipsec-total-statistics-information>

     To get esp-encrypted-packets, esp-decrypted-packets

     ===================================================

     Python:
         ipsec_stats = get_ipsec_stats(dev_obj, key=['esp-encrypted-packets',
                       'esp-decrypted-packets', 'ah-input-packets','ah-output-packets'])

     Robot:
         set test variable  @{key}  esp-encrypted-packets  esp-decrypted-packets  ah-input-packets  ah-output-packets

         ${ipsec_stats} =  get ipsec stats  ${dev_obj}  key=@{key}

     Returns

         {'ah-input-packets': '0', 'esp-encrypted-packets': '0',
         'ah-output-packets': '0', 'esp-decrypted-packets': '0'}
    """
    key_names = []
    if isinstance(kwargs.get('key'), str):
        key_names.append(kwargs.get('key'))
    else:
        key_names = kwargs.get('key')

    show_cmd = "show services ipsec-vpn ipsec statistics detail"
    rpc_eq = device_handle.get_rpc_equivalent(command=show_cmd)
    root_elem = device_handle.execute_rpc(command=rpc_eq).response()

    dict1 = {}
    for elem_name in key_names:
        dict1.update(_check_recur(root_elem, elem_name))
    return dict1

def get_ike_stats(device_handle, **kwargs):
    """
        Gets requested ike values from the

        show services ipsec-vpn ike statistics |display xml

        :param device_handle:
        **REQUIRED**  device handle

        :param key:
        **REQUIRED**  Single value or list of values from show output

        :param remote_gw:
        **REQUIRED** Ip address of remote gateway

        :return: dictonary of requested values

        EXAMPLE::

         <ike-security-associations-block>
            <ike-sa-remote-address>12.0.1.1</ike-sa-remote-address>
            <ike-security-associations>
                <ike-sa-initiator-cookie>7fbfe094090a111a</ike-sa-initiator-cookie>
                <ike-sa-responder-cookie>a20c3812ec9ca32b</ike-sa-responder-cookie>
                <ike-sa-routing-instance></ike-sa-routing-instance>
                <ike-sa-local-address>11.0.1.1</ike-sa-local-address>
                <ike-sa-remote-address>12.0.1.1</ike-sa-remote-address>
                <ike-sa-misc>
                    <ike-sa-num-ipsec-sas-created>24</ike-sa-num-ipsec-sas-created>
                    <ike-sa-num-ipsec-sas-deleted>22</ike-sa-num-ipsec-sas-deleted>
                    <ike-sa-num-ipsec-rekeys>12</ike-sa-num-ipsec-rekeys>
                    <ike-sa-exchange-type>IKEv2</ike-sa-exchange-type>
                </ike-sa-misc>
                <ike-sa-traffic-statistics>
                    <ike-sa-input-bytes>28876</ike-sa-input-bytes>
                    <ike-sa-output-bytes>28876</ike-sa-output-bytes>
                    <ike-sa-input-packets>427</ike-sa-input-packets>
                    <ike-sa-output-packets>427</ike-sa-output-packets>
                </ike-sa-traffic-statistics>
                <ike-sa-payload-statistics>
                    <ike-sa-delete-payloads-received>11</ike-sa-delete-payloads-received>
                    <ike-sa-delete-payloads-sent>11</ike-sa-delete-payloads-sent>
                    <ike-sa-dpd-request-payloads-received>207</ike-sa-dpd-request-payloads-received>
                    <ike-sa-dpd-request-payloads-sent>197</ike-sa-dpd-request-payloads-sent>
                    <ike-sa-dpd-response-payloads-received>197</ike-sa-dpd-response-payloads-received>
                    <ike-sa-dpd-response-payloads-sent>207</ike-sa-dpd-response-payloads-sent>
                    <ike-sa-dpd-response-payloads-missed>0</ike-sa-dpd-response-payloads-missed>
                    <ike-sa-dpd-response-payloads-maximum-delay>26</ike-sa-dpd-response-payloads-maximum-delay>
                    <ike-sa-invalid-spi-notifications-received>0</ike-sa-invalid-spi-notifications-received>
                    <ike-sa-invalid-spi-notifications-sent>0</ike-sa-invalid-spi-notifications-sent>
                </ike-sa-payload-statistics>
            </ike-security-associations>


         To get values of ike-sa-delete-payloads-received and ike-sa-delete-payloads-sent
         ===============================================================================

         Python:

             ike_stats = get_ike_stats(dev_obj, remote_gw='12.0.1.1',
                         key=['ike-sa-delete-payloads-received','ike-sa-delete-payloads-sent'])

         Robot:
             set test variable  @{key}  ike-sa-delete-payloads-received  ike-sa-delete-payloads-sent

             ${ipsec_stats} =  get ike stats  ${dev_obj}  key=@{key}

         Returns
         {'ike-sa-delete-payloads-received': '11', 'ike-sa-delete-payloads-sent': '11'}
    """

    rw_address = kwargs.get('remote_gw')
    key_names = []
    dict1 = {}
    if isinstance(kwargs.get('key'), str):
        key_names.append(kwargs.get('key'))
    else:
        key_names = kwargs.get('key')

    show_cmd = "show services ipsec-vpn ike statistics"
    rpc_eq = device_handle.get_rpc_equivalent(command=show_cmd)
    root_elem = device_handle.execute_rpc(command=rpc_eq).response()
    if isinstance(root_elem, str) and 'rpcerror' in root_elem.lower():
        dict1['error'] = root_elem
        return dict1
    for elem_name in key_names:
        ret = _parse_ike_value(root_elem, elem_name, rw_address)
        if ret is not None:
            dict1[elem_name] = ret
    return dict1

# verify ike sa
def verify_ike_sa(device_handle, **kwargs):
    """

         Verifies given ike values with actual values

         :param device_handle:
                **REQUIRED** device object

         :param remote_gw:
                **REQUIRED**  Remote gateway Ip

         :param exp_dic:
                **REQUIRED**  Dictionary of expected key-value pairs.
                Note: keys should be same as displayed by
                (show security ike sa detail | display xml)

         :param max_tries:
                Maximum number of retries. Default is 2

         :param sleep_time:
                Sleep in secs before next try. Default is 5

         :param err_level:
                Supported values INFO/WARN/ERROR
                Default ERROR

         :return:  TRUE on match,  FALSE on mismatch

         EXAMPLE::

           Python:
              verify_ike_sa(device_handle, remote_gw='10.0.1.2', exp_dic={'ike-sa-state': 'matured'})

           Robot:
              set test variable     &{ike-sa}    ike-sa-state=matured

              ${ret-ike} =  verify ike sa  ${device_handle}  remote_gw=11.0.1.2  exp_dic=${ike-sa}
    """

    if 'remote_gw' not in kwargs:
        device_handle.log("Need remote_gw as it is mandatory argument")
        raise KeyError("required  Arguments remote_gw missing")

    max_tries = kwargs.get('max_tries', 2)
    sleep_time = kwargs.get('sleep_time', 5)
    err_level = kwargs.get('err_level', 'ERROR')
    exp_dic = kwargs.get('exp_dic')
    keys = exp_dic.keys()
    i = 0
    # import sys, pdb
    # pdb.Pdb(stdout=sys.__stdout__).set_trace()
    while i < int(max_tries):
        actual_dic = get_ike_values(device_handle, key=keys,
                                    remote_gw=strip_mask(kwargs.get('remote_gw')))
        if 'error' in actual_dic:
            device_handle.log(level='ERROR', message=actual_dic['error'])
            return False
        if _cmp_(actual_dic, exp_dic):
            device_handle.log("Expected and actual values match")
            return True
        i = i + 1
        time.sleep(int(sleep_time))

    device_handle.log(level=err_level, message="Expected values:%s \
                    and actual values:%s  didnot match" %(exp_dic, actual_dic))
    return False


# verify ipsec sa
def verify_ipsec_sa(device_handle, **kwargs):
    """

        Verifies given ipsec values with actual values

        :param device_handle:
            **REQUIRED** device object

        :param remote_gw:
            **REQUIRED**  Remote gateway Ip

        :param exp_dic:
            **REQUIRED**  Dictionary of expected key-value pairs.
            Note: keys should be same as displayed by (show security ipsec sa detail | display xml)

        :param direction:
            *OPTIONAL* ipsec direction. default is inbound
            Supported values inbound/outbound

        :param max_tries:
            Maximum number of retries. Default is 2

        :param sleep_time:
            Sleep in secs before next try. Default is 5

        :param err_level:
                Supported values INFO/WARN/ERROR
                Default ERROR

        :return: TRUE on match,  FALSE on mismatch

        EXAMPLE::

          Python:
              verify_ipsec_sa(device_handle, remote_gw='', exp_dic={'sa-state': 'installed'})

          Robot:
              set test variable     &{ipsec-sa}    sa-state=installed

              verify ipsec sa  ${device_handle}  remote_gw=10.0.1.2  exp_dic=${ipsec-sa}

    """

    if 'remote_gw' not in kwargs:
        device_handle(level="ERROR", message="Need remote_gw as it is mandatory argument")
        raise KeyError("required  Arguments remote_gw missing")

    exp_dic = kwargs.get('exp_dic')
    keys = exp_dic.keys()
    max_tries = kwargs.get('max_tries', 2)
    sleep_time = kwargs.get('sleep_time', 5)
    err_level = kwargs.get('err_level', 'ERROR')
    exp_dic = kwargs.get('exp_dic')
    actual_dic = {}
    # import sys,pdb
    # pdb.Pdb(stdout=sys.__stdout__).set_trace()
    i = 0
    while i < int(max_tries):
        if 'direction' in kwargs:
            actual_dic = get_ipsec_values(device_handle, key=keys,
                                          remote_gw=strip_mask(kwargs.get('remote_gw')),
                                          direction=kwargs.get('direction'))
        else:
            actual_dic = get_ipsec_values(device_handle, key=keys,
                                          remote_gw=strip_mask(kwargs.get('remote_gw')))

        if 'error' in actual_dic:
            device_handle.log(level="ERROR", message=actual_dic['error'])
            return False
        if _cmp_(actual_dic, exp_dic):
            device_handle.log("Expected and actual values match")
            return True
        i = i + 1
        time.sleep(int(sleep_time))

    device_handle.log(level=err_level, message="Expected values: %s and \
                      actual values: %s  didnot match" % (exp_dic, actual_dic))
    return False


#  verifies pic is online or offline
def verify_pic_status(device_handle, **kwargs):
    """
        Verifies pic status by running "show chassis fpc pic-status"

        :param device_handle:
            **REQUIRED** device object

        :param max_tries
            *OPTIONAL*  Number of tries before returning. Default is 2

        :param sleep_time
            *OPTIONAL*  Sleep in secs before next try. Default is 30

        :param err_level:
                Supported values INFO/WARN/ERROR
                Default ERROR

        :return: True if pics are online
             False if pics are offline

        EXAMPLE::

             Python:
                 verify_pic_status(device_handle)

             Robot:
                 verify pic status  ${device_handle}

    """
    i = 1
    flag = 1
    max_tries = kwargs.get('max_tries', 2)
    sleep_time = kwargs.get('sleep_time', 30)
    err_level = kwargs.get('err_level', 'ERROR')
    show_cmd = 'show chassis fpc pic-status'
    rpc_eq = device_handle.get_rpc_equivalent(command=show_cmd)
    while i < int(max_tries):
        resp = device_handle.execute_rpc(command=rpc_eq).response()
        for fpc in resp.findall('./fpc'):
            for pic in fpc.findall('./pic'):
                if pic.find('./pic-state').text.lower() != 'online':
                    flag = 0
        if flag == 1:
            return True
        i = i + 1
        time.sleep(int(sleep_time))
    device_handle.log(level=err_level, message="Pics are not online")
    return False

#  Function to get required string from log
#  get_string_from_log(device_handle, log='kmd', string='auth fail')
def get_string_from_log(device_handle, **kwargs):
    """
       Gets line matching the string from the log.
       :param device_handle:
       :param log:
        **REQUIRED** log file name to search
        eg: kmd/syslog/pkid
       :param string:
        **REQUIRED**  string to search
       :return: matched string line
       EXAMPLE:
           Python:
              get_string_from_log(device_handle, log='kmd', string='auth fail')

           Robot:
              ${string} =  get string from log  {device_handle}  lof=kmd  string=auth fail
    """
    log = kwargs.get('log')
    str1 = kwargs.get('string')
    # result = device_handle.cli(command="show log "+  log + "|grep "+ str1).response()
    matched_str = device_handle.shell(command="grep " + str1 + ' /var/log/' + log).response()
    device_handle.log(level="INFO", message="Matched string %s in log %s:" % (log, matched_str))
    return matched_str

# Verification of DPD behaviour w.r.to interval and threshold values
def verify_dpd(dh, **kwargs):
    """
         Verification of DPD behaviour
         w.r.to interval and threshold values

         :param dh:
                **REQUIRED** device object

         :param dpd_int:
                **REQUIRED** dpd interval value

         :param dpd_thr:
                **REQUIRED**  dpd thershold value

         :param key:
                **REQUIRED**  key to get dpd missed count

         :param remote_gw:
                **REQUIRED**  Remote gateway Ip

         :param exp_dic:
                **REQUIRED**  exp_dic for IKE_SA State

         :param err_level:
                Supported values INFO/WARN/ERROR
                Default ERROR

         :return:  TRUE on match,  FALSE on mismatch

         EXAMPLE::

           Python:
               verify_dpd(dh, dpd_int='10', dpd_thr='5',

               key='ike-sa-dpd-response-payloads-missed', remote_gw='12.0.1.1',exp_dic={'ike-sa-state': 'UP'})

           Robot:
               set test variable   @{key}  ike-sa-dpd-response-payloads-missed

               set test variable   &{exp_dict}  ike-sa-state=UP

               verify  dpd  {dh}  dpd_int=10  dpd_thr=5  key=@{key}  remote_gw=12.0.1.1  exp_dic=&{exp_dict}

    """

    if not kwargs.keys() & {'dh', 'dpd_int', 'dpd_thr', 'key', 'remote_gw', 'exp_dic'}:
        dh.log("Mandatory arguments are missing")
        raise ValueError("Mandatory arguments are missing")

    dpd_int = kwargs.get('dpd_int')
    dpd_thr = kwargs.get('dpd_thr')
    key = kwargs.get('key')
    remote_gw = kwargs.get('remote_gw')
    exp_dic = kwargs.get('exp_dic')
    err_level = kwargs.get('err_level', 'ERROR')
    i = 0
    #for i in range(0, int(dpd_thr)):
    while i < int(dpd_thr):
        dict1 = get_ike_stats(dh, key=key, remote_gw=remote_gw)
        dpd_missed_count = int(dict1[key])
        dh.log(level='INFO', message="missed count: %s" %dpd_missed_count)
        if dpd_missed_count >= (int(dpd_thr) - 2):
            time.sleep((int(dpd_int)*3)+10)
            if not verify_ike_sa(dh, remote_gw=remote_gw, exp_dic=exp_dic, err_level=err_level):
                dh.log(level='INFO', message="IKE SA got cleared after reaching dpd threshold value as expected")
                return True
        i = i+1
        time.sleep(int(dpd_int))
    dh.log(level='ERROR', message="DPD is not working as expected")
    return False

# Configure IKE profile at groups level
def configure_groups_ike_access(dh, **kwargs):
    """
         Configure groups IKE access profile

            :param dh
                *REQUIRED* device object

            :param groups_name:
                *REQUIRED* provide the groups name to be configured

            :param ike_profile:
                *OPTIONAL* Profile name to be configured.
                Default is <*>

            :param ike_client:
                *OPTIONAL* Name of entity requesting access

                Default is <*>
            :param init_dpd:
                *OPTIONAL* Configure inititiate-dead-peer-detection

                Supported values 1/0

            :param dpd_interval:
                *OPTIONAL* Dead peer detection interval

            :param dpd_threshold:
                *OPTIONAL* Dead peer detection threshold

            :param ipsec_policy:
                *OPTIONAL*  Configure IPSec Policy

                Explicitly mention the IPSec policy to be configured

            :param ike_policy:
                *OPTIONAL*   Configure IKE Policy

                Explicitly mention the IKE policy to be configured

            :param ascii_key:
                *OPTIONAL* Define pre-shared key in ascii-text

            :param interface_id:
                *OPTIONAL* Identity of logical service interface pool

            :return:

            EXAMPLE::

                configure groups ike access   ${dh0}   groups_name=enable_dpd   init_dpd=1   dpd_interval=40

    """
    if 'groups_name' not in kwargs:
        dh.log(level="ERROR", message="Need groups_name as it is mandatory argument")
        raise KeyError("required  Arguments groups_name missing")

    cmdlist = []
    ike_profile = kwargs.get('ike_profile','<*>')
    ike_client = kwargs.get('ike_client','<*>')

    dh.log(" Configuring IKE access profile in groups ")
    access_str = 'set groups ' + kwargs.get('groups_name') + ' access profile ' + ike_profile + ' client ' + \
            ike_client + ' ike '
    if 'init_dpd' in kwargs:
        cmdlist.append(access_str + ' initiate-dead-peer-detection')
    if 'dpd_interval' in kwargs:
        cmdlist.append(access_str + ' dead-peer-detection interval ' + \
                    str(kwargs.get('dpd_interval')))
    if 'dpd_threshold' in kwargs:
        cmdlist.append(access_str + ' dead-peer-detection threshold ' + \
                    str(kwargs.get('dpd_threshold')))
    if 'ipsec_policy' in kwargs:
        cmdlist.append(access_str + ' ipsec-policy ' + kwargs.get('ipsec_policy'))
    if 'ike_policy' in kwargs:
        cmdlist.append(access_str + ' ike-policy ' + kwargs.get('ike_policy'))
    if 'ascii_key' in kwargs:
        cmdlist.append(access_str + ' pre-shared-key ascii-text ' + kwargs.get('[ascii_key]'))
    if 'interface_id' in kwargs:
        cmdlist.append(access_str + ' interface-id ' + kwargs.get('interface_id'))

    try:
        dh.log('Groups IKE access config: ' + str(cmdlist))
        dh.config(command_list=cmdlist).status()
        return True
    except Exception as error:
        dh.log(level="ERROR", message=error)
        raise error

# recursively check for the element from xml root
# and returns dictonary with elemnet and its value
def _check_recur(root, key, dic=None):
    if dic is None:
        dic = {}
    if root.tag.title().lower() == key.lower():
        # print(root.attrib.get('name', root.text))
        # return root.attrib.get('name', root.text)
        dic[key] = root.attrib.get('name', root.text.strip('\n'))
    else:
        for elem in root.getchildren():
            _check_recur(elem, key, dic)
    return dic

#  Compare dictionaries
def _cmp_(dict1, dict2):
    match = True
    if not bool(dict1):
        match = False
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
            match = False
    return match

#  Loads set commands on to the router
#  _load_set_config(device_handle,command_list,timeout=1200)
def _load_set_config(device_handle, command_list, timeout=1200):

    conf_file = "scale_config.txt"
    device_handle.log(" Going to load " + str(command_list) + " set commands with a timeout of " \
                      + str(timeout) + " secs")
    file_handle = open(conf_file, "w+")
    for cmd in command_list:
        file_handle.write(cmd + '\n')
    file_handle.close()

    try:
        device_handle.upload(local_file=conf_file, remote_file="/var/home/regress")
        return device_handle.config(command_list=["load set "+ conf_file]).status()
    except Exception as error:
        device_handle.log(level="ERROR", message=error)
        raise error


# wrapper functions for robo keywords
# Create Ipsec object
def create_ipsec_object(dev_obj, **kwargs):
    """
            Wrapper function for robot, calls IPSec init class

            Intializes vpn object based on remote gateway
            and sp interface

            :param device_handle:
                **REQUIRED** device object

            :param svc_intf:
                **REQUIRED** service interface

            :param ss:
                **OPTIONAL** service set name
                Default is ipsec_ss1

            :param local_gw:
                **REQUIRED**  Local IP address for IKE negotiations

            :param remote_gw:
                **REQUIRED**  Remote IP address of the peer

            :param vpn_name:
                **OPTIONAL** vpn rule name
                Default is vpn_rule1

            :param tunnels:
                *OPTIONAL*  Number of tunnels. Default is 1

            :param num_terms:
                *OPTIONAL*  Number of terms per rule
                 Default is 1

            :param num_rules:
                *OPTIONAL* Number of rules.
                Default is 1

            :param ipsec_policy:
                *OPTIONAL* IPSec Policy Name
                Default is ipsec_policy

            :param ipsec_proposal:
                *OPTIONAL* IPSec Proposal Name
                Default is ipsec_prop

            :param ike_profile:
                *OPTIONAL* IKE Profile Name
                Default is ike_access

            :param ike_proposal:
                *OPTIONAL* IKE Proposal Name
                Default is ike_proposal

            :param ike_policy:
                *OPTIONAL* IKE Policy Name
                Default is ike_policy

            :param ike_auth:
                *OPTIONAL* IKE Authentication type
                Default is 'pre-shared-keys'

            :param ike_version:
                *OPTIONAL* IKE Version
                Default is 2

            :param ike_mode:
                *OPTIONAL* IKE Mode
                Default is 'main'
                Supported values main/aggresive

            :param ike_clnt:
                *OPTIONAL* IKE Client
                 Default is '*'

            :param ike_group:
                *OPTIONAL*  Define Diffie-Hellman group
                Default is 'group2'

            :param group_name:
                *OPTIONAL* Group Name
                Default  is 'ipsec-changes'

            :param protocol:
                *OPTIONAL* Protocol [ESP|AH]
                Default is 'esp'

            :param ipsec_auth_algo:
                *OPTIONAL* Authentication algorithm for IPSec.

                Default is 'hmac-sha1-96'

            :param ipsec_encr_algo:
                *OPTIONAL*Encryption algorithm for IPSec.

                Default is '3des-cbc'

            :param ike_auth_algo:
                *OPTIONAL* IKE Authentication algorithm:

                Default is 'sha1'

            :param ike_encr_algo:
                *OPTIONAL* IKE Encryption algorithm.
                Default is '3des-cbc'

            :param estd_tun:
                *OPTIONAL* Establish tunnels immediately. default is 0

                Supported values 0/1

            :return: IPSec object

            EXAMPLE::

               ${ipsec_obj} =  Create Ipsec Object  ${dh0}  local_gw=${t['resources']['r0']['interfaces']['r0-r1']['uv-ip']}
                              remote_gw=${t['resources']['r1']['interfaces']['r0-r1']['uv-ip']}
                              svc_intf=${t['resources']['r0']['interfaces']['r0-ms0-0']['pic']}

    """
    return IPSec(dev_obj, **kwargs)

# calls set access
def configure_access(ipsec_obj, **kwargs):
    """
            Wrapper function which calls set_access

            :param init_dpd:
                *OPTIONAL* Configure inititiate-dead-peer-detection
                Supported values 1/0

            :param dpd_interval:
                *OPTIONAL* Dead peer detection interval

            :param dpd_threshold:
                *OPTIONAL* Dead peer detection threshold

            :param ipsec_policy:
                *OPTIONAL*  Configure IPSec Policy
                Supported values 1/0

            :param ike_policy:
                *OPTIONAL*   Configure IKE Policy
                Supported values 1/0

            :param apply-groups:
                *OPTIONAL*  Apply groups config to access profile

            :param proxy-pair:
                *OPTIONAL* Configure local and remote proxy pairs

                Eg: [30.0.0.0/16, 80.0.0.0/16]

            :return: True on success, Raise exception on Failure

            EXAMPLE::

               configure access  ${ipsec_obj}

               Apply groups and proxy pair for access:

               configure access   ${ipsec_obj}   apply-groups=enable_dpd   proxy_pair=${proxy_pair}
    """
    return ipsec_obj.set_access(**kwargs)


def configure_ipsec(ipsec_obj, **kwargs):
    """
            Wrapper function which calls set_ipsec_config
            Configure ipsec knob under set services ipsec-vpnm

            :param ipsec_lifetime:
                *OPTIONAL* Ipsec Lifetime, in seconds
                  Range 180..86400 seconds

            :param ipsec_prop_desc:
                *OPTIONAL* Text description of IPSec proposal

            :param ipsec_protocol:
                *OPTIONAL* Define an IPSec protocol for the proposal
                Supported values are ah/esp

            :param ipsec_prop_set:
                *OPTIONAL* Types of default IPSEC proposal-set
                 Supported values are basic/compatible/standard/suiteb-gcm-128/suiteb-gcm-256

            :param estd_tun:
                *OPTIONAL* Establish tunnels immediately. default is 0

                Supported values 0/1

            :param ike_lifetime:
                *OPTIONAL* IKE Proposal lifetime in seconds

            :param ascii_text:
                *OPTIONAL*  ascii key for authentication pre-shared key

                Default is "juniper123"

            :param hexa_key:
                *OPTIONAL*  hexa key for authentication pre-shared key

            :param pfs:
                *OPTIONAL* Define perfect forward secrecy

                Supported values group1/group14/group19/group2/
                group20/group24/group5

            :param local_cert:
                *OPTIONAL* Local certificate name if ike_auth specified as rsa

            :param local_id_fqdn:
                *OPTIONAL* Use a fully-qualified domain name in local certificate

            :param local_id_inet:
                *OPTIONAL* Use an IPv4 address

            :param local_id_inet6:
                *OPTIONAL* Use an IPv6 address

            :param local_id_key:
                *OPTIONAL* Use an key-id

            :param remote_id_fqdn:
                *OPTIONAL*  Use a fully-qualified domain name specified in remote certificate

            :param remote_id_inet:
                *OPTIONAL* Use an IPv4 address

            :param remote_id_inet6:
                *OPTIONAL* Use an IPv6 address

            :param remote_id_key_id:
                *OPTIONAL* Use an  key-id

            :param peer_cert_type:
                *OPTIONAL* Peer certificate type

            :param ipsec_trace:
                *OPTIONAL* Trace options for IPSec data-plane debug. Default is All

                 Supported values are next-hop-tunnel-binding/packet-drops/
                 packet-processing/security-associations

            :param ipsec_level:
                *OPTIONAL* ipsec trace level

                Default is 'all'

            :return:

            EXAMPLE::

                configure ipsec   ${ipsec_obj}

    """
    return ipsec_obj.set_ipsec_config(**kwargs)


def configure_service_set(ipsec_obj, **kwargs):
    """
        Wrapper function which calls service_set

        Configure knobs under set services service-set

        :param ike_access
             *OPTIONAL*  Configures IKE access profile

             Supported values 1/0

        :param int base_if:

            *OPTIONAL* Define base ifl. Default is 1

        :param int sp_nh_style:
            *OPTIONAL* Configures Next hop style. default 1

            Supported values are 0/1

        :param int index:
            *OPTIONAL* Index from which service-set names tagging will start. Default is 1

        :param int dial_options:
            *OPTIONAL* Configure dial options. For DEP use in-conjunction with ike_access=1

             Supported values are 1/0

        :param str dial_mode:
            *OPTIONAL* Configures dail mode. Default shared

             Supported values are 'dedicated'/'shared'

        :param sp_inside_ip:
            *OPTIONAL* SP Inside IP Address

        :param sp_inside_ipv6:
            *OPTIONAL* SP Inside IPv6 Address

        :param sp_outside_ip:
            *OPTIONAL* SP Outside IP Address

        :param sp_outside_ipv6:
            *OPTIONAL* SP Outside IPv6 Address

        :param ike_access:
            *OPTIONAL* Configures IKE access profile.For DEP tunnels use dial_options=1

            Supported values are 1/0

        :param instance:
            *OPTIONAL* Routing instance to be configured for local gateway

        :param vpn_rule str:
            *OPTIONAL* Configure IPSec VPN rule.

        :param vpn_clr_df_bit:
            *OPTIONAL* Configures VPN options Clear DF bit

             Supported values are 1/0

        :param vpn_cp_df_bit:
            *OPTIONAL* Configures VPN options copy DF bit

            Supported values are 1/0

        :param vpn_mtu:
            *OPTIONAL* Configures VPN options Tunnel MTU

        :param arw_size:
            *OPTIONAL*  Size of the anti-replay window (64..4096)

        :param no_ar:
            *OPTIONAL* Disable the anti-replay check

        :param psv_mode:
            *OPTIONAL*  passive mode tunneling

        :param udp_encap:
            *OPTIONAL*  UDP encapsulation of IPsec data traffic

        :param dst_port:
            *OPTIONAL*  UDP destination port

        :param lgw_step:
                *OPTIONAL* Step by which local gw needs to be incremented per rule.
                Default is 0

                When this is used,  local_gw should not be an array of IPs

        :param tcp_mss:
            *OPTIONAL*  Enable the limit on TCP Max. Seg.

             Size in SYN packets (536..65535)

        :param no_nat_traversal:
            *OPTIONAL* Disable NAT traversal for this service-set even if NAT is detected

             Supported value: 1

        :param nat-keepalive:
            *OPTIONAL* NAT-T keepalive interval in secs (1..300)

        EXAMPLE::

              configure service set  ${ipsec_obj}

              In case od DEP:

                  configure service set   ${ipsec_obj}   ike_access=1   dial_options=1
    """
    return ipsec_obj.set_ss(**kwargs)


def configure_ipsec_vpn_rule(ipsec_obj, **kwargs):
    """
            Wrapper function which calls ipsec_vpn_rule.
            Routine for configuring IPSec VPN rule

            :param term:
                *OPTIONAL* Term name.

                Default is 'term1'

            :param term_idx:
                *OPTIONAL* Index from which the term will start.

                Default is '1'

            :param index:
                *OPTIONAL* Index from which the rule tagging will start.

                Default is '1'

            :param direction:
                *OPTIONAL* Match direction.

                Default is 'input'

            :param from_src:
                *OPTIONAL* Source Address

            :param from_src_incr:
                *OPTIONAL*  Boolean flag whether to increment Host part of Src IP.
                Default is 1

            :param from_src_nw_incr:
                *OPTIONAL* Boolean flag whether to increment Network part of Src IP.
                Default is 0

            :param from_dst:
                *OPTIONAL* Destination Address

            :param from_dst_incr:
                *OPTIONAL*  Boolean flag whether to increment Host part of Dst IP.
                Default is 1.

            :param  from_dst_nw_incr:
                *OPTIONAL* Boolean flag whether to increment Network part of Dst IP.
                Default is 0.

            :param rgw_step:
                *OPTIONAL* Step by which remote gw needs to be incremented per rule.
                Default is 0

                When this is used,  remote_gw should not be an array of IPs

            :param rgw_step_term:
                *OPTIONAL* Step by which remote gw needs to be incremented per term.
                Default is 0.

            :param base_ifl:
                *OPTIONAL* Base IFL.
                Default is 1

            :param ifl_step:
                *OPTIONAL* IFL Step for every tunnel.
                Default is 2

            :return:
                True on success , Raise exception on failure

            EXAMPLE::

                   configure ipsec vpn rule  ${ipsec_obj}
    """
    return ipsec_obj.set_rule(**kwargs)
