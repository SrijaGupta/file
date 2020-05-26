"""
vsrx_cloudformation.py Unit Test
"""
import sys
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from lxml import etree
import builtins
import boto3
import botocore


from jnpr.toby.services.vsrx_aws.vsrx_cloudformation import VSRXcloudformation
#from vsrx_cloudformation import VSRXcloudformation
builtins.t = MagicMock()

@attr('unit')
class test_VSRXcloudformation(unittest.TestCase):
    @patch('jnpr.toby.services.vsrx_aws.vsrx_cloudformation.VSRXcloudformation')
    def test_get_stack_descr(self,cloudformation_mock):
        response_descr_stack='efgh'
        self.assertTrue(VSRXcloudformation.get_stack_descr(cloudformation_mock,'abcd'))
        

    @patch('time.sleep')
    @patch('jnpr.toby.services.vsrx_aws.vsrx_cloudformation.VSRXcloudformation')
    def test_ver_ec2_status(self,cloudformation_mock,time_mock):
        status={}
        status['InstanceId']='abcd'
        cloudformation_mock.status_all=False
        status['InstanceStatus']={}
        status['InstanceStatus']['Details']={}
        status['InstanceStatus']['Details'][0]={}
        status['InstanceStatus']['Details'][0]['Status']='up'
        self.assertFalse(VSRXcloudformation.ver_ec2_status(cloudformation_mock,'abcd','up',240))

    @patch('jnpr.toby.services.vsrx_aws.vsrx_cloudformation.VSRXcloudformation')
    def test_stop_instance(self,cloudformation_mock):
        self.assertTrue(VSRXcloudformation.stop_instance(cloudformation_mock,'abcd'))

    @patch('jnpr.toby.services.vsrx_aws.vsrx_cloudformation.VSRXcloudformation')
    def test_start_instance(self,cloudformation_mock):
        self.assertTrue(VSRXcloudformation.start_instance(cloudformation_mock,'abcd'))

    @patch('jnpr.toby.services.vsrx_aws.vsrx_cloudformation.VSRXcloudformation')
    def test_stop_terminate_instance(self,cloudformation_mock):
        self.assertTrue(VSRXcloudformation.stop_terminate_instance(cloudformation_mock,'abcd'))

    @patch('jnpr.toby.services.vsrx_aws.vsrx_cloudformation.VSRXcloudformation')
    def test_del_cfn_stack(self,cloudformation_mock):
        self.assertTrue(VSRXcloudformation.del_cfn_stack(cloudformation_mock,'abcd'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_VSRXcloudformation)

    unittest.TextTestRunner(verbosity=2).run(suite)

