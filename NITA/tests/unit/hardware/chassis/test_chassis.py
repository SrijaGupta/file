import unittest
import logging
import sys,os,logging
from jnpr.toby.hldcl.juniper.junos import Juniper
from jnpr.toby.hardware.chassis import chassis
from mock import patch, MagicMock, Mock
from jnpr.toby.hldcl.unix.unix import Unix
from jnpr.toby.hldcl.unix.unix import FreeBSD
from jnpr.toby.utils.response import Response
from lxml import etree
import time
import ast,jxmlease
from jnpr.toby.hardware.chassis.chassis import __cli_get_firmware as cli_get_firmware
from jnpr.toby.hardware.chassis.chassis import __cli_get_environment as cli_get_environment
from jnpr.toby.hardware.chassis.chassis import __check_fru1_led as check_fru1_led
from jnpr.toby.hardware.chassis.chassis import __get_chassis_inventory as get_chassis_inventory
from jnpr.toby.hardware.chassis.chassis import __get_uptime as get_uptime
from jnpr.toby.hardware.chassis.chassis import __get_psd as get_psd
from jnpr.toby.hardware.chassis.chassis import __get_cid as get_cid
from jnpr.toby.hardware.chassis.chassis import __error_arg_msg as error_arg_msg
from jnpr.toby.hardware.chassis.chassis import __sleep as sleep
from jnpr.toby.hardware.chassis.chassis import __check_fru2_led as check_fru2_led
from jnpr.toby.hardware.chassis.chassis import __cli_get_mac as _cli_get_mac
from jnpr.toby.hardware.chassis.chassis import __cli_get_alarm as _cli_get_alarm
from jnpr.toby.hardware.chassis.chassis import __cli_get_craft as _cli_get_craft
from jnpr.toby.hardware.chassis.chassis import __cli_get_ethernet as _cli_get_ethernet
from jnpr.toby.hardware.chassis.chassis import __cli_get_fru as _cli_get_fru
from jnpr.toby.hardware.chassis.chassis import __check_dynamic_db as check_dynamic_db
from jnpr.toby.hardware.chassis.chassis import __check_re_led as check_re_led
from jnpr.toby.hardware.chassis.chassis import __check_sfm_led as check_sfm_led
from jnpr.toby.hardware.chassis.chassis import __chop as chop
from jnpr.toby.hardware.chassis.chassis import __convert_alarm_display as convert_alarm_display
from jnpr.toby.hardware.chassis.chassis import __convert_db_name as convert_db_name
from jnpr.toby.hardware.chassis.chassis import __convert_name as convert_name
from jnpr.toby.hardware.chassis.chassis import __get_alarm_info as get_alarm_info
from jnpr.toby.hardware.chassis.chassis import __get_alarm_led as get_alarm_led
from jnpr.toby.hardware.chassis.chassis import __get_fru_craft as get_fru_craft
from jnpr.toby.hardware.chassis.chassis import __get_fru_led as get_fru_led
from jnpr.toby.hardware.chassis.chassis import __get_hardware as get_hardware
from jnpr.toby.hardware.chassis.chassis import __get_pic_info as get_pic_info
from jnpr.toby.hardware.chassis.chassis import __get_pic_status as get_pic_status
from jnpr.toby.hardware.chassis.chassis import __timeless as timeless
from jnpr.toby.hardware.chassis.chassis import __cli_get_hardware as cli_get_hardware

class TestChassis(unittest.TestCase):
   
    def setUp(self):
        logging.info("\n##################################################\n")
        logging.info("Initializing mock device handle.............\n")
        self.handle=MagicMock(spec=Juniper)
        self.patcher = patch('jnpr.toby.hardware.chassis.chassis.sleep')                     
        self.sleep_patch = self.patcher.start()
        
    def create_patch(self,name):
        patcher = patch(name)
        thing   = patcher.start()
        self.addCleanup(patcher.stop)
        return thing
    
    def tearDown(self):
        logging.info("Close mock device handle session ...........\n")
        self.handle.close()
        self.sleep_patch.stop()

    @patch('time.sleep')  
    def test_check_chassis_firmware(self,sleep_patch):
 
        logging.info ("Testing check_chassis_firmware..............\n")
        logging.info("Test case 1: Test for without passing the arguments fru and type of chassis")
        result = chassis.check_chassis_firmware(device=self.handle,version='7.0b12')
        self.assertEqual(result,False, 'Missing arguments fru and type')
        logging.info(" Testing with missed parameters has passed...\n")

        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_firmware') as firmware_patch:
            firmware_response = {'fpc 0': 
                                          {'ROM': 'Juniper ROM Monitor Version 6.0b12',
                                            'O/S':'Version 15.1R1.9 by builder on 2015-06-18 06:38:55 UTC'},
                                  'fpc 1': {'ROM': 'Juniper ROM Monitor Version 6.0b12',
                                            'O/S':'Version 15.1R1.9 by builder on 2015-06-18 06:38:55 UTC'}}
            firmware_patch.return_value = firmware_response


            logging.info("Test case 2: Check for chassis firmware version matches")
            firmware_patch.return_value = firmware_response
            result =chassis.check_chassis_firmware(device=self.handle,version='6.0b12',
                                       fru='fpc 0',type_chassis='ROM')
            self.assertEqual(result,True, 'chassis firmware version is not matched')
            logging.info("Chassis firmware version matched and passed...\n")
    
            logging.info("Test case 3: Check for chassis firmware version mismatches and sleep check_interval time")
            firmware_patch.return_value = firmware_response
            result = chassis.check_chassis_firmware(device=self.handle,version='7.0b12',fru='fpc 0',
                                            type_chassis='ROM',check_count=2)
            self.assertEqual(result,False, 'Chassis firmware version matched and \
                                              sleep interval is nottested')
            logging.info("Check chassis firmware version mismatched and passed...\n")
        logging.info("successfully tested check_chassis_firmware........\n")

    
    def test_check_fan_environment(self):
        logging.info("Testing check_fan_environment.....\n")
        logging.info("Test case 1: checks fan env for m5 or m10 model...")
        self.handle.get_model = MagicMock(return_value='m5')
        env = {'left fan 1': {'class': 'Fans',
                                 'comment': 'Spinning at normal speed',
                                  'status': 'OK'},
                   'left fan 2': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                   'left fan 3': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                   'left fan 4': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle, env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 1: checks fan env for m5 or m10 model PASSED...\n")
        
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_environment') as env_patch: 
            logging.info("Test case 2: checks fan env for m7i model...")
            self.handle.get_model = MagicMock(return_value='m7i')
            env_patch.return_value = {'fan 1': {'class': 'Fans',
                                                'comment': 'Spinning at normal speed',
                                                'status': 'OK'},
                                      'fan 2': {'class': 'Fans',
                                                'comment': 'Spinning at normal speed',
                                                'status': 'OK' },
                                      'fan 3': {'class': 'Fans',
                                                'comment': 'Spinning at normal speed',
                                                'status': 'OK' },
                                      'fan 4': {'class': 'Fans',
                                                'comment': 'Spinning at normal speed',
                                                'status': 'OK' }}           
            result = chassis.check_fan_environment(device=self.handle)
            self.assertEqual(result,True, 'Unable to check fan environment')
            logging.info("Test case 2: checks fan env for m7i model PASSED...\n")
 
        logging.info("Test case 3: checks fan env for m10i model ...")
        self.handle.get_model = MagicMock(return_value='m10i')
        env = {'fan tray 0 fan 1': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK'},
               'fan tray 0 fan 2': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray 0 fan 3': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray 0 fan 4': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray 0 fan 5': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK'},
               'fan tray 0 fan 6': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray 0 fan 7': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray 0 fan 8': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray 1 fan 0': 'Absent', 
               'fan tray 1 fan 1': 'Absent',
               'fan tray 1 fan 2': 'Absent',
               'fan tray 1 fan 3': 'Absent',
               'fan tray 1 fan 4': 'Absent',
               'fan tray 1 fan 5': 'Absent',
               'fan tray 1 fan 6': 'Absent',
               'fan tray 1 fan 7': 'Absent',
               'fan tray 1 fan 8': 'Absent'
               }
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 3: checks fan env for m10i model PASSED...\n")

        logging.info("Test case 4: checks fan env for m20 model ...")
        self.handle.get_model = MagicMock(return_value='m20')
        env = {'rear fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'front upper fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 4: checks fan env for m20 model PASSED...\n")

        logging.info("Test case 5: checks fan env for m40 model ...")
        self.handle.get_model = MagicMock(return_value='m40')
        env = {'top impeller': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'bottom impeller': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear left fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear center fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear right fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 5: checks fan env for m40 model PASSED...\n")
        
        logging.info("Test case 6: checks fan env for m40e or m160 model ...")
        self.handle.get_model = MagicMock(return_value='m40e')
        env = {'rear bottom blower': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'rear top blower': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front top blower': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray rear left': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray rear right': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray front left': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'fan tray front right': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 6: checks fan env for m40e or m160 model PASSED...\n")

        logging.info("Test case 7: checks fan env for m120 model ...")
        self.handle.get_model = MagicMock(return_value='m120')
        env = {'front top tray fan 1': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'front top tray fan 2': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front top tray fan 3': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front top tray fan 4': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front top tray fan 5': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front top tray fan 6': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front top tray fan 7': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front top tray fan 8': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'front bottom tray fan 1': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom tray fan 2': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom tray fan 3': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom tray fan 4': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom tray fan 5': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom tray fan 6': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom tray fan 7': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom tray fan 8': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 1': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 2': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 3': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 4': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 5': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 6': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 7': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear top tray fan 8': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 1': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 2': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 3': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 4': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 5': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 6': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 7': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear bottom tray fan 8': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }
                                   }
               
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 7: checks fan env for m120 model PASSED...\n")
     
        logging.info("Test case 8: checks fan env for m320 model ...")
        self.handle.get_model = MagicMock(return_value='m320')
        env = {'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear fan 1 (top)': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear fan 2': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear fan 3': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear fan 4': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear fan 5': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear fan 6': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear fan 7 (bottom)': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 8: checks fan env for m320 model PASSED...\n")   
    
        logging.info("Test case 9: checks fan env for t320 model ...")
        self.handle.get_model = MagicMock(return_value='t320')
        env = {'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left middle fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'bottom left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray top fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray second fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'rear tray middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray fourth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 9: checks fan env for t320 model PASSED...\n")
        
        logging.info("Test case 10: checks fan env for t640/t1600/TX model ...")
        self.handle.get_model = MagicMock(return_value='t1600')
        env = {'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left middle fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'bottom right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray top fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray second fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray third fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray fourth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'rear tray fifth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray sixth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray seventh fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'rear tray bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 10: checks fan env for t640/t1600/TX model PASSED...\n")
        
        with patch('jnpr.toby.hardware.chassis.chassis.check_enhance_fantray') as fantray_patch:
            logging.info("Test case 11: checks fan env for mx960 model ...")
            self.handle.get_model = MagicMock(return_value='mx960')
            fantray_patch.return_value = True
            env = {'top tray fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
               'top tray fan 3': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
               'top tray fan 4': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 5': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 6': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 7': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 8': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 9': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
                'top tray fan 10': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 11': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'top tray fan 12': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 3': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 4': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 5': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 6': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 7': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 8': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 9': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
                'bottom tray fan 10': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 11': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
               'bottom tray fan 12': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'}}
            result = chassis.check_fan_environment(device=self.handle,env=env)
            self.assertEqual(result,True, 'Unable to check fan environment')
            logging.info("Test case 11: checks fan env for mx960 model PASSED...\n")

        logging.info("Test case 12: checks fan env for a40/srx5800 model ...")
        self.handle.get_model = MagicMock(return_value='srx5800')
        env = {'top tray fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'top tray fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
       'top tray fan 3': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top tray fan 4': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'top tray fan 5': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'top tray fan 6': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'bottom tray fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'bottom tray fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'bottom tray fan 3': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'bottom tray fan 4': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'bottom tray fan 5': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'bottom tray fan 6': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'}}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 12: checks fan env for a40/srx5800 model PASSED...\n")
   
        logging.info("Test case 13: checks fan env for mx240 model ...")
        self.handle.get_model = MagicMock(return_value='mx240')
        env = {'front fan': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'middle fan': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
       'rear fan': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 13: checks fan env for mx240 model PASSED...\n")

        logging.info("Test case 14: checks fan env for mx480/a15/a20/srx5600/srx5400 model ...")
        self.handle.get_model = MagicMock(return_value='mx480')
        env = {'top rear fan': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'bottom rear fan': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
       'top middle fan': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom middle fan': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top front fan': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom front fan': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 14: checks fan env for mx480/a15/a20/srx5600/srx5400 model PASSED...\n")
        
        logging.info("Test case 15: checks fan env for a10/srx3600 model ...")
        self.handle.get_model = MagicMock(return_value='a10')
        env = {'fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
       'fan 3': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 4': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 5': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 6': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 7': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 8': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 9': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 10': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 15: checks fan env for a10/srx3600 model PASSED...\n")

        logging.info("Test case 16: checks fan env for a2/srx3400 model ...")
        self.handle.get_model = MagicMock(return_value='a2')
        env = {'fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
       'fan 3': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 4': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 16: checks fan env for a2/srx3400 model PASSED...\n")

        logging.info("Test case 17: checks fan env for ex8208 model ...")
        self.handle.get_model = MagicMock(return_value='ex8208')
        env = {'fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
       'fan 3': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 4': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 5': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 6': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 7': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 8': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 9': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 10': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 11': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'fan 12': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 17: checks fan env for ex8208 model PASSED...\n")

        logging.info("Test case 18: checks fan env for ex8216 model with incorect fan count...")
        self.handle.get_model = MagicMock(return_value='ex8216')
        env = {'top fan 1': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK'},
       'top fan 2': {'class': 'Fans','comment': 'Spinning at normal speed','status': 'OK' },
       'top fan 3': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top fan 4': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top fan 5': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top fan 6': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top fan 7': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top fan 8': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'top fan 9': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom fan 1': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom fan 2': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom fan 3': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom fan 4': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom fan 5': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' },
       'bottom fan 6': {'class': 'Fans',  'comment': 'Spinning at normal speed','status': 'OK' }}
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,True, 'Unable to check fan environment')
        logging.info("Test case 18: checks fan env for ex8216 model PASSED...\n")   

        logging.info("Test case 19: checks fan env for unsupportes model...")
        self.handle.get_model = MagicMock(return_value='ex8000')
        result = chassis.check_fan_environment(device=self.handle,env=env)
        self.assertEqual(result,False, 'Unable to check fan environment')
        logging.info("Test case 19: checks fan env for unsupported  model PASSED...\n")
        logging.info("Successfully tested check fan environment.............\n")


    def test_get_chassis_list(self):
        logging.info("Testing get_chassis_list......\n")
        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots') as slots_patch:
            logging.info("Test case 1: Get chassis list for TX Matrix model...")
            self.handle.get_model = MagicMock(return_value='TX Matrix')
            slots_patch.return_value = ['0','1']
            result = chassis.get_chassis_list(device=self.handle)
            self.assertEqual(type(result),list,'Failed to get chassis list for TX Matrix')
            logging.info("Test case 1: Get chassis list for TX Matrix model passed...\n")
            
            logging.info("Test case 2: Get chassis list for TXP model...")
            slots_patch.return_value = ['0','1','2']
            self.handle.get_model = MagicMock(return_value='TXP')
            result = chassis.get_chassis_list(device=self.handle)
            self.assertEqual(type(result),list,'Failed to get chassis list for TXP')
            logging.info("Test case 2: Get chassis list for TXP model passed...\n")  
   
            logging.info("Test case 3: Get chassis list for mx480 model...")
            slots_patch.return_value = '1'
            self.handle.get_model = MagicMock(return_value='mx480')
            result = chassis.get_chassis_list(device=self.handle)
            self.assertEqual(type(result),list,'Failed to get chassis list for TXP')
            logging.info("Test case 3: Get chassis list for TXP model passed...\n")
        logging.info("successfully tested get_chassis_list........\n")
        del slots_patch
    def test_get_chassis_temperature(self):
        logging.info("Testing get_chassis_temperature......\n")
        logging.info("Test case 1: Checking temperature for fru from chassis environment by passing environment argument ...")
        env = {'fpc1':{'status':'OK','temperature':'35 degrees C/ 95 degrees F'}}
        result = chassis.get_chassis_temperature(device = self.handle,env=env)
        self.assertEqual(type(result),list , 'Failed to get chassis temperature')
        logging.info("Test case 1: Checking temperature for fru from chassis environment PASSED...\n")
    
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_environment') as env_patch:
            env_patch.return_value = {'fpc1':{'status':'OK','temperature':'chassis'},'fpc2':{'status':'OK','temperature':'chassis temperature'}}
            logging.info("Test case 2: Check temperature by passing environment from get chassis environment ...")
            result = chassis.get_chassis_temperature(device = self.handle)
            self.assertEqual(type(result),list , 'Failed to get chassis temperature')
            logging.info("Test case 2: Check temperature by passing environment from get chassis environment PASSED...\n")

        logging.info("Test case 3: Checking incorrect temperature for fru from chassis environment by passing environment argument ...")
        env = {'fpc1':{'status':'OK','temperature':'0 degrees C/ 32 degrees F'}}
        result = chassis.get_chassis_temperature(device = self.handle,env=env)
        self.assertEqual(result,None , 'found correct maximum and minimum temperature from chassis temperature')
        logging.info("Test case 3: Checking incorrect temperature for fru from chassis environment PASSED...\n")       

        logging.info("Test case 4: Checking without temperature from chassis environment by passing environment argument ...")
        env = {'fpc1':{'status':'OK'}}
        result = chassis.get_chassis_temperature(device = self.handle,env=env)
        self.assertEqual(type(result),list , 'found correct maximum and minimum temperature from chassis temperature')
        logging.info("Test case 4: Checking incorrect temperature for fru from chassis environment PASSED...\n")

        logging.info("Test case 5: Checking incorrect temperature for fru from chassis environment by passing environment argument ...")
        env = {'fpc1':{'status':'OK','temperature':'10000 degrees C/ 32000 degrees F'}}
        result = chassis.get_chassis_temperature(device = self.handle,env=env)
        self.assertEqual(type(result),list , 'found correct maximum and minimum temperature from chassis temperature')
        logging.info("Successflly tested get_chassis_temperature......\n") 

       

    def test_get_chassis_memory(self):            
        logging.info("Testing get_chassis_memory......\n")
       
        logging.info("Test case 1: Getting memory of the chassis...\n ")
        self.handle.get_model = MagicMock(return_value='m10i')
        response = " 1733 root        2   8  -88 51096K 16704K nanslp 117:08  0.00% chassisd"
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_memory(device = self.handle)
        self.assertEqual(type(result),list , 'Failed to get chassis memory')
        logging.info("Test case 1: Getting memory of the chassis PASSED...\n ")    

        logging.info("Test case 2: Getting memory of the chassis for mx480 device ")
        self.handle.get_model = MagicMock(return_value='m10i')
        response = "4754 root        2 -26  r26   814M 35064K nanslp  0  35:01   3.08% chassisd"
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_memory(device = self.handle)
        self.assertEqual(type(result),list , 'Failed to get chassis memory')
        logging.info("Test case 2: Getting memory of the chassis for mx480 device PASSED...\n ")   
        
        logging.info("Test case 3: Getting memory of the chassis for mx480 device ")
        self.handle.get_model = MagicMock(return_value='m10i')
        response = "juniper"
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_memory(device = self.handle)
        self.assertEqual(result,None, 'Failed to get chassis memory')
        logging.info("Test case 3: Getting memory of the chassis for mx480 device PASSED...\n ")

        logging.info("Tested successfully get_chassis_memory......")

    def test_get_chassis_pid(self):   
        logging.info("Testing get_chassis_pid......")
 
        logging.info("Test case 1: Getting pid of the chassis ")
        res = "1733  ??  S     45:16.13 /usr/sbin/chassisd -N"
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = chassis.get_chassis_pid(device = self.handle)
        self.assertEqual(type(result),str , 'Failed to get chassis pid')
        logging.info("Test case 1: Getting pid of the chassis PASSED...\n")

        logging.info("Test case 2: Chassis pid is not present... ")
        res = "  ??  S     45:16.13 /usr/sbin/chassisd -N"
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = chassis.get_chassis_pid(device = self.handle)
        self.assertEqual(result,None , 'Chassis pid is present')
        logging.info("Test case 2: Chassis pid is not present PASSED...\n")
        
        logging.info("Successfully tested get_chassis_pid......")

    def test_get_chassis_hostname(self):
        logging.info("Testing get_chassis_hostname......")
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_list') as chas_list_patch:
            logging.info("Test case 1: Get the hostname of the chassis for TX Matrix/TXP with chassis as lcc 0 ")
            self.handle.get_model = MagicMock(return_value='TXP')
            chas_list_patch.return_value = ['sfc 0','lcc 0','lcc 1']
            xml = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/14.2R7/junos">
    <multi-routing-engine-results>
        
        <multi-routing-engine-item>
            
            <re-name>lcc0-re0</re-name>
            
            <software-information>
                <host-name>leonardo</host-name>
                <product-model>t1600</product-model>
                <product-name>t1600</product-name>
                <package-information>
                    <name>junos-version</name>
                    <comment>Junos: 14.2R7.5</comment>
                </package-information>
            </software-information>
        </multi-routing-engine-item>
        
    </multi-routing-engine-results>
    <cli>
        <banner></banner>               
    </cli>
</rpc-reply>
            """
            response = etree.fromstring(xml)
            self.handle.execute_rpc = MagicMock(return_value=Response(response=response))
            result = chassis.get_chassis_hostname(device = self.handle,chassis='lcc 0')
            self.assertEqual(type(result),str , 'Failed to get chassis hostname')
            logging.info("Test case 1: Get the hostname of the chassis for TX Matrix/TXP with chassis as lcc 0 PASSED....\n")
   
            logging.info("Test case 2: Get the hostname of the chassis for TX Matrix/TXP without chassis ")
            self.handle.get_model = MagicMock(return_value='TXP')
            chas_list_patch.return_value = ['sfc 0','lcc 0','lcc 1']
            xml = """
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/14.2R7/junos">
    <multi-routing-engine-results>
        
        <multi-routing-engine-item>
            
            <re-name>sfc0-re0</re-name>
            
            <software-information>
                <host-name>splinter</host-name>
                <product-model>txp</product-model>
                <product-name>txp</product-name>
                <package-information>
                    <name>junos-version</name>
                    <comment>Junos: 14.2R7.5</comment>
                </package-information>
          </software-information>
        </multi-routing-engine-item>
        
        <multi-routing-engine-item>
                <re-name>lcc0-re0</re-name> 
            
            <software-information>
                <host-name>leonardo</host-name>
                <product-model>t1600</product-model>
                <product-name>t1600</product-name>
                <package-information>
                    <name>junos-version</name>
                    <comment>Junos: 14.2R7.5</comment>
                </package-information>
          </software-information>
        </multi-routing-engine-item>
        
        <multi-routing-engine-item>
            
            <re-name>lcc1-re0</re-name>
           <software-information>
                <host-name>raphael</host-name>
                <product-model>t1600</product-model>
                <product-name>t1600</product-name>
                <package-information>
                    <name>junos-version</name>
                    <comment>Junos: 14.2R7.5</comment>
                </package-information>
           </software-information>
        </multi-routing-engine-item>
        
    </multi-routing-engine-results>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
            """
            response = etree.fromstring(xml)
            self.handle.execute_rpc = MagicMock(return_value=Response(response=response))
            result = chassis.get_chassis_hostname(device = self.handle)
            self.assertEqual(type(result),dict, 'Failed to get chassis hostname')
            logging.info("Test case 2: Get the hostname of the chassis for TX Matrix/TXP without chassis PASSED...\n")
            
        logging.info("Test case 3: Get the hostname of the chassis for mx480 device ")
        self.handle.get_model=MagicMock(return_value = 'mx480')
        xml="""
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1R1/junos">
    <software-information>
        <host-name>springpark</host-name>
        <product-model>mx480</product-model>
        <product-name>mx480</product-name>
        <junos-version>17.1R1.7</junos-version>
        <package-information>
            <name>os-kernel</name>
            <comment>JUNOS OS Kernel 64-bit  [20170209.344539_builder_stable_10]</comment>
        </package-information>
        <package-information>
            <name>os-libs</name>
            <comment>JUNOS OS libs [20170209.344539_builder_stable_10]</comment>
        </package-information>
        <package-information>
            <name>os-runtime</name>
            <comment>JUNOS OS runtime [20170209.344539_builder_stable_10]</comment>
        </package-information>
        <package-information>
            <name>zoneinfo</name>
            <comment>JUNOS OS time zone information [20170209.344539_builder_stable_10]</comment>
        </package-information>
        <package-information>
            <name>os-libs-compat32</name>
            <comment>JUNOS OS libs compat32 [20170209.344539_builder_stable_10]</comment>
        </package-information>
        <package-information>           
            <name>os-compat32</name>
            <comment>JUNOS OS 32-bit compatibility [20170209.344539_builder_stable_10]</comment>
        </package-information>
        <package-information>
            <name>py-extensions</name>
            <comment>JUNOS py extensions [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>py-base</name>
            <comment>JUNOS py base [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>os-crypto</name>
            <comment>JUNOS OS crypto [20170209.344539_builder_stable_10]</comment>
        </package-information>
        <package-information>
            <name>netstack</name>
            <comment>JUNOS network stack and utilities [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-modules</name>
            <comment>JUNOS modules [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-modules-platform</name>
            <comment>JUNOS mx modules [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-libs</name>
            <comment>JUNOS libs [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-libs-compat32</name>
            <comment>JUNOS libs compat32 [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-runtime</name>
            <comment>JUNOS runtime [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-libs-compat32-platform</name>
            <comment>JUNOS mx libs compat32 [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-runtime-platform</name>
            <comment>JUNOS mx runtime [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
        <package-information>
            <name>junos-platform</name>
            <comment>JUNOS common platform support [20170223.052849_builder_junos_171_r1]</comment>
        </package-information>
 </software-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply> 
        """
        response = etree.fromstring(xml)
        self.handle.execute_rpc = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_hostname(device = self.handle)
        print (result)
        self.assertEqual(type(result),str, 'Failed to get chassis hostname')
        logging.info("Successfully tested get chassis hostname...........")
    
    def test__cli_get_firmware(self):
        logging.info("Testing __cli_get_firmware.....\n")             
        logging.info("Test case 1: get the chassis firmware information ")
        res="""
Part                     Type       Version
FPC 0                    ROM        Juniper ROM Monitor Version 6.0b12         
                         O/S        Version 15.1R1.9 by builder on 2015-06-18 06:38:55 UTC
FPC 1                    ROM        Juniper ROM Monitor Version 6.0b12         
                         O/S        Version 15.1R1.9 by builder on 2015-06-18 06:38:55 UTC
CFEB 0                  
CFEB 1                   ROM        Juniper ROM Monitor Version 6.0b12         
                         O/S        Version 15.1R1.9 by builder on 2015-06-18 06:38:55 UTC
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_firmware(self.handle)    
        self.assertEqual(type(result), dict, 'Unable to get the chassis firmware information')
        logging.info("Test case 1: get the chassis firmware information PASSED...\n")
        
 
        logging.info("Successfully tested __cli_get_firmware...\n")
   
    def test_cli_get_environment(self):
        logging.info("Testing __cli_get_environment.......")
        logging.info(
            "Test case 1: get the chassis environment information " +
            "without fru and chassis")
        res = """
Class Item                           Status     Measurement
Temp  PEM 0                          OK         40 degrees C / 104 degrees F
      PEM 1                          OK         35 degrees C / 95 degrees F
      PEM 2                          Check
      PEM 3                          Check
      Routing Engine 0               OK         37 degrees C / 98 degrees F
      Routing Engine 0 CPU           OK         36 degrees C / 96 degrees F
      Routing Engine 1               Present
      Routing Engine 1 CPU           Present
      CB 0 Intake                    OK         38 degrees C / 100 degrees F
      CB 0 Exhaust A                 OK         34 degrees C / 93 degrees F
      CB 0 Exhaust B                 OK         42 degrees C / 107 degrees F
      CB 0 ACBC                      OK         42 degrees C / 107 degrees F
      CB 0 XF A                      OK         46 degrees C / 114 degrees F
      CB 0 XF B                      OK         46 degrees C / 114 degrees F
      CB 1 Intake                    OK         34 degrees C / 93 degrees F
      CB 1 Exhaust A                 OK         33 degrees C / 91 degrees F
      CB 1 Exhaust B                 OK         40 degrees C / 104 degrees F
      CB 1 ACBC                      OK         38 degrees C / 100 degrees F
      CB 1 XF A                      OK         44 degrees C / 111 degrees F
      CB 1 XF B                      OK         43 degrees C / 109 degrees F
      FPC 0 Intake                   OK         29 degrees C / 84 degrees F
      FPC 0 Exhaust A                OK         28 degrees C / 82 degrees F
      FPC 0 Exhaust B                OK         30 degrees C / 86 degrees F
      FPC 3 Intake                   OK         29 degrees C / 84 degrees F
      FPC 3 Exhaust A                OK         30 degrees C / 86 degrees F
      FPC 3 Exhaust B                OK         30 degrees C / 86 degrees F
      FPC 4 Intake                   OK         29 degrees C / 84 degrees F
      FPC 4 Exhaust A                OK         29 degrees C / 84 degrees F
      FPC 4 Exhaust B                OK         30 degrees C / 86 degrees F
      FPC 5 Intake                   OK         29 degrees C / 84 degrees F
      FPC 5 Exhaust A                OK         28 degrees C / 82 degrees F
      FPC 5 Exhaust B                OK         29 degrees C / 84 degrees F
Fans  Top Rear Fan                   OK         Spinning at normal speed
      Bottom Rear Fan                OK         Spinning at normal speed
      Top Middle Fan                 OK         Spinning at normal speed
      Bottom Middle Fan              OK         Spinning at normal speed
      Top Front Fan                  OK         Spinning at normal speed
      Bottom Front Fan               OK         Spinning at normal speed
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle)
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 1: get the chassis environment information " +
            "without fru and chassis PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 2: get the chassis environment information by " +
            "passing chassis without fru")
        res = """
Class Item                           Status     Measurement
Temp  PEM 0                          Check      36 degrees C / 96 degrees F
      PEM 1                          Absent
      SCG 0                          OK         38 degrees C / 100 degrees F
      SCG 1                          OK         37 degrees C / 98 degrees F
      Routing Engine 0               OK         38 degrees C / 100 degrees F
      Routing Engine 0 CPU           OK         55 degrees C / 131 degrees F
      Routing Engine 1               OK         37 degrees C / 98 degrees F
      Routing Engine 1 CPU           OK         51 degrees C / 123 degrees F
      CB 0                           OK         38 degrees C / 100 degrees F
      CB 1                           OK         38 degrees C / 100 degrees F
      SIB 0                          OK         49 degrees C / 120 degrees F
      SIB 0 (B)                      OK         40 degrees C / 104 degrees F
      SIB 2                          OK         50 degrees C / 122 degrees F
      SIB 2 (B)                      OK         41 degrees C / 105 degrees F
      SIB 3                          OK         50 degrees C / 122 degrees F
      SIB 3 (B)                      OK         41 degrees C / 105 degrees F
      SIB 4                          OK         52 degrees C / 125 degrees F
      SIB 4 (B)                      OK         42 degrees C / 107 degrees F
      FPC 0 Top                      OK         38 degrees C / 100 degrees F
      FPC 0 Bottom                   OK         39 degrees C / 102 degrees F
      FPC 1 Top                      OK         37 degrees C / 98 degrees F
      FPC 1 Bottom                   OK         37 degrees C / 98 degrees F
      FPC 2 Top                      OK         36 degrees C / 96 degrees F
      FPC 2 Bottom                   OK         37 degrees C / 98 degrees F
      FPC 3 Top                      OK         40 degrees C / 104 degrees F
      FPC 3 Bottom                   OK         39 degrees C / 102 degrees F
      FPC 4 Top                      OK         41 degrees C / 105 degrees F
      FPC 4 Bottom                   OK         39 degrees C / 102 degrees F
      FPC 5 Top                      OK         42 degrees C / 107 degrees F
      FPC 5 Bottom                   OK         41 degrees C / 105 degrees F
      FPC 7 Top                      OK         42 degrees C / 107 degrees F
      FPC 7 Bottom                   OK         43 degrees C / 109 degrees F
      FPM GBUS                       OK         25 degrees C / 77 degrees F
      FPM Display                    OK         28 degrees C / 82 degrees F
Fans  Top Left Front fan             OK         Spinning at high speed
      Top Left Middle fan            OK         Spinning at high speed
      Top Left Rear fan              OK         Spinning at high speed
      Top Right Front fan            OK         Spinning at high speed
      Top Right Middle fan           Check
      Top Right Rear fan             OK         Spinning at high speed
      Bottom Left Front fan          OK         Spinning at high speed
      Bottom Left Middle fan         OK         Spinning at high speed
      Bottom Left Rear fan           OK         Spinning at high speed
      Bottom Right Front fan         OK         Spinning at high speed
      Bottom Right Middle fan        OK         Spinning at high speed
      Bottom Right Rear fan          OK         Spinning at high speed
      Rear Tray Top fan              OK         Spinning at high speed
      Rear Tray Second fan           OK         Spinning at high speed
      Rear Tray Third fan            OK         Spinning at high speed
      Rear Tray Fourth fan           OK         Spinning at high speed
      Rear Tray Fifth fan            OK         Spinning at high speed
      Rear Tray Sixth fan            OK         Spinning at high speed
      Rear Tray Seventh fan          OK         Spinning at high speed
      Rear Tray Bottom fan           OK         Spinning at high speed
Misc  CIP                            OK
      SPMB 0                         OK
      SPMB 1                         OK
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, chassis='lcc 0')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 2: get the chassis environment information by " +
            "passing chassis without fru PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 3: get the chassis environment information by " +
            "passing without chassis and fru, to match psd/rsd")
        self.handle.get_model = MagicMock(return_value='m10i')
        res = """
Class Item                           Status     Measurement
PSD:
      State                          Online     Master
      Temperature                    34         degrees C / 93 degrees F
      CPU Temperature                39         degrees C / 102 degrees F
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 3: get the chassis environment information by " +
            "passing without chassis and fru, to match psd/rsd PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 4: get the chassis environment information by " +
            "passing fru as fpc without chassis")
        self.handle.get_model = MagicMock(return_value='mx480')
        res = """
FPC 0 status:
  State                      Offline
  Temperature Intake         29 degrees C / 84 degrees F
  Temperature Exhaust A      27 degrees C / 80 degrees F
  Temperature Exhaust B      30 degrees C / 86 degrees F
  Power
  I2C Slave Revision         19
FPC 3 status:
  State                      Offline
  Temperature Intake         29 degrees C / 84 degrees F
  Temperature Exhaust A      30 degrees C / 86 degrees F
  Temperature Exhaust B      30 degrees C / 86 degrees F
  Power
  I2C Slave Revision         111
FPC 4 status:
  State                      Offline
  Temperature Intake         29 degrees C / 84 degrees F
  Temperature Exhaust A      29 degrees C / 84 degrees F
  Temperature Exhaust B      30 degrees C / 86 degrees F
  Power
  I2C Slave Revision         111
FPC 5 status:
  State                      Offline
  Temperature Intake         29 degrees C / 84 degrees F
  Temperature Exhaust A      28 degrees C / 82 degrees F
  Temperature Exhaust B      29 degrees C / 84 degrees F
  Power
  I2C Slave Revision         70

        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='fpc')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 4: get the chassis environment information by " +
            "passing fru as fpc without chassis PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 5: get the chassis environment information by " +
            "passing fru as cb without chassis")
        self.handle.get_model = MagicMock(return_value='mx480')
        res = """
CB 0 status:
  State                      Online Master
  Temperature                37 degrees C / 98 degrees F
  Power 1
    1.0 V                       1002 mV
    1.2 V                       1202 mV
    1.5 V                       1508 mV
    1.8 V                       1811 mV
    2.5 V                       2520 mV
    3.3 V                       3312 mV
    5.0 V                       5020 mV
    5.0 V RE                    4975 mV
    12.0 V                     11968 mV
    12.0 V RE                  12026 mV
  Power 2
    4.6 V bias MidPlane         4846 mV
    11.3 V bias PEM            11292 mV
    11.3 V bias FPD            11195 mV
    11.3 V bias POE 0          11292 mV
    11.3 V bias POE 1          11292 mV
  Bus Revision               96
  FPGA Revision              16
  PMBus             Expected   Measured   Measured  Calculated
  device            voltage    voltage    current   power
    XF ASIC A        1033 mV    1033 mV   16500 mA   17044 mW
    XF ASIC B        1034 mV    1034 mV   17000 mA   17578 mW
CB 1 status:
  State                      Online
  Temperature                34 degrees C / 93 degrees F
  Power 1
    1.0 V                       1005 mV
    1.2 V                       1205 mV
    1.5 V                       1504 mV
    1.8 V                       1811 mV
    2.5 V                       2513 mV
    3.3 V                       3319 mV
    5.0 V                       5040 mV
    5.0 V RE                    4995 mV
    12.0 V                     12026 mV
    12.0 V RE                  12026 mV
  Power 2
    4.6 V bias MidPlane         4866 mV
    11.3 V bias PEM            11214 mV
    11.3 V bias FPD            11176 mV
    11.3 V bias POE 0          11253 mV
    11.3 V bias POE 1          11272 mV
  Bus Revision               96
  FPGA Revision              0
  PMBus             Expected   Measured   Measured  Calculated
  device            voltage    voltage    current   power
    XF ASIC A         959 mV     959 mV   16000 mA   15344 mW
    XF ASIC B         958 mV     957 mV   16000 mA   15312 mW
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='cb')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 5: get the chassis environment information by " +
            "passing fru as cb without chassis PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 6: Chassis environment information with " +
            "fru as sfm without chassis")
        res = """
SFM 0 status:
  State                           Online
  temperature              40 degrees C / 104 degrees F
  temperature              44 degrees C / 111 degrees F
  Power:
    1.5 V                    1501 mV
    2.5 V                    2472 mV
    3.3 V                    3293 mV
    5.0 V                    5028 mV
    5.0 V bias               4964 mV
  Power:
    1.5 V                    1501 mV
    2.5 V                    2483 mV
    3.3 V                    3308 mV
    5.0 V                    5035 mV
    5.0 V bias               4981 mV
    8.0 V bias               8239 mV
  CMB Revision                 12
SFM 1 status:
  State                           Online - Standby
  temperature              43 degrees C / 109 degrees F
  temperature              45 degrees C / 113 degrees F
  Power:
    1.5 V                    1503 mV
    2.5 V                    2483 mV
    3.3 V                    3284 mV
    5.0 V                    5045 mV
    5.0 V bias               4993 mV
  Power:
    1.5 V                    1498 mV
    2.5 V                    2472 mV
    3.3 V                    3284 mV
    5.0 V                    5035 mV
    5.0 V bias               4991 mV
    8.0 V bias               8231 mV
  CMB Revision               12

        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru="sfm")
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 6: Chassis environment information with fru as " +
            "sfm without chassis PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 7: Verify 2 PEM with same name in output")
        res = """
Class Item                           Status     Measurement
Temp  PEM 0                          OK         40 degrees C / 104 degrees F
      PEM 0                          OK         35 degrees C / 95 degrees F
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle)
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 7: Verifying 2 PEM with same name in output " +
            "PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 8: Verify without Measurement")
        res = """
Class Item                           Status     Measurement
Temp  PEM 0                          OK                    
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle)
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 8: Verifying without Measurement PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 9: Verify with chassis and fru arguments")
        res = """
FPC 0 status:
  State                      Online
  Temperature Intake         32 degrees C / 89 degrees F             
  Temperature Exhaust A      43 degrees C / 109 degrees F            
  Temperature Exhaust B      55 degrees C / 131 degrees F            
  Temperature LU 0 TSen      49 degrees C / 120 degrees F            
  Temperature LU 0 Chip      55 degrees C / 131 degrees F            
  Temperature LU 1 TSen      49 degrees C / 120 degrees F            
  Temperature LU 1 Chip      50 degrees C / 122 degrees F            
  Temperature LU 2 TSen      49 degrees C / 120 degrees F            
  Temperature LU 2 Chip      55 degrees C / 131 degrees F            
  Temperature LU 3 TSen      49 degrees C / 120 degrees F            
  Temperature LU 3 Chip      63 degrees C / 145 degrees F            
  Temperature XM 0 TSen      49 degrees C / 120 degrees F            
  Temperature XM 0 Chip      56 degrees C / 132 degrees F            
  Temperature XF 0 TSen      49 degrees C / 120 degrees F            
  Temperature XF 0 Chip      70 degrees C / 158 degrees F            
  Temperature PLX Switch TSen49 degrees C / 120 degrees F            
  Temperature PLX Switch Chip47 degrees C / 116 degrees F            
  Power                      
    MPC-BIAS3V3-zl2105          3301 mV
    MPC-VDD3V3-zl6100           3305 mV
    MPC-VDD2V5-zl6100           2505 mV
    MPC-VDD1V8-zl2004           1796 mV
    MPC-AVDD1V0-zl2004           993 mV
    MPC-VDD1V2-zl6100           1203 mV
    MPC-VDD1V5A-zl2004          1494 mV
    MPC-VDD1V5B-zl2004          1498 mV
    MPC-XF_0V9-zl2004            993 mV
    MPC-PCIE_1V0-zl6100         1002 mV
    MPC-LU0_1V0-zl2004           997 mV
    MPC-LU1_1V0-zl2004           998 mV
    MPC-LU2_1V0-zl2004           995 mV
    MPC-LU3_1V0-zl2004           997 mV
    MPC-12VA-BMR453            12003 mV
    MPC-12VB-BMR453            12019 mV
    MPC-PMB_1V1-zl2006          1097 mV
    MPC-PMB_1V2-zl2106          1198 mV
    MPC-XM_0V9-vt273m            915 mV
  I2C Slave Revision         111
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='fpc', chassis='0')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 9: Verifying with chassis and " +
            "fru arguments PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 10: Verify with fru=routing engine")
        res = """
Routing Engine 0 status:
  State                      Online Master
  Temperature                33 degrees C / 91 degrees F             
  CPU Temperature            32 degrees C / 89 degrees F  
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='routing-engine',
                                     chassis='0')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 10: Verifying with fru=routing engine PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 11: Verify with fru=routing engine and model = ptx5000")
        res = """
Routing Engine 0 status:
  State                      Online Master
  Temperature                33 degrees C / 91 degrees F             
  CPU Temperature            32 degrees C / 89 degrees F  
        """
        self.handle.get_model = MagicMock(return_value='ptx5000')
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='routing-engine',
                                     chassis='0')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 11: Verifying with fru=routing engine " +
            "and model = ptx5000 PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 12: Verify with incorrect output for Routing Engine")
        res = """
Route Engine 0 status:
  State                      Online Master
  Temperature                33 degrees C / 91 degrees F             
  CPU Temperature            32 degrees C / 89 degrees F  
        """
        self.handle.get_model = MagicMock(return_value='ptx5000')
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='routing-engine',
                                     chassis='0')
        self.assertEqual(result, None,
                         'Result should be None')
        logging.info(
            "\tTest case 12: Verifying with incorrect output for " +
            "Routing Engine PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 13: Verify with fru = PDU")
        res = """
PDU 0 status:
  State                      Online
  Hours Used                 4281
  Firmware Version (MCU1)    00.02
  Firmware Version (MCU2)    00.02
  Firmware Version (MCU3)    00.02
  Firmware Version (MCU4)    00.02
PDU 0 PSM 0 status:
  State                      Online
  Temperature                OK   32 degrees C / 89 degrees F
  Fans                       OK
  DC Input                   OK
  DC Output                  OK
  Hours Used                 2864
  Firmware Version           00.04
PDU 0 PSM 1 status:
  State                      Online
  Temperature                OK   30 degrees C / 86 degrees F
  Fans                       OK
  DC Input                   OK
  DC Output                  OK
  Hours Used                 3540
  Firmware Version           00.04
PDU 0 PSM 2 status:                     
  State                      Online
  Temperature                OK   29 degrees C / 84 degrees F
  Fans                       OK
  DC Input                   OK
  DC Output                  OK
  Hours Used                 3711
  Firmware Version           00.04
PDU 0 PSM 3 status:
  State                      Online
  Temperature                OK   29 degrees C / 84 degrees F
  Fans                       OK
  DC Input                   OK
  DC Output                  OK
  Hours Used                 4243
  Firmware Version           00.04
        """
        self.handle.get_model = MagicMock(return_value='ptx5000')
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='pdu',
                                     chassis='0')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 13: Verifying with fru = PDU PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 14: Verify with fru = fpm")
        res = """
FPM status:
  State                       Online
  FPM CMB Voltage:
    5.0 V bias           5030 mV
    8.0 V bias           8083 mV
  FPM Display Voltage:
    5.0 V bias           4998 mV
  FPM CMB temperature      34 degrees C / 93 degrees F
  FPM Display temperature  35 degrees C / 95 degrees F
  CMB Revision             12
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='fpm')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 14: Verifying with fru = fpm PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 15: Verify with wrong FRU name in output")
        res = """
ABC FPM status:
  State                       Online
  FPM CMB Voltage:
    5.0 V bias           5030 mV
    8.0 V bias           8083 mV
  FPM Display Voltage:
    5.0 V bias           4998 mV
  FPM CMB temperature      34 degrees C / 93 degrees F
  FPM Display temperature  35 degrees C / 95 degrees F
  CMB Revision             12
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='fpm')
        self.assertEqual(result, None,
                         'Result should be None')
        logging.info(
            "\tTest case 15: Verifying with wrong FRU name in output " +
            "PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 16: Verify with multiple Temperature formats")
        res = """
SCG 0 status:
  State                      Online -  Master clock
  Temperature                Error             
  Power                      
    GROUND                       0 mV
    1.8 V bias                1794 mV
    3.3 V                     3310 mV
    3.3 V bias                3299 mV
    5.0 V                     5040 mV
    5.0 V bias                5003 mV
    5.6 V                     5780 mV
    8.0 V bias                7416 mV
  Bus Revision               40
SCG 1 status:
  State                      Online - Standby  
  ABC temperature            33 degrees C / 91 degrees F             
  Power                      
    GROUND                       0 mV
    1.8 V bias                1794 mV
    3.3 V                     3319 mV
    3.3 V bias                3286 mV
    5.0 V                     5047 mV
    5.0 V bias                5013 mV
    5.6 V                     5758 mV
    8.0 V bias                7347 mV
  Bus Revision               40
SCG 2 status:
  State                      Online - Standby  
  Temperature                Error             
  Power                      
    GROUND                       0 mV
    1.8 V bias                1794 mV
    3.3 V                     3319 mV
    3.3 V bias                3286 mV
    5.0 V                     5047 mV
    5.0 V bias                5013 mV
    5.6 V                     5758 mV
    8.0 V bias                7347 mV
  Bus Revision               40
        """
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='scg')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 16: Verifying with multiple Temperature formats " +
            "PASSED...\n")
        # =================================================================== #
        logging.info(
            "Test case 17: Verify with fru=routing engine and " +
            "model = ptx5000, slot=0")
        res = """
Routing Engine 0 status:
  State                      Online Master
  Temperature                33 degrees C / 91 degrees F             
  CPU Temperature            32 degrees C / 89 degrees F  
        """
        self.handle.get_model = MagicMock(return_value='ptx5000')
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_environment(self.handle, fru='routing-engine',
                                     chassis='0', slot='0')
        self.assertEqual(type(result), dict,
                         'Unable to get chassis environment information')
        logging.info(
            "\tTest case 17: Verifying with fru=routing engine " +
            "and model = ptx5000, slot=0PASSED...\n")
        # =================================================================== #
        logging.info("\tSuccessfully tested __cli_get_environment...\n")



    def test_get_fru_backup(self):
        logging.info("Testing get_fru_backup....")
        logging.info("Testcase 1: Get fru backup status information from the status given...")
        status = [{'state':'OK','status':'Standby'}]
        result = chassis.get_fru_backup(self.handle,chassis='',fru='fpc',status=status)
        self.assertEqual(type(result), int, 'Unable to get fru backup status...')
        logging.info("Testcase 1: Get fru backup status information from the status given PASSED...\n")

        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_status') as status_patch:
            logging.info("Testcase 2: Get fru backup status information from the get_fru_status...")
            status_patch.return_value = [{'state':'backup','status':'Standby'}]
            result = chassis.get_fru_backup(self.handle,chassis='',fru='fpc')
            self.assertEqual(type(result), int, 'Unable to get fru backup status...')
            logging.info("Testcase 2: Get fru backup status information from the get_fru_status PASSED...\n")

        logging.info("Testcase 3: Get fru backup status information from the status given...")
        status = [{'state':'Offline','status':'Offline'}]
        result = chassis.get_fru_backup(self.handle,chassis='',fru='fpc',status=status)
        self.assertEqual(result, None, 'Unable to get fru backup status...')
        logging.info("Testcase 1: Get fru backup status information from the status given PASSED...\n")
        logging.info("Successfully tested get_fru_backup....\n")
    
    def test_check_chassis_coredump(self):
        logging.info("Testcase1: Check chassis coredump files in cli command by passing fru as list and slot values")
        response = """
        /var/crash/*core*: No such file or directory
        /var/tmp/*core*: No such file or directory
        /var/tmp/pics/*core*: No such file or directory
        /var/crash/kernel.*: No such file or directory
        /var/jails/rest-api/tmp/*core*: No such file or directory
        """
        self.handle.cli = MagicMock(return_value=Response(response=response))
        slot = {'fpc':0, 'pic':0}
        fru = ['fpc','pic'] 
        result = chassis.check_chassis_coredump(device = self.handle,fru=fru,slot=slot)
        self.assertEqual(result, True , 'Chassis core files are found')
        logging.info("Testcase1: Check chassis coredump files in cli command by passing fru as list and slot values PASSED...\n") 
     
        logging.info("Testcase2: Check chassis coredump files in vty command by passing fru and slot...")
        response = """
        /var/crash/*core*: No such file or directory
        /var/tmp/*core*: No such file or directory
        /var/tmp/pics/*core*: No such file or directory
        /var/crash/kernel.*: No such file or directory
        /var/jails/rest-api/tmp/*core*: No such file or directory
        """
        self.handle.vty = MagicMock(return_value=Response(response= response))
        slot = {'fpc':[0,1]}
        fru = 'fpc'
        result = chassis.check_chassis_coredump(device = self.handle,fru=fru,slot=slot,cmd_type='vty')
        self.assertEqual(result, True , 'Chassis core files are found')
        logging.info("Testcase2: Check chassis coredump files in vty command by passing fru and slot PASSED...\n")
        
        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots') as slots_patch:
            logging.info("Testcase3: Check chassis coredump files in cli command by patching get_fru_slots")
            response = """
            /var/crash/*core*: No such file or directory
            /var/tmp/*core*: No such file or directory
            /var/tmp/pics/*core*: No such file or directory
            /var/crash/kernel.*: No such file or directory
            /var/jails/rest-api/tmp/*core*: No such file or directory
            """
            self.handle.cli = MagicMock(return_value=Response(response=response))
            fru = ['fpc','pic']
            slots_patch.return_value = {'fpc':[0,1],'pic':0}
            result = chassis.check_chassis_coredump(device = self.handle,fru=fru)
            self.assertEqual(result, True , 'Chassis core files are found')
            logging.info("Testcase3: Check chassis coredump files in cli command by patching get_fru_slots PASSED...\n")
    
        logging.info("Testcase4: No need to check the core dump files for spmb/scb/ssb/feb/cfeb")           
        result = chassis.check_chassis_coredump(device = self.handle,fru='spmb',slot=0)
        self.assertEqual(result, True , 'checking core dump files for unneccessary fru models')
        logging.info("Testcase4: No need to check the core dump files for spmb/scb/ssb/feb/cfeb PASSED...\n")
 
        logging.info("Testcase5: Check for the core dump files present") 
        response = "file name   : core-/var/tmp/core"
        self.handle.cli = MagicMock(return_value=Response(response=response))
        fru = ['fpc','pic']
        slot = {'fpc':[0,1],'pic':0}
        result = chassis.check_chassis_coredump(device = self.handle,fru=fru,slot=slot,check_count =2)
        self.assertEqual(result, False , 'Chassis core files are not found')        
        logging.info("Testcase5: Check for the core dump files present PASSED...\n")

        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots') as slots_patch:
            logging.info("Testcase6: Check chassis coredump files in vty command by passing fru as list and slot values")
            response = """        
               /var/crash/*core*: No such file or directory
               /var/tmp/*core*: No such file or directory
               /var/tmp/pics/*core*: No such file or directory
               /var/crash/kernel.*: No such file or directory
               /var/jails/rest-api/tmp/*core*: No such file or directory
                   """        
            self.handle.vty = MagicMock(return_value=Response(response=response)) 
            slots_patch.return_value = {}
            fru = 'scb'        
            result = chassis.check_chassis_coredump(device = self.handle,fru=fru, cmd_type='vty')
            self.assertEqual(result, True , 'Chassis core files are found')        
            logging.info("Testcase6: Check chassis coredump files in vty command by passing fru as list and slot values PASSED...\n")

        logging.info("Successfully tested check_chassis_coredump...\n")        

    def test_set_chassis_control(self):
        
        logging.info("Testing set_chassis_control...")
        
        logging.info("Testcase1: Enabling set system processes chassis-control")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_chassis_control(device=self.handle,enable=1,commit =1)
        self.assertEqual(result, True,"Unable to enable set system processes chassis-control")
        logging.info("Testcase1: Enabling set system processes chassis-control PASSED...\n")
        
        logging.info("Testcase2: Disabling set system processes chassis-control")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_chassis_control(device=self.handle,disable=1,commit =1)
        self.assertEqual(result, True,"Unable to Disable set system processes chassis-control")
        logging.info("Testcase2: Disabling set system processes chassis-control PASSED...\n")
             
        logging.info("Testcase3: Fail-overing set system processes chassis-control")
        self.handle.config = MagicMock(return_value =Response(response='True'))
        result=chassis.set_chassis_control(device=self.handle,failover=1,commit =1)
        self.assertEqual(result, True,"Unable to fail-over set system processes chassis-control")
        logging.info("Testcase3: Fail-overing set system processes chassis-control PASSED...\n")
        
        logging.info("Testcase1: Enabling set system processes chassis-control without commit")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_chassis_control(device=self.handle,enable=1)
        self.assertEqual(result, True,"Unable to enable set system processes chassis-control")
        logging.info("Testcase1: Enabling set system processes chassis-control PASSED...\n")
        
        logging.info("Successfully tested set_chassis_control...\n")

    
    def test_set_chassis_graceful(self):
        
        logging.info("Testing set_chassis_graceful...")
	
        logging.info("Testcase1: Setting redundancy graceful-switchover for the version lessthan 9.0")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        self.handle.get_version.return_value='9.0'
        result=chassis.set_chassis_graceful(device=self.handle)
        self.assertEqual(result, True,"Unable to set redundancy graceful-switchover")
        logging.info("Testcase1:Setting redundancy graceful-switchover for the version lessthan 9.0 PASSED ...\n")

        logging.info("Testcase2: Setting redundancy graceful-switchover for the version greaterthan 9.0")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        self.handle.get_version.return_value='5.0'
        result=chassis.set_chassis_graceful(device=self.handle,commit =1)
        self.assertEqual(result, True,"Unable to set redundancy graceful-switchover")
        logging.info("Testcase2:Setting redundancy graceful-switchover for the version greaterthan 9.0 PASSED ...\n")
            
    def test_set_chassis_manufacturing_diagnostic_mode(self):
        logging.info("Testcase1: setting chassis manufacturing-diagnostic-mode using cli command")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_chassis_manufacturing_diagnostic_mode(device=self.handle,commit =1)
        self.assertEqual(result, True,"Unable to set chassis manufacturing-diagnostic-mode")
        logging.info("Testcase1: setting chassis manufacturing-diagnostic-mode using cli command PASSED...\n")
        logging.info("Testcase1: setting chassis manufacturing-diagnostic-mode without commit")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_chassis_manufacturing_diagnostic_mode(device=self.handle)
        self.assertEqual(result, True,"Unable to set chassis manufacturing-diagnostic-mode")
        logging.info("Testcase1: setting chassis manufacturing-diagnostic-mode using cli command PASSED...\n")
		
		
    @patch('jnpr.toby.hardware.chassis.chassis.check_craft_display')
    def test_set_craft_display(self,display_patch):
        logging.info("Testcase1: Send display message to craft-interface using the cli command")
        display_patch.return_value = False
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_craft_display(device=self.handle,display="craft display message",check_count=2)    
        self.assertEqual(result, False,"Unable to set craft display message")
        logging.info("Testcase1: Send display message to craft-interface using the cli command PASSED...\n")
      
        logging.info("Testcase2: Send display message to craft-interface using the cli command")
        display_patch.return_value = True
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_craft_display(device=self.handle,display="craft display message",check_count=2)    
        self.assertEqual(result,True,"Unable to set craft display message")
        logging.info("Testcase2: Send display message to craft-interface using the cli command PASSED...\n")
        
        logging.info("Testcase3: Send check_count as zero")
        display_patch.return_value = True
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_craft_display(device=self.handle,display="craft display message",check_count=0)
        self.assertEqual(result,True,"Unable to set craft display message")
        logging.info("Testcase3: Send check_count as zero PASSED...\n")

    def test_set_temperature_threshold(self):
        logging.info("Testcase1: Sets the chassis temperature threshold for yellow_alarm using the cli command")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_temperature_threshold(device=self.handle,yellow_alarm=1,commit=1)
        self.assertEqual(result, True,"Unable to set chassis temperature threshold for yellow_alarm")
        logging.info("Testcase1: Sets the chassis temperature threshold for yellow_alarm using the cli command PASSED...\n")

        logging.info("Testcase2: Sets the chassis temperature threshold for red-alarm using the cli command")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_temperature_threshold(device=self.handle,red_alarm=1)
        self.assertEqual(result, True,"Unable to set chassis temperature threshold for red_alarm")
        logging.info("Testcase2: Sets the chassis temperature threshold for red_alarm using the cli command PASSED...\n")

        logging.info("Testcase3: Sets the chassis temperature threshold fans to normal speeed using the cli command")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_temperature_threshold(device=self.handle,normal_speed=1,commit=1)
        self.assertEqual(result, True,"Unable to set chassis temperature threshold fans to normal speeed")
        logging.info("Testcase3: Sets the chassis temperature threshold fans to normal speeed using the cli command PASSED...\n")
        
        logging.info("Testcase4: Sets the chassis temperature threshold fans to full speeed using the cli command")
        self.handle.config = MagicMock(return_value = Response(response='True'))
        result=chassis.set_temperature_threshold(device=self.handle,full_speed=1,commit=1)
        self.assertEqual(result, True,"Unable to set temperature threshold fans to full speeed")
        logging.info("Testcase4: Sets the temperature threshold fans to full speeed using the cli command PASSED...\n")
        
        logging.info("Testcase5: Without passing arguments to set temperature threshold")
        result=chassis.set_temperature_threshold(device=self.handle)
        self.assertEqual(result, False," Arguments passed to set temperature threshold ")
        logging.info("Testcase5: without passing arguments to set temperature threshold PASSED...\n")

        logging.info ("Sucessfully tested set_temperature_threshold...\n")
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_status')
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_status')
    @patch('time.sleep')
    def test_restart_chassisd(self,sleep_patch,check_status_patch,get_status_patch):
        logging.info("Testing restart_chassisd...")
        logging.info("Testcase1: Without passing arguments to restart chassisd")
        get_status_patch.return_value = [{'state':'Online','status':'Offline'}]
        check_status_patch.return_value = False
        result=chassis.restart_chassisd(device=self.handle)
        self.assertEqual(result, False," Arguments passed to restart chassid")
        logging.info("Testcase1: without passing arguments to restart chassisd PASSED...\n")         
 
        logging.info("Testcase2: With passing arguments to restart chassisd")
        check_status_patch.return_value = True
        status = [{'state':'Online','status':'Offline'}] 
        result=chassis.restart_chassisd(device=self.handle,sleep_val=5,status=status,chassis='lcc',soft='soft',check_all=1)
        self.assertEqual(result, True," Arguments passed to restart chassid")
        logging.info("Testcase2: With passing arguments to restart chassisd PASSED...\n")

        logging.info("Testcase3: With passing check_count but not soft arguments to restart chassisd")
        check_status_patch.return_value = True
        status = [{'state':'Online','status':'Offline'}]
        result=chassis.restart_chassisd(device=self.handle,sleep_val=5,status=status,chassis='lcc',check_all=1,check_count=5)
        self.assertEqual(result, True,"Soft passed to restart chassid")
        logging.info("Testcase3:With passing check_count but not soft arguments to restart chassisd PASSED...\n")

    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_status')
    @patch('jnpr.toby.hardware.chassis.chassis.kill_process')
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_status')
    def test_kill_chassisd(self, check_status_patch, kill_patch, get_status_patch):
        logging.info("Testing kill_chassisd...")
        logging.info("Testcase1:Kill chassis daemon process by passing sleep argument")
        kill_patch.return_vlaue = True
        check_status_patch.return_value = False
        get_status_patch.return_value = [{'state':'backup','status':'Online'}]
        self.handle.su = MagicMock(return_value = Response(response='True'))
        result = chassis.kill_chassisd(device=self.handle,sleep_val=1,check_all=1)
        self.assertEqual(result, False, "kill chassis daemon process success")
        logging.info("Testcase1:Kill chassis daemon process by passing sleep argument PASSED...\n")

        logging.info("Testcase2: Kill chassis daemon process in TX Matrix /TXP models...")
        kill_patch.return_vlaue = True
        check_status_patch.return_value = True
        self.handle.get_model = MagicMock(return_value = 'TXP')
        status = [{'state':'backup','status':'Online'}]
        self.handle.su = MagicMock(return_value = Response(response='True'))
        result = chassis.kill_chassisd(device=self.handle,sleep_val=1, check_all=1,status=status)
        self.assertEqual(result, True, "Failed to kill chassis daemon process")
        logging.info("Testcase2: Kill chassis daemon process in TX Matrix /TXP models...\n")

        logging.info("Testcase3: Kill chassis daemon process for other than TX Matrix /TXP models...")
        kill_patch.return_vlaue = True
        check_status_patch.return_value = True
        self.handle.get_model = MagicMock(return_value = 'mx480')
        status = [{'state':'backup','status':'Online'}]
        self.handle.su = MagicMock(return_value = Response(response='True'))
        result = chassis.kill_chassisd(device=self.handle,sleep_val=1, check_all=0,
                                       check_interface=1, status=status)
        self.assertEqual(result, True, "Failed to kill chassis daemon process")
        logging.info("Testcase3: Kill chassis daemon process in TX Matrix /TXP models...\n")

        logging.info("Testcase4: Kill chassis daemon process by passing sleep argument")
        self.handle.get_model = MagicMock(return_value = 'MX960')
        kill_patch.return_vlaue = True
        check_status_patch.return_value = False
        get_status_patch.return_value = [{'state':'backup','status':'Online'}]
        self.handle.su = MagicMock(return_value = Response(response='True'))
        result = chassis.kill_chassisd(device=self.handle,sleep_val=1, check_all=1, check_interface=0,
                                       check_hardware=0, check_craft=0, check_alarm=0,
                                       check_memory=0, check_database=0)
        self.assertEqual(result, False, "kill chassis daemon process success")
        logging.info("Testcase4:Kill chassis daemon process by passing sleep argument PASSED...\n")
        
    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_list')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_status')
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_list')
    def test_get_fru_slots(self,chas_list_patch,status_patch,fru_list_patch):

        from jnpr.toby.hardware.chassis.chassis import get_fru_slots
		
        logging.info("Testing get fru slots...")
        logging.info("Testcase1: get the slots for lcc...")
        xml= """
        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
    <multi-routing-engine-results>
         
        <multi-routing-engine-item>
             
            <re-name>sfc0-re0</re-name>
             
            <software-information>
                <host-name>splinter</host-name>
                <product-model>txp</product-model>
                <product-name>txp</product-name>
                <junos-version>17.1-20170407.0</junos-version>
                <package-information>
                    <name>junos</name>
                    <comment>JUNOS Base OS boot [17.1-20170407.0]</comment>
                </package-information>
</software-information>
        </multi-routing-engine-item>
         
        <multi-routing-engine-item>
             
            <re-name>lcc0-re0</re-name>
             
            <software-information>
                <host-name>leonardo</host-name>
                <product-model>t1600</product-model>
                <product-name>t1600</product-name>
                <junos-version>17.1-20170407.0</junos-version>
                <package-information>
                    <name>junos</name>
                    <comment>JUNOS Base OS boot [17.1-20170407.0]</comment>
                </package-information>
</software-information>
        </multi-routing-engine-item>
         
        <multi-routing-engine-item>
             
            <re-name>lcc1-re0</re-name>
   <software-information>
                <host-name>raphael</host-name>
                <product-model>t1600</product-model>
                <product-name>t1600</product-name>
                <junos-version>17.1-20170407.0</junos-version>
                <package-information>
                    <name>junos</name>
                    <comment>JUNOS Base OS boot [17.1-20170407.0]</comment>
                </package-information>
  </software-information>
        </multi-routing-engine-item>
         
    </multi-routing-engine-results>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>

        """
        response = etree.fromstring(xml)
        # ====================================================================#
        logging.info("Testcase1: Get chassis slots for fru is lcc")
        self.handle.get_model = MagicMock(return_value = 'TXP')
        self.handle.execute_rpc = MagicMock(return_value=Response(response=response))        
        result = get_fru_slots(device=self.handle,fru='lcc')
        self.assertEqual(result, ['0', '1'], "get slots successful with fru is lcc")   

        self.handle.get_model = MagicMock(return_value = 'TXP')
        chas_list_patch.return_value = ['scc']
        result = get_fru_slots(device=self.handle, fru='pic')
        self.assertEqual(result, {}, "get slots unsuccessful with fru is incorrect")   
        # ====================================================================#
        logging.info("Testcase2: Get chassis slots for TX Matrix/TXP model.")
        chas_list_patch.return_value = ['sfc 0','lcc 0','lcc 1']
        self.handle.get_model = MagicMock(return_value = 'TXP')
        status = {'sfc 0':[{'state':'Online','status':'backup'}],'lcc 0':{'state':'Online'},'lcc 1':{'state':'Online'}}
        result = get_fru_slots(device=self.handle,fru='fpc',status=status)
        expected_result = {'lcc 0': [0], 'lcc 1': [0], 'sfc 0': [0]}
        self.assertEqual(result,expected_result, "get slots for TX Matrix/TXP model successful") 
 
        # ====================================================================#
        logging.info("Testcase3: Get fru list from get_chassis_list and fru as list")
        self.handle.get_model = MagicMock(return_value='mx480')
        fru_list_patch.return_value = ['pic']         
        status_patch.return_value = {'pic': []}
        result = get_fru_slots(device=self.handle)
        self.assertEqual(type(result),dict,"Failed to get fru slots")
        # ====================================================================#
        logging.info("Testcase4: Get fru slots for pic")
        self.handle.get_model = MagicMock(return_value='mx480')
        status = [[{'state':'backup','status':'Online'}]]
        result = get_fru_slots(device=self.handle,fru=['pic','re', 'abc'],status=status)
        expected_result = {'pic': [], 'abc': [0], 're': [0]}
        self.assertEqual(result,expected_result,"Failed to get fru slots")
        #====================================================================#
        logging.info("Testcase5: Get fru slots successful with state value")
        self.handle.get_model = MagicMock(return_value='mx480')
        status = [[{'state':'Online'}]]
        result = get_fru_slots(device=self.handle,fru='pic',status=status,
                               state='Online')
        expected_result = [[0, 0]]
        self.assertEqual(result,expected_result,"get fru slots successfull "
                         "with state value")
        # ====================================================================#
        logging.info("Testcase6: Get fru slots with chassis is scc")
        self.handle.get_model = MagicMock(return_value='mx480')
        status = [[{'state':'Online'}]]
        result = get_fru_slots(device=self.handle,chassis='scc',
                               fru=['pic', 're'] ,status=status)
        self.assertEqual(result, {'re': [0]}, "Get fru slots fail with chassis is scc")

  
        # ====================================================================#
        logging.info("Testcase7: Get fru slots for pic and re and model ex4200")
        xml= """<multi-routing-engine-results>
        <multi-routing-engine-item>
            <re-name>member1</re-name>
            <software-information>
                <host-name>splinter</host-name>
                <product-model>txp</product-model>
                <product-name>txp</product-name>
                <junos-version>17.1-20170407.0</junos-version>
                <package-information>
                    <name>junos</name>
                    <comment>JUNOS Base OS boot [17.1-20170407.0]</comment>
                </package-information>
                </software-information>
        </multi-routing-engine-item>
        </multi-routing-engine-results>
        """
        response = etree.fromstring(xml)
        self.handle.execute_rpc = MagicMock(return_value=Response(response=response)) 
        self.handle.get_model = MagicMock(return_value='ex4200')

        status = {'state': 'Online'}
        result = get_fru_slots(device=self.handle,fru=['pic', 're', 'abc'],
                               status=status)
        expected_result = {'re': {'member1': [0]}, 'pic': {'member1': []}, 'abc': {}}
        self.assertEqual(result, expected_result, "get fru slots successful"
                         "with model ex4200")

        status = [[{'state': 'Online'}]]
        status_patch.return_value = status
        result = get_fru_slots(device=self.handle,fru=['pic'], state='Offline')
        expected_result = {'pic': {'member1': []}}
        self.assertEqual(result, expected_result, "get fru slots successful"
                         "with model ex4200")

        status = [{'state': 'Online'}]
        status_patch.return_value = status
        result = get_fru_slots(device=self.handle,fru=['re'], state='Offline')
        expected_result = {'re': {'member1': []}}
        self.assertEqual(result, expected_result, "get fru slots successful"
                         "with model ex4200")

        result = get_fru_slots(device=self.handle,fru=['re'], state='Online')
        self.handle.get_model = MagicMock(return_value='ptx5000')
        expected_result = {'re': {'member1': [0]}}
        self.assertEqual(result, expected_result, "get fru slots successful"
                         "with model ptx support")

        status = [{'0': {'status': 'Master', 'state': 'Online', 'name': '12.0 V *', 'value': '65'},
                 '1': {'status': 'Standby', 'state': 'Online', 'name': '12.0 V *', 'value': '65'}}]
        self.handle.get_model = MagicMock(return_value='ptx5000')
        result = get_fru_slots(device=self.handle,fru='ccg',status=status,state='Online')
        self.assertEqual(type(result),list , "get fru slots successful"
                         "with model ptx support")
    
        status = [{'0': {'status': 'Master'},
                 '1': {'status': 'Standby'}}]
        self.handle.get_model = MagicMock(return_value='ptx5000')
        result = get_fru_slots(device=self.handle,fru='ccg',status=status,state='Online')
        self.assertEqual(type(result),list , "get fru slots successful"
                         "with model ptx support")
		
    def test_check_chassis_memory(self):
       
        logging.info(" Testing check_chassis_memory......") 
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_memory',return_value=['43144K']) as memory_patch:
            logging.info("\tTest case 1: Checking for positive case")
            result = chassis.check_chassis_memory(device=self.handle,memory = [912432234000])
            self.assertEqual(result,True,'Expected result not found')
            logging.info("\t\tTestcase Passed")

        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_memory',return_value=['43144K']) as memory_patch:
            logging.info("\tTest case 2: Checking for negative case")
            result = chassis.check_chassis_memory(device=self.handle,memory = [91243])
            self.assertEqual(result,False,'Expected result not found')
            logging.info("\t\tTestcase Passed")
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_check_fru_valid(self):
        
        logging.info(" Testing check_fru_valid......")
        self.handle.get_model = MagicMock(return_value = 'mx480')
 
        logging.info("\tTest case 1 : Passing a valid fru (positive case)")
        result = chassis.check_fru_valid(device=self.handle,fru='fpc')
        self.assertEqual(result,True,"Expected result not found")
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 2 : Passing Invalid fru (negative case)")
        result = chassis.check_fru_valid(device=self.handle,fru='invalid_fru')
        self.assertEqual(result,False,"Expected result not found")
        logging.info("\t\tTestcase Passed")
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_get_fru_list(self):
        
        logging.info(" Testing get_fru_list......")
        self.handle.get_model = MagicMock(return_value = 'mx480')
        logging.info("\tTest case 1 : Setting test value")
        result = chassis.get_fru_list(device = self.handle,test=1)
        self.assertEqual(type(result),list, 'Expecting list but found %s'%(type(result)))
        result = chassis.get_fru_list(device = self.handle)
        self.assertEqual(type(result),list, 'Expecting list but found %s'%(type(result)))
        logging.info("\t\tTestcase Passed") 
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_get_spc_slots(self):

        logging.info(" Testing get_spc_slots......")
        response = """
                     FPC  01
                     FPC  02
                   """
        self.handle.cli = MagicMock(return_value=Response(response = response))
        logging.info("\tTest case 1 : Passing response with spc slots")
        result = chassis.get_spc_slots(device=self.handle)
        self.assertEqual(type(result),list,'Expecting list but found %s'%type(result))
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 2 : Without passing response")
        self.handle.cli = MagicMock(return_value=Response(response = ''))
        result = chassis.get_spc_slots(device=self.handle)
        self.assertEqual(result,False,'Expecting False but found %s'%type(result))
        logging.info("\t\tTestcase Passed")
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_get_test_frus(self):
        
        logging.info(" Testing get_test_frus......")
        logging.info("\tTest case : Checking for list of fru returning")
        self.handle.get_model = MagicMock(return_value = "mx480")
        result = chassis.get_test_frus(device = self.handle)
        self.assertEqual(type(result),list,'Expecting list but found %s'%type(result))
        logging.info("\t\tTestcase Passed")
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_get_chassis_status(self):

        logging.info(" Testing get_chassis_status......")

        fru_patch       = self.create_patch('jnpr.toby.hardware.chassis.chassis.get_fru_status')
        hardware_patch  = self.create_patch('jnpr.toby.hardware.chassis.chassis.get_chassis_hardware')
        craft_patch     = self.create_patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft')
        interface_patch = self.create_patch('jnpr.toby.hardware.chassis.chassis.get_chassis_interface')
        alarm_patch     = self.create_patch('jnpr.toby.hardware.chassis.chassis.get_chassis_alarm')
        memory_patch    = self.create_patch('jnpr.toby.hardware.chassis.chassis.get_chassis_memory')

        fru_patch.return_value       = { 'PEM 01' : { 'state' : 'Online'}}
        hardware_patch.return_value  = {'cb 0': {'description': 'Enhanced MX SCB', 'serial-number': 'CAAS1382'}}
        craft_patch.return_value     = { 'craft-information' : {'display-panel':{'display-line':'2 Alarms Active'}}}
        interface_patch.return_value = {'interface-information':{'name':'pfh-0/0/0'}}
        alarm_patch.return_value     = {'alarm-information' :{'alarm-summary':'No alarms Active'}}
        memory_patch.return_value    = ['43144K',"resobj"]

        logging.info("\tTestcase : Collecting chassis status")
        result = chassis.get_chassis_status(device = self.handle,skip_interface = 'pimd')
        self.assertEqual(type(result), dict, 'Cannot get chassis status')
        logging.info("\t\tTestcase Passed")
        
        logging.info("\tTestcase : Collecting chassis status without fru")
        result = chassis.get_chassis_status(device = self.handle, fru=0,
                                            hardware=0, craft=0, interface=0,
                                            alarm=0, memory=0)
        self.assertEqual(result, {}, 'Cannot get chassis status')
        logging.info("\t\tTestcase Passed")
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")    



    def test_get_chassis_interface(self):

        logging.info(" Testing get_chassis_interface......")

        response  = """
              <rpc-reply xmlns:junos="http://xml.juniper.net/junos/13.3R10/junos">
                  <interface-information xmlns="http://xml.juniper.net/junos/13.3R10/junos-interface" junos:style="terse">
                      <physical-interface>
                          <name>pfh-0/0/0</name>
                          <admin-status>up</admin-status>
                          <oper-status>up</oper-status>
                          <logical-interface>
                               <name>pfh-0/0/0.16383</name>
                               <admin-status>up</admin-status>
                               <oper-status>up</oper-status>
                               <filter-information></filter-information>
                               <address-family>
                                   <address-family-name>inet</address-family-name>
                               </address-family>
                          </logical-interface>
                      </physical-interface>
                  </interface-information>
                  <cli>
                      <banner></banner>
                  </cli>
              </rpc-reply>
              """
        self.handle.cli = MagicMock(return_value = Response(response=response))

        logging.info("\tTest case 1 : Without passing arguments")
        result = chassis.get_chassis_interface(self.handle)
        self.assertEqual(type(result), dict,'Expected dict but found %s'%type(result))
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 2 : Passing interface argument")
        result = chassis.get_chassis_interface(self.handle,interface_name='pfh-0/0/0')
        self.assertEqual(type(result), dict,'Expected dict but found %s'%type(result))
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 3 : Passing skip_interface argument")
        result = chassis.get_chassis_interface(self.handle,skip_interface='fe-2/2.*')
        self.assertEqual(type(result), dict,'Expected dict but found %s'%type(result))
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 4 : Different Interface and skip_if arguments")
        result = chassis.get_chassis_interface(self.handle,interface_name='lo0',skip_interface='pfh-0/0/0')
        self.assertEqual(type(result), dict,'Expected dict but found %s'%type(result))
        logging.info("\t\tTestcase Passed")

        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_get_chassis_ethernet(self):
       
        logging.info(" Testing get_chassis_ethernet......")
        with patch('jnpr.toby.hardware.chassis.chassis.__cli_get_ethernet') as ethernet_patch:
            logging.info("\tTest case : Getting info from cli_get_ethernet ")
            ethernet_patch.return_value = {'re':{'duplex':'full','port':'13','speed': '100Mb','status': 'good'}} 
            result = chassis.get_chassis_ethernet(device=self.handle)
            self.assertEqual(type(result), dict,'Expected dict but found %s'%type(result))
            logging.info("\t\tTestcase Passed")
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")
        
    def test_check_craft_led(self):
        
        logging.info(" Testing check_craft_led......")

        response = """
                   <craft-information>\n<front-panel>\n<display-panel>\n<display-line>\n+--------------------+\n</display-line>\n<display-line>\n|win                 |\n</display-line>\n<display-line>\n|2 Alarms active     |\n</display-line>\n<display-line>\n|R: PEM 3 Not OK     |\n</display-line>\n<display-line>\n|R: PEM 2 Not OK     |\n</display-line>\n<display-line>\n+--------------------|\n</display-line>\n</display-panel>\n<re-panel>\n<re>\n<slot>0</slot>\n<ok-led/>\n<master-led/>\n</re>\n<re>\n<slot>1</slot>\n<ok-led/>\n</re>\n</re-panel>\n<alarm-indicators>\n<red-led/>\n<major-alarm-relay/>\n</alarm-indicators>\n<fpc-panel>\n<fpc>\n<slot>0</slot>\n<green-led/>\n</fpc>\n<fpc>\n<slot>1</slot>\n<green-led/>\n</fpc>\n<fpc>\n<slot>2</slot>\n<green-led/>\n</fpc>\n<fpc>\n<slot>3</slot>\n<green-led/>\n</fpc>\n<fpc>\n<slot>4</slot>\n<green-led/>\n</fpc>\n<fpc>\n<slot>5</slot>\n<green-led/>\n</fpc>\n<fpc>\n<slot>6</slot>\n</fpc>\n<fpc>\n<slot>7</slot>\n</fpc>\n</fpc-panel>\n</front-panel>\n<cb-panel>\n<cb>\n<slot>0</slot>\n<green-led/>\n<blue-led/>\n</cb>\n<cb>\n<slot>1</slot>\n<green-led/>\n</cb>\n</cb-panel>\n<sib-panel>\n<sib>\n<slot>0</slot>\n<green-led/>\n</sib>\n<sib>\n<slot>1</slot>\n<green-led/>\n</sib>\n<sib>\n<slot>2</slot>\n<green-led/>\n</sib>\n<sib>\n<slot>3</slot>\n<green-led/>\n</sib>\n</sib-panel>\n<power-supply-panel>\n<power-supply>\n<slot>0</slot>\n<green-led/>\n</power-supply>\n<power-supply>\n<slot>1</slot>\n<green-led/>\n</power-supply>\n<power-supply>\n<slot>2</slot>\n<red-led/>\n</power-supply>\n<power-supply>\n<slot>3</slot>\n<red-led/>\n</power-supply>\n</power-supply-panel>\n<output>\nFPM Display contents:\n    +--------------------+\n    |win                 |\n    |2 Alarms active     |\n    |R: PEM 3 Not OK     |\n    |R: PEM 2 Not OK     |\n    +--------------------|\n\nFront Panel System LEDs:\nRouting Engine    0    1\n--------------------------\nOK                *    *\nFail              .    .\nMaster            *    .\n\nFront Panel Alarm Indicators:\n-----------------------------\nRed LED      *\nYellow LED   .\nMajor relay  *\nMinor relay  .\n\nFront Panel FPC LEDs:\nFPC    0   1   2   3   4   5   6   7\n------------------------------------\nRed    .   .   .   .   .   .   .   .\nGreen  *   *   *   *   *   *   .   .\n\nCB LEDs:\n  CB   0   1\n--------------\nAmber  .   .\nGreen  *   *\nBlue   *   .\n\nSIB LEDs:\n  SIB  0   1   2   3\n------------------------\nRed    .   .   .   .\nGreen  *   *   *   *\n\nPS LEDs:\n  PS   0   1   2   3\n------------------------\nRed    .   .   *   *\nGreen  *   *   .   .\n</output>\n</craft-information>\n
                   """
      
        logging.info("\tTest case 1 : Without passing fru and led")
        result = chassis.check_craft_led(device=self.handle)
        self.assertEqual(result,None, "Expected result not found")
        logging.info("\t\tTestcase Passed")

        with patch("jnpr.toby.hardware.chassis.chassis.get_chassis_craft") as craft_patch:
            logging.info("\tTest case 2 : Negative case without check_count argument")
            response = response.strip('\n')
            output   = ast.literal_eval(str(jxmlease.parse(response)))
            craft_patch.return_value = output['craft-information']['front-panel']['fpc-panel']
            result = chassis.check_craft_led(device=self.handle,fru = 'fpc', led = ['green-led'],slot = 2)
            self.assertEqual(result, False, "Expecting False but found %s"%result)
            logging.info("\t\tTestcase Passed")

            logging.info("\tTest case 3 : Negative case with check_count argument")
            result = chassis.check_craft_led(device=self.handle,fru = 'fpc', led = ['green-led'],slot = 2,check_count=2)
            self.assertEqual(result, False, "Expecting False but found %s"%result)
            logging.info("\t\tTestcase Passed")

            logging.info("\tTest case 4 : Positive case by passing led argument as string")
            output['craft-information']['front-panel']['fpc-panel']['fpc'][2]['green-led']=1
            result = chassis.check_craft_led(device=self.handle,fru = 'fpc', led = 'green-led',slot = 2)
            self.assertEqual(result, True, "Expecting True but found %s"%result)
            logging.info("\t\tTestcase Passed")
            
            logging.info("\tTest case 5 : with craft  argument")
            craft = output['craft-information']['front-panel']['fpc-panel']
            result = chassis.check_craft_led(device=self.handle,fru = 'fpc', led = {'green-led':1},slot = 2,craft=craft)
            self.assertEqual(result, True, "Expecting True but found %s"%result)
            logging.info("\t\tTestcase Passed")
 
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_check_chassis_hardware(self):
    
        logging.info(" Testing check_chassis_hardware......")
    
        with patch("jnpr.toby.hardware.chassis.chassis.get_chassis_hardware") as hardware_patch:
            logging.info("\tTest case 1 : Positive case for passing hardware")
            hardware_patch.return_value = {'cb 0': {'description': 'Enhanced MX SCB', 'serial-number': 'CAAS1382'},
                                           'cb 1': {'description': 'Enhanced MX SCB', 'serial-number': 'CAAS1153'}}
            result = chassis.check_chassis_hardware(device = self.handle,chassis='sfc 0')
            self.assertEqual(result,True, 'Hardware not matching')
            logging.info("\t\tTestcase Passed")

            logging.info("\tTest case 1 : Negative case for passing hardware")
            hardware_patch.return_value = {'cb 0': {'description': 'Enhanced MX SCB', 'serial-number': 'CAAS1382'},
                                           'cb 1': {'description': 'Enhanced MX SCB', 'serial-number': 'CAAS1153'}}
            hardware = {'routing engine 0': {'description': 'RE-S-1800x4', 'serial-number': '9009119525'}}
            result   = chassis.check_chassis_hardware(device = self.handle,chassis='sfc 0',hardware=hardware)
            self.assertEqual(result,False, 'Hardware matching but expecting not to match(negative case)')
            logging.info("\t\tTestcase Passed")

        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    @patch('jnpr.toby.hardware.chassis.chassis.__cli_get_craft')
    def test_get_chassis_craft(self, cli_craft):
        
        logging.info(" Testting get_chassis_craft......")
        
        
        logging.info("\tTest case 1 : Global variable CHECK_CRAFT in False state")
        chassis.CHECK_CRAFT  = False
        result = chassis.get_chassis_craft(device=self.handle)
        self.assertEqual(result,None,'Expecting None but found %s'%(type(result)))
        logging.info("\t\tTestcase Passed")
        chassis.CHECK_CRAFT = True
 
        logging.info("\tTest case 2 : Passing model as mx480")
        cli_craft.return_value = { "craft-information": {'alarm': {'alarm': 1}, 'cb': {'0': {'blue': 1, 'green': 1}}}}
        self.handle.get_model = MagicMock(return_value="mx480")
        result = chassis.get_chassis_craft(device=self.handle)
        self.assertEqual(type(result), dict,'Expected dict result from cli_get_craft but found %s'%type(result))
        logging.info("\t\tTestcase Passed")
        
        logging.info("\tTest case 3 : Test model as ex4200")
        self.handle.get_model = MagicMock(return_value="ex4200")
        result = chassis.get_chassis_craft(device=self.handle)
        self.assertEqual(type(result), dict,'Expected dict result from cli_get_craft but found %s'%type(result))
        logging.info("\t\tTestcase Passed")
        
 
        logging.info("Test case 4 : Passing model as TXP")
        response_xml  = """
                    <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
                      <multi-routing-engine-results>
                         <multi-routing-engine-item>
                            <re-name>sfc0-re0</re-name>
                            <craft-information>
                                   <front-panel>
                                         <display-panel>
                                                <display-line>+--------------------+</display-line>
                                                <display-line>|splinter            |</display-line>
                                                <display-line>|13 Alarms active    |</display-line>
                                                <display-line>|R: SIB F13 8 Fault  |</display-line>
                                                <display-line>|R: SIB F13 1 Absent |</display-line>
                                                <display-line>+--------------------+</display-line>
                                         </display-panel>
                                         <re-panel>
                                                <re>
                                                    <slot>0</slot>
                                                    <ok-led/>
                                                    <master-led/>
                                                </re>
                                         </re-panel>
                                         <alarm-indicators>
                                                <red-led/>
                                                <yellow-led/>
                                                <major-alarm-relay/>
                                                <minor-alarm-relay/>
                                         </alarm-indicators>
                                   </front-panel>
                                   <sib-panel>
                                         <sib>
                                                <slot>0</slot>
                                                <ok-led/>
                                                <active-led/>
                                         </sib>
                                   </sib-panel>
                                   <power-supply-panel>
                                         <power-supply>
                                                <slot>0</slot>
                                         </power-supply>
                                   </power-supply-panel>
                                   <fan-tray-panel>
                                         <fan-tray>
                                                <slot>0</slot>
                                                <green-led/>
                                         </fan-tray>
                                   </fan-tray-panel>
                                   <cb-panel>
                                         <cb>
                                                <slot>0</slot>
                                                <green-led/>
                                                <blue-led/>
                                         </cb>
                                   </cb-panel>
                            </craft-information>
                        </multi-routing-engine-item>
                   </multi-routing-engine-results>                              
                   <cli>
                        <banner></banner>
                   </cli>
                </rpc-reply>
                 """
        xml    = etree.fromstring(response_xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=response_xml)
        self.handle.execute_rpc        = MagicMock(return_value=Response(response=xml))
        self.handle.get_model = MagicMock(return_value="TXP")
        result = chassis.get_chassis_craft(device=self.handle,xml=1)
        self.assertEqual(type(result), dict, 'Expected dict not found')
        logging.info("\t\tTestcase Passed")
        
        logging.info("Test case 5 : Passing model as TXP")
        response_xml  = """
                    <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
                      <multi-routing-engine-results>
                         <multi-routing-engine-item>
                            <re-name>re0</re-name>
                            <craft-information>
                                    <abc>

                                    </abc>
                                   <front-panel>
                                         <display-panel>
                                                <display-line>+--------------------+</display-line>
                                                <display-line>|splinter            |</display-line>
                                                <display-line>|13 Alarms active    |</display-line>
                                                <display-line>|R: SIB F13 8 Fault  |</display-line>
                                                <display-line>|R: SIB F13 1 Absent |</display-line>
                                                <display-line>+--------------------+</display-line>
                                         </display-panel>
                                         <re-panel>
                                                <re>
                                                    <slot>0</slot>
                                                    <ok-led/>
                                                    <master-led/>
                                                </re>
                                         </re-panel>
                                         <alarm-indicators>
                                                <red-led/>
                                                <yellow-led/>
                                                <major-alarm-relay/>
                                                <minor-alarm-relay/>
                                         </alarm-indicators>
                                        <abc>
                                                <red-led/>
                                                <yellow-led/>
                                                <major-alarm-relay/>
                                                <minor-alarm-relay/>
                                         </abc>
                                   </front-panel>
                                   <sib-panel>
                                         <sib>
                                                <slot>0</slot>
                                                <ok-led/>
                                                <active-led/>
                                         </sib>
                                   </sib-panel>
                                   <power-supply-panel>
                                         <power-supply>
                                                <slot>0</slot>
                                         </power-supply>
                                   </power-supply-panel>
                                   <fan-tray-panel>
                                         <fan-tray>
                                                <slot>0</slot>
                                                <green-led/>
                                         </fan-tray>
                                   </fan-tray-panel>
                                   <cb-panel>
                                         <cb>
                                                <slot>0</slot>
                                                <green-led/>
                                                <blue-led/>
                                         </cb>
                                   </cb-panel>
                            </craft-information>
                        </multi-routing-engine-item>
                   </multi-routing-engine-results>
                   <cli>
                        <banner></banner>
                   </cli>
                </rpc-reply>
                 """
        xml    = etree.fromstring(response_xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=response_xml)
        self.handle.execute_rpc        = MagicMock(return_value=Response(response=xml))
        self.handle.get_model = MagicMock(return_value="TXP")
        result = chassis.get_chassis_craft(device=self.handle,xml=1)
        self.assertEqual(type(result), dict, 'Expected dict not found')
        logging.info("\t\tTestcase Passed")
        
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_get_chassis_firmware(self):
        
        logging.info(" Testing get_chassis_firmware......")
        
        with patch("jnpr.toby.hardware.chassis.chassis.__cli_get_firmware") as cli_firmware_patch :
            logging.info("\tTest case 1 : Setting xml variable as 0 & Expecting dict from __cli_get_firmware")
            cli_firmware_patch.return_value = {'fpc 0':{'ROM':'Juniper ROM Monitor Version 6.0b12',
                                                        'O/S':'Version 15.1R1.9 by builder on 2015-06-18 06:38:55 UTC'}} 
            self.handle.get_model = MagicMock(return_value="mx480")
            result = chassis.get_chassis_firmware(device=self.handle,xml=0)
            self.assertEqual(type(result), dict,'Expected dict result from cli_get_firmware but found %s'%type(result))
            logging.info("\t\tTestcase Passed")
        
        logging.info("Test case 2 : Passing model as TXP")
        response_xml  = """
                        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
                           <multi-routing-engine-results>
                               <multi-routing-engine-item>
                                    <re-name>sfc0-re0</re-name>
                                    <firmware-information>
                                           <chassis junos:style="firmware">
                                                 <chassis-module>
                                                     <name>Global FPC 0</name>
                                                 </chassis-module>
                                                 <chassis-module>
                                                     <name>SPMB 0</name>
                                                     <firmware>
                                                        <type>ROM</type>
                                                        <firmware-version>Juniper ROM Monitor Version 9.5b1</firmware-version>
                                                     </firmware>
                                                     <firmware>
                                                         <type>O/S</type>
                                                         <firmware-version>Version 17.1-20170407.0 by builder on 2017-04-07 01:00:09 UTC</firmware-version>
                                                     </firmware>
                                                 </chassis-module>
                                                 <chassis-module>
                                                     <name>SPMB 1</name> 
                                                     <firmware>      
                                                         <type>ROM</type>
                                                         <firmware-version>Juniper ROM Monitor Version 9.5b1</firmware-version>
                                                     </firmware>
                                                 </chassis-module>
                                           </chassis>
                                   </firmware-information>
                              </multi-routing-engine-item>
                         </multi-routing-engine-results>
                         <cli>
                             <banner></banner>
                         </cli>
                     </rpc-reply>
                        """
        xml    = etree.fromstring(response_xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=response_xml)
        self.handle.execute_rpc        = MagicMock(return_value=Response(response=xml))
        self.handle.get_model          = MagicMock(return_value="TXP")
        result = chassis.get_chassis_firmware(device=self.handle,xml=1)
        self.assertEqual(type(result), dict, 'Expected dict not found')
        logging.info("\t\tTestcase Passed")
      
        logging.info("Test case 3 : Passing model as Mx480")
        response_xml  = """
                        <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
                            <chassis-module>
                                <name>SPMB 0</name>
                                <firmware>
                                    <type>ROM</type>
                                    <type>O/S</type>
                                    <firmware-version>Version 17.1-20170407.0 by builder on 2017-04-07 01:00:09 UTC</firmware-version>
                                </firmware>
                            </chassis-module>
                            <chassis-module>
                                <name>SPMB 1</name> 
                                <firmware>      
                                     <type>ROM</type>
                                     <firmware-version>Juniper ROM Monitor Version 9.5b1</firmware-version>
                                </firmware>
                           </chassis-module>
                        </rpc-reply>
                        """
        xml    = etree.fromstring(response_xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=response_xml)
        self.handle.execute_rpc        = MagicMock(return_value=Response(response=xml))
        self.handle.get_model          = MagicMock(return_value="mx480")
        result = chassis.get_chassis_firmware(device=self.handle,xml=1)
        self.assertEqual(type(result), dict, 'Expected dict not found')
        logging.info("\t\tTestcase Passed")

        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_test_chassis_fan(self):
        
        logging.info(" Testing test_test_chassis_fan......")
        enhance_fantray_patch = self.create_patch("jnpr.toby.hardware.chassis.chassis.check_enhance_fantray")
       
        with patch("jnpr.toby.hardware.chassis.chassis.check_chassis_fan",return_value=False) as chassis_fan_patch:
            logging.info("\tTest case 1 : Passing model as TX Matrix & check_chassis_fan returns False")
            self.handle.get_model = MagicMock(return_value="TX Matrix")
            enhance_fantray_patch.return_value = True
            result = chassis.test_chassis_fan(device = self.handle)
            self.assertEqual(result,False,"Expecting False but found True")
            logging.info("\t\tTestcase Passed")

        with patch("jnpr.toby.hardware.chassis.chassis.check_chassis_fan",side_effect=[True,False]) as chassis_fan_patch:
            logging.info("\tTest case 2 : Passing model as TXP")
            self.handle.get_model = MagicMock(return_value="TXP")
            enhance_fantray_patch.return_value = True
            result = chassis.test_chassis_fan(device = self.handle)
            self.assertEqual(result,False,"Expecting False but found True")
            logging.info("\t\tTestcase Passed")

        with patch("jnpr.toby.hardware.chassis.chassis.check_chassis_fan",return_value=True) as chassis_fan_patch:
            logging.info("\tTest case 3 : Passing model as TXP & check_enhance_fantray returns False")
            self.handle.get_model = MagicMock(return_value="TXP")
            enhance_fantray_patch.return_value = True
            result = chassis.test_chassis_fan(device = self.handle)
            self.assertEqual(result,True,"Expecting True but found False")
            logging.info("\t\tTestcase Passed")

        with patch("jnpr.toby.hardware.chassis.chassis.check_chassis_fan",return_value=True) as chassis_fan_patch:
            logging.info("\tTest case 4 : Passing unknown speed (negative case)")
            self.handle.get_model = MagicMock(return_value="TXP")
            enhance_fantray_patch.return_value = True
            result = chassis.test_chassis_fan(device = self.handle,speed="unknown")
            self.assertEqual(result,False,"Expecting False but found True")
            logging.info("\t\tTestcase Passed")
        
        with patch("jnpr.toby.hardware.chassis.chassis.check_chassis_fan",return_value=True) as chassis_fan_patch:
            logging.info("\tTest case 5 : Passing speed as full,Model as mx480 and  (negative case)")
            self.handle.get_model = MagicMock(return_value="mx480")
            enhance_fantray_patch.return_value = False
            result = chassis.test_chassis_fan(device = self.handle,speed="full")
            self.assertEqual(result,None,"Expecting None but found %s"%result)
            logging.info("\t\tTestcase Passed")
 
        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    def test_get_chassis_alarm(self):
        
        logging.info(" Testing get_chassis_alarm......")
        with patch("jnpr.toby.hardware.chassis.chassis.__cli_get_alarm") as cli_alarm_patch:
            logging.info("\tTest case 1 : Passing xml as 0 ")
            cli_alarm_patch.return_value = [{'short-description': 'PEM 1 Not OK', 'description':'PEM 1 Not OK','type': 'Chassis', 'class': 'Major'}]
            result = chassis.get_chassis_alarm(device = self.handle,xml=0)
            self.assertEqual(type(result),list,"Expecting list but found %s"%type(result))
            logging.info("\t\tTestcase Passed")
        
        xml_string = """
                   <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
                        <multi-routing-engine-results>
                              <multi-routing-engine-item>
                                   <re-name>sfc0-re0</re-name>
                                   <alarm-information>
                                         <alarm-summary>
                                               <active-alarm-count>2</active-alarm-count>
                                         </alarm-summary>
                                         <alarm-detail>
                                               <alarm-time junos:seconds="1491965610">2017-04-11 19:53:30 PDT</alarm-time>
                                               <alarm-class>Major</alarm-class>
                                               <alarm-description>LCC 1 Major Errors</alarm-description>
                                               <alarm-short-description>LCC 1 Major Errors</alarm-short-description>
                                               <alarm-type>Chassis</alarm-type>
                                         </alarm-detail>
                                         <alarm-detail>
                                               <alarm-time junos:seconds="1491965599">2017-04-11 19:53:19 PDT</alarm-time>
                                               <alarm-class>Minor</alarm-class>
                                               <alarm-description>LCC 1 Minor Errors</alarm-description>
                                               <alarm-short-description>LCC 1 Minor Errors</alarm-short-description>
                                               <alarm-type>Chassis</alarm-type>
                                         </alarm-detail>
                                   </alarm-information>
                              </multi-routing-engine-item>
                        </multi-routing-engine-results>
                        <cli>
                             <banner></banner>
                        </cli>
                  </rpc-reply>

                   """
        alarm_info_patch              = self.create_patch("jnpr.toby.hardware.chassis.chassis.__get_alarm_info")
        alarm_info_patch.return_value = [{'alarm-information':{'alarm-summary':{'active-alarm-count':2},'alarm-detail':{'alarm-class':'Major'}}}]
        xml                           = etree.fromstring(xml_string)
        self.handle.execute_rpc       = MagicMock(return_value=Response(response=xml))  
 
        logging.info("\tTest case 2 : Without Passing xml variable(default xml is 1) & Model as TXP")
        self.handle.get_model         = MagicMock(return_value="TXP")
        result = chassis.get_chassis_alarm(device = self.handle)
        self.assertEqual(type(result),list,"Expecting list but found %s"%type(result))
        logging.info("\t\tTestcase Passed")

        with patch("jnpr.toby.hardware.chassis.chassis.__get_cid",return_value="rsd") as cid_patch:
            logging.info("\tTest case 3 : Without Passing xml variable(default xml is 1) & Model as psd")
            self.handle.get_model         = MagicMock(return_value="psd")
            result = chassis.get_chassis_alarm(device = self.handle,chassis="re",sd="rsd")
            self.assertEqual(type(result),list,"Expecting list but found %s"%type(result))
            logging.info("\t\tTestcase Passed")
     
        logging.info("\tTest case 4 : Without Passing xml variable(default xml is 1) & Model as Mx480")
        self.handle.get_model         = MagicMock(return_value="Mx480")
        result = chassis.get_chassis_alarm(device = self.handle)
        self.assertEqual(type(result),list,"Expecting list but found %s"%type(result))
        logging.info("\t\tTestcase Passed")
       
        logging.info("\tTest case 5 : Without Passing xml variable(default xml is 1) & Model as TXP")
        self.handle.get_model         = MagicMock(return_value="TXP")
        result = chassis.get_chassis_alarm(device = self.handle,chassis='sfc 0')
        self.assertEqual(type(result),list,"Expecting list but found %s"%type(result))
        logging.info("\t\tTestcase Passed")

        logging.info(" Successfully Tested")
        logging.info("\n ###########################################################")

    @patch('jnpr.toby.hardware.chassis.chassis.request_fru_online')
    @patch('jnpr.toby.hardware.chassis.chassis.request_fru_offline')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots')    
    def test_flap_spare_sib(self,slots_patch,offline_patch,online_patch):
        from jnpr.toby.hardware.chassis.chassis import flap_spare_sib
        self.handle.get_model = MagicMock(return_value='mx960')
        # ================================================================= #
        logging.info("Test case 1: Flap spare sib with "
                     "with fru slot is not null")
        param = {'fru': 'sib', 'chassis': 'scc'}
        slots_patch.return_value=[1, 2, 3]
        offline_patch.return_value=True
        online_patch.return_value=True
        self.assertEqual(flap_spare_sib(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Flap spare sib with "
                     "with fru slot is null")
        param = {'fru': 'sib', 'chassis': 'scc'}
        slots_patch.return_value=[]
        self.assertEqual(flap_spare_sib(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Flap spare sib with "
                     "with fru is not sib")
        param = {'fru': 'abc', 'chassis': 'scc'}
        self.assertEqual(flap_spare_sib(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 3 passed")

    def test_delete_chassis_control(self):
        from jnpr.toby.hardware.chassis.chassis import delete_chassis_control
        # ================================================================= #
        logging.info("Test case 1: Deactivate system processes "
                     "chassis-control configuration successful with commit")
        param = {'deactivate': 1, 'commit': 1}
        self.assertTrue(delete_chassis_control(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Deactivate system processes "
                     "chassis-control configuration successful without commit")
        param = {'deactivate': 1}
        self.assertTrue(delete_chassis_control(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Delete system processes "
                     "chassis-control configuration successful")
        param = {'commit': 1}
        self.assertTrue(delete_chassis_control(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 3 passed")

    def test_delete_chassis_redundancy(self):
        from jnpr.toby.hardware.chassis.chassis import delete_chassis_redundancy
        # ================================================================= #
        logging.info("Test case 1: deactivate the chassis redundancy "
                     "successful with commit")
        param = {'deactivate': 1, 'commit': 1}
        self.assertTrue(delete_chassis_redundancy(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: deactivate the chassis redundancy "
                     "successful without commit")
        param = {'deactivate': 1}
        self.assertTrue(delete_chassis_redundancy(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: delete the chassis redundancy successful")
        param = {'commit': 1}
        self.assertTrue(delete_chassis_redundancy(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 3 passed")

    def test_delete_chassis_manufacturing_diagnostics_mode(self):
        from jnpr.toby.hardware.chassis.chassis import delete_chassis_manufacturing_diagnostics_mode
        # ================================================================= #
        logging.info("Test case 1: deactivate chassis "
                     "manufacturing-diagnostic-mode "
                     "configuration successful with commit")
        param = {'deactivate': 1, 'commit': 1}
        self.assertTrue(
            delete_chassis_manufacturing_diagnostics_mode(self.handle, **param),
            "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: deactivate chassis "
                     "manufacturing-diagnostic-mode "
                     "configuration successful without commit")
        param = {'deactivate': 1}
        self.assertTrue(
            delete_chassis_manufacturing_diagnostics_mode(self.handle, **param),
            "Result should be True")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Delete chassis "
                     "manufacturing-diagnostic-mode "
                     "configuration successful")
        param = {'commit': 1}
        self.assertTrue(delete_chassis_manufacturing_diagnostics_mode(
            self.handle, **param), "Result should be True")
        logging.info("\t Test case 3 passed")

    def test_request_fru_switch(self):
        from jnpr.toby.hardware.chassis.chassis import request_fru_switch
        from jnpr.toby.hardware.chassis import chassis as chass
        self.handle.get_model = MagicMock(return_value='mx960')

        # ================================================================= #
        logging.info("Test case 1: Request chassis fru successful with "
                     "fru is re")
        param = {'fru': 're', 'chassis': 'scc', 'check_count': 1,
                 'check_all': True, 'check_interval': 1,
                 'check_database': True, 'check_all': True,
                 'check_interface': 0, 'check_hardware': 0, 'check_craft': 0,
                 'check_fru': 0}
        chass.get_chassis_status = MagicMock(return_value={'interface': 'up'})
        chass.check_chassis_status = MagicMock(return_value=True)
        self.handle.switch_re = MagicMock(return_value=True)
        self.assertEqual(request_fru_switch(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Request chassis fru unsuccessful with "
                     "fru is re")
        param = {'fru': 're', 'chassis': 'scc', 'check_count': 1,
                 'check_interval': 1,
                 'check_database': True,
                 'check_interface': 0, 'check_hardware': 0, 'check_craft': 0,
                 'check_fru': 0, 'method': 'acquire'}
        chass.get_chassis_status = MagicMock(return_value={'interface': 'up'})
        chass.check_chassis_status = MagicMock(return_value=False)
        self.handle.switch_re = MagicMock(return_value=True)
        self.assertEqual(request_fru_switch(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Request chassis fru successful with "
                     "fru is not re")
        param = {'fru': 'cluster', 'confirm': True,
                 'status': 'Online',
                 'check_all': True}
        chass.get_chassis_status = MagicMock(return_value={'interface': 'up'})
        chass.check_chassis_status = MagicMock(return_value=True)
        self.assertEqual(request_fru_switch(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 3 passed")
        # ================================================================= #
        logging.info("Test case 4: Request chassis fru unsuccessful with "
                     "fru is not re and check_chassis_status is False")
        param = {'fru': 'cluster', 'confirm': True, 'check_count': 1,
                 'status': 'Online', 'check_alarm': 0, 'check_memory': 0,
                 'check_all': True, 'check_interval': 1}
        chass.get_chassis_status = MagicMock(return_value={'interface': 'up'})
        chass.check_chassis_status = MagicMock(return_value=False)
        self.assertEqual(request_fru_switch(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 4 passed")

    def test_request_fru_reset(self):
        from jnpr.toby.hardware.chassis.chassis import request_fru_reset
        from jnpr.toby.hardware.chassis import chassis as chass
        self.handle.get_model = MagicMock(return_value='mx960')
        # ================================================================= #
        logging.info("Test case 1: Request chassis fru reset successful with "
                     "check_offline")
        param = {'fru': 're', 'chassis': 'scc', 'check_count': 1,
                 'check_interval': 1, 'slot': 'fpc0'}
        chass.check_fru_state = MagicMock(return_value=True)
        self.assertEqual(request_fru_reset(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Request chassis fru reset successful "
                     "without check_offline")
        param = {'fru': 're', 'chassis': 'scc', 'check_count': 1,
                 'method': 'board-reset', 'check_interval': 1,
                 'slot': ['re0', 're1'],
                 'check_offline': False}
        chass.check_fru_state = MagicMock(return_value=True)
        self.assertEqual(request_fru_reset(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Request chassis fru reset unsuccessful"
                     " with check_fru_state is False")
        param = {'fru': 're', 'chassis': 'scc', 'check_count': 1,
                 'check_interval': 1, 'slot': ['fpc0', 'fpc1']}
        chass.check_fru_state = MagicMock(return_value=False)
        self.assertEqual(request_fru_reset(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 3 passed")
        # ================================================================= #
        logging.info("Test case 4: Request chassis fru reset unsuccessful "
                     "with invalid method")
        param = {'fru': 're', 'chassis': 'scc', 'check_count': 1,
                 'method': 'fasfasf', 'check_interval': 1, 'slot': 'fpc1',
                 'check_offline': False}
        chass.check_fru_state = MagicMock(return_value=True)
        self.assertEqual(request_fru_reset(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 4 passed")
        # ================================================================= #
        logging.info("Test case 5: Request chassis fru reset unsuccessful "
                     "with check_count and check_fru_state is false")
        param = {'fru': 're', 'check_count': 1, 'check_offline': False,
                 'check_interval': 1, 'slot': 'fpc0'}
        chass.check_fru_state = MagicMock(return_value=False)
        self.assertEqual(request_fru_reset(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 5 passed")
        # ================================================================= #
        logging.info("Test case 6: Request chassis fru reset successful "
                     "without check_offline and check_count")
        param = {'fru': 're', 'method': 'board-reset', 'check_count': False,
                 'check_offline': False, 'check_interval': 1, 'slot': 'fpc0'}
        chass.check_fru_state = MagicMock(return_value=True)
        self.assertEqual(request_fru_reset(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 6 passed")

    def test_check_fru2_led(self):
        self.handle.get_model = MagicMock(return_value='MX960')
        # ================================================================= #
        logging.info("Test case 1: function return false when status is "
                     "null, green is ok and state is 'Offline")
        status = {'re': [{'status': '', 'state': 'Offline'},
                         {'status': '', 'state': 'Offline'}]}
        craft = {'re': [{'green': '', 'amber': '', 'blue': 'ok'},
                        {'green': '', 'amber': '', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle,
                               fru='re', status=status, craft=craft)
        self.assertEqual(check, False, "Result should be False")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: function return true when status is "
                     "null, amber is ok and state is 'Offline")

        status = {'re': [{'status': '', 'state': 'Offline'},
                         {'status': '', 'state': 'Offline'}]}
        craft = {'re': [{'green': 'ok', 'amber': 'ok', 'blue': 'ok'},
                        {'green': '', 'amber': 'ok', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle,
                               fru='re', status=status, craft=craft)
        self.assertEqual(check, True, "Result should be True")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info(" Test case 3: function return true when status is"
                     " null and state is 'Online'")
        status = {'re': [{'status': '', 'state': 'Online'},
                         {'status': '', 'state': 'Online'}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': 'ok'},
                        {'green': 'ok', 'amber': '', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        logging.info("\t Test case 3 passed")
        # ================================================================= #
        logging.info("Test case 4: function return false when status "
                     "is 'Master'")
        status = {'re': [{'status': 'Master', 'state': ''},
                         {'status': 'Master', 'state': ''}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': ''},
                        {'green': 'ok', 'amber': '', 'blue': ''}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        logging.info("\t Test case 4 passed")
        # ================================================================= #
        logging.info("Test case 5: function return false when "
                     "status is 'Standby'")
        status = {'re': [{'status': 'Standby', 'state': ''},
                         {'status': 'Standby', 'state': ''}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': 'ok'},
                        {'green': 'ok', 'amber': '', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, False, "Result should be False")
        logging.info("\t Test case 5 passed")
        # ================================================================= #
        logging.info("Test case 6: function return True when status is "
                     "null and state is 'Offline'")
        status = {'re': [{'status': '', 'state': 'Offline'},
                         {'status': '', 'state': 'Offline'}]}
        craft = {'re': [{'green': '', 'amber': '', 'blue': ''},
                        {'green': '', 'amber': '', 'blue': ''}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        logging.info("\t Test case 6 passed")
        # ================================================================= #
        logging.info("Test case 7: function return True when status is not"
                     "null and state is 'Online'")
        status = {'re': [{'status': '', 'state': 'Online'},
                         {'status': '', 'state': 'Online'}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': ''},
                        {'green': 'ok', 'amber': '', 'blue': ''}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        logging.info("\t Test case 7 passed")
        # ================================================================= #
        logging.info("Test case 8: function return True when status "
                     "is 'Master'")
        status = {'re': [{'status': 'Master', 'state': ''},
                         {'status': 'Master', 'state': ''}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': 'ok'},
                        {'green': '', 'amber': 'ok', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        status = {'re': [{'status': 'Master', 'state': ''},
                         {'status': 'Master', 'state': ''}]}
        craft = {'re': [{'green': 'ok', 'amber': 'ok', 'blue': 'ok'},
                        {'green': '', 'amber': 'ok', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        status = {'re': [{'status': 'Master', 'state': ''},
                         {'status': 'Master', 'state': ''}]}
        craft = {'re': [{'green': '', 'amber': 'ok', 'blue': 'ok'},
                        {'green': '', 'amber': 'ok', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        logging.info("\t Test case 8 passed")
        # ================================================================= #
        logging.info("Test case 9: function return True when status is"
                     " 'Standby'")
        status = {'re': [{'status': 'Standby', 'state': ''},
                         {'status': 'Standby', 'state': ''}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': ''},
                        {'green': 'ok', 'amber': '', 'blue': ''}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        status = {'re': [{'status': 'Standby', 'state': ''},
                         {'status': 'Standby', 'state': ''}]}
        craft = {'re': [{'green': '', 'amber': '', 'blue': ''},
                        {'green': '', 'amber': '', 'blue': ''}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        status = {'re': [{'status': 'Standby', 'state': ''},
                         {'status': 'Standby', 'state': ''}]}
        craft = {'re': [{'green': 'ok', 'amber': 'ok', 'blue': ''},
                        {'green': '', 'amber': '', 'blue': ''}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        status = {'re': [{'status': 'Standby', 'state': 'Online'},
                         {'status': 'Standby', 'state': 'Online'}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': ''},
                        {'green': 'ok', 'amber': '', 'blue': ''}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be True")
        logging.info("\t Test case 9 passed")
        # ================================================================= #
        logging.info("Test case 10: function return True when status is"
                     " 'Standby'")
        status = {'re': [{'status': 'Standby', 'state': 'Online'},
                         {'status': 'Standby', 'state': 'Online'}]}
        craft = {'re': [{'green': 'ok', 'amber': '', 'blue': 'ok'},
                        {'green': 'ok', 'amber': '', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, False, "Result should be False")

        status = {'cb': [{'status': 'Standby', 'state': 'Online'},
                         {'status': 'Standby', 'state': 'Online'}]}
        craft = {'cb': [{'green': 'ok', 'amber': 'ok', 'blue': 'ok'},
                        {'green': '', 'amber': 'ok', 'blue': 'ok'}]}
        check = check_fru2_led(self.handle, fru='cb', status=status,
                               craft=craft)
        self.assertEqual(check, True, "Result should be False")
        logging.info("\t Test case 10 passed")
        
    def test_error_arg_msg(self):
        # ================================================================= #
        logging.info("Test case 1:")
        error_arg_msg(self.handle, 'arg0', 'arg1')

    def test_sleep(self):
        # ================================================================= #
        logging.info("Test case 1: Run sleep function with multiple retry")
        sleep(self.handle, 1, "unittest", 5, "run unittest")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Run sleep with retry value is 0")
        sleep(self.handle, 0, "unittest", 5, "run unittest")
        logging.info("\t Test case 2 passed")

    def test_get_cid(self):
        # ================================================================= #
        logging.info("Testcase 1: Get cid successful with string is lcc")
        string = "lcc123-re05"
        expected = "lcc123"
        check = get_cid(self.handle, string)
        self.assertEqual(check, expected, "Get cid successful as expected")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Testcase 2: Get cid successful with string is psd")
        string = "psd123-re05"
        expected = "psd123"
        check = get_cid(self.handle, string)
        self.assertEqual(check, expected, "Get cid successful as expected")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Get cid successful with string is rsd")
        string = "rsd123-re05"
        expected = "rsd"
        check = get_cid(self.handle, string)
        self.assertEqual(check, expected, "Get cid successful as expected")
        logging.info("\t Test case 3 passed")
        # ================================================================= #
        logging.info("Test case 4: Get cid successful with string is sfc")
        string = "sfc123-re05"
        expected = "sfc123"
        check = get_cid(self.handle, string)
        self.assertEqual(check, expected, "Get cid successful as expected")
        logging.info("\t Test case 4 passed")
        # ================================================================= #
        logging.info("Test case 5: Get cid successful with string "
                     "is test123-re05")
        string = "test123-re05"
        expected = "scc"
        check = get_cid(self.handle, string)
        self.assertEqual(check, expected, "Get cid successful as expected")
        logging.info("\t Test case 5 passed")
        # ================================================================= #
        logging.info("Test case 6: Get cid successful with string is test123")
        string = "test123"
        expected = "scc"
        check = get_cid(self.handle, string)
        self.assertEqual(check, expected, "Get cid successful as expected")
        logging.info("\t Test case 6 passed")

    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_hardware')
    def test_get_psd(self, mock):
        # ================================================================= #
        logging.info("Testcase 1: Get psd unsuccessful with incorrect data")
        data = {'test1': 123, 'test2': 'testpsd'}
        mock.return_value = data
        self.assertEqual(get_psd(self.handle), False, 'Get psd unsuccessful')
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Testcase 2: Get psd successful with correct data")
        data = {'test': 123, 'psd15': 'testpsd'}
        mock.return_value = data
        self.assertEqual(get_psd(self.handle), 'psd15', 'Get psd successful')
        logging.info("\t Test case 2 passed")

    def test_get_uptime(self):
        # ================================================================= #
        logging.info("Test case 1: function return 0 when uptime "
                     "value is incorrect")
        uptime = "test 1"
        times = get_uptime(self.handle, uptime)
        expected = 0
        self.assertEqual(times, expected, 'uptime value is incorrect')
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: function return correct second value "
                     "when uptime value is correct")
        uptime = "0 hours, 0 minutes, 30 seconds"
        times = get_uptime(self.handle, uptime)
        expected = 30
        self.assertEqual(times, expected, 'uptime value is correct')

        logging.info("Test case 3:")
        uptime = "0 hours, 3 minutes, 20 seconds"
        times = get_uptime(self.handle, uptime)
        expected = 200
        self.assertEqual(times, expected, 'uptime value is correct')

        logging.info("Test case 4:")
        uptime = "1 hours, 1 minutes, 6 seconds"
        times = get_uptime(self.handle, uptime)
        expected = 3666
        self.assertEqual(times, expected, 'uptime value is correct')
        logging.info("\t Test case 2 passed")

    def test_check_enhance_fantray(self):
        from jnpr.toby.hardware.chassis.chassis import check_enhance_fantray
        # ================================================================= #
        logging.info("Test case 1: Function return true when enhance fantray "
                     "is found (1 fantray)")
        response = """
                Item             Version  Part number  Serial number     FRU model number
                Fan Tray 0       REV 08   740-031521   ACDB2712          ENH-FANTRAY-MX960-HC-S
                Fan Tray 1       REV 08   740-031521   ACDB2711          ENH-FANTRAY-MX960-HC-S
                """
        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model = MagicMock(return_value='MX960')
        param = {'ft': ['fan tray 0', 'fan tray 1']}

        result = check_enhance_fantray(self.handle, **param)
        self.assertEqual(result, True,
                         'enhance fantray is found (1 fantray)')
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Function return true when enhance fantray "
                     "is found (multiple fantrays)")
        response = """
                Item             Version  Part number  Serial number     FRU model number
                Fan Tray 0       REV 08   740-031521   ACDB2712          ENH-FANTRAY-MX960-HC-S
                Fan Tray 1       REV 08   740-031521   ACDB2711          ENH-FANTRAY-MX960-HC-S
                """
        param = {'ft': 'fan tray 0'}
        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model = MagicMock(return_value='MX960')
        result = check_enhance_fantray(self.handle, **param)

        self.assertEqual(result, True,
                         'enhance fantray is found'
                         '(multiple fantrays)')
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: function return False when enhance fantray"
                     "is not found")
        response = """
                Item             Version  Part number  Serial number     FRU model number
                Fan Tray 0       REV 08   740-031521   ACDB2712          ENH-FANTRAY-MX960-HC-S
                Fan Tray 1       REV 08   740-031521   ACDB2711          ENH-FANTRAY-MX960-HC-S
                """
        self.handle.get_model = MagicMock(return_value='MX960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        param = {}

        result = check_enhance_fantray(self.handle, **param)
        self.assertEqual(result, True, 'enhance fantray is not found')
        logging.info("\t Test case 3 passed")
        # ================================================================= #
        logging.info("Test case 4: Return false when the fan tray is not an "
                     "enhance fan tray")
        response = """
                Item             Version  Part number  Serial number     FRU model number
                Fan Tray 0       REV 08   740-031521   ACDB2712          ENH-FANTRAY-MX960-HC-S
                Fan Tray 3       REV 08   740-031521   ACDB2711          FANTRAY-MX960-HC-S
                """
        self.handle.get_model = MagicMock(return_value='MX960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        param = {'ft': ['fan tray 3']}

        result = check_enhance_fantray(self.handle, **param)
        self.assertEqual(result, False,
                         'The fan tray is not an enhance fan tray')
        logging.info("\t Test case 4 passed")
        # ================================================================= #
        logging.info("Test case 5: Return false when model is incorrect")
        self.handle.get_model = MagicMock(return_value='SRX240')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        param = {'ft': ['fan tray 3']}
        result = check_enhance_fantray(self.handle, **param)
        self.assertEqual(result, False, 'model is incorrect')
        logging.info("\t Test case 5 passed")
        # ================================================================= #
        logging.info("Test case 6: Return false when "
                     "cli command cannot be executed")
        self.handle.get_model = MagicMock(return_value='MX960')
        self.handle.cli = MagicMock(side_effect=Exception('error'))
        param = {'ft': ['fan tray 3']}
        result = check_enhance_fantray(self.handle, **param)
        self.assertEqual(result, False, 'cli command cannot be executed ')
        logging.info("\t Test case 6 passed")
        # ================================================================= #
        logging.info("Test case 7: function return false "
                     "enhance fantray is not found")
        response = """
                Item             Version  Part number  Serial number     FRU model number
                Fan Tray 0       REV 08   740-031521   ACDB2712          FANTRAY-MX960-HC-S
                Fan Tray 3       REV 08   740-031521   ACDB2711          FANTRAY-MX960-HC-S
                """
        self.handle.get_model = MagicMock(return_value='MX960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        param = {}
        result = check_enhance_fantray(self.handle, **param)
        self.assertEqual(result, False, 'enhance fantray is not found')
        logging.info("\t Test case 7 passed")
 
    def test_get_fpc_pic_spuflow(self):
        from jnpr.toby.hardware.chassis.chassis import get_fpc_pic_spuflow
        # =================================================================== #
        logging.info("Test case 1: Get fpc pic spuflow successful "
                     "with correct output response")
        xml = """
            <multi-routing-engine-results>
                <multi-routing-engine-item>
                        <re-name>node0</re-name>
                        <fpc-information>
                            <fpc>
                                <slot>0</slot>
                                <state>Online</state>
                                <description>FPC</description>
                                <pic>
                                    <pic-slot>0</pic-slot>
                                    <pic-state>Online</pic-state>
                                    <pic-type>Flow PIC</pic-type>
                                </pic>
                            </fpc>
                        </fpc-information>
                    </multi-routing-engine-item>
                    <multi-routing-engine-item>
                        <re-name>node1</re-name>
                        <fpc-information>
                            <fpc>
                                <slot>0</slot>
                                <state>Online</state>
                                <description>FPC</description>
                                <pic>
                                    <pic-slot>0</pic-slot>
                                    <pic-state>Online</pic-state>
                                    <pic-type>VSRX DPDK GE</pic-type>
                                </pic>
                            </fpc>
                        </fpc-information>
                    </multi-routing-engine-item>
                </multi-routing-engine-results>
            """
        response = etree.fromstring(xml)
        self.handle.execute_rpc = MagicMock(return_value=Response(
            response=response))
        expected_result = ['FPC0 PIC0']
        result = get_fpc_pic_spuflow(self.handle, node_id='1')
        self.assertEqual(result, expected_result,
                         'Get fpc pic spuflow successful')
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Get fpc pic spuflow unsuccessful "
                     "with incorrect output response")
        xml = """
            <multi-routing-engine-results>
            </multi-routing-engine-results>
            """
        response = etree.fromstring(xml)
        self.handle.execute_rpc = MagicMock(return_value=Response(
            response=response))
        expected_result = []
        result = get_fpc_pic_spuflow(self.handle)
        self.assertEqual(result, expected_result,
                         'Get fpc pic spuflow unsuccessful')
        logging.info("\t Test case 2 passed")

    def test_get_chassis_inventory(self):
        # =================================================================== #
        logging.info("Test case 1: Input valid chassis_inventory")
        xml = """<chassis-inventory>
        <chassis>
            <name>Chassis</name>
            <serial-number>VMX4849</serial-number>
            <description>MX960</description>
            <chassis-module>
                <name>Midplane</name>
            </chassis-module>
            <chassis-module>
                <name>Routing Engine 0</name>
                <serial-number>f6437774-94</serial-number>
                <description>RE-VMX</description>
            </chassis-module>
            <chassis-module>
                <name>Routing Engine 1</name>
                <serial-number>f643780a-94</serial-number>
                <description>RE-VMX</description>
            </chassis-module>
            <chassis-module>
                <name>CB 0</name>
                <description>VMX SCB</description>
            </chassis-module>
            <chassis-module>
                <name>CB 1</name>
                <description>VMX SCB</description>
            </chassis-module>
            <chassis-module>
                <name>FPC 0</name>
                <description>Virtual 20x1G + 4x10G FPC</description>
                <chassis-sub-module>
                    <name>CPU</name>
                    <version>Rev. 1.0</version>
                    <part-number>RIOT</part-number>
                    <serial-number>123XYZ987</serial-number>
                </chassis-sub-module>
                <chassis-sub-module>
                    <name>MIC 0</name>
                    <description>Virtual 20x 1GE(LAN) SFP</description>
                    <chassis-sub-sub-module>
                        <name>PIC 0</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>Virtual 10x 1GE(LAN) SFP</description>
                    </chassis-sub-sub-module>
                    <chassis-sub-sub-module>
                        <name>PIC 1</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>Virtual 10x 1GE(LAN) SFP</description>
                    </chassis-sub-sub-module>
                </chassis-sub-module>
                <chassis-sub-module>
                    <name>MIC 1</name>
                    <description>Virtual 4x 10GE(LAN) XFP</description>
                    <chassis-sub-sub-module>
                        <name>PIC 2</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>Virtual 2x 10GE(LAN) XFP</description>
                    </chassis-sub-sub-module>
                    <chassis-sub-sub-module>
                        <name>PIC 3</name>
                        <part-number>BUILTIN</part-number>
                        <serial-number>BUILTIN</serial-number>
                        <description>Virtual 2x 10GE(LAN) XFP</description>
                        <chassis-sub-sub-sub-module>
                            <name>PIC 3</name>
                            <part-number>BUILTIN</part-number>
                            <serial-number>BUILTIN</serial-number>
                        </chassis-sub-sub-sub-module>
                    </chassis-sub-sub-module>
                </chassis-sub-module>
            </chassis-module>
        </chassis>
        </chassis-inventory>
        """
        response = etree.fromstring(xml)
        result = get_chassis_inventory(self.handle, response)

        self.assertGreater(len(result), 0,
                           "Expected list of chassis inventory")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: slot tag does not exist")
        xml = """<fpc-information>
            <fpc>
            </fpc>
        </fpc-information>"""
        response = etree.fromstring(xml)
        result = get_chassis_inventory(self.handle, response)
        expected_result = {}
        self.assertEqual(result, expected_result,
                         "Unexpected dict of chassis inventory")
        logging.info("\t Test case 2 passed")

    def test_check_fru1_led(self):
        # =================================================================== #
        logging.info(
            "Test case 1: function return false with model is 'tx matrix'")
        self.handle.get_model = MagicMock(return_value='tx matrix')
        status = {'sib': [{'state': 'Spare'}, {'state': 'Spare'}]}
        craft = {'sib': [{'active': 'active'}, {'active': 'active'}]}
        check = check_fru1_led(self.handle,
                               fru='sib', status=status,
                               craft=craft, chas='scc')
        self.assertEqual(check, False, "Return False with model is "
                         "'tx matrix'")
        logging.info("\t Test case 1 passed")
        # =================================================================== #
        logging.info(
            "Test case 2: function return false with model is 'tx matrix'")
        self.handle.get_model = MagicMock(return_value='tx matrix')
        status = {'sib': [{'state': 'Spare'}, {'state': 'Spare'},
                          {'state': 'Spare'}, {'state': 'Spare'},
                          {'state': 'Spare'}, {'state': 'Spare'},
                          {'state': 'Spare'}, {'state': 'Spare'},
                          {'state': 'Spare'}, {'state': 'Spare'},
                          {'state': 'Spare'}, {'state': 'Spare'}]}
        craft = {'sib': [{'ok': 'ok'}, {'ok': 'ok'},
                         {'ok': 'ok'}, {'ok': 'ok'},
                         {'ok': 'ok'}, {'ok': 'ok'}]}
        check = check_fru1_led(self.handle,
                               fru='sib', status=status,
                               craft=craft, chas='scc')
        self.assertEqual(check, True, "Return True with model is "
                         "'tx matrix'")
        logging.info("\t Test case 2 passed")
        # =================================================================== #
        logging.info(
            "Test case 3: function return false with model is 'ptx5000'")
        self.handle.get_model = MagicMock(return_value='ptx5000')
        status = {'sib': [{'state': 'Online'}, {'state': 'Online'},
                          {'state': 'Online'}, {'state': 'Online'},
                          {'state': 'Online'}, {'state': 'Online'},
                          {'state': 'Online'}, {'state': 'Online'},
                          {'state': 'Online'}, {'state': 'Online'},
                          {'state': 'Online'}]}
        craft = {'sib': [{'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         {'active': 'active', 'ok': 'ok'},
                         ]}
        check = check_fru1_led(self.handle,
                               fru='sib', status=status,
                               craft=craft)
        self.assertEqual(check, False, "return false with model is 'ptx5000'")
        logging.info("\t Test case 3 passed")
        # =================================================================== #
        logging.info(
            "Test case 4: function return true with model is 'ptx5000'")
        self.handle.get_model = MagicMock(return_value='ptx5000')
        status = {'sib': [{'state': 'Check'}, {'state': 'Check'}]}
        check = check_fru1_led(self.handle,
                               fru='sib', status=status,
                               craft=craft)
        self.assertEqual(check, True, "return True with model is 'ptx5000'")
        logging.info("\t Test case 4 passed")
        # =================================================================== #
        logging.info(
            """
            Test case 5: function return false when fru is 'sib' and state is
            'check' or state is 'Online'
            """
            )
        self.handle.get_model = MagicMock(return_value='m320')
        status = {'sib': [{'state': 'Check'}, {'state': 'Check'},
                          {'state': 'Check'}, {'state': 'Check'},
                          {'state': 'Check'}, {'state': 'Check'}]}
        craft = {'sib': [{'red': 'fail'}, {'red': 'fail'},
                         {'red': 'fail'}, {'red': 'fail'},
                         {'red': 'fail'}, {'red': 'fail'}]}
        check = check_fru1_led(self.handle, fru='sib', status=status,
                               craft=craft)
        self.assertEqual(check, False, "return false when fru is 'sib' "
                         "and state is 'check' or state is 'Online'")
        logging.info("\t Test case 5 passed")
        # =================================================================== #
        logging.info(
            """
            Test case 6: function return true when fru is 'sib' and state is
            'check' or state is 'Online'
            """
            )
        self.handle.get_model = MagicMock(return_value='m320')
        status = {'sib': [{'state': 'Check'}, {'state': 'Check'},
                          {'state': 'Check'}, {'state': 'Check'},
                          {'state': 'Check'}, {'state': 'Check'}]}
        craft = {'sib': [{'green': 'ok'}, {'green': 'ok'},
                         {'green': 'ok'}, {'green': 'ok'},
                         {'green': 'ok'}, {'green': 'ok'}]}
        check = check_fru1_led(self.handle, fru='sib', status=status,
                               craft=craft)
        self.assertEqual(check, True, "return false when fru is 'sib' "
                         "and state is 'check' or state is 'Online'")
        logging.info("\t Test case 6 passed")
        # =================================================================== #
        logging.info(
            """
            Test case 7: function return false when
            comment is 'Unresponsive'
            """
            )
        self.handle.get_model = MagicMock(return_value='m320')
        status = {'re': [{'state': 'check'}, {'state': 'check'},
                         {'comment': 'Unresponsive'},
                         {'state': 'check'}, {'state': 'check'},
                         {'comment': 'Unresponsive'}]}
        craft = {'re': [{'green': 'fail'}, {'green': 'fail'},
                        {'green': 'fail'}, {'green': 'fail'}]}
        check = check_fru1_led(self.handle, fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, False, "return false when "
                         "comment is 'Unresponsive'")
        logging.info("\t Test case 7 passed")
        # =================================================================== #
        logging.info(
            """
            Test case 8: function return false when
            when comment is 'Unresponsive' and green is ok
            """
            )
        self.handle.get_model = MagicMock(return_value='m320')
        status = {'re': [{'comment': 'Unresponsive'},
                         {'comment': 'Unresponsive'},
                         {'comment': 'Unresponsive'}]}
        craft = {'re': [{'green': 'ok'}, {'green': 'ok'},
                        {'green': 'ok'}, {'green': 'ok'}]}
        check = check_fru1_led(self.handle,
                               fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, False,
                         "return false when comment is 'Unresponsive'")
        logging.info("\t Test case 8 passed")
        # =================================================================== #
        logging.info(
            """
            Test case 9: function return false when
            when comment is 'Unresponsive' and red is ok
            """
            )
        self.handle.get_model = MagicMock(return_value='m320')
        status = {'re': [{'comment': 'Unresponsive'},
                         {'comment': 'Unresponsive'},
                         {'comment': 'Unresponsive'}]}
        craft = {'re': [{'red': 'ok'}, {'red': 'ok'},
                        {'red': 'ok'}, {'red': 'ok'}]}
        check = check_fru1_led(self.handle,
                               fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True,
                         "return false when comment is 'Unresponsive'")
        logging.info("\t Test case 9 passed")
        # =================================================================== #
        logging.info(
            """
            Test case 10: function return false when red is ok
            """
            )
        self.handle.get_model = MagicMock(return_value='m320')
        status = {'re': [{'state': ''}, {'state': ''},
                         {'comment': 'Unresponsive'}]}
        craft = {'re': [{'red': 'ok'}, {'red': 'ok'},
                        {'red': 'ok'}, {'red': 'ok'}]}
        check = check_fru1_led(self.handle,
                               fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, False, "return false when red is ok")
        logging.info("\t Test case 10 passed")
        # ================================================================= #
        logging.info(
            """
            Test case 11: function return false when blue is ok
            """
            )
        status = {'re': [{'state': ''}, {'state': ''},
                         {'comment': 'Unresponsive'}]}
        craft = {'re': [{'blue': 'ok'}, {'blue': 'ok'},
                        {'blue': 'ok'}, {'blue': 'ok'}]}
        check = check_fru1_led(self.handle,
                               fru='re', status=status,
                               craft=craft)
        self.assertEqual(check, True, "return false when blue is ok")
        logging.info("\t Test case 11 passed")
        # ================================================================= #

         

    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_alarm')		
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_hardware')		
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_memory')
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_database')
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_craft')
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_interface')
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_interface')
    @patch('jnpr.toby.hardware.chassis.chassis.check_fru_state')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_list')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots')
    def test_check_chassis_status(self,slots_patch,list_patch,state_patch,interface_patch,
	            chk_int_patch,craft_patch,database_patch,memory_patch,hardware_patch,alarm_patch):
        from jnpr.toby.hardware.chassis.chassis import check_chassis_status
        self.handle.get_model = MagicMock(return_value='mx960')
        # ================================================================= #
        logging.info("Test case 1: Check chassis status successful"
                     " with check_all is true")

        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        state_patch.return_value=True
        interface_patch.return_value='xe-1/0/1'
        chk_int_patch.return_value=True
        craft_patch.return_value=True
        database_patch.return_value=True
        memory_patch.return_value=True
        hardware_patch.return_value=True
        alarm_patch.return_value=True

        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_all': 1, 'check_count': 1,
                 'check_interval': 1}
        self.assertEqual(check_chassis_status(self.handle, **param), True,
                         "Result should be True")

        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_all': 1,
                 'check_fru': 'sib',
                 'check_craft': 'craft',
                 'check_interface': 'xe-1/0/1',
                 'check_hardware': 're',
                 'check_memory': 'memory',
                 'check_database': 'database',
                 'check_alarm': ['info', 'error'],
                 'check_count': 1,
                 'check_interval': 1}

        self.assertEqual(check_chassis_status(self.handle, **param), True,
                         "Result should be True")

        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_all': 1,
                 'check_fru': 'sib',
                 'check_craft': 'craft',
                 'check_interface': 'xe-1/0/1',
                 'check_hardware': 're',
                 'check_memory': 'memory',
                 'check_database': 'database',
                 'check_alarm': {'scc': 'Chassis'},
                 'check_count': 1,
                 'check_interval': 1}

        self.assertEqual(check_chassis_status(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Check chassis status unsuccessful"
                     " with check_fru_state is False")
        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_fru': 1, 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        state_patch.return_value=False
        self.assertEqual(check_chassis_status(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Check chassis status unsuccessful"
                     " with check_fru_state is False")
        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_interface': 1, 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        chk_int_patch.return_value=False
        self.assertEqual(check_chassis_status(self.handle, **param),False,
                         "Result should be False")
        logging.info("\t Test case 3 passed")
        # ================================================================= #
        logging.info("Test case 4: Check chassis status unsuccessful"
                     " with check_chassis_craft is False")
        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_craft': 1, 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        craft_patch.return_value=False
        self.assertEqual(check_chassis_status(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 4 passed")
        # ================================================================= #
        logging.info("Test case 5: Check chassis status unsuccessful"
                     " with check_chassis_database is False")
        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_database': 1, 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        database_patch.return_value=False
        self.assertEqual(check_chassis_status(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 5 passed")
        # ================================================================= #
        logging.info("Test case 6: Check chassis status unsuccessful"
                     " with check_chassis_hardware is False")
        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_hardware': 1, 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        hardware_patch.return_value=False
        self.assertEqual(check_chassis_status(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 6 passed")
        # ================================================================= #
        logging.info("Test case 7: Check chassis status unsuccessful"
                     " with check_chassis_hardware is False")
        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_alarm': 1, 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        alarm_patch.return_value=False
        self.assertEqual(check_chassis_status(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 7 passed")
        # ================================================================= #
        logging.info("Test case 8: Check chassis status unsuccessful"
                     " with check_chassis_memory is False")
        param = {'chassis': 'scc', 'sd': 'rsd',
                 'check_memory': 1, 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        memory_patch.return_value=False
        self.assertEqual(check_chassis_status(self.handle, **param), False,
                         "Result should be False")
        logging.info("\t Test case 8 passed")
        # ================================================================= #
        logging.info("Test case 9: Check chassis status successful"
                     " without check anything")
        param = {'chassis': 'scc', 'sd': 'rsd', 'check_count': 1,
                 'check_interval': 1}
        list_patch.return_value=['sib']
        slots_patch.return_value=['re0', 're1']
        self.assertEqual(check_chassis_status(self.handle, **param), True,
                         "Result should be True")
        logging.info("\t Test case 9 passed")
    def test_get_fabric_status(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_fabric_status")

        logging.info(" Test case 1: return false for unexpected model")
        self.handle.get_model=MagicMock(return_value='m10')
        result = chassis.get_fabric_status(self.handle)
        self.assertEqual(type(result), list , '\t Failed : unexpected result for given model')
        logging.info("\t Passed : Expected result for given model, result : %s",result)  

        logging.info(" Test case 2: when uptime values present in fabric status " )
        response = """Plane   State    Uptime
 0      Online   11 days, 16 hours, 59 minutes, 16 seconds
 1      Online   11 days, 16 hours, 59 minutes, 16 seconds
 2      Online   11 days, 16 hours, 59 minutes, 16 seconds
 3      Online   11 days, 16 hours, 59 minutes, 16 seconds
"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value='m120')
        result = chassis.get_fabric_status(self.handle)
        self.assertEqual(type(result), list, '\t Failed : Unable to get the fabric uptime status')
        logging.info("\t Passed : fabric status found : %s ",result)


        logging.info(" Test case 3: for slot and for uptime 0 in response")
        response = """Plane   State    Uptime
 0      Online  
 1      Online  
 2      Online  
 3      Online 
"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value='m120')
        result = chassis.get_fabric_status(self.handle, slot=1)
        self.assertEqual(type(result), dict, '\t Failed : uptime not found')
        logging.info("\t Passed : Uptime status found : %s",result)

        logging.info(" Test case 4: for model ptx" )
        response = """FRU         State          Errors
 
SIB0        Online         None
SIB1        Online         None
SIB2        Online         None
SIB3        Online         None
SIB4        Online         None
SIB5        Online         None
SIB6        Online         None
SIB7        Empty
SIB8        Online         None
 
FPC0        Empty
FPC1        Empty
FPC2        Online         None
FPC3        Empty
FPC4        Empty
FPC5        Online         None
FPC6        Online         None
FPC7        Online         None"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value='ptx5000')
        result = chassis.get_fabric_status(self.handle)
        self.assertEqual(type(result), list, '\t Failed : Unable to get the fabric uptime status')
        logging.info("\t Passed : fabric status found : %s ",result)
		
        logging.info(" END : test_get_fabric_status")

		
    def test_get_fabric_fpc(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_fabric_fpc")
        
        logging.info("Test case 1: unexpected device model")
        self.handle.get_model=MagicMock(return_value="m120")
        result = chassis.get_fabric_fpc(self.handle,slot=1)
        self.assertEqual(type(result), dict, '\t Failed : unexpected result for given model')
        logging.info("\t Passed : Expected result for given model, result : %s",result)

        logging.info("Test case 2: Passing available slot for fpc details")
        response="""Fabric management FPC state
FPC 0
  PFE #0
      Plane 0: Plane enabled
FPC 1
  PFE #0
      Plane 0: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
FPC 12
  PFE #0
      Plane 0: Plane enabled
  PFE #1
      Plane 0: Plane enabled
"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value="srx3600")
        result = chassis.get_fabric_fpc(self.handle,slot=0)
        self.assertEqual(type(result), dict, '\t Failed : fpc details not found')
        logging.info("\t Passed : fpc details found : %s",result)

        logging.info("Test case 3: Passing unavailable slot for fpc details")
        response="""Fabric management FPC state
FPC 0
  PFE #0
      Plane 0: Plane enabled
FPC 1
  PFE #0
      Plane 0: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
FPC 12
  PFE #0
      Plane 0: Plane enabled
  PFE #1
      Plane 0: Plane enabled
"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value="srx3600")
        result = chassis.get_fabric_fpc(self.handle,slot =1)
        self.assertEqual(type(result), dict, '\t Failed : fpc details not found...')
        logging.info("\t Passed : fpc details found : %s",result)
        logging.info(" END : test_get_fabric_feb")
        
        logging.info("Test case 4: Passing unavailable slot for fpc details")
        response="""Fabric management FPC state
FPC 0
  PFE #0
      Plane 0: Plane enabled
FPC 1
  PFE #0
      Plane 0: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
FPC 12
  PFE #0
      Plane 0: Plane enabled
  PFE #1
      Plane 0: Plane enabled
"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value="srx3600")
        result = chassis.get_fabric_fpc(self.handle,slot =10)
        self.assertEqual(type(result), dict, '\t Failed : fpc details not found...')
        logging.info("\t Passed : fpc details found : %s",result)
	
        logging.info("Test case 4 : ptx model support")
        response="""Fabric management FPC state:                                  
FPC #2
    PFE #0
	SIB0_Fcore0 (plane  0)   Plane Enabled, Links OK 
	SIB0_Fcore1 (plane  1)   Plane Enabled, Links OK 
	SIB1_Fcore0 (plane  2)   Plane Enabled, Links OK 
	SIB1_Fcore1 (plane  3)   Plane Enabled, Links OK 
	SIB2_Fcore0 (plane  4)   Plane Enabled, Links OK 
	SIB2_Fcore1 (plane  5)   Plane Enabled, Links OK 
	SIB3_Fcore0 (plane  6)   Plane Enabled, Links OK 
	SIB3_Fcore1 (plane  7)   Plane Enabled, Links OK 
	SIB4_Fcore0 (plane  8)   Plane Enabled, Links OK 
	SIB4_Fcore1 (plane  9)   Plane Enabled, Links OK 
	SIB5_Fcore0 (plane 10)   Plane Enabled, Links OK 
	SIB5_Fcore1 (plane 11)   Plane Enabled, Links OK 
	SIB6_Fcore0 (plane 12)   Plane Enabled, Links OK 
	SIB6_Fcore1 (plane 13)   Plane Enabled, Links OK 
	SIB8_Fcore0 (plane 16)   Plane Enabled, Links OK 
	SIB8_Fcore1 (plane 17)   Plane Enabled, Links OK 
    PFE #1
	SIB0_Fcore0 (plane  0)   Plane Enabled, Links OK 
	SIB0_Fcore1 (plane  1)   Plane Enabled, Links OK 
	SIB1_Fcore0 (plane  2)   Plane Enabled, Links OK 
	SIB1_Fcore1 (plane  3)   Plane Enabled, Links OK 
	SIB2_Fcore0 (plane  4)   Plane Enabled, Links OK 
	SIB2_Fcore1 (plane  5)   Plane Enabled, Links OK 
        SIB3_Fcore0 (plane  6)   Plane Enabled, Links OK 
	SIB3_Fcore1 (plane  7)   Plane Enabled, Links OK 
	SIB4_Fcore0 (plane  8)   Plane Enabled, Links OK 
	SIB4_Fcore1 (plane  9)   Plane Enabled, Links OK 
	SIB5_Fcore0 (plane 10)   Plane Enabled, Links OK 
	SIB5_Fcore1 (plane 11)   Plane Enabled, Links OK 
	SIB6_Fcore0 (plane 12)   Plane Enabled, Links OK 
	SIB6_Fcore1 (plane 13)   Plane Enabled, Links OK 
	SIB8_Fcore0 (plane 16)   Plane Enabled, Links OK 
	SIB8_Fcore1 (plane 17)   Plane Enabled, Links OK 
FPC #5                                  
    PFE #0
	SIB0_Fcore0 (plane  0)   Plane Enabled, Links OK 
	SIB0_Fcore1 (plane  1)   Plane Enabled, Links OK 
	SIB1_Fcore0 (plane  2)   Plane Enabled, Links OK 
	SIB1_Fcore1 (plane  3)   Plane Enabled, Links OK 
	SIB2_Fcore0 (plane  4)   Plane Enabled, Links OK 
	SIB2_Fcore1 (plane  5)   Plane Enabled, Links OK 
	SIB3_Fcore0 (plane  6)   Plane Enabled, Links OK 
	SIB3_Fcore1 (plane  7)   Plane Enabled, Links OK 
	SIB4_Fcore0 (plane  8)   Plane Enabled, Links OK 
	SIB4_Fcore1 (plane  9)   Plane Enabled, Links OK 
	SIB5_Fcore0 (plane 10)   Plane Enabled, Links OK 
	SIB5_Fcore1 (plane 11)   Plane Enabled, Links OK 
	SIB6_Fcore0 (plane 12)   Plane Enabled, Links OK 
	SIB6_Fcore1 (plane 13)   Plane Enabled, Links OK 
	SIB8_Fcore0 (plane 16)   Plane Enabled, Links OK 
	SIB8_Fcore1 (plane 17)   Plane Enabled, Links OK 
    PFE #1
	SIB0_Fcore0 (plane  0)   Plane Enabled, Links OK 
	SIB0_Fcore1 (plane  1)   Plane Enabled, Links OK 
	SIB1_Fcore0 (plane  2)   Plane Enabled, Links OK 
	SIB1_Fcore1 (plane  3)   Plane Enabled, Links OK 
	SIB2_Fcore0 (plane  4)   Plane Enabled, Links OK 
	SIB2_Fcore1 (plane  5)   Plane Enabled, Links OK 
	SIB3_Fcore0 (plane  6)   Plane Enabled, Links OK 
        SIB3_Fcore1 (plane  7)   Plane Enabled, Links OK 
	SIB4_Fcore0 (plane  8)   Plane Enabled, Links OK 
	SIB4_Fcore1 (plane  9)   Plane Enabled, Links OK 
	SIB5_Fcore0 (plane 10)   Plane Enabled, Links OK 
	SIB5_Fcore1 (plane 11)   Plane Enabled, Links OK 
	SIB6_Fcore0 (plane 12)   Plane Enabled, Links OK 
	SIB6_Fcore1 (plane 13)   Plane Enabled, Links OK 
	SIB8_Fcore0 (plane 16)   Plane Enabled, Links OK 
	SIB8_Fcore1 (plane 17)   Plane Enabled, Links OK"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value="ptx5000")
        result = chassis.get_fabric_fpc(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : fpc details not found...')
        logging.info("\t Passed : fpc details found : %s",result)
		
        logging.info(" END : test_get_fabric_feb")		
		

    def test_get_fabric_plane(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_fabric_plane")

        logging.info("Test case 1: unexpected device model")
        self.handle.get_model=MagicMock(return_value="m10")
        result = chassis.get_fabric_plane(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : unexpected result for given model')
        logging.info("\t Passed : Expected result for given model, result : %s",result)
      
        logging.info("Test case 2: plane FEB in device model m120") 
        self.handle.get_model=MagicMock(return_value="m120")
        response= """Fabric management PLANE state
Plane 0
  Plane state: ACTIVE
      FEB 1
          PFE 0 :Links ok
      FEB 2
          PFE 0 :Links ok
      FEB 3
          PFE 0 :Links ok
Plane 1
  Plane state: ACTIVE
      FEB 0
          PFE 0 :Links ok
      FEB 2
          PFE 0 :Links ok
      FEB 3
          PFE 0 :Links ok
Plane 2
  Plane state: ACTIVE
      FEB 0
          PFE 0 :Links ok
      FEB 2
          PFE 0 :Links ok
      FEB 3
          PFE 0 :Links ok
Plane 3                                 
  Plane state: ACTIVE
      FEB 0
          PFE 0 :Links ok
      FEB 2
          PFE 0 :Links ok
      FEB 3
          PFE 0 :Links ok 
"""

        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_fabric_plane(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : Plane details not found')
        logging.info("\t Passed : Plane details found : %s",result)     

        logging.info("Test case 3: for plane FPC and slot 1") 
        self.handle.get_model=MagicMock(return_value="mx480")
        response= """Fabric management PLANE state
Plane 0
  Plane state: ACTIVE
      FPC 0
          PFE 0 :Links ok
      FPC 2
          PFE 0 :Links ok
      FPC 3
          PFE 0 :Links ok
Plane 1
  Plane state: ACTIVE
      FPC 0
          PFE 0 :Links ok
      FPC 2
          PFE 0 :Links ok
      FPC 3
          PFE 0 :Links ok
Plane 2
  Plane state: ACTIVE
      FPC 0
          PFE 0 :Links ok
      FPC 2
          PFE 0 :Links ok
      FPC 3
          PFE 0 :Links ok
Plane 3                                 
  Plane state: ACTIVE
      FPC 0
          PFE 0 :Links ok
      FPC 2
          PFE 0 :Links ok
      FPC 3
          PFE 0 :Links ok 
"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_fabric_plane(self.handle,slot =1)
        self.assertEqual(type(result), dict, '\t Failed : Plane details not found...')
        logging.info("\t Passed : Plane details found : %s",result)

        logging.info(" END : test_get_fabric_plane")


    def test_get_fabric_feb(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_fabric_feb")

        logging.info("Test case 1: unexpected device model")
        self.handle.get_model=MagicMock(return_value="m10")
        result = chassis.get_fabric_feb(self.handle,slot=1)
        self.assertEqual(type(result), dict, '\t Failed : unexpected result for given model')
        logging.info("\t Passed : Expected result for given model, result : %s",result)

        logging.info("Test case 2: feb details for existing slot")
        self.handle.get_model=MagicMock(return_value="m120")
        response="""FPC 0
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 3
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_fabric_feb(self.handle,slot=0)
        self.assertEqual(type(result), dict, '\t Failed : feb details not found')
        logging.info("\t Passed : feb details found : %s",result)

        logging.info("Test case 3: For slot which is not exist")
        response="""FPC 0
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 3
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled """

        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value="m120") 
        result = chassis.get_fabric_feb(self.handle,slot =1)
        self.assertEqual(type(result), dict, '\t Failed : feb details not found...')
        logging.info("\t Passed : feb details found : %s",result)

        logging.info(" END : test_get_fabric_feb")

    def test_get_fabric_feb(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_fabric_feb")

        logging.info("Test case 1: unexpected device model")
        self.handle.get_model=MagicMock(return_value="m10")
        result = chassis.get_fabric_feb(self.handle,slot=1)
        self.assertEqual(type(result), dict, '\t Failed : unexpected result for given model')
        logging.info("\t Passed : Expected result for given model, result : %s",result)

        logging.info("Test case 2: feb details for existing slot")
        self.handle.get_model=MagicMock(return_value="m120")
        response="""FPC 0
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 3
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_fabric_feb(self.handle,slot=0)
        self.assertEqual(type(result), dict, '\t Failed : feb details not found')
        logging.info("\t Passed : feb details found : %s",result)

        logging.info("Test case 3: For slot which is not exist")
        response="""FPC 0
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 3
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled """

        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value="m120") 
        result = chassis.get_fabric_feb(self.handle,slot =1)
        self.assertEqual(type(result), dict, '\t Failed : feb details not found...')
        logging.info("\t Passed : feb details found : %s",result)
        
        logging.info("Test case 3: For slot agument is None")
        response="""FPC 0
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 2
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled
FPC 3
  PFE #0
      Plane 0: Plane enabled
      Plane 1: Plane enabled
      Plane 2: Plane enabled
      Plane 3: Plane enabled """

        self.handle.cli = MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value="m120") 
        result = chassis.get_fabric_feb(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : feb details not found...')
        logging.info("\t Passed : feb details found : %s",result)

        logging.info(" END : test_get_fabric_feb")

    def test_get_chassis_mac(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_chassis_mac")

        logging.info("Test case 1: check for mac address details return")
        with patch('jnpr.toby.hardware.chassis.chassis.__cli_get_mac') as mac_addr_patch:
            mac_addr_patch.return_value={'public-count': '2032', 'private-count': '16', 'public-base-address': '00:19:e2:65:f8:00', 'private-base-address': '00:19:e2:65:ff:f0'}
            result = chassis.get_chassis_mac(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : Mac address not found')
        logging.info("\t Passed : Mac address Details : %s",result)
      
        logging.info(" END : test_get_chassis_mac")



    def test_cli_get_mac(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_cli_get_mac")

        logging.info("Test case 1: for show mac addresses response")
        response="""MAC address information:
  Public base address     00:19:e2:65:f8:00
  Public count            2032
  Private base address    00:19:e2:65:ff:f0
  Private count           16
"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_mac(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : No mac details found')
        logging.info("\t Passed : Mac details : %s",result)

        logging.info("Test case 2: chassis argument and no show mac addresses response")
        response="""ahkjdfakjvjabsvj"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_mac(self.handle,chassis='ssc')
        self.assertEqual(result, {}, '\t Failed : No mac details found')
        logging.info("\t Passed : Mac details : %s",result)
     
        

        logging.info(" END : test_cli_get_mac")


    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft',return_value={'display':['','|sun |','|Y:  |','|R:  |','|--------|','']})
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_alarm',return_value={'alarm':['Minor']})
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_alarm',return_value=True)
    def test_check_craft_alarm(self,check_alarm_patch,get_alarm_patch,get_craft_patch):
        logging.info("\n##################################################\n")
        logging.info(" START : test_check_craft_alarm")

        self.handle.get_model=MagicMock(return_value='t640')

        logging.info("Test case 1: No argument")
        result = chassis.check_craft_alarm(self.handle)
        self.assertEqual(result,True ,'\t Failed : craft alarms not found')
        logging.info("\t Passed : craft alarm found : %s",result)
        
        logging.info("Test case 2: Negative case for wrong craft argument ")
        craft_dict={'alarm': ['None'],
 'display': [],
 'fpc': {},
 're': {'ok': 1}}
        with patch('jnpr.toby.hardware.chassis.chassis.check_chassis_alarm',return_value=False) as check_alarm_patch:
            result = chassis.check_craft_alarm(self.handle,craft=craft_dict,check_count=3,check_interval=1)
            self.assertEqual(result, False,'\t Failed : craft alarms found')
            logging.info("\t Passed : craft alarm not found : %s",result)

        logging.info("Test case 3 : for check count sleep")
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft',return_value={}) as check_craft_patch:
            result = chassis.check_craft_alarm(self.handle,check_count=3,check_interval=1)
            self.assertEqual(result,True ,'\t Failed : craft alarms not found')
            logging.info("\t Passed : craft alarm found : %s",result)

        logging.info("Test case 4: Negative case for wrong craft argument ")
        craft_dict={'alarm': ['None'],
 'display': [],
 'fpc': {},
 're': {'ok': 1}}
        with patch('jnpr.toby.hardware.chassis.chassis.check_chassis_alarm',return_value=False) as check_alarm_patch:
            result = chassis.check_craft_alarm(self.handle,craft=craft_dict,check_count=3,alarm={'alarm':['Minor']},check_interval=1)
            self.assertEqual(result, False,'\t Failed : craft alarms found')
            logging.info("\t Passed : craft alarm not found : %s",result)
 

        logging.info(" END : check_craft_alarm")

    def test_check_craft_display(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_check_craft_alarm")

        self.handle.get_model=MagicMock(return_value='m120')
        
        logging.info("Test case 1: unexpected model")
        result = chassis.check_craft_display(self.handle,display ='ntt')
        self.assertEqual(result, True, '\t Failed : display not found')
        logging.info("\t Passed : Display check skipped for the model")

        self.handle.get_model=MagicMock(return_value='t640')

        logging.info("Test case 2: Display argument")
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft',return_value={'display':['','|sun |']}):
            result = chassis.check_craft_display(self.handle,display ='sun')
            self.assertEqual(result, True, '\t Failed : display not found')
            logging.info("\t Passed : Display found : %s"%result)
        
        logging.info("Test case 3: Display and craft argument")
        craft_dict={'display':['','|(noname)  |']}
        result = chassis.check_craft_display(self.handle,display ='',craft=craft_dict)
        self.assertEqual(result, True, '\t Failed : display not found')
        logging.info("\t Passed : Display found : %s"%result)

        logging.info("Test case 4: Negative case with wrong display argument")
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft',return_value={'display':['','|sun |']}):
            result = chassis.check_craft_display(self.handle,display ='voltaire')
            self.assertEqual(result,False ,'\t Failed : display found')
            logging.info("\t Passed : Display not found : %s"%result)

        logging.info("Test case 5: Negative case with wrong craft argument")
        craft_dict={'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
 'display': ['+--------------------+',
             '|Voltaire             |',
             '|Up: 34+14:59:59     |',
             '|                    |',
             '|0pps Load           |',
             '+--------------------+'],
 'fpc': {},
 're': {'ok': 1}}
        result = chassis.check_craft_display(self.handle,display ='ntt',craft=craft_dict)
        self.assertEqual(result, False, '\t Failed : display found')
        logging.info("\t Passed : Display not found :%s",result)

        logging.info("Test case 6: Nagative case with no display in craft")
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft',return_value={'sample':['','| sun |']}):
            result = chassis.check_craft_display(self.handle,display ='voltaire')
            self.assertEqual(result,False ,'\t Failed : display found')
            logging.info("\t Passed : Display not found :%s",result)
 
        logging.info(" END : check_craft_display")

    def test_cli_get_alarm(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_cli_get_alarm")

        logging.info("Test case 1: With no arguments")
        self.handle.get_model=MagicMock(return_value='t640')
        response="""1 alarms currently active
Alarm time               Class  Description
2017-03-23 11:33:08 IST  Major  PEM 1 Not OK
""" 
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_alarm(self.handle)
        self.assertEqual(type(result), list, '\t failed : no alarm found')
        logging.info("\t Passed : alarms found : %s"%result)


        logging.info("Test case 2: Chassis argument")
        response="""1 alarms currently active
Alarm time               Class  Description
2017-03-23 11:33:08 IST  Major  PEM 1 Not OK
"""     
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_alarm(self.handle,chassis='ssc')
        self.assertEqual(type(result), list, '\t failed : no alarm found')
        logging.info("\t Passed : alarms found : %s"%result)


        logging.info("Test case 3: nagative case for no alarm response")
        response=""" """
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_alarm(self.handle)
        self.assertEqual(type(result), list, '\t failed : alarm found')
        logging.info("\t Passed : No alarms found : %s"%result)
  
        logging.info(" END : test_cli_get_alarm")       

 
    def test_cli_get_craft(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_cli_get_craft")

        logging.info("Test case 1: No arguments")
        self.handle.get_model=MagicMock(return_value='m10i')
        response="""
Red alarm:               LED off, relay off
Yellow alarm:            LED off, relay off
Routing Engine OK LED:   On
Routing Engine fail LED: Off

FPCs     0  1
-------------
Green    *  .
Red      *  .

LCD screen:
     +--------------------+
     |voltaire            |
     |Up: 17+18:21:24     |
     |                    |
     |0pps Load           |
     +--------------------+
"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_craft(self.handle)
        self.assertEqual(type(result), dict, '\r Failed : craft details not found')
        logging.info("\t Passed : craft details found : %s"%result)

        logging.info("Test case 2: chassis argument")
        self.handle.get_model=MagicMock(return_value='t640')
        response="""FPM Display contents:
    +--------------------+
    |sun                 |
    |1 Alarm active      |
    |R: PEM 1 Not OK     |
    |                    |
    +--------------------|

Front Panel System LEDs:
Routing Engine    0    1
--------------------------
OK                *    *
Fail              .    .
Master            *    .

Front Panel Alarm Indicators:
-----------------------------
Red LED      *
Yellow LED   .
Major relay  *
Minor relay  .

Front Panel PS LEDs:
FPC    0   1   2   3   4   5   6   7
------------------------------------
Red    .   .   .   .   .   .   .   .    
Green  *   .   *   *   *   *   *   .

CB LEDs:
  CB   0   1
--------------
Amber  .   .
Green  *   *
Blue   *   .

SCG LEDs:
  SCG  0   1
--------------
Amber  .   .
Green  *   *
Blue   *   .

SIB LEDs:
  SIB  0   1   2   3   4
--------------------------
Red    .   .   .   .   .
Green  *   *   *   *   *
"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_craft(self.handle,chassis='scc')
        self.assertEqual(type(result), dict, '\t Failed : craft details not found')
        logging.info("\t Passed : craft details found :%s",result)
    
        logging.info("Test case 3: chassis argument")
        self.handle.get_model=MagicMock(return_value='t640')
        response="""FPM Display contents:
 
    1--------------------
    2sun                 
    # Alarm active      
    R: PEM 1 Not OK     
                       



Front Panel System LEDs:
Routing Engine    0    1
--------------------------
OK                *    *
Fail              .    .
Master            *    .

Front Panel Alarm Indicators:
-----------------------------
Red LED      *
Yellow LED   .
Major relay  *
Minor relay  .
             
        Front Panel PS LEDs:
FPC    0   1   2   3   4   5   6   7
------------------------------------
Red    .   .   .   .   .   .   .   .    
Green  *   .   *   *   *   *   *   .

CB LEDs:
  CB   0   1
--------------
Amber  .   .
Green  *   *
Blue   *   .

SCG LEDs:
  SCG  0   1
--------------
Amber  .   .
Green  *   *
Blue   *   .

SIB LEDs:
  SIB  0   1   2   3   4
--------------------------
Red    .   .   .   .   .
Green  *   *   *   *   *
"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_craft(self.handle,chassis='scc')
        self.assertEqual(type(result), dict, '\t Failed : craft details not found')

        logging.info(" END : test_cli_get_craft")


    def test_cli_get_ethernet(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_cli_get_ethernet")

        logging.info("Test case 1: cli response for show ethernet")
        response="""Link is good on FE port 0 connected to device: FPC0
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled

Link is good on FE port 2 connected to device: FPC2
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled

Link is good on FE port 3 connected to device: FPC3
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled

Link is good on FE port 4 connected to device: FPC4
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled

Link is good on FE port 5 connected to device: FPC5
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled
                                        
Link is good on FE port 6 connected to device: FPC6
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled

Link is good on FE port 8 connected to device: SPMB
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled

Link is good on GE port 13 connected to device: Other RE
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled

Link is good on GE port 13 connected to device: Other RE
  Speed is 100Mb
  Duplex is full
  Autonegotiate is Enabled


"""
        self.handle.get_model=MagicMock(return_value='m120')
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_ethernet(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : ethernet details not found')
        logging.info("\t Passed :ethernet details found : %s"%result)

        response=''
        self.handle.cli=MagicMock(return_value=Response(response=response))
        self.handle.get_model=MagicMock(return_value='m120')
        logging.info("Test case 2: No response")
        result = _cli_get_ethernet(self.handle)
        self.assertEqual(type(result), dict, '\t Failed : ethernet details not found')
        logging.info("Passed :ethernet details found : %s"%result)
    
        logging.info(" END : test_cli_get_ethernet")


    def test_cli_get_fru(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_cli_get_fru")

        logging.info("Test case 1: for fru value fpc")
        self.handle.get_model=MagicMock(return_value='m120')
        response="""                     Temp  CPU Utilization (%)   Memory    Utilization (%)
Slot State            (C)  Total  Interrupt      DRAM (MB) Heap     Buffer
  0  Online            29      1          0       1024        4         23
  1  Empty           
  2  Online            40      6          0       2048        4         23
  3  Online            30      1          0       256        23         47
  4  Online            40      3          0       2048        4         23
  5  Online            41      4          0       2048        4         23
  6  Online            41      4          0       2048        4         23
  7  Empty   """
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_fru(self.handle,fru='fpc')
        self.assertEqual(type(result), dict, '\t Failed : fru values not found')
        logging.info("\t Passed : fru values found : %s"%result)

        logging.info("Test case 2: for fru value sib")
        self.handle.get_model=MagicMock(return_value='t640')
        response="""Slot  State              Link errors  Destination errors  Uptime
 0    Spare                 NONE             NONE
 1    Online                NONE             NONE         2 days, 21 hours, 31 minutes, 57 seconds
 2    Online                NONE             NONE         2 days, 21 hours, 31 minutes, 57 seconds
 3    Online                NONE             NONE         2 days, 21 hours, 31 minutes, 56 seconds
 4    Online                NONE             NONE         2 days, 21 hours, 31 minutes, 56 seconds"""
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_fru(self.handle,fru='sib')
        self.assertEqual(type(result), dict, '\t Failed : fru values not found')
        logging.info("\t Passed : fru values found : %s"%result)
        
        logging.info("Test case 3: Negative test fru value fpc")
        self.handle.get_model=MagicMock(return_value='m120')
        response="""                     Temp  CPU Utilization (%)   Memory    Utilization (%)
Slot State            (C)  Total  Interrupt      DRAM (MB) Heap     Buffer
  0  Online            29      1          0       1024        4         23
  1  Empty           
  2  Online            40      6          0       2048        4         23
  3  Online            30      1          0       256        23         47
  4  Online            40      3          0       2048        4         23
  5  Online            41      4          0       2048        4         23
  6  Online            41      4          0       2048        4         23
  1  Empty   """
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_fru(self.handle,fru='fpc')
        self.assertEqual(type(result), dict, '\t Passed : fru values found')
        logging.info("\t Passed : fru values found : %s"%result)
        
        logging.info("Test case 4:Negative test for fru value fpc")
        self.handle.get_model=MagicMock(return_value='m120')
        response="""                     Temp  CPU Utilization (%)   Memory    Utilization (%)
Slot State            (C)  Total  Interrupt      DRAM (MB)     
  0  Offline            29      1          0       1024        
  1  Empty   """
        self.handle.cli=MagicMock(return_value=Response(response=response))
        result = _cli_get_fru(self.handle,fru='fpc')
        self.assertEqual(type(result), dict, '\t Passed : fru values found')
        logging.info("\t Passed : fru values found : %s"%result)

        logging.info(" END : test_cli_get_fru")


    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft')
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_hostname')
    def test_clear_craft_display(self,get_hostname_patch, get_chassis_craft_path):
        logging.info("\n##################################################\n")
        logging.info(" START : test_clear_craft_display")

        logging.info("Test case 1: Display value in craft")
        get_chassis_craft_path.return_value={'chassis': '', 'display': ['|+--------+|','|sun     |','','','','|++++++++++|']}
        get_hostname_patch.return_value = 'sun'
        result = chassis.clear_craft_display(device=self.handle)
        self.assertEqual(result, True, '\t Failed : clear craft display')
        logging.info("\t Passed : clear craft display : %s"%result)

        logging.info("Test case 2 : Negative case wrong display value")
        get_chassis_craft_path.return_value={'chassis': '', 'display': ['|+--------+|','|Voltaire     |','','','','|++++++++++|']}
        get_hostname_patch.return_value = 'sun'
        result = chassis.clear_craft_display(device=self.handle, check_count = 2)
        self.assertEqual(result, False, '\t Failed: clear craft display')
        logging.info("\t Passed : no clear craft display : %s"%result)

        logging.info(" END : test_clear_craft_display")


    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_hostname')
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_status')
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_craft')
    @patch('jnpr.toby.hardware.chassis.chassis.check_craft_display')
    @patch('jnpr.toby.hardware.chassis.chassis.check_craft_alarm')
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_alarm')
    @patch('jnpr.toby.hardware.chassis.chassis.__check_re_led')
    @patch('jnpr.toby.hardware.chassis.chassis.__check_fru1_led')
    @patch('jnpr.toby.hardware.chassis.chassis.__check_fru2_led')
    @patch('jnpr.toby.hardware.chassis.chassis.check_fru_valid')
    @patch('jnpr.toby.hardware.chassis.chassis.__check_sfm_led')
    def test_check_chassis_craft(self, mock_check_sfm_led,
                                 mock_check_fru_valid,
                                 mock_check_fru2_led,
                                 mock_check_fru1_led,
                                 mock_check_re_led,
                                 mock_check_chassis_alarm,
                                 mock_check_craft_alarm,
                                 mock_check_craft_display,
                                 mock_get_chassis_craft,
                                 mock_get_chassis_status,
                                 mock_get_chassis_hostname):
        from jnpr.toby.hardware.chassis.chassis import check_chassis_craft
        logging.info("\n##################################################\n")
        logging.info(" START : test_check_chassis-craft")
        # =================================================================== #
        logging.info("Test case 1: without craft argument")
        self.handle.get_model = MagicMock(return_value='TXP')
        # return value
        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = True
  
        mock_get_chassis_craft.return_value = {'chassis': '',
                                               'display': ['|+--------+|',
                                                           '|sun     |', '',
                                                           '', '',
                                                           '|++++----+++|']}
        mock_get_chassis_status.return_value = {'fru': 1, 'alarm': {
            'major': '1', 'minor': '1'}, 'skip_interface': 'pimd',
                                                'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'
  
        result = check_chassis_craft(self.handle)
        self.assertEqual(result, True, 'Return True without craft argument')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 2: check_craft argument is false")
        result = check_chassis_craft(self.handle, check_craft=False)
        self.assertEqual(result, True, 'Return True with check_craft is false')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 3: check_chassis-craft false with"
                     " check_craft_display is false")
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}
 
        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = False
 
        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'
 
        result = check_chassis_craft(self.handle, chassis='lcc', status=status,
                                     craft=craft_dict, check_count=2,
                                     check_interval=1)
        self.assertEqual(result, False, 'Return False with '
                         'check_craft_display is false')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 4: check_chassis-craft false with "
                     "check_craft_alarm is false")
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}
 
        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = False
        mock_check_craft_display.return_value = True
 
        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'
 
        result = check_chassis_craft(self.handle, chassis='lcc', status=status,
                                     craft=craft_dict, check_count=2,
                                     check_interval=1)
        self.assertEqual(result, False, 'Return True with with '
                         'check_craft_alarm is false')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 5: check_chassis-craft false with "
                     "check_re_led is false")
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}
 
        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = False
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = True
 
        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'
 
        result = check_chassis_craft(self.handle, chassis='lcc', status=status,
                                     craft=craft_dict, check_count=2,
                                     check_interval=1)
        self.assertEqual(result, False, 'Return True with with '
                         'check_re_led is false')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 6: check_chassis-craft false with "
                     "check_fru_valid is false")
        self.handle.get_model = MagicMock(return_value='TXP')
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}

        mock_check_fru_valid.return_value = False
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = True

        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'

        result = check_chassis_craft(self.handle, chassis='lcc', status=status,
                                     craft=craft_dict, check_count=2,
                                     check_interval=1)
        self.assertEqual(result, True, 'Return True with with '
                         'check_re_led is false')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 7: check_chassis-craft false with "
                     "check_fru1_led is false")
        self.handle.get_model = MagicMock(return_value='TXP')
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}

        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = False
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = True

        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'

        result = check_chassis_craft(self.handle, chassis='lcc', status=status,
                                     craft=craft_dict, check_count=2,
                                     check_interval=1)
        self.assertEqual(result, False, 'Return False with with '
                         'check_fru1_led is false')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 8: check_chassis-craft false with "
                     "check_fru2_led is false")
        self.handle.get_model = MagicMock(return_value='TXP')
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}

        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = False
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = True

        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'

        result = check_chassis_craft(self.handle, chassis='lcc', status=status,
                                     craft=craft_dict, check_count=2,
                                     check_interval=1)
        self.assertEqual(result, False, 'Return False with with '
                         'check_fru2_led is false')
        logging.info("\tPassed")
        # =================================================================== #
        logging.info("Test case 9: check_chassis-craft false with "
                     "check_sfm_led is false")
        self.handle.get_model = MagicMock(return_value='m160')
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}

        mock_check_sfm_led.return_value = False
        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = True

        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'

        result = check_chassis_craft(self.handle, chassis='lcc', status=status,
                                     craft=craft_dict, check_count=2,
                                     check_interval=1)
        self.assertEqual(result, False, 'Return False with with '
                         'check_sfm_led is false')
        logging.info("\tPassed")

        # =================================================================== #
        logging.info("Test case 10: check_chassis-craft false with "
                     "check_sfm_led is true")
        self.handle.get_model = MagicMock(return_value='m160')
        craft_dict = {'alarm': {'major': 0, 'minor': 0, 'red': 0, 'yellow': 0},
                      'display': [], 'fpc': {}, 're': {'ok': 1}}

        mock_check_sfm_led.return_value = True
        mock_check_fru_valid.return_value = True
        mock_check_fru2_led.return_value = True
        mock_check_fru1_led.return_value = True
        mock_check_re_led.return_value = True
        mock_check_chassis_alarm.return_value = True
        mock_check_craft_alarm.return_value = True
        mock_check_craft_display.return_value = True
        mock_get_chassis_craft.return_value = {'chassis': '',
                                               'display': ['|+--------+|',
                                                           '|sun     |', '',
                                                           '', '',
                                                           '|++++----+++|']}

        status = {'fru': 1, 'alarm': {'major': '1', 'minor': '1'},
                  'skip_interface': 'pimd', 'chassis': ''}
        mock_get_chassis_hostname.return_value = 'host'

        result = check_chassis_craft(self.handle, chassis='lcc', status=status)
        self.assertEqual(result, True, 'Return True with with '
                         'check_sfm_led is true')
        logging.info("\tPassed")

        logging.info(" END : test_check_chassis_craft")    


    def test_get_chassis_routing_engine(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_chassis_routing_engine")

        logging.info("Test case 1: No arguments")
        response="""Routing Engine status:
  Slot 0:
    Current state                  Master
    Election priority              Master (default)
    Temperature                 24 degrees C / 75 degrees F
    CPU temperature             30 degrees C / 86 degrees F
    DRAM                      8155 MB (8192 MB installed)
    Memory utilization          12 percent
    5 sec CPU utilization:
      User                       0 percent
      Background                 0 percent
      Kernel                     4 percent
      Interrupt                  1 percent
      Idle                      96 percent
    1 min CPU utilization:
      User                       0 percent
      Background                 0 percent
      Kernel                     4 percent
      Interrupt                  0 percent
      Idle                      96 percent
    5 min CPU utilization:
      User                       0 percent
      Background                 0 percent
      Kernel                     4 percent
      Interrupt                  0 percent
      Idle                      96 percent
    15 min CPU utilization:
      User                       0 percent
      Background                 0 percent
      Kernel                     4 percent
      Interrupt                  0 percent
      Idle                      96 percent
    Model                          RE-A-1800x2
    Serial ID                      9009073659
    Start time                     2017-04-09 03:13:56 PDT
    Uptime                         23 hours, 58 minutes, 44 seconds
    Last reboot reason             0x1:power cycle/failure 
    Load averages:                 1 minute   5 minute  15 minute
                                       0.01       0.04       0.00
Routing Engine status:
  Slot 1:
    Current state                  Backup
    Election priority              Backup (default)
    Temperature                 23 degrees C / 73 degrees F
    CPU temperature             27 degrees C / 80 degrees F
    DRAM                      8155 MB (8192 MB installed)
    Memory utilization          11 percent
    5 sec CPU utilization:
      User                       0 percent
      Background                 0 percent
      Kernel                     1 percent
      Interrupt                  0 percent
      Idle                      99 percent
    Model                          RE-A-1800x2
    Serial ID                      9009072174
    Start time                     2017-04-09 03:13:55 PDT
    Uptime                         2 day, 8 hours, 46 minutes
    Last reboot reason             0x1:power cycle/failure 
    Load averages:                 1 minute   5 minute  15 minute
                                       0.08       0.04       0.01
"""
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_routing_engine(self.handle)
        self.assertEqual(type(result), dict,'\t Failed : routing engine details not found ')
        logging.info("\t Passed : routing engine details : %s"%result)

        logging.info(" END : test_get_chassis_routing_engine")

    def test_get_chassis_database(self):

        from jnpr.toby.hardware.chassis.chassis import get_chassis_database	
        ######################################################################
        logging.info("Test case 1: Get db with dynamic and fpc")
        self.handle.get_model = MagicMock(return_value="mx460")
        res = '''
<chassisd-database>
   <mic>
       <type>collection</type>
   </mic>
   <fan>
       <type>collection</type>
       <fan-instance>
           <slot>0</slot>
           <query-forwarding>
               <type>string</type>
               <value>fan-info/0</value>
           </query-forwarding>
       </fan-instance>
   </fan>
   <fpm>
       <type>collection</type>
       <fpm-instance>
           <slot>a</slot>
           <query-forwarding>
               <type>string</type>
               <value>fpm-info/511</value>
           </query-forwarding>
           <serial-no>
               <type>string</type>
               <value>CAAF4560</value>
           </serial-no>
       </fpm-instance>
   </fpm>
   <fpc>
       <type>collection</type>
       <fpc-instance>
           <slot>0</slot>
           <pic>
               <type>collection</type>
               <mic-instance>
                   <slot>0</slot>
                   <query-forwarding>
                       <type>string</type>
                       <value>mic-info/736</value>
                   </query-forwarding>
               </mic-instance>
               <pic-instance>
                   <slot>a</slot>
                   <pic-applnmode>
                       <type>unsigned integer</type>
                       <value>0</value>
                   </pic-applnmode>
                   <fru-subtype>
                       <type>unsigned integer</type>
                       <value>7</value>
                   </fru-subtype>
                   <pic-prefix>
                       <type>string</type>
                       <value></value>
                   </pic-prefix>
               </pic-instance>
               <pic-instance>
                   <slot>0</slot>
                   <reason>
                       <type>unsigned integer</type>
                       <value>0</value>
                   </reason>
                   <state>
                       <type>unsigned integer</type>
                       <value>5</value>
                   </state>
                   <frutype>
                       <type>unsigned integer</type>
                       <value>6</value>
                   </frutype>
               </pic-instance>
           </pic>
           <frutype>
               <type>unsigned integer</type>
               <value>1</value>
           </frutype>
       </fpc-instance>
       <fpc-instance>
           <slot>2</slot>
           <pic>
               <type>collection</type>
               <mic-instance>
                   <slot>1</slot>
                   <frutype>
                       <type>unsigned integer</type>
                       <value>8</value>
                   </frutype>
               </mic-instance>
               <pic-instance>
                   <slot>3</slot>
                   <pic-applnmode>
                       <type>unsigned integer</type>
                       <value>0</value>
                   </pic-applnmode>
                   <frutype>
                       <type>unsigned integer</type>
                       <value>6</value>
                   </frutype>
               </pic-instance>
               <pic-instance>
                   <slot>2</slot>
                   <fpc-slot>
                       <type>unsigned integer</type>
                       <value>2</value>
                   </fpc-slot>
                   <frutype>
                       <type>unsigned integer</type>
                       <value>6</value>
                   </frutype>
               </pic-instance>
               <pic-instance>
                   <slot>0</slot>
                   <frutype>
                       <type>unsigned integer</type>
                       <value>6</value>
                   </frutype>
               </pic-instance>
           </pic>

           <frutype>
               <type>unsigned integer</type>
               <value>1</value>
           </frutype>
       </fpc-instance>
   </fpc>
</chassisd-database>
'''
        self.handle.cli = MagicMock(side_effect=[Response(response=res),
                                                 Response(response=res)])
        result = get_chassis_database(device=self.handle)
        self.assertIsInstance(result, dict, "Return is not a dict as expectation")

        ######################################################################
        logging.info("Test case 2: Get db with fru= psd and single fpc")
        self.handle.get_model = MagicMock(return_value="mx460")
        res = '''
<chassisd-database>
   <mic>
       <type>collection</type>
   </mic>
   <psd>
       <type>collection</type>
       <fan-instance>
           <slot>0</slot>
           <query-forwarding>
               <type>string</type>
               <value>fan-info/0</value>
           </query-forwarding>
       </fan-instance>
   </psd>
   <fpc>
       <type>collection</type>
       <fpc-instance>
           <slot>0</slot>
           <pic>
               <type>collection</type>
               <mic-instance>
                   <slot>0</slot>
                   <query-forwarding>
                       <type>string</type>
                       <value>mic-info/736</value>
                   </query-forwarding>
               </mic-instance>
               <pic-instance>
                   <slot>a</slot>
               </pic-instance>
           </pic>
           <frutype>
               <type>unsigned integer</type>
               <value>1</value>
           </frutype>
       </fpc-instance>
   </fpc>
</chassisd-database>
'''
        self.handle.cli = MagicMock(side_effect=[Response(response=res)])
        result = get_chassis_database(device=self.handle, dynamic=1)
        self.assertIsInstance(result, dict, "Return is not a dict as expectation")

        ######################################################################
        logging.info("Test case 3: Get db with static")
        self.handle.get_model = MagicMock(return_value="mx460")
        res = '''
<chassisd-database>
   <mic>
       <type>collection</type>
   </mic>
   <psd>
       <type>collection</type>
       <fan-instance>
           <slot>0</slot>
           <query-forwarding>
               <type>string</type>
               <value>fan-info/0</value>
           </query-forwarding>
       </fan-instance>
   </psd>
   <fpc>
       <type>collection</type>
       <fpc-instance>
           <slot>0</slot>
           <pic>
               <type>collection</type>
               <mic-instance>
                   <slot>0</slot>
                   <query-forwarding>
                       <type>string</type>
                       <value>mic-info/736</value>
                   </query-forwarding>
               </mic-instance>
               <pic-instance>
                   <slot>a</slot>
               </pic-instance>
           </pic>
           <frutype>
               <type>unsigned integer</type>
               <value>1</value>
           </frutype>
       </fpc-instance>
   </fpc>
</chassisd-database>
'''
        self.handle.cli = MagicMock(side_effect=[Response(response=res)])
        result = get_chassis_database(device=self.handle, static=1)
        self.assertIsInstance(result, dict, "Return is not a dict as expectation")
		

    @patch('jnpr.toby.hardware.chassis.chassis.__cli_get_environment',return_value={})
    @patch('jnpr.toby.hardware.chassis.chassis.__get_cid')
    def test_get_chassis_environment(self, mock_get_cid, mock_get_env_patch):
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_chassis_environment")

        logging.info(" Test case 1: if fru and if xml")
        result = chassis.get_chassis_environment(self.handle,fru='pic',xml=1)
        self.assertEqual(type(result), dict , '\t Failed : environment details not found')
        logging.info("\t Passed : environment details : %s",result)

        logging.info(" Test case 2: if not fru and  not xml")
        result = chassis.get_chassis_environment(self.handle,xml=0)
        self.assertEqual(type(result), dict , '\t Failed : environment details not found')
        logging.info("\t Passed : environment details : %s",result)

        response="""<rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
    <multi-routing-engine-results>
        
        <multi-routing-engine-item>
            
            <re-name>sfc0-re0</re-name>
            
            <environment-information>
                
                <environment-item>
                    <name>PEM 1</name>
                    <class>Temp</class>
                    <status>OK</status>
                    <temperature junos:celsius="25">25 degrees C / 77 degrees F</temperature>
                </environment-item>                
                <environment-item>
                    <name>CB 1 Exhaust B</name>
                    <class>Temp</class>
                    <status>OK</status>
                    <temperature junos:celsius="30">30 degrees C / 86 degrees F</temperature>
                </environment-item>
                
            </environment-information>
        </multi-routing-engine-item>
        
        <multi-routing-engine-item>
            
            <re-name>lcc0-re0</re-name>
            
            <environment-information>
                <environment-item>
                    <name>PEM 0</name>  
                    <class>Temp</class>
                    <status>Check</status>
                    <temperature junos:celsius="36">36 degrees C / 96 degrees F</temperature>
                </environment-item>                
                <environment-item>
                    <name>Rear Tray Third fan</name>
                    <class>Fans</class>
                    <status>OK</status>
                    <comment>Spinning at high speed</comment>
                </environment-item>                        
                <environment-item>
                    <name>CIP</name>
                    <class>Misc</class>
                    <status>OK</status>
                </environment-item>             
            </environment-information>
        </multi-routing-engine-item>
        <multi-routing-engine-item>
            
            <re-name>lcc0-re0</re-name>
            
            <environment-information>
                
                <environment-item>
                    <name>CIP</name>
                    <class>Misc</class>
                    <status>OK</status>
                </environment-item>
                <environment-item>
                    <name>SPMB 0</name>
                    <class>Misc</class>
                    <status>OK</status>
                </environment-item>               
            </environment-information>  
        </multi-routing-engine-item>
        
        <multi-routing-engine-item>
            
            <re-name>lcc1-re0</re-name>
            
            <environment-information>
                <environment-item>
                    <name>PEM 0</name>
                    <class>Temp</class>
                    <status>OK</status>
                    <temperature junos:celsius="36">36 degrees C / 96 degrees F</temperature>
                </environment-item>
                
                <environment-item>
                    <name>Rear Tray Bottom fan</name>
                    <class>Fans</class>
                    <status>OK</status>
                    <comment>Spinning at normal speed</comment>
                </environment-item>
                
            </environment-information>
        </multi-routing-engine-item>
        
    </multi-routing-engine-results>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>"""
        xml = etree.fromstring(response)
        self.handle.execute_rpc = MagicMock(return_value=Response(response=xml))

        logging.info(" Test case 3: if not fru and if xml and txp model")
        self.handle.get_model=MagicMock(return_value="txp")       
        mock_get_cid.return_value = 'lcc0'
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_environment(self.handle,xml=1)
        self.assertEqual(type(result), dict , '\t Failed : environment details not found')
        logging.info("\t Passed : environment details : %s",result)

        logging.info(" Test case 4: if not fru and if xml and psd model")
        self.handle.get_model=MagicMock(return_value="psd")
        mock_get_cid.return_value = 'psd0'
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_environment(self.handle,xml=1)
        self.assertEqual(type(result), dict , '\t Failed : environment details not found')
        logging.info("\t Passed : environment details : %s",result)
    
        logging.info(" Test case 5: if not fru and if xml and other model")
        self.handle.get_model=MagicMock(return_value="srx3600")
        mock_get_cid.return_value = 'test'
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_environment(self.handle,xml=1)
        self.assertEqual(type(result), dict , '\t Failed : environment details not found')
        logging.info("\t Passed : environment details : %s",result)
        
        logging.info(" Test case 6: if fru and without xml")
        result = chassis.get_chassis_environment(self.handle,fru='pic',xml=False)
        self.assertEqual(type(result), dict , '\t Failed : environment details not found')
        logging.info("\t Passed : environment details : %s",result)
        
        logging.info(" Test case 7: if sd  and if xml and psd model")
        self.handle.get_model=MagicMock(return_value="psd")
        mock_get_cid.return_value = 'psd0'
        self.handle.cli = MagicMock(return_value=Response(response=response))
        result = chassis.get_chassis_environment(self.handle,xml=1, sd='abc')
        self.assertEqual(type(result), dict , '\t Failed : environment details not found')
        logging.info("\t Passed : environment details : %s",result)
    
        logging.info(" END : test_get_chassis_environment")


    def test_check_spare_sib(self):
        logging.info("\n##################################################\n")
        logging.info(" START : test_check_spare_sib")

        logging.info(" Test case 1 : TXP model with no chassis argument ")
        self.handle.get_model=MagicMock(return_value="TXP")
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_list',return_value=['lcc 0','ssc 0']) as chas_list_patch:
            with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots',side_effect=[[0,1,2,3,7],[3],[0,1,2,3,7],[3]]) as fru_slots_patch:
                result = chassis.check_spare_sib(self.handle)
                self.assertEqual(result, True,'\t Failed : No spare sib found')
                logging.info("\t Passed : Spare sib found : %s",result)

        logging.info(" Test case 2: T model with chassis argument ")
        self.handle.get_model=MagicMock(return_value="t320")
        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots',side_effect=[[0,3,7],[3]]) as fru_slots_patch:
            result = chassis.check_spare_sib(self.handle,chassis='lcc 0')
            self.assertEqual(result, True , '\t Failed : No spare sib found')
            logging.info("\t Passed : Spare sib found : %s",result)

        logging.info(" Test case 3: Negative testcase for unexpected model ")
        self.handle.get_model=MagicMock(return_value="m10i")
        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots',side_effect=[[0,3,7],[3]]) as fru_slots_patch:
            result = chassis.check_spare_sib(self.handle,chassis='lcc 0')
            self.assertEqual(result, False , '\t Failed : spare sib found')
            logging.info("\t Passed : No spare sib found for unexpected model: %s",result)

        logging.info(" Test case 4: Negative testcase for model and sib_slot mismatch  ")
        self.handle.get_model=MagicMock(return_value="TXP")
        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots',side_effect=[[0,3,7,8,9],[]]) as fru_slots_patch:
            result = chassis.check_spare_sib(self.handle,chassis='lcc 0')
            self.assertEqual(result, False , '\t Failed : spare sib found')
            logging.info("\t Passed : No spare sib found for unexpected model: %s",result)

        logging.info(" Test case 5: Negative testcase for spare_sib values not list ")
        self.handle.get_model=MagicMock(return_value="TXP")
        with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots',side_effect=[1,2]) as fru_slots_patch:
            result = chassis.check_spare_sib(self.handle,chassis='lcc 0')
            self.assertEqual(result, False , '\t Failed : spare sib found')
            logging.info("\t Passed : No spare sib found for unexpected model: %s",result)

        logging.info(" Test case 6: Negative testcase with no chassis argument ")
        self.handle.get_model=MagicMock(return_value="TXP")
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_list',return_value=['lcc 0','ssc 0']) as chas_list_patch:
            with patch('jnpr.toby.hardware.chassis.chassis.get_fru_slots',side_effect=[[0,1,2,7],[3],[0,1,2,3,7],[3]]) as fru_slots_patch:
                result = chassis.check_spare_sib(self.handle)
                self.assertEqual(result, False , '\t Failed : spare sib found')
                logging.info("\t Passed : No spare sib found for unexpected model: %s",result)
        logging.info(" END : test_check_spare_sib")        

    def test_get_pic_status(self):
        from jnpr.toby.hardware.chassis.chassis import get_pic_status
        logging.info("\n##################################################\n")
        logging.info(" START : test_get_pic_status")

        response="""<rpc-reply>
            <multi-routing-engine-results>
                <multi-routing-engine-item>
                    <re-name>lcc1-re0</re-name>
                    <fpc-information>
                        <fpc>
                            <slot>0</slot>
                            <state>Online</state>
                            <description>FPC Type 4-ES</description>
                            <pic>
                                <pic-slot>0</pic-slot>
                                <pic-state>Online</pic-state>
                                <pic-type>4x 10GE (LAN/WAN) XFP</pic-type>
                            </pic>
                            <pic>               
                                <pic-slot>1</pic-slot>
                                <pic-state>Online</pic-state>
                                <pic-type>4x 10GE (LAN/WAN) XFP</pic-type>
                            </pic>
                        </fpc>
                        <fpc>
                            <slot>2</slot>
                            <state>Online</state>
                            <description>E2-FPC Type 1</description>
                            <pic>
                                <pic-slot>0</pic-slot>
                                <pic-state>Online</pic-state>
                                <pic-type>4x OC-3 IQE SONET</pic-type>
                            </pic>
                            <pic>
                                <pic-slot>1</pic-slot>
                                <pic-state>Online</pic-state>
                                <pic-type>4x OC-3 1x OC-12 SFP</pic-type>
                            </pic>
                            <pic>
                                <pic-slot>2</pic-slot>
                                <pic-state>Online</pic-state>
                                <pic-type>4x OC-3 1x OC-12 SFP</pic-type>
                            </pic>
                            <pic>
                                <pic-slot>3</pic-slot>
                                <pic-state>Online</pic-state>
                                <pic-type>4x OC-3 1x OC-12 SFP</pic-type>
                            </pic>
                        </fpc>
                        <fpc>
                            <slot>6</slot>
                            <state>Offline</state>
                            <description>FPC Type 4-ES</description>
                        </fpc>
                    </fpc-information>
                </multi-routing-engine-item>
                
            </multi-routing-engine-results>
            <cli>
                <banner></banner>
            </cli>
        </rpc-reply>
        """
        xml = etree.fromstring(response)
        self.handle.execute_rpc = MagicMock(return_value=Response(response=xml))

        logging.info("Testcase 1 : TXP model with chassis and mid argument")
        self.handle.get_model=MagicMock(return_value="TXP")
        result = get_pic_status(self.handle, chassis='lcc', mid='0')
        expected_result = {'lcc': [['Online', 'Online'], None,
                                    ['Online', 'Online', 'Online', 'Online'],
                                    None, None, None, []]}
        self.assertEqual(result, expected_result ,
                         '\t Passed : pic status is found')
        logging.info("\t Passed : pic status found %s",result)

        logging.info("Testcase 2 : TXP model with no chassis and mid argument")
        self.handle.get_model=MagicMock(return_value="TXP")
        result = get_pic_status(self.handle)
        expected_result = {'lcc1': [['Online', 'Online'], None,
                                     ['Online', 'Online', 'Online', 'Online'],
                                     None, None, None, []]}
        self.assertEqual(result, expected_result ,
                          '\t Passed : pic status is found')
        logging.info("\t Passed : pic status found %s",result)

        logging.info("Testcase 3 : psd model")
        self.handle.get_model=MagicMock(return_value="psd")
        result = get_pic_status(self.handle)
        expected_result = {'lcc1': [['Online', 'Online'], None,
                                     ['Online', 'Online', 'Online', 'Online'],
                                     None, None, None, []]}
        self.assertEqual(result, expected_result ,
                          '\t Passed : pic status is found')
        logging.info("\t Passed : pic status found %s",result)

        logging.info("Testcase 4 : psd model and sd argument")
        self.handle.get_model=MagicMock(return_value="psd")
        result = get_pic_status(self.handle, sd='lcc1')
        expected_result = [['Online', 'Online'], None,
                           ['Online', 'Online', 'Online', 'Online'],
                           None, None, None, []]
        self.assertEqual(result, expected_result,
                          '\t Passed : pic status is found')
        logging.info("\t Passed : pic status found %s",result)
   
   
        logging.info("Testcase 5 : ex model with mid argument")
        self.handle.get_model=MagicMock(return_value="ex34")
        result = get_pic_status(self.handle, mid='0')
        expected_result = {'0': [['Online', 'Online'], None,
                                 ['Online', 'Online', 'Online', 'Online'],
                                 None, None, None, []]}
        self.assertEqual(result, expected_result ,
                          '\t Passed : pic status is found')
        logging.info("\t Passed : pic status found %s",result)

        logging.info("Testcase 6 : TXP model without chassis")
        self.handle.get_model=MagicMock(return_value="TXP")
        result = get_pic_status(self.handle)
        expected_result = {'lcc1': [['Online', 'Online'], None,
                                    ['Online', 'Online', 'Online', 'Online'],
                                    None, None, None, []]}
        self.assertEqual(result, expected_result ,
                         '\t Passed : pic status is found')
        logging.info("\t Passed : pic status found %s",result)
    
        logging.info(" END : test_get_pic_status")


    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_list') 
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_alarm')
    def test_check_chassis_alarm(self, chas_alarm_patch, chas_list_patch):
        logging.info("Testing check_chassis_alarm........")
        # =================================================================== #
        logging.info(
            "Testcase1: Testing chassis alarm by passing the alarm as list " +
            "and the first list element as dictionary...")
        self.handle.get_model = MagicMock(return_value="mx480")
        alarm = [
            {'class': 'Major', 'description': 'PEM 3 Input Failure',
             'short-description': 'PEM 3 Input Failure',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 3 Not OK',
             'short-description': 'PEM 3 Not OK',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Input Failure',
             'short-description': 'PEM 2 Input Failure',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Not OK',
             'short-description': 'PEM 2 Not OK',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Minor',
             'description': 'Loss of communication with Backup RE',
             'short-description': 'Loss of communication with Backup RE',
             'time': '2017-04-09 11:34:00 PDT', 'type': 'Chassis'}]
        chas_alarm_patch.return_value = [
            {'class': 'Major', 'description': 'PEM 3 Input Failure',
             'short-description': 'PEM 3 Input Failure',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 3 Not OK',
             'short-description': 'PEM 3 Not OK',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Input Failure',
             'short-description': 'PEM 2 Input Failure',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Not OK',
             'short-description': 'PEM 2 Not OK',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Minor',
             'description': 'Loss of communication with Backup RE',
             'short-description': 'Loss of communication with Backup RE',
             'time': '2017-04-09 11:34:00 PDT', 'type': 'Chassis'}]
        count = 5
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=count, class_alarm="Major")
        self.assertEqual(result,True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase1: Testing chassis alarm by passing the alarm " +
            "PASSED...\n")
        # =================================================================== #
        logging.info(
            "Testcase3: Testing chassis alarm ............")
        self.handle.get_model = MagicMock(return_value="mx480")
        alarm = [
            {'class': 'Major', 'description': 'PEM 3 Input Failure',
             'short-description': 'PEM 3 Input Failure',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 3 Not OK',
             'short-description': 'PEM 3 Not OK',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Input Failure',
             'short-description': 'PEM 2 Input Failure',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Not OK',
             'short-description': 'PEM 2 Not OK',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Minor',
             'description': 'Loss of communication with Backup RE',
             'short-description': 'Loss of communication with Backup RE',
             'time': '2017-04-09 11:34:00 PDT', 'type': 'Chassis'}]
        chas_alarm_patch.return_value = [
            {'class': 'Major', 'description': 'PEM 3 Input Failure',
             'short-description': 'PEM 3 Input Failure',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 3 Not OK',
             'short-description': 'PEM 3 Not OK',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Input Failure',
             'short-description': 'PEM 2 Input Failure',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Not OK',
             'short-description': 'PEM 2 Not OK',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Minor',
             'description': 'Loss of communication with Backup RE',
             'short-description': 'Loss of communication with Backup RE',
             'time': '2017-04-09 11:34:00 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm,count=5, class_alarm="Minor")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase3: Testing chassis alarm PASSED...\n")
        # =================================================================== #
        logging.info(
            "Testcase4: Testing chassis alarm with incorrect alarm counts")
        alarm = [
            {'class': 'Major', 'description': 'PEM 3 Input Failure',
             'short-description': 'PEM 3 Input Failure',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 3 Not OK',
             'short-description': 'PEM 3 Not OK',
             'time': '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Input Failure',
             'short-description': 'PEM 2 Input Failure',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Major', 'description': 'PEM 2 Not OK',
             'short-description': 'PEM 2 Not OK',
             'time':  '2017-04-09 11:34:04 PDT', 'type': 'Chassis'},
            {'class': 'Minor',
             'description': 'Loss of communication with Backup RE',
             'short-description': 'Loss of communication with Backup RE',
             'time': '2017-04-09 11:34:00 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=5, class_alarm="Major")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase4: Testing chassis alarm with incorrect alarm counts " +
            "PASSED...\n")
        # =================================================================== #
        logging.info(
            "Testcase5: Testing chassis alarm for TX Matrix/TXP model...")
        self.handle.get_model = MagicMock(return_value='TXP')
        chas_list_patch.return_value = ['sfc 0', 'lcc 0', 'lcc 1']
        alarm = {
            'sfc 0': [
                {'class': 'Minor',
                 'description': 'SIB F13 11 XC HSL Link Error',
                 'short-description': 'SIB F13 11 XC HSL Link Error',
                 'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'SIB F13 8 Fault',
                 'short-description': 'SIB F13 8 Fault',
                 'time':  '2017-04-09 04:38:38 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'SIB F13 1 Absent',
                 'short-description': 'SIB F13 1 Absent',
                 'time': '2017-04-09 04:38:38 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'LCC 1 Major Errors',
                 'short-description': 'LCC 1 Major Errors',
                 'time':  '2017-04-09 04:37:39 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'Fan Tray Failure',
                 'short-description': 'Fan Tray Failure',
                 'time': '2017-04-09 04:37:23 PDT', 'type': 'Chassis'},
                {'class': 'Minor', 'description': 'LCC 1 Minor Errors',
                 'short-description': 'LCC 1 Minor Errors',
                 'time': '2017-04-09 04:37:15 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'LCC 0 Major Errors',
                 'short-description': 'LCC 0 Major Errors',
                 'time':  '2017-04-09 04:37:02 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'LCC 0 Minor Errors',
                 'short-description': 'LCC 0 Minor Errors',
                 'time':  '2017-04-09 04:37:02 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'SIB F13 12 Absent',
                 'short-description': 'SIB F13 12 Absent',
                 'time': '2017-04-09 04:36:50 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'SIB F13 9 Absent',
                 'short-description': 'SIB F13 9 Absent',
                 'time': '2017-04-09 04:36:50 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'SIB F13 7 Absent',
                 'short-description': 'SIB F13 7 Absent',
                 'time': '2017-04-09 04:36:50 PDT', 'type': 'Chassis'},
                {'class': 'Minor', 'description': 'PEM 0 Absent',
                 'short-description': 'PEM 0 Absent',
                 'time':  '2017-04-09 04:36:46 PDT', 'type': 'Chassis'}],
            'lcc 0': [
                {'class': 'Major', 'description': 'SIB 3 Fault',
                 'short-description': 'SIB 3 Fault',
                 'time':  '2017-04-09 04:38:37 PDT', 'type': 'Chassis'},
                {'class': 'Minor', 'description': 'SIB 0 Fbr Bndls',
                 'short-description': 'SIB 0 Fbr Bndls',
                 'time':  '2017-04-09 04:38:33 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'Front Top Fan Tray Failure',
                 'short-description': 'Front Top Fan Tray Failure',
                 'time': '2017-04-09 04:37:58 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'PEM 0 Input Failure',
                 'short-description': 'PEM 0 Input Failure',
                 'time':  '2017-04-09 04:37:12 PDT', 'type': 'Chassis'},
                {'class': 'Minor', 'description': 'PEM 1 Absent',
                 'short-description': 'PEM 1 Absent',
                 'time': '2017-04-09 04:37:02 PDT', 'type': 'Chassis'}],
            'lcc 1': [
                {'class': 'Minor', 'description': 'SIB 0 Fbr Bndls',
                 'short-description': 'SIB 0 Fbr Bndls',
                 'time': '2017-04-09 04:38:32 PDT', 'type': 'Chassis'},
                {'class': 'Major', 'description': 'FPC 6 Hard errors',
                 'short-description': 'FPC 6 Hard errors',
                 'time':  '2017-04-09 04:37:39 PDT', 'type': 'Chassis'},
                {'class': 'Minor', 'description': 'SIB 3 Not Online',
                 'short-description': 'SIB 3 Not Online',
                 'time':  '2017-04-09 04:37:26 PDT', 'type': 'Chassis'},
                {'class': 'Minor', 'description': 'PEM 1 Absent',
                 'short-description': 'PEM 1 Absent',
                 'time': '2017-04-09 04:37:15 PDT', 'type': 'Chassis'}]}
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=21,class_alarm="Major")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase5: Testing chassis alarm for TX Matrix/TXP model " +
            "PASSED ...")
        # =================================================================== #
        logging.info(
            "Testcase6: Testing chassis alarm for TX Matrix/TXP model " +
            "with alarm is not dict...")
        self.handle.get_model = MagicMock(return_value='TXP')
        chas_list_patch.return_value = ['sfc 0']
        alarm = [
            {'class': 'Minor',
             'description': 'SIB F13 11 XC HSL Link Error',
             'short-description': 'SIB F13 11 XC HSL Link Error',
             'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}]
        chas_alarm_patch.return_value = [
            {'class': 'Minor',
             'description': 'SIB F13 11 XC HSL Link Error',
             'short-description': 'SIB F13 11 XC HSL Link Error',
             'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1, class_alarm="Major")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase6: Testing chassis alarm for TX Matrix/TXP model " +
            "with alarm is not dict PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase7: Testing chassis alarm for TX Matrix/TXP model " +
            "with alarm is dict...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='TXP')
        alarm = {
            'sfc 0': [
                {'class': 'Minor',
                 'description': 'SIB F13 11 XC HSL Link Error',
                 'short-description': 'SIB F13 11 XC HSL Link Error',
                 'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}],
            'lcc 0': [
                {'class': 'Major', 'description': 'SIB 3 Fault',
                 'short-description': 'SIB 3 Fault',
                 'time':  '2017-04-09 04:38:37 PDT', 'type': 'Chassis'}]}
        chas_alarm_patch.return_value = [
            [{'class': 'Minor',
              'description': 'SIB F13 11 XC HSL Link Error',
              'short-description': 'SIB F13 11 XC HSL Link Error',
              'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}],
            [{'class': 'Major', 'description': 'SIB 3 Fault',
              'short-description': 'SIB 3 Fault',
              'time':  '2017-04-09 04:38:37 PDT', 'type': 'Chassis'}]]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1, class_alarm="Major")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase7: Testing chassis alarm for TX Matrix/TXP model " +
            "with alarm is dict PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase8: Testing chassis alarm for PSD model " +
            "with alarm is dict...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='PSD')
        alarm = {
            'sfc 0': [
                {'class': 'Minor',
                 'description': 'SIB F13 11 XC HSL Link Error',
                 'short-description': 'SIB F13 11 XC HSL Link Error',
                 'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}]}
        chas_alarm_patch.return_value = [
            {'class': 'Minor',
             'description': 'SIB F13 11 XC HSL Link Error',
             'short-description': 'SIB F13 11 XC HSL Link Error',
             'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1, class_alarm="Major")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase8: Testing chassis alarm for PSD model " +
            "with alarm is dict PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase9: Testing chassis alarm for PSD model " +
            "and time not in range ...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='PSD')
        alarm = {
            'sfc 0': [
                {'class': 'Minor',
                 'description': 'SIB F13 11 XC HSL Link Error',
                 'short-description': 'SIB F13 11 XC HSL Link Error',
                 'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}]}
        chas_alarm_patch.return_value = [
            {'class': 'Minor',
             'description': 'SIB F13 11 XC HSL Link Error',
             'short-description': 'SIB F13 11 XC HSL Link Error',
             'time':  '2017-04-09 07:54:49 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1, class_alarm="Major")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase9: Testing chassis alarm for PSD model " +
            "and time not in range PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase10: Testing chassis alarm for PSD model " +
            "and time not in range ...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='PSD')
        alarm = {
            'sfc 0': ['Minor', 'SIB F13 11 XC HSL Link Error',
                      'SIB F13 11 XC HSL Link Error',
                      '2017-04-09 07:54:47 PDT', 'Chassis']}
        chas_alarm_patch.return_value = [
            {'class': 'Minor',
             'description': 'SIB F13 11 XC HSL Link Error',
             'short-description': 'SIB F13 11 XC HSL Link Error',
             'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1,class_alarm="Major")
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase10: Testing chassis alarm for PSD model " +
            "and time not in range PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase11: Testing chassis alarm with alarm is string ...")
        chas_list_patch.return_value = ['sfc 0']
        self.handle.get_model = MagicMock(return_value='MX480')
        alarm = 'SIB F13 11 XC HSL Link'
        check_alarm = [
            {'class': 'Minor',
             'description': 'SIB F13 11 XC HSL Link Error',
             'short-description': 'SIB F13 11 XC HSL Link Error',
             'time':  '2017-04-09 07:54:49 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1, class_alarm="Major")
        self.assertEqual(result, False, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase11: Testing chassis alarm with alarm is string " +
            "PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase12: Testing chassis alarm with check_count = 10 ...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='MX480')
        alarm = 'SIB F13 11 XC HSL Link Error'
        chas_alarm_patch.return_value = [{
            'class': 'Minor',
            'description': 'SIB F13 11 XC HSL Link Error',
            'short-description': 'SIB F13 11 XC HSL Link Error',
            'time':  '2017-04-09 07:54:49 PDT', 'type': 'Chassis'}] * 2
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1, class_alarm="ABC", check_count=2,
            check_interval=1)
        self.assertEqual(result, False, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase12: Testing chassis with check_count = 10 PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase13: Testing chassis alarm with " +
            "check_alarm is not list ...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='PSD')
        alarm = 'SIB F13 11 XC HSL Link Error'
        chas_alarm_patch.return_value = [{
            'class': 'Minor',
            'description': 'SIB F13 11 XC HSL Link Error',
            'short-description': 'SIB F13 11 XC HSL Link Error',
            'time':  '2017-04-09 07:54:49 PDT', 'type': 'Chassis'}]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, count=1, class_alarm="ABC", check_count=1)
        self.assertEqual(result, False, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase13: Testing chassis with " +
            "check_alarm is not list PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase14: Testing chassis alarm without options ...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='TXP')
        alarm = {
            'sfc 0': [
                {'class': 'Minor',
                 'description': 'SIB F13 11 XC HSL Link Error',
                 'short-description': 'SIB F13 11 XC HSL Link Error',
                 'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}],
            'lcc 0': [
                {'class': 'Major', 'description': 'SIB 3 Fault',
                 'short-description': 'SIB 3 Fault',
                 'time':  '2017-04-09 04:38:37 PDT', 'type': 'Chassis'}]}
        chas_alarm_patch.return_value = [
            [{'class': 'Minor',
              'description': 'SIB F13 11 XC HSL Link Error',
              'short-description': 'SIB F13 11 XC HSL Link Error',
              'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}],
            [{'class': 'Major', 'description': 'SIB 3 Fault',
              'short-description': 'SIB 3 Fault',
              'time':  '2017-04-09 04:38:37 PDT', 'type': 'Chassis'}]]
        alarm= 'SIB 3 Fault'
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, class_alarm="Major", count=1)
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase14: Testing chassis alarm without options PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase15: Testing chassis alarm without count option ...")
        chas_list_patch.return_value = ['sfc 0', 'lcc 0']
        self.handle.get_model = MagicMock(return_value='TXP')
        alarm = {
            'sfc 0': [
                {'class': 'Minor',
                 'description': 'SIB F13 11 XC HSL Link Error',
                 'short-description': 'SIB F13 11 XC HSL Link Error',
                 'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}],
            'lcc 0': [
                {'class': 'Major', 'description': 'SIB 3 Fault',
                 'short-description': 'SIB 3 Fault',
                 'time':  '2017-04-09 04:38:37 PDT', 'type': 'Chassis'}]}
        chas_alarm_patch.return_value = [
            [{'class': 'Minor',
              'description': 'SIB F13 11 XC HSL Link Error',
              'short-description': 'SIB F13 11 XC HSL Link Error',
              'time':  '2017-04-09 07:54:47 PDT', 'type': 'Chassis'}],
            [{'class': 'Major', 'description': 'SIB 3 Fault',
              'short-description': 'SIB 3 Fault',
              'time':  '2017-04-09 04:38:37 PDT', 'type': 'Chassis'}]]
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, class_alarm="ABC", count=2)
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase15: Testing chassis alarm without count option " +
            "PASSED...")
        # =================================================================== #
        logging.info(
            "Testcase16: Testing chassis alarm return False...")
        self.handle.get_model = MagicMock(return_value="mx480")
        alarm = [[{
            'class': 'Minor',
            'description': 'SIB F13 11 XC HSL Link Error',
            'short-description': 'SIB F13 11 XC HSL Link Error',
            'time':  '2017-04-09 07:45:50 PDT', 'type': 'Chassis'}]]

        chas_alarm_patch.return_value = [{
            'class': 'Minor',
            'description': 'SIB F13 11 XC HSL Link Error',
            'short-description': 'SIB F13 11 XC HSL Link Error',
            'time':  '2017-04-09 07-54-49 PDT', 'type': 'Chassis'}]
        count = 1
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, class_alarm="Minor", count=count)
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase16: Testing chassis alarm return False " +
            "PASSED...\n")
        # =================================================================== #
        logging.info(
            "Testcase17: Testing chassis alarm return True...")
        self.handle.get_model = MagicMock(return_value="mx480")
        alarm = [[{
            'class': 'Minor',
            'description': 'SIB F13 11 XC HSL Link Error',
            'short-description': 'SIB F13 11 XC HSL Link Error',
            'time':  '2017-04-09 07:45:50 PDT', 'type': 'Chassis'}]]

        chas_alarm_patch.return_value = [{
            'class': 'Minor',
            'description': 'SIB F13 11 XC HSL Link Error',
            'short-description': 'SIB F13 11 XC HSL Link Error',
            'time':  '2017-04-09 07:45:50 PDT', 'type': 'Chassis'}]
        count = 1
        result = chassis.check_chassis_alarm(
            self.handle, alarm=alarm, class_alarm="Minor",count=count)
        self.assertEqual(result, True, 'Failed to check chassis alarm')
        logging.info(
            "\tTestcase17: Testing chassis alarm return True " +
            "PASSED...\n")
			
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_database')
    @patch('jnpr.toby.hardware.chassis.chassis.__check_dynamic_db')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_status')
    def test_check_chassis_database(self, mock1, mock2, mock3):
        from jnpr.toby.hardware.chassis.chassis import check_chassis_database
        self.handle.get_version = MagicMock(return_value='6.3') 
        # ================================================================= #
        logging.info("Test case 1: Check chassis database successful"
                     " with")
        param = {'fru': ['fan'], 'check_count': 2, 'check_interval': 1}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [{'state': 'Online'}, {'state': 'Online'}]
        mock2.return_value = True

        mock3.return_value = {"dynamic": {"fan": ['1', '2']}}
        self.assertEqual(check_chassis_database(self.handle, **param), True,
                         "Result should be True")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 2: Check chassis database successful"
                     " with check_all is true")
        param = {'fru': ['fan'], 'dynamic': 1, 'check_interval': 1}
        response = "Count: 0 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.get_version = MagicMock(return_value='3.3')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = {'memory-dram-size': '2048',
                              'memory-heap-utilization': '13',
                              'memory-buffer-utilization': '14',
                              'state': 'Online', 'temperature': '42',
                              'cpu-15min-avg': '10', 'cpu-5min-avg': '12',
                              'cpu-total': '13', 'cpu-1min-avg': '12',
                              'cpu-interrupt': '0'}
        mock2.return_value = True
        mock3.return_value = {"dynamic": {"fan": ['1', '2']}}
        self.assertEqual(check_chassis_database(self.handle, **param), False,
                         "Result should be False")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 3: Check chassis database True"
                     " with model is TX Matrix")
        param = {'fru': 'fan', 'dynamic': 1, 'check_interval': 1}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='TX Matrix')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [{'memory-dram-size': '2048',
                               'memory-heap-utilization': '13',
                               'memory-buffer-utilization': '14',
                               'state': 'Online', 'temperature': '42',
                               'cpu-15min-avg': '10', 'cpu-5min-avg': '12',
                               'cpu-total': '13', 'cpu-1min-avg': '12',
                               'cpu-interrupt': '0'}]
        mock2.return_value = True
        mock3.return_value = {"dynamic": {"fan": ['1', '2']}}
        self.assertEqual(check_chassis_database(self.handle, **param), True,
                         "Result should be True")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 4: Check chassis database True"
                     " with model is TX Matrix")
        param = {'fru': ['sib'], 'dynamic': 1, 'check_interval': 1}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='TX Matrix')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [{'memory-dram-size': '2048',
                               'memory-heap-utilization': '13',
                               'memory-buffer-utilization': '14',
                               'state': 'Online', 'temperature': '42',
                               'cpu-15min-avg': '10', 'cpu-5min-avg': '12',
                               'cpu-total': '13', 'cpu-1min-avg': '12',
                               'cpu-interrupt': '0'}]
        mock2.return_value = True
        mock3.return_value = {"dynamic": {"sib": ['1', '2']}}
        self.assertEqual(check_chassis_database(self.handle, **param), True,
                         "Result should be True")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 5: Check chassis database unsuccessful"
                     " with number of fru_dynamic_db greater than "
                     "number of fru_status")
        param = {'fru': 'sib', 'check_count': 1, 'check_interval': 1}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
       	self.handle.get_version = MagicMock(return_value='3.3')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [{'state': 'Online'}]
        mock2.return_value = True
        mock3.return_value = {"dynamic": {"sib": ['1', '2']}}
        self.assertEqual(check_chassis_database(self.handle, **param), False,
                         "Result should be False")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 6: Check chassis database successful")
        param = {'fru': ['fan'], 'static': 1, 'dynamic': 1, 'check_count': 1,
                 'check_interval': 1}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [{'memory-dram-size': '2048',
                               'memory-heap-utilization': '13',
                               'memory-buffer-utilization': '14',
                               'state': 'Online', 'temperature': '42',
                               'cpu-15min-avg': '10', 'cpu-5min-avg': '12',
                               'cpu-total': '13', 'cpu-1min-avg': '12',
                               'cpu-interrupt': '0'}]
        mock2.return_value = True
        mock3.return_value = {"dynamic": {"fan": ['1', '2']}}
        self.assertEqual(check_chassis_database(self.handle, **param), True,
                         "Result should be True")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 7: Check chassis database unsuccessful"
                     " with chassis_database is not a list")
        param = {'fru': ['fan'], 'static': 1, 'dynamic': 1, 'check_count': 1,
                 'check_interval': 1}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [{'state': 'Online'}]
        mock2.return_value = True
        mock3.return_value = {"dynamic": {"fan": 'abc'}}
        self.assertEqual(check_chassis_database(self.handle, **param), False,
                         "Result should be False")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 8: Check chassis database unsuccessful"
                     " with fru_status is not a list")
        param = {'fru': 'sib', 'check_count': 1, 'check_interval': 1}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = 'abc'
        mock2.return_value = True
        mock3.return_value = {"dynamic": {"sib": ['1']}}
        self.assertEqual(check_chassis_database(self.handle, **param), False,
                         "Result should be False")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 9: Check unsuccessful with wrong get_chassis_database")
        param = {'fru': 'fan', 'check_interval': 1, 'check_count': 2}
        response = "Count: 1 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = 'abc'
        mock2.return_value = True
        mock3.return_value = []
        self.assertEqual(check_chassis_database(self.handle, **param), False,
                         "Result should be false with wrong get_chassis_database")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 10: Check with fru=fan and wrong response")
        param = {'fru': 'fan', 'check_interval': 1, 'check_count': 1,
                 'static': 1, 'dynamic': {"fan": {"state": 'OK'}}}
        response = "Test"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = 'abc'
        mock2.return_value = True
        mock3.return_value = []
        self.assertEqual(check_chassis_database(self.handle, **param), True,
                         "Result should be True")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 11: Check with fru=fan and Count = 0")
        param = {'fru': 'fan', 'check_interval': 1, 'check_count': 1,
                 'static': 1, 'dynamic': {"fan": {"state": 'OK'}}}
        response = "Count: 0 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = 'abc'
        mock2.return_value = True
        mock3.return_value = []
        self.assertEqual(check_chassis_database(self.handle, **param), True,
                         "Result should be True")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 12: Check with return of list get_fru_status and false __check_dynamic_db")
        param = {'fru': 'fpc', 'check_interval': 1, 'check_count': 1,
                 'static': 1, 'dynamic': {"fpc": {"state": 'OK'}}}
        response = "Count: 0 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [1, 2]
        mock2.return_value = False
        mock3.return_value = []
        self.assertEqual(check_chassis_database(self.handle, **param), False,
                         "Result should be False")
        logging.info("\tPassed")

        # ================================================================= #
        logging.info("Test case 13: Check with return of list get_fru_status and true __check_dynamic_db")
        param = {'fru': 'fpc', 'check_interval': 1, 'check_count': 1,
                 'static': 1, 'dynamic': {"fpc": {"state": 'OK'}}}
        response = "Count: 0 lines"
        self.handle.get_model = MagicMock(return_value='mx960')
        self.handle.cli = MagicMock(return_value=Response(response=response))
        mock1.return_value = [1, 2]
        mock2.return_value = True
        mock3.return_value = []
        self.assertEqual(check_chassis_database(self.handle, **param), True,
                         "Result should be TRue")
        logging.info("\tPassed")
	
    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_status')
    def test_check_fru_state(self, mock1):
        from jnpr.toby.hardware.chassis.chassis import check_fru_state
        ######################################################################
        logging.info("Test case 1: Check with chassis=scc and fru=fpc")
        self.handle.get_model = MagicMock(return_value="mx320")
        result = check_fru_state(device=self.handle, chassis='scc', fru='fpc')
        self.assertTrue(result, "Cheching failed with chassis=scc and fru=fpc")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Checking with model = TXP and dict slot")
        mock1.return_value = [{'state' : 'ON'}]
        self.handle.get_model = MagicMock(return_value="TXP")
        result = check_fru_state(device=self.handle, fru='fpc',
                                 slot={'1':1, '2':1},
                                 state={'1':'ON', '2': 'ON'})
        self.assertTrue(result, "Cheching failed with model = TXP and dict slot")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Checking with model = TXP and dict slot return False")
        mock1.return_value = [{'state' : 'ON'}]
        self.handle.get_model = MagicMock(return_value="TXP")
        result = check_fru_state(device=self.handle, fru='fpc',
                                 slot={'1':1, '2':1},
                                 state={'1':'ON', '2': 'OFF'})
        self.assertFalse(result, "Cheching failed when current state != state")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Checking with model = TXP and not dict slot")
        mock1.return_value = [{'state' : 'ON'}]
        self.handle.get_model = MagicMock(return_value="TXP")
        result = check_fru_state(device=self.handle, fru='fpc',
                                 slot=1,
                                 state={'1':'ON', '2': 'OFF'})
        self.assertFalse(result, "Cheching failed with model = TXP and not dict slot")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Checking with model = TXP and dict slot and not dict state")
        mock1.return_value = [{'state' : 'ON'}]
        self.handle.get_model = MagicMock(return_value="TXP")
        result = check_fru_state(device=self.handle, fru='fpc',
                                 slot={'1':1, '2':1},
                                 state='ON')
        self.assertTrue(result, "Cheching failed with model = TXP and dict slot and not dict state")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Checking with list fru")
        mock1.return_value = [{'state' : 'ON'}]
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru=['fpc', 'pem'],
                                 chassis='scc',
                                 slot={'fpc':1, 'pem':2},
                                 state='ON')
        self.assertTrue(result, "Cheching failed with list fru")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Checking with list fru and return false")
        mock1.return_value = [{'state' : 'OFF'}]
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru=['fpc', 'pem'],
                                 chassis='scc',
                                 slot={'fpc':1, 'pem':2},
                                 state='ON')
        self.assertFalse(result, "Cheching failed with list fru and return false")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Checking with fru= pic and without state")
        mock1.return_value = [{'state' : 'ON'}]
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pic',
                                 chassis='sss', slot=[[1, 2],[3, 4]])
        self.assertFalse(result, "Wrong return when missed state")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Checking with fru= pic")
        mock1.return_value = [{'state' : 'ON'}]
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pic',
                                 chassis='sss', slot=[[1, 2],[3, 4]],
                                 state='ON')
        self.assertTrue(result, "checking failed with fru=pic")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 10: Checking with fru= pic and failed state")
        mock1.return_value = [{'state' : 'OFF'}]
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pic',
                                 chassis='sss', slot=[[1, 2],[3, 4]],
                                 state='ON')
        self.assertFalse(result, "checking failed with fru=pic")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 11: Checking with fru= pic and not list slot[0]")
        mock1.return_value = [{'state': 'ON'}]
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pic',
                                 chassis='sss', slot=[[1,2]],
                                 state={'pic': {'1': {'state': 'ON'}, '2': 'OFF'}})
        self.assertFalse(result, "checking failed with fru=pic and not list slot[0]")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 12: Checking with fru= pic and not list slot[0] and not dict state")
        mock1.return_value = [{'state': 'OFF'}]
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pic',
                                 chassis='sss', slot=[[1, 2]],
                                 state='ON')
        self.assertFalse(result, "checking failed with fru=pic and not list slot[0] and not dict state")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 13: Checking with not fru= pic and list slot")
        mock1.return_value = {'1': {'state': 'ON'}}
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pem',
                                 slot=[1], state={'pem': {'1': {'state': 'ON'}}})
        self.assertTrue(result, "checking failed with  fru=pic and list slot")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 14: Checking with not fru= pic and list slot and failed state")
        mock1.return_value = {'1': {'state': 'OFF'}}
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pem',
                                 slot=[1], state={'pem': {'1': {'state': 'ON'}}})
        self.assertFalse(result, "checking failed with fru=pic and list slot and failed state")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 15: Checking with not fru= pic and list slot and not dict state")
        mock1.return_value = {'1': {'state': 'OFF'}}
        self.handle.get_model = MagicMock(return_value="mx460")
        result = check_fru_state(device=self.handle, fru='pem',
                                 slot=[1], state="ON")
        self.assertFalse(result, "checking failed with fru=pic and list slot and not dict state")
        logging.info("\tPassed")

    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_environment')
    @patch('jnpr.toby.hardware.chassis.chassis.get_pic_status')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fabric_status')
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_list')
    @patch('jnpr.toby.hardware.chassis.chassis.get_test_frus')
	
    def test_get_fru_status(self, mock1, mock2, mock3, mock4, mock5):
        from jnpr.toby.hardware.chassis.chassis import get_fru_status
        ######################################################################
        logging.info("Test case 1: Get staus with fru=re")
        mock1.return_value = True
        self.handle.get_model = MagicMock(return_value="vx")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <route-engine-information>
        <route-engine>
            <slot>0</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </route-engine>
    </route-engine-information>
    <route-engine-information>
        <route-engine>
            <slot>1</slot>
            <mastership-state>local Chassis test</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </route-engine>
    </route-engine-information>
    <route-engine-information>
        <route-engine>
            <slot>2</slot>
            <mastership-state>Protocol test</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </route-engine>
    </route-engine-information>
</rpc-reply>

'''
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, fru='re',
                                mid="mid")
        self.assertIsInstance(result, list, "Get fru status failed with fru=re")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Get staus with fru=spmb")
        mock1.return_value = True
        self.handle.get_model = MagicMock(return_value="mx86")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <spmb-information>
        <spmb>
            <state>Online - Standby</state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </spmb>
    </spmb-information>
    <spmb-information>
        <spmb>
            <slot>1</slot>
            <state>Online</state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </spmb>
    </spmb-information>
    <spmb-information>
        <spmb>
            <slot>2</slot>
            <state>Offline</state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
            <load-average-one>0.20</load-average-one>
            <load-average-five>0.18</load-average-five>
            <load-average-fifteen>0.16</load-average-fifteen>
        </spmb>
    </spmb-information>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, chassis="cc", fru='spmb')
        self.assertIsInstance(result, list, "Get fru status failed with fru=spmb")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Get staus with fru=sib")
        mock1.return_value = True
        self.handle.get_model = MagicMock(return_value="TX Matrix")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <multi-routing-engine-results>
        <multi-routing-engine-item>
            <slot>0</slot>
            <state>Online - Standby</state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, chassis="cc", fru='sib')
        self.assertIsInstance(result, list, "Get fru status failed with fru=sib")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Get staus with fru= sfm and model = psd ")
        mock1.return_value = True
        self.handle.get_model = MagicMock(return_value="psd")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <multi-routing-engine-results>
        <multi-routing-engine-item>
            <slot>0</slot>
            <state>Online - Standby</state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, fru='sfm')
        self.assertIsInstance(result, list, "Get fru status failed with fru= sfm and model = psd ")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Get staus with mid and model = ex23 ")
        mock1.return_value = True
        self.handle.get_model = MagicMock(return_value="ex23")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <multi-routing-engine-results>
        <multi-routing-engine-item>
            <slot>0</slot>
            <state>Online - Standby</state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, fru='cfeb', mid="mid")
        self.assertIsInstance(result, list, "Get fru status failed with mid and model = ex23")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Get staus with list fru and slot ")
        mock1.return_value = True
        self.handle.get_model = MagicMock(return_value="vx123")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <sfm-information>
        <sfm>
            <slot>0</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </sfm>
    </sfm-information>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res),
                                                         Response(response=res)])
        result = get_fru_status(device=self.handle, chassis="scc",
                                fru=['sfm', 'scg'], slot=1)
        self.assertIsInstance(result, dict, "Get fru status failed with list fru and slot")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Get status with model = TXP and not chassis and fru != lcc ")
        mock2.return_value = ['scc']
        self.handle.get_model = MagicMock(return_value="TXP")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <sfm-information>
        <sfm>
            <slot>0</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </sfm>
    </sfm-information>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res),
                                                         Response(response=res)])
        result = get_fru_status(device=self.handle, fru='sfm', slot=1)
        self.assertIsInstance(result, list, "Get fru status failed with model = TXP and not chassis and fru != lcc")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Get status with model = TXP and not chassis and fru = pic")
        mock2.return_value = ['scc']
        self.handle.get_model = MagicMock(return_value="TXP")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <sfm-information>
        <sfm>
            <slot>0</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </sfm>
    </sfm-information>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res),
                                                         Response(response=res)])
        result = get_fru_status(device=self.handle, fru='pic', slot=1)
        self.assertIsInstance(result, list, "Get fru status failed with model = TXP and not chassis and fru = pic")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Get status with fru = fabric plane")
        mock3.return_value = []
        self.handle.get_model = MagicMock(return_value="vx30")
        self.handle.get_version = MagicMock(return_value="7.0")
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response="")])
        result = get_fru_status(device=self.handle, fru='fabric plane', slot=1)
        self.assertIsInstance(result, list, "Get fru status failed with fru = fabric plane")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 10: Get status with fru = pic and slot")
        mock3.return_value = []
        self.handle.get_model = MagicMock(return_value="TXP")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <pic-detail>
        <multi-routing-engine-results>
        <multi-routing-engine-item>
            <slot>0</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </multi-routing-engine-item>
        </multi-routing-engine-results>
    </pic-detail>
    <pic-detail>
        <multi-routing-engine-results>
        <multi-routing-engine-item>
            <slot>1</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </multi-routing-engine-item>
        </multi-routing-engine-results>
    </pic-detail>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, fru='pic', slot=[1, 2],
                                chassis="chassis")
        self.assertIsInstance(result, list, "Get fru status failed with fru = pic and slot")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 11: Get status with fru = pic and slot and model = ex43")
        mock3.return_value = []
        self.handle.get_model = MagicMock(return_value="ex43")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <pic-detail>
        <multi-routing-engine-results>
        <multi-routing-engine-item>
            <slot>0</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </multi-routing-engine-item>
        </multi-routing-engine-results>
    </pic-detail>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, fru='pic', slot=[1, 2],
                                mid="mid")
        self.assertIsInstance(result, list, "Get fru status failed with fru = pic and slot and model = ex43")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 12: Get status with fru = pic and without slot")
        mock4.return_value = {'mid': [1, [2,3]]}
        self.handle.get_model = MagicMock(return_value="ex43")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <pic-detail>
        <multi-routing-engine-results>
        <multi-routing-engine-item>
            <slot>0</slot>
            <mastership-state>master</mastership-state>
            <mastership-priority>master (default)</mastership-priority>
            <memory-dram-size>1023</memory-dram-size>
        </multi-routing-engine-item>
        </multi-routing-engine-results>
    </pic-detail>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res),
                                                         Response(response=res)])
        result = get_fru_status(device=self.handle, fru='pic',
                                mid="mid")
        self.assertIsInstance(result, list, "Get fru status failed with fru = pic and slot and model = ex43")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 13: Get status with fru = pic and without slot and mid not in pic_status")
        mock4.return_value = {'mid1': [1, [2,3]]}
        self.handle.get_model = MagicMock(return_value="ex43")
        self.handle.get_version = MagicMock(return_value="7.0")
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response="")])
        result = get_fru_status(device=self.handle, fru='pic',
                                mid="mid")
        self.assertEqual(result, [], "Get fru status failed with mid not in pic_status")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 14: Get status with fru = scg and chassis=scc")
        result = get_fru_status(device=self.handle, fru='scg', chassis='scc')
        self.assertEqual(result, [], "Get fru status failed with fru = scg and chassis=scc")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 15: Get status with fru = pem")
        mock5.return_value = {'pem 0': {'status': 'OK'},
                              'pem 1': {'status': 'FA'}}
        self.handle.get_model = MagicMock(return_value="m20")
        result = get_fru_status(device=self.handle, fru='pem')
        self.assertIsInstance(result, list, "Get fru status failed with fru = pem")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 16: Get status with fru != fan")
        mock5.return_value = {}
        result = get_fru_status(device=self.handle, fru='fan1')
        self.assertEqual(result, {}, "Get fru status failed with fru != fan")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 17: Get status with fru = fan")
        result = get_fru_status(device=self.handle, fru='fan')
        self.assertEqual(result, [], "Get fru status failed with fru = fan")
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 18: Get staus with fru=sib")
        mock1.return_value = True
        self.handle.get_model = MagicMock(return_value="ptx5000")
        self.handle.get_version = MagicMock(return_value="7.0")
        xml = '''
<rpc-reply>
    <sib-information>
        <sib>
            <slot>0</slot>
            <state>Online</state>
            <sib-link-state>Active</sib-link-state>
            <sib-link-errors>None</sib-link-errors>
        </sib>
</sib-information>
    <cli>
        <banner></banner>
    </cli>
</rpc-reply>
'''

        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock()
        self.handle.execute_rpc = MagicMock(side_effect=[Response(response=res)])
        result = get_fru_status(device=self.handle, fru='sib')
        self.assertIsInstance(result, list, "Get fru status failed with fru=sib")
        logging.info("\tPassed")
                                                                                       

    @patch('jnpr.toby.hardware.chassis.chassis.get_fabric_plane')
    @patch('jnpr.toby.hardware.chassis.chassis.check_chassis_database')
    @patch('jnpr.toby.hardware.chassis.chassis.check_fru_state')
    def test_request_fru_offline(self, mock1, mock2, mock3):
        from jnpr.toby.hardware.chassis.chassis import request_fru_offline
        ######################################################################
        logging.info("Test case 1: Request offline with slot")
        mock1.return_value = True
        mock2.return_value = True
        self.handle.get_model = MagicMock(return_value="MX120")
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle, slot=[1, 2, 3],
                                     chassis="fpc", check_online=1,
                                     check_count=1, check_interval=10)

        self.assertTrue(result, 'Request unsuccessfully with slot')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Request offline with slot return false")
        self.handle.get_model = MagicMock(return_value="MX120")
        mock1.return_value = False
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle, slot=[1, 2, 3],
                                     chassis="fpc", check_online=1,
                                     check_count=1, check_interval=10)

        self.assertFalse(result, 'Wrong return when check_fru_state return False')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3:request offline with fru_inf and fru = pic and chassis")
        self.handle.get_model = MagicMock(return_value="MX120")
        mock1.return_value = True
        mock2.return_value = True
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle, fru_if="ge-1/2/3",
                                     chassis="fpc", check_database=1,
                                     check_count=1, check_interval=10,
                                     fru='pic')

        self.assertTrue(result, 'request unsuccessfully with fru_inf and fru = pic and chassis')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4:request offline with fru_inf and fru = pic and check_chassis_database false")
        self.handle.get_model = MagicMock(return_value="MX120")
        mock1.return_value = True
        mock2.return_value = False
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle, fru_if="ge-1/2/3",
                                     check_database=1,
                                     check_count=1, check_interval=10,
                                     fru='pic')

        self.assertFalse(result, 'request unsuccessfully with fru_inf and fru = pic and check_chassis_database false')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 5:request offline with fru= fpc and method=power and chassis")
        self.handle.get_model = MagicMock(return_value="M20")
        mock1.return_value = False
        mock2.return_value = False
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle,
                                     check_database=1,
                                     check_count=1, check_interval=10,
                                     fru='fpc', slot=2, method="power",
                                     chassis="chassis")

        self.assertFalse(result, 'Wrong return when check_fru_state false')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 6:request offline with fru= cp and method=power_output")
        self.handle.get_model = MagicMock(return_value="M20")
        mock1.return_value = False
        mock2.return_value = False
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle,
                                     check_database=1,
                                     check_count=1, check_interval=10,
                                     fru='cb', slot=2, method="power_output")

        self.assertFalse(result, 'Wrong return when check_fru_state false')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 7:request offline with fru= feb")
        self.handle.get_model = MagicMock(return_value="M120")
        mock1.return_value = True
        mock2.return_value = True
        mock3.return_value = [{'state': "ACTIVE", 'links': {'2': 1}},
                              {'state': "PASSIVE", 'links': {'2': 2}}]
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle,
                                     check_count=1, check_interval=10,
                                     fru='feb', slot=2)

        self.assertTrue(result, 'request unsuccessfully with fru= feb')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 8:request offline with fru= fabric plane and state OFFLINE")
        self.handle.get_model = MagicMock(return_value="M120")
        mock1.return_value = True
        mock2.return_value = True
        mock3.return_value = {'state': "OFFLINE", 'links': {'slot': 0}}
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle,
                                     check_count=1, check_interval=10,
                                     fru='fabric plane', slot=2)

        self.assertTrue(result, 'request unsuccessfully with fru= feb')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 9:request offline with fru= fabric plane and state not OFFLINE")
        self.handle.get_model = MagicMock(return_value="M120")
        mock1.return_value = True
        mock2.return_value = True
        mock3.return_value = {'state': "ACTIVE", 'links': {'slot': 0}}
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle,
                                     check_count=1, check_interval=10,
                                     fru='fabric plane', slot=2)

        self.assertFalse(result, 'wrong return when fabric_plane still active')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 10:request offline with fru= sfm and undefined method")
        self.handle.get_model = MagicMock(return_value="M120")
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle,
                                     check_count=1, check_interval=10,
                                     fru='sfm', slot=2, method="abc")

        self.assertFalse(result, 'wrong return when method is undefined')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 11: request offline without fru and slot")
        self.handle.get_model = MagicMock(return_value="M120")
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle,
                                     check_count=1, check_interval=10)

        self.assertFalse(result, 'wrong return when without fru and slot')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 12: request offline with both fru_if and slot")
        self.handle.get_model = MagicMock(return_value="M120")
        self.handle.cli = MagicMock()
        with self.assertRaises(Exception) as text:
            request_fru_offline(device=self.handle, fru_if='ge-1/2/3', slot=2)

        self.assertTrue("Cannot use both IF and SLOT arguments" in str(text.exception))
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 13: request offline with wrong fru")
        self.handle.get_model = MagicMock(return_value="M120")
        self.handle.cli = MagicMock()
        result = request_fru_offline(device=self.handle, fru='ge-1/2/3', slot=1)

        self.assertTrue(result, "Wrong return with wrong fru")
        logging.info("\tPassed")

    @patch('jnpr.toby.hardware.chassis.chassis.check_spare_sib')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fabric_plane')
    @patch('jnpr.toby.hardware.chassis.chassis.check_fru_state')
    def test_request_fru_online(self, mock1, mock2, mock3):
        from jnpr.toby.hardware.chassis.chassis import request_fru_online
        ######################################################################
        logging.info("Test case 1: Request online with fru=pic")
        mock1.return_value = True
        mock2.return_value = True
        self.handle.get_model = MagicMock(return_value="MX120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='pic',
                                    slot=[1, 2, 3], check_offline=1,
                                    check_count=1)

        self.assertTrue(result, 'Request unsuccessfully with fru=pic')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Request online with fru=pic and check_fru_state false")
        mock1.return_value = False
        mock2.return_value = True
        self.handle.get_model = MagicMock(return_value="MX120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='pic',
                                    slot=[1, 2, 3], check_offline=1)

        self.assertFalse(result, 'Wrong return when check_fru_state false')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Request online with fru=pic and chassis")
        mock1.return_value = False
        mock2.return_value = True
        self.handle.get_model = MagicMock(return_value="MX120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='pic',
                                    slot=[1, 2, 3], chassis="chassis")

        self.assertTrue(result, 'Request unsuccessfully with fru=pic and chassis')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Request online with fru=fpc and model=m40")
        mock1.return_value = True
        mock2.return_value = True
        self.handle.get_model = MagicMock(return_value="M40")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='fpc',
                                    slot=3, check_offline=1, chassis="chassis")

        self.assertTrue(result, 'Request unsuccessfully with fru=fpc and model=m40')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Request online with fru=sib and model =t320")
        mock1.return_value = False
        mock2.return_value = True
        mock3.return_value = True
        self.handle.get_model = MagicMock(return_value="t320")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='sib',
                                    slot=0, check_count=1, method="power")

        self.assertFalse(result, 'wrong return when check_fru_state false')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Request online with fru=sib and method = power_output")
        mock1.return_value = False
        mock2.return_value = True
        mock3.return_value = True
        self.handle.get_model = MagicMock(return_value="m20")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='sib',
                                    slot=0, check_count=1, method="power_output")

        self.assertFalse(result, 'wrong return when check_fru_state false')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 7: Request online with fru=feb and model=m120")
        mock1.return_value = True
        mock2.return_value = [{'state': 'ACTIVE', 'links': {'2': 'ok'}},
                              {'state': 'PASSIVE', 'links': {'2': 1}},
                              {'state': 'ACTIVE', 'links': {'2': 'not'}}]
        mock3.return_value = True
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='feb',
                                    slot=2, check_count=1, method="power_output")

        self.assertTrue(result, 'Request unsuccessfully with fru=feb and model=m120')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 8: Request online with fru=fabric and model=m120")
        mock1.return_value = True
        mock2.return_value = {'state': 'ACTIVE', 'links': {'2': 'ok'}}
        mock3.return_value = True
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='fabric plane',
                                    slot=2, check_count=1, method="power_output")

        self.assertTrue(result, 'Request unsuccessfully with fru=feb and model=m120')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 9: Request online with fru=fabric and model=m120 and wrong get_fabric_plane")
        mock1.return_value = True
        mock2.return_value = {'state': 'PASSIVE', 'links': {'2': 'ok'}}
        mock3.return_value = True
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='fabric plane',
                                    slot=2, check_count=1)

        self.assertFalse(result, 'Wrong return with fru=feb and model=m120 and wrong get_fabric_plane')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 10: Request online with wrong method")
        mock1.return_value = True
        mock2.return_value = True
        mock3.return_value = True
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='spmb',
                                    slot=2, check_count=1, method="abc")

        self.assertFalse(result, 'Wrong return with wrong method')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 11: Request online with wrong fru")
        mock1.return_value = True
        mock2.return_value = True
        mock3.return_value = True
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru='test',
                                    slot=2, check_count=1)

        self.assertFalse(result, 'Wrong return with wrong fru')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 12: Request online without fru and slot")
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle)

        self.assertFalse(result, 'Wrong return without fru and slot')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 13: Request online with fru_if")
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru_if="ge-1/2/3",
                                    fru='ccg')

        self.assertTrue(result, 'Request unsuccessfully with fru_if')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 13: Request online with fru_if and invalid fru")
        self.handle.get_model = MagicMock(return_value="m120")
        self.handle.cli = MagicMock()
        result = request_fru_online(device=self.handle, fru_if="ge-1/2/3",
                                    fru='test')

        self.assertFalse(result, 'wrong return with fru_if and invalid fru')
        logging.info("\tPassed")

        #####################################################################
        logging.info("Test case 14: request online with both fru_if and slot")
        self.handle.get_model = MagicMock(return_value="M120")
        self.handle.cli = MagicMock()
        with self.assertRaises(Exception) as text:
            request_fru_online(device=self.handle, fru_if='ge-1/2/3', slot=2)

        self.assertTrue("Cannot use both IF and SLOT arguments" in str(text.exception))
        logging.info("\tPassed")

    @patch('jnpr.toby.hardware.chassis.chassis.get_fru_status')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fabric_plane')
    @patch('jnpr.toby.hardware.chassis.chassis.get_fabric_status')
    def test_check_fabric_plane(self, mock_fabric_status,
                                mock_fabric_plane, mock_fru_status):
        from jnpr.toby.hardware.chassis.chassis import check_fabric_plane
        # =================================================================== #
        logging.info(
            "Test case 1: Check fabric plane unsuccessful with " +
            "model is not supported")
        self.handle.get_model = MagicMock(return_value='EX9214')
        result = check_fabric_plane(self.handle)
        self.assertEqual(result, False,
                         "The function does not return False " +
                         "when running with Unsupported model")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info(
            "Test case 2: Check fabric plane successful with model is mx480")
        self.handle.get_model = MagicMock(return_value='MX480')
        mock_fru_status.return_value =\
            [{'memory-dram-size': '64', 'cpu-total': '3',
              'memory-heap-utilization': '18',
              'memory-buffer-utilization': '43', 'temperature': '36',
              'state': 'Online', 'cpu-interrupt': '0'}] * 8
        mock_fabric_plane.return_value =\
            [{'links': {'fpc': [{'pfe': ['ok'] * 4}]},
              'state': 'ACTIVE'}] * 3 +\
            [{'links': {'fpc': [{'pfe': ['ok'] * 4}]},
              'state': 'ACTIVE'}] * 3
        mock_fabric_status.return_value =\
            [{'uptime': 67785, 'state': 'Online'}] * 3 +\
            [{'uptime': 67785, 'state': 'Check'}] * 3 +\
            [{'uptime': 67785, 'state': 'Spare'}] * 2
        result = check_fabric_plane(self.handle)
        self.assertEqual(result, True,
                         "Fail to check fabric plane with model mx480")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 3: Check fabric plane successful with model is mx960")
        self.handle.get_model = MagicMock(return_value='MX960')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 1
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 1}]},
             'state': 'ACTIVE'}] * 1
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 1
        result = check_fabric_plane(self.handle)
        self.assertEqual(result, True,
                         "Fail to check fabric plane with model mx960")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 4: Check fabric plane successful with model is m120")
        self.handle.get_model = MagicMock(return_value='M120')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 4}]},
             'state': 'ACTIVE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        param = {'links': ['ok'] * 8}
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane with model m120")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 5: Check fabric plane unsuccessful " +
            "with model is mx960 when pfe status is not ok")
        self.handle.get_model = MagicMock(return_value='MX960')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 1
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['not ok'] * 1}]},
             'state': 'ACTIVE'}] * 1
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 1
        result = check_fabric_plane(self.handle)
        self.assertEqual(result, False,
                         "Return True when checking fabric plane unsuccessful")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info("Test case 6: Check fabric plane unsuccessful with " +
                     "model is m120, pfe status is not ok")
        self.handle.get_model = MagicMock(return_value='M120')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 4}]},
             'state': 'ACTIVE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        param = {'links': ['not ok'] * 8}
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, False,
                         "Return True when checking fabric plane unsuccessful")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info("Test case 7: Check fabric plane unsuccessful with " +
                     "model is mx960, fru status is not Online")
        self.handle.get_model = MagicMock(return_value='MX960')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Offline',
                                         'cpu-interrupt': '0'}
                                        ] * 1
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 1}]},
             'state': 'ACTIVE'}] * 1
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 1
        result = check_fabric_plane(self.handle)
        self.assertEqual(result, False,
                         "Return True when checking fabric plane unsuccessful")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info("Test case 8: Check fabric plane unsuccessful with " +
                     "model is m120, fru status is not Online")
        self.handle.get_model = MagicMock(return_value='M120')
        param = {'links': ['ok'] * 8}
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Offline',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 4}]},
             'state': 'ACTIVE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, False,
                         "Return True when checking fabric plane unsuccessful")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info("Test case 9: Check fabric plane unsuccessful with " +
                     "model is mx960, fabric status is not Online")
        self.handle.get_model = MagicMock(return_value='MX960')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 1
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 1}]},
             'state': 'ACTIVE'}] * 1
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Offline'}] * 1
        result = check_fabric_plane(self.handle)
        self.assertEqual(result, False,
                         "Return True when checking fabric plane unsuccessful")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info("Test case 10: Check fabric plane successful with " +
                     "model is m120, fabric status is not Online")
        param = {'links': ['ok'] * 8}
        self.handle.get_model = MagicMock(return_value='M120')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 4}]},
             'state': 'ACTIVE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Offline'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info("Test case 11: Check fabric plane successful with " +
                     "model is mx960, fabric plane is not ACTIVE")
        self.handle.get_model = MagicMock(return_value='MX960')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 1
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 1}]},
             'state': 'SPARE'}] * 1
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 1
        result = check_fabric_plane(self.handle)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info("Test case 12: Check fabric plane unsuccessful with " +
                     "model is m120, fabric plane is not ACTIVE")
        param = {'links': ['ok'] * 8}
        self.handle.get_model = MagicMock(return_value='M120')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 4}]},
             'state': 'SPARE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, False,
                         "Return True when checking fabric plane unsuccessful")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info("Test case 13: links's statuses are not ok")
        param = {'links': ['not ok'] * 8}
        self.handle.get_model = MagicMock(return_value='M120')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Offline',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['ok'] * 4}]},
             'state': 'ACTIVE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info("Test case 14: State is OFFLINE")
        param = {'links': ['not ok'] * 8}
        self.handle.get_model = MagicMock(return_value='M120')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'OFFLINE',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['not ok'] * 4}]},
             'state': 'OFFLINE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'OFFLINE'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 15: get_fabric_plane returns None and model is mx240")
        param = {'links': ['ok'] * 8}
        self.handle.get_model = MagicMock(return_value='MX240')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [None] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 16: Model is mx240 and " +
            "fabric_status is not ACTIVE/SPARE")
        param = {'links': ['ok'] * 8}
        self.handle.get_model = MagicMock(return_value='MX240')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['not ok'] * 4}]},
             'state': 'OFFLINE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, False,
                         "Return True when checking fabric plane unsuccessful")
        logging.info("\tChecked fabric plane unsuccessful as expected")
        # =================================================================== #
        logging.info(
            "Test case 17: Model is mx240 and " +
            "fb_planes[plane]['links']['fpc'][slot] is None")
        param = {'links': ['ok'] * 8}
        self.handle.get_model = MagicMock(return_value='MX240')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Online',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [None]}, 'state': 'ACTIVE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 18: Model is mx240 and " +
            "fb_planes[plane]['links']['fpc'][slot]['pfe'][pfe] == 'ok'")
        param = {'links': ['ok'] * 8}
        self.handle.get_model = MagicMock(return_value='MX240')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Offline',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['not ok'] * 4}]},
             'state': 'ACTIVE'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Online'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 19: Model is mx240 and Status is Error")
        param = {'links': ['ok'] * 8}
        self.handle.get_model = MagicMock(return_value='MX240')
        mock_fru_status.return_value = [{'memory-dram-size': '64',
                                         'cpu-total': '3',
                                         'memory-heap-utilization': '18',
                                         'memory-buffer-utilization': '43',
                                         'temperature': '36',
                                         'state': 'Error',
                                         'cpu-interrupt': '0'}
                                        ] * 8
        mock_fabric_plane.return_value = [
            {'links': {'fpc': [{'pfe': ['not ok'] * 4}]},
             'state': 'Offline'}] * 8
        mock_fabric_status.return_value = [
            {'uptime': 67785, 'state': 'Error'}] * 8
        result = check_fabric_plane(self.handle, **param)
        self.assertEqual(result, True,
                         "Fail to check fabric plane")
        logging.info("\tChecked fabric plane successful as expected")

    def test__chop(self):
        ######################################################################
        logging.info("Test case 1: chop with space at start and end of string")
        string = "     test space    "
        expected = "test space"
        check = chop(self.handle, string)
        self.assertEqual(check, expected,
                         "Delete failed spaces at start and end of string")
        logging.info("\t Chop passed")
        ######################################################################
        logging.info("Test case 2: chop with new line")
        string = '''
             test space

                '''
        expected = "test space"

        check = chop(self.handle, string)
        self.assertEqual(check, expected,
                         "Delete failed new line in string")
        logging.info("\t Chop passed")
 
    def test__get_pic_status(self):
        ######################################################################
        logging.info("Test case 1:Get pics status successfully")
        fpc_slot = 's1'
        pic = {'pic-slot': 'ps11', 'test1': 1, 'test2': 2}
        chas_fru = {'test': 111}
        result = get_pic_status(self.handle, fpc_slot, pic, chas_fru)
        expected = {'pic': {'s1': {'ps11': {'test1': 1, 'test2': 2}}},
                    'test': 111}
        self.assertEqual(result, expected, 'Get pics status unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Get pics status successfully with only pic-slot")
        fpc_slot = 's1'
        pic = {'pic-slot': 'ps11'}
        chas_fru = {'test': 111}
        result = get_pic_status(self.handle, fpc_slot, pic, chas_fru)
        expected = {'pic': {'s1': {'ps11': {}}},
                    'test': 111}
        self.assertEqual(result, expected, 'Get pics status unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Get pics status successfully with chas_fru")
        fpc_slot = 's1'
        pic = {'pic-slot': 'ps11', 'ABC': '222'}
        chas_fru = {'pic': {'s1': {'ps11': {}}}, 'test': 111}
        result = get_pic_status(self.handle, fpc_slot, pic, chas_fru)
        expected = {'pic': {'s1': {'ps11': {'ABC': '222'}}},
                    'test': 111}
        self.assertEqual(result, expected, 'Get pics status successfully')
        logging.info("\tPassed")

    def test__get_fru_craft(self):
        ######################################################################
        logging.info("Test case 1: Create fru craft with multi slot")
        fru = [{'slot': ' slot1 ', 'name': 'abc', 't1-led': 5, 't11-led': 5},
               {'slott': ' slott2 ', 'name': 'xyz', 't2-led': 6},
               {'slot': ' slot3 ', 'name': 'a123', 't3-led': 7}]
        fru_craft = get_fru_craft(self.handle, fru)
        expected = {'slot1': {'t1': 1, 't11': 1}, 'slot3': {'t3': 1}}
        self.assertEqual(fru_craft, expected, 'Create fru craft successfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Create fru craft with 1 slot")
        fru = {'slot': ' slot1 ', 'name': 'abc', 't1-led': 5, 't11-led': 5}
        fru_craft = get_fru_craft(self.handle, fru)
        expected = {'t1': 1, 't11': 1}
        self.assertEqual(fru_craft, expected, 'Create fru craft successfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Create fru craft with a Null fru")
        fru = {}
        fru_craft = get_fru_craft(self.handle, fru)
        expected = {}
        self.assertEqual(fru_craft, expected, 'Result is not a Null dict')
        logging.info("\tPassed")

    def test__get_fru_led(self):
        ######################################################################
        logging.info("Test case 1: Create fru led status successfully")
        led = {'t1-led': 4, 't2-led': 5, 't3': 6, 't4-led': 7}
        fru = get_fru_led(self.handle, led)
        expected = {'t1': 1, 't2': 1, 't4': 1}
        self.assertEqual(fru, expected, 'reate fru led status unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Create fru led status with Null led")
        led = {}
        fru = get_fru_led(self.handle, led)
        expected = {}
        self.assertEqual(fru, expected, 'Result is not a Null dict')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Create fru led status with wrong led")
        led = {'t1': 'a', 't2': 4}
        fru = get_fru_led(self.handle, led)
        expected = {}
        self.assertEqual(fru, expected, 'Result is not a Null dict')
        logging.info("\tPassed")

    def test__get_alarm_led(self):
        ######################################################################
        logging.info("Test case 1: Create alarm led status successfully")
        led = {'test-abc123': 123, 'check-123abc': 456, 'notmatch': 789}
        result = get_alarm_led(self.handle, led)
        expected = {'test': 1, 'check': 1}
        self.assertEqual(result, expected, 'Create alarm led successfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Create alarm led status with wrong value")
        led = {'testabc123': 123, 'check123abc': 456, 'notmatch': 789}
        result = get_alarm_led(self.handle, led)
        expected = {}
        self.assertEqual(result, expected, 'Result is not a Null dict')
        logging.info("\tPassed")

    def test__timeless(self):
        ######################################################################
        logging.info("Test case 1: Compare 2 time with return True")

        self.assertTrue(timeless(self.handle, "11:22:33", "11:22:34"),
                        'Compare should be True')
        self.assertTrue(timeless(self.handle, "11:22:33", "11:23:33"),
                        'Compare should be True')
        self.assertTrue(timeless(self.handle, "11:22:33", "12:22:33"),
                        'Compare should be True')
        logging.info("\t Compare Passed")

        ######################################################################
        logging.info("Test case 2: Compare 2 time with return False")
        self.assertFalse(timeless(self.handle, "11:22:33", "11:22:32"),
                         'Compare should be False')
        self.assertFalse(timeless(self.handle, "11:22:33", "11:21:33"),
                         'Compare should be True')
        self.assertFalse(timeless(self.handle, "11:22:33", "10:22:33"),
                         'Compare should be True')
        self.assertFalse(timeless(self.handle, "11:22:33", "11:22:33"),
                         'Compare should be True')
        self.assertFalse(timeless(self.handle, "11:22::33", "11::22:33"),
                         'Compare should be True')
        logging.info("\t Compare Passed")

    def test_show_data(self):
        from jnpr.toby.hardware.chassis.chassis import show_data
        ######################################################################
        logging.info("Test case 1: Show dict data")
        message = "unittest"
        data = {'t1': 1, 't2': {'t3': {'t4': 2}}}
        self.assertTrue(show_data(self.handle, data, message),
                        "Error when showing dict data")
        logging.info("\tShow Passed")

        ######################################################################
        logging.info("Test case 2: show string data")
        message = "unittest"
        data = "string data for testing"
        self.assertTrue(show_data(self.handle, data, message),
                        "Error when showing string data")
        logging.info("\tShow Passed")

        ######################################################################
        logging.info("Test case 3: Show list data")
        message = "unittest"
        data = [1, 2, 3]
        self.assertTrue(show_data(self.handle, data, message),
                        "Error when showing list data")
        logging.info("\tShow Passed")

    def test__check_re_led(self):
        logging.info("Test case 1: Check re led passed with model is " +
                     "in m5|m[124]0|m7i|m10i|IRM")
        self.handle.get_model = MagicMock(return_value='m10i')
        craft = {'re': {'ok': 1}}
        status = {'re': [{'mastership-state': 'master', 'status': 'Online'},
                         {'mastership-state': 'backup', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 2: Check re led failed with model is " +
                     "in m5|m[124]0|m7i|m10i|IRM")
        self.handle.get_model = MagicMock(return_value='m10i')
        craft = {'re': {'fail': 1}}
        status = {'re': [{'mastership-state': 'master', 'status': 'Online'},
                         {'mastership-state': 'backup', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 3: Check re led passed with model is " +
                     "not in m5|m[124]0|m7i|m10i|IRM")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'master': 1},
                        {'ok': 1, 'backup': 1}]}
        status = {'re': [{'mastership-state': 'master', 'status': 'Online'},
                         {'mastership-state': 'backup', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 4: Check re led failed with model is " +
                     "not in m5|m[124]0|m7i|m10i|IRM")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'master': 1, 'fail': 1},
                        {'ok': 1, 'backup': 1, 'fail': 1}]}
        status = {'re': [{'mastership-state': 'master', 'status': 'Online'},
                         {'mastership-state': 'backup', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 5: Check re led failed with master, model " +
                     "is not in m5|m[124]0|m7i|m10i|IRM and not 'ok' key")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'master': 1},
                        {'backup': 1}]}
        status = {'re': [{'mastership-state': 'master', 'status': 'Online'},
                         {'mastership-state': 'backup', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 6: Check re led failed with master, model " +
                     "is not in m5|m[124]0|m7i|m10i|IRM and not 'master' key")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1},
                        {'ok': 1}]}
        status = {'re': [{'mastership-state': 'master', 'status': 'Online'},
                         {'mastership-state': 'backup', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 7: Check re led failed with backup, model" +
                     " is not in m5|m[124]0|m7i|m10i|IRM and " +
                     "'master' key exist")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'master': 1},
                        {'ok': 1, 'master': 1}]}
        status = {'re': [{'mastership-state': 'backup', 'status': 'Online'},
                         {'mastership-state': 'master', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 8: Check re led failed with backup, model" +
                     " is not in m5|m[124]0|m7i|m10i|IRM and " +
                     "'fail' key exist")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'backup': 1, 'fail': 1},
                        {'ok': 1, 'master': 1, 'fail': 1}]}
        status = {'re': [{'mastership-state': 'backup', 'status': 'Online'},
                         {'mastership-state': 'master', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 9: Check re led failed with model" +
                     " is not in m5|m[124]0|m7i|m10i|IRM and " +
                     "'status' key does not exist in status")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'master': 1},
                        {'ok': 1, 'backup': 1}]}
        status = {'re': [{'mastership-state': 'unknown'},
                         {'mastership-state': 'unknown'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 10: Check re led failed with model" +
                     " is not in m5|m[124]0|m7i|m10i|IRM and " +
                     "state is Present")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'master': 1},
                        {'ok': 1, 'backup': 1}]}
        status = {'re': [{'mastership-state': 'Present'},
                         {'mastership-state': 'Present'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 11: Check re led passed with model" +
                     " is not in m5|m[124]0|m7i|m10i|IRM and " +
                     "state is host")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'master': 1},
                        {'ok': 1, 'backup': 1}]}
        status = {'re': [{'mastership-state': 'host', 'status': 'Online'},
                         {'mastership-state': 'host', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked RE LED")
        # =================================================================== #
        logging.info("Test case 12: Check re led passed with model" +
                     " is not in m5|m[124]0|m7i|m10i|IRM and " +
                     "but not master")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'re': [{'ok': 1, 'masr': 1},
                        {'ok': 1, 'backup': 1}]}
        status = {'re': [{'mastership-state': 'Present', 'status': 'Online'},
                         {'mastership-state': 'Present', 'status': 'Online'}]}
        result = check_re_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked RE LED")

    def test__check_sfm_led(self):
        logging.info("Test case 1: Model='m40e', State=Online and " +
                     "return True")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 1, 'amber': 0, 'blue': 1},
                         {'green': 1, 'amber': 0, 'blue': 1}]
                 }
        status = {'sfm': [{'state': 'Online'},
                          {'state': 'Online'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 2: Model = 'm40e', State = Online and " +
                     "return False")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 0, 'amber': 1, 'blue': 0},
                         {'green': 0, 'amber': 1, 'blue': 0}]
                 }
        status = {'sfm': [{'state': 'Online'},
                          {'state': 'Online'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 3: Model='m40e', State='Online - Standby' " +
                     "and return True")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 1, 'amber': 0, 'blue': 0},
                         {'green': 1, 'amber': 0, 'blue': 0}]
                 }
        status = {'sfm': [{'state': 'Online - Standby'},
                          {'state': 'Online - Standby'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 4: Model='m40e', State='Online - Standby' " +
                     "and return False")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 0, 'amber': 1, 'blue': 1},
                         {'green': 0, 'amber': 1, 'blue': 1}]
                 }
        status = {'sfm': [{'state': 'Online - Standby'},
                          {'state': 'Online - Standby'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 5: Model='m40e', State='Offline' " +
                     "and return True")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 0, 'amber': 0, 'blue': 0},
                         {'green': 0, 'amber': 0, 'blue': 0}]
                 }
        status = {'sfm': [{'state': 'Offline'},
                          {'state': 'Offline'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 6: Model='m40e', State='Offline' " +
                     "and return False")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 1, 'amber': 1, 'blue': 1},
                         {'green': 1, 'amber': 1, 'blue': 1}]
                 }
        status = {'sfm': [{'state': 'Offline'},
                          {'state': 'Offline'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 7: Model='m40e', State='Present' " +
                     "and return True")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 0, 'amber': 1, 'blue': 0},
                         {'green': 0, 'amber': 1, 'blue': 0}]
                 }
        status = {'sfm': [{'state': 'Present'},
                          {'state': 'Present'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, True, "Result should be True")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 8: Model='m40e', State='Present' " +
                     "and return False")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 1, 'amber': 0, 'blue': 1},
                         {'green': 1, 'amber': 0, 'blue': 1}]
                 }
        status = {'sfm': [{'state': 'Present'},
                          {'state': 'Present'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 9: Model='mx960', State='Online' " +
                     "and return False")
        self.handle.get_model = MagicMock(return_value='mx960')
        craft = {'sfm': [{'green': 1, 'amber': 0, 'blue': 1},
                         {'green': 1, 'amber': 0, 'blue': 1}]
                 }
        status = {'sfm': [{'state': 'Online'},
                          {'state': 'Online'}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 10: Model='mx966'")
        self.handle.get_model = MagicMock(return_value='mx966')
        craft = {}
        status = {}
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked SFM LED")
        # =================================================================== #
        logging.info("Test case 11: Model='m40e' with state is None")
        self.handle.get_model = MagicMock(return_value='m40e')
        craft = {'sfm': [{'green': 1, 'amber': 0, 'blue': 1},
                         {'green': 1, 'amber': 0, 'blue': 1}]
                 }
        status = {'sfm': [{'state': None},
                          {'state': None}]
                  }
        result = check_sfm_led(self.handle, craft, status)
        self.assertEqual(result, False, "Result should be False")
        logging.info("\tChecked SFM LED")

    def test__convert_alarm_display(self):
        ######################################################################
        logging.info("Test case 1: Convert alarm successfully with absent")
        level = 'major'
        descr = ' Absnt test 1 '
        alarm = convert_alarm_display(self.handle, level, descr)
        expected = {'class': 'major', 'description': 'Absent test 1'}
        self.assertEqual(alarm, expected, 'Convert absent alarm unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Convert alarm successfully with VltSnsr")
        level = 'minor'
        descr = ' VltSnsr test 2 '
        alarm = convert_alarm_display(self.handle, level, descr)
        expected = {'class': 'minor', 'description': 'Volt Sensor test 2'}
        self.assertEqual(alarm, expected, 'Convert VltSnsr alarm unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Convert alarm successfully with check LOS")
        level = 'minor'
        descr = ' check LOS test 3 '
        alarm = convert_alarm_display(self.handle, level, descr)
        expected = {'class': 'minor',
                    'description': 'check : SONET loss test 3'}
        self.assertEqual(alarm, expected, 'Convert check LOS alarm unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Convert alarm successfully with boot: alt")
        level = 'minor'
        descr = ' boot: alt test 4 '
        alarm = convert_alarm_display(self.handle, level, descr)
        expected = {'class': 'minor',
                    'description': 'Boot from alternate media test 4'}
        self.assertEqual(alarm, expected, 'Convert boot: alt alarm unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Convert alarm successfully with slot")
        level = 'minor'
        descr = ' Slot 11: errors test 5 '
        alarm = convert_alarm_display(self.handle, level, descr)
        expected = {'class': 'minor',
                    'description': 'Too many unrecoverable errors test 5'}
        self.assertEqual(alarm, expected, 'Convert Slot alarm unsuccessfully')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Convert alarm successfully with undefined alarm")
        level = 'minor'
        descr = ' test 6 '
        alarm = convert_alarm_display(self.handle, level, descr)
        expected = {'class': 'minor',
                    'description': 'test 6'}
        self.assertEqual(alarm, expected, 'Convert undefined alarm unsuccessfully')
        logging.info("\tPassed")

    def test__convert_name(self):
        ######################################################################
        logging.info("Test case 1: Convert name successfully with Routing Engine")
        name = 'Routing Engine'
        alarm = convert_name(self.handle, name)
        expected = 're'
        self.assertEqual(alarm, expected, 'Ressult is not re')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Convert name successfully with specify Routing Engine")
        name = 'Routing Engine 15'
        alarm = convert_name(self.handle, name)
        expected = 're 15'
        self.assertEqual(alarm, expected, 'Ressult is not re 15')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 3: Convert name successfully with Power Supply A")
        name = 'Power Supply A'
        alarm = convert_name(self.handle, name)
        expected = 'pem 0'
        self.assertEqual(alarm, expected, 'Ressult is not pem 0')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 4: Convert name successfully with Power Supply B")
        name = 'Power Supply B'
        alarm = convert_name(self.handle, name)
        expected = 'pem 1'
        self.assertEqual(alarm, expected, 'Ressult is not pem 1')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 5: Convert name successfully with specify Power Supply")
        name = 'Power Supply 23'
        alarm = convert_name(self.handle, name)
        expected = 'pem 23'
        self.assertEqual(alarm, expected, 'Ressult is not pem 23')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 6: Convert name successfully with undefined name")
        name = ' test 6 '
        alarm = convert_name(self.handle, name)
        expected = 'test 6'
        self.assertEqual(alarm, expected, 'Ressult is not as undefined name')
        logging.info("\tPassed")

    def test__get_hardware(self):
        ######################################################################
        logging.info("Test case 1: Get hardware successfully")
        arg0 = {}
        arg1 = "name test"
        arg2 = "version 1"
        arg3 = "part-number 1"
        arg4 = "serial-number 1"
        arg5 = "description unittest"
        result = get_hardware(self.handle, arg0, arg1, arg2, arg3, arg4, arg5)
        expected = {'name': 'name test',
                    'version': 'version 1',
                    'part-number': 'part-number 1',
                    'serial-number': 'serial-number 1',
                    'description': 'description unittest'
                    }
        self.assertEqual(result, expected, 'Get hardware unsuccessfully with wrong value')
        logging.info("\tPassed")

    def test_compare_data(self):
        from jnpr.toby.hardware.chassis.chassis import compare_data
        logging.info("Test case 1: h1 and h2 are compared passed")
        self.assertTrue(compare_data(self.handle,
                                     var1={'a': 1, 'b': 2, 'c': 3},
                                     var2={'a': 1, 'b': 2},
                                     skip_list=['c']))
        self.assertTrue(compare_data(self.handle,
                                     var1={'a': 1, 'b': 2},
                                     var2={'a': 1, 'b': 2, 'c': 3},
                                     skip_list=['c']))
        self.assertFalse(compare_data(self.handle,
                                      var1={'a': 1, 'b': 2},
                                      var2={'a': 1, 'b': 2, 'c': 3},
                                      ))
        self.assertFalse(compare_data(self.handle,
                                      var2={'a': 1, 'b': 2},
                                      var1={'a': 1, 'b': 2, 'c': 3},
                                      ))
        self.assertFalse(compare_data(self.handle,
                                      var2=[1, 2, 3],
                                      var1=[1, 2, 3, 4],
                                      ))
        self.assertTrue(compare_data(self.handle,
                                     var2=[1, 2, 3, 4],
                                     var1=[1, 2, 3, 4],
                                     ))
        self.assertTrue(compare_data(self.handle,
                                     var2="test",
                                     var1="test",
                                     ))
        logging.info("\tCompleted comparing data")
        # =================================================================== #
        logging.info("Test case 2: h1 and h2 are compared failed")
        h1_list = [{'a': 2, 'b': 2},
                   {'a': 1, 'b': 2, 'c': 3},
                   {'a': 1, 'b': 2},
                   {'a': 2, 'b': 2},
                   [1, 2, 3, 4],
                   [1, 2, 3],
                   [4, 1, 2],
                   "abcd",
                   1234]
        h2_list = [{'a': 1, 'b': 2},
                   {'a': 1, 'b': 2},
                   {'a': 1, 'b': 2, 'c': 3},
                   {'a': 1, 'b': 2},
                   [1, 2, 3],
                   [1, 2, 3, 4],
                   [2, 3, 1],
                   "abc",
                   123]
        skip_list = ['b']
        self.assertFalse(compare_data(self.handle,
                                      var1=h1_list,
                                      var2=h2_list,
                                      skip_list=skip_list))
        logging.info("\tCompleted comparing data")
        # =================================================================== #
        logging.info("Test case 3: Compare empty list with empty dictionary")
        self.assertFalse(compare_data(self.handle, var1=[], var2={},
                                      skip_list=""))
        logging.info("\tCompleted comparing data")
        # =================================================================== #
        logging.info("Test case 4: Compare string with empty list")
        self.assertFalse(compare_data(self.handle, var1="abc", var2=[],
                                      skip_list=""))
        logging.info("\tCompleted comparing data")
        # =================================================================== #
        logging.info("Test case 5: Compare empty list with string")
        self.assertFalse(compare_data(self.handle, var1=[], var2="abc",
                                      skip_list=""))
        logging.info("\tCompleted comparing data")

    def test__get_alarm_info(self):
        logging.info("Test case 1: Input valid alarm info")
        xml = "<alarm-information><alarm-summary>" +\
            "<active-alarm-count>4</active-alarm-count></alarm-summary>" +\
            "<alarm-detail><alarm-time seconds=\"1474407975\">" +\
            "2016-09-20 14:46:15 PDT</alarm-time><alarm-class>Minor" +\
            "</alarm-class><alarm-description>PEM 1 Fan Failed" +\
            "</alarm-description><alarm-short-description>PEM 1 Fan Failed" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail><alarm-detail><alarm-time seconds=" +\
            "\"1474407971\">2016-09-20 14:46:11 PDT</alarm-time>" +\
            "<alarm-class>Minor</alarm-class><alarm-description>" +\
            "Require a Fan Tray upgrade</alarm-description>" +\
            "<alarm-short-description>Higher cooling capa" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail><alarm-detail><alarm-time seconds=" +\
            "\"1474407965\">2016-09-20 14:46:05 PDT</alarm-time>" +\
            "<alarm-class>Minor</alarm-class><alarm-description>" +\
            "Temperature Warm</alarm-description><alarm-short-description>" +\
            "Temperature Warm</alarm-short-description>" +\
            "<alarm-type>Chassis</alarm-type></alarm-detail>" +\
            "<alarm-detail><alarm-time seconds=\"1474407934\">" +\
            "2016-09-20 14:45:34 PDT</alarm-time><alarm-class>Minor" +\
            "</alarm-class><alarm-description>Backup RE Active" +\
            "</alarm-description><alarm-short-description>Backup RE Active" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail></alarm-information>"
        response = etree.fromstring(xml)
        alarms = get_alarm_info(self.handle, response)
        self.assertEqual(len(alarms), 4, "Should get 4 alarms")
        logging.info("\tGot 4 Alarms successful as expected")
        # =================================================================== #
        logging.info("Test case 2: Alarm count is not equal to " +
                     "length of alarms")
        xml = "<alarm-information><alarm-summary>" +\
            "<active-alarm-count>5</active-alarm-count></alarm-summary>" +\
            "<alarm-detail><alarm-time seconds=\"1474407975\">" +\
            "2016-09-20 14:46:15 PDT</alarm-time><alarm-class>Minor" +\
            "</alarm-class><alarm-description>PEM 1 Fan Failed" +\
            "</alarm-description><alarm-short-description>PEM 1 Fan Failed" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail><alarm-detail><alarm-time seconds=" +\
            "\"1474407971\">2016-09-20 14:46:11 PDT</alarm-time>" +\
            "<alarm-class>Minor</alarm-class><alarm-description>" +\
            "Require a Fan Tray upgrade</alarm-description>" +\
            "<alarm-short-description>Higher cooling capa" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail><alarm-detail><alarm-time seconds=" +\
            "\"1474407965\">2016-09-20 14:46:05 PDT</alarm-time>" +\
            "<alarm-class>Minor</alarm-class><alarm-description>" +\
            "Temperature Warm</alarm-description><alarm-short-description>" +\
            "Temperature Warm</alarm-short-description>" +\
            "<alarm-type>Chassis</alarm-type></alarm-detail>" +\
            "<alarm-detail><alarm-time seconds=\"1474407934\">" +\
            "2016-09-20 14:45:34 PDT</alarm-time><alarm-class>Minor" +\
            "</alarm-class><alarm-description>Backup RE Active" +\
            "</alarm-description><alarm-short-description>Backup RE Active" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail></alarm-information>"
        response = etree.fromstring(xml)
        alarms = get_alarm_info(self.handle, response)
        self.assertEqual(len(alarms), 4, "Should get 4 alarms")
        logging.info("\tGot 4 Alarms successful as expected")
        # =================================================================== #
        logging.info("Test case 3: Alarm count is 0 but has alarm details")
        xml = "<alarm-information><alarm-summary>" +\
            "<active-alarm-count>0</active-alarm-count></alarm-summary>" +\
            "<alarm-detail><alarm-time seconds=\"1474407975\">" +\
            "2016-09-20 14:46:15 PDT</alarm-time><alarm-class>Minor" +\
            "</alarm-class><alarm-description>PEM 1 Fan Failed" +\
            "</alarm-description><alarm-short-description>PEM 1 Fan Failed" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail><alarm-detail><alarm-time seconds=" +\
            "\"1474407971\">2016-09-20 14:46:11 PDT</alarm-time>" +\
            "<alarm-class>Minor</alarm-class><alarm-description>" +\
            "Require a Fan Tray upgrade</alarm-description>" +\
            "<alarm-short-description>Higher cooling capa" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail><alarm-detail><alarm-time seconds=" +\
            "\"1474407965\">2016-09-20 14:46:05 PDT</alarm-time>" +\
            "<alarm-class>Minor</alarm-class><alarm-description>" +\
            "Temperature Warm</alarm-description><alarm-short-description>" +\
            "Temperature Warm</alarm-short-description>" +\
            "<alarm-type>Chassis</alarm-type></alarm-detail>" +\
            "<alarm-detail><alarm-time seconds=\"1474407934\">" +\
            "2016-09-20 14:45:34 PDT</alarm-time><alarm-class>Minor" +\
            "</alarm-class><alarm-description>Backup RE Active" +\
            "</alarm-description><alarm-short-description>Backup RE Active" +\
            "</alarm-short-description><alarm-type>Chassis</alarm-type>" +\
            "</alarm-detail></alarm-information>"
        response = etree.fromstring(xml)
        alarms = get_alarm_info(self.handle, response)
        self.assertEqual(len(alarms), 4, "Should get 4 alarms")
        logging.info("\tGot 4 Alarms successful as expected")
        # =================================================================== #
        logging.info("Test case 4: Alarms is Empty")
        xml = "<alarm-information><alarm-summary><no-active-alarms/>" +\
            "</alarm-summary></alarm-information>"
        response = etree.fromstring(xml)
        alarms = get_alarm_info(self.handle, response)
        self.assertEqual(len(alarms), 0, "Should get 0 alarm")
        logging.info("\tGot 0 Alarm successful as expected")
        # =================================================================== #
        logging.info("Test case 5: Fail to get Alarms")
        xml = '''
<alarm-information>
    <alarm-summary>
        <active-alarm-count>4</active-alarm-count>
    </alarm-summary>
    <alarm-detail>
        <alarm-class>Minor</alarm-class>
        <alarm-description>PEM 1 Fan Failed</alarm-description>
        <alarm-short-description>PEM 1 Fan Failed</alarm-short-description>
        <alar-type>Chassis</alar-type>
    </alarm-detail>
    <alarm-detail>
        <alarm-class>Minor2</alarm-class>
        <alarm-description>PEM 2 Fan Failed</alarm-description>
        <alarm-short-description>PEM 2 Fan Failed</alarm-short-description>
        <alarm-type>Chassis2</alarm-type>
    </alarm-detail>
</alarm-information>
'''
        response = etree.fromstring(xml)
        alarms = get_alarm_info(self.handle, response)
        self.assertEqual(len(alarms), 2, "Should get 2 alarms")
        logging.info("\tGot Alarm info unsuccessful as expected")

    def test__get_pic_info(self):
        logging.info("Test case 1: Input valid pic info")
        xml = """<fpc-information>
            <fpc>
                <slot>0</slot>
                <state>Online</state>
                <description>MPC5E 3D Q 2CGE+4XGE</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>2X10GE SFPP OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>1</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>1X100GE CFP2 OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>2</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>2X10GE SFPP OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>3</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>1X100GE CFP2 OTN</pic-type>
                </pic>
            </fpc>
            <fpc>
                <slot>4</slot>
                <state>Online</state>
                <description>MPC5E 3D Q 2CGE+4XGE</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>2X10GE SFPP OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>1</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>1X100GE CFP2 OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>2</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>2X10GE SFPP OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>3</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>1X100GE CFP2 OTN</pic-type>
                </pic>
            </fpc>
            <fpc>
                <slot>11</slot>
                <state>Online</state>
                <description>MPC5E 3D Q 24XGE+6XLGE</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>12X10GE SFPP OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>1</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>12X10GE SFPP OTN</pic-type>
                </pic>
                <pic>
                    <pic-slot>2</pic-slot>
                    <pic-state>Offline</pic-state>
                    <pic-type>3X40GE QSFPP</pic-type>
                </pic>
                <pic>
                    <pic-slot>3</pic-slot>
                    <pic-state>Offline</pic-state>
                    <pic-type>3X40GE QSFPP</pic-type>
                </pic>
            </fpc>
        </fpc-information>"""
        response = etree.fromstring(xml)
        pic_status = get_pic_info(self.handle, response)
        expected_pic_status = [['Online', 'Online', 'Online', 'Online'],
                               None, None, None,
                               ['Online', 'Online', 'Online', 'Online'],
                               None, None, None, None, None, None,
                               ['Online', 'Online', 'Offline', 'Offline']]
        self.assertListEqual(pic_status, expected_pic_status,
                             "PIC status should be %s" % expected_pic_status)
        logging.info("\tGet PIC status successful")
        # =================================================================== #
        logging.info("Test case 2: pic tag does not exist")
        xml = """<fpc-information>
            <fpc>
                <slot>0</slot>
                <state>Online</state>
                <description>MPC5E 3D Q 2CGE+4XGE</description>
            </fpc>
        </fpc-information>"""
        response = etree.fromstring(xml)
        pic_status = get_pic_info(self.handle, response)
        expected_pic_status = [[]]
        self.assertListEqual(pic_status, expected_pic_status,
                             "PIC status should be %s" % expected_pic_status)
        logging.info("\tGet PIC status successful")
        # =================================================================== #
        logging.info("Test case 3: slot tag does not exist")
        xml = """<fpc-information>
            <fpc>
            </fpc>
        </fpc-information>"""
        response = etree.fromstring(xml)
        pic_status = get_pic_info(self.handle, response)
        expected_pic_status = []
        self.assertListEqual(pic_status, expected_pic_status,
                             "PIC status should be %s" % expected_pic_status)
        logging.info("\tGet PIC status successful")
        # =================================================================== #
        logging.info("Test case 4: ")
        xml = """<fpc-information>
            <fpc>
                <slot>0</slot>
                <state>Online</state>
                <description>MPC5E 3D Q 2CGE+4XGE</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-tate>Online</pic-tate>
                    <pic-type>2X10GE SFPP OTN</pic-type>
                </pic>
                <pic>
                    <pic-lot>1</pic-lot>
                    <pic-state>Online</pic-state>
                    <pic-type>1X100GE CFP2 OTN</pic-type>
                </pic>
            </fpc>
            <fpc>
                <slot>4</slot>
                <state>Online</state>
                <description>MPC5E 3D Q 2CGE+4XGE</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>2X10GE SFPP OTN</pic-type>
                </pic>
            </fpc>
        </fpc-information>"""
        response = etree.fromstring(xml)
        pic_status = get_pic_info(self.handle, response)
        expected_pic_status = [[None], None, None, None, ['Online']]
        self.assertListEqual(pic_status, expected_pic_status,
                             "PIC status should be %s" % expected_pic_status)
        logging.info("\tGet PIC status successful")

    def test__check_dynamic_db(self):
        ######################################################################
        logging.info("Test case 1: fru state is not in Empty|Offline|Present")
        slot = 0
        dynamic_db = [[{'state': 'Empty'}, {'state': 'Empty'}],
                      [{'state': 'Present'}, {'state': 'Present'}]]
        fru_status = [[{'state': 'Online'}, {'state': 'Online'}],
                      [{'state': 'Present'}, {'state': 'Present'}]]
        self.assertTrue(check_dynamic_db(self.handle, slot,
                                         dynamic_db, fru_status),
                        'check dynamic database unsuccessful')
        logging.info("\t Check passed")

        ######################################################################
        logging.info("Test case 2: dynamic db NOT exists for slot")
        slot = 2
        dynamic_db = [[{'state': 'Present'}],
                      [{'state': 'Present'}, {'state': 'Online'}]]
        fru_status = [[{'state': 'Online'}, {'state': 'Online'}],
                      [{'state': 'Present'}, {'state': 'Online'}]]
        self.assertTrue(check_dynamic_db(self.handle, slot,
                                         dynamic_db, fru_status),
                        'check dynamic database unsuccessful')
        logging.info("\t Check passed")

        ######################################################################
        logging.info("Test case 3: fru state is in Empty|Offline|Present")
        slot = 0
        dynamic_db = [[{'state': 'Online'}], [{'state': 'Online'}]]
        fru_status = [[{'state': 'Empty'}], [{'state': 'Online'}]]
        self.assertFalse(check_dynamic_db(self.handle, slot,
                                          dynamic_db, fru_status),
                         'check dynamic database successful')
        logging.info("\t Check passed")

        ######################################################################
        logging.info("Test case 4:dynamic_db has more entries then fru_status")
        slot = 0
        dynamic_db = [[{'state': 'Present'}, {'state': 'Present'}],
                      [{'state': 'Online'}]]
        fru_status = [[{'state': 'Online'}],
                      [{'state': 'Present'}]]
        self.assertFalse(check_dynamic_db(self.handle, slot,
                                          dynamic_db, fru_status),
                         'check dynamic database successful')
        logging.info("\t Check passed")

        ######################################################################
        logging.info("Test case 5: fru_status NOT exists for slot")
        slot = 1
        dynamic_db = [[{'state': 'Present'}, {'state': 'Present'}],
                      [{'state': 'Present'}, {'state': 'Present'}]]
        fru_status = [[{'state': 'Online'}, {'state': 'Present'}]]
        self.assertFalse(check_dynamic_db(self.handle, slot,
                                          dynamic_db, fru_status),
                         'Run well although Fru_status NOT exists for slot')
        logging.info("\t Check passed")

        ######################################################################
        logging.info("Test case 6: fru status is not list")
        slot = 0
        dynamic_db = [[{'state': 'Present'}]]
        fru_status = [{'state': 'Online'}]
        self.assertFalse(check_dynamic_db(self.handle, slot,
                                          dynamic_db, fru_status),
                         'Run well although Fru_status is not list')
        logging.info("\t Check passed")

        ######################################################################
        logging.info("Test case 7: Test checking failed for slot")
        slot = 2
        dynamic_db = [[{'state': 'Present'}]]
        fru_status = [[{'state': 'Online'}],
                      [{'state': 'Present'}],
                      [{'state': 'Present'}],
                      [{'state': 'Present'}],
                      [{'state': 'Present'}]]
        self.assertFalse(check_dynamic_db(self.handle, slot,
                                          dynamic_db, fru_status),
                         'Run well although checking failed for slot')
        logging.info("\t Check passed")

    def test__convert_db_name(self):
        logging.info("Test case 1: Current db name is cbd")
        db_name = 'cbd'
        models = ['m160', 'm40e', 'mx240', 'mx960']
        new_db_names = ['mcs', 'mcs', 'cb', 'cb']
        for i in range(0, len(models)):
            new_db_name = convert_db_name(self.handle, db_name, models[i])
            self.assertEqual(new_db_name,
                             new_db_names[i],
                             "Unexpected new DB name: %s" % new_db_name)
            logging.info("\tExpected new DB name for %s/%s: %s" %
                         (db_name, models[i], new_db_name))
        # =================================================================== #
        logging.info("Test case 2: Current db name is cg")
        db_name = 'cg'
        models = ['m160', 'm40e', 'mx240', 'mx960']
        new_db_names = ['pcg', 'pcg', 'scg', 'scg']
        for i in range(0, len(models)):
            new_db_name = convert_db_name(self.handle, db_name, models[i])
            self.assertEqual(new_db_name,
                             new_db_names[i],
                             "Unexpected new DB name: %s" % new_db_name)
            logging.info("\tExpected new DB name for %s/%s: %s" %
                         (db_name, models[i], new_db_name))
        # =================================================================== #
        logging.info("Test case 3: Current db name is not cbd or cg")
        db_name = 'abc'
        models = ['m160', 'm40e', 'mx240', 'mx960']
        new_db_names = ['abc', 'abc', 'abc', 'abc']
        for i in range(0, len(models)):
            new_db_name = convert_db_name(self.handle, db_name, models[i])
            self.assertEqual(new_db_name,
                             new_db_names[i],
                             "Unexpected new DB name: %s" % new_db_name)
            logging.info("\tExpected new DB name for %s/%s: %s" %
                         (db_name, models[i], new_db_name))

    def test_get_fpc_pic_spucp(self):
        from jnpr.toby.hardware.chassis.chassis import get_fpc_pic_spucp
        logging.info("Test case 1:")
        xml = """
<multi-routing-engine-results>
    <multi-routing-engine-item>
            <re-name>node0</re-name>
            <fpc-information>
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>VSRX DPDK GE</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>1</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>VSRX DPDK GE</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>2</slot>
                    <state>Offline</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Offline</pic-state>
                        <pic-type>VSRX DPDK GE</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>
        <multi-routing-engine-item>
            <re-name>node1</re-name>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
"""
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=True)
        self.handle.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        result = get_fpc_pic_spucp(self.handle, state='Online')
        self.assertEqual(result, ['FPC0', 'FPC1'], 'Failed to get 2 FPCs')
        logging.info("\tGet FPC PIC SPUCP successful as expected")
        # =================================================================== #
        logging.info("Test case 2:")
        xml = """
<multi-routing-engine-results>
    <multi-routing-engine-item>
        <re-name>node1</re-name>
        <fpc-information>
            <fpc>
                <slot>0</slot>
                <state>Online</state>
                <description>FPC</description>
                <pic>
                    <pic-slot>0</pic-slot>
                    <pic-state>Online</pic-state>
                    <pic-type>VSRX DPDK GE</pic-type>
                </pic>
            </fpc>
        </fpc-information>
    </multi-routing-engine-item>
</multi-routing-engine-results>
"""
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=True)
        self.handle.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        result = get_fpc_pic_spucp(self.handle, state='Online')
        self.assertEqual(result, ['FPC0'], 'Failed to get 1 FPC')
        logging.info("\tGet FPC PIC SPUCP successful as expected")
        # =================================================================== #
        logging.info("Test case 3:")
        xml = """
<multi-routing-engine-results>
    <multi-routing-engine-item>
            <re-name>node0</re-name>
            <fpc-information>
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>SPU Cp DPDK GE</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>2</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>VSRX DPDK GE</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>
        <multi-routing-engine-item>
            <re-name>node1</re-name>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
"""
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=True)
        self.handle.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        result = get_fpc_pic_spucp(self.handle, node_id="1")
        self.assertEqual(result, ['FPC0 PIC0'],
                         'Failed to get FPC with node id 1')
        logging.info("\tGet FPC PIC SPUCP successful as expected")
        # =================================================================== #
        logging.info("Test case 4:")
        xml = """
<multi-routing-engine-results>
    <fpc>
        <slot>0</slot>
    </fpc>
</multi-routing-engine-results>
"""
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=True)
        self.handle.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        self.assertFalse(get_fpc_pic_spucp(self.handle, node_id="1"),
                         "Result is not False")
        logging.info("\tGet FPC PIC SPUCP unsuccessful as expected")
 
    def test_get_fpc_pic_npc(self):
        from jnpr.toby.hardware.chassis.chassis import get_fpc_pic_npc
        logging.info(
            "Test case 1: Get FPC PIC NPC successful with SRX5600 model")
        xml = """
<multi-routing-engine-results>
    <multi-routing-engine-item>
            <re-name>node0</re-name>
            <fpc-information>
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>NPC PIC</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>
        <multi-routing-engine-item>
            <re-name>node1</re-name>
            <fpc-information>
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>VSRX DPDK GE</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
        </multi-routing-engine-item>
    </multi-routing-engine-results>
"""
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=True)
        self.handle.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        self.handle.get_model = MagicMock(return_value='SRX5600')
        result = get_fpc_pic_npc(self.handle)
        self.assertEqual(type(result), list, "Failed to get FPC PIC NPC")
        logging.info("\tGet FPC PIC NPC successful as expected")
        # =================================================================== #
        logging.info(
            "Test case 2: Get FPC PIC NPC unsuccessful with TRT model")
        xml = "<abc-test>132</abc-test>"
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=True)
        self.handle.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        self.handle.get_model = MagicMock(return_value='TRT')
        self.assertFalse(get_fpc_pic_npc(self.handle),
                         msg="Result is not False")
        logging.info("\tGet fpc pic npc unsuccessful as expected")
        # =================================================================== #
        logging.info(
            "Test case 3: Get FPC PIC NPC successful with SMX960 model")
        xml = """
            <fpc-information>
                <fpc>
                    <slot>0</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>VSRX DPDK GE</pic-type>
                    </pic>
                </fpc>
                <fpc>
                    <slot>2</slot>
                    <state>Online</state>
                    <description>FPC</description>
                    <pic>
                        <pic-slot>0</pic-slot>
                        <pic-state>Online</pic-state>
                        <pic-type>NPC PIC</pic-type>
                    </pic>
                </fpc>
            </fpc-information>
"""
        res = etree.fromstring(xml)
        self.handle.get_rpc_equivalent = MagicMock(return_value=True)
        self.handle.execute_rpc = MagicMock(
            side_effect=[Response(response=res)])
        self.handle.get_model = MagicMock(return_value='SMX960')
        self.assertEqual(get_fpc_pic_npc(self.handle), ['FPC2 PIC0'],
                         "SPC slots is incorrect")
        logging.info("\tGet FPC PIC NPC successful as expected")

    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_hardware')
    def test_get_ms_pics_info(self, mock):
        from jnpr.toby.hardware.chassis.chassis import get_ms_pics_info
        logging.info("Test case 1: Get MS PIC Info Unsuccessful")
        data = {
            'pc 0': {
                'MIC 0': {
                    'PIC 0': {
                        'serial-number': 'BUILTIN',
                        'description': 'Virtual 10x 1GE(LAN) SFP'},
                    'PIC 1': {
                        'serial-number': 'BUILTIN',
                        'description': 'Virtual 10x 1GE(LAN) SFP'},
                    'description': 'Virtual 20x 1GE(LAN) SFP'},
                'MIC 1': {
                    'PIC 2': {
                        'serial-number': 'BUILTIN',
                        'description': 'Virtual 2x 10GE(LAN) XFP'},
                    'PIC 3': {'serial-number': 'BUILTIN',
                              'description': 'Virtual 2x 10GE(LAN) XFP'},
                    'description': 'Virtual 4x 10GE(LAN) XFP'},
                'CPU': {'serial-number': '123XYZ987'},
                'description': 'Virtual 20x1G + 4x10G FPC'},
            'routing engine 1': {
                'serial-number': 'f643780a-94',
                'description': 'RE-VMX'},
            'chassis': {
                'serial-number': 'VMX4849',
                'description': 'MX960'},
            'routing engine 0': {
                'serial-number': 'f6437774-94',
                'description': 'RE-VMX'}}
        mock.return_value = data
        result = get_ms_pics_info(self.handle)
        self.assertEqual(result, False,
                         'Function does not return False in Negative test case'
                         )
        logging.info("\tGot MS PIC Info unsuccessful")
        # =================================================================== #
        logging.info("Testcase 2: Get MS PIC Info successful")
        jobject = MagicMock(spec=Juniper)
        jobject.handle = MagicMock()
        data = {
            'fpc 0': {
                'MIC 0': {
                    'PIC 0': {
                        'serial-number': 'BUILTIN',
                        'description': 'Virtual 10x 1GE(LAN) SFP'},
                    'PIC 1': {
                        'serial-number': 'BUILTIN',
                        'description': '10x 1GE(LAN) SFP'},
                    'description': 'Virtual 20x 1GE(LAN) SFP'},
                'MIC 1': {
                    'PIC 2': {
                        'serial-number': 'BUILTIN',
                        'description': '2x 10GE(LAN) XFP'},
                    'PIC 3': {
                        'serial-number': 'BUILTIN',
                        'description': 'Virtual 2x 10GE(LAN) XFP'},
                    'description': 'Virtual 4x 10GE(LAN) XFP'},
                'CPU': {
                    'serial-number': '123XYZ987'},
                'description': 'Virtual 20x1G + 4x10G FPC'},
            'fpc 1': {
                'PIC 0': {
                    'serial-number': 'BUILTIN',
                    'description': 'Virtual 10x 1GE(LAN) SFP'},
                'PIC 1': {
                    'serial-number': 'BUILTIN',
                    'description': '10x 1GE(LAN) SFP'},
                'PIC 2': {
                    'serial-number': 'BUILTIN',
                    'description': '2x 10GE(LAN) XFP'},
                'PIC 3': {
                    'serial-number': 'BUILTIN',
                    'description': 'Virtual 2x 10GE(LAN) XFP'},
                'description': 'Virtual 4x 10GE(LAN) XFP',
                'CPU': {'serial-number': '123XYZ987'},
                'description': 'Virtual 20x1G + 4x10G FPC'},
            'routing engine 1': {
                'serial-number': 'f643780a-94',
                'description': 'RE-VMX'},
            'chassis': {
                'serial-number': 'VMX4849',
                'description': 'MX960'},
            'routing engine 0': {
                'serial-number': 'f6437774-94',
                'description': 'RE-VMX'}}
        mock.return_value = data
        result = get_ms_pics_info(self.handle, status='Virtual')
        self.assertEqual(type(result), dict,
                         "The return value is not Dictionary")
        logging.info("\tGot MS PIC Info successful")

    def test_delete_chassis_alarm(self):
        from jnpr.toby.hardware.chassis.chassis import delete_chassis_alarm
        logging.info(
            "Test case 1: Delete_chassis_alarm without any option")
        self.handle.config = MagicMock(
            return_value=Response(response="", status=True))
        self.handle.commit = MagicMock(
            return_value=Response(response="commit complete", status=True))
        result = delete_chassis_alarm(device=self.handle)
        self.assertEqual(result, True,
                         "Result should be True")
        logging.info(
            "\tVerify Delete_chassis_alarm without any option PASSED")
        # =================================================================== #
        logging.info(
            "Test case 2: Delete_chassis_alarm with deactivate and commit")
        self.handle.config = MagicMock(
            return_value=Response(response="", status=True))
        self.handle.commit = MagicMock(
            return_value=Response(response="commit complete", status=True))
        result = delete_chassis_alarm(device=self.handle,
                                      deactivate=1, commit=1)
        self.assertEqual(result, "commit complete",
                         "Result should be 'commit complete'")
        logging.info(
            "\tVerify Delete_chassis_alarm with deactivate and commit PASSED")

    def test_delete_temperature_threshold(self):
        from jnpr.toby.hardware.chassis.chassis import delete_temperature_threshold
        # ================================================================= #
        logging.info("Test case 1: Deactivate chassis temperature-threshold "
                     "configuration successful with commit")
        param = {'deactivate': 1, 'commit': 1}
        self.assertTrue(delete_temperature_threshold(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 1 passed")
        # ================================================================= #
        logging.info("Test case 2: Deactivate chassis temperature-threshold "
                     "configuration successful without commit")
        param = {'deactivate': 1}
        self.assertTrue(delete_temperature_threshold(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 2 passed")
        # ================================================================= #
        logging.info("Test case 3: Delete chassis temperature-threshold "
                     "configuration successful")
        param = {'commit': 1}
        self.assertTrue(delete_temperature_threshold(self.handle, **param),
                        "Result should be True")
        logging.info("\t Test case 3 passed")    			

    def test__cli_get_hardware(self):
        ######################################################################
        logging.info("Test case 1: Create Chassis hardware information ")
        self.handle.get_model = MagicMock(return_value="")
        res = """
Hardware inventory:
Item             Version  Part number  Serial number     Description
Chassis                                B3645             M10I
Midplane         REV 07   710-008920   DY0897            M10i Midplane
Power Supply 0   Rev 05   740-008537   QB12578           AC Power Supply
Power Supply 1   Rev 08   740-008537   VC51641           AC Power Supply
HCM 0            REV 06   710-010580   DY4625            M10i HCM
HCM 1            REV 06   710-010580   DY4590            M10i HCM
Routing Engine 0 REV 04   740-039441   9009123064        RE-B-1800x1
Routing Engine 1 REV 04   740-039441   9009123015        RE-B-1800x1
CFEB 0           N/A      N/A          N/A               Backup
CFEB 1           REV 12   750-010465   DY2195            Internet Processor II
FPC 0                                                    E-FPC
  PIC 0          REV 04   750-002992   HA6507            4x F/E, 100 BASE-TX
  PIC 1          REV 01   750-002982   HF2572            1x Tunnel
  PIC 2          REV 13   750-012838   DZ4423            4x 1GE(LAN), IQ2
    Xcvr 0       REV 02   740-011613   AM0925SBLP9       SFP-SX
    Xcvr 1       REV 02   740-011613   AM0925SBLNT       SFP-SX
    Xcvr 2       REV 01   740-011613   AM0821S9ZMD       SFP-SX
    Xcvr 3       REV 01   740-011782   P8J28JH           SFP-SX
    PIC 3        REV 03   750-000612   AC1775            2x OC-3 ATM, MM
FPC 1                                                    E-FPC
  PIC 0          REV 04   750-000611   AP6321            4x OC-3 SONET, MM
  PIC 1          REV 06   750-000616   AB5165            1x OC-12 ATM, MM
  PIC 2          REV 04   750-003036   HD7279            4x E1, RJ48
  PIC 3          REV 02   750-000613   AA9239            1x OC-12 SONET, SMIR
Fan Tray 1                                               Rear Right Fan Tray
 
"""
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_hardware(self.handle)
        self.assertEqual(type(result), dict, 'Create chassis hardware dict failed')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Chassis hardware information with psd and chassis")
        res = """
PSD1-RE0
Hardware inventory:
Item             Version  Part number  Serial number     Description
Chassis                                B3645             M10I
Midplane         REV 07   710-008920   DY0897            M10i Midplane
Power Supply 0   Rev 05   740-008537   QB12578           AC Power Supply
Power Supply 1   Rev 08   740-008537   VC51641           AC Power Supply
HCM 0            REV 06   710-010580   DY4625            M10i HCM
HCM 1            REV 06   710-010580   DY4590            M10i HCM
Routing Engine 0 REV 04   740-039441   9009123064        RE-B-1800x1
Routing Engine 1 REV 04   740-039441   9009123015        RE-B-1800x1
CFEB 0           N/A      N/A          N/A               Backup
CFEB 1           REV 12   750-010465   DY2195            Internet Processor II
FPC 0                                                    E-FPC
  PIC 0          REV 04   750-002992   HA6507            4x F/E, 100 BASE-TX
  PIC 1          REV 01   750-002982   HF2572            1x Tunnel
  PIC 2          REV 13   750-012838   DZ4423            4x 1GE(LAN), IQ2
    Xcvr 0       REV 02   740-011613   AM0925SBLP9       SFP-SX
    Xcvr 1       REV 02   740-011613   AM0925SBLNT       SFP-SX
    Xcvr 2       REV 01   740-011613   AM0821S9ZMD       SFP-SX
    Xcvr 3       REV 01   740-011782   P8J28JH           SFP-SX
    PIC 3        REV 03   750-000612   AC1775            2x OC-3 ATM, MM
FPC 1                                                    E-FPC
  PIC 0          REV 04   750-000611   AP6321            4x OC-3 SONET, MM
  PIC 1          REV 06   750-000616   AB5165            1x OC-12 ATM, MM
  PIC 2          REV 04   750-003036   HD7279            4x E1, RJ48
  PIC 3          REV 02   750-000613   AA9239            1x OC-12 SONET, SMIR
Fan Tray 1                                               Rear Right Fan Tray

"""
        self.handle.cli = MagicMock(return_value=Response(response=res))
        result = cli_get_hardware(self.handle, chassis="clei-models")
        self.assertEqual(type(result), dict, 'Create chassis hardware dict failed')
        logging.info("\tPassed")


    def test_delete_chassis_graceful(self):
        ######################################################################
        logging.info("Test case 1: Run with deactiavte and commit")
        self.handle.get_model = MagicMock(return_value="")
        self.handle.get_version.return_value='9.0'
        self.handle.config = MagicMock()
        self.handle.commit = MagicMock(side_effect=[Response(response=True)])
        result = chassis.delete_chassis_graceful(self.handle, deactivate=1, commit=1)
        self.assertTrue(result, 'Function do not return True with deactivate param')
        logging.info("\tPassed")

        ######################################################################
        logging.info("Test case 2: Run without deacivate and commit")
       	self.handle.get_version.return_value='5.0'
        self.handle.config = MagicMock()
        result = chassis.delete_chassis_graceful(self.handle)
        self.assertTrue(result, 'Function do not return True without deactivate param')
        logging.info("\tPassed")

    def test_get_chassis_hardware(self):
       
        logging.info(" Testing test_get_chassis_hardware......")
      
        with patch("jnpr.toby.hardware.chassis.chassis.__cli_get_hardware") as cli_hardware_patch :
            logging.info("\tTest case 1 : Passing xml as 0 & detail as 1")
            cli_hardware_patch.return_value = {'name':'chassis','description':'TXP','serial-number':'JN1145008AHB'}
            result = chassis.get_chassis_hardware(device = self.handle,xml=0,detail=1)
            self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
            logging.info("\t\tTestcase Passed")
           
            logging.info("\tTest case 2 : Passing xml as 0 & extensive as 1")
            cli_hardware_patch.return_value = {'name':'chassis','description':'TXP','serial-number':'JN1145008AHB'}
            result = chassis.get_chassis_hardware(device = self.handle,xml=0,extensive=1)
            self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
            logging.info("\t\tTestcase Passed")

            logging.info("\tTest case 3 : Passing xml as 0 & frus as 1")
            cli_hardware_patch.return_value = {'name':'chassis','description':'TXP','serial-number':'JN1145008AHB'}
            result = chassis.get_chassis_hardware(device = self.handle,xml=0,frus=1)
            self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
            logging.info("\t\tTestcase Passed")
        
            logging.info("\tTest case 4 : Passing xml as 0 & models as 1")
            cli_hardware_patch.return_value = {'name':'chassis','description':'TXP','serial-number':'JN1145008AHB'}
            result = chassis.get_chassis_hardware(device = self.handle,xml=0,models=1,chassis='sfc 0')
            self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
            logging.info("\t\tTestcase Passed")

        with patch("jnpr.toby.hardware.chassis.chassis.__get_chassis_inventory") as chassis_inventory_patch :
            
            xml_string = """
                      <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
    			<multi-routing-engine-results>
        		    <multi-routing-engine-item>
            			<re-name>sfc0-re0</re-name>
            			<chassis-inventory>
                			<chassis>
                    				<name>Chassis</name>
                    				<serial-number>JN1145008AHB</serial-number>
                    				<description>TXP</description>
                    				<chassis-module>
                        				<name>Midplane</name>
                        				<version>REV 05</version>
                        				<part-number>710-022574</part-number>
                        				<serial-number>ABAA0009</serial-number>
                        				<description>SFC Midplane</description>
                        				<model-number>CHAS-BP-TXP-S</model-number>
                    				</chassis-module>
                                	</chassis>
				</chassis-inventory>
        	           </multi-routing-engine-item>
    		     </multi-routing-engine-results>
                     <cli>
                           <banner></banner>
                     </cli>
                   </rpc-reply>
                         """
            xml                     = etree.fromstring(xml_string)
            self.handle.execute_rpc = MagicMock(return_value=Response(response=xml))
            chassis_inventory_patch.return_value = {'name':'chassis','description':'TXP','serial-number':'JN1145008AHB'}

            logging.info("\tTest case 5 : Passing chassis argument & model as TXP ")
            self.handle.get_model   = MagicMock(return_value="TXP")
            result = chassis.get_chassis_hardware(device = self.handle,chassis='sfc 0')
            self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
            logging.info("\t\tTestcase Passed")
            
            logging.info("\tTest case 6 : Without passing chassis argument  & passing model as TXP ")
            self.handle.get_model   = MagicMock(return_value="TXP")
            result = chassis.get_chassis_hardware(device = self.handle)
            self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
            logging.info("\t\tTestcase Passed")
            
            logging.info("\tTest case 7 : Passing model as Mx480 ")
            self.handle.get_model   = MagicMock(return_value="Mx480")
            result = chassis.get_chassis_hardware(device = self.handle)
            self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
            logging.info("\t\tTestcase Passed")

        chassis_fru_xml_string = """
                      <rpc-reply xmlns:junos="http://xml.juniper.net/junos/17.1I0/junos">
                                <chassis-fru-inventory>
                                        <chassis-fru>
                                                <name>Chassis</name>
                                                <serial-number>JN1145008AHB</serial-number>
                                                <description>TXP</description>
                                                <chassis-fru-module>
                                                        <name>Midplane</name>
                                                        <version>REV 05</version>
                                                        <part-number>710-022574</part-number>
                                                        <serial-number>ABAA0009</serial-number>
                                                        <description>SFC Midplane</description>
                                                        <model-number>CHAS-BP-TXP-S</model-number>
                                                </chassis-fru-module>
                                        </chassis-fru>
                                </chassis-fru-inventory>
                   </rpc-reply>
                               """
        xml                     = etree.fromstring(chassis_fru_xml_string)
        self.handle.execute_rpc = MagicMock(return_value=Response(response=xml))

        logging.info("\tTest case 8 : Passing frus as 1")
        self.handle.get_model   = MagicMock(return_value="TXP")
        result = chassis.get_chassis_hardware(device = self.handle,frus=1)
        self.assertEqual(type(result),dict,"Expecting dict but found %s"%type(result))
        logging.info("\t\tTestcase Passed")   

    def test_kill_process(self):

        logging.info(" Testing kill_process......")
        logging.info("\tTest case 1 : Passing no_proc_ok argument ")
        self.handle.shell = MagicMock(return_value=Response(response=" 1234"))
        result = chassis.kill_process(device=self.handle,pid="49921",signal=" some-string",prog=" string sun",no_proc_ok="1")
        self.assertEqual(result,True,"Should return True But found %s"%result)
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 2 : Without Passing no_proc_ok argument ")
        self.handle.shell = MagicMock(return_value=Response(response=" 1234 permitted"))
        result = chassis.kill_process(device=self.handle,pid=["49921"],signal=" some-string",prog=" string")
        self.assertEqual(result,False,"Should return False But found %s"%result)
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 3 : Without Passing prog argument ")
        self.handle.send_control_char = MagicMock(return_value=True)
        result = chassis.kill_process(device=self.handle,signal=" some-string")
        self.assertEqual(result,True,"Should return True But found %s"%result)
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 4 : Passing no_proc_ok argument ")
        self.handle.shell = MagicMock(return_value=Response(response=" 1234 permitted"))
        result = chassis.kill_process(device=self.handle,pid="49921",signal=" some-string",prog=" string sun",no_proc_ok="1")
        self.assertEqual(result,False,"Should return True But found %s"%result)
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 5 : Passing no_proc_ok argument ")
        self.handle.shell = MagicMock(return_value=Response(response=""))
        result = chassis.kill_process(device=self.handle,pid="49921",signal=" some-string",prog=" string sun",no_proc_ok="1")
        self.assertEqual(result,True,"Should return True But found %s"%result)
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 6 : Passing no_proc_ok argument ")
        self.handle.shell = MagicMock(return_value=Response(response=""))
        result = chassis.kill_process(device=self.handle,pid="49921",signal=" some-string",prog=" string sun",no_proc_ok="0")
        self.assertEqual(result,False,"Should return True But found %s"%result)
        logging.info("\t\tTestcase Passed")

        logging.info("\tTest case 7 : Kill command exceptional case ")
        self.handle.shell = MagicMock(return_value=Exception("Error while executing command"))
        try :
            result = chassis.kill_process(device=self.handle,pid="49921",signal=" some-string",prog=" string sun",no_proc_ok="0")
        except :
            logging.info("\t\tTestcase Passed")


        logging.info("\tTest case 8 : Kill command exceptional case ")
        self.handle.shell = MagicMock(side_effect=[Response(response=" 1234"),Exception("Error while executing command")])
        try :
            result = chassis.kill_process(device=self.handle,pid="49921",signal=" some-string",prog=" string sun",no_proc_ok="0")
        except :
            logging.info("\t\tTestcase Passed")

    def test_check_args(self):

        logging.info(" Testing check_args......")
        logging.info("\tTest case 1 : Passing invalid argument in kw_dict")
        try :
            kvargs = {'term':'string'}
            result = chassis.check_args(device=self.handle,valid_key=['name','match'],required_key=['name'],kw_dict=kvargs)
        except :
            logging.info("\t\tTestcase Passed")
        logging.info("\tTest case 2 : Passing invalid key in required_key")
        try :
            kvargs = {'name':'string'}
            result = chassis.check_args(device=self.handle,valid_key=['name','match'],required_key=['term'],kw_dict=kvargs)
        except :
            logging.info("\t\tTestcase Passed")
        logging.info("\tTest case 2 : Passing valid required_keys")
        kvargs = {'name':'string'}
        result = chassis.check_args(device=self.handle,valid_key=['name','match'],required_key=['name'],kw_dict=kvargs)
        self.assertEqual(result,kvargs,"Should return the Passed dict")
        logging.info("\t\tTestcase Passed")
		
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_environment')
    @patch('jnpr.toby.hardware.chassis.chassis.check_enhance_fantray')
    def test_check_chassis_fan(self,fantray_patch,env_patch):

        logging.info("Test case 1: Check chassis fan count for TX Matrix")
        self.handle.get_model = MagicMock(return_value='TX Matrix')
        fantray_patch.return_value = False
        env_patch.return_value = {'scc':{'top left front fan':'spinning at normal speed','top left middle fan':'spinning at normal speed','top left rear fan':'spinning at normal speed','top right front fan':'spinning at normal speed','top right middle fan':'spinning at normal speed','top right rear fan':'spinning at normal speed','bottom left front fan':'spinning at normal speed','bottom left middle fan':'spinning at normal speed','bottom left rear fan':'spinning at normal speed','bottom right front fan':'spinning at normal speed','bottom right middle fan':'spinning at normal speed','bottom right rear fan':'spinning at normal speed','rear tray top fan':'spinning at normal speed','rear tray second fan':'spinning at normal speed','rear tray third fan':'spinning at normal speed','rear tray fourth fan':'spinning at normal speed','rear tray fifth fan':'spinning at normal speed','rear tray sixth fan':'spinning at normal speed','rear tray seventh fan':'spinning at normal speed','rear tray bottom fan':'spinning at normal speed'}}
        env = {'scc':{'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left middle fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'bottom right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray top fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray second fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray third fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray fourth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'rear tray fifth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray sixth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray seventh fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'rear tray bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'bottom left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'bottom right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}}        
        result = chassis.check_chassis_fan(device=self.handle,speed='normal',env = env )
        self.assertEqual(result,True,"Result should be True")
		
        logging.info("Test case 2: Check chassis fan count for TXP Matrix with incorrect fan speed")
        self.handle.get_model = MagicMock(return_value='TXP')
        fantray_patch.return_value = False
        env_patch.return_value = {'sfc 0':{'top left front fan':'spinning at normal speed',
	                    'top left middle fan':'spinning at normal speed','top left rear fan':'spinning at normal speed',
	                    'top right front fan':'spinning at normal speed','top right middle fan':'spinning at normal speed',
			    'top right rear fan':'spinning at normal speed','bottom left front fan':'spinning at normal speed',
			    'bottom left middle fan':'spinning at normal speed','bottom left rear fan':'spinning at normal speed',
			    'bottom right front fan':'spinning at normal speed','bottom right middle fan':'spinning at normal speed',
			    'bottom right rear fan':'spinning at normal speed','rear tray top fan':'spinning at normal speed',
			    'rear tray second fan':'spinning at normal speed','rear tray third fan':'spinning at normal speed',
			    'rear tray fourth fan':'spinning at normal speed','rear tray fifth fan':'spinning at normal speed',
			    'rear tray sixth fan':'spinning at normal speed','rear tray seventh fan':'spinning at normal speed',
			    'rear tray bottom fan':'spinning at normal speed'}}
        env = {'sfc 0':{'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'Check'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'top right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'top right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'top right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'bottom left front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'bottom left middle fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'Check'},
               'bottom right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'bottom right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'rear tray top fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'rear tray second fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'rear tray third fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'rear tray fourth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
                'rear tray fifth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'rear tray sixth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'rear tray seventh fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
                'rear tray bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
                'bottom left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
                'bottom right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' }}}        
        result = chassis.check_chassis_fan(device=self.handle,speed='high',env = env )
        self.assertEqual(result,False,"Result should be True")
        logging.info("Test case 2: Check chassis fan count for TXP Matrix with incorrect fan speed PASSED.../n")
		
        logging.info("Testcase 3: Checking with unknown fan speed")
        fantray_patch.return_value = True
        result = chassis.check_chassis_fan(device=self.handle,speed="low")
        self.assertEqual(result,False,"Result should be False")
        logging.info("Testcase 3: Checking with unknown fan speed PASSED...\n")
 
        logging.info("Testcase 4: Checking with incorrect fan count")
        fantray_patch.return_value = False
        self.handle.get_model = MagicMock(return_value='m20')
        env_patch.return_value = {'rear fan':'Spinning at high speed','front upper fan':'Spinning at high speed',
                                  'front middle fan':'Spinning at high speed', 'front bottom fan':'Spinning at high speed'}
        result = chassis.check_chassis_fan(device=self.handle,speed="high",count = 3)

        self.assertEqual(result,False,"Result should be False")
        logging.info("Testcase 4: Checking with incorrect fan count PASSED...\n") 

        logging.info("Testcase 5: Checking with fan count and status for m20 model other than TX Matix/TXP")
        fantray_patch.return_value = False
        self.handle.get_model = MagicMock(return_value='m20')
        env_patch.return_value = {'rear fan':'Spinning at high speed','front upper fan':'Spinning at high speed',
                                  'front middle fan':'Spinning at high speed', 'front bottom fan':'Spinning at high speed'}
        env = {'rear fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'front upper fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_chassis_fan(device=self.handle,speed="normal",count = 4,env = env)
        self.assertEqual(result,True,"Result should be True")   
        logging.info("Testcase 5: Checking with fan count and status for m20 model other than TX Matix/TXP PASSED.../n")
		
        logging.info("Testcase 6: Checking incorrect fan speed for m20 model")
        fantray_patch.return_value = False
        self.handle.get_model = MagicMock(return_value='m20')
        env_patch.return_value = {'rear fan':'Spinning at high speed','front upper fan':'Spinning at high speed',
                                  'front middle fan':'Spinning at high speed', 'front bottom fan':'Spinning at high speed'}
        env = {'rear fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'front upper fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'front bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_chassis_fan(device=self.handle,speed="high",count = 4,env = env)
        self.assertEqual(result,False,"Result should be False")   
        logging.info("Testcase 6: Checking incorrect fan speed for m20 model PASSED.../n")
		
        logging.info("Testcase 7: Checking incorrect fan status for m20 model")
        fantray_patch.return_value = False
        self.handle.get_model = MagicMock(return_value='m20')
        env_patch.return_value = {'rear fan':'Spinning at high speed','front upper fan':'Spinning at high speed',
                                  'front middle fan':'Spinning at high speed', 'front bottom fan':'Spinning at high speed'}
        env = {'rear fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'check'},
               'front upper fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'check' },
               'front middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'check' },
               'front bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' }}
        result = chassis.check_chassis_fan(device=self.handle,speed="high",count = 4,env = env)
        self.assertEqual(result,False,"Result should be False")   
        logging.info("Testcase 7: Checking incorrect fan speed for m20 model PASSED.../n")

        logging.info("Testcase 8: Checking incorrect fan status for m20 model")
        fantray_patch.return_value = False
        self.handle.get_model = MagicMock(return_value='m20')
        env_patch.return_value = {'rear fan':'Spinning at high speed','front upper fan':'Spinning at high speed',
                                  'front middle fan':'Spinning at high speed', 'front bottom fan':'Spinning at high speed'}
        env = {'rear fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'Check'},
               'front upper fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'front middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' },
               'front bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'Check' }}
        result = chassis.check_chassis_fan(device=self.handle,speed="high",count = 4,env = env)
        self.assertEqual(result,False,"Result should be False")   
        logging.info("Testcase 8: Checking incorrect fan status for m20 model PASSED.../n")
		
        logging.info("Testcase 9: Checking fan is not present for m20 model")
        fantray_patch.return_value = False
        self.handle.get_model = MagicMock(return_value='m20')
        env_patch.return_value = {'rear fan':'Spinning at normal speed','front upper fan':'Spinning at normal speed',
                                  'front middle fan':'Spinning at normal speed', 'front bottom fan':'Spinning at normal speed'}
        env = {'rear fan': {'class': 'Fans',
                            'status': 'check'},
               'front upper fan': {'class': 'Fans',
                                  'status': 'check' },
               'front middle fan': {'class': 'Fans',
                                  'status': 'check' },
               'front bottom fan': {'class': 'Fans',
                                  'status': 'Check' }}
        result = chassis.check_chassis_fan(device=self.handle,speed="high",count = 4,env = env)
        self.assertEqual(result,True,"Result should be True")   
        logging.info("Testcase 9: Checking fan speed is not present for m20 model PASSED.../n")		

        logging.info("Test case 10: Check chassis fan count for TXP Matrix with incorrect fan speed")
        self.handle.get_model = MagicMock(return_value='TXP')
        fantray_patch.return_value = False
        env_patch.return_value = {'sfc 0':{'top left front fan':'spinning at normal speed',
	                                'top left middle fan':'spinning at normal speed','top left rear fan':'spinning at normal speed',
					'top right front fan':'spinning at normal speed','top right middle fan':'spinning at normal speed',
					'top right rear fan':'spinning at normal speed','bottom left front fan':'spinning at normal speed',
					'bottom left middle fan':'spinning at normal speed','bottom left rear fan':'spinning at normal speed',
	        		'bottom right front fan':'spinning at normal speed','bottom right middle fan':'spinning at normal speed',
				'bottom right rear fan':'spinning at normal speed','rear tray top fan':'spinning at normal speed',
				'rear tray second fan':'spinning at normal speed','rear tray third fan':'spinning at normal speed',
				'rear tray fourth fan':'spinning at normal speed','rear tray fifth fan':'spinning at normal speed',
				'rear tray sixth fan':'spinning at normal speed','rear tray seventh fan':'spinning at normal speed',
				'rear tray bottom fan':'spinning at normal speed'}}
        env = {'sfc 0':{'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom left middle fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'bottom right middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'bottom right rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray top fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray second fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray third fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray fourth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'rear tray fifth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray sixth fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'rear tray seventh fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'rear tray bottom fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'bottom left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
                'bottom right front fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}}        
        result = chassis.check_chassis_fan(device=self.handle,speed='high',env = env,count=20 )
        self.assertEqual(result,False,"Result should be True")
        logging.info("Test case 10: Check chassis fan count for TXP Matrix with incorrect fan speed PASSED.../n")

        logging.info("Testcase11: comment is not there in TX model environment argument")
        self.handle.get_model = MagicMock(return_value='TXP')
        env_patch.return_value = {'sfc 0':{'top left front fan':'spinning at normal speed',
		                            'top left middle fan':'spinning at normal speed','top left rear fan':'spinning at normal speed',
					'top right front fan':'spinning at normal speed','top right middle fan':'spinning at normal speed',
					'top right rear fan':'spinning at normal speed','bottom left front fan':'spinning at normal speed',
					'bottom left middle fan':'spinning at normal speed','bottom left rear fan':'spinning at normal speed',
				'bottom right front fan':'spinning at normal speed','bottom right middle fan':'spinning at normal speed',
				'bottom right rear fan':'spinning at normal speed','rear tray top fan':'spinning at normal speed',
				'rear tray second fan':'spinning at normal speed','rear tray third fan':'spinning at normal speed',
				'rear tray fourth fan':'spinning at normal speed','rear tray fifth fan':'spinning at normal speed',
				'rear tray sixth fan':'spinning at normal speed','rear tray seventh fan':'spinning at normal speed',
				'rear tray bottom fan':'spinning at normal speed'}}
        fantray_patch.return_value = False
        env = {'sfc 0':{'top left front fan': {'class': 'Fans',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'status': 'OK' },
               'top right front fan': {'class': 'Fans',
                                  'status': 'OK' },
               'top right middle fan': {'class': 'Fans',
                                  'status': 'OK' },
               'top right rear fan': {'class': 'Fans',
                                  'status': 'OK' },
               'bottom left front fan': {'class': 'Fans',
                                  'status': 'OK' },
               'bottom left middle fan': {'class': 'Fans',
                            'status': 'OK'},
               'bottom right middle fan': {'class': 'Fans',
                                  'status': 'OK' },
               'bottom right rear fan': {'class': 'Fans',
                                  'status': 'OK' },
               'rear tray top fan': {'class': 'Fans',
                                  'status': 'OK' },
               'rear tray second fan': {'class': 'Fans',
                                  'status': 'OK' },
               'rear tray third fan': {'class': 'Fans',
                                  'status': 'OK' },
               'rear tray fourth fan': {'class': 'Fans',
                                  'status': 'OK' },
                'rear tray fifth fan': {'class': 'Fans',
                                  'status': 'OK' },
               'rear tray sixth fan': {'class': 'Fans',
                                  'status': 'OK' },
               'rear tray seventh fan': {'class': 'Fans',
                                  'status': 'OK' },
                'rear tray bottom fan': {'class': 'Fans',
                                  'status': 'OK' },
                'bottom left rear fan': {'class': 'Fans',
                                  'status': 'OK' },
                'bottom right front fan': {'class': 'Fans',
                                  'status': 'OK' }}}
        result = chassis.check_chassis_fan(self.handle,env=env,speed='normal',count=20)
        self.assertEqual(result,True,"Result should be True")
        logging.info("Testcase11: comment is not there in TX model environment argument PASSED...\n")
 
        logging.info("Testcase 12: Fan is not there in chassis environment for TX Matrix")
        self.handle.get_model=MagicMock(return_value = 'TX Matrix')
        env_patch.return_value = {'scc':{'top left front':'spinning at normal speed',
		                        'top left middle':'spinning at normal speed','top left rear':'spinning at normal speed'}}
        env = {'scc':{'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}}
        result = chassis.check_chassis_fan(self.handle,env=env,speed='normal',count=3)
        self.assertEqual(result,False,"Result should be False")
        
        logging.info("Testcase 13: Fan is not there in chassis environment for TXP ")
        self.handle.get_model=MagicMock(return_value = 'TXP')
        env_patch.return_value = {'sfc 0':{'top left front':'spinning at normal speed',   
                                     'top left middle':'spinning at normal speed','top left rear':'spinning at normal speed'}}
        env = {'sfc 0':{'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}}
        result = chassis.check_chassis_fan(self.handle,env=env,speed='normal',count=3)
        self.assertEqual(result,False,"Result should be False")
     
        logging.info("Testcase 14: Fan is not there in chassis environment for m20 ")
        self.handle.get_model=MagicMock(return_value = 'm20')
        env_patch.return_value = {'top left front':'spinning at normal speed',                                                                           'top left middle':'spinning at normal speed','top left rear':'spinning at normal speed'}
        env = {'top left front fan': {'class': 'Fans',
                            'comment': 'Spinning at normal speed',
                            'status': 'OK'},
               'top left middle fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' },
               'top left rear fan': {'class': 'Fans',
                                  'comment': 'Spinning at normal speed',
                                  'status': 'OK' }}
        result = chassis.check_chassis_fan(self.handle,env=env,speed='normal',count=3)
        self.assertEqual(result,False,"Result should be False")

    def test_check_chassis_interface(self):
       
        logging.info(" Testing check_chassis_interface......") 
        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_interface') as interface_patch : 
            logging.info("\tTest Case 1 : Without passing interface Argument ")
            interface_patch.return_value = {'interface-information' : { 'physical-interface' : {'name' : 'fe-0/0/0'}}}
            result = chassis.check_chassis_interface(device=self.handle)
            self.assertEqual(result,True, 'Interface Information not matching')
            logging.info("\t\tTestcase Passed")

        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_interface') as interface_patch :
            logging.info("\tTest case 2 : Passing interface Argument(positive case)")
            interface_patch.return_value = {'interface-information' : { 'physical-interface' : {'name' : 'fe-0/0/0'}}}
            interface  = {'interface-information' : { 'physical-interface' : {'name' : 'fe-0/0/0'}}}
            result = chassis.check_chassis_interface(device=self.handle,interface=interface)
            self.assertEqual(result,True, 'Passed Interface Information not matching')
            logging.info("\t\tTestCase Passed")

        with patch('jnpr.toby.hardware.chassis.chassis.get_chassis_interface') as interface_patch :
            logging.info("\tTest case 3 : Passing interface Argument(negative case)")
            interface_patch.return_value = {'interface-information' : { 'physical-interface' : {'name' : 'fe-1/1/0'}}}
            interface = {'interface-information' : { 'physical-interface' : {'admin-status' : 'up'}}}
            result = chassis.check_chassis_interface(device=self.handle,interface=interface)
            self.assertEqual(result,False, 'Passed Interface Information not matching')
            logging.info("\t\tTestcase Passed")
        logging.info(" Successfully Tested")  
        logging.info("\n ###########################################################")
		
    @patch('jnpr.toby.hardware.chassis.chassis.get_chassis_hostname')
    @patch('jnpr.toby.hardware.chassis.chassis.Unix.__new__')
    def test_get_chassis_mib(self, mock_unix_new,
                             mock_chassis_hostname):
        logging.info(
            "Test case 1: Verify get_chassis_mib with the existed mib dir")
        mibs_dir = \
            "/volume/build/junos/15.1/release/15.1F5-S3.6/" + \
            "src/junos/shared/mibs"
        mock_chassis_hostname.return_value = "babson"
        res1 = 'exists'
        res2 = '''
jnxBoxClass.0 = OID: jnxProductLineMX240.0
jnxBoxDescr.0 = Juniper MX240 Internet Backbone Router
jnxBoxSerialNo.0 = JN11F66CFAFC
jnxBoxRevision.0 = 
jnxBoxInstalled.0 = Timeticks: (13297100) 1 day, 12:56:11.00
jnxContainersIndex.1 = 1
jnxContainersIndex.2 = 2
jnxContainersIndex.4 = 4
jnxContainersIndex.7 = 7
jnxContainersIndex.8 = 8
jnxContainersIndex.9 = 9
jnxContainersIndex.10 = 10
jnxContainersIndex.12 = 12
jnxContainersIndex.20 = 20
jnxContainersView.1 = 1
jnxContainersView.2 = 2
jnxContainersView.4 = 3
jnxContainersView.7 = 1
jnxContainersView.8 = 1
jnxContainersView.9 = 1
jnxContainersView.10 = 1
jnxContainersView.12 = 1
jnxContainersView.20 = 1
jnxContainersLevel.1 = 0
jnxContainersLevel.2 = 1
jnxContainersLevel.4 = 1
jnxContainersLevel.7 = 1
jnxContainersLevel.8 = 2
jnxContainersLevel.9 = 1
jnxContainersLevel.10 = 1
jnxContainersLevel.12 = 1
jnxContainersLevel.20 = 2
jnxContainersWithin.1 = 0
jnxContainersWithin.2 = 1
jnxContainersWithin.4 = 1
jnxContainersWithin.7 = 1
jnxContainersWithin.8 = 7
jnxContainersWithin.9 = 1
jnxContainersWithin.10 = 1
jnxContainersWithin.12 = 1
jnxContainersWithin.20 = 7
jnxContainersType.1 = OID: jnxChassisMX240.0
jnxContainersType.2 = OID: jnxMX240SlotPower.0
jnxContainersType.4 = OID: jnxMX240SlotFan.0
jnxContainersType.7 = OID: jnxMX240SlotFPC.0
jnxContainersType.8 = OID: jnxMX240MediaCardSpacePIC.0
jnxContainersType.9 = OID: jnxMX240SlotHM.0
jnxContainersType.10 = OID: jnxMX240SlotFPB.0
jnxContainersType.12 = OID: jnxMX240SlotCB.0
jnxContainersType.20 = OID: jnxMX240MediaCardSpaceMIC.0
jnxContainersDescr.1 = chassis frame
jnxContainersDescr.2 = PEM slot
jnxContainersDescr.4 = FAN slot
jnxContainersDescr.7 = FPC slot
jnxContainersDescr.8 = PIC slot
jnxContainersDescr.9 = Routing Engine slot
jnxContainersDescr.10 = FPM slot
jnxContainersDescr.12 = CB slot
jnxContainersDescr.20 = MIC slot
        '''
        mock_freebsd = Mock(spec=FreeBSD)
        mock_freebsd.shell.side_effect = [Response(response=res1),
                                          Response(response=res2)]
        mock_unix_new.return_value = mock_freebsd
        self.handle.get_model = MagicMock(return_value="mx240")
        result = chassis.get_chassis_mib(device=self.handle,mib_dir=mibs_dir)
        expected_result = {
            'chassis': {
                'jnxBoxSerialNo': 'JN11F66CFAFC',
                'jnxBoxInstalled': 'Timeticks: (13297100) 1 day, 12:56:11.00',
                'jnxBoxClass': 'OID: jnxProductLineMX240.0',
                'jnxBoxDescr': 'Juniper MX240 Internet Backbone Router',
                'jnxBoxRevision': ''
                },
            're slot': {
                'jnxContainersWithin': '1',
                'jnxContainersDescr': 'Routing Engine slot',
                'jnxContainersView': '1',
                'jnxContainersLevel': '1',
                'jnxContainersType': 'OID: jnxMX240SlotHM.0',
                'jnxContainersIndex': '9'
                },
            'fan slot': {
                'jnxContainersWithin': '1',
                'jnxContainersType': 'OID: jnxMX240SlotFan.0',
                'jnxContainersView': '3', 'jnxContainersLevel': '1',
                'jnxContainersDescr': 'FAN slot', 'jnxContainersIndex': '4'
                },
            'fpm slot': {
                'jnxContainersWithin': '1',
                'jnxContainersType': 'OID: jnxMX240SlotFPB.0',
                'jnxContainersView': '1', 'jnxContainersLevel': '1',
                'jnxContainersDescr': 'FPM slot', 'jnxContainersIndex': '10'
                },
            'mic slot': {
                'jnxContainersWithin': '7', 'jnxContainersDescr': 'MIC slot',
                'jnxContainersView': '1', 'jnxContainersLevel': '2',
                'jnxContainersType': 'OID: jnxMX240MediaCardSpaceMIC.0',
                'jnxContainersIndex': '20'},
            'pem slot': {
                'jnxContainersWithin': '1',
                'jnxContainersDescr': 'PEM slot', 'jnxContainersView': '2',
                'jnxContainersLevel': '1',
                'jnxContainersType': 'OID: jnxMX240SlotPower.0',
                'jnxContainersIndex': '2'
                },
            'chassis frame': {
                'jnxContainersWithin': '0',
                'jnxContainersType': 'OID: jnxChassisMX240.0',
                'jnxContainersView': '1', 'jnxContainersLevel': '0',
                'jnxContainersDescr': 'chassis frame',
                'jnxContainersIndex': '1'
                },
            'pic slot': {
                'jnxContainersWithin': '7',
                'jnxContainersType': 'OID: jnxMX240MediaCardSpacePIC.0',
                'jnxContainersView': '1', 'jnxContainersLevel': '2',
                'jnxContainersDescr': 'PIC slot', 'jnxContainersIndex': '8'
                },
            'fpc slot': {
                'jnxContainersWithin': '1',
                'jnxContainersType': 'OID: jnxMX240SlotFPC.0',
                'jnxContainersView': '1', 'jnxContainersLevel': '1',
                'jnxContainersDescr': 'FPC slot', 'jnxContainersIndex': '7'
                },
            'cb slot': {
                'jnxContainersWithin': '1', 'jnxContainersDescr': 'CB slot',
                'jnxContainersView': '1', 'jnxContainersLevel': '1',
                'jnxContainersType': 'OID: jnxMX240SlotCB.0',
                'jnxContainersIndex': '12'
                }
            }
        self.assertDictEqual(result, expected_result)
        logging.info("\t Check passed")

        logging.info(
            "Test case 2: Verify get_chassis_mib when failed to get mib dir")
        mibs_dir = ""
        mock_chassis_hostname.return_value = "babson"
        res1 = ''
        res2 = ''
        mock_freebsd = Mock(spec=FreeBSD)
        mock_freebsd.shell.side_effect = [Response(response=res1),
                                          Response(response=res2)]
        mock_unix_new.return_value = mock_freebsd
        self.handle.get_model = MagicMock(return_value="mx240")
        result = chassis.get_chassis_mib(device=self.handle,mib_dir=mibs_dir)
        expected_result = False
        self.assertEqual(result, expected_result)
        logging.info("\t Check passed")

        logging.info(
            "Test case 3: Verify get_chassis_mib when mib dir does not exist")
        mibs_dir = "/home/abc"
        mock_chassis_hostname.return_value = "babson"
        res1 = 'not found'
        res2 = ''
        mock_freebsd = Mock(spec=FreeBSD)
        mock_freebsd.shell.side_effect = [Response(response=res1),
                                          Response(response=res2)]
        mock_unix_new.return_value = mock_freebsd
        self.handle.get_model = MagicMock(return_value="mx240")
        result = chassis.get_chassis_mib(device=self.handle,mib_dir=mibs_dir)
        expected_result = False
        self.assertEqual(result, expected_result)
        logging.info("\t Check passed")

        logging.info(
            "Test case 4:")
        mibs_dir = \
            "/volume/build/junos/15.1/release/15.1F5-S3.6/" + \
            "src/junos/shared/mibs"
        mock_chassis_hostname.return_value = "babson"
        res1 = 'exists'
        res2 = '''
jnxContainersL1Index.1.0 = 
jnxContainersL1Index.1.1 = abc
jnxContainersL2Index.1.1.1 = abc
jnxContainersL3Index.1.1.1.1 = abc
jnxContainersL4Index.1 = abc
ABCDescr.1.1.1.1 = abc
ABCName.1.1.1.1 = abc
jnxContainersL1Index.1.1 = 1
jnxContainersL2Index.1.1.1 = 1
jnxContainersL3Index.1.1.1.1 = 1
jnxContainersL4Index.1 = 1
ABCDescr.1.1.1.1 = routing engine 1
ABCDescr.1.1.1.2 = routing engine
ABCDescr.1.1.1.3 = routing engine ABC
ABCDescr.1.1.1.4 = FPC slot 1
ABCDescr.1.1.1.5 = pic0@ 0/0/*
ABCDescr.1.1.1.6 = fpc0@ 0/*/*
ABCDescr.1.1.1.7 = sfm 0 spr
ABCName.1.1.1.1 = 1

        '''
        mock_freebsd = Mock(spec=FreeBSD)
        mock_freebsd.shell.side_effect = [Response(response=res1),
                                          Response(response=res2)]
        mock_unix_new.return_value = mock_freebsd
        self.handle.get_model = MagicMock(return_value="mx240")
        result = chassis.get_chassis_mib(device=self.handle,mib_dir=mibs_dir)
        expected_result = {'chassis': {}}
        self.assertDictEqual(result, expected_result)
        logging.info("\t Check passed")		

if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name+".log", level=logging.INFO)
    unittest.main()

