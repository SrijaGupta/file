# pylint: disable=undefined-variable,invalid-name,bad-whitespace,missing-docstring

import builtins
from datetime import datetime
import unittest2 as unittest
from mock import patch, MagicMock
from jnpr.toby.engines.monitor.MonitoringEngine import pd as pandas
from jnpr.toby.engines.monitor.MonitoringEngine import ET as etree
from jnpr.toby.utils.response import Response
from pandas.compat import StringIO
from jnpr.toby.init.init import init
from jnpr.toby.engines.monitor.MonitoringEngine import Device
from jnpr.toby.engines.monitor.MonitoringEngine import TobyException
from jnpr.toby.engines.monitor.MonitoringEngine import MonitoringEngine


class TestMonitoringEngine(unittest.TestCase):

    def setUp(self):
        builtins.t = MagicMock(spec=init)
        t.is_robot = True
        t._script_name = "test_init"
        t.background_logger = MagicMock()
        t.log = MagicMock()
        create_t_data()
        t.resources = t.t_dict['resources']
        t.__getitem__ = MagicMock(return_value=t.t_dict['resources'])
        builtins.dev = MagicMock(spec=Device)
        dev.get_version = MagicMock(return_value='16.1')
        dev.is_evo = MagicMock(return_value=False)
        builtins.mon = MagicMock(spec=MonitoringEngine)
        builtins.TESTDATA = StringIO("""DATETIME,HOST,TYPE,FRU,MEM,CPU
                            2017-11-11 14:38:35.588368,sachem,RE,re0,29,3
                            2017-11-11 14:38:35.588368,sachem,RE,re1,22,3
                            2017-11-11 14:38:38.652501,sachem,RE,re0,29,34
                            2017-11-11 14:38:38.652501,sachem,RE,re1,22,10
                            2017-11-11 14:38:41.664695,sachem,RE,re0,29,21
                            2017-11-11 14:38:41.664695,sachem,RE,re1,22,10
                            2017-11-11 14:38:44.317696,sachem,RE,re0,29,21
                            2017-11-11 14:38:44.317696,sachem,RE,re1,22,10
                            2017-11-11 14:38:47.667680,sachem,RE,re0,29,25
                            2017-11-11 14:38:47.667680,sachem,RE,re1,22,10
                            2017-11-11 14:38:50.665835,sachem,RE,re0,29,14
                            2017-11-11 14:38:50.665835,sachem,RE,re1,22,10
                            2017-11-11 14:38:54.350929,sachem,RE,re0,29,14
                            2017-11-11 14:38:54.350929,sachem,RE,re1,22,10
                            2017-11-11 14:38:57.060702,sachem,RE,re0,29,24
                            2017-11-11 14:38:57.060702,sachem,RE,re1,23,17
                            2017-11-11 14:38:59.862547,sachem,RE,re0,29,24
                            2017-11-11 14:38:59.862547,sachem,RE,re1,23,17
                            2017-11-11 14:39:02.744849,sachem,RE,re0,29,21
                            2017-11-11 14:39:02.744849,sachem,RE,re1,23,17
                            2017-11-11 14:39:06.024669,sachem,RE,re0,29,21
                            2017-11-11 14:39:06.024669,sachem,RE,re1,23,17
                            2017-11-11 14:38:35.820504,sachem,PFE,fpc0,25,26
                            2017-11-11 14:38:35.820504,sachem,PFE,fpc1,21,14
                            2017-11-11 14:38:35.820504,sachem,PFE,fpc2,21,15
                            2017-11-11 14:38:35.820504,sachem,PFE,fpc3,24,25
                            2017-11-11 14:38:35.820504,sachem,PFE,fpc4,23,35
                            2017-11-11 14:38:39.278710,sachem,PFE,fpc0,25,24
                            2017-11-11 14:38:39.278710,sachem,PFE,fpc1,21,14
                            2017-11-11 14:38:39.278710,sachem,PFE,fpc2,21,15
                            2017-11-11 14:38:39.278710,sachem,PFE,fpc3,24,39
                            2017-11-11 14:38:39.278710,sachem,PFE,fpc4,23,35
                            2017-11-11 14:38:41.891458,sachem,PFE,fpc0,25,24
                            2017-11-11 14:38:41.891458,sachem,PFE,fpc1,21,14
                            2017-11-11 14:38:41.891458,sachem,PFE,fpc2,21,15
                            2017-11-11 14:38:41.891458,sachem,PFE,fpc3,24,39
                            2017-11-11 14:38:41.891458,sachem,PFE,fpc4,23,36
                            2017-11-11 14:38:44.588638,sachem,PFE,fpc0,25,24
                            2017-11-11 14:38:44.588638,sachem,PFE,fpc1,21,14
                            2017-11-11 14:38:44.588638,sachem,PFE,fpc2,21,15
                            """)
        builtins.MIN = StringIO("""min(MEM)
                       12
                       """)
        builtins.MAX = StringIO("""max(MEM)
                       14
                       """)
        builtins.AVG = StringIO("""avg(MEM)
                       13
                       """)
        builtins.MINC = StringIO("""min(CPU)
                        12
                        """)
        builtins.MAXC = StringIO("""max(CPU)
                        14
                        """)
        builtins.AVGC = StringIO("""avg(CPU)
                        13
                        """)

    def test__init(self):
        new_mon = MonitoringEngine()
        self.assertIsInstance(new_mon, MonitoringEngine)


    @patch('jnpr.toby.engines.monitor.MonitoringEngine.threading.Thread')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._find_file')
    @patch('builtins.open')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.fsync')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.yaml.safe_load')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.Device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.py.offline.plot')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    def test_monitoring_engine_start_monitor(self, sqlite_patch, isfile_patch, starttime_patch, plotly_patch,
                                             pandas_patch, device_patch,
                                             sleep_patch, safe_load_patch, fsync_patch, open_patch, find_file_patch, thread_patch):
        mon.is_running = False
        sqlite_patch.return_value = 'Test'
        sleep_patch.return_value = True
        device_patch.return_value = dev
        df = pandas.read_csv(TESTDATA, sep=',', parse_dates=['DATETIME'])
        pandas_patch.return_value = df
        plotly_patch.return_value = True
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')

        t.resources['r0']['system']['primary']['osname'] = 'abcd'
        self.assertIsNone(MonitoringEngine.monitoring_engine_start_monitor(mon, interval=1, log_level='ERROR')) 

        mon.is_running = False
        t.resources['r0']['system']['primary']['osname'] = 'JunOS'
        isfile_patch.return_value = True
        safe_load_patch.return_value = {'r0': {}}
        self.assertIsNone(MonitoringEngine.monitoring_engine_start_monitor(mon, interval=1, log_level='ERROR'))

        mon.is_running = False
        t.resources['r0']['system']['primary']['osname'] = 'JunOS'
        safe_load_patch.return_value = {'r1': {}}
        self.assertIsNone(MonitoringEngine.monitoring_engine_start_monitor(mon, interval=1, log_level='ERROR'))


        mon.is_running = False
        safe_load_patch.return_value = {'r0': {'unstructured_data': [{'mpls': [{'trace1': {'cmd': 'Test'}}]}],
                                               'data': [{'graph1': [{'trace1': {'cmd': 'Test'}}]}],
                                               'processes': ['rpd'], 'syslog': ['Test'], 'custom_data' : ['Test']}}
        self.assertIsNone(MonitoringEngine.monitoring_engine_start_monitor(mon, nomonlist=['r0', 'r1']))

        isfile_patch.return_value = False
        t.get_resource_list.return_value = ['r0']
        thread_patch.return_value = MagicMock()
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_start_monitor(mon, interval=1, infile='monitor.yaml', log_level='ERROR'))

        mon.is_running = True
        self.assertIsNone(MonitoringEngine.monitoring_engine_start_monitor(mon, interval=1, log_level='ERROR'))



    @patch('jnpr.toby.engines.monitor.MonitoringEngine.threading.Thread.join')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    def test_monitoring_engine_stop_monitor(self, sleep_patch, join_patch):
        mon.threads = [MagicMock(), MagicMock()]
        join_patch.return_value = True
        mon.interval = 1
        sleep_patch.return_value = True
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_stop_monitor(mon))
        mon.is_running = True
        self.assertIsNone(MonitoringEngine.monitoring_engine_stop_monitor(mon))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.fsync')
    def test_monitoring_engine_annotate(self, fsync_patch, sleep_patch):
        sleep_patch.return_value = True
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_annotate(mon, annotation='annotation1'))
        mon.is_running = True
        fsync_patch.return_value = True
        self.assertIsNone(MonitoringEngine.monitoring_engine_annotate(mon, annotation='annotation1'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    def test_monitoring_engine_get_pfe_memory_minimum(self, sleep_patch, starttime_patch, pandas_patch, isfile_patch,
                                                      sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        sleep_patch.return_value = True
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon))
        df = pandas.read_csv(MIN)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon, resource='r0'), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon, resource='r0', fru='fpc0'), 12)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_minimum(mon, resource='r0', fru='fpc0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    def test_monitoring_engine_get_pfe_memory_maximum(self, sleep_patch, starttime_patch, pandas_patch, isfile_patch,
                                                      sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        sleep_patch.return_value = True
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon))
        df = pandas.read_csv(MAX)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon, resource='r0'), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon, resource='r0', fru='fpc0'), 14)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_maximum(mon, resource='r0', fru='fpc0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    def test_monitoring_engine_get_pfe_memory_average(self, sleep_patch, starttime_patch, pandas_patch, isfile_patch,
                                                      sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        sleep_patch.return_value = True
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon))
        df = pandas.read_csv(AVG)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon, resource='r0'), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon, resource='r0', fru='fpc0'), 13)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_memory_average(mon, resource='r0', fru='fpc0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_pfe_cpu_minimum(self, sleep_patch, starttime_patch, pandas_patch, isfile_patch,
                                                   sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        sleep_patch.return_value = True
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon))
        df = pandas.read_csv(MINC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon, resource='r0'), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon, resource='r0', fru='fpc0'), 12)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_minimum(mon, resource='r0', fru='fpc0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_pfe_cpu_maximum(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon))
        df = pandas.read_csv(MAXC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon, resource='r0'), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon, resource='r0', fru='fpc0'), 14)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_maximum(mon, resource='r0', fru='fpc0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_pfe_cpu_average(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon))
        df = pandas.read_csv(AVGC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon, resource='r0'), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon, resource='r0', fru='fpc0'), 13)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_pfe_cpu_average(mon, resource='r0', fru='fpc0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_re_memory_minimum(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon))
        df = pandas.read_csv(MIN)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon, resource='r0'), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon, resource='r0', fru='re0'), 12)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_minimum(mon, resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_re_memory_maximum(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon))
        df = pandas.read_csv(MAX)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon, resource='r0'), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon, resource='r0', fru='re0'), 14)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_maximum(mon, resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_re_memory_average(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_average(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_average(mon))
        df = pandas.read_csv(AVG)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_average(mon), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_average(mon, resource='r0'), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_memory_average(mon, resource='r0', fru='re0'), 13)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_average(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_average(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_memory_average(mon, resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_re_cpu_minimum(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon))
        df = pandas.read_csv(MINC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon, resource='r0'), 12)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon, resource='r0', fru='re0'), 12)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_minimum(mon, resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_re_cpu_maximum(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon))
        df = pandas.read_csv(MAXC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon, resource='r0'), 14)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon, resource='r0', fru='re0'), 14)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_maximum(mon, resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    def test_monitoring_engine_get_re_cpu_average(self, starttime_patch, pandas_patch, isfile_patch, sqlite_patch):
        starttime_patch.return_value = datetime.strptime(str('2017-11-11 14:38:35.820504'), '%Y-%m-%d %H:%M:%S.%f')
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon))
        df = pandas.read_csv(AVGC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon, resource='r0'), 13)
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon, resource='r0', fru='re0'), 13)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon, resource='r0'))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_cpu_average(mon, resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    def test_monitoring_engine_get_re_process_memory_minimum(self, pandas_patch, isfile_patch, sqlite_patch):
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd'))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd'))
        df = pandas.read_csv(MIN)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd'), 12)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd', resource='r0'), 12)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd', resource='r0',
                                                                             fru='re0'), 12)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd', resource='r0',
                                                                             fru='re0'))
        pandas_patch.return_value = pandas.DataFrame({'min(MEM)': [None]})
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_minimum(mon, process='rpd', resource='r0',
                                                                             fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    def test_monitoring_engine_get_re_process_memory_maximum(self, pandas_patch, isfile_patch, sqlite_patch):
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd'))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd'))
        df = pandas.read_csv(MAX)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd'), 14)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd', resource='r0'), 14)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd', resource='r0',
                                                                             fru='re0'), 14)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd', resource='r0',
                                                                             fru='re0'))
        pandas_patch.return_value = pandas.DataFrame({'max(MEM)': [None]})
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_maximum(mon, process='rpd', resource='r0',
                                                                             fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    def test_monitoring_engine_get_re_process_memory_average(self, pandas_patch, isfile_patch, sqlite_patch):
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd'))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd'))
        df = pandas.read_csv(AVG)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd'), 13)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd', resource='r0'), 13)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd', resource='r0',
                                                                             fru='re0'), 13)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd', resource='r0',
                                                                             fru='re0'))
        pandas_patch.return_value = pandas.DataFrame({'avg(MEM)': [None]})
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_memory_average(mon, process='rpd', resource='r0',
                                                                             fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    def test_monitoring_engine_get_re_process_cpu_minimum(self, pandas_patch, isfile_patch, sqlite_patch):
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd'))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd'))
        df = pandas.read_csv(MINC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd'), 12)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd', resource='r0'), 12)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd', resource='r0', fru='re0'),
            12)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd', resource='r0', fru='re0'))
        pandas_patch.return_value = pandas.DataFrame({'min(CPU)': [None]})
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_minimum(mon, process='rpd', resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    def test_monitoring_engine_get_re_process_cpu_maximum(self, pandas_patch, isfile_patch, sqlite_patch):
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd'))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd'))
        df = pandas.read_csv(MAXC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd'), 14)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd', resource='r0'), 14)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd', resource='r0', fru='re0'),
            14)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd', resource='r0', fru='re0'))
        pandas_patch.return_value = pandas.DataFrame({'max(CPU)': [None]})
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_maximum(mon, process='rpd', resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.sqlite3')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.path.isfile')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    def test_monitoring_engine_get_re_process_cpu_average(self, pandas_patch, isfile_patch, sqlite_patch):
        mon.is_running = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd'))
        mon.is_running = True
        isfile_patch.return_value = False
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd'))
        df = pandas.read_csv(AVGC)
        pandas_patch.return_value = df
        isfile_patch.return_value = True
        sqlite_patch.connect.return_value = MagicMock()
        sqlite_patch.close.return_value = True
        self.assertEqual(MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd'), 13)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd', resource='r0'), 13)
        self.assertEqual(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd', resource='r0', fru='re0'),
            13)
        pandas_patch.return_value = pandas.DataFrame()
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd', resource='r0', fru='re0'))
        pandas_patch.return_value = pandas.DataFrame({'avg(CPU)': [None]})
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd', resource='r0'))
        self.assertIsNone(
            MonitoringEngine.monitoring_engine_get_re_process_cpu_average(mon, process='rpd', resource='r0', fru='re0'))

    @patch('jnpr.toby.engines.monitor.MonitoringEngine._strip_xml_namespace')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_cli_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.reconnect_to_device') 
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.DataFrame.to_sql')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_controller')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.py.offline.plot')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.stat')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_csv')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.create_engine')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.makedirs')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.Device.__new__')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_device_log_level')
    def test__monitor_re_data(self, log_level_patch, device_patch, os_makedirs_patch, create_engine_patch,
                              pandas_read_csv_patch,
                              os_stat_patch, pandas_read_sql_query_patch, plotly_patch, set_current_controller_patch,
                              pandas_to_sql_patch, sleep_patch, reconnect_to_device_patch, execute_cli_command_on_device_patch,
                              strip_xml_namespace_patch):
        data = [{'graph1': None},
                {'graph2': [{'trace1': None},
                            {'trace2': {'xpath': 'Test', 'cmd': 'Test'}},
                            {'trace3': {'xpath': 'Test', 'cmd': 'Test'}}]},
                {'graph3': [{'trace1': {'xpath': 'Test', 'cmd': 'Test'}},
                            {'trace2': {'xpath': None, 'cmd': 'Test'}},
                            {'trace3': {'xpath': 'Test', 'cmd': 'Test'}},
                            {'trace4': {'xpath': 'Test', 'cmd': 'Test'}},
                            {'trace5': {'xpath': 'Test', 'cmd': 'Test', 'alert': '100'}}]}]
        data2 = [{'graph1': None},
                 {'graph2': [{'trace1': None},
                             {'trace2': {'xpath': 'Test', 'cmd': 'Test'}},
                             {'trace3': {'xpath': 'Test', 'cmd': 'Test'}}]},
                 {'graph3': [{'trace1': {'xpath': 'Test', 'cmd': 'Test'}},
                             {'trace2': {'xpath': None, 'cmd': 'Test'}},
                             {'trace3': {'xpath': 'Test', 'cmd': 'Test'}},
                             {'trace4': {'xpath': 'Test', 'cmd': 'Test'}},
                             {'trace5': {'xpath': 'Test', 'cmd': 'Test', 'alert': None}},
                             {'trace5': {'xpath': 'Test', 'cmd': 'Test', 'alert': '100'}},
                             {'trace6': {'xpath': 'Test', 'cmd': 'Test', 'alert': '100'}}]}]
        mon.is_running = False
        log_level_patch.return_value = True
        device_patch.return_value = builtins.dev
        device_patch.get_version.retrun_value = dev.get_version
        create_engine_patch.return_value = 'Test'
        set_current_controller_patch.return_value = 'Test'
        os_makedirs_patch.return_value = 'Test'
        pandas_read_csv_patch.return_value = pandas.DataFrame({'DATETIME': ['Test'], 'ANNOTATION': ['Test']})
        pandas_read_sql_query_patch.side_effect = [pandas.DataFrame(), pandas.DataFrame({'DATETIME': [], 'DATA': []}),
                                                   pandas.DataFrame(),
                                                   pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame(),
                                                   pandas.DataFrame({'DATETIME': ['Test'], 'DATA': ['Test']})]
        plotly_patch.return_value = True

        os_stat_patch.return_value = MagicMock(st_size=0)
        self.assertIsNone(
            MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data, log_level='ERROR'))

        os_stat_patch.return_value = MagicMock(st_size=1)
        self.assertIsNone(
            MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data, log_level='ERROR'))

        os_stat_patch.side_effect = Exception('Test')
        self.assertIsNone(
            MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data, log_level='ERROR'))

        mon.is_running = True
        dev.current_node = MagicMock()
        dev.current_node.is_node_master = MagicMock(side_effect=[Exception('Test'), Exception('Test'), False, False, False, False,
                                                                 False, False, False, False, False, True,
                                                                 Exception('Test')])
        dev.current_node.controllers = MagicMock()                           
        dev.current_node.controllers.keys = MagicMock(return_value=['re0', 're1'])
        dev.get_rpc_equivalent = MagicMock(
            side_effect=[None, Exception('Test'), 'Test', 'Test', 'Test', 'Test', 'Test'])
        dev.execute_rpc = MagicMock(side_effect=[Exception('Test'), Response(status=True, response=None),
                                                 Response(status=True, response=etree.fromstring('<A></A>')),
                                                 Response(status=True,
                                                          response=etree.fromstring('<A><Test>Test</Test></A>')),
                                                 Response(status=True,
                                                          response=etree.fromstring('<A><Test>100</Test></A>'))])
        pandas_to_sql_patch.side_effect = [Exception('Test'),
                                           'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test',
                                           Exception('Test'),
                                           'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test','Test', 'Test',
                                           Exception('Test'), Exception('Test'), 'Test',
                                           Exception('Test'), Exception('Test'),
                                           Exception('Test')] 
        reconnect_to_device_patch.return_value = True 
        execute_cli_command_on_device_patch.side_effect = [Exception('Test'), Exception('Test'), 'Test', 'Test',
                                                          'Test', 'Test', 'Test', 'Test', 'Test', 'Test',
                                                           Exception('Test')]
        Test = MagicMock()
        Test.findtext.side_effect  = [None, 'Test', 123, 123, 70, 123]
        strip_xml_namespace_patch.side_effect = [Exception('Test'), None, Test, Test, Test, Test, Test, Test]
        os_stat_patch.side_effect = [Exception('Test'), MagicMock(st_size=0), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1),MagicMock(st_size=1),
                                     MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1),MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1)]

        MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data, log_level='ERROR')

        MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data, log_level='ERROR')

        MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data2, log_level='ERROR')

        dev.current_node.controllers.keys = MagicMock(return_value=['re0'])
        MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data2, log_level='ERROR')

        mon.is_running = False
        t.get_resource_list.return_value = ['r0'] 
        MonitoringEngine._monitor_re_data(mon, resource='r0', interval=1, data=data, log_level='OFF') 


    @patch('jnpr.toby.engines.monitor.MonitoringEngine.create_engine')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.reconnect_to_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.DataFrame.to_sql')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.re.search')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_vty_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.switch_to_superuser')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_shell_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_cli_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_controller')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.py.offline.plot')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.stat')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_csv')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.makedirs')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.Device.__new__')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_device_log_level')
    def test__monitor_re_unstructured_data(self, log_level_patch, device_patch, os_makedirs_patch,
                                           pandas_read_csv_patch, os_stat_patch, pandas_read_sql_query_patch,
                                           plotly_patch, set_current_controller_patch, execute_cli_command_patch,
                                           execute_shell_command_patch,
                                           switch_to_superuser_patch, execute_vty_command_patch, re_search_patch,
                                           pandas_to_sql_patch, sleep_patch, reconnect_patch, create_engine_patch):
        running_data1 = [{'graph1': None},
                        {'graph2': [{'trace1': None}, 
                                    {'trace2': {'mode': 'Test'}}, 
                                    {'trace3': {'cmd': 'Test', 'parameters': [{'parameter1': None},
                                                                              {'parameter2': {'label': 'Test'}},
                                                                              {'parameter3': {'group': 'Test'}},
                                                                              {'parameter4': {'group': 'Test'}}]}},
                                    {'trace4': {'cmd': 'Test', 'mode': 'Test', 'regexp': 'Test', 'parameters': [{'parameter1': {'group': 'Test'}}]}}]}]
        running_data2 = [{'graph1': [{'trace1': {'mode': 'Test'}},
                                     {'trace2': {'mode': 'Test'}},
                                     {'trace3': {'cmd': 'Test',
                                                 'parameters': [{'parameter2': {'label': 'Test'}}]}},
                                     {'trace4': {'cmd': 'Test', 'mode': 'Test', 'regexp': 'Test', 
                                                 'parameters': [{'parameter1': {'group': 'Test'}},
                                                                {'parameter2': {'group': 0, 'regexp' : 'Test'}}]}}]}]
        running_data3 = [{'graph1': [{'trace1': {'cmd': 'Test', 'parameters': [{'parameter1': {'label': 'Test'}}]}},
                                     {'trace2': {'cmd': 'Test', 'mode': 'Shell', 'regexp': 'Test', 
                                                 'parameters': [{'parameter1': {'group': 'Test'}},
                                                                {'parameter2': {'group': 0, 'regexp' : 'Test'}}]}}]}]
        running_data4 = [{'graph1': [{'trace1': {'cmd': 'Test', 'mode': 'Shell', 'parameters': [{'parameter1': {'label': 'Test'}}]}},
                                     {'trace2': {'cmd': 'Test', 'mode': 'Root', 'regexp': 'Test', 
                                                 'parameters': [{'parameter1': {'group': 'Test'}},
                                                                {'parameter2': {'group': 0, 'regexp' : 'Test'}}]}}]}]
        running_data5 = [{'graph1': [{'trace1': {'cmd': 'Test', 'mode': 'Root', 'parameters': [{'parameter1': {'label': 'Test'}}]}},
                                     {'trace2': {'cmd': 'Test', 'mode': 'Vty', 'regexp': 'Test', 
                                                 'parameters': [{'parameter1': {'group': 'Test'}},
                                                                {'parameter2': {'group': 0, 'regexp' : 'Test'}}]}}]}]
        running_data6 = [{'graph1': [{'trace1': {'cmd': 'Test', 'mode': 'Vty', 'parameters': [{'parameter1': {'label': 'Test'}}]}},
                                     {'trace2': {'cmd': 'Test', 'mode': 'Vty', 'regexp': 'Test', 
                                                 'parameters': [{'parameter1': {'group': 'Test'}},
                                                                {'parameter2': {'group': 0, 'regexp' : 'Test'}}]}},
                                     {'trace3': {'cmd': 'Test', 'mode': 'Vty', 'parameters': [{'parameter1': None},
                                                                                              {'parameter2': {'label': 'Test'}},
                                                                                              {'parameter3': {'group': 'Test'}},
                                                                                              {'parameter3': {'group': 'Test', 'regexp': 'Test'}},
                                                                                              {'parameter4': {'group': 'Test', 'regexp': 'Test'}},
                                                                                              {'parameter5': {'group': 'Test', 'regexp': 'Test'}},
                                                                                              {'parameter6': {'group': 'Test', 'regexp': 'Test'}}]}},
                                     {'trace4': {'cmd': 'Test', 'mode': 'Vty', 'regexp': 'Test', 'parameters': [{'parameter1': {'group': 'Test'}}]}}]}]
        stopped_data = [{'graph1': None},
		        {'graph2': [{'trace1': None}, 
			            {'trace2': {'mode': 'Test'}},
                                    {'trace3': {'cmd': 'Test', 'parameters': [{'parameter1': None},
				                                              {'parameter2': {'group': 'Test'}},
                                                                              {'parameter3': {'label': 'Test'}},
                                                                              {'parameter4': {'label': 'Test', 'regexp': 'Test'}}]}},
                                    {'trace4': {'cmd': 'Test', 'regexp': 'Test', 'parameters': [{'parameter1': {'label': 'Test'}},
                                                                                                {'parameter2': {'label': 'Test'}}]}}]},
                        {'graph3': [{'trace1': {'cmd': 'Test', 'regexp': 'Test', 'parameters': [{'parameter1': {'label': 'Test'}}]}}]}]
        mon.is_running = True
        sleep_patch.return_value = None #<--
        log_level_patch.return_value = True
        device_patch.return_value = builtins.dev
        device_patch.get_version.return_value = dev.get_version
        os_makedirs_patch.return_value = 'Test'
        pandas_read_csv_patch.side_effect = [pandas.DataFrame({'DATETIME': ['Test'], 'ANNOTATION': ['Test']})]
        pandas_read_sql_query_patch.side_effect = [pandas.DataFrame(),
                                                   pandas.DataFrame({'DATETIME': ['Test'], 'DATA': ['Test']}),
                                                   pandas.DataFrame()]
        plotly_patch.return_value = True
        dev.current_node = MagicMock()
        dev.current_node.is_node_master = MagicMock(return_value=False)
        dev.current_node.controllers = MagicMock()                                 
        dev.current_node.controllers.keys = MagicMock(return_value=['re0', 're1'])

        dev.current_node.is_node_master.side_effect = [Exception('Test'), Exception('Test'), False, True, True, True, True, True, True, True,
                                                       True, True, True, True, Exception('Test')]
        os_stat_patch.side_effect = [Exception('Test'), MagicMock(st_size=0), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1),
                                     MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1), MagicMock(st_size=1)]
        pandas_to_sql_patch.side_effect = [Exception('Test1'), 'Test2', 'Test3', Exception('Test4'),
                                           'Test5', 'Test6', Exception('Test7'),
                                           'Test8', 'Test9', Exception('Test10'),
                                           'Test11', 'Test12', Exception('Test13'),
                                           'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', Exception('Test'), Exception('Test'), Exception('Test'),
                                           Exception('Test')]
        execute_cli_command_patch.side_effect = [Exception('Test'), Exception('Test'), Exception('Test')]
        execute_shell_command_patch.side_effect = [Exception('Test'), Exception('Test'), Exception('Test'), Exception('Test')]
        execute_vty_command_patch.side_effect = [Exception('Test'), Exception('Test'), None, 'Test', 'Test']
        Test = MagicMock()
        Test.group.side_effect = [False, 'Test', '123', '123']
        re_search_patch.side_effect = [False, Test, Test, Test, Test]

        MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=running_data1, log_level='OFF')

        MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=running_data2, log_level='ERROR') 

        MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=running_data3, log_level='ERROR')

        MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=running_data4, log_level='ERROR')

        MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=running_data5, log_level='ERROR')

        MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=running_data6, log_level='ERROR') 

        dev.current_node.controllers.keys = MagicMock(return_value=['re0']) 
        MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=running_data3, log_level='ERROR')


        mon.is_running = False
        os_stat_patch.side_effect = [Exception('Test'), MagicMock(st_size=0), MagicMock(st_size=1), MagicMock(st_size=1)]
        self.assertIsNone(MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=stopped_data, log_level='ERROR'))

        t.get_resource_list.return_value = ['r0']
        self.assertIsNone(MonitoringEngine._monitor_re_unstructured_data(mon, resource='r0', interval=1, data=stopped_data, log_level='ERROR'))


    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_cli_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.reconnect_to_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._get_testcase_starttime')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_shell_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_controller')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_system_node')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.Device.__new__')
    def test__monitor_re_syslog(self, device_patch, set_system_node_patch, set_current_controller_patch,
                                execute_shell_command_patch, sleep_patch, testcase_starttime_patch,
                                reconnect_to_device_patch, execute_cli_command_patch):
        mon.is_running = True
        sleep_patch.return_value = Exception('Test')
        device_patch.return_value = builtins.dev
        dev.get_current_controller_name = MagicMock(return_value='Test')
        device_patch.get_current_controller_name.return_value = dev.get_current_controller_name
        dev.get_current_controller_name = MagicMock(side_effect=[None, 'Test', 'Test', 'Test', 'Test', 'Test', 'Test','Test'])
        dev.nodes = MagicMock()
        dev.nodes.keys = MagicMock(return_value=['primary'])
        dev.current_node = MagicMock()
        dev.current_node.controllers = MagicMock()
        dev.current_node.controllers.keys = MagicMock(return_value=['re0'])
        testcase_starttime_patch.side_effect = [False, datetime.strptime(str('2017-11-11 14:38:35.820504'),'%Y-%m-%d %H:%M:%S.%f'),
                                                       datetime.strptime(str('2017-11-11 14:38:35.820504'),'%Y-%m-%d %H:%M:%S.%f'),
                                                       datetime.strptime(str('2017-11-11 14:38:35.820504'),'%Y-%m-%d %H:%M:%S.%f'),
                                                       datetime.strptime(str('2017-11-11 14:38:35.820504'),'%Y-%m-%d %H:%M:%S.%f'),
                                                       datetime.strptime(str('2017-11-11 14:38:35.820504'),'%Y-%m-%d %H:%M:%S.%f'),
                                                       datetime.strptime(str('2017-11-11 14:38:35.820504'),'%Y-%m-%d %H:%M:%S.%f')]


        execute_shell_command_patch.side_effect = [Exception('Test'), Exception('Test'), 'Test', Exception('Test'),
                                                   'Test', 'Test', 'Jun 26 15:41:47 2018', 'Jun 26 15:42:47 2018', Exception('Test')]
        execute_cli_command_patch.side_effect = [Exception('Test'), 'a\nb', Exception('Test'), 
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n', '',
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwap a nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 'Oct 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 'Dec 28 18:00:06 Mem:\nSwap:\n 0K \nSwa1p % nice, ---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n']
        reconnect_to_device_patch.side_effect = [Exception('Test'), True, Exception('Test')]

        mon.syslog_alerts = {}
        try:
            MonitoringEngine._monitor_re_syslog(mon, resource='r0', interval=1, syslog=['Test'], log_level='ERROR')
        except:
            self.assertRaises(Exception)

        MonitoringEngine._monitor_re_syslog(mon, resource='r0', interval=1, syslog=['Test', None], log_level='ERROR')

        t.get_resource_list.return_value = ['r0']
        MonitoringEngine._monitor_re_syslog(mon, resource='r0', interval=1, syslog=None, log_level='OFF')

        t.get_resource_list.return_value = ['r1']
        try:
            MonitoringEngine._monitor_re_syslog(mon, resource='r0', interval=1, syslog=None, log_level='OFF')
        except:
            self.assertRaises(Exception)

        mon.is_running = False
        MonitoringEngine._monitor_re_syslog(mon, resource='r0', interval=1, syslog=['Test', None], log_level='ERROR')

    @patch('jnpr.toby.engines.monitor.MonitoringEngine.reconnect_to_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.DataFrame.to_sql')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.DataFrame.drop_duplicates')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_csv')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_cli_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.py.offline.plot')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_controller')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_system_node')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.create_engine')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.makedirs')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.Device.__new__')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_device_log_level')
    def test_monitor_re_processes(self, log_level_patch, device_patch, os_makedirs_patch, create_engine_patch,
                                  set_system_node_patch,
                                  set_current_controller_patch, pandas_read_sql_patch, plotly_patch, sleep_patch,
                                  execute_cli_command_patch, pandas_read_csv_patch,
                                  pandas_drop_duplicates_patch, pandas_to_sql_patch, reconnect_to_device_patch):
        mon.is_running = False
        set_current_controller_patch.return_value = 'Test'
        pandas_drop_duplicates_patch.return_value = 'Test'
        create_engine_patch.return_value = 'Test'
        plotly_patch.return_value = 'Test'
        set_system_node_patch.return_value = 'Test'
        sleep_patch.return_value = 'Test'
        log_level_patch.return_value = True
        device_patch.return_value = builtins.dev
        device_patch.get_version.return_value = dev.get_version

        dev.get_current_controller_name = MagicMock(return_value=None)
        device_patch.get_current_controller_name.return_value = dev.get_current_controller_name
        os_makedirs_patch.return_value = True

        pandas_read_csv_patch.side_effect = [pandas.DataFrame(),
                                             pandas.DataFrame({'DATETIME': ['Test'], 'ANNOTATION': ['Test']}),
                                             pandas.DataFrame({'DATETIME': ['Test'], 'ANNOTATION': ['Test']})]
        dev.nodes = MagicMock()
        dev.nodes.keys = MagicMock(return_value=['primary'])
        MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1, processes=[], log_level='OFF')

        dev.get_current_controller_name = MagicMock(return_value='Test')
        device_patch.get_current_controller_name.return_value = dev.get_current_controller_name
        dev.current_node = MagicMock()
        dev.current_node.controllers = MagicMock()
        dev.current_node.controllers.keys = MagicMock(return_value=['re0'])
        pandas_read_sql_patch.return_value = pandas.DataFrame({'PID': [1], 'DATETIME': [1], 'MEM': [1], 'CPU': [1]})
        self.assertIsNone(MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1,
                                                                 processes=[{'Test1': None, 'Test2': 'Test'}, 'Test3'], log_level='ERROR'))

        process3 = ['Test1', 'Test2']
        dev.current_node.controllers.keys = MagicMock(return_value=['re0'])
        pandas_read_sql_patch.return_value = pandas.DataFrame({'PID': [], 'DATETIME': [], 'MEM': [], 'CPU': []})
        self.assertIsNone(MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1, processes=process3 , log_level='ERROR'))

        t.get_resource_list.return_value = ['r0']
        self.assertIsNone(MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1, processes=process3 , log_level='ERROR'))

        mon.is_running = True
        process1 = ['Test1', 'Test2']
        process2 = [{'dcd': None},
                    {'snmpd': {'alert': None}},
                    {'rpd': {'alert': {'mem': 1, 'cpu': 1}}}]
        process4 = [{'rpd': {'alert': {'mem': None}}},
                    {'rpd': {'alert': {'cpu': None}}},
                    {'rpd': {'alert': {'mem': 2}}},
                    {'rpd': {'alert': {'cpu': 2}}}]
        process5 = [[],[]]

        dev.nodes = MagicMock()
        dev.nodes.keys.return_value = ['primary', 'primary']
        dev.current_node.controllers.keys.return_value = ['re0', 're0', 're0', 're0', 're0', 're0']
        dev.get_current_controller_name.side_effect = [None, 'Test', 'Test2', 'Test3']

        execute_cli_command_patch.side_effect = [Exception('Test'), Exception('Test'), "node: node:", Exception('Test'),
                                                 'COMMAND\n    \nlast\nprocesses:\nMem:\nSwap:\n 0K \nSwap\n% nice,\n---\nnode:\ntop\nTasks:\n%Cpu\ntotal,\n\n',
                                                 '', '', '', Exception('Test'), 'Test', Exception('Test'),
                                                 'Test', Exception('Test')]
        pandas_read_sql_patch.return_value = pandas.DataFrame({'PID': [2], 'DATETIME': [1], 'MEM': [1], 'CPU': [1]})
        pandas_to_sql_patch.side_effect = [Exception('Test'),
                                           'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test', 'Test',
                                           Exception('Test'), 'Test', 'Test']
        pandas_read_csv_patch.side_effect = [Exception('Test'), 'Test',
                                             pandas.DataFrame({'WCPU': ['1'], 'VIRT': ['1'], 'RES': ['1'], 'DATETIME': ['Test'],
                                                               'RESOURCE': ['Test'], 'NODE': ['Test'], 'CONTROLLER': ['Test'], 'HOST': ['Test']}),
                                             pandas.DataFrame({'%CPU': ['1'], 'SIZE': ['1'], 'DATETIME': ['Test'],
                                                               'RESOURCE': ['Test'], 'NODE': ['Test'],
                                                               'CONTROLLER': ['Test'], 'HOST': ['Test'], 'COMMAND': ['rpd']}),
                                             pandas.DataFrame({'%CPU': ['1'], 'SIZE': ['1'], 'VIRT': ['1'], 'RES': ['1'],
                                                               'C': ['Test'], 'THR': ['Test']}),
                                             pandas.DataFrame({'%CPU': ['1'], 'SIZE': ['1'], 'DATETIME': ['Test'],
                                                               'RESOURCE': ['Test'], 'NODE': ['Test'],
                                                               'CONTROLLER': ['Test'], 'HOST': ['Test'], 'COMMAND': ['rpd']})]
        pandas_drop_duplicates_patch = MagicMock(side_effect=[Exception('Test'), 'Test', 'Test'])

        MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1, processes=process1, log_level='ERROR')

        dev.nodes.keys.return_value = ['primary']
        MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1, processes=process2, log_level='ERROR')

        dev.nodes.keys.return_value = ['primary']
        dev.current_node.controllers.keys.return_value = ['re0']
        dev.get_current_controller_name.side_effect = ['Test', 'Test', 'Test', 'Test']
        from jnpr.toby.engines.monitor.MonitoringEngine import np
        np.issubdtype = MagicMock(return_value=True)
        pandas_to_sql_patch.side_effect = ['Test', Exception('Test'), 'Test', Exception('Test')]
        MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1, processes=process1, log_level='ERROR')

        MonitoringEngine._monitor_re_processes(mon, resource='r0', interval=1, processes=process4, log_level='ERROR')



    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_shell_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_system_node') 
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.reconnect_to_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.py.offline.plot')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.time.sleep')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_controller')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.DataFrame.to_sql')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.py.graph_objs.Scatter')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_csv')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_csv')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.makedirs')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.Device.__new__')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_device_log_level')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_cli_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine._strip_xml_namespace')
    def test__monitor_re_pfe(self, strip_xml_namespace_patch, execute_cli_command_on_device_patch, log_level_patch,
                             device_patch, makedirs_patch, read_csv_patch, read_sql_query_patch,
                             pandas_read_csv_patch, plotly_patch, to_sql_patch, set_controller_patch, sleep_patch,
                             plotly_offline_patch, reconnect_to_device_patch, set_current_system_node_patch,
                             execute_shell_command_on_device_patch):
        log_level_patch.return_value = True
        device_patch.return_value = builtins.dev
        device_patch.get_version.return_value = dev.get_version
        device_patch.is_evo.return_value = dev.is_evo
        mon.is_running = False
        read_sql_query_patch.return_value = pandas.DataFrame({'FRU': [1], 'DATETIME': [1], 'MEM': [MagicMock()], 'CPU': [MagicMock()]})
        pandas_read_csv_patch.return_value = pandas.DataFrame({'DATETIME': ['Test'], 'ANNOTATION': ['Test']})
        self.assertIsNone(MonitoringEngine._monitor_re_pfe(mon, resource='r0', interval=1, log_level='OFF'))

        mon.is_running = True
        rei = MagicMock()
        rei.tag = False

        execute_cli_command_on_device_patch.side_effect = [Exception('Test'), Exception('Test'), 'Test', 'Test', 'Test', Exception('Test'),
                                                           'Test']
        to_sql_patch.side_effect = [Exception('Test'), 'Test', 'Test', 'Test', Exception('Test'),
                                    Exception('Test3'), 'Test3', Exception('Call3')]
        strip_xml_namespace_patch.side_effect = [Exception('Test'), None, rei, rei]

        MonitoringEngine._monitor_re_pfe(mon, resource='r0', interval=1, log_level='ERROR')
        MonitoringEngine._monitor_re_pfe(mon, resource='r0', interval=1, log_level='ERROR')

        mrei = MagicMock()
        rengine = MagicMock()
        rengine.findtext.return_value = 45
        mrei.findtext.return_value = 'rename'
        mrei.findall.return_value = [rengine, rengine]
        rei.tag = 'multi-routing-engine-results'
        rei.findall.return_value = [mrei]
        mon.re_memory_alert_level = -1
        mon.re_cpu_alert_level = -1

        dev.nodes = MagicMock()
        dev.current_node = MagicMock()
        dev.nodes.keys = MagicMock(return_value=['primary', 'primary'])
        dev.current_node.controllers.keys.return_value = ['re0']
        dev.get_current_controller_name = MagicMock(side_effect=[None, 'Test'])
        dev.is_evo.return_value = True
        execute_shell_command_on_device_patch.side_effect = [Exception('Test')]

        MonitoringEngine._monitor_re_pfe(mon, resource='r0', interval=1, log_level='ERROR')



    def test_monitoring_engine_get_syslog_alerts(self):
        mon.is_running=False
        mon.syslog_alerts = {'resource' : 'r'}
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon, resource='r0'))
        mon.is_running=True
        mon.syslog_alerts = {'r0' : 'r'}
        self.assertEquals(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon),['r'])
        self.assertEquals(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon, resource='r0'),'r')
        self.assertEquals(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon, resource='r1'),[])



    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_cli_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_system_node')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.DataFrame.to_sql')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_controller')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.py.offline.plot')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_sql_query')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.stat')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.pd.read_csv')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.create_engine')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.os.makedirs')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_device_log_level')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.Device.__new__')
    def test__monitor_custom_data(self, device_patch, log_level_patch, os_makedirs_patch, create_engine_patch,
                                        pandas_read_csv_patch, os_stat_patch, pandas_read_sql_query_patch, plotly_patch,
                                        set_current_controller_patch, pandas_to_sql_patch, set_system_node_patch,
                                        execute_cli_command_on_device_patch):
        data = [{'graph1': None}, 
                {'graph2': [{'trace1': None}, 
                            {'trace2': {'parameters': [{'group' : None}] } },
                            {'trace3': {'parameters': [{'name' : 'Test'}] , 'command' : 'Test', 'format' : 'xml', 'node': 'Test', 'controller' : 'Test', 'mode' : 'shell'}},
                            {'trace4': {'parameters': [{'name' : 'Test'}] , 'command' : 'Test', 'format' : 'xml', 'node': 'Test', 'controller' : 'Test', 'mode' : 'shell'}}]},
                {'graph3': [{'trace1': {'parameters': [{'name' : 'Test'}]}}, 
                            {'trace2': {'parameters': [{'name' : 'Test'}], 'command' : 'Test', 'format' : 'json', 'node' : 'Test', 'mode' : 'shell'}},
                            {'trace3': {'parameters': [{'name' : 'Test'}], 'command' : 'Test', 'format' : 'xml'}}, 
                            {'trace4': {'parameters': [{'name' : 'Test'}], 'command' : 'Test', 'format' : 'Test'}},
                            {'trace5': {'parameters': [{'name' : 'Test'}], 'command' : 'Test'}}]}]

        mon.is_running=False
        log_level_patch.return_value = True
        device_patch.return_value = builtins.dev
        device_patch.get_version.return_value = dev.get_version
        os_makedirs_patch.return_value = 'Test'
        create_engine_patch.return_value = 'Test'
        pandas_read_csv_patch.return_value = pandas.DataFrame({'DATETIME': ['Test'], 'ANNOTATION': ['Test']})
        pandas_read_sql_query_patch.side_effect = [pandas.DataFrame(), pandas.DataFrame({'DATETIME': [], 'DATA': []}),
                                                   pandas.DataFrame(),
                                                   pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame(),
                                                   pandas.DataFrame({'DATETIME': ['Test'], 'DATA': ['Test']})]

        set_system_node_patch.return_value = 'Test'
        set_current_controller_patch.return_value = 'Test'

        t.get_resource_list.return_value = ['r0']
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='OFF')) 

        t.get_resource_list.return_value = ['r1']
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR')) 

        os_stat_patch.return_value = MagicMock(st_size=0)
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR'))

        os_stat_patch.side_effect = Exception('Test')
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR'))


        mon.is_running = True
        execute_cli_command_on_device_patch.side_effect = [Exception('Test'), 'Test']
        os_stat_patch.return_value = MagicMock(st_size=0)
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR'))


        

    def test_monitoring_engine_get_syslog_alerts(self):
        mon.is_running=False
        mon.syslog_alerts = {'resource' : 'r'}
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon))
        self.assertIsNone(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon, resource='r0'))
        mon.is_running=True
        mon.syslog_alerts = {'r0' : 'r'}
        self.assertEquals(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon),['r'])
        self.assertEquals(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon, resource='r0'),'r')
        self.assertEquals(MonitoringEngine.monitoring_engine_get_syslog_alerts(mon, resource='r1'),[])



    @patch('jnpr.toby.engines.monitor.MonitoringEngine.execute_cli_command_on_device')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_system_node')
    @patch('pandas.DataFrame.to_sql')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_current_controller')
    @patch('plotly.offline.plot')
    @patch('pandas.read_sql_query')
    @patch('os.stat')
    @patch('pandas.read_csv')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.create_engine')
    @patch('os.makedirs')
    @patch('jnpr.toby.engines.monitor.MonitoringEngine.set_device_log_level')
    @patch('jnpr.toby.hldcl.device.Device.__new__')
    def test__monitor_custom_data(self, device_patch, log_level_patch, os_makedirs_patch, create_engine_patch,
                                        pandas_read_csv_patch, os_stat_patch, pandas_read_sql_query_patch, plotly_patch,
                                        set_current_controller_patch, pandas_to_sql_patch, set_system_node_patch,
                                        execute_cli_command_on_device_patch):
        data = [{'graph1': None}, 
                {'graph2': [{'trace1': None}, 
                            {'trace2': {'parameters': [{'group' : None}] } },
                            {'trace3': {'parameters': [{'name' : 'Test'}] , 'command' : 'Test', 'format' : 'xml', 'node': 'Test', 'controller' : 'Test', 'mode' : 'shell'}},
                            {'trace4': {'parameters': [{'name' : 'Test'}] , 'command' : 'Test', 'format' : 'xml', 'node': 'Test', 'controller' : 'Test', 'mode' : 'shell'}}]},
                {'graph3': [{'trace1': {'parameters': [{'name' : 'Test'}]}}, 
                            {'trace2': {'parameters': [{'name' : 'Test'}], 'command' : 'Test', 'format' : 'json', 'node' : 'Test', 'mode' : 'shell'}},
                            {'trace3': {'parameters': [{'name' : 'Test'}], 'command' : 'Test', 'format' : 'xml'}}, 
                            {'trace4': {'parameters': [{'name' : 'Test'}], 'command' : 'Test', 'format' : 'Test'}},
                            {'trace5': {'parameters': [{'name' : 'Test'}], 'command' : 'Test'}}]}]

        mon.is_running=False
        log_level_patch.return_value = True
        device_patch.return_value = builtins.dev
        device_patch.get_version.return_value = dev.get_version
        os_makedirs_patch.return_value = 'Test'
        create_engine_patch.return_value = 'Test'
        pandas_read_csv_patch.return_value = pandas.DataFrame({'DATETIME': ['Test'], 'ANNOTATION': ['Test']})
        pandas_read_sql_query_patch.side_effect = [pandas.DataFrame(), pandas.DataFrame({'DATETIME': [], 'DATA': []}),
                                                   pandas.DataFrame(),
                                                   pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame(),
                                                   pandas.DataFrame({'DATETIME': ['Test'], 'DATA': ['Test']})]

        set_system_node_patch.return_value = 'Test'
        set_current_controller_patch.return_value = 'Test'

        t.get_resource_list.return_value = ['r0']
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='OFF')) 

        t.get_resource_list.return_value = ['r1']
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR')) 

        os_stat_patch.return_value = MagicMock(st_size=0)
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR'))

        os_stat_patch.side_effect = Exception('Test')
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR'))


        mon.is_running = True
        execute_cli_command_on_device_patch.side_effect = [Exception('Test'), 'Test']
        os_stat_patch.return_value = MagicMock(st_size=0)
        self.assertIsNone(MonitoringEngine._monitor_custom_data(mon, resource='r0', interval=1, custom_data=data, log_level='ERROR'))


        


