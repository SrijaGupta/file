import sys

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hldcl.system  import *

if sys.version < '3':
    builtin_string = '__builtin__'
else:
    builtin_string = 'builtins'


@attr('unit')
class TestSystem(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch("jnpr.toby.hldcl.system.Node", return_value = ['re0', 're1'])
    @patch("jnpr.toby.hldcl.system.JuniperNode", return_value = ['re0', 're1'])
    @patch("jnpr.toby.hldcl.system.SrxNode", return_value ="test")
    def test_System_init(self, patch_node, patch_juniper, patch_srx):
        self.assertIsInstance(
            System( system_data={'system':{ 'primary': {'controllers': {'r0':{'model':'MX2020','osname':'JUNOS'}}, 'osname': 'JUNOS'}}}), System)
        self.assertIsInstance(
            System( system_data={'system':{ 'primary': {'controllers': {'r0':{'model':'SRX3000','osname':'JUNOS'}}, 'osname': 'JUNOS'}}}), System)
        self.assertIsInstance(
            System( system_data={'system':{ 'primary': {'controllers': {'r0':{'model':'ha_cluster','osname':'JUNOS'}}, 'osname': 'JUNOS'}}}), System)
        self.assertIsInstance(
            System( system_data={'system':{ 'primary': {'controllers': {'r0':{'model':'MX2020','osname':'UBUNTU'}}, 'osname': 'UBUNTU'}}}), System)
        self.assertIsInstance(
        System( system_data={'system':{ 'primary': {'controllers': {'r0':{'model':' S360','osname':''}}, 'osname': ''}}}), System)
        self.assertIsInstance(
        System( system_data={'system':{ 'primary': {'controllers': {'r0':{'model':' S360','osname':''}}, 'osname': ''}}}),System)
        try:
            System( system_data=None)
        except Exception as err:
            self.assertEqual(err.args[0], 'System data not passed to init.')
    
        with patch("jnpr.toby.hldcl.system.System.findkeys") as findkeys_patch:
            findkeys_patch.return_value = '1'
            try:
                System( system_data={'system':{}})
            except Exception as err:
                self.assertEqual(err.args[0], "Unable to create any nodes (ex: Connection to 'primary')")
            #self.assertIsInstance(
        #System( system_data={'system':{ 'primary': {'model':'SRX1','osname':''}}, 'osname': ''}),System)
        with patch('jnpr.toby.hldcl.system.System.is_controller_connect_set') as connect_set_patch:
            connect_set_patch.return_value = True
            self.assertIsInstance(
                System( system_data={'system':{ 'primary': {'model':'SRX1','connect':False,'osname':''}}, 'osname': ''}),System)
            connect_set_patch.return_value = False
            self.assertIsInstance(
                System( system_data={'system':{ 'primary': {'model':'SRX1','connect':False,'osname':''}}, 'osname': ''}),System) 

    
    def test_reboot(self):

        j2object = MagicMock(spec=Juniper)
        j2object.os = 'JUNOS'
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        obj1 = MagicMock()
        obj2 = MagicMock()
        sobject.nodes={'node0':obj1}
        sobject.controllers={'re0':obj2}
        self.assertEqual(str(type(System.reboot(sobject))),"<class 'mock.mock.MagicMock'>")

        j2object = MagicMock(spec=Juniper)
        j2object.os = 'TOTO'
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        try:
            System.reboot(sobject, mode='CLI')
        except Exception as err:
            self.assertEqual(err.args[0], "Argument 'mode' can be set to CLI only if device is running Junos")

        try:
            System.reboot(sobject, all=True)
        except Exception as err:
            self.assertEqual(err.args[0], "Argument 'all' can only be used to reboot Junos devices")

        j2object.os = 'TOTO'
        self.assertEqual(str(type(System.reboot(sobject,mode='shell'))),"<class 'mock.mock.MagicMock'>")


    #@patch('jnpr.toby.hldcl.system.run_multiple')
    @patch('jnpr.toby.utils.utils.run_multiple')
    def test_reboot2(self,run_mock):

        jobject = MagicMock(spec=Juniper)
        j2object = MagicMock(spec=Juniper)
        j2object.os = 'JUNOS'
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        nobject.controllers = {'re0': jobject}
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        obj1 = MagicMock()
        obj2 = MagicMock()
        sobject.nodes={'node0':obj1}
        sobject.controllers={'re0':obj2}

        run_mock.return_value =[True, False]

        try:
            System.reboot(sobject, all=True)
        except Exception as err:
            self.assertEqual(err.args[0], "Unable to reboot all REs of device.")

        run_mock.return_value =[True, True]
        self.assertTrue(System.reboot(sobject,all=True))


    def test_reconnect(self):
        
        jobject = MagicMock()
        obj1 = MagicMock()
        obj2 = MagicMock()
        jobject.nodes={'node0':obj1}
        obj1.controllers={'re0':obj2}
        obj2.reconnect.return_value = True
        self.assertEqual(System.reconnect(jobject,all=True),True)
        
        #Exception
        obj2.reconnect.return_value = False
        self.assertRaises(Exception, System.reconnect, jobject,all=True)

        #Else
        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.reconnect(sobject))),"<class 'mock.mock.MagicMock'>")


    def test__set_current_node(self):
  
        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject
        sobject.nodes = {'r0':nobject}
        self.assertEqual(System._set_current_node(sobject, set_node=None), None)
        self.assertEqual(System._set_current_node(sobject, set_node='r0'), None)
        sobject.nodes = {'r0':nobject,'r1':nobject} 
        self.assertEqual(System._set_current_node(sobject, set_node=None), None)
        nobject.is_node_master = MagicMock(return_value=Exception('err'))
        sobject.nodes = {'r0':nobject,'r1':nobject}
        
        self.assertEqual(System._set_current_node(sobject, set_node=None), None)
        nobject.is_node_master.side_effect = [Exception('err'),Exception('err'),Exception('err'),False]
        sobject.current_node = None
        
        self.assertEqual(System._set_current_node(sobject, set_node=None), None)
        nobject.is_node_master.side_effect = [Exception('err'),Exception('err'),True,True]
        sobject.current_node = None
        try:
            System._set_current_node(sobject, set_node=None)
        except:
            pass

    def test_shell(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.shell(sobject))),"<class 'mock.mock.MagicMock'>")

    def test_su(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.su(sobject))),"<class 'mock.mock.MagicMock'>")

    def test_disconnect(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.disconnect(sobject))),"<class 'mock.mock.MagicMock'>")

    def test_close(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.close(sobject))),"<class 'mock.mock.MagicMock'>")

    def test_upload(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.upload(sobject))),"<class 'mock.mock.MagicMock'>")

    def test_download(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.download(sobject))),"<class 'mock.mock.MagicMock'>")

    def test_log(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.log(sobject,message='message'))),"<class 'mock.mock.MagicMock'>")

    def test_vty(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.vty(sobject, command="", destination=""))),"<class 'mock.mock.MagicMock'>")

    def test_cty(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        self.assertEqual(str(type(System.cty(sobject, command="", destination=""))),"<class 'mock.mock.MagicMock'>")


    def test_set_current_system_node(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True

        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject
        sobject.nodes = {'re0':nobject}

        try:
            System.set_current_system_node(sobject,system_node='current')
        except Exception as err:
            self.assertEqual(err.args[0], 'Parameter values passed are invalid. system_node :"current" is not a part of device object')
        
        self.assertEqual(System.set_current_system_node(sobject,system_node='re0'),True)


    def test_set_current_controller(self):

        jobject = MagicMock(spec=Juniper)
        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller= j2object
        nobject.controllers = {'re0': jobject}
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject
        sobject.nodes = {'r0':nobject,'r1':nobject} 

        self.assertEqual(System.set_current_controller(sobject,controller='re0', system_node='current'),True)

        try:
            System.set_current_controller(sobject,controller='re1', system_node='current')
        except Exception as err:
            self.assertEqual(err.args[0], 'Parameter values passed are invalid. controller :"re1" is not a part of device object')
        
        try:
           System.set_current_controller(sobject,controller='re0', system_node='primary')
        except Exception as err:
            self.assertEqual(err.args[0], 'Parameter values passed are invalid. system_node :"primary" is not a part of device object')

        try:
           System.set_current_controller(sobject,controller='re3', system_node='r0')
        except Exception as err:
            self.assertEqual(err.args[0], 'Parameter values passed are invalid. controller :"re3" is not a part of device object')

        self.assertTrue(System.set_current_controller(sobject,controller='re0', system_node='r0'))


    def test_get_current_controller_name(self):

        j2object = MagicMock(spec=Juniper)
        cobject = MagicMock(spec=Node)
        cobject.current_controller= j2object
        nobject = MagicMock(spec=JuniperNode)
        nobject.is_node_master = True
        nobject.current_controller_str = 'str'
        nobject.current_controller= j2object
        sobject = MagicMock(spec=System)
        sobject.current_node = nobject

        System.get_current_controller_name(sobject)
        self.assertEqual(type(System.get_current_controller_name(sobject)), str)

    def test_add_channel(self):
        from jnpr.toby.hldcl.system import System
        system_obj = MagicMock(spec=System)
        controller = 'current'
        system_obj.nodes = dict()
        system_obj.nodes['primary'] = system_obj.current_node = MagicMock()
        system_obj.current_node.add_channel = MagicMock(return_value={'111': 'snmp handle 1111 to Router'})
        channel_dict = System.add_channel(system_obj, 'snmp')
        self.assertEqual(channel_dict['primary'], {'111': 'snmp handle 1111 to Router'})
        self.assertEqual(channel_dict['current_node'], {'111': 'snmp handle 1111 to Router'})

        system_obj.nodes['primary'].add_channel = MagicMock(return_value={'111': 'snmp handle 1111 to Router'})
        channel_dict = System.add_channel(system_obj, 'snmp', system_node='all')
        self.assertEqual(channel_dict, {'primary': {'111': 'snmp handle 1111 to Router'}})
        channel_dict = System.add_channel(system_obj, 'snmp', system_node='primary')
        self.assertEqual(channel_dict, {'primary': {'111': 'snmp handle 1111 to Router'}})

        snmp_exception = ''
        try:
            System.add_channel(system_obj, 'snmp', system_node='member1')
        except Exception as ex:
            snmp_exception = str(ex)

        self.assertEqual(snmp_exception, 'System Node member1 does not exist for the device')

    def test_findkeys(self):
        from jnpr.toby.hldcl.system import System
        node = ['node1','node2']
        kv = {'node1':'value1','node2':'value2'}
        system_obj = MagicMock(spec=System)
        System.findkeys(system_obj,node,kv)

if __name__ == '__main__' :
    unittest.main()
