#!/usr/bin/env python3
"""

Attribute Initialiser for Master Test Suites

Tool provides framework to control platform dependent varilables to be stored in a central inventory
Users can use attribute inventory variable to control they script execution

Supports invocation via Toby or standalone execution for users

"""

import os
import re
import sys
import posix
import getopt
import ast
import warnings

from io import StringIO
from copy import deepcopy
from collections.abc import MutableMapping

from ruamel.yaml import safe_load as load

from ruamel.yaml.constructor import DuplicateKeyError, DuplicateKeyFutureWarning
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError

import jnpr.junos.exception

from jnpr.junos import Device

import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.init.init import init
from jnpr.toby.utils.format_xml import normalize_xml
from jnpr.toby.utils.utils import _fetch_version
from jnpr.toby.utils.utils import log_file_version as _log_file_version
from jnpr.toby.hldcl.device import execute_cli_command_on_device as _execute_cli_command_on_device
from jnpr.toby  import __version__ as toby_version

# Global variables
INVENTORY_FILE_PATH = None
INVENTORY_INFORMATION = dict()
CONFIGURATION_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIGURATION_FILE_NAME = "inventory_configuration.yaml"
CHASSIS_CONFIGURATION = None
MODULE_CONFIGURATION = None
OVERRIDE_CONFIGURATION = None

def log(level=None, message=None):
    '''
    Custom logging function to handle Robot and Non-Robot execution
    '''

    # Check if any level or message defined
    if level is None and message is None:
        return

    # Validate arguments for logging
    if level is not None and message is None:
        message = level
        level = 'Info'
    if level is None:
        level = 'Info'

    # Identify method of invocation
    try:
        log_via_robot = bool(t.is_robot)
    except (NameError, AttributeError):
        log_via_robot = False

    # Redirect to t.log() if invoked via Robot framework else print()
    if log_via_robot:
        t.log(level, message)
    else:
        print("[ " + str(level).upper() + " ] " + str(message))

def log_yaml_file_version(abs_file_path):
    '''
    Fetch Git blob version from YAML file
    '''

    abs_file_path = "'" + abs_file_path + "'"

    # Identify method of invocation
    try:
        log_via_robot = bool(t.is_robot)
    except (NameError, AttributeError):
        log_via_robot = False

    if log_via_robot:
        _log_file_version(abs_file_path) # Used if invoked via Toby/Robot framework
    else:
        file_version = _fetch_version(abs_file_path) or None
        log("Debug", "File version : " + str(file_version))

def build_resource_template(device_name_list):
    '''
    Construct Toby YAML file if tool needs to run independently
    '''

    resource_template = '''t: \n  resources:'''
    resource_node_template = '''
    <host-name>:
      system:
        primary:
          fv-connect-channels: text
          controllers:
            unknown:
              domain: englab.juniper.net
              hostname: <host-name>
              mgt-ip: <host-name>
              osname: JunOS
          make: juniper
          model: unknown
          name: <host-name>
          osname: JunOS'''

    for device_name in device_name_list:
        resource_template += resource_node_template.replace('<host-name>', device_name)
    return resource_template

def flatten_dict(nested_dict, key_prefix='', key_separator='_'):
    '''
    Convert nested dictionary to flattened dictionary
    '''

    item_list = list()

    for key, value in nested_dict.items():

        flattened_key = key_prefix + key_separator + key if key_prefix else key

        if isinstance(value, MutableMapping):
            item_list.extend(flatten_dict(value, flattened_key, key_separator).items())
        else:
            item_list.append((flattened_key, value))

    return dict(item_list)

