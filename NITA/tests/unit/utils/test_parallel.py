import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.utils.parallel import parallel as Parallel
from jnpr.toby.engines.verification.verifyEngine import verifyEngine
import builtins
from jnpr.toby.init.init import init
from robot.running.context import EXECUTION_CONTEXTS

class TestParallel(unittest.TestCase):
    
    def setUp(self):
        self.par = MagicMock(spec=Parallel)
        self.par._jobs = {}
        self.par._vars = {}
        self.par._jobs['default'] = {}
        self.par._vars['default'] = {}
        builtins.t = MagicMock(spec=init)
        t.background_logger = MagicMock()
        t.log = MagicMock()
 
    def tearDown(self):
        del self.par

    def test__init(self):
        par_obj = Parallel()
        self.assertIsInstance(par_obj, Parallel)
    
    def test_run_in_parallel(self):
        try:
            Parallel.run_in_parallel(self.par)
        except:
            self.assertRaises(Exception, "No keywords passed to run in parallel")
        self.par._run_all_tasks = MagicMock(return_value=True)
        self.assertEqual(Parallel.run_in_parallel(self.par, "Config Engine", "Run Event"), True)
        self.assertEqual(Parallel.run_in_parallel(self.par, "job=job1"), True)
        self.assertEqual(Parallel.run_in_parallel(self.par, "tasks=task1,task2"), True)
        self.assertEqual(Parallel.run_in_parallel(self.par, "job=job1", "tasks=task1,task2"), True)

    def test_create_job(self):
        try:
            Parallel.create_job(self.par)
        except:
            self.assertRaises(Exception, "Job name is not specified")
        self.par._jobs['default'] = {}
        try:
            Parallel.create_job(self.par, job="job1", tasks="task1,task2")
        except:
            self.assertRaises(Exception, "Task task1 is not defined")
        self.assertEqual(Parallel.create_job(self.par, job="job1"), None)
        self.par._jobs['default'] = {"task1": ["Config Engine"], "task2": ["Run Event"]}
        self.assertEqual(Parallel.create_job(self.par, job="job1", tasks="task1,task2"), None)

    def test_create_task(self):
        try:
            Parallel.create_task(self.par)
        except:
            self.assertRaises(Exception, "No arguments passed to create task")
        try:
            Parallel.create_task(self.par, "Config Engine", "Run Event")
        except:
            self.assertRaises(Exception, "Task name is not defined")
        mock_obj = MagicMock()
        self.assertEqual(Parallel.create_task(self.par, "task=task1", "$(output)","Config Engine", "", "Run Event", mock_obj), None)
        try:
            Parallel.create_task(self.par, "job=job1", "task=task1", "Config Engine")
        except:
            self.assertRaises(Exception, "Job job1 is not defined")
        self.par._jobs['job1'] = {}
        self.par._vars['job1'] = {}
        self.assertEqual(Parallel.create_task(self.par, "job=job1", "task=task1", "Config Engine"), None)
    
    def test_append_to_task(self):
        try:
            Parallel.append_to_task(self.par)
        except:
            self.assertRaises(Exception, "No arguments passed to create task")
        try:
            Parallel.append_to_task(self.par, "Config Engine", "Run Event")
        except:
            self.assertRaises(Exception, "Task name is not defined")
        mock_obj = MagicMock()
        self.assertEqual(Parallel.append_to_task(self.par, "task=task1", "$(output)","Config Engine", "", "Run Event", mock_obj), None)
        try:
            Parallel.append_to_task(self.par, "job=job1", "task=task1", "Config Engine")
        except:
            self.assertRaises(Exception, "Job job1 is not defined")
        self.par._jobs['job1'] = {}
        self.par._vars['job1'] = {}
        self.assertEqual(Parallel.append_to_task(self.par, "job=job1", "task=task1", "Config Engine"), None)
    
    @patch('jnpr.toby.utils.parallel.run_multiple') 
    def test__run_all_tasks(self, run_multiple_patch):
        try:
            Parallel._run_all_tasks(self.par)
        except:
            self.assertRaises(Exception, "No arguments passed to run")
        try:
            Parallel._run_all_tasks(self.par, tasks="task1")
        except:
            self.assertRaises(Exception, "Task task1 is not defined")
        run_multiple_patch.return_value = [False]
        self.par._jobs['default']['task1'] = ['Config Engine']
        try:
            Parallel._run_all_tasks(self.par, tasks="task1")
        except:
            self.assertRaises(Exception, "One or more tasks failed during execution")
        run_multiple_patch.return_value = [True]
        self.par._jobs['default']['task1'] = ['Config Engine']
        self.assertEqual(Parallel._run_all_tasks(self.par, tasks="task1"), [True])
        self.par._jobs['job1'] = {}
        self.par._jobs['job1']['task1'] = ['Config Engine']
        self.assertEqual(Parallel._run_all_tasks(self.par, job='job1'), [True])
        mock_obj = MagicMock()
        self.assertEqual(Parallel._run_all_tasks(self.par, None, None, 'Config Engine', mock_obj, 'device=r0'), [True])
    
    def test_get_var_from_task(self):
        try:
            Parallel.get_var_from_task(self.par)
        except:
            self.assertRaises(Exception)
        try:
            Parallel.get_var_from_task(self.par, task='task1')
        except:
            self.assertRaises(Exception)
        try:
            Parallel.get_var_from_task(self.par, task='task1', var='$(device)')
        except:
            self.assertRaises(Exception)
        self.par._vars['default']['task1'] = {'device': 'nanos'}
        try:
            Parallel.get_var_from_task(self.par, task='task1', var='$(resource)')
        except:
            self.assertRaises(Exception)
        self.assertEqual(Parallel.get_var_from_task(self.par, task='task1', var='device'), 'nanos')
 
    @patch('robot.libraries.BuiltIn.BuiltIn.get_library_instance') 
    def test__get_library_instance(self, lib_patch):
        self.assertEqual(Parallel._get_library_instance(self.par, 'init'), t)
        lib_patch.return_value = MagicMock()
        self.assertIsInstance(Parallel._get_library_instance(self.par, 'verification'), verifyEngine)
        # self.assertIsInstance(Parallel._get_library_instance(self.par, 'parallel'), Parallel)
        Parallel._get_library_instance(self.par, 'jnpr.toby.engines.verification.verifyEngine')
        Parallel._get_library_instance(self.par, 'RobotLib')

    def test__get_library_method(self):
        self.assertEqual(Parallel._get_library_method(self.par, 'get'), 'get_specific_data')
        self.assertEqual(Parallel._get_library_method(self.par, 'verify'), 'verify_specific_checks_api')
        self.assertEqual(Parallel._get_library_method(self.par, 'config engine'), 'config_engine')

    def test__resolve_vars(self):
        self.assertEqual(Parallel._resolve_vars(self.par), [])
        self.par._vars['default']['task1'] = {'device': 'nanos'} 
        self.assertEqual(Parallel._resolve_vars(self.par, job='default', task='task1', args=('$(device)',)), ['nanos'])
        try:
            Parallel._resolve_vars(self.par, job='default', task='task1', args=('$(resource)',))
        except:
            self.assertRaises(Exception, "Variable resource is not defined")
    
    @patch('robot.running.context.EXECUTION_CONTEXTS')
    def test__get_handler_from_keyword(self, context_patch):
        try:
            Parallel._get_handler_from_keyword(self.par, 'Log')
        except:
            self.assertRaises(Exception)
                            

if __name__ == '__main__':
    unittest.main()        
