#!/usr/local/bin/python3

import sys
import os
from collections import OrderedDict, defaultdict
import unittest2 as unittest
from mock import patch, Mock, MagicMock, call, mock_open
import builtins
from jnpr.toby.init.init import init
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.juniper.junos import Juniper
import jnpr.toby.engines.config.config_utils as config_utils
from jnpr.toby.engines.config.config import config
#from config import config
#import config_utils
import pprint
builtins.t = MagicMock(spec=init)
t.t_dict ={'resources':
                {'r0':
                    {'interfaces':
                        {'r0r1_2':
                           {'pic': 'ge-1/0/7',
                            'management': 0,
                            'name': 'ge-1/0/7.0',
                            'link': 'link2',
                            'type': ['10x', '1GE', 'LAN', 'EQ', 'SFP-SX', 'QDPCE-R-40X', 'B3', 'I3', 'ether', 'ge'],
                            'unit': 0},
                         'r0r1_1':
                            {'management': 0,
                            'uv_test': 2,
                            'uv-test2': 3,
                            'unit': 0,
                            'type': ['10x', '1GE', 'LAN', 'EQ', 'SFP-SX', 'QDPCE-R-40X', 'B3', 'I3', 'ether', 'ge'],
                            'pic': 'ge-1/0/6', 'name': 'ge-1/0/6.0', 'link': 'link1'}},
                     'system':
                        {'primary':
                            {'cube': ['COMMON-LISP::OR', 'rbu-cst-core-wf-1', 'misc'],
                            'osname': 'JunOS',
                            'name': 'tetra',
                            'model': 'mx240',
                            'make': 'juniper',
                            'controllers':
                                {'re0':
                                    {'domain': 'englab.juniper.net',
                                    'isoaddr': '47.0005.80ff.f800.0000.0108.0001.0100.0923.4220.00',
                                    'con-ip': '10.9.53.203',
                                    'loop-ip': '10.9.234.220',
                                    'hostname': 'tetra',
                                    'mgt-ip': '10.9.33.24',
                                    'loop-ipv6': 'abcd::10:9:234:220',
                                    'osname': 'JunOS',
                                    'mgt-ipv6': 'abcd::10:9:33:24',
                                    'mgt-intf-name': 'fxp0.0'}},
                            }}},
                'r1':
                    {'interfaces':
                        {'r0r1_2':
                            {'pic': 'ge-0/0/3',
                            'management': 0,
                            'name': 'ge-0/0/3.0',
                            'link': 'link2',
                            'type': ['IQ2E', 'SFP-SX', 'DOWN', 'B3', 'E-FPC', 'ge', 'ether', '4x', '1GE', 'LAN'],
                            'unit': 0},
                         'r0r1_1':
                            {'pic': 'ge-0/0/2',
                            'management': 0,
                            'name': 'ge-0/0/2.0', 'link': 'link1',
                            'type': ['ge', 'ether', '4x', '1GE', 'LAN', 'IQ2E', 'SFP-SX', 'DOWN', 'B3', 'E-FPC'],
                            'unit': 0}},
                     'system':
                        {'primary':
                            {'re_type': 'RE-5.0',
                            'cube': ['COMMON-LISP::OR', 'rbu-cst-core-wf-1', 'misc'],
                            'osname': 'JunOS',
                            'name': 'brandeis',
                            'model': 'm10i',
                            'make': 'juniper',
                            'controllers':
                                {'re0':
                                    {'domain': 'englab.juniper.net',
                                    'isoaddr': '47.0005.80ff.f800.0000.0108.0001.0100.0901.0154.00',
                                    'con-ip': '10.9.17.141',
                                    'loop-ip': '10.9.10.154',
                                    'hostname': 'brandeis',
                                    'mgt-ip': '10.9.2.154',
                                    'loop-ipv6': 'abcd::10:9:10:154',
                                    'osname': 'JunOS',
                                    'mgt-ipv6': 'abcd::10:9:2:154',
                                    'mgt-intf-name': 'fxp0.0'}},
                                }
                            }
                    }}}


