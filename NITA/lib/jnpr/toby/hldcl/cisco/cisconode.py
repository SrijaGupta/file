"""
Class for CiscoNode Devices
"""
from jnpr.toby.hldcl.node import Node


class CiscoNode(Node):
    """
    Class Node to create IOS node objects.
    """

    def __init__(self, node_data):
        """
        Base class for IOS devices

        :param nodedict:
            **REQUIRED** node_data of node
        :return: node object based os and model
        """
        super(CiscoNode, self).__init__(node_data)
