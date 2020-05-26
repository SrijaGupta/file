import unittest2 as unittest
from mock import patch, MagicMock, PropertyMock
from jnpr.toby.hldcl.unix.unix import Unix, UnixHost, FreeBSD, CentOS
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.connectors.sshconn import SshConn
from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
from telnetlib import Telnet

import os
from nose.plugins.attrib import attr
from jnpr.toby.logger.logger import Logger
import robot.api.logger as robot_logger

ret_val = [False, True]
builtin_string = 'builtins'

@attr('unit')
class Mockhandle(object):
    def write(self, *args, **kwargs):
        pass

    def expect(self, *args, **kwargs):
        if 'version' in os.environ and os.environ['version'] == 'freebsd':
            return 1, 1, b'FreeBSD'
        elif 'version' in os.environ and os.environ['version'] == 'centos':
            return 1, 1, b'Linux'
        else:
            return 1, 1, b'Junos'


class TestJunosModule(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = self
        t.is_robot = True
        t._script_name = 'name'
        t.log = MagicMock()

    @patch('jnpr.toby.hldcl.unix.unix.Host.__init__')
    def test_unixhost_init(self, patch_host_init):
        uobject = UnixHost(unix_flavour='UNIX', osname='UNIX',handle='test', host='host')
        self.assertEqual(uobject.model, 'UNIX')
        self.assertEqual(uobject.handle, 'test')
        self.assertTrue(patch_host_init.called)

    def test_unixhost_get_model(self):
        uobject = MagicMock(spec=UnixHost)

        uobject.shell.return_value.response.return_value = " test"
        self.assertIsNone(UnixHost.get_model(uobject))

        uobject.shell.return_value.response.return_value = "mx480"
        self.assertEqual(UnixHost.get_model(uobject), "mx480")

        uobject.model = "mx2020"
        self.assertEqual(UnixHost.get_model(uobject), "mx2020")

    def test_unixhost_get_model_failure(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.name = 'foo'
        uobject.channels = []

        # Exception
        uobject.shell.side_effect = Exception
        try:
            UnixHost.get_model(uobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Could not get model info")

    def test_unixhost_get_version(self):
        uobject = MagicMock(spec=UnixHost)

        uobject.shell.return_value.response.return_value = " test"
        self.assertIsNone(UnixHost.get_version(uobject))

        uobject.shell.return_value.response.return_value = "15.1"
        self.assertEqual(UnixHost.get_version(uobject), "15.1")

        uobject.version = "17.2"
        self.assertEqual(UnixHost.get_version(uobject), "17.2")

    def test_unixhost_get_version_failure(self):

        uobject = MagicMock(spec=UnixHost)
        uobject.name = 'foo'
        uobject.channels = []

        # Exception
        uobject.shell.side_effect = Exception

        try:
            UnixHost.get_version(uobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Could not get version info")

    @patch('jnpr.toby.logger.logger.Logger')
    def test_test1(self, patch1):
        uobject = MagicMock(spec=Unix)
        uobject.handle = MagicMock()
        uobject.prompt = MagicMock(return_value='%')
        uobject.handle.execute = MagicMock(side_effect=Exception)
        self.assertRaises(Exception, UnixHost.execute, command='ls')

    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    @patch('jnpr.toby.hldcl.unix.unix.select', side_effect=[('', '', ''), ('$', '', ''), ('$', '', '')])
    @patch('logging.error')
    @patch('jnpr.toby.hldcl.unix.unix.TelnetConn')
    @patch('jnpr.toby.hldcl.unix.unix.Host.__init__')
    @patch('jnpr.toby.hldcl.unix.unix.CentOS')
    @patch('jnpr.toby.hldcl.unix.unix.FreeBSD')
    def test_unix_get_unix_flavour(self, freebsd_patch, centos_patch, host_patch, telnetconn_patch,
                                   logging_patch, select_patch, sshconn_patch):

        import builtins
        builtins.t = self
        t.log = MagicMock()

        telnetconn_patch.return_value.expect.return_value = ['test1', 'test2', b'Linux']
        obj1 = MagicMock()
        centos_patch.return_value = obj1
        ab = Unix(host="dummy-freebsd", connect_mode='telnet', osname='unix', user='')
        self.assertEqual(ab, obj1)

        telnetconn_patch.return_value.expect.return_value = ['test1', 'test2', b'FreeBSD']
        obj2 = MagicMock()
        freebsd_patch.return_value = obj2
        ab = Unix(host="dummy-freebsd", connect_mode='telnet', osname='unix', user='root', password='Embe1mpls')
        self.assertEqual(ab, obj2)

        # Exception
        telnetconn_patch.return_value.expect.return_value = ['test1', 'test2', b'fedora']
        try:
            ab = Unix(host="dummy-freebsd", connect_mode='telnet', osname='unix', user='')
        except Exception as exp:
            self.assertEqual(exp.args[0], 'Invalid Unix model detected: \'Unknown\'')

        # Exception
        sshconn_patch.return_value.client.recv.side_effect = [b'test', b'>'] 
        try:
            ab = Unix(host="dummy-freebsd", connect_mode='ssh', osname='unix', user='', ssh_key_file='')
        except Exception as exp:
            self.assertEqual(exp.args[0], 'Invalid Unix model detected: \'Unknown\'')

        # Exception
        sshconn_patch.side_effect = Exception
        try:
            ab = Unix(host="dummy-freebsd", connect_mode='ssh', osname='unix', user='')
        except Exception as exp:
            self.assertEqual(exp.args[0], 'Cannot connect to unix Device dummy-freebsd')

    @patch('jnpr.toby.hldcl.unix.unix.FreeBSD')
    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    @patch('jnpr.toby.hldcl.unix.unix.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.unix.unix.FreeBSD.set_prompt')
    @patch('jnpr.toby.hldcl.unix.unix.credentials.get_credentials', return_value=('user','pasword'))
    @patch('jnpr.toby.hldcl.host.Host.log')
    def test_unix_new_param(self, patch1, patch2, patch3, patch4, patch5, patch6):
        obj = MagicMock()
        patch6.return_value = obj
        obj.host = 'host1'

        patch1.client = MagicMock
        patch1.client.recv = MagicMock(return_value=b'FreeBSD vm-soa2-bsd1.'
                                                    b'englab.juniper $')
        ab = Unix(host="dummy-freebsd", connect_mode='ssh', osname='unix', user='', ssh_key_file='')
        #self.assertIsInstance(ab, FreeBSD)
        self.assertEqual(ab, obj)

    @patch('jnpr.toby.hldcl.unix.unix.CentOS')
    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    @patch('jnpr.toby.hldcl.unix.unix.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.unix.unix.UnixHost.set_prompt')
    @patch('jnpr.toby.hldcl.unix.unix.credentials.get_credentials', return_value=('user','pasword'))
    @patch('jnpr.toby.hldcl.host.Host.log')
    def test_unix_new_param2(self, patch1, patch2, patch3, patch4, patch5, patch6):
        obj = MagicMock()
        patch6.return_value = obj
        obj.host = 'host1'

        patch1.client = MagicMock
        patch1.client.recv = MagicMock(return_value=b'Linux vm-soa2-bsd1.'
                                                    b'englab.juniper $')
        ab = Unix(host="dummy-freebsd", connect_mode='ssh', osname='unix', user='', ssh_key_file='')
        #self.assertIsInstance(ab, CentOS)
        self.assertEqual(ab, obj)

    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    @patch('jnpr.toby.hldcl.unix.unix.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.unix.unix.FreeBSD.set_prompt')
    @patch('logging.error')
    def test_unix_new_ssh_freebsd(self, patch1, patch2, patch3, patch4):
        patch1.client = MagicMock
        patch1.client.recv = MagicMock(return_value=b'FreeBSD vm-soa2-bsd1.'
                                                    b'englab.juniper $')

    @patch('jnpr.toby.hldcl.unix.unix.CentOS', return_value='test')
    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    @patch('jnpr.toby.hldcl.unix.unix.select', return_value=('$', '', ''))
    @patch('jnpr.toby.hldcl.unix.unix.CentOS.set_prompt')
    @patch('logging.error')
    def test_unix_new_ssh_linux(self, patch1, patch2, patch3, patch4, patch5):
        obj = MagicMock()
        patch5.return_value = obj
        obj.host = 'host1'

        # TBA line 44: just test existnce not null value
        patch1.client = MagicMock
        patch1.client.recv = MagicMock(return_value=b'Linux tot-linux1 $')
        ab = Unix(host="dummy-freebsd", connect_mode='ssh', os='unix', model='linux', user=False, osname='linux', ssh_key_file='')
        #self.assertIsInstance(ab, CentOS)
        self.assertEqual(ab, obj)

    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    @patch('jnpr.toby.hldcl.unix.unix.select', return_value=('$', '', ''))
    def test_unix_new_ssh_oth(self, patch1, patch2):
        patch1.client = MagicMock
        patch1.client.recv = MagicMock(return_value=b'sun-solaris-bsd1 $')
        self.assertRaises(Exception, lambda: Unix(host="dummy-freebsd",
                                                  connect_mode='ssh',
                                                  os='unix', model='os360'))

    def test_unix_execute(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.handle = MagicMock()
        uobject.prompt = MagicMock(return_value='%')
        uobject.handle.execute = MagicMock(return_value='regress')
        uobject.shell_timeout  = 60
        self.assertEqual(UnixHost.execute(uobject, command='ls'), 'regress')

    def test_unix_disconnect(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.connect_mode = 'ssh'
        uobject.handle = MagicMock()
        uobject.log_handle = MagicMock()
        uobject.close_obj = MagicMock()
        self.assertTrue(UnixHost.close(uobject))

    def test_unix_disconnect2(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.connect_mode = 'telnet'
        uobject.handle = MagicMock()
        uobject.log_handle = MagicMock()
        self.assertTrue(UnixHost.close(uobject))

    def test_unix_close(self):
        self.test_unix_disconnect() 
        uobject = MagicMock(spec=UnixHost)
        self.assertTrue(UnixHost.close(uobject))

    def test_unix_close2(self):
        self.test_unix_disconnect2()
        uobject = MagicMock(spec=UnixHost)
        self.assertTrue(UnixHost.close(uobject))

    def test_unix_set_prompt(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=1)
        uobject.prompt = MagicMock(return_value="TOBY")
        type(uobject).response = PropertyMock(side_effect=['/bin/sh $'])
        self.assertTrue(UnixHost.set_prompt(uobject, prompt='TOBY'))

    def test_unix_set_prompt_bash(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=1)
        uobject.prompt = MagicMock(return_value="TOBY")
        type(uobject).response = PropertyMock(side_effect=['/bin/bash $'])
        self.assertTrue(UnixHost.set_prompt(uobject, prompt='TOBY'))

    def test_unix_set_prompt_csh(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=1)
        uobject.prompt = MagicMock(return_value="TOBY")
        type(uobject).response = PropertyMock(side_effect=['csh $'])
        self.assertTrue(UnixHost.set_prompt(uobject, prompt='TOBY'))

    def test_unix_set_prompt_expection(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=-1)
        uobject.prompt = MagicMock(return_value="TOBY")
        type(uobject).response = PropertyMock(side_effect=['csh $'])
        self.assertRaises(Exception, lambda: UnixHost.set_prompt(uobject, prompt='TOBY'))

    def test_unix_set_prompt_expection2(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=1)
        uobject.prompt = MagicMock(return_value="TOBY")
        type(uobject).response = PropertyMock(side_effect=['vsh $'])
        self.assertRaises(Exception, lambda: UnixHost.set_prompt(uobject, prompt='TOBY'))

    def test_unix_set_prompt_expection3(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(side_effect=[1,-1])
        uobject.prompt = MagicMock(return_value="TOBY")
        type(uobject).response = PropertyMock(side_effect=['csh $'])
        self.assertRaises(Exception, lambda: UnixHost.set_prompt(uobject, prompt='TOBY'))

    def test_unix_su(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=1)
        uobject.get_su_credentials = MagicMock(return_value=('root',
                                                             'Embe1mpls'))
        uobject.prompt = '$ '
        uobject.set_prompt = MagicMock
        uobject.shell.return_value.response.return_value = "root"
        self.assertTrue(UnixHost.su(uobject))

    def test_unix_su_user_password(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=1)
        uobject.prompt = '$ '
        uobject.set_prompt = MagicMock
        uobject.shell.return_value.response.return_value = "root"
        self.assertTrue(UnixHost.su(uobject,password='Embe1mpls'))

    def test_unix_su_exception(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(side_effect=[1,1])
        uobject.prompt = '$ '
        uobject.set_prompt = MagicMock
        uobject.shell = MagicMock(return_value=-1)
        print ('toto')
        self.assertRaises(Exception, lambda: UnixHost.su(uobject, password='Embe1mpls'))

    @patch('time.sleep')
    def test_unix_reboot(self, patch1):
        uobject = MagicMock(spec=UnixHost)
        uobject.su = MagicMock()
        uobject.shell = MagicMock(return_value=-1)
        uobject.is_alive = MagicMock(return_value=False)
        uobject.host = 'dummy'
        uobject.reconnect = MagicMock()
        self.assertTrue(UnixHost.reboot(uobject))

    @patch('jnpr.toby.hldcl.unix.unix.check_socket', side_effect=[True, False])
    @patch('time.sleep')
    def test_unix_reboot_exception1(self, patch1, patch2):
        uobject = MagicMock(spec=UnixHost)
        uobject.su = MagicMock()
        uobject.execute = MagicMock(return_value=1)
        uobject.host = 'dummy'
        uobject.connect_mode = 'ssh'
        uobject.handle = MagicMock()
        uobject.reconnect = MagicMock()
        self.assertRaises(Exception, lambda: UnixHost.reboot(uobject))

    @patch('jnpr.toby.hldcl.unix.unix.check_socket', side_effect=[True, False])
    @patch('time.sleep')
    def test_unix_reboot_exception2(self, patch1, patch2):
        uobject = MagicMock(spec=UnixHost)
        uobject.su = MagicMock()
        uobject.execute = MagicMock(return_value=1)
        uobject.host = 'dummy'
        uobject.connect_mode = 'ssh'
        uobject.handle = MagicMock()
        uobject.reconnect = MagicMock()
        self.assertRaises(Exception, lambda: UnixHost.reboot(uobject))

    @patch('jnpr.toby.hldcl.unix.unix.check_socket')
    @patch('time.sleep')
    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    def test_unix_reconnect(self, patch1, patch2, patch3):
        uobject = MagicMock(spec=UnixHost)
        uobject.prompt = MagicMock(return_value='%')
        uobject.host = 'dummy'
        uobject.user = 'regress'
        uobject.password = 'MaRtInI'
        uobject.connect_mode = 'ssh'
        uobject._kwargs = {'user':'regress','password':'MaRtInI', 'ssh_key_file':'dummy'}
        uobject.handle = MagicMock()
        uobject.set_prompt = MagicMock()
        self.assertTrue(UnixHost.reconnect(uobject))

        uobject.handle.client.get_transport.return_value.isAlive.return_value = False
        self.assertTrue(UnixHost.reconnect(uobject))

    @patch('jnpr.toby.hldcl.unix.unix.check_socket')
    @patch('time.sleep')
    @patch('jnpr.toby.hldcl.unix.unix.TelnetConn')
    def test_unix_reconnect2(self, patch1, patch2, patch3):
        uobject = MagicMock(spec=UnixHost)
        uobject.prompt = MagicMock(return_value='%')
        uobject.host = 'dummy'
        uobject.user = 'regress'
        uobject.password = 'MaRtInI'
        uobject.connect_mode = 'telnet'
        uobject._kwargs = MagicMock()
        uobject.handle = MagicMock()
        uobject.set_prompt = MagicMock()
        self.assertTrue(UnixHost.reconnect(uobject))

    @patch('logging.error')
    def test_unix_init_execption(self, patch1):
        self.assertRaises(Exception, lambda: Unix(connect_mode='ssh',
                                                  os='unix'))

    @patch('jnpr.toby.hldcl.unix.unix.TelnetConn', return_value=Mockhandle)
    @patch('jnpr.toby.hldcl.unix.unix.UnixHost.set_prompt')
    def test_unix_flavour_exception(self, patch1, patch2):
        os.environ['version'] = 'junos'
        self.assertRaises(Exception, lambda: Unix(host="dummy-freebsd",
                                                  connect_mode='telnet',
                                                  os='unix'))

    @patch('jnpr.toby.hldcl.unix.unix.TelnetConn', side_effect=Exception)
    @patch('jnpr.toby.hldcl.unix.unix.UnixHost.set_prompt')
    def test_unix_flavour_exception2(self, patch1, patch2):
        os.environ['version'] = 'junos'
        self.assertRaises(Exception, lambda: Unix(host="dummy-freebsd",
                                                  connect_mode='telnet',
                                                  os='unix'))

    def test_unix_execute_exception(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.handle = MagicMock()
        uobject.prompt = MagicMock(return_value='%')
        self.assertRaises(Exception, lambda: UnixHost.execute(uobject))

    def test_unix_close_exception(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.disconnect = MagicMock()
        uobject.disconnect.side_effect = Exception
        self.assertRaises(Exception, lambda: UnixHost.close(uobject))

    def test_unix_close2_exception(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.disconnect = MagicMock()

    def test_unix_disconnect_exception(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.connect_mode = 'telnet'
        uobject.handle = MagicMock()
        uobject.handle.close = MagicMock()
        uobject.handle.close.side_effect = Exception
        self.assertRaises(Exception, lambda: UnixHost.disconnect(uobject))

    def test_unix_set_prompt_exception(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=1)
        type(uobject).response = PropertyMock(side_effect=['junos $'])
        self.assertRaises(Exception, lambda: UnixHost.set_prompt(
            uobject, prompt='TOBY'))

    def test_unix_set_prompt_exception2(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=-1)
        self.assertRaises(Exception, lambda: UnixHost.set_prompt(
            uobject, prompt='TOBY'))

    def test_unix_set_prompt_exception3(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock()
        uobject.execute.side_effect = (1, -1)
        type(uobject).response = PropertyMock(side_effect=['csh $'])
        self.assertRaises(Exception, lambda: UnixHost.set_prompt(
            uobject, prompt='TOBY'))

    def test_unix_su_exception(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(return_value=-1)
        uobject.prompt = '$ '
        self.assertRaises(Exception, lambda: UnixHost.su(uobject))

    def test_unix_su_exception2(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock()
        uobject.execute.side_effect = (1, -1)
        uobject.prompt = '$ '
        uobject.get_su_credentials = MagicMock(return_value=('root',
                                                             'Embe1mpls'))
        self.assertRaises(Exception, lambda: UnixHost.su(uobject))

    def test_unix_su_exception3(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock()
        uobject.prompt = '$ '
        uobject.execute.side_effect = Exception
        self.assertRaises(Exception, lambda: UnixHost.su(uobject))

    def test_unix_su_exception4(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.execute = MagicMock(side_effect=(1, 1))
        uobject.prompt = '$ '
        uobject.set_prompt = MagicMock()
        uobject.name = 'foo'
        uobject.channels = [] # needed to raise TobyException
        # Exception
        uobject.shell.return_value.response.return_value.find.return_value = -1
        try:
            UnixHost.su(uobject, password='Embe1mpls')
        except Exception as exp:
            self.assertEqual(exp.args[0], "Not able to switch to root user")

        # return True
        uobject.execute = MagicMock(side_effect=(1, 1))
        uobject.shell.return_value.response.return_value.find.return_value = 1
        uobject.get_su_credentials.return_value = ('root', 'Embe1mpls')
        uobject.shell.return_value.response.return_value = "root"
        self.assertTrue(UnixHost.su(uobject))

        # Exception
        uobject.execute = MagicMock(side_effect=(-1, 1))
        try:
            UnixHost.su(uobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Not able to switch to root user")

        # Exception
        uobject.execute = MagicMock(side_effect=(-1, -1))
        try:
            UnixHost.su(uobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Not able to switch to root user")

    @patch('jnpr.toby.hldcl.unix.unix.check_socket', return_value=0)
    @patch('time.sleep')
    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    def test_unix_reconnect_exception(self, patch1, patch2, patch3):
        uobject = MagicMock(spec=UnixHost)
        uobject.prompt = MagicMock(return_value='%')
        uobject.host = 'dummy'
        uobject.user = 'regress'
        uobject.password = 'MaRtInI'
        uobject.connect_mode = 'ssh'
        uobject.handle = MagicMock()
        uobject.set_prompt = MagicMock()
        self.assertRaises(Exception, lambda: UnixHost.reconnect(uobject))

    @patch('jnpr.toby.hldcl.unix.unix.check_socket', side_effect=Exception)
    @patch('time.sleep')
    @patch('jnpr.toby.hldcl.unix.unix.SshConn')
    def test_unix_reconnect_exception2(self, patch1, patch2, patch3):
        uobject = MagicMock(spec=UnixHost)
        uobject.prompt = MagicMock(return_value='%')
        uobject.host = 'dummy'
        uobject.user = 'regress'
        uobject.password = 'MaRtInI'
        uobject.connect_mode = 'ssh'
        uobject.handle = MagicMock()
        uobject.set_prompt = MagicMock()
        self.assertRaises(Exception, lambda: UnixHost.reconnect(uobject))

    @patch('jnpr.toby.hldcl.unix.unix.check_socket')
    @patch('time.sleep')
    def test_unix_reboot_exception3(self, patch1, patch2):
        uobject = MagicMock(spec=UnixHost)
        uobject.su = MagicMock()
        uobject.execute = MagicMock(return_value=-1)
        uobject.host = 'dummy'
        uobject.connect_mode = 'ssh'
        uobject.handle = MagicMock()
        uobject.reconnect = MagicMock()
        self.assertRaises(Exception, lambda: UnixHost.reboot(uobject))

    @patch('jnpr.toby.hldcl.unix.unix.check_socket', side_effect=[False,
                                                                  False])
    @patch('time.sleep')
    def test_unix_reboot_exception4(self, patch1, patch2):
        uobject = MagicMock(spec=UnixHost)
        uobject.su = MagicMock()
        uobject.execute = MagicMock(return_value=1)
        uobject.host = 'dummy'
        uobject.connect_mode = 'ssh'
        uobject.handle = MagicMock()
        uobject.reconnect = MagicMock()
        self.assertRaises(Exception, lambda: UnixHost.reboot(uobject))

    def test_unix_shell(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.handle = MagicMock()
        uobject.execute = MagicMock(return_value=1)
        uobject.response = 'regress'
        uobject.shell_timeout  = 60
        self.assertIsInstance(UnixHost.shell(uobject, command='ls'), Response)

    def test_unix_shell_exception_no_cmd(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.handle = MagicMock()
        uobject.execute = MagicMock(return_value=1)
        uobject.response = 'regress'
        self.assertRaises(Exception, lambda: UnixHost.shell(uobject))

    def test_unix_shell_exception_no_match(self):
        uobject = MagicMock(spec=UnixHost)
        uobject.handle = MagicMock()
        uobject.execute = MagicMock(return_value=-1)
        self.assertRaises(Exception, lambda: UnixHost.shell(uobject,
                                                            command='ls'))

    @patch('jnpr.toby.hldcl.unix.unix.UnixHost.__init__', return_value=None)
    def test_freebsd(self, patch1):
        uobject = MagicMock(spec=FreeBSD)
        self.assertIsInstance(FreeBSD(host='host', os='UNIX', user='regress', password='MaRtIni',connect_mode='ssh'), FreeBSD)

    def test_freebsd_get_model(self):
        uobject = MagicMock(spec=FreeBSD)

        uobject.shell.return_value.response.return_value = " test"
        self.assertIsNone(FreeBSD.get_model(uobject))

        uobject.shell.return_value.response.return_value = "mx480"
        self.assertEqual(FreeBSD.get_model(uobject), "mx480")

        uobject.model = "mx2020"
        self.assertEqual(FreeBSD.get_model(uobject), "mx2020")

    def test_freebsd_get_model_failure(self):
        uobject = MagicMock(spec=FreeBSD)
        uobject.name = 'foo'
        uobject.channels = []

        # Exception
        uobject.shell.side_effect = Exception

        try:
            FreeBSD.get_model(uobject)
        except Exception as exp:
            self.assertEqual(exp.args[0], "Could not get model info") # Correct one

    @patch('jnpr.toby.hldcl.unix.unix.UnixHost.__init__', return_value=None)
    def test_centos(self, patch1):
        uobject = MagicMock(spec=CentOS)
        self.assertIsInstance(CentOS(host='host', os='UNIX', user='regress', password='MaRtIni', connect_mode='ssh'), CentOS)

if __name__ == '__main__':
    unittest.main()
