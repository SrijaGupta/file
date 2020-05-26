#!/usr/local/bin/python3

from mock import patch
from mock import MagicMock
from mock import Mock
import unittest
import unittest2 as unittest

from jnpr.toby.utils import iputils


class TestIputils(unittest.TestCase):
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    mocked_t = MagicMock()

    def test_ip_get_version(self):
        self.assertEqual(iputils.ip_get_version('1.1.1.1'), 4)

    def test_ip_get_version_none_param(self):

        with self.assertRaises(Exception) as context:
            iputils.ip_get_version(None)
        self.assertTrue('Missing mandatory argument, ip_addr' in str(context.exception))
        # self.assertEqual(iputils.ip_get_version(None), None)

    def test_is_ip(self):
        self.assertEqual(iputils.is_ip('1.1.1.1'), True)

    # @patch(iputils.ipaddress.ip_address)
    #     test_patch.return_value = False
    # def return_false(self, ipaddress):
    #     return False

    @patch('jnpr.toby.utils.iputils.ipaddress.ip_address')
    def test_is_ip_partial_false(self, test_patch):
    # def test_is_ip_partial_false(self):
        test_patch.return_value = False
        self.assertEqual(iputils.is_ip('1.1.1.1'), None)

    def test_is_ip_else_case(self):
        self.assertEqual(iputils.is_ip('1.1.1'), False)

    def test_is_ip_ipv4(self):
        self.assertEqual(iputils.is_ip_ipv4('1.1.1.1'), True)

    def test_is_ip_ipv6(self):
        self.assertEqual(iputils.is_ip_ipv6('2000::2'), True)

    def test_is_ip_in_subnet(self):
        self.assertEqual(iputils.is_ip_in_subnet('1.1.1.1', '1.1.1.0/24'), True)

    def test_cmp_ip(self):
        self.assertEqual(iputils.cmp_ip('1.1.1.1', '1.1.1.1'), True)

    def test_get_mask(self):
        self.assertEqual(iputils.get_mask('1.1.1.1/24'), '24')

    def test_get_network_mask(self):
        self.assertEqual(iputils.get_network_mask('1.1.1.1'), '255.255.255.255')

    def test_get_network_mask_invalid_ip(self):
        self.assertEqual(iputils.get_network_mask('Non-ip'), False)

    def test_get_network_address(self):
        self.assertEqual(iputils.get_network_address('1.1.1.1'), '1.1.1.1')
        self.assertEqual(iputils.get_network_address('1.1.1.1/16'), '1.1.0.0')
        self.assertEqual(iputils.get_network_address('1.1.1.1/16', with_prefix=True), '1.1.0.0/16')
        self.assertEqual(iputils.get_network_address('1.1.1.1/16', with_netmask=True), '1.1.0.0/255.255.0.0')
        self.assertEqual(iputils.get_network_address('1.1.1.1/16', with_prefix=True, with_netmask=True), '1.1.0.0/16')

        self.assertEqual(iputils.get_network_address('2000:1:1:1::1/64'), '2000:1:1:1::')
        self.assertEqual(iputils.get_network_address('2000:1:1:1::1/64', with_prefix=True), '2000:1:1:1::/64')
        self.assertEqual(iputils.get_network_address('2000:1:1:1::1/64', with_netmask=True), '2000:1:1:1::/ffff:ffff:ffff:ffff::')
        self.assertEqual(iputils.get_network_address('2000:1:1:1::1/64', with_prefix=True, with_netmask=True), '2000:1:1:1::/64')


    def test_get_network_address_invalid_ip(self):
        self.assertEqual(iputils.get_network_address('Non-ip'), False)

    def test_normalize_ipv6(self):
        self.assertEqual(iputils.normalize_ipv6('2000::2/64'),
                         '2000:0000:0000:0000:0000:0000:0000:0002/64')

    def test_normalize_ipv6_none_mask(self):
        self.assertEqual(iputils.normalize_ipv6('2000::2'),
                         '2000:0000:0000:0000:0000:0000:0000:0002')

    def test_normalize_ipv6_none_mask(self):
        self.assertEqual(iputils.normalize_ipv6('2000::2', compress_zero=True),
                         '2000:0:0:0:0:0:0:2')

    def test_strip_mask(self):
        self.assertEqual(iputils.strip_mask(['2000::2/64', '1000::4/64' ]),
                         ['2000::2', '1000::4'])

    def test_incr_ip(self):
        self.assertEqual(iputils.incr_ip('1.1.1.1'), '1.1.1.2')

    def test_incr_ip_input_ipv6(self):
        self.assertEqual(iputils.incr_ip('2000::BEC'), '2000::bed')

    def test_incr_ip_with_net_mask(self):
        self.assertEqual(iputils.incr_ip('1.1.1.1/24'), '1.1.1.2/24')

    def test_incr_ip_subnet(self):
        self.assertEqual(iputils.incr_ip_subnet('1.1.1.1/24'), '1.1.2.1/24')
        self.assertEqual(iputils.incr_ip_subnet('1.1.1.1'), '1.1.1.2/32')

    def test_get_network_ip_range(self):
        self.assertEqual(iputils.get_network_ip_range('10.10.10.0/24'), '10.10.10.1-10.10.10.254')
        self.assertEqual(iputils.get_network_ip_range('10.10.10.1/32'), '10.10.10.1-10.10.10.1')

    @patch('logging.debug', return_value=None)
    @patch('logging.warning', return_value=None)
    @patch('logging.error', return_value=None)
    @patch('logging.info', return_value=None)
    @patch('time.sleep', return_value=None)
    def test_ping(self, sleep_mock, info_mock, error_mock, warning_mock, debug_mock):
        ###################################################################
        # Test case 1: Ping ipv4 successful
        output = '''
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.036 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.040 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.040 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.037 ms
64 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.043 ms

--- 127.0.0.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3997ms
rtt min/avg/max/mdev = 0.036/0.039/0.043/0.004 ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='127.0.0.1')
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 2: Ping ipv6 successful
        output = '''
