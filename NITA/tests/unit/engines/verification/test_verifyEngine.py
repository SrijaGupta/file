import os
import sys
import unittest
import datetime
import mock
import time
from mock import patch, MagicMock
import builtins
from jnpr.toby.engines.verification.verifyEngine import verifyEngine
import jnpr.toby.engines.verification.verify_utils
from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem
from jnpr.toby.init.init import init
from lxml import etree

# pylint: disable= unused-argument
# pylint: disable= protected-access
# pylint: disable= missing-docstring
# pylint: disable= singleton-comparison

ve = verifyEngine()
verify_yaml_file = "tests/unit/engines/verification/verify_ut.yaml"
jvision_1 = "tests/unit/engines/verification/jvision_1.json"
jvision_2 = "tests/unit/engines/verification/jvision_2.json"
jvision_demo_ifd_2 = "tests/unit/engines/verification/jvision_demo_ifd_2.json"
jvision = "tests/unit/engines/verification/jvision.json"
maping = "tests/unit/engines/verification/maping.yaml"
maping1 = "tests/unit/engines/verification/maping1.yaml"
maping2 = "tests/unit/engines/verification/maping2.yaml"
verify_jvision = "tests/unit/engines/verification/verify_jvision.yaml"
verify_jvision_new = "tests/unit/engines/verification/verify_jvision_new.yaml"
verify_jvision_new_1 = "tests/unit/engines/verification/verify_jvision_new_1.yaml"
verify_utils_ut = "tests/unit/engines/verification/verify_utils_ut.yaml"
test_1 = "tests/unit/engines/verification/test_1.yaml"
test_2 = "test_2.yaml"

class TestVerifyEngine(unittest.TestCase):
    def setUp(self):
        builtins.t = self
        builtins.t.log = MagicMock()
        t = MagicMock(spec=init)
        t.t_dict = MagicMock(return_value={"resources": {'r0': {}, 'device0': {}}})

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._pre_process_testcases", \
            return_value={'result':True, 'args':[{'arg1':1}, {'arg2':'2'}]})
    def test_initialize_verify_engine(self, patch_pre_process):
        result = verifyEngine.initialize_verify_engine(ve)
        self.assertEqual(result, False)

        try:
            result = verifyEngine.initialize_verify_engine(ve, is_robot=True)
        except Exception as exp:
            self.assertEqual(exp.args[0], "File argument is missing to Initialize Verify Engine")
        # mmohan
        result = verifyEngine.initialize_verify_engine(ve, file=verify_yaml_file)
        self.assertEqual(result, True)
        #mmohan
        patch_pre_process.return_value = {'result':False}
        try:
            result = verifyEngine.initialize_verify_engine(ve, file=verify_yaml_file, is_robot=True)
        except Exception as exp:
            self.assertEqual(exp.args[0], "In Initialize Verify Engine, Unable to pre-process the file : "+verify_yaml_file)

        result = verifyEngine.initialize_verify_engine(ve, file=verify_yaml_file)
        self.assertEqual(result, False)

    @patch("jnpr.toby.engines.verification.verify_utils.expand_alpha_numeric_string", return_value=['dh1'])
    @patch("jnpr.toby.engines.verification.verify_utils.get_devices", return_value=False)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._search_template", return_value={'value':'123'})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._form_device_specific_testcase", return_value={'sk':'great'})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._merge_template_data", return_value={})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._make_ifd_tvar", return_value=None)
    @patch("jnpr.toby.engines.verification.verify_utils._replace_value", return_value=None)
    @patch("jnpr.toby.engines.verification.verify_utils.get_key_value", return_value={'args':'hello','val':{'template':{'abc':'def'}}})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._source_templates", return_value=True)
    @patch("jnpr.toby.engines.verification.verify_utils.get_yaml_data_as_dict", return_value=False)
    def test_pre_process_testcases(self, patch_verify, patch_source, patch_get, patch_replace, patch_make, patch_merge, patch_form,patch_search,\
    patch_devices, patch_expand):
        builtins.t = self
        t.t_dict = {'resources':{'device0':{'interface':['ge0.1']}, 'device2':{'interface':['ge0.1']}}}

        result = verifyEngine._pre_process_testcases(ve, file_to_process=verify_yaml_file)
        self.assertFalse(result['result'])

        patch_verify.return_value = {}
        result = verifyEngine._pre_process_testcases(ve, file_to_process=verify_yaml_file)
        self.assertEqual(result, {'data': ['sk'], 'result': True, 'args': 'hello'})

        patch_expand.return_value = []
        patch_get.return_value = {'args':'hello', 'devices':{'val':{'template':{'abc':'def'}}}}
        result = verifyEngine._pre_process_testcases(ve, file_to_process=verify_yaml_file)
        self.assertEqual(result, {'data': ['sk'], 'result': True, 'args': 'hello'})

        with patch("jnpr.toby.engines.verification.verify_utils.get_devices", return_value=True):
            patch_expand.return_value = []
            patch_get.return_value = {'args':'hello', 'devices_<vhjd>':{'val':{'template':{'abc':'def'}}}}
            result = verifyEngine._pre_process_testcases(ve, file_to_process=verify_yaml_file)
            self.assertEqual(result, {'data': ['sk'], 'result': True, 'args': 'hello'})

    def test_generate_dataset(self):
