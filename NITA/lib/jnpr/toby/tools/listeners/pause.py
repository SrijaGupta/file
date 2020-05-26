'''
      Pause listener
'''
import os
import ruamel.yaml as yaml
from sys import stdout as console
from robot.libraries.BuiltIn import BuiltIn
import signal

ROBOT_LISTENER_API_VERSION = 2

def resume_execution(signal_number, frame):
    '''
    resume_execution
    '''
    print("\nResuming execution...\n")
    t.log("Resuming execution...\n")
    del signal_number   #unused hence deleting to improve pylint score
    del frame           #unused hence deleting to improve pylint score

def pause_execution():
    '''
    pause_execution
    '''
    console.write('\nToby process [ %s ] sending signal to group PID [ %s ] ' % (str(os.getpid()), os.getpgid(os.getpid())))
    t.log('Toby process [ %s ] sending signal to parent process [ %s ]\n' % (str(os.getpid()), os.getpgid(os.getpid())))
    os.kill(os.getpgid(os.getpid()), signal.SIGCONT)
    signal.signal(signal.SIGINT, resume_execution)
    print("\nPress Ctrl+C to resume...")
    signal.pause()
#########################################################
#
#  Pause Listener
#
#########################################################

class pause(object):
    '''
      Pause listener
       This listener is attached when --pause option is enabled from toby wrapper script with required YAML input file.
       Based on input YAML file, it will Pause the excecution and wait for SIGCONT to resume execution.
    '''
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.pause_file_content = None
        console.write('Running with Pause listener attached...\n')

    def load_pause_yaml(self):
        '''
        load_pause_yaml
        '''
        if self.pause_file_content is None:
            val = BuiltIn().get_variable_value('${pause_file}')
            if val:
                try:
                    self.pause_file_content = yaml.safe_load(open(val))
                except Exception as error:
                    raise error

    def check_for_pause(self, where, when, name):
        '''
        check_for_pause
        '''
        try:
            input_list = self.pause_file_content[where][when]
            input_list = [element.lower() for element in input_list]
            if name.lower() in input_list or 'any' in input_list:
                return True
        except Exception:
            pass
        return False

    def end_keyword(self, name, attrs):
        """
            This listener method is called when keyword ends

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing type, kwname, librname,
                 starttime, endtime, elapsedtime and status.
            :return:
                None
        """
        self.load_pause_yaml()
        if self.check_for_pause('keywords', 'after', name) or (attrs['status'] == "FAIL" and self.check_for_pause('keywords', 'fail', name)):
            print("\nPaused after Keyword: " + name)
            t.log("Paused after Keyword: " + name)
            pause_execution()

    def start_keyword(self, name, attrs):
        """
            This listener method is called when keyword starts

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing type, kwname, librname,
                 starttime, endtime, elapsedtime and status.
            :return:
                None
        """
        self.load_pause_yaml()
        if self.check_for_pause('keywords', 'before', name):
            print("\nPaused before Keyword: " + name)
            t.log("Paused before Keyword: " + name)
            pause_execution()
            del attrs    #unused hence deleting to improve pylint score

    def start_test(self, name, attrs):
        """
            This listener method is called when test starts

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing id, longname, starttime,
            :return:
                None
        """
        self.load_pause_yaml()
        if self.check_for_pause('testcases', 'before', name):
            print("\nPaused before Test-case: " + name)
            t.log("Paused before Test-case: " + name)
            pause_execution()
            del attrs    #unused hence deleting to improve pylint score

    def end_test(self, name, attrs):
        """
            This listener method is called when test ends

            :param name:
                **REQUIRED** The shortname of test suite
            :param attrs:
                **REQUIRED** The attribute dictionary containing id, longname, starttime,
            :return:
                None
        """
        self.load_pause_yaml()
        if self.check_for_pause('testcases', 'after', name) or (attrs['status'] == "FAIL" and self.check_for_pause('testcases', 'fail', name)):
            print("\nPaused after Test-case: " + name)
            t.log("Paused after Test-case: " + name)
            pause_execution()
