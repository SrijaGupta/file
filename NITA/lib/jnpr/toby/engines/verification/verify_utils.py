#!/usr/bin/env python
# coding=utf-8
# pylint: disable=locally-disabled,undefined-variable,too-many-branches,too-many-nested-blocks,eval-used,import-error,protected-access
import os
import re
import time
import datetime
import copy
import pprint
from statistics import mean
from yaml import load
import lxml
from jnpr.toby.utils.Vars import Vars
from jnpr.toby.logger.logger import get_log_dir
import ruamel.yaml
#from pykwalify.core import Core
# Check if string is representing int, float or boolean.
# If it is not string for ex. dict or list then don't do anything return as it is.
ROBOT = True
try:
    from robot.libraries.BuiltIn import BuiltIn
    BuiltIn().get_variable_value('${TRUE}')
except Exception:
    ROBOT = False


def convert_str_to_num_or_bool(input_str):
    """
    Converts  string type input to the coresponding data type.
    Example : '1' to 1
              '1.1' to 1.1
              'True' to True (boolean)
    :param input_str: takes string as input
    :return: return with typecast
    """
    if isinstance(input_str, str) is not True:
        return input_str

    # Checking if string is representing int.
    try:
        int(input_str)
        return int(input_str)
    except ValueError:

        # Checking if string is representing float.
        try:
            float(input_str)
            return float(input_str)
        except ValueError:

            # Checking if string is representing bool.
            if input_str == 'True':
                return True
            elif input_str == 'False':
                return False
            else:
                return input_str


def create_ve_debug_log(data, message):
    timestamp = datetime.datetime.now()
    failed_tc_file = open(get_log_dir()+'/VerifyDebug.log', 'a')
    failed_tc_file.write(str(timestamp)+"\t"+str(message)+"\n")
    failed_tc_file.write(
        "-------------------------------------------------------\n")
    pprint.pprint(data, failed_tc_file)
    failed_tc_file.write(
        "\n\n\n-------------------------------------------------------\n")
    failed_tc_file.close()


def get_timestamp():
    timestamp = time.time()
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d__%H:%M:%S')


def _convert_list_to_datatype(input_list):
    if not isinstance(input_list, list):
        return input_list
    for each_element in range(0, len(input_list)):
        input_list[each_element] = convert_str_to_num_or_bool(
            input_list[each_element])
    return input_list


def _convert_lxml_to_data(input_data):
    """
    Converts string or xml input to the coresponding data type
    Example : '1' to 1
              <tag>'1.1'</tag> to 1.1
              <tag>'True'</tag> to True (boolean)
    """
    temp_value = list()
    if isinstance(input_data, list):
        for each_input_data in input_data:
            try:
                if isinstance(each_input_data, lxml.etree._Element):
                    temp_value.append(
                        convert_str_to_num_or_bool(each_input_data.text))
                else:
                    temp_value.append(
                        convert_str_to_num_or_bool(each_input_data))
            except:
                t.log(level='info', message="NOT ABLE TO FIND THE TEXT ,RETURNING None")
                return None
    else:
        if isinstance(input_data, lxml.etree._Element):
            temp_value.append(
                convert_str_to_num_or_bool(input_data.text))
        else:
            temp_value.append(
                convert_str_to_num_or_bool(input_data))
    return temp_value


def _process_obtained_value_constraints(obtained_value, constraints):
    t.log(level="debug", message="Before applying obtained_value constraints..")
    t.log(level="debug", message="obtained_value:")
    t.log(level="debug", message=obtained_value)
    t.log(level="debug", message="constraints:")
    t.log(level="debug", message=constraints)

    constraints = str(constraints).split(',')

    for each_constraint in constraints:
        t.log(level="debug", message="Applying obtained_value constraint..")
        t.log(level="debug", message=each_constraint)
        is_supported = False
        each_constraint = each_constraint.strip()
        if str(each_constraint).upper() == 'MIN' and isinstance(obtained_value, list):
            obtained_value = _convert_list_to_datatype(
                copy.deepcopy(obtained_value))
            is_supported = True
            obtained_value = min(obtained_value)
        if str(each_constraint).upper() == 'MAX' and isinstance(obtained_value, list):
            obtained_value = _convert_list_to_datatype(
                copy.deepcopy(obtained_value))
            is_supported = True
            obtained_value = max(obtained_value)
        if str(each_constraint).upper() == 'AVG' and isinstance(obtained_value, list):
            obtained_value = _convert_list_to_datatype(
                copy.deepcopy(obtained_value))
            is_supported = True
            obtained_value = mean(obtained_value)
        if str(each_constraint).upper() == 'DELTA' and isinstance(obtained_value, list):
            is_supported = True
            obtained_value = obtained_value

        if is_supported is False:
            t.log(level='error', message="Unsupported Constraint : " + each_constraint)

    t.log(level="debug", message="After applying obtained_value constraints..")
    t.log(level="debug", message="obtained_value:")
    t.log(level="debug", message=obtained_value)

    return obtained_value


