# coding: UTF-8
# pylint: disable=no-member
"""ISSU feature for SRX platform

Here are 2 DEMO scripts about how to use this module:

+   Just do ISSU without any session checking

    https://ssd-git.juniper.net/Juniper/test-suites/blob/master/FUNCTIONAL_REG/SECURITY/NAT/ISSU/nat_issu_root_tenant.robot

+   ISSU with FTP/TELNET session checking

    https://ssd-git.juniper.net/Juniper/test-suites/blob/master/FUNCTIONAL_REG/PLATFORM/CHASSIS/ISSU/issu_toby_gw.robot
"""

__author__ = ['Jon Jiang']
__contact__ = 'jonjiang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import os
import re
import time
import copy

from jnpr.toby.frameworkDefaults import credentials
from jnpr.toby.hldcl import device as dev
from jnpr.toby.hldcl.juniper.security import robot_keyword
from jnpr.toby.exception.toby_exception import TobyPromptTimeoutException
from jnpr.toby.utils.setup_server import setup_server
from jnpr.toby.utils.flow_common_tool import flow_common_tool
from jnpr.toby.utils.linux.linux_tool import linux_tool
from jnpr.toby.security.chassis.chassis import chassis
from jnpr.toby.security.issu.srx_manual_issu import srx_manual_issu
from jnpr.toby.security.HA.HA import HA
from jnpr.toby.utils.utils import run_multiple


