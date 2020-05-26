#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: srx operation keywords for ALG
Author: Vincent Wang, wangdn@juniper.net
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import re


class alg_srx(object):
    """
    Description: srx operation keywords for ALG

    keywords list:
    *
    * request_srx_service_twamp
    *
    """

    def __init__(self, device=None):
        """ device handle """
        self.device = device
        self.cli_timeout = 60

    def request_srx_service_twamp(self, device=None, operator=None, control_name=None):
        """
        :param str device:
            **REQUIRED** srx handle

        :param str operator:
            **REQUIRED** operator to start or stop

        :param str control_name:
        **REQUIRED** control name of twamp client

        """
        if device is None:
            raise Exception("device handle is None")

        if operator is None:
            raise Exception("twamp operator is None")

        if control_name is None:
            cli_command = 'request services rpm twamp ' + operator + ' client'
        else:
            cli_command = 'request services rpm twamp ' + operator + ' client ' + control_name

        response = device.cli(command=cli_command, timeout=self.cli_timeout).response()
        if re.search('error', response):
            raise Exception("------do request query failed!------\n")
        return response
