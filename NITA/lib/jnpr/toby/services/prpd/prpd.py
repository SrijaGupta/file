"""
prpd-api-module
"""
import logging
import importlib
import os
import re
import socket
import struct
from copy import deepcopy
import netaddr

def execute_prpd_api(dev, channel_id=None, command=None, **kwargs):
    """
    DESCRIPTION:
        'Execute PRPD API' is used to execute any of the prpd api calls from the client side using
        pre-established grpc channel. It supports

          * add/modify/update/delete/get/monitor of  RIB-Static routes, BGP (inet, inet6, inet-vpn(in bgp.l3vpn table),
          inet6-vpn (in bgp.l3vpn table), inet-srte,net6-srte, inet-flow,inet6-flow).
          * add/modify/update/delete/get of RIB-MPLS-Static routes.
          * Interface monitoring

          Slides - easylink.juniper.net/REM

    ROBOT USAGE:
        Sample usage Toby script - https://easylink.juniper.net/REM.robot

        For Single BGP Prefix add:
            ${add_result}=  execute prpd api  ${r0}   command=bgp_route_add
            ...   dest_prefix=20.1.1.0
            ...   table=inet.0
            ...   prefix_len=${30}
            ...   next_hop=${nh_list}

        For multi BGP prefix add:
        ${prefix_list} =    Create List    20.1.1.0    20.1.2.0    20.1.3.0
        ${add_result}=  execute prpd api  ${r0}   command=bgp_route_add
        ...   dest_prefix=${prefix_list}
        ...   table=inet6.0
        ...   prefix_len=${120}
        ...   next_hop=2001:5::1

        For Single STATIC  Prefix add:
        ${add_result}=  execute prpd api  ${r0}   command=rib_route_add \
        ...   dest_prefix=50.0.0.1
        ...   table=inet.0
        ...   prefix_len=${32}
        ...   next_hop=1.1.0.2

        For multi STATIC prefix add:
        ${prefix_list} =    Create List    20.1.1.0    20.1.2.0    20.1.3.0
        ${add_result}=  execute prpd api  ${r0}   command=rib_route_add
        ...   next_hop_interface=ge-0/0/0.0
        ...   dest_prefix=${prefix_list}
        ...   table=inet.0
        ...   prefix_len=${32}
        ...   next_hop=1.1.0.2


    ARGUMENTS:
        :dev:
            *MANDATORY*
            device on which the routes needs to be programmed/monitored.
            pass the router handle acquired in Toby.
        :channel_id:
            *OPTIONAL*
            By default, command is executed on first grpc channel added using 'Add Channel To Device' keyword
            If additional channels are added to the device with 'Add Channel To Device' and user wants to execute the command on a specific channel,
            user needs to provide the channel_id
            If provided , grpc channel specificied will be used for executing prpd api calls.

        :command:
            *MANDATORY*
            Below is the list of commands supported
            BGP:
                bgp_route_add
                    - To add bgp routes.
                    - BGP routes can be added for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * inet-vpn in bgp.l3vpn.0 table in RR
                        * inet6-vpn in bgp.l3vpn-inet6.0 table in RR
                        * inet-srte in bgp.inetsrte.0 table
                        * inet6-srte in bgp.inet6srte.0 table
                        * inet-flow in inetflow.0 table
                        * inet6-flow in inet6flow.0 table
                bgp_route_modify
                    - To modify attributes in already added bgp routes using execute_prpd_api.
                    - BGP routes can be modified for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * inet-vpn in bgp.l3vpn.0 table in RR
                        * inet6-vpn in bgp.l3vpn-inet6.0 table in RR
                        * inet-srte in bgp.inetsrte.0 table
                        * inet6-srte in bgp.inet6srte.0 table
                        * inet-flow in inetflow.0 table
                        * inet6-flow in inet6flow.0 table
                bgp_route_update
                    - To update attributes in already added bgp routes using execute_prpd_api or
                        add new route if the route is not present already.
                    - BGP routes can be updated for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * inet-vpn in bgp.l3vpn.0 table in RR
                        * inet6-vpn in bgp.l3vpn-inet6.0 table in RR
                        * inet-srte in bgp.inetsrte.0 table
                        * inet6-srte in bgp.inet6srte.0 table
                        * inet-flow in inetflow.0 table
                        * inet6-flow in inet6flow.0 table
                bgp_route_remove
                    - To delete already added bgp routes using execute_prpd_api.
                    - BGP routes can be deleted for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * inet-vpn in bgp.l3vpn.0 table in RR
                        * inet6-vpn in bgp.l3vpn-inet6.0 table in RR
                        * inet-srte in bgp.inetsrte.0 table
                        * inet6-srte in bgp.inet6srte.0 table
                        * inet-flow in inetflow.0 table
                        * inet6-flow in inet6flow.0 table
                bgp_route_get
                    - To get already added bgp routes either using execute_prpd_api or advertised by peer.
                    - Supported for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * inet-vpn in bgp.l3vpn.0 table in RR
                        * inet6-vpn in bgp.l3vpn-inet6.0 table in RR
                        * inet-srte in bgp.inetsrte.0 table
                        * inet6-srte in bgp.inet6srte.0 table
                        * inet-flow in inetflow.0 table
                        * inet6-flow in inet6flow.0 table
                        * inet-lu and inet6-lu routes
                bgp_route_monitor
                    - To monitor the routes advertised by BGP peer.
                       Need to configure import policy with analyze knob for the routes to be monitored.
                    - Supported for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * inet-vpn in bgp.l3vpn.0 table in RR
                        * inet6-vpn in bgp.l3vpn-inet6.0 table in RR
                        * inet-srte in bgp.inetsrte.0 table
                        * inet6-srte in bgp.inet6srte.0 table
                        * inet-flow in inetflow.0 table
                        * inet6-flow in inet6flow.0 table
                        * inet-lu and inet6-lu routes

            RIB:
                rib_route_add
                    - To add static routes
                    - STATIC routes can be added for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * mpls in mpls.0 table
                        * inet/ine6 routes in routing instances

                rib_route_modify
                    - To modify attributes in already added static routes
                    - STATIC routes can be modified for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * mpls in mpls.0 table
                        * inet/ine6 routes in routing instances

                rib_route_update
                    - To update attributes in already added static routes
                        add new route if the route is not present already.
                    - STATIC routes can be updated for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * mpls in mpls.0 table
                        * inet/ine6 routes in routing instances

                rib_route_remove
                    - To delete already added static routes using execute_prpd_api
                    ** ONLY THE ROUTES ADDED BY A UNIQUE client_id CAN BE REMOVED
                    - STATIC routes can be removed for below address families
                        * inet in inet.0 table
                        * inet6 in inet6.0 table
                        * mpls in mpls.0 table
                        * inet/ine6 routes in routing instances

                rib_route_get
                    - To fetch routes present in the rib (Returns data in JSON format)
                    - Supported for below address families

                rib_route_monitor
                    - To monitor the routes in Junos rib. (Returns data in JSON format)
                    - Supported for below address families

            INTERFACE:
                interface_initialize:
                    - Command required to initiaize interface API for a device.
                       Below interface commands cannot be used without initialization

                interface_notification_register:
                    - Register for and recieve stream of interface notifications
                    - Supported for below interface components
                        * IFD
                        * IFL
                        * IPv4/IPv6

                interface_notification_unregister:
                    - Unregister from interface notifications
                    - Supported for below interface components
                        * IFD
                        * IFL
                        * IPv4/IPv6

                interface_get:
                    - Poll for a specific interface data from device once per API call
                    - Supported for below interface components
                        * IFD
                        * IFL
                        * IPv4/IPv6
        :**kwargs:
            *MANDATORY*

            Each of the command supported requires specific set of arguments as mandatory arguments.
            Below document has all the supported arguments for each of the commands and it's description.
            <TBD>
            Below is the manadatory argument list.

            BGP:
            command = bgp_route_add | bgp_route_modify | bgp_route_update:
                dest_prefix    - BGP prefix which needs to be added/modified/updated.
                table          - Table in which prefix needs to be added/modified/updated
                prefix_len     - Prefix length of the dest prefix
                next_hop       - Protocol next-hop address of the dest_prefix(Remote BGP peer IP).
                                Needs to be resolved for the dest_prefix to be seen as active route in the table.
            command = bgp_route_get | bgp_route_remove:
                dest_prefix    - BGP prefix which needs to be added/modified/updated.
                table          - Table in which prefix needs to be added/modified/updated
                prefix_len     - Prefix length of the dest prefix
            command = bgp_route_monitor:
                 No Mandatory arguments. However import policy with analyze knob has to be configured in the router
                 for the routes to be monitored.


            RIB:
            command = rib_route_add | rib_route_modify | rib_route_update:
                dest_prefix    - prefix which needs to be added/modified/updated.
                table          - Table in which prefix needs to be added/modified/updated
                prefix_len     - Prefix length of the dest prefix
                next_hop       - next-hop address of the dest_prefix.
                                 Needs to be resolved for the dest_prefix to be seen as active route in the table.

            command = rib_route_get | rib_route_remove:
                dest_prefix    - prefix which needs to be monitored/deleted
                table          - Table from which routes needs to be read/removed
                prefix_len     - Prefix length of the dest prefix (Multiple prefixes can be read depending on the subnet)

            command = rib_route_remove:
                dest_prefix    - prefix which needs to be deleted
                table          - Table from which routes needs to be removed
                prefix_len     - Prefix length of the dest prefix

            command = rib_route_monitor:
                table          - Table from which routes needs to be read


            INTERFACE:
            command = interface_get:
                interface      - Interface name to poll the information for (IDF.IFL)



    """

    logging.debug("Input parameters\n")
    logging.debug(kwargs)


    if kwargs.get("compliance", None) == True:
        api_version = '2'
    else:
        api_version = kwargs.get("api_version", '1')
        if (api_version == None):
            api_version = '1'

    current_target = dev.current_node.current_controller

    if channel_id is None:
        channel_id = current_target.default_grpc_channel

    if command is None:
        raise Exception("Mandatory parameter 'command' absent")
    else:
        commands, module = init_command(command, api_version)

    if command in commands:

        func = getattr(module, command)
        api_result = func(dev, channel_id, **kwargs)

        return  api_result
    else:
        print("Valid list of commands", commands)
        raise Exception("Please use a valid PRPD api command to execute from below commands", commands)



