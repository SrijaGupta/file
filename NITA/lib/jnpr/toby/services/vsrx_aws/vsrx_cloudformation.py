""" This script does various AWS STACK operationis using python boto3 """
import time
import sys
import os
import logging
from stat import S_IREAD
import paramiko
import boto3
from jnpr.toby.services.aws.aws import Aws
#from stat import S_IREAD, S_IRGRP, S_IROTH
#import pdb

class VSRXcloudformation(Aws):
    """ Functions to create stack """
    def __init__(self, *args, **kwargs):
        """
            Function to inherit AWS session as per credentials and config as below:

            :param:
                profile : profile from ~/.aws/config [optional]

            :return:  A handle to aws services
        """
        self.response_descr_stack = None
        self.status_all = None
        super().__init__(*args, **kwargs)

    def create_cfn_stack(self, stackname, tempurl, parameters):
        """
            Function to create stack using cloudformation template stored in S3

            :param stackname:
                The name of the stack to be created
            :param  tempurl:
                The S3 url to cloudforamtion template
            :param parameters:
                A list of dictionaries to ParameterKey and ParameterValue pairs

                eg :[
                        {
                            "ParameterKey": "vMXName",
                            "ParameterValue": "jsiji-toby-3"
                        },
                        {
                            "ParameterKey": "AvailZone",
                            "ParameterValue": "us-east-1e"
                        },
                        {
                            "ParameterKey": "SSHKey",
                            "ParameterValue": "toby-key"
                        }
                    ]
                From robot:
                ${PARAMETERS}=  Create Dictionary       vMXName=${EC2_NAME}\
                                AvailZone=${ZONE}              SSHKey=${SSHKEY}
                ${stacks} =         Create Cloudformation Stack         ${aws_handle}  ${STACK}\
                                    ${TEMPURL}          ${PARAMETERS}

            :returns True/False:
                True is creation was successful.
                Fail if creation failed.
        """
        param_list = []
        for k, val in parameters.items():
            param_list.append({'ParameterKey': k, 'ParameterValue': val})
        try:
            self.client_cfn.validate_template(TemplateURL=tempurl)
            #response = self.client_cfn.validate_template(TemplateURL=tempurl)
        except:
            logging.error(sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])
        try:
            self.client_cfn.create_stack(StackName=stackname,
                                         TemplateURL=tempurl,
                                         Parameters=param_list,
                                         Capabilities=['CAPABILITY_IAM'])
        except:
            logging.warning(sys.exc_info()[0])
        state = self.verif_st_state(stackname=stackname, state='CREATE_COMPLETE')
        state = True
        if state:
            return True
        return False

    def update_cfn_stack(self, stackname, tempurl, parameters):
        """
            Function to create stack using cloudformation template stored in S3

            :param stackname:
                The name of the stack to be created
            :param  tempurl:
                The S3 url to cloudforamtion template
            :param parameters:
                A list of dictionaries to ParameterKey and ParameterValue pairs

                eg :[
                        {
                            "ParameterKey": "vMXName",
                            "ParameterValue": "jsiji-toby-3"
                        },
                        {
                            "ParameterKey": "AvailZone",
                            "ParameterValue": "us-east-1e"
                        },
                        {
                            "ParameterKey": "SSHKey",
                            "ParameterValue": "toby-key"
                        }
                    ]
                From robot:
                ${PARAMETERS}=  Create Dictionary       vMXName=${EC2_NAME} \
                                 AvailZone=${ZONE}              SSHKey=${SSHKEY}
                ${stacks} =         Create Cloudformation Stack         ${aws_handle} \
                                     ${STACK}     ${TEMPURL}          ${PARAMETERS}

            :returns True/False:
                True is creation was successful.
                Fail if creation failed.
        """
        param_list = []
        for k, val in parameters.items():
            param_list.append({'ParameterKey': k, 'ParameterValue': val})
        try:
            self.client_cfn.validate_template(TemplateURL=tempurl)
            #response = self.client_cfn.validate_template(TemplateURL=tempurl)
        except:
            logging.error(sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])
        try:
            self.client_cfn.update_stack(StackName=stackname,
                                         TemplateURL=tempurl,
                                         Parameters=param_list,
                                         NotificationARNs=[],
                                         ResourceTypes=['AWS::EC2::VPNGateway'],
                                         Tags=[],
                                         Capabilities=[])
        except:
            logging.warning(sys.exc_info()[0])
            return False
        state = self.verif_st_state(stackname=stackname, state='UPDATE_COMPLETE')
        state = True
        if state:
            return True
        return False

    def get_stack_descr(self, stackname):
        """
            Function to get stack description

            :param stackname:
                Name of the existing stack

            :return response_descr_stack:
                Description of the stack
        """
        self.response_descr_stack = self.client_cfn.describe_stacks(
            StackName=stackname
        )
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        return self.response_descr_stack

    def get_st_resources(self, stackname, lid):
        """
            Function to get stack resource details

            :param stackname:
                Name of the stack
            :param lid:
                Logical name of the resource

            :return response_resource_stack:
                Details of the Logical resource
        """
        try:
            self.response_resource_stack = self.client_cfn.describe_stack_resource(
                StackName=stackname,
                LogicalResourceId=lid
            )
        except:
            logging.error(sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        return self.response_resource_stack

    def stop_terminate_instance(self, instance_id):
        """
            Function to stop and terminate the EC2 instance

            :param instance_id:
                The EC2 instance id

            :return status/0:
                returns instance state on success.
                0 on failure
        """

        ids = [instance_id]
        try:
            rsp = self.resource_ec2.instances.filter(InstanceIds=ids).stop()
            rsp = self.resource_ec2.instances.filter(InstanceIds=ids).terminate()
        except:
            logging.warning(sys.exc_info()[0])
        rsp = self.client_ec2.describe_instances(InstanceIds=ids)
        if rsp:
            self.status = rsp['Reservations'][0]['Instances'][0]
            return self.status['State']['Name']
        else:
            return 0

    def stop_instance(self, instance_id):
        """
            Function to stop and terminate the EC2 instance

            :param instance_id:
                The EC2 instance id

            :return status/0:
                returns instance state on success.
                0 on failure
        """

        ids = [instance_id]
        try:
            rsp = self.resource_ec2.instances.filter(InstanceIds=ids).stop()
        except:
            logging.warning(sys.exc_info()[0])
        rsp = self.client_ec2.describe_instances(InstanceIds=ids)
        if rsp:
            self.status = rsp['Reservations'][0]['Instances'][0]
            return self.status['State']['Name']
        else:
            return 0

    def start_instance(self, instance_id):
        """
            Function to start the EC2 instance

            :param instance_id:
                The EC2 instance id

            :return status/0:
                returns instance state on success.
                0 on failure
        """

        ids = [instance_id]
        try:
            rsp = self.resource_ec2.instances.filter(InstanceIds=ids).start()
        except:
            logging.warning(sys.exc_info()[0])
        rsp = self.client_ec2.describe_instances(InstanceIds=ids)
        if rsp:
            self.status = rsp['Reservations'][0]['Instances'][0]
            return self.status['State']['Name']
        else:
            return 0

    def del_cfn_stack(self, stackname):
        """
            Function to delete stack.

            :param stackname:
                Name of the stack to be deleted

            :return True/False:
                True if deletion successful
                False if deletion failed/stack already deleted.
        """
        self.client_cfn.delete_stack(
            StackName=stackname
        )
        state = self.verif_st_state(stackname, 'DELETE_COMPLETE')
        if state:
            return True
        return False

    def get_inst_name(self, fid):
        """
            When given an instance ID as str e.g. 'i-1234567', \
            return the instance 'Name' from the name tag.

            :param fid:
                instance ID

            :return instancename:
                Name of the instance
        """
        ec2instance = self.resource_ec2.Instance(fid)
        self.instancename = ''
        for tags in ec2instance.tags:
            if tags["Key"] == 'Name':
                self.instancename = tags["Value"]
        return self.instancename

    def ver_ec2_state(self, instance_id, state, waittime=900):
        """
            Verifies the state of ec2 instance against \
            the given state running/stopped/terminated/shutting-down.

            :param instance_id:
                instance ID as str e.g. 'i-1234567'
            :param state:
                state of the instance to be verified against
            :param waittime:
                Max time in seconds for the verification which will be repeated every 60s.
                Default 900s

            :return True/False:
                True if the state matches the provided state
                Else False
        """
        waittime = int(waittime)/60
        iteration = 1
        status = False
        while iteration <= waittime:
            instances = self.resource_ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': [state]}])
            for instance in instances:
                #logging.info(instance.id,instance.tags)
                if instance_id == instance.id:
                    logging.info("Instance state FOUND")
                    logging.info(instance_id, instance.id, instance.tags)
                    status = True
                    break
            if status:
                break
            time.sleep(60)
            iteration = iteration + 1
            logging.info('Status is:')
            logging.info(status)
        return self.status
    def ver_ec2_status(self, instance_id, state, waittime=900):
        """
            Verify ec2 instance status against the provided state passed/failed

            :param instance_id:
                instance ID as str e.g. 'i-1234567'
            :param state:
                state of the instance to be verified against passed/failed
            :param waittime:
                Max time in seconds for the verification which will be repeated every 60s.
                Default 900s

            :return True/False:
                True if the state matches the provided state
                Else False
        """
        waittime = int(waittime)/120
        iteration = 1
        self.status_all = False
        #flag = False
        while iteration <= waittime:
            logging.info('Iteration: ' + str(iteration))
            for status in self.resource_ec2.meta.client.describe_instance_status()\
['InstanceStatuses']:
                logging.info('************id:id-fetched:state:state-fetched****************\n\n')
                logging.info(instance_id)
                logging.info(status['InstanceId'])
                logging.info(state)
                logging.info(status['InstanceStatus']['Details'][0]['Status'])
                logging.info('********************************************\n\n')
                if instance_id == status['InstanceId']:
                    logging.info("Instance  FOUND ")
                    if state == status['InstanceStatus']['Details'][0]['Status']:
                        logging.info("Instance state FOUND ")
                        self.status_all = True
                    else:
                        logging.info("Instance state not FOUND ")
                    #flag = True
                    break
                else:
                    logging.info("Instance not FOUND ")
            if self.status_all:
                break
            time.sleep(120)
            iteration = iteration + 1
        logging.info('Status is:')
        logging.info(self.status_all)
        return self.status_all

    def verif_st_state(self, stackname, state, waittime=600):
        """
            Function to verify stack state

            :param stackname:
                Name of the the stack of which state to be verified
            :param state:
                state to os the stack to be checked against
            :param waittime:
                    Max time in seconds for the verification which will be repeated every 60s.
                    Default 600s
            :return True/False:
                True if the existing state matches param state
                False if not
        """
        waittime = int(waittime)/5
        iteration = 1
        while iteration < waittime:
            try:
                response_descr_stack = self.client_cfn.describe_stacks(
                    StackName=stackname
                )
                status = response_descr_stack['Stacks'][0]
                logging.info("State of the stack:")
                logging.info(status['StackStatus'])
                if status['StackStatus'] == state:
                    return True
                time.sleep(5)
                iteration = iteration + 1
            except:
                if state == 'DELETE_COMPLETE':
                    return True
                else:
                    logging.error(sys.exc_info()[0])
                    raise Exception(sys.exc_info()[0])
        return False
    def ssh_pub(self, hostname, myuser, sshkey, cmd):
        """
            Function to ssh a device after creation, \
            which is not present in params.yaml,  using sshkey file

            :param hostname:
                hostname of the sreated instance
            :param myuser:
                default user name of the EC2 instance, for junos currently 'jnpr'
            :param sshkey:
                ssh key file generated and used in the cloud formation stack for the instance
            :param cmd:
                The command to execute : eg: 'show chassis fpc'

            return:
                output of the command
        """
        sshcon = paramiko.SSHClient()  # will create the object
        sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())# no known_hosts error
        sshcon.connect(hostname, username=myuser, key_filename=sshkey) # no passwd needed
        stdin, stdout, stderr = sshcon.exec_command(cmd)
        stdout.channel.recv_exit_status()
        self.lines = stdout.readlines()
        sshcon.close()
        return self.lines
    def create_ssh_key_pair(self, keypair):
        """
            Function to create and download ssh_key pair

            :param aws_handle:
                    Handle crested in init
            :param keypair:
                Name of the keypair to be created.

            :return privatekey:
                Returns privatekey
        """
        try:
            keypair = self.client_ec2.create_key_pair(KeyName=keypair)
            logging.info(keypair['KeyMaterial'])
        except:
            logging.error(sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])
        return keypair['KeyMaterial']
    def import_ssh_key_pair(self, keypair, public_key):
        """
            Function to check and then import ssh_key pair

            :param aws_handle:
                    Handle created in init
            :param keypair:
                Name of the keypair to be imported.
            :param public_key:
                Public key to be imported.

        """
        try:
            response = self.client_ec2.describe_key_pairs(KeyNames=[keypair],)
            logging.debug(response['KeyPairs'])
            if response['KeyPairs']:
                return
        except:
            logging.info(sys.exc_info()[0])
            try:
                keypr = self.client_ec2.import_key_pair(
                    KeyName=keypair, PublicKeyMaterial=public_key)
                logging.info(keypr)
            except:
                logging.error(sys.exc_info()[0])
                raise Exception(sys.exc_info()[0])
            return
    def delete_ssh_key_pair(self, keypair):
        """
            Function to delete keypair.

            :param aws_handle:
                    Handle crested in init
            :param keypair:
                Name of the keypair to be created.

            :return True:
                True if deletion successful
        """
        try:
            keypair = self.client_ec2.delete_key_pair(KeyName=keypair)
        except:
            logging.error(sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])
        return True
    def verify_vpn_status(self, vpnid, state, waittime=3600):
        """
            Verifies the state of vpn connection against the given state UP/DOWN.
            :param vgwid:
                VGW ID as str e.g. 'vgw-38e94c26'
            :param state:
                state of the vpn to be verified against; UP/DOWN
            :param waittime:
                Max time in seconds for the verification which will be repeated every 60s.
                Default 3600s

            :return True/False:
                True if the state matches the provided state
                Else False
        """
        vpns = self.client_ec2.describe_vpn_connections(
            Filters=[{
                'Name' : 'vpn-connection-id',
                'Values' : [
                    vpnid]}])
        return vpns
