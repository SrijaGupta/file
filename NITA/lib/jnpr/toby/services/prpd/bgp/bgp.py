"""
bgp-api-module
"""

import copy
import jnpr.toby.services.prpd.prpd as prpd# pylint: disable=import-error

def _init(api_list):
    """
    Import the stub files
    """
    prpd.import_api(api_list)


def bgp_init(dev, channel_id, **kwargs):
    """
    Initialize BGP API's.This is must to execute any bgp api call's
    """
    initreq = prpd.BgpRouteInitializeRequest()
    initres = prpd.process_api(dev, channel_id, "BgpRouteInitialize", [initreq, "BgpRoute"])

    return initres


def bgp_route_add(dev, channel_id, **kwargs):
    """
    Add BGP Routes
    """

    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)

    addresult = []
    for i in dest_prefix_iterator:
        if isinstance(kwargs["dest_prefix"], dict):
            dpref_attr = copy.deepcopy(kwargs["dest_prefix"])
            dpref_attr.pop('dest_prefix')
            kwargs["dpref_attr"] = copy.deepcopy(dpref_attr)

        kwargs["dest_prefix"] = i

        updreq = bgp_generate_update_req(**kwargs)
        addres = prpd.process_api(dev, channel_id, "BgpRouteAdd", [updreq, "BgpRoute"])
        addresult.append(addres)
    return  addresult


def bgp_route_modify(dev, channel_id, **kwargs):
    """
    Modify attributes of already added bgp routes.
    BGP routes added by a client can be modified only by same client.
    """

    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)
    modresult = []
    for i in dest_prefix_iterator:
        if isinstance(kwargs["dest_prefix"], dict):
            dpref_attr = copy.deepcopy(kwargs["dest_prefix"])
            dpref_attr.pop('dest_prefix')
            kwargs["dpref_attr"] = copy.deepcopy(dpref_attr)

        kwargs["dest_prefix"] = i

        updreq = bgp_generate_update_req(**kwargs)

        modres = prpd.process_api(dev, channel_id, "BgpRouteModify", [updreq, "BgpRoute"])
        modresult.append(modres)

    return  modresult



def bgp_route_update(dev, channel_id, **kwargs):
    """
    Update attributes of already added bgp routes.BGP routes added by a client can be updated by same client.
    If route is not present, new route will get added.
    """

    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)
    updresult = []
    for i in dest_prefix_iterator:
        if isinstance(kwargs["dest_prefix"], dict):
            dpref_attr = copy.deepcopy(kwargs["dest_prefix"])
            dpref_attr.pop('dest_prefix')
            kwargs["dpref_attr"] = copy.deepcopy(dpref_attr)

        kwargs["dest_prefix"] = i

        updreq = bgp_generate_update_req(**kwargs)

        updres = prpd.process_api(dev, channel_id, "BgpRouteUpdate", [updreq, "BgpRoute"])
        updresult.append(updres)

    return  updresult

def bgp_route_remove(dev, channel_id, **kwargs):
    """
    Remove already added bgp routes.Routes added by a client can be deleted only by same client.
    """

    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)
    remresult = []
    for i in dest_prefix_iterator:
        if isinstance(kwargs["dest_prefix"], dict):
            dpref_attr = copy.deepcopy(kwargs["dest_prefix"])
            dpref_attr.pop('dest_prefix')
            kwargs["dpref_attr"] = copy.deepcopy(dpref_attr)
        kwargs["dest_prefix"] = i

        remreq = bgp_generate_remove_req(**kwargs)

        remres = prpd.process_api(dev, channel_id, "BgpRouteRemove", [remreq, "BgpRoute"])
        remresult.append(remres)
    return remresult


def bgp_route_get(dev, channel_id, **kwargs):
    """
    Get programmed bgp routes or the routes advertised by any bgp peers
    """

    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)

    for i in dest_prefix_iterator:

        if isinstance(kwargs["dest_prefix"], dict):
            dpref_attr = copy.deepcopy(kwargs["dest_prefix"])
            dpref_attr.pop('dest_prefix')
            kwargs["dpref_attr"] = copy.deepcopy(dpref_attr)
        kwargs["dest_prefix"] = i

        getreq = bgp_generate_get_req(**kwargs)
        getres = prpd.process_api(dev, channel_id, "BgpRouteGet", [getreq, "BgpRoute"])

    return  getres

