'''
    TobyException
'''
# pylint: disable=undefined-variable,broad-except,super-init-not-called
import traceback
import re
from subprocess import Popen, PIPE, STDOUT

class TobyException(Exception):
    """
    Toby Exception
    """
    def __init__(self, message, host_obj=None):

        try:
            if host_obj:
                exception_message = ''
                if host_obj.name:
                    exception_message = '[' + host_obj.name + '] ' + str(message)
                elif host_obj.host:
                    exception_message = '[' + host_obj.host + '] ' + str(message)
            raise Exception(exception_message)
        except Exception:
            trace = traceback.format_stack()
            trace.pop()
            indent = ''
            trace_str = 'TobyException occuring. Traceback:\n'
            for caller in trace:
                if 'robot' not in caller:
                    caller = indent + re.sub(r"\n\s+", "\n" + indent + '  ', caller)
                    trace_str = trace_str + caller
                    indent = indent + '  '

            t.log(level='INFO', message=trace_str)
            try:
                from robot.libraries.BuiltIn import BuiltIn
                if BuiltIn().get_variable_value('${macro_lib}'):
                    print("*HTML* Macro Engine employed.  <a href=macro_logs target=_blank>Macro Engine Logs</a>")
            except Exception:
                pass

class TobyConnectLost(TobyException):
    """
    Exception to handle Connection Lost to Device
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: CONNECT_LOST]")
            raise TobyException(message, host_obj)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")

class TobyConnectFail(TobyException):
    """
    Exception to handle Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: CONNECT_FAIL]")
            raise TobyException(message, host_obj)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")

class TobyLinkFail(TobyException):
    """
    Exception to handle link Failure.
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: LINK_FAIL]")
            raise TobyException(message, host_obj=self)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")

class SpirentLicenseError(TobyException):
    """
    Exception to handle Spirent License Error
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: SPIRENT_LICENSE_ERROR]")
            raise TobyException(message, host_obj=self)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")
            spirent_fv_debug_usage()

class SpirentConnectError(TobyException):
    """
    Exception to handle Spirent Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: SPIRENT_CONNECT_ERROR]")
            raise TobyException(message, host_obj=self)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")
            spirent_fv_debug_usage()

class TobySpirentException(TobyException):
    """
    Exception to handle Spirent invoke Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: SPIRENT_INVOKE_ERROR]")
            raise TobyException(message, host_obj=self)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")
            spirent_fv_debug_usage()

class TobySpirentLabserverConnectException(TobyException):
    """
    Exception to handle Spirent Labserver Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: SPIRENT_LABSERVER_CONNECT_ERROR]")
            raise TobyException(message, host_obj=self)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")
            spirent_fv_debug_usage()

class TobySpirentChassisConnectException(TobyException):
    """
    Exception to handle Spirent Chassis Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: SPIRENT_CHASSIS_CONNECT_ERROR]")
            raise TobyException(message, host_obj=self)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")
            spirent_fv_debug_usage()

class IxiaConnectError(TobyException):
    """
    Exception to handle Ixia Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: IXIA_CONNECT_ERROR]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")


class TobyIxiaException(TobyException):
    """
    Exception to handle Ixia Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: IXIA_ERROR]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")


class TobyIxiaAppserverConnectException(TobyException):
    """
    Exception to handle Ixia Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: TobyIxiaAppserverConnectException]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")


class TobyIxiaChassisConnectException(TobyException):
    """
    Exception to handle Ixia Connection Failure
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='ERROR', message="[ERROR_CODE: TobyIxiaChassisConnectException]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='ERROR', message=str(message) + "\nException raised")

class TobyConnectionClosedException(TobyException):
    """
    Exception to handle if device is reachable, but the channel connection lost
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='INFO', message="[ERROR_CODE: CONNECTION_CLOSED]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='INFO', message=str(message) + " Exception raised")

class TobyDevicePortUnreachableException(TobyException):
    """
    Exception to handle if channel connection lost and device is unreachable
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='INFO', message="[ERROR_CODE: DEVICE_PORT_UNREACHABLE]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='INFO', message=str(message) + " Exception raised")

