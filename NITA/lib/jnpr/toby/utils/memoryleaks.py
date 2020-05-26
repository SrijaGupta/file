import re
import traceback
import os
from sys import exit
from time import sleep
from jnpr.toby.hldcl.juniper.junos import Juniper


# def task_memory_command
def task_memory_command(device, file_name):
    """
    Robot Usage Example :
	${dh} =  Get Handle   resource=r1
	${result} =  Task Memory Command  device=${dh}    file_name='memoryleaks'

    To save 'show task memory detail' command output into a file.
    :param device:
        **REQUIRED** device handle need to pass
    :param file_name:
        **REQUIRED** File name to store task memory details.
    :return:
        TRUE if task memory details saved successfully
        FALSE if task mempory details not saved successfully
    """
    sub = function_name(device)
    response=device.cli(command="show task memory detail").response()
    if response :
        print ("Output of the show task memory detail: \n %s"%response)
        response=device.cli(command="show task memory detail | save %s" % file_name)
        return True
    else:
        device.log(message = "This device is not having the task memory details", level= "debug")
        return False
    # end def task_memory_command


# def task_memory_snapshot
def task_memory_snapshot(device):
    """
    Robot Usage Example :
      ${dh} =  Get Handle   resource=r1
      ${result} =  Task Memory Snapshot  device=${dh}

    Gets the allocated blocks and bytes of memory for every task block in a device.
    :params device:
       **REQUIRED** device handle need to pass
    :return: Dictionary of task block names and their memory allocation details
    """
    memory_result = {}
    start = 0
    response = device.cli(command="show task memory detail").response()
    if response:
        for line in response.split('\n'):
            if re.search('Allocator Memory Report', line):
                start = 1
            if not start:
                continue
            if re.search('Malloc Usage Report', line):
                break
            pattern = r'^\s+(\w+[\w\d\.]+|\w+[\w\d\.]+ [\w\d\.]+)\s+(\d+)' + \
                      r'\s+(\d+)\s+([0-9_]+)\s+([0-9_]+)'
            match = re.search(pattern, line)
            if match:
                memory_result[match.group(1) + match.group(2)] = [match.group(4), match.group(5)]
    else:
        device.log(message = "This device is not having the task memory details", level= "debug")
        return {}
    return memory_result
# end def task_memory_snapshot


# def __proto_memoryleaks
def __proto_memoryleaks(device, **kwargs):
    """
    Check memory leaks for all/any task block name given as a regular expression.

    :param device:
     	**REQUIRED** device handle need to pass
    :param regex:
	    *OPTIONAL* task block name as a regular expression
    :param tag:
        **REQUIRED** Tag number required
    :return:
	    TRUE/OK if no memory leak for the task block(s)
	    FALSE/Not_Ok if memory leak found for the task block(s)
    """
    valid_keys = ['regex', 'tag']
    required_keys = []
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    regex = kwargs.get("regex", '')
    tag = kwargs.get("tag", '')
    sub = function_name(device)
    status = True
    records = task_memory_snapshot(device)
    for name in sorted(records):
        if regex and not re.search(regex, name):
            device.log(message="%s:task name '%s'doesn't match %s Skipping..."
                       % (sub, name, regex), level='debug')
            continue
        records_blocks = records[name][0]
        records_bytes = records[name][1]
        device.log(message="%s:%s did not free up memory blocks/bytes" % (sub, tag) +
                   "for %s(%s/%s)." % (name, records_blocks, records_bytes), level='error')
        status = False
    return status
# end def __proto_memoryleaks


