import sys
import unittest2 as unittest
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, patch
from jnpr.toby.hldcl.device import Device
from jnpr.toby.security.ipsec.ipsec import *
import jnpr.toby.security.ipsec.ipsec
import os
#from Ipsec import IPSec


# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

def get_file_path(file_name):
    path = os.path.dirname(__file__)
    file = os.path.join(path, file_name)
    return file

#class TestIPsec(unittest.TestCase):
class TestIPsec(unittest.TestCase):
    # def setUp(self):
    # dev_obj = MagicMock(spec=junos)
    # return dev_obj

    mocked_obj = MagicMock(spec=IPSec)
    mocked_obj.log = MagicMock()
    mocked_obj.dh = MagicMock()
    mocked_obj.svc_intf = MagicMock()
    mocked_obj.ss = MagicMock()
    mocked_obj.ike_gw = MagicMock()
    mocked_obj.vpn_name = MagicMock()
    mocked_obj.local_gw = MagicMock()
    mocked_obj.remote_gw = MagicMock()
    mocked_obj.ext_intf = MagicMock()
    mocked_obj.tunnels = MagicMock()
    mocked_obj.num_terms = MagicMock()
    mocked_obj.num_rules = MagicMock()
    mocked_obj.ipsec_policy = MagicMock()
    mocked_obj.ipsec_proposal = MagicMock()
    mocked_obj.ike_profile = MagicMock()
    mocked_obj.ike_proposal = MagicMock()
    mocked_obj.ike_policy = MagicMock()
    mocked_obj.ike_auth = MagicMock()
    mocked_obj.ike_version = MagicMock()
    mocked_obj.ike_mode = MagicMock()
    mocked_obj.ike_clnt = MagicMock()
    mocked_obj.ike_group = MagicMock()
    mocked_obj.if_id = MagicMock()
    mocked_obj.estd_tun = MagicMock()
    # mocked_obj.vpn_rule = kwargs.get('vpn_rule','vpn_rule')
    mocked_obj.group_name = MagicMock()
    mocked_obj.protocol = MagicMock()
    mocked_obj.auth_algo = MagicMock()
    mocked_obj.encro_algo = MagicMock()
    mocked_obj.ike_auth_algo = MagicMock()
    mocked_obj.ike_encr_algo = MagicMock()
    device_obj = MagicMock(spec=Device)
    #

    def test_create_ipsec_object(self):
        #self.device_obj = MagicMock(spec=Device)
        x = create_ipsec_object(self.device_obj, svc_intf='ms-1/0/0')
        self.assertEqual(isinstance(x, IPSec), True)
        #x = create_ipsec_object(self.device_obj)
        #self.assertRaises(Exception, create_ipsec_object(self.device_obj))
        try:
            x = create_ipsec_object(self.device_obj)
        except Exception as err:
            self.assertEqual(err.args[0],"'svc_intf' parameter is mandatory")
            #self.assertRaises(Exception, x)

    def test_set_access(self):
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.config.status = MagicMock(return_value=True)
        self.mocked_obj.tunnels = 1
        self.mocked_obj.ike_profile = 'ike_access'
        self.mocked_obj.ike_client = '*'
        self.mocked_obj.ascii_key = 'juniper123'
        self.mocked_obj.ipsec_policy = 'ipsec_policy'
        self.mocked_obj.ike_policy = 'ike_policy'
        self.assertTrue(IPSec.set_access(self.mocked_obj))
        self.assertTrue(IPSec.set_access(self.mocked_obj, init_dpd='1', dpd_interval='20', dpd_threshold='3', ike_policy=1,
                             ipsec_policy=1))

    def test_set_ipsec_config(self):

        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.config.status = MagicMock(return_value=True)
        self.mocked_obj.tunnels = 10
        self.mocked_obj.ike_profile = 'ike_access'
        self.mocked_obj.ike_client = '*'
        self.mocked_obj.ascii_key = 'juniper123'
        self.mocked_obj.ipsec_policy = 'ipsec_policy'
        self.mocked_obj.ike_policy = 'ike_policy'
        self.mocked_obj.ipsec_trace = 'all'
        self.mocked_obj.ipsec_level = 'all'
        self.mocked_obj.ss = 'ipsec_ss'
        self.mocked_obj.ike_gw = "ike_gateway_"
        self.mocked_obj.vpn_name = 'vpn_'
        self.mocked_obj.local_gw = 0
        self.mocked_obj.remote_gw = 0
        # self.mocked_obj.ext_intf = kwargs.get('ext_intf')
        self.mocked_obj.tunnels = 1
        self.mocked_obj.num_terms = 1
        self.mocked_obj.num_rules = 1
        self.mocked_obj.ipsec_policy = 'ipsec_policy'
        self.mocked_obj.ipsec_proposal = 'ipsec_prop'
        self.mocked_obj.ike_profile = 'ike_access'
        self.mocked_obj.ike_proposal = 'ike_proposal'
        self.mocked_obj.ike_policy = 'ike_policy'
        self.mocked_obj.ike_auth = 'pre-shared-keys'
        self.mocked_obj.ike_version = '2'
        self.mocked_obj.ike_mode = 'main'
        self.mocked_obj.ike_clnt = '*'
        self.mocked_obj.ike_group = 'group2'
        self.mocked_obj.if_id = 'if_id'
        # self.mocked_obj.vpn_rule = kwargs.get('vpn_rule','vpn_rule')
        self.mocked_obj.group_name = 'ipsec_changes'
        self.mocked_obj.protocol = 'esp'
        self.mocked_obj.auth_algo = 'hmac-sha1-96'
        self.mocked_obj.encro_algo = '3des-cbc'
        self.mocked_obj.ike_auth_algo = 'sha1'
        self.mocked_obj.ike_encr_algo = '3des-cbc'

        # with default values
        self.assertTrue(IPSec.set_ipsec_config(self.mocked_obj))
        self.assertTrue(IPSec.set_ipsec_config(self.mocked_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test',
                                               pfs='group14', group14='300', ike_prop_desc='ike_desc',
                                               hexa_key='0x123'))
        # ike_verion=1 , ike_auth='rsa-signatures'
        self.mocked_obj.ike_auth = 'rsa-signatures'
        self.mocked_obj.ike_version = '1'
        self.assertTrue(
            IPSec.set_ipsec_config(self.mocked_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                   local_cert='test_cert', local_id_fqdn='juniper.net', ike_lifetime='300',
                                   remote_id_fqdn='juniper.net'))
        self.assertTrue(
            IPSec.set_ipsec_config(self.mocked_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                   local_cert='test_cert', local_id_key='test123', peer_cert_type='x509-signature',
                                   remote_id_key='test123'))
        self.assertTrue(
            IPSec.set_ipsec_config(self.mocked_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                   local_cert='test_cert', local_id_inet='10.0.1.1', resp_bad_spi=3, estd_tun=1,
                                   remote_id_inet='10.0.1.2'))
        self.assertTrue(
            IPSec.set_ipsec_config(self.mocked_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                   local_cert='test_cert', local_id_inet6='2001:db8:a0b:12f0::1',
                                   remote_id_inet6='2001:db8:a0b:12f0::1'))

    def test_set_ss(self):
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.config.status = MagicMock(return_value=True)
        self.mocked_obj.tunnels = 10
        self.mocked_obj.ike_profile = 'ike_access'
        self.mocked_obj.ike_client = '*'
        self.mocked_obj.ascii_key = 'juniper123'
        self.mocked_obj.ipsec_policy = 'ipsec_policy'
        self.mocked_obj.ike_policy = 'ike_policy'
        self.mocked_obj.ipsec_trace = 'all'
        self.mocked_obj.ipsec_level = 'all'
        self.mocked_obj.ss = 'ipsec_ss'
        self.mocked_obj.ike_gw = "ike_gateway_"
        self.mocked_obj.vpn_name = 'vpn_'
        self.mocked_obj.local_gw = '10.0.1.1/24'
        self.mocked_obj.remote_gw = '10.0.1.2/24'
        # self.mocked_obj.ext_intf = kwargs.get('ext_intf')
        self.mocked_obj.tunnels = 1
        self.mocked_obj.num_terms = 1
        self.mocked_obj.num_rules = 1
        self.mocked_obj.ipsec_policy = 'ipsec_policy'
        self.mocked_obj.ipsec_proposal = 'ipsec_prop'
        self.mocked_obj.ike_profile = 'ike_access'
        self.mocked_obj.ike_proposal = 'ike_proposal'
        self.mocked_obj.ike_policy = 'ike_policy'
        self.mocked_obj.ike_auth = 'pre-shared-keys'
        self.mocked_obj.ike_version = '2'
        self.mocked_obj.ike_mode = 'main'
        self.mocked_obj.ike_clnt = '*'
        self.mocked_obj.ike_group = 'group2'
        self.mocked_obj.if_id = 'if_id'
        # self.mocked_obj.vpn_rule = kwargs.get('vpn_rule','vpn_rule')
        self.mocked_obj.group_name = 'ipsec_changes'
        self.mocked_obj.protocol = 'esp'
        self.mocked_obj.auth_algo = 'hmac-sha1-96'
        self.mocked_obj.encro_algo = '3des-cbc'
        self.mocked_obj.ike_auth_algo = 'sha1'
        self.mocked_obj.ike_encr_algo = '3des-cbc'
       
        self.assertTrue(IPSec.set_ss(self.mocked_obj))
        # dial_mode=dedicated
        self.assertTrue(IPSec.set_ss(self.mocked_obj, dial_options='dedicated', dial_mode=1,
                                              sp_inside_ip='10.0.1.2', sp_outside_ip='10.0.1.1', ike_access=1,
                                              instance='vrf1', vpn_clr_df_bit=1, vpn_cp_df_bit=1, vpn_mtu='1500',
                                              arw_size='100', psv_mode=1, udp_encap=1, dst_port='8089',lgw_step=1))
        # dial_mode=shared
        self.assertTrue(IPSec.set_ss(self.mocked_obj, dial_options='shared', dial_mode=1,
                                              sp_inside_ipv6='2001:db8:a0b:12f0::2',
                                              sp_outside_ipv6='2001:db8:a0b:12f0::1',
                                              ike_access=1, instance='vrf1', vpn_clr_df_bit=1, vpn_cp_df_bit=1,
                                              vpn_mtu='1500', arw_size='100', psv_mode=1, udp_encap=1, dst_port='8089'))

        self.mocked_obj.local_gw = ['10.0.1.1/24']
        self.assertTrue(IPSec.set_ss(self.mocked_obj,no_ar=1,tcp_mss=1480))

    def test_set_rule(self):
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.config.status = MagicMock(return_value=True)
        self.mocked_obj.tunnels = 10
        self.mocked_obj.ike_profile = 'ike_access'
        self.mocked_obj.ike_client = '*'
        self.mocked_obj.ascii_key = 'juniper123'
        self.mocked_obj.ipsec_policy = 'ipsec_policy'
        self.mocked_obj.ike_policy = 'ike_policy'
        self.mocked_obj.ipsec_trace = 'all'
        self.mocked_obj.ipsec_level = 'all'
        self.mocked_obj.ss = 'ipsec_ss'
        self.mocked_obj.ike_gw = "ike_gateway_"
        self.mocked_obj.vpn_name = 'vpn_'
        self.mocked_obj.local_gw = '10.0.1.1/24'
        self.mocked_obj.remote_gw = '10.0.1.2/24'
        # self.mocked_obj.ext_intf = kwargs.get('ext_intf')
        self.mocked_obj.tunnels = 1
        self.mocked_obj.num_terms = 1
        self.mocked_obj.num_rules = 1
        self.mocked_obj.ipsec_policy = 'ipsec_policy'
        self.mocked_obj.ipsec_proposal = 'ipsec_prop'
        self.mocked_obj.ike_profile = 'ike_access'
        self.mocked_obj.ike_proposal = 'ike_proposal'
        self.mocked_obj.ike_policy = 'ike_policy'
        self.mocked_obj.ike_auth = 'pre-shared-keys'
        self.mocked_obj.ike_version = '2'
        self.mocked_obj.ike_mode = 'main'
        self.mocked_obj.ike_clnt = '*'
        self.mocked_obj.ike_group = 'group2'
        self.mocked_obj.if_id = 'if_id'
        # self.mocked_obj.vpn_rule = kwargs.get('vpn_rule','vpn_rule')
        self.mocked_obj.group_name = 'ipsec_changes'
        self.mocked_obj.protocol = 'esp'
        self.mocked_obj.auth_algo = 'hmac-sha1-96'
        self.mocked_obj.encro_algo = '3des-cbc'
        self.mocked_obj.ike_auth_algo = 'sha1'
        self.mocked_obj.ike_encr_algo = '3des-cbc'

        self.assertTrue(IPSec.set_rule(self.mocked_obj))
        self.assertTrue(IPSec.set_rule(self.mocked_obj,from_src='80.0.0.1',from_dst='30.0.0.1', init_dpd=1,
                                       dpd_interval=10,dpd_threshold=5,clr_df_bit=1,mtu=2000))
        self.assertTrue(IPSec.set_rule(self.mocked_obj, from_src='80.0.0.1', from_dst='30.0.0.1', init_dpd=1,
                                       cp_df_bit=1, set_df_bit=1, bkup_rgw='10.0.1.2/24',rgw_step_term=1,rgw_step=2))

    def test_get_ike_values(self):
        #dh = MagicMock(spec=Device)
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.get_rpc_equivalent = MagicMock(return_value='<get-ike-services-security-associations-information><detail/></get-ike-services-security-associations-information>')
        tree = ET.parse(get_file_path('ike_sa_detail.xml'))
        #import pdb
        #pdb.set_trace()
        root_elem = tree.getroot()
        #dh.execute_rpc = MagicMock()
        #mocked_obj.dh.execute_rpc.response = MagicMock(return_value=root_elem)
        self.mocked_obj.dh.execute_rpc().response =  MagicMock(return_value=root_elem)
        self.assertEqual(get_ike_values(self.mocked_obj.dh, remote_gw='10.0.1.2', key=['ike-sa-state', 'ike-sa-initiator-cookie']),
                         {'ike-sa-initiator-cookie': '16ac5f588b934e91', 'ike-sa-state': 'matured'})

        # element at first level
        self.assertEqual(get_ike_values(self.mocked_obj.dh, remote_gw='10.0.1.2', key=['ike-sa-remote-address']),
                         {'ike-sa-remote-address': '10.0.1.2'})

        # rpc error case
        self.mocked_obj.dh.execute_rpc().response = MagicMock(return_value='rpcerror')
        self.assertEqual(get_ike_values(self.mocked_obj.dh, remote_gw='10.0.1.2', key=['ike-sa-state', 'ike-sa-initiator-cookie']),
                         {'error': 'rpcerror'})

    def test_get_ipsec_values(self):
        # dh = MagicMock(spec=Device)
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.get_rpc_equivalent = MagicMock(
            return_value='<get-services-security-associations-information><detail/></get-services-security-associations-information>')
        tree = ET.parse(get_file_path('ipsec_sa_detail.xml'))

        # import pdb
        # pdb.set_trace()
        root_elem = tree.getroot()
        # dh.execute_rpc = MagicMock()
        # mocked_obj.dh.execute_rpc.response = MagicMock(return_value=root_elem)
        self.mocked_obj.dh.execute_rpc().response = MagicMock(return_value=root_elem)
        self.assertEqual(
            get_ipsec_values(self.mocked_obj.dh, remote_gw='10.0.1.2', key=['sa-state', 'sa-tunnel-mtu']),
            {'sa-state': 'installed', 'sa-tunnel-mtu': '2000'})
        # direction and key is string
        self.assertEqual(
            get_ipsec_values(self.mocked_obj.dh, remote_gw='10.0.1.2', direction='outbound',key='svc-set-name'),
            {'svc-set-name': 'ipsec_ss1'})

        # rpc error case
        self.mocked_obj.dh.execute_rpc().response = MagicMock(return_value='rpcerror')
        self.assertEqual(
            get_ipsec_values(self.mocked_obj.dh, remote_gw='10.0.1.2', direction='outbound', key='svc-set-name'),
            {'error': 'rpcerror'})

    def test_get_ipsec_stats(self):
        tree = ET.parse(get_file_path('ipsec_stats_detail.xml'))
        root_elem = tree.getroot()
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.get_rpc_equivalent = MagicMock(
            return_value='<get-services-ipsec-statistics-information><detail/></get-services-ipsec-statistics-information>')
        self.mocked_obj.dh.execute_rpc().response = MagicMock(return_value=root_elem)
        self.assertEqual(get_ipsec_stats(self.mocked_obj.dh,key=['esp-encrypted-packets']), {'esp-encrypted-packets': '0'})
        self.assertEqual(get_ipsec_stats(self.mocked_obj.dh, key='ah-authentication-failures'),
                         {'ah-authentication-failures': '0'})

    def test_get_ike_stats(self):
        tree = ET.parse(get_file_path('ike_stats.xml'))
        root_elem = tree.getroot()
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.mocked_obj.dh.get_rpc_equivalent = MagicMock(return_value='<get-ike-services-statistics/>')
        self.mocked_obj.dh.execute_rpc().response = MagicMock(return_value=root_elem)
        self.assertEqual(get_ike_stats(self.mocked_obj.dh, remote_gw='12.0.1.1',key=['ike-sa-dpd-response-payloads-sent']),
                         {'ike-sa-dpd-response-payloads-sent': '207'})

    @patch('time.sleep')
    @patch('jnpr.toby.security.ipsec.ipsec.get_ike_values')
    def test_verify_ike_state(self,get_ike, mock_sleep):
        get_ike.return_value = {'ike-sa-state': 'matured'}
        mock_sleep.return_value = True
        #import pdb
        #pdb.set_trace()
        #self.get_ike_values = MagicMock(return_value={'ike-sa-state': 'matured'})

        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.assertTrue(verify_ike_sa(self.mocked_obj.dh, remote_gw='10.0.1.2', exp_dic={'ike-sa-state': 'matured'}))
        # negative case
        get_ike.return_value = {'ike-sa-state': 'notmatured'}
        #self.mocked_obj.get_ike_values = MagicMock(return_value={'ike-sa-state': 'notmatured'})
        self.assertFalse(verify_ike_sa(self.mocked_obj.dh, remote_gw='10.0.1.2', exp_dic={'ike-sa-state': 'matured'}))
        get_ike.return_value = {'error': 'rpcerror'}
        self.assertFalse(verify_ike_sa(self.mocked_obj.dh, remote_gw='10.0.1.2', exp_dic={'ike-sa-state': 'matured'}))

    def test_mandatory_argument_case_verify_ike_state(self):
        # mandatory argument case
        try:
            verify_ike_sa(self.mocked_obj.dh, exp_dic={'ike-sa-state': 'matured'})
        except Exception as err:
            self.assertEqual(err.args[0], 'required  Arguments remote_gw missing')

    @patch('time.sleep')
    @patch('jnpr.toby.security.ipsec.ipsec.get_ipsec_values')
    def test_verify_ipsec_state(self,get_ipsec, mock_sleep):
        get_ipsec.return_value = {'sa-state': 'installed'}
        mock_sleep.return_value = True
        self.mocked_obj.dh.log = MagicMock(return_value=True)
        self.assertTrue(verify_ipsec_sa(self.mocked_obj.dh, remote_gw='10.0.1.2', exp_dic={'sa-state': 'installed'}))
        self.assertTrue(verify_ipsec_sa(self.mocked_obj.dh, remote_gw='10.0.1.2',
                                        direction='outbound', exp_dic={'sa-state': 'installed'}))
        # negative case
        get_ipsec.return_value = {'sa-state': 'not installed'}
        self.assertFalse(verify_ipsec_sa(self.mocked_obj.dh, remote_gw='10.0.1.2', exp_dic={'sa-state': 'installed'}))
        # error
        get_ipsec.return_value = {'error': 'rpcerror'}
        self.assertFalse(verify_ipsec_sa(self.mocked_obj.dh, remote_gw='10.0.1.2', exp_dic={'sa-state': 'installed'}))

    def test_mandatory_argument_case_verify_ipsec_state(self):
        # mandatory argument case
        try:
            verify_ipsec_sa(self.mocked_obj.dh, exp_dic={'sa-state': 'installed'})
        except Exception as err:
            self.assertEqual(err.args[0], 'required  Arguments remote_gw missing')

    @patch('time.sleep')
    def test_verify_pic_status(self, mock_sleep):
        mock_sleep.return_value = True
        tree = ET.parse(get_file_path('pic_status.xml'))
        root_elem = tree.getroot()
        response_object = MagicMock()
        response_object.response = MagicMock(return_value=root_elem)
        dh_object = MagicMock()
        dh_object.log = MagicMock(return_value=True)
        dh_object.get_rpc_equivalent = MagicMock(return_value='<get-pic-information/>')
        dh_object.execute_rpc = MagicMock(return_value=response_object)
        self.assertTrue(verify_pic_status(dh_object))

        # case where pic is offline
        tree = ET.parse(get_file_path('pic_status_offline.xml'))
        root_elem = tree.getroot()
        response_object = MagicMock()
        response_object.response = MagicMock(return_value=root_elem)
        dh_object.execute_rpc = MagicMock(return_value=response_object)
        self.assertFalse(verify_pic_status(dh_object))

    def test_get_string_from_log(self):
        response_object = MagicMock()
        response_object.response = MagicMock(return_value='Jan 10 01:27:52 ikev2_do_cleanup: [1ca6c00/1cfb000] Calling IPsec SA done callback with error')
        dh_object = MagicMock()
        dh_object.log = MagicMock(return_value=True)
        dh_object.shell =  MagicMock(return_value=response_object)
        self.assertEqual(get_string_from_log(dh_object,log='kmd',string='error'),
                         'Jan 10 01:27:52 ikev2_do_cleanup: [1ca6c00/1cfb000] Calling IPsec SA done callback with error')

    def test_differnt_get_ike(self):
        tree = ET.parse(get_file_path('ike_sa_detail.xml'))
        root_elem = tree.getroot()
        response_object = MagicMock()
        response_object.response = MagicMock(return_value=root_elem)
        dh_object = MagicMock()
        dh_object.log = MagicMock(return_value=True)
        dh_object.get_rpc_equivalent = MagicMock(
            return_value='<get-ike-services-security-associations-information><detail/></get-ike-services-security-associations-information>')
        dh_object.execute_rpc = MagicMock(return_value=response_object)
        self.assertEqual(
            get_ike_values(dh_object, remote_gw='10.0.1.2', key=['ike-sa-state', 'ike-sa-initiator-cookie']),
            {'ike-sa-initiator-cookie': '16ac5f588b934e91', 'ike-sa-state': 'matured'})
        # element at first level
        self.assertEqual(get_ike_values(dh_object, remote_gw='10.0.1.2', key=['ike-sa-remote-address']),
                         {'ike-sa-remote-address': '10.0.1.2'})

        # rpc error case
        response_object.response = MagicMock(return_value='rpcerror')
        dh_object.execute_rpc = MagicMock(return_value=response_object)
        self.assertEqual(
            get_ike_values(dh_object, remote_gw='10.0.1.2', key=['ike-sa-state', 'ike-sa-initiator-cookie']),
            {'error': 'rpcerror'})

    @patch('time.sleep')
    @patch('jnpr.toby.security.ipsec.ipsec.get_ike_stats')
    @patch('jnpr.toby.security.ipsec.ipsec.verify_ike_sa')
    def test_verify_dpd(self, mock_verify, get_stats, time_sleep):
        #self.verify_ike_sa = MagicMock(return_value=True)
        time_sleep.return_value = True
        mock_verify.return_value = False
        get_stats.return_value =  {'ike-sa-dpd-response-payloads-missed': '4'}
        dh_object = MagicMock()
        dh_object.log = MagicMock(return_value=True)
        self.assertTrue(verify_dpd(dh_object, dpd_int='2', dpd_thr='2',
                        key='ike-sa-dpd-response-payloads-missed', remote_gw='12.0.1.1',exp_dic={'ike-sa-state': 'UP'}))

        #negative case
        #import pdb
        #pdb.set_trace()
        get_stats.return_value = {'ike-sa-dpd-response-payloads-missed': '0'}

        self.assertFalse(verify_dpd(dh_object, dpd_int='2', dpd_thr='3',
                                   key='ike-sa-dpd-response-payloads-missed', remote_gw='12.0.1.1',
                                   exp_dic={'ike-sa-state': 'UP'}))

    def test_configure_groups_ike_access(self):
        dh_object = MagicMock()
        dh_object.log = MagicMock(return_value=True)
        dh_object.load = MagicMock(return_value=True)
        dh_object.config.status = MagicMock(return_value=True)
        self.assertTrue(configure_groups_ike_access(dh_object, groups_name='ike_groups', init_dpd='1', \
                                                    dpd_interval='20', dpd_threshold='3', ike_policy='ike_pol', \
                                                    ipsec_policy='ipsec_pol', interface_id='intf_id'))

    def test_configure_access(self):
        #device_obj = MagicMock(spec=Device)
        #self.mocked_obj = MagicMock()
        #self.mocked_obj.dh.log = MagicMock(return_value=True)
        #self.mocked_obj.dh.config.response = MagicMock(return_value=True)
        self.assertTrue(configure_access(self.mocked_obj))
        #self.assertTrue(configure_access(self.mocked_obj,init_dpd='1',dpd_interval='20',dpd_threshold='3',ike_polciy=1,ipsec_policy=1))

    def test_configure_ipsec_vpn_rule(self):
        self.assertTrue(configure_ipsec_vpn_rule(self.mocked_obj))


    def test_configure_ipsec(self):

        ipsec_obj = MagicMock()
        ipsec_obj.dh.log = MagicMock(return_value=True)
        ipsec_obj.dh.config.response = MagicMock(return_value=True)
        ipsec_obj.tunnels = 1
        ipsec_obj.ike_profile = 'ike_access'
        ipsec_obj.ike_client = '*'
        ipsec_obj.ascii_key = 'juniper123'
        ipsec_obj.ipsec_policy = 'ipsec_policy'
        ipsec_obj.ike_policy = 'ike_policy'
        ipsec_obj.ipsec_trace = 'all'
        ipsec_obj.ipsec_level = 'all'
        ipsec_obj.ss = 'ipsec_ss'
        ipsec_obj.ike_gw = "ike_gateway_"
        ipsec_obj.vpn_name = 'vpn_'
        ipsec_obj.local_gw = 0
        ipsec_obj.remote_gw = 0
        # ipsec_obj.ext_intf = kwargs.get('ext_intf')
        ipsec_obj.tunnels = 1
        ipsec_obj.num_terms = 1
        ipsec_obj.num_rules = 1
        ipsec_obj.ipsec_policy = 'ipsec_policy'
        ipsec_obj.ipsec_proposal = 'ipsec_prop'
        ipsec_obj.ike_profile = 'ike_access'
        ipsec_obj.ike_proposal = 'ike_proposal'
        ipsec_obj.ike_policy = 'ike_policy'
        ipsec_obj.ike_auth = 'pre-shared-keys'
        ipsec_obj.ike_version = '2'
        ipsec_obj.ike_mode = 'main'
        ipsec_obj.ike_clnt = '*'
        ipsec_obj.ike_group = 'group2'
        ipsec_obj.if_id = 'if_id'
        # ipsec_obj.vpn_rule = kwargs.get('vpn_rule','vpn_rule')
        ipsec_obj.group_name = 'ipsec_changes'
        ipsec_obj.protocol = 'esp'
        ipsec_obj.auth_algo = 'hmac-sha1-96'
        ipsec_obj.encro_algo = '3des-cbc'
        ipsec_obj.ike_auth_algo = 'sha1'
        ipsec_obj.ike_encr_algo = '3des-cbc'

        # with default values
        self.assertTrue(configure_ipsec(ipsec_obj))
        # with more kwargs option
        self.assertTrue(configure_ipsec(ipsec_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14', group14='300',
                                         ike_prop_desc='ike_desc', hexa_key='0x123'))
        # ike_verion=1 , ike_auth='rsa-signatures'
        ipsec_obj.ike_auth = 'rsa-signatures'
        ipsec_obj.ike_version ='1'
        self.assertTrue(configure_ipsec(ipsec_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                         local_cert='test_cert',local_id_fqdn='juniper.net',
                                         remote_id_fqdn='juniper.net'))
        self.assertTrue(configure_ipsec(ipsec_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                         local_cert='test_cert', local_id_key='test123',
                                         remote_id_key='test123'))
        self.assertTrue(configure_ipsec(ipsec_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                         local_cert='test_cert', local_id_inet='10.0.1.1',
                                         remote_id_inet='10.0.1.2'))
        self.assertTrue(configure_ipsec(ipsec_obj, ipsec_lifetime='300', ipsec_prop_desc='ipsec_test', pfs='group14',
                                         local_cert='test_cert', local_id_inet6='2001:db8:a0b:12f0::1',
                                         remote_id_inet6='2001:db8:a0b:12f0::1'))

    def test_configure_service_set(self):
        ipsec_obj = MagicMock()
        ipsec_obj.dh.log = MagicMock(return_value=True)
        ipsec_obj.dh.config.response = MagicMock(return_value=True)
        ipsec_obj.tunnels = 1
        ipsec_obj.ike_profile = 'ike_access'
        ipsec_obj.ike_client = '*'
        ipsec_obj.ascii_key = 'juniper123'
        ipsec_obj.ipsec_policy = 'ipsec_policy'
        ipsec_obj.ike_policy = 'ike_policy'
        ipsec_obj.ipsec_trace = 'all'
        ipsec_obj.ipsec_level = 'all'
        ipsec_obj.ss = 'ipsec_ss'
        ipsec_obj.ike_gw = "ike_gateway_"
        ipsec_obj.vpn_name = 'vpn_'
        ipsec_obj.local_gw = 0
        ipsec_obj.remote_gw = 0
        # ipsec_obj.ext_intf = kwargs.get('ext_intf')
        ipsec_obj.tunnels = 1
        ipsec_obj.num_terms = 1
        ipsec_obj.num_rules = 1
        ipsec_obj.ipsec_policy = 'ipsec_policy'
        ipsec_obj.ipsec_proposal = 'ipsec_prop'
        ipsec_obj.ike_profile = 'ike_access'
        ipsec_obj.ike_proposal = 'ike_proposal'
        ipsec_obj.ike_policy = 'ike_policy'
        ipsec_obj.ike_auth = 'pre-shared-keys'
        ipsec_obj.ike_version = '2'
        ipsec_obj.ike_mode = 'main'
        ipsec_obj.ike_clnt = '*'
        ipsec_obj.ike_group = 'group2'
        ipsec_obj.if_id = 'if_id'
        # ipsec_obj.vpn_rule = kwargs.get('vpn_rule','vpn_rule')
        ipsec_obj.group_name = 'ipsec_changes'
        ipsec_obj.protocol = 'esp'
        ipsec_obj.auth_algo = 'hmac-sha1-96'
        ipsec_obj.encro_algo = '3des-cbc'
        ipsec_obj.ike_auth_algo = 'sha1'
        ipsec_obj.ike_encr_algo = '3des-cbc'

        self.assertTrue(configure_service_set(ipsec_obj))
        # dial_mode=dedicated
        self.assertTrue(configure_service_set(ipsec_obj, dial_options='1', dial_mode='dedicated',
                                         sp_inside_ip='10.0.1.2', sp_outside_ip='10.0.1.1', ike_access=1,
                                         instance='vrf1', vpn_clr_df_bit=1, vpn_cp_df_bit=1, vpn_mtu='1500',
                                         arw_size='100', psv_mode=1, udp_encap=1, dst_port='8089', lgw_step=1))
        # dial_mode=shared
        self.assertTrue(configure_service_set(ipsec_obj, dial_options='1', dial_mode='shared',
                                              sp_inside_ipv6='2001:db8:a0b:12f0::2', sp_outside_ipv6='2001:db8:a0b:12f0::1',
                                              ike_access=1,instance='vrf1', vpn_clr_df_bit=1, vpn_cp_df_bit=1,
                                              vpn_mtu='1500',arw_size='100', psv_mode=1, udp_encap=1, dst_port='8089'))


    def test_load_set_config(self):
        dh_object = MagicMock()
        dh_object.log = MagicMock(return_value=True)
        dh_object.load = MagicMock(return_value=True)
        dh_object.config.status = MagicMock(return_value=True)
        command_list = ['set services service-set ipsec_ss1 ipsec-vpn-rules vpn_1',
                        'set services ipsec - vpn rule vpn_1 match - direction input']
        self.assertTrue(jnpr.toby.security.ipsec.ipsec._load_set_config(dh_object,command_list))

    """
    def test_ipsec_init(self):
        dev_obj = MagicMock(spec=Device)
        ipsec_obj = IPSec(dev_obj, svc_intf='ms-1/0/0', local_gw='10.0.1.1',
                     remote_gw='10.0.1.2', ext_intf='ge-0/2/1')
        self.assertIsInstance(ipsec_obj, IPSec)



    def test_ike_config(self):
        dev_obj = MagicMock(spec=junos)
        dev_obj.log = MagicMock(return_value=True)
        dev_obj.config = MagicMock(return_value=True)
        cobj = MagicMock(spec=Cmvpn)
        cobj.dh = dev_obj
        cobj.svc_intf = 'ms-1/0/0'
        cobj.ss = 'ipsec_ss'
        cobj.ike_gw = "ike_gateway_"
        cobj.vpn_name = 'vpn_name'
        cobj.local_gw = '10.0.1.1'
        cobj.remote_gw = '10.0.1.2'
        cobj.ext_intf = 'ge-0/2/1'
        cobj.tunnels = 1
        self.assertTrue(Cmvpn.set_ike_config(cobj))
    """

if __name__ == '__main__':
    #import pdb
    #pdb.set_trace()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIPsec)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
