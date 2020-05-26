import unittest2 as unittest
from mock import MagicMock, patch
#from jnpr.toby.hldcl.juniper.security.srx import Srx
from jnpr.toby.hldcl.device import Device
from jnpr.toby.security.appsecure.appqoe_stats_verify import *


class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=Device)
    mocked_obj.log = MagicMock()
    maxDiff = None
    def test_get_appqoe_sla_stats(self):
        rpc_output = {'apbr-sla-statistics': {'apbr-sla-statistics-active-path-down': '3',
                         'apbr-sla-statistics-active-probe-paths': '0',
                         'apbr-sla-statistics-active-probe-sent': '14436',
                         'apbr-sla-statistics-active-probe-sessions': '0',
                         'apbr-sla-statistics-passive-ongoing-sessions': '0',
                         'apbr-sla-statistics-passive-probe-sessions': '0',
                         'apbr-sla-statistics-passive-session-processed': '3339',
                         'apbr-sla-statistics-passive-sessions-sampled': '0',
                         'apbr-sla-statistics-passive-sla-violations': '0'}}

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=rpc_output)
        self.assertEqual(get_appqoe_sla_stats(device=self.mocked_obj), rpc_output['apbr-sla-statistics'])

        try:
            x = get_appqoe_sla_stats()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

    @patch('jnpr.toby.security.appsecure.appqoe_stats_verify.get_appqoe_sla_stats')
    def test_verify_appqoe_sla_stats(self, get_appqoe_sla_stats):
        get_appqoe_sla_stats.return_value = {'apbr-sla-statistics-active-path-down': '3',
                         'apbr-sla-statistics-active-probe-paths': '0',
                         'apbr-sla-statistics-active-probe-sent': '14436',
                         'apbr-sla-statistics-active-probe-sessions': '0',
                         'apbr-sla-statistics-passive-ongoing-sessions': '0',
                         'apbr-sla-statistics-passive-probe-sessions': '0',
                         'apbr-sla-statistics-passive-session-processed': '3339',
                         'apbr-sla-statistics-passive-sessions-sampled': '0',
                         'apbr-sla-statistics-passive-sla-violations': '0'}
        #import pdb
        #pdb.set_trace()
        self.assertTrue(verify_appqoe_sla_stats(device=self.mocked_obj,
                                                 counter_values={'apbr-sla-statistics-passive-probe-sessions': '0',
                                                           'apbr-sla-statistics-active-path-down': '3'},
                                                node="node0"))

        try:
            x = verify_appqoe_sla_stats()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle is a mandatory argument")

        try:
            x = verify_appqoe_sla_stats(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "counter_values is None, it is mandatory argument")

        #stats value mismatch case
        try:
            x = verify_appqoe_sla_stats(device=self.mocked_obj,
                                        counter_values={'apbr-sla-statistics-passive-probe-sessions': '0',
                                                           'apbr-sla-statistics-active-path-down': '9'},)
        except Exception as err:
            self.assertEqual(err.args[0], "APBR sla statistics validation failed")


    def test_get_appqoe_active_probe_stats(self):
        rpc_output = {'apbr-active-statistics': {'apbr-active-statistics-info':
                                                         [{'apbr-active-statistics-details-dest-ip': '42.1.1.1',
                                                             'apbr-active-statistics-details-egress-jit': '558',
                                                             'apbr-active-statistics-details-ingress-jit': '196',
                                                             'apbr-active-statistics-details-pkt-loss': '0',
                                                             'apbr-active-statistics-details-rtt': '8702',
                                                             'apbr-active-statistics-details-src-ip': '42.1.1.2',
                                                             'apbr-active-statistics-details-two-way': '634'},
                                                            {'apbr-active-statistics-details-dest-ip': '41.1.1.1',
                                                             'apbr-active-statistics-details-egress-jit': '310',
                                                             'apbr-active-statistics-details-ingress-jit': '171',
                                                             'apbr-active-statistics-details-pkt-loss': '0',
                                                             'apbr-active-statistics-details-rtt': '5074',
                                                             'apbr-active-statistics-details-src-ip': '41.1.1.2',
                                                             'apbr-active-statistics-details-two-way': '317'},
                                                            {'apbr-active-statistics-details-dest-ip': '40.1.1.1',
                                                             'apbr-active-statistics-details-egress-jit': '199',
                                                             'apbr-active-statistics-details-ingress-jit': '733',
                                                             'apbr-active-statistics-details-pkt-loss': '0',
                                                             'apbr-active-statistics-details-rtt': '6389',
                                                             'apbr-active-statistics-details-src-ip': '40.1.1.2',
                                                             'apbr-active-statistics-details-two-way': '545'}]}}

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=rpc_output)
        self.assertEqual(get_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1'),
                                                       rpc_output['apbr-active-statistics'])

        try:
            x = get_appqoe_active_probe_stats()
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle and probe_name  is a mandatory argument")

    @patch('jnpr.toby.security.appsecure.appqoe_stats_verify.get_appqoe_active_probe_stats')
    def test_verify_appqoe_active_probe_stats(self, probe_stats):
        probe_stats.return_value = {'apbr-active-statistics-info':
                                                         [{'apbr-active-statistics-details-dest-ip': '42.1.1.1',
                                                             'apbr-active-statistics-details-egress-jit': '558',
                                                             'apbr-active-statistics-details-ingress-jit': '196',
                                                             'apbr-active-statistics-details-pkt-loss': '0',
                                                             'apbr-active-statistics-details-rtt': '8702',
                                                             'apbr-active-statistics-details-src-ip': '42.1.1.2',
                                                             'apbr-active-statistics-details-two-way': '634'},
                                                            {'apbr-active-statistics-details-dest-ip': '41.1.1.1',
                                                             'apbr-active-statistics-details-egress-jit': '310',
                                                             'apbr-active-statistics-details-ingress-jit': '171',
                                                             'apbr-active-statistics-details-pkt-loss': '20',
                                                             'apbr-active-statistics-details-rtt': '5074',
                                                             'apbr-active-statistics-details-src-ip': '41.1.1.2',
                                                             'apbr-active-statistics-details-two-way': '317'},
                                                            {'apbr-active-statistics-details-dest-ip': '40.1.1.1',
                                                             'apbr-active-statistics-details-egress-jit': '199',
                                                             'apbr-active-statistics-details-ingress-jit': '733',
                                                             'apbr-active-statistics-details-pkt-loss': '0',
                                                             'apbr-active-statistics-details-rtt': '6389',
                                                             'apbr-active-statistics-details-src-ip': '40.1.1.2',
                                                             'apbr-active-statistics-details-two-way': '545'}]}

        self.assertTrue(verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='41.1.1.2',
                        dest_address='41.1.1.1',target_pkt_loss=[10, 'greatereq'], target_rtt=30000,
                        target_ingress_jitter=[100, 'greatereq'],target_egress_jitter=[300,'greatereq'], target_two_way_jitter=400))

        self.assertTrue(verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='41.1.1.2',
                        dest_address='41.1.1.1', target_pkt_loss=30, target_rtt=[3000, 'greatereq'],
                        target_ingress_jitter=200, target_egress_jitter=400, target_two_way_jitter=[40, 'greatereq']))

        #Negative conditions, one/more of the value mismatch
        try:
            verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='41.1.1.2',
                        dest_address='41.1.1.1', target_pkt_loss=[30, 'greatereq'], target_rtt=30000,
                        target_ingress_jitter=[100, 'greatereq'], target_egress_jitter=[300, 'greatereq'], target_two_way_jitter=400)
        except Exception as err:
            self.assertEqual(err.args[0],
            "AppQoE active probe statistics are not matching - Expected less than or greear than or equal of passed target values")

        try:
            verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='41.1.1.2',
                        dest_address='41.1.1.1', target_pkt_loss=[10, 'greatereq'], target_rtt=3000,
                        target_ingress_jitter=[100, 'greatereq'], target_egress_jitter=[300, 'greatereq'], target_two_way_jitter=400)
        except Exception as err:
            self.assertEqual(err.args[0],
            "AppQoE active probe statistics are not matching - Expected less than or greear than or equal of passed target values")

        try:
            verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='41.1.1.2',
                        dest_address='41.1.1.1', target_pkt_loss=[10, 'greatereq'], target_rtt=30000,
                        target_ingress_jitter=[1000, 'greatereq'], target_egress_jitter=[300, 'greatereq'], target_two_way_jitter=400)
        except Exception as err:
            self.assertEqual(err.args[0],
            "AppQoE active probe statistics are not matching - Expected less than or greear than or equal of passed target values")

        try:
            verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='41.1.1.2',
                        dest_address='41.1.1.1', target_pkt_loss=[10, 'greatereq'], target_rtt=30000,
                        target_ingress_jitter=[100, 'greatereq'], target_egress_jitter=[3000, 'greatereq'], target_two_way_jitter=400)
        except Exception as err:
            self.assertEqual(err.args[0],
            "AppQoE active probe statistics are not matching - Expected less than or greear than or equal of passed target values")

        try:
            verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='41.1.1.2',
                        dest_address='41.1.1.1', target_pkt_loss=[30, 'greatereq'], target_rtt=30000,
                        target_ingress_jitter=[100, 'greatereq'], target_egress_jitter=[300, 'greatereq'], target_two_way_jitter=40)
        except Exception as err:
            self.assertEqual(err.args[0],
            "AppQoE active probe statistics are not matching - Expected less than or greear than or equal of passed target values")

    def test_mandatory_args_verify_appqoe_active_probe_stats(self):
        try:
            x = verify_appqoe_active_probe_stats()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            x = verify_appqoe_active_probe_stats(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'probe_name' is a mandatory argument")

        try:
            x = verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1')
        except Exception as err:
            self.assertEqual(err.args[0], "'source_address' is a mandatory argument")

        try:
            x = verify_appqoe_active_probe_stats(device=self.mocked_obj, probe_name='probe1', source_address='40.1.1.1')
        except Exception as err:
            self.assertEqual(err.args[0], "'dest_address' is a mandatory argument")

    def test_get_appqoe_passive_probe_app_detail(self):
        rpc_output = {'apbr-prof-app':
                        {'apbr-prof-app-appid': '67',
                         'apbr-prof-app-appname': 'HTTP',
                         'apbr-prof-app-appstate': 'SLA MET',
                         'apbr-prof-app-egr-jit': '0',
                         'apbr-prof-app-idlestate': '0',
                         'apbr-prof-app-ing-jit': '0',
                         'apbr-prof-app-ip': '40.1.1.1',
                         'apbr-prof-app-pkt-loss': '0',
                         'apbr-prof-app-port': '35011',
                         'apbr-prof-app-profname': 'apbr1',
                         'apbr-prof-app-riname': 'appqoe',
                         'apbr-prof-app-rtt': '0',
                         'apbr-prof-app-rulename': 'rule-app1',
                         'apbr-prof-app-slaname': 'sla1',
                         'apbr-prof-app-two-way': '0'
                        }
                    }
        version = '20.1R1'
        self.mocked_obj.get_version = MagicMock(return_value=version )
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=rpc_output)
        self.assertEqual(get_appqoe_passive_probe_app_detail(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                         dest_group_name='site1'), rpc_output['apbr-prof-app'])

    @patch('jnpr.toby.security.appsecure.appqoe_stats_verify.get_appqoe_passive_probe_app_detail')
    def test_verify_appqoe_passive_probe_app_detail(self, get_probe_app):
        get_probe_app.return_value = {'apbr-prof-app-appid': '67',
                         'apbr-prof-app-appname': 'HTTP',
                         'apbr-prof-app-appstate': 'SLA MET',
                         'apbr-prof-app-egr-jit': '0',
                         'apbr-prof-app-idlestate': '0',
                         'apbr-prof-app-ing-jit': '0',
                         'apbr-prof-app-ip': '40.1.1.1',
                         'apbr-prof-app-pkt-loss': '20',
                         'apbr-prof-app-port': '35011',
                         'apbr-prof-app-profname': 'apbr1',
                         'apbr-prof-app-riname': 'appqoe',
                         'apbr-prof-app-rtt': '1000',
                         'apbr-prof-app-rulename': 'rule-app1',
                         'apbr-prof-app-slaname': 'sla1',
                         'apbr-prof-app-two-way': '0'
                        }
        version = '20.1R1'
        self.mocked_obj.get_version = MagicMock(return_value=version )
        self.assertTrue(verify_appqoe_passive_probe_app_detail(device=self.mocked_obj, profile_name='apbr1',
                        application='HTTP', dest_group_name='site1', app_details={'apbr-prof-app-appid': '67',
                        'apbr-prof-app-profname': 'apbr1', 'apbr-prof-app-riname': 'appqoe'}))

        self.assertTrue(verify_appqoe_passive_probe_app_detail(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                        dest_group_name='site1', app_details={'apbr-prof-app-appid': '67', 'apbr-prof-app-profname': 'apbr1',
                        'apbr-prof-app-riname': 'appqoe'}, target_rtt=[300,'greatereq'], target_pkt_loss=[10,'greatereq'],
                        target_two_way_jitter= '10'))

        self.assertTrue(verify_appqoe_passive_probe_app_detail(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                                                   dest_group_name='site1', app_details={'apbr-prof-app-appid': '67',
                                                                                         'apbr-prof-app-profname': 'apbr1',
                                                                                         'apbr-prof-app-riname': 'appqoe'},
                                                   target_rtt=3000, target_pkt_loss=30,
                                                   target_two_way_jitter='10'))
        try:
            verify_appqoe_passive_probe_app_detail(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                        dest_group_name='site1', app_details={'apbr-prof-app-appid': '67', 'apbr-prof-app-profname': 'apbr1',
                        'apbr-prof-app-riname': 'appqoe'}, target_rtt=[30000,'greatereq'], target_pkt_loss=[100,'greatereq'],
                        target_two_way_jitter= '10')
        except Exception as err:
            self.assertEqual(err.args[0],"AppQoE passive probe application details are not matching")

        try:
            verify_appqoe_passive_probe_app_detail(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                        dest_group_name='site1', app_details={'apbr-prof-app-appid': '67', 'apbr-prof-app-profname': 'apbr1',
                        'apbr-prof-app-riname': 'appqoe'}, target_rtt=30, target_pkt_loss=10,
                        target_two_way_jitter= '10')
        except Exception as err:
            self.assertEqual(err.args[0],"AppQoE passive probe application details are not matching")

    def test_get_appqoe_application_status(self):
        rpc_output = {'apbr-prof-app-status': {'apbr-prof-app-status-monitor-sess': '0',
                          'apbr-prof-app-status-path-switch': '2',
                          'apbr-prof-app-status-sess': '0',
                          'apbr-prof-app-status-sla-viol': '0'}}
        version = '20.1R1'
        self.mocked_obj.get_version = MagicMock(return_value=version )
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=rpc_output)
        self.assertEqual(get_appqoe_application_status(device=self.mocked_obj, profile_name='apbr1',
                        application='HTTP', dest_group_name='site1'), rpc_output['apbr-prof-app-status'])

    @patch('jnpr.toby.security.appsecure.appqoe_stats_verify.get_appqoe_application_status')
    def test_verify_appqoe_application_status(self, app_status):
        app_status.return_value = {'apbr-prof-app-status-monitor-sess': '0',
                          'apbr-prof-app-status-path-switch': '2',
                          'apbr-prof-app-status-sess': '0',
                          'apbr-prof-app-status-sla-viol': '0'}

        self.assertTrue(verify_appqoe_application_status(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                        dest_group_name='site1',app_status={'apbr-prof-app-status-sla-viol': 0,
                                                     'apbr-prof-app-status-path-switch': 2}))
        try:
            verify_appqoe_application_status(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                                             dest_group_name='site1', app_status={'apbr-prof-app-status-sla-viol': 3,
                                                                                  'apbr-prof-app-status-path-switch': 2})
        except Exception as err:
            self.assertEqual(err.args[0], "Application status validation failed")

        app_status.return_value = {}
        try:
            verify_appqoe_application_status(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                                             dest_group_name='site1', app_status={'apbr-prof-app-status-sla-viol': 3,
                                                                                  'apbr-prof-app-status-path-switch': 2})
        except Exception as err:
            self.assertEqual(err.args[0], "Application status validation failed")

        try:
            x = verify_appqoe_application_status(device=self.mocked_obj, profile_name='apbr1', application='HTTP')
        except Exception as err:
            self.assertEqual(err.args[0], "Device handle, profile_name and dest_group_name is a mandatory argument")

        try:
            x = verify_appqoe_application_status(device=self.mocked_obj, profile_name='apbr1', dest_group_name='site1')
        except Exception as err:
            self.assertEqual(err.args[0], "Either Application or DSCP is mandatory argument")

        try:
            x = verify_appqoe_application_status(device=self.mocked_obj, profile_name='apbr1', application='HTTP',
                                             dest_group_name='site1')
        except Exception as err:
            self.assertEqual(err.args[0], "app_status is None, it is mandatory argument")

    def test_get_appid_counter(self):
        rpc_output = {'appid-counter-information': {'appid-counter-usp': {'counter-name': ['Unknown applications',
                                                  'Encrpted unknown applications',
                                                  'Cache hits pkt-plugin',
                                                  'Cache hits stream-plugin',
                                                  'Cache misses pkt-plugin',
                                                  'Cache misses stream-plugin',
                                                  'Client-to-server packets processed',
                                                  'Server-to-client packets processed',
                                                  'Client-to-server bytes processed',
                                                  'Server-to-client bytes processed',
                                                  'Client-to-server encrypted packets processed',
                                                  'Server-to-client encrypted packets processed',
                                                  'Client-to-server encrypted bytes processed',
                                                  'Server-to-client encrypted bytes processed',
                                                  'Sessions bypassed due to resource allocation failure',
                                                  'Segment case 1 - New segment to left',
                                                  'Segment case 2 - New segment overlap right',
                                                  'Segment case 3 - Old segment overlapped',
                                                  'Segment case 4 - New segment overlapped',
                                                  'Segment case 5 - New segment overlap left',
                                                  'Segment case 6 - New segment to right'],
                                                   'counter-value': ['0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0',
                                                                       '0'],
                                                     'pic': '0/0'}}}

        expec_output ={'Client-to-server encrypted packets processed': '0', 'Client-to-server encrypted bytes processed': '0',
                      'Server-to-client bytes processed': '0', 'Segment case 2 - New segment overlap right': '0',
                      'Segment case 3 - Old segment overlapped': '0', 'Encrpted unknown applications': '0', 'Unknown applications': '0',
                      'Server-to-client encrypted packets processed': '0', 'Cache hits stream-plugin': '0', 'Segment case 1 - New segment to left': '0',
                      'Server-to-client encrypted bytes processed': '0', 'Cache misses pkt-plugin': '0', 'Client-to-server bytes processed': '0',
                      'Segment case 5 - New segment overlap left': '0', 'Cache misses stream-plugin': '0', 'Segment case 6 - New segment to right': '0',
                      'Cache hits pkt-plugin': '0', 'Client-to-server packets processed': '0', 'Segment case 4 - New segment overlapped': '0',
                      'Server-to-client packets processed': '0', 'Sessions bypassed due to resource allocation failure': '0'}

        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=rpc_output)
        self.assertEqual(get_appid_counter(device=self.mocked_obj), expec_output)

    @patch('jnpr.toby.security.appsecure.appqoe_stats_verify.get_appid_counter')
    def test_verify_appid_counter(self, app_counter):
        app_counter.return_value = {'Client-to-server encrypted packets processed': '0', 'Client-to-server encrypted bytes processed': '0',
                      'Server-to-client bytes processed': '0', 'Segment case 2 - New segment overlap right': '0',
                      'Segment case 3 - Old segment overlapped': '0', 'Encrpted unknown applications': '0', 'Unknown applications': '0',
                      'Server-to-client encrypted packets processed': '0', 'Cache hits stream-plugin': '0', 'Segment case 1 - New segment to left': '0',
                      'Server-to-client encrypted bytes processed': '0', 'Cache misses pkt-plugin': '0', 'Client-to-server bytes processed': '0',
                      'Segment case 5 - New segment overlap left': '0', 'Cache misses stream-plugin': '0', 'Segment case 6 - New segment to right': '0',
                      'Cache hits pkt-plugin': '0', 'Client-to-server packets processed': '0', 'Segment case 4 - New segment overlapped': '0',
                      'Server-to-client packets processed': '0', 'Sessions bypassed due to resource allocation failure': '0'}

        self.assertTrue(verify_appid_counter(device=self.mocked_obj,counter_values={'Unknown applications':'0'}))
        try:
            verify_appid_counter(device=self.mocked_obj, counter_values={'Unknown applications': '1'})
        except Exception as err:
            self.assertEqual(err.args[0], "Application counters are not matchin")
        try:
            verify_appid_counter(device=self.mocked_obj, counter_values={'no key applications': '1'})
        except Exception as err:
            self.assertEqual(err.args[0], "Application counters are not matchin")

        #mandatory args check
        try:
            verify_appid_counter(counter_values={'no key applications': '1'})
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")
        try:
            verify_appid_counter(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "counter_values argument is mandatory argument")
        try:
            verify_appid_counter(device=self.mocked_obj, counter_values=['no key applications', '1'])
        except Exception as err:
            self.assertEqual(err.args[0], "counter_values should be of dictionary type")

    def test_get_next_hop_id(self):
        rpc_output = {'apbr-prof-app-brief':
                        {'apbr-prof-app-brief-info':
                            {'apbr-prof-app-brief-ip': '13.13.13.1',
                             'apbr-prof-app-brief-dpg': 'site1',
                             'apbr-prof-app-brief-nh': '262142',
                             'apbr-prof-app-brief-server-ip': 'N/A' 
                            }
                        }
                    }
        self.mocked_obj.execute_as_rpc_command = MagicMock(return_value=rpc_output)
        self.assertEqual(get_next_hop_id(device=self.mocked_obj, profile_name='apbr1', application='HTTP'), rpc_output)