def bgp_generate_update_req(**kwargs):# pylint: disable=too-many-locals,too-many-branches,too-many-statements

    """
    Generate the update request for bgp route add/modify/update
    """

    if 'api_user' in kwargs:
        api_user = kwargs.get('api_user', 'default')
    else:
        api_user = None

    if 'next_hop' in kwargs:
        next_hop = kwargs.get('next_hop')
        if isinstance(next_hop, str):
            next_hop_list = [next_hop]
        elif isinstance(next_hop, list):
            next_hop_list = next_hop
    elif api_user != 'test':
        raise Exception("Next hop is mandatory parameter.")
    else:
        next_hop_list = None

    if 'multi_nh' in kwargs:
        multi_nh = kwargs.get('multi_nh')
    else:
        multi_nh = None

    if 'table' in kwargs:
        table = kwargs.get('table')
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'table' absent")
    else:
        table = None

    if 'dest_prefix' in kwargs:
        dest_prefix = kwargs.get('dest_prefix')
        if isinstance(dest_prefix, str):
            dest_prefix = [dest_prefix]
        elif isinstance(dest_prefix, list):
            dest_prefix = dest_prefix
        elif isinstance(dest_prefix, dict):
            dest_prefix = [dest_prefix]
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'dest_prefix' absent")
    else:
        dest_prefix = None


    if 'prefix_len' in kwargs:
        if isinstance(kwargs["prefix_len"], int):
            prefix_len = kwargs.get('prefix_len')
            if table == 'inet6.0':
                if prefix_len > 128 and api_user != 'test':
                    raise Exception("Prefix length should be <= 128 for inet6")
            elif table == 'inet.0':
                if prefix_len > 32 and api_user != 'test':
                    raise Exception("Prefix length should be <= 32 for inet")
        elif api_user != 'test':
            raise Exception("Please enter integer value for prefix_len")
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'prefix_len' absent")
    else:
        prefix_len = None

