"""
Unit tests for schema_validation.py
author: Srinivas T
"""
import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.system.jvision.schema_validation import schema_validation


class TestSystem(unittest.TestCase):

    schema_val_obj = schema_validation()
    
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        self.sensor_data = {'/network-instances/network-instance/mpls':{'freq':10000,'gnmi_submode':2}}
        self.gnmi_data={'mode':0,'encoding':2, 'decoder_path':'/abc/d/ef', 'sub_mode': 2, 'encoding':2, 'freq':3000}

    @patch('jnpr.toby.system.jvision.schema_validation.Device')
    @patch("builtins.open", create_file=False)
    @patch('jnpr.toby.system.jvision.schema_validation.jinja2')
    def test_gen_and_upload_suite_proto(self, jinja_obj_patch, file_open_patch, dev_patch):
        jinja_obj_patch.render.return_value = "template"
        dev_patch.upload.return_value = True
        val = self.schema_val_obj.gen_and_upload_suite_proto(dut_port=1234, dut_ip='192.168.1.1', sensor_params=self.sensor_data, gnmi_params=self.gnmi_data, validation_type='path_validation')
        self.assertTrue(val)

    @patch('jnpr.toby.system.jvision.schema_validation.re')
    @patch('jnpr.toby.system.jvision.schema_validation.Device')
    def test_schema_validation(self, dev_obj_patch, re_patch):
        dev_obj_patch.shell.response = MagicMock()
        dev_obj_patch.shell.response.return_value="True"
        re_patch.search.return_value = "SUCCESS"
        val = self.schema_val_obj.schema_validation(suite_file='abc', output_file='def', gnmi_server_handle=dev_obj_patch, decoder_path='/abc/')
        self.assertTrue(val)   
        
    def test_get_jinja_template(self):
        self.schema_val_obj.val_type = "path_validation"
        val = self.schema_val_obj._get_jinja_template()
        self.assertTrue(val)
        self.schema_val_obj.val_type = "datatype_validation"
        val = self.schema_val_obj._get_jinja_template()
        self.assertTrue(val)

    @patch('jnpr.toby.system.jvision.schema_validation.re')
    @patch('jnpr.toby.system.jvision.schema_validation.Device')
    @patch("builtins.open", create_file=False)
    @patch('jnpr.toby.system.jvision.schema_validation.jinja2')
    def test_build_schema_modules(self, jinja_obj_patch, file_open_patch, dev_obj_patch, re_patch):
        jinja_obj_patch.render.return_value = "template"
        dev_obj_patch.upload.return_value = True
        dev_obj_patch.shell.response = MagicMock()
        dev_obj_patch.shell.response.return_value="True"
        re_patch.search.return_value = False
        pkg_path='/homes/junos-openconfig-yang-19.4I-20191202.0.0031.tgz'
        schema_path='/usr/local/go/src/github.com/openconfig/gnmitest/schemas/openconfig'
        val = self.schema_val_obj.build_schema_modules(pkg_path=pkg_path, schema_path=schema_path, gnmi_server_handle=dev_obj_patch, gnmi_server_name='gnmi_server_name')
        self.assertTrue(val)
        
        
if __name__ == '__main__' :
    unittest.main()
