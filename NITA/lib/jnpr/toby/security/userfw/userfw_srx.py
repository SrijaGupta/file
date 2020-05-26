#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Userfw SRX keywords
Author: Wentao Wu, wtwu@juniper.net
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
import re
import ipaddress
import time

from jnpr.toby.utils.junos.dut_tool import dut_tool


class userfw_srx(object):
    """
    Description: Userfw SRX keywords

    keywords list:
    * config_srx_userfw_webapi
    * delete_srx_userfw_webapi
    * config_srx_userfw_clearpass_userquery
    * delete_srx_userfw_clearpass_userquery
    * check_srx_userfw_auth_table_number
    * check_srx_userfw_device_entry_number
    * check_srx_userfw_no_user_auth_entry
    * check_srx_userfw_clearpass_auth_table_on_pfe
    * show_srx_userfw_auth_table_all
    * delete_srx_userfw_auth_table_by_request
    * check_srx_userfw_no_auth_entry_on_pfe_with_ip
    * check_srx_userfw_auth_entry_count_on_pfe
    * check_srx_userfw_clearpass_query_status
    * check_srx_userfw_clearpass_query_counter
    * clear_srx_userfw_clearpass_query_counter
    * request_srx_userfw_query
    * config_srx_userfw_clearpass
    * delete_srx_userfw_clearpass
    """

    def __init__(self, device=None):
        """
        device handle
        """
        self.device = device
        self.commit_timeout = 150
        self.shell_timeout = 60
        self.cli_timeout = 60
        self.interval = 5
        self.retry = 5

        self.dut = dut_tool()

    def config_srx_userfw_webapi(self, device=None, client_ip=None, user=None, password=None, http_port=None, https_port=None, certificate=None, commit=False):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
            **REQUIRED** srx handle

        :param str client_ip:
        *OPTIONAL* IPV4 or IPV6 address of simulator

        :param str user:
        *OPTIONAL* webapi user name

        :param str password:
        *OPTIONAL* password of webapi user

        :param int http_port:
        *OPTIONAL* http port

        :param int https_port:
        *OPTIONAL* https port

        :param str certificate:
        *OPTIONAL* certificate

        :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False

        """

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'set system services webapi '

        if user is not None:
            commands.append(prefix + 'user ' + user)

        if password is not None:
            commands.append(prefix + 'user password ' + password)

        if client_ip is not None:
            commands.append(prefix + 'client ' + client_ip)

        if http_port is not None:
            commands.append(prefix + 'http port ' + str(http_port))

        if https_port is not None:
            commands.append(prefix + 'https port ' + str(https_port))

        if certificate is not None:
            commands.append(prefix + 'https pki-local-certificate ' + certificate)
        else:
            commands.append(prefix + 'https default-certificate')

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        return_value = device.config(command_list=commands).response()

        if commit:
            return_value = device.commit(timeout=self.commit_timeout)
        return return_value

    def delete_srx_userfw_webapi(self, device=None, item=None, client_ip=None, commit=False):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** srx handle

        :param str item:
        *OPTIONAL* delete detailed item of webapi

        :param str client_ip:
        *OPTIONAL* IPV4 or IPV6 address of simulator

        :param str certificate:
        *OPTIONAL* certificate

        :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False

        """

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'delete system services webapi '

        if item == 'password':
            commands.append(prefix + 'user password')
        elif item == 'user':
            commands.append(prefix + 'user')
        elif client_ip is not None:
            commands.append(prefix + 'client ' + client_ip)
        elif item == 'client':
            commands.append(prefix + 'client')
        elif item == 'http port':
            commands.append(prefix + 'http')
        elif item == 'https port':
            commands.append(prefix + 'https port')
        elif item == 'pki-local-certificate':
            commands.append(prefix + 'https pki-local-certificate')
        elif item == 'default-certificate':
            commands.append(prefix + 'https default-certificate')
        elif item == 'https':
            commands.append(prefix + 'https')
        else:
            commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        return_value = device.config(command_list=commands).response()

        if commit:
            return_value = device.commit(timeout=self.commit_timeout)
        return return_value

    def config_srx_userfw_clearpass_userquery(self, device=None, server_name=None, address=None, client_id=None, client_secret=None, method=None, port=None, token_api=None, query_api=None, commit=False):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
            **REQUIRED** srx handle

        :param str server_name:
        **REQUIRED** web server name

        :param str address:
        **REQUIRED** IPV4 or IPV6 address

        :param str client_id:
        **REQUIRED** client id

        :param str client_secret:
        **REQUIRED** client secret

        :param str method:
        *OPTIONAL* connect protocol(http or https)

        :param int port:
        *OPTIONAL* http or https port

        :param str token_api:
        *OPTIONAL* client token_api

        :param str query_api:
        *OPTIONAL* client query_api

        :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False

        """

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'set services user-identification authentication-source aruba-clearpass user-query '

        if server_name is not None:
            commands.append(prefix + 'web-server ' + server_name)

        if address is not None:
            commands.append(prefix + 'web-server address ' + address)

        if client_id is not None:
            commands.append(prefix + 'client-id ' + client_id)

        if client_secret is not None:
            commands.append(prefix + 'client-secret ' + client_secret)

        if method is not None:
            commands.append(prefix + 'web-server connect-method ' + method)

        if port is not None:
            commands.append(prefix + 'web-server port ' + str(port))

        if token_api is not None:
            commands.append(prefix + 'token-api ' + token_api)
        else:
            commands.append(prefix + 'token-api server/token.action')

        if query_api is not None:
            commands.append(prefix + 'query-api ' + query_api)
        else:
            commands.append(prefix + 'query-api "server/query.action?ip=$IP$"')

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        return_value = device.config(command_list=commands).response()

        if commit:
            return_value = device.commit(timeout=self.commit_timeout)
        return return_value

    def delete_srx_userfw_clearpass_userquery(self, device=None, item=None, commit=False):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
            **REQUIRED** srx handle

        :param str item:
        *OPTIONAL* delete detailed item of user-query

        :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False

        """

        if device is None:
            raise Exception("device handle is None.")

        commands = []
        prefix = 'delete services user-identification authentication-source aruba-clearpass user-query '

        if item == 'address':
            commands.append(prefix + 'web-server address')
        elif item == 'method':
            commands.append(prefix + 'web-server connect-method')
        elif item == 'port':
            commands.append(prefix + 'web-server port')
        elif item == 'id':
            commands.append(prefix + 'client-id')
        elif item == 'secret':
            commands.append(prefix + 'client-secret')
        elif item == 'token-api':
            commands.append(prefix + 'client-id')
        elif item == 'query-api':
            commands.append(prefix + 'client-secret')
        else:
            commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        return_value = device.config(command_list=commands).response()

        if commit:
            return_value = device.commit(timeout=self.commit_timeout)
        return return_value

    def check_srx_userfw_no_user_auth_entry(self, device=None, ip=None, auth_source=None, domain=None, node=None, **kwargs):
        """
        Author: John Chen, xjchen@juniper.net

        Check an auth entry should not be found in the specific auth source, return true if entry is not found

        :param str device:
         **REQUIRED** Device handle for the DUT

        :param str ip:
         **OPTIONAL** ip address for the checked entry

        :param str domain:
         **OPTIONAL** Domain name for the auth entry

        :param str auth_source:
         **REQUIRED** auth source for auth entry

        :param str node:
        *OPTIONAL* HA testbed using it

        :param str logical_system:
        *OPTIONAL* logical system name
        """
        if device is None:
            raise Exception("device handle is None")

        logical_system = kwargs.get("logical_system")

        base_cmd = "show services user-identification authentication-table authentication-source"
        if auth_source is None:
            cmd_list = base_cmd + " all "
        elif auth_source.lower() == 'active-directory' or auth_source.lower() == 'aruba-clearpass':
            cmd_list = base_cmd + " " + auth_source
        else:
            cmd_list = base_cmd + " identity-management source-name " + "\"" + auth_source + "\""
        if domain is not None:
            cmd_list = cmd_list + " domain " + domain
        if node is not None:
            cmd_list = cmd_list + " node " + node
        if logical_system is not None:
            cmd_list = cmd_list + " logical-system " + logical_system

        return_value = device.cli(device=device, command=cmd_list, timeout=self.cli_timeout).response()
        if ip is None:
            if re.search(r"warning|error:\s*.*", return_value, re.S):
                return True
            else:
                device.log(level='ERROR', message="Found auth entry")
                raise Exception("Found the unexpected entry")
        else:
            if re.search(r"{}".format(ip), return_value, re.S):
                device.log(level='ERROR', message="Found the unexpected entry")
                raise Exception("Found the unexpected entry")
            else:
                device.log(level='INFO', message="Did not find the unexpected entry")
                return True

    def check_srx_userfw_auth_table_number(self, device=None, domain=None, total_number=0, node=None, **kwargs):
        """
        Author: John Chen, xjchen@juniper.net

        Check total auth entries number per domain on RE

        :param str device:
         **REQUIRED** Device handle for the DUT

        :param str domain:
         **OPTIONAL** Domain name for the auth entry

        :param str total_number:
         **REQUIRED** Total number for auth entries

        :param str node:
        *OPTIONAL* HA testbed using it

        :param str logical_system:
        *OPTIONAL* logical system name
        """
        if device is None:
            raise Exception("device handle is None")

        logical_system = kwargs.get("logical_system")
        auth_source = kwargs.get("auth_source")
        retry = int(kwargs.get("retry", self.retry))
        interval = int(kwargs.get("interval", self.interval))
        total_number = int(total_number)

        base_cmd = "show services user-identification authentication-table authentication-source"
        if auth_source is None:
            cmd_list = base_cmd + " all "
        elif auth_source.lower() == 'active-directory' or auth_source.lower() == 'aruba-clearpass':
            cmd_list = base_cmd + " " + auth_source
        else:
            cmd_list = base_cmd + " identity-management source-name " + "\"" + auth_source + "\""
        if domain is not None:
            cmd_list = cmd_list + " domain " + domain
        if node is not None:
            cmd_list = cmd_list + " node " + node
        if logical_system is not None:
            cmd_list = cmd_list + " logical-system " + logical_system
        i = 1
        while i <= int(retry):
            return_value = device.cli(device=device, command=cmd_list).response()
            if total_number != 0:
                # total number is not 0, check if cli output matchs r"Total\s+entries:\s*(\d+)"
                match = re.search(r"Total\s+entries:\s*(\d+)", return_value, re.S)
                device.log(level='DEBUG', message="Expected total_number in domain {} should be {}".format(domain, total_number))
                if match:
                    # cli output has auth entries, then check the total number
                    real_number = int(match.group(1))
                    if total_number <= real_number:
                        # total_number is correct, keyword return true
                        device.log(level='INFO', message="Expected total_number in domain is correct")
                        return True
            else:
                # total number is 0, needs to retry int(retry) times to double confirm the auth entry number is 0. Sometime userid needs takes time to get the auth entries or userid is not up
                if not re.search(r"warning|error:\s*.*", return_value, re.S):
                    # cli output doesn't match r"warning|error:\s*.*", means found auth entries or output error, reture false
                    device.log(level='ERROR', message="Match Total number failed, expected should be 0, but cli output is {}".format(return_value))
                    raise Exception("total auth number not match")
            time.sleep(int(interval))
            i += 1
        # exit from loop with i>int(retry), now either "total_number is 0 and match pattern" or "total_number is not 0 and match pattern"
        if total_number == 0 and re.search(r"warning:\s*.*", return_value, re.S):
            # after int(retry) times check, if cli ouput still matches r"warning:\s*.*", means no auth entry
            device.log(level='INFO', message="Expected total_number is 0, it is correct")
            return True
        else:
            device.log(level='ERROR', message="Match Total number timeout, expected should be {}, but get {}".format(total_number, return_value))
            raise Exception("match total auth number timeout")

    def check_srx_userfw_device_entry_number(self, device=None, domain=None, total_number=0, node=None, **kwargs):
        """
        Author: John Chen, xjchen@juniper.net

        Check total device entries number per domain on RE

        :param str device:
         **REQUIRED** Device handle for the DUT

        :param str domain:
         **REQUIRED** Domain name for the auth entry

        :param str total_number:
         **REQUIRED** Total number for auth entries

        :param str node:
        *OPTIONAL* HA testbed using it

        :param str logical_system:
        *OPTIONAL* logical system name
        """
        if device is None:
            raise Exception("device handle is None")
        if domain is None:
            raise Exception("domain name is None")

        logical_system = kwargs.get("logical_system")
        retry = int(kwargs.get("retry", self.retry))
        interval = int(kwargs.get("interval", self.interval))
        total_number = int(total_number)

        cmd_list = "show services user-identification device-information table all" + " domain " + domain

        if node is not None:
            cmd_list = cmd_list + " node " + node
        if logical_system is not None:
            cmd_list = cmd_list + " logical-system " + logical_system
        i = 1
        while i <= int(retry):
            return_value = device.cli(device=device, command=cmd_list).response()
            if total_number != 0:
                # total number is not 0, check if cli output matchs r"Total\s+entries:\s*(\d+)"
                match = re.search(r"Total\s+entries:\s*(\d+)", return_value, re.S)
                device.log(level='DEBUG', message="Expected total_number in domain {} should be {}".format(domain, total_number))
                if match:
                    # cli output has auth entries, then check the total number
                    real_number = int(match.group(1))
                    if total_number <= real_number:
                        # total_number is correct, keyword return true
                        device.log(level='INFO', message="Expected total_number in domain is correct")
                        return True
            else:
                # total number is 0, needs to retry int(retry) times to double confirm the auth entry number is 0. Sometime userid needs takes time to get the auth entries or userid is not up
                if not re.search(r"warning|error:\s*.*", return_value, re.S):
                    # cli output doesn't match r"warning|error:\s*.*", means found auth entries or output error, reture false
                    device.log(level='ERROR', message="Match Total number failed, expected should be 0, but cli output is {}".format(return_value))
                    raise Exception("total auth number not match")
            time.sleep(int(interval))
            i += 1
        # exit from loop with i>int(retry), now either "total_number is 0 and match pattern" or "total_number is not 0 and match pattern"
        if total_number == 0 and re.search(r"warning:\s*.*", return_value, re.S):
            # after int(retry) times check, if cli ouput still matches r"warning:\s*.*", means no auth entry
            device.log(level='INFO', message="Expected total_number is 0, it is correct")
            return True
        else:
            device.log(level='ERROR', message="Match Total number timeout, expected should be {}, but get {}".format(total_number, return_value))
            raise Exception("match total auth number timeout")

    def check_srx_userfw_clearpass_auth_table_on_pfe(self, device=None, ip=None, user=None, domain=None, state="valid", group_number=0, node=None):
        """
        Author: Terry Peng, tpeng@juniper.net

        Check Clear Pass auth entry on PFE

        :param str device:
         **REQUIRED** Device handle for the DUT

        :param str ip:
         **REQUIRED** IP address for the auth entry

        :param str user:
         **REQUIRED** User name for the auth entry

        :param str domain:
         **REQUIRED** Domain name for the auth entry

        :param str state:
         **REQUIRED** State for the auth entry

        :param str group_number:
         **REQUIRED** Group number for the auth entry

        :param str node:
        *OPTIONAL* HA testbed using it
        """

        if device is None:
            raise Exception("device handle is None")
        group_number = int(group_number)
        base_cmd = "plugin jsf_userfw show cp-auth ip-address"
        cmd_list = []

        if ip is not None:
            cmd_list.append(base_cmd + " " + ip)

        if node is not None:
            response = self.dut.send_vty_cmd(
                device=device,
                node=node,
                component="SPU",
                cmd=cmd_list,
            )
        else:
            response = self.dut.send_vty_cmd(
                device=device,
                component="SPU",
                cmd=cmd_list,
            )

        real_ip = re.search(r"IP\s*address:\s+(.*?)[\r\n]", response, re.S).group(1)
        device.log(level='DEBUG', message="get the real_ip {} on PFE".format(real_ip))

        match_ip = ipaddress.ip_address(real_ip)

        if ipaddress.ip_address(match_ip) == ipaddress.ip_address(ip):
            if user is not None:
                if re.search(r"User\s*Name:\s*{}".format(user), response, re.S) is None:
                    raise Exception('user can not found in auth entry')
            if domain is not None:
                if "." in domain:
                    new_domain = re.sub(r'\.', r'\\.', domain)
                    if re.search(r"Domain\s*Name:\s*{}".format(new_domain), response, re.S) is None:
                        raise Exception('domain can not found in auth entry')
            if state is not None:
                if re.search(r"State:\s*{}".format(state), response, re.S) is None:
                    raise Exception('state is not correct in auth entry')
            if group_number is not None:
                if re.search(r"Group\s*number:\s*{}".format(group_number), response, re.S) is None:
                    raise Exception('group number is not correct in auth entry')
            device.log(level='DEBUG', message="get the correct auth table on dut")
            return True
        else:
            raise Exception('this auth entry can not be found on PFE')

    def show_srx_userfw_auth_table_all(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str source:
        *OPTIONAL* source  [active-directory  |  aruba-clearpass  |  identity-management  |all]

        :param str user:
        *OPTIONAL* user name

        :param str group:
        *OPTIONAL* group name

        :param str domain:
        *OPTIONAL* domain name

        :param str node:
        *OPTIONAL* which node, 0 or 1

        """

        source = kwargs.get("source", 'all')
        user = kwargs.get("user")
        group = kwargs.get("group")
        domain = kwargs.get("domain")
        node = kwargs.get("node")
        logical_system = kwargs.get("logical_system")

        if device is None:
            raise Exception("device handle is None")

        prefix = 'show services user-identification authentication-table authentication-source ' + source

        if node is not None:

            if user is not None and domain is None:
                command_line = prefix + ' user ' + user + ' node ' + node
            elif user is not None and domain is not None:
                command_line = prefix + ' user ' + user + ' domain ' + domain + ' node ' + node
            elif group is not None and domain is None:
                command_line = prefix + ' group ' + group + ' node ' + node
            elif group is not None and domain is not None:
                command_line = prefix + ' group ' + group + ' domain ' + domain + ' node ' + node
            elif domain is not None:
                command_line = prefix + ' domain ' + domain + ' node ' + node
            else:
                command_line = prefix + ' node ' + node

        else:
            if user is not None and domain is None:
                command_line = prefix + ' user ' + user
            elif user is not None and domain is not None:
                command_line = prefix + ' user ' + user + ' domain ' + domain
            elif group is not None and domain is None:
                command_line = prefix + ' group ' + group
            elif group is not None and domain is not None:
                command_line = prefix + ' group ' + group + ' domain ' + domain
            elif domain is not None:
                command_line = prefix + ' domain ' + domain
            else:
                command_line = prefix

        if logical_system is not None:
            command_line = command_line + ' logical-system ' + logical_system

        device.log(level='DEBUG', message='Configuration command_line gathered from the function: ')
        device.log(level='DEBUG', message=command_line)
        return_value = device.cli(command=command_line, timeout=self.cli_timeout).response()
        return return_value

    def delete_srx_userfw_auth_table_by_request(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str ip:
        *OPTIONAL* ip address

        :param str source:
        *OPTIONAL* source  [active-directory  |  aruba-clearpass  |  identity-management  |all]
        :param str source_name:
        *OPTIONAL* source_name of the auth source when the auth source is other source than  active-directory ,aruba-clearpass, identity-management and all

        :param str domain:
        *OPTIONAL* domain name

        :param str user:
        *OPTIONAL* user name

        :param str group:
        *OPTIONAL* group name

        """

        ip = kwargs.get("ip")
        source = kwargs.get("source", 'all')
        source_name = kwargs.get("source_name")
        user = kwargs.get("user")
        group = kwargs.get("group")
        domain = kwargs.get("domain")

        if device is None:
            raise Exception("device handle is None")
        prefix_basic = "request services user-identification authentication-table delete "
        if source_name is not None:
            prefix = prefix_basic + 'authentication-source identity-management source-name ' + "\"" + source_name + "\""
        else:
            prefix = prefix_basic + "authentication-source " + source
        if ip is not None:
            command_line = prefix_basic + 'ip-address ' + ip
        elif user is not None and domain is not None:
            command_line = prefix + ' user ' + user + ' domain ' + domain
        elif group is not None and domain is not None:
            command_line = prefix + ' group ' + group + ' domain ' + domain
        elif domain is not None:
            command_line = prefix + ' domain ' + domain
        elif user is not None:
            command_line = prefix + ' user ' + user
        elif group is not None:
            command_line = prefix + ' group ' + group
        else:
            command_line = prefix
        device.log(level='DEBUG', message='Configuration command_line gathered from the function: ')
        device.log(level='DEBUG', message=command_line)
        return_value = device.cli(command=command_line, timeout=self.cli_timeout).response()
        return return_value

    def check_srx_userfw_no_auth_entry_on_pfe_with_ip(self, device=None, node=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
         **REQUIRED** Device handle for the DUT

        :param str ip:
         **REQUIRED** IP address for the auth entry

        :param str userfw_type:
         **REQUIRED** userfw_type  (ad-auth  | cp-auth  |local-auth-table)

        :param str node:
        *OPTIONAL* HA testbed using it
        """

        userfw_type = kwargs.get("userfw_type", 'cp-auth')
        ip = kwargs.get("ip")

        if device is None:
            raise Exception("device handle is None")

        if ip is not None:
            command_line = 'plugin jsf_userfw show ' + userfw_type + ' ip-address ' + ip
        else:
            raise Exception("ip is None")

        if node is not None:
            response = self.dut.send_vty_cmd(
                device=device,
                node=node,
                component="SPU",
                cmd=command_line,
            )
        else:
            response = self.dut.send_vty_cmd(
                device=device,
                component="SPU",
                cmd=command_line,
            )

        if re.search(r"{}".format(ip), response, re.M):
            raise Exception("the specified IP exist on PFE, this's unexpected.\n")
        else:
            device.log(level='INFO', message="the specified IP doesn't exist, this's expected.")

        return True

    def check_srx_userfw_auth_entry_count_on_pfe(self, device=None, node=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
         **REQUIRED** Device handle for the DUT

        :param str userfw_type:
         **REQUIRED** userfw_type  (ad-auth  | cp-auth  |local-auth-table)

        :param int count:
         **REQUIRED** auth entry count on pfe

        :param str node:
        *OPTIONAL* HA testbed using it
        """

        userfw_type = kwargs.get("userfw_type", 'cp-auth')
        count = kwargs.get("count")

        if device is None:
            raise Exception("device handle is None")

        command_line = 'plugin jsf_userfw show ' + userfw_type + ' table brief'

        if node is not None:
            response = self.dut.send_vty_cmd(
                device=device,
                node=node,
                component="SPU",
                cmd=command_line,
            )
        else:
            response = self.dut.send_vty_cmd(
                device=device,
                component="SPU",
                cmd=command_line,
            )

        result = re.search(r"total\s*auth\s*entry\s*count:\s*(\d+)", response, re.M)
        get_count = result.group(1)
        device.log(level='DEBUG', message="getting count is {}".format(get_count))
        device.log(level='DEBUG', message="inputing count is {}".format(count))

        if int(get_count) >= int(count):
            device.log(level='DEBUG', message="auth entry is expected value on pfe.")
        else:
            raise Exception("auth entry is unexpected value on pfe.\n")

        return True

    def check_srx_userfw_clearpass_query_status(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str ip:
        **REQUIRED** ip address

        :param str status:
        **REQUIRED** query connect status   [Online|Offline]

        """

        ip = kwargs.get("ip", '1.1.1.1')
        status = kwargs.get("status", 'Online')

        if device is None:
            raise Exception("device handle is None")

        time.sleep(10)
        response = device.cli(command='show services user-identification authentication-source aruba-clearpass user-query status', timeout=self.cli_timeout).response()

        result = re.search(r"Web\s+server\s+Address:\s+(.*?)[\r\n]", response, re.S)
        get_ip = result.group(1)

        if get_ip != ip:
            raise Exception("------input ip doesn't match get ip!------\n")

        result = re.search(r"Status:\s+(\w+)[\r\n]", response, re.S)
        get_status = result.group(1)
        if get_status != status:
            raise Exception("------input status doesn't match get status!------\n")

        return True

    def check_srx_userfw_clearpass_query_counter(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str ip:
        **REQUIRED** ip address

        :param int request_number:
        *OPTIONAL* request query number

        :param int response_number:
        *OPTIONAL* response query number

        :param bool online:
        *OPTIONAL* default value is True, True is 1, False is 0

        :param bool offline:
        *OPTIONAL* default value is True, True is 1, False is 0

        """

        ip = kwargs.get("ip", '1.1.1.1')
        request_number = kwargs.get("request_number")
        response_number = kwargs.get("response_number")
        online = kwargs.get("online", 1)
        offline = kwargs.get("offline", 0)

        if device is None:
            raise Exception("device handle is None")

        response = device.cli(command='show services user-identification authentication-source aruba-clearpass user-query counters', timeout=self.cli_timeout).response()

        result = re.search(r"Web\s+server\s+Address:\s+(.*?)[\r\n]", response, re.S)
        get_ip = result.group(1)

        if get_ip != ip:
            raise Exception("------input ip doesn't match get ip!------\n")

        result = re.search(r"Access\s+token:\s+(.*?)[\r\n]", response, re.S)
        token_info = result.group(1)

        if online and token_info != 'NULL':
            device.log(level='INFO', message="when query is online, token isn't NULL, it's expected")
        elif offline and token_info == 'NULL':
            device.log(level='INFO', message="when query is offline, token is NULL, it's expected")
        else:
            raise Exception("------token is unexpected, please check token connect status!------\n")

        if request_number is not None:
            result = re.search(r"Request\s+sent\s+number:\s+(\w+)[\r\n]", response, re.S)
            get_request_number = result.group(1)
            if int(get_request_number) < int(request_number):
                raise Exception("------request number is unexpected!------\n")

        if response_number is not None:
            result = re.search(r"Total\s+response\s+received\s+number:\s+(\w+)[\r\n]", response, re.S)
            get_response_number = result.group(1)
            if int(get_response_number) < int(response_number):
                raise Exception("------response number is unexpected!------\n")
        return True

    def clear_srx_userfw_clearpass_query_counter(self, device=None):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        """

        if device is None:
            raise Exception("device handle is None")

        device.cli(command='clear services user-identification authentication-source aruba-clearpass user-query counters', timeout=self.cli_timeout)
        return True

    def request_srx_userfw_query(self, device=None, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** Device handle for the DUT

        :param str ip:
        **REQUIRED** request ip address

        :param str userfw_type:
        **REQUIRED** userfw query type [ad | cp |jims]

        """

        ip = kwargs.get("ip", '1.1.1.1')
        userfw_type = kwargs.get("userfw_type", 'ad')

        if device is None:
            raise Exception("device handle is None")

        if userfw_type == 'ad':
            response = device.cli(command='request services user-identification active-directory-access ip-user-probe address ' + ip, timeout=self.cli_timeout).response()
        elif userfw_type == 'cp':
            response = device.cli(command='request services user-identification authentication-source aruba-clearpass user-query address ' + ip, timeout=self.cli_timeout).response()
        elif userfw_type == 'jims':
            response = device.cli(command='request services user-identification identity-management ip-query address ' + ip, timeout=self.cli_timeout).response()
        else:
            response = device.cli(command='request services user-identification active-directory-access ip-user-probe address ' + ip, timeout=self.cli_timeout).response()

        if re.search('error', response):
            raise Exception("------do request query failed!------\n")

        time.sleep(5)
        return True

    def config_srx_userfw_clearpass(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** srx handle

        :param int entry_timeout:
        *OPTIONAL* entry timeout value

        :param int invalid_timeout:
        *OPTIONAL* invalid timeout value

        :param str no_user_query:
        *OPTIONAL* no user query

        :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False

        """

        entry_timeout = kwargs.get("entry_timeout")
        invalid_timeout = kwargs.get("invalid_timeout")
        no_user_query = kwargs.get("no_user_query")

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'set services user-identification authentication-source aruba-clearpass '

        if entry_timeout is not None:
            commands.append(prefix + 'authentication-entry-timeout ' + str(entry_timeout))

        if invalid_timeout is not None:
            commands.append(prefix + 'invalid-authentication-entry-timeout ' + str(invalid_timeout))

        if no_user_query is not None:
            commands.append(prefix + 'no-user-query')

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        return_value = device.config(command_list=commands).response()

        if commit:
            return_value = device.commit(timeout=self.commit_timeout)
        return return_value

    def delete_srx_userfw_clearpass(self, device=None, commit=False, **kwargs):
        """
        Author: Ruby Wu, rubywu@juniper.net

        :param str device:
        **REQUIRED** srx handle

        :param int entry_timeout:
        *OPTIONAL* entry timeout value

        :param int invalid_timeout:
        *OPTIONAL* invalid timeout value

        :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False

        """

        entry_timeout = kwargs.get("entry_timeout")
        invalid_timeout = kwargs.get("invalid_timeout")
        item = kwargs.get("item")

        if device is None:
            raise Exception("device handle is None")

        commands = []
        prefix = 'delete services user-identification authentication-source aruba-clearpass '

        if entry_timeout is not None:
            commands.append(prefix + 'authentication-entry-timeout ' + str(entry_timeout))
        elif invalid_timeout is not None:
            commands.append(prefix + 'invalid-authentication-entry-timeout ' + str(invalid_timeout))
        elif item == 'authentication-entry-timeout':
            commands.append(prefix + 'authentication-entry-timeout')
        elif item == 'invalid-authentication-entry-timeout':
            commands.append(prefix + 'invalid-authentication-entry-timeout')
        elif item == 'no-user-query':
            commands.append(prefix + 'no-user-query')
        else:
            commands.append(prefix)

        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        return_value = device.config(command_list=commands).response()

        if commit:
            return_value = device.commit(timeout=self.commit_timeout)
        return return_value