#Building the Nexthop for the RIB Route Params

    if 'communities' in kwargs:
        community = kwargs.get('communities')
        if isinstance(community, str):
            community_list = [community, ]
        elif isinstance(community, list):
            community_list = community
    elif api_user == 'test':
        community_list = prpd.CommunityList(com_list=None)
    else:
        community_list = None

    if 'cluster_id' in kwargs:
        clusterid = kwargs.get('cluster_id')
        num_clusterid = prpd.ip_to_uint32(clusterid)
        cluster = prpd.BgpAttrib32(value=num_clusterid)
    else:
        cluster = None

    if 'originator_id' in kwargs:
        originatorid = kwargs.get('originator_id')
        num_originatorid = prpd.ip_to_uint32(originatorid)
        originator = prpd.BgpAttrib32(value=num_originatorid)
    else:
        originator = None

    if 'route_preference' in kwargs:
        route_preference = kwargs.get('route_preference')
        route_preference = int(route_preference)
        route_pref = prpd.BgpAttrib32(value=route_preference)
    else:
        route_pref = None

    if 'local_preference' in kwargs:
        local_preference = kwargs.get('local_preference')
        local_preference = int(local_preference)
        local_pref = prpd.BgpAttrib32(value=local_preference)
    else:
        local_pref = None

    if 'med' in kwargs:
        med = kwargs.get('med')
        med = int(med)
        bgpmd = prpd.BgpAttrib32(value=med)
    else:
        bgpmd = None

    if 'aspath' in kwargs:
        aspath = kwargs.get('aspath')
        as_path = prpd.AsPath(aspath_string=aspath)
    elif api_user == 'test':
        as_path = prpd.AsPath(aspath_string=None)
    else:
        as_path = None

    if 'vpn_label' in kwargs:
        vpnlabel = kwargs.get('vpn_label')
        vpnlabel = int(vpnlabel)
    elif table is 'bgp.l3vpn.0' or table is 'bgp.l3vpn-inet6.0' and api_user != 'test':
        raise Exception("Mandatory parameter 'label' absent")
    else:
        vpnlabel = None

    if 'route_type' in kwargs:
        rt_type = kwargs.get('route_type')
        rt_type = int(rt_type)
    else:
        rt_type = None

    if 'path_cookie' in kwargs:
        pathcookie = kwargs.get('path_cookie')
        pathcookie = int(pathcookie)
    else:
        pathcookie = None

    if  'routedata' in kwargs and isinstance(kwargs['routedata'], dict):
        routedata = kwargs.get('routedata')
    elif table == 'bgp.inetsrte.0' or table == 'bgp.inet6srte.0' and api_user != 'test' and table == 'inetflow.0' and table == 'inet6flow.0':
        raise Exception("Mandatory parameter 'routedata' is absent")
    else:
        routedata = None

    if 'dpref_attr' in kwargs and isinstance(kwargs['dpref_attr'], dict):
        dpref_attr = kwargs["dpref_attr"]
    else:
        dpref_attr = {}

    routelist = list()

    for destprefix in dest_prefix:
        routeparams = prpd.BgpRouteEntry()
        if destprefix is not None and table is not None and prefix_len is not None and api_user != 'test':
            if isinstance(dpref_attr, dict) and api_user != 'test' and 'table' in destprefix and dpref_attr is not None:
                dest_table = destprefix['table']
            else:
                dest_table = table
            dpref_attr["dest_prefix"] = destprefix
            dprefix = prefix_gen(dest_table, dpref_attr, api_user)
            routeparams.dest_prefix.CopyFrom(dprefix)
        if table is not None and api_user != 'test':
            table_name = prpd.RouteTable(rtt_name=prpd.RouteTableName(name=table))
            routeparams.table.CopyFrom(table_name)
        if prefix_len is not None and api_user != 'test':
            routeparams.dest_prefix_len = prefix_len
        if next_hop_list is not None and api_user != 'test':
            nhlist = []
            if multi_nh is not None:
                for bgpnh in next_hop_list:
                    nhlist.append(prpd.IpAddress(addr_string=bgpnh))
            elif len(dest_prefix) == len(next_hop_list):
                nhlist.append(prpd.IpAddress(addr_string=next_hop_list.pop(0)))
            else:
                single_nh = []
                single_nh.append(next_hop_list.pop(0))
                next_hop_list.append(single_nh[0])
                nhlist.append(prpd.IpAddress(addr_string=single_nh[0]))

            routeparams.protocol_nexthops.extend(nhlist)
        if routedata is not None and api_user != 'test':
            routeparams.route_data.CopyFrom(routedatagen(routedata, table, api_user))
        if local_pref is not None and api_user != 'test':
            routeparams.local_preference.CopyFrom(local_pref)
        if route_pref is not None and api_user != 'test':
            routeparams.route_preference.CopyFrom(route_pref)
        if bgpmd is not None and api_user != 'test':
            routeparams.med.CopyFrom(bgpmd)
        if as_path is not None and api_user != 'test':
            routeparams.aspath.CopyFrom(as_path)
        if community_list is not None and api_user != 'test':
            cm_list = []
            len_comm = len(community_list)
            for i in range(0, len_comm):
                comm = prpd.Community(community_string=community_list[i])
                cm_list.append(comm)
            c_list = prpd.CommunityList(com_list=cm_list)
            routeparams.communities.CopyFrom(c_list)
        if cluster is not None and api_user != 'test':
            routeparams.cluster_id.CopyFrom(cluster)
        if originator is not None and api_user != 'test':
            routeparams.originator_id.CopyFrom(originator)
        if vpnlabel is not None and api_user != 'test':
            routeparams.vpn_label = vpnlabel
        if rt_type is not None and api_user != 'test':
            routeparams.route_type = rt_type
        if pathcookie is not None and api_user != 'test':
            routeparams.path_cookie = pathcookie
        routelist.append(routeparams)
    updreq = prpd.BgpRouteUpdateRequest(bgp_routes=routelist)
    return updreq