#        ve._extract_value_from_path = MagicMock(return_value=True)
        tc_data = {'iterator':{'loop(args:intf)'}, \
                   'args': [{'intf':[1, 2, 3]}], \
                   'xpath':'/ospf-interface-information/ospf-interface', \
                   'parameters': {'hello-interval': {'value': 1}}, \
                   'cmd':"show ospf interface var['intf'] detail", \
                   'type':'get'}
        iterator = {'loop(args:intf)': 'xyz'}
        # iterator = tc_data['iterator']
        height = 2
        expanded_tc_datas = []
        result = verifyEngine._generate_dataset(ve, iterator, height, [], [], tc_data, expanded_tc_datas)
        self.assertEqual(result, None)

        tc_data = {'iterator':{'loop(args:intf)'}, \
                   'args': [{'intf':[1, 2, 3]}], \
                   'xpath':'/ospf-interface-information/ospf-interface', \
                   'parameters': {'hello-interval': {'value': 1}}, \
                   'cmd':"show ospf interface var['intf'] detail", \
                   'type':'get'}
        #iterator = {'loop(args:intf)': 'xyz'}
        iterator = 'loop(args:intf)'
        # iterator = tc_data['iterator']
        height = 0
        expanded_tc_datas = []
        result = verifyEngine._generate_dataset(ve, iterator, height, [], [], tc_data, expanded_tc_datas)
        self.assertEqual(result, None)

    def test_verify_parameters(self):
        element_data = {'value': 1, 'operator': 'is-equal'}
        element_data_keys = ['operator', 'value']
        tag = 'timeout'

        xpath_result = '2'
        result = verifyEngine._verify_parameters(ve, xpath_result, element_data, element_data_keys, \
                                                 tag, return_result=True)
        self.assertFalse(result)

        xpath_result = '1'
        result = verifyEngine._verify_parameters(ve, xpath_result, element_data, element_data_keys, \
                                                 tag, return_result=True)
        self.assertTrue(result)

        result = verifyEngine._verify_parameters(ve, xpath_result, element_data, element_data_keys, \
                                                 tag, is_ex_get=True, is_get=True, return_type='bool', \
                                                 return_result=dict())
        self.assertEqual(result['timeout'], 1)

        result = verifyEngine._verify_parameters(ve, xpath_result, element_data, element_data_keys, \
                                                 tag, is_ex_get=True, is_get=True, return_type='bol', \
                                                 return_result=dict())
        self.assertEqual(result['timeout'], 1)

        element_data_keys = []
        result = verifyEngine._verify_parameters(ve, xpath_result, element_data, element_data_keys, \
                                                 tag, return_result=True)
        self.assertTrue(result)

        result = verifyEngine._verify_parameters(ve, xpath_result, element_data, element_data_keys, \
                                                 tag, is_ex_get=True, is_get=True, return_type='blah', \
                                                 return_result=dict())
        self.assertEqual(result['timeout'], 1)

        with patch('jnpr.toby.engines.verification.verify_utils.get_xpath_result', return_value='1'):
            element_data = {'timeout': {'value': 1, 'operator': 'is-equal'}}
            xpath_result = 'timeout/1'
            element_data_keys = ['timeout']
            result = verifyEngine._verify_parameters(ve, xpath_result, element_data, element_data_keys, \
                                                 tag, return_result=True)
        self.assertTrue(result)

    def test_expand_modifiers(self):
        data = {'xpath': '/ospf-interface-information/ospf-interface', 'args': [{'intf': 'ae1.15'}]}
        verifyEngine._expand_modifiers(ve, data=data)

        data = {'xpath': '/ospf-interface-information/ospf-interface', 'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail"}
        verifyEngine._expand_modifiers(ve, data=data)

        with patch("jnpr.toby.engines.verification.verifyEngine.config_utils.expand_to_list", return_value=True):
            data = {'xpath': '/ospf-interface-information/ospf-interface', 'args': [{'intf': 'ae1.15'}],\
            'cmd': "<<show ospf interface var['intf'] detail>>"}
            verifyEngine._expand_modifiers(ve, data=data)


    def test_get_iterator_height(self):
        data = {'a':{'c':'d'}, 'b':{'x':{'y':{'z':1}}}}
        result = verifyEngine._get_iterator_height(ve, tc_data=data)

    def test_expand_file_list(self):
        files = ['a', '/c']
        with patch("jnpr.toby.engines.verification.verifyEngine.fnmatch.filter", return_value=['c']):
            result = verifyEngine._expand_file_list(ve, file_list=files)

    def test_put_sub_tc_result_msg(self):
        verifyEngine._put_sub_tc_result_msg(ve, tc_name='TC1', tc_data={'failmsg':"Fail"}, result=False)
        verifyEngine._put_sub_tc_result_msg(ve, tc_name='TC1', tc_data={}, result=False)
        verifyEngine._put_sub_tc_result_msg(ve, tc_name='TC1', tc_data={}, result=True)
        verifyEngine._put_sub_tc_result_msg(ve, tc_name='TC1', tc_data={'passmsg':"Pass"}, result=True)


    def test_put_tc_result_msg(self):
        verifyEngine._put_tc_result_msg(ve, tc_name='TC1', tc_data={'failmsg':"Fail"}, device_name='device1', result=False)
        verifyEngine._put_tc_result_msg(ve, tc_name='TC1', tc_data={}, device_name='device1', result=False)
        verifyEngine._put_tc_result_msg(ve, tc_name='TC1', tc_data={}, device_name='device1', result=True)
        verifyEngine._put_tc_result_msg(ve, tc_name='TC1', tc_data={'passmsg':"Pass"}, device_name='device1', result=True)

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._process_testcase", side_effect=[False, {'result':'value'}])
    def test_execute_testcase(self, patch_process_tc):
        ve._device_handle = MagicMock()
        result = verifyEngine._execute_testcase(ve, data=[{'device0':{}}, {'dh[0]':{}}], pre_res_data={}, is_testcase_executed=False,\
        return_result=True, device_list=[], is_get=False)
        self.assertEqual(result, (False, False))

        ve.is_VE_offline = True
        data = [{'device0':{'tc1':{'tag':['TAG1']}}}, {'dh[0]':{'tc2':{}}}]
        result = verifyEngine._execute_testcase(ve, data=data, pre_res_data={}, is_testcase_executed=False, return_result=True, device_list=[],\
        is_get=False, each_tag='tag1')
        self.assertEqual(result, (True, False))

        data = [{'dh[0]':{'tc2':{'tag':['TAG1']}}}]
        result = verifyEngine._execute_testcase(ve, data=data, pre_res_data={}, is_testcase_executed=False, return_result=True,\
        device_list=[], is_get=True)
        self.assertEqual(result, (True, True))

    #omkar
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._execute_testcase", return_value=[True, True])
    def test_execute_testcase_parallel(self, patch_exec_tc):
        data = [{'device0':{}}, {'device1':{}}]
        patch_exec_tc.return_result = [True, True]
        result = verifyEngine._execute_testcase_parallel(ve, data=data, pre_res_data={}, is_testcase_executed=False, device_list=[],\
        is_get=False)
        self.assertEqual(result, (False, False))

    @patch("builtins.open", create_file=False)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._pre_process_testcases", return_value={'result':'value', 'args':['a1']})
    @patch("jnpr.toby.engines.verification.verify_utils.extract_data", return_value="sample_result")
    def test_verify_all_checks_api(self, patch_extract_data, patch_pre_process, patch_open):
        builtins.t = self
        t.is_robot = True
        t.t_dict = {'resources':{}}

        verification_file = ve.verification_file
        ve.verification_file = None
        result = verifyEngine.verify_all_checks_api(ve, type='get', args={'args':[]})
        self.assertEqual(result, False)
        ve.verification_file = verification_file

        result = verifyEngine.verify_all_checks_api(ve, type='get', args={'args':[]})
        self.assertEqual(result, {})

        result = verifyEngine.verify_all_checks_api(ve, file=verify_yaml_file, type='get', args={'args':[]})
        self.assertEqual(result, {})

        result = verifyEngine.verify_all_checks_api(ve, file=verify_yaml_file, type='get', args={'arg1':'val1', 'arg2':'val2'}, is_robot=True)
        self.assertEqual(result, {})

        try:
            result = verifyEngine.verify_all_checks_api(ve, data="{'device0':{}}", devices='device0', tag='tag1', is_robot=True)
            self.assertEqual(result, True) #omkar
        except Exception as exp:
            self.assertEqual(exp[0], "+ VERIFY FAILED: ['device0'] specific checks in None file")

        patch_pre_process.return_value = {'result':False}
        result = verifyEngine.verify_all_checks_api(ve, file=verify_yaml_file, type='get', args={'args':[]})
        self.assertEqual(result, False)

        result = verifyEngine.verify_all_checks_api(ve, data="{'device0':{}}", type='get', args=['a', 'b'])
        self.assertEqual(result, False)

        result = verifyEngine.verify_all_checks_api(ve, type='get', args=['a', 'b'])
        self.assertEqual(result, {})

        ve.verification_file = None
        result = verifyEngine.verify_all_checks_api(ve)
        self.assertEqual(result, False)

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_all_checks_api", return_value=True)
    @patch("builtins.open", create_file=False)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._pre_process_testcases", return_value={'result':'value', 'args':['a1']})
    @patch("jnpr.toby.engines.verification.verify_utils.get_yaml_data_as_dict", return_value={})
    def test_verify_statement_checks(self, patch_verify_utils, patch_pre_process, patch_open, patch_all_checks):
        stanza = "hello-interval is-equal 30 and interface-type is-equal LAN"
        template = "ospf_interface_check"
        device = "device0"

        result = verifyEngine.verify_statement_checks(ve, stanzas=stanza, template=template, devices=device)
        self.assertFalse(result)

        self.assertRaises(Exception, verifyEngine.verify_statement_checks, ve, stanzas=stanza, \
                          is_robot=True, template=template, devices=device)

        ve.verification_file = "testFile.yaml"
        result = verifyEngine.verify_statement_checks(ve, stanzas=stanza, template=template, devices=device)
        self.assertFalse(result)

        value = {'ospf_interface_check': {'cmd': "show ospf interface var['intf'] detail",\
                 'xpath': '/ospf-interface-information/ospf-interface',\
                 'parameters': {'ospf-interface-topology': {'ospf-topology-metric': {\
                 'value': 1, 'operator': 'is-equal'}}, 'interface-type': {'value': 'LAN',\
                 'operator': 'is-equal'}, 'hello-interval': {'value': 30, 'operator': \
                 'is-equal'}}, 'args': [{'intf': 'ae1.15'}]}}

        with patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._search_template", return_value=value):
            verify_file = "verifyFile.yaml"
            result = verifyEngine.verify_statement_checks(ve, stanzas=stanza, template=template, devices=device, file=verify_file)
            self.assertTrue(result)

            stanza = "hello-interval is-equal 20 and interface-type is-equal LAN on intf as ae1.11"
            result = verifyEngine.verify_statement_checks(ve, stanzas=stanza, template=template, devices=device, file=verify_file)
            self.assertTrue(result)

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._merge_template_data", return_value={'dsd':'dds'})
    @patch("builtins.open", create_file=False)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._pre_process_testcases", return_value={'result':'value', 'args':['a1']})
    @patch("jnpr.toby.engines.verification.verify_utils.extract_data", return_value="sample_result")
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_all_checks_api", return_value=True)
    @patch("jnpr.toby.engines.verification.verify_utils.get_yaml_data_as_dict", return_value={'verify':{}})
    def test_verify_specific_checks_api(self, patch_verify_utils, patch_all_checks, patch_extract_data, patch_pre_process, patch_open,\
    patch_merge_template):
        builtins.t = self
        t.t_dict = {'resources':{'device0':{'interface':['ge0.1']}, 'device2':{'interface':['ge0.1']}}}

        ve.is_VE_offline = True
        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check_3']", devices='device0', args={'args':[]})
        self.assertEqual(result, False)

        val = ve.t_handle
        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check_3']", devices='device0',\
        args={'args':[]}, offline_data="dsv")
        self.assertEqual(result, False)
        ve.t_handle = val

        ve.is_VE_offline = False

        ve.verification_file = None
        result = verifyEngine.verify_specific_checks_api(ve, optimize=True, checks="template['ospf_interface_check']", devices='device0',\
        args={'args':[]}, file=verify_yaml_file)
        self.assertEqual(result, True)

        ve.verification_file = None
        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'args':[]})
        self.assertEqual(result, False)

        ve.verification_file = verify_yaml_file
        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'args':[]},\
        optimize="true")
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'arg1':'val1',\
        'arg2':'val2'}, file=verify_yaml_file)
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args=['arg1:val1',\
        'arg2:val2'], file=verify_yaml_file)
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, devices='device0', args={'args':[]}, file=verify_yaml_file)
        self.assertEqual(result, False)

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", args={'args':[]}, file=verify_yaml_file)
        self.assertEqual(result, False)

        patch_pre_process.return_value = {'result':False}
        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'args':[]},\
        file=verify_yaml_file)
        self.assertEqual(result, False)
        patch_pre_process.return_value = {'result':'value', 'args':['a1']}

        patch_verify_utils.return_value = {'verify_tmpl':{}}
        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'args':[]},\
        file=verify_yaml_file)
        self.assertEqual(result, True)
        patch_verify_utils.return_value = {'verify':{}}

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'args':[]},\
        data="adfdfssssss")
        self.assertEqual(result, True)

        patch_pre_process.return_value = {'result':False}
        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'args':[]},\
        data="adfdfssssss")
        self.assertEqual(result, False)
        patch_pre_process.return_value = {'result':'value', 'args':['a1']}

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']:parameters:[hello-interval, interface-type]",\
        devices='device0', args={'args':[]}, file=verify_yaml_file)
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0', args={'args':[]},\
        file=verify_yaml_file, verify_parallel=True)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", devices='device0',\
        args="args:arg1 as val1 and vars:arg2 as val2 and arg3 as val3 ", file=verify_yaml_file)
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']", device_handle="dh[0]",\
        args="args:arg1 as val1 and vars:arg2 as val2 and arg3 as val3 ", file=verify_yaml_file)
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, is_robot=True, checks="template['ospf_interface_check']", devices='device0',\
        args="args:arg1 as val1 and vars:arg2 as val2 and arg3 as val3 ", file=verify_yaml_file)
        self.assertEqual(result, True)

        patch_all_checks.return_value = False
        self.assertRaises(Exception, verifyEngine.verify_specific_checks_api, ve, is_robot=True, checks="template['ospf_interface_check']",\
        devices='device0', args="args:arg1 as val1 and vars:arg2 as val2 and arg3 as val3 ", file=verify_yaml_file)
        patch_all_checks.return_value = True

        with patch('jnpr.toby.engines.verification.verifyEngine.verifyEngine._search_and_retrieve_tc_data', return_value=({'data': 'value'},\
        {'data': 'value'}, 'a/b/c')):
            result = verifyEngine.verify_specific_checks_api(ve, checks="template['ospf_interface_check']:parameters:hello-interval",\
            devices='device0', args={'args':[]}, file=verify_yaml_file, params_dict={'parameter':{}})
            self.assertEqual(result, True)

        patch_pre_process.return_value = {'data':[{'device0':{'temp':{'parameters':{'hello-interval':{'value':'20'}}}}}],\
        'result':'value', 'args':['a1']}
        patch_verify_utils.return_value = {'verify':{'device0':{'temp':{'parameters':{'hello-interval':{'value':'20'}}}}}}
        result = verifyEngine.verify_specific_checks_api(ve, checks="temp:parameters:hello-interval:timeout", devices='device0',\
        args={'args':[]}, file=verify_yaml_file, params_dict={'timeout':{'value':'30'}})
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="temp:parameters:hello-interval:timeout", devices='device0',\
        args={'args':[]}, file=verify_yaml_file)
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="temp:parameters:hello-interval:timeout", devices='device0',\
        args={'args':[]}, file=verify_yaml_file, params_dict={'time':{'value':'30'}})
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="temp:parameters:hello-interval:inf:timeout", devices='device0',\
        args={'args':[]}, file=verify_yaml_file, params_dict={'timeout':{'value':'30'}})
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="temp:parameters:hello-interval:inf:timeout", devices='device0',\
        args={'args':[]}, file=verify_yaml_file)
        self.assertEqual(result, True)

        result = verifyEngine.verify_specific_checks_api(ve, checks="temp:parameters:hello-interval:inf:timeout", devices='device0',\
        args={'args':[]}, file=verify_yaml_file, params_dict={'time':{'value':'30'}})
        self.assertEqual(result, True)

        patch_pre_process.return_value = {'result':'value', 'args':['a1']}
        patch_verify_utils.return_value = {'verify':{}}

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._substitute_variables", return_value=None)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._specific_jvision_records_fetcher", return_value={'abc':'20'})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._evaluate", return_value=True)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._put_verify_log", return_value=None)
    def test_verify_jvision_records_api(self, patch_put, patch_evaluate, patch_specific, patch_substitute):

        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new)
        self.assertEqual(result, True)

        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new, key_specific=False)
        self.assertEqual(result, True)

        result = verifyEngine.verify_jvision_records_api(ve, verify_file=verify_jvision_new, key_specific=False)
        self.assertEqual(result, False)

        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, key_specific=False)
        self.assertEqual(result, False)

        data = '[{"jkey":"abc", "jvalue":"20"}]'
        result = verifyEngine.verify_jvision_records_api(ve, verify_file=verify_jvision_new, jvision_data=data)
        self.assertEqual(result, True)

        data = '{}{}'
        self.assertRaises(ValueError, verifyEngine.verify_jvision_records_api, ve, verify_file=verify_jvision_new, jvision_data=data)


        self.assertRaises(ValueError, verifyEngine.verify_jvision_records_api, ve, verify_file=verify_jvision_new, jvision_file=jvision_1)

        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new, args={'data':'value'})
        self.assertEqual(result, True)

        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new, args={'data':'value'})
        self.assertEqual(result, True)

        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new, args=[{'data':'value'}])
        self.assertEqual(result, True)

        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new, args={'args':[{'k1':'v1'},\
        {'k2':'v2'}]})
        self.assertEqual(result, True)

        patch_specific.return_value = {}
        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new_1)
        self.assertEqual(result, True)
        patch_specific.return_value = {'abc':'20'}

        patch_specific.return_value = {}
        result = verifyEngine.verify_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new)
        self.assertEqual(result, False)
        patch_specific.return_value = {'abc':'20'}

        result = verifyEngine.verify_jvision_records_api(ve, is_get=True, jvision_file=jvision, verify_file=verify_jvision_new)
        self.assertEqual(result, '2')

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_jvision_records_api", return_value=True)
    def test_verify_specific_jvision_records_api(self, patch_verify):

        result = verifyEngine.verify_specific_jvision_records_api(ve, verify_file=verify_jvision_new, operator="is-equal", value="15",\
        attribute="abc", records="all", checks="ospf_hello_interval")
        self.assertEqual(result, False)

        result = verifyEngine.verify_specific_jvision_records_api(ve, jvision_file=jvision, verify_file=verify_jvision_new,\
        operator="is-equal", value="15", attribute="abc", records="all")
        self.assertEqual(result, False)

        result = verifyEngine.verify_specific_jvision_records_api(ve, jvision_file=jvision, operator="is-equal", value="15",\
        attribute="abc", records="all", checks="ospf_hello_interval")
        self.assertEqual(result, False)

        result = verifyEngine.verify_specific_jvision_records_api(ve, jvision_file=jvision, operator="is-equal", value="15",\
        attribute="abc", records="all", checks="ospf_hello_interval, abcd", verify_file=verify_jvision_new)
        self.assertEqual(result, False)

    def test_specific_jvision_records_fetcher(self):
        jvision_records = [{'jkey':'abc', 'jvalue':'20', 'val':'31'}]
        verify_data = {'jkey':'abc', 'value':'20'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data, "val")
        self.assertEqual(result, {'abc':['31']})

        verify_data = {'jkey_pattern':'abc', 'value':'20'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data, "val")
        self.assertEqual(result, {'abc':['31']})

        verify_data = {'value':'20'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data, "val", True)
        self.assertEqual(result, {'abc':['31']})

        verify_data = {'value':'20'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data, "val")
        self.assertEqual(result, {})

        verify_data = {'jkey':'abc', 'value':'20'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data)
        self.assertEqual(result, [{'jkey': 'abc', 'val': '31', 'jvalue': '20'}])

        verify_data = {'jkey':'abc', 'value':'20', 'records':'0'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data, None, True)
        self.assertEqual(result, [{'jkey': 'abc', 'val': '31', 'jvalue': '20'}])

        verify_data = {'jkey':'abcd', 'value':'20', 'records':'0'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data, None, True)
        self.assertEqual(result, [])

        verify_data = {'key_pattern':'abcd', 'value':'20', 'records':'0'}
        result = verifyEngine._specific_jvision_records_fetcher(ve, jvision_records, verify_data, None, True)
        self.assertEqual(result, [])

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._get_logical_name", return_value="hello")
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_specific_checks_api", return_value=True)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._specific_jvision_records_fetcher", return_value={})
    def test_jvision_to_ve_converter(self, patch_specific, patch_verify, patch_get):
        result = verifyEngine.jvision_to_ve_converter(ve, jvision_1, verify_jvision)
        self.assertEqual(result, False)

        result = verifyEngine.jvision_to_ve_converter(ve, "jvi.json", verify_jvision)
        self.assertEqual(result, False)

        result = verifyEngine.jvision_to_ve_converter(ve, jvision, test_1)
        self.assertEqual(result, False)

        val = ve._suite_source_path
        ve._suite_source_path = "tests/unit/engines/verification"
        result = verifyEngine.jvision_to_ve_converter(ve, jvision, test_2)
        self.assertEqual(result, False)
        ve._suite_source_path = val

        result = verifyEngine.jvision_to_ve_converter(ve, jvision, "test_3.yaml")
        self.assertEqual(result, False)

        result = verifyEngine.jvision_to_ve_converter(ve, jvision_2, verify_jvision)
        self.assertEqual(result, False)

        result = verifyEngine.jvision_to_ve_converter(ve, jvision, verify_jvision, {'abc':'def'})
        self.assertEqual(result, False)

        patch_specific.return_value = [{'jkey': 'abc', 'val': '31', 'jvalue': '20'}]
        result = verifyEngine.jvision_to_ve_converter(ve, jvision, maping1, {'abc':'def'})
        self.assertEqual(result, False)

        result = verifyEngine.jvision_to_ve_converter(ve, jvision, maping, {'abc':'def'})
        self.assertEqual(result, True)

        result = verifyEngine.jvision_to_ve_converter(ve, jvision, maping2, {'abc':'def'})
        self.assertEqual(result, True)

    @patch("jnpr.toby.engines.verification.verify_utils._replace_value", return_value=None)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._merge_template_data", return_value={})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._search_template", return_value=False)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._put_tc_result_msg", return_value=None)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._get_testcase_result", return_value={'val':['result']})
    def test_verify_expression_testcase(self, patch_get, patch_put, patch_search, patch_merge, patch_replace):
        tc_data = {'expr':'1+1', 'preq':["val"], 'args':{'iterate_for':'10'}, 'val':{}, 'type':'get'}
        result = verifyEngine._verify_expression_testcase(ve, tc_data, "hello", 'device0', True,\
                                                        expanded_tc_datas=[{}])
        self.assertEqual(result, {'hello': [{'val': 2}]})

        tc_data = {'expr':'1+1', 'preq':["val"], 'args':{'iterate_for':'10'}, 'type':'get'}
        result = verifyEngine._verify_expression_testcase(ve, tc_data, "hello", 'device0', True,\
                                                        expanded_tc_datas=[{}])
        self.assertEqual(result, {'hello': [{'val': 2}]})

        patch_search.return_value = True
        tc_data = {'func':'1+1', 'preq':["val"], 'args':{'iterate_for':'10'}, "template['val']":{}}
        result = verifyEngine._verify_expression_testcase(ve, tc_data, "hello", 'device0', True,\
                                                        expanded_tc_datas=[{}])
        self.assertEqual(result, True)

        patch_get.return_value = {'val':['result', 'result2']}
        tc_data = {'expr':'1+1', 'preq':["val"], 'args':{'iterate_for':'10'}, 'val':{}, 'type':'get'}
        result = verifyEngine._verify_expression_testcase(ve, tc_data, "hello", 'device0', True,\
                                                        expanded_tc_datas=[{}])
        self.assertEqual(result, {'hello': [{'val': 2}]})

        tc_data = {'expr':'1e1{}', 'preq':["val"], 'args':{'iterate_for':'10'}, 'val':{}}
        result = verifyEngine._verify_expression_testcase(ve, tc_data, "hello", 'device0', True,\
                                                        expanded_tc_datas=[{}])
        self.assertEqual(result, False)

        tc_data = {'func':'1e1{}', 'preq':["val"], 'args':{'iterate_for':'10'}, "template['val']":{}}
        result = verifyEngine._verify_expression_testcase(ve, tc_data, "hello", 'device0', True,\
                                                        expanded_tc_datas=[{}])
        self.assertEqual(result, False)

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._verify_testcase", return_value=True)
    @patch("jnpr.toby.engines.verification.verify_utils.merge_dicts", return_value="abc")
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._pop_iterator_data", return_value=[{'abc':{'def':'sk'}}, {'value':'data'}])
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._iterator", return_value=True)
    def test_get_testcase_result(self, patch_iterator, patch_pop, patch_utils, patch_verify):
        result = verifyEngine._get_testcase_result(ve, [[{'abc':{'def':'sk'}}]], 'device0', 'sk', True)
        self.assertEqual(result, 'abc')

        result = verifyEngine._get_testcase_result(ve, [[{'abc':{'def':'sk'}}]], 'device0', 'sk', False)
        self.assertEqual(result, True)

        result = verifyEngine._get_testcase_result(ve, [{'abc':{'def':'sk'}}], 'device0', 'sk', False)
        self.assertEqual(result, True)

        result = verifyEngine._get_testcase_result(ve, [{'abc':{'def':'sk'}}], 'device0', 'sk', True)
        self.assertEqual(result, 'abc')

        result = verifyEngine._get_testcase_result(ve, [{}], 'device0', 'sk', False)
        self.assertEqual(result, True)

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._update_convergence", return_value=['is-equal', '20'])
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._is_converge", return_value=[True, '5'])
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._verify_testcase", return_value=True)
    @patch("time.sleep", return_value=True)
    def test_iterator(self, patch_verify, patch_converge, patch_update, patch_pop):
        kwargs = {"function":ve._verify_testcase, "iterate_type":"iterate_until", "tc_data":{'type':'def'}, "expected_return":True,\
        "device_handle":'device0', "tc_name" :'sk', "is_get":True, 'interval':1, 'timeout':1}
        result = verifyEngine._iterator(ve, **kwargs)
        self.assertEqual(result, True)

        kwargs = {"function":ve._verify_testcase, "iterate_type":"iterate_for", "tc_data":{'type':'def'}, "expected_return":True,\
        "device_handle":'device0', "tc_name" :'sk', "is_get":True, 'interval':1, 'timeout':1}
        result = verifyEngine._iterator(ve, **kwargs)
        self.assertEqual(result, True)


    def test_pop_iterator_data(self):
        result = verifyEngine._pop_iterator_data(ve, {'iterate_for':'10'})
        self.assertEqual(result, ({'iterate_for': '10'}, {}))

        result = verifyEngine._pop_iterator_data(ve, {'iterate_until':'10'})
        self.assertEqual(result, ({'iterate_until': '10'}, {}))

        result = verifyEngine._pop_iterator_data(ve, [])
        self.assertEqual(result, (None, None))

        result = verifyEngine._pop_iterator_data(ve, {'sk':{'iterate_until':'10'}})
        self.assertEqual(result, ({'iterate_until': '10'}, {}))

    def test_cleanup_xml_namespace(self):
        data = """<h:table xmlns:h="http://www.w3.org/TR/html4/"><name>'sk'</name></h:table>"""
        result = verifyEngine._cleanup_xml_namespace(ve, data)
        self.assertNotEqual(result, '')

        data = """hello"""
        self.assertRaises(etree.XMLSyntaxError, verifyEngine._cleanup_xml_namespace, ve, data)

        data = """<h:table xmlns:h="http://www.w3.org/TR/html4/"><name>'sk'</name><acs>'dcc'</acs></h:table>"""
        result = verifyEngine._cleanup_xml_namespace(ve, data)
        self.assertNotEqual(result, '')


    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.get_t_var", return_value="hello")
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.get_ifd_from_tag", return_value="hii")
    @patch("jnpr.toby.engines.verification.verify_utils.nested_set", return_value=None)
    def test_make_ifd_tvar(self, patch_verify, patch_get_ifd, patch_get_t):
        ve.t_handle = {'device0':{'interfaces':{'inf1':{'pic':'abc-123/456/789', 'link':'123'}, 'intf2':{'pic':'abc-123/456/789', 'link':'123'}}}}
        result = verifyEngine._make_ifd_tvar(ve)
        self.assertEqual(result, None)


    def test_update_convergence(self):
        ve._last_verify_result = {'hello':{'sk':{}}}
        ve._last_verify_device_name = "hello"
        ve._last_verify_tc_name = "sk"
        result = verifyEngine._update_convergence(ve, '12:10:24', None, 'abc', 'sk')
        self.assertEqual(result, (None, None))

    def test_get_monotonic_time(self):
        result = verifyEngine._get_monotonic_time(ve)
        self.assertTrue(result)

    @patch("time.sleep", return_value=True)
    def test_update_until(self, patch_cleanup):
        result = verifyEngine._update_until(ve, 0, 0.1, 0)
        self.assertEqual(result, (1, 0.1))

    def test_merge_template_data(self):
        tmpl_data = {'sk':{'value':{}, 'args':{'abc':'def'}}}
        tc_data = {'args':{'value':'123'}, 'parameters':{'value':'321'}}
        tc_name = 'sk'
        result = verifyEngine._merge_template_data(ve, tmpl_data, tc_data, tc_name)
        self.assertEqual(result, {'value': {}, 'parameters': {'value': '321'}, 'args': {'abc': 'def', 'value': '123'}})

        tmpl_data = {'sk':{'value':{}, 'args':{'abc':'def'}, 'parameters':{'val':'123'}}}
        tc_data = {'args':{'var':{'ab':'cd'}}, 'parameters':{'value':'321'}}
        tc_name = 'sk'
        result = verifyEngine._merge_template_data(ve, tmpl_data, tc_data, tc_name)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        tmpl_data = {'sk':{'value':{}, 'args':[{'abc':'def'}], 'xyz':{'parameters':{'value':{'data':'123'}}, 'xpath':"def"}}}
        tc_data = {'args':[{'ab':'cd'}], 'xyz':{'parameters':{'value':{'data':'321'}}, 'xpath':"abc"}}
        tc_name = 'sk'
        result = verifyEngine._merge_template_data(ve, tmpl_data, tc_data, tc_name)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        tmpl_data = {'sk':{'value':{}, 'args':{'abc':'def'}, 'parameters':{'value':{'ab':'123'}}}}
        tc_data = {'args':{'var':{'ab':'cd'}}, 'parameters':{'value':{'ab':'321'}}}
        tc_name = 'sk'
        result = verifyEngine._merge_template_data(ve, tmpl_data, tc_data, tc_name)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._cleanup_xml_namespace", return_value="hello")
    def test_get_response(self, patch_cleanup):
        ve.is_VE_offline = True
        ve.offline_data = None
        result = verifyEngine._get_response(ve, "command", "text", {'data':'value'}, "device0")
        self.assertEqual(result, False)

        ve.offline_data = True
        result = verifyEngine._get_response(ve, "command", "text", {'data':'value'}, "device0")
        self.assertEqual(result, True)

        ve.offline_data = """<?xml version="1.0" encoding="utf-16"?><supplier xmlns="http://schema.peters.com/doc_353/1/Types">019172</supplier>"""
        result = verifyEngine._get_response(ve, "command", "xml", {'data':'value'}, "device0")
        self.assertEqual(result, "hello")

        ve.is_VE_offline = False
        ve.offline_data = None
        ve._showdump = True
        result = verifyEngine._get_response(ve, "command", "xml", {'data':'value'}, "device0")
        self.assertEqual(result, "hello")

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value'}, "device0")
        self.assertEqual(result, True)
        ve._showdump = None

        ve.user_optimized = True
        result = verifyEngine._get_response(ve, None, "Text", {'data':'value'}, None)
        self.assertEqual(result, None)

        ve.user_optimized = False
        ve.response_optimize_iterator = True
        dh = MagicMock()
        dh.shell.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, None, "Text", {'data':'value'}, dh)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)
        ve.response_optimize_iterator = False

        sk = MagicMock()
        sk.nodes = MagicMock(return_value={"abc":'def'})
        sk.nodes.controllers = MagicMock(return_value={"pqr":"xyz"})
        sk.nodes.controllers.shell = MagicMock(return_value=None)
        sk.nodes.controllers.shell.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'user':'su'}, sk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'user':'su', 'password':'123'}, sk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk = MagicMock(spec=JuniperSystem)
        self.assertRaises(Exception, verifyEngine._get_response, ve, "command", "Text", {'data':'value', 'mode':'cty'}, mk)

        mk.nodes = MagicMock(return_value={"abc":'def'})
        mk.nodes.controllers = MagicMock(return_value={"pqr":"xyz"})
        mk.nodes.controllers.cty = MagicMock(return_value=None)
        mk.nodes.controllers.cty.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'node':'abc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'node':'abc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'node':'abc', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'node':'abc', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.current_node = MagicMock(return_value={"abc":'def'})
        mk.current_node.controllers = MagicMock(return_value={"pqr":"xyz"})
        mk.current_node.controllers.cty = MagicMock(return_value=None)
        mk.current_node.controllers.cty.response = MagicMock(return_value={'abc':'def'})

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'cmd':"abc", 'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cty', 'cmd':"abc", 'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.nodes.controllers.vty = MagicMock(return_value=None)
        mk.nodes.controllers.vty.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'node':'abc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'node':'abc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'node':'abc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'node':'abc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.current_node = MagicMock(return_value={"abc":'def'})
        mk.current_node.controllers = MagicMock(return_value={"pqr":"xyz"})
        mk.current_node.controllers.vty = MagicMock(return_value=None)
        mk.current_node.controllers.vty.response = MagicMock(return_value={'abc':'def'})

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'vty', 'cmd':"abc", 'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.su = MagicMock(return_value=None)

        mk.nodes.controllers.shell = MagicMock(return_value=None)
        mk.nodes.controllers.shell.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'node':'abc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs', 'user':'su', 'password':'abc'}, mk)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'node':'abc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs', 'user':'su'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'node':'abc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'node':'abc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.current_node = MagicMock(return_value={"abc":'def'})
        mk.current_node.controllers = MagicMock(return_value={"pqr":"xyz"})
        mk.current_node.controllers.shell = MagicMock(return_value=None)
        mk.current_node.controllers.shell.response = MagicMock(return_value={'abc':'def'})

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'shell', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.nodes.controllers.config = MagicMock(return_value=None)
        mk.nodes.controllers.config.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'format':'xml', 'data':'value', 'mode':'config', 'node':'abc',\
        'controller':'pqr', 'cmd':"abc", 'destination':'xzs', 'user':'su', 'password':'abc'}, mk)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)


        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'config', 'node':'abc', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.current_node = MagicMock(return_value={"abc":'def'})
        mk.current_node.controllers = MagicMock(return_value={"pqr":"xyz"})
        mk.current_node.controllers.config = MagicMock(return_value=None)
        mk.current_node.controllers.config.response = MagicMock(return_value={'abc':'def'})

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'config', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'config', 'cmd':"abc", 'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'config', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.nodes.controllers.get_rpc_equivalent = MagicMock(return_value=None)
        mk.nodes.controllers.execute_rpc = MagicMock(return_value=None)
        mk.nodes.controllers.execute_rpc.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'format':'xml', 'data':'value', 'mode':'xml-rpc', 'node':'abc',\
        'controller':'pqr', 'cmd':"abc", 'destination':'xzs', 'user':'su', 'password':'abc'}, mk)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)


        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'xml-rpc', 'node':'abc', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.current_node = MagicMock(return_value={"abc":'def'})
        mk.current_node.controllers = MagicMock(return_value={"pqr":"xyz"})
        mk.current_node.controllers.get_rpc_equivalent = MagicMock(return_value=None)
        mk.current_node.controllers.execute_rpc = MagicMock(return_value=None)
        mk.current_node.controllers.execute_rpc.response = MagicMock(return_value={'abc':'def'})

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'xml-rpc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'xml-rpc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'xml-rpc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.nodes.controllers.cli = MagicMock(return_value=None)
        mk.nodes.controllers.cli.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'format':'xml', 'data':'value', 'mode':'cli', 'node':'abc', 'controller':'pqr',\
        'cmd':"abc", 'destination':'xzs'}, mk)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cli', 'node':'abc', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cli', 'node':'abc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cli', 'node':'abc', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.current_node = MagicMock(return_value={"abc":'def'})
        mk.current_node.controllers = MagicMock(return_value={"pqr":"xyz"})
        mk.current_node.controllers.cli = MagicMock(return_value=None)
        mk.current_node.controllers.cli.response = MagicMock(return_value={'abc':'def'})

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cli', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cli', 'controller':'pqr', 'cmd':"abc",\
        'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cli', 'cmd':"abc", 'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'cli', 'cmd':"abc", 'destination':'xzs'}, mk, 60, 'abc')
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        mk.nodes.controllers.execute_command = MagicMock(return_value=None)
        mk.nodes.controllers.execute_command.response = MagicMock(return_value={'abc':'def'})
        result = verifyEngine._get_response(ve, "command", "Text", {'format':'xml', 'mode':'xyz', 'data':'value', 'cmd':"abc", 'destination':'xzs'},\
        mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)

        result = verifyEngine._get_response(ve, "command", "Text", {'data':'value', 'mode':'xyz', 'cmd':"abc", 'destination':'xzs'}, mk, 60)
        if result == None:
            result = False
        else:
            result = True
        self.assertEqual(result, True)


    @patch("builtins.open", create_file=False)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_all_checks_api", return_value=True)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_specific_checks_api", return_value={'args':{}, 'data':''})
    @patch("jnpr.toby.engines.verification.verify_utils.merge_dicts", return_value={'abc':'def'})
    def test_verify_specific_checks_in_parallel(self, patch_merge, patch_specific, patch_all, patch_open):
        t.set_background_logger = MagicMock(return_value=None)
        t.process_background_logger = MagicMock(return_value=None)
        builtins.t = MagicMock()
        t.log.return_value = True
        #omkar technically this function does not run.
        try:
            result = verifyEngine.verify_specific_checks_in_parallel(ve)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Mandatory argument list_checks not provided.")

        list_checks = [{'device':'device1', 'checks':'ospf_interface_check', \
                        'args':{'intf1':'ae1.1000'}}, {'device':'device0', \
                        'checks':'ospf_interface_check_new', 'args':{'intf2':'ae1.2000'}}]

        try:
            failmsg = "This is a robot call."
            result = verifyEngine.verify_specific_checks_in_parallel(ve, list_checks=list_checks, \
            is_robot=True, failmsg=failmsg)
        except Exception as exp:
            self.assertEqual(exp.args[0], "list index out of range")
        result = verifyEngine.verify_specific_checks_in_parallel(ve, list_checks=list_checks)
        self.assertTrue(result)

    def test_evaluate(self):
        ############   Testcases for basic value checks ########
        result = verifyEngine._evaluate(ve)
        self.assertEqual(result, False, "_evaluate function for no argument failed")


        result = verifyEngine._evaluate(ve, expect_value=1)
        self.assertEqual(result, False, "_evaluate function for no obtained value testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=1, opr='count')
        self.assertEqual(result, False, "_evaluate function for count opr testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='[1]', obtained_value='[1]')
        self.assertEqual(result, True, "_evaluate function for default is-equal testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='[1]', obtained_value=[1])
        self.assertEqual(result, True, "_evaluate function for is-equal negative testcase failed")

        #########  Testcases for delta constarints ###########

        result = verifyEngine._evaluate(ve, expect_value=1, obtained_value=[1, 3], opr="is-lt", atr_constraint='delta')
        self.assertEqual(result, False, "_evaluate function for lt and gt delta constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=3, obtained_value=[1, 2], opr="is-lt", atr_constraint='delta')
        self.assertEqual(result, True, "_evaluate function for lt and gt delta constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=2, obtained_value={1, 1}, opr="is-lt", atr_constraint='delta')
        self.assertEqual(result, False, "_evaluate function for lt and gt delta constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=2, obtained_value=1, opr="is-lt", atr_constraint='delta')
        self.assertEqual(result, False, "_evaluate function for lt and gt delta constraint testcase failed")

        ######  Testcases for switch-value operator ########

        result = verifyEngine._evaluate(ve, expect_value=[1, 2, 3], obtained_value=[1, 2, 3, 3], opr="switch-value")
        self.assertEqual(result, True, "_evaluate function for switch-value operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=[1, 3, 5, 7], obtained_value=[1, 2, 3, 4, 5, 6, 7], opr="switch-value")
        self.assertEqual(result, False, "_evaluate function for switch-value operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=[1, 3, 5, 7], obtained_value=[1, 2, 3, 4, 5, 6, 7], opr="switch-value[loose]")
        self.assertEqual(result, True, "_evaluate function for switch-value operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=[1, 2, 3], obtained_value=[1, 2, 3, 4, 5], opr="switch-value[loose]")
        self.assertEqual(result, False, "_evaluate function for switch-value operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=[1, 2, 3, 4, 5, 6, 7], obtained_value=[1, 2, 3, 4, 5], opr="switch-value[loose]")
        self.assertEqual(result, False, "_evaluate function for switch-value operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=[1, 3, 5, 5], obtained_value=[1, 2, 3, 3, 4, 4, 5], opr="switch-value[loose]")
        self.assertEqual(result, False, "_evaluate function for switch-value operator testcase failed") #for line 1390

        result = verifyEngine._evaluate(ve, expect_value=[0, 2, 3, 4, 5], obtained_value=[1, 2, 3, 4, 5], opr="switch-value[loose]")
        self.assertEqual(result, False, "_evaluate function for switch-value operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=[1, 1], obtained_value=[1, 2], opr="switch-value[xyz]")
        self.assertEqual(result, False, "_evaluate function for switch-value operator testcase failed")

        ##########  Testcases for is-equal, not-equal, is-lt, is-gt constraints #######

        result = verifyEngine._evaluate(ve, expect_value='[2]', obtained_value='[2]', opr="not-equal")
        self.assertEqual(result, False, "_evaluate function for not-equal constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='[1, 2]', obtained_value='[2, 3]', opr="not-equal")
        self.assertEqual(result, True, "_evaluate function for not-equal constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='[1, 2]', obtained_value='[4, 2]')
        self.assertEqual(result, False, "_evaluate function for no constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='[1, 2]', obtained_value='[2, 3, 4]', opr="not-equal")
        self.assertEqual(result, False, "_evaluate function for not-equal constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='1', obtained_value='[2, 3]', opr="not-equal")
        self.assertEqual(result, True, "_evaluate function for not-equal constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='1', obtained_value='[2, 3]')
        self.assertEqual(result, False, "_evaluate function for not constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='1', obtained_value='[1, 2, 3]', opr="is-lt")
        self.assertEqual(result, False, "_evaluate function for is-lt constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value={'1':1}, obtained_value='[1, 2, 3]', opr="is-gt")
        self.assertEqual(result, False, "_evaluate function for is-gt constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=['test', 'sample'], obtained_value='test', opr="not-equal")
        self.assertEqual(result, False, "_evaluate function for not-equal constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='test', obtained_value='test', opr="not-equal")
        self.assertEqual(result, False, "_evaluate function for not-equal constraint testcase failed")

        # Testcases for Count constrints #

        result = verifyEngine._evaluate(ve, expect_value=2, obtained_value=[1, 2, 3], opr="count-is-equal")
        self.assertEqual(result, False, "_evaluate function for count-is-equal negative constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=2, obtained_value=[1, 2, 3], opr="count-is-gt")
        self.assertEqual(result, True, "_evaluate function for count-is-gt negative constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=5, obtained_value=[1, 2, 3], opr="count-is-lt-or-equal")
        self.assertEqual(result, True, "_evaluate function for count-is-lt-or-equal constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=3, obtained_value=[1, 2, 3], opr="count-is-equal")
        self.assertEqual(result, True, "_evaluate function for count-is-equal constraint testcase failed")

        ######## Testcases for regex constraints #########

        result = verifyEngine._evaluate(ve, expect_value="test", obtained_value="testvalue", opr="regexp")
        self.assertEqual(result, True, "_evaluate function for regexp constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value="test1", obtained_value="testvalue", opr="regexp")
        self.assertEqual(result, False, "_evaluate function for regexp negative constraint testcase failed")

        ######## Testcases for range constraints #########

        result = verifyEngine._evaluate(ve, expect_value="1-5", obtained_value=29, opr="not-range")
        self.assertEqual(result, True, "_evaluate function for not-range constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=["1to5"], obtained_value=29, opr="not-range")
        self.assertEqual(result, True, "_evaluate function for not-range constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=["1to5"], obtained_value=[1, 2], opr="in-range")
        self.assertEqual(result, True, "_evaluate function for not-range constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value="10to50", obtained_value=29, opr="in-range")
        self.assertEqual(result, True, "_evaluate function for in-range constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value="10:20", obtained_value=29, opr="in-range")
        self.assertEqual(result, False, "_evaluate function for in-range negative testcase failed")

        result = verifyEngine._evaluate(ve, expect_value="10:20:30", obtained_value=29, opr="in-range")
        self.assertEqual(result, False, "_evaluate function for negative testcase failed")


        ######## Testcases for contains constraints #########

        result = verifyEngine._evaluate(ve, expect_value="test", obtained_value="testvalue", opr="contains")
        self.assertEqual(result, True, "_evaluate function for contains constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value="test1", obtained_value="testvalue", opr="not-contains")
        self.assertEqual(result, True, "_evaluate function for not-contains testcase failed")

        result = verifyEngine._evaluate(ve, expect_value="test", obtained_value="testvalue", opr="not-contains")
        self.assertEqual(result, False, "_evaluate function for not-contains negative testcase failed")

        ######## Testcases for exist constraints #########

        result = verifyEngine._evaluate(ve, expect_value="test", obtained_value=['test'], opr="not-exists")
        self.assertEqual(result, False, "_evaluate function for not-exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, expect_value="test", obtained_value=['test'], opr="exists")
        self.assertEqual(result, True, "_evaluate function for exists constraint testcase failed")

        ######## Testcases for number or string constraints #########

        result = verifyEngine._evaluate(ve, obtained_value=[2], opr="is-number")
        self.assertEqual(result, True, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value="test", opr="is-string")
        self.assertEqual(result, True, "_evaluate function for exists constraint testcase failed")

        ######## Testcases for number or string constraints #########

        result = verifyEngine._evaluate(ve, obtained_value=[3, 7], opr="is-odd")
        self.assertEqual(result, True, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value=[4, 8], opr="is-even")
        self.assertEqual(result, True, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value=3, opr="is-odd")
        self.assertEqual(result, True, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value=4, opr="is-even")
        self.assertEqual(result, True, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value=-1, opr="is-even")
        self.assertEqual(result, False, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value=[-1, -2], opr="is-even")
        self.assertEqual(result, False, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value="even", opr="is-even")
        self.assertEqual(result, False, "_evaluate function for exists constraint testcase failed")

        result = verifyEngine._evaluate(ve, obtained_value="sent", opr="sending-false")
        self.assertEqual(result, False, "_evaluate function for exists constraint testcase failed")

        ######## Testcases for in operators #########
        result = verifyEngine._evaluate(ve, expect_value="test", obtained_value=['test'], opr="is-in")
        self.assertEqual(result, True, "_evaluate function for is-in operator  testcase failed")

        result = verifyEngine._evaluate(ve, expect_value=['test', 'value'], obtained_value=['testvalue'], opr="is-in")
        self.assertEqual(result, False, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.1-10.0.0.10', obtained_value='10.0.0.5', opr="is-in")
        self.assertEqual(result, True, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.0/24', obtained_value='10.0.0.121', opr="is-in")
        self.assertEqual(result, True, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.1', obtained_value='10.0.0.2', opr="is-in")
        self.assertEqual(result, False, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.1-10.0.0.5', obtained_value=['10.0.0.3', '10.0.0.2'], opr="is-in")
        self.assertEqual(result, True, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.1-10.0.0.5', obtained_value=['10.0.0.3', '10.0.0.2'], opr="not-in")
        self.assertEqual(result, False, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.0/24', obtained_value=['10.0.0.1', '10.0.0.2'], opr="is-in")
        self.assertEqual(result, True, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.2', obtained_value=['10.0.0.1', '10.0.0.2'], opr="not-in")
        self.assertEqual(result, False, "_evaluate function for is-in operator testcase failed")

        result = verifyEngine._evaluate(ve, expect_value='10.0.0.2', obtained_value=['10.0.0.1', '10.0.0.2'], opr="is-in")
        self.assertEqual(result, False, "_evaluate function for is-in operator testcase failed")

    @patch("builtins.open", create_file=False)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_all_checks_api", return_value=True)
    def test_verify_dict(self, patch_verify_all, patch_open):
        patch_open.side_effect = [mock.mock_open(read_data=None).return_value,\
            Exception]
        # mmohan
        result = verifyEngine.verify_dict(ve, input_dict={'verify':{'device0':{'check1':{'args':[{'intf':'ge10.0.0'}]}}}})
        self.assertEqual(result, True, "verify_dict TC for dict input failed")

        result = verifyEngine.verify_dict(ve, input_dict=[{'verify':{'device0':{'check1':{'args':[{'intf':'ge10.0.0'}]}}}}])
        self.assertEqual(result, False, "verify_dict TC for non-dict input failed")

        #result = verifyEngine.verify_dict(ve, input_dict={'verify':{'device0':{'check1':{'args':[{'intf':'ge10.0.0'}]}}}})
        #self.assertEqual(result, False, "verify_dict TC for exception in file operation failed")


    def test_jvision_records_slicer(self):

        result = verifyEngine._jvision_records_slicer(ve, records="2:5", obtained_value=[])
        self.assertEqual(result, [], "_jvision_records_slicer TC for empty obtained value failed")

        result = verifyEngine._jvision_records_slicer(ve, records="2:5", obtained_value=[1, 2, 3, 4, 5, 6])
        self.assertEqual(result, [3, 4, 5], "_jvision_records_slicer TC for record type a:b failed")

        result = verifyEngine._jvision_records_slicer(ve, records=":6", obtained_value=[1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(result, [1, 2, 3, 4, 5, 6], " _jvision_records_slicer TC for record type :b failed")

        result = verifyEngine._jvision_records_slicer(ve, records="3:", obtained_value=[1, 2, 3, 4, 5, 6])
        self.assertEqual(result, [4, 5, 6], "_jvision_records_slicer TC for record type a: failed")

        result = verifyEngine._jvision_records_slicer(ve, records="5", obtained_value=[1, 2, 3, 4, 5, 6])
        self.assertEqual(result, 6, "_jvision_records_slicer TC for normal index failed")

    def test_sub_merge_args_list(self):
        prior_args = [{'l1':'1'}, {'l2':'2'}, {'l3':'3'}]
        non_prior_args = [{'l4':'4'}, {'l5':'5'}, {'l6':'6'}]
        result = verifyEngine._sub_merge_args_list(ve, prior_args, non_prior_args)
        self.assertEqual(result, [{'l1':'1'}, {'l2':'2'}, {'l3':'3'}, {'l4':'4'}, {'l5':'5'}, {'l6':'6'}])

        prior_args = [{'l1':'1'}, {'l2':'2'}, {'l3':'3'}]
        non_prior_args = [{'l2':'4'}, {'l3':'5'}, {'l1':'6'}]
        result = verifyEngine._sub_merge_args_list(ve, prior_args, non_prior_args)
        self.assertEqual(result, [{'l1':'1'}, {'l2':'2'}, {'l3':'3'}])

    def test_merge_args_list(self):
        result = verifyEngine._merge_args_list(ve)
        self.assertEqual(result, [], "_merge_args_list TC for empty args")

        result = verifyEngine._merge_args_list(ve, local_args=[{'l1':1}, {'l2':2}], global_args=[{'g1':1}, {'g2':2}], cli_args=[{'c1':1}, {'c2':2}])
        self.assertEqual(result, [{'c1': 1}, {'c2': 2}, {'l1': 1}, {'l2': 2}, {'g1': 1}, {'g2': 2}], "_merge_args_list TC for empty args")

    @patch("jnpr.toby.engines.verification.verify_utils.get_yaml_data_as_dict", return_value={'verify_tmpl':{'args':['intf']}})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._expand_file_list", return_value=['a.yaml', 'b.yaml'])
    def test_source_templates(self, patch_expand, patch_get_yaml):
        verify_data = {'use_template':'a, b'}
        file_data = {'verify_template':{}}

        verifyEngine._source_templates(ve, verify_data={}, file=file_data)

        patch_get_yaml.return_value = {'verify_template':{'args':['intf']}}
        verifyEngine._source_templates(ve, verify_data={}, file=file_data)

        patch_get_yaml.return_value = {"verify":{}}
        verifyEngine._source_templates(ve, verify_data={}, file=file_data)

        patch_get_yaml.return_value = {}
        verifyEngine._source_templates(ve, verify_data={}, file=file_data)

    def test_merge_nested_template_data(self):
        tmpl_data = {'sk':{'value':{}, 'args':{'abc':'def'}}}
        nested_tmpl_data = {'sk':{'value':{}, 'args':{'abc':'def'}}}

        verifyEngine._merge_nested_template_data(ve, tmpl_data=tmpl_data, nested_tmpl_data=nested_tmpl_data)

    def test_merge_generic_tmpl(self):
        tmpl_data = {'sk':{'value':{}, 'args':{'abc':'def'}}}
        verifyEngine._merge_generic_tmpl(ve, tmpl_data=tmpl_data)

        tmpl_data = {'sk':{'value':{}, 'template':'abc'}}
        verifyEngine._merge_generic_tmpl(ve, tmpl_data=tmpl_data)

        tmpl_data = {'sk':{'value':{}, 'template':'abc'}}
        result = verifyEngine._merge_generic_tmpl(ve, tmpl_data=tmpl_data)
        self.assertEqual(result, None)

    @patch("builtins.open", create_file=False)
    #@patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.sys.path.append", return_value =True)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._merge_template_data", return_value={'key':'value'})
    #@patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._search_template", side_effect=[False, True, True, True, True, True])
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._search_template", side_effect=[True])
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._get_testcase_result", return_value={'preq1':['result'],\
    'preq2':['result1', 'result2']})
    def test_process_testcase(self, patch_verify, patch_search, patch_merge, patch_open):
        result = verifyEngine._process_testcase(ve, tc_data={'iterator':'loop(intf, interval)', 'intf':[1, 2, 3], 'interval':(10, 20),\
        'value':"sample", 'cmd':"test"}, tc_name="TC1", device_handle='dh0', device='device1', device_name="abc", is_get=True)
        self.assertEqual(result, None, "test_process_testcase Failed")

        result = verifyEngine._process_testcase(ve, tc_data={'tc1':{'intf':[1, 2, 3], 'interval':(10, 20), 'value':"sample", 'cmd':"test"},\
        'tc2':{'intf':[1, 2, 3], 'interval':(10, 20), 'value':"val", 'cmd':"test", 'type':'get'}}, tc_name="TC1", device_handle='dh0',\
        device='device1', device_name="abc", is_get=True)
        self.assertEqual(result, None, " Failed")

        result = verifyEngine._process_testcase(ve, tc_data={'intf':[1, 2, 3], 'interval':(10, 20), 'value':"sample", 'cmd':"test", 'type':'get'},\
        tc_name="TC1", device_handle='dh0', device='device1', device_name="abc", is_get=True)
        self.assertEqual(result, {'preq2': ['result1', 'result2'], 'preq1': ['result']}, "test_process_testcase Failed")


    def test_form_device_specific_testcase(self):
        result = verifyEngine._form_device_specific_testcase(ve, tc_data={'args':{}, 'cmd':"show version"}, device_list="device1-3")
        self.assertEqual(result, [{'device1': {'args': {}, 'cmd': 'show version'}}, {'device2': {'args': {}, 'cmd': 'show version'}},\
        {'device3': {'args': {}, 'cmd': 'show version'}}], "test_form_device_specific_testcase Failed")

    def test_search_template(self):
        builtins.t = self
        t.is_robot = True
        t.t_dict = {'resources':{'device0':{'interface':['ge0.1']}, 'device2':{'interface':['ge0.1']}}}

        ve.process_tmpl_data = [{"device0-2":{'Temp1':"abc.tmpl"}, 'device3':{}, "Temp1":{}}]
        result = verifyEngine._search_template(ve, template_name="Temp1")
        self.assertEqual(result, {'Temp1': 'abc.tmpl'}, "test_search_template Failed")

        ve.process_tmpl_data = [{"Temp1":{}}]
        result = verifyEngine._search_template(ve, template_name="Temp1")
        self.assertEqual(result, {'Temp1': {}}, "test_search_template Failed")


    def test_expand_and_append(self):
        result = verifyEngine._expand_and_append(ve, values=[], path_to_subtc={'tc':{'parameters':{}}}, each_item='', data={'args':[{'intf':"ae1"}]})
        self.assertEqual(result, None, "test_expand_and_append Failed")

    def test_expand_ce_modifier(self):
        result = verifyEngine._expand_ce_modifier(ve, "text")
        self.assertEqual(result, ['text'], "test_expand_ce_modifier Failed")

        result = verifyEngine._expand_ce_modifier(ve, 10)
        self.assertEqual(result, [10], "test_expand_ce_modifier Failed")

        result = verifyEngine._expand_ce_modifier(ve, '<<text>>')
        self.assertEqual(result, ['text'], "test_expand_ce_modifier Failed")

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._expand_and_append")
    def test_extract_value_from_path(self, patch_expand_append):
        result = verifyEngine._extract_value_from_path(ve, data={'intf':'ge1.0'}, each_item='intf', values=[])
        self.assertEqual(result, None, "test_extract_value_from_path Failed")

        result = verifyEngine._extract_value_from_path(ve, data={'args':['intf'], 'port':1}, each_item='args', values=[])
        self.assertEqual(result, None, "test_extract_value_from_path Failed")

        result = verifyEngine._extract_value_from_path(ve, data={'args':['intf'], 'port':1}, each_item='args:', values=[])
        self.assertEqual(result, None, "test_extract_value_from_path Failed")

    @patch("jnpr.toby.engines.verification.verify_utils.find_dict_data", return_value=[[{'interface':'ge1.0'}], "/device0/interface"])
    def test_get_t_var(self, patch_dict_data):
        builtins.t = self
        t.is_robot = True
        t.t_dict = {'resources':{'device0':{'interface':['ge1.0']}, 'device2':{'interface':['ge1.0']}}}

        try:
            result = verifyEngine.get_t_var(ve)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Mandatory arg 'tv' is missing", "test_get_t_var Failed....")

        result = verifyEngine.get_t_var(ve, tv="device0__interface")
        self.assertEqual(result, {'interface': 'ge1.0'}, "test_get_t_var Failed")

        result = verifyEngine.get_t_var(ve, tv="interface")
        self.assertEqual(result, {'interface': 'ge1.0'}, "test_get_t_var Failed")

        patch_dict_data.return_value = [{'interface':'ge1.0'}, "/device0/interface"]
        result = verifyEngine.get_t_var(ve, tv="device0_interface", return_path=True)
        self.assertEqual(result, ({'interface': 'ge1.0'}, '/device0/interface'), "test_get_t_var Failed")

        try:
            result = verifyEngine.get_t_var(ve, tv="tv[device0]")
        except Exception as exp:
            self.assertEqual(exp.args[0], "tvar tv[device0] can not be accessed as a list", "test_get_t_var Failed....")

        patch_dict_data.return_value = [None, None]
        result = verifyEngine.get_t_var(ve, tv="tv[interface]")
        self.assertEqual(result, None, "test_get_t_var Failed")

        patch_dict_data.return_value = [[{'interface':'ge1.0'}], "/device0/interface"]
        result = verifyEngine.get_t_var(ve, tv="tv[device0]")
        self.assertEqual(result, "tv[device0]", "test_get_t_var Failed")

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.get_t_var", return_value=None)
    def test_get_ifd_from_tag(self, patch_get_t_var):
        try:
            result = verifyEngine.get_ifd_from_tag(ve, device_tag='device0', ifd_tag='intf0')
        except Exception as exp:
            self.assertEqual(exp.args[0], "cannot find ifd tag intf0 in device0", "test_get_ifd_from_tag Failed..")
        patch_get_t_var.return_value = "value"
        result = verifyEngine.get_ifd_from_tag(ve, device_tag='device0', ifd_tag='intf0')
        self.assertEqual(result, "value", "test_get_ifd_from_tag Failed..")

    def test_execute_xpath(self):
        result = verifyEngine._execute_xpath(ve, input_xml="<a><b><c>data</c></b></a>", tc_data={'xpath':"/a/b/c"})
        self.assertEqual(result, '_NONE', "test_execute_xpath")

        with patch("jnpr.toby.engines.verification.verify_utils._convert_lxml_to_data", return_value=[]):
            result = verifyEngine._execute_xpath(ve, input_xml="<a><b><c>data</c></b></a>", tc_data={'xpath':"/a/b"})
            self.assertEqual(result, [], "test_execute_xpath")

#    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine.log_text_output", return_value=True)
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._get_response", side_effect=[Exception, "data", etree.XML("<a>1</a>")])
    def test_get_xml_response(self, patch_response):
        result = verifyEngine._get_xml_response(ve, each_cmd="command", form={}, each_proto_data={'data':'value'}, dev="device0")
        self.assertEqual(result, False, "test_get_xml_response Failed")

        result = verifyEngine._get_xml_response(ve, each_cmd="command", form={}, each_proto_data={'data':'value'}, dev="device0")
        self.assertEqual(result, False, "test_get_xml_response Failed")

        ve.log_text_output = True
        result = verifyEngine._get_xml_response(ve, each_cmd="command", form={}, each_proto_data={'data':'value'}, dev="device0")
        self.assertEqual(result, False, "test_get_xml_response Failed")

        result = verifyEngine._get_xml_response(ve, each_cmd="command", form={}, each_proto_data={'data':'value'}, dev="device0")
        #self.assertEqual(type(result), type(etree.XML("<a>1</a>")), "test_get_xml_response Failed")

    def test_execute_regexp(self):
        result = verifyEngine._execute_regexp(ve, regexp=".*", processed_data="data", regexp_flags=None, match_all=False)
        self.assertEqual(result.group(), "data", "test_execute_regexp Failed")

        result = verifyEngine._execute_regexp(ve, regexp=".*", processed_data="data", regexp_flags="re.I", match_all=False)
        self.assertEqual(result.group(), "data", "test_execute_regexp Failed")

        result = verifyEngine._execute_regexp(ve, regexp="(data)", processed_data="data data", regexp_flags=None, match_all=True)
        self.assertEqual(result, ['data', 'data'], "test_execute_regexp Failed")

        result = verifyEngine._execute_regexp(ve, regexp="data", processed_data="data data", regexp_flags="re.I", match_all=True)
        self.assertEqual(result, ['data', 'data'], "test_execute_regexp Failed")

    def test_execute_grep(self):
        result = verifyEngine._execute_grep(ve, grep="grep", grep_flags=None, processed_data="data1\n data2grep\n data3")
        self.assertEqual(result, [' data2grep'], "test_execute_grep Failed")

        result = verifyEngine._execute_grep(ve, grep="grep", grep_flags="re.I", processed_data="data1\n data2grep\n data3")
        self.assertEqual(result, [' data2grep'], "test_execute_grep Failed")

    def test_execute_regexp_grep(self):
        result = verifyEngine._execute_regexp_grep(ve, tc_data={'regexp':"", "grep":"", "group":""}, input_text="sample_text", re_flag="re.I",\
        re_flag_constant="")
        self.assertEqual(result, False, "test_execute_regexp_grep Failed")

        result = verifyEngine._execute_regexp_grep(ve, tc_data={"grep":"text", "group":""}, input_text="sample_text", re_flag="re.I",\
        re_flag_constant="")
        self.assertEqual(result, ['sample_text'], "test_execute_regexp_grep Failed")

        result = verifyEngine._execute_regexp_grep(ve, tc_data={'regexp':"text", "group":""}, input_text="sample_text", re_flag="re.I",\
        re_flag_constant="")
        self.assertEqual(result, ['_NONE'], "test_execute_regexp_grep Failed")

        result = verifyEngine._execute_regexp_grep(ve, tc_data={'regexp':"txt", "group":""}, input_text="sample_text", re_flag="re.I",\
        re_flag_constant="")
        self.assertEqual(result, ['_NONE'], "test_execute_regexp_grep Failed")

    @patch("jnpr.toby.engines.verification.verify_utils.get_xpath_result", return_value={'abc':'def'})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._verify_parameters", return_value={'sk':'123'})
    def test_process_parameters(self, patch_verify, patch_get):
        tc_data = {'cmd_timeout':21, 'cmd_pattern':'abcxyz'}
        test_data = {'rpath':'def'}
        tree = {'pqr':'xyz'}
        small_testcase_data = {'abc':{'xpath':'abc'}}
        cmd = "safrfr"
        tree = {'abc':'def'}
        result = verifyEngine._process_parameters(ve, tc_data, test_data, tree, small_testcase_data, cmd, 12, 'device0', True, True, "acs")
        self.assertEqual(result, {'sk': '123'})

        result = verifyEngine._process_parameters(ve, tc_data, test_data, tree, small_testcase_data, cmd, 12, 'device0', None, True, "acs")
        self.assertEqual(result, None)

    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._execute_regexp_grep", return_value='123')
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._get_response", return_value='value')
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._get_xml_response", return_value=etree.XML("<a>1</a>"))
    @patch("jnpr.toby.engines.verification.verify_utils.create_ve_debug_log", return_value=None)
    def test_verify_testcase(self, patch_create, patch_get, patch_response, patch_execute):
        ve._last_verify_device_name = MagicMock()
        ve._last_verify_result = MagicMock()
        ve.global_args = [{'arg1':1}, {'arg2':'2'}]
        tc_data = {'cmd': 'show ospf neighbor | display xml', 'value': '10.0.0.0/16', \
                   'xpath': '/ospf-neighbor-information/ospf-neighbor/neighbor-address', \
                   'operator': 'is-in'}
        tc_name = "check_ospf_count_1"
        device_handle = 'dh0'

        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)

        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "xpath": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'xpath': '/ospf-interface-information/ospf-interface'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)


        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"value": 1.5, "operator": "is-lt"}, \
                   'xpath': '/ospf-interface-information/ospf-interface'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)


        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "xpath": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'xpath': '/ospf-interface-information/ospf-interface', 'format':'Text'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)

        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"value": 1.5, "operator": "is-lt"}, \
                   'xpath': '/ospf-interface-information/ospf-interface'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)



        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "Text": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'text': '/ospf-interface-information/ospf-interface', 'format':'Text'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)

        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "xpath": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'xpath': '/ospf-interface-information/ospf-interface', 'format':'Text', 'value':'123'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertTrue(result)

        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "xpath": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'xpath': '/ospf-interface-information/ospf-interface', 'format':'xml', 'value':'123'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)

        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", \
                   "check_interface_metric": {"value": 1.5, "operator": "is-lt"}, \
                   'xpath': '/ospf-interface-information/ospf-interface', 'format':'txt'}

        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertTrue(result)

        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", 'regexp_flags': "re.I", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "xpath": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'xpath': '/ospf-interface-information/ospf-interface', 'format':'Text', 'value':'123'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertTrue(result)

        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", 'regexp':".*", 'regexp_flags': "re.I", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "Text": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'text': '/ospf-interface-information/ospf-interface', 'format':'Text'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertFalse(result)


        tc_data = {'args': [{'intf': 'ae1.15'}], 'cmd': "show ospf interface var['intf'] detail", 'type': "positive", \
                   "check_interface_metric": {"parameters": {"ospf-topology-metric": {"value": 1.5, \
                   "operator": "is-lt"}}, \
                    "xpath": "/ospf-interface-information/ospf-interface/ospf-interface-topology"}, \
                   'parameters': {'hello-interval': {'operator': 'is-equal', 'value': 30}, \
                   'ospf-interface-topology': {'ospf-topology-metric': {'operator': 'is-equal', \
                   'value': 1}}}, 'xpath': '/ospf-interface-information/ospf-interface', 'format':'Text', 'value':'123'}
        result = verifyEngine._verify_testcase(ve, tc_data, device_handle, tc_name)
        self.assertEqual(result, None)

    def test_is_converge(self):
        timestamp = datetime.datetime.now()
        result = verifyEngine._is_converge(ve, False, 10, 2, True, True, timestamp)
        self.assertTrue(result)

        result = verifyEngine._is_converge(ve, False, 10, 2, True, False, timestamp)
        self.assertTrue(result)

        result = verifyEngine._is_converge(ve, True, 2, 10, True, False, timestamp)
        self.assertTrue(result)

    def test_put_verify_log(self):
        verifyEngine._put_verify_log(ve, opr="count", obtain="_NONE")

        verifyEngine._put_verify_log(ve, opr="count", obtain="msg")

        verifyEngine._put_verify_log(ve, opr="add", obtain="_NONE")

        verifyEngine._put_verify_log(ve, opr="add", obtain=["_NONE"])

        verifyEngine._put_verify_log(ve, opr="add", obtain=["text"])

        verifyEngine._put_verify_log(ve, opr="add", obtain=["text", "1"])

        verifyEngine._put_verify_log(ve, opr="add", obtain=["text", "1"], result=False)

    @patch("jnpr.toby.engines.verification.verify_utils.find_dict_data", return_value=[{"data":"value"}, "a/b/c"])
    def test_search_and_retrieve_tc_data(self, patch_find_dict):
        result = verifyEngine._search_and_retrieve_tc_data(ve, data=[{"device0":{"a":{"b":"c", "d":"e"}}}], device="device0", test_data="a/d",\
        testcase="a:b")
        self.assertEqual(result, ({'data': 'value'}, {'data': 'value'}, 'a/b/c'), "test_search_and_retrieve_tc_data Failed")

        #patch_find_dict.return_value=None
        result = verifyEngine._search_and_retrieve_tc_data(ve, data=[{"device1":{"a":{"b":"c", "d":"e"}}}], device="device0", test_data="a/d",\
        testcase="a:b")
        self.assertEqual(result, ({'data': 'value'}, {'data': 'value'}, 'a/b/c'), "test_search_and_retrieve_tc_data Failed")


    def test_get_specific_data(self):
        with patch('jnpr.toby.engines.verification.verifyEngine.verifyEngine.verify_specific_checks_api',\
        return_value={'tt-testtech-vj-27-9066443-vm': {'ospf_interface_check': {'hello-interval': 30}}}):
            result = verifyEngine.get_specific_data(ve, return_type='hello-interval')
            self.assertEqual(result, 30)


    def test_get_logical_name(self):
        t.t_dict = {'resources':{'device0':{'interface':['ge0.1'], 'system': {'primary': {'name': 'verify_device'}}}}}

        device = verifyEngine._get_logical_name('verify')
        device = verifyEngine._get_logical_name('verify_device')
        self.assertEqual(device, 'device0')

    def test_is_file_exists(self):
        file_name = 'verify_jvision'
        result = verifyEngine._is_file_exists(file_name)
        self.assertFalse(result)
        file_name = 'verify_not.yaml'
        result = verifyEngine._is_file_exists(file_name)
        self.assertFalse(result)

    def test_get_last_verify_result(self):
        result = verifyEngine.get_last_verify_result(ve)
        self.assertTrue(isinstance(result, dict))

    def test_segregate_tc_data(self):
        data = {'value':'abc', 'operator':'is-equal', 'iterate_for':'10'}
        result = verifyEngine._segregate_tc_data(ve, data)
        self.assertEqual(result, [[{'value':'abc', 'operator':'is-equal', 'iterate_for':'10'}], {}])

        data = {'iterate_for':'10'}
        result = verifyEngine._segregate_tc_data(ve, data)
        self.assertEqual(result, [[{'iterate_for':'10'}], {}])

        data = {'abc':{'iterate_for':'10'}}
        result = verifyEngine._segregate_tc_data(ve, data)
        self.assertEqual(result, [[{'abc':{'iterate_for':'10'}}], {}])

        data = {'abc':{'value':'abc', 'operator':'is-equal'}}
        result = verifyEngine._segregate_tc_data(ve, data)
        self.assertEqual(result, [[], {'abc':{'value':'abc', 'operator':'is-equal'}}])

        data = {'abc':{}}
        result = verifyEngine._segregate_tc_data(ve, data)
        self.assertEqual(result, [[], {'abc':{}}])

    def test_process_xpath_filter(self):
        xpath_filter = None
        tc_data = {'_all_parameters':{'abc':{'def':'123'}}, 'xpath':"abc"}
        result = verifyEngine._process_xpath_filter(ve, xpath_filter, tc_data)
        self.assertEqual(result, {})
        xpath_filter = ['abc']
        result = verifyEngine._process_xpath_filter(ve, xpath_filter, tc_data)
        self.assertEqual(result, {'_root_xpath': 'abc'})
        tc_data = {'_all_parameters':{'abc':{'xpath':'abc/123/2113/123'}}}
        result = verifyEngine._process_xpath_filter(ve, xpath_filter, tc_data)
        self.assertEqual(result, {'2113': '123'})


    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._search_template", return_value=True)
    @patch("jnpr.toby.engines.verification.verify_utils.get_yaml_data_as_dict", return_value={'abc':'def'})
    @patch("jnpr.toby.engines.verification.verifyEngine.verifyEngine._source_templates", return_value=None)
    def test_check_generic_template(self, patch_source, patch_get, patch_search):
        template_name = "abc"
        result = verifyEngine._check_generic_template(ve, template_name)
        self.assertEqual(result, False)

        template_name = "j_check_abc"
        result = verifyEngine._check_generic_template(ve, template_name)
        self.assertEqual(result, False)

        template_name = "j_check_abc"
        result = verifyEngine._check_generic_template(ve, template_name)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()