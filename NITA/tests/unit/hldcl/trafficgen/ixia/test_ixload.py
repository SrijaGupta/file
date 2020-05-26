import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
import unittest.mock as umock
import os
import sys
from jnpr.toby.hldcl.trafficgen.ixia.ixload import IxLoad
#from jnpr.toby.trafficgen.ixia.ixload.IxLoadHL import IxLoadHL
from jnpr.toby.hldcl.trafficgen.ixia import IxRestApi as IxRestUtils
class test_IxLoad(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixload.os')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixload.yaml')
    @patch('builtins.super')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixload.IxLoad._get_version')
    @patch('jnpr.toby.hldcl.trafficgen.ixia.ixload.IxLoad.cleanup')
    def test_init(self,os_patch,yml_patch, super_patch, get_version_mock, cleanup_mock):
        ixia_mock = MagicMock(spec=IxLoad)
        self.assertRaises(Exception, IxLoad.__init__, ixia_mock)
        #os_patch.path.dirname.return_value = "jnpr/toby/something"
        with patch('jnpr.toby.hldcl.trafficgen.ixia.ixload.re.sub') as re_patch:
            re_patch.return_value = "jnpr/toby/something"
            IxLoad.__init__(ixia_mock, system_data=create_system_data())

    def test_create_session(self):
        rt_handle = MagicMock(spec=IxLoad)
        with patch('jnpr.toby.hldcl.trafficgen.ixia.IxRestApi.Connection.http_post') as http_post:
            with patch('jnpr.toby.hldcl.trafficgen.ixia.IxRestApi.Connection.http_get') as http_get:
                post_mock = MagicMock()
                post_mock.ok = True
                post_mock.headers = {'location':'/dummy'}
                #post_mock.reconnect = None
                http_post.return_value = post_mock
                get_mock = MagicMock()
                get_mock.state = 'finished'
                get_mock.status = 'Successful'
                get_mock.isActive = True
                http_get.return_value = get_mock
                a = {"status": 1, "session" : "dummy"}
                #mobj = MagicMock(spec=IxLoad)
                rt_handle.reconnect = "dummy"
                rt_handle.reconnect_session = MagicMock(return_value=a)
                #result = IxLoad.reconnect_session(rt_handle,"")
                #self.assertEqual(result['status'], 0)
                #self.assertIsInstance(result, type(post_mock))
                result = IxLoad.create_session(rt_handle,"","","")
                #self.assertIsInstance(result, type(MagicMock()))
                self.assertEqual(result['status'], 1)
                
                rt_handle.reconnect = None
                get_mock = MagicMock()
                get_mock.state = 'finished'
                get_mock.status = 'Successful'
                # get_mock.status = 'Error'
                # get_mock.error = 'some error'
                http_get.return_value = get_mock
                result = IxLoad.create_session(rt_handle,"","","")
                self.assertEqual(result['status'], 1)
               
                get_mock.status = 'something else'
                result = IxLoad.create_session(rt_handle,"","","")
                self.assertEqual(result['status'], 0)
                
                

                post_mock.headers = None
                result = IxLoad.create_session(rt_handle,"","","")
                self.assertEqual(result['status'], 0)

                post_mock.ok = False
                result = IxLoad.create_session(rt_handle,"","","")
                self.assertEqual(result['status'], 0)
                
                post_mock = MagicMock()
                post_mock.headers = {'location':'/dummy'}
                post_mock.ok.side_effect = [True, False]
                result = IxLoad.create_session(rt_handle,"","","")
                self.assertEqual(result['status'], 0)       
         
    def test_add_interfaces(self):
        ixia_mock = MagicMock(spec=IxLoad)
        self.assertRaises(Exception, IxLoad.add_interfaces, ixia_mock)
    def test_add_intf_to_port_map(self):
        ixia_mock = MagicMock(spec=IxLoad)
        intf_to_port_map={'dummy':"dummy"}
        self.assertRaises(Exception, IxLoad.add_intf_to_port_map, ixia_mock)
        IxLoad.add_intf_to_port_map(ixia_mock, intf_to_port_map=intf_to_port_map)
    def test_get_port_handle(self):
        ixia_mock = MagicMock(spec=IxLoad)
        intf="a"
        ixia_mock.port_to_handle_map = {'a' : 'dummy'}
        ixia_mock.intf_to_port_map = {'a' : 'dummy'}
        self.assertRaises(Exception, IxLoad.get_port_handle, ixia_mock)
        IxLoad.get_port_handle(ixia_mock, intf=intf)

    def test_set_envs(self):
        ixia_mock = MagicMock(spec=IxLoad)
        intf="a"
        ixia_mock.lib_path = "/foo/"
        self.assertIsNone(IxLoad._set_envs(ixia_mock), ixia_mock)
        IxLoad._set_envs(ixia_mock)

    def test_reconnect_session(self):
        rt_handle = MagicMock(spec=IxLoad)
        with patch('jnpr.toby.hldcl.trafficgen.ixia.IxRestApi.Connection.http_get') as http_get:
            get_mock = MagicMock()
            get_mock.reply = MagicMock(return_value={"isActive":True})
            http_get.return_value = get_mock
            rt_handle.session_url = "dummy"
            result = IxLoad.reconnect_session(rt_handle,"dummy2")
            self.assertEqual(result['status'], 0)

def create_system_data():
    """
    Function to create system_data
    :return:
        Returns system_data
    """
    system_data = dict()
    system_data['system'] = dict()
    system_data['system']['primary'] = dict()
    system_data['system']['primary']['controllers'] = dict()
    system_data['system']['primary']['controllers']['re0'] = dict()
    system_data['system']['primary']['controllers']['re0']['hostname'] = 'abc'
    system_data['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    system_data['system']['primary']['controllers']['re0']['osname'] = 'IXIA'
    system_data['system']['primary']['name'] = 'abc'
    system_data['system']['primary']['model'] = 'IXIA'
    system_data['system']['primary']['make'] = 'IXIA'
    system_data['system']['primary']['osname'] = 'IXIA'
    system_data['system']['primary']['appserver'] = '2.2.2.2'
    return system_data
    
if __name__ == '__main__':
    unittest.main()
