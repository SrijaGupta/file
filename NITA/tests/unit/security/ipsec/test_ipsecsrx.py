import sys
import unittest
from unittest.mock import MagicMock, patch
from jnpr.toby.hldcl.device import Device
from jnpr.toby.security.ipsec.ipsecsrx import *
from lxml import etree
import os
import jxmlease
from jnpr.toby.utils.iputils import *

def get_file_path(file_name):
    path = os.path.dirname(__file__)
    file = os.path.join(path, file_name)
    return file


class TestIPsecSRX(unittest.TestCase):

    def test_get_ipsec_pkt_stats(self):
        tree = etree.parse(get_file_path('srx_ipsec_stats.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ipsec-statistics-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        exp_dic = {'AH_AUTH_FAIL': 0, 'BAD_HEAD': 0, 'BAD_TRAIL': 0, 'DBYTES': 0, 'DPKTS': 0, 'EBYTES': 0, 'EPKTS': 0, 'ESP_AUTH_FAIL': 0, 'ESP_DECR_FAIL': 0, 'IBYTES': 0, 'IPKTS': 0, 'OBYTES': 0, 'OPKTS': 0, 'REPLAY_ERRORS': 0}
        self.assertEqual(get_ipsec_pkt_stats(device_obj), exp_dic)
        self.assertEqual(get_ipsec_pkt_stats(device_obj, index=67108881), exp_dic)
        self.assertEqual(get_ipsec_pkt_stats(device_obj, node='local'), exp_dic)

    def test_verify_ipsec_pkt_stats(self):
        tree = etree.parse(get_file_path('srx_ipsec_stats.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ipsec-statistics-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        self.assertTrue(verify_ipsec_pkt_stats(device_obj,expected_stats={ 'BAD_HEAD': 0, 'BAD_TRAIL': 0, 'DBYTES': 0, 'DPKTS': 0, 'EBYTES': 0, 'EPKTS': 0, 'ESP_AUTH_FAIL': 0, 'ESP_DECR_FAIL': 0, 'IBYTES': 0, 'IPKTS': 0, 'OBYTES': 0, 'OPKTS': 0, 'REPLAY_ERRORS': 0}))
        self.assertTrue(verify_ipsec_pkt_stats(device_obj, index=67108881, node='local',
                                               expected_stats={'BAD_HEAD': 0, 'BAD_TRAIL': 0, 'DBYTES': 0, 'DPKTS': 0,
                                                               'EBYTES': 0, 'EPKTS': 0, 'ESP_AUTH_FAIL': 0,
                                                               'ESP_DECR_FAIL': 0, 'IBYTES': 0, 'IPKTS': 0, 'OBYTES': 0,
                                                               'OPKTS': 0, 'REPLAY_ERRORS': 0}))
        self.assertTrue(verify_ipsec_pkt_stats(device_obj, index=67108881,
                                               expected_stats={'BAD_HEAD': 0, 'BAD_TRAIL': 0, 'DBYTES': 0, 'DPKTS': 0,
                                                               'EBYTES': 0, 'EPKTS': 0, 'ESP_AUTH_FAIL': 0,
                                                               'ESP_DECR_FAIL': 0, 'IBYTES': 0, 'IPKTS': 0, 'OBYTES': 0,
                                                               'OPKTS': 0, 'REPLAY_ERRORS': 0}))
        self.assertTrue(verify_ipsec_pkt_stats(device_obj, node='local',
                                               expected_stats={'BAD_HEAD': 0, 'BAD_TRAIL': 0, 'DBYTES': 0, 'DPKTS': 0,
                                                               'EBYTES': 0, 'EPKTS': 0, 'ESP_AUTH_FAIL': 0,
                                                               'ESP_DECR_FAIL': 0, 'IBYTES': 0, 'IPKTS': 0, 'OBYTES': 0,
                                                               'OPKTS': 0, 'REPLAY_ERRORS': 0}))
        self.assertFalse(verify_ipsec_pkt_stats(device_obj,expected_stats={ 'BAD_HEAD': 0, 'BAD_TRAIL': 0, 'DBYTES': 20, 'DPKTS': 20, 'EBYTES': 20, 'EPKTS': 20, 'ESP_AUTH_FAIL': 0, 'ESP_DECR_FAIL': 20, 'IBYTES': 0, 'IPKTS': 20, 'OBYTES': 20, 'OPKTS': 20, 'REPLAY_ERRORS': 0}))

    def test_get_ike_sa(self):
        tree = etree.parse(get_file_path('srx_ike_sa.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ike-security-associations-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        exp_dic = {'3.3.3.2': {'index': 3922268,
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
        self.assertDictEqual(get_ike_sa(device_obj), exp_dic)
        exp_dic = {3922268: {'index': 3922268,
                               'init_cookie': '1e29005494f73fb3',
                               'mode': 'IKEv2',
                               'remote_ip': '3.3.3.2',
                               'resp_cookie': '835a88571b16a29f',
                               'state': 'UP'},
                   3922267: {'index': 3922267,
                               'init_cookie': '95ccf59c2783de54',
                               'mode': 'IKEv2',
                               'remote_ip': '5.5.5.2',
                               'resp_cookie': 'fec2c4b00faf0495',
                               'state': 'UP'},
                   'total': 2}
        self.assertDictEqual(get_ike_sa(device_obj,dic_key='id'), exp_dic)

    def test_get_ike_sa_detail(self):
        tree = etree.parse(get_file_path('srx_ike_sa_detail.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ike-security-associations-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        exp_dic = {'3.3.3.2': {'auth_algo': 'hmac-sha1-96',
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
                               'reauth': 'Disabled',
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
        self.assertDictEqual(get_ike_sa(device_obj, detail=1), exp_dic)

    def test_verify_ike_sa_status(self):
        tree = etree.parse(get_file_path('srx_single_ike_sa.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ike-security-associations-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        self.assertTrue(verify_ike_sa_status(device_obj, peer_ip=['3.3.3.2']))
        self.assertTrue(verify_ike_sa_status(device_obj, peer_ip=['3.3.3.1'], negative=1))

    def test_verify_ike_sa_count(self):
        tree = etree.parse(get_file_path('srx_ike_sa.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ike-security-associations-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        self.assertTrue(verify_ike_sa_count(device_obj, count=2))

    @patch('jnpr.toby.security.ipsec.ipsecsrx.get_ipsec_sa')
    def test_verify_ipsec_sa_status(self,get_ipsec):
        get_ipsec.return_value = {'3.3.3.2': {'auth_algo': 'sha256',
             'encr_algo': 'aes-cbc-192',
             'in_spi': 'd617f066',
             'index': 67108868,
             'lifesize': '149997',
             'lifetime': 1128,
             'local_port': 500,
             'monitor': '-',
             'out_spi': '8e8cfe61',
             'protocol': 'ESP',
             'remote_ip': '3.3.3.2',
             'remote_port': 500,
             'state': 'up'}, 'total': 1}
        device_obj = MagicMock()
        self.assertTrue(verify_ipsec_sa_status(device_obj, peer_ip=['3.3.3.2']))
        self.assertTrue(verify_ipsec_sa_status(device_obj, peer_ip=['3.3.3.1'], negative=1))

    @patch('jnpr.toby.security.ipsec.ipsecsrx.get_ipsec_sa')
    def test_verify_ipsec_sa_count(self,get_ipsec):
        get_ipsec.return_value = {67108866: {'auth_algo': 'sha256',
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
        device_obj = MagicMock()
        self.assertTrue(verify_ipsec_sa_count(device_obj, count=2))

    def test_verify_ike_rekey(self):
        self.assertTrue(verify_ike_rekey(ike_cookie_old=[10,11], ike_cookie_new=[10,11], rekey=0))
        self.assertTrue(verify_ike_rekey(ike_cookie_old=[10, 11], ike_cookie_new=[10, 12], rekey=1))

    def test_verify_ipsec_rekey(self):
        self.assertTrue(verify_ipsec_rekey(ipsec_spi_old=[10,11], ipsec_spi_new=[10,11], rekey=0))
        self.assertTrue(verify_ipsec_rekey(ipsec_spi_old=[10, 11], ipsec_spi_new=[10, 12], rekey=1))

    @patch('time.sleep')
    def test_verify_ifl_status(self,ts):
        ts.return_value = True
        tree = etree.parse(get_file_path('srx_ifl_up.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-interface-information><terse/><interface-name>st0.1</interface-name></get-interface-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        xml_obj = MagicMock(spec=jxmlease)
        xml_obj.parse_etree = MagicMock(return_value="""{'interface-information': {'logical-interface': {'address-family': {'address-family-name': XMLCDATANode(xml_attrs=OrderedDict(), value='inet'), 'interface-address': {'ifa-local': XMLCDATANode(xml_attrs=OrderedDict([('emit', 'emit')]), value='202.2.1.100/24')}},
                                                 'admin-status': XMLCDATANode(xml_attrs=OrderedDict(), value='up'), 'filter-information': XMLCDATANode(xml_attrs=OrderedDict(), value=''), 'name': XMLCDATANode(xml_attrs=OrderedDict(), value='st0.1'), 'oper-status': XMLCDATANode(xml_attrs=OrderedDict(), value='up')}}}""")
        self.assertTrue(verify_ifl_status(device_obj, ifl=['st0.1']))
        tree = etree.parse(get_file_path('srx_ifl_down.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-interface-information><terse/><interface-name>st0.1</interface-name></get-interface-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)
        xml_obj = MagicMock(spec=jxmlease)
        xml_obj.parse_etree = MagicMock(return_value="""{'interface-information': {'logical-interface': {'address-family': {'address-family-name': XMLCDATANode(xml_attrs=OrderedDict(), value='inet'), 'interface-address': {'ifa-local': XMLCDATANode(xml_attrs=OrderedDict([('emit', 'emit')]), value='202.2.1.100/24')}},
                                                         'admin-status': XMLCDATANode(xml_attrs=OrderedDict(), value='up'), 'filter-information': XMLCDATANode(xml_attrs=OrderedDict(), value=''), 'name': XMLCDATANode(xml_attrs=OrderedDict(), value='st0.1'), 'oper-status': XMLCDATANode(xml_attrs=OrderedDict(), value='down')}}}""")
        self.assertTrue(verify_ifl_status(device_obj, ifl=['st0.1'], status='down'))

    def test_verify_pattern(self):
        device_obj = MagicMock()
        string = """Hostname: vsrxvpn86
                    Model: vsrx
                    Junos: 15.1-2017-03-26.0_JUNOS_151_X49_D90
                    JUNOS Software Release [15.1-2017-03-26.0_JUNOS_151_X49_D90]"""
        device_obj.cli().response = MagicMock(return_value=string)
        self.assertTrue(verify_pattern(device_obj,cmd='show version', pattern=['Model: vsrx', 'Hostname: vsrxvpn86']))
        self.assertFalse(verify_pattern(device_obj, cmd='show version', pattern=['Model: vsrx', 'Hostname: noname'], retry=1))

    @patch('jnpr.toby.security.ipsec.ipsecsrx.get_ike_sa')
    def test_verify_nat_traversal(self,get_ike):
        get_ike.return_value = {'9.168.0.1': {'auth_algo': 'hmac-sha256-128',
               'auth_method': 'Pre-shared-keys',
               'dh_group': 'DH-group-14',
               'encr_algo': 'aes256-cbc',
               'index': 4967388,
               'init_cookie': 'c95dc1679b63f189',
               'lifetime': 28731,
               'local__id': '9.168.0.2',
               'local_ip': '9.168.0.2',
               'local_port': '4500',
               'mode': 'main',
               'name': 'R0R3_GW1',
               'prf_algo': 'hmac-sha256',
               'remote_id': '9.168.0.1',
               'remote_ip': '9.168.0.1',
               'remote_port': '12400',
               'resp_cookie': '6e1abe19783ff083',
               'role': 'responder',
               'state': 'UP',
               'status': 'IKE SA is created',
               'xauth_ip': '0.0.0.0',
               'xauth_user': None},
 'total': 1}
        device_obj = MagicMock()
        self.assertTrue(verify_nat_traversal(device_obj, peer_ip='9.168.0.1'))
        get_ike.return_value = {'9.168.0.1': {'auth_algo': 'hmac-sha256-128',
               'auth_method': 'Pre-shared-keys',
               'dh_group': 'DH-group-14',
               'encr_algo': 'aes256-cbc',
               'index': 4967388,
               'init_cookie': 'c95dc1679b63f189',
               'lifetime': 28731,
               'local__id': '9.168.0.2',
               'local_ip': '9.168.0.2',
               'local_port': '500',
               'mode': 'main',
               'name': 'R0R3_GW1',
               'prf_algo': 'hmac-sha256',
               'remote_id': '9.168.0.1',
               'remote_ip': '9.168.0.1',
               'remote_port': '500',
               'resp_cookie': '6e1abe19783ff083',
               'role': 'responder',
               'state': 'UP',
               'status': 'IKE SA is created',
               'xauth_ip': '0.0.0.0',
               'xauth_user': None},
 'total': 1}
        self.assertFalse(verify_nat_traversal(device_obj, peer_ip='9.168.0.1'))
    
    def test_verify_ipsec_ts(self): 
        op_str = "<ipsec-traffic-selector-information><ipsec-traffic-selector-block><sa-tunnel-index>67108866</sa-tunnel-index><sa-bind-interface>st0.1</sa-bind-interface><ike-ike-id>9.168.0.1</ike-ike-id><traffic-selector-source-address>ipv4(41.0.2.10)</traffic-selector-source-address><traffic-selector-destination-address>ipv4(61.0.2.10)</traffic-selector-destination-address></ipsec-traffic-selector-block></ipsec-traffic-selector-information>"
        tree = etree.fromstring(op_str)
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ipsec-traffic-selector-information>')
        device_obj.execute_rpc().response = MagicMock(return_value=tree)
        self.assertTrue(verify_ipsec_ts(device_obj,st_ifl='st0.1', src_ip='41.0.2.10/32', dst_ip='61.0.2.10/32'))
        self.assertTrue(verify_ipsec_ts(device_obj,st_ifl='st0.1', src_ip='41.0.2.10/32'))
        self.assertTrue(verify_ipsec_ts(device_obj,st_ifl='st0.1', dst_ip='61.0.2.10/32'))
        self.assertTrue(verify_ipsec_ts(device_obj,st_ifl='st0.1'))
        op_str = "<ipsec-traffic-selector-information></ipsec-traffic-selector-information>"
        tree = etree.fromstring(op_str)
        device_obj.execute_rpc().response = MagicMock(return_value=tree)
        self.assertFalse(verify_ipsec_ts(device_obj,st_ifl='st0.2'))

    @patch('jnpr.toby.utils.iputils.is_ip_ipv4')
    def test_verify_ari_route(self,ip_version):
        ip_version.return_value = True
        device_obj = MagicMock()
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-route-information>')
        op_str = '<route-information><route-table><table-name>inet.0</table-name><destination-count>2</destination-count><total-route-count>2</total-route-count><active-route-count>2</active-route-count><holddown-route-count>0</holddown-route-count><hidden-route-count>0</hidden-route-count><rt style="brief"><rt-destination>61.0.1.10/32</rt-destination><rt-entry><active-tag>*</active-tag><current-active/><last-active/><protocol-name>Static</protocol-name><preference>5</preference><age seconds="19239">05:20:39</age><nh><selected-next-hop/><via>st0.1</via></nh></rt-entry></rt></route-table></route-information>'
        tree = etree.fromstring(op_str)
        device_obj.execute_rpc().response = MagicMock(return_value=tree)
        self.assertTrue(verify_ari_route(device_obj,route='61.0.1.10/32', nexthop='st0.1'))
        try:
            verify_ari_route(device_obj,route='61.0.1.10/32', nexthop='st0.1', negative=1)
        except Exception as error:
            self.assertEqual(error.args[0],'61.0.1.10/32 exists in routing table inet.0')
        op_str = '<route-information></route-information>'
        tree = etree.fromstring(op_str)
        device_obj.execute_rpc().response = MagicMock(return_value=tree)
        self.assertTrue(verify_ari_route(device_obj,route='41.0.1.10/32', negative=1))
        try:
            verify_ari_route(device_obj,route='41.0.1.10/32')
        except Exception as error:
            self.assertEqual(error.args[0],'41.0.1.10/32 doesn\'t exists in routing table inet.0')


    @patch('jnpr.toby.security.ipsec.ipsecsrx.jxmlease.parse_etree')
    def test_get_ipsec_tunnel_distribution(self, mock_jxmlease):
        device_obj = MagicMock()
        exp_dict = dict()
        exp_dict = {
            "7": 80,
            "8": 90,
            "1": 20,
            "9": 100,
            "2": 30,
            "4": 50,
            "6": 70,
            "3": 40,
            "0": 10,
            "10": 110,
            "5": 60
        }
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-ipsec-tunnel-distribution>')
        op_str = '<ipsec-tunnel-distribution-information><ipsec-tunnel-distribution-summary-block><ipsec-thread-id>0</ipsec-thread-id><ipsec-thread-number-of-tunnels>10</ipsec-thread-number-of-tunnels><ipsec-thread-id>1</ipsec-thread-id><ipsec-thread-number-of-tunnels>20</ipsec-thread-number-of-tunnels><ipsec-thread-id>2</ipsec-thread-id><ipsec-thread-number-of-tunnels>30</ipsec-thread-number-of-tunnels><ipsec-thread-id>3</ipsec-thread-id><ipsec-thread-number-of-tunnels>40</ipsec-thread-number-of-tunnels><ipsec-thread-id>4</ipsec-thread-id><ipsec-thread-number-of-tunnels>50</ipsec-thread-number-of-tunnels><ipsec-thread-id>5</ipsec-thread-id><ipsec-thread-number-of-tunnels>60</ipsec-thread-number-of-tunnels><ipsec-thread-id>6</ipsec-thread-id><ipsec-thread-number-of-tunnels>70</ipsec-thread-number-of-tunnels><ipsec-thread-id>7</ipsec-thread-id><ipsec-thread-number-of-tunnels>80</ipsec-thread-number-of-tunnels><ipsec-thread-id>8</ipsec-thread-id><ipsec-thread-number-of-tunnels>90</ipsec-thread-number-of-tunnels><ipsec-thread-id>9</ipsec-thread-id><ipsec-thread-number-of-tunnels>100</ipsec-thread-number-of-tunnels><ipsec-thread-id>10</ipsec-thread-id><ipsec-thread-number-of-tunnels>110</ipsec-thread-number-of-tunnels></ipsec-tunnel-distribution-summary-block></ipsec-tunnel-distribution-information>'
        tree = etree.fromstring(op_str)
        device_obj.execute_rpc().response = MagicMock(return_value=tree)
        mock_jxmlease.return_value = {'ipsec-tunnel-distribution-information': {'ipsec-tunnel-distribution-summary-block': {
                                           'ipsec-thread-id': ['0',
                                                               '1',
                                                               '2',
                                                               '3',
                                                               '4',
                                                               '5',
                                                               '6',
                                                               '7',
                                                               '8',
                                                               '9',
                                                               '10'],
                                           'ipsec-thread-number-of-tunnels': ['10',
                                                                              '20',
                                                                              '30',
                                                                              '40',
                                                                              '50',
                                                                              '60',
                                                                              '70',
                                                                              '80',
                                                                              '90',
                                                                              '100',
                                                                              '110']}}}
        #self.assertEqual(get_ipsec_tunnel_distribution(device_obj) , exp_dict)


    def test_verify_ipsec_event_stats(self):
        device_obj = MagicMock()
        string = "DPD detected peer as down. Existing IKE/IPSec SAs cleared                                       : 4 "
        device_obj.cli().response = MagicMock(return_value=string)
        self.assertTrue(verify_ipsec_event_stats(device_obj,event='DPD detected peer as down', count=4))
        try:
            verify_ipsec_event_stats(device_obj, event='DPD detected peer as down', count=1, retry=1)
        except Exception as error:
            self.assertEqual(error.args[0], 'not found correct number of DPD detected peer as down in event stats')


    def test_clear_sa_all(self):
        device_obj = MagicMock()
        device_obj.cli = MagicMock(return_value=True)
        self.assertTrue(clear_sa_all(device_obj))


    def test_get_flow_pmi_stats(self):
        device_obj = MagicMock()
        string = """ PMI_ENCAP                                  118
                   PMI_ENCAP                                    2"""
        device_obj.shell().response = MagicMock(return_value=string)
        try:
            get_flow_pmi_stats(device_obj)
        except Exception as error:
            self.assertEqual(error.args[0],'send the name of the stats you are looking')
        self.assertEqual(get_flow_pmi_stats(device_obj,stats_name='PMI_ENCAP'),120)
        self.assertEqual(get_flow_pmi_stats(device_obj,stats_name='PMI_ENCAP', pic_tnp_address='0x110'),120)

    @patch('jnpr.toby.hldcl.device.execute_cli_command_on_device')
    def test_get_pmi_stats_on_re(self, exec):
        tree = etree.parse(get_file_path('srx_pmi_stats.xml'))
        root_elem = tree.getroot()
        device_obj = MagicMock()
        string = "        <product-model>vSRX</product-model>"
        device_obj.cli().response = MagicMock(return_value=string)
        device_obj.get_rpc_equivalent = MagicMock(return_value='<get-pmi-statistics-all>')
        device_obj.execute_rpc().response = MagicMock(return_value=root_elem)

        exp_dict = dict()
        exp_dic = {'PMI_TX': 0, 'PMI_RFP': 0, 'PMI_DROP': 0, 'PMI_ENCAP_BYTES': 1400, 'PMI_DECAP': 20, 'PMI_DECAP_BYTES': 1400, 'PMI_ENCAP': 20, 'PMI_RX': 0}

        exec.return_value =  {'rpc-reply': {'cli': {'banner': ''},
               'flow-pmi-statistics': {'pmi-decap-bytes': '1400',
                                       'pmi-decap-pkts': '20',
                                       'pmi-drop': '0',
                                       'pmi-encap-bytes': '1400',
                                       'pmi-encap-pkts': '20',
                                       'pmi-rfp': '0',
                                       'pmi-rx': '0',
                                       'pmi-tx': '0'}}}

        self.assertEqual(get_pmi_stats_on_re(device_obj, node='local'), exp_dic)
        self.assertEqual(get_pmi_stats_on_re(device_obj, node='local', location='fpc0.pic0'), exp_dic)
        self.assertEqual(get_pmi_stats_on_re(device_obj, stat_name='PMI_ENCAP'), 20)
        self.assertEqual(get_pmi_stats_on_re(device_obj, stat_name='PMI_ENCAP', node='local'), 20)
        self.assertEqual(get_pmi_stats_on_re(device_obj, stat_name='PMI_ENCAP', node='local', location='fpc0.pic0'), 20)

    @patch('jnpr.toby.security.ipsec.ipsecsrx.get_pmi_stats_on_re')
    def test_verify_pmi_stats_on_re(self, pmi_stats):
        device_obj = MagicMock()
        string = "        <product-model>vSRX</product-model>"
        device_obj.cli().response = MagicMock(return_value=string)
        pmi_stats.return_value = {'PMI_TX': 0, 'PMI_RFP': 0, 'PMI_DROP': 0, 'PMI_ENCAP_BYTES': 1400, 'PMI_DECAP': 20, 'PMI_DECAP_BYTES': 1400, 'PMI_ENCAP': 20, 'PMI_RX': 0}

        self.assertFalse(verify_pmi_stats_on_re(device_obj,stat_dict={'PMI_DROP': 20, 'PMI_RFP': 20}, relation='equal'))

  
            
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIPsecSRX)
    unittest.TextTestRunner(verbosity=2).run(suite)
