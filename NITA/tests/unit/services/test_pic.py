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
import copy

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

from jnpr.toby.services.pic import pic

class Testpic(unittest.TestCase):


    def setUp(self):
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
        self.pic = pic(test=None)

        builtins.t = MagicMock()
        self.pic.log = t.log
        self.pic.get_fpc_pic_port_from_ifname = MagicMock()
        self.pic.get_fpc_pic_port_from_ifname.return_value = (12, 0, 0)
        self.pic.get_model = MagicMock()
        # self.pic.get_model = MagicMock()
        self.pic.set_resource = MagicMock()
        self.pic.cmd_add = MagicMock()
        self.pic.config = MagicMock()
        self.pic.dh = MagicMock()
        self.pic.dh.cli = MagicMock()
        self.pic.dh.cmd = MagicMock()
        self.pic.dh.cmd.return_value = True
        self.pic.dh.shell = MagicMock()
        self.pic.dh.shell.return_value = True
        self.pic.dh.vty = MagicMock()
        self.pic.dh.vty.return_value = True
        self.pic.dh.get_model = MagicMock()
        self.pic.dh.get_model.return_value = 'mx960'
        self.pic.fpc_slot = 1
        self.pic.pic_slot = 1
        self.pic.cmd_add = MagicMock()
        self.pic.config = MagicMock()
        self.pic.commit = MagicMock()
        self.pic.commit.return_value = True

    @patch('jnpr.toby.services.pic.pic.init')
    def test_init_constructor(self, init_patch):
        self.assertTrue(isinstance(pic(init_pic=True), pic))

    def test_pic_update(self):

        self.pic.ptr = {}
        self.assertEqual(self.pic._update(resource='h0', ifname='ms-1/0/0', vmsmpc=1, perf_mode=1, mx_vc=1, media=0, online=1, pic_type=None), None)

    def test_pic_init(self):
        self.pic.get_pic_type = MagicMock()
        self.pic.get_pic_type.return_value = True
        self.pic.online = MagicMock()
        self.pic.online.return_value = True
        self.pic.is_pic_online_yet = MagicMock()
        self.pic.is_pic_online_yet.return_value = True
        self.pic.fpc_type = 'MPC'
        self.pic.get_pic_type = MagicMock()
        self.pic.get_pic_type.return_value = True
        self.pic.is_vmsmpc = True
        self.pic.is_perf_mode = True
        self.pic.is_vc = True
        self.assertEqual(self.pic.init(resource='h0', ifname='ms-1/0/0', vmsmpc=1, perf_mode=1, mx_vc=1, media=0, online=1, pic_type=None), True)

    def test_pic_init_ifname_exception(self):
        with self.assertRaises(Exception) as context:
            self.pic.init()
        self.assertTrue('Missing mandatory argument, ifname' in str(context.exception))

    def test_pic_init_fpc_pic_none_exception(self):
        self.pic.get_fpc_pic_port_from_ifname.return_value  = (None, None, 0)
        with self.assertRaises(Exception) as context:
            self.pic.init(resource='h0', ifname='ms-1/0/0')
        self.assertTrue("fpc/pic couldn't be determined from the given ifname" in str(context.exception))

    # def test_pic_init_online_exception(self):
    #     self.pic.get_pic_type = MagicMock()
    #     self.pic.get_pic_type.return_value = None
    #     self.pic.get_fpc_pic_port_from_ifname.return_value  =  (12, 0, 0)

    #     self.pic.online = MagicMock()
    #     self.pic.online.return_value = False
    #     self.pic.fpc_type = 'MPC'
    #     self.pic.is_pic_online_yet = MagicMock()
    #     self.pic.is_pic_online_yet.return_value = False
    #     self.assertEqual(self.pic.init(resource='h0', ifname='ms-1/0/0', vmsmpc=1, perf_mode=1, mx_vc=1, media=0, online=1, pic_type=None), False)
        # with self.assertRaises(Exception) as context:
        #     self.pic.init(resource='h0', ifname='ms-1/0/0', vmsmpc=1, perf_mode=1, mx_vc=1, media=0, online=1, pic_type=None)
        # self.assertTrue('Could not online mic/pic' in str(context.exception))

    def test_pic_init_is_pic_online_yet_exception(self):
        self.pic.get_pic_type = MagicMock()
        self.pic.get_pic_type.return_value = None
        self.pic.online = MagicMock()
        self.pic.online.return_value = True
        self.pic.get_fpc_pic_port_from_ifname.return_value  =  (12, 0, 0)
        self.pic.is_pic_online_yet = MagicMock()
        self.pic.is_pic_online_yet.return_value = False
        self.pic.fpc_type = 'MPC'
        with self.assertRaises(Exception) as context:
            self.pic.init(resource='h0', ifname='ms-1/0/0', vmsmpc=1, perf_mode=1, mx_vc=1, media=0, online=1, pic_type=None)
        self.assertTrue('Unable to login to mic/pic even after' in str(context.exception))

    def test_pic_init_pic_type_false_exception(self):
        self.pic.get_pic_type = MagicMock()
        self.pic.get_pic_type.return_value = False
        self.pic.online = MagicMock()
        self.pic.online.return_value = True
        self.pic.get_fpc_pic_port_from_ifname.return_value  =  (12, 0, 0)
        self.pic.is_pic_online_yet = MagicMock()
        self.pic.is_pic_online_yet.return_value = True
        self.pic.fpc_type = 'MPC'
        with self.assertRaises(Exception) as context:
            self.pic.init(resource='h0', ifname='ms-1/0/0', vmsmpc=1, perf_mode=1, mx_vc=1, media=0, online=1, pic_type=None)
        self.assertTrue('Failed to create the pic object for' in str(context.exception))

    def test_pic_init_else_condition(self):
        self.pic.get_pic_type = MagicMock()
        self.pic.get_pic_type.return_value = True
        self.pic.online = MagicMock()
        self.pic.online.return_value = True
        self.pic.get_fpc_pic_port_from_ifname.return_value  =  (12, 0, 0)
        self.pic.is_pic_online_yet = MagicMock()
        self.pic.is_pic_online_yet.return_value = True
        self.pic.fpc_type = 'MPC'
        self.pic.is_media = False
        self.pic.do_online = False
        self.assertEqual(self.pic.init(resource='h0', ifname='ms-1/0/0', vmsmpc=1, perf_mode=1, mx_vc=1, media=0, online=0, pic_type=None), True)

    def test_pic_is_pic_online_yet(self):

        self.pic._login = MagicMock()
        self.pic._logout = MagicMock()
        self.pic._login.return_value = True
        self.pic._logout.return_value = True
        self.pic.is_connected = True
        self.pic.ifname = 'ms-2/1/0'
        self.assertEqual(self.pic.is_pic_online_yet(wait_time=10, chk_interval=10), True)

    def test_pic_is_pic_online_yet_outside_if(self):

        self.pic._login = MagicMock()
        self.pic._logout = MagicMock()
        self.pic._login.return_value = False
        self.pic._logout.return_value = True
        self.pic.is_connected = True
        self.pic.ifname = 'ms-2/1/0'

        with self.assertRaises(RuntimeError) as context:
            self.pic.is_pic_online_yet(wait_time=10, chk_interval=10)
        self.assertTrue("Pic, ms-2/1/0, didn't come online even after 10 secs" in str(context.exception))

    def test_pic_get_pic_type(self):
        self.pic.is_vc = True
        self.pic.mbr_id = 1
        data = {}
        info = {}
        info1 = {}
        info1['pic-detail'] = {}
        info1['pic-detail']['pic-type'] = True
        info1['pic-detail']['state'] = True
        info['multi-routing-engine-results'] = {}
        info['multi-routing-engine-results']['multi-routing-engine-item'] = {}
        info['multi-routing-engine-results']['multi-routing-engine-item']['fpc-information'] = {}
        info['multi-routing-engine-results']['multi-routing-engine-item']['fpc-information']['fpc'] = info1
        self.pic.get_fpc_pic_status = MagicMock()
        self.pic.get_xml_output = MagicMock()
        self.pic.get_xml_output.return_value = info
        self.pic.get_fpc_pic_status.return_value = data
        self.pic.is_connected = True
        data['pic'] = {}
        data['pic'][1] = {}
        data['fpc'] = {}
        data['descr'] = ''
        data['pic'][1]['type'] = True
        data['pic'][1]['state'] = True
        data['fpc']['state']  = True
        self.pic.ifname = 'ms-2/1/0'
        self.assertEqual(self.pic.get_pic_type(), True)
        #else condition
        data['pic'][1]['type'] = None
        data['pic'][1]['state'] = None

        info1['pic-detail']['pic-type'] = None
        info1['pic-detail']['state'] = None
        self.pic.get_fpc_pic_status.return_value = data
        self.pic.get_xml_output.return_value = info
        self.assertEqual(self.pic.get_pic_type(), None)

    def test_get_fpc_pic_status(self):
        self.pic.is_vc = True
        info = {}
        info1 = {}
        info1['description'] = True
        info1['state'] = True
        info['multi-routing-engine-results'] = {}
        info['multi-routing-engine-results']['multi-routing-engine-item'] = {}
        info['multi-routing-engine-results']['multi-routing-engine-item']['fpc-information'] = {}
        info['multi-routing-engine-results']['multi-routing-engine-item']['fpc-information']['fpc'] = info1
        self.pic.get_xml_output = MagicMock()
        self.pic.get_xml_output.return_value = info
        self.assertEqual(isinstance(self.pic.get_fpc_pic_status(fpc=''),dict), True)
        info1['pic'] = [{'pic-type':'', 'pic-state':'', 'pic-slot':'1'}]
        info['multi-routing-engine-results']['multi-routing-engine-item']['fpc-information']['fpc'] = info1
        #if condition after return
        self.pic.get_xml_output.return_value = info
        self.assertEqual(isinstance(self.pic.get_fpc_pic_status(fpc=''),dict),  True)
        info1['pic'] = {'pic-type':'', 'pic-state':'', 'pic-slot':'1'}
        info['multi-routing-engine-results']['multi-routing-engine-item']['fpc-information']['fpc'] = info1
		#else condition
        self.pic.get_xml_output.return_value = info
        self.assertEqual(isinstance(self.pic.get_fpc_pic_status(fpc=''),dict),  True)

    def test_check_pic_state(self):
        self.pic.check_fpc_pic_status = MagicMock()
        self.pic.check_fpc_pic_status.return_value = True
        self.assertEqual(self.pic.check_pic_state(), True)

    def test_login_to_pic(self):
        self.pic._login = MagicMock()
        self.pic._login.return_value = True
        self.assertEqual(self.pic.login_to_pic(), True)

    def test_logout_from_pic(self):
        self.pic._logout = MagicMock()
        self.pic._logout.return_value = True
        self.assertEqual(self.pic.logout_from_pic(), True)


    def test_execute_command_on_pic_exception(self):
        self.pic._cmd = MagicMock()
        self.pic._cmd.return_value = True
        with self.assertRaises(TypeError) as context:
            self.pic.execute_command_on_pic()
        self.assertTrue("Missing mandatory parameter, cmd" in str(context.exception))

    def test_execute_command_on_pic(self):
        self.pic._cmd = MagicMock()
        self.pic._cmd.return_value = True
        self.assertEqual(self.pic.execute_command_on_pic(cmd=''), True)

    def test_execute_commands_on_pic(self):
      self.pic.is_media = True
      self.pic._login = MagicMock()
      self.pic._logout = MagicMock()
      test = Values()
      test.response = MagicMock()
      test.response.return_value = True
      self.pic.dh.vty.return_value = test
      self.pic.ifname = 'ms-2/1/0'
      self.assertNotEqual(self.pic.execute_commands_on_pic(cmds=[1]), {1: True})
      self.pic.is_media = True
      self.pic.is_mpsdk = False
      self.pic._login = MagicMock()
      self.pic._logout = MagicMock()
      test = Values()
      test.response = MagicMock()
      test.response.return_value = True
      self.pic.dh.cli.return_value = test
      self.assertEqual(self.pic.execute_commands_on_pic(cmds=[1]), {1: True})
      self.pic.is_media = False
      self.pic.is_mpsdk = False
      self.pic._login = MagicMock()
      self.pic._logout = MagicMock()
      test = Values()
      test.response = MagicMock()
      test.response.return_value = True
      self.pic.dh.cli.return_value = test
      self.assertEqual(self.pic.execute_commands_on_pic(cmds=[1]), {1: True})

    def test_reboot_pics(self):
        self.assertEqual(self.pic.reboot_pics(), None)


    def test_get_pic_memory_snapshot(self):
      self.pic.media = True
      self.pic._login = MagicMock()
      self.pic._login.return_value = True
      test = Values()
      test.response = MagicMock()
      test.response.return_value = '''yntax yntax yntax yntax yntax yntax yntax
      grep yntax yntax yntax yntax yntax yntax yntax
      yntax yntax yntax yntax yntax 1234K 1234K yntax 1234K
      yntax yntax yntax yntax yntax 1234M 1234M yntax 1234M'''
      self.pic.dh.cli.return_value = test

      self.pic.logout = MagicMock()
      self.pic.logout.return_value = True
      self.assertEqual(isinstance(self.pic.get_pic_memory_snapshot(daemon_list=['yntax']), dict), True)

      self.pic.media = True
      self.pic._login = MagicMock()
      self.pic._login.return_value = True
      test = Values()
      test.response = MagicMock()
      test.response.return_value = '''grep ntax ntax ntax ntax ntax ntax
        SHM.*Allocated ntax ntax ntax ntax ntax ntax ntax
        Object cache.*Size ntax ntax ntax ntax ntax ntax ntax
        actual free space = 12780545360ntax ntax ntax ntax ntax ntax ntax
        yntax yntax yntax yntax 1234K 1234K 1234K ntax 1234K
        yntax yntax yntax yntax 1234K 1234K 1234M ntax 1234M'''
      self.pic.dh.cli.return_value = test

      self.pic._logout = MagicMock()
      self.pic._logout.return_value = True
      self.assertEqual(isinstance(self.pic.get_pic_memory_snapshot(daemon_list=['yntax']), dict), True)


    @patch('jnpr.toby.services.pic.utils.cmp_dicts')
    def test_verify_pic_memory_snapshot(self, cmp_dicts_patch):
        cmp_dicts_patch.return_value = True
        data = {}
        data['shm'] = 'test'
        data['objcache'] = {}
        data['objcache']['test'] = 1
        data['daemon'] = 'test'
        data['mum'] = 'test'
        self.pic.get_pic_memory_snapshot = MagicMock()
        self.pic.get_pic_memory_snapshot.return_value = data

        self.assertEqual(self.pic.verify_pic_memory_snapshot(before=data, daemon_list=['test'], ignore_list=['test'] ), True)
        cmp_dicts_patch.return_value = True
        data = {}
        data['shm'] = 'test'
        data['objcache'] = {}
        data['objcache']['test'] = 1
        data['daemon'] = 'test'
        data['mum'] = 'test'
        self.pic.get_pic_memory_snapshot = MagicMock()
        self.pic.get_pic_memory_snapshot.return_value = data

        self.assertEqual(self.pic.verify_pic_memory_snapshot(before=data, daemon_list=['test'], ignore_list=[] , tol_shm=1), True)
        cmp_dicts_patch.return_value = True
        data = {}
        data['shm'] = 'test'
        data['objcache'] = {}
        data['objcache']['test'] = 1
        data['daemon'] = 'test'
        data['mum'] = 'test'
        data1 = copy.deepcopy(data)
        data1['objcache']['test'] = 2
        self.pic.get_pic_memory_snapshot = MagicMock()
        self.pic.get_pic_memory_snapshot.return_value = data1

        self.assertEqual(self.pic.verify_pic_memory_snapshot(before=data, daemon_list=['test'], ignore_list=['test'] , tol_shm=1), False)

    def test_login(self):
        self.pic.is_vmsmpc = True
        self.pic.is_mpsdk = True
        self.pic.is_mpsdk_dbgm = True
        test = Values()
        test.status = MagicMock()
        self.pic.ifname = 'ms-2/1/0'
        self.pic.is_media = True
        self.assertEqual(self.pic._login(), True)
        self.pic.is_media = False
        test.status.return_value = True
        self.pic.dh.cli.return_value = test
        self.pic.dh.shell.return_value = test
        self.pic._kill_mspdbg = MagicMock()
        self.assertEqual(self.pic._login(), True)
        self.pic.is_vmsmpc = False
        self.assertEqual(self.pic._login(), True)
        self.pic.is_mpsdk_dbgm = False
        self.pic.is_vmsmpc = True
        self.assertEqual(self.pic._login(), True)
        self.pic.is_mpsdk_dbgm = False
        self.pic.is_vmsmpc = False
        self.assertEqual(self.pic._login(), True)
        self.pic.is_mpsdk_dbgm = False
        self.pic.is_vmsmpc = False
        test.status.return_value = False
        self.pic.dh.cli.return_value = test
        self.pic.dh.shell.return_value = test
        with self.assertRaises(RuntimeError) as context:
            self.pic._login()
        self.assertTrue("Unable to login to ms-2/1/0" in str(context.exception))

    def test_logout(self):
        self.pic.mpsdk = True
        self.pic.is_loggedin = True
        self.pic.is_connected = True
        self.pic.is_media = True
        self.assertEqual(self.pic._logout(), True)
        self.pic.is_media = False
        self.assertNotEqual(self.pic._logout(), True)
        self.pic.is_mpsdk = False
        self.pic.is_connected = False
        self.assertEqual(self.pic._logout(), True)
        
    def test_kill_mspdbg(self):
        test = Values()
        test.response = MagicMock()
        test.response.return_value =  '''
        grep
        mspdbg-cli tewst
        '''
        self.pic.dh.cli.return_value = test
        self.assertEqual(self.pic._kill_mspdbg(), None)

    def test_cmd(self):
        self.pic._dut_model = ''
        self.pic._login = MagicMock()
        self.pic._login.return_value = True
        self.pic.is_mpsdk_dbgm = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value = True
        self.pic.dh.cli.return_value = test
        self.pic._logout = MagicMock()
        self.pic._logout.return_value = True
        self.assertEqual(self.pic._cmd(), True)
        self.pic._login = MagicMock()
        self.pic._login.return_value = True
        self.pic.is_mpsdk_dbgm = False
        self.pic.is_mpsdk = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value = True
        self.pic.dh.cli.return_value = test
        self.pic._logout = MagicMock()
        self.pic._logout.return_value = True
        self.assertEqual(self.pic._cmd(), True)
        self.pic.is_mpsdk_dbgm = False
        self.pic.is_mpsdk = False
        self.pic.is_media = True
        test = Values()
        test.response = MagicMock()
        test.response.return_value = True
        self.pic.dh.vty.return_value = test
        self.assertEqual(self.pic._cmd(), True)
        self.pic.is_mpsdk_dbgm = False
        self.pic.is_mpsdk = False
        self.pic.is_media = False
        test = Values()
        test.response = MagicMock()
        test.response.return_value = True
        self.pic.dh.cli.return_value = test
        self.assertEqual(self.pic._cmd(), True)
        self.pic._login = MagicMock()
        self.pic._login.return_value = False
        self.assertEqual(self.pic._cmd(), None)

    @patch('jnpr.toby.services.pic.time.sleep')
    def test_check_fpc_pic_status(self, sleep_patch):
        self.pic.dh.cli = MagicMock()
        test = Values
        test.response =  MagicMock()
        test.response.return_value ='''Slot 0   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 1   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 2   Online       MPC Type 2 3D EQ
  PIC 0  Online       10x 1GE(LAN) SFP
  PIC 1  Online       10x 1GE(LAN) SFP
  PIC 2  Online       2x 10GE  XFP
  PIC 3  Online       2x 10GE  XFP
Slot 4   Online       MS-MPC
  PIC 0  offline       MS-MPC-PIC
  PIC 1  Online       MS-MPC-PIC
  PIC 2  Online       MS-MPC-PIC
  PIC 3  Online       MS-MPC-PIC
''' 
         
        self.pic.dh.cli.return_value = test

        self.assertNotEqual(self.pic.check_fpc_pic_status(), None)

    @patch('jnpr.toby.services.pic.time.sleep')
    def test_check_fpc_pic_status_ignore_list(self, sleep_patch):
        self.pic.dh.cli = MagicMock()
        test = Values
        test.response =  MagicMock()
        test.response.return_value ='''Slot 0   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 1   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 2   Online       MPC Type 2 3D EQ
  PIC 0  Online       10x 1GE(LAN) SFP
  PIC 1  Online       10x 1GE(LAN) SFP
  PIC 2  Online       2x 10GE  XFP
  PIC 3  Online       2x 10GE  XFP
Slot 4   Online       MS-MPC
  PIC 0  Online       MS-MPC-PIC
  PIC 1  Online       MS-MPC-PIC
  PIC 2  Online       MS-MPC-PIC
  PIC 3  Online       MS-MPC-PIC
''' 
         
        self.pic.dh.cli.return_value = test

        self.assertNotEqual(self.pic.check_fpc_pic_status(ignore="None", fpc_list=[2, 4]), None)

    @patch('jnpr.toby.services.pic.time.sleep')
    def test_check_fpc_pic_status_while_exception(self, sleep_patch):
        self.pic.dh.cli = MagicMock()
        test = Values
        test.response =  MagicMock()
        test.response.return_value ='''Slot 0   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 1   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 2   Online       MPC Type 2 3D EQ
  PIC 0  Online       10x 1GE(LAN) SFP
  PIC 1  Online       10x 1GE(LAN) SFP
  PIC 2  Online       2x 10GE  XFP
  PIC 3  Online       2x 10GE  XFP
Slot 4   Online       MS-MPC''' 
         
        self.pic.dh.cli.return_value = test

        self.assertNotEqual(self.pic.check_fpc_pic_status(ignore="None", fpc_list=[2, 4]), None)

    @patch('jnpr.toby.services.pic.time.sleep')
    def test_check_fpc_pic_status_fpc_slot(self, sleep_patch):
        self.pic.dh.cli = MagicMock()
        test = Values
        test.response =  MagicMock()
        test.response.return_value ='''Slot 0   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 1   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 2   Online       MPC Type 2 3D EQ
  PIC 0  Online       10x 1GE(LAN) SFP
  PIC 1  Online       10x 1GE(LAN) SFP
  PIC 2  Online       2x 10GE  XFP
  PIC 3  Online       2x 10GE  XFP
Slot 4   Online       MS-MPC
  PIC 0  Online       MS-MPC-PIC
  PIC 1  offline       MS-MPC-PIC
  PIC 2  Online       MS-MPC-PIC
  PIC 3  Online       MS-MPC-PIC
''' 
         
        self.pic.dh.cli.return_value = test

        self.assertNotEqual(self.pic.check_fpc_pic_status(ignore="None", fpc_list=[2, 4]), None)

    @patch('jnpr.toby.services.pic.time.sleep')
    def test_check_fpc_pic_status_fpc_slot_pic_slot(self, sleep_patch):
        self.pic.dh.cli = MagicMock()
        test = Values
        test.response =  MagicMock()
        test.response.return_value ='''Slot 0   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 1   Online       MS-DPC
  PIC 0  Online       MS-DPC PIC
  PIC 1  Online       MS-DPC PIC
Slot 2   Online       MPC Type 2 3D EQ
  PIC 0  Online       10x 1GE(LAN) SFP
  PIC 1  Online       10x 1GE(LAN) SFP
  PIC 2  Online       2x 10GE  XFP
  PIC 3  Online       2x 10GE  XFP
Slot 4   Online       MS-MPC
  PIC 0  Online       MS-MPC-PIC
  PIC 1  offline       MS-MPC-PIC
  PIC 2  offline       MS-MPC-PIC
  PIC 3  Online       MS-MPC-PIC
''' 
         
        self.pic.dh.cli.return_value = test

        self.assertNotEqual(self.pic.check_fpc_pic_status(ignore="None", fpc_list=[2, 4], pic_list=[0, 2, 5], timeout=300), None)

        # self.pic.is_vmsmpc = True
        # self.pic.is_mpsdk = True
        # self.pic.is_mpsdk_dbgm = True
        # test.status.return_value = False
        # self.pic.dh.cli.return_value = test
        # self.pic.dh.shell.return_value = test
        # self.pic._kill_mspdbg = MagicMock()
        # with self.assertRaises(RuntimeError) as context:
        #     self.pic._login()
        # self.assertTrue("Unable to login to ms-2/1/0" in str(context.exception))
        # # # self.assertEqual(self.pic._login(), False)
        # self.pic.is_vmsmpc = False
        # self.pic.is_mpsdk = True
        # self.pic.is_mpsdk_dbgm = False
        # test.status.return_value = False
        # self.pic.dh.cli.return_value = test
        # self.pic._kill_mspdbg = MagicMock()
        # with self.assertRaises(RuntimeError) as context:
        #     self.pic._login()
        # self.assertTrue("Unable to login to ms-2/1/0" in str(context.exception))
        # self.assertEqual(self.pic._login(), False)
        # self.pic.is_vmsmpc = False
        # self.pic.is_mpsdk = False
        # self.pic.is_mpsdk_dbgm = False
        # test.status.return_value = True
        # self.pic.dh.cli.return_value = test
        # self.pic._kill_mspdbg = MagicMock()
        # self.assertEqual(self.pic._login(), False)
        # with self.assertRaises(RuntimeError) as context:
        #     self.pic._login()
        # self.assertTrue("Unable to login to ms-2/1/0" in str(context.exception))
        #covers  elif self.is_vmsmpc:
        # self.pic.is_vmsmpc = True
        # self.pic.is_mpsdk = True
        # self.pic.is_mpsdk_dbgm = False
        # test.status.return_value = True
        # self.pic.dh.cli.return_value = test
        # self.pic._kill_mspdbg = MagicMock()
        # self.assertEqual(self.pic._login(), True)
        #covers if self.is_media:
        # self.pic.is_media = True
        # self.assertEqual(self.pic._login(), True)

  #   @patch('jnpr.toby.services.pic.time.sleep')
  #   def test_setup(self, sleep_patch):
  #       sleep_patch.return_value = ''
  #       self.pic.ifname = 'ms-sp'
  #       self.pic.dh.chk_if_status = MagicMock()
  #       self.pic.dh.chk_if_status.return_value = True
  #       self.assertEqual(self.pic.setup(apps='abc|def', mpsdk=1, image_file='', boot_ejunos64=True, affinity_hash='', commit=1, action='delete'),  True)
  #       self.pic.ifname = 'spabc'
  #       self.pic.dh.chk_if_status = MagicMock()
  #       self.pic.dh.chk_if_status.side_effect = [False, False]
  #       self.assertEqual(self.pic.setup(apps='abc|def', mpsdk=1, image_file='', boot_ejunos64=True, affinity_hash='', commit=1, total_mem='', mem_size='', fw_db_size='', data_pollers=True),  False)
  #       self.pic.ifname = 'spabc'
  #       self.pic.dh.chk_if_status = MagicMock()
  #       self.pic.dh.chk_if_status.side_effect = [False, True]
  #       self.pic.model = 'mx80'
  #       self.pic.pic_type = 'MS-MIC'
  #       self.pic.online = MagicMock()
  #       self.pic.online.return_value = True
  #       self.assertEqual(self.pic.setup(apps='abc|def', mpsdk=1, image_file='', boot_ejunos64=True, affinity_hash='', commit=1, total_mem='', mem_size='', fw_db_size=''),  True)
  #       self.pic.ifname = 'spabc'
  #       self.pic.dh.chk_if_status = MagicMock()
  #       self.pic.dh.chk_if_status.side_effect = [False, True]
  #       self.pic.model = 'mx80'
  #       self.pic.pic_type = 'MS-MIC'
  #       self.pic.online = MagicMock()
  #       self.pic.online.return_value = True
  #       self.assertEqual(self.pic.setup(apps='abc|def', mpsdk=1, image_file='', boot_ejunos64=True, affinity_hash='', commit=1, total_mem='', mem_size='', fw_db_size='', wait_ifl=0),  True)
  #       self.pic.ifname = 'spabc'
  #       self.pic.dh.chk_if_status = MagicMock()
  #       self.pic.dh.chk_if_status.side_effect = [False, True]
  #       self.pic.model = 'mx80'
  #       self.pic.pic_type = 'MS-MIC'
  #       self.pic.online = MagicMock()
  #       self.pic.online.return_value = True
  #       self.pic.commit.return_value = False
  #       self.assertEqual(self.pic.setup(apps='abc|def', mpsdk=1, image_file='', boot_ejunos64=True, affinity_hash='', commit=1, total_mem='', mem_size='', fw_db_size='', wait_ifl=0),  False)

  #   def test_check_state(self):
  #   	self.pic.dh.chk_pic =MagicMock()
  #   	self.pic.dh.chk_pic.return_value = True
  #   	self.assertEqual(self.pic.check_state(), True)

  #   def test_kill_mspdbg(self):
  #   	self.pic.dh.cli.return_value = '''
  #   	grep
  #   	mspdbg-cli tewst
  #   	'''
  #   	self.assertEqual(self.pic._kill_mspdbg(), None)

  #   def test_login(self):
  #   	self.pic.vmsmpc = True
  #   	self.pic.mpsdk = True
  #   	self.pic.mpsdk_dbgm = True
  #   	self.pic.dh.cli.return_value = True
  #   	self.pic._kill_mspdbg = MagicMock()
  #   	self.assertEqual(self.pic.login(), True)
  #   	self.pic.vmsmpc = True
  #   	self.pic.mpsdk = True
  #   	self.pic.mpsdk_dbgm = True
  #   	self.pic.dh.cli.return_value = False
  #   	self.pic._kill_mspdbg = MagicMock()
  #   	self.assertEqual(self.pic.login(), False)
  #   	self.pic.vmsmpc = False
  #   	self.pic.mpsdk = True
  #   	self.pic.mpsdk_dbgm = False
  #   	self.pic.dh.cli.return_value = False
  #   	self.pic._kill_mspdbg = MagicMock()
  #   	self.assertEqual(self.pic.login(), False)
  #   	self.pic.vmsmpc = False
  #   	self.pic.mpsdk = False
  #   	self.pic.mpsdk_dbgm = False
  #   	self.pic.dh.cli.return_value = False
  #   	self.pic._kill_mspdbg = MagicMock()
  #   	self.assertEqual(self.pic.login(), False)
  #   	self.pic.vmsmpc = True
  #   	self.pic.mpsdk = True
  #   	self.pic.mpsdk_dbgm = False
  #   	self.pic.dh.cli.return_value = True
  #   	self.pic._kill_mspdbg = MagicMock()
  #   	self.assertEqual(self.pic.login(), True)


  #   def test_logout(self):
  #   	self.pic.mpsdk = True
  #   	self.pic.is_loggedin = True
  #   	self.pic.is_connected = True
  #   	self.assertNotEqual(self.pic.logout(), True)
  #   	self.pic.mpsdk = False
  #   	self.pic.is_connected = False
  #   	self.assertEqual(self.pic.logout(), True)


  #   def test_cmds(self):
  #   	self.pic.media = True
  #   	self.pic.login = MagicMock()
  #   	self.pic.logout = MagicMock()
  #   	test = Values()
  #   	test.response = MagicMock()
  #   	test.response.return_value = True
  #   	self.pic.dh.vty.return_value = test
  #   	self.assertEqual(self.pic.cmds(cmds=[1]), {1: True})
  #   	self.pic.media = True
  #   	self.pic.mpsdk = True
  #   	self.pic.login = MagicMock()
  #   	self.pic.logout = MagicMock()
  #   	test = Values()
  #   	test.response = MagicMock()
  #   	test.response.return_value = True
  #   	self.pic.dh.cmd.return_value = test
  #   	self.assertEqual(self.pic.cmds(cmds=[1]), {1: True})
  #   	self.pic.media = False
  #   	self.pic.mpsdk = False
  #   	self.pic.login = MagicMock()
  #   	self.pic.logout = MagicMock()
  #   	test = Values()
  #   	test.response = MagicMock()
  #   	test.response.return_value = True
  #   	self.pic.dh.cmd.return_value = test
  #   	self.assertEqual(self.pic.cmds(cmds=[1]), {1: True})

  #   def test_cmd(self):
  #   	self.pic.model = ''
  #   	self.pic.login = MagicMock()
  #   	self.pic.login.return_value = True
  #   	self.pic.mpsdk_dbgm = True
  #   	test = Values()
  #   	test.response = MagicMock()
  #   	test.response.return_value = True
  #   	self.pic.dh.cli.return_value = test
  #   	self.pic.logout = MagicMock()
  #   	self.pic.logout.return_value = True
  #   	self.assertEqual(self.pic._cmd(), True)
  #   	self.pic.login = MagicMock()
  #   	self.pic.login.return_value = True
  #   	self.pic.mpsdk_dbgm = False
  #   	self.pic.mpsdk = True
  #   	test = Values()
  #   	test.response = MagicMock()
  #   	test.response.return_value = True
  #   	self.pic.dh.cli.return_value = test
  #   	self.pic.logout = MagicMock()
  #   	self.pic.logout.return_value = True
  #   	self.assertEqual(self.pic._cmd(), True)
  #   	self.pic.mpsdk_dbgm = False
  #   	self.pic.mpsdk = False
  #   	self.pic.media = True
  #   	test = Values()
  #   	test.response = MagicMock()
  #   	test.response.return_value = True
  #   	self.pic.dh.vty.return_value = test
  #   	self.assertEqual(self.pic._cmd(), True)
  #   	self.pic.mpsdk_dbgm = False
  #   	self.pic.mpsdk = False
  #   	self.pic.media = False
  #   	test = Values()
  #   	test.response = MagicMock()
  #   	test.response.return_value = True
  #   	self.pic.dh.cli.return_value = test
  #   	self.assertEqual(self.pic._cmd(), True)
  #   	self.pic.login = MagicMock()
  #   	self.pic.login.return_value = False
  #   	self.assertEqual(self.pic._cmd(), None)












if __name__ == '__main__':
    unittest.main()
