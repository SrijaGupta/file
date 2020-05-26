#!/usr/local/bin/python3

import sys
import mock
from mock import patch
from mock import Mock
from mock import MagicMock
import unittest
import unittest2 as unittest
from optparse import Values

import builtins
builtins.t = MagicMock()

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'

from jnpr.toby.trafficgen.warp17.Warp17api import Warp17api

class Shellmock2(object):
    @staticmethod
    def recv(self, *args, **kwargs):
        return b'> FreeBSD $'
    def send(self, *args, **kwargs):
        pass



class TestWarp17(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()
        self.warp = Warp17api(MagicMock(sideeffect={}))
        self.wobject = MagicMock(spec=Warp17api)
   
    def test_instanstiate_warp17_class(self):
        self.assertEqual(isinstance(Warp17api(server_name=Mock()), Warp17api), True)
   
    def test_warp17_init_missing_arg(self):
        with self.assertRaises(Exception) as context:
            Warp17api(server_name=None)
        self.assertTrue(
            'Missing server_name parameter' in str(context.exception))

    @patch('jnpr.toby.trafficgen.warp17.Warp17api.re')
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_connect(self,unix_patch,re_patch):
        self.wobject.server_name="dummy"
        self.wobject.virtual_machine = '0'
        self.wobject.setup_dpdk_flag = True
        self.wobject.ctrl_cores = 2
        self.wobject.data_cores = 14
        self.wobject.mem_in_mb = 124928
        self.wobject.ucb_pool_sz = 1
        self.wobject.lcores = None
        self.wobject.calc_cpu_cores.return_value={"num_of_cpus": "32", "Arch": "x86_64", "l1d_cache": "32K", "byte_order": "Little Endian", "stepping": "2", "virtual": "VT-x", "thread_per_core": "2", "core_per_sock": "8", "vendor": "GenuineIntel", "cpu_op_mode": "32-bit, 64-bit", "cpu_family": "6", "numa_node": {"0": {"cpu_core": ["0", 1, 2, 3, 4, 5, 6, 7, "16", 17, 18, 19, 20, 21, 22, 23]}, "1": {"cpu_core": ["8", 9, 10, 11, 12, 13, 14, 15, "24", 25, 26, 27, 28, 29, 30, 31]}, "total_numa_node": "2"}, "online_cpus": "0", "bogomips": "5201.21", "sock_total": "2", "cpu_mhz": "1198.640", "model": "63"}
        self.wobject.get_numa_node.return_value =1

        self.assertEqual(Warp17api.connect(self.wobject,'p1p1',tcb_pool_sz = 'max'),True)
        self.assertEqual(self.wobject.warp17_defaults_vm.assert_not_called(),None)      
        self.assertEqual(self.wobject.warp17_defaults.assert_called_once(), None)
        self.assertEqual(self.wobject.tcb_pool_sz,99942) 
        self.assertEqual(self.wobject.lcores,"0@8,1@8,2@9,3@10,4@11,5@12,6@13,7@14,8@15,9@24,10@25,11@26,12@27,13@28,14@29,15@30,16@31")       


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.re')
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_l2_intf_missing_arguements(self,unix_patch,re_patch):
        with self.assertRaises(Exception) as context:
            Warp17api.l2_intf(self.wobject,port='p1p2')
        self.assertTrue("Missing mandatory argument,  mtu" in str(context.exception)) 
        with self.assertRaises(Exception) as context:
            Warp17api.l2_intf(self.wobject,mtu='1500')
        self.assertTrue("Missing mandatory argument, port" in str(context.exception))
        self.wobject.client_handle=MagicMock()
        self.wobject.rpc_client_path="/root/WARP17/warp17-dev-common/examples/python/RPC_CLIENT.py"
        self.assertEqual(Warp17api.l2_intf(self.wobject,mtu='1500',port='p1p1'),True)
       
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_calc_cpu_cores(self,unix_patch):
        self.wobject.log=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value = "CPU op-mode(s):        32-bit, 64-bit\n\
Byte Order:            Little Endian\n\
CPU(s):                32\n\
On-line CPU(s) list:   0-31\n\
Thread(s) per core:    2\n\
Core(s) per socket:    8\n\
Socket(s):             2\n\
NUMA node(s):          2\n\
Vendor ID:             GenuineIntel\n\
CPU family:            6\n\
Model:                 63\n\
Stepping:              2\n\
CPU MHz:               1197.015\n\
BogoMIPS:              5201.21\n\
Virtualization:        VT-x\n\
L1d cache:             32K\n\
L1i cache:             32K\n\
L2 cache:              256K\n\
L3 cache:              20480K\n\
NUMA node0 CPU(s):     0-7,16-23\n\
NUMA node1 CPU(s):     8-15,24-31"
        lscpu=Warp17api.calc_cpu_cores(self.wobject)
        self.assertEqual(lscpu,{"vendor": "GenuineIntel", "byte_order": "Little Endian", "l1d_cache": "32K", "cpu_mhz": "1197.015", "bogomips": "5201.21", "online_cpus": "0", "stepping": "2", "model": "63", "cpu_op_mode": "32-bit, 64-bit", "sock_total": "2", "core_per_sock": "8", "num_of_cpus": "32", "cpu_family": "6", "numa_node": {"total_numa_node": "2", "1": {"cpu_core": ["8", 9, 10, 11, 12, 13, 14, 15, "24", 25, 26, 27, 28, 29, 30, 31]}, "0": {"cpu_core": ["0", 1, 2, 3, 4, 5, 6, 7, "16", 17, 18, 19, 20, 21, 22, 23]}}, "thread_per_core": "2", "virtual": "VT-x"})
 
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.re')
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_l3_intf_missing_arguemnts(self,unix_patch,re_patch):
        self.wobject.client_handle=MagicMock()
        self.wobject.rpc_client_path="/root/WARP17/warp17-dev-common/examples/python/RPC_CLIENT.py"
        with self.assertRaises(Exception) as context:
            Warp17api.l3_intf(self.wobject,port='p1p2',ip_end='10.10.10.2',mask='255.255.255.255',gateway='1.1.1.1')
        self.assertTrue("Missing mandatory argument, ip_start" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Warp17api.l3_intf(self.wobject,port='p1p2',ip_start='10.10.10.1',mask='255.255.255.255',gateway='1.1.1.1')
        self.assertTrue("Missing mandatory argument, ip_end" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Warp17api.l3_intf(self.wobject,ip_end='10.10.10.10',ip_start='10.10.10.1',mask='255.255.255.255',gateway='1.1.1.1')
        self.assertTrue("Missing mandatory argument, port" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Warp17api.l3_intf(self.wobject,ip_end='10.10.10.10',ip_start='10.10.10.1',port='p2p2',gateway='1.1.1.1')
        self.assertTrue("Missing mandatory argument, mask" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Warp17api.l3_intf(self.wobject,ip_end='10.10.10.10',ip_start='10.10.10.1',port='p2p2',mask='255.255.255.255')
        self.assertTrue("Missing mandatory argument, gateway" in str(context.exception))
        self.assertEqual(Warp17api.l3_intf(self.wobject,port='p1p1',ip_end='10.10.10.2',mask='255.255.255.255',ip_start='10.10.10.1',gateway='1.1.1.1'),True)
        self.assertEqual(Warp17api.l3_intf(self.wobject,port='p1p1',ip_end='10.10.10.2',mask='255.255.255.255',ip_start='10.10.10.1',gateway='1.1.1.1',vlan_id=20),True) 
        
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.re')
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_ipv4_options_missing_arguemnts(self,unix_patch,re_patch):
        self.wobject.client_handle=MagicMock()
        self.wobject.rpc_client_path="/root/WARP17/warp17-dev-common/examples/python/RPC_CLIENT.py"
        with self.assertRaises(Exception) as context:
            Warp17api.ipv4_options(self.wobject,port='p1p2')             
        self.assertTrue("Mandatory argument tc_id is missing" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Warp17api.ipv4_options(self.wobject,tc_id='2')
        self.assertTrue("Mandatory argument port is missing" in str(context.exception))
        self.assertEqual(Warp17api.ipv4_options(self.wobject,port='p1p1',tc_id='2',tos='96'),True)
        self.assertEqual(Warp17api.ipv4_options(self.wobject,port='p1p1',tc_id='2',ecn='ce2',dscp='12'),True)
        self.assertEqual(Warp17api.ipv4_options(self.wobject,port='p1p1',tc_id='2',ecn='ce2',tos='96',dscp='12'),True)


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.re')
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_vlan_options_missing_arguemnts(self,unix_patch,re_patch):
        self.wobject.client_handle=MagicMock()
        self.wobject.rpc_client_path="/root/WARP17/warp17-dev-common/examples/python/RPC_CLIENT.py"
        with self.assertRaises(Exception) as context:
            Warp17api.vlan_options(self.wobject,port='p1p2')
        self.assertTrue("Mandatory argument tc_id is missing" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Warp17api.vlan_options(self.wobject,tc_id='2')
        self.assertTrue("Mandatory argument port is missing" in str(context.exception))
        self.assertEqual(Warp17api.vlan_options(self.wobject,port='p1p1',tc_id='2',vlan_id='23',vlan_pri='7'),True)

    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Warp17api')
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.re')
    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_verify_warp17_stats_missing_arguemnts(self,unix_patch,re_patch,warp_patch):
        self.wobject.log=MagicMock()
        self.wobject.warp17_obj=MagicMock()
        self.wobject.eth_port = dict()
        self.wobject.eth_port['p1p2']='1'
        warp_patch.get_port_config.return_value={"0":{"resv_bit_set": "0","ip_hdr_too_small": "0","invl_chk_sum": "0","rcvd_icmp": "0","small_mbuf_frag": "0","rcvd_tcp": "0","invl_version": "0","rcvd_pkts": "0","total_len_invl": "0","rcvd_bytes": "0","rcvd_frags": "0","rcvd_other": "0","rcvd_udp": "0"},"1": {"resv_bit_set": "0","ip_hdr_too_small": "0","invl_chk_sum": "0","rcvd_icmp": "0","small_mbuf_frag": "0","rcvd_tcp": "0","invl_version": "0","rcvd_pkts": "0","total_len_invl": "0","rcvd_bytes": "0","rcvd_frags": "0","rcvd_other": "0","rcvd_udp": "0"}}
        with self.assertRaises(Exception) as context:
            Warp17api.verify_warp17_stats(self.wobject,warp17_stat='get_port_config',tol_val=10,tol_perc=10,rcvd_tcp=550,rcvd_pkts=600,rcvd_bytes=23000)
        self.assertTrue("Mandatory argument port is missing" in str(context.exception))
        Warp17api.verify_warp17_stats(self.wobject,warp17_stat='get_port_config',port='p1p2',tol_val=10,tol_perc=10,rcvd_tcp=550,rcvd_pkts=600,rcvd_bytes=23000)


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_get_arp_stats(self,unix_patch):
        self.wobject.log=MagicMock()
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="Port 0 ARP statistics:\n\
  Received Requests   :                    0\n\
  Received Replies    :                    0\n\
  Received \"other\"    :                    0\n\
  Sent Requests       :                    0\n\
  Sent Requests Failed:                    0\n\
  Sent Replies        :                    0\n\
  Sent Replies Failed :                    0\n\
\n\
  Request not mine    :                    0\n\
\n\
  Small mbuf fragment :                    0\n\
  Invalid hw space    :                    0\n\
  Invalid hw length   :                    0\n\
  Invalid proto space :                    0\n\
  Invalid proto length:                    0\n\
\n\
Port 1 ARP statistics:\n\
  Received Requests   :                    0\n\
  Received Replies    :                    1\n\
  Received \"other\"    :                    0\n\
  Sent Requests       :                    2\n\
  Sent Requests Failed:                    0\n\
  Sent Replies        :                    2\n\
  Sent Replies Failed :                    0\n\
\n\
  Request not mine    :                    0\n\
\n\
  Small mbuf fragment :                    0\n\
  Invalid hw space    :                    0\n\
  Invalid hw length   :                    0\n\
  Invalid proto space :                    0\n\
  Invalid proto length:                    0"

        arp_stats=Warp17api.get_arp_stats(self.wobject)
        self.assertEqual(arp_stats['1']['resp_sent'],'2')
 

    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_show_tcp_stats(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="Port 0 TCP statistics:\n\
  Received Packets    :              2505234\n\
  Received Bytes      :            279194415\n\
  Sent Ctrl Packets   :              1374121\n\
  Sent Ctrl Bytes     :             51724760\n\
  Sent Data Packets   :              1212117\n\
  Sent Data Bytes     :            155150976\n\
\n\
  Malloced TCBs       :                    0\n\
  Freed TCBs          :                    0\n\
  Not found TCBs      :                    0\n\
  TCB alloc errors    :                    0\n\
\n\
  Invalid checksum    :                    0\n\
  Small mbuf fragment :                    0\n\
  TCP hdr to small    :                    0\n\
  Ctrl Failed Packets :                    0\n\
  DATA Failed Packets :                    0\n\
  DATA Clone Failed   :                    0\n\
  Reserved bit set    :                    0\n\
\n\
Port 1 TCP statistics:\n\
  Received Packets    :              2586245\n\
  Received Bytes      :            206876260\n\
  Sent Ctrl Packets   :              1293123\n\
  Sent Ctrl Bytes     :             50104860\n\
  Sent Data Packets   :              1212120\n\
  Sent Data Bytes     :            229090680\n\
\n\
  Malloced TCBs       :                81048\n\
  Freed TCBs          :                    0\n\
  Not found TCBs      :                    0\n\
  TCB alloc errors    :                    0\n\
\n\
  Invalid checksum    :                    0\n\
  Small mbuf fragment :                    0\n\
  TCP hdr to small    :                    0\n\
  Ctrl Failed Packets :                    0\n\
  DATA Failed Packets :                    0\n\
  DATA Clone Failed   :                    0\n\
  Reserved bit set    :                    0"

        tcp_stats=Warp17api.get_tcp_stats(self.wobject)
        self.assertEqual(tcp_stats['1']['sent_ctrl_pkts'],'1293123')



    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_get_port_link(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="Port 0 linkstate UP, speed 10Gbps, duplex full(auto)\n\
Port 1 linkstate UP, speed 10Gbps, duplex full(auto)"
        port_link=Warp17api.get_port_link(self.wobject)
        self.assertEqual(port_link['1']['duplex'],'full')


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_get_msg_stats(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="MSG statistics:\n\
  Messages rcvd       :             37893811\n\
  Messages sent       :             37893749\n\
  Messages polled     :          69833221487\n\
\n\
  Messages errors     :                    0\n\
  Messages proc err   :                    0\n\
\n\
  Messages allocated  :                   30\n\
  Messages alloc err  :                    0\n\
  Messages freed      :                   30"

        msg_stats=Warp17api.get_msg_stats(self.wobject)
        self.assertEqual(msg_stats['freed'],'30')
        self.assertEqual(msg_stats['rcvd'],'37893811')        




    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_setup_dpdk(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.bind='igb_uio'
        dpdk_status=Warp17api.setup_dpdk(self.wobject)

    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_port_config(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="L3 Interface   : 30.3.3.2/255.255.255.0, VLAN-ID:    0, GW: 0.0.0.0\n\
GW             : 30.3.3.1\n\
\n\
Test Case Id   : 0\n\
Test type      : TCP CL (Async)\n\
Local IP:Port  : [30.3.3.2 -&gt; 30.3.3.2]:[3000 -&gt; 30000]\n\
Remote IP:Port : [40.4.4.2 -&gt; 40.4.4.2]:[1500 -&gt; 1502]\n\
\n\
Rate Open      : 10000s/s\n\
Rate Close     : INFINITE\n\
Rate Send      : 10000s/s\n\
Delay Init     : INFINITE\n\
Delay Uptime   : INFINITE\n\
Delay Downtime : INFINITE\n\
\n\
HTTP CLIENT:\n\
Request Method      : GET\n\
Request Object      : /index.com\n\
Request Host        : google.com\n\
\n\
Request Size        : 10\n\
Request HTTP Fields :\n\
ContentType: plain/text"
        port_config=Warp17api.get_port_config(self.wobject,port='p1p1')

    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_route_stats(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="Port 0 Route statistics:\n\
  Intf Add            :                    1\n\
  Intf Del            :                    0\n\
  Gw Add              :                    1\n\
  Gw Del              :                    0\n\
\n\
  Route Tbl Full      :                    0\n\
  Intf No Mem         :                    0\n\
  Intf Not Found      :                    0\n\
  Gw Intf Not Found   :                    0\n\
  NH not found        :                    0\n\
  Route not found     :                    0\n\
\n\
Port 1 Route statistics:\n\
  Intf Add            :                    1\n\
  Intf Del            :                    0\n\
  Gw Add              :                    1\n\
  Gw Del              :                    0\n\
\n\
  Route Tbl Full      :                    0\n\
  Intf No Mem         :                    0\n\
  Intf Not Found      :                    0\n\
  Gw Intf Not Found   :                    0\n\
  NH not found        :                    0\n\
  Route not found     :                    0"
        route_stats=Warp17api.get_route_stats(self.wobject,port='p1p1')
        self.assertEqual(route_stats['1']['gw_add'],'1')


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_tsm_stats(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="Port 0 TSM statistics:\n\
  INIT                :                    0\n\
  LISTEN              :                    0\n\
  SYN_SENT            :                    0\n\
  SYN_RECV            :                    0\n\
  ESTAB               :                81003\n\
  FIN_WAIT_1          :                    0\n\
  FIN_WAIT_2          :                    0\n\
  LAST_ACK            :                    0\n\
  CLOSING             :                    0\n\
  TIME_WAIT           :                    0\n\
  CLOSE_WAIT          :                    0\n\
  CLOSED              :                    0\n\
\n\
  SYN retrans TO      :                    0\n\
  SYN/ACK retrans TO  :                    0\n\
  Retrans TO          :                    0\n\
  Retrans bytes       :                    0\n\
  Missing seq         :                    0\n\
  SND win full        :                    0\n\
\n\
Port 1 TSM statistics:\n\
  INIT                :                    0\n\
  LISTEN              :                   45\n\
  SYN_SENT            :                    0\n\
  SYN_RECV            :                    0\n\
  ESTAB               :                81003\n\
  FIN_WAIT_1          :                    0\n\
  FIN_WAIT_2          :                    0\n\
  LAST_ACK            :                    0\n\
  CLOSING             :                    0\n\
  TIME_WAIT           :                    0\n\
  CLOSE_WAIT          :                    0\n\
  CLOSED              :                    0\n\
\n\
  SYN retrans TO      :                    0\n\
  SYN/ACK retrans TO  :                    0\n\
  Retrans TO          :                    0\n\
  Retrans bytes       :                    0\n\
  Missing seq         :                    0\n\
  SND win full        :                    0"
        tsm_stats=Warp17api.get_tsm_stats(self.wobject)
        self.assertEqual(tsm_stats['1']['estab'],'81003')


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_get_dpdk_status(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.dpdk_dev_bind_path="path"
        self.wobject.warp17_obj.shell.return_value.response.return_value="Network devices using DPDK-compatible driver\n\
============================================\n\
<none>\n\
\n\
Network devices using kernel driver\n\
===================================\n\
0000:01:00.0 'I350 Gigabit Network Connection' if=eth0 drv=igb unused=igb_uio *Active*\n\
0000:01:00.1 'I350 Gigabit Network Connection' if=eth1 drv=igb unused=igb_uio\n\
0000:01:00.2 'I350 Gigabit Network Connection' if=eth3 drv=igb unused=igb_uio\n\
0000:01:00.3 'I350 Gigabit Network Connection' if=eth4 drv=igb unused=igb_uio\n\
0000:81:00.0 'Ethernet Controller X710 for 10GbE SFP+' if=p1p1 drv=i40e unused=igb_uio\n\
0000:81:00.1 'Ethernet Controller X710 for 10GbE SFP+' if=p1p2 drv=i40e unused=igb_uio\n\
0000:81:00.2 'Ethernet Controller X710 for 10GbE SFP+' if=p1p3 drv=i40e unused=igb_uio\n\
0000:81:00.3 'Ethernet Controller X710 for 10GbE SFP+' if=p1p4 drv=i40e unused=igb_uio\n\
0000:82:00.0 'Ethernet Controller X710 for 10GbE SFP+' if=p2p1 drv=i40e unused=igb_uio\n\
0000:82:00.1 'Ethernet Controller X710 for 10GbE SFP+' if=p2p2 drv=i40e unused=igb_uio\n\
0000:82:00.2 'Ethernet Controller X710 for 10GbE SFP+' if=p2p3 drv=i40e unused=igb_uio\n\
0000:82:00.3 'Ethernet Controller X710 for 10GbE SFP+' if=p2p4 drv=i40e unused=igb_uio\n\
\n\
Other network devices\n\
=====================\n\
<none>\n\
\n\
Crypto devices using DPDK-compatible driver\n\
===========================================\n\
<none>\n\
\n\
Crypto devices using kernel driver\n\
==================================\n\
<none>\n\
\n\
Other crypto devices\n\
====================\n\
<none>"
        dpdk_status=Warp17api.get_dpdk_status(self.wobject)

        self.wobject.warp17_obj.shell.return_value.response.return_value="Network devices using DPDK-compatible driver\n\
============================================\n\
0000:81:00.1 'Ethernet Controller X710 for 10GbE SFP+' drv=igb_uio unused=\n\
\n\
Network devices using kernel driver\n\
===================================\n\
0000:01:00.0 'I350 Gigabit Network Connection' if=eth0 drv=igb unused=igb_uio *Active*\n\
0000:01:00.1 'I350 Gigabit Network Connection' if=eth1 drv=igb unused=igb_uio\n\
0000:01:00.2 'I350 Gigabit Network Connection' if=eth3 drv=igb unused=igb_uio\n\
0000:01:00.3 'I350 Gigabit Network Connection' if=eth4 drv=igb unused=igb_uio\n\
0000:81:00.0 'Ethernet Controller X710 for 10GbE SFP+' if=p1p1 drv=i40e unused=igb_uio\n\
0000:81:00.2 'Ethernet Controller X710 for 10GbE SFP+' if=p1p3 drv=i40e unused=igb_uio\n\
0000:81:00.3 'Ethernet Controller X710 for 10GbE SFP+' if=p1p4 drv=i40e unused=igb_uio\n\
0000:82:00.0 'Ethernet Controller X710 for 10GbE SFP+' if=p2p1 drv=i40e unused=igb_uio\n\
0000:82:00.1 'Ethernet Controller X710 for 10GbE SFP+' if=p2p2 drv=i40e unused=igb_uio\n\
0000:82:00.2 'Ethernet Controller X710 for 10GbE SFP+' if=p2p3 drv=i40e unused=igb_uio\n\
0000:82:00.3 'Ethernet Controller X710 for 10GbE SFP+' if=p2p4 drv=i40e unused=igb_uio\n\
\n\
Other network devices\n\
=====================\n\
<none>\n\
\n\
Crypto devices using DPDK-compatible driver\n\
===========================================\n\
<none>\n\
\n\
Crypto devices using kernel driver\n\
==================================\n\
<none>\n\
\n\
Other crypto devices\n\
====================\n\
<none>"
        dpdk_status=Warp17api.get_dpdk_status(self.wobject)
        self.wobject.warp17_obj.shell.return_value.response.return_value="Network devices using DPDK-compatible driver\n\
============================================\n\
0000:81:00.0 'Ethernet Controller X710 for 10GbE SFP+' drv=igb_uio unused=\n\
\n\
Network devices using kernel driver\n\
===================================\n\
0000:01:00.0 'I350 Gigabit Network Connection' if=eth0 drv=igb unused=igb_uio *Active*\n\
0000:01:00.1 'I350 Gigabit Network Connection' if=eth1 drv=igb unused=igb_uio\n\
0000:01:00.2 'I350 Gigabit Network Connection' if=eth3 drv=igb unused=igb_uio\n\
0000:01:00.3 'I350 Gigabit Network Connection' if=eth4 drv=igb unused=igb_uio\n\
0000:81:00.2 'Ethernet Controller X710 for 10GbE SFP+' if=p1p3 drv=i40e unused=igb_uio\n\
0000:81:00.3 'Ethernet Controller X710 for 10GbE SFP+' if=p1p4 drv=i40e unused=igb_uio\n\
0000:82:00.0 'Ethernet Controller X710 for 10GbE SFP+' if=p2p1 drv=i40e unused=igb_uio\n\
0000:82:00.1 'Ethernet Controller X710 for 10GbE SFP+' if=p2p2 drv=i40e unused=igb_uio\n\
0000:82:00.2 'Ethernet Controller X710 for 10GbE SFP+' if=p2p3 drv=i40e unused=igb_uio\n\
0000:82:00.3 'Ethernet Controller X710 for 10GbE SFP+' if=p2p4 drv=i40e unused=igb_uio\n\
\n\
Other network devices\n\
=====================\n\
0000:81:00.1 'Ethernet Controller X710 for 10GbE SFP+' unused=igb_uio\n\
\n\
Crypto devices using DPDK-compatible driver\n\
===========================================\n\
<none>\n\
\n\
Crypto devices using kernel driver\n\
==================================\n\
<none>\n\
\n\
Other crypto devices\n\
====================\n\
<none>"
        dpdk_status=Warp17api.get_dpdk_status(self.wobject)
        self.assertEqual(dpdk_status['dpdk_pci_inuse'][0],'0000:81:00.0')
        self.assertEqual(dpdk_status['dpdk_driver_others'][0],'0000:81:00.1')

    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_get_arp_entries(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="ARP table for port 0:\n\
\n\
IPv4             MAC address        Age         Flags\n\
---------------  -----------------  ----------  -----\n\
       30.3.3.2  3C:FD:FE:9E:FF:D0          -1  ul\n\
       30.3.3.1  88:E0:F3:BA:BD:28          -1  u-\n\
\n\
ARP table for port 1:\n\
\n\
IPv4             MAC address        Age         Flags\n\
---------------  -----------------  ----------  -----\n\
       40.4.4.2  3C:FD:FE:9E:FF:D1          -1  ul\n\
       40.4.4.1  88:E0:F3:BA:BD:7A          -1  u-"
        arp_entries=Warp17api.get_arp_entry(self.wobject)


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_eth_stats(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="Port 0 ethernet statistics:\n\
  etype ARP  (0x0806) :                    1\n\
  etype IPv4 (0x0800) :               726577\n\
  etype IPv6 (0x86DD) :                    0\n\
  etype VLAN (0x8100) :                    0\n\
\n\
  small mbuf fragment :                    0\n\
  no tx mbuf          :                    0\n\
\n\
Port 1 ethernet statistics:\n\
  etype ARP  (0x0806) :                    1\n\
  etype IPv4 (0x0800) :               807585\n\
  etype IPv6 (0x86DD) :                    0\n\
  etype VLAN (0x8100) :                    0\n\
\n\
  small mbuf fragment :                    0\n\
  no tx mbuf          :                    0"
        eth_stats=Warp17api.get_eth_stats(self.wobject)
        self.assertEqual(eth_stats['0']['ipv4'],'726577')


    @patch('jnpr.toby.trafficgen.warp17.Warp17api.Unix')
    def test_testcase_stats(self,unix_patch):
        self.wobject.warp17_obj=MagicMock()
        self.wobject.warp17_obj.shell.return_value.response.return_value="Port 0, Test Case 0 Statistics:\n\
      Estab/s      Closed/s   Data Send/s\n\
            0             0          9993\n\
     Requests     Responses   Invalid Msg        No Len     Trans-Enc\n\
       309768        309767             0             0             0\n\
        Closed (No Request)        Closed (No Response)\n\
                          0                           0"
        tc_stats=Warp17api.get_test_stats(self.wobject,port="p1p1",tc_id='0')
        self.assertEqual(tc_stats['p1p1']['0']['resp'],'309767')


if __name__ == '__main__':
    unittest.main()