def process_constraints(obtained_value, expect_value, opr):
    """
    takes the operator with constraints and process the values according to
    the 1 or more constraints
    Example :
      Input : obtained_value : [2,1,3]
              expected_value : [1,2,3]
              oprerator : isequal[Unordered] ==> here isequal is operator and
                          unordered is constraint to neglect the order of values
      output: [1,2,3] [1,2,3] isequal unordered

      Input : obtained_value : "SAMPLE"
              expected_value : "sample"
              oprerator : isequal[ignorecase] ==> for case insensitive
      output: SAMPLE, SAMPLE, isequal, ignorecase

    :param obtained_value:
    :param expect_value:
    :param opr:
    :return: obtained_value , expect_value, opr, constarint
    """

    constraints_exist = re.search(r"^(.*)?\s*\[(.*)?\]", opr, re.I)
    t.log(level="debug", message="Before applying operator constraints..")
    t.log(level="debug", message="obtained_value:")
    t.log(level="debug", message=obtained_value)
    t.log(level="debug", message="expect_value:")
    t.log(level="debug", message=expect_value)
    t.log(level="debug", message="operator")
    t.log(level="debug", message=opr)
    opr_constraint = None
    if constraints_exist is not None:
        # for more than 1 constraints that are separated by comma (,)
        constraints = str(constraints_exist.group(2)).split(',')
        opr_constraint = constraints_exist.group(2).strip().upper()
        for each_constraint in constraints:
            t.log(level="debug", message="Applying operator constraint..")
            t.log(level="debug", message=each_constraint)
            is_supported = False
            constraint_fail = False
            each_constraint = each_constraint.strip()
            # for unordered constraint sort both values to compare without considering the order
            if str(each_constraint).upper() == 'UNORDERED' and isinstance(expect_value, list):
                expect_value = _convert_list_to_datatype(
                    copy.deepcopy(expect_value))
                is_supported = True
                if isinstance(obtained_value, list):
                    obtained_value.sort()
                else:
                    # If obtained value is not a list , make it as a list
                    temp_obtained_value = obtained_value
                    obtained_value = list()
                    obtained_value.append(temp_obtained_value)
                expect_value.sort()
            # For ignorecase constraint convert both values to upper case
            if str(each_constraint).upper() == 'IGNORECASE':
                is_supported = True
                if isinstance(expect_value, str):
                    expect_value = expect_value.upper()
                if isinstance(obtained_value, str):
                    obtained_value = obtained_value.upper()
                # incase of list of values convert each element to upper
                if isinstance(expect_value, list):
                    for each_val in range(0, len(expect_value)):
                        if isinstance(expect_value[each_val], str):
                            expect_value[each_val] = expect_value[each_val].upper()
                if isinstance(obtained_value, list):
                    for each_val in range(0, len(obtained_value)):
                        if isinstance(obtained_value[each_val], str):
                            obtained_value[each_val] = obtained_value[each_val].upper(
                            )

            # for constraint to be a function .. ex: isequal[upper()] apply the
            # function on obtained value
            if re.search(r'.*\(.*\)', str(each_constraint)) is not None:
                is_supported = True
                try:
                    program = "obtained_value = " + \
                        "obtained_value." + str(each_constraint)
                    local = locals()
                    exec(program, globals(), local)
                    obtained_value = local['obtained_value']
                except Exception as ecp:
                    t.log(level='error', message="Unable to execute " + each_constraint +
                          "on obtained_value")
                    t.log(level='info', message=ecp)
            if str(each_constraint).upper() == 'LOOSE' or str(each_constraint).upper() == 'STRICT':
                is_supported = True

            # For constraint which neglects space in the values, strips white space in both values
            if str(each_constraint).upper() == 'STRIPSPACE':
                is_supported = True
                if isinstance(obtained_value, str):
                    obtained_value = obtained_value.strip()
                elif isinstance(obtained_value, list):
                    for index in range(0, len(obtained_value)):
                        if isinstance(obtained_value[index], str):
                            obtained_value[index] = obtained_value[index].strip()
                        else:
                            constraint_fail = True
                    if constraint_fail:
                        t.log(level="debug", message="The operator constraint STRIPSPACE"
                                                     "cannot be applied to integer "
                                                     "outputs from DUT.")
            # acceptnone constraint ensures negative testing passes if obtained value is none
            if str(each_constraint).upper() == 'ACCEPTNONE':
                is_supported = True

            if is_supported is False:
                t.log(level='error',
                      message="Unsupported Constraint : " + each_constraint)

        opr = constraints_exist.group(1).strip()

        t.log(level="debug", message="After applying all operator constraints..")
        t.log(level="debug", message="obtained_value:")
        t.log(level="debug", message=obtained_value)
        t.log(level="debug", message="expect_value:")
        t.log(level="debug", message=expect_value)
        t.log(level="debug", message="operator")
        t.log(level="debug", message=opr)

    return obtained_value, expect_value, opr, opr_constraint