PING ::1(::1) 56 data bytes
64 bytes from ::1: icmp_seq=1 ttl=64 time=0.093 ms
64 bytes from ::1: icmp_seq=2 ttl=64 time=0.057 ms
64 bytes from ::1: icmp_seq=3 ttl=64 time=0.128 ms
64 bytes from ::1: icmp_seq=4 ttl=64 time=0.062 ms
64 bytes from ::1: icmp_seq=5 ttl=64 time=0.074 ms

--- ::1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4027ms
rtt min/avg/max/mdev = 0.057/0.082/0.128/0.028 ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='::1', ipv6=True)
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 3: Ping ipv4 unsuccessful
        output = '''
PING 5.6.4.4 (5.6.4.4) 56(84) bytes of data.

--- 5.6.4.4 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4033ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='5.6.4.4', timeout=1)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 4: Ping ipv6 unsuccessful
        output = '''
connect: Network is unreachable
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='AB::3', ipv6=True, timeout=11)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 5: Negative test - Ping ipv4 unsuccessful
        output = '''
PING 5.6.4.4 (5.6.4.4) 56(84) bytes of data.

--- 5.6.4.4 ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4033ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='5.6.4.4', negative=True, timeout=11)
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 6: Negative test - Ping ipv6 unsuccessful
        output = '''
connect: Network is unreachable
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='AB::3', ipv6=True, negative=True, timeout=11)
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 7: Negative test - Ping ipv4 successful
        output = '''
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.036 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.040 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.040 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.037 ms
64 bytes from 127.0.0.1: icmp_seq=5 ttl=64 time=0.043 ms

--- 127.0.0.1 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 3997ms
rtt min/avg/max/mdev = 0.036/0.039/0.043/0.004 ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'

                test = iputils.ping(host='127.0.0.1', negative=True)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 8: Ping ipv4 successful with count < 4
        output = '''
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.037 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.039 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.032 ms

--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.032/0.036/0.039/0.003 ms

        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='127.0.0.1', count=3)
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 9: Ping on windows
        output = '\r\nPinging 127.0.0.1 with 32 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=32 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=32 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=32 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 3, Received = 3, Lost = 0 (0% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=3)
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 10: Ping on windows with length option
        output = '\r\nPinging 127.0.0.1 with 10 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 3, Received = 3, Lost = 0 (0% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = ''
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=3, option='-l 10')
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 11: Ping ipv4 successful with interval option
        output = '''
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.150 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.044 ms

--- 127.0.0.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 5000ms
rtt min/avg/max/mdev = 0.040/0.050/0.061/0.012 ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='127.0.0.1', count=4,
                            option='-i 5', timeout=11)
                self.assertTrue(test, "Return should be True")

        ###################################################################
        # Test case 12: Ping unknown host
        output = '''
ping: unknown host abc
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='abc', count=1, timeout=11)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 13: Ping unsuccessful with fail_ok = warning
        output = '''
PING 5.6.4.4 (5.6.4.4) 56(84) bytes of data.

--- 5.6.4.4 ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 5028ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='5.6.4.4', fail_ok='warning', timeout=11)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 14: Ping unsuccessful with fail_ok = info
        output = '''
