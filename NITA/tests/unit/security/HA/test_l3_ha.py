# coding: UTF-8
"""All unit test cases for L3 HA module"""
__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2019'
# pylint: disable=attribute-defined-outside-init,invalid-name

import os
import unittest2 as unittest
import mock

from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.security.issu.issu import issu
from jnpr.toby.security.chassis.chassis import chassis
from jnpr.toby.security.HA.l3_ha import l3_ha


class TestL3HA(unittest.TestCase):
    """TEST L3 HA CLASS"""
    def setUp(self):
        """INIT"""
        self.tool = flow_common_tool()
        self.ins = l3_ha()
        self.ins.default["regression_image_folder"] = "/var/home/regress/Regression_image"
        self.ins.default["higher_image_folder"] = "/var/home/regress/HIGHER_image"

        self.r0 = mock.Mock(spec=SrxSystem)
        self.r0.log = mock.Mock()
        self.r0.get_host_name.return_value = "vsrx_device_0"

        self.r1 = mock.Mock(spec=SrxSystem)
        self.r1.log = mock.Mock()
        self.r1.get_host_name.return_value = "vsrx_device_1"

        self.response = {}

        self.regression_image_filename = "junos-install-vsrx3-x86-64-19.4I-20190918_dev_common.0.0857.tgz"
        self.higher_image_filename = "junos-install-vsrx3-x86-64-19.4I-20190919_dev_common.0.1213.tgz"
        self.response["IMAGES"] = {
            "higher_image": os.path.join(self.ins.default["higher_image_folder"], self.higher_image_filename),
            "higher_image_filename": self.higher_image_filename,
            "regression_image": os.path.join(self.ins.default["regression_image_folder"], self.regression_image_filename),
            "regression_image_filename": self.regression_image_filename,
        }

    @mock.patch.object(issu, "_search_image_on_both_node")
    def test_get_image(self, mock_search_image_on_both_node):
        """UNIT TEST"""

        print("Normal testing")
        mock_search_image_on_both_node.side_effect = [self.regression_image_filename, self.higher_image_filename]
        images = self.ins.get_image(device=self.r0)
        self.assertEqual(images, self.response["IMAGES"])

        print("force get")
        self.ins.runtime["get_image"]["vsrx_device_0"] = self.response["IMAGES"]
        images = self.ins.get_image(device=self.r0)
        self.assertEqual(images, self.response["IMAGES"])



    @mock.patch("jnpr.toby.security.HA.l3_ha.run_multiple")
    @mock.patch.object(chassis, "waiting_for_pic_online")
    @mock.patch.object(l3_ha, "get_image")
    def test_l3_ha_upgrade_init(self, mock_get_image, mock_waiting_for_pic_online, mock_run_multiple):
        """UNIT TEST"""
        mock_get_image.side_effect = (self.response["IMAGES"], self.response["IMAGES"])
        mock_waiting_for_pic_online.side_effect = (True, True)

        print("basic checking for device version same as Regression_image")
        self.r0.get_version_info.return_value = {"version": "19.4I-20190918_dev_common.0.0857",}
        self.r1.get_version_info.return_value = {"version": "19.4I-20190918_dev_common.0.0857",}
        result = self.ins.l3_ha_upgrade_init(
            device_1=self.r0,
            device_2=self.r1,
            check_count="60",
            check_interval=60,
            no_validate=False,
            no_copy=False,
        )
        self.assertTrue(result)

        print("only 1 device need to downgrade")
        mock_get_image.side_effect = (self.response["IMAGES"], self.response["IMAGES"])

        self.r0.get_version_info.side_effect = (
            {"version": "19.4I-20190918_dev_common.0.0857",},
            {"version": "19.4I-20190918_dev_common.0.0857",},
        )
        self.r1.get_version_info.side_effect = (
            {"version": "19.4I-20190919_dev_common.0.1213",},
            {"version": "19.4I-20190918_dev_common.0.0857",},
        )

        self.r0.software_install.return_value = True
        self.r1.software_install.return_value = True

        mock_run_multiple.side_effect = (None, None)

        result = self.ins.l3_ha_upgrade_init(device_1=self.r0, device_2=self.r1)
        self.assertTrue(result)

        print("negetivation test 1")
        mock_get_image.side_effect = (False, self.response["IMAGES"])
        self.assertRaisesRegex(
            RuntimeError,
            r"No proper image found",
            self.ins.l3_ha_upgrade_init,
            device_1=self.r0, device_2=self.r1,
        )

        print("negetivation test 2")
        mock_get_image.side_effect = (self.response["IMAGES"], {
            "higher_image": "aa",
            "higher_image_filename": "aa",
            "regression_image": "aa",
            "regression_image_filename": "aa"
        })
        self.assertRaisesRegex(
            RuntimeError,
            r"regression image filename are different between device_1 and device_2",
            self.ins.l3_ha_upgrade_init,
            device_1=self.r0, device_2=self.r1,
        )

        # print("negetivation test 3")
        # mock_get_image.side_effect = (self.response["IMAGES"], self.response["IMAGES"]])
        # self.r0.get_version_info.side_effect = (
        #     False,
        #     {"version": "19.4I-20190918_dev_common.0.0857",},
        # )
        # self.assertRaisesRegex(
        #     RuntimeError,
        #     r"Get device version info from .* failed",
        #     self.ins.l3_ha_upgrade_init,
        #     device_1=self.r0, device_2=self.r1,
        # )