def extract_data(data, return_type):
    """
    To extract data from the dictionary which is generated from yaml file
    :param data: dictionary as input
    :param return_type: type of the return value
    :return: return if only one key present in hierarchy then single value will be return
                    otherwise entire dictionary will be returned.
    """
    t.log(level="debug", message="extract data input :")
    t.log(level="debug", message=data)
    # If not dictionary return data as it is.
    if not isinstance(data, dict):
        if return_type.lower() == 'list':
            if isinstance(data, list):
                return data
            else:
                return [data]
        else:
            return data
    value = 0
    while value < 2:
        if isinstance(data, dict):

            dict_keys = list(data.keys())

            # If number of keys are more than 1 than return entire dictionary.
            if len(dict_keys) > 1 or len(dict_keys) == 0:
                if return_type.lower() == 'list':
                    if isinstance(data, list):
                        return data
                    else:
                        return [data]
                else:
                    return data

            # If only one key then get one level inside data.
            data = data[dict_keys[0]]
            value = value + 1

    if not isinstance(data, dict) and not isinstance(data, list):
        if return_type.lower() == 'list':
            if isinstance(data, list):
                return data
            else:
                return [data]
        else:
            return data

    # List contains a single non dictionary element then return only that element start.
    if isinstance(data, list) and len(data) == 1:
        if not isinstance(data[0], dict):
            return data if return_type.lower() == 'list' else data[0]

    # List or Dictionary contains more than one element then return only that element.
    if len(data) == 1 and isinstance(data, dict):
        dict_keys = list(data.keys())
        data = data[dict_keys[0]]
        #return {dict_keys[0]: data} if return_type.lower() == 'dict' else data
        if return_type.lower() == 'dict':
            return {dict_keys[0]: data}
        elif return_type.lower() == 'list':
            if isinstance(data, list):
                return data
            else:
                return [data]
        else:
            return data        

    return data

# Execute xpath on the xml data and return result.
def get_xpath_result(data, xpath):
    """
    Execute the xpath expression on data and return the result
    :param data: xml data from the command execution
    :param xpath: xpath expression
    :return: evaluated xpath result
    """
    # Executing xpath on data.

    return_xpath = []
    try:
        # For list of xml data input apply xpath for every list element
        if isinstance(data, list):
            for each_element in data:
                if isinstance(each_element, lxml.etree._Element):
                    return_xpath.extend(each_element.xpath(xpath))
        else:
            if isinstance(data, lxml.etree._Element) or isinstance(data, lxml.etree._ElementTree):
                return_xpath.append(data.xpath(xpath))
            else:
                return ['_NONE']
    except lxml.etree.XPathEvalError as err:
       t.log(level="error", message="Error occured during XPath evaluation. Please check your Xpath." + 
              str(xpath) + " :--")
       return ['_NONE']
    except Exception as err:
        t.log(level="error", message="Exception occured during execution of xpath " +
              str(xpath) + " :--")
        t.log(level="error", message=str(err))
        return ['_NONE']
    if len(return_xpath) == 0:
        t.log(level="debug", message="\tpath:" + xpath +
              "\nELEMENT XPATH IS NOT RETURNING ANYTHING ,PLEASE CHECK CMD AND XPATH")
        return ['_NONE']
    t.log(level="debug", message="xpath result :")

    if len(return_xpath) == 1:
        # t.log(level="debug", message=tostring(xpath_results[0]))
        return return_xpath[0]

    else:
        # t.log(level="debug", message=tostring(xpath_results))
        return return_xpath


