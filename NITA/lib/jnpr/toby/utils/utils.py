#! /usr/bin/python
"""
General utilities which are useful throughout TOBY.
"""
# pylint: disable=import-error,anomalous-backslash-in-string
from threading import Thread
from threading import Lock
from queue import Queue
import time
import psutil
import datetime
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.logger.logger import get_log_dir as get_script_log_dir
from jnpr.toby.utils.Vars import Vars
import subprocess
import re
import ruamel.yaml as yaml
import os

lock = Lock()

def server_cpu_usage(threshold=90):
    """This function provides the cpu details of the underlying server
    during script execution.

    The function provides CPU usage and memory utilization.
    """
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()[2]
    t.log(level='INFO', message="Execution host CPU utilization: %s percent"% cpu_percent)
    t.log(level='INFO', message="Execution host memory utilization: %s percent"% memory_percent)
    if cpu_percent > threshold or memory_percent > threshold:
        t.log(level='WARN', message="CPU utilization or Memory utilization is more than threshold value of 90%, you may want to switch to other server")

def _call_string(target, args, kwargs):
    """A string representation of the call to target(*args, **kwargs)

    Used for logging or printing the equivalent call that is made from
    run_multiple. It does NOT actually invoke the call.

    Args:
        target: A callable object
        args: A list of positional parameters to be passed to target()
        kwargs: A dict of keyword parameters to be passed to target()

    Returns:
        A string representing the call to target(*args, **kwargs)
    """
    try:
        target_name = target.__name__
    except AttributeError:
        # Occurs when target_name isn't a callable.
        # This helps to see you're trying to invoke something as a callable
        # that won't actually work.
        target_name = str(target)
    quoted_args = []
    for arg in args:
        if isinstance(arg, str):
            arg = "'%s'" % (arg)
        quoted_args.append(arg)
    quoted_kwargs = []
    for (key, value) in kwargs.items():
        if isinstance(value, str):
            new_value = "'%s'" % (value)
        else:
            new_value = value
        quoted_kwargs.append("%s=%s" % (key, new_value))
    return "%s(%s)" % (target_name,
                       ', '.join(map(str, (quoted_args + quoted_kwargs))))


class RunMultipleTimeoutException(Exception):
    """Indicates timeout while waiting for a thread of run_multiple to finish.

    Attributes:
        target: Callable object the thread is executing.
        delay: Float of number of seconds delay before target was started.
        args: List of positional arguments passed to target.
        kwargs: Dict of keyword arguments passed to target.
        timeout: Float of number of seconds which expired before this
            timeout exception was raised.
    """
    def __init__(self, target, delay, args, kwargs, timeout):
        """Initialize with information about the thread which timed out.

        Args:
            target: Callable object the thread is executing.
            delay: Float of number of seconds delay before target was started.
            args: List of positional arguments passed to target.
            kwargs: Dict of keyword arguments passed to target.
            timeout: Float of number of seconds which expired before this
                timeout exception was raised.

        Returns:
            Instance of a RunMultipleTimeoutException.
        """
        Exception.__init__(self)
        self.target = target
        self.delay = delay
        self.args = args
        self.kwargs = kwargs
        self.timeout = timeout

    def __str__(self):
        """The string representation of the object.
        """
        return self.__repr__()

    def __repr__(self):
        """The string representation of the object.

        Includes information on the timeout, the target invocation, and delay.
        """
        return "%s('Timeout after %s seconds. Invoked: %s Delay: %s')" % \
               (self.__class__.__name__,
                self.timeout,
                _call_string(self.target, self.args, self.kwargs),
                self.delay)


