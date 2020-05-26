""" This module is library of WARP17 traffic generator """

__author__ = ['Raghavendra Shenoy']
__contact__ = 'shenoyr@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

from jnpr.toby.hldcl.unix.unix import Unix
#from jnpr.toby.logger.logger import get_log_dir
import re
import pexpect
import json
import os
import time
import inspect

###################################################################################
# Name        : Manager()
# Description : Creates an instance of WARP17 Manager which will do a RPC to config WARP17 box
################################################################################

class Warp17api(object):
    """
        Method called by user to Create an instance of WARP17
        :server name
            *MANDATORY* server where warp17 process is generated
        :eth_if  :
            *MANDATORY* ethernet interface on Host machine
        :Other Optional Arugments:
         inet                  - [1|0] ip v4 interface (Default = true)
         inet6                 - [1|0] ip v6 interface (Default = false)
         mem_in_mb             - RAM allocation for traffic (Default = 32768(mb))
         setup_dpdk_flag       - [1|0] if set as true it binds, unbinds, re-installs DPDK (Default = true)
         setup_warp17  	       - [1|0] Kick starts WARP17 (Default = true)
         qmap                  - bitmask specifying the physical cores (default = 0x42)
         qmap_default          - way of handling physical cores (default = max-q)
         ch_cfg                - [1|0] default value 0
         data_cores            - physical cores used for traffic (default = 14)
         ctrl_cores            - physical cores used for cli and managements (default = 2)
         mbuf_hdr_pool_sz      - size of the packet headers pool (default = 750)
         mbuf_pool_sz          - size of the packet pool (default = 750)
         cmd_file              - WARP17 configuration file name
         bind                  - To bind ethernet interface from the current driver list and move to use igb_uio (default = igb_uio)
         dpdk_src_path         - DPDK path (default = /root/WARP17/dpdk-16.04)
         hex_mask              - Hexadecimal value of CPU cores (default = ff00ff00)
         tcb_pool_sz           - TCP control block pool size (default = (num_of_cpus/2) * 1700)
         ucb_pool_sz           - UDP control block pool size (default = 32768)
         ring_if_pairs         - [1|0] for running WARP17 without the pysical interfaces (default = false)
         nchan                 - number of dmidecode channels (default = 'system default : (dmidecode | grep -i channel))
         log_level             - Log verbosity level (default = not-added)
    """
    warp17_obj, eth_if, eth_port = None, None, None
    dpdk_src_path, data_cores, unbind = None, None, None
    inet, inet6, nchan, dpdk_status, warp17_path, dpdk_final, dpdk_order = None, None, None, None, None, None, None
    uname, password, cmdlist, ctrl_cores, mem_in_mb, mbuf_pool_sz, mbuf_hdr_pool_sz, ch_cfg = None, None, None, None, None, None, None, None
    host_name = "localhost"
    debug_logs = True
    def __init__(self, server_name):
        self.ip_start = None
        if server_name:
            self.server_name = server_name
        else:
            raise Exception("Missing server_name parameter")

    def connect(self, port_list, **kwargs):
        """ connect """
        # Connecting to server
        #print = utils.log
        self.warp17_obj = Unix(host=self.server_name, user='root', password='Embe1mpls', osname='Unix')
        self.eth_if = port_list
        # Modify the default values if the user has provided an input arguments
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Get all the default values for WARP17.
        if kwargs.get('virtual_machine') == '1':
            self.warp17_defaults_vm()
        else:
            self.warp17_defaults()

        if self.setup_dpdk_flag:
            self.dpdk_status = self.setup_dpdk()
        self.dpdk_order = self.get_dpdk_status()

        options_cpu = []
        options_cpu.append(self.data_cores)
        options_cpu.append(self.ctrl_cores)
        lscpu_data = self.calc_cpu_cores()


        if isinstance(kwargs.get('tcb_pool_sz'), int):
            if kwargs.get('tcb_pool_sz') > 1:
                self.tcb_pool_sz = kwargs.get('tcb_pool_sz')
            else:
                self.tcb_pool_sz = 1
        elif isinstance(kwargs.get('tcb_pool_sz'), str):
            if kwargs.get('tcb_pool_sz') == 'max':
                self.tcb_pool_sz = int(self.mem_in_mb * 80/100)

        if isinstance(kwargs.get('ucb_pool_sz'), int):
            if kwargs.get('ucb_pool_sz') > 1:
                self.ucb_pool_sz = kwargs.get('ucb_pool_sz')
            else:
                self.ucb_pool_sz = 1
        elif isinstance(kwargs.get('ucb_pool_sz'), str):
            if kwargs.get('ucb_pool_sz') == 'max':
                self.ucb_pool_sz = int(self.mem_in_mb * 90/100)


        uniq = dict()
        dpdk_core = 2

        for intf in self.eth_if:
            if_bus_slot_func = self.dpdk_status['intf_pci_map'][intf]
            if kwargs.get('virtual_machine') == '1':
                pci_numa_node = 0
            else:
                pci_numa_node = self.get_numa_node(eth_if_in_bus_slot_func=if_bus_slot_func)
            uniq[pci_numa_node] = 'dummy'
        print("pic_numa_node is "+str(pci_numa_node))
        all_numa_node = uniq.keys()
        for each_numa_node in all_numa_node:
            temp_lcores = lscpu_data['numa_node'][str(each_numa_node)]['cpu_core']
            print(" new variables "+str(lscpu_data['numa_node'][str(each_numa_node)]['cpu_core']))
            if kwargs.get('virtual_machine') == '1':
                lcores = '0'+'@'+str(temp_lcores[0])+','+'1'+'@'+str(temp_lcores[1])
                temp_lcores = temp_lcores[2:]
                for core in temp_lcores:
                    lcores = str(lcores)+','+str(dpdk_core)+'@'+str(core)
                    dpdk_core += 1
            else:
                lcores = '0'+'@'+str(temp_lcores[0])+','+'1'+'@'+str(temp_lcores[0])
                temp_lcores = temp_lcores[1:]
                for core in temp_lcores:
                    lcores = str(lcores)+','+str(dpdk_core)+'@'+str(core)
                    dpdk_core += 1
        if not self.lcores:
            self.lcores = lcores

        print("\n"+self.lcores+"\n")


        print("Driver to ethernet map\n")
        if self.setup_warp17():
            print("Successfully Created\n")
        else:
            print("WARP17 process is not started\n")
            return False

        self.client_handle = Unix(host=self.server_name, user='root', password='Embe1mpls', osname='Unix')
        if self.host_name == "localhost":
            print(" RPC client should be running in local server")
        else:
            #self.client_handle.shell(command="export WARP17_HOST="+self.host_name)
            self.client_handle.shell(command="export WARP17_HOST="+self.host_name)

        output = getattr(self.client_handle, 'shell')(command="locate rpc_client.py").response()
        if output is not None:
            match = re.search(r"(.*)rpc_client.py.*", output)
            self.rpc_client_path = match.group(1)
            self.client_handle.shell(command="cd "+self.rpc_client_path)
        else:
            print(": There is no RPC client file available at specified server\n")
            return False

        ini = self.create_rpc_ini_file(self.rpc_client_path)
        if ini:
            print(": Successfully created rpcClient.ini file\n")
        else:
            print(": Failed to create rpcClient.ini\n")
            return False

        return True


    def clienttestcase(self, **kwargs):
        """ Configures Client port with L4-L7 traffic details which includes rate,
        criteria and application layer protocol details."""

        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]
        if 'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        if 'source_ip_start' in kwargs:
            source_ip_start = kwargs.get('source_ip_start')
        if 'source_ip_end' in kwargs:
            source_ip_end = kwargs.get('source_ip_end')
        if 'dest_ip_start' in kwargs:
            dest_ip_start = kwargs.get('dest_ip_start')
        if 'dest_ip_end' in kwargs:
            dest_ip_end = kwargs.get('dest_ip_end')
        if 'spr_start' in kwargs:
            spr_start = kwargs.get('spr_start', '10001')
        if 'spr_end' in kwargs:
            spr_end = kwargs.get('spr_end', '30000')
        if 'dpr_start' in kwargs:
            dpr_start = kwargs.get('dpr_start', '101')
        if 'dpr_end' in kwargs:
            dpr_end = kwargs.get('dpr_end', '200')
        if 'action' in kwargs:
            action = kwargs.get('action')
        else:
            action = 'None'
            print("Mandatory Argument Action is required\n")
        if  'port' in kwargs:
            port = kwargs.get('port')
        else:
            port = 'None'
            print("Mandatory Argument Action is required\n")
        if 'multicast' in kwargs:
            multicast = kwargs.get('multicast')
        else:
            multicast = None

        if 'proto' in kwargs:
            proto = kwargs.get('proto')
        if 'async' in kwargs:
            async1 = kwargs.get('async', 'True')

        if not source_ip_end:
            source_ip_end = source_ip_start
        if not dest_ip_end:
            dest_ip_end = dest_ip_start

        if 'app_proto' in kwargs:
            if kwargs.get('app_proto') == 'HTTP':
                app_proto = kwargs.get('app_proto')
                size = kwargs.get('size')
                objct = kwargs.get('object')
                host = kwargs.get('host')
            elif kwargs.get('app_proto') == 'RAW':
                app_proto = kwargs.get('app_proto')
                req_size = kwargs.get('req_size', '100')
                resp_size = kwargs.get('resp_size', '200')
        if 'tc_run_time' in kwargs:
            tc_run_time = kwargs.get('tc_run_time')
        if 'init_delay' in kwargs:
            init_delay = kwargs.get('init_delay')
        if 'uptime' in kwargs:
            uptime = kwargs.get('uptime')
        if 'downtime' in kwargs:
            downtime = kwargs.get('downtime')

        open_rate = kwargs.get('open_rate', '10000')
        send_rate = kwargs.get('send_rate', '10000')
        close_rate = kwargs.get('close_rate', '500')

        if app_proto == 'HTTP':
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+ \
            " port="+str(self.eth_port[port])+" proto="+proto+" tc_id="+tc_id+" source_ip_start="+ \
            source_ip_start+" source_ip_end="+source_ip_end+" dest_ip_start="+dest_ip_start+ \
            " dest_ip_end="+dest_ip_end+" dpr_start="+dpr_start+" dpr_end="+dpr_end+ \
            " tc_run_time="+tc_run_time+" app_proto="+app_proto+" object="+objct+" size="+size+ \
            " host="+host+" spr_start="+spr_start+" spr_end="+spr_end+" init_delay="+init_delay+" uptime="+uptime+ \
            " send_rate="+send_rate+" open_rate="+open_rate+" close_rate="+close_rate+" async="+async1+ \
            " downtime="+downtime+" multi="+str(multicast))
        else:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+" port="+ \
            str(self.eth_port[port])+" proto="+proto+" tc_id="+tc_id+" source_ip_start="+source_ip_start+" source_ip_end="+ \
            source_ip_end+" dest_ip_start="+dest_ip_start+" dest_ip_end="+dest_ip_end+" dpr_start="+dpr_start+ \
            " dpr_end="+dpr_end+" tc_run_time="+tc_run_time+" app_proto="+app_proto+" init_delay="+init_delay+ \
            " uptime="+uptime+" req_size="+req_size+" resp_size="+resp_size+" spr_start="+spr_start+ \
            " spr_end="+spr_end+" send_rate="+send_rate+" open_rate="+open_rate+" close_rate="+close_rate+ \
            " downtime="+downtime+" async="+async1+" multi="+str(multicast))
        if result is not None:
            return True


    def imix(self, **kwargs):
        """ Configures Client port with L4-L7 traffic details which includes rate,
        criteria and application layer protocol details."""

        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]
        if 'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        if 'source_ip_start' in kwargs:
            source_ip_start = kwargs.get('source_ip_start')
        if 'source_ip_end' in kwargs:
            source_ip_end = kwargs.get('source_ip_end')
        if 'dest_ip_start' in kwargs:
            dest_ip_start = kwargs.get('dest_ip_start')
        if 'dest_ip_start' in kwargs:
            dest_ip_end = kwargs.get('dest_ip_end')
        if 'spr_start' in kwargs:
            spr_start = kwargs.get('spr_start', '10001')
        if 'spr_end' in kwargs:
            spr_end = kwargs.get('spr_end', '30000')
        if 'dpr_start' in kwargs:
            dpr_start = kwargs.get('dpr_start', '101')
        if 'dpr_end' in kwargs:
            dpr_end = kwargs.get('dpr_end', '200')
        if 'action' in kwargs:
            action = kwargs.get('action')
        else:
            action = 'None'
            print("Mandatory Argument Action is required\n")
        if  'port' in kwargs:
            port = kwargs.get('port')
        else:
            port = 'None'
            print("Mandatory Argument Action is required\n")

        if 'proto' in kwargs:
            proto = kwargs.get('proto')
        if 'async' in kwargs:
            async1 = kwargs.get('async', 'True')

        if 'app_proto' in kwargs:
            app_proto = kwargs.get('app_proto')
        if 'size' in kwargs:
            size = kwargs.get('size')

        if 'weight' in kwargs:
            weight = kwargs.get('weight')
        if 'tc_run_time' in kwargs:
            tc_run_time = kwargs.get('tc_run_time')
        if 'init_delay' in kwargs:
            init_delay = kwargs.get('init_delay')
        if 'uptime' in kwargs:
            uptime = kwargs.get('uptime')
        #if 'downtime' in kwargs:
        #   downtime = kwargs.get('downtime')
        if 'imix_type' in kwargs:
            imix_type = kwargs.get('imix_type')
        if 'imix_id' in kwargs:
            imix_id = kwargs.get('imix_id')

        open_rate = kwargs.get('open_rate', '10000')
        send_rate = kwargs.get('send_rate', '10000')

        if imix_type == 'client':
            if not source_ip_end:
                source_ip_end = source_ip_start
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+ \
            " port="+str(self.eth_port[port])+" proto="+proto+" tc_id="+tc_id+" source_ip_start="+ \
            source_ip_start+" source_ip_end="+source_ip_end+" dest_ip_start="+dest_ip_start+ \
            " dest_ip_end="+dest_ip_end+" dpr_start="+dpr_start+" dpr_end="+dpr_end+ \
            " tc_run_time="+tc_run_time+" app_proto=\""+app_proto+"\""+" size=\""+size+"\""+ \
            " spr_start="+spr_start+" spr_end="+spr_end+" init_delay="+init_delay+" uptime="+uptime+ \
            " send_rate="+send_rate+" open_rate="+open_rate+" async="+async1+" weight=\""+weight+"\""+" imix_type="+imix_type+" imix_id="+imix_id)
        elif imix_type == 'server':
            if not dest_ip_end:
                dest_ip_end = dest_ip_start
            req_size = kwargs.get('req_size', '100')
            resp_size = kwargs.get('resp_size', '150')
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+ \
            " port="+str(self.eth_port[port])+" tc_id="+tc_id+" proto="+proto+ \
            " dest_ip_start="+dest_ip_start+" dest_ip_end="+dest_ip_end+" dpr_start="+dpr_start+ \
            " dpr_end="+dpr_end+" app_proto=\""+app_proto+"\""+" req_size="+req_size+" size=\""+size+"\""+ \
            " resp_size="+resp_size+" tc_run_time="+tc_run_time+" async="+async1+" weight=\""+weight+"\""+" imix_type="+imix_type+" imix_id="+imix_id)
        if result is not None:
            return True

