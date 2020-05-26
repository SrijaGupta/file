#!/usr/local/bin/python3

import sys
import copy
import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values
from jnpr.toby.trafficgen.exabgp.exabgp_master import exabgp_master

import builtins
builtins.t = MagicMock()


class Test_exabgp_master(unittest.TestCase):
    def setUp(self):
        self.exb = exabgp_master()
        #self.exb.create_generic_exabgp_file = MagicMock()
        self.device = MagicMock()
        self.device.shell = MagicMock()
        self.device.log = MagicMock()

    def test_ExabgpMaster_init_without_arg(self):
        self.assertEqual(self.exb._path_loc, '/tmp')

    def test_ExabgpMaster_init_with_arg(self):
        path_loc = '/home/regress'
        self.exb_with_path = exabgp_master(path_loc)
        self.assertEqual(self.exb_with_path._path_loc, path_loc)

    def test_stop_exabgp_routing_device_exception(self):
        with self.assertRaises(Exception) as context:
            self.exb.stop_exabgp_routing()
        self.assertTrue(
            'device is mandatory argument' in str(context.exception))
    def test_stop_exabgp_routing(self):
        self.assertEqual(self.exb.stop_exabgp_routing(device=self.device), None)

    def test_start_exabgp_routing_device_exception(self):
        with self.assertRaises(Exception) as context:
            self.exb.start_exabgp_routing()
        self.assertTrue(
            'device is mandatory argument' in str(context.exception))
    def test_start_exabgp_routing(self):
        self.assertEqual(self.exb.start_exabgp_routing(device=self.device), None)

    def test_cleanup_exabgp_device_exception(self):
        with self.assertRaises(Exception) as context:
            self.exb.cleanup_exabgp()
        self.assertTrue(
            'device is mandatory argument' in str(context.exception))
    def test_cleanup_exabgp(self):
        self.assertEqual(self.exb.cleanup_exabgp(device=self.device), None)

    def test_check_exabgp_and_path_availability_device_directory_exists(self):
        response_path = Values()
        self.device.shell.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "exabgp /xxxxxx"
        self.assertEqual(self.exb.check_exabgp_and_path_availability(device=self.device), True)

    def test_check_exabgp_and_path_availability_device_directory_not_exists_so_created(self):
        response_path = Values()
        self.device.shell.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "exabgp / No such file or directory"
        self.assertEqual(self.exb.check_exabgp_and_path_availability(device=self.device), True)

    def test_check_exabgp_and_path_availability_device_directory_not_exists_and_permission_denied(self):
        response_path = Values()
        self.device.shell.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "No such file or directory and Permission denied"
        self.assertEqual(self.exb.check_exabgp_and_path_availability(device=self.device), False)

    def test_check_exabgp_and_path_availability_device_exception(self):
        with self.assertRaises(Exception) as context:
            self.exb.check_exabgp_and_path_availability()
        self.assertTrue(
            'device is mandatory argument' in str(context.exception))

    def test_check_exabgp_and_path_availability_not_installed(self):
        response_path = Values()
        self.device.shell.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "exa"
        self.assertEqual(self.exb.check_exabgp_and_path_availability(device=self.device), False)

    def test_check_exabgp_and_path_availability_installed(self):
        response_path = Values()
        self.device.shell.return_value = response_path
        response_path.response = MagicMock()
        response_path.response.return_value = "exabgp /usr/sbin/exabgp /etc/exabgp /usr/share"
        self.assertEqual(self.exb.check_exabgp_and_path_availability(device=self.device), True) 

    def test_create_generic_exabgp_file(self):
        response_script = Values()
        self.device.shell.return_value = response_script
        response_script.response = MagicMock()
        response_script.response.return_value = "xxxx generic_exabgp.py: No such file or directory"
        self.assertEqual(self.exb.create_generic_exabgp_file(device=self.device), None)

    def test_create_exabgp_files_device_exception(self):
        with self.assertRaises(Exception) as context:
            self.exb.create_exabgp_files()
        self.assertTrue(
            'Device handle is a mandatory Argument' in str(context.exception))

    def test_create_exabgp_files_with_dev_handle_without_kwarg(self):
        with self.assertRaises(Exception) as context:
            self.exb.create_exabgp_files(device=self.device)
        self.assertTrue(
            'base_local_ip is mandatory argument' in str(context.exception))

    def test_create_exabgp_files_exception_base_remote_ip(self):
        with self.assertRaises(Exception) as context:
            self.exb.create_exabgp_files(device=self.device,base_local_ip='10.0.0.0')
        self.assertTrue(
            'base_remote_ip is mandatory argument' in str(context.exception))

    def test_create_exabgp_files_exception_base_local_as(self):
        with self.assertRaises(Exception) as context:
            self.exb.create_exabgp_files(device=self.device, base_local_ip='10.0.0.0', base_remote_ip='20.0.0.0')
        self.assertTrue(
            'base_local_as is mandatory argument' in str(context.exception))

    def test_create_exabgp_files_exception_remote_as(self):
        with self.assertRaises(Exception) as context:
            self.exb.create_exabgp_files(device=self.device, base_local_ip='10.0.0.0', base_remote_ip='20.0.0.0', base_local_as=500)
        self.assertTrue(
            'remote_as is mandatory argument' in str(context.exception))

    def test_create_exabgp_files_exception_base_rt_prefix(self):
        with self.assertRaises(Exception) as context:
            self.exb.create_exabgp_files(device=self.device, base_local_ip='10.0.0.0', base_remote_ip='20.0.0.0', base_local_as=500, remote_as=600)
        self.assertTrue(
            'base_rt_prefix is mandatory argument' in str(context.exception))

    def test_create_exabgp_files_v4(self):
        self.exb.create_generic_exabgp_file = MagicMock()
        self.assertEqual(self.exb.create_exabgp_files(device=self.device, peer_count=10, base_local_ip='20.0.0.2', base_remote_ip='20.0.0.1', base_local_as=501, remote_as=500, base_rt_prefix='100.0.0.1/32'), None)
    def test_create_exabgp_files_v6(self):
        self.exb.create_generic_exabgp_file = MagicMock()
        self.assertEqual(self.exb.create_exabgp_files(device=self.device, peer_count=10, base_local_ip='2000::2', base_remote_ip='2000::1', base_local_as=501, remote_as=500, base_rt_prefix='4000::1/128', base_router_id= '1::1',routes_per_peer=10, rt_rate=100), None)
if __name__ == '__main__':
    unittest.main()