class RunMultipleFailedStartException(Exception):
    """Indicates a thread of run_multiple failed to start.

    Attributes:
        target: Callable object the thread attempted to execute.
        delay: Float of number of seconds delay before target was started.
        args: List of positional arguments passed to target.
        kwargs: Dict of keyword arguments passed to target.
    """
    def __init__(self, target, delay, args, kwargs):
        """Initialize with information about the thread which failed to start.

        Args:
            target: Callable object the thread attempted to execute.
            delay: Float of number of seconds delay before target was started.
            args: List of positional arguments passed to target.
            kwargs: Dict of keyword arguments passed to target.

        Returns:
            An instance of a RunMultipleFailedStartException.
        """
        Exception.__init__(self)
        self.target = target
        self.delay = delay
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """The string representation of the object.
        """
        return self.__repr__()

    def __repr__(self):
        """The string representation of the object.

        Includes information on the attempted target invocation and delay.
        """
        return "%s('Failed to start. Invoked: %s Delay: %s')" % \
               (self.__class__.__name__,
                _call_string(self.target, self.args, self.kwargs),
                self.delay)


class RunMultipleException(Exception):
    """Indicates one or more threads of run_multiple raised an exception.

    Attributes:
        results: A list of the individual result of each target execution.
            The value of each item in the list is either the value returned
            from target() or the exception raised by target().
            At least one of the values in the results list will be some type of
            exception (i.e. a subclass of Exception).
    """
    def __init__(self, results):
        """Initialize with results.

        Args:
            results: A list containing the result from target of each thread..

        Returns:
            An instance of a RunMultipleException
        """
        Exception.__init__(self)
        self.results = results

    def __str__(self):
        """The string representation of the object.
        """
        return self.__repr__()

    def __repr__(self):
        """The string representation of the object.

        Includes the string representation of the results list.
        """
        return "%s('%s')" % (self.__class__.__name__, repr(self.results))


def _invoke_target(*args, **kwargs):
    """Invoke target() callable with *args and **kwargs and queue the result.

    This function is used as the target of each thread which is spawned by
    run_multiple. It waits for delay seconds and then invokes
    target(*args, **kwargs) inside a try/except block. The index and
    result are queued onto result_q. If target() raises an exception, the
    exception is treated as the result and queued onto result_q.

    Args:
        *args: A list of positional arguments. The first four values are
            mandatory and are treated as arguments to invoke_target():
                target: The callable object to invoke.
                index: An index used to identify results in result_q.
                result_q: A queue on which to place (index, result) tuple.
                delay: Seconds to wait before invoking target().
            The remaining values in args, if any, are treated as positional
            arguments to target().
        **kwargs: Keyword arguments to target().
    """
    # Convert tuple to list so we can use pop()
    args = list(args)
    # Pulling these arguments from unnamed *args avoids a conflict with
    # the argument names accepted by target()
    target = args.pop(0)
    index = args.pop(0)
    result_q = args.pop(0)
    delay = args.pop(0)
    # Wait for the delay before invoking target().
    time.sleep(delay)
    # Initialize result to None
    result = None
    # Wrap the invocation of target() in a try/except block
    # in order to return any exception which is raised.
    try:
        # Invoke target() with arguments.
        result = target(*args, **kwargs)
    except Exception as ex:
        # Put the exception in result.
        result = ex
    # Put a tuple of (index, result) on the queue.
    result_q.put((index, result))


def _check_threads_running(threads, targets):
    """Check to make sure the target of each thread is running.

    Log a message about whether or not the target of each thread has
    started. Technically, we're seeing if the thread is running 0.1 seconds
    after it was started, so if a thread exits in less than .1 seconds,
    then it is logged as possibly having failed to start even though it may
    have just started and exited quickly.

    Args:
        threads: A list of threads to check.
        targets: A list of target information for each thread.

    Returns:
        A list of booleans. True if a thread is running. False if it is not.
    """
    time.sleep(0.1)
    #  A list of whether or not each thread is running.
    thread_running = [True] * len(targets)
    for index, item in enumerate(targets):
        target = item['target']
        args = item.get('args', [])
        kwargs = item.get('kwargs', {})
        delay = item.get('delay', 0)
        parent_thread = item.get('parent_thread', False)
        if threads[index].is_alive():
            t.log(level='INFO',
                  message="Successfully invoked %s with delay of %s seconds" %
                  (_call_string(target, args, kwargs), delay))
            #  Added code to add parent threads for background logging.
            if parent_thread:
                tname = threads[index].name
                t.log(level='INFO', message="Adding parent thread %s " % tname)
                if tname not in t.background_logger.LOGGING_THREADS:
                    logging_threads = list(t.background_logger.LOGGING_THREADS)
                    logging_threads.append(tname)
                    t.background_logger.LOGGING_THREADS = tuple(logging_threads)
        else:
            t.log(level='WARN',
                  message="Possibly failed to invoke or execution "
                          "completed before the check for %s with delay of %s "
                          "seconds" %
                  (_call_string(target, args, kwargs), delay))
            thread_running[index] = False
    return thread_running


