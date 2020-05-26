import os
import sys
import unittest2 as unittest
from nose.plugins.attrib import attr
from mock import patch, MagicMock

from jnpr.toby.logger.logger import Logger, get_script_name,get_log_dir
from jnpr.toby.utils.Vars import Vars

@attr('unit')
class TestLogger(unittest.TestCase):
    '''
    def test_logger_new(self):
        log_dir = os.path.join(os.getcwd()) + '/toby_logs'
        os.environ['TOBY_LOG_FOLDER'] = log_dir
        logger = Logger('Toby')
        #Get the log file name
        log_filename = os.path.join(log_dir, '.'.join(['test', 'Toby', 'log']))
        #Check if file is created
        self.assertTrue(os.path.isfile(log_filename))
        #Remove Log file 
        os.remove(log_filename)

        #Check with console=True
        logger = Logger('Toby', console=True)
        #Remove Log file 
        os.remove(log_filename)

        #Check with name as script name
        logger = Logger('test_logger')
        #Get the log file name 
        log_filename = os.path.join(log_dir, '.'.join(['test','test_logger','log']))
        #Check if file is created
        self.assertTrue(os.path.isfile(log_filename))
        #Remove Log file 
        os.remove(log_filename)

    def test_logger_new_without_mandatory_parameter(self):
        with self.assertRaises(TypeError):
            logger = Logger()

    def test_logger_log_dir(self):
        lobject = MagicMock(spec=Logger)
        lobject._log_dir = "test_str"
        self.assertEqual(Logger.log_dir(lobject), 'test_str')
    
    def test_logger_new_with_log_dir_env(self):
        os.environ['TOBY_LOG_LEVEL'] = 'info'
        logger = Logger('Toby')
        pid = str(os.getpid())
        log_dir = 'toby_logs'
        #Get the log file name
        log_filename = os.path.join(log_dir, '.'.join(['test', 'Toby', 'log']))
        #Check if file is created 
        self.assertTrue(os.path.isfile(log_filename))
        #Remove Log file
        os.remove(log_filename)
        del os.environ['TOBY_LOG_LEVEL']
    
    def test_logger_new_with_robot_log_dir_env(self):
        logger = Logger('Toby')
        log_dir = 'toby_logs'
        #Get the log file name
        log_filename = os.path.join(log_dir, '.'.join(['test', 'Toby', 'log']))
        #Check if file is created 
        self.assertTrue(os.path.isfile(log_filename))
        #Remove Log file and dir
        os.remove(log_filename)

    '''
    @patch('jnpr.toby.logger.logger.Vars')
    @patch('jnpr.toby.logger.logger.main')
    def test_logger_get_script_name(self, mock_main, mock_vars):
        mock_vars().get_global_variable = MagicMock(return_value='test_logger')
        self.assertEqual(get_script_name(), 'test_logger')
        mock_vars().get_global_variable = MagicMock(return_value=None)
        self.assertEqual(get_script_name(), 'toby')
        mock_main.__file__ = 'test_logger'
        self.assertEqual(get_script_name(), 'test_logger')
        mock_main.__file__ = ''
        self.assertRaises(Exception, get_script_name)
    
    @patch('jnpr.toby.logger.logger.get_log_dir',return_value='log_dir')
    @patch('jnpr.toby.logger.logger.get_script_name',return_value = 'test_script')
    @patch('jnpr.toby.logger.logger.logging')
    @patch('jnpr.toby.logger.logger.logging.Logger.__init__')
    @patch('jnpr.toby.logger.logger.logging.Logger.setLevel')
    @patch('jnpr.toby.logger.logger.logging.Logger.addHandler')
    @patch('jnpr.toby.logger.logger.os')
    def test_logger_init_(self,os_patch,super_addHandler,super_setLevel,super_init,logging_patch,script_patch,logdir_patch):
       	os_patch.environ  = {'TOBY_LOG_LEVEL' : 'INFO'}
        logging_patch.getLogger.return_value = 'test'
        mock_object = MagicMock(spec=logging_patch.Logger)
        os_patch.path.exists.return_value=False
        os_patch.makedirs.return_value = None
        os_patch.path.join.return_value ='log_file'
        Logger(name='test_name')
        os_patch.environ = {}
        os_patch.path.exists.return_value=True
        Logger(name='test_script',console=True)
     
    def test_logger_log_dir(self):
        mock_object = MagicMock(spec=Logger)
        mock_object._log_dir = 'test'
        self.assertEqual(Logger.log_dir(mock_object),'test')
    
    @patch('jnpr.toby.utils.Vars.Vars.get_global_variable')
    @patch('jnpr.toby.logger.logger.os')
    def test_logger_get_log_dir(self,os_patch,get_glbl_var_patch):
        os_patch.environ  = {'TOBY_LOG_FOLDER' : 'INFO'}        
        self.assertEqual(get_log_dir(),'INFO')
        os_patch.environ  = {}
        os_patch.getcwd.return_value = 'cwd'
        get_glbl_var_patch.return_value = 'test'
        os_patch.path.join.return_value = 'cwd'
        self.assertEqual(get_log_dir(),'test')
        get_glbl_var_patch.return_value = 'cwd'
        self.assertEqual(get_log_dir(),'cwd/toby_logs')


if __name__=='__main__':
    unittest.main()
