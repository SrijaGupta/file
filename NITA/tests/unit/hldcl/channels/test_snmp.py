import unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import logging, os
from pyasn1.codec.ber import decoder
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pysnmp.hlapi import *

@attr('unit')
class TestSnmpModule(unittest.TestCase):
   
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.channels.snmp.UdpTransportTarget')
    @patch('jnpr.toby.hldcl.channels.snmp.SnmpEngine')
    def test_snmp_init(self, patch_snmp_engine, patch_udp):
        from jnpr.toby.hldcl.channels.snmp import Snmp
        snmp_attributes = {'host':'router1'}
        snmp_obj = Snmp(snmp_attributes)
        self.assertIsInstance(snmp_obj, Snmp)
        self.assertEqual(snmp_obj.timeout, 60)
        self.assertEqual(snmp_obj.community, 'public')
        self.assertEqual(snmp_obj.version, 2)
        self.assertEqual(snmp_obj.group, None)
        self.assertEqual(patch_udp.call_count, 1)

    def test_invoke(self):
        dev_handle = MagicMock()
        from jnpr.toby.hldcl.channels.snmp import Snmp
        snmp_handle = MagicMock(spec=Snmp)
        rv = Snmp.invoke(snmp_handle, dev_handle,'ContextData')
        self.assertEqual(dev_handle.log.call_count, 1)
        from pysnmp.hlapi.context import ContextData
        self.assertIsInstance(rv, ContextData)
        snmp_exception = ''
        try:
            rv = Snmp.invoke(snmp_handle, dev_handle, 'dummycommand')
        except Exception as ex:
            snmp_exception = str(ex)
        self.assertEqual(snmp_exception,'Method dummycommand not implemented')

    @patch('pysnmp.hlapi.CommunityData')
    @patch('pysnmp.hlapi.UsmUserData')
    def test_create_community_data(self, patch_usm_user_data, patch_communi_data):
        from jnpr.toby.hldcl.channels.snmp import Snmp
        logging.info("-----------Test create_community_data: -----------")
        ######################################################################
        snmp_handle = MagicMock(spec=Snmp)
        snmp_handle.handle = MagicMock()
        snmp_handle.version = 1
        snmp_handle.user = 'abc'
        snmp_handle.auth_type = 'usmHMACSHAAuthProtocol'
        snmp_handle.auth_pass = 'abc'
        snmp_handle.priv_type = 'usmAesCfb128Protocol'
        snmp_handle.priv_pass = 'abc'
        snmp_handle.community = 'abc'
        patch_usm_user_data.return_value = True
        patch_communi_data.return_value = True
        ######################################################################
        logging.info("Test case 1: create_community_data with version 1 successfully")
        kwargs = dict()
        kwargs['community'] = 'public'
        kwargs['version'] = 1
        result = Snmp.create_community_data(snmp_handle, **kwargs)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 2: create_community_data with version 2 "
                     "successfully")
        kwargs = dict()
        kwargs['community'] = 'public'
        kwargs['version'] = 2
        result = Snmp.create_community_data(snmp_handle, **kwargs)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 3: create_community_data with version 3 "
                     "successfully with usmNoPrivProtocol and usmHMACMD5AuthProtocol")
        kwargs = dict()
        kwargs['community'] = 'public'
        kwargs['version'] = 3
        kwargs['priv_type'] = 'usmNoPrivProtocol'
        kwargs['auth_pass'] = 'usmHMACMD5AuthProtocol'
        result = Snmp.create_community_data(snmp_handle, **kwargs)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 4: create_community_data with version 3 "
                     "successfully with usm3DESEDEPrivProtocol")
        kwargs = dict()
        kwargs['community'] = 'public'
        kwargs['version'] = 3
        kwargs['priv_type'] = 'usm3DESEDEPrivProtocol'
        kwargs['auth_pass'] = 'usmHMACMD5AuthProtocol'
        result = Snmp.create_community_data(snmp_handle, **kwargs)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 5: create_community_data with version 3 "
                     "successfully with usmNoPrivProtocol")
        kwargs = dict()
        kwargs['community'] = 'public'
        kwargs['version'] = 3
        kwargs['priv_type'] = 'usmNoPrivProtocol'
        result = Snmp.create_community_data(snmp_handle, **kwargs)
        self.assertEqual(result, True, 'Should be True')
        ######################################################################
        logging.info("Test case 6: create_community_data with invalid version")
        kwargs['version'] = 4
        with self.assertRaises(Exception) as context:
            Snmp.create_community_data(snmp_handle, **kwargs)
        self.assertTrue('Invalid Version' in str(context.exception),
                        "an exception should be raised")

    @patch('pysnmp.hlapi.ObjectIdentity')
    def test_create_object_identity(self, patch_oid):
        from jnpr.toby.hldcl.channels.snmp import Snmp
        logging.info("-----------Test create_object_identity: -----------")
        snmp_handle = MagicMock(spec=Snmp)
        snmp_handle.handle = MagicMock()
        snmp_handle.mibs_dir = 'abc'
        snmp_handle.mibs_custom_dir = 'test'
        from pysnmp.hlapi import ObjectType
        ######################################################################
        logging.info("Test case 1: create_object_identity successfully")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::sysUpTime'
        patch_oid.return_value = MagicMock()
        rv = Snmp.create_object_identity(snmp_handle, **kwargs)
        self.assertIsInstance(rv, ObjectType)
        ######################################################################
        logging.info("Test case 2: create_object_identity successfully"
                     " for snmp set")
        kwargs = dict()
        kwargs['oid'] = 'SNMPv2-MIB::sysUpTime.0'
        kwargs['value'] = 'test'
        patch_oid.return_value = MagicMock()
        rv = Snmp.create_object_identity(snmp_handle, **kwargs)
        self.assertIsInstance(rv, ObjectType)
        ######################################################################
        logging.info("Test case 3: create_object_identity successfully"
                     " with oid is a string of numbers")
        kwargs = dict()
        kwargs['oid'] = '1.3.6.1.4.1.2636.3.1.1.0'
        kwargs['value'] = 'test'
        patch_oid.return_value = MagicMock()
        rv = Snmp.create_object_identity(snmp_handle, **kwargs)
        self.assertIsInstance(rv, ObjectType)

        ######################################################################
        logging.info("Test case 4: create_object_identity successfully with"
                     "oid = sysUpTime")
        kwargs = dict()
        kwargs['oid'] = 'sysUpTime'
        kwargs['value'] = 'test'

        with patch('pysnmp.smi.rfc1902.ObjectIdentity.resolveWithMib') as res_mib:
            with patch('pysnmp.smi.rfc1902.ObjectIdentity.getOid') as get_oid:
                get_oid.return_value.asTuple = MagicMock()
                rv = Snmp.create_object_identity(snmp_handle, **kwargs)
        self.assertIsInstance(rv, ObjectType)

    @patch('jnpr.toby.hldcl.channels.snmp.SnmpEngine')
    def test_get_snmp_id(self, patch_snmp_engine):
        from jnpr.toby.hldcl.channels.snmp import Snmp
        logging.info("-----------Test get_snmp_id: -----------")
        ######################################################################
        snmp_handle = MagicMock(spec=Snmp)
        snmp_handle.snmpchannel = MagicMock()
        snmp_handle.snmpchannel.snmpEngineID._value.decode = MagicMock(
            return_value='1594914942379179')
        result = Snmp.get_snmp_id(snmp_handle)
        self.assertEqual(result, '1594914942379179', 'Should be True')
