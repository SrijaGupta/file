"""
Copyright (C) 2016-2017, Juniper Networks, Inc.
All rights reserved.
Author: Venu Nalladhimmu, vgreddy@juniper.net
Description: srx ipsec vpn keywords
"""

import re
import time
import datetime
from pprint import pprint
import jxmlease
from jnpr.toby.utils.iputils import is_ip_ipv4
from jnpr.toby.hldcl import device as dev


class IpsecSrx(object):
    """
    Class factory to configure srx ipsec vpn
    """

    def __init__(self, **kwargs):
        """
            Method to initialize IPsec object

        """


# function to get ipsec sa statistics
# -------------------------------------
def get_ipsec_pkt_stats(device_handle, **kwargs):
    """Get ipsec data statistics
    :param device_handle:
        **REQUIRED** device object
    :param index:
        *OPTIONAL* ipsec sa index to get per tunnel ipsec data statistics
    : param ha_link:
        *OPTIONAL* specify boolean True or False to fetch ha link encr tunnel stats
    : params fpc, pic:
        *OPTIONAL* specify perticular fpc and pic numbers to fetech the ipsec stats from
    :param node:
        *OPTIONAL* Provide node options are local/primary/all
    :return: A Dictionary will be return having ipsec data statistics
    Example : stats = get_ipsec_pkt_stats(R0)
    {'AH_AUTH_FAIL': 0,
     'BAD_HEAD': 0,
     'BAD_TRAIL': 0,
     'DBYTES': 2456,
     'DPKTS': 10,
     'EBYTES': 2345,
     'EPKTS': 10,
     'ESP_AUTH_FAIL': 0,
     'ESP_DECR_FAIL': 0,
     'IBYTES': 0,
     'IPKTS': 0,
     'OBYTES': 0,
     'OPKTS': 0,
     'REPLAY_ERRORS': 1}
    """

    cmd = "show security ipsec statistics "
    ha_link = kwargs.get('ha_link', 0)
    if ha_link:
        cmd = cmd + ' ha-link-encryption'
    if 'fpc' in kwargs and 'pic' in kwargs:
        cmd = cmd + ' fpc ' + kwargs.get('fpc') + ' pic ' + kwargs.get('pic')
    if 'index' in kwargs:
        cmd = cmd + ' index ' + str(kwargs.get('index'))
    if 'node' in kwargs:
        cmd = cmd + ' node ' + str(kwargs.get('node'))
    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    encr_pkts = resp.findall('.//esp-encrypted-packets')
    decr_pkts = resp.findall('.//esp-decrypted-packets')
    encr_bytes = resp.findall('.//esp-encrypted-bytes')
    decr_bytes = resp.findall('.//esp-decrypted-bytes')
    in_pkts = resp.findall('.//ah-input-packets')
    out_pkts = resp.findall('.//ah-output-packets')
    in_bytes = resp.findall('.//ah-input-bytes')
    out_bytes = resp.findall('.//ah-output-bytes')
    ah_auth_fail = resp.findall('.//ah-authentication-failures')
    replay_errors = resp.findall('.//replay-errors')
    esp_auth_fail = resp.findall('.//esp-authentication-failures')
    esp_decr_fail = resp.findall('.//esp-decryption-failures')
    bad_headers = resp.findall('.//bad-headers')
    bad_trailers = resp.findall('.//bad-trailers')
    if str(kwargs.get('node')) != '1':
        stats = dict(EPKTS=int(encr_pkts[0].text),
                     DPKTS=int(decr_pkts[0].text),
                     EBYTES=int(encr_bytes[0].text),
                     DBYTES=int(decr_bytes[0].text),
                     IPKTS=int(in_pkts[0].text),
                     OPKTS=int(out_pkts[0].text),
                     IBYTES=int(in_bytes[0].text),
                     OBYTES=int(out_bytes[0].text),
                     AH_AUTH_FAIL=int(ah_auth_fail[0].text),
                     REPLAY_ERRORS=int(replay_errors[0].text),
                     ESP_AUTH_FAIL=int(esp_auth_fail[0].text),
                     ESP_DECR_FAIL=int(esp_decr_fail[0].text),
                     BAD_HEAD=int(bad_headers[0].text),
                     BAD_TRAIL=int(bad_trailers[0].text))
    else:
        stats = dict(EPKTS=int(encr_pkts[1].text),
                     DPKTS=int(decr_pkts[1].text),
                     EBYTES=int(encr_bytes[1].text),
                     DBYTES=int(decr_bytes[1].text),
                     IPKTS=int(in_pkts[1].text),
                     OPKTS=int(out_pkts[1].text),
                     IBYTES=int(in_bytes[1].text),
                     OBYTES=int(out_bytes[1].text),
                     AH_AUTH_FAIL=int(ah_auth_fail[1].text),
                     REPLAY_ERRORS=int(replay_errors[1].text),
                     ESP_AUTH_FAIL=int(esp_auth_fail[1].text),
                     ESP_DECR_FAIL=int(esp_decr_fail[1].text),
                     BAD_HEAD=int(bad_headers[1].text),
                     BAD_TRAIL=int(bad_trailers[1].text))
    pprint(stats)
    return stats


# verify ipsec data statistics
# ---------------------------------
def verify_ipsec_pkt_stats(device_handle, expected_stats=None, **kwargs):
    """
    verify ipsec data statistics

    :param device_handle:
        **REQUIRED** device object
    :param  expected_stats:
        **REQUIRED** pass a dictionary of values need to verify, dictionary consists of expected
        values of 'AH_AUTH_FAIL' 'BAD_HEAD' 'BAD_TRAIL' 'DBYTES''DPKTS' 'EBYTES'
        'EPKTS''ESP_AUTH_FAIL' 'ESP_DECR_FAIL' 'IN_BYTES' 'IN_PKTS' 'OUT_BYTES'
        'OUT_PKTS' 'REPLAY_ERRORS'
        dictionary keys should be same as get_ipsec_pkt_stats method return dictionary keys
    :param kwargs:
    *OPTIONAL* index is ipsec sa index,
    node is local/primary/all from where to collect ipsec statistics in HA mode
    ha_link as 0/1 for ha link tunnel and fpc/pic numbers for specific slot numbers
    :return: true or false based on findings

    Example :
    verify_ipsec_stats(device_handle, expected_stats={'EPKTS':24, 'DPKTS':24,
    'REPLAY_ERRORS':0})

    """

    actual_stats = get_ipsec_pkt_stats(device_handle, **kwargs)
    result = True
    for key in expected_stats:
        if expected_stats[key] == actual_stats[key]:
            device_handle.log(message='actual ' + key + 'count is' + str(actual_stats[key])
                              + ' matching with expected count ' + str(expected_stats[key]))
        else:
            device_handle.log(message='actual ' + key + 'count is' + str(actual_stats[key])
                              + ' not matching with expected count ' + str(expected_stats[key]), level='error')
            result = False
    return result


