"""
Created on , 8/1/2017

@author: vappachan
"""

from jnpr.toby.hldcl.device import Device
import logging
from xml.etree import ElementTree
from jnpr.toby.hardware.chassis import chassis
import jxmlease
import sys
import re



def get_fpc_ccl_link(device=None,fpc=None,asic=None,pfe=None,inst=None,sc=None):
    """
        Gets FPC CCL link array
            example: get fpc ccl link  ${dut} ${fpc} ${asic} ${pfe} ${txi} ${txsc}

        :param device:
            **REQUIRED** Device handle
        :param fpc:
            **REQUIRED** FPC slot
        :param asic:
            **REQUIRED** Type of FPC asic
        :param pfe:
            **REQUIRED** PFE number
        :param inst:
            **REQUIRED** TX instance
        :param sc:
            **OPTIONAL** Sub channel

        :return: Dictionary which contains output of show ccl links of FPC
    """

    if ( (device is None) or  (fpc is None) or (asic is None) or (pfe is None) or (inst is None)):
        raise Exception("Mandatory arguements are missing ")

    error = 0
    ccl_link=[]
    fpcslot = "fpc"+str(fpc)
    pfenum = str(asic)+str(pfe)
    cmd = "show ccl link "
    cmd = cmd+pfenum
    cmd = cmd+" "
    inst="tx"+str(inst)
    cmd = cmd+inst
    
    if sc is not None:
        sc = "sc"+str(sc)
        cmd = cmd+" "
        cmd = cmd+sc
    output = device.vty(destination=fpcslot, command=cmd)
    response = output.response()

    output =[]
    output = response.split("\n")

    if sc is not None:
        link = {}
        for line in output:
            reg ="(\d+)\s+(\d+)\s+(\d+)"
            if re.search(reg,line,re.M|re.I):
                match = re.search(reg,line,re.M|re.I)
                link['fpc']    = fpc
                link['asic']   = asic
                link['pfe']    = pfe
                link['inst']    = inst
                link['sc']   = sc
                link['logical']  = match.group(1)
                link['physical'] = match.group(2)
                link['serdes']   = match.group(3)
        
        ccl_link.append(link)

    else:
        link = {}
        for line in output:
            reg ="(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"
            if re.search(reg,line,re.M|re.I):
                match = re.search(reg,line,re.M|re.I)
                index = match.group(1)
                link['fpc']    = fpc
                link['asic']   = asic
                link['pfe']    = pfe
                link['inst']    = inst
                link['sc']   = match.group(1)
                link['logical']  = match.group(2)
                link['physical'] = match.group(3)
                link['serdes']   = match.group(4)
                ccl_link.append(link)

    device.log(message="Returns:: fpc link array %s" %ccl_link, level="info")
    return ccl_link



def get_sib_ccl_link(device=None,spmb=None,sib=None,asic=None,pfe=None,inst=None,sc=None):
    """
        Get sib ccl link as a dictionary

            example: get sib ccl link ${dut} ${spmb} ${sib} ${asic} ${pfe} ${txi} ${txsc}

        :param device:
            **REQUIRED** Device handle
        :param spmb:
            **REQUIRED** spmb slot
        :param sib:
            **REQUIRED** sib slot
        :param asic:
            **REQUIRED** Type of FPC asic , say pf
        :param pfe:
            **REQUIRED** PFE number
        :param inst:
            **REQUIRED** TX instance
        :param sc:
            **OPTIONAL** Sub channel

        :return: Dictionary which contains output of show ccl links from SIB
    """

    if ( (device is None) or (spmb is None) or (sib is None) or (asic is None) or (pfe is None) or (inst is None)):
        raise Exception("Mandatory arguements are missing ")

    error = 0
    ccl_link = []
    sib_name = "sib"+str(sib)+"_"+asic+"_"+str(pfe)
    cmd = "show ccl link "
    cmd = cmd+sib_name
    cmd = cmd+" "
    inst = "tx"+str(inst)
    cmd = cmd+inst
    if sc is not None:
        sc = " sc"+str(sc)
        cmd = cmd+sc

    output = device.vty(destination=spmb, command=cmd)
    response = output.response()
    output =[]
    output = response.split("\n")

    if sc is not None:
        link = {}
        for line in output:
            reg ="(\d+)\s+(\d+)\s+(\d+)"
            if re.search(reg,line,re.M|re.I):
                match = re.search(reg,line,re.M|re.I)
                link['sib']    = sib
                link['pfe']     = pfe
                link['inst']    = inst
                link['sc']   = sc
                link['logical']  = match.group(1)
                link['physical'] = match.group(2)
                link['serdes']   = match.group(3)
        ccl_link.append(link)

    else:
        link= {}
        for line in output:
            reg ="(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"
            if re.search(reg,line,re.M|re.I):
          
                match = re.search(reg,line,re.M|re.I)
                index = int(match.group(1))
                link['sib']      = sib
                link['pfe']       = pfe
                link['inst']     = inst
                link['sc']   = match.group(1)
                link['logical']  = match.group(2)
                link['physical'] = match.group(3)
                link['serdes']   = match.group(4)
                ccl_link.append(link)

    device.log(message="Returns:: sib ccl link array %s" %ccl_link, level="info")
    return ccl_link


