# coding: UTF-8
"""All unit test cases for LSYS module"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

from unittest import TestCase, mock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.lsys.lsys import lsys
from jnpr.toby.security.chassis.chassis import chassis


class TestLsys(TestCase):
    """Unitest cases for LSYS module"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = lsys()

        self.response = {}
        self.response["SA_LSYS_MULTITENANCY"] = """
    <show-mtenancy xmlns="http://xml.juniper.net/junos/18.2I0/junos-lsys-lic">
        <mtenancy-mode-config>logical-domain</mtenancy-mode-config>
        <mtenancy-mode-running>logical-domain</mtenancy-mode-running>
    </show-mtenancy>
        """

        self.response["SA_LSYS_MULTITENANCY_IN_LSYS"] = """
    <show-mtenancy xmlns="http://xml.juniper.net/junos/18.2I0/junos-lsys-lic">
        <mtenancy-mode-config>logical-system</mtenancy-mode-config>
        <mtenancy-mode-running>logical-system</mtenancy-mode-running>
    </show-mtenancy>
        """

        self.response["HA_LSYS_MULTITENANCY"] = """
    <multi-routing-engine-results>

        <multi-routing-engine-item>

            <re-name>node1</re-name>

            <show-mtenancy xmlns="http://xml.juniper.net/junos/18.2I0/junos-lsys-lic">
                <mtenancy-mode-config>logical-domain</mtenancy-mode-config>
                <mtenancy-mode-running>logical-domain</mtenancy-mode-running>
            </show-mtenancy>
        </multi-routing-engine-item>

    </multi-routing-engine-results>
        """

        self.response["SA_LSYS_MULTITENANCY_NEED_REBOOT"] = """
    <show-mtenancy xmlns="http://xml.juniper.net/junos/18.2I0/junos-lsys-lic">
        <mtenancy-mode-config>logical-domain</mtenancy-mode-config>
        <mtenancy-mode-config-status>(configuration changed: must reboot!)</mtenancy-mode-config-status>
        <mtenancy-mode-running>logical-system</mtenancy-mode-running>
        <mtenancy-mode-running-status>(remain same until reboot)</mtenancy-mode-running-status>
    </show-mtenancy>
        """


    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(chassis, "waiting_for_pic_online")
    @mock.patch.object(dev, "reboot_device")
    @mock.patch.object(dev, "execute_config_command_on_device")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_change_multitenancy_mode(self, mock_send_cli_cmd, mock_send_conf_cmd, mock_reboot, mock_waiting_for_pic_online):
        """checking change multitenancy mode"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.is_ha.return_value = True

        print("SA setup that alread in wanted mode")
        mock_device_ins.is_ha.return_value = False
        mock_send_conf_cmd.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LSYS_MULTITENANCY"])
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="ld")
        self.assertTrue(status)

        print("HA setup that alread in wanted mode")
        mock_device_ins.is_ha.return_value = False
        mock_send_conf_cmd.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LSYS_MULTITENANCY"])
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="ld")
        self.assertTrue(status)

        print("SA commit configuration failed")
        mock_device_ins.is_ha.return_value = False
        mock_send_conf_cmd.return_value = False
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="ld")
        self.assertFalse(status)

        print("HA waiting all PIC online failed")
        mock_device_ins.is_ha.return_value = False

        mock_send_conf_cmd.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LSYS_MULTITENANCY_NEED_REBOOT"])
        mock_reboot.return_value = True
        mock_waiting_for_pic_online.return_value = False
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="ld")
        self.assertFalse(status)

        print("checking 'mode' option")
        mock_device_ins.is_ha.return_value = False
        mock_send_conf_cmd.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LSYS_MULTITENANCY_IN_LSYS"])
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="lsys")
        self.assertTrue(status)

        print("checking 'mode' option invalid value")
        self.assertRaisesRegex(
            ValueError,
            r"'mode' must be",
            self.ins.change_multitenancy_mode,
            device=mock_device_ins, mode="unknown",
        )

        print("checking reboot device failed")
        mock_send_conf_cmd.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["SA_LSYS_MULTITENANCY_NEED_REBOOT"])
        mock_reboot.return_value = False
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="ld")
        self.assertFalse(status)

        mock_device_ins.node0.return_value = None
        mock_device_ins.node1.return_value = None

        print("checking for primary node")
        mock_device_ins.is_ha.return_value = True
        mock_device_ins.node0.is_master.return_value = True
        mock_reboot.return_value = True
        mock_send_cli_cmd.return_value = self.xml.xml_string_to_dict(self.response["HA_LSYS_MULTITENANCY"])
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="ld")
        self.assertTrue(status)

        mock_device_ins.node0.is_master.return_value = False
        status = self.ins.change_multitenancy_mode(device=mock_device_ins, mode="ld")
        self.assertTrue(status)