# function to get ike sa information
# -------------------------------------
def get_ike_sa(device_handle, **kwargs):
    """
    Get Ike security-associations information

    :param device_handle:
        **REQUIRED** device object
    :param family:
        *OPTIONAL* get ike sa information based on tunnel type ipv4 or ipv6
    :param index:
        *OPTIONAL* get ike sa information based on sa index
    :param peer_ip:
        *OPTIONAL* get ike sa information based on peer ip address
    :param detail:
        *OPTIONAL* get ike sa information in detail, default is brief
    :param dic_key:
        *OPTIONAL* Build dictionary bsed on dic_key value, can be id or ip,
        id returns dictionary by setting index as key
        and ip returns dictionary by setting remote_ip as key, default is ip
    :return: A Dictionary of dictionaries will be return ike security-associations information,
    dictionary of dictionary key value is peer ip address
    Example :  p1_sa = get_ike_sa(device_handle)
    {'3.3.3.2': {'index': 3922268,
                 'init_cookie': '1e29005494f73fb3',
                 'mode': 'IKEv2',
                 'remote_ip': '3.3.3.2',
                 'resp_cookie': '835a88571b16a29f',
                 'state': 'UP'},
     '5.5.5.2': {'index': 3922267,
                 'init_cookie': '95ccf59c2783de54',
                 'mode': 'IKEv2',
                 'remote_ip': '5.5.5.2',
                 'resp_cookie': 'fec2c4b00faf0495',
                 'state': 'UP'},
     'total': 2}
    Example : p1_sa = get_ike_sa(device_handle, detail=1)
    {'3.3.3.2': {'auth_algo': 'hmac-sha1-96',
                 'auth_method': 'RSA-signatures',
                 'dh_group': 'DH-group-5',
                 'encr_algo': 'aes256-cbc',
                 'index': 3922268,
                 'init_cookie': '1e29005494f73fb3',
                 'lifetime': 21458,
                 'local__id': 'C=US, DC=juniper, ST=CA, L=Sunnyvale, O=Juniper, '
                              'OU=engineering, CN=eng_hub',
                 'local_ip': '2.2.2.2',
                 'local_port': '500',
                 'mode': 'IKEv2',
                 'name': 'ADVPN_SUGGESTER_GW',
                 'prf_algo': 'hmac-sha1',
                 'remote_id': 'C=US, DC=juniper, ST=CA, L=Sunnyvale, O=Juniper, '
                              'OU=engineering, CN=eng_spoke1',
                 'remote_ip': '3.3.3.2',
                 'remote_port': '500',
                 'resp_cookie': '835a88571b16a29f',
                 'role': 'responder',
                 'state': 'UP',
                 'status': 'IKE SA is created',
                 'xauth_ip': '0.0.0.0',
                 'frag': 'Enabled',
                 'frag_size': '576',
                 'reauth': 'Expires in 1973 seconds',
                 'xauth_user': None},
     '5.5.5.2': {'auth_algo': 'hmac-sha1-96',
                 'auth_method': 'RSA-signatures',
                 'dh_group': 'DH-group-5',
                 'encr_algo': 'aes256-cbc',
                 'index': 3922267,
                 'init_cookie': '95ccf59c2783de54',
                 'lifetime': 11242,
                 'local__id': 'C=US, DC=juniper, ST=CA, L=Sunnyvale, O=Juniper, '
                              'OU=engineering, CN=eng_hub',
                 'local_ip': '2.2.2.2',
                 'local_port': '500',
                 'mode': 'IKEv2',
                 'name': 'ADVPN_SUGGESTER_GW',
                 'prf_algo': 'hmac-sha1',
                 'remote_id': 'C=US, DC=juniper, ST=CA, L=Sunnyvale, O=Juniper, '
                              'OU=engineering, CN=eng_spoke2',
                 'remote_ip': '5.5.5.2',
                 'remote_port': '500',
                 'resp_cookie': 'fec2c4b00faf0495',
                 'role': 'responder',
                 'state': 'UP',
                 'status': 'IKE SA is created',
                 'xauth_ip': '0.0.0.0',
                 'frag': 'Enabled',
                 'frag_size': '576',
                 'reauth': 'Disabled',
                 'xauth_user': None},
     'total': 2}
    """

    cmd = "show security ike security-associations "
    detail = kwargs.get('detail', 0)
    dic_key = kwargs.get('dic_key', 'ip')
    ha_link = kwargs.get('ha_link', 0)
    if ha_link:
        cmd = cmd + ' ha-link-encryption '
    if 'family' in kwargs:
        if kwargs.get('family') == 'ipv6':
            cmd += 'family inet6 '
        else:
            cmd += 'family inet '
    if 'peer_ip' in kwargs:
        cmd += kwargs.get('peer_ip')
    elif 'index' in kwargs:
        cmd += 'index ' + str(kwargs.get('index'))
    if detail:
        cmd += ' detail'
    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    ike_sa = dict()
    cnt = 0
    act_cnt = 0
    if resp is not None:
        if detail:
            remote_ip = resp.findall('.//ike-security-associations-block/ike-sa-remote-address')
            index = resp.findall('.//ike-sa-index')
            gw_name = resp.findall('.//ike-gw-name')
            role = resp.findall('.//ike-sa-role')
            state = resp.findall('.//ike-sa-state')
            init_cookie = resp.findall('.//ike-sa-initiator-cookie')
            resp_cookie = resp.findall('.//ike-sa-responder-cookie')
            mode = resp.findall('.//ike-sa-exchange-type')
            auth_method = resp.findall('.//ike-sa-authentication-method')
            local_ip = resp.findall('.//ike-sa-local-address')
            local_port = resp.findall('.//ike-sa-local-port')
            remote_port = resp.findall('.//ike-sa-remote-port')
            lifetime = resp.findall('.//ike-sa-lifetime')
            local_id = resp.findall('.//ike-sa-local-id')
            remote_id = resp.findall('.//ike-sa-remote-id')
            xauth_user = resp.findall('.//ike-xauth-username')
            xauth_ip = resp.findall('.//ike-xauth-user-assigned-ip')
            auth_algo = resp.findall('.//ike-sa-authentication-algorithm')
            encr_algo = resp.findall('.//ike-sa-encryption-algorithm')
            prf_algo = resp.findall('.//ike-sa-prf-algorithm')
            dh_group = resp.findall('.//ike-sa-dhgroup')
            sa_flag = resp.findall('.//ike-sa-flags')
            reauth = resp.findall('.//ike-sa-reauthlifetime')
            frag = resp.findall('.//ike-sa-ike-frag')
            frag_size = resp.findall('.//ike-sa-frag-size')
            while cnt < len(index):
                sa_info = dict()
                sa_info['index'] = int(index[cnt].text)
                sa_info['name'] = gw_name[cnt].text
                sa_info['role'] = role[cnt].text
                sa_info['state'] = state[cnt].text
                sa_info['init_cookie'] = init_cookie[cnt].text
                sa_info['resp_cookie'] = resp_cookie[cnt].text
                sa_info['mode'] = mode[cnt].text
                sa_info['auth_method'] = auth_method[cnt].text
                sa_info['local_ip'] = local_ip[cnt].text
                sa_info['local_port'] = local_port[cnt].text
                sa_info['remote_ip'] = remote_ip[cnt].text
                sa_info['remote_port'] = remote_port[cnt].text
                lft = re.findall(r'\d+', lifetime[cnt].text)
                sa_info['lifetime'] = int(lft[0])
                sa_info['local__id'] = local_id[cnt].text
                sa_info['remote_id'] = remote_id[cnt].text
                sa_info['xauth_user'] = xauth_user[cnt].text
                sa_info['xauth_ip'] = xauth_ip[cnt].text
                sa_info['auth_algo'] = auth_algo[cnt].text
                sa_info['encr_algo'] = encr_algo[cnt].text
                sa_info['prf_algo'] = prf_algo[cnt].text
                sa_info['dh_group'] = dh_group[cnt].text
                sa_info['status'] = sa_flag[cnt].text
                sa_info['reauth'] = reauth[cnt].text
                sa_info['frag'] = frag[cnt].text
                sa_info['frag_size'] = frag_size[cnt].text
                if dic_key == 'ip':
                    sa_key = remote_ip[cnt].text
                else:
                    sa_key = int(index[cnt].text)
                if sa_info['state'] == 'UP':
                    act_cnt += 1
                cnt += 1
                ike_sa[sa_key] = sa_info
        else:
            remote_ip = resp.findall('.//ike-sa-remote-address')
            index = resp.findall('.//ike-sa-index')
            state = resp.findall('.//ike-sa-state')
            init_cookie = resp.findall('.//ike-sa-initiator-cookie')
            resp_cookie = resp.findall('.//ike-sa-responder-cookie')
            mode = resp.findall('.//ike-sa-exchange-type')
            while cnt < len(index):
                sa_info = dict()
                sa_info['remote_ip'] = remote_ip[cnt].text
                sa_info['index'] = int(index[cnt].text)
                sa_info['state'] = state[cnt].text
                sa_info['init_cookie'] = init_cookie[cnt].text
                sa_info['resp_cookie'] = resp_cookie[cnt].text
                sa_info['mode'] = mode[cnt].text
                if dic_key == 'ip':
                    sa_key = remote_ip[cnt].text
                else:
                    sa_key = int(index[cnt].text)
                if sa_info['state'] == 'UP':
                    act_cnt += 1
                cnt += 1
                ike_sa[sa_key] = sa_info
    ike_sa['total'] = act_cnt
    pprint(ike_sa)
    return ike_sa


