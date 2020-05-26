import unittest
from mock import patch, MagicMock
from jnpr.toby.hldcl.juniper.junos import Juniper
import logging
import os
from jnpr.toby.utils.response import Response
from lxml import etree
from jnpr.toby.firewall.Firewall import __check_value as check_value
from jnpr.toby.firewall.Firewall import __get_dst_addrss as get_dst_addrss
from jnpr.toby.firewall.Firewall import __cprod as cprod
from jnpr.toby.firewall.Firewall import __timeless as timeless


class TestFirewall(unittest.TestCase):
    def setUp(self):
        logging.info("\n##################################################\n")
        logging.info("Initializing mock device handle.............\n")
        self.jobject = MagicMock(spec=Juniper)
        self.jobject.handle = MagicMock()

    def tearDown(self):
        logging.info("Close mock device handle session ...........\n")
        self.jobject.handle.close()

    def test_check_args(self):
        from jnpr.toby.firewall.Firewall import check_args
        logging.info("-----------Test check_args: -----------")
        ######################################################################
        logging.info("Test case 1: Get args successful with correct arguments")
        kwargs = {'name': 'VOIP-COS', 'family': 'inet'}
        valid_keys = ['name', 'family']
        required_key = ['name']
        result = check_args(valid_keys, required_key, kwargs)
        self.assertEqual(result, kwargs, "Get args unsuccessful")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Get args unsuccessful with invalid key")
        kwargs = {'name': 'VOIP-COS', 'family': 'inet', 'abc': '111'}
        valid_keys = ['name', 'family']
        required_key = ['name']
        with self.assertRaises(Exception) as context:
            check_args(valid_keys, required_key, kwargs)
        self.assertTrue('is not valid' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Get args unsuccessful with invalid required_key")
        kwargs = {'name': 'VOIP-COS', 'family': 'inet'}
        valid_keys = ['name', 'family']
        required_key = ['name', 'term']
        with self.assertRaises(Exception) as context:
            check_args(valid_keys, required_key, kwargs)
        self.assertTrue('value is not' in str(context.exception))
        logging.info("\tPassed")

    def test_configure_firewall_filter(self):
        from jnpr.toby.firewall.Firewall import configure_firewall_filter
        logging.info("-----------Test configure_firewall_filter: -----------")
        ######################################################################
        logging.info("Test case 1: Test execute command fail when configuring "
                     "firewall filter")
        # For configure unsuccessfully with invalid input
        param = {'name': 'VOIP-COS1',
                 'family': 'inet',
                 'term': 'SIP',
                 'match': 'protocol udp',
                 'action': 'next term',
                 'physical_interface_filter': True,
                 'enhanced_mode': True,
                 'interface_specific': True,
                 'enhanced_mode_override': True,
                 'fast_lookup_filter': True,
                 'interface_shared': True,
                 'instance_shared': True
                 }

        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(configure_firewall_filter(self.jobject, **param),
                         "Return shoule be False")

        # For configure unsuccessfully with invalid input
        param = {'name': 'VOIP-COS1',
                 'action': ['next term'],
                 'term': 'SIP',
                 'physical_interface_filter': True,
                 'enhanced_mode': True,
                 'interface_specific': True,
                 'enhanced_mode_override': True,
                 'fast_lookup_filter': True,
                 'interface_shared': True,
                 'instance_shared': True
                 }

        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(configure_firewall_filter(self.jobject, **param),
                         "Return shoule be False")

        # For configure unsuccessfully with invalid input
        param = {'name': 'VOIP-COS1',
                 'match': 'protocol tcp',
                 'term': 'SIP',
                 'physical_interface_filter': True,
                 'enhanced_mode': True,
                 'interface_specific': True,
                 'enhanced_mode_override': True,
                 'fast_lookup_filter': True,
                 'interface_shared': True,
                 'instance_shared': True
                 }

        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(configure_firewall_filter(self.jobject, **param),
                         "Return shoule be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Test configure firewall filter fail "
                     "without match value and action value")
        # Configure unsuccessfully match value and action value is not defined
        param = {'name': 'VOIP-COS1'}
        result = configure_firewall_filter(self.jobject, **param)
        self.assertFalse(result, "match value and action value is not defined")

        # For configure successfully with commit
        logging.info("Test case 3: Test configure firewall filter successful")
        self.jobject.config = MagicMock(return_value=Response(response=''))
        param = {'name': 'VOIP-COS1',
                 'term': 'SIP',
                 'match': ['protocol udp'],
                 'action': 'next term',
                 'commit': True}
        # For configure successfully without commit
        self.assertTrue(configure_firewall_filter(self.jobject, **param),
                        "Return should be True")
        param = {'name': 'VOIP-COS1',
                 'term': 'SIP',
                 'match': 'protocol udp',
                 'action': ['next term']}
        self.assertTrue(configure_firewall_filter(self.jobject, **param))
        logging.info("\tPassed")

    def test_configure_firewall_psa(self):
        from jnpr.toby.firewall.Firewall import configure_firewall_psa
        logging.info("-----------Test configure_firewall_psa: -----------")
        logging.info("Test case 1: Configure FW psa successfully with commit")
        ######################################################################
        # Configure firewall psa successfully with commit
        param = {'name': 'psa-1Mbps-per-source-24-32-256-1',
                 'count': True, 'filter_specific': True,
                 'policer': '1Mbps-policer',
                 'source_prefix_length': '8',
                 'destination_prefix_length': '32',
                 'subnet_prefix_length': '24',
                 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_firewall_psa(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Configure FW psa successfully without "
                     "source_prefix_length")
        # Configure firewall psa successfully without source_prefix_length
        param = {'name': 'psa-1Mbps-per-source-24-32-256-1',
                 'count': True, 'filter_specific': True,
                 'destination_prefix_length': '32',
                 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_firewall_psa(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Configure FW psa successfully without commit")
        # Configure firewall psa successfully without commit
        param = {'name': 'psa-1Mbps-per-source-24-32-256-1',
                 'policer': '1Mbps-policer',
                 'source_prefix_length': '8',
                 'subnet_prefix_length': '24'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_firewall_psa(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Configure firewall psa unsuccessfully")
        # Configure firewall psa unsuccessfully
        param = {'name': 'psa-1Mbps-per-source-24-32-256-1',
                 'policer': '1Mbps-policer',
                 'source_prefix_length': '8',
                 'subnet_prefix_length': '24'}
        self.jobject.config = MagicMock(
            return_value=Response(response='syntax error'))
        self.assertFalse(configure_firewall_psa(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_configure_prefix_list(self):
        from jnpr.toby.firewall.Firewall import configure_prefix_list
        logging.info("-----------Test configure_prefix_list: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Configure prefix list successfully with commit")
        # Configure prefix list successfully with commit
        param = {'name': 'customers',
                 'list': ['172.16.1.16/28'],
                 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_prefix_list(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Configure prefix list successfully without commit")
        # Configure prefix list successfully without commit
        param = {'name': 'customers',
                 'list': ['172.16.1.16/28', '172.16.1.16/28']}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_prefix_list(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Configure prefix list unsuccessfully")
        # Configure prefix list unsuccessfully
        param = {'name': 'customers',
                 'list': '172.16.1.16/28'}
        self.jobject.config = MagicMock(
            return_value=Response(response='syntax error'))
        self.assertFalse(configure_prefix_list(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_get_rpf_counter(self):
        from jnpr.toby.firewall.Firewall import get_rpf_counter
        logging.info("-----------Test get_rpf_counter: -----------")
        ######################################################################
        logging.info("Test case 1: Run with valid params and valid response ")
        xml = """<interface-information>
                    <logical-interface>
                        <name>xe-0/0/0.1</name>
                        <address-family>
                            <address-family-name>inet</address-family-name>
                            <route-rpf-statistics>
                                <route-rpf-packets>11023</route-rpf-packets>
                                <route-rpf-bytes>20454424</route-rpf-bytes>
                            </route-rpf-statistics>
                        </address-family>
                    </logical-interface>
                </interface-information>"""
        response = etree.fromstring(xml)
        param = {'interface': ['xe-0/0/0.1', 'xe-0/0/0.2']}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        expectation = {
            'xe-0/0/0.1': {'packets': '11023', 'bytes': '20454424'},
            'xe-0/0/0.2': {'packets': '11023', 'bytes': '20454424'}}
        self.assertEqual(get_rpf_counter(self.jobject, **param), expectation,
                         "Result is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error in response")
        param = {'interface': 'xe-0/0/0.5'}
        self.jobject.execute_rpc = MagicMock(side_effect=Exception('error'))
        self.assertEqual(get_rpf_counter(self.jobject, **param), {},
                         "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with invalid response")
        xml = """<abc>1</abc>"""
        response = etree.fromstring(xml)
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_rpf_counter(self.jobject, **param), {},
                         "Return should be a Null Dict")
        logging.info("\tPassed")

    def test_get_firewall_psc(self):
        from jnpr.toby.firewall.Firewall import get_firewall_psc
        logging.info("-----------Test get_firewall_psc: -----------")

        ######################################################################
        logging.info("Test case 1: run with valid params and valid response")

        xml = """<firewall-prefix-action-information>
                    <filter-information>
                        <filter-name>PROTECTHOST</filter-name>
                        <counter>
                            <counter-name>act1-0</counter-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </counter>
                        <counter>
                            <counter-name>act1-1</counter-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </counter>
                        <counter>
                            <counter-name>act1-2</counter-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </counter>
                        <counter>
                            <counter-name>act1-3</counter-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </counter>
                    </filter-information>
            </firewall-prefix-action-information>"""
        response = etree.fromstring(xml)
        param = {'filter': 'test', 'prefix_action': 'act1-term1',
                 'from': 0, 'to': 3}
        expectation = {'act1-2': {'byte_count': '0', 'packet_count': '0'},
                       'act1-1': {'byte_count': '0', 'packet_count': '0'},
                       'act1-0': {'byte_count': '0', 'packet_count': '0'},
                       'act1-3': {'byte_count': '0', 'packet_count': '0'}}

        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_psc(self.jobject, **param), expectation,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response")

        param = {'filter': 'test', 'prefix_action': 'act1-term1',
                 'from': 0, 'to': 3}
        self.jobject.execute_rpc = MagicMock(side_effect=Exception('error'))
        self.assertEqual(get_firewall_psc(self.jobject, **param), {},
                         "Return should be a Null Dict")

    def test_get_firewall_counter(self):
        from jnpr.toby.firewall.Firewall import get_firewall_counter
        logging.info("-----------Test get_firewall_counter: -----------")

        ######################################################################
        logging.info("Test case 1: filter or interface value not be specified")
        xml = """<filter-information>
                    <filter-name>xe-0/0/0.81-i</filter-name>
                        <counter>
                            <counter-name>packets</counter-name>
                            <packet-count>1281805</packet-count>
                            <byte-count>71852096</byte-count>
                        </counter>
                 </filter-information>"""
        response = etree.fromstring(xml)
        # filter or interface value was not be specified
        param = {'counter': 'counter1'}
        self.assertFalse(get_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: specifiy both input and output")
        # specifiy both input and output
        param = {'interface': 'xe-0/0/0.1', 'input': True, 'output': True}
        self.assertFalse(get_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: get firewall counter with input option")
        # get firewall counter with input option
        param = {'interface': 'xe-0/0/0.1',
                 'input': True, 'counter': 'packets'}
        expectation = {'packets': {'packet_count':
                                   '1281805', 'byte_count': '71852096'}}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_counter(self.jobject, **param),
                         expectation, "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: get firewall counter with output option")
        # get firewall counter with output option
        param = {'interface': 'xe-0/0/0.1',
                 'output': True, 'counter': 'packets'}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_counter(self.jobject, **param),
                         expectation, "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: get FW counter without counter option")
        # get firewall counter without counter option
        param = {'interface': 'xe-0/0/0.1', 'output': True}
        self.jobject.execute_rpc = MagicMock(side_effect=Exception('error'))
        self.assertFalse(get_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Get FW counter with incorrect xml response")
        # Get firewall counter with incorrect xml response
        xml = """<filter-information>
                    <filter-name>xe-0/0/0.81-i</filter-name>
                        <counter>
                        </counter>
                 </filter-information>"""
        response = etree.fromstring(xml)
        param = {'counter': 'counter1'}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertFalse(get_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_firewall_counter')
    def test_check_firewall_counter(self, mock_get_fw_counter, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_firewall_counter
        logging.info("-----------Test check_firewall_counter: -----------")

        ######################################################################
        logging.info("Test case 1: Run with only counter")
        param = {'counter': 'counter1'}
        self.assertFalse(check_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: With correct packet_count and byte_count")
        param = {'interface': 'xe-0/0/0.1', 'input': True,
                 'byte': [100, 7571314296], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {
            'packets': {'packet_count': '34335', 'byte_count': '10000'}}
        self.assertTrue(check_firewall_counter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: With wrong packet_count and byte_count")
        param = {'interface': 'xe-0/0/0.1', 'input': True,
                 'byte': [100, 1000], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {
            'packets': {'packet_count': '34335', 'byte_count': '2000'}}
        self.assertFalse(check_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: With wrong packet_count only")
        param = {'interface': 'xe-0/0/0.1', 'input': True,
                 'byte': [100, 1000], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {
            'packets': {'packet_count': '111', 'byte_count': '200'}}
        self.assertFalse(check_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Run with correct packet_count only")
        param = {'interface': 'xe-0/0/0.1', 'input': True,
                 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {
            'packets': {'packet_count': '34335', 'byte_count': '200'}}
        self.assertTrue(check_firewall_counter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Run with correct byte_count only")
        param = {'filter': 'filter1', 'input': True,
                 'byte': [100, 7571314296], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {
            'packets': {'packet_count': '34335', 'byte_count': '10000'}}
        self.assertTrue(check_firewall_counter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 7: Run with invalid response of get_firewall_counter")
        param = {'filter': 'filter1', 'input': True,
                 'byte': [100, 7571314296], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {}
        self.assertFalse(check_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Run without packet and byte in params")
        param = {'interface': 'xe-0/0/0.1'}
        mock_get_fw_counter.return_value = {
            'packets': {'packet_count': '34335', 'byte_count': '10000'}}
        self.assertTrue(check_firewall_counter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Run with chck_count and wrong byte_count")
        param = {'interface': 'xe-0/0/0.1', 'input': True, 'byte': [100, 200],
                 'packet': [34332, 5334563], 'chk_count': 2, 'chk_interval': 1}
        mock_get_fw_counter.return_value = {
            'packets': {'packet_count': '34335', 'byte_count': '10000'}}
        self.assertFalse(check_firewall_counter(self.jobject, **param),
                         "Return should be False")

    def test_get_firewall_log(self):
        from jnpr.toby.firewall.Firewall import get_firewall_log
        logging.info("-----------Test get_firewall_log: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response")
        xml = """
                 <firewall-log-information>
                    <log-information>
                        <time>2017-03-29 19:29:16 PDT</time>
                        <filter-name>icmp_syslog</filter-name>
                        <action-name>accept</action-name>
                        <interface-name>fxp0.0</interface-name>
                        <protocol-name>TCP</protocol-name>
                        <packet-length>92</packet-length>
                        <destination-address>10.48.4.108:22</destination-address>
                        <source-address>172.29.27.95:49658</source-address>
                    </log-information>
                    <log-information>
                        <time>2017-03-29 19:29:16 PDT</time>
                        <filter-name>icmp_syslog</filter-name>
                        <action-name>accept</action-name>
                        <interface-name>fxp0.0</interface-name>
                        <protocol-name>TCP</protocol-name>
                        <packet-length>92</packet-length>
                        <destination-address>10.48.4.108:22</destination-address>
                        <source-address>172.29.27.95:49658</source-address>
                    </log-information>
                </firewall-log-information>"""
        response = etree.fromstring(xml)
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        param = {'filter': 'icmp_syslog', 'protocol': 'TCP',
                 'packet_length': '92', 'interface': 'fxp0.0',
                 'action': 'accept', 'from': '00:00:00', 'to': '23:59:59'}
        result = get_firewall_log(self.jobject, **param)
        self.assertGreater(len(result), 0, "Return should not a Null Dict")

        param = {'filter': 'icmp_syslog', 'protocol': 'TCP',
                 'packet_length': '92', 'interface': 'fxp0.0',
                 'action': 'accept', 'from': '00:00:00'}
        result = get_firewall_log(self.jobject, **param)
        self.assertGreater(len(result), 0, "Return should not a Null Dict")

        param = {'filter': 'icmp_syslog', 'protocol': 'TCP',
                 'packet_length': '92', 'interface': 'fxp0.0',
                 'action': 'accept', 'to': '23:59:59'}
        result = get_firewall_log(self.jobject, **param)
        self.assertGreater(len(result), 0, "Return should not a Null Dict")

        param = {'filter': 'icmp_syslog', 'protocol': 'TCP',
                 'packet_length': '92', 'interface': 'fxp0.0',
                 'action': 'accept'}
        result = get_firewall_log(self.jobject, **param)
        self.assertGreater(len(result), 0, "Return should not a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with incorrect filter name")
        param = {'filter': 'abc'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with incorrect protocol")
        param = {'protocol': 'abc'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with incorrect packet_length")
        param = {'packet_length': 'abc'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Run with incorrect action")
        param = {'action': 'abc'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Run with incorrect from")
        param = {'from': '20:01:00'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Run with incorrect to")
        param = {'to': '18:02:59'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Run with incorrect source_address")
        param = {'source_address': 'abc'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Run with incorrect destination_address")
        param = {'destination_address': 'abc'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 10: Run with wrong response")
        param = {'filter': 'icmp_syslog'}
        self.jobject.execute_rpc = MagicMock(return_value=Exception('error'))
        result = get_firewall_log(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        xml = """
                 <firewall-log-information>
                </firewall-log-information>"""
        response = etree.fromstring(xml)
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        param = {'filter': 'icmp_syslog'}
        result = get_firewall_log(self.jobject, **param)
        self.assertEqual(result, {}, "Return should be a Null Dict")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_firewall_log')
    def test_check_firewall_log(self, mock, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_firewall_log
        logging.info("-----------Test check_firewall_log: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid return of get_firewall_log")
        mock.return_value = {'action': 'accept',
                             'destination_address': '10.48.4.108:22',
                             'packet_length': '92', 'protocol': 'TCP',
                             'filter': 'icmp_syslog',
                             'source_address': '172.29.27.95:49658'}

        param = {'filter': 'icmp_syslog', 'protocol': 'TCP',
                 'interface': 'fxp0.0', 'action': 'accept',
                 'from': '00:00:00', 'to': '23:59:59',
                 'chk_count': 2, 'chk_interval': 1}
        result = check_firewall_log(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: with invalid return of get_firewall_log")
        mock.return_value = {}
        param = {'filter': 'icmp_syslog', 'protocol': 'TCP',
                 'interface': 'fxp0.0', 'action': 'accept',
                 'from': '00:01:00', 'to': '00:02:59',
                 'chk_count': 2, 'chk_interval': 1}
        result = check_firewall_log(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_firewall_psc')
    def test_check_firewall_psc(self, mock, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_firewall_psc
        logging.info("-----------Test check_firewall_psc: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid return of get_firewall_psc")
        # Testcase 1
        mock.return_value = {'act1-3': {'byte_count': '3654',
                                        'packet_count': '4954'}}
        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3,
                 'byte': [1000, 4000], 'packet': 4954}
        result = check_firewall_psc(self.jobject, **param)
        self.assertTrue(result, "Return should be True")

        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3,
                 'packet': 4954}
        result = check_firewall_psc(self.jobject, **param)
        self.assertTrue(result, "Return should be True")

        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3,
                 'byte': 3654}
        result = check_firewall_psc(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid return of get_firewall_psc"
                     " and without byte, packet")
        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3}
        result = check_firewall_psc(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with wrong byte_count and packet_count")
        mock.return_value = {'act1-3': {'byte_count': '9654',
                                        'packet_count': '4952'}}
        param = {'filter': 'test', 'prefix_action': 'act1-3', 'index': 3,
                 'byte': [1000, 4000], 'packet': 4954, 'chk_count': 2,
                 'chk_interval': 1}
        result = check_firewall_psc(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run without byte and packet in params")
        mock.return_value = {'act1-3': {'byte_count': '3654',
                                        'packet_count': '4954'}}
        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3}
        result = check_firewall_psc(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: With invalid return of get_firewall_psc")
        mock.return_value = {}
        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3,
                 'byte': [1000, 4000], 'packet': 4954}
        result = check_firewall_psc(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

    def test_get_pfe_kmem(self):
        from jnpr.toby.firewall.Firewall import get_pfe_kmem
        logging.info("-----------Test get_pfe_kmem: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response")

        param = {'pfe': 'fpc0'}
        res = """
ID      Base      Total(b)       Free(b)       Used(b)   %   Name
--  --------     ---------     ---------     ---------  ---   -----------
 0  452c64a8    1878234844    1560870692     317364152   16  Kernel
 1  b51ffb88      67108860      56200964      10907896   16  LAN buffer
 2  bcdfffe0      52428784      52428784             0    0  Blob
 3  b91ffb88      62914556      62914556             0    0  ISSU scratch
"""

        self.jobject.shell = MagicMock(side_effect=[Response(response=res)])
        expectation = {'total': '1878234844', 'used': '317364152'}
        self.assertDictEqual(get_pfe_kmem(self.jobject, **param), expectation,
                             "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response")
        param = {'pfe': 'fpc0'}
        self.jobject.shell = MagicMock(
            side_effect=Response(response=Exception('error')))

        self.assertFalse(get_pfe_kmem(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with invalid response")
        param = {'pfe': 'fpc0'}
        self.jobject.shell = MagicMock(
            side_effect=[Response(response="testing")])

        self.assertDictEqual(get_pfe_kmem(self.jobject, **param), {},
                             "Return should be a Null Dict")
        logging.info("\tPassed")

    def test_get_pfe_jmem(self):
        from jnpr.toby.firewall.Firewall import get_pfe_jmem
        logging.info("-----------Test get_pfe_jmem: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response")
        param = {'pfe': 'fpc0', 'num': 1}
        res = '''
                Jtree memory segment 0 (Context: 0x472a2640)
                -------------------------------------------
                Memory Statistics:
                   16777216 bytes total
                   10509096 bytes used
                    6124872 bytes available (5655040 bytes from free pages)
                       4032 bytes wasted
                     139216 bytes unusable
                      32768 pages total
                      20587 pages used (2574 pages used in page alloc)
                       1136 pages partially used
                      11045 pages free (max contiguous = 3935)

            '''
        self.jobject.shell = MagicMock(side_effect=[Response(response=res)])
        expectation = {'total': '16777216', 'used': '10509096'}
        self.assertDictEqual(get_pfe_jmem(self.jobject, **param), expectation,
                             "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response")
        param = {'pfe': 'fpc0', 'num': 1}
        self.jobject.shell = MagicMock(
            side_effect=Response(response=Exception('error')))

        self.assertFalse(get_pfe_jmem(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 1: Run with invalid response")
        param = {'pfe': 'fpc0', 'num': 1}
        self.jobject.shell = MagicMock(
            side_effect=[Response(response="testing")])

        self.assertDictEqual(get_pfe_jmem(self.jobject, **param), {},
                             "Return should be a Null Dict")
        logging.info("\tPassed")

    def test_get_pfe_list(self):
        from jnpr.toby.firewall.Firewall import get_pfe_list
        logging.info("-----------Test get_pfe_list: -----------")

        ######################################################################
        logging.info("Test case 1: Get pfe successfully")
        param = {'interface': 'xe-2/1/0'}
        expected_result = ['fpc2']
        self.assertEqual(get_pfe_list(self.jobject, **param), expected_result,
                         "Return is incorrect as expectation")

        param = {'interface': ['xe-2/1/0']}
        expected_result = ['fpc2']
        self.assertEqual(get_pfe_list(self.jobject, **param), expected_result,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with invalid interface")
        param = {'interface': 'gsdgs'}
        expected_result = []
        self.assertEqual(get_pfe_list(self.jobject, **param), expected_result,
                         "Return sould be a Null List")

    def test_get_firewall_policer(self):
        from jnpr.toby.firewall.Firewall import get_firewall_policer
        logging.info("-----------Test configure: -----------")

        ######################################################################
        logging.info("Test case 1: filter or interface value not be specified")
        xml = """<filter-information></filter-information>"""
        response = etree.fromstring(xml)
        # filter or interface value was not be specified
        param = {'interface': 'xe-0/0/1.81', 'input': True,
                 'policer': 'CLASS6_CC'}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_policer(self.jobject, **param), {})

        xml = """<filter-information>
                    <filter-name>xe-0/0/1.81-i</filter-name>
                        <policer>
                            <policer-name>CLASS6_CC-xe-0/0/1.81-i</policer-name>
                            <packet-count>1281805</packet-count>
                            <byte-count>71852096</byte-count>
                        </policer>
                 </filter-information>"""
        response = etree.fromstring(xml)
        # filter or interface value was not be specified
        param = {'policer': 'CLASS6_CC'}
        self.assertFalse(get_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: specifiy both input and output")
        # specifiy both input and output
        param = {'interface': 'xe-0/0/1.81', 'input': True, 'output': True}
        self.assertFalse(get_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: get firewall counter with input option")
        # get firewall counter with input option
        param = {'interface': 'xe-0/0/1.81', 'input': True,
                 'policer': 'CLASS6_CC'}
        expected_result = {'CLASS6_CC-xe-0/0/1.81-i': {
            'packet_count': '1281805', 'byte_count': '71852096'}}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_policer(self.jobject,
                                              **param), expected_result,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: get firewall counter with output option")
        # get firewall counter with output option
        param = {'interface': 'xe-0/0/1.81', 'input': True,
                 'policer': 'CLASS6_CC'}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_policer(self.jobject,
                                              **param), expected_result,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Get FW counter without counter option")
        # get firewall counter without counter option
        param = {'interface': 'xe-0/0/1.81', 'input': 0}
        self.jobject.execute_rpc = MagicMock(side_effect=Exception('error'))
        self.assertFalse(get_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: get firewall counter with output option")

        # get firewall counter with output option
        param = {'interface': 'xe-0/0/1.81', 'input': 0,
                 'policer': 'CLASS6_CC'}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_policer(self.jobject,
                                              **param), expected_result,
                         "Return is incorrect as expectation")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_firewall_policer')
    def test_check_firewall_policer(self, mock_get_fw_counter, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_firewall_policer
        logging.info("-----------Test check_firewall_policer: -----------")

        ######################################################################
        logging.info("Test case 1: Run without interface and filter")

        param = {'policer': 'policer1'}
        self.assertFalse(check_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid packet_count and "
                     "byte_count with interface")
        param = {'interface': 'xe-0/0/0.1', 'input': True,
                 'byte': [100, 7571314296], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {'packets':
                                            {'packet_count': '34335',
                                             'byte_count': '10000'}}
        self.assertTrue(check_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with valid packet_count and "
                     "byte_count with filter")
        param = {'filter': 'filter1', 'input': True,
                 'byte': [100, 7571314296], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {'packets':
                                            {'packet_count': '343325',
                                             'byte_count': '343323'}}
        self.assertTrue(check_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with wrong byte_count and packet_count")

        param = {'filter': 'filter1', 'input': True,
                 'byte': [100, 7571314296], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {'packets':
                                            {'packet_count': '34335',
                                             'byte_count': '10'}}
        self.assertFalse(check_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Run with wrong byte_count")

        param = {'filter': 'filter1', 'input': True,
                 'byte': [100, 7571314296]}
        mock_get_fw_counter.return_value = {'packets':
                                            {'packet_count': '34335',
                                             'byte_count': '10'}}
        self.assertFalse(check_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Run with wrong packet_count")

        param = {'filter': 'filter1', 'input': True,
                 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {'packets':
                                            {'packet_count': '3433',
                                             'byte_count': '10'}}
        self.assertFalse(check_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Run without input and valid packet_count")

        param = {'filter': 'filter1',
                 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {'packets':
                                            {'packet_count': '343324',
                                             'byte_count': '1000'}}
        self.assertTrue(check_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Run with input and byte only in params")

        param = {'filter': 'filter1', 'input': True,
                 'byte': [100, 7571314296]}
        mock_get_fw_counter.return_value = {'packets':
                                            {'packet_count': '343325',
                                             'byte_count': '343323'}}
        self.assertTrue(check_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: With invalid response of get_fw_counter")

        param = {'filter': 'filter1', 'input': True,
                 'byte': [100, 7571314296], 'packet': [34332, 5334563]}
        mock_get_fw_counter.return_value = {}
        self.assertFalse(check_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 10: Run without packet_count and byte_count in params")

        param = {'interface': 'xe-0/0/0.1'}
        mock_get_fw_counter.return_value = {'packets': {
            'packet_count': '34335', 'byte_count': '10000'}}
        self.assertTrue(check_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 11: Run with chk_count and wrong "
                     "byte_count, packet_count")

        param = {'interface': 'xe-0/0/0.1', 'input': True,
                 'byte': [100, 200], 'packet': [34332, 5334563],
                 'chk_count': 2, 'chk_interval': 1}
        mock_get_fw_counter.return_value = {'packets': {
            'packet_count': '34335', 'byte_count': '10000'}}
        self.assertFalse(check_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 12: Run with both input and output in params")

        param = {'interface': 'xe-0/0/0.1', 'input': True, 'output': True}
        self.assertFalse(check_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_filter_index')
    @patch('jnpr.toby.firewall.Firewall.__cprod')
    def test_check_filter_install(self, mock_response, mock_index, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_filter_install
        logging.info("-----------Test check_filter_install: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response")
        param = {'filter': 'icmp_syslog', 'interface': 'xe-0/0/0',
                 'chk_count': 2, 'chk_interval': 1}
        response = ['Pfe Inst:0 Hw Instance 2, type:2 op:2']
        mock_response.return_value = response
        mock_index.return_value = 11
        self.assertTrue(check_filter_install(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid response and list interface")
        param = {'filter': 'icmp_syslog', 'interface': ['xe-0/0/0'],
                 'chk_count': 2, 'chk_interval': 1}
        response = ['Pfe Inst:0 Hw Instance 2, type:2 op:2']
        mock_response.return_value = response
        mock_index.return_value = 11
        self.assertTrue(check_filter_install(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: With invalid response of get_filter_index")
        mock_index.return_value = 0
        self.assertFalse(check_filter_install(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: With valid response filter instasll")
        response = ['Filter Install (10 active planes)   0x09 0x09 0x09 8 ']
        mock_index.return_value = 11
        mock_response.return_value = response
        self.assertTrue(check_filter_install(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: With valid response filter "
                     "instasll and wrong get_filter_index")
        mock_index.return_value = 0
        self.assertFalse(check_filter_install(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: With invalid response filter")
        response = ['zxvccxbxcb']
        mock_index.return_value = 11
        mock_response.return_value = response
        self.assertFalse(check_filter_install(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_filter_index')
    @patch('jnpr.toby.firewall.Firewall.__cprod')
    def test_check_filter_remove(self, mock_response, mock_index, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_filter_remove
        logging.info("-----------Test check_filter_remove: -----------")

        ######################################################################
        logging.info("Test case 1: With invalid response and single interface")
        param = {'filter': 'icmp_syslog', 'interface': 'xe-0/0/0',
                 'chk_count': 2, 'chk_interval': 1}
        response = ['hgdhgh']
        mock_response.return_value = response
        mock_index.return_value = 11
        self.assertTrue(check_filter_remove(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: With invalid response and list interface")
        param = {'filter': 'icmp_syslog', 'interface': ['xe-0/0/0'],
                 'chk_count': 2, 'chk_interval': 1}
        response = ['hgdhgh']
        mock_response.return_value = response
        mock_index.return_value = 11
        self.assertTrue(check_filter_remove(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: With valid response and wrong get_filter_index")
        response = ['Filter Install (10 active planes)   0x09 0x09 0x09 8 ']
        mock_response.return_value = response
        self.assertFalse(check_filter_remove(self.jobject, **param),
                         "Return should be False")

        response = ['Pfe Inst:0 Hw Instance 2, type:2 op:2 ']
        mock_response.return_value = response
        self.assertFalse(check_filter_remove(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 5: With valid response and get_filter_index")
        mock_index.return_value = 0
        self.assertTrue(check_filter_remove(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    def test_get_rchip_stat(self):
        from jnpr.toby.firewall.Firewall import get_rchip_stat
        logging.info("-----------Test get_rchip_stat: -----------")

        ######################################################################
        logging.info("Test case 1: run with model m120 and rchip not exist")
        self.jobject.get_model = MagicMock(return_value='m120')
        res1 = 'pass'
        res2 = 'rchip not exist'
        param = {'vty': 'fpc0', 'rchip': [2, 3]}
        self.jobject.vty = MagicMock(side_effect=[Response(response=res1),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=res2),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response="")])

        self.assertTrue(get_rchip_stat(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: run with model m320 and rchip not exist")
        self.jobject.get_model = MagicMock(return_value='m320')
        res = 'rchip not exist'
        param = {'vty': 'fpc0', 'rchip': 2}
        self.jobject.vty = MagicMock(side_effect=[Response(response=res),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response="")])

        self.assertFalse(get_rchip_stat(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: run with model m220 and rchip not exist")
        self.jobject.get_model = MagicMock(return_value='m220')
        res = 'rchip not exist'
        param = {'vty': 'fpc0'}
        self.assertFalse(get_rchip_stat(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: run with model m320 and error response")
        self.jobject.get_model = MagicMock(return_value='m320')
        param = {'vty': 'fpc0', 'rchip': 2}
        self.jobject.vty = MagicMock(
            side_effect=Response(response=Exception('error')))

        self.assertFalse(get_rchip_stat(self.jobject, **param))
        logging.info("\tPassed")

    def test__timeless(self):
        logging.info("-----------Test __timeless: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid input")
        result = timeless('08:02:32', '11:52:02')
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with wrong input")
        result = timeless('11:52:02', '08:02:32')
        self.assertFalse(result, "Time due to time a > time b FALSE")
        logging.info("\tPassed")

    def test__check_value(self):
        logging.info("-----------Test __check_value: -----------")

        ######################################################################
        logging.info("Test case 1: v is list, and a in range v")
        valid_a = [100, 150, 200]
        v = [100, 200]
        result = True
        for a in valid_a:
            if not check_value(a, v):
                result = False
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: v is list, and a out of range v")
        valid_a = [99, 201]
        v = [100, 200]
        result = False
        for a in valid_a:
            if check_value(a, v):
                result = True
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: v is integer, and a is equal v")
        a = '100'
        v = 100
        result = check_value(a, v)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: v is integer, and a is not equal v")
        a = 100
        v = 200
        result = check_value(a, v)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: v is string, and a is in v")
        a = "unit test"
        v = "this is unit test"
        result = check_value(a, v)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: v is string, and a is not in v")
        a = "function test"
        v = "this is unit test"
        result = check_value(a, v)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: v is string, a is integer in v")
        a = 7
        v = "7 unit tests"
        result = check_value(a, v)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: v is integer, a is string")
        a = 7
        v = "7 unit tests"
        result = check_value(a, v)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

    def test_configure_firewall_policer(self):
        from jnpr.toby.firewall.Firewall import configure_firewall_policer
        logging.info("-----------Test configure_firewall_policer: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Configure firewall policer successfully with commit")
        param = {'name': '1Mbps-policer',
                 'filter_specific': True,
                 'logical_bandwidth_policer': True,
                 'logical_interface_policer': True,
                 'physical_interface_policer': True,
                 'shared_bandwidth_policer': True,
                 'limit_type': 'if-exceeding-pps',
                 'packet_burst': '1m',
                 'pps_limit': '63k',
                 'action': ['accept', 'discard'],
                 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Configure firewall policer "
                     "successfully without commit")
        param = {'name': '1Mbps-policer',
                 'filter_specific': True,
                 'logical_bandwidth_policer': True,
                 'logical_interface_policer': True,
                 'physical_interface_policer': True,
                 'shared_bandwidth_policer': True,
                 'limit_type': 'if-exceeding-pps',
                 'packet_burst': '1m',
                 'pps_limit': '63k',
                 'action': ['accept', 'discard']}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Configure firewall policer unsuccessfully "
                     "with incorrect limit type")
        param = {'name': '1Mbps-policer',
                 'filter_specific': True,
                 'logical_bandwidth_policer': True,
                 'logical_interface_policer': True,
                 'physical_interface_policer': True,
                 'shared_bandwidth_policer': True,
                 'limit_type': 'dfdf',
                 'packet_burst': '1m',
                 'pps_limit': '63k',
                 'action': ['accept', 'discard']}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertFalse(configure_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Configure firewall policer "
                     "unsuccessfully with commit set failed")
        param = {'name': '1Mbps-policer',
                 'limit_type': 'if-exceeding',
                 'bw_percent': '100',
                 'burst_size': '63k',
                 'action': ['accept', 'discard'],
                 'commit': 1}
        self.jobject.config = MagicMock(
            return_value=Response(response='syntax error'))
        self.assertFalse(configure_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Configure firewall policer "
                     "successfully with action is a string")
        param = {'name': '1Mbps-policer',
                 'limit_type': 'if-exceeding',
                 'bw_limit': '1m',
                 'burst_size': '63k',
                 'action': 'discard',
                 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Configure firewall policer unsuccessfully"
                     " without burst-size-limit and bandwidth"
                     "as limit/percent value")
        param = {'name': '1Mbps-policer',
                 'limit_type': 'if-exceeding',
                 'action': ['accept', 'discard'],
                 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertFalse(configure_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Configure firewall policer unsuccessfully"
                     " without packet-burst and pps-limit")
        param = {'name': '1Mbps-policer',
                 'limit_type': 'if-exceeding-pps',
                 'action': ['accept', 'discard'],
                 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertFalse(configure_firewall_policer(self.jobject, **param),
                         "Return should be False")

    def test_get_dcu_counter(self):
        from jnpr.toby.firewall.Firewall import get_dcu_counter
        logging.info("-----------Test get_dcu_counter: -----------")

        ######################################################################
        logging.info("Test case 1: With valid response and single interface")
        param = {'interface': 'ge-0/0/1.0', 'dcu_name': 'ABC'}
        xml = '''
                <rpc-reply>
                    <destination-class>
                        <dcu-class-name>ABC</dcu-class-name>
                        <dcu-class-packets>10</dcu-class-packets>
                        <dcu-class-bytes>20</dcu-class-bytes>
                    </destination-class>
                </rpc-reply>
                '''
        res = etree.fromstring(xml)
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        expectation = {'ABC': {'byte_count': '20', 'packet_count': '10'}}
        self.assertDictEqual(get_dcu_counter(self.jobject,
                                             **param), expectation,
                             "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: With valid response and list interface")
        param = {'interface': ['ge-0/0/1', 'ge-1/2/3'], 'dcu_name': 'ABC'}
        xml1 = '''
                    <rpc-reply>
                        <destination-class>
                            <dcu-class-name>ABC</dcu-class-name>
                            <dcu-class-packets>10</dcu-class-packets>
                            <dcu-class-bytes>20</dcu-class-bytes>
                        </destination-class>
                    </rpc-reply>
                    '''
        xml2 = '''
            <rpc-reply>
                <destination-class>
                    <dcu-class-name>XYZ</dcu-class-name>
                    <dcu-class-packets>30</dcu-class-packets>
                    <dcu-class-bytes>40</dcu-class-bytes>
                </destination-class>
            </rpc-reply>
            '''
        res1 = etree.fromstring(xml1)
        res2 = etree.fromstring(xml2)
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res1), Response(response=res2)])
        expectation = {'ge-0/0/1': {'ABC': {'byte_count': '20',
                                            'packet_count': '10'}},
                       'ge-1/2/3': {'XYZ': {'byte_count': '40',
                                            'packet_count': '30'}}}
        self.assertDictEqual(get_dcu_counter(self.jobject,
                                             **param), expectation,
                             "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with invalid response")
        param = {'interface': 'ge-0/0/1.0', 'dcu_name': 'ABC'}
        xml = '''
                <rpc-reply>
                    <check-fail>
                        <scu-fail>ABC</scu-fail>
                    </check-fail>
                </rpc-reply>
                '''
        res = etree.fromstring(xml)
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        self.assertDictEqual(get_dcu_counter(self.jobject, **param), {},
                             "Return sould be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with Error response")
        param = {'interface': 'ge-0/0/1.0', 'dcu_name': 'ABC'}
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=Response(response=Exception('error')))

        with self.assertRaises(Exception) as context:
            get_dcu_counter(self.jobject, **param)
        self.assertTrue('Fail to get the response of dcu counter'
                        in str(context.exception))
        logging.info("\tPassed")

    def test_get_scu_counter(self):
        from jnpr.toby.firewall.Firewall import get_scu_counter
        logging.info("-----------Test get_scu_counter: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response and single intf")
        param = {'interface': 'ge-0/0/1.0', 'scu_name': 'ABC'}
        xml = '''
            <rpc-reply>
                <source-class>
                    <scu-class-name>ABC</scu-class-name>
                    <scu-class-packets>10</scu-class-packets>
                    <scu-class-bytes>20</scu-class-bytes>
                </source-class>
            </rpc-reply>
            '''
        res = etree.fromstring(xml)
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        expectation = {'ABC': {'byte_count': '20', 'packet_count': '10'}}
        self.assertDictEqual(get_scu_counter(self.jobject,
                                             **param), expectation,
                             "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid response and list intf")
        param = {'interface': ['ge-0/0/1', 'ge-1/2/3'], 'scu_name': 'ABC'}
        xml1 = '''
            <rpc-reply>
                <source-class>
                    <scu-class-name>ABC</scu-class-name>
                    <scu-class-packets>10</scu-class-packets>
                    <scu-class-bytes>20</scu-class-bytes>
                </source-class>
            </rpc-reply>
            '''
        xml2 = '''
            <rpc-reply>
                <source-class>
                    <scu-class-name>XYZ</scu-class-name>
                    <scu-class-packets>30</scu-class-packets>
                    <scu-class-bytes>40</scu-class-bytes>
                </source-class>
            </rpc-reply>
            '''
        res1 = etree.fromstring(xml1)
        res2 = etree.fromstring(xml2)
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res1), Response(response=res2)])
        expectation = {'ge-0/0/1': {'ABC': {'byte_count': '20',
                                            'packet_count': '10'}},
                       'ge-1/2/3': {'XYZ': {'byte_count': '40',
                                            'packet_count': '30'}}}
        self.assertDictEqual(get_scu_counter(self.jobject,
                                             **param), expectation,
                             "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with invalid response")
        param = {'interface': 'ge-0/0/1.0', 'scu_name': 'ABC'}
        xml = '''
                <rpc-reply>
                    <check-fail>
                        <scu-fail>ABC</scu-fail>
                    </check-fail>
                </rpc-reply>
                '''
        res = etree.fromstring(xml)
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])

        self.assertDictEqual(get_scu_counter(self.jobject, **param), {},
                             "Return sould be a Null Dict")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with error response")
        param = {'interface': 'ge-0/0/1.0', 'scu_name': 'ABC'}
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=Response(response=Exception('error')))

        with self.assertRaises(Exception) as context:
            get_scu_counter(self.jobject, **param)
        self.assertTrue('Fail to get the response of scu counter'
                        in str(context.exception))
        logging.info("\tPassed")

    def test_clear_vty_syslog(self):
        from jnpr.toby.firewall.Firewall import clear_vty_syslog
        logging.info("-----------Test clear_vty_syslog: -----------")

        ######################################################################
        logging.info(
            "Test case 1: clear vty syslog successfully with single fpc")
        param = {'vty': 'fpc0'}
        self.jobject.vty = MagicMock(side_effect=[Response(status=True)])

        result = clear_vty_syslog(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: clear vty syslog successfully with list fpc")
        param = {'vty': ['fpc0']}
        self.jobject.vty = MagicMock(side_effect=[Response(status=True),
                                                  Response(status=True)])

        result = clear_vty_syslog(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: cannot clear vty syslog counter with error response")
        param = {'vty': 'fpc0'}
        self.jobject.vty = MagicMock(side_effect=[Response(status=False)])

        result = clear_vty_syslog(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

    def test_get_vty_syslog(self):
        from jnpr.toby.firewall.Firewall import get_vty_syslog
        logging.info("-----------Test get_vty_syslog: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Get vty syslog successfully with single fpc")
        param = {'vty': 'fpc0'}
        self.jobject.vty = MagicMock(
            return_value=Response(response='Log: abc'))
        result = get_vty_syslog(self.jobject, **param)
        self.assertEqual(result, 'Log: abc',
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Get vty syslog successfully with list fpc")
        param = {'vty': ['fpc0']}
        self.jobject.vty = MagicMock(
            return_value=Response(response='Log: abc'))
        result = get_vty_syslog(self.jobject, **param)
        self.assertEqual(result, 'Log: abc',
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

    def test_check_vty_error(self):
        from jnpr.toby.firewall.Firewall import check_vty_error
        logging.info("-----------Test check_vty_error: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response match in params")
        param = {'vty': ['fpc0', 'fpc1'], 'error': 'MQCHIP'}
        self.jobject.vty = MagicMock(
            side_effect=[Response(response="LOG: Err MQCHIP error"),
                         Response(response="LOG: Err ABC error")])

        self.assertTrue(check_vty_error(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: With invalid response not match in params")
        param = {'vty': 'fpc0', 'error': 'MQCHIP'}
        self.jobject.vty = MagicMock(
            side_effect=[Response(response="LOG: Err ABC error")])

        self.assertFalse(check_vty_error(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_get_firewall_psp(self):
        from jnpr.toby.firewall.Firewall import get_firewall_psp
        logging.info("-----------Test get_firewall_psp: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response")
        xml = """
              <firewall-prefix-action-information>
                    <filter-information>
                        <filter-name>test</filter-name>
                        <policer>
                            <policer-name>act1-0</policer-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </policer>
                        <policer>
                            <policer-name>act1-1</policer-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </policer>
                        <policer>
                            <policer-name>act1-2</policer-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </policer>
                        <policer>
                            <policer-name>act1-3</policer-name>
                            <packet-count>0</packet-count>
                            <byte-count>0</byte-count>
                        </policer>
                    </filter-information>
            </firewall-prefix-action-information>
                """
        response = etree.fromstring(xml)
        param = {'filter': 'test', 'prefix_action': 'act1-term1',
                 'from': 0, 'to': 3}

        expectation = {'act1-2': {'packet_count': '0', 'byte_count': '0'},
                       'act1-1': {'packet_count': '0', 'byte_count': '0'},
                       'act1-3': {'packet_count': '0', 'byte_count': '0'},
                       'act1-0': {'packet_count': '0', 'byte_count': '0'}}

        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        result = get_firewall_psp(self.jobject, **param)
        self.assertEqual(result, expectation,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with invalid response")
        xml = """
                <firewall-prefix-action-information>
                </firewall-prefix-action-information>
            """
        response = etree.fromstring(xml)
        param = {'filter': 'test', 'prefix_action': 'act1-term1',
                 'from': 0, 'to': 3}
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=response))
        self.assertEqual(get_firewall_psp(self.jobject, **param), {},
                         "Return sould be a Null Dict")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.__cprod')
    def test_get_filter_index(self, mock_response):
        from jnpr.toby.firewall.Firewall import get_filter_index
        logging.info("-----------Test get_filter_index: -----------")

        ######################################################################
        logging.info("Test case 1: Get index successfully with valid response")
        param = {'filter': 'HOSTBOUND_IPv4_FILTER', 'interface': 'ge-2/0/7.0',
                 'family': 'inet', 'if_specific': 1, 'input': 1, 'output': 0}

        response = ['46137345  Classic    HOSTBOUND_IPv4_FILTER-'
                    'ge-2/0/7.0-inet-i',
                    '46137346  Classic    HOSTBOUND_IPv6_FILTER']
        mock_response.return_value = response
        self.assertEqual(get_filter_index(self.jobject, **param), 46137345,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Get index successfully with valid response"
                     " and without if_specific")
        param = {'filter': 'HOSTBOUND_IPv4_FILTER', 'interface': 'ge-2/0/7.0',
                 'family': 'inet', 'input': 1, 'output': 0}
        response = ['46137345  Classic    HOSTBOUND_IPv4_FILTER-'
                    'ge-2/0/7.0-inet-i',
                    '46137346  Classic    HOSTBOUND_IPv6_FILTER']
        mock_response.return_value = response
        self.assertEqual(get_filter_index(self.jobject, **param), 46137345,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Get index successfully with valid response"
                     " and pfe")

        param = {'interface': 'ge-2/0/7.0', 'pfe': 'fpc0', 'if_specific': True,
                 'input': 0, 'output': 1}
        response = ['46137345  Classic    ge-2/0/7.0-o',
                    '46137346  Classic    HOSTBOUND_IPv6_FILTER']
        mock_response.return_value = response
        self.assertEqual(get_filter_index(self.jobject, **param), 46137345,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 4: Get index unsuccessfully with invalid response")
        param = {'interface': 'ge-2/0/7.0', 'pfe': 'fpc0', 'if_specific': True,
                 'input': 0, 'output': 1}
        response = ['dsfsdfd']
        mock_response.return_value = response
        self.assertEqual(get_filter_index(self.jobject, **param), None,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Raise exception without interface param")
        param = {'filter': 'HOSTBOUND_IPv4_FILTER', 'family': 'inet',
                 'if_specific': 1, 'input': 1, 'output': 0}
        with self.assertRaises(Exception) as context:
            get_filter_index(self.jobject, **param)
        self.assertTrue('interface-specific filter' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: With both input and output in params")
        param = {'filter': 'HOSTBOUND_IPv4_FILTER', 'interface': 'ge-2/0/7.0',
                 'family': 'inet', 'if_specific': 1, 'input': 1, 'output': 1}
        with self.assertRaises(Exception) as context:
            get_filter_index(self.jobject, **param)
        self.assertTrue('cannot specifiy both input '
                        'and output options' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Get index unsuccessfully without filter")
        param = {'interface': 'ge-2/0/7.0', 'pfe': 'fpc0',
                 'if_specific': False, 'input': 0, 'output': 1, 'filter': None}
        self.assertEqual(get_filter_index(self.jobject, **param), None,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.__get_dst_addrss')
    def test__cprod(self, mock_dst_addrss):
        logging.info("-----------Test __cprod: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response and model = 15.1")
        self.jobject.get_version = MagicMock(return_value='15.1')
        mock_dst_addrss.return_value = '00:1C:23:59:5A:92'
        response = """9  Classic    -         rpf-special-case-dhcp-bootp
                     11  Classic    -         xe-2/3/0.2582-i"""
        self.jobject.shell = MagicMock(
            return_value=Response(response=response))
        self.assertNotEqual(cprod(self.jobject, name='fpc0',
                                  cmd="show filter"), [],
                            "Return is incorrect as expectation")
        self.assertNotEqual(cprod(self.jobject, option="-t",
                                  cmd="show filter"), [],
                            "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run without name and option in params")

        with self.assertRaises(Exception) as context:
            cprod(self.jobject, cmd="show filter")
        self.assertTrue('Name is required unless there are options'
                        in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run without cmd and option")
        with self.assertRaises(Exception) as context:
            cprod(self.jobject, name='fpc0')
        self.assertTrue('Either cmd or cmd_array must be specified unless'
                        in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with valid response and model = 5.4")
        self.jobject.get_version = MagicMock(return_value='5.4')
        self.assertNotEqual(cprod(self.jobject, name='feb',
                                  cmd="show filter", option="-t"), [],
                            "Return is incorrect as expectation")
        logging.info("\tPassed")

    def test__get_dst_addrss(self):
        logging.info("-----------Test __get_dst_addrss: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response and match pfe")
        response = """
  Name                TNPaddr      MAC address IF      MTU E H R
master                   0x1 02:00:00:00:00:04 em0    1500 0 0 3
master                   0x1 02:00:01:00:00:04 em1    1500 0 1 3
re0                      0x4 02:00:00:00:00:04 em0    1500 0 0 3
re0                      0x4 02:00:01:00:00:04 em1    1500 0 1 3
fpc0                    0x10 02:00:00:00:00:10 em0    1500 5 0 3
fpc2                    0x12 02:00:00:00:00:12 em0    1500 4 0 3
bcast             0xffffffff ff:ff:ff:ff:ff:ff em0    1500 0 0 3
bcast             0xffffffff ff:ff:ff:ff:ff:ff em1    1500 0 1 3
"""
        self.jobject.shell = MagicMock(
            return_value=Response(response=response))
        pfe = "fpc0"
        self.assertEqual(get_dst_addrss(self.jobject, pfe), '0x10',
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid response and not match pfe")

        response = """
  Name                TNPaddr      MAC address IF      MTU E H R
master                   0x1 02:00:00:00:00:04 em0    1500 0 0 3
master                   0x1 02:00:01:00:00:04 em1    1500 0 1 3
re0                      0x4 02:00:00:00:00:04 em0    1500 0 0 3
re0                      0x4 02:00:01:00:00:04 em1    1500 0 1 3
fpc0                    0x10 02:00:00:00:00:10 em0    1500 5 0 3
fpc2                    0x12 02:00:00:00:00:12 em0    1500 4 0 3
bcast             0xffffffff ff:ff:ff:ff:ff:ff em0    1500 0 0 3
bcast             0xffffffff ff:ff:ff:ff:ff:ff em1    1500 0 1 3
"""
        self.jobject.shell = MagicMock(
            return_value=Response(response=response))
        pfe = "fpc3"
        self.assertEqual(get_dst_addrss(self.jobject, pfe), '',
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with invalid response")

        self.jobject.shell = MagicMock(return_value=Response(response=''))
        self.assertEqual(get_dst_addrss(self.jobject, pfe), None,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_firewall_psp')
    def test_check_firewall_psp(self, mock, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_firewall_psp
        logging.info("-----------Test check_firewall_psp: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid return of get_firewall_psp"
                     " and correct packet_count")
        mock.return_value = {'act1-3': {'byte_count': '3654',
                                        'packet_count': '4954'}}
        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3,
                 'packet': 4954, 'chk_count': 2}
        result = check_firewall_psp(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid return of get_firewall_psp"
                     " and smaller packet_count")
        mock.return_value = {'act1-3': {'byte_count': '9654',
                                        'packet_count': '4952'}}
        param = {'filter': 'test', 'prefix_action': 'act1-3', 'index': 3,
                 'packet': 4954, 'chk_count': 2,
                 'chk_interval': 1}
        result = check_firewall_psp(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with invalid response")
        mock.return_value = {}
        param = {'filter': 'test', 'prefix_action': 'act1-3', 'index': 3,
                 'packet': 4954, 'chk_count': 1,
                 'chk_interval': 1}
        result = check_firewall_psp(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with valid return of get_firewall_psp"
                     " and bigger packet_count")
        mock.return_value = {'act1-3': {'byte_count': '3654',
                                        'packet_count': '4954'}}
        param = {'filter': 'test', 'prefix_action': 'act1-term1', 'index': 3,
                 'packet': 4955, 'chk_count': 1, 'chk_interval': 1}
        result = check_firewall_psp(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

    def test_set_firewall_syslog(self):
        from jnpr.toby.firewall.Firewall import set_firewall_syslog
        logging.info("-----------Test set_firewall_syslog: -----------")

        ######################################################################
        logging.info("Test case 1: set firewall syslog successful with commit")
        param = {'activate': True, 'commit': 1, 'log_file': 'messages',
                 'log_level': 'info'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_syslog(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: set firewall syslog successful without commit")
        param = {'activate': True, 'log_file': 'messages', 'log_level': 'info'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_syslog(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: set firewall syslog unsuccessful with "
                     "incorrect response")
        param = {'commit': 1, 'log_file': 'messages', 'log_level': 'info'}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_syslog(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.check_filter_install')
    def test_set_firewall_filter(self, mock_chk_FW_install):
        from jnpr.toby.firewall.Firewall import set_firewall_filter
        logging.info("-----------Test set_firewall_filter: -----------")

        ######################################################################
        logging.info("Test case 1: Run with all valid params and "
                     "true response of config and commit")
        param = {'activate': 'set', 'interface': 'ge-2/0/2.1',
                 'family': 'inet', 'filter': 'filter',
                 'filter_name': 'ACCESS-CNTRL',
                 'if_specific': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with all valid params and "
                     "error response of config and commit")
        param = {'commit': 1,
                 'activate': 'set',
                 'interface': 'ge-2/0/2',
                 'filter': 'simple_filter',
                 'family': 'inet',
                 'output': 1, 'input': 0,
                 'chk_count': 1,
                 'filter_name': ['service_filter_example'],
                 'if_specific': 'if_specific'}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Run with all valid params and simple_filter")

        param = {'commit': 1, 'activate': 'set', 'interface': 'ge-2/0/2',
                 'filter': 'simple_filter', 'family': 'inet', 'chk_count': 1,
                 'input': 1, 'output': 0,
                 'filter_name': ['service_filter_example'],
                 'if_specific': 'if_specific'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with missmatch filter and "
                     "error response of config")
        param = {'commit': 1, 'interface': 'ge-2/0/2.1',
                 'family': 'inet', 'filter': 'service',
                 'input': 1, 'output': 0,
                 'filter_name': 'ACCESS-CNTRL',
                 'chk_count': 1, 'if_specific': True}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 5: Run with define output and valid response of config")

        param = {'commit': 1, 'interface': 'ge-2/0/2.1',
                 'family': 'inet', 'filter': 'service',
                 'input': 0, 'output': 1,
                 'filter_name': 'ACCESS-CNTRL',
                 'chk_count': 1, 'if_specific': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Run with simple-filter and error"
                     " response of config and define input")
        param = {'commit': 1, 'interface': 'ge-2/0/2.1',
                 'family': 'inet', 'filter': 'simple-filter',
                 'input': 1, 'output': 0,
                 'filter_name': 'ACCESS-CNTRL',
                 'chk_count': 1, 'if_specific': True}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Run with simple-filter and error"
                     " response of config and define output")
        param = {'commit': 1, 'interface': 'ge-2/0/2.1',
                 'family': 'inet', 'filter': 'simple-filter',
                 'input': 0, 'output': 1,
                 'filter_name': 'ACCESS-CNTRL',
                 'chk_count': 1, 'if_specific': True}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 8: Run with return false of check_firewall_install")
        mock_chk_FW_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 9: Run with return True of check_firewall_install")

        mock_chk_FW_install.return_value = True
        self.assertTrue(set_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 10: Run with error response of config"
                     " and missmath filter name")
        param = {'commit': 1, 'activate': 'set', 'interface': ['ge-2/0/2.1'],
                 'family': 'inet', 'filter': 'service', 'input': 1,
                 'filter_name': 'ACCESS-CNTRL',
                 'chk_count': 1, 'if_specific': True}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 11: Run with filter = service and define input")
        param = {'activate': 'set', 'interface': ['ge-2/0/2.1'],
                 'family': 'inet', 'filter': 'service', 'input': 1,
                 'filter_name': 'ACCESS-CNTRL',
                 'if_specific': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 12: Run with filter = filter and "
                     "not define input and output")
        param = {'commit': 1, 'activate': 'set', 'interface': ['ge-2/0/2.1'],
                 'family': 'inet', 'filter': 'filter', 'input': 0, 'output': 0,
                 'filter_name': 'ACCESS-CNTRL',
                 'chk_count': 1, 'if_specific': True}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.check_filter_install')
    def test_set_firewall_policer(self, mock_chk_FW_install):
        from jnpr.toby.firewall.Firewall import set_firewall_policer
        logging.info("-----------Test set_firewall_policer: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response of config and"
                     " commit and false check_firewall_install")
        param = {'commit': 1, 'family': 'inet', 'activate': 'set',
                 'interface': ['abc', 'xe-0/0/1.2'],
                 'policer': '1Mbps-policer',
                 'input': 1, 'output': 0, 'chk_count': 2}
        mock_chk_FW_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid response of config and"
                     " commit and true check_firewall_install")
        # Testcase 2:
        param = {'commit': 1, 'family': 'inet',
                 'interface': 'xe-0/0/1.2', 'policer': '1Mbps-policer',
                 'chk_count': 2}
        mock_chk_FW_install.return_value = True
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with error response of config")
        param = {'commit': 1, 'family': 'inet', 'activate': 'set',
                 'interface': 'xe-0/0/1.2', 'policer': '1Mbps-policer',
                 'input': 0, 'output': 1, 'chk_count': 2}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run without commit")
        param = {'family': 'inet', 'activate': 'set',
                 'interface': 'xe-0/0/1.2', 'policer': '1Mbps-policer',
                 'input': 1, 'output': 0}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.check_filter_install')
    def test_set_ftf_filter(self, mock_chk_FW_install):
        from jnpr.toby.firewall.Firewall import set_ftf_filter
        logging.info("-----------Test set_ftf_filter: -----------")

        ######################################################################
        logging.info(
            "Test case 1: configure ftf filter successfully with commit")
        param = {'commit': 1, 'family': 'inet', 'activate': 'set',
                 'filter': 'limit-source-one-24',
                 'routing_instance': 'FTF_FILTER',
                 'chk_count': 1, 'chk_interval': 1, 'interface': 'ge-0/0/2'}
        mock_chk_FW_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_ftf_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: configure ftf filter unsuccessfully"
                     " with incorrect command")
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_ftf_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: configure ftf filter successfully without commit")
        param = {'family': 'inet', 'activate': 'set',
                 'filter': 'limit-source-one-24', 'interface': 'ge-0/0/2'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_ftf_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: configure ftf filter successfully "
                     "with true check_firewall_install")
        param = {'commit': 1, 'family': 'inet', 'activate': 'set',
                 'filter': 'limit-source-one-24',
                 'routing_instance': 'FTF_FILTER',
                 'chk_count': 1, 'chk_interval': 1, 'interface': 'ge-0/0/2'}
        mock_chk_FW_install.return_value = True
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_ftf_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    def test_set_sampling(self):
        from jnpr.toby.firewall.Firewall import set_sampling
        logging.info("-----------Test set_sampling: -----------")

        ######################################################################
        logging.info("Test case 1: Run with commit True")
        param = {'interface': ['ge-0/0/0'], 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_sampling(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of config")
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(set_sampling(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: commit successfully with logical interface")
        param = {'interface': 'ge-0/0/0.1', 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_sampling(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with define input")
        # Testcase 4:
        param = {'interface': 'ge-0/0/0', 'commit': 1, 'input': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_sampling(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Run without commit and define output")
        param = {'interface': 'ge-0/0/0', 'output': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(set_sampling(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    def test_delete_firewall_syslog(self):
        from jnpr.toby.firewall.Firewall import delete_firewall_syslog
        logging.info("-----------Test delete_firewall_syslog: -----------")

        ######################################################################
        logging.info("Test case 1: Run with commit True")
        param = {'deactivate': 'deactivate', 'level': 'error',
                 'file': 'messages', 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_syslog(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of connfig")
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(delete_firewall_syslog(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run without commit")
        param = {'deactivate': 'deactivate',
                 'file': 'messages'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_syslog(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    def test_delete_firewall(self):
        from jnpr.toby.firewall.Firewall import delete_firewall
        logging.info("-----------Test delete_firewall: -----------")

        ######################################################################
        logging.info("Test case 1: Run with commit true")
        param = {'filter': 'filter-name',
                 'family': 'inet', 'term': 'term-name',
                 'deactivate': 'deactivate',
                 'commit': 1}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of config")
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(delete_firewall(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run without commit and filter name")
        param = {'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(delete_firewall(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run without commit only")
        param = {'filter': 'filter-name',
                 'family': 'inet', 'term': 'term-name',
                 'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.check_filter_install')
    def test_delete_firewall_filter(self, chk_fw_install):
        from jnpr.toby.firewall.Firewall import delete_firewall_filter
        logging.info("-----------Test delete_firewall_filter: -----------")

        ######################################################################
        logging.info(
            "Test case 1: delete firewall filter with list interface")
        param = {'filter': 'icmp_syslog',
                 'family': 'inet', 'interface': ['ge-0/0/2'],
                 'chk_count': 1, 'chk_interval': 1,
                 'if_specific': True, 'commit': 1,
                 'deactivate': 'deactivate'}
        chk_fw_install.return_value = True
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of config")
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(delete_firewall_filter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with single interface and "
                     "without commit and define input")
        param = {'filter': 'filter',
                 'family': 'invalid', 'interface': 'ge-0/0/2',
                 'input': True, 'chk_count': 1, 'chk_interval': 1,
                 'if_specific': 'if_specific',
                 }
        chk_fw_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with define output in params")
        param = {'filter': 'filter',
                 'family': 'invalid', 'interface': 'ge-0/0/2',
                 'output': 'output',
                 'if_specific': True, 'commit': 1,
                 'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 5: delete firewall filter with logical interface")
        param = {'filter': 'filter',
                 'family': 'inet', 'interface': 'ge-0/0/2.0',
                 'input': True, 'chk_count': 1, 'chk_interval': 1,
                 'if_specific': True, 'commit': 1,
                 'deactivate': 'deactivate'}
        chk_fw_install.return_value = True
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.check_filter_install')
    def test_delete_firewall_policer(self, chk_fw_install):
        from jnpr.toby.firewall.Firewall import delete_firewall_policer
        logging.info("-----------Test delete_firewall_policer: -----------")

        ######################################################################
        logging.info("Test case 1: Delete successfully with list interfaces")
        param = {'policer': 'policer', 'family': 'inet',
                 'interface': ['ge-2/0/7'], 'chk_count': 1, 'chk_interval': 1,
                 'commit': 1,
                 'deactivate': 'deactivate'}
        chk_fw_install.return_value = True
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Run with a single interface and without commit")
        param = {'policer': 'policer',
                 'family': 'invalid_name',
                 'interface': 'ge-2/0/7',
                 'deactivate': 'deactivate'}
        chk_fw_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: delete with param 'input' only")
        param = {'policer': 'policer',
                 'family': 'inet', 'input': True,
                 'interface': 'ge-2/0/7',
                 'chk_count': 1, 'chk_interval': 1,
                 'commit': 1}
        chk_fw_install.return_value = True
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(delete_firewall_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: delete with only param 'output'")
        param = {'policer': 'policer',
                 'family': 'inet',
                 'interface': 'ge-2/0/7', 'output': True,
                 'chk_count': 1, 'chk_interval': 1,
                 'commit': 1,
                 'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: delete with logical interface")
        param = {'policer': 'policer',
                 'family': 'inet',
                 'interface': 'ge-2/0/7.0', 'input': True,
                 'chk_count': 1, 'chk_interval': 1,
                 'commit': 1,
                 'deactivate': 'deactivate'}
        chk_fw_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: delete with logical interface and ouput")
        param = {'policer': 'policer',
                 'family': 'inet',
                 'interface': 'ge-2/0/7.0', 'output': True,
                 'chk_count': 1, 'chk_interval': 1,
                 'commit': 1,
                 'deactivate': 'deactivate'}
        chk_fw_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_firewall_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.check_filter_install')
    def test_delete_forwarding_table_filter(self, chk_fw_install):
        from jnpr.toby.firewall.Firewall import delete_forwarding_table_filter
        logging.info(
            "-----------Test delete_forwarding_table_filter: -----------")

        ######################################################################
        logging.info("Test case 1: Delete forwarding table filter "
                     "successfully with commit")
        param = {'filter': 'icmp_syslog', 'family': 'inet',
                 'routing_instance': 'abc', 'chk_count': 2,
                 'chk_interval': 1, 'commit': 1, 'deactivate': 'deactivate',
                 'interface': 'ge-0/0/2.0'}
        chk_fw_install.return_value = True
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_forwarding_table_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Delete forwarding table filter "
                     "successfully without commit ")
        param = {'filter': 'icmp_syslog', 'family': 'inet',
                 'deactivate': 'deactivate',
                 'interface': 'ge-0/0/2.0'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_forwarding_table_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Delete forwarding table filter "
                     "successfully with false return check_filter_install")
        param = {'filter': 'icmp_syslog', 'family': 'inet',
                 'routing_instance': 'abc', 'chk_count': 2,
                 'chk_interval': 1, 'commit': 1, 'deactivate': 'deactivate',
                 'interface': 'ge-0/0/2.0'}
        chk_fw_install.return_value = False
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_forwarding_table_filter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with error response of config")
        # Testcase 4: Delete forwarding table filter unsuccessfully
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(delete_forwarding_table_filter(self.jobject, **param),
                         "Return should be True")
        logging.info("\tPassed")

    def test_delete_sampling(self):
        from jnpr.toby.firewall.Firewall import delete_sampling
        logging.info("-----------Test delete_sampling: -----------")

        ######################################################################
        logging.info("Test case 1: delete sampling with physical interface")
        param = {'interface': 'ge-2/0/2', 'commit': 1, 'input': 1,
                 'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_sampling(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: delete sampling with logical interface")
        param = {'interface': 'ge-2/0/2.0', 'commit': 1, 'output': 1,
                 'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(delete_sampling(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with invalid interface")
        param = {'interface': 'invalid', 'commit': 1,
                 'deactivate': 'deactivate'}
        self.assertFalse(delete_sampling(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: delete sampling with list interface")
        param = {'interface': ['ge-2/0/2'], 'input': 1, 'output': 1,
                 'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(delete_sampling(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

    def test_clear_firewall_counter(self):
        from jnpr.toby.firewall.Firewall import clear_firewall_counter
        logging.info("-----------Test clear_firewall_counter: -----------")

        ######################################################################
        logging.info("Test case 1: Clear firewall with counter and"
                     " valid response of config")
        param = {'filter': 'filter', 'counter': 'counter'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(clear_firewall_counter(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Clear firewall with counter and"
                     " invalid response of config")
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(clear_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Clear firewall without counter")
        param = {'filter': 'filter'}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(clear_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Clear firewall all")
        param = {}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(clear_firewall_counter(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.set_dcu')
    def test_configure_protocol_dcu(self, mock_set_dcu):
        from jnpr.toby.firewall.Firewall import configure_protocol_dcu
        logging.info("-----------Test configure_protocol_dcu: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid config and commit true")
        mock_set_dcu.return_value = True
        param = {'name': 'dcu', 'interface': 'xe-1/1/0',
                 'protocol': 'vpls', 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_protocol_dcu(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid config and not commit")
        param = {'name': 'dcu', 'protocol': 'vpls'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_protocol_dcu(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with error response of config")

        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(configure_protocol_dcu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_set_dcu(self):
        from jnpr.toby.firewall.Firewall import set_dcu
        logging.info("-----------Test set_dcu: -----------")

        ######################################################################
        logging.info("Test case 1: Run with error response of config")
        param = {'interface': 'ge-0/0/1',
                 'family': 'inet'}
        self.jobject.get_version = MagicMock(return_value='15.1')
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])
        result = set_dcu(self.jobject, **param)

        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Run with valid response of config and commit")
        param = {'interface': 'ge-0/0/1',
                 'family': 'inet',
                 'commit': 1}
        self.jobject.get_version = MagicMock(return_value='15.1')
        self.jobject.config = MagicMock(
            side_effect=[Response(response="ok")])

        self.assertTrue(set_dcu(self.jobject, **param))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with list interface and without commit")
        param = {'interface': ['ge-0/0/1', 'ge-3/1/2.0'],
                 'family': 'inet'}
        self.jobject.get_version = MagicMock(return_value='5.4')
        self.jobject.config = MagicMock(side_effect=[Response(response="ok"),
                                                     Response(response="ok")])

        self.assertEqual(set_dcu(self.jobject, **param), None,
                         "Return should be None")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 1: Run with invalid response of config")
        param = {'interface': 'ge-0/0/1',
                 'family': 'inet'}
        self.jobject.get_version = MagicMock(return_value='5.4')
        self.jobject.config = MagicMock(
            side_effect=[Response(response="invalid")])

        self.assertFalse(set_dcu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_configure_rpf_feasible(self):
        from jnpr.toby.firewall.Firewall import configure_rpf_feasible
        logging.info("-----------Test configure_rpf_feasible: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Run with commit and valid response of config")
        param = {'commit': 1}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])

        self.assertTrue(configure_rpf_feasible(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Run without commit and error response of config")
        param = {}
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])

        self.assertFalse(configure_rpf_feasible(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Run without commit and valid response of config")
        param = {}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])

        self.assertEqual(configure_rpf_feasible(self.jobject, **param), None,
                         "Return should be None")
        logging.info("\tPassed")

    def test_delete_rpf_feasible(self):
        from jnpr.toby.firewall.Firewall import delete_rpf_feasible
        logging.info("-----------Test delete_rpf_feasible: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Run with commit and valid response of config")
        param = {'commit': 1}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])

        self.assertTrue(delete_rpf_feasible(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Run with deactivate and error response of config")
        param = {'deactivate': 'deactivate'}
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])

        self.assertFalse(delete_rpf_feasible(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run without commit and deactivate")
        param = {}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])

        self.assertEqual(delete_rpf_feasible(self.jobject, **param), None,
                         "Return should be False")
        logging.info("\tPassed")

    def test_set_rpf_check(self):
        from jnpr.toby.firewall.Firewall import set_rpf_check
        logging.info("-----------Test set_rpf_check: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Run with commit and valid response of config")
        param = {'loose_mode': 1,
                 'fail_filter': 'ACCESS-CNTRL',
                 'family': 'family',
                 'interface': 'ge-0/0/1',
                 'commit': 1}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])

        self.assertTrue(set_rpf_check(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of config")
        param = {'interface': 'ge-0/0/1.3'}
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])

        self.assertFalse(set_rpf_check(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with list interfaces")
        param = {'interface': ['ge-0/0/1.3', 'ge-0/0/2']}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok"),
                                                     Response(response="ok")])

        self.assertEqual(set_rpf_check(self.jobject, **param), None,
                         "Return should be None")
        logging.info("\tPassed")

    def test_delete_rpf_check(self):
        from jnpr.toby.firewall.Firewall import delete_rpf_check

        logging.info("-----------Test delete_rpf_check: -----------")
        ######################################################################
        logging.info("Test case 1: Run with list interfaces and commit")
        param = {'deactivate': 'delete',
                 'fail_filter': 'ACCESS-CNTRL',
                 'family': 'inet',
                 'interface': ['ge-0/0/1', 'ge-0/0/3.3'],
                 'commit': 1}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok"),
                                                     Response(response="ok")])
        self.assertTrue(delete_rpf_check(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with single interface and "
                     "error response of config")
        param = {'interface': 'ge-0/0/1.3'}
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])

        self.assertFalse(delete_rpf_check(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run without commit")
        param = {'deactivate': 'deactivate',
                 'fail_filter': 'ACCESS-CNTRL',
                 'interface': ['ge-0/0/1.3', 'ge-0/0/2']
                 }
        self.jobject.config = MagicMock(side_effect=[Response(response="ok"),
                                                     Response(response="ok")])
        self.assertEqual(delete_rpf_check(self.jobject, **param), None,
                         "Return should be None")
        logging.info("\tPassed")

    def test_delete_scu(self):
        from jnpr.toby.firewall.Firewall import delete_scu
        logging.info("-----------Test delete_scu: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response and commit true")
        res = '''
                Hostname: lab
                Model: mx240
                Junos: 13.3R1.4
                JUNOS Base OS boot [13.3R1.4]
                '''
        self.jobject.cli = MagicMock(side_effect=[Response(response=res)])
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])
        param = {'commit': 1, 'interface': 'ge-0/0/1.1',
                 'deactivate': 'deactivate', 'family': 'inet'}

        self.assertTrue(delete_scu(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of config")
        res = '''
                Hostname: lab
                Model: mx240
                JUNOS Base OS boot [13.3R1.4]
                '''
        self.jobject.cli = MagicMock(side_effect=[Response(response=res)])
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])
        param = {'commit': 1, 'interface': 'ge-0/0/1',
                 'deactivate': 'deactivate', 'family': 'inet'}

        self.assertFalse(delete_scu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run without commit and valid response")
        res = '''
                Hostname: lab
                Model: mx240
                Junos: 5.4R1.4
                JUNOS Base OS boot [13.3R1.4]
                '''
        self.jobject.cli = MagicMock(side_effect=[Response(response=res)])
        self.jobject.config = MagicMock(side_effect=[Response(response="ok"),
                                                     Response(response="ok")])
        param = {'interface': ['ge-0/0/1.1', 'ge-1/2/3'], 'family': 'inet'}
        self.assertEqual(delete_scu(self.jobject, **param), None,
                         "Return should be None")
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 4: Run with invaid response")
        res = '''
                Hostname: lab
                Model: mx240
                Junos: 5.4R1.4
                JUNOS Base OS boot [13.3R1.4]
                '''
        self.jobject.cli = MagicMock(side_effect=[Response(response=res)])
        self.jobject.config = MagicMock(
            side_effect=[Response(response="invalid"),
                         Response(response="invalid")])
        param = {'interface': ['ge-0/0/1.1', 'ge-1/2/3'], 'family': 'inet'}
        self.assertFalse(delete_scu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 5: Run without interfaces")
        param = {'commit': 1, 'family': 'inet'}
        self.assertFalse(delete_scu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_delete_dcu(self):
        from jnpr.toby.firewall.Firewall import delete_dcu

        logging.info("-----------Test delete_dcu: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response and commit true")
        self.jobject.get_version = MagicMock(return_value='15.4')
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])
        param = {'commit': "1", 'interface': 'ge-0/0/1.1',
                 'deactivate': 'deactivate', 'family': 'inet'}

        self.assertTrue(delete_dcu(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of config")
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])
        self.jobject.get_version = MagicMock(return_value='15.4')
        param = {'commit': 1, 'interface': 'ge-0/0/1',
                 'deactivate': 'deactivate', 'family': 'inet'}
        self.assertFalse(delete_dcu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Run with list interfaces and valid response")
        self.jobject.config = MagicMock(side_effect=[Response(response="ok"),
                                                     Response(response="ok")])
        self.jobject.get_version = MagicMock(return_value='5.4')
        param = {'interface': ['ge-0/0/1.1', 'ge-1/2/3'],
                 'family': 'inet'}
        self.assertEqual(delete_dcu(self.jobject, **param), None,
                         "Return should be None")
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 4: Run with invalid response of config")
        self.jobject.config = MagicMock(
            side_effect=[Response(response="invalid"),
                         Response(response="invalid")])
        self.jobject.get_version = MagicMock(return_value='5.4')
        param = {'interface': ['ge-0/0/1.1', 'ge-1/2/3'],
                 'family': 'inet'}
        self.assertFalse(delete_dcu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    @patch('jnpr.toby.firewall.Firewall.set_scu')
    def test_configure_protocol_scu(self, mock):
        from jnpr.toby.firewall.Firewall import configure_protocol_scu
        logging.info("-----------Test configure_protocol_scu: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response and commit true")
        param = {'name': 'scu',
                 'prot': 'vpls',
                 'commit': 1,
                 'interface': 'ge-1/2/3'}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])
        mock.return_value = True

        self.assertTrue(configure_protocol_scu(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run without commit")
        param = {'name': 'scu',
                 'prot': 'vpls'}
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])
        mock.return_value = True
        self.assertEqual(configure_protocol_scu(self.jobject, **param), None,
                         "Return should be None")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with error response of config")
        param = {'name': 'scu',
                 'prot': 'vpls'}
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])
        mock.return_value = True
        self.assertFalse(configure_protocol_scu(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_set_scu(self):
        from jnpr.toby.firewall.Firewall import set_scu
        logging.info("-----------Test set_scu: -----------")

        ######################################################################
        logging.info("Test case 1: Run with error response of config")
        param = {'interface': 'ge-0/0/1',
                 'family': 'inet'}
        self.jobject.get_version = MagicMock(return_value='15.1')
        self.jobject.config = MagicMock(
            side_effect=[Response(response="error")])
        result = set_scu(self.jobject, **param)

        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with valid response and commit true")
        param = {'interface': 'ge-0/0/1',
                 'family': 'inet',
                 'commit': 1}
        self.jobject.get_version = MagicMock(return_value='15.1')
        self.jobject.config = MagicMock(side_effect=[Response(response="ok")])
        self.jobject.commit = MagicMock()
        self.jobject.commit.status = MagicMock(side_effect=True)
        result = set_scu(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with valid response and without commit")
        param = {'interface': ['ge-0/0/1', 'ge-3/1/2.0'], 'family': 'inet'}
        self.jobject.get_version = MagicMock(return_value='5.4')
        self.jobject.config = MagicMock(side_effect=[Response(response="ok"),
                                                     Response(response="ok")])
        self.assertEqual(set_scu(self.jobject, **param), None,
                         "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with invalid response")
        param = {'interface': 'ge-0/0/1',
                 'family': 'inet'}
        self.jobject.get_version = MagicMock(return_value='5.4')
        self.jobject.config = MagicMock(
            side_effect=[Response(response="invalid")])
        result = set_scu(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

    def test_configure_three_color_policer(self):
        from jnpr.toby.firewall.Firewall import configure_three_color_policer
        logging.info(
            "-----------Test configure_three_color_policer: -----------")

        ######################################################################
        logging.info("Test case 1: Commit true with sigle-rate")
        param = {"policer_name": "abc", "rate_type": "single-rate",
                 "color_aware": 1, "committed_information_rate": "40m",
                 "committed_burst_size": "100k", "excess_burst_size": "100k",
                 "peak_information_rate": "60m", "peak_burst_size": "200k",
                 "action_discard": 1, "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertTrue(configure_three_color_policer(self.jobject, **param),
                        "Return should be True")

        param = {"policer_name": "abc", "rate_type": "single-rate",
                 "color_aware": 1, "committed_information_rate": "40m",
                 "committed_burst_size": "100k", "excess_burst_size": "100k",
                 "peak_information_rate": "60m", "peak_burst_size": "200k"}
        self.assertTrue(configure_three_color_policer(self.jobject, **param),
                        "Return should be True")

        param = {"policer_name": "abc", "rate_type": "two-rate",
                 "committed_information_rate": "40m",
                 "committed_burst_size": "100k", "excess_burst_size": "100k",
                 "peak_information_rate": "60m", "peak_burst_size": "200k",
                 "action_discard": 1, "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertTrue(configure_three_color_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with commit fail")
        param = {"policer_name": "abc", "rate_type": "two-rate",
                 "color_aware": 1, "committed_information_rate": "invalid",
                 "committed_burst_size": "100k", "excess_burst_size": "100k",
                 "peak_information_rate": "60m", "peak_burst_size": "200k",
                 "action_discard": 1, "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.jobject.commit = MagicMock(side_effect=Exception('error'))
        self.assertFalse(configure_three_color_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Don't specify CIR or CBS or EBS with single-rate")
        param = {"policer_name": "abc", "rate_type": "single-rate",
                 "color_aware": 1, "committed_information_rate": "",
                 "committed_burst_size": "100k", "excess_burst_size": "100k",
                 "peak_information_rate": 0, "peak_burst_size": 0,
                 "action_discard": 1, "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_three_color_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 4: Don't specify CIR or CBS or EBS with two-rate")
        param = {"policer_name": "abc", "rate_type": "two-rate",
                 "color_aware": 1, "committed_information_rate": "",
                 "committed_burst_size": "100k", "excess_burst_size": "100k",
                 "peak_information_rate": 0, "peak_burst_size": 0,
                 "action_discard": 1, "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_three_color_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: run with invalid_type")
        param = {"policer_name": "abc", "rate_type": "invalid_type",
                 "color_aware": 1, "committed_information_rate": "",
                 "committed_burst_size": "100k", "excess_burst_size": "100k",
                 "peak_information_rate": 0, "peak_burst_size": 0,
                 "action_discard": 1, "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_three_color_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_configure_hierarchical_policer(self):
        from jnpr.toby.firewall.Firewall import configure_hierarchical_policer
        logging.info(
            "-----------Test configure_hierarchical_policer: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Run type if-exceeding with valid configuration")
        param = {"policer_name": "test-1",
                 "aggr_limit_type": "if-exceeding",
                 "aggr_burst_size_limit": 1500,
                 "aggr_bandwidth_limit": "70m",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding",
                 "premium_burst_size_limit": 1500,
                 "premium_bandwidth_limit": "50m",
                 "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertTrue(configure_hierarchical_policer(self.jobject, **param),
                        "Return should be True")

        param = {"policer_name": "test-1",
                 "aggr_limit_type": "if-exceeding",
                 "aggr_burst_size_limit": 1500,
                 "aggr_bandwidth_limit": "70m",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding",
                 "premium_burst_size_limit": 1500,
                 "premium_bandwidth_limit": "50m",
                 "filter_specific": 1}
        self.assertTrue(configure_hierarchical_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Run type if-exceeding-pps with valid configuration")
        param = {"policer_name": "test-2",
                 "aggr_limit_type": "if-exceeding-pps",
                 "aggr_packet_burst": 1500,
                 "aggr_pps_limit": 70000,
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding-pps",
                 "premium_packet_burst": 1500,
                 "premium_pps_limit": 50000,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertTrue(configure_hierarchical_policer(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run type if-exceeding without "
                     "'if-exceeding' or 'if-exceeding-pps'")
        param = {"policer_name": "test-1",
                 "aggr_limit_type": "if-exceeding",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding",
                 "premium_burst_size_limit": 1500,
                 "premium_bandwidth_limit": "50m",
                 "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": True,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_hierarchical_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run type if-exceeding-pps without "
                     "packet-burst and pps-limit")
        param = {"policer_name": "test-2",
                 "aggr_limit_type": "if-exceeding-pps",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding-pps",
                 "premium_packet_burst": 1500,
                 "premium_pps_limit": 50000,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_hierarchical_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Run incorrect limit_type")
        param = {"policer_name": "test-1",
                 "aggr_limit_type": "abc",
                 "aggr_burst_size_limit": 1500,
                 "aggr_bandwidth_limit": "70m",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding",
                 "premium_burst_size_limit": 1500,
                 "premium_bandwidth_limit": "50m",
                 "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": True,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_hierarchical_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Run premium_limit_type without "
                     "burst-size-limit and bandwidth-limit")
        param = {"policer_name": "test-1",
                 "aggr_limit_type": "if-exceeding",
                 "aggr_burst_size_limit": 1500,
                 "aggr_bandwidth_limit": "70m",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding",
                 "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": True,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_hierarchical_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Run premium_limit_type: if-exceeding-pps "
                     "without packet-burst and pps-limit")
        param = {"policer_name": "test-1",
                 "aggr_limit_type": "if-exceeding",
                 "aggr_burst_size_limit": 1500,
                 "aggr_bandwidth_limit": "70m",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding-pps",
                 "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": True,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_hierarchical_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Run with incorrect premium_limit_type")
        param = {"policer_name": "test-1",
                 "aggr_limit_type": "if-exceeding",
                 "aggr_burst_size_limit": 1500,
                 "aggr_bandwidth_limit": "70m",
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "asfasdf",
                 "filter_specific": 1,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": True,
                 "shared_bandwidth_policer": 1}
        self.assertFalse(configure_hierarchical_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Run with Commit fail")
        param = {"policer_name": "test-2",
                 "aggr_limit_type": "if-exceeding-pps",
                 "aggr_packet_burst": 1500,
                 "aggr_pps_limit": 70000,
                 "aggr_then_actions": "discard,forwarding-class af,"
                 "loss-priority low",
                 "premium_limit_type": "if-exceeding-pps",
                 "premium_packet_burst": 1500,
                 "premium_pps_limit": 50000,
                 "logical_interface_policer": 1,
                 "physical_interface_policer": 1,
                 "shared_bandwidth_policer": 1}
        self.jobject.commit = MagicMock(side_effect=Exception('error'))
        self.assertFalse(configure_hierarchical_policer(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_configure_tunnel_end_point(self):
        from jnpr.toby.firewall.Firewall import configure_tunnel_end_point
        logging.info("-----------Test configure: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Configure tunnel end point successfully with commit")

        param = {'tunnel_name': 'sample_tunnel', 'transport_protocol': 'ipv4',
                 'encapsulation_protocol': 'gre',
                 'destination_address': '1.1.1.1',
                 'source_address': '2.2.2.2', 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_tunnel_end_point(self.jobject, **param),
                        "Return should be True")

        param = {'tunnel_name': 'sample_tunnel', 'transport_protocol': 'ipv4',
                 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertFalse(configure_tunnel_end_point(self.jobject, **param),
                         "Return should be False")

        param = {'tunnel_name': 'sample_tunnel', 'transport_protocol': 'ipv4',
                 'source_address': '2.2.2.2', 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_tunnel_end_point(self.jobject, **param),
                        "Return should be True")

        param = {'tunnel_name': 'sample_tunnel', 'logical_system': 'abc',
                 'transport_protocol': 'ipv4',
                 'destination_address': '2.2.2.2', 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_tunnel_end_point(self.jobject, **param),
                        "Return should be True")

        param = {'tunnel_name': 'sample_tunnel', 'logical_system': 'abc',
                 'commit': True}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_tunnel_end_point(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Configure tunnel end point "
                     "successfully without commit")

        param = {'tunnel_name': 'sample_tunnel', 'transport_protocol': 'ipv4',
                 'encapsulation_protocol': 'gre',
                 'destination_address': '1.1.1.1', 'source_address': '2.2.2.2'}
        self.jobject.config = MagicMock(return_value=Response(response=''))
        self.assertTrue(configure_tunnel_end_point(self.jobject, **param),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Configure tunnel end point unsuccessfully")
        param = {'tunnel_name': 'sample_tunnel', 'logical_system': 'L1',
                 'transport_protocol': 'ipv4',
                 'encapsulation_protocol': 'gre',
                 'destination_address': '1.1.1.1',
                 'source_address': '2.2.2.2', 'commit': True}
        self.jobject.config = MagicMock(
            return_value=Response(response='error'))
        self.assertFalse(configure_tunnel_end_point(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Configure tunnel end point unsuccessfully")
        param = {'tunnel_name': 'sample_tunnel', 'transport_protocol': 'ipv4',
                 'encapsulation_protocol': 'gre', 'commit': True}
        self.assertFalse(configure_tunnel_end_point(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

    def test_get_pfe_firewall_syslog(self):
        from jnpr.toby.firewall.Firewall import get_pfe_firewall_syslog
        logging.info("-----------Test get_pfe_firewall_syslog: -----------")

        ######################################################################
        logging.info("Test case 1: Run with valid response of cli")
        response = """
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.1513 A 05e9:0800 00:00:00:00:00:02 -> 00:00:00:00:00:08   61 101.1.1.1 101.1.1.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.513 A 0201:0800 00:00:00:00:00:01 -> 00:00:00:00:00:07   61 100.1.1.1 100.1.1.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.0   A 0007:0001:0800 00:00:00:00:00:05 -> 40:b4:f0:e2:b9:9c   61 20.20.20.2 21.21.21.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.2513 A 09d1:0800 00:00:00:00:00:03 -> 00:00:00:00:00:04   61 102.1.1.1 102.1.1.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP6_GEN: FW: xe-1/1/0.1   A 0002:86dd 00:00:00:00:00:06 -> 40:b4:f0:e2:b9:9c 59 SA 20:1:1:1:1:1:1:2  -> DA 21:1:1:1:1:1:1:2  (1 packets)
Jun 12 14:12:44 re0-sur02-cran7 fpc5 PFE_FW_SYSLOG_IP: FW: xe-5/1/0.0 A icmp 10.252.4.206 10.252.70.21 11 0 (2 packets)
Jun 12 14:12:45 re0-sur02-cran7 fpc5 PFE_FW_SYSLOG_IP: FW: xe-5/1/0.0 A icmp 10.252.4.206 10.252.70.21 11 0 (1 packets)
Mar 20 08:08:45 hostname feb FW: so-0/1/0.0   A icmp 192.168.207.222 192.168.207.223     0     0 (515 packets)
sdgsdgsdg hostname feb FW: bdfhffg   dgdfg icmp fhdfhf dfhdfh     0     0 (515 packets)
                    """
        self.jobject.cli = MagicMock(return_value=Response(response=response))
        param = {'file': 'Firewall', 'interface': 'xe-1/1/0.1',
                 'inner_vlan': '2', 'src_mac': '00:00:00:00:00:06',
                 'dst_mac': '40:b4:f0:e2:b9:9c',
                 'src_ip': '20:1:1:1:1:1:1:2', 'dst_ip': '21:1:1:1:1:1:1:2',
                 'ip_protocol': '59', 'from': '11:30:00', 'to': '11:35:00',
                 'action': 'A', 'count': 1}
        expected_result = [{'action': 'A', 'ip_protocol': '59',
                            'hostname': 'redium', 'inner_vlan': '2',
                            'time': '11:33:56', 'date': 'May 30',
                            'src_ip': '20:1:1:1:1:1:1:2',
                            'interface': 'xe-1/1/0.1',
                            'src_mac': '00:00:00:00:00:06',
                            'dst_mac': '40:b4:f0:e2:b9:9c',
                            'dst_ip': '21:1:1:1:1:1:1:2',
                            'ether_type': '86dd'}]
        result = get_pfe_firewall_syslog(self.jobject, **param)
        self.assertEqual(result, expected_result,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run with error response of cli")
        # Testcase 2 input is not correct
        param = {'file': 'Firewall', 'interface': 'xe-1/0/3',
                 'inner_vlan': '1', 'outer_vlan': '100', 'src_mac': 'abc',
                 'dst_mac': 'abc', 'src_ip': 'abc', 'dst_ip': 'abc',
                 'ip_protocol': 'abc', 'from': '15:15:00',
                 'to': '03:16:00', 'action': 'abc'}
        result = get_pfe_firewall_syslog(self.jobject, **param)
        self.assertEqual(len(result), 0, "Return is incorrect as expectation")

        self.jobject.cli = MagicMock(side_effect=Exception('error'))
        self.assertFalse(get_pfe_firewall_syslog(self.jobject, **param),
                         "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run with valid response of cli")
        response = """
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.1513 A 05e9:0800 00:00:00:00:00:02 -> 00:00:00:00:00:08   61 101.1.1.1 101.1.1.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.513 A 0201:0800 00:00:00:00:00:01 -> 00:00:00:00:00:07   61 100.1.1.1 100.1.1.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.0   A 0007:0001:0800 00:00:00:00:00:05 -> 40:b4:f0:e2:b9:9c   61 20.20.20.2 21.21.21.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP: FW: xe-1/1/0.2513 A 09d1:0800 00:00:00:00:00:03 -> 00:00:00:00:00:04   61 102.1.1.1 102.1.1.2     0     0 (1 packets)
May 30 11:34:22 [TRACE] [R0 redium] May 30 11:33:56  redium fpc1 PFE_FW_SYSLOG_ETH_IP6_GEN: FW: xe-1/1/0.1   A 0002:86dd 00:00:00:00:00:06 -> 40:b4:f0:e2:b9:9c 59 SA 20:1:1:1:1:1:1:2  -> DA 21:1:1:1:1:1:1:2  (1 packets)
Jun 12 14:12:44 re0-sur02-cran7 fpc5 PFE_FW_SYSLOG_IP: FW: xe-5/1/0.0 A icmp 10.252.4.206 10.252.70.21 11 0 (2 packets)
Jun 12 14:12:45 re0-sur02-cran7 fpc5 PFE_FW_SYSLOG_IP: FW: xe-5/1/0.0 A icmp 10.252.4.206 10.252.70.21 11 0 (1 packets)
Mar 20 08:08:45 hostname feb FW: so-0/1/0.0   A icmp 192.168.207.222 192.168.207.223     0     0 (515 packets)
sdgsdgsdg hostname feb FW: bdfhffg   dgdfg icmp fhdfhf dfhdfh     0     0 (515 packets)
                    """
        self.jobject.cli = MagicMock(return_value=Response(response=response))
        param = {'file': 'Firewall', 'interface': 'xe-1/1/0.1',
                 'inner_vlan': '2', 'src_mac': '00:00:00:00:00:06', 'count': 2,
                 'dst_mac': '40:b4:f0:e2:b9:9c', 'src_ip': '20:1:1:1:1:1:1:2',
                 'dst_ip': '21:1:1:1:1:1:1:2', 'ip_protocol': '59',
                 'from': '11:30:00', 'to': '11:35:00', 'action': 'A'}
        expected_result = [{'action': 'A', 'ip_protocol': '59',
                            'hostname': 'redium', 'inner_vlan': '2',
                            'time': '11:33:56', 'date': 'May 30',
                            'src_ip': '20:1:1:1:1:1:1:2',
                            'interface': 'xe-1/1/0.1',
                            'src_mac': '00:00:00:00:00:06',
                            'dst_mac': '40:b4:f0:e2:b9:9c',
                            'dst_ip': '21:1:1:1:1:1:1:2',
                            'ether_type': '86dd'}]
        result = get_pfe_firewall_syslog(self.jobject, **param)
        self.assertEqual(result, expected_result,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.firewall.Firewall.get_pfe_firewall_syslog')
    def test_check_pfe_firewall_syslog(self, mock, sleep_mock):
        from jnpr.toby.firewall.Firewall import check_pfe_firewall_syslog
        logging.info("-----------Test check_pfe_firewall_syslog: -----------")

        ######################################################################
        logging.info(
            "Test case 1: Run with valid response of get_pfe_firewall_syslog")
        mock.return_value = [{'action': 'A', 'ip_protocol': '05e9',
                              'date': 'May 30', 'inner_vlan': '1513',
                              'dst_mac': '00:00:00:00:00:08',
                              'time': '11:33:56', 'dst_ip': '101.1.1.2',
                              'ether_type': '0800', 'hostname': 'redium',
                              'interface': 'xe-1/1/0.1513',
                              'src_ip': '101.1.1.1',
                              'src_mac': '00:00:00:00:00:02'}]
        param = {'file': 'Firewall', 'interface': 'xe-1/1/0.1513',
                 'inner_vlan': '1513', 'src_mac': '00:00:00:00:00:02',
                 'dst_mac': '00:00:00:00:00:08', 'src_ip': '101.1.1.1',
                 'chk_count': 2, 'chk_interval': 1}
        result = check_pfe_firewall_syslog(self.jobject, **param)
        self.assertTrue(result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2:Run with invalid response of get_pfe_firewall_syslog")
        mock.return_value = {}
        param = {'file': 'Firewall', 'interface': 'xe-1/1/0.1513',
                 'inner_vlan': '1513', 'src_mac': '00:00:00:00:00:02',
                 'dst_mac': '00:00:00:00:00:08', 'src_ip': '101.1.1.1',
                 'chk_count': 2, 'chk_interval': 1}
        result = check_pfe_firewall_syslog(self.jobject, **param)
        self.assertFalse(result, "Return should be False")
        logging.info("\tPassed")

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name+".log", level=logging.INFO)
    unittest.main()