def _start_threads(targets, result_q):
    """Start a thread to run each target in targets.

    Args:
        targets: A list of thread targets. See run_multiple() for details.
        result_q: The queue on which each thread should place the result
            returned by target (or the exception raised.)

    Returns:
        A list of the threads which were started.
    """
    threads = []
    for index, item in enumerate(targets):
        # target, or fname for compatibility, is mandatory.
        target = item.get('target')
        if target is None:
            target = item.get('fname')
            if target is None:
                raise KeyError('target not specified.')
            else:
                # Replace 'fname' with 'target' so we don't have to do this
                # dance again.
                item['target'] = target
                del item['fname']
        args = item.get('args', [])
        kwargs = item.get('kwargs', {})
        delay = item.get('delay', 0.01)
        threads.append(Thread(target=_invoke_target,
                              args=[target, index, result_q, delay] + args,
                              kwargs=kwargs))
        # A hung thread shouldn't keep the main thread from exiting.
        threads[index].daemon = True
        try:
            threads[index].start()
        except Exception as e:
            raise TobyException("Failed to start the threads: %s" % e)
    return threads


def _wait_for_threads(threads, timeout):
    """Wait for each thread in the threads list to exit or timeout

    Args:
        threads: A list of threads on which to wait.
        timeout: Float of the number of seconds to wait before timing out.
    """
    # The wall time when we should timeout.
    if timeout is not None:
        end_time = (datetime.datetime.now() +
                    datetime.timedelta(seconds=timeout))

    # Wait for all threads to exit or timeout.
    # Because we have to do a join() on one thread at a time, the amount
    # of time to wait is the difference between the time that all threads
    # should timeout (end_time) and now.
    for index, _ in enumerate(threads):
        if timeout is None:
            wait_time = None
        else:
            wait_time = (end_time - datetime.datetime.now()).total_seconds()
            # Make sure we don't send a negative wait_time
            wait_time = 0 if wait_time < 0 else wait_time
        threads[index].join(wait_time)


