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
parser.add_argument('-ifl','--iflname', help='Input interface name',required=True)
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
	

	print "################################################################################################ Classifier ADD COS1 DSCP ################"
	print "################################################################################################################################"
 	api_request = CosClassifier(classifier_name	="cos", 
				    classifier_type	=classifier_rewrite_type_EXP,
				    sharable		=True, ######### FALSE
				    rule		=[ClassifierRule(operation = operation_ADD ,
									forwarding_class_name="be1", ## STRING
					   				loss_priority=loss_priority_MEDIUM_HIGH,
					   				code_points=[7])])
				    ####ref_objects=[CosObjRefInfo(referencing_obj_count=1, referencing_obj_type="ss", referencing_obj_name="co")], status=EOK)
        print api_request
	result = cos.ClassifierAdd(api_request, api_timeout)
	print 'Invoking fw.ClassifierAdd \nreturn = ', result
	
	if result.status is EOK :
            print "ClassifierAdd RPC Passed"
    	else:
            print "ClassifierAdd RPC Failed"
	
	pause()

	print "################################################################################################ Classifier ADD COS DSCP ################"
	print "################################################################################################################################"
 	api_request = CosClassifier(classifier_name	="cos1", 
				    classifier_type	=classifier_rewrite_type_EXP,
				    sharable		=True, ######### FALSE
				    rule		=[ClassifierRule(operation = operation_ADD ,
									forwarding_class_name="be1", ## STRING
					   				loss_priority=loss_priority_MEDIUM_LOW,
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

	#######################  CosNodeType  ###########################################
	CosNodeType_INTERFACE_INVALID 	= NODE_TYPE_INVALID 
	CosNodeType_LOGICAL_INTERFACE   = NODE_TYPE_LOGICAL_INTERFACE
	CosNodeType_INTERFACE_SET 	= NODE_TYPE_INTERFACE_SET
	CosNodeType_INTERFACE 		= NODE_TYPE_INTERFACE

	############################ CosNodedirection ###############################
	
    	direction_DIRECTION_INVALID  =	DIRECTION_INVALID
    	direction_INGRESS 	     =  INGRESS
    	direction_EGRESS	     =  EGRESS
	
	############################ ClassifierFamily  ###############################
	
	classifier_family_INVALID		 =  NODE_FEATURE_CLFR_PROTO_INVALID
	classifier_family_DSCP			 =  NODE_FEATURE_CLFR_DSCP
	classifier_family_DSCP_MPLS 		 =  NODE_FEATURE_CLFR_DSCP_MPLS
	classifier_family_DSCP_IPV6 		 =  NODE_FEATURE_CLFR_DSCP_IPV6
	classifier_family_DSCP_IPV6_MPLS	 =  NODE_FEATURE_CLFR_DSCP_IPV6_MPLS
	classifier_family_EXP			 =  NODE_FEATURE_CLFR_EXP
	classifier_family_INET 			 =  NODE_FEATURE_CLFR_INET_PRECEDENCE
	classifier_family_IEEE8021P 	         =  NODE_FEATURE_CLFR_IEEE8021P 
	classifier_family_IEEE8021P_INNER 	 =  NODE_FEATURE_CLFR_IEEE8021P_TAG_MODE_INNER
	classifier_family_IEEE8021P_TRANSPARENT  =  NODE_FEATURE_CLFR_IEEE8021P_TAG_MODE_TRANSPARENT
	classifier_family_IEEE8021AD  		 =  NODE_FEATURE_CLFR_IEEE8021AD
	classifier_family_IEEE8021AD_INNER 	 =  NODE_FEATURE_CLFR_IEEE8021_AD_TAG_MODE_INNER
	classifier_family_IEEE8021AD_DEFAULT	 =  NODE_FEATURE_CLFR_NO_DEFAULT 
	
	############################ rewriteFamily  ###############################
	
	rewrite_family_INVALID		 	=  NODE_FEATURE_RW_PROTO_INVALID
	rewrite_family_DSCP			 		=  NODE_FEATURE_RW_DSCP
	rewrite_family_DSCP_MPLS 		=  NODE_FEATURE_RW_DSCP_MPLS
	rewrite_family_DSCP_IPV6 		=  NODE_FEATURE_RW_DSCP_IPV6
	rewrite_family_DSCP_IPV6_MPLS		=  NODE_FEATURE_RW_DSCP_IPV6_MPLS
	rewrite_family_EXP			=  NODE_FEATURE_RW_EXP
	rewrite_family_EXP_MPLS_INET_BOTH	=  NODE_FEATURE_RW_EXP
	rewrite_family_MPLS_INET_BOTH_NON_VPN	=  NODE_FEATURE_RW_EXP
	rewrite_family_INET 			=  NODE_FEATURE_RW_INET_PRECEDENCE
	rewrite_family_INET_MPLS	        =  NODE_FEATURE_RW_INET_PREC_MPLS 
	rewrite_family_IEEE8021P	    	=  NODE_FEATURE_RW_IEEE8021P
	rewrite_family_IEEE8021P_INNER_OUTER	=  NODE_FEATURE_RW_IEEE8021_TAG_MODE_OUTER_AND_INNER
	rewrite_family_IEEE8021AD  		 =  NODE_FEATURE_RW_IEEE8021AD
	rewrite_family_IEEE8021AD_INNER_OUTER 	 =  NODE_FEATURE_RW_IEEE8021AD_TAG_MODE_OUTER_AND_INNER

	############################### CosNodeFeatureFamilyType ####################
	feature_type_INVALID 			=	NODE_FEATURE_FAMILY_INVALID 
   	feature_type_classifier_rule 		=	NODE_FEATURE_FAMILY_CLFR_RULE 
   	feature_type_rewrite_rule 		=	NODE_FEATURE_FAMILY_RW_RULE 
	############################## NodeFeatures #################################
	feature_type_INVALID     		=  NODE_FEATURE_INVALID 
    	feature_type_SMAP     			=  NODE_FEATURE_SMAP
    	feature_type_SRATE	     		=  NODE_FEATURE_SRATE ####// not valid for interface sets
    	feature_type_TCP	    		=  NODE_FEATURE_TCP
    	feature_type_TCP_REMAINING		=  NODE_FEATURE_TCP_REMAINING
    	feature_type_FORWARDING_CLASS	    	=  NODE_FEATURE_FORWARDING_CLASS ########### // not valid for interface sets
    	feature_type_SCHED	    		=  NODE_FEATURE_MEMBER_LINK_SCHED 
    	feature_type_SHARE			=  NODE_FEATURE_EXCESS_BW_SHARE
	print "################################################################################################ Classifier NODE with only node_family_features################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".0",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname, 
					 
					 
					 node_family_features=[CosNodeFamilyFeature(feature_option=CosNodeFeatureOption( classifier_family = classifier_family_EXP ),
										    operation = operation_ADD,
										    direction=direction_INGRESS,
										    feature_object_name = "cos1",
					 					    feature_type=feature_type_classifier_rule)],)
					#node_features=[CosNodeFeature(direction=direction_INGRESS,
					#				 operation=operation_ADD,
					#				 feature_type=NODE_FEATURE_FORWARDING_CLASS,
					#			         feature_val=CosNodeFeatureVal(object_name="be1"))])
										  					 								     
	print api_request
	result = cos.NodeFeaturesAdd(api_request, api_timeout)
	print 'Invoking cos.NodeFeaturesAdd \nreturn = ', result 
	
	if result.status is EOK :
            print "NodeFeaturesAdd RPC Passed"
    	else:
            print "NodeFeaturesAdd RPC Failed"
	pause()
	print "################################################################################################ Classifier NODE change with only node_family_features################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".0",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname, 
					 
					 
					 node_family_features=[CosNodeFamilyFeature(feature_option=CosNodeFeatureOption( classifier_family = classifier_family_EXP ),
										    operation = operation_ADD,
										    direction=direction_INGRESS,
										    feature_object_name = "cos",
					 					    feature_type=feature_type_classifier_rule)],)
					
										  					 								     
	print api_request
	result = cos.NodeFeaturesChange(api_request, api_timeout)
	print 'Invoking cos.NodeFeaturesChange \nreturn = ', result 
	
	if result.status is EOK :
            print "NodeFeaturesChange RPC Passed"
    	else:
            print "NodeFeaturesChange RPC Failed"
	pause()
	print "################################################################################################ Classifier NODE  cos1 with only node_family_features################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".1",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname, 
					 
					 
					 node_family_features=[CosNodeFamilyFeature(feature_option=CosNodeFeatureOption( classifier_family = classifier_family_EXP ),
										    operation = operation_ADD,
										    direction=direction_INGRESS,
										    feature_object_name = "cos1",
					 					    feature_type=feature_type_classifier_rule)],)
										  					 								     
	print api_request
	result = cos.NodeFeaturesAdd(api_request, api_timeout)
	print 'Invoking cos.NodeFeaturesAdd \nreturn = ', result 
	
	if result.status is EOK :
            print "NodeFeaturesAdd RPC Passed"
    	else:
            print "NodeFeaturesAdd RPC Failed"
	pause()

	
	print "################################################################################################ Node Get ################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".0",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname,	)
	 #node_family_features=[CosNodeFamilyFeature(feature_option=CosNodeFeatureOption( classifier_family = classifier_family_INET ),