def get_chassis_fabric_fpc(device=None):
    """
        Get show chassis fabric fpc output in below format :( [ fpcslot => 0,pfe => ([pfenum => 0, planelink => ([ sib => 0, core => 0, plane => 0, linkstate => enable, ok]

        example: get_chassis_fabric_fpc {$dut}

        :param device:
            **REQUIRED** Device handle

        :return: Dictionary which contains output of 'show chassis fabric fpc'
    """

    if ( device is None):
        raise Exception("Mandatory arguements are missing ")

    cmd = "show chassis fabric fpcs"
    res = device.cli(command=cmd, format='xml').response()
    response = jxmlease.parse(res)['rpc-reply']['fm-qfx10-fpc-state-information']
    response = response.jdict()
    ans = []
    fabric = []
    try:
        ans = response['fm-qfx10-fpc-state-information']['fm-fpc-ln1-q']
    except:
        return fabric

    i = 0


    start =str(ans)[0]
    if (start != '['):
        ans=[ans]
 
    for fpc in ans:
        device.log(message="========== %s" %fpc, level="debug")
           
        fabric.append({})
        fabric[i]['fpcslot'] = int(fpc['fpc-slot1-q'])
        slot = fpc['fpc-slot1-q']
        fpc = fpc['fm-pfe-ln1-q']
        fabric[i]['pfe'] = [];

        for pfeL in fpc:
            device.log(message="========== %s" %pfeL, level="debug")
            pfe_slot = int(pfeL['pfe-slot1-q'])
            fabric[i]['pfe'].append({})
            fabric[i]['pfe'][pfe_slot]['pfenum'] = int(pfeL['pfe-slot1-q'])
            planeList = pfeL['fm-pfe-asic-ln-q']
            j = 0
 
            plane = {}

            fabric[i]['pfe'][pfe_slot]['planelink'] = []
            for plane in planeList:
                device.log(message="========== %s" %plane, level="debug")

                fabric[i]['pfe'][pfe_slot]['planelink'].append({})

                fabric[i]['pfe'][pfe_slot]['planelink'][j]['sib'] = int(plane['sib-slot-q'])
                fabric[i]['pfe'][pfe_slot]['planelink'][j]['fcore'] = int(plane['sib-asic-q'])
                fabric[i]['pfe'][pfe_slot]['planelink'][j]['plane'] = int(plane['sib-plane-q'])
                fabric[i]['pfe'][pfe_slot]['planelink'][j]['linkstate'] = str(plane['pfe-asic-link-state-q'])
                j=j+1
        i=i+1

    device.log(message="Returns:: show chassis fabric fpc %s" %fabric, level="info")

    return fabric


