import boto3
import time
import sys

class Aws(object):
    def __init__(self,profile='default'):
        """
        Function to initiate AWS session as per credentials and config as below:

        :param:
            profile from /home/regress/.aws/config

        :return:  A handle to aws services

        """

        dev = boto3.session.Session(profile_name=profile)
        self.resource_ec2 = dev.resource('ec2')
        self.client_ec2 = dev.client('ec2')
        self.client_cfn = dev.client('cloudformation')