#def check_memory_leaks
def check_memory_leaks(device, **kwargs):
    """
    Robot Usage Example :
         ${dh} =   Get Handle   resource=r1
	 ${result} =   Check Memory Leaks  device=${dh}  router=springpark   protocol=ip   action=set   interval=15
 
    Checks memory leaks status after deactivating protocol and routing instances.
    :param router:
	    **REQUIRED** Router device name which needs memory leaks check
    :param protocol:
	    **REQUIRED** The protocol to be deactivated
    :param action:
	    **REQUIRED** Action to be taken on the protocol/router instances
    :param cmd:
	    *OPTIONAL* Command to be executed on device
    :param timeout:
	    *OPTIONAL* Maximum time to wait for memory leak check. Default 60 seconds.
    :param interval:
	    *OPTIONAL* Time duration between two memory leak checks. Default 15 seconds.
    :param reset_config:
	    *OPTIONAL* Set to reset the configuration. Default False.
    :param regex:
	    *OPTIONAL* Task block name as regular expression, Default generated from protocols.
    :param keep_rt_instance:
	    *OPTIONAL* Set to not change(not deactivate) the router instance, Default False.
    :return :
	    TRUE/OK if no memory leak for the task block(s)
	    FALSE/Not_Ok if memory leak found for the task block(s)
    """
    valid_keys = ['protocol', 'action', 'cmd', 'timeout', 'interval',
                  'reset_config', 'regex', 'keep_rt_instance']
    required_keys = ['protocol','action']
    kwargs = check_args(device, valid_keys, required_keys, kwargs)
    sub = function_name(device)
    status = True
    #rh_name = device.get_host() #not yet implemented get_host
    #rh_tag = device.get_tag()   #not yet implemented get_tag
    #rh_TAG = rh_tag+" ("+rh_name+")"
    proto = kwargs.get("protocol")
    action = kwargs.get("action")
    proto_str = ", ".join(proto).upper()
    config_arr = []
    protocol = proto if  isinstance(proto, list) else [proto]
    action = action if  isinstance(action, list) else [action]
    if kwargs.get('cmd'):
        cmd = kwargs.get('cmd')
        cmd = cmd if isinstance(cmd, list) else [cmd]
    reset_config = True if kwargs.get('reset_config') else False
    keep_rt_instance = True if kwargs.get('keep_rt_instance') else False
    regex = kwargs.get('regex', '(' + '|'.join(protocol) + ')')
    regex = re.compile(regex)
    timeout = kwargs.get('timeout', 60)
    interval = kwargs.get('interval', 15)
    config_file = "/tmp/mleak_test.config.%s"%(os.getpid())
    if reset_config:
        device.config(command_list=["save %s"%config_file])
    device.log(message="%s: Check for %s memory leak [REGEX:%s]."%(sub, proto_str, regex))
    response = device.cli(command="show task memory detail").response()
    if response:
        device.log("Memory leaks status before deactivating the protocols and routing instances")
        print("output of show task memory details\n %s"%response)
    else:
        device.log("No memory leaks status before deactivating the protocols and routing instances")
    for proto in protocol:
        response = __config_build__(cmd=["%s protocols %s"%(action[0], proto)])
        config_arr.append(response)
    if kwargs.get('cmd'):
        response = __config_build__(cmd=cmd)
        config_arr.append(response)
    if not keep_rt_instance:
        response = __config_build__(cmd=["%s routing-instances"%action[0]])
        config_arr.append(response)
    for item in range(0, len(config_arr)):
        device.config(command_list=config_arr[item])
    # Added as part of TT-30637
    device.log(message="Proceeding for checking commit error\n",
               level='info')
    try:
        device.commit().response()
    except Exception as err:
        device.log(message=err, level='Error')
    while timeout >= 0:
        device.log(message="%s: Checking %s memory allocations, expired \
	          in %s seconds."%(sub, proto_str, timeout), level='error')
        sleep(interval)
        status = __proto_memoryleaks(device, regex=regex) #tag = rh_TAG
        if status:
            device.log(message="%s: All %s memory have been deallocated."%(sub, proto_str),
                       level='info')
            break
        timeout = timeout - interval
        device.log(message="%s: %s memory still in use. Checking again \
	                      after %s seconds."%(sub, proto_str, interval), level='warn')
    if reset_config:
        device.load_config(remote_file=config_file, format="text")
        device.shell(command="rm -f %s"%config_file)
    return status
#end def check_memory_leaks


# def check_args
def check_args(device, valid_key, required_key, kw_dict):
    """
        -Check all value in valid_key list is existed in kw_dict
        -Check all value in requred_key list is existed
        in kw_dict and it is defined

    :param device:
        **REQUIRED** Device handle
    :param valid_key:
        **REQUIRED** the list of valid keys need to be checked (list)
    :param required_key:
        **REQUIRED** the list of required keys need to be checked (list)
    :param kw_dict:
        **REQUIRED** all arguments need to be checked  (dict)

    :return:
        kw_dict: all arguments
        Eg:
            valid_keys = ['name', 'family', 'term', 'match','action',
            'method', 'if_specific', 'commit']
            required_key = ['name', 'term']
            kwargs = check_args(device, valid_keys, required_key, kwargs)
    """
    # Check valid_value in kwargs
    for current_key in kw_dict.keys():
        if current_key not in valid_key:
            device.log(message="%s value is not valid" % current_key, level='error')
            raise Exception("%s value is not valid" % current_key)
    # Check all value in required_key list is existed
    for required_k in required_key:
        if required_k not in valid_key or kw_dict[required_k] == '':
            device.log(message="%s value is not defined" % required_k,
                       level='error')
            raise Exception("%s value is not defined" % required_k)
    return kw_dict

# end def check_args


# def function_name
def function_name(device):
    """
        To get the fucntion name.

    :param device:
        **REQUIRED** Device handle

    :returns:
        The function name
    """
    device.log(message="Getting function name ...", level='debug')
    return traceback.extract_stack(None, 2)[0][2]
# end function_name


##################################################
#              STUB FUNCTIONS                    #
##################################################
def __config_build__(cmd):
    '''
        Add to a list of config commands to execute later
    :param cmd list
        The command list to push to the config list
    '''
    config_arr = []
    config_arr.extend(cmd)
    return config_arr
