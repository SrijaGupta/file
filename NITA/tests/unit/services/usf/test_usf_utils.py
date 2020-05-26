"""Enable USF Unit Test """
import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.services.usf.usf_utils import ensure_usf_mode
builtins.t = MagicMock()


class Testusfenable(unittest.TestCase):
    """Testusfenable to handld usf.py unit tests"""
    def setUp(self):
        self.response = {}
        self.response["USF_OUTPUT_DISABLED"] = """ <rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
    <unified-services-status-information>
        <unified-services-status>Unified Services : Disabled</unified-services-status>
    </unified-services-status-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
        self.response["USF_OUTPUT_ENABLED"] = """ <rpc-reply xmlns:junos="http://xml.juniper.net/junos/18.3D0/junos">
    <unified-services-status-information>
        <unified-services-status>Unified Services : Enabled</unified-services-status>
    </unified-services-status-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
"""
    @patch('jnpr.toby.hldcl.device.Device')
    def test_usf_on_list(self, mock_cli):
        """ Function to test passing Device handle as list"""
        mock_cli = MagicMock()
        mock_cli.response = MagicMock()
        dobject = MagicMock()
        dobject.cli = MagicMock(return_value=True)
        dobject.cli.return_value = mock_cli
        mock_cli.response.side_effect = (self.response["USF_OUTPUT_DISABLED"], "", "", self.response["USF_OUTPUT_ENABLED"])
        result = ensure_usf_mode(device_handle=[dobject])
        self.assertTrue(result, True)
    def test_usf_one_device(self):
        """ Function to test passing Device handle as tuple"""
        mock_cli = MagicMock()
        mock_cli.response = MagicMock()
        mock_cli.response.side_effect = (self.response["USF_OUTPUT_DISABLED"], "", "", self.response["USF_OUTPUT_ENABLED"])
        dobject = MagicMock()
        dobject.cli = MagicMock(return_value=True)
        dobject.cli.return_value = mock_cli
        self.assertTrue(ensure_usf_mode(dobject), True)
    def test_usf_exception_device(self):
        """ Function to test Exception after restart"""
        mock_cli = MagicMock()
        mock_cli.response = MagicMock()
        mock_cli.response.side_effect = (self.response["USF_OUTPUT_DISABLED"], "", "", self.response["USF_OUTPUT_DISABLED"])

        dobject = MagicMock()
        dobject.cli = MagicMock()
        dobject.cli.return_value = mock_cli
        with self.assertRaises(Exception) as context:
            ensure_usf_mode(dobject)
            self.assertTrue("USF is still not enabled" in str(context.exception))
    def test_usf_already_enabled(self):
        """ Function to test if USF is already enabled"""
        mock_cli = MagicMock()
        mock_cli.response = MagicMock()
        mock_cli.response.side_effect = (self.response["USF_OUTPUT_ENABLED"], "", "", self.response["USF_OUTPUT_ENABLED"])
        dobject = MagicMock()
        dobject.cli = MagicMock(return_value=True)
        dobject.cli.return_value = mock_cli
        self.assertTrue(ensure_usf_mode(dobject), True)



if __name__ == '__main__':
    unittest.main()
