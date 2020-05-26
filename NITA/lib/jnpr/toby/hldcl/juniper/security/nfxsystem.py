"""
Class for NfxSystem Devices
"""
from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem

class NfxSystem(SrxSystem):
    """
    Class System to create JunOS NFX System object.
    """
    def __init__(self, system_data):
        """
        Base class for JunOS NFX system
        """

        # For now since NFX devices are not HA we will set this to False
        self.ha = False
        super(NfxSystem, self).__init__(system_data)
