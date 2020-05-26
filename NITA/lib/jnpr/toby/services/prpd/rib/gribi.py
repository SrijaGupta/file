"""
    DOC : GRIBI
"""

# import sys
# from authentication_service_pb2 import *
# from prpd_service_pb2 import *
# from prpd_common_pb2 import *
# from jnx_addr_pb2 import *
# from rib_service_pb2 import *
# from gribi_service_pb2 import *
# from gribi_aft_pb2 import *
# from gribi_ywrapper_pb2 import *
# import gribi_service_pb2
# import gribi_aft_pb2
# import gribi_ywrapper_pb2
import copy
# import logging
# import time
# import os
# import re
#import random
#from prpd import *
import jnpr.toby.services.prpd.prpd as prpd # pylint: disable=import-error
#import prpd as prpd
# from jnpr.toby.hldcl.device_data import DeviceData
# from datetime import datetime
# from jnpr.toby.init.init import init


def _init(api_list):
    """
    DOcs
    """
    prpd.import_api(api_list)


def gribi_add(dev, channel_id, **kwargs):
    """
       DOC : This function gets the parameter values for
       nexthop/nexthop group/mpls/ipev4/ipv6/inetcolor/inet6color
       in the form of list for adding an entry to the table
    """
    gribiop = prpd.AFTOperation()
    gop = prpd.AFTOperation.ADD
    gribiop.op = gop
    ret = kwargs.get('ret', None)
    stream = kwargs.get('stream', None)
    gribi_request_list = []

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "next_hop":
            gribirequestl = process_nexthop(gribiop, **kwargs)

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "next_hop_group":
            gribirequestl = process_nexthopgroup(gribiop, **kwargs)

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "route":
            gribirequestl = process_route(gribiop, **kwargs)

    if ret is True:
        #print("its coming to this true point")
        return gribirequestl

    if 'gribi_request_list' in kwargs:
        result = prpd.process_api(dev, channel_id, "Modify",\
                              [kwargs.get('gribi_request_list'), "gRIBI"], stream=True)
    else:
        gribi_request_list.append(gribirequestl)
        result = prpd.process_api(dev, channel_id, "Modify",\
                              [gribi_request_list, "gRIBI"], stream=True)
    return  result

def gribi_delete(dev, channel_id, **kwargs):
    """
       DOC : This function gets the parameter values for
       nexthop/nexthop group/mpls/ipev4/ipv6/inetcolor/inet6color
       in the form of list for deleting an entry from the table
    """
    gribiop = prpd.AFTOperation()
    gop = prpd.AFTOperation.DELETE
    gribiop.op = gop
    ret = kwargs.get('ret', None)
    stream = kwargs.get('stream', None)
    gribi_request_list = []

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "next_hop":
            gribirequestl = process_nexthop(gribiop, **kwargs)

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "next_hop_group":
            gribirequestl = process_nexthopgroup(gribiop, **kwargs)

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "route":
            gribirequestl = process_route(gribiop, **kwargs)

    if ret is True:
        return gribirequestl
    if 'gribi_request_list' in kwargs:
        result = prpd.process_api(dev, channel_id, "Modify",\
                              [kwargs.get('gribi_request_list'), "gRIBI"], stream=True)
    else:
        gribi_request_list.append(gribirequestl)
        result = prpd.process_api(dev, channel_id, "Modify",\
                              [gribi_request_list, "gRIBI"], stream=True)

    return  result

def gribi_modify(dev, channel_id, **kwargs):
    """
       DOC : This function gets the parameter values for
       nexthop/nexthopgroup/mpls/ipev4/ipv6/inetcolor/inet6color
       in the form of list for modifying/updating an entry in the table
    """
    gribiop = prpd.AFTOperation()
    gop = prpd.AFTOperation.REPLACE
    gribiop.op = gop
    ret = kwargs.get('ret', None)
    stream = kwargs.get('stream', None)
    gribi_request_list = []

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "next_hop":
            gribirequestl = process_nexthop(gribiop, **kwargs)

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "next_hop_group":
            gribirequestl = process_nexthopgroup(gribiop, **kwargs)

    if 'type_of_operation' in kwargs:
        type_of_operation = kwargs.get('type_of_operation')
        if type_of_operation == "route":
            gribirequestl = process_route(gribiop, **kwargs)

    if ret is True:
        return gribirequestl
    if 'gribi_request_list' in kwargs:
        result = prpd.process_api(dev, channel_id, "Modify",\
                              [kwargs.get('gribi_request_list'), "gRIBI"], stream=True)
    else:
        gribi_request_list.append(gribirequestl)
        result = prpd.process_api(dev, channel_id,\
                              "Modify", [gribi_request_list, "gRIBI"], stream=True)

    return  result

