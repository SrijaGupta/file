"""
rib-api-module
"""
from google.protobuf import wrappers_pb2
import builtins
import logging
import jnpr.toby.services.prpd.prpd as prpd # pylint: disable=import-error
from jnpr.toby.exception.toby_exception import TobyException


def _init(api_list):
    """
    DOcs
    """
    prpd.import_api(api_list)


def rib_route_initialize(dev, channel_id, **kwargs):
    """
    Route Initialize
    """
    initreq = prpd.RouteInitializeRequest()

    default_preferences0 = kwargs.get('default_preferences0', None)
    default_preferences1 = kwargs.get('default_preferences1', None)

    if default_preferences1 is not None:
        initreq.default_preferences[1].CopyFrom(route_attribute(default_preferences1))

    if default_preferences0 is not None:
        initreq.default_preferences[0].CopyFrom(route_attribute(default_preferences0))

    initreq.default_response_address_format = kwargs.get('response_address_format', 0)


    initrep = prpd.process_api(dev, channel_id, "RouteInitialize", [initreq, "jnx_Rib"])

    return initrep


def rib_route_cleanup(dev, channel_id, **kwargs):
    """
    Route cleanup
    """
    initreq = prpd.RouteCleanupRequest()
    initrep = prpd.process_api(dev, channel_id, "RouteCleanup", [initreq, "jnx_Rib"], kwargs.get("timeout", None))
    return initrep


def rib_route_add(dev, channel_id, **kwargs):
    """
    Add static routes
    """

    result = []
    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)

    for i in dest_prefix_iterator:
        kwargs["dest_prefix"] = i

        updreq = rib_generate_update_req(**kwargs)
        result.append(prpd.process_api(dev, channel_id, "RouteAdd", [updreq, "jnx_Rib"], kwargs.get("timeout", None)))

    return  result


def rib_route_modify(dev, channel_id, **kwargs):
    """
    Modify attributes in already added static routes
    """
    result = []
    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)

    for i in dest_prefix_iterator:
        kwargs["dest_prefix"] = i

        updreq = rib_generate_update_req(**kwargs)

        result.append(prpd.process_api(dev, channel_id, "RouteModify", [updreq, "jnx_Rib"], kwargs.get("timeout", None)))


    return  result


def rib_route_update(dev, channel_id, **kwargs):
    """
    Update attributes in already added static routes
    add new route if the route is not present already
    """
    result = []
    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)

    for i in dest_prefix_iterator:
        kwargs["dest_prefix"] = i

        updreq = rib_generate_update_req(**kwargs)

        result.append(prpd.process_api(dev, channel_id, "RouteUpdate", [updreq, "jnx_Rib"], kwargs.get("timeout", None)))

    return  result