def run_multiple(targets=None, list_of_dicts=None, timeout=None, internal_call=True):
    """Runs multiple callable objects in parallel.

    Spawns a thread for each target item in the targets list. Each target
    item is a dict which defines a callable object and it's arguments. Each
    thread will invoke a target item from the list via the _invoke_target()
    function.

    WARNING: It is the caller's responsibility to ensure that none of the
             callable objects modify shared state in a thread-unsafe way.
             Because threads are used each callable object has full access to
             global variables. Modifying global variables without a thread-safe
             locking mechanism will produce unexpected results.

             The most common usage of this function is to invoke methods on a
             device handle. As long as each item in targets uses a unique
             device handle, this is generally safe.

    WARNING: Python does not provide a mechanism for killing a thread. Threads
             started by run_multiple() are only stopped when the main thread
             exits. If a thread raises a RunMultipleTimeoutException it means
             that thread is STILL RUNNING at the time run_multiple() returns.
             The thread will continue to run until it either exits on its
             own, or until the main thread exits.

    Args:
        targets: A mandatory list of target items. ('list_of_dicts' may be
            used as an alias for backwards compatibility.) Each target item is
            a dictionary with the following keys :
            'target': A callable object (i.e. a function name or method without
                the parenthesis.)(mandatory. 'fname' may be used as an alias
                for backwards compatibility.)
            'delay': A float of number of seconds to wait before invoking
                target(*args, **kwargs). (optional) (default: 0)
            'args': A list of positional arguments passed to target() as
                target(*args, **kwargs). (optional) (default: [])
            'kwargs': A dict of keyword arguments and values passed to target()
                as target(*args, **kwargs). (optional) (default: {})
        timeout: A float of number of seconds to wait for all threads to
                complete execution. (optional)
                (default: None - Interpreted as an infinite timeout.)

    Returns: A list comprised of the value returned by the target object of
             each thread. The sequence of values in the list is the same as
             the sequence of target objects in targets. If the target
             object does not return a value, then the list contains a None
             value for that index in the list.

    Raises:
        If any thread raises an exception, then a RunMultipleException is
        raised. A RunMultipleException has a results attribute which is a list
        of the return value for each thread's target. If the target raised
        an exception, then the return value is the exception which was raised.
        If the timeout is exceeded and the thread is still running, then the
        return value for that thread will be a RunMultipleTimeoutException.
        If the thread is not running after 0.1 seconds, and has not returned a
        value, then the return value for that thread will be a
        RunMultipleFailedStartException. The string representation of
        a RunMultipleException is the string representation of the results
        attribute.

    Examples:
    from jnpr.toby.hldcl.device import Device
    from jnpr.toby.utils.utils import run_multiple
    from jnpr.toby.init.init import init

    init_obj = init()
    init_obj.Initialize(init_file='<your yaml>.yaml')

    #One can create device handle list by iterating through 't' variable
    handle0 = init_obj.get_handle(resource='device0')
    handle1 = init_obj.get_handle(resource='device1')
    handles = [handle0, handle1]

    list_of_dicts = []

    for dev in handles:
        list_of_dicts.append({'fname': dev.reboot,
	'kwargs': {'wait':<waittimeout>, 'timeout':<timeout>, 'all':True}})

    run_multiple(list_of_dicts)

    Few other example of run_multiple in Toby code,
    Refer: https://git.juniper.net/Juniper/toby/blob/b49a2d427578e3b056abd2f4d3e332469f11f65a/lib/jnpr/toby/init/init.py file.
    """
    # targets, or the list_of_dicts alias, is mandatory
    if targets is None:
        targets = list_of_dicts
    if targets is None:
        raise TypeError("Mandatory argument 'targets' is missing")
    # The shared queue for sending/receiving results between threads.
    result_q = Queue()
    # The result list. Pre-populate with None since that's the value we set if
    # the callable object doesn't return anything.
    results = [None] * len(targets)

    # Create the background logger
    if internal_call:
        t.set_background_logger()

    # Start the threads
    threads = _start_threads(targets, result_q)

    # Make sure all threads started.
    threads_running = _check_threads_running(threads, targets)

    # Wait for all threads to exit or timeout.
    _wait_for_threads(threads, timeout)

    # Gather the results.
    while not result_q.empty():
        (index, result) = result_q.get()
        results[index] = result

    # Any timeout exceptions?
    for index, item in enumerate(targets):
        if results[index] is None and threads[index].is_alive():
            target = item['target']
            args = item.get('args', [])
            kwargs = item.get('kwargs', {})
            delay = item.get('delay', 0)
            results[index] = RunMultipleTimeoutException(target=target,
                                                         delay=delay,
                                                         args=args,
                                                         kwargs=kwargs,
                                                         timeout=timeout)

    # Any failed to start exceptions?
    # Commented out for now as it is causing false failures
    # for index, item in enumerate(targets):
    #     if results[index] is None and threads_running[index] is False:
    #         target = item['target']
    #         args = item.get('args', [])
    #         kwargs = item.get('kwargs', {})
    #         delay = item.get('delay', 0)
    #         results[index] = RunMultipleFailedStartException(target=target,
    #                                                         delay=delay,
    #                                                         args=args,
    #                                                         kwargs=kwargs)

    # Any exceptions in the results?
    for index, result in enumerate(results):
        if isinstance(result, Exception):
            if internal_call:
                t.process_background_logger() # need to see logs even on fail
            raise RunMultipleException(results)

    # Process background logger
    if t.background_logger is not None and internal_call:
        # Added code to clean up extra thread added for background logging.
        logging_threads = list(t.background_logger.LOGGING_THREADS)
        if len(logging_threads) > 2:
            pr_thread = logging_threads.pop()
            t.process_background_logger(pr_thread)
            t.background_logger.LOGGING_THREADS = tuple(logging_threads)
        else:
            t.process_background_logger()

    return results


