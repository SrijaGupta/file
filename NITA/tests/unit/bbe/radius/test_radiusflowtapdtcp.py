import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.bbe.radius.radiusflowtapdtcp import RadiusFlowtapDtcp
builtins.t = MagicMock()
builtins.t.log = MagicMock()
dtcp = MagicMock(spec=RadiusFlowtapDtcp)

class TestRadiusFlowTapDtcp(unittest.TestCase):
    """
    TestRadiusFlowTapDtcp class to handle radiusflowtapdtcp.py unit tests
    """
    @patch('os.remove')
    def test_dtcp_add_filter(self, patch_os):
        dtcp_args = {'router': 'r0', 'num_filt': '1', 'version': '0.7', 'src_addr': '10.0.0.1',
                     'dst_addr': '20.0.0.1', 'filter_type': 'inoutvrfnegv6', 'cdest2_id': 'cd2', 'cdest1_id': 'cd1',
                     'csource_port': '2001', 'csource_id': 'scid', 'cdest2_addr': '200.0.0.1', 'intf': 'eth1',
                     'cdest1_addr': '100.0.0.1', 'cdest1_port': '80', 'cdest2_port': '90', 'src_port': '801',
                     'dst_port': '901', 'protocol': 'dtcp', 'csource_addr': '30.0.0.1', 'ttl': '64',
                     'src_step': 1}
        dtcp._dtcp_response.return_value = ('ssdfe', 1)
        dtcp._flow_tap.return_value = 'aabbb'
        self.assertEqual(RadiusFlowtapDtcp.dtcp_add_filter(dtcp, **dtcp_args), True)
        dtcp_args.pop('cdest2_id')
        dtcp_args['src_addr'] = '*'
        dtcp_args['dst_addr'] = '*'
        dtcp_args.pop('src_step')
        dtcp._dtcp_response.return_value = ('ssdfe', 0)
        self.assertEqual(RadiusFlowtapDtcp.dtcp_add_filter(dtcp, **dtcp_args), False)
        dtcp_args.pop('cdest1_id')
        dtcp_args['cdest2_id'] = 'cd2'
        self.assertEqual(RadiusFlowtapDtcp.dtcp_add_filter(dtcp, **dtcp_args), False)

    @patch('os.remove')
    def test_dtcp_add_sbr_filter(self, patch_os):
        dtcp_args = {'router': 'r0', 'num_filt': '1', 'version': '0.7', 'src_addr': '10.0.0.1',
                     'dst_addr': '20.0.0.1', 'filter_type': 'inoutvrfnegv6', 'cdest_id': 'cd2', 'cdest1_id': 'cd1',
                     'csource_port': '2001', 'csource_id': 'scid', 'cdest_addr': '200.0.0.1', 'user_name': 'test',
                     'li': '1', 'ri': 'vr', 'cdest_port': '90', 'src_port': '801',
                     'dst_port': '901', 'protocol': 'dtcp', 'csource_addr': '30.0.0.1', 'ttl': '64', 'circuit_id': 'circ1'}
        dtcp._dtcp_response.return_value = ('ssdfe', 1)
        dtcp._flow_tap.return_value = 'aabbb'
        self.assertEqual(RadiusFlowtapDtcp.dtcp_add_sbr_filter(dtcp, **dtcp_args), True)
        dtcp._dtcp_response.return_value = ('ssdfe', 0)
        self.assertEqual(RadiusFlowtapDtcp.dtcp_add_sbr_filter(dtcp, **dtcp_args), False)

    @patch('os.remove')
    @patch('builtins.open')
    def test_dtcp_list_filter(self, patch_open, patch_os):
        dtcp_args = {'router': 'r0', 'id': 'cdest', 'csource_id': 'csid', 'flag': 'qq', 'id_val': '1122'}
        dtcp._dtcp_response.return_value = ('ssdfe', 1)
        dtcp._flow_tap.return_value = 'aabbb'
        self.assertEqual(RadiusFlowtapDtcp.dtcp_list_filter(dtcp, **dtcp_args), True)
        dtcp_args['id'] = 'c'
        dtcp_args['csource'] = 'cs'
        dtcp_args['flags'] = 'ss'
        dtcp._dtcp_response.return_value = ('ssdfe', 0)
        self.assertEqual(RadiusFlowtapDtcp.dtcp_list_filter(dtcp, **dtcp_args), False)

    @patch('os.remove')
    @patch('builtins.open')
    def test_dtcp_delete_filter(self, patch_open, patch_os):
        dtcp_args = {'router': 'r0', 'id': 'cdest', 'csource_id': 'csid', 'flag': 'qq', 'id_val': '1122'}
        dtcp._dtcp_response.return_value = ('ssdfe', 1)
        dtcp._flow_tap.return_value = 'aabbb'
        self.assertEqual(RadiusFlowtapDtcp.dtcp_delete_filter(dtcp, **dtcp_args), True)
        dtcp_args['id'] = 'c'
        dtcp._dtcp_response.return_value = ('ssdfe', 0)
        self.assertEqual(RadiusFlowtapDtcp.dtcp_delete_filter(dtcp, **dtcp_args), False)

    @patch('time.sleep')
    @patch('hmac.new')
    @patch('builtins.open')
    @patch('paramiko.Transport')
    @patch('socket.socket')
    @patch('paramiko.SSHClient')
    def test_flow_tap(self, patch_ssh, patch_socket, patch_transport, patch_open, patch_hmac, patch_sleep):
        patch_open.return_value.readlines.return_value = ['seq', 'test', '']
        self.assertIsInstance(RadiusFlowtapDtcp._flow_tap(dtcp, 'r0', 'user', 'test', 'file'), str)

    @patch('builtins.open')
    @patch('time.sleep')
    def test_dtcp_response(self, patch_sleep, patch_open):
        patch_open.return_value.readlines.return_value = ['DTCP/0.7 200 ADC']
        self.assertIsInstance(RadiusFlowtapDtcp._dtcp_response(dtcp, 'test'), tuple)
        patch_open.return_value.readlines.return_value = ['DTCP/0.7 101 cd']
        self.assertIsInstance(RadiusFlowtapDtcp._dtcp_response(dtcp, 'test'), tuple)
        patch_open.return_value.readlines.return_value = ['', 'abc', 'Received disconnect']
        self.assertIsInstance(RadiusFlowtapDtcp._dtcp_response(dtcp, 'test'), tuple)

if __name__ == '__main__':
    unittest.main()
