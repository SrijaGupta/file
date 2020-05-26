from jnpr.toby.utils.linux import linux_network_config
from jnpr.toby.hldcl.unix.unix import UnixHost
from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.utils.linux.linux_network_config import configure_linux_interface
from jnpr.toby.utils.linux.linux_network_config import configure_ip_address
from jnpr.toby.utils.linux.linux_network_config import get_ip_address_type
from jnpr.toby.utils.linux.linux_network_config import restart_network_service
from jnpr.toby.utils.linux.linux_network_config import add_route
from jnpr.toby.utils.linux.linux_network_config import delete_route
from jnpr.toby.utils.linux.linux_network_config import add_arp
from jnpr.toby.utils.linux.linux_network_config import delete_arp
from jnpr.toby.utils.linux.linux_network_config import add_ipv6_neighbor
from jnpr.toby.utils.linux.linux_network_config import delete_ipv6_neighbor
from jnpr.toby.utils.linux.linux_network_config import get_linux_int_mac
from jnpr.toby.utils.linux.linux_network_config import get_linux_int_ip
from jnpr.toby.utils.linux.linux_network_config import get_linux_default_gateway
from jnpr.toby.utils.linux.linux_network_config import check_ip_forward
# To return response of shell() mehtod
class Response:

    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()
                         
    def test_check_configure_linux_interface_exception(self):
        try:
            configure_linux_interface()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is a mandatory argument")

        try:
            configure_linux_interface(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Interface is a mandatory argument")
                 
        try:
            configure_linux_interface(device=self.mocked_obj, interface=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Arguments are not enough to take any action!")
    
    def test_check_ipv6_configure_linux_interface_success(self):
        lst = [
               Response(""),
               Response("inet6 addr: 2005::1/"),
               Response(""),
               Response("inet6 addr: 2006::1/")
              ]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.assertEqual(
             configure_linux_interface(
                    device=self.mocked_obj,
                    address="2005::1",
                    interface="eth1",
                    mask="64"),
                    True)
        self.assertEqual(
             configure_linux_interface(
                    device=self.mocked_obj,
                    address="2006::1",
                    interface="eth2",
                    mask=64),
                    True)

    def test_check_ipv4_configure_linux_interface_success(self):
        lst = [
               Response(""),
               Response("inet addr:4.0.0.1  Bcast:4.255.255.255  Mask:255.0.0.0"),
               Response(""),
               Response("inet addr:6.0.0.1  Bcast:4.0.0.255  Mask:255.255.255.0"),
              ]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.assertEqual(
             configure_linux_interface(
                    device=self.mocked_obj,
                    address="4.0.0.1",
                    interface="eth1",
                    mask="8"),
                    True)
        self.assertEqual(
             configure_linux_interface(
                    device=self.mocked_obj,
                    address="6.0.0.1",
                    interface="eth2",
                    mask=24),
                    True)
                    
    def test_check_mtu_configure_linux_interface_success(self):
        lst = [Response(""),Response("mtu 2000")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             configure_linux_interface(
                    device=self.mocked_obj,
                    mtu="2000",
                    interface="eth1"),
                    True)
    
    def test_check_status_configure_linux_interface_success(self):
        lst = [Response(""),Response("state UP")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             configure_linux_interface(
                    device=self.mocked_obj,
                    status="up",
                    interface="eth1"),
                    True)
    
    
    def test_check_configure_ip_addr_exception(self):
        try:
            configure_ip_address()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

        try:
            configure_ip_address(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Interface and IPv4/IPv6 address are mandatory argument")


    def test_check_ipv6_configure_ip_addr_success(self):
        lst = [Response(""),Response("inet6 addr: 2005::1/")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.assertEqual(
             configure_ip_address(
                    device=self.mocked_obj,
                    address="2005::1",
                    interface="eth1",
                    mask="64"),
                    True)

    def test_check_ipv4_configure_ip_addr_success(self):
        lst = [Response(""),Response("inet addr:4.0.0.1  Bcast:4.255.255.255  Mask:255.0.0.0")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.assertEqual(
             configure_ip_address(
                    device=self.mocked_obj,
                    address="4.0.0.1",
                    interface="eth1",
                    mask="255.0.0.0"),
                    True)

    def test_check_configure_ip_addr_failure(self):
        lst = [Response(""),Response("inet6 addr: 2007::1/")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        get_ip_address_type=MagicMock(side_effect="ipv6")
        try:
            configure_ip_address(
                    device=self.mocked_obj,
                    address="2005::1",
                    interface="eth1",
                    mask="64")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "IPv4/IPv6 address is not configured successfully")

    def test_check_configure_ip_addr_failure(self):
        lst = [Response(""),Response("inet addr:4.0.1.1  Bcast:4.255.255.255  Mask:255.0.0.0")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        get_ip_address_type=MagicMock(side_effect="ipv4")
        try:
            configure_ip_address(
                    device=self.mocked_obj,
                    address="4.0.0.1",
                    interface="eth1",
                    mask="255.0.0.0")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "IPv4/IPv6 address is not configured successfully")

#---------------------------------------------------------------------

    def test_checkget_ip_address_type(self):
        self.assertEqual(
             get_ip_address_type(
                       address="10.2.2.2"),
                       "ipv4")
        self.assertEqual(
             get_ip_address_type(
                       address="2004::5"),
                       "ipv6")   

#-----------------------------------------------------------------------
    def test_check_restart_network_service_success(self):
        lst = [Response("Bringing up interface eth1:                                [OK]")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             restart_network_service(
                        device=self.mocked_obj),
                        True)

    def test_check_restart_network_service_exception(self):
        lst = [Response("Bringing up interface eth1:                                [FAILED]")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
             restart_network_service()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device is mandatory argument")
        
        try:
             restart_network_service(
                     device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Network service restart Failed")

#--------------------------------------------------------------------------

    def test_check_add_route_exception(self):
        try:
             add_route()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device argument is mandatory")

    def test_check_add_route_ipv4_default_gateway_success(self):
        lst = [Response(""),Response("0.0.0.0         10.209.95.254   0.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_route(
                     device=self.mocked_obj,
                     default_gateway="10.209.95.254"),
                     True)

    def test_check_add_route_ipv6_default_gateway_success(self):
        lst = [Response(""),Response("*/0                                         2006::1")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_route(
                     device=self.mocked_obj,
                     default_gateway="2006::1"),
                     True)

    def test_check_add_route_ipv4_default_gateway_fail(self):
        lst = [Response(""),Response("0.0.0.0         10.219.95.254   0.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_route(
                    device=self.mocked_obj,
                    default_gateway="10.209.95.254")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not configured")

    def test_check_add_route_ipv6_default_gateway_fail(self):
        lst = [Response(""),Response("*/0                                         2006::2")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_route(
                    device=self.mocked_obj,
                    default_gateway="2006::1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not configured")

    def test_check_add_route_ipv4_host_success(self):
        lst = [Response(""),Response("5.0.0.1         4.0.0.254   255.255.255.255         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_route(
                     device=self.mocked_obj,
                     host="5.0.0.1",
                     gateway="4.0.0.254"),
                     True)

    def test_check_add_route_ipv6_host_success(self):
        lst = [Response(""),Response("2005::1/128                                         2005::254   \n")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_route(
                     device=self.mocked_obj,
                     host="2005::1",
                     gateway="2005::254"),
                     True)

    def test_check_add_route_ipv4_host_fail(self):
        lst = [Response(""),Response("5.0.0.1         4.0.0.254   255.255.255.255         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_route(
                    device=self.mocked_obj,
                    host="10.209.95.254",
                    gateway="4.0.0.254")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not configured")

    def test_check_add_route_ipv6_host_fail(self):
        lst = [Response(""),Response("2005::1/128                                         2005::254   \n")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_route(
                    device=self.mocked_obj,
                    host="2006::1",
                    gateway="2005::254")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not configured")

    def test_check_add_route_host_exception(self):
        try:
            add_route(
                    device=self.mocked_obj,
                     host="10.209.95.254")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Gateway address is required for host based route")

    def test_check_add_route_network_exception(self):
        try:
            add_route(
                    device=self.mocked_obj,
                    network="5.0.0.0")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "network,netmask and gateway are required for network based route")

    def test_check_add_route_ipv4_network_success(self):
        lst = [Response(""),Response("5.0.0.0         4.0.0.254   255.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_route(
                     device=self.mocked_obj,
                     network="5.0.0.0",
                     gateway="4.0.0.254",
                     netmask="255.0.0.0"),
                     True)

    def test_check_add_route_ipv6_network_success(self):
        lst = [Response(""),Response("2005::/64                                         2004::254 ")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_route(
                     device=self.mocked_obj,
                     network="2005::",
                     gateway="2004::254",
                     netmask="64"),
                     True)

    def test_check_add_route_ipv4_network_fail(self):
        lst = [Response(""),Response("5.0.0.0         4.0.0.254   255.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_route(
                    device=self.mocked_obj,
                    network="5.0.0.0",
                    gateway="6.0.0.254",
                    netmask="255.0.0.0")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not configured")

    def test_check_add_route_ipv6_network_fail(self):
        lst = [Response(""),Response("2005::/64                                         2004::254")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_route(
                    device=self.mocked_obj,
                    network="2005::",
                    gateway="2001::25",
                    netmask="64")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not configured")

    def test_check_add_route_with_interface(self):
        lst = [Response(""),Response("5.0.0.0         4.0.0.254   255.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_route(
                     device=self.mocked_obj,
                     network="5.0.0.0",
                     gateway="4.0.0.254",
                     netmask="255.0.0.0",
                     interface="eth0"),
                     True)

#-----------------------------------------------------------------------------

    def test_check_delete_route_exception(self):
        try:
             delete_route()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device argument is mandatory")

    def test_check_delete_route_ipv4_default_gateway_success(self):
        lst = [Response(""),Response("0.0.0.0         10.209.95.254   0.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_route(
                     device=self.mocked_obj,
                     default_gateway="10.209.9.254"),
                     True)

    def test_check_delete_route_ipv6_default_gateway_success(self):
        lst = [Response(""),Response("*/0                                         2006::1")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_route(
                     device=self.mocked_obj,
                     default_gateway="2005::1"),
                     True)

    def test_check_delete_route_ipv4_default_gateway_fail(self):
        lst = [Response(""),Response("0.0.0.0         10.209.95.254   0.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_route(
                    device=self.mocked_obj,
                    default_gateway="10.209.95.254")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not deleted")

    def test_check_delete_route_ipv6_default_gateway_fail(self):
        lst = [Response(""),Response("*/0                                         2006::2")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_route(
                    device=self.mocked_obj,
                    default_gateway="2006::2")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not deleted")

    def test_check_delete_route_ipv4_host_success(self):
        lst = [Response(""),Response("6.0.0.1         4.0.0.254   255.255.255.255         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_route(
                     device=self.mocked_obj,
                     host="5.0.0.1"),
                     True)

    def test_check_delete_route_ipv6_host_success(self):
        lst = [Response(""),Response("2005::4/128                                         2005::254   \n")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_route(
                     device=self.mocked_obj,
                     host="2005::1"),
                     True)

    def test_check_delete_route_ipv4_host_fail(self):
        lst = [Response(""),Response("5.0.0.1         4.0.0.254   255.255.255.255         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_route(
                    device=self.mocked_obj,
                    host="5.0.0.1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not deleted")

    def test_check_delete_route_ipv6_host_fail(self):
        lst = [Response(""),Response("2005::1/128                                         2005::254   \n")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_route(
                    device=self.mocked_obj,
                    host="2005::1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not deleted")

    def test_check_delete_route_network_exception(self):
        try:
            delete_route(
                    device=self.mocked_obj,
                    network="5.0.0.0")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "network and netmask are required to delete network based route")

    def test_check_delete_route_ipv4_network_success(self):
        lst = [Response(""),Response("6.0.0.0         4.0.0.254   255.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_route(
                     device=self.mocked_obj,
                     network="5.0.0.0",
                     gateway="4.0.0.254",
                     netmask="255.0.0.0"),
                     True)

    def test_check_delete_route_ipv6_network_success(self):
        lst = [Response(""),Response("2006::/64                                         2004::254 ")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_route(
                     device=self.mocked_obj,
                     network="2005::",
                     gateway="2004::254",
                     netmask="64"),
                     True)

    def test_check_delete_route_ipv4_network_fail(self):
        lst = [Response(""),Response("5.0.0.0         4.0.0.254   255.0.0.0         UG        0 0          0 eth0")]
        get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_route(
                    device=self.mocked_obj,
                    network="5.0.0.0",
                    gateway="4.0.0.254",
                    netmask="255.0.0.0")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not deleted")

    def test_check_delete_route_ipv6_network_fail(self):
        lst = [Response(""),Response("2005::/64                                         2004::254")]
        get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_route(
                    device=self.mocked_obj,
                    network="2005::",
                    gateway="2004::25",
                    netmask="64")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Route is not deleted")

#-------------------------------------------------------------------------------------------------

    def test_check_add_arp_exception(self):
        try:
             add_arp()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device is mandatory argument")

        try:
            add_arp(
                    device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ip_addr and hw_addr are mandatory argument")

    def test_check_add_arp_success(self):
        lst = [Response(""),Response("i? (10.209.95.254) at 84:18:88:14:A0:30 [ether] on eth0")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             add_arp(
                     device=self.mocked_obj,
                     ip_address="10.209.95.254",
                     hardware_address="84:18:88:14:A0:30"),
                     True)

    def test_check_add_arp_unsuccess(self):
        lst = [Response(""),Response("i? (10.21.95.254) at 84:18:88:14:A0:30 [ether] on eth0")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_arp(
                    device=self.mocked_obj,
                     ip_address="10.1.95.254",
                     hardware_address="84:18:88:14:A0:30")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ARP entry is not added successfully")

#-------------------------------------------------------------------------------

    def test_check_delete_arp_exception(self):
        try:
            delete_arp()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device is mandatory argument")

        try:
            delete_arp(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ip_addr is mandatory argument")

    def test_check_delete_arp_success(self):
        lst = [Response(""),Response("i? (10.2.95.254) at 84:18:88:14:A0:30 [ether] on eth0")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_arp(
                     device=self.mocked_obj,
                     ip_address="10.209.95.254"),
                     True)

    def test_check_delete_arp_unsuccess(self):
        lst = [Response(""),Response("i? (10.1.95.254) at 84:18:88:14:A0:30 [ether] on eth0")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_arp(
                    device=self.mocked_obj,
                     ip_address="10.1.95.254")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ARP entry is not deleted successfully")

#-------------------------------------------------------------------------------------

    def test_check_add_ipv6_neighbor_exception(self):
        try:
             add_ipv6_neighbor()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device is mandatory argument")

        try:
            add_ipv6_neighbor(
                    device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipv6_address,link_address and interface are mandatory arguments")

    def test_check_add_ipv6_neighbor_success(self):
        lst = [Response(""),Response("2001::1 dev eth1 lladdr 02:01:02:03:04:05 nud permanent")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
            add_ipv6_neighbor(
                     device=self.mocked_obj,
                     ipv6_address="2001::1",
                     link_address="02:01:02:03:04:05",
                     interface="eth1"),
                     True)

    def test_check_add_ipv6_neighbor_unsuccess(self):
        lst = [Response(""),Response("2002::2 dev eth1 lladdr 02:01:02:03:04:05 nud permanent")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            add_ipv6_neighbor(
                    device=self.mocked_obj,
                     ipv6_address="2001::1",
                     link_address="84:18:88:14:A0:30",
                     interface="eth1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Neighbor is not added successfully")

#-------------------------------------------------------------------------

    def test_check_delete_ipv6_neighbor_exception(self):
        try:
             delete_ipv6_neighbor()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device is mandatory argument")

        try:
            delete_ipv6_neighbor(
                    device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipv6_address,link_address and interface are mandatory arguments")

    def test_check_delete_ipv6_neighbor_success(self):
        lst = [Response(""),Response("2001::2 dev eth1 lladdr 02:01:02:03:04:05 nud permanent")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             delete_ipv6_neighbor(
                     device=self.mocked_obj,
                     ipv6_address="2001::1",
                     link_address="02:01:02:03:04:05",
                     interface="eth1"),
                     True)

    def test_check_delete_ipv6_neighbor_unsuccess(self):
        lst = [Response(""),Response("2001::2 dev eth1 lladdr 02:01:02:03:04:05 nud permanent")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            delete_ipv6_neighbor(
                    device=self.mocked_obj,
                     ipv6_address="2001::2",
                     link_address="02:01:02:03:04:05",
                     interface="eth1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Neighbor is not deleted successfully")

#------------------------------------------------------------------------------------------

    def test_check_get_linux_int_mac_exception(self):
        try:
             get_linux_int_mac()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device is mandatory argument")

        try:
            get_linux_int_mac(
                    device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "interface argument is mandatory")

    def test_check_get_linux_int_mac_success(self):
        lst = [Response("HWaddr 00:50:56:9E:42:39")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             get_linux_int_mac(
                     device=self.mocked_obj,
                     interface="eth1"),
                     "00:50:56:9E:42:39")

    def test_check_get_linux_int_mac_success_2(self):
        lst = [Response("ether 00:50:56:9E:42:39")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             get_linux_int_mac(
                     device=self.mocked_obj,
                     interface="eth1"),
                     "00:50:56:9E:42:39")
    def test_check_get_linux_int_mac_unsuccess(self):
        lst = [Response("HWaddriAAA 00:50:56:9E:42:39")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            get_linux_int_mac(
                     device=self.mocked_obj,
                     interface="eth1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Couldn't find the MAC of interface eth1")                            
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
    def test_check_get_linux_int_ip_exception(self):
        try:
             get_linux_int_ip()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "device is mandatory argument")

        try:
            get_linux_int_ip(
                    device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "interface argument is mandatory")

    def test_check_get_linux_int_ip_success1(self):
        lst = [Response("inet addr:10.16.17.29 ")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             get_linux_int_ip(
                     device=self.mocked_obj,
                     interface="eth1"),
                     "10.16.17.29")

    def test_check_get_linux_int_ip_success2(self):
        lst = [Response("inet 10.16.17.29 ")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             get_linux_int_ip(
                     device=self.mocked_obj,
                     interface="eth1"),
                     "10.16.17.29")

    def test_check_get_linux_int_ip_unsuccess(self):
        lst = [Response("inet addr233:10.16.17.29")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            get_linux_int_ip(
                     device=self.mocked_obj,
                     interface="eth1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Ipv4 address not configured in interface")

#--------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------- 
    def test_get_linux_default_gateway_exception(self):
        try:
           get_linux_default_gateway() 
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Linux handle is a mandatory argument")


    def test_get_linux_default_gateway_1(self):
        lst = [Response("default via 10.209.95.254 dev")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(get_linux_default_gateway(device=self.mocked_obj), "10.209.95.254")

    def test_get_linux_default_gateway_2(self):
        lst = [Response("default via 10.209.95.254 Suchi")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            get_linux_default_gateway(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Couldn't find the default gateway")


#--------------------------------------------------------------------------------------------
    def test_check_ip_forward_exception(self):
        try:
           check_ip_forward()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Linux handle is a mandatory argument")


        lst = [Response("net.ipv4.ip_forward = suchi"), Response(""), Response(""), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(check_ip_forward(device=self.mocked_obj, mgt_intf="eth0", fwd_intf="eth1"), None)

    def test_check_ip_forward_execution_1(self):
        lst = [Response("net.ipv4.ip_forward = 1"), Response(""), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(check_ip_forward(device=self.mocked_obj, mgt_intf="eth0", fwd_intf="eth1"), None)

#-------------------------------------------------------------------------------------------
    def test_configure_linux_tunnel_success_1(self):
        lst = [Response(""),Response("tun                    17051  0"),Response(""),Response("ipip                    8435  0"),Response(""),Response(""),Response(""),Response("dslite: ip/ip  remote 2.1.1.2  local 2.1.1.1  dev eth1")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2.1.1.2",
                     local_address="2.1.1.1",
                     interface="eth1",
                     tunnel_name="dslite"),
                     True)

    def test_configure_linux_tunnel_success_2(self):
        lst = [Response(""),Response("tun                    17051  0"),Response(""),Response("ip6_tunnel             13489  0"),Response(""),Response(""),Response(""),Response("dslite: ip/ipv6 remote 2002:2010::1401:1 local 2002:2010::1401:65 dev eth1")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
            linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2002:2010::1401:1",
                     local_address="2002:2010::1401:65",
                     interface="eth1",
                     tunnel_name="dslite"),
                     True)


    def test_configure_linux_tunnel_exception_1(self):
        try:
            linux_network_config.configure_linux_tunnel()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")
        try:
            linux_network_config.configure_linux_tunnel(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "remote address,local address,device interface\
                and tunnel name are mandatory arguments")

    def test_configure_linux_tunnel_exception_2(self):
        lst = [Response(""),Response("tun                    17051  0"),Response(""),Response("ipip                    8435  0"),Response(""),Response(""),Response(""),Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
             linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2.1.1.2",
                     local_address="2.1.1.1",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipip tunnel is not added successfully")


    def test_configure_linux_tunnel_exception_3(self):
        lst = [Response(""),Response("tun                    17051  0"),Response(""),Response("ip6_tunnel             13489  0"),Response(""),Response(""),Response(""),Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2002:2010::1401:1",
                     local_address="2002:2010::1401:65",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipip6 tunnel is not added successfully")


    def test_configure_linux_tunnel_exception_4(self):
        lst = [Response(""),Response("tun          17051  0")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2002:2010::1401:1",
                     local_address="2.1.1.1",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Remote and Local IP versions are not same")


    def test_configure_linux_tunnel_exception_5(self):
        lst = [Response(""),Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2002:2010::1401:1",
                     local_address="2002:2010::1401:65",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "tunnel service module not up")

    def test_configure_linux_tunnel_exception_6(self):
        lst = [Response(""),Response("tun                    17051  0"),Response(""),Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2002:2010::1401:1",
                     local_address="2002:2010::1401:65",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipip6 tunnel service not up")



    def test_configure_linux_tunnel_exception_7(self):
        lst = [Response(""),Response("tun                    17051  0"),Response(""),Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            linux_network_config.configure_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2.1.1.2",
                     local_address="2.1.1.1",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipip tunnel service not up")


    def test_delete_linux_tunnel_success_1(self):
        lst = [Response(""),Response(""),Response(""),Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             linux_network_config.delete_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2.1.1.2",
                     local_address="2.1.1.1",
                     interface="eth1",
                     tunnel_name="dslite"),
                     True)


    def test_delete_linux_tunnel_success_2(self):
        lst = [Response(""),Response(""),Response(""),Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             linux_network_config.delete_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2002:2010::1401:1",
                     local_address="2002:2010::1401:65",
                     interface="eth1",
                     tunnel_name="dslite"),
                     True)


    def test_delete_linux_tunnel_exception_1(self):
        try:
            linux_network_config.delete_linux_tunnel()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")
        try:
            linux_network_config.delete_linux_tunnel(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "remote address,local address,device interface\
                and tunnel name are mandatory arguments")


    def test_delete_linux_tunnel_exception_2(self):
        lst = [Response(""),Response(""),Response(""),Response("dslite: ip/ipv6 remote 2002:2010::1401:1 local 2002:2010::1401:65 dev eth1")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            linux_network_config.delete_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2002:2010::1401:1",
                     local_address="2002:2010::1401:65",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipip6 tunnel is not deleted successfully")


    def test_delete_linux_tunnel_exception_3(self):
        lst = [Response(""),Response(""),Response(""),Response("dslite: ip/ip  remote 2.1.1.2  local 2.1.1.1  dev eth1")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)

        try:
            linux_network_config.delete_linux_tunnel(
                     device=self.mocked_obj,
                     remote_address="2.1.1.2",
                     local_address="2.1.1.1",
                     interface="eth1",
                     tunnel_name="dslite"),

        except Exception as err:
            self.assertEqual(
                err.args[0],
                "ipip tunnel is not deleted successfully")


if __name__ == '__main__': 
    unittest.main()
