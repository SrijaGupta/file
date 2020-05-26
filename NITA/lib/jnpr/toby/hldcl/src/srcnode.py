"""
Class for SrcNode
"""
from jnpr.toby.hldcl.juniper.junipernode import JuniperNode

class SrcNode(JuniperNode):
    """
    Class to create SRC node objects.
    """
    def __init__(self, *args, **kwargs):
        """
        Base class for SRC devices

        :param nodedict:
            **REQUIRED** node_data of node
        :return: node object based os and model
        """
        super(SrcNode, self).__init__(*args, **kwargs)
