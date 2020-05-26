import builtins
from robot.libraries.BuiltIn import BuiltIn
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.utils.response import Response

from jnpr.toby.jdm.phone_home import phone_home

import unittest
import builtins
import requests
from mock import MagicMock
from mock import patch

class TestTime(unittest.TestCase):

    sample_json = b"{ \"state\" : \"Activation required\"}"
    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 200
    response.content = sample_json
    @patch('requests.get', return_value=response)
    def test_fetch_activation_state(self, patch_requests):

        dut_ip = "10.204.34.40"
        webscript = "activation_page.py"

        ph_obj = phone_home()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(ph_obj.fetch_activation_state(dut_ip, webscript), "Activation required")

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.post', return_value=response)
    def test_provision_device_on_phs(self, patch_requests):

        phs_ip = "10.204.38.161"
        device_serial_id = "ABCDXXXX1234"
        activation_code = "rightcode123"
        install_image = "jinstall-sample.tgz"
        auth_user = "admin"
        auth_password = "admin"

        ph_obj = phone_home()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(ph_obj.provision_device_on_phs(phs_ip, device_serial_id, activation_code, install_image, auth_user, auth_password), True)       

    response = MagicMock(spec=requests.models.Response, autospec=True)
    response.status_code = 201
    response.content = ""
    @patch('requests.get', return_value=response)
    def test_remove_device_from_phs_not_existing(self, patch_requests):

        phs_ip = "10.204.38.161"
        device_serial_id = "ABCDXXXX1234"

        ph_obj = phone_home()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(ph_obj.remove_device_from_phs(phs_ip, device_serial_id), True)

    response_get = MagicMock(spec=requests.models.Response, autospec=True)
    response_del = MagicMock(spec=requests.models.Response, autospec=True)
    response_get.status_code = 200
    response_del.status_code = 204
    response.content = ""
    @patch('requests.get', return_value=response_get)
    @patch('requests.delete', return_value=response_del)
    def test_remove_device_from_phs_existing(self, patch_get, patch_del):

        phs_ip = "10.204.38.161"
        device_serial_id = "ABCDXNONO1234"

        ph_obj = phone_home()
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

        self.assertEqual(ph_obj.remove_device_from_phs(phs_ip, device_serial_id), True)

if __name__ =='__main__':
    unittest.main()
