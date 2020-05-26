#!/usr/bin/env python
# coding=utf-8
"""
 Copyright (C) 2015-2016, Juniper Networks, Inc.
 All rights reserved.
 Author: Omkar Gojala

 Description: Test suite for VE template utils.
"""
import sys
import unittest
from mock import patch, MagicMock
from jnpr.toby.engines.verification.ve_template_utils import *
#from ve_template_utils import *
import builtins
from lxml import etree
import pprint

class MockDevice():
    """A mock device to temporarily suppress output to stdout
    Similar to UNIX /dev/null.
    """

    def write(self, s): pass

verify_template_path = "tests/unit/engines/verification/ve_templates"
verify_template_file = "tests/unit/engines/verification/ve_templates/chassis_template.yaml"
chassis1_xml = "tests/unit/engines/verification/chassis1.xml"

class TestVerifyEngineTemplates(unittest.TestCase):
    def setUp(self):
        builtins.t = self

    def test_file_to_string(self):
        result = file_to_string(chassis1_xml)
        self.assertEqual(type(result), str)
        result = file_to_string("template.yaml")
        self.assertEqual(result, "VERIFY_TEMPLATE: ")

    def test_get_existing_templates(self):
        result = False
        template = verify_template_path
        template_name = 'check_chassis_fpc'
        template_data = get_existing_templates(template)
        for key, value in template_data.items():
            if key == template_name:
                result = True
        self.assertTrue(result) 

    def test_find_equivalant_template(self):
        template_name = "chassis_template"
        templates = {'template_chassis': '1'}
        with patch('sys.stdout', new=MockDevice()) as std_out_patch:
            result = find_equivalent_template(template_name, templates)
            self.assertEqual(result, 'template_chassis')

    def test_write_template_file(self):
        template = verify_template_file
        template_name = 'check_chassis_fpc'
        template_data = get_existing_templates(template)
        with patch('sys.stdout', new=MockDevice()) as std_out_patch:
            if template_data:
                result = write_template_file(template_data)
                self.assertTrue(result)
                result = write_template_file(template_data, './template_data.yaml')
                self.assertEqual(result, None)
                result = os.path.exists('./template_data.yaml')
                self.assertTrue(result)
                if result == True:
                    os.remove('./template_data.yaml')

    def test_get_template_name_from_show_cmd(self):
        show_cmd = "show ospf interface"
        result = get_template_name_from_show_cmd(show_cmd)
        self.assertEqual(result, "j_check_ospf_interface")

    def test_get_template_directory_name_from_show_cmd(self):
        show_cmd = "show ospf interface"
        template_path = verify_template_path
        result = get_template_directory_name_from_show_cmd(template_path, show_cmd)
        self.assertEqual(result, verify_template_path+"/ospf/")

    def test_read_xml_file(self):
        xml_file = chassis1_xml
        result = read_xml_file(xml_file)
        ElementTree =  type(etree.Element("child1"))
        self.assertEqual(type(result), ElementTree)

    def test_find_unique_parameter_name(self):
        template = verify_template_path
        template_name = 'check_chassis_fpc'
        template_data = get_existing_templates(template)
        template_data = template_data['check_chassis_fpc']

        xpath = '/multi-routing-engine-results/multi-routing-engine-item/fpc-information/fpc/slot'
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(template_data)
        result = find_unique_parameter_name(template_data, xpath)
        self.assertEqual(result, 'fpc/slot')

    def test_find_equivalent_template(self):
        template_name = 'j_check_ospf_interface'
        templates = ['j_check_ospf_interface', 'j_check1', 'j_check2']
        with patch('sys.stdout', new=MockDevice()) as std_out_patch:
            result = find_equivalent_template(template_name, templates)
            self.assertEqual(result, 'j_check_ospf_interface')
            template_name = 'j_ospf_check_interface'
            result = find_equivalent_template(template_name, templates)
            self.assertEqual(result, 'j_check_ospf_interface')

    def test_find_parameter_xpath(self):
        old_xpath = '/ospf-interface/interface-address/hello-interval'
        new_xpath = '/ospf-interface/interface-address/logical-address/hello-interval'
        result = find_parameter_xpath(old_xpath, new_xpath)
        self.assertFalse(result)
        old_xpath = '/ospf-interface/interface-address/hello-interval'
        new_xpath = '/ospf-interface/interface-address/hello-interval'
        result = find_parameter_xpath(old_xpath, new_xpath)
        self.assertEqual(result['xpath'], 'interface-address/hello-interval')

    def test_add_a_parameter(self):
        template = verify_template_path
        template_name = 'check_chassis_fpc'
        template_data = get_existing_templates(template)
        template_data = template_data['check_chassis_fpc']
        new_xpath = "/multi-routing-engine-results/multi-routing-engine-item/fpc-information/fpc/cpu-timeout"

        result = add_a_parameter(template_data, new_xpath)

    def test_update_template(self):
        xml_file = verify_template_file
        show_cmd = "show chassis fpc"
        with patch('sys.stdout', new=MockDevice()) as std_out_patch:
            with self.assertRaises(SystemExit) as ex:
                update_template(xml_file, show_cmd)
            self.assertEqual(ex.exception.code, None)
            xml_file = "tests/unit/engines/verification/mxvc_show_chassis_fpc.xml"
            result = update_template(xml_file, show_cmd)
            boolean = isinstance(result, tuple)
            self.assertTrue(boolean)

    def test_get_list_of_show_cmds(self):
        command = 'show ospf interface'
        result = get_list_of_show_cmds(command)
        self.assertEqual(result[0], 'show ospf ?')
        command = 'show ospf interface x'
        result = get_list_of_show_cmds(command)
        self.assertEqual(result[1], 'show ospf interface ?')

    #def test_get_bulk_input(self):

if __name__ == '__main__':
    unittest.main()
