import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.radius.radiusconfig import *
from jnpr.toby.bbe.bbevar.bbevars import BBEVars
builtins.bbe = MagicMock(spec=BBEVars)
builtins.t = MagicMock(spec=init)
builtins.t.log = MagicMock()


class TestRadiusConfig(unittest.TestCase):
    """
    TestRadiusConfig class to handle radiusconfig.py unit tests
    """
    @patch('jnpr.toby.bbe.radius.radiusconfig.FreeRadius')
    def test_config_radius_server(self, patch_radius):
        builtins.bbe.get_devices.return_value = ['h0']
        obj1 = MagicMock()
        obj1.current_node.current_controller.name = 'hercules'
        builtins.t.get_handle.return_value = obj1

        builtins.bbe.bbevar = {'cos': {'configure-cos': True, 'static-cos': False},
                               'resources': {'h0': {'config': {'radius-secret': 'test'}}}}
        self.assertEqual(config_radius_server(), None)

    @patch('jnpr.toby.engines.config.config.config.CONFIG_SET')
    def test_config_dut_radius_links(self, patch_config):
        builtins.bbe.get_devices.return_value = ['r0']
        obj1 = MagicMock()
        obj1.interface_name = 'radius-0'
        builtins.bbe.get_interfaces.return_value = [obj1]
        self.assertEqual(config_dut_radius_links(), True)
        try:
            patch_config.side_effect = Exception
            config_dut_radius_links()
        except:
            self.assertRaises(BBEConfigError)
        try:
            patch_config.side_effect = [True, Exception]
            config_dut_radius_links()
        except:
            self.assertRaises(BBEConfigError)
        patch_config.side_effect = None

    def test_set_host_ntp_server(self):
        self.assertEqual(set_host_ntp_server(), True)

if __name__ == '__main__':
    unittest.main()