def check_chassis_fabric_fpc(device=None,fpc=None,sib=None,pfe=None,fcore=None,plane=None,pstate=None,lstate=None,linkOkCount=None):
    """
        Check if links in 'show chassis fabric fpc' links are OK
   
        example :check chassis fabric fpc   ${dut} None   None   None   None     None     None     None count : To check if all links in 'show chassis fabric fpc' are OK . 
        example :check chassis fabric fpc   ${dut} ${fpc} ${sib} ${pfe} ${fcore} ${plane} Disabled Down None : TO check status of specific link
  
        :param device:
            **REQUIRED** Device handle
        :param fpc:
            **OPTIONAL** fpc slot
        :param sib:
            **OPTIONAL** sib slot
        :param pfe:
            **OPTIONAL** PFE number
        :param fcore:
            **OPTIONAL** FCORE number of SIB
        :param plane:
            **OPTIONAL** Plane
        :param pstate:
            **OPTIONAL** Expected plane state
        :param lstate:
            **OPTIONAL** Expected link state
        :param linkOkCount:
            **OPTIONAL** No of SIB-PFE links which are in OK state

        :return: False if check fails and True if check passes
    """

    if ( device is None):
        raise Exception("Mandatory arguements are missing")

    error = 0
    count = 0
    match = 0

    if pstate is None:
         pstate      = 'Enabled'
    if lstate is None:
         lstate      = 'OK'
    
    fabric_fpc = get_chassis_fabric_fpc(device)
    fpc_online_slots = chassis.get_fru_slots(device,fru="fpc", state="Online")
    sib_online_slots = chassis.get_fru_slots(device,fru="sib", state="Online")
    for onlinefpc in fpc_online_slots:
        for fpcA in fabric_fpc:
            device.log(message="===== %s" %fpcA, level="debug")
            if (fpcA['fpcslot'] == onlinefpc):
                match = match + 1
                total_pfe = 3
                i = 0
                for pfeA in fpcA['pfe']:
                    device.log(message="========= %s" %pfeA, level="debug")
                    pfePresent = int(pfeA['pfenum'])
                  
                    l = 0
                    j = 0
                    k = 0

                    for link in pfeA['planelink']:
                        device.log(message="================ %s" %link, level="debug")
                        device.log(message="DETAIL of current iteration fpc/pfe/plane/sib/fcore==== %s %s %s %s %s" %(fpcA['fpcslot'],pfePresent,link['plane'],link['sib'],link['fcore']), level="debug")

                        line = link['linkstate']
                        if ( (fpc is not None) and (pfe is not None) and (sib is not None) and (fcore is not None) and (plane is not None) and (pstate is not None) and  (lstate is not None)):
                        
                            device.log(message="DETAIL of current iteration fpc/pfe/plane/sib/fcore actual%s %s %s %s %s" %(fpcA['fpcslot'],pfePresent,link['plane'],link['sib'],link['fcore']), level="debug")
                            device.log(message="DETAIL of current iteration fpc/pfe/plane/sib/fcore expected %s %s %s %s %s" %(fpc,pfe,plane,sib,fcore), level="debug")

                            if ( (int(fpc) == int(fpcA['fpcslot'])) and (int(pfe) == int(pfePresent)) and (int(sib) == int(link['sib'])) and (int(fcore) == int(link['fcore'])) and (int(plane) == int(link['plane'])) ):

                                if not re.search(pstate,line,re.M|re.I):
                                    device.log(message="Plane state is not same as expected====== %s %s" %(pstate,line), level="error")
                                    return False
                                if not re.search(lstate,line,re.M|re.I):
                                    device.log(message="Link state is not same as expected====== %s %s" %(lstate,line), level="error")
                                    return False
                                else:
                                    device.log(message="Link state is  same as expected====== %s %s" %(lstate,line), level="info")
                                    return True
                            
                        else: 
                            reg ="Enabled"
                            if not re.search(reg,line,re.M|re.I):
                                error= error+1
                                device.log(message="Link state error" , level="info")

                            reg ="OK"
                            if not re.search(reg,line,re.M|re.I):
                                error= error+1
                                device.log(message="Link state error" , level="info")
                            else:
                                count = count +1


                        l=l+1
                        if (l % 2):
                            k = 1
                        else:
                            k = 0
                    j=j+1
                i=i+1;



    device.log(message="Links count of OK links %s" %count, level="info")
    if linkOkCount is not None:
        if (linkOkCount == count):
            device.log(message="Returns:: show chassis fabric fpc PASS" , level="info")
            return True
        else:
            device.log(message="Returns:: show chassis fabric fpc FAILED" , level="error")
            error= error+1
            return False

    if error:
        device.log(message="Returns:: show chassis fabric fpc FAILED" , level="error")
        return False
    else:
        device.log(message="Returns:: show chassis fabric fpc PASS" , level="info")
        return True

def get_chassis_fabric_sib(device=None):
    """
        Get show chassis fabric sib output in below format.  [ {sibslot => 0, state => online,core => [ {fcore => 0, plane => 0, planestate => active, fpc => [ {fpcslot = 0, pfe => [ {linkstate =>ok, pfenum => 0},{linkstate =>ok, pfenum => 1},

        example:get_chassis_fabric_sib {$dut}

        :param device:
            **REQUIRED** Device handle

        return: Show chassis fabric SIB out in dictionary format
    """
    if ( device is None):
        raise Exception("Mandatory arguements are missing ")

    fabric= []
    cmd = "show chassis fabric sibs"
    res = device.cli(command=cmd, format='xml').response()
    response = jxmlease.parse(res)['rpc-reply']['fm-qfx10-sib-state-information']
    response = response.jdict()
    ans = []
    ans = response['fm-qfx10-sib-state-information']['fms-sib-ln1-q']


    i = 0
    for sib in ans: 
        device.log(message="=== %s" %(sib), level="debug")

        state = str(sib['sib-fms-state1-q'])
        reg ="ault|ffline"
        if re.search(reg,state,re.M|re.I):
            try:
                sib = sib['fms-asic-ln-q']
                device.log(message="=== Offline / Fault skipping", level="debug")
            except Exception as e:
                device.log(message="=== Offline / Fault skipping", level="debug")
                continue

        fabric.append({})
        fabric[i]['sibslot'] = int(sib['sib-slot-q'])
        fabric[i]['state'] = str(sib['sib-fms-state1-q'])
        sib = sib['fms-asic-ln-q']

        fabric[i]['core'] = []
        for core in sib:
            device.log(message="=== %s" %(core), level="debug")
            fabric[i]['core'].append({})
            sib_core = int(core['sib-asic-q'])
            fabric[i]['core'][sib_core]['fcore'] = int(core['sib-asic-q'])
            fabric[i]['core'][sib_core]['plane'] = int(core['sib-plane-q'])
            fabric[i]['core'][sib_core]['planestate'] = str(core['sib-fms-asic-state-q'])

            try:
                core = core['fms-asic-fpc-ln-q']
            except:
                device.log(message="=== continue", level="debug")
                continue
            j = 0
            fabric[i]['core'][sib_core]['fpc']= []

            start =str(core)[0]
            if (start != '['):
                core=[core]
            for fpc in core:
                device.log(message="=== %s" %(fpc), level="debug")
                fabric[i]['core'][sib_core]['fpc'].append({})
                fabric[i]['core'][sib_core]['fpc'][j]['fpcslot']= int(fpc['slot'])
                fpc = fpc['fms-asic-pfe-ln-q']
                k = 0
                fabric[i]['core'][sib_core]['fpc'][j]['pfe'] = []

                for pfe in fpc:
                    device.log(message="=== %s" %(pfe), level="debug")
                    fabric[i]['core'][sib_core]['fpc'][j]['pfe'].append({})
                    fabric[i]['core'][sib_core]['fpc'][j]['pfe'][k]['pfenum'] = int(pfe['pfe-slot-q'])
                    fabric[i]['core'][sib_core]['fpc'][j]['pfe'][k]['linkstate'] = str(pfe['fms-asic-pfe-link-state-q'])
                    k=k+1
                device.log(message="===fabric after fpc loop  %s" %(fabric), level="debug")
                j=j+1
        i=i+1

    device.log(message="Returns:: show chassis fabric fpc %s" %fabric, level="info")
    return fabric


