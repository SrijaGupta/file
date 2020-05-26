"""All unit test cases for CHASSIS module"""
__author__ = ['Baba Syed Mazaz Hussain']
__contact__ = 'babasyedm@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import unittest
import logging
import sys,os,logging
from jnpr.toby.hldcl.juniper.junos import Juniper

from jnpr.toby.hardware.chassis import chassis
from mock import patch, MagicMock, Mock
from jnpr.toby.hldcl.unix.unix import Unix
from jnpr.toby.hldcl.unix.unix import FreeBSD
from jnpr.toby.utils.response import Response
from lxml import etree
import time
import ast,jxmlease
from optparse import Values
from jnpr.toby.security.macsec import macsec


class UnitTest(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
        t.get_handle = MagicMock()

    def test_get_lowest_mac_device_exception(self):
        with self.assertRaises(Exception) as context:
            macsec.get_lowest_mac_device()
        self.assertTrue(
            'device dictionary is mandatory argument' in str(context.exception))

    def test_get_lowest_mac_device(self):  
        dev = {}
        dev['r0'] = 'ge-0/0/6'
        device = Values()
        device.cli = MagicMock()
        resp = Values()
        resp.response = MagicMock()
        resp.response.return_value = """
        show interfaces ge-0/0/6
        Physical interface: ge-0/0/6, Enabled, Physical link is Up
        Interface index: 144, SNMP ifIndex: 515
        Link-level type: Ethernet, MTU: 1514, LAN-PHY mode, Link-mode: Half-duplex, Speed: 1000mbps, BPDU Error: None, Loop Detect PDU Error: None,
        Ethernet-Switching Error: None, Source filtering: Disabled
        Ethernet-Switching Error: None, MAC-REWRITE Error: None, Loopback: Disabled, Flow control: Disabled, Auto-negotiation: Enabled, Remote fault: Online
        Device flags   : Present Running
        Interface flags: SNMP-Traps Internal: 0x0
        Link flags     : None
        CoS queues     : 8 supported, 8 maximum usable queues
        Current address: 30:b6:4f:26:71:46, Hardware address: 30:b6:4f:26:71:46
        Last flapped   : 2017-07-31 12:24:50 PDT (00:39:20 ago)
        Input rate     : 0 bps (0 pps)
        Output rate    : 672 bps (0 pps)
        Active alarms  : None
        Active defects : None
        PCS statistics                      Seconds
          Bit errors                             0
          Errored blocks                         0
        Ethernet FEC statistics              Errors
          FEC Corrected Errors                    0
          FEC Uncorrected Errors                  0
          FEC Corrected Errors Rate               0
          FEC Uncorrected Errors Rate             0
        Interface transmit statistics: Disabled
        
        Logical interface ge-0/0/6.0 (Index 74) (SNMP ifIndex 527)
          Flags: Up SNMP-Traps 0x0 Encapsulation: Ethernet-Bridge
          Input packets : 346
          Output packets: 375
          Security: Zone: Null
          Protocol eth-switch, MTU: 1514
            Flags: Is-Primary 
                                   """
        device.cli.return_value = resp
        t.get_handle.return_value=device
        self.assertEqual(macsec.get_lowest_mac_device(device_dict=dev), 'r0')

    def test_get_lowest_mac_device_return_none(self):  
        r2 = {}
        self.assertEqual(macsec.get_lowest_mac_device(device_dict=r2), None)

    def test_pid_exception(self):   
        with self.assertRaises(Exception) as context:
            macsec.get_pid()
        self.assertTrue(
            'device dictionary is mandatory argument' in str(context.exception))

    def test_pid(self):  
        r2 = {}
        r2['dev1'] = 'dot1xd'
        device = Values()
        device.cli = MagicMock()
        resp = Values()
        resp.response = MagicMock()
        resp.response.return_value = '6080  ??  S      0:00.56 /usr/sbin/dot1xd -N'
        device.cli.return_value = resp
        t.get_handle.return_value=device
        self.assertEqual(macsec.get_pid(device_dict=r2), {'dev1': '6080'})

    def test_pid_return_none(self):  
        r2 = {}
        self.assertEqual(macsec.get_pid(device_dict=r2), None)

if __name__ == '__main__':

    unittest.main()
