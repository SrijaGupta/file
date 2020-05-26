"""
Unit test cases for jvision.py
author: akanadam
"""
import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from jnpr.toby.system.jvision import jvision
#from jvision import jvision
#from influxReader import InfluxDB
#from jnpr.toby.hldcl.juniper.junos import Juniper
#from jnpr.toby.hldcl.system  import *

#if sys.version < '3':
#    builtin_string = '__builtin__'
#else:
#    builtin_string = 'builtins'

import builtins
builtins.t=MagicMock()

@attr('unit')
class TestSystem(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()
        builtins.tv=MagicMock()
        self.sensor_data={'/network-instances/network-instance/mpls':{'freq':10000,'gnmi_submode':2}}
        self.gnmi_data={'mode':0,'encoding':2}

    def test_jvision_init_device_excptn(self):
        jv=jvision.jvision()
        with self.assertRaises(Exception) as context:
            jv.jvision_init()
        self.assertTrue('server & dut information are mandatory arguments' in str(context.exception))

    def test_jvision_init_server_excptn(self):
        jv=jvision.jvision()
        device=MagicMock()
        with self.assertRaises(Exception) as context:
            jv.jvision_init(device=device,interface='eth1',server_ip_address='1.1.1.1/24',dut_ip_address='2.2.2.2/24')
        self.assertTrue('cannot configure IP address and route on server' in str(context.exception))

    def test_start_jvision_decoder(self):
        jv=jvision.jvision()
        jv.json_file='xyz'
        server=MagicMock()
        #self.assertTrue(jv.start_jvision_decoder(server_handle=server,type='python',decoder_type='grpc',decoder_command='./grpc'),True)
        jv.start_jvision_decoder(server_handle=server,type='python',decoder_type='grpc',decoder_command='./grpc')

    def test_stop_jvision_decoder(self):
        jv=jvision.jvision()
        server=MagicMock()
        jv.decoder_status={'grpc':False,'gnmi':True}
        jv.decoder_pid={'grpc':1234,'gnmi':6789}
        with self.assertRaises(Exception) as context:
            jv.stop_jvision_decoder(server_handle=server,decoder_type='grpc')
        #self.assertTrue('Decoder cannot be stopped if its not running' in str(context.exception))
        #jv.stop_jvision_decoder(server_handle=server,decoder_type='gnmi')

    def test_kill_jvision_decoder(self):
        jv=jvision.jvision()
        server=MagicMock()
        jv.decoder_status={'grpc':False,'gnmi':True}
        jv.decoder_pid={'grpc':1234,'gnmi':6789}
        with self.assertRaises(Exception) as context:
            jv.kill_jvision_decoder(server_handle=server,decoder_type='grpc')
        #self.assertTrue('Decoder cannot be killed if its not running' in str(context.exception))
        #jv.kill_jvision_decoder(server_handle=server,decoder_type='gnmi')


    def test_jvision_init_mgmt_ip(self):
        jv=jvision.jvision()
        device=MagicMock()
        with self.assertRaises(Exception) as context:
            jv.jvision_init(device=device,interface='eth1',server_ip_address='10.48.40.226/24',dut_ip_address='10.48.40.85/24',mgmt_ip="True")
        self.assertTrue('expected string or bytes-like object' in str(context.exception))

    def test_grpc_init(self):
        jv=jvision.jvision()
        device=MagicMock()
        server=MagicMock()
        with self.assertRaises(Exception) as context:
            jv.grpc_init(server_handle=server,dut_handle=device)
        self.assertTrue('cannot generate pem file on server' in str(context.exception))

    def test_gen_and_upload_json_gnmi(self):
        jv=jvision.jvision()
        jv.jv_db_server="abc"
        jv.decoder_port={'gnmi':1234}
        with self.assertRaises(Exception) as context:
            jv.gen_and_upload_json(sensor_params=self.sensor_data,gnmi_params=self.gnmi_data,eos=1,decoder_type='gnmi')
        #self.assertTrue('getaddrinfo() argument 1 must be string or None' in str(context.exception))


if __name__ == '__main__' :
    unittest.main()