def rib_generate_update_req(**kwargs): # pylint: disable=too-many-locals
    """
    Update request method common for add/modify/update
    """


    if 'table' in kwargs:
        table = kwargs.get('table')
    else:
        raise Exception("Mandatory parameter 'table' absent")


    if 'dest_prefix' in kwargs:
        dest_prefix = kwargs.get('dest_prefix')
        if isinstance(kwargs["dest_prefix"], str):
            dest_prefix = [kwargs["dest_prefix"], ]
        elif isinstance(kwargs["dest_prefix"], list):
            dest_prefix = kwargs["dest_prefix"]
    else:
        raise Exception("Mandatory parameter 'destination_prefix' absent")


    if 'prefix_len' in kwargs:
        if isinstance(kwargs["prefix_len"], int):
            prefix_len = kwargs.get('prefix_len')
            if 'inet6' in table:
                if prefix_len > 128:
                    raise Exception("Prefix length should be <= 128 for inet6")
            elif 'inet.0' in table:
                if prefix_len > 32:
                    raise Exception("Prefix length should be <= 32 for inet")
            else:
                if prefix_len > 52:
                    raise Exception("Prefix length should be <= 52 for inet")
        else:
            raise Exception("Please enter integer value for prefix_len")
    else:
        raise Exception("Mandatory parameter 'prefix_length' absent")

    ecmp = kwargs.get("ecmp", False)


    if 'next_hop' in kwargs:
        if isinstance(kwargs["next_hop"], str):
            next_hop_list = [kwargs["next_hop"], ]
        elif isinstance(kwargs["next_hop"], list):
            next_hop_list = kwargs["next_hop"]
            if isinstance(next_hop_list[0], list):
                for i in range(0, len(next_hop_list)):
                    if len(next_hop_list[i]) > 513 and ecmp is True:
                        raise Exception("Next hop is limit exceeded with more than 512 nexthops for ecmp")
            elif len(next_hop_list) > 513 and ecmp is True:
                raise Exception("Next hop is limit exceeded with more than 512 nexthops for ecmp")
    else:
        raise Exception("Next hop is mandatory parameter.")

    #Removed deepcopy for enabling next_hop_list rotation via pop()
    #next_hop_list = prpd.deepcopy(next_hop_list)

    routelist = list()


    for index in range(0, len(dest_prefix)):
        #Building the Key for RIB Route Params


        if 'inet6' in table:
            destprefix = prpd.NetworkAddress(inet6=prpd.IpAddress(addr_string=dest_prefix[index]))

        else:

            if 'mpls' in table:
                destprefix = prpd.NetworkAddress(mpls=prpd.MplsAddress(label=int(dest_prefix[index])))

            else:

                destprefix = prpd.NetworkAddress(inet=prpd.IpAddress(addr_string=dest_prefix[index]))

        route_table = prpd.RouteTable(name=prpd.RouteTableName(name=table))
        route_match_field = prpd.RouteMatch(dest_prefix=destprefix, dest_prefix_len=prefix_len, table=route_table)


        if 'cookie' in kwargs:
            if isinstance(kwargs["cookie"], int):
                route_match_field.cookie = kwargs.get('cookie')

        # Update: Below code is handled in rib_nexthop
        # Calculating nexthop for below scenarios
        # ecmp is None
        # Only single nexthop is provided
#         if len(next_hop_list) >= 1 and ecmp is not True:
#
#
#             single_nh = []
#             single_nh.append(next_hop_list.pop(0))
#             next_hop_list.append(single_nh[0])
#
#             nh_list = rib_nexthop(single_nh, **kwargs)
#
# #         elif len(next_hop_list) == 1 and ecmp is not True:
# #
# #             single_nh = []
# #             single_nh.append(next_hop_list.pop(0))
# #             next_hop_list.append(single_nh[0])
# #
# #             nh_list = rib_nexthop(single_nh, **kwargs)
#
#         elif ecmp == True and skip_rib_nexthop == False:

        nh_list = rib_nexthop(**kwargs)
                #skip_rib_nexthop = True
                # Commented above line to provide support for unique label stack
                # for each prefix

        routeparams = prpd.RouteEntry()

        attributes = 0
        # Added second if loop as pylint throws error for too many conditions in single if
        if 'preferences0' in kwargs or 'preferences1' in kwargs or 'colors0' in kwargs or 'no_advertise' in kwargs:

            rtattr = prpd.RouteAttributes()
            if 'preferences0' in kwargs:
                rtattr.preferences[0].CopyFrom(route_attribute(kwargs.get('preferences0')))

            if 'preferences1' in kwargs:
                rtattr.preferences[1].CopyFrom(route_attribute(kwargs.get('preferences1')))

            if 'colors0' in kwargs:
                rtattr.colors[0].CopyFrom(route_attribute(kwargs.get('colors0')))

            if 'no_advertise' in kwargs:
                rtattr.no_advertise = kwargs.get('no_advertise')
            attributes = 1


        if 'colors1' in kwargs or 'tags0' in kwargs or 'tags1' in kwargs or attributes == 1:

            if attributes == 0:
                rtattr = prpd.RouteAttributes()

            if 'colors1' in kwargs:
                rtattr.colors[1].CopyFrom(route_attribute(kwargs.get('colors1')))

            if 'tags0' in kwargs:
                rtattr.tags[0].CopyFrom(route_attribute(kwargs.get('tags0')))

            if 'tags1' in kwargs:
                rtattr.tags[1].CopyFrom(route_attribute(kwargs.get('tags1')))

            routeparams.attributes.CopyFrom(rtattr)

        routeparams.key.CopyFrom(route_match_field)
        routeparams.nexthop.CopyFrom(nh_list)

        routelist.append(routeparams)

    updreq = prpd.RouteUpdateRequest(routes=routelist)

    return updreq


