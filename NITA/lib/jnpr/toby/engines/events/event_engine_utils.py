"""
Copyright (C) 2015-2016, Juniper Networks, Inc.
All rights reserved.
Authors:
    jpzhao, bphillips
Description:
    Toby Library - Event Engine Utilities

"""
# pylint: disable=locally-disabled,undefined-variable,too-many-branches,too-many-nested-blocks,invalid-name,import-error
import re
#import copy
#import os
#import types
#import time
import datetime
from inspect import stack
from jnpr.toby.hldcl.device import set_device_log_level
from jnpr.toby.hldcl.device import add_mode
from jnpr.toby.hldcl.device import execute_command_on_device as execute_custom_mode
from lxml import etree as ET

try:
    from robot.libraries.BuiltIn import BuiltIn
except Exception:
    ROBOT = False

#HLDCL_Devices = (SrxSystem, MxSystem, NfxSystem, JuniperSystem,
#                 Warp17, System,
#                 CiscoSystem, BrocadeSystem, SrcSystem,
#                 Avalanche, Landslide, Spirent,
#                 Paragon,
#                 IxLoad, Ixia,
#                 Breakingpoint,
#                 Elevate,
#                )

device_handle_map = {}
device_list = []
dh_info = {}
threads = []
custom_modes = {}

def add_tag_name_to_handle():
    '''
    add_tag_name_to_handle
    '''
    for node in t.resources:
        dname = t.resources[node]['system']['primary']['name']
        dh = t.get_handle(resource=node)
        #pprint(dh.current_node.current_controller_str); input('dh')
        # does this work for testers/linux?
        dh.tag = node
        dh.name = dname

