#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: linux operation keywords for VoIP ALG
Author: Vincent Wang, wangdn@juniper.net
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import re
import ipaddress


class alg_voip_linux(object):
    """
    Description: linux operation keywords for VoIP ALG

    keywords list:
    * config_linux_service_opensips
    * set_linux_service_opensips_status
    * config_linux_linphone
    * run_linux_linphone
    * execute_cmd_on_linux_linphone
    * send_linux_linphone_call
    * send_linux_linphone_answer
    * send_linux_linphone_terminate
    * stop_linux_linphone
    *
    """

    def __init__(self, device=None):
        """ device handle """
        self.device = device
        self.shell_timeout = 60

    def config_linux_service_opensips(self, device=None, ip_list=None, port='5060', protocol='udp', config='/usr/local/etc/opensips/opensips.cfg', **kwargs):
        """
        Description: Config the profile of OpenSIPs
        Author: Vincent Wang, wangdn@juniper.net

        :param str device:
            **REQUIRED** linux VM handle

        :param str ip_list:
        **REQUIRED** list of IP address of opensips

        :param str port:
        **OPTIONAL** listen port of opensips

        :param str protocol:
        **OPTIONAL** TCP/UDP protocol of opensips

        :param str config:
        **OPTIONAL** config file of opensips

        """
        if device is None:
            raise Exception("device handle is None")
        if ip_list is None:
            raise Exception("Cannot find the IPv4 or IPv6 address of OpenSIPs ")
        timeout = int(kwargs.get("timeout", self.shell_timeout))

        device.su()
        device.shell(command='/bin/cp -f ' + config + ' ' + config + '.bak', timeout=timeout)
        device.shell(command='sed -i \"/listen/d\" ' + config)
        device.shell(command='sed -i \"/disable_tcp/d\" ' + config)

        for ipaddr in ip_list:
            device.log(level='DEBUG', message="get the ipaddr {} from ip_list".format(ipaddr))
            if ipaddress.ip_address(ipaddr).version == 6:
                ipaddr = '[' + ipaddr + ']'
            device.shell(command='echo -e \" listen="' + protocol + ':' + ipaddr + ':' + port + '>> ' + config)

        if re.search('tcp', protocol) is not None:
            device.shell(command='echo -e \" disable_tcp=no \" >> ' + config)
        else:
            device.shell(command='echo -e \" disable_tcp=yes \" >> ' + config)
        return True

    def set_linux_service_opensips_status(self, device=None, operator='restart', **kwargs):
        """
        Description: Config the profile of OpenSIPs
        Author: Vincent Wang, wangdn@juniper.net

        :param str device:
            **REQUIRED** linux VM handle

        :param str operator:
        **OPTIONAL** operator to opensips service

        """
        if device is None:
            raise Exception("device handle is None")
        timeout = int(kwargs.get("timeout", self.shell_timeout))
        device.su()
        response = device.shell(command='opensipsctl ' + operator, timeout=timeout).response()
        if re.search('started', response) and re.search('start', operator):
            return True
        elif re.search('already running', response) and re.search('start', operator):
            return True
        elif re.search('stopped', response) and re.search('stop', operator):
            return True
        else:
            raise Exception("Fail to set the OpenSIPs status!")

    def config_linux_linphone(self, device=None, phone_number=None, proxy_address=None, port='5060', protocol='udp', expires='120', config='~root/.linphonerc', **kwargs):
        """
        Description: Config the profile of SIP linphone
        Author: Vincent Wang, wangdn@juniper.net

        :param str device:
            **REQUIRED** linux VM handle

        :param str phone_number:
        **REQUIRED** phone number of linphone

        :param str proxy_address:
        **REQUIRED** IPv4/IPv6 address of SIP proxy

        :param str port:
        **OPTIONAL** listen port of linphone

        :param str protocol:
        **OPTIONAL** TCP/UDP protocol of linphone

        :param str expires:
        **OPTIONAL** register expires of linphone

        :param str config:
        **OPTIONAL** config file of linphone

        """
        if device is None:
            raise Exception("device handle is None")

        if phone_number is None:
            raise Exception("Phone number is None")

        if proxy_address is None:
            raise Exception("IP address of SIP proxy is None")
        timeout = int(kwargs.get("timeout", self.shell_timeout))
        device.su()
        device.shell(command='/bin/cp -f ' + config + ' ' + config + '.bak', timeout=timeout)
        device.shell(command='sed -i \"/use_ipv6/d\" ' + config)
        device.shell(command='sed -i \"/reg_proxy/d\" ' + config)
        device.shell(command='sed -i \"/reg_identity/d\" ' + config)
        device.shell(command='sed -i \"/sip_port/d\" ' + config)
        device.shell(command='sed -i \"/transport/d\" ' + config)
        device.shell(command='sed -i \"/sip_tcp_port/d\" ' + config)
        device.shell(command='sed -i \"/reg_expires/d\" ' + config)

        if re.search(':', proxy_address) is None:
            device.shell(command=r'sed -i "/\[sip\]/ a\ use_ipv6=0" ' + config)
            device.shell(command=r'sed -i "/\[proxy_0\]/ a\ reg_identity=sip:' + str(phone_number) + '@' + proxy_address + '" ' + config)
            device.shell(command=r'sed -i "/\[proxy_0\]/ a\ reg_proxy=sip:' + proxy_address + '" ' + config)
        else:
            proxy_address = '[' + proxy_address + ']'
            device.shell(command=r'sed -i "/\[sip\]/ a\ use_ipv6=1" ' + config)
            device.shell(command=r'sed -i "/\[proxy_0\]/ a\ reg_identity=sip:' + str(phone_number) + '@' + proxy_address + '" ' + config)
            device.shell(command=r'sed -i "/\[proxy_0\]/ a\ reg_proxy=sip:' + proxy_address + '" ' + config)

        if re.search('udp', protocol) is None:
            device.shell(command=r'sed -i "/\[sip\]/ a\ sip_port=0" ' + config)
            device.shell(command=r'sed -i "/\[sip\]/ a\ transport=tcp" ' + config)
            device.shell(command=r'sed -i "/\[sip\]/ a\ sip_tcp_port=' + port + '" ' + config)
        else:
            device.shell(command=r'sed -i "/\[sip\]/ a\ sip_port=' + port + '" ' + config)
            device.shell(command=r'sed -i "/\[sip\]/ a\ sip_tcp_port=0" ' + config)

        device.shell(command=r'sed -i "/\[proxy_0\]/ a\ reg_expires=' + expires + '" ' + config)
        return True

    def run_linux_linphone(self, device=None, config='~root/.linphonerc', log='~root/linphone.log', option='-d 6', **kwargs):
        """
        Description: Run linphone
        Author: Vincent Wang, wangdn@juniper.net

        :param str device:
            **REQUIRED** linux VM handle

        :param str config:
        **OPTIONAL** config file of linphone

        :param str log:
        **OPTIONAL** log file of linphone

        :param str option:
        **OPTIONAL** option of linphone

        """

        if device is None:
            raise Exception("device handle is None")
        timeout = int(kwargs.get("timeout", self.shell_timeout))
        shell_command = 'linphonec -b ' + config + ' -l ' + log + ' ' + option
        device.su()
        response = device.shell(command=shell_command, pattern='linphonec>', timeout=timeout).response()
        if re.search('refused', response):
            raise Exception("------Environment Error, please start VNC on the VM!------\n")
        elif re.search('No such file', response):
            raise Exception("------Environment Error, cannot find linphone program!------\n")
        elif re.search('Cannot', response):
            raise Exception("------Environment Error, cannot find linphone config file!------\n")
        elif re.search('Ready', response):
            return True
        else:
            raise Exception("------Cannot run linphone correctly!------\n")

    def execute_command_on_linux_linphone(self, device=None, command=None, **kwargs):
        """
        Description: Execute command on linphone
        Author: Vincent Wang, wangdn@juniper.net

        :param str device:
            **REQUIRED** linux VM handle which already run linphone

        :param str command:
        **REQUIRED** the command to be executed on linphone

        """
        if device is None:
            raise Exception("device handle is None")

        if command is None:
            raise Exception("Call number is None")
        timeout = int(kwargs.get("timeout", self.shell_timeout))
        response = device.shell(command=command, pattern='linphonec>', timeout=timeout).response()
        return response

    def stop_linux_linphone(self, device=None, **kwargs):
        """
        Description: Make a call on linphone
        Author: Vincent Wang, wangdn@juniper.net

        :param str device:
            **REQUIRED** linux VM handle

        """

        if device is None:
            raise Exception("device handle is None")
        timeout = int(kwargs.get("timeout", self.shell_timeout))
        device.shell(command='terminate', pattern='linphonec>', timeout=timeout)
        response = device.shell(command='quit').response()
        if re.search('Terminating', response):
            return True
        else:
            raise Exception("------Error, fail to quit linphone------\n")