def process_nexthop(gribiop, **kwargs):
    """
       DOC : This function gets the parameter values for nexthop entry
    """
    onenh = prpd.Afts.NextHop()
    nhk = prpd.Afts.NextHopKey()

    if 'table_name' in kwargs:
        table = kwargs.get('table_name')
        gribiop.network_instance = table

    if 'next_hop_id' in kwargs:
        try:
            next_hop_id_list = []
            if isinstance(kwargs["next_hop_id"], list):
                next_hop_id_list = copy.deepcopy(kwargs.get('next_hop_id'))
            else:
                next_hop_id_list = [kwargs["next_hop_id"], ]
            nhk.index = next_hop_id_list.pop()
        except ValueError as excp:
            return excp

    if 'gateway_address' in kwargs:
        gwaddr = kwargs.get('gateway_address')
        gwv = prpd.StringValue(value=gwaddr)
        onenh.ip_address.value = gwv.value

    if 'interface_name' in kwargs:
        try:
            interface = prpd.Afts.NextHop.InterfaceRef()
            intf = kwargs.get('interface_name')
            if "." in intf:
                ifd, subunit = intf.split('.')
                subunit = int(subunit)
            else:
                ifd = intf
                subunit = 0
            intfd = prpd.StringValue(value=ifd)
            intfs = prpd.UintValue(value=subunit)
            interface.nh_interface.value = intfd.value
            interface.subinterface.value = intfs.value
            onenh.interface_ref.CopyFrom(interface)

        except ValueError as excp:
            return excp

    if 'labels' in kwargs:
        try:
            label_stack = []
            if isinstance(kwargs["labels"], list):
                label_stack = copy.deepcopy(kwargs.get('labels'))
            else:
                label_stack = [kwargs["labels"], ]
            lblstack = []
            for label in label_stack:
                lblstack.append(prpd.Afts.NextHop.PushedMplsLabelStackUnion(
                    pushed_mpls_label_stack_uint64=int(label)))
            onenh.pushed_mpls_label_stack.extend(lblstack)

        except ValueError as excp:
            return excp

    nhk.next_hop.CopyFrom(onenh)

    gribiop.id = kwargs.get('operation_id', 1)
    gribiop.next_hop.CopyFrom(nhk)
    gribioplist = [gribiop]
    gribirequestlist = []
    gribirequestlist.append(prpd.ModifyRequest(operation=gribioplist))

    return  prpd.ModifyRequest(operation=gribioplist)

