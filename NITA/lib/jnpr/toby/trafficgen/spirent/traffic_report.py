"""
Obtain per port per streamblock traffic results based on sqlite query of
results.db and return results in tabular format. Optionally return PASS/FAIL
based on user result expectation, and/or loss tolerance

User should be able to call from Robot like
  Execute Tester Command  ${rt_handle}  command=get_traffic_report

This is refactored from PyNT
"""
import time
import sys
import traceback
import sqlite3
import importlib
import logging
from jnpr.toby.logger.logger import get_log_dir

__author__ = "Sean Wu"
__copyright__ = "Copyright 2019, Juniper Toby Project"
__credits__ = ["PyNT"]
__version__ = "0.0.1"
__maintainer__ = "xwu"
__email__ = "xwu@juniper.net"
__status__ = "Beta"


def ntlog(message, level=logging.INFO):
    """ Common Log Facility """
    if t in globals():
        t.log(level=level, message=message)
    else:
        logging.log(level, message)


def traffic_report(rth=None, intf_alias=None, db_file=None,
                   expected_summ=None, **kwargs):
    """
    Get traffic report
    :param rth: Router Tester Handle
    :param intf_alias: [{"name": "r0-rt-1", "alias": "CE1"}, ...]
    :param db_file: path to results data base file. If none, a fresh copy
                will be downloaded from Spirent
    :param expected_summ: if None, all considered pass, print result only
            the expected recipient interface needs to be consistent
            with intf_alias passed. If no intf_alias specified, use
            interface tag like r1-t0-1
            {"sb_name_01": ["r1-t0-1", "r2-to-2"],
             "sb_name_02": ["r2-t0-1"]}
    :param skip_inactive: default True. Stream Blocks with TX=0 not counted
    :param failonly: report only show detailed data in table for stream failed
    :param log_console: default True. Print a copy to log
    :param pps: packet per second with default 1000
    :param loss_msec: loss in msec calc as max_loss_packets * 1000 / pps
    :param loss_pct: loss in percent, default 0% max_loss_packet * 100 / tx_pkt
    :return:   {'status': True/False,
                'report': String of report in text,
                'stats': list of lists that can be fed to generate report,
                'db_file': from which the report is extracted
                }
    """
    result = {'status': False, "stats": [], "report": "", "db_file": db_file}
    try:
        stc = SpirentTestCenter(rt_handle=rth)
        port_alias = stc.get_port_alias(intf_alias)
        if db_file is None:
            db_result = stc.save_result_db()
            # if not db_result['status']:
            #    return result
            result['db_file'] = db_result['db_file']
        result["stats"] = stc.get_result_from_db(
            dbfile=result["db_file"],
            port_alias=port_alias)
        report = stc.export_traffic_stats(
            result=result["stats"], expected_summ=expected_summ, **kwargs)
        result["report"] = report
        pass_str = ("Traffic Verification SUCCEEDED",
                    "Traffic Verification PASSED")
        if report.startswith(pass_str):
            result['status'] = True
    except:
        ntlog('Traffic Report Failed!')
        ntlog("%s\n%s" % (sys.exc_info()[0], traceback.format_exc()),
              logging.ERROR)
    return result