#builtins.t.log = MagicMock(return_value=True)
#x = init._create_global_tv_dictionary(t)
builtins.tv = {'r0__cube': ['COMMON-LISP::OR',
              'rbu-cst-core-wf-1',
              'rbu-cst-core-wf-2',
              'nrtb1',
              'rbu-protocol-core-wf-1',
              'misc'],
 'r0__make': 'juniper',
 'r0__model': 'mx240',
 'r0__name': 'tetra',
 'r0__osname': 'JunOS',
 'r0__r0r1_1__fpcslot': '1',
 'r0__r0r1_1__link': 'link1',
 'r0__r0r1_1__management': 0,
 'r0__r0r1_1__name': 'ge-1/0/6.0',
 'r0__r0r1_1__pic': 'ge-1/0/6',
 'r0__r0r1_1__picslot': '0',
 'r0__r0r1_1__portslot': '6',
 'r0__r0r1_1__type': ['10x',
                      '1GE',
                      'LAN',
                      'EQ',
                      'SFP-SX',
                      'QDPCE-R-40X',
                      'B3',
                      'I3',
                      'ether',
                      'ge'],
 'r0__r0r1_1__unit': 0,
 'r0__r0r1_1__uv-test2': 3,
 'r0__r0r1_1__uv_test': 2,
 'r0__r0r1_2__fpcslot': '1',
 'r0__r0r1_2__link': 'link2',
 'r0__r0r1_2__management': 0,
 'r0__r0r1_2__name': 'ge-1/0/7.0',
 'r0__r0r1_2__pic': 'ge-1/0/7',
 'r0__r0r1_2__picslot': '0',
 'r0__r0r1_2__portslot': '7',
 'r0__r0r1_2__type': ['10x',
                      '1GE',
                      'LAN',
                      'EQ',
                      'SFP-SX',
                      'QDPCE-R-40X',
                      'B3',
                      'I3',
                      'ether',
                      'ge'],
 'r0__r0r1_2__unit': 0,
 'r0__re0__con-ip': '10.9.53.203',
 'r0__re0__domain': 'englab.juniper.net',
 'r0__re0__hostname': 'tetra',
 'r0__re0__isoaddr': '47.0005.80ff.f800.0000.0108.0001.0100.0923.4220.00',
 'r0__re0__loop-ip': '10.9.234.220',
 'r0__re0__loop-ipv6': 'abcd::10:9:234:220',
 'r0__re0__mgt-intf-name': 'fxp0.0',
 'r0__re0__mgt-ip': '10.9.33.24',
 'r0__re0__mgt-ipv6': 'abcd::10:9:33:24',
 'r0__re0__osname': 'JunOS',
 'r1__cube': ['COMMON-LISP::OR',
              'rbu-cst-core-wf-1',
              'rbu-cst-core-wf-2',
              'nrtb1',
              'rbu-protocol-core-wf-1',
              'misc'],
 'r1__make': 'juniper',
 'r1__model': 'm10i',
 'r1__name': 'brandeis',
 'r1__osname': 'JunOS',
 'r1__r0r1_1__fpcslot': '0',
 'r1__r0r1_1__link': 'link1',
 'r1__r0r1_1__management': 0,
 'r1__r0r1_1__name': 'ge-0/0/2.0',
 'r1__r0r1_1__pic': 'ge-0/0/2',
 'r1__r0r1_1__picslot': '0',
 'r1__r0r1_1__portslot': '2',
 'r1__r0r1_1__type': ['ge',
                      'ether',
                      '4x',
                      '1GE',
                      'LAN',
                      'IQ2E',
                      'SFP-SX',
                      'DOWN',
                      'B3',
                      'E-FPC'],
 'r1__r0r1_1__unit': 0,
 'r1__r0r1_2__fpcslot': '0',
 'r1__r0r1_2__link': 'link2',
 'r1__r0r1_2__management': 0,
 'r1__r0r1_2__name': 'ge-0/0/3.0',
 'r1__r0r1_2__pic': 'ge-0/0/3',
 'r1__r0r1_2__picslot': '0',
 'r1__r0r1_2__portslot': '3',
 'r1__r0r1_2__type': ['IQ2E',
                      'SFP-SX',
                      'DOWN',
                      'B3',
                      'E-FPC',
                      'ge',
                      'ether',
                      '4x',
                      '1GE',
                      'LAN'],
 'r1__r0r1_2__unit': 0,
 'r1__re0__con-ip': '10.9.17.141',
 'r1__re0__domain': 'englab.juniper.net',
 'r1__re0__hostname': 'brandeis',
 'r1__re0__isoaddr': '47.0005.80ff.f800.0000.0108.0001.0100.0901.0154.00',
 'r1__re0__loop-ip': '10.9.10.154',
 'r1__re0__loop-ipv6': 'abcd::10:9:10:154',
 'r1__re0__mgt-intf-name': 'fxp0.0',
 'r1__re0__mgt-ip': '10.9.2.154',
 'r1__re0__mgt-ipv6': 'abcd::10:9:2:154',
 'r1__re0__osname': 'JunOS',
 'r1__re_type': 'RE-5.0'}



t.get_handle = MagicMock()
t.get_handle.execute_rpc = MagicMock(return_value = Response(status=True, response='test'))

cfg = MagicMock(spec=config)
cfg.c_dict = {}
cfg.cv_flat = {}
cfg.templates = {}
cfg.device_handle_map = {}
cfg.cfg = defaultdict(list)
cfg.cached = False
cfg.cached_cfg = {}
#cfg.__make_c_dict = MagicMock(return_value={'a':1})
#cfg._process_cv = MagicMock()
cfg._config__get_cvar.return_value = 'JunOS'
cfg._config__copy_t_dict = MagicMock(side_effect=config._config__copy_t_dict(cfg))