def del_eni(self, vpcid):
    """ delete eni """
    enis = self.resource_ec2.Vpc(vpcid).network_interfaces.all()
    for eni in enis:
        try:
            eni.delete()
        except:
            logging.error(sys.exc_info()[0])
            return False
    return True
def connect_to_aws(*args, **kwargs):
    """
    Connect to AWS services

        :param
        NONE

    Returns: handles to AWS EC2 and clouformation
    """
    return VSRXcloudformation(*args, **kwargs)

def create_cloudformation_stack(aws_handle, stackname, tempurl, parameters):
    """
        Create a stack using cloudformation template

        :param aws_handle:
            Handle crested in init
        :param stackname
            Name of the stack to be created
        :param tempurl
            Location of the cloudforamtion template in S3
        :param ec2Name
            Name of the instance to be created
        :param AvailZone
            AvailabilityZone to be deployed on
        :param  SSHkey
            Keypair for the instance

        return: Binary, Stack creation successful : True
            Stack creation failed : False
    """
    return aws_handle.create_cfn_stack(stackname, tempurl, parameters)

def verify_stack_state(aws_handle, *args, **kwargs):
    """
        Function to verify stack state

        :param aws_handle:
            Handle crested in init
        :param stackname:
            Name of the the stack of which state to be verified
        :param state:
            state to os the stack to be checked against
        :param waittime:
                Max time in seconds for the verification which will be repeated every 60s.
                Default 600s

        :return True/False:
            True if the existing state matches param state
            False if not
    """
    return aws_handle.verif_st_state(*args, **kwargs)
