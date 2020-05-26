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
        pause()
        flag = 0
        res=[]
        pparam=AclPolicerParameter(sr_three_color_parameter=AclPolicerSingleRateThreeColor(committed_rate_unit=ACL_POLICER_RATE_KBPS,committed_rate=10,committed_burst_unit=ACL_POLICER_BURST_SIZE_KBYTE,committed_burst_size=1500,excess_burst_size=2000,excess_burst_unit=ACL_POLICER_BURST_SIZE_KBYTE,discard=ACL_TRUE,color_mode=ACL_COLOR_MODE_COLOR_AWARE))
        pol1=AccessListPolicer(policer_name="P1",policer_type=ACL_SINGLE_RATE_THREE_COLOR_POLICER,policer_flag=ACL_POLICER_FLAG_TERM_SPECIFIC,policer_params=pparam)

        print pol1

        polres = fw.AccessListPolicerAdd(pol1, 10)
        print 'Invoking fw.AccessListPolicerAdd \nreturn = ', polres
        if polres.status is ACL_STATUS_EOK:
                print "AccessListPolicerAdd RPC Passed"
                res.append("AccessListPolicerAdd RPC Passed and returned %s" % (polres))
        else:
                print "AccessListPolicerAdd RPC Failed"
                res.append("AccessListPolicerAdd RPC Failed and returned %s" % (polres))
                flag += 1
        pause()

        MAC1 = MacAddress(addr_string='aa:00:00:00:00:11')
        MAC2 = MacAddress(addr_string='bb:00:00:00:00:11')
        matchMAC1 = AclMatchMacAddress(addr=MAC1, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)
        matchMAC2 = AclMatchMacAddress(addr=MAC2, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)

        term1match1 = AclEntryMatchVpls(match_dst_macs=[matchMAC2],match_src_macs=[matchMAC1])
        t = AclEntryVplsTerminatingAction(action_accept=1)
        t1 = AclEntryVplsTerminatingAction(action_accept=1)
        nt=AclEntryVplsNonTerminatingAction(action_count = AclActionCounter(counter_name="Match1"),action_log=1,action_syslog=1,action_policer=AclActionPolicer(policer=pol1))
        nt1 = AclEntryVplsNonTerminatingAction(action_count=AclActionCounter(counter_name="Match2"))
        term1Action1 = AclEntryVplsAction(action_t=t, actions_nt=nt)
        term1Action2 = AclEntryVplsAction(action_t=t1, actions_nt=nt1)

        adj=AclAdjacency(type=ACL_ADJACENCY_AFTER)
        term1=AclVplsEntry(ace_name="t1",ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1,actions=term1Action1)
        tlist1=AclEntry(vpls_entry=term1)
        term2 = AclVplsEntry(ace_name="t2", ace_op=ACL_ENTRY_OPERATION_ADD, adjacency=adj,actions=term1Action2)
        tlist2 = AclEntry(vpls_entry=term2)

        filter = AccessList(acl_name="f1", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_VPLS,acl_flag=ACL_FLAGS_NONE, ace_list=[tlist1,tlist2])
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

        bind=AccessListObjBind(acl=filter,obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.0'),bind_direction=ACL_BIND_DIRECTION_INPUT,bind_family=ACL_FAMILY_VPLS)
        print bind

        bindaddresult=fw.AccessListBindAdd(bind,10)
        print 'Invoking fw.AccessListBindAdd \nreturn = ', bindaddresult
        if  bindaddresult.status is ACL_STATUS_EOK :
                print "AccessListBindAdd RPC Passed"
                res.append("AccessListBindAdd RPC Passed and returned %s" % (bindaddresult))
        else:
                print "AccessListBindAdd RPC Failed"
                res.append("AccessListBindAdd RPC Failed and returned %s" % (bindaddresult))
                flag += 1

        pause()
        # bind = AccessListObjBind(acl=filter, obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.0'),bind_direction=ACL_BIND_DIRECTION_INPUT, bind_family=ACL_FAMILY_VPLS)
        # print bind
        binddelresult = fw.AccessListBindDelete(bind,10)
        print 'Invoking fw.AccessListBindDelete \nreturn = ', binddelresult
        if binddelresult.status is ACL_STATUS_EOK :
                print "AccessListBindDelete RPC Passed"
                res.append("AccessListBindDelete RPC Passed and returned %s" % (binddelresult))
        else:
                print "AccessListBindDelete RPC Failed"
                res.append("AccessListBindDelete RPC Failed and returned %s" % (binddelresult))
                flag += 1

        pause()
        filter = AccessList(acl_name="f1",acl_family = ACL_FAMILY_VPLS)
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
        print pol1
        poldelresult = fw.AccessListPolicerDelete(pol1,10)
        print 'Invoking fw.AccessListPolicerDelete \nreturn = ', poldelresult
        if acldelresult.status is ACL_STATUS_EOK :
                print "AccessListPolicerDelete RPC Passed"
                res.append("AccessListPolicerDelete RPC Passed and returned %s" % (poldelresult))
        else:
                print "AccessListPolicerDelete RPC Failed"
                res.append("AccessListPolicerDelete RPC Failed and returned %s" % (poldelresult))
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

# except Exception as tx:
#     print ("Caught Exception {0}\n".format(tx))

# except Exception as tx:
#        print '%s' % (tx.message)

while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)
