"""
Class for BrocadeNode Devices
"""
from jnpr.toby.hldcl.node import Node

class BrocadeNode(Node):
    """
    Class Node to create brocade node objects.
    """

    def __init__(self, node_data):
        """
        Base class for brocade devices

        :param nodedict:
            **REQUIRED** node_data of node
        :return: node object based os and model
        """
        super(BrocadeNode, self).__init__(node_data)
