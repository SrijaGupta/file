import unittest as unittest
from mock import patch, MagicMock, Mock
from jnpr.toby.hldcl.juniper.junos import Juniper


class TestControllerChannels(unittest.TestCase):

    def test_add_channel(self):

        g = MagicMock()
        g._add_grpc_channel.return_value = "test_grpc"

        channel_type = "grpc"
        self.assertEqual(Juniper.add_channel(g,channel_type),"test_grpc")

        g = MagicMock()
        channel_type = "snmp"
        g._add_snmp_channel.return_value = True 
        self.assertEqual(Juniper.add_channel(g,channel_type),True)

        channel_type = "text"
        self.assertEqual(Juniper.add_channel(g,channel_type),True)

        channel_type = "future_protocol"
        self.assertEqual(Juniper.add_channel(g,channel_type),True)

    def test_add_grpc_channel(self):
        g1 = MagicMock()
        g1._grpc_init.return_value="my_channel"

        channel_attributes = {}
        channel_attributes['grpc_id'] = "my_channel"

        g1._grpc_connect_to_server.return_value = "123"

        self.assertEqual(Juniper._add_grpc_channel(g1,channel_attributes),"my_channel")

        g1._grpc_connect_to_server.return_value = None

        self.assertEqual(Juniper._add_grpc_channel(g1,channel_attributes),None) 

    @patch('jnpr.toby.hldcl.juniper.junos.Grpc')
    def test_grpc_init(self,grpc_patch):

        rhandle = MagicMock()
        rhandle.os = "JUNOS"
        
        channel_attributes = {}

        grpc_patch.return_value.get_grpc_id = MagicMock() 
        grpc_id = grpc_patch.return_value.get_grpc_id.return_value = "10"

        self.assertEqual(Juniper._grpc_init(rhandle,channel_attributes),grpc_id)

        channel_attributes['channel_id'] = "my_channel"
        channel_attributes['host'] = "1.1.1.1"

        self.assertEqual(Juniper._grpc_init(rhandle,channel_attributes),grpc_id)

    def test_grpc_connect_to_server(self):

        channel_attributes = {'grpc_id':"10"}

        grpc_id = "10"
        gObj = MagicMock()

        g = MagicMock()
        g.channels = {'grpc': {grpc_id: gObj}}

        gObj.open.return_value = True
        self.assertEqual(Juniper._grpc_connect_to_server(g,channel_attributes),True) 

        gObj.open.return_value = False 
        self.assertEqual(Juniper._grpc_connect_to_server(g,channel_attributes),False)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestControllerChannels)
    unittest.TextTestRunner(verbosity=2).run(suite)

