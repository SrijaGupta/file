import os
import sys
import time
#import argparse

import authentication_service_pb2
import firewall_service_pb2
import jnx_addr_pb2
from authentication_service_pb2 import *
from firewall_service_pb2 import *
from grpc.beta import implementations
from jnx_addr_pb2 import *
from grpc.framework.interfaces.face.face import *

#timestr = time.strftime("%Y%m%d_%H%M%S")
#start_time = time.time()
#parser = argparse.ArgumentParser()
#parser.add_argument('-d','--device', help='Input host name',required=True)
#parser.add_argument('-ifl','--iflname', help='Input interface name',required=True)
#args = parser.parse_args()

HOST = args.device
# device1 = "10.220.113.147"
USER = 'regress'
PASSWORD = 'MaRtInI'
GRPC_PORT = 9999
CLIENT_ID = '101'
TIMEOUT = 5

channel = implementations.insecure_channel(host=HOST, port=GRPC_PORT)
stub = authentication_service_pb2.beta_create_Login_stub(channel)
login_response = stub.LoginCheck(
    authentication_service_pb2.LoginRequest(user_name=USER, password=PASSWORD, client_id=CLIENT_ID), TIMEOUT)
fw = firewall_service_pb2.beta_create_AclService_stub(channel)

try:
    res = []
    # address = ['abc','2001::1','10.1.1.2','10.1.1:2','256.1.1.1']



    pp1 = AclPolicerTwoColor(bw_unit = ACL_POLICER_RATE_BPS, bandwidth = 8000, burst_unit = ACL_POLICER_BURST_SIZE_BYTE, burst_size = 1500,
                             lp = ACL_LOSS_PRIORITY_MEDIUM_LOW, fc_string = "FWC", discard=True)
    pp = AclPolicerParameter(two_color_parameter = pp1)
    polc1 = AccessListPolicer(policer_name='p1', policer_type=ACL_TWO_COLOR_POLICER, policer_flag=ACL_POLICER_FLAG_TERM_SPECIFIC, policer_params=pp)

    raw_input("enter to continue to call AccessListPolicerAdd RPC")
    result = fw.AccessListPolicerAdd(polc1, 10)
    print 'Invoking fw.AccessListAdd \nreturn = ', result

    print polc1

    if result.status is ACL_STATUS_EOK:
        print "AccessListPolicerAdd RPC Passed"
    else:
        print "AccessListPolicerAdd RPC Failed"



    IP2 = IpAddress(addr_string='10::2')

    matchIP2 = AclMatchIpAddress(addr=IP2, prefix_len=128, match_op=ACL_MATCH_OP_EQUAL)

    term1match1 = AclEntryMatchInet6(match_addrs=[matchIP2])
    t = AclEntryInet6TerminatingAction(action_accept=1)

    polc = AclActionPolicer(policer=polc1)
    #nt = AclEntryInet6NonTerminatingAction(action_log=1)
    nt = AclEntryInet6NonTerminatingAction(action_policer=polc)
    term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

    adj = AclAdjacency(type=ACL_ADJACENCY_AFTER)
    term1 = AclInet6Entry(ace_name="t1", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,
                         actions=term1Action1)
    tlist1 = AclEntry(inet6_entry=term1)

    filter = AccessList(acl_name='f1', acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_INET6,
                        acl_flag=ACL_FLAGS_NONE, ace_list=[tlist1])

    raw_input("enter to continue to call AccessListAdd RPC")
    result = fw.AccessListAdd(filter, 10)
    print 'Invoking fw.AccessListAdd \nreturn = ', result

    print filter

    if result.status is ACL_STATUS_EOK:
        print "AccessListAdd RPC Passed"
    else:
        print "AccessListAdd RPC Failed"

    # time.sleep(120)
#    bind = AccessListObjBind(acl=filter, obj_type=ACL_BIND_OBJ_TYPE_INTERFACE, bind_object='ge-1/0/1.0',
#                             bind_direction=ACL_BIND_DIRECTION_OUTPUT, bind_family=ACL_FAMILY_INET6)
#    print bind
#
#    raw_input("enter to continue to call AccessListBindAdd RPC")
#    bindaddresult = fw.AccessListBindAdd(bind, 10)
#
#    print 'Invoking fw.AccessListBindAdd \nreturn = ', bindaddresult
#
#    if bindaddresult.status is ACL_STATUS_EOK:
#        print "AccessListObjBind RPC Passed"
#        res.append("AccessListObjBind RPC Passed")
#    else:
#        print "AccessListObjBind RPC Failed"
#        res.append("AccessListObjBind RPC Failed")
#
#    raw_input("enter to continue to call AccessListBindDelete RPC")
#    binddelresult = fw.AccessListBindDelete(bind, 10)
#
#    print 'Invoking fw.AccessListBindDelete \nreturn = ', binddelresult
#
#    if binddelresult.status is ACL_STATUS_EOK:
#        print "AccessListBindDelete RPC Passed"
#        res.append("AccessListBindDelete RPC Passed")
#    else:
#        print "AccessListBindDelete RPC Failed"
#        res.append("AccessListBindDelete RPC Failed")

    raw_input("enter to continue to call AccessListDelete RPC")
    filter = AccessList(acl_name='f1', acl_family=ACL_FAMILY_INET6)
    print filter
    acldelresult = fw.AccessListDelete(filter, 10)

    print 'Invoking fw.AccessListDelete \nreturn = ', acldelresult

    if acldelresult.status is ACL_STATUS_EOK:
        print "AccessListDelete RPC Passed"
        res.append("AccessListDelete RPC Passed")
        print "Test passed"
    else:
        print "AccessListDelete RPC Failed"
        res.append("AccessListDelete RPC Failed")
        print "Test failed"

    raw_input("enter to continue")

except AbortionError as e:
                print "code is ", e.code
                print "details is ", e.details

except Exception as tx:
    print '%s' % (tx.message)
while True:
    import signal

    os.kill(os.getpid(), signal.SIGTERM)
