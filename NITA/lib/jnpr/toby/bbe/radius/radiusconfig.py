""" This module defines the configuration methods necessary for BBEConfig to setup radius servers
"""

from jnpr.toby.engines.config import config
from jnpr.toby.bbe.errors import BBEConfigError
from jnpr.toby.bbe.version import get_bbe_version
from jnpr.toby.bbe.radius.freeradius import FreeRadius

# Local paths
# from toby.lib.jnpr.toby.bbe.errors import BBEConfigError
# from toby.lib.jnpr.toby.bbe import BBEVars
# from version import get_bbe_version, log_bbe_version
# from radius.freeradius import *

__author__ = ['Dan Bond']
__contact__ = 'dbond@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()


def config_radius_server():
    """Configures the radius servers defined in the BBEVar YAML file.

    :return:
    """

    # TODO: Temporary variable values for exercising code paths
    # l2tp_tunnels = False
    # vrfs = False
    # ndra = False
    # ia_pd_flag = False
    # ia_na_flag = False
    # nfp = False
    # user_name_transform = False
    # sbr_initialize = False
    sbr = False
    free_radius_initialize = True

    # TODO: Acquire equivalent variables from bbevar using accessors
    #   - $l2tp = $v->{'L2TP_TUNNELS'}  L2TP tunnels enabled?
    #   - $vrfs = $v->{L3_RETAILERS}    Account for vrfs?
    #   - $ndra = $t->{myVar}{paramsHashes}{v6AddressAssignment}{'NDRA'}    NDRA?
    #   - $pd = $t->{myVar}{paramsHashes}{v6AddressAssignment}{'type'}      V6 Prefix delegation?
    #   - $na = $t->{myVar}{paramsHashes}{v6AddressAssignment}{'type'}      V6 NA?
    #   - $nfp = $v->{DHCP_MULT_PREF_SUB}
    #   - $userNameTransform = $l2tp && !($l2tp && $v->{L2TP_TUNNEL_MODE} !~ /domainMap/i);
    #     Don't set up username transform if doing non-domainMap l2tp, or no l2tp at all
    #   - $sbr = T/F True is radius is sbr, false otherwise
    #   - $sbrInit = 1 unless set to 0 explicitly
    #   - $frInit = 1 unless set to 0 explicitly

    # TODO: Acquire list of resource tags which are associated with radius servers (typically h0,h1,etc)
    radius_servers = bbe.get_devices(device_tags='radius', id_only=True)

    # TODO: Configure links and set NTP server
    # config_dut_radius_links()  # Stub
    # set_host_ntp_server()      # Stub, not important at this time


    if sbr:
        # To be implemented later
        t.log('error', 'Sbr radius servers are not supported yet')
    else:
        t.log('Configuring FreeRADIUS servers')

        for server in radius_servers:
            # Generate hostname, device handle, and instantiate FreeRadius object
            handle = t.get_handle(resource=server)
            host = handle.current_node.current_controller.name + ".englab.juniper.net"
            radius = FreeRadius(dev_handle=handle, host_name=host)

            # TODO: Initialize server if set. Consider moving this into the FreeRadius class __init__()
            if free_radius_initialize:
                t.log('FreeRADIUS initialization.')
            else:
                t.log('FreeRADIUS initialization skipped by user override.')

            # TODO: Add DUT as client, if this radius is associated with the DUT
            # Will need DUT associated with this radius server and the loopback of that DUT

                #$h[0]->rs_add_client(
                    #client => "$t->{myVar}{loopbacks}{v4}[$dutIndex]",
                    #secret => "$v->{'RADIUS_SECRET'}",
                    #shortname => "$r[$dutIndex]->{'HOST'}",
                    #commit => JT::FALSE,
                    #new => JT::TRUE
                #);
            loopback = '101.0.0.1'
            # loopback = bbe.get_loopback(resource='r0') # Needed method. r0 is the router associated with 'server'
            # radius_secret = 'joshua'
            radius_secret = bbe.bbevar['resources'][server]['config']['radius-secret']
            # radius_secret = bbe.get_radius_secret  # Something similar needed

            radius.add_radius_client(client=loopback, secret=radius_secret,
                                     short_name=handle.current_node.current_controller.name, commit=True, new=True)

            # TODO: Add clients for VRFs

            # TODO: Add DEFAULT with common attributes
            request_avp = "Service-Type == Framed-User, Auth-Type := Local"
            reply_avp = "Auth-Type = Local, Service-Type = Framed-User, Fall-Through = 1"

            radius.add_radius_user(user='DEFAULT', request_avp=request_avp, reply_avp=reply_avp,
                                   commit=True, new=False)


            # TODO: Add user DEFAULTUSER. Reply avp can vary based on Cos, Filter, etc.
            default_user_request_avp = 'User-Password == \'{0}\''.format(radius_secret)
            default_user_reply_avp = ''
            default_user = 'DEFAULTUSER'    #Static for now

            # Add CoS reply AVPs if DEFAULTUSER requires
            if bbe.bbevar['cos']['configure-cos'] and not bbe.bbevar['cos']['static-cos']:
                default_user_reply_avp = "Jnpr-CoS-Parameter-Type := \"T01 be_ef_af_smap\"\n" \
                                         "Jnpr-CoS-Parameter-Type += \"T02 30m\"\n" \
                                         "Jnpr-CoS-Parameter-Type += \"T03 30m\"\n" \
                                         "Jnpr-CoS-Parameter-Type += \"T04 30m\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"be_sch T01 10\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"be_sch T02 10\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"be_sch T03 low\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"be_sch T04 d0\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"be_sch T05 d1\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"be_sch T06 d2\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"be_sch T07 d3\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"ef_sch T01 20\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"ef_sch T02 20\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"ef_sch T03 medium-low\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"ef_sch T04 d3\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"ef_sch T05 d2\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"ef_sch T06 d1\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"ef_sch T07 d0\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"af_sch T01 30\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"af_sch T02 30\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"af_sch T03 medium-high\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"af_sch T04 d0\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"af_sch T05 d1\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"af_sch T06 d2\"\n" \
                                         "Jnpr-Cos-Scheduler-Pmt-Type += \"af_sch T07 d3\""

            # TODO: Add Filter reply AVPs if DEFAULTUSER requires

            # TODO: Add Ascend Data Filter AVPs if DEFAULTUSER requires

            # TODO: Add service activation if DEFAULTUSER requires

            # TODO: Add L2BSA if DEFAULTUSER requires

            # TODO: $nfp if DEFAULTUSER requires

            # TODO: Commit DEFAULTUSER changes (add radius user)
            radius.add_radius_user(user=default_user, request_avp=default_user_request_avp,
                                   reply_avp=default_user_reply_avp, commit=True, new=False)

            # TODO: Add non-vrf l2tp clients with attributes based on default client

            # TODO: Add Wholesale users

            # TODO: Ping router to see if connection is up. Assumes access profiles are configured