def check_chassis_fabric_sib(device=None,fpc=None,sib=None,pfe=None,plane=None,fcore=None,lstate=None,linkOkCount=None):
    """
        Check if 'show chassis fabric sib' links are OK 

        example: check chassis fabric sib ${dut} None   None   None   None     None   None None     : To check if all links in 'show chassis fabric sib' are OK
        example: check chassis fabric sib ${dut} None   None   None   None     None   None ${pfeOk} : To check if all links in 'show chassis fabric sib' are OK . Expected count is ${pfeOk}
        example: check chassis fabric sib ${dut} ${fpc} ${pfe} ${sib} ${plane} ${core} Error None   : TO check status of specific link

        :param device:
            **REQUIRED** Device handle
        :param fpc:
            **OPTIONAL** fpc slot
        :param sib:
            **OPTIONAL** sib slot
        :param pfe:
            **OPTIONAL** PFE number
        :param plane:
            **OPTIONAL** SIB Plane
        :param fcore:
            **OPTIONAL** SIB Fcore
        :param lstate:
            **OPTIONAL** Expected link state
        :param linkOkCount:
            **OPTIONAL** No of SIB-PFE links which are in OK state

        :return: False if check fails and True if check passes
    """

    if ( device is None):
        raise Exception("Mandatory arguements are missing")


    error = 0
    match = 0
    count = 0
    countA = 0

    if lstate is None:
        lstate       = 'OK'

    sib_online_slots = chassis.get_fru_slots(device,fru="sib", state="Online")
    fpc_online_slots = chassis.get_fru_slots(device,fru="fpc", state="Online")
    fabric_sib = get_chassis_fabric_sib(device)
    try:
        for onlinesib in sib_online_slots:
            for sibA in fabric_sib:
                device.log(message="=== %s" %(sibA), level="debug")
                if (sibA['sibslot'] == onlinesib):
                    match = match +1
                    i = 0
                    for core in sibA['core']:
                        device.log(message="=== %s" %(core), level="debug")
                        reg ="Active"
                        line = core['planestate']
                        if not re.search(reg,line,re.M|re.I):
                           error= error+1
                           device.log(message="===link state error" , level="info")
                        else:
                            countA = countA+1
                            device.log(message="===count of Active plane %s" %(countA), level="debug")
                        try:
                            for  fpcA in core['fpc']:
                                device.log(message="=== %s" %(fpcA), level="debug")
                                j = 0
                                for pfeA in fpcA['pfe']:
                                    device.log(message="=== %s" %(pfeA), level="debug")

                                    line = pfeA['linkstate']
                                    device.log(message="==DETAIL of current iteration fpc/pfe/sib/fcore/plane %s %s %s %s %s" %(fpcA['fpcslot'],pfeA['pfenum'],sibA['sibslot'], core['fcore'] ,core['plane']), level="info")
        
                                    if ( (fpc is not None) and (pfe is not None) and (sib is not None) and (fcore is not None) and (plane is not None)  and (lstate is not None)):

                                        device.log(message="==DETAIL of current iteration fpc/pfe/sib/fcore/plane(actual) %s %s %s %s %s" %(fpcA['fpcslot'],pfeA['pfenum'],sibA['sibslot'], core['fcore'] ,core['plane']), level="info")
                                        device.log(message="==DETAIL of current iteration fpc/pfe/sib/fcore/plane(expect) %s %s %s %s %s" %( fpc,pfe,sib,fcore,plane), level="info")

                                        if ( (int(fpc) == int(fpcA['fpcslot'])) and (int(pfe) == int(pfeA['pfenum'])) and (int(sib) == int(sibA['sibslot'])) and (int(fcore) == int(core['fcore'])) and (int(plane) == int(core['plane'])) ):
                                            device.log(message="===HIT %s %s" %(lstate,line), level="debug")

                                            if not re.search(lstate,line,re.M|re.I):
                                                device.log(message="==Link state is not same as expected %s %s" %(lstate,line), level="debug")
                                                return False
                                            else:
                                                device.log(message="==Link state is same as expected %s %s" %(lstate,line), level="debug")
                                                return True
                                    else:
                                        reg ="OK"
                                        if not re.search(reg,line,re.M|re.I):
                                            error= error+1
                                            device.log(message="error link state error." , level="info")
                                        else:
                                            count = count+1
                                        device.log(message="==Count is  %s" %(count), level="info")
                                    j=j+1
                        except:
                            device.log(message="FPC is empty" , level="info")
                        i=i+1

    except Exception as e:
        error= error+1
        device.log(message="Exception occured." , level="error")
    device.log(message="==Count is  %s" %(count), level="debug")
    device.log(message="==Count is  %s" %(countA), level="debug")
    if linkOkCount is not None:
        if (linkOkCount == count):
            device.log(message="Returns:: show chassis fabric sib PASS" , level="info")
            return True
        else:
            device.log(message="== PFE links has errors. Expected Actual %s %s" %(linkOkCount,count), level="debug")
            error= error+1
            return False
    if error:
        device.log(message="Returns:: show chassis fabric sib FAILED" , level="error")
        return False
    else:
        device.log(message="Returns:: show chassis fabric sib PASS" , level="info")
        return True