PING 5.6.4.4 (5.6.4.4) 56(84) bytes of data.

--- 5.6.4.4 ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 5028ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='5.6.4.4', fail_ok='info', timeout=11)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 15: Ping with packet loss
        output = '\r\nPinging 127.0.0.1 with 10 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 5, Received = 3, Lost = 0 (40% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = ''
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=5, option='-l 10',
                            acceptable_packet_loss=10)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 16: Ping with packet loss, negative and fail_ok = warning
        output = '\r\nPinging 127.0.0.1 with 10 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 5, Received = 3, Lost = 0 (40% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = ''
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=5, option='-l 10',
                            acceptable_packet_loss=10, negative=True,
                            fail_ok='warning')
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 17: Ping with packet loss, negative and fail_ok = info
        output = '\r\nPinging 127.0.0.1 with 10 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 5, Received = 3, Lost = 0 (40% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = ''
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=5, option='-l 10',
                            acceptable_packet_loss=10,
                            negative=True, fail_ok='info')
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 18: Ping with packet loss, negative and  fail_ok = info, timeout = 1
        output = '\r\nPinging 127.0.0.1 with 10 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 5, Received = 3, Lost = 0 (40% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = ''
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=5, option='-l 10',
                            acceptable_packet_loss=10, negative=True,
                            fail_ok='info', timeout=11)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 19: Ping with packet loss, negative and fail_ok = warn, timeout = 1")
        output = '\r\nPinging 127.0.0.1 with 10 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 5, Received = 3, Lost = 0 (40% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = ''
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=5, option='-l 10',
                            acceptable_packet_loss=10, negative=True,
                            fail_ok='warn', timeout=11)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 20: Ping with packet loss, negative and fail_ok = err, timeout = 1
        output = '\r\nPinging 127.0.0.1 with 10 bytes of data:\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n' +\
            'Reply from 127.0.0.1: bytes=10 time<1ms TTL=128\r\n\r\n' +\
            'Ping statistics for 127.0.0.1:\r\n' +\
            '    Packets: Sent = 5, Received = 3, Lost = 0 (40% loss),\r\n' +\
            'Approximate round trip times in milli-seconds:\r\n' +\
            '    Minimum = 0ms, Maximum = 0ms, Average = 0ms\r\n'
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = ''
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'windows'
                test = iputils.ping(host='127.0.0.1', count=5, option='-l 10',
                            acceptable_packet_loss=10, negative=True,
                            fail_ok='error', timeout=11)
                self.assertFalse(test, "Return should be False")

        ###################################################################
        # Test case 21: Ping ipv4 with timeout < 0
        output = '''
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.033 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.045 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.043 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.041 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2998ms
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                error = None
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                expected = None
                test = iputils.ping(host='127.0.0.1', timeout=-1)
                self.assertEqual(test, expected, "Return should be None")

        ###################################################################
        # Test case 22: Ping ipv4 with error
        output = '''
        '''
        with patch('platform.system') as system_mock:
            with patch('subprocess.Popen') as mock_subproc_popen:
                output = output.encode('utf-8')
                res = "unknown host"
                error = res.encode('utf-8')
                process_mock = Mock()
                attrs = {'communicate.return_value': (output, error)}
                process_mock.configure_mock(**attrs)
                mock_subproc_popen.return_value = process_mock
                system_mock.return_value = 'linux'
                test = iputils.ping(host='127.0.0.1', timeout=11)
                self.assertFalse(test, "Return should be False")

    def test_narrow_ip(self):
        without_prefix_test_list = (
            # whether_with_prefix, origin_str, expect_result
            (False, "192.168.080.001/24", "192.168.80.1"),
            (False, "192.168.000.01/16", "192.168.0.1"),
            (False, "2000::0100/64", "2000::100"),
            (False, "2000:0:0:0:0:0000:00:0100/64", "2000::100"),
            (False, "2000:0::0100/64", "2000::100"),
            (True, "192.168.1.001/32", "192.168.1.1/32"),
            (True, "2000:0:0:0000::0100/64", "2000::100/64"),
        )

        for (with_prefix, ipaddr, expect_result) in without_prefix_test_list:
            iputils.narrow_ip(ipaddr, with_prefix=with_prefix) == expect_result

    def test_get_broadcast_ip(self):
        test_list = (
            ("2000:121:11:11::3/96", "2000:121:11:11::ffff:ffff"),
            ("192.168.1.0/24", "192.168.1.255"),
        )

        for (ipaddr, expect_result) in test_list:
            iputils.get_broadcast_ip(ipaddr) == expect_result

if __name__ == '__main__':
    unittest.main()
