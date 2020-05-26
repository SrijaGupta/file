import unittest
import builtins
from mock import patch, MagicMock
from jnpr.toby.bbe.radius.freeradius import FreeRadius, BBEConfigError
builtins.t = MagicMock()
builtins.t.log = MagicMock()
builtins.t.get_handle.return_value = MagicMock()
rthandle = builtins.t.get_handle.return_value


class TestFreeRadius(unittest.TestCase):
    """
    TestFreeRadius class to handle freeradius.py unit tests
    """
    def setUp(self):
        self.fr_cls = MagicMock(spec=FreeRadius)

    @patch('re.search')
    @patch('re.match')
    @patch('ldap3.Connection')
    @patch('ldap3.Server')
    def test_freeradius_class(self, patch_server, patch_connection, patch_re, patch_search):
        self.assertIsInstance(FreeRadius.__init__(self.fr_cls, rthandle), object)
        rthandle.get_model.return_value = 'sbr'
        self.assertIsInstance(FreeRadius.__init__(self.fr_cls, rthandle), object)
        patch_connection.side_effect = Exception
        patch_search.return_value = None
        try:
            FreeRadius.__init__(self.fr_cls, rthandle)
        except Exception as err:
            self.assertTrue('failed to start SteelBelt radius before connection' in err.args[0])
        patch_connection.side_effect = None
        patch_search.return_value = MagicMock()

    @patch('re.search')
    def test_start_radius_server(self, patch_re):
        self.fr_cls.device_handle = MagicMock()
        self.fr_cls.sbr = False
        self.assertEqual(FreeRadius.start_radius_server(self.fr_cls), True)
        self.fr_cls.sbr = True
        self.assertEqual(FreeRadius.start_radius_server(self.fr_cls), True)
        try:
            patch_re.return_value = False
            FreeRadius.start_radius_server(self.fr_cls)
        except Exception as err:
            self.assertEqual('failed to start SteelBelt radius', err.args[0])
        self.fr_cls.sbr = False
        obj1 = MagicMock()
        obj2 = MagicMock()
        obj2.resp = ''
        self.fr_cls.device_handle.shell.side_effect = [obj1, obj2, obj1]
        self.fr_cls.device_handle.su.return_value = MagicMock()
        try:
            self.fr_cls.sbin = '/usr/sbin/radiusd'
            self.fr_cls.config_directory = '/usr/etc/freeradius'
            FreeRadius.start_radius_server(self.fr_cls)
        except Exception:
            self.assertRaises(BBEConfigError)
        self.fr_cls.device_handle.shell.side_effect = [obj1, obj2, obj2, obj1]
        self.assertEqual(FreeRadius.start_radius_server(self.fr_cls), True)
        self.fr_cls.device_handle.shell.side_effect = [obj1, obj2, obj2, obj2]
        try:
            FreeRadius.start_radius_server(self.fr_cls)
        except Exception:
            self.assertRaises(BBEConfigError)
        self.fr_cls.device_handle.shell.side_effect = None

    @patch('re.search')
    def test_stop_radius_server(self, patch_re):

        self.fr_cls.device_handle = MagicMock()
        self.fr_cls.sbr = False
        try:
            FreeRadius.stop_radius_server(self.fr_cls)
        except:
            self.assertRaises(BBEConfigError)
        self.fr_cls.sbr = True
        try:
            FreeRadius.stop_radius_server(self.fr_cls)
        except Exception as err :
            self.assertEqual('failed to stop SteelBelt radius', err.args[0])

        patch_re.return_value = False

        self.fr_cls.device_handle.su.return_value = MagicMock()
        self.assertEqual(FreeRadius.stop_radius_server(self.fr_cls), True)
        self.fr_cls.sbr = False
        obj1 = MagicMock()
        obj2 = MagicMock()
        obj2.resp = ''
        self.fr_cls.device_handle.shell.side_effect = [obj1, obj2]
        self.assertEqual(FreeRadius.stop_radius_server(self.fr_cls), True)
        self.fr_cls.device_handle.shell.side_effect = [obj1, obj1, obj1, obj2]
        try:
            FreeRadius.stop_radius_server(self.fr_cls)
        except:
            self.assertRaises(BBEConfigError)

        self.fr_cls.device_handle.shell.side_effect = None

    @patch('re.match')
    def test_restart_radius_server(self, patch_re):

        self.fr_cls.device_handle = MagicMock()
        self.fr_cls.sbr = True
        self.assertEqual(FreeRadius.restart_radius_server(self.fr_cls), True)
        try:
            patch_re.return_value = False
            FreeRadius.restart_radius_server(self.fr_cls)
        except Exception as err :
            self.assertEqual('failed to restart SteelBelt radius', err.args[0])

        self.fr_cls.sbr = False
        self.assertEqual(FreeRadius.restart_radius_server(self.fr_cls), True)

        try:
            self.fr_cls.stop_radius_server.return_value = False
            FreeRadius.restart_radius_server(self.fr_cls)
        except:
            self.assertRaises(BBEConfigError)

        try:
            self.fr_cls.stop_radius_server.return_value = True
            self.fr_cls.start_radius_server.return_value = False
            FreeRadius.restart_radius_server(self.fr_cls)
        except:
            self.assertRaises(BBEConfigError)

    @patch('re.sub')
    def test_add_radius_user(self, patch_re):

        self.fr_cls.device_handle = MagicMock()
        self.fr_cls.conn = MagicMock()
        self.fr_cls.sbr = True
        req_avp = "Service-Type == Framed-User, Auth-Type := Local, User-Password == joshua"
        rep_avp = "Auth-Type = Local, Service-Type = Framed-User, Fall-Through = 1, Jnpr-CoS-Parameter-Type += 'T05 1'," \
                  " Jnpr-CoS-Parameter-Type += 'T04 1'"
        self.assertEqual(FreeRadius.add_radius_user(self.fr_cls, 'test', req_avp, rep_avp, True), True)
        self.fr_cls.conn.add.side_effect = Exception
        self.assertEqual(FreeRadius.add_radius_user(self.fr_cls, 'test', req_avp, rep_avp, True), False)
        self.fr_cls.conn.add.side_effect = None
        try:
            rep_avp = ""
            FreeRadius.add_radius_user(self.fr_cls, 'test', req_avp, rep_avp, True)
        except Exception as err:
            self.assertTrue('the reply attribute' in err.args[0])
        self.fr_cls.sbr = False
        self.fr_cls.config_directory = '/usr/local/etc/raddb'
        self.fr_cls.config_files = {'users': '/usr/etc'}
        rep_avp = "Auth-Type = Local, Service-Type = Framed-User, Fall-Through = 1"
        self.fr_cls.commit_file_on_radius_server.return_value = True
        self.fr_cls.set_radius_users_candidate_config.return_value = True
        self.fr_cls.host = 'hercules'
        self.fr_cls.candidate_configs = {'users': '/etc'}
        self.fr_cls.version = '3'
        self.assertEqual(FreeRadius.add_radius_user(self.fr_cls, 'test', req_avp, rep_avp, True), True)
        self.assertEqual(FreeRadius.add_radius_user(self.fr_cls, 'test', req_avp, rep_avp, False), True)
        self.fr_cls.commit_file_on_radius_server.return_value = False
        self.assertEqual(FreeRadius.add_radius_user(self.fr_cls, 'test', req_avp, rep_avp, True), False)
        self.fr_cls.version = '2'

    def test_commit_radius_user(self):

        self.fr_cls.sbr = True
        self.fr_cls.host = 'hercules'
        self.assertEqual(FreeRadius.commit_radius_user(self.fr_cls), None)
        self.fr_cls.sbr = False
        self.fr_cls.commit_file_on_radius_server.return_value = True
        self.fr_cls.config_directory = '/usr/local/etc/rad'
        self.fr_cls.config_files = {'users': '/usr/etc'}
        self.fr_cls.candidate_configs = {'users': '/etc'}
        self.fr_cls.set_radius_users_candidate_config.return_value = True
        self.assertEqual(FreeRadius.commit_radius_user(self.fr_cls), True)
        self.fr_cls.commit_file_on_radius_server.return_value = False
        self.assertEqual(FreeRadius.commit_radius_user(self.fr_cls), False)


    @patch('jnpr.toby.bbe.radius.freeradius.SshConn')
    def test_delete_radius_user(self, patch_sshconn):

        self.fr_cls.sbr = True
        self.fr_cls.host = 'hercules'
        self.fr_cls.conn = MagicMock()
        self.assertEqual(FreeRadius.delete_radius_user(self.fr_cls, 'test'), True)
        self.fr_cls.conn.delete.side_effect = Exception
        self.assertEqual(FreeRadius.delete_radius_user(self.fr_cls, 'test'), False)
        self.fr_cls.conn.delete.side_effect = None
        self.fr_cls.sbr = False
        self.fr_cls.config_directory = '/usr/local/etc/rad'
        self.fr_cls.config_files = {'users': '/usr/etc'}
        self.assertEqual(FreeRadius.delete_radius_user(self.fr_cls, 'test'), False)

        patch_sshconn.return_value.open_sftp.return_value.open.return_value.__enter__.\
            return_value.readlines.return_value = ['test', '\tat1', 'test2', '\ttest3']
        self.fr_cls.commit_file_on_radius_server.return_value = True
        self.assertEqual(FreeRadius.delete_radius_user(self.fr_cls, 'test'), True)
        self.fr_cls.commit_file_on_radius_server.return_value = False
        patch_sshconn.return_value.open_sftp.return_value.open.return_value.__enter__.\
            return_value.readlines.return_value = ['test', '\tat1', 'test2', '\ttest3']
        self.assertEqual(FreeRadius.delete_radius_user(self.fr_cls, 'test'), False)

    def test_add_radius_client(self):

        self.fr_cls.sbr = True
        self.fr_cls.host = 'hercules'
        self.fr_cls.conn = MagicMock()
        self.assertEqual(FreeRadius.add_radius_client(self.fr_cls, 'hercules', 'joshua', 'hercules'), True)
        self.assertEqual(FreeRadius.add_radius_client(self.fr_cls, 'hercules', 'joshua', 'hercules', True, True), True)
        self.fr_cls.conn.add.side_effect = Exception
        try:
            FreeRadius.add_radius_client(self.fr_cls, 'hercules', 'joshua', 'hercules', True, True)
        except Exception as err:
            self.assertTrue('failed to add radius client' in err.args[0])
        self.fr_cls.conn.add.side_effect = None
        self.fr_cls.sbr = False
        self.fr_cls.config_directory = '/usr/local/etc/rad'
        self.fr_cls.config_files = {'clients': '/usr/etc'}
        self.assertEqual(FreeRadius.add_radius_client(self.fr_cls, 'a', 'b', 'c', False, False, nastype='a',
                                                      password='p', login='l'), True)
        self.fr_cls.commit_file_on_radius_server.return_value = True
        self.assertEqual(FreeRadius.add_radius_client(self.fr_cls, 'a', 'b', 'c', True), True)
        self.fr_cls.commit_file_on_radius_server.return_value = False
        self.assertEqual(FreeRadius.add_radius_client(self.fr_cls, 'a', 'b', 'c', True), False)

    def test_modify_radius_auth(self):

        self.fr_cls.sbr = True
        self.fr_cls.host = 'hercules'
        self.fr_cls.conn = MagicMock()
        self.assertEqual(FreeRadius.modify_radius_auth(self.fr_cls, 'Native'), None)

    @patch('jnpr.toby.bbe.radius.freeradius.SshConn')
    def test_delete_radius_client(self, patch_sshconn):

        self.fr_cls.sbr = True
        self.fr_cls.conn = MagicMock()
        self.assertEqual(FreeRadius.delete_radius_client(self.fr_cls, 'hercules'), True)
        self.fr_cls.conn.delete.return_value = False
        self.assertEqual(FreeRadius.delete_radius_client(self.fr_cls, 'hercules'), False)
        self.fr_cls.sbr = False
        self.fr_cls.host = 'test'
        self.fr_cls.config_directory = '/usr/local/etc/rad'
        self.fr_cls.config_files = {'users': '/usr/etc', 'clients': '/clients'}
        self.assertEqual(FreeRadius.delete_radius_client(self.fr_cls, 'test'), False)

        patch_sshconn.return_value.open_sftp.return_value.open.return_value.__enter__.\
            return_value.readlines.return_value = ['test', '\tat1', 'test2', '\ttest3']
        self.fr_cls.commit_file_on_radius_server.return_value = True
        self.assertEqual(FreeRadius.delete_radius_client(self.fr_cls, 'test'), True)
        patch_sshconn.return_value.open_sftp.return_value.open.return_value.__enter__.\
            return_value.readlines.return_value = ['test', '\tat1', 'test2', '\ttest3']
        self.fr_cls.commit_file_on_radius_server.return_value = False
        self.assertEqual(FreeRadius.delete_radius_client(self.fr_cls, 'test'), False)

    @patch('jnpr.toby.bbe.radius.freeradius.SshConn')
    def test_commit_file_on_radius_server(self, patch_sshconn):

        self.fr_cls.sbr = True
        self.assertEqual(FreeRadius.commit_file_on_radius_server(self.fr_cls, 'a', 'b', True, 'd'), None)
        self.fr_cls.sbr = False
        self.fr_cls.host = None
        try:
            FreeRadius.commit_file_on_radius_server(self.fr_cls, 'a', 'b', True, 'd')
        except:
            self.assertRaises(BBEConfigError)
        self.fr_cls.host = 'test'
        self.assertEqual(FreeRadius.commit_file_on_radius_server(self.fr_cls, 'a', 'b', True, 'd'), False)
        help_tool = MagicMock()
        help_tool.read.return_value.decode.return_value = 'boo'
        patch_sshconn.return_value.open_sftp.return_value.open.return_value = help_tool
        self.assertEqual(FreeRadius.commit_file_on_radius_server(self.fr_cls, 'a', 'b', False, 'd'), True)

    @patch('os.getenv', return_value='test')
    @patch('jnpr.toby.bbe.radius.freeradius.SshConn')
    def test_set_file_watermark(self, patch_sshconn, patch_osenv):

        self.fr_cls.host = 'test'
        help_tool = MagicMock()
        patch_sshconn.return_value.open_sftp.return_value.open.return_value = help_tool
        self.assertEqual(FreeRadius.set_file_watermark(self.fr_cls, '/etc/str'), True)

    def test_get_radius_filename(self):
        self.fr_cls.config_files = {'users': '/usr/etc', 'clients': '/clients', 'server': '/server'}
        self.assertEqual(FreeRadius.get_radius_clients_configuration_filename(self.fr_cls), '/clients')
        self.assertEqual(FreeRadius.get_radius_configuration_filename(self.fr_cls), '/server')
        self.assertEqual(FreeRadius.get_radius_users_configuration_filename(self.fr_cls), '/usr/etc')

    def test_radius_candidate(self):
        self.fr_cls.candidate_configs = {'users': 'z', 'clients': 'a', 'server': 's'}
        self.assertEqual(FreeRadius.get_radius_clients_candidate_config(self.fr_cls), 'a')
        self.assertEqual(FreeRadius.get_radius_users_candidate_config(self.fr_cls), 'z')
        self.assertEqual(FreeRadius.get_radius_candidate_config(self.fr_cls), 's')
        self.assertEqual(FreeRadius.set_radius_candidate_config(self.fr_cls, 'test', True), True)
        self.assertEqual(FreeRadius.set_radius_candidate_config(self.fr_cls, 'test', False), True)
        self.assertEqual(FreeRadius.set_radius_clients_candidate_config(self.fr_cls, 'c', True), True)
        self.assertEqual(FreeRadius.set_radius_clients_candidate_config(self.fr_cls, 'c', False), True)
        self.assertEqual(FreeRadius.set_radius_users_candidate_config(self.fr_cls, 'u', True), True)
        self.assertEqual(FreeRadius.set_radius_users_candidate_config(self.fr_cls, 'u', False), True)

if __name__ == '__main__':
    unittest.main()