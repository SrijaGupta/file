"""
Class for SrcSystem
"""
from jnpr.toby.hldcl.juniper.junipersystem import JuniperSystem 


class SrcSystem(JuniperSystem):
    """
    Class  to create SRC system objects.
    """
    def __init__(self, system_data):
        """
        Base class for IOS devices

        """
        super(SrcSystem, self).__init__(system_data)
