# coding: UTF-8
# pylint: disable=attribute-defined-outside-init,invalid-name
"""All unit test cases for FLOW module"""
__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2019'

from unittest import TestCase, mock

from jnpr.toby.hldcl import device as dev
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.xml_tool import xml_tool
from jnpr.toby.security.flows.services_offload import services_offload
from jnpr.toby.security.chassis.chassis import chassis


class TestServicesOffload(TestCase):
    """UT cases"""
    def setUp(self):
        """setup before all cases"""
        self.tool = flow_common_tool()
        self.xml = xml_tool()
        self.ins = services_offload()

        self.response = {}
        self.response["SA_HE_FPC_PIC_STATUS_WITH_SOF"] = """
Slot 1   Online       SRX5k IOC II
  PIC 0  Online       10x 10GE SFP+- np-cache/services-offload
Slot 3   Online       SPC3
  PIC 0  Online       SPU Cp-Flow
  PIC 1  Online       SPU Flow
        """

        self.response["SA_HE_FPC_PIC_STATUS_WITHOUT_SOF"] = """
Slot 1   Online       SRX5k IOC II
  PIC 0  Online       10x 10GE SFP+-
Slot 3   Online       SPC3
  PIC 0  Online       SPU Cp-Flow
  PIC 1  Online       SPU Flow
        """

        self.response["SA_HE_SHOW_INTERFACE"] = """
Interface               Admin Link Proto    Local                 Remote
gr-0/0/0                up    up
ip-0/0/0                up    up
lt-0/0/0                up    up
xe-1/0/0                up    up
xe-1/0/1                up    up
xe-1/0/2                up    up
xe-1/0/3                up    up
xe-1/0/4                up    up
xe-1/0/5                up    up
xe-1/0/6                up    up
xe-1/0/7                up    up
xe-1/0/8                up    up
xe-2/0/9                up    up
xe-2/0/0                up    up
xe-2/0/1                up    up
xe-2/0/2                up    up
xe-2/0/3                up    up
xe-7/0/4                up    up
xe-7/0/5                up    up
xe-7/0/6                up    up
avs0                    up    up
avs1                    up    up
avs1.0                  up    up   inet     254.0.0.254         --> 0/0
                                   inet6    fe80::199
dsc                     up    up
em0                     up    up
em0.0                   up    up   inet     10.0.0.1/8
                                            10.0.0.4/8
        """

    def tearDown(self):
        """teardown after all case"""
        pass

    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_get_ioc_slot_number(self, mock_execute_cli_command_on_device):
        """UT case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        print("Normal testing")
        mock_execute_cli_command_on_device.return_value = self.response["SA_HE_SHOW_INTERFACE"]
        result = self.ins.get_ioc_slot_number(device=mock_device_ins)
        self.assertTrue(result == [1, 2])

        print("Get IOC number from cache")
        result = self.ins.get_ioc_slot_number(device=mock_device_ins)
        self.assertTrue(result == [1, 2])

        print("Force get IOC number by except_slot_number")
        result = self.ins.get_ioc_slot_number(device=mock_device_ins, except_slot_number=1)
        self.assertTrue(result == [2, ])

        print("Force get IOC number if except_slot_number set")
        result = self.ins.get_ioc_slot_number(device=mock_device_ins, except_slot_number=[0, 2])
        self.assertTrue(result == [1, ])

        print("Change largest_slot_number")
        result = self.ins.get_ioc_slot_number(device=mock_device_ins, largest_slot_number=10, force_get="True")
        self.assertTrue(result == [1, 2, 7])

    @mock.patch.object(chassis, "waiting_for_pic_online")
    @mock.patch.object(dev, "reboot_device")
    @mock.patch.object(dev, "execute_config_command_on_device")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    @mock.patch("time.sleep")
    def test_set_services_offload(
        self,
        mock_sleep,
        mock_execute_cli_command_on_device,
        mock_execute_config_command_on_device,
        mock_reboot_device,
        mock_waiting_for_pic_online,
    ):
        """UT case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_sleep.return_value = None

        print("Normal testing")
        mock_execute_cli_command_on_device.return_value = True
        mock_execute_config_command_on_device.return_value = True
        status = self.ins.set_services_offload(device=mock_device_ins, ioc_slot_number="1")
        self.assertTrue(status)

        print("Normal testing with reboot")
        mock_execute_cli_command_on_device.return_value = True
        mock_reboot_device.return_value = True
        mock_device_ins.is_ha.return_value = True
        status = self.ins.set_services_offload(device=mock_device_ins, ioc_slot_number=["1", 2], reboot_mode="reboot", waiting_for_pic_online=False)
        self.assertTrue(status)

        print("Normal testing with waiting_for_pic_online")
        mock_execute_cli_command_on_device.return_value = True
        mock_reboot_device.return_value = True
        mock_device_ins.is_ha.return_value = False
        mock_waiting_for_pic_online.return_value = True

        status = self.ins.set_services_offload(device=mock_device_ins, ioc_slot_number=["1", 2], reboot_mode="reboot", waiting_for_pic_online=False)
        self.assertTrue(status)

        mock_execute_cli_command_on_device.return_value = True
        status = self.ins.set_services_offload(device=mock_device_ins, ioc_slot_number=3, reboot_mode="immediately", waiting_for_pic_online=True)
        self.assertTrue(status)

        print("Invalid test")
        self.assertRaisesRegex(
            ValueError,
            r"option 'action' must be enable or disable",
            self.ins.set_services_offload,
            device=mock_device_ins, ioc_slot_number=1, action="Unknown"
        )

        self.assertRaisesRegex(
            ValueError,
            r"option 'reboot_mode' must be 'none', 'reboot', 'gracefully'",
            self.ins.set_services_offload,
            device=mock_device_ins, ioc_slot_number=1, reboot_mode="Unknown"
        )
