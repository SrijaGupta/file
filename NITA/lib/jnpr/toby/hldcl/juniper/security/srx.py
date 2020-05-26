"""
SRX Model Handling
"""
from jnpr.toby.hldcl.juniper.security.security import Security


class Srx(Security):
    """
    SRX related functions
    """
    def __init__(self, *args, **kwargs):
        super(Srx, self).__init__(**kwargs)
        self.reboot_timeout  = 900
        self.upgrade_timeout = 1800
        self.issu_timeout = 2700

    def vty(self, **kwargs):
        """
        Executes vty commands on the specified destination.
        :param command:
            **REQUIRED**  vty command to be executed
        :param destination:
            **REQUIRED**  destination to vty into.  example: fpc0
        :param timeout:
            **OPTIONAL**  max time to wait for response. Default is 60s
        :return: Exception if vty fails, else vty command response
        """

        if self.su():
            return super(Srx, self).vty(**kwargs)
        else:
            self.log(level='ERROR', message='Unable to switch to root')
            return False

class VSrx(Srx):
    """
	VSRX related functions
	"""
    pass


class CSrx(Security):
    """
	CSRX related functions
	"""
    pass