def config_inventory_pattern(file_name=CONFIGURATION_FILE_NAME, dir_path=CONFIGURATION_FILE_PATH):
    '''
    Configure inventory pattern for chassis and modules
    '''

    global CHASSIS_CONFIGURATION, MODULE_CONFIGURATION, OVERRIDE_CONFIGURATION # pylint: disable=global-statement

    config_inventory_pattern_failed = False # To track status of inventory configuration

    pattern_configuration = read_configuration_file(file_name, dir_path)

    log("Debug", "Inventory configuration file contains : " + str(pattern_configuration))

    if 'CHASSIS_CONFIGURATION' in pattern_configuration:
        log("Debug", "Loaded Chassis pattern configuration")
        CHASSIS_CONFIGURATION = pattern_configuration['CHASSIS_CONFIGURATION']
    else:
        log("Error", "Failed to load Chassis pattern configuration")
        config_inventory_pattern_failed = True

    if 'MODULE_CONFIGURATION' in pattern_configuration:
        log("Debug", "Loaded Module pattern configuration")
        MODULE_CONFIGURATION = pattern_configuration['MODULE_CONFIGURATION']
    else:
        log("Error", "Failed to load Module pattern configuration")
        config_inventory_pattern_failed = True

    if 'OVERRIDE_CONFIGURATION' in pattern_configuration:
        log("Debug", "Loaded Override pattern configuration")
        OVERRIDE_CONFIGURATION = pattern_configuration['OVERRIDE_CONFIGURATION']
    else:
        log("Error", "Failed to load Override pattern configuration")
        config_inventory_pattern_failed = True

    if config_inventory_pattern_failed:
        log("Error", "Failed to configure required inventory patterns")
        sys.exit(1)

def config_inventory_path(inventory_path=None):
    '''
    Configure custom or default path for inventory files
    '''

    global INVENTORY_FILE_PATH # pylint: disable=global-statement
    global INVENTORY_INFORMATION # pylint: disable=global-statement

    INVENTORY_INFORMATION = dict() # Reinitialise inventory information

    config_inventory_path_failed = False # To track status of inventory path configuration

    if inventory_path is not None:
        log("Warn", "Custom inventory path configured : " + inventory_path)
        INVENTORY_FILE_PATH = inventory_path
    else:
        # Generate file path based on inventory type
        try:
            environment_path = os.path.join(os.path.dirname(credentials.__file__), "environment.yaml")
            log("Debug", "Loading environment file : " + environment_path)
            environment = load(open(environment_path))
            log("Debug", "Environment file contains : " + str(environment))
            dir_path = environment['attribute-inventory-path'] # '/volume/regressions/toby/test-suites/MTS/attribute_vars'
        except (KeyError, TypeError):
            log("Error", "Unable to fetch 'Attribute Inventory' location from environment file")
            config_inventory_path_failed = True
        except FileNotFoundError:
            log("Error", "Unable to find environment file to fetch 'Attribute Inventory' location")
            config_inventory_path_failed = True
        except IOError:
            log("Error", "Unable to access environment file to fetch 'Attribute Inventory' location")
            config_inventory_path_failed = True
        finally:
            if config_inventory_path_failed:
                sys.exit(1)
            else:
                INVENTORY_FILE_PATH = dir_path

def read_yaml_file(abs_file_path):
    '''
    Process and parse YAML file
    '''

    read_yaml_file_failed = False # To track status of file load operation

    # Access and process file content
    if os.path.exists(abs_file_path):
        try:
            with open(abs_file_path) as file_handle:
                log("Debug", "Accessing file : " + abs_file_path)
                warnings.simplefilter("error", DuplicateKeyFutureWarning) # Raise duplicate key warning as error
                file_content = load(file_handle.read()) # YAML file load from ruamel.yaml
        except IOError:
            log("Error", "Unable to read file : " + abs_file_path)
            read_yaml_file_failed = True
        except (ScannerError, ParserError):
            log("Error", "Failed to parse file content in proper format")
            read_yaml_file_failed = True
        except (DuplicateKeyError, DuplicateKeyFutureWarning):
            log("Error", "Duplicate keys found during parsing of file")
            read_yaml_file_failed = False
            with open(abs_file_path) as file_handle:
                log("Warn", "Attempting to load file with duplicate keys")
                warnings.simplefilter("ignore", DuplicateKeyFutureWarning) # Ignore duplicate key warning
                file_content = load(file_handle.read()) # Attempt YAML file load from ruamel.yaml with duplicates
        finally:
            if read_yaml_file_failed:
                sys.exit(1)
            else:
                log_yaml_file_version(abs_file_path) # Log blob version from YAML file for tracking
    else:
        log("Error", "Unable to access file : " + abs_file_path)
        return dict()

    return file_content

