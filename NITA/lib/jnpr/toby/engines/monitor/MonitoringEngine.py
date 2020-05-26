"""
Monitoring Engine class and methods
"""
# pylint: disable=C0302
# pylint: disable=maybe-no-member

import datetime
import io
import json
import os
import re
import sqlite3
import threading
import time

import humanfriendly
import numpy as np
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import yaml
from jnpr.toby.exception.toby_exception import TobyException
from jnpr.toby.hldcl.device import Device
from jnpr.toby.hldcl.device import execute_cli_command_on_device
from jnpr.toby.hldcl.device import execute_shell_command_on_device
from jnpr.toby.hldcl.device import execute_vty_command_on_device
from jnpr.toby.hldcl.device import reconnect_to_device
from jnpr.toby.hldcl.device import set_current_controller
from jnpr.toby.hldcl.device import set_current_system_node
from jnpr.toby.hldcl.device import set_device_log_level
from jnpr.toby.hldcl.device import switch_to_superuser
from jnpr.toby.logger.logger import get_log_dir
from jnpr.toby.utils.Vars import Vars
from jsonpath_rw import parse
from lxml import etree as ET
from sqlalchemy import create_engine


def _get_testcase_starttime():
    try:
        from robot.libraries.BuiltIn import BuiltIn
        from robot.running.context import EXECUTION_CONTEXTS
        ctx = EXECUTION_CONTEXTS.current if not False else EXECUTION_CONTEXTS.top
        if ctx is None:
            print('Cannot access Robot execution context')
            return None
        else:
            starttime = ctx.test.starttime
    except:
        return None
    datetime_object = datetime.datetime.strptime(str(starttime), '%Y%m%d %H:%M:%S.%f')
    return datetime_object


def _find_file(infile):
    if os.path.isfile(infile):
        return infile
    if Vars().get_global_variable('${SUITE_SOURCE}'):
        src_path = os.path.dirname(Vars().get_global_variable('${SUITE_SOURCE}'))
        suite_file = os.path.join(src_path, infile)
        if os.path.isfile(suite_file):
            return suite_file
    print("infile %s not found" % infile)
    return infile


def _strip_xml_namespace(xml_string):
    xml = ET.fromstring(xml_string).getchildren()[0]
    query = ".//*[namespace-uri()!='']"
    for ele in xml.xpath(query):
        ele.tag = ET.QName(ele).localname
    return xml