def  prefix_gen(dest_table, prefix, api_user,prefix_type=None):
    """
    Generate prefix based on table
    """
    if dest_table == 'inet.0':
        if prefix_type == 'bgp_lu':
            destpfx = prpd.RoutePrefix(labeled_inet=prpd.IpAddress(addr_string=prefix["dest_prefix"]))
        else:
            destpfx = prpd.RoutePrefix(inet=prpd.IpAddress(addr_string=prefix["dest_prefix"]))
    elif dest_table == 'inet6.0':
        if prefix_type == 'bgp_lu':
            destpfx = prpd.RoutePrefix(labeled_inet6=prpd.IpAddress(addr_string=prefix["dest_prefix"]))
        else:
            destpfx = prpd.RoutePrefix(inet6=prpd.IpAddress(addr_string=prefix["dest_prefix"]))
    elif dest_table == "bgp.l3vpn.0" or dest_table == "bgp.l3vpn-inet6.0":
        destpfx = bgpvpnprefix(dest_table, prefix, api_user)
    elif dest_table == "bgp.inetsrte.0" or dest_table == "bgp.inet6srte.0":
        destpfx = bgpsrteprefix(dest_table, prefix, api_user)
    elif dest_table == "inetflow.0" or dest_table == "inet6flow.0":
        destpfx = bgpflowprefix(dest_table, prefix, api_user)
    else:
        destpfx = None
    return destpfx

def bgpvpnprefix(dest_table, prefix, api_user):
    """
    Generate bgp vpn prefix
    """
    if 'dest_prefix' in prefix:
        dprefix = prefix.get('dest_prefix')
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'dest_prefix' absent")
    else:
        dprefix = None

    if 'rd_type' in prefix:
        rdtype = prefix.get('rd_type')
        rdtype = int(rdtype)
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'rd_type' absent for bgp vpn route ")
    else:
        rdtype = None

    if 'as_number' in prefix:
        asnum = prefix.get('as_number')
        asnum = int(asnum)
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'as_number' absent for bgp vpn route")
    else:
        asnum = None

    if 'assigned_number' in prefix:
        asgnd_number = prefix.get('assigned_number')
        asgnd_number = int(asgnd_number)
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'assigned_number' absent for bgp vpn route")
    else:
        asgnd_number = None

    if 'ipaddress' in prefix and rdtype == 1:
        ipaddress = prefix.get('ipaddress')
    elif api_user != 'test' and rdtype == 1:
        raise Exception("Mandatory parameter 'ipaddress' absent for bgp vpn route")
    else:
        ipaddress = None

    if rdtype is None and api_user == 'test':
        bgprd = prpd.RouteDistinguisher()
    else:
        if rdtype == 0:
            if asnum is None or asgnd_number is None and api_user == 'test':
                bgprd = prpd.RouteDistinguisher(rd0=prpd.RdType0())
            else:
                bgprd = prpd.RouteDistinguisher(rd0=prpd.RdType0(as_number=asnum, assigned_number=asgnd_number))
        if rdtype == 1:
            if ipaddress is None or asgnd_number is None and api_user == 'test':
                bgprd = prpd.RouteDistinguisher(rd1=prpd.RdType1())
            else:
                bgprd = prpd.RouteDistinguisher(rd1=prpd.RdType1(ip_address=prpd.IpAddress(addr_string=ipaddress), assigned_number=asgnd_number))
        if rdtype == 2:
            if asnum is None or asgnd_number is None and api_user == 'test':
                bgprd = prpd.RouteDistinguisher(rd2=prpd.RdType2())
            else:
                bgprd = prpd.RouteDistinguisher(rd2=prpd.RdType2(as_number=asnum, assigned_number=asgnd_number))
        vpn_address = prpd.L3vpnAddress(rd=bgprd, vpn_addr=prpd.IpAddress(addr_string=dprefix))
        if dest_table == "bgp.l3vpn.0":
            vpnpfx = prpd.RoutePrefix(inetvpn=vpn_address)
        if dest_table == "bgp.l3vpn-inet6.0":
            vpnpfx = prpd.RoutePrefix(inet6vpn=vpn_address)
    return vpnpfx