def read_configuration_file(file_name, dir_path):
    '''
    Reads configuration file after validating their availability
    '''

    # Process arguments and create file access path
    file_path = os.path.join(dir_path, file_name)
    abs_file_path = os.path.abspath(file_path)

    return read_yaml_file(abs_file_path)

def read_inventory_file(fru_name):
    '''
    Reads inventory files after validating their availability
    '''

    # Process arguments and create file access path
    base_folder = os.path.join(INVENTORY_FILE_PATH, 'inventory')
    file_name = fru_name + '.' + 'yaml'
    file_path = os.path.join(base_folder, file_name)
    abs_file_path = os.path.abspath(file_path)

    return read_yaml_file(abs_file_path)

def fetch_inventory_info(fru_name):
    '''
    Fetch information from inventory files and cache for later usage on-demand
    '''

    global INVENTORY_INFORMATION # pylint: disable=global-statement

    # Confirm if it is initial call to fetch inventory information
    if not INVENTORY_INFORMATION.get(fru_name):
        INVENTORY_INFORMATION[fru_name] = {} # Initialize module record
        INVENTORY_INFORMATION[fru_name] = read_inventory_file(fru_name)

    return deepcopy(INVENTORY_INFORMATION[fru_name])

def filter_inventory_info(full_inventory, filter_desc):
    '''
    Filter attribute inventory information with matching inventory
    '''

    filtered_inventory = dict()

    # Update default values to filtered inventory
    if full_inventory.get('default'):
        filtered_inventory = full_inventory.get('default')
        filtered_inventory.update({'desc': "default"})
    else:
        log("Info", "No default information found")

    # Update specific values based on filter and overrrite default values
    if full_inventory.get(filter_desc):
        filtered_inventory.update(full_inventory.get(filter_desc))
        filtered_inventory.update({'desc': filter_desc})
    else:
        log("Warn", "No specific information found for '" + filter_desc + "'")

    return deepcopy(filtered_inventory)

def override_sub_module_attributes_local(inventory, override_inventory, module_name, sub_module_desc):
    '''
    Merge and override attribute values based on override options defined under same module
    '''

    if sub_module_desc in override_inventory:

        # For debug purpose
        log("Debug", "Values found for '" + module_name + "'")
        log("Debug", inventory)
        log("Debug", "Override values found for '" + module_name + "'")
        log("Debug", override_inventory[sub_module_desc])

        inventory.update(override_inventory[sub_module_desc])

        # For debug purpose
        log("Debug", "Values after merge for '" + module_name + "'")
        log("Debug", inventory)

    return inventory

def override_sub_module_attributes_external(inventory, override_inventory, sub_module_name, sub_module_key):
    '''
    Merge and override attribute values based on override options defined under external module
    '''

    if sub_module_key in inventory:
        if 'desc' in inventory[sub_module_key]:
            sub_module_desc = inventory[sub_module_key]['desc']
            if sub_module_desc in override_inventory:

                # For debug purpose
                log("Debug", "Values found for '" + sub_module_name + "'")
                log("Debug", inventory[sub_module_key])
                log("Debug", "Override values found for '" + sub_module_name + "'")
                log("Debug", override_inventory[sub_module_desc])

                inventory[sub_module_key].update(override_inventory[sub_module_desc])

                # For debug purpose
                log("Debug", "Values after merge for '" + sub_module_name + "'")
                log("Debug", inventory[sub_module_key])
        else:
            for sub_module_num in inventory[sub_module_key]:
                if 'desc' in inventory[sub_module_key][sub_module_num]:
                    sub_module_desc = inventory[sub_module_key][sub_module_num]['desc']
                    if sub_module_desc in override_inventory:

                        # For debug purpose
                        log("Debug", "Values found for '" + sub_module_name + "' : " + sub_module_num)
                        log("Debug", inventory[sub_module_key][sub_module_num])
                        log("Debug", "Override values found for '" + sub_module_name + "' : " + sub_module_num)
                        log("Debug", override_inventory[sub_module_desc])

                        inventory[sub_module_key][sub_module_num].update(override_inventory[sub_module_desc])

                        # For debug purpose
                        log("Debug", "Values after merge for '" + sub_module_name + "' : " + sub_module_num)
                        log("Debug", inventory[sub_module_key][sub_module_num])

    return inventory