def process_nexthopgroup(gribiop, **kwargs):
    """
       DOC : This function gets the parameter values for nexthop group entry
    """
    nhg = prpd.Afts.NextHopGroupKey()
    nh_pair = prpd.Afts.NextHopGroup.NextHopKey()
    nh_weight = prpd.Afts.NextHopGroup.NextHop()
    nhlst = []

    if 'table_name' in kwargs:
        table = kwargs.get('table_name')
        gribiop.network_instance = table

    if 'next_hop_id' in kwargs:
        try:
            next_hop_id_list = []
            if isinstance(kwargs["next_hop_id"], list):
                next_hop_id_list = kwargs.get('next_hop_id')
            else:
                next_hop_id_list = [kwargs["next_hop_id"], ]
            for nhopid in next_hop_id_list:
                nh_pair = prpd.Afts.NextHopGroup.NextHopKey()
                nh_pair.index = nhopid
                nhlst.append(nh_pair)
        except ValueError as excp:
            return excp

    if 'weight' in kwargs:
        try:
            wt_list = []
            if isinstance(kwargs["weight"], list):
                wt_list = kwargs.get('weight')
            else:
                wt_list = [kwargs["weight"], ]
            for i in range(len(wt_list)):
                wtl = prpd.UintValue(value=wt_list[i])
                nh_weight.weight.value = wtl.value
                nhlst[i].next_hop.CopyFrom(nh_weight)
        except ValueError as excp:
            return excp

    if 'next_hop_groupid' in kwargs:
        try:
            next_hop_groupid_list = []
            if isinstance(kwargs["next_hop_groupid"], list):
                next_hop_groupid_list = copy.deepcopy(kwargs.get('next_hop_groupid'))
            else:
                next_hop_groupid_list = [kwargs["next_hop_groupid"], ]
            nhg.id = next_hop_groupid_list.pop()
        except ValueError as excp:
            return excp

    if 'color' in kwargs:
        try:
            color = kwargs.get('color')
            colv = prpd.UintValue(value=color)
            nhg.next_hop_group.color.value = colv.value
        except ValueError as excp:
            return excp

    nhg.next_hop_group.next_hop.extend(nhlst)
    gribiop.id = kwargs.get('operation_id', 1)
    gribiop.next_hop_group.CopyFrom(nhg)
    gribioplist = [gribiop]
    gribirequestlist = []
    gribirequestlist.append(prpd.ModifyRequest(operation=gribioplist))
    return prpd.ModifyRequest(operation=gribioplist)


def process_route(gribiop, **kwargs):
    """
       DOC : This function gets the parameter values for mpls/inet/inet6/inetcolor/inet6color entry
    """
    nhgpv = prpd.UintValue()
    if 'table_name' in kwargs:
        table = kwargs.get('table_name')
        gribiop.network_instance = table

    if 'next_hop_groupid' in kwargs:
        try:
            next_hop_groupid_list = []
            if isinstance(kwargs["next_hop_groupid"], list):
                next_hop_groupid_list = copy.deepcopy(kwargs.get('next_hop_groupid'))
            else:
                next_hop_groupid_list = [kwargs["next_hop_groupid"], ]
            nhgpv = prpd.UintValue(value=next_hop_groupid_list.pop())
        except ValueError as excp:
            return excp

    if 'prefix' in kwargs:
        pfx = kwargs.get('prefix')

    if 'prefix_length' in kwargs and 'prefix' in kwargs:
        pfx = str(pfx) + '/' +str(kwargs.get('prefix_length'))

    if 'table_name' in kwargs:
        family = kwargs.get('table_name')
        if "mpls" in family:
            try:
                mplsentry = prpd.Afts.LabelEntry()
                prefixlist = prpd.Afts.LabelEntryKey()
                if nhgpv:
                    mplsentry.next_hop_group.value = nhgpv.value
                prefixlist.label_uint64 = int(kwargs.get('prefix'))
                prefixlist.label_entry.CopyFrom(mplsentry)
                gribiop.mpls.CopyFrom(prefixlist)
            except ValueError as excp:
                return excp


        elif "inet6" in family:
            try:
                ipv6entry = prpd.Afts.Ipv6Entry()
                prefixlist = prpd.Afts.Ipv6EntryKey()
                if nhgpv:
                    ipv6entry.next_hop_group.value = nhgpv.value
                prefixlist.prefix = (pfx)
                prefixlist.ipv6_entry.CopyFrom(ipv6entry)
                gribiop.ipv6.CopyFrom(prefixlist)
            except ValueError as excp:
                return excp

        elif "inet" in family:
            try:
                ipv4entry = prpd.Afts.Ipv4Entry()
                prefixlist = prpd.Afts.Ipv4EntryKey()
                if nhgpv:
                    ipv4entry.next_hop_group.value = nhgpv.value
                prefixlist.prefix = (pfx)
                prefixlist.ipv4_entry.CopyFrom(ipv4entry)
                gribiop.ipv4.CopyFrom(prefixlist)
            except ValueError as excp:
                return excp

    else:
        raise Exception("Mandatory parameter 'table-name' absent")

    gribiop.id = kwargs.get('operation_id', 1)
    gribioplist = [gribiop]
    gribirequestlist = []
    gribirequestlist.append(prpd.ModifyRequest(operation=gribioplist))
    return prpd.ModifyRequest(operation=gribioplist)

   