def device_handle_parser(device=None, **kwargs):
    '''
    - User can pass in the device in any format: hendle, alias, or hostname,
      This method will find the handle for the device
    - After the input, this will do reverse lookups to figure
      out what it doesn have.
    - Instad of returning the values, this save the:
        dh string, device alias and the device hostname
    - If dh string, device alias and the device hostname have
      already been found, move on.....

    :param resource:
        ** device inout requires, can be dh string, device alias and the device hostname
        ex 1: dh = jnpr.toby.hldcl.Device(resource='router_name')
              _device_handle_parser(device=dh)
        ex 2: _device_handle_parser(device='r0')
        ex 3: _device_handle_parser(device='gallon')

    : returns:
        dict: dh string, and device alias and the device hostname in the device_handle
        ex return:  <jnpr.toby.hldcl.juniper.routing.mxsystem.MxSystem object at 0x7fa74fe96978>
    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())

    dev_h = None
    if isinstance(device, str):
        if tv.get(device + '__name'): # If the device alias, get the DH string and hostname
            #t.log('debug','It is an alias, get DH handle and hostname')
            dev_h = t.get_handle(resource=device)
            dev_h.tag = device ### device tag/alias
            dev_h.name = dev_h.current_node.current_controller.name ### hostname
        else:  ### eg: r3__name: alcohol
            # device is not a device alias, could be a device hostname
            for alias in t.resources:
                if t.resources[alias]['system']['primary']['name'] == device:
                    if kwargs.get('debug_log_on'):
                        t.log('debug', '{}: device: {} found'.format(func_name(), device))
                    dev_h = t.get_handle(resource=alias)
                    device_handle_map[device] = dev_h
                    t.log('debug', '{} in device_list is a name rather than an alias' \
                               .format(device))
                    dev_h.tag = alias
                    dev_h.name = device
                    break
            else:
                raise Exception(device + ' is neither an alias or a host name in params, \
                                cannot find device handle for it')

    elif re.match(r'<class \'jnpr.toby.hldcl', str(type(device))):
    #elif isinstance(device, HLDCL_Devices):
        # is an hldcl device handle
        dev_h = device
        if get_device_info_from_handle(dh=dev_h, **kwargs) is True:
            t.log('device tag and hostname was derived from device_handle')
        # elif get_device_info_from_handle(dh=dev_h, **kwargs) is 'external_device':
        #     print('DEV TAG: {}'.format(dev_h.tag))
        #     dev_host = dev_h.current_node.current_controller.host
        #     if dev_h.tag == 'external_device':
        #         device_handle_map[dev_host] = dev_h
        #         # replace device_list with the host ( an ip address in most cases)
        #         t.log('debug', ' device_list has a handle, replace it with its host {}' \
        #               .format(dev_host))
        #         dev_h.name = dev_host

    return dev_h

def get_dh_name(dh):
    '''
    get_dh_name
    '''
    name = None
    if dh.__dict__.get('name'):
        name = dh.name
    elif dh.__dict__.get('host'):
        name = dh.host
    return name

def get_dh_tag(dh):
    '''
    get_dh_tag
    '''
    return dh.tag

def _get_dev_handle(resource, **kwargs):
    '''
    retrieve device handle from t

    :param resource:
        **REQUIRED** device tag/name as shown in the t (or toby yaml file)
    :return: device handle

    '''
    if kwargs.get('debug_log_on'):
        t.log('debug', func_name())
    # Most probably it is a device alias  in params / t (r0, ht0, ..)
    try:
        dev_hdl = t.get_handle(resource=resource)
        return dev_hdl
    except:
        t.log('debug', 'cannot find device handle for {} in t'.format(resource))

    # if not, it might be a host mapped to a device handle
    if device_handle_map.get(resource):
        dev_hdl = device_handle_map[resource]
    else:
        # last try, it might be a device name
        for dev in t.resources:
            if t.resources[dev]['system']['primary']['name'] == resource:
                if kwargs.get('debug_log_on'):
                    t.log('debug', '{}: device: {} found'.format(func_name(), dev))
                dev_hdl = t.get_handle(resource=dev)
                break
        else:
            # out of luck, cannot find a handle
            raise Exception('cannot find device handle for {}'.format(resource))

    return dev_hdl

def get_device_info_from_handle(dh, **kwargs):
    '''
    get_device_info_from_handle
    '''
    hostname = dh.current_node.current_controller.name
    dev_host = dh.current_node.current_controller.host

    status = ''

    if hostname:
        for alias in t.resources:
            if t.resources[alias]['system']['primary']['name'] == hostname:
                if kwargs.get('debug_log_on'):
                    t.log('debug', '{}: device: {} found'.format(func_name(), alias))
                dh.tag = alias
                dh.name = hostname
                status = 'yaml_device'
                break
    elif dev_host:
        for alias in t.resources:
            for r_engine in t.resources[alias]['system']['primary']['controllers']:
                for mgt_ip in t.resources[alias]['system']['primary']['controllers']\
                                [r_engine]['mgt-ip']:
                    if mgt_ip == dev_host:
                        if kwargs.get('debug_log_on'):
                            t.log('debug', '{}: device: {} found'.format(func_name(), alias))
                        dh.tag = alias
                        dh.name = dev_host
                        status = 'yaml_device'
                        break

    if status == 'yaml_device':
        return True
    else:  ## Handles the external device, give the device tag the hostname
        if kwargs.get('debug_log_on'):
            t.log('debug', 'Based on DH string, device hostname and tag are not in t')
        dh.tag = 'external_device'
        dh.name = hostname
        #return dh.tag

def interface_handler_to_ifd(device, interface):
    '''
    examples:
     interface=${tv['r0__r0-r1__pic']}
     interface=r0-r1
     interface=tc10 (passing in the fv-tags)
     interface=xe-0/0/0

    will also handle an external
        interface, not in <your>.params.yaml
    '''
    t.log('debug', func_name())

    prefixes = ('ae', 'af', 'xe-', 'et-', 'ge-','mge-')

    ifd_list = []

    if isinstance(interface, str):
        # if the list is comma separated, break it into a list
        interface = [link.strip() for link in interface.split(',')]
    for each_interface in interface:
        if re.match('tv', each_interface, re.I):
            ifd_name = each_interface
            ifd_list.append(ifd_name)
        elif any(map(each_interface.startswith, prefixes)):
            ifd_list.append(each_interface)
        elif each_interface and device is 'external_device':
            ifd_list.append(each_interface)
        elif t.get_interface_list(resource=device, tag=each_interface):
            t_gil = t.get_interface_list(resource=device, tag=each_interface)
            for i in t_gil:
                ifd = tv['__'.join([device, i, 'pic'])]
                ifd_list.append(ifd)
        else:
            for intf in t.resources[device]['interfaces']:
                if intf == each_interface:
                    tv_ifd = tv['__'.join([device, each_interface, 'pic'])]
                    ifd_list.append(tv_ifd)

    if len(ifd_list) != 0:
        return ifd_list
    else:
        raise Exception('interface(s)/fv-tag: {} not found in t. Check syntax, interface, fv-tags or if valid.'\
                        .format(nice_string(interface)))

def get_pfe(dh, ifd):
    """
    just part of it, to start with
    For multi-chassis platforms, assume fpc has counted LCCs  already
    """
    model = str(dh.get_model())
    match = re.match(r'\w+-(\d+)/(\d+)/(\d+)(.*)', ifd)
    fpcslot = ''
    if match:
        fpcslot = match.group(1)
    else:
        t.log('error', 'cannot find fpc slot from {}'.format(ifd))
        return None

    pfe = None

    if re.match('mx80', model, re.I):
        pfe = 'tfeb0'
    elif re.match(r'mx104|mxtsr80', model, re.I):
        pfe = 'afeb0'
    elif re.match(r'ptx10001', model, re.I):
        pfe = 'fpc0.0' ## Argus pfe
    elif re.match(r'tx|(?:t|m32|mx|mxtsr)\d+|psd|vmx|ptx|vptx', model, re.I):
        pfe = 'fpc' + fpcslot
    elif re.match(r'm(10|7)i', model, re.I):
        pfe = 'cfeb'
    #Adding support for QFX10016
    elif re.match(r'qfx(10008|1002-72q|5110-48s-4c|5100-48S-6Q|5100|5200-32c-32q|10016|5110-32Q|5200-32c-32q)|ptx10003-80C|5210-64c', model, re.I):
        if dh.is_evo():
            pfe = 'cli-pfe'
        else:
            pfe = 'fpc' + fpcslot
    elif re.match(r'qfx(5120-48Y-8C|5200-48Y|10002|5110|10002-72Q|5210-64C)', model, re.I) or re.match(r'acx(710|5448-d|5448-m|5448)', model, re.I) or re.match(r'r(6675)', model, re.I):
        pfe = 'fpc0'
    elif re.match(r'srx(650|550|340|345)', model, re.I):
        pfe = 'fwdd'
    elif re.match(r'acx(500|1000|1100|2100|2200|4000|5000|5400|6360)', model, re.I):
        pfe = 'feb0'
    else:
        elog('error', 'cannot find pfe for {} on a {}'.format(ifd, model))
        pfe = None

    return pfe


def func_name():
    '''
    Defines function name within logging.
    - returns: <function_name>
    '''
    func_stack = stack()[1][3]
    out = ('{}()'.format(func_stack))
    return out

def me_object():
    '''
    Checks to see if Monitoring Engine is enabled, if enabled
    then return the exiting MonitoringEngine object.
    *** This is used for ME annotations ****
    '''
    if 'framework_variables' in t and t['framework_variables'] is not None and \
                            'fv-monitoring-engine' in t['framework_variables']:
        try:
            monitor = BuiltIn().get_library_instance('MonitoringEngine')
            return monitor
        except:
            return None

def mon_eng_annotate(message, **kwargs):
    '''
    annotate to Monitoring Engine
    - Looks to see if ME is running and gets the ME object from init.
    '''
    # t.log('debug', 'Bypasing Monitor Engine annotations, soon to come.')
    return True

    # if kwargs['me_object'] is not None:
        # kwargs['me_object'].monitoring_engine_annotate(annotation=\
                                # 'EE: {}'.format(message))
    # else:
        # return None

def robot_test_name():
    '''
    If Robot TEST_NAME, get the Testcase name and return
    - For proper formating, need to set as so in robot:
        (This will split based on the - )
        ex: TESTCASE 1 - foo in goo
            - returns: TESTCASE 1
        ex: TC 4.1.2 - goo in foo
            - returns: TC 4.1.2
    '''
    if BuiltIn().get_variable_value('${TEST_NAME}'):
        full_name = BuiltIn().get_variable_value('${TEST_NAME}')

        name = full_name[:15]

        if re.search('-', name):
            name = full_name.split('-')[0]
            return name
        else:
            return name

def elog(level=None, message=None, annotate=None, **kwargs):
    '''
    log to both console and device to show progress rel time
    optional: annotate to Monitoring Engine
    '''
    current_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S.%f")
    if level is not None and message is None:
        #User didn't pass in level; default to INFO
        message = level
        level = 'INFO'

    t.log_console("\n" + current_time + ": " + message)
    t.log(level, message)

    if annotate:
        mon_eng_annotate('testing', **kwargs)
    if level == 'error':
        return False

def nice_string(list_or_iterator):
    '''
    nice-string
    '''
    if isinstance(list_or_iterator, list):
        return ', '.join(str(x) for x in list_or_iterator)
    else:
        return list_or_iterator

def strip_xml_namespace(xml_string):
    

    xml = ET.fromstring(xml_string).getchildren()[0]
    query = ".//*[namespace-uri()!='']"
    for ele in xml.xpath(query):
        ele.tag = ET.QName(ele).localname
    return xml

def cli_pfe(dh, cmd):
    '''
    cli_pfe wrapper to create a cli-pfe mode for EVO pfe
    '''
    alias = get_dh_tag(dh)
    dh.su()

    if not alias in custom_modes:
        custom_modes[alias] = {}
    if 'cli-pfe' not in custom_modes[alias]:
        try:
            custom_modes[alias]['cli-pfe'] = \
                add_mode(device=dh, mode='cli-pfe', exit_command='exit', command='cli-pfe', pattern='>')
        except Exception:
            custom_modes[alias]['cli-pfe'] = False
    if custom_modes[alias]['cli-pfe']:
        res = execute_custom_mode(device=dh, mode='cli-pfe', command=cmd)
        return str(res)
    else:
        elog("Skipping cli-pfe command " + command['cmd'] + " (no cli-pfe available)")

def hshell(dh, cmd):
    '''
    cli_pfe wrapper to create a cli-pfe mode for EVO pfe
    '''
    alias = get_dh_tag(dh)
    dh.su()

    if not alias in custom_modes:
        custom_modes[alias] = {}
    if 'hshell' not in custom_modes[alias]:
        try:
            custom_modes[alias]['hshell'] = \
                add_mode(device=dh, mode='hshell', exit_command='exit', command='hshell', pattern='#')
        except Exception:
            custom_modes[alias]['hshell'] = False
    if custom_modes[alias]['hshell']:
        res = execute_custom_mode(device=dh, mode='hshell', command=cmd)
        return str(res)
    else:
        elog("Skipping hshell command " + command['cmd'] + " (no hshell available)")

def vhclient(dh, cmd):
    '''
    cli_pfe wrapper to create a cli-pfe mode for EVO pfe
    '''
    alias = get_dh_tag(dh)
    dh.su()

    if not alias in custom_modes:
        custom_modes[alias] = {}
    if 'vhclient' not in custom_modes[alias]:
        try:
            custom_modes[alias]['vhclient'] = \
                add_mode(device=dh, mode='vhclient', exit_command='exit', command='vhclient -s', pattern='#')
        except Exception:
            custom_modes[alias]['vhclient'] = False
    if custom_modes[alias]['vhclient']:
        res = execute_custom_mode(device=dh, mode='vhclient', command=cmd)
        return str(res)
    else:
        elog("Skipping vhclient command " + command['cmd'] + " (no vhclient available)")


def get_vty_pfe_for_line_card_mode(dh, fpc_slot=None):
    """
    This method returns the PFE format needed to login to VTY
    depending on the type of MPC's. For newer MPC's MPC10 and MPC11
    it returns FPC<n>.0 for line card specific login.


    :param obj device_handle
        **REQUIRED** Router's handle

    :param string fpc_slot
        **REQUIRED** Fpc number

    :return: string value in the format needed for logging to VTY

    :rtype: string
    """

    output = dh.cli(
            command="show chassis fpc pic-status | match \"Slot %s\"" %
            str(fpc_slot)).response()
    vty_pfe = fpc_slot
    if 'MPC10E' in output:
        vty_pfe = fpc_slot + '.0'
    elif 'MPC11E' in output:
        vty_pfe = fpc_slot + '.0'
    return vty_pfe

