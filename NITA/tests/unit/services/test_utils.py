#!/usr/local/bin/python3

import sys

import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values



import builtins
builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

from jnpr.toby.services import utils


class TestUtils(unittest.TestCase):


    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
        # utils.log = t.log
    # #Passed
    def test_utils_get_reg_ex_ip_address(self):
        self.assertEqual(utils.get_regex_ip(), '(?:(?:(?:[A-Fa-f\d]{0,4}:{1,2}?){2,7}(?:(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|[A-Fa-f\d]{0,4})?)|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))')

    def test_utils_get_regex_if(self):
        self.assertEqual(utils.get_regex_if(), r'(?:\b(?:\w+-\d+\/\d+\/|em|irb|as|ae|rlsq|rsp|fxp|gre|ipip|reth|lo|vlan|psgr|pimd|pime|pip0|pp0|tap)\d*(?::\d+)?(?:\.\d+)?)')

    def test_utils_cmp_dicts(self):
        self.assertEqual(utils.cmp_dicts({'min__a':10, 'max__b':10, 'neg__d': -10, 'c': 'abc', 'f':10}, {'a':10, 'b': 20, 'd': 10, 'c': 'abc'}, exact=True, tol_perc=1, tol_val=1), False)

    def test_utils_cmp_dicts_non_exact(self):
        self.assertEqual(utils.cmp_dicts({'min__a':10, 'max__b':10, 'neg__d': -10, 'c': 'abc', 'f':10}, {'a':10, 'b': 20, 'd': -20, 'c': 'abc'}, tol_perc=1, tol_val=1), False)

    def test_utils_cmp_dicts_plain(self):
        self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc', 'f':10 , 'd': None}, {'k':10, 'd': -20, 'c': 'abc'}, tol_perc=1, tol_val=1), False)

    @patch('jnpr.toby.services.services.iputils.cmp_ip')
    @patch('jnpr.toby.services.services.iputils.is_ip')
    def test_utils_cmp_dicts_ip(self, is_ip_patch, cmp_ip_patch):
        is_ip_patch.return_value = True
        cmp_ip_patch.return_value = True
        self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc', 'f':10 , 'd': None}, {'k':10, 'd': -20, 'c': 'abc'}, tol_perc=1, tol_val=1), False)

    def test_utils_cmp_dicts_plain_no_tolerance(self):
        self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc'}, {'k':10, 'd': -20, 'c': 'abc'}), True)

    def test_utils_cmp_dicts_plain_no_tolerance_exact(self):
        self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc'}, {'k':10, 'd': -20, 'c': 'abc'}, exact=True), False)

    def test_utils_cmp_dicts_plain_no_tolerance_exact(self):
        self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc', 'f':10}, {'k':10, 'd': -20, 'c': 'abc'}, exact=True), False)

    def test_utils_cmp_dicts_plain_no_tolerance_exact(self):
         self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc', 'f':10}, {'k':10, 'd': -20, 'c': 'abc', 'f': 9}, exact=True), False)

    def test_utils_cmp_dicts_exp_data_exception(self):
        self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc', 'f':10}, {'k':10, 'd': -20, 'c': 'abc', 'f': 9}, exact=True), False)
        with self.assertRaises(Exception) as context:
            utils.cmp_dicts({}, {})
        self.assertTrue("exp_data is not defined" in str(context.exception))

    def test_utils_cmp_dicts_act_data_exception(self):
        self.assertEqual(utils.cmp_dicts({'k':10, 'c': 'abc', 'f':10}, {'k':10, 'd': -20, 'c': 'abc', 'f': 9}, exact=True), False)
        with self.assertRaises(Exception) as context:
            utils.cmp_dicts({'1':1}, {})
        self.assertTrue("act_data is not defined" in str(context.exception))

    def test_utils_cmp_val_missing_act_val(self):
        self.assertEqual(utils.cmp_val(10, None), False)

    def test_utils_cmp_val_both_None(self):
        self.assertEqual(utils.cmp_val(None, None), True)

    def test_utils_cmp_val_tol_perc_if(self):
        self.assertEqual(utils.cmp_val(10, 12, tol_perc=10), False)

    def test_utils_cmp_val_tol_perc_else(self):
        self.assertEqual(utils.cmp_val(10, 10, tol_perc=10), True)

    def test_utils_cmp_val_tol_val_if(self):
        self.assertEqual(utils.cmp_val(10, 12, tol_val=1), False)

    def test_utils_cmp_val_tol_val_else(self):
        self.assertEqual(utils.cmp_val(10, 10, tol_val=1), True)

    def test_utils_cmp_val_final_if(self):
        self.assertEqual(utils.cmp_val(10, 12), True)

    def test_utils_cmp_val_final_else(self):
        self.assertEqual(utils.cmp_val(10, 9), False)

    def test_utils_get_val(self):
        self.assertEqual(utils.update_data_from_output({},{'a':10}, {'a':20}), None)

    def test_utils_get_arg_vals(self):
        self.assertEqual(isinstance(utils.update_opts_from_args({'b':'20', 'a':10} ,{'a':10}), dict), True)

    # def test_utils_shift_args_val(self):
        # self.assertEqual(utils.shift_args_val({'a':10}, 'a'), 10)

        # Passed
    def test_utils_log_exception(self):
        with self.assertRaises(Exception) as context:
            utils.log()
        self.assertTrue("Issued 'log' without arguments. t.log() Requires min 1 argument" in str(context.exception))
    # Passed
    def test_utils_log_level_none(self):
        self.assertEqual(utils.log('Message'), None)
    # Passed
    def test_utils_log(self):
        self.assertEqual(utils.log('INFO', 'Message'), None)

    def test_get_time_diff(self):
        self.assertEqual(utils.get_time_diff('2011-10-31 04:46:04', '2011-10-31 04:48:34'), 150.0)





if __name__ == '__main__':
    unittest.main()