def get_stack_resources(aws_handle, *args, **kwargs):
    """
        Function to get stack resource details

        :param aws_handle:
            Handle crested in init
        :param stackname:
            Name of the stack
        :param lid:
            Logical name of the resource

        :return response_resource_stack:
            Details of the Logical resource

    """
    return aws_handle.get_st_resources(*args, **kwargs)
def verify_ec2_status(aws_handle, *args, **kwargs):
    """
        Verify ec2 instance status against the provided state passed/failed

        :param aws_handle:
            Handle crested in init
        :param id:
            instance ID as str e.g. 'i-1234567'
        :param state:
            state of the instance to be verified against passed/failed
        :param waittime:
            Max time in seconds for the verification which will be repeated every 60s.
            Default 900s

        :return True/False:
            True if the state matches the provided state
            Else False
    """
    return aws_handle.ver_ec2_status(*args, **kwargs)
def get_stack_description(aws_handle, *args, **kwargs):
    """
        Function to get stack description

        :param aws_handle:
            Handle crested in init
        :param stackname:
            Name of the existing stack

        :return response_descr_stack:
            Description of the stack
    """
    return aws_handle.get_stack_descr(*args, **kwargs)
def get_instance_name(aws_handle, *args, **kwargs):
    """
        When given an instance ID as str e.g. 'i-1234567', \
        return the instance 'Name' from the name tag.

        :param aws_handle:
            Handle crested in init
        :param fid:
            instance ID
        :return instancename:
            Name of the instance
    """
    return aws_handle.get_inst_name(*args, **kwargs)