# Function to get ipsec sa information
# -----------------------------------------
def get_ipsec_sa(device_handle, **kwargs):
    """
    Get IPsec security-associations information

    :param device_handle:
        **REQUIRED** device object
    :param family:
        *OPTIONAL* get ipsec sa information based on tunnel type ipv4 or ipv6
    :param vpn_name:
        *OPTIONAL* get ipsec sa information based on the name of vpn object
    :param ts_name:
        *OPTIONAL* get ipsec sa information based on the name of traffic-selector object
    :param sa_type:
        *OPTIONAL* get ipsec sa information based on the type of sa(shortcut)
    :param dic_key:
        *OPTIONAL* Build dictionary bsed on dic_key value, can be id or ip, id returns dictionary
        by setting index as key and ip returns dictionary by setting remote_ip as key,
        default is ip
    :return: A Dictionary of dictionaries will return as ipsec security-associations information,
    dictionary of dictionary key value is sa index
    values can be accessed through 'auth_algo'  'protocol' 'encr_algo'  'local_ip'  'local_port'
    'remote_ip'  'remote_port'  'index'  'in_spi'  'lifetime'  'lifesize' 'name'   'out_spi'  'role'
    'state'  'status'  'monitor'
    Example : p2_sa = pmi(device_handle)
    {'3.3.3.2': {'auth_algo': 'sha256',
                 'encr_algo': 'aes-cbc-192',
                 'in_spi': 'e3ec43b9',
                 'index': 67108866,
                 'lifesize': '150000',
                 'lifetime': 264,
                 'local_port': 500,
                 'monitor': '-',
                 'out_spi': 'ef2490a3',
                 'protocol': 'ESP',
                 'remote_ip': '3.3.3.2',
                 'remote_port': 500,
                 'state': 'up'},
     '5.5.5.2': {'auth_algo': 'sha256',
                 'encr_algo': 'aes-cbc-192',
                 'in_spi': 'cf7057b5',
                 'index': 67108867,
                 'lifesize': '150000',
                 'lifetime': 302,
                 'local_port': 500,
                 'monitor': '-',
                 'out_spi': '6fe3f60e',
                 'protocol': 'ESP',
                 'remote_ip': '5.5.5.2',
                 'remote_port': 500,
                 'state': 'up'},
     'total': 2}
    Example : p2_sa = get_ipsec_sa(device_handle, dic_key='id')
    {67108866: {'auth_algo': 'sha256',
                'encr_algo': 'aes-cbc-192',
                'in_spi': 'e3ec43b9',
                'index': 67108866,
                'lifesize': '150000',
                'lifetime': 264,
                'local_port': 500,
                'monitor': '-',
                'out_spi': 'ef2490a3',
                'protocol': 'ESP',
                'remote_ip': '3.3.3.2',
                'remote_port': 500,
                'state': 'up'},
     67108867: {'auth_algo': 'sha256',
                'encr_algo': 'aes-cbc-192',
                'in_spi': 'cf7057b5',
                'index': 67108867,
                'lifesize': '150000',
                'lifetime': 302,
                'local_port': 500,
                'monitor': '-',
                'out_spi': '6fe3f60e',
                'protocol': 'ESP',
                'remote_ip': '5.5.5.2',
                'remote_port': 500,
                'state': 'up'},
     'total': 2}
    """

    ipsec_sa = dict()
    cmd = "show security ipsec security-associations "
    dic_key = kwargs.get('dic_key', 'ip')
    ha_link = kwargs.get('ha_link', 0)
    if ha_link:
        cmd = cmd + ' ha-link-encryption '
    if 'family' in kwargs:
        if kwargs.get('family') == 'ipv6':
            cmd += 'family inet6 '
        else:
            cmd += 'family inet '
    if 'sa_type' in kwargs:
        cmd = cmd + 'sa-type ' + kwargs.get('sa_type')
    if 'vpn_name' in kwargs:
        cmd = cmd + 'vpn-name ' + kwargs.get('vpn_name')
    if 'ts_name' in kwargs:
        cmd = cmd + 'traffic-selector ' + kwargs.get('ts_name')
    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    rpc_resp = device_handle.execute_rpc(command=rpc_eq).response()
    resp = jxmlease.parse_etree(rpc_resp)
    if 'multi-routing-engine-results' in resp.keys():
        device_handle.log(" device is chassis cluster mode")
        resp = resp['multi-routing-engine-results']['multi-routing-engine-item']
    else:
        device_handle.log(" device is not in chassis cluster mode")
    if int(resp['ipsec-security-associations-information']['total-active-tunnels']) == 0:
        device_handle.log("No SA found")
        ipsec_sa['total'] = 0
        return ipsec_sa
    sa_info = resp['ipsec-security-associations-information']['ipsec-security-associations-block']
    if int(resp['ipsec-security-associations-information']['total-active-tunnels']) > 1:
        for msa in sa_info:
            ipsec = dict()
            ipsec['index'] = int(msa['ipsec-security-associations'][0]['sa-tunnel-index'])
            ipsec['state'] = str(msa['sa-block-state'])
            if '/' in msa['ipsec-security-associations'][0]['sa-esp-encryption-algorithm']:
                ipsec['encr_algo'] = str(
                    msa['ipsec-security-associations'][0]['sa-esp-encryption-algorithm'].strip('/'))
            else:
                ipsec['encr_algo'] = str(msa['ipsec-security-associations'][0]['sa-esp-encryption-algorithm'])
            ipsec['auth_algo'] = str(msa['ipsec-security-associations'][0]['sa-hmac-algorithm'])
            if ':' in msa['ipsec-security-associations'][0]['sa-protocol']:
                ipsec['protocol'] = str(msa['ipsec-security-associations'][0]['sa-protocol'].strip(':'))
            else:
                ipsec['protocol'] = str(msa['ipsec-security-associations'][0]['sa-protocol'])
            ipsec['local_port'] = int(msa['ipsec-security-associations'][0]['sa-port'])
            ipsec['remote_port'] = int(msa['ipsec-security-associations'][1]['sa-port'])
            ipsec['remote_ip'] = str(msa['ipsec-security-associations'][0]['sa-remote-gateway'])
            ipsec['in_spi'] = str(msa['ipsec-security-associations'][0]['sa-spi'])
            ipsec['out_spi'] = str(msa['ipsec-security-associations'][1]['sa-spi'])
            if 'sa-hard-lifetime' in msa['ipsec-security-associations'][0]:
                if 'expir' in msa['ipsec-security-associations'][0]['sa-hard-lifetime']:
                    ipsec['lifetime'] = 'expir'
                elif '/' in msa['ipsec-security-associations'][0]['sa-hard-lifetime']:
                    ipsec['lifetime'] = int(msa['ipsec-security-associations'][0]['sa-hard-lifetime'].strip('/'))
                else:
                    lft = re.findall(r'\d+', msa['ipsec-security-associations'][0]['sa-hard-lifetime'])
                    ipsec['lifetime'] = lft[0]
                ipsec['lifesize'] = str(msa['ipsec-security-associations'][0]['sa-lifesize-remaining'])
            if 'sa-vpn-monitoring-state' in msa['ipsec-security-associations'][0].keys():
                ipsec['monitor'] = str(msa['ipsec-security-associations'][0]['sa-vpn-monitoring-state'])
            if dic_key == 'ip':
                sa_key = ipsec['remote_ip']
            else:
                sa_key = ipsec['index']
            ipsec_sa[sa_key] = ipsec
    else:
        ipsec = dict()
        ipsec['index'] = int(sa_info['ipsec-security-associations'][0]['sa-tunnel-index'])
        ipsec['state'] = str(sa_info['sa-block-state'])
        if '/' in sa_info['ipsec-security-associations'][0]['sa-esp-encryption-algorithm']:
            ipsec['encr_algo'] = str(sa_info['ipsec-security-associations'][0]['sa-esp-encryption-algorithm'].strip('/'))
        else:
            ipsec['encr_algo'] = str(sa_info['ipsec-security-associations'][0]['sa-esp-encryption-algorithm'])
        ipsec['auth_algo'] = str(sa_info['ipsec-security-associations'][0]['sa-hmac-algorithm'])
        if ':' in sa_info['ipsec-security-associations'][0]['sa-protocol']:
            ipsec['protocol'] = str(sa_info['ipsec-security-associations'][0]['sa-protocol'].strip(':'))
        else:
            ipsec['protocol'] = str(sa_info['ipsec-security-associations'][0]['sa-protocol'])
        ipsec['local_port'] = int(sa_info['ipsec-security-associations'][0]['sa-port'])
        ipsec['remote_port'] = int(sa_info['ipsec-security-associations'][1]['sa-port'])
        ipsec['remote_ip'] = str(sa_info['ipsec-security-associations'][0]['sa-remote-gateway'])
        ipsec['in_spi'] = str(sa_info['ipsec-security-associations'][0]['sa-spi'])
        ipsec['out_spi'] = str(sa_info['ipsec-security-associations'][1]['sa-spi'])
        if 'sa-hard-lifetime' in sa_info['ipsec-security-associations'][0]:
            if '/' in sa_info['ipsec-security-associations'][0]['sa-hard-lifetime']:
                ipsec['lifetime'] = int(sa_info['ipsec-security-associations'][0]['sa-hard-lifetime'].strip('/'))
            else:
                lft = re.findall(r'\d+', sa_info['ipsec-security-associations'][0]['sa-hard-lifetime'])
                ipsec['lifetime'] = lft[0]
            ipsec['lifesize'] = str(sa_info['ipsec-security-associations'][0]['sa-lifesize-remaining'])
        if 'sa-vpn-monitoring-state' in sa_info['ipsec-security-associations'][0].keys():
            ipsec['monitor'] = str(sa_info['ipsec-security-associations'][0]['sa-vpn-monitoring-state'])
        if dic_key == 'ip':
            sa_key = ipsec['remote_ip']
        else:
            sa_key = ipsec['index']
        ipsec_sa[sa_key] = ipsec
    ipsec_sa['total'] = len(ipsec_sa)
    pprint(ipsec_sa)
    return ipsec_sa


# function to verify ike sa rekey
# -----------------------------------------
def verify_ike_rekey(ike_cookie_old=None, ike_cookie_new=None, rekey=1):
    """
    Verify ike sa rekey

    :param ike_cookie_old:
        **REQUIRED**  first set of ike SA initiator and responder cookie as list
    :param ike_cookie_new:
        **REQUIRED**  second set of ike SA initiator and responder cookie as list
    :param rekey:
        **OPTIONAL**  Specify rekey value 0 if rekey is not expected and 1 if rekey expected,
         default value is 1
    :return: true if successful or raise assertion for failure

    Example - verify_ike_rekey(ike_cookie_old=[10,11], ike_cookie_new=[10,11], rekey=0)
    """
    if ike_cookie_old is None or ike_cookie_new is None:
        raise KeyError("Missing mandatory arguments, pass two set of ike sa cookies to compare")

    if ike_cookie_old[0] == ike_cookie_new[0] and ike_cookie_old[1] == ike_cookie_new[1]:
        print("cookie values are same, ike SAs are same")
        rekeyed = 0
    else:
        print("cookie values are different,ike SAs are different")
        rekeyed = 1
    if rekey == 1:
        if rekeyed:
            print('ike sa rekeyed, pass')
        else:
            raise Exception("ike sa not rekeyed")
    else:
        if rekeyed:
            raise Exception("ike sa rekeyed")
        else:
            print('ike sa not rekeyed,pass')
    return True


# function to verify ipsec sa rekey
# -----------------------------------------
def verify_ipsec_rekey(ipsec_spi_old=None, ipsec_spi_new=None, rekey=1):
    """
    Verify ipsec sa rekey

    :param ipsec_spi_old:
        **REQUIRED**  first set of IPsec SA initiator and responder cookie as list
    :param ipsec_spi_new:
        **REQUIRED**  second set of IPsec SA initiator and responder cookie as list
    :param rekey:
        **OPTIONAL**  Specify rekey value 0 if rekey is not expected and 1 if rekey expected,
        default value is 1
    :return: true if successful or raise assertion for failure

    Example - verify_ipsec_rekey(ipsec_spi_old=[10,11], ipsec_spi_new=[10,11], rekey=0)
    """
    if ipsec_spi_old is None or ipsec_spi_new is None:
        raise KeyError("Missing mandatory arguments, pass two set of ipsec sa SPIs to compare")

    if ipsec_spi_old[0] == ipsec_spi_new[0] and ipsec_spi_old[1] == ipsec_spi_new[1]:
        print("SPI values are same, IPsec SAs are same")
        rekeyed = 0
    else:
        print("SPI values are different,IPsec SAs are different")
        rekeyed = 1
    if rekey == 1:
        if rekeyed:
            print('ipsec sa rekeyed, pass')
        else:
            raise Exception("ipsec sa not rekeyed")
    else:
        if rekeyed:
            raise Exception("ipsec sa rekeyed")
        else:
            print('ipsec sa not rekeyed,pass')
    return True


