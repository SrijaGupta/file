import unittest
import builtins
from mock import patch, MagicMock, mock_open
from jnpr.toby.bbe.radius.radius import Radius
from io import StringIO
builtins.t = MagicMock()
builtins.t.log = MagicMock()
radius = MagicMock(spec=Radius)

class TestRadius(unittest.TestCase):
    """
    TestRadius class to handle radius.py unit tests
    """
    def test_radius_class(self):

        self.assertEqual(Radius.__init__(radius), None)

    def test_configure_certificate(self):
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.configure_certificates('r0'), False)
        builtins.t.get_handle.return_value = MagicMock()
        self.assertEqual(Radius.configure_certificates('r0'), True)

    @patch('time.sleep')
    def test_restart_radius_server(self, patch_sleep):
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.restart_radius_server('r0', 'start'), False)
        obj1 = MagicMock()
        obj1.shell.return_value.response.return_value = "app\nradiusd 1120\n"
        builtins.t.get_handle.return_value = obj1
        self.assertEqual(Radius.restart_radius_server('r0', 'start'), 'True')
        self.assertEqual(Radius.restart_radius_server('r0', 'restart'), 'True')
        self.assertEqual(Radius.restart_radius_server('r0', 'stop'), 'True')
        obj1.shell.return_value.response.return_value = "app\n"
        self.assertEqual(Radius.restart_radius_server('r0', 'start'), 'True')

    @patch('time.sleep')
    @patch('builtins.open')
    @patch('os.stat')
    @patch('paramiko.SFTPClient.from_transport')
    @patch('paramiko.Transport')
    def test_add_radius_server_user(self, patch_transport, patch_sftp, patch_stat, patch_open, patch_sleep):
        patch_open.return_value.readlines.return_value = ['User-Name = "test"', 'Acct-Session-Id = "15"',
                                                          'Called-Station-Id = "ac15"', 'Calling-Station-Id = "cda15"']
        obj1 = MagicMock()
        obj1.st_size = 0
        patch_stat.return_value = obj1
        args = ['10.0.0.1', 'test', 'pwd', 'ud', '/etc', 'other', '', '/tmp']
        self.assertEqual(Radius.add_radius_server_user(*args), False)
        obj1.st_size = 1
        self.assertEqual(Radius.add_radius_server_user(*args), 'False')
        args[5] = 'user'
        args[6] = 'no'
        self.assertEqual(Radius.add_radius_server_user(*args), 'True')
        args[5] = 'coa'
        self.assertEqual(Radius.add_radius_server_user(*args), 'True')
        args[6] = 'acct'
        self.assertEqual(Radius.add_radius_server_user(*args), 'True')
        args[6] = 'calling'
        self.assertEqual(Radius.add_radius_server_user(*args), 'True')
        args[6] = 'acct_calling'
        self.assertEqual(Radius.add_radius_server_user(*args), 'True')

    @patch('time.sleep')
    @patch('builtins.enumerate')
    @patch('builtins.open')
    @patch('os.stat')
    @patch('paramiko.SFTPClient.from_transport')
    @patch('paramiko.Transport')
    @patch('paramiko.SSHClient')
    def test_remove_radius_server_user(self, patch_ssh, patch_transport, patch_sftp, patch_stat, patch_open, patch_enum,
                                       patch_sleep):
        args = ['10.0.0.1', 'root', 'pwd', 'test', '/etc', 'user', '1']
        self.assertEqual(Radius.remove_radius_server_user(*args), True)
        patch_enum.return_value = [(1, 'test'), (2, 'other')]
        self.assertEqual(Radius.remove_radius_server_user(*args), 'True')
        args[5] = 'coa'
        patch_ssh.return_value.connect.side_effect = Exception
        self.assertEqual(Radius.remove_radius_server_user(*args), False)
        patch_ssh.return_value.connect.side_effect = None
        patch_ssh.return_value.exec_command.return_value = (MagicMock(), 'b', 'c')
        self.assertEqual(Radius.remove_radius_server_user(*args), True)
        args[5] = 'co'
        self.assertEqual(Radius.remove_radius_server_user(*args), 'False')

    @patch('time.sleep')
    def test_packet_capture_radius(self, patch_sleep):
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.packet_capture_radius('r0', 's1', 'start', '/tmp'), False)
        obj1 = MagicMock()
        obj1.shell.return_value.response.return_value = "app\nradiusd 1120\n"
        builtins.t.get_handle.return_value = obj1
        self.assertEqual(Radius.packet_capture_radius('r0', 's1', 'start', '/tmp'), 'True')
        self.assertEqual(Radius.packet_capture_radius('r0', 's1', 'stop', '/tmp'), 'True')
        self.assertEqual(Radius.packet_capture_radius('r0', 's1', 'non', '/tmp'), 'False')

    @patch('time.sleep')
    @patch('builtins.open')
    @patch('os.stat')
    @patch('paramiko.SFTPClient.from_transport')
    @patch('paramiko.Transport')
    def test_verify_dot1x_msgs(self, patch_transport, patch_sftp, patch_stat, patch_open, patch_sleep):
        """
        this original script has some login problems, needs to be fixed by the author
        :param patch_transport:
        :param patch_sftp:
        :param patch_stat:
        :param patch_open:
        :param patch_sleep:
        :return:
        """
        obj1 = MagicMock()
        obj1.st_size = 0
        patch_stat.return_value = obj1
        args = ['10.0.0.1', 'root', 'pwd', '100.0.0.1', 'ip', ['1','2'], 'sameserver', '/tmp']
        self.assertEqual(Radius.verify_dot1x_msgs(*args), False)
        obj1.st_size = 1
        patch_open.return_value.readlines.return_value = ['Received Access-Request packet from'
                                                          ' host 100.0.0.1 port 1,100']
        self.assertEqual(Radius.verify_dot1x_msgs(*args), True)
        patch_open.return_value.readlines.return_value = ['Received Accounting-Request'
                                                          ' packet from host 100.0.0.1 port 1,100, id=1,1']
        args[6] = 'diffserver'
        self.assertEqual(Radius.verify_dot1x_msgs(*args), True)
        args[6] = 'other'
        self.assertEqual(Radius.verify_dot1x_msgs(*args), False)

    @patch('builtins.open', create=True)
    @patch('paramiko.SFTPClient.from_transport')
    @patch('paramiko.Transport')
    @patch('time.sleep')
    @patch('os.remove')
    @patch('os.path.exists')
    def test_send_coa_dm(self, patch_path, patch_remove, patch_sleep, patch_transport, patch_sftp, patch_open):
        builtins.t.get_handle.return_value = None
        args = ['r0', '10.0.0.9', 'root', 'pwd', '10.0.0.1', 'sec', 'coa', '/tmp', ['1'], 'ipv4', 'yes']
        self.assertEqual(Radius.send_coa_dm(*args), False)
        builtins.t.get_handle.return_value = MagicMock()
        patch_remove.side_effect = Exception
        self.assertEqual(Radius.send_coa_dm(*args), False)
        patch_remove.side_effect = None
        patch_path.return_value = False
        args[9] = 'ipv6'
        args[10] = 'no'
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.send_coa_dm(*args), False)
        builtins.t.get_handle.return_value = MagicMock()
        self.assertEqual(Radius.send_coa_dm(*args), False)
        patch_open.return_value.__enter__.return_value = StringIO('1')
        self.assertEqual(Radius.send_coa_dm(*args), True)
        args[10] = 'yes'
        patch_open.return_value.__enter__.return_value = StringIO('1')
        self.assertEqual(Radius.send_coa_dm(*args), True)
        args[10] = 'oo'
        self.assertEqual(Radius.send_coa_dm(*args), None)
        args[9] = 'ipv6'
        args[10] = 'no'
        args[6] = 'disconnect'
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.send_coa_dm(*args), False)
        builtins.t.get_handle.return_value = MagicMock()
        self.assertEqual(Radius.send_coa_dm(*args), False)
        patch_path.return_value = True
        self.assertEqual(Radius.send_coa_dm(*args), False)
        patch_remove.side_effect = Exception
        self.assertEqual(Radius.send_coa_dm(*args), False)
        patch_remove.side_effect = None
        patch_path.return_value = False
        args[9] = 'ipv4'
        args[10] = 'yes'
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.send_coa_dm(*args), False)
        builtins.t.get_handle.return_value = MagicMock()
        self.assertEqual(Radius.send_coa_dm(*args), False)
        args[10] = 'na'
        self.assertEqual(Radius.send_coa_dm(*args), False)
        patch_open.return_value.__enter__.return_value = StringIO('1')
        self.assertEqual(Radius.send_coa_dm(*args), True)
        args[10] = 'yes'
        patch_open.return_value.__enter__.return_value = StringIO('1')
        self.assertEqual(Radius.send_coa_dm(*args), True)
        args[10] = 'no'
        patch_open.return_value.__enter__.return_value = StringIO('1')
        self.assertEqual(Radius.send_coa_dm(*args), True)
        args[10] = 'oo'
        self.assertEqual(Radius.send_coa_dm(*args), None)

    def test_config_eth_ipaddr(self):
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.config_eth_ipaddr('r0', 'eth0', 'ipv4', '10.0.0.9'), False)
        builtins.t.get_handle.return_value = MagicMock()
        self.assertEqual(Radius.config_eth_ipaddr('r0', 'eth0', 'dual', '10.0.0.9'), False)
        builtins.t.get_handle.return_value.shell.return_value.response.return_value = 'inet6 addr\n'
        self.assertEqual(Radius.config_eth_ipaddr('r0', 'eth0', 'ipv6', '1000::9'), True)
        builtins.t.get_handle.return_value.shell.return_value.response.return_value = 'inet addr\n'
        self.assertEqual(Radius.config_eth_ipaddr('r0', 'eth0', 'ipv6', '1000::9'), True)
        self.assertEqual(Radius.config_eth_ipaddr('r0', 'eth0', 'ipv4', '10.0.0.9'), True)
        builtins.t.get_handle.return_value.shell.return_value.response.return_value = 'inet6 addr\n'
        self.assertEqual(Radius.config_eth_ipaddr('r0', 'eth0', 'ipv4', '10.0.0.9'), True)

    @patch('jnpr.toby.utils.Vars.Vars')
    @patch('builtins.open')
    @patch('os.stat')
    @patch('paramiko.SFTPClient.from_transport')
    @patch('paramiko.Transport')
    def test_get_st_id(self, patch_transport, patch_sftp, patch_stat, patch_open, patch_vars):
        obj1 = MagicMock()
        obj1.st_size = 0
        patch_stat.return_value = obj1
        self.assertEqual(Radius.get_st_id('10.0.0.1', 'root', 'pwd', 'called', '/log'), False)
        obj1.st_size = 1
        patch_open.return_value.readlines.return_value = ['Called-Station-Id = "test"']
        self.assertEqual(Radius.get_st_id('10.0.0.1', 'root', 'pwd', 'called', '/log'), True)
        patch_open.return_value.readlines.return_value = ['Calling-Station-Id = "test"']
        self.assertEqual(Radius.get_st_id('10.0.0.1', 'root', 'pwd', 'calling', '/log'), True)
        patch_open.return_value.readlines.return_value = ['Acct-Session-Id = "test"']
        self.assertEqual(Radius.get_st_id('10.0.0.1', 'root', 'pwd', 'acct', '/log'), True)

    def test_restart_services(self):
        self.assertEqual(Radius.restart_services('r0', 'rad'), True)
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.restart_services('r0', 'rad'), False)
        builtins.t.get_handle.return_value = MagicMock()

    @patch('paramiko.SFTPClient.from_transport')
    @patch('paramiko.Transport')
    @patch('builtins.open')
    def test_add_cp_user(self, patch_open, patch_trans, patch_sftp):
        self.assertEqual(Radius.add_cp_user('10.0.0.9', 'root', 'pwd', '11', '/log', 'user'), True)

    @patch('builtins.open')
    @patch('time.sleep')
    @patch('os.stat')
    @patch('paramiko.SFTPClient.from_transport')
    @patch('paramiko.Transport')
    @patch('os.remove')
    @patch('os.path.exists')
    def test_send_verify_cp(self, patch_path, patch_remove, patch_trans, patch_sftp, patch_stat, patch_slp, patch_open):
        obj1 = MagicMock()
        obj1.st_size = 0
        patch_stat.return_value = obj1
        args = ['r0', '10.0.0.1', 'root', 'pwd', 'no', 'p', 'http://', '123']
        self.assertEqual(Radius.send_verify_cp(*args), False)
        patch_remove.side_effect = Exception
        self.assertEqual(Radius.send_verify_cp(*args), False)
        patch_remove.side_effect = None
        patch_path.return_value = False
        builtins.t.get_handle.return_value = None
        self.assertEqual(Radius.send_verify_cp(*args), False)
        args[4] = 'yes'
        self.assertEqual(Radius.send_verify_cp(*args), False)
        builtins.t.get_handle.return_value = MagicMock()
        self.assertEqual(Radius.send_verify_cp(*args), False)
        obj1.st_size = 1
        patch_open.return_value.__enter__.return_value = StringIO('123')
        self.assertEqual(Radius.send_verify_cp(*args), True)


if __name__ == '__main__':
    unittest.main()        