class Tool(object):
    """ Common Toolkit"""
    TABULATE_WARN = False
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG
    WARN = logging.WARNING
    INFO = logging.INFO
    FATAL = logging.FATAL

    def __init__(self, log_level=INFO):
        self.log_level = log_level

    @staticmethod
    def get_epoch():
        """ Return Epoch time as Integer"""
        return int(time.time())

    @staticmethod
    def _sqlite_dict_factory(cursor, row):
        data = {}
        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]
        return data

    @staticmethod
    def sqlite_exec(dbfile, stmt):
        """
        Execute a SQL Statement for SQLite DB
        :param dbfile:
        :param stmt:
        :return:
        """
        dbconn = sqlite3.connect(dbfile)
        dbc = dbconn.cursor()
        dbc.execute(stmt)
        dbconn.close()

    @classmethod
    def sqlite_query(cls, dbfile, stmt, fmt='dict'):
        """
        SQLite Query and return result in a dict
        :param dbfile:
        :param stmt:
        :param fmt:
        :return:
        """
        dbconn = sqlite3.connect(dbfile)
        if fmt == "dict":
            dbconn.row_factory = cls._sqlite_dict_factory
        elif fmt == "row":
            dbconn.row_factory = sqlite3.Row
        dbc = dbconn.cursor()
        dbc.execute(stmt)
        ret = dbc.fetchall()
        dbconn.close()
        return ret

    @classmethod
    def get_tabulate(cls, table, headers=None, tablefmt='orgtbl'):
        """
        wrapper of tabulate in case it is not installed
        :param table:
        :param headers:
        :param tablefmt: only orgtbl supported for now
        :return:
        """
        try:
            tabu = importlib.import_module("tabulate")
            return tabu.tabulate(table, headers=headers, tablefmt=tablefmt)
        except ImportError:
            if cls.TABULATE_WARN:
                ntlog("tabulate module not found, trying best to print")
        try:
            return cls._get_tabulate_lite(table, headers)
        except:
            ntlog(headers)
            ntlog("----  table body ---")
            ntlog(table)
            return ''

    @staticmethod
    def _get_tabulate_lite(table, headers=None):
        cols = len(table[0])
        colsize = [1] * cols
        if not isinstance(headers[0], list):
            hdrs = [headers]
        else:
            hdrs = headers
        align = ["-"] * cols
        for rid, row in enumerate(hdrs + table):
            for col in range(cols):
                if row[col] is None:
                    continue
                elif rid > 0 and str(row[col]).isnumeric():
                    align[col] = ""
                if len(str(row[col])) >= colsize[col]:
                    colsize[col] = len(str(row[col])) + 1
        fmt = "| %%%s%ds |" % (align[0], colsize[0])
        divider = "|" + "-" * (colsize[0] + 2)
        for cid in range(1, cols):
            fmt += " %%%s%ds |" % (align[cid], colsize[cid])
            divider += "+" + "-" * (colsize[cid]+2)
        fmt += "\n"
        divider += "|\n"
        tbl = divider
        for hdr in hdrs:
            tbl += fmt % tuple(map(str, hdr))
        tbl += divider
        for row in table:
            tbl += fmt % tuple(map(str, row))
        tbl += divider
        return tbl