######################################################################################
# Name       : l3_intf
# Description: Configures ip addresses or list of ip addresses and gateway on specified port
######################################################################################


    def l3_intf(self, **kwargs):
        """ methos to configure ip, gateway and mask"""
        #self.client_handle.shell(command="cd "+self.rpc_client_path)
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]

        if 'gateway' in kwargs:
            gateway = kwargs.get('gateway')
        else:
            raise TypeError('Missing mandatory argument, gateway')
        if 'ip_start' in kwargs:
            ip_start = kwargs.get('ip_start')
        else:
            raise TypeError('Missing mandatory argument, ip_start')
        if 'ip_end' in kwargs:
            ip_end = kwargs.get('ip_end')
        else:
            raise TypeError('Missing mandatory argument, ip_end')
        if 'mask' in kwargs:
            mask = kwargs.get('mask')
        else:
            raise TypeError('Missing mandatory argument, mask')
        if 'action' in kwargs:
            action = kwargs.get('action')
        else:
            action = 'None'
        if  'port' in kwargs:
            port = kwargs.get('port')
        else:
            raise TypeError('Missing mandatory argument, port')

        if 'vlan_id' in kwargs:
            vlan_id = kwargs.get('vlan_id')
            vlan_enable = True
        else:
            vlan_enable = False

        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        if vlan_enable:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+" port="+\
            str(self.eth_port[port])+\
            " gateway="+gateway+" ip_start="+ip_start+" ip_end="+ip_end+" mask="+mask+" vlan="+str(vlan_enable)+" vlan_id="+str(vlan_id))
        else:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+" port="+\
            str(self.eth_port[port])+\
            " gateway="+gateway+" ip_start="+ip_start+" ip_end="+ip_end+" mask="+mask+" vlan="+str(None))
        if result is not None:
            return True


######################################################################################
# Name       : l2_intf
# Description: Configures mtu on given interface
######################################################################################


    def l2_intf(self, **kwargs):
        """ Configures mtu on given interface """
        #self.client_handle.shell(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]

        if 'port' in kwargs:
            port = kwargs.pop('port')
        else:
            raise TypeError('Missing mandatory argument, port')
        if 'mtu' in kwargs:
            mtu = kwargs.pop('mtu')
        else:
            raise TypeError('Missing mandatory argument,  mtu')
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" port="+\
                 str(self.eth_port[port])+" mtu="+mtu)
        if result is not None:
            return True


    def ipv4_options(self, **kwargs):
        """ Configures dscp and ecn on ipv4 packet """
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]

        if 'port' in kwargs:
            port = kwargs.pop('port')
        else:
            raise TypeError('Mandatory argument port is missing')
        if 'tc_id' in kwargs:
            tc_id = kwargs.pop('tc_id')
        else:
            raise TypeError('Mandatory argument tc_id is missing')
        dscp = kwargs.get('dscp', None)
        ecn = kwargs.get('ecn', None)
        tos = kwargs.get('tos', None)
        if tos is None:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" port="+str(self.eth_port[port])\
                     +" tc_id="+str(tc_id)+" dscp="+dscp+" ecn="+ecn)
        else:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" port="+str(self.eth_port[port])\
                     +" tc_id="+str(tc_id)+" tos="+tos)
        if result is not None:
            return True


    def vlan_options(self, **kwargs):
        """ Configures vlan on ethernet packet """
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]

        if 'port' in kwargs:
            port = kwargs.pop('port')
        else:
            raise TypeError("Mandatory argument port is missing")
        if 'tc_id' in kwargs:
            tc_id = kwargs.pop('tc_id')
        else:
            raise TypeError("Mandatory argument tc_id is missing")

        vlan_id = kwargs.get('vlan_id', None)
        vlan_pri = kwargs.get('vlan_pri', None)
        result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" port="+\
                 str(self.eth_port[port])+" tc_id="+str(tc_id)+" vlan="+vlan_id+" vlan_pri="+vlan_pri)
        if result is not None:
            return True