def override_module_attributes(inventory, module_name, module_key, module_override):
    '''
    Merge and override attribute values based on various module types
    '''

    var_digit = re.compile(r'^\d+$') # Matches number from variable

    # Merge override options available for sub modules from module component
    for sub_module in module_override.values(): # pylint: disable=too-many-nested-blocks

        sub_module_override_pattern = sub_module['override_pattern']
        sub_module_name = sub_module['name']
        sub_module_key = sub_module['key']
        sub_module_merge_local = sub_module.get('merge_local', False) # Used to control merge location for override values

        if sub_module_override_pattern in inventory[module_key]:
            log("Info", "Override values found for '" + sub_module_name + "' under '" + module_name + "'")
            override_inventory = inventory[module_key][sub_module_override_pattern]
            if sub_module_merge_local:
                sub_module_desc = inventory[sub_module_key]['desc']
                inventory = override_sub_module_attributes_local(inventory,
                                                                 override_inventory,
                                                                 module_name, sub_module_desc)
            else:
                inventory = override_sub_module_attributes_external(inventory,
                                                                    override_inventory,
                                                                    sub_module_name, sub_module_key)
            inventory[module_key].pop(sub_module_override_pattern)
        else:
            for module_num in inventory[module_key]:
                if isinstance(inventory[module_key][module_num], dict) and re.match(var_digit, module_num):
                    if sub_module_override_pattern in inventory[module_key][module_num]:
                        log("Info", "Override values found for '" + sub_module_name + "' under '" + module_name + "' : " + module_num)
                        override_inventory = inventory[module_key][module_num][sub_module_override_pattern]
                        if sub_module_merge_local:
                            sub_module_desc = inventory[sub_module_key]['desc']
                            inventory[module_key][module_num] = override_sub_module_attributes_local(inventory[module_key][module_num],
                                                                                                     override_inventory,
                                                                                                     module_name, sub_module_desc)
                        else:
                            inventory[module_key][module_num] = override_sub_module_attributes_external(inventory[module_key][module_num],
                                                                                                        override_inventory,
                                                                                                        sub_module_name, sub_module_key)
                        inventory[module_key][module_num].pop(sub_module_override_pattern)

    return inventory

def override_attributes(inventory):
    '''
    Merge and override attribute values based on inventory modules
    '''

    if OVERRIDE_CONFIGURATION is not None:

        # Merge override options available for supported modules
        for module in OVERRIDE_CONFIGURATION.values():

            module_name = module['name']
            module_key = module['key']
            module_override = module['override']

            # Process override if module is present in inventory
            if module_key in inventory:

                log("Info", "Processing override configuration for '" + module_name + "'")
                inventory = override_module_attributes(inventory, module_name, module_key, module_override)

    else:
        log("Warn", "Attribute override feature configuration is not available")

    return inventory

