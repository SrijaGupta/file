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
        login_response = stub.LoginCheck(authentication_service_pb2.LoginRequest(user_name=APP_USER, password=APP_PASSWORD, client_id=client_id), 100)
        if (login_response.result == 1):
            print "Login to ", device1, "successful"
        else:
            print "Login to ", device1, "failed"
            raise SystemExit()
        fw = firewall_service_pb2.beta_create_AclService_stub(channel)
        res=[]
        MAC1=MacAddress(addr_string='00:00:00:00:01:11')
        MAC2=MacAddress(addr_string='00:00:00:00:02:22')
        matchIP1=AclMatchMacAddress(addr=MAC1,addr_len=32,match_op=ACL_MATCH_OP_EQUAL)
        matchIP2=AclMatchMacAddress(addr=MAC2,addr_len=32,match_op=ACL_MATCH_OP_EQUAL)

        term1match1=AclEntryMatchVpls(match_dst_macs=[matchIP2],match_src_macs=[matchIP1])
        t=AclEntryVplsTerminatingAction(action_accept = ACL_TRUE)
        nt=AclEntryVplsNonTerminatingAction(action_count = AclActionCounter(counter_name="C1"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_NONE,ace_name='')
        term1=AclVplsEntry(ace_name="t1",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(vpls_entry=term1)

        filter=AccessList(acl_name = "VPLS1", acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListAdd(filter,10)
        print 'Invoking fw.AccessListAdd \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListAdd RPC Passed with adj type : ACL_ADJACENCY_NONE"
                res.append("AccessListAdd RPC Passed with adj type : ACL_ADJACENCY_NONE and returned %s" % (result))
        else:
                print "AccessListAdd RPC Failed with adj type : ACL_ADJACENCY_NONE"
                res.append("AccessListAdd RPC Failed with adj type : ACL_ADJACENCY_NONE and returned %s" % (result))

        pause()
        MAC1 = MacAddress(addr_string='00:00:00:00:03:33')
        MAC2 = MacAddress(addr_string='00:00:00:00:04:44')
        matchIP1 = AclMatchMacAddress(addr=MAC1, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)
        matchIP2 = AclMatchMacAddress(addr=MAC2, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchIP2], match_src_macs=[matchIP1])
        t = AclEntryVplsTerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C2"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj = AclAdjacency(type=ACL_ADJACENCY_AFTER, ace_name='t3')
        term1 = AclVplsEntry(ace_name="t2", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,actions=term1Action1)
        tlist1 = AclEntry(vpls_entry=term1)

        filter = AccessList(acl_name="VPLS1", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_VPLS, acl_flag=ACL_FLAGS_NONE,ace_list=[tlist1])
        print filter

        result = fw.AccessListChange(filter, 10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK:
            print "AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with Non existing term"
            res.append("AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with Non existing term and returned %s" % (result))
        else:
            print "AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with Non existing term"
            res.append("AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with Non existing term and returned %s" % (result))

        pause()
        MAC1 = MacAddress(addr_string='00:00:00:00:05:55')
        MAC2 = MacAddress(addr_string='00:00:00:00:06:66')
        matchIP1 = AclMatchMacAddress(addr=MAC1, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)
        matchIP2 = AclMatchMacAddress(addr=MAC2, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchIP2], match_src_macs=[matchIP1])
        t = AclEntryVplsTerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C3"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj = AclAdjacency(type=ACL_ADJACENCY_BEFORE, ace_name='t5')
        term1 = AclVplsEntry(ace_name="t3", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,actions=term1Action1)
        tlist1 = AclEntry(vpls_entry=term1)

        filter = AccessList(acl_name="VPLS1", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_VPLS, acl_flag=ACL_FLAGS_NONE,ace_list=[tlist1])
        print filter

        result = fw.AccessListChange(filter, 10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK:
            print "AccessListChange RPC Passed with adj type : ACL_ADJACENCY_BEFORE with Non existing term"
            res.append("AccessListChange RPC Passed with adj type : ACL_ADJACENCY_BEFORE with Non existing term and returned %s" % (result))
        else:
            print "AccessListChange RPC Failed with adj type : ACL_ADJACENCY_BEFORE with Non existing term"
            res.append("AccessListChange RPC Failed with adj type : ACL_ADJACENCY_BEFORE with Non existing term and returned %s" % (result))

        pause()
        MAC1 = MacAddress(addr_string='a1:00:00:00:07:77')
        MAC2 = MacAddress(addr_string='b1:00:00:00:08:88')
        matchIP1 = AclMatchMacAddress(addr=MAC1, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)
        matchIP2 = AclMatchMacAddress(addr=MAC2, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchIP2], match_src_macs=[matchIP1])
        t = AclEntryVplsTerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C4"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_BEFORE,ace_name='')
        term1=AclVplsEntry(ace_name="t1",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(vpls_entry=term1)

        filter=AccessList(acl_name = "VPLS1",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListAdd(filter,10)
        print 'Invoking fw.AccessListAdd \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListAdd RPC Passed with adj type : ACL_ADJACENCY_BEFORE with null term"
                res.append("AccessListAdd RPC Passed with adj type : ACL_ADJACENCY_BEFORE with null term and returned %s" % (result))
        else:
                print "AccessListAdd RPC Failed with adj type : ACL_ADJACENCY_BEFORE with null term"
                res.append("AccessListAdd RPC Failed with adj type : ACL_ADJACENCY_BEFORE with null term and returned %s" % (result))

        pause()
        MAC1 = MacAddress(addr_string='a2:00:00:00:09:99')
        MAC2 = MacAddress(addr_string='b2:00:00:00:10:10')
        matchIP1 = AclMatchMacAddress(addr=MAC1, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)
        matchIP2 = AclMatchMacAddress(addr=MAC2, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchIP2], match_src_macs=[matchIP1])
        t = AclEntryVplsTerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C5"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER,ace_name='t1')
        term2=AclVplsEntry(ace_name="t2",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist2=AclEntry(vpls_entry=term2)

        filter=AccessList(acl_name = "VPLS1",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist2])
        print filter

        result = fw.AccessListChange(filter,10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with existing term"
                res.append("AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with existing term and returned %s" % (result))
        else:
                print "AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with existing term"
                res.append("AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with existing term and returned %s" % (result))

        pause()
        MAC1 = MacAddress(addr_string='a3:00:00:00:11:11')
        MAC2 = MacAddress(addr_string='b3:00:00:00:12:12')
        matchIP1 = AclMatchMacAddress(addr=MAC1, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)
        matchIP2 = AclMatchMacAddress(addr=MAC2, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchIP2], match_src_macs=[matchIP1])
        t = AclEntryVplsTerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C6"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER,ace_name='')
        term1=AclVplsEntry(ace_name="t3",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(vpls_entry=term1)

        filter=AccessList(acl_name = "VPLS1",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
        print filter

        result = fw.AccessListChange(filter,10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with null term"
                res.append("AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with null term and returned %s" % (result))
        else:
                print "AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with null term"
                res.append("AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with null term and returned %s" % (result))

        pause()
        MAC1 = MacAddress(addr_string='a4:00:00:00:13:13')
        MAC2 = MacAddress(addr_string='b4:00:00:00:14:14')
        matchIP1 = AclMatchMacAddress(addr=MAC1, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)
        matchIP2 = AclMatchMacAddress(addr=MAC2, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchIP2], match_src_macs=[matchIP1])
        t = AclEntryVplsTerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C7"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_BEFORE,ace_name='t1')
        term2=AclVplsEntry(ace_name="t4",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist2=AclEntry(vpls_entry=term2)

        filter=AccessList(acl_name = "VPLS1",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist2])
        print filter

        result = fw.AccessListChange(filter,10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListChange RPC Passed with adj type : ACL_ADJACENCY_BEFORE with existing term"
                res.append("AccessListChange RPC Passed with adj type : ACL_ADJACENCY_BEFORE with existing term and returned %s" % (result))
        else:
                print "AccessListChange RPC Failed with adj type : ACL_ADJACENCY_BEFORE with existing term"
                res.append("AccessListChange RPC Failed with adj type : ACL_ADJACENCY_BEFORE with existing term and returned %s" % (result))

        pause()
        MAC1 = MacAddress(addr_string='a5:00:00:00:15:15')
        MAC2 = MacAddress(addr_string='b5:00:00:00:16:16')
        matchIP1 = AclMatchMacAddress(addr=MAC1, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)
        matchIP2 = AclMatchMacAddress(addr=MAC2, addr_len=32, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchIP2], match_src_macs=[matchIP1])
        t = AclEntryVplsTerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="C8"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER,ace_name='t2')
        term2=AclVplsEntry(ace_name="t5",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist2=AclEntry(vpls_entry=term2)

        filter=AccessList(acl_name = "VPLS1",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_VPLS, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist2])
        print filter

        result = fw.AccessListChange(filter,10)
        print 'Invoking fw.AccessListChange \nreturn = ', result
        if result.status is ACL_STATUS_EOK :
                print "AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with existing term"
                res.append("AccessListChange RPC Passed with adj type : ACL_ADJACENCY_AFTER with existing term and returned %s" % (result))
        else:
                print "AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with existing term"
                res.append("AccessListChange RPC Failed with adj type : ACL_ADJACENCY_AFTER with existing term and returned %s" % (result))

        pause()
        bind=AccessListObjBind(acl=filter,obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.0'),bind_direction=ACL_BIND_DIRECTION_INPUT,bind_family=ACL_FAMILY_VPLS)
        print bind

        bindresult=fw.AccessListBindAdd(bind,10)
        print 'Invoking fw.AccessListBindAdd \nreturn = ', bindresult
        if bindresult.status is ACL_STATUS_EOK:
            print "AccessListBindAdd RPC Passed"
            res.append("AccessListBindAdd RPC Passed and returned %s" % (bindresult))
        else:
            print "AccessListBindAdd RPC Failed"
            res.append("AccessListBindAdd RPC Failed and returned %s" % (bindresult))

        pause()
        binddelresult = fw.AccessListBindDelete(bind, 10)
        print 'Invoking fw.AccessListBindDelete \nreturn = ', binddelresult
        if binddelresult.status is ACL_STATUS_EOK:
            print "AccessListBindDelete RPC Passed with ace operation : ACL_ENTRY_OPERATION_ADD"
            res.append("AccessListBindDelete RPC Passed with ace operation : ACL_ENTRY_OPERATION_ADD and returned %s" % (binddelresult))
        else:
            print "AccessListBindDelete RPC Failed with ace operation :ACL_ENTRY_OPERATION_ADD"
            res.append("AccessListBindDelete RPC Failed with ace operation : ACL_ENTRY_OPERATION_ADD and returned %s" % (binddelresult))
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
       

        
        


