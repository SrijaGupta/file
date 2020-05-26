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
        tname = [
            '1234567890123456789012345678901234567890123456789012345678901234',
            '!@!@!', 'f1', '0000000000', '-1', '""',
            '12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678',
            '',
            '12345678901234567890123456789012345678901234567890123456789012345']
        for termname in tname:
                matchMPLS1 = AclMatchMplsLabel(min=1, max=1048575, match_op=ACL_MATCH_OP_EQUAL)

                term1match1 = AclEntryMatchMpls(match_label1=[matchMPLS1])
                t = AclEntryMplsTerminatingAction(action_accept=1)
                nt = AclEntryMplsNonTerminatingAction(action_count=AclActionCounter(counter_name="Match1"))
                term1Action1 = AclEntryMplsAction(action_t=t, actions_nt=nt)

                adj = AclAdjacency(type=ACL_ADJACENCY_AFTER)
                term1 = AclMplsEntry(ace_name=termname, ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,actions=term1Action1)
                tlist1 = AclEntry(mpls_entry=term1)

                filter=AccessList(acl_name = "MPLS1",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_MPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
                print filter

                result = fw.AccessListAdd(filter,10)
                print 'Invoking fw.AccessListAdd \nreturn = ', result

                if result.status is ACL_STATUS_EOK:
                    print "AccessListAdd RPC Passed with term name : %s" % termname
                    res.append("AccessListAdd RPC Passed with term name : %s and returned %s" % (termname, result))
                else:
                    print "AccessListAdd RPC Failed with term name : %s" % termname
                    res.append("AccessListAdd RPC Failed with term name : %s and returned %s" % (termname, result))
                    flag += 1
        
                pause()
                bind=AccessListObjBind(acl=filter,obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.0'),bind_direction=ACL_BIND_DIRECTION_INPUT,bind_family=ACL_FAMILY_MPLS)
                print bind

                bindaddresult=fw.AccessListBindAdd(bind,10)
                print 'Invoking fw.AccessListBindAdd \nreturn = ', bindaddresult
                if bindaddresult.status is ACL_STATUS_EOK:
                    print "AccessListBindAdd RPC Passed with term name : %s" % termname
                    res.append("AccessListBindAdd RPC Passed with term name : %s and returned %s" % (termname, bindaddresult))
                else:
                    print "AccessListBindAdd RPC Failed with term name : %s" % termname
                    res.append("AccessListBindAdd RPC Failed with term name : %s and returned %s" % (termname, bindaddresult))
                    flag += 1

                pause()
                binddelresult = fw.AccessListBindDelete(bind,10)
                print 'Invoking fw.AccessListBindDelete \nreturn = ', binddelresult
                if binddelresult.status is ACL_STATUS_EOK:
                    print "AccessListBindDelete RPC Passed with term name : %s" % termname
                    res.append("AccessListBindDelete RPC Passed with term name : %s and returned %s" % (termname, binddelresult))
                else:
                    print "AccessListBindDelete RPC Failed with term name : %s" % termname
                    res.append("AccessListBindDelete RPC Failed with term name : %s and returned %s" % (termname, binddelresult))
                    flag += 1

                pause()
                filter = AccessList(acl_name="MPLS1",acl_family = ACL_FAMILY_MPLS)
                print filter
                acldelresult = fw.AccessListDelete(filter,10)
                print 'Invoking fw.AccessListDelete \nreturn = ', acldelresult
                if acldelresult.status is ACL_STATUS_EOK:
                    print "AccessListDelete RPC Passed with term name : %s" % termname
                    res.append("AccessListDelete RPC Passed with term name : %s and returned %s" % (termname, acldelresult))
                else:
                    print "AccessListDelete RPC Failed with term name : %s" % termname
                    res.append("AccessListDelete RPC Failed with term name : %s and returned %s" % (termname, acldelresult))
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
