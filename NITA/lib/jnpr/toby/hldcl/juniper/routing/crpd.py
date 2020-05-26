"""
Class for CRPD Devices
"""
from jnpr.toby.hldcl.juniper.routing import Router
import re
import time


class Crpd(Router):
    """
    Crpd Class
    """
    def __init__(self, *args, **kwargs):
        """
             Initialize class for containerized deamon - cRPD
        """
        super(Crpd, self).__init__(**kwargs)

    def _check_interface_status(self, interfaces, timeout=40, interval=10):
        """
            This checks the interface status on all the junos resources
            :Returns: True if all the interfaces are UP else False
        """
        retry = 1

        while timeout > 0 and retry:
            output = self.cli(command='show interfaces routing', format='text').response()
            for interface in interfaces:
                if re.search(r"^" + re.escape(interface), output, re.MULTILINE):
                    intf = r"^" + re.escape(interface) + r"\s+(\S+)\s+(\S+)"
                    result = re.search(intf, output, re.MULTILINE)
                    message = ''
                    if result:
                        state, addresses = result.groups()
                        t.log(level='INFO', message=str(state))
                        if re.match(r'up', state, re.IGNORECASE):
                            self.log(level="INFO", message="Interface " + str(interface) + " State is : up")
                            retry = 0
                        else:
                            message = "Interface " + str(interface) + " State is down. "
                            retry = 1
                    else:
                        message = "Could not fetch the status of the interface."
                        retry = 1
                else:
                    retry = 1
                    message = "Interface " + str(interface) + " specified in yaml does not exists on the router."
                if retry:
                    timeout = timeout - interval
                    if timeout > 0:
                        self.log(level="WARN", message=str(message) + ' Trying again in %s seconds' % interval)
                    else:
                        self.log(level="ERROR", message=str(message))
                    time.sleep(interval)
                    break

        if retry:
            return False
        return True
