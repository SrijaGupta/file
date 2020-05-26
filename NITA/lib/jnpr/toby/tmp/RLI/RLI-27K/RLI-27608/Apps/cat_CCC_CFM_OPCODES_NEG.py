import os
import sys
import logging
import time
import argparse
sys.path.append("/var/tmp")

#  Importing API libraries
from grpc.beta import implementations
import authentication_service_pb2
from authentication_service_pb2 import *
import jnx_addr_pb2
from jnx_addr_pb2 import *
import firewall_service_pb2
from firewall_service_pb2 import *
import authentication_service_pb2
from authentication_service_pb2 import *

timestr = time.strftime("%Y%m%d_%H%M%S")
start_time = time.time()
log_file_name = 'cat_' + 'CCC_CFM_OPCODES' + '_' + timestr + '.log'
log_file = os.path.join('/var/tmp', log_file_name)

    
# Logging
fmt_str = "%(asctime)s:%(levelname)s:%(message)s" # check for more in logging module
logging.basicConfig(filename=log_file, filemode='w+', level=logging.INFO, format=fmt_str,datefmt="%b-%d-%Y %H:%M:%S")
logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument('-d','--device', help='Input host name',required=True)
parser.add_argument('-ifl','--iflname', help='Input interface name',required=True)
args = parser.parse_args()

# APP Config
device = args.device  # DUT Name/IP here
APP_USER = 'regress'  # username
APP_PASSWORD = 'MaRtInI'  # Password
port = 9999  # GRPC port number
client_id = 'CCC_CFM_OPCODES'  # App Id (Will be replaced by test name)
login_timeout = 100  # Timeout for Logincheck API
api_timeout = 10  # Timeout for all the API calls
   

# Pass/Fail flags and counters
calls_count = 0
pass_count = 0
fail_count = 0
pass_flag = 0
api_pass_flag = 0
api_pass_count = 0
api_fail_count = 0

def pause():
    programPause = raw_input("Enter to continue...")
    
logger.info("Executing Python app")
pause()

def validate(result, api_name, api_request, count, category):
    """ Function to validate the api response """
    api_info = "--------------------------------------------\n\nExecuted API - {0}-({1})".format(api_name, count)
    logger.info("{0}".format(api_info))
    logger.info("\nREQUEST ===>\n{0}".format(api_request))
    if not hasattr(result, '__iter__'):
        response = str(result).replace('\\n', '\n')
        response = str(response).replace('\\"', '\"')
        logger.info("\nRESPONSE ===>\n{0}".format(response))
    global pass_count, fail_count, pass_flag, calls_count
    calls_count += 1
    log_str = "API - {0}-({1}) ".format(api_name, count)
    status = 0
    if category == 'negative':
        test_condition = 'result.status is not status'
    else:
        test_condition = 'result.status is status'
    if hasattr(result, '__iter__'):
        logger.info('\nRESPONSE (Streaming API) ===>\n')
        fail_flag = 0
        for i in result:
            if i :
                response = str(i).replace('\\n', '\n')
                response = str(response).replace('\\"', '\"')
                logger.info("\n{0}".format(response))
                if i.status is not status and category != 'negative':
                    fail_flag = 1
        if fail_flag is 0:
            pass_count += 1
            logger.info("\nRESULT ===>\n{0} -> PASS\n".format(log_str))
        else:
            fail_count += 1
            logger.info("\nRESULT ===>\n{0} -> FAIL\n".format(log_str))
            pass_flag = 1

    else:
        if eval(test_condition):
            pass_count += 1
            logger.info("\nRESULT ===>\n{0} -> PASS\n".format(log_str))
        else:
            fail_count += 1
            logger.info("\nRESULT ===>\n{0} -> FAIL\n".format(log_str))
            pass_flag = 1

    
try:

    # Channel Creation and Authentication
    channel = implementations.insecure_channel(host=device, port=port)
    stub = authentication_service_pb2.beta_create_Login_stub(channel)
    login_response = stub.LoginCheck(authentication_service_pb2.LoginRequest(user_name=APP_USER, password=APP_PASSWORD, client_id=client_id), login_timeout)

    # Service stub creation
    AclService_stub = beta_create_AclService_stub(channel)

    # All the negative combinations

    logger.info('All the negative combinations')


    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 1, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 1, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 1, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=1, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 1, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 2, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 2, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 2, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=1, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 2, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 3, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 3, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 3, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 3, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 4, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 4, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 4, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 4, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 5, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 5, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 5, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 5, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 6, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 6, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 6, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 6, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 7, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 7, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 7, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 7, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 8, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 8, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 8, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 8, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=254, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 9, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 9, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 9, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 9, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 10, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 10, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 10, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 10, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 11, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 11, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 11, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 11, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 12, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 12, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 12, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 12, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 13, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 13, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 13, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 13, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListAdd', api_request, 14, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 14, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 14, 'negative')


    pause() 
    api_request = AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1)
    print api_request 
    result = AclService_stub.AccessListDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListDelete', api_request, 14, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 15, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 15, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 15, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_accept=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 15, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 16, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=254, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 16, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 16, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=254, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 16, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 17, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 17, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 17, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 17, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 18, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 18, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 18, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 18, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 19, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname + ".0"), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 19, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 19, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=254, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 19, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 20, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=254, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 20, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 20, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=254, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 20, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 21, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 21, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 21, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 21, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 22, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=0, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 22, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 22, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=0)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 22, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 23, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=254)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 23, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=1, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindAdd(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindAdd', api_request, 23, 'negative')


    pause() 
    api_request = AccessListObjBind(bind_direction=1, bind_family=6, obj_type=1, bind_object=AccessListBindObjPoint(intf=args.iflname), acl=AccessList(ace_list=[AclEntry(ccc_entry=AclCccEntry(matches=AclEntryMatchCcc(cfm_opcodes=[AclMatchCfmOpcode(max=256, match_op=2, min=255)]), ace_name="t1", adjacency=AclAdjacency(type=1), actions=AclEntryCccAction(actions_nt=AclEntryCccNonTerminatingAction(action_syslog=1, action_sample=1, action_count=AclActionCounter(counter_name="C1"), action_log=1), action_t=AclEntryCccTerminatingAction(action_discard=1)), ace_op=1))], acl_family=6, acl_flag=0, acl_name="CCC1", acl_type=1))
    print api_request 
    result = AclService_stub.AccessListBindDelete(api_request, api_timeout)
    print result 
    validate(result, 'AccessListBindDelete', api_request, 23, 'negative')
    pause()

    logger.info("--------------------------------------------\nAPI TEST SUMMARY : \n")
    logger.info("TOTAL NUMBER OF TESTCASES EXECUTED :  {0}\n".format(calls_count))
    logger.info("TOTAL NUMBER OF TESTCASES PASSED   :  {0}\n".format(pass_count))
    logger.info("TOTAL NUMBER OF TESTCASES FAILED   :  {0}\n".format(fail_count))

    if pass_flag is 0:
        logger.info("API TESTING ------PASS\n")
    else:
        logger.info("API TESTING ------FAIL\n")
    duration = time.time() - start_time
    logger.info("Exeution Duration(in seconds) = {}".format(duration))

    logger.info("\nAPI TESTING COMPLETED\n")
    
except Exception as tx:
    logger.info("Caught Exception {0}\nPlease check the API calls".format(tx))
    pass
while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)

