from mock import patch
import unittest2 as unittest
from mock import MagicMock
from jnpr.toby.utils.linux import tcpdump
from jnpr.toby.hldcl.unix.unix import UnixHost




# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()

    def test_check_pcap_exception(self):

        try:
            tcpdump.check_pcap(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory arguments: string and device have to be "
                                          "passed")

        lst = [Response(""), Response(""), Response(""), Response(""), Response("5"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512", delete_pcap="yes", sport=100, dport=80, src_v4="4.0.0.1", dst_v4="5.0.0.1", tcp_port=1234)
        except Exception as err:
            self.assertEqual(err.args[0], "'proto' is mandatory if 'tcp_port' is passed")




    def test_check_pcap_true(self):

        lst = [Response(""), Response(""), Response(""), Response(""), Response("5"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512",
                                            delete_pcap="yes", sport=100, dport=80, src_v4="4.0.0.1", dst_v4="5.0.0.1" ), True)

        lst = [Response(""), Response(""), Response(""), Response(""), Response("5"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512", tcp_port=123, proto="http",
                                            delete_pcap="yes", sport=100, dport=80, src_v4="4.0.0.1", dst_v4="5.0.0.1"),
                         True)


        lst = [Response(""), Response(""), Response(""), Response(""), Response("3"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512",
                                            delete_pcap="yes", sport=100, dport=80, src_v6="4::1", dst_v6="5::1", times=3), True)

        lst = [Response(""), Response(""), Response(""), Response("0"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512", sport=100,
                                            dport=80, src_v6="4::1", dst_v6="5::1", protocol="udp", pcap_name="/tmp/abc.pcap", state="absence"), True)


    def test_check_pcap_false(self):

        lst = [Response(""), Response(""), Response(""), Response(""), Response("0"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512", delete_pcap="yes",
                               sport=100, dport=80, src_v4="4.0.0.1", dst_v4="5.0.0.1")
        except Exception as err:
            self.assertEqual(err.args[0], "String is found 0 times in PCAP")

        #self.assertEqual(tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512",
        # delete_pcap="yes", sport=100, dport=80, src_v4="4.0.0.1", dst_v4="5.0.0.1"), False)

        lst = [Response(""), Response(""), Response(""), Response(""), Response("5"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        try:
            tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512", delete_pcap="yes",
                               sport=100, dport=80, src_v6="4::1", dst_v6="5::1", times=3)
        except Exception as err:
            self.assertEqual(err.args[0], "String is found 5 times in PCAP")

        #self.assertEqual(tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512",
        # delete_pcap="yes", sport=100, dport=80, src_v6="4::1", dst_v6="5::1", times=3), False)

        lst = [Response(""), Response(""), Response(""), Response("10"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        try:
            tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512", sport=100,
                               dport=80, src_v6="4::1", dst_v6="5::1", protocol="udp",
                               pcap_name="/tmp/abc.pcap", state="absence")
        except Exception as err:
            self.assertEqual(err.args[0], "String is found 10 times in PCAP")

        #self.assertEqual(tcpdump.check_pcap(device=self.mocked_obj, string="Frame 512", sport=100,
            # dport=80, src_v6="4::1", dst_v6="5::1", protocol="udp", pcap_name="/tmp/abc.pcap", state="absence"), False)


    def test_start_tcpdump_exception(self):
        try:
            tcpdump.start_tcpdump(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument-'interface' and 'device' has to be "
                                          "passed")

        lst = [Response("csh"), Response(""), Response(""), Response(""), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            tcpdump.start_tcpdump(device=self.mocked_obj, interface="eth1", ip_mode="ipv6",
                                  port=500,
                                  negate_port="yes")
        except Exception as err:
            self.assertEqual(err.args[0], "Tcpdump could not be started")


    def test_start_tcpdump(self):

        lst = [Response("ssh"), Response(""), Response("[1] 10230"), Response(" listening "), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(tcpdump.start_tcpdump(device=self.mocked_obj,interface="eth1",
                                               ip_mode="both", src="4.0.0.1", dst="5.0.0.1"), 10230)

        lst = [Response("csh"), Response(""), Response("[1] 10235"), Response(" listening "), Response("")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(tcpdump.start_tcpdump(device=self.mocked_obj, interface="eth1",
                                               ip_mode="ipv4", port=500), 10235)


    def test_stop_tcpdump(self):
        self.mocked_obj.shell = MagicMock()
        self.assertEqual(tcpdump.stop_tcpdump(device=self.mocked_obj, pid=123), None)
        self.assertEqual(tcpdump.stop_tcpdump(device=self.mocked_obj), None)


    def test_stop_tcpdump_exception(self):
        try:
            tcpdump.stop_tcpdump()
        except Exception as err:
            self.assertEqual(err.args[0], "device is a mandatory argument")


if __name__ == '__main__':
    unittest.main()