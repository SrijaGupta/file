'''
   Python test script to interface with Calnex Paragon-X
'''

from __future__ import print_function

def configure_operating_mode(rth, **kwargs):
    '''
    Configure Operating Mode
    '''
    master_slave_emulation = list(kwargs.values())
    operating_mode = master_slave_emulation[0]
    if operating_mode == "PTP":
#        rth.invoke('paragonset', 'OperatingMode', 'ptp')
        rth.invoke('paragonset', "OperatingMode", "ptp")
        rth.invoke('paragonset', "MasterSlave Enabled", "TRUE")
    elif operating_mode == "SYNCE":
        rth.invoke('paragonset', "OperatingMode", "SYNCE")

def setup_port1_as_rj45_port2_as_rj45(rth):
    '''
    Setup Interface port1 as RJ45 and port2 as RJ45
    '''
    rth.invoke('paragonset', "TxRxMode", "TRUE")
    rth.invoke('paragonset', "Physical RefClkSource", "EXT_10M")
    rth.invoke('paragonset', "Physical Coupled", "TRUE")
    rth.invoke('paragonset', "Physical LineRate", "1GBE")
    rth.invoke('paragonset', "Physical LineInterface", "ELECTRICAL")
    rth.invoke('paragonset', "Physical EthAutonegotiate", "TRUE")

def setup_port1_as_sfp_port2_as_sfp(rth):
    '''
    Setup Interface port1 as SFP and port2 as SFP
    '''
    rth.invoke('paragonset', "TxRxMode", "TRUE")
    rth.invoke('paragonset', "Physical RefClkSource", "EXT_10M")
    rth.invoke('paragonset', "Physical Coupled", "TRUE")
    rth.invoke('paragonset', "Physical LineRate", "1GBE")
    rth.invoke('paragonset', "Physical LineInterface", "OPTICAL")
    rth.invoke('paragonset', "Physical EthAutonegotiate", "TRUE")
    rth.invoke('paragonset', "Physical AuxInputThreshold", "1.1")

def setup_port1_as_sfpp_port2_as_sfpp(rth):
    '''
    Setup port1 as SFPP and port2 as SFPP
    '''
    rth.invoke('paragonset', "TxRxMode", "TRUE")
    rth.invoke('paragonset', "Physical RefClkSource", "EXT_10M")
    rth.invoke('paragonset', "Physical Coupled", "TRUE")
    rth.invoke('paragonset', "Physical LineRate", "10GBE")
    rth.invoke('paragonset', "Physical xFPSelect", "SFPPLUS")
    rth.invoke('paragonset', "Physical AuxInputThreshold", "1.1")

def setup_port1_as_xfp_port2_as_xfp(rth):
    '''
    Setup port1 as XFP and port2 as XFP
    '''
    rth.invoke('paragonset', "TxRxMode", "TRUE")
    rth.invoke('paragonset', "Physical RefClkSource", "EXT_10M")
    rth.invoke('paragonset', "Physical Coupled", "TRUE")
    rth.invoke('paragonset', "Physical LineRate", "10GBE")
    rth.invoke('paragonset', "Physical xFPSelect", "XFP")

def configure_boundary_clock_ipv4(rth):
    '''
    Configure Boundary clock ipv4
    '''
    rth.invoke('paragonset', "MasterSlave DeviceConfiguration", "MASTERANDSLAVE")
    rth.invoke('paragonset', "MasterSlave Master #0 Encapsulation", "IPV4")
    rth.invoke('paragonset', "MasterSlave Master #0 IpAddress", "1.1.1.2")
    rth.invoke('paragonset', "MasterSlave Master #0 Mode", "AUTO")
    rth.invoke('paragonset', "MasterSlave Master #0 UnicastEnabled", "TRUE")
    rth.invoke('paragonset', "MasterSlave Master #0 MulticastEnabled", "FALSE")
    rth.invoke('paragonset', "MasterSlave Slave Encapsulation", "IPV4")
    rth.invoke('paragonset', "MasterSlave Slave IpAddress", "2.2.2.2")
    rth.invoke('paragonset', "MasterSlave Slave Mode", "AUTO")
    rth.invoke('paragonset', "MasterSlave Slave UnicastAnnounce", "TRUE")
    rth.invoke('paragonset', "MasterSlave Slave UnicastSync", "TRUE")
    rth.invoke('paragonset', "MasterSlave Slave UnicastDelResp", "TRUE")
    rth.invoke('paragonset', "MasterSlave Slave MasterIpAddress", "2.2.2.1")
    rth.invoke('paragonset', "MasterSlave Slave MasterMACAddress", "08 b2 58 e2 d3 8c")
    rth.invoke('paragonset', "MasterSlave Master #0 Enabled", "TRUE")

