#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Windows common keywords
Author: Wentao Wu, wtwu@juniper.net
"""
import ipaddress
import time

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments


class common_windows(object):
    """
    Description: Windows common keywords

    keywords list:
    * config_windows_interface_ip_address
    * delete_windows_interface_ip_address
    """
    def __init__(self, device=None):
        """
        device handle
        """
        self.device = device
        self.shell_timeout = 60
        self.interval = 5
        self.retry = 5

    def _run_windows_command(self, device=None, command=None, **kwargs):
        """
        run windows command will have [Access is denied] error
        this command can re-run the command in loop
        """
        if device is None:
            raise Exception("device handle is None")
        if command is None:
            raise Exception("command is mandatory argument")

        retry = int(kwargs.get("retry", self.retry))
        timeout = int(kwargs.get("timeout", self.shell_timeout))

        index = 1
        while index <= int(retry):
            device.log(level='DEBUG', message="run windows command : {}".format(command))
            response = device.shell(command=command, timeout=timeout).response()
            device.log(level='DEBUG', message="run windows command result : {}".format(response))
            # if access is denied/syntax is incorrect, re-run the command again
            if "denied" in response:
                device.log(level='INFO', message=" run windows command {} is denied, wil retry... retried {} times".format(command, index))
                index += 1
            else:
                device.log(level='INFO', message=" run windows command {} passed in {} times".format(command, index))
                return response
        # return error after retry loop
        device.log(level='ERROR', message=" run windows command {} failed, retried {} times".format(command, index))
        raise Exception("run windows command error")

    def config_windows_interface_ip_address(self, device=None, interface='trf', ip='1.2.3.4', mask='24', **kwargs):
        """
        Config Windows Interface Ip Address

        :param str device:
        **REQUIRED** Device handle
        """
        if device is None:
            raise Exception("device handle is None")

        retry = int(kwargs.get("retry", self.retry))
        interval = int(kwargs.get("interval", self.interval))

        # check ip format
        if ipaddress.ip_address(ip):
            ip_version = ipaddress.ip_address(ip).version
            device.log(level='DEBUG', message="ip address {} version is {}".format(ip, ip_version))

        # set config command
        if ip_version == 6:
            cmd = 'c:/windows/system32/netsh.exe interface ipv6 set address "' + interface + '" ' + ip + '/' + str(mask)
            show_cmd = 'c:/windows/system32/netsh.exe interface ipv6 show address "' + interface + '"'
        else:
            cmd = 'c:/windows/system32/netsh.exe interface ipv4 set address "' + interface + '" static ' + ip + '/' + str(mask)
            show_cmd = 'c:/windows/system32/netsh.exe interface ipv4 show address "' + interface + '"'

        # run command
        device.log(level='DEBUG', message="config command is {}".format(cmd))
        response = self._run_windows_command(device=device, command=cmd)
        device.log(level='DEBUG', message="config command response is {}".format(response))

        if "incorrect" in response or "not" in response:
            # return error when command result have error
            device.log(level='ERROR', message="config windows interface ip address command syntax error: {} ".format(cmd))
            raise Exception("config interface ip address error, please check interface name or status")

        # run command with loop, need to wait the address available in interface
        device.log(level='DEBUG', message="show command is: {}".format(show_cmd))
        index = 1
        while index <= int(retry):
            response = self._run_windows_command(device=device, command=show_cmd)
            device.log(level='DEBUG', message="show command response is {}".format(response))
            if ip in response:
                device.log(level='INFO', message="config windows interface ip address passed: {} {}/{} ".format(interface, ip, mask))
                return True
            else:
                device.log(level='INFO', message="ip address not available {} {}/{} , will sleep {} sec to retry... retried {} times".format(interface, ip, mask, interval, index))
            index += 1
            time.sleep(int(interval))
        # return error after retry loop
        device.log(level='ERROR', message="config windows interface ip address failed: {} {}/{} ".format(interface, ip, mask))
        raise Exception("config windows interface ip address failed")

    def delete_windows_interface_ip_address(self, device=None, interface='trf', ip=None, **kwargs):
        """
         Delete Windows Interface Ip Address

        :param str device:
            **REQUIRED** Device handle for the Linux host
        """
        if device is None:
            raise Exception("device handle is None")

        retry = int(kwargs.get("retry", self.retry))
        interval = int(kwargs.get("interval", self.interval))

        # check ip format when ip is not None
        if ip is not None:
            ip_version = ipaddress.ip_address(ip).version
            if ip_version == 6:
                # set command
                cmd = 'c:/windows/system32/netsh.exe interface ipv6 delete address "' + interface + '" ' + ip
                show_cmd = 'c:/windows/system32/netsh.exe interface ipv6 show address "' + interface + '"'
            else:
                cmd = 'c:/windows/system32/netsh.exe interface ipv4 delete address "' + interface + '" ' + ip
                show_cmd = 'c:/windows/system32/netsh.exe interface ipv4 show address "' + interface + '"'
        # ip is None, set ip_version=0
        else:
            device.log(level='INFO', message="set interface {} with dhcp mode to clear all IPv4 address".format(interface))
            ip_version = 0
            # set command
            cmd = 'c:/windows/system32/netsh.exe interface ipv4 set address "' + interface + '" source=dhcp '
            show_cmd = 'c:/windows/system32/netsh.exe interface ipv4 show address "' + interface + '"'

        # run command
        device.log(level='DEBUG', message="delete command is: {}".format(cmd))
        response = self._run_windows_command(device=device, command=cmd)
        device.log(level='DEBUG', message="delete command response is: {}".format(response))

        if "incorrect" in response or "not" in response:
            # return error when command result have error
            device.log(level='ERROR', message="delete windows interface ip address command syntax error: {} ".format(cmd))
            raise Exception("delete interface ip address error, please check interface name or status")

        # run command with loop, need to wait the address delete pass in interface
        device.log(level='DEBUG', message="show command is: {}".format(show_cmd))
        index = 1
        while index <= int(retry):
            response = self._run_windows_command(device=device, command=show_cmd)
            device.log(level='DEBUG', message="show command response is {}".format(response))
            # ipv4 or ipv6 mode, ip can't be found in reponse
            if ip_version > 0:
                if ip not in response:
                    device.log(level='INFO', message="delete windows interface {} ip address {} passed.".format(interface, ip))
                    return True
                else:
                    device.log(level='INFO', message="delete interface {} address {} not pass, will sleep {} sec to retry... retried {} times".format(interface, ip, interval, index))
            # dhcp mode, result should have 'Yes' in response
            else:
                if "Yes" in response:
                    device.log(level='INFO', message="set interface {} to dhcp mode passed. ".format(interface))
                    return True
                else:
                    device.log(level='INFO', message="set interface {} to dhcp mode not pass, will sleep {} sec to retry... retried {} times".format(interface, interval, index))
            index += 1
            time.sleep(int(interval))
        # return error after retry loop
        device.log(level='ERROR', message="delete windows interface ip address failed: {} {}".format(interface, ip))
        raise Exception("delete windows interface ip address failed")
