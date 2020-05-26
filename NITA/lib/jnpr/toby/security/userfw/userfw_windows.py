#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Userfw SRX keywords
Author: Ruby Wu, wtwu@juniper.net
"""

import re

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments


class userfw_windows(object):
    """
    Description: Userfw windows keywords

    keywords list:
    * get_windows_domain_name
    """

    def __init__(self, device=None):
        """
        device handle
        """
        self.device = device
        self.shell_timeout = 60

    def get_windows_domain_name(self, device=None):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
            **REQUIRED** handle of windows PC
        """

        if device is None:
            raise Exception("device handle is None")

        response = device.shell(command='set', timeout=self.shell_timeout).response()

        if re.search('USERDNSDOMAIN', response):
            result = re.search(r"USERDNSDOMAIN=(.*?)[\r\n]", response, re.S)
            get_domain_name = result.group(1)
            device.log(level='INFO', message="get domain name is: {}".format(get_domain_name))

            if get_domain_name == 'JNPR.NET':
                raise Exception("------this windows PC is official computer, can't domain controller!------\n")

            get_domain_name = get_domain_name.lower()
            device.log(level='INFO', message="return domain name is: {}".format(get_domain_name))

            return get_domain_name

        else:
            raise Exception("------the windows PC isn't domain controller, please double check!------\n")