def bgpsrteprefix(dest_table, prefix, api_user):
    """
    Generate bgp srte prefix
    """
    if 'dest_prefix' in prefix:
        pfx = prefix.get('dest_prefix')
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'prefix' absent for bgp srte route")
    else:
        pfx = None
    if 'sr_color' in prefix:
        srcolor = prefix.get('sr_color')
        srcolor = int(srcolor)
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'sr_color' absent for bgp srte route")
    else:
        srcolor = None

    if 'sr_distinguisher' in prefix:
        srdistinguisher = prefix.get('sr_distinguisher')
        srdistinguisher = int(srdistinguisher)
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'sr_distinguisher' absent for bgp srte route")
    else:
        srdistinguisher = None

    srteaddr = prpd.SRTEAddress()
    if pfx is not None and api_user != 'test':
        sraddr = prpd.IpAddress(addr_string=(pfx))
        srteaddr.destination.CopyFrom(sraddr)
    if srcolor is None and api_user == 'test':
        srteaddr.sr_color = prpd.SRTEColor()
    else:
        srteaddr.sr_color.CopyFrom(prpd.SRTEColor(color=srcolor))
    if srdistinguisher is None and api_user == 'test':
        srteaddr.sr_distinguisher = prpd.SRTEDistinguisher()
    else:
        srteaddr.sr_distinguisher.CopyFrom(prpd.SRTEDistinguisher(distinguisher=srdistinguisher))
    if dest_table == "bgp.inetsrte.0":
        srteprefix = prpd.RoutePrefix(inet_srte_policy=srteaddr)
    elif dest_table == "bgp.inet6srte.0":
        srteprefix = prpd.RoutePrefix(inet6_srte_policy=srteaddr)
    return srteprefix

def bgpflowprefix(dest_table, prefix, api_user):
    """
    Generate bgp flow spec prefix
    """
    if 'dest_prefix' in prefix:
        dest_pfx = prefix.get('dest_prefix')
    else:
        dest_pfx = None
    if 'dest_len' in prefix:
        dlen = prefix.get('dest_len')
    else:
        dlen = None
    if 'src_prefix' in prefix:
        src_pfx = prefix.get('src_prefix')
    else:
        src_pfx = None
    if 'src_len' in prefix:
        slen = prefix.get('src_len')
    else:
        slen = None

    if 'protocols' in prefix:
        protocols = prefix.get('protocols')
        if isinstance(protocols, str):
            protocols = [protocols]
        elif isinstance(protocols, (list)):
            protocols = protocols

    else:
        protocols = None

    if 'ports' in prefix:
        ports = prefix.get('ports')
        if isinstance(ports, str):
            ports = [ports, ]
        elif isinstance(ports, (list)):
            ports = ports
    else:
        ports = None

    flspec_addr = prpd.FlowspecAddress()
    if dest_pfx is not None and dlen is not None and api_user != 'test':
        flspec_addr.destination.addr_string = dest_pfx
        flspec_addr.dest_prefix_len = dlen
    if src_pfx is not None and slen is not None and api_user != 'test':
        flspec_addr.source.addr_string = src_pfx
        flspec_addr.source_prefix_len = slen
    if protocols != None:
        protorange = numrangelist(protocols)
        flspec_addr.ip_protocols.range_list.extend(protorange.range_list)
    if ports != None:
        ports = numrangelist(ports)
        flspec_addr.ports.range_list.extend(ports.range_list)

    if dest_table == "inetflow.0":
        flspec_prefix = prpd.RoutePrefix(inet_flowspec=flspec_addr)
    elif dest_table == "inet6flow.0":
        flspec_prefix = prpd.RoutePrefix(inet6_flowspec=flspec_addr)
    return flspec_prefix

def numrangelist(narr):
    """
    Assign port/proto list
    """
    nlist = list()
    cnt = 0
    for i in range(len(narr)):
        if cnt % 2:
            nrange = prpd.NumericRange(min=narr[cnt-1], max=narr[cnt])
            nlist.append(nrange)
        cnt = cnt + 1
        i = i
    nrangelist = prpd.NumericRangeList(range_list=nlist)
    return nrangelist