class TobyPromptTimeoutException(TobyException):
    """
    Exception to handle if device prompt did not return within <timeout> seconds
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='INFO', message="[ERROR_CODE: COMMAND_TIMEOUT]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='INFO', message=str(message) + " Exception raised")

class TobyDeviceUnreachableException(TobyException):
    """
    Exception to handle if device prompt did not return within <timeout> seconds
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='INFO', message="[ERROR_CODE: DEVICE_UNREACHABLE]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='INFO', message=str(message) + " Exception raised")

class DeviceModeSwitchException(TobyException):
    """
    Exception to handle if device prompt did not return within <timeout> seconds
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='INFO', message="[ERROR_CODE: DEVICE_MODE_SWITCH_TIMEOUT]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='INFO', message=str(message) + " Exception raised")

class TobyCustomPatternTimeoutException(TobyException):
    """
    Exception to handle if device prompt did not return within <timeout> seconds
    """
    def __init__(self, message, host_obj=None):
        try:
            t.log(level='INFO', message="[ERROR_CODE: CUSTOM_PATTERN_NOT_FOUND]")
            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='INFO', message=str(message) + " Exception raised")

class TobyFileIOException(TobyException):
    """
    Exception to handle if can't write to logdir
    """
    def __init__(self, message, host_obj=None):
        try:
            from jnpr.toby.logger.logger import get_log_dir
            log_dir = get_log_dir()

            # First test if file can be written to log directory
            p  = Popen(["touch", log_dir + "/test_file.txt"], stdout=PIPE)
            p.wait()

            # Failure to write file
            if p.returncode > 0:
                t.log(level='WARN',  message="Couldn't write to log directory: "+log_dir)
            else:
                p  = Popen(["rm", log_dir + "/test_file.txt"], stdout=PIPE)
                p.wait()

            # Second we test if the log dir is mounted
            p  = Popen(["findmnt", "-T", log_dir], stdout=PIPE)
            p.wait()

            # Prints the output from 'findmnt' command
            t.log(level='INFO', message="Mountpoint...\n"+str(p.communicate()[0].decode()))

            raise TobyException(message, host_obj=host_obj)
        except Exception:
            t.log(level='INFO', message=str(message) + " Exception raised")


def raise_toby_exception(device_health, message=None, host_obj=None, connect_fail=False):
    """
       Added API to raise corresponding excepiton based on type of error.
     """
    if message is None:
        message = ''
    if len(device_health.keys()) > 0:
        if device_health['device_unreachable']:
            raise TobyDeviceUnreachableException(message, host_obj=host_obj)
        elif device_health['ports_unreachable']:
            message = "Connection closed and target device not listening on designated " \
                      "text channel (port 22)"
            raise TobyDevicePortUnreachableException(message, host_obj=host_obj)
        elif device_health['connection_lost']:
            message = "Text / PyEZ channel to device is no longer available"
            raise TobyConnectionClosedException(message, host_obj=host_obj)
        else:
            if connect_fail:
                raise TobyConnectFail(message, host_obj=host_obj)
            elif device_health.get('user_pattern_not_found', False):
                raise TobyCustomPatternTimeoutException(message, host_obj=host_obj)
            else:
                raise TobyPromptTimeoutException(message, host_obj=host_obj)
    else:
        raise TobyPromptTimeoutException(message, host_obj=host_obj)

def spirent_fv_debug_usage():
    """
      print fv-debug usage to users
    """
    t.log(level='ERROR', message='''Note : For more additional spirent related logs you can make use of below knob in your yaml
    fv-debug:
       allowed-values:
          - enable
    description:
        This knob is used for particular platforms, create addition debug logs
        Examples-
        rt0 {
          system {
            make "spirent";
            fv-debug "enable";
          }
        }''')
