#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: pptp linux keywords
Author: sebrinazhao, sebrinazhao@juniper.net
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments

import re
import time


class alg_linux(object):
    """
    Description: pptp linux keywords
    keywords list:
    *
    * config_linux_pptp_client_option
    * config_linux_pptp_client_chap_secrets
    * config_linux_pptp_client_peers
    * config_linux_pptp_server_options_pptpd
    * config_linux_pptp_server_pptpd
    * config_linux_pptp_server_chap_secrets
    * set_linux_service_pptp_status
    * config_linux_pptp_client
    * send_linux_pptp
    *
    """

    def __init__(self, device=None):
        """
        Description: device handle
        """
        self.device = device
        self.shell_timeout = 60

    def config_linux_pptp_client_option(self, device=None, **kwargs):
        """
        Description: Setup PPTP client configuration file of /etc/ppp/options.pptp
        Author: Sebrina Zhao, sebrinazhao@juniper.net

        param str device:
        **REQUIRED** handle of linux PC

        param str pptp_client_option_file_all:
        **REQUIRED** whole path and file name about pptp option configuration file for pptp client pc

        param str pptp_client_option_file_bak_all:
        **REQUIRED** whole path and file name about pptp option configuration bakup file for pptp client pc
        """

        option_file = kwargs.get("option_file_all", '/etc/ppp/options.pptp')
        option_file_bak = kwargs.get("option_file_bak", '/etc/ppp/options_bak.pptp')

        if device is None:
            raise Exception("------device handle is None!------\n")

        timeout = kwargs.get("timeout", self.shell_timeout)

        device.su()

        device.shell(command='/bin/mv ' + option_file + ' ' + option_file_bak, timeout=timeout)
        device.shell(command='/bin/rm -rf ' + ' ' + option_file, timeout=timeout)
        device.shell(command='/bin/ls -l' + ' ' + option_file, timeout=timeout)

        device.shell(command='echo -e "lock"  >' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "noauth"  >>' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "nobsdcomp"  >>' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "nodeflate" >>' + ' ' + option_file, timeout=timeout)

        device.shell(command='/bin/ls -l' + ' ' + option_file, timeout=timeout)
        device.shell(command='more' + ' ' + option_file, timeout=timeout)

        return True

    def config_linux_pptp_client_chap_secrets(self, device=None, **kwargs):
        """
        Description: Setup PPTP client configuration file of /etc/ppp/chap-secrets
        Author: Sebrina Zhao, sebrinazhao@juniper.net

        param str device:
        **REQUIRED** handle of linux PC

        param str chap_secrets_file:
        **REQUIRED** whole path and file name about pptp chap-secrets configuration file for pptp client pc

        param str chap_secrets_file_bak:
        **REQUIRED** whole path and file name about pptp chap-secrets configuration bakup file for pptp client pc
        """

        chap_secrets_file = kwargs.get("chap_secrets_file", '/etc/ppp/chap-secrets')
        chap_secrets_file_bak = kwargs.get("chap_secrets_file_bak", '/etc/ppp/chap-secrets_bak')
        timeout = kwargs.get("timeout", self.shell_timeout)

        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.shell(command='/bin/mv ' + chap_secrets_file + ' ' + chap_secrets_file_bak, timeout=timeout)
        device.shell(command='/bin/rm -rf ' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='/bin/ls -l' + ' ' + chap_secrets_file, timeout=timeout)

        device.shell(command='echo -e "# Secrets for authentication using CHAP" >' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "# client    server    secret         IP addresses" >> ' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "pptpuser    v4server    Abcd1234       *" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "pptpuser    v6server    Abcd1234       *" >>' + ' ' + chap_secrets_file, timeout=timeout)

        device.shell(command='/bin/ls -l' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='more' + ' ' + chap_secrets_file, timeout=timeout)
        return True

    def config_linux_pptp_client_peers(self, device=None, **kwargs):
        """
        Description: Setup PPTP client configuration file of /etc/ppp/peers/vpnipv4
        Author: Sebrina Zhao, sebrinazhao@juniper.net

        param str device:
        **REQUIRED** handle of linux PC

        param str chap_secrets_file:
        **REQUIRED** whole path and file name about pptp peers configuration file for pptp client pc

        param str peers_file_bak:
        **REQUIRED** whole path and file name about pptp peers configuration bakup file for pptp client pc

        """

        peers_file = kwargs.get("peers_file", '/etc/ppp/peers/vpnipv4')
        peers_file_bak = kwargs.get("peers_file_bak", '/etc/ppp/peers/vpnipv4_bak')
        timeout = kwargs.get("timeout", self.shell_timeout)
        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.shell(command='/bin/mv ' + peers_file + ' ' + peers_file_bak, timeout=timeout)
        device.shell(command='/bin/rm -rf ' + ' ' + peers_file, timeout=timeout)
        device.shell(command='/bin/ls -l ' + ' ' + peers_file, timeout=timeout)

        device.shell(command='echo -e "remotename v4server" >' + ' ' + peers_file, timeout=timeout)
        device.shell(command='echo -e "linkname   v4server" >> ' + ' ' + peers_file, timeout=timeout)
        device.shell(command='echo -e "ipparam    vpnipv4" >>' + ' ' + peers_file, timeout=timeout)
        device.shell(command='echo -e "name pptpuser" >>' + ' ' + peers_file, timeout=timeout)
        device.shell(command='echo -e "usepeerdns" >>' + ' ' + peers_file, timeout=timeout)
        device.shell(command='echo -e "noauth" >> ' + ' ' + peers_file, timeout=timeout)
        device.shell(command='echo -e "require-mppe" >>' + ' ' + peers_file, timeout=timeout)
        device.shell(command='echo -e "file /etc/ppp/options.pptp" >>' + ' ' + peers_file, timeout=timeout)

        device.shell(command='/bin/ls -l' + ' ' + peers_file, timeout=timeout)
        device.shell(command='more' + ' ' + peers_file, timeout=timeout)

        return True

    def config_linux_pptp_server_options(self, device=None, **kwargs):
        """
        Description: Setup PPTP client configuration file of /usr/local/pptpd/etc/pptpd.conf
        Author: Sebrina Zhao, sebrinazhao@juniper.net

        param str device:
        **REQUIRED** handle of linux PC

        param str option_file:
        **REQUIRED** whole path and file name about pptp pptpd options file for pptp server pc

        param str option_file_bak:
        **REQUIRED** whole path and file name about pptp pptpd options configuration bakup file for pptp server pc
        """
        option_file = kwargs.get("option_file", '/usr/local/pptpd/etc/options.pptpd')
        timeout = kwargs.get("timeout", self.shell_timeout)
        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()
        device.shell(command='echo -e "name v4server" >' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "refuse-pap" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "refuse-chap" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "refuse-mschap" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "require-mschap-v2" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "require-mppe-128" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "nomppe-stateful" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "ms-dns 208.67.222.222" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "ms-dns 208.67.220.220" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "proxyarp" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "debug" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "lock" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "nobsdcomp" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "novj" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "novjccomp" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "nologfd" >> ' + ' ' + option_file, timeout=timeout)
        device.shell(command='echo -e "ipparam pptpd" >> ' + ' ' + option_file, timeout=timeout)

        device.shell(command='/bin/ls -l' + ' ' + option_file, timeout=timeout)
        device.shell(command='more' + ' ' + option_file, timeout=timeout)

        return True

    def config_linux_pptp_server_pptpd(self, device=None, **kwargs):
        """
        Description: Setup PPTP client configuration file of /usr/local/pptpd/etc/pptpd.conf
        Author: Sebrina Zhao, sebrinazhao@juniper.net

        param str device:
        **REQUIRED** handle of linux PC

        param str pptpd_file:
        **REQUIRED** whole path and file name about pptp pptpd file for pptp server pc

        param str pptpd_file_bak:
        **REQUIRED** whole path and file name about pptp pptpd configuration bakup file for pptp server pc
        """
        pptpd_file = kwargs.get("pptpd_file", '/usr/local/pptpd/etc/pptpd.conf')
        pptpd_file_bak = kwargs.get("pptpd_file_bak", '/usr/local/pptpd/etc/pptpd.conf_bak')
        timeout = kwargs.get("timeout", self.shell_timeout)
        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.shell(command='/bin/mv ' + pptpd_file + ' ' + pptpd_file_bak, timeout=timeout)
        device.shell(command='/bin/rm -rf ' + ' ' + pptpd_file, timeout=timeout)
        device.shell(command='/bin/ls -l ' + ' ' + pptpd_file, timeout=timeout)

        device.shell(command='echo -e "option /usr/local/pptpd/etc/options.pptpd" >' + ' ' + pptpd_file, timeout=timeout)
        device.shell(command='echo -e "debug" >> ' + ' ' + pptpd_file, timeout=timeout)
        device.shell(command='echo -e "stimeout 30" >>' + ' ' + pptpd_file, timeout=timeout)

        # device.shell(command='echo -e "localip 110.110.110.254" >>' + ' ' + pptpd_file)
        # device.shell(command='echo -e "remoteip 110.110.100.110.200-210" >>' + ' ' + pptpd_file)

        device.shell(command='/bin/ls -l' + ' ' + pptpd_file, timeout=timeout)
        device.shell(command='more' + ' ' + pptpd_file, timeout=timeout)

        return True

    def config_linux_pptp_server_chap_secrets(self, device=None, **kwargs):
        """
        Description: Setup PPTP client configuration file of /etc/ppp/chap-secrets
        Author: Sebrina Zhao, sebrinazhao@juniper.net

        param str device:
        **REQUIRED** handle of linux PC

        param str chap_secrets_file:
        **REQUIRED** whole path and file name about pptp chap-secrets file for pptp server pc

        param str chap_secrets_file_bak:
        **REQUIRED** whole path and file name about pptp chap-secrets configuration bakup file for pptp server pc
        """
        chap_secrets_file = kwargs.get("chap_secrets_file", '/etc/ppp/chap-secrets')
        chap_secrets_file_bak = kwargs.get("chap_secrets_file_bak", '/etc/ppp/chap-secrets_bak')
        timeout = kwargs.get("timeout", self.shell_timeout)
        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.shell(command='/bin/mv ' + chap_secrets_file + ' ' + chap_secrets_file_bak, timeout=timeout)
        device.shell(command='/bin/rm -rf ' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='/bin/ls -l ' + ' ' + chap_secrets_file, timeout=timeout)

        device.shell(command='echo -e "# PPTP User Accounts" >' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "# username server_name password ip" >> ' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "pptpuser   v4server    Abcd1234  *" >>' + ' ' + chap_secrets_file, timeout=timeout)

        device.shell(command='/bin/ls -l' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='more' + ' ' + chap_secrets_file, timeout=timeout)

        return True

    def set_linux_service_pptp_status(self, device=None, **kwargs):
        """
        Description: restart PPTP service of PPTPD on PPTP server
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        timeout = kwargs.get("timeout", self.shell_timeout)
        if device is None:
            raise Exception("------device handle is None!------\n")
        device.shell(command='killall pptpd')

        device.shell(command='killall jpptpd')

        device.shell(command='netstat -an | grep 1723')

        device.shell(command='/usr/local/pptpd/sbin/jpptpd -c /usr/local/pptpd/etc/pptpd.conf -o /usr/local/pptpd/etc/options.pptpd --ipver 4')
        device.shell(command='/usr/sbin/pptpd -c /etc/pptpd.conf -o /etc/ppp/options.pptpd')
        device.shell(command='netstat -an | grep 1723')

        response = device.shell(command='netstat -an | grep 1723', timeout=timeout).response()
        if re.search(r"0.0.0.0:1723", response) is None:
            raise Exception("------restart pptp service failed!------\n")

        return True

    def config_linux_pptp_client(self, device=None, **kwargs):
        """
        Description: Setup PPTP client configuration file of /etc/ppp/chap-secrets for testcase1
        Author: Sebrina Zhao, sebrinazhao@juniper.net
        param int timeout:
            *OPTIONAL* Server start timeout. Default: 300
        """
        timeout = kwargs.get("timeout", self.shell_timeout)
        chap_secrets_file = kwargs.get("chap_secrets_file", '/etc/ppp/peers/vpnipv4')
        chap_secrets_file_bak = kwargs.get("chap_secrets_file_bak", '/etc/ppp/peers/vpnipv4_bak')

        server_ip = kwargs.get("server_ip", '1.1.1.1')

        if device is None:
            raise Exception("------device handle is None!------\n")

        device.su()

        device.shell(command='/bin/mv ' + chap_secrets_file + ' ' + chap_secrets_file_bak, timeout=timeout)
        device.shell(command='/bin/rm -rf ' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='/bin/ls -l ' + ' ' + chap_secrets_file, timeout=timeout)

        device.shell(command='echo -e "pty \\\"pptp' + ' ' + server_ip + ' --nolaunchpppd\\\"" >' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "remotename v4server" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "linkname v4server" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "ipparam vpnipv4" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "name pptpuser" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "usepeerdns" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "noauth" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "require-mppe" >>' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='echo -e "file /etc/ppp/options.pptp" >>' + ' ' + chap_secrets_file, timeout=timeout)

        device.shell(command='/bin/ls -l' + ' ' + chap_secrets_file, timeout=timeout)
        device.shell(command='more' + ' ' + chap_secrets_file, timeout=timeout)

        return True

    def send_linux_pptp(self, device=None, **kwargs):
        """Description: dial off or dail on pptp connection on pptp client pc
        :Author: Sebrina Zhao, sebrinazhao@juniper.net
        """
        timeout = kwargs.get("timeout", self.shell_timeout)
        operator = kwargs.get("operator", "pon")

        if device is None:
            raise Exception("------wrong: device handle is None!------\n")

        device.su()
        device.log(level='INFO', message="------operator------")
        device.shell(command='cd /etc/ppp/peers', timeout=timeout)
        device.shell(command=operator + ' vpnipv4', timeout=timeout)

        # test operator is pptp_start:
        if operator == "pon":
            time.sleep(5)
            response = device.shell(command='ifconfig', timeout=timeout).response()
            device.log(level='INFO', message="------response:------ {}".format(response))
            if "ppp0" not in response:
                raise Exception("------dail ppp failed and can not find inf ppp0!------\n")
        return True