def route_attribute(attribute):

    """
    DOcs
    """
    attribute_obj = wrappers_pb2.UInt32Value()
    attribute_obj.value = attribute

    return attribute_obj

def rib_route_remove(dev, channel_id, **kwargs):
    """
    delete already added static routes using execute_prpd_api.
    ** ONLY THE ROUTES ADDED BY A UNIQUE client_id CAN BE REMOVED
    """
    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)

    if 'table' in kwargs:
        table = kwargs.get('table')

    if 'prefix_len' in kwargs:
        prefix_len = kwargs.get('prefix_len')


    result = []
    for i in dest_prefix_iterator:
        dest_prefix = i



        rtkeys = []

        for index in range(0, len(dest_prefix)):
           #Building the Key for RIB Route Params

            if 'inet6' in table:
                destprefix = prpd.NetworkAddress(inet6=prpd.IpAddress(addr_string=dest_prefix[index]))
            else:
                if 'mpls' in table:
                    destprefix = prpd.NetworkAddress(mpls=prpd.MplsAddress(label=int(dest_prefix[index])))
                else:
                    destprefix = prpd.NetworkAddress(inet=prpd.IpAddress(addr_string=dest_prefix[index]))


            tablename = prpd.RouteTable(name=prpd.RouteTableName(name=table))

            route_match_field = prpd.RouteMatch(dest_prefix=destprefix, dest_prefix_len=prefix_len, table=tablename)

            if 'cookie' in kwargs:
                if isinstance(kwargs["cookie"], int):
                    route_match_field.cookie = kwargs.get('cookie')

            rtkeys.append(route_match_field)

        remreq = prpd.RouteDeleteRequest(keys=rtkeys)
        result.append(prpd.process_api(dev, channel_id, "RouteDelete", [remreq, "jnx_Rib"], kwargs.get("timeout", None)))

    return  result



def rib_route_get(dev, channel_id, **kwargs):
    """
    To fetch routes present in the rib
    """

    dest_prefix_iterator = prpd.dest_prefix_limiter(**kwargs)


    if 'table' in kwargs:
        table = kwargs.get('table')

    else:
        raise Exception("Mandatory parameter 'table' absent")


    if 'prefix_len' in kwargs:

        if isinstance(kwargs["prefix_len"], int):
            prefix_len = kwargs.get('prefix_len')
            if 'inet6' in table:
                if prefix_len > 128:
                    raise Exception("Prefix length should be <= 128 for inet6")
            else:
                if prefix_len > 32:
                    raise Exception("Prefix length should be <= 32 for inet")
        else:
            raise Exception("Please enter integer value for prefix_len")

    else:
        raise Exception("Mandatory parameter 'prefix_len' absent")



    count = kwargs.get('route_count', 1000)


    if 'dest_prefix' in kwargs:
        dest_prefix = kwargs.get('dest_prefix')
    else:
        raise Exception("Mandatory parameter 'destination_prefix' absent")

    route_match_type = kwargs.get('route_match_type', prpd.BEST)



    if 'inet6' in table:
        destprefix = prpd.NetworkAddress(inet6=prpd.IpAddress(addr_string=dest_prefix))
    else:
        destprefix = prpd.NetworkAddress(inet=prpd.IpAddress(addr_string=dest_prefix))

    tablename = prpd.RouteTable(name=prpd.RouteTableName(name=table))

    route_match_field = prpd.RouteMatch(dest_prefix=destprefix, dest_prefix_len=prefix_len, table=tablename)


    if 'cookie' in kwargs:
        route_match_field.cookie = kwargs.get('cookie')

    #Defining the RouteGetRequest Structure
    getreq = prpd.RouteGetRequest(key=route_match_field, match_type=route_match_type, route_count=count)

    if 'active_routes' in kwargs:
        if kwargs['active_routes'].upper() == 'TRUE':
            getreq.active_only = True

    getreply = prpd.process_api(dev, channel_id, "RouteGet", [getreq, "jnx_Rib"], kwargs.get("timeout", None))


    return  getreply


