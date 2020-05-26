import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.bbe.bbeutils.junosutil import *
from jnpr.toby.bbe.errors import BBEDeviceError
from jnpr.toby.init.init import init
builtins.t = MagicMock(spec=init)
builtins.t.log = MagicMock()


class TestJunosUtil(unittest.TestCase):
    """
    TestJunosUtil class to handle junosutil.py unit tests
    """
    def test_check_handle(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = None
        try:
            builtins.t.get_handle.return_value = None
            obj1._check_handle()
        except Exception as err:
            self.assertIsInstance(err, BBEDeviceError)

        builtins.t.get_handle.return_value = MagicMock()

        self.assertEqual(obj1._check_handle(), None)

    def test_set_bbe_junos_util_device_handle(self):
        obj1 = BBEJunosUtil()
        handle = MagicMock()
        obj1.set_bbe_junos_util_device_handle(handle)
        self.assertEqual(obj1.router_handle, handle)

    def test_get_subscriber_count(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = MagicMock()
        test_args = {'client-type':'dhcp', 'routing-instance':'retailer1'}
        self.assertIsInstance(obj1.get_subscriber_count(**test_args), tuple)

    def test_get_pppoe_subscriber_count(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = MagicMock()
        self.assertIsInstance(obj1.get_pppoe_subscriber_count('retailer1'), tuple)

    def test_get_dhcp_subscriber_count(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = MagicMock()
        self.assertIsInstance(obj1.get_dhcp_subscriber_count('retailer1'), tuple)

    def test_get_vlan_subscriber_count(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = MagicMock()
        self.assertIsInstance(obj1.get_vlan_subscriber_count('retailer1'), tuple)

    def test_oob_get_vlan_subscriber_count(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = MagicMock()
        self.assertIsInstance(obj1.get_vlan_oob_subscriber_count('retailer1'), tuple)

    def test_get_l2tp_subscriber_count(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = MagicMock()
        self.assertIsInstance(obj1.get_l2tp_subscriber_count('retailer1'), tuple)

    def test_get_subscriber_count_by_state(self):
        obj1 = BBEJunosUtil()
        obj1.router_handle = MagicMock()
        test_args = {'state': 'active', 'client_type': 'dhcp', 'routing_instance': 'retailer1'}
        self.assertIsInstance(obj1.get_subscriber_count_by_state(**test_args), tuple)

    @patch('time.sleep')
    @patch('time.time')
    def test_cpu_settle(self, patch_time, patch_sleep):
        obj1 = BBEJunosUtil()
        obj1.set_bbe_junos_util_device_handle(MagicMock())
        obj1.router_handle.shell.return_value.resp = 'hw.ncpu: 4'

        obj2 = MagicMock()
        obj2.resp = 'Count: 4 lines'
        obj3 = MagicMock()
        obj3.resp = "PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND\r\n" \
                    "11 root     155 ki31     0K    64K CPU1    1 612.1H 100.00% idle{idle: cpu1}\r\n" \
                    "   11 root     155 ki31     0K    64K CPU2    2 611.8H  99.76% idle{idle: cpu2}\r\n" \
                    "   11 root     155 ki31     0K    64K RUN     3 611.7H  99.66% idle{idle: cpu3}\r\n" \
                    "   11 root     155 ki31     0K    64K CPU0    0 610.2H  97.27% idle{idle: cpu0}\r\n" \
                    "21880 root      22    0   442M 52068K nanslp  1  29.9H   4.05% chassisd{chassisd}\r\n" \
                    "22008 root      20    0   357M 13080K select  3 170:45   0.20% license-check\r\n" \
                    "22387 root      20    0   598M   206M select  0 122:30   0.10% repd{repd}\r\n" \
                    "22382 root      20    0   571M   154M select  1  59:43   0.10% jl2tpd{jl2tpd}\r\n" \
                    "22039 root      20    0   717M   308M select  2 266:08   0.00% authd\r\n" \
                    "21993 root      20    0   901M   324M select  3 162:10   0.00% bbe-smgd{bbe-smgd}\r\n"

        obj1.router_handle.cli.side_effect = [obj2, obj3]
        try:
            obj1.cpu_settle(cpu_threshold=50, idle_min=50, dead_time=600, interval=500)
        except Exception as err:
            self.assertIsInstance(err, BBEDeviceError)
        obj1.router_handle.cli.side_effect = None



if __name__ == '__main__':
    unittest.main()