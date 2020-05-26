import unittest2 as unittest
import re
import logging
from lxml import etree
from lxml.builder import E
from jnpr.toby.hldcl.device_data import DeviceData
from jnpr.junos.device import Device as Pyez_Device
from jnpr.junos.rpcmeta import _RpcMetaExec
from jnpr.toby.exception.toby_exception import TobyException, TobyConnectFail

from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.host import Host
from nose.plugins.attrib import attr


@attr('unit')
class TestDeviceData(unittest.TestCase):


    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.device_data.Pyez_Device')
    @patch('jnpr.toby.hldcl.device_data.DeviceData.get_model',return_value='MX')
    @patch('logging.error')
    def test_device_data(self, patch1, patch2, pyez_patch):

        thandle = MagicMock(spec=DeviceData)
        thandle.handle = pyez_patch
        self.assertIsInstance(thandle,DeviceData)

        thandle = DeviceData(os='JUNOS',host='host',user='user1', password='password')
        self.assertIsInstance(thandle,DeviceData)

        ## Added code to test pyez_port argument
        thandle = DeviceData(os='JUNOS',host='host',user='user1', password='password', pyez_port=22)
        self.assertIsInstance(thandle,DeviceData)

        try:
            DeviceData(os='JUNOS')
        except Exception as err:
            self.assertEqual(err.args[0], "'host' is mandatory")

    @patch('jnpr.toby.hldcl.device_data.DeviceData.get_model',return_value='4567')
    @patch('logging.error')
    def test_device_data_2(self, patch1, patch2):

        try:
            thandle = DeviceData(os='JUNOS',host='host')
            self.assertIsInstance(thandle,DeviceData)

        except Exception as err:
                self.assertRaises(Exception, "Could not connect to device host")



    @patch('jnpr.toby.hldcl.device_data.DeviceData.get_model',return_value='MX')
    @patch('jnpr.toby.frameworkDefaults.credentials.JUNOS', {
    'USERNAME': None,
    'PASSWORD': None,
    'SU': 'root',
    'SUPASSWORD': 'Embe1mpls',})
    @patch('logging.error')
    def test_device_data__get_credentials(self, patch1, patch2):
        
        try:
            thandle = DeviceData(os='JUNOS',host='host')
            self.assertIsInstance(thandle,DeviceData)

        except Exception as err:
                self.assertRaises(Exception, "Could not connect to device host:Username/Password cannot be determined")


    @patch('jnpr.toby.hldcl.device_data.DeviceData.get_model',return_value='MX')
    @patch('logging.error')
    @patch('jnpr.toby.hldcl.device_data.Pyez_Device')
    def test_device_data__connect(self, patch1, patch2, patch3):

        #self.assertRaises(Exception, lambda: DeviceData(os='JUNOS',host='host', connect_mode='ftp'))
        try:
            DeviceData(os='JUNOS',host='host', connect_mode='ftp')
        except Exception as err:
                self.assertEqual(err.args[0], "Invalid connect mode(ftp) specified. Connect mode can be telnet/ssh/console/netconf")

        self.assertIsInstance( DeviceData(os='JUNOS',host='host', connect_mode='telnet'),DeviceData) 

    @patch('jnpr.toby.hldcl.device_data.DeviceData._get_host_ip',return_value='1.1.1.1')
    def test_device_data__get_juniper_node_facts(self, patch1):
        sobject = MagicMock(spec=DeviceData)
        sobject._get_juniper_details.return_value=[True, 're0', 'host_name0', 'model0', 'junos', 're1', 'host_name1', 'model1', 'junos']

        self.assertEqual(DeviceData._get_juniper_node_facts(sobject),'re1')

    @patch('jnpr.toby.hldcl.device_data.DeviceData._get_host_ip',return_value='1.1.1.1')
    def test_device_data__get__juniper_node_facts2(self, patch1):
        sobject = MagicMock(spec=DeviceData)
        sobject._get_juniper_details.return_value = [False, 're0', 'host_name0', 'model0', 'junos']

        self.assertEqual(type(DeviceData._get_juniper_node_facts(sobject)),dict)


    @patch('jnpr.toby.hldcl.device_data.DeviceData._get_host_ip',return_value='1.1.1.1')
    def test_device_data__get_juniper_node_facts(self, patch1):
        sobject = MagicMock(spec=DeviceData)
        sobject._get_juniper_details.return_value=[True, 're0', 'host_name0', 'model0', 'junos', 're1', 'host_name1', 'model1', 'junos']

        self.assertEqual(type(DeviceData._get_juniper_node_facts(sobject)),dict)


    @patch('jnpr.toby.hldcl.device_data.DeviceData._get_host_ip',return_value='1.1.1.1')
    def test_device_data__get_srx_facts(self, patch1):
        sobject = MagicMock(spec=DeviceData)
        sobject._get_srx_details.return_value=[True, 'node0', 'host_name0', 'model0', 'junos', 'node1', 'host_name1', 'model1', 'junos']
        # TBA does not create slave key then error
        #self.assertEqual(type(DeviceData._get_srx_facts(sobject)),dict)

    @patch('jnpr.toby.hldcl.device_data.DeviceData._get_host_ip_srx',return_value='1.1.1.1')
    def test_device_data__get_srx_facts2(self, patch1):

        sobject = MagicMock(spec=DeviceData)
        sobject._get_srx_details.return_value = [False, 'node0', 'host_name0', 'model0', 'junos']
        self.assertEqual(type(DeviceData._get_srx_facts(sobject)),dict)

        sobject._get_srx_details.return_value = [False, 'node1', 'host_name0', 'model0', 'junos']
        # TBA : does not create primary keys then error
        # need code change to cover 113/114, if not the code get in error later
        # self.assertEqual(type(DeviceData._get_srx_facts(sobject)),dict)

    def test_device_data__get_juniper_details(self ):

        dobject = MagicMock(spec=DeviceData)
        dobject.handle = MagicMock()
        xmldata = etree.XML(
               '<rpc><software-information><host-name>mayo</host-name>'
               '<product-model>mx5600</product-model>'
        	   '<product-name>mx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information></rpc>')
        dobject.handle.cli = MagicMock(return_value=xmldata)

        try:
            DeviceData._get_juniper_details(dobject)
        except Exception as err:
            self.assertEqual(err.args[0], "Could not retrieve details")    

        d2object = MagicMock(spec=DeviceData)
        d2object.handle = MagicMock()
        xmldata2 = etree.XML(
        	   '<multi-routing-engine-results><multi-routing-engine-item>'
               '<re-name>node0</re-name>'
               '<software-information><host-name>mayo</host-name>'
               '<product-model>mx5600</product-model>'
        	   '<product-name>mx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information></multi-routing-engine-item>'
               '<multi-routing-engine-item><re-name>node1</re-name>'
               '<software-information><host-name>mayo</host-name>'
               '<product-model>mx5600</product-model>'
        	   '<product-name>mx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information>'
               '</multi-routing-engine-item></multi-routing-engine-results>')
        d2object.handle.cli = MagicMock(return_value=xmldata2)
        self.assertEqual(type(DeviceData._get_juniper_details(d2object)),list)

        d3object = MagicMock(spec=DeviceData)
        d3object.handle = MagicMock()
        xmldata3 = etree.XML(
        	   '<multi-routing-engine-results><multi-routing-engine-item>'
               '<re-name>re0</re-name><software-information><host-name>mayo</host-name>'
               '<product-model>mx5600</product-model>'
        	   '<product-name>mx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information></multi-routing-engine-item>'
               '<multi-routing-engine-item>'
               '<software-information><host-name>mayo</host-name>'
               '<product-model>mx5600</product-model>'
        	   '<product-name>mx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information>'
               '</multi-routing-engine-item></multi-routing-engine-results>')
        d3object.handle.cli = MagicMock(return_value=xmldata3)
        self.assertEqual(type(DeviceData._get_juniper_details(d3object)),list)

        d4object = MagicMock(spec=DeviceData)
        d4object.handle = MagicMock()
        xmldata4 = etree.XML(
        	   '<multi-routing-engine-results><multi-routing-engine-item>'
               '<re-name>re0</re-name><software-information><host-name>mayo</host-name>'
               '<product-model>mx5600</product-model>'
        	   '<product-name>mx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information></multi-routing-engine-item>'
               '</multi-routing-engine-results>')
        d4object.handle.cli = MagicMock(return_value=xmldata4)

        # try:
        self.assertEqual(type(DeviceData._get_juniper_details(d4object)),list)   
             # except Exception as err:
        #     self.assertEqual(err.args[0], "Could not retrieve details")    

    @patch('jnpr.toby.hldcl.device_data.Pyez_Device')
    def test_devicedata__get_juniper_details(self, pyez_patch):
        dobject = MagicMock(spec=DeviceData)
        dobject.handle = pyez_patch
        obj = MagicMock()
        dobject.handle.cli.return_value = obj
        obj.findall.side_effect = Exception
        try:
            DeviceData._get_juniper_details(dobject)
        except Exception as err:
            self.assertEqual(err.args[0], "Could not connect to the other RE.")


    def test__get_srx_details(self):

        dobject = MagicMock(spec=DeviceData)
        dobject.handle = MagicMock()
        xmldata = etree.XML(
               '<software-information><host-name>mayo</host-name>'
               '<product-model>srx5600</product-model>'
        	   '<product-name>srx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information>')
        dobject.handle.cli = MagicMock(return_value=xmldata)
        self.assertEqual(type(DeviceData._get_srx_details(dobject)),list)


        d2object = MagicMock(spec=DeviceData)
        d2object.handle = MagicMock()
        xmldata2 = etree.XML(
        	   '<multi-routing-engine-results><multi-routing-engine-item>'
               '<re-name>re0</re-name>'
               '<software-information><host-name>mayo</host-name>'
               '<product-model>srx5600</product-model>'
        	   '<product-name>srx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information></multi-routing-engine-item>'
               '<multi-routing-engine-item><re-name>re11</re-name>'
               '<software-information><host-name>mayo</host-name>'
               '<product-model>srx5600</product-model>'
        	   '<product-name>srx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information>'
               '</multi-routing-engine-item></multi-routing-engine-results>')
        d2object.handle.cli = MagicMock(return_value=xmldata2)
        self.assertEqual(type(DeviceData._get_srx_details(d2object)),list)


        d3object = MagicMock(spec=DeviceData)
        d3object.handle = MagicMock()
        xmldata3 = etree.XML(
               '<software-information><host-name>mayo</host-name>'
        	   '<product-name>srx5600</product-name><jsr/>'
               '<package-information><name>junos</name>'
               '<comment>JUNOS Software Release [12.3X48-D43]</comment>'
               '</package-information></software-information>')
        d3object.handle.cli = MagicMock(return_value=xmldata3)
        try:
            DeviceData._get_srx_details(d3object)
        except Exception as err:
            self.assertEqual(err.args[0], "Could not retrieve details")

    def test_get_model(self):

        dobject = MagicMock(spec=DeviceData)
        dobject.handle = MagicMock()
        xmldata = etree.XML(
            '<software-information><host-name>mayo</host-name>'
            '<product-model>srx5600</product-model><product-name>srx5600</product-name>'
            '<jsr/><package-information><name>junos</name><comment>JUNOS Software Release [12.3X48-D43]</comment>'
            '</package-information></software-information>')

        dobject.handle.rpc.get_software_information = MagicMock(return_value=xmldata)

        self.assertEqual(type(DeviceData.get_model(dobject)),str)

        d2object = MagicMock(spec=DeviceData)
        d2object.handle = MagicMock()
        xmldata2 = etree.XML(
            '<software-information><host-name>mayo</host-name>'
            '<product-name>srx5600</product-name>'
            '<jsr/><package-information><name>junos</name><comment>JUNOS Software Release [12.3X48-D43]</comment>'
            '</package-information></software-information>')

        d2object.handle.rpc.get_software_information = MagicMock(return_value=xmldata2)

        try:
            DeviceData.get_model(d2object)
        except Exception as err:
            self.assertEqual(err.args[0], "Could not retrieve model")


        d3object = MagicMock(spec=DeviceData)
        d3object.handle = MagicMock()
        xmldata3 = etree.XML(
            '<multi-routing-engine-results><multi-routing-engine-item>'
            '<re-name>node0</re-name><software-information>'
            '<host-name>junkbert</host-name><product-model>srx5600</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item>'
            '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
            '<host-name>kingbert</host-name><product-model>srx5600</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata3)
        self.assertEqual(type(DeviceData.get_model(d3object)),str)

        xmldata4 = etree.XML(
            '<multi-routing-engine-results><multi-routing-engine-item>'
            '<re-name>node0</re-name><software-information>'
            '<host-name>junkbert</host-name><product-model>MX2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item>'
            '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
            '<host-name>kingbert</host-name><product-model>MX2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata4)
        self.assertEqual(type(DeviceData.get_model(d3object)),str)

        xmldata5 = etree.XML(
            '<multi-routing-engine-results><multi-routing-engine-item>'
            '<re-name>node0</re-name><software-information>'
            '<host-name>junkbert</host-name><product-model>VSRX2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item>'
            '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
            '<host-name>kingbert</host-name><product-model>VSRX2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata5)
        self.assertEqual(type(DeviceData.get_model(d3object)),str)

        xmldata6 = etree.XML(
            '<multi-routing-engine-results><multi-routing-engine-item>'
            '<re-name>node0</re-name><software-information>'
            '<host-name>junkbert</host-name><product-model>ex2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item>'
            '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
            '<host-name>kingbert</host-name><product-model>ex2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata6)
        self.assertEqual(type(DeviceData.get_model(d3object)),str)

        xmldata7 = etree.XML(
            '<multi-routing-engine-results><multi-routing-engine-item>'
            '<re-name>node0</re-name><software-information>'
            '<host-name>junkbert</host-name><product-model>qfx2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item>'
            '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
            '<host-name>kingbert</host-name><product-model>qfx2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata7)
        self.assertEqual(type(DeviceData.get_model(d3object)),str)

        xmldata8 = etree.XML(
            '<multi-routing-engine-results><multi-routing-engine-item>'
            '<re-name>node0</re-name><software-information>'
            '<host-name>junkbert</host-name><product-model>ocx2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item>'
            '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
            '<host-name>kingbert</host-name><product-model>ocx2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata8)
        self.assertEqual(type(DeviceData.get_model(d3object)),str)

        xmldata9 = etree.XML(
            '<multi-routing-engine-results><multi-routing-engine-item>'
            '<re-name>node0</re-name><software-information>'
            '<host-name>junkbert</host-name><product-model>nfx2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item>'
            '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
            '<host-name>kingbert</host-name><product-model>nfx2020</product-model>'
            '<product-name>srx5600</product-name><jsr/><package-information>'
            '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
            '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata9)
        self.assertEqual(type(DeviceData.get_model(d3object)),str)

        # TBA verify product model in the muti re case
        # xmldata10 = etree.XML(
        #     '<multi-routing-engine-results><multi-routing-engine-item>'
        #     '<re-name>node0</re-name><software-information>'
        #     '<host-name>junkbert</host-name>
        #     '<product-name>srx5600</product-name><jsr/><package-information>'
        #     '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
        #     '</package-information></software-information></multi-routing-engine-item>'
        #     '<multi-routing-engine-item><re-name>node1</re-name><software-information>'
        #     '<host-name>kingbert</host-name>'
        #     '<product-name>srx5600</product-name><jsr/><package-information>'
        #     '<name>junos</name><comment>JUNOS Software Release [12.3X48-D45]</comment>'
        #     '</package-information></software-information></multi-routing-engine-item></multi-routing-engine-results>')

        # d3object.handle.rpc.get_software_information = MagicMock(return_value=xmldata10)
        # self.assertEqual(type(DeviceData.get_model(d3object)),str)

    def test__other_re_slot_name(self):
        sobject = MagicMock(spec=DeviceData)
        sobject.reg = 're0'
        self.assertEqual(DeviceData._other_re_slot_name(sobject),'re1')
        
        sobject = MagicMock(spec=DeviceData)
        sobject.reg = 're1'
        self.assertEqual(DeviceData._other_re_slot_name(sobject),'re0')


    def test__other_node_name(self):
        sobject = MagicMock(spec=DeviceData)
        sobject.node_name = 'slave'
        self.assertEqual(DeviceData._other_node_name(sobject),'primary')
        
        sobject = MagicMock(spec=DeviceData)
        sobject.node_name = 'primary'
        self.assertEqual(DeviceData._other_node_name(sobject),'slave')


    def test__get_host_ip(self):

        dobject = MagicMock(spec=DeviceData)
        dobject.handle = MagicMock()
        xmldata = etree.XML(
        	'<configuration>'
            '<version>12.3X48-D45</version>'
            '<groups><name>re0</name><system><host-name>junkbert</host-name>'
            '</system><interfaces><interface><name>fxp0</name>'
            '<unit><name>0</name><family>'
            '<inet><address><name>10.204.134.91/18</name></address>'
            '</inet></family></unit></interface></interfaces></groups>'
            '<groups><name>re1</name><system><host-name>junkbert</host-name>'
            '</system><interfaces><interface><name>fxp0</name>'
            '<unit><name>0</name><family>'
            '<inet><address><name>10.204.134.92/18</name></address>'
            '</inet></family></unit></interface></interfaces></groups>'
            '</configuration>')
        dobject.handle.rpc.get_configuration = MagicMock(return_value=xmldata)

        self.assertEqual(type(DeviceData._get_host_ip(dobject, re_name='re0')),str)
        self.assertEqual(type(DeviceData._get_host_ip(dobject, re_name='re1')),str)

  
        d2object = MagicMock(spec=DeviceData)
        d2object.handle = MagicMock()
        xmldata2 = etree.XML(
        	'<configuration>'
            '<version>12.3X48-D45</version>'
            '<groups><name>member0</name><system><host-name>junkbert</host-name>'
            '</system><interfaces><interface><name>em0</name>'
            '<unit><name>0</name><family>'
            '<inet><address><name>10.204.134.91/18</name></address>'
            '</inet></family></unit></interface></interfaces></groups>'
            '</configuration>')
        d2object.handle.rpc.get_configuration = MagicMock(return_value=xmldata2)

        self.assertEqual(type(DeviceData._get_host_ip(d2object, re_name='re0')),str)


        d3object = MagicMock(spec=DeviceData)
        d3object.handle = MagicMock()
        xmldata3 = etree.XML(
        	'<configuration>'
            '<version>12.3X48-D45</version>'
            '<groups><name>member0</name><system><host-name>junkbert</host-name>'
            '</system><interfaces><interface><name>ge-0/0/0</name>'
            '<unit><name>0</name><family>'
            '<inet><address><name>10.204.134.91/18</name></address>'
            '</inet></family></unit></interface></interfaces></groups>'
            '</configuration>')
        d3object.handle.rpc.get_configuration = MagicMock(return_value=xmldata3)

        try:
            DeviceData._get_host_ip(d3object, re_name='re0')
        except Exception as err:
            self.assertEqual(err.args[0], "Could not determined other RE management IP")


    def test__get_host_ip_srx(self):

        d2object = MagicMock(spec=DeviceData)
        d2object.handle = MagicMock()
        xmldata2 = etree.XML(
        	'<configuration>'
            '<version>12.3X48-D45</version>'
            '<groups><name>node0</name><system><host-name>junkbert</host-name>'
            '</system><interfaces><interface><name>fxp0</name>'
            '<unit><name>0</name><family>'
            '<inet><address><name>10.204.134.91/18</name></address>'
            '</inet></family></unit></interface></interfaces></groups>'
            '</configuration>')
        d2object.handle.rpc.get_configuration = MagicMock(return_value=xmldata2)

        self.assertEqual(type(DeviceData._get_host_ip_srx(d2object, node='primary')),str)

        d3object = MagicMock(spec=DeviceData)
        d3object.handle = MagicMock()
        xmldata3 = etree.XML(
            '<configuration>'
            '<version>12.3X48-D45</version>'
            '<groups><name>node1</name><system><host-name>junkbert</host-name>'
            '</system><interfaces><interface><name>fxp0</name>'
            '<unit><name>0</name><family>'
            '<inet><address><name>10.204.134.91/18</name></address>'
            '</inet></family></unit></interface></interfaces></groups>'
            '</configuration>')
        d3object.handle.rpc.get_configuration = MagicMock(return_value=xmldata3)

        self.assertEqual(type(DeviceData._get_host_ip_srx(d3object, node='slave')),str)


        dobject = MagicMock(spec=DeviceData)
        dobject.handle = MagicMock()
        xmldata = etree.XML(
        	'<configuration>'
            '<version>12.3X48-D45</version>'
            '<groups><name>node0</name><system><host-name>junkbert</host-name>'
            '</system><interfaces><interface><name>em00</name>'
            '<unit><name>0</name><family>'
            '<inet><address><name>10.204.134.91/18</name></address>'
            '</inet></family></unit></interface></interfaces></groups>'
            '</configuration>')
        dobject.handle.rpc.get_configuration = MagicMock(return_value=xmldata)

        # TBA fix bug in line 317 first : existence of host_ip
        # try:
        # 	DeviceData._get_host_ip_srx(dobject, node='primary')
        # except Exception as err:
        #     self.assertEqual(err.args[0], "Could not determined management IP")



    @patch('jnpr.toby.hldcl.device_data.DeviceData._get_srx_facts', return_value=True)
    @patch('jnpr.toby.hldcl.device_data.DeviceData._get_juniper_node_facts', return_value=True)
    @patch('pprint.pprint')

    def test_system_facts(self, patch1, patch2,patch3):
        sobject = MagicMock(spec=DeviceData)
        sobject.series = 'SRX'

        self.assertEqual(str(type(DeviceData.system_facts(sobject))),"<class 'mock.mock.MagicMock'>")

        sobject = MagicMock(spec=DeviceData)
        sobject.series = 'MX'
        self.assertEqual(type(DeviceData.system_facts(sobject)),dict)

    def test_pyez_facts(self):
        sobject = MagicMock(spec=DeviceData)
        sobject.handle = MagicMock(spec=Pyez_Device)
        sobject.handle.facts =MagicMock(return_value=True)

        self.assertEqual(str(type(DeviceData.pyez_facts(sobject))),"<class 'mock.mock.MagicMock'>")

    def test_device_close(self):
        sobject = MagicMock(spec=DeviceData)
        sobject.handle = MagicMock(spec=Pyez_Device)

        self.assertEqual(DeviceData.close(sobject),True)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDeviceData)
    #unittest.TextTestRunner(verbosity=2).run(SUITE)  
    unittest.main()