class issu():
    """All ALG related ISSU feature"""
    def __init__(self):
        """Init processing"""
        self.tool = flow_common_tool()
        self.manual_issu = srx_manual_issu()
        self.host = linux_tool()
        self.srv = setup_server()
        self.chassis = chassis()
        self.ha = HA()

        self.default = {
            "cli_show_timeout": 300,
            "reboot_timeout": 3600,
            "issu_starting_timeout": 3600,
            "issu_upload_image_timeout": 3600,
            "junos_username": credentials.Junos["USERNAME"],
            "junos_password": credentials.Junos["PASSWORD"],
            "lower_image_folder": "/var/home/regress/LOWER_image",
            "regression_image_folder": "/var/home/regress/Regression_image",
            "higher_image_folder": "/var/home/regress/HIGHER_image",
        }

        self.image = {
            "lower_image_base_dir": None,
            "lower_image_filename": None,
            "lower_image_fullpath": None,

            "regression_image_base_dir": None,
            "regression_image_filename": None,
            "regression_image_fullpath": None,

            "higher_image_base_dir": None,
            "higher_image_filename": None,
            "higher_image_fullpath": None,

            "src_image_base_dir": None,
            "src_image_filename": None,
            "src_image_fullpath": None,

            "dst_image_base_dir": None,
            "dst_image_filename": None,
            "dst_image_fullpath": None,
        }

        self.image_path = {
            "regression_image": None,
            "higher_image": None,
        }

    def _jt_behavior(self, device, **kwargs):
        """JT script behavior to TOBY

        /volume/labtools/lib/Testsuites/Viking/HA/ISSU_Common.pm

        JT behavior include:

        +   Get value from below environment variables:

            -   TOBY_ISSU_LOWER_IMG_PATH
            -   TOBY_ISSU_REG_IMG_PATH
            -   TOBY_ISSU_HIGHER_IMG_PATH
            -   TOBY_LOWER_IMG_PATH_IN_SHELL_SERVER
            -   TOBY_REG_IMG_PATH_IN_SHELL_SERVER
            -   TOBY_HIGHER_IMG_PATH_IN_SHELL_SERVER
            -   TOBY_ISSU_TO

        +   SCP image file from shell server to devices' both node
        +   According to "TOBY_ISSU_TO" to determin which folder used to ISSU init/close stage.

        :param BOOL upload_image:
            *OPTIONAL* whether upload needed image from shell server to device. default: True

        :param BOOL delete_exist_file_before_upolad:
            *OPTIONAL* if option 'upload_image' and 'delete_exist_file_before_upolad' are all True, delete existing
                       image file before upload new one. default: True

        :param STR shell_server_username:
            *OPTIONAL* upload image from shell server account name. default: regress

        :param STR shell_server_password:
            *OPTIONAL* upload image from shell server account password. according to username

        :return:
            Return a DICT which have some path like below:

            {
                "lower_image_base_dir": lower_image_dir_on_device,
                "regression_image_base_dir": regression_image_dir_on_device,
                "higher_image_base_dir": higher_image_dir_on_device,
                "lower_image_path_in_shell_server": lower_image_full_path_in_shell_server,
                "regression_image_path_in_shell_server": regression_image_full_path_in_shell_server,
                "higher_image_path_in_shell_server": higher_image_full_path_in_shell_server,
                "src_image_base_dir": src_image_dir_on_device,
                "dst_image_base_dir": dst_image_dir_on_device,
                "src_image_path_in_shell_server": src_image_full_path_in_shell_server,
                "dst_image_path_in_shell_server": dst_image_full_path_in_shell_server,
            }
        """
        func_name = self.tool.get_current_function_name()

        options = {}
        options["upload_image"] = self.tool.check_boolean(kwargs.pop("upload_image", True))
        options["delete_exist_file_before_upolad"] = self.tool.check_boolean(kwargs.pop("delete_exist_file_before_upolad", True))
        options["check_md5_after_upload"] = self.tool.check_boolean(kwargs.pop("check_md5_after_upload", True))
        options["shell_server_username"] = kwargs.pop("shell_server_username", self.default["junos_username"])
        options["shell_server_password"] = kwargs.pop("shell_server_password", self.default["junos_password"])

        if self.image["src_image_fullpath"] is not None and self.image["dst_image_fullpath"] is not None and options["upload_image"] is False:
            return self.image

        path = {
            "lower_image_base_dir": os.getenv("TOBY_ISSU_LOWER_IMG_PATH", self.default["lower_image_folder"]),
            "regression_image_base_dir": os.getenv("TOBY_ISSU_REG_IMG_PATH", self.default["regression_image_folder"]),
            "higher_image_base_dir": os.getenv("TOBY_ISSU_HIGHER_IMG_PATH", self.default["higher_image_folder"]),
            "lower_image_path_in_shell_server": os.getenv("TOBY_LOWER_IMG_PATH_IN_SHELL_SERVER", None),
            "regression_image_path_in_shell_server": os.getenv("TOBY_REG_IMG_PATH_IN_SHELL_SERVER", None),
            "higher_image_path_in_shell_server": os.getenv("TOBY_HIGHER_IMG_PATH_IN_SHELL_SERVER", None),
        }

        # as default, src_folder is "/var/home/regress/Regression_image" and dst_folder is "/var/home/regress/HIGHER_image"
        #
        # if "TOBY_ISSU_TO" have keyword "regression", src_folder is "/var/home/regress/LOWER_image" and dst_folder is
        # "/var/home/regress/Regression_image"
        #
        # if "TOBY_ISSU_TO" do not have keyword "regression", src_folder and dst_folder same as default
        path["src_image_base_dir"] = copy.deepcopy(path["regression_image_base_dir"])
        path["dst_image_base_dir"] = copy.deepcopy(path["higher_image_base_dir"])
        path["src_image_path_in_shell_server"] = copy.deepcopy(path["regression_image_path_in_shell_server"])
        path["dst_image_path_in_shell_server"] = copy.deepcopy(path["higher_image_path_in_shell_server"])
        if re.match(r"regression", str(os.getenv("TOBY_ISSU_TO")).lower()):
            path["src_image_base_dir"] = copy.deepcopy(path["lower_image_base_dir"])
            path["dst_image_base_dir"] = copy.deepcopy(path["regression_image_base_dir"])
            path["src_image_path_in_shell_server"] = copy.deepcopy(path["lower_image_path_in_shell_server"])
            path["dst_image_path_in_shell_server"] = copy.deepcopy(path["regression_image_path_in_shell_server"])

        # according to base dir path on device, find existing image name and full path. if no image on device, just leave to None
        for keyword in ("lower_image_", "regression_image_", "higher_image_", "src_image_", "dst_image_"):
            base_dir_keyword = keyword + "base_dir"
            fullpath_keyword = keyword + "fullpath"
            filename_keyword = keyword + "filename"

            found_image_filename = self._search_image_on_both_node(device=device, folder=path[base_dir_keyword], raise_if_contain_multi_image=True)
            if found_image_filename is not None:
                path[fullpath_keyword] = os.path.join(path[base_dir_keyword], found_image_filename)
                path[filename_keyword] = found_image_filename

        self.image.update(path)
        if options["upload_image"] is False:
            return self.image

        # upload image from shell server, if image already existing, skip upload
        list_of_threads = []
        for image_base_dir_in_device, image_path_in_shell_server in (
                (path["src_image_base_dir"], path["src_image_path_in_shell_server"]),
                (path["dst_image_base_dir"], path["dst_image_path_in_shell_server"]),
        ):
            if image_path_in_shell_server is not None:
                # make sure image exists in shell server (local)
                if not os.path.isfile(image_path_in_shell_server):
                    raise RuntimeError("No local image file found: {}".format(image_path_in_shell_server))

                image_exists = False
                image_filename_in_shell_server = os.path.basename(image_path_in_shell_server)
                lines = dev.execute_shell_command_on_device(device=device, command="/bin/ls -l {}".format(image_base_dir_in_device))
                for line in lines.splitlines():
                    image_filename_in_device = re.split(r"\s+", line)[-1]
                    if image_filename_in_device == image_filename_in_shell_server:
                        image_exists = True
                        break

                if image_exists is False:
                    # delete all files if wanted image not in device
                    if options["delete_exist_file_before_upolad"] is True:
                        dev.execute_shell_command_on_device(device=device, command="/bin/rm -f {}/*".format(image_base_dir_in_device))

                    for hdl in (device.node0, device.node1):
                        list_of_threads.append({
                            'fname': hdl.upload,
                            'kwargs': {
                                "local_file": image_path_in_shell_server,
                                "remote_file": os.path.join(image_base_dir_in_device, image_filename_in_shell_server),
                                "user": options["shell_server_username"],
                                "password": options["shell_server_password"],
                                "protocol": "scp",
                            }
                        })

        if list_of_threads:
            run_multiple(targets=list_of_threads, timeout=int(self.default["issu_upload_image_timeout"] * 1.2))

        for keyword in ("src_image_", "dst_image_"):
            base_dir_keyword = keyword + "base_dir"
            fullpath_keyword = keyword + "fullpath"
            filename_keyword = keyword + "filename"

            found_image_filename = self._search_image_on_both_node(device=device, folder=path[base_dir_keyword], raise_if_contain_multi_image=True)
            if found_image_filename is not None:
                path[fullpath_keyword] = os.path.join(path[base_dir_keyword], found_image_filename)
                path[filename_keyword] = found_image_filename

        self.image.update(path)
        device.log(message="parallel upload image from shell server to device finished...", level="INFO")
        device.log(message="{} return value: \n{}".format(func_name, self.tool.pprint(self.image)), level="INFO")
        return self.image

    def _search_image_on_both_node(self, device, folder, **kwargs):
        """Search image in given path on 2 nodes, and return contained image(s)

        **Will get image on 2 nodes, and make sure images are same**

        :param STR folder:
            **REQUIRED** image basedir.

        :param BOOL raise_if_contain_multi_image:

            *OPTIONAL* if set True, raise RuntimeError exception while given folder have 1+ images. default: True

        :return:
            Return a LIST if raise_if_contain_multi_image=False, even only 1 image found. otherwise return image_filename or None
        """
        options = {}
        options["raise_if_contain_multi_image"] = self.tool.check_boolean(kwargs.pop("raise_if_contain_multi_image", True))

        device.log(message="find image from both nodes: '{}'".format(folder), level="INFO")

        devices = {
            "node0": device.node0,
            "node1": device.node1,
        }
        match_images = {}
        for node_name in devices:
            response = dev.execute_shell_command_on_device(device=devices[node_name], command="ls -l {}".format(folder))
            match_images[node_name] = []
            for line in response.splitlines():
                image_name = re.split(r"\s+", line.strip())[-1]
                match = re.match(r"junos\-\S+\.tgz", image_name)
                if match:
                    match_images[node_name].append(image_name)

        # make sure 2 nodes have same image(s)
        if match_images["node0"] != match_images["node1"]:
            raise RuntimeError("2 nodes have different image or no image in specific node")

        found_image_cnt = len(match_images["node0"])
        if options["raise_if_contain_multi_image"] is True:
            if found_image_cnt == 0:
                return_value = None
            elif found_image_cnt == 1:
                return_value = match_images["node0"][0]
            else:
                raise RuntimeError("Given folder '{}' contain 1+ images:\n{}".format(folder, self.tool.pprint(match_images)))
        else:
            return_value = match_images["node0"]

        return return_value

    def search_issu_image_path(self, device, **kwargs):
        """Search ISSU regression and higher image path

        :param STR regression_image_folder:
            *OPTIONAL* regression_image_folder. Default: /var/home/regress/Regression_image

        :param STR higher_image_folder:
            *OPTIONAL* higher_image_folder. Default: /var/home/regress/HIGHER_image

        :param BOOL force:
            *OPTIONAL* force to get image path again. Default: False

        :return:
            Return a DICT witch contain image path like below:

                $DICT = {
                    "regression_image":        "{IMAGE_ABS_PATH}",
                    "higher_image":            "{IMAGE_ABS_PATH}",
                }

            If multiple image or no image found, return False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["regression_image_folder"] = kwargs.pop("regression_image_folder", self.default["regression_image_folder"])
        options["higher_image_folder"] = kwargs.pop("higher_image_folder", self.default["higher_image_folder"])
        options["force"] = self.tool.check_boolean(kwargs.pop("force", False))

        if (options["force"] is False and
                self.image_path["regression_image"] is not None and
                self.image_path["higher_image"] is not None):

            return self.image_path

        search_path = {
            "regression_image":     options["regression_image_folder"],
            "higher_image":         options["higher_image_folder"]
        }

        for keyword in search_path:
            device.log(message="find image from '{}'".format(search_path[keyword]), level="INFO")
            response = dev.execute_shell_command_on_device(device=device, command="ls -l {}".format(search_path[keyword]))

            match_images = []
            for line in response.splitlines():
                match = re.search(r"\s+(junos-\S+\.tgz)", line)
                if match:
                    match_images.append(match.group(1))

            level = "INFO"
            if not match_images:
                msg = "No image found from '{}'".format(search_path[keyword])
                level = "ERROR"
            elif len(match_images) > 1:
                msg = "Multiple images found from '{}'".format(search_path[keyword])
                level = "ERROR"
            else:
                image = os.path.join(search_path[keyword], match_images[0])
                msg = "{}: {}".format(keyword, image)
                self.image_path[keyword] = image

            device.log(message=msg, level=level)
            if level == "ERROR":
                return False

        return self.image_path

    @staticmethod
    def compare_version_string(junos_version_string, image_filename_string):
        """Compare version string

        This method used for JunOS version check. it is because ticket TOBY-3277: https://engsupport.juniper.net/browse/TOBY-3277
        For JunOS version 19.1, image name is 'junos-srxhe-x86-64-19.1-2019-01-27.0_RELEASE_191_THROTTLE.tgz', but while load to device, version
        string is '19.1-20190127.0', this means device version string is not part of image name. And this cause version checking failed

        The solution is: delete all '-' and '_' from image filename and device version string, then searching version string. For examle:
          JunOS Version String: 19.120190127.0
          Image filename: JUNOSSRXHEX866419.120190127.0RELEASE191THROTTLE.TGZ
        Now they matched

        :return: True/False
        """
        version_string_matched = False
        if re.search(junos_version_string, image_filename_string):
            version_string_matched = True

        if version_string_matched is False:
            junos_version_string = re.sub(r"[-_]", "", junos_version_string.upper())
            image_filename_string = re.sub(r"[-_]", "", image_filename_string.upper())

            if re.search(junos_version_string, image_filename_string):
                version_string_matched = True

        return version_string_matched

    def software_install(self, device, package, **kwargs):
        """Install software on device based on command: request system software add ...

        :params STR package:
            **REQUIRED** package path on device

        :params STR system:
            **OPTIONAL** string 'system' or 'vmhost' to do 'request system/vmhost software add ...'. default: automatic find

        :param BOOL no_copy:
            *OPTIONAL* no_copy option in base command. default: False

        :params BOOL no_validate:
            *OPTIONAL* no_validate option in base command. default: True

        :params BOOL reboot:
            *OPTIONAL* reboot option in base command. default: True

        :param INT wait:
            *OPTIONAL* waiting time before reconnect device. will ignore this option if option 'reboot' is False. default: 60

        :params STR|INT timeout:
            *OPTIONAL* reconnect device timeout. default: 3600
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["package"] = package
        options["system"] = kwargs.get("system", None)
        options["no_copy"] = self.tool.check_boolean(kwargs.get("no_copy", False))
        options["no_validate"] = self.tool.check_boolean(kwargs.get("no_validate", True))
        options["reboot"] = self.tool.check_boolean(kwargs.get("reboot", True))
        options["wait"] = int(kwargs.get("wait", 60))
        options["timeout"] = int(kwargs.get("timeout", self.default["reboot_timeout"]))

        hostname = device.get_host_name()

        if options["system"] is None:
            options["system"] = robot_keyword.check_vmhost(device=device)

        # vmhost based platform do not support no-copy behavior
        if options["system"] == "vmhost":
            options["no_copy"] = False

        cmd_element_list = []
        cmd_element_list.append("request {} software add {}".format(options["system"], options["package"]))

        for keyword in ("no_copy", "no_validate"):
            if options[keyword] is True:
                cmd_element_list.append(keyword.replace("_", "-"))

        cmd = " ".join(cmd_element_list)
        device.log(message="install package on {}: {}".format(hostname, cmd), level="INFO")
        dev.execute_cli_command_on_device(device=device, command=cmd, channel="text", format="text", timeout=options["timeout"])

        if options["reboot"] is True:
            reboot_options = {"mode": "cli", "wait": options["wait"], "timeout": options["timeout"]}
            if options["system"] == "vmhost":
                reboot_options["device_type"] = "vmhost"

            device.log(message="start rebooting {}".format(hostname), level="INFO")
            reboot_status = device.reboot(**reboot_options)
            if reboot_status is False:
                device.log(message="device reboot failed...", level="ERROR")
                device.log(message="{} return value: {}".format(func_name, reboot_status), level="ERROR")
                return reboot_status

            device.log(message="device reboot succeed...", level="INFO")

        device.log(message="{} return value: {}".format(func_name, True), level="INFO")
        return True

    def issu_init(self, device, **kwargs):
        """Init ISSU environment

        For compatibility, 2 options "regression_image_folder" and "higher_image_folder" used for previous scripts, but
        they are now has be deprecated. Do not use them for new scripts.

        New options are "src_image_folder" and "dst_image_folder". And checking with:

        1.  checking only 1 image in src_image_folder and dst_image_folder
        2.  checking current image version whether same as src_image_folder

        :param STR regression_image_folder:
            *OPTIONAL* regression_image_folder. Default: /var/home/regress/Regression_image

        :param STR higher_image_folder:
            *OPTIONAL* higher_image_folder. Default: /var/home/regress/HIGHER_image

        :param STR src_image_folder:
            *OPTIONAL* src_image_folder. If environment variables TOBY_ISSU_TO="regression" then is
                       "/var/home/regress/LOWER_image", otherwise is "/var/home/regress/Regression_image"

        :param STR dst_image_folder:
            *OPTIONAL* dst_image_folder. If environment variables TOBY_ISSU_TO="regression" then is
                       "/var/home/regress/Regression_image", otherwise is "/var/home/regress/HIGHER_image"

        :params STR system:
            **OPTIONAL** string 'system' or 'vmhost' to do 'request system/vmhost software add ...'. default: automatic find

        :param BOOL no_validate:
            *OPTIONAL* software install with 'no-validate' option. default: True

        :param INT reboot_timeout:
            *OPTIONAL* device will reboot and reconnect after software installation, this option indicate how many secs the device reboot
                       finished. This method will reconnct device in loop every 20 secs until reach reboot_timeout. default: 600

        :param STR|LIST|TUPLE except_component:
            *OPTIONAL* skip specific device hardware component such as "SLOT 0 PIC 0", "SLOT 1", etc. More detail pls see
                       jnpr.toby.security.chassis.chassis.waiting_for_pic_online

        :param INT check_counter:
            *OPTIONAL* times to check all FPC online. default: 30

        :param INT check_interval:
            *OPTIONAL* time interval to check all FPC online. default: 60

        :return:
            Return True if all init success, or raise RuntimeError exception if:

                1.  src_image_folder or dst_image_folder have 1+ image
                2.  install src_image_folder image failed
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["regression_image_folder"] = kwargs.pop("regression_image_folder", self.default["regression_image_folder"])
        options["higher_image_folder"] = kwargs.pop("higher_image_folder", self.default["higher_image_folder"])
        options["system"] = kwargs.pop("system", None)
        options["no_validate"] = self.tool.check_boolean(kwargs.pop("no_validate", True))
        options["reboot_timeout"] = int(kwargs.pop("reboot_timeout", self.default["reboot_timeout"]))
        options["except_component"] = kwargs.pop("except_component", ())
        options["check_counter"] = int(kwargs.pop("check_counter", 20))
        options["check_interval"] = float(kwargs.pop("check_interval", 60))

        device.switch_to_primary_node()
        image = self._jt_behavior(device=device, upload_image=True, delete_exist_file_before_upolad=True)
        options["src_image_folder"] = kwargs.pop("src_image_folder", image["src_image_base_dir"])
        options["dst_image_folder"] = kwargs.pop("dst_image_folder", image["dst_image_base_dir"])

        src_image_filename = self._search_image_on_both_node(device=device, folder=options["src_image_folder"], raise_if_contain_multi_image=True)
        _ = self._search_image_on_both_node(device=device, folder=options["dst_image_folder"], raise_if_contain_multi_image=True)

        if options["system"] is None:
            options["system"] = robot_keyword.check_vmhost(device=device)

        dev.execute_cli_command_on_device(
            device=device,
            command="request chassis cluster in-service-upgrade abort",
            channel="text",
            format="text",
        )

        version_info = device.get_version_info(force_get=True)
        if not isinstance(version_info, dict):
            raise RuntimeError("Get device version failed.")

        device_hdl = {
            "node0":        device.node0,
            "node1":        device.node1,
        }

        list_of_threads = []
        for node_name in device_hdl:
            if self.compare_version_string(version_info[node_name]["version"], src_image_filename) is True:
                continue

            device.log(message="starting to install software '{}' on '{}' on parallel...".format(src_image_filename, node_name), level="INFO")
            list_of_threads.append({
                'fname': self.software_install,
                'kwargs': {
                    "device": device_hdl[node_name],
                    "package": os.path.join(options["src_image_folder"], src_image_filename),
                    "system": options["system"],
                    "no_copy": True,
                    "reboot": True,
                    "no_validate": options["no_validate"],
                    "timeout": options["reboot_timeout"],
                }
            })

        if list_of_threads:
            run_multiple(targets=list_of_threads, timeout=options["reboot_timeout"] * 2)
            device.log(message="parallel upgrade {} finished...".format(src_image_filename), level="INFO")
        else:
            device.log(message="2 nodes' have same version as image {}".format(src_image_filename), level="INFO")

        # make sure all FPC online, and check node version whether same as regression image
        device.log(message="waiting for all FPC online...", level="INFO")
        result = self.chassis.waiting_for_pic_online(
            device=device,
            except_component=options["except_component"],
            check_counter=options["check_counter"],
            check_interval=options["check_interval"],
        )
        if result is False:
            raise RuntimeError("FPC online check failed...")

        device.log(message="all FPC are online...", level="INFO")

        device.log(message="checking 2 nodes have same software version and match regression image...", level="INFO")
        response = device.get_version_info(force_get=True)
        if response is False:
            raise RuntimeError("get device version failed...")

        if response["node0"]["version"] != response["node1"]["version"]:
            raise RuntimeError("2 nodes have different version: {} != {}".format(response["node0"]["version"], response["node1"]["version"]))

        if self.compare_version_string(response["node0"]["version"], src_image_filename) is False:
            raise RuntimeError("device version '{}' different as regression_image '{}'".format(
                response["node0"]["version"], src_image_filename
            ))

        device.log(
            message="2 nodes' version '{}' same as regression image '{}'".format(response["node0"]["version"], src_image_filename),
            level="INFO",
        )

        device.log(message="{} return value: {}".format(func_name, True))
        return True

    def issu_close(self, device, **kwargs):
        """Restore ISSU environment to regression image

        On device, there should have 3 image locations such as ~regress/LOWER_image/, HIGHER_image/ and
        Regression_image/ , this method will upgrade/downgrade to Regression_image

        :param STR regression_image_folder:
            *OPTIONAL* regression_image_folder. Default: /var/home/regress/Regression_image

        :param STR higher_image_folder:
            *OPTIONAL* higher_image_folder. Default: /var/home/regress/HIGHER_image

        :param STR src_image_folder:
            *OPTIONAL* src_image_folder. If environment variables TOBY_ISSU_TO="regression" then is
                       "/var/home/regress/LOWER_image", otherwise is "/var/home/regress/Regression_image"

        :param STR dst_image_folder:
            *OPTIONAL* dst_image_folder. If environment variables TOBY_ISSU_TO="regression" then is
                       "/var/home/regress/Regression_image", otherwise is "/var/home/regress/HIGHER_image"

        :param INT reboot_timeout:
            *OPTIONAL* device will reboot and reconnect after software installation, this option indicate how many secs the device reboot
                       finished. This method will reconnct device in loop every 20 secs until reach reboot_timeout. default: 600

        :param INT check_counter:
            *OPTIONAL* times to check all FPC online. default: 20

        :param INT check_interval:
            *OPTIONAL* time interval to check all FPC online. default: 60

        :return:
            Return True if all init success, or raise RuntimeError exception if:

                1.  src_image_folder or dst_image_folder have 1+ image
                2.  install src_image_folder image failed
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        device.current_node.current_controller.reconnect()
        device.node0.reconnect()
        device.node1.reconnect()

        # always upgrade/downgrade to regression image
        kwargs["src_image_folder"] = os.getenv("TOBY_ISSU_REG_IMG_PATH", self.default["regression_image_folder"])
        return self.issu_init(device=device, **kwargs)

    def do_issu(self, device, package, **kwargs):
        """start ISSU upgrade

        :param STR package:
            **REQUIRED** package local path on device

        :param STR username:
            *OPTIONAL* device login username. default: regress

        :param STR password:
            *OPTIONAL* device login password. default: MaRtInI

        :param BOOL no_copy:
            *OPTIONAL* whether add 'no-copy' option while do ISSU. default: True

        :param BOOL reboot:
            *OPTIONAl* whether add 'reboot' option while do ISSU. default: True

        :param STR more_options:
            *OPTIONAL* tail more string to issu upgrade cmd. this is useful to add hidden options such as "no-validate", "no-compatibility-check"
                         etc... default: None

        :param STR system:
            *OPTIONAL* system string for "system" or "vmhost". default: automatic

        :param INT reconnection_counter:
            *OPTIONAL* during ISSU, connection to primary device will break and need to reconnect.
                         "reconnection_counter" and "reconnect_interval" option used for loop reconnection device.

                         default: 30

        :param INT reconnection_interval:
            *OPTIONAL*   default: 60

        :param INT cluster_checking_counter:
            *OPTIONAL* after primary node rebooting, script will checking cluster state to make sure priority > 0 and cluster status is
                         'primary' or 'secondary'. option 'cluster_checking_counter' and 'cluster_checking_interval' used for loop checking
                         them. default: 20

        :param STR|LIST|TUPLE cluster_except_component:
            *OPTIONAL* As default, 2 nodes' component must all online, but you can give one or more component name here to avoid checking.

            For example:

                ```
                Slot 0   Online       SRX5k SPC II
                  PIC 0  Offline      SPU Cp
                  PIC 1  Online       SPU Flow
                  PIC 2  Online       SPU Flow
                  PIC 3  Offline      SPU Flow
                Slot 2   Online       SRX5k IOC II
                  PIC 0  Online       10x 10GE SFP+
                ```

            Above output will create an internal offline list: ["SLOT 0 PIC 0", "SLOT 0 PIC 3", "PIC 0", "PIC 3"], you can list these
            keywords in this option to skip them. This means you can just skip "PIC 0" for all SLOT, or set "SLOT 0 PIC 0" for specific PIC.

            By the way, component keyword is case insensitive, this means keyword "pic 0", "PIC 0", or "Slot 0 Pic 0" all match above output

            For IOC 3, 2 PICs always offline, and this method will skip them automatically.

        :param INT cluster_checking_interval:
            *OPTIONAL*   default: 60

        :return:
            True/False
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        options = {}
        options["package"] = package
        options["username"] = kwargs.get("username", self.default["junos_username"])
        options["password"] = kwargs.get("password", self.default["junos_password"])
        options["no_copy"] = kwargs.get("no_copy", True)
        options["reboot"] = kwargs.get("reboot", True)
        options["more_options"] = kwargs.get("more_options", None)
        options["system"] = kwargs.get("system", None)
        options["reconnection_counter"] = int(kwargs.get("reconnection_counter", 30))
        options["reconnection_interval"] = int(kwargs.get("reconnection_interval", 60))
        options["cluster_checking_counter"] = int(kwargs.get("cluster_checking_counter", 40))
        options["cluster_checking_interval"] = int(kwargs.get("cluster_checking_interval", 60))
        options["cluster_except_component"] = kwargs.get("cluster_except_component", None)

        if options["cluster_except_component"] is None:
            options["cluster_except_component"] = ()

        if options["system"] is None:
            options["system"] = robot_keyword.check_vmhost(device=device)

        # vmhost based device do not support no-copy behavior
        if options["system"] == "vmhost":
            options["no_copy"] = False

        # create new primary device's handler to starting issu
        device.switch_to_primary_node()
        dev.execute_cli_command_on_device(device=device, channel="text", format="text", command="request chassis cluster in-service-upgrade abort")

        # make sure all RGs in normal status
        rgs = self.ha.get_ha_rgs(device=device)
        if rgs is False:
            device.log(message="Cannot get RGs from device {}".format(device), level="ERROR")
            return False

        for rg in rgs:
            status = self.ha.get_ha_healthy_status(device=device, rg=str(rg))
            if status is False:
                device.log(message="rg {} is on abnormal status".format(rg))
                return False

        # send issu cmd to device and waiting for primary device reboot
        issu_cmd_element = []
        issu_cmd_element.append("request {} software in-service-upgrade {}".format(options["system"], package))
        if options["no_copy"] is True:
            issu_cmd_element.append("no-copy")

        issu_cmd_element.append("reboot")

        if options["more_options"] is not None:
            issu_cmd_element.append(options["more_options"])

        issu_cmd = " ".join(issu_cmd_element)
        device.log(message="send cmd: {}".format(issu_cmd), level="INFO")

        try:
            dev.execute_cli_command_on_device(
                device=device,
                channel="text",
                format="text",
                timeout=self.default["issu_starting_timeout"],
                pattern="System going down IMMEDIATELY",
                command=issu_cmd,
            )
        except TobyPromptTimeoutException as err: # pragma: no cover
            device.log(message="ISSU breaked with:\n{}".format(err), level="ERROR")
            return False

        device.disconnect(ignore_error=True)
        device.current_node.current_controller.disconnect(ignore_error=True)
        device.node0.disconnect(ignore_error=True)
        device.node1.disconnect(ignore_error=True)

        time.sleep(120)
        device.log(message="waiting 120 seconds for ISSU upgrading...")
        status = device.reconnect(
            all=True,
            timeout=options["reconnection_interval"] * options["reconnection_counter"] + 60,
            interval=options["reconnection_interval"],
            force=True,
        )
        if status is False:
            return status

        # waiting for cluster online
        all_node_online = self.chassis.waiting_for_pic_online(
            device=device,
            except_component=options["cluster_except_component"],
            check_counter=options["cluster_checking_counter"],
            check_interval=options["cluster_checking_interval"],
        )

        if all_node_online is True:
            msg = "ISSU upgrade succeed..."
        else:
            msg = "ISSU node not online after '{}' secs...".format(options["reconnection_counter"] * options["reconnection_interval"])

        device.log(message=msg, level="INFO")
        return all_node_online

    def start_and_check_ftp_connection_during_issu(self, **kwargs):
        """Create FTP session on HA topo, and check related flow session during ISSU upgrade

        Steps:

            +   start FTP service on "ftp_server_handler"
            +   use ftp client to download file.
            +   loop check FTP file size whether increase

        All options are in DICT options as below:

        :param DICT device_handlers:

            :param OBJ ha_device_handler:
                **REQUIRED** HA handler such as ${r0}

            :param OBJ ftp_server_handler:
                **REQUIRED** FTP server device's handler. Will use vsftpd to create FTP server.

            :param OBJ ftp_client_handler:
                **REQUIRED** FTP client device's handler.

        :param DICT ftp_topo_options:

            :param IP ftp_server_ipaddr:
                **REQUIRED** FTP server IP address.

            :param INT ftp_service_listen_port:
                *OPTIONAL* FTP service listen port. Default: None

            :param STR ftp_service_control_tool:
                *OPTIONAL* Must be "service" or "systemctl". Default: service

                           Based on different Linux OS, vsftpd server may managed by /sbin/service or /sbin/systemctl cmd. As I know Ubuntu 12.04,
                           CentOS 6 and previous distribution use 'service' cmd like "service vsftpd restart", and Ubuntu 16.04, CentOS7 and upper
                           version use 'systemctl' cmd like "systemctl restart vsftpd". You should give right tool to manage them.

            :param INT ftp_service_max_rate:
                *OPTIONAL* Traffic max rate both upload and download. Default: 10240 (10K)

                           Because we need keep alive FTP session during ISSU upgrade, max rate will keep background traffic in long time

            :param STR username:
                *OPTIONAL* FTP login username. Default: regress

            :param STR password:
                *OPTIONAL* FTP login password. Default: MaRtInI

            :param STR download_file:
                *OPTIONAL* File path will download from server. Default: ~{USERNAME}/ftp_download_file

                           On FTP server, according to option "username" to use 'dd' cmd to create download file.

            :param STR download_file_size:
                *OPTIONAL* Download file size. Unit: byte and Default: 209715200 (200Mb)

        :param DICT ftp_checking_options:
            :param INT check_counter:
                *OPTIONAL* How many times to check flow session during ISSU. The session must exising every checking. Default: 30

            :param INT check_interval:
                *OPTIONAl* Time interval between 2 check. Default: 55

            :param INT sleep_time:
                *OPTIONAL* Waiting a while before ISSU upgrading start. Default: 0

            :param INT check_failed_threshold:
                *OPTIONAL* Sometimes FTP checking may failed by accident but session is alive. Set this option to skip several checking.

                           default: 0

        :return:
            True or False
        """
        options = {
            "ha_device_handler":            kwargs["device_handlers"].get("ha_device_handler"),
            "ftp_server_handler":           kwargs["device_handlers"].get("ftp_server_handler"),
            "ftp_client_handler":           kwargs["device_handlers"].get("ftp_client_handler"),

            "ftp_server_ipaddr":            kwargs["ftp_topo_options"].get("ftp_server_ipaddr"),
            "ftp_service_listen_port":      kwargs["ftp_topo_options"].get("ftp_service_listen_port", 21),
            "ftp_service_control_tool":     kwargs["ftp_topo_options"].get("ftp_service_control_tool", "service"),
            "ftp_service_max_rate":         int(kwargs["ftp_topo_options"].get("ftp_service_max_rate", 10240)),
            "username":                     kwargs["ftp_topo_options"].get("username", self.default["junos_username"]),
            "password":                     kwargs["ftp_topo_options"].get("password", self.default["junos_password"]),
            "download_file_size":           int(kwargs["ftp_topo_options"].get("download_file_size", 209715200)), # 200Mb

            "check_counter":                int(kwargs["ftp_checking_options"].get("check_counter", 30)),
            "check_interval":               int(kwargs["ftp_checking_options"].get("check_interval", 55)),
            "check_failed_threshold":       int(kwargs["ftp_checking_options"].get("check_failed_threshold", 0)),
            "sleep_time":                   int(kwargs["ftp_checking_options"].get("sleep_time", 0)),
        }
        func_name = self.tool.get_current_function_name()
        options["ha_device_handler"].log(message=self.tool.print_title(func_name), level="INFO")

        options["download_file"] = kwargs["ftp_topo_options"].get("download_file", "ftp_download_file")

        if options["sleep_time"] != 0:
            options["ha_device_handler"].log(message="{} waiting {} secs for ISSU starting...".format(func_name, options["sleep_time"]), level="INFO")
            time.sleep(options["sleep_time"])

        options["ha_device_handler"].log(message="All FTP options:\n{}".format(self.tool.pprint(options)), level="INFO")

        # setup FTP server
        if re.search(r":", options["ftp_server_ipaddr"]):
            ipv6_support = True
        else:
            ipv6_support = False

        options["ftp_server_handler"].log(message="Start FTP service...", level="INFO")
        result = self.srv.start_ftp_service(
            device=options["ftp_server_handler"],
            listen_port=options["ftp_service_listen_port"],
            service_control_tool=options["ftp_service_control_tool"],
            max_rate=options["ftp_service_max_rate"],
            banner="FTP server for ISSU background traffic testing",
            ipv6_support=ipv6_support,
        )
        if result is not True:
            raise RuntimeError("Create FTP server failed.")

        options["ftp_server_handler"].log(message="Start FTP service result: {}".format(result), level="INFO")
        cmd = "dd if=/dev/zero of={} bs={} count=1".format(options["download_file"], options["download_file_size"])
        options["ftp_server_handler"].log(message="Create download file by: '{}'".format(cmd), level="INFO")

        response = dev.execute_shell_command_on_device(device=options["ftp_server_handler"], command=cmd, timeout=120)
        if not re.search(str(options["download_file_size"]), response):
            raise RuntimeError("Crate FTP download file failed.")

        # start FTP traffic and download file times same as flow session check counter
        options["ftp_client_handler"].log(message="Get file from FTP server in background...", level="INFO")
        self.host.create_ftp_connection_between_host(
            device=options["ftp_client_handler"],
            remote_host=options["ftp_server_ipaddr"],
            port=options["ftp_service_listen_port"],
            username=options["username"],
            password=options["password"],
            cmd="get {}".format(options["download_file"]),
            mode="background",
            no_need_pid=True,
            timeout=options["check_counter"] * options["check_interval"] * 2,
        )
        options["ftp_client_handler"].log(message="waiting '60' secs to create FTP session...", level="INFO")
        time.sleep(60)

        # check FTP download file increase in loop
        options["ftp_client_handler"].log(message="start checking FTP download file increasing...", level="INFO")

        final_result = True
        ftp_basename = os.path.basename(options["download_file"])
        cmd = "ls -l {} | cat".format(ftp_basename)
        last_size = 0
        check_fail_cnt = 0
        for index in range(1, options["check_counter"] + 1):
            response = dev.execute_shell_command_on_device(device=options["ftp_client_handler"], command=cmd, timeout=10)
            options["ftp_client_handler"].log(message="{}:\n{}".format(cmd, response), level="INFO")

            level = "INFO"
            msg = ""
            new_size = 0
            for line in response.splitlines():
                match = re.search(r"\s+{}$".format(ftp_basename), line.strip())
                if match:
                    new_size = int(re.split(r"\s+", line)[4])
                    break

            if new_size == 0:
                check_fail_cnt += 1
                msg = "index '{}': cannot get FTP download file size on FTP client host, fail cnt: {}".format(index, check_fail_cnt)
                level = "WARN"
            else:
                if last_size >= new_size:
                    check_fail_cnt += 1
                    msg = "index '{}': looks FTP download file size is not change... (Last Size) {} <==> {} (Current Size), fail cnt: {}".format(
                        index, last_size, new_size, check_fail_cnt,
                    )
                    level = "WARN"
                else:
                    msg = "index '{}': FTP download file size increased '{}' bytes".format(index, new_size - last_size)
                    level = "INFO"
                    last_size = new_size

            options["ftp_client_handler"].log(message=msg, level=level)

            if check_fail_cnt > options["check_failed_threshold"]:
                options["ftp_client_handler"].log(
                    message="index '{}': FTP download file size checking failed {} time(s). break next checking.".format(index, check_fail_cnt),
                    level="ERROR"
                )
                final_result = False
                break

            options["ftp_client_handler"].log(message="waiting {} seconds for next checking...".format(options["check_interval"]), level="INFO")
            time.sleep(options["check_interval"])

        # stop FTP connection and delete temp file
        options["ftp_client_handler"].log(message="stop FTP connection and delete temporary file...", level="INFO")

        self.host.close_ftp_connection_between_host(device=options["ftp_client_handler"])
        dev.execute_shell_command_on_device(device=options["ftp_client_handler"], command="/bin/rm {}".format(ftp_basename), timeout=30)
        dev.execute_shell_command_on_device(device=options["ftp_server_handler"], command="/bin/rm {}".format(options["download_file"]), timeout=30)
        options["ha_device_handler"].log(message="{} result: {}".format(func_name, final_result), level="INFO")
        return final_result

    def start_and_check_telnet_connection_during_issu(self, **kwargs):
        """Create TELNET session on HA topo, and check related flow session during ISSU upgrade

        Steps:

            +   start TELNET service on host
            +   create TELNET connection and write some string to TELNET server
            +   loop checking new string on TELNET server to make sure connection exists

        All options are in DICT options as below:

        :params DICT device_handlers:

            :param OBJ ha_device_handler:
                **REQUIRED** HA handler such as ${r0}

            :param OBJ telnet_server_handler:
                **REQUIRED** TELNET server device's handler. Will use xinetd to create TELNET server.

            :param OBJ telnet_client_handler:
                **REQUIRED** TELNET client device's handler.

        :params DICT telnet_topo_options:

            :param IP telnet_server_ipaddr:
                **REQUIRED** TELNET server IP address.

            :param INT telnet_service_listen_port:
                *OPTIONAL* TELNET service listen port. Default: 23

            :param STR telnet_service_control_tool:
                *OPTIONAL* Must be "service" or "systemctl". Default: service

                           Based on different Linux OS, TELNET server may managed by /sbin/service or /sbin/systemctl cmd. As I know Ubuntu 12.04,
                           CentOS 6 and previous distribution use 'service' cmd like "service xinetd restart", and Ubuntu 16.04, CentOS7 and upper
                           version use 'systemctl' cmd like "systemctl restart xinetd". You should give right tool to manage them.

            :param STR username:
                *OPTIONAL* TELNET login username. Default: regress

            :param STR password:
                *OPTIONAL* TELNET login password. Default: MaRtInI

        :params DICT telnet_checking_options:
            :param INT check_counter:
                *OPTIONAL* How many times to check flow session during ISSU. The session must exising every checking. Default: 30

            :param INT check_interval:
                *OPTIONAl* Time interval between 2 check. Default: 55

            :param INT sleep_time:
                *OPTIONAL* Waiting a while before ISSU upgrading start. Default: 10

            :param INT check_failed_threshold:
                *OPTIONAL* Sometimes TELNET checking may failed by accident but session is alive. Set this option to skip several checking.

                           default: 0

        :return:
            True or False
        """
        options = {
            "ha_device_handler":            kwargs["device_handlers"].get("ha_device_handler"),
            "telnet_server_handler":        kwargs["device_handlers"].get("telnet_server_handler"),
            "telnet_client_handler":        kwargs["device_handlers"].get("telnet_client_handler"),

            "telnet_server_ipaddr":         kwargs["telnet_topo_options"].get("telnet_server_ipaddr"),
            "telnet_service_listen_port":   int(kwargs["telnet_topo_options"].get("telnet_service_listen_port", 23)),
            "telnet_service_control_tool":  kwargs["telnet_topo_options"].get("telnet_service_control_tool", "service"),
            "username":                     kwargs["telnet_topo_options"].get("username", self.default["junos_username"]),
            "password":                     kwargs["telnet_topo_options"].get("password", self.default["junos_password"]),

            "check_counter":                int(kwargs["telnet_checking_options"].get("check_counter", 30)),
            "check_interval":               int(kwargs["telnet_checking_options"].get("check_interval", 55)),
            "check_failed_threshold":       int(kwargs["telnet_checking_options"].get("check_failed_threshold", 0)),
            "sleep_time":                   int(kwargs["telnet_checking_options"].get("sleep_time", 10)),
        }
        func_name = self.tool.get_current_function_name()
        options["ha_device_handler"].log(message=self.tool.print_title(func_name), level="INFO")

        options["ha_device_handler"].log(message="All TELNET options:\n{}".format(self.tool.pprint(options)), level="INFO")
        if options["sleep_time"] != 0:
            options["ha_device_handler"].log(message="{} waiting {} secs for ISSU starting...".format(func_name, options["sleep_time"]), level="INFO")
            time.sleep(options["sleep_time"])

        result = self.srv.start_telnet_service(
            device=options["telnet_server_handler"],
            port=options["telnet_service_listen_port"],
            service_control_tool=options["telnet_service_control_tool"],
        )
        if result is False:
            options["telnet_server_handler"].log(message="Start TELNET service failed...", level="ERROR")
            return False

        options["telnet_server_handler"].log(message="Start TELNET service succeed...", level="INFO")

        # create TELNET connection
        write_file = "/tmp/telnet_alive_file"
        cmd_element_list = []
        for index in range(1, options["check_counter"] + 1):
            cmd_element_list.append("echo '{:02d}. TELNET_IS_ALIVE' >> {}, sleep {}".format(
                index, write_file, options["check_interval"] - 1
            ))

        self.host.create_telnet_connection_between_host(
            device=options["telnet_client_handler"],
            remote_host=options["telnet_server_ipaddr"],
            mode="background",
            username=options["username"],
            password=options["password"],
            no_need_pid=True,
            cmd=",".join(cmd_element_list),
            timeout=300,
        )

        options["telnet_client_handler"].log(message="waiting '10' secs for TELNET session created...", level="INFO")
        time.sleep(10)

        # checking TELNET connection
        final_result = True
        last_cnt = 0
        check_fail_cnt = 0
        cmd = "cat {} | grep TELNET_IS_ALIVE".format(write_file)
        for check_index in range(1, options["check_counter"]):
            response = dev.execute_shell_command_on_device(device=options["telnet_server_handler"], command=cmd, timeout=30)
            options["telnet_client_handler"].log(message="response of cmd '{}':\n{}".format(cmd, response), level="INFO")

            level = "INFO"
            msg = ""
            new_cnt = len(response.splitlines())
            if last_cnt == new_cnt:
                msg = "index '{}': looks new TELNET_IS_ALIVE string not added to {}".format(check_index, write_file)
                level = "WARN"
                check_fail_cnt += 1
            else:
                msg = "\nwaiting '{}' secs next TELNET session alive checking...\n".format(options["check_interval"])
                level = "INFO"
                last_cnt = new_cnt

            options["telnet_client_handler"].log(message=msg, level=level)

            if check_fail_cnt > options["check_failed_threshold"]:
                options["telnet_client_handler"].log(
                    message="index '{}': TELNET_IS_ALIVE checking failed {} time(s). break next checking.".format(check_index, check_fail_cnt),
                    level="ERROR"
                )
                final_result = False
                break

            options["telnet_client_handler"].log(message="waiting {} seconds for next checking...".format(options["check_interval"]), level="INFO")
            time.sleep(options["check_interval"])

        # stop TELNET connection and delete temp file
        dev.execute_shell_command_on_device(device=options["telnet_server_handler"], command="/bin/rm {}".format(write_file), timeout=30)
        status = self.host.close_telnet_connection_between_host(device=options["telnet_client_handler"])

        options["ha_device_handler"].log(message="stop TELNET connection: {}".format(status), level="INFO")
        options["ha_device_handler"].log(message="{} result: {}".format(func_name, final_result), level="INFO")
        return final_result

    def start_issu_upgrade(self, device, **kwargs):
        """Do ISSU upgrade and monitor upgrade processing

        :param HANDLE device:
            **REQUIRED** HA device handler. Make sure not node handler

        :param STR package:
            *OPTIONAL*   default will find TOBY_ISSU_TO environment variable whether have keyword "regression" to
                         determin package is from ~regress/HIGHER_image or ~regress/Regression_image folder. You can set
                         this option for specific package

        :param BOOL no_copy:
            *OPTIONAL*   whether add 'no-copy' option while do ISSU. default: True

        :param BOOL storage_cleanup_before_issu:
            *OPTIONAL*   cleanup all nodes' storage before issu. default: False

        :param STR system:
            *OPTIONAL* system string for "system" or "vmhost". default: automatic

        :param STR more_options:
            *OPTIONAL* more option string tail in ISSU command. default: None

        :param INT wait_time_before_reconnection:
            *OPTIONAL* wait time before reconnection devices. default: 120

        :param INT reconnection_counter:
            *OPTIONAL*   during ISSU, connection to primary device will break and need to reconnect.
                         "reconnection_counter" and "reconnect_interval" option used for loop reconnection device.

                         default: 30

        :param INT reconnection_interval:
            *OPTIONAL*   default: 60

        :param INT cluster_checking_counter:
            *OPTIONAL*   after primary node rebooting, script will checking cluster state to make sure priority > 0 and cluster status is
                         'primary' or 'secondary'. option 'cluster_checking_counter' and 'cluster_checking_interval' used for loop checking
                         them. default: 20

        :param STR|LIST|TUPLE cluster_except_component:
            *OPTIONAL* As default, 2 nodes' component must all online, but you can give one or more component name here to avoid checking.

            For example:

                ```
                Slot 0   Online       SRX5k SPC II
                  PIC 0  Offline      SPU Cp
                  PIC 1  Online       SPU Flow
                  PIC 2  Online       SPU Flow
                  PIC 3  Offline      SPU Flow
                Slot 2   Online       SRX5k IOC II
                  PIC 0  Online       10x 10GE SFP+
                ```

            Above output will create an internal offline list: ["SLOT 0 PIC 0", "SLOT 0 PIC 3", "PIC 0", "PIC 3"], you can list these
            keywords in this option to skip them. This means you can just skip "PIC 0" for all SLOT, or set "SLOT 0 PIC 0" for specific PIC.

            By the way, component keyword is case insensitive, this means keyword "pic 0", "PIC 0", or "Slot 0 Pic 0" all match above output

            For IOC 3, 2 PICs always offline, and this method will skip them automatically.


        :param INT cluster_checking_interval:
            *OPTIONAL*   default: 60
        """
        func_name = self.tool.get_current_function_name()
        device.log(message=self.tool.print_title(func_name), level="INFO")

        do_issu_options = {}
        do_issu_options["device"] = device
        do_issu_options["package"] = kwargs.pop("package", None)
        do_issu_options["no_copy"] = kwargs.pop("no_copy", True)
        do_issu_options["system"] = kwargs.pop("system", None)
        do_issu_options["more_options"] = kwargs.pop("more_options", None)

        if do_issu_options["system"] is None:
            do_issu_options["system"] = robot_keyword.check_vmhost(device=device)

        options = {}
        options["storage_cleanup_before_issu"] = self.tool.check_boolean(kwargs.pop("storage_cleanup_before_issu", False))
        options["wait_time_before_reconnection"] = int(kwargs.pop("wait_time_before_reconnection", 120))
        options["reconnection_counter"] = int(kwargs.pop("reconnection_counter", 30))
        options["reconnection_interval"] = int(kwargs.pop("reconnection_interval", 60))
        options["cluster_checking_counter"] = int(kwargs.pop("cluster_checking_counter", 20))
        options["cluster_checking_interval"] = int(kwargs.pop("cluster_checking_interval", 60))
        options["cluster_except_component"] = kwargs.pop("cluster_except_component", None)

        if options["cluster_except_component"] is None:
            options["cluster_except_component"] = ()

        # vmhost based device do not support no-copy behavior
        if do_issu_options["system"] == "vmhost":
            do_issu_options["no_copy"] = False

        if do_issu_options["package"] is None:
            if self.image["dst_image_fullpath"] is None or self.image["higher_image_fullpath"] is None:
                self.image = self._jt_behavior(device=device, upload_image=False, delete_exist_file_before_upolad=False)

            do_issu_options["package"] = self.image["dst_image_fullpath"] if self.image["dst_image_fullpath"] is not None else self.image["higher_image_fullpath"]

        if do_issu_options["package"] is None:
            device.log(message="Cannot get upgrade image path from device", level="ERROR")
            return False

        # ISSU prepare
        #     +   Make sure all RGs in normal status
        #     +   Cleanup 2 nodes' storage
        rgs = self.ha.get_ha_rgs(device=device)
        if rgs is False:
            device.log(message="Cannot get RGs from device {}".format(device), level="ERROR")
            return False

        for rg in rgs:
            status = self.ha.get_ha_healthy_status(device=device, rg=str(rg))
            if status is False:
                device.log(message="rg {} is on abnormal status".format(rg))
                return False

        device.switch_to_primary_node()
        if options["storage_cleanup_before_issu"] is True:
            for hdl in (device.node0, device.node1):
                dev.execute_cli_command_on_device(
                    device=hdl,
                    channel="text",
                    format="text",
                    command="request {} storage cleanup no-confirm".format(do_issu_options["system"]),
                )

        # do ISSU
        try:
            device.log(message="issu options: {}".format(self.tool.pprint(do_issu_options)), level="INFO")
            result = self.manual_issu.do_issu(**do_issu_options)
        except BaseException as err:
            device.log(message=err, level="ERROR")
            result = False

        if result is False:
            return result

        # reconnect device then waiting for chassis all FPC onlined and HA state restored
        device.disconnect(ignore_error=True)
        device.current_node.current_controller.disconnect(ignore_error=True)
        device.node0.disconnect(ignore_error=True)
        device.node1.disconnect(ignore_error=True)
        device.log(message="waiting {} seconds for ISSU upgrading...".format(options["wait_time_before_reconnection"]))
        time.sleep(options["wait_time_before_reconnection"])

        status = device.reconnect(
            all=True,
            timeout=options["reconnection_interval"] * options["reconnection_counter"] + 60,
            interval=options["reconnection_interval"],
            force=True,
        )
        if status is False:
            return status

        # waiting for cluster online
        all_node_online = self.chassis.waiting_for_pic_online(
            device=device,
            except_component=options["cluster_except_component"],
            check_counter=options["cluster_checking_counter"],
            check_interval=options["cluster_checking_interval"],
        )

        if all_node_online is True:
            message = "ISSU upgrade succeed..."
        else:
            message = "ISSU node not online after '{}' secs...".format(options["reconnection_counter"] * options["reconnection_interval"])

        device.log(message=message, level="INFO")
        return all_node_online


    def checking_issu_upgrade(self, device_handlers, protocol_check_list, **kwargs):
        """Main processing to start ISSU processing with traffic

        :param OBJ device_handlers:
            **REQUIRED** device handlers on ISSU setup.  Example:

            For robot:

                &{device_handlers}    Create Dictionary
                ...    ha_device_handler=${r0}
                ...    ftp_client_handler=${h0}
                ...    ftp_server_handler=${h1}
                ...    telnet_client_handler=${h2}
                ...    telnet_server_handler=${h3}

            For Python:

                device_handlers = {
                    "ha_device_handler": r0,
                    "ftp_client_handler": h0,
                    "ftp_server_handler": h1,
                    "telnet_client_handler": h2,
                    "telnet_server_handler": h3,
                }

        :param STR|LIST|TUPLE protocol_check_list
            **REQUIRED** How many protocol need to check during ISSU upgrade. If get a string, will use re.split(",") to split. If not set, just
                       do pure ISSU upgrade.

            Example:

                FTP,TELNET,SSH ==> ("FTP", "TELNET", "SSH")             # from .robot, use comma to split each protocol
                ["FTP", "TELNET", "SSH"] ==> ("FTP", "TELNET", "SSH")   # from .py should give list directly

        :param STR issu_options:
            *OPTIONAL* options for issu, such as "package", "no_copy", "reconnect_counter", etc...

            Example:

                For robot:

                    &{issu_options}    Create Dictionary
                    ...    package=${None}
                    ...    no_copy=${True}
                    ...    system=vmhost
                    ...    reconnect_counter=${10}
                    ...    reconnect_interval=${60}
                    ...    cluster_except_component=${None}
                    ...    cluster_checking_counter=${20}
                    ...    cluster_checking_interval=${60}

                For Python:
                    issu_options = {
                        "package": None,
                        "no_copy": True,
                        "system": "vmhost",
                        "reconnect_counter": 10,
                        "reconnect_interval": 60,
                        "cluster_except_component": None,
                        "cluster_checking_counter": 20,
                        "cluster_checking_interval": 60,
                    }

        :params DICT ftp_topo_options:
            *OPTIONAL* FTP server/client options. Example:

            For robot:

            &{ftp_topo_options}    Create Dictionary
            ...    ftp_server_ipaddr=xxx.xxx.xxx.xxx
            ...    ftp_service_listen_port=${21}
            ...    ftp_service_control_tool=systemctl
            ...    ftp_service_max_rate=${102400}
            ...    download_file_size=${104857600}
            ...    username=regress
            ...    password=MaRtInI

        :params DICT ftp_checking_options:
            *OPTIONAL* FTP checking behavior. Example:

            For robot:

            &{ftp_checking_options}    Create Dictionary
            ...    check_counter=${60}
            ...    check_interval=${120}
            ...    check_failed_threshold=${3}

        :params DICT telnet_topo_options:
            *OPTIONAL* TELNET server/client options. Example:

            For robot:

            &{telnet_topo_options}    Create Dictionary
            ...    telnet_server_ipaddr=xxx.xxx.xxx.xxx
            ...    telnet_service_listen_port=${23}
            ...    telnet_service_control_tool=systemctl
            ...    username=regress
            ...    password=MaRtInI

        :params DICT telnet_checking_options:
            *OPTIONAL* FTP checking behavior. Example:

            For robot:

            &{telnet_checking_options}    Create Dictionary
            ...    check_counter=${60}
            ...    check_interval=${120}
            ...    check_failed_threshold=${3}

        Invoke this method example:

        For robot:

            ${result}    issu.Checking ISSU Upgrade
            ...    device_handlers=${device_handlers}
            ...    protocol_check_list=FTP,TELNET
            ...    ftp_topo_options=${ftp_topo_options}
            ...    ftp_checking_options=${ftp_checking_options}
            ...    telnet_topo_options=${telnet_topo_options}
            ...    telnet_checking_options=${telnet_checking_options}
            ...    issu_options=${issu_options}

        :return:
            True or False
        """
        options = {}
        options["protocol_check_list"] = protocol_check_list
        options["issu_options"] = kwargs.pop("issu_options", {})

        default_value_list = (
            ("package", None),
            ("no_copy", True),
            ("system", None),
            ("reconnection_counter", 10),
            ("reconnection_interval", 60),
            ("cluster_except_component", None),
            ("cluster_checking_counter", 20),
            ("cluster_checking_interval", 60),
        )

        for keyword, value in default_value_list:
            if keyword not in options["issu_options"]:
                options["issu_options"][keyword] = value

        if options["issu_options"]["cluster_except_component"] is None:
            options["issu_options"]["cluster_except_component"] = ()

        func_name = self.tool.get_current_function_name()
        device_handlers["ha_device_handler"].log(message=self.tool.print_title(func_name), level="INFO")

        # check option
        if isinstance(options["protocol_check_list"], str):
            options["protocol_check_list"] = re.split(r"\s*,\s*", options["protocol_check_list"])
        elif isinstance(options["protocol_check_list"], (list, tuple)):
            pass
        else:
            raise ValueError("option 'protocol_check_list' should be STR, LIST or TUPLE, but got '{}'".format(type(protocol_check_list)))

        check_list = []
        for element in options["protocol_check_list"]:
            check_list.append(element.upper())

        list_of_threads = []
        # check FTP scenario.
        #   FTP checking need "ftp_topo_options" and "ftp_session_options", and they must be DICT
        if "FTP" in check_list:
            if "ftp_topo_options" not in kwargs or not isinstance(kwargs["ftp_topo_options"], dict):
                raise RuntimeError("For FTP scenario, DICT option 'ftp_topo_options' must given.")

            if "ftp_checking_options" not in kwargs:
                kwargs["ftp_checking_options"] = {}

            list_of_threads.append({
                'fname': self.start_and_check_ftp_connection_during_issu,
                'kwargs': {
                    "device_handlers":          device_handlers,
                    "ftp_topo_options":         kwargs["ftp_topo_options"],
                    "ftp_checking_options":     kwargs["ftp_checking_options"],
                }
            })

        # check TELNET scenario
        #   TELNET checking need "telnet_topo_options" and "telnet_session_options", and they must be DICT
        if "TELNET" in check_list:
            if "telnet_topo_options" not in kwargs or not isinstance(kwargs["telnet_topo_options"], dict):
                raise RuntimeError("For TELNET scenario, DICT option 'telnet_topo_options' must given.")

            if "telnet_checking_options" not in kwargs:
                kwargs["telnet_checking_options"] = {}

            list_of_threads.append({
                'fname': self.start_and_check_telnet_connection_during_issu,
                'kwargs': {
                    "device_handlers":          device_handlers,
                    "telnet_topo_options":      kwargs["telnet_topo_options"],
                    "telnet_checking_options":  kwargs["telnet_checking_options"],
                }
            })

        # do ISSU upgrade, don't delete
        options["issu_options"]["device"] = device_handlers["ha_device_handler"]
        list_of_threads.append({
            'fname': self.start_issu_upgrade,
            'kwargs': options["issu_options"],
        })

        result = run_multiple(targets=list_of_threads, timeout=self.default["issu_starting_timeout"] * 2)
        self.host.close_ftp_connection_between_host(device=device_handlers["ftp_client_handler"])
        self.host.close_telnet_connection_between_host(device=device_handlers["telnet_client_handler"])

        final_result = result.count(True) == len(list_of_threads)
        device_handlers["ha_device_handler"].log(message="multiple threads result: {}".format(result))
        device_handlers["ha_device_handler"].log(message="{} final result: {}".format(func_name, final_result), level="INFO")
        return final_result
