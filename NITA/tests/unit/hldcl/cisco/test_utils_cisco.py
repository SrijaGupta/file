import os
import unittest
import logging
from mock import MagicMock
from mock import patch
import builtins
from time import sleep
from jnpr.toby.hldcl.cisco.cisco import IOS
from jnpr.toby.hldcl.cisco.cisco import Cisco
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.cisco.utils import ping, extended_ping, traceroute, get_image, check_interface_status


class TestCiscoUtilsModule(unittest.TestCase):

    def test_ping(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Invalid host. Ping unsuccessfully")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, ping(device))
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: host Unrecognized. ping unsuccessfully")
        device.cli = MagicMock(return_value=Response(response='Unrecognized'))
        device.model = 'erx'
        result = ping(device, host='1.1.1.1', ipv6=True,
                      source='2.2.2.2', count=10, option='abc')
        self.assertEqual(result, {'reachable': False},
                         "Result should be {'reachable': False}")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 3: ping unsuccessfully")
        device.model = ''
        device.cli = MagicMock(return_value=Response(response=""""1 172.31.20.2 16 msec 16 msec 16 msec
        2 172.20.10.2 28 msec 28 msec 32 msec
        3 2.1.1.1 32 msec 28 msec *"""))
        result = ping(device, host='1.1.1.1', source='2.2.2.2', timeout=10)
        self.assertEqual(result, {'reachable': False},
                         "Result should be {'reachable': False}")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 4: ping successfully")
        device.model = ''
        device.cli = MagicMock(return_value=Response(response=""""1 172.31.20.2 16 msec 16 msec 16 msec
        2 172.20.10.2 28 msec 28 msec 32 msec
        3 1.1.1.1 32 msec 28 msec *
        Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms"""))
        expected_result = {
            'packets_transmitted': 5, 'reachable': True, 'packets_received': 5,
            'round_trip': {'min': '1', 'avg': '2', 'max': '4'},
            'packet_loss': 0}
        result = ping(device, host='1.1.1.1', timeout=10)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 5: ping unsuccessfully")
        device.model = ''
        device.cli = MagicMock(return_value=Response(response=""""1 172.31.20.2 16 msec 16 msec 16 msec
        2 172.20.10.2 28 msec 28 msec 32 msec
        3 1.1.1.1 32 msec 28 msec *
        Success rate is 20 percent (1/5), round-trip min/avg/max = 1/2/4 ms"""))
        expected_result = {
            'reachable': False, 'packets_received': 1, 'packet_loss': 80,
            'packets_transmitted': 5,
            'round_trip': {'max': '4', 'min': '1', 'avg': '2'}}
        result = ping(device, host='1.1.1.1', timeout=10)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")

    def test_extended_ping(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Invalid host. Ping unsuccessfully")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, extended_ping(device))
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: host Unrecognized. ping unsuccessfully")
        device.cli = MagicMock(
            return_value=Response(response='Bad IP address'))
        result = extended_ping(device, host='abc', ipv6=True,
                               source='2.2.2.2', count=10)
        self.assertEqual(result, {'reachable': False},
                         "Result should be {'reachable': False}")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 3: ping successfully")
        device.cli = MagicMock(
            return_value=Response(response='Protocol [ip]:'))
        device.execute = MagicMock(
            side_effect=['Target IP address:',
                         'Repeat count [5]:', 'Datagram size [100]:', 'Timeout in seconds [2]:',
                         'Extended commands [n]:', 'Source address or interface:',
                         'Type of service [0]:', 'Set DF bit in IP header? [no]:',
                         'Validate reply data? [no]:', 'Data pattern [0xABCD]:',
                         'Loose, Strict, Record, Timestamp, Verbose[none]:', 'Sweep range of sizes [n]:',
                         'Sweep min size [36]', 'Sweep max size [18024]:', 'Sweep interval [1]:',
                         """Type escape sequence to abort.
                            Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
                            !!!!!
                            Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms"""])
        result = extended_ping(
            device, host='1.1.1.1', tos=2, source='2.2.2.2',
            count=5, timeout=20, pktsize=1, protocol='ip',
            acceptable_packet_loss=0, df=False, validate_reply=False,
            data_pattern=1000, misc=10, sweep=True,
            sweep_min_size=1, sweep_max_size=1000, sweep_interval=1)
        expected_result = {'round_trip': {'min': '1', 'avg': '2', 'max': '4'},
                           'packets_transmitted': 5, 'packet_loss': 0,
                           'reachable': True, 'packets_received': 5}
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 4: ping unsuccessfully")
        device.cli = MagicMock(
            return_value=Response(response='Protocol [ip]:'))
        device.execute = MagicMock(
            side_effect=['Target IP address:',
                         'Repeat count [5]:', 'Datagram size [100]:', 'Timeout in seconds [2]:',
                         'Extended commands [n]:', 'Source address or interface:',
                         'Type of service [0]:', 'Set DF bit in IP header? [no]:',
                         'Validate reply data? [no]:', 'Data pattern [0xABCD]:',
                         'Loose, Strict, Record, Timestamp, Verbose[none]:', 'Sweep range of sizes [n]:',
                         'Sweep min size [36]', 'Sweep max size [18024]:', 'Sweep interval [1]:',
                         """Type escape sequence to abort.
                            Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
                            !!!!!
                            Success rate is 20 percent (5/1), round-trip min/avg/max = 1/2/4 ms"""])
        result = extended_ping(
            device, host='1.1.1.1', acceptable_packet_loss=10,
            df=False, validate_reply=False,
            data_pattern=1000, misc=10, sweep=True)
        expected_result = {'packets_transmitted': 1, 'packet_loss': 80,
                           'reachable': False, 'packets_received': 5,
                           'round_trip': {'min': '1', 'avg': '2', 'max': '4'}}
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 5: ping unsuccessfully")
        device.cli = MagicMock(
            return_value=Response(response='Protocol [ip]:'))
        device.execute = MagicMock(
            side_effect=['Target IP address:',
                         'Repeat count [5]:', 'Datagram size [100]:', 'Timeout in seconds [2]:',
                         'Extended commands [n]:', 'Source address or interface:',
                         'Type of service [0]:', 'Set DF bit in IP header? [no]:',
                         'Validate reply data? [no]:', 'Data pattern [0xABCD]:',
                         'Loose, Strict, Record, Timestamp, Verbose[none]:', 'Sweep range of sizes [n]:',
                         'Sweep min size [36]', 'Sweep max size [18024]:', 'Sweep interval [1]:',
                         """Type escape sequence to abort.
                            Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
                            !!!!!
                            Success rate is 20 percent (5/1), round-trip min/avg/max = 1/2/4 ms
                            """])
        result = extended_ping(device, host='1.1.1.1',
                               acceptable_packet_loss=10)
        expected_result = {'packets_transmitted': 1, 'packet_loss': 80,
                           'reachable': False, 'packets_received': 5,
                           'round_trip': {'min': '1', 'avg': '2', 'max': '4'}}
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 6: ping unsuccessfully")
        device.cli = MagicMock(
            return_value=Response(response='Protocol [ip]:'))
        device.execute = MagicMock(
            side_effect=['Target IP address:',
                         'Repeat count [5]:', 'Datagram size [100]:', 'Timeout in seconds [2]:',
                         'Extended commands [n]:', 'Sweep range of sizes [no]:',
                         'Type of service [0]:', 'Set DF bit in IP header? [no]:',
                         'Validate reply data? [no]:', 'Data pattern [0xABCD]:',
                         'Loose, Strict, Record, Timestamp, Verbose[none]:',
                         'abc [36]', 'abc [18024]:', 'abc [1]:',
                         """Type escape sequence to abort.
                            Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
                            !!!!!
                            Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms"""])
        result = extended_ping(
            device, host='1.1.1.1', tos=2, source='2.2.2.2',
            count=5, timeout=20, pktsize=1, protocol='ip',
            acceptable_packet_loss=0, df=False, validate_reply=False,
            data_pattern=1000, misc=10, sweep=True,
            sweep_min_size=1, sweep_max_size=1000, sweep_interval=1)
        expected_result = {'reachable': False}
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 7: ping unsuccessfully")
        device.cli = MagicMock(
            return_value=Response(response='Protocol [ip]:'))
        device.execute = MagicMock(
            side_effect=['Target IP address:',
                         'Repeat count [5]:', 'Datagram size [100]:', 'Timeout in seconds [2]:',
                         'Extended commands [n]:', 'Source address or interface:',
                         'Type of service [0]:', 'Set DF bit in IP header? [no]:',
                         'Validate reply data? [no]:', 'Data pattern [0xABCD]:',
                         'Loose, Strict, Record, Timestamp, Verbose[none]:', 'abc [n]:',
                         'Sweep min size [36]', 'Sweep max size [18024]:', 'Sweep interval [1]:',
                         """Type escape sequence to abort.
                            Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
                            !!!!!
                            Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/4 ms"""])
        result = extended_ping(
            device, host='1.1.1.1', tos=2, source='2.2.2.2',
            count=5, timeout=20, pktsize=1, protocol='ip',
            acceptable_packet_loss=0, df=False, validate_reply=False,
            data_pattern=1000, misc=10, sweep=True,
            sweep_min_size=1, sweep_max_size=1000, sweep_interval=1)
        expected_result = {'reachable': False}
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")

    def test_traceroute(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Invalid host. traceroute unsuccessfully")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, traceroute(device))
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: traceroute successfully")
        device.cli = MagicMock(return_value=Response(response=""""Type escape sequence to abort.
        Tracing the route to alex-bsd.juniper.net (172.17.22.87)
          1 172.17.41.254 0 msec 0 msec 0 msec
          2 pound-stonewall-atm.juniper.net (172.17.254.62) 0 msec 0 msec 0 msec
          3 peso-pound-oc12.juniper.net (172.17.254.18) 0 msec 0 msec 0 msec
          4 yen-peso-oc12.juniper.net (172.17.254.42) 0 msec 0 msec 0 msec
          5 alex-bsd.juniper.net (172.17.22.87) 0 msec 0 msec 0 msec"""))
        expected_result = {'hop': ['172.17.41.254', '172.17.254.62',
                                   '172.17.254.18', '172.17.254.42',
                                   '172.17.22.87'], 'reachable': True}
        result = traceroute(
            device, host='172.17.254.62', source='1.1.1.1', timeout=300,
            options='abc', ttl=10, noresolve=True)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 3: traceroute successfully")
        device.cli = MagicMock(return_value=Response(response=""""Type escape sequence to abort.
        Tracing the route to 172.17.22.87
          1 172.17.41.254 0 msec 0 msec 0 msec
          2 172.17.254.62 0 msec 0 msec 0 msec
          3 172.17.254.18 0 msec 0 msec 0 msec
          4 172.17.254.42 0 msec 0 msec 0 msec
          5 172.17.22.87 0 msec 0 msec 0 msec"""))
        expected_result = {'hop': ['172.17.41.254', '172.17.254.62',
                                   '172.17.254.18', '172.17.254.42',
                                   '172.17.22.87'], 'reachable': True}
        result = traceroute(device, host='172.17.254.62')
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 4: traceroute unsuccessfully")
        device.cli = MagicMock(return_value=Response(response=""""Type escape sequence to abort.
        Tracing the route to 172.17.22.87
          1 172.17.41.254 0 msec 0 msec 0 msec
          2 172.17.254.62 0 msec 0 msec 0 msec
          3 ***
          4 ***
          """))
        expected_result = {'reachable': False,
                           'hop': ['172.17.41.254', '172.17.254.62']}
        result = traceroute(device, host='172.17.254.62')
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")

    def test_get_image(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: get_image successfully")
        device.cli = MagicMock(return_value=Response(response=""""ROM: ROMMON Emulation Microcode
        ROM: 3700 Software (C3745-ADVENTERPRISEK9_SNA-M), Version 12.4(25d), RELEASE SOFTWARE (fc1)
        R1 uptime is 3 hours, 53 minutes
        System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
        System image file is "tftp://255.255.255.255/unknown"
        This product contains cryptographic features and is subject to United"""))
        expected_result = 'tftp://255.255.255.255/unknown'
        result = get_image(device)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: get_image unsuccessfully")
        device.cli = MagicMock(return_value=Response(response=""""ROM: ROMMON Emulation Microcode
        ROM: 3700 Software (C3745-ADVENTERPRISEK9_SNA-M),
        R1 uptime is 3 hours, 53 minutes
        System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
        System image file is ""
        This product contains cryptographic features and is subject to United"""))
        expected_result = ''
        result = get_image(device)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")

    def test_check_interface_status(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info(
            "Test case 1: Invalid interface, check_interface_status unsuccessfully")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, check_interface_status(device))
        logging.info("\tPassed")
        ###################################################################
        logging.info(
            "Test case 2: Invalid input detected, check_interface_status unsuccessfully")
        device.cli = MagicMock(return_value=Response(
            response=""""Invalid input detected"""))
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, check_interface_status(
                device, interface='fa0/1'))
        logging.info("\tPassed")
        ###################################################################
        logging.info(
            "Test case 3: interface up, check_interface_status successfully")
        device.cli = MagicMock(return_value=Response(response=""""FastEthernet0/1 is up, line protocol is up
          Hardware is Gt96k FE, address is c400.16dc.0001 (bia c400.16dc.0001)
          Internet address is 172.16.1.1/24
          MTU 1500 bytes, BW 10000 Kbit/sec, DLY 1000 usec,
             reliability 255/255, txload 1/255, rxload 1/255
        """))
        expected_result = {'fa0/1': {'oper-status': True}}
        result = check_interface_status(device, interface=['fa0/1'])
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info(
            "Test case 4: interface Down, check_interface_status successfully")
        device.cli = MagicMock(return_value=Response(response=""""FastEthernet0/1 is Down, line protocol is Down
          Hardware is Gt96k FE, address is c400.16dc.0001 (bia c400.16dc.0001)
          Internet address is 172.16.1.1/24
          MTU 1500 bytes, BW 10000 Kbit/sec, DLY 1000 usec,
             reliability 255/255, txload 1/255, rxload 1/255
        """))
        expected_result = {'fa0/1': {'oper-status': False}}
        result = check_interface_status(device, interface=['fa0/1'])
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info(
            "Test case 5: incorrect response, check_interface_status successfully")
        device.cli = MagicMock(return_value=Response(response=""""
          Hardware is Gt96k FE, address is c400.16dc.0001 (bia c400.16dc.0001)
          Internet address is 172.16.1.1/24
          MTU 1500 bytes, BW 10000 Kbit/sec, DLY 1000 usec,
             reliability 255/255, txload 1/255, rxload 1/255
        """))
        expected_result = {'fa0/1': {'oper-status': False}}
        result = check_interface_status(device, interface=['fa0/1'])
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")

    @patch('time.sleep')
    def test_check_ospf_neighbor(self, sleep_time):
        from jnpr.toby.hldcl.cisco.utils import check_ospf_neighbor
        device = MagicMock()
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Run with valid response and return True")
        res = '''
Neighbor ID         Pri   State        Dead Time     Address         Interface
10.199.199.137  1    FULL/DR       0:00:31    192.168.80.37      Ethernet0
172.16.48.1     1    FULL/DROTHER  0:00:33    172.16.48.1        Fddi0
172.16.48.200   1    WAIT/DROTHER  0:00:33    172.16.48.200      Fddi0
10.199.199.137  5    FULL/DR       0:00:33    172.16.48.189      Fddi0
        '''
        device.cli = MagicMock(side_effect=[Response(response="no response"),
                                            Response(response=res)])

        result = check_ospf_neighbor(
            device, ospfv3=False, address=['192.168.80.37', '172.16.48.1'],
            interface=['Ethernet0', 'Fddi0'],
            router_id=['10.199.199.137', '172.16.48.1'],
            state='Full', num=None, timeout=90, interval=10, options=" area 1")
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: Run with ospfv3 and not match state")
        device.cli = MagicMock(return_value=Response(response=res))
        result = check_ospf_neighbor(
            device, ospfv3=True, address='172.16.48.200',
            interface='Fddi0', router_id='172.16.48.200', state='Full',
            num=1, timeout=90, interval=10, options=None)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

    @patch('time.sleep')
    def test_check_bgp_peer(self, sleep_patch):
        from jnpr.toby.hldcl.cisco.utils import check_bgp_peer
        device = MagicMock()
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Run with wrong state of a peer")
        res = '''
BGP router identifier 172.16.1.1, local AS number 100
BGP table version is 199, main routing table version 199

Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down State/PfxRcd
10.100.1.1      4   200      26      22      199    0    0 00:14:23 23
10.100.1.2      4   300      21      51      199    0    0 00:13:40 active
10.100.1.3      4   300      21      51      199    0    0 00:13:40 33
        '''
        device.cli = MagicMock(side_effect=[Response(response="no response"),
                                            Response(response=res)])
        result = check_bgp_peer(
            device, peer=['10.100.1.1', '10.100.1.2'], state=None, timeout=10)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: Run with not match state")
        device.cli = MagicMock(side_effect=[Response(response="no response"),
                                            Response(response=res)])
        result = check_bgp_peer(
            device, peer=['10.100.1.1', '10.100.1.2'],
            state="active", timeout=10)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 3: Run with 1 peer check and return True")
        device.cli = MagicMock(return_value=Response(response=res))
        result = check_bgp_peer(
            device, peer='10.100.1.1', state=None, timeout=10)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 4: Run with BGP not running")
        device.cli = MagicMock(return_value=Response(
            response="BGP is not running on this device"))
        result = check_bgp_peer(
            device, peer='10.100.1.1', state=None, timeout=10)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

    @patch('time.sleep')
    def test_check_isis_neighbor(self, sleep_time):
        from jnpr.toby.hldcl.cisco.utils import check_isis_neighbor
        device = MagicMock()
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Run with valid response and return True")
        res = '''
System Id      Type Interface IP Address      State Holdtime Circuit Id
0000.0000.0002 L1   Et0/0     192.168.128.2   UP    21       R5.02
0000.0000.0003 L2   Et0/0     192.168.128.3   UP    28       R5.03
0000.0000.0004 L3   Et0/0     192.168.128.4   Down    28       R5.04
        '''
        device.cli = MagicMock(side_effect=[Response(response="no response"),
                                            Response(response=res)])

        result = check_isis_neighbor(
            device, system_id=['0000.0000.0002', '0000.0000.0003'],
            router_type=['L1', 'L2'],
            interface=['Et0/0', 'Et0/0'],
            ip_address=['192.168.128.2', '192.168.128.3'], state='Up',
            circuit_id=['R5.02', 'R5.03'], num=2, timeout=90,
            interval=10, options="detail")
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 2: Run with not match state")
        device.cli = MagicMock(return_value=Response(response=res))

        result = check_isis_neighbor(
            device, system_id='0000.0000.0004', router_type='L3',
            interface='Et0/0', ip_address='192.168.128.4', state='Up',
            circuit_id='R5.04', num=None, timeout=90,
            interval=10, options=None)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

    def test_get_loopback_adress(self):
        from jnpr.toby.hldcl.cisco.utils import get_loopback_adress
        device = MagicMock()
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Run with loop_ip")

        result = get_loopback_adress(
            device, loop_ip='127.0.0.1')
        self.assertEqual(result, '127.0.0.1', "Return is wrong as expected")
        logging.info("\tPassed")

        ###################################################################
        logging.info(
            "Test case 2: Run with get_interface_address return a list")
        device.get_interface_address = MagicMock(
            return_value=['1.2.3.4/32', 'abc123', '2.3.4.5/24'])
        result = get_loopback_adress(device, loop_ip='')
        expected = ['1.2.3.4', '2.3.4.5']
        self.assertEqual(result, expected, "Return is wrong as expected")
        logging.info("\tPassed")

        ###################################################################
        logging.info(
            "Test case 3: Run with get_interface_address return a string")
        device.get_interface_address = MagicMock(
            return_value='1.2.3.4/25')
        result = get_loopback_adress(device, loop_ip='')
        self.assertEqual(result, '1.2.3.4', "Return is wrong as expected")
        logging.info("\tPassed")

        ###################################################################
        logging.info(
            "Test case 4: Run with get_interface_address return invalid value")
        device.get_interface_address = MagicMock(
            return_value={'addr': '1.2.3.4/32'})
        result = get_loopback_adress(device, loop_ip='')
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name + ".log", level=logging.INFO)
    unittest.main()
