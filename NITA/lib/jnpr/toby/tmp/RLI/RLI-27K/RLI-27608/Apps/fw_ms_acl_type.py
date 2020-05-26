import sys,time,os,argparse
from grpc.beta import implementations
import firewall_service_pb2,jnx_addr_pb2,authentication_service_pb2
from firewall_service_pb2 import *
from jnx_addr_pb2 import *
from authentication_service_pb2 import *
from grpc.framework.interfaces.face.face import *

parser = argparse.ArgumentParser()
parser.add_argument('-d','--device', help='Input host name',required=True)
parser.add_argument('-ifl','--iflname', help='Input interface name',required=True)
args = parser.parse_args()

device1 = args.device
APP_USER = 'regress'
APP_PASSWORD = 'MaRtInI'
port = 9999
client_id = '101'

def pause():
    programPause = raw_input("Enter to continue...")

print "Executing Python app"
pause()

try:
        channel = implementations.insecure_channel(host=device1, port=port)
        stub = authentication_service_pb2.beta_create_Login_stub(channel)
        login_response = stub.LoginCheck(
                authentication_service_pb2.LoginRequest(user_name=APP_USER, password=APP_PASSWORD,
                                                        client_id=client_id), 100)
        if (login_response.result == 1):
                print "Login to ", device1, "successful"
        else:
                print "Login to ", device1, "failed"
                raise SystemExit()
        fw = firewall_service_pb2.beta_create_AclService_stub(channel)
        flag = 0
        res=[]

        IP1 = IpAddress(addr_string='10.1.1.2')
        matchIP1 = AclMatchIpAddress(addr=IP1, prefix_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchMultiService(match_addrs=[matchIP1])
        t = AclEntryMultiServiceTerminatingAction(action_accept=1)
        nt = AclEntryMultiServiceNonTerminatingAction(action_count=AclActionCounter(counter_name="Match1"),action_syslog=1, action_log=1, action_sample=1)
        term1Action1 = AclEntryMultiServiceAction(action_t=t, actions_nt=nt)

        adj = AclAdjacency(type=ACL_ADJACENCY_AFTER)
        term1 = AclMultiServiceEntry(ace_name="t1", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,actions=term1Action1)
        tlist1 = AclEntry(mservice_entry=term1)

        filter=AccessList(acl_name = "MS1",acl_type = ACL_TYPE_INVALID, acl_family = ACL_FAMILY_MULTISERVICE, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListAdd(filter,10)
        print 'Invoking fw.AccessListAdd \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListAdd RPC Failed as expected"
                res.append("AccessListAdd RPC Failed as expected and returned %s" % (result))
                flag += 1
        else:
                print "AccessListAdd RPC Passed"
                res.append("AccessListAdd RPC Passed and returned %s" % (result))

        pause()

        filter = AccessList(acl_name="MS1", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_MULTISERVICE,acl_flag=ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListAdd(filter, 10)
        print 'Invoking fw.AccessListAdd \nreturn = ', result
        if result.status is ACL_STATUS_EOK:
            print "AccessListAdd RPC Passed"
            res.append("AccessListAdd RPC Passed and returned %s" % (result))

        else:
            print "AccessListAdd RPC Failed"
            res.append("AccessListAdd RPC Failed and returned %s" % (result))
            flag += 1

        pause()

        bind = AccessListObjBind(acl=filter, obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.0'),bind_direction=ACL_BIND_DIRECTION_INPUT, bind_family=ACL_FAMILY_MULTISERVICE)
        print bind

        bindaddresult = fw.AccessListBindAdd(bind, 10)
        print 'Invoking fw.AccessListBindAdd \nreturn = ', bindaddresult
        if bindaddresult.status is ACL_STATUS_EOK:
                print "AccessListBindAdd RPC Passed"
                res.append("AccessListBindAdd RPC Passed and returned %s" % (bindaddresult))
        else:
                print "AccessListBindAdd RPC Failed"
                res.append("AccessListBindAdd RPC Failed and returned %s" % (bindaddresult))
                flag += 1

        pause()
        binddelresult = fw.AccessListBindDelete(bind, 10)
        print 'Invoking fw.AccessListBindDelete \nreturn = ', binddelresult
        if binddelresult.status is ACL_STATUS_EOK:
                print "AccessListBindDelete RPC Passed"
                res.append("AccessListBindDelete RPC Passed and returned %s" % (binddelresult))
        else:
                print "AccessListBindDelete RPC Failed"
                res.append("AccessListBindDelete RPC Failed and returned %s" % (binddelresult))
                flag += 1

        pause()
        filter = AccessList(acl_name="MS1",acl_family = ACL_FAMILY_MULTISERVICE)
        print filter
        acldelresult = fw.AccessListDelete(filter,10)
        print 'Invoking fw.AccessListDelete \nreturn = ', acldelresult
        if acldelresult.status is ACL_STATUS_EOK :
                print "AccessListDelete RPC Passed"
                res.append("AccessListDelete RPC Passed and returned %s" % (acldelresult))
        else:
                print "AccessListDelete RPC Failed"
                res.append("AccessListDelete RPC Failed and returned %s" % (acldelresult))
                flag += 1
        
        pause()
        print "FINAL RESULT : \n"
        for i in res:
            print i

        if flag > 0:
            print "TEST FAILED"
        else:
            print "TEST PASSED"

except AbortionError as e:
    print "code is ", e.code
    print "details is ", e.details

while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)
