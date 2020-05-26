"""
Copyright (C) 2016-2017, Juniper Networks, Inc.
All rights reserved.
Authors:

Description:
    Toby Sflow test suite
"""

class Csflow(object):
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

    def sflow_init(self, device, log_filename, decoder_path, decoder_port):
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
        server = device
        if not server.su():
            raise ValueError("cannot login to server as root user")

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