def check_chas_fabric_topology(device=None,fpc=None,sib=None,pfe=None,sibpfe=None,core=None,state1=None,state2=None,linkOkCount=None):
    """
        Check if links in 'show chassis fabric topology' is OK 
 
        example: check chas fabric topology ${dut} None    None  None   None      None    None  None None    : To check if all links are OK in show chassis fabric topology
        example: check chas fabric topology ${dut} None    None  None   None      None    None  None {$count}: To check if all links are OK in show chassis fabric topology .Input is number of OK links.
        example: check chas fabric topology ${dut} ${fpc} ${sib} ${pfe} ${sibpfe} ${core} Error Down None    :To check status of exact link.
   

        :param device:
            **REQUIRED** Device handle
        :param fpc:
            **OPTIONAL** fpc slot
        :param sib:
            **OPTIONAL** sib slot
        :param pfe:
            **OPTIONAL** PFE number
        :param sibpfe:
            **OPTIONAL** sib PFE number
        :param core:
            **OPTIONAL** Core , on which we want to check link state
        :param state1:
            **OPTIONAL** State of FPC to sib link
        :param state2:
            **OPTIONAL** State of SIB to fpc link
        :param linkOkCount:
            **OPTIONAL** No of SIB-PFE links which are in OK state

        :return: False if check fails and True if check passes
    """

    if ( device is None ):
        raise Exception("Mandatory arguements are missing ")

    error = 0
    count = 0
    fpc_online_slots = chassis.get_fru_slots(device,fru="fpc", state="Online")
    sib_online_slots = chassis.get_fru_slots(device,fru="sib", state="Online")
    filter =None
    if fpc is not None:

        if (int(fpc)<10):
            filter = "FPC0"+str(fpc)
        else:
            filter = "FPC"+str(fpc)
        if pfe is not None:
            filter = filter+"FE"+str(pfe)

        device.log(message="=== filter is  %s" %(filter), level="debug")

        if sib is not None:
            filter = filter + ".*" + "->S0" + str(sib)  + "F" + str(sibpfe) +"_" + str(core)
    if state1 is None:
        state1       ='OK' 
        state2       ='OK' 

    cmd = "show chassis fabric topology"

    if filter is not None:
        cmd = "show chassis fabric topology | grep "
        cmd = cmd + filter

    response = device.cli(command=cmd).response()
    lines = []
    lines = response.split("\n")
    for line in lines:
        device.log(message="===   %s" %(line), level="debug")
        reg = "FPC([0-9]+)FE([0-9])\(([0-9]+),([0-9]+)\)->S([0-9]+)F([0-9])_0\([0-9]+,([0-9]+),([0-9]+)\)\s+(\w+)\s+S[0-9]+F[0-9]_0\([0-9]+,([0-9]+),([0-9]+)\)->FPC.+\(([0-9]+),([0-9]+)\)\s+(\w+)"
        if re.search(reg,line,re.M|re.I):
            match = re.search(reg,line,re.M|re.I)
            fpc     = int(match.group(1))
            sib     = int(match.group(5))
            state1A   = str(match.group(9))
            state2A   = str(match.group(14))
            device.log(message="=== fpc sib state  %s %s %s %s" %(fpc,sib,state1A,state2A), level="debug")
            if not re.search(state1,state1A,re.M|re.I):
                device.log(message="== ERROR . Expected state , Actual state %s %s" %(state1,state1A), level="error")
                error = error+1
            else:
                count = count +1
            if not re.search(state2,state2A,re.M|re.I):
                device.log(message="== ERROR . Expected state , Actual state %s %s" %(state2,state2A), level="error")
                error = error+1
            else:
                count = count +1
    device.log(message="===Count is   %s" %(count), level="debug")
    if linkOkCount is not None:
        if (linkOkCount == count):
            device.log(message="All pfe links are fine" , level="info")
        else:
            device.log(message="== PFE links has errors. Expected Actual %s %s" %(linkOkCount,count), level="debug")
            error= error+1

    if (error):
        device.log(message="Returns:: check chassis fabric topology, FAIL FAILED" , level="error")
        return False
    else:
        device.log(message="Returns:: check chassis fabric topology, PASS" , level="info")
        return True



