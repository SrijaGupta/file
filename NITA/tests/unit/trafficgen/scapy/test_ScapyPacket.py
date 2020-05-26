"""
All unit test cases for ScapyPacket.py
__author__ = ['Mohan kumar']
__contact__ = 'mvmohan@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2018'

"""

#from unittest import TestCase
#import unittest
from jnpr.toby.utils.message import message
from jnpr.toby.trafficgen.scapy.ScapyPacket import ScapyPacket

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr


class TestScapyPacket(unittest.TestCase):
    """
    class for uni test class for ScapyPacket
    """
    def setUp(self):
        """setup before all case"""
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        builtins.tv=MagicMock() 
        self.log = message(name="ScapyPacketGenerator", level="INFO", show_color=False)
        self.ins = ScapyPacket()
        self.ins.log = t.log
        self.test_create_packet_yaml = "tests/unit/trafficgen/scapy/packet_new.yaml"
        self.test_verify_packet_yaml = "tests/unit/trafficgen/scapy/packet_verify.yaml"
        self.test_packet1 = "packet1"
        self.test_packet2 = "packet2"
        self.test_packet3 = "packet3"
        self.test_packet4 = "packet4"
        self.test_packet5 = "packet5"
        self.test_packet1_hex = "009944445588001122445566810000640800450000\
28000100004006faabac101402ac10140103e700500000000000000000500220000b880000"
        self.ins.raw_send_packet = {'packet2': "Ether(src='00:11:22:44:55:66',\
                dst='00:99:44:44:55:88')\
                /Dot1Q(vlan=875)/IP(src='182.16.145.9',dst='172.16.20.1')",\
                'packet3': "Ether(src='00:11:22:44:55:66',dst='00:99:44:44:55:88')/\
                IP(src='172.16.99.2',dst='172.16.99.1')\
                /TCP(sport=999,dport=80)", 'packet1': "Ether(src='00:11:22:44:55:66',\
                dst='00:99:44:44:55:88')/\
                Dot1Q(vlan=100)\
                /IP(src='172.16.20.2',dst='172.16.20.1')/TCP(sport=999,dport=80)", 'packet4': \
                "Ether(src='00:11:22:44:55:66',\
                dst='00:99:44:44:55:88')/Dot1Q(vlan=4000)/IP(src='192.16.10.2',dst='192.16.20.1')"}

        self.ins.raw_verify_packet = {'packet2': "Ether(src='00:11:22:44:55:66',\
                dst='00:99:44:44:55:88')\
                /Dot1Q(vlan=875)/IP(src='182.16.145.9',dst='172.16.20.1')", 'packet1': \
                "Ether(src='00:11:22:44:55:66',dst='00:99:44:44:55:88')/Dot1Q(vlan=100)\
                /IP(src='172.16.20.2',dst='172.16.20.1')/TCP(sport=999,dport=80)", \
                'packet4': "Ether(src='00:11:22:44:55:66',dst='00:99:44:44:55:88')\
                /Dot1Q(vlan=4000)/IP(src='192.16.10.2',dst='192.16.20.1')", \
                'packet3': "Ether(src='00:11:22:44:55:66',dst='00:99:44:44:55:88')/\
                IP(src='172.16.99.2',dst='172.16.99.1')/TCP(sport=999,dport=80)"}
    def test_packet_init(self):
        """
        Test the packet init function
        """
        self.assertEqual(self.ins.packet_init(self.test_create_packet_yaml), True)
    def test_verify_packet_init(self):
        """
        Test the packet verify function
        """
        self.assertEqual(self.ins.verify_packet_init(self.test_verify_packet_yaml), True)
    def test_create_and_get_send(self):
        """
        Test the create and get hex dump packet for send function
        """
        self.assertEqual(self.ins.create_and_get_hex_dump_packet_for_send(packet='packet1'),\
                self.test_packet1_hex)
    def test_create_and_get_verify(self):
        """
        Test the function for verify
        """
        self.assertEqual(self.ins.create_and_get_hex_dump_packet_for_verify\
                (packet=self.test_packet1), \
                self.test_packet1_hex)
    def test_packet_show_command_send(self):
        """
        Test the function for packet show for send
        """
        self.assertEqual(self.ins.packet_show_command(packet=self.test_packet1, \
                packet_mode='Send'), True)
    def test_packet_show_command_verify(self):
        """
        Test the function for packet show for verify
        """
        self.assertEqual(self.ins.packet_show_command(packet=self.test_packet1, \
                packet_mode='Verify'), True)


if __name__ == '__main__' :
        unittest.main() 

