'''
Created on Feb 21, 2017

@author: Terralogic VN
'''
import os
import unittest
import logging
from mock import MagicMock
from mock import patch
import xml.etree.ElementTree as ET

from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.juniper.jpg.jpg import Jpg
from jnpr.toby.hldcl.juniper.jpg.jpg import set_jpg_interfaces
from jnpr.toby.hldcl.juniper.jpg.jpg import connect_to_jpg_device
from jnpr.toby.hldcl.juniper.jpg.jpg import configure_jpg
from jnpr.toby.hldcl.juniper.jpg.jpg import configure_jpg_replication
from jnpr.toby.hldcl.juniper.jpg.jpg import setup_jpg_filter
from jnpr.toby.hldcl.juniper.jpg.jpg import attach_jpg_filter
from jnpr.toby.hldcl.juniper.jpg.jpg import get_jpg_stats


class test_jpg(unittest.TestCase):

    @patch('jnpr.toby.hldcl.juniper.junos.Juniper.__init__')
    def setUp(self, mock_Juniper):
        logging.info("\n##################################################\n")
        logging.info("Initializing mock device handle.............\n")
#         MagicMock(spec=Juniper)
        mock_Juniper.return_value = MagicMock(return_value=None)
        self.jobject = Jpg(os='junos')
        import builtins
        builtins.t = self
        t.log = MagicMock()

    def tearDown(self):
        logging.info("Close mock device handle session ...........\n")

    def test_configure_jpg(self):
        ######################################################################
        logging.info("Test case 1: run with null  inout_intf_rep_pair")
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        self.jobject._Jpg__get_ingress_egress_interfaces = MagicMock()
        self.jobject.inout_intf_pair = ['fe-0/1/2|ge-1/2/3',
                                        'fe-0/1/2|xe-1/2/3']
        self.jobject.inout_intf_rep_pair = []
        self.jobject._Jpg__reset_jpg_config = MagicMock()
        self.jobject._Jpg__configure_jpg_bridge = MagicMock()
        self.jobject._Jpg__configure_jpg_replication = MagicMock()
        result = self.jobject.configure_jpg()

        self.assertEqual(result, True, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: run with valid  inout_intf_rep_pair ...")
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        self.jobject._Jpg__get_ingress_egress_interfaces = MagicMock()
        self.jobject.inout_intf_pair = ['fe-0/1/2|ge-1/2/3',
                                        'fe-0/1/2|xe-1/2/3']
        self.jobject.inout_intf_rep_pair = [
            'fe-0/1/2|ge-1/2/3', 'fe-0/1/2|xe-1/2/3']
        self.jobject._Jpg__reset_jpg_config = MagicMock()
        self.jobject._Jpg__configure_jpg_bridge = MagicMock()
        self.jobject._Jpg__configure_jpg_replication = MagicMock()
        result = self.jobject.configure_jpg()

        self.assertEqual(result, True, "Return should be True")
        logging.info("\tPassed")

    def test__get_ingress_egress_interfaces(self):
        ######################################################################
        logging.info("Test case 1: run with valid interface ...")
        self.jobject.inout_intf_rep_pair = []
        self.jobject.inout_intf_pair = []
        self.jobject.interfaces = {
                    'fe': {
                        'jpg-bridge-name': 'x_bridge_name',
                        'pic': 'fe_pic',
                        'jpg-replication-factor': 'fe_x_factor'},
                    'ge': {
                        'jpg-bridge-name': 'x_bridge_name',
                        'pic': 'ge_pic',
                        'jpg-replication-factor': ''}}
        self.jobject.log = MagicMock()
        self.jobject._Jpg__get_ingress_egress_interfaces()
        self.assertEqual(len(self.jobject.inout_intf_pair), 1,
                         "inout_intf_pair array is incorrect")
        self.assertEqual(len(self.jobject.inout_intf_rep_pair), 1,
                         "inout_intf_rep_pair array is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: run without replication-factor")
        self.jobject.inout_intf_rep_pair = []
        self.jobject.inout_intf_pair = []
        self.jobject.interfaces = {
                    'fe': {
                        'jpg-bridge-name': 'x_bridge_name',
                        'pic': 'fe_pic',
                        'jpg-replication-factor': ''},
                    'ge': {
                        'jpg-bridge-name': 'x_bridge_name',
                        'pic': 'ge_pic',
                        'jpg-replication-factor': ''}}
        self.jobject.log = MagicMock()
        self.jobject.channels = [] #Used within TobyException class when Exception thrown
        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__get_ingress_egress_interfaces()
        self.assertTrue('jpg-replication-factor is a mandatory knob that' in str(context.exception))

        self.assertEqual(len(self.jobject.inout_intf_pair), 0,
                         "inout_intf_pair array is incorrect")
        self.assertEqual(len(self.jobject.inout_intf_rep_pair), 0,
                         "inout_intf_rep_pair array is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: run with bridge name missmatch")
        self.jobject.inout_intf_rep_pair = []
        self.jobject.inout_intf_pair = []
        self.jobject.interfaces = {
                    'fe': {
                        'jpg-bridge-name': 'bridge1',
                        'pic': 'fe_pic',
                        'jpg-replication-factor': 'abc'},
                    'ge': {
                        'jpg-bridge-name': 'bridge2',
                        'pic': 'ge_pic',
                        'jpg-replication-factor': ''}}
        self.jobject.log = MagicMock()
        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__get_ingress_egress_interfaces()
        self.assertTrue('BRIDGE NAME did not match for'
                        in str(context.exception))

        self.assertEqual(len(self.jobject.inout_intf_pair), 0,
                         "inout_intf_pair array is incorrect")
        self.assertEqual(len(self.jobject.inout_intf_rep_pair), 0,
                         "inout_intf_rep_pair array is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: run with invalid bridge name")
        self.jobject.inout_intf_rep_pair = []
        self.jobject.inout_intf_pair = []
        self.jobject.interfaces = {
                    'fe': {
                        'jpg-bridge-name': '',
                        'pic': 'fe_pic',
                        'jpg-replication-factor': 'abc'},
                    'ge': {
                        'jpg-bridge-name': '',
                        'pic': 'ge_pic',
                        'jpg-replication-factor': ''}}
        self.jobject.log = MagicMock()
        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__get_ingress_egress_interfaces()
        self.assertTrue('Either jpg-bridge-name or pic is'
                        in str(context.exception))

        self.assertEqual(len(self.jobject.inout_intf_pair), 0,
                         "inout_intf_pair array is incorrect")
        self.assertEqual(len(self.jobject.inout_intf_rep_pair), 0,
                         "inout_intf_rep_pair array is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: run with invalid interface")
        self.jobject.inout_intf_rep_pair = []
        self.jobject.inout_intf_pair = []
        self.jobject.interfaces = {
                    '': {
                        'jpg-bridge-name': 'bridge1',
                        'pic': 'fe_pic',
                        'jpg-replication-factor': 'abc'},
                    '': {
                        'jpg-bridge-name': 'bridge1',
                        'pic': 'ge_pic',
                        'jpg-replication-factor': ''}}
        self.jobject.log = MagicMock()
        self.jobject._Jpg__get_ingress_egress_interfaces()

        self.assertEqual(len(self.jobject.inout_intf_pair), 0,
                         "inout_intf_pair array is incorrect")
        self.assertEqual(len(self.jobject.inout_intf_rep_pair), 0,
                         "inout_intf_rep_pair array is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: run with multiple pairs")
        self.jobject.inout_intf_rep_pair = []
        self.jobject.inout_intf_pair = []
        self.jobject.interfaces = {
            'ge-4/2/1': {
                'jpg-bridge-name': 'r0-rt0',
                'pic': 'ge-4/2/1'},
            'ge-4/2/2': {
                'jpg-bridge-name': 'r0-rt0',
                'jpg-replication-factor': 1,
                'pic': 'ge-4/2/2'},
            'ge-4/2/3': {
                'jpg-bridge-name': 'r0-rt1',
                'jpg-replication-factor': 1,
                'pic': 'ge-4/2/3'},
            'ge-4/2/4': {
                'jpg-bridge-name': 'r0-rt1',
                'pic': 'ge-4/2/4'},
            'ge-4/2/5': {
                'jpg-bridge-name': 'r0-rt2',
                'pic': 'ge-4/2/5'},
            'ge-4/2/6': {
                'jpg-bridge-name': 'r0-rt2',
                'jpg-replication-factor': 1,
                'pic': 'ge-4/2/6'},
            'ge-4/2/8': {
                'jpg-bridge-name': 'r0-rt3',
                'pic': 'ge-4/2/8'},
            'ge-4/2/7': {
                'jpg-bridge-name': 'r0-rt3',
                'jpg-replication-factor': 1,
                'pic': 'ge-4/2/7'}
            }
        self.jobject.inout_intf_pair = ['ge-4/2/6|ge-4/2/5']
        self.jobject.inout_intf_rep_pair = ['ge-4/2/6,1|ge-4/2/5,']
        self.jobject.log = MagicMock()
        self.jobject._Jpg__get_ingress_egress_interfaces()

        self.assertEqual(len(self.jobject.inout_intf_pair), 4,
                         "inout_intf_pair array is incorrect")
        self.assertEqual(len(self.jobject.inout_intf_rep_pair), 4,
                         "inout_intf_rep_pair array is incorrect")
        logging.info("\tPassed")

    def test___reset_jpg_config(self,):
        ######################################################################
        logging.info("Testcase 1: run with valid inout_intf_pair and response")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_pair = ['ge-2/0/3|xe-4/1/7']
        self.jobject.shell = MagicMock()
        res1 = "set bridge-domains bd_ge2_0_3_xe4_1_7 interface ge-2/0/3.0"
        res2 = "set bridge-domains bd_ge2_0_3_xe4_1_7 interface xe-4/1/7.0"
        res3 = '''set bridge-domains bd_ge2_0_3_xe4_1_7 interface ge-2/0/3.0
set bridge-domains bd_ge2_0_3_xe4_1_7 interface xe-4/1/7.0
abc

'''
        res4 = '''set bridge-domains bd_ge2_0_3_xe4_1_7 interface ge-2/0/3.0
set bridge-domains bd_ge2_0_3_xe4_1_7 interface xe-4/1/7.0
abc

'''
        self.jobject.cli = MagicMock(side_effect=[Response(response=res1),
                                                  Response(response=res2),
                                                  Response(response=res3),
                                                  Response(response=res4),
                                                  ])
#         jobject.config = MagicMock(side_effect=True)
        self.jobject.config = MagicMock(
            side_effect=[Response(response=""),
                         Response(response=""),
                         Response(response=""),
                         Response(response="<name>bd_ge2_0_3_xe4_1_7</name>"),
                         Response(response="Count: 4 lines"),
                         Response(response="")
                         ])

        result = self.jobject._Jpg__reset_jpg_config()
        self.assertEqual(result, False, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 2: run with invalid response")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_pair = ['ge-2/0/3|xe-4/1/7']
        self.jobject.shell = MagicMock()
        res = "set bridge-domains bd_ge2_0_3_xe4_1_7 interface xe-4/1/7.0"
        self.jobject.cli = MagicMock(side_effect=[Response(response=""),
                                                  Response(response=res),
                                                  Response(response=""),
                                                  ])
        self.jobject.config = MagicMock(side_effect=[Response(response=""),
                                                     Response(response=""),
                                                     Response(response=""),
                                                     Response(response="test"),
                                                     Response(response="test"),
                                                     Response(response="")
                                                     ])

        result = self.jobject._Jpg__reset_jpg_config()
        self.assertEqual(result, False, "Return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 3: run with invalid res of cli ")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_pair = ['ge-2/0/3|xe-4/1/7']
        self.jobject.shell = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  ])
        self.jobject.config = MagicMock(
            side_effect=[Response(response=""),
                         Response(response=""),
                         Response(response=""),
                         Response(response="<name>bd_ge2_0_3_xe4_1_7</name>"),
                         Response(response="test"),
                         Response(response="")
                         ])

        result = self.jobject._Jpg__reset_jpg_config()
        self.assertEqual(result, False, "return shoud be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 4: run with valid inout_intf_pair " +
                     " and commit successful")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_pair = ['ge-2/0/3|xe-4/1/7']
        self.jobject.shell = MagicMock()
        res1 = "set bridge-domains bd_ge2_0_3_xe4_1_7 interface ge-2/0/3.0"
        res2 = "set bridge-domains bd_ge2_0_3_xe4_1_7 interface xe-4/1/7.0"
        res3 = '''set bridge-domains bd_ge2_0_3_xe4_1_7 interface ge-2/0/3.0
set bridge-domains bd_ge2_0_3_xe4_1_7 interface xe-4/1/7.0
abc

'''
        res4 = '''set bridge-domains bd_ge2_0_3_xe4_1_7 interface ge-2/0/3.0
set bridge-domains bd_ge2_0_3_xe4_1_7 interface xe-4/1/7.0
abc

'''
        self.jobject.cli = MagicMock(side_effect=[Response(response=res1),
                                                  Response(response=res2),
                                                  Response(response=res3),
                                                  Response(response=res4),
                                                  ])