# function to verify ike sa information
#  -----------------------------------------
def verify_ike_sa_status(device_handle, peer_ip=None, **kwargs):
    """
    Verify Ike security-associations information

    :param device_handle:
        **REQUIRED** device object
    :param peer_ip:
        **REQUIRED** verify ike sa information based on peer ip address or address list
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success
          retry_interval is interval gap between each retry
    :return: true if successful or raise assertion for failure

    Example - verify_ike_sa_status(r0, peer_ip=['1.1.1.1','1.1.1.2'])
              verify_ike_sa_status(r0, peer_ip='1.1.1.1',negative=1)
    """
    detail = kwargs.get('detail', 0)
    retry = kwargs.get('retry', 10)
    retry_interval = kwargs.get('retry_interval', 2)
    negative = kwargs.get('negative', 0)
    halink = kwargs.get('ha_link', 0)
    i = 1
    if peer_ip is None:
        raise KeyError("Missing mandatory arguments, pass vpn remote address list")
    if isinstance(peer_ip, list):
        ip_list = peer_ip
    else:
        ip_list = [peer_ip]
    for ip_addr in ip_list:
        while i <= retry:
            ike_sa = get_ike_sa(device_handle, peer_ip=ip_addr, detail=detail, ha_link=halink)
            if negative != 0:
                if ip_addr in ike_sa and ike_sa[ip_addr]['state'] == 'UP':
                    device_handle.log(message='found ike sa up for %s, retry' % ip_addr)
                    time.sleep(retry_interval)
                    if i == retry:
                        raise Exception("found ike sa for peer " + ip_addr)
                    i += 1
                else:
                    device_handle.log(message='Ike sa not up for peer %s' % ip_addr)
                    break
            else:
                if ip_addr not in ike_sa or ike_sa[ip_addr]['state'] != 'UP':
                    device_handle.log(message="Ike sa not up for %s, retry" % ip_addr)
                    time.sleep(retry_interval)
                    if i == retry:
                        raise Exception("not found ike sa up for peer " + ip_addr)
                    i += 1
                else:
                    device_handle.log(message="found ike sa for peer %s" % ip_addr)
                    break
    return True


# function to verify ipsec sa information
#  -----------------------------------------
def verify_ipsec_sa_status(device_handle, peer_ip=None, **kwargs):
    """
    Verify Ike security-associations information

    :param device_handle:
        **REQUIRED** device object
    :param peer_ip:
        **REQUIRED** verify ipsec sa information based on peer ip address or address list
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success
         retry_interval is interval gap between each retry
    :return: true if successful or raise assertion for failure

    Example - verify_ipsec_sa_status(r0, peer_ip=['1.1.1.1','1.1.1.2'])
              verify_ipsec_sa_status(r0, peer_ip='1.1.1.1', negative=1)
    """
    retry = kwargs.get('retry', 10)
    retry_interval = kwargs.get('retry_interval', 2)
    negative = kwargs.get('negative', 0)
    halink = kwargs.get('ha_link', 0)
    i = 1
    if peer_ip is None:
        raise KeyError("Missing mandatory arguments, pass vpn remote address list")
    if isinstance(peer_ip, list):
        ip_list = peer_ip
    else:
        ip_list = [peer_ip]

    for ip_addr in ip_list:
        while i <= retry:
            if 'vpn_name' in kwargs:
                ipsec_sa = get_ipsec_sa(device_handle, dic_key='ip',
                                        vpn_name=kwargs.get('vpn_name'), ha_link=halink)
            elif 'ts_name' in kwargs:
                ipsec_sa = get_ipsec_sa(device_handle, dic_key='ip',
                                        ts_name=kwargs.get('ts_name'), ha_link=halink)
            else:
                ipsec_sa = get_ipsec_sa(device_handle, dic_key='ip', ha_link=halink)
            if negative != 0:
                if ip_addr in ipsec_sa and ipsec_sa[ip_addr]['state'] == 'up':
                    device_handle.log(message='found ipsec sa up for %s, retry' % ip_addr)
                    time.sleep(retry_interval)
                    if i == retry:
                        raise Exception("found ipsec sa for peer " + ip_addr)
                    i += 1
                else:
                    device_handle.log(message='IPsec sa up for %s, retry' % ip_addr)
                    break
            else:
                if ip_addr not in ipsec_sa or ipsec_sa[ip_addr]['state'] != 'up':
                    device_handle.log(message='IPsec sa not up for %s, retry' % ip_addr)
                    time.sleep(retry_interval)
                    if i == retry:
                        raise Exception("not found IPsec sa up for peer " + ip_addr)
                    i += 1
                else:
                    device_handle.log(message='found IPsec sa up for %s' % ip_addr)
                    break
    return True


# function to verify ike sa count
#  -----------------------------------------
def verify_ike_sa_count(device_handle, count=None, **kwargs):
    """
    Verify Ike security-associations count

    :param device_handle:
        **REQUIRED** device object
    :param count:
        **REQUIRED** ike sa count expected value
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success
         retry_interval is interval gap between each retry
    :return: true if successful or raise assertion for failure

    Example - P: verify_ike_sa_count(r0, count=10)
              R: verify ike sa count  r0  count=${10}
    """
    retry = kwargs.get('retry', 10)
    retry_interval = kwargs.get('retry_interval', 2)
    halink = kwargs.get('ha_link', 0)
    if count is None:
        raise KeyError("Missing mandatory arguments, need expected ike sa count")
    i = 1

    while i <= retry:
        if 'family' in kwargs:
            ike_sa = get_ike_sa(device_handle, family=kwargs.get('family'),
                                dic_key=id, ha_link=halink)
        else:
            ike_sa = get_ike_sa(device_handle, dic_key=id, ha_link=halink)
        if ike_sa['total'] != int(count):
            device_handle.log(message="total ike sa count is %d, but expected is %d, retry "
                              % (ike_sa['total'], count))
            time.sleep(retry_interval)
            if i == retry:
                raise Exception("total ike sa count is %d not correct" % ike_sa['total'])
            i += 1
        else:
            device_handle.log(message="total ike sa count is %d" % ike_sa['total'])
            break
    return True


# function to verify ipsec sa count
#  -----------------------------------------
def verify_ipsec_sa_count(device_handle, count=None, sa_count=None, **kwargs):
    """
    Verify ipsec tunnel/security-associations count

    :param device_handle:
        **REQUIRED** device object
    :param count:
        **REQUIRED** ipsec tunnel count expected value
    :param sa_count:
        **REQUIRED** ipsec sa count expected value
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success,
        retry_interval is interval gap between each retry
        vpn_name is the name of vpn object
        ts_name is name of traffic-selector
    :return: true if successful or raise assertion for failure

    Example - P: verify_ipsec_sa_count(r0, count=10)
              R: verify ipsec sa count  r0  count=${10}
    """
    retry = kwargs.get('retry', 10)
    retry_interval = kwargs.get('retry_interval', 2)
    halink = kwargs.get('ha_link', 0)
    if count is None:
        raise KeyError("Missing mandatory arguments, need expected ipsec tunnel count")
    i = 1
    while i <= retry:
        if halink:
            if sa_count is None:
                raise KeyError("Missing mandatory arguments, need expected ipsec sa count")
            (tunnel_cnt, sa_cnt) = get_total_ipsec_tunnel_and_sa_count(device_handle, ha_link=1)
            if int(count) == tunnel_cnt and int(sa_count) == sa_cnt:
                device_handle.log(message="total ipsec tunnel and sa count is matching with expected count")
                break
            else:
                if i == retry:
                    raise Exception("total ipsec tunnel and sa count is not matching with expected count")
                i += 1
        else:
            if 'family' in kwargs:
                ipsec_sa = get_ipsec_sa(device_handle, family=kwargs.get('family'), dic_key=id)
            elif 'vpn_name' in kwargs:
                ipsec_sa = get_ipsec_sa(device_handle, vpn_name=kwargs.get('vpn_name'), dic_key=id)
            elif 'ts_name' in kwargs:
                ipsec_sa = get_ipsec_sa(device_handle, vpn_name=kwargs.get('ts_name'), dic_key=id)
            else:
                ipsec_sa = get_ipsec_sa(device_handle, dic_key=id)
            if ipsec_sa['total'] != int(count):
                device_handle.log(message="total ipsec sa count is %d and expected is %d, retry"
                                  % (ipsec_sa['total'], count))
                time.sleep(retry_interval)
                if i == retry:
                    raise Exception("total ipsec sa count is %d not correct" % ipsec_sa['total'])
                i += 1
            else:
                device_handle.log("found expected number of ipsec sa %d" % ipsec_sa['total'])
                break
    return True



# function to get ipsec tunnel and sa count as list
#  ------------------------------------------------
def get_total_ipsec_tunnel_and_sa_count(device_handle, **kwargs):
    """
    Get ipsec total tunnel and sa count

    :param device_handle:
        **REQUIRED** device object
    :param count:
        **REQUIRED** ipsec sa count expected value


    :return: return a list of tunnel and sa count values

    Example - P: (tunnel_count, sa_count) = get_total_ipsec_tunnel_and_sa_count(r0, ha_link=1)
              R: count = get total ipsec tunnel and sa count  r0  ha_link={1}
    """

    cmd = "show security ipsec sa "
    ha_link = kwargs.get('ha_link', 0)
    if ha_link:
        cmd = cmd + ' ha-link-encryption'
    if 'fpc' in kwargs and 'pic' in kwargs:
        cmd = cmd + ' fpc ' + str(kwargs.get('fpc')) + ' pic ' + str(kwargs.get('pic'))
    cmd = cmd + ' | display xml | match total'
    resp = device_handle.cli(command=cmd).response()
    count = re.findall(r'\d+', resp)
    tun_cnt = int(count[0])
    sa_cnt = int(count[1])
    device_handle.log(message="total ipsec tunnel count is %d and sa count is %d"
                      % (tun_cnt, sa_cnt))
    return [tun_cnt, sa_cnt]


