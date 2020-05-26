# coding: UTF-8
"""All unit test cases for ROUTE INSTANCE module"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

from unittest import TestCase, mock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.route.route import route


class TestRoute(TestCase):
    """Unitest cases for ROUTE INSTANCE module"""
    def setUp(self):
        """setup before all case"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = route()

        self.response = {}
        self.response["HA_SINGLE_INSTANCE"] = """
    <instance-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-routing" junos:style="terse">
        <instance-core>
            <instance-name>master</instance-name>
            <instance-type>forwarding</instance-type>
            <instance-rib>
                <irib-name>inet.0</irib-name>
                <irib-active-count>22</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.0</irib-name>
                <irib-active-count>7</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
    </instance-information>
        """

        self.response["HA_MULTI_INSTANCE"] = """
    <instance-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-routing" junos:style="terse">
        <instance-core>
            <instance-name>master</instance-name>
            <instance-type>forwarding</instance-type>
            <instance-rib>
                <irib-name>inet.0</irib-name>
                <irib-active-count>22</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.0</irib-name>
                <irib-active-count>7</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
        <instance-core>
            <instance-name>__juniper_private1__</instance-name>
            <instance-type>forwarding</instance-type>
            <instance-rib>
                <irib-name>__juniper_private1__.inet.0</irib-name>
                <irib-active-count>12</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
        <instance-core>
            <instance-name>__juniper_private2__</instance-name>
            <instance-type>forwarding</instance-type>
            <instance-rib>
                <irib-name>__juniper_private2__.inet.0</irib-name>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>1</irib-hidden-count>
            </instance-rib>
        </instance-core>
        <instance-core>
            <instance-name>__juniper_private3__</instance-name>
            <instance-type>forwarding</instance-type>
        </instance-core>
        <instance-core>
            <instance-name>__juniper_private4__</instance-name>
            <instance-type>forwarding</instance-type>
            <instance-rib>
                <irib-name>__juniper_private4__.inet.0</irib-name>
                <irib-active-count>2</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
        <instance-core>
            <instance-name>__master.anon__</instance-name>
            <instance-type>forwarding</instance-type>
        </instance-core>
        <instance-core>
            <instance-name>mgmt_junos</instance-name>
            <instance-type>forwarding</instance-type>
        </instance-core>
    </instance-information>
        """


        self.response["HA_SINGLE_INSTANCE_BRIEF"] = """
    <instance-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-routing" junos:style="terse">
        <instance-core>
            <instance-name>master</instance-name>
            <instance-type>forwarding</instance-type>
            <instance-rib>
                <irib-name>inet.0</irib-name>
                <irib-active-count>18</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.0</irib-name>
                <irib-active-count>1</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
    </instance-information>
        """

        self.response["HA_SINGLE_INSTANCE_DETAIL"] = """
    <instance-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-routing" junos:style="detail">
        <instance-core>
            <instance-name>master</instance-name>
            <router-id>10.208.133.147</router-id>
            <instance-type>forwarding</instance-type>
            <instance-state>Active</instance-state>
            <instance-rib>
                <irib-name>inet.0</irib-name>
                <irib-route-count>18</irib-route-count>
                <irib-active-count>18</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.0</irib-name>
                <irib-route-count>1</irib-route-count>
                <irib-active-count>1</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
    </instance-information>
        """

        self.response["HA_SINGLE_INSTANCE_EXTENSIVE"] = """
    <instance-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-routing" junos:style="detail">
        <instance-core>
            <instance-name>master</instance-name>
            <router-id>10.208.133.147</router-id>
            <instance-type>forwarding</instance-type>
            <instance-state>Active</instance-state>
            <instance-rib>
                <irib-name>inet.0</irib-name>
                <irib-route-count>20</irib-route-count>
                <irib-active-count>20</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet.1</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet.2</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet.3</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>iso.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>mpls.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>__mpls-oam__.mpls.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.0</irib-name>
                <irib-route-count>5</irib-route-count>
                <irib-active-count>5</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.1</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.2</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.3</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>l2circuit.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>mdt.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>l2protection.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>lsdist.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>lsdist.1</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inetcolor.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6color.0</irib-name>
                <irib-route-count>0</irib-route-count>
                <irib-active-count>0</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
    </instance-information>
        """

        self.response["HA_SINGLE_INSTANCE_SUMMARY"] = """
    <instance-information xmlns="http://xml.juniper.net/junos/18.1I0/junos-routing" junos:style="terse">
        <instance-core>
            <instance-name>master</instance-name>
            <instance-type>forwarding</instance-type>
            <instance-rib>
                <irib-name>inet.0</irib-name>
                <irib-active-count>22</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
            <instance-rib>
                <irib-name>inet6.0</irib-name>
                <irib-active-count>5</irib-active-count>
                <irib-holddown-count>0</irib-holddown-count>
                <irib-hidden-count>0</irib-hidden-count>
            </instance-rib>
        </instance-core>
    </instance-information>
        """

        self.response["SA_INSTANCE_TEXT"] = """
Instance             Type
         Primary RIB                                     Active/holddown/hidden
master               forwarding
         inet.0                                          18/0/0

__juniper_private1__ forwarding
         __juniper_private1__.inet.0                     6/0/0

__juniper_private2__ forwarding
         __juniper_private2__.inet.0                     0/0/1

__juniper_private3__ forwarding

__juniper_private4__ forwarding
         __juniper_private4__.inet.0                     2/0/0

__master.anon__      forwarding
        """

    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_route_instance_entry(self, mock_execute_cli_command_on_device):
        """Test get source nat interface nat ports info"""
        mock_device_ins = mock.Mock()

        print("Get master instance info from HA topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_SINGLE_INSTANCE"]
        response = self.ins.get_route_instance_entry(device=mock_device_ins, name="master")
        print(self.tool.pprint(response))
        self.assertIsInstance(response, (list, tuple))
        self.assertEqual(len(response), 2)

        print("Get all instance info from HA topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_MULTI_INSTANCE"]
        response = self.ins.get_route_instance_entry(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertIsInstance(response, (list, tuple))
        self.assertEqual(len(response), 8)
        self.assertEqual(int(response[5]["instance_rib_irib_active_count"]), 2)

        print("Get brief all instance info from HA topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_SINGLE_INSTANCE_BRIEF"]
        response = self.ins.get_route_instance_entry(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertIsInstance(response, (list, tuple))
        self.assertEqual(len(response), 2)
        self.assertEqual(int(response[0]["instance_rib_irib_active_count"]), 18)

        print("Get detail all instance info from HA topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_SINGLE_INSTANCE_DETAIL"]
        response = self.ins.get_route_instance_entry(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertIsInstance(response, (list, tuple))
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["router_id"], "10.208.133.147")

        print("Get extensive all instance info from HA topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_SINGLE_INSTANCE_EXTENSIVE"]
        response = self.ins.get_route_instance_entry(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertIsInstance(response, (list, tuple))
        self.assertEqual(len(response), 18)
        self.assertEqual(response[17]["instance_rib_irib_name"], "inet6color.0")

        print("Get summary all instance info from HA topo")
        mock_execute_cli_command_on_device.return_value = self.response["HA_SINGLE_INSTANCE_SUMMARY"]
        response = self.ins.get_route_instance_entry(device=mock_device_ins)
        print(self.tool.pprint(response))
        self.assertIsInstance(response, (list, tuple))
        self.assertGreaterEqual(len(response), 1)

        print("Get route instance info by text and more options")
        mock_execute_cli_command_on_device.return_value = self.response["SA_INSTANCE_TEXT"]
        response = self.ins.get_route_instance_entry(device=mock_device_ins, return_mode="text", more_options="summary")
        print(self.tool.pprint(response))
        self.assertIsInstance(response, str)
        self.assertRegex(response, r"__juniper_private1__.inet.0")

        print("Invalid return_mode value")
        mock_execute_cli_command_on_device.return_value = self.response["HA_SINGLE_INSTANCE_SUMMARY"]
        self.assertRaisesRegex(
            ValueError,
            r"'return_mode' must be 'ENTRY_LIST' or 'TEXT'",
            self.ins.get_route_instance_entry,
            device=mock_device_ins, return_mode="Unknown",
        )

        print("Cannot get response from device")
        mock_execute_cli_command_on_device.return_value = False
        response = self.ins.get_route_instance_entry(device=mock_device_ins, more_options="summary")
        self.assertFalse(response)

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_search_route_instance_entry(self, mock_execute_cli_command_on_device):
        """Test search source nat interface nat ports info"""
        mock_device_ins = mock.Mock()

        print("search master instance info from HA topo")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_SINGLE_INSTANCE"])
        response = self.ins.search_route_instance_entry(
            mock_device_ins,
            return_mode="counter",
            instance_name="master",
            instance_rib_irib_active_count=22,
            instance_rib_irib_hidden_count=0,
        )
        self.assertEqual(response, 1)

        print("search master instance from previous result")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_SINGLE_INSTANCE"])
        self.ins.runtime["route_instance_entry_list"] = self.ins.get_route_instance_entry(mock_device_ins)
        response = self.ins.search_route_instance_entry(
            mock_device_ins,
            match_from_previous_response=True,
            return_mode="counter",
            instance_name="master",
            instance_rib_irib_active_count=22,
            instance_rib_irib_hidden_count=0,
        )
        self.assertEqual(response, 1)

        print("search instance info with brief and not interested counter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_SINGLE_INSTANCE_BRIEF"])
        response = self.ins.search_route_instance_entry(
            mock_device_ins,
            instance_type="forwarding",
            instance_rib_irib_active_count=1,
            instance_rib_irib_holddown_count=0,
        )
        self.assertEqual(response, 1)

        print("search instance info with detail")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_SINGLE_INSTANCE_DETAIL"])
        response = self.ins.search_route_instance_entry(
            mock_device_ins,
            instance_type="forwarding",
            instance_state=("Active", "in"),
            instance_rib_irib_active_count=18,
            instance_rib_irib_holddown_count=0,
        )
        self.assertTrue(response)

        print("search instance info but entry don't have related parameter")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_SINGLE_INSTANCE_SUMMARY"])
        response = self.ins.search_route_instance_entry(
            mock_device_ins,
            instance_type="forwarding",
            instance_state=("Active", "in"),
            instance_rib_irib_active_count=22,
            instance_rib_irib_holddown_count=0,
        )
        self.assertFalse(response)

        print("search instance info with extensive")
        mock_execute_cli_command_on_device.return_value = self.xml.xml_string_to_dict(self.response["HA_SINGLE_INSTANCE_EXTENSIVE"])
        response = self.ins.search_route_instance_entry(
            mock_device_ins,
            return_mode="counter",
            instance_type="forwarding",
            instance_rib_irib_active_count=0,
            instance_rib_irib_holddown_count=0,
        )
        self.assertEqual(response, 16)