def populate_module_attributes(module_filter_list, module_info, module_name, module_inventory_name, module_key, module_index):
    '''
    Populate attribute variable based on device inventory per module
    '''

    # For debug purpose
    log("Debug", "'" + module_name + "' information under process")
    log("Debug", module_info)

    var_num = re.compile(r'.*?(\d+)$') # Matches ending number from string

    final_inventory = dict()

    if module_filter_list: # pylint: disable=too-many-nested-blocks

        # For debug purpose
        log("Debug", "Processing filtered '" + module_name + "' inventory : " + str(module_filter_list))

        # Parse module components from inventory
        for module_info_key in module_filter_list:
            # Parse individual module component from inventory
            log("Info", "Processing '" + module_name + "' inventory : " + str(module_info_key))
            module_desc = module_info[module_info_key][0]
            module_inventory = fetch_inventory_info(module_inventory_name)
            module_filtered_inventory = filter_inventory_info(module_inventory, module_desc)

            # For debug purpose
            log("Debug", "'" + module_name + "' inventory content")
            log("Debug", module_filtered_inventory)

            # Update module record to final inventory
            if module_filtered_inventory:
                match_module_num = re.match(var_num, module_info_key)
                if match_module_num:
                    module_num = match_module_num.group(1)
                else:
                    module_num = "0" if module_index else None
                if not final_inventory.get(module_key):
                    final_inventory[module_key] = {} # Initialize module record
                if module_num:
                    final_inventory[module_key].update({module_num: module_filtered_inventory})
                else:
                    final_inventory.update({module_key : module_filtered_inventory})

                # Check module contains sub-module information
                try:
                    sub_module_info = module_info[module_info_key][1]

                    if sub_module_info and isinstance(sub_module_info, dict):
                        if module_num:
                            final_inventory[module_key][module_num].update(populate_chassis_attributes(sub_module_info))
                        else:
                            final_inventory[module_key].update(populate_chassis_attributes(sub_module_info))

                except IndexError:
                    log("Info", "No sub-module inventory found under '" + module_name + "'")

    return deepcopy(final_inventory)

def populate_chassis_attributes(chassis_info):
    '''
    Populate attribute variables based on device inventory per chassis
    '''

    # For debug purpose
    log("Debug", "Inventory information under process")
    log("Debug", chassis_info)

    final_inventory = dict() # Initialize record

    for module in MODULE_CONFIGURATION.values():

        # Filter supported chassis modules from chassis inventory
        module_pattern = re.compile(module['pattern'])
        module_filter_list = list(filter(module_pattern.match, chassis_info.keys()))

        if module_filter_list:
            final_inventory.update(populate_module_attributes(module_filter_list, chassis_info, module['name'], module['file'], module['key'], module['index']))

    return final_inventory

def populate_attributes(device_info):
    '''
    Populate attribute variables based on device inventory
    '''

    # For debug purpose
    log("Debug", "'Device' information under process")
    log("Debug", device_info)

    # Supported chassis types from device inventory loaded from configuration file
    chassis_pattern = re.compile(CHASSIS_CONFIGURATION['pattern'])

    final_inventory = dict() # Initialize record

    # Filter supported chassis types from device inventory
    chassis_type_filter_list = list(filter(chassis_pattern.match, device_info.keys()))

    if chassis_type_filter_list:

        # For debug purpose
        log("Debug", "Processing filtered 'Chassis' types : " + str(chassis_type_filter_list))

        # Parse chassis types from device inventory
        for chassis_type_info_key in chassis_type_filter_list:
            # Parse individual chassis from device inventory
            log("Info", "Processing 'Chassis' inventory type : " + str(chassis_type_info_key))
            chassis_type_info = device_info[chassis_type_info_key]
            final_inventory[chassis_type_info_key] = override_attributes(populate_chassis_attributes(chassis_type_info))
    else:
        # Parse stand-alone chassis from device inventory
        final_inventory = override_attributes(populate_chassis_attributes(device_info))

    flattened_inventory = flatten_dict(final_inventory)

    # For debug purpose
    log("Debug", "'Attribute Initialiser' information in nested dictionary")
    log("Debug", final_inventory)
    log("Debug", "'Attribute Initialiser' information in flattened dictionary")
    log("Debug", flattened_inventory)

    return flattened_inventory

