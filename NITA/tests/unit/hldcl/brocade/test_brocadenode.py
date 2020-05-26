import os
import unittest
import logging
from mock import MagicMock
from mock import patch
from jnpr.toby.hldcl.node import Node
from jnpr.toby.hldcl.brocade.brocadenode import BrocadeNode

class TestBrocadeNodeModule(unittest.TestCase):
    
    @patch('jnpr.toby.hldcl.node.Node.__init__')
    def test_init(self, patch_node):
        patch_node.return_value = None
        BrocadeNode(node_data='abc')

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    unittest.main()