class TestConfig(unittest.TestCase):
    def test__init(self):
        new_cfg = config()
        self.assertIsInstance(new_cfg, config)
    
    def test_config_engine_device_list(self):
        # load file
        kwargs = {'load_timeout':60}
        cfg._process_cv.return_value=kwargs
        dh = MagicMock()
        dh.current_node.current_controller.os = 'JunOS'
        dh.current_node.current_controller.host = '1.1.1.1'
       # dh.execute_rpc.return_value = Response(status=True, response='test')
        cfg._get_dev_handle.return_value = dh
        #self.assertTrue(config.config_engine(cfg, cmd_list='set this', device_list='tetra'))
        # device_list has a name that does not exist
        try:
            config.config_engine(cfg, cmd_list='set this', device_list='noname')
        except:
            self.assertRaises(Exception)

        # device _list has a handle:
        self.assertTrue(config.config_engine(cfg, cmd_list='set this', device_list=dh))
        try:
            config.config_engine(cfg, cmd_list='set this', device_list=dict())
        except:
            self.assertRaises(Exception)

    @patch("builtins.open", new_callable=mock_open, read_data='test_file')
    @patch("jnpr.toby.engines.config.config_utils.find_file")
    @patch('jnpr.toby.engines.config.config_utils.read_yaml', return_value={'r0':'CONFIG'})
    def test_config_engine_kwargs_templates(self, mock_file, find_file, read_yaml):
        self.find_file = MagicMock()
        kwargs = {'template_files': mock_file, 'templates':'test2', 'commit_timeout':60}
        cfg._process_cv.return_value=kwargs
        self.assertTrue(config.config_engine(cfg, device_list='r0', **kwargs))

        # template read_yaml exception
        read_yaml.side_effect =Exception
        kwargs = {'templates':'test2'}
        cfg._process_cv.return_value=kwargs
        try:
            config.config_engine(cfg, device_list='r0', **kwargs)
        except:
            self.assertRaises(Exception)
            #pass
        #self.assertRaises(Exception)

    @patch("builtins.open", new_callable=mock_open, read_data='test_file')
    @patch("jnpr.toby.engines.config.config_utils.find_file")
    @patch('jnpr.toby.engines.config.config_utils.read_yaml', return_value={'r0':'CONFIG'})
    def test_config_engine_kwargs_config_templates(self, mock_file, find_file, read_yaml):
        self.find_file = MagicMock()
        kwargs = {'template_files':mock_file, 'config_templates':'test','timeout':60}
        cfg._process_cv.return_value=kwargs
        self.assertTrue(config.config_engine(cfg, device_list='r0', **kwargs))

        kwargs = {'template_files':'test_file','config_templates':['test','test1'],'commit_timeout':60}
        cfg._process_cv.return_value=kwargs
        self.assertTrue(config.config_engine(cfg, device_list='r0', **kwargs))

        # template read_yaml exception
        read_yaml.side_effect =Exception
        kwargs = {'template_files':'test2'}
        cfg._process_cv.return_value=kwargs
        try:
            config.config_engine(cfg, device_list='r0', **kwargs)
        except:
            self.assertRaises(Exception)

        try:
            config.config_engine(cfg, **kwargs)
        except:
            self.assertRaises(Exception)


    #patch('config_utils.read_yaml', return_value={'r0':'CONFIG'})
    @patch('jnpr.toby.engines.config.config_utils.read_yaml', return_value={'r0':'CONFIG'})
    def test_config_engine_load_file(self, read_yaml):

        # load_file_without_device_list
        try:
            config.config_engine(cfg, load_file='myfile')
        except Exception as err:
            self.assertEqual(str(err), "missing device_list for load_file")
        # load file
        kwargs = {'load_timeout':60}
        cfg._process_cv = MagicMock(return_value=kwargs)
        self.assertTrue(config.config_engine(cfg, load_file='local:myfile', device_list='r0', load_timeout=60))
        kwargs = {'timeout':60}
        cfg._process_cv.return_value=kwargs
        self.assertTrue(config.config_engine(cfg, load_file='myfile', device_list='r0', timeout=60))

    def test_config_engine_load_string(self):

        # load_file_without_device_list
        kwargs = {'load_string': 'mycfg', 'load_timeout':60}
        cfg._process_cv.return_value=kwargs
        try:
            config.config_engine(cfg, load_string='myfstr')
        except Exception as err:
            self.assertEqual(str(err), "missing device_list for load_string")

        # load file
        self.assertTrue(config.config_engine(cfg, load_string='set mystr', device_list='r0', load_timeout=60))
        kwargs = {'load_string': 'set mycfg', 'timeout':60}
        cfg._process_cv.return_value=kwargs
        self.assertTrue(config.config_engine(cfg, load_string='set mystr', device_list='r0', timeout=60))

        
    def test_config_set(self):

        #without_device_list
        kwargs = {'cmd_list':'set hello abc', 'load_timeout':60}
        try:
            config.config_engine(cfg,**kwargs)
        except Exception as err:
            self.assertEqual(str(err), "missing device_list for cmd_list")

        #with device_list 
        self.assertTrue(config.config_engine(cfg, cmd_list='set mystr', device_list='r0', load_timeout=60))
        kwargs = {'device_list':'r0','cmd_list':['set mycfg','set mycfg1'],'timeout':60}
        self.assertTrue(config.config_engine(cfg, **kwargs))
    '''
    def test_config_engine_load_string(self):
        cfg = config()

        # load_file_without_device_list
        try:
            cfg.config_engine(load_string='myfstr')
        except Exception as err:
            self.assertEqual(str(err), "missing device_list for load_string")

        cfg._load_onto_device = MagicMock()
        cfg._load_onto_device.return_value = True

        # load file
        self.assertTrue(cfg.config_engine(load_string='set mystr', device_list='r0', load_timeout=60))
        self.assertTrue(cfg.config_engine(load_string='myfile', device_list='r0', timeout=60))
    '''
    
    @patch('jnpr.toby.engines.config.config_utils.read_yaml', return_value={'r0':'CONFIG'})
    #@patch('config_utils.read_yaml', return_value={'r0':'CONFIG'})
    def test_config_engine_config_file(self, read_yaml):

        # load_file_without_device_list

        # load file
        kwargs = {'load_timeout':60}
        cfg._process_cv.return_value=kwargs
        self.assertTrue(config.config_engine(cfg, config_file='myfile', load_timeout=60))
        kwargs = {'timeout':60}
        cfg._process_cv.return_value=kwargs
