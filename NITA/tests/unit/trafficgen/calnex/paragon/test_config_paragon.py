import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
import jnpr.toby.trafficgen.calnex.paragon.config_paragon as tester


class TestConfigParagon(unittest.TestCase):
    """
    TestConfigParagon class to handle config_paragon.py unit tests
    """
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.log = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        self.rthandle = MagicMock()
       
    def test_configure_operating_mode(self):
        test_args = {'a':1}
        tester.configure_operating_mode(self.rthandle, **test_args)
    def test_setup_port1_as_rj45_port2_as_rj45(self):
        test_args = {}
        tester.setup_port1_as_rj45_port2_as_rj45(self.rthandle, **test_args)
    def test_setup_port1_as_sfp_port2_as_sfp(self):
        test_args = {}
        tester.setup_port1_as_sfp_port2_as_sfp(self.rthandle, **test_args)
    def test_setup_port1_as_sfpp_port2_as_sfpp(self):
        test_args = {}
        tester.setup_port1_as_sfpp_port2_as_sfpp(self.rthandle, **test_args)
    def test_setup_port1_as_xfp_port2_as_xfp(self):
        test_args = {}
        tester.setup_port1_as_xfp_port2_as_xfp(self.rthandle, **test_args)
    def test_configure_boundary_clock_ipv4(self):
        test_args = {}
        tester.configure_boundary_clock_ipv4(self.rthandle, **test_args)
    def test_configure_boundary_clock_ipv4_g82751_enh(self):
        test_args = {}
        tester.configure_boundary_clock_ipv4_g82751_enh(self.rthandle, **test_args)
    def test_configure_boundary_clock_ethernet(self):
        test_args = {}
        tester.configure_boundary_clock_ethernet(self.rthandle, **test_args)
    def test_configure_capture(self):
        test_args = {}
        tester.configure_capture(self.rthandle, **test_args)
    def test_paragon_disconnect(self):
        test_args = {}
        tester.paragon_disconnect(self.rthandle, **test_args)
    def test_paragon_performance_measurements(self):
        test_args = {}
        tester.paragon_performance_measurements(self.rthandle, **test_args)
    def test_paragon_start_esmc_generation_port1(self):
        test_args = {}
        tester.paragon_start_esmc_generation_port1(self.rthandle, **test_args)
    def test_paragon_stop_esmc_generation_port1(self):
        test_args = {}
        tester.paragon_stop_esmc_generation_port1(self.rthandle, **test_args)
    def test_paragon_stop_master_slave_emulation(self):
        test_args = {}
        tester.paragon_stop_master_slave_emulation(self.rthandle, **test_args)
    def test_detect_1pps(self):
        test_args = {}
        tester.detect_1pps(self.rthandle, **test_args)
    def test_paragon_start_timing_capture(self):
        test_args = {}
        tester.paragon_start_timing_capture(self.rthandle, **test_args)
    def test_paragon_stop_timing_capture(self):
        test_args = {}
        tester.paragon_stop_timing_capture(self.rthandle, **test_args)
    def test_paragon_set_packet_measurements(self):
        test_args = {}
        tester.paragon_set_packet_measurements(self.rthandle, **test_args)
    def test_set_packet_measurements_ethernet(self):
        test_args = {}
        tester.paragon_set_packet_measurements_ethernet(self.rthandle, **test_args)
    def test_get_packet_measurements(self):
        test_args = {}
        tester.paragon_get_packet_measurements(self.rthandle, **test_args)
    def test_paragon_export_multiple(self):
        test_args = {}
        tester.paragon_export_multiple(self.rthandle, **test_args)
    def test_history_1pps(self):
        test_args = {}
        tester.history_1pps(self.rthandle, **test_args)
    def test_paragon_get_1pps_measurements(self):
        test_args = {}
        tester.paragon_get_1pps_measurements(self.rthandle, **test_args)
    def test_paragon_get_synce_measurements(self):
        test_args = {}
        tester.paragon_get_synce_measurements(self.rthandle, **test_args)
    def test_paragon_get_1pps_measurements1(self):
        test_args = {}
        tester.paragon_get_1pps_measurements1(self.rthandle, **test_args)

if __name__ == '__main__':
    #SUITE = unittest.TestLoader().loadTestsFromTestCase(TestIxiaTester)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)
    unittest.main()
