# coding: UTF-8
"""ALL L3 HA environment keywords"""

# pylint: disable=invalid-name

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2019'

import os

from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.utils import run_multiple, RunMultipleTimeoutException, RunMultipleException
from jnpr.toby.security.issu.issu import issu
from jnpr.toby.security.chassis.chassis import chassis

class l3_ha():
    """ALL L3 HA environment keywords"""
    def __init__(self):
        """INIT"""
        self.tool = flow_common_tool()
        self.issu = issu()
        self.chassis = chassis()

        self.default = {
            "reboot_timeout":               1800,
            "regression_image_folder":      "/var/home/regress/Regression_image",
            "higher_image_folder":          "/var/home/regress/HIGHER_image",
        }

        self.runtime = {
            "get_image": {},
        }

    def get_image(self, device, **kwargs):
        """Get image path from device

        :param STR regression_image_folder:
            *OPTIONAL* regression_image_folder. Default: /var/home/regress/Regression_image

        :param STR higher_image_folder:
            *OPTIONAL* higher_image_folder. Default: /var/home/regress/HIGHER_image

        :param BOOL force_get:
            *OPTIONAL* force to get image path again. Default: False

        :return:
            Return a DICT witch contain image path like below:

                $DICT = {
                    "regression_image":             "IMAGE_ABS_PATH",
                    "regression_image_filename":    "IMAGE_FILENAME",
                    "higher_image":                 "IMAGE_ABS_PATH",
                    "higher_image_filename":        "IMAGE_FILENAME",
                }

            If multiple image or no image found, return False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["regression_image_folder"] = kwargs.pop("regression_image_folder", self.default["regression_image_folder"])
        options["higher_image_folder"] = kwargs.pop("higher_image_folder", self.default["higher_image_folder"])
        options["force_get"] = kwargs.pop("force_get", False)

        dev_name = device.get_host_name()
        if dev_name not in self.runtime["get_image"]:
            self.runtime["get_image"][dev_name] = None

        if options["force_get"] is False and self.runtime["get_image"][dev_name] is not None:
            device.log(
                message="{} return value: \n{}".format(func_name, self.tool.pprint(self.runtime["get_image"][dev_name])),
                level="INFO",
            )
            return self.runtime["get_image"][dev_name]

        images = {}
        images["regression_image_filename"] = self.issu._search_image_on_both_node(
            device=device,
            folder=options["regression_image_folder"],
            raise_if_contain_multi_image=True,
        )
        images["regression_image"] = os.path.join(options["regression_image_folder"], images["regression_image_filename"])

        images["higher_image_filename"] = self.issu._search_image_on_both_node(
            device=device,
            folder=options["higher_image_folder"],
            raise_if_contain_multi_image=True,
        )
        images["higher_image"] = os.path.join(options["higher_image_folder"], images["higher_image_filename"])
        self.runtime["get_image"][dev_name] = images
        device.log(
            message="{} return value: \n{}".format(func_name, self.tool.pprint(self.runtime["get_image"][dev_name])),
            level="INFO",
        )
        return self.runtime["get_image"][dev_name]

    def l3_ha_upgrade_init(self, device_1, device_2, **kwargs):
        """Init upgrade environment on L3 HA setup

        1.  checking only 1 image in ~regress/Regression_image and ~regress/HIGHER_image folder
        2.  checking current image version whether same as ~regress/Regression_image folder

        :param OBJECT device_1 and device_2:
            **REQUIRED** 2 L3 HA device handlers.

        :param STR regression_image_folder:
            *OPTIONAL* regression_image_folder. Default: /var/home/regress/Regression_image

        :param STR higher_image_folder:
            *OPTIONAL* higher_image_folder. Default: /var/home/regress/HIGHER_image

        :param BOOL no_copy:
            *OPTIONAL* software install with 'no-copy' option. default: True

        :param BOOL no_validate:
            *OPTIONAL* software install with 'no-validate' option. default: True

        :param INT reboot_timeout:
            *OPTIONAL* device will reboot and reconnect after software installation, this option indicate how many secs the device reboot
                       finished. This method will reconnct device in loop every 20 secs until reach reboot_timeout. default: 600

        :param STR|LIST|TUPLE except_component:
            *OPTIONAL* skip specific device hardware component such as "SLOT 0 PIC 0", "SLOT 1", etc. More detail pls see
                       jnpr.toby.security.chassis.chassis.waiting_for_pic_online

        :param INT check_counter:
            *OPTIONAL* times to check all FPC online. default: 20

        :param INT check_interval:
            *OPTIONAL* time interval to check all FPC online. default: 60

        :return:
            Return True if all init success, or raise RuntimeError exception if:

                1.  Regression_image and HIGHER_image folder have more than 1 image or no image
                2.  upgrade to Regression_image failed
        """
        func_name = self.tool.get_current_function_name()
        device_1.log(message=func_name, level="INFO")

        options = {}
        options["regression_image_folder"] = kwargs.pop("regression_image_folder", self.default["regression_image_folder"])
        options["higher_image_folder"] = kwargs.pop("higher_image_folder", self.default["higher_image_folder"])
        options["no_copy"] = kwargs.pop("no_copy", True)
        options["no_validate"] = kwargs.pop("no_validate", True)
        options["reboot_timeout"] = int(kwargs.pop("reboot_timeout", self.default["reboot_timeout"]))
        options["except_component"] = kwargs.pop("except_component", ())
        options["check_counter"] = int(kwargs.pop("check_counter", 20))
        options["check_interval"] = float(kwargs.pop("check_interval", 60))

        names = {
            "device_1": device_1.get_host_name(),
            "device_2": device_2.get_host_name(),
        }
        device_handlers = {
            "device_1": device_1,
            "device_2": device_2,
        }

        # get regression image and higher image's path
        images = {}
        for keyword in device_handlers:
            images[keyword] = self.get_image(
                device=device_handlers[keyword],
                regression_image_folder=options["regression_image_folder"],
                higher_image_folder=options["higher_image_folder"],
                force_get=True,
            )

        if images["device_1"] is False or images["device_2"] is False:
            raise RuntimeError("No proper image found in '{}' and '{}'".format(options["regression_image_folder"], options["higher_image_folder"]))

        if images["device_1"]["regression_image_filename"] != images["device_2"]["regression_image_filename"]:
            raise RuntimeError("regression image filename are different between device_1 and device_2:\n\tdevice_1: {}\n\tdevice_2: {}".format(
                images["device_1"]["regression_image_filename"], images["device_2"]["regression_image_filename"]
            ))


        thread_list = []
        for keyword in device_handlers:
            version_info = device_handlers[keyword].get_version_info(force_get=True)
            if version_info is False: # pragma: no cover
                raise RuntimeError("Get device version info from '{}' failed.".format(keyword))

            if self.issu.compare_version_string(version_info["version"], images[keyword]["regression_image_filename"]) is False:
                device_handlers[keyword].log(message="'{}' version is different to '{}', will do upgrade for '{}'".format(
                    version_info["version"], images[keyword]["regression_image"], names[keyword]
                ), level="INFO")

                thread_list.append({
                    "fname": device_handlers[keyword].software_install,
                    "kwargs": {
                        "package": images[keyword]["regression_image_filename"],
                        "remote_path": options["regression_image_folder"],
                        "no_copy": options["no_copy"],
                        "validate": not options["no_validate"],         # user given no_validate which need reverse here
                        "reboot": True,
                        "timeout": options["reboot_timeout"],
                    }
                })


            else:
                device_1.log(message="'{}' version match to '{}', skip upgrade on '{}'".format(
                    version_info["version"], images[keyword]["regression_image"], names[keyword]
                ), level="INFO")

        # If no upgrade needed, stop immediately
        if not thread_list:
            device_1.log(message="{} return value: True".format(func_name))
            return True

        try:
            run_multiple(thread_list)
        except (RunMultipleTimeoutException, RunMultipleException): # pragma: no cover
            pass

        device_1.log(message="upgrade 2 devices done", level="INFO")

        # make sure all FPC online, and check node version whether same as regression image
        thread_list = []
        for keyword in device_handlers:
            device_handlers[keyword].log(message="waiting for '{}' all FPC online...".format(keyword), level="INFO")
            thread_list.append({
                "fname": self.chassis.waiting_for_pic_online,
                "kwargs": {
                    "device": device_handlers[keyword],
                    "except_component": options["except_component"],
                    "check_counter": options["check_counter"],
                    "check_interval": options["check_interval"],
                }
            })

        try:
            run_multiple(thread_list)
        except (RunMultipleTimeoutException, RunMultipleException): # pragma: no cover
            pass

        device_1.log(message="waiting all FPC online for 2 devices finished", level="INFO")
        device_1.log(message="checking 2 nodes have same software version and match regression image...", level="INFO")
        version_info = {
            "device_1": device_1.get_version_info(force_get=True),
            "device_2": device_2.get_version_info(force_get=True),
        }

        if version_info["device_1"]["version"] != version_info["device_2"]["version"]: # pragma: no cover
            raise RuntimeError("2 devices have different version:\n\tdevice_1: {}\n\tdevice_2: {}".format(
                version_info["device_1"]["version"], version_info["device_2"]["version"]))

        if self.issu.compare_version_string(version_info["device_1"]["version"], images["device_1"]["regression_image_filename"]) is False:
            raise RuntimeError("device version '{}' different as regression_image '{}'".format(
                version_info["device_1"]["version"], images["device_1"]["regression_image_filename"]))   # pragma: no cover

        device_1.log(
            message="2 devices' version '{}' same as regression image '{}'".format(
                version_info["device_1"]["version"], images["device_1"]["regression_image_filename"]
            ), level="INFO",
        )

        device_1.log(message="{} return value: True".format(func_name))
        return True
