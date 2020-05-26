"""
subscribers.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbevar.interfaces import BBEVarInterface
import builtins
from jnpr.toby.bbe.bbevar.subscribers import DHCPSubscribers, PPPoESubscribers, L2TPSubscribers, \
    L2BSASubscribers, HAGSubscribers, StaticSubscribers, CUPSSubscribers, PGWSubscribers, FWASubscribers

builtins.t = MagicMock(spec=init)
rinterface = MagicMock(spec=BBEVarInterface)
rinterface.device_id = 'r0'
rinterface.interface_id = 'access0'
rinterface.interface_pic = 'ge-1/0/0'
rtinterface = MagicMock(spec=BBEVarInterface)
rtinterface.device_id = 'rt0'
rtinterface.interface_pic = '3/1'
rinterface.device_name = 'router'
rtinterface.interface_link = 'access0'
builtins.t.get_handle.return_value = MagicMock()
builtins.t.log = MagicMock()

class TestSubscribers(unittest.TestCase):
    """
    test the subscribers.py for the different subscribers types
    """
    def test_class_cupssubscribers(self):
        rinterface.interface_config = {'description': 'access interface 0',
                                       'subscribers': {'cups': [{'session-count': 10,
                                                                 'tag': '5gtest1',
                                                                 'default-bearers': '1',
                                                                 'dedicated-bearers': '0',
                                                                 'access-peer-type': 'spirent',
                                                                 'user-base-address': '10.1.1.1/24',
                                                                 'user-v6-base-address': 'FEED:D00D::/24',
                                                                 'control-peer-type': 'spirent',
                                                                 'control-base-address': '10.1.1.1/24',
                                                                 'control-v6-base-address': 'FEED:D00D::/24',
                                                                 'uplink-peer-type': 'spirent',
                                                                 'uplink-base-address': '30.1.1.1/24',
                                                                 'uplink-v6-base-address': 'FEED:BABE::/24',
                                                                 'bearer-ipv4-addr-pool': '77.0.0.1',
                                                                 'apn-name': 'test-apn',
                                                                 'total-apns': '1',
                                                                 'session-groups': {'group1': 1, 'group2': 2},
                                                                 'test-activity': 'Command Mode',
                                                                 'home-addr-type': 2,
                                                                 'use-loopback-access': 'true',
                                                                 'use-loopback-control': 'true',
                                                                 'enodeb-user-node-count': 10,
                                                                 'sxab-control-node-count': 10,
                                                                 'access-vlan-id': 100,
                                                                 'control-vlan-id': 200,
                                                                 'uplink-vlan-id': 100
                                        }]}}

        builtins.bbe = MagicMock()
        # Access, Control, Uplink all have a single port
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [MagicMock(spec=BBEVarInterface)],
                                                   [MagicMock(spec=BBEVarInterface)]]
        sub = CUPSSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='cups', tag='5gtest1')
        self.assertIsInstance(sub, CUPSSubscribers)
        rinterface.interface_config['subscribers']['cups'][0].pop('session-groups')

        # Access and Control consolidated to single port
        rinterface.interface_config['subscribers']['cups'][0]['control-base-address'] = '20.1.1.1/24'
        rinterface.interface_config['subscribers']['cups'][0]['control-v6-base-address'] = 'C0DE:D00D::/24'
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [],
                                                   [MagicMock(spec=BBEVarInterface)]]
        sub = CUPSSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='cups', tag='5gtest1')
        self.assertIsInstance(sub, CUPSSubscribers)
        del rinterface.interface_config['subscribers']['cups'][0]['control-v6-base-address']
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [],
                                                   [MagicMock(spec=BBEVarInterface)]]
        sub = CUPSSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='cups', tag='5gtest1')
        self.assertIsInstance(sub, CUPSSubscribers)

        # Exception path when Access has < 1 port
        builtins.bbe.get_interfaces.side_effect = [[], [MagicMock(spec=BBEVarInterface)],
                                                   [MagicMock(spec=BBEVarInterface)]]
        try:
            sub = CUPSSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='cups', tag='5gtest1')
        except Exception as err:
            self.assertTrue('Must have minimum of 1 access and 1 uplink interface' in err.args[0])

        # Exception path when Uplink has < 1 port (sufficient to check just access, but being thorough)
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [MagicMock(spec=BBEVarInterface)],
                                                   []]
        try:
            sub = CUPSSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='cups', tag='5gtest1')
        except Exception as err:
            self.assertTrue('Must have minimum of 1 access and 1 uplink interface' in err.args[0])



    def test_cups_subscriber_action(self):

        subscriber = MagicMock(spec=CUPSSubscribers)
        subscriber.rt_device_id = 'rt0'
        subscriber.test_session_handle = '0x29'
        subscriber.test_session_name = 'session1'
        subscriber.node_test_case_name = 'dbond_SGW_Node'
        subscriber.nodal_test_case_name = 'dbond_SGW_Nodal'
        subscriber.libname = 'ixia'
        subscriber.access_interface = 'eth0'
        subscriber.uplink_interface = 'eth1'
        subscriber.control_interface = 'eth2'
        subscriber.tsname = 'test'
        subscriber.isactive = False

        builtins.t._log_dir = MagicMock()
        try:
            CUPSSubscribers.action(subscriber, action='notstart')
        except Exception as err:
            self.assertEqual(err.args[0], 'action notstart is not supported')

        result = CUPSSubscribers.action(subscriber, action='results')
        self.assertIsNotNone(result)
        for action in ['start', 'stop', 'abort', 'logout', 'delete', 'continue', 'report', 'start_with_auto_pcap',
                       'automation_control']:
            result = CUPSSubscribers.action(subscriber, action)
            self.assertIsNone(result)

        for action in ['capture_start', 'capture_stop', 'capture_save']:
            for port in ['access', 'uplink', 'control', 'all']:
                if action == 'capture_start':
                    subscriber.isactive = False
                result = CUPSSubscribers.action(subscriber, action, port=port)
                if action == 'capture_save':
                    self.assertIsNotNone(result)
                else:
                    self.assertIsNone(result)

        # action=check_session_status
        try:
            CUPSSubscribers.action(subscriber, action='check_session_status')
        except Exception as err:
            self.assertTrue('kwargs[\'state\'] is a required parameter for this action' in err.args[0])

        builtins.t.get_handle.return_value.invoke.return_value = 'complete'
        result = CUPSSubscribers.action(subscriber, action='check_session_status', state='complete')
        self.assertIsNone(result)

        try:
            CUPSSubscribers.action(subscriber, action='check_session_status', state='waiting')
        except Exception as err:
            self.assertTrue('Test Session state is not' in err.args[0])

        # action=capture_config
        for port in ['access', 'uplink', 'control']:
            result = CUPSSubscribers.action(subscriber, action='capture_config', port=port)
            self.assertIsNone(result)
        # action=is_fireball
        builtins.t.get_handle.return_value.invoke.return_value = {'DataGenPerformance': True}
        self.assertIsInstance(CUPSSubscribers.action(subscriber, action='is_fireball'), bool)

    def test_class_pgwsubscribers(self):
        rinterface.interface_config = {'description': 'access interface 0',
                                       'subscribers': {'pgw': [{'session-count': 10,
                                                                 'tag': '5gtest1',
                                                                 'default-bearers': '1',
                                                                 'dedicated-bearers': '0',
                                                                 'access-peer-type': 'spirent',
                                                                 'user-base-address': '10.1.1.1/24',
                                                                 'user-v6-base-address': 'FEED:D00D::/24',
                                                                 'control-peer-type': 'spirent',
                                                                 'control-base-address': '10.1.1.1/24',
                                                                 'control-v6-base-address': 'FEED:D00D::/24',
                                                                 'uplink-peer-type': 'spirent',
                                                                 'uplink-base-address': '30.1.1.1/24',
                                                                 'uplink-v6-base-address': 'FEED:BABE::/24',
                                                                 'bearer-ipv4-addr-pool': '77.0.0.1',
                                                                 'apn-name': 'test-apn',
                                                                 'total-apns': '1',
                                                                 'session-groups': {'group1': 1, 'group2': 2},
                                                                 'test-activity': 'Command Mode',
                                                                 'home-addr-type': 2,
                                                                 'use-loopback-access': 'true',
                                                                 'use-loopback-control': 'true',                                                                 'sgw-control-node-count': 10,
                                                                 'sxb-control-node-count': 10,
                                                                 'access-vlan-id': 100,
                                                                 'control-vlan-id': 200,
                                                                 'uplink-vlan-id': 100
                                        }]}}

        builtins.bbe = MagicMock()
        # Access, Control, Uplink all have a single port
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [MagicMock(spec=BBEVarInterface)],
                                                   [MagicMock(spec=BBEVarInterface)]]
        sub = PGWSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='pgw', tag='5gtest1')
        self.assertIsInstance(sub, PGWSubscribers)
        rinterface.interface_config['subscribers']['pgw'][0].pop('session-groups')

        # Access and Control consolidated to single port
        rinterface.interface_config['subscribers']['pgw'][0]['control-base-address'] = '20.1.1.1/24'
        rinterface.interface_config['subscribers']['pgw'][0]['control-v6-base-address'] = 'C0DE:D00D::/24'
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [],
                                                   [MagicMock(spec=BBEVarInterface)]]
        sub = PGWSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='pgw', tag='5gtest1')
        self.assertIsInstance(sub, PGWSubscribers)
        del rinterface.interface_config['subscribers']['pgw'][0]['control-v6-base-address']
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [],
                                                   [MagicMock(spec=BBEVarInterface)]]
        sub = PGWSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='pgw', tag='5gtest1')
        self.assertIsInstance(sub, PGWSubscribers)

        # Exception path when Access has < 1 port
        builtins.bbe.get_interfaces.side_effect = [[], [MagicMock(spec=BBEVarInterface)],
                                                   [MagicMock(spec=BBEVarInterface)]]
        try:
            sub = PGWSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='pgw', tag='5gtest1')
        except Exception as err:
            self.assertTrue('Must have minimum of 1 access and 1 uplink interface' in err.args[0])

        # Exception path when Uplink has < 1 port (sufficient to check just access, but being thorough)
        builtins.bbe.get_interfaces.side_effect = [[MagicMock(spec=BBEVarInterface)], [MagicMock(spec=BBEVarInterface)],
                                                   []]
        try:
            sub = PGWSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='pgw', tag='5gtest1')
        except Exception as err:
            self.assertTrue('Must have minimum of 1 access and 1 uplink interface' in err.args[0])

    def test_pgw_subscriber_action(self):

        subscriber = MagicMock(spec=PGWSubscribers)
        subscriber.rt_device_id = 'rt0'
        subscriber.test_session_handle = '0x29'
        subscriber.test_session_name = 'session1'
        subscriber.node_test_case_name = 'dbond_SGW_Node'
        subscriber.nodal_test_case_name = 'dbond_SGW_Nodal'
        subscriber.libname = 'ixia'
        subscriber.access_interface = 'eth0'
        subscriber.uplink_interface = 'eth1'
        subscriber.control_interface = 'eth2'
        subscriber.tsname = 'test'
        subscriber.isactive = False

        builtins.t._log_dir = MagicMock()
        try:
            PGWSubscribers.action(subscriber, action='notstart')
        except Exception as err:
            self.assertEqual(err.args[0], 'action notstart is not supported')

        result = PGWSubscribers.action(subscriber, action='results')
        self.assertIsNotNone(result)
        for action in ['start', 'stop', 'abort', 'logout', 'delete', 'continue', 'report', 'start_with_auto_pcap',
                       'automation_control']:
            result = PGWSubscribers.action(subscriber, action)
            self.assertIsNone(result)

        for action in ['capture_start', 'capture_stop', 'capture_save']:
            for port in ['access', 'uplink', 'control', 'all']:
                if action == 'capture_start':
                    subscriber.isactive = False
                result = PGWSubscribers.action(subscriber, action, port=port)
                if action == 'capture_save':
                    self.assertIsNotNone(result)
                else:
                    self.assertIsNone(result)

        # action=check_session_status
        try:
            PGWSubscribers.action(subscriber, action='check_session_status')
        except Exception as err:
            self.assertTrue('kwargs[\'state\'] is a required parameter for this action' in err.args[0])

        builtins.t.get_handle.return_value.invoke.return_value = 'complete'
        result = PGWSubscribers.action(subscriber, action='check_session_status', state='complete')
        self.assertIsNone(result)

        try:
            PGWSubscribers.action(subscriber, action='check_session_status', state='waiting')
        except Exception as err:
            self.assertTrue('Test Session state is not' in err.args[0])

        # action=capture_config
        for port in ['access', 'uplink', 'control']:
            result = PGWSubscribers.action(subscriber, action='capture_config', port=port)
            self.assertIsNone(result)
        # action=is_fireball
        builtins.t.get_handle.return_value.invoke.return_value = {'DataGenPerformance': True}
        self.assertIsInstance(PGWSubscribers.action(subscriber, action='is_fireball'), bool)

    def test_class_fwasubscribers(self):
        rinterface.interface_config = {'description': 'access interface 0',
                                       'subscribers': {'fwa': [{'count': 10,
                                                                'tag': 'fwatest1',
                                                                'family': 'ipv4',
                                                                'sut-loopback': '1.2.3.4',
                                                                's11': {},
                                                                'dhcp': {'client-id': 'testuser1',
                                                                         'retries': 30,
                                                                         'v6-ia-type': 'IA_PD'},
                                                                'traffic': {'data-profile': [
                                                                    {'client-port': 2000,
                                                                     'client-port-mode': 'random',
                                                                     'initiate-side': 'client',
                                                                     'name': 'udp_traffic',
                                                                     'packet-size': 550,
                                                                     'segment-size': 880,
                                                                     'server-port': 1003,
                                                                     'start': True,
                                                                     'tos': [0,
                                                                             32,
                                                                             64,
                                                                             96,
                                                                             128],
                                                                     'transaction': 'continuous',
                                                                     'transaction-rate': 1000,
                                                                     'ttl': 64,
                                                                     'type': 'udp',
                                                                     'udp-burst-transaction-count': 10}],
                                                                    'dualstack': True,
                                                                    'gateway': '10.1.5.1',
                                                                    'mtu': 1470,
                                                                    'network-host-type': 'local',
                                                                    'node-count': 1,
                                                                    'start-delay': 1000,
                                                                    'start-ip': '15.1.8.1/16',
                                                                    'start-when': 'all',
                                                                    'svlan-id': 1,
                                                                    'v6-gateway': '2000::1',
                                                                    'v6-node-count': 1,
                                                                    'v6-start-ip': '2000::2/48',
                                                                    'vlan-id': 1},
                                                                'devices': {'sgw': {'control-address': '10.1.5.10',
                                                                                    'user-address': '10.1.4.1'},
                                                                            'pgw': {'address': '10.1.5.11'},
                                                                            'mme-control-node': {'start-ip': '10.1.4.3',
                                                                                                 'count': '1'},
                                                                            'enodeb-user-node': {
                                                                                'start-ip': '10.1.4.4'},
                                                                            'sgw-control-node': {'count': '1',
                                                                                                 'start-ip':
                                                                                                     '10.1.5.10'},
                                                                            }}]}}
        device = FWASubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='fwa', tag='fwatest1')
        self.assertIsInstance(device, FWASubscribers)
        rinterface.interface_config['subscribers']['fwa'][0].pop('s11')
        device = FWASubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='fwa', tag='fwatest1')
        self.assertIsInstance(device, FWASubscribers)

    def test_class_hagsubscribers(self):

        rinterface.interface_config = \
            {'description': 'access interface 0',
             'subscribers': {'hag': [{'count': 100,
                                      'devices': {'dsl-node': {'start-ip': '40.1.2.4'},
                                                  'gateway': '40.1.1.1',
                                                  'lte-node': {'activation-rate': 100,
                                                               'count': 100,
                                                               'deactivation-rate': 100,
                                                               'start-ip': '40.1.1.2/16'}},
                                      'dhcp': {'client-id': 'testuser1',
                                               'retries': 30,
                                               'v6-ia-type': 'IA_PD'},
                                      'family': 'ipv4',
                                      'hybrid-access': {'bypass-traffic-rate': 750,
                                                        'client-id': 'Testuser1',
                                                        'dsl': {'no-answer-retries': 3,
                                                                'packet-distribution': 1,
                                                                'protocol': 'annexb',
                                                                'setup-deny-retries': 3,
                                                                'setup-request-timeout': 10,
                                                                'setup-retry-interval': 30,
                                                                'sync-rate': 5000},
                                                        'ipv6-prefix-haap': '1002::1',
                                                        'ipv6-prefix-th': '1002::1',
                                                        'lte': {'no-answer-retries': 3,
                                                                'packet-distribution': 1,
                                                                'setup-deny-retries': 3,
                                                                'setup-request-timeout': 10,
                                                                'setup-retry-interval': 30},
                                                        'packet-reorder': 0},
                                      'mac': '00:11:03:04:05:06',
                                      'sut-loopback': '172.1.1.1',
                                      'tag': 'hagtest1',
                                      'traffic': {'data-profile': [
                                                                   {'client-port': 2000,
                                                                    'client-port-mode': 'random',
                                                                    'initiate-side': 'client',
                                                                    'name': 'udp_traffic',
                                                                    'packet-size': 550,
                                                                    'segment-size': 880,
                                                                    'server-port': 1003,
                                                                    'start': True,
                                                                    'tos': [0,
                                                                            32,
                                                                            64,
                                                                            96,
                                                                            128],
                                                                    'transaction': 'continuous',
                                                                    'transaction-rate': 1000,
                                                                    'ttl': 64,
                                                                    'type': 'udp',
                                                                    'udp-burst-transaction-count': 10}],
                                                  'error-injection':{'type':'aa', 'distribution':'flexible',
                                                                     'inbound-rate':'10k', 'outbound-rate':'100k',
                                                                     'bad-source-ip':'1'},
                                                  'dualstack': True,
                                                  'gateway': '20.1.20.1',
                                                  'mtu': 1470,
                                                  'network-host-type': 'local',
                                                  'node-count': 1,
                                                  'start-delay': 1000,
                                                  'start-ip': '20.1.20.2/16',
                                                  'start-when': 'all',
                                                  'svlan-id': 1,
                                                  'v6-gateway': '2000::1',
                                                  'v6-node-count': 1,
                                                  'v6-start-ip': '2000::2/48',
                                                  'vlan-id': 1}
                                                  },
                                     {'count': 16000,
                                      'devices': {'dsl-node': {'start-ip': '40.1.1.4'},
                                                  'gateway': '40.1.1.1',
                                                  'lte-node': {'activation-rate': 100,
                                                               'count': 1,
                                                               'deactivation-rate': 100,
                                                               'start-ip': '40.1.1.2'}},
                                      'dhcp': {'client-id': 'testuser1',
                                               'retries': 30,
                                               'v6-ia-type': 'IA_PD'},
                                      'family': 'dual',
                                      'hybrid-access': {'bypass-traffic-rate': 750,
                                                        'client-id': 'Testuser1',
                                                        'dsl': {'no-answer-retries': 3,
                                                                'packet-distribution': 1,
                                                                'protocol': 'annexb',
                                                                'setup-deny-retries': 3,
                                                                'setup-request-timeout': 10,
                                                                'setup-retry-interval': 30,
                                                                'sync-rate': 5000},
                                                        'ipv6-prefix-haap': '1002::1',
                                                        'ipv6-prefix-th': '1002::1',
                                                        'lte': {'no-answer-retries': 3,
                                                                'packet-distribution': 1,
                                                                'setup-deny-retries': 3,
                                                                'setup-request-timeout': 10,
                                                                'setup-retry-interval': 30},
                                                        'packet-reorder': 0},
                                      'mac': '00:11:03:04:05:07',
                                      'sut-loopback': '172.1.1.1',
                                      'tag': 'hagtest2',
                                      'traffic': {'data-profile': [{'client-port-mode': 'random',
                                                                    'host-expension-ratio': 2,
                                                                    'initiate-side': 'client',
                                                                    'name': 'raw_traffic',
                                                                    'packet-size': 1450,
                                                                    'segment-size': 1000,
                                                                    'server-port': 3001,
                                                                    'start': True,
                                                                    'tos': [6],
                                                                    'transaction': 'continuous',
                                                                    'transaction-rate': 1000,
                                                                    'ttl': 64,
                                                                    'type': 'raw'},
                                                                   {'client-port': 2000,
                                                                    'client-port-mode': 'random',
                                                                    'initiate-side': 'client',
                                                                    'name': 'udp_traffic',
                                                                    'packet-size': 1450,
                                                                    'segment-size': 80,
                                                                    'server-port': 1003,
                                                                    'start': True,
                                                                    'tos': [0,
                                                                            32,
                                                                            64,
                                                                            96,
                                                                            128],
                                                                    'transaction': 'continuous',
                                                                    'transaction-rate': 1000,
                                                                    'ttl': 64,
                                                                    'type': 'udp',
                                                                    'udp-burst-transaction-count': 10},
                                                                   {'3way-handshake': False,
                                                                    'client-port': 3000,
                                                                    'client-port-mode': 'random',
                                                                    'disconnect-type': 'fin',
                                                                    'initiate-side': 'client',
                                                                    'max-packets-before-ack': 0,
                                                                    'max-segment-size': 0,
                                                                    'min-tcp-header-size': 20,
                                                                    'name': 'tcp_traffic',
                                                                    'packet-size': 1450,
                                                                    'segment-size': 700,
                                                                    'server-port': 2004,
                                                                    'slowstart-congestionavoid': False,
                                                                    'socket-disc-side': 'client',
                                                                    'start': True,
                                                                    'tos': [24, 32, 48],
                                                                    'transaction': 'continuous',
                                                                    'transaction-rate': 1000,
                                                                    'ttl': 64,
                                                                    'type': 'tcp',
                                                                    'window-size': 32768}],
                                                  'do-not-fragment': False,
                                                  'dualstack': True,
                                                  'gateway': '20.1.20.1',
                                                  'mtu': 1470,
                                                  'network-host-type': 'local',
                                                  'node-count': 1,
                                                  'start-delay': 1000,
                                                  'start-ip': '20.1.20.2/16',
                                                  'start-when': 'all',
                                                  'svlan-id': 1,
                                                  'v6-gateway': '2000::1',
                                                  'v6-node-count': 1,
                                                  'v6-start-ip': '2000::2/48',
                                                  'vlan-id': 1}},
                                     {'count': 16000,
                                      'devices': {'dsl-node': {'start-ip': '40.1.1.4'},
                                                  'gateway': '40.1.1.1',
                                                  'lte-node': {'activation-rate': 100,
                                                               'count': 1,
                                                               'deactivation-rate': 100,
                                                               'start-ip': '40.1.1.2'}},
                                      'dhcp': {'client-id': 'testuser1',
                                               'retries': 30,
                                               'v6-ia-type': 'IA_PD'},
                                      'family': 'ipv4',
                                      'hybrid-access': {'bypass-traffic-rate': 750,
                                                        'client-id': 'Testuser1',
                                                        'dsl': {'no-answer-retries': 3,
                                                                'packet-distribution': 1,
                                                                'protocol': 'annexb',
                                                                'setup-deny-retries': 3,
                                                                'setup-request-timeout': 10,
                                                                'setup-retry-interval': 30,
                                                                'sync-rate': 5000},
                                                        'ipv6-prefix-haap': '1002::1',
                                                        'ipv6-prefix-th': '1002::1',
                                                        'lte': {'no-answer-retries': 3,
                                                                'packet-distribution': 1,
                                                                'setup-deny-retries': 3,
                                                                'setup-request-timeout': 10,
                                                                'setup-retry-interval': 30},
                                                        'packet-reorder': 0},
                                      'mac': '00:11:03:04:05:08',
                                      'sut-loopback': '172.1.1.1',
                                      'tag': 'hagtest3',
                                      'li': {'start-ip': '10.0.0.1', 'nexthop-ip': '10.0.0.2'},
                                      'traffic': {'data-profile': [{'client-port-mode': 'random',
                                                                    'initiate-side': 'client',
                                                                    'name': 'ping_traffic',
                                                                    'packet-size': 1450,
                                                                    'segment-size': 900,
                                                                    'server-port': 3001,
                                                                    'start': True,
                                                                    'transaction': 'continuous',
                                                                    'transaction-rate': 1000,
                                                                    'ttl': 64,
                                                                    'type': 'ping'}],
                                                  'do-not-fragment': False,
                                                  'dualstack': False,
                                                  'gateway': '20.1.20.1',
                                                  'mtu': 1470,
                                                  'network-host-type': 'local',
                                                  'node-count': 1,
                                                  'start-delay': 1000,
                                                  'start-ip': '20.1.20.2',
                                                  'start-when': 'all',
                                                  'svlan-id': 1,
                                                  'vlan-id': 1}}]}}
        for tag in ['hagtest1', 'hagtest2', 'hagtest3']:
            device = HAGSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='hag', tag=tag)
            self.assertIsInstance(device, HAGSubscribers)

    def test_hag_subscriber_action(self):

        hag = MagicMock(spec=HAGSubscribers)
        hag.rt_device_id = 'rt0'
        hag.test_session_handle = '0x29'
        hag.test_session_name = 'session1'
        hag.libname = 'ixia'
        hag.access_interface = 'eth0'
        hag.uplink_interface = 'eth1'
        hag.tsname = 'test'
        hag.isactive = False

        builtins.t._log_dir = MagicMock()
        try:
            HAGSubscribers.action(hag, action='notstart')
        except Exception as err:
            self.assertEqual(err.args[0], 'action notstart is not supported')

        result = HAGSubscribers.action(hag, action='results')
        self.assertIsNotNone(result)
        for action in ['start', 'stop', 'abort', 'logout', 'delete', 'continue', 'report']:
            result = HAGSubscribers.action(hag, action)
            self.assertIsNone(result)

        for action in ['capture_start', 'capture_stop', 'capture_save']:
            for port in ['access', 'uplink', 'all']:
                result = HAGSubscribers.action(hag, action, port=port)
                if action == 'capture_save':
                    self.assertIsNotNone(result)
                else:
                    self.assertIsNone(result)

        # action=check_session_status
        try:
            HAGSubscribers.action(hag, action='check_session_status')
        except Exception as err:
            self.assertTrue('kwargs[\'state\'] is a required parameter for this action' in err.args[0])

        builtins.t.get_handle.return_value.invoke.return_value = 'complete'
        result = HAGSubscribers.action(hag, action='check_session_status', state='complete')
        self.assertIsNone(result)

        try:
            HAGSubscribers.action(hag, action='check_session_status', state='waiting')
        except Exception as err:
            self.assertTrue('Test Session state is not' in err.args[0])


    def test_class_dhcpsubscribers(self):
        rinterface.interface_config = \
            {'ae': {'active': False, 'bundle': 'ae0', 'enable': 0},
             'description': 'access interface 0',
             'subscribers': {'dhcp': [{'clr': 200,
                                       'count': 16000,
                                       'csr': 250,
                                       'dhcpv6-ia-type': 'iapd',
                                       'family': 'dual',
                                       'igmp': {'version': '3',
                                                'filter-mode': 'include',
                                                'iptv': '0',
                                                'group': {'start': '225.0.0.1',
                                                          'step': '0.0.0.1',
                                                          'count': '5'},
                                                'source': {'start': '10.0.0.1',
                                                           'step': '0.0.0.1',
                                                           'count': '5'}},
                                       'maintain-subscribers': 0,
                                       'mld': {'version': '3',
                                                'filter-mode': 'include',
                                                'iptv': '0',
                                                'group': {'start': 'FF02::1',
                                                          'step': '::1',
                                                          'count': '5'},
                                                'source': {'start': '1000::1',
                                                           'step': '::1',
                                                           'count': '5'}},
                                       'option20': 1,
                                       'option6': [6, 67],
                                       'option82': {'circuit-id': 'agent1-aci',
                                                    'circuit-id-repeat': 1,
                                                    'circuit-id-start': 100,
                                                    'circuit-id-step': 1,
                                                    'remote-id': 'agent1-ari',
                                                    'remote-id-repeat': 1,
                                                    'remote-id-start': 100,
                                                    'remote-id-step': 1},
                                       'outstanding': 1000,
                                       'ri': 'default',
                                       # 'svlan': {'length': 1000,
                                       #           'repeat': 16,
                                       #           'start': 1,
                                       #           'step': 1},
                                       'tag': 'dhcpscaling1',
                                       'softgre': {'source': '1.1.1.1',
                                                   'destination': '2.2.2.2',
                                                   'gateway': '1.1.1.2',
                                                   'count': '2'},
                                       # 'vlan': {'length': 16,
                                       #          'repeat': 1,
                                       #          'start': 1,
                                       #          'step': 1},
                                       'vlan-encap': 'none'}]}}
        device = DHCPSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='dhcp', tag='dhcpscaling1')
        self.assertIsInstance(device, DHCPSubscribers)
        device.rt_dhcpv6_handle = 'testdhcp'
        self.assertEqual(device.rt_dhcpv6_handle, 'testdhcp')
        device.rt_dhcpv4_handle = 'testdhcp4'
        self.assertEqual(device.rt_dhcpv4_handle, 'testdhcp4')
        self.assertEqual(device.has_option82, True)
        print(device)
        self.assertIsInstance(device.option82_aci, tuple)
        self.assertIsInstance(device.option82_ari, tuple)
        device.clr = '300'
        self.assertEqual(device.clr, '300')
        device.outstanding = '300'
        self.assertEqual(device.outstanding, '300')
        device.csr = '300'
        self.assertEqual(device.csr, '300')
        device.rt_device_group_handle = 'group'
        self.assertEqual(device.rt_device_group_handle, 'group')
        device.rt_ethernet_handle = 'ethernet'
        self.assertEqual(device.rt_ethernet_handle, 'ethernet')
        self.assertEqual(device.vlan_encap, 'none')
        self.assertIsInstance(device.has_option18, bool)
        self.assertIsInstance(device.has_option37, bool)
        self.assertIsInstance(device.device_id, str)
        self.assertIsInstance(device.device_name, str)
        self.assertIsInstance(device.interface_id, str)
        self.assertIsInstance(device.tag, str)
        self.assertIsInstance(device.subscribers_type, str)
        self.assertIsInstance(device.count, int)
        self.assertIsInstance(device.protocol, str)
        self.assertIsInstance(device.family, str)
        self.assertIsInstance(device.router_port, str)
        self.assertIsInstance(device.rt_device_id, str)
        self.assertIsInstance(device.rt_port, str)
        self.assertIsInstance(device.ri, str)
        self.assertIsInstance(device.on_ae, bool)
        self.assertIsInstance(device.is_ae_active, int)
        self.assertIsInstance(device.ae_bundle, str)
        self.assertIsInstance(device.dhcpv6_ia_type, str)
        self.assertIsInstance(device.dhcpv6_iana_count, str)
        self.assertIsInstance(device.dhcpv6_iapd_count, str)
        rinterface.interface_config['subscribers']['dhcp'][0]['option82'] = 'test'
        DHCPSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='dhcp', tag='dhcpscaling1')
        rinterface.interface_config['subscribers']['dhcp'][0].pop('option82')
        DHCPSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='dhcp', tag='dhcpscaling1')

    def test_class_pppoesubscriber(self):
        rinterface.interface_config = \
            {'ae': {'active': True, 'bundle': 'ae0', 'enable': 0},
             'description': 'access interface  1',
             'subscribers': {'pppoe': [{'circuit-id': 'pppoe-aci',
                                        'circuit-id-length': 2,
                                        'circuit-id-repeat': 1,
                                        'circuit-id-start': 100,
                                        'circuit-id-step': 1,
                                        'clr': 200,
                                        'count': 16000,
                                        'csr': 200,
                                        'dhcpv6-ia-type': 'iapd',
                                        'family': 'dual',
                                        'igmp': False,
                                        'maintain-subscribers': 0,
                                        'mld': False,
                                        'option6': [6, 67],
                                        'ancp':{'count': '2',
                                                'vlan': {'start':'1'},
                                                'svlan': {'start':'1'}
                                                },
                                        'outstanding': 1000,
                                        'remote-id': 'pppoe-ari',
                                        'remote-id-length': 2,
                                        'remote-id-repeat': 1,
                                        'remote-id-start': 100,
                                        'remote-id-step': 1,
                                        'ri': 'default',
                                        'svlan': {'repeat': 1, 'start': 1, 'step': 1},
                                        'tag': 'pppoescaling2',
                                        'vlan': {'repeat': 1, 'start': 1, 'step': 1},
                                        'vlan-encap': 'dsvlan'}]}}
        device = PPPoESubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='pppoe', tag='pppoescaling2')
        self.assertIsInstance(device, PPPoESubscribers)
        device.rt_pppox_handle = 'test'
        self.assertEqual(device.rt_pppox_handle, 'test')
        device.rt_dhcpv6_handle = 'testdhcp'
        self.assertEqual(device.rt_dhcpv6_handle, 'testdhcp')
        self.assertEqual(device.username, 'DEFAULTUSER')
        self.assertEqual(device.password, 'joshua')
        self.assertEqual(device.domain, '')
        self.assertEqual(device.keep_alive, 120)
        self.assertEqual(device.termination, 'local')
        self.assertEqual(device.auth_method, 'pap_or_chap')
        self.assertIsInstance(device.vlan_range, tuple)
        self.assertIsInstance(device.svlan_range, tuple)
        print(device)
        try:
            device.start()
            device.stop()
            device.restart_down()
            device.abort()
        except:
            self.assertRaises(Exception)

    @patch('jnpr.toby.bbe.bbevar.subscribers.Subscribers.__init__')
    def test_class_staticsubscriber(self, patch_subscriber):
        patch_subscriber.return_value = None
        rinterface.interface_config = \
            {'subscribers':{'static':[{'tag': 'static1', 'mac-resolve': True, 'gateway-mac':'01:22:33:22:44:55',
                                      'ip':'10.0.0.1', 'ip-step':'0.0.0.1', 'ip-gateway':'10.0.0.255',
                                      'ipv6':'1000::/64', 'ipv6-step':'::1', 'ipv6-gateway':'1000::1'}]}
            }
        device = StaticSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='static', tag='static1')
        self.assertIsInstance(device, StaticSubscribers)

    #@patch('jnpr.toby.bbe.bbevar.subscribers.Subscribers.__init__')
    def test_class_l2bsasubscriber(self):
        #patch_subscriber.return_value = None
        rinterface.interface_config = \
            {'subscribers':{'l2bsa':[{'tag': 'l2bsa1',
                                      'mac-resolve': True,
                                      'gateway-mac':'01:22:33:22:44:55',
                                      'ip':'10.0.0.1',
                                      'ip-step':'0.0.0.1',
                                      'ip-gateway':'10.0.0.255',
                                      'ipv6':'1000::/64',
                                      'ipv6-step':'::1',
                                      'ipv6-gateway':'1000::1',
                                      'circuit-id': 'pppoe-aci',
                                      'circuit-id-length': 2,
                                      'circuit-id-repeat': 1,
                                      'circuit-id-start': 100,
                                      'circuit-id-step': 1,
                                      'remote-id': 'pppoe-ari',
                                      'remote-id-length': 2,
                                      'remote-id-repeat': 1,
                                      'remote-id-start': 100,
                                      'remote-id-step': 1,
                                      'vlan': '1',
                                      'svlan': '1',
                                      'vlan-encap': 'svlan',
                                      'option20': False,
                                      'option18': {'interface-id': 'testid',
                                                   'interface-id-start': '1',
                                                   'interface-id-step': '1',
                                                   'interface-id-repeat': '2',
                                                   'interface-id-length': '10',
                                                   },
                                      'option37': {'remote-id': 'testid',
                                                   'remote-id-start': '1',
                                                   'remote-id-step': '1',
                                                   'remote-id-repeat': '2',
                                                   'remote-id-length': '10',
                                                   },
                                      'option38': {'subscriber-id':'test'},
                                      }]}
            }
        device = L2BSASubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='l2bsa', tag='l2bsa1')
        self.assertIsInstance(device, L2BSASubscribers)
        self.assertIsInstance(device.option18, tuple)
        self.assertIsInstance(device.option37, tuple)
        self.assertIsInstance(device.option38, tuple)

   # @patch('jnpr.toby.bbe.bbevar.subscribers.Subscribers.__init__')
    def test_class_l2tpsubscriber(self):
        #patch_subscriber.return_value = None
        rinterface.interface_config = \
            {'subscribers':{'l2tp':[{'tag': 'l2tp1',
                                     'num-of-lac' : '10',
                                     'num-tunnels-per-lac': '20',
                                     'sessions-per-tunnel': '4',
                                     'tunnel-vlan-id': '1',
                                     'tunnel-vlan-step': '1',
                                     'tunnel-auth-enable': '1',
                                     'tunnel-secret': 'sec',
                                     'tunnel-destination-ip': '200.0.0.2',
                                     'tunnel-source-ip': '100.0.0.1',
                                     'tunnel-source-gateway': '100.0.0.2',
                                     'tunnel-prefix-length': '24',
                                     'tunnel-source-step': '1',
                                     'tunnel-destination-step': '1',
                                     'tunnel-hello-req': '3',
                                     'tunnel-hello-interval': '5',
                                     'lac-hostname': 'testlac',
                                     'option18': True,
                                     'option37': True,
                                     'option38': True
                                      }]}
            }
        device = L2TPSubscribers(rinterface=rinterface, rtinterface=rtinterface, protocol='l2tp', tag='l2tp1')
        self.assertIsInstance(device, L2TPSubscribers)

        self.assertEqual(device.tunnel_hello_req, '3')
        self.assertEqual(device.tunnel_hello_interval, '5')
        self.assertEqual(device.lac_hostname, 'testlac')
        self.assertEqual(device.num_of_lac, '10')
        self.assertEqual(device.tunnels_per_lac, '20')
        self.assertEqual(device.sessions_per_tunnel, '4')
        self.assertEqual(device.tunnel_vlan_id, '1')
        self.assertEqual(device.tunnel_vlan_step, '1')
        self.assertEqual(device.tunnel_auth_enable, '1')
        self.assertEqual(device.tunnel_secret, 'sec')
        self.assertEqual(device.tunnel_destination_ip, '200.0.0.2')
        self.assertEqual(device.tunnel_source_ip, '100.0.0.1')
        self.assertEqual(device.tunnel_source_gateway, '100.0.0.2')
        self.assertEqual(device.tunnel_prefix_length, '24')
        self.assertEqual(device.tunnel_source_step, '1')
        self.assertEqual(device.tunnel_destination_step, '1')
        device.rt_lac_handle = 'test'
        self.assertEqual(device.rt_lac_handle, 'test')

if __name__ == '__main__':
    unittest.main()