'''
   # NOTE : the below test is making S2C hung!, hence commenting it for now to unblock S2C move testing..
    def test_get_trap_result(self):
        from jnpr.toby.hldcl.channels.snmp import Snmp
        logging.info("-----------Test get_trap_result: -----------")
        ######################################################################
        def send_test_trap():
            errorIndication, errorStatus, errorIndex, varBinds = next(
                sendNotification(
                SnmpEngine(),
                CommunityData('public'),
                UdpTransportTarget(('localhost', 1585)),
                ContextData(),
                'trap',
                NotificationType(
                    ObjectIdentity('1.3.6.1.6.3.1.1.5.2')
                ).addVarBinds(
                    ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.2'),
                    ('1.3.6.1.2.1.1.1.0', OctetString('my system'))
                )
            )
        )
            errorIndication, errorStatus, errorIndex, varBinds = next(
                sendNotification(
                    SnmpEngine(),
                    CommunityData('public', mpModel=0),
                    UdpTransportTarget(('localhost', 1585)),
                    ContextData(),
                    'trap',
                    NotificationType(
                        ObjectIdentity('1.3.6.1.6.3.1.1.5.3')
                    ).addVarBinds(
                        ('1.3.6.1.6.3.1.1.4.3.0', '1.3.6.1.4.1.20408.4.1.1.3'),
                        ('1.3.6.1.2.1.1.1.0', OctetString('ENDTRAP'))
                    )
                )
            )
            errorIndication, errorStatus, errorIndex, varBinds = next(
                sendNotification(
                    SnmpEngine(),
                    UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
                    UdpTransportTarget(('localhost', 1585)),
                    ContextData(),
                    'trap',
                    NotificationType(
                        ObjectIdentity('1.3.6.1.6.3.1.1.5.4')
                    ).addVarBinds(
                        ('1.3.6.1.6.3.1.1.4.3.54', '1.3.6.1.4.1.20408.4.1.1.4'),
                        ('1.3.6.1.2.1.1.1.0', OctetString('interface down'))
                    )
                )
            )

        dict = {}
        snmp_handle = Snmp(dict)
        ######################################################################
        logging.info("Test case 1: get_trap_result with pattern_end_trap")
        result = Snmp.get_trap_result(snmp_handle, send_test_trap,
                                      pattern_end_trap='ENDTRAP',
                                      timeout=300, port=1585,
                                      time_end_trap=None)
        self.assertEqual(type(result), str)
        ######################################################################
        logging.info("Test case 2: get_trap_result with time_end_trap")
        result = Snmp.get_trap_result(snmp_handle, send_test_trap,
                                      pattern_end_trap=None,
                                      timeout=300, port=1585, time_end_trap=2)
        self.assertEqual(type(result), str)
        ######################################################################
        logging.info("Test case 3: get_trap_result with pattern_end_trap is "
                     "not match and time_end_trap is None")
        result = Snmp.get_trap_result(snmp_handle, send_test_trap,
                                      pattern_end_trap='abc', timeout=10,
                                      port=1585, time_end_trap=None)
        self.assertEqual(type(result), str)
'''

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name+".log", level=logging.INFO)
    unittest.main()