def replace_with_case(data, keywords):
    """
    Used to make case-insensitive Verification Engine keywords in verify yaml file.
    Example : CMD : ""
              Cmd : ""
              cmd : ""
    All 3 keys for specifying the command is valid as we convert them into lowercase
    using this function

    :param data : dictionary generated from yaml file
    :param keywords : keys to be converted to lowercase
    :return : data with the specified keys converted into lowercase
    """

    if isinstance(data, dict):
        data_keys = list(data.keys())
        for each in data_keys:
            if each.lower() in keywords:
                data[each.lower()] = data.pop(each)

                # If nested dictionary presents change the case of nested dictionary.
                if isinstance(data[each.lower()], dict):
                    replace_with_case(data[each.lower()], keywords)
            else:
                # If nested dictionary presents change the case of nested dictionary.
                if isinstance(data[each], dict):
                    replace_with_case(data[each], keywords)
        return data


def get_yaml_data_as_dict(filename, keywords, yaml_file_data=None):
    """
    load the yaml and return the case-insensitivity data dictionary from yaml
    :param filename: yaml file name
    :param keywords: keys to be converted into lowercase
    :param yaml_file_data: dict to store the yaml data load and reuse
    :return: case-insensitivity data dictionary
    """
    # if file not in current directory check in user defined path.
    if not os.path.isfile(filename):
        # check the file in the path specified in global variable SUITE_SOURCE
        src_path = "./"
        if ROBOT:
            src_path = os.path.dirname(
                Vars().get_global_variable('${SUITE_SOURCE}'))
        if os.path.isfile(os.path.join(src_path, filename)):
            filename = os.path.join(src_path, filename)
        else:
            t.log(level='info', message="FILE PATH \"" + filename + "\" NOT FOUND")
            return False

    t.log(level="info", message="FILE NAME AFTER SUITE_SOURCE:..")
    t.log(level="info", message=filename)

    try:
        # open the yaml file and load data to dictionary
        if yaml_file_data and filename in yaml_file_data and (str(os.path.basename(filename)) not in ['tmp_jvision_data.yaml', 'tmpdata.yaml', 'userdata.yaml']):
            t.log(level="debug",message="Using the loaded yaml dict as its same file being used")
            t.log(level="debug", message="File name which is getting re-used is :" + str(filename))
            return yaml_file_data[filename]
        else:
            with open(filename, 'r') as stream:
                try:
                    file_data = ruamel.yaml.load(stream, Loader=ruamel.yaml.RoundTripLoader)
                    # convert the keywords to lowercase
                    file_lower_data = replace_with_case(file_data, keywords)
                    if yaml_file_data is not None:
                        yaml_file_data[filename] = file_lower_data
                    return file_lower_data
                except Exception as exc:
                    t.log(level='error', message=exc)
                    t.log(level="error", message=
                        " FILE " + filename+" NOT IN YAML FORMAT , MAKE SURE FILE IS IN YAML FORMAT")
                    return False
    except Exception as exc:
        t.log(level='info', message=exc)
        t.log(level='info', message="FILE NAME " + filename + " NOT FOUND")
        return False


def _expand_numeric_string(input_str):
    """
    Expand the string and return list
    Eg. input_str = '1-4,14,16,22-25'
        output    = [1, 2, 3, 4, 14, 16, 22, 23, 24, 25]
    """
    if isinstance(input_str, str):
        expanded_list = []
        for i in input_str.split(','):
            if '-' not in i:
                expanded_list.append(int(i))
            else:
                left_part, right_part = list(map(int, i.split('-')))
                expanded_list += list(range(left_part, right_part + 1))
        return expanded_list
    else:
        return input_str