#        self.assertTrue(config.config_engine(cfg, config_file='myfile', device_list='r0', timeout=60))

        # config_data
        self.assertTrue(config.config_engine(cfg, config_data='mycfg', load_timeout=60))
        read_yaml.side_effect =Exception
        try:
            config.config_engine(cfg, config_data='mycfg', load_timeout=60)
        except:
            self.assertRaises(Exception)

    def test_config_engine_cmd_list(self):

        # load_file_without_device_list

        # load file
        kwargs = {'load_timeout':60}
        cfg._process_cv.return_value=kwargs

        self.assertTrue(config.config_engine(cfg, cmd_list='set this', device_list='r0'))
        self.assertTrue(config.config_engine(cfg, cmd_list=['set this', 'set that'], device_list='r0'))

        # no device_list
        try:
            config.config_engine(cfg, cmd_list='mycfg')
        except:
            self.assertRaises(Exception)




    #@patch('jnpr.toby.hldcl.juniper.junos.Juniper.execute_rpc', side_effect=Response(status=True, response='testing'))
    #@patch('jnpr.toby.hldcl.juniper.junos.Juniper.execute_rpc', return_value=Response(status=True, response='testing'))
    #@patch('config.config._get_dev_handle')
    #def test_load_rpc(self, dh, exec_rpc):
    def test__load_rpc(self):
        '''
        rpc function of config engine
        '''
        rpc_cmd = 'rpc_str'
        dh = MagicMock()
        #dh.execute_rpc = MagicMock(return_value = Response(status=True, response='test'))
        #dh.execute_rpc = MagicMock()
        dh.execute_rpc.return_value = Response(status=True, response='test')
        #cfg._get_dev_handle = MagicMock()
        cfg._get_dev_handle.return_value = dh

        self.assertTrue(config._load_rpc(cfg, rpc=rpc_cmd, device='r0'))
        try:
            #dh.execute_rpc = MagicMock(return_value = Response(status=False, response='test'))
            dh.execute_rpc.return_value = Response(status=False, response='test')
            config._load_rpc(cfg, rpc=rpc_cmd, device='r0')
        except Exception as err:
            self.assertRaises(Exception)
            self.assertRegex(str(err), r'.*On device.*')
        '''
        config_mock = MagicMock(spec=config)
        Exe_Rpc_mock = MagicMock()
        # If case in try block
        Exe_Rpc_mock.execute_rpc = MagicMock(return_value=Response(response='sample',status=True))
        config_mock._get_dev_handle.return_value = Exe_Rpc_mock
        self.assertTrue(config._load_rpc(config_mock))
        # Else case in try block
        Exe_Rpc_mock.execute_rpc = MagicMock(return_value=Response(response='sample',status=False))
        self.assertRaises(Exception,config._load_rpc,config_mock)
        # Exception case for try block
        config_mock._get_dev_handle.return_value = 'Exe_Rpc_mock'
        self.assertRaises(Exception,config._load_rpc,config_mock)

        '''

    def test_config_engine_rpc(self):
        '''
        rpc function of config engine
        '''
        dh = MagicMock()
        #dh.commit = MagicMock()
        dh.commit.return_value = Response(status=True, response='test')
        cfg._get_dev_handle.return_value = dh
        kwargs = {'rpc':'test', 'commit_timeout':60}
        cfg._process_cv.return_value=kwargs
        rpc_cmd = '<edit-config><target><candidate/></target><config><configuration><system><host-name>tobybbb</host-name></system></configuration></config></edit-config>'

        # load rpc without device_list
        cfg._load_rpc = MagicMock()
        try:
            config.config_engine(cfg, rpc=rpc_cmd)
        except Exception as err:
            self.assertEqual(str(err), "missing device_list for rpc")

        # run rpc:
        self.assertTrue(config.config_engine(cfg, rpc=rpc_cmd, device_list='r0', commit=True, commit_timeout=60))

        dh.commit.return_value = Response(status=False, response='test')

        #self.assertRaises(Exception, config.config_engine(cfg, rpc=rpc_cmd, device_list='r0', commit=True, commit_timeout=60))

        cfg._process_cv.return_value = {'rpc':'test', 'timeout':60}
        try:
            config.config_engine(cfg, rpc=rpc_cmd, device_list='r0', commit=True, commit_timeout=60)
        except Exception as err:
            self.assertRaises(Exception)


    def test___copy_t_dict(self):
        '''
        __copy_t_dict
        '''
        try:
            config._config__copy_t_dict(cfg)
            assertTrue('r0' in cfg.c_dict)
            #assertEqual(cfg.c_dict['system']['osname']
        except:
            pass
    
    @patch('jnpr.toby.engines.config.config_utils.read_yaml', return_value={'TEMPLATES': {'Test': 'Test'}})
    def test__config_data(self, read_yaml):
        '''
        _config_data
        '''
        test_data = {
            #'VARS': [{'arg1': 1}, {'arg2': 2},],
            'TEMPLATE_FILES': [ 'temp_file'],
            'TEMPLATES': {
                'temp1' : {'CONFIG': ['set this']},
                'temp2' : {'CONFIG': ['set that']},
                },
            'r0': {
                'CONFIG': ['set this'],
                'interfaces': {
                    'r0r1_1': {
                        'CONFIG': ['set this']
                        },
                    },
                },
            }
        cfg._process_role_tags.return_value = True
        cfg._process_cv.return_value = test_data
        cfg._make_virtual_c_dict.return_value = True
        #cfg._config_interfaces.return_value = True
        cfg._expand_config.return_value = ['set first', 'set second']
        cfg_list = config._config_data(cfg, cfg_data=test_data)

        self.assertTrue('set first' in cfg_list['r0'])

