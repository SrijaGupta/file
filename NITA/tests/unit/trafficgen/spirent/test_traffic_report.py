import unittest
from mock import patch, MagicMock, Mock
from jnpr.toby.trafficgen.spirent.traffic_report import *
import builtins

builtins.t = MagicMock()
builtins.t.log = MagicMock()
rt_handle = MagicMock()


class TrafficReport(unittest.TestCase):
    def test_ntlog(self):
        builtins.t.log.return_value = None
        self.assertEqual(ntlog("Sample Message"), None)
        self.assertEqual(ntlog("Sample Message", Tool.DEBUG), None)

    def test_stc_action(self):
        rt_handle.invoke.return_value = {'port': {'status': 1}}
        stc = SpirentTestCenter(rt_handle=rt_handle)
        self.assertEqual(stc.start_traffic(), {'port': {'status': 1}})
        self.assertEqual(stc.stop_traffic(), {'port': {'status': 1}})
        self.assertEqual(stc.arpnd(streamids=None), {'port': {'status': 1}})
        self.assertEqual(stc.clear_stats(), {'port': {'status': 1}})
        self.assertEqual(stc.save_result_db()['port'], {'status': 1})

    def test_stc_sqlite(self):
        sqlite3.connect = MagicMock()
        sqlite3.connect.close.return_value = None
        sqlite3.connect.cursor = MagicMock()
        sqlite3.connect.execute.return_value = None
        sqlite3.connect.cursor.description.return_value = {'col': 1}
        sqlite3.connect.fetchall = Mock()
        sqlite3.connect.fetchall.return_value = [['h1', 'h2'], [1, 2]]
        self.assertEqual(Tool.sqlite_exec("results.db", ""), None)
        # self.assertEqual(Tool.sqlite_query("results.db", "", fmt='dict'), [])
        #                 [['h1', 'h2'], [1, 2]])

    def test_get_tabulate(self):
        table = [['sb1', 'tx', 100, 0, 200], ['sb1', 'rx', 200, 0, 100]]
        hdr = ['sbname', 'item', 'port1', 'port2', 'port3']
        asciitbl = """|---------+-------+--------+--------+--------|
| sbname  | item  |  port1 |  port2 |  port3 |
|---------+-------+--------+--------+--------|
| sb1     | tx    |    100 |      0 |    200 |
| sb1     | rx    |    200 |      0 |    100 |
|---------+-------+--------+--------+--------|
"""
        self.assertEqual(Tool.get_tabulate(table, headers=hdr,
                                           tablefmt='orgtbl'), asciitbl)

    def test_traffic_report_alias(self):
        expected_summ_alias = {
            "BD0003-V0003-MH7-INTRA-SH1-IPV4": ["SH1"],
            "BD0003-V0003-SH3-INTRA-MH7-IPV6": ["MH7"],
            "BD0003-V0003-SH1-BC": ["SH2", "SH3", "MH7", "MH8"],
            "BD0003-V0003-SH1-UC-MH8": ["MH8"],
            "BD0003-V0003-SH1-UC-SH2": ["SH2"],
        }
        intf_alias = [
            {"name": "r0-t0-1", "alias": "SH1"},
            {"name": "r1-t0-1", "alias": "SH2"},
            {"name": "r2-t0-1", "alias": "SH3"},
            {"name": "r2-t0-2", "alias": "SH4"},
            {"name": "r3-t0-1", "alias": "SH5"},
            {"name": "r5-t0-1", "alias": "MH7"},
            {"name": "r5-t0-2", "alias": "MH8"},
        ]
        sql_tr_rslt = [
            {'TxFrameCount': 30100, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'TxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 30100, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-2 //3/2'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-9 //3/9'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-1 //3/1'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-2-11 //2/11'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-11 //3/11'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-2-4 //2/4'},
            {'TxFrameCount': 30200, 'StreamBlockName': 'BD0003-V0003-MH7-INTRA-SH1-IPV4',
             'TxPortName': '10.48.5.124-3-11 //3/11'},
            {'RxFrameCount': 30160, 'StreamBlockName': 'BD0003-V0003-MH7-INTRA-SH1-IPV4',
             'RxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 40, 'StreamBlockName': 'BD0003-V0003-MH7-INTRA-SH1-IPV4',
             'RxPortName': '10.48.5.124-3-2 //3/2'},
            {'TxFrameCount': 30098, 'StreamBlockName': 'BD0003-V0003-SH3-INTRA-MH7-IPV6',
             'TxPortName': '10.48.5.124-3-9 //3/9'},
            {'RxFrameCount': 30098, 'StreamBlockName': 'BD0003-V0003-SH3-INTRA-MH7-IPV6',
             'RxPortName': '10.48.5.124-3-11 //3/11'},
            {'TxFrameCount': 30123, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'TxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 30098, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-3-2 //3/2'},
            {'RxFrameCount': 30156, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-3-9 //3/9'},
            {'RxFrameCount': 30123, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-3-11 //3/11'},
            {'RxFrameCount': 30123, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-2-4 //2/4'},
            {'TxFrameCount': 30153, 'StreamBlockName': 'BD0003-V0003-SH1-UC-MH8',
             'TxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 30153, 'StreamBlockName': 'BD0003-V0003-SH1-UC-MH8',
             'RxPortName': '10.48.5.124-2-4 //2/4'},
        ]
        rt_handle.intf_to_port_map = {
            "r0-t0-1": "2/6",
            "r1-t0-1": "3/2",
            "r2-t0-1": "3/9",
            "r2-t0-2": "3/1",
            "r3-t0-1": "2/11",
            "r5-t0-1": "3/11",
            "r5-t0-2": "2/4",
        }
        port_alias_return = [
            {'name': '2/6', 'alias': 'SH1'},
            {'name': '3/2', 'alias': 'SH2'},
            {'name': '3/9', 'alias': 'SH3'},
            {'name': '3/1', 'alias': 'SH4'},
            {'name': '2/11', 'alias': 'SH5'},
            {'name': '3/11', 'alias': 'MH7'},
            {'name': '2/4', 'alias': 'MH8'}
        ]
        stc = SpirentTestCenter(rt_handle=rt_handle)
        port_alias = stc.get_port_alias(intf_alias=intf_alias)
        self.assertEqual(port_alias, port_alias_return)
        tr_result = stc._stc_export_result(sql_tr_rslt, 'dict', port_alias)
        tr_result_return = {
            'header': ['StreamBlock', 'T/R', 'SH1', 'SH2', 'SH3', 'SH4', 'SH5', 'MH7', 'MH8'],
            'BD0003-V0003-MH7-INTRA-SH1-IPV4': {
                'tx': [0, 0, 0, 0, 0, 30200, 0],
                'rx': [30160, 40, 0, 0, 0, 0, 0]},
            'BD0003-V0003-SH1-BC': {
                'tx': [30123, 0, 0, 0, 0, 0, 0],
                'rx': [0, 30098, 30156, 0, 0, 30123, 30123]},
            'BD0003-V0003-SH1-UC-MH8': {
                'tx': [30153, 0, 0, 0, 0, 0, 0],
                'rx': [0, 0, 0, 0, 0, 0, 30153]},
            'BD0003-V0003-SH1-UC-SH2': {
                'tx': [30100, 0, 0, 0, 0, 0, 0],
                'rx': [0, 30100, 0, 0, 0, 0, 0]},
            'BD0003-V0003-SH3-INTRA-MH7-IPV6': {
                'tx': [0, 0, 30098, 0, 0, 0, 0],
                'rx': [0, 0, 0, 0, 0, 30098, 0]}
        }
        self.assertEqual(tr_result, tr_result_return)
        result = stc.export_traffic_stats(
            result=tr_result, port_alias=port_alias, pps=1000,
            expected_summ=expected_summ_alias, loss_msec=50, log_console=False)
        report_return = """Traffic Verification PASSED within tolerance of 50 msec or 0.0000%
        maximum loss is 40 msec and 0.1325%
        FAILED with unexpected traffic in 2 out of 5 streams
    BD0003-V0003-MH7-INTRA-SH1-IPV4 failed with unexpected packets rx at 0.1325% or loss of 40 msec
    BD0003-V0003-SH1-BC failed with unexpected packets rx at 0.1096% or loss of 33 msec
The following streams passed:
    BD0003-V0003-SH1-UC-MH8
    BD0003-V0003-SH1-UC-SH2
    BD0003-V0003-SH3-INTRA-MH7-IPV6

Detailed traffic statistics for failed streams
|----------------------------------+-------+--------+--------+--------+------+------+--------+--------|
| StreamBlock                      | T/R   |    SH1 |    SH2 |    SH3 |  SH4 |  SH5 |    MH7 |    MH8 |
|----------------------------------+-------+--------+--------+--------+------+------+--------+--------|
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | TX    |      0 |      0 |      0 |    0 |    0 |  30200 |      0 |
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | RX    |  30160 |     40 |      0 |    0 |    0 |      0 |      0 |
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | EXP   |  30200 |      0 |      0 |    0 |    0 |      0 |      0 |
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | COMP  |      0 |      0 |      1 |    1 |    1 |      1 |      1 |
| BD0003-V0003-SH1-BC              | TX    |  30123 |      0 |      0 |    0 |    0 |      0 |      0 |
| BD0003-V0003-SH1-BC              | RX    |      0 |  30098 |  30156 |    0 |    0 |  30123 |  30123 |
| BD0003-V0003-SH1-BC              | EXP   |      0 |  30123 |  30123 |    0 |    0 |  30123 |  30123 |
| BD0003-V0003-SH1-BC              | COMP  |      1 |      0 |      0 |    1 |    1 |      1 |      1 |
|----------------------------------+-------+--------+--------+--------+------+------+--------+--------|
"""
        self.assertEqual(result, report_return)

    def test_traffic_report_no_alias(self):
        sql_tr_rslt = [
            {'TxFrameCount': 30100, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'TxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 30100, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-2 //3/2'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-9 //3/9'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-1 //3/1'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-2-11 //2/11'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-3-11 //3/11'},
            {'RxFrameCount': 0, 'StreamBlockName': 'BD0003-V0003-SH1-UC-SH2',
             'RxPortName': '10.48.5.124-2-4 //2/4'},
            {'TxFrameCount': 30200, 'StreamBlockName': 'BD0003-V0003-MH7-INTRA-SH1-IPV4',
             'TxPortName': '10.48.5.124-3-11 //3/11'},
            {'RxFrameCount': 30160, 'StreamBlockName': 'BD0003-V0003-MH7-INTRA-SH1-IPV4',
             'RxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 40, 'StreamBlockName': 'BD0003-V0003-MH7-INTRA-SH1-IPV4',
             'RxPortName': '10.48.5.124-3-2 //3/2'},
            {'TxFrameCount': 30098, 'StreamBlockName': 'BD0003-V0003-SH3-INTRA-MH7-IPV6',
             'TxPortName': '10.48.5.124-3-9 //3/9'},
            {'RxFrameCount': 30098, 'StreamBlockName': 'BD0003-V0003-SH3-INTRA-MH7-IPV6',
             'RxPortName': '10.48.5.124-3-11 //3/11'},
            {'TxFrameCount': 30123, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'TxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 30098, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-3-2 //3/2'},
            {'RxFrameCount': 30156, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-3-9 //3/9'},
            {'RxFrameCount': 30123, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-3-11 //3/11'},
            {'RxFrameCount': 30123, 'StreamBlockName': 'BD0003-V0003-SH1-BC',
             'RxPortName': '10.48.5.124-2-4 //2/4'},
            {'TxFrameCount': 30153, 'StreamBlockName': 'BD0003-V0003-SH1-UC-MH8',
             'TxPortName': '10.48.5.124-2-6 //2/6'},
            {'RxFrameCount': 30153, 'StreamBlockName': 'BD0003-V0003-SH1-UC-MH8',
             'RxPortName': '10.48.5.124-2-4 //2/4'},
        ]
        rt_handle.intf_to_port_map = {
            "r0-t0-1": "2/6",
            "r1-t0-1": "3/2",
            "r2-t0-1": "3/9",
            "r2-t0-2": "3/1",
            "r3-t0-1": "2/11",
            "r5-t0-1": "3/11",
            "r5-t0-2": "2/4",
        }
        expected_summ = {
            "BD0003-V0003-MH7-INTRA-SH1-IPV4": ["r0-t0-1"],
            "BD0003-V0003-SH3-INTRA-MH7-IPV6": ["r5-t0-1"],
            "BD0003-V0003-SH1-BC": ["r1-t0-1", "r2-t0-1", "r5-t0-1", "r5-t0-2"],
            "BD0003-V0003-SH1-UC-MH8": ["r5-t0-2"],
            "BD0003-V0003-SH1-UC-SH2": ["r1-t0-1"],
        }
        result_return = """Traffic Verification PASSED within tolerance of 50 msec or 0.0000%
        maximum loss is 40 msec and 0.1325%
        FAILED with unexpected traffic in 2 out of 5 streams
    BD0003-V0003-MH7-INTRA-SH1-IPV4 failed with unexpected packets rx at 0.1325% or loss of 40 msec
    BD0003-V0003-SH1-BC failed with unexpected packets rx at 0.1096% or loss of 33 msec
The following streams passed:
    BD0003-V0003-SH1-UC-MH8
    BD0003-V0003-SH1-UC-SH2
    BD0003-V0003-SH3-INTRA-MH7-IPV6

Detailed traffic statistics for failed streams
|----------------------------------+-------+----------+----------+----------+----------+----------+----------+----------|
| StreamBlock                      | T/R   |  r0-t0-1 |  r1-t0-1 |  r2-t0-1 |  r2-t0-2 |  r3-t0-1 |  r5-t0-1 |  r5-t0-2 |
|----------------------------------+-------+----------+----------+----------+----------+----------+----------+----------|
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | TX    |        0 |        0 |        0 |        0 |        0 |    30200 |        0 |
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | RX    |    30160 |       40 |        0 |        0 |        0 |        0 |        0 |
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | EXP   |    30200 |        0 |        0 |        0 |        0 |        0 |        0 |
| BD0003-V0003-MH7-INTRA-SH1-IPV4  | COMP  |        0 |        0 |        1 |        1 |        1 |        1 |        1 |
| BD0003-V0003-SH1-BC              | TX    |    30123 |        0 |        0 |        0 |        0 |        0 |        0 |
| BD0003-V0003-SH1-BC              | RX    |        0 |    30098 |    30156 |        0 |        0 |    30123 |    30123 |
| BD0003-V0003-SH1-BC              | EXP   |        0 |    30123 |    30123 |        0 |        0 |    30123 |    30123 |
| BD0003-V0003-SH1-BC              | COMP  |        1 |        0 |        0 |        1 |        1 |        1 |        1 |
|----------------------------------+-------+----------+----------+----------+----------+----------+----------+----------|
"""
        stc = SpirentTestCenter(rt_handle=rt_handle)
        port_alias = stc.get_port_alias()
        tr_result = stc._stc_export_result(sql_tr_rslt, 'dict', port_alias)
        result = stc.export_traffic_stats(
            result=tr_result, pps=1000, expected_summ=expected_summ,
            port_alias=port_alias, loss_msec=50, log_console=False)
        self.assertEqual(result, result_return)

    @patch('jnpr.toby.trafficgen.spirent.traffic_report.SpirentTestCenter.save_result_db', return_value={'db_file': None})
    @patch('jnpr.toby.trafficgen.spirent.traffic_report.SpirentTestCenter.get_port_alias', return_value=None)
    @patch('jnpr.toby.trafficgen.spirent.traffic_report.SpirentTestCenter.get_result_from_db', return_value=None)
    @patch('jnpr.toby.trafficgen.spirent.traffic_report.SpirentTestCenter.export_traffic_stats',
           return_value="Traffic Verification PASSED ")
    def test_traffic_report(self, patch_save_result_db, patch_get_port_alias,
                            patch_get_result_from_db, patch_export_traffic_stats):
        rpt = "Traffic Verification PASSED "
        rslt = traffic_report(rt_handle)
        self.assertEqual(rslt, {"status": True, "stats": None,
                                "report": rpt, "db_file": None})


if __name__ == '__main__':
    unittest.main()