def expand_alpha_numeric_string(input_str):
    """
    takes the string and expand to list of values
    Used for device value expand and a interface value expand
    :param input_str:
    :return:
    Eg. input_str = 'device1-3,dut10-14, 1-3R'
        output = [device1, device2, device3, dut10, dut11, dut12, dut13, dut14, 1R, 2R, 3R]
    """
    output_range_list = []

    # If input is empty return empty list.
    if not isinstance(input_str, str):
        return input_str
    if input_str is None or input_str == '':
        return output_range_list
    splitted_range_list = input_str.split(",")

    for each_token_range_list in splitted_range_list:

        # Checking for number-number pattern.
        # Eg. will match 1-3, 24-28.
        result = re.search(r"\d+\-\d+", each_token_range_list)
        if result:
            # Extracting number-number pattern.
            actual_range = result.group(0)

            initial_range_len = len(output_range_list)

            # new output list with increased size after expanding number-number pattern.
            output_range_list = output_range_list + \
                _expand_numeric_string(actual_range)

            # Attaching word to the range start.
            for each_range_item in range(initial_range_len, len(output_range_list)):
                output_range_list[each_range_item] = each_token_range_list[:result.start()] + str(
                    output_range_list[each_range_item]) + each_token_range_list[result.end():]
                # Attaching word to the range end.
        else:
            # No match for number-number pattern. Just append the string as it is.
            output_range_list = output_range_list + [each_token_range_list]

    # converting all items to string for the safe side.
    output_range_list = list(map(str, output_range_list))
    return output_range_list


def get_devices(input_str):
    """
    decide the the testcase is device centric or protocol centric
    :param input_str:
    :return:False if protocol centric else return the device list
    """
    var = re.search(r'devices_\s*<(.*)>', input_str, re.I)
    if var:
        return var.group(1)
    else:
        return False


def _replace_value(main_data, replace_data, key_to_change):
    """
    Replace the dict key-value with new value
    """
    if not isinstance(main_data, dict):
        return main_data
    for key in list(main_data.keys()):
        if key == key_to_change:
            main_data[key] = replace_data
    return main_data


def _get_temp_args(temp_args=None, default=None):
    """
    internal function to get template args in list/dict , and turn them into a dict
    Example : [{'a':1},{'b':2},{'c':3}] to {'a':1, 'b':2, 'c':3}
              [{'a':1},'b','c'] to {'a':1, 'b':None, 'c':None}
    """
    arg_dict = {}
    # if args is dict type return it
    if isinstance(temp_args, dict):
        return temp_args
    # for list of args process each element
    elif isinstance(temp_args, list):
        for arg in temp_args:
            # for dict in list update it into new dictionary value
            if isinstance(arg, dict):
                arg_dict.update(arg)
            # for string in the list, convert string as key and add None as value
            elif isinstance(arg, str):
                if default is not None:
                    # get all args from template, even if not assigned yet
                    arg_dict[arg] = None
            else:
                raise Exception('wrong template arg format: ' + str(temp_args))
    else:
        raise Exception('wrong template arg format: ' + str(temp_args))

    return arg_dict