class MonitoringEngine:
    """
    Monitoring Engine class for Toby
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    is_running = None
    interval = ''
    threads = []
    afn = ''
    afh = ''
    datadir = ''
    re_pfe_filename = ''
    re_processes_filename = ''
    re_data_filename = ''
    re_unstructured_data_filename = ''
    custom_data_filename = ''
    re_memory_alert_level = 100
    re_cpu_alert_level = 100
    pfe_memory_alert_level = 100
    pfe_cpu_alert_level = 100
    syslog_alerts = {}

    def __init__(self, interval=5):
        self.interval = interval
        self.is_running = False

    def _monitor_re_pfe(self, resource, interval, log_level):

        fname = 'RE_PFE monitoring'
        # do not monitor if tag "NOMONREPFE" is set
        nomonlist = t.get_resource_list(tag='NOMONREPFE')
        if resource in nomonlist:
            print("Not monitoring RE/PFE for resource %s..." % resource)
            return

        # get host info
        name = t['resources'][resource]['system']['primary']['name']
        model = t['resources'][resource]['system']['primary']['model']
        sys = dict(t['resources'][resource]['system'])
        sys.pop('dh')

        if str(log_level).upper() == 'OFF':
            dev = Device(system=sys, global_logger=False, device_logger=False)
        else:
            dev = Device(system=sys)
            set_device_log_level(dev, log_level)
        version = dev.get_version()
        evo = dev.is_evo()

        # initialize data files
        hostdir = "%s/%s" % (self.datadir, name)
        os.makedirs(hostdir, exist_ok=True)
        re_pfe_db = create_engine("sqlite:///%s" % self.re_pfe_filename)

        # dbfile = "file:" + self.re_pfe_filename + "?mode=rwc"
        # re_pfe_db = sqlite3.connect(dbfile, uri=True)

        def _insert_null(name, db):
            redf = pd.read_sql_query('select * from data where host = :host and type = :type', db,
                                     params={'host': name, 'type': 'RE'})
            recpudf = pd.read_sql_query('select * from data where host = :host and type = :type', db,
                                        params={'host': name, 'type': 'RECPU'})
            pfedf = pd.read_sql_query('select * from data where host = :host and type = :type', db,
                                      params={'host': name, 'type': 'PFE'})
            date = datetime.datetime.now()
            for fru in redf.FRU.unique():
                tlist = [date, name, 'RE', fru, None, None]
                df = pd.DataFrame(data=[tlist], columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                df.to_sql('data', db, if_exists='append')
            for fru in recpudf.FRU.unique():
                tlist = [date, name, 'RECPU', fru, None, None]
                df = pd.DataFrame(data=[tlist], columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                df.to_sql('data', db, if_exists='append')
            for fru in pfedf.FRU.unique():
                tlist = [date, name, 'PFE', fru, None, None]
                df = pd.DataFrame(data=[tlist], columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                df.to_sql('data', db, if_exists='append')

        # collect data
        while self.is_running:
            # get RE data
            date = datetime.datetime.now()
            cmd = 'show chassis routing-engine'
            try:
                rei = execute_cli_command_on_device(device=dev, command=cmd, format='xml')
            except:
                print("Error for command %s on %s" % (cmd, name))
                try:
                    print("Reconnecting to %s in %s" % (name, fname))
                    _insert_null(name, re_pfe_db)
                    reconnect_to_device(device=dev, interval=interval)
                    print("Reconnected to %s in %s" % (name, fname))
                    continue
                except:
                    print("Reconnect failed to %s in %s" % (name, fname))
                    return
            try:
                rei = _strip_xml_namespace(rei)
            except:
                print("Error stripping namespace on %s command %s in %s" % (name, cmd, fname))
                continue
            if rei is None:
                print("No RE data for resource %s" % resource)
                continue
            if not rei.tag:
                print("No RE data tag for resource %s" % resource)
                continue
            if rei.tag == 'multi-routing-engine-results':
                for mrei in rei.findall('multi-routing-engine-item'):
                    rename = mrei.findtext('re-name')
                    for rengine in mrei.findall('.//route-engine'):
                        slot = rengine.findtext('slot', default=0)
                        fru = rename + "-re" + str(slot)
                        mem = int(rengine.findtext('memory-buffer-utilization', default=0))
                        cpu = 100 - int(rengine.findtext('cpu-idle', default=100))
                        tlist = [date, name, 'RE', fru, mem, cpu]
                        dataframe = pd.DataFrame(data=[tlist],
                                                 columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                        try:
                            dataframe.to_sql('data', re_pfe_db, if_exists='append')
                        except:
                            continue
                        if int(mem) > (self.re_memory_alert_level * 0.8):
                            print(
                                "[ALERT:RE:MEM]: %s RE memory utilization is %s%% on %s %s" % (
                                    date, mem, name, fru))
                        if int(cpu) > (self.re_cpu_alert_level * 0.8):
                            print("[ALERT:RE:CPU]: %s RE CPU utilization is %s%% on %s %s" % (
                                date, cpu, name, fru))
            else:
                for rengine in rei.findall('route-engine'):
                    slot = rengine.findtext('slot', default=0)
                    fru = "re" + str(slot)
                    mem = int(rengine.findtext('memory-buffer-utilization', default=0))
                    cpu = 100 - int(rengine.findtext('cpu-idle', default=100))
                    tlist = [date, name, 'RE', fru, mem, cpu]
                    dataframe = pd.DataFrame(data=[tlist], columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                    try:
                        dataframe.to_sql('data', re_pfe_db, if_exists='append')
                    except:
                        continue
                    if int(mem) > (self.re_memory_alert_level * 0.8):
                        print("[ALERT:RE:MEM]: %s RE memory utilization is %s%% on %s %s" % (
                            date, mem, name, fru))
                    if int(cpu) > (self.re_cpu_alert_level * 0.8):
                        print("[ALERT:RE:CPU]: %s RE CPU utilization is %s%% on %s %s" % (
                            date, cpu, name, fru))
            for node in dev.nodes.keys():
                set_current_system_node(device=dev, system_node=node)
                current_controller_name = dev.get_current_controller_name()
                if current_controller_name is None:
                    continue
                for controller in dev.current_node.controllers.keys():
                    set_current_controller(device=dev, controller=controller)
                    hostname = t['resources'][resource]['system'][node]['controllers'][controller]['hostname']
                    if evo:
                        cmd = "mpstat -P ALL 1 1 | grep ^Average"
                        regexp_index = re.compile('Average:\s*(\S*)')
                        regexp_idle = re.compile('(\S*)\s*$')
                        try:
                            rei = execute_shell_command_on_device(device=dev, command=cmd)
                        except:
                            print("Error for command %s on %s" % (cmd, hostname))
                            try:
                                print("Reconnecting to %s in %s" % (name, fname))
                                _insert_null(name, re_pfe_db)
                                reconnect_to_device(device=dev, interval=interval)
                                print("Reconnected to %s in %s" % (name, fname))
                                continue
                            except:
                                print("Reconnect failed to %s in %s" % (name, fname))
                                return
                        lines = rei.splitlines(True)
                        for line in lines:
                            if not line:
                                continue
                            if "CPU" in line:
                                continue
                            if "all" in line:
                                continue
                            if not regexp_index.search(line):
                                continue
                            if not regexp_idle.search(line):
                                continue
                            cpu_index = regexp_index.search(line).groups()[0]
                            cpu_idle = regexp_idle.search(line).groups()[0]
                            cpu = 100 - float(cpu_idle)
                            mem = '0'
                            if len(dev.nodes.keys()) > 1:
                                fru = node + '-' + controller + '-' + "cpu" + cpu_index
                            else:
                                fru = controller + '-' + "cpu" + cpu_index
                            tlist = [date, name, 'RECPU', fru, mem, cpu]
                            dataframe = pd.DataFrame(data=[tlist],
                                                     columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                            try:
                                dataframe.to_sql('data', re_pfe_db, if_exists='append')
                            except:
                                continue
                    else:
                        cmd = 'top -b -d2 -s1 | grep -i ^CPU'
                        regexp_index = re.compile('CPU\s*(\S*):')
                        regexp_idle = re.compile('(\S+)%\s+idle')
                        try:
                            rei = execute_shell_command_on_device(device=dev, command=cmd)
                        except:
                            print("Error for command %s on %s" % (cmd, hostname))
                            try:
                                print("Reconnecting to %s in %s" % (name, fname))
                                _insert_null(name, re_pfe_db)
                                reconnect_to_device(device=dev, interval=interval)
                                print("Reconnected to %s in %s" % (name, fname))
                                continue
                            except:
                                print("Reconnect failed to %s in %s" % (name, fname))
                                return
                        lines = rei.splitlines(True)
                        for line in lines:
                            if not line:
                                continue
                            if not regexp_index.search(line):
                                continue
                            if not regexp_idle.search(line):
                                continue
                            if "CPU:" in line:
                                cpu_index = '0'
                            else:
                                cpu_index = regexp_index.search(line).groups()[0]
                            cpu_idle = regexp_idle.search(line).groups()[0]
                            cpu = 100 - float(cpu_idle)
                            mem = '0'
                            if len(dev.nodes.keys()) > 1:
                                fru = node + '-' + controller + '-' + "cpu" + cpu_index
                            else:
                                fru = controller + '-' + "cpu" + cpu_index
                            tlist = [date, name, 'RECPU', fru, mem, cpu]
                            dataframe = pd.DataFrame(data=[tlist],
                                                     columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                            try:
                                dataframe.to_sql('data', re_pfe_db, if_exists='append')
                            except:
                                continue
            date = datetime.datetime.now()
            # get PFE data
            if len(dev.current_node.controllers.keys()) > 1:
                try:
                    if not dev.current_node.is_node_master():
                        set_current_controller(device=dev, controller='Master')
                except:
                    print("Error in is_node_master")
                    continue
            cmd = 'show chassis fpc'
            try:
                pfei = execute_cli_command_on_device(device=dev, command=cmd, format='xml')
            except:
                print("Error for command %s on %s" % (cmd, name))
                continue
            try:
                pfei = _strip_xml_namespace(pfei)
            except:
                print("Error stripping namespace on %s command %s in %s" % (name, cmd, fname))
                continue
            if pfei is None:
                print("No PFE data for resource %s" % resource)
                continue
            try:
                if not pfei.tag:
                    print("No PFE data for resource %s" % resource)
                    continue
            except:
                continue
            if pfei.tag == 'multi-routing-engine-results':
                for mrei in pfei.findall('multi-routing-engine-item'):
                    rename = mrei.findtext('re-name')
                    for fpc in mrei.findall('.//fpc'):
                        state = fpc.findtext('state')
                        if state == 'Empty':
                            continue
                        slot = fpc.findtext('slot')
                        fru = rename + "-fpc" + slot
                        mem = int(fpc.findtext('memory-heap-utilization', default=0))
                        cpu = int(fpc.findtext('cpu-total', default=0))
                        tlist = [date, name, 'PFE', fru, mem, cpu]
                        dataframe = pd.DataFrame(data=[tlist],
                                                 columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                        try:
                            dataframe.to_sql('data', re_pfe_db, if_exists='append')
                        except:
                            continue
                        if int(mem) > (self.pfe_memory_alert_level * 0.8):
                            print(
                                "[ALERT:PFE:MEM]: %s PFE memory utilization is %s%% on %s %s" % (
                                    date, mem, name, fru))
                        if int(cpu) > (self.pfe_cpu_alert_level * 0.8):
                            print(
                                "[ALERT:PFE:CPU]: %s PFE CPU utilization is %s%% on %s %s" % (
                                    date, cpu, name, fru))
            else:
                for fpc in pfei.findall('fpc'):
                    state = fpc.findtext('state')
                    if state == 'Empty':
                        continue
                    slot = fpc.findtext('slot')
                    fru = "fpc" + slot
                    mem = int(fpc.findtext('memory-heap-utilization', default=0))
                    cpu = int(fpc.findtext('cpu-total', default=0))
                    tlist = [date, name, 'PFE', fru, mem, cpu]
                    dataframe = pd.DataFrame(data=[tlist], columns=['DATETIME', 'HOST', 'TYPE', 'FRU', 'MEM', 'CPU'])
                    try:
                        dataframe.to_sql('data', re_pfe_db, if_exists='append')
                    except:
                        continue
                    if int(mem) > (self.pfe_memory_alert_level * 0.8):
                        print(
                            "[ALERT:PFE:MEM]: %s PFE memory utilization is %s%% on %s %s" % (
                                date, mem, name, fru))
                    if int(cpu) > (self.pfe_cpu_alert_level * 0.8):
                        print("[ALERT:PFE:CPU]: %s PFE CPU utilization is %s%% on %s %s" % (
                            date, cpu, name, fru))
            time.sleep(interval)

        # do not create graphs if tag "NOGRAPH" is set
        nographlist = t.get_resource_list(tag='NOGRAPH')
        if resource in nographlist:
            print("Not creating graphs for resource %s..." % resource)
            return

        # read annotations into pandas dataframe
        adf = pd.read_csv(self.afn, parse_dates=['DATETIME'])

        # plot RE data
        redf = pd.read_sql_query(
            'select * from data where host = :host and type = :type',
            re_pfe_db,
            params={'host': name, 'type': 'RE'})
        redf2 = pd.read_sql_query(
            'select * from data where host = :host and type = :type',
            re_pfe_db,
            params={'host': name, 'type': 'RECPU'})
        recpudatalist = []
        shapes = []
        annotations = []
        for fru in redf.FRU.unique():
            tdf = redf[redf['FRU'] == fru]
            cpu = go.Scatter(x=tdf['DATETIME'], y=tdf['CPU'], name=fru)
            recpudatalist.append(cpu)
        for fru in redf2.FRU.unique():
            tdf = redf2[redf2['FRU'] == fru]
            cpu = go.Scatter(x=tdf['DATETIME'], y=tdf['CPU'], name=fru)
            recpudatalist.append(cpu)
        recputitle = t['framework_variables'].get("fv-recputitle", "")
        if recputitle == "":
            recputitle = "RE CPU Monitor - %s/%s - %s" % (name, model.lower(), version)
        recpuyaxis = t['framework_variables'].get("fv-recpuyaxis", "")
        if recpuyaxis == "":
            recpuyaxis = "RE CPU Utilization (%)"
        recpulayout = dict(
            title=recputitle,
            yaxis=dict(title=recpuyaxis),
            showlegend=True
        )
        for row in adf.itertuples():
            shape = dict(
                type='line',
                opacity=0.5,
                x0=row.DATETIME,
                x1=row.DATETIME,
                yref='paper',
                y0=0,
                y1=1,
                line=dict(
                    color='black',
                    dash='dash',
                )
            )
            shapes.append(shape)
            annotation = dict(
                text=row.ANNOTATION,
                showarrow=False,
                textangle=-90,
                xanchor='left',
                opacity=0.5,
                x=row.DATETIME,
                yref='paper',
                y='1',
            )
            annotations.append(annotation)
        recpulayout.update(dict(shapes=shapes))
        recpulayout.update(dict(annotations=annotations))
        recpufigure = dict(data=recpudatalist, layout=recpulayout)
        recpufn = "%s/%s.re.cpu.html" % (hostdir, name)
        if not recpudatalist:
            print("No RE CPU data for resource %s" % resource)
        else:
            py.offline.plot(recpufigure, filename=recpufn, auto_open=False)

        rememdatalist = []
        shapes = []
        annotations = []
        for fru in redf.FRU.unique():
            tdf = redf[redf['FRU'] == fru]
            mem = go.Scatter(x=tdf['DATETIME'], y=tdf['MEM'], name=fru)
            rememdatalist.append(mem)
        rememtitle = t['framework_variables'].get("fv-rememtitle", "")
        if rememtitle == "":
            rememtitle = "RE CPU Monitor - %s/%s - %s" % (name, model.lower(), version)
        rememyaxis = t['framework_variables'].get("fv-rememyaxis", "")
        if rememyaxis == "":
            rememyaxis = "RE Memory Utilization (%)"
        rememlayout = dict(
            title=rememtitle,
            yaxis=dict(title=rememyaxis),
            showlegend=True
        )
        for row in adf.itertuples():
            shape = dict(
                type='line',
                opacity=0.5,
                x0=row.DATETIME,
                x1=row.DATETIME,
                yref='paper',
                y0=0,
                y1=1,
                line=dict(
                    color='black',
                    dash='dash',
                )
            )
            shapes.append(shape)
            annotation = dict(
                text=row.ANNOTATION,
                showarrow=False,
                textangle=-90,
                xanchor='left',
                opacity=0.5,
                x=row.DATETIME,
                yref='paper',
                y='1',
            )
            annotations.append(annotation)
        rememlayout.update(dict(shapes=shapes))
        rememlayout.update(dict(annotations=annotations))
        rememfigure = dict(data=rememdatalist, layout=rememlayout)
        rememfn = "%s/%s.re.mem.html" % (hostdir, name)
        if not rememdatalist:
            print("No RE memory data for resource %s" % resource)
        else:
            py.offline.plot(rememfigure, filename=rememfn, auto_open=False)

        # plot PFE data
        pfedf = pd.read_sql_query(
            'select * from data where host = :host and type = :type',
            re_pfe_db,
            params={'host': name, 'type': 'PFE'})
        if pfedf['MEM'].dtype == np.object:
            pfedf = pfedf[pfedf.MEM != "None"]
            pfedf[['MEM']] = pfedf[['MEM']].apply(pd.to_numeric)
        if pfedf['CPU'].dtype == np.object:
            pfedf = pfedf[pfedf.CPU != "None"]
            pfedf[['CPU']] = pfedf[['CPU']].apply(pd.to_numeric)
        pfememdatalist = []
        pfecpudatalist = []
        shapes = []
        annotations = []
        for fru in pfedf.FRU.unique():
            tdf = pfedf[pfedf['FRU'] == fru]
            mem = go.Scatter(x=tdf['DATETIME'], y=tdf['MEM'], name=fru)
            pfememdatalist.append(mem)
            cpu = go.Scatter(x=tdf['DATETIME'], y=tdf['CPU'], name=fru)
            pfecpudatalist.append(cpu)
        pfememtitle = t['framework_variables'].get("fv-pfememtitle", "")
        if pfememtitle == "":
            pfememtitle = "RE CPU Monitor - %s/%s - %s" % (name, model.lower(), version)
        pfememyaxis = t['framework_variables'].get("fv-pfememyaxis", "")
        if pfememyaxis == "":
            pfememyaxis = 'PFE Memory Utilization (%)'
        pfememlayout = dict(
            title=pfememtitle,
            yaxis=dict(title=pfememyaxis),
            showlegend=True
        )
        for row in adf.itertuples():
            shape = dict(
                type='line',
                opacity=0.5,
                x0=row.DATETIME,
                x1=row.DATETIME,
                yref='paper',
                y0=0,
                y1=1,
                line=dict(
                    color='black',
                    dash='dash',
                )
            )
            shapes.append(shape)
            annotation = dict(
                text=row.ANNOTATION,
                showarrow=False,
                textangle=-90,
                xanchor='left',
                opacity=0.5,
                x=row.DATETIME,
                yref='paper',
                y='1',
            )
            annotations.append(annotation)
        pfememlayout.update(dict(shapes=shapes))
        pfememlayout.update(dict(annotations=annotations))
        pfememfigure = dict(data=pfememdatalist, layout=pfememlayout)
        pfememfn = "%s/%s.pfe.mem.html" % (hostdir, name)
        if not pfememdatalist:
            print("No PFE memory data for resource %s" % resource)
        else:
            py.offline.plot(pfememfigure, filename=pfememfn, auto_open=False)

        shapes = []
        annotations = []
        pfecputitle = t['framework_variables'].get("fv-pfecputitle", "")
        if pfecputitle == "":
            pfecputitle = "RE CPU Monitor - %s/%s - %s" % (name, model.lower(), version)
        pfecpuyaxis = t['framework_variables'].get("fv-pfecpuyaxis", "")
        if pfecpuyaxis == "":
            pfecpuyaxis = 'PFE CPU Utilization (%)'
        pfecpulayout = dict(
            title=pfecputitle,
            yaxis=dict(title=pfecpuyaxis),
            showlegend=True
        )
        for row in adf.itertuples():
            shape = dict(
                type='line',
                opacity=0.5,
                x0=row.DATETIME,
                x1=row.DATETIME,
                yref='paper',
                y0=0,
                y1=1,
                line=dict(
                    color='black',
                    dash='dash',
                )
            )
            shapes.append(shape)
            annotation = dict(
                text=row.ANNOTATION,
                showarrow=False,
                textangle=-90,
                xanchor='left',
                opacity=0.5,
                x=row.DATETIME,
                yref='paper',
                y='1',
            )
            annotations.append(annotation)
        pfecpulayout.update(dict(shapes=shapes))
        pfecpulayout.update(dict(annotations=annotations))
        pfecpufigure = dict(data=pfecpudatalist, layout=pfecpulayout)
        pfecpufn = "%s/%s.pfe.cpu.html" % (hostdir, name)
        if not pfecpudatalist:
            print("No PFE CPU data for resource %s" % resource)
        else:
            py.offline.plot(pfecpufigure, filename=pfecpufn, auto_open=False)

    def _monitor_re_processes(self, resource, interval, processes, log_level):
        fname = 'RE_PROCESS monitoring'
        # get host info
        name = t['resources'][resource]['system']['primary']['name']
        model = t['resources'][resource]['system']['primary']['model']
        sys = dict(t['resources'][resource]['system'])
        sys.pop('dh')
        if str(log_level).upper() == 'OFF':
            dev = Device(system=sys, global_logger=False, device_logger=False)
        else:
            dev = Device(system=sys)
            set_device_log_level(dev, log_level)
        version = dev.get_version()

        # initialize data files
        hostdir = "%s/%s" % (self.datadir, name)
        os.makedirs(hostdir, exist_ok=True)
        processes_db = create_engine("sqlite:///%s" % self.re_processes_filename)

        # dbfile = "file:" + self.re_processes_filename + "?mode=rwc"
        # processes_db = sqlite3.connect(dbfile, uri=True)

        def _insert_null(dev, resource, db):
            date = datetime.datetime.now()
            for node in dev.nodes.keys():
                for controller in dev.current_node.controllers.keys():
                    hostname = t['resources'][resource]['system'][node]['controllers'][controller]['hostname']
                    for process in processes:
                        if isinstance(process, str):
                            redf = pd.read_sql_query(
                                'select * from data where command = :cmd and node = :node and controller = :ctrl and host '
                                '= :host',
                                processes_db,
                                params={'cmd': process, 'node': node, 'ctrl': controller, 'host': hostname})
                            for pid in redf.PID.unique():
                                redfpid = redf[redf['PID'] == pd.to_numeric(pid)]
                                if not redfpid.empty:
                                    tlist = [date, hostname, process, pid, node, controller, None, None]
                                    df = pd.DataFrame(data=[tlist],
                                                      columns=['DATETIME', 'HOST', 'COMMAND', 'PID', 'NODE',
                                                               'CONTROLLER', 'MEM',
                                                               'CPU'])
                                    df.to_sql('data', db, if_exists='append')
                        else:
                            for name in process:
                                if process[name] is None:
                                    continue
                                redf = pd.read_sql_query(
                                    'select * from data where command = :cmd and node = :node and controller = :ctrl and host '
                                    '= :host',
                                    processes_db,
                                    params={'cmd': name, 'node': node, 'ctrl': controller, 'host': hostname})
                                for pid in redf.PID.unique():
                                    redfpid = redf[redf['PID'] == pd.to_numeric(pid)]
                                    if not redfpid.empty:
                                        tlist = [date, hostname, name, pid, node, controller, None, None]
                                        df = pd.DataFrame(data=[tlist],
                                                          columns=['DATETIME', 'HOST', 'COMMAND', 'PID', 'NODE',
                                                                   'CONTROLLER',
                                                                   'MEM',
                                                                   'CPU'])
                                        df.to_sql('data', db, if_exists='append')

        # get data
        while self.is_running:
            for node in dev.nodes.keys():
                set_current_system_node(device=dev, system_node=node)
                current_controller_name = dev.get_current_controller_name()
                if current_controller_name is None:
                    continue
                for controller in dev.current_node.controllers.keys():
                    set_current_controller(device=dev, controller=controller)
                    hostname = t['resources'][resource]['system'][node]['controllers'][controller]['hostname']
                    command = "show system processes extensive"
                    date = datetime.datetime.now()
                    try:
                        rei = execute_cli_command_on_device(device=dev, command=command)
                    except:
                        print("Error for command %s on %s" % (command, hostname))
                        try:
                            print("Reconnecting to %s in %s" % (name, fname))
                            _insert_null(dev, resource, processes_db)
                            reconnect_to_device(device=dev, interval=interval)
                            print("Reconnected to %s in %s" % (name, fname))
                            continue
                        except:
                            print("Reconnect failed to %s in %s" % (name, fname))
                            return
                    if rei.count('node:') > 1:
                        command += " node %s" % controller
                        try:
                            rei = execute_cli_command_on_device(device=dev, command=command)
                        except:
                            print("Error for command %s on %s" % (command, hostname))
                            continue
                    lines = rei.splitlines(True)
                    output = io.StringIO()
                    header_added = False
                    for line in lines:
                        if "COMMAND" in line:
                            if not header_added:
                                print(line, file=output)
                                header_added = True
                        elif not line:
                            pass
                        elif line.startswith("last"):
                            pass
                        elif "processes:" in line:
                            pass
                        elif line.startswith("Mem:"):
                            pass
                        elif line.startswith("Swap:"):
                            pass
                        elif " 0K " in line:
                            pass
                        elif "Swap" in line:
                            pass
                        elif "% nice," in line:
                            pass
                        elif line.startswith("---"):
                            pass
                        elif line.startswith("node:"):
                            pass
                        elif line.startswith("top"):
                            pass
                        elif line.startswith("Tasks:"):
                            pass
                        elif line.startswith("%Cpu"):
                            pass
                        elif "total," in line:
                            pass
                        else:
                            print(line, file=output)
                    try:
                        output.seek(0)
                        redf = pd.read_csv(output, delim_whitespace=True)
                    except:
                        print("Error with RE process data file %s on %s" % (output, hostname))
                        continue
                    output.close()
                    try:
                        redf.drop_duplicates(subset=['PID'], keep='first')
                        if 'WCPU' in redf.columns:
                            redf['WCPU'] = redf['WCPU'].map(lambda x: x.rstrip('%'))
                            redf['WCPU'] = redf['WCPU'].apply(pd.to_numeric)
                            redf.rename(columns={'WCPU': 'CPU'}, inplace=True)
                        if '%CPU' in redf.columns:
                            redf['%CPU'] = redf['%CPU'].apply(pd.to_numeric)
                            redf.rename(columns={'%CPU': 'CPU'}, inplace=True)
                        if 'SIZE' in redf.columns:
                            if not np.issubdtype(redf['SIZE'].dtype, np.number):
                                redf['SIZE'] = redf['SIZE'].apply(humanfriendly.parse_size)
                            redf['SIZE'] = redf['SIZE'].apply(pd.to_numeric)
                            redf.rename(columns={'SIZE': 'MEM'}, inplace=True)
                        if 'VIRT' in redf.columns:
                            if not np.issubdtype(redf['VIRT'].dtype, np.number):
                                redf['VIRT'] = redf['VIRT'].apply(humanfriendly.parse_size)
                            redf['VIRT'] = redf['VIRT'].apply(pd.to_numeric)
                            redf.rename(columns={'VIRT': 'MEM'}, inplace=True)
                        if 'RES' in redf.columns:
                            if not np.issubdtype(redf['RES'].dtype, np.number):
                                redf['RES'] = redf['RES'].apply(humanfriendly.parse_size)
                            redf['RES'] = redf['RES'].apply(pd.to_numeric)
                    except:
                        print("Error processing RE process data file on %s" % hostname)
                        continue
                    dates = []
                    resources = []
                    nodes = []
                    controllers = []
                    hosts = []
                    c_column = []
                    thr_column = []
                    for _, _ in redf.iterrows():
                        dates.append(date)
                        resources.append(resource)
                        nodes.append(node)
                        controllers.append(controller)
                        hosts.append(hostname)
                        c_column.append('0')
                        thr_column.append('1')
                    redf['DATETIME'] = dates
                    redf['RESOURCE'] = resources
                    redf['NODE'] = nodes
                    redf['CONTROLLER'] = controllers
                    redf['HOST'] = hosts
                    if 'C' not in redf.columns:
                        redf['C'] = c_column
                    if 'THR' not in redf.columns:
                        redf['THR'] = thr_column
                    try:
                        redf.to_sql('data', processes_db, if_exists='append')
                    except:
                        continue
                    for process in processes:
                        if not isinstance(process, str):
                            for name in process:
                                if process[name] is None:
                                    continue
                                if "alert" in process[name].keys():
                                    tdf = redf[redf['COMMAND'] == name]
                                    if tdf.empty:
                                        continue
                                    if "mem" in process[name]['alert'].keys():
                                        if process[name]['alert']['mem'] is not None:
                                            memalert = process[name]['alert']['mem']
                                            result = tdf.iloc[0]['MEM']
                                            if float(result) > (float(memalert) * 0.8):
                                                percent = int(float(result) / float(memalert) * 100)
                                                formatted_result = humanfriendly.format_size(result)
                                                formatted_threshold = humanfriendly.format_size(int(memalert))
                                                print(
                                                    "[ALERT:RE:PROCESS:MEM]: %s %s memory %s is %s%% of threshold %s "
                                                    "on %s" % (
                                                        date, name, formatted_result, percent, formatted_threshold,
                                                        hostname))
                                    if "cpu" in process[name]['alert'].keys():
                                        if process[name]['alert']['cpu'] is not None:
                                            cpualert = process[name]['alert']['cpu']
                                            result = tdf.iloc[0]['CPU']
                                            if float(result) > (float(cpualert) * 0.8):
                                                percent = int(float(result) / float(cpualert) * 100)
                                                threshold = int(cpualert)
                                                print(
                                                    "[ALERT:RE:PROCESS:CPU]: %s %s CPU %s%% is %s%% of threshold %s%% "
                                                    "on %s" % (
                                                        date, name, result, percent, threshold,
                                                        hostname))
            time.sleep(interval)

        # do not create graphs if tag "NOGRAPH" is set
        nographlist = t.get_resource_list(tag='NOGRAPH')
        if resource in nographlist:
            print("Not creating graphs for resource %s..." % resource)
            return

        # read annotations into pandas dataframe
        adf = pd.read_csv(self.afn, parse_dates=['DATETIME'])

        # create re graphs
        for node in dev.nodes.keys():
            set_current_system_node(device=dev, system_node=node)
            current_controller_name = dev.get_current_controller_name()
            if current_controller_name is None:
                continue
            for controller in dev.current_node.controllers.keys():
                set_current_controller(device=dev, controller=controller)
                hostname = t['resources'][resource]['system'][node]['controllers'][controller]['hostname']
                memdatalist = []
                cpudatalist = []
                shapes = []
                annotations = []
                for process in processes:
                    if isinstance(process, str):
                        redf = pd.read_sql_query(
                            'select * from data where command = :cmd and node = :node and controller = :ctrl and host '
                            '= :host',
                            processes_db,
                            params={'cmd': process, 'node': node, 'ctrl': controller, 'host': hostname})
                        for pid in redf.PID.unique():
                            redfpid = redf[redf['PID'] == pd.to_numeric(pid)]
                            if not redfpid.empty:
                                processname = str(process) + '(' + str(pid) + ')'
                                mem = go.Scatter(x=redfpid['DATETIME'], y=redfpid['MEM'], name="%s" % processname)
                                memdatalist.append(mem)
                                cpu = go.Scatter(x=redfpid['DATETIME'], y=redfpid['CPU'], name="%s" % processname)
                                cpudatalist.append(cpu)
                    else:
                        for name in process:
                            if process[name] is None:
                                continue
                            redf = pd.read_sql_query(
                                'select * from data where command = :cmd and node = :node and controller = :ctrl and '
                                'host = :host',
                                processes_db,
                                params={'cmd': name, 'node': node, 'ctrl': controller, 'host': hostname})
                            for pid in redf.PID.unique():
                                redfpid = redf[redf['PID'] == pd.to_numeric(pid)]
                                if not redfpid.empty:
                                    processname = str(name) + '(' + str(pid) + ')'
                                    mem = go.Scatter(x=redfpid['DATETIME'], y=redfpid['MEM'],
                                                     name="%s" % processname)
                                    memdatalist.append(mem)
                                    cpu = go.Scatter(x=redfpid['DATETIME'], y=redfpid['CPU'],
                                                     name="%s" % processname)
                                    cpudatalist.append(cpu)
                layout = dict(
                    title="RE Process Memory Monitor - %s/%s - %s" % (hostname, model.lower(), version),
                    yaxis=dict(title='RE Process Memory Utilization (Bytes)'),
                    showlegend=True
                )
                for row in adf.itertuples():
                    shape = dict(
                        type='line',
                        opacity=0.5,
                        x0=row.DATETIME,
                        x1=row.DATETIME,
                        yref='paper',
                        y0=0,
                        y1=1,
                        line=dict(
                            color='black',
                            dash='dash',
                        )
                    )
                    shapes.append(shape)
                    annotation = dict(
                        text=row.ANNOTATION,
                        showarrow=False,
                        textangle=-90,
                        xanchor='left',
                        opacity=0.5,
                        x=row.DATETIME,
                        yref='paper',
                        y='1',
                    )
                    annotations.append(annotation)
                layout.update(dict(shapes=shapes))
                layout.update(dict(annotations=annotations))
                fig = dict(data=memdatalist, layout=layout)
                if not memdatalist:
                    continue
                py.offline.plot(fig, filename="%s/%s.re.process.mem.html" % (hostdir, hostname), auto_open=False)
                shapes = []
                annotations = []
                layout = dict(
                    title="RE Process CPU Monitor - %s/%s - %s" % (hostname, model.lower(), version),
                    yaxis=dict(title='RE Process CPU Utilization (%)'),
                    showlegend=True
                )
                for row in adf.itertuples():
                    shape = dict(
                        type='line',
                        opacity=0.5,
                        x0=row.DATETIME,
                        x1=row.DATETIME,
                        yref='paper',
                        y0=0,
                        y1=1,
                        line=dict(
                            color='black',
                            dash='dash',
                        )
                    )
                    shapes.append(shape)
                    annotation = dict(
                        text=row.ANNOTATION,
                        showarrow=False,
                        textangle=-90,
                        xanchor='left',
                        opacity=0.5,
                        x=row.DATETIME,
                        yref='paper',
                        y='1',
                    )
                    annotations.append(annotation)
                layout.update(dict(shapes=shapes))
                layout.update(dict(annotations=annotations))
                fig = dict(data=cpudatalist, layout=layout)
                if not cpudatalist:
                    continue
                py.offline.plot(fig, filename="%s/%s.re.process.cpu.html" % (hostdir, hostname), auto_open=False)

    def _monitor_re_data(self, resource, interval, data, log_level):
        fname = 'RE_DATA monitoring'
        # get host info
        name = t['resources'][resource]['system']['primary']['name']
        model = t['resources'][resource]['system']['primary']['model']
        sys = dict(t['resources'][resource]['system'])
        sys.pop('dh')
        if str(log_level).upper() == 'OFF':
            dev = Device(system=sys, global_logger=False, device_logger=False)
        else:
            dev = Device(system=sys)
            set_device_log_level(dev, log_level)
        version = dev.get_version()

        # initialize database
        hostdir = "%s/%s" % (self.datadir, name)
        os.makedirs(hostdir, exist_ok=True)
        data_db = create_engine("sqlite:///%s" % self.re_data_filename)

        # dbfile = "file:" + self.re_data_filename + "?mode=rwc"
        # data_db = sqlite3.connect(dbfile, uri=True)

        def _insert_null(name, data, db):
            date = datetime.datetime.now()
            for graph in data:
                for graphname in graph:
                    if graph[graphname] is None:
                        continue
                    for trace in graph[graphname]:
                        for tracename in trace:
                            if trace[tracename] is None:
                                continue
                            cmd = trace[tracename]['cmd']
                            xpath = trace[tracename]['xpath']
                            try:
                                if not os.stat(self.re_data_filename).st_size:
                                    continue
                            except:
                                continue
                            tlist = [name, cmd, xpath, None, date, graphname]
                            df = pd.DataFrame(data=[tlist],
                                              columns=['NAME', 'CMD', 'XPATH', 'DATA', 'DATETIME', 'GRAPH'])
                            df.to_sql('data', db, if_exists='append')

        # collect data
        while self.is_running:
            for graph in data:
                for graphname in graph:
                    if graph[graphname] is None:
                        continue
                    for trace in graph[graphname]:
                        for tracename in trace:
                            if trace[tracename] is None:
                                continue
                            if len(dev.current_node.controllers.keys()) > 1:
                                try:
                                    if not dev.current_node.is_node_master():
                                        set_current_controller(device=dev, controller='Master')
                                except:
                                    print("Error checking for mastership on %s in %s" % (name, fname))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, data, data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            cmd = trace[tracename]['cmd']
                            xpath = trace[tracename]['xpath']
                            date = datetime.datetime.now()
                            try:
                                rei = execute_cli_command_on_device(device=dev, command=cmd, format='xml')
                            except:
                                print("Error for command %s on %s" % (cmd, name))
                                try:
                                    print("Reconnecting to %s in %s" % (name, fname))
                                    _insert_null(name, data, data_db)
                                    reconnect_to_device(device=dev, interval=interval)
                                    print("Reconnected to %s in %s" % (name, fname))
                                    continue
                                except:
                                    print("Reconnect failed to %s in %s" % (name, fname))
                                    return
                            try:
                                rei = _strip_xml_namespace(rei)
                            except:
                                print("Error stripping namespace on %s command %s in %s" % (name, cmd, fname))
                                continue
                            if rei is None:
                                print("No response for command %s on %s" % (cmd, name))
                                continue
                            result = rei.findtext(xpath)
                            if result is None:
                                print("No result %s for command: %s xpath: %s on %s" % (result, cmd, xpath, name))
                                continue
                            try:
                                result = float(result)
                            except ValueError:
                                print("Non numeric result %s for command: %s xpath: %s on %s" % (result, cmd, xpath,
                                                                                                 name))
                                continue
                            if "alert" in trace[tracename].keys():
                                alert = trace[tracename]['alert']
                                if alert is not None:
                                    if float(result) > (float(alert) * 0.8):
                                        percent = int(float(result) / float(alert) * 100)
                                        print("[ALERT:RE]: %s %s %s is %s%% of threshold %s on %s" % (
                                            date, xpath, result, percent, alert, name))
                            redf = pd.DataFrame([[name, cmd, xpath, result, date, graphname]],
                                                columns=['NAME', 'CMD', 'XPATH', 'DATA', 'DATETIME', 'GRAPH'])
                            try:
                                redf.to_sql('data', data_db, if_exists='append')
                            except:
                                continue
            time.sleep(interval)

        # do not create graphs if tag "NOGRAPH" is set
        nographlist = t.get_resource_list(tag='NOGRAPH')
        if resource in nographlist:
            print("Not creating graphs for resource %s..." % resource)
            return

        # read annotations into pandas dataframe
        adf = pd.read_csv(self.afn, parse_dates=['DATETIME'])

        # plot RE data
        for graph in data:
            for graphname in graph:
                if graph[graphname] is None:
                    continue
                shapes = []
                annotations = []
                tracelist = []
                for trace in graph[graphname]:
                    for tracename in trace:
                        if trace[tracename] is None:
                            continue
                        cmd = trace[tracename]['cmd']
                        xpath = trace[tracename]['xpath']
                        try:
                            if not os.stat(self.re_data_filename).st_size:
                                continue
                        except:
                            continue
                        redf = pd.read_sql_query(
                            'select * from data where graph = :graph and cmd = :cmd and xpath = :xpath and name = '
                            ':name',
                            data_db,
                            params={'graph': graphname, 'cmd': cmd, 'xpath': xpath, 'name': name})
                        if redf.empty:
                            print("No data collected for command: %s xpath: %s on %s" % (cmd, xpath, name))
                            continue
                        tracelist.append(go.Scatter(x=redf['DATETIME'], y=redf['DATA'], name=xpath))
                if not tracelist:
                    print("No traces for graph: %s" % graphname)
                    continue
                layout = dict(
                    title="RE Data Monitor - %s - %s/%s - %s" % (graphname, name, model.lower(), version),
                    showlegend=True,
                    legend=dict(orientation="h")
                )
                for row in adf.itertuples():
                    shape = dict(
                        type='line',
                        opacity=0.5,
                        x0=row.DATETIME,
                        x1=row.DATETIME,
                        yref='paper',
                        y0=0,
                        y1=1,
                        line=dict(
                            color='black',
                            dash='dash',
                        )
                    )
                    shapes.append(shape)
                    annotation = dict(
                        text=row.ANNOTATION,
                        showarrow=False,
                        textangle=-90,
                        xanchor='left',
                        opacity=0.5,
                        x=row.DATETIME,
                        yref='paper',
                        y='1',
                    )
                    annotations.append(annotation)
                layout.update(dict(shapes=shapes))
                layout.update(dict(annotations=annotations))
                fig = dict(data=tracelist, layout=layout)
                py.offline.plot(fig, filename="%s/%s.%s.re.data.html" % (hostdir, name, graphname), auto_open=False)

    def _monitor_re_unstructured_data(self, resource, interval, data, log_level):
        fname = 'RE_UNSTRUCTURED_DATA monitoring'
        # get host info
        name = t['resources'][resource]['system']['primary']['name']
        model = t['resources'][resource]['system']['primary']['model']
        sys = dict(t['resources'][resource]['system'])
        sys.pop('dh')
        if str(log_level).upper() == 'OFF':
            dev = Device(system=sys, global_logger=False, device_logger=False)
        else:
            dev = Device(system=sys)
            set_device_log_level(dev, log_level)
        version = dev.get_version()

        # initialize database
        hostdir = "%s/%s" % (self.datadir, name)
        os.makedirs(hostdir, exist_ok=True)
        unstructured_data_db = create_engine("sqlite:///%s" % self.re_unstructured_data_filename)

        def _insert_null(name, data, db):
            date = datetime.datetime.now()
            for graph in data:
                for graphname in graph:
                    if graph[graphname] is None:
                        continue
                    for trace in graph[graphname]:
                        for tracename in trace:
                            if trace[tracename] is None:
                                continue
                            if 'cmd' in trace[tracename]:
                                cmd = trace[tracename]['cmd']
                            else:
                                print("No unstructured data cmd provided...")
                                continue
                            for parameter in trace[tracename]['parameters']:
                                for parametername in parameter:
                                    if parameter[parametername] is None:
                                        continue
                                    try:
                                        if not os.stat(self.re_unstructured_data_filename).st_size:
                                            continue
                                    except:
                                        continue
                                    if 'regexp' in parameter[parametername]:
                                        regexp = parameter[parametername]['regexp']
                                    elif 'regexp' in trace[tracename]:
                                        regexp = trace[tracename]['regexp']
                                    else:
                                        print("No unstructured data regexp provided...")
                                        continue
                                    tlist = [name, cmd, regexp, None, date, graphname, tracename, parametername]
                                    df = pd.DataFrame(data=[tlist],
                                                      columns=['NAME', 'CMD', 'REGEXP', 'DATA', 'DATETIME', 'GRAPH',
                                                               'TRACE', 'PARAMETER'])
                                    df.to_sql('data', db, if_exists='append')

        # collect data
        while self.is_running:
            for graph in data:
                for graphname in graph:
                    if graph[graphname] is None:
                        continue
                    for trace in graph[graphname]:
                        for tracename in trace:
                            if trace[tracename] is None:
                                continue
                            if len(dev.current_node.controllers.keys()) > 1:
                                try:
                                    if not dev.current_node.is_node_master():
                                        set_current_controller(device=dev, controller='Master')
                                except:
                                    print("Error checking for mastership on %s in %s" % (name, fname))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, data, unstructured_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            if 'cmd' in trace[tracename]:
                                cmd = trace[tracename]['cmd']
                            else:
                                print("No unstructured data cmd provided...")
                                continue
                            if 'mode' in trace[tracename]:
                                mode = trace[tracename]['mode']
                            else:
                                mode = 'cli'
                            if mode.lower() == 'cli':
                                try:
                                    result = execute_cli_command_on_device(device=dev, command=cmd)
                                except:
                                    print("No result for command: %s on %s" % (cmd, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, data, unstructured_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            elif mode.lower() == 'shell':
                                try:
                                    result = execute_shell_command_on_device(device=dev, command=cmd)
                                except:
                                    print("No result for command: %s on %s" % (cmd, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, data, unstructured_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            elif mode.lower() == 'root':
                                try:
                                    switch_to_superuser(device=dev)
                                    result = execute_shell_command_on_device(device=dev, command=cmd)
                                except:
                                    print("No result for command: %s on %s" % (cmd, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, data, unstructured_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            else:
                                try:
                                    result = execute_vty_command_on_device(device=dev, command=cmd, destination=mode)
                                except:
                                    print("No result for command: %s on %s" % (cmd, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, data, unstructured_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            date = datetime.datetime.now()
                            if result is None:
                                print("No result for command: %s on %s" % (cmd, name))
                                continue
                            for parameter in trace[tracename]['parameters']:
                                for parametername in parameter:
                                    if parameter[parametername] is None:
                                        continue
                                    if 'group' in parameter[parametername]:
                                        group = parameter[parametername]['group']
                                    else:
                                        print("No unstructured data group provided...")
                                        continue
                                    if 'regexp' in parameter[parametername]:
                                        regexp = parameter[parametername]['regexp']
                                    elif 'regexp' in trace[tracename]:
                                        regexp = trace[tracename]['regexp']
                                    else:
                                        print("No unstructured data regexp provided...")
                                        continue
                                    search_object = re.search(regexp, result, re.M | re.S)
                                    if not search_object:
                                        print("No result for command: %s regexp: %s on %s" % (cmd, regexp, name))
                                        continue
                                    filtered_result = search_object.group(group)
                                    if not filtered_result:
                                        print("No result for command: %s regexp: %s on %s" % (cmd, regexp, name))
                                        continue
                                    try:
                                        numeric_result = float(filtered_result)
                                    except ValueError:
                                        print("Non numeric result %s for command: %s regexp: %s on %s" % (
                                            filtered_result, cmd, regexp,
                                            name))
                                        continue
                                    redf = pd.DataFrame(
                                        [[name, cmd, regexp, numeric_result, date, graphname, tracename,
                                          parametername]],
                                        columns=['NAME', 'CMD', 'REGEXP', 'DATA', 'DATETIME', 'GRAPH', 'TRACE',
                                                 'PARAMETER'])
                                    try:
                                        redf.to_sql('data', unstructured_data_db, if_exists='append')
                                    except:
                                        continue
            time.sleep(interval)

        # do not create graphs if tag "NOGRAPH" is set
        nographlist = t.get_resource_list(tag='NOGRAPH')
        if resource in nographlist:
            print("Not creating graphs for resource %s..." % resource)
            return

        # read annotations into pandas dataframe
        adf = pd.read_csv(self.afn, parse_dates=['DATETIME'])

        # plot RE data
        for graph in data:
            for graphname in graph:
                if graph[graphname] is None:
                    continue
                shapes = []
                annotations = []
                tracelist = []
                for trace in graph[graphname]:
                    for tracename in trace:
                        if trace[tracename] is None:
                            continue
                        if 'cmd' in trace[tracename]:
                            cmd = trace[tracename]['cmd']
                        else:
                            print("No unstructured data cmd provided...")
                            continue
                        for parameter in trace[tracename]['parameters']:
                            for parametername in parameter:
                                if parameter[parametername] is None:
                                    continue
                                if 'label' in parameter[parametername]:
                                    label = parameter[parametername]['label']
                                else:
                                    print("No unstructured data label provided...")
                                    continue
                                if 'regexp' in parameter[parametername]:
                                    regexp = parameter[parametername]['regexp']
                                elif 'regexp' in trace[tracename]:
                                    regexp = trace[tracename]['regexp']
                                else:
                                    print("No unstructured data regexp provided...")
                                    continue
                                try:
                                    if not os.stat(self.re_unstructured_data_filename).st_size:
                                        continue
                                except:
                                    continue
                                redf = pd.read_sql_query(
                                    'select * from data where graph = :graph and trace = trace and cmd = :cmd and regexp = :regexp and name = :name and parameter = :parameter',
                                    unstructured_data_db,
                                    params={'graph': graphname, 'trace': tracename, 'cmd': cmd, 'regexp': regexp,
                                            'name': name, 'parameter': parametername})
                                if redf.empty:
                                    print("No data collected for command: %s regexp: %s on %s" % (cmd, regexp, name))
                                    continue
                                tracelist.append(go.Scatter(x=redf['DATETIME'], y=redf['DATA'], name=label))
                if not tracelist:
                    print("No traces for graph: %s" % graphname)
                    continue
                layout = dict(
                    title="RE Unstructured Data Monitor - %s - %s/%s - %s" % (graphname, name, model.lower(), version),
                    showlegend=True,
                    legend=dict(orientation="h")
                )
                for row in adf.itertuples():
                    shape = dict(
                        type='line',
                        opacity=0.5,
                        x0=row.DATETIME,
                        x1=row.DATETIME,
                        yref='paper',
                        y0=0,
                        y1=1,
                        line=dict(
                            color='black',
                            dash='dash',
                        )
                    )
                    shapes.append(shape)
                    annotation = dict(
                        text=row.ANNOTATION,
                        showarrow=False,
                        textangle=-90,
                        xanchor='left',
                        opacity=0.5,
                        x=row.DATETIME,
                        yref='paper',
                        y='1',
                    )
                    annotations.append(annotation)
                layout.update(dict(shapes=shapes))
                layout.update(dict(annotations=annotations))
                fig = dict(data=tracelist, layout=layout)
                py.offline.plot(fig, filename="%s/%s.%s.re.unstructured.data.html" % (hostdir, name, graphname),
                                auto_open=False)

    def _monitor_custom_data(self, resource, interval, custom_data, log_level):
        fname = 'CUSTOM_DATA monitoring'
        # get host info
        name = t['resources'][resource]['system']['primary']['name']
        model = t['resources'][resource]['system']['primary']['model']
        sys = dict(t['resources'][resource]['system'])
        sys.pop('dh')
        if str(log_level).upper() == 'OFF':
            dev = Device(system=sys, global_logger=False, device_logger=False)
        else:
            dev = Device(system=sys)
            set_device_log_level(dev, log_level)
        version = dev.get_version()

        # initialize database
        hostdir = "%s/%s" % (self.datadir, name)
        os.makedirs(hostdir, exist_ok=True)
        custom_data_db = create_engine("sqlite:///%s" % self.custom_data_filename)

        def _insert_null(name, data, db):
            date = datetime.datetime.now()
            for graph in data:
                for graphname in graph:
                    if graph[graphname] is None:
                        continue
                    for trace in graph[graphname]:
                        for tracename in trace:
                            if trace[tracename] is None:
                                continue
                            for parameter in trace[tracename]['parameters']:
                                for parametername in parameter:
                                    if parameter[parametername] is None:
                                        continue
                                    try:
                                        if not os.stat(self.custom_data_filename).st_size:
                                            continue
                                    except:
                                        continue
                                    if 'command' in trace[tracename]:
                                        command = trace[tracename]['command']
                                    else:
                                        print("No command set for trace %s on %s" % (tracename, name))
                                        continue
                                    command_format = 'text'
                                    filter = ''
                                    if 'format' in trace[tracename]:
                                        command_format = trace[tracename]['format']
                                    if command_format == 'text':
                                        if 'regexp' in parameter[parametername]:
                                            regexp = parameter[parametername]['regexp']
                                            filter = regexp
                                        else:
                                            print("No regexp set for parameter %s on %s" % (parametername, name))
                                            continue
                                    elif command_format == 'xml':
                                        command = command + " | display xml"
                                        if 'xpath' in parameter[parametername]:
                                            xpath = parameter[parametername]['xpath']
                                            filter = xpath
                                        else:
                                            print("No xpath set for parameter %s on %s" % (parametername, name))
                                            continue
                                    elif command_format == 'json':
                                        command = command + " | display json"
                                        if 'jsonpath' in parameter[parametername]:
                                            jsonpath = parameter[parametername]['jsonpath']
                                            filter = jsonpath
                                        else:
                                            print("No jsonpath set for parameter %s on %s" % (parametername, name))
                                            continue
                                    tlist = [name, command, filter, None, date, graphname, tracename, parametername]
                                    df = pd.DataFrame(data=[tlist],
                                                      columns=['NAME', 'COMMAND', 'FILTER', 'DATA', 'DATETIME', 'GRAPH',
                                                               'TRACE', 'PARAMETER'])
                                    df.to_sql('data', db, if_exists='append')

        # collect data
        while self.is_running:
            for graph in custom_data:
                for graphname in graph:
                    if graph[graphname] is None:
                        continue
                    for trace in graph[graphname]:
                        for tracename in trace:
                            if trace[tracename] is None:
                                continue
                            if 'command' in trace[tracename]:
                                command = trace[tracename]['command']
                            else:
                                print("No command set for trace %s on %s" % (tracename, name))
                                continue
                            command_format = 'text'
                            if 'format' in trace[tracename]:
                                command_format = trace[tracename]['format']
                            if command_format == 'xml':
                                command = command + " | display xml"
                            elif command_format == 'json':
                                command = command + " | display json"
                            if 'node' in trace[tracename]:
                                node = trace[tracename]['node']
                                try:
                                    set_current_system_node(device=dev, system_node=node)
                                except TobyException:
                                    print("Cannot set system node to %s on %s" % (node, name))
                                    continue
                            if 'controller' in trace[tracename]:
                                controller = trace[tracename]['controller']
                                try:
                                    set_current_controller(device=dev, controller=controller)
                                except TobyException:
                                    print("Cannot set controller to %s on %s" % (controller, name))
                                    continue
                            mode = 'cli'
                            if 'mode' in trace[tracename]:
                                mode = trace[tracename]['mode']
                            if mode.lower() == 'cli':
                                try:
                                    result = execute_cli_command_on_device(device=dev, command=command)
                                except:
                                    print("No result for command: %s on %s" % (command, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, custom_data, custom_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            elif mode.lower() == 'shell':
                                try:
                                    result = execute_shell_command_on_device(device=dev, command=command)
                                except:
                                    print("No result for command: %s on %s" % (command, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, custom_data, custom_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            elif mode.lower() == 'root':
                                try:
                                    switch_to_superuser(device=dev)
                                    result = execute_shell_command_on_device(device=dev, command=command)
                                except:
                                    print("No result for command: %s on %s" % (command, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, custom_data, custom_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            else:
                                try:
                                    result = execute_vty_command_on_device(device=dev, command=command,
                                                                           destination=mode)
                                except:
                                    print("No result for command: %s on %s" % (command, name))
                                    try:
                                        print("Reconnecting to %s in %s" % (name, fname))
                                        _insert_null(name, custom_data, custom_data_db)
                                        reconnect_to_device(device=dev, interval=interval)
                                        print("Reconnected to %s in %s" % (name, fname))
                                        continue
                                    except:
                                        print("Reconnect failed to %s in %s" % (name, fname))
                                        return
                            date = datetime.datetime.now()
                            if result is None:
                                print("No result for command: %s on %s" % (command, name))
                                continue
                            for parameter in trace[tracename]['parameters']:
                                for parametername in parameter:
                                    if parameter[parametername] is None:
                                        continue
                                    if command_format == 'text':
                                        if 'group' in parameter[parametername]:
                                            group = parameter[parametername]['group']
                                        else:
                                            print("No group set for parameter %s on %s" % (parametername, name))
                                            continue
                                        if 'regexp' in parameter[parametername]:
                                            regexp = parameter[parametername]['regexp']
                                        else:
                                            print("No regexp set for parameter %s on %s" % (parametername, name))
                                            continue
                                        search_object = re.search(regexp, result, re.M | re.S)
                                        if not search_object:
                                            print("No result for command %s regexp %s on %s" % (command, regexp, name))
                                            continue
                                        filtered_result = search_object.group(group)
                                        if not filtered_result:
                                            print("No result for command %s regexp %s on %s" % (command, regexp, name))
                                            continue
                                        try:
                                            numeric_result = float(filtered_result)
                                        except ValueError:
                                            print("Non numeric result %s for command: %s regexp %s on %s" % (
                                                filtered_result, command, regexp,
                                                name))
                                            continue
                                        redf = pd.DataFrame(
                                            [[name, command, regexp, numeric_result, date, graphname, tracename,
                                              parametername]],
                                            columns=['NAME', 'COMMAND', 'FILTER', 'DATA', 'DATETIME', 'GRAPH', 'TRACE',
                                                     'PARAMETER'])
                                        try:
                                            redf.to_sql('data', custom_data_db, if_exists='append')
                                        except:
                                            continue
                                    elif command_format == 'xml':
                                        if 'xpath' in parameter[parametername]:
                                            xpath = parameter[parametername]['xpath']
                                        else:
                                            print("No xpath set for parameter %s on %s" % (parametername, name))
                                            continue
                                        try:
                                            result_object = _strip_xml_namespace(result)
                                        except:
                                            print(
                                                "Error stripping namespace on %s command %s in %s" % (
                                                    name, command, fname))
                                            continue
                                        if result_object is None:
                                            print("No response for command %s on %s" % (command, name))
                                            continue
                                        filtered_result = result_object.findtext(xpath)
                                        if not filtered_result:
                                            print("No result for command %s xpath %s on %s" % (command, xpath, name))
                                            continue
                                        try:
                                            numeric_result = float(filtered_result)
                                        except ValueError:
                                            print("Non numeric result %s for command %s xpath %s on %s" % (
                                                filtered_result, command, xpath, name))
                                            continue
                                        redf = pd.DataFrame([[name, command, xpath, numeric_result, date, graphname,
                                                              tracename, parametername]],
                                                            columns=['NAME', 'COMMAND', 'FILTER', 'DATA', 'DATETIME',
                                                                     'GRAPH', 'TRACE', 'PARAMETER'])
                                        try:
                                            redf.to_sql('data', custom_data_db, if_exists='append')
                                        except:
                                            continue
                                    elif command_format == 'json':
                                        if 'jsonpath' in parameter[parametername]:
                                            jsonpath = parameter[parametername]['jsonpath']
                                        else:
                                            print("No jsonpath set for parameter %s on %s" % (parametername, name))
                                            continue
                                        try:
                                            jsonpath_expr = parse(jsonpath)
                                        except:
                                            print("Error parsing jsonpath %s for parameter %s on %s" % (
                                                jsonpath, parametername, name))
                                            continue
                                        try:
                                            json_data = json.loads(result)
                                        except:
                                            print("Error loading JSON data for parameter %s on %s" % (
                                                parametername, name))
                                            continue
                                        try:
                                            matches = jsonpath_expr.find(json_data)
                                        except:
                                            print("Error filtering JSON data for parameter %s on %s" % (
                                                parametername, name))
                                            continue
                                        filtered_result = None if len(matches) < 1 else matches[0].value
                                        try:
                                            numeric_result = float(filtered_result)
                                        except ValueError:
                                            print("Non numeric result %s for command %s jsonpath %s on %s" % (
                                                filtered_result, command, jsonpath, name))
                                            continue
                                        redf = pd.DataFrame([[name, command, jsonpath, numeric_result, date, graphname,
                                                              tracename, parametername]],
                                                            columns=['NAME', 'COMMAND', 'FILTER', 'DATA', 'DATETIME',
                                                                     'GRAPH', 'TRACE', 'PARAMETER'])
                                        try:
                                            redf.to_sql('data', custom_data_db, if_exists='append')
                                        except:
                                            continue
            time.sleep(interval)

        # do not create graphs if tag "NOGRAPH" is set
        nographlist = t.get_resource_list(tag='NOGRAPH')
        if resource in nographlist:
            print("Not creating graphs for resource %s..." % resource)
            return

        # read annotations into pandas dataframe
        adf = pd.read_csv(self.afn, parse_dates=['DATETIME'])

        # plot data
        for graph in custom_data:
            for graphname in graph:
                if graph[graphname] is None:
                    continue
                shapes = []
                annotations = []
                tracelist = []
                for trace in graph[graphname]:
                    for tracename in trace:
                        if trace[tracename] is None:
                            continue
                        for parameter in trace[tracename]['parameters']:
                            for parametername in parameter:
                                if parameter[parametername] is None:
                                    continue
                                label = parametername
                                try:
                                    if not os.stat(self.custom_data_filename).st_size:
                                        continue
                                except:
                                    continue
                                redf = pd.read_sql_query(
                                    'select * from data where graph = :graph and trace = trace and name = :name and parameter = :parameter',
                                    custom_data_db,
                                    params={'graph': graphname, 'trace': tracename,
                                            'name': name, 'parameter': parametername})
                                if redf.empty:
                                    print("No data collected for graph %s trace %s parameter %s on %s" % (
                                        graphname, tracename, parametername, name))
                                    continue
                                tracelist.append(go.Scatter(x=redf['DATETIME'], y=redf['DATA'], name=label))
                if not tracelist:
                    print("No traces for graph: %s" % graphname)
                    continue
                layout = dict(
                    title="Custom Data Monitor - %s - %s/%s - %s" % (graphname, name, model.lower(), version),
                    showlegend=True,
                    legend=dict(orientation="h")
                )
                for row in adf.itertuples():
                    shape = dict(
                        type='line',
                        opacity=0.5,
                        x0=row.DATETIME,
                        x1=row.DATETIME,
                        yref='paper',
                        y0=0,
                        y1=1,
                        line=dict(
                            color='black',
                            dash='dash',
                        )
                    )
                    shapes.append(shape)
                    annotation = dict(
                        text=row.ANNOTATION,
                        showarrow=False,
                        textangle=-90,
                        xanchor='left',
                        opacity=0.5,
                        x=row.DATETIME,
                        yref='paper',
                        y='1',
                    )
                    annotations.append(annotation)
                layout.update(dict(shapes=shapes))
                layout.update(dict(annotations=annotations))
                fig = dict(data=tracelist, layout=layout)
                py.offline.plot(fig, filename="%s/%s.%s.html" % (hostdir, name, graphname),
                                auto_open=False)

    def _monitor_re_syslog(self, resource, interval, syslog, log_level):
        fname = 'SYSLOG monitoring'
        # do not monitor if tag "NOMONSYSLOG" is set
        nomonlist = t.get_resource_list(tag='NOMONSYSLOG')
        if resource in nomonlist:
            print("Not monitoring syslog for resource %s..." % resource)
            return

        sys = dict(t['resources'][resource]['system'])
        sys.pop('dh')
        if str(log_level).upper() == 'OFF':
            dev = Device(system=sys, global_logger=False, device_logger=False)
        else:
            dev = Device(system=sys)
            set_device_log_level(dev, log_level)
        self.syslog_alerts[resource] = []
        current_testcase_start = None
        errors = ['JTASK_SCHED_SLIP', 'jlock hog', 'WEDGE DETECTED', 'xtxn error', 'Error PPE', 'cmerror']
        if syslog is not None:
            for error in syslog:
                if error is not None:
                    errors.append(error)

        # check syslog
        while self.is_running:
            for node in dev.nodes.keys():
                set_current_system_node(device=dev, system_node=node)
                current_controller_name = dev.get_current_controller_name()
                if current_controller_name is None:
                    continue
                for controller in dev.current_node.controllers.keys():
                    set_current_controller(device=dev, controller=controller)
                    name = t['resources'][resource]['system'][node]['controllers'][controller]['hostname']
                    testcase_start = _get_testcase_starttime()
                    if not testcase_start:
                        continue
                    if testcase_start != current_testcase_start:
                        self.syslog_alerts[resource] = []
                    current_testcase_start = testcase_start
                    server_datetime = datetime.datetime.now()
                    server_datetime_utc = datetime.datetime.utcnow()
                    server_delta = server_datetime_utc - server_datetime
                    testcase_start_utc = testcase_start + server_delta
                    dateformat = "%b %d %H:%M:%S %Y"
                    datecmd = "date " + "'+%s'" % dateformat
                    try:
                        router_date = execute_shell_command_on_device(device=dev, command=datecmd)
                    except:
                        print("Error for command %s on %s" % (datecmd, name))
                        try:
                            print("Reconnecting to %s in %s" % (name, fname))
                            reconnect_to_device(device=dev, interval=interval)
                            print("Reconnected to %s in %s" % (name, fname))
                            continue
                        except:
                            print("Reconnect failed to %s in %s" % (name, fname))
                            return
                    datecmd = "date -u " + "'+%s'" % dateformat
                    try:
                        router_date_utc = execute_shell_command_on_device(device=dev, command=datecmd)
                    except:
                        print("Error for command %s on %s" % (datecmd, name))
                        continue
                    try:
                        router_datetime = datetime.datetime.strptime(router_date, dateformat)
                        router_datetime_utc = datetime.datetime.strptime(router_date_utc, dateformat)
                    except:
                        continue
                    router_delta = router_datetime_utc - router_datetime
                    syslog_start = testcase_start_utc - router_delta
                    for error in errors:
                        cmd = "show log messages | match \"%s\"" % error
                        try:
                            rei = execute_cli_command_on_device(device=dev, command=cmd)
                        except:
                            print("Error for command %s on %s" % (cmd, name))
                            continue
                        lines = rei.splitlines()
                        cmd2 = "show log messages.0.gz | match \"%s\"" % error
                        try:
                            rei2 = execute_cli_command_on_device(device=dev, command=cmd2)
                        except:
                            print("Error for command %s on %s" % (cmd2, name))
                            continue
                        lines2 = rei2.splitlines()
                        lines.extend(lines2)
                        if len(lines) > 1:
                            for line in lines:
                                if not line:
                                    continue
                                linelist = line.split()
                                if len(linelist) < 3:
                                    continue
                                year = str(syslog_start.year)
                                month = linelist[0]
                                if not str(month).isalpha():
                                    continue
                                day = linelist[1]
                                if not str(day).isdigit():
                                    continue
                                timestamp = linelist[2].split('.')[0]
                                microsecond = str(syslog_start.microsecond)
                                separator = " "
                                sequence = (year, month, day, timestamp, microsecond)
                                date_line = separator.join(sequence)
                                linedatetime = datetime.datetime.strptime(date_line, '%Y %b %d %H:%M:%S %f')
                                if linedatetime < syslog_start:
                                    continue
                                if line not in self.syslog_alerts[resource]:
                                    self.syslog_alerts[resource].append(line)
                                    print("[ALERT:RE:SYSLOG]: %s" % line)
            time.sleep(interval)

    def monitoring_engine_start_monitor(self, **kwargs):
        """
        Monitor engine will start monitoring the Devices.

        DOCUMENTATION:
            start monitoring engine for all JUNOS resources unless they are tagged "NOMON" at the
            system level creates one parallel thread per resource for RE/PFE CPU/MEM monitoring
            creates one parallel thread per resource for syslog monitoring
            creates one parallel thread per resource for RE process monitoring if processes are specified
            creates one parallel thread per resource for custom data monitoring if data is specified
            creates one parallel thread per resource for custom unstructured data monitoring if dunstructured_ata
            is specified creates an annotation file for annotations (time stamped line of descriptive
            text seen in all graphs) to be added via the primary thread.

               Example params file:

                r0 {
                   system {
                      name "tinybud";
                   }
                }
                r1 {
                   system {
                      name "patagonia";
                      # turn off monitoring for r1
                      fv-tags "NOMON";
                      }
                }

                For each resource four graphs are created:
                    RE memory
                    RE CPU
                    PFE memory
                    PFE CPU

                If infile is specified or default infile exists, one graph is created per controller per resource if resource
                processes are specifed in the file:
                    RE processes

                If infile is specified or default infile exists, one graph is created per resource if resource data is
                specifed in the file:
                    RE custom data

                If infile is specified or default infile exists, one graph is created per resource if resource unstructured_data is
                specifed in the file:
                    RE custom unstructured data

                # mode can be any of: cli/shell/root/fpc1/fpc4
                # any number of traces in any number of graphs
                # graphs and traces can have any user defined names
                # label is text to provide a description for each trace

                Alerts can be specified for RE processes and/or RE custom data.  Alerts are logged to the robot log if data
                reaches 80% of alert thresholds.

                Example infile:

                r0:
                    processes: [rpd,xmlproxyd,agentd,na-grpcd,na-mqttd,jsd,mosquitto]
                    data:
                        - graph1:
                            - trace1:
                                cmd: 'show chassis routing-engine'
                                xpath: 'route-engine[slot="0"]/memory-buffer-utilization’
                            - trace2:
                                cmd: 'show chassis fpc'
                                xpath: 'fpc[slot="0"]/memory-heap-utilization'
                                alert: ‘85'
                        - graph2:
                            - trace1:
                                cmd: 'show system memory'
                                xpath: 'system-memory-summary-information/system-memory-total'
                            - trace2:
                                cmd: 'show system statistics'
                                xpath: 'tcp/received-completely-duplicate-packet'
                    unstructured_data:
                        - mpls:
                            - trace1:
                                cmd: 'show shim jnh memory dev 0 usage mpls'
                                regexp: 'block 0.*?used\W+(\d+)'
                                mode: 'fpc0'
                                parameters:
                                    - available:
                                        group: 1
                                        label: 'fpc0-mpls-block-0-bytes-available'
                r1:
                    processes:
                        - rpd:
                            alert:
                                mem: '5555'
                                cpu: '80’
                r2:
                    processes: [rpd,chassisd,snmpd,dcd]

                syslog is monitored for the following error strings:

                errors = ['JTASK_SCHED_SLIP', 'jlock hog', 'WEDGE DETECTED', 'xtxn error', 'Error PPE', 'cmerror']

                If found, a syslog alert is written to the robot log.  The user can also specify any number of error strings
                that trigger the same behavior.  Below is an example entry in the monitor.yaml file:

                r0:
                    syslog:
                        - 'error string one'
                        - 'trigger RSI for this error'
                        - error string to check
        ARGUMENTS:
            [interval=${2}    infile=monitor.yaml    log_level=ERROR]
            :param STR infile:
                *MANDATORY* The YAML containing `fv-monitoring-engine:
            :param INT interval:
                *OPTIONAL* This will change the data collection interval from its default value of
                            5 sec to the user specified setting.
            :param STR log_level:
                *OPTIONAL* This will change the log level from its default value of ‘ERROR’
                            to the user specified setting
                            (i.e. CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET).

        ROBOT USAGE:
            Monitoring Engine Start Monitor    interval=${2}    infile=monitor.yaml    log_level=CRITICAL

        :return:None
        """
        if self.is_running:
            print("Monitoring Engine cannot be started because it is already running...")
            return
        interval = 5
        infile = 'monitor.yaml'
        log_level = 'ERROR'
        for key, value in kwargs.items():
            if key.lower() == 'interval':
                interval = int(value)
            elif key.lower() == 'infile':
                infile = str(value)
            elif key.lower() == 'log_level':
                log_level = str(value).upper()
        infile = _find_file(infile)
        print(
            'Starting Monitoring Engine with infile %s interval %s and log_level %s...' % (infile, interval, log_level))
        self.interval = interval
        self.is_running = True

        # initialize annotations data file
        logdir = get_log_dir()
        self.datadir = "%s/monitor_data" % logdir
        os.makedirs(self.datadir, exist_ok=True)
        self.afn = "%s/monitor_annotations.csv" % self.datadir
        self.afh = open(self.afn, 'w')
        aheader = 'DATETIME,ANNOTATION'
        print(aheader, file=self.afh)
        self.afh.flush()
        os.fsync(self.afh.fileno())

        # initialize RE PFE data file
        self.re_pfe_filename = "%s/re_pfe.db" % self.datadir

        # initialize RE processes data file
        self.re_processes_filename = "%s/re_processes.db" % self.datadir

        # initialize RE custom data file
        self.re_data_filename = "%s/re_data.db" % self.datadir

        # initialize RE custom unstructured data file
        self.re_unstructured_data_filename = "%s/re_unstructured_data.db" % self.datadir

        # initialize user defined data file
        self.custom_data_filename = "%s/custom_data.db" % self.datadir

        # do not monitor if tag "NOMON" is set
        nomonlist = t.get_resource_list(tag='NOMON')

        yamlinput = {}
        if os.path.isfile(infile):
            with open(infile, 'r') as fname:
                yamlinput = yaml.safe_load(fname)
        for resource in t['resources']:
            osname = t['resources'][resource]['system']['primary']['osname']
            if osname.lower() != 'junos':
                continue
            if resource in nomonlist:
                print("Not monitoring resource %s..." % resource)
                continue
            name = t['resources'][resource]['system']['primary']['name']
            model = t['resources'][resource]['system']['primary']['model']
            print("Starting Monitoring Engine for %s/%s/%s..." % (resource, name, model))
            thread = threading.Thread(target=self._monitor_re_pfe, args=(resource, interval, log_level))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            processes = {}
            data = {}
            unstructured_data = {}
            custom_data = {}
            syslog = {}
            if resource in yamlinput:
                if 'processes' in yamlinput[resource]:
                    processes = yamlinput[resource]['processes']
                if 'data' in yamlinput[resource]:
                    data = yamlinput[resource]['data']
                if 'unstructured_data' in yamlinput[resource]:
                    unstructured_data = yamlinput[resource]['unstructured_data']
                if 'custom_data' in yamlinput[resource]:
                    custom_data = yamlinput[resource]['custom_data']
                if 'syslog' in yamlinput[resource]:
                    syslog = yamlinput[resource]['syslog']
            if processes:
                thread = threading.Thread(target=self._monitor_re_processes,
                                          args=(resource, interval, processes, log_level))
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
            if data:
                thread = threading.Thread(target=self._monitor_re_data, args=(resource, interval, data, log_level))
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
            if unstructured_data:
                thread = threading.Thread(target=self._monitor_re_unstructured_data,
                                          args=(resource, interval, unstructured_data, log_level))
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
            if custom_data:
                thread = threading.Thread(target=self._monitor_custom_data,
                                          args=(resource, interval, custom_data, log_level))
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
            thread = threading.Thread(target=self._monitor_re_syslog, args=(resource, interval, syslog, log_level))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        # allow for monitoring connections to be established
        time.sleep(60)

    def monitoring_engine_annotate(self, annotation):
        """
        Monitoring engine annotate keyword in your robot file to specify annotations to be added to all graphs.

        ARGUMENTS:
            [annotation]

            :param STR annotation:
                *MANDATORY* a text string to be embedded into all graphs with a timestamp

        ROBOT USAGE:
            Monitoring Engine Annotate    annotation=Annotation String

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine Annotation cannot be added because Monitoring Engine is not running...")
            return
        date = datetime.datetime.now()
        print("Adding Monitoring Engine annotation %s at time %s" % (annotation, date))
        tlist = [date, annotation]
        tline = ','.join(map(str, tlist))
        print(tline, file=self.afh)
        self.afh.flush()
        os.fsync(self.afh.fileno())

    def monitoring_engine_stop_monitor(self):
        """
        Monitoring Engine Stop Monitor.Stop monitoring engine and create graphs

        ARGUMENTS:
            []

        ROBOT USAGE:
            Monitoring Engine Stop Monitor

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine cannot be stopped because it is not running...")
            return
        print("Stopping Monitoring Engine...")
        self.afh.close()
        self.is_running = False
        timeout = self.interval + 60
        for thread in self.threads:
            thread.join(timeout=timeout)
        self.threads = []

    def monitoring_engine_get_pfe_memory_minimum(self, resource=None, fru=None):
        """
        Get the minimum PFE memory for all FPCs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the minimum PFE memory for all FPCs on a
                            single resource in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the minimum PFE memory for a single FPC
                        on a single fru in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Pfe Memory Minimum    resource=r0   fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No PFE memory utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select min(MEM) from data where type = :type and datetime > :starttime', database,
                params={'type': 'PFE', 'starttime': starttime})
            if not dataframe.empty:
                minimum = dataframe.iloc[0]['min(MEM)']
                print("Minimum PFE memory utilization for all resources is %s%%" % minimum)
            else:
                print("No PFE memory utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select min(MEM) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'PFE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(MEM)']
                    print(
                        "Minimum PFE memory utilization for resource %s fru %s is %s%%" % (resource, fru, minimum))
                else:
                    print("No PFE memory data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select min(MEM) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'PFE', 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(MEM)']
                    print("Minimum PFE memory utilization for resource %s is %s%%" % (resource, minimum))
                else:
                    print("No PFE memory utilization data for resource %s" % resource)
                    return
        database.close()
        return minimum

    def monitoring_engine_get_pfe_memory_maximum(self, resource=None, fru=None):
        """
        Get the maximum PFE memory for all FPCs across all resources in your topology.

        ARGUMENTS:
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the maximum PFE memory for all FPCs on a single resource
                       in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the maximum PFE memory for a single FPC on a single resource
                        in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Pfe Memory Maximum

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No PFE memory utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select max(MEM) from data where type = :type and datetime > :starttime', database,
                params={'type': 'PFE', 'starttime': starttime})
            if not dataframe.empty:
                maximum = dataframe.iloc[0]['max(MEM)']
                print("Maximum PFE memory utilization for all resources is %s%%" % maximum)
            else:
                print("No PFE memory utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select max(MEM) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'PFE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(MEM)']
                    print(
                        "Maximum PFE memory utilization for resource %s fru %s is %s%%" % (resource, fru, maximum))
                else:
                    print("No PFE memory data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select max(MEM) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'PFE', 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(MEM)']
                    print("Maximum PFE memory utilization for resource %s is %s%%" % (resource, maximum))
                else:
                    print("No PFE memory utilization data for resource %s" % resource)
                    return
        database.close()
        return maximum

    def monitoring_engine_get_pfe_memory_average(self, resource=None, fru=None):
        """
        Get the average PFE memory for all FPCs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the average PFE memory for all FPCs on a single resource
                            in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the average PFE memory for a single FPC on a single
                           fru in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Pfe Memory Average    resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No PFE memory utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select avg(MEM) from data where type = :type and datetime > :starttime', database,
                params={'type': 'PFE', 'starttime': starttime})
            if not dataframe.empty:
                average = dataframe.iloc[0]['avg(MEM)']
                print("Average PFE memory utilization for all resources is %s%%" % str(round(average, 2)))
            else:
                print("No PFE memory utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select avg(MEM) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'PFE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(MEM)']
                    print(
                        "Average PFE memory utilization for resource %s fru %s is %s%%" % (
                            resource, fru, str(round(average, 2))))
                else:
                    print("No PFE memory data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select avg(MEM) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'PFE', 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(MEM)']
                    print("Average PFE memory utilization for resource %s is %s%%" % (resource, str(round(average, 2))))
                else:
                    print("No PFE memory utilization data for resource %s" % resource)
                    return
        database.close()
        return average

    def monitoring_engine_get_pfe_cpu_minimum(self, resource=None, fru=None):
        """
        Get the minimum PFE CPU for all FPCs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the minimum PFE CPU for all FPCs on a
                            single resource in your topology.Deafult is set to None
            :param STR fru:
                *OPTIONAL* Get the minimum PFE CPU for a single FPC on a single fru
                        in your topology.Deafult is set to None

        ROBOT USAGE:
            monitoring engine get pfe cpu minimum        resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No PFE CPU utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select min(CPU) from data where type = :type and datetime > :starttime', database,
                params={'type': 'PFE', 'starttime': starttime})
            if not dataframe.empty:
                minimum = dataframe.iloc[0]['min(CPU)']
                print("Minimum PFE CPU utilization for all resources is %s%%" % minimum)
            else:
                print("No PFE CPU utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select min(CPU) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'PFE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(CPU)']
                    print(
                        "Minimum PFE CPU utilization for resource %s fru %s is %s%%" % (resource, fru, minimum))
                else:
                    print("No PFE CPU data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select min(CPU) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'PFE', 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(CPU)']
                    print("Minimum PFE CPU utilization for resource %s is %s%%" % (resource, minimum))
                else:
                    print("No PFE CPU utilization data for resource %s" % resource)
                    return
        database.close()
        return minimum

    def monitoring_engine_get_pfe_cpu_maximum(self, resource=None, fru=None):
        """
        Get the maximum PFE CPU for all FPCs across all resources in your topology

        ARGUMENTS
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the maximum PFE CPU for all FPCs on a single
                            resource in your topology.Defult is set to None
            :param STR fru:
                *OPTIONAL* Get the maximum PFE CPU for a single FPC on a single
                           fru in your topology.Defult is set to None

        ROBOT USAGE
            monitoring engine get pfe cpu maximum        resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No PFE CPU utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select max(CPU) from data where type = :type and datetime > :starttime', database,
                params={'type': 'PFE', 'starttime': starttime})
            if not dataframe.empty:
                maximum = dataframe.iloc[0]['max(CPU)']
                print("Maximum PFE CPU utilization for all resources is %s%%" % maximum)
            else:
                print("No PFE CPU utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select max(CPU) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'PFE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(CPU)']
                    print(
                        "Maximum PFE CPU utilization for resource %s fru %s is %s%%" % (resource, fru, maximum))
                else:
                    print("No PFE CPU data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select max(CPU) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'PFE', 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(CPU)']
                    print("Maximum PFE CPU utilization for resource %s is %s%%" % (resource, maximum))
                else:
                    print("No PFE CPU utilization data for resource %s" % resource)
                    return
        database.close()
        return maximum

    def monitoring_engine_get_pfe_cpu_average(self, resource=None, fru=None):
        """
        Get the average PFE CPU for all FPCs across all resources in your topology

        ARGUMENTS
            [resource=None, fru=None]
            :param resource:
            *OPTIONAL* Get the average PFE CPU for all FPCs on a single resource
                       in your topology.Defult is set to None.
            :param fru:
            *OPTIONAL* Get the average PFE CPU for a single FPC on a single resource
                       in your topology.Defult is set to None.
        ROBOT USAGE
            Monitoring engine get pfe cpu average   resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No PFE CPU utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select avg(CPU) from data where type = :type and datetime > :starttime', database,
                params={'type': 'PFE', 'starttime': starttime})
            if not dataframe.empty:
                average = dataframe.iloc[0]['avg(CPU)']
                print("Average PFE CPU utilization for all resources is %s%%" % str(round(average, 2)))
            else:
                print("No PFE CPU utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select avg(CPU) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'PFE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(CPU)']
                    print(
                        "Average PFE CPU utilization for resource %s fru %s is %s%%" % (
                            resource, fru, str(round(average, 2))))
                else:
                    print("No PFE CPU data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select avg(CPU) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'PFE', 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(CPU)']
                    print("Average PFE CPU utilization for resource %s is %s%%" % (resource, str(round(average, 2))))
                else:
                    print("No PFE CPU utilization data for resource %s" % resource)
                    return
        database.close()
        return average

    def monitoring_engine_get_re_memory_minimum(self, resource=None, fru=None):
        """
        Get the minimum RE memory for all REs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the minimum RE memory for all REs on a single resource
                        in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the minimum RE memory for a single RE on a single
                      fru in your topology.Default is set to None.

        ROBOT USAGE:
            monitoring engine get re memory minimum    resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No RE memory utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select min(MEM) from data where type = :type and datetime > :starttime', database,
                params={'type': 'RE', 'starttime': starttime})
            if not dataframe.empty:
                minimum = dataframe.iloc[0]['min(MEM)']
                print("Minimum RE memory utilization for all resources is %s%%" % minimum)
            else:
                print("No RE memory utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select min(MEM) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'RE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(MEM)']
                    print(
                        "Minimum RE memory utilization for resource %s fru %s is %s%%" % (resource, fru, minimum))
                else:
                    print("No RE memory data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select min(MEM) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'RE', 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(MEM)']
                    print("Minimum RE memory utilization for resource %s is %s%%" % (resource, minimum))
                else:
                    print("No RE memory utilization data for resource %s" % resource)
                    return
        database.close()
        return minimum

    def monitoring_engine_get_re_memory_maximum(self, resource=None, fru=None):
        """
        Get the maximum RE memory for all REs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the maximum RE memory for all REs on a single
                            resource in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the maximum RE memory for a single RE on a single
                        fru in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Memory Maximum       resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No RE memory utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select max(MEM) from data where type = :type and datetime > :starttime', database,
                params={'type': 'RE', 'starttime': starttime})
            if not dataframe.empty:
                maximum = dataframe.iloc[0]['max(MEM)']
                print("Maximum RE memory utilization for all resources is %s%%" % maximum)
            else:
                print("No RE memory utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select max(MEM) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'RE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(MEM)']
                    print(
                        "Maximum RE memory utilization for resource %s fru %s is %s%%" % (resource, fru, maximum))
                else:
                    print("No RE memory data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select max(MEM) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'RE', 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(MEM)']
                    print("Maximum RE memory utilization for resource %s is %s%%" % (resource, maximum))
                else:
                    print("No RE memory utilization data for resource %s" % resource)
                    return
        database.close()
        return maximum

    def monitoring_engine_get_re_memory_average(self, resource=None, fru=None):
        """
        Get the average RE memory for all REs across all resources in your topology

        ARGUMENTS:
            [ resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the average RE memory for all REs on a single
                         resource in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the average RE memory for a single RE on a single
                            fru in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Memory Average         resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No RE memory utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select avg(MEM) from data where type = :type and datetime > :starttime', database,
                params={'type': 'RE', 'starttime': starttime})
            if not dataframe.empty:
                average = dataframe.iloc[0]['avg(MEM)']
                print("Average RE memory utilization for all resources is %s%%" % str(round(average, 2)))
            else:
                print("No RE memory utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select avg(MEM) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'RE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(MEM)']
                    print(
                        "Average RE memory utilization for resource %s fru %s is %s%%" % (
                            resource, fru, str(round(average, 2))))
                else:
                    print("No RE memory data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select avg(MEM) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'RE', 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(MEM)']
                    print("Average RE memory utilization for resource %s is %s%%" % (resource, str(round(average, 2))))
                else:
                    print("No RE memory utilization data for resource %s" % resource)
                    return
        database.close()
        return average

    def monitoring_engine_get_re_cpu_minimum(self, resource=None, fru=None):
        """
        Get the minimum RE CPU for all REs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
           :param STR resource:
                *OPTIONAL* Get the minimum RE CPU for all REs on a single
                            resource in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the minimum RE CPU for a single RE on a fru
                             resource in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Cpu Minimum      resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No RE CPU utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select min(CPU) from data where type = :type and datetime > :starttime', database,
                params={'type': 'RE', 'starttime': starttime})
            if not dataframe.empty:
                minimum = dataframe.iloc[0]['min(CPU)']
                print("Minimum RE CPU utilization for all resources is %s%%" % minimum)
            else:
                print("No RE CPU utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select min(CPU) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'RE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(CPU)']
                    print(
                        "Minimum RE CPU utilization for resource %s fru %s is %s%%" % (resource, fru, minimum))
                else:
                    print("No RE CPU data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select min(CPU) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'RE', 'starttime': starttime})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(CPU)']
                    print("Minimum RE CPU utilization for resource %s is %s%%" % (resource, minimum))
                else:
                    print("No RE CPU utilization data for resource %s" % resource)
                    return
        database.close()
        return minimum

    def monitoring_engine_get_re_cpu_maximum(self, resource=None, fru=None):
        """
        Get the maximum RE CPU for all REs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
            :param STR resource:
                *OPTIONAL* Get the maximum RE CPU for all REs on a single resource
                        in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the maximum RE CPU for a single RE on a single fru
                        in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Cpu Maximum     resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No RE CPU utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select max(CPU) from data where type = :type and datetime > :starttime', database,
                params={'type': 'RE', 'starttime': starttime})
            if not dataframe.empty:
                maximum = dataframe.iloc[0]['max(CPU)']
                print("Maximum RE CPU utilization for all resources is %s%%" % maximum)
            else:
                print("No RE CPU utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select max(CPU) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'RE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(CPU)']
                    print(
                        "Maximum RE CPU utilization for resource %s fru %s is %s%%" % (resource, fru, maximum))
                else:
                    print("No RE CPU data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select max(CPU) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'RE', 'starttime': starttime})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(CPU)']
                    print("Maximum RE CPU utilization for resource %s is %s%%" % (resource, maximum))
                else:
                    print("No RE CPU utilization data for resource %s" % resource)
                    return
        database.close()
        return maximum

    def monitoring_engine_get_re_cpu_average(self, resource=None, fru=None):
        """
        Get the average RE CPU for all REs across all resources in your topology

        ARGUMENTS:
            [resource=None, fru=None]
            :param resource:
                *OPTIONAL* Get the average RE CPU for all REs on a single resource
                            in your topology.Default is set to None.
            :param fru:
                *OPTIONAL* Get the average RE CPU for a single RE on a single fru
                        in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Cpu Average     resource=r1    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_pfe_filename
        if not os.path.isfile(dfn):
            print("No RE CPU utilization data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query(
                'select avg(CPU) from data where type = :type and datetime > :starttime', database,
                params={'type': 'RE', 'starttime': starttime})
            if not dataframe.empty:
                average = dataframe.iloc[0]['avg(CPU)']
                print("Average RE CPU utilization for all resources is %s%%" % str(round(average, 2)))
            else:
                print("No RE CPU utilization data")
                return
        else:
            name = t['resources'][resource]['system']['primary']['name']
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select avg(CPU) from data where host = :name and type = :type and fru = :fru and datetime > '
                    ':starttime',
                    database,
                    params={'name': name, 'type': 'RE', 'fru': fru, 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(CPU)']
                    print(
                        "Average RE CPU utilization for resource %s fru %s is %s%%" % (
                            resource, fru, str(round(average, 2))))
                else:
                    print("No RE CPU data for resource %s fru %s" % (resource, fru))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select avg(CPU) from data where host = :name and type = :type and datetime > :starttime', database,
                    params={'name': name, 'type': 'RE', 'starttime': starttime})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(CPU)']
                    print("Average RE CPU utilization for resource %s is %s%%" % (resource, str(round(average, 2))))
                else:
                    print("No RE CPU utilization data for resource %s" % resource)
                    return
        database.close()
        return average

    def monitoring_engine_get_re_process_memory_minimum(self, process, resource=None, fru=None):
        """
        Get the minimum RE process memory for a process across all REs on all resources in your topology

        ARGUMENTS:
            [process, resource=None, fru=None]

            :param STR process:
                *MANDATORY*Process name to get the minimum RE
            :param STR resource:
                *OPTIONAL* Get the minimum RE process memory for a process across all REs on a
                            single resource in your topology.Default is set to None.
            :param STR fru:
            *OPTIONAL* Get the minimum RE process memory for a process on a single RE on a
                        single fru in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Process Memory Minimum    process=rpd    resource=r0    fru=re0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_processes_filename
        if not os.path.isfile(dfn):
            print("No RE process memory data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query('select min(MEM) from data where command = :cmd and datetime > :starttime',
                                          database,
                                          params={'cmd': process, 'starttime': starttime})
            if not dataframe.empty:
                minimum = dataframe.iloc[0]['min(MEM)']
                formatted_minimum = humanfriendly.format_size(minimum)
                print("Minimum RE process memory for process %s is %s" % (process, formatted_minimum))
            else:
                print("No RE process memory data for process %s" % process)
                return
        else:
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select min(MEM) from data where command = :cmd and datetime > :starttime and resource = '
                    ':resource and controller = :fru',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource, 'fru': fru})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(MEM)']
                    if minimum is not None:
                        formatted_minimum = humanfriendly.format_size(minimum)
                        print("Minimum RE process memory for resource %s fru %s process %s is %s" % (
                            resource, fru, process, formatted_minimum))
                    else:
                        print("No RE process memory data for resource %s fru %s process %s" % (
                            resource, fru, process))
                        return
                else:
                    print("No RE process memory data for resource %s fru %s process %s" % (
                        resource, fru, process))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select min(MEM) from data where command = :cmd and datetime > :starttime and resource = :resource',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(MEM)']
                    if minimum is not None:
                        formatted_minimum = humanfriendly.format_size(minimum)
                        print("Minimum RE process memory for resource %s process %s is %s" % (
                            resource, process, formatted_minimum))
                    else:
                        print("No RE process memory data for resource %s process %s" % (resource, process))
                        return
                else:
                    print("No RE process memory data for resource %s process %s" % (resource, process))
                    return
        database.close()
        return minimum

    def monitoring_engine_get_re_process_memory_maximum(self, process, resource=None, fru=None):
        """
        Get the maximum RE process memory for a process across all REs on all resources in your topology

        ARGUMENTS:
            [process, resource=None, fru=None]
            :param STR process:
                *MANDATORY*Get the maximum RE process memory for a specified process
            :param STR resource:
                *OPTIONAL* Get the maximum RE process memory for a process across all REs on a single resource in your topology
            :param STR fru:
                *OPTIONAL* Get the maximum RE process memory for a process on a single RE on a single Fru in your topology

        ROBOT USAGE:
            Monitoring Engine Get Re Process Memory Maximum   process=rpd    resource=r0    fru=re0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_processes_filename
        if not os.path.isfile(dfn):
            print("No RE process memory data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query('select max(MEM) from data where command = :cmd and datetime > :starttime',
                                          database,
                                          params={'cmd': process, 'starttime': starttime})
            if not dataframe.empty:
                maximum = dataframe.iloc[0]['max(MEM)']
                formatted_maximum = humanfriendly.format_size(maximum)
                print("Maximum RE process memory for process %s is %s" % (process, formatted_maximum))
            else:
                print("No RE process memory data for process %s" % process)
                return
        else:
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select max(MEM) from data where command = :cmd and datetime > :starttime and resource = '
                    ':resource and controller = :fru',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource, 'fru': fru})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(MEM)']
                    if maximum is not None:
                        formatted_maximum = humanfriendly.format_size(maximum)
                        print("Maximum RE process memory for resource %s fru %s process %s is %s" % (
                            resource, fru, process, formatted_maximum))
                    else:
                        print("No RE process memory data for resource %s fru %s process %s" % (
                            resource, fru, process))
                        return
                else:
                    print("No RE process memory data for resource %s fru %s process %s" % (
                        resource, fru, process))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select max(MEM) from data where command = :cmd and datetime > :starttime and resource = :resource',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(MEM)']
                    if maximum is not None:
                        formatted_maximum = humanfriendly.format_size(maximum)
                        print("Maximum RE process memory for resource %s process %s is %s" % (
                            resource, process, formatted_maximum))
                    else:
                        print("No RE process memory data for resource %s process %s" % (resource, process))
                        return
                else:
                    print("No RE process memory data for resource %s process %s" % (resource, process))
                    return
        database.close()
        return maximum

    def monitoring_engine_get_re_process_memory_average(self, process, resource=None, fru=None):
        """
        Get the average RE process memory for a process across all REs on all resources in your topology

        ARGUMENTS:
            [process, resource=None, fru=None]
            :param STR process:
                *MANDATORY*Get the average RE process memory for a process.

            :param STR resource:
                *OPTIONAL* Get the average RE process memory for a process across
                            all REs on a single resource in your topology
                            Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the average RE process memory for a process on a single
                             RE on a single fur in your topology. Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Process Memory Average   process=rpd    resource=r0    fru=re0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_processes_filename
        if not os.path.isfile(dfn):
            print("No RE process memory data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query('select avg(MEM) from data where command = :cmd and datetime > :starttime',
                                          database,
                                          params={'cmd': process, 'starttime': starttime})
            if not dataframe.empty:
                average = dataframe.iloc[0]['avg(MEM)']
                formatted_average = humanfriendly.format_size(average)
                print("Average RE process memory for process %s is %s" % (process, formatted_average))
            else:
                print("No RE process memory data for process %s" % process)
                return
        else:
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select avg(MEM) from data where command = :cmd and datetime > :starttime and resource = '
                    ':resource and controller = :fru',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource, 'fru': fru})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(MEM)']
                    if average is not None:
                        formatted_average = humanfriendly.format_size(average)
                        print("Average RE process memory for resource %s fru %s process %s is %s" % (
                            resource, fru, process, formatted_average))
                    else:
                        print("No RE process memory data for resource %s fru %s process %s" % (
                            resource, fru, process))
                        return
                else:
                    print("No RE process memory data for resource %s fru %s process %s" % (
                        resource, fru, process))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select avg(MEM) from data where command = :cmd and datetime > :starttime and resource = :resource',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(MEM)']
                    if average is not None:
                        formatted_average = humanfriendly.format_size(average)
                        print("Average RE process memory for resource %s process %s is %s" % (
                            resource, process, formatted_average))
                    else:
                        print("No RE process memory data for resource %s process %s" % (resource, process))
                        return
                else:
                    print("No RE process memory data for resource %s process %s" % (resource, process))
                    return
        database.close()
        return average

    def monitoring_engine_get_re_process_cpu_minimum(self, process, resource=None, fru=None):
        """
        Get the minimum RE process CPU for a process across all REs on all resources in your topology

        ARGUMENTS:
            [ process, resource=None, fru=None]
            :param process:
                *MANDATORY*Get the minimum RE process CPU for a specified process.
            :param resource:
                *OPTIONAL* Get the minimum RE process CPU for a process across
                            all REs on a single resource in your topology.
                            Default is set to None.
            :param fru:
                *OPTIONAL* Get the minimum RE process CPU for a process on a single RE
                            on a single fru in your topology.Default is set to None.
        ROBOT USAGE:
            Monitoring Engine Get Re Process Memory Maximum    process=rpd    resource=${rtr}    fru=fpc0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_processes_filename
        if not os.path.isfile(dfn):
            print("No RE process CPU data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query('select min(CPU) from data where command = :cmd and datetime > :starttime',
                                          database,
                                          params={'cmd': process, 'starttime': starttime})
            if not dataframe.empty:
                minimum = dataframe.iloc[0]['min(CPU)']
                print("Minimum RE process CPU for process %s is %s%%" % (process, minimum))
            else:
                print("No RE process CPU data for process %s" % process)
                return
        else:
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select min(CPU) from data where command = :cmd and datetime > :starttime and resource = '
                    ':resource and controller = :fru',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource, 'fru': fru})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(CPU)']
                    if minimum is not None:
                        print("Minimum RE process CPU for resource %s fru %s process %s is %s%%" % (
                            resource, fru, process, minimum))
                    else:
                        print("No RE process CPU data for resource %s fru %s process %s" % (
                            resource, fru, process))
                        return
                else:
                    print("No RE process CPU data for resource %s fru %s process %s" % (
                        resource, fru, process))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select min(CPU) from data where command = :cmd and datetime > :starttime and resource = :resource',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource})
                if not dataframe.empty:
                    minimum = dataframe.iloc[0]['min(CPU)']
                    if minimum is not None:
                        print("Minimum RE process CPU for resource %s process %s is %s%%" % (
                            resource, process, minimum))
                    else:
                        print("No RE process CPU data for resource %s process %s" % (resource, process))
                        return
                else:
                    print("No RE process CPU data for resource %s process %s" % (resource, process))
                    return
        database.close()
        return minimum

    def monitoring_engine_get_re_process_cpu_maximum(self, process, resource=None, fru=None):
        """
        Get the maximum RE process memory for a process across all REs on all resources in your topology

        ARGUMENTS:
            [process, resource=None, fru=None]

            :param STR process:
                *MANDATORY*Get the maximum RE process memory for a specified process
            :param STR resource:
                *OPTIONAL* Get the maximum RE process memory for a process across all REs on
                            a single resource in your topology.Default is set to None
            :param STR fru:
                *OPTIONAL* Get the maximum RE process memory for a process on a single RE on
                            a single fru in your topology.Default is set to None

        ROBOT USAGE:
            Monitoring Engine Get Re Process Cpu Maximum      process=dcd    resource=r1    fru=re0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_processes_filename
        if not os.path.isfile(dfn):
            print("No RE process CPU data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query('select max(CPU) from data where command = :cmd and datetime > :starttime',
                                          database,
                                          params={'cmd': process, 'starttime': starttime})
            if not dataframe.empty:
                maximum = dataframe.iloc[0]['max(CPU)']
                print("Maximum RE process CPU for process %s is %s%%" % (process, maximum))
            else:
                print("No RE process CPU data for process %s" % process)
                return
        else:
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select max(CPU) from data where command = :cmd and datetime > :starttime and resource = '
                    ':resource and controller = :fru',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource, 'fru': fru})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(CPU)']
                    if maximum is not None:
                        print("Maximum RE process CPU for resource %s fru %s process %s is %s%%" % (
                            resource, fru, process, maximum))
                    else:
                        print("No RE process CPU data for resource %s fru %s process %s" % (
                            resource, fru, process))
                        return
                else:
                    print("No RE process CPU data for resource %s fru %s process %s" % (
                        resource, fru, process))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select max(CPU) from data where command = :cmd and datetime > :starttime and resource = :resource',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource})
                if not dataframe.empty:
                    maximum = dataframe.iloc[0]['max(CPU)']
                    if maximum is not None:
                        print("Maximum RE process CPU for resource %s process %s is %s%%" % (
                            resource, process, maximum))
                    else:
                        print("No RE process CPU data for resource %s process %s" % (resource, process))
                        return
                else:
                    print("No RE process CPU data for resource %s process %s" % (resource, process))
                    return
        database.close()
        return maximum

    def monitoring_engine_get_re_process_cpu_average(self, process, resource=None, fru=None):
        """
        Get the average RE process CPU for a process across all REs on all resources in your topology

        ARGUMENTS:
            [process, resource=None, fru=None]
            :param STR process:
                *MANDATORY* Get the average RE specified process.
            :param STR resource:
                *OPTIONAL* Get the average RE process CPU for a process across all REs on a
                        single resource in your topology.Default is set to None.
            :param STR fru:
                *OPTIONAL* Get the average RE process CPU for a process on a single RE on a
                        single fru in your topology.Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Re Process Cpu Average      process=dcd    resource=r1    fru=re0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        dfn = self.re_processes_filename
        if not os.path.isfile(dfn):
            print("No RE process CPU data")
            return
        dbfile = "file:" + dfn + "?mode=ro"
        database = sqlite3.connect(dbfile, uri=True)
        starttime = _get_testcase_starttime()
        if resource is None:
            dataframe = pd.read_sql_query('select avg(CPU) from data where command = :cmd and datetime > :starttime',
                                          database,
                                          params={'cmd': process, 'starttime': starttime})
            if not dataframe.empty:
                average = dataframe.iloc[0]['avg(CPU)']
                print("Average RE process CPU for process %s is %s%%" % (process, str(round(average, 2))))
            else:
                print("No RE process CPU data for process %s" % process)
                return
        else:
            if fru is not None:
                dataframe = pd.read_sql_query(
                    'select avg(CPU) from data where command = :cmd and datetime > :starttime and resource = '
                    ':resource and controller = :fru',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource, 'fru': fru})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(CPU)']
                    if average is not None:
                        print("Average RE process CPU for resource %s fru %s process %s is %s%%" % (
                            resource, fru, process, str(round(average, 2))))
                    else:
                        print("No RE process CPU data for resource %s fru %s process %s" % (
                            resource, fru, process))
                        return
                else:
                    print("No RE process CPU data for resource %s fru %s process %s" % (
                        resource, fru, process))
                    return
            else:
                dataframe = pd.read_sql_query(
                    'select avg(CPU) from data where command = :cmd and datetime > :starttime and resource = :resource',
                    database,
                    params={'cmd': process, 'starttime': starttime, 'resource': resource})
                if not dataframe.empty:
                    average = dataframe.iloc[0]['avg(CPU)']
                    if average is not None:
                        print("Average RE process CPU for resource %s process %s is %s%%" % (
                            resource, process, str(round(average, 2))))
                    else:
                        print("No RE process CPU data for resource %s process %s" % (resource, process))
                        return
                else:
                    print("No RE process CPU data for resource %s process %s" % (resource, process))
                    return
        database.close()
        return average

    def monitoring_engine_get_syslog_alerts(self, resource=None):
        """
        Get the currently detected syslog alerts

        ARGUMENTS:
            [resource=None]
            :param resource:
                *OPTIONAL* Get the currently detected syslog alerts for a given resource.
                            Default is set to None.

        ROBOT USAGE:
            Monitoring Engine Get Syslog Alerts      resource=r0

        :return:None
        """
        if not self.is_running:
            print("Monitoring Engine is not running...")
            return
        syslog_data = []
        if resource is None:
            for myresource in self.syslog_alerts:
                syslog_data.extend(self.syslog_alerts[myresource])
        else:
            if resource in self.syslog_alerts:
                syslog_data = self.syslog_alerts[resource]
        for alert in syslog_data:
            print(alert)
        return syslog_data