def routedatagen(routedata, table, api_user):
    """
    Generate route data for srte or flow routes
    """
    if table == 'bgp.inetsrte.0' or table == 'bgp.inet6srte.0':
        srrdata = bgpsrteroutedata(routedata, api_user)
        rdata = prpd.AddressFamilySpecificData(srte_policy_data=srrdata)
    if table == 'inetflow.0' or table == 'inet6flow.0':
        flowrdata = flowroutedata(routedata, api_user)
        rdata = prpd.AddressFamilySpecificData(flowspec_data=flowrdata)
    return rdata

def bgpsrteroutedata(routedatavalue, api_user):# pylint: disable=too-many-locals
    """
    Generate bgp srte route data
    """
    if 'segment_lists' in routedatavalue:
        segment_lists = routedatavalue.get('segment_lists')
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'segment_list' absent for bgp srte route")
    else:
        segment_lists = None

    if 'sr_preference' in routedatavalue:
        srpreference = routedatavalue.get('sr_preference')
        srpreference = int(srpreference)
    else:
        srpreference = None

    if 'binding_sid' in routedatavalue:
        bsidlabel = routedatavalue.get('binding_sid')
    else:
        bsidlabel = None

    srterdata = prpd.SRTERouteData()
    if segment_lists is not None and api_user != 'test':
        s_list = []
        for seglist in segment_lists:
            srteslist = prpd.SRTESegmentList()
            if seglist.get('weight') is not None:
                srteslist.weight = seglist.get('weight')
            if seglist.get('segment_entries') is not None:
                sentry_list = []
                for s_entry_dict in seglist.get('segment_entries'):
                    srteseg = prpd.SRTESegment()
                    segtype = prpd.SegmentType1()
                    lentry = label_gen(s_entry_dict)
                    segtype.sid_label_entry.CopyFrom(lentry)
                    srteseg.segment_type1.CopyFrom(segtype)
                    sentry_list.append(srteseg)
                srteslist.segments.extend(sentry_list)
            s_list.append(srteslist)
        srterdata.segment_lists.extend(s_list)
    if srpreference is not None:
        srterdata.preference = srpreference
    if bsidlabel is not None:
        srtebsid = prpd.SRTEBindingSID()
        sentry = prpd.SidEntry()
        blentry = label_gen(bsidlabel)
        sentry.sid_label_entry.CopyFrom(blentry)
        srtebsid.binding_sr_id.CopyFrom(sentry)
        srterdata.binding_sid.CopyFrom(srtebsid)
    return srterdata

def label_gen(labelentry):
    """
    Generate label
    """
    lentry = prpd.LabelEntry()
    if labelentry.get('label') is not None:
        lentry.label = labelentry.get('label')
    if labelentry.get('traffic_class') is not None:
        lentry.traffic_class = labelentry.get('traffic_class')
    if labelentry.get('ttl') is not None:
        lentry.ttl = labelentry.get('ttl')
    if labelentry.get('bottom_of_stack') is not None:
        lentry.bottom_of_stack = labelentry.get('bottom_of_stack')
    return lentry

def flowroutedata(routedatavalue, api_user):
    """
    Generate flow route data
    """
    if 'rate_limit' in routedatavalue:
        rate_limit = routedatavalue.get('rate_limit')
    else:
        rate_limit = None
    if 'discard' in routedatavalue:
        discard = routedatavalue.get('discard')
    else:
        discard = None
    if 'mark_dscp' in routedatavalue:
        mark_dscp = routedatavalue.get('mark_dscp')
    else:
        mark_dscp = None
    if 'redirect_to_vrf' in routedatavalue:
        redirect_to_vrf = routedatavalue.get('redirect_to_vrf')
    else:
        redirect_to_vrf = None
    if 'sample' in routedatavalue:
        sample = routedatavalue.get('sample')
    else:
        sample = None

    flow_rdata = prpd.FlowspecRouteData()
    if rate_limit is not None and api_user != 'test':
        flow_rdata.rate_limit_val = rate_limit
    if discard is not None and api_user != 'test':
        flow_rdata.discard = discard
    if mark_dscp is not None and api_user != 'test':
        flow_rdata.mark_dscp = mark_dscp
    if redirect_to_vrf is not None and api_user != 'test':
        flow_rdata.redirect_inst_rt_comm = redirect_to_vrf
    if sample is not None and api_user != 'test':
        flow_rdata.sample = sample

    return flow_rdata

