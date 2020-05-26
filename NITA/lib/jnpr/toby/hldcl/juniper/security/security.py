"""
Module to handle security products
"""
from jnpr.toby.hldcl.juniper.junos import Juniper


class Security(Juniper):
    """
    Class to handle security products
    """
    def re_slot_name(self):
        """

        Retrieves connected RE slot name

        :return: RE slot name
        """
        # return self.re.upper()
        # For non multi-chassis case
        # if not self.vc_capable:
        # Single RE case, where the re is always master
        return 'RE0'

    def _is_master(self):
        """

        :return: Boolean. True if RE is master.
        """
        return True
