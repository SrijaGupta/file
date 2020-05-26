"""
Facts module to gather system facts
"""
import logging
import re
from jnpr.junos.device import Device as Pyez_Device
from jnpr.toby.hldcl.host import Host
from jnpr.toby.exception.toby_exception import TobyException

class Facts(Host):
    """
    Facts class to gather device details
    """
    def _get_credentials(self):
        """
        Populates self.user and self.password based on user inputs. If user
        has not provided then try to get them from default credentials. Else
        raise an exception.

        :param kwargs: Keyword arguments provided by the user to create a
        device object

        :return: Tuple containing username and password
        """

        # Check if user and password are passed arguments
        if not self._kwargs.get('user') or not self._kwargs.get('password'):
            from jnpr.toby.frameworkDefaults.credentials import JUNOS
            # Check if default credentials are available
            if not JUNOS['USERNAME'] or not JUNOS['PASSWORD']:
                raise TobyException("Username/Password cannot be determined")
            return JUNOS['USERNAME'], JUNOS['PASSWORD']
        return self._kwargs['user'], self._kwargs['password']

    def _connect(self):

        # Default connect_mode to ssh
        connect_mode = self._kwargs.get('connect_mode', 'ssh').lower()
        # Check for valid connect modes
        if connect_mode not in ('telnet', 'ssh', 'console', 'netconf'):
            raise TobyException(
                'Invalid connect mode({0}) specified. Connect mode can be '
                'telnet/ssh/console/netconf'.format(connect_mode)
            )
        handle = None
        try:
            user, password = self._get_credentials()
            device_args = {'host': self._kwargs['host'], 'user': user,
                           'passwd': password, 'gather_facts': False}
            if connect_mode == 'ssh':
                device_args['port'] = 22
            if connect_mode == 'telnet' or connect_mode == 'console':
                device_args['mode'] = 'telnet'
            if self._kwargs['pyez_port'] is not None:
                device_args['port'] = int(self._kwargs['pyez_port'])
            handle = Pyez_Device(**device_args)
            handle.open()
        except Exception as exp:
            logging.error('Could not connect to device ' + self._kwargs['host'] +
                          ':' + str(exp))
        return handle

    def _get_juniper_node_facts(self):
        # Populate common properties
        facts_list = self._get_juniper_details()
        self.reg = facts_list[1]
        devip = self._get_host_ip(re_name=self.reg)
        is_dual_re = facts_list[0]
        hostname = facts_list[2]
        model = facts_list[3]
        devos = facts_list[4]
        facts_re = {'name': hostname, 'mgt-ip': devip, 'model': model, 'osname': devos}
        facts_node = {self.reg: facts_re}

        if is_dual_re:
            other_re = facts_list[5]
            other_re_ip = self._get_host_ip(re_name=other_re)
            other_re_hostname = facts_list[6]
            other_re_model = facts_list[7]
            other_re_os = facts_list[8]
            facts_re = {'name': other_re_hostname, 'mgt-ip': other_re_ip,
                        'model': other_re_model, 'osname': other_re_os}
            facts_node[other_re] = facts_re

        facts_node['os'] = facts_node['re0']['osname']
        facts_node['model'] = facts_node['re0']['model']

        return facts_node

    def _get_srx_facts(self):
        self.reg = 're0'
        facts_list = self._get_srx_details()
        is_ha = facts_list[0]
        self.node_name = facts_list[1]
        hostname = facts_list[2]
        model = facts_list[3]
        devos = facts_list[4]
        if is_ha:
            devip = self._get_host_ip_srx(node=self.node_name)
        else:
            devip = self._get_host_ip_srx(node=self.reg)
        facts_re = {'name': hostname, 'mgt-ip': devip, 'model': model, 'osname': devos}
        facts_node = {self.reg: facts_re}
        facts_system = {self.node_name: facts_node}
        facts_system['node0']['os'] = facts_system['node0']['re0']['osname']
        facts_system['node0']['model'] = facts_system['node0']['re0']['model']
        if is_ha:
            other_node_re = 're0'
            other_node_name = self._other_node_name()
            other_node_ip = self._get_host_ip_srx(node=other_node_name)
            other_node_hostname = facts_list[6]
            other_node_model = facts_list[7]
            other_node_os = facts_list[8]
            facts_re = {'name': other_node_hostname, 'mgt-ip': other_node_ip,
                        'model': other_node_model, 'osname': other_node_os}
            facts_node = {other_node_re: facts_re}
            facts_system[other_node_name] = facts_node
            facts_system['node1']['os'] = facts_system['node1']['re0']['osname']
            facts_system['node1']['model'] = facts_system['node1']['re0']['model']

        return facts_system

    def _get_juniper_details(self):
        response = self.handle.cli(command='show version invoke-on all-routing-engines',
                                   format='xml', warning=False)
        print(type(response))



        multi_re = response.findall('multi-routing-engine-item')
        if len(multi_re) > 0:
            re_name0 = multi_re[0].find('re-name').text
            model0 = multi_re[0].find('software-information/product-model').text
            host_name0 = multi_re[0].find('software-information/host-name').text
            os_list = multi_re[0].findall('software-information/package-information')
            os0 = os_list[0].find('name').text
            try:
                re_name1 = multi_re[1].find('re-name').text
                model1 = multi_re[1].find('software-information/product-model').text
                host_name1 = multi_re[1].find('software-information/host-name').text
                os_list1 = multi_re[1].findall('software-information/package-information')
                os1 = os_list1[0].find('name').text
                dual_re = True
            except:
                re_name1 = None
                model1 = None
                host_name1 = None
                os1 = None
                dual_re = False
            facts_list = [dual_re, re_name0, host_name0, model0, os0, re_name1, host_name1,
                          model1, os1]
        else:
            try:
                re_name = response.find('re-name').text
                model = response.find('product-model').text
                host_name = response.find('host-name').text
                os_list = response.findall('package-information')
                devos = os_list[0].find('name').text
                facts_list = [False, re_name, host_name, model, devos, None, None, None, None]
            except:
                raise TobyException('Could not retrieve details')
        return facts_list

    def _get_srx_details(self):
        response = self.handle.cli(command='show version', format='xml', warning=False)
        multi_re = response.findall('multi-routing-engine-item')
        if len(multi_re) > 0:
            node_name0 = multi_re[0].find('re-name').text
            model0 = multi_re[0].find('software-information/product-model').text
            host_name0 = multi_re[0].find('software-information/host-name').text
            os_list = multi_re[0].findall('software-information/package-information')
            os0 = os_list[0].find('name').text
            node_name1 = multi_re[1].find('re-name').text
            model1 = multi_re[1].find('software-information/product-model').text
            host_name1 = multi_re[1].find('software-information/host-name').text
            os_list1 = multi_re[1].findall('software-information/package-information')
            os1 = os_list1[0].find('name').text
            dual_re = True
            facts_list = [dual_re, node_name0, host_name0, model0, os0, node_name1,
                          host_name1, model1, os1]
        else:
            try:
                node_name = 'node0'
                model = response.find('product-model').text
                host_name = response.find('host-name').text
                os_list = response.findall('package-information')
                devos = os_list[0].find('name').text
                facts_list = [False, node_name, host_name, model, devos, None, None, None, None]
            except:
                raise TobyException('Could not retrieve details')

        return facts_list

    def get_model(self):
        """
        Returns  model of the device
        """
        version = self.handle.rpc.get_software_information()
        multi_re = version.findall('multi-routing-engine-item')
        if len(multi_re) > 0:
            model = multi_re[0].find('software-information/product-model').text
            if re.search(r'MX\d+', model, re.I):
                return 'MX'
            elif re.search(r'VSRX', model, re.I):
                return 'VSRX'
            elif re.search(r'SRX\d+', model, re.I):
                return 'SRX'
            elif re.search(r'ex\d+', model, re.I):
                return 'EX'
            elif re.search(r'qfx\d+', model, re.I):
                return 'QFX'
            elif re.search(r'ocx\d+', model, re.I):
                return 'OCX'
            elif re.search(r'nfx\d+', model, re.I):
                return 'NFX'
        try:
            model = version.find('product-model').text
        except:
            raise TobyException('Could not retrieve model')
        return model

    def _other_re_slot_name(self):
        """
        Other RE name
        :return: Return other RE name
        """
        other_re = None
        if self.reg == 're0':
            other_re = 're1'
        elif self.reg == 're1':
            other_re = 're0'
        return other_re

    def _other_node_name(self):
        """
        Other Node name
        :return: Return other Node name
        """
        other_node = None
        if self.node_name == 'node0':
            other_node = 'node1'
        elif self.node_name == 'node0':
            other_node = 'node1'
        return other_node

    def _get_host_ip(self, re_name):
        """
        Get the management IP of RE

        :param re_name: Name of RE whose management IP needs to be retrieved
        :return: Management IP address. Raises exception in case of failure.
        """
        re_name = re_name.lower()
        host_ip = None
        response = self.handle.rpc.get_configuration({'database': 'committed'})
        response = response.findall('groups[name="{0}"]'.format(re_name))
        em0_data = response[0].find('interfaces/interface[name="em0"]')
        if em0_data is not None:
            host_ip = em0_data.find('unit/family/inet/address/name').text
        else:
            fxp0_data = response[0].find('interfaces/interface[name="fxp0"]')
            if fxp0_data is not None:
                host_ip = fxp0_data.find('unit/family/inet/address/name').text
        if not host_ip:
            raise TobyException('Could not determined other RE management IP')
        #host_ip = host_ip.split('/')[0]
        return host_ip

    def _get_host_ip_srx(self, node):
        """
        Get the management IP of chassis

        :param re_name: Name of RE whose management IP needs to be retrieved
        :param node: Name of the srx node('node0'/'node1')
        :return: Management IP address. Raises exception in case of failure.
        """
        response = self.handle.rpc.get_configuration(
            {'database': 'committed'}
        )
        response = response.findall('groups[name="{0}"]'.format(node))
        fxp0_data = response[0].find('interfaces/interface[name="fxp0"]')
        if fxp0_data is not None:
            host_ip = fxp0_data.find('unit/family/inet/address/name').text
        if not host_ip:
            raise TobyException('Could not determined management IP')
        #host_ip = host_ip.split('/')[0]
        return host_ip

    def __init__(self, *args, **kwargs):
        # Check if host is provided
        if 'host' not in kwargs:
            raise TobyException("'host' is mandatory")
        kwargs['os'] = kwargs.get('os', 'JUNOS')

        # Connect to given hostname/
        self.reg = None
        self.node_name = None
        self._kwargs = kwargs
        self.host = kwargs['host']
        self.handle = self._connect()
        self.model = self.get_model()
        mat = re.search(r'(\D+)\d*', self.model, re.I)
        if mat:
            self.series = mat.group(1).upper()
        else:
            raise TobyException('Could not determine model')

    def system_facts(self):
        """
        Returns systems facts dictionary
        """
        if self.series in ('SRX', 'VSRX'):
            response = self._get_srx_facts()
        else:
            node_info = self._get_juniper_node_facts()
            response = {'primary': node_info}
        from pprint import pprint
        pprint(response)
        return response

    def pyez_facts(self):
        """
        Returns pyEZ handle facts
        """
        self.handle.facts_refresh()
        return self.handle.facts

    def close(self):
        """
        Close the connection
        """
        self.handle.close()
        return True

#Unittesting
#a = Facts(host="mayo", user="regress", password="MaRtInI", os="JUNOS")
#pprint(a.system_facts())
#pprint(a.pyez_facts())
#a.close()
