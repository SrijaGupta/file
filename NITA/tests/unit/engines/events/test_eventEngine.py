#!/usr/local/bin/python3

import unittest2 as unittest
import builtins
from mock import patch, Mock, MagicMock, call
from jnpr.toby.init.init import init
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.juniper.junos import Juniper
from collections import OrderedDict, defaultdict
from jnpr.toby.utils.Vars import Vars
import jnpr.toby.engines.config.config_utils as config_utils
import jnpr.toby.engines.events.event_engine_utils as ee_utils
from jnpr.toby.engines.events.eventEngine import eventEngine
from jnpr.toby.engines.events.event_engine_utils import me_object
from jnpr.toby.engines.events.event_engine_utils import device_handle_parser
from jnpr.toby.engines.events.event_engine_utils import interface_handler_to_ifd
from jnpr.toby.engines.events.event_engine_utils import elog

class TesteventEngine(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = self
        t.log = MagicMock(return_value=True)
        t.log_console = MagicMock(return_value=True)

    def test__init(self):
        eventMock= MagicMock(spec=eventEngine())
        self.assertIsInstance(eventMock, eventEngine)
        
    
    
    @patch('jnpr.toby.engines.events.event_engine_utils.elog', return_value='True')
    def test_call_keyword(self, elog_patch):
        dh = MagicMock()
        eventMock= MagicMock(spec=eventEngine())
        eventEngine._call_keyword(eventMock, kwargs = {'debug_log_on' : "val"})
        self.assertFalse(eventEngine._call_keyword(eventMock, kwargs = {'debug_log_on' : "val"}))  
    
    @patch('jnpr.toby.engines.events.eventEngine.re')   
    def test_update_events(self, mock_re):
        dh = MagicMock()
        eventMock= MagicMock(spec=eventEngine())
        mock_re.match.return_value=False
        eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'method' : 'jnpr.toby.engines.events'}}})
        self.assertTrue(eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'method' : 'jnpr.toby.engines.events'}}}))
        mock_re.match.return_value=False
        eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'method' : 'jnpr.toby'}}})
        self.assertTrue(eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'method' : 'jnpr.toby'}}}))
        module_name = MagicMock()
        module_name.endswith=True
        mock_re.match.return_value=True
        eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'method' : '(jnpr.toby)'}}})
        self.assertTrue(eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'method' : '(jnpr.toby)'}}}))
        eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'args' : 'jnpr.toby.engines.events'}}})
        self.assertEqual({'event': {'action': {'args': 'jnpr.toby.engines.events'}}},eventEngine._update_events(eventMock, events={ 'event' : {'action' : {'args' : 'jnpr.toby.engines.events'}}}))    
        
    def test_process_method_args(self):
        dh = MagicMock()
        eventMock= MagicMock(spec=eventEngine())
        eventEngine._process_method_args(eventMock, 'restart_daemonn', trigger_method = { 'type' : {"ROBOT_keyword" : "val"}})
        self.assertTrue(eventEngine._process_method_args(eventMock, 'restart_daemonn', trigger_method = { 'type' : {"ROBOT_keyword" : "val"}}))
        #eventEngine._process_method_args(eventMock, 'restart_daemon', trigger_method = {'args':'=33=44'})
        try:
           eventEngine._process_method_args(eventMock, 'restart_daemon', trigger_method = { 'args' : "**kwargs"})
        except:
            self.assertRaises(Exception)                
        
        
    @patch('jnpr.toby.engines.events.event_engine_utils.device_handle_parser', return_value='r0')
    @patch('jnpr.toby.engines.events.event_engine_utils.me_object', return_value=True)
    @patch('jnpr.toby.engines.events.event_engine_utils.get_dh_name', return_value='dname')
    @patch('jnpr.toby.engines.events.event_engine_utils.get_dh_tag', return_value='dtag')
    def test_run_event(self, dtag, dh_nameMock, meMock, dhMock):
        eventMock= MagicMock(spec=eventEngine())
        dh = MagicMock()
        eventEngine.run_event(eventMock, 'restart_daemon', device=dh)
        eventEngine.run_event(eventMock, 'restart_daemon', device=dh, duration=0.01, interval=0.001)
        eventEngine.run_event(eventMock, 'restart_daemon', device=dh, interface='xe=0/0/0')
        self.assertTrue( eventEngine.run_event(eventMock, 'restart_daemon', device=dh))
        self.assertTrue(eventEngine.run_event(eventMock, 'restart_daemon', device=dh, duration=0.01, interval=0.001))
        self.assertTrue(eventEngine.run_event(eventMock, 'restart_daemon', device=dh, interface='xe=0/0/0'))            
    
    @patch('jnpr.toby.engines.events.eventEngine.config_utils.read_yaml', return_value = {'abc': '222'})
    def test_register_event(self, read_yaml_patch):
        dh = MagicMock()
        eventMock = MagicMock(spec=eventEngine())
        eventEngine.register_event(eventMock, 'file')
        eventMock.events_registered = False
        eventEngine.register_event(eventMock, file ='update')
        test = "value"
        eventEngine.register_event(eventMock, test)
        self.assertFalse( eventEngine.register_event(eventMock, args = 'val' , kwargs = {'file' : "hiii"}))
        
    
    @patch('jnpr.toby.engines.events.event_engine_utils.device_handle_parser', return_value='r0')
    @patch('jnpr.toby.engines.events.event_engine_utils.me_object', return_value=True)
    @patch('jnpr.toby.engines.events.event_engine_utils.get_dh_name', return_value='dname')
    @patch('jnpr.toby.engines.events.event_engine_utils.get_dh_tag', return_value='dtag')
    def test_run_event(self, dtag, dh_nameMock, meMock, dhMock):
        eventMock= MagicMock(spec=eventEngine())
        dh = MagicMock()
        eventEngine.run_event(eventMock, 'restart_daemon', device=dh)
        eventEngine.run_event(eventMock, 'restart_daemon', device=dh, duration=0.01, interval=0.001)
        eventEngine.run_event(eventMock, 'restart_daemon', device=dh, interface='xe=0/0/0')

    
    def test_confirm_event_state(self):
        dh = MagicMock()
        eventMock= MagicMock(spec=eventEngine())
        result=eventEngine._confirm_event_state(eventMock, 'restart_daemon')
        self.assertEqual(result,True)

    def test_get_event_functions(self):
        dh = MagicMock()
        eventMock= MagicMock(spec=eventEngine())
        try:
           result=eventEngine._get_event_functions(eventMock, 'restart_daeMOn')
           self.assertEqual(result,'restart_daemon')
        except:
           self.assertRaises(Exception)
if __name__ == '__main__':
    unittest.main()