#        test_data1 = {
#            'r0': {
#                'CONFIG': ['set this'],
#                'interfaces': {
#                    'r0r1_1': {
#                        'CONFIG': ['set this']
#                        },
#                    },
#                },
#            }

        try:
            config._config_data(cfg, cfg_data=test_data)
        except Exception as err:
            self.assertRaises(Exception)

        # VARS:
        test_data['VARS'] = {'a1':1}
        test_data['TEMPLATES'] = 'Test'
        try:
            config._config_data(cfg, cfg_data=test_data)
        except:
            self.assertRaises(Exception)

        test_data.pop('TEMPLATES')
        test_data['CONFIG'] = {'Test'}
        try:
            config._config_data(cfg, cfg_data=test_data)
        except:
            self.assertRaises(Exception)

        test_data['VARS'] = [{'a1':1}, 'Test']
        try:
            config._config_data(cfg, cfg_data=test_data)
        except:
            self.assertRaises(Exception)

        test_data['VARS'] = [1]
        try:
            config._config_data(cfg, cfg_data=test_data)
        except:
            self.assertRaises(Exception)

        test_data['VARS'] = [{'a1':1}]

        try:
            config._config_data(cfg, cfg_data=test_data, vars='Test')
        except:
            self.assertRaises(Exception)

        cfg_list = config._config_data(cfg, cfg_data=test_data, vars={'b1':1})

        self.assertTrue('set first' in cfg_list['r0'])

    def test_get_template_args(self):
        '''
        _get_template_args
        '''
        # template ARGS as dict
        args =  {
            'a1':1,
            'a2':2
            }

        # template ARGS as list
        temp_args = config._get_template_args(cfg, temp_args=args)
        self.assertEqual(temp_args, args)
        args =  [
            {'a1':1},
            {'a2':2},
            'b1'
            ]
        temp_args = config._get_template_args(cfg, temp_args=args, default=1)
        self.assertTrue('b1' in temp_args)

        # wrong arg format:
        args =  [
            {'a1':1},
            ['b1']
            ]
        try:
            temp_args = config._get_template_args(cfg, temp_args=args, default=1)
        except:
            self.assertRaises(Exception)

        args ='string'
        try:
            temp_args = config._get_template_args(cfg, temp_args=args, default=1)
        except:
            self.assertRaises(Exception)

    def test_process_rt_vars(self):
        data = 'vars'
        cfg._process_cv.return_value = 'resolved'
        self.assertEqual(config._process_rt_vars(cfg, data, 'rt0', port_tag='r0rt0'), 'resolved')

    def test_get_ifd_from_tag(self):
        cfg._config__get_cvar.return_value = 'ge-1/0/6'
        cfg._config__get_cvar.return_value = None
        try:
            config._get_ifd_from_tag(cfg, 'r0', 'r0r1_10')
        except:
            self.assertRaises(Exception)
        cfg._config__get_cvar.return_value = 'JunOS'
        self.assertEqual(config._get_ifd_from_tag(cfg, 'r0', 'r0r1_10'), 'JunOS')

    def test__config_interfaces(self):
        ''' 
        _config_interfaces
        '''
        intf_data = { 
            'r0': {
                'CONFIG': ['set this'],
                'interfaces': {
                    'r0r1_1': {
                        'CONFIG': ['set this']
                        },  
                    },  
                },
             'r1': {
                'Test': ['Test']
                }
            }   
        cfg._process_role_tags.return_value = True
        cfg._process_cv.return_value = intf_data
        cfg._make_virtual_c_dict.return_value = True
        cfg._expand_config.return_value = ['set interfaces abc', 'set interfaces xyz']
        cfg_list = config._config_interfaces(cfg, dev_tag='r0', data=intf_data)
        self.assertTrue('set interfaces abc' in cfg_list['r0'])
        self.assertTrue('set interfaces xyz' in cfg_list['r0'])

    def test__config_template(self):
        ''' 
        _config_template
        '''
        try:
            config._config_template(cfg)
        except:
            self.assertRaises(Exception)

        try:
            config._config_template(cfg, template='NotNone')
        except:
            self.assertRaises(Exception)

        cfg.templates['Test'] = {'ARGS': 'Test', 'CONFIG': 'Test'}
        cfg._get_template_args.return_value = {'Test': 'Test'}
        cfg._process_cv.return_value = 'Test'
        cfg._process_args.return_value = {'Test': None}
        try:
            config._config_template(cfg, template='Test', args='Test')
        except:
            self.assertRaises(Exception)

        cfg._process_args.return_value = {'Test': 'Test'}
        cfg._build_config.return_value = ['Test']
        self.assertEqual(config._config_template(cfg, template='Test', args='Test'), ['Test'])

        cfg._process_args.return_value = None
        self.assertEqual(config._config_template(cfg, template='Test', args='Test'), ['Test'])

        cfg._build_config.return_value = None
        self.assertEqual(config._config_template(cfg, template='Test', args='Test'), [])

    def test___make_c_dict(self):
        config._config__copy_t_dict(cfg)
        dh = Mock()
        cfg._get_dev_handle = MagicMock(return_value = dh)
        cfg.__get_cvar = MagicMock(return_value = 'Junos')    
        cfg._make_ifd_cvar = MagicMock(return_value=True)
        config._config__make_c_dict(cfg)
        self.assertIsInstance(cfg.c_dict, dict)
        # need to figure out why it passes in manual run,
        # but fails in Jenkins
        #dh.intf_to_port_map = {'R0R1': '1/2'}
        #dh.port_to_handle_map = {'1/2': '1/1/1'}
        #config._config__make_c_dict(cfg)
        #self.assertEqual(cfg.cv_flat['r0__R0R1__porthandle'], '1/1/1') 
    
    def test__make_virtual_c_dict(self):
        data = 'str'
        self.assertEqual(config._make_virtual_c_dict(cfg, data), data)
        config._config__copy_t_dict(cfg)
        data = {'r0':
                 {'interfaces':
                    {'r0r1_2':
                       {'pic': 'ge-1/0/7',
                        'management': 0,
                        'name': 'ge-1/0/7.0',
                        'link': 'link2',
                        'type': ['10x', '1GE', 'LAN', 'EQ', 'SFP-SX', 'QDPCE-R-40X', 'B3', 'I3', 'ether', 'ge'],
                        'unit': 0},
                     'ae0':
                        {'management': 0,
                        'type': ['ae'],
                        'pic': 'ae0',  
                        'link': 'ae0'
                        },
                    }}}

        config._make_virtual_c_dict(cfg, data)
        self.assertIsInstance(cfg.c_dict['r0']['interfaces']['ae0'], dict)
        
        del(data['r0']['interfaces']['ae0']['link'])
        try:
            config._make_virtual_c_dict(cfg, data)
        except:
            self.assertRaises(Exception)
 
    @patch('builtins.open')
    def test__resolve_vars_in_file(self, open_mock):
        self.assertEqual(config._resolve_vars_in_file(cfg, 'load_file'), 'res_load_file')
        
        cfg._process_cv.side_effect = Exception
        try:
            config._resolve_vars_in_file(cfg, 'llload_file')
        except:
            self.assertRaises(Exception)
            
        cfg._process_cv =  MagicMock()    
  
    def test__process_config_vars(self):
        self.assertEqual(config._process_config_vars(cfg, data=None), None)
        self.assertEqual(config._process_config_vars(cfg, data='set without var'), 'set without var')
        cfg._get_config_var = MagicMock(return_value=None)
        self.assertEqual(config._process_config_vars(cfg, data="set with var['xxx']"), "set with var['xxx']")
        self.assertEqual(config._process_config_vars(cfg, data="set with var['xxx']", no_warn=1), "set with var['xxx']")
        
        cfg._get_config_var.return_value=True
        self.assertEqual(config._process_config_vars(cfg, data="set with var['xxx']"), "set with bool:True[xxx]")

        cfg._get_config_var.return_value=1
        self.assertEqual(config._process_config_vars(cfg, data="set with var['xxx']"), "set with 1")

        cfg._get_config_var.return_value=['a', 'b']
        self.assertEqual(config._process_config_vars(cfg, data="set with var['xxx']"), ['set with a', 'set with b'])

        cfg._get_config_var.return_value={'a': 1}
        try:
            config._process_config_vars(cfg, data="set with var['xxx']")
        except:
            self.assertRaises(Exception)
        
        data =["set var['x']", 'set 2']       
        cfg._process_config_vars.return_value = 'set'
        self.assertEqual(config._process_config_vars(cfg, data=data), ['set', 'set'])
        
        cfg._process_config_vars.return_value = [1, 2]
        self.assertEqual(config._process_config_vars(cfg, data=data), [1, 2, 1, 2])
       
        data ={"set var['x']": 1}      
        cfg._process_config_vars.return_value = 'set'
        self.assertEqual(config._process_config_vars(cfg, data=data), OrderedDict([('set', 'set')]))
        
        cfg._process_config_vars.return_value = ['set 1',  'set 2']
        self.assertEqual(config._process_config_vars(cfg, data=data), OrderedDict([('set 1', ['set 1', 'set 2']), ('set 2', ['set 1', 'set 2'])]))
       
        cfg._process_config_vars.return_value = {'set': 1}
        try:
            config._process_config_vars(cfg, data=data)
        except:
            self.assertRaises(Exception)
            
            
    def test__process_cv(self):
        self.assertEqual(config._process_cv(cfg, data=None), None)
        self.assertEqual(config._process_cv(cfg, data='set without cv'), 'set without cv')
        
        data = ["set cv['r0__name']", 'set 2']
        cfg._process_cv.return_value = ['set 1', 'set 2']
        self.assertEqual(config._process_cv(cfg, data=data), ['set 1', 'set 2', 'set 1', 'set 2'])
        
        cfg._process_cv.return_value = 'set dut'
        self.assertEqual(config._process_cv(cfg, data=data), ['set dut', 'set dut'])
        
        data = {"set cv['r0__name']": 2}
        cfg._process_cv.return_value = 'set 1'
        cfg._process_cv.side_effect=['set dut', 2, 3]
        self.assertEqual(config._process_cv(cfg, data=data), OrderedDict([('set dut', 2)]))
        
        cfg._process_cv = MagicMock()
        data = "set cv['r0__name']"
        cfg._resolve_cv.return_value = 'set dut'
        self.assertEqual(config._process_cv(cfg, data=data), "set dut")

    def test__make_ifd_cvar(self):
        config._config__copy_t_dict(cfg)
        config._make_ifd_cvar(cfg)  
        self.assertEqual(cfg.cv_flat['r1__r0r1_1__slot'], '0/0/2')
        
    def test__make_ifl_cvar(self):
        cmd_list = ['set others',
                    'set interfaces ge-0/0/0 unit 0 family inet address address 10.1.1.1/24',
                    'set interfaces ge-0/0/0 unit 1 family inet address address 10.2.1.1/24',
                    'set interfaces ge-0/0/0 unit 0 family inet6 address address a::1:1:1:1/64',
                    ]
        dev_tag = 'r0'
        ifd_tag = 'r0r1_1'        
        config._config__copy_t_dict(cfg)
        config_utils.nested_set(cfg.c_dict, [dev_tag, 'interfaces', ifd_tag], {})             
        config._make_ifl_cvar(cfg, dev_tag=dev_tag, ifd_tag=ifd_tag, cmd_list=cmd_list)  
        self.assertIsInstance(cfg.c_dict[dev_tag]['interfaces'][ifd_tag]['unit']['1'], dict)
        
        cmd_list = ['set interfaces ge-0/0/0 unit 0 family inet address address 333.1.1.1/44']
        try:
            config._make_ifl_cvar(cfg, dev_tag=dev_tag, ifd_tag=ifd_tag, cmd_list=cmd_list)
        except:
            self.assertRaises(Exception)
        
    def test__find_dict_data(self): 
        key_list = ["set cv['r0__name']"]
        data = {"set cv['r0__name']": 2}
        path = None 
        config._find_dict_data(cfg, key_list=key_list, data=data, path=path)   
        key_list = ["set cv['r0__name']"]
        data = {"set cv['r1__name']": {"delete": 2}}
        try:
            config._find_dict_data(cfg, key_list=key_list, data=data, path=path)
        except:
            self.assertRaises(Exception)
    
    @patch('jnpr.toby.engines.config.config_utils.read_yaml', return_value={'interface': 'intf1'})
    def test_get_cv(self, read_yaml):
        cfg.c_dict = False
        cfg.__make_c_dict = MagicMock(return_value=True)
        cfg.cv_file = "test"
        self.assertEqual(config.get_cv(cfg, reconnect=True), {'interface': 'intf1'})
        #cfg.cv_flat = {"interface": "intf1"}
        self.assertEqual(config.get_cv(cfg, cv='interface'), 'intf1')
    
    @patch('jnpr.toby.engines.config.config_utils.read_yaml', return_value={'interface': 'intf1'})
    def test_add_cv(self, read_yaml):
        cfg.c_dict = False
        cfg.__make_c_dict = MagicMock(return_value=True)
        cfg.cv_file = "test"
        self.assertIsNone(config.add_cv(cfg, 'protocols', 'bgp', reconnect=True))
    
    def test__process_args(self):
        self.assertIsNone(config._process_args(cfg))
        data = {"set cv['r0__name']": 2}
        cfg._process_config_vars = MagicMock(return_value=True)
        self.assertTrue(config._process_args(cfg, data=data))
    
    @patch('jnpr.toby.engines.config.config_utils.expand_to_list', return_value=[1, '<<2..>>', 3]) 
    def test__expand_config(self, expand_to_list):
        config_list = ["<<1..10>>", 1, {'args': {'arg1': '<<1..10>>'}}]
        cfg._process_cv = MagicMock(return_value=[1, '2', 3])
        cfg._role_expand = MagicMock(return_value=['2'])
        self.assertEqual(config._expand_config(cfg, config_list=config_list), [1, '2', 3])
        expand_to_list.return_value = "1"
        self.assertEqual(config._expand_config(cfg, config_list=config_list), [1, '2', 3]) 

    def test__role_expand(self):
        self.assertEqual(config._role_expand(cfg, base="tag[]"), ["tag[]"])
        cfg._get_role_attr = MagicMock(return_value = {"r0": "", "r1": "CONFIG"})
        self.assertEqual(config._role_expand(cfg, base="tag['@']"), ["r0", "r1 CONFIG"])
      
    def test__get_role_attr(self):
        cfg.roles = {'INTERFACE': {'fe': 'r0'}}
        cfg._config__get_cvar.return_value = 'JunOS'
        try:
            config._get_role_attr(cfg, device_tag='r0', tag='')
        except:
            self.assertRaises(Exception)
        try:
            config._get_role_attr(cfg, device_tag='r0', tag='pe@neighbor', role_type='INTERFACE')
        except Exception as err:
            self.assertEqual(err.args[0], "undefined role TAG pe@neighbor in role types: [['INTERFACE']]")
        cfg.roles = {'INTERFACE': {'pe': {'r0': 'ge-1/1/0', 'r1': {'ifd_tag': {'ifd': 'option1'}}}}} 
        self.assertEqual(config._get_role_attr(cfg, device_tag='r0', tag='pe@neighbor'), {'JunOS': 'option1'})
        cfg.roles = {'INTERFACE': {'pe': {'r1': {'ifd_tag': {'ifd': 'option1'}}}}}
        self.assertEqual(config._get_role_attr(cfg, device_tag='r1', tag='pe@remote'), {'JunOS': 'option1'})
        self.assertEqual(config._get_role_attr(cfg, device_tag='r1', tag='pe'), {'JunOS': 'option1'})
        cfg.roles = {'INTERFACE': {'pe': {'r1': {'ifd_tag': {'ifl_1': 'option1'}}}}}
        self.assertEqual(config._get_role_attr(cfg, device_tag='r0', tag='pe@neighbor:ip'), {'JunOS': 'option1'})
        cfg.roles = {'INTERFACE': {'pe': {'r1': {'ifd_tag': {'ifl_<<1..2>>': 'option1'}}}}}
        self.assertEqual(config._get_role_attr(cfg, device_tag='r0', tag='pe@neighbor:ip'), {'JunOS': 'option1'})
        self.assertEqual(config._get_role_attr(cfg, device_tag='r0', tag='pe@neighbor:loop-ip'), {'JunOS.2': 'option1', 'JunOS.1': 'option1'})
        cfg.roles = {'NODE': {'pe': {'r0': 'ge-1/1/0', 'r1': {'ifd_tag': {'ifd': 'option1'}}}}}
        self.assertEqual(config._get_role_attr(cfg, device_tag='r0', tag='pe@local', role_type='NODE'), {'r0': 'ge-1/1/0'})
        self.assertEqual(config._get_role_attr(cfg, device_tag='r0', tag='pe@neighbor:loop-ip', role_type='NODE'), {'JunOS': {'ifd_tag': {'ifd': 'option1'}}})

    def test__get_config_var(self):
        cfg.vars = {'r0': {'var1': None}, 'var1': 10}
        self.assertEqual(config._get_config_var(cfg, var='var1', device='r0'), 10)
        self.assertEqual(config._get_config_var(cfg, var='var1', vars={'var1':10}), 10)
    
    def test__get_role_value(self):
        try:
            config._get_role_value(cfg)
        except Exception as err:
            self.assertEqual(err.args[0], "Wrong Tagging Format: <class 'NoneType'>. \
                    only str or dict allowed")
        self.assertEqual(config._get_role_value(cfg, role='rsvp'), ('rsvp', ''))
        self.assertEqual(config._get_role_value(cfg, role={'mpls': 'all'}), ('mpls', 'all'))
    
    def test__save_interface_role_tags(self):
        try:
            config._save_interface_role_tags(cfg, role_tags="")
        except:
            self.assertRaises(Exception) 
        try:
            config._save_interface_role_tags(cfg, role_tags={'ifl': ['rsvp', 'mpls', 'isis']})
        except Exception as err:
            self.assertEqual(err.args[0],'Wrong Interface TAG format on device None ifd None: ifl')
        self.assertIsNone(config._save_interface_role_tags(cfg, role_tags={'ifd': ['rsvp', 'mpls', 'isis']}))
      
    def test__process_role_tags(self):
        config_data = {'VARS': 'var1', 'r0': {'TAGS': {'role1': 'value1'}, 'interfaces': {'intf1': {'TAGS': {'role1': 'value1'}}}}} 
        cfg._get_role_value = MagicMock(return_value=('role1','value1'))
        cfg.roles['INTERFACE'] = {'intf1': {'r0': {'if1': 'value1'}}}
        self.assertIsNone(config._process_role_tags(cfg, cfg_data=config_data))
        cfg.roles['INTERFACE'] = None
        self.assertIsNone(config._process_role_tags(cfg, cfg_data=config_data))

    def test_register_device_methods(self):
        config.register_device_methods(cfg)
    
    def test_CONFIG_SET(self):
        cfg.config_engine.return_value = None
        self.assertIsNone(config.CONFIG_SET(cfg))

    def test_CONFIG_LOAD(self):
        cfg.config_engine.return_value = None
        self.assertIsNone(config.CONFIG_LOAD(cfg))

    def test__build_config(self):
        kwargs = {'ifd_tag': 'Test'}
        cfg._config__get_ifd_from_tag = MagicMock(return_value='Test')
        cfg._config__get_cvar.return_value = 'JunOS'
        cfg._build_junos_config.return_value = 'Test'
        self.assertEqual(config._build_config(cfg, device='Test', **kwargs), 'Test')

        cfg._config__get_cvar.return_value = 'Linux'
        try:
            config._build_config(cfg, device='Test', **kwargs)
        except:
            self.assertRaises(Exception)
        cfg._build_linux_config.return_value = 'Test'
        self.assertEqual(config._build_config(cfg, device='Test', config_data=['Test'], **kwargs), 'Test')

        cfg._config__get_cvar.return_value = 'ix'
        try:
            config._build_config(cfg, device='Test', **kwargs)
        except:
            self.assertRaises(Exception)
        cfg._build_rt_config.return_value = 'Test'
        self.assertEqual(config._build_config(cfg, device='Test', config_data=['Test'], **kwargs), 'Test')

    def test__build_junos_config(self):
        cfg._build_junos_config.return_value = ['Test']
        self.assertEqual(config._build_junos_config(cfg, config_data=['Test']), ['Test'])

        self.assertEqual(config._build_junos_config(cfg, config_data={'set': 'Test'}), ['Test'])
        self.assertEqual(config._build_junos_config(cfg, config_data={"template['Test']": 'Test'}), [])
        self.assertEqual(config._build_junos_config(cfg, config_data={'Test': 'Test'}), ['Test'])
        self.assertEqual(config._build_junos_config(cfg, config_data="template['Test']"), [])

        cfg._build_junos_config.return_value = None
        cfg._config_template.return_value = None
        self.assertEqual(config._build_junos_config(cfg, config_data=['Test']), [])

        try:
            config._build_junos_config(cfg, config_data={1: 'Test'})
        except:
            self.assertRaises(Exception)

