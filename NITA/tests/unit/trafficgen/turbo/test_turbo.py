import sys

import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values

import builtins
builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

from jnpr.toby.trafficgen.turbo.turbo import turbo


class TestTurbo(unittest.TestCase):


    def test_instanstiate_turbo_class(self):
        self.assertEqual(isinstance(turbo(test=None), turbo), True)

    def test_turbo_init(self):
    	self.client_ports = ['r0h0']
    	self.server_ports = ['r0h1']
    	self.client_list = ['h0']
    	self.server_list = ['h1']
    	self.client_names = []
    	self.server_names = []
    	self.chassis = {}
    	self.chassis['client'] = {}
    	self.chassis['server'] = {}
    	self.chassis['client']['turbo-vm2'] = {}
    	self.chassis['server']['turbo-vm1'] = {}
    	self.chassis = {'server': {'a': {'ip_list': ['5.0.0.2/24'], 'gw_list': ['5.0.0.1'], 'port_list': ['eth1']}}, 'client': {'b': {'ip_list': ['4.0.0.2/24'], 'gw_list': ['4.0.0.1'], 'port_list': ['eth1']}}}	
    	#for client in self.client_list:
    	#	self.turbo.
    	self.assertEqual(turbo.init(self,port_pair={'client_ports': {'h0': ['r0h0']}, 'server_ports': {'h1': ['r0h1']}}), True)

    '''def test_turbo_configure_chassis(self):
    	self.chassis = {}
    	self.chassis['client'] = {}
    	self.chassis['server'] = {}
    	self.chassis['client']['turbo-vm2'] = {}
    	self.chassis['server']['turbo-vm1'] = {}
    	self.chassis = {'server': {'turbo-vm2': {'ip_list': ['5.0.0.2/24'], 'gw_list': ['5.0.0.1'], 'port_list': ['eth1']}}, 'client': {'turbo-vm1': {'ip_list': ['4.0.0.2/24'], 'gw_list': ['4.0.0.1'], 'port_list': ['eth1']}}}	
    	json_body_client = {'role': 'client', 'is_ns_enabled': True}
    	json_body_server = {'role': 'client', 'is_ns_enabled': True}
    	self.assertEqual(turbo.configure_chassis(self), True)

    def test_turbo_configure_networks(self):
    	self.chassis = {}
    	self.chassis['client'] = {}
    	self.chassis['server'] = {}
    	self.chassis['client']['turbo-vm2'] = {}
    	self.chassis['server']['turbo-vm1'] = {}
    	self.chassis = {'server': {'turbo-vm2': {'ip_list': ['5.0.0.2/24'], 'gw_list': ['5.0.0.1'], 'port_list': ['eth1']}}, 'client': {'turbo-vm1': {'ip_list': ['4.0.0.2/24'], 'gw_list': ['4.0.0.1'], 'port_list': ['eth1']}}}	
    	json_body_client = {'role': 'client', 'is_ns_enabled': True}
    	json_body_server = {'role': 'client', 'is_ns_enabled': True}
    	self.assertEqual(turbo.configure_networks(self), True)

    def test_turbo_start_traffic(self):
    	self.chassis = {}
    	self.chassis['client'] = {}
    	self.chassis['server'] = {}
    	self.chassis['client']['turbo-vm2'] = {}
    	self.chassis['server']['turbo-vm1'] = {}
    	self.chassis = {'server': {'turbo-vm2': {'ip_list': ['5.0.0.2/24'], 'gw_list': ['5.0.0.1'], 'port_list': ['eth1']}}, 'client': {'turbo-vm1': {'ip_list': ['4.0.0.2/24'], 'gw_list': ['4.0.0.1'], 'port_list': ['eth1']}}}	
    	json_body_client = {'role': 'client', 'is_ns_enabled': True}
    	json_body_server = {'role': 'client', 'is_ns_enabled': True}
    	self.assertEqual(turbo.start_traffic(self), True)

    def test_turbo_stop(self):
    	self.chassis = {}
    	self.chassis['client'] = {}
    	self.chassis['server'] = {}
    	self.chassis['client']['turbo-vm2'] = {}
    	self.chassis['server']['turbo-vm1'] = {}
    	self.chassis = {'server': {'turbo-vm2': {'ip_list': ['5.0.0.2/24'], 'gw_list': ['5.0.0.1'], 'port_list': ['eth1']}}, 'client': {'turbo-vm1': {'ip_list': ['4.0.0.2/24'], 'gw_list': ['4.0.0.1'], 'port_list': ['eth1']}}}	
    	json_body_client = {'role': 'client', 'is_ns_enabled': True}
    	json_body_server = {'role': 'client', 'is_ns_enabled': True}
    	self.assertEqual(turbo.stop_traffic(self), True)'''


if __name__ == '__main__':
        unittest.main()

