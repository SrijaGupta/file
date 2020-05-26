"""
Copyright (C) 2016-2017, Juniper Networks, Inc.
All rights reserved.
Authors:

Description:
    Toby Sflow test suite
"""

import re
import ipaddress

class Sflow(object):
    """
    Base Class for Toby sFlow
    Protocol/feature independent Design
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.decoder_path = None
        self.decoder_status = False
        self.decoder_pid = None
        self.decoder_port = None
        self.log_filename = None

    def sflow_init(self, device, interface, server_ip_address, dut_ip_address, log_filename, decoder_path, decoder_port):
        """
        Parameters to initialize sflow server so sflow decoder gets right ip address and udp port to listen to
        :params device:
                **REQUIRED**  device handle of linux sflow server
        :params interface:
                **REQUIRED**  sflow server interface name which is connected to dut
        :params server_ip_address:
                **REQUIRED**  ipv4 address for sflow server interface
        :params dut_ip_address:
                **REQUIRED**  dut ipv4 address for interface which is connected to sflow server
        :params log_filename:
                **REQUIRED**  log name for sflow decoder
        :params decoder_path:
                **REQUIRED**  directory where sflow decoder is
        :params decoder_port:
                **REQUIRED**  sflow decoder udp port number
        """
        count = 5
        server = device
        if not server.su():
            raise ValueError("cannot login to server as root user")

        try:
            t.log(level='INFO', message='configuring IP address on interface facing DUT')
            server.shell(command="ifconfig %s 0" % interface + '\n')
            server.shell(command='ifconfig ' + interface + ' ' + server_ip_address + '\n')
            t.log(level='INFO', message='verify IP address configuration on interface')
            response = server.shell(command="ifconfig %s" % interface + '\n')
            server_ip = str(ipaddress.IPv4Interface(server_ip_address)).split("/")
            match = re.search('inet' + '.*' + server_ip[0] + '.*' + 'Mask:', response.response())
            if match:
                t.log(level='INFO', message="Server IP address is configured successfully")
            else:
                t.log(level='ERROR', message="Server IP address is not configured successfully")

            t.log(level='INFO', message='configuring static route to DUT')
            dut_network = str(ipaddress.IPv4Network(dut_ip_address, strict=False).with_netmask).split("/")
            dut_ip = str(ipaddress.IPv4Interface(dut_ip_address)).split("/")
            server.shell(command='route add -net ' + dut_network[0] + ' ' + 'netmask' + ' ' + dut_network[1] + ' ' + 'dev' + ' ' + interface + '\n')
            response = server.shell(command="netstat -nr" + '\n')
            match = re.search(dut_network[0] + '.*' + dut_network[1] + '.*', response.response())
            if match:
                t.log(level='INFO', message="Route to DUT is configured successfully")
            else:
                t.log(level='ERROR', message="Route to DUT is not configured successfully")

            t.log(level='INFO', message='Verify if DUT is reachable')
            response = server.shell(command=('ping ' + dut_ip[0] + ' ' + '-c' + ' ' + str(count)) + '\n')
            match = re.search(str(count) + ' ' + 'packets transmitted,' + ' ' + str(count) + ' ' + 'received,' + ' ' + '0% packet loss', response.response())
            if match:
                t.log(level='INFO', message="Ping successful to DUT")
            else:
                t.log(level='ERROR', message="Ping unsuccessful to DUT")
        except:
            t.log(level='ERROR', message='shell command execution failed')
            raise ValueError("cannot configure IP address and route on server")
        self.decoder_port = decoder_port
        self.decoder_path = decoder_path
        self.log_filename = log_filename

    def start_sflow_decoder(self, server_handle, decoder_command):
        '''
        start sflow decoder
        Parameters to start sflow decoder
        :params server_handle:
                **REQUIRED**  device handle of linux sflow server
        :params decoder_command:
                **REQUIRED**  sflow decoder name
        '''
        server = server_handle
        decoder_cmd = str(decoder_command) + " > " + self.log_filename
        server.su()
        try:
            t.log(level='INFO', message='starting decoder')
            self.decoder_status = True
            server.shell(command='cd '+ str(self.decoder_path) + '\n')
            #decoder_res = server.shell(command=decoder_cmd + ' >/dev/null 2>&1 &').response().split(' ')
            decoder_res = server.shell(command=decoder_cmd + '&').response().split(' ')
            self.decoder_pid = int(decoder_res[1])
        except TypeError:
            t.log(level='ERROR', message='shell command execution failed')
            raise

    def stop_sflow_decoder(self, server_handle):
        '''
        stop sflow decoder
        Parameters to stop sflow decoder
        :params server_handle:
                **REQUIRED**  device handle of linux sflow server
        '''
        server = server_handle
        if not self.decoder_status:
            t.log(level='ERROR', message='Decoder not running')
            raise TypeError("sflowtool not running")
        try:
            t.log(level='INFO', message='killing ' + ' decoder')
            server.shell(command='kill -9 ' + str(self.decoder_pid) + '\n').response()
            #res = server.shell(command='kill -9 ' + str(self.decoder_pid) + '\n').response()
            #t.log(level="INFO", message=res)
        except:
            t.log(level='ERROR', message="Stop failed")
            raise
        self.decoder_status = False
