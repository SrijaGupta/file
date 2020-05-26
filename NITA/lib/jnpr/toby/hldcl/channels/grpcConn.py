"""
    GRPC Conn Module
"""
import logging
import sys
import time
import os
import re
from subprocess import Popen, PIPE
import importlib
import ruamel.yaml as yaml # pylint: disable=import-error

import jnpr.toby.engines.config.config_utils as file_util # pylint: disable=import-error
import jnpr.toby.utils.grpc.yaml_to_grpcCallable as CAT # pylint: disable=import-error


class Grpc(object):
    """
        GRPC Conn Class
    """
    def __init__(self, **kwargs):
        """

        Create a Grpc object

        :param rhandle: Junos router object to which grpc connection needs to
         be established. Either one of 'rhandle' or 'host' can only be provided

        :param host: Name or IP address of a Junos device to which grpc
         connection needs to be established. Either one of 'rhandle' or 'host'
         can only be provided

        :param port: Port on Junos router on which grpc is started
                     *OPTIONAL* : defaults to 50051

        :param user: Username for login to the router
            *MANDATORY*: when param 'host' is passed instead of 'rhandle'
            *OPTIONAL* : when params 'rhandle' is passed, defaults to extract
                from credentials DB

        :param password: Password for login to the router
            *MANDATORY*: when param 'host' is passed instead of 'rhandle'
            *OPTIONAL* : when params 'rhandle' is passed, defaults to extract
                from credentials DB

        :param channel_id: Name of Grpc channel
            OPTIONAL*: computed as a unique string, when not passed

        :param timeout:
            Timeout by when grpc channel operations or API executions
            are expected to be completed
            *OPTIONAL*: Defaults to 300 seconds

        :param grpc_lib_path: Path where GRPC service libraries are located
            *OPTIONAL* : Defaults to /volume/regressions/grpc_lib/latest
            The path '/volume/regressions/grpc_lib' will have sub-directories
            pointing to libs from latest TOT, previous releases and hence
            the sub-directory 'latest' will be a soft link to the latest TOT.

        :return: Object of Grpc class

        """
        self.channel_id = kwargs.get(
            'channel_id', str(os.getpid()) + str(time.time()).split('.')[0])
        self.client_id = None
        self.port = int(kwargs.get('port', 50051))
        self.user = kwargs.get('user', None)
        self.password = kwargs.get('password', None)
        self.channel = None
        self.timeout = kwargs.get('timeout', 300)
        self.grpc_lib_path = kwargs.get(
            'grpc_lib_path', '/volume/regressions/grpc_lib/latest')

        sys.path.append(self.grpc_lib_path)

        # GRPC connection can bypass JSD authentication and directly
        # connect to RPD on default port-40051
        # (Essential for CRPD until JSD is supported)
        self.bypass_jsd = kwargs.get('bypass_jsd', None)

        if self.bypass_jsd is True:
            self.port = int(kwargs.get('port', 40051))


        # Only one of 'rhandle' or 'host' should be provided
        if 'rhandle' in kwargs and 'host' in kwargs:
            logging.error(
                "Only one of 'rhandle' and 'host' should be provided")
            raise AttributeError

        # Either 'rhandle' or 'host' should be provided
        if 'rhandle' not in kwargs and 'host' not in kwargs:
            logging.error("'rhandle' or 'host' attribute is mandatory")
            raise AttributeError

        if 'rhandle' in kwargs:
            self.host = kwargs['rhandle'].host
        else:
            self.host = kwargs['host']

        if 'rhandle' in kwargs and \
                (not self.user or not self.password):
            if kwargs['rhandle'].os.upper() == 'JUNOS':
                kwargs['rhandle'].get_credentials()
                self.user = kwargs['rhandle'].user
                self.password = kwargs['rhandle'].password
            else:
                logging.error("'rhandle' should be a Junos Device object")
                raise AttributeError

        # 'host': 'user' and 'password' are mandatory
        if 'host' in kwargs and (not self.user or not self.password):
            logging.error(
                "'user' and 'password' are mandatory if 'host' is used")
            raise AttributeError
        self.services = {}

    def get_grpc_id(self):
        """
          Used to encode the grpc channel id

          :return: encoded channel_id
        """
        return self.channel_id.encode('utf-8')


    def client_metadata(self, unused_metadata):
        """
        Client Metadata to add client ID for beta channel (Used for bypass_jsd opetion)

        :return: client_id

        """
        return (('client-id', self.client_id),)


    def open(self):
        """
        Opens a grpc channel

        :return: True, upon successful creation & authentication of channel,
                 False, in case of failure

        """

        timeout = self.timeout

        import grpc # pylint: disable=import-error
        import authentication_service_pb2 # pylint: disable=import-error
        import authentication_service_pb2_grpc # pylint: disable=import-error
        from grpc.beta import implementations # pylint: disable=import-error

        try:
            host_port = self.host + ':' + str(self.port)

            if self.bypass_jsd is True:
                logging.info(
                    'Using implementations.insecure_channel on %s', self.host)

                channel = implementations.insecure_channel(
                    host=self.host, port=self.port)
            else:
#                 channel = grpc.insecure_channel(
#                     target=host_port,
#                 )
                # use_local_subchannel_pool is supported from grpcio=1.19.0
                # Helps retain the multi channel functionality of gRPC
                # Automatically ignored for unsupported versions by gRPC (backwards compatible)

                channel = grpc.insecure_channel(host_port, options=[('grpc.use_local_subchannel_pool', 1)])

            # Generate random client id
            client_id_list = []
            #client_id = str(random.randint(100000, 1000000))
            #Making the client_id same as channel_id

            client_id = self.channel_id
            client_id_list.append(client_id)
            self.client_id = client_id
            # while True:
            #     if client_id not in client_id_list:
            #         client_id_list.append(client_id)
            #         self.client_id = client_id
            #         break
            #     else:
            #         client_id = str(random.randint(100000, 1000000))
            if self.bypass_jsd is not True:
                stub = authentication_service_pb2_grpc.LoginStub(channel)
                logging.info(
                    "Channel created via JSD")

                try:
                    login_response = \
                        stub.LoginCheck(
                            authentication_service_pb2.LoginRequest(
                                user_name=self.user,
                                password=self.password,
                                client_id=client_id
                            ),
                            timeout
                        )

                    if login_response.result:
                        logging.info('GRPC client-server connect is successful')
                    else:
                        logging.error('GRPC client-server connect has failed')
                        return False

                except Exception as exp:
                    logging.error(exp)
                    return False

            self.channel = channel
            logging.info(
                'GRPC channel created successfully for %s', self.host)
            return True

        except Exception as exp:
            logging.error(exp)
            return False

    def _create_stub(self, service, service_name=None):
        """
        Internal method to create a stub for a service

        :param service: *MANDATORY* : Grpc service

        :param service_name:
            *OPTIONAL* : Unique identifier with which service has to referenced

        :return: True

        """
        module = self._get_module_name(service)

        module = importlib.import_module(module, package=None)
        if not service_name:
            service_name = service

        if "_" in service:
            service = service.split("_")[1]

        if self.bypass_jsd is True:
            logging.info("Stub will use metadata for beta channel implementation")
            mcall = getattr(module, 'beta_create_' + service + '_stub')
            self.services[service_name] = mcall(self.channel, metadata_transformer=self.client_metadata)
        else:
            mcall = getattr(module, service + 'Stub')
            self.services[service_name] = mcall(self.channel)


        msg = 'Stub created successfully for %s:%s' % (self.host, service_name)
        logging.info(msg)

        return True

    def send_api(self, *args, **kwargs):
        """
        Sends API request on the established service
        :param service: Name of the stub service in which api request
            needs to be sent
            *MANDATORY*: when param 'api' or 'api_call' options are used
            *OPTIONAL* : when param 'id' option is used

        :param api:  *OPTIONAL* : API name
                    (Option 1 to invoke/exec an API)

        :param args: Arguments to the API request
                     *MANDATORY*: when param 'api' is used
                     *OPTIONAL* : otherwise

        :param api_call:  *OPTIONAL* : API name with arguments
                         (Option 2 to invoke/exec an API)

        :param library:
            file containing the list of grpc library files to import
            *MANDATORY*: when param 'api_call' is used
                         refers to a yaml file which has the list of grpc
                         library files to import
            *OPTIONAL* : otherwise
            Sample file contents:
            {
               'Libraries': ['mgd_service_pb2.py','openconfig_service_pb2.py'],
            }

        (Below id + yaml_file combo. is the option 3 to invoke/exec an API)
        :param id: *OPTIONAL* :
            - Tag/id name in the yaml file to match
            - This would be the main 'keys' in the dictionary format contents
                of the yaml file
            - Refer to the "CAT" tool to generate this file given
                the .proto file as input
            - The "CAT" tool generated file is then required to be manually
                edited to supply input to the API call

        :param yaml_file :
            yaml file, which has the service & API calls with args
            *MANDATORY*: when param 'id' is used
            *OPTIONAL* : otherwise

        :return:  API execution result
        """

        # Set default values
        kwargs['timeout'] = kwargs.get('timeout', 300)

        # grpc_lib_path = self.grpc_lib_path

        # If user specifies service, api and arguments for the lego API call
        if 'api' in kwargs:
            if 'service' not in kwargs:
                logging.error(
                    "'service' parameter is required when 'api' " +
                    "parameter is provided")
                return False

            if 'args' not in kwargs:
                logging.error(
                    "'args' parameter is required when 'api' parameter " +
                    "is provided")
                return False

            if kwargs['service'] not in self.services:
                self._create_stub(service=kwargs['service'])

            mcall = getattr(self.services[kwargs['service']], kwargs['api'])

            result = mcall(kwargs['args'], kwargs['timeout'])

            logging.info('Result is : %s', result)
            return result

        if 'api_call' in kwargs:
            if 'service' not in kwargs:
                logging.error(
                    "'service' parameter is required when 'api_call' " +
                    "parameter is provided")
                return False
            api_call_string = kwargs['api_call']
            #import yaml

            # Parse yaml library names file
            if 'library' not in kwargs:
                logging.error('GRPC libraries file not provided')
                return False

            try:
                file = file_util.find_file(kwargs['library']) # pylint: disable=redefined-builtin
            except Exception as exp:
                logging.error(exp)
                return False

            logging.info(
                "File containing GRPC Libraries names is : %s", file)
            api_full_data = yaml.safe_load(
                open(file, 'r').read()
            )

            index = api_call_string.find('(')
            if index == -1:
                logging.error("Could not get the arguments from the API call")
                return False
            arguments = api_call_string[index+1:-1]
            y_api = api_call_string[:index]

            # Import required libraries that are specifed in yaml data file
            # Key is Libraries
            for lib in api_full_data['Libraries']:
                if re.search(r'\.py$', lib):
                    lib = lib[:-3]
                lib = lib.replace(os.path.sep, '.')
                module = importlib.import_module(lib, package=None)
                for ele_x in dir(module):
                    globals()[ele_x] = getattr(module, ele_x)

            arguments = eval(arguments)
            if kwargs['service'] not in self.services:
                self._create_stub(service=kwargs['service'])

            msg = 'Sending API on %s:%s' % (self.host, kwargs['service'])
            logging.info(msg)
            logging.info(y_api)

            mcall = getattr(self.services[kwargs['service']], y_api)

            result = mcall(arguments, kwargs['timeout'])

            logging.info('Result is : %s', result)
            return result

        # If User specifies yaml file where the lego api call information is
        # stored.
        # Use CAT build API call
        if 'id' in kwargs:
            if 'yaml_file' not in kwargs:
                logging.error("Yaml file is required when 'id' is provided")
                return False

            try:
                yaml_file = file_util.find_file(kwargs['yaml_file'])
            except Exception as exp:
                logging.error(exp)
                return False

            logging.info(
                "File containing GRPC Libraries and GRPC API calls in yaml format is : %s", yaml_file)

            #import yaml

            # Parse 'yaml_file' file
            api_full_data = yaml.safe_load(
                open(kwargs['yaml_file'], 'r').read()
            )

            api_data = api_full_data[kwargs['id']]
            # temp_keys = api_data.keys()

            # Get service and API name
            y_api_data_keys = list(api_data.keys())
            y_service = y_api_data_keys[0]
            y_api_keys = list(api_data[y_service].keys())
            y_api = y_api_keys[0]

            res0 = CAT.clean_dict(api_data[y_service][y_api])
            res = CAT.split_oneof(res0)
            res1 = CAT.gen_valid(res)
            api_call_string = CAT.str_of_code({y_api: res1[0][0]})

            # Clean API call
            api_call_string = api_call_string.replace('input=', '', 1)
            api_call_string = api_call_string.replace('_cat_enum', '')
            if '_cat_init' in api_call_string:
                api_call_string = re.sub(
                    '_cat_init=.*"', '()', api_call_string)

            # Get arguments of y_api from the api_call_string
            msg = 'Sending API on %s:%s' % (self.host, y_service)
            logging.info(msg)
            logging.info(api_call_string)
            mat = re.search(r'^%s\((.*)\)$' % y_api, api_call_string, re.I)
            arguments = mat.group(1)
            # if mat:
            #     arguments = mat.group(1)
            # else:
            #     logging.error("Could not get the arguments from the API call")
            #     return False

            # Import required libraries that are specifed in yaml data file
            # Key is Libraries
            for lib in api_full_data['Libraries']:
                lib = lib[:-3]
                lib = lib.replace(os.path.sep, '.')
                module = importlib.import_module(lib, package=None)
                for ele_x in dir(module):
                    globals()[ele_x] = getattr(module, ele_x)

            arguments = eval(arguments)
            if y_service not in self.services:
                self._create_stub(service=y_service)

            mcall = getattr(self.services[y_service], y_api)

            result = mcall(arguments, kwargs['timeout'])

            logging.info('Result is : %s', result)

            return result

    def _get_module_name(self, service):
        """
        Internal method to look for the service in
        the GRPC LIB PATH class variable
        :param service: service name, to look for
        :return: name of the module corresponding to the service, if present,
            else False
        """

        grpc_lib_path = self.grpc_lib_path

        # After Lego compliance many APIs have service name common
        # in both new and old version of APIs
        # Below logic requires user to provide jnx_<service> as service name
        # to differentiate between old and new apis


        logging.info("Logging service - %s",service)

        if 'jnx' in service.lower():
            service = service.split("_")[1]
            flag = "-i"
        else:
            flag = "-vi"

        logging.info("service - %s",service)
        logging.info("grpc_lib_path - %s",grpc_lib_path)
        logging.info("grep flag - %s",flag)

        if self.bypass_jsd is True:
            pipe = Popen(
                ['/bin/sh', '-c', 'grep -l \'%s\' %s/*_pb2.py | grep "%s" jnx' % (service, grpc_lib_path, flag)], stdout=PIPE)

            logging.info('grep -l \'%s\' %s/*_pb2.py | grep "%s" jnx' % (service, grpc_lib_path, flag))

        else:
            pipe = Popen(
                ['/bin/sh', '-c', 'grep -l \'%s\' %s/*_grpc.py | grep "%s" jnx' % (service, grpc_lib_path, flag)], stdout=PIPE)

            logging.info('grep -l \'%s\' %s/*_grpc.py | grep "%s" jnx' % (service, grpc_lib_path, flag))



        out0 = pipe.communicate()[0]
        out1 = out0.decode('utf-8')
        out = out1.split('\n')[:-1]

        if len(out) != 1:
            logging.error("Multiple libraries found for service %s", service)
            return False
        mat = re.search(r'.*[/](.*).py$', out[0])

        if not mat:
            return False
        module = mat.group(1)
        return module