def config_dut_radius_links():
    """Configures the radius links associated with the DUT in BBEVar YAML file.

    :return:
    """

    # TODO: Add method to retrieve l3 retailer count from the DUT
    # number_of_l3_retailers = bbe.get_l3_retailers()
    number_of_l3_retailers = 10

    # Set no-auto-negotiation on the DUT and vlan-tagging on the pipe
    dut_device_id = bbe.get_devices(device_tags='dut', id_only=True)
    dut_radius_interface = bbe.get_interfaces(dut_device_id, interfaces='radius-0')[0]  # Gives me BBEVarInterface obj
    dut_radius_interface = dut_radius_interface.interface_name  # Pull out physical intf name since it's all we need

    config_commands = []
    config_commands.append('set interfaces {0} gigether-options no-auto-negotiation'.format(dut_radius_interface))
    config_commands.append('set interfaces {0} vlan-tagging'.format(dut_radius_interface))

    try:
        config.config().CONFIG_SET(device_list=dut_device_id, cmd_list=config_commands, commit=True)
    except Exception as err:
        raise BBEConfigError('\nError while configuring radius interface on router {0}: {1}'\
                             .format(dut_device_id, str(err)))

    # Generate router IPs and configure DUT if l3 retailers are present
    # base_address = '9.0.0.0'
    netmask = '24'
    config_commands = []    # Clear config_commands

    # Use config engine to generate set commands to accommodate l3 retailers
    if number_of_l3_retailers > 0:
        config_commands.append('set interfaces {0} unit <<1..>> family inet address 9.0.<<0..{1}>>.1/{2}'\
                               .format(dut_radius_interface, number_of_l3_retailers, netmask))

        try:
            config.config().CONFIG_SET(device_list=dut_device_id, cmd_list=config_commands, commit=True)
        except Exception as err:
            raise BBEConfigError('\nError while configuring radius interfaces on router {0}: {1}'\
                                 .format(dut_device_id, str(err)))


    # TODO: Generate radius IP addresses. Default bit offset is 9
    # If # of radius IP == # of router IPs, generate radius IP addresses from count of l3 retailers

    # TODO: Clear radius interface on DUT (if needed)

    # TODO: Iterate over radius IPs and configure the VLAN interface associated with it.

    # TODO: Add static route on radius to the router loopback address associated with it

    # TODO: Create the ifl on the router

    return True

def set_host_ntp_server():
    """Set NTP server for host (radius server).

    :return:
    """
    return True
