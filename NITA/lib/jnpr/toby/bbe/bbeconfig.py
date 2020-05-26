# Copyright 2016- Juniper Networks
# Toby BBE development team

""" This module Configures BBE on all devices in the topology as defined in the BBE Config YAML

Refer to BBE Engine Users Guide for detail usage information: http://bit.ly/2jwcjph

"""

#from jnpr.toby.engines.config.config import config
from jnpr.toby.bbe.version import get_bbe_version
from jnpr.toby.exception.toby_exception import TobyException
import jnpr.toby.frameworkDefaults.credentials as credentials
import yaml
import re
import os
import time


__author__ = ['Benjamin Schurman']
__contact__ = 'bschurman@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()

class BBEConfig:
    """
    Configures BBE features on all the devices in topology.
    Config is based on features enabled/disabled in the bbe config yaml file

    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

    @staticmethod
    def configure_tomcat(device='all', max_db_size='314572800'):
        """
        Configure tomcat mode on all routers marked with a tag of tomcat.
        This will also enable enhanced-ip mode if no already enabled

        :param max_db_size:
            max size of the

        :return:
            True if config is loaded successful
            raise exception if failed, TobyException
        """

        # get a list of routers that are DUTs
        if device == 'all':
            routers = bbe.get_devices(device_tags='tomcat', id_only=True)
            if not routers:
                t.log("No tomcat configuration is needed")
                return
        else:
            routers = device
            if not isinstance(routers, list):
                routers = [routers]

        # check each router to see if tomcat mode is enabled via lxml
        for router in routers:
            cmds = []
            enhanced_ip = False
            tomcat = False
            router_handle = t.get_handle(resource=router)
            hostname = router_handle.current_node.current_controller.name
            modelname = router_handle.get_model()
            if max_db_size == '314572800':
                dbsize = '300m'
                if modelname in ['MX104', 'MX80', 'MX80-T','MX40', 'MX40-T', 'AMX', 'MX10', 'MX5']:
                    dbsize = '100m'
            else:
                dbsize = max_db_size
            master_re = router_handle.get_current_controller_name()
            if hasattr(router_handle, 'vc') and router_handle.vc:
                #master_node = router_handle.detect_master_node()
                vc_re_name = router_handle.current_node.role
                if 'member0' in vc_re_name:
                    master_node = 'primary'
                elif 'member1' in vc_re_name:
                    master_node = 'member1'

                for node in ['primary', 'member1']:
                    for controller in ['re0', 're1']:
                        router_handle.set_current_controller(controller, node)
                        if router_handle.current_node.current_controller.is_master():
                            break
                    resp = router_handle.pyez('network_services').resp
                    if resp.findtext('network-services-information/name') != 'Enhanced-IP':
                        enhanced_ip = True
                    else:
                        resp = router_handle.cli(command="show configuration chassis network-services").resp
                        if 'enhanced-ip' not in resp:
                            enhanced_ip = True
                            t.log(
                                "Enhanced IP is enabled in vc {} chassis, however, "
                                "the configuration was removed".format(node))
                        else:
                            t.log('info', 'Enhanced IP enabled in vc {} chassis. Skipping config...'.format(node))

                    resp = router_handle.pyez('get_subscriber_management_statistics').resp
                    if 'not enabled' in resp.findtext('bbe-smgd-generic-string-list/bbe-smgd-generic-string'):
                        t.log('info', 'Tomcat mode NOT enabled in VC {}. Enabling...'.format(node))
                        tomcat = True
                    else:
                        resp = router_handle.cli(command="show configuration system services subscriber-management")
                        if 'enable' not in resp.resp:
                            tomcat = True
                            t.log("Tomcat is enabled in VC {} chassis, however,"
                                  " the configuration was removed".format(node))
                        else:
                            t.log('info', 'Tomcat mode enabled in VC {} chassis. Skipping config...'.format(node))

                    if enhanced_ip or tomcat:
                        cmds.append('set chassis network-services enhanced-ip')
                        cmds.append('set system services subscriber-management enable force')
                        cmds.append('set system configuration-database max-db-size {0}'.format(dbsize))
                        cmds.append('set system commit synchronize')
                        break
                router_handle.set_current_controller(master_re, master_node)
                if enhanced_ip or tomcat:
                    #config().CONFIG_SET(device_list=router, cmd_list=cmds, commit=True)
                    cmds.append('commit synchronize')
                    resp = router_handle.config(command_list=cmds, timeout=300).resp
                    if not re.search(r'please reboot', resp, re.IGNORECASE):
                        t.log("tomcat enabled in router {}".format(router))
                        continue
                    try:

                        t.log('Rebooting mxvc router {0}'.format(hostname))
                        #router_handle.reboot(wait=240, mode='cli', all=True)
                        router_handle.reboot(wait=240, all=True)
                        master_node = router_handle.detect_master_node()
                        master_re = router_handle.current_node.current_controller_str
                        t.log("after reboot, master node is {}, master re is {}".format(master_node, master_re))
                    except Exception as err:
                        raise TobyException('\nRouter reboot failed for {0}: {1}'.format(hostname, (str(err))))

                    for node in ['primary', 'member1']:
                        for controller in ['re0', 're1']:
                            router_handle.set_current_controller(controller, node)
                            if router_handle.current_node.current_controller.is_master():
                                break
                        hostname = router_handle.current_node.current_controller.name
                        resp = router_handle.pyez('network_services').resp
                        if resp.findtext('network-services-information/name') != 'Enhanced-IP':
                            raise TobyException(
                                'Enhanced-IP not enabled on VC {} {} node after reboot'.format(hostname, node))
                        else:
                            t.log('info', 'Enhanced-IP successfully enabled on VC {} {} node'
                                          ' after reboot'.format(hostname, node))

                        resp = router_handle.pyez('get_subscriber_management_statistics').resp
                        if 'not enabled' in resp.findtext('bbe-smgd-generic-string-list/bbe-smgd-generic-string'):
                            raise TobyException('Tomcat mode not enabled on VC {} {} node '
                                                'after reboot'.format(hostname, node))
                        else:
                            t.log('info', 'Tomcat mode is enabled on VC {} {} node after reboot'.format(hostname, node))
                    router_handle.set_current_controller(master_re, master_node)
                continue

            for re_name in t.get_resource(router)['system']['primary']['controllers']:
                router_handle.set_current_controller(controller=re_name, system_node='primary')
                # is enhanced-ip already enabled
                lxml = router_handle.execute_rpc(command='<network-services></network-services>').resp
                network_service_mode = lxml.findtext('network-services-information/name')
                if network_service_mode != 'Enhanced-IP':
                    t.log('info', 'Enhanced IP NOT enabled in {}. Enabling...'.format(re_name))
                    enhanced_ip = True
                else:
                    resp = router_handle.cli(command="show configuration chassis network-services").resp
                    if 'enhanced-ip' not in resp:
                        enhanced_ip = True
                        t.log("Enhanced IP is enabled in {}, however, the configuration was removed".format(re_name))
                    else:
                        t.log('info', 'Enhanced IP enabled in {}. Skipping config...'.format(re_name))

                # is tomcat already enabled?
                lxml = router_handle.execute_rpc(
                    command='<get-subscriber-management-statistics></get-subscriber-management-statistics>').resp
                tomcat_mode = lxml.findtext('bbe-smgd-generic-string-list/bbe-smgd-generic-string')
                if 'not enabled' in tomcat_mode:
                    t.log('info', 'Tomcat mode NOT enabled in {}. Enabling...'.format(re_name))
                    tomcat = True
                else:
                    resp = router_handle.cli(command="show configuration system services subscriber-management").resp
                    if 'enable' not in resp:
                        tomcat = True
                        t.log("Tomcat is enabled in {}, however, the configuration was removed".format(re_name))
                    else:
                        t.log('info', 'Tomcat mode enabled in {}. Skipping config...'.format(re_name))

                if enhanced_ip or tomcat:
                    cmds.append('set chassis network-services enhanced-ip')
                    cmds.append('set system services subscriber-management enable force')
                    cmds.append('set system configuration-database max-db-size {0}'.format(dbsize))
                    break
            ##switch back to master re
            router_handle.set_current_controller(controller=master_re, system_node='primary')
            if enhanced_ip or tomcat:
                if len(t.get_resource(router)['system']['primary']['controllers'].keys()) > 1:
                    cmds.append('set system commit synchronize')
                #config().CONFIG_SET(device_list=router, cmd_list=cmds, commit=True)
                cmds.append('commit')
                resp = router_handle.config(command_list=cmds, timeout=300).resp
                if not re.search(r'please reboot', resp, re.IGNORECASE):
                    t.log("tomcat enabled in router {}".format(router))
                    continue
                try:
                    t.log('Rebooting router, {0}'.format(hostname))
                    router_handle.reboot(wait=120, all=True)
                except Exception as err:
                    raise TobyException('\nRouter reboot failed for {0}: {1}'.format(hostname, (str(err))))

                master_re = router_handle.get_current_controller_name()
                t.log("after reboot, current master re is {}".format(master_re))
                for re_name in t.get_resource(router)['system']['primary']['controllers']:
                    router_handle.set_current_controller(controller=re_name, system_node='primary')
                    # check if tomcat is enabled
                    # add 6 retries for RE tomcat mode verification, each with 15 seconds
                    index = 0
                    while index < 6:
                        try:
                            lxml = router_handle.execute_rpc(
                                command='<get-subscriber-management-statistics></get-subscriber-management-statistics>').resp
                        except Exception as err:
                            t.log("got rpc exception with {}, waiting for another 10s".format(str(err)))
                            time.sleep(10)
                            index += 1
                            continue
                        tomcat_mode = lxml.findtext('bbe-smgd-generic-string-list/bbe-smgd-generic-string')
                        if 'not enabled' in tomcat_mode or not tomcat_mode:
                            t.log("waiting for another 10 seconds to check tomcat mode in {}".format(re_name))
                            time.sleep(10)
                            index += 1
                        else:
                            break
                    if 'not enabled' in tomcat_mode or not tomcat_mode:
                        raise TobyException('\nTomcat mode not enabled on {} {}after reboot'.format(hostname, re_name))
                    else:
                        t.log('info', 'Tomcat mode successfully enabled on {} {} after reboot'.format(hostname, re_name))
                    ## do not check the backup RE enhanced-ip mode after reboot since 16.1 backup RE does not have result
                    if re_name != master_re:
                        continue
                    # check if enhanced-ip is enabled on router
                    lxml = router_handle.execute_rpc(command='<network-services></network-services>').resp
                    network_service_mode = lxml.findtext('network-services-information/name')
                    if network_service_mode != 'Enhanced-IP' and re_name == master_re:
                        raise TobyException('\nEnhanced-IP not enabled on {} {} after reboot'.format(hostname, re_name))
                    else:
                        t.log('info', 'Enhanced-IP successfully enabled on {} {} after reboot'.format(hostname, re_name))


                ##switch back to master re
                t.log("after tomcat check, switch back to master re {}".format(master_re))
                router_handle.set_current_controller(controller=master_re, system_node='primary')

        return True
