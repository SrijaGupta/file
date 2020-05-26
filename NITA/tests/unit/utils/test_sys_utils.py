import os
import unittest
import logging
from mock import patch
from unittest import mock
from subprocess import getoutput

from jnpr.toby.utils.sys_utils import ascii2hex
from jnpr.toby.utils.sys_utils import inttohex
#from jnpr.toby.utils.sys_utils import sleep
from jnpr.toby.utils.sys_utils import get_idp_predefined_service_hash
from jnpr.toby.utils.sys_utils import compare_list_of_dict
from jnpr.toby.utils.sys_utils import compare_dict
from jnpr.toby.utils.sys_utils import compare_list_of_list
from jnpr.toby.utils.sys_utils import compare_list
from jnpr.toby.utils.sys_utils import file_presence_search
from jnpr.toby.utils.sys_utils import extract_arp_packet_from_capture
from jnpr.toby.utils.sys_utils import extract_icmpv6_packet_from_capture

class test_sys_utils(unittest.TestCase):
    def setUp(self):
        logging.info("\n##################################################\n")

    def tearDown(self):
        logging.info("\n##################################################\n")

    def test_ascii2hex(self):
        logging.info(".........Test : ascii2hex ............")
        logging.info("Test case 1: convert pass")
        asscii = {'string': 'test pass'}
        expected = '74 65 73 74 20 70 61 73 73'
        test = ascii2hex(**asscii)
        self.assertEqual(test, expected, "String is not equal as expectation")
        logging.info("\tPassed")

    def test_inttohex(self):
        logging.info(".........Test : inttohex ............")
        ###################################################################
        logging.info("Test case 1: convert pass")
        int_ = {'integer': 100, 'bytelen': 2}
        expected = '0064'
        test = inttohex(**int_)

        self.assertEqual(test, expected, "Return is not as expectation")
        logging.info("\tPassed")