def merge_dicts(dict1, dict2):
    """
    Recursively merges dict2 into dict1
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict2
    for k in dict2:
        if k in dict1:
            dict1[k] = merge_dicts(dict1[k], dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1


def find_dict_data(data=None, key_list=None, path=None):
    """
    used internally to dynamically retrieve t_vars from t dictionary
    the key_list can be a subset of the complete tree that traverse
    from root to the leaf value, as long as the list is unique, this makes
    the dynamic t_var expression concise.
    """
    # Path initialization.
    if path is None:
        path = []
    value = None
    test_keys = copy.deepcopy(key_list)
    first_key = test_keys[0]
    # if the first key specified in test_keys present in data , add the key into path list
    if first_key in data.keys():
        path.append(test_keys.pop(0))
        # for more than 1 key in test_keys make recursive call
        if len(test_keys) > 0:
            if isinstance(data, dict):
                value, path = find_dict_data(data=data[first_key],
                                             key_list=test_keys, path=path)
                # if value != None:
                # find it
                # return value, path
        else:
            # find it.
            # return data[first_key], path
            value = data[first_key]
    # if the first key not present in the data, check the subkeys
    else:
        for subkey in data.keys():
            if isinstance(data[subkey], dict):
                path.append(subkey)
                value, path = find_dict_data(data=data[subkey],
                                             key_list=test_keys, path=path)
                if value is None:
                    path.pop()
                else:
                    # find it
                    break

    return value, path


def get_key_value(data=None, key=None, message=None, if_false=None):
    """
    Get the value from dictionary using the key path
    :param data: dict data
    :param key: path to get the data
    :param message: If Fail ,Message to show
    :param if_false: if_false what to return
    :return:
    """
    if data is None:
        t.log(level='info', message="DATA IS MANDATORY")
        return None
    if key is None:
        t.log(level='info', message="KEY IS MANDATORY")
        return None

    obtain_data = [None]

    try:
        if isinstance(data, dict):
            obtain_data = find_dict_data(
                data=data, key_list=key.split('/'))
    except KeyError:
        t.log(level='info', message="Exception: KEY NOT FOUND," + message)
        return if_false
    if obtain_data[0] is None:
        t.log(level='debug', message="Searching for the keyword " + key + " " + message)
        return if_false
    t.log(level="debug", message="Searching for the keyword: " + key + " - FOUND")
    return obtain_data[0]


def find_key(dict_data, search_key):
    """
    Get the path of search_key in dictionary d
    :param dict_data: dict data
    :param search_key: key to search
    :return: list containing path to the search_key in dictionary.
    """
    if isinstance(dict_data, dict):
        for key, val in dict_data.items():
            if key == search_key:
                return [key]
            if isinstance(val, dict):
                temp_key = find_key(val, search_key)
                if temp_key:
                    return [key] + temp_key


def iterate_value(each_proto_data):
    """
    Gets "iterate for" and "iterate until" details from data dictionary.
    iterate for :  iteration stops when you get the expected value or timeout.
    iterate until : iteration stops when you don't get the expected value or timeout.

    :param each_proto_data : data dictionary
    ;return : details of iterate for and iterate until
    """
    # Itereate for
    is_until_for_present = False

    # Iterate until
    is_until_present = False
    it_count = 0
    interval = None
    timeout = None
    if isinstance(each_proto_data, dict):
        proto_data_keys = list(each_proto_data.keys())
        # If iterate_until or iterate_for is present update the statistics.
        if 'iterate_until' in proto_data_keys or 'iterate_for' in proto_data_keys:
            # if iterate for present in data,  get its values
            if 'iterate_for' in proto_data_keys:
                is_until_for_present = True
                interval = float(
                    each_proto_data['iterate_for']['interval'])
                timeout = float(each_proto_data['iterate_for']['timeout'])
            # if iterate unitl presents , process the data and get its values
            else:
                interval = float(
                    each_proto_data['iterate_until']['interval'])
                timeout = float(
                    each_proto_data['iterate_until']['timeout'])
            it_count = 1
            is_until_present = True
    return is_until_for_present, is_until_present, it_count, interval, timeout


def nested_set(base, keys, value, append=False):
    """
    set a leaf node value with list of nested keys in a dict

    :param base:
    :param keys:
    :param value:
    :param append:
    """

    for key in keys[:-1]:
        base = base.setdefault(key, {})
    if keys[-1] not in base:
        base[keys[-1]] = value
    elif append:
        if not isinstance(base[keys[-1]], list):
            base[keys[-1]] = [base[keys[-1]]]
        if isinstance(value, list):
            base[keys[-1]].extend(value)
        else:
            base[keys[-1]].append(value)
    else:
        base[keys[-1]] = value


def expand_sub_testcases(testcase):
    """
    Expands the subcases specified in the testcase.
    Example
    Input : Testcase1:[subTC1,subTC2,subTC3]
    output : Testcase1:subTC1, Testcaes1:subTC2, Testcase1:subTC3

    :params testcase: testcase name with/without sub testcases
    :return : expanded sub testcases names
    """
    var = re.search(r'([^,]*?\:)\[(.*)?\]', testcase)
    sub_testcases = []
    if var is not None:
        # get sub testcase names from regex group
        sub_tcs = var.group(2).split(',')
        for testcase in sub_tcs:
            # Expand the sub testcase name by adding it with testcase name
            sub_testcases.append(var.group(1)+testcase.strip("'\" "))
        testcases = ""
        # Convert the sub testcase name list into a string
        for testcase in sub_testcases:
            if testcases == "":
                testcases = testcase
            else:
                testcases = testcases + "," + testcase
        return testcases
    else:
        return testcase


def get_valid_xpaths(data, xpath_list):

    return_xpath = []
    # if not (isinstance(data,lxml.etree._Element) or isinstance(data,lxml.etree._ElementTree)):
    #    t.log("\'data\' argument should be etree instance(Element or ElementTree) in _get_valid_xpaths")
    #    return []
    for each_xpath in xpath_list:
        try:
            xpath_result = data.xpath(each_xpath)
        except:
            xpath_result = ['_NONE']
        if len(xpath_result) != 0:
            return_xpath.append(each_xpath)
    return return_xpath