def rib_route_monitor(dev, channel_id, **kwargs):
    """
    To monitor the routes in Junos rib.
    """
    if 'table' in kwargs:
        table = kwargs.get('table')
        tablename = prpd.RouteTableName(name=table)
    else:
        raise Exception("Mandatory parameter 'table' absent")

    if 'monitor_operation' in kwargs:
        monitor_operation = kwargs.get('monitor_operation')
    else:
        raise Exception("Mandatory parameter 'monitor_operation' absent")

    policy = kwargs.get('policy', 'export_static')

    monitor_context = int(kwargs.get('monitor_context', 100))

    monitor_reply_count = int(kwargs.get('route_count', 1))

    fl_flag = prpd.RouteSubscribeFlags(no_eor_to_client=1)
    route_policy_name = prpd.RouteSubscribePolicy(policy=policy)

    if  monitor_operation == 'SUBSCRIBE_ADDD':
        flashreq = prpd.RouteSubscribeRequest(table_name=tablename, operation=monitor_operation, flag=fl_flag,\
                                           route_count=monitor_reply_count, policy=route_policy_name, context=monitor_context)

    else:
        flashreq = prpd.RouteSubscribeRequest(table_name=tablename, operation=monitor_operation,\
                                              context=100, flag=fl_flag)


    flashreq.policy.CopyFrom(route_policy_name)


    if "route_count" in kwargs:
        flashreq.route_count = kwargs.get('route_count')

    route_flash_stream = prpd.process_api(dev, channel_id, "RouteSubscribe", [flashreq, "jnx_Rib"], timeout=kwargs.get("timeout", 120))

    return route_flash_stream


def rib_labels(opcode, label):

    """
    Module to generate label structure for nexthop
    """

    lbl_ntry = prpd.LabelEntry(label=int(label))

    lblstkentry = prpd.LabelStackEntry(opcode=opcode.upper(), label_entry=lbl_ntry)

    return lblstkentry



