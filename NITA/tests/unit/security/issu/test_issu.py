# coding: UTF-8
"""All unit test cases for ISSU module"""
# pylint: disable=attribute-defined-outside-init,invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import time
import os
from unittest import TestCase, mock

from jnpr.toby.exception.toby_exception import TobyPromptTimeoutException
from jnpr.toby.hldcl import device as dev
from jnpr.toby.hldcl.juniper.security import robot_keyword
from jnpr.toby.hldcl.juniper.security.srxsystem import SrxSystem
from jnpr.toby.utils.linux.linux_tool import linux_tool
from jnpr.toby.utils.setup_server import setup_server
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.security.issu.issu import issu
from jnpr.toby.security.issu.srx_manual_issu import srx_manual_issu
from jnpr.toby.security.chassis.chassis import chassis
from jnpr.toby.security.HA.HA import HA


class TestIssu(TestCase):
    """Unitest cases for ISSU module"""
    def setUp(self):
        """setup before all cases"""
        self.ins = issu()
        self.srv = setup_server()
        self.chassis = chassis()
        self.tool = flow_common_tool()

        self.response = {}
        self.response["1_IMAGE_IN_FOLDER"] = """
        total 1282816
        -rw-r--r--  1 regress  20  656610462 May  8 08:25 junos-srx5000-17.3-20170430_dev_common.1.tgz
        """

        self.response["MULTI_IMAGE_IN_FOLDER"] = """
        total 1282816
        -rw-r--r--  1 regress  20  656610462 May  8 08:25 junos-srx5000-17.3-20170430_dev_common.1.tgz
        -rw-r--r--  1 regress  20  656610462 May  8 08:25 junos-srx5000-17.3-20170501_dev_common.1.tgz
        """

        self.response["NO_IMAGE_IN_FOLDER"] = """
        total 1282816
        """

    def tearDown(self):
        """tear down"""
        pass

    @mock.patch("os.getenv")
    @mock.patch("os.path.isfile")
    @mock.patch("jnpr.toby.security.issu.issu.run_multiple")
    @mock.patch.object(issu, "_search_image_on_both_node")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_jt_behavior(self, mock_execute_shell_command_on_device, mock_search_image_on_both_node, mock_run_multiple, mock_isfile, mock_getenv):
        """UT CASE"""
        mock_device_ins = mock.Mock()

        lower_image_filename = "lower_image.tgz"
        lower_image_base_dir = "/var/home/regress/LOWER_image"
        lower_image_fullpath = os.path.join(lower_image_base_dir, lower_image_filename)

        regression_image_filename = "regression_image.tgz"
        regression_image_base_dir = "/var/home/regress/Regression_image"
        regression_image_fullpath = os.path.join(regression_image_base_dir, regression_image_filename)

        higher_image_filename = "higher_image.tgz"
        higher_image_base_dir = "/var/home/regress/HIGHER_image"
        higher_image_fullpath = os.path.join(higher_image_base_dir, higher_image_filename)

        src_image_filename = "src_image.tgz"
        src_image_base_dir = regression_image_base_dir
        src_image_fullpath = os.path.join(src_image_base_dir, src_image_filename)

        dst_image_filename = "dst_image.tgz"
        dst_image_base_dir = higher_image_base_dir
        dst_image_fullpath = os.path.join(dst_image_base_dir, dst_image_filename)

        lower_image_path_in_shell_server = "/volumn/lower_image.tgz"
        regression_image_path_in_shell_server = "/volumn/regression_image.tgz"
        higher_image_path_in_shell_server = "/volumn/higher_image.tgz"

        # compatible testing that no new JT behavior
        mock_getenv.side_effect = [
            lower_image_base_dir, regression_image_base_dir, higher_image_base_dir,
            None, None, None,
            "", # TOBY_ISSU_TO
        ]
        mock_search_image_on_both_node.side_effect = [lower_image_filename, regression_image_filename, higher_image_filename, src_image_filename, dst_image_filename]
        image = self.ins._jt_behavior(device=mock_device_ins, upload_image=False)
        print("compatible testing that no new JT behavior result:\n{}".format(self.tool.pprint(image)))
        self.assertEqual(image["lower_image_base_dir"], lower_image_base_dir)
        self.assertEqual(image["lower_image_filename"], lower_image_filename)
        self.assertEqual(image["lower_image_fullpath"], lower_image_fullpath)
        self.assertEqual(image["lower_image_path_in_shell_server"], None)
        self.assertEqual(image["regression_image_base_dir"], regression_image_base_dir)
        self.assertEqual(image["regression_image_filename"], regression_image_filename)
        self.assertEqual(image["regression_image_fullpath"], regression_image_fullpath)
        self.assertEqual(image["regression_image_path_in_shell_server"], None)
        self.assertEqual(image["higher_image_base_dir"], higher_image_base_dir)
        self.assertEqual(image["higher_image_filename"], higher_image_filename)
        self.assertEqual(image["higher_image_fullpath"], higher_image_fullpath)
        self.assertEqual(image["higher_image_path_in_shell_server"], None)
        self.assertEqual(image["src_image_base_dir"], src_image_base_dir)
        self.assertEqual(image["src_image_filename"], src_image_filename)
        self.assertEqual(image["src_image_fullpath"], src_image_fullpath)
        self.assertEqual(image["src_image_path_in_shell_server"], None)
        self.assertEqual(image["dst_image_base_dir"], dst_image_base_dir)
        self.assertEqual(image["dst_image_filename"], dst_image_filename)
        self.assertEqual(image["dst_image_fullpath"], dst_image_fullpath)
        self.assertEqual(image["dst_image_path_in_shell_server"], None)

        # Testing for JT behavior
        mock_getenv.side_effect = [
            lower_image_base_dir, regression_image_base_dir, higher_image_base_dir,
            lower_image_path_in_shell_server, regression_image_path_in_shell_server, higher_image_path_in_shell_server,
            "", # TOBY_ISSU_TO
        ]
        mock_isfile.side_effect = [True, True]
        mock_execute_shell_command_on_device.side_effect = [
            """
            total 2292224
            -rw-r--r--  1 regress  20  1173282565 Mar 14 09:52 new_src_image.tgz
            """,
            """""", # rm image file in src_image_dir
            """
            total 2505600
            -rw-r--r--  1 regress  20  1282495659 Mar 14 09:57 new_dst_image.tgz
            """,
            """""", # rm image file in dst_image_dir
        ]
        mock_run_multiple.return_value = ["", ""]
        mock_search_image_on_both_node.side_effect = [
            # first search_image invoke
            lower_image_filename, regression_image_filename, higher_image_filename, src_image_filename, dst_image_filename,
            # second search_image_invoke
            "new_src_image.tgz", "new_dst_image.tgz",
        ]

        image = self.ins._jt_behavior(device=mock_device_ins)
        print("Testing for JT behavior:\n{}".format(self.tool.pprint(image)))

        self.assertEqual(image["src_image_base_dir"], regression_image_base_dir)
        self.assertEqual(image["src_image_filename"], "new_src_image.tgz")
        self.assertEqual(image["src_image_fullpath"], os.path.join(regression_image_base_dir, "new_src_image.tgz" ))
        self.assertEqual(image["src_image_path_in_shell_server"], regression_image_path_in_shell_server)
        self.assertEqual(image["dst_image_base_dir"], higher_image_base_dir)
        self.assertEqual(image["dst_image_filename"], "new_dst_image.tgz")
        self.assertEqual(image["dst_image_fullpath"], os.path.join(higher_image_base_dir, "new_dst_image.tgz"))
        self.assertEqual(image["dst_image_path_in_shell_server"], higher_image_path_in_shell_server)

        # Get image from previous result
        self.ins.image["src_image_fullpath"] = lower_image_fullpath
        self.ins.image["dst_image_fullpath"] = regression_image_fullpath
        image = self.ins._jt_behavior(device=mock_device_ins, upload_image=False)
        self.assertEqual(image["src_image_fullpath"], lower_image_fullpath)
        self.assertEqual(image["dst_image_fullpath"], regression_image_fullpath)

        # Have TOBY_ISSU_TO environment variable and image already exists
        mock_getenv.side_effect = [
            lower_image_base_dir, regression_image_base_dir, higher_image_base_dir,
            lower_image_path_in_shell_server, regression_image_path_in_shell_server, higher_image_path_in_shell_server,
            "regression", # TOBY_ISSU_TO
        ]

        mock_search_image_on_both_node.side_effect = [
            # first search_image invoke
            lower_image_filename, regression_image_filename, higher_image_filename, src_image_filename, dst_image_filename,
            # second search_image_invoke
            lower_image_filename, regression_image_filename,
        ]

        mock_isfile.side_effect = [True, True]
        mock_execute_shell_command_on_device.side_effect = [
            """
            total 2292224
            -rw-r--r--  1 regress  20  1173282565 Mar 14 09:52 {}
            """.format(lower_image_filename),
            """""", # rm image file in src_image_dir
            """
            total 2505600
            -rw-r--r--  1 regress  20  1282495659 Mar 14 09:57 {}
            """.format(regression_image_filename),
            """""", # rm image file in dst_image_dir
        ]

        image = self.ins._jt_behavior(device=mock_device_ins)
        print("Have TOBY_ISSU_TO environment variable:\n{}".format(self.tool.pprint(image)))
        self.assertEqual(image["src_image_base_dir"], lower_image_base_dir)
        self.assertEqual(image["src_image_filename"], lower_image_filename)
        self.assertEqual(image["src_image_fullpath"], lower_image_fullpath)
        self.assertEqual(image["src_image_path_in_shell_server"], lower_image_path_in_shell_server)
        self.assertEqual(image["dst_image_base_dir"], regression_image_base_dir)
        self.assertEqual(image["dst_image_path_in_shell_server"], regression_image_path_in_shell_server)

        # if given image is not on shell server
        mock_getenv.side_effect = [
            lower_image_base_dir, regression_image_base_dir, higher_image_base_dir,
            lower_image_path_in_shell_server, regression_image_path_in_shell_server, higher_image_path_in_shell_server,
            "regression", # TOBY_ISSU_TO
        ]

        mock_execute_shell_command_on_device.side_effect = [
            """
            total 2292224
            -rw-r--r--  1 regress  20  1173282565 Mar 14 09:52 {}
            """.format(lower_image_filename),
            """""", # rm image file in src_image_dir
            """
            total 2505600
            -rw-r--r--  1 regress  20  1282495659 Mar 14 09:57 {}
            """.format(regression_image_filename),
            """""", # rm image file in dst_image_dir
        ]

        mock_search_image_on_both_node.side_effect = [
            # first search_image invoke
            lower_image_filename, regression_image_filename, higher_image_filename, src_image_filename, dst_image_filename,
            # second search_image_invoke
            lower_image_filename, regression_image_filename,
        ]

        mock_isfile.side_effect = [True, False]
        self.assertRaisesRegex(
            RuntimeError,
            r"No local image file found",
            self.ins._jt_behavior,
            device=mock_device_ins
        )

        print("upload image from shell server then update image path")
        mock_getenv.side_effect = [
            lower_image_base_dir, regression_image_base_dir, higher_image_base_dir,
            lower_image_path_in_shell_server, regression_image_path_in_shell_server, higher_image_path_in_shell_server,
            "regression", # TOBY_ISSU_TO
        ]
        mock_search_image_on_both_node.side_effect = [
            # first search_image invoke
            lower_image_filename, regression_image_filename, higher_image_filename, src_image_filename, dst_image_filename,
            # second search_image_invoke
            os.path.basename(lower_image_path_in_shell_server), os.path.basename(regression_image_path_in_shell_server),
        ]
        mock_isfile.side_effect = [True, True]
        mock_execute_shell_command_on_device.side_effect = [
            """
            total 2292224
            -rw-r--r--  1 regress  20  1173282565 Mar 14 09:52 {}
            """.format(lower_image_filename),
            """""", # rm image file in src_image_dir
            """
            total 2505600
            -rw-r--r--  1 regress  20  1282495659 Mar 14 09:57 {}
            """.format(regression_image_filename),
            """""", # rm image file in dst_image_dir
        ]
        image = self.ins._jt_behavior(device=mock_device_ins, upload_image=True, delete_exist_file_before_upolad=True)
        print(self.tool.pprint(image))
        self.assertEqual(image["lower_image_base_dir"], lower_image_base_dir)
        self.assertEqual(image["lower_image_filename"], lower_image_filename)
        self.assertEqual(image["lower_image_fullpath"], lower_image_fullpath)
        self.assertEqual(image["lower_image_path_in_shell_server"], lower_image_path_in_shell_server)
        self.assertEqual(image["regression_image_base_dir"], regression_image_base_dir)
        self.assertEqual(image["regression_image_filename"], regression_image_filename)
        self.assertEqual(image["regression_image_fullpath"], regression_image_fullpath)
        self.assertEqual(image["regression_image_path_in_shell_server"], regression_image_path_in_shell_server)
        self.assertEqual(image["higher_image_base_dir"], higher_image_base_dir)
        self.assertEqual(image["higher_image_filename"], higher_image_filename)
        self.assertEqual(image["higher_image_fullpath"], higher_image_fullpath)
        self.assertEqual(image["higher_image_path_in_shell_server"], higher_image_path_in_shell_server)
        self.assertEqual(image["src_image_base_dir"], lower_image_base_dir)
        self.assertEqual(image["src_image_filename"], os.path.basename(lower_image_path_in_shell_server))
        self.assertEqual(image["src_image_fullpath"], os.path.join(lower_image_base_dir, os.path.basename(lower_image_path_in_shell_server)))
        self.assertEqual(image["dst_image_base_dir"], regression_image_base_dir)
        self.assertEqual(image["dst_image_filename"], os.path.basename(regression_image_path_in_shell_server))
        self.assertEqual(image["dst_image_fullpath"], os.path.join(regression_image_base_dir, os.path.basename(regression_image_path_in_shell_server)))




    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_search_issu_image_path(self, mock_execute_shell_command_on_device):
        """test_analyse_all_text_flow_session"""
        # mock needed instance
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        # verify 1 image in right path
        mock_execute_shell_command_on_device.side_effect = [self.response["1_IMAGE_IN_FOLDER"], self.response["1_IMAGE_IN_FOLDER"]]
        response = self.ins.search_issu_image_path(device=mock_device_ins)
        self.assertTrue(isinstance(response, dict))

        # Get image path from previous result
        response = self.ins.search_issu_image_path(device=mock_device_ins)
        self.assertTrue(isinstance(response, dict))

        # no image in higher path
        mock_execute_shell_command_on_device.side_effect = [self.response["1_IMAGE_IN_FOLDER"], self.response["NO_IMAGE_IN_FOLDER"]]
        self.ins.image_path["regression_image"] = None
        self.ins.image_path["higher_image"] = None
        response = self.ins.search_issu_image_path(device=mock_device_ins)
        self.assertFalse(response)

        # 2 images in specific path
        mock_execute_shell_command_on_device.side_effect = [self.response["MULTI_IMAGE_IN_FOLDER"], self.response["MULTI_IMAGE_IN_FOLDER"]]
        self.ins.image_path["regression_image"] = None
        self.ins.image_path["higher_image"] = None
        response = self.ins.search_issu_image_path(device=mock_device_ins)
        self.assertFalse(response)


    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_search_image_on_both_node(self, mock_execute_shell_command_on_device):
        """UT CASE"""
        # mock needed instance
        mock_device_ins = mock.Mock()
        mock_device_ins.log.return_value = None

        # verify 1 image in right path
        mock_execute_shell_command_on_device.side_effect = [self.response["1_IMAGE_IN_FOLDER"], self.response["1_IMAGE_IN_FOLDER"]]
        response = self.ins._search_image_on_both_node(device=mock_device_ins, folder="/folder")
        self.assertEqual(response, "junos-srx5000-17.3-20170430_dev_common.1.tgz")

        # no image
        mock_execute_shell_command_on_device.side_effect = [self.response["NO_IMAGE_IN_FOLDER"], self.response["NO_IMAGE_IN_FOLDER"]]
        response = self.ins._search_image_on_both_node(device=mock_device_ins, folder="/folder")
        self.assertEqual(response, None)

        # 2 images in specific path
        mock_execute_shell_command_on_device.side_effect = [self.response["MULTI_IMAGE_IN_FOLDER"], self.response["MULTI_IMAGE_IN_FOLDER"]]
        response = self.ins._search_image_on_both_node(device=mock_device_ins, folder="/folder", raise_if_contain_multi_image=False)
        self.assertEqual(response, ["junos-srx5000-17.3-20170430_dev_common.1.tgz", "junos-srx5000-17.3-20170501_dev_common.1.tgz"])

        # raise if got multiple images
        mock_execute_shell_command_on_device.side_effect = [self.response["MULTI_IMAGE_IN_FOLDER"], self.response["MULTI_IMAGE_IN_FOLDER"]]
        self.assertRaisesRegex(
            RuntimeError,
            r"""contain 1\+ images""",
            self.ins._search_image_on_both_node,
            device=mock_device_ins, folder="/folder", raise_if_contain_multi_image=True,
        )

        # different image on 2 nodes
        mock_execute_shell_command_on_device.side_effect = [self.response["1_IMAGE_IN_FOLDER"], self.response["NO_IMAGE_IN_FOLDER"]]
        self.assertRaisesRegex(
            RuntimeError,
            r"""2 nodes have different image or no image in specific node""",
            self.ins._search_image_on_both_node,
            device=mock_device_ins, folder="/folder",
        )



    @mock.patch("jnpr.toby.hldcl.juniper.security.robot_keyword.check_vmhost")
    @mock.patch("jnpr.toby.security.issu.issu.run_multiple")
    @mock.patch.object(chassis, "waiting_for_pic_online")
    @mock.patch.object(issu, "software_install")
    @mock.patch.object(issu, "_jt_behavior")
    @mock.patch.object(issu, "_search_image_on_both_node")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    def test_issu_init(self,
            mock_execute_shell_command_on_device,
            mock_execute_cli_command_on_device,
            mock_search_image_on_both_node,
            mock_jt_behavior,
            mock_software_install,
            mock_waiting_for_pic_online,
            mock_run_multiple,
            mock_check_vmhost,
        ):
        """test issu init"""
        self.ins.image = {}
        self.ins.image["lower_image_base_dir"] = "/var/home/regress/LOWER_image"
        self.ins.image["lower_image_filename"] = "junos-srx5000-17.2-20170430_dev_common.1.tgz"
        self.ins.image["lower_image_fullpath"] = os.path.join(self.ins.image["lower_image_base_dir"], self.ins.image["lower_image_filename"])
        self.ins.image["regression_image_base_dir"] = "/var/home/regress/Regression_image"
        self.ins.image["regression_image_filename"] = "junos-srx5000-18.2-20170430_dev_common.1.tgz"
        self.ins.image["regression_image_fullpath"] = os.path.join(self.ins.image["regression_image_base_dir"], self.ins.image["regression_image_filename"])
        self.ins.image["higher_image_base_dir"] = "/var/home/regress/HIGHER_image"
        self.ins.image["higher_image_filename"] = "junos-srx5000-19.2-20170430_dev_common.1.tgz"
        self.ins.image["higher_image_fullpath"] = os.path.join(self.ins.image["higher_image_base_dir"], self.ins.image["higher_image_filename"])
        self.ins.image["src_image_base_dir"] = self.ins.image["regression_image_base_dir"]
        self.ins.image["src_image_filename"] = self.ins.image["regression_image_filename"]
        self.ins.image["src_image_fullpath"] = self.ins.image["regression_image_fullpath"]
        self.ins.image["dst_image_base_dir"] = self.ins.image["higher_image_base_dir"]
        self.ins.image["dst_image_filename"] = self.ins.image["higher_image_filename"]
        self.ins.image["dst_image_fullpath"] = self.ins.image["higher_image_fullpath"]

        lower_version = "17.2-20170430_dev_common.1"
        regression_version = "18.2-20170430_dev_common.1"
        higher_version = "19.2-20170430_dev_common.1"

        # mock needed methods
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_check_vmhost.return_value = "system"
        mock_jt_behavior.return_value = self.ins.image

        # do not need upgrade before issu
        mock_execute_cli_command_on_device.side_effect = ["", ""]
        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]
        mock_device_ins.get_version_info.side_effect = [
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": higher_version,},
            },
            {
                "node0":        {"version": regression_version,},
                "node1":        {"version": regression_version,},
            },
        ]
        mock_software_install.side_effect = [True, True]
        mock_waiting_for_pic_online.return_value = True
        response = self.ins.issu_init(device=mock_device_ins)
        self.assertTrue(response)

        # cannot get version info from device
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]

        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]

        mock_device_ins.get_version_info.side_effect = [False, False]
        self.assertRaisesRegex(
            RuntimeError,
            r"Get device version failed",
            self.ins.issu_init,
            device=mock_device_ins,
        )

        # need upgrade 1 or 2 node
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]
        mock_device_ins.get_version_info.side_effect = [
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": higher_version,},
            },
            {
                "node0":        {"version": regression_version,},
                "node1":        {"version": regression_version,},
            },
        ]
        mock_run_multiple.return_value = True
        mock_waiting_for_pic_online.return_value = True
        response = self.ins.issu_init(device=mock_device_ins)
        self.assertTrue(response)

        # after software installed, PIC not online in long time
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]
        mock_device_ins.get_version_info.side_effect = [
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": higher_version,},
            },
            {
                "node0":        {"version": regression_version,},
                "node1":        {"version": regression_version,},
            },
        ]
        mock_run_multiple.return_value = True
        mock_waiting_for_pic_online.return_value = False
        self.assertRaisesRegex(
            RuntimeError,
            r"FPC online check failed",
            self.ins.issu_init,
            device=mock_device_ins,
        )

        # cannot get new version info after software installed
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]
        mock_device_ins.get_version_info.side_effect = [
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": higher_version,},
            },
            False,
        ]
        mock_run_multiple.return_value = True
        mock_waiting_for_pic_online.return_value = True
        self.assertRaisesRegex(
            RuntimeError,
            r"get device version failed",
            self.ins.issu_init,
            device=mock_device_ins,
        )

        # node0 and node1 have different version after software installed
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]
        mock_device_ins.get_version_info.side_effect = [
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": higher_version,},
            },
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": regression_version,},
            },
        ]
        mock_run_multiple.return_value = True
        mock_waiting_for_pic_online.return_value = True
        self.assertRaisesRegex(
            RuntimeError,
            r"2 nodes have different version",
            self.ins.issu_init,
            device=mock_device_ins,
        )

        # after software installed, node version still different as regression_image
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]
        mock_device_ins.get_version_info.side_effect = [
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": higher_version,},
            },
            {
                "node0":        {"version": higher_version,},
                "node1":        {"version": higher_version,},
            },
        ]
        mock_run_multiple.return_value = True
        mock_waiting_for_pic_online.return_value = True
        self.assertRaisesRegex(
            RuntimeError,
            r"different as regression_image",
            self.ins.issu_init,
            device=mock_device_ins,
        )

        # 2 nodes already have needed version
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_search_image_on_both_node.side_effect = [
            self.ins.image["src_image_filename"],
            self.ins.image["dst_image_filename"],
        ]
        mock_device_ins.get_version_info.side_effect = [
            {
                "node0":        {"version": regression_version,},
                "node1":        {"version": regression_version,},
            },
            {
                "node0":        {"version": regression_version,},
                "node1":        {"version": regression_version,},
            },
        ]
        response = self.ins.issu_init(device=mock_device_ins)
        self.assertTrue(response)

    def test_compare_version_string(self):
        """UT CASE"""
        result = self.ins.compare_version_string(
            junos_version_string="17.4-20170430_dev_common.1",
            image_filename_string="junos-srx5000-17.3-20170430_dev_common.1.tgz",
        )
        self.assertFalse(result)

        result = self.ins.compare_version_string(
            junos_version_string="17.3-20170430_dev_common.1",
            image_filename_string="junos-srx5000-17.3-20170430_dev_common.1.tgz",
        )
        self.assertTrue(result)

        result = self.ins.compare_version_string(
            junos_version_string="17.3-2017-04-30_dev_common.1",
            image_filename_string="junos-srx5000-17.3-20170430_dev_common.1.tgz",
        )
        self.assertTrue(result)

    @mock.patch("jnpr.toby.hldcl.juniper.security.robot_keyword.check_vmhost")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_software_install(self, mock_execute_cli_command_on_device, mock_check_vmhost):
        """UT CASE"""
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.current_node.current_controller = mock.Mock()
        mock_device_ins.log.return_value = None

        # normal test
        mock_device_ins.get_vmhost_infra.return_value = False
        mock_device_ins.reboot.return_value = True
        mock_execute_cli_command_on_device.return_value = True
        result = self.ins.software_install(device=mock_device_ins, package=None)
        self.assertTrue(result)

        # no-reboot for vmhost platform
        mock_check_vmhost.return_value = "vmhost"
        mock_device_ins.get_vmhost_infra.return_value = True
        mock_device_ins.reboot.return_value = True
        mock_execute_cli_command_on_device.return_value = True
        result = self.ins.software_install(device=mock_device_ins, package=None)
        self.assertTrue(result)

        # reboot failed after software install
        mock_device_ins.get_vmhost_infra.return_value = False
        mock_device_ins.reboot.return_value = False
        mock_execute_cli_command_on_device.return_value = True
        result = self.ins.software_install(device=mock_device_ins, package=None)
        self.assertFalse(result)

    @mock.patch.object(issu, "issu_init")
    def test_issu_close(self, mock_issu_init):
        """test issu init"""
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.current_node.current_controller = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.get_host_name.return_value = "dev1"

        # do issu close
        mock_issu_init.return_value = True
        response = self.ins.issu_close(device=mock_device_ins)
        self.assertTrue(response)

    @mock.patch("jnpr.toby.hldcl.juniper.security.robot_keyword.check_vmhost")
    @mock.patch("time.sleep")
    @mock.patch.object(HA, "get_ha_healthy_status")
    @mock.patch.object(HA, "get_ha_rgs")
    @mock.patch.object(chassis, "waiting_for_pic_online")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    def test_do_issu(self,
        mock_execute_cli_command_on_device,
        mock_waiting_for_pic_online,
        mock_get_ha_rgs,
        mock_get_ha_healthy_status,
        mock_sleep,
        mock_check_vmhost,
    ):
        """UT case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.current_node.current_controller = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True
        mock_check_vmhost.return_value = "vmhost"

        # normal function
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_get_ha_rgs.return_value = ["0", "1"]
        mock_get_ha_healthy_status.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = True
        result = self.ins.do_issu(device=mock_device_ins, package=None, more_options="no-copy", system="vmhost")
        self.assertTrue(result)

        # cannot get rgs info
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_get_ha_rgs.return_value = False
        mock_get_ha_healthy_status.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = True
        mock_check_vmhost.return_value = "system"
        result = self.ins.do_issu(device=mock_device_ins, package=None, no_copy=True)
        self.assertFalse(result)

        # HA rgs status is not healthy before issu
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_get_ha_rgs.return_value = ["0", "1"]
        mock_get_ha_healthy_status.return_value = False
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = True
        result = self.ins.do_issu(device=mock_device_ins, package=None)
        self.assertFalse(result)

        # reconnect device failed after issu
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_get_ha_rgs.return_value = ["0", "1"]
        mock_get_ha_healthy_status.return_value = True
        mock_device_ins.reconnect.return_value = False
        mock_waiting_for_pic_online.return_value = True
        result = self.ins.do_issu(device=mock_device_ins, package=None)
        self.assertFalse(result)

        # PIC not online after issu
        mock_device_ins.switch_to_primary_node.return_value = True
        mock_execute_cli_command_on_device.side_effect = [True, True]
        mock_get_ha_rgs.return_value = ["0", "1"]
        mock_get_ha_healthy_status.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = False
        result = self.ins.do_issu(device=mock_device_ins, package=None)
        self.assertFalse(result)



    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    @mock.patch.object(linux_tool, "create_ftp_connection_between_host")
    @mock.patch.object(linux_tool, "close_ftp_connection_between_host")
    @mock.patch.object(setup_server, "start_ftp_service")
    def test_start_and_check_ftp_connection_during_issu(self,
        mock_start_ftp_service,
        mock_create_ftp_connection_between_host,
        mock_close_ftp_connection_between_host,
        mock_execute_shell_command_on_device,
        mock_sleep
    ):
        """UT case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.current_node.current_controller = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True

        # normal checking
        mock_start_ftp_service.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """[root@fnd-lnx34 ~]# dd if=/dev/zero of=/home/regress/ftp_download_file bs=209715200 count=1
1+0 records in
1+0 records out
209715200 bytes (10 MB) copied, 0.888294 s, 70.8 MB/s
            """,
            """-rw-------. 1 root root 71508 Dec 16 16:02 ftp_download_file""",
            """-rw-------. 1 root root 81508 Dec 16 16:02 ftp_download_file""",
            """-rw-------. 1 root root 91508 Dec 16 16:02 ftp_download_file""",
            """-rw-------. 1 root root 101508 Dec 16 16:02 ftp_download_file""",
            """-rw-------. 1 root root 111508 Dec 16 16:02 ftp_download_file""",
            True,
            True,
        )
        mock_create_ftp_connection_between_host.return_value = True
        mock_close_ftp_connection_between_host.return_value = True

        device_handlers = {
            "ha_device_handler":        mock_device_ins,
            "node0_handler":            mock_device_ins,
            "node1_handler":            mock_device_ins,
            "ftp_server_handler":       mock_device_ins,
            "ftp_client_handler":       mock_device_ins,
        }
        ftp_topo_options = {
            "ftp_server_ipaddr":        "192.168.100.2",
        }
        ftp_checking_options = {
            "check_counter":            5,
            "sleep_time":               10,
        }

        result = self.ins.start_and_check_ftp_connection_during_issu(
            device_handlers=device_handlers,
            ftp_topo_options=ftp_topo_options,
            ftp_checking_options=ftp_checking_options,
        )
        self.assertTrue(result)

        # FTP support IPv6
        mock_start_ftp_service.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """[root@fnd-lnx34 ~]# dd if=/dev/zero of=/home/regress/ftp_download_file bs=209715200 count=1
1+0 records in
1+0 records out
209715200 bytes (10 MB) copied, 0.888294 s, 70.8 MB/s
            """,
            "-rw-------. 1 root root 11508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 21508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 31508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 41508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 51508 Dec 16 16:02 ftp_download_file",
            True,
            True,
        )
        mock_create_ftp_connection_between_host.return_value = True

        ftp_topo_options = {
            "ftp_server_ipaddr":        "2000:20::2",
        }
        ftp_checking_options = {
            "check_counter":            5,
            "sleep_time":               10,
        }

        result = self.ins.start_and_check_ftp_connection_during_issu(
            device_handlers=device_handlers,
            ftp_topo_options=ftp_topo_options,
            ftp_checking_options=ftp_checking_options,
        )
        self.assertTrue(result)

        # Create FTP server failed
        mock_start_ftp_service.return_value = False

        case = False
        try:
            self.ins.start_and_check_ftp_connection_during_issu(
                device_handlers=device_handlers,
                ftp_topo_options=ftp_topo_options,
                ftp_checking_options=ftp_checking_options,
            )
        except Exception as err:
            case = True
        self.assertTrue(case)

        # Create FTP download file failed
        mock_start_ftp_service.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """Permission Denied""",
            "-rw-------. 1 root root 11508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 21508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 31508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 41508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 51508 Dec 16 16:02 ftp_download_file",
            True,
            True,
        )
        mock_create_ftp_connection_between_host.return_value = True

        ftp_topo_options = {
            "ftp_server_ipaddr":        "2000:20::2",
        }
        ftp_checking_options = {
            "check_counter":            5,
            "sleep_time":               10,
        }
        case = False
        try:
            self.ins.start_and_check_ftp_connection_during_issu(
                device_handlers=device_handlers,
                ftp_topo_options=ftp_topo_options,
                ftp_checking_options=ftp_checking_options,
            )
        except Exception as err:
            case = True
        self.assertTrue(case)

        # FTP checking failed
        mock_start_ftp_service.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """[root@fnd-lnx34 ~]# dd if=/dev/zero of=/home/regress/ftp_download_file bs=209715200 count=1
1+0 records in
1+0 records out
209715200 bytes (10 MB) copied, 0.888294 s, 70.8 MB/s
            """,
            "-rw-------. 1 root root 11508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 11508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 11508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 11508 Dec 16 16:02 ftp_download_file",
            "-rw-------. 1 root root 11508 Dec 16 16:02 ftp_download_file",
            True,
            True,
        )
        mock_create_ftp_connection_between_host.return_value = True

        device_handlers = {
            "ha_device_handler":        mock_device_ins,
            "node0_handler":            mock_device_ins,
            "node1_handler":            mock_device_ins,
            "ftp_server_handler":       mock_device_ins,
            "ftp_client_handler":       mock_device_ins,
        }
        ftp_topo_options = {
            "ftp_server_ipaddr":        "192.168.100.2",
        }
        ftp_checking_options = {
            "check_counter":            5,
            "check_failed_threshold":   3,
            "sleep_time":               10,
        }

        result = self.ins.start_and_check_ftp_connection_during_issu(
            device_handlers=device_handlers,
            ftp_topo_options=ftp_topo_options,
            ftp_checking_options=ftp_checking_options,
        )
        self.assertFalse(result)

        # No FTP download file found
        mock_start_ftp_service.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """[root@fnd-lnx34 ~]# dd if=/dev/zero of=/home/regress/ftp_download_file bs=209715200 count=1
1+0 records in
1+0 records out
209715200 bytes (10 MB) copied, 0.888294 s, 70.8 MB/s
            """,
            """No such file or directory""",
            """No such file or directory""",
            """No such file or directory""",
            """No such file or directory""",
            """No such file or directory""",
            True,
            True,
        )
        mock_create_ftp_connection_between_host.return_value = True

        device_handlers = {
            "ha_device_handler":        mock_device_ins,
            "node0_handler":            mock_device_ins,
            "node1_handler":            mock_device_ins,
            "ftp_server_handler":       mock_device_ins,
            "ftp_client_handler":       mock_device_ins,
        }
        ftp_topo_options = {
            "ftp_server_ipaddr":        "192.168.100.2",
        }
        ftp_checking_options = {
            "check_counter":            5,
            "check_failed_threshold":   3,
            "sleep_time":               10,
        }

        result = self.ins.start_and_check_ftp_connection_during_issu(
            device_handlers=device_handlers,
            ftp_topo_options=ftp_topo_options,
            ftp_checking_options=ftp_checking_options,
        )
        self.assertFalse(result)

    @mock.patch("time.sleep")
    @mock.patch.object(dev, "execute_shell_command_on_device")
    @mock.patch.object(linux_tool, "create_telnet_connection_between_host")
    @mock.patch.object(linux_tool, "close_telnet_connection_between_host")
    @mock.patch.object(setup_server, "start_telnet_service")
    def test_start_and_check_telnet_connection_during_issu(self,
        mock_start_telnet_service,
        mock_create_telnet_connection_between_host,
        mock_close_telnet_connection_between_host,
        mock_execute_shell_command_on_device,
        mock_sleep
    ):
        """UT Case"""
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.current_node.current_controller = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True


        # normal checking
        mock_start_telnet_service.return_value = True
        mock_create_telnet_connection_between_host.return_value = True
        mock_close_telnet_connection_between_host.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """
            01. TELNET_IS_ALIVE
            """,
            """
            01. TELNET_IS_ALIVE
            02. TELNET_IS_ALIVE
            """,
            """
            01. TELNET_IS_ALIVE
            02. TELNET_IS_ALIVE
            03. TELNET_IS_ALIVE
            """,
            """
            01. TELNET_IS_ALIVE
            02. TELNET_IS_ALIVE
            03. TELNET_IS_ALIVE
            04. TELNET_IS_ALIVE
            """,
            """
            01. TELNET_IS_ALIVE
            02. TELNET_IS_ALIVE
            03. TELNET_IS_ALIVE
            04. TELNET_IS_ALIVE
            05. TELNET_IS_ALIVE
            """,
            True,
        )

        device_handlers = {
            "ha_device_handler":        mock_device_ins,
            "node0_handler":            mock_device_ins,
            "node1_handler":            mock_device_ins,
            "telnet_server_handler":    mock_device_ins,
            "telnet_client_handler":    mock_device_ins,
        }
        telnet_topo_options = {
            "telnet_server_ipaddr":     "192.168.100.2",
        }
        telnet_checking_options = {
            "check_counter":            5,
            "sleep_time":               10,
        }

        result = self.ins.start_and_check_telnet_connection_during_issu(
            device_handlers=device_handlers,
            telnet_topo_options=telnet_topo_options,
            telnet_checking_options=telnet_checking_options,
        )
        self.assertTrue(result)

        # create TELNET server failed
        mock_start_telnet_service.return_value = False
        mock_create_telnet_connection_between_host.return_value = True
        mock_close_telnet_connection_between_host.return_value = True

        device_handlers = {
            "ha_device_handler":        mock_device_ins,
            "node0_handler":            mock_device_ins,
            "node1_handler":            mock_device_ins,
            "telnet_server_handler":    mock_device_ins,
            "telnet_client_handler":    mock_device_ins,
        }
        telnet_topo_options = {
            "telnet_server_ipaddr":     "192.168.100.2",
        }
        telnet_checking_options = {
            "check_counter":            5,
            "sleep_time":               10,
        }

        result = self.ins.start_and_check_telnet_connection_during_issu(
            device_handlers=device_handlers,
            telnet_topo_options=telnet_topo_options,
            telnet_checking_options=telnet_checking_options,
        )
        self.assertFalse(result)

        # TELNET ALIVE checking failed
        mock_start_telnet_service.return_value = True
        mock_create_telnet_connection_between_host.return_value = True
        mock_close_telnet_connection_between_host.return_value = True
        mock_execute_shell_command_on_device.side_effect = (
            """01. TELNET_IS_ALIVE""",
            """01. TELNET_IS_ALIVE""",
            """01. TELNET_IS_ALIVE""",
            """01. TELNET_IS_ALIVE""",
            """01. TELNET_IS_ALIVE""",
            True,
        )

        device_handlers = {
            "ha_device_handler":        mock_device_ins,
            "node0_handler":            mock_device_ins,
            "node1_handler":            mock_device_ins,
            "telnet_server_handler":    mock_device_ins,
            "telnet_client_handler":    mock_device_ins,
        }
        telnet_topo_options = {
            "telnet_server_ipaddr":     "192.168.100.2",
        }
        telnet_checking_options = {
            "check_counter":            5,
            "check_failed_threshold":   2,
            "sleep_time":               10,
        }

        result = self.ins.start_and_check_telnet_connection_during_issu(
            device_handlers=device_handlers,
            telnet_topo_options=telnet_topo_options,
            telnet_checking_options=telnet_checking_options,
        )
        self.assertFalse(result)

    @mock.patch.object(issu, "_jt_behavior")
    @mock.patch.object(chassis, "waiting_for_pic_online")
    @mock.patch("jnpr.toby.hldcl.juniper.security.robot_keyword.check_vmhost")
    @mock.patch("time.sleep")
    @mock.patch.object(srx_manual_issu, "do_issu")
    @mock.patch.object(dev, "execute_cli_command_on_device")
    @mock.patch.object(HA, "get_ha_healthy_status")
    @mock.patch.object(HA, "get_ha_rgs")
    def test_start_issu_upgrade(self,
        mock_get_ha_rgs,
        mock_get_ha_healthy_status,
        mock_execute_cli_command_on_device,
        mock_do_issu,
        mock_sleep,
        mock_check_vmhost,
        mock_waiting_for_pic_online,
        mock_jt_behavior,
    ):
        "UT Case"
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.current_node.current_controller = mock.Mock()
        mock_device_ins.log.return_value = None

        path = {}
        path["lower_image_base_dir"] = "/var/home/regress/LOWER_image"
        path["lower_image_filename"] = "junos-srx5000-17.2-20170430_dev_common.1.tgz"
        path["lower_image_fullpath"] = os.path.join(path["lower_image_base_dir"], path["lower_image_filename"])
        path["regression_image_base_dir"] = "/var/home/regress/Regression_image"
        path["regression_image_filename"] = "junos-srx5000-18.2-20170430_dev_common.1.tgz"
        path["regression_image_fullpath"] = os.path.join(path["regression_image_base_dir"], path["regression_image_filename"])
        path["higher_image_base_dir"] = "/var/home/regress/HIGHER_image"
        path["higher_image_filename"] = "junos-srx5000-19.2-20170430_dev_common.1.tgz"
        path["higher_image_fullpath"] = os.path.join(path["higher_image_base_dir"], path["higher_image_filename"])
        path["src_image_base_dir"] = path["regression_image_base_dir"]
        path["src_image_filename"] = path["regression_image_filename"]
        path["src_image_fullpath"] = path["regression_image_fullpath"]
        path["dst_image_base_dir"] = path["higher_image_base_dir"]
        path["dst_image_filename"] = path["higher_image_filename"]
        path["dst_image_fullpath"] = path["higher_image_fullpath"]
        mock_jt_behavior.return_value = path

        print("Normal ISSU testing")
        mock_check_vmhost.return_value = "vmhost"
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, True]
        mock_do_issu.return_value = True
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = True

        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertTrue(result)

        print("cannot get rgs")
        mock_check_vmhost.return_value = "vmhost"
        mock_get_ha_rgs.return_value = False
        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertFalse(result)

        print("rg status is not normal")
        mock_check_vmhost.return_value = "vmhost"
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, False]
        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertFalse(result)

        print("do storage cleanup before issu")
        mock_check_vmhost.return_value = "system"
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, True]
        mock_execute_cli_command_on_device.side_effect = ["", ""]
        mock_do_issu.return_value = True
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = True

        result = self.ins.start_issu_upgrade(device=mock_device_ins, storage_cleanup_before_issu=True)
        self.assertTrue(result)

        print("ISSU failed")
        mock_check_vmhost.return_value = "system"
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, True]
        mock_do_issu.side_effect = Exception

        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertFalse(result)

        print("reconnect device failed")
        mock_check_vmhost.return_value = "system"
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, True]
        mock_do_issu.side_effect = [True, True]
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True
        mock_device_ins.reconnect.return_value = False
        mock_waiting_for_pic_online.return_value = True

        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertFalse(result)

        print("FPC not online after checking")
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, True]
        mock_do_issu.return_value = True
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = False

        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertFalse(result)

        print("ISSU with package path")
        self.ins.image = {
            "dst_image_base_dir": "/var/home/regress/HIGHER_image",
            "dst_image_filename": "junos-install-srx5000-x86-64-19.4R2.6.tgz",
            "dst_image_fullpath": "/var/home/regress/HIGHER_image/junos-install-srx5000-x86-64-19.4R2.6.tgz",
            "dst_image_path_in_shell_server": None,
            "higher_image_base_dir": "/var/home/regress/HIGHER_image",
            "higher_image_filename": "junos-install-srx5000-x86-64-19.4R2.6.tgz",
            "higher_image_fullpath": "/var/home/regress/HIGHER_image/junos-install-srx5000-x86-64-19.4R2.6.tgz",
            "higher_image_path_in_shell_server": None,
            "lower_image_base_dir": "/var/home/regress/LOWER_image",
            "lower_image_path_in_shell_server": None,
            "regression_image_base_dir": "/var/home/regress/Regression_image",
            "regression_image_filename": "junos-install-srx5000-x86-64-19.4R1.12.tgz",
            "regression_image_fullpath": "/var/home/regress/Regression_image/junos-install-srx5000-x86-64-19.4R1.12.tgz",
            "regression_image_path_in_shell_server": None,
            "src_image_base_dir": "/var/home/regress/Regression_image",
            "src_image_filename": "junos-install-srx5000-x86-64-19.4R1.12.tgz",
            "src_image_fullpath": "/var/home/regress/Regression_image/junos-install-srx5000-x86-64-19.4R1.12.tgz",
            "src_image_path_in_shell_server": None,
        }
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, True]
        mock_do_issu.return_value = False
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = False

        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertFalse(result)

        print("No package found")
        mock_get_ha_rgs.return_value = [0, 1]
        mock_get_ha_healthy_status.side_effect = [True, True]
        mock_do_issu.return_value = False
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True
        mock_device_ins.reconnect.return_value = True
        mock_waiting_for_pic_online.return_value = False
        mock_jt_behavior.return_value = {"dst_image_fullpath": None, "higher_image_fullpath": None}
        self.ins.image["dst_image_fullpath"] = None
        self.ins.image["higher_image_fullpath"] = None
        result = self.ins.start_issu_upgrade(device=mock_device_ins)
        self.assertFalse(result)

        print("upload image from shell server and update image name")
        mock_jt_behavior.return_value = path




    @mock.patch("jnpr.toby.security.issu.issu.run_multiple")
    @mock.patch.object(linux_tool, "close_telnet_connection_between_host")
    @mock.patch.object(linux_tool, "close_ftp_connection_between_host")
    @mock.patch.object(issu, "start_and_check_ftp_connection_during_issu")
    @mock.patch.object(issu, "start_and_check_telnet_connection_during_issu")
    @mock.patch.object(issu, "start_issu_upgrade")
    def test_checking_issu_upgrade(self,
        mock_issu,
        mock_telnet,
        mock_ftp,
        mock_close_ftp,
        mock_close_telnet,
        mock_run_multiple,
    ):
        """UT Case"""
        # All case passed
        mock_device_ins = mock.Mock()
        mock_device_ins.node0 = mock.Mock()
        mock_device_ins.node1 = mock.Mock()
        mock_device_ins.current_node.current_controller = mock.Mock()
        mock_device_ins.log.return_value = None
        mock_device_ins.disconnect.return_value = True
        mock_device_ins.node0.disconnect.return_value = True
        mock_device_ins.node1.disconnect.return_value = True

        device_handlers = {
            "ha_device_handler":  mock_device_ins,
            "node0_handler":      mock_device_ins,
            "node1_handler":      mock_device_ins,
            "ftp_client_handler": mock_device_ins,
            "ftp_server_handler": mock_device_ins,
            "telnet_client_handler":  mock_device_ins,
            "telnet_server_handler":  mock_device_ins,
        }

        ftp_topo_options = {
            "ftp_server_ipaddr":            "192.168.20.2",
            "ftp_service_listen_port":      2121,
            "ftp_service_control_tool":     "service",
            "ftp_service_max_rate":         "1024",
            "download_file":                "ftp_download_file",
        }

        ftp_checking_options = {
            "check_counter":        20,
            "check_interval":       60,
            "check_failed_threshold": 3,
            "sleep_time":           10,
        }

        telnet_topo_options = {
            "telnet_server_ipaddr":         "192.168.20.2",
            "telnet_service_control_tool":  "service",
            "username":             "regress",
            "password":             "MaRtInI",
        }

        telnet_checking_options = {
            "check_counter":        20,
            "check_interval":       50,
            "check_failed_threshold":   3,
            "sleep_time":           20,
        }

        issu_options = {
            "package":              None,
            "no_copy":              True,
            "system":               "vmhost",
            "reconnect_counter":    20,
            "reconnect_interval":   60,
            "cluster_checking_counter":     20,
            "cluster_checking_interval":    60,
        }

        mock_issu.return_value = True
        mock_telnet.return_value = True
        mock_ftp.return_value = True
        mock_close_ftp.return_value = True
        mock_close_telnet.return_value = True
        mock_run_multiple.return_value = [True, True, True]

        result = self.ins.checking_issu_upgrade(
            device_handlers=device_handlers,
            protocol_check_list="FTP,TELNET",
            issu_options=issu_options,
            ftp_topo_options=ftp_topo_options,
            ftp_checking_options=ftp_checking_options,
            telnet_topo_options=telnet_topo_options,
            telnet_checking_options=telnet_checking_options,
        )
        self.assertTrue(result)

        # Protocol check list is LIST
        result = self.ins.checking_issu_upgrade(
            device_handlers=device_handlers,
            protocol_check_list=("FTP", "TELNET"),
            issu_options=issu_options,
            ftp_topo_options=ftp_topo_options,
            ftp_checking_options=ftp_checking_options,
            telnet_topo_options=telnet_topo_options,
            telnet_checking_options=telnet_checking_options,
        )
        self.assertTrue(result)

        # Protocol check list is Invalid
        case = False
        try:
            self.ins.checking_issu_upgrade(
                device_handlers=device_handlers,
                protocol_check_list=None,
                issu_options=issu_options,
                ftp_topo_options=ftp_topo_options,
                ftp_checking_options=ftp_checking_options,
                telnet_topo_options=telnet_topo_options,
                telnet_checking_options=telnet_checking_options,
            )
        except (ValueError, Exception) as err:
            case = True
        self.assertTrue(result)

        # No FTP related options
        device_handlers = {
            "ha_device_handler":  mock_device_ins,
            "node0_handler":      mock_device_ins,
            "node1_handler":      mock_device_ins,
            "ftp_client_handler": mock_device_ins,
            "ftp_server_handler": mock_device_ins,
            "telnet_client_handler":  mock_device_ins,
            "telnet_server_handler":  mock_device_ins,
        }

        ftp_topo_options = {
            "ftp_server_ipaddr":            "192.168.20.2",
            "ftp_service_listen_port":      2121,
            "ftp_service_control_tool":     "service",
            "ftp_service_max_rate":         "1024",
            "download_file":                "ftp_download_file",
            "download_file_size":           1048576,
        }

        ftp_checking_options = {
            "check_counter":        20,
            "check_interval":       60,
            "check_failed_threshold": 3,
            "sleep_time":           10,
        }

        telnet_topo_options = {
            "telnet_server_ipaddr":         "192.168.20.2",
            "telnet_service_control_tool":  "service",
            "username":             "regress",
            "password":             "MaRtInI",
        }

        telnet_checking_options = {
            "check_counter":        20,
            "check_interval":       50,
            "check_failed_threshold":   3,
            "sleep_time":           20,
        }

        issu_options = {
            "package":              None,
            "no_copy":              True,
            "system":               "system",
            "reconnect_counter":    20,
            "reconnect_interval":   60,
            "cluster_checking_counter":     20,
            "cluster_checking_interval":    60,
        }

        mock_issu.return_value = True
        mock_telnet.return_value = True
        mock_ftp.return_value = True

        case = False
        try:
            self.ins.checking_issu_upgrade(
                device_handlers=device_handlers,
                protocol_check_list="FTP,TELNET",
                issu_options=issu_options,
                # ftp_topo_options=ftp_topo_options,
                ftp_checking_options=ftp_checking_options,
                telnet_topo_options=telnet_topo_options,
                telnet_checking_options=telnet_checking_options,
            )
        except (ValueError, Exception) as err:
            case = True
        self.assertTrue(case)

        # No TELNET related options
        case = False
        try:
            self.ins.checking_issu_upgrade(
                device_handlers=device_handlers,
                protocol_check_list="FTP,TELNET",
                issu_options=issu_options,
                ftp_topo_options=ftp_topo_options,
                ftp_checking_options=ftp_checking_options,
                # telnet_topo_options=telnet_topo_options,
                telnet_checking_options=telnet_checking_options,
            )
        except (ValueError, Exception) as err:
            case = True
        self.assertTrue(case)

        # No FTP and TELNET checking options
        result = self.ins.checking_issu_upgrade(
            device_handlers=device_handlers,
            protocol_check_list="FTP,TELNET",
            issu_options=issu_options,
            ftp_topo_options=ftp_topo_options,
            # ftp_checking_options=ftp_checking_options,
            telnet_topo_options=telnet_topo_options,
            # telnet_checking_options=telnet_checking_options,
        )
        self.assertTrue(result)
