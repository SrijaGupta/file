"""
rtdhcpserver.py unit test
"""

import unittest
from mock import patch, MagicMock
from jnpr.toby.init.init import init
from jnpr.toby.bbe.bbevar.bbevars import BBEVars
from jnpr.toby.bbe.bbevar.rtdhcpserver import RTDHCPv4Server, RTDHCPv6Server, RTDHCPServer
import builtins

builtins.t = MagicMock(spec=init)

class TestRtDhcpServer(unittest.TestCase):
    """
    test rtdhcpserver.py
    """
    @patch('jnpr.toby.bbe.bbevar.rtdhcpserver.RTDHCPServer')
    def test_class_rtdhcpv4server(self, patch_dhcpserver):
        patch_dhcpserver.return_value = None
        builtins.bbe = MagicMock(spec=BBEVars)
        builtins.bbe.bbevar = MagicMock()
        server = RTDHCPv4Server()
        self.assertIsInstance(server, RTDHCPv4Server)
        self.assertIsInstance(server.family, object)
        self.assertIsInstance(server.lease_time, object)
        self.assertIsInstance(server.pool_size, object)
        self.assertIsInstance(server.pool_gateway, object)
        self.assertIsInstance(server.pool_start_address, object)
        self.assertIsInstance(server.pool_mask_length, object)
        server._multi_servers = MagicMock()
        self.assertIsInstance(server.multi_servers_config, object)
        server.created = True
        self.assertEqual(server.created, True)
        server.server_interface = 'test'
        self.assertEqual(server.server_interface, 'test')
        server.server_handle = 'server'
        self.assertEqual(server.server_handle, 'server')

        server = RTDHCPv6Server()
        self.assertIsInstance(server, RTDHCPv6Server)
        self.assertIsInstance(server.family, object)
        self.assertIsInstance(server.lease_time, object)
        self.assertIsInstance(server.pool_size, object)
        self.assertIsInstance(server.pool_start_address, object)
        self.assertIsInstance(server.pool_mask_length, object)
        self.assertIsInstance(server.pool_ia_type, object)
        self.assertIsInstance(server.pool_prefix_length, object)
        self.assertIsInstance(server.pool_prefix_size, object)
        self.assertIsInstance(server.pool_prefix_start, object)
        server._multi_servers = MagicMock()
        self.assertIsInstance(server.multi_servers_config, object)
        builtins.bbe.bbevar = builtins.t
        server = RTDHCPv4Server()
        self.assertIsInstance(server, RTDHCPv4Server)
        server = RTDHCPv6Server()
        self.assertIsInstance(server, RTDHCPv6Server)



if __name__ == '__main__':
    unittest.main()