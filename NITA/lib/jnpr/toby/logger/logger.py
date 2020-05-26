"""
    Logger module for Toby
"""
import logging
import os
import sys
import pprint
from jnpr.toby.exception.toby_exception import TobyFileIOException
from jnpr.toby.utils.Vars import Vars
import __main__ as main

class Logger(logging.Logger):
    """
        Logger class for Toby
    """

    def __init__(self, name, console=False, level='INFO'):
        """
        Logger class for Toby
        Logger class creates log files for Toby.
        The log filename will be of format
            <logFileName>.<pid>.log.
        By default log files gets created under current working directory.
        User can override this by setting ENV var TOBY_LOG_FOLDER or
        pass it with -d option in robot to full path.
        The logs are of the format
        [<date-timestamp>] [<methodName>:<lineNum>:<fileName>] [<level>] : <log message>
        The following sample code section illustrate the usage of Logger class::
        -class Device(object):
        -    def __init__(self, dev_name="test"):
        -        self.logger = Logger(dev_name)  # Logger object creation for device dev_name
        -
        -        my_dev.log.info("Trying to connect to {0} using {1} ...".
        -                    format(self.host, kwargs['connect_mode']))
        -        my_dev.log.info(message='In connect')
        -
        Toby will create logger object by default and it can be used like below.
        t.log(level='INFO', message='In connect')
        # Sample log statement:
        [2016-07-22 15:02:13] [<module>():123:toby_logger.py] INFO: Log name...myDevice.0

            :param name:
                *MANDATORY* mandatory Logger name variable.
            :return:  Logger object to log data

        """

        self.robot_log_level = None
        try:
            from robot.libraries.BuiltIn import BuiltIn
            _builtin = BuiltIn()
            self.robot_log_level = _builtin.get_variable_value("${LOG_LEVEL}")
        except:
            pass

        if "TOBY_LOG_LEVEL" in os.environ:
            level = os.environ['TOBY_LOG_LEVEL']

        self._level = getattr(logging, level.upper(), logging.INFO)
        self.log = logging.getLogger(name)

        self._script_name = get_script_name()
        if name != self._script_name:
            name = '.'.join([self._script_name, name])
        try:
            self._log_dir = get_log_dir()

            if not os.path.exists(self._log_dir):
                os.makedirs(self._log_dir)
            self._log_filename = os.path.join(self._log_dir, '.'.join([name, 'log']))
            file_handler = logging.FileHandler(self._log_filename)
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(funcName)s():%(lineno)d:%(filename)s] %(message)s',\
                        '%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)

            super(Logger, self).__init__(name)
            super(Logger, self).addHandler(file_handler)
            super(Logger, self).setLevel(self._level)
            if console:
                # Add console handler to print logs to console
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                super(Logger, self).addHandler(console_handler)
        except Exception as error:
            message = "Cannot get log directory due to the following error: {}".format(error.__str__())
            raise TobyFileIOException(message=message)

    def log_dir(self):
        """
            Method to get log dir
        """
        return self._log_dir


    def _log(self, log_level_int, message, optional_parameters=None):

        if type(message) is dict or type(message) is list:
            message = "\n" + pprint.pformat(message, indent=4)
        else:
            message = str(message)

        if message == '': # if no message content, do nothing
            return
        message = message.rstrip('\r\n')
        try:
            if self.robot_log_level:
                if log_level_int >= self.level:
                    # int 10 is standard Python loglevelger level 'DEBUG'
                    # only print DEBUG lines if Robot user is NOT using default loglevel INFO
                    if log_level_int != 10 or self.robot_log_level != 'INFO':
                        super(Logger, self)._log(log_level_int, message, optional_parameters)
            else:
                if log_level_int >= self.level:
                    super(Logger, self)._log(log_level_int, message, optional_parameters)
        except Exception as error:
            message = "Cannot get log directory due to the following error: {}".format(error.__str__())
            raise TobyFileIOException(message=message)


def get_log_dir():
    #Determine log dir
    log_dir = None
    if "TOBY_LOG_FOLDER" in os.environ:
        log_dir = os.environ['TOBY_LOG_FOLDER']
    elif Vars().get_global_variable('${OUTPUT DIR}') \
            and Vars().get_global_variable('${OUTPUT DIR}') != os.getcwd():
        log_dir = Vars().get_global_variable('${OUTPUT DIR}')
    else:
        log_dir = os.path.join(os.getcwd()) + '/toby_logs'
    return log_dir


def get_script_name():
    """
        Method to get caller script name.
    """
    script_name = None
    if Vars().get_global_variable('${SUITE_SOURCE}'):
        suite_source = Vars().get_global_variable('${SUITE_SOURCE}')
        path_list = suite_source.split('/')
        script_no_path = path_list[-1]
        script_name = script_no_path.replace(".robot", "")
    else:
        if hasattr(main, '__file__'):
            path, script_name = os.path.split(main.__file__)
            script_name = str(os.path.splitext(script_name)[0])
        else:
            script_name = 'toby'
    if not script_name:
        raise Exception("Unable to derive proper log file name")
    return script_name