def ssh_public(aws_handle, *args, **kwargs):
    """
        Function to ssh a device after creation, \
        which is not present in params.yaml,  using sshkey file

        :param aws_handle:
            Handle crested in init
        :param hostname:
            hostname of the sreated instance
        :param myuser:
            default user name of the EC2 instance, for junos currently 'jnpr'
        :param sshkey:
            ssh key file generated and used in the cloud formation stack for the instance
        :param cmd:
            The command to execute : eg: 'show chassis fpc'

        return:
            output of the command
    """
    return aws_handle.ssh_pub(*args, **kwargs)
def stop_terminate_instance(aws_handle, *args, **kwargs):
    """
        Function to stop and terminate the EC2 instance

        :param aws_handle:
            Handle crested in init
        :param id:
            The EC2 instance id
        :return status/0:
            returns instance state on success.
            0 on failure
    """
    return aws_handle.stop_terminate_instance(*args, **kwargs)
def stop_instance(aws_handle, *args, **kwargs):
    """
        Function to stop the EC2 instance

        :param aws_handle:
            Handle crested in init
        :param id:
            The EC2 instance id
        :return status/0:
            returns instance state on success.
            0 on failure
    """
    return aws_handle.stop_instance(*args, **kwargs)
def start_instance(aws_handle, *args, **kwargs):
    """
        Function to start the EC2 instance

        :param aws_handle:
            Handle crested in init
        :param id:
            The EC2 instance id
        :return status/0:
            returns instance state on success.
            0 on failure
    """
    return aws_handle.start_instance(*args, **kwargs)
