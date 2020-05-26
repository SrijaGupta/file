#! /usr/local/bin/python3

from mock import patch
import unittest
from mock import MagicMock
import unittest
from jnpr.toby.fabric import fabric

class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class TestFabric(unittest.TestCase):
    mocked_obj = MagicMock()
    mocked_obj.log = MagicMock()
    mocked_obj.cli = MagicMock()

    # Test check_chas_fabric_topology

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_check_chas_fabric_topology(self,get_fru_slots):

        xml = '''  In-link  : FPC# FE# ASIC# (TX inst#, TX sub-chnl #) ->
            SIB# ASIC#_FCORE# (RX port#, RX sub-chn#, RX inst#)

             Out-link : SIB# ASIC#_FCORE# (TX port#, TX sub-chn#, TX inst#) ->
            FPC# FE# ASIC# (RX inst#, RX sub-chnl #)
            SIB 0 FCHIP 0 FCORE 0 :
            ----------------------
            in-links               State             Out-links              State
            --------------------------------------------------------------------------------
            FPC00FE0(1,17)->S00F0_0(00,0,00) OK      S00F0_0(16,2,16)->FPC00FE0(1,17) OK
            FPC00FE1(1,14)->S00F0_0(00,2,00) OK      S00F0_0(16,0,16)->FPC00FE1(1,14) OK
            FPC00FE2(1,16)->S00F0_0(19,2,19) OK      S00F0_0(15,6,15)->FPC00FE2(1,16) OK

            SIB 0 FCHIP 1 FCORE 0 :
            -----------------------
            In-links               State             Out-links              State
            --------------------------------------------------------------------------------
            FPC00FE0(1,13)->S00F1_0(16,7,16) OK      S00F1_0(17,6,17)->FPC00FE0(1,13) OK
            FPC00FE1(1,10)->S00F1_0(16,4,16) OK      S00F1_0(17,4,17)->FPC00FE1(1,10) OK
            FPC00FE2(1,12)->S00F1_0(17,2,17) OK      S00F1_0(17,2,17)->FPC00FE2(1,12) OK

            SIB 0 FCHIP 2 FCORE 0 :
            -----------------------
            In-links               State             Out-links              State
            --------------------------------------------------------------------------------
            FPC00FE0(1,09)->S00F2_0(18,3,18) OK      S00F2_0(13,1,13)->FPC00FE0(1,09) OK
            FPC00FE1(1,06)->S00F2_0(18,1,18) OK      S00F2_0(13,3,13)->FPC00FE1(1,06) OK
            FPC00FE2(1,08)->S00F2_0(18,7,18) OK      S00F2_0(13,5,13)->FPC00FE2(1,08) OK

            SIB 0 FCHIP 3 FCORE 0 :
            -----------------------
            In-links               State             Out-links              State
            --------------------------------------------------------------------------------
            FPC00FE0(1,15)->S00F3_0(19,7,19) OK      S00F3_0(01,5,01)->FPC00FE0(1,15) OK
            FPC00FE1(1,16)->S00F3_0(19,5,19) OK      S00F3_0(01,7,01)->FPC00FE1(1,16) OK
            FPC00FE2(1,14)->S00F3_0(19,3,19) OK      S00F3_0(01,1,01)->FPC00FE2(1,14) OK

            SIB 0 FCHIP 4 FCORE 0 :
            -----------------------
            In-links               State             Out-links              State
            --------------------------------------------------------------------------------
            FPC00FE0(1,11)->S00F4_0(12,5,12) OK      S00F4_0(14,7,14)->FPC00FE0(1,11) OK
            FPC00FE1(1,12)->S00F4_0(12,7,12) OK      S00F4_0(14,5,14)->FPC00FE1(1,12) OK
            FPC00FE2(1,10)->S00F4_0(12,3,12) OK      S00F4_0(13,5,13)->FPC00FE2(1,10) OK

            SIB 0 FCHIP 5 FCORE 0 :
            -----------------------
            In-links               State             Out-links              State
            --------------------------------------------------------------------------------
            FPC00FE0(1,07)->S00F5_0(13,0,13) OK      S00F5_0(17,7,17)->FPC00FE0(1,07) OK
            FPC00FE1(1,08)->S00F5_0(13,2,13) OK      S00F5_0(17,5,17)->FPC00FE1(1,08) OK
            FPC00FE2(1,06)->S00F5_0(13,4,13) OK      S00F5_0(18,3,18)->FPC00FE2(1,06) OK

        '''
        get_fru_slots.return_value = [0]
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.check_chas_fabric_topology(self.mocked_obj,None,None,None,None,None,None,None,36)
        self.assertEqual(val, 1 , '\t Passed : show chassis fabric topology')
 
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.check_chas_fabric_topology(self.mocked_obj,None,None,None,None,None,None,None,3)
        self.assertEqual(val, 0 , '\t Passed : show chassis fabric topology')

        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.check_chas_fabric_topology(self.mocked_obj,0,0,0,0,0,"OK","OK",None)
        self.assertEqual(val, 1 , '\t Passed : show chassis fabric topology')

        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.check_chas_fabric_topology(self.mocked_obj,0,0,0,0,0,"Error","Error",None)
        self.assertEqual(val, 0 , '\t Passed : show chassis fabric topology')

        try:
            fabric.check_chas_fabric_topology() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")
 
    # Test get_fpc_fabric_connection_info

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_get_fpc_fabric_connection_info(self,get_fru_slots):
        xml = '''<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
        <fpc>
            <slot>0</slot>
            <state>Online</state>
            <description>LC1102 - 12C / 36Q / 144X</description>
            <pic>
                <pic-slot>0</pic-slot>
                <pic-state>Online</pic-state>
                <pic-type>12x100GE/36x40GE/144x10GE</pic-type>
            </pic>
        </fpc>
        <fpc>
            <slot>3</slot>
            <state>Offline</state>
            <description>LC1101 - 30C / 30Q / 96X</description>
        </fpc>
        <fpc>
            <slot>8</slot>
            <state>Offline</state>
            <description>LC1101 - 30C / 30Q / 96X</description>
        </fpc>
        <fpc>
            <slot>9</slot>
            <state>Offline</state>
            <description>LC1103 - 2C / 6Q / 60X</description>
        </fpc>
        <fpc>
            <slot>10</slot>
            <state>Offline</state>
            <description>LC1101 - 30C / 30Q / 96X</description>
        </fpc>
        <fpc>
            <slot>13</slot>
            <state>Offline</state>
            <description>LC1101 - 30C / 30Q / 96X</description>
        </fpc>
        <fpc>
            <slot>15</slot>
            <state>Offline</state>
            <description>LC1102 - 12C / 36Q / 144X</description>
        </fpc>
    </fpc-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''
        get_fru_slots.return_value = [0]
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.get_fpc_fabric_connection_info(self.mocked_obj,6,None)
        val = val['total']
        self.assertEqual(val, 18 , '\t Passed : get_fpc_fabric_connection_info')

        xml = '''<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
        <fpc>
            <slot>0</slot>
            <state>Online</state>
            <description>LC1101 - 12C / 36Q / 144X</description>
            <pic>
                <pic-slot>0</pic-slot>
                <pic-state>Online</pic-state>
                <pic-type>12x100GE/36x40GE/144x10GE</pic-type>
            </pic>
        </fpc>
        <fpc>
            <slot>15</slot>
            <state>Offline</state>
            <description>LC1102 - 12C / 36Q / 144X</description>
        </fpc>
    </fpc-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''
        get_fru_slots.return_value = [0]
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.get_fpc_fabric_connection_info(self.mocked_obj,6,None)
        val = val['total']
        self.assertEqual(val, 36 , '\t Passed : get_fpc_fabric_connection_info')

        xml = '''<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <fpc-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="pic-style">
        <fpc>
            <slot>0</slot>
            <state>Online</state>
            <description>FPC - 12C / 36Q / 144X</description>
            <pic>
                <pic-slot>0</pic-slot>
                <pic-state>Online</pic-state>
                <pic-type>12x100GE/36x40GE/144x10GE</pic-type>
            </pic>
        </fpc>
        <fpc>
            <slot>15</slot>
            <state>Offline</state>
            <description>LC1102 - 12C / 36Q / 144X</description>
        </fpc>
    </fpc-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''
        get_fru_slots.return_value = [0]
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.get_fpc_fabric_connection_info(self.mocked_obj,6,None)
        val = val['total']
        self.assertEqual(val, 24 , '\t Passed : get_fpc_fabric_connection_info')



        try:
            fabric.get_fpc_fabric_connection_info() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")

    # Test get_fpc_ccl_link
    
    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_get_fpc_ccl_link(self,get_fru_slots):
        output = """
        LinkMap:
        ========
           Logical   Physical     Serdes
        ==================================
                 0          100         26
        """
        get_fru_slots.return_value = [0]
        self.mocked_obj.vty = MagicMock(side_effect=[Response(output)])

        val = fabric.get_fpc_ccl_link(self.mocked_obj,0,'pe',0,0,0)
        val = int(val[0]['physical'])
        self.assertEqual(val, 100 , '\t Passed : get_fpc_fabric_connection_info')

        try:
            fabric.get_fpc_ccl_link() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")

        output = """
        PE0 Rx Instance 0 LinkMap:
            sc_num    Logical   Physical     Serdes   tdm_slot
        ======================================================
                 0          0          0          8        255

                 1          1          1          9        255

                 2          2          2         10        255

                 3          3          3         11        255

        """
        self.mocked_obj.vty = MagicMock(side_effect=[Response(output)])
        val = fabric.get_fpc_ccl_link(self.mocked_obj,0,'pe',0,0,None)
        val = val[0]
        val = int(val['physical'])
        self.assertEqual(val, 3 , '\t Passed : get_fpc_fabric_connection_info')



    # Test get_sib_ccl_link

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_get_sib_ccl_link(self,get_fru_slots):
        output = """
        LinkMap:
        ========
           Logical   Physical     Serdes
        ==================================
                 0          200          5
        """
        get_fru_slots.return_value = [0]
        self.mocked_obj.vty = MagicMock(side_effect=[Response(output)])
        val = fabric.get_sib_ccl_link(self.mocked_obj,'spmb0',0,'pf',0,0,0)
        val = int(val[0]['physical'])
        self.assertEqual(val, 200 , '\t Passed : get_sib_ccl_link')

        output = """
        SIB0_PF_0 Rx Instance 0 LinkMap:
            sc_num    Logical   Physical     Serdes   tdm_slot
        ======================================================
                 0          0          1          5        255

                 2          2          2          7        255

                 4          4          4          9        255

                 6          6          6         11        255

        """
        self.mocked_obj.vty = MagicMock(side_effect=[Response(output)])
        val = fabric.get_sib_ccl_link(self.mocked_obj,'spmb0',0,'pf',0,0,None)
        val = val[0]
        val = int(val['physical'])
        self.assertEqual(val, 6 , '\t Passed : get_sib_ccl_link')

        try:
            fabric.get_sib_ccl_link() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")

    # Test corrupt_crc_fpc_to_sib

    def test_corrupt_crc_fpc_to_sib(self):
        output = """
        None
        """
        self.mocked_obj.vty = MagicMock(side_effect=[Response(output)])
        val = fabric.corrupt_crc_fpc_to_sib(self.mocked_obj,0,"pe",0,0,1,10,10)
        self.assertEqual(val, 1 , '\t Passed : corrupt_crc_fpc_to_sib')

        try:
            fabric.corrupt_crc_fpc_to_sib() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")

    # Test corrupt_crc_sib_to_fpc

    def test_corrupt_crc_sib_to_fpc(self):
        output = """
        None
        """
        self.mocked_obj.vty = MagicMock(side_effect=[Response(output)])
        val = fabric.corrupt_crc_sib_to_fpc(self.mocked_obj,"spmb0",0,"pf",0,0,1,10,10)
        self.assertEqual(val, 1 , '\t Passed : corrupt_crc_sib_to_fpc')

        try:
            fabric.corrupt_crc_sib_to_fpc() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")

    # Test check_autoheal

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_check_autoheal(self,get_fru_slots):
        lst = [Response("Count: 2 lines")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(fabric.check_autoheal(self.mocked_obj,1,1,None), 1)
        lst = [Response("Count: 0 lines")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(fabric.check_autoheal(self.mocked_obj,1,1,None), 0)
        lst = [Response("Count: 2 lines")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        self.assertEqual(fabric.check_autoheal(self.mocked_obj,1,None,1), 1)

        try:
            fabric.check_autoheal() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")
    # Test  get_re_sib_state

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_get_re_sib_state(self,get_fru_slots):

        xml = '''<rpc-reply xmlns:junos="http://xml.juniper.net/junos/15.1F5/junos">
         <sib-information xmlns="http://xml.juniper.net/junos/15.1F5/junos-chassis" junos:style="brief1">
         <sib>
            <slot>7</slot>
            <state>Online</state>
            <sib-link-state>Active</sib-link-state>
            <sib-link-errors>None</sib-link-errors>
         </sib>
         <sib>
            <slot>8</slot>
            <state>Online</state>
            <sib-link-state>Active</sib-link-state>
            <sib-link-errors>None</sib-link-errors>
          </sib>
         </sib-information>
         <cli>
         <banner></banner>
         </cli>
         </rpc-reply>
         '''
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.get_re_sib_state(self.mocked_obj)
        expected_result = [{'linkstate': 'Active', 'linkerror': 'None', 'state': 'Online', 'slot': 7}, {'linkstate': 'Active', 'linkerror': 'None', 'state': 'Online', 'slot': 8}]
        self.assertEqual(val, expected_result , '\t Passed : show chassis sib')

        try:
            fabric.get_re_sib_state() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")
    # Test check_chassis_sib

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_check_chassis_sib(self,get_fru_slots):

        with patch('jnpr.toby.fabric.fabric.get_re_sib_state') as get_sib:
            get_sib.return_value = [{'linkstate': 'Active', 'linkerror': 'None', 'state': 'Online', 'slot': 7}, {'linkstate': 'Active', 'linkerror': 'None', 'state': 'Online', 'slot': 8}]
            val = fabric.check_chassis_sib(self.mocked_obj,8,"Online","Active","None")
            self.assertEqual(val, 1 , '\t Passed : check chassis sib')
            val = fabric.check_chassis_sib(self.mocked_obj,8,"Online","error","None")
            self.assertEqual(val, 0 , '\t Passed : check chassis sib')
            val = fabric.check_chassis_sib(self.mocked_obj,8,None,None,None)
            self.assertEqual(val, 1 , '\t Passed : check chassis sib')

        try:
            fabric.check_chassis_sib() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")
    # Test get_fpc_sib_links

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_get_fpc_sib_links(self,get_fru_slots):

        lst = [Response("FPC02FE0(2,04)->S02F0_0(14,0,14) OK      S02F0_0(14,0,14)->FPC02FE0(2,04) OK")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        val = fabric.get_fpc_sib_links(self.mocked_obj,2,2,0,0,0,1,None,None,1)
        self.assertEqual(val, 4 , '\t Passed : get_fpc_sib_links')
        lst = [Response("FPC02FE0(2,04)->S02F0_0(14,0,14) OK      S02F0_0(14,0,14)->FPC02FE0(2,04) OK")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        val = fabric.get_fpc_sib_links(self.mocked_obj,2,2,0,0,0,1,None,1,None)
        self.assertEqual(val, 2 , '\t Passed : get_fpc_sib_links')
        lst = [Response("FPC02FE0(2,04)->S02F0_0(14,0,14) OK      S02F0_0(14,0,14)->FPC02FE0(2,04) OK")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        val = fabric.get_fpc_sib_links(self.mocked_obj,2,2,0,0,0,None,1,1,None)
        self.assertEqual(val, 14 , '\t Passed : get_fpc_sib_links')

        lst = [Response("FPC02FE0(2,04)->S02F0_0(14,0,14) OK      S02F0_0(14,0,14)->FPC02FE0(2,04) OK")]
        self.mocked_obj.cli = MagicMock(side_effect=lst)
        val = fabric.get_fpc_sib_links(self.mocked_obj,2,2,0,0,0,None,1,None,1)
  
        try:
            fabric.get_fpc_sib_links() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")
    # Test get_chassis_fabric_sib
 
    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_get_chassis_fabric_sib(self,get_fru_slots):

        xml = '''<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
        <fm-qfx10-sib-state-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="brief1-q">
        <fms-sib-ln1-q>
            <sib-slot-q>0</sib-slot-q>
            <sib-fms-state1-q>Online</sib-fms-state1-q>
            <fms-asic-ln-q>
                <sib-asic-q>0</sib-asic-q>
                <sib-plane-q>0</sib-plane-q>
                <sib-fms-asic-state-q>Active</sib-fms-asic-state-q>
                <fms-asic-fpc-ln-q>
                    <slot>0</slot>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>0</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>1</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>2</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                </fms-asic-fpc-ln-q>
            </fms-asic-ln-q>
            <fms-asic-ln-q>
                <sib-asic-q>1</sib-asic-q>
                <sib-plane-q>1</sib-plane-q>
                <sib-fms-asic-state-q>Active</sib-fms-asic-state-q>
                <fms-asic-fpc-ln-q>
                    <slot>0</slot>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>0</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>1</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>2</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                </fms-asic-fpc-ln-q>
            </fms-asic-ln-q>
            <fms-asic-ln-q>
                <sib-asic-q>2</sib-asic-q>
                <sib-plane-q>2</sib-plane-q>
                <sib-fms-asic-state-q>Active</sib-fms-asic-state-q>
                <fms-asic-fpc-ln-q>
                    <slot>0</slot>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>0</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>1</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>2</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                </fms-asic-fpc-ln-q>
            </fms-asic-ln-q>
            <fms-asic-ln-q>
                <sib-asic-q>3</sib-asic-q>
                <sib-plane-q>3</sib-plane-q>
                <sib-fms-asic-state-q>Active</sib-fms-asic-state-q>
                <fms-asic-fpc-ln-q>
                    <slot>0</slot>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>0</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>1</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>2</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                </fms-asic-fpc-ln-q>
            </fms-asic-ln-q>
            <fms-asic-ln-q>
                <sib-asic-q>4</sib-asic-q>
                <sib-plane-q>4</sib-plane-q>
                <sib-fms-asic-state-q>Active</sib-fms-asic-state-q>
                <fms-asic-fpc-ln-q>
                    <slot>0</slot>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>0</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>1</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>2</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                </fms-asic-fpc-ln-q>
            </fms-asic-ln-q>
            <fms-asic-ln-q>
                <sib-asic-q>5</sib-asic-q>
                <sib-plane-q>5</sib-plane-q>
                <sib-fms-asic-state-q>Active</sib-fms-asic-state-q>
                <fms-asic-fpc-ln-q>
                    <slot>0</slot>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>0</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>1</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                    <fms-asic-pfe-ln-q>
                        <pfe-slot-q>2</pfe-slot-q>
                        <fms-asic-pfe-link-state-q>OK</fms-asic-pfe-link-state-q>
                    </fms-asic-pfe-ln-q>
                </fms-asic-fpc-ln-q>
            </fms-asic-ln-q>
        </fms-sib-ln1-q>
        <fms-sib-ln1-q>
            <sib-slot-q>1</sib-slot-q>
            <sib-fms-state1-q>Offline</sib-fms-state1-q>
        </fms-sib-ln1-q>
        <fms-sib-ln1-q>
            <sib-slot-q>2</sib-slot-q>
            <sib-fms-state1-q>Offline</sib-fms-state1-q>
        </fms-sib-ln1-q>
        <fms-sib-ln1-q>
            <sib-slot-q>3</sib-slot-q>
            <sib-fms-state1-q>Offline</sib-fms-state1-q>
        </fms-sib-ln1-q>
        <fms-sib-ln1-q>
            <sib-slot-q>4</sib-slot-q>
            <sib-fms-state1-q>Offline</sib-fms-state1-q>
        </fms-sib-ln1-q>
        <fms-sib-ln1-q>
            <sib-slot-q>5</sib-slot-q>
            <sib-fms-state1-q>Offline</sib-fms-state1-q>
        </fms-sib-ln1-q>
    </fm-qfx10-sib-state-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.get_chassis_fabric_sib(self.mocked_obj)
        expected_result = [{'sibslot': 0, 'state': 'Online', 'core': [{'planestate': 'Active', 'plane': 0, 'fcore': 0, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 1, 'fcore': 1, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 2, 'fcore': 2, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 3, 'fcore': 3, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 4, 'fcore': 4, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 5, 'fcore': 5, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}]}]
        self.assertEqual(val, expected_result , '\t Passed : show chassis fabric sib')

        try:
            fabric.get_chassis_fabric_sib() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")
    # Test check_chassis_fabric_sib

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_check_chassis_fabric_sib(self,get_fru_slots):

        with patch('jnpr.toby.fabric.fabric.get_chassis_fabric_sib') as get_fabric_sib:
            with patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots') as get_fru_slots:
                get_fabric_sib.return_value =  [{'sibslot': 0, 'state': 'Online', 'core': [{'planestate': 'Active', 'plane': 0, 'fcore': 0, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 1, 'fcore': 1, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 2, 'fcore': 2, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 3, 'fcore': 3, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 4, 'fcore': 4, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 5, 'fcore': 5, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}]}]
                get_fru_slots.return_value = [0]
                val = fabric.check_chassis_fabric_sib(self.mocked_obj,None,None,None,None,None,None,18)
                self.assertEqual(val, 1 , '\t Passed : check chassis fabric sib')
                val = fabric.check_chassis_fabric_sib(self.mocked_obj,None,None,None,None,None,None,8)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric sib')
                val = fabric.check_chassis_fabric_sib(self.mocked_obj,0,0,0,0,0,"OK",None)
                self.assertEqual(val, 1 , '\t Passed : check chassis fabric sib')
                val = fabric.check_chassis_fabric_sib(self.mocked_obj,0,0,0,0,0,"error",None)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric sib')

                get_fabric_sib.return_value =  [{'sibslot': 0, 'state': 'Online', 'core': [{'planestate': 'Active', 'plane': 0, 'fcore': 0, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'down'}, {'pfenum': 1, 'linkstate': 'down'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 1, 'fcore': 1, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 2, 'fcore': 2, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 3, 'fcore': 3, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 4, 'fcore': 4, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}, {'planestate': 'Active', 'plane': 5, 'fcore': 5, 'fpc': [{'pfe': [{'pfenum': 0, 'linkstate': 'OK'}, {'pfenum': 1, 'linkstate': 'OK'}, {'pfenum': 2, 'linkstate': 'OK'}], 'fpcslot': 0}]}]}]
                get_fru_slots.return_value = [0]
                val = fabric.check_chassis_fabric_sib(self.mocked_obj,0,0,0,0,0,"Error",None)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric sib')
                val = fabric.check_chassis_fabric_sib(self.mocked_obj,None,None,None,None,None,None,None)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric sib')



        try:
            fabric.check_chassis_fabric_sib() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing")
    # Test get_chassis_fabric_fpc

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_get_chassis_fabric_fpc(self,get_fru_slots):



        xml = '''<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.4D0/junos">
    <fm-qfx10-fpc-state-information xmlns="http://xml.juniper.net/junos/17.4D0/junos-chassis" junos:style="brief1-q">
        <fm-fpc-ln1-q>
            <fpc-slot1-q>0</fpc-slot1-q>
            <fm-pfe-ln1-q>
                <pfe-slot1-q>0</pfe-slot1-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>0</sib-asic-q>
                    <sib-plane-q> 0</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>1</sib-asic-q>
                    <sib-plane-q> 1</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>2</sib-asic-q>
                    <sib-plane-q> 2</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>3</sib-asic-q>
                    <sib-plane-q> 3</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>4</sib-asic-q>
                    <sib-plane-q> 4</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>5</sib-asic-q>
                    <sib-plane-q> 5</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
            </fm-pfe-ln1-q>
            <fm-pfe-ln1-q>
                <pfe-slot1-q>1</pfe-slot1-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>0</sib-asic-q>
                    <sib-plane-q> 0</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>1</sib-asic-q>
                    <sib-plane-q> 1</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>2</sib-asic-q>
                    <sib-plane-q> 2</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>3</sib-asic-q>
                    <sib-plane-q> 3</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>4</sib-asic-q>
                    <sib-plane-q> 4</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>5</sib-asic-q>
                    <sib-plane-q> 5</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
            </fm-pfe-ln1-q>
            <fm-pfe-ln1-q>
                <pfe-slot1-q>2</pfe-slot1-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>0</sib-asic-q>
                    <sib-plane-q> 0</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>1</sib-asic-q>
                    <sib-plane-q> 1</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>2</sib-asic-q>
                    <sib-plane-q> 2</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>3</sib-asic-q>
                    <sib-plane-q> 3</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>4</sib-asic-q>
                    <sib-plane-q> 4</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
                <fm-pfe-asic-ln-q>
                    <sib-slot-q>0</sib-slot-q>
                    <sib-asic-q>5</sib-asic-q>
                    <sib-plane-q> 5</sib-plane-q>
                    <pfe-asic-link-state-q> Plane Enabled, Links OK</pfe-asic-link-state-q>
                </fm-pfe-asic-ln-q>
            </fm-pfe-ln1-q>
        </fm-fpc-ln1-q>
    </fm-qfx10-fpc-state-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''
        self.mocked_obj.cli = MagicMock(side_effect=[Response(xml)])
        val = fabric.get_chassis_fabric_fpc(self.mocked_obj)
        expected_result = [{'pfe': [{'pfenum': 0, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}, {'pfenum': 1, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}, {'pfenum': 2, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}], 'fpcslot': 0}]

        self.assertEqual(val, expected_result , '\t Passed : show chassis fabric fpc')

        try:
            fabric.get_chassis_fabric_fpc() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing ")

    # Test check_chassis_fabric_fpc

    @patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots')
    def test_check_chassis_fabric_fpc(self,get_fru_slots):


        with patch('jnpr.toby.fabric.fabric.get_chassis_fabric_fpc') as get_fabric_fpc:
            with patch('jnpr.toby.fabric.fabric.chassis.get_fru_slots') as get_fru_slots:
                get_fabric_fpc.return_value = [{'pfe': [{'pfenum': 0, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}, {'pfenum': 1, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}, {'pfenum': 2, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}], 'fpcslot': 0}]
                get_fru_slots.return_value = [0]
                val = fabric.check_chassis_fabric_fpc(self.mocked_obj,None,None,None,None,None,None,None,18)
                self.assertEqual(val, 1 , '\t Passed : check chassis fabric fpc')

                val = fabric.check_chassis_fabric_fpc(self.mocked_obj,None,None,None,None,None,None,None,1)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric fpc')
                val = fabric.check_chassis_fabric_fpc(self.mocked_obj,0,0,0,0,0,"Enabled","OK",None)
                self.assertEqual(val, 1 , '\t Passed : check chassis fabric fpc')
                val = fabric.check_chassis_fabric_fpc(self.mocked_obj,0,0,0,0,0,"Enabled","Error",None)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric fpc')

                get_fabric_fpc.return_value = [{'pfe': [{'pfenum': 0, 'planelink': [{'linkstate': 'Plane disabled, Links Error', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}, {'pfenum': 1, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}, {'pfenum': 2, 'planelink': [{'linkstate': 'Plane Enabled, Links OK', 'plane': 0, 'sib': 0, 'fcore': 0}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 1, 'sib': 0, 'fcore': 1}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 2, 'sib': 0, 'fcore': 2}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 3, 'sib': 0, 'fcore': 3}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 4, 'sib': 0, 'fcore': 4}, {'linkstate': 'Plane Enabled, Links OK', 'plane': 5, 'sib': 0, 'fcore': 5}]}], 'fpcslot': 0}]
                get_fru_slots.return_value = [0]
                val = fabric.check_chassis_fabric_fpc(self.mocked_obj,0,0,0,0,0,"Enabled","OK",None)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric fpc')
                val = fabric.check_chassis_fabric_fpc(self.mocked_obj,None,None,None,None,None,None,None,None)
                self.assertEqual(val, 0 , '\t Passed : check chassis fabric fpc')


        try:
            fabric.check_chassis_fabric_fpc() 
        except Exception as err:
            self.assertEqual( err.args[0], "Mandatory arguements are missing")


if __name__ == '__main__':
    unittest.main()