def get_testcase_name():
    """
        Get the testcase name
    """
    from robot.libraries.BuiltIn import BuiltIn
    t._test_stage = BuiltIn().get_variable_value('${TEST_NAME}')


def check_version(device=None, version=None, operator='ge', all=False):
    """
       Utility to check Minimum Junos Version required to run a Testcase.

       :device:
       *MANDATORY* device handle for the currently executing device
       :version:
       *MANDATORY* Minimum JUNOS version required
       :operator:
       *OPTIONAL* Condition for version comparision. Currently supporting
       1. greater than or equal(ge)
       2. equal(eq)
       :all:
       *OPTIONAL* Valid only if the device is of Junos.
 	 When set to True, all JUNOS REs will be checked for Version match.
    """
    input_condition = ['ge', 'eq']
    result = False
    if all:
        if operator in input_condition:
            for node in device.nodes.keys():
                for controller_name in device.nodes[node].controllers.keys():
                    device_version = re.match(r"^\d+\.\d+.*", \
			 device.nodes[node].controllers[controller_name].get_version(refresh=True))
                    if operator == 'ge':
                        result = device_version.group() >= version
                        if not result:
                            device.log(level="WARN", \
			       message="Version check failed on: %s" % controller_name)
                            break
                        else:
                            device.log(level="INFO", \
			      message="Version check passed on: %s" % controller_name)
                    else:
                        result = device_version.group() == version
                        if not result:
                            break
            return result
        else:
            raise TobyException("Invalid Condition provided. Supported values" \
	     + str(input_condition))
    else:
        device_version = re.match(r"^\d+\.\d+.*", device.get_version(refresh=True))
        if operator in input_condition:
            if operator == 'ge':
                if device_version.group() >= version:
                    result = True
            else:
                if device_version.group() == version:
                    result = True
            return result
        else:
            raise TobyException("Invalid Condition provided. Supported values" +str(input_condition))


def check_device_connection(host):
    """
    See if ports are listening on target device
    """
    if host and hasattr(host, 'channels'):
        results = 'Checking Connection Channels...\n'
        ret_val = True
        for channel in host.channels:
            try:
                if channel == 'pyez':
                    if host.channels[channel].probe():
                        results += '    Channel [' + channel + '] Connected\n'
                        ret_val = True
                    else:
                        results += '    Channel [' + channel + '] Not Connected\n'
                        return False
                else:
                    if host.channels[channel].is_active():
                        results += '    Channel [' + channel + '] Connected\n'
                        ret_val = True
                    else:
                        results += '    Channel [' + channel + '] Not Connected\n'
                        host.log(results)
                        return False
            except Exception:
                pass
        host.log(results)
        return ret_val


def _check_device_port(host, port, channel):
    import socket
    ret_val = True
    try:
        s_handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_timeout = 5
        s_handle.settimeout(socket_timeout)
        s_handle.connect((host, int(port)))
        s_handle.close()
        results = '    [' + channel + '] Port ' + str(port) + ' UP and Listening\n'
    except socket.error:
        results = '    [' + channel + '] Port ' + str(port) + ' Down \n'
        ret_val = False
    return (ret_val, results)


def check_device_port(device, **device_args):
    ''' DOCUMENTATION TO DO '''
    results = 'Port scanning target device...\n'
    if device is None:
        (ret_val, msg) = _check_device_port(device_args['host'], device_args['port'], \
	 device_args['channel'])
        results += msg
    elif device and hasattr(device, 'channels'):
        ret_val = True
        for channel in device.channels:
            if device.channels[channel].port:
                (ret_val, msg) = _check_device_port(device.host, device.channels[channel].port, channel)
                results += msg
                if not ret_val:
                    device.log(results)
                    return ret_val
    t.log(results)
    return ret_val