def dest_prefix_limiter(**kwargs):
    """
    DOcs
    """
    if 'prefix_length' in kwargs:
        kwargs["prefix_len"] = kwargs.pop("prefix_length")

    if 'destination_prefix' in kwargs and 'dest_prefix' in kwargs:
        raise Exception("Either destination_prefix or dest_prefix can be used.")

    if 'destination_prefix' in kwargs:
        kwargs["dest_prefix"] = kwargs.pop("destination_prefix")

    if 'dest_prefix' in kwargs:
        if isinstance(kwargs["dest_prefix"], str) or isinstance(kwargs["dest_prefix"], int):
            dest_prefix = [kwargs["dest_prefix"], ]
        elif isinstance(kwargs["dest_prefix"], list):
            dest_prefix = kwargs["dest_prefix"]
        elif isinstance(kwargs["dest_prefix"], dict):
            dprefix_dict = kwargs["dest_prefix"]
            dest_prefix = dprefix_dict["dest_prefix"]
            if isinstance(dest_prefix, str):
                dest_prefix = [dest_prefix]
    else:
        raise Exception("Mandatory parameter 'dest_prefix' absent")

    bulk_count = int(kwargs.get("bulk_count", 1000))
    if bulk_count < 1 or  bulk_count > 1000:
        raise Exception("Please provide integer value for bulk count from range 1-1000 ")


    # Deepcopy of dest_prefix to avoid deleting elements from array provided by the user
    destination_prefix = deepcopy(dest_prefix)
    while  destination_prefix:
        newlist = destination_prefix[0:bulk_count]
        del destination_prefix[0:bulk_count]
        yield  newlist