def parse_device_inventory(inventory, search_tag="./chassis"):
    '''
    Parse device inventory in XML to dictionary format
    '''

    inventory_dict = dict()

    # Process chassis under multi-chassis environment
    for chassis in inventory.findall("./multi-routing-engine-item"):

        chassis_name = str(chassis.findtext(".//re-name"))

        # Process modules under chassis inventory
        if chassis.find(".//chassis") is not None:
            inventory_dict[chassis_name] = parse_device_inventory(chassis, ".//chassis")

    # Process components under inventory information
    for module in inventory.findall(search_tag):

        module_name = str(module.findtext(".//name"))
        module_desc = str(module.findtext(".//description"))

        module_desc_list = list()
        module_desc_list.append(module_desc)

        # Process modules under chassis and merge with chassis inventory level
        if module.find("./chassis-module") is not None:
            inventory_dict.update(dict(parse_device_inventory(module, "./chassis-module")))

        # Process sub modules under modules and merge under module inventory level
        if module.find("./chassis-sub-module") is not None:
            module_desc_list.append(parse_device_inventory(module, "./chassis-sub-module"))

        # Process sub sub modules under sub modules and merge under sub module inventory level
        if module.find("./chassis-sub-sub-module") is not None:
            module_desc_list.append(parse_device_inventory(module, "./chassis-sub-sub-module"))

        # Process sub sub sub modules under sub sub modules and merge under sub sub module inventory level
        if module.find("./chassis-sub-sub-sub-module") is not None:
            module_desc_list.append(parse_device_inventory(module, "./chassis-sub-sub-sub-module"))

        inventory_dict[module_name] = module_desc_list

    return inventory_dict if inventory_dict else None

def process_resources(t_var):
    '''
    Access resources and process inventory information
    '''

    attribute_vars = dict()

    for resource_id in t_var.get_junos_resources():

        # Fetch inventory information per node
        device_name = t_var.get_t(resource=resource_id, attribute='name')
        t_var.log("Processing resource : " + device_name)
        device_handle = t_var.get_handle(resource=resource_id)
        response = _execute_cli_command_on_device(device=device_handle, command='show chassis hardware', format='xml')

        # Process inventory information and populate attribute variables per node
        chassis_info = parse_device_inventory(normalize_xml(response))
        attribute_vars[resource_id] = populate_attributes(chassis_info)

    return attribute_vars

def pyez_based_access(device_name_list):
    '''
    Handle PyEZ based execution via command line
    '''

    attribute_vars = dict()

    # Process individual devices from device list
    for device_name in device_name_list:

        # Connect and fetch chassis inventory from device
        device_handle = Device(host=device_name, user='regress', password='MaRtInI')
        try:
            device_handle.open()
            hw_inventory = device_handle.rpc.get_chassis_inventory()
        except jnpr.junos.exception.ConnectAuthError:
            log("Error", "Authentication failed while connecting to device")
            sys.exit(1)
        except jnpr.junos.exception.ConnectRefusedError:
            log("Error", "Connection refused by device. Verify NETCONF is enabled on device")
            sys.exit(1)
        except jnpr.junos.exception.ConnectUnknownHostError:
            log("Error", "Please check device name")
            sys.exit(1)
        except jnpr.junos.exception.ConnectTimeoutError:
            log("Error", "Connection to device timed out")
            sys.exit(1)
        except jnpr.junos.exception.ConnectError:
            log("Error", "Connection failed to device")
            sys.exit(1)
        else:
            # After successful connection parse device inventory
            chassis_info = parse_device_inventory(hw_inventory)
            attribute_vars[device_name] = populate_attributes(chassis_info)
        finally:
            device_handle.close()

    return attribute_vars

def toby_based_access(device_name_list):
    '''
    Handle Toby based execution via command line
    '''

    # Toby information for reference
    log("Info", "Toby version : " + toby_version)

    # Create and save YAML based resource template file
    resource_template = build_resource_template(device_name_list)
    uniq_id = posix.getpid()
    resource_yaml = '/tmp/attribute_init_topo_' + str(uniq_id) + '.yaml'
    try:
        with open(resource_yaml, 'w') as file_handle:
            file_handle.write(resource_template)
            file_handle.flush()
    except IOError:
        log("Error", "Could not write file : " + resource_yaml)
        sys.exit(1)
    finally:
        file_handle.close()

    # Initialize resources and create 't' object for Toby
    log("Info", "Initializing resources")
    try:
        stdout_orig = sys.stdout # Disable Toby console logging during device initialization
        sys.stdout = StringIO()
        t = init()
        t.Initialize(init_file=resource_yaml)
    except jnpr.toby.utils.utils.RunMultipleException:
        sys.stdout = stdout_orig # Enable Toby console logging after failure
        log("Error", "Exception occured while initializing resources")
        sys.exit(1)
    finally:
        sys.stdout = stdout_orig # Enable Toby console logging after device initialization
    log("Info", "Resource initialization completed")

    # Remove YAML based resource template file
    if uniq_id:
        os.remove(resource_yaml)

    # Process resources and generate attribute variables
    return process_resources(t)

