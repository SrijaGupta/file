#! /usr/local/bin/python3

from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.utils.linux.linux_network_config import get_linux_int_mac 
from jnpr.toby.utils.linux.tcpreplay import tcpreplay_l2mode
from jnpr.toby.utils.linux.tcpreplay import tcpreplay_l3mode


class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()


#### UT for tcpreplay_l2mode starts here
    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l2mode_exception(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:37"
        try:
           tcpreplay_l2mode() 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "linux handle is the mandatory argument")

        try:
           tcpreplay_l2mode(device=self.mocked_obj) 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "pcap_file is a mandatory argument")

        try:
           tcpreplay_l2mode(device=self.mocked_obj, pcap_file="j", multiplier="2", pps="2")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")

        try:
           tcpreplay_l2mode(device=self.mocked_obj, pcap_file="j", pps="2", mbps="3")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")

        try:
           tcpreplay_l2mode(device=self.mocked_obj, pcap_file="j", mbps="2", topspeed="yes")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")

#        try:
#           tcpreplay_l2mode(device=self.mocked_obj, pcap_file="j", topspeed="yes")
#        except Exception as err:
#            self.assertEqual(
#                err.args[0],
#                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")


    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l2mode_execution_1(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:38"
        lst = [Response("abcd")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpreplay_l2mode(device=self.mocked_obj, pcap_file="j", multiplier="2"), "abcd")


    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l2mode_execution_2(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:39"
        lst = [Response("abc")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpreplay_l2mode(device=self.mocked_obj, pcap_file="j", pps="2"), "abc")


    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l2mode_execution_3(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:35"
        lst = [Response("ab")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpreplay_l2mode(device=self.mocked_obj, pcap_file="j", mbps="3"), "ab")

######## UT for tcpreplay_l2mode ends here


########## UT for tcpreplay_l3mode starts here.
    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l3mode_exception(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:34"
        try:
           tcpreplay_l3mode()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "linux handle is the mandatory argument")

        try:
           tcpreplay_l3mode(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "To replay pcap, pcap file name is mandatory")

        try:
           tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Mandatory arguments are client_ip, server_ip and split_ip")

        try:
           tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Mandatory arguments are device_ingress_mac and device_egress_mac")



        lst = [Response("a"), Response("b")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
           tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", multiplier="2", pps="3")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")

        lst = [Response("c"), Response("d")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
           tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", pps="3", mbps="4")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")


        lst = [Response("e"), Response("f")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
           tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", mbps="4", topspeed="yes")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")


        lst = [Response("g"), Response("h")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
           tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", topspeed="yes", pps="5")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Only one argument can be passed out of multiplier, pps, mbps and topspeed")



    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l3mode_execution_1(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:33"
        lst = [Response("abcd"), Response("m"), Response("n"), Response("o"), Response("p")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", portmap="8080:80", multiplier="2"), "o")



    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l3mode_execution_2(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:32"
        lst = [Response("abcd"), Response("m"), Response("n"), Response("o"), Response("p")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", pps="2", timer="nano"), "o")



    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l3mode_execution_3(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:31"
        lst = [Response("abcd"), Response("m"), Response("n"), Response("o"), Response("p")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="4.0.0.1", server_ip="5.0.0.1", split_ip="10.0.0.1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", mbps="3"), "o")



    @patch('jnpr.toby.utils.linux.tcpreplay.get_linux_int_mac')
    def test_tcpreplay_l3mode_execution_4(self, patched_get_linux_int_mac):
        patched_get_linux_int_mac.return_value = "00:50:56:A6:32:30"
        lst = [Response("abcd"), Response("m"), Response("n"), Response("o"), Response("p")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpreplay_l3mode(device=self.mocked_obj, pcap_file="test.pcap", client_ip="2004::1", server_ip="2005::1", split_ip="2010::1", device_ingress_mac="ge1", device_egress_mac="ge2", client_mac="abc", server_mac="def", topspeed="yes", ipproto="ipv6"), "o")

######## UT for tcpreplay_l3mode ends here.


if __name__ == '__main__':
    unittest.main()
