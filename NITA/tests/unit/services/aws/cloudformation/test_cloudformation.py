"""
Cloudformation.py Unit Test
"""
import sys
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from lxml import etree
import builtins
import boto3
import botocore


from jnpr.toby.services.aws.cloudformation.cloudformation import *
#from jnpr.toby.toby.services.aws.cloudformation.cloudformation import *
#import jnpr.toby.services.aws.cloudformation.cloudformation
builtins.t = MagicMock()

@attr('unit')
class TestCloudformation(unittest.TestCase):
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_create_cloudformation_stack(self,cloudformation_mock):
        self.assertTrue(Cloudformation.create_cfn_stack(cloudformation_mock,'toby-unittest','https://s3-us-west-2.amazonaws.com/aws-jnpr-jdi-ops-dev-ct/toby31112/testcase4.template',{'vmxName':'toby-vm','AvailZone':'us-east-1e','SSHKEY':'toby-key'}))
    
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_get_stack_descr(self,cloudformation_mock):
        response_descr_stack='efgh'
        self.assertTrue(Cloudformation.get_stack_descr(cloudformation_mock,'abcd'))
        
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_connect_to_aws(self,cloudformation_mock):
        self.assertTrue(connect_to_aws())
    @patch('time.sleep') 
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_verify_stack_state(self,cloudformation_mock,time_mock):
        self.assertFalse(Cloudformation.verif_st_state(cloudformation_mock,'abcd','CREATE_COMPLETE'))
    
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_get_stack_resources(self,cloudformation_mock):
        self.assertTrue(Cloudformation.get_st_resources(cloudformation_mock,'abcd','vmxname'))

    @patch('time.sleep')
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_ver_ec2_status(self,cloudformation_mock,time_mock):
        status={}
        status['InstanceId']='abcd'
        cloudformation_mock.status_all=False
        status['InstanceStatus']={}
        status['InstanceStatus']['Details']={}
        status['InstanceStatus']['Details'][0]={}
        status['InstanceStatus']['Details'][0]['Status']='up'
        self.assertFalse(Cloudformation.ver_ec2_status(cloudformation_mock,'abcd','up',240))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_get_instance_name(self,cloudformation_mock):
        self.assertTrue(get_instance_name(cloudformation_mock,'abcd'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_ssh_public(self,cloudformation_mock):
        self.assertTrue(ssh_public(cloudformation_mock,'abcd','user','key','cmd'))
    
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_stop_terminate_instance(self,cloudformation_mock):
        self.assertTrue(stop_terminate_instance(cloudformation_mock,'abcd'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_stop_instance(self,cloudformation_mock):
        self.assertTrue(Cloudformation.stop_instance(cloudformation_mock,'abcd'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_start_instance(self,cloudformation_mock):
        self.assertTrue(Cloudformation.start_instance(cloudformation_mock,'abcd'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_update_cloudformation_stack(self,cloudformation_mock):
        self.assertTrue(update_cloudformation_stack(cloudformation_mock,'toby-unittest','https://s3-us-west-2.amazonaws.com/aws-jnpr-jdi-ops-dev-ct/toby31112/testcase4.template',{'vmxName':'toby-vm','AvailZone':'us-east-1e','SSHKEY':'toby-key'}))
    
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_create_ssh_key_pair(self,cloudformation_mock):
        self.assertTrue(create_ssh_key_pair(cloudformation_mock,'key'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_delete_ssh_key_pair(self,cloudformation_mock):
        self.assertTrue(delete_ssh_key_pair(cloudformation_mock,'key'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_verify_vpn_status(self,cloudformation_mock):
        self.assertTrue(verify_vpn_status(cloudformation_mock,'vgw','up','240'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_delete_eni(self,cloudformation_mock):
        self.assertTrue(delete_eni(cloudformation_mock,'vpcid'))

    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_delete_cfn_stack(self,cloudformation_mock):
        cloudformation_mock.verif_st_state('stack','DELETE_COMPLETE').return_value=False
        self.assertTrue(delete_cfn_stack(cloudformation_mock,'stack'))
        cloudformation_mock.verif_st_state('stack','DELETE_COMPLETE').return_value=True
        self.assertTrue(delete_cfn_stack(cloudformation_mock,'stack'))
    
    @patch('jnpr.toby.services.aws.cloudformation.cloudformation.Cloudformation')
    def test_verify_ec2_state(self,cloudformation_mock):
        self.assertTrue(verify_ec2_state(cloudformation_mock,'id','state',10))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCloudformation)

    unittest.TextTestRunner(verbosity=2).run(suite)