def corrupt_crc_fpc_to_sib(device=None,fpc=None,asic=None,pfe=None,tx_instance=None,tx_link=None,num_frame=None,count=None):
    """
        Corrupt one FPC to SIB link

        example: corrupt crc fpc to sib  ${dut} ${fpc} ${asic} ${pfe} ${txi} ${txl} 10 10

        :param device:
            **REQUIRED** Device handle
        :param fpc:
            **REQUIRED** fpc slot
        :param asic:
            **REQUIRED** Type of chip pe/tq
        :param pfe:
            **REQUIRED** PFE number
        :param tx_instance:
            **REQUIRED** Tx instance
        :param tx_link:
            **REQUIRED** Tx link
        :param num_frame:
            **REQUIRED** number of frames to corrupt
        :param count:
            **REQUIRED** number of 500ms periods

        :return: True on success
    """

    if ( (device is None) or  (fpc is None) or (asic is None) or (pfe is None) or (tx_instance is None) or (tx_link is None) or (num_frame is None) or (count is None)):
        raise Exception("Mandatory arguements are missing ")


    chip = asic+str(pfe)
    tx_instance = "tx"+str(tx_instance)

    cmd = "bringup ccl bist corrupt frame-crc "
    space = " "
    cmd = cmd+chip+space+tx_instance+space+str(tx_link)+space+str(num_frame)+space+str(count)
    fpcslot = "fpc"+str(fpc)
    output = device.vty(destination=fpcslot, command=cmd)
    response = output.response()


    return True


def corrupt_crc_sib_to_fpc(device=None,spmb=None,sib=None,asic=None,pfe=None,tx_instance=None,tx_link=None,num_frame=None,count=None):
    """
        Corrupt one SIB to FPC  link

        example: corrupt crc sib to fpc ${dut} ${spmb} ${sib} pf ${pfe} ${txi} ${txl} 10 10
    
        :param device:
            **REQUIRED** Device handle
        :param sib:
            **REQUIRED** sib slot
        :param spmb:
            **REQUIRED** spmb slot
        :param asic:
            **REQUIRED** Type of chip pf/tq
        :param pfe:
            **REQUIRED** PFE number
        :param tx_instance:
            **REQUIRED** Tx instance
        :param tx_link:
            **REQUIRED** Tx link
        :param num_frame:
            **REQUIRED** number of frames to corrupt
        :param count:
            **REQUIRED** number of 500ms periods

        :return: True on success
    """
    if ((device is None) or (spmb is None) or (sib is None) or (asic is None) or (pfe is None) or (tx_instance is None) or (tx_link is None) or (num_frame is None) or (count is None)):
        raise Exception("Mandatory arguements are missing ")


    tx_instance = "tx"+str(tx_instance)
    sib_name = "sib"+str(sib)+"_"+asic+"_"+str(pfe)
     

    cmd = "bringup ccl bist corrupt frame-crc "
    space = " "
    cmd = cmd+sib_name+space+tx_instance+space+str(tx_link)+space+str(num_frame)+space+str(count)
    output = device.vty(destination=spmb, command=cmd)
    response = output.response()
 
    return True


