import os
import sys
import time

import authentication_service_pb2
import firewall_service_pb2
import jnx_addr_pb2
from authentication_service_pb2 import *
from firewall_service_pb2 import *
from grpc.beta import implementations
from jnx_addr_pb2 import *

HOST = args.device

# device1 = "10.220.13.147"
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

    #ifl = AclMatchIflNameIndex(ifl_index = 9999990)
    ifl = AclMatchIflNameIndex(ifl_name = "ge-0/3/2.0")

    term1match1 = AclEntryMatchInet6(ifl_names=[ifl])
    t = AclEntryInet6TerminatingAction(action_accept=1)
    nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="Match1"))
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
    bo = AccessListBindObjPoint(intf='ge-0/3/2.0')
    bind = AccessListObjBind(acl=filter, obj_type=ACL_BIND_OBJ_TYPE_INTERFACE, bind_object=bo,
                             bind_direction=ACL_BIND_DIRECTION_INPUT, bind_family=ACL_FAMILY_INET6)

    raw_input("enter to continue to call AccessListBindAdd RPC")
    bindaddresult = fw.AccessListBindAdd(bind, 10)

    print bind

    print 'Invoking fw.AccessListBindAdd \nreturn = ', bindaddresult

    if bindaddresult.status is ACL_STATUS_EOK:
        print "AccessListObjBind RPC Passed"
        res.append("AccessListObjBind RPC Passed")
    else:
        print "AccessListObjBind RPC Failed"
        res.append("AccessListObjBind RPC Failed")

    raw_input("enter to continue to call AccessListBindDelete RPC")
    binddelresult = fw.AccessListBindDelete(bind, 10)

    print 'Invoking fw.AccessListBindDelete \nreturn = ', binddelresult

    if binddelresult.status is ACL_STATUS_EOK:
        print "AccessListBindDelete RPC Passed"
        res.append("AccessListBindDelete RPC Passed")
    else:
        print "AccessListBindDelete RPC Failed"
        res.append("AccessListBindDelete RPC Failed")

    raw_input("enter to continue to call AccessListDelete RPC")
    filter = AccessList(acl_name='f1', acl_family=ACL_FAMILY_INET6)
    print filter
    acldelresult = fw.AccessListDelete(filter,10)

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


except Exception as tx:
    print '%s' % (tx.message)
while True:
    import signal

    os.kill(os.getpid(), signal.SIGTERM)