def configure_boundary_clock_ipv4_g82751_enh(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "MasterSlave DeviceConfiguration", "MASTERANDSLAVE")
    rth.invoke('paragonset', "MasterSlave Master #0 Encapsulation", "IPV4")
    rth.invoke('paragonset', "MasterSlave Master #0 IpAddress", "1.1.1.2")
#    rth.invoke('paragonset', "MasterSlave Master #0 Mode", "FORCED")
    rth.invoke('paragonset', "MasterSlave Master #0 UnicastEnabled", "TRUE")
    rth.invoke('paragonset', "MasterSlave Master #0 MulticastEnabled", "FALSE")
    rth.invoke('paragonset', "MasterSlave Master #0 Mode", "FORCED")
    rth.invoke('paragonset', "MasterSlave Master #0 AllowedSlave #0 IpAddress", "1.1.1.1")
#    rth.invoke('paragonset', "MasterSlave Master #0 AllowedSlave #0 MACAddress", "08 b2 58 e2 d3 8b")
    rth.invoke('paragonset', "MasterSlave Master #0 AllowedSlave #0 MACAddress", "08 b2 58 e2 d3 6f")
    rth.invoke('paragonset', "MasterSlave Master #0 DomainNumber", "24")
    rth.invoke('paragonset', "MasterSlave Master #0 AllowedSlave #0 AnnounceRate", "1")
    rth.invoke('paragonset', "MasterSlave Master #0 AllowedSlave #0 SyncRate", "64")
    rth.invoke('paragonset', "MasterSlave Slave Encapsulation", "IPV4")
    rth.invoke('paragonset', "MasterSlave Slave IpAddress", "2.2.2.2")
    rth.invoke('paragonset', "MasterSlave Slave Mode", "FORCED")
    rth.invoke('paragonset', "MasterSlave Slave UnicastAnnounce", "TRUE")
    rth.invoke('paragonset', "MasterSlave Slave UnicastSync", "TRUE")
    rth.invoke('paragonset', "MasterSlave Slave UnicastDelResp", "TRUE")
    rth.invoke('paragonset', "MasterSlave Slave MasterIpAddress", "2.2.2.1")
    rth.invoke('paragonset', "MasterSlave Slave MasterMACAddress", "08 b2 58 e2 d3 70")
#    rth.invoke('paragonset', "MasterSlave Slave MasterMACAddress", "08 b2 58 e2 d3 8c")
#    rth.invoke('paragonset', "MasterSlave Master #0 Enabled", "TRUE")
    rth.invoke('paragonset', "MasterSlave Slave DelRespMsgRate", "64")
    rth.invoke('paragonset', "MasterSlave Slave DomainNumber", "24")
    rth.invoke('paragonset', "MasterSlave Master #0 Enabled", "TRUE")

def configure_boundary_clock_ethernet(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "MasterSlave DeviceConfiguration", "MASTERANDSLAVE")
    rth.invoke('paragonset', "MasterSlave StandardsProfile", "G.8275.1_PHASE_PROFILE")
#    rth.invoke('paragonset', "MasterSlave Master #0 Enabled", "TRUE")

def configure_capture(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "Capture Ptp IncludeCorrectionField", "TRUE")
    rth.invoke('paragonset', "Capture SyncE MeasurementPort", "PORT2")
    rth.invoke('paragonset', "Capture OnePps AccuracyLimit", "0.050")

def paragon_disconnect(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "Rst", "TRUE")
    rth.invoke('disconnect')

def paragon_performance_measurements(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "SimulMeasImpairMode", "MEASUREANDIMPAIR")
    rth.invoke('paragonset', "Capture SyncE WanderCaptEnable", "TRUE")
    rth.invoke('paragonset', "Capture OnePps AccuracyCaptEnable", "TRUE")

def paragon_start_esmc_generation_port1(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "PacketGeneration #0 Esmc #0 SsmType", "QL-PRC")
    rth.invoke('paragonset', "PacketGeneration #0 Enable", "TRUE")

