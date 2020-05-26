#!/usr/bin/env python3
"""
Copyright (C) 2015-2016, Juniper Networks, Inc.
All rights reserved.
Author: Michael Zhou
Description: BPS in Toby
"""

import time
import logging
import os

#import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

logging.basicConfig(level="INFO")


def bps_load_test(bph, **kwargs):
    """
    Load a test on BPS, the test can be uploaded or existing saved test on BPS chassis

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param bpt_file:
        *OPTIONAL* an exported bpt file from BPS, it will be uploaded to BPS chassis
    :param test_name:
        *OPTIONAL* an existing saved test on BPS

    Returns: test_name if succeed, Exception if fail

    """
    bpt_file = kwargs.get("bpt_file", None)
    test_name = kwargs.get("test_name", None)

    # showing current port reservation state
    bph.invoke('portsState')

    # the bpt_file name has the format of "test_name" + ".bpt"
    if bpt_file:
        bpt_file = os.path.abspath(bpt_file)
        if os.path.isfile(bpt_file):
            bph.invoke('uploadBPT', filePath=bpt_file, force=True)
            test_name = os.path.basename(bpt_file).split(".")[0]
        else:
            raise Exception("The bpt file doesn't exist: " + str(bpt_file))

    if bph.invoke('setNormalTest', test_name=test_name):
        return test_name
    else:
        raise Exception("Cannot load bps test: " + str(test_name))

def bps_start_test(bph, test_name, group):
    """
    start to run the current test on BPS

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param test_name:
        *MANDATORY* the current test on BPS
    :param group:
        *MANDATORY* the group to be used

    Returns: runid if succeed, Exception if fail

    """
    # please note the runid generated. It will be used for many more functionalities
    runid = bph.invoke('runTest', modelname=test_name, group=group)
    if runid != -1:
        return runid
    else:
        raise Exception("Cannot start bps test: " + str(test_name))

def bps_stop_test(bph, runid):
    """
    stop the running test on BPS

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param runid:
        *MANDATORY* the runid of current running test

    Returns:
    """
  
    bph.invoke('stopTest',testid=runid)
    #bph.invoke('logout')

def bps_get_statistics(bph, runid, duration=10, stats_group="summary"):
    """
    Get real time statistics when test is running

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param runid:
        *MANDATORY* runid of the running test
    :param duration:
        *OPTIONAL* get statistics for this duration, default time is 10 seconds
    :param stats_group:
        *OPTIONAL* specify the statsGroup, see below for mapping
        RTS Group shown in GUI      statsGroup parameter
        Summary                     summary
        Interface                   iface
        TCP                         l4stats
        SSL/TLS                     sslStats
        IPsec                       ipsecStats
        Application                 l7Stats
        Client                      clientStats
        Attacks                     attackStats
        GTP                         gtp
        Resources                   resource

    Returns:

    """
    # showing progress and current statistics
    progress = 0
    timer = 0
    interval = 2
    # by default, the number passed from robot is taken as string but not number
    duration = int(duration)
    while timer < duration and progress < 100:
        progress = bph.invoke('getRTS',runid=runid, statsGroup=stats_group)
        time.sleep(interval)
        timer += interval

def bps_get_result(bph, runid):
    """
    get the result of test

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param runid:
        *MANDATORY* the runid of current running test

    Returns:
    """
    return bph.invoke('getTestResult',runid=runid)

def bps_get_report(bph, runid, location, report_name):
    """
    get the report of test

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param runid:
        *MANDATORY* the runid of current running test
    :param location:
        *MANDATORY* the directory to save report
    :param report_name:
        *MANDATORY* the report name of test

    Returns:
    """
    bph.invoke('exportTestReport',testId=runid, reportName=report_name, location=location)

def bps_get_tests_summary(bph, location, csv_name):
    """
    get a csv file contaning a short summary of all the tests that have been run on the chassis

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param location:
        *MANDATORY* the directory to save csv file
    :param csv_name:
        *MANDATORY* the csv file name
    """
    bph.invoke('exportTestsCsv',csvName=csv_name, location=location)

def bps_get_running_test(bph):
    """
    get running test info

    :param bph:
        *MANDATORY* the session connecting to BPS chassis

    Returns: a list which includes running test info if there is test running, 
            blank list [] if there is no test running, False if cannot get running info
    """
    return bph.invoke('runningTestInfo')

def bps_get_components(bph, test_name):
    """
    get the component list for the specified test

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param test_name:
        *MANDATORY* the name of saved test
    """
    bph.invoke('compName',modelName=test_name, enableRequestPrints=False)

