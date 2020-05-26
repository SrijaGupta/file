#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Fwauth SRX keywords
Author: Linjing Liu, ljliu@juniper.net
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import re
import ipaddress

from jnpr.toby.utils.junos.dut_tool import dut_tool


class fwauth_srx(object):
    """
    Description: Fwauth SRX keywords

    keywords list:
    * check_srx_firewall_auth_jims_statistics
    * clear_srx_firewall_auth_jims_statistics
    * check_srx_firewall_auth_table
    * check_srx_firewall_auth_table_on_pfe
    """

    def __init__(self, device=None):
        """
        :param str device:
        **REQUIRED** srx handle
        """
        self.device = device
        self.commit_timeout = 150
        self.shell_timeout = 60
        self.cli_timeout = 60
        self.dut = dut_tool()

    def check_srx_firewall_auth_jims_statistics(self, device=None, field="success", value=0):
        """
        :param str device:
        **REQUIRED** srx handle

        :param str field:
        *OPTIONAL* field name    # success  | other value

        :param str value:
        *OPTIONAL* field value
        """

        if device is None:
            raise Exception("device handle is None")

        cmd_list = "show security firewall-authentication jims statistics"

        if field == 'success':
            pattern = r"Push success counter:\s+(\d+)"
        else:
            pattern = r"Push failure counter:\s+(\d+)"
        return_value = device.cli(device=device, command=cmd_list, timeout=self.cli_timeout).response()
        match = re.search(pattern, return_value, re.S)
        get_count = match.group(1)
        device.log(level='DEBUG', message="getting count is {}".format(get_count))
        device.log(level='DEBUG', message="inputing value is {}".format(value))

        if int(get_count) == int(value):
            device.log(level='INFO', message="the push value is the same as expected.")
            return True
        else:
            raise Exception("the push value is unexpected.\n")

    def clear_srx_firewall_auth_jims_statistics(self, device=None):
        """
        :param str device:
        **REQUIRED** srx handle

        """

        if device is None:
            raise Exception("device handle is None")

        cmd_list = "clear security firewall-authentication jims statistics"
        device.cli(device=device, command=cmd_list, timeout=self.cli_timeout)
        return True

    def check_srx_firewall_auth_table(self, device=None, node=None, no_entry=False, **kwargs):
        """
        Author: Linjing Liu, ljliu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str ip:
        **REQUIRED** ip address

        :param str node:
        *OPTIONAL* HA testbed using it

        :param str username:
        *OPTIONAL* user name

        :param str no_entry:
        *OPTIONAL* have no entry            True: no entry    False: have entry

        :param str profile:
        *OPTIONAL* access profile

        :param str status:
        *OPTIONAL* Authentication state

        :param str method:
        *OPTIONAL* Authentication method

        :param str src_zone:
        *OPTIONAL* source zone

        :param str dst_zone:
        *OPTIONAL* destination zone

        :param str client_groups:
        *OPTIONAL* client group

        :param str logical_system:
        *OPTIONAL* logical system name

        """
        ip = kwargs.get("ip", '1.1.1.1')
        username = kwargs.get("username")
        profile = kwargs.get("profile")
        status = kwargs.get("status")
        method = kwargs.get("method")
        src_zone = kwargs.get("src_zone")
        dst_zone = kwargs.get("dst_zone")
        client_groups = kwargs.get("client_groups")
        logical_system = kwargs.get("logical_system")

        base_cmd = "show security firewall-authentication users address " + ip
        if device is None:
            raise Exception("device handle is None")

        if logical_system is not None:
            base_cmd = base_cmd + " logical-system " + logical_system

        if node is not None:
            cmd_list = base_cmd + " node " + node
        else:
            cmd_list = base_cmd

        return_value = device.cli(command=cmd_list, timeout=self.cli_timeout).response()
        if no_entry:

            if re.search(r"{}".format(ip), return_value, re.M):
                raise Exception("the specified firewall auth IP exists on RE, this's unexpected.\n")
            else:
                device.log(level='INFO', message="the specified firewall auth IP doesn't exist, this's expected.")
                return True

        real_ip = re.search(r"Source\s*IP:\s+(.*?)[\r\n]", return_value, re.S).group(1)

        match_ip = ipaddress.ip_address(real_ip)

        if ipaddress.ip_address(match_ip) == ipaddress.ip_address(ip):
            if username is not None:
                if re.search(r"Username:\s+{}".format(username), return_value, re.S) is None:
                    raise Exception('user name can not be found in auth entry')
            if profile is not None:
                if re.search(r"Access\s+profile:\s+{}".format(profile), return_value, re.S) is None:
                    raise Exception('access profile is not correct in auth entry')
            if status is not None:
                if re.search(r"Authentication state:\s+{}".format(status), return_value, re.S) is None:
                    raise Exception('Authentication state is not correct in auth entry')
            if method is not None:
                if re.search(r"Authentication method:\s+{}".format(method), return_value, re.S) is None:
                    raise Exception('Authentication method is not correct in auth entry')
            if src_zone is not None:
                if re.search(r"Source zone:\s+{}".format(src_zone), return_value, re.S) is None:
                    raise Exception('src_zone is not correct in auth entry')
            if dst_zone is not None:
                if re.search(r"Destination zone:\s+{}".format(dst_zone), return_value, re.S) is None:
                    raise Exception('dst_zone is not correct in auth entry')
            if client_groups is not None:
                if re.search(r"Client-groups:\s+{}".format(client_groups), return_value, re.S) is None:
                    raise Exception('client groups is not correct in auth entry')
            if logical_system is not None:
                if re.search(r"Lsys:\s+{}".format(logical_system), return_value, re.S) is None:
                    raise Exception('logical system is not correct in auth entry')
            device.log(level='DEBUG', message="get the correct auth table on dut")
            return True
        else:
            raise Exception('the firewall auth entry can not be found on RE')

    def check_srx_firewall_auth_table_on_pfe(self, device=None, node=None, no_entry=False, **kwargs):
        """
        Author: Linjing Liu, ljliu@juniper.net

        Check srx firewall authentication table on PFE

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str ip:
        **REQUIRED** ip address

        :param str node:
        *OPTIONAL* HA testbed using it

        :param str username:
        *OPTIONAL* user name

        :param str no_entry:
        *OPTIONAL* have no entry            True: no entry    False: have entry

        :param str profile:
        *OPTIONAL* access profile

        :param str status:
        *OPTIONAL* Authentication state


        :param str src_zone:
        *OPTIONAL* source zone

        :param str dst_zone:
        *OPTIONAL* destination zone

        :param str client_groups:
        *OPTIONAL* client group


        """

        ip = kwargs.get("ip", "1.1.1.1")
        username = kwargs.get("username")
        profile = kwargs.get("profile")
        status = kwargs.get("status")
        src_zone = kwargs.get("src_zone")
        dst_zone = kwargs.get("dst_zone")
        client_groups = kwargs.get("client_groups")

        if device is None:
            raise Exception("device handle is None")

        cmd_list = "show usp fwauth users ip " + ip

        if node is not None:
            return_value = self.dut.send_vty_cmd(
                device=device,
                node=node,
                component="SPU",
                cmd=cmd_list,
            )
        else:
            return_value = self.dut.send_vty_cmd(
                device=device,
                component="SPU",
                cmd=cmd_list,
            )

        if no_entry:
            if re.search(r"{}".format(ip), return_value, re.M):
                raise Exception("the specified firewall auth IP should not exist on PFE\n")
            else:
                device.log(level='INFO', message="the specified firewall auth IP doesn't exist, this's expected.")
                return True

        real_ip = re.search(r"Source\s*IP:\s+(.*?)\s+[\r\n]", return_value, re.S).group(1)
        device.log(level='DEBUG', message="get the real_ip {} on PFE".format(real_ip))

        match_ip = ipaddress.ip_address(real_ip)

        if ipaddress.ip_address(match_ip) == ipaddress.ip_address(ip):
            if username is not None:
                if re.search(r"Username:\s+{}".format(username), return_value, re.S) is None:
                    raise Exception('user name can not be found in auth entry')
            if profile is not None:
                if re.search(r"access\s+profile:\s+{}\s+".format(profile), return_value, re.S) is None:
                    raise Exception('access profile is not correct in auth entry')
            if status is not None:
                if re.search(r"Status:\s+{}\s+".format(status), return_value, re.S) is None:
                    raise Exception('Authentication state is not correct in auth entry')
#            if method is not None:
#                if re.search(r"Authentication via:\s+{}".format(method), return_value, re.S) is None:
#                    raise Exception('Authentication method is not correct in auth entry')
            if client_groups is not None:
                if re.search(r"Groups List:\s+{}".format(client_groups), return_value, re.S) is None:
                    raise Exception('client groups is not correct in auth entry')
            if src_zone is not None:
                if re.search(r"Zone:\s+{}->.*".format(src_zone), return_value, re.S) is None:
                    raise Exception('src_zone is not correct in auth entry')
            if dst_zone is not None:
                if re.search(r"Zone:\s+.*->{}".format(dst_zone), return_value, re.S) is None:
                    raise Exception('dst_zone is not correct in auth entry')
            device.log(level='DEBUG', message="get the correct auth table on pfe")
            return True
        else:
            raise Exception('the firewall auth entry can not be found on PFE')