def create_t_data():
    """
    Create t data
    :return:
        Returns t data
    """
    t.t_dict = dict()
    t.t_dict['resources'] = dict()
    t.t_dict['resources']['r0'] = dict()
    t.t_dict['resources']['r0']['interfaces'] = dict()
    t.t_dict['resources']['r0']['interfaces']['fe0'] = dict()
    t.t_dict['resources']['r0']['interfaces']['fe0']['name'] = 'fe0.0'
    t.t_dict['resources']['r0']['interfaces']['fe0']['link'] = 'link'
    t.t_dict['resources']['r0']['system'] = dict()
    t.t_dict['resources']['r0']['system']['dh'] = "test"
    t.t_dict['resources']['r0']['system']['primary'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0'] = dict()
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['hostname'] = 'dummy_host'
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['mgt-ip'] = '1.1.1.1'
    t.t_dict['resources']['r0']['system']['primary']['controllers']['re0']['osname'] = 'JunOS'
    t.t_dict['resources']['r0']['system']['primary']['name'] = 'dummy_host'
    t.t_dict['resources']['r0']['system']['primary']['model'] = 'mx'
    t.t_dict['resources']['r0']['system']['primary']['make'] = 'Juniper'
    t.t_dict['resources']['r0']['system']['primary']['osname'] = 'JunOS'


if __name__ == '__main__':
    unittest.main()