def get_fpc_sib_links(device=None,fpc=None,sib=None,pfe=None,sibpfe=None,core=None,inlink=None,outlink=None,txi=None,txsc=None):
    """
        Get FPC to SIB links ( either tx sc or txi)
        example: get fpc sib links ${dut} ${fpc} ${sib} ${pfe} ${sibpfe} ${core} 1 None None 1
    

        :param device:
            **REQUIRED** Device handle
        :param fpc:
            **OPTIONAL** fpc slot
        :param sib:
            **OPTIONAL** sib slot
        :param pfe:
            **OPTIONAL** PFE number
        :param sibpfe:
            **OPTIONAL** sib PFE number
        :param core:
            **OPTIONAL** core
        :param inlink:
            **OPTIONAL** 1 if info regarding inlinks are needed
        :param outlinks:
            **OPTIONAL** 1 if info regarding outlinks are needed
        :param txi:
            **OPTIONAL** 1 if info regarding txi is needed
        :param txsc:
            **OPTIONAL** 1 if info regarding subchanel is needed

        :return: False if check fails and True if check passes
    """

    if ( device is None ):
        raise Exception("Mandatory arguements are missing ")

    error = 0
    count = 0
    filter =None
    if fpc is not None:

        if (int(fpc)<10):
            filter = "FPC0"+str(fpc)
        else:
            filter = "FPC"+str(fpc)
        if pfe is not None:
            filter = filter+"FE"+str(pfe)

        device.log(message="==filter is= %s" %(filter), level="debug")

        if sib is not None:
            filter = filter + ".*" + "->S0" + str(sib)  + "F" + str(sibpfe) +"_" + str(core)


    cmd = "show chassis fabric topology"

    if filter is not None:
        cmd = "show chassis fabric topology | grep "
        cmd = cmd + filter
    response = device.cli(command=cmd).response()
    lines = []
    lines = response.split("\n")
    for line in lines:
        device.log(message="=== %s" %(line), level="debug")
        reg = "FPC([0-9]+)FE([0-9])\(([0-9]+),([0-9]+)\)->S([0-9]+)F([0-9])_0\([0-9]+,([0-9]+),([0-9]+)\)\s+(\w+)\s+S[0-9]+F[0-9]_0\([0-9]+,([0-9]+),([0-9]+)\)->FPC.+\(([0-9]+),([0-9]+)\)\s+(\w+)"
        if re.search(reg,line,re.M|re.I):
            match = re.search(reg,line,re.M|re.I)
            fpc     = int(match.group(1))
            c1     = int(match.group(3))
            c2     = int(match.group(4))
            c3     = int(match.group(11))
            c4     = int(match.group(10))
            sib     = int(match.group(5))
            state1A   = str(match.group(9))
            state2A   = str(match.group(14))
            device.log(message="===fpc sib state fpc sib state1A ,state2A c1 c2 %s %s %s %s %s %s" %(fpc,sib,state1A,state2A,c1,c2), level="debug")
            if inlink is not None:
                if txi is not None:
                    device.log(message="==txi is  %s" %(c1), level="debug")
                    return c1
                if txsc is not None:
                    device.log(message="==tsc is  %s" %(c2), level="debug")
                    return c2
            if outlink is not None:
                if txi is not None:
                    device.log(message="==txi is  %s" %(c3), level="debug")
                    return c3
                if txsc is not None:
                    device.log(message="==tsc is  %s" %(c4), level="debug")
                    return c4
    return True


def get_fpc_fabric_connection_info(device=None,planecount=None,sib=None):
    """
        Get output of FPC to SIB connection info

        example: get fpc fabric connection info ${dut} ${planecount} None

        :param device:
            **REQUIRED** Device handle
        :param sib:
            **OPTIONAL** Number of SIBs.
        :param planecount:
            **REQUIRED** Number of planes in SIB (Per sibs how many slots are there)

        :return: List , per fpc slot , how many connections are there to Fabric.This is specific to VALE chassis.
    """

    if ( (device is None) or (planecount is None) ):
        raise Exception("Mandatory arguements are missing ")


    cmd = "show chassis fpc pic-status"
    res = device.cli(command=cmd, format='xml').response()
    response = jxmlease.parse(res)['rpc-reply']['fpc-information']
    response = response.jdict()
    ans = []
    ans = response['fpc-information']['fpc']

    pfe = {}
    c1 =0
    c2 =0 
    c3 =0 
    c4 =0
    c5 =0 
    c6 =0 
    for fpc in ans:
        device.log(message="== fpc is  %s" %(fpc), level="debug")

        slot = int(fpc['slot'])
        state = str(fpc['state'])
        reg ="ault|ffline"
        if re.search(reg,state,re.M|re.I):
            device.log(message="=Offline / Fault skipping" , level="info")
            continue

        desc = fpc['description']
        device.log(message="== lot desc %s %s" %(slot,desc), level="debug")
        pat1 = "LC1101"
        pat2 = "LC1102"
        pat3 = "FPC"
        if re.search(pat1,desc,re.M|re.I):
            device.log(message="=5 PFE FPC" , level="info")
            # no of  pfe x no of asic per sib
            pfe[slot] = int(planecount) * 6
            c1=c1+1
            c4 = int(planecount) * 6
        if re.search(pat2,desc,re.M|re.I):
            device.log(message="=3 PFE FPC" , level="info")
            # no of  pfe x no of plane
            pfe[slot] = 6
            pfe[slot] = int(planecount) * 3
            c5 = int(planecount) * 3
            c2=c2+1
        if re.search(pat3,desc,re.M|re.I):
            device.log(message="=PTX 5k Broadway" , level="info")
            #pfe[slot] = 8
            pfe[slot] = int(planecount) * 4
            c6 = int(planecount) * 4
            c3=c3+1
    if sib is None:
        sib = chassis.get_fru_slots(device,fru="sib", state="Online")
        sib = len(sib)
    device.log(message="===sib   %s" %(sib), level="debug")
    sib=int(sib)
    total= (c1* sib*c4) + (c2 * sib *c5) + (c3 * sib *c6)
    #total= (c1* sib*36) + (c2 * sib *18) + (c3 * sib *8)
    pfe['total'] = total
    device.log(message="===pfe total   %s" %(total), level="debug")
    device.log(message="===pfe array   %s" %(pfe), level="debug")
    return pfe

