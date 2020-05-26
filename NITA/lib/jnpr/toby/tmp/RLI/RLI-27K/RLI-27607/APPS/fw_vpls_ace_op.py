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
            authentication_service_pb2.LoginRequest(user_name=APP_USER, password=APP_PASSWORD, client_id=client_id), 100)
        if (login_response.result == 1):
            print "Login to ", device1, "successful"
        else:
            print "Login to ", device1, "failed"
            raise SystemExit()
        fw = firewall_service_pb2.beta_create_AclService_stub(channel)
        res=[]
        MAC1 = MacAddress(addr_string='aa:00:00:00:00:11')
        MAC2 = MacAddress(addr_string='bb:00:00:00:00:11')
        matchMAC1 = AclMatchMacAddress(addr=MAC1, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)
        matchMAC2 = AclMatchMacAddress(addr=MAC2, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchMAC1], match_src_macs=[matchMAC2])
        t = AclEntryVplsTerminatingAction(action_accept=1)
        nt=AclEntryVplsNonTerminatingAction(action_count = AclActionCounter(counter_name="C1"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER)
        term1=AclVplsEntry(ace_name="t1",ace_op=ACL_ENTRY_OPERATION_INVALID,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(vpls_entry=term1)

        filter=AccessList(acl_name = "VPLS1", acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListAdd(filter,10)
        print 'Invoking fw.AccessListAdd \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListAdd RPC Passed with ace operation : ACL_ENTRY_OPERATION_INVALID"
                res.append("AccessListAdd RPC Passed with ace operation : ACL_ENTRY_OPERATION_INVALID and returned %s" % (result))
        else:
                print "AccessListAdd RPC Failed with ace operation : ACL_ENTRY_OPERATION_INVALID as expected"
                res.append("AccessListAdd RPC Failed with ace operation : ACL_ENTRY_OPERATION_INVALID as expected and returned %s" % (result))
        pause()

        MAC1 = MacAddress(addr_string='aa:00:00:00:00:11')
        MAC2 = MacAddress(addr_string='bb:00:00:00:00:11')
        matchMAC1 = AclMatchMacAddress(addr=MAC1, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)
        matchMAC2 = AclMatchMacAddress(addr=MAC2, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchMAC1], match_src_macs=[matchMAC2])
        t = AclEntryVplsTerminatingAction(action_accept=1)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C1"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj = AclAdjacency(type=ACL_ADJACENCY_AFTER)
        term1 = AclVplsEntry(ace_name="t1", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,actions=term1Action1)
        tlist1 = AclEntry(vpls_entry=term1)

        filter = AccessList(acl_name="VPLS1", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_VPLS,acl_flag=ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListAdd(filter,10)
        print 'Invoking fw.AccessListAdd \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListAdd RPC Passed with ace operation : ACL_ENTRY_OPERATION_ADD"
                res.append("AccessListAdd RPC Passed with ace operation : ACL_ENTRY_OPERATION_ADD and returned %s" % (result))
        else:
                print "AccessListAdd RPC Failed with ace operation : ACL_ENTRY_OPERATION_ADD"
                res.append("AccessListAdd RPC Failed with ace operation : ACL_ENTRY_OPERATION_ADD and returned %s" % (result))
        pause()

        MAC1 = MacAddress(addr_string='aa:11:00:00:00:11')
        MAC2 = MacAddress(addr_string='bb:11:00:00:00:11')
        matchMAC1 = AclMatchMacAddress(addr=MAC1, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)
        matchMAC2 = AclMatchMacAddress(addr=MAC2, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchMAC1], match_src_macs=[matchMAC2])
        t = AclEntryVplsTerminatingAction(action_accept=1)
        nt=AclEntryVplsNonTerminatingAction(action_count = AclActionCounter(counter_name="Match1"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER)
        term1=AclVplsEntry(ace_name="t2",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(vpls_entry=term1)

        filter=AccessList(acl_name = "VPLS1", acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListChange(filter,10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListChange RPC Passed with ace operation : ACL_ENTRY_OPERATION_ADD"
                res.append("AccessListChange RPC Passed with ace operation : ACL_ENTRY_OPERATION_ADD and returned %s" % (result))
        else:
                print "AccessListChange RPC Failed with ace operation : ACL_ENTRY_OPERATION_ADD"
                res.append("AccessListChange RPC Failed with ace operation : ACL_ENTRY_OPERATION_ADD and returned %s" % (result))
        pause()

        MAC1 = MacAddress(addr_string='aa:22:00:00:00:11')
        MAC2 = MacAddress(addr_string='bb:22:00:00:00:11')
        matchMAC1 = AclMatchMacAddress(addr=MAC1, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)
        matchMAC2 = AclMatchMacAddress(addr=MAC2, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchMAC1], match_src_macs=[matchMAC2])
        t = AclEntryVplsTerminatingAction(action_accept=1)
        nt=AclEntryVplsNonTerminatingAction(action_count = AclActionCounter(counter_name="C2"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER)
        term2=AclVplsEntry(ace_name="t2",ace_op=ACL_ENTRY_OPERATION_REPLACE,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist2=AclEntry(vpls_entry=term2)

        filter=AccessList(acl_name = "VPLS1",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist2])
        print filter

        result = fw.AccessListChange(filter,10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListChange RPC Passed with ace operation : ACL_ENTRY_OPERATION_REPLACE"
                res.append("AccessListChange RPC Passed with ace operation : ACL_ENTRY_OPERATION_REPLACE and returned %s" % (result))
        else:
                print "AccessListChange RPC Failed with ace operation : ACL_ENTRY_OPERATION_REPLACE"
                res.append("AccessListChange RPC Failed with ace operation : ACL_ENTRY_OPERATION_REPLACE and returned %s" % (result))
        pause()

        bind=AccessListObjBind(acl=filter,obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.0'),bind_direction=ACL_BIND_DIRECTION_INPUT,bind_family=ACL_FAMILY_VPLS)
        bindresult=fw.AccessListBindAdd(bind,10)
        print 'Invoking fw.AccessListBindAdd \nreturn = ', bindresult
        if bindresult.status is ACL_STATUS_EOK:
            print "AccessListBindAdd RPC Passed"
            res.append("AccessListBindAdd RPC Passed and returned %s" % (bindresult))
        else:
            print "AccessListBindAdd RPC Failed"
            res.append("AccessListBindAdd RPC Failed and returned %s" % (bindresult))
        pause()

        for i in range(1,3):
            term1=AclVplsEntry(ace_name="t"+str(i),ace_op=ACL_ENTRY_OPERATION_DELETE,adjacency=adj,matches=term1match1,actions=term1Action1)
            tlist1=AclEntry(vpls_entry=term1)

            filter=AccessList(acl_name = "VPLS1", acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
            print filter

            result = fw.AccessListChange(filter,10)
            print 'Invoking fw.AccessListChange \nreturn = ', result
            if result.status is ACL_STATUS_EOK :
                    print "AccessListChange RPC Passed with ace operation : ACL_ENTRY_OPERATION_DELETE with term" + "t"+str(i)
                    res.append("AccessListChange RPC Passed with ace operation : ACL_ENTRY_OPERATION_DELETE with term" + "t"+str(i) +" and returned %s" % (result))
            else:
                    print "AccessListChange RPC Failed with ace operation : ACL_ENTRY_OPERATION_DELETE with term" + "t"+str(i)
                    res.append("AccessListChange RPC Failed with ace operation : ACL_ENTRY_OPERATION_DELETE with term" + "t"+str(i) +" and returned %s" % (result))
            pause()

        binddelresult = fw.AccessListBindDelete(bind, 10)
        print 'Invoking fw.AccessListBindDelete \nreturn = ', binddelresult
        if binddelresult.status is ACL_STATUS_EOK:
            print "AccessListBindDelete RPC Passed"
            res.append("AccessListBindDelete RPC Passed and returned %s" % (binddelresult))
        else:
            print "AccessListBindDelete RPC Failed "
            res.append("AccessListBindDelete RPC Failed and returned %s" % (binddelresult))
        pause()

        acldelresult = fw.AccessListDelete(filter,10)
        print 'Invoking fw.AccessListDelete \nreturn = ', acldelresult
        if acldelresult.status is ACL_STATUS_EOK :
                print "AccessListDelete RPC Passed"
                res.append("AccessListDelete RPC Passed and returned %s" % (acldelresult))
        else:
                print "AccessListDelete RPC Failed"
                res.append("AccessListDelete RPC Failed and returned %s" % (acldelresult))
        pause()

        print "FINAL RESULT : \n"
        for i in res:
            print i

except AbortionError as e:
    print "code is ", e.code
    print "details is ", e.details

while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)

       

        
        


