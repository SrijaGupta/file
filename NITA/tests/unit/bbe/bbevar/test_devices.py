"""
devices.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbevar.bbevars import BBEVars
from jnpr.toby.bbe.bbevar.devices import BBEVarDevice
import builtins

builtins.t = MagicMock(spec=init)

class TestDevices(unittest.TestCase):
    """
    test devices.py
    """
    def test_class_devices(self):
        device_handle = MagicMock()
        device_id = 'r0'
        bbevar = {'resources': {'r0': {'system': {'primary': {'controllers': {'if0': {'domain': 'englab.juniper.net'}},
                                                              'mgt-ip': '10.9.1.123/21',
                                                              'name': 'test',
                                                              'osname': 'junos',
                                                              'dh': device_handle}}}}}
        device = BBEVarDevice(bbevar, device_id)
        self.assertIsInstance(device, BBEVarDevice)
        self.assertIsInstance(device.device_tags, list)
        self.assertIsInstance(device.has_vrf, bool)
        self.assertEqual(device.vrf, None)
        self.assertIsInstance(device.device_id, str)
        self.assertIsInstance(device.device_name, str)
        self.assertIsInstance(device.device_controllers, dict)
        self.assertIsInstance(device.device_os, str)
        self.assertEqual(device.device_model, None)
        self.assertEqual(device.device_make, None)
        self.assertEqual(device.device_labserver, None)
        self.assertIsInstance(device.device_handle, object)
        self.assertIsInstance(device.device_config, object)
        self.assertIsInstance(device.device_interfaces, list)
        self.assertIsInstance(device.is_dut, bool)
        self.assertIsInstance(device.is_mxvc, bool)
        self.assertIsInstance(device.is_lns, bool)
        self.assertIsInstance(device.is_tomcat, bool)
        print(device)
        bbevar['resources']['r0']['config'] = {'vrf': {}, 'quickcst': {}}
        bbevar['resources']['r0']['system']['primary']['os'] = 'junos'
        bbevar['resources']['r0']['system']['primary'].pop('osname')
        device = BBEVarDevice(bbevar, device_id)
        self.assertIsInstance(device, BBEVarDevice)
        bbevar = builtins.t
        device = BBEVarDevice(bbevar, device_id)
        self.assertIsInstance(device, BBEVarDevice)



if __name__ == '__main__':
    unittest.main()