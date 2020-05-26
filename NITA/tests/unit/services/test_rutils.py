#!/usr/local/bin/python3

import sys

import mock
import builtins
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values
from collections import defaultdict

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

from jnpr.toby.services.rutils import rutils

class TestRutils(unittest.TestCase):


    def setUp(self):
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
        self.rutils = rutils(test=None)
        builtins.t = MagicMock()
        # self.log = t.log
    # # #Passed
    # def test_rutils_log(self):
    # 	self.assertEqual(self.rutils.log(), None)

    def test_rutils_get_intf_list_in_path_missing_args(self):
    	self.rutils.log = MagicMock()
    	with self.assertRaises(Exception) as context:
    		self.rutils.get_intf_list_in_path()
    	self.assertTrue('Missing mandatory argument, intf' in str(context.exception))

    def test_rutils_get_intf_list_in_path(self):
    	self.rutils.log = MagicMock()
    	self.rutils.topo = {}
    	self.rutils.topo['intf'] = {}
    	self.rutils.topo['intf']['eth1'] = {}
    	self.rutils.topo['intf']['eth1']['path'] = 'path_1'
    	self.rutils.topo['path'] = {}
    	self.rutils.topo['path']['path_1'] = 'path_1'
    	self.assertEqual(self.rutils.get_intf_list_in_path(intf='eth1'), 'path_1')

    def test_rutils_parse_topo_missing_args(self):
        self.rutils.log = MagicMock()
        with self.assertRaises(Exception) as context:
            self.rutils.parse_topo()
        self.assertTrue('Missing mandatory argument, pkt_path' in str(context.exception))

    # def test_rutils_parse_topo(self):
    # 	self.rutils.log = MagicMock()
    # 	dd = {}
    # 	dd = lambda:defaultdict(dd)
    # 	self.rutils.dd = MagicMock()
    # 	self.rutils.return_value = dd()
    # 	builtins.t = {}
    # 	t = {}
    # 	t['resources'] = {}
    # 	for res in ['H0', 'R0' , 'H1']:
    # 		for intf in ['path1_eth1', 'eth2']:
    # 			t['resources'][res] = {}
    # 			t['resources'][res]['interfaces'] = {}
    # 			t['resources'][res]['interfaces'][intf] = {}
    # 			t['resources'][res]['interfaces'][intf]['link'] = 'path1_eth1'

    # 	print(t)
    # 	self.assertEqual(self.rutils.parse_topo(['H0', 'R0' , 'H1']), True)

    def test_rutils_parse_topo(self):
        builtins.t = MagicMock()
        self.rutils.log = MagicMock()
        t.get_interface_list = MagicMock()
        t.get_interface_list.return_value = ['h0r0_1_if']
        t.get_interface = MagicMock()
        t.get_interface.return_value = {'link': 'path1_connect1', 'type': ['eth', 'ether'], 'pic': 'eth1', 'name': 'eth1', 'uv-ip': '20.1.1.2/24', 'management': 0}
        self.assertEqual(self.rutils.parse_topo(['h0', 'r0' , 'h1']), True)

    def test_rutils_parse_topo_tohit_contnue(self):
        self.rutils.log = MagicMock()
        t.get_interface_list = MagicMock()
        t.get_interface_list.return_value = ['h0r0_1_if']
        t.get_interface = MagicMock()
        t.get_interface.return_value = {'link': 'connect1', 'type': ['eth', 'ether'], 'pic': 'eth1', 'name': 'eth1', 'uv-ip': '20.1.1.2/24', 'management': 0}
        self.assertEqual(self.rutils.parse_topo(
            ['h0', 'r0', 'h1']), True)
         # # Passed
    def test_rutils_get_tg_port_pairs(self):
        self.rutils.log = MagicMock()
        self.rutils.topo['path'] = {'path1':['h0:h0r0_1_if', 'h1:h1r0_1_if'] }
        self.assertEqual(self.rutils.get_tg_port_pairs(), [
                         ['h0:h0r0_1_if', 'h1:h1r0_1_if']])

    def test_rutils_set_resource_exception(self):
        self.rutils.log = MagicMock()
        with self.assertRaises(Exception) as context:
            self.rutils.set_resource()
        self.assertTrue('Missing mandatory argument, resource' in str(context.exception))

    def test_rutils_set_resource(self):
        self.rutils.log = MagicMock()
        # with self.assertRaises(Exception) as context:
            # self.rutils.set_resource()
        # self.assertTrue('Missing mandatory argument, resource' in str(context.exception))
        # self.dh = Values()
        # self.dh.cli = Values()
        # self.dh.cli.response = MagicMock()
        # self.dh.cli.response.return_value = True
        t.get_handle = MagicMock()
        t.get_handle.return_value = True
        self.assertEqual(self.rutils.set_resource(resource='abc'), True)

    def test_rutils_init_set_resource_false(self):
    	self.rutils.log = MagicMock()
    	self.rutils.set_resource = MagicMock()
    	self.rutils.set_resource.return_value = False
    	self.assertEqual(self.rutils.init(), False)

    def test_rutils_init_parse_topo_false(self):
    	self.rutils.log = MagicMock()
    	self.rutils.set_resource = MagicMock()
    	self.rutils.set_resource.return_value = True
    	self.rutils.parse_topo = MagicMock()
    	self.rutils.parse_topo.return_value = False

    	self.assertEqual(self.rutils.init(), False)

    def test_rutils_init_true(self):
    	self.rutils.log = MagicMock()
    	self.rutils.set_resource = MagicMock()
    	self.rutils.set_resource.return_value = True
    	self.rutils.parse_topo = MagicMock()
    	self.rutils.parse_topo.return_value = True

    	self.assertEqual(self.rutils.init(), True)

    def test_rutils_get_cli_output_exception(self):
        self.rutils.log = MagicMock()
        with self.assertRaises(Exception) as context:
            self.rutils.get_cli_output()
        self.assertTrue('Missing mandatory argument, cmd_list' in str(context.exception))

    def test_rutils_get_cli_output(self):
        self.rutils.log = MagicMock()
        # with self.assertRaises(Exception) as context:
            # self.rutils.get_cli_output()
        # self.assertTrue('Missing mandatory argument, resource' in str(context.exception))
        test = Values()
        test.response = MagicMock()
        test.response.return_value = True
        self.rutils.dh = Values()
        self.rutils.dh.cli = MagicMock()
        self.rutils.dh.cli.return_value = test

        # self.rutils.dh.cli.response = MagicMock()
        # self.rutils.dh.cli.response.return_value = True
        # t.get_handle = MagicMock()
        # t.get_handle.return_value = True
        self.assertEqual(self.rutils.get_cli_output(cmd='abc'), True)

    def test_rutils_get_xml_output(self):
        self.rutils.log = MagicMock()
        test = Values()
        test.response = MagicMock()
        self.rutils.dh = Values()
        self.rutils.dh.cli = MagicMock()
        self.rutils.dh.cli.return_value = test
        xml_tree = {}
        xml_tree['rpc-reply'] = {'a' : { 'b': [1,2,3]}}
        # xml_tree['a'] = {}
        # xml_tree['a']['b'] = [1,2,3]
        test.response.return_value = xml_tree
        self.rutils.xml = Values()
        self.rutils.xml.xml_string_to_dict = MagicMock()
        self.rutils.xml.xml_string_to_dict.return_value = xml_tree
        self.assertEqual(self.rutils.get_xml_output(xpath='a/b', want_list=True), [1, 2, 3])

    def test_rutils_get_xml_output_want_list_false(self):
        self.rutils.log = MagicMock()
        test = Values()
        test.response = MagicMock()
        self.rutils.dh = Values()
        self.rutils.dh.cli = MagicMock()
        self.rutils.dh.cli.return_value = test
        xml_tree = {}
        xml_tree['rpc-reply'] = {'a' : { 'b': [1,2,3]}}
        # xml_tree['a'] = {}
        # xml_tree['a']['b'] = [1,2,3]
        test.response.return_value = xml_tree
        self.rutils.xml = Values()
        self.rutils.xml.xml_string_to_dict = MagicMock()
        self.rutils.xml.xml_string_to_dict.return_value = xml_tree
        self.assertEqual(self.rutils.get_xml_output(xpath='a/b'), [1, 2, 3])

    def test_rutils_get_fpc_pic_port_from_ifname(self):
        self.assertEqual(self.rutils.get_fpc_pic_port_from_ifname(intf='ms-1/2/0'), ('1', '2', '0'))

    def test_rutils_get_fpc_pic_from_ifname(self):
        self.rutils.get_fpc_pic_port_from_ifname =MagicMock()
        self.rutils.get_fpc_pic_port_from_ifname.return_value = ('1', '2', '0')

        self.assertEqual(self.rutils.get_fpc_pic_from_ifname(intf='ms-1/2/0'), ('1', '2'))


    @patch(builtin_string + '.open')
    def test_rutils_load_set_cfg(self, test_patch):
    	self.rutils.log = MagicMock()
    	test = Values()
    	test.writelines = MagicMock()
    	test.close = MagicMock()
    	test_patch.return_value = test
    	self.rutils.log = MagicMock()
    	self.rutils.dh = Values()
    	self.rutils.dh.load_config = MagicMock()
    	self.rutils.dh.load_config.return_value = True
    	self.rutils.cmd_list = None
    	self.assertEqual(self.rutils.load_set_cfg(), True)

    def test_rutils_cmd_add(self):
        self.rutils.log = MagicMock()
        self.rutils.cmd = ''
        self.rutils.cmd_list = []
        self.rutils.ptr = {}
        self.rutils.ptr['arg_list'] = {'a': 10, 'b': 20}
        self.assertEqual(self.rutils.cmd_add('', arg='arg_list', mapping=True), None)


    def test_rutils_cmd_add_opt_flag(self):
    	self.rutils.log = MagicMock()
    	self.rutils.cmd = ''
    	self.rutils.cmd_list = []
    	self.rutils.ptr = {}
    	self.rutils.ptr['arg'] = {'a' : 10, 'b': 20}
    	self.assertEqual(self.rutils.cmd_add('', arg='arg', opt='flag'), None)

    def test_rutils_cmd_add_opt_non_flag(self):
        self.rutils.log = MagicMock()
        self.rutils.cmd = ''
        self.rutils.cmd_list = []
        self.rutils.ptr = {}
        self.rutils.ptr['arg'] = ''
        self.rutils._cmd_mapping = {}
        self.rutils._cmd_name_tag = {}
        self.assertEqual(self.rutils.cmd_add(
            '', arg='arg', tag='', update=True, mapping=True), None)

    def test_rutils_cmd_add_arg_none(self):
    	self.rutils.log = MagicMock()
    	self.rutils.cmd = ''
    	self.rutils.cmd_list = []
    	self.rutils.ptr = {}
    	self.rutils.ptr['arg'] = ''
    	self.assertEqual(self.rutils.cmd_add('', arg=None), None)

    def test_rutils_config_exception(self):
        self.rutils.log = MagicMock()
        with self.assertRaises(Exception) as context:
            self.rutils.config()
        self.assertTrue('Device handle is not set, dh' in str(context.exception))

    def test_rutils_config_if(self):
        self.rutils.log = MagicMock()
        self.rutils.cmd_list = [0  , 1  , 2  , 3  , 4  , 5  , 6  , 7  , 8  , 9  , 10  , 11  , 12  , 13  , 14  , 15  , 16  , 17  , 18  , 19  , 20  , 21  , 22  , 23  , 24  , 25  , 26  , 27  , 28  , 29  , 30  , 31  , 32  , 33  , 34  , 35  , 36  , 37  , 38  , 39  , 40  , 41  , 42  , 43  , 44  , 45  , 46  , 47  , 48  , 49  , 50  , 51  , 52  , 53  , 54  , 55  , 56  , 57  , 58  , 59]
        self.rutils.load_set_cfg = MagicMock()
        self.rutils.load_set_cfg.return_value = True
        self.rutils.dh = True
        self.assertEqual(self.rutils.config(dh=None), True)

    def test_rutils_config_else(self):
    	self.rutils.log = MagicMock()
    	self.rutils.cmd_list = [0  , 1  , 2  , 3 ]
    	self.rutils.dh = Values()
    	self.rutils.dh.config = MagicMock()
    	test = Values()
    	test.status = MagicMock()
    	test.status.return_value = True
    	self.rutils.dh.config.return_value = test
    	self.assertEqual(self.rutils.config(dh=None), True)

    def test_rutils_commit(self):
    	self.rutils.log = MagicMock()
    	self.rutils.dh = Values()
    	self.rutils.dh.commit = MagicMock()
    	test = Values()
    	test.status = MagicMock()
    	test.status.return_value = True
    	self.rutils.dh.commit.return_value = test
    	self.assertEqual(self.rutils.commit(), True)

    def test_rutils_set_dh(self):
        self.assertEqual(self.rutils.set_dh(None), None)

    def test_fn_checkin(self):
        self.assertEqual(self.rutils.fn_checkin("None"), None)

    def test_fn_checkout(self):
        self.rutils._chk_in_msg= {"test_fn_checkout":"abc def"}
        self.assertEqual(self.rutils.fn_checkout(True, err_msg=""), True)
        with self.assertRaises(Exception) as context:
            self.rutils.fn_checkout(False, err_msg="abc")
        self.assertTrue('abc' in str(context.exception))
        # self.assertEqual(self.rutils.fn_checkout(False, err_msg="abc"), True)





if __name__ == '__main__':
    unittest.main()
