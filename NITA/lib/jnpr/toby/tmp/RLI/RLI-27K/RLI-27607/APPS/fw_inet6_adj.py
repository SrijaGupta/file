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
        match1 = AclMatchPort(min=0, max=120, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=10, max=20, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t=AclEntryInet6TerminatingAction(action_accept = ACL_TRUE)
        nt=AclEntryInet6NonTerminatingAction(action_count = AclActionCounter(counter_name="C1"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_NONE,ace_name='')
        term1=AclInet6Entry(ace_name="t1",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(inet6_entry=term1)

        filter=AccessList(acl_name = "INET61", acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_INET6, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
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
        match1 = AclMatchPort(min=10, max=120, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=100, max=120, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t = AclEntryInet6TerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="C2"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj = AclAdjacency(type=ACL_ADJACENCY_AFTER, ace_name='t3')
        term1 = AclInet6Entry(ace_name="t2", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,actions=term1Action1)
        tlist1 = AclEntry(inet6_entry=term1)

        filter = AccessList(acl_name="INET61", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_INET6, acl_flag=ACL_FLAGS_NONE,ace_list=[tlist1])
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
        match1 = AclMatchPort(min=110, max=120, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=10, max=30, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t = AclEntryInet6TerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="C3"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj = AclAdjacency(type=ACL_ADJACENCY_BEFORE, ace_name='t5')
        term1 = AclInet6Entry(ace_name="t3", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj, matches=term1match1,actions=term1Action1)
        tlist1 = AclEntry(inet6_entry=term1)

        filter = AccessList(acl_name="INET61", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_INET6, acl_flag=ACL_FLAGS_NONE,ace_list=[tlist1])
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
        match1 = AclMatchPort(min=5, max=125, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=15, max=25, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t = AclEntryInet6TerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="C4"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_BEFORE,ace_name='')
        term1=AclInet6Entry(ace_name="t1",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(inet6_entry=term1)

        filter=AccessList(acl_name = "INET61",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_INET6, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
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
        match1 = AclMatchPort(min=30, max=120, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=50, max=70, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t = AclEntryInet6TerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="C5"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER,ace_name='t1')
        term2=AclInet6Entry(ace_name="t2",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist2=AclEntry(inet6_entry=term2)

        filter=AccessList(acl_name = "INET61",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_INET6, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist2])
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
        match1 = AclMatchPort(min=20, max=70, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=15, max=80, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t = AclEntryInet6TerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="C6"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER,ace_name='')
        term1=AclInet6Entry(ace_name="t3",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(inet6_entry=term1)

        filter=AccessList(acl_name = "INET61",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_INET6, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist1])
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
        match1 = AclMatchPort(min=100, max=120, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=100, max=130, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t = AclEntryInet6TerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="C7"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_BEFORE,ace_name='t1')
        term2=AclInet6Entry(ace_name="t4",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist2=AclEntry(inet6_entry=term2)

        filter=AccessList(acl_name = "INET61",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_INET6, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist2])
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
        match1 = AclMatchPort(min=120, max=220, match_op=ACL_MATCH_OP_EQUAL)
        match2 = AclMatchPort(min=80, max=520, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchInet6(match_dst_ports=[match2],match_src_ports=[match1])
        t = AclEntryInet6TerminatingAction(action_accept=ACL_TRUE)
        nt = AclEntryInet6NonTerminatingAction(action_count=AclActionCounter(counter_name="C8"))
        term1Action1 = AclEntryInet6Action(action_t=t, actions_nt=nt)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER,ace_name='t2')
        term2=AclInet6Entry(ace_name="t5",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist2=AclEntry(inet6_entry=term2)

        filter=AccessList(acl_name = "INET61",acl_type = ACL_TYPE_CLASSIC, acl_family = ACL_FAMILY_INET6, acl_flag = ACL_FLAGS_NONE, ace_list=[tlist2])
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
        bind=AccessListObjBind(acl=filter,obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.0'),bind_direction=ACL_BIND_DIRECTION_INPUT,bind_family=ACL_FAMILY_INET6)
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
       

        
        