def bgp_generate_remove_req(**kwargs):
    """
    Generate remove request
    """
    if 'api_user' in kwargs:
        api_user = kwargs.get('api_user', 'default')
    else:
        api_user = None
    if 'orlonger' in kwargs and api_user != 'test':
        orlonger = kwargs.get('orlonger')
    else:
        orlonger = None

    remlist = bgp_generate_route_match(**kwargs)

    remreq = prpd.BgpRouteRemoveRequest()
    if remlist is not None:
        remreq.bgp_routes.extend(remlist)
    if orlonger is not None and api_user != 'test':
        remreq.or_longer = orlonger

    return remreq

def bgp_generate_get_req(**kwargs):
    """
    Generate get request
    """
    if 'api_user' in kwargs:
        api_user = kwargs.get('api_user', 'default')
    else:
        api_user = None

    if 'orlonger' in kwargs and api_user != 'test':
        orlonger = kwargs.get('orlonger')
        orlonger = int(orlonger)
    else:
        orlonger = None

    if 'active_only' in kwargs and api_user != 'test':
        activeroutes = kwargs.get('active_only')
    else:
        activeroutes = None

    if 'route_count' in kwargs and api_user != 'test':
        routecnt = kwargs.get('route_count')
    else:
        routecnt = None

    if 'reply_address_format' in kwargs and api_user != 'test':
        addrformat = kwargs.get('reply_address_format')
    else:
        addrformat = None

    if 'reply_table_format' in kwargs and api_user != 'test':
        tableformat = kwargs.get('reply_table_format')
    else:
        tableformat = None

    getentry = bgp_generate_route_match(**kwargs)

    bgproutegetreq = prpd.BgpRouteGetRequest()
    if getentry is not None and api_user != 'test':
        bgproutegetreq.bgp_route.CopyFrom(getentry[0])
    if orlonger is not None and api_user != 'test':
        bgproutegetreq.or_longer = orlonger
    if activeroutes is not None and api_user != 'test':
        bgproutegetreq.active_only = activeroutes
    if routecnt is not None and api_user != 'test':
        bgproutegetreq.route_count = routecnt
    if addrformat is not None and api_user != 'test':
        bgproutegetreq.reply_address_format = addrformat
    if tableformat is not None and api_user != 'test':
        bgproutegetreq.reply_table_format = tableformat

    return  bgproutegetreq