def paragon_stop_esmc_generation_port1(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "PacketGeneration #0 Enable", "FALSE")

def paragon_stop_master_slave_emulation(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "MasterSlave Master #0 Enabled", "FALSE")

def detect_1pps(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    detect1pps = rth.invoke('paragonget', "InstrumentStatus Interface 1ppsMeasLock Detected")
    print("Detect1pps: %s" %detect1pps)
    detect1pps_1 = detect1pps.rstrip()
    print(type(detect1pps))
    if detect1pps_1 == 'TRUE':
        print("1pps signal is detected")
        return 1
    else:
        print("1pps signal is not detected")
        return 0

def paragon_start_timing_capture(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('starttimingcapture')
#    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSet", "TRUE")

def paragon_stop_timing_capture(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('stopcapture')
    rth.invoke('exportdata', "C:/Users/Calnex/Calnex_Automation/Captures/g82732_performance_3.clxz")

def paragon_set_packet_measurements(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "MasterSlave Capture", "PORT2")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureClear", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSync", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureDelReq", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureDelResp", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureAnnounce", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSlaveIP", "2.2.2.2")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureFollowUp", "FALSE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSet", "TRUE")

def paragon_set_packet_measurements_ethernet(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "MasterSlave Capture", "PORT2")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureClear", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSlaveMAC", "d0 00 00 00 00 01")
#    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSync", "TRUE")
#    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureDelReq", "TRUE")
#    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureDelResp", "TRUE")
#    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSlaveMAC", "d0 00 00 00 00 01")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureMulticastAnnounce", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureMulticastSync", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureMulticastDelay", "TRUE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureMulticastAllSlaves", "FALSE")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureMulticastSlavePortId", "00 00 00 00 00 00 00 02 00 01")
    rth.invoke('paragonset', "MasterSlave FlowFilter CaptureSet", "TRUE")
    rth.invoke('paragonset', "MasterSlave Master #0 Enabled", "TRUE")

def paragon_get_packet_measurements(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "Cat Show", "TRUE")
    rth.invoke('paragonset', "Cat", "1588TimeError")
    rth.invoke('paragonset', "Cat SelectSlot ", "2Way")
    rth.invoke('paragonset', "Cat DTEMTIE Mask ", "G.8273.2 dTE Gen Const Temp")
    rth.invoke('paragonset', "Cat DTETDEV Mask ", "G.8273.2 dTE Gen Const Temp")
    rth.invoke('paragonset', "Cat DTE ThresholdLimit", "0.04")
    rth.invoke('paragonset', "Cat DTEHF ThresholdLimit", "0.07")
    rth.invoke('paragonset', "Cat AVERAGEDTE AveragingPeriod", "1000")

    rth.invoke('paragonset', "Cat SelectSlot ", "Sync")
    t1_te_min = rth.invoke('paragonget', "Cat TIMEERROR Min")
    t1_te_max = rth.invoke('paragonget', "Cat TIMEERROR Max")
    rth.invoke('paragonset', "Cat SelectSlot ", "Delay Req")
    t4_te_min = rth.invoke('paragonget', "Cat TIMEERROR Min")
    t4_te_max = rth.invoke('paragonget', "Cat TIMEERROR Max")

    print("T1 TimeError Min : " + t1_te_min)
    print("T1 TimeError Max : " + t1_te_max)
    print("T4 TimeError Min : " + t4_te_min)
    print("T4 TimeError Max : " + t4_te_max)

    rth.invoke('paragonset', "Cat SelectSlot 2Way")
    rth.invoke('paragonset', "Cat Calculate", "1")
    rth.invoke('waitforcat')

    te_min = rth.invoke('paragonget', "Cat TIMEERROR Min")
    te_max = rth.invoke('paragonget', "Cat TIMEERROR Max")
    te_mean = rth.invoke('paragonget', "Cat TIMEERROR Mean")

    print("2Way TimeError Minimum : " + te_min)
    print("2Way TimeError Maximum : " + te_max)
#    print("2Way TimeError Mean : "+ TE_mean)

    cte = rth.invoke('paragonget', "Cat AVERAGEDTE cTe")
    print("Constant Time Error,cTE: " + cte)

    cte_min = rth.invoke('paragonget', "Cat AVERAGEDTE MIN")
    print("Constant Time Error (cTE) Minimum : " + cte_min)
    cte_max = rth.invoke('paragonget', "Cat AVERAGEDTE MAX")
    print("Constant Time Error (cTE) Maximum : " + cte_max)

    mtie_result = rth.invoke('paragonget', "Cat DTEMTIE MaskResult")
    print("MTIE_Result:" + mtie_result)
    tdev_result = rth.invoke('paragonget', "Cat DTETDEV MaskResult")
    print("TDEV_Result:" + tdev_result)

#    rth.invoke('paragonset', "Cat SelectSlot 2Way")
    dtelf_min = rth.invoke('paragonget', "Cat DTELF Min")
    dtelf_max = rth.invoke('paragonget', "Cat DTELF Max")
    dtehf_min = rth.invoke('paragonget', "Cat DTEHF Min")
    dtehf_max = rth.invoke('paragonget', "Cat DTEHF Max")
    dtemtie_min = rth.invoke('paragonget', "Cat DTEMTIE Min")
    dtemtie_max = rth.invoke('paragonget', "Cat DTEMTIE Max")
    dtetdev_min = rth.invoke('paragonget', "Cat DTETDEV Min")
    dtetdev_max = rth.invoke('paragonget', "Cat DTETDEV Max")

    print("2Way Dynamic TE LF Minimum : " + dtelf_min)
    print("2Way Dynamic TE LF Maximum : " + dtelf_max)
    print("2Way Dynamic TE HF Minimum : " + dtehf_min)
    print("2Way Dynamic TE HF Maximum : " + dtehf_max)
    print("2Way Dynamic MTIE LF Minimum : " + dtemtie_min)
    print("2Way Dynamic MTIE LF Maximum : " + dtemtie_max)
    print("2Way Dynamic TDEV LF Minimum : " + dtetdev_min)
    print("2Way Dynamic TDEV LF Maximum : " + dtetdev_max)


    print("T1_TE_min : " + t1_te_min)
    print("T1_TE_max : " + t1_te_max)
    print("T4_TE_min : " + t4_te_min)
    print("T4_TE_max : " + t4_te_max)

    a1_var = cte.strip('-')
    b1_var = cte_min.strip('-')
    c1_var = cte_max.strip('-')
    d1_var = mtie_result.strip('- ')
    e1_var = tdev_result.strip('- ')
#    f1_var = dtelf_min.strip('- ')
#    g1_var = dtelf_max.strip('- ')
#    h1_var = dtehf_min.strip('- ')
#    i1_var = dtehf_max.strip('- ')
#    j1_var = dtemtie_min.strip('- ')
#    k1_var = dtemtie_max.strip('- ')
#    l1_var = dtetdev_min.strip('- ')
#    m1_var = dtetdev_max.strip('- ')

    te1 = te_min.strip('- ')
    te2 = te_max.strip('- ')
    te3 = te_mean.strip('- ')
    te11 = t1_te_min.strip('- ')
    te12 = t1_te_max.strip('- ')
    te13 = t4_te_min.strip('- ')
    te14 = t4_te_max.strip('- ')

    print("D1:" + d1_var)
    print("E1:" + e1_var)

    a2_var = a1_var.rstrip()
    b2_var = b1_var.rstrip()
    c2_var = c1_var.rstrip()
    d2_var = d1_var.rstrip()
    e2_var = e1_var.rstrip()
#    f2_var = f1_var.rstrip()
#    g2_var = g1_var.rstrip()
#    h2_var = h1_var.rstrip()
#    i2_var = i1_var.rstrip()
#    j2_var = j1_var.rstrip()
#    k2_var = k1_var.rstrip()
#    l2_var = l1_var.rstrip()
#    m2_var = m1_var.rstrip()

    te4 = te1.rstrip()
    te5 = te2.rstrip()
    te6 = te3.rstrip()
    te21 = te11.rstrip()
    te22 = te12.rstrip()
    te23 = te13.rstrip()
    te24 = te14.rstrip()

    print("D2:" + d2_var)
    print("E2:" + e2_var)

    print(type(d2_var))
    print(type(e2_var))

    a_var = int(float(a2_var))
    b_var = int(float(b2_var))
    c_var = int(float(c2_var))
    d_var = int(float(d2_var))
    e_var = int(float(e2_var))
#    f_var = int(float(f2_var))
#    g_var = int(float(g2_var))
#    h_var = int(float(h2_var))
#    i_var = int(float(i2_var))
#    j_var = int(float(j2_var))
#    k_var = int(float(k2_var))
#    l_var = int(float(l2_var))
#    m_var = int(float(m2_var))

    te7 = int(float(te4))
    te8 = int(float(te5))
    te9 = int(float(te6))
    te31 = int(float(te21))
    te32 = int(float(te22))
    te33 = int(float(te23))
    te34 = int(float(te24))

   # print("D:" %D)
   # print("E:" %E)

    if d_var == 1:
        print("2Way Dynamic MTIE LF_Mask : PASS")
    else:
        print("2Way Dynamic MTIE LF_Mask : FAIL")

    if e_var == 1:
        print("2Way Dynamic TDEV LF_Mask : PASS")
    else:
        print("2Way Dynamic TDEV LF_Mask : FAIL")

    rth.invoke('paragonset', "Cat SelectSlot ", "2Way")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimit", "0.07")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimitEnabled", "True")

    rth.invoke('paragonset', "Cat SelectSlot ", "Sync")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimit", "0.07")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimitEnabled", "True")

    rth.invoke('paragonset', "Cat SelectSlot ", "Delay Req")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimit", "0.07")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimitEnabled", "True")

    print("Going to Generate report for packet measurements")
    rth.invoke('paragonset', "Cat ReportField", "Report Title:Packet_Measurements_report")
    rth.invoke('paragonset', "Cat ReportField", "Report Description: Packet_Measurements report")
    rth.invoke('paragonset', "Cat ReportField", "User Name:reddyh")
