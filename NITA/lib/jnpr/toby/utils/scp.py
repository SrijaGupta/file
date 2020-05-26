"""
Secure Copy Utility
"""

from __future__ import absolute_import
import inspect
import os
from scp import SCPClient
from jnpr.toby.exception.toby_exception import TobyException
import logging
import paramiko

LOGGER = logging.getLogger("jnpr.toby.utils.file_transfer")


class SCP(SCPClient):
    """
    The SCP utility is used to conjunction with :class:`jnpr.junos.utils.sw.SW`
    when transferring the Junos image to the device.  The :class:`SCP` can be
    used for other secure-copy use-cases as well; it is implemented to support
    the python *context-manager* pattern.  For example::
        from jnpr.junos.utils.scp import SCP
        with SCP(dev, progress=True) as scp:
            scp.put(package, remote_path)
    """
    def __init__(self, host, user=None, password=None, port=None, proxy=None, \
                 proxy_user=None, proxy_host=None, proxy_password=None, \
                 proxy_port=None, proxy_ssh_key=None, socket_timeout=30, **scpargs):
        """
        Constructor that wraps :py:mod:`paramiko` and :py:mod:`scp` related
        objects.
        :param Device junos: the Device object
        :param kvargs scpargs: any additional args to be passed to paramiko SCP
        """
        self.host = host
        self.user = user
        if port:
            self.port = port
        else:
            self.port = 22
        self.password = password
        self._scpargs = scpargs
        self._by10pct = 0
        self.proxy = False
        self._user_progress = self._scpargs.get('progress')
        socket_timeout = scpargs.pop('timeout', 30)
        self._scpargs['socket_timeout'] = socket_timeout
        if proxy is True:
            self.proxy = proxy
            self.proxy_user = proxy_user
            self.proxy_host = proxy_host
            self.proxy_password = proxy_password
            self.proxy_ssh_key = proxy_ssh_key
            self.proxy_port = proxy_port
        if self._user_progress is True:
            self._scpargs['progress'] = self._scp_progress
        elif callable(self._user_progress):
            # User case also define progress with 3 params, the way scp module
            # expects. Function will take path, total size, transferred.
            # https://github.com/jbardin/scp.py/blob/master/scp.py#L97
            spec = inspect.getargspec(self._user_progress)
            if len(spec.args) == 3:
                self._scpargs['progress'] = self._user_progress
            else:
                # this will override the function _progress_local defined for this
                # class to use progress provided by user.
                self._progress = lambda report: \
                    self._user_progress(self.host, report)
                self._scpargs['progress'] = self._scp_progress
        self.open()
        if not self.proxy:
            super(SCP, self).__init__(self._ssh.get_transport(), **scpargs)
    def _progress_local(self, report):
        """ simple progress report function """
        print(self.host + ": " + report)

    def _scp_progress(self, _path, _total, _xfrd):

        # calculate current percentage xferd
        pct = int(float(_xfrd) / float(_total) * 100)

        # if 10% more has been copied, then print a message
        if (pct % 10) == 0 and pct != self._by10pct:
            self._by10pct = pct
            self._progress_local(
                "%s: %s / %s (%s%%)" %
                (_path, _xfrd, _total, str(pct)))

    def open(self):
        """
        Creates an instance of the scp object and return to caller for use.
        .. note:: This method uses the same username/password authentication
                   credentials as used by :class:`jnpr.junos.device.Device`.
        .. warning:: The :class:`jnpr.junos.device.Device`
                     ``ssh_private_key_file``
                     option is currently **not** supported.
        .. todo:: add support for ``ssh_private_key_file``.
        :returns: SCPClient object
        """
        # @@@ should check for multi-calls to connect to ensure we don't keep
        # @@@ opening new connections
        if self.proxy:
            port = 22
            transport = paramiko.Transport((self.proxy_host, self.proxy_port))
            transport.start_client()
            if self.proxy_ssh_key:
                privkey = paramiko.RSAKey.from_private_key_file(self.proxy_ssh_key)
                conn_result = transport.auth_publickey(username=self.proxy_user, key=privkey)
            else:
                conn_result = transport.auth_password(username=self.proxy_user, password=self.proxy_password)
            if len(conn_result) != 0:
                raise Exception('Could not create Channel for file transfer')
            tunnel = paramiko.Transport(transport.open_channel(kind='direct-tcpip', dest_addr=(self.host, port), src_addr=('127.0.0.1', 0)))
            tunnel.start_client()
            conn_result = tunnel.auth_password(username=self.user, password=self.password)
            if len(conn_result) != 0:
                raise Exception('Could not create Channel for file transfer')
            self._ssh = paramiko.SFTPClient.from_transport(tunnel)
        else:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sock = None
            self._ssh.connect(hostname=self.host, \
                              port=self.port, \
                              username=self.user, \
                              password=self.password, \
                              sock=sock \
                              )
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
        if self.proxy:
            try:
                self._ssh.get(remote_file, local_file)
            except Exception as exp:
                raise TobyException('Could not transfer file: %s' % str(exp))
        else:
            try:

                self.get(local_path=local_file, remote_path=remote_file)
            except Exception as exp:
                logging.error(exp)
                raise TobyException('Could not transfer file: %s' % str(exp))
        return True

    def put_file(self, local_file, remote_file=None, **kwargs):
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
        logging.info(kwargs)
        if self.proxy:
            try:
                self._ssh.put(local_file, remote_file)
            except Exception as exp:
                LOGGER.error(exp)
                raise Exception('Could not transfer file: %s' % str(exp))
        else:
            try:
                if not isinstance(local_file, (list, tuple)):
                    local_file = [local_file]
                for file_name in local_file:
                    if remote_file is None:
                        remote_file = os.path.split(file_name)[1]
                    self.put(files=file_name, remote_path=remote_file)
            except Exception as ex:
                LOGGER.error(ex)
                raise Exception('Could not Transfer file: %s' % str(ex))
        return True

    def close(self):
        """
        Closes the ssh/scp connection to the device
        """
        self._ssh.close()

    # -------------------------------------------------------------------------
    # CONTEXT MANAGER
    # -------------------------------------------------------------------------

    def __enter__(self, **kwargs):
        return self

    def __exit__(self, exc_ty, exc_val, exc_tb):
        self.close()