# function to verify interface status
# -----------------------------------------
def verify_ifl_status(device_handle, ifl=None, status='up', **kwargs):
    """
    Verify Interface status

    :param device_handle:
        **REQUIRED** device object
    :param ifl:
        **REQUIRED** list of logical interface name to verify the status
    :param status:
        *OPTIONAL* expected status of the tunnel ifl up/down, default is up
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success,
        retry_interval is interval gap between each retry
    :return: true if successful or raise assertion for failure

    Example - verify_ifl_status(r0, ifl=['st0.1', 'st0.2'])
    verify_ifl_status(r0, ifl='st0.1', status='down')
    """
    retry = kwargs.get('retry', 10)
    retry_interval = kwargs.get('retry_interval', 2)
    if ifl is None:
        raise KeyError("Missing mandatory arguments, need interface ifl")
    i = 1
    if isinstance(ifl, list):
        ifl_list = ifl
    else:
        ifl_list = [ifl]
    for interface in ifl_list:
        cmd = "show interfaces terse " + interface
        rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
        while i <= retry:
            resp = device_handle.execute_rpc(command=rpc_eq).response()
            if resp.find('.//name') is not None:
                state = resp.findall('.//oper-status')
                if state[0].text == status:
                    device_handle.log(message="%s link state is %s" %(interface, state[0].text))
                    break
                else:
                    time.sleep(retry_interval)
                    if i == retry:
                        raise Exception("%s link state is %s" %(interface, state[0].text))
                    i += 1
            else:
                raise AssertionError('could not find interface information')
    return True


# verify pattern matching in given command in any device mode
# ----------------------------------------------------------
def verify_pattern(device_handle, cmd=None, pattern=None, mode='cli', **kwargs):
    """

    verify pattern matching for given command output in shell/cli/config/vty mode
    :param device_handle:
        **REQUIRED** device object
    :param cmd:
        **REQUIRED** operational cli command to collect the output
    :param pattern:
        **REQUIRED** list of patterns to be searched in command output
    :param mode:
        *OPTIONAL*  default is cli, user can specify shell/cli/config
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success,
        retry_interval is interval gap between each retry
    :return: true or false based on findings

    Example :
    verify_pattern(device_handle, cmd='show version', pattern=['Model: vsrx', 'Hostname: vsx2'])
    """

    if cmd is None or pattern is None:
        raise KeyError("Missing mandatory arguments, need cmd and pattern to verify")

    retry = kwargs.get('retry', 10)
    retry_interval = kwargs.get('retry_interval', 1)
    i = 1
    if isinstance(pattern, list):
        pat_list = pattern
    else:
        pat_list = [pattern]
    for pat in pat_list:
        while i <= retry:
            if mode == 'cli':
                resp = device_handle.cli(command=cmd).response()
            elif mode == 'shell':
                resp = device_handle.shell(command=cmd).response()
            elif mode == 'config':
                resp = device_handle.config(command_list=[cmd]).response()
            elif mode == 'vty':
                resp = device_handle.vty(command=cmd, destination=kwargs.get('pic')).response()
            else:
                raise KeyError("unknown mode for command execution")
            if pat.lower() in resp.lower():
                device_handle.log("found pattern %s in output" % pat)
                break
            else:
                time.sleep(retry_interval)
                device_handle.log("pattern %s not found, retry" % pat)
                i += 1
                if i > retry:
                    device_handle.log("not found pattern %s in output" % pat)
                    return False
    return True


# function to get ipsec sa statistics
# -------------------------------------
def get_ike_active_peer(device_handle, peer_ip=None, **kwargs):
    """Get ike active peer information
    :param device_handle:
        **REQUIRED** device object
    :param peer_ip:
        **REQUIRED** peer ip to verify status

    :return: A Dictionary will be return having active peer
    Example P: peer_info = get_ike_active_peer(R0, peer_ip='30.1.1.1')
            R: peer_info  Get Ike Active Peer  R0    peer_ip=30.1.1.1

            {'assigned_ip': '0.0.0.0',
             'remote_address': '30.1.1.1',
             'remote_id': 'C=US, DC=juniper, ST=CA, L=Sunnyvale, O=Juniper, '
              'OU=engineering, CN=SPOKE1',
             'remote_port': '500',
             'xauth_user': 'not available'}
    """

    cmd = "show security ike active-peer "
    ha_link = kwargs.get('ha_link', 0)
    if ha_link:
        cmd = cmd + ' ha-link-encryption '
    if peer_ip is None:
        raise KeyError("peer_ip argument must passed to function")
    cmd = cmd + peer_ip

    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    active_peer = dict()
    if resp.find('.//ike-sa-remote-address') is not None:
        remote_address = resp.findall('.//ike-sa-remote-address')
        remote_port = resp.findall('.//ike-sa-remote-port')
        remote_id = resp.findall('.//ike-ike-id')
        xauth_user = resp.findall('.//ike-xauth-username')
        assigned_ip = resp.findall('.//ike-xauth-user-assigned-ip')
        active_peer.update(remote_address=remote_address[0].text)
        active_peer.update(remote_port=remote_port[0].text)
        active_peer.update(remote_id=remote_id[0].text)
        active_peer.update(xauth_user=xauth_user[0].text)
        active_peer.update(assigned_ip=assigned_ip[0].text)
        pprint(active_peer)
        return active_peer
    else:
        device_handle.log(message="ike active peer information not found")
        return None


# function to get ipsec sa statistics
# -------------------------------------
def verify_ike_active_peer(device_handle, peer_ip=None, expect_values=None, **kwargs):
    """Verify active peer information
    :param device_handle:
        **REQUIRED** device object
    :param peer_ip:
        **REQUIRED** peer ip to verify status
    :param expect_values:
        **REQUIRED** dictionary of expect active peer values

    :return: true or false based on findings
    Example P: verify_ike_active_peer(R0, peer_ip='30.1.1.1',
               expect_values={'remote_port': '500', 'remote_address': '30.1.1.1'})
            R: Verify Ike Active Peer  R0    peer_ip=30.1.1.1
    """

    halink = kwargs.get('ha_link', 0)
    if peer_ip is None or expect_values is None:
        raise KeyError("peer_ip and expect_info argument must passed to function")

    actual_values = get_ike_active_peer(device_handle, peer_ip=peer_ip, ha_link=halink)
    if actual_values is None:
        device_handle.log(message="peer info not found in the active peer list", level='error')
        return False
    result = True
    for key in expect_values:
        if expect_values[key] == actual_values[key]:
            device_handle.log(message='actual ' + key + ' is ' + actual_values[key] + ' matching with expected ' + expect_values[key])
        else:
            device_handle.log(message='actual ' + key + ' is ' + actual_values[key] + ' not matching with expected ' + expect_values[key], level='error')
            result = False
    return result


# function to verify ipsec traffic-selector
# -----------------------------------------
def verify_ipsec_ts(device_handle, st_ifl=None, src_ip=None, dst_ip=None):
    """
    Verify IPsec traffic-selector

    :param device_handle:
        **REQUIRED** device object
    :param st_ifl:
        **REQUIRED** list of logical interface name to verify the status
    :param src_ip:
        *OPTIONAL* traffic-selector source-address
    :param dst_ip:
        *OPTIONAL* traffic-selector destination-address
    :param kwargs:
        *OPTIONAL*
    :return: true or false based on findings

    Example - P: verify_ipsec_ts(r0, st_ifl='st0.1', src_ip='10.0.1.0/24', dst_ip='20.0.1.0/24')
              R: Verify Ipsec Ts  r0  st_ifl='st0.1'  src_ip='10.0.1.0/24'  dst_ip='20.0.1.0/24'
    """

    if st_ifl is None:
        raise KeyError("Missing mandatory arguments, pass tunnel interface associated with traffic-selector")

    cmd = "show security ipsec traffic-selector interface-name " + st_ifl
    if src_ip is not None:
        cmd = cmd + " source-address " + src_ip
    if dst_ip is not None:
        cmd = cmd + " destination-address " + dst_ip
    cli_resp = device_handle.cli(command=cmd).response()
    if 'missing' in cli_resp:
        raise KeyError(cli_resp)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    if resp.find('.//sa-tunnel-index') is not None:
        device_handle.log(message="find matching traffic-selector for the tunnel interface %s" %(st_ifl))
        return True
    else:
        device_handle.log(message="not found any matching traffi-selector", level='error')
        return False


# function to verify ipsec nat traversal
#  -----------------------------------------
def verify_nat_traversal(device_handle, peer_ip=None, **kwargs):
    """
    Verify ipsec nat traversal

    :param device_handle:
        **REQUIRED** device object
    :param peer_ip:
        **REQUIRED** ipsec vpn remote peer address
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success
    :return: true if successful or raise assertion for failure

    Example - P: verify_nat_traversal(r0, peer_ip='1.1.1.1')
              R: Verify Nat Traversal  r0  peer_ip='1.1.1.1'
    """

    halink = kwargs.get('ha_link', 0)
    if peer_ip is None:
        raise KeyError("Missing mandatory arguments, pass vpn remote ip address ")

    ike_sa = get_ike_sa(device_handle, peer_ip=peer_ip, detail=1, ha_link=halink)
    if peer_ip in ike_sa:
        if (ike_sa[peer_ip]['local_port'] == '4500') and (ike_sa[peer_ip]['remote_port'] != '500'):
            device_handle.log(message="local port is 4500 and remote port is not 500, connection is ipsec nat traversal tunnel")
            return True
        else:
            device_handle.log(message="local and remote ports are 500, connetion is not ipsec nat traversal tunnel", level='error')
            return False
    else:
        raise Exception("SA not found for %s" % peer_ip)


# function to verify traffic-selector auto route insertion
#  -----------------------------------------
def verify_ari_route(device_handle, route=None, **kwargs):
    """
    Verify traffic-selector auto route insertion(ari) information

    :param device_handle:
        **REQUIRED** device object
    :param route:
        **REQUIRED** ari route that need to be verified
    :param nexthop:
        *OPTIONAL* nexthop tunnel interface
    :param instance:
        *OPTIONAL* routing-instance if not default
    :param negative:
        *OPTIONAL* 1 if route shouldn't exists
    :return: true if successful or raise Exception for failure

    Example - P: verify_ari_route(r0, route='1.1.1.0/24')
              R: Verify Ari Route  r0  route=1.1.1.0/24
    """

    if route is None:
        raise KeyError("Missing mandatory arguments, route that need to be verified is mandatory ")

    negative = kwargs.get('negative', 0)
    cmd = 'show route ' + route
    if is_ip_ipv4(route):
        table = 'inet.0'
    else:
        table = 'inet6.0'
    if 'instance' in kwargs:
        table = kwargs.get('instance') + '.' + table
    cmd = cmd + ' table ' + table
    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    if resp.find('.//route-table') is not None:
        if negative:
            raise Exception("%s exists in routing table %s" % (route, table))
        else:
            if 'nexthop' in kwargs:
                if resp.findtext('.//via') != kwargs.get('nexthop'):
                    raise Exception("incorrect nexthop found for the route %s" % route)
            if resp.findtext('.//protocol-name') == 'Static':
                device_handle.log(message="%s exists in routing table %s" % (route, table))
                return True
    else:
        if negative:
            device_handle.log(message="%s doesn't exists in routing table %s" % (route, table))
            return True
        else:
            raise Exception("%s doesn't exists in routing table %s" % (route, table))