#										    operation = operation_ADD,
#										    direction=direction_INGRESS,
#										    feature_object_name = "cos",
#					 					    feature_type=feature_type_classifier_rule)],)				
					 					  					 								  
	result = cos.NodeFeaturesGet(api_request, api_timeout)
	print 'Invoking cos.NodeFeaturesGet \nreturn = ', result 
	
	if result.status is EOK :
            print "NodeFeaturesGet RPC Passed"
    	else:
            print "NodeFeaturesGet RPC Failed"
	pause()


	print "################################################################################################ node Get NEXT ################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".0",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname,)

					
					 					  					 								     
	print api_request
	result = cos.NodeFeaturesGetNext(api_request, api_timeout)
	print 'Invoking cos.NodeFeaturesGetNext \nreturn = ', result 
	
	if result.status is EOK :
            print "NodeFeaturesGetNext RPC Passed"
    	else:
            print "NodeFeaturesGetNext RPC Failed"
	pause()
		
	print "################################################################################################ node Bulk GET ################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".0",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname,)


	x = 1
	
	for stream in cos.NodeFeaturesBulkGet(api_request,10):
		i = x
		print 'Invoking cos.NodeFeaturesBulkGet \nreturn = ', stream , str(i)	
		x += 1
	pause()
	print "################################################################################################ Classifier NODE with Del ################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".0",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname,)
					 
					 
					
					 					  					 								     
	print api_request
	result = cos.NodeFeaturesDelete(api_request, api_timeout)
	print 'Invoking cos.NodeFeaturesDelete \nreturn = ', result 
	
	if result.status is EOK :
            print "NodeFeaturesDelete RPC Passed"
    	else:
            print "NodeFeaturesDelete RPC Failed"
	pause()
	


	print "################################################################################################ Classifier NODE with Del ################"
	print "################################################################################################################################"
	api_request = CosNodeBindFeatures(node_type=CosNodeType_LOGICAL_INTERFACE ,
					 node_name=args.iflname + ".1",
					 node_parent_type=CosNodeType_INTERFACE,
					 node_parent_name=args.iflname,)
					 
					 
					
					 					  					 								     
	print api_request
	result = cos.NodeFeaturesDelete(api_request, api_timeout)
	print 'Invoking cos.NodeFeaturesDelete \nreturn = ', result 
	
	if result.status is EOK :
            print "NodeFeaturesDelete RPC Passed"
    	else:
            print "NodeFeaturesDelete RPC Failed"
	pause()
	


	
	print "################################################################################################ Classifier Delete COS ################"
	print "################################################################################################################################"



    	api_request = CosClassifier(classifier_name="cos", classifier_type=classifier_rewrite_type_EXP,)# rule=[ClassifierRule(code_points=[1], forwarding_class_name="be1")])
    	result = cos.ClassifierDelete(api_request, api_timeout)
	print 'Invoking cos.ClassifierDelete \nreturn = ', result 
	
	if result.status is EOK :
            print "ClassifierBulkGet RPC Passed"
    	else:
            print "ClassifierBulkGet RPC Failed"
	
	#pause()
	
	print "################################################################################################ Classifier Delete COS1 ################"
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


		
