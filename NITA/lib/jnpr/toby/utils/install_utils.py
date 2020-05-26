#! /usr/bin/python
"""
Install utilities which are useful throughout TOBY/CCNG.
"""
import time
import os as OS
import re
import copy
from jnpr.toby.exception.toby_exception import TobyException

def _aft_pakcage_install(self, package=None, timeout=None):
    """
    device_object.software_install(package = '/volume/openconfig/trunk/
    junos-openconfig-x86-32-0.0.0I20161227_1103_rbu-builder.tgz',
    progress = True)

    Performs the complete installation of the **package** that includes the
    following steps:

    :param str package:
    The file-path to the install package tarball
    on the local filesystem

    :param int timeout:
    The amount of time (seconds) before declaring an command timeout.
    """

    if package is None:
        raise TobyException('aft_image_upgrade() takes atleast 1 argument package ', host_obj=self)

    if timeout is None:
        timeout = 600
    self.log(level='INFO', message='Loading AFT package')
    self.su()

    if not re.match(r'\S+\s*,\s*\S+', package, re.I):
        if re.match('.sha1', package, re.I):
            return True
        package = package + "," + package + ".sha1"

    self.log(level="DEBUG", message="Checking weather the AFT package installation supported or not")
    mpc10_output = self.cli(command="show chassis fpc pic-status |match MPC5").response()
    fpc10_output = dict()
    for line in mpc10_output.split("\n"):
        match = re.match(r'Slot\s+(\d+)\s+(Online|Offline)\s+', line, re.I)
        if match:
            fpc10_output[match.group(1)] = 1
    hostname = self.get_host_name()
    if len(fpc10_output.keys()) > 0:
        self.log(level='INFO', message='AFT package installation supported on %s' % hostname)
    else:
        self.log(level='INFO', message='AFT package not supported on %s , \
                 skipping the package installation' % hostname)
        return True

    result = None
    package_list = package.split(',')

    for aft_pkg in package_list:
        if OS.path.exists(aft_pkg):
            self.log(level="INFO", message="AFT package %s is available on the shell server" % aft_pkg)
            match = re.match(r'(?:.*\/)?(.+)', aft_pkg, re.I)
            if match:
                aft_package = match.group(1)
            self.shell(command='cd /usr/share/pfe')
            if re.match(r'\.sha1', aft_pkg, re.I):
                self.log(level="INFO", message="mv aft.tgz.sha1 aft.tgz.sha1.orig")
                cmd_resp = self.shell(command="mv aft.tgz.sha1 aft.tgz.sha1.orig", \
                           pattern=['y/n', r'%[\s]?', r'#[\s]?', 'No such file or directory'],\
                           raw_output=True).response()
                if re.search(r'y/n', cmd_resp, re.I):
                    self.shell(command="y")
            else:
                self.log(level="INFO", message="mv aft.tgz aft.tgz.orig")
                cmd_resp = self.shell(command="mv aft.tgz aft.tgz.orig", \
                                   pattern=['y/n', r'%[\s]?', r'#[\s]?', 'No such file or directory'], \
                                   raw_output=True).response()
                if re.search(r'y/n', cmd_resp, re.I):
                    self.shell(command="y")

            if re.match(r'\.sha1', aft_package):
                dest_image_name = "/usr/share/pfe/" + "aft.tgz.sha1"
            else:
                dest_image_name = "/usr/share/pfe/" + "aft.tgz"

            if self.upload(local_file=aft_pkg, remote_file=dest_image_name,\
                           timeout=600, user='root', password='Embe1mpls'):
                self.log(level="INFO", message="Successfully copied the AFT package(%s) to %s" \
                          % (aft_pkg, dest_image_name))
                self.shell(command="ls -lrt %s " % dest_image_name)
            else:
                self.log(level="INFO", message="Failed to copy the AFT package(%s) to %s" \
                         % (aft_pkg, dest_image_name))
                return False
        else:
            self.log("AFT package(%s) provided is not available on shell server." % aft_pkg)
            return False

        restart_fpcs = list()
        self.log(level="DEBUG", message="Checking for the MPC10 FPC's Online")
        result = check_fpc_status(self, fpc_slots=fpc10_output.keys())

    self.log(level='DEBUG', message="Restarting the FPC's that are Online")
    for fpc_num in fpc10_output:
        restart_fpcs.append(fpc_num)
        self.log(level='DEBUG', message="Restarting the FPC %s" % fpc_num)
        fpc_restart_cmd = "restart fpc %s" % fpc_num
        self.cli(command=fpc_restart_cmd, timeout=150)
        time.sleep(5)
        while 1:
            pic_status_cmd = "show chassis fpc pic-status %s " % fpc_num
            pic_statu_resp = self.cli(command=pic_status_cmd, timeout=150).response()
            fpc_status = re.compile(r"Slot\s+%s\s+Online" % fpc_num)
            if fpc_status.search(pic_statu_resp, re.I):
                self.log(level="DEBUG", message="Restarting the FPC %s was successfull" % fpc_num)
                continue
            else:
                self.log(level="DEBUG", message="Sleeping for 5 sec before retry")
                time.sleep(5)

    if restart_fpcs and len(restart_fpcs) > 0:
        self.log(level='DEBUG', message="Checking whether the restarted FPC's are Online or not")
        result = check_fpc_status(self, fpc_slots=restart_fpcs, timeout=1500)
    return result



