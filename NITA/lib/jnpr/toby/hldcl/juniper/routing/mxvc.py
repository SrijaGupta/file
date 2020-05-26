# pylint: disable=missing-docstring,unused-import,inconsistent-return-statements,no-member

from jnpr.toby.hldcl.juniper.routing.mx import Mx
import re
from lxml import etree
from jnpr.toby.exception.toby_exception import TobyException
import pdb
import time

class MxVc(Mx):

    def switch_re_master(self, retry=True):
        """
        device_object.switch_re_master()

        """
        self.log(level="DEBUG",
                 message="Entering 'switch_re_master'\n" + __file__)
        if self.dual_controller is False:
            self.log(level='info', message='Toby connected to only master RE, so skipping RE mastership switchover')
            return True
        try:
            command = "request virtual-chassis routing-engine master switch"
            resp = self.cli(command=command, pattern=[r'Toggle mastership between routing engines.*']).response()
            resp = self.cli(command='yes').response()
            if not re.search(r'error: ', resp, re.IGNORECASE):  # pylint: disable= no-else-return
                self.log(level='INFO', message='RE mastership switchover successful')
                return True
            elif retry is True:
                match = re.search(r'Not ready for mastership switch, '
                                  r'try after (\d+) secs.|error: Mastership switch not supported during '
                                  r'fru reconnect | error: mastership switch request NOT honored, backup not ready', resp)
                if match:
                    if match.group(1) is not None:
                        wait = int(match.group(1)) + 2
                    else:
                        wait = 30
                    self.log(level='INFO', message='A mastership switch was recently executed.'
                             ' Waiting for %s seconds before retrying.' % wait)
                    time.sleep(wait)
                    return_value = self.switch_re_master(retry=False)
                    return return_value
        except Exception as err:
            raise TobyException(err)