def verify_ec2_state(aws_handle, *args, **kwargs):
    """
        Verifies the state of ec2 instance against \
        the given state running/stopped/terminated/shutting-down.

        :param aws_handle:
            Handle crested in init
        :param id:
            instance ID as str e.g. 'i-1234567'
        :param state:
            state of the instance to be verified against
        :param waittime:
            Max time in seconds for the verification which will be repeated every 60s.
            Default 900s

        :return True/False:
            True if the state matches the provided state
            Else False
    """
    return aws_handle.ver_ec2_state(*args, **kwargs)
def delete_cfn_stack(aws_handle, *args, **kwargs):
    """
        Function to delete stack.

        :param aws_handle:
                Handle crested in init
        :param stackname:
            Name of the stack to be deleted

        :return True/False:
            True if deletion successful
            False if deletion failed/stack already deleted.
    """
    return aws_handle.del_cfn_stack(*args, **kwargs)
def update_cloudformation_stack(aws_handle, stackname, tempurl, parameters):
    """
        Function to update stack.

        :param aws_handle:
                Handle crested in init
        :param stackname:
            Name of the stack to be updated
        :param tempurl:
            Stack template name.
        :param parameters:
            list of parameters

        :return True/False:
            True if deletion successful
            False if deletion failed/stack already deleted.
    """
    return aws_handle.update_cfn_stack(stackname, tempurl, parameters)
def create_ssh_key_pair(aws_handle, *args, **kwargs):
    """
        Function to create and download ssh_key pair

        :param aws_handle:
                Handle crested in init
        :param keypair:
            Name of the keypair to be created.

        :return privatekey:
            Returns privatekey
    """
    return aws_handle.create_ssh_key_pair(*args, **kwargs)
def import_ssh_key_pair(aws_handle, *args, **kwargs):
    """
            Function to check and then import ssh_key pair

            :param aws_handle:
                    Handle created in init
            :param keypair:
                Name of the keypair to be imported.
            :param public_key:
                Public key to be imported.
    """
    return aws_handle.import_ssh_key_pair(*args, **kwargs)
def delete_ssh_key_pair(aws_handle, *args, **kwargs):
    """
        Function to delete keypair.

        :param aws_handle:
                Handle crested in init
        :param keypair:
            Name of the keypair to be created.

        :return True:
            True if deletion successful
    """
    return aws_handle.delete_ssh_key_pair(*args, **kwargs)

def verify_vpn_status(aws_handle, *args, **kwargs):
    """
        Verifies the state of vpn connection against the given state UP/DOWN.
        :param aws_handle:
                Handle crested in init
        :param vgwid:
            VGW ID as str e.g. 'vgw-38e94c26'
        :param state:
            state of the vpn to be verified against; UP/DOWN
        :param waittime:
            Max time in seconds for the verification which will be repeated every 60s.
            Default 3600s

        :return True/False:
            True if the state matches the provided state
            Else False
    """
    return aws_handle.verify_vpn_status(*args, **kwargs)
def make_read_only(filename):
    """ chnage the permission of the file to read-only """
    os.chmod(filename, S_IREAD)
def delete_eni(aws_handle, *args, **kwargs):
    """
        Verifies the state of vpn connection against the given state UP/DOWN.
        :param aws_handle:
                Handle crested in init
        :param vgwid:
            VGW ID as str e.g. 'vgw-38e94c26'
        :param state:
            state of the vpn to be verified against; UP/DOWN
        :param waittime:
            Max time in seconds for the verification which will be repeated every 60s.
            Default 3600s

        :return True/False:
            True if the state matches the provided state
            Else False
    """
    return aws_handle.del_eni(*args, **kwargs)
