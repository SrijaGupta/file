"""
IxVeriwave module providing connectivity to IxVeriwave chassis
"""
from telnetlib import Telnet
from jnpr.toby.hldcl.trafficgen.trafficgen import TrafficGen
import jnpr.toby.frameworkDefaults.credentials as credentials
from jnpr.toby.exception.toby_exception import TobyException

class IxVeriwave(TrafficGen):
    """
    IxVeriwave emulation class
    """
    def __init__(self, system_data=None):
        """
        IxVeriwave abstraction layer

        :param  system_data  *MANDATORY* Dictionary of IxVeriwave information
          Example:
          system_data =
              system:
                primary:
                  controllers:
                    re0:
                      domain: englab.juniper.net
                      hostname: branch-ixveriwave
                      isoaddr: 47.0005.80ff.f800.0000.0108.0001.0102.5523.0232.00
                      loop-ip: 10.255.230.232
                      loop-ipv6: abcd::10:255:230:232
                      mgt-intf-name: mgt.0
                      mgt-ip: 10.204.230.232
                      mgt-ipv6: abcd::10:204:230:232
                      osname: JunOS
                  make: ixia
                  model: ixveriwave ata100
                  name: branch-ixveriwave
                  osname: JunOS


        :return: IxVeriwave object
        """
        self.expect_timeout = 20 # Timeout for telnet expect
        self.telnet_handle = None # Telnet object on which commands will be invoked
        self.prompt = r"ready>\s?" # This is the main prompt in the IxVeriwave console
        if system_data:
            self.host_args = dict() # Used to hold host arguments like user, password, osname, etc.
            sys_pri = system_data['system']['primary']
            if 'name' in sys_pri:
                self.host_args['host'] = sys_pri['name']
            controller_key = list(sys_pri['controllers'].keys())[0]
            self.chassis = sys_pri['controllers'][controller_key]['mgt-ip']

            if 'osname' in sys_pri['controllers'][controller_key]:
                self.host_args['os'] = sys_pri['controllers'][controller_key]['osname']
            else:
                self.host_args['os'] = 'IxVeriwave'
            # Getting user/password for login
            self.host_args['user'], self.host_args['password'] = credentials.get_credentials(os=self.host_args['os'])
            # Checking to see if a username has been passed via fv knob
            if 'user' in sys_pri['controllers'][controller_key]:
                self.host_args['user'] = sys_pri['controllers'][controller_key]['user']
            self.prompt = "{} {}".format(self.host_args['user'], self.prompt).encode(encoding='ascii')
            super(IxVeriwave, self).__init__(**self.host_args)

    def connect(self):
        """
        Connect to IxVeriwave chassis
        """

        self.telnet_handle = Telnet(self.chassis)
        # First we need to login to the chassis by issuing the appropriate command for the expected prompts
        match_results = self.telnet_handle.expect([br"Hit Enter to proceed:\s"], timeout=self.expect_timeout)
        if match_results[0] == -1:
            raise TobyException("Expected 'Hit Enter to proceed: ' but instead got:\r\n'" + match_results[2].decode('ascii') + "'")
        # We need to hit enter to continue
        self.telnet_handle.write(b'\r\n')
        match_results = self.telnet_handle.expect([br"Enter username:\s"], timeout=self.expect_timeout)
        if match_results[0] == -1:
            raise TobyException("Expected 'Enter username: ' but instead got:\r\n'" + match_results[2].decode('ascii') + "'")
        # We need to enter username at this point
        user = self.host_args['user'] + '\r\n'
        user = user.encode(encoding='ascii')
        self.telnet_handle.write(user)
        match_results = self.telnet_handle.expect([self.prompt], timeout=self.expect_timeout)
        if match_results[0] == -1:
            raise TobyException("Expected 'ready>' but instead got:\r\n'" + match_results[2].decode('ascii') + "'")
        else:
            return "Successfully connected to IxVeriwave chassis!"

    def invoke(self, command, *args, **kwargs):
        """
        Function to issue commands on IxVeriwave chassis
        """

        # This converts all the parameters, along with their values to a string. Since we are issuing the command to 
        # via telnet we need it to be one big, long string
        arguments = ' '.join(['{}={}'.format(parameter, value) for parameter, value in kwargs.items()])
        full_command = "{} {}{}".format(command, arguments, '\r\n') # Combines the command + arguments
        full_command = full_command.encode(encoding='ascii')
        self.telnet_handle.write(full_command)
        exp_timeout = kwargs.get('timeout', self.expect_timeout)
        match_results = self.telnet_handle.expect([self.prompt], timeout=exp_timeout)
        if match_results[0] == -1:
            raise TobyException("Expected 'ready>' but instead got:\r\n'" + match_results[2].decode('ascii') + "'")
        result = match_results[2].decode('ascii')
        if 'cmdStatus=fail' in result:
            raise TobyException("Invocation of IxVeriwave API '" + command + "' resulted in the command failing with the result:\r\n" + str(result))
        if 'Invalid command' in result:
            raise TobyException("Invocation of IxVeriwave API '" + command + "' failed because '" + command + "' is an invalid command")
        if 'Usage:' in result:
            raise TobyException("Invocation of IxVeriwave API '" + command + "' resulted in failure because the command was used incorrectly. Look at the output for more information:\r\n" + str(result))
        self.log("INFO", message="Invocation of IxVeriwave API '" + command + "' completed with result:\r\n" + str(result))
        return result