#    def test_sleep(self):
#        logging.info(".........Test : sleep ............")
#        ###################################################################
#        logging.info("Test case 1: Sleep with valid time")
#        time = 2
#
#        self.assertIsNone(sleep(time), "Run sleep function without error")
#        logging.info("\tPassed")
#
#        ###################################################################
#        logging.info("Test case 2: Sleep with invalid time")
#        time = "abc"
#
#        with self.assertRaises(Exception):
#            sleep(time)
#        logging.info("\tPassed")

    def test_get_idp_predefined_service_hash(self):
        logging.info(
            ".........Test : get_idp_predefined_service_hash ............")
        ###################################################################
        logging.info(
            "Test case 1: Run with invalid predefserv file")
        param = {'path': 'test_file'}
        test = get_idp_predefined_service_hash(**param)
        self.assertEqual(test, None, "Return should be None")
        logging.info("\tPassed")

        ###################################################################
        logging.info(
            "Test case 2: Run with valid predefserv file")
        param = {'path': os.path.join(os.getcwd(),
                                      'Testsuites/IDP/support/predefserv')}
        data = '''
: (any
    :type (any)
)
: (TCP-ANY
    :type (tcp)
    :port (0-65535)
)
: (WAIS
    :type (tcp)
    :port (210)
)
: (netbios-ssn-tcp
    :type (tcp)
    :port (139)
)
: (netbios-ssn-udp
    :type (udp)
    :port (139)
)
: (netbios-ssn
    :type (group)
    :members (
        : (netbios-ssn-tcp)
        : (netbios-ssn-udp)
    )
)
: (rstatd
    : (rpc)
    :program (100001-100001)
)
: (sunrpc-tcp
    :type (tcp)
    :port (111)
)
: (sunrpc-udp
    : (udp)
    :port (111)
)
: (sunrpc
    :type (group)
    :members (
        : (sunrpc-tcp)
        : (sunrpc-udp)
    )
)
: (smtp
    :type (tcp)
    :port (25)
)
: (OSPF
    :type (ip)
    :protocol (89)
)
: (PIM
    :type (ip)
    :protocol (103)
)
: (dhcpv6-server-tcp
    :type (tcp)
    :port (547)
)
: (ICMP-INFO
    :type (icmp)
    :icmp_type (15)
    :icmp_code (0)
)
: (FINGER
    :type (tcp)
    :port (79)
)
: (finger-udp
    :type (udp)
    :port (79)
)
: (FINGER-ALL
    :type (group)
    :members (
        : (FINGER)
        : (finger-udp)
    )
)
: (netbios-ns-udp
    :type (udp)
    :port (137)
)
: (sched
    :type (rpc)
    :program (100019-100019)
)
: (bootp-client-tcp
    :type (tcp)
    :port (68)
)
: (bootp-client-udp
    :type (udp)
    :port (68)
)
: (bootp-client
    :type (group)
    :members (
        : (bootp-client-tcp)
        : (bootp-client-udp)
    )
)
: (socks-tcp
    :type (tcp)
    :port (1080)
)
: (HTTP
    :type (tcp)
    :port (80)
)
: (dhcpv6-client-udp
    :type (udp)
    :port (546)
)
: (VRRP
    :type (ip)
    :protocol (112)
)
: (TALK
    :type (udp)
    :port (517-518)
)
: (ICMP-ALL
    :type (group)
    :members (
        : (ICMP-INFO)
        : (info-reply)
    )
)
: (PING
    :type (icmp)
    :icmp_type (8)
    :icmp_code (0)
)
: (IPv6-Options
    :type (ip)
    :protocol (60)
)
: (addrmask-request
    :type (icmp)
    :icmp_type (17)
    :icmp_code (0)
)
: ("VDO Live"
    :type (tcp)
    :port (7000-7010)
)
: (ypupdated
    :type (rpc)
    :program (100028-100028)
)
: ("H.323_1"
    :type (tcp)
    :port (1720)
)
: ("H.323_2"
    :type (tcp)
    :port (1503)
)
: ("H.323_3"
    :type (tcp)
    :port (389)
)
: ("H.323_4"
    :type (tcp)
    :port (522)
)
: ("H.323_5"
    :type (tcp)
    :port (1731)
)
: ("H.323_6"
    :type (udp)
    :port (1719)
)
: ("H.323"
    :type (group)
    :members (
        : ("H.323_1")
        : ("H.323_2")
        : ("H.323_3")
        : ("H.323_4")
        : ("H.323_5")
        : ("H.323_6")
    )
)
: (echo-request
    :type (icmp)
    :icmp_type (8)
    :icmp_code (0)
)
: (PING-ALL
    :type (group)
    :members (
        : (echo-request)
        : (echo-reply)
    )
)
: (IKE
    :type (udp)
    :port (500)
)
: (mountd
    :type (rpc)
    :program (100005-100005)
)
: (IPv6-NoNext
    :type (ip)
    :protocol (59)
)
: ("Real Media_1"
    :type (tcp)
    :port (7070)
)
: ("Real Media_2"
    :type (tcp)
    :port (554)
)
: ("Real Media"
    :type (group)
    :members (
        : ("Real Media_1")
        : ("Real Media_2")
    )
)
: (EGP
    :type (ip)
    :protocol (8)
)
: (netstat
    :type (tcp)
    :port (15)
)
: (discard-udp
    :type (udp)
    :port (9)
)
: (IPIP
    :type (ip)
    :protocol (4)
)
: (snmp-tcp
    :type (tcp)
    :port (161)
)
: (snmp-udp
    :type (udp)
    :port (161)
)
: (snmptrap-udp
    :type (udp)
    :port (162)
)
: (snmptrap-tcp
    :type (tcp)
    :port (162)
)
: (SNMP
    :type (group)
    :members (
        : (snmp-tcp)
        : (snmp-udp)
        : (snmptrap-udp)
        : (snmptrap-tcp)
    )
)
: (SWIPE
    :type (ip)
    :protocol (53)
)
: (echo-udp
    :type (udp)
    :port (7)
)
: (EIGRP
    :type (ip)
    :protocol (88)
)
: (DGP
    :type (ip)
    :protocol (86)
)
: (netbios-ns-tcp
    :type (tcp)
    :port (137)
)
: (GOPHER
    :type (tcp)
    :port (70)
)
: (gopher-udp
    :type (udp)
    :port (70)
)
: (GOPHER-ALL
    :type (group)
    :members (
        : (GOPHER)
        : (gopher-udp)
    )
)
: ("IDP Management Server"
    :type (tcp)
    :port (7203)
)
: (ypserv
    :type (rpc)
    :program (100004-100004)
)
: (socks-udp
    :type (udp)
    :port (1080)
)
: (socks
    :type (group)
    :members (
        : (socks-tcp)
        : (socks-udp)
    )
)
: (NFS-SUNRPC
    :type (rpc)
    :program (100003-100003)
)
: (ldap-tcp
    :type (tcp)
    :port (389)
)
: (IPX-in-IP
    :type (ip)
    :protocol (111)
)
: (GGP
    :type (ip)
    :protocol (3)
)
: (bootp-server-tcp
    :type (tcp)
    :port (67)
)
: (x11
    :type (tcp)
    :port (6000)
)
: (NFS_1
    :type (udp)
    :port (111)
)
: (NFS_2
    :type (tcp)
    :port (111)
)
: (NFS_3
    :type (udp)
    :port (2049)
)
: (NFS_4
    :type (tcp)
    :port (2049)
)
: (NFS
    :type (group)
    :members (
        : (NFS_1)
        : (NFS_2)
        : (NFS_3)
        : (NFS_4)
    )
)
: (NFS-ALL
    :type (group)
    :members (
        : (NFS)
        : (NFS-SUNRPC)
    )
)
: (keyserv
    :type (rpc)
    :program (100029-100029)
)
: (ICMP-TIMESTAMP
    :type (icmp)
    :icmp_type (13)
    :icmp_code (0)
)
: (LDAP
    :type (tcp)
    :port (389)
)
: (nameserver-udp
    :type (udp)
    :port (42)
)
: (yppasswdd
    :type (rpc)
    :program (100009-100009)
)
: (ESP
    :type (ip)
    :protocol (50)
)
: (RLOGIN
    :type (tcp)
    :port (513)
)
: (NTP_1
    :type (udp)
    :port (123)
)
: (NTP_2
    :type (tcp)
    :port (123)
)
: (NTP
    :type (group)
    :members (
        : (NTP_1)
        : (NTP_2)
    )
)
: (ntp-udp
    :type (udp)
    :port (123)
)
: (NTP-ALL
    :type (group)
    :members (
        : (NTP)
        : (ntp-udp)
    )
)
: (FTP
    :type (tcp)
    :port (21)
)
: (chargen-tcp
    :type (tcp)
    :port (19)
)
: (BGP
    :type (tcp)
    :port (179)
)
: (PPTP_1
    :type (tcp)
    :port (1723)
)
: (PPTP_2
    :type (ip)
    :protocol (47)
)
: (PPTP
    :type (group)
    :members (
        : (PPTP_1)
        : (PPTP_2)
    )
)
: (MAIL
    :type (tcp)
    :port (25)
)
: (snmp-idp
    :type (group)
    :members (
        : (snmp-tcp)
        : (snmp-udp)
    )
)
: (AOL
    :type (tcp)
    :port (5190-5194)
)
: (ldap-udp
    :type (udp)
    :port (389)
)
: (LDAP-ALL
    :type (group)
    :members (
        : (ldap-tcp)
        : (ldap-udp)
    )
)
: (IPv6-ICMP
    :type (ip)
    :protocol (58)
)
: (shell
    :type (tcp)
    :port (514)
)
: (rsync
    :type (tcp)
    :port (873)
)
: (AH
    :type (ip)
    :protocol (51)
)
: ("NS Global_1"
    :type (tcp)
    :port (15397)
)
: ("NS Global_2"
    :type (udp)
    :port (15397)
)
: ("NS Global"
    :type (group)
    :members (
        : ("NS Global_1")
        : ("NS Global_2")
    )
)
: (TRACEROUTE_1
    :type (icmp)
    :icmp_type (8)
    :icmp_code (0)
)
: (TRACEROUTE_2
    :type (udp)
    :port (33400)
)
: (TRACEROUTE
    :type (group)
    :members (
        : (TRACEROUTE_1)
        : (TRACEROUTE_2)
    )
)
: (nntp-udp
    :type (udp)
    :port (119)
)
: (chargen-udp
    :type (udp)
    :port (19)
)
: (IDPR
    :type (ip)
    :protocol (35)
)
: (SSH
    :type (tcp)
    :port (22)
)
: (hostname-tcp
    :type (tcp)
    :port (101)
)
: (hostname-udp
    :type (udp)
    :port (101)
)
: (hostname
    :type (group)
    :members (
        : (hostname-tcp)
        : (hostname-udp)
    )
)
: (FTP-Put
    :type (tcp)
    :port (21)
)
: (statmon
    :type (rpc)
    :program (100023-100023)
)
: (imap-ssl
    :type (tcp)
    :port (993)
)
: (echo-tcp
    :type (tcp)
    :port (7)
)
: (discard-tcp
    :type (tcp)
    :port (9)
)
: (UUCP
    :type (udp)
    :port (540)
)
: (daytime-tcp
    :type (tcp)
    :port (13)
)
: (daytime-udp
    :type (udp)
    :port (13)
)
: (daytime
    :type (group)
    :members (
        : (daytime-tcp)
        : (daytime-udp)
    )
)
: (dns-udp
    :type (udp)
    :port (53)
)
: (WINFRAME
    :type (tcp)
    :port (1494)
)
: (rtsp-udp
    :type (udp)
    :port (554)
)
: (RTSP-ALL
    :type (group)
    :members (
        : (RTSP)
        : (rtsp-udp)
    )
)
: (OSPF-IGP
    :type (ip)
    :protocol (89)
)
: (UDP-ANY
    :type (udp)
    :port (0-65535)
)
: (FTP-Get
    :type (tcp)
    :port (21)
)
: (http-alt
    :type (tcp)
    :port (8008)
)
: (identd-tcp
    :type (tcp)
    :port (113)
)
: (identd-udp
    :type (udp)
    :port (113)
)
: (dhcpv6-server-udp
    :type (udp)
    :port (547)
)
: (linuxconf
    :type (tcp)
    :port (98)
)
: (exec
    :type (tcp)
    :port (512)
)
: (HTTPS
    :type (tcp)
    :port (443)
)
: (NNTP
    :type (tcp)
    :port (119)
)
: (SYSLOG_1
    :type (udp)
    :port (514)
)
: (SYSLOG_2
    :type (udp)
    :port (514)
)
: (SYSLOG
    :type (group)
    :members (
        : (SYSLOG_1)
        : (SYSLOG_2)
    )
)
: (netbios-dgm-tcp
    :type (tcp)
    :port (138)
)
: (NNTP-ALL
    :type (group)
    :members (
        : (NNTP)
        : (nntp-udp)
    )
)
: (x25
    :type (rpc)
    :program (100114-100114)
)
: (login
    :type (tcp)
    :port (513)
)
: (dns-tcp
    :type (tcp)
    :port (53)
)
: (SKIP
    :type (ip)
    :protocol (57)
)
: (TALK-IDP
    :type (udp)
    :port (517)
)
: (walld
    :type (rpc)
    :program (100008-100008)
)
: (dhcpv6-client-tcp
    :type (tcp)
    :port (546)
)
: (portmapper
    :type (rpc)
    :program (100000-100000)
)
: ("Internet Locator Service_1"
    :type (tcp)
    :port (389)
)
: ("Internet Locator Service_2"
    :type (tcp)
    :port (522)
)
: ("Internet Locator Service_3"
    :type (tcp)
    :port (636)
)
: ("Internet Locator Service"
    :type (group)
    :members (
        : ("Internet Locator Service_1")
        : ("Internet Locator Service_2")
        : ("Internet Locator Service_3")
    )
)
: (nisd
    :type (rpc)
    :program (100300-100300)
)
: (bootp-server-udp
    :type (udp)
    :port (67)
)
: (bootp-server
    :type (group)
    :members (
        : (bootp-server-tcp)
        : (bootp-server-udp)
    )
)
: (IGP
    :type (ip)
    :protocol (9)
)
: (xfs
    :type (tcp)
    :port (7100)
)
: (rusersd
    :type (rpc)
    :program (100002-100002)
)
: (ntalk
    :type (udp)
    :port (518)
)
: (X-WINDOWS
    :type (tcp)
    :port (6000-6063)
)
: (nameserver-tcp
    :type (tcp)
    :port (42)
)
: (nispasswd
    :type (rpc)
    :program (100303-100303)
)
: (IMAP
    :type (tcp)
    :port (143)
)
: (bugtraqd
    :type (rpc)
    :program (100071-100071)
)
: (ypxfrd
    :type (rpc)
    :program (100069-100069)
)
: (any-ip
    :type (ip)
    :protocol (0)
)
: (TRACEROUTE-IDP
    :type (udp)
    :port (33434)
)
: (L2TP-IDP
    :type (ip)
    :protocol (115)
)
: (netbios-ns
    :type (group)
    :members (
        : (netbios-ns-tcp)
        : (netbios-ns-udp)
    )
)
: (netbios-dgm-udp
    :type (udp)
    :port (138)
)
: (netbios-dgm
    :type (group)
    :members (
        : (netbios-dgm-tcp)
        : (netbios-dgm-udp)
    )
)
: (DNS
    :type (group)
    :members (
        : (dns-tcp)
        : (dns-udp)
    )
)
: (status
    :type (rpc)
    :program (100024-100024)
)
: (sync
    :type (rpc)
    :program (100104-100104)
)
: (dhcpv6-server
    :type (group)
    :members (
        : (dhcpv6-server-tcp)
        : (dhcpv6-server-udp)
    )
)
: (rquotad
    :type (rpc)
    :program (100011-100011)
)
: (icmp-addrmask
    :type (group)
    :members (
        : (addrmask-request)
        : (addrmask-reply)
    )
)
: (PC-Anywhere_1
    :type (udp)
    :port (5632)
)
: (PC-Anywhere_2
    :type (udp)
    :port (22)
)
: (PC-Anywhere_3
    :type (tcp)
    :port (5631)
)
: (PC-Anywhere
    :type (group)
    :members (
        : (PC-Anywhere_1)
        : (PC-Anywhere_2)
        : (PC-Anywhere_3)
    )
)
: (nameserver
    :type (group)
    :members (
        : (nameserver-tcp)
        : (nameserver-udp)
    )
)
: (ETHER-IP
    :type (ip)
    :protocol (97)
)
: (NetMeeting_1
    :type (tcp)
    :port (1720)
)
: (NetMeeting_2
    :type (tcp)
    :port (1503)
)
: (NetMeeting_3
    :type (tcp)
    :port (389)
)
: (NetMeeting_4
    :type (tcp)
    :port (522)
)
: (NetMeeting_5
    :type (tcp)
    :port (1731)
)
: (NetMeeting_6
    :type (udp)
    :port (1719)
)
: (NetMeeting
    :type (group)
    :members (
        : (NetMeeting_1)
        : (NetMeeting_2)
        : (NetMeeting_3)
        : (NetMeeting_4)
        : (NetMeeting_5)
        : (NetMeeting_6)
    )
)
: (dhcpv6-client
    :type (group)
    :members (
        : (dhcpv6-client-tcp)
        : (dhcpv6-client-udp)
    )
)
: (POP3
    :type (tcp)
    :port (110)
)
: (IPv6
    :type (ip)
    :protocol (41)
)
: (IRC
    :type (tcp)
    :port (6660-6669)
)
: (L2TP
    :type (tcp)
    :port (1701)
)
: (IPv6-Fragment
    :type (ip)
    :protocol (44)
)
: (IPv6-Route
    :type (ip)
    :protocol (43)
)
: (snmptrap
    :type (group)
    :members (
        : (snmptrap-udp)
        : (snmptrap-tcp)
    )
)
: (GRE
    :type (ip)
    :protocol (47)
)
: (RIP
    :type (udp)
    :port (520)
)
: (ICMP-TIMESTAMP-ALL
    :type (group)
    :members (
        : (ICMP-TIMESTAMP)
        : (timestamp-reply)
    )
)
: ("NS Global PRO_1"
    :type (tcp)
    :port (15397)
)
: ("NS Global PRO_2"
    :type (udp)
    :port (15397)
)
: ("NS Global PRO_3"
    :type (tcp)
    :port (15400-15403)
)
: ("NS Global PRO"
    :type (group)
    :members (
        : ("NS Global PRO_1")
        : ("NS Global PRO_2")
        : ("NS Global PRO_3")
    )
)
: (IGMP
    :type (ip)
    :protocol (2)
)
: (DHCP-Relay
    :type (udp)
    :port (67)
)
: (TELNET
    :type (tcp)
    :port (23)
)
: (bootparam
    :type (rpc)
    :program (100026-100026)
)
: (TFTP
    :type (udp)
    :port (69)
)
: (pcnfsd
    :type (rpc)
    :program (150001-150001)
)
: (ypbind
    :type (rpc)
    :program (100007-100007)
)
: ("ICMP Port Unreachable"
    :type (icmp)
    :icmp_type (3)
    :icmp_code (3)
)
: (RADIUS
    :type (udp)
    :port (1812-1813)
)
: ("ICMP Redirect TOS & Net"
    :type (icmp)
    :icmp_type (5)
    :icmp_code (2)
)
: (MS-RPC-EPM_1
    :type (udp)
    :port (135)
)
: (MS-RPC-EPM_2
    :type (tcp)
    :port (135)
)
: (MS-RPC-EPM
    :type (group)
    :members (
        : (MS-RPC-EPM_1)
        : (MS-RPC-EPM_2)
    )
)
: (WHOIS
    :type (tcp)
    :port (43)
)
: (info-reply
    :type (icmp)
    :icmp_type (16)
    :icmp_code (0)
)
: ("ICMP Fragment Needed"
    :type (icmp)
    :icmp_type (3)
    :icmp_code (4)
)
: (echo-reply
    :type (icmp)
    :icmp_type (16)
    :icmp_code (0)
)
: (MS-AD-BR_1
    :type (rpc)
    :program (135)
)
: (MS-AD-BR_2
    :type (rpc)
    :program (135)
)
: (MS-AD-BR
    :type (group)
    :members (
        : (MS-AD-BR_1)
        : (MS-AD-BR_2)
    )
)
: (MS-AD-DRSUAPI
    :type (rpc)
    :program (135)
)
: (MS-AD-DSROLE
    :type (rpc)
    :program (135)
)
: (MS-AD-DSSETUP
    :type (rpc)
    :program (135)
)
: (MS-AD
    :type (group)
    :members (
        : (MS-AD-BR)
        : (MS-AD-DRSUAPI)
        : (MS-AD-DSROLE)
        : (MS-AD-DSSETUP)
    )
)
: (SUN-RPC_1
    :type (udp)
    :port (111)
)
: (SUN-RPC_2
    :type (tcp)
    :port (111)
)
: (SUN-RPC_3
    :type (udp)
    :port (2049)
)
: (SUN-RPC_4
    :type (tcp)
    :port (2049)
)
: (SUN-RPC
    :type (group)
    :members (
        : (SUN-RPC_1)
        : (SUN-RPC_2)
        : (SUN-RPC_3)
        : (SUN-RPC_4)
    )
)
: (MS-SQL
    :type (tcp)
    :port (1433)
)
: (MS-EXCHANGE-DATABASE
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-DIRECTORY_1
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-DIRECTORY_2
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-DIRECTORY_3
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-DIRECTORY
    :type (group)
    :members (
        : (MS-EXCHANGE-DIRECTORY_1)
        : (MS-EXCHANGE-DIRECTORY_2)
        : (MS-EXCHANGE-DIRECTORY_3)
    )
)
: (MS-EXCHANGE-INFO-STORE_1
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-INFO-STORE_2
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-INFO-STORE_3
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-INFO-STORE_4
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-INFO-STORE
    :type (group)
    :members (
        : (MS-EXCHANGE-INFO-STORE_1)
        : (MS-EXCHANGE-INFO-STORE_2)
        : (MS-EXCHANGE-INFO-STORE_3)
        : (MS-EXCHANGE-INFO-STORE_4)
    )
)
: (MS-EXCHANGE-MTA_1
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-MTA_2
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-MTA
    :type (group)
    :members (
        : (MS-EXCHANGE-MTA_1)
        : (MS-EXCHANGE-MTA_2)
    )
)
: (MS-EXCHANGE-STORE_1
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-STORE_2
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-STORE_3
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-STORE_4
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-STORE
    :type (group)
    :members (
        : (MS-EXCHANGE-STORE_1)
        : (MS-EXCHANGE-STORE_2)
        : (MS-EXCHANGE-STORE_3)
        : (MS-EXCHANGE-STORE_4)
    )
)
: (MS-EXCHANGE-SYSATD_1
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-SYSATD_2
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-SYSATD_3
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-SYSATD_4
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-SYSATD_5
    :type (rpc)
    :program (135)
)
: (MS-EXCHANGE-SYSATD
    :type (group)
    :members (
        : (MS-EXCHANGE-SYSATD_1)
        : (MS-EXCHANGE-SYSATD_2)
        : (MS-EXCHANGE-SYSATD_3)
        : (MS-EXCHANGE-SYSATD_4)
        : (MS-EXCHANGE-SYSATD_5)
    )
)
: (MS-EXCHANGE
    :type (group)
    :members (
        : (MS-EXCHANGE-DATABASE)
        : (MS-EXCHANGE-DIRECTORY)
        : (MS-EXCHANGE-INFO-STORE)
        : (MS-EXCHANGE-MTA)
        : (MS-EXCHANGE-STORE)
        : (MS-EXCHANGE-SYSATD)
    )
)
: (SUN-RPC-YPBIND
    :type (rpc)
    :program (100007-100007)
)
: ("ICMP Redirect"
    :type (icmp)
    :icmp_type (5)
    :icmp_code (0)
)
: ("ICMP Parameter Problem"
    :type (icmp)
    :icmp_type (12)
    :icmp_code (0)
)
: (SUN-RPC-SPRAYD
    :type (rpc)
    :program (100012-100012)
)
: (SIP_1
    :type (udp)
    :port (5060)
)
: (SIP_2
    :type (tcp)
    :port (5060)
)
: (SIP
    :type (group)
    :members (
        : (SIP_1)
        : (SIP_2)
    )
)
: ("ICMP Host Unreachable"
    :type (icmp)
    :icmp_type (3)
    :icmp_code (1)
)
: (SUN-RPC-WALLD
    :type (rpc)
    :program (100008-100008)
)
: (SUN-RPC-PORTMAPPER_1
    :type (udp)
    :port (111)
)
: (SUN-RPC-PORTMAPPER_2
    :type (tcp)
    :port (111)
)
: (SUN-RPC-PORTMAPPER
    :type (group)
    :members (
        : (SUN-RPC-PORTMAPPER_1)
        : (SUN-RPC-PORTMAPPER_2)
    )
)
: ("ICMP Protocol Unreach"
    :type (icmp)
    :icmp_type (3)
    :icmp_code (2)
)
: ("ICMP Source Quench"
    :type (icmp)
    :icmp_type (4)
    :icmp_code (0)
)
: (timestamp-reply
    :type (icmp)
    :icmp_type (14)
    :icmp_code (0)
)
: (SUN-RPC-SADMIND
    :type (rpc)
    :program (100232-100232)
)
: (SUN-RPC-MOUNTD
    :type (rpc)
    :program (100005-100005)
)
: (LPR
    :type (tcp)
    :port (515)
)
: (SCCP
    :type (tcp)
    :port (2000)
)
: ("ICMP Dest Unreachable"
    :type (icmp)
    :icmp_type (3)
    :icmp_code (0)
)
: (SMTP
    :type (tcp)
    :port (25)
)
: ("ICMP Address Mask"
    :type (icmp)
    :icmp_type (17)
    :icmp_code (0)
)
: (GTP_1
    :type (udp)
    :port (3386)
)
: (GTP_2
    :type (udp)
    :port (2123)
)
: (GTP_3
    :type (udp)
    :port (2152)
)
: (GTP_4
    :type (tcp)
    :port (3386)
)
: (GTP_5
    :type (tcp)
    :port (2123)
)
: (GTP_6
    :type (tcp)
    :port (2152)
)
: (GTP
    :type (group)
    :members (
        : (GTP_1)
        : (GTP_2)
        : (GTP_3)
        : (GTP_4)
        : (GTP_5)
        : (GTP_6)
    )
)
: (SUN-RPC-RQUOTAD
    :type (rpc)
    :program (100011-100011)
)
: (SUN-RPC-RSTATD
    :type (rpc)
    :program (100001-100001)
)
: (DISCARD
    :type (group)
    :members (
        : (discard-tcp)
        : (discard-udp)
    )
)
: (SUN-RPC-NLOCKMGR
    :type (rpc)
    :program (100021-100021)
)
: (GNUTELLA_1
    :type (udp)
    :port (6346-6347)
)
: (GNUTELLA_2
    :type (tcp)
    :port (5346-5347)
)
: (GNUTELLA
    :type (group)
    :members (
        : (GNUTELLA_1)
        : (GNUTELLA_2)
    )
)
: (REXEC
    :type (tcp)
    :port (512)
)
: (RSH
    :type (tcp)
    :port (514)
)
: (RTSP
    :type (tcp)
    :port (554)
)
: ("SQL*Net V2"
    :type (tcp)
    :port (1521)
)
: (IDENT
    :type (group)
    :members (
        : (identd-tcp)
        : (identd-udp)
    )
)
: (MGCP-UA
    :type (udp)
    :port (2427)
)
: (MGCP-CA
    :type (udp)
    :port (2727)
)
: (VOIP
    :type (group)
    :members (
        : ("H.323")
        : (SIP)
        : (MGCP-CA)
        : (MGCP-UA)
    )
)
: (NBNAME
    :type (udp)
    :port (137)
)
: (addrmask-reply
    :type (icmp)
    :icmp_type (18)
    :icmp_code (0)
)
: (HTTP-EXT_1
    :type (tcp)
    :port (7001)
)
: (HTTP-EXT_2
    :type (tcp)
    :port (8000-8001)
)
: (HTTP-EXT_3
    :type (tcp)
    :port (8080-8081)
)
: (HTTP-EXT_4
    :type (tcp)
    :port (8100)
)
: (HTTP-EXT_5
    :type (tcp)
    :port (8200)
)
: (HTTP-EXT_6
    :type (tcp)
    :port (9080)
)
: (HTTP-EXT
    :type (group)
    :members (
        : (HTTP-EXT_1)
        : (HTTP-EXT_2)
        : (HTTP-EXT_3)
        : (HTTP-EXT_4)
        : (HTTP-EXT_5)
        : (HTTP-EXT_6)
    )
)
: (SMB_1
    :type (tcp)
    :port (139)
)
: (SMB_2
    :type (tcp)
    :port (445)
)
: (SMB
    :type (group)
    :members (
        : (SMB_1)
        : (SMB_2)
    )
)
: (SUN-RPC-STATUS
    :type (rpc)
    :program (100024-100024)
)
: ("ICMP Redirect Host"
    :type (icmp)
    :icmp_type (5)
    :icmp_code (1)
)
: ("ICMP Source Route Fail"
    :type (icmp)
    :icmp_type (3)
    :icmp_code (5)
)
: (MSN
    :type (tcp)
    :port (1863)
)
: (NSM_1
    :type (udp)
    :port (69)
)
: (NSM_2
    :type (tcp)
    :port (7204)
)
: (NSM_3
    :type (tcp)
    :port (7800)
)
: (NSM_4
    :type (tcp)
    :port (11122)
)
: (NSM_5
    :type (tcp)
    :port (15400)
)
: (NSM
    :type (group)
    :members (
        : (NSM_1)
        : (NSM_2)
        : (NSM_3)
        : (NSM_4)
        : (NSM_5)
    )
)
: (SUN-RPC-NFS_1
    :type (rpc)
    :program (100003-100003)
)
: (SUN-RPC-NFS_2
    :type (rpc)
    :program (100227-100227)
)
: (SUN-RPC-NFS
    :type (group)
    :members (
        : (SUN-RPC-NFS_1)
        : (SUN-RPC-NFS_2)
    )
)
: (NBDS
    :type (tcp)
    :port (138)
)
: (YMSG
    :type (tcp)
    :port (5050)
)
: ("ICMP Fragment Reassembly"
    :type (icmp)
    :icmp_type (11)
    :icmp_code (1)
)
: ("SQL*Net V1"
    :type (tcp)
    :port (1525)
)
: (CHARGEN
    :type (group)
    :members (
        : (chargen-tcp)
        : (chargen-udp)
    )
)
: (VNC_1
    :type (tcp)
    :port (5800)
)
: (VNC_2
    :type (tcp)
    :port (5900)
)
: (VNC
    :type (group)
    :members (
        : (VNC_1)
        : (VNC_2)
    )
)
: (ECHO
    :type (group)
    :members (
        : (echo-tcp)
        : (echo-udp)
    )
)
: (MS-IIS-COM_1
    :type (rpc)
    :program (135)
)
: (MS-IIS-COM_2
    :type (rpc)
    :program (135)
)
: (MS-IIS-COM
    :type (group)
    :members (
        : (MS-IIS-COM_1)
        : (MS-IIS-COM_2)
    )
)
: (MS-IIS-IMAP4
    :type (rpc)
    :program (135)
)
: (MS-IIS-INETINFO
    :type (rpc)
    :program (135)
)
: (MS-IIS-NNTP
    :type (rpc)
    :program (135)
)
: (MS-IIS-POP3
    :type (rpc)
    :program (135)
)
: (MS-IIS-SMTP
    :type (rpc)
    :program (135)
)
: (MS-IIS
    :type (group)
    :members (
        : (MS-IIS-COM)
        : (MS-IIS-IMAP4)
        : (MS-IIS-INETINFO)
        : (MS-IIS-NNTP)
        : (MS-IIS-POP3)
        : (MS-IIS-SMTP)
    )
)
: (ICMP-ANY
    :type (icmp)
    :icmp_type (any)
    :icmp_code (any)
)
: ("ICMP Redirect TOS & Host"
    :type (icmp)
    :icmp_type (5)
    :icmp_code (3)
)
: (SUN-RPC-RUSERD
    :type (rpc)
    :program (100002-100002)
)
: ("SQL Monitor"
    :type (udp)
    :port (1434)
)
: ("ICMP Time Exceeded"
    :type (icmp)
    :icmp_type (11)
    :icmp_code (0)
)
: (IKE-NAT
    :type (udp)
    :port (500)
)
: (MGCP
    :type (group)
    :members (
        : (MGCP-CA)
        : (MGCP-UA)
    )
)
        '''
        with patch('builtins.open', mock.mock_open(read_data=data)):
            self.assertIsInstance(get_idp_predefined_service_hash(**param),
                                  dict, "Return should be a dict")
        logging.info("\tPassed")

        ###################################################################
        logging.info(
            "Test case 3: With invalid predefserv file")
        param = {
            'path': os.path.join(os.getcwd(),
                                 'Testsuites/IDP/support/predefserv_fail')}
        data = '''
: (netbios-ssn
    :type (group)
    :members1 (
        : (netbios-ssn-tcp)
        : (netbios-ssn-udp)
    )
)
        '''
        with patch('builtins.open', mock.mock_open(read_data=data)):
            self.assertEqual(get_idp_predefined_service_hash(**param),
                             {'netbios-ssn,type': 'group',
                              'name,netbios-ssn': 'netbios-ssn'},
                             "Return should be None")
        logging.info("\tPassed")
        ###################################################################
        logging.info(
            "Test case 4: With directory of predefserv file is in sys.path")
        param = {
            'path': os.path.join(os.getcwd(),
                                 'Testsuites/IDP/support/predefserv')}
        with patch('os.path.isfile', return_value=True):
            self.assertEqual(get_idp_predefined_service_hash(**param),
                             None, "Return should be None")
        logging.info("\tPassed")

    def test_compare_list_of_dict(self):
        logging.info(".........Test : compare_list_of_dict ............")
        ###################################################################
        logging.info("Test case 1: Comparing lists of dictionaries passed")
        d1 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 123},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        d2 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 123},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        result = compare_list_of_dict(org_lod=d1, usr_lod=d2)

        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 2: Comparing lists of dictionaries failed")
        d1 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 123},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        d2 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 1231},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        result = compare_list_of_dict(org_lod=d1, usr_lod=d2)

        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 3: Comparing lists of dictionaries passed"
                     " and Return list")
        d1 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 123},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        d2 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 123},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        result = compare_list_of_dict(org_lod=d1, usr_lod=d2, return_list=True)

        self.assertListEqual(result, [1, 1, 1],
                             "Result is not equal as expectation")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 4: Comparing lists of dictionaries failed "
                     "and Return list")
        d1 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 123},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        d2 = [{'list': [1, 2, 3], 'str': 'abc', 'int': 1231},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 456},
              {'list': [1, 2, 3], 'str': 'abc', 'int': 789}]
        result = compare_list_of_dict(org_lod=d1, usr_lod=d2, return_list=True)
        self.assertListEqual(result, [0, 1, 1],
                             "Result is not equal as expectation")
        logging.info("\tPassed")

    def test_compare_dict(self):
        logging.info(".........Test : compare_dict ............")
        ###################################################################
        logging.info("Test case 1: Comparing dictionary passed, " +
                     "negate = False")
        d1 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'str': 'abc', 'int': 123}
        d2 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'str': 'abc', 'int': 123}
        result = compare_dict(org_dict=d1, usr_dict=d2)

        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 2: Comparing dictionary passed, " +
                     "negate = True")
        d1 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'str': 'abc', 'int': 123}
        d2 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'str': 'abc', 'int': 123}
        result = compare_dict(org_dict=d1, usr_dict=d2, negate=True)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 3: Comparing dictionary failed, " +
                     "negate = False")
        d1 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'int': 1234}
        d2 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'str': 'abc', 'int': 123}
        result = compare_dict(org_dict=d1, usr_dict=d2)
        self.assertFalse(result, "Result should be False")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 4: Comparing dictionary failed, " +
                     "negate = True")
        d1 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'int': 1234}
        d2 = {'list': [1, 2, 3], 'dict': {'a': 1}, 'str': 'abc', 'int': 123}
        result = compare_dict(org_dict=d1, usr_dict=d2, negate=True)
        self.assertTrue(result, "Result should be True")
        logging.info("\tPassed")

    def test_compare_list_of_list(self):
        logging.info(".........Test : compare_list_of_list ............")
        ###################################################################
        logging.info("Test case 1: Return True")
        li = {'org_lol': 'this is test 1',
              'usr_lol': ['this Is TEST 1']}
        expected = True
        test = compare_list_of_list(**li)
        try:
            self.assertEqual(test, expected, "Test Fail")
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tPassed")
        except Exception:
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tFailed")

        ###################################################################
        logging.info("Test case 2: return False")
        li = {'org_lol': 'this is test 1',
              'usr_lol': ['test 2']}
        expected = False
        test = compare_list_of_list(**li)
        try:
            self.assertEqual(test, expected, "Test Fail")
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tPassed")
        except Exception:
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tFailed")

        ###################################################################
        logging.info("Test case 3: Return list True")
        li = {'org_lol': 'this is test 1',
              'usr_lol': ['this Is TEST 1'],
              'return_list': True}
        expected = [1]
        test = compare_list_of_list(**li)
        try:
            self.assertListEqual(test, expected, "Test Fail")
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tPassed")
        except Exception:
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tFailed")

        ###################################################################
        logging.info("Test case 4: Return list False")
        li = {'org_lol': 'this is test 1',
              'usr_lol': ['this Is TEST 2'],
              'return_list': True}
        expected = [0]
        test = compare_list_of_list(**li)
        try:
            self.assertListEqual(test, expected, "Test Fail")
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tPassed")
        except Exception:
            logging.info("\tExpected result: %s" % str(expected))
            logging.info("\tActual result: %s" % str(test))
            logging.info("\tFailed")

    def test_compare_list(self):
        logging.info(".........Test : compare_list ............")
        ###################################################################
        logging.info("Test case 1: Return Fail without negate")
        li = {'org_list': 'this is test 1',
              'usr_list': ['this Is TEST 1', ['test 2']]}
        test = compare_list(**li)
        self.assertFalse(test, "Result should be False")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 2: return True with negate")
        li = {'org_list': 'this is test 1',
              'usr_list': ['this Is TEST 1', ['test 2']],
              'negate': True}
        test = compare_list(**li)
        self.assertTrue(test, "Result should be True")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 3: return True without negate")
        li = {'org_list': 'this is test 1',
              'usr_list': ['this Is TEST 1']}
        test = compare_list(**li)

        self.assertTrue(test, "Result should be True")
        logging.info("\tPassed")

        ###################################################################
        logging.info("Test case 4: return False with negate")
        li = {'org_list': 'this is test 1',
              'usr_list': ['this Is TEST 1'],
              'negate': 'True'}
        test = compare_list(**li)
        self.assertFalse(test, "Result should be False")
        logging.info("\tPassed")

    def test_file_presence_search(self):
        logging.info(".........Test : file_presence_search ............")

        sample_list = []
        sample_string = ""
        try:
            file_presence_search(sample_list)
        except Exception as err:
            self.assertEqual(err.args[0], "No Matching File Present on the System")

        try:
            file_presence_search(sample_string)
        except Exception as err:
            self.assertEqual(err.args[0], "Argument file_list must be of type 'list'")

        from jnpr.toby.init.init import init
        init(initialize_t=True)

        import lxml
        valid_file = lxml.__path__[0] + "/__init__.py"
        sample_list = [ 
            "/var/tmp/not-present-file.txt",
            valid_file
        ]
        self.assertEqual(file_presence_search(sample_list), valid_file)

        sample_list = [
            "/var/tmp/AAA",
            "/var/tmp/BBB",
        ]
        try:
            file_presence_search(sample_list)
        except Exception as err:
            self.assertEqual(err.args[0], "No Matching File Present on the System")

    data_json = """ [ {
    "_index": "packets-2019-04-30",
    "_type": "pcap_file",
    "_score": null,
    "_source": {
      "layers": {
        "frame": {
          "frame.encap_type": "1",
          "frame.time": "Apr 24, 2019 13:45:32.583372690 IST",
          "frame.offset_shift": "0.000000000",
          "frame.time_epoch": "1556093732.583372690",
          "frame.time_delta": "0.000000000",
          "frame.time_delta_displayed": "0.000000000",
          "frame.time_relative": "0.000000000",
          "frame.number": "1",
          "frame.len": "68",
          "frame.cap_len": "68",
          "frame.marked": "0",
          "frame.ignored": "0",
          "frame.protocols": "eth:ethertype:vlan:ethertype:arp"
        },
        "eth": {
          "eth.dst": "ff:ff:ff:ff:ff:ff",
          "eth.dst_tree": {
            "eth.dst_resolved": "Broadcast",
            "eth.addr": "ff:ff:ff:ff:ff:ff",
            "eth.addr_resolved": "Broadcast",
            "eth.lg": "1",
            "eth.ig": "1"
          },
          "eth.src": "00:00:00:11:11:01",
          "eth.src_tree": {
            "eth.src_resolved": "00:00:00_11:11:01",
            "eth.addr": "00:00:00:11:11:01",
            "eth.addr_resolved": "00:00:00_11:11:01",
            "eth.lg": "0",
            "eth.ig": "0"
          },
          "eth.type": "0x00008100"
        },
        "vlan": {
          "vlan.priority": "0",
          "vlan.cfi": "0",
          "vlan.id": "100",
          "vlan.etype": "0x00000806",
          "eth.padding": "00:00:00:00:00:00:00:00:00:00:00:00:00:00",
          "vlan.trailer": "00:00:00:00:d4:83:43:fc"
        },
        "arp": {
          "arp.hw.type": "1",
          "arp.proto.type": "0x00000800",
          "arp.hw.size": "6",
          "arp.proto.size": "4",
          "arp.opcode": "1",
          "arp.src.hw_mac": "00:00:00:11:11:01",
          "arp.src.proto_ipv4": "56.1.1.103",
          "arp.dst.hw_mac": "00:00:00:00:00:00",
          "arp.dst.proto_ipv4": "192.85.2.1"
        }
      }
    }
  }
  ,
  {
    "_index": "packets-2019-04-26",
    "_type": "pcap_file",
    "_score": null,
    "_source": {
      "layers": {
        "frame": {
          "frame.encap_type": "1",
          "frame.time": "May  6, 2014 19:16:59.220915260 IST",
          "frame.offset_shift": "0.000000000",
          "frame.time_epoch": "1399384019.220915260",
          "frame.time_delta": "2.000762360",
          "frame.time_delta_displayed": "2.000762360",
          "frame.time_relative": "3.992219060",
          "frame.number": "3",
          "frame.len": "82",
          "frame.cap_len": "82",
          "frame.marked": "0",
          "frame.ignored": "0",
          "frame.protocols": "eth:ethertype:ipv6:icmpv6"
        },
        "eth": {
          "eth.dst": "33:33:00:00:00:01",
          "eth.dst_tree": {
            "eth.dst_resolved": "IPv6mcast_01",
            "eth.addr": "33:33:00:00:00:01",
            "eth.addr_resolved": "IPv6mcast_01",
            "eth.lg": "1",
            "eth.ig": "1"
          },
          "eth.src": "00:10:94:00:34:01",
          "eth.src_tree": {
            "eth.src_resolved": "Performa_00:34:01",
            "eth.addr": "00:10:94:00:34:01",
            "eth.addr_resolved": "Performa_00:34:01",
            "eth.lg": "0",
            "eth.ig": "0"
          },
          "eth.type": "0x000086dd",
          "eth.fcs": "0xcda4dabd",
          "eth.fcs.status": "1"
        },
        "ipv6": {
          "ipv6.version": "6",
          "ip.version": "6",
          "ipv6.tclass": "0x00000000",
          "ipv6.tclass_tree": {
            "ipv6.tclass.dscp": "0",
            "ipv6.tclass.ecn": "0"
          },
          "ipv6.flow": "0x00000000",
          "ipv6.plen": "24",
          "ipv6.nxt": "58",
          "ipv6.hlim": "255",
          "ipv6.src": "fe80::210:94ff:fe00:3401",
          "ipv6.addr": "fe80::210:94ff:fe00:3401",
          "ipv6.src_host": "fe80::210:94ff:fe00:3401",
          "ipv6.host": "fe80::210:94ff:fe00:3401",
          "ipv6.src_sa_mac": "00:10:94:00:34:01",
          "ipv6.sa_mac": "00:10:94:00:34:01",
          "ipv6.dst": "ff02::1",
          "ipv6.addr": "ff02::1",
          "ipv6.dst_host": "ff02::1",
          "ipv6.host": "ff02::1",
          "Source GeoIP: Unknown": "",
          "Destination GeoIP: Unknown": ""
        },
        "icmpv6": {
          "icmpv6.type": "134",
          "icmpv6.code": "0",
          "icmpv6.checksum": "0x0000a9e5",
          "icmpv6.checksum.status": "1",
          "icmpv6.nd.ra.cur_hop_limit": "64",
          "icmpv6.nd.ra.flag": "0x00000000",
          "icmpv6.nd.ra.flag_tree": {
            "icmpv6.nd.ra.flag.m": "0",
            "icmpv6.nd.ra.flag.o": "0",
            "icmpv6.nd.ra.flag.h": "0",
            "icmpv6.nd.ra.flag.prf": "0",
            "icmpv6.nd.ra.flag.p": "0",
            "icmpv6.nd.ra.flag.rsv": "0"
          },
          "icmpv6.nd.ra.router_lifetime": "30",
          "icmpv6.nd.ra.reachable_time": "0",
          "icmpv6.nd.ra.retrans_timer": "0",
          "icmpv6.opt": {
            "icmpv6.opt.type": "1",
            "icmpv6.opt.length": "1",
            "icmpv6.opt.linkaddr": "00:10:94:00:34:01",
            "icmpv6.opt.src_linkaddr": "00:10:94:00:34:01"
          }
        }
      }
    }
  }
] """
    data_dict = [
{
    "_index": "packets-2019-04-30",
    "_type": "pcap_file",
    "_score": None,
    "_source": {
      "layers": {
        "frame": {
          "frame.encap_type": "1",
          "frame.time": "Apr 24, 2019 13:45:32.583372690 IST",
          "frame.offset_shift": "0.000000000",
          "frame.time_epoch": "1556093732.583372690",
          "frame.time_delta": "0.000000000",
          "frame.time_delta_displayed": "0.000000000",
          "frame.time_relative": "0.000000000",
          "frame.number": "1",
          "frame.len": "68",
          "frame.cap_len": "68",
          "frame.marked": "0",
          "frame.ignored": "0",
          "frame.protocols": "eth:ethertype:vlan:ethertype:arp"
        },
        "eth": {
          "eth.dst": "ff:ff:ff:ff:ff:ff",
          "eth.dst_tree": {
            "eth.dst_resolved": "Broadcast",
            "eth.addr": "ff:ff:ff:ff:ff:ff",
            "eth.addr_resolved": "Broadcast",
            "eth.lg": "1",
            "eth.ig": "1"
          },
          "eth.src": "00:00:00:11:11:01",
          "eth.src_tree": {
            "eth.src_resolved": "00:00:00_11:11:01",
            "eth.addr": "00:00:00:11:11:01",
            "eth.addr_resolved": "00:00:00_11:11:01",
            "eth.lg": "0",
            "eth.ig": "0"
          },
          "eth.type": "0x00008100"
        },
        "vlan": {
          "vlan.priority": "0",
          "vlan.cfi": "0",
          "vlan.id": "100",
          "vlan.etype": "0x00000806",
          "eth.padding": "00:00:00:00:00:00:00:00:00:00:00:00:00:00",
          "vlan.trailer": "00:00:00:00:d4:83:43:fc"
        },
        "arp": {
          "arp.hw.type": "1",
          "arp.proto.type": "0x00000800",
          "arp.hw.size": "6",
          "arp.proto.size": "4",
          "arp.opcode": "1",
          "arp.src.hw_mac": "00:00:00:11:11:01",
          "arp.src.proto_ipv4": "56.1.1.103",
          "arp.dst.hw_mac": "00:00:00:00:00:00",
          "arp.dst.proto_ipv4": "192.85.2.1"
        }
      }
    }
  }
  ,
  {
    "_index": "packets-2019-04-26",
    "_type": "pcap_file",
    "_score": None,
    "_source": {
      "layers": {
        "frame": {
          "frame.encap_type": "1",
          "frame.time": "May  6, 2014 19:16:59.220915260 IST",
          "frame.offset_shift": "0.000000000",
          "frame.time_epoch": "1399384019.220915260",
          "frame.time_delta": "2.000762360",
          "frame.time_delta_displayed": "2.000762360",
          "frame.time_relative": "3.992219060",
          "frame.number": "3",
          "frame.len": "82",
          "frame.cap_len": "82",
          "frame.marked": "0",
          "frame.ignored": "0",
          "frame.protocols": "eth:ethertype:ipv6:icmpv6"
        },
        "eth": {
          "eth.dst": "33:33:00:00:00:01",
          "eth.dst_tree": {
            "eth.dst_resolved": "IPv6mcast_01",
            "eth.addr": "33:33:00:00:00:01",
            "eth.addr_resolved": "IPv6mcast_01",
            "eth.lg": "1",
            "eth.ig": "1"
          },
          "eth.src": "00:10:94:00:34:01",
          "eth.src_tree": {
            "eth.src_resolved": "Performa_00:34:01",
            "eth.addr": "00:10:94:00:34:01",
            "eth.addr_resolved": "Performa_00:34:01",
            "eth.lg": "0",
            "eth.ig": "0"
          },
          "eth.type": "0x000086dd",
          "eth.fcs": "0xcda4dabd",
          "eth.fcs.status": "1"
        },
        "ipv6": {
          "ipv6.version": "6",
          "ip.version": "6",
          "ipv6.tclass": "0x00000000",
          "ipv6.tclass_tree": {
            "ipv6.tclass.dscp": "0",
            "ipv6.tclass.ecn": "0"
          },
          "ipv6.flow": "0x00000000",
          "ipv6.plen": "24",
          "ipv6.nxt": "58",
          "ipv6.hlim": "255",
          "ipv6.src": "fe80::210:94ff:fe00:3401",
          "ipv6.addr": "fe80::210:94ff:fe00:3401",
          "ipv6.src_host": "fe80::210:94ff:fe00:3401",
          "ipv6.host": "fe80::210:94ff:fe00:3401",
          "ipv6.src_sa_mac": "00:10:94:00:34:01",
          "ipv6.sa_mac": "00:10:94:00:34:01",
          "ipv6.dst": "ff02::1",
          "ipv6.addr": "ff02::1",
          "ipv6.dst_host": "ff02::1",
          "ipv6.host": "ff02::1",
          "Source GeoIP: Unknown": "",
          "Destination GeoIP: Unknown": ""
        },
        "icmpv6": {
          "icmpv6.type": "134",
          "icmpv6.code": "0",
          "icmpv6.checksum": "0x0000a9e5",
          "icmpv6.checksum.status": "1",
          "icmpv6.nd.ra.cur_hop_limit": "64",
          "icmpv6.nd.ra.flag": "0x00000000",
          "icmpv6.nd.ra.flag_tree": {
            "icmpv6.nd.ra.flag.m": "0",
            "icmpv6.nd.ra.flag.o": "0",
            "icmpv6.nd.ra.flag.h": "0",
            "icmpv6.nd.ra.flag.prf": "0",
            "icmpv6.nd.ra.flag.p": "0",
            "icmpv6.nd.ra.flag.rsv": "0"
          },
          "icmpv6.nd.ra.router_lifetime": "30",
          "icmpv6.nd.ra.reachable_time": "0",
          "icmpv6.nd.ra.retrans_timer": "0",
          "icmpv6.opt": {
            "icmpv6.opt.type": "1",
            "icmpv6.opt.length": "1",
            "icmpv6.opt.linkaddr": "00:10:94:00:34:01",
            "icmpv6.opt.src_linkaddr": "00:10:94:00:34:01"
          }
        }
      }
    }
  }
 ]
    @patch("subprocess.getoutput", return_value=data_json)
    @patch("json.loads", return_value=data_dict)
    def test_extract_arp_packet_from_capture(self, patch1, patch2):
        logging.info(".........Test : extract_arp_packet_from_capture ....")

        expected_dict = { "00:00:00:11:11:01,56.1.1.103" : 1}
        self.assertEqual(extract_arp_packet_from_capture(capture_file="some-test-file"), expected_dict)

    @patch("subprocess.getoutput", return_value=data_json)
    @patch("json.loads", return_value=data_dict)
    def test_extract_arp_packet_from_capture(self, patch1, patch2):
        logging.info(".........Test : extract_icmpv6_packet_from_capture ....")

        expected_dict = { "00:10:94:00:34:01,fe80::210:94ff:fe00:3401" : '134'}
        self.assertEqual(extract_icmpv6_packet_from_capture(capture_file="some-test-file"), expected_dict)



if __name__ == '__main__':
    file_name, extension = os.path.splitext(os.path.basename(__file__))
    logging.basicConfig(filename=file_name+".log", level=logging.INFO)
    unittest.main()