#         jobject.config = MagicMock(side_effect=True)
        self.jobject.config = MagicMock(
            side_effect=[Response(response=""),
                         Response(response=""),
                         Response(response=""),
                         Response(response="<name>bd_ge2_0_3_xe4_1_7</name>"),
                         Response(response="Count: 4 lines"),
                         Response(response="")
                         ])
        self.jobject.commit = MagicMock(return_value=Response(response=True))
        result = self.jobject._Jpg__reset_jpg_config()
        self.assertEqual(result, True, "Return should be True")
        logging.info("\tPassed")


    def test__configure_jpg_bridge(self):
        ######################################################################
        logging.info("Testcase 1: run with commit True")
        self.jobject.inout_intf_pair = ['fe-0/1/2|ge-1/2/3',
                                        'fe-0/1/2|xe-1/2/3']
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(return_value=Response(response=""))
        self.jobject.config = MagicMock()
        self.jobject.commit = MagicMock(return_value=Response(response=True))
        self.assertTrue(self.jobject._Jpg__configure_jpg_bridge(),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 2: run with commit error")
        self.jobject.inout_intf_pair = ['fe-0/1/2|ge-1/2/3',
                                        'fe-0/1/2|xe-1/2/3']
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        self.jobject.config = MagicMock()
        self.jobject.commit = MagicMock(side_effect=Exception('error'))
        self.assertNotEqual(self.jobject._Jpg__configure_jpg_bridge(), True,
                            "Return should not be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 3: run with valid response of cli")
        self.jobject.inout_intf_pair = ['fe-0/1/2|ge-1/2/3',
                                        'fe-0/1/2|xe-1/2/3']
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(return_value=Response(response="config"))
        self.jobject.config = MagicMock()
        self.jobject.commit = MagicMock(return_value=Response(response=True))
        self.assertTrue(self.jobject._Jpg__configure_jpg_bridge(),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 4: Run with null inout_intf_pair")
        self.jobject.inout_intf_pair = []
        self.jobject.log = MagicMock()
        self.assertTrue(self.jobject._Jpg__configure_jpg_bridge(),
                        "Return should be True")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    def test__configure_jpg_replication(self, patched_time_sleep):
        ######################################################################
        logging.info("Testcase 1: run with valid res and commit true")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_rep_pair = ['xe-4/1/3,1|xe-5/3/1,']
        self.jobject.inout_intf_pair = ['xe-4/1/3|xe-5/3/1']
        int_up = '''
<rpc-reply>
    <interface-information>
        <physical-interface>
            <name>xe-4/1/3</name>
            <admin-status>up</admin-status>
            <oper-status>up</oper-status>
            <speed>10Gbps</speed>
        </physical-interface>
    </interface-information>
</rpc-reply>
'''
        res = ET.fromstring(int_up)
        cli_flood = '''
Bridging domain: bd_xe5_3_1_xe4_1_3
Flood Routes:
  Prefix    Type          Owner                 NhType          NhIndex
  0x3000f/51 FLOOD_GRP_COMP_NH __all_ces__      comp            807
  0x3000e/51 FLOOD_GRP_COMP_NH __re_flood__     comp            754
'''
        cli_ver = '''
Hostname: scbe2-jpg
Model: mx480
Junos: 13.3R4.6
'''
        shell_cprod = '''
807(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
    751(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
        724(Unicast, BRIDGE, ifl:387:xe-5/3/1.0, pfe-id:21)
        720(Unicast, BRIDGE, ifl:385:xe-4/1/3.0, pfe-id:16)
'''
        self.jobject.config = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[
                                             Response(response=cli_flood),
                                             Response(response=cli_ver)
                                             ])
        self.jobject.commit = MagicMock(side_effect=[Response(response=""),
                                                     Response(response=""),
                                                     Response(response=""),
                                                     Response(response=True)
                                                     ])
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res), Response(response=res),
                         Response(response=res), Response(response=res)])
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=""), Response(response=shell_cprod),
                         Response(response=""), Response(response="")])
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        self.jobject._Jpg__get_intf_nhid = MagicMock(side_effect=[1, 1])

        result = self.jobject._Jpg__configure_jpg_replication()
        self.assertEqual(result, True, "return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 2: run with valid res and commit error")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_rep_pair = ['xe-4/1/3,a|xe-5/3/1,']
        self.jobject.inout_intf_pair = ['xe-4/1/3|xe-5/3/1']
        int_up = '''
<rpc-reply>
    <interface-information>
        <physical-interface>
            <name>xe-4/1/3</name>
            <admin-status>up</admin-status>
            <oper-status>up</oper-status>
            <speed>10Gbps</speed>
        </physical-interface>
    </interface-information>
</rpc-reply>
'''
        int_down = '''
<rpc-reply>
    <interface-information>
        <physical-interface>
            <name>xe-4/1/3</name>
            <admin-status>down</admin-status>
            <oper-status>down</oper-status>
            <speed>10Gbps</speed>
        </physical-interface>
    </interface-information>
</rpc-reply>
'''
        res = ET.fromstring(int_up)
        res1 = ET.fromstring(int_down)
        cli_flood = '''
Bridging domain: bd_xe5_3_1_xe4_1_3
Flood Routes:
  Prefix    Type          Owner                 NhType          NhIndex
  0x3000f/51 FLOOD_GRP_COMP_NH __all_ces__      comp            807
  0x3000e/51 FLOOD_GRP_COMP_NH __re_flood__     comp            754
'''
        cli_ver = '''
Hostname: scbe2-jpg
Model: mx808
Junos: 13.3R4.6
'''
        shell_cprod = '''
807(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
    751(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
        724(Unicast, BRIDGE, ifl:387:xe-5/3/1.0, pfe-id:21)
        720(Unicast, BRIDGE, ifl:385:xe-4/1/3.0, pfe-id:16)
'''
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res1), Response(response=res1),
                         Response(response=res), Response(response=res),
                         Response(response=res), Response(response=res)])
        self.jobject.config = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=""),
                                                  Response(response=cli_flood),
                                                  Response(response=cli_ver)])
        self.jobject.commit = MagicMock(side_effect=[Response(response=""),
                                                     Response(response=""),
                                                     Response(response=""),
                                                     Exception("error")])
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=""), Response(response=shell_cprod),
                         Response(response=""), Response(response="")])
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        self.jobject._Jpg__get_intf_nhid = MagicMock(side_effect=[1, 1])

        result = self.jobject._Jpg__configure_jpg_replication()
        self.assertEqual(result, False, "return should be False")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 3: run with interface down")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_rep_pair = ['xe-4/1/3,a|xe-5/3/1,']
        self.jobject.inout_intf_pair = ['xe-4/1/3|xe-5/3/1']
        int_down = '''
<rpc-reply>
    <interface-information>
        <physical-interface>
            <name>xe-4/1/3</name>
            <admin-status>down</admin-status>
            <oper-status>down</oper-status>
            <speed>10Gbps</speed>
        </physical-interface>
    </interface-information>
</rpc-reply>
'''
        res1 = ET.fromstring(int_down)

        self.jobject.get_rpc_equivalent = MagicMock()
        list_response = []
        for i in range(1, 21):
            list_response.append(Response(response=res1))
        self.jobject.execute_rpc = MagicMock(side_effect=list_response)
        self.jobject.config = MagicMock()
        self.jobject.cli = MagicMock()
        self.jobject.commit = MagicMock()
        self.jobject.shell = MagicMock()
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        self.jobject._Jpg__get_intf_nhid = MagicMock(side_effect=[1, 1])
        self.jobject._Jpg__reset_jpg_config = MagicMock()
        self.jobject.channels = [] #Used when TobyException is raised
        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__configure_jpg_replication()
        self.assertTrue('One or more Interfaces are down' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 4: run with interfaces != down")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_rep_pair = ['xe-4/1/3,a|xe-5/3/1,']
        self.jobject.inout_intf_pair = ['xe-4/1/3|xe-5/3/1']
        int_down = '''
<rpc-reply>
    <interface-information>
        <physical-interface>
            <name>xe-4/1/3</name>
            <admin-status>flap</admin-status>
            <oper-status>flap</oper-status>
            <speed>10Gbps</speed>
        </physical-interface>
    </interface-information>
</rpc-reply>
'''
        res1 = ET.fromstring(int_down)

        self.jobject.get_rpc_equivalent = MagicMock()
        list_response = []
        for i in range(1, 21):
            list_response.append(Response(response=res1))
        self.jobject.execute_rpc = MagicMock(side_effect=list_response)
        self.jobject.config = MagicMock()
        self.jobject.cli = MagicMock()
        self.jobject.commit = MagicMock()
        self.jobject.shell = MagicMock()
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        self.jobject._Jpg__get_intf_nhid = MagicMock(side_effect=[1, 1])
        self.jobject._Jpg__reset_jpg_config = MagicMock()

        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__configure_jpg_replication()
        self.assertTrue('One or more Interfaces '
                        'are down' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 5: run with Unable to get the "
                     "nhindex for route-flood-group")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_rep_pair = ['xe-4/1/3,a|xe-5/3/1,']
        self.jobject.inout_intf_pair = ['xe-4/1/3|xe-5/3/1']
        int_up = '''
<rpc-reply>
    <interface-information>
        <physical-interface>
            <name>xe-4/1/3</name>
            <admin-status>up</admin-status>
            <oper-status>up</oper-status>
            <speed>10Gbps</speed>
        </physical-interface>
    </interface-information>
</rpc-reply>
'''
        res = ET.fromstring(int_up)
        cli_flood = '''
Bridging domain: bd_xe5_3_1_xe4_1_3
Flood Routes:
  Prefix    Type          Owner                 NhType          NhIndex
  0x3000e/51 FLOOD_GRP_COMP_NH __re_flood__     comp            754
'''
        cli_ver = '''
Hostname: scbe2-jpg
Model: mx480
Junos: 13.3R4.6
'''
        shell_cprod = '''
807(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
    751(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
        724(Unicast, BRIDGE, ifl:387:xe-5/3/1.0, pfe-id:21)
        720(Unicast, BRIDGE, ifl:385:xe-4/1/3.0, pfe-id:16)
'''
        self.jobject.config = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[
                                             Response(response=cli_flood),
                                             Response(response=cli_ver)
                                             ])
        self.jobject.commit = MagicMock(side_effect=[Response(response=""),
                                                     Response(response=""),
                                                     Response(response=""),
                                                     Response(response=True)])
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res), Response(response=res),
                         Response(response=res), Response(response=res)])
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=""), Response(response=shell_cprod),
                         Response(response=""), Response(response="")])
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        self.jobject._Jpg__get_intf_nhid = MagicMock(side_effect=[1, 1])

        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__configure_jpg_replication()
        self.assertTrue('Unable to get the nhindex for '
                        'route-flood-group' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 6: run with Unable to get Next-Hop Id")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_rep_pair = ['xe-4/1/3,1|xe-5/3/1,']
        self.jobject.inout_intf_pair = ['xe-4/1/3|xe-5/3/1']
        int_up = '''
<rpc-reply>
    <interface-information>
        <physical-interface>
            <name>xe-4/1/3</name>
            <admin-status>up</admin-status>
            <oper-status>up</oper-status>
            <speed>10Gbps</speed>
        </physical-interface>
    </interface-information>
</rpc-reply>
'''
        res = ET.fromstring(int_up)
        cli_flood = '''
Bridging domain: bd_xe5_3_1_xe4_1_3
Flood Routes:
  Prefix    Type          Owner                 NhType          NhIndex
  0x3000f/51 FLOOD_GRP_COMP_NH __all_ces__      comp            807
  0x3000e/51 FLOOD_GRP_COMP_NH __re_flood__     comp            754
'''
        cli_ver = '''
Hostname: scbe2-jpg
Model: mx480
Junos: 13.3R4.6
'''
        shell_cprod = '''
807(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
    751(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)

'''
        self.jobject.config = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[
                                             Response(response=cli_flood),
                                             Response(response=cli_ver)
                                             ])
        self.jobject.commit = MagicMock(side_effect=[Response(response=""),
                                                     Response(response=""),
                                                     Response(response=""),
                                                     Response(response=True)])
        self.jobject.get_rpc_equivalent = MagicMock()
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=res), Response(response=res),
                         Response(response=res), Response(response=res)])
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=""), Response(response=shell_cprod),
                         Response(response=""), Response(response="")])
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        self.jobject._Jpg__get_intf_nhid = MagicMock(side_effect=[1, 1])

        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__configure_jpg_replication()
        self.assertTrue('Unable to get Next-Hop Id' in str(context.exception))
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.Jpg._Jpg__jpg_replication_module')
    def test_jpg_replication(self, mock):
        ######################################################################
        logging.info("Test case 1: __jpg_replication_module return True")
        self.jobject.log = MagicMock()
        self.jobject._Jpg__jpg_replication_module = MagicMock(
            side_effect=[True, True])
        result = Jpg.jpg_replication([self.jobject, self.jobject])

        self.assertTrue(result, "Fail in execute function")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: __jpg_replication_module return Exception")
        self.jobject.log = MagicMock()
        self.jobject._Jpg__jpg_replication_module = MagicMock(
            side_effect=[True, Exception("Unable to get inner ids. ")])

        try:
            Jpg.jpg_replication([self.jobject, self.jobject])
        except Exception as exp:
            self.assertEqual(exp.args[0], 'Fail to execute JPG replication module on all devices')
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.Jpg._Jpg__get_intf_nhid')
    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.Jpg._Jpg__get_ingress_egress_interfaces')
    def test__jpg_replication_module(self, intf_nhid, pair_inft_rep):
        ######################################################################
        logging.info("Test case 1: Verify function when it returns True")
        self.jobject.log = MagicMock()
        self.jobject.inout_intf_rep_pair = ['ge-2/0/2,a|xe-4/2/5,b']
        intf_nhid.return_value = "123"
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx480
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Speed: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "regress"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        actual_result = self.jobject._Jpg__jpg_replication_module()

        self.assertTrue(actual_result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Verify function when no nhindex is found")
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = ""
        cli_res2 = ""
        cli_res3 = ""
        cli_res4 = ""
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = ""
        shell_res2 = ""
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = None
        actual_result = self.jobject._Jpg__jpg_replication_module()

        self.assertTrue(actual_result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 3: Verify function when model is mx80 or mx 104")
        self.jobject.inout_intf_rep_pair = ['ge-2/0/2,1|xe-4/2/5,']
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx80
        Junos: 13.3R4.6

        '''
        cli_res3 = '''
        Link-level type: Ethernet-Bridge, MTU: 9192,
            MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None,
            MAC-REWRITE Error: None, Loopback: None,
        '''
        cli_res4 = '''
        Link-level type: Ethernet-Bridge, MTU: 9192,
            MRU: 9200, Speed: 1000mbps, BPDU Error: None,
            MAC-REWRITE Error: None, Loopback: Disabled,
        '''
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "regress"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = "123"
        actual_result = self.jobject._Jpg__jpg_replication_module()

        self.assertTrue(actual_result, "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 4: Verify function when able to get inner ids")
        intf_nhid.return_value = ""
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx80
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Speed: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "regress"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res3),
                         Response(response=shell_res3)])

        self.assertTrue(self.jobject._Jpg__jpg_replication_module(),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: User is root")
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx480
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Speed: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "root"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = "123"

        self.assertTrue(self.jobject._Jpg__jpg_replication_module(),
                        "Return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Format of interface does not contain -")
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx480
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Speed: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "root"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = "123"
        actual_result = self.jobject._Jpg__jpg_replication_module()

        self.assertTrue(actual_result, "Fail in execute function")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Get model failed")
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Speed: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "regress"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = "123"
        with self.assertRaises(UnboundLocalError) as context:
            self.jobject._Jpg__jpg_replication_module()
        self.assertTrue("local variable 'model' referenced before "
                        "assignment" in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: cprod_cmd returns unexpected value")
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx480
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Speed: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "regress"
        shell_res2 = 'aaa'
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = "123"
        self.jobject.channels = []  #used for TobyException class

        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__jpg_replication_module()
        self.assertTrue('Unable to get inner ids' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Run with valid replication factor")
        self.jobject.inout_intf_rep_pair = ['ge-2/0/2,a|xe-4/2/5,b']
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx480
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Sped: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Speed: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "regress"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = "123"

        with self.assertRaises(UnboundLocalError) as context:
            self.jobject._Jpg__jpg_replication_module()
        self.assertTrue("local variable 'link_speed_p2' referenced "
                        "before assignment" in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 10: Cannot get Ingress speed")
        self.jobject.inout_intf_rep_pair = ['ge2/0/2,a|xe-4/2/5,']
        self.jobject.log = MagicMock()
        self.jobject.su = MagicMock()
        cli_res1 = '''Name: default-switch
        CEs: 15
        VEs: 0
        Bridging domain: bd_ge2_0_2_xe4_2_5
        Flood Routes:
          Prefix    Type          Owner                 NhType          NhIndex
          0x30003/51 FLOOD_GRP_COMP_NH __all_ces__      comp            883
          0x30002/51 FLOOD_GRP_COMP_NH __re_flood__     comp            879

        '''
        cli_res2 = '''Hostname: scbe2-jpg
        Model: mx480
        Junos: 13.3R4.6

        '''
        cli_res3 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: None,"
        cli_res4 = "Link-level type: Ethernet-Bridge, MTU: 9192, " +\
            "MRU: 9200, Sped: 1000mbps, BPDU Error: None, " +\
            "MAC-REWRITE Error: None, Loopback: Disabled,"
        self.jobject.cli = MagicMock(side_effect=[Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4),
                                                  Response(response=cli_res1),
                                                  Response(response=cli_res2),
                                                  Response(response=cli_res3),
                                                  Response(response=cli_res4)])
        shell_res1 = "regress"
        shell_res2 = '''
        883(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
        870(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
            863(Unicast, BRIDGE, ifl:340:xe-4/2/5.0, pfe-id:17)
            861(Unicast, BRIDGE, ifl:334:ge-2/0/2.0, pfe-id:8)
        '''
        shell_res3 = ""
        self.jobject.shell = MagicMock(
            side_effect=[Response(response=shell_res1),
                         Response(response=shell_res2),
                         Response(response=shell_res3),
                         Response(response=shell_res2),
                         Response(response=shell_res3)])
        intf_nhid.return_value = "123"

        with self.assertRaises(UnboundLocalError) as context:
            self.jobject._Jpg__jpg_replication_module()
        self.assertTrue("local variable 'link_speed_p1' referenced "
                        "before assignment" in str(context.exception))
        logging.info("\tPassed")

    def test_setup_jpg_filter(self):
        ######################################################################
        logging.info("Testcase 1: run without filter")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        result = self.jobject.setup_jpg_filter(**param)

        self.assertFalse(result, "Return should be False")
        self.assertEqual(len(self.jobject.term_array), 0,
                         "term_array is not none")
        self.assertEqual(len(self.jobject.jpg_config), 0,
                         "jpg_config is not none")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 2: run without term_name")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        result = self.jobject.setup_jpg_filter(**param)

        self.assertFalse(result, "Return should be False")
        self.assertEqual(len(self.jobject.term_array), 0,
                         "term_array is not none")
        self.assertEqual(len(self.jobject.jpg_config), 0,
                         "jpg_config is not none")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 3: run without port_name")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        result = self.jobject.setup_jpg_filter(**param)

        self.assertFalse(result, "Return should be False")
        self.assertEqual(len(self.jobject.term_array), 0,
                         "term_array is not none")
        self.assertEqual(len(self.jobject.jpg_config), 0,
                         "jpg_config is not none")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 4: run without vlan_id")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)

        self.assertEqual(
            len(self.jobject.term_array), 31, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 52, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 5: run with vlan_id and without vlan_id_count")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            # 'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)

        self.assertEqual(
            len(self.jobject.term_array), 36, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 60, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 6: run without source_port")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            # 'vlan_id_count': '5',
            'vlan_id_step': '2',
            # 'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)

        self.assertEqual(
            len(self.jobject.term_array), 34, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 58, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 7: run without source_port and dest_port")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            # 'vlan_id_count': '5',
            'vlan_id_step': '2',
            # 'source_port': '80',
            # 'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 32, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 53, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 8: run without ether_type")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            # 'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            # 'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 33, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 54, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 9: run without ip_precedence")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': '1',
            # 'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 33, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 57, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 10: run without vlan_pri")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            # 'vlan_pri': '1',
            'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': '1',
            # 'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 30, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 51, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 11: run without src_mask and src_num_addr")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            # 'vlan_pri': '1',
            'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': '1',
            # 'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            # 'src_num_addr': '2',
            # 'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 26, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 47, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 12: run without dst_mask and dst_num_addr")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            # 'dst_num_addr': '2',
            # 'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 42, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 66, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 13: run without mac_src")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            # 'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 41, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 62, "jpg_config is incorrect")

        ######################################################################
        logging.info(
            "Testcase 14: run with mac_src and mac_dst without src_num_addr")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            # 'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'}
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 42, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 66, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 15: run without mac_dst")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            # 'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 41, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 62, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 16: run with src_mod=1")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            'prefix_list': '',
            'vlan_id': '10',
            'vlan_pri': '1',
            'ether_type': '1',
            'ip_precedence': '7',
            'single_term': '1',
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            'dest_port': '90',
            'src_mod': '1',
            'src_num_addr': '2',
            'src_mask': '24',
            'dst_mod': '1',
            # 'dst_num_addr': '2',
            'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 42, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 66, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 17: run without value")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            # 'ip_src': '1.1.1.0',
            # 'ip_dst': '1.1.1.1',
            # 'prefix_list': '',
            # 'vlan_id': '10',
            # 'vlan_pri': '1',
            # 'ether_type': '1',
            # 'ip_precedence': '7',
            # 'single_term': '1',
            # 'vlan_id_count': '5',
            # 'vlan_id_step': '2',
            # 'source_port': '80',
            # 'dest_port': '90',
            # 'src_mod': '1',
            # 'src_num_addr': '2',
            # 'src_mask': '24',
            # 'dst_mod': '1',
            # 'dst_num_addr': '2',
            # 'dst_mask': '24',
            # 'step': '2',
            # 'mac_src': '00:00:00:11:00:11',
            # 'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
        # print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 0, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 0, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 18: run with src_mod=2")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            # 'prefix_list': '',
            'vlan_id': '10',
            # 'vlan_pri': '1',
            # 'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': 0,
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            # 'dest_port': '90',
            'src_mod': '2',
            'src_num_addr': '2',
            # 'src_mask': '24',
            'dst_mod': '2',
            'dst_num_addr': '2',
            # 'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
#         print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 35, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 53, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 19: run with src_mod=3")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            # 'prefix_list': '',
            'vlan_id': '10',
            # 'vlan_pri': '1',
            # 'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': 0,
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            # 'dest_port': '90',
            'src_mod': '3',
            'src_num_addr': '2',
            # 'src_mask': '24',
            'dst_mod': '3',
            'dst_num_addr': '2',
            # 'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
#         print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 35, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 53, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 20: run with src_mod=4")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            'ip_src': '1.1.1.0',
            'ip_dst': '1.1.1.1',
            # 'prefix_list': '',
            'vlan_id': '10',
            # 'vlan_pri': '1',
            # 'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': 0,
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            # 'dest_port': '90',
            'src_mod': '4',
            'src_num_addr': '2',
            # 'src_mask': '24',
            'dst_mod': '4',
            'dst_num_addr': '2',
            # 'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
#         print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 35, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 53, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 21: run with src_mod=5")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            # 'ip_src': '1.1.1.0',
            # 'ip_dst': '1.1.1.1',
            # 'prefix_list': '',
            'vlan_id': '10',
            # 'vlan_pri': '1',
            # 'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': 0,
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            # 'dest_port': '90',
            'src_mod': '5',
            'src_num_addr': '2',
            # 'src_mask': '24',
            'dst_mod': '5',
            'dst_num_addr': '2',
            # 'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
#         print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 25, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 37, "jpg_config is incorrect")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 22: run with src_mod=6")
        self.jobject.term_array = []
        self.jobject.jpg_config = []
        param = {
            'filter': 'ctrl_input_dut_1',
            'term_name': 'ipterm',
            'port_name': 'ge-9/0/0',
            # 'ip_src': '1.1.1.0',
            # 'ip_dst': '1.1.1.1',
            # 'prefix_list': '',
            'vlan_id': '10',
            # 'vlan_pri': '1',
            # 'ether_type': '1',
            # 'ip_precedence': '7',
            'single_term': 0,
            'vlan_id_count': '5',
            'vlan_id_step': '2',
            'source_port': '80',
            # 'dest_port': '90',
            'src_mod': '6',
            'src_num_addr': '2',
            # 'src_mask': '24',
            'dst_mod': '6',
            'dst_num_addr': '2',
            # 'dst_mask': '24',
            'step': '2',
            'mac_src': '00:00:00:11:00:11',
            'mac_dst': '00:00:00:11:00:12'
        }
        self.jobject.log = MagicMock()
        self.jobject.setup_jpg_filter(**param)
#         print len(self.jobject.term_array)

        self.assertEqual(
            len(self.jobject.term_array), 25, "term_array is incorrect")
        self.assertEqual(
            len(self.jobject.jpg_config), 37, "jpg_config is incorrect")
        logging.info("\tPassed")

    def test_attach_jpg_filter(self):
        ######################################################################
        logging.info("Test case 1: run with commit True and empty term_array")
        self.jobject.term_array = []
        self.jobject.user_filter = ['test1', 'test2']
        self.jobject.log = MagicMock()
        self.jobject.config = MagicMock()
        self.jobject.commit = MagicMock(side_effect=[Response(response=True)])
        result = self.jobject.attach_jpg_filter()

        self.assertIsNot(result, False, "Return should not be False")
        self.assertListEqual(self.jobject.term_array, self.jobject.user_filter,
                             'Delete 2 list failed')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: run with commit True and valid term_array")
        self.jobject.term_array = [
            'set firewall filter test term test from source-address 1.2.3.4',
            'set firewall filter test term test then accept',
            'delete firewall filter test term test'
            ]
        self.jobject.user_filter = ['test1', 'test2']
        self.jobject.log = MagicMock()
        self.jobject.config = MagicMock()
        self.jobject.commit = MagicMock(side_effect=[Response(response=True)])
        result = self.jobject.attach_jpg_filter()

        self.assertIsNot(result, False, "Return should not be False")
        self.assertListEqual(self.jobject.term_array, self.jobject.user_filter,
                             'Delete 2 list failed')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: run with commit error and valid term_array")
        self.jobject.term_array = [
            'set firewall filter test term test from source-address 1.2.3.4',
            'set firewall filter test term test then accept',
            'delete firewall filter test term test'
            ]
        self.jobject.user_filter = ['test1', 'test2']
        self.jobject.log = MagicMock()
        self.jobject.config = MagicMock()
        self.jobject.commit = MagicMock(side_effect=Exception('error'))
        result = self.jobject.attach_jpg_filter()

        self.assertIsNot(result, True, "Return should not be True")
        logging.info("\tPassed")

    def test__add_new_filter_to_array(self):
        ######################################################################
        logging.info("Test case 1: Run function with user_filter is empty")
        self.jobject.log = MagicMock()
        self.jobject.user_filter = []
        self.jobject._Jpg__add_new_filter_to_array(filter='Filter_1')
        expected = ['Filter_1']

        self.assertListEqual(self.jobject.user_filter, expected,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run function with user_filter is not empty")
        self.jobject.user_filter = ['Filter_1', 'Filter_2']
        self.jobject._Jpg__add_new_filter_to_array(filter='Filter_3')
        expected = ['Filter_1', 'Filter_2', 'Filter_3']

        self.assertListEqual(self.jobject.user_filter, expected,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run function with new filter already " +
                     "exists in user_filter")
        self.jobject.user_filter = ['Filter_1', 'Filter_2']
        self.jobject._Jpg__add_new_filter_to_array(filter='Filter_2')
        expected = ['Filter_1', 'Filter_2']

        self.assertListEqual(self.jobject.user_filter, expected,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run function with input is " +
                     "a dictionary format")
        self.jobject.user_filter = ['Filter_1', 'Filter_2']
        self.jobject._Jpg__add_new_filter_to_array(**{'filter': 'Filter_3'})
        expected = ['Filter_1', 'Filter_2', 'Filter_3']

        self.assertListEqual(self.jobject.user_filter, expected,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Run function without filter key in " +
                     "the input dictionary")
        self.jobject.user_filter = ['Filter_1', 'Filter_2']
        self.jobject._Jpg__add_new_filter_to_array(
            **{'filter_test': 'Filter_3'})
        expected = ['Filter_1', 'Filter_2']

        self.assertListEqual(self.jobject.user_filter, expected,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Run function without filter key")
        self.jobject._Jpg__add_new_filter_to_array(filter1='Filter_1')
        self.jobject.user_filter = []
        expected = []

        self.assertListEqual(self.jobject.user_filter, expected,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

    def test__attach_default_term(self):
        ######################################################################
        logging.info("Test case 1: Run function with jpg_config are empty")
        self.jobject.log = MagicMock()
        self.jobject.jpg_config = []
        fil = 'Filter_Default'
        term = 'default'
        self.jobject._Jpg__attach_default_term(filter=fil)
        expected_result = ["set firewall family bridge filter " +
                           "%s term %s then forwarding-class FC-Q1" % (fil,
                                                                       term),
                           "set firewall family bridge filter " +
                           "%s term %s then accept" % (fil, term),
                           "set firewall family bridge filter " +
                           "%s term %s then count %s" % (fil, term, term)]

        self.assertListEqual(self.jobject.jpg_config, expected_result,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run function with jpg_config are not empty")
        fil = 'Filter_Default'
        term = 'default'
        self.jobject.jpg_config = ["set firewall family bridge filter " +
                                   "%s term %s then forwarding-class FC-Q1"
                                   % ("Filter1", term),
                                   "set firewall family bridge filter " +
                                   "%s term %s then accept"
                                   % ("Filter1", term),
                                   "set firewall family bridge filter " +
                                   "%s term %s then count %s"
                                   % ("Filter1", term, term)]
        expected_result = ["set firewall family bridge filter " +
                           "%s term %s then forwarding-class FC-Q1" % (
                               "Filter1", term),
                           "set firewall family bridge filter " +
                           "%s term %s then accept" % ("Filter1", term),
                           "set firewall family bridge filter " +
                           "%s term %s then count %s" % ("Filter1",
                                                         term,
                                                         term),
                           "set firewall family bridge filter " +
                           "%s term %s then forwarding-class FC-Q1" % (fil,
                                                                       term),
                           "set firewall family bridge filter " +
                           "%s term %s then accept" % (fil, term),
                           "set firewall family bridge filter " +
                           "%s term %s then count %s" % (fil, term, term)]
        self.jobject._Jpg__attach_default_term(filter=fil)

        self.assertListEqual(self.jobject.jpg_config, expected_result,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Run function without filter key in input " +
                     "and jpg_config are not empty")
        self.jobject.jpg_config = []
        _filter = 'Filter_Default'
        term = 'default'
        self.jobject.jpg_config = ["set firewall family bridge filter " +
                                   "%s term %s then forwarding-class FC-Q1"
                                   % ("Filter1", term),
                                   "set firewall family bridge filter " +
                                   "%s term %s then accept"
                                   % ("Filter1", term),
                                   "set firewall family bridge filter " +
                                   "%s term %s then count %s"
                                   % ("Filter1", term, term)]
        expected_result = ["set firewall family bridge filter " +
                           "%s term %s then forwarding-class FC-Q1" % (
                               "Filter1", term),
                           "set firewall family bridge filter " +
                           "%s term %s then accept" % ("Filter1", term),
                           "set firewall family bridge filter " +
                           "%s term %s then count %s" % ("Filter1",
                                                         term,
                                                         term)]
        self.jobject._Jpg__attach_default_term(filter1=_filter)

        self.assertListEqual(self.jobject.jpg_config, expected_result,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run function without filter key in input " +
                     "and jpg_config are empty")
        self.jobject.jpg_config = []
        _filter = 'Filter_Default'
        expected_result = []
        self.jobject._Jpg__attach_default_term(filter1=_filter)

        self.assertListEqual(self.jobject.jpg_config, expected_result,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Run function without filter key in input " +
                     "dictionary and jpg_config are empty")
        self.jobject.jpg_config = []
        fil = 'Filter_Default'
        term = 'default'
        self.jobject._Jpg__attach_default_term(**{'filter': fil})
        expected_result = ["set firewall family bridge filter " +
                           "%s term %s then forwarding-class FC-Q1" % (fil,
                                                                       term),
                           "set firewall family bridge filter " +
                           "%s term %s then accept" % (fil, term),
                           "set firewall family bridge filter " +
                           "%s term %s then count %s" % (fil, term, term)]

        self.assertListEqual(self.jobject.jpg_config, expected_result,
                             "Wrong return, Lists mismatched as expectation")
        logging.info("\tPassed")

    def test_get_jpg_stats(self):
        ######################################################################
        logging.info(
            "Test case 1: Verify get_gpg_stats with dictionary return")
        self.jobject.log = MagicMock()
        self.jobject.get_rpc_equivalent = MagicMock(return_value='test')
        xml1 = '''
<firewall-information><filter-information><filter-name>__default_bpdu_filter__</filter-name></filter-information><filter-information><filter-name>filter_egress_in_ge2_0_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge2_0_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge2_2_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge2_2_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge2_2_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge2_2_9</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge2_3_8</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge5_1_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_1_1</filter-name><counter><counter-name>arp</counter-name><packet-count>318</packet-count><byte-count>19080</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_1_1</filter-name><counter><counter-name>arp</counter-name><packet-count>191</packet-count><byte-count>11460</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge5_1_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge5_1_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge5_1_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe1_2_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_3_1</filter-name><counter><counter-name>arp</counter-name><packet-count>191</packet-count><byte-count>11460</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_0_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_0_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge5_1_2</filter-name><counter><counter-name>arp</counter-name><packet-count>385</packet-count><byte-count>23100</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_1_2</filter-name><counter><counter-name>arp</counter-name><packet-count>377</packet-count><byte-count>22620</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_1_5</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_1_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_1_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_5</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_2_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_3_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_3_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_3_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_3_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_3_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_3_5</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe4_3_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge2_0_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge2_0_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge2_2_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge2_2_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge2_2_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge2_2_9</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge2_3_8</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge5_1_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge5_1_2</filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_3_2</filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge5_1_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge5_1_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge5_1_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe1_2_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_ge5_1_3</filter-name><counter><counter-name>arp</counter-name><packet-count>163</packet-count><byte-count>9780</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_0_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_0_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_ge5_1_3</filter-name><counter><counter-name>arp</counter-name><packet-count>204</packet-count><byte-count>12240</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_1_2</filter-name><counter><counter-name>arp</counter-name><packet-count>179</packet-count><byte-count>10740</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_1_5</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_1_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_1_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_5</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_2_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_3_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_3_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_3_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_3_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_3_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_3_5</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe4_3_6</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_0_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_0_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_0_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_2_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_2_4</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_2_7</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_3_0</filter-name><counter><counter-name>arp</counter-name><packet-count>179</packet-count><byte-count>10740</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_xe5_2_0</filter-name><counter><counter-name>arp</counter-name><packet-count>204</packet-count><byte-count>12240</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_in_xe1_2_1</filter-name><counter><counter-name>arp</counter-name><packet-count>375</packet-count><byte-count>22500</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge2_3_3</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_ge5_0_2</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_egress_out_xe1_2_1</filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_xe5_2_1</filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_xe5_3_0</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information><filter-information><filter-name>filter_ingress_xe5_3_1</filter-name><counter><counter-name>arp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>default</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>177741</packet-count><byte-count>177030036</byte-count></counter></filter-information></firewall-information>
'''
        xml2 = '''
<configuration commit-localtime="2017-03-20 23:20:17 PDT" commit-seconds="1490077217" commit-user="regress"><interfaces><interface><name>xe-1/0/0</name><unit><name>0</name></unit></interface><interface><name>xe-1/0/1</name><unit><name>0</name></unit></interface><interface><name>xe-1/0/2</name><unit><name>0</name></unit></interface><interface><name>xe-1/0/3</name><unit><name>0</name></unit></interface><interface><name>et-1/1/0</name><unit><name>0</name></unit></interface><interface><name>xe-1/2/0</name><unit><name>0</name></unit></interface><interface><name>xe-1/2/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input-list>filter_egress_in_xe1_2_1</input-list><output-list>filter_egress_out_xe1_2_1</output-list></filter></bridge></family></unit></interface><interface><name>xe-1/2/2</name><unit><name>0</name></unit></interface><interface><name>et-1/3/0</name><unit><name>0</name></unit></interface><interface><name>ge-2/0/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_ge2_0_2</filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/0/3</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><gigether-options><loopback /></gigether-options><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_ge2_0_3</filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/0/4</name><unit><name>0</name></unit></interface><interface><name>ge-2/0/5</name><unit><name>0</name><family><inet><address><name>183.10.20.1/30</name></address><address><name>183.10.22.1/30</name></address><address><name>183.10.77.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/0/6</name><unit><name>0</name><family><inet><address><name>183.10.21.1/30</name></address><address><name>183.10.23.1/30</name></address><address><name>183.10.78.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/0/7</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_egress_in_ge2_0_7</filter-name></input><output><filter-name>filter_egress_out_ge2_0_7</filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-2/2/1</name><unit><name>0</name></unit></interface><interface><name>ge-2/2/3</name><unit><name>0</name><family><inet><address><name>183.10.22.1/30</name></address><address><name>183.10.24.1/30</name></address><address><name>183.10.79.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/2/8</name><unit><name>0</name></unit></interface><interface><name>ge-2/2/9</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_egress_in_ge2_2_9</filter-name></input><output><filter-name>filter_egress_out_ge2_2_9</filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-2/3/0</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_ge2_3_0</filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/3/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_ge2_3_1</filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/3/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_ge2_3_2</filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/3/8</name><unit><name>0</name><family><inet><address><name>183.10.80.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/3/9</name><unit><name>0</name><family><inet><address><name>183.10.81.1/30</name></address></inet></family></unit></interface><interface><name>xe-3/0/1</name><unit><name>0</name></unit></interface><interface><name>et-3/1/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/1</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/3</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/4</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_egress_in_xe4_0_4</filter-name></input><output><filter-name>filter_egress_out_xe4_0_4</filter-name></output></filter></bridge></family></unit></interface><interface><name>xe-4/1/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_egress_in_xe4_1_1</filter-name></input><output><filter-name>filter_egress_out_xe4_1_1</filter-name></output></filter></bridge></family></unit></interface><interface><name>xe-4/1/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_egress_in_xe4_1_2</filter-name></input><output><filter-name>filter_egress_out_xe4_1_2</filter-name></output></filter></bridge></family></unit></interface><interface><name>xe-4/1/3</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/4</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/6</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/7</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/1</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/2</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/3</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/4</name><unit><name>0</name><family><inet><address><name>183.10.83.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/2/5</name><unit><name>0</name><family><inet><address><name>183.10.84.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/2/6</name><unit><name>0</name><family><inet><address><name>183.10.85.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/2/7</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/1</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/4</name><unit><name>0</name><family><inet><address><name>183.10.86.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/3/5</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/6</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/7</name><unit><name>0</name><family><inet><address><name>183.10.87.1/30</name></address></inet></family></unit></interface><interface><name>ge-5/0/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><gigether-options><loopback /></gigether-options><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_ge5_0_2</filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-5/1/0</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/1</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_egress_in_ge5_1_2</filter-name></input><output><filter-name>filter_egress_out_ge5_1_2</filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-5/1/3</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_egress_in_ge5_1_3</filter-name></input><output><filter-name>filter_egress_out_ge5_1_3</filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-5/1/4</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/5</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/6</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/7</name><unit><name>0</name></unit></interface><interface><name>xe-5/2/0</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_xe5_2_0</filter-name></input></filter></bridge></family></unit></interface><interface><name>xe-5/2/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name>filter_ingress_xe5_2_1</filter-name></input></filter></bridge></family></unit></interface></interfaces></configuration>
'''
        root1 = ET.fromstring(xml1)
        root2 = ET.fromstring(xml2)
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=root1), Response(response=root2)])
        result = self.jobject.get_jpg_stats()

        self.assertEqual(type(result), dict,
                         "Wrong return, value is not a dictionary")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 2: Verify get_gpg_stats with other responses")
        self.jobject.get_rpc_equivalent = MagicMock(return_value='test')
        xml1_fail = '''
<firewall-information><filter-information><filter-name></filter-name></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>318</packet-count><byte-count>19080</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>191</packet-count><byte-count>11460</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>191</packet-count><byte-count>11460</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>385</packet-count><byte-count>23100</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>377</packet-count><byte-count>22620</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>11</packet-count><byte-count>2970</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>163</packet-count><byte-count>9780</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>204</packet-count><byte-count>12240</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>179</packet-count><byte-count>10740</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>179</packet-count><byte-count>10740</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>204</packet-count><byte-count>12240</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>375</packet-count><byte-count>22500</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>101</packet-count><byte-count>6060</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information><filter-information><filter-name></filter-name><counter><counter-name>arp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>bgp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>default</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>esmc</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>icmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>igmp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>isis</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ospf</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>pim</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter><counter><counter-name>ptp</counter-name><packet-count>0</packet-count><byte-count>0</byte-count></counter></filter-information></firewall-information>
'''
        xml2_fail = '''
<configuration commit-localtime="2017-03-20 23:20:17 PDT" commit-seconds="1490077217" commit-user="regress"><interfaces><interface><name>xe-1/0/0</name><unit><name>0</name></unit></interface><interface><name>xe-1/0/1</name><unit><name>0</name></unit></interface><interface><name>xe-1/0/2</name><unit><name>0</name></unit></interface><interface><name>xe-1/0/3</name><unit><name>0</name></unit></interface><interface><name>et-1/1/0</name><unit><name>0</name></unit></interface><interface><name>xe-1/2/0</name><unit><name>0</name></unit></interface><interface><name>xe-1/2/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input-list>filter_egress_in_xe1_2_1</input-list><output-list>filter_egress_out_xe1_2_1</output-list></filter></bridge></family></unit></interface><interface><name>xe-1/2/2</name><unit><name>0</name></unit></interface><interface><name>et-1/3/0</name><unit><name>0</name></unit></interface><interface><name>ge-2/0/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/0/3</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><gigether-options><loopback /></gigether-options><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/0/4</name><unit><name>0</name></unit></interface><interface><name>ge-2/0/5</name><unit><name>0</name><family><inet><address><name>183.10.20.1/30</name></address><address><name>183.10.22.1/30</name></address><address><name>183.10.77.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/0/6</name><unit><name>0</name><family><inet><address><name>183.10.21.1/30</name></address><address><name>183.10.23.1/30</name></address><address><name>183.10.78.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/0/7</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input><output><filter-name></filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-2/2/1</name><unit><name>0</name></unit></interface><interface><name>ge-2/2/3</name><unit><name>0</name><family><inet><address><name>183.10.22.1/30</name></address><address><name>183.10.24.1/30</name></address><address><name>183.10.79.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/2/8</name><unit><name>0</name></unit></interface><interface><name>ge-2/2/9</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input><output><filter-name></filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-2/3/0</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/3/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/3/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-2/3/8</name><unit><name>0</name><family><inet><address><name>183.10.80.1/30</name></address></inet></family></unit></interface><interface><name>ge-2/3/9</name><unit><name>0</name><family><inet><address><name>183.10.81.1/30</name></address></inet></family></unit></interface><interface><name>xe-3/0/1</name><unit><name>0</name></unit></interface><interface><name>et-3/1/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/1</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/3</name><unit><name>0</name></unit></interface><interface><name>xe-4/0/4</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input><output><filter-name></filter-name></output></filter></bridge></family></unit></interface><interface><name>xe-4/1/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input><output><filter-name></filter-name></output></filter></bridge></family></unit></interface><interface><name>xe-4/1/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input><output><filter-name></filter-name></output></filter></bridge></family></unit></interface><interface><name>xe-4/1/3</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/4</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/6</name><unit><name>0</name></unit></interface><interface><name>xe-4/1/7</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/0</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/1</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/2</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/3</name><unit><name>0</name></unit></interface><interface><name>xe-4/2/4</name><unit><name>0</name><family><inet><address><name>183.10.83.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/2/5</name><unit><name>0</name><family><inet><address><name>183.10.84.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/2/6</name><unit><name>0</name><family><inet><address><name>183.10.85.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/2/7</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/1</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/4</name><unit><name>0</name><family><inet><address><name>183.10.86.1/30</name></address></inet></family></unit></interface><interface><name>xe-4/3/5</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/6</name><unit><name>0</name></unit></interface><interface><name>xe-4/3/7</name><unit><name>0</name><family><inet><address><name>183.10.87.1/30</name></address></inet></family></unit></interface><interface><name>ge-5/0/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><gigether-options><loopback /></gigether-options><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface><interface><name>ge-5/1/0</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/1</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/2</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input><output><filter-name></filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-5/1/3</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input><output><filter-name></filter-name></output></filter></bridge></family></unit></interface><interface><name>ge-5/1/4</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/5</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/6</name><unit><name>0</name></unit></interface><interface><name>ge-5/1/7</name><unit><name>0</name></unit></interface><interface><name>xe-5/2/0</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface><interface><name>xe-5/2/1</name><mtu>9192</mtu><encapsulation>ethernet-bridge</encapsulation><unit><name>0</name><family><bridge><filter><input><filter-name></filter-name></input></filter></bridge></family></unit></interface></interfaces></configuration>
'''
        root1 = ET.fromstring(xml1_fail)
        root2 = ET.fromstring(xml2_fail)
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=root1), Response(response=root2)])
        result = self.jobject.get_jpg_stats()

        self.assertEqual(type(result), dict,
                         "Wrong return, value is not a dictionary")
        logging.info("\tPassed")

    def test_get_interface_status(self):
        ######################################################################
        logging.info("Test case 1: Execute function with invalid interface")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        self.jobject.get_rpc_equivalent = MagicMock(return_value='test')
        xml_string1 = '<interface-information style="normal"><rpc-error>' +\
            '<error-type>protocol</error-type><error-tag>operation-failed' +\
            '</error-tag><error-severity>error</error-severity>' +\
            '<source-daemon>ifinfo</source-daemon><error-message>' +\
            'device invalid not found</error-message></rpc-error>' +\
            '</interface-information>'
        xml1 = ET.fromstring(xml_string1)
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=xml1))
        intf = "invalid"
        actual_result = self.jobject._Jpg__get_interface_status(intf=intf)
        expected_result =\
            "Interface %s is not present. Hence exiting..." % intf

        self.assertEqual(actual_result, expected_result,
                         "Wrong return, Unexpected result")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Execute function with valid interface " +
                     "and not found Laser rx power low alarm status")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        self.jobject.get_rpc_equivalent = MagicMock(return_value='test')
        xml1 = '''
<interface-information style="normal"><physical-interface><name>ge-2/1/3</name><admin-status format="Enabled">up</admin-status><oper-status>up</oper-status><local-index>175</local-index><snmp-index>551</snmp-index><description>&#226;</description><link-level-type>Flexible-Ethernet</link-level-type><mtu>9100</mtu><sonet-mode>LAN-PHY</sonet-mode><mru>9108</mru><source-filtering>disabled</source-filtering><speed>1000mbps</speed><bpdu-error>none</bpdu-error><l2pt-error>none</l2pt-error><loopback>disabled</loopback><if-flow-control>enabled</if-flow-control><if-auto-negotiation>enabled</if-auto-negotiation><if-remote-fault>online</if-remote-fault><pad-to-minimum-frame-size>Disabled</pad-to-minimum-frame-size><if-device-flags><ifdf-present /><ifdf-running /></if-device-flags><ifd-specific-config-flags><internal-flags>0x200</internal-flags></ifd-specific-config-flags><if-config-flags><iff-snmp-traps /><internal-flags>0x4000</internal-flags></if-config-flags><if-media-flags><internal-flags>0x810</internal-flags></if-media-flags><physical-interface-cos-information><physical-interface-cos-hw-max-queues>8</physical-interface-cos-hw-max-queues><physical-interface-cos-use-max-queues>8</physical-interface-cos-use-max-queues><physical-interface-schedulers>0</physical-interface-schedulers></physical-interface-cos-information><current-physical-address>a8:d0:e5:f2:05:d2</current-physical-address><hardware-physical-address>a8:d0:e5:f2:05:d2</hardware-physical-address><interface-flapped seconds="1322790">2017-03-07 13:12:58 PST (2w1d 07:26 ago)</interface-flapped><traffic-statistics style="brief"><input-bps>0</input-bps><input-pps>0</input-pps><output-bps>0</output-bps><output-pps>0</output-pps></traffic-statistics><active-alarms><interface-alarms><alarm-not-present /></interface-alarms></active-alarms><active-defects><interface-alarms><alarm-not-present /></interface-alarms></active-defects><interface-transmit-statistics>Disabled</interface-transmit-statistics><logical-interface><name>ge-2/1/3.90</name><local-index>2386</local-index><snmp-index>784</snmp-index><if-config-flags><iff-up /><iff-snmp-traps /><internal-flags>0x4000</internal-flags></if-config-flags><link-address format="VLAN-Tag [ 0x8100.90 ] ">[ 0x8100.90 ]</link-address><encapsulation>ENET2</encapsulation><policer-overhead /><traffic-statistics style="brief"><input-packets>8</input-packets><output-packets>8</output-packets></traffic-statistics><filter-information /><address-family><address-family-name>inet</address-family-name><mtu>9078</mtu><address-family-flags><ifff-sendbcast-pkt-to-re /><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>157.2.1.0/30</ifa-destination><ifa-local>157.2.1.1</ifa-local><ifa-broadcast>157.2.1.3</ifa-broadcast></interface-address></address-family><address-family><address-family-name>inet6</address-family-name><mtu>9078</mtu><max-local-cache>75000</max-local-cache><new-hold-limit>75000</new-hold-limit><intf-curr-cnt>0</intf-curr-cnt><intf-unresolved-cnt>0</intf-unresolved-cnt><intf-dropcnt>0</intf-dropcnt><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>f053::9d02:100/126</ifa-destination><ifa-local>f053::9d02:101</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address><interface-address><ifa-flags><ifaf-current-preferred /><internal-flags>0x800</internal-flags></ifa-flags><ifa-destination>fe80::/64</ifa-destination><ifa-local>fe80::aad0:e500:5af2:5d2</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address></address-family><address-family><address-family-name>multiservice</address-family-name><mtu>Unlimited</mtu><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags></address-family></logical-interface><logical-interface><name>ge-2/1/3.91</name><local-index>2387</local-index><snmp-index>785</snmp-index><if-config-flags><iff-up /><iff-snmp-traps /><internal-flags>0x4000</internal-flags></if-config-flags><link-address format="VLAN-Tag [ 0x8100.91 ] ">[ 0x8100.91 ]</link-address><encapsulation>ENET2</encapsulation><policer-overhead /><traffic-statistics style="brief"><input-packets>8</input-packets><output-packets>8</output-packets></traffic-statistics><filter-information /><address-family><address-family-name>inet</address-family-name><mtu>9078</mtu><address-family-flags><ifff-sendbcast-pkt-to-re /><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>157.2.1.4/30</ifa-destination><ifa-local>157.2.1.5</ifa-local><ifa-broadcast>157.2.1.7</ifa-broadcast></interface-address></address-family><address-family><address-family-name>inet6</address-family-name><mtu>9078</mtu><max-local-cache>75000</max-local-cache><new-hold-limit>75000</new-hold-limit><intf-curr-cnt>0</intf-curr-cnt><intf-unresolved-cnt>0</intf-unresolved-cnt><intf-dropcnt>0</intf-dropcnt><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>f053::9d02:104/126</ifa-destination><ifa-local>f053::9d02:105</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address><interface-address><ifa-flags><ifaf-current-preferred /><internal-flags>0x800</internal-flags></ifa-flags><ifa-destination>fe80::/64</ifa-destination><ifa-local>fe80::aad0:e500:5bf2:5d2</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address></address-family><address-family><address-family-name>multiservice</address-family-name><mtu>Unlimited</mtu><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags></address-family></logical-interface><logical-interface><name>ge-2/1/3.92</name><local-index>2388</local-index><snmp-index>786</snmp-index><if-config-flags><iff-up /><iff-snmp-traps /><internal-flags>0x4000</internal-flags></if-config-flags><link-address format="VLAN-Tag [ 0x8100.92 ] ">[ 0x8100.92 ]</link-address><encapsulation>ENET2</encapsulation><policer-overhead /><traffic-statistics style="brief"><input-packets>8</input-packets><output-packets>8</output-packets></traffic-statistics><filter-information /><address-family><address-family-name>inet</address-family-name><mtu>9078</mtu><address-family-flags><ifff-sendbcast-pkt-to-re /><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>157.2.1.8/30</ifa-destination><ifa-local>157.2.1.9</ifa-local><ifa-broadcast>157.2.1.11</ifa-broadcast></interface-address></address-family><address-family><address-family-name>inet6</address-family-name><mtu>9078</mtu><max-local-cache>75000</max-local-cache><new-hold-limit>75000</new-hold-limit><intf-curr-cnt>0</intf-curr-cnt><intf-unresolved-cnt>0</intf-unresolved-cnt><intf-dropcnt>0</intf-dropcnt><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>f053::9d02:108/126</ifa-destination><ifa-local>f053::9d02:109</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address><interface-address><ifa-flags><ifaf-current-preferred /><internal-flags>0x800</internal-flags></ifa-flags><ifa-destination>fe80::/64</ifa-destination><ifa-local>fe80::aad0:e500:5cf2:5d2</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address></address-family><address-family><address-family-name>multiservice</address-family-name><mtu>Unlimited</mtu><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags></address-family></logical-interface><logical-interface><name>ge-2/1/3.93</name><local-index>2389</local-index><snmp-index>787</snmp-index><if-config-flags><iff-up /><iff-snmp-traps /><internal-flags>0x4000</internal-flags></if-config-flags><link-address format="VLAN-Tag [ 0x8100.93 ] ">[ 0x8100.93 ]</link-address><encapsulation>ENET2</encapsulation><policer-overhead /><traffic-statistics style="brief"><input-packets>8</input-packets><output-packets>8</output-packets></traffic-statistics><filter-information /><address-family><address-family-name>inet</address-family-name><mtu>9078</mtu><address-family-flags><ifff-sendbcast-pkt-to-re /><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>157.2.1.12/30</ifa-destination><ifa-local>157.2.1.13</ifa-local><ifa-broadcast>157.2.1.15</ifa-broadcast></interface-address></address-family><address-family><address-family-name>inet6</address-family-name><mtu>9078</mtu><max-local-cache>75000</max-local-cache><new-hold-limit>75000</new-hold-limit><intf-curr-cnt>0</intf-curr-cnt><intf-unresolved-cnt>0</intf-unresolved-cnt><intf-dropcnt>0</intf-dropcnt><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>f053::9d02:10c/126</ifa-destination><ifa-local>f053::9d02:10d</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address><interface-address><ifa-flags><ifaf-current-preferred /><internal-flags>0x800</internal-flags></ifa-flags><ifa-destination>fe80::/64</ifa-destination><ifa-local>fe80::aad0:e500:5df2:5d2</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address></address-family><address-family><address-family-name>multiservice</address-family-name><mtu>Unlimited</mtu><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags></address-family></logical-interface><logical-interface><name>ge-2/1/3.94</name><local-index>2390</local-index><snmp-index>788</snmp-index><if-config-flags><iff-up /><iff-snmp-traps /><internal-flags>0x4000</internal-flags></if-config-flags><link-address format="VLAN-Tag [ 0x8100.94 ] ">[ 0x8100.94 ]</link-address><encapsulation>ENET2</encapsulation><policer-overhead /><traffic-statistics style="brief"><input-packets>8</input-packets><output-packets>8</output-packets></traffic-statistics><filter-information /><address-family><address-family-name>inet</address-family-name><mtu>9078</mtu><address-family-flags><ifff-sendbcast-pkt-to-re /><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>157.2.1.16/30</ifa-destination><ifa-local>157.2.1.17</ifa-local><ifa-broadcast>157.2.1.19</ifa-broadcast></interface-address></address-family><address-family><address-family-name>inet6</address-family-name><mtu>9078</mtu><max-local-cache>75000</max-local-cache><new-hold-limit>75000</new-hold-limit><intf-curr-cnt>0</intf-curr-cnt><intf-unresolved-cnt>0</intf-unresolved-cnt><intf-dropcnt>0</intf-dropcnt><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>f053::9d02:110/126</ifa-destination><ifa-local>f053::9d02:111</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address><interface-address><ifa-flags><ifaf-current-preferred /><internal-flags>0x800</internal-flags></ifa-flags><ifa-destination>fe80::/64</ifa-destination><ifa-local>fe80::aad0:e500:5ef2:5d2</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address></address-family><address-family><address-family-name>multiservice</address-family-name><mtu>Unlimited</mtu><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags></address-family></logical-interface><logical-interface><name>ge-2/1/3.95</name><local-index>2391</local-index><snmp-index>789</snmp-index><if-config-flags><iff-up /><iff-snmp-traps /><internal-flags>0x4000</internal-flags></if-config-flags><link-address format="VLAN-Tag [ 0x8100.95 ] ">[ 0x8100.95 ]</link-address><encapsulation>ENET2</encapsulation><policer-overhead /><traffic-statistics style="brief"><input-packets>8</input-packets><output-packets>8</output-packets></traffic-statistics><filter-information /><address-family><address-family-name>inet</address-family-name><mtu>9078</mtu><address-family-flags><ifff-sendbcast-pkt-to-re /><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>157.2.1.20/30</ifa-destination><ifa-local>157.2.1.21</ifa-local><ifa-broadcast>157.2.1.23</ifa-broadcast></interface-address></address-family><address-family><address-family-name>inet6</address-family-name><mtu>9078</mtu><max-local-cache>75000</max-local-cache><new-hold-limit>75000</new-hold-limit><intf-curr-cnt>0</intf-curr-cnt><intf-unresolved-cnt>0</intf-unresolved-cnt><intf-dropcnt>0</intf-dropcnt><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags><interface-address><ifa-flags><ifaf-current-preferred /><ifaf-current-primary /></ifa-flags><ifa-destination>f053::9d02:114/126</ifa-destination><ifa-local>f053::9d02:115</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address><interface-address><ifa-flags><ifaf-current-preferred /><internal-flags>0x800</internal-flags></ifa-flags><ifa-destination>fe80::/64</ifa-destination><ifa-local>fe80::aad0:e500:5ff2:5d2</ifa-local><interface-address><in6-addr-flags><ifaf-none /></in6-addr-flags></interface-address></interface-address></address-family><address-family><address-family-name>multiservice</address-family-name><mtu>Unlimited</mtu><address-family-flags><internal-flags>0x0</internal-flags></address-family-flags></address-family></logical-interface><logical-interface><name>ge-2/1/3.32767</name><local-index>2392</local-index><snmp-index>790</snmp-index><if-config-flags><iff-up /><iff-snmp-traps /><internal-flags>0x4004000</internal-flags></if-config-flags><link-address format="VLAN-Tag [ 0x0000.0 ] ">[ 0x0000.0 ]</link-address><encapsulation>ENET2</encapsulation><policer-overhead /><traffic-statistics style="brief"><input-packets>0</input-packets><output-packets>0</output-packets></traffic-statistics><filter-information /><address-family><address-family-name>multiservice</address-family-name><mtu>Unlimited</mtu><address-family-flags><ifff-none /></address-family-flags></address-family></logical-interface></physical-interface></interface-information>
'''
        xml2 = '''
<interface-information style="normal"><physical-interface><name>ge-2/1/3</name><optics-diagnostics><laser-bias-current>5.788</laser-bias-current><laser-output-power>0.2810</laser-output-power><laser-output-power-dbm>-5.51</laser-output-power-dbm><module-temperature celsius="35.2">35 degrees C / 95 degrees F</module-temperature><module-voltage>3.2540</module-voltage><rx-signal-avg-optical-power>0.2908</rx-signal-avg-optical-power><rx-signal-avg-optical-power-dbm>-5.36</rx-signal-avg-optical-power-dbm><laser-bias-current-high-alarm>off</laser-bias-current-high-alarm><laser-bias-current-low-alarm>off</laser-bias-current-low-alarm><laser-bias-current-high-warn>off</laser-bias-current-high-warn><laser-bias-current-low-warn>off</laser-bias-current-low-warn><laser-tx-power-high-alarm>off</laser-tx-power-high-alarm><laser-tx-power-low-alarm>off</laser-tx-power-low-alarm><laser-tx-power-high-warn>off</laser-tx-power-high-warn><laser-tx-power-low-warn>off</laser-tx-power-low-warn><module-temperature-high-alarm>off</module-temperature-high-alarm><module-temperature-low-alarm>off</module-temperature-low-alarm><module-temperature-high-warn>off</module-temperature-high-warn><module-temperature-low-warn>off</module-temperature-low-warn><module-voltage-high-alarm>off</module-voltage-high-alarm><module-voltage-low-alarm>off</module-voltage-low-alarm><module-voltage-high-warn>off</module-voltage-high-warn><module-voltage-low-warn>off</module-voltage-low-warn><laser-rx-power-high-alarm>off</laser-rx-power-high-alarm><laser-rx-power-low-alarm>off</laser-rx-power-low-alarm><laser-rx-power-high-warn>off</laser-rx-power-high-warn><laser-rx-power-low-warn>off</laser-rx-power-low-warn><laser-bias-current-high-alarm-threshold>17.000</laser-bias-current-high-alarm-threshold><laser-bias-current-low-alarm-threshold>1.000</laser-bias-current-low-alarm-threshold><laser-bias-current-high-warn-threshold>14.000</laser-bias-current-high-warn-threshold><laser-bias-current-low-warn-threshold>2.000</laser-bias-current-low-warn-threshold><laser-tx-power-high-alarm-threshold>0.6310</laser-tx-power-high-alarm-threshold><laser-tx-power-high-alarm-threshold-dbm>-2.00</laser-tx-power-high-alarm-threshold-dbm><laser-tx-power-low-alarm-threshold>0.0660</laser-tx-power-low-alarm-threshold><laser-tx-power-low-alarm-threshold-dbm>-11.80</laser-tx-power-low-alarm-threshold-dbm><laser-tx-power-high-warn-threshold>0.6310</laser-tx-power-high-warn-threshold><laser-tx-power-high-warn-threshold-dbm>-2.00</laser-tx-power-high-warn-threshold-dbm><laser-tx-power-low-warn-threshold>0.0790</laser-tx-power-low-warn-threshold><laser-tx-power-low-warn-threshold-dbm>-11.02</laser-tx-power-low-warn-threshold-dbm><module-temperature-high-alarm-threshold celsius="110.0">110 degrees C / 230 degrees F</module-temperature-high-alarm-threshold><module-temperature-low-alarm-threshold celsius="-40.0">-40 degrees C / -40 degrees F</module-temperature-low-alarm-threshold><module-temperature-high-warn-threshold celsius="93.0">93 degrees C / 199 degrees F</module-temperature-high-warn-threshold><module-temperature-low-warn-threshold celsius="-30.0">-30 degrees C / -22 degrees F</module-temperature-low-warn-threshold><module-voltage-high-alarm-threshold>3.900</module-voltage-high-alarm-threshold><module-voltage-low-alarm-threshold>2.700</module-voltage-low-alarm-threshold><module-voltage-high-warn-threshold>3.700</module-voltage-high-warn-threshold><module-voltage-low-warn-threshold>2.900</module-voltage-low-warn-threshold><laser-rx-power-high-alarm-threshold>1.2589</laser-rx-power-high-alarm-threshold><laser-rx-power-high-alarm-threshold-dbm>1.00</laser-rx-power-high-alarm-threshold-dbm><laser-rx-power-low-alarm-threshold>0.0100</laser-rx-power-low-alarm-threshold><laser-rx-power-low-alarm-threshold-dbm>-20.00</laser-rx-power-low-alarm-threshold-dbm><laser-rx-power-high-warn-threshold>0.7943</laser-rx-power-high-warn-threshold><laser-rx-power-high-warn-threshold-dbm>-1.00</laser-rx-power-high-warn-threshold-dbm><laser-rx-power-low-warn-threshold>0.0158</laser-rx-power-low-warn-threshold><laser-rx-power-low-warn-threshold-dbm>-18.01</laser-rx-power-low-warn-threshold-dbm></optics-diagnostics></physical-interface></interface-information>
'''
        root1 = ET.fromstring(xml1)
        root2 = ET.fromstring(xml2)
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=root1), Response(response=root2)])
        intf = "ge-0/0/0"
        actual_result = self.jobject._Jpg__get_interface_status(intf=intf)
        expected_result = "Optics Missing"

        self.assertEqual(actual_result, expected_result,
                         "Wrong return, Unexpected result")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Execute function with valid interface " +
                     "and Laser rx power low alarm status exists")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        self.jobject.get_rpc_equivalent = MagicMock(return_value='test')
        xml3 = '''
<interface-information style="normal"><physical-interface><name>ge-2/1/3</name><optics-diagnostics><laser-bias-current>5.788</laser-bias-current><laser-output-power>0.2810</laser-output-power><laser-output-power-dbm>-5.51</laser-output-power-dbm><module-temperature celsius="35.2">35 degrees C / 95 degrees F</module-temperature><module-voltage>3.2540</module-voltage><rx-signal-avg-optical-power>0.2908</rx-signal-avg-optical-power><rx-signal-avg-optical-power-dbm>-5.36</rx-signal-avg-optical-power-dbm><laser-bias-current-high-alarm>off</laser-bias-current-high-alarm><laser-bias-current-low-alarm>off</laser-bias-current-low-alarm><laser-bias-current-high-warn>off</laser-bias-current-high-warn><laser-bias-current-low-warn>off</laser-bias-current-low-warn><laser-tx-power-high-alarm>off</laser-tx-power-high-alarm><laser-tx-power-low-alarm>off</laser-tx-power-low-alarm><laser-tx-power-high-warn>off</laser-tx-power-high-warn><laser-tx-power-low-warn>off</laser-tx-power-low-warn><module-temperature-high-alarm>off</module-temperature-high-alarm><module-temperature-low-alarm>off</module-temperature-low-alarm><module-temperature-high-warn>off</module-temperature-high-warn><module-temperature-low-warn>off</module-temperature-low-warn><module-voltage-high-alarm>off</module-voltage-high-alarm><module-voltage-low-alarm>off</module-voltage-low-alarm><module-voltage-high-warn>off</module-voltage-high-warn><module-voltage-low-warn>off</module-voltage-low-warn><laser-rx-power-high-alarm>off</laser-rx-power-high-alarm><laser-rx-power-low-alarm>on</laser-rx-power-low-alarm><laser-rx-power-high-warn>off</laser-rx-power-high-warn><laser-rx-power-low-warn>off</laser-rx-power-low-warn><laser-bias-current-high-alarm-threshold>17.000</laser-bias-current-high-alarm-threshold><laser-bias-current-low-alarm-threshold>1.000</laser-bias-current-low-alarm-threshold><laser-bias-current-high-warn-threshold>14.000</laser-bias-current-high-warn-threshold><laser-bias-current-low-warn-threshold>2.000</laser-bias-current-low-warn-threshold><laser-tx-power-high-alarm-threshold>0.6310</laser-tx-power-high-alarm-threshold><laser-tx-power-high-alarm-threshold-dbm>-2.00</laser-tx-power-high-alarm-threshold-dbm><laser-tx-power-low-alarm-threshold>0.0660</laser-tx-power-low-alarm-threshold><laser-tx-power-low-alarm-threshold-dbm>-11.80</laser-tx-power-low-alarm-threshold-dbm><laser-tx-power-high-warn-threshold>0.6310</laser-tx-power-high-warn-threshold><laser-tx-power-high-warn-threshold-dbm>-2.00</laser-tx-power-high-warn-threshold-dbm><laser-tx-power-low-warn-threshold>0.0790</laser-tx-power-low-warn-threshold><laser-tx-power-low-warn-threshold-dbm>-11.02</laser-tx-power-low-warn-threshold-dbm><module-temperature-high-alarm-threshold celsius="110.0">110 degrees C / 230 degrees F</module-temperature-high-alarm-threshold><module-temperature-low-alarm-threshold celsius="-40.0">-40 degrees C / -40 degrees F</module-temperature-low-alarm-threshold><module-temperature-high-warn-threshold celsius="93.0">93 degrees C / 199 degrees F</module-temperature-high-warn-threshold><module-temperature-low-warn-threshold celsius="-30.0">-30 degrees C / -22 degrees F</module-temperature-low-warn-threshold><module-voltage-high-alarm-threshold>3.900</module-voltage-high-alarm-threshold><module-voltage-low-alarm-threshold>2.700</module-voltage-low-alarm-threshold><module-voltage-high-warn-threshold>3.700</module-voltage-high-warn-threshold><module-voltage-low-warn-threshold>2.900</module-voltage-low-warn-threshold><laser-rx-power-high-alarm-threshold>1.2589</laser-rx-power-high-alarm-threshold><laser-rx-power-high-alarm-threshold-dbm>1.00</laser-rx-power-high-alarm-threshold-dbm><laser-rx-power-low-alarm-threshold>0.0100</laser-rx-power-low-alarm-threshold><laser-rx-power-low-alarm-threshold-dbm>-20.00</laser-rx-power-low-alarm-threshold-dbm><laser-rx-power-high-warn-threshold>0.7943</laser-rx-power-high-warn-threshold><laser-rx-power-high-warn-threshold-dbm>-1.00</laser-rx-power-high-warn-threshold-dbm><laser-rx-power-low-warn-threshold>0.0158</laser-rx-power-low-warn-threshold><laser-rx-power-low-warn-threshold-dbm>-18.01</laser-rx-power-low-warn-threshold-dbm></optics-diagnostics></physical-interface></interface-information>
'''
        root2 = ET.fromstring(xml3)
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=root1), Response(response=root2)])
        intf = "ge-0/0/0"
        actual_result = self.jobject._Jpg__get_interface_status(intf=intf)
        expected_result = "Loss of signal present %s" % intf

        self.assertEqual(actual_result, expected_result,
                         "Wrong return, Unexpected result")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Execute function with invalid interface")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        self.jobject.get_rpc_equivalent = MagicMock(return_value='test')
        xml_string1 = '<interface-information style="normal"><rpc-error>' +\
            '<error-type>protocol</error-type><error-tag>operation-failed' +\
            '</error-tag><error-severity>error</error-severity>' +\
            '<source-daemon>ifinfo</source-daemon><error-message>' +\
            'another error</error-message></rpc-error>' +\
            '</interface-information>'
        xml1 = ET.fromstring(xml_string1)
        self.jobject.execute_rpc = MagicMock(
            return_value=Response(response=xml1))
        intf = "invalid"
        actual_result = self.jobject._Jpg__get_interface_status(intf=intf)
        expected_result = None

        self.assertEqual(actual_result, expected_result,
                         "Wrong return, Unexpected result")
        logging.info("\tPassed")

        ######################################################################
        logging.info(
            "Test case 5: Laser rx power low alarm status does not exist")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        self.jobject.get_rpc_equivalent = MagicMock(return_value='test')
        xml4 = '''
<interface-information style="normal"><physical-interface><name>ge-2/1/3</name><optics-diagnostics><laser-bias-current>5.788</laser-bias-current><laser-output-power>0.2810</laser-output-power><laser-output-power-dbm>-5.51</laser-output-power-dbm><module-temperature celsius="35.2">35 degrees C / 95 degrees F</module-temperature><module-voltage>3.2540</module-voltage><rx-signal-avg-optical-power>0.2908</rx-signal-avg-optical-power><rx-signal-avg-optical-power-dbm>-5.36</rx-signal-avg-optical-power-dbm><laser-bias-current-high-alarm>off</laser-bias-current-high-alarm><laser-bias-current-low-alarm>off</laser-bias-current-low-alarm><laser-bias-current-high-warn>off</laser-bias-current-high-warn><laser-bias-current-low-warn>off</laser-bias-current-low-warn><laser-tx-power-high-alarm>off</laser-tx-power-high-alarm><laser-tx-power-low-alarm>off</laser-tx-power-low-alarm><laser-tx-power-high-warn>off</laser-tx-power-high-warn><laser-tx-power-low-warn>off</laser-tx-power-low-warn><module-temperature-high-alarm>off</module-temperature-high-alarm><module-temperature-low-alarm>off</module-temperature-low-alarm><module-temperature-high-warn>off</module-temperature-high-warn><module-temperature-low-warn>off</module-temperature-low-warn><module-voltage-high-alarm>off</module-voltage-high-alarm><module-voltage-low-alarm>off</module-voltage-low-alarm><module-voltage-high-warn>off</module-voltage-high-warn><module-voltage-low-warn>off</module-voltage-low-warn><laser-rx-power-high-alarm>off</laser-rx-power-high-alarm><laser-rx-power-high-warn>off</laser-rx-power-high-warn><laser-rx-power-low-warn>off</laser-rx-power-low-warn><laser-bias-current-high-alarm-threshold>17.000</laser-bias-current-high-alarm-threshold><laser-bias-current-low-alarm-threshold>1.000</laser-bias-current-low-alarm-threshold><laser-bias-current-high-warn-threshold>14.000</laser-bias-current-high-warn-threshold><laser-bias-current-low-warn-threshold>2.000</laser-bias-current-low-warn-threshold><laser-tx-power-high-alarm-threshold>0.6310</laser-tx-power-high-alarm-threshold><laser-tx-power-high-alarm-threshold-dbm>-2.00</laser-tx-power-high-alarm-threshold-dbm><laser-tx-power-low-alarm-threshold>0.0660</laser-tx-power-low-alarm-threshold><laser-tx-power-low-alarm-threshold-dbm>-11.80</laser-tx-power-low-alarm-threshold-dbm><laser-tx-power-high-warn-threshold>0.6310</laser-tx-power-high-warn-threshold><laser-tx-power-high-warn-threshold-dbm>-2.00</laser-tx-power-high-warn-threshold-dbm><laser-tx-power-low-warn-threshold>0.0790</laser-tx-power-low-warn-threshold><laser-tx-power-low-warn-threshold-dbm>-11.02</laser-tx-power-low-warn-threshold-dbm><module-temperature-high-alarm-threshold celsius="110.0">110 degrees C / 230 degrees F</module-temperature-high-alarm-threshold><module-temperature-low-alarm-threshold celsius="-40.0">-40 degrees C / -40 degrees F</module-temperature-low-alarm-threshold><module-temperature-high-warn-threshold celsius="93.0">93 degrees C / 199 degrees F</module-temperature-high-warn-threshold><module-temperature-low-warn-threshold celsius="-30.0">-30 degrees C / -22 degrees F</module-temperature-low-warn-threshold><module-voltage-high-alarm-threshold>3.900</module-voltage-high-alarm-threshold><module-voltage-low-alarm-threshold>2.700</module-voltage-low-alarm-threshold><module-voltage-high-warn-threshold>3.700</module-voltage-high-warn-threshold><module-voltage-low-warn-threshold>2.900</module-voltage-low-warn-threshold><laser-rx-power-high-alarm-threshold>1.2589</laser-rx-power-high-alarm-threshold><laser-rx-power-high-alarm-threshold-dbm>1.00</laser-rx-power-high-alarm-threshold-dbm><laser-rx-power-low-alarm-threshold>0.0100</laser-rx-power-low-alarm-threshold><laser-rx-power-low-alarm-threshold-dbm>-20.00</laser-rx-power-low-alarm-threshold-dbm><laser-rx-power-high-warn-threshold>0.7943</laser-rx-power-high-warn-threshold><laser-rx-power-high-warn-threshold-dbm>-1.00</laser-rx-power-high-warn-threshold-dbm><laser-rx-power-low-warn-threshold>0.0158</laser-rx-power-low-warn-threshold><laser-rx-power-low-warn-threshold-dbm>-18.01</laser-rx-power-low-warn-threshold-dbm></optics-diagnostics></physical-interface></interface-information>
'''
        root2 = ET.fromstring(xml4)
        self.jobject.execute_rpc = MagicMock(
            side_effect=[Response(response=root1), Response(response=root2)])
        intf = "ge-0/0/0"
        actual_result = self.jobject._Jpg__get_interface_status(intf=intf)
        expected_result = "Optics Missing"

        self.assertEqual(actual_result, expected_result,
                         "Wrong return, Unexpected result")
        logging.info("\tPassed")

    def test__verify_cprod_response(self):
        ######################################################################
        logging.info("Test case 1: Execute function with response does not " +
                     "contain err:No route to host")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        response = "Connected"
        actual_result = self.jobject._Jpg__verify_cprod_response(response)

        self.assertTrue(actual_result, "Result should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Execute function with response " +
                     "contains err:No route to host")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        self.jobject.channels = []
        response = "err:No route to host"
        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__verify_cprod_response(response)
        self.assertTrue('System is in Error state' in str(context.exception))
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Execute function with response " +
                     "is empty")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        response = ""
        actual_result = self.jobject._Jpg__verify_cprod_response(response)

        self.assertTrue(actual_result, "Result should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Run with real devices and using cli method")
        self.jobject.log = MagicMock()
        self.jobject.cli = MagicMock(side_effect=[Response(response="")])
        cmd = "cprod -A fpc0 -c \"show nhdb summary\""
        res = self.jobject.cli(command=cmd, format='text')
        result = self.jobject._Jpg__verify_cprod_response(res.response())

        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")

    @patch('time.sleep', return_value=None)
    def test___get_intf_nhid(self, patch_time_sleep):
        ######################################################################
        logging.info("Testcase 1: run successfully with valid res")
        self.jobject.log = MagicMock()
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        shell_cprod = '''
807(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:Flood)
    751(Compst, BRIDGE, ifl:0:-, pfe-id:0, comp-fn:SH)
        724(Unicast, BRIDGE, ifl:387:xe-5/3/1.0, pfe-id:21)
        720(Unicast, BRIDGE, ifl:385:xe-4/1/3.0, pfe-id:16)
'''

        self.jobject.shell = MagicMock(
            side_effect=["", Response(response=shell_cprod)])

        result = self.jobject._Jpg__get_intf_nhid("fpc_1", "888", "ge-4/1/3")
        self.assertEqual(int(result), 807)
        logging.info("\tPassed")

        ######################################################################
        logging.info("Testcase 2: run with invalid res")
        self.jobject.log = MagicMock()
        self.jobject._Jpg__verify_cprod_response = MagicMock()
        self.jobject._Jpg__get_interface_status = MagicMock()
        res_list = []
        for i in range(1, 21):
            res_list.append(Response(response=""))

        self.jobject.shell = MagicMock(side_effect=res_list)
        self.jobject.channels =[] # Used when TobyException is raised
        with self.assertRaises(Exception) as context:
            self.jobject._Jpg__get_intf_nhid("fpc_1", "888", "ge-4/1/3")
        self.assertTrue('Unable to get nhid for' in str(context.exception))
        logging.info("\tPassed")

    def test_set_jpg_interfaces(self):
        ######################################################################
        logging.info("Test case 1: Set JPG interfaces successfully")
        self.jobject.log = MagicMock()
        self.jobject.interfaces = {}
        intf = {'ge-2/1/3': {}, 'xe-3/5/5': {}}
        self.jobject.set_jpg_interfaces(intf)
        self.assertEqual(self.jobject.interfaces, intf,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

    def test_reset_jpg_config(self):
        ######################################################################
        logging.info("Test case 1: Set JPG interfaces successfully")
        self.jobject.log = MagicMock()
        self.jobject.interfaces = {}
        intf = {'ge-2/1/3': {}, 'xe-3/5/5': {}}
        self.jobject._Jpg__reset_jpg_config = MagicMock(return_value=True)
        self.jobject.inout_intf_pair = ['fe-0/1/2|ge-1/2/3']
        result = self.jobject.reset_jpg_config()
        self.assertEqual(result, True, "Return should be True")
        self.jobject.inout_intf_pair = []
        result = self.jobject.reset_jpg_config()
        self.assertEqual(result, True, "Return should be True")
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.connect_to_jpg_device')
    def test_public_set_jpg_interfaces(self, dev):
        ######################################################################
        logging.info("Test case 1: Set JPG interfaces successfully")
        self.jobject.log = MagicMock()
        dev.return_value = MagicMock(return_value=None)
        dev.current_node = MagicMock()
        dev.current_node.current_controller = MagicMock()
        intf = {'test': 1}
        dev.current_node.current_controller.set_jpg_interfaces = \
            MagicMock(return_value=self.jobject.set_jpg_interfaces(intf))
        set_jpg_interfaces(dev, intf)
        self.assertEqual(self.jobject.interfaces, intf,
                         "Return is incorrect as expectation")
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.Jpg.__init__')
    def test_public_connect_to_jpg_device(self, jpg_dev):
        ######################################################################
        jpg_dev.return_value = None
        logging.info("Test case 1: Verify connect_to_jpg_device")
        self.jobject.log = MagicMock()
        dev = connect_to_jpg_device(host='1.1.1.1')

        self.assertEqual(type(dev), Jpg, "dev is not Jpg")
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.connect_to_jpg_device')
    def test_public_configure_jpg(self, dev):
        ######################################################################
        logging.info("Test case 1: Verify configure_jpg passed")
        self.jobject.log = MagicMock()
        dev.return_value = MagicMock(return_value=None)
        dev.configure_jpg = MagicMock(return_value=True)
        result = configure_jpg(dev)

        self.assertEqual(result, True, "return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Verify configure_jpg failed")
        dev.configure_jpg = MagicMock(return_value=None)

        with self.assertRaises(Exception) as context:
            configure_jpg(dev)
        self.assertTrue('Cannot configure Jpg' in str(context.exception))
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.connect_to_jpg_device')
    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.connect_to_jpg_device')
    def test_public_configure_jpg_replication(self, dev1, dev2):
        ######################################################################
        logging.info("Test case 1: Verify configure_jpg_replication passed")
        self.jobject.log = MagicMock()
        dev1.return_value = MagicMock(return_value=None)
        dev2.return_value = MagicMock(return_value=None)
        dev1._Jpg__jpg_replication_module = MagicMock(return_value=True)
        dev2._Jpg__jpg_replication_module = MagicMock(return_value=True)
        result = configure_jpg_replication([dev1, dev2])

        self.assertEqual(result, True, "return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Verify configure_jpg_replication failed")
        dev1._Jpg__jpg_replication_module = MagicMock(
            side_effect=Exception('Test'))
        dev2._Jpg__jpg_replication_module = MagicMock(
            side_effect=Exception('Test'))

        with self.assertRaises(Exception) as context:
            configure_jpg_replication([dev1, dev2])
        self.assertTrue('Cannot configure Jpg replication '
                        'on devices' in str(context.exception))
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.connect_to_jpg_device')
    def test_public_setup_jpg_filter(self, dev):
        ######################################################################
        logging.info("Test case 1: Verify setup_jpg_filter passed")
        self.jobject.log = MagicMock()
        dev.return_value = MagicMock(return_value=None)
        dev.setup_jpg_filter = MagicMock(return_value=True)
        result = setup_jpg_filter(dev)

        self.assertEqual(result, True, "return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Verify setup_jpg_filter failed")
        dev.setup_jpg_filter = MagicMock(return_value=False)

        try:
            setup_jpg_filter(dev)
        except Exception as exp:
            self.assertEqual(exp.args[0], 'Cannot setup Jpg filter')

        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.connect_to_jpg_device')
    def test_public_attach_jpg_filter(self, dev):
        ######################################################################
        logging.info("Test case 1: Verify attach_jpg_filter passed")
        self.jobject.log = MagicMock()
        dev.return_value = MagicMock(return_value=None)
        dev.attach_jpg_filter = MagicMock(return_value=True)
        result = attach_jpg_filter(dev)

        self.assertEqual(result, True, "return should be True")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Verify attach_jpg_filter failed")
        dev.attach_jpg_filter = MagicMock(return_value=False)

        with self.assertRaises(Exception) as context:
            attach_jpg_filter(dev)
        self.assertTrue('Cannot attach Jpg filter' in str(context.exception))
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.juniper.jpg.jpg.connect_to_jpg_device')
    def test_public_get_jpg_stats(self, dev):
        ######################################################################
        logging.info("Test case 1: Verify get_jpg_stats passed")
        self.jobject.log = MagicMock()
        dev.return_value = MagicMock(return_value=None)
        dev.get_jpg_stats = MagicMock(return_value={'a': 1})
        result = get_jpg_stats(dev)

        self.assertGreater(len(result), 0, "Statistics dict is Empty")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Verify get_jpg_stats failed")
        dev.get_jpg_stats = MagicMock(return_value={})

        with self.assertRaises(Exception) as context:
            get_jpg_stats(dev)
        self.assertTrue('Cannot get Jpg statistics' in str(context.exception))
        logging.info("\tPassed")

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name + ".log", level=logging.INFO)
    unittest.main()

