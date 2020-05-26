import sys,time,os,argparse,datetime
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

#

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
    time1 = datetime.datetime.now()
    print time1
    mytlist = []
    k = 1
    start = AccessListVoid(void="start")
    start_res = fw.AccessListPileupStart(start, 1000)  ###############
    print 'Invoking fw.AccessListpileupstart \nreturn = ', start_res
    if start_res.status is ACL_STATUS_EOK:
        print "AccessListpileupstart RPC Passed"
    else:
        print "AccessListpileupstart RPC Failed"
    pause()
    for i in range(1,51):
            mac = hex(i).split('x')[1]
            pparam = AclPolicerParameter(
                two_color_parameter=AclPolicerTwoColor(bw_unit=ACL_POLICER_RATE_MBPS, bandwidth=1,
                                                       burst_unit=ACL_POLICER_BURST_SIZE_BYTE, burst_size=1500,
                                                       discard=ACL_TRUE))
            policer = AccessListPolicer(policer_name="P"+str(k), policer_type=ACL_TWO_COLOR_POLICER,policer_flag=ACL_POLICER_FLAG_TERM_SPECIFIC, policer_params=pparam)
            print policer

            result = fw.AccessListPolicerAdd(policer, 10)
            print 'Invoking fw.AccessListPolicerAdd \nreturn = ', result
            if result.status is ACL_STATUS_EOK:
                print "AccessListPolicerAdd RPC Passed"
            else:
                print "AccessListPolicerAdd RPC Failed"

            MAC1 = MacAddress(addr_string="aa:00:00:00:" + mac + ":11")
            MAC2 = MacAddress(addr_string="bb:00:00:00:" + mac + ":11")
            matchMAC1 = AclMatchMacAddress(addr=MAC1, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)
            matchMAC2 = AclMatchMacAddress(addr=MAC2, addr_len=48, match_op=ACL_MATCH_OP_EQUAL)

            term1match1 = AclEntryMatchCcc(match_dst_macs=[matchMAC2], match_src_macs=[matchMAC1])

            tt=AclEntryCccTerminatingAction(action_accept = ACL_TRUE)
            nt=AclEntryCccNonTerminatingAction(action_count = AclActionCounter(counter_name="Match"+str(k)),action_policer=AclActionPolicer(policer=policer))
            term1Action1 = AclEntryCccAction(action_t=tt, actions_nt=nt)
            adj=AclAdjacency(type=ACL_ADJACENCY_AFTER)
            term1=AclCccEntry(ace_name="t"+str(k),ace_op=ACL_ENTRY_OPERATION_ADD,adjacency=adj,matches=term1match1 ,actions=term1Action1)
            tlist=AclEntry(ccc_entry=term1)
            print tlist
            mytlist.append(tlist)
            k += 1

    pause()
    filter = AccessList(acl_name="CCC1", acl_type=ACL_TYPE_CLASSIC, acl_family=ACL_FAMILY_CCC,acl_flag=ACL_FLAGS_NONE, ace_list=mytlist)
    print filter
    result = fw.AccessListAdd(filter, 100)
    print 'Invoking fw.AccessListAdd \nreturn = ', result

    if result.status is ACL_STATUS_EOK:
        print "AccessListAdd RPC Passed"
    else:
        print "AccessListAdd RPC Failed"
    pause()

    end = AccessListVoid(void="stop")
    end_res = fw.AccessListPileupEnd(end, 5000)  ###############
    print 'Invoking fw.AccessListpileupEnd \nreturn = ', end_res
    if end_res.status is ACL_STATUS_EOK:
        print "AccessListpileupEnd RPC Passed"
    else:
        print "AccessListpileupEnd RPC Failed"
    pause()

    start = AccessListVoid(void="start")
    start_res = fw.AccessListPileupStart(start, 1000)  ###############
    print 'Invoking fw.AccessListpileupstart \nreturn = ', start_res
    if start_res.status is ACL_STATUS_EOK:
        print "AccessListpileupstart RPC Passed"
    else:
        print "AccessListpileupstart RPC Failed"
    pause()
    for k in range(1,51):

        bind=AccessListObjBind(acl=filter,obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,bind_object=AccessListBindObjPoint(intf=args.iflname + '.' + str(k)),bind_direction=ACL_BIND_DIRECTION_INPUT,bind_family=ACL_FAMILY_CCC)
        bindresult=fw.AccessListBindAdd(bind,10)
        print 'Invoking fw.AccessListBindAdd \nreturn = ', bindresult
        if bindresult.status is ACL_STATUS_EOK:
            print "AccessListBindAdd RPC Passed -- %s" %k
        else:
            print "AccessListBindAdd RPC Failed -- %s" %k
        # pause()

    pause()
    end = AccessListVoid(void="stop")
    end_res = fw.AccessListPileupEnd(end, 5000)  ###############
    print 'Invoking fw.AccessListpileupEnd \nreturn = ', end_res
    if end_res.status is ACL_STATUS_EOK:
        print "AccessListpileupEnd RPC Passed"
    else:
        print "AccessListpileupEnd RPC Failed"
    pause()

    for i in range(1, 51):
        count = AccessListCounter(acl=filter, counter_name="Match"+str(i))
        cntres = fw.AccessListCounterGet(count, 10)
        print 'Invoking fw.AccessListCounterGet \nreturn = ', cntres
        if cntres.status is ACL_STATUS_EOK:
            print "AccessListCounterGet RPC Passed"
        else:
            print "AccessListCounterGet RPC Failed"
        pause()

    for i in range(1, 51):
        pcount = AccessListCounter(acl=filter, counter_name="P"+str(i)+"-t"+str(i))
        pcntres = fw.AccessListPolicerCounterGet(pcount, 10)
        print 'Invoking fw.AccessListPolicerCounterGet \nreturn = ', pcntres
        if pcntres.status is ACL_STATUS_EOK:
            print "AccessListPolicerCounterGet RPC Passed"
        else:
            print "AccessListPolicerCounterGet RPC Failed"
        pause()

    for i in range(0,5):
        j = i * 10
        count = AccessListCounterBulk(acl=filter, starting_index=j)
        for stream in fw.AccessListCounterBulkGet(count, 10):
            print stream
    pause()

    for i in range(0, 5):
        j = i * 10
        count = AccessListCounterBulk(acl=filter, starting_index=j)
        for stream in fw.AccessListPolicerCounterBulkGet(count, 10):
            print stream
    pause()

    start = AccessListVoid(void="start")
    start_res = fw.AccessListPileupStart(start, 1000)  ###############
    print 'Invoking fw.AccessListpileupstart \nreturn = ', start_res
    if start_res.status is ACL_STATUS_EOK:
        print "AccessListpileupstart RPC Passed"
    else:
        print "AccessListpileupstart RPC Failed"

    pause()
    for i in range(1, 51):
        bind = AccessListObjBind(acl=filter, obj_type=ACL_BIND_OBJ_TYPE_INTERFACE, bind_object=AccessListBindObjPoint(intf=args.iflname + '.' + str(i)),
                                 bind_direction=ACL_BIND_DIRECTION_INPUT, bind_family=ACL_FAMILY_CCC)

        bindresult = fw.AccessListBindDelete(bind, 10)
        print 'Invoking fw.AccessListBindDelete \nreturn = ', bindresult
        if bindresult.status is ACL_STATUS_EOK:
            print "AccessListBindDelete RPC Passed %s" % i
        else:
            print "AccessListBindDelete RPC Failed %s" % i
        # pause()

    pause()
    end = AccessListVoid(void="stop")
    end_res = fw.AccessListPileupEnd(end, 5000)  ###############
    print 'Invoking fw.AccessListpileupEnd \nreturn = ', end_res
    if end_res.status is ACL_STATUS_EOK:
        print "AccessListpileupEnd RPC Passed"
    else:
        print "AccessListpileupEnd RPC Failed"

    pause()
    filter = AccessList(acl_name="CCC1",acl_family=ACL_FAMILY_CCC)
    result = fw.AccessListDelete(filter,10)
    print 'Invoking fw.AccessListDelete \nreturn = ', result
    if result.status is ACL_STATUS_EOK :
            print "AccessListDelete RPC Passed"
    else:
            print "AccessListDelete RPC Failed"
    pause()

except AbortionError as e:
    print "code is ", e.code
    print "details is ", e.details

while True:
    import signal
    os.kill(os.getpid(), signal.SIGTERM)