def get_attribute_variables(inventory_path=None):
    '''
    Handle Toby based execution via script
    '''

    log("Generating attribute variables for Juniper resources")

    # Configure inventory pattern for chassis and modules
    config_inventory_pattern()

    # Configure inventory file path with custom or default value
    config_inventory_path(inventory_path)

    # Process resources and generate attribute variables
    return flatten_dict(process_resources(t))

def cmd_access():
    '''
    Default function to handle command line calls
    '''

    # Decale default values for variables
    resource_list = None
    access_method = 'Toby'
    online_mode = None
    offline_mode = None
    attribute_vars = dict()
    inventory_path = None
    custom_inventory_path = False

    # Fetch and parse command line arguments
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hr:m:p:", ["help", "resources=", "method=", "path=", "online", "offline"])
    except getopt.GetoptError as error:
        log("Error", "" + str(error))
        print_help()
        sys.exit(2)

    # Choose execution mode based on arguments if any
    for arg in args:
        if arg.lower() == 'online':
            online_mode = True
        if arg.lower() == 'offline':
            offline_mode = True

    # Assign values for variables based on arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit(2)
        elif opt in ("-r", "--resources"):
            resource_list = arg
        elif opt in ("-m", "--method"):
            access_method = arg
        elif opt == "--online":
            online_mode = True
        elif opt == "--offline":
            offline_mode = True
        elif opt in ("-p", "--path"):
            custom_inventory_path = True
            inventory_path = arg

    # Configure inventory path with custom or default value
    if custom_inventory_path:
        config_inventory_path(inventory_path)
    else:
        config_inventory_path()

    # Configure inventory pattern for chassis and modules
    config_inventory_pattern()

    # Verify access method mentioned via arguments
    if access_method.lower() != 'toby' and access_method.lower() != 'pyez':
        log("Error", "Invalid access method mentioned")
        print_help()
        sys.exit(2)

    # Decide on execution mode with default mode as offline
    if online_mode and offline_mode:
        log("Error", "Invalid mode selection")
        print_help()
        sys.exit(2)
    elif online_mode:
        log("Info", "Running in 'Online' mode")

        if resource_list is None:
            resource_list = input("Please provide list of resources separated with comma : ").strip()

        device_name_list = resource_list.split(',')

        # Decide on access method to fetch information from nodes
        if access_method.lower() == 'toby':
            log("Info", "Using 'Toby' based access method")
            attribute_vars = toby_based_access(device_name_list)
        else:
            log("Info", "Using 'PyEZ' based access method")
            attribute_vars = pyez_based_access(device_name_list)
    else:
        log("Info", "Running in 'Offline' mode")

        # Parse input from user in dictionary format
        try:
            device_info = ast.literal_eval(input("Please provide device information to be processed : ").strip())
            attribute_vars['dummy_device'] = populate_attributes(device_info)
        except SyntaxError:
            log("Error", "Please make sure device information is provided in dictionary format")
            sys.exit(2)

    log("Info", "'Attribute Variables'")
    log("Info", attribute_vars)

def print_help():
    '''
    Print help message for standalone executions
    '''

    print('''
Usage: attribute_init [online|offline]
       attribute_init online [-r resources] [-m Toby|PyEZ]
       attribute_init offline
       attribute_init [-p <custom-inventory-path>]

Attribute Initialiser for Master Test Suites

   -h|--help                   Show this help message and exit
   online|offline              Choose execution mode (default:offline)
   -m|--method [Toby|PyEZ]     Provide device access method (default:Toby)
   -r|--resources              List of resources seprated with colon
   -p|--path                   Configure custom inventory path
''')

if __name__ == "__main__":
    cmd_access()

