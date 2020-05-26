#!/usr/bin/env python
#from jnpr.jet.JetHandler import *
import argparse
import sys,time,os
import logging


from datetime import datetime
#import pexpect
##sys.path.append("/var/www/html/CAT/user/ravimr/Projects/Cos_24/lib")
sys.path.append("/var/www/html/CAT/user/ravimr/Projects/Cos_code1/lib")
sys.path.append("/var/www/html/CAT_CLI/CAT/lib")

from grpc.beta import implementations
from grpc.framework.interfaces.face.face import *

import authentication_service_pb2
from authentication_service_pb2 import *
import cosd_service_pb2
from cosd_service_pb2 import *
import re


parser = argparse.ArgumentParser()
parser.add_argument('-d','--device', help='Input host name',required=True)
#parser.add_argument('-ifl','--iflname', help='Input interface name',required=True)

args = parser.parse_args()




client_id = '1'
#device1 = "10.216.65.40"
device1 = args.device
APP_USER = 'root'
APP_PASSWORD = 'Embe1mpls'
port = 15000



channel = implementations.insecure_channel(host=device1, port=port)
stub = authentication_service_pb2.beta_create_Login_stub(channel)
login_response = stub.LoginCheck(authentication_service_pb2.LoginRequest(user_name=APP_USER,password=APP_PASSWORD, client_id=client_id),1)
cos = cosd_service_pb2.beta_create_CosService_stub(channel)

if (login_response.result == 1):
            print "Login to device successful"
else:
            print "Login to  device failed"
            raise SystemExit()


def pause():
    programPause = raw_input("Enter to continue...")

try:
	########### classifier types and rewrite types  #####
	rewrite_type_INVALID 	=  FEATURE_CP_TYPE_INVALID
        classifier_rewrite_type_INET    	=  FEATURE_CP_TYPE_INET_PRECEDENCE
	classifier_rewrite_type_DSCP    	=  FEATURE_CP_TYPE_DSCP
	classifier_rewrite_type_DSCP_IPV6	=  FEATURE_CP_TYPE_DSCP_IPV6
	classifier_rewrite_type_EXP		=  FEATURE_CP_TYPE_EXP 
        classifier_rewrite_type_IEEE8021	=  FEATURE_CP_TYPE_IEEE8021     
	classifier_rewrite_type_IEEE8021AD      =  FEATURE_CP_TYPE_IEEE8021AD 
	
	#CosMessageAttribOperation
	operation_ADD 		= ATTRIB_ADD 
	operation_CHANGE 	= ATTRIB_CHANGE
	operation_DELETE 	= ATTRIB_DELETE
	operation_NOOP 		= ATTRIB_NOOP
	
	#loss_priority
	loss_priority_INVALID		= CLFR_RW_LP_INVALID 
    	loss_priority_HIGH		= CLFR_RW_LP_HIGH
    	loss_priority_MEDIUM_HIGH	= CLFR_RW_LP_MEDIUM_HIGH 
    	loss_priority_MEDIUM_LOW	= CLFR_RW_LP_MEDIUM_LOW 
    	loss_priority_LOW		= CLFR_RW_LP_LOW 

  	#API TIOMEOUT
	api_timeout = 1
	t1 = time.time()
	l = time.asctime(time.localtime(time.time()))
	print "############### ForwardClassGet ################"
	print "####################################################"
        for b in range(0,701):

                api_request = CosClassifier(classifier_name     ="cos"+str(b),
                                    classifier_type     =classifier_rewrite_type_INET,
                                    sharable            =True, ######### FALSE
                                    rule                =[ClassifierRule(operation = operation_ADD ,
                                                                        forwarding_class_name="nc3", ## STRING
                                                                        loss_priority=loss_priority_MEDIUM_HIGH,
                                                                        code_points=[1])])
      #         print api_request
                result = cos.ClassifierAdd(api_request, api_timeout)
     #          print 'Invoking fw.ClassifierAdd \nreturn = ', result , l , b 



	print "Time taken to add classifer: ", time.time() - t1 , l , b 


	
		#if result.status is EOK :
            	#	print "ForwardClassGet RPC Passed"
    		#else:
            	#	print "ForwardClassGet RPC Failed"
	
    	
	
	pause()

except Exception as tx:
        print '%s' % (tx.message)
    

while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)





		