def process_api(dev, channel_id, api, api_arguments, timeout=None, stream=None):
    """
    DOcs
    """
    if timeout is None:
        timeout = 120


    logging.debug('channel_id,api,api_arguments,timeout')
    logging.debug(channel_id)
    logging.debug(api)
    logging.debug(api_arguments)
    logging.debug(stream)


    if stream is True:
        if len(api_arguments[0]) > 1:
            response = []
            response.append(dev.current_node.current_controller.channels['grpc'][channel_id].send_api(api=api, args=iter(api_arguments[0]),\
                                                                                                      service=api_arguments[1], timeout=timeout))
        else:
            response = dev.current_node.current_controller.channels['grpc'][channel_id].send_api(api=api, args=iter(api_arguments[0]),\
                                                                                                      service=api_arguments[1], timeout=timeout)       
    else:
        response = dev.current_node.current_controller.channels['grpc'][channel_id].send_api(api=api, args=api_arguments[0], service=api_arguments[1],\
                                                                                         timeout=timeout)
    return response


def init_command(command, api_version):

    """
    DOcs
    """

    if int(api_version) == 2:

        logging.info("Using compliance API version ")

        api_list = ["jnx_common_addr_types_pb2", "jnx_common_base_types_pb2", "jnx_routing_base_types_pb2"]

        if "rib" in command:
            api_list.extend(["jnx_routing_rib_service_pb2"])

            commands = ["rib_route_add", "rib_route_modify", "rib_route_update", "rib_route_monitor",\
                    "rib_route_remove", "rib_route_get", "rib_route_flash", "rib_route_cleanup", "rib_route_initialize"]

            module_name = "jnpr.toby.services.prpd.rib.rib_" + str(api_version)
            module = importlib.import_module(module_name, package=None)


        if "bgp" in command:
            api_list.extend(["jnx_routing_bgp_service_pb2"])

            commands = ["bgp_init", "bgp_route_add", "bgp_route_update",\
                    "bgp_route_modify", "bgp_route_remove", "bgp_route_get", "bgp_monitor_register",\
                    "bgp_monitor_unregister"]

            module_name = "jnpr.toby.services.prpd.bgp.bgp_" + str(api_version)
            module = importlib.import_module(module_name, package=None)

        if "interface" in command:
            api_list.extend(["jnx_routing_interface_service_pb2"])

            commands = ["interface_initialize", "interface_notification_register", "interface_notification_unregister",\
                    "interface_get", "interface_notification_refresh"]

            module_name = "jnpr.toby.services.prpd.interface.interface_" + str(api_version)
            module = importlib.import_module(module_name, package=None)


    else:

        api_list = ["prpd_service_pb2", "prpd_common_pb2", "jnx_addr_pb2"]

        logging.info("Using non-compliance API version ")


        if "rib" in command and "gribi" not in command:
            api_list.extend(["rib_service_pb2"])

            commands = ["rib_route_add", "rib_route_modify", "rib_route_update", "rib_route_monitor",\
                    "rib_route_remove", "rib_route_get", "rib_route_flash"]

            module = importlib.import_module("jnpr.toby.services.prpd.rib.rib", package=None)


        if "bgp" in command:
            api_list.extend(["bgp_route_service_pb2"])

            commands = ["bgp_init", "bgp_route_add", "bgp_route_update",\
                    "bgp_route_modify", "bgp_route_remove", "bgp_route_get", "bgp_monitor_register",\
                    "bgp_monitor_unregister"]

            module = importlib.import_module("jnpr.toby.services.prpd.bgp.bgp", package=None)


        if "interface" in command:
            api_list.extend(["routing_interface_service_pb2"])

            commands = ["interface_initialize", "interface_notification_register", "interface_notification_unregister",\
                    "interface_get", "interface_notification_refresh"]

            module = importlib.import_module("jnpr.toby.services.prpd.interface.interface", package=None)


        if "gribi" in command:
            api_list.extend(["gribi_service_pb2", "gribi_aft_pb2", "gribi_ywrapper_pb2"])

            commands = ["gribi_add", "gribi_delete", "gribi_modify"]

            module = importlib.import_module("jnpr.toby.services.prpd.rib.gribi", package=None)
        
        if "bfd" in command:
            api_list.extend(["bfd_service_pb2"])

            commands = ["bfd_initialize", "bfd_session_add", "bfd_notification_subscribe", "bfd_notification_unsubscribe",\
                    "bfd_session_delete", "bfd_session_delete_all"]

            module = importlib.import_module("jnpr.toby.services.prpd.bfd.bfd", package=None)

    func = getattr(module, "_init")
    func(api_list)


    return  commands, module


def import_api(api_list):
    """
    DOcs
    """

    for lib in api_list:
        if re.search(r'\.py$', lib):
            lib = lib[:-3]
        lib = lib.replace(os.path.sep, '.')
        module = importlib.import_module(lib, package=None)

        for ele_x in dir(module):
            globals()[ele_x] = getattr(module, ele_x)


    return  api_list

def ip_to_uint32(address):
    """
    DOcs
    """
    t = socket.inet_aton(address)

    return struct.unpack("I", t)[0]

def uint32_to_ip(ipn):
    """
    DOcs
    """
    t = struct.pack("I", ipn)
    return socket.inet_ntoa(t)



def increment_prefix(ipstart,count):

    logging.info("ipstart - %s", ipstart)
    logging.info("count - %s", count)

    netlist= []
    if isinstance(ipstart, str):
        ipnet = netaddr.IPNetwork(ipstart)
        size = ipnet.size

        ipnext = int(netaddr.IPAddress(ipnet.ip))
        for i in range(0, count):
            nextip = str(netaddr.IPAddress(ipnext))
            netlist.append(nextip)
            ipnext = ipnext + size
    else:

        for i in range(0, count):
            netlist.append(ipstart)
            ipstart = ipstart + 1

    return netlist