######################################################################################
# Name       : ServerTestCase
# Description: Configures Server port with L4-L7 traffic details which includes rate, criteria and application layer protocol details.
######################################################################################

    def servertestcase(self, **kwargs):
        """ method to configure server port """
        #self.client_handle.shell(command="cd "+self.rpc_client_path)
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]
        if 'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        if 'dest_ip_start' in kwargs:
            dest_ip_start = kwargs.get('dest_ip_start')
        if 'dest_ip_end' in kwargs:
            dest_ip_end = kwargs.get('dest_ip_end')
        if 'dpr_start' in kwargs:
            dpr_start = kwargs.get('dpr_start', '101')
        if 'dpr_end' in kwargs:
            dpr_end = kwargs.get('dpr_end', '200')
        if 'action' in kwargs:
            action = kwargs.get('action')
        if  'port' in kwargs:
            port = kwargs.get('port')
        if  'proto' in kwargs:
            proto = kwargs.get('proto')
        if 'action' in kwargs:
            action = kwargs.get('action')
        else:
            action = 'None'
        if 'tc_run_time' in kwargs:
            tc_run_time = kwargs.get('tc_run_time')
        if 'async' in kwargs:
            async1 = kwargs.get('async', 'True')

        if 'app_proto' in kwargs:
            if kwargs.get('app_proto') == 'HTTP':
                app_proto = kwargs.get('app_proto')
                resp_size = kwargs.get('resp_size')
                resp_code = kwargs.get('resp_code')
            elif kwargs.get('app_proto') == 'RAW':
                app_proto = kwargs.get('app_proto')
                req_size = kwargs.get('req_size', '100')
                resp_size = kwargs.get('resp_size', '150')

        if app_proto == 'HTTP':
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+ \
            " port="+str(self.eth_port[port])+" tc_id="+tc_id+" proto="+proto+ \
            " dest_ip_start="+dest_ip_start+" dest_ip_end="+dest_ip_end+" dpr_start="+dpr_start+ \
            " dpr_end="+dpr_end+" resp_code="+resp_code+" resp_size="+resp_size+ \
            " app_proto="+app_proto+" tc_run_time="+tc_run_time+" async="+async1)
        else:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" action="+action+ \
            " port="+str(self.eth_port[port])+" tc_id="+tc_id+" proto="+proto+ \
            " dest_ip_start="+dest_ip_start+" dest_ip_end="+dest_ip_end+" dpr_start="+dpr_start+ \
            " dpr_end="+dpr_end+" app_proto="+app_proto+" req_size="+req_size+ \
            " resp_size="+resp_size+" tc_run_time="+tc_run_time+" async="+async1)
        if result is not None:
            return True

    def delete_testcase(self, **kwargs):
        """ this method configures tcp options on client and server ports """
        if 'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        if 'port' in kwargs:
            port = kwargs.get('port')
        result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function=delete_testcase port="+str(self.eth_port[port])+ \
            " tc_id="+tc_id)
        if result is not None:
            return True


    def tcp_control(self, **kwargs):
        """ this method configures tcp options on client and server ports """
        if 'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        if 'port' in kwargs:
            port = kwargs.get('port')
        if 'to_syn_ack_retry_cnt' in kwargs:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function=tcp_options port="+str(self.eth_port[port])+ \
          " tc_id="+tc_id+" tcp_option=to_syn_ack_retry_cnt tcp_option_value="+kwargs.get('to_syn_ack_retry_cnt'))
        if 'to_retry_cnt' in kwargs:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function=tcp_options port="+str(self.eth_port[port])+ \
            " tc_id="+tc_id+" tcp_option=to_retry_cnt tcp_option_value="+kwargs.get('to_retry_cnt'))
        if 'to_rto' in kwargs:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function=tcp_options port="+str(self.eth_port[port])+ \
            " tc_id="+tc_id+" tcp_option=to_rto tcp_option_value="+kwargs.get('to_rto'))
        if 'to_data_retry_cnt' in kwargs:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function=tcp_options port="+str(self.eth_port[port])+ \
            " tc_id="+tc_id+" tcp_option=to_data_retry_cnt tcp_option_value="+kwargs.get('to_data_retry_cnt'))
        if 'to_win_size' in kwargs:
            result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function=tcp_options port="+str(self.eth_port[port])+ \
            " tc_id="+tc_id+" tcp_option=to_win_size  tcp_option_value="+kwargs.get('to_win_size'))
        if result is not None:
            return True

    def starttraffic(self, **kwargs):
        """ this method triggers traffic on given port """
        #self.client_handle.shell(command="cd "+self.rpc_client_path)
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]
        if  'port' in kwargs:
            port = kwargs.get('port')
        #if 'action' in kwargs:
        result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" port="+str(self.eth_port[port]))
        if result is not None:
            return True

    def stoptraffic(self, **kwargs):
        """ this method stops traffic on given port """
        #self.client_handle.shell(command="cd "+self.rpc_client_path)
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]
        if  'port' in kwargs:
            port = kwargs.get('port')
        #if 'action' in kwargs:
        #    action = kwargs.get('action')
        result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+" port="+str(self.eth_port[port]))
        if result is not None:
            return True


    def checkstatus(self, **kwargs):
        """ this methos provides status of port """
        #self.client_handle.shell(command="cd "+self.rpc_client_path)
        getattr(self.client_handle, 'shell')(command="cd "+self.rpc_client_path)
        func_name = inspect.stack()[0][3]
        if  'port' in kwargs:
            port = kwargs.get('port')
        if  'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        result = getattr(self.client_handle, 'shell')(command="python rpc_client.py function="+func_name+\
                 " port="+str(self.eth_port[port])+" tc_id="+tc_id)
        if result is not None:
            return True


    def get_ipv4_stats(self, **kwargs):
        """ this method provides dict with ipv4 stats """
        ipv4_stats = dict()
        if  'port' in kwargs:
            port = kwargs.get('port')
        output = getattr(self.warp17_obj, 'shell')(command="show ipv4 statistics", pattern="warp17>").response()
        out = output.split("\n")
        for line in out:
            if len(line) > 0:
                if re.search(r"Port\s+(\d+)\s+IPv4\s+statistics:", line) is not None:
                    match = re.search(r"^Port\s+(\d+)\s+IPv4\s+statistics:", line)
                    port = match.group(1)
                    ipv4_stats[port] = dict()
                if re.search(r"Received\s*Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*Packets\s*:\s*(\d+)", line)
                    ipv4_stats[port]['rcvd_pkts'] = match.group(1)
                if re.search(r"Received\s*Bytes\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*Bytes\s*:\s*(\d+)", line)
                    ipv4_stats[port]['rcvd_bytes'] = match.group(1)
                if re.search(r"Received\s*ICMP\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*ICMP\s*:\s*(\d+)", line)
                    ipv4_stats[port]['rcvd_icmp'] = match.group(1)
                if re.search(r"Received\s*TCP\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*TCP\s*:\s*(\d+)", line)
                    ipv4_stats[port]['rcvd_tcp'] = match.group(1)
                if re.search(r"Received\s*UDP\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*UDP\s*:\s*(\d+)", line)
                    ipv4_stats[port]['rcvd_udp'] = match.group(1)
                if re.search(r"Received\s*other\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*other\s*:\s*(\d+)", line)
                    ipv4_stats[port]['rcvd_other'] = match.group(1)
                if re.search(r"Received\s*Fragments\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*Fragments\s*:\s*(\d+)", line)
                    ipv4_stats[port]['rcvd_frags'] = match.group(1)
                if re.search(r"Invalid\s+checksum\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Invalid\s+checksum\s*:\s*(\d+)", line)
                    ipv4_stats[port]['invl_chk_sum'] = match.group(1)
                if re.search(r"Small\s+mbuf\s+fragment\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Small\s+mbuf\s+fragment\s*:\s*(\d+)", line)
                    ipv4_stats[port]['small_mbuf_frag'] = match.group(1)
                if re.search(r"IP\s+hdr\s+\w+\s+small\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"IP\s+hdr\s+\w+\s+small\s*:\s*(\d+)", line)
                    ipv4_stats[port]['ip_hdr_too_small'] = match.group(1)
                if re.search(r"Total\s+length\s+invalid\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Total\s+length\s+invalid\s*:\s*(\d+)", line)
                    ipv4_stats[port]['total_len_invl'] = match.group(1)
                if re.search(r"Invalid version.*\s+:\s*(\d+)", line) is not None:
                    match = re.search(r"Invalid version.*\s+:\s*(\d+)", line)
                    ipv4_stats[port]['invl_version'] = match.group(1)
                if re.search(r"Reserved\s+bit\s+set.*\s+:\s*(\d+)", line) is not None:
                    match = re.search(r"Reserved\s+bit\s+set.*\s+:\s*(\d+)", line)
                    ipv4_stats[port]['resv_bit_set'] = match.group(1)

        #print(json.dumps(ipv4_stats, indent=4))
        return ipv4_stats



    def verify_warp17_stats(self, **kwargs):
        """ this method is wrapper def for stats method """
        args, act_data = dict(), dict()
        tc_id, tol_val, tol_perc = None, None, None
        if  'warp17_stat' in kwargs:
            warp17_stat = kwargs.get('warp17_stat')
            del kwargs['warp17_stat']
        if  'tol_val' in kwargs:
            tol_val = kwargs.get('tol_val')
            del kwargs['tol_val']

        if  'tol_perc' in kwargs:
            tol_perc = kwargs.get('tol_perc')
            del kwargs['tol_perc']
        args = kwargs.copy()

        if 'port' not in args:
            raise TypeError("Mandatory argument port is missing")

        port = args['port']
        if 'tc_id' in args:
            tc_id = args.get('tc_id')
        else:
            tc_id = None

        del args['port']
        if tc_id:
            del args['tc_id']

        if port is None:
            act_data = getattr(Warp17api, warp17_stat)(self)
        else:
            print(" Geting  "+warp17_stat)
            act_data = getattr(Warp17api, warp17_stat)(self, port=str(self.eth_port[port]))
        print("Expected Data"+json.dumps(args, indent=4))

        if port:
            if tc_id:
                return Warp17api.cmp_data(args, act_data[str(self.eth_port[port])][tc_id], tol_val, tol_perc)
            else:
                print(act_data[str(self.eth_port[port])])
                return Warp17api.cmp_data(args, act_data[str(self.eth_port[port])], tol_val, tol_perc)

        else:
            return Warp17api.cmp_data(args, act_data, tol_val, tol_perc)


    def get_port_config(self, **kwargs):
        """ this method provides dict with port configs """

        print("### show tests config port <port> ###")
        port_config = dict()
        if 'port' not in kwargs:
            raise TypeError('Mandatory argument port is missing')
        else:
            port = kwargs.get('port')

        output = getattr(self.warp17_obj, 'shell')(command='show tests config port ' + \
                 str(self.dpdk_order["port_order"][self.dpdk_final["intf_pci_map"][port]]), pattern="warp17>").response()
        out = output.split("\n")

        out = [i.rstrip().strip() for i in out]
        app_host, tc_id = None, None
        for line in out:
            if len(line) > 0:
                if re.search(r"^GW:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", line) is not None:
                    match = re.search(r"^GW:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", line)
                    port_config['gw_ip'] = match.group(1)


                if re.search(r"^Test\s+Case\s+Id:\s+(\w+)$", line) is not None:
                    match = re.search(r"^Test\s+Case\s+Id:\s+(\w+)$", line)
                    tc_id = match.group(1)

                if re.search(r"^Test\s+type:\s+(.*)$", line) is not None:
                    match = re.search(r"^Test\s+type:\s+(.*)$", line)
                    tc_type = match.group(1)
                    tc_type.replace(" ", "_")
                    port_config['tc_type'] = tc_type

                if re.search(r"^Local\s+IP:Port\s+:\s+\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+->\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]:[(\d+)\s+->\s+(\d+)]", \
                    line) is not None:
                    match = re.search(r"^Local\s+IP:Port\s+:\s+\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+->\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]:[(\d+)\s+->\s+(\d+)]", \
                    line)
                    port_config['local_ip_low'] = match.group(1)
                    port_config['local_ip_high'] = match.group(2)
                    port_config['local_port_low'] = match.group(3)
                    port_config['local_port_high'] = match.group(4)

                if re.search(r"^Remote\s+IP:Port\s+:\s+\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+->\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]:[(\d+)\s+->\s+(\d+)]", \
                    line) is not None:
                    match = re.search(r"^Remote\s+IP:Port\s+:\s+\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+->\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]:[(\d+)\s+->\s+(\d+)]", \
                    line)
                    port_config['remote_ip_low'] = match.group(1)
                    port_config['remote_ip_high'] = match.group(2)
                    port_config['remote_port_low'] = match.group(3)
                    port_config['remote_port_high'] = match.group(4)

                if re.search(r"^Rate\s*Open\s*:\s*(\w+)$", line) is not None:
                    match = re.search(r"^Rate\s*Open\s*:\s*(\w+)$", line)
                    port_config['rate_open'] = match.group(1)

                if re.search(r"^Rate\s*Close\s*:\s*(\w+)$", line) is not None:
                    match = re.search(r"^Rate\s*Close\s*:\s*(\w+)$", line)
                    port_config['rate_close'] = match.group(1)

                if re.search(r"^Rate\s*Send\s*:\s*(\w+)$", line) is not None:
                    match = re.search(r"^Rate\s*Send\s*:\s*(\w+)$", line)
                    port_config['rate_send'] = match.group(1)

                if re.search(r"^Delay\s+Init\s+:\s+(\w+)$", line) is not None:
                    match = re.search(r"^Delay\s+Init\s+:\s+(\w+)$", line)
                    port_config['delay_init'] = match.group(1)

                if re.search(r"^Delay\s+Uptime\s+:\s+(\w+)$", line) is not None:
                    match = re.search(r"^Delay\s+Uptime\s+:\s+(\w+)$", line)
                    port_config['delay_up'] = match.group(1)

                if re.search(r"^Delay\s+Downtime\s+:\s+(\w+)$", line) is not None:
                    match = re.search(r"^Delay\s+Downtime\s+:\s+(\w+)$", line)
                    port_config['delay_down'] = match.group(1)

                if re.search(r"^HTTP\s+(CLIENT|SERVER):$", line) is not None:
                    match = re.search(r"^HTTP\s+(CLIENT|SERVER):$", line)
                    app_host = match.group(1)
                    port_config['http'], port_config['http'][app_host], port_config['http'][app_host][tc_id] = dict(), dict(), dict()
                if re.search(r"^Request\s+Method\s+:\s+(\w+)$", line) is not None:
                    match = re.search(r"^Request\s+Method\s+:\s+(\w+)$", line)
                    port_config['http'][app_host][tc_id]['method'] = match.group(1)

                if re.search(r"^Request\s+Object\s+:\s+(.*)$", line) is not None:
                    match = re.search(r"^Request\s+Object\s+:\s+(.*)$", line)
                    port_config['http'][app_host][tc_id]['req_obj'] = match.group(1)

                if re.search(r"^Request\s+Host\s+:\s+(\w+)$", line) is not None:
                    match = re.search(r"^Request\s+Host\s+:\s+(\w+)$", line)
                    port_config['http'][app_host][tc_id]['req_host'] = match.group(1)

                if re.search(r"^Request\s+Size\s+:\s+(\w+)$", line) is not None:
                    match = re.search(r"^Request\s+Size\s+:\s+(\w+)$", line)
                    port_config['http'][app_host][tc_id]['req_size'] = match.group(1)

                if re.search(r"^Response\s+Status\s+:\s+(.*)$", line) is not None:
                    match = re.search(r"^Response\s+Status\s+:\s+(.*)$", line)
                    resp = match.group(1)
                    resp.replace(" ", "_")
                    resp.replace("-", "_").lower()
                    port_config['http'][app_host][tc_id]['resp'] = resp

                if re.search(r"^Response\s+Size\s+:\s+(.*)$", line) is not None:
                    match = re.search(r"^Response\s+Size\s+:\s+(.*)$", line)
                    port_config['http'][app_host][tc_id]['resp_size'] = match.group(1)

        print(json.dumps(port_config, indent=4))
        return port_config

    @classmethod
    def cmp_data(cls, exp_dict, act_dict, tol_val, tol_perc):
        """ this method compares expected and actual list values """
        results = 1
        result_dictionary = {}
        for key in exp_dict.keys():
            if key in act_dict.keys():
                if exp_dict[key] == act_dict[key]:
                    print('act_val= {} and exp_val= {}  are equal'.format(act_dict[key], exp_dict[key]))

                elif tol_val:
                    if int(act_dict[key]) >= (int(exp_dict[key]) - int(tol_val)) and int(act_dict[key]) <= \
                    (int(exp_dict[key]) + int(tol_val)):
                        print('act_val= {} and exp_val= {} falls in tolerence level of tolerance value {}'\
                        .format(act_dict[key], exp_dict[key], tol_val))
                        raise TypeError('comparing values failed')

                    else:
                        print('act_val= {} and exp_val={} does not fall in tolerence level of tolerance value {}'.\
                        format(act_dict[key], exp_dict[key], tol_val))
                        results &= 0
                        raise TypeError('comparing values failed')

                elif tol_perc:
                    if (int(act_dict[key])) >= (int(exp_dict[key]) - ((int(exp_dict[key])/100)*int(tol_perc)))\
                    and (int(act_dict[key])) <= (int(exp_dict[key]) + ((int(exp_dict[key])/100)*int(tol_perc))):
                        print('act_val= {} and exp_val={} falls in tolerence level of tolerance percent {}'.\
                        format(act_dict[key], exp_dict[key], tol_perc))

                    else:
                        print('act_val= {} and exp_val={} does not fall in tolerence level of tolerance percentage {}'.\
                        format(act_dict[key], exp_dict[key], tol_perc))
                        results &= 0
                        raise TypeError('Comparing values failed')

                else:
                    print('act_val= {} and exp_val= {}  are not equal'.format(act_dict[key], exp_dict[key]))
                    results &= 0
                    raise TypeError('Comparing values failed')

            else:
                print('Key {}  is not present in actual values'.format(exp_dict[key]))
            results &= 0

        result_dictionary['results'] = results
        return result_dictionary

    def get_mem_stats(self):
        """ this method provides dict with mem stats """
        print("### get memory statistics starts ###")
        mem_stat = dict()
        count = -1
        output = getattr(self.warp17_obj, 'shell')(command="show memory statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]

        for index, line in enumerate(out):
            count += 1
            if len(line) > 0:
                if  re.search(r"MBUF\s+RX:$", line) is not None:
                    mem_stat['mbuf_rx_alloc'] = re.search(r"^Total\s+Allocated:\s+(\d+)", out[index+1]).group(1)
                    mem_stat['mbuf_rx_free'] = re.search(r"^Total\s+Free\s+:\s+(\d+)", out[index+2]).group(1)

                if re.search(r"MBUF\s+TX\s+HDR:$", line) is not None:
                    mem_stat['mbuf_tx_alloc'] = re.search(r"^Total\s+Allocated:\s+(\d+)", out[index+1]).group(1)
                    mem_stat['mbuf_tx_free'] = re.search(r"^Total\s+Free\s+:\s+(\d+)", out[index+2]).group(1)

                if re.search(r"MBUF\s+CLONE:$", line) is not None:
                    match = re.search(r"^Total\s+Allocated:\s+(\d+)", out[index+1])
                    mbuf_clone_alloc = match.group(1)
                    match = re.search(r"^Total\s+Free\s+:\s+(\d+)", out[index+2])
                    mbuf_clone_free = match.group(1)
                    mem_stat['mbuf_clone_alloc'] = mbuf_clone_alloc
                    mem_stat['mbuf_clone_free'] = mbuf_clone_free

                if re.search(r"TCB:$", line) is not None:
                    match = re.search(r"^Total\s+Allocated:\s+(\d+)", out[index+1])
                    mbuf_tcb_alloc = match.group(1)
                    match = re.search(r"^Total\s+Free\s+:\s+(\d+)", out[index+2])
                    mbuf_tcb_free = match.group(1)
                    mem_stat['mbuf_tcb_alloc'] = mbuf_tcb_alloc
                    mem_stat['mbuf_tcb_free'] = mbuf_tcb_free

                if re.search(r"UCB:$", line) is not None:
                    match = re.search(r"^Total\s+Allocated:\s+(\d+)", out[index+1])
                    mbuf_ucb_alloc = match.group(1)
                    match = re.search(r"^Total\s+Free\s+:\s+(\d+)", out[index+2])
                    mbuf_ucb_free = match.group(1)
                    mem_stat['mbuf_ucb_alloc'] = mbuf_ucb_alloc
                    mem_stat['mbuf_ucb_free'] = mbuf_ucb_free

        print(json.dumps(mem_stat, indent=4))
        return mem_stat


    def get_port_link(self):
        """ This method provides dict with link stats information """
        print("### get port link stats ###")
        port_link_stat = dict()
        output = getattr(self.warp17_obj, 'shell')(command="show port link", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:
                if re.search(r"^Port\s+(\d+)\s+linkstate\s+(\w+),\s+speed\s+(\d+)Gbps,\s+duplex\s+(\w+)\(\w+\)$", line) is not None:
                    match = re.search(r"^Port\s+(\d+)\s+linkstate\s+(\w+),\s+speed\s+(\d+)Gbps,\s+duplex\s+(\w+)\(\w+\)$", line)
                    port = match.group(1)
                    port_link_stat[port] = dict()
                    port_link_stat[port]['lstate'] = match.group(2)
                    port_link_stat[port]['speed'] = match.group(3)
                    port_link_stat[port]['duplex'] = match.group(4)

        print(json.dumps(port_link_stat, indent=4))
        return port_link_stat


    def get_msg_stats(self):
        """ This method provides dict with message stats """
        print("### get msg stats ###")
        msg_stat = dict()

        output = getattr(self.warp17_obj, 'shell')(command="show msg statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:
                if re.search(r"^Messages\s+rcvd\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+rcvd\s+:\s+(\d+)$", line)
                    msg_stat['rcvd'] = match.group(1)

                if re.search(r"^Messages\s+sent\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+sent\s+:\s+(\d+)$", line)
                    msg_stat['sent'] = match.group(1)

                if re.search(r"^Messages\s+polled\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+polled\s+:\s+(\d+)$", line)
                    msg_stat['poll'] = match.group(1)

                if re.search(r"^Messages\s+errors\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+errors\s+:\s+(\d+)$", line)
                    msg_stat['err'] = match.group(1)

                if re.search(r"^Messages\s+proc\s+err\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+proc\s+err\s+:\s+(\d+)$", line)
                    msg_stat['proc_err'] = match.group(1)

                if re.search(r"^Messages\s+allocated\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+allocated\s+:\s+(\d+)$", line)
                    msg_stat['alloc'] = match.group(1)

                if re.search(r"^Messages\s+alloc\s+err\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+alloc\s+err\s+:\s+(\d+)$", line)
                    msg_stat['alloc_err'] = match.group(1)

                if re.search(r"^Messages\s+freed\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^Messages\s+freed\s+:\s+(\d+)$", line)
                    msg_stat['freed'] = match.group(1)

        print(json.dumps(msg_stat, indent=4))
        return msg_stat

    def get_port_stats(self, **kwargs):
        """ This method will provide dict with port stats """
        print("### get port stats ###")
        port_stat = dict()
        if  'port' in kwargs:
            port = kwargs.get('port')
        output = getattr(self.warp17_obj, 'shell')(command="show port statistics", pattern="warp17>").response()
        out = output.split("\n")

        for line in out:
            if len(line) > 0:
                if re.search(r"Port\s+(\d+)\s+software\s+statistics:", line) is not None:
                    match = re.search(r"Port\s+(\d+)\s+software\s+statistics:", line)
                    port = match.group(1)
                    port_stat[port] = dict()

                if re.search(r"Received\s+packets\s+:\s+(\d+)", line) is not None:
                    match = re.search(r"Received\s+packets\s+:\s+(\d+)", line)
                    port_stat[port]['rcvd_pkts'] = match.group(1)

                if re.search(r"Received\s+bytes\s+:\s+(\d+)", line) is not None:
                    match = re.search(r"Received\s+bytes\s+:\s+(\d+)", line)
                    port_stat[port]['rcvd_bytes'] = match.group(1)

                if re.search(r"Sent\s+packets\s+:\s+(\d+)", line) is not None:
                    match = re.search(r"Sent\s+packets\s+:\s+(\d+)", line)
                    port_stat[port]['sent_pkts'] = match.group(1)

                if re.search(r"Sent\s+bytes\s+:\s+(\d+)", line) is not None:
                    match = re.search(r"Sent\s+bytes\s+:\s+(\d+)", line)
                    port_stat[port]['sent_bytes'] = match.group(1)

                if re.search(r"RX\s+Ring\s+If\s+failures\s+:\s+(\d+)", line) is not None:
                    match = re.search(r"RX\s+Ring\s+If\s+failures\s+:\s+(\d+)", line)
                    port_stat[port]['rx_ring_if_fail'] = match.group(1)

                if re.search(r"Simulated\s+failures\s+:\s+(\w+)", line) is not None:
                    match = re.search(r"Simulated\s+failures\s+:\s+(\w+)", line)
                    port_stat[port]['sim_fail'] = match.group(1)

        print(json.dumps(port_stat, indent=4))
        return port_stat
        

    def get_port_state(self, **kwargs):
        """ this method will provide dict with port state """
        port_state = dict()
        if  'port' in kwargs:
            port = kwargs.get('port')
        else:
            print("Mandatory argument port is missing")
        if  'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        cmd = "show tests state port "+str(self.eth_port[port])

        output = getattr(self.warp17_obj, 'shell')(command=cmd, pattern="warp17>").response()

        key = ['tc_id', 'type', 'criteria', 'state', 'runtime', 'qk_stats']
        out = output.split("\n")
        out = [i.rstrip() for i in out]

        for line in out:
            if len(line) > 0:
                if re.search(r"^Port\s+(\d+)$", line):
                    if str(self.eth_port[port]) != re.search(r"^Port\s+(\d+)$", line).group(1):
                        print(" Unexpected port instead of "+str(self.eth_port[port]))
                        break
                if re.search(r"(\d+)\s+(\w*\s+\w*)\s+.*:\s+(\w+)\s+(\w+)\s+(.*)\s+\w+\s+\w+:\s+(\w+)$", line):
                    match = re.search(r"(\d+)\s+(\w*\s+\w*)\s+.*:\s+(\w+)\s+(\w+)\s+(.*)\s+\w+\s+\w+:\s+(\w+)$", line)
                    val = [str(match.group(3)), str(match.group(4)), str(match.group(5)), str(match.group(6))]
                    tc_id = "tc_"+str(match.group(1))
                    port_state[tc_id] = dict()
                    temp = str(match.group(2)).lower().strip()
                    val = [temp]+val
                    val = [str(match.group(1))]+val
                    j = 0
                    for k in key:
                        port_state[tc_id][k] = val[j]
                        j += 1
        print(json.dumps(port_state, indent=4))
        if tc_id is not None:
            return  port_state
        else:
            return None

    def get_test_stats(self, **kwargs):
        """ This method will provide dict with test stats """
        port_stats = dict()
        if  'port' in kwargs:
            port = kwargs.get('port')
        if  'tc_id' in kwargs:
            tc_id = kwargs.get('tc_id')
        if  tc_id and port is None:
            print("Mandatory argument port is missing")
            return
        port_stats[port] = dict()
        port_stats[port][tc_id] = dict()
        key_connextion = ['est', 'closed', 'send']
        key_msgs = ['req', 'resp', 'invl_msg', 'no_len', 'trans_enc']
        #cmd = "show tests stats port "+port+" test-case-id "+tc_id
        output = getattr(self.warp17_obj, 'shell')(command="show tests stats port "+\
                 str(self.dpdk_order["port_order"][self.dpdk_final["intf_pci_map"][port]])+" test-case-id "+tc_id, pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip() for i in out]

        for line in out:
            if len(line) > 0:
                line.strip()
                if re.search(r"^ERROR:(.*)", line) is not None:
                    match = re.search(r"^ERROR:(.*)", line)
                    print("Please verify :"+str(match.group(1)))
                if re.search(r"Port\s+(\d+),\s+Test\s+Case\s+(\d+)\s+Statistics:", line) is not None:
                    match = re.search(r"Port\s+(\d+),\s+Test\s+Case\s+(\d+)\s+Statistics:", line)
                    if port != str(match.group(1)) and tc_id != str(match.group(2)):
                        print(" Unexpected port"+str(match.group(1))+"instead of "+port+"or wrong testcase ID "+\
                        str(match.group(2))+" instead of "+tc_id)
                        return
                flag = 1
                if re.search(r"(\d+)\s+(\d+)\s+(\d+)", line) and flag == 1:
                    match = re.search(r"(\d+)\s+(\d+)\s+(\d+)", line)
                    val = [str(match.group(1)), str(match.group(1)), str(match.group(3))]
                    j = 0
                    for k in key_connextion:
                        port_stats[port][tc_id][k] = val[j]
                        j += 1
                    flag = 0
                if  re.search(r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", line) is not None:
                    match = re.search(r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
                    val = [str(match.group(1)), str(match.group(2)), str(match.group(3)), str(match.group(4)), str(match.group(5))]
                    j = 0
                    for k in key_msgs:
                        port_stats[port][tc_id][k] = val[j]
                        j += 1
                    flag = 0
        print("get_test_stats")
        print(json.dumps(port_stats, indent=4))
        return port_stats



    def get_eth_stats(self):
        """ This methos provides dict with eth stats """
        eth_stats = dict()
        cmd = "show ethernet statistics"
        output = getattr(self.warp17_obj, 'shell')(command=cmd, pattern="warp17>").response()

        out = output.split("\n")
        out = [i.rstrip() for i in out]
        for line in out:
            if len(line) > 0:
                if re.search(r"^Port\s+(\d+)\s+ethernet\s+statistics:$", line) is not None:
                    port = re.search(r"^Port\s+(\d+)\s+ethernet\s+statistics:$", line).group(1)
                    eth_stats[port] = dict()
                if re.search(r"etype\s+ARP\s+\(.*\)\s+:\s+(\d+)$", line) is not None:
                    eth_stats[port]['arp'] = re.search(r"etype\s+ARP\s+\(.*\)\s+:\s+(\d+)$", line).group(1)
                if re.search(r"etype\s+IPv4\s+\(.*\)\s+:\s+(\d+)$", line) is not None:
                    eth_stats[port]['ipv4'] = re.search(r"etype\s+IPv4\s+\(.*\)\s+:\s+(\d+)$", line).group(1)
                if re.search(r"etype\s+IPv6\s+\(.*\)\s+:\s+(\d+)$", line) is not None:
                    eth_stats[port]['ipv6'] = re.search(r"etype\s+IPv6\s+\(.*\)\s+:\s+(\d+)$", line).group(1)
                if re.search(r"^etype\s+VLAN\s+\(.*\)\s+:\s+(\d+)$", line) is not None:
                    eth_stats[port]['vlan'] = re.search(r"^etype\s+VLAN\s+\(.*\)\s+:\s+(\d+)$", line).group(1)
                if re.search(r"small\s+mbuf\s+fragment\s+:\s+(\d+)", line) is not None:
                    eth_stats[port]['mbuf_frag'] = re.search(r"small\s+mbuf\s+fragment\s+:\s+(\d+)", line).group(1)

        print("get_eth_stats")
        print(json.dumps(eth_stats, indent=4))
        return eth_stats


    def get_arp_entry(self):
        """ This method provides ARP details of ports """
        arp_entry = dict()
        cmd = "show arp entries"
        output = getattr(self.warp17_obj, 'shell')(command=cmd, pattern="warp17>").response()

        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:
                if re.search(r"^ARP\s+table\s+for\s+port\s+(\d+):$", line) is not None:
                    port = re.search(r"^ARP\s+table\s+for\s+port\s+(\d+):$", line).group(1)
                    arp_entry[port] = dict()
                if re.search(r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\s+([A-F0-9:]+)\s+(.*)\s+(.*)$",\
                    line) is not None:
                    match = re.search(r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\s+([A-F0-9:]+)\s+(.*)\s+(.*)$",\
                     line)
                    arp_entry[port][str(match.group(1))] = dict()
                    arp_entry[port][str(match.group(1))]['mac'] = match.group(6)
                    arp_entry[port][str(match.group(1))]['age'] = match.group(7)
                    arp_entry[port][str(match.group(1))]['flag'] = match.group(8)
        print("get_arp_entry")
        print(json.dumps(arp_entry, indent=4))
        return arp_entry


    def get_arp_stats(self):
        """ This method provides ARP details of ports """
        print("### get arp stats ###")
        arp_stat = dict()
        out = []

        output = getattr(self.warp17_obj, 'shell')(command="show arp statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:
                if re.search(r"Port\s+(\d+)\s+ARP\s+statistics:", line) is not None:
                    match = re.search(r"Port\s+(\d+)\s+ARP\s+statistics:", line)
                    port = match.group(1)
                    arp_stat[port] = dict()


                if re.search(r"^Received\s+Requests\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Received\s+Requests\s*:\s*(\d+)$", line)
                    arp_stat[port]['req_rcvd'] = match.group(1)

                if re.search(r"^Received\s+Replies\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Received\s+Replies\s*:\s*(\d+)$", line)
                    arp_stat[port]['resp_rcvd'] = match.group(1)

                if re.search(r"^Received\s+\"other\"\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Received\s+\"other\"\s*:\s*(\d+)$", line)
                    arp_stat[port]['other_rcvd'] = match.group(1)

                if re.search(r"^Sent\s+Requests\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Sent\s+Requests\s*:\s*(\d+)$", line)
                    arp_stat[port]['req_sent'] = match.group(1)

                if re.search(r"^Sent\s+Requests\s+Failed\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Sent\s+Requests\s+Failed\s*:\s*(\d+)$", line)
                    arp_stat[port]['req_sent_failed'] = match.group(1)

                if re.search(r"^Sent\s+Replies\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Sent\s+Replies\s*:\s*(\d+)$", line)
                    arp_stat[port]['resp_sent'] = match.group(1)

                if re.search(r"^Sent\s+Replies\s+Failed\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Sent\s+Replies\s+Failed\s*:\s*(\d+)$", line)
                    arp_stat[port]['resp_sent_failed'] = match.group(1)

                if re.search(r"^Request\s+not\s+mine\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Request\s+not\s+mine\s*:\s*(\d+)$", line)
                    arp_stat[port]['req_not_mine'] = match.group(1)

                if re.search(r"^Small\s+mbuf\s+fragment\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Small\s+mbuf\s+fragment\s*:\s*(\d+)$", line)
                    arp_stat[port]['mbuf_frag'] = match.group(1)

                if re.search(r"^Invalid\s+hw\s+space\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Invalid\s+hw\s+space\s*:\s*(\d+)$", line)
                    arp_stat[port]['invalid_hw_space'] = match.group(1)

                if re.search(r"^Invalid\s+hw\s+length\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Invalid\s+hw\s+length\s*:\s*(\d+)$", line)
                    arp_stat[port]['invalid_hw_length'] = match.group(1)

                if re.search(r"^Invalid\s+proto\s+space\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Invalid\s+proto\s+space\s*:\s*(\d+)$", line)
                    arp_stat[port]['invalid_proto_space'] = match.group(1)

                if re.search(r"^Invalid\s+proto\s+length\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Invalid\s+proto\s+length\s*:\s*(\d+)$", line)
                    arp_stat[port]['invalid_proto_length'] = match.group(1)

        #print(json.dumps(arp_stat, indent=4))
        return arp_stat


    def get_route_stats(self, **kwargs):
        """ This method is to get routes stats of warp ports """
        print("### get route stats ###")
        route_stats = dict()
        if  'port' in kwargs:
            port = kwargs.get('port')

        output = getattr(self.warp17_obj, 'shell')(command="show route statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:

                if re.search(r"^Port\s+(\d+)\s+Route\s+statistics:$", line) is not None:
                    match = re.search(r"^Port\s+(\d+)\s+Route\s+statistics:$", line)
                    port = match.group(1)
                    route_stats[port] = dict()

                if re.search(r"^Intf\s*Add\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Intf\s*Add\s*:\s*(\d+)$", line)
                    route_stats[port]['intf_add'] = match.group(1)

                if re.search(r"^Intf\s+Del\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Intf\s+Del\s*:\s*(\d+)$", line)
                    route_stats[port]['intf_del'] = match.group(1)

                if re.search(r"^Gw\s+Add\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Gw\s+Add\s*:\s*(\d+)$", line)
                    route_stats[port]['gw_add'] = match.group(1)

                if re.search(r"^Gw\s+Del\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Gw\s+Del\s*:\s*(\d+)$", line)
                    route_stats[port]['gw_del'] = match.group(1)

                if re.search(r"^Route\s+Tbl\s+Full\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Route\s+Tbl\s+Full\s*:\s*(\d+)$", line)
                    route_stats[port]['route_tbl_full'] = match.group(1)

                if re.search(r"^Intf\s+No\s+Mem\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Intf\s+No\s+Mem\s*:\s*(\d+)$", line)
                    route_stats[port]['intf_no_mem'] = match.group(1)

                if re.search(r"^Intf\s+Not\s+Found\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Intf\s+Not\s+Found\s*:\s*(\d+)$", line)
                    route_stats[port]['intf_not_found'] = match.group(1)

                if re.search(r"^Gw\s+Intf\s+Not\s+Found\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Gw\s+Intf\s+Not\s+Found\s*:\s*(\d+)$", line)
                    route_stats[port]['gw_intf_not_found'] = match.group(1)

                if re.search(r"^NH\s+not\s+found\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^NH\s+not\s+found\s*:\s*(\d+)$", line)
                    route_stats[port]['nh_not_found'] = match.group(1)

                if re.search(r"^Route\s+not\s+found\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Route\s+not\s+found\s*:\s*(\d+)$", line)
                    route_stats[port]['route_not_found'] = match.group(1)

        print(json.dumps(route_stats, indent=4))
        return route_stats


    def get_tcp_stats(self):
        """ This method provide dict of tcp stats of ports """
        print("### get tcp stats ###")
        tcp_stat = dict()
        #if  'port' in kwargs:
         #   self.port = kwargs.get('port')

        output = getattr(self.warp17_obj, 'shell')(command="show tcp statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:
                if re.search(r"Port\s+(\d+)\s+TCP\s+statistics:", line) is not None:
                    match = re.search(r"^Port\s+(\d+)\s+TCP\s+statistics:$", line)
                    port = match.group(1)
                    tcp_stat[port] = dict()

                if re.search(r"Received\s*Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*Packets\s*:\s*(\d+)", line)
                    tcp_stat[port]['rcvd_pkts'] = match.group(1)

                if re.search(r"Received\s*Bytes\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*Bytes\s*:\s*(\d+)", line)
                    tcp_stat[port]['rcvd_bytes'] = match.group(1)

                if re.search(r"Sent\s+Ctrl\s+Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Ctrl\s+Packets\s*:\s*(\d+)", line)
                    tcp_stat[port]['sent_ctrl_pkts'] = match.group(1)

                if re.search(r"Sent\s+Ctrl\s+Bytes\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Ctrl\s+Bytes\s*:\s*(\d+)", line)
                    tcp_stat[port]['sent_ctrl_bytes'] = match.group(1)

                if re.search(r"Sent\s+Data\s+Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Data\s+Packets\s*:\s*(\d+)", line)
                    tcp_stat[port]['sent_data_pkts'] = match.group(1)

                if re.search(r"Sent\s+Data\s+Bytes\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Data\s+Bytes\s*:\s*(\d+)", line)
                    tcp_stat[port]['sent_data_bytes'] = match.group(1)

                if re.search(r"Malloced\s+TCBs\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Malloced\s+TCBs\s*:\s*(\d+)", line)
                    tcp_stat[port]['mal_tcbs'] = match.group(1)

                if re.search(r"Freed\s+TCBs\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Freed\s+TCBs\s*:\s*(\d+)", line)
                    tcp_stat[port]['free_tcbs'] = match.group(1)

                if re.search(r"Not\s+found\s+TCBs\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Not\s+found\s+TCBs\s*:\s*(\d+)", line)
                    tcp_stat[port]['not_found_tcbs'] = match.group(1)

                if re.search(r"TCB\s+alloc\s+errors\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"TCB\s+alloc\s+errors\s*:\s*(\d+)", line)
                    tcp_stat[port]['tcb_alloc_err'] = match.group(1)

                if re.search(r"Invalid\s+checksum\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Invalid\s+checksum\s*:\s*(\d+)", line)
                    tcp_stat[port]['invl_csum'] = match.group(1)

                if re.search(r"Small\s+mbuf\s+fragment\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Small\s+mbuf\s+fragment\s*:\s*(\d+)", line)
                    tcp_stat[port]['small_mbuf_frag'] = match.group(1)

                if re.search(r"TCP hdr\s+\w+\s+small\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"TCP hdr\s+\w+\s+small\s*:\s*(\d+)", line)
                    tcp_stat[port]['tcp_hdr_too_small'] = match.group(1)

                if re.search(r"Ctrl\s+Failed\s+Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Ctrl\s+Failed\s+Packets\s*:\s*(\d+)", line)
                    tcp_stat[port]['ctrl_failed_pkts'] = match.group(1)

                if re.search(r"DATA\s+Failed\s+Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"DATA\s+Failed\s+Packets\s*:\s*(\d+)", line)
                    tcp_stat[port]['data_failed_pkts'] = match.group(1)

                if re.search(r"DATA\s+Clone\s+Failed\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"DATA\s+Clone\s+Failed\s*:\s*(\d+)", line)
                    tcp_stat[port]['data_clone_failed'] = match.group(1)

                if re.search(r"Reserved\s+bit\s+set\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Reserved\s+bit\s+set\s*:\s*(\d+)", line)
                    tcp_stat[port]['resv_bit_set'] = match.group(1)

                if re.search(r"Freed\s+TCBs\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Freed\s+TCBs\s*:\s*(\d+)", line)
                    tcp_stat[port]['freed_tcbs'] = match.group(1)

        print(json.dumps(tcp_stat, indent=4))
        return tcp_stat


    def get_udp_stats(self):
        """ This method provides dict of udp stats of ports """
        print("### get udp stats ###")
        udp_stat = dict()
        output = getattr(self.warp17_obj, 'shell')(command="show udp statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:

                if re.search(r"Port\s+(\d+)\s+UDP\s+statistics:", line) is not None:
                    match = re.search(r"Port\s+(\d+)\s+UDP\s+statistics:", line)
                    port = match.group(1)
                    udp_stat[port] = dict()

                if re.search(r"Received\s*Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*Packets\s*:\s*(\d+)", line)
                    udp_stat[port]['rcvd_pkts'] = match.group(1)

                if re.search(r"Received\s*Bytes\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Received\s*Bytes\s*:\s*(\d+)", line)
                    udp_stat[port]['rcvd_bytes'] = match.group(1)

                if re.search(r"Sent\s+Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Packets\s*:\s*(\d+)", line)
                    udp_stat[port]['sent_pkts'] = match.group(1)

                if re.search(r"Sent\s+Bytes\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Bytes\s*:\s*(\d+)", line)
                    udp_stat[port]['sent_bytes'] = match.group(1)

                if re.search(r"Sent\s+Data\s+Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Data\s+Packets\s*:\s*(\d+)", line)
                    udp_stat[port]['sent_data_pkts'] = match.group(1)

                if re.search(r"Sent\s+Data\s+Bytes\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Sent\s+Data\s+Bytes\s*:\s*(\d+)", line)
                    udp_stat[port]['sent_data_bytes'] = match.group(1)

                if re.search(r"Malloced\s+UCBs\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Malloced\s+UCBs\s*:\s*(\d+)", line)
                    udp_stat[port]['free_ucbs'] = match.group(1)

                if re.search(r"Freed\s+UCBs\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Freed\s+UCBs\s*:\s*(\d+)", line)
                    udp_stat[port]['free_ucbs'] = match.group(1)

                if re.search(r"Not\s+found\s+UCBs\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Not\s+found\s+UCBs\s*:\s*(\d+)", line)
                    udp_stat[port]['not_found_ucbs'] = match.group(1)

                if re.search(r"UCB\s+alloc\s+errors\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"UCB\s+alloc\s+errors\s*:\s*(\d+)", line)
                    udp_stat[port]['ucb_alloc_err'] = match.group(1)

                if re.search(r"Invalid\s+checksum\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Invalid\s+checksum\s*:\s*(\d+)", line)
                    udp_stat[port]['invl_csum'] = match.group(1)

                if re.search(r"Small\s+mbuf\s+fragment\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Small\s+mbuf\s+fragment\s*:\s*(\d+)", line)
                    udp_stat[port]['small_mbuf_frag'] = match.group(1)

                if re.search(r"Failed\s+Packets\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"Failed\s+Packets\s*:\s*(\d+)", line)
                    udp_stat[port]['failed_pkts'] = match.group(1)

        print(json.dumps(udp_stat, indent=4))
        return udp_stat
        

    def get_tsm_stats(self):
        """ This method provides dict with tsm stats """
        print("### get tsm stats ###")
        tsm_stats = dict()
        output = getattr(self.warp17_obj, 'shell')(command="show tsm statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:

            if len(line) > 0:
                if re.search(r"^Port\s+(\d+)\s+TSM\s+statistics:$", line) is not None:
                    match = re.search(r"^Port\s+(\d+)\s+TSM\s+statistics:$", line)
                    port = match.group(1)
                    tsm_stats[port] = dict()

                if re.search(r"^INIT\s+:\s+(\d+)$", line) is not None:
                    match = re.search(r"^INIT\s+:\s+(\d+)$", line)
                    tsm_stats[port]['init'] = match.group(1)

                if re.search(r"^LISTEN\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^LISTEN\s*:\s*(\d+)$", line)
                    tsm_stats[port]['listen'] = match.group(1)

                if re.search(r"^SYN_SENT\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^SYN_SENT\s*:\s*(\d+)$", line)
                    tsm_stats[port]['syn_sent'] = match.group(1)

                if re.search(r"^SYN_RECV\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^SYN_RECV\s*:\s*(\d+)$", line)
                    tsm_stats[port]['syn_rcvd'] = match.group(1)

                if re.search(r"^ESTAB\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^ESTAB\s*:\s*(\d+)$", line)
                    tsm_stats[port]['estab'] = match.group(1)

                if re.search(r"^FIN_WAIT_1\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^FIN_WAIT_1\s*:\s*(\d+)$", line)
                    tsm_stats[port]['fin_wait1'] = match.group(1)

                if re.search(r"^FIN_WAIT_2\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^FIN_WAIT_2\s*:\s*(\d+)$", line)
                    tsm_stats[port]['fin_wait2'] = match.group(1)

                if re.search(r"^LAST_ACK\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^LAST_ACK\s*:\s*(\d+)$", line)
                    tsm_stats[port]['last_ack'] = match.group(1)

                if re.search(r"^CLOSING\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^CLOSING\s*:\s*(\d+)$", line)
                    tsm_stats[port]['closing'] = match.group(1)

                if re.search(r"^TIME_WAIT\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^TIME_WAIT\s*:\s*(\d+)$", line)
                    tsm_stats[port]['time_wait'] = match.group(1)

                if re.search(r"^CLOSE_WAIT\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^CLOSE_WAIT\s*:\s*(\d+)$", line)
                    tsm_stats[port]['close_wait'] = match.group(1)

                if re.search(r"^CLOSED\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^CLOSED\s*:\s*(\d+)$", line)
                    tsm_stats[port]['closed'] = match.group(1)

                if re.search(r"^SYN\s+retrans\s+TO\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^SYN\s+retrans\s+TO\s*:\s*(\d+)$", line)
                    tsm_stats[port]['syn_retrans_to'] = match.group(1)

                if re.search(r"^SYN\/ACK\s+retrans\s+TO\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^SYN\/ACK\s+retrans\s+TO\s*:\s*(\d+)$", line)
                    tsm_stats[port]['synack_retrans_to'] = match.group(1)

                if re.search(r"^Retrans\s+TO\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Retrans\s+TO\s*:\s*(\d+)$", line)
                    tsm_stats[port]['retrans_to'] = match.group(1)

                if re.search(r"^Retrans\s+bytes\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Retrans\s+bytes\s*:\s*(\d+)$", line)
                    tsm_stats[port]['retrans_bytes'] = match.group(1)

                if re.search(r"^Missing\s+seq\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^Missing\s+seq\s*:\s*(\d+)$", line)
                    tsm_stats[port]['miss_seq'] = match.group(1)

                if re.search(r"^SND\s+win\s+full\s*:\s*(\d+)$", line) is not None:
                    match = re.search(r"^SND\s+win\s+full\s*:\s*(\d+)$", line)
                    tsm_stats[port]['snd_win_full'] = match.group(1)

        print(json.dumps(tsm_stats, indent=4))
        return tsm_stats



    def get_http_stats(self):
        """ This method provides http stats """
        print("### get http stats ###")
        http_stats = dict()
        output = getattr(self.warp17_obj, 'shell')(command="show http statistics", pattern="warp17>").response()
        out = output.split("\n")
        out = [i.rstrip().strip() for i in out]
        for line in out:
            if len(line) > 0:
                if re.search(r"Port\s+(\d+)\s+HTTP\s+statistics:", line) is not None:
                    match = re.search(r"Port\s+(\d+)\s+HTTP\s+statistics:", line)
                    port = match.group(1)
                    http_stats[port] = dict()
                    print(port)
                if re.search(r"HTTP\s+Req\s+Build\s+Err\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"HTTP\s+Req\s+Build\s+Err\s*:\s*(\d+)", line)
                    http_stats[port]['req_err'] = match.group(1)

                if re.search(r"HTTP\s+Resp\s+Build\s+Err\s*:\s*(\d+)", line) is not None:
                    match = re.search(r"HTTP\s+Resp\s+Build\s+Err\s*:\s*(\d+)", line)
                    http_stats[port]['resp_err'] = match.group(1)

        print(json.dumps(http_stats, indent=4))
        return http_stats



######################################################################################
# Name       : calc_cpu_cores
# Description: Calculates cpu cores and NUMA node, which can be used to determine how many cores WARP17 should use.
######################################################################################


    def calc_cpu_cores(self):
        """
        :Desciption: Method called by user to Calculates cpu cores and NUMA node, which can be used to determine how many cores WARP17 should use
        :Arguments: No Arguments required
        :return: a Dictionary which contains data about cpu cores
        """
        lscpu = []
        lscpu_data = dict()
        lscpu_output = getattr(self.warp17_obj, 'shell')(command="lscpu").response()
        lscpu_detail = lscpu_output.split("\n")
        for i in lscpu_detail:
            lscpu.append(i.rstrip("\r"))
        for line in lscpu:
            if len(line) > 0:
                if re.search(r"Architecture:\s+(\w+)", line) is not None:
                    arch = re.search(r"Architecture:\s+(\w+)", line)
                    lscpu_data.update(Arch=arch.group(1))

                if re.search(r"^CPU\s*op-mode\(s\):\s*(.*)", line) is not None:
                    mode = re.search(r"^CPU\s*op-mode\(s\):\s*(.*)", line)
                    lscpu_data.update(cpu_op_mode=mode.group(1))

                if  re.search(r"^Byte\s*Order:\s*(.*)", line) is not None:
                    byte = re.search(r"^Byte\s*Order:\s*(.*)", line)
                    lscpu_data.update(byte_order=byte.group(1))

                if  re.search(r"^CPU\(s\):\s*(\d+)", line) is not None:
                    cpu = re.search(r"^CPU\(s\):\s*(\d+)", line)
                    lscpu_data.update(num_of_cpus=cpu.group(1))

                if  re.search(r"^On-line\s*CPU.*list:\s*(\w+)", line) is not None:
                    online = re.search(r"^On-line\s*CPU.*list:\s*(\w+)", line)
                    lscpu_data.update(online_cpus=online.group(1))

                if  re.search(r"^Thread\(s\)\s*per\s*core:\s*(\d+)", line) is not None:
                    thread = re.search(r"^Thread\(s\)\s*per\s*core:\s*(\d+)", line)
                    lscpu_data.update(thread_per_core=thread.group(1))

                if re.search(r"^Core\(s\)\s*per\s*socket:\s*(\d+)", line) is not None:
                    core = re.search(r"^Core\(s\)\s*per\s*socket:\s*(\d+)", line)
                    lscpu_data.update(core_per_sock=core.group(1))

                if re.search(r"^Socket\(s\):\s*(\d+)", line) is not None:
                    socket = re.search(r"^Socket\(s\):\s*(\d+)", line)
                    lscpu_data.update(sock_total=socket.group(1))

                if re.search(r"^NUMA\s*node\(s\):\s*(\d+)", line) is not None:
                    node = re.search(r"^NUMA\s*node\(s\):\s*(\d+)", line)
                    lscpu_data['numa_node'] = dict()
                    lscpu_data['numa_node']['total_numa_node'] = node.group(1)

                if re.search(r"^Vendor\s*ID:\s*(\w+)", line) is not None:
                    vendor = re.search(r"^Vendor\s*ID:\s*(\w+)", line)
                    lscpu_data.update(vendor=vendor.group(1))

                if re.search(r"^CPU\s*family:\s*(.*)", line) is not None:
                    family = re.search(r"^CPU\s*family:\s*(.*)", line)
                    lscpu_data.update(cpu_family=family.group(1))

                if re.search(r"^Model:\s*(.*)", line) is not None:
                    model = re.search(r"^Model:\s*(.*)", line)
                    lscpu_data.update(model=model.group(1))

                if re.search(r"^Stepping:\s*(.*)", line) is not None:
                    step = re.search(r"^Stepping:\s*(.*)", line)
                    lscpu_data.update(stepping=step.group(1))

                if re.search(r"^CPU\s*MHz:\s*(.*)", line) is not None:
                    cpu = re.search(r"^CPU\s*MHz:\s*(.*)", line)
                    lscpu_data.update(cpu_mhz=cpu.group(1))

                if re.search(r"^BogoMIPS:\s*(.*)", line) is not None:
                    bogo = re.search(r"^BogoMIPS:\s*(.*)", line)
                    lscpu_data.update(bogomips=bogo.group(1))

                if re.search(r"^Virtualization:\s*(.*)", line) is not None:
                    virt = re.search(r"^Virtualization:\s*(.*)", line)
                    lscpu_data.update(virtual=virt.group(1))

                if re.search(r"^L1d\s*cache:\s*(.*)", line) is not None:
                    cache = re.search(r"^L1d\s*cache:\s*(.*)", line)
                    lscpu_data.update(l1d_cache=cache.group(1))

                if re.search(r"^NUMA\s*node(\d*)\s*CPU\(s\):\s*(.*)", line) is not None:
                    core = []
                    match = re.search(r"^NUMA\s*node(\d*)\s*CPU\(s\):\s*(.*)", line)
                    numa_node = match.group(1)
                    index_low_high = match.group(2)
                    print("NUMA node = "+numa_node+" , Bit index  = "+index_low_high+" \n")
                    core_range = index_low_high.split(',')
                    for each_core in core_range:
                        if re.search(r"-", each_core) is not None:
                            core_temp = each_core.split('-')
                            while int(core_temp[0]) <= int(core_temp[1]):
                                core.append(core_temp[0])
                                core_temp[0] = int(core_temp[0]) + 1
                    lscpu_data['numa_node'][numa_node] = dict()
                    lscpu_data['numa_node'][numa_node]['cpu_core'] = core

        print("LSCPU data on WARP17 box : "+json.dumps(lscpu_data))
        return  lscpu_data

################################################################################
# Name       : warp17_cfg
# Description: Loads cli commands on to the warp17
################################################################################

    def warp17_cfg(self, **kwargs):
        """
        Method called by user to Loads cli commands on to the warp17
        :Arguments: dst_path is the path where config file is being loaded
        :return: True if scp is is successful
        """
        host = kwargs.get('host', self.warp17_obj)
        dst_path = kwargs.get('dst_path', '/root/WARP17/')
        #dst_path = kwargs.get('dst_path', '/root/WARP17/warp17-master/')
        #pattern = kwargs.get('pattern', '.*')
        #timeout = kwargs.get('timeout', 60)
        uname = kwargs.get('uname', 'root')
        password = kwargs.get('pw', 'Embe1mpls')
        cmdlist = kwargs.get('cmdlist')
        src_path = kwargs.get('src_path')

        if cmdlist is not None:
            cfg_file_name = kwargs.get('cfg_file_name', 'warp17_cfg.txt')
            filehandle = open(cfg_file_name, 'w+')
            cmdlist = cmdlist.split("\n")
            for cmd in cmdlist:
                filehandle.write(cmd)
                filehandle.write("\n")
            filehandle.close()

        if src_path is not None:
            outfile = src_path+'/'+cfg_file_name

        self.scp(server_name=host, src_path=outfile, dst_path=dst_path, uname=uname, password=password)
        getattr(host, 'shell')(command="chmod 777  "+dst_path+"/"+cfg_file_name)



######################################################################################
# Name       : _scp
# Description: sends files to WARP17 using SCP.
######################################################################################
    def scp(self, **kwargs):
        """ this method is to trasfer files between servers """
        src_path = kwargs.get('src_path', '/volume/testtech-jt-scripts/Testsuites/Infrastructure/GSP/Sparks/WARP17')
        dst_path = kwargs.get('dst_path', '/root/WARP17/')
        #dst_path = kwargs.get('dst_path', '/root/WARP17/warp17-master')
        uname = kwargs.get('uname', 'root')
        password = kwargs.get('pw', 'Embe1mpls')
        expect_obj = pexpect.spawn("scp -o \"StrictHostKeyChecking no\" "+src_path+" "+uname+"@"+self.server_name+":"+dst_path)
        expect_obj.expect([pexpect.TIMEOUT, '.*password:'])
        expect_obj.sendline(password)
        expect_obj.expect(pexpect.EOF, timeout=10)
        return True



######################################################################################
# Name       : dpdk_status
# Description: Returns a hash of the Network devices using drivers
######################################################################################
    def get_dpdk_status(self):
        """ This method provides dict with port to intf bindings """

        dpdk_status = dict()
        dpdk_status['dpdk_pci_inuse'] = dict()
        dpdk_status['intf_pci_map'] = dict()
        dpdk_status['dpdk_driver_others'] = dict()
        dpdk_status['intf_drv'] = dict()
        dpdk_status['pci_intf_map'] = dict()
        dpdk_status['port_order'] = dict()
        skip_mgmt_port = []
        dpdk_dev_bind_path = '/usr/local/share/dpdk/tools/dpdk-devbind.py'

        skip_mgmt_port.append('eth0')
        uniq = dict()
        output = getattr(self.warp17_obj, 'shell')(command=dpdk_dev_bind_path+" --status").response()
        dpdk_dev_bind_status = output.split("\n")
        line_cnt = len(dpdk_dev_bind_status)

        for pci_cnt in  range(0, line_cnt):

            if len(dpdk_dev_bind_status[pci_cnt]) > 0:

                for skip in skip_mgmt_port:

                    if re.search(r"(\w+:\w+:\w+\.\w+)\s*\'.*\'\s*if="+skip, dpdk_dev_bind_status[pci_cnt]) is not None:
                        break
                if re.search(r"Network\s*devices\s*using\s*DPDK.compatible\s*driver", dpdk_dev_bind_status[pci_cnt]) is not None:

                    pci_cnt += 2
                    if re.search(r"<none>", dpdk_dev_bind_status[pci_cnt]) is not None:
                        #print("No interface is binded in dpdk space")
                        pci_cnt = pci_cnt+2
                    i = 0

                    while re.search(r"(\w+:\w+:\w+\.\w+)\s*\'.*\'\s*drv=igb_uio unused=", dpdk_dev_bind_status[pci_cnt+i]) is not None:
                        match = re.search(r"(\w+:\w+:\w+\.\w+)\s*\'.*\'\s*drv=igb_uio unused=", dpdk_dev_bind_status[pci_cnt+i])
                        dpdk_status['dpdk_pci_inuse'][i] = match.group(1)
                        dpdk_status['port_order'][match.group(1)] = i
                        i += 1
                if re.search(r"Network\s*devices\s*using\s*kernel\s*driver", dpdk_dev_bind_status[pci_cnt]) is not None:
                    pci_cnt += 2
                    i = 0
                    while re.search(r"(\w+:\w+:\w+\.\w+)\s*\'.*\'\s*if=(\w+)\s*drv=(\w+)\s*unused=igb_uio?", \
                        dpdk_dev_bind_status[pci_cnt+i]) is not None:
                        match = re.search(r"(\w+:\w+:\w+\.\w+)\s*\'.*\'\s*if=(\w+)\s*drv=(\w+)\s*unused=igb_uio?", dpdk_dev_bind_status[pci_cnt+i])
                        dpdk_status['intf_pci_map'][match.group(2)] = match.group(1)
                        uniq[match.group(3)] = i
                        i += 1
                    pci_cnt += i
                if re.search(r"Other\s*network\s*devices", dpdk_dev_bind_status[pci_cnt]) is not None:
                    pci_cnt = pci_cnt + 2
                    if re.search(r"<none>", dpdk_dev_bind_status[pci_cnt]) is not None:
                        #print("No interface is binded in other network space")
                        pci_cnt = pci_cnt+2

                    i = 0
                    while re.search(r"(\w+:\w+:\w+\.\w+)\s*\'.*\'.*", dpdk_dev_bind_status[pci_cnt+i]) is not None:
                        match = re.search(r"(\w+:\w+:\w+\.\w+)\s*\'.*\'.*", dpdk_dev_bind_status[pci_cnt+i])
                        dpdk_status['dpdk_driver_others'][i] = match.group(1)
                        i += 1
                    pci_cnt += i
                i = 0
                for key in uniq:
                    dpdk_status['intf_drv'][i] = key
                    i += 1


        dpdk_status['dpdk_dev_bind_path'] = dpdk_dev_bind_path

        dpdk_status['pci_intf_map'] = {v: k for k, v in dpdk_status['intf_pci_map'].items()}
        return dpdk_status



######################################################################################
# Name       : dpdk_unbind
# Description: unbinds eth interfaces before the start of warp process
######################################################################################


    def dpdk_unbind(self):
        """ This method unbinds dpdk bindings """
        new_list = []
        print(self.dpdk_status['dpdk_driver_inuse'])
        print(type(self.dpdk_status['dpdk_driver_inuse']))
        for val in self.dpdk_status['dpdk_driver_inuse'].values():
            new_list.append(val)
        for address in new_list:
            output = getattr(self.warp17_obj, 'shell')(command=self.dpdk_status['dpdk_dev_bind_path']+" --bind=i40e "+address).response()
            if output is None:
                print("Successfully Unbinded"+"\n")
            else:
                print("Could not Unbind port"+"\n")


######################################################################################
# Name       : setup_dpdk
# Description: Sets up DPDK (binds/unbinds eth interfaces, re-installs DPDK)
######################################################################################

    def setup_dpdk(self):

        """
        Method called by user to Sets up DPDK (binds/unbinds eth interfaces, re-installs DPDK)
        :Arguments: options_dpdk is a list which contains data of total_eth_port and dpdk_src_path
        eth_if=set of interfaces
        bind=bind type
        re_install_dpdk=flag which decides whether to reinstall dpdk or not
        :return: a dictionaty dpdk_status which contains details of all ethernet to driver mappings.
            In all other cases Exception is raised
        """
        pci_drv_map = dict()
        if self.eth_if:
            eth_if = self.eth_if
        else:
            print("Mandatory Argument Eth If is missing\n")

        if self.bind:
            bind = self.bind

        #all_drv_path = '/sys/bus/pci/drivers/'

        if self.unbind:
            unbind = self.unbind

        self.dpdk_status, result = dict(), True

        for inf in self.eth_if:
            getattr(self.warp17_obj, 'shell')(command="ifconfig "+inf+" 0")
            getattr(self.warp17_obj, 'shell')(command="ifconfig "+inf+" down")

        print("An error may occure above and quite expected if the interfaces are not on kernel space,\
         please ignore the error, its no problem :) !!!\n")

        print("DPDK status before un-binding\n")
        dpdk_status = self.get_dpdk_status()
        dpdk_dev_bind_path = dpdk_status['dpdk_dev_bind_path']

        if dpdk_status['intf_drv']:
            for key, value in dpdk_status['intf_drv'].items():
                unbind.append(value)

        uniq = dict()
        for key in unbind:
            uniq[key] = "dummy"

        dpdk_intf_driver_inuse, other_intf_driver_inuse = unbind, unbind

        print("All Interface driver used for un-binding are = "+str(unbind)+"\n")
        drv_cnt = -1
        for un_driver in unbind:
            drv_cnt += 1
            pci_cnt = -1
            dpdk_status = self.get_dpdk_status()
            for key in dpdk_status['dpdk_pci_inuse']:
                pci_cnt += 1
                pci_inuse = dpdk_status['dpdk_pci_inuse'][key]
                print(" pci_inuse on DPDK = "+str(pci_inuse)+" Count = "+str(key)+" !!!\n")
                output = None
                if dpdk_status['dpdk_pci_inuse'][key]:
                    test_res = getattr(self.warp17_obj, 'shell')(command=dpdk_dev_bind_path+" -b "+un_driver+" "+pci_inuse)
                    output = test_res.response()
                    #output = self.warp17_obj.shell(command=dpdk_dev_bind_path+" -b "+un_driver+" "+pci_inuse).response()
                    out = output.split("\n")

                for line in out:
                    number_of_lines = len(out)

                    print("\n\n\n number_of_lines : "+str(number_of_lines)+" , line = "+line+"  \n")
                    if re.search(dpdk_dev_bind_path, line) is not None and number_of_lines == 1:
                        pci_drv_map[pci_inuse] = unbind[drv_cnt]
                        print("Driver number = "+drv_cnt+", pci_inuse = "+pci_inuse+", "+"driver name = "+unbind[drv_cnt]+"\n")
                    if len(line) == 0:
                        print(pci_inuse+" is successfully unbinded !!!\n")
                        pci_drv_map[pci_inuse] = unbind[key]
                    elif re.search(r"already\s*bound\s*to\s*driver.*skipping", line):
                        print("pci_inuse is successfully unbinded !!!\n")
                        pci_drv_map[pci_inuse] = unbind[key]
                    elif re.search(r".*Error:.*", line):
                        print(pci_inuse +"un-bind failed, driver not found yet, look for the next one !!!\n")
                        i = 0
                        for match in dpdk_intf_driver_inuse:
                            if match == un_driver:
                                dpdk_intf_driver_inuse.remove(un_driver)
                            i += 1
                        continue
                    else:
                        print("pci_inuse un-bind successfull !!!\n")
                        continue

        print("Found the kernel drivers for the PCIs on DPDK: \n"+ json.dumps(pci_drv_map, indent=4))
        drv_cnt = -1
        for un_driver in unbind:
            drv_cnt += 1
            pci_cnt = -1
            dpdk_status = self.get_dpdk_status()
            for key in dpdk_status['dpdk_driver_others']:
                pci_cnt += 1
                pci_inuse = dpdk_status['dpdk_driver_others'][key]
                print("pci_inuse on other = "+pci_inuse+" Count = "+str(key)+" !!!\n")
                output = None
                if dpdk_status['dpdk_driver_others'][key]:
                    #output = self.warp17_obj.shell(command=dpdk_dev_bind_path+" -b "+un_driver+" "+pci_inuse).response()
                    output = getattr(self.warp17_obj, 'shell')(command=dpdk_dev_bind_path+" -b "+un_driver+" "+pci_inuse).response()
                    out = output.split("\n")
                for line in out:
                    number_of_lines = len(line)
                    print("\n\n\n number_of_lines : "+str(number_of_lines)+" , line = "+str(line)+" \n")
                    if re.search(r"dpdk_dev_bind_path", line) is not None and number_of_lines == 1:
                        pci_drv_map[pci_inuse] = unbind[drv_cnt]
                        print("\n\n\n$sub: Driver number = "+drv_cnt+", pci_inuse = "+pci_inuse+", driver name = "+unbind[drv_cnt]+"\n")
                    if len(line) == 0:
                        print(pci_inuse+" is successfully unbinded !!!\n")
                        pci_drv_map[pci_inuse] = unbind[key]
                    elif re.search(r"already\s*bound\s*to\s*driver.*skipping", line):
                        print(pci_inuse+" is successfully unbinded !!!\n")
                        pci_drv_map[pci_inuse] = unbind[key]
                    elif re.search(r".*Error:.*", line):
                        print(pci_inuse+" un-bind failed, driver not found yet, look for the next one !!!\n")
                        i = 0
                        for match in other_intf_driver_inuse:
                            if match == un_driver:
                                other_intf_driver_inuse.remove(un_driver)
                            i += 1
                        continue
                    else:
                        print(pci_inuse+" un-bind successfull !!!\n")
                        continue

        print("Found the kernel drivers for PCIs on Others: \n"+ json.dumps(pci_drv_map, indent=4))

        pci_cnt = 0
        for key in dpdk_status['dpdk_pci_inuse']:
            if dpdk_status['dpdk_pci_inuse'][key]:
                getattr(self.warp17_obj, 'shell')(command=dpdk_dev_bind_path+" -b "+pci_drv_map[dpdk_status['dpdk_pci_inuse'][key]]+\
                "  "+dpdk_status['dpdk_pci_inuse'][key]).response()
        pci_cnt = 0
        for key in dpdk_status['dpdk_driver_others']:
            if dpdk_status['dpdk_driver_others'][key]:
                getattr(self.warp17_obj, 'shell')(command=dpdk_dev_bind_path+" -b "+pci_drv_map[dpdk_status['dpdk_driver_others'][key]]+\
                "  "+dpdk_status['dpdk_driver_others'][key]).response()
                pci_cnt += 1

        self.eth_port = dict()
        print("The interfaces"+str(self.eth_if)+" will have below set of port numbers which can be used as Client or Server\n"+\
        json.dumps(self.eth_port, indent=4))
        print("At this point, All the interface driver on DPDK and Others are brought back to Kernel And also the interface driver are known\n")
        dpdk_status = self.get_dpdk_status()
        self.dpdk_final = self.get_dpdk_status()

        pci_before_sort = []
        pci_after_sort = []
        for eth_intf in eth_if:
            if dpdk_status['intf_pci_map'][eth_intf]:
                pci_before_sort.append(dpdk_status['intf_pci_map'][eth_intf])
            else:
                pci_before_sort.append(dpdk_status['intf_pci_map'][eth_intf])
        pci_before_sort.sort()
        pci_after_sort = pci_before_sort
        port_count = 0

        print("All eth_if = "+str(self.eth_if)+",  pci_before_sort="+str(pci_before_sort)+", pci_after_sort= "+str(pci_after_sort)+"\n")

        for pci in pci_after_sort:
            intf = dpdk_status['pci_intf_map'][pci]
            self.eth_port[intf] = port_count
            port_count += 1

        print("DPDK status after un-binding all  "+str(pci_after_sort)+"\n"+ json.dumps(self.eth_port))
        dpdk_status = self.get_dpdk_status()
        print("Bind the interfaces to DPDK\n")
        pci_drv_map = dict()
        for domain_bus_slot_func in pci_after_sort:
            output = getattr(self.warp17_obj, 'shell')(command="find /sys/bus/pci/drivers name | xargs grep "+domain_bus_slot_func).response()
            #output = self.warp17_obj.shell(command="find /sys/bus/pci/drivers name | xargs grep "+domain_bus_slot_func).response()
            for line in output.split("\n"):
                if len(line) > 0:
                    if re.search(r"(\w+)\/'+domain_bus_slot_func+':\s*Is\s*a\s*directory", line):
                        match = re.search(r"(\w+)\/"+domain_bus_slot_func+r":\s*Is\s*a\s*directory", line)
                        pci_drv_map[domain_bus_slot_func] = match.group(1)
                        print("Driver found as "+match.group(1)+" \n")

            #output = self.warp17_obj.shell(command=dpdk_dev_bind_path+" --bind="+bind+" "+domain_bus_slot_func).response()
            output = getattr(self.warp17_obj, 'shell')(command=dpdk_dev_bind_path+" --bind="+bind+" "+domain_bus_slot_func).response()
            if output:
                for line in output.split("\n"):
                    print(line+"\n")
                    if re.search(dpdk_dev_bind_path, line):
                        continue
                    if len(line) == 0:
                        print("Ethernet is using "+domain_bus_slot_func+" and successfully binded to DPDK-compatible driver igb_uio!!!\n")
                    elif re.search(r"already\s*bound\s*to\s*driver\s*\w+,\s*skipping", line):
                        print("Ethernet is using "+domain_bus_slot_func+" and successfully binded to DPDK-compatible driver igb_uio!!!\n")
                    else:
                        print("Ethernet is using "+domain_bus_slot_func+" and bind failed!!!\n")
                        result &= False

        dpdk_status['pci_drv_map'] = dict()
        dpdk_status['pci_drv_map'] = pci_drv_map
        #print("DPDK status: \n"+json.dumps(dpdk_status, indent=4))

        return dpdk_status





######################################################################################
# Name       : setup_warp17
# Description: initialize warp17 and gives you the prompt warp17>
######################################################################################

    def setup_warp17(self):
        """
        Method initialize warp17 and gives you the prompt warp17>
        :Arguments:ptional arguments ring_if_pairs,tcb_pool_sz,log_level,ucb_pool_sz
        :return: returns true if successful
        """
        host, result = self.warp17_obj, True
        print("Force kill , if warp17 is already running\n")
        #host.shell(command="ps -aux | grep \"warp17\"| awk '{print $2}'| xargs kill -9").response()
        getattr(host, 'shell')(command="ps -aux | grep \"warp17\"| awk '{print $2}'| xargs kill -9").response()
        #if 'tcb_pool_sz' in kwargs:
        #    tcb_pool_sz = kwargs.pop('tcb_pool_sz', None)
        #if 'ucb_pool_sz' in kwargs:
        #    ucb_pool_sz = kwargs.pop('ucb_pool_sz', None)
        #if 'log_level' in kwargs:
        #    log_level = kwargs.pop('log_level', None)
        options = "\n"

        #output = host.shell(command="locate /build/warp17").response()
        output = getattr(host, 'shell')(command="locate /build/warp17").response()
        for line in output.split("\n"):
            if not self.warp17_path:
                if len(line) > 0:
                    if re.search(r"(.*)\/build\/warp17", line) is not None:
                        match = re.search(r"(.*)\/build\/warp17", line)
                        self.warp17_path = match.group(1)

        options = " "

        #try:
            #self.cfg_file_name
        #    options = " --cmd-file "+cfg_file_name+options
        #except Exception as error:
        #    print(str(error)+": cfg_file_name is not there")

        if self.ring_if_pairs:
            options = " --ring-if-pairs "+str(self.ring_if_pairs)+options
        if self.tcb_pool_sz:
            options = " --tcb-pool-sz "+str(self.tcb_pool_sz)+options
        if self.ucb_pool_sz:
            options = " --ucb-pool-sz "+str(self.ucb_pool_sz)+options
        #except Exception as error:
        #    print(str(error)+": ucb_pool_sz is not there")
        #try:
            #print_level
         #   options = " --log-level "+log_level+options
        #except Exception as error:
         #   print(str(error)+" :log level is not there")
        if self.qmap_default:
            options = " --qmap-default "+str(self.qmap_default)+options
        options = " -- "+options
        if self.nchan:
            options = " -n "+str(self.nchan)+options
        if self.mem_in_mb:
            options = " -m "+str(self.mem_in_mb)+options
        #try:
            #self.hex_mask
        #    options = " -c "+str(self.hexmask)+options
        #except Exception as error:
        #    print(str(error)+": hexmax is not found")
        #try:
            #self.lcore
        #    options = " -l "+self.lcore+options
        #except Exception as error:
        #    print(str(error)+"lcore is  not available")
        try:
            #self.lcores
            options = " --lcores "+self.lcores+options
        except Exception as error:
            print(str(error)+" :lcores is  not available")

        start_warp17 = self.warp17_path+"/build/warp17 "+str(options)

        print(": List of parameter are supported\n")
        getattr(host, 'shell')(command=self.warp17_path+r"/build\/warp17 --help").response()
        out = getattr(host, 'shell')(command=start_warp17, pattern='warp17>', timeout=100).response()
        time.sleep(80)
        print(out)
        output = out.split("\n")
        for line in output:
            line.rstrip("\r")
        for line in output:
            if len(line) > 0:
                if re.search(r"PANIC\s*in\s*.*", line) is not None:
                    print("WARP17 is not started due to :\n"+line)
                    result = False
                if re.search(r"Not\s*enough\s*memory\s*available.\s*Requested:\s*(\d*)MB,\s*available:\s*(\d*)MB", line) is not None:
                    match = re.search(r"^Not\s*enough\s*memory\s*available.\s*Requested:\s*(\d*)MB,\s*available:\s*(\d*)MB", line)
                    print("WARP17 is not started , try changing the memory '-m' option to"+match.group(1)+" :\n"+line)
                    result = False
                if re.search(r"Cannot\s*init\s*memory.*", line) is not None:
                    print(" WARP17 is not started , try changing the memory '-m' option as mentioned above\n"+line)
                    result = False
                if re.search(r"Aborted\s*\(core\s*dumped\)", line) is not None:
                    print("WARP17 is not started due to a core dump:\n"+line)
                    result = False
                if re.search(r":\s*ERROR:.*", line) is not None:
                    print("WARP17 is not started due to error :\n"+line)
                    result = False

        return result


######################################################################################
# Name       : warp17_defaults
# Description: Loads the default
######################################################################################

    def warp17_defaults(self):

        """
        Method called by user or in time of initialization to get the default values
        :host ssh obj :
            *MANDATORY* ssh object to the host
        :return: TRUE/FALSE.
            In all other cases Exception is raised
        """

        self.bind = 'igb_uio'
        self.unbind = ['i40e', 'e1000', 'ixgbe', 'e1000e', 'ixgbevf']
        self.setup_warp17_flag = 1
        self.setup_dpdk_flag = 1
        self.dpdk_status = dict()

        #_cores : CPU cores for processing packets , ctrl_cores : cores will be used by CLI and MGMT
        self.data_cores = 14 #cores for processing packets
        self.ctrl_cores = 2 #cores will be used by CLI and MGMT

        self.mem_in_mb = int(Warp17api.get_mem_in_mb(handle=self.warp17_obj))
        self.qmap = '0x42'
        self.qmap_default = 'max-q'
        self.mbuf_pool_sz = 750
        self.mbuf_hdr_pool_sz = 750

        # Miscelleneous optional parameters .
        self.ch_cfg = 0
        self.inet = 1
        self.inet6 = 0 #no IPV6 support yet , this is for future use

        self.uname = 'root'
        self.password = 'Embe1mpls'
        self.pattern = '.*'
        self.timeout = 120
        #self.dpdk_dev_bind_path = "/usr/local/share/dpdk/tools/dpdk-devbind.py"
        chan = Warp17api.num_of_dmidecode_channels(handle=self.warp17_obj)
        if not chan:
            print("Did not get the total number of channel present on "+self.server_name)
            return None
        else:
            print("Got the total number of channel as "+str(chan))
        self.nchan = chan

        return True





######################################################################################
# Name       : warp17_defaults_vm
# Description: Loads the default on a vm machine with 10 GE interfaces (tested)
######################################################################################
    def warp17_defaults_vm(self):
        """ initializes default values for vm server """

        self.bind = 'igb_uio'
        self.unbind = ['i40e', 'e1000', 'ixgbe', 'e1000e', 'ixgbevf']
        self.setup_warp17_flag = 1
        self.setup_dpdk_flag = 1
        self.dpdk_status = dict()
        self.dpdk_src_path = None

        #_cores : CPU cores for processing packets , ctrl_cores : cores will be used by CLI and MGMT
        self.data_cores = 2 #cores for processing packets
        self.ctrl_cores = 2 #cores will be used by CLI and MGMT

        self.mem_in_mb = int(Warp17api.get_mem_in_mb(handle=self.warp17_obj))
        self.qmap = '0x42'
        self.qmap_default = 'max-c'
        self.mbuf_pool_sz = 750
        self.mbuf_hdr_pool_sz = 750

        # Miscelleneous optional parameters .
        self.ch_cfg = 0
        self.inet = 1
        self.inet6 = 0 #no IPV6 support yet , this is for future use

        self.uname = 'root'
        self.password = 'Embe1mpls'
        self.pattern = '.*'
        self.timeout = 120
        #self.dpdk_dev_bind_path = "/usr/local/share/dpdk/tools/dpdk-devbind.py"

        # Determine the total memory channels available on WARP17 machine
        #chan = Warp17api.num_of_dmidecode_channels(handle=self.warp17_obj)
        #if chan:
        #    print("Did not get the total number of channel present on "+self.server_name)
        #    return None
        #else:
        #    print("Got the total number of channel as "+chan)
        self.nchan = 1

        return True


######################################################################################
# Name       : get_mem_in_mb
# Description: gets the available RAM in MB
######################################################################################
    @classmethod
    def get_mem_in_mb(cls, **kwargs):
        """ gets the available RAM in MB """
        obj = kwargs.get('handle')
        test_res = getattr(obj, 'shell')(command="cat /proc/meminfo")
        output = test_res.response()
        print(r"\n Command output for Physical Memory in MB \(RAM\): "+str(output))

        for line in output.split("\n"):
            if len(line) > 0:
                if re.search(r"HugePages_Total:\s+(\d+)", line) is not None:
                    match = re.search(r"HugePages_Total:\s+(\d+)", line)
                    hugepage = int(match.group(1))
                if re.search(r"Hugepagesize:\s+(\d+)", line) is not None:
                    num = re.search(r"Hugepagesize:\s+(\d+)", line)
                    hugepage_size = int(num.group(1))

        total_memory = int((hugepage_size *  hugepage) /1024)

        #Return only 90 % of the memory free.
        scale = ((((total_memory)*90/100) * 70/100) / 1024)
        print("Maximum approximate scale you can achive on this machine is "+str(scale)+r" million\(s\) \n This is a approximate value")
        return total_memory



######################################################################################
# Name       : num_of_dmidecode_channels
# Description: Calculates dmidecode_channel and returns a number of channels
######################################################################################

    @classmethod
    def num_of_dmidecode_channels(cls, **kwargs):

        """
        Method called by user to Calculates dmidecode_channel
        :host ssh obj :
            *MANDATORY* ssh object to the host
        :return: the number of channels.
            In all other cases Exception is raised
        """
        (port, node, channel, dimm, chan_info, num_of_channel) = (0, 0, 0, 0, 0, 0)
        host = kwargs.get('handle')
        chan = []

        #cmd_output = host.shell(command="dmidecode").response()
        cmd_output = getattr(host, 'shell')(command="dmidecode").response()
        chan_info = cmd_output.split("\n")
        for i in chan_info:
            chan.append(i.rstrip("\r"))
        for line in chan:
            if len(line) > 0:
                #print("line = {}".format(line))
                if re.search(r"Bank\s+Locator:\s+P(\d+)_Node(\d+)_Channel(\d+)_Dimm(\d+)", line) is not None:

                    chan_info = re.search(r"Bank\s+Locator:\s+P(\d+)_Node(\d+)_Channel(\d+)_Dimm(\d+)", line)
                    port = chan_info.group(1)
                    node = chan_info.group(2)
                    channel = chan_info.group(3)
                    dimm = chan_info.group(4)

                    if int(num_of_channel) < int(channel):
                        print("Port = {},  Node = {}, Channel = {}, Dimm = {}".format(port, node, channel, dimm))
                        num_of_channel = channel
                #else :
                #   print("RE Match not found")
        #print(int(num_of_channel) + 1)
        return int(num_of_channel) + 1

######################################################################################
# Name       : get_numa_node
# Description: gets the numa node value by issuing /sys/bus/pci/devices/<interface_in_domain:bus:slot.func_format>/numa_node
######################################################################################


    def get_numa_node(self, **kwargs):

        """
        Method called by user to Calculates numa_node
        :host ssh obj :
            *MANDATORY* ssh object to the host
        :eth_if_in_bus_slot_func:
            *MANDATORY* argument for ethernet to eth_if_in_bus_slot_func
        :return: the numa_node.
            In all other cases Exception is raised
        """
        if 'eth_if_in_bus_slot_func' in kwargs:
            eth_if_in_bus_slot_func = kwargs.pop('eth_if_in_bus_slot_func')
        numa = []
        host = self.warp17_obj

        cmd = '{0}{1}{2}'.format("cat  /sys/bus/pci/devices/", eth_if_in_bus_slot_func, "/numa_node")

        #cmd_output = host.shell(command=cmd).response()
        cmd_output = getattr(host, 'shell')(command=cmd).response()
        numa_info = cmd_output.split("\n")
        for i in numa_info:
            numa.append(i.rstrip("\r"))
        for line in numa:
            if len(line) > 0:
                #print("line = {}".format(line))
                if re.search(r"(\d*)", line) is not None:
                    numa_info = re.search(r"(\d*)", line)
                    numa_node = numa_info.group(1)
                else:
                    print("RE Match not found for numa node")

        return numa_node

######################################################################################
# Name       : create_rpc_ini_file
# Description: gets the numa node value by issuing /sys/bus/pci/devices/<interface_in_domain:bus:slot.func_format>/numa_node
######################################################################################

    def create_rpc_ini_file(self, rpc_client_path):
        """ this module is to create rpc_client.ini file in server """
        res = True

        outfile = os.path.join(os.getcwd(), "rpc_client.ini")

        file_handle = open("rpc_client.ini", "w")
        core = "coremask="+self.lcores
        nchan = "nchan="+str(self.nchan)
        memory = "memory="+str(self.mem_in_mb)
        tcbpool = "tcb-pool-sz="+str(self.tcb_pool_sz)
        #ports="ports="+self.dpdk_status['intf_pci_map'][self.eth_if[0]]+" "+self.dpdk_status['intf_pci_map'][self.eth_if[1]]
        ports = "ports="
        for eth in self.eth_if:
            ports = ports+self.dpdk_status['intf_pci_map'][eth]+" "
        qmapdefault = "qmap-default="+self.qmap_default
        listt = ["[DEFAULT]", core, nchan, memory, tcbpool, ports, qmapdefault]
        try:
            for i in listt:
                file_handle.write(i)
                file_handle.write("\n")
        except Exception as error:
            print(str(error)+": Failed to write ini file\n")
            res = False

        file_handle.close()
        self.scp(src_path=outfile, dst_path=rpc_client_path)
        return res

######################################################################################
# Name       : cleanup_warp
# Description: Deleting warp17 session and unbiding ports from DPDK
######################################################################################

    def cleanup_warp(self):
        """ Deleting warp17 session and unbiding ports from DPDK """
        getattr(self.client_handle, 'shell')(command="ps -aux | grep \"warp17\"| awk '{print $2}'| xargs kill -9").response()

        self.dpdk_status = self.get_dpdk_status()

        i = 0
        for intf in self.eth_if:
            domain_bus_slot_func = self.dpdk_status['dpdk_pci_inuse'][i]
            flag = 0
            for key, value in self.dpdk_status['intf_drv'].items():
                if flag == 0:
                    output = getattr(self.client_handle, 'shell')(command=self.dpdk_status['dpdk_dev_bind_path']+" --bind="+\
                    value+" "+domain_bus_slot_func).response()
                    out = output.split("\n")
                    if len(out) == 1:
                        flag = 1
                    elif re.search(r""+domain_bus_slot_func+r"\s*already\s*bound\s*to\s*driver\s*\w+,\s*skipping", output) is not None:
                        flag = 1
            i = i+1