def rib_nexthop(**kwargs):# pylint: disable=too-many-branches

    """
    Module to generate label structure for add/modify/update functions

    Module either gets next_hop_list <= 513 when ecmp=True
    or gets 1 element for non ecmp scenario
    """

    if 'next_hop_interface' in kwargs:
        if isinstance(kwargs["next_hop_interface"], list):
            next_hop_interface_list = kwargs["next_hop_interface"]
        else:
            next_hop_interface_list = [kwargs["next_hop_interface"], ]
    else:
        next_hop_interface_list = []

    if 'label' in kwargs:
        if isinstance(kwargs["label"], (list)):
            label_list = kwargs["label"]
        else:
            label_list = [kwargs["label"], ]
    else:
        label_list = []


    if 'opcode' in kwargs:
        if isinstance(kwargs["opcode"], list):
            opcode_list = kwargs["opcode"]
        else:
            opcode_list = [kwargs["opcode"], ]

    if 'weight' in kwargs:
        if isinstance(kwargs["weight"], list):
            weight_list = kwargs["weight"]
        else:
            weight_list = [kwargs["weight"], ]
    else:
        weight_list = []

    if 'bandwidth' in kwargs:
        if isinstance(kwargs["bandwidth"], list):
            bandwidth_list = kwargs["bandwidth"]
        else:
            bandwidth_list = [kwargs["bandwidth"], ]
    else:
        bandwidth_list = []

    stack_labels = kwargs.get('stack_labels', None)


    if 'next_hop' in kwargs:
        if isinstance(kwargs["next_hop"], str):
            next_hop_list = [kwargs["next_hop"], ]
        elif isinstance(kwargs["next_hop"], list):
            next_hop_list = kwargs["next_hop"]
    else:
        next_hop_list = []

    ecmp = kwargs.get("ecmp", False)

    nhlist = []
    nhlistoflists = False
    next_hop_innerlist = []
    next_hop_interface_innerlist = []
    weight_innerlist = []
    bandwidth_innerlist = []

    if isinstance(next_hop_list[0], list) and ecmp is True:# pylint: disable=too-many-branches
        nhlistoflists = True
        next_hop_innerlist = next_hop_list.pop(0)
        next_hop_list.append(next_hop_innerlist)
        nh_list_length = len(next_hop_innerlist)
    elif isinstance(next_hop_list[0], str) and ecmp is True:
        next_hop_innerlist = next_hop_list
        nh_list_length = len(next_hop_list)
    elif isinstance(next_hop_list[0], str) and ecmp is False:
        next_hop_innerlist.append(next_hop_list.pop(0))
        next_hop_list.extend(next_hop_innerlist)
        nh_list_length = 1
    elif isinstance(next_hop_list[0], list) and ecmp is False:
        next_hop_new_list = [item for sublist in next_hop_list for item in sublist]
        next_hop_innerlist.append(next_hop_new_list.pop(0))
        next_hop_new_list.extend(next_hop_innerlist)
        kwargs.pop("next_hop")
        kwargs.update(next_hop=next_hop_new_list)
        next_hop_list = next_hop_new_list
        nh_list_length = 1

    if len(next_hop_interface_list) > 0:
        next_hop_interface_exists = True
        if isinstance(next_hop_interface_list[0], list) and ecmp is True and nhlistoflists is True:# pylint: disable=too-many-branches
            next_hop_interface_innerlist = next_hop_interface_list.pop(0)
            next_hop_interface_list.append(next_hop_interface_innerlist)
        elif isinstance(next_hop_interface_list[0], str) and ecmp is True:
            next_hop_interface_innerlist = next_hop_interface_list
        elif isinstance(next_hop_interface_list[0], str) and ecmp is False:
            next_hop_interface_innerlist.append(next_hop_interface_list.pop(0))
            next_hop_interface_list.extend(next_hop_interface_innerlist)
        elif isinstance(next_hop_interface_list[0], list) and ecmp is False:
            next_hop_interface_new_list = [item for sublist in next_hop_interface_list for item in sublist]
            next_hop_interface_innerlist.append(next_hop_interface_new_list.pop(0))
            next_hop_interface_new_list.extend(next_hop_interface_innerlist)
            kwargs.pop("next_hop_interface")
            kwargs.update(next_hop_interface=next_hop_interface_new_list)
            next_hop_interface_list = next_hop_interface_new_list
    else:
        next_hop_interface_exists = False

    if len(weight_list) > 0:
        weight_exists = True
        if isinstance(weight_list[0], list) and ecmp is True and nhlistoflists is True:# pylint: disable=too-many-branches
            weight_innerlist = weight_list.pop(0)
            weight_list.append(weight_innerlist)
        elif (isinstance(weight_list[0], str) or isinstance(weight_list[0], int)) and ecmp is True:
            weight_innerlist = weight_list
        elif (isinstance(weight_list[0], str) or isinstance(weight_list[0], int)) and ecmp is False:
            weight_innerlist.append(weight_list.pop(0))
            weight_list.extend(weight_innerlist)
        elif isinstance(weight_list[0], list) and ecmp is False:
            weight_new_list = [item for sublist in weight_list for item in sublist]
            weight_innerlist.append(weight_new_list.pop(0))
            weight_new_list.extend(weight_innerlist)
            kwargs.pop("weight")
            kwargs.update(weight=weight_new_list)
            weight_list = weight_new_list
    else:
        weight_exists = False

    if len(bandwidth_list) > 0:
        bandwidth_exists = True
        if isinstance(bandwidth_list[0], list) and ecmp is True and nhlistoflists is True:# pylint: disable=too-many-branches
            bandwidth_innerlist = bandwidth_list.pop(0)
            bandwidth_list.append(bandwidth_innerlist)
        elif (isinstance(bandwidth_list[0], str) or isinstance(bandwidth_list[0], int)) and ecmp is True:
            bandwidth_innerlist = bandwidth_list
        elif (isinstance(bandwidth_list[0], str) or isinstance(bandwidth_list[0], int)) and ecmp is False:
            bandwidth_innerlist.append(bandwidth_list.pop(0))
            bandwidth_list.extend(bandwidth_list)
        elif isinstance(bandwidth_list[0], list) and ecmp is False:
            bandwidth_new_list = [item for sublist in bandwidth_list for item in sublist]
            bandwidth_innerlist.append(bandwidth_new_list.pop(0))
            bandwidth_new_list.extend(bandwidth_innerlist)
            kwargs.pop("bandwidth")
            kwargs.update(bandwidth=bandwidth_new_list)
            bandwidth_list = bandwidth_new_list
    else:
        bandwidth_exists = False

    for i in range(0, nh_list_length):# pylint: disable=too-many-nested-blocks
        next_hop = prpd.RouteGateway()

        ip_type = prpd.netaddr.IPAddress(next_hop_innerlist[i])
        ip_type.version

        next_hop_ip = next_hop_innerlist[i]


        if ip_type.version == 4:
            gateway = prpd.NetworkAddress(inet=prpd.IpAddress(addr_string=next_hop_ip))
        else:
            gateway = prpd.NetworkAddress(inet6=prpd.IpAddress(addr_string=next_hop_ip))


        if 'opcode' in kwargs:
            lblstkentrylist = list()

            if stack_labels is None:
                opcode = opcode_list.pop(0)
                opcode_list.append(opcode)
                if opcode.upper() == "POP":
                    lblstkentrylist.append(rib_labels("POP", 0))
                else:
                    element = label_list.pop(0)
                    label_list.append(element)
                    lblstkentrylist.append(rib_labels(opcode, element))
            else:
                if isinstance(label_list[0], list):

                    #labels = prpd.deepcopy(label_list.pop(0))
                    labels = label_list.pop(0)
                    label_list.append(labels)

                else:
                    labels = label_list

                for opcode in opcode_list:
                    if opcode.upper() == "POP":
                        lblstkentrylist.append(rib_labels("POP", 0))
                    else:
                        if not label_list:
                            logging.error("Label list is mandatory if opcode is used")
