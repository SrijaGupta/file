import os
import unittest
import logging
from mock import MagicMock
from mock import patch
import builtins
from time import sleep
from jnpr.toby.hldcl.cisco.cisco import IOS
from jnpr.toby.hldcl.cisco.cisco import Cisco
from jnpr.toby.utils.response import Response
from jnpr.toby.hldcl.cisco.utils import ping, get_image


class TestCiscoModule(unittest.TestCase):
    
    @patch('jnpr.toby.hldcl.cisco.cisco.IOS.__init__')
    def test_class_cisco(self, patch_ios):
        patch_ios.return_value = None
        builtins.t = MagicMock()
        device = Cisco(host='10.20.15.201')
        device.log = MagicMock()
        device.connect = MagicMock()
    
    @patch('jnpr.toby.hldcl.cisco.cisco.Cisco.__init__')
    @patch('jnpr.toby.hldcl.host.Host.__init__')
    @patch('jnpr.toby.hldcl.cisco.cisco.IOS.connect')
    def test_class_ios(self, patch_connect, patch_host, patch_cisco):
        patch_cisco.return_value = None
        patch_host.return_value = None
        patch_connect.return_value = None
        IOS.log = MagicMock()
        ######################################################################
        logging.info("Test case 1: connect mode is not console")
        IOS(host='10.20.15.201')
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 1: host is not defined")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, IOS())
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 1: connect mode is console")
        IOS(host='10.20.15.201', connect_mode='console')
        logging.info("\tPassed")

    def test_connect(self):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.host = 'test'
        device._connect = MagicMock(return_value=True)
        device.enable = MagicMock(return_value=True)
        device.cli = MagicMock()
        device.log = MagicMock()
        device.cli = MagicMock(return_value=Response(response=''))
        IOS.connect(device)
        device.cli = MagicMock(return_value=Response(response='error'))
        IOS.connect(device)

    @patch('telnetlib.Telnet.close')
    @patch('jnpr.toby.hldcl.connectors.telnetconn.TelnetConn.__init__')
    @patch('jnpr.toby.hldcl.connectors.sshconn.SshConn.__init__')
    def test_connect_(self, patch_sshconn, patch_TelnetConn, patch_telnetlib):
        from jnpr.toby.hldcl.connectors.telnetconn import TelnetConn
        from jnpr.toby.hldcl.connectors.sshconn import SshConn
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ######################################################################
        logging.info("Test case 1: Connect to device by Telnet")
        device._kwargs = {}
        device.host = 'test'
        device.user = 'regress'
        device.password = 'password'
        device._kwargs['connect_mode'] = 'telnet'
        device._kwargs['port'] = 23
        device._kwargs['console'] = True
        device.log = MagicMock()
        patch_telnetlib.return_value = None
        patch_TelnetConn.return_value = None
        result = IOS._connect(device)
        self.assertIsInstance(result, TelnetConn)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 2: Connect to device by ssh")
        device._kwargs = {}
        device.host = 'test'
        device.user = None
        device.password = None
        device._kwargs['connect_mode'] = 'ssh'
        device._kwargs['console'] = True
        device._kwargs['con-ip'] = '1.1.1.1'
        device.log = MagicMock()
        patch_sshconn.return_value = None
        result = IOS._connect(device)
        self.assertIsInstance(result, SshConn)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3: Connect to device by console")
        device._kwargs = {}
        device.host = 'test'
        device._kwargs['connect_mode'] = 'console'
        device.log = MagicMock()
        result = IOS._connect(device)
        self.assertEqual(result, None)
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 4: Connect to device with Unknown connection mode")
        device._kwargs = {}
        device.host = 'test'
        device._kwargs['connect_mode'] = 'abc'
        device.log = MagicMock()
        result = IOS._connect(device)
        self.assertEqual(result, None)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 5: Connect to device by ssh")
        device._kwargs = {}
        device.host = 'test'
        device.user = None
        device.password = None
        device._kwargs['connect_mode'] = 'ssh'
        device._kwargs['console'] = False
        device.log = MagicMock()
        patch_sshconn.return_value = None
        result = IOS._connect(device)
        self.assertIsInstance(result, SshConn)
        logging.info("\tPassed")

    def test_switch_mode(self):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.enable = MagicMock(return_value=True)
        device.detect_mode = MagicMock(return_value=True)
        device._switch_mode = MagicMock(return_value=True)
        device.execute = MagicMock(return_value=True)
        ######################################################################
        logging.info(
            "Test case 1: switch mode from user mode to privilege mode")
        device.prompt = '>'
        device.mode = 'user'
        result = IOS._switch_mode(device, mode='privileged')
        self.assertEqual(result, True, 'Should be True')
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 2: switch mode from privilege mode to user mode")
        device.prompt = '#'
        device.mode = 'privileged'
        result = IOS._switch_mode(device, mode='user')
        self.assertEqual(result, True, 'Should be True')
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 3: switch mode from config mode to privileged mode")
        device.prompt = '#'
        device.mode = 'config'
        result = IOS._switch_mode(device, mode='privileged')
        self.assertEqual(result, True, 'Should be True')
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 4: switch mode from user mode to config mode")
        device.prompt = '>'
        device.mode = 'user'
        result = IOS._switch_mode(device, mode='config')
        self.assertEqual(result, True, 'Should be True')
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 5: switch mode to user mode at user mode")
        device.prompt = '>'
        device.mode = 'user'
        result = IOS._switch_mode(device, mode='user')
        self.assertEqual(result, True, 'Should be True')
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 6: Get exception when switching mode")
        device.prompt = '#'
        device.mode = 'config'
        device.execute = MagicMock(side_effect=Exception('error'))
        with self.assertRaises(Exception) as context:
            result = IOS._switch_mode(device, mode='privileged')
        self.assertRaises(Exception, result)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 7: Wrong mode")
        device.prompt = '#'
        device.mode = 'privileged'
        result = IOS._switch_mode(device, mode='abc')
        self.assertEqual(result, True, 'Should be True')
        logging.info("\tPassed")

    def test_execute(self):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ######################################################################
        logging.info("Test case 1: execute command successfully")
        device.prompt = '#'
        device.channel = MagicMock()
        device.channel.execute = MagicMock(return_value='abc')
        device.response = 'abc'
        result = IOS.execute(device, command='interface f0/0')
        self.assertEqual(result, 'abc', 'Should be a response')
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 2: execute command unsuccessfully")
        device.channel = MagicMock()
        device.channel.execute = MagicMock(return_value=-1)
        with self.assertRaises(Exception) as context:
            result = IOS.execute(device, command='interface f0/0', pattern='#')
        self.assertRaises(Exception, result)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3: execute without command")
        device.channel = MagicMock()
        result = IOS.execute(device, pattern='#')
        self.assertEqual(result, 'abc', 'Should be False')
        logging.info("\tPassed")

    def test_cli(self):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device._switch_mode = MagicMock(return_value=True)
        device.execute = MagicMock(return_value=True)
        device.prompt = '#'
        ######################################################################
        logging.info("Test case 1: execute cli successfully")
        result = IOS.cli(device, command='show version', pattern='#')
        self.assertIsInstance(result, Response, 'Should be string')
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 2: Exception when executing cli without command")
        with self.assertRaises(Exception) as context:
            result = IOS.cli(device, command=None, pattern='#')
        self.assertRaises(Exception, result)
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3: execute cli unsuccessfully")
        with self.assertRaises(Exception) as context:
            result = IOS.cli(device, command=111)
        self.assertRaises(Exception, result)
        logging.info("\tPassed")

    def test_config(self):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device._switch_mode = MagicMock(return_value=True)
        device.execute = MagicMock(return_value=True)
        device.detect_mode = MagicMock(return_value=True)
        device.prompt = '#'
        ######################################################################
        logging.info("Test case 1: execute config with command_list is None")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, IOS.config(
                device, command_list=None, pattern='#'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 2: execute config with command_list is not a list")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, IOS.config(
                device, command_list=111, pattern='#'))
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3: execute config successfully")
        result = IOS.config(device, command_list=[
                            'interface f0/1', 'no shut'], pattern='#')
        self.assertIsInstance(result, Response, 'Should be string')
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 2: execute config with element in command_list is not a string")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, IOS.config(
                device, command_list=[111, 'abc']))
        logging.info("\tPassed")

    def test_enable(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.channel = MagicMock()
        device.channel.execute = MagicMock()
        ######################################################################
        logging.info("Test case 1: Enable the IOS device by passing password")
        result = IOS.enable(device, enable_password='test')
        self.assertNotEqual(result, None, "Result should be none")
        logging.info("\tPassed")
        #####################################################################
        logging.info("Test case 2: Enable the IOS device without password")
        device.enable_password = 'test'
        result = IOS.enable(device)
        self.assertNotEqual(result, None, "Result should be none")
        logging.info("\tPassed")

    @patch('time.sleep')
    def test_reconnect(self, patch_sleep):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.channel = MagicMock()
        device.channel.execute = MagicMock()
        #############################################################
        logging.info("Test case 1:With reconnect True")
        device.disconnect = MagicMock(return_value=True)
        device.connect = MagicMock(
            side_effect=[Exception('Error'), True])
        result = IOS.reconnect(device)
        self.assertTrue(result, "Result should be true")
        logging.info("\tPassed")
        #############################################################
        logging.info("Test case 2:With reconnect fails")
        device.disconnect = MagicMock(return_value=True)
        device.connect = MagicMock(return_value=Exception('Error'))
        result = IOS.reconnect(device, timeout=0)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

    def test_disconnect(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.channel = MagicMock()
        ###################################################################
        logging.info("Test case 1:with disconnect success ")
        device.connected = True
        result = IOS.disconnect(device)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ################################################################
        logging.info("Test case 2:with self.connected fail ")
        device.connected = False
        device.host = 'test'
        result = IOS.disconnect(device)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3:with disconnect fail ")
        device.connected = True
        device.channel = MagicMock()
        device.channel.close = MagicMock(side_effect=Exception('Error'))
        result = IOS.disconnect(device)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")
        #######################################################################

    def test_close(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.channel = MagicMock()
        ###################################################################
        logging.info("Test case 1:with close success ")
        device.connected = True
        device.channel.close = MagicMock(return_value=True)
        result = IOS.close(device)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ################################################################
        logging.info("Test case 2:with close fail ")
        device.channel = MagicMock()
        device.channel.close = MagicMock(side_effect=Exception('Error'))
        result = IOS.close(device)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")
        #######################################################################
        logging.info("Test case 3:with close success")
        device.connected = False
        device.channel.close = MagicMock(return_value=True)
        result = IOS.close(device)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ################################################################

    @patch('time.sleep')
    def test_reboot(self, sleep_patch):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        sleep_patch = MagicMock()
        device.save_config = MagicMock()
        ###################################################################
        logging.info("Test case 1: Cannot save config. Reboot unsuccessfully")
        device.cli = MagicMock(return_value=Response(response='yes/no'))
        device.execute = MagicMock()
        result = IOS.reboot(device)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: Reboot successfully")
        device.cli = MagicMock(return_value=Response(response='confirm'))
        device.execute = MagicMock()
        device.reconnect = MagicMock(return_value=True)
        result = IOS.reboot(device)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: Reboot unsuccessfully")
        device.cli = MagicMock(return_value=Response(response='confirm'))
        device.execute = MagicMock()
        device.reconnect = MagicMock(return_value=False)
        result = IOS.reboot(device)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

    def test_save_config(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: save config successfully")
        device.cli = MagicMock(return_value=Response(response=''))
        device.execute = MagicMock(
            side_effect=['want to overwrite?', '[confirm]', '[OK]'])
        result = IOS.save_config(device, file='start')
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: Invalid file. save config unsuccessfully")
        device.cli = MagicMock(return_value=Response(response=''))
        device.execute = MagicMock(
            side_effect=['want to overwrite?', '[confirm]', '[OK]'])
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, IOS.save_config(device))
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 3: save config successfully")
        device.cli = MagicMock(return_value=Response(response=''))
        device.execute = MagicMock(side_effect=['', '', ''])
        result = IOS.save_config(device, file='start')
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

    def test_get_version(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: get_version successfully")
        device.cli = MagicMock(return_value=Response(response=""""ROM: ROMMON Emulation Microcode
        ROM: 3700 Software (C3745-ADVENTERPRISEK9_SNA-M), Version 12.4(25d), RELEASE SOFTWARE (fc1)
        R1 uptime is 3 hours, 53 minutes
        System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
        System image file is "tftp://255.255.255.255/unknown"
        This product contains cryptographic features and is subject to United"""))
        expected_result = '12.4(25d)'
        result = IOS.get_version(device)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: get_version unsuccessfully")
        device.cli = MagicMock(return_value=Response(response=""""ROM: ROMMON Emulation Microcode
        ROM: 3700 Software (C3745-ADVENTERPRISEK9_SNA-M),
        R1 uptime is 3 hours, 53 minutes
        System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
        System image file is "tftp://255.255.255.255/unknown"
        This product contains cryptographic features and is subject to United"""))
        expected_result = ''
        result = IOS.get_version(device)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")

    @patch('glob.glob')
    @patch('os.path.exists')
    @patch('os.system')
    def test_clean_config(self, system_mock, exists_mock, glob_mock):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.load_config = MagicMock(return_value=True)
        device.detect_mode = MagicMock(return_value=True)
        device.prompt = '#'
        ######################################################################
        logging.info("Test case 1: config_file in flash:")
        device.cli = MagicMock(
            side_effect=[Response(response=''),
                         Response(response='\r\nbaseline-config.conf\r\n')])
        self.assertEqual(True, IOS.clean_config(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 2: config_file in slot0:")
        device.cli = MagicMock(
            side_effect=[Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response='\r\nbaseline-config.conf\r\n')])
        self.assertEqual(True, IOS.clean_config(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 3: config_file in slot1:")
        device.cli = MagicMock(
            side_effect=[Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response='\r\nbaseline-config.conf\r\n')])
        self.assertEqual(True, IOS.clean_config(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 4: config_file in flash:")
        device._kwargs = {'host': 'test-con'}
        device.cli = MagicMock(
            side_effect=[Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response='\r\ntest-config.conf\r\n')])
        device.execute = MagicMock(return_value='')
        glob_mock.return_value = ['test1', 'test2']
        exists_mock.return_value = True
        system_mock.return_value = True
        self.assertEqual(True, IOS.clean_config(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 5: item in labs does not exist")
        device._kwargs = {'host': 'test-con'}
        device.cli = MagicMock(
            side_effect=[Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response='\r\ntest-config.conf\r\n')])
        device.execute = MagicMock(return_value='')
        glob_mock.return_value = ['test1', 'test2']
        exists_mock.return_value = False
        system_mock.return_value = True
        self.assertEqual(False, IOS.clean_config(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 6: config does not exist in /volume/tftpboot/JT")
        device._kwargs = {'host': 'test-con'}
        device.cli = MagicMock(
            side_effect=[Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response='\r\ntest-config.conf\r\n')])
        device.execute = MagicMock(return_value='')
        glob_mock.return_value = ['test1', 'test2']
        exists_mock.side_effect = [True, False]
        system_mock.return_value = True
        self.assertEqual(False, IOS.clean_config(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info("Test case 7: error in copying file")
        device._kwargs = {'host': 'test-con'}
        device.cli = MagicMock(
            side_effect=[Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response=''),
                         Response(response='\r\ntest-config.conf\r\n')])
        device.execute = MagicMock(return_value='error')
        glob_mock.return_value = ['test1', 'test2']
        exists_mock.side_effect = [True, True]
        system_mock.return_value = True
        self.assertEqual(False, IOS.clean_config(device))
        logging.info("\tPassed")

    def test_kill_process(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info(
            "Test case 1: pid is not specified, kill process unsuccessfully")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception, IOS.kill_process(device))
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: kill process unsuccessfully")
        device.cli = MagicMock(return_value=Response(response=''))
        expected_result = False
        result = IOS.kill_process(device, pid=1, signal=9)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 3: kill process successfully")
        device.cli = MagicMock(return_value=Response(response='abc'))
        expected_result = 'abc'
        result = IOS.kill_process(device, pid=1)
        self.assertEqual(result, expected_result,
                         "Result should be %s" % expected_result)
        logging.info("\tPassed")

    @patch('time.sleep')
    @patch('jnpr.toby.hldcl.cisco.cisco.ping')
    def test_switchover(self, ping_mock, sleep_mock):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.load_config = MagicMock(return_value=True)
        device.detect_mode = MagicMock(return_value=True)
        device.prompt = '#'
        sleep_mock = MagicMock()
        ######################################################################
        logging.info("Test case 1: return True")
        device.cli = MagicMock(
            side_effect=[Response(response='success')])
        device.execute = MagicMock(
            side_effect=['abc'])
        ping_mock.return_value = {'reachable': True}
        device._kwargs = {'host': 'test-con'}
        device.reconnect = MagicMock(return_value=True)
        self.assertEqual(True, IOS.switchover(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 2: error in command 'redundancy force-switchover'")
        device.cli = MagicMock(
            return_value=Response(response='error'))
        device.execute = MagicMock(
            side_effect=['abc'])
        ping_mock.return_value = {'reachable': True}
        device._kwargs = {'host': 'test-con'}
        device.reconnect = MagicMock(return_value=True)
        self.assertEqual(False, IOS.switchover(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 3: timeout=0")
        device.cli = MagicMock(
            return_value=Response(response='success'))
        device.execute = MagicMock(
            side_effect=['abc'])
        ping_mock.return_value = {'reachable': True}
        device._kwargs = {'host': 'test-con'}
        device.reconnect = MagicMock(return_value=True)
        self.assertEqual(False, IOS.switchover(device, timeout=-1))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 4: response of ping contains 'reachable'")
        device.cli = MagicMock(
            return_value=Response(response='success'))
        device.execute = MagicMock(
            side_effect=['abc'])
        ping_mock.return_value = {'reachable': False}
        device._kwargs = {'host': 'test-con'}
        device.reconnect = MagicMock(return_value=True)
        self.assertEqual(False, IOS.switchover(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 5: reconnect returns False")
        device.cli = MagicMock(
            return_value=Response(response='success'))
        device.execute = MagicMock(
            side_effect=['abc'])
        ping_mock.return_value = {'reachable': True}
        device._kwargs = {'host': 'test-con'}
        device.reconnect = MagicMock(return_value=False)
        self.assertEqual(False, IOS.switchover(device))
        logging.info("\tPassed")

    @patch('jnpr.toby.hldcl.cisco.cisco.get_image')
    def test_upgrade(self, get_image_mock):
        from jnpr.toby.hldcl.cisco.cisco import Cisco, IOS
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        device.prompt = '#'
        ######################################################################
        logging.info("Test case 1: Image is not defined")
        self.assertEqual(False, IOS.upgrade(device))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 2: Input URL with the image that matches current image")
        get_image_mock.return_value = 'tftp://192.168.7.24/cs3-rx.90-1'
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            True,
            IOS.upgrade(device, url='tftp://192.168.7.24/cs3-rx.90-1'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 3: Input the image that matches current image")
        get_image_mock.return_value = 'flash:2:igs-bpx-l'
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            True,
            IOS.upgrade(device, image='igs-bpx-l'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 4: get_image return mismatch value")
        get_image_mock.return_value = 'abc'
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            False,
            IOS.upgrade(device, image='igs-bpx-m'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 5: Input URL with the image " +
            "that does not match current image but upgrade failed")
        get_image_mock.return_value = 'tftp://192.168.7.24/cs3-rx.90-1'
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            False,
            IOS.upgrade(device, url='tftp://192.168.7.24/cs3-rx.90-2'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 6: Input the image that does not match current image " +
            "but upgrade failed")
        get_image_mock.return_value = 'flash:2:igs-bpx-l'
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            False,
            IOS.upgrade(device, image='igs-bpx-m'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 7: Input URL with the image " +
            "that does not match current image and upgrade successful")
        get_image_mock.side_effect = ['tftp://192.168.7.24/cs3-rx.90-1',
                                      'tftp://192.168.7.24/cs3-rx.90-2']
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            True,
            IOS.upgrade(device, url='tftp://192.168.7.24/cs3-rx.90-2'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 8: Input the image that does not match current image " +
            "and upgrade successful")
        get_image_mock.side_effect = ['flash:2:igs-bpx-l', 'flash:2:igs-bpx-m']
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            True,
            IOS.upgrade(device, image='igs-bpx-m'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 9: config function return error")
        get_image_mock.side_effect = ['flash:2:igs-bpx-l', 'flash:2:igs-bpx-m']
        device.config = MagicMock(
            side_effect=[Response(response='error'),
                         Response(response='error')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            False,
            IOS.upgrade(device, image='igs-bpx-m'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 10: Failed to reboot")
        get_image_mock.side_effect = ['flash:2:igs-bpx-l', 'flash:2:igs-bpx-m']
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=False)
        self.assertEqual(
            False,
            IOS.upgrade(device, image='igs-bpx-m'))
        logging.info("\tPassed")
        ######################################################################
        logging.info(
            "Test case 11: get_image returns mismatched value")
        get_image_mock.side_effect = ['flash:2:igs-bpx-l', 'abc']
        device.config = MagicMock(
            side_effect=[Response(response='success'),
                         Response(response='success')])
        device.reboot = MagicMock(return_value=True)
        self.assertEqual(
            False,
            IOS.upgrade(device, image='igs-bpx-m'))
        logging.info("\tPassed")
    
    def test_load_config(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info(
            "Test case 1: local_file is not specified, load config unsuccessfully")
        with self.assertRaises(Exception) as context:
            self.assertRaises(Exception,
                              IOS.load_config(device, option='/verify',
                                              remote_file='flash:xyz.bin'))
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 2: load successfully")
        device.cli = MagicMock(return_value=Response(response='Destination'))
        device.execute = MagicMock(side_effect=['[confirm]', '[OK]'])
        result = IOS.load_config(device, option='/verify',
                                 local_file='flash:abc.bin',
                                 remote_file='flash:xyz.bin')
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 3: load unsuccessfully")
        device.cli = MagicMock(return_value=Response(
            response='error'))
        device.execute = MagicMock(side_effect=['[confirm]', 'error'])
        result = IOS.load_config(device,
                                 local_file='flash:abc.bin',
                                 remote_file='flash:xyz.bin')
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tPassed")
        ###################################################################
        logging.info("Test case 4: load unsuccessfully")
        device.cli = MagicMock(return_value=Response(
            response='Destination filename [abc.txt]?'))
        device.execute = MagicMock(return_value='error')
        result = IOS.load_config(device,
                                 local_file='flash:abc.bin',
                                 remote_file='flash:xyz.bin')
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tPassed")

    def test_get_interface_address(self):
        device = MagicMock(spec=Cisco)
        device.log = MagicMock()
        ###################################################################
        logging.info("Test case 1: Run with ipv4 and valid response")
        res = """
fe01 is up, line protocol is up
  Internet address is 10.6.58.4/24
  Broadcast address is 255.255.255.255
  Address determined by non-volatile memory
  MTU is 1500 bytes
  Helper address is not set
        """
        device.cli = MagicMock(return_value=Response(response=res))
        result = IOS.get_interface_address(
            device, interface="fe01", interface_type=None, family=None)
        self.assertEqual(result, "10.6.58.4/24", "Get ip of intf incorrectly")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 2: Run with ipv6 and link-local")
        res = """
fe01 is up, line protocol is up
  link-local address is 2017::1/64
  Broadcast address is 2017:FF/64
  Address determined by non-volatile memory
  MTU is 1500 bytes
  Helper address is not set
        """
        device.cli = MagicMock(return_value=Response(response=res))
        result = IOS.get_interface_address(
            device, interface="fe01", interface_type="link-local", family=6)
        self.assertEqual(result, "2017::1/64", "Get ip of intf incorrectly")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 3: Run with ipv6 and not link-local")
        res = """
Ethernet0/0 is up, line protocol is up
  IPv6 is enabled, link-local address is FE80::A8BB:CCFF:FE00:6700
  No Virtual link-local address(es):
  Global unicast address(es):
    2001::1, subnet is 2001::/64 [DUP]
    2001::A8BB:CCFF:FE00:6700, subnet is 2001::/64 [EUI]
    2001:100::1, subnet is 2001:100::/64
  Joined group address(es):
    FF02::1
    FF02::2
    FF02::1:FF00:1
    FF02::1:FF00:6700
        """
        device.cli = MagicMock(return_value=Response(response=res))
        result = IOS.get_interface_address(
            device, interface="fe01", interface_type="global", family=6)
        self.assertEqual(result, "2001::1/64", "Get ip of intf incorrectly")
        logging.info("\tPassed")

        res = """
Ethernet0/0 is up, line protocol is up
  IPv6 is enabled, link-local address is FE80::A8BB:CCFF:FE00:6700
  No Virtual link-local address(es):
  Global unicast address(es):
  Joined group address(es):
    FF02::1
    FF02::2
    FF02::1:FF00:1
    FF02::1:FF00:6700
        """
        device.cli = MagicMock(return_value=Response(response=res))
        result = IOS.get_interface_address(
            device, interface="fe01", interface_type="global", family=6)
        self.assertEqual(result, "", "Get ip of intf incorrectly")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 4: Run without interface")
        with self.assertRaises(Exception) as context:
            IOS.get_interface_address(device, interface="",
                                      interface_type="link-local", family=6)
            self.assertTrue(
                'Please specify the interface' in str(context.exception))

        ###################################################################
        logging.info("Test case 5: Run with invalid response")
        device.cli = MagicMock(return_value=Response(response="invalid input"))
        with self.assertRaises(Exception) as context:
            IOS.get_interface_address(device, interface="1.2.3.4",
                                      interface_type="link-local", family=6)
            self.assertTrue(
                'Error in executing the show' in str(context.exception))

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name + ".log", level=logging.INFO)
    unittest.main()