# Function to get IPSec tunnel distribution information
# -----------------------------------------------------
def get_ipsec_tunnel_distribution(device_handle):
    """
    Get IPsec tunnel distribution information
    :param device_handle:
        **REQUIRED** device object
    :return: A Dictionary of dictionaries will be returned,
    dictionary key is <spu_id value> and nested dictionary{key:value}
    pair is <thread-id> : <No. of tunnels anchored>
    Example : ipsec_td = get_ipsec_tunnel_distribution(device_handle)
    {
        "0": {
            "7": 12,
            "12": 12,
            "17": 12,
            "14": 12,
            "8": 11,
            "1": 11,
            "21": 11,
            "9": 11,
            "15": 12,
            "2": 11,
            "11": 12,
            "23": 11,
            "18": 12,
            "4": 11,
            "16": 12,
            "19": 11,
            "13": 11,
            "6": 11,
            "3": 12,
            "0": 11,
            "20": 12,
            "10": 11,
            "5": 12,
            "22": 11
        }
    }
    To access no. of tunnels anchored at thread 7 in spu 0 use ipsec_td['0']['7']
    """

    ipsec_td = dict()
    cmd = "show security ipsec tunnel-distribution summary"
    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    rpc_resp = device_handle.execute_rpc(command=rpc_eq).response()
    resp = jxmlease.parse_etree(rpc_resp)
    if 'multi-routing-engine-results' in resp.keys():
        device_handle.log(" device is chassis cluster mode")
        resp = resp['multi-routing-engine-results']['multi-routing-engine-item']
    else:
        device_handle.log(" device is not in chassis cluster mode")
    dist_info = resp['ipsec-tunnel-distribution-information']['ipsec-tunnel-distribution-summary-block']
    for msa in dist_info:
        if msa == 'ipsec-thread-number-of-tunnels':
            thread_count = len(dist_info[msa])
        elif msa == 'ipsec-thread-id':
            tunnel_count_entries = len(dist_info[msa])
        else:
            raise KeyError("Unknown key identifier encountered in tunnel distribution output")

    if thread_count == tunnel_count_entries:
        thread_info = dict()
        for thd in range(0, thread_count):
            thread_id = dist_info['ipsec-thread-id'][thd]
            thread_info[thread_id] = int(dist_info['ipsec-thread-number-of-tunnels'][thd])
    else:
        device_handle.log(message="No if entries of thread-ID and tunnel count not matching", level='error')
        return False
    ipsec_td = thread_info
    pprint(ipsec_td)
    return ipsec_td


# verify tunnel event statistics
# ----------------------------------
def verify_ipsec_event_stats(device_handle, event=None, count=None, **kwargs):
    """
    verify given ipsec tunnel event stats
    :param device_handle:
        **REQUIRED** device object
    :param event:
        **REQUIRED** type of ipsec event to verify
    :param count:
        **REQUIRED** expected ipsec event count
    :param kwargs:
        *OPTIONAL* retry is max number of retires to success,
        retry_interval is interval gap between each retry
    :return: true or false based on findings

    Example :
    P: verify_ipsec_event_stats(device_handle, event='DPD detected peer as down', count=1)
    R: verify ipsec event stats  device_handle  event=DPD detected peer as down  count=${1}
    """

    if event is None or count is None:
        raise KeyError("Missing mandatory arguments, need event and event count to verify")

    retry = kwargs.get('retry', 10)
    retry_interval = kwargs.get('retry_interval', 1)
    i = 1
    cmd = "show security ipsec tunnel-events-statistics | match " + '\"' + event + '\"'
    while i <= retry:
        resp = device_handle.cli(command=cmd).response()
        if count == int(re.search(r'\d+', resp).group()):
            device_handle.log("found correct number of %s in event stats" % event)
            break
        else:
            time.sleep(retry_interval)
            device_handle.log("event stats not found, retry")
            i += 1
            if i > retry:
                raise Exception("not found correct number of %s in event stats" % event)
    return True


# function to get dpd infomation and statistics
# ----------------------------------------------
def get_dpd_stats(device_handle, peer_ip=None, **kwargs):
    """Get ike active peer information
    :param device_handle:
        **REQUIRED** device object
    :param peer_ip:
        **REQUIRED** peer ip of the dpd gateway

    :return: A Dictionary will be return having active peer dpd information
    Example P: peer_info = get_dpd_stats(R0, peer_ip='30.1.1.1')
            R: peer_info  Get Dpd Stats  R0    peer_ip=30.1.1.1

            {'mode': 'always-send',
             'interval': '10',
             'threshold': '5',
             'sequence': 362795397,
             'sent': '3',
             'received': '3'}
    """

    cmd = "show security ike active-peer detail "
    ha_link = kwargs.get('ha_link', 0)
    if ha_link:
        cmd = cmd + ' ha-link-encryption '
    if peer_ip is not None:
        cmd = cmd + peer_ip

    text_resp = device_handle.cli(command=cmd).response()
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    dpd_info = dict()
    if resp.find('.//ike-dpd-cfg-mode') is not None:
        mode = resp.findall('.//ike-dpd-cfg-mode')
        interval = resp.findall('.//ike-dpd-cfg-interval')
        threshold = resp.findall('.//ike-dpd-cfg-threshold')
        probe_sent = resp.findall('.//ike-dpd-stats-req')
        probe_received = resp.findall('.//ike-dpd-stats-resp')
        seq_number = re.findall(r'DPD seq-no               :(\d+)', text_resp)
        dpd_info.update(mode=mode[0].text)
        dpd_info.update(interval=interval[0].text)
        dpd_info.update(threshold=threshold[0].text)
        dpd_info.update(sent=probe_sent[0].text)
        dpd_info.update(received=probe_received[0].text)
        dpd_info.update(sequence=int(seq_number[0]))
        pprint(dpd_info)
        return dpd_info
    else:
        device_handle.log(message="not found ike active peer or dpd information")
        return False


# function to get clear ike & ipsec infomation and statistics
# ----------------------------------------------
def clear_sa_all(device_handle, **kwargs):
    """clear ike and ipsec sa and log information
    :param device_handle:
        **REQUIRED** device object lists
    :param ike:
        **OPTIONAL** default clear ike sa
    :param ipsec:
        **OPTIONAL** default clear ipsec sa
    :param data_stats:
        **OPTIONAL** default clear ipsec data stats
    :param event_stats:
        **OPTIONAL** default clear ipsec event stats
    :param logs:
        **OPTIONAL** default clear iked logs
    :param ha_link:
        **OPTIONAL** default clear ha-link tunnel information

    :return: True upon executing all cli commands
    Example P: clear_sa_all(R0)
            R: Clear Sa  All    R0
    """

    ike = kwargs.get('ike', True)
    ipsec = kwargs.get('ipsec', True)
    data_stats = kwargs.get('data_stats', True)
    event_stats = kwargs.get('event_stats', True)
    logs = kwargs.get('logs', True)
    ha_link = kwargs.get('ha_link', 0)
    if ha_link:
        device_handle.log(message="clear multi node ha link encryption tunnel information")
        if ike:
            device_handle.cli(command='clear security ike sa ha-link-encryption')
        if ipsec:
            device_handle.cli(command='clear security ipsec sa ha-link-encryption')
        if data_stats:
            device_handle.cli(command='clear security ipsec statistics ha-link-encryption')
    else:
        device_handle.log(message="clear ike/ipsec sa and information")
        if ike:
            device_handle.cli(command='clear security ike sa')
        if ipsec:
            device_handle.cli(command='clear security ipsec sa')
        if data_stats:
            device_handle.cli(command='clear security ipsec statistics')
        if event_stats:
            device_handle.cli(command='clear security ipsec tunnel-events-statistics')
    if logs:
        device_handle.cli(command='clear log iked')

    return True


# function to get ipsec vpn related logs and information
# ------------------------------------------------------
def capture_ipsec_vpn_debug_logs(device_handle):
    """Get ipsec vpn debug logs
    :param device_handle:
        **REQUIRED** device object lists

    :return: True upon executing all cli commands
    Example P: capture_ipsec_vpn_debug_logs(R0)
            R: Capture Ipsec Vpn Debug Logs    R0
    """
    current_time = str(datetime.datetime.now()).replace(" ", "_")
    device_handle.log(message="collect ipsec vpn debug logs")
    cmd_list = ['show security ike sa detail| no-more',
                'show security ike active-peer',
                'show security ipsec sa detail | no-more',
                'show security ipsec inactive-tunnels',
                'show security ipsec tunnel-events-statistics',
                "show route forwarding-table | no-more",
                'show security ike stats | except ": 0" | no-more',
                'show security ipsec statistics',
                'show security ike statistics all-modules | except \" 0 !\"'
                'show security pki statistics'
                'show configuration | display set | except groups']
    for cmd in cmd_list:
        device_handle.cli(command=cmd)
    logfile = 'kmd' + current_time
    device_handle.log(message="kmd log messages saved with %s name" %logfile)
    device_handle.cli(command="file copy /var/log/kmd /var/tmp/%s" %logfile)
    return True