def _check_device_reachability(host):
    from jnpr.toby.utils.iputils import ping
    if host:
        if ping(host=host, count=2, interval=2, timeout=10):
            results = '    Device is responding to pings\n'
            return (True, results)
        else:
            results = '    Device is not responding to pings\n'
            return (False, results)


def check_device_reachability(device, **device_args):
    ''' documentation to do '''
    results = "Checking device is pingable...\n"
    if device is None:
        if 'host' in device_args:
            (ret_val, msg) = _check_device_reachability(device_args['host'])
    else:
        (ret_val, msg) = _check_device_reachability(device.host)
    results += msg
    t.log(results)
    return ret_val


def check_device_scan(device, channels_check=True, port_check=True, ping_check=True, **device_args):
    ''' Documentation '''
    device_health = dict()
    device_health['connection_lost'] = False
    device_health['ports_unreachable'] = False
    device_health['device_unreachable'] = False
    if channels_check:
        if not check_device_connection(device):
            device_health['connection_lost'] = True
    if port_check:
        if not check_device_port(device, **device_args):
            device_health['ports_unreachable'] = True
    if ping_check:
        if not check_device_reachability(device, **device_args):
            device_health['device_unreachable'] = True
    return device_health


def prepare_log_message(cmd, mode, pattern_exp, pattern_recv, timeout):
    ''' documentation '''
    message = '\n'
    cmd_message = "Sent {} command:".format(mode.lower())
    message += "{:<40}".format(cmd_message)
    message += "{}\n".format(cmd)

    prompt_message = "Expected {} prompt:".format(mode.lower())
    message += "{:<40}".format(prompt_message)
    message += "'{}'\n".format(pattern_exp)

    message += "{:<40}'{}'\n".format("Received response ending with:", pattern_recv)
    message += "{:<40}{}\n".format("Timeout:", timeout)
    return message


def add_to_toby_exec(under_key, data_dict, add_under_key=True):
    """
    This method will update the toby_exec.yaml with the data given to it
    :param under_key: Specify the key under which the data_dict has to be appended in toby_exec.yaml
    :param data_dict: Data dictionary that will be added under specified key ( under_key)
    :param add_under_key: Add under_key to the toby_exec.yaml if add_under_key is set to True
    :return: None
    """
    try:
        output_file = str(get_script_log_dir()) + "/toby_exec.yaml"
        if os.path.exists(output_file):
            loaded_yaml = yaml.YAML().load(open(output_file))
            if add_under_key:
                if under_key not in loaded_yaml.keys():
                    loaded_yaml.update({under_key: dict()})
            loaded_yaml[under_key].update(data_dict)
            with open(output_file, 'w') as toby_exec_file:
                yaml.YAML().dump(loaded_yaml, toby_exec_file)
        else:
            return False
    except IOError as exp:
        pass

def log_file_version(file_name):
    """
    method to fetch blob version from file
    The blob version will be encoded into each file using syntax "$Id : <blob-id> $"
    following method will fetch this blob id and logs it in log file when suite execution starts
    """
    file_version = _fetch_version(file_name) or "None"
    #In case of multi-threading, locking threads when they access the method together to avoid conflicts
    lock.acquire()
    add_to_toby_exec(under_key="dependent_files", data_dict={file_name : file_version})
    lock.release()


def _fetch_version(file_name):
    """
    fetch_version is private metnod to fetch verion info from file
    """
    cmd = 'grep -oE "\\\$\s*Id\s*:\s*([a-f0-9A-F]+)\s*" ' + file_name + ' | cut -d " " -f2 '
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate()
        proc.wait()
        out = out.decode("utf-8")
        if out != "":
            out = out.rstrip('\n')
        return out
    except Exception as exp:
        pass
