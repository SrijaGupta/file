#!/usr/bin/env python
#from jnpr.jet.JetHandler import *

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


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d','--device', help='Input host name',required=True)
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
	
	name = "0000000000000000000000000000000"
	print "################################################################################################ Rewrite ADD COS1 IEEE8021AD ################"
	print "################################################################################################################################"
	
 	api_request = CosRewrite(rewrite_name	="cos", 
				    rewrite_type	=classifier_rewrite_type_IEEE8021AD,
				    sharable		=True, ######### FALSE
				    rule		=[RewriteRule(operation = operation_ADD ,
									forwarding_class_name="nc3", ## STRING
					   				loss_priority=loss_priority_MEDIUM_HIGH,
					   				code_point_options=FeatureCodePoint(code_point= 15))])
				    ####ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
	
        print api_request
	result = cos.RewriteAdd(api_request, api_timeout)
	print 'Invoking fw.RewriteAdd \nreturn = ', result
	
	if result.status is EOK :
            print "RewriteAdd RPC Passed"
    	else:
            print "RewriteAdd RPC Failed"
	
	pause()
	print "################################################################################################ Rewrite ADD COS IEEE8021AD ################"
	print "################################################################################################################################"
 	api_request = CosRewrite(rewrite_name	="cos1", 
				    rewrite_type	=classifier_rewrite_type_IEEE8021AD,
				    sharable		=True, ######### FALSE
				    rule		=[RewriteRule(operation = operation_ADD ,
									forwarding_class_name="nc3", ## STRING
					   				loss_priority=loss_priority_MEDIUM_LOW,
					   				code_point_options=FeatureCodePoint(code_point_str="0101"))])
				    ####ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
        print api_request
	result = cos.RewriteAdd(api_request, api_timeout)
	print 'Invoking fw.RewriteAdd \nreturn = ', result
	
	if result.status is EOK :
            print "RewriteAdd RPC Passed"
    	else:
            print "RewriteAdd RPC Failed"
	
	pause()
	print "################################################################################################ Rewrite Change ################"
	print "################################################################################################################################"

	api_request = CosRewrite(rewrite_name	="cos1", 
				    rewrite_type	=classifier_rewrite_type_IEEE8021AD,
				    sharable		=True, ######### FALSE
				    rule		=[RewriteRule(operation = operation_CHANGE ,
									forwarding_class_name="be1", ## STRING
					   				loss_priority=loss_priority_HIGH,
					   				code_point_options=FeatureCodePoint(code_point_str="0011"))])
				    ####ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
	print api_request
	result = cos.RewriteChange(api_request, api_timeout)
	print 'Invoking cos.RewriteChange \nreturn = ', result 
	
	if result.status is EOK :
            print "RewriteChange RPC Passed"
    	else:
            print "RewriteChange RPC Failed"
	
	pause()
	print "################################################################################################ Rewrite Change ATR DELETE ################"
	print "################################################################################################################################"

	api_request = CosRewrite(rewrite_name	="cos1", 
				    rewrite_type	=classifier_rewrite_type_IEEE8021AD,
				    sharable		=True, ######### FALSE
				    rule		=[RewriteRule(operation = operation_DELETE ,
									forwarding_class_name="be1", ## STRING
					   				loss_priority=loss_priority_HIGH,
					   				code_point_options=FeatureCodePoint(code_point_str="0011"))])
				    ####ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
	print api_request
	result = cos.RewriteChange(api_request, api_timeout)
	print 'Invoking cos.RewriteChange \nreturn = ', result 
	
	if result.status is EOK :
            print "RewriteChange RPC Passed"
    	else:
            print "RewriteChange RPC Failed"
	
	pause()

	
	print "################################################################################################ Rewrite Get ################"
	print "################################################################################################################################"

	api_request = CosRewrite(rewrite_name	="cos", 
				    rewrite_type	=classifier_rewrite_type_IEEE8021AD,
				    ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
	#print api_request
	result = cos.RewriteGet(api_request, api_timeout)
	print 'Invoking cos.RewriteGet \nreturn = ', result 
	
	if result.status is EOK :
            print "RewriteGet RPC Passed"
    	else:
            print "RewriteGet RPC Failed"
	
	pause()

	print "################################################################################################ Rewrite Get NEXT ################"
	print "################################################################################################################################"

	api_request = CosRewrite(rewrite_name="cos", rewrite_type=classifier_rewrite_type_IEEE8021AD)
   	result = cos.RewriteGetNext(api_request, api_timeout)
	
	print 'Invoking cos.RewriteNext \nreturn = ', result 
	
	if result.status is EOK :
            print "RewriteNext RPC Passed"
    	else:
            print "RewriteNext RPC Failed"
	
	pause()
	
	print "################################################################################################ Rewrite Bulk GET ################"
	print "################################################################################################################################"

	api_request = CosRewrite(rewrite_name="cos", rewrite_type=classifier_rewrite_type_IEEE8021AD)
 #  	result = cos.RewriteBulkGet(api_request, api_timeout)
	
#	print 'Invoking cos.RewriteBulkGet \nreturn = ', result 
	
	#if result.status is EOK :
         #   print "RewriteBulkGet RPC Passed"
    	#else:
        #    print "RewriteBulkGet RPC Failed"
	
#	
	x = 1
	
	for stream in cos.RewriteBulkGet(api_request,10):
		i = x
		print 'Invoking cos.RewriteBulkGet \nreturn = ', stream , str(i)	
		x += 1
	pause()

	
	print "################################################################################################ Rewrite Delete cos ################"
	print "################################################################################################################################"



    	api_request = CosRewrite(rewrite_name="cos", rewrite_type=classifier_rewrite_type_IEEE8021AD,)# rule=[RewriteRule(code_points=[1], forwarding_class_name="be1")])
    	result = cos.RewriteDelete(api_request, api_timeout)
	print 'Invoking cos.RewriteDelete \nreturn = ', result 
	
	if result.status is EOK :
            print "RewriteBulkGet RPC Passed"
    	else:
            print "RewriteBulkGet RPC Failed"
	
	#pause()
	
	print "################################################################################################ Rewrite Delete cos1 ################"
	print "################################################################################################################################"



    	api_request = CosRewrite(rewrite_name="cos1", rewrite_type=classifier_rewrite_type_IEEE8021AD,)# rule=[RewriteRule(code_points=[1], forwarding_class_name="be1")])
    	result = cos.RewriteDelete(api_request, api_timeout)
	print 'Invoking cos.RewriteDelete \nreturn = ', result 
	
	if result.status is EOK :
            print "RewriteBulkGet RPC Passed"
    	else:
            print "RewriteBulkGet RPC Failed"
	
	pause()
except AbortionError as e:
        	print "code is ", e.code
		print "details is ", e.details
except Exception as tx:
        print '%s' % (tx.message)
    

while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)


		