#                           if hasattr(builtins, 't'):
#                               raise TobyException("Label list is mandatory if opcode is used")
                        else:
                            opcode_length = len(opcode_list) - sum('pop' in single_opcode.lower() for single_opcode in opcode_list)

                            if opcode_length != len(labels):

                                logging.error("\n\
                                length Label-list != length opcode-list (POP is ignored)\n\
                                Label 0 is assigned internally for POP opcode \n\
                                Do not provide label value if opcode is POP \n\
                                Only provide label values for PUSH and SWAP operations")

#                                 if hasattr(builtins, 't'):
#                                     raise TobyException("Label list != opcode list (POP is ignored)")

                        element = labels.pop(0)
                        labels.append(element)
                        lblstkentrylist.append(rib_labels(opcode, element))

            lblstack = prpd.LabelStack(entries=lblstkentrylist)

            next_hop.label_stack.CopyFrom(lblstack)

        if next_hop_interface_exists:
            dest_intf_list_element = next_hop_interface_innerlist.pop(0)
            next_hop.interface_name = dest_intf_list_element
            next_hop_interface_innerlist.append(dest_intf_list_element)

        next_hop.gateway_address.CopyFrom(gateway)

        if weight_exists:
            weight_current = weight_innerlist.pop(0)
            if isinstance(weight_current, int):
                next_hop.weight = weight_current
            if isinstance(weight_current, str):
                next_hop.weight = weight_translate(weight_current)
            weight_innerlist.append(weight_current)

        if bandwidth_exists:
            bandwidth_element = bandwidth_innerlist.pop(0)
            next_hop.bandwidth = int(bandwidth_element)
            bandwidth_innerlist.append(bandwidth_element)


    return  prpd.RouteNexthop(gateways=nhlist)

