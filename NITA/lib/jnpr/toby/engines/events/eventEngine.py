"""
Copyright (C) 2015-2016, Juniper Networks, Inc.
All rights reserved.
Authors:
    jpzhao, bphillips, ajaykv
Description:
    Toby Network Event Engine.


"""
# pylint: disable=locally-disabled,undefined-variable,invalid-name

import re
#import copy
import os
import sys
#import types
#import pprint
import time
import importlib
import inspect
from robot.libraries.BuiltIn import BuiltIn as RobotBuiltIn
from jnpr.toby.utils.Vars import Vars
from jnpr.toby.engines.events.event_engine_utils import elog
import jnpr.toby.engines.events.event_engine_utils as ee_utils
import jnpr.toby.engines.config.config_utils as config_utils



class eventEngine(object):
    """
    Class of Toby Event Engine
    - A network event is a disruption to normal network operational evironment('steady states'),
      which usually causes topology/routing information changes, that requires the network
      to react to the changes in order to maintain network connectivity.
    - triggering an event in a testbed will test the DUTs capability to recover from the event(s).
    - Generic Event engine handles all event actions in a consistent way
      . standard logging for easy debugging
      . arg handling
      . iteration/duration/timeout/exception handling

     - Extensible to add new events in a consistent style
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        # get the event/check methods/functions from a register file
        #self.events_registered = self.register_event()
        self.events_registered = {}
        self.response = ''
        self.status = ''
        #self.error_msg = ''
        self.time_spent = None
        self.src_path = None
        if Vars().get_global_variable('${SUITE_SOURCE}'):
            self.src_path = os.path.dirname(Vars().get_global_variable('${SUITE_SOURCE}'))
        else:
            self.src_path = os.getcwd()

        # the built-in event yaml file are in the same location of eventEngine.
        self.ee_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) #
        if self.ee_path not in sys.path:
            sys.path.append(self.ee_path)

    def _call_keyword(self, *args, **kwargs):
        '''
        call Robot keyword inside event engine
        '''
        # TBD: if it is Toby keyword, call them directly with Python code?
        my_args = []
        keyword = None
        if kwargs:
            for key, val in kwargs.items():
                if key == 'ROBOT_keyword':
                    keyword = val
                else:
                    my_args.append('{}={}'.format(key, val))

        if keyword is None:
            elog('_call_keyword(): no keyword passed in via ROBOT_keyword')
            return False

        # run user picked Robot keyword
        elog('debug', '====== Robot keyword {} with args: {}'.format(keyword, my_args))
        res = RobotBuiltIn().run_keyword_and_return_status(keyword, *my_args)
        return res

    def _update_events(self, events):
        '''
        updagate events to ee's attribute 'events_registered'
        '''
        registered_events = {}
        for event in events:
            registered_events[event] = {}
            for action in events[event]:    # trigger or check
                if events[event][action].get('method'):
                    method_name_with_path = events[event][action]['method'].strip('\'\"')
                    func_name = method_name_with_path
                    #module_name = 'jnpr.toby.engines.events.triggers'
                    module_name = 'triggers'
                    if '.' in method_name_with_path:
                        module_name, func_name = method_name_with_path.rsplit('.', 1)
                    if module_name.endswith(')'):
                        # dealing with a class method here
                        class_pkg, class_name = module_name.rsplit('.', 1)
                        class_name = class_name.rstrip(r'()')
                        class_obj = getattr(importlib.import_module(class_pkg), class_name)()
                        method = getattr(class_obj, func_name)
                        config_utils.nested_set(registered_events[event],
                                                [action, 'type', 'class_obj'], class_obj)
                    elif re.match(r'ROBOT:', func_name):
                        # A Robot keyword
                        # 1. any Robot keyword user defined : done
                        # 2. Todo: Toby keywords, pre-imported?( verify, execute_cli_.., )
                        #    any benefit of doing that?
                        method = self._call_keyword
                        keyword = re.sub(r'ROBOT:', '', func_name).strip()
                        config_utils.nested_set(registered_events[event],
                                                [action, 'type', 'ROBOT_keyword'], keyword)
                    else:
                        # a function
                        method = getattr(importlib.import_module(module_name), func_name)
                        config_utils.nested_set(registered_events[event],
                                                [action, 'type', 'function'], func_name)

                    config_utils.nested_set(registered_events[event], [action, 'method'], method)
                if events[event][action].get('args'):
                    # tbd: processing tv/cv in args?
                    # proc_args =
                    config_utils.nested_set(registered_events[event], [action, 'args'],
                                            events[event][action]['args'])

        #update registered events
        config_utils.nested_update(self.events_registered, registered_events)

        return registered_events

    def register_event(self, *args, **kwargs):
        '''
        register events
        '''
        events = {}
        if not self.events_registered:
            # import Event Engine BuiltIn events file
            print('+++++++++++++++ builtin event file path', self.ee_path)
            events = config_utils.read_yaml(\
                            file=self.ee_path + '/Builtin_Events.yaml')
            self._update_events(events)

        if kwargs.get('file'):
            events.update(config_utils.read_yaml(file=kwargs['file']))
            self._update_events(events)
        elif args:
            # expecting one arg as event name
            the_event = args[0].lower().strip('\'\" ')
            if ' ' in the_event:
                the_event = '_'.join(the_event.split())
            if not events.get(the_event):
                # a new event
                t.log('\n=== adding a new event: {}'.format(the_event))
                events[the_event] = {}
            else:
                t.log('debug', 'updating existing event: ' + the_event)

            event_args = ('trigger_method', 'trigger_args', 'check_method', 'check_args')
            for arg_key in kwargs:
                if arg_key in event_args:
                    key_list = arg_key.split('_')
                    config_utils.nested_set(events[the_event], key_list, kwargs[arg_key])

            self._update_events(events)

        return self.events_registered

    def _get_event_functions(self, event):
        '''
        only 'registered events with methods, and CLI/VTY commands are accepted
        so that no user defined config can 'sneak in' via event for example
        '''
        nevent = re.sub(r'\s+', '_', event.strip()).lower()
        if self.events_registered.get(nevent):
            return self.events_registered[nevent]
        else:
            raise Exception('cannot find this event: ' + event)
            # maybe just return None


    def _process_method_args(self, event, trigger_method, **kwargs):
        '''
        process args and find missing args of a trigger method
        '''
        trg_kwargs = {}
        if trigger_method.get('args'):
            if '**kwargs' in trigger_method['args']:
                trg_kwargs.update(kwargs)

            for default_targ in trigger_method.get('args'):
                targ = default_targ.strip(' \'\"')
                if re.match(r'\*args|\*\*kwargs', targ):
                    continue
                tval = None
                if '=' in default_targ:
                    matched = re.match(r'([^=]+)=([^=]+)$', targ)
                    targ = matched.group(1)
                    tval = matched.group(2)
                if targ in kwargs:
                    trg_kwargs.update({targ: kwargs[targ]})
                elif tval is not None:
                    trg_kwargs.update({targ: tval})  # take registered default value
                else:
                    raise Exception('missing mandatory argument "{}" in event "{}"'.\
                                    format(default_targ, event))

        ## adjust args depending on the type of method
        if trigger_method['type'].get('ROBOT_keyword'):
            trg_kwargs['ROBOT_keyword'] = trigger_method['type']['ROBOT_keyword']

        return trg_kwargs

    ##### exposed keyword and high level functions
    def run_event(self, event, *args, **kwargs):
        """
        This is the exposed Event keyword to toby/Robot
        - Note: Only take the trigger args and check args as named args


        """

        if not self.events_registered:
            # get the BuiltIn list of events
            self.events_registered = self.register_event()

        iteration = int(kwargs.get('iteration', 1))
        device = kwargs.get('device', None)
        #interface = kwargs.get('interface', None)
        kwargs['me_object'] = ee_utils.me_object()

        dev_name = ''
        dev_tag = ''
        if device:
            dh = ee_utils.device_handle_parser(device=device)
            #if dh.__dict__.get('TE') is None:
            #    dh.TE = {}
            kwargs['dh'] = dh
            dev_name = ee_utils.get_dh_name(dh)
            dev_tag = ee_utils.get_dh_tag(dh)

        # get all the functions related to this event
        func_list = self._get_event_functions(event)
        trg_kwargs = {}
        if func_list['trigger'].get('args'):
            trg_kwargs = self._process_method_args(event, func_list['trigger'], **kwargs)

        chk_kwargs = {}
        if kwargs.get('enable_check'):
            if func_list.get('check') and func_list['check'].get('args'):
                chk_kwargs = self._process_method_args(event, func_list['check'], **kwargs)
  
        start_time = time.time()
        elog('==== event <{}> starts:'.format(event))

        # find duration/iteration.
        interval = float(kwargs.get('interval', 5))  # unit second.  0.01 also works( msec)

        # up+down considered one iteration
        duration = kwargs.get('duration', None)
        if duration is not None:
            duration = float(duration)
            iteration = 99999999  # duration takes control

        # execute

        # todo: running in parallel, (noise at back ground)
        # todo: multiple events
        # todo: as a seperate tool, or multi-thread, or async?

        error = 0
        for itr in range(iteration):
            elog('== BEGIN: Event {} # {}: {}({})'.format(event, str(itr+1), dev_tag, dev_name), \
                        annotate=True, **kwargs)
            #elog('== BEGIN: Event {} #{}: {}({})/{}'.format(event, str(itr+1), dh.tag, \
                        #dh.name, ifd), annotate=True, **kwargs)
            #look for function first

            kwargs['event_iteration'] = itr + 1

            res = func_list['trigger']['method'](**trg_kwargs)
            t.log('debug', 'run_event trigger returned {}'.format(str(res)))
            if res is False:
                error += 1
            elif not self._confirm_event_state(event, check_kwargs=chk_kwargs, **kwargs):
                error += 1
            if iteration > 1 and itr < iteration - 1:
                t.log('debug', 'wait for {} seconds before next iteration'.format(str(interval)))
                time.sleep(interval)
            if duration and time.time() - start_time > duration:
                print('Event duration is up')
                break
            #if time.time() - start_time > timeout
                # break


        end_time = time.time()
        self.time_spent = end_time - start_time
        elog('==== END: Event <{0}>, took {1:.2f} seconds'.format(event, self.time_spent), \
                    annotate=True, **kwargs)
        # return True/false or raise exception when failed??
        #ret = False if error > 0  else True
        if error > 0:
            # Todo: an eventException to standardize error msg
            #raise Exception('event failed with error: ' + str(error))
            elog('error', 'event failed with error: ' + str(error))
            return False
        return True

    def _confirm_event_state(self, event, **kwargs):
        '''
        check to confirm event status
        '''
        if not kwargs.get('enable_check'):
            return True
        self.status = True
        func_list = self._get_event_functions(event)

        st_check = False
        if func_list.get('check'):
            check_kwargs = kwargs.get('check_kwargs', {})
            # time in float means it can take millisecond
            timeout = float(kwargs.get('timeout', 30))
            check_interval = float(kwargs.get('check_interval', 1))
            start = time.time()
            while time.time() - start < timeout:
                res = func_list['check']['method'](**check_kwargs)
                if res:
                    t.log('debug', 'state confirmed')
                    duration = time.time() - start
                    st_check = duration
                    t.log('takes {} for {} to finish'.format(duration, event))
                    break
                time.sleep(check_interval)
            else:
                elog('error', '== Check event {} status failed'.format(event))
                st_check = False
        else:
            t.log('warn', 'No check function for {}, skip'.format(event))
            st_check = True

        return st_check