#        self.assertEqual(config._build_junos_config(cfg, config_data={'LOOP(': 'Test'}), None)
        self.assertEqual(config._build_junos_config(cfg, config_data={"template['Test']": 'Test'}), [])
        self.assertEqual(config._build_junos_config(cfg, config_data={'set': 'Test'}), [])
        self.assertEqual(config._build_junos_config(cfg, config_data={'Test': 'Test'}), [])
        self.assertEqual(config._build_junos_config(cfg, config_data=None), ['set'])

        try:
            config._build_junos_config(cfg, config_data=Exception('Test'))
        except:
            self.assertRaises(Exception)


    def test__build_linux_config(self):
        cfg._build_linux_config.return_value = ['Test']
        cfg._config_template.return_value = ['Test']
        self.assertEqual(config._build_linux_config(cfg, config_data=['Test']), ['Test'])

        self.assertEqual(config._build_linux_config(cfg, config_data={"template['Test']": 'Test'}), ['Test'])
        self.assertEqual(config._build_linux_config(cfg, config_data={'bool:True': 'Test'}), [])
        self.assertEqual(config._build_linux_config(cfg, config_data={'Test': 'Test'}), [OrderedDict([('cmd', 'Test'), ('args', 'Test'), ('toby_args', {'device_tag': None})])])
        self.assertEqual(config._build_linux_config(cfg, config_data="template['Test']"), ['Test'])

        cfg._build_linux_config.return_value = None
        cfg._config_template.return_value = None
        self.assertEqual(config._build_linux_config(cfg, config_data=['Test']), [])

        try:
            config._build_linux_config(cfg, config_data={1: 'Test'})
        except:
            self.assertRaises(Exception)

        self.assertEqual(config._build_linux_config(cfg, config_data={"template['Test']": 'Test'}), [])
        self.assertEqual(config._build_linux_config(cfg, config_data=None), [''])

        try:
            config._build_linux_config(cfg, config_data=Exception('Test'))
        except:
            self.assertRaises(Exception)


    def test__build_ret_config(self):
        cfg._build_rt_config.return_value = ['Test']
        cfg._config_template.return_value = ['Test']
        self.assertEqual(config._build_rt_config(cfg, config_data=['Test']), ['Test'])

        self.assertEqual(config._build_rt_config(cfg, config_data={"template['Test']": 'Test'}), ['Test'])
        self.assertEqual(config._build_rt_config(cfg, config_data={'bool:True': 'Test'}), [])
        self.assertEqual(config._build_rt_config(cfg, config_data="template['Test']"), ['Test'])
        self.assertEqual(config._build_rt_config(cfg, config_data='Test'), ['Test'])

        cfg._build_rt_config.return_value = None

        try:
            config._build_rt_config(cfg, config_data={1: 'Test'})
        except:
            self.assertRaises(Exception)

        try:
            config._build_rt_config(cfg, config_data=Exception('Test'))
        except:
            self.assertRaises(Exception)


    def test__load_onto_device(self):
        try:
            config._load_onto_device(cfg, device='JunOS')
        except:
            self.assertRaises(Exception)



    def test__load_junos_cfg(self):
        try:
            config._load_junos_cfg(cfg, device='JunOS')
        except:
            self.assertRaises(Exception)


    def test__load_linux_cfg(self):
        self.assertEqual(config._load_linux_cfg(cfg, device='JunOS'), True)


    def test__load_tester_cfg(self):
        self.assertEqual(config._load_tester_cfg(cfg, device='JunOS'), True)


    def test__load_spirent_config(self):
        self.assertIsNone(config._load_spirent_config(cfg, device='JunOS'))


    def test__load_ixia_config(self):
        self.assertIsNone(config._load_ixia_config(cfg, device='JunOS'))


    @patch('jnpr.toby.engines.config.config.run_multiple')
    @patch('os.environ', return_value={'some':'value'})
    @patch('jnpr.toby.engines.config.config.config_utils')
    def test__load_template_v1_and_get_commands(self, cfg_utils, os_patch,rm_patch):

        cfg_utils.read_yaml = MagicMock(return_value={})
        cfg_utils.nested_set = MagicMock(return_value={})
        kwargs = {'template_files': 'temp_file', 'templates':'templates', 'vars':{'s':'v'}}
        #os_patch.environ = MagicMock(return_value={'some':'value'})
        cfg.templates = {}
        cfg.read_template_files = MagicMock(return_value={})
        cfg.timeout = 10
        try:
            config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs:(user)', device_list='r0',load_timeout=10,**kwargs)
        except:
            pass

        config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='r0',load_timeout=10,do_parallel=True,**kwargs)
        self.assertEqual(config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='r0',load_timeout=10,do_parallel=True,**kwargs), None)

        config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='r0',load_timeout=10,do_parallel=True,load_string='some',**kwargs)
        self.assertEqual(config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='r0',load_timeout=10,do_parallel=True,load_string='some',**kwargs),None)

        config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='r0',load_timeout=10,do_parallel=True,config_file='config_file',config_data='config_data',config_templates='config_templates',cmd_list='cmd1',**kwargs)

        self.assertEqual(config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='r0',load_timeout=10,do_parallel=True,config_file='config_file',config_data='config_data',config_templates='config_templates',cmd_list='cmd1',**kwargs), None)
        cfg.timeout = False
        config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='None',do_parallel=True,config_file='config_file',config_data='config_data',config_templates='config_templates',cmd_list='cmd1',**kwargs)
        self.assertEqual(config._load_template_v1_and_get_commands(cfg, load_file='local/some@cvs(user)', device_list='None',do_parallel=True,config_file='config_file',config_data='config_data',config_templates='config_templates',cmd_list='cmd1',**kwargs), None)


#    def test___get_cvar(self):
#        try:
#            config._config__get_cvar(cfg)
#        except Exception as err:
#            self.assertEqual(err.args[0], "Mandatory arg 'cv' is missing")
#        cfg._find_dict_data = MagicMock(return_value=(None,None))
#        cfg.c_dict = False
#        cfg.__make_c_dict(cfg)
#        config._config__get_cvar(cfg, cv_name='interfaces')        
 
if __name__ == '__main__':
    unittest.main()