def bgp_generate_route_match(**kwargs):# pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """
    Generate route match for get and remove
    """
    if 'api_user' in kwargs:
        api_user = kwargs.get('api_user', 'default')
    else:
        api_user = None
    if 'table' in kwargs:
        table = kwargs.get('table')
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'table' absent")
    else:
        table = None

    if 'dest_prefix' in kwargs:
        dest_prefix = kwargs.get('dest_prefix')
        if isinstance(dest_prefix, str):
            dest_prefix = [dest_prefix]
        elif isinstance(dest_prefix, list):
            dest_prefix = dest_prefix
        elif isinstance(dest_prefix, dict):
            dest_prefix = [dest_prefix]
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'dest_prefix' absent")
    else:
        dest_prefix = None

    if 'prefix_len' in kwargs:
        if isinstance(kwargs["prefix_len"], int):
            prefix_len = kwargs.get('prefix_len')
            if table == 'inet6.0':
                if prefix_len > 128 and api_user != 'test':
                    raise Exception("Prefix length should be <= 128 for inet6")
            elif table == 'inet.0':
                if prefix_len > 32 and api_user != 'test':
                    raise Exception("Prefix length should be <= 32 for inet")
        elif api_user != 'test':
            raise Exception("Please enter integer value for prefix_len")
    elif api_user != 'test':
        raise Exception("Mandatory parameter 'prefix_len' absent")
    else:
        prefix_len = 0

    if 'path_cookie' in kwargs and api_user != 'test':
        pathcookie = kwargs.get('path_cookie')
        pathcookie = int(pathcookie)
    else:
        pathcookie = None

    if 'protocol' in kwargs and api_user != 'test':
        protocol = kwargs.get('protocol')
        protocol = int(protocol)
    else:
        protocol = None

    if 'communities' in kwargs:
        community = kwargs.get('communities')
        if isinstance(community, str):
            community_list = [community]
        elif isinstance(community, list):
            community_list = community
    elif api_user == 'test':
        community_list = prpd.CommunityList(com_list=None)
    else:
        community_list = None

    if 'dpref_attr' in kwargs and isinstance(kwargs['dpref_attr'], dict):
        dpref_attr = kwargs["dpref_attr"]
    else:
        dpref_attr = {}

    prefix_type = kwargs.get('prefix_type',None)
    
    routelist = []


    for destprefix in dest_prefix:
        routeparams = prpd.BgpRouteMatch()
        if destprefix is not None and table is not None and prefix_len is not None and api_user != 'test':
            if isinstance(dpref_attr, dict) and api_user != 'test' and 'table' in destprefix and dpref_attr is not None:
                dest_table = destprefix['table']
            else:
                dest_table = table
            dpref_attr["dest_prefix"] = destprefix
            dprefix = prefix_gen(dest_table, dpref_attr, api_user, prefix_type)
            routeparams.dest_prefix.CopyFrom(dprefix)
        if table is not None and api_user != 'test':
            table_name = prpd.RouteTable(rtt_name=prpd.RouteTableName(name=table))
            routeparams.table.CopyFrom(table_name)
        if prefix_len is not None and api_user != 'test':
            routeparams.dest_prefix_len = prefix_len
        if pathcookie is not None and api_user != 'test':
            routeparams.path_cookie = pathcookie
        if community_list is not None and api_user != 'test':
            cm_list = []
            len_comm = len(community_list)
            for i in range(0, len_comm):
                comm = prpd.Community(community_string=community_list[i])
                cm_list.append(comm)
            c_list = prpd.CommunityList(com_list=cm_list)
            routeparams.communities.CopyFrom(c_list)
        if protocol is not None and api_user != 'test':
            routeparams.protocol = protocol
        routelist.append(routeparams)

    return routelist

def bgp_monitor_register(dev, channel_id, **kwargs):
    """
    BGP monitor register for monitoring bgp routes advertised by a peer and having import policy configured with analyze.
    """
    if 'api_user' in kwargs:
        api_user = kwargs.get('api_user', 'default')
    else:
        api_user = None

    if 'route_count' in kwargs and api_user != 'test':
        routecnt = kwargs.get('route_count')
    else:
        routecnt = None

    if 'reply_address_format' in kwargs and api_user != 'test':
        addrformat = kwargs.get('reply_address_format')
    else:
        addrformat = None

    if 'reply_table_format' in kwargs and api_user != 'test':
        tableformat = kwargs.get('reply_table_format')
    else:
        tableformat = None

    monitorreq = prpd.BgpRouteMonitorRegisterRequest()
    if addrformat is not None and api_user != 'test':
        monitorreq.reply_address_format = addrformat
    if tableformat is not None and api_user != 'test':
        monitorreq.reply_table_format = tableformat
    if routecnt is not None and api_user is not 'test':
        monitorreq.route_count = routecnt

    monitor_stream = prpd.process_api(dev, channel_id, "BgpRouteMonitorRegister", [monitorreq, "Bgp"])

    return monitor_stream

def bgp_monitor_unregister(dev, channel_id):
    """
    BGP monitor unregister to stop monitoring
    """

    monitorreq = prpd.BgpRouteMonitorUnregisterRequest()
    monitor_unreg_reply = prpd.process_api(dev, channel_id, "BgpRouteMonitorUnregister", [monitorreq, "Bgp"])

    return monitor_unreg_reply