class SpirentTestCenter(object):
    """  Wrapper of SpirentTestCenter Object for logging   """
    def __init__(self, rt_handle=None):
        self.hdl = rt_handle
        self.streamids = []
        self.logdir = get_log_dir()

    def execute(self, command, **kwargs):
        """ common shortcut to invoke """
        return self.hdl.invoke(function=command, **kwargs)

    def arpnd(self, streamids):
        """ ARPND operation on a list of streamids """
        stcargs = {"command": "arp_control",
                   "arp_target": "stream",
                   "handle": streamids}
        return self.execute(**stcargs)

    def start_traffic(self, streamids=None):
        """ Start Traffic Stream Blocks IDS"""
        if streamids is None:
            streamids = self.streamids
        cmd_args = "-streamblocklist \"%s\"" % " ".join(streamids)
        stcargs = {"command": "invoke",
                   "cmd": "stc::perform streamblockstart " + cmd_args}
        return self.execute(**stcargs)

    def stop_traffic(self, streamids=None, db_file=1):
        """ Stop traffic Stream Blocks and download results.db by default"""
        if streamids is None:
            # Future support on selective traffic op
            pass
        stcargs = {"command": "traffic_control", "action": "stop",
                   "db_file": db_file, "port_handle": "all"}
        return self.execute(**stcargs)

    def save_result_db(self, dbfile=None):
        """
        Short cut for saving results.db
        :param dbfile:
        :return:
        """
        if dbfile is None:
            dbfile = "result_%d.db" % Tool.get_epoch()
            dbfile = "/".join([self.logdir, dbfile])
        cmd = 'stc::perform SaveResults -CollectResult TRUE'
        cmd += " -ResultFileName %s" % dbfile
        cmd += ' -SaveDetailedResults TRUE -LoopMode OVERWRITE'
        cmd += ' -ExecuteSynchronous TRUE'
        # ' -OverwriteIfExist TRUE'
        result = self.execute(command="invoke", cmd=cmd)
        if isinstance(result, dict):
            result['db_file'] = dbfile
        elif isinstance(result, bool):
            result = {'status': result, 'db_file': dbfile}
        else:
            result = {'status': False, 'db_file': dbfile}
        return result

    def clear_stats(self):
        """ Clear result stats """
        return self.execute(command="invoke",
                            cmd="stc::perform resultsclearall")

    def get_port_alias(self, intf_alias=None):
        """
        Provider user alias for each Tester port
        :param intf_alias: [{"name": "r0-t0-1": "alias": "CE1"}...]
        :return: [{"name": "4/1", "alias": "CE1"}...]
               if exception raised, default return is
                 [{"name": "4/1", "alias": "r0-t0-1"}...]
        """
        port_alias_def = []
        port_alias = []
        if self.hdl is not None:
            for intf, port in sorted(self.hdl.intf_to_port_map.items()):
                port_alias_def.append({"name": port, "alias": intf})
        else:
            port_alias = None
        try:
            for ifa in intf_alias:
                port = self.hdl.intf_to_port_map[ifa["name"]]
                port_alias.append({"name": port, "alias": ifa["alias"]})
        except:
            port_alias = port_alias_def
        return port_alias

    @staticmethod
    def _db_create_table_txrxeot(dbfile):
        sql = """CREATE TABLE IF NOT EXISTS TxRxEotStreamResults AS
              SELECT Tx.DataSetId AS DataSetId,
              Tx.ParentHnd AS TxParentHnd,
              Tx.PortName AS TxPortName,
              Tx.StreamBlockName AS TxStreamBlockName,
              Tx.StreamIndex AS TxStreamIndex,
              Tx.StreamId AS TxStreamId,
              Tx.ParentStreamBlock AS TxParentStreamBlock,
              Tx.OffsetInStreamBlock AS TxOffsetInStreamBlock,
              Tx.FrameCount AS TxFrameCount,
              Tx.OctetCount AS TxOctetCount,
              Tx.RxPort AS ExpectedRxPortHandle,
              Tx.RxPortName AS ExpectedRxPortName,
              Tx.NumOfMulticastExpectedRxPort AS NumOfMulticastExpectedRxPort,
              Tx.L1BitCount AS TxL1BitCount,
              Rx.L1BitCount AS RxL1BitCount,
              (Tx.NumOfMulticastExpectedRxPort * Tx.FrameCount) 
                  AS ExpectedRxFrameCount,
              (Rx.FrameCount - 1) AS ModFrameCount,
              (Rx.InSeqFrameCount - 1) AS ModInSeqFrameCount,
              (Rx.SigFrameCount - 1) AS ModSigFrameCount,
              Rx.PortName AS ActualRxPortName,
              Rx.*
              FROM TxEotStreamResults AS Tx LEFT JOIN RxEotStreamResults AS Rx 
              ON Tx.DataSetId = Rx.DataSetId AND Tx.StreamId = Rx.Comp32
              """
        Tool.sqlite_exec(dbfile, sql)

    @staticmethod
    def _db_get_result_sql_stmt(name):
        """
        remove dependency on custom table TxRxEotStreamResults
        :return:
        """
        sql = {
            'txSBPort': """SELECT StreamBlockName,
                TxPortName,
                sum(TxFrameCount) AS TxFrameCount
                FROM (
                    SELECT PortName AS TxPortName,
                        StreamBlockName,
                        FrameCount AS TxFrameCount
                    FROM TxEotStreamResults
                    GROUP BY StreamId
                )
                GROUP BY StreamBlockName,
                    TxPortName
            """,
            'rxSBPort': """
                SELECT (
                        SELECT Name
                        FROM StreamBlock
                        WHERE Handle = ParentStreamBlock
                    ) AS StreamBlockName,
                    PortName AS RxPortName,
                    sum(SigFrameCount) AS RxFrameCount
                FROM RxEotStreamResults
                WHERE StreamBlockName IS NOT NULL
                GROUP BY ParentStreamBlock,
                    RxPortName
            """,
        }
        return sql[name]

    @staticmethod
    def _get_expected_from_summ(summ, rtifs):
        """
        summ uses stream name as key, and value is list of rx rt if tags
        rtifs is an array of rtifs with clean names as table header
        pad is tester port_alilas_default, which is array of {alias/clean_name}
        :param summ:
        :param rtifs:
        :return:
        """
        expected = {}
        # ifname_to_tag = {}
        # for itag in pad:
        #     ifname_to_tag[itag['name']] = itag['alias']
        for stname, rxports in summ.items():
            row = []
            for col in rtifs:
                if col in rxports:
                    row.append(1)
                else:
                    row.append(0)
            expected[stname] = row
        return expected

    def export_traffic_stats(self, result, expected=None, failonly=True,
                             skip_inactive=True, log_console=True,
                             **kwargs):
        """
        Export traffic stats in a tabular format
        :param result:
        :param expected:
        :param failonly:
        :param skip_inactive:
        :param log_console: Default True to print a copy
        :return:
        """
        tbl = []
        header = result.pop("header")
        pct = 0  # exact
        precision = 10000
        cnt = len(header) - 2
        passstr = []
        failstr = {}
        tblfail = []
        cnt_streams = 0
        pps = kwargs.pop("pps", 1000)
        loss_msec = kwargs.pop("loss_msec", 0)
        loss_pct = float(kwargs.pop("loss_pct", 0))
        expected_summ = kwargs.pop("expected_summ", None)
        if expected is None and expected_summ is not None:
            var1 = expected_summ
            var2 = header[2:]
            expected = self._get_expected_from_summ(summ=var1, rtifs=var2)
        max_msec = 0
        max_pct = 0
        stab = " " * 4
        dtab = stab * 2
        for k, val in sorted(result.items()):
            rowa = [k, 'TX'] + val['tx']
            tx_cnt = sum(val['tx'])  # always assume one port tx
            if tx_cnt == 0 and skip_inactive:
                continue
            cnt_streams += 1
            tbl.append(rowa)
            rowb = [k, 'RX'] + val['rx']
            tbl.append(rowb)
            if expected is not None and k in expected:
                row_exp = [k, 'EXP']
                for exp in expected[k]:
                    row_exp.append(int(tx_cnt * exp))
                tbl.append(row_exp)
                rslt = []
                maxerr = 0
                maxmsec = 0
                err_cnt = 0
                err_msec = 0
                for idx in range(cnt):
                    if tx_cnt == 0:
                        err_cnt = val['rx'][idx]
                        err_msec = err_cnt * 1000.0 / pps
                    elif expected[k][idx] == 1:
                        diff = abs(tx_cnt - val['rx'][idx])
                        err_cnt = diff * precision * 100 / tx_cnt
                        err_msec = diff * 1000.0 / pps
                    elif expected[k][idx] == 0:
                        err_cnt = val['rx'][idx] * precision * 100 / tx_cnt
                        err_msec = val['rx'][idx] * 1000.0 / pps
                    if err_cnt > pct * precision:
                        rslt.append(0)
                    else:
                        rslt.append(1)
                    if err_cnt > maxerr * precision:
                        maxerr = err_cnt * 1.0 / precision
                    if err_msec > maxmsec:
                        maxmsec = int(err_msec)
                tbl.append([k, 'COMP'] + rslt)
                if sum(rslt) != len(rslt):
                    failstr[k] = {"pct": maxerr, "msec": maxmsec}
                    tblfail.extend([rowa, rowb, row_exp, [k, 'COMP'] + rslt])
                else:
                    passstr.append(k)
                if maxmsec > max_msec:
                    max_msec = maxmsec
                if maxerr > max_pct:
                    max_pct = maxerr
        summ = "Traffic Verification "
        if not failstr:
            summ += "SUCCEEDED for %d streams!\n" % cnt_streams
        else:
            if max_msec <= loss_msec or max_pct <= loss_pct:
                summ += "PASSED within tolerance of %d msec or %.4f%%\n" \
                        % (loss_msec, loss_pct)
                summ += "%smaximum loss is %d msec and %0.4f%%\n%s" \
                        % (dtab, max_msec, max_pct, dtab)
            summ += "FAILED with unexpected traffic in %d out of %d streams\n" \
                    % (len(failstr), cnt_streams)
        for msg, errs in sorted(failstr.items()):
            summ += "    %s failed with unexpected packets rx at %.4f%%" % \
                    (msg, errs['pct']) + " or loss of %d msec\n" % errs['msec']
        if expected is None:
            summ += Tool.get_tabulate(tbl, headers=header, tablefmt='orgtbl')
        elif failonly:
            # summ += "Streams supressed if passed 100%. Only failed " \
            #         "streams shown below\n\n"
            summ += "The following streams passed:\n    %s\n" % \
                    "\n    ".join(passstr)
            if failstr:
                summ += "\nDetailed traffic statistics for failed streams\n"
                summ += Tool.get_tabulate(tblfail, headers=header,
                                          tablefmt='orgtbl')
        else:
            summ += Tool.get_tabulate(tbl, headers=header, tablefmt='orgtbl')
        if log_console:
            ntlog(summ)
        return summ

    def get_result_from_db(self, dbfile=None, fmt="dict", port_alias=None):
        """
        Get result from results.db for Spirent Test Center
        :param dbfile:
        :param fmt:
        :param port_alias:
        :return:
        """
        if not dbfile.startswith("/"):
            logdir = self.logdir
            dbfile = "/".join([logdir, dbfile])
        result = []
        self._db_create_table_txrxeot(dbfile)
        for name in ['rxSBPort', 'txSBPort']:
            stmt = self._db_get_result_sql_stmt(name)
            result.extend(Tool.sqlite_query(dbfile, stmt, 'dict'))
        return self._stc_export_result(result, fmt, port_alias)

    def _stc_export_result(self, result, fmt='dict', port_alias=None,
                           port_original=False, rtifonly=True):
        """
        port_alias is in format of [{'alias': 'port1',
                    'name': '10.10.10.10-2-10'}, {...}, ... ]
        :param result:
        :param fmt:
        :param port_alias:
        :return:
        """
        ports = {}
        table = {}
        for row in result:
            if row['StreamBlockName'] not in table:
                table[row['StreamBlockName']] = {'tx': {}, 'rx': {}}
            if 'TxPortName' in row:
                pname = self._stc_clean_port_name(row['TxPortName'])
                if pname not in ports:
                    ports[pname] = 1
                table[row['StreamBlockName']]['tx'][pname] = row['TxFrameCount']
            elif 'RxPortName' in row:
                pname = self._stc_clean_port_name(row['RxPortName'])
                if pname not in ports:
                    ports[pname] = 1
                table[row['StreamBlockName']]['rx'][pname] = row['RxFrameCount']
        header = ['StreamBlock', 'T/R']
        porta = []
        porto = []
        portname = []
        if port_alias is None:
            ports = sorted(ports.keys())
            for palias in ports:
                if rtifonly:
                    porta.append(palias[palias.find("/")+1:])
                else:
                    porta.append(palias)
        else:
            for val in port_alias:
                porta.append(val['alias'])
                pname = val['name']
                portname.append(pname)
                if pname in ports:
                    porto.append(pname)
                else:
                    notfound = True
                    for pn_orig in ports:
                        if pname == pn_orig[pn_orig.find("/")+1:]:
                            porto.append(pn_orig)
                            notfound = False
                            break
                    if notfound:
                        porto.append(pname)
            ports = porto
        header.extend(porta)
        if fmt == 'dict':
            summ = {'header': header}
            if portname and port_original:
                summ['rt_intf'] = ['RT Intf', ''] + portname
        else:
            summ = [header]
            if portname and port_original:
                summ.append(['RT Intf', ''] + portname)
        for sblock in sorted(table.keys()):
            rows = [[], []]
            for port in ports:
                if port in table[sblock]['tx']:
                    rows[0].append(table[sblock]['tx'][port])
                else:
                    rows[0].append(0)
                if port in table[sblock]['rx']:
                    rows[1].append(table[sblock]['rx'][port])
                else:
                    rows[1].append(0)
            if fmt == 'list':
                records = [[sblock, 'tx'], [sblock, 'rx']]
                for idx in [0, 1]:
                    records[idx].extend(rows[idx])
                summ.extend(records)
            else:
                summ[sblock] = {'tx': rows[0], 'rx': rows[1]}
        return summ

    @staticmethod
    def _stc_clean_port_name(name):
        idx = name.find('//')
        if idx == -1:
            clean_name = name.replace("-", "/")
        else:
            clean_name = name[:idx-1].replace("-", "/")
        return clean_name