def check_chassis_sib(device=None,sib=None,sstate=None,lstate=None,lerror=None):
    """
        Check output of 'show chassis fabric sib'

        example: check chassis sib ${dut} ${sib} Offline Unused None
    
        :param device:
            **REQUIRED** Device handle
        :param sib:
            **OPTIONAL** SIB state
        :param sstate:
            **OPTIONAL** Fabric state
        :param lstate:
            **OPTIONAL** Fabric link state.
        :param lerror:
            **OPTIONAL** Fabric error state 

        :return: False if check fails and True if check passes
    """

    if ( (device is None)):
        raise Exception("Mandatory arguements are missing ")

    error = 0;
    cur_state = get_re_sib_state(device)

    if sstate is None:
        sstate = 'Online'
    if lstate is None:
        lstate ='Active'
    if lerror is None:
        lerror ='None'
    i=0
    for s in cur_state:
        device.log(message="==iteration   %s" %(s), level="debug")
        if sib is not None:
            if (int(s['slot']) != int(sib)):
                device.log(message="===continuing %s  %s" %(s['slot'],sib), level="debug")
                continue
        if (s['state'] == "Empty"):
            device.log(message="Empty ....." , level="info")
            continue
        if ( (s['state'] == sstate) and (s['linkstate'] == lstate) and (s['linkerror'] == lerror) ):
            device.log(message="===state is :sstate lstate lerror exp:   %s  %s %s" %(sstate,lstate,lerror), level="info")
            device.log(message="===state is :sstate lstate lerror actual %s  %s %s" %(s['state'],s['linkstate'],s['linkerror']), level="info")
        else:
            device.log(message="==ERROR:state is :sstate lstate lerror expected : %s %s %s" %(sstate,lstate,lerror), level="info")
            device.log(message="==ERROR:state is :sstate lstate lerror actual   : %s %s %s" %(s['state'],s['linkstate'],s['linkerror']), level="info")
            error=error+1
        i=i+1

    if (error):
        device.log(message="check_chassis_sib FAILED" , level="error")
        return False
    else:
        device.log(message="check_chassis_sib PASS" , level="info")
        return True

       
def get_re_sib_state(device=None): 
    """
        Get output of 'show chassis sib'

        example: get_re_sib_state ${dut}

        :param device:
            **REQUIRED** Device handle

        :return: Output of show chassis SIBs
    """

    if ( device is None):
        raise Exception("Mandatory arguements are missing ")

    cmd = "show chassis sibs"
    res = device.cli(command=cmd, format='xml').response()
    response = jxmlease.parse(res)['rpc-reply']['sib-information']
    response = response.jdict()
    ans = []
    ans = response['sib-information']['sib']
    state=[]
    i=0
    for sib in ans:
        device.log(message="==sib %s" %(sib), level="debug")
        state.append({})
        slot=sib['slot']
        state[i]['slot'] = int(sib['slot'])
        state[i]['state'] = str(sib['state'])
        state[i]['linkstate'] = str(sib['sib-link-state'])
        state[i]['linkerror'] = str(sib['sib-link-errors'])
        i=i+1
    
    device.log(message="==sib state is :   %s" %(state), level="debug")
    return state

def check_autoheal(device=None,sib=None,complete=None,skip=None):
    """
        To check if sib autoheal has worked.

        example: check autoheal ${dut} ${sib} 1 None

        :param device:
            **REQUIRED** Device handle
        :param sib:
            **REQUIRED** sib slot
        :param skip:
            **OPTIONAL** To check if autoheal has skipped
        :param complete:
            **OPTIONAL** To check if autoheal has completed

        :return: False if check fails and True if check passes
    """


    if ( (device is None) or (sib is None)):
        raise Exception("Mandatory arguements are missing ")


    if complete is not None:
        filter1 = "Completed: SIB "+str(sib)
        filter2 = "autoheal"
    if skip is not None:
        filter1 = "Denied: Sib "+str(sib)
        filter2 = "time less than user configured"

    device.log(message="==filter is %s  %s" %(filter1,filter2), level="debug")


    cmd = "show chassis fabric errors autoheal | grep \""
    cmd = cmd + filter1
    cmd = cmd + "\"| grep \""
    cmd = cmd + filter2+"\""
    cmd = cmd + " | count"

    response = device.cli(command=cmd).response()
    device.log(message="==resp is   %s" %(response), level="debug")
    reg="Count: [1-9]+ lines"

    if re.search(reg,response,re.M|re.I):
        device.log(message="check_autoheal PASS" , level="info")
        return True
    else:
        device.log(message="check_autoheal FAILED" , level="error")
        return False