#    rth.invoke('paragonset', "Cat GenerateReport", "TRUE")
    rth.invoke('paragonset', "Cat GenerateReport True ", "C:/Users/Calnex/Calnex_Automation/CAT_Reports/Result3_PacketMeasurements.pdf")
    rth.invoke('paragonset', "Cat Show", "FALSE")
    rth.invoke('paragonset', "Cat RemoveAll")

    print("Report Generation is completed")

    if a_var <= 20 and b_var <= 20 and c_var <= 20 and d_var == 1 and e_var == 1 and te7 <= 50 and te8 <= 50 and te9 <= 50 \
      and te31 <= 100 and te32 <= 100 and te33 <= 100 and te34 <= 100:
        print("PASS")
        return 1
    elif a_var <= 50 and b_var <= 50 and c_var <= 50 and d_var == 1 and e_var == 1 and te7 <= 70 and te8 <= 70 and te9 <= 70 \
      and te31 <= 100 and te32 <= 100 and te33 <= 100 and te34 <= 100:
        print("Device comply Class-A only")
        print("PASS")
        return 1
    else:
        print("FAIL")
        return 0

    rth.invoke('paragonset', "Cat", "Close")

def paragon_export_multiple(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('exportdata', "automation.cpd")

def history_1pps(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    history1pps = rth.invoke('paragonget', "InstrumentStatus Interface 1ppsMeasLock History")
    print("History1pps: %s" %history1pps)
    history1pps_1 = history1pps.rstrip()
    if history1pps_1 == "FALSE":
        print("1pps signal drop is not seen")
        return 1
    else:
        print("1pps signal drop is seen")
        return 0

def paragon_get_1pps_measurements(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "Cat Show", "TRUE")
    rth.invoke('paragonset', "Cat", "1PPS")
    rth.invoke('paragonset', "Cat SelectSlot ", "1pps")
    rth.invoke('paragonset', "Cat DTEMTIE Enable", "True")
    rth.invoke('paragonset', "Cat DTE Enable", "True")
    rth.invoke('paragonset', "Cat DTEHF Enable", "True")
    rth.invoke('paragonset', "Cat DTEMTIE Enable", "True")
    rth.invoke('paragonset', "Cat DTETDEV Enable", "True")
    rth.invoke('paragonset', "Cat DTEMTIE Mask ", "G.8273.2 dTE Gen Const Temp")
    rth.invoke('paragonset', "Cat DTETDEV Mask ", "G.8273.2 dTE Gen Const Temp")

    rth.invoke('paragonset', "Cat TIMEERROR Enable", "TRUE")
    te_min = rth.invoke('paragonget', "Cat TIMEERROR MIN")
    te_max = rth.invoke('paragonget', "Cat TIMEERROR MAX")
    print("1pps TIME ERROR Minimum:" + te_min)
    print("1pps TIME ERROR Maximum:" + te_max)

    rth.invoke('paragonset', "Cat AVERAGEDTE AveragingPeriod", "1000")
    rth.invoke('paragonset', "Cat Calculate", "1")
    rth.invoke('waitforcat')
    cte = rth.invoke('paragonget', "Cat AVERAGEDTE cTe")
    print("1pps Constant Time Error,cTE: " + cte)

    cte_min = rth.invoke('paragonget', "Cat AVERAGEDTE MIN")
    print("1pps Constant Time Error Minimum,cTE_min: " + cte_min)
    cte_max = rth.invoke('paragonget', "Cat AVERAGEDTE MAX")
    print("1pps Constant Time Error Maximum,cTE_max: " + cte_max)
    mtie_result = rth.invoke('paragonget', "Cat DTEMTIE MaskResult")

    tdev_result = rth.invoke('paragonget', "Cat DTETDEV MaskResult")

    dtelf_min = rth.invoke('paragonget', "Cat DTELF Min")
    print("1pps Dynamic TE LF Minimum : " + dtelf_min)

    dtelf_max = rth.invoke('paragonget', "Cat DTELF Max")
    print("1pps Dynamic TE LF Maximum : " + dtelf_max)

    dtehf_min = rth.invoke('paragonget', "Cat DTEHF Min")
    print("1pps Dynamic TE HF Minimum : " + dtehf_min)

    dtehf_max = rth.invoke('paragonget', "Cat DTEHF Max")
    print("1pps Dynamic TE HF Maximum : " + dtehf_max)

    dtemtie_min = rth.invoke('paragonget', "Cat DTEMTIE Min")
    print("1pps Dynamic TE MTIE LF Minimum : " + dtemtie_min)

    dtemtie_max = rth.invoke('paragonget', "Cat DTEMTIE Max")
    print("1pps Dynamic TE MTIE LF Maximum : " + dtemtie_max)

#    rth.invoke('paragonset', "Cat DTETDEV Enable", "True")

    dtetdev_min = rth.invoke('paragonget', "Cat DTETDEV Min")
    print("1pps Dynamic TE TDEV LF Minimum : " + dtetdev_min)

    dtetdev_max = rth.invoke('paragonget', "Cat DTETDEV Max")
    print("1pps Dynamic TE TDEV LF Maximum : " + dtetdev_max)

#    rth.invoke('paragonset', "Cat SelectSlot ", "1pps")

    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimit", "0.05")
#    rth.invoke('paragonset', "Cat TIMEERROR IncludeCorrectionField", "TRUE")

    a1_var = cte.strip('-')
    b1_var = cte_min.strip('-')
    c1_var = cte_max.strip('-')
    d1_var = mtie_result.strip('- ')
    e1_var = tdev_result.strip('- ')
    f1_var = te_min.strip('-')
    g1_var = te_max.strip('-')

#    print("A1:" + a1_var)
#    print("B1:" + b1_var)
#    print("C1:" + c1_var)
#    print("D1:" + d1_var)
#    print("E1:" + e1_var)
#    print("F1:" + f1_var)

    a2_var = a1_var.rstrip()
    b2_var = b1_var.rstrip()
    c2_var = c1_var.rstrip()
    d2_var = d1_var.rstrip()
    e2_var = e1_var.rstrip()
    f2_var = f1_var.rstrip()
    g2_var = g1_var.rstrip()

#    print("A2:" + a2_var)
#    print("B2:" + b2_var)
#    print("C2:" + c2_var)
#    print("D2:" + d2_var)
#    print("E2:" + e2_var)
#    print("F2:" + f2_var)

#    print(type(a2_var))
#    print(type(b2_var))
#    print(type(c2_var))
#    print(type(d2_var))

    a_var = int(float(a2_var))
    b_var = int(float(b2_var))
    c_var = int(float(c2_var))
    d_var = int(float(d2_var))
    e_var = int(float(e2_var))
    f_var = int(float(f2_var))
    g_var = int(float(g2_var))

#    print("cTE: %s" %a_var)
#    print("cTE_min: %s" %b_var)
#    print("cTE_max: %s" %c_var)
#    print("MTIE: %s" %d_var)
#    print("TE_min: %s" %e_var)
#    print("TE_max: %s" %f_var)

    if d_var == 1:
        print("2Way Dynamic MTIE LF_Mask : PASS")
    else:
        print("2Way Dynamic MTIE LF_Mask : FAIL")

    if e_var == 1:
        print("2Way Dynamic TDEV LF_Mask : PASS")
    else:
        print("2Way Dynamic TDEV LF_Mask : FAIL")


    #rth.invoke('paragonset', "Cat SelectSlot ", "2Way")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimit", "0.05")


    print("Going to Generate report for 1pps measurements")
    rth.invoke('paragonset', "Cat ReportField", "Report Title:1pps_Measurements_report")
    rth.invoke('paragonset', "Cat ReportField", "Report Description: 1pps_Measurements report")
    rth.invoke('paragonset', "Cat ReportField", "User Name:reddyh")
#    rth.invoke('paragonset', "Cat GenerateReport", "TRUE")
    rth.invoke('paragonset', "Cat GenerateReport True ", "C:/Users/Calnex/Calnex_Automation/CAT_Reports/Result3_1ppsMeasurements.pdf")
    rth.invoke('paragonset', "Cat Show", "FALSE")
    rth.invoke('paragonset', "Cat RemoveAll")
    print("Report Generation is completed")


    if a_var <= 20 and b_var <= 20 and c_var <= 20 and d_var == 1 and e_var == 1 and f_var <= 50 and g_var <= 50:
        print("PASS")
        return 1
    elif a_var <= 50 and b_var <= 50 and c_var <= 50 and d_var == 1 and e_var == 1 and f_var <= 70 and g_var <= 70:
        print("Device comply Class-A only")
        print("PASS")
        return 1
    else:
        print("FAIL")
        return 0

    rth.invoke('paragonset', "Cat", "Close")

def paragon_get_synce_measurements(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "Cat Show", "TRUE")
    rth.invoke('paragonset', "Cat", "SyncE")
    rth.invoke('paragonset', "Cat SelectSlot ", "SyncE")
    rth.invoke('paragonset', "Cat MTIE Enable", "True")
    rth.invoke('paragonset', "Cat TDEV Enable", "True")
    rth.invoke('paragonset', "Cat MTIE Mask ", "G.8262 Wander Generation EEC Op1")
    rth.invoke('paragonset', "Cat TDEV Mask ", "G.8262 Wander Generation EEC Op1")
    rth.invoke('paragonset', "Cat Calculate", "1")
    rth.invoke('waitforcat')

#    rth.invoke('paragonset', "Cat TIE", "TRUE")
    te_min = rth.invoke('paragonget', "Cat TIE MIN")
    te_max = rth.invoke('paragonget', "Cat TIE MAX")
    print("SyncE TIE Minimum:" + te_min)
    print("SyncE TIE Maximum:" + te_max)

    mtie_min = rth.invoke('paragonget', "Cat MTIE Min")
    print("SyncE MTIE Minimum : " + mtie_min)

    mtie_max = rth.invoke('paragonget', "Cat MTIE Max")
    print("SyncE MTIE Maximum : " + mtie_max)

#    rth.invoke('paragonset', "Cat DTETDEV Enable", "True")

    tdev_min = rth.invoke('paragonget', "Cat TDEV Min")
    print("SyncE TDEV Minimum : " + tdev_min)

    tdev_max = rth.invoke('paragonget', "Cat TDEV Max")
    print("SyncE TDEV Maximum : " + tdev_max)

    mtie_result = rth.invoke('paragonget', "Cat MTIE MaskResult")
    print("MTIE_Result : " + mtie_result)
    mtie = mtie_result.strip('- ')
    mtie1 = mtie.rstrip()
    mtie2 = int(float(mtie1))
    if mtie2 == 1:
        print("SyncE MTIE Mask : PASS")
    else:
        print("SyncE MTIE Mask : FAIL")

#    print("MTIE_Result: " + mtie_result)
    tdev_result = rth.invoke('paragonget', "Cat TDEV MaskResult")
    print("TDEV_Result : " + tdev_result)
    tdev = tdev_result.strip('- ')
    tdev1 = tdev.rstrip()
    tdev2 = int(float(tdev1))
    if tdev2 == 1:
        print("SyncE TDEV Mask : PASS")
    else:
        print("SyncE TDEV Mask : FAIL")

#    print("TDEV_Result: " + tdev_result)

    print("Going to Generate report for SYncE Measurements")
    rth.invoke('paragonset', "Cat ReportField", "Report Title:SyncE_Measurements_report")
    rth.invoke('paragonset', "Cat ReportField", "Report Description: SyncE_Measurements report")
    rth.invoke('paragonset', "Cat ReportField", "User Name:reddyh")
#    rth.invoke('paragonset', "Cat GenerateReport", "TRUE")
    rth.invoke('paragonset', "Cat GenerateReport True ", "C:/Users/Calnex/Calnex_Automation/CAT_Reports/Result3_SyncEMeasurements.pdf")
    rth.invoke('paragonset', "Cat Show", "FALSE")
    rth.invoke('paragonset', "Cat RemoveAll")
    print("Report Generation is completed")

#    mtie = mtie_result.strip('_')
#    tdev = tdev_result.strip('_')

#    print("MTIE:" + mtie)
#    print("TDEV:" + tdev)

#    mtie1 = mtie.rstrip()
#    tdev1 = tdev.rstrip()

#    print("MTIE1:" + mtie1)
#    print("TDEV1:" + tdev1)

#    print(type(mtie1))
#    print(type(tdev1))

#    mtie2 = int(float(mtie1))
#    tdev2 = int(float(tdev1))

#    print("MTIE_Result: %s" %mtie2)
#    print("TDEV_Result: %s" %tdev2)

    if mtie2 == 1 and tdev2 == 1:
        print("PASS")
        return 1
    else:
        print("FAIL")
        return 0

    rth.invoke('paragonset', "Cat", "Close")

def paragon_get_1pps_measurements1(rth):
    '''
    Please insert proper description of method and parameters here
    '''
    rth.invoke('paragonset', "Cat 1PPS")
    rth.invoke('paragonset', "Cat Show", "TRUE")
    rth.invoke('paragonset', "Cat TIMEERROR", "SelectTab")
    rth.invoke('paragonset', "Cat TIMEERROR ThresholdLimit", "0.2")
    rth.invoke('paragonset', "Cat Calculate")
    rth.invoke('waitforcat')

    rth.invoke('paragonset', "Cat AVERAGEDTE AllEnable", "True")
    rth.invoke('paragonset', "Cat AVERAGEDTE", "SelectTab")
    rth.invoke('paragonset', "Cat AVERAGEDTE AveragingPeriod", "50")
    rth.invoke('paragonset', "Cat AVERAGEDTE ThresholdLimitEnabled", "True")
    rth.invoke('paragonset', "Cat SelectSlot", "C0")
    rth.invoke('paragonset', "Cat AVERAGEDTE ThresholdLimit", "0.1")
    rth.invoke('paragonset', "Cat Calculate")
    rth.invoke('waitforcat')

    rth.invoke('paragonset', "Cat SelectSlot", "C0")
    rth.invoke('paragonset', "Cat DTEMTIE Enable", "True")
    rth.invoke('paragonset', "Cat DTEMTIE Mask", "G.8273.2 dTE Gen Const Temp")
    rth.invoke('paragonset', "Cat DTEMTIE AveragingPeriod", "50")
    rth.invoke('paragonset', "Cat Calculate")

    rth.invoke('paragonset', "Cat SelectSlot", "C0")
    rth.invoke('paragonset', "Cat DTETDEV Enable", "True")
    rth.invoke('paragonset', "Cat DTETDEV Mask", "G.8273.2 dTE Gen Const Temp")
    rth.invoke('paragonset', "Cat DTETDEV AveragingPeriod", "50")
    rth.invoke('paragonset', "Cat Calculate")
    rth.invoke('waitforcat')

    cte = rth.invoke('paragonget', "Cat AVERAGEDTE cTe")
    print("cTE: "+ cte)

    mtie_result = rth.invoke('paragonget', "Cat DTEMTIE MaskResult")
    print("MTIE_Result: " + mtie_result)

    tdev_result = rth.invoke('paragonget', "Cat DTETDEV MaskResult")
    print("TDEV_Result: " + tdev_result)

#######	 SAVE 1pps measurements report #################################

    print("\n\nSaving 1pps measurement pdf results \n\n")
    rth.invoke('paragonset', "Cat ReportField", "Report Title:PTP_1pps_report")
    rth.invoke('paragonset', "Cat ReportField", "Report Description: PTP 1pps report")
    rth.invoke('paragonset', "Cat ReportField", "User Name:Juniper")
    rth.invoke('paragonset', "Cat GenerateReport", "TRUE")
    rth.invoke('paragonset', "Cat Show", "FALSE")
    rth.invoke('paragonset', "Cat RemoveAll")
