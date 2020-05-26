

#!/usr/bin/env python
#from jnpr.jet.JetHandler import *

#!/usr/bin/env python
#from jnpr.jet.JetHandler import *

import sys,time,os
import logging


from datetime import datetime
#import pexpect
##sys.path.append("/var/www/html/CAT/user/ravimr/Projects/Cos_24/lib")
sys.path.append("/var/www/html/CAT/user/ravimr/Projects/Cos_code1/lib")
sys.path.append('/opt/lib/python2.7/site-packages/jnpr/jet/grpc_services/ ')
sys.path.append("/var/www/html/CAT_CLI/CAT/lib")

from grpc.beta import implementations
from grpc.framework.interfaces.face.face import *

import authentication_service_pb2
from authentication_service_pb2 import *
import cosd_service_pb2
from cosd_service_pb2 import *
import re
from grpc.framework.interfaces.face.face import * 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-d','--device', help='Input host name',required=True)
#parser.add_argument('-ifl','--iflname', help='Input interface name',required=True)
args = parser.parse_args()




client_id = '1'
#device1 = "10.216.66.148"
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
	

	
	print "################################################################################################ Classifier ADD COS1 EXP ################"
	print "################################################################################################################################"
	
 	api_request = CosClassifier(classifier_name	="cos", 
				    classifier_type	=classifier_rewrite_type_EXP,
				    sharable		=True, ######### FALSE
				    rule		=[ClassifierRule(operation = operation_ADD ,
									forwarding_class_name="nc3", ## STRING
					   				loss_priority=loss_priority_MEDIUM_HIGH,
					   				code_points=[1])])
				    ####ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
        print api_request
	result = cos.ClassifierAdd(api_request, api_timeout)
	print 'Invoking fw.ClassifierAdd \nreturn = ', result
	
	if result.status is EOK :
            print "ClassifierAdd RPC Passed"
    	else:
            print "ClassifierAdd RPC Failed"
	
	pause()
	print "################################################################################################ Classifier ADD COS1 DSCP ################"
	print "################################################################################################################################"
	
 	api_request = CosClassifier(classifier_name	="cos1", 
				    classifier_type	=classifier_rewrite_type_EXP,
				    sharable		=True, ######### FALSE
				    rule		=[ClassifierRule(operation = operation_ADD ,
									forwarding_class_name="nc3", ## STRING
					   				loss_priority=loss_priority_MEDIUM_HIGH,
					   				code_points=[1])])
				    ####ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
        print api_request
	result = cos.ClassifierAdd(api_request, api_timeout)
	print 'Invoking fw.ClassifierAdd \nreturn = ', result
	
	if result.status is EOK :
            print "ClassifierAdd RPC Passed"
    	else:
            print "ClassifierAdd RPC Failed"
	
	pause()
	######Classifer type ::
	class_type_DSCP 	= RI_CLFR_CP_TYPE_DSCP
	class_type_INVALID 	= RI_CLFR_CP_TYPE_INVALID 
    	class_type_DSCP_IPV6    = RI_CLFR_CP_TYPE_DSCP_IPV6
    	class_type_EXP 		= RI_CLFR_CP_TYPE_EXP
    	class_type_IEEE8021 	= RI_CLFR_CP_TYPE_IEEE8021
    	class_type_NO_DEFAULT   = RI_CLFR_CP_TYPE_NO_DEFAULT
	######Rewrite type
	rw_type_INVALID 	= RI_RW_CP_TYPE_INVALID
    	rw_type_IEEE8021 	= RI_RW_CP_TYPE_IEEE8021
    	rw_type_IEEE8021AD 	= RI_RW_CP_TYPE_IEEE8021AD
	#######Classifer tags####
	class_tag_INVALID	=RI_CLFR_IEEE8021_TAG_MODE_INVALID
        class_tag_INNER		=RI_CLFR_IEEE8021_TAG_MODE_ENCAP_VLAN_TAG_INNER
    	class_tag_OUTER		=RI_CLFR_IEEE8021_TAG_MODE_ENCAP_VLAN_TAG_OUTER
	#######Rewrite tags####
	rw_tag_INVALID		=RI_RW_IEEE8021X_TAG_MODE_INVALID
    	rw_tag_OUTER		=RI_RW_IEEE8021X_TAG_MODE_ENCAP_VLAN_TAG_OUTER
	rw_tag_OUTER_AND_INNER  =RI_RW_IEEE8021X_TAG_MODE_ENCAP_VLAN_TAG_OUTER_AND_INNER

	print "################################################################################################ RT ADD ################"
	print "################################################################################################################################"


	api_request = CosRoutingInstanceBindPoint(
						 classifiers=[CosRoutingInstanceClassifier(feature_object_name="cos1",
						 type=class_type_EXP, operation=ATTRIB_ADD)], 
						 routing_instance_name="pe1")
	print api_request
	result = cos.RoutingInstanceBindPointAdd(api_request, api_timeout)
	print 'Invoking fw.RoutingInstanceBindPointAdd \nreturn = ', result

	pause()

	print "################################################################################################ RT Change Change cos1 EXP ################"
	print "################################################################################################################################"


	api_request = CosRoutingInstanceBindPoint(
						 classifiers=[CosRoutingInstanceClassifier(feature_object_name="cos",
						 type=class_type_EXP, operation=ATTRIB_ADD)], 
						 routing_instance_name="pe1")
	print api_request
	result = cos.RoutingInstanceBindPointChange(api_request, api_timeout)
	print 'Invoking fw.RoutingInstanceBindPointchange \nreturn = ', result

	pause()
	print "################################################################################################ RT ADD ################"
	print "################################################################################################################################"


	api_request = CosRoutingInstanceBindPoint(
						 classifiers=[CosRoutingInstanceClassifier(feature_object_name="cos1",
						 type=class_type_EXP, operation=ATTRIB_ADD)], 
						 routing_instance_name="pe2")
	print api_request
	result = cos.RoutingInstanceBindPointAdd(api_request, api_timeout)
	print 'Invoking fw.RoutingInstanceBindPointAdd \nreturn = ', result

	pause()
	print "################################################################################################ RT GET ################"
	print "################################################################################################################################"
	api_request = CosRoutingInstanceBindPoint(routing_instance_name="pe1",)
	#print api_request
	result = cos.RoutingInstanceBindPointGet(api_request, api_timeout)
	print 'Invoking fw.RoutingInstanceBindPointGet \nreturn = ', result
	pause()
	print "################################################################################################ RT GET NEXT################"
	print "################################################################################################################################"
	api_request = CosRoutingInstanceBindPoint(routing_instance_name="pe1",)
	#print api_request
	result = cos.RoutingInstanceBindPointGetNext(api_request, api_timeout)
	print 'Invoking fw.RoutingInstanceBindPointGetNext \nreturn = ', result
	pause()
	print "################################################################################################ RT GET BULK ################"
	print "################################################################################################################################"
	api_request = CosRoutingInstanceBindPoint(routing_instance_name="pe1",)
	x = 1
	for stream in cos.RoutingInstanceBindPointBulkGet(api_request,10):
		i = x
		print 'Invoking cos.RoutingInstanceBindPointBulkGet( \nreturn = ', stream , str(i)	
		x += 1
	pause()
	
	
	print "################################################################################################ RT DEL  ################"
	print "################################################################################################################################"

	api_request = CosRoutingInstanceBindPoint(routing_instance_name="pe1")
	print api_request
	result = cos.RoutingInstanceBindPointDelete(api_request, api_timeout)
	print 'Invoking fw.RoutingInstanceBindPointDelete \nreturn = ', result

	pause()
	print "################################################################################################ RT DEL  ################"
	print "################################################################################################################################"

	api_request = CosRoutingInstanceBindPoint(routing_instance_name="pe2")
	print api_request
	result = cos.RoutingInstanceBindPointDelete(api_request, api_timeout)
	print 'Invoking fw.RoutingInstanceBindPointDelete \nreturn = ', result

	pause()
	
	

	print "################################################################################################ Classifier Delete cos ################"
	print "################################################################################################################################"



    	api_request = CosClassifier(classifier_name="cos", classifier_type=classifier_rewrite_type_EXP,)# rule=[ClassifierRule(code_points=[1], forwarding_class_name="be1")])
    	result = cos.ClassifierDelete(api_request, api_timeout)
	print 'Invoking cos.ClassifierDelete \nreturn = ', result 
	
	if result.status is EOK :
            print "ClassifierBulkGet RPC Passed"
    	else:
            print "ClassifierBulkGet RPC Failed"
	
	#pause()

	print "################################################################################################ Classifier Delete cos ################"
	print "################################################################################################################################"



    	api_request = CosClassifier(classifier_name="cos1", classifier_type=classifier_rewrite_type_EXP,)# rule=[ClassifierRule(code_points=[1], forwarding_class_name="be1")])
    	result = cos.ClassifierDelete(api_request, api_timeout)
	print 'Invoking cos.ClassifierDelete \nreturn = ', result 
	
	if result.status is EOK :
            print "ClassifierBulkGet RPC Passed"
    	else:
            print "ClassifierBulkGet RPC Failed"
	
	pause()

except AbortionError as e:
        	print "code is ", e.code
		print "details is ", e.details

except Exception as tx:
        print '%s' % (tx.message)
    

while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)
