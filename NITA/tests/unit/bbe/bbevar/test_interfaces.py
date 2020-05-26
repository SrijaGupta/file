"""
interfaces.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbevar.bbevars import BBEVars
from jnpr.toby.bbe.bbevar.interfaces import BBEVarInterface
import builtins

builtins.t = MagicMock(spec=init)

class TestInterfaces(unittest.TestCase):
    """
    test interfaces.py
    """
    def test_class_interface(self):
        device_id = 'r0'
        interface_id = 'access0'
        device_handle = MagicMock()
        bbevar = {'resources': {'r0': {'interfaces': {'access0': {'link': 'radius0', 'management': 0, 'name': 'eth1',
                                                                  'pic': 'eth1', 'type': ['L1', 'ether', 'eth']}},
                                       'system': {'primary': {'controllers': {'if0': {'domain': 'englab.juniper.net'}},
                                                              'mgt-ip': '10.9.1.123/21',
                                                              'name': 'test',
                                                              'dh': device_handle}}}}}

        interface = BBEVarInterface(bbevar, device_id, interface_id)
        self.assertIsInstance(interface, BBEVarInterface)
        bbevar['resources']['r0']['interfaces']['access0']['config'] = {'vlan':{'start': '1',
                                                                                'step': '1',
                                                                                'repeat': '1',
                                                                                'length': '10'},
                                                                        'svlan':{'start': '1',
                                                                                 'step': '1',
                                                                                 'repeat': '2',
                                                                                 'length': '5'},
                                                                        'ae': {'active': True,
                                                                               'bundle': 'ae0',
                                                                               'enable': 0}}
        interface = BBEVarInterface(bbevar, device_id, interface_id)
        self.assertIsInstance(interface, BBEVarInterface)
        self.assertIsInstance(interface.device_id, str)
        self.assertIsInstance(interface.device_name, str)
        self.assertIsInstance(interface.device_mgt_ip, str)
        self.assertIsInstance(interface.interface_id, str)
        self.assertIsInstance(interface.interface_name, str)
        self.assertIsInstance(interface.interface_link, str)
        self.assertIsInstance(interface.interface_pic, str)
        self.assertIsInstance(interface.interface_type, list)
        self.assertIsInstance(interface.interface_config, dict)
        self.assertIsInstance(interface.interface_id, str)
        self.assertIsInstance(interface.interface_description, str)
        self.assertIsInstance(interface.is_ae_active, int)
        self.assertEqual(interface.is_ae, False)
        self.assertIsInstance(interface.ae_bundle, str)
        self.assertIsInstance(interface.device_handle, object)
        interface.rt_ethernet_handle = 'ethernet'
        self.assertEqual(interface.rt_ethernet_handle, 'ethernet')
        interface.rt_device_group_handle = 'group'
        self.assertEqual(interface.rt_device_group_handle, 'group')
        interface.rt_ipv4_handle = 'ipv4'
        self.assertEqual(interface.rt_ipv4_handle, 'ipv4')
        interface.rt_ipv6_handle = 'ipv6'
        self.assertEqual(interface.rt_ipv6_handle, 'ipv6')
        interface.rt_lns_handle = 'lns'
        self.assertEqual(interface.rt_lns_handle, 'lns')
        interface.rt_lns_server_session_handle = 'session'
        print(interface)
        self.assertEqual(interface.rt_lns_server_session_handle, 'session')
        bbevar['resources']['r0']['interfaces']['access0']['config']['ae'] = {'enable': '1'}
        interface = BBEVarInterface(bbevar, device_id, interface_id)
        self.assertIsInstance(interface, BBEVarInterface)
        interface_id = 'uplink0'
        bbevar['resources']['r0']['interfaces']['uplink0'] ={'config': {'ae': '0'}}
        interface = BBEVarInterface(bbevar, device_id, interface_id)
        self.assertIsInstance(interface, BBEVarInterface)
        bbevar = builtins.t
        interface = BBEVarInterface(bbevar, device_id, interface_id)
        self.assertIsInstance(interface, BBEVarInterface)



if __name__ == '__main__':
    unittest.main()