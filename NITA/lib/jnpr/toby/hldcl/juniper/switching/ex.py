"""
Class for Ex, Qfx, Ocx & Nfx
"""
from jnpr.toby.hldcl.juniper.switching import switch
from jnpr.toby.hldcl.juniper.security.srx import Srx


class Ex(switch.Switch):
    """
    Base class for Ex devices
    """
    pass


class Qfx(switch.Switch):
    """
    Base class for Qfx devices
    """
    pass


class Ocx(switch.Switch):
    """
    Base class for Ocx devices
    """
    pass


class Nfx(switch.Switch, Srx):
    """
    Base class for Nfx devices

    Gets its functionality from both Switch class and Srx (Security) class
    """
    def __init__(self, *args, **kwargs):
        super(Nfx, self).__init__(**kwargs)
        self.core_path = ["/var/jails/rest-api/tmp/*core*", "/tftpboot/corefiles/*core*", "/var/third-party/jcrash/*core*",
                          "/var/crash/*core*", "/var/tmp/*core*", "/var/tmp/pics/*core*",
                          "/var/core/*/*core*", "/var/lib/ftp/in/*/*core*", "/var/crash/corefiles/*core*"]
        self.powercyler_pattern = ".*(Press enter to boot the selected OS).*"
