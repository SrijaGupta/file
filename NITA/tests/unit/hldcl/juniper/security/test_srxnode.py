"""UT for the module jnpr.toby.hldcl.juniper.security.srxnode"""

import unittest2 as unittest
from mock import patch, MagicMock

from collections import defaultdict
from jnpr.toby.hldcl.juniper.security.srxnode import SrxNode

class TestSrxNode(unittest.TestCase):
    """UT for SrxNode"""
    @patch('jnpr.toby.hldcl.juniper.security.srxnode.JuniperNode.__init__')
    def test_srxnode_init(self, sup_init_patch):
        """Test '__init__' method of class SrxNode"""
        self.assertIsInstance(SrxNode(), SrxNode)
        self.assertTrue(sup_init_patch.called)

    @patch('jnpr.toby.hldcl.juniper.security.srxnode.etree')
    @patch('jnpr.toby.hldcl.juniper.security.srxnode.re')
    @patch('jnpr.toby.hldcl.juniper.security.srxnode.jxmlease')
    def test_srxnode_node_name(self, jxm_patch, re_patch, etree_patch):
        """Test 'node_name' method of class SrxNode"""
        sobject = MagicMock(spec=SrxNode)
        sobject.current_controller = MagicMock()
        channel_obj = MagicMock()
        sobject.current_controller.channels = {'text': channel_obj}
        channel_obj.cli.return_value = "text"

        # Exception
        jxm_patch.parse_etree.return_value = {}
        self.assertRaises(Exception, SrxNode.node_name, sobject)

        status = defaultdict(lambda: defaultdict(dict))
        status['multi-routing-engine-results']['multi-routing-engine-item'][0] =\
              defaultdict(lambda: defaultdict(dict))
        status['multi-routing-engine-results']['multi-routing-engine-item'][1] =\
              defaultdict(lambda: defaultdict(dict))
        status['multi-routing-engine-results']['multi-routing-engine-item'][0][
            'software-information']['host-name'] = "node0"
        status['multi-routing-engine-results']['multi-routing-engine-item'][1][
            'software-information']['host-name'] = "node1"
        jxm_patch.parse_etree.return_value = status
        re_patch.match.return_value = MagicMock()
        # return node0_name
        sobject.current_controller.shell.return_value.response.return_value = "node0"
        self.assertEqual(SrxNode.node_name(sobject), "node0")
        # return node1_name
        sobject.current_controller.shell.return_value.response.return_value = "node1"
        self.assertEqual(SrxNode.node_name(sobject), "node1")
        # return None
        sobject.current_controller.shell.return_value.response.return_value = "node"
        self.assertEqual(SrxNode.node_name(sobject), None)

    def test_srxnode_is_node_master(self):
        """Test 'is_node_master method' of class SrxNode"""
        sobject = MagicMock(spec=SrxNode)
        self.assertTrue(SrxNode.is_node_master(sobject))

    @patch('jnpr.toby.hldcl.juniper.security.srxnode.etree')
    @patch('jnpr.toby.hldcl.juniper.security.srxnode.re')
    @patch('jnpr.toby.hldcl.juniper.security.srxnode.jxmlease')
    def test_srxnode_is_node_status_primary(self, jxm_patch, re_patch, etree_patch):
        """Test 'is_node_status_primary' method of class SrxNode"""
        sobject = MagicMock(spec=SrxNode)
        sobject.current_controller = MagicMock()
        channel_obj = MagicMock()
        sobject.current_controller.channels = {'text': channel_obj}
        channel_obj.cli.return_value = "text"

        # Exception
        jxm_patch.parse_etree.return_value = {}
        self.assertRaises(Exception, SrxNode.is_node_status_primary, sobject)

        status = defaultdict(lambda: defaultdict(dict))
        status = status['chassis-cluster-status']['redundancy-group']['device-stats'] =\
                 defaultdict(lambda: defaultdict(dict))

        sobject.node_name.return_value = 'node0'
        status['redundancy-group-status'][0] = 'primary'
        re_patch.match.return_value = MagicMock()
        jxm_patch.parse_etree.return_value = status
        self.assertTrue(SrxNode.is_node_status_primary(sobject))

        sobject.node_name.return_value = 'node1'
        status['redundancy-group-status'][1] = 'primary'
        jxm_patch.parse_etree.return_value = status
        self.assertTrue(SrxNode.is_node_status_primary(sobject))

        sobject.node_name.return_value = 'node'
        self.assertFalse(SrxNode.is_node_status_primary(sobject))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestSrxNode)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
