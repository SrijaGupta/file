#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: linux operation keywords
Author: Vincent Wang, wangdn@juniper.net
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import re


class common_linux(object):
    """
    Description: linux operation keywords

    keywords list:
    *
    * get_linux_process_id
    *
    """

    def __init__(self, device=None):
        """ device handle """
        self.device = device
        self.shell_timeout = 60

    def get_linux_process_id(self, device=None, process_name=None, **kwargs):
        """
        Description: get process id on linux VM
        Author: Vincent Wang, wangdn@juniper.net

        :param str device:
        **REQUIRED** linux VM handle

        :param str process_name:
        **REQUIRED** process name

        :return:
            process ID of the specific process
            0 if cannot find specific process
        """

        if device is None:
            raise Exception("device handle is None")

        if process_name is None:
            raise Exception("device handle is None")

        timeout = int(kwargs.get("timeout", self.shell_timeout))
        shell_command = 'ps aux | grep -v grep | grep ' + process_name
        response = device.shell(command=shell_command, timeout=timeout).response()
        match_obj = re.match(r"\w+\s+(\d+)", response)
        if match_obj:
            process_id = match_obj.group(1)
            return process_id
        return None
