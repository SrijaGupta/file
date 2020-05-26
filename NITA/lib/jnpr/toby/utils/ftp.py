"""
FTP utility
"""

import ftplib
import os
import logging


logger = logging.getLogger("jnpr.toby.utils.file_transfer")


class FTP(ftplib.FTP):
    """
    FTP utility can be used to transfer files to and from device.
    """

    def __init__(self, host, user=None, password=None, **ftpargs):
        """
        :param Device junos: Device object
        :param kvargs ftpargs: any additional args to be passed to ftplib FTP
        Supports python *context-manager* pattern.  For example::
            from jnpr.junos.utils.ftp import FTP
            with FTP(dev) as ftp:
                ftp.put(package, remote_path)
        """

        self.host = host
        timeout = ftpargs.get('timeout', 30)
        self._ftpargs = ftpargs
        ftplib.FTP.__init__(self, self.host, user, password, timeout)
        self.open()

    # dummy function, as connection is created by ftb lib in __init__ only
    def open(self):
        return self

    def put_file(self, local_file, remote_file=None):
        """
        This function is used to upload file to the router from local
        execution server/shell.
        :param local_file:
            ***REQUIRED*** Full path along with filename which has to be
            copied to router
        :param remote_file:
            *OPTIONAL* Path along with file name with whcih local_file
            should be stored on the host. If not given will be stored with
            same name in the default home location
        :returns: True if the transfer succeeds, else False
        """

        try:
            if not isinstance(local_file, (list, tuple)):
                local_file = [local_file]
            for file in local_file:
                if remote_file is None:
                    remote_file = os.path.split(file)[1]
                print('Check1')
                self.storbinary('STOR ' + remote_file, open(file, 'rb'))
        except Exception as ex:
            logger.error(ex)
            raise Exception('Could not Transfer file')
        return True

    def get_file(self, remote_file, local_file):
        """
        This function is used to download file from router to local execution
        server/shell.
        :param local_file:
            **REQUIRED** File name to be stored locally
        :param remote_file:
            **REQUIRED** Full path along with filename on the host
        :returns: True if the transfer succeeds, else False
        """
        try:

            self.retrbinary('RETR ' + remote_file,
                            open(local_file, 'wb').write)
        except Exception as ex:
            logger.error(ex)
            raise Exception('Could not Transfer file')
        return True

    # -------------------------------------------------------------------------
    # CONTEXT MANAGER
    # -------------------------------------------------------------------------

    def __enter__(self):
        # return self.open(**self._ftpargs)
        return self

    def __exit__(self, exc_ty, exc_val, exc_tb):
        return self.close()
