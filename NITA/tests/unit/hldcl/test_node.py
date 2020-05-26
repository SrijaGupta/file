"""UT for the module jnpr.toby.hldcl.node"""

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr

from collections import defaultdict
from jnpr.toby.hldcl.node import Node


@attr('unit')
class TestNode(unittest.TestCase):
    """UT for SrxNode"""
    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    @patch('sys.stdout')
    def test_node_init(self, stdout_patch):
        """Test '__init__' method of class Node"""

        # Exception
        self.assertRaises(Exception, Node)

        node_data = defaultdict(lambda: defaultdict(dict))
        node_data['connect'] = None
        nobject = Node(node_data)
        self.assertEqual(nobject.controllers, {})
        self.assertEqual(nobject.current_controller, None)
        self.assertEqual(nobject.current_controller_str, None)

        # Exception
        node_data['connect'] = "test"
        #self.assertRaises(Exception, Node, node_data)

        # Exception
        node_data['controllers']['node0']['osname'] = "test"
        node_data['controllers']['node0']['connect'] = "test"
        self.assertRaises(Exception, Node, node_data)

        node_data['controllers']['node0']['osname'] = "junos"
        #self.assertIsInstance(Node(node_data), Node)
        #self.assertRaises(Exception, Node, node_data)
        #stdout_patch.write.assert_any_call("Skipping the connection for 'node0'")
        mocked_controller_object = MagicMock()
        mocked_controller_object.dual_controller = None
        node_data['controllers']['node0']['connect'] = True
        with patch('jnpr.toby.hldcl.juniper.junos.Junos', return_value=mocked_controller_object):
            nobject = Node(node_data)
            self.assertEqual(nobject.controllers['node0'], mocked_controller_object)
            self.assertEqual(nobject.current_controller, mocked_controller_object)
            self.assertEqual(nobject.current_controller_str, "node0")

        node_data['controllers']['node0']['osname'] = "unix"
        with patch('jnpr.toby.hldcl.unix.unix.Unix', return_value=mocked_controller_object):
            nobject = Node(node_data)
            self.assertEqual(nobject.controllers['node0'], mocked_controller_object)
            self.assertEqual(nobject.current_controller, mocked_controller_object)
            self.assertEqual(nobject.current_controller_str, "node0")
        ''' 
        node_data['controllers']['node0']['osname'] = "IOS"
        with patch('jnpr.toby.hldcl.cisco.cisco.Cisco', return_value="test"):
            nobject = Node(node_data)
            self.assertEqual(nobject.controllers['node0'], "test")
            self.assertEqual(nobject.current_controller, "test")
            self.assertEqual(nobject.current_controller_str, "node0")
        '''
        node_data['controllers']['node0']['osname'] = "windows"
        with patch('jnpr.toby.hldcl.windows.windows.Windows', return_value=mocked_controller_object):
            nobject = Node(node_data)
            self.assertEqual(nobject.controllers['node0'], mocked_controller_object)
            self.assertEqual(nobject.current_controller, mocked_controller_object)
            self.assertEqual(nobject.current_controller_str, "node0")

    def test_node__set_current_controller(self):
        """Test '_set_current_controller' method of class Node"""
        nobject = MagicMock(spec=Node)
        nobject.controllers = {}

        # Exception
        self.assertRaises(Exception, Node._set_current_controller, nobject)
        mocked_controller_object = MagicMock()
        mocked_controller_object.dual_controller = None
        nobject.controllers['node0'] = mocked_controller_object
        Node._set_current_controller(nobject)
        self.assertEqual(nobject.current_controller_str, "node0")
        self.assertEqual(nobject.current_controller,  mocked_controller_object)

        nobj = MagicMock()
        nobject.current_controller_str = None
        nobject.current_controller = None
        nobject.controllers['node1'] = nobj
        nobject.controllers['node0'] = MagicMock()
        nobject.controllers['node0'].is_master.return_value = False
        # Exception
        nobject.controllers['node1'].is_master.return_value = False
        self.assertRaises(Exception, Node._set_current_controller, nobject)

        nobject.controllers['node1'].is_master.return_value = True
        Node._set_current_controller(nobject)
        self.assertEqual(nobject.current_controller_str, "node1")
        self.assertEqual(nobject.current_controller, nobj)

    def test_node_switch_controller(self):
        """Test 'switch_controller' method of class Node"""
        nobject = MagicMock(spec=Node)

        # Exception
        self.assertRaises(Exception, Node.switch_controller, nobject)

        nobject.controllers = {}
        controller = "node0"
        self.assertIsNone(Node.switch_controller(nobject, controller))
        
        nobj = MagicMock()
        nobject.controllers[nobj] = "test1"
        nobject.controllers['node1'] = "test2"
        nobject.current_controller_str = nobj
        print ("........",nobject.controllers)
        self.assertIsNone(Node.switch_controller(nobject, "test"))
        nobject.current_controller_str = "node1"
        self.assertIsNone(Node.switch_controller(nobject, "node1"))

        
           
    def test_add_channel(self):
        from jnpr.toby.hldcl.node import Node
        node_obj = MagicMock(spec=Node)
        controller = 'current'
        node_obj.current_controller_str = 're0'
        node_obj.current_controller = MagicMock()
        node_obj.current_controller.add_channel = MagicMock(return_value={'111':'snmp handle 1111 to Router'})
        channel_dict = Node.add_channel(node_obj, 'snmp')
        self.assertEqual(channel_dict['re0'], {'111':'snmp handle 1111 to Router'})
        self.assertEqual(channel_dict['current_controller'], {'111': 'snmp handle 1111 to Router'})

        node_obj.controllers = dict()
        node_obj.controllers['re0'] = MagicMock()
        node_obj.controllers['re0'].add_channel = MagicMock(return_value={'111':'snmp handle 1111 to Router'})
        channel_dict = Node.add_channel(node_obj, 'snmp', controller='all')
        self.assertEqual(channel_dict, {'re0': {'111': 'snmp handle 1111 to Router'}})
        channel_dict = Node.add_channel(node_obj, 'snmp', controller='re0')
        self.assertEqual(channel_dict, {'re0': {'111': 'snmp handle 1111 to Router'}})

        snmp_exception = ''
        try:
            Node.add_channel(node_obj, 'snmp', controller='re1')
        except Exception as ex:
            snmp_exception = str(ex)

        self.assertEqual(snmp_exception, 'Controller re1 does not exist for the device')

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestNode)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