# function to get flow pmi stats from pfe
# ----------------------------------------
def get_flow_pmi_stats(device_handle, stats_name=None, **kwargs):
    """Get Flow Pmi Stats
    :param device_handle:
        **REQUIRED** device object
    :param stats_name:
        **REQUIRED** name of the pmi stats need to be collected
        user can query for any of the following pmi stats available
        PMI_RX
        PMI_TX
        PMI_RFP
        PMI_DECAP
        PMI_DECAP_BYTES
        PMI_ENCAP
        PMI_ENCAP_BYTES
        PMI_INBOUND_DROP
        PMI_OUTBOUND_DROP
        PMI_CLASSIFY_DROP
        PMI_ENQUEUE_DROP
        PMI_DEQUEUE_DROP
        PMI_ENQUEUE_COP_DROP
        PMI_TX_DROP
    :param pic_tnp_address:
        *OPTIONAL* provide specific tnp address of the pic to collect the stats
    :return: Stats Count will be returned
    Python Examples : stats = get_flow_pmi_stats(srx0, stats_name='PMI_RX')
                      stats = get_flow_pmi_stats(srx0, stats_name='PMI_RX', pic_tnp_address='0x110')

    ROBOT Examples : stats = Get Flow Pmi Stats    srx0  stats_name=PMI_ENCAP
                     stats = Get Flow Pmi Stats    srx0  stats_name=PMI_DECAP  pic_tnp_address=0x110
    """

    device_handle.shell(command="srx-cprod.sh -s spu -c \"show usp flow pmi stats\"")
    if stats_name is None:
        raise KeyError("send the name of the stats you are looking")
    if 'pic_tnp_address' in kwargs:
        cmd = "cprod -A " + kwargs.get('pic_tnp_address') + " -c \"show usp flow pmi stats\"" + " | grep \"" + stats_name + " \" "
    else:
        cmd = "srx-cprod.sh -s spu -c \"show usp flow pmi stats\"" + " | grep \"" + stats_name + " \" "
    output = device_handle.shell(command=cmd).response()
    exp = stats_name + '\\s+(\d+)'
    matches = map(int, re.findall(exp, output))
    stats_cnt = sum(matches)
    print("number of packets for %s stats : %d" % (stats_name, stats_cnt))
    return stats_cnt

