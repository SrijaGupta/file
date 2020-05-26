import sys
import unittest2 as unittest
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock, patch, PropertyMock
#from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.device import Device
from jnpr.toby.hldcl.unix.unix import *
from jnpr.toby.security.ipsec.openssl import *

import os

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

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

class TestOpenssl(unittest.TestCase):
    linux_handle = MagicMock(spec=Unix)
    openssl_obj = MagicMock(spec=Openssl)
    openssl_obj.linux_handle =  MagicMock()
    openssl_obj.linux_handle.log = MagicMock()
    openssl_obj._chk_path = MagicMock(return_value=1)
    openssl_obj.ca_path = MagicMock()
    openssl_obj.ca_cert = MagicMock()
    openssl_obj.openssl_dir = MagicMock()
    openssl_obj.key_size = MagicMock()
    openssl_obj.key_type = MagicMock()
    openssl_obj.crl_path = MagicMock()
    openssl_obj.sign = MagicMock()
    openssl_obj.days = MagicMock()
    openssl_obj.port_number = MagicMock()
    openssl_obj.subject = MagicMock()
    openssl_obj.ca_openssl_cnf = MagicMock()
    openssl_obj.cert_dir = MagicMock()
    openssl_obj.crl_dir = MagicMock()
    openssl_obj.newcerts = MagicMock()
    openssl_obj.key = MagicMock()
    openssl_obj.hash_algo = MagicMock()
    openssl_obj.cert_file = MagicMock()
    openssl_obj.private = MagicMock()
    device_obj = MagicMock(spec=Device)

    def test_create_openssl_object(self):
        #response_object = MagicMock()
        #response_object.response = MagicMock(return_value='10.168.204.15')
        lst = [Response("10.168.204.15")]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        self.linux_handle.log = MagicMock(return_value=True)
        self.linux_handle.su = MagicMock(return_value=True)
        #self.linux_handle.shell = MagicMock(return_value=response_object)
        x = create_openssl_object(self.linux_handle, cert_name='root_ca')
        self.assertEqual(isinstance(x, Openssl), True)
        self.linux_handle.shell = MagicMock(side_effect=lst)
        x = create_openssl_object(self.linux_handle, cert_name='ca1', key_size='256',
                                  self_sign=0, parent_cert='root_ca')
        self.assertEqual(isinstance(x, Openssl), True)
        try:
            x = create_openssl_object(self.linux_handle)
        except Exception as err:
            self.assertEqual(err.args[0], "cert_name parameter is mandatory")

        try:
            x = create_openssl_object(self.linux_handle, cert_name='ca1',self_sign=0 )
        except Exception as err:
            self.assertEqual(err.args[0], "parent_cert is required for non self signed cert")

    def test_generate_openssl_ca_cert(self):
        lst = [Response("")]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        self.linux_handle.log = MagicMock(return_value=True)
        self.assertTrue(generate_openssl_ca_cert(self.openssl_obj))


    @patch('jnpr.toby.security.ipsec.openssl.update_index_file')
    def test_gen_openssl_ca_cert(self, update):
        update.return_value = True
        self.openssl_obj._invoke = MagicMock(return_value='success')
        lst = [Response("8040"), Response("8040 success"), Response("8040 success"), Response(" 8040 success"),
               Response("8040"),  Response("success"),  Response("success")]
        self.openssl_obj.linux_handle.shell = MagicMock(side_effect=lst)
        #self.linux_handle.shell.response = MagicMock(return_value=response_object)
        #self.openssl_obj.linux_handle.shell.response = 'success'
        #self.result = 'success'
        self.openssl_obj.parent_port = 8401
        self.openssl_obj.linux_handle.log= MagicMock(return_value=True)
        self.assertTrue(Openssl.gen_openssl_ca_cert(self.openssl_obj))
        self.openssl_obj.key_size=256
        self.openssl_obj.key_type = 'ecdsa'
        self.assertTrue(Openssl.gen_openssl_ca_cert(self.openssl_obj))
        # negative case
        self.openssl_obj._chk_path = MagicMock(return_value=0)
        try:
            Openssl.gen_openssl_ca_cert(self.openssl_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Failed creating private key")
        self.openssl_obj._chk_path = MagicMock(return_value=1)

        self.linux_handle.download = MagicMock(return_value=False)
        try:
            self.ca_cert = 'test_ca'
            Openssl.gen_openssl_ca_cert(self.openssl_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Downloading cert failed: test_ca.pem")

    def test_gen_cert_req(self):
        self.openssl_obj._gen_cert_req_router = MagicMock(return_value=True)
        self.assertTrue(Openssl.gen_cert_req(self.openssl_obj,'router_handle'))

    def test_gen_cert_req_router(self):
        self.device_obj.log = MagicMock(return_value=True)
        lst = [Response("Generated"), Response("success")]
        self.device_obj.cli = MagicMock(side_effect=lst)
        self.device_obj.download = MagicMock(return_value=True)
        self.assertTrue(Openssl._gen_cert_req_router(self.openssl_obj, self.device_obj, cert_id='test_local'))
        try:
            Openssl._gen_cert_req_router(self.openssl_obj, self.device_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "cert_id parameter is mandatory")
        lst = [Response("Generated"), Response("error")]
        self.device_obj.cli = MagicMock(side_effect=lst)
        try:
            Openssl._gen_cert_req_router(self.openssl_obj, self.device_obj,cert_id='test_local')
        except Exception as err:
            self.assertEqual(err.args[0], "Failed Generating cert request error")

    #@mock.patch("open", create=True)
    #@mock.patch("write", create=True)
    #@patch("close", create=True)
    @patch('jnpr.toby.security.ipsec.openssl.update_index_file')
    @patch('jnpr.toby.security.ipsec.openssl.gen_crl')
    def test_sign_cert(self, mock_update, mock_gen_crl):
        self.openssl_obj.domain_name = 'juniper.net'
        self.openssl_obj.email = 'test@juniper.net'
        self.openssl_obj.ip ='1.1.1.1'
        #mock_open.side_effect = mock.mock_open(
        #    write_data="subjectAltName=DNS:juniper.net,email:test@juniper.net").return_value
        self.open = MagicMock(return_value=True)
        self.write = MagicMock(return_value=True)
        self.close = MagicMock(return_value=True)

        mock_update.return_value = True
        mock_gen_crl.return_value = True
        self.device_obj.log = MagicMock(return_value=True)
        self.linux_handle.log = MagicMock(return_value=True)
        self.openssl_obj._invoke = MagicMock(return_value='success')
        self.device_obj.upload = MagicMock(return_value=True)
        self.device_obj.download = MagicMock(return_value=True)
        self.assertTrue(Openssl.sign_cert(self.openssl_obj))
        self.openssl_obj.local_cert = 'test_local'
        self.assertTrue(Openssl.sign_cert(self.openssl_obj))
        try:
            self.linux_handle.upload = MagicMock(return_value=False)
            #self.openssl_obj.cert_file = 'test.pem'
            x = Openssl.sign_cert(self.openssl_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Upload of openssl.cnf failed")

    #@patch('jnpr.toby.hldcl.juniper.junipersystem.JuniperSystem.cli')
    def test_load_cert(self):
        lst = [Response("success"), Response("success"), Response("success")]
        self.device_obj.log = MagicMock(return_value=True)
        self.device_obj.cli = MagicMock(side_effect=lst)
        #mock_cli.response.side_effect =  ['success', 'test']
        #lst = [Response("success"), Response("success")]
        #self.device_obj.cli = MagicMock(side_effect=lst)
        #self.device_obj.cli.response = MagicMock(side_effect=lst)
        #response = MagicMock(side_effect=lst)
        self.device_obj.upload = MagicMock(return_value=True)
        self.device_obj.download = MagicMock(return_value=True)
        self.assertTrue(Openssl.load_cert(self.openssl_obj))
        try:
            self.device_obj.upload = MagicMock(return_value=False)
            self.openssl_obj.cert_file = 'test.pem'
            x = Openssl.load_cert(self.openssl_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Upload of test.pem failed")

    def test_invoke(self):
        self.openssl_obj.linux_handle.log = MagicMock(return_value=True)
        lst = [Response("success")]
        self.openssl_obj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertEqual(Openssl._invoke(self.openssl_obj, 'ls'), 'success')
        #negative test case

    def test_chk_path(self):
        lst = [Response('test.txt'), Response('No such file or dir')]
        self.openssl_obj.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertEqual(Openssl._chk_path(self.openssl_obj, 'test.txt'), 1)
        #negative case
        self.assertEqual(Openssl._chk_path(self.openssl_obj, 'test.txt'), 0)

    @patch('os.path.isfile')
    @patch('os.unlink')
    def test_edit_openssl_cnf(self, mock_isfile, mock_unlink):
        lst = [Response("success")]
        mock_isfile.side_effects = lst
        mock_unlink.side_effects = True
        open = MagicMock(return_value=True)
        write = MagicMock(return_value=True)
        self.openssl_obj.host_ip = '1.1.1.1'
        self.openssl_obj.linux_handle.download = MagicMock(return_value=True)
        self.assertTrue(Openssl._edit_openssl_cnf(self.openssl_obj))
        self.openssl_obj.parent_cert = 'test_root'
        self.openssl_obj.parent_port = '8401'
        self.assertTrue(Openssl._edit_openssl_cnf(self.openssl_obj))
        #negative case
        try:
            self.linux_handle.upload = MagicMock(return_value=False)
            #self.openssl_obj.cert_file = 'test.pem'
            x = Openssl._edit_openssl_cnf(self.openssl_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Uploading openssl.cnf.TRUE failed")

    def test_gen_crl(self):
        self.linux_handle.log = MagicMock(return_value=True)
        self.linux_handle.su = MagicMock(return_value=True)
        isinstance = True
        cert_name ='test'
        lst = [Response('success'), Response('True'),Response('True'),Response('True'),Response('True'),Response('True')]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(gen_crl(self.linux_handle,cert_name=cert_name))
        try:
            x = gen_crl(self.linux_handle)
        except Exception as err:
            self.assertEqual(err.args[0], "Missing required argument 'cert_name'")
        try:
            lst = [Response('success'), Response('error'), Response('True'), Response('True'), Response('True')]
            self.linux_handle.shell = MagicMock(side_effect=lst)
            x = gen_crl(self.linux_handle, cert_name=['test_ca', 'test_subca'])
        except Exception as err:
            self.assertEqual(err.args[0], "Failed Generating cert request error")

    def test_start_ocsp_responder(self):
        self.linux_handle.log = MagicMock(return_value=True)
        self.linux_handle.su = MagicMock(return_value=True)
        lst = [Response('8400'), Response('True'), Response('True'), Response('Waiting Client connections')]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        self.assertTrue(start_ocsp_responder(self.linux_handle, 'test_ca'))
        try:
            lst = [Response('8400'), Response('True'), Response('True'), Response('error in starting')]
            self.linux_handle.shell = MagicMock(side_effect=lst)
            x = start_ocsp_responder(self.linux_handle, cert_name='test_ca')
        except Exception as err:
            self.assertEqual(err.args[0], "Failed starting ocsp responder error in starting")

    @patch(builtin_string + '.open')
    #@patch(builtin_string + '.close')
    @patch('jnpr.toby.security.ipsec.openssl.start_ocsp_responder')
    def test_revoke_cert(self,open_mock,mock_ocsp_responder):
        self.linux_handle.log = MagicMock(return_value=True)
        self.linux_handle.su = MagicMock(return_value=True)
        lst = [Response('True'), Response('True'), Response('True'), Response('somw string'),
               Response('somw string'), Response('somw string'), Response('somw string'), Response('somw string'),
               Response('somw string'), Response('somw string')]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        self.linux_handle.download = MagicMock(return_value=True)
        self.linux_handle.upload = MagicMock(return_value=True)
        #self.open = MagicMock(return_value=True)
        #self.readlines = MagicMock(return_value=True)
        #self.close = MagicMock(return_value=True)
        #mock_open = MagicMock()
        open_mock.return_value = True
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.readlines.return_value = 'test string'
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        self.assertTrue(revoke_cert(self.linux_handle, cert_name='test_ca', local_cert='local_test'))

        # download exception
        self.linux_handle.download = MagicMock(return_value=False)
        try:
            x = revoke_cert(self.linux_handle, cert_name='test_ca', local_cert='local_test')
        except Exception as err:
            self.assertEqual(err.args[0], "Downloading index file failed: /etc/pki/script_gen/test_ca/index.txt")

        self.linux_handle.download = MagicMock(return_value=True)
        # upload
        # download exception
        self.linux_handle.upload = MagicMock(return_value=False)
        try:
            x = revoke_cert(self.linux_handle, cert_name='test_ca', local_cert='local_test')
        except Exception as err:
            self.assertEqual(err.args[0], "Uploading request file failed /etc/pki/script_gen/test_ca/newindex.txt")

        self.linux_handle.upload = MagicMock(return_value=True)
        #Having local_cert in readlines
        """
        open_mock.return_value = True
        open_obj = MagicMock()
        open_obj.write.return_value = True
        open_obj.readlines.return_value = 'local_test subject'
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        self.assertTrue(revoke_cert(self.linux_handle, cert_name='test_ca', local_cert='local_test'))
        """
        #ca cert
        lst = [Response('issuer= /C=US/ST=CA/L=Sunnyvale/O=Juniper/CN=test_root_ca/OU=QA'), Response('True'), Response('True'), Response('somw string'),
               Response('somw string'), Response('somw string'), Response('somw string'), Response('somw string'),
               Response('somw string'), Response('somw string')]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        mock_ocsp_responder.return_value = True
        #import pdb
        #pdb.set_trace()
        self.assertTrue(revoke_cert(self.linux_handle, cert_name='test_ca', ocsp=1))
        try:
            x = revoke_cert(self.linux_handle)
        except Exception as err:
            self.assertEqual(err.args[0], "required argument missing 'cert_name'")
        try:
            lst = [Response('issuer= /C=US/ST=CA/L=Sunnyvale/O=Juniper/CN=test_root_ca/OU=QA'), Response('True'),
                   Response('error revoking cert'), Response('somw string'),
                   Response('somw string'), Response('somw string'), Response('somw string'), Response('somw string'),
                   Response('somw string'), Response('somw string')]
            self.linux_handle.shell = MagicMock(side_effect=lst)
            x = revoke_cert(self.linux_handle, cert_name='test_ca', ocsp=1)
        except Exception as err:
            self.assertEqual(err.args[0], "Failed to revoke cert error revoking cert")
        try:
            lst = [Response('issuer= /C=US/ST=CA/L=Sunnyvale/O=Juniper/CN=test_root_ca/OU=QA'), Response('True'),
                   Response('some string'), Response('error regenerating'),
                   Response('somw string'), Response('somw string'), Response('somw string'), Response('somw string'),
                   Response('somw string'), Response('somw string')]
            self.linux_handle.shell = MagicMock(side_effect=lst)
            x = revoke_cert(self.linux_handle, cert_name='test_ca', ocsp=1)
        except Exception as err:
            self.assertEqual(err.args[0], "Failed to re-generate crl error regenerating")

    def test_get_file_stamp(self):
        self.assertEqual(get_timestamp('Apr 24 08:26:52 2018 GMT'), '180424082652Z')


    @patch(builtin_string + '.open')
    def test_update_index_file(self, open_mock):
        open_mock.return_value = True
        open_obj = MagicMock()
        open_obj.write.return_value = True
        #open_obj.readlines.return_value = 'test string'
        open_obj.close.return_value = True
        open_mock.return_value = open_obj
        self.linux_handle.log = MagicMock(return_value=True)
        self.linux_handle.su = MagicMock(return_value=True)
        result = """notBefore=Apr 24 08:26:52 2017 GMT\r
notAfter=Apr 24 08:26:52 2018 GMT\r
serial=841B8989DD817DDC\r
subject= /C=US/ST=CA/L=Sunnyvale/O=Juniper/CN=local_neg/CN=test@juniper.net/OU=QA\r"""
        lst = [Response(result), Response('True'), Response('True'), Response('somw string')]
        self.linux_handle.shell = MagicMock(side_effect=lst)
        self.linux_handle.download = MagicMock(return_value=True)
        self.linux_handle.upload = MagicMock(return_value=True)
        self.assertTrue(update_index_file(self.linux_handle, '/etc/pki/script_gen/test_ca/certs/test_ca.pem', '/etc/pki/script_gen/test_ca/certs/index.txt'))

if __name__ == '__main__':
    #import pdb
    #pdb.set_trace()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOpenssl)
    unittest.TextTestRunner(verbosity=2).run(suite)