def bps_modify_test(bph, **kwargs):
    """Modify and save test on BPS, 3 steps are needed as below

    1. Before modifying a saved test, the test has to be set as the current working model.
    2. Then parameter values that need to be changed must be modified.
    3. Finally, the modified test must be saved before execution.

    :param bph:
        *MANDATORY* the session to BPS chassis
    :param test_name:
        *MANDATORY* the name of saved test
    :param params:
        *MANDATORY* the parameter of modificaion items, it's a nested list with below format
    :param save_as:
        *OPTIONAL* the new name of test to be saved

    Returns: runid if succeed, otherwise False

    Example::

        # params need follow the below format
        params = [
            [componentId, elementId, value],
            [componentId, elementId, paramId, value], # if the element has the params within
            ...
        ]

    """
    test_name = kwargs.get("test_name")
    params = kwargs.get("params")
    save_as = kwargs.get("save_as", None)

    # setting the current working model
    bph.invoke('setNormalTest',test_name=test_name)
    bph.invoke('viewNormalTest')

    for arg in params:
        if len(arg) == 3:
            component_id = arg[0]
            element_id = arg[1]
            value = arg[2]
            bph.invoke('modifyNormalTest',componentId=component_id, elementId=element_id, Value=value)
        elif len(arg) == 4:
            component_id = arg[0]
            element_id = arg[1]
            param_id = arg[2]
            value = arg[3]
            bph.invoke('modifyNormalTest2',componentId=component_id, elementId=element_id, paramId=param_id, Value=value)

    if save_as is not None:
        bph.invoke('saveNormalTest',name=save_as, force=True)
    else:
        bph.invoke('saveNormalTest')


def bps_modify_network_neighborhood(bph, **kwargs):
    """Modify and save network neighborhood on BPS, 3 steps are needed as below
    1. Retrieve the network neighborhood
    2. Modify the desired element
    3. Save the neighborhood

    :param bph:
        *MANDATORY* the session to BPS chassis
    :param neighborhood_name:
        *MANDATORY* the name of network neighborhood
    :param params:
        *MANDATORY* the parameter of modificaion items, it's a nested list with below format
    :param save_as:
        *OPTIONAL* the new name of test to be saved

    Returns: runid if succeed, otherwise False

    Example::

        params = [
            [componentId, elementId, value],
            [componentId, elementId, value],
            ...
        ]
        # Given a smaple neighborhood as below.
        "ip4Router" : {
            "id:services-1-vr4" : "[id:services-1-vr4, ip_address:115.115.0.1, netmask:8, gateway_ip_address:115.0.0.10, default_container:services-1]",
            "id:mobiles-1-vr4" : "[id:mobiles-1-vr4, ip_address:116.116.0.1, netmask:8, gateway_ip_address:116.0.0.10, default_container:mobiles-1]",
        }
        # Assume you want to modify the ip_address of services-1-vr4 and mobiles-1-vr4, use the params as this.
        params = [
            ["services-1-vr4", "ip_address", "115.115.0.2"],
            ["mobiles-1-vr4", "ip_address", "116.116.0.2"],
        ]

    """
    neighborhood_name = kwargs.get("neighborhood_name")
    params = kwargs.get("params")
    save_as = kwargs.get("save_as", None)

    # retrieving the neighborhood
    bph.invoke('retrieveNetwork',NN_name=neighborhood_name)
    bph.invoke('viewNetwork')

    for arg in params:
        if len(arg) == 3:
            component_id = arg[0]
            element_id = arg[1]
            value = arg[2]
            bph.invoke('modifyNetwork',componentId=component_id, elementId=element_id, Value=value)

    if save_as is not None:
        bph.invoke('saveNetwork',name=save_as, force=True)
    else:
        bph.invoke('saveNetwork')

## wrapper to start bps traffic in one keyword
def bps_start_traffic(bph, **kwargs):
    """
    load bpt file and send traffic

    :param bph:
        **MANDATORY** the session connecting to BPS chassis
    :param bpt_file:
        **MANDATORY** an exported bpt file from BPS, it will be uploaded to BPS chassis
    :param group:
        **OPTIONAL** the group number when running bps traffic
    :param params:
        **OPTIONAL** the params which used to modify bpt file

    Returns: runid if succeed, otherwise False

    """
    bpt_file = kwargs.get("bpt_file", None)
    group = kwargs.get("group", 1)
    params = kwargs.get("params", None)

    test_name = bps_load_test(bph, bpt_file=bpt_file)
    if params is not None:
        params_list = []
        for key, value in params.items():
            if value == "enable":
                params_list.append([key, "active", "true"])
            elif value == "disable":
                params_list.append([key, "active", "false"])
        bps_modify_test(bph, test_name=test_name, params=params_list)
    runid = bps_start_test(bph, test_name=test_name, group=group)
    return runid

def bps_stop_traffic(bph, runid):
    """
    stop the running test on BPS

    :param bph:
        *MANDATORY* the session connecting to BPS chassis
    :param runid:
        *MANDATORY* the runid of current running test

    Returns:
    """
    bps_stop_test(bph, runid)




