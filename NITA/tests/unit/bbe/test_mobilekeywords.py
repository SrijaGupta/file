import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbeconfig import BBEConfig
from jnpr.toby.bbe.bbevar.bbevars import BBEVars, BBEVarDevice
from jnpr.toby.bbe.bbevar.subscribers import CUPSSubscribers
import builtins
import itertools
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.bbe.mobilekeywords import mobile_configure_sgi_traffic, mobile_get_stats_results, \
    mobile_get_sx_association_stats, mobile_get_sx_session_stats, mobile_get_traffic_stats, mobile_login_sx_session, \
    mobile_logout_sx_session, mobile_calculate_router_stats, mobile_calculate_tester_stats, mobile_pause_sgi_traffic, \
    mobile_resume_sgi_traffic, mobile_configure_bearers, mobile_configure_modification_tft_sets, \
    mobile_configure_dhcp_ue, mobile_control_bearers, mobile_verify_traffic, mobile_remove_traffic, \
    mobile_get_stats_results, mobile_get_packetloss, mobile_create_tft_dict, mobile_get_ue_session_info, \
    mobile_configure_lawful_intercept, mobile_create_usage_rule_dict, mobile_configure_usage_rules, \
    mobile_load_custom_pfcp_message

class Testmobilekeywords(unittest.TestCase):
    def setUp(self):
        builtins.t = MagicMock(spec=init)
        builtins.t.get_handle.return_value.os = 'SPIRENT'
        builtins.bbe = MagicMock(spec=BBEVars)

    def test_mobile_get_sx_association_stats(self):
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.action.return_value = {'Sx Association': {'Key': 'Value', 'Key1': 'Value1'}}
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}
        # all keys case
        self.assertDictEqual(mobile_get_sx_association_stats(subscriber, 'all'), {'Key': 'Value', 'Key1': 'Value1'})
        # one key case
        self.assertDictEqual(mobile_get_sx_association_stats(subscriber, ['Key']), {'Key': 'Value'})
        # wrong key case
        with self.assertRaises(Exception) as context:
            mobile_get_sx_association_stats(subscriber, ['test'])
        self.assertIn('ERROR: The search', context.exception.args[0])
        # bad stats case
        subscriber.action.return_value = {'Unexpected Key': {'Key': 'Value', 'Key1': 'Value1'}}
        with self.assertRaises(Exception) as context:
            mobile_get_sx_association_stats(subscriber, 'all')
        self.assertIn('Error: Did not properly receive Sx Association stats. Received stats:',
                      context.exception.args[0])

        # reset to normal parameters
        subscriber.action.return_value = {'Sx Association': {'Key': 'Value', 'Key1': 'Value1'}}
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}
        # extra subscriber key case
        self.assertDictEqual(mobile_get_sx_association_stats([subscriber, MagicMock(spec=CUPSSubscribers)], ['Key']),
            {'Key': 'Value'})
        # args is not a list
        subscriber.action.return_value = {'Sx Association': {'Key': 'Value', 'Key1': 'Value1'}}
        self.assertDictEqual(mobile_get_sx_association_stats(subscriber, 'Key1'), {'Key1': 'Value1'})
        # args is not a list bad key
        with self.assertRaises(Exception) as context:
            mobile_get_sx_association_stats(subscriber, 'test')
        self.assertIn('ERROR: The search', context.exception.args[0])

    def test_mobile_get_sx_session_stats(self):
        # Initialize Test
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.action.return_value = {
            'Sx Session': {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3'},
            'Sx Association': {'Key': 'Value', 'Key1': 'Value1'},
        }
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}
        search_all_keys = 'all'
        search_keys = ['Key1', 'Key3']

        # All Keys in Sx Session
        self.assertDictEqual(mobile_get_sx_session_stats(subscriber, search_all_keys),
                             {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3'})

        # Partial Keys in Sx Session (more than one and less than all)
        self.assertDictEqual(mobile_get_sx_session_stats(subscriber, search_keys), {'Key1': 'Value1', 'Key3': 'Value3'})

        # One Key in Sx Session
        self.assertDictEqual(mobile_get_sx_session_stats(subscriber, 'Key1'), {'Key1': 'Value1'})


        # Invalid Key search in Sx Session
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}
        with self.assertRaises(Exception) as context:
            mobile_get_sx_session_stats(subscriber, 'not_valid_request')
        self.assertIn('Error: The search \'not_valid_request\' does not exist in Sx Session Stats.',
                      context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_get_sx_session_stats(subscriber, ['not_valid_request'])
        self.assertIn('Error: The search \'not_valid_request\' does not exist in Sx Session Stats.',
                      context.exception.args[0])

        # More than one subscriber
        self.assertDictEqual(mobile_get_sx_session_stats([subscriber, MagicMock()], search_all_keys),
                             {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3'})

        # No Sx Session keys in landslide answer and subscriber not list
        subscriber.action.return_value = {'Missing_Sx_Session': {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3'},
                                          'Sx Association': {'Key': 'Value', 'Key1': 'Value1'}}
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}
        with self.assertRaises(Exception) as context:
            mobile_get_sx_session_stats(subscriber, search_all_keys)
        self.assertIn('Error: Did not properly receive Sx Session stats. Received stats:', context.exception.args[0])

    def test_mobile_get_traffic_stats(self):
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.action.return_value = {
            'L3 Client': {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3'},
            'L3 Server': {'Key1': 'Value1', 'Key2': 'Value2'},
            'Not_supported': {'Key1': 'Value1', 'Key2': 'Value2'},
            'L4 Server': {'Key1': 'Value1', 'Key2': 'Value2'},
            'L5-7 Client|Basic': {'Key1': 'Value1', 'Key2': 'Value2'},
            'L5-7 Server|Basic': {'Key1': 'Value1', 'Key2': 'Value2'},
        }
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}
        search_type = 'L5-7 Server|Basic'
        search_all_keys = 'all'
        self.assertIsNotNone(mobile_get_traffic_stats(subscriber, search_type, search_all_keys))
        # unsupported SGi type
        search_type = 'not_supported'
        with self.assertRaises(Exception) as context:
            mobile_get_traffic_stats(subscriber, search_type, search_all_keys)
        self.assertIn('Error: traffic search type is not defined. Supported types are:\n', context.exception.args[0])
        # Missing SGi type in results
        search_type = 'L4 Client'
        with self.assertRaises(Exception) as context:
            mobile_get_traffic_stats(subscriber, search_type, search_all_keys)
        self.assertIn('Error: Did not receive expected traffic stats for L4 Client. Received stats:\n',
                       context.exception.args[0])
        # Unexpected SGi traffic stats for search list
        search_keys = ['Unsupported_key', 'Key1']
        search_type = 'L3 Server'
        with self.assertRaises(Exception) as context:
            mobile_get_traffic_stats(subscriber, search_type, search_keys)
        self.assertIn('Error: The search \'Unsupported_key\' does not exist in traffic ' +
                      search_type + ' stats.\nRetrievable stats:\n', context.exception.args[0])
        # Unexpected SGi traffic stats for search string
        with self.assertRaises(Exception) as context:
            mobile_get_traffic_stats(subscriber, search_type, 'Unsupported_key')
        self.assertIn('Error: The search \'Unsupported_key\' does not exist in traffic ' +
                      search_type + ' stats.\nRetrievable stats:\n', context.exception.args[0])
        # Valid search list
        search_keys = ['Key1', 'Key2']
        self.assertIsNotNone(mobile_get_traffic_stats(subscriber, search_type, search_keys))
        # Valid search string and test all SGi types
        self.assertIsNotNone(mobile_get_traffic_stats(subscriber, 'L3 Client', 'Key1'))

    @patch('time.sleep')
    def test_mobile_get_stats_results(self, patch_sleep):
        data = {
            'Sx Session': {'Key1': 'Value1', 'Key2': 'Value2', 'Key3': 'Value3'},
            'Sx Association': {'Key': 'Value', 'Key1': 'Value1'},
        }
        data_not_available = {'status_message': 'The results are not yet available. Try after 10-15s'}
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.tsname = 'wf-virtual-ls02'
        subscriber.node_test_case_name = 'my_node_tc'
        subscriber.nodal_test_case_name = 'my_nodal_tc'
        subscriber.action.side_effect = [data_not_available, data]
        self.assertIsNotNone(mobile_get_stats_results([subscriber, MagicMock(spec=CUPSSubscribers)], filter='node'))
        subscriber.action.side_effect = None
        subscriber.action.return_value = data
        self.assertIsNotNone(mobile_get_stats_results(subscriber, filter='node'))
        self.assertIsNotNone(mobile_get_stats_results(subscriber, filter='nodal'))

    @patch('builtins.print')
    def test_mobile_configure_sgi_traffic(self, patch_print):
        kwargs = {
            'traffic_type': 'ipv4',
            'host_type': 'local',
            'vlan': '100',
            'svlan': '200',
            'tcp_socket_disc_side': 'client',
            'tcp_3way_handshake': 'true',
            'tcp_disconnect_type': 'FIN',
            'tcp_congestion_avoid': 'true',
            'tcp_window_size': '32768',
            'tcp_max_segment_size': '100',
            'tcp_min_header_size': '50',
            'tcp_max_packets_before_ack': '10',
            'client_port': '50',
            'server_port': '1000',
            'name': 'udp1',
            'payload_type': 'udp',
            'udp_burst_count': '10',
        }
        subscriber = MagicMock()
        subscriber.rt_device_id = 'rt0'
        subscriber.traffic_start_ip = '20.1.1.2'
        subscriber.libname = 'mylib'
        subscriber.subscribers_type = 'cups'
        builtins.t['resources']['rt0']['system']['primary']['uv-ts-name'] = 'ls'
        builtins.t._script_name = 'my_rli_script'
        self.assertIsNone(mobile_configure_sgi_traffic([subscriber, MagicMock(spec=CUPSSubscribers)], **kwargs))
        subscriber.subscribers_type = 'pgw'
        self.assertIsNone(mobile_configure_sgi_traffic(subscriber, **kwargs))

        kwargs['host_type'] = 'remote'
        kwargs['packet_size'] = '96'
        kwargs['segment_size'] = '128'
        subscriber.dmf_handle = None
        subscriber.uplink_addr = '20.1.1.1'
        self.assertIsNone(mobile_configure_sgi_traffic(subscriber, **kwargs))
        kwargs['payload_type'] = 'tcp'
        kwargs['traffic_type'] = 'ipv6'
        kwargs['host_type'] = 'local'
        self.assertIsNone(mobile_configure_sgi_traffic(subscriber, **kwargs))
        kwargs['traffic_type'] = 'dualstack'
        kwargs['tos_list'] = ['32', '64']
        self.assertIsNone(mobile_configure_sgi_traffic(subscriber, **kwargs))

    def test_mobile_remove_traffic(self):
        kwargs = {'name': 'udp1'}
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.subscribers_type = 'cups'
        subscriber.test_session_handle = 'handle'
        subscriber.nodal_testcase_handle = 'nodal'
        subscriber.rt_device_id = 'rt0'
        subscriber.libname = 'mylib'
        builtins.t['resources']['rt0']['system']['primary']['uv-ts-name'] = 'ls'
        builtins.t._script_name = 'my_rli_script'
        subscriber.dmf_handle = {'udp1': 'invoke_return'}
        subscriber.dmf_name_list = ['udp1']
        subscriber.dmf_role = ['client']
        subscriber.dmf_transport_list = ['any']
        subscriber.dmf_lib_list = [subscriber.libname]
        self.assertIsNone(mobile_remove_traffic([subscriber, MagicMock(spec=CUPSSubscribers)], **kwargs))
        subscriber.subscribers_type = 'pgw'
        subscriber.dmf_handle = {'udp1': 'invoke_return'}
        subscriber.dmf_name_list = ['udp1']
        subscriber.dmf_role = ['client']
        subscriber.dmf_transport_list = ['any']
        subscriber.dmf_lib_list = [subscriber.libname]
        self.assertIsNone(mobile_remove_traffic(subscriber, **kwargs))
        subscriber.dmf_handle = {'udp1': 'invoke_return'}
        subscriber.dmf_name_list = ['udp1', 'udp2']
        subscriber.dmf_role = ['client', 'client']
        subscriber.dmf_transport_list = ['any', 'any']
        subscriber.dmf_lib_list = [subscriber.libname, subscriber.libname]
        self.assertIsNone(mobile_remove_traffic(subscriber, **kwargs))

        # Exception path for name_list having no entries
        kwargs['name'] = 'tcp1'
        with self.assertRaises(Exception) as context:
            mobile_remove_traffic(subscriber, **kwargs)
        self.assertIn('traffic name', context.exception.args[0])

        kwargs.pop('name')
        self.assertIsNone(mobile_remove_traffic(subscriber, **kwargs))
        delattr(subscriber, 'dmf_name_list')
        self.assertIsNone(mobile_remove_traffic(subscriber, **kwargs))

    @patch('time.sleep')
    @patch('jnpr.toby.bbe.mobilekeywords.Thread')
    def test_mobile_login_sx_session(self, patch_thread, patch_sleep):
        subscriber = MagicMock()
        subscriber.subscriber_group_indices = {'default': (1, 2)}
        subscriber.test_activity = 'Other-Mode'
        subscriber.test_session_handle = 'Test_Handle'
        with self.assertRaises(Exception) as context:
            mobile_login_sx_session(subscriber)
        self.assertIn('ERROR: Keyword login sx session only supported for CUPSSubscribers in Command Mode',
                      context.exception.args[0])

        subscriber.isactive = False
        subscriber.test_activity = 'Command Mode'

        # Port capture on start code path
        port_capture_invoke_retval = '{PortCaptureConfig(0)} {PortCaptureConfig(1)} '
        builtins.t.get_handle.return_value.invoke.side_effect = ['', port_capture_invoke_retval, '', '', '',
                                                        '3_Waiting', '6_Waiting', 'true', 'true']
        self.assertIsNone(mobile_login_sx_session(subscriber, retries=2, auto_capture_on_start='true'))

        builtins.t.get_handle.return_value.invoke.side_effect = None
        builtins.t.get_handle.return_value.invoke.return_value = 'Waiting'
        subscriber.subscriber_group_indices = dict()
        subscriber.subscriber_group_indices['default'] = (1,1)
        subscriber.isactive = True
        subscriber.session_count = 1
        subscriber.apn_name = 'apn'
        subscriber.tsname = 'test_system_name'
        subscriber.nodal_test_case_name = 'nodal_test'
        kwargs = {
            'stats_router': True,
            'stats_tester': True,
        }
        self.assertIsNone(mobile_login_sx_session([subscriber, MagicMock(spec=CUPSSubscribers)], **kwargs))

        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.isactive = False
        subscriber.test_activity = 'Command Mode'
        subscriber.test_session_handle = 'Test_Handle'
        builtins.t.get_handle.return_value.invoke.return_value = '3_Waiting'
        subscriber.action.side_effect = ['', Exception('Session is no longer running'),
                                         Exception('Session is running'),
                                         Exception('Session is running'),
                                         Exception('Session is running')]
        with self.assertRaises(Exception) as context:
            mobile_login_sx_session(subscriber)

    @patch('time.sleep')
    @patch('jnpr.toby.bbe.mobilekeywords.Thread')
    def test_mobile_logout_sx_session(self, patch_thread, patch_sleep):
        subscriber = MagicMock()
        subscriber.subscriber_group_indices = {'default': (1, 2)}
        with self.assertRaises(Exception) as context:
            mobile_logout_sx_session([subscriber, MagicMock(spec=CUPSSubscribers)])
        self.assertIn('Keyword Logout Sx Session only supported for CUPSSubscribers in Command Mode!',
                      context.exception.args[0])
        subscriber.test_activity = ['Command Mode']
        subscriber.isactive = False
        with self.assertRaises(Exception) as context:
            mobile_logout_sx_session(subscriber)
        self.assertIn('Sx Session must be active in order to logout Sx Session.', context.exception.args[0])
        subscriber.isactive = True
        builtins.t.get_handle.return_value.invoke.return_value = 'Waiting'
        with self.assertRaises(Exception) as context:
            mobile_logout_sx_session(subscriber, group='not_defined')
        self.assertIn(
            'Error: Subscriber group not_defined is not defined. The following subscriber groups are defined: ',
            context.exception.args[0])
        kwargs = {
            'stats_router': True,
            'stats_tester': True,
        }
        self.assertIsNone(mobile_logout_sx_session(subscriber, **kwargs))
        builtins.t.get_handle.return_value.invoke.return_value = 'running'
        self.assertIsNone(mobile_logout_sx_session(subscriber))

    @patch('time.sleep')
    @patch('time.time')
    @patch('plotly.offline.plot')
    @patch('numpy.load')
    @patch('numpy.savez')
    @patch('os.remove')
    def test_mobile_calculate_router_stats(self, patch_remove, patch_savez, patch_load,
                                           patch_plotly, patch_time, patch_sleep):
        # Make time go up by 60 sec every time it is called
        patch_time.side_effect = itertools.count(0, 60)
        patch_load.return_value = {
            'timestamps': [],
            'rates': [],
            'sessions': [],
        }
        kwargs = {
            'stats_mode': 'login',
            'stats_bearer': 'default',
            'stats_scale': 100,
            'stats_scale_dedicated': 100,
            'stats_router_full_graph': True,
        }
        router = builtins.t.get_handle.return_value
        sessions = ['','',50,90,90,100,100,100]
        sessions_summary = [MagicMock(resp='Sessions by State:\n   ESTABLISHED: {}'.format(s)) for s in sessions]
        router.cli.side_effect = sessions_summary
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))
        kwargs['stats_mode'] = 'logout'
        sessions = [100,50,'','','','','','']
        sessions_summary = [MagicMock(resp='Sessions by State:\n   ESTABLISHED: {}'.format(s)) for s in sessions]
        router.cli.side_effect = sessions_summary
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))
        sessions = [100,50,50,50,50,50,50,50]
        sessions_summary = [MagicMock(resp='Sessions by State:\n   ESTABLISHED: {}'.format(s)) for s in sessions]
        router.cli.side_effect = sessions_summary
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))
        router.cli.side_effect = None
        router.cli.return_value.resp = 'Sessions by State:\n   ESTABLISHED: 100'
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))
        kwargs['stats_bearer'] = 'dedicated'
        router.cli.return_value.resp = 'Bearers by State:\n   ESTABLISHED: 100'
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))
        router.cli.return_value.resp = ''
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))
        router.shell.side_effect = [MagicMock(resp='5 5 ERROR: invalid pfe instance!')] * 10
        builtins.bbe.get_devices.return_value = ['r0']
        builtins.t.resources = {
            'r0': {
                'interfaces': {
                    'access': {
                        'pic': 'lt-1/0/0'
                    }
                }
            }
        }
        kwargs['stats_router_pfe'] = True
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))
        kwargs['stats_router_pfe_slots'] = 7
        self.assertIsNone(mobile_calculate_router_stats(**kwargs))

        kwargs['stats_mode'] = 'not login nor logout'
        with self.assertRaises(Exception) as context:
            mobile_calculate_router_stats(**kwargs)
        self.assertIn('mobile_calculate_router_stats mode must be "login" or "logout"', context.exception.args[0])
        kwargs['stats_mode'] = 'login'
        kwargs['stats_bearer'] = 'not default, dedicated, or both'
        with self.assertRaises(Exception) as context:
            mobile_calculate_router_stats(**kwargs)
        self.assertIn('mobile_calculate_router_stats bearer must be "default", "dedicated", or "both"',
                      context.exception.args[0])

    @patch('time.sleep')
    @patch('time.time')
    @patch('time.ctime')
    @patch('plotly.offline.plot')
    @patch('numpy.load')
    @patch('numpy.savez')
    @patch('os.remove')
    @patch('jnpr.toby.bbe.mobilekeywords.mobile_get_stats_results')
    def test_mobile_calculate_tester_stats(self, patch_get_stats_results, patch_remove, patch_savez, patch_load,
                                           patch_plotly, patch_ctime, patch_time, patch_sleep):
        # Make ctime go up by 30 sec every time it is called
        patch_ctime.side_effect = itertools.count(0, 30)
        # Make time go up by 30 sec every time it is called
        patch_time.side_effect = itertools.count(0, 30)

        mock_actual_rates = [0,0,500,750,1000,750,1000,1000,1000,500,0,0,0,0,0]
        scale = sum(mock_actual_rates) * 15
        mock_get_stats = {
            'Connect': [],
            'Disconnect': [],
        }
        patch_get_stats_results.side_effect = []

        mock_prev_session_login = 0
        mock_prev_session_logout = scale
        mock_stats_login = []
        mock_stats_logout = []
        mock_stats_broken_sessions = []
        mock_stats_broken_rates = []
        for mock_actual_rate in mock_actual_rates:
            mock_session = mock_actual_rate * 15 + mock_prev_session_login
            mock_prev_session_login = mock_session
            mock_stats_login.append({
                'Test Summary': {
                    'Actual Connect Rate (Sessions/Second)': mock_actual_rate,
                    'Actual Dedicated Bearer Session Connect Rate (Sessions/Second)': mock_actual_rate,
                    'Dedicated Bearer Sessions Established': mock_session,
                    'Sessions Established': mock_session,
                },
            })
            mock_stats_broken_sessions.append({
                'Test Summary': {
                    'Actual Connect Rate (Sessions/Second)': mock_actual_rate,
                    'Actual Dedicated Bearer Session Connect Rate (Sessions/Second)': mock_actual_rate,
                    'Dedicated Bearer Sessions Established': 0,
                    'Sessions Established': 0,
                },
            })
            mock_session = mock_actual_rate * -15 + mock_prev_session_logout
            mock_prev_session_logout = mock_session
            mock_stats_logout.append({
                'Test Summary': {
                    'Actual Disconnect Rate (Sessions/Second)': mock_actual_rate,
                    'Actual Dedicated Bearer Session Disconnect Rate (Sessions/Second)': mock_actual_rate,
                    'Dedicated Bearer Sessions Established': mock_session,
                    'Sessions Established': mock_session,
                },
            })

        patch_load.return_value = {
            'timestamps': [],
            'default_rates': [],
            'dedicated_rates': [],
            'sessions_established_default': [],
            'sessions_established_dedicated': [],
        }
        kwargs = {
            'stats_mode': 'login',
            'stats_bearer': 'both',
            'stats_scale': scale,
            'stats_scale_dedicated': scale,
            'stats_tester_full_graph': True,
        }
        cups_test_handle = MagicMock()
        patch_get_stats_results.side_effect = mock_stats_login
        self.assertIsNone(mobile_calculate_tester_stats(cups_test_handle, **kwargs),)
        kwargs['stats_mode'] = 'logout'
        patch_get_stats_results.side_effect = mock_stats_logout
        self.assertIsNone(mobile_calculate_tester_stats(cups_test_handle, **kwargs),)
        kwargs['stats_tester_full_graph'] = False
        kwargs['stats_mode'] = 'login'
        kwargs['stats_scale'] = sum(mock_actual_rates) + 1
        kwargs['stats_scale_dedicated'] = sum(mock_actual_rates) + 1
        patch_get_stats_results.side_effect = mock_stats_login
        self.assertIsNone(mobile_calculate_tester_stats(cups_test_handle, **kwargs),)
        patch_get_stats_results.side_effect = mock_stats_broken_sessions
        self.assertIsNone(mobile_calculate_tester_stats(cups_test_handle, **kwargs),)
        kwargs['stats_repeated_zeros'] = 2
        patch_get_stats_results.side_effect = mock_stats_login
        self.assertIsNone(mobile_calculate_tester_stats(cups_test_handle, **kwargs),)
        patch_get_stats_results.side_effect = mock_stats_broken_sessions
        self.assertIsNone(mobile_calculate_tester_stats(cups_test_handle, **kwargs),)
        kwargs['stats_timeout'] = 15
        patch_get_stats_results.side_effect = mock_stats_login
        self.assertIsNone(mobile_calculate_tester_stats(cups_test_handle, **kwargs),)
        kwargs['stats_mode'] = 'not login nor logout'
        with self.assertRaises(Exception) as context:
            mobile_calculate_tester_stats(cups_test_handle, **kwargs)
        self.assertIn('mobile_calculate_tester_stats mode must be "login" or "logout"', context.exception.args[0])
        kwargs['stats_mode'] = 'login'
        kwargs['stats_bearer'] = 'not default, dedicated, or both'
        with self.assertRaises(Exception) as context:
            mobile_calculate_tester_stats(cups_test_handle, **kwargs)
        self.assertIn('mobile_calculate_tester_stats bearer must be "default", "dedicated", or "both"',
            context.exception.args[0])

    def test_mobile_pause_sgi_traffic(self):
        kwargs = {}
        subscriber = MagicMock()
        builtins.t['resources']['rt0']['system']['primary']['uv-ts-name'] = 'ls'
        self.assertIsNone(mobile_pause_sgi_traffic([subscriber, MagicMock(spec=CUPSSubscribers)], **kwargs))

        dmfList=['testDmf', 'scratch_udp_traffic']
        kwargs['dmfList'] = dmfList
        self.assertIsNone(mobile_pause_sgi_traffic(subscriber, **kwargs))

    def test_mobile_resume_sgi_traffic(self):
        kwargs = {}
        subscriber = MagicMock()
        builtins.t['resources']['rt0']['system']['primary']['uv-ts-name'] = 'ls'
        self.assertIsNone(mobile_resume_sgi_traffic([subscriber, MagicMock(spec=CUPSSubscribers)], **kwargs),)

        dmfList=['testDmf', 'scratch_udp_traffic']
        kwargs['dmfList'] = dmfList
        self.assertIsNone(mobile_resume_sgi_traffic(subscriber, **kwargs))

    def test_mobile_configure_bearers(self):
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.test_activity = 'Command Mode'
        subscriber.rt_device_id = 'rt0'
        subscriber.nodal_testcase_handle = 'nodal'
        subscriber.node_testcase_handle = 'node'
        subscriber.test_session_handle = 'handle'

        kwargs = {
            'downlink_ambr': '1000',
            'uplink_ambr': '1000',
            'dedicated_bearer_delay': [5, 10],
        }

        sdf1 = {
            'direction': 'uplink',
            'precedence': '255',
            'protocol-number': '17',
            'remote-address': '23.0.0.1/24',
            'start-port-local': '2002',
            'end-port-local': '2003',
            'start-port-remote': '1002',
            'end-port-remote': '1003',
            'tos': '16',
            'security-parameter-index': '100',
            'flow-label': 'flow123',
        }
        sdf2 = {
            'direction': 'downlink',
            'precedence': '254',
            'protocol-number': '17',
            'remote-address': '23.0.0.1/24',
            'start-port-local': '2002',
            'end-port-local': '2003',
            'start-port-remote': '1002',
            'end-port-remote': '1003',
            'tos': '16',
            'security-parameter-index': '100',
            'flow-label': 'flow123',
        }
        sdf3 = {
            'direction': 'bidirectional',
            'precedence': '254',
            'protocol-number': '17',
            'remote-address': '23.0.0.1/24',
            'start-port-local': '3002',
            'end-port-local': '3003',
            'start-port-remote': '4002',
            'end-port-remote': '4003',
            'tos': '32',
            'security-parameter-index': '200',
            'flow-label': 'flow123',
        }
        sdf4 = {
            'direction': 'pre-rel7',
            'precedence': '254',
            'protocol-number': '17',
            'remote-address': '23.0.0.1/24',
            'start-port-local': '3002',
            'end-port-local': '3003',
            'start-port-remote': '4002',
            'end-port-remote': '4003',
            'tos': '32',
            'security-parameter-index': '200',
            'flow-label': 'flow123',
        }
        sdfs = {'B0': [sdf1, sdf2], 'B1': [sdf3, sdf4]}

        # No Exceptions code path
        subscriber.subscribers_type = 'cups'
        self.assertTrue(mobile_configure_bearers([subscriber, MagicMock(spec=CUPSSubscribers)], sdf_dict=sdfs,
                                                 default_bearers=1, dedicated_bearers=2, **kwargs))
        subscriber.subscribers_type = 'pgw'
        self.assertTrue(mobile_configure_bearers(subscriber, sdf_dict=sdfs, default_bearers=1,
                                                 dedicated_bearers=2, **kwargs))
        self.assertTrue(mobile_configure_bearers(subscriber, sdf_dict=sdfs, default_bearers=1,
                                                 dedicated_bearers=1, default_bearer_sdf='true',
                                                 bearer_qci_list=[9,3], **kwargs))
        sdfs.pop('B1')
        self.assertTrue(mobile_configure_bearers(subscriber, sdf_dict=sdfs, default_bearers=1,
                                                 dedicated_bearers=0, default_bearer_sdf='true',
                                                 bearer_qci_list=[9], **kwargs))
        self.assertTrue(mobile_configure_bearers(subscriber, sdf_dict=sdfs, default_bearers=1,
                                                 dedicated_bearers=0, default_bearer_sdf='false',
                                                 bearer_qci_list=[9], **kwargs))

        # SDF settings code path for SDF QoS
        sdf1['sdf-index'] = '1'
        sdf1['uplink-gate-status'] = '0'
        sdf1['downlink-gate-status'] = '0'
        sdf1['uplink-gbr'] = '5'
        sdf1['downlink-gbr'] = '5'
        sdf1['uplink-mbr'] = '10'
        sdf1['downlink-mbr'] = '10'
        self.assertTrue(mobile_configure_bearers(subscriber, sdf_dict=sdfs, default_bearers=1,
                                                 dedicated_bearers=0, default_bearer_sdf='true', bearer_qci_list=[9],
                                                 **kwargs), True)

        # SDF settings code path exception for excluding bearer_qci_list
        with self.assertRaises(Exception) as context:
            mobile_configure_bearers(subscriber, sdf_dict=sdfs, default_bearers=1, dedicated_bearers=0,
                                     default_bearer_sdf='true', **kwargs)
        self.assertIn('bearer_qci_list is a required argument when SDF QoS parameters', context.exception.args[0])

        builtins.t.get_handle.return_value.os = 'IXIA'
        with self.assertRaises(Exception) as context:
            mobile_configure_bearers(subscriber, sdf_dict=sdfs, default_bearers=1, dedicated_bearers=2, **kwargs)
        self.assertIn('only supported for Spirent Landslide', context.exception.args[0])

    def test_mobile_configure_modification_tft_sets(self):
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.test_activity = 'Command Mode'
        subscriber.dedicated_bearers = '1'
        subscriber.bearer_per_session = '1'
        subscriber.rt_device_id = 'rt0'
        subscriber.nodal_testcase_handle = 'nodal'
        subscriber.node_testcase_handle = 'node'
        subscriber.test_session_handle = 'handle'
        subscriber.subscribers_type = 'cups'

        sdf1 = {'direction': 'uplink', 'precedence': '255', 'protocol-number': '17', 'remote-address': '23.0.0.1/24',
                'start-port-local': '2002', 'end-port-local': '2003', 'start-port-remote': '1002',
                'end-port-remote': '1003', 'tos': '16', 'security-parameter-index': '100', 'flow-label': 'flow123'}
        sdf2 = {'direction': 'downlink', 'precedence': '254', 'protocol-number': '17', 'remote-address': '23.0.0.1/24',
                'start-port-local': '2002', 'end-port-local': '2003', 'start-port-remote': '1002',
                'end-port-remote': '1003', 'tos': '16', 'security-parameter-index': '100', 'flow-label': 'flow123'}
        sdf3 = {'direction': 'bidirectional', 'precedence': '254', 'protocol-number': '17',
                'remote-address': '23.0.0.1/24',
                'start-port-local': '3002', 'end-port-local': '3003', 'start-port-remote': '4002',
                'end-port-remote': '4003', 'tos': '32', 'security-parameter-index': '200', 'flow-label': 'flow123'}
        sdf4 = {'direction': 'pre-rel7', 'precedence': '254', 'protocol-number': '17',
                'remote-address': '23.0.0.1/24',
                'start-port-local': '3002', 'end-port-local': '3003', 'start-port-remote': '4002',
                'end-port-remote': '4003', 'tos': '32', 'security-parameter-index': '200', 'flow-label': 'flow123'}
        sdf5 = {'direction': 'downlink', 'precedence': '252', 'protocol-number': '6', 'remote-address': '27.0.0.1/24',
                'start-port-local': '2002', 'end-port-local': '2003', 'start-port-remote': '6002',
                'end-port-remote': '6003', 'tos': '16', 'security-parameter-index': '100', 'flow-label': 'flow123'}

        sdf6 = {'direction': 'bidirectional', 'precedence': '251', 'protocol-number': '6',
                'remote-address': '28.0.0.1/24',
                'start-port-local': '3002', 'end-port-local': '3003', 'start-port-remote': '7002',
                'end-port-remote': '7003', 'tos': '32', 'security-parameter-index': '200', 'flow-label': 'flow123'}

        sdf_dict1 = {'B0': [sdf1, sdf2], 'B1': [sdf3]}
        sdf_dict2 = {'B0': [sdf6], 'B1': [sdf4, sdf5]}
        sdf_dict3 = {'B0': [sdf2, sdf4], 'B1': [sdf5, sdf1]}
        mod_sets = {'S1': sdf_dict1, 'S2': sdf_dict2, 'S3': sdf_dict3}
        subscriber.tft_settings = sdf_dict1

        # No Exceptions code path
        self.assertTrue(mobile_configure_modification_tft_sets([subscriber, MagicMock(spec=CUPSSubscribers)], mod_sets))
        subscriber.subscribers_type = 'pgw'
        self.assertTrue(mobile_configure_modification_tft_sets(subscriber, mod_sets))

        # Exception for no Command mode
        subscriber.test_activity = 'Capacity Test'
        with self.assertRaises(Exception) as context:
            mobile_configure_modification_tft_sets(subscriber, mod_sets)
        self.assertIn('only supported for CUPSSubscribers in Command Mode', context.exception.args[0])

        # Exception for unsupported OS of router tester
        builtins.t.get_handle.return_value.os = 'IXIA'
        with self.assertRaises(Exception) as context:
            mobile_configure_modification_tft_sets(subscriber, mod_sets)
        self.assertIn('only supported for Spirent Landslide', context.exception.args[0])

    def test_mobile_configure_dhcp_ue(self):
        subscriber = MagicMock()
        subscriber.subscribers_type = 'cups'
        blank = MagicMock()
        kwargs = {
            'mac_address': blank,
            'client_id': blank,
            'lease_time_request': blank,
            'enterprise_number': blank,
            'rapid_commit': blank,
            'enable_broadcast': blank,
            'parameter_request_list': blank,
            'host_name': blank,
            'vendor_class_id': blank,
            'retries': blank,
            'v4_offer_message': blank,
            'v4_ack_message': blank,
            'ia_option': blank,
            'interface_tag': blank,
            'vlan_id': blank,
            'next_hop_ip_address': blank,
            'server_port': blank,
            'circuit_id': blank,
            'lease_query_type': blank,
        }
        self.assertTrue(mobile_configure_dhcp_ue([subscriber, MagicMock(spec=CUPSSubscribers)], **kwargs))
        kwargs['interface_tag'] = 'control';
        self.assertTrue(mobile_configure_dhcp_ue(subscriber, **kwargs))
        kwargs['interface_tag'] = 'access';
        self.assertTrue(mobile_configure_dhcp_ue(subscriber, **kwargs))
        kwargs['interface_tag'] = 'uplink';
        self.assertTrue(mobile_configure_dhcp_ue(subscriber, **kwargs))
        builtins.t.get_handle.return_value.os = 'IXIA'
        with self.assertRaises(Exception) as context:
            mobile_configure_dhcp_ue(subscriber, **kwargs)
        self.assertIn('ERROR: Keyword presently only supported for Spirent Landslide!', context.exception.args[0])
        subscriber.subscribers_type = "pgw"
        with self.assertRaises(Exception) as context:
            mobile_configure_dhcp_ue(subscriber, **kwargs)
        self.assertIn("mobile_configure_dhcp_ue does not support PGWSubscribers handles", context.exception.args[0])

    def test_mobile_control_bearers(self):
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.test_activity = 'Command Mode'
        subscriber.dedicated_bearers = '1'
        subscriber.bearer_per_session = '1'
        subscriber.rt_device_id = 'rt0'
        subscriber.nodal_test_case_name = 'dbond_nodal_scratch1'
        subscriber.node_test_case_name = 'dbond_node_scratch1'
        subscriber.test_session_handle = 'handle'
        subscriber.tsname = 'wf-virtual-ls02'
        subscriber.subscriber_group_indices = {'default': (1, 2)}
        subscriber.isactive = True
        builtins.t.get_handle.return_value.invoke.return_value = 'WAITING'

        # Standard code path
        self.assertTrue(mobile_control_bearers([subscriber, MagicMock(spec=CUPSSubscribers)], action='modify_bearer',
                                               tft_operation='create_new_tft'))
        self.assertTrue(mobile_control_bearers(subscriber, action='modify_bearer',
                                               tft_operation='delete_existing_tft'))
        self.assertTrue(mobile_control_bearers(subscriber, action='modify_bearer', modification_initiator='MME',
                                               tft_set='1'))
        self.assertTrue(mobile_control_bearers(subscriber, action='modify_bearer',
                                               tft_operation='add_filter_to_existing_tft'))
        self.assertTrue(mobile_control_bearers(subscriber, action='modify_bearer',
                                               tft_operation='replace_filter_in_existing_tft'))
        self.assertTrue(mobile_control_bearers(subscriber, action='modify_bearer',
                                               tft_operation='delete_filter_in_existing_tft'))
        self.assertTrue(mobile_control_bearers(subscriber, action='stop_dedicated_bearer'))
        self.assertTrue(mobile_control_bearers(subscriber, action='start_dedicated_bearer'))

        # Subscriber inactive exception path
        subscriber.isactive = False
        with self.assertRaises(Exception) as context:
            mobile_control_bearers(subscriber, action='start_dedicated_bearer')
        self.assertIn('Sx Session must be active', context.exception.args[0])

        # Test Session not in 'waiting' state exception path
        subscriber.isactive = True
        builtins.t.get_handle.return_value.invoke.return_value = 'started'
        with self.assertRaises(Exception) as context:
            mobile_control_bearers(subscriber, action='start_dedicated_bearer')
        self.assertIn('Sx Session not properly running', context.exception.args[0])

        # Invalid tft_operation exception path
        with self.assertRaises(Exception) as context:
            mobile_control_bearers(subscriber, tft_operation='invalid_action')
        self.assertIn('ERROR: Invalid tft_operation', context.exception.args[0])

        # Invalid group exception path
        with self.assertRaises(Exception) as context:
            mobile_control_bearers(subscriber, group='INVALID')
        self.assertIn('ERROR: Subscriber group', context.exception.args[0])

        # Invalid action exception path
        with self.assertRaises(Exception) as context:
            mobile_control_bearers(subscriber, action='INVALID')
        self.assertIn('ERROR: Keyword supports actions:', context.exception.args[0])

        # Command Mode exception path
        subscriber.test_activity = 'Capacity Test'
        with self.assertRaises(Exception) as context:
            mobile_control_bearers(subscriber, action='start_dedicated_bearer')
        self.assertIn('Keyword only supported for CUPSSubscribers in Command Mode!', context.exception.args[0])

        # Invalid tester OS exception path
        builtins.t.get_handle.return_value.os = 'IXIA'
        with self.assertRaises(Exception) as context:
            mobile_control_bearers(subscriber, action='start_dedicated_bearer')
        self.assertIn('Keyword presently only supported for Spirent Landslide!', context.exception.args[0])

    def test_mobile_verify_traffic(self):
        data = {
            'L3 Client': {
                'Total Packets Sent/Sec': '1,000',
                'Total Packets Received/Sec': '1,000',
                'Total Packets Received': '200',
                'Total Bits Received/Sec': '8,000,000',
                'Total Packets Sent': '300',
            },
            'L3 Server': {
                'Total Packets Sent/Sec': '2,000',
                'Total Packets Received/Sec': '950',
                'Total Packets Received': '199',
                'Total Bits Received/Sec': '16,000,000',
                'Total Packets Sent': '300',
            },
            'traffic1': {
                'L3 Client': {
                    'Total Packets Sent/Sec': '1,000',
                    'Total Packets Received/Sec': '1,000',
                    'Total Packets Received': '200',
                    'Total Bits Received/Sec': '8,000,000',
                    'Total Packets Sent': '300',
                },
                'L3 Server': {
                    'Total Packets Sent/Sec': '2,000',
                    'Total Packets Received/Sec': '950',
                    'Total Packets Received': '199',
                    'Total Bits Received/Sec': '16,000,000',
                    'Total Packets Sent': '300',
                },
            },
        }
        data_pi = {
            'perIntervalStats': {
                'L3 Client': {
                    'Total Packets Sent/Sec  (P-I)': '1,000',
                    'Total Packets Received/Sec  (P-I)': '1,000',
                    'Total Packets Received  (P-I)': '200',
                    'Total Bits Received/Sec  (P-I)': '8,000,000',
                    'Total Packets Sent  (P-I)': '300',
                },
                'L3 Server': {
                    'Total Packets Sent/Sec  (P-I)': '2,000',
                    'Total Packets Received/Sec  (P-I)': '950',
                    'Total Packets Received  (P-I)': '199',
                    'Total Bits Received/Sec  (P-I)': '16,000,000',
                    'Total Packets Sent  (P-I)': '300',
                }
            },
            'traffic1': {
                'L3 Client': {
                    'Total Packets Sent/Sec': '1,000',
                    'Total Packets Received/Sec': '1,000',
                    'Total Packets Received': '200',
                    'Total Bits Received/Sec': '8,000,000',
                    'Total Packets Sent': '300',
                },
                'L3 Server': {
                    'Total Packets Sent/Sec': '2,000',
                    'Total Packets Received/Sec': '950',
                    'Total Packets Received': '199',
                    'Total Bits Received/Sec': '16,000,000',
                    'Total Packets Sent': '300',
                },
            },
            'L3 Client': {
                'Total Packets Sent/Sec  (P-I)': '1,000',
                'Total Packets Received/Sec  (P-I)': '1,000',
                'Total Packets Received  (P-I)': '200',
                'Total Bits Received/Sec  (P-I)': '8,000,000',
                'Total Packets Sent  (P-I)': '300',
            },
            'L3 Server': {
                'Total Packets Sent/Sec  (P-I)': '2,000',
                'Total Packets Received/Sec  (P-I)': '950',
                'Total Packets Received  (P-I)': '199',
                'Total Bits Received/Sec  (P-I)': '16,000,000',
                'Total Packets Sent  (P-I)': '300',
            }
        }
        data1 = {
            'L3 Client': {
                'Total Packets Sent/Sec': '0',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '200',
                'Total Bits Received/Sec': '8,000,000',
            },
            'L3 Server': {
                'Total Packets Sent/Sec': '0',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '199',
                'Total Bits Received/Sec': '16,000,000',
            },
        }
        data1_pi = {
            'perIntervalStats': {
                'L3 Client': {
                    'Total Packets Sent/Sec  (P-I)': '0',
                    'Total Packets Received/Sec  (P-I)': '0',
                    'Total Packets Received  (P-I)': '200',
                    'Total Bits Received/Sec  (P-I)': '8,000,000',
                },
                'L3 Server': {
                    'Total Packets Sent/Sec  (P-I)': '0',
                    'Total Packets Received/Sec  (P-I)': '0',
                    'Total Packets Received  (P-I)': '199',
                    'Total Bits Received/Sec  (P-I)': '16,000,000',
                }
            },
            'L3 Client': {
                'Total Packets Sent/Sec': '0',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '200',
                'Total Bits Received/Sec': '8,000,000',
            },
            'L3 Server': {
                'Total Packets Sent/Sec': '0',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '199',
                'Total Bits Received/Sec': '16,000,000',
            },
        }
        data2 = {
            'L3 Client': {
                'Total Packets Sent': '200',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '200',
                'Total Bits Received/Sec': '8,000,000',
            },
            'L3 Server': {
                'Total Packets Sent': '200',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '199',
                'Total Bits Received/Sec': '16,000,000',
            },
        }
        data3 = {
            'L3 Client': {
                'Total Packets Sent': '100',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '0',
                'Total Bits Received/Sec': '0',
            },
            'L3 Server': {
                'Total Packets Sent': '100',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '100',
                'Total Bits Received/Sec': '0',
            },
        }
        nothing = {
            'L3 Client': {
                'Total Packets Sent': '0',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '0',
                'Total Bits Received/Sec': '0',
            },
            'L3 Server': {
                'Total Packets Sent': '0',
                'Total Packets Received/Sec': '0',
                'Total Packets Received': '0',
                'Total Bits Received/Sec': '0',
            },
        }
        dmfs = {'traffic0': 'na', 'traffic1': 'na'}
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.action.return_value = data_pi
        subscriber.dmf_handle = dmfs
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}

        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='not_valid')
        self.assertIn(
            'Verification type is not supported. Supported verification types are: throughput, packetcount and rate',
            context.exception.args[0])

        # minimum_rx_percentage
        self.assertIsNotNone(mobile_verify_traffic(subscriber, minimum_rx_percentage=10))
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, minimum_rx_percentage=100)
        self.assertIn(
            'Observed aggregate uplink throughput of 95.0% is less than minimum allowable percentage of 100%!',
            context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, minimum_rx_percentage=90, dmf='1')
        # self.assertIn(
        #     'Observed aggregate downlink throughput of 50.0% is less than minimum allowable percentage of 90%!',
        #     context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, minimum_rx_percentage=90, dmf='2')
        self.assertIn('error: DMF name does not exist.', context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, minimum_rx_percentage=90)
        self.assertIn(
            'Observed aggregate downlink throughput of 50.0% is less than minimum allowable percentage of 90%!',
            context.exception.args[0])
        subscriber.action.return_value = data1_pi
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, minimum_rx_percentage=90)
        self.assertIn('Observed aggregate uplink throughput of 0% is less than minimum allowable percentage of 90%!',
            context.exception.args[0])

        # verify_by='packetcount'
        subscriber.action.return_value = data
        self.assertIsNotNone(mobile_verify_traffic(subscriber, verify_by='packetcount', client_packet_count=200,
                                                   server_packet_count=199))
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='packetcount', client_packet_count=1, server_packet_count=1)
        self.assertIn(
            '200 packets received at client are not equal to the expected 1 packets', context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='packetcount', client_packet_count=200, server_packet_count=1)
        self.assertIn(
            '199 packets received at server are not equal to the expected 1 packets', context.exception.args[0])
        
        # verify_by='rate'
        subscriber.action.return_value = data_pi
        self.assertIsNotNone(mobile_verify_traffic(subscriber, verify_by='rate', server_expected_rate=16,
                                                   client_expected_rate=8))
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='rate', server_expected_rate=1, client_expected_rate=2)
        self.assertIn('Measured rx client traffic rate of 8.0mbps is NOT within ', context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='rate', server_expected_rate=1, client_expected_rate=8)
        self.assertIn('Measured rx server traffic rate of 16.0mbps is NOT within ', context.exception.args[0])

        # verify_by='packetloss'
        subscriber.action.return_value = data
        self.assertIsNotNone(mobile_verify_traffic(subscriber, verify_by='packetloss', packet_loss_client=101,
                                                   packet_loss_server=102))
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='packetloss', packet_loss_client=80, packet_loss_server=80)
        self.assertIn(
            'Server lost 101 packets. Lost packets are higher then the expected 80 packets.', context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='packetloss', packet_loss_client=42, packet_loss_server=102)
        self.assertIn(
            'Client lost 100 packets. Lost packets are higher then the expected 42 packets.', context.exception.args[0])
        
        # verify_by='total_throughput'
        subscriber.action.return_value = data2
        self.assertIsNotNone(mobile_verify_traffic(subscriber, verify_by='total_throughput', packet_loss_client=101,
                                                   packet_loss_server=102))
        subscriber.action.return_value = data
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='total_throughput', packet_loss_client=101,
                                  packet_loss_server=102)
        self.assertIn('less than minimum allowable percentage', context.exception.args[0])
        subscriber.action.return_value = data3
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='total_throughput', packet_loss_client=101,
                                  packet_loss_server=102)
        self.assertIn('less than minimum allowable percentage', context.exception.args[0])
        # No Client/Server sent packets scenario
        subscriber.action.return_value = nothing
        with self.assertRaises(Exception) as context:
            mobile_verify_traffic(subscriber, verify_by='total_throughput', packet_loss_client=101,
                                  packet_loss_server=102)
        self.assertIn('less than minimum allowable percentage', context.exception.args[0])

    def test_mobile_get_packetloss(self):
        data = {
            'L3 Client': {
                'Total Packets Sent/Sec': '1,000',
                'Total Packets Received/Sec': '1,000',
                'Total Packets Received': '200',
                'Total Bits Received/Sec': '8,000,000',
                'Total Packets Sent': '300',
            },
            'L3 Server': {
                'Total Packets Sent/Sec': '2,000',
                'Total Packets Received/Sec': '950',
                'Total Packets Received': '199',
                'Total Bits Received/Sec': '16,000,000',
                'Total Packets Sent': '300',
            },
            'traffic1': {
                'L3 Client': {
                    'Total Packets Sent/Sec': '1,000',
                    'Total Packets Received/Sec': '1,000',
                    'Total Packets Received': '200',
                    'Total Bits Received/Sec': '8,000,000',
                    'Total Packets Sent': '300',
                },
                'L3 Server': {
                    'Total Packets Sent/Sec': '2,000',
                    'Total Packets Received/Sec': '950',
                    'Total Packets Received': '199',
                    'Total Bits Received/Sec': '16,000,000',
                    'Total Packets Sent': '300',
                },
            },
        }
        dmfs = {'traffic0': 'na', 'traffic1': 'na'}
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.action.return_value = data
        subscriber.dmf_handle = dmfs
        builtins.bbe.bbevar = {
            'resources': {subscriber.rt_device_id: {'system': {'primary': {'landslide-manager': 'ip'}}}}}
        loss_dict_valid = {'packet_loss_server': 101, 'packet_loss_client': 100}
        self.assertEqual(mobile_get_packetloss(subscriber), loss_dict_valid)
        self.assertEqual(mobile_get_packetloss(subscriber, dmf='1'), loss_dict_valid)
        with self.assertRaises(Exception) as context:
            mobile_get_packetloss(subscriber, dmf='invalid')
        self.assertIn('error: DMF name does not exist.', context.exception.args[0])

    def test_mobile_create_tft_dict(self):
        kwargs = {
            'precedence': '255',
            'direction': 'bidirectional',
            'protocol': '6',
            'remote_address': '10.1.1.1',
            'src_port_start': '2000',
            'src_port_end': '3000',
            'dst_port_start': '2000',
            'dst_port_end': '3000',
            'tos': '64',
            'security_parameter_index': '5',
            'flow_label': 'flow123',
            'uplink_mbr': '5000',
            'uplink_gbr': '2500',
            'uplink_gate_status': '0',
            'downlink_mbr': '5000',
            'downlink_gbr': '2500',
            'downlink_gate_status': '0',
            'sdf_index': '1',
            'urr_name': 'urr1',
        }
        self.assertIsNotNone(mobile_create_tft_dict(**kwargs))

    def test_mobile_get_ue_session_info(self):
        searchable_text = MagicMock()
        searchable_text.findtext.return_value = '''
            <ip-address>99.0.0.1</ip-address>
            <num-bearers-cups>1</num-bearers-cups>
            <state>EST</state>
            <vrf-id>0x0</vrf-id>
            <apn-name>apntest</apn-name>
            <access-c-peer-address>11.1.11.9</access-c-peer-address>
            <access-u-peer-address>11.1.11.2</access-u-peer-address>
            <anchor-pfe>pfe-3/0/0</anchor-pfe>
            <cpf-seid>0x2710</cpf-seid>
            <upf-seid>0x300000c</upf-seid>
        '''
        builtins.t.get_handle.return_value.pyez.return_value.resp.findall.return_value = [searchable_text]
        self.assertIsNotNone(mobile_get_ue_session_info(router_id='r0', return_by_key='ip'))
        self.assertIsNotNone(mobile_get_ue_session_info(router_id='r0', return_by_key='seid'))
        self.assertIsNotNone(mobile_get_ue_session_info(router_id='r0'))
        self.assertIsNotNone(mobile_get_ue_session_info(router_id='r0', return_by_key='ip', by_random=1))

    def test_mobile_configure_lawful_intercept(self):
        kwargs = {'imsi_increment': '1', 'interface_tag': 'access', 'vlan_id': '221'}
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.subscribers_type = 'cups'
        subscriber.node_start_imsi = '505024101215074'
        subscriber.test_session_handle = 'java0x2'
        subscriber.node_testcase_handle = 'java0x3'
        subscriber.access_interface = 'eth1'
        subscriber.control_interface = 'eth2'
        subscriber.uplink_interface = 'eth3'
        from ipaddress import IPv4Network
        subscriber.access_ip_generator = MagicMock(spec=IPv4Network).hosts()
        subscriber.control_ip_generator = MagicMock(spec=IPv4Network).hosts()
        subscriber.uplink_ip_generator = MagicMock(spec=IPv4Network).hosts()
        self.assertIsNotNone(mobile_configure_lawful_intercept(subscriber, count='1', port_number='2500', **kwargs))
        subscriber.subscribers_type = 'pgw'
        self.assertIsNotNone(mobile_configure_lawful_intercept(subscriber, count='1', port_number='2500', **kwargs))
        kwargs['interface_tag'] = 'control'
        self.assertIsNotNone(mobile_configure_lawful_intercept(subscriber, count='1', port_number='2500', **kwargs))
        kwargs['interface_tag'] = 'uplink'
        self.assertIsNotNone(mobile_configure_lawful_intercept(subscriber, count='1', port_number='2500', **kwargs))
        del kwargs['interface_tag']
        self.assertIsNotNone(mobile_configure_lawful_intercept(subscriber, count='1', port_number='2500', **kwargs))

    def test_mobile_create_usage_rule_dict(self):
        kwargs = {
            'name': 'urr1',
            'measurement_methods': ['volume', 'duration', 'event'],
            'reporting_triggers': ['dropped_dl_traffic_threshold', 'start_of_traffic', 'stop_of_traffic', 'time_quota',
                                   'time_threshold', 'envelope_closure', 'quota_holding_time', 'linked_usage',
                                   'event_threshold', 'volume_quota', 'volume_threshold', 'periodic'],
            'downlink_drop_threshold_packets': '1500',
            'downlink_drop_threshold_bytes': '1000000',
            'measurement_period': '60',
            'time_threshold': '120',
            'time_quota': '180',
            'quota_holding_time': '240',
            'volume_threshold_uplink_bytes': '5000',
            'volume_threshold_total_bytes': '1000000',
            'volume_threshold_downlink_bytes': '6000',
            'volume_quota_total_bytes': '2000000',
            'volume_quota_uplink_bytes': '11000',
            'volume_quota_downlink_bytes': '50000',
        }
        self.assertIsNotNone(mobile_create_usage_rule_dict(**kwargs))
        kwargs['reporting_triggers'] = 'volume_threshold'
        kwargs['measurement_methods'] = 'volume'
        self.assertIsNotNone(mobile_create_usage_rule_dict(**kwargs))
        del kwargs['measurement_methods']
        with self.assertRaises(Exception) as context:
            mobile_create_usage_rule_dict(**kwargs)
        self.assertIn('No measurement method specified in usage rule dictionary', context.exception.args[0])
        kwargs['measurement_methods'] = 'volume'
        del kwargs['reporting_triggers']
        with self.assertRaises(Exception) as context:
            mobile_create_usage_rule_dict(**kwargs)
        self.assertIn('No reporting triggers specified in usage rule dictionary', context.exception.args[0])

    def test_mobile_configure_usage_rules(self):
        kwargs = {
            'name': 'urr1',
            'measurement_methods': ['volume', 'duration', 'event'],
            'reporting_triggers': ['dropped_dl_traffic_threshold', 'start_of_traffic', 'stop_of_traffic', 'time_quota',
                                   'time_threshold', 'envelope_closure', 'quota_holding_time', 'linked_usage',
                                   'event_threshold', 'volume_quota', 'volume_threshold', 'periodic'],
            'downlink_drop_threshold_packets': '1500',
            'downlink_drop_threshold_bytes': '1000000',
            'measurement_period': '60',
            'time_threshold': '120',
            'time_quota': '180',
            'quota_holding_time': '240',
            'volume_threshold_uplink_bytes': '5000',
            'volume_threshold_total_bytes': '1000000',
            'volume_threshold_downlink_bytes': '6000',
            'volume_quota_total_bytes': '2000000',
            'volume_quota_uplink_bytes': '11000',
            'volume_quota_downlink_bytes': '50000',
        }
        ret_dict = mobile_create_usage_rule_dict(**kwargs)

        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.subscribers_type = 'cups'
        subscriber.test_session_handle = 'java0x2'
        subscriber.node_testcase_handle = 'java0x3'
        self.assertTrue(mobile_configure_usage_rules(subscriber=[subscriber, MagicMock(spec=CUPSSubscribers)],
                                                      rule_list=[ret_dict]))
        subscriber.subscribers_type = 'pgw'
        self.assertTrue(mobile_configure_usage_rules(subscriber=subscriber, rule_list=[ret_dict]))
        sdf_dict = {'B0': [{'urr-name': 'urr1'}, {'urr-name': 'urr1'}]}
        self.assertTrue(mobile_configure_usage_rules(subscriber=subscriber, rule_list=[ret_dict], mode='sdf',
                                                      sdf_dict=sdf_dict))
        with self.assertRaises(Exception) as context:
            mobile_configure_usage_rules(subscriber=subscriber, rule_list=[ret_dict], mode='bad', sdf_dict=sdf_dict)
        self.assertIn('mobile_configure_usage_rules mode must be "bearer" or "sdf"', context.exception.args[0])
        with self.assertRaises(Exception) as context:
            mobile_configure_usage_rules(subscriber=subscriber, rule_list=[ret_dict], mode='sdf')
        self.assertIn('sdf_dict must be passed in if using sdf mode', context.exception.args[0])
        sdf_dict['B0'][0] = {}
        with self.assertRaises(Exception) as context:
            mobile_configure_usage_rules(subscriber=subscriber, rule_list=[ret_dict], mode='sdf', sdf_dict=sdf_dict)
        self.assertIn('For SDF, sdf_dict items must include the URR name', context.exception.args[0])
        sdf_dict['B0'][0] = {'urr-name': 'urr2'}
        with self.assertRaises(Exception) as context:
            mobile_configure_usage_rules(subscriber=subscriber, rule_list=[ret_dict], mode='sdf', sdf_dict=sdf_dict)
        self.assertIn('URR name urr2 not found in rule_list', context.exception.args[0])
        del ret_dict['name']
        with self.assertRaises(Exception) as context:
            mobile_configure_usage_rules(subscriber=subscriber, rule_list=[ret_dict], mode='sdf', sdf_dict=sdf_dict)
        self.assertIn('For SDF, each rule must be named', context.exception.args[0])

    def test_mobile_load_custom_pfcp_message(self):
        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.subscribers_type = 'cups'
        subscriber.test_session_handle = 'java0x2'
        subscriber.node_testcase_handle = 'java0x3'
        self.assertTrue(mobile_load_custom_pfcp_message(subscriber=[subscriber, MagicMock(spec=CUPSSubscribers)],
                                                         file_name='Modify-Update-URR', username='dbond'))
        subscriber.subscribers_type = 'pgw'
        self.assertTrue(mobile_load_custom_pfcp_message(subscriber=subscriber, file_name='Modify-Update-URR',
                                                         username='dbond'))

if __name__ == '__main__':
    unittest.main()