def _ulc_pakcage_install(self, package=None, timeout=None):
    """
    device_object.software_install(package = '/volume/openconfig/trunk/
    junos-openconfig-x86-32-0.0.0I20161227_1103_rbu-builder.tgz',
    progress = True)

    Performs the complete installation of the **package** that includes the
    following steps:

    :param str package:
        The file-path to the install package tarball
        on the local filesystem

    :param int timeout:
        The amount of time (seconds) before declaring an command timeout.
    """

    if package is None:
        raise TobyException('ulc_image_upgrade() takes atleast 1 argument package ', host_obj=self)

    if timeout is None:
        timeout = 600
    self.log(level='INFO', message='Loading ULC package')

    self.su()
    dest_path = "/usr/share/pfe/mpc"
    pkg_version, dev_version, result = None, None, None
    remote_pkg = None
    package_list = ()
    if isinstance(package, str):
        package_list = [package, ]
    elif isinstance(package, (list, tuple)):
        package_list = list(copy.deepcopy(package))
    for ulc_pkg in package_list:
        if OS.path.exists(ulc_pkg):
            self.log(level="INFO", message="ULC package %s is available on the shell server" % ulc_pkg)
            remote_pkg = 'ulc-mx-image'
            re_match = re.match(r'(.*)\.(tgz|iso)', ulc_pkg, re.I)
            if re_match:
                pkg_version = re_match.group(1)
                remote_pkg = remote_pkg+"."+re_match.group(2)
                if re_match.group(2) == 'iso':
                    dest_path = "/usr/share/pfe"
                else:
                    cmd_resp = self.shell(command="rm -rf $dest_path/*", \
                               pattern=['y/n', r'%[\s]?', r'#[\s]?'], raw_output=True).response()
                    if re.search(r'y/n', cmd_resp, re.I):
                        self.shell(command='y')
                re.sub('/.*/', '', pkg_version)
                self.shell(command='rm -rf /usr/share/pfe/ulc-mx-image.iso')
                remote_package = dest_path + "/" + remote_pkg
                if self.upload(local_file=ulc_pkg, remote_file=remote_package,\
                               timeout=600, user='root', password='Embe1mpls'):
                    self.log(level="INFO", message="Successfully copied the ULC package(%s) to %s" \
                              % (ulc_pkg, remote_package))
                    self.shell(command="ls -lrt %s " % remote_package)
                else:
                    self.log(level="INFO", message="Failed to copy the AFT package(%s) to %s" \
                             % (ulc_pkg, remote_package))
                    return False
            else:
                self.log("AFT package(%s) provided is not a supported format." % ulc_pkg)
                return False
        else:
            self.log("AFT package(%s) provided is not available on shell server." % ulc_pkg)
            return False

    if pkg_version:
        self.log("Restarting the chassisd")
        self.cli(command="restart chassis-control", timeout=150)
        self.log(level="INFO", message="Sleeping for 30 sec after chassis restart")
        time.sleep(30)
        version_cmd = "cat /usr/share/pfe/mpc/mpc11e_137_grub.cfg | grep evo"
        dev_version = self.shell(command=version_cmd).response()
        self.log(level="DEBUG", message="pkg_version: %s, dev_version: %s" % (pkg_version, dev_version))
        if re.search(pkg_version, pkg_version, re.I):
            self.log(level="INFO", message="ULC Pakcage version matched after upgrade")
            result = True
        else:
            self.log(level="INFO", message="ULC Pakcage version not matched after upgrade")
            result = False
    return result

def check_fpc_status(self, fpc_slots=None, timeout=900, interval=20):
    """
    FPC status check
    """
    retry = 1
    count = 0
    if fpc_slots is None:
        return True

    while (retry and interval >= 0):
        count = 0
        chk_stat_res = self.cli(command="show chassis fpc").response()
        for fpc_num in fpc_slots:
            fpc_status = re.compile(r'\s+%s\s+Online' % fpc_num)
            if fpc_status.search(chk_stat_res):
                count += 1
                self.log(level="DEBUG", message="FPC %s is Online after upgrade" % fpc_num)
            else:
                self.log(level="DEBUG", message="FPC %s is not yet Online after upgrade, \
                        Retrying again after 20" % fpc_num)
                time.sleep(interval)
                retry = 1
                timeout = timeout - 20
                continue
        if count == len(fpc_slots):
            self.log(level="INFO", message="All MPC10 FPC's are in Online state")
            retry = 0
            return True

    if interval < 0 and retry:
        self.log(level="ERROR", message="One or more FPC's restarted did not come Online")
        return False
