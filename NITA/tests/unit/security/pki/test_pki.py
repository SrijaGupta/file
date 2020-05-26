"""
==================================================
Description: Unit test for pki library 
Author: Niketa Chellani 
Email: nchellani@juniper.net
==================================================
"""

import os
import sys
import unittest as unittest
import jxmlease
import logging
import xml.etree.ElementTree as ET
from lxml import etree
from unittest.mock import MagicMock, patch
from jnpr.toby.hldcl.device import Device
from jnpr.toby.security.pki.pki import *

def etree2dict(tree):
    root, contents = recursive_dict(tree)
    return {root: contents}


def get_file_path(file_name):
    path = os.path.dirname(__file__)
    file = os.path.join(path, file_name)
    return file

def read_xml_file(file_name):
    xml_obj = etree.parse(get_file_path(file_name))
    xml_data = etree.tostring(xml_obj)
    return xml_data

# To return response of shell() method
class Response:
    def __init__(self, x=""):
        self.resp = x
        
    def response(self):
        return self.resp


class TestPki(unittest.TestCase):
    pki=MagicMock(spec=Pki)
    pki.handle=MagicMock()
    pki.handle.log=MagicMock()
    pki.handle.cli=MagicMock()
    pki.handle.cli.response=MagicMock()
    handle=MagicMock()

    dev_obj=MagicMock(spec=Device)

    def test_create_pki_object(self):
        self.dev_obj.log = MagicMock(return_value=True)
        self.dev_obj.config = MagicMock(return_value=True)
        
        try:
            x = create_pki_object(self.dev_obj)
            self.assertEqual(isinstance(x, Pki), True)
        except Exception as e:
            self.assertEqual(e.args[0], " missing 1 required positional argument: device handle")
            
    
    def test_configure_ca_cert(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.ca_profile='Root'
        self.pki.handle=MagicMock()
        self.pki.handle.log = MagicMock(return_value=True)
        self.pki.handle.config = MagicMock(return_value=True)

        self.pki.ca_profile = 'Root'
        self.pki.ca_identity = 'root'
        self.pki.url = 'http://10.204.128.120:8080/scep/Root/'
        self.pki.crl_url = 'http://10.204.128.120:8080/crl-as-der/currentcrl-292.crlid=292'
        self.pki.ocsp_url = 'http://10.204.128.120:8090/Root/'
        self.pki.filename = '/etc/certs/JuniperRootCA.pem'
        self.pki.refresh_interval = 1
       
        #testing configure_ca_profile with revocation disabled
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='disable', traceoptions=1, flag='all'))
        #testing configure_ca_profile with revocation crl
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='crl', crl_url=self.pki.crl_url))
        #testing configure_ca_profile with revocation ocsp
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='ocsp', ocsp_url=self.pki.ocsp_url))
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='ocsp', ocsp_url=self.pki.ocsp_url, disable_responder_revocation_check=1))
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='ocsp', ocsp_url=self.pki.ocsp_url, connection_failure='disable'))
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='ocsp', ocsp_url=self.pki.ocsp_url, connection_failure='fallback-crl'))
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='ocsp', ocsp_url=self.pki.ocsp_url, nonce_payload='disable'))
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='ocsp', ocsp_url=self.pki.ocsp_url, nonce_payload='enable'))
        self.assertTrue(configure_ca_profile(self.pki, ca_profile=self.pki.ca_profile, ca_identity=self.pki.ca_identity, url=self.pki.url, revocation_check='ocsp', ocsp_url=self.pki.ocsp_url, disable_responder_revocation_check='True'))
            

    def test_enroll_ca_cert(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.ca_profile='Root'
        self.pki.cc=1
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)
        self.pki.filename='/etc/certs/Juniper.pem'
                
        ### Positive testcase ###
        self.pki.handle.cli().response=MagicMock(return_value="CA certificate for profile Root loaded successfully")
        self.assertTrue(enroll_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0))
        self.assertTrue(enroll_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, filename=self.pki.filename, max_retries=1, wait_time=0))
        
        ### Negative testcases ###
        self.pki.handle.cli().response=MagicMock(return_value="CA certificate for Root already exists")
        self.assertFalse(enroll_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0))
        
        self.pki.handle.cli().response=MagicMock(return_value="syntax error, expecting <data>")
        self.assertFalse(enroll_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0))

        self.pki.handle.cli().response=MagicMock(return_value="syntax error, expecting <command>")
        self.assertFalse(enroll_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0))

 
    def test_verify_ca_cert(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.ca_profile='Root'
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)
        
        ### Positive testcase ###
        self.pki.handle.cli().response=MagicMock(return_value="CA certificate Root verified successfully")
        self.assertTrue(verify_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile))

        ### Negative testcases ###
        self.pki.handle.cli().response=MagicMock(return_value="error: ca-profile root is not configured")
        self.assertFalse(verify_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0))
        
        self.pki.handle.cli().response=MagicMock(return_value="error: ca-profile root doesn't exist")
        self.assertFalse(verify_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0)) 
        
        self.pki.handle.cli().response=MagicMock(return_value="CRL download failed for certificate root")
        self.assertFalse(verify_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0))

        
    def test_get_ca_cert(self):
    	self.pki=MagicMock(spec=Pki)
    	self.pki.ca_profile='scep-root'
    	self.pki.handle=MagicMock()
    	self.pki.handle.log=MagicMock(return_value=True)

        ## device is non-ha and ca-profile is given
    	xml_data = read_xml_file('ca_cert_details.xml')
    	self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
    	expected_dict={'scep-root': {'validity-not-before': '07-19-2016 18:47 UTC', 'public-key-algorithm': 'rsaEncryption', 'serial-number': '00000f49', 'recipient': '', 'public-key-length': '2048', 'validity-not-after': '07-18-2036 18:47 UTC', 'signature-algorithm': 'sha256WithRSAEncryption', 'issued-by': ''}}
    	self.assertEqual(get_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, detail=1), expected_dict)

        ## device is in non-ha and ca-profile is not given
    	xml_data = read_xml_file('ca_cert_details2.xml')
    	self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
    	expected_list=[{'scep-root': {'validity-not-after': '07-18-2036 18:47 UTC', 'recipient': '', 'issued-by': '', 'public-key-length': '2048', 'validity-not-before': '07-19-2016 18:47 UTC', 'signature-algorithm': 'sha256WithRSAEncryption', 'serial-number': '00000f49', 'public-key-algorithm': 'rsaEncryption'}}, {'ca-advpn': {'validity-not-after': '07-15-2066 22:13 UTC', 'recipient': '', 'issued-by': '', 'public-key-length': '1024', 'validity-not-before': '07-15-2016 22:13 UTC', 'signature-algorithm': 'sha256WithRSAEncryption', 'serial-number': '000005d6', 'public-key-algorithm': 'rsaEncryption'}}]
    	self.assertEqual(get_ca_cert(self.pki.handle, detail=1), expected_list)

    	## device is ha and ca-profile is given
    	xml_data = read_xml_file('ca_cert_details3.xml')
    	self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
    	expected_dict={'scep-root': {'validity-not-before': '07-19-2016 18:47 UTC', 'public-key-algorithm': 'rsaEncryption', 'serial-number': '00000f49', 'recipient': '', 'public-key-length': '2048', 'validity-not-after': '07-18-2036 18:47 UTC', 'signature-algorithm': 'sha256WithRSAEncryption', 'issued-by': ''}}
    	self.assertEqual(get_ca_cert(self.pki.handle, ca_profile=self.pki.ca_profile, detail=1), expected_dict)

    	## device is in ha and ca-profile is not given
    	xml_data = read_xml_file('ca_cert_details4.xml')
    	self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
    	expected_list=[{'scep-root': {'validity-not-after': '07-18-2036 18:47 UTC', 'recipient': '', 'issued-by': '', 'public-key-length': '2048', 'validity-not-before': '07-19-2016 18:47 UTC', 'signature-algorithm': 'sha256WithRSAEncryption', 'serial-number': '00000f49', 'public-key-algorithm': 'rsaEncryption'}}, {'ca-advpn': {'validity-not-after': '07-15-2066 22:13 UTC', 'recipient': '', 'issued-by': '', 'public-key-length': '1024', 'validity-not-before': '07-15-2016 22:13 UTC', 'signature-algorithm': 'sha256WithRSAEncryption', 'serial-number': '000005d6', 'public-key-algorithm': 'rsaEncryption'}}]
    	self.assertEqual(get_ca_cert(self.pki.handle, detail=1), expected_list)


    def test_enroll_local_cert(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.ca_profile='Root'
        self.pki.cert_id='mynewcert'
        self.pki.filename='/etc/certs/Juniper.pem'
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)

        ### Positive testcase ###
        self.pki.handle.cli().response=MagicMock(return_value='            <identifier>mynewcert</identifier>')
        self.assertTrue(enroll_local_cert(self.pki.handle, ca_profile=self.pki.ca_profile, certificate_id = self.pki.cert_id, max_retries=1, wait_time=0))
        
        ### Negative testcases ###
        self.pki.handle.cli().response=MagicMock(return_value="error: Error: Certificate mynewcert already exists")
        self.assertFalse(enroll_local_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0, certificate_id = self.pki.cert_id))
        
        self.pki.handle.cli().response=MagicMock(return_value="error: Error: Keypair doesn't exist for certificate")
        self.assertFalse(enroll_local_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0, certificate_id = self.pki.cert_id))
        
        self.pki.handle.cli().response=MagicMock(return_value="missing argument.")
        self.assertFalse(enroll_local_cert(self.pki.handle, ca_profile=self.pki.ca_profile, max_retries=1, wait_time=0, certificate_id = self.pki.cert_id))

    def test_enroll_cmpv2_cert(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.ca_profile='Root'
        self.pki.cert_id='myecdsa256'
        self.pki.ca_secret='emergency_fix_psk' 
        self.pki.ca_reference='51899'
        self.pki.size='256' 
        self.pki.email='test@juniper.net'
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)
        
        ### Positive testcase ###
        self.pki.handle.cli().response=MagicMock(return_value='            <identifier>myecdsa256</identifier>')
        self.assertTrue(enroll_cmpv2_cert(self.pki.handle, ca_profile=self.pki.ca_profile, certificate_id=self.pki.cert_id, ca_secret=self.pki.ca_secret, ca_reference=self.pki.ca_reference, email=self.pki.email, size=self.pki.size, wait_time=0, max_retries=1))
        
        ### Negative testcases ###
        self.pki.cert_id='myecdsa384'
        self.pki.handle.cli().response=MagicMock(return_value="error: Keypair doesn't exist for certificate myecdsa384")
        self.assertFalse(enroll_cmpv2_cert(self.pki.handle, ca_profile=self.pki.ca_profile, certificate_id=self.pki.cert_id, ca_secret=self.pki.ca_secret, ca_reference=self.pki.ca_reference, email=self.pki.email, size=self.pki.size, wait_time=0, max_retries=1))


    def test_generate_key_pair(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.handle=MagicMock()
        self.pki.cert_id = 'mynewcert'
        self.pki.size = 1024
        self.pki.type = 'rsa'
        self.pki.handle.log=MagicMock(return_value=True)
        
        ### Positive testcase ###
        self.pki.handle.cli().response=MagicMock(return_value='Generated key pair')
        self.assertTrue(generate_key_pair(self.pki.handle, certificate_id=self.pki.cert_id, size=self.pki.size, type=self.pki.type))
        
        ### Negative testcases ###
        self.pki.handle.cli().response=MagicMock(return_value='Command aborted as key pair already exists')
        self.assertFalse(generate_key_pair(self.pki.handle, certificate_id=self.pki.cert_id, size=self.pki.size, type=self.pki.type))
            
    def test_verify_local_cert(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.cert_id='mynewcert'
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)
        
        ### Positive testcase ###
        self.pki.handle.cli().response=MagicMock(return_value="CA certificate Root verified successfully")
        self.assertTrue(verify_local_cert(self.pki.handle, certificate_id=self.pki.cert_id))
        
        ### Negative testcases ###  
        self.pki.handle.cli().response=MagicMock(return_value="Could not find local certificate mynewcert in local database")
        self.assertFalse(verify_local_cert(self.pki.handle, certificate_id=self.pki.cert_id, max_retries=1, wait_time=0,))
        
        self.pki.handle.cli().response=MagicMock(return_value="Error: Certificate lcrt doesn't exist")
        self.assertFalse(verify_local_cert(self.pki.handle, certificate_id=self.pki.cert_id, max_retries=1, wait_time=0))

        self.pki.handle.cli().response=MagicMock(return_value="Error: Certificate lcrt is not valid yet")
        self.assertFalse(verify_local_cert(self.pki.handle, certificate_id=self.pki.cert_id, max_retries=1, wait_time=0))
        

    def test_get_local_cert(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.ca_profile='scep-root'
        self.pki.cert_id='mynewcert'
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)

        ## device is non-ha and certificate-id is given
        xml_data = read_xml_file('local_cert_details.xml')
        self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
        expected_dict =  {'mynewcert': {'signature-algorithm': 'sha256WithRSAEncryption', 'public-key-algorithm': 'rsaEncryption', 'validity-not-before': '04- 5-2018 21:58 UTC', 'public-key-length': '1024', 'validity-not-after': '04- 5-2019 22:28 UTC', 'serial-number': '025d78d9', 'recipient': '', 'issued-by': '', 'subject-ipv4-addr': '1.1.1.1'}}
        self.assertEqual(get_local_cert(self.pki.handle, certificate_id = self.pki.cert_id, detail=1), expected_dict)

        ## device is in non-ha and certificate-id is not given
        xml_data = read_xml_file('local_cert_details2.xml')
        self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
        expected_list = [{'localcert': {'signature-algorithm': 'sha256WithRSAEncryption', 'public-key-algorithm': 'rsaEncryption', 'validity-not-before': '04- 5-2018 22:00 UTC', 'public-key-length': '1024', 'validity-not-after': '07-15-2066 22:13 UTC', 'serial-number': '021d3fd4', 'recipient': '', 'issued-by': '', 'subject-ipv4-addr': '2.2.2.2'}}, {'mynewcert': {'signature-algorithm': 'sha256WithRSAEncryption', 'public-key-algorithm': 'rsaEncryption', 'validity-not-before': '04- 5-2018 21:58 UTC', 'public-key-length': '1024', 'validity-not-after': '04- 5-2019 22:28 UTC', 'serial-number': '025d78d9', 'recipient': '', 'issued-by': '', 'subject-ipv4-addr': '1.1.1.1'}}]
        self.assertEqual(get_local_cert(self.pki.handle, detail=1), expected_list)

        ##device is in ha and certitificate-id is given
        xml_data = read_xml_file('local_cert_details3.xml')
        self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
        expected_dict = {'mynewcert': {'signature-algorithm': 'sha256WithRSAEncryption', 'public-key-algorithm': 'rsaEncryption', 'validity-not-before': '04- 5-2018 22:04 UTC', 'public-key-length': '2048', 'validity-not-after': '07-15-2066 22:13 UTC', 'serial-number': '021d491b', 'recipient': '', 'issued-by': '', 'subject-ipv4-addr': '1.1.1.1'}}
        self.assertEqual(get_local_cert(self.pki.handle, certificate_id = self.pki.cert_id, detail=1), expected_dict)

        ##device is ha and certificate-id is not given
        xml_data = read_xml_file('local_cert_details4.xml')
        self.pki.handle.cli().response =  MagicMock(return_value = xml_data)
        expected_list = [{'localcert1': {'signature-algorithm': 'sha256WithRSAEncryption', 'public-key-algorithm': 'rsaEncryption', 'validity-not-before': '04- 5-2018 22:04 UTC', 'public-key-length': '2048', 'validity-not-after': '07-15-2066 22:13 UTC', 'serial-number': '021d491b', 'recipient': '', 'issued-by': '', 'subject-ipv4-addr': '1.1.1.1'}}, {'localcert2': {'signature-algorithm': 'sha256WithRSAEncryption', 'public-key-algorithm': 'rsaEncryption', 'validity-not-before': '04- 5-2018 22:04 UTC', 'public-key-length': '2048', 'validity-not-after': '04- 5-2019 22:34 UTC', 'serial-number': '025d7c22', 'recipient': '', 'issued-by': '', 'subject-ipv4-addr': '2.2.2.2'}}]
        self.assertEqual(get_local_cert(self.pki.handle, detail=1), expected_list)



    def test_add_to_trusted_ca_group(self):
        self.dev_obj.log = MagicMock(return_value=True)
        self.dev_obj.config = MagicMock(return_value=True)
        self.dev_obj.commit = MagicMock(return_value=True)
        self.assertTrue(add_to_trusted_ca_group(self.dev_obj, ca_profiles='test_ca3', trusted_ca_group='mytrust_grp', commit=True))
        self.assertTrue(add_to_trusted_ca_group(self.dev_obj, ca_profiles=['test_ca2', 'test_ca1'], trusted_ca_group='mytrust_grp'))

        try:
            x = add_to_trusted_ca_group(self.dev_obj)
        except Exception as e:
            self.assertEqual(e.args[0], "Mandatory arguments 'trusted_ca_group' or 'ca_profiles'  missing")

        #lst = [Response("error: commit failed: ")]
        self.dev_obj.commit = MagicMock(return_value="error: commit failed: ")
        try:
            x = add_to_trusted_ca_group(self.dev_obj, ca_profiles='test_ca3', trusted_ca_group='mytrust_grp', commit=True)
        except Exception as e:
            self.assertEqual(e.args[0], "error configuring: ")

    def test_clear_pki(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)
        self.pki.ca_profile='scep-root'
        self.pki.cert_id='mynewcert'

        self.assertTrue(clear_pki(self.pki.handle, ca_certificate=1, ca_profile=self.pki.ca_profile))
        self.assertTrue(clear_pki(self.pki.handle, local_certificate=1, certificate_id=self.pki.cert_id))
        self.assertTrue(clear_pki(self.pki.handle, key_pair=1, certificate_id=self.pki.cert_id))
        self.assertTrue(clear_pki(self.pki.handle, certificate_request=1, certificate_id=self.pki.cert_id))
        self.assertTrue(clear_pki(self.pki.handle, crl=1, ca_profile=self.pki.ca_profile))
        self.assertTrue(clear_pki(self.pki.handle, key_pair=1, certificate_request=1, local_certificate=1, certificate_id=self.pki.cert_id))
        self.assertTrue(clear_pki(self.pki.handle, crl=1, ca_certificate=1, ca_profile=self.pki.ca_profile))

    def test_clear_pki_all(self):
        self.pki=MagicMock(spec=Pki)
        self.pki.handle=MagicMock()
        self.pki.handle.log=MagicMock(return_value=True)
        self.assertTrue(clear_pki(self.pki.handle))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPki)
    unittest.TextTestRunner(verbosity=2).run(suite)



