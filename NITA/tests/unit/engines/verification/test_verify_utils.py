import sys
import unittest
from mock import patch, MagicMock
from lxml import etree
from jnpr.toby.engines.verification.verify_utils import *
#from verify_utils import *
from jnpr.toby.engines.verification.verify_utils import _convert_list_to_datatype, _convert_lxml_to_data, get_xpath_result, process_constraints, \
    _expand_numeric_string,  expand_alpha_numeric_string, _replace_value, _get_temp_args, merge_dicts
#from verify_utils import _convert_list_to_datatype, _convert_lxml_to_data, get_xpath_result, process_constraints, \
#    _expand_numeric_string,  expand_alpha_numeric_string, _replace_value, _get_temp_args, merge_dicts
import builtins
#
# TODO: This is a placeholder for UT's
#

class TestVerifyUtils(unittest.TestCase):
    def setUp(self):
        builtins.t = self
        t.log = MagicMock()

    def test_convert_str_to_num_or_bool(self):
        result = convert_str_to_num_or_bool([1,2])
        self.assertEqual(result, [1,2], "convert_str_to_num_or_bool for Non string input failed")

        result = convert_str_to_num_or_bool("Test")
        self.assertEqual(result, "Test", "convert_str_to_num_or_bool for string input failed")

        result = convert_str_to_num_or_bool("1")
        self.assertEqual(result, 1, "convert_str_to_num_or_bool for integer type string input failed")
        
        result = convert_str_to_num_or_bool("10.1")
        self.assertEqual(result, 10.1, "convert_str_to_num_or_bool for float type string input failed")

        result = convert_str_to_num_or_bool("True")
        self.assertEqual(result, True, "convert_str_to_num_or_bool for 'True' string input failed")

        result = convert_str_to_num_or_bool("False")
        self.assertEqual(result, False, "convert_str_to_num_or_bool for 'False' string input failed")


    def test_get_timestamp(self):
        result = get_timestamp()

    def test_convert_list_to_datatype(self):
        result = _convert_list_to_datatype({'a':1})
        self.assertEqual(result, {'a':1}, "convert_list_to_datatype for dict type input failed")

        result = _convert_list_to_datatype([1, "sample", "25", "5.5","False",{'a':1}])
        self.assertEqual(result, [1, "sample", 25, 5.5, False, {'a':1}], "convert_list_to_datatype for dict type input failed")

    def test_convert_lxml_to_data(self):
        input_data = etree.XML("<a>1</a>")
        result = _convert_lxml_to_data(input_data)
        self.assertEqual(result, [1], "convert_xml_to_data for not-list XML input failed")

        input_data = "test"
        result = _convert_lxml_to_data(input_data)
        self.assertEqual(result, ["test"], "convert_xml_to_data for not-list XML input failed")

        input_data =[etree.XML("<a>10</a>"), "string", etree.XML("<b>test</b>")] 
        result = _convert_lxml_to_data(input_data)
        self.assertEqual(result, [10, 'string', 'test'], "convert_xml_to_data for list of XML input failed")

        input_data = "test"
        result = _convert_lxml_to_data(input_data)
        self.assertEqual(result, ["test"], "convert_xml_to_data for not-list XML input failed")


    def test_extract_data(self):
        data = "test"
        result = extract_data(data=data, return_type="None")        
        self.assertEqual(result, "test", "extract_data for non-dict input failed")

        data = {'R0':{"check1":{"tag1":"value1"}}, 'R1':{"check2":{"tag2":"value2"}}}
        result = extract_data(data=data, return_type="None")
        self.assertEqual(result, {'R0':{"check1":{"tag1":"value1"}}, 'R1':{"check2":{"tag2":"value2"}}},\
                        "extract_data for 2 key dict input failed")

        data = {"check1":{"tag1":"value1"}}
        result = extract_data(data=data, return_type="None")        
        self.assertEqual(result, "value1", "extract_data for 2 level dict input failed")

        data = {'R1':{"check2":{"tag2":"value2"}}}
        result = extract_data(data=data, return_type="None")
        self.assertEqual(result, "value2", "extract_data for 3 level dict input failed")
       
        data = {'R1':{"check2":["value2"]}}
        result = extract_data(data=data, return_type="None")
        self.assertEqual(result, "value2", "extract_data for 2 level dict and with list input failed")

        data = {'R1':{"check2":["value1","value2"]}}
        result = extract_data(data=data, return_type="None")
        self.assertEqual(result, ["value1","value2"], "extract_data for 2 level dict and list with 2 values input failed")


    def test_get_xpath_result(self):
        xml_data = etree.XML("<root><child1>10</child1><child2>20<child3>30</child3></child2></root>")
        xml_path = "/root/child1"
        result = get_xpath_result(data=xml_data, xpath=xml_path)
        self.assertEqual(result, xml_data.xpath(xml_path), "get_xpath_result for single XML data input failed")

        xml_data = [etree.XML("<root><child1>10</child1></root>"),etree.XML("<root><child1>20</child1><child2>30</child2></root>")]
        xml_path = "/root/child1"
        result = get_xpath_result(data=xml_data, xpath=xml_path)
        self.assertEqual(result, [xml_data[0].xpath(xml_path)[0], xml_data[1].xpath(xml_path)[0]], "get_xpath_result for list of XML input failed")
       
        xml_data = ""
        xml_path = "/root/child1"
        result = get_xpath_result(data=xml_data, xpath=xml_path) 
        self.assertEqual(result, ['_NONE'], "get_xpath_result for empty data input failed")

        xml_data = etree.XML("<root><child1>10</child1></root>")
        xml_path = None
        result = get_xpath_result(data=xml_data, xpath=xml_path) 
        self.assertEqual(result, ['_NONE'], "get_xpath_result for non-existing xpath failed")

        xml_data = [etree.XML("<root><child1>10</child1></root>")]
        xml_path = '/root/child3'
        result = get_xpath_result(data=xml_data, xpath=xml_path)
        self.assertEqual(result, ['_NONE'], "get_xpath_result for non-existing xpath failed")


    def test_process_constraints(self):
        result = process_constraints(obtained_value=[2,4,1,3], expect_value=[1,2,3,4], opr="isequal[unordered]")
        self.assertEqual(result, ([1, 2, 3, 4], [1, 2, 3, 4], 'isequal', 'UNORDERED'), "process_constraints for unordered failed")
      
        result = process_constraints(obtained_value=3, expect_value=[3], opr="isequal[unordered]")
        self.assertEqual(result, ([3], [3], 'isequal', 'UNORDERED'), "process_constraints for unordered failed")       
     
        result = process_constraints(obtained_value="Test",expect_value="TEST", opr="isequal[ignorecase]")
        self.assertEqual(result, ("TEST", "TEST", 'isequal', 'IGNORECASE'), "process_constraints for ignorecase failed")

        result = process_constraints(obtained_value=['a','b','c'], expect_value=['A','c','B'], opr="isequal[unordered, ignorecase]")
        self.assertEqual(result, (['A','B','C'], ['A','B','C'], 'isequal', 'UNORDERED, IGNORECASE'),\
                                    "process_constraints for list of constraints failed")

        result = process_constraints(obtained_value="Test",expect_value="test", opr="isequal[lower()]")
        self.assertEqual(result, ("test", "test", 'isequal', 'LOWER()'), "process_constraints for function constraint failed")

        result = process_constraints(obtained_value="Test",expect_value="test", opr="isequal[dummy()]")
        self.assertEqual(result, ("Test", "test", 'isequal', 'DUMMY()'), "process_constraints for invalid function constraint failed")
      
        result = process_constraints(obtained_value="Test",expect_value="test", opr="isequal[loose]")
        self.assertEqual(result, ("Test", "test", 'isequal', 'LOOSE'), "process_constraints for loose|strict constraint failed")

        result = process_constraints(obtained_value="test  ",expect_value="test", opr="isequal[stripspace]")
        self.assertEqual(result, ("test", "test", 'isequal', 'STRIPSPACE'), "process_constraints for string stripspace constraint failed")

        result = process_constraints(obtained_value=["test  ",1],expect_value=["test",1], opr="isequal[stripspace]")
        self.assertEqual(result, (["test", 1],["test", 1], 'isequal', 'STRIPSPACE'), "process_constraints for string stripspace constraint failed")

        result = process_constraints(obtained_value="Test",expect_value="test", opr="isequal[constraints]")
        self.assertEqual(result, ("Test","test", 'isequal', 'CONSTRAINTS'), "process_constraints for unsupported constraint failed")

    def test_replace_with_case(self):
        data = {'Key1':"abc", "Key2":{"key3":"xyz"}}
        keywords = ["key1", "key3"]
        result = replace_with_case(data=data, keywords=keywords)
        self.assertEqual(result, {'key1': 'abc', 'Key2': {'key3': 'xyz'}}, "replace_with_case for nested dictionary failed")

        data = {'Key1':{"Key2":"xyz"}}
        keywords = ["key1", "key2"]
        result = replace_with_case(data=data, keywords=keywords)
        self.assertEqual(result, {'key1': {'key2': 'xyz'}}, "replace_with_case for single level dictionary failed")

    def test_get_yaml_data_as_dict(self):
        result = get_yaml_data_as_dict(filename='tests/unit/engines/verification/verify_utils_ut.yaml', keywords=['cmd','xpath'], yaml_file_data={})
        self.assertEqual(result,{'R0': {'ospf_interface_check': {'xpath': '/ospf-interface-information/ospf-interface', 'args': ['intf'], 'cmd': 'show ospf interface vat[‘intf’] detail', 'parameters': {'dead-interval': {'value': 20}, 'interface-type': {'value': 'LAN'}, 'hello-interval': {'value': 10}}}}}, "get_yaml_data_as_dict for yaml file in current directory failed")

        try:
            with patch("jnpr.toby.engines.verification.verify_utils.load") as patch_load:
                patch_load.side_effect = Exception('err')
                result = get_yaml_data_as_dict(filename='tests/unit/engines/verification/verify_utils_ut.yaml', keywords=['cmd','xpath'], yaml_file_data={})
        except Exception as exp:
            self.assertEqual(exp.args[0], 'err', "get_yaml_data_as_dict for load Exception case failed")
        
        try:
            import builtins
            with patch('builtins.open') as open_patch:
                open_patch.side_effect = Exception('err')
                result = get_yaml_data_as_dict(filename='tests/unit/engines/verification/verify_utils_ut.yaml', keywords=['cmd','xpath'], yaml_file_data={})
        except Exception as exp:
            self.assertEqual(exp.args[0], 'err', "get_yaml_data_as_dict for file open Exception case failed")

        with patch("jnpr.toby.engines.verification.verify_utils.os.path.isfile", side_effect = (False, True, False, False)):
            with patch("jnpr.toby.engines.verification.verify_utils.os.path.dirname", return_value =os.getcwd()):
                result = get_yaml_data_as_dict(filename='tests/unit/engines/verification/verify_utils_ut.yaml', keywords=['cmd','xpath'], yaml_file_data={})
                self.assertEqual(result,{'R0': {'ospf_interface_check': {'xpath': '/ospf-interface-information/ospf-interface', 'args': ['intf'], 'cmd': 'show ospf interface vat[‘intf’] detail', 'parameters': {'dead-interval': {'value': 20}, 'interface-type': {'value': 'LAN'}, 'hello-interval': {'value': 10}}}}}, "get_yaml_data_as_dict for yaml file existing in User defined path failed")

                result = get_yaml_data_as_dict(filename='tests/unit/engines/verification/verify_utils_ut.yaml', keywords=['cmd','xpath'], yaml_file_data={})
                self.assertEqual(result, False, "get_yaml_data_as_dict for yaml file does not exist in User defined path failed")
        

    def test_expand_numeric_string(self):
        result =  _expand_numeric_string('1-4,14,16,22-25')
        self.assertEqual(result, [1, 2, 3, 4, 14, 16, 22, 23, 24, 25] ,"_expand_numeric_string for numeric string failed")

        result =  _expand_numeric_string([1,2,3])
        self.assertEqual(result, [1, 2, 3] ,"_expand_numeric_string for list input failed")


    def test_expand_alpha_numeric_string(self):
        result =  expand_alpha_numeric_string('device1-3,1-3R,dut1')
        self.assertEqual(result, ['device1', 'device2', 'device3','1R', '2R', '3R', 'dut1'] ,\
                    "expand_alpha_numeric_string for alpha numeric input failed")

        result =  expand_alpha_numeric_string('')
        self.assertEqual(result, [] , "expand_alpha_numeric_string for empty input failed")

        result =  expand_alpha_numeric_string([1,2,3])
        self.assertEqual(result, [1,2,3] , "expand_alpha_numeric_string for non-alpha numeric input failed")

    def test_get_devices(self):
        result = get_devices("devices_<R0>")
        self.assertEqual(result, 'R0' , "get_devices for device details failed")

        result = get_devices("devices<R0>")
        self.assertEqual(result, False , "get_devices for getting False failed")


    def test_replace_value(self):
        result = _replace_value(main_data=[1,2,3], replace_data=1, key_to_change=2)
        self.assertEqual(result, [1,2,3] , "_replace_value for non-dict input failed")   
 
        result = _replace_value(main_data={'a':1, 'b':'2'}, replace_data='3', key_to_change='b')
        self.assertEqual(result, {'a':1, 'b':'3'} , "_replace_value for dict input failed")

    def test_get_temp_args(self):
        result = _get_temp_args(temp_args={'key1':'value1'})
        self.assertEqual(result, {'key1':'value1'} , "_get_temp_args for dict input failed")


        result = _get_temp_args(temp_args=[{'key1':'value1'},{'key2':'value2'},'key3'], default = "value")
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2','key3': None} , "_get_temp_args for list-of-dict input failed")

        try:
            result = _get_temp_args(temp_args=['a',['b']])
        except Exception as exp:
            self.assertEqual(exp.args[0],"wrong template arg format: ['a', ['b']]","_get_temp_args for wrong input format failed")

        try:
            result = _get_temp_args(temp_args="wrong input")
        except Exception as exp:
            self.assertEqual(exp.args[0],'wrong template arg format: wrong input','_get_temp_args for invalid input failed')

    def test_merge_dicts(self):
        result = merge_dicts(dict1={'key1': 'value1'}, dict2={'key1':'value2', 'key2':'value3'})
        self.assertEqual(result, {'key1': 'value2', 'key2':'value3'}, "merge_dicts for 2 dict values failed")

        result = merge_dicts(dict1={'key1', 'value1'}, dict2=['value2'])
        self.assertEqual(result, ['value2'], "merge_dicts for 2 dict values failed")
  

    def test_find_dict_data(self):
        result = find_dict_data(data={'a':{'b':{'c':'d'},'e':{'f':'g'}}}, key_list=['a','b'])
        self.assertEqual(result, ({'c': 'd'}, ['a', 'b']), "find_dict_data for first key occurence failed")

        result = find_dict_data(data={'a':{'b':{'c':'d'},'e':{'f':'g'}}}, key_list=['e','f'])
        self.assertEqual(result, ('g', ['a', 'e', 'f']), "find_dict_data for subkey input is failed")

    def test_get_key_value(self):
        result = get_key_value(data = None, key = 'a/b/c', message = "c value not found", if_false = 'False')
        self.assertEqual(result, None, "get_key_value for None data value failed")

        result = get_key_value(data = {'a':{'b':{'c':'d'}}}, key = None, message = "c value not found", if_false = 'False')
        self.assertEqual(result, None, "get_key_value for None key value failed")

        result = get_key_value(data = {'a':{'b':{'c':'d'}}}, key = 'a/b/c', message = "c value not found", if_false = 'False')
        self.assertEqual(result, 'd', "get_key_value for all valid input failed")

        result = get_key_value(data = {'a':{'b':{'c':'d'}}}, key = 'a/b/e', message = "c value not found", if_false = 'False')
        self.assertEqual(result, 'False', "get_key_value for invalid key value failed")

        result = get_key_value(data = {'a':{'b':{'c':'d'}}}, key = '/', message = "c value not found", if_false = 'False')
        self.assertEqual(result, 'False', "get_key_value for invalid key value failed")

    def test_find_key(self):
        result = find_key(dict_data={'a':{'b':{'c':'d'},'e':{'f':'g'}}}, search_key='f')
        self.assertEqual(result, ['a', 'e', 'f'], "get_key_value for invalid key value failed")


    def test_iterate_value(self):
        result = iterate_value(each_proto_data = {'iterate_until':{'interval':10, 'timeout':30},'iterate_for':{'interval':10, 'timeout':30}})
        self.assertEqual(result, (True, True, 1, 10.0, 30.0), "get_key_value for invalid key value failed")

        result = iterate_value(each_proto_data = {'iterate_until':{'interval':10, 'timeout':30}})
        self.assertEqual(result, (False, True, 1, 10.0, 30.0), "get_key_value for invalid key value failed")

    #def test_nested_set(self):
    #    result = nested_set(base={1:'a',2:'b'}, keys=[1,2,3], value='c')
    #    print ("======================", result)

    def test_expand_sub_testcases(self):
        result = expand_sub_testcases(testcase="Testcase1:[a,b,c]")
        self.assertEqual(result, "Testcase1:a,Testcase1:b,Testcase1:c", "expand_sub_testcases for sub testcase input failed")

        result = expand_sub_testcases(testcase="Testcase1")
        self.assertEqual(result, "Testcase1", "expand_sub_testcases for single testcase input failed")


if __name__ == '__main__':
    unittest.main()
