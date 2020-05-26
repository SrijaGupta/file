import sys

import unittest2 as unittest
from mock import patch, MagicMock
from nose.plugins.attrib import attr
from lxml import etree

from jnpr.toby.hldcl.host import *


@attr('unit')
class TestHost(unittest.TestCase):
    def test_host__next_log_file_name(self):
        hobject = MagicMock(spec=Host)
        hobject._object_counts = {}

        # If no logger created for the filename
        self.assertEqual(Host._next_log_file_name(hobject, name='Device'), 'Device')

        # If the log filename already has logger created
        hobject._object_counts['Device'] = 0
        self.assertEqual(Host._next_log_file_name(hobject, name='Device'), 'Device.1')

        # Check with no arguments
        self.assertRaises(Exception, Host._next_log_file_name, hobject)

    def test_host_get_credentials_failures(self):
        hobject = MagicMock(spec=Host)
        hobject.os = 'Test'
        self.assertRaises(
            Exception,
            Host.get_credentials, hobject, **{'os': 'asdad'}
        )

    @patch('jnpr.toby.hldcl.host.credentials')
    def test_host_get_credentials(self, cred_mock):
        hobject = MagicMock(spec=Host)
        hobject.os = 'JUNOS'
        cred_mock.JUNOS = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        hobject.os = 'UNIX'
        cred_mock.UNIX = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        hobject.os = 'IOS'
        cred_mock.IOS = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        hobject.os = 'SPIRENT'
        cred_mock.SPIRENT = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        hobject.os = 'IXIA'
        cred_mock.IXIA = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        hobject.os = 'WINDOWS'
        cred_mock.WINDOWS = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        hobject.os = 'BREAKINGPOINT'
        cred_mock.BREAKINGPOINT = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        hobject.os = 'BPS'
        cred_mock.BREAKINGPOINT = {'USERNAME': 'user', 'PASSWORD': 'password'}
        self.assertEqual(Host.get_credentials(hobject), ('user', 'password'))

        # If default credentials are not available
        hobject.os = 'JUNOS'
        cred_mock.JUNOS = {'USERNAME': None, 'PASSWORD': None}
        self.assertRaises(Exception, Host.get_credentials, hobject)

        # Check with user and password passed as arguments
        self.assertEqual(Host.get_credentials(hobject, **{'user': 'user', 'password': 'password'}), ('user', 'password'))
        self.assertEqual(Host.get_credentials(hobject, **{'user': 'user', 'password': 'password','ssh_key_file':'key_file'}), ('user', 'password'))

    @patch('jnpr.toby.hldcl.host.credentials')
    def test_host_get_su_credentials_failures(self, cred_mock):
        hobject = MagicMock(spec=Host)
        hobject.os = 'JUNOS1'
        self.assertRaises(Exception, Host.get_su_credentials, hobject)

    @patch('jnpr.toby.hldcl.host.credentials')
    def test_host_get_su_credentials(self, cred_mock):
        hobject = MagicMock(spec=Host)
        hobject.os = 'JUNOS'
        cred_mock.JUNOS = {'SU': 'user', 'SUPASSWORD': 'password'}
        self.assertEqual(Host.get_su_credentials(hobject), ('user', 'password'))
        hobject.os = 'UNIX'
        cred_mock.UNIX = {'SU': 'user', 'SUPASSWORD': 'password'}
        self.assertEqual(Host.get_su_credentials(hobject), ('user', 'password'))
        hobject.os = 'IOS'
        cred_mock.IOS = {'SU': 'user', 'SUPASSWORD': 'password'}
        self.assertEqual(Host.get_su_credentials(hobject), ('user', 'password'))

    @patch('jnpr.toby.utils.ftp.FTP')
    @patch('jnpr.toby.utils.scp.SCP')
    def test_host_upload(self, ftp_mock, scp_mock):
        hobject = MagicMock(spec=Host)
        hobject.proxy = True
        hobject.proxy_host = 'host'
        hobject.proxy_user = 'host'
        hobject.proxy_password = 'host'
        hobject.proxy_ssh_key = 'host'
        hobject.proxy_port = 'host'
        hobject.connect_mode = 'telnet'
        hobject.host = 'device-a'
        hobject.user = 'device-a'
        hobject.password = 'device-a'
        hobject.text_port = None
        # telnet as connect mode
        hobject.controllers_data = {}
        hobject.controllers_data['mgt-ip'] = hobject.host
        self.assertTrue(Host.upload(hobject, local_file='', remote_file=''))
        # ssh as connect mode
        hobject.connect_mode = 'ssh'
        self.assertTrue(Host.upload(hobject, local_file='', remote_file=''))

        # with only user
        self.assertTrue(Host.upload(hobject, local_file='', remote_file='',user='user'))
        # with only password
        self.assertTrue(Host.upload(hobject, local_file='', remote_file='', password="password"))
        # with user and password
        self.assertTrue(Host.upload(hobject, local_file='', remote_file='', user="user", password="password"))

    @patch('jnpr.toby.utils.ftp.FTP')
    @patch('jnpr.toby.utils.scp.SCP')
    def test_host_upload_failures(self, ftp_mock, scp_mock):
        hobject = MagicMock(spec=Host)
        hobject.connect_mode = 'telnet'
        hobject.host = 'device-a'
        hobject.user = 'device-a'
        hobject.password = 'device-a'
        # Invalid protocol
        self.assertRaises(
            Exception,
            Host.upload, hobject, local_file='', remote_file='',
            protocol='sftp'
        )

    @patch('jnpr.toby.utils.ftp.FTP')
    @patch('jnpr.toby.utils.scp.SCP')
    def test_host_download(self, ftp_mock, scp_mock):
        hobject = MagicMock(spec=Host)
        hobject.proxy = True
        hobject.connect_mode = 'telnet'
        hobject.host = 'device-a'
        hobject.user = 'device-a'
        hobject.password = 'device-a'
        hobject.proxy_host = 'host'
        hobject.proxy_user = 'host'
        hobject.proxy_password = 'host'
        hobject.proxy_ssh_key = ''
        hobject.proxy_port = 'host'
        hobject.text_port = None
        hobject.controllers_data = {}
        hobject.controllers_data['mgt-ip'] = hobject.host
        # telnet as connect mode
        self.assertTrue(Host.download(hobject, local_file='', remote_file=''))
        # ssh as connect mode
        hobject.connect_mode = 'ssh'
        self.assertTrue(Host.download(hobject, local_file='', remote_file=''))

        # with only user
        self.assertTrue(Host.download(hobject, local_file='', remote_file='', user="user"))
        # with only password
        self.assertTrue(Host.download(hobject, local_file='', remote_file='', password="password"))
        # with user and password
        self.assertTrue(Host.download(hobject, local_file='', remote_file='', user="user", password="password"))

    @patch('jnpr.toby.utils.ftp.FTP')
    @patch('jnpr.toby.utils.scp.SCP')
    def test_host_download_failures(self, ftp_mock, scp_mock):
        hobject = MagicMock(spec=Host)
        hobject.connect_mode = 'telnet'
        hobject.host = 'device-a'
        hobject.user = 'device-a'
        hobject.password = 'device-a'
        # Invalid protocol
        self.assertRaises(
            Exception,
            Host.download, hobject, local_file='', remote_file='',
            protocol='sftp'
        )

    @patch('jnpr.toby.hldcl.host.Host.get_credentials',return_value=('user','password'))
    @patch('jnpr.toby.hldcl.host.Logger')
    def test_host_init(self, logger_mock, get_cred_patch):
        import builtins
        builtins.t = self
        t.is_robot = True
        t.background_logger = MagicMock()
        t._script_name = 'name'
        t.t_dict = {'console_log':'test'}
        type(logger_mock.return_value).level = 10
        hobject = Host(host='host', os='Junos',global_logging=True, device_logging=True, re_name='re0')
        self.assertEqual(hobject.host, 'host')
        self.assertEqual(hobject.os, 'Junos')
        self.assertEqual(hobject.tag, None)
        self.assertEqual(hobject.logger_name, 'host')
        #logger_mock.assert_any_call('host', console=False)
        #logger_mock.assert_any_call('name', console=False)
        #assert logger_mock.call_count == 2
        
        #self.assertFalse(hobject.proxy)
        #self.assertEqual(hobject.proxy_host, 'a')
        #self.assertEqual(hobject.proxy_password, 'a')
        #self.assertEqual(hobject.proxy_user, 'a')
        #self.assertEqual(hobject.proxy_port, 'a')        
        hobject = Host(host='host', os='Junos', tag='tag',ssh_key_file="test",global_logging=True, device_logging=True, re_name='re0')
        self.assertEqual(hobject.host, 'host')
        self.assertEqual(hobject.os, 'Junos')
        self.assertEqual(hobject.tag, 'tag')
        self.assertEqual(hobject.logger_name, 'host.1')
        #logger_mock.assert_any_call('host.1', console=False)
        #assert logger_mock.call_count == 4

        hobject = Host(host='host', os='Junos', tag='tag', hostname='hostname',global_logging=True, device_logging=True, re_name='re0')
        self.assertEqual(hobject.host, 'host')
        self.assertEqual(hobject.os, 'Junos')
        self.assertEqual(hobject.tag, 'tag')
        self.assertEqual(hobject.name, 'hostname')
        self.assertEqual(hobject.logger_name, 'hostname')
        #assert logger_mock.call_count == 6

        t.is_robot = False
        t.background_logger = None
        self.assertIsInstance(Host(host='host', os='Junos',global_logging=True, device_logging=True, re_name='re0'), Host)
        #logger_mock.assert_any_call('name', console=True)
        #logger_mock.assert_any_call('host.2', console=False)
        #assert logger_mock.call_count == 8

        del builtins.t
        self.assertIsInstance(Host(host='host', os='Junos',global_logging=True, device_logging=True, re_name='re0'), Host)
        #logger_mock.assert_any_call('host.3', console=True)
        #assert logger_mock.call_count == 9

        # With no arguments
        self.assertRaises(Exception, Host)
        # With only one argument
        self.assertRaises(Exception, Host, host='host')
        self.assertRaises(Exception, Host, os='Junos')

        get_cred_patch.return_value = ('user', None)
        self.assertIsInstance(Host(host='host', os='Junos',global_logging=True, device_logging=True, re_name='re0'), Host)

    def test_host_log(self):
        hobject = MagicMock(spec=Host)
        hobject.device_logger = MagicMock()
        hobject.logger_name = MagicMock()
        hobject.global_logger = MagicMock()
        hobject.device_logger_flag = True
        hobject.global_logger_flag = True

        xmldata = etree.XML('<software-information></software-information>')

        import builtins
        builtins.t = self

        ## Check for t_exists = False
        hobject.t_exists = False
        self.assertIsNone(Host.log(hobject, message=xmldata))
        self.assertTrue(hobject.device_logger._log.called)

        # Check with only 'level' argument
        self.assertIsNone(Host.log(hobject, level='INFO'))
        assert hobject.device_logger._log.call_count == 2
        self.assertFalse(hobject.global_logger._log.called)

        # Check with only 'message' argument
        self.assertIsNone(Host.log(hobject, message=xmldata))
        assert hobject.device_logger._log.call_count == 3
        self.assertFalse(hobject.global_logger._log.called)

        # with two arguments
        self.assertIsNone(Host.log(hobject, message=xmldata, level='INFO'))
        assert hobject.device_logger._log.call_count == 4
        self.assertFalse(hobject.global_logger._log.called)

        ## Check for t_exists = True
        hobject.t_exists = True
        t.is_robot = True
        t.background_logger = MagicMock()
        t.t_dict = {'console_log':'test'}
        hobject.global_logger.level = 30
        with patch('robot.api.logger') as robot_logger:
            # with two arguments

            self.assertIsNone(Host.log(hobject, message=xmldata, level='WARN'))
            assert hobject.device_logger._log.call_count == 5
            self.assertTrue(robot_logger.warn.called)
            self.assertTrue(hobject.global_logger._log.called)

        t.is_robot = False
        t.background_logger = None
        self.assertIsNone(Host.log(hobject, message=xmldata))
        assert hobject.device_logger._log.call_count == 6
        self.assertTrue(hobject.global_logger._log.called)

        # Check with no arguments
        self.assertRaises(Exception, Host.log, hobject)

        t.is_robot = True
        del t.t_dict['console_log']
        self.assertIsNone(Host.log(hobject, message=xmldata))
        t.t_dict = {'console_log': None}
        self.assertIsNone(Host.log(hobject, message=xmldata))

    def test_device_upload_file(self):
        dobject = MagicMock()
        dobject.upload = MagicMock(return_value='test_str')
        self.assertEqual(upload_file(dobject), 'test_str')
        # Exception case
        dobject.upload = MagicMock(return_value=False)
        self.assertRaises(Exception, upload_file, dobject)

    def test_device_download_file(self):
        dobject = MagicMock()
        dobject.download = MagicMock(return_value='test_str')
        self.assertEqual(download_file(dobject), 'test_str')
        # Exception case
        dobject.download = MagicMock(return_value=False)
        self.assertRaises(Exception, download_file, dobject)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHost)
    unittest.TextTestRunner(verbosity=2).run(suite)