# Function to get Pmi Statistics from Dut CLI
# -----------------------------------------------------
def get_pmi_stats_on_re(device_handle, **kwargs):
    """
    :param device_handle:
        **REQUIRED** device object

    :param stat_name:
        **OPTIONAL** specify the stat name (from left column) for which the count has to be returned.
                     Refer to the table below:

        Stat name to be specified             | Stat name on RE
        ------------------------------------------------------------
        PMI_RX                                |  PMI received packets
        PMI_TX                                |  PMI transmitted packets
        PMI_RFP                               |  PMI regular flow path
        PMI_DROP                              |  PMI dropped packets
        PMI_ENCAP_BYTES                       |  PMI encapsulation bytes
        PMI_DECAP_BYTES                       |  PMI decapsulation bytes
        PMI_ENCAP                             |  PMI encapsulation packets
        PMI_DECAP                             |  PMI decapsulation packets

    :param location:
        **OPTIONAL** specify the fpc and pic location for which PMI stats have to be fetched.
                     Example: fpc0.pic0
                     Default is 'summary'

    :param node:
        ***OPTIONAL*** specify the node on which the PMI stats have to be fetched.
                       Node can be given as one of the following:
                       <node_id>: (0..1)
                       local
                       primary

                       Default is local

    :return:
        Stats count value will be returned if stat_name is specified, else dictionary of key-value pair of all stat_name and count will be returned

    Python Examples : pmi_stats = get_pmi_stats_on_re (srx0)
                      pmi_stats = get_pmi_stats_on_re (srx0, stat_name=PMI_DECAP)
                      pmi_stats = get_pmi_stats_on_re (srx0, stat_name=PMI_DECAP, node=local)
                      pmi_stats = get_pmi_stats_on_re (srx0, stat_name=PMI_DECAP, location=fpc0.pic0)

    ROBOT Examples : pmi_stats = Get Pmi Stats On Re    srx0
                     pmi_stats = Get Pmi Stats On Re    srx0   stat_name=PMI_DECAP
                     pmi_stats = Get Pmi Stats On Re    srx0   stat_name=PMI_DECAP  node=local
                     pmi_stats = Get Pmi Stats On Re    srx0   stat_name=PMI_DECAP  location=fpc0.pic0

    """
    resp = device_handle.cli(command='show version | no-more |display xml |match model').response()
    model = re.search(r'>(\w+)<', resp).group(1)

    cmd = "show security flow pmi statistics"

    cluster = _check_chassis_cluster(device_handle)

    if cluster and 'node' in kwargs:
        cmd = cmd + ' node ' + str(kwargs.get('node'))
    elif cluster and 'node' not in kwargs:
        cmd = cmd + ' node local'

    xml_dict = (dev.execute_cli_command_on_device(device=device_handle, command=cmd, format="xml", channel="text", xml_to_dict=True))

    if 'multi-routing-engine-results' in (xml_dict['rpc-reply']).keys():
        if 'list' in str(type(xml_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item'])):
            flow_list = dict(((xml_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item'])[0])['flow-pmi-statistics'])
        else:
            flow_list = (xml_dict['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['flow-pmi-statistics'])
    else:
        flow_list = xml_dict['rpc-reply']['flow-pmi-statistics']

    if re.search(r'^srx5[0-9]00$', model, re.IGNORECASE):
        if 'location' in kwargs and str(kwargs.get('location')) != 'summary':
            pic_location = (str(kwargs.get('location')).split(".")[0]).upper() + " " + (str(kwargs.get('location')).split(".")[1]).upper()
        else:
            pic_location = str('summary')

        match = int([index for (index, item) in enumerate(flow_list) if pic_location in str(item['pmi-spu-id'])][0])
        stat_dict = dict(flow_list[match])
    else:
        stat_dict = dict(flow_list)

    pmi_stat_dict = dict(PMI_RX=int(stat_dict['pmi-rx']), PMI_TX=int(stat_dict['pmi-tx']), PMI_ENCAP=int(stat_dict['pmi-encap-pkts']), PMI_DECAP=int(stat_dict['pmi-decap-pkts']), PMI_ENCAP_BYTES=int(stat_dict['pmi-encap-bytes']), PMI_DECAP_BYTES=int(stat_dict['pmi-decap-bytes']), PMI_RFP=int(stat_dict['pmi-rfp']), PMI_DROP=int(stat_dict['pmi-drop']))
    return pmi_stat_dict[kwargs.get('stat_name')] if 'stat_name' in kwargs else pmi_stat_dict

# Function to Verify Pmi Statistics On RE
# -----------------------------------------------------
def verify_pmi_stats_on_re(device_handle, stat_dict, relation, **kwargs):
    """
    :param device_handle:
        **REQUIRED** device object

    :param stat_dict:
        **REQUIRED** dictionary with stat_name as the key and the expected count as the value
                     Example: {PMI_ENCAP=20, PMI_DECAP=25, PMI_DROP=0}

    :param relation:
       ***OPTIONAL*** comparison operator: used to compare the relation of actual_count to expected count.
       Default is equal. Values can be:
                      greater
                      lesser
                      equal

                      Example: # Checking if PMI_ENCAP, PMI_DECAP AND PMI_DROP are equal to the value provided i.e. 20,25 and 0 respectively
                               stat_dict={PMI_ENCAP:20, PMI_DECAP:25, PMI_DROP:0}     relation=equal

                               # Checking whether  PMI_ENCAP and PMI_DECAP are greater than zero
                               stat_dict={PMI_ENCAP:0, PMI_DECAP:0}      relation=greater

    :param location:
        **OPTIONAL** specify the fpc and pic location for which PMI stats have to be fetched. Default is summary. Example: fpc0.pic0

    :param node:
        ***OPTIONAL*** specify the node on which the PMI stats have to be fetched.
        Node can be given as one of the following. Default is local if device is HA:
                       <node_id>: (0..1)
                       local
                       primary

    :return:
        True if the count value matches


    Python Examples : pmi_stats = verify_pmi_stats_on_re (srx0,
                                  stat_dict={PMI_ENCAP:20, PMI_DECAP:25, PMI_DROP:0}     relation=equal)
                      pmi_stats = verify_pmi_stats_on_re (srx0,
                      stat_dict={PMI_ENCAP:0, PMI_DECAP:0}      relation=greater)


    ROBOT Examples : &{pmi_dict} =  Create Dictionary     PMI_ENCAP=${0}    PMI_DECAP=${0}
                     pmi_stats = Verify Pmi Stats on Re    srx0   stat_dict = &{pmi_dict}    relation=greater

    """

    resp = device_handle.cli(command='show version | no-more |display xml |match model').response()
    model = re.search(r'>(\w+)<', resp).group(1)
    cluster = _check_chassis_cluster(device_handle)
    actual_count_list = []
    expected_count_list = []

    for stat_name in stat_dict:
        expected_count_list.append(stat_dict[stat_name])
        if cluster and re.search(r'^srx5[0-9]00$', model, re.IGNORECASE):        ## device is 5k HA
            actual_count_list.append(get_pmi_stats_on_re(device_handle, location=kwargs.get('location', 'summary'),
                                                         node=kwargs.get('node', 'local'), stat_name=stat_name))
        elif cluster:                                                            ## device is vSRX HA
            actual_count_list.append(get_pmi_stats_on_re(device_handle, node=kwargs.get('node', 'local'),
                                                         stat_name=stat_name))
        elif not cluster and re.search(r'^srx5[0-9]00$', model, re.IGNORECASE):   ## device is 5k SA
            actual_count_list.append(get_pmi_stats_on_re(device_handle, location=kwargs.get('location', 'summary'),
                                                         stat_name=stat_name))
        else:                                                                ## device is vSRX SA
            actual_count_list.append(get_pmi_stats_on_re(device_handle, stat_name=stat_name))

    for i in range(len(actual_count_list)):
        if relation.lower() == 'greater':
            result = True if actual_count_list[i] > expected_count_list[i] else False
        elif relation.lower() == 'lesser':
            result = True if actual_count_list[i] < expected_count_list[i] else False
        elif relation.lower() == 'equal':
            result = True if actual_count_list[i] == expected_count_list[i] else False

    return result


# Function to get IPSec tunnel pfe anchorship
# -----------------------------------------------------
def get_ipsec_sa_pic(device_handle, ipsec_index=None):
    """
    Get IPsec tunnel pic anchorship information
    :param device_handle:
        **REQUIRED** device object
	: param ipsec_index:
	    **OPTIONAL**
    :return: pic information of ipsec sa where anchored,
	         for srx5k platforms function returns spu pic info
			 rest of the srx platfroms pfe pic information
    Example : ipsec_pic = get_ipsec_sa_pic(device_handle)
	          ipsec_pic = get_ipsec_sa_pic(device_handle, ipsec_index=500001)

    """

    resp = device_handle.cli(command='show version | no-more |display xml |match model').response()
    model = re.search(r'>(\w+)<', resp).group(1)
    device_handle.log(message="device model is %s" %model)
    if re.search(r'^srx5[0-9]00$', model, re.IGNORECASE):
        if ipsec_index is None:
            raise KeyError("ipsec index is mandatory for all srx5k series platforms")
        else:
            cmd = "show security ipsec sa index " + str(ipsec_index)
            device_handle.cli(command=cmd)
            rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
            resp = device_handle.execute_rpc(command=rpc_eq).response()
            fpc = resp.findall('.//sa-fpc')
            pic = resp.findall('.//sa-pic')
            ipsec_pic = 'fpc' + fpc[0].text + '.pic' + pic[0].text
    elif re.search(r'^srx[0-9]00$', model, re.IGNORECASE) or re.search(r'^vSRX$', model):
        ipsec_pic = 'fwdd'
    elif re.search(r'^srx[0-4][0-9][0-9]0$', model, re.IGNORECASE) or re.search(r'^vsrx$', model):
        ipsec_pic = 'fpc0'
    else:
        raise Exception("unsupported platform")
    device_handle.log("installed pic is %s" %ipsec_pic)
    return ipsec_pic


# Function to verify PMI fat core functionality
# ---------------------------------------------
def verify_pmi_fatcore_stats(device_handle, ipsec_index=None, **kwargs):
    """
    Get IPsec tunnel pic anchorship information
    :param device_handle:
        **REQUIRED** device object
    : param ipsec_index:
        **OPTIONAL** ipsec tunnel index to find the anchorship information on srx5k platforms
    : params node:
        **OPTIONAL** incase of HA, which node need dataplane is active to be passed,
                     default verification is on node0
    : param anchor_thread_check:
       **OPTIONAL** option to skip tunnel anchor thread pmi fat core processing check,
                    user need to pass boolean False to skip this check
                    if same thread involved on hosting tunnel
                    and helping other tunnels in the fat core group
    :return: True if packets procssed in pmi fat core mode,
             False if packets processed in non-pmi mode
    Example : result = verify_pmi_fatcore_stats(srx0)
              result = verify_pmi_fatcore_stats(srx0,
              ipsec_index=500001, node=1, anchor_thread_check)

              result =  Verify Pmi Fatcore Stats    ${srx0}  ipsec_index=500001  node=0
    """

    anchor_thread_check = kwargs.get('anchor_thread_check', 1)
    node = kwargs.get('node', '0')
    model = device_handle.shell(command='jwhoami -p').response()
    device_handle.log(message='device model is %s' % model)
    if re.search(r'^srx5[0-9]00$', model, re.IGNORECASE):
        if ipsec_index is None:
            raise KeyError(
                'ipsec index is mandatory for all srx5k series platforms')
        else:
            cmd = 'show security ipsec sa index ' + str(ipsec_index)
            device_handle.cli(command=cmd)
            rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
            resp = device_handle.execute_rpc(command=rpc_eq).response()
            fpc = resp.findall('.//sa-fpc')[0].text
            pic = resp.findall('.//sa-pic')[0].text
            thread = int(resp.findall('.//sa-anchor-thread')[0].text)
            anchorship = 'fpc' + fpc + '.pic' + pic
            # define fat core group size
            device_handle.log('define fat core group size and thread list')
            if thread < 14:
                fcg = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                       12, 13]
            else:
                fcg = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    elif re.search(r'^srx[0-9]00$', model, re.IGNORECASE) or re.search(r'^vSRX$', model):
        anchorship = 'fwdd'
    elif re.search(r'^srx[0-4][0-9][0-9]0$', model, re.IGNORECASE) or re.search(r'^vsrx$', model):
        anchorship = 'fpc0'
        fcg = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    else:
        raise Exception('unsupported platform')

    resp = device_handle.shell(command='jwhoami -c').response()
    if resp != 'mcluster not enabled':
        anchorship = 'node' + str(node) + '.' + anchorship
    fcg.remove(thread)
    ### verify tunnel anchor/host thread pmi stats
    if anchor_thread_check:
        cmd = 'cprod -A ' + anchorship + \
            ' -c show usp flow pmi stats ' + str(thread)
        resp = device_handle.shell(command=cmd).response()
        if int(re.findall(r'Encap success rcvd from PMI path packet\s+(\d+)',
                          resp)[0]) != 0 or int(re.findall(r'Decap success packet\s+(\d+)', resp)[0]) != 0:
            device_handle.log(
                'anchor host thread in fat group participated in crypto operation')
            return False
    ### verify fat core group help threads pmi stats
    for i in fcg:
        cmd = 'cprod -A ' + anchorship + \
            ' -c show usp flow pmi stats ' + str(i)
        resp = device_handle.shell(command=cmd).response()
        if int(re.findall(r'Encap success rcvd from PMI path packet\s+(\d+)',
                          resp)[0]) == 0 or int(re.findall(r'Decap success packet\s+(\d+)', resp)[0]) == 0:
            device_handle.log(
                'helping threads in fat core group not participated in crypto operation')
            return False
    device_handle.log('packets processed in pmi fat core mode')
    return True


# function to get multi node ha peer information
# ----------------------------------------------
def get_l3ha_peer_info(device_handle):
    """Get multinode HA peer information
    :param device_handle:
        **REQUIRED** device object

    :return: A Dictionary will be return having HA peer information
    Example P: peer_info = get_l3ha_peer_info(R0)
            R: peer_info =  Get L3ha Peer Info  R0

           {'bfd_status': 'UP',
            'cold_sync_status': 'Completed',
            'ifl': 'xe-4/0/9.0',
            'ifl_vr': 'default',
            'link_encr_status': 'YES',
            'pid': '1',
            'pip': '2.2.2.1'}
    """

    cmd = "show chassis high-availability peer-info"
    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    ha_info = dict()
    if resp.find('.//high-availability-peer-id') is not None:
        pid = resp.findall('.//high-availability-peer-id')
        pip = resp.findall('.//high-availability-peer-ip-address')
        ifl_vr = resp.findall('.//high-availability-peer-rt-instance')
        ifl = resp.findall('.//high-availability-local-interface')
        bfd_status = resp.findall('.//high-availability-peer-bfd-status')
        link_encr_status = resp.findall('.//high-availability-peer-encryption-status')
        cold_sync_status = resp.findall('.//cold-sync-status')
        ha_info.update(pid=pid[0].text)
        ha_info.update(pip=pip[0].text)
        ha_info.update(ifl=ifl[0].text)
        ha_info.update(ifl_vr=ifl_vr[0].text)
        ha_info.update(bfd_status=bfd_status[0].text)
        ha_info.update(link_encr_status=link_encr_status[0].text)
        ha_info.update(cold_sync_status=cold_sync_status[0].text)
        pprint(ha_info)
        return ha_info
    else:
        device_handle.log(message="not found ha peer information")
        return False


# function to get multi node ha srg information
# ----------------------------------------------
def get_l3ha_srg_info(device_handle, srg=1):
    """Get multinode HA srg information
    :param device_handle:
        **REQUIRED** device object
    :param srg:
        **REQUIRED** service redundancy group id, default is 1
    :return: A Dictionary will be return having HA srg information
    Example P: srg_info = get_l3ha_srg_info(R0)
            R: srg_info =  Get L3ha Srg Info    R0    srg=1

            {'control_plane': 'READY',
             'failover_ready': 'Unknown',
             'failure_events': 'None',
             'ha_pid': '2',
             'health_status': 'Healthy',
             'node_role': 'ACTIVE'}
    """

    cmd = "show chassis high-availability information"
    device_handle.cli(command=cmd)
    rpc_eq = device_handle.get_rpc_equivalent(command=cmd)
    resp = device_handle.execute_rpc(command=rpc_eq).response()
    srg_info = dict()
    if resp.find('.//chassis-high-availability-srg-info/srg-id') is not None:
        srg_list = resp.findall('.//srg-id')
        node_role = resp.findall('.//node-role')
        control_plane = resp.findall('.//control-plane')
        failure_events = resp.findall('.//failure-events')
        ha_pid = resp.findall('.//peer-id')
        health_status = resp.findall('.//health-status')
        failover_ready = resp.findall('.//failover-readiness')
        i = 0
        while i < len(srg_list):
            if int(srg_list[i].text) == srg:
                device_handle.log("found the srg info")
                srg_info.update(node_role=node_role[i].text)
                srg_info.update(control_plane=control_plane[i].text)
                srg_info.update(failure_events=failure_events[i].text)
                srg_info.update(ha_pid=ha_pid[i].text)
                srg_info.update(health_status=health_status[i].text)
                srg_info.update(failover_ready=failover_ready[i].text)
                pprint(srg_info)
                return srg_info
            else:
                i += 1
                if i == len(srg_list):
                    raise Exception("not found the requested srg info")
    else:
        raise Exception("could not find any information related to srg")


# Private Method to check if chassis cluster is enabled on device
# ---------------------------------------------------------------
def _check_chassis_cluster(handle):
    """
        This is a private method used by the library to check if the device is in HA/non-HA mode
        It returns 1 if the device is in HA and 0 if the device is in non-HA
    """
    out = handle.cli(command="show chassis cluster status").response()

    handle.cli(command="show version |grep model").response()
    if re.search("Chassis cluster is not enabled", str(out)):
        check_chassis = False
    else:
        check_chassis = True

    return check_chassis
