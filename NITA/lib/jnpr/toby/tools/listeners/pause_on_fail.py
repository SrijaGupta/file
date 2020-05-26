
'''
    Robot Keywords Debugger - Pause on Fialure listener
    This listener is attached when --pause_on_failure option is enabled from toby wrapper script
    It checks for Env var pause_on_failure, if set to True, then it checks for status of each
    Keywords at the end of execution, if any Keyword resutls in Failure, the tests are halted and
    control is returned to Shell command handler, where it provides cli options such as
     'p - print robot variable value, c - continue to next testcase, q - quit the debugger without cleanup.
'''
import sys
from sys import stdout as console
from robot.libraries.BuiltIn import BuiltIn

ROBOT_LISTENER_API_VERSION = 2



# Import necessary packages for mailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import getpass
import socket

class Command:
    '''
        Interface
    '''
    def execute(self, cmd):
        '''
            execute command
        '''
        raise NotImplementedError()

    def cancel(self):
        '''
            To be implemented
        '''
        raise NotImplementedError()

    def name(self):
        '''
            To be implemented
        '''
        raise NotImplementedError()

class SessionClosed(Exception):
    '''
        Handling 'exit' command
    '''
    def __init__(self, value):
        self.value = value

class ContinueCommand(Command):
    '''
        Continue command
    '''
    def execute(self, cmd):
        '''
            TODO: execute method
        '''
        pass

    def cancel(self):
        '''
            TODO: cancel method
        '''
        pass

    def name(self):
        '''
            name method
        '''
        return "c"

class PrintCommand(Command):
    '''
        print command class
    '''
    def execute(self, cmd):
        '''
            execute method
        '''
        try:
            val = BuiltIn().get_variable_value(cmd)
            console.write(val)
        except Exception as exptn:
            console.write(str(sys.exc_info()[1]))
            console.write(str(exptn))

    def cancel(self):
        console.write("You have canceled \"print\" command\n")

    def name(self):
        return "p"

class HelpCommand(Command):
    '''
        Help command class
    '''
    def execute(self, cmd):
        '''
            execute helper command method
        '''
        console.write("Robot keywords Debugger 0.1 (rdb)\n")
        console.write("\tc - continue to next testcase (pauses if failure occurs again!)\n")
        console.write("\tp <var-name> - Print the variable value; for example 'p ${valn_id_1}'\n")
        console.write("\tq - quit the debugger witout cleaning up\n")

    def cancel(self):
        pass

    def name(self):
        pass

class QuitCommand(Command):
    '''
        Quit command class
    '''
    def execute(self, cmd):
        '''
            ececute command method
        '''
        raise SessionClosed("Good bye!")

    def cancel(self):
        pass

    def name(self):
        return False

# available commands
COMMANDS = {'c': ContinueCommand(), 'p': PrintCommand(), 'q': QuitCommand(),
            'h': HelpCommand(), "help": HelpCommand(), '?': HelpCommand()}

# Debug Shell
def shell():
    '''
        Debug shell handler
    '''
    try:
        while True:
            console.flush()
            #console.write("Entering Robot debug shell...\n")
            console.write("\nrdb>> ")
            cmd = input()
            try:
                arg1 = None
                #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
                cmd_args = cmd.split()
                if len(cmd_args) == 2:  # <cmd> <arg1>
                    cmd = cmd_args[0]
                    arg1 = cmd_args[1]

                    command = COMMANDS[cmd]
                    command.execute(arg1)
                else:
                    command = COMMANDS[cmd]
                    command.execute(cmd_args[0])
                if command.name() == "c":
                    return True

            except KeyError:
                console.write("ERROR: Command \"%s\" not found\n" % cmd)
                return False
    except SessionClosed:
        return False

#########################################################
#
#  PauseOnFail Listener
#
#########################################################

class pause_on_fail(object):
    '''
      Pause on Failure listener
       This listener is attached when --pause_on_failure option is enabled from toby wrapper script
       It checks for Env var pause_on_failure, if set to True, then it checks for status of each
       Keywords at the end of execution, if any Keyword resutls in Failure, the tests are halted and
       control is returned to Shell command handler, where it provides cli options such as
        'p - print robot variable value, c - Continue to next testcase, pauses again for any failures, q - quit the debugger without cleanup

    '''
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self._ctx = None
        self._testname = None
        self._script_name = None
        self._continue = False
        self._attributes = None
        from robot.running.context import EXECUTION_CONTEXTS
        self._ctx = EXECUTION_CONTEXTS.current if not False else EXECUTION_CONTEXTS.top
        console.write('Robot keywords Debugger 0.1 (rdb)\n')

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
        self._testname = name
        if BuiltIn().get_variable_value('${SUITE_SOURCE}'):
            self._script_name = BuiltIn().get_variable_value('${SUITE_SOURCE}')
        else:
            self._script_name = '(script not found)'
        if attrs['status'] == "FAIL":
            print("\nKeyword '"+attrs['kwname'] + "' invocation failed, Execution Paused!")
            if self._testname is not None:
                print("\tTestcase: "+self._testname)
            if 'libname' in attrs and attrs['libname'] is not None:
                print("\tlibname: "+attrs['libname'])
            if 'args' in attrs:
                print("\targs: "+str(attrs['args']))
            # Send mail to user if the option has been enabled
            if BuiltIn().get_variable_value('${mail}'):
                if BuiltIn().get_variable_value('${mail}') == 'enable':
                    # have local host send email
                    smtp_server = smtplib.SMTP(host='127.0.0.1', port= 25)
                    # create properly formatted email notifying of failure to user
                    multi_part_message = MIMEMultipart()
                    body_of_message = ("Script '" + self._script_name + "' failed on keyword '" + attrs['kwname'] +
                                       "' during testcase '" + self._testname + "'.")
                    # gets current username
                    user_email = '<{}@juniper.net>'.format(getpass.getuser())
                    recipients = [user_email]
                    hostname = socket.gethostname()
                    # sends mail from current server
                    multi_part_message['From']=email.utils.formataddr(('TOBY', 'toby@{}'.format(hostname)))
                    multi_part_message['To']= ", ".join(recipients)
                    multi_part_message['Subject']="TOBY failure has occured during " + self._script_name + " script run!"
                    multi_part_message.attach(MIMEText(body_of_message, 'plain'))
                    # attempst to mail user about script's failure(s)
                    try:
                        smtp_server.send_message(multi_part_message)
                        print("An email has been sent notifying of failure to {}".format(user_email))
                    except Exception as error:
                        print("Sending email to {} failed!".format(user_email))
                        print(error)
                    smtp_server.quit()
            ret = shell()
            if not ret:
                exit(0)
            else:
                self._continue = True
        if self._continue:
            return True
        return False

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
        self._testname = name
        self._attributes = attrs
