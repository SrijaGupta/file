import unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import os
import logging
from jnpr.toby.utils.response import Response
from jnpr.toby.system.snmp.snmpkeywords import __kill_trapd as kill_trapd
from jnpr.toby.system.snmp.snmpkeywords import __auto_set_mibdirs as auto_set_mibdirs


@attr('unit')
class TestSnmpModule(unittest.TestCase):

    @patch('jnpr.toby.system.snmp.snmpkeywords.next')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_snmp_channel')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_snmp_get(self, patch_controller, patch_snmp_channel,
                      patch_next):
        logging.info("-----------Test snmp_get: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import snmp_get

        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        patch_snmp_channel.return_value.create_community_data = MagicMock()
        patch_snmp_channel.return_value.create_object_identity = MagicMock()
        patch_snmp_channel.return_value.snmpchannel = MagicMock()
        patch_snmp_channel.return_value.transport = MagicMock()
        patch_snmp_channel.return_value.invoke = MagicMock()
        ######################################################################
        logging.info("Test case 1: SNMP get successfully")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::sysUpTime'
        kwargs['index'] = '0'
        kwargs['snmp_channel_id'] = '12312'
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::sysUpTime.0'
        mock_val2.prettyPrint = MagicMock()
        mock_val2.prettyPrint.return_value = '20132343'
        patch_next.return_value = ['', '', '', [(mock_val1, mock_val2)]]
        dev_object = MagicMock()
        result = snmp_get(dev_object, **kwargs)
        self.assertEqual(result, {'SNMPv2-MIB::sysUpTime.0': '20132343'},
                         'Should be a dictionary')
        ######################################################################
        logging.info("Test case 2: SNMP get unsuccessfully with "
                     "No Such Instance currently exists at this OID")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::abc'
        kwargs['snmp_channel_id'] = '12312'
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::abc'
        mock_val2.prettyPrint = MagicMock()
        mock_val2.prettyPrint.return_value = 'No Such Instance currently'
        patch_next.return_value = ['', '', '', [(mock_val1, mock_val2)]]
        result = snmp_get(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 3: SNMP get unsuccessfully with "
                     "errorIndication")
        err_indication = MagicMock()
        err_indication.prettyPrint = MagicMock()
        err_indication.prettyPrint.return_value = 'Error retrieving MIBS'
        patch_next.return_value = [err_indication, '', 1,
                                   [(mock_val1, mock_val2)]]
        result = snmp_get(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 4: SNMP get unsuccessfully with "
                     "errorStatus")

        err_status = MagicMock()
        err_status.prettyPrint = MagicMock()
        err_status.prettyPrint.return_value = 'Error retrieving MIBS'
        patch_next.return_value = ['', err_status, 1, [(mock_val1, mock_val2)]]
        result = snmp_get(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')

    @patch('jnpr.toby.system.snmp.snmpkeywords.next')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_snmp_channel')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_snmp_set(self, patch_controller, patch_snmp_channel,
                      patch_next):
        logging.info("-----------Test snmp_set: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import snmp_set

        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        patch_snmp_channel.return_value.create_community_data = MagicMock()
        patch_snmp_channel.return_value.create_object_identity = MagicMock()
        patch_snmp_channel.return_value.snmpchannel = MagicMock()
        patch_snmp_channel.return_value.transport = MagicMock()
        patch_snmp_channel.return_value.invoke = MagicMock()
        ######################################################################
        logging.info("Test case 1: SNMP set successfully")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::sysContact'
        kwargs['index'] = '0'
        kwargs['value'] = 'test'
        kwargs['snmp_channel_id'] = '12312'
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::sysContact.0'
        mock_val2.prettyPrint = MagicMock()
        mock_val2.prettyPrint.return_value = 'test'
        patch_next.return_value = ['', '', '', [(mock_val1, mock_val2)]]
        dev_object = MagicMock()
        result = snmp_set(dev_object, **kwargs)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 2: SNMP set unsuccessfully with "
                     "No Such Instance currently exists at this OID")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::abc'
        kwargs['value'] = 'test'
        kwargs['snmp_channel_id'] = '12312'
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::abc'
        mock_val2.prettyPrint = MagicMock()
        mock_val2.prettyPrint.return_value = 'No Such Instance currently'
        patch_next.return_value = ['', '', '', [(mock_val1, mock_val2)]]
        result = snmp_set(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 3: SNMP set unsuccessfully with "
                     "errorIndication")
        err_indication = MagicMock()
        err_indication.prettyPrint = MagicMock()
        err_indication.prettyPrint.return_value = 'Error retrieving MIBS'
        patch_next.return_value = [err_indication, '', 1,
                                   [(mock_val1, mock_val2)]]
        result = snmp_set(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 4: SNMP set unsuccessfully with "
                     "errorStatus")

        err_status = MagicMock()
        err_status.prettyPrint = MagicMock()
        err_status.prettyPrint.return_value = 'Error retrieving MIBS'
        patch_next.return_value = ['', err_status, 1, [(mock_val1, mock_val2)]]
        result = snmp_set(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')

    @patch('jnpr.toby.system.snmp.snmpkeywords.next')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_snmp_channel')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_snmp_getnext(self, patch_controller, patch_snmp_channel,
                          patch_next):
        logging.info("-----------Test get_snmp_getnext: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import snmp_getnext

        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        patch_snmp_channel.return_value.create_community_data = MagicMock()
        patch_snmp_channel.return_value.create_object_identity = MagicMock()
        patch_snmp_channel.return_value.snmpchannel = MagicMock()
        patch_snmp_channel.return_value.transport = MagicMock()
        patch_snmp_channel.return_value.invoke = MagicMock()
        ######################################################################
        logging.info("Test case 1: SNMP getnext successfully")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::sysUpTime'
        kwargs['index'] = '0'
        kwargs['snmp_channel_id'] = '12312'
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::sysUpTime.0'
        mock_val2.prettyPrint = MagicMock()
        mock_val2.prettyPrint.return_value = '20132343'
        patch_next.return_value = ['', '', '', [(mock_val1, mock_val2)]]
        dev_object = MagicMock()
        result = snmp_getnext(dev_object, **kwargs)
        self.assertEqual(result, {'SNMPv2-MIB::sysUpTime.0': '20132343'},
                         'Should be a dictionary')
        ######################################################################
        logging.info("Test case 2: SNMP getnext unsuccessfully with "
                     "No Such Instance currently exists at this OID")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::abc'
        kwargs['snmp_channel_id'] = '12312'
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::abc'
        mock_val2.prettyPrint = MagicMock()
        mock_val2.prettyPrint.return_value = 'No Such Instance currently'
        patch_next.return_value = ['', '', '', [(mock_val1, mock_val2)]]
        result = snmp_getnext(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 3: SNMP getnext unsuccessfully with "
                     "errorIndication")
        err_indication = MagicMock()
        err_indication.prettyPrint = MagicMock()
        err_indication.prettyPrint.return_value = 'Error retrieving MIBS'
        patch_next.return_value = [err_indication, '', 1,
                                   [(mock_val1, mock_val2)]]
        result = snmp_getnext(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 4: SNMP getnext unsuccessfully with "
                     "errorStatus")

        err_status = MagicMock()
        err_status.prettyPrint = MagicMock()
        err_status.prettyPrint.return_value = 'Error retrieving MIBS'
        patch_next.return_value = ['', err_status, 1, [(mock_val1, mock_val2)]]
        result = snmp_getnext(dev_object, **kwargs)
        self.assertEqual(result, False, 'Should be False')

    @patch('jnpr.toby.system.snmp.snmpkeywords._get_snmp_channel')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_snmp_walk(self, patch_controller, patch_snmp_channel):
        logging.info("-----------Test snmp_walk: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import snmp_walk

        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        patch_snmp_channel.return_value.create_community_data = MagicMock()
        patch_snmp_channel.return_value.create_object_identity = MagicMock()
        patch_snmp_channel.return_value.snmpchannel = MagicMock()
        patch_snmp_channel.return_value.context_engine = MagicMock()
        patch_snmp_channel.return_value.context_name = MagicMock()
        patch_snmp_channel.return_value.transport = MagicMock()
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val2.prettyPrint = MagicMock()
        ######################################################################
        logging.info("Test case 1: SNMP walk successfully")
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::sysUpTime.0'
        mock_val2.prettyPrint.return_value = '20132343'
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, None, None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_walk(dev_object, **kwargs)
        self.assertEqual(result, {'SNMPv2-MIB::sysUpTime.0': '20132343'},
                         'Should be a dictionary')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: SNMP walk unsuccessfully with "
                     " No Such Instance currently")
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::sysUpTime.0'
        mock_val2.prettyPrint.return_value = 'No Such Instance currently'
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, None, None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_walk(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: SNMP walk unsuccessfully with errorIndication")
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[("Error", None, None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_walk(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 4: SNMP walk unsuccessfully with errorStatus")
        error_status = MagicMock()
        error_status.prettyPrint = MagicMock()
        error_status.prettyPrint.return_value = "Error"
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, error_status,
                           None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_walk(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 5: SNMP walk unsuccessfully with errorIndex")
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, None, "Error", [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_walk(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

    @patch('jnpr.toby.system.snmp.snmpkeywords._get_snmp_channel')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_snmp_bulkget(self, patch_controller, patch_snmp_channel):
        logging.info("-----------Test snmp_bulkget: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import snmp_bulkget

        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        patch_snmp_channel.return_value.create_community_data = MagicMock()
        patch_snmp_channel.return_value.create_object_identity = MagicMock()
        patch_snmp_channel.return_value.snmpchannel = MagicMock()
        patch_snmp_channel.return_value.context_engine = MagicMock()
        patch_snmp_channel.return_value.context_name = MagicMock()
        patch_snmp_channel.return_value.transport = MagicMock()
        mock_val1 = MagicMock()
        mock_val2 = MagicMock()
        mock_val1.prettyPrint = MagicMock()
        mock_val2.prettyPrint = MagicMock()
        ######################################################################
        logging.info("Test case 1: SNMP bulkget successfully")
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::sysUpTime.0'
        mock_val2.prettyPrint.return_value = '20132343'
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, None, None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_bulkget(dev_object, **kwargs)
        self.assertEqual(result, {'SNMPv2-MIB::sysUpTime.0': '20132343'},
                         'Should be a dictionary')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: SNMP bulkget unsuccessfully with "
                     " No Such Instance currently")
        mock_val1.prettyPrint.return_value = 'SNMPv2-MIB::sysUpTime.0'
        mock_val2.prettyPrint.return_value = 'No Such Instance currently'
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, None, None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_bulkget(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: SNMP bulkget unsuccessfully with errorIndication")
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[("Error", None, None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_bulkget(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 4: SNMP bulkget unsuccessfully with errorStatus")
        error_status = MagicMock()
        error_status.prettyPrint = MagicMock()
        error_status.prettyPrint.return_value = "Error"
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, error_status,
                           None, [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_bulkget(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 5: SNMP bulkget unsuccessfully with errorIndex")
        patch_snmp_channel.return_value.invoke = MagicMock(
            return_value=[(None, None, "Error", [(mock_val1, mock_val2)])])
        kwargs = {'oid': 'SNMPv2-MIB::sysUpTime', 'snmp_channel_id': '12312'}
        dev_object = MagicMock()
        result = snmp_bulkget(dev_object, **kwargs)
        self.assertFalse(result, 'Return should be False')
        logging.info("\tPassed")

    @patch('jnpr.toby.system.snmp.snmpkeywords.snmp_getnext')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_check_getnext(self, patch_controller, path_snmp_getnext):
        logging.info("-----------Test check_getnext: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import check_getnext
        dev_object = MagicMock()
        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        ######################################################################
        logging.info("Test case 1: SNMP check_getnext successfully")
        param = {'oid': "sysUpTime", 'index': '0', 'next_oid': "sysContact.0",
                 'value_expected': r'\w+'}
        path_snmp_getnext.return_value = {'SNMPv2-MIB::sysContact.0': 'abc'}
        result = check_getnext(dev_object, **param)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 2: SNMP check_getnext unsuccessfully")
        param = {'oid': "sysUpTime.0", 'next_oid': "sysContact.0",
                 'value_expected': '12345'}
        path_snmp_getnext.return_value = {'SNMPv2-MIB::sysContact.0': 'abc'}
        result = check_getnext(dev_object, **param)
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 3: SNMP check_getnext unsuccessfully with "
                     "an exception error when snmp getnext")
        param = {'oid': "sysUpTime.0", 'next_oid': "sysContact.0",
                 'value_expected': 'abc'}
        path_snmp_getnext.return_value = Exception('error')
        result = check_getnext(dev_object, **param)
        self.assertEqual(result, False, 'Should be False')

    @patch('jnpr.toby.system.snmp.snmpkeywords.snmp_walk')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_check_walk(self, patch_controller, patch_snmp_walk):
        logging.info("-----------Test check_walk: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import check_walk

        patch_controller.return_value.log = MagicMock()
        patch_snmp_walk.return_value = \
            {'SNMP-FRAMEWORK-MIB::snmpEngineBoots.0': '123',
             'SNMP-FRAMEWORK-MIB::snmpEngineTime.0': '456'}
        ######################################################################
        logging.info("Test case 1: SNMP check_walk successfully")
        check = {'oid': "SNMP-FRAMEWORK-MIB::snmpEngineBoots.0",
                 'community': "public"}
        value_expected = [{'variable': "SNMP-FRAMEWORK-MIB::snmpEngineBoots.0",
                           'value': '123'},
                          {'variable': "SNMP-FRAMEWORK-MIB::snmpEngineTime.0",
                           'value': '456'}]
        kwargs = {'value_expected': value_expected, 'check': check,
                  'oid': 'SNMP-FRAMEWORK-MIB::snmpEngineBoots.0'}
        dev_object = MagicMock()
        self.assertTrue(check_walk(dev_object, **kwargs),
                        'Return should be True')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: SNMP check_walk false with wrong value")
        check = {'oid': "SNMP-FRAMEWORK-MIB::snmpEngineBoots.0",
                 'community': "public"}
        value_expected = [{'variable': "SNMP-FRAMEWORK-MIB::snmpEngineBoots.0",
                           'value': '789'},
                          {'variable': "SNMP-FRAMEWORK-MIB::snmpEngineTime.0",
                           'value': '456'}]
        kwargs = {'value_expected': value_expected, 'check': check,
                  'oid': 'SNMP-FRAMEWORK-MIB::snmpEngineBoots.0'}
        dev_object = MagicMock()
        self.assertFalse(check_walk(dev_object, **kwargs),
                         'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: SNMP check_walk false "
                     "with missing value_expected")
        check = {'oid': "SNMP-FRAMEWORK-MIB::snmpEngineBoots.0",
                 'community': "public"}
        kwargs = {'check': check,
                  'oid': 'SNMP-FRAMEWORK-MIB::snmpEngineBoots.0'}
        dev_object = MagicMock()
        self.assertFalse(check_walk(dev_object, **kwargs),
                         'Return should be False')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: SNMP check_walk false "
                     "with exception when getting mibs")
        check = {'oid': "SNMP-FRAMEWORK-MIB::snmpEngineBoots.0",
                 'community': "public"}
        kwargs = {'check': check,
                  'oid': 'SNMP-FRAMEWORK-MIB::snmpEngineBoots.0'}
        dev_object = MagicMock()
        patch_snmp_walk.side_effect = Exception("error")
        self.assertFalse(check_walk(dev_object, **kwargs),
                         'Return should be False')
        logging.info("\tPassed")
    
    @patch('jnpr.toby.system.snmp.snmpkeywords.snmp_get')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_check_varbind(self, patch_controller, patch_snmp_get):
        logging.info("-----------Test check_varbind: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import check_varbind
        patch_controller.return_value.log = MagicMock()
        dev_object = MagicMock()
        ######################################################################
        logging.info("Test case 1: SNMP check_varbind successfully")
        patch_snmp_get.return_value = {'SNMPv2-MIB::sysContact.0': 'test'}
        param = {'varbind': {'oid': "SNMPv2-MIB::sysContact", 'version': 2,
                             'index': '0'}, 'value_expected': 'test'}
        result = check_varbind(dev_object, **param)
        self.assertEqual(result, True, 'Return should be True')
        ######################################################################
        logging.info("Test case 2: SNMP check_varbind unsuccessfully"
                     " with value_expected is not found")
        patch_snmp_get.return_value = {'SNMPv2-MIB::sysContact.0': 'test'}
        param = {'varbind': {'oid': "SNMPv2-MIB::sysContact", 'version': 2,
                             'index': '0'}, 'value_expected': 'abc'}
        result = check_varbind(dev_object, **param)
        self.assertEqual(result, False, 'Return should be False')
        ######################################################################
        logging.info("Test case 3: SNMP check_varbind unsuccessfully"
                     " with snmp_get failed")
        patch_snmp_get.return_value = False
        param = {'varbind': {'oid': "SNMPv2-MIB::sysContact", 'version': 2,
                             'index': '0'}, 'value_expected': 'abc'}
        result = check_varbind(dev_object, **param)
        self.assertEqual(result, False, 'Return should be False')
        ######################################################################
        logging.info("Test case 4: SNMP check_varbind false "
                     "with exception when getting mibs")
        param = {'varbind': {'oid': "SNMPv2-MIB::sysContact", 'version': 2,
                             'index': '0'}, 'value_expected': 'abc'}

        patch_snmp_get.side_effect = Exception("error")
        self.assertFalse(check_varbind(dev_object, **param),
                         'Return should be False')
        logging.info("\tPassed")



    def test_get_if_snmp_index(self):
        logging.info("-----------Test get_if_snmp_index: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import get_if_snmp_index
        dev_object = MagicMock()
        ######################################################################
        logging.info("Test case 1: Get interface snmp index successfully")
        response = """
Logical interface xe-0/0/0.1 (Index 3833) (SNMP ifIndex 3445) (Generation 3642)
Flags: Up SNMP-Traps 0x4000 VLAN-Tag [ 0x8100.1 ]  Encapsulation: ENET2
        """
        dev_object.cli = MagicMock(return_value=Response(response=response))
        result = get_if_snmp_index(dev=dev_object, interface='xe-0/0/0.1')
        self.assertEqual(result, '3445', 'Should not be False')
        ######################################################################
        logging.info("Test case 2: Get interface snmp index unsuccessfully"
                     " with response of cli command is empty")
        response = ""
        dev_object.cli = MagicMock(return_value=Response(response=response))
        result = get_if_snmp_index(dev=dev_object, interface='xe-0/0/0.1')
        self.assertEqual(result, False, 'Should be False')
        ######################################################################
        logging.info("Test case 3: Get interface snmp index unsuccessfully"
                     " with snmp index not found")
        response = "Logical interface xe-0/0/0.1 (Index 3833)"
        dev_object.cli = MagicMock(return_value=Response(response=response))
        result = get_if_snmp_index(dev=dev_object, interface='xe-0/0/0.1')
        self.assertEqual(result, False, 'Should be False')

    def test_kill_trapd(self):
        logging.info("-----------Test __kill_trapd: -----------")
        dev_object = MagicMock()
        ######################################################################
        logging.info("Test case 1: __kill_trapd successfully")
        response = "regress 40865   0.0  0.0   22680   2144  1  "\
            "S+   11:58PM     0:00.00 grep snmptrapd"
        dev_object.shell = MagicMock(return_value=Response(response=response))
        result = kill_trapd(dev_object)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 2: __kill_trapd unsuccessfully")
        response = ""
        dev_object.shell = MagicMock(return_value=Response(response=response))
        result = kill_trapd(dev_object, port=40865)
        self.assertEqual(result, False, 'Should be False')

    @patch('time.sleep', return_value=None)
    @patch('jnpr.toby.hldcl.channels.snmp.Snmp.get_trap_result')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_snmp_channel')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    @patch('jnpr.toby.system.snmp.snmpkeywords.__kill_trapd')
    def test_check_trap(self, patch_kill_trapd, patch_controller,
                        patch_snmp_channel, patch_get_trap_result,
                        patch_sleep):
        logging.info("-----------Test check_trap: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import check_trap
        dev_object = MagicMock()
        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        patch_snmp_channel.return_value.snmpchannel = MagicMock()
        patch_kill_trapd.return_value = True

        def test_trap():
            pass
        ######################################################################
        logging.info("Test case 1: SNMP check_trap successfully")
        patch_snmp_channel.return_value.get_trap_result = MagicMock(
            return_value='.1.3.6.1.2.1.14.16.2.0.2')
        result = check_trap(dev_object, test_trap, port=162,
                            config_trap=False, pattern='1.3.6.1.2',
                            time_end_trap=1)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 2: SNMP check_trap unsuccessfully")
        patch_snmp_channel.return_value.get_trap_result = MagicMock(
            return_value='.1.3.6.1.2.1.14.16.2.0.2')
        dev_object.config = MagicMock(return_value=Response(response=''))
        result = check_trap(dev_object, test_trap, port=162,
                            config_trap=True, trap_group='abc',
                            pattern=['abc', '123'], time_end_trap=1)
        self.assertEqual(result, False, 'Should be False')

    @patch('jnpr.toby.system.snmp.snmpkeywords.get_mibs_dir')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_snmp_channel')
    @patch('jnpr.toby.system.snmp.snmpkeywords._get_controller')
    def test_auto_set_mibdirs(self, patch_controller,
                              patch_snmp_channel, patch_get_mibs_dir):
        logging.info("-----------Test __kill_trapd: -----------")
        dev_object = MagicMock()
        patch_controller.return_value.log = MagicMock()
        patch_controller.return_value.host = MagicMock()
        patch_snmp_channel.return_value.mibs_dir = ''
        patch_snmp_channel.return_value.snmpchannel = MagicMock()
        ######################################################################
        logging.info("Test case 1: Auto set mibdirs successfully")
        patch_get_mibs_dir.return_value = "/volume/build/junos/15.1"\
            "/release/15.1F5-S3.6/src/junos/shared/mbs"
        result = auto_set_mibdirs(dev_object)
        self.assertEqual(result, '/volume/build/junos/15.1/release/15.1F5-'
                         'S3.6/src/junos/shared/mbs', 'Should not be Empty')
        ######################################################################
        logging.info("Test case 2: Auto set mibdirs unsuccessfully")
        patch_get_mibs_dir.return_value = ""
        result = auto_set_mibdirs(dev_object)
        self.assertEqual(result, '', 'Should be Empty')
        ######################################################################
        logging.info("Test case 3: Auto set mibdirs successfully")
        patch_snmp_channel.return_value.mibs_dir = '/volume/build/junos/'\
            '15.1/release/15.1F5-S3.6/src/junos/shared/mbs'
        patch_get_mibs_dir.return_value = ""
        result = auto_set_mibdirs(dev_object)
        self.assertEqual(result, '/volume/build/junos/15.1/release/15.1F5-'
                         'S3.6/src/junos/shared/mbs', 'Should not be Empty')

    def test_get_mibs_dir(self):
        logging.info("-----------Test get_mibs_dir: -----------")
        ######################################################################
        from jnpr.toby.system.snmp.snmpkeywords import get_mibs_dir
        dev_object = MagicMock()
        ######################################################################
        logging.info(
            "Test case 1: Get mibs dir successfully with ver = 9.0R1.4")
        dev_object.get_version = MagicMock(return_value="9.0R1.4")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/9.0/release/9.0R"\
            "1.4/src/juniper/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Get mibs dir successfully with ver = 9.6R1.4")
        dev_object.get_version = MagicMock(return_value="9.6R1.4")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/9.6/release/9.6R"\
            "1.4/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Get mibs dir successfully with ver = 8.6X1.4")
        dev_object.get_version = MagicMock(return_value="8.6X1.4")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/8.6/service/8.6X"\
            "1.4/src/juniper/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 4: Get mibs dir successfully with ver = 9.6X1.4")
        dev_object.get_version = MagicMock(return_value="9.6X1.4")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/9.6/service/9.6X"\
            "1.4/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Get mibs dir successfully "
                     "with ver = 13.3-4_ib56.7")
        dev_object.get_version = MagicMock(return_value="13.3-4_ib56.7")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/ib56/13.3/development"\
            "/4.7/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Get mibs dir successfully "
                     "with ver = 13.3-4_pr56.7")
        dev_object.get_version = MagicMock(return_value="13.3-4_pr56.7")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/pr56/13.3/"\
            "daily/4.7/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Get mibs dir successfully "
                     "with ver = 13.3-4_dev_56.7")
        dev_object.get_version = MagicMock(return_value="13.3-4_dev_56.7")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/dev_56/13.3/"\
            "development/4.7/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Get mibs dir successfully "
                     "with ver = 13.3-4_internal.7")
        dev_object.get_version = MagicMock(return_value="13.3-4_internal.7")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/13.3/daily"\
            "/current/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Get mibs dir successfully "
                     "with ver = 9.3-4_internal.7")
        dev_object.get_version = MagicMock(return_value="9.3-4_internal.7")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/9.3/daily/"\
            "current/src/juniper/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 10: Get mibs dir successfully "
                     "with ver = 13.3-4internal.7")
        dev_object.get_version = MagicMock(return_value="13.3-4internal.7")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/13.3/daily"\
            "/4.7/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 11: Get mibs dir successfully "
                     "with ver = 9.3-4internal.7")
        dev_object.get_version = MagicMock(return_value="9.3-4internal.7")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/9.3/daily/"\
            "4.7/src/juniper/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 12: Get mibs dir successfully with ver = 13.3I4-I5.6")
        dev_object.get_version = MagicMock(return_value="13.3I4-I5.6")
        result = get_mibs_dir(dev_object)
        expectation = "/volume/build/junos/13.3/daily/"\
            "current/src/junos/shared/mibs"
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 13: Get mibs dir successfully with"
                     " WB_TC_LOGGING and ver = 8.3ABC")
        dev_object.get_version = MagicMock(return_value="8.3ABC")
        os.environ['WB_TC_LOGGING'] = "test"
        expectation = None
        result = get_mibs_dir(dev_object)
        del os.environ['WB_TC_LOGGING']
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 14: Get mibs dir successfully "
                     "with WB_TC_LOGGING and ver = 8.3I 4-56-78 ")
        dev_object.get_version = MagicMock(return_value="8.3I 4-56-78 ")
        os.environ['WB_TC_LOGGING'] = "test"
        expectation = "/volume/regressions/JUNOS/CBR"\
            "/8.3/4-56-78/build/src/junos/shared/mibs"
        result = get_mibs_dir(dev_object)
        del os.environ['WB_TC_LOGGING']
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        #####################################################################
        logging.info(
            "Test case 15: Get mibs dir successfully with ver = 8.3R1.4")
        dev_object.get_version = MagicMock(return_value="8.3R1.4")
        expectation = "/volume/build/8.3R1.4/src/juniper/shared/mibs"
        result = get_mibs_dir(dev_object)
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        #####################################################################
        logging.info(
            "Test case 15: Get mibs dir successfully with ver = 8.3X1.4")
        dev_object.get_version = MagicMock(return_value="8.3X1.4")
        expectation = "/volume/build/8.3/current/src/juniper/shared/mibs"
        result = get_mibs_dir(dev_object)
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        #####################################################################
        logging.info(
            "Test case 16: Get mibs dir successfully with ver = 8.3-4K1.4")
        dev_object.get_version = MagicMock(return_value="8.3-4K1.4")
        expectation = "/volume/build/8.3/4.4/src/juniper/shared/mibs"
        result = get_mibs_dir(dev_object)
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 17: Get mibs dir successfully "
                     "with MIBDIRS in enviroment")
        dev_object.get_version = MagicMock(return_value="8.3-4K1.4")
        expectation = "test"
        os.environ['MIBDIRS'] = "test"
        result = get_mibs_dir(dev_object)
        del os.environ['MIBDIRS']
        self.assertEqual(result, expectation,
                         "Mib dir is incorrect as expectation")
        logging.info("\tPassed")

    def test_get_snmp_channel(self):
        controller = MagicMock()
        controller.channels = dict()
        controller.channels = {'snmp': {'1111': 'snmp handle to 1111'}}
        from jnpr.toby.system.snmp.snmpkeywords import _get_snmp_channel
        self.assertEqual(_get_snmp_channel(controller, '1111'),
                         'snmp handle to 1111')
        self.assertEqual(_get_snmp_channel(controller),
                         'snmp handle to 1111')
        snmp_exception = ''
        try:
            _get_snmp_channel(controller, '2222')
        except Exception as ex:
            snmp_exception = str(ex)
        self.assertEqual(snmp_exception, 'SNMP channel with ID 2222 not found')
        controller.channels = {'text': {'1111': 'text handle to 1111'}}
        snmp_exception = ''
        try:
            _get_snmp_channel(controller, '2222')
        except Exception as ex:
            snmp_exception = str(ex)
        self.assertEqual(snmp_exception,
                         'SNMP channel not present in controller')

    def test_get_controller(self):
        dev_obj = MagicMock()
        dev_obj.nodes = dict()
        controller_dict = {'re0': 're0 object for device'}
        dev_obj.nodes['primary'] = MagicMock()
        dev_obj.nodes['primary'].controllers = controller_dict
        dev_obj.current_node = MagicMock()
        dev_obj.current_node.current_controller = 're0 object for device'
        from jnpr.toby.system.snmp.snmpkeywords import _get_controller
        self.assertEqual(_get_controller(dev_obj, 'current', 'current'),
                         're0 object for device')
        self.assertEqual(_get_controller(dev_obj, 'primary', 're0'),
                         're0 object for device')
        # Negative testing
        controller_dict = {'re1': 're1 object for device'}
        dev_obj.nodes['primary'].controllers = controller_dict
        snmp_exception = ''
        try:
            _get_controller(dev_obj, 'primary', 're0')
        except Exception as ex:
            snmp_exception = str(ex)
        self.assertEqual(snmp_exception, 'Controller re0 does not exist for '
                         'the device in node primary ')
        snmp_exception = ''
        try:
            _get_controller(dev_obj, 'member1', 're0')
        except Exception as ex:
            snmp_exception = str(ex)
        self.assertEqual(snmp_exception, 'System Node member1 does not exist '
                         'for the device')

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name+".log", level=logging.INFO)
    unittest.main()