"""Module contains methods for Pic"""
# pylint: disable=undefined-variable
# pylint: disable=invalid-name
__author__ = ['Sumanth Inabathini']
__contact__ = 'isumanth@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'

import re
import time
from jnpr.toby.services import utils
from jnpr.toby.services.rutils import rutils

class pic(rutils):
    """Class contains methods for Pic"""

    def __init__(self, **kwargs):
        """Constructor method for Pic class

        :param bool is_media:
            **OPTIONAL** Enable if given interface is a media pic. Default is False

        :param bool is_vc:
            **OPTIONAL** Enable if system is part of MX Virtual Chassis. Default is False

        :param bool is_qosmos:
            **OPTIONAL** Enable for QOSMOS. Default is False

        :param bool is_vmsmpc:
            **OPTIONAL** Enable for vMSMPC mode. Default is False

        :param bool is_perf_mode:
            **OPTIONAL** Enable for performance mode for vMSMPC. Default is False

        :param bool do_online:
            **OPTIONAL** Bring the pic online. Default is True

        :param int mspmand_wait:
            **OPTIONAL** Maximum time to wait for MSPMAND to come up after rebooting.
            Default is 580

        :param bool is_mpsdk_dbgm:
            **OPTIONAL** Enable MSP-DEBUG. Default is False

        :return: Object on successful instantiation else raises an exception

        :rtype: Object or exception
        """

        super().__init__(**kwargs)

        #self.pic = {}
        # Pic state machine
        self.is_connected = False
        self.is_loggedin = False

        self.pic_state = None
        self._dut_model = None
        self._ri_ip = None
        self._vc_mbr_id = None
        self.fpc_type = None
        self.pic_type = None
        #self.fpc_slot = None
        #self.pic_slot = None
        #self.port = None
        self.init_pic = kwargs.get('init_pic', False)

        self.is_vc = kwargs.get('is_vc', False)
        self.is_qosmos = kwargs.get('is_qosmos', False)
        self.is_media = kwargs.get('is_media', False)
        self.is_mpsdk = kwargs.get('is_mpsdk', True)
        self.is_mpsdk_dbgm = kwargs.get('is_mpsdk_dbgm', False)
        self.is_vmsmpc = kwargs.get('is_vmsmpc', False)
        self.is_perf_mode = kwargs.get('is_perf_mode', True)
        self.do_online = kwargs.get('do_online', True)

        self.mspmand_wait = kwargs.get('mspmand_wait', 580)

        #for key in kwargs:
            #setattr(self, key, kwargs[key])

        if self.init_pic:
            self.init(**kwargs)

    #def init(self, resource=None, ifname=None, **kwargs):
    def init(self, **kwargs):
        """Initialise the class parameters

        :param string resource:
            **REQUIRED** DUT name

        :param string ifname:
            **REQUIRED** MS Interface

        Example::

          Python:
            init(resource='h0', ifname='ms-1/1/2')

          Robot:
            init   resource=r0   ifname=ms-1/1/2
        """
        # super().init(**kwargs)

        resource = kwargs.get('resource', None)
        ifname = kwargs.get('ifname', None)

        self.set_resource(resource=resource)
        self.resource = resource

        if ifname is None:
            self.log('ERROR', "Missing mandatory argument, ifname")
            raise TypeError("Missing mandatory argument, ifname")

        self.ifname = ifname

        self.fpc_slot, self.pic_slot, self.port = self.get_fpc_pic_port_from_ifname(self.ifname)

        self.log('INFO', "Creating pic object for " + self.ifname)

        if self.fpc_slot is None or self.pic_slot is None:
            self.log('ERROR', "fpc/pic couldn't be determined from the given ifname:{}\
                ".format(self.ifname))
            raise Exception("fpc/pic couldn't be determined from the given ifname:{}\
                ".format(self.ifname))

        if self.is_vmsmpc and self.is_perf_mode:
            self.log('INFO', "Configuring performance-mode for fpc {}".format(self.ifname))
            self.cmd = "set chassis fpc {} performance-mode".format(self.fpc_slot)
            self.cmd_add('')
            self.config()
        if self.is_vc:
            self._vc_mbr_id = 1 if int(self.fpc_slot) > 11 else 0
            if self.fpc_slot > 11:
                self.fpc_slot -= 12

        self._ri_ip = str(129 + self._vc_mbr_id) if self.is_vc else str(128)
        self._ri_ip += ".0." + str(int(self.pic_slot) + 1) + "." + str(int(self.fpc_slot) + 16)
        self.pic_type = self.get_pic_type(err_lvl='INFO') if not self.is_media else 'media'
        self.is_loggedin = self.is_connected = False

        self.log('INFO', "Pic ({}) is {}".format(self.ifname, self.pic_state))

        if not self.is_media and self.do_online:
            if self.pic_type is None and 'MS-' not in self.fpc_type:
                self.log('INFO', "Setting pic type to MS-MIC")
                self.pic_type = 'MS-MIC-16G'

            # Online the PIC irrespective of the current state.
            self.log('INFO', "Trying to online {}, irrespective of the current state".format(
                self.ifname))
            # if not self.online(online_wait=0):  # online need to be implemented
            #     self.log('ERROR', "Could not online mic/pic, {}".format(self.ifname))
            #     raise Exception("Could not online mic/pic, {}".format(self.ifname))

            # Ensure the pic is online before we proceed.
            self.log('INFO', "Waiting for the PIC to be online within {}secs".format(
                self.mspmand_wait))
            if not self.is_pic_online_yet(**kwargs):
                self.log('ERROR', "Unable to login to mic/pic even after {}secs".format(
                    self.mspmand_wait))
                raise Exception("Unable to login to mic/pic even after {}secs".format(
                    self.mspmand_wait))

            self.pic_type = self.get_pic_type(**kwargs)
            self.log('INFO', "PIC, {}, is online & UP".format(self.ifname))
        else:
            self.log(
                'INFO', "PIC, {}, is presumed to be online".format(self.ifname))

        if not self.pic_type:
            self.log('ERROR', "Failed to create the pic object for {}".format(self.ifname))
            raise Exception("Failed to create the pic object for {}".format(self.ifname))

        self.log('INFO', "Created pic object for {}".format(self.ifname))

        return True

    def is_pic_online_yet(self, wait_time=0, chk_interval=60):
        """Check if the pic is online or not.

        :param int wait_time:
            **OPTIONAL** Maximum time to wait for the pic to be online.

        :param int chk_interval:
            **OPTIONAL** Interrval for checking status of the pic to be online.
            Default is 60 secs

        :return: True if pic comes up online else raises RuntimeError exception

        :rtype: True or exception

        Example::

          Python:
            is_pic_online_yet()

          Robot:
            Is Pic Online Yet
        """

        iter_count = wait_time / chk_interval + 1
        is_pic_online = False

        iter_ii = 0
        while iter_ii < iter_count and not is_pic_online:
            self.log('INFO', "Waiting for login prompt to be available. \
                     {} of {} iterations".format(str(iter_ii + 1), iter_count))
            is_pic_online = self._login(login_to=chk_interval, login_to_ok=True,
                                        mspmand_to=chk_interval,
                                        mspmand_to_ok=True, err_lvl='I')
            if self.is_connected:
                self._logout()
            if is_pic_online:
                self.log('INFO', "Pic, {}, came online in {} secs".format(
                    self.ifname, (iter_ii + 1) * chk_interval))
                is_pic_online = True
            iter_ii += 1

        if not is_pic_online:
            self.log('ERROR', "Pic, {}, didn't come online even after {} secs".format(
                self.ifname, wait_time))
            raise RuntimeError("Pic, {}, didn't come online even after {} secs".format(
                self.ifname, wait_time))

        return is_pic_online

    def get_pic_type(self, err_lvl='ERROR'):
        """Return the pic type

        :param string err_lvl:
            **OPTIONAL** Log level at which the fail conditions need to be logged.
            Default is ERROR

        :return: Pic type if successful else None

        :rtype: string

        Example::

          Python:
            get_pic_type()

          Robot:
            Get Pic Type
        """

        self._dut_model = self.dh.get_model()
        self.log('INFO', "Router Model is : {}".format(self._dut_model))

        cmd = "show chassis pic fpc-slot {} pic-slot {}".format(self.fpc_slot, self.pic_slot)

        opts = {}
        opts['fpc'] = self.fpc_slot

        if self.is_vc:
            cmd += " member " + str(self._vc_mbr_id)

        data = self.get_fpc_pic_status(**opts)
        info = self.get_xml_output(cmd=cmd)

        if self.is_vc:
            info = info['multi-routing-engine-results']['multi-routing-engine-item']

        info = info['fpc-information']['fpc']

        self.pic_type = self.pic_state = None

        if 'pic-detail' in info:
            if 'pic-type' in info['pic-detail']:
                self.pic_type = info['pic-detail']['pic-type']
            if 'state' in info['pic-detail']:
                self.pic_state = info['pic-detail']['state']

        if self.pic_slot in data['pic']:
            if self.pic_type is None and 'type' in data['pic'][self.pic_slot]:
                self.pic_type = data['pic'][self.pic_slot]['type']

            if self.pic_state is None and 'state' in data['pic'][self.pic_slot]:
                self.pic_state = data['pic'][self.pic_slot]['state']
            if self.pic_state is None and 'state' in data['fpc']:
                self.pic_state = data['fpc']['state']

        self.fpc_type = data['descr']

        if self.pic_type is not None:
            self.log('INFO', "Pic Type of {} is {}".format(self.ifname, self.pic_type))
            self.log('INFO', "Pic state of {} is {}".format(self.ifname, self.pic_state))
            return self.pic_type
        else:
            self.log(err_lvl, "Unable to determine pic type of {}".format(self.ifname))
            return None

    def get_fpc_pic_status(self, **kwargs):
        """Return pics status of the FPC.

        :param int fpc:
            **OPTIONAL** FPC slot. Default is fpc slot of the current Pic

        :return: Dictionary containing the pic status.

        :rtype: dict

        Example::

          Python:
            pic_status = get_fpc_pic_status()
            pic_status = get_fpc_pic_status(fpc_slot=2)

          Robot:
            ${pic_status} =   Get FPC Pic Status
            ${pic_status} =   Get FPC Pic Status   fpc_slot=2

        Sample output::

              [cmd] show chassis fpc pic-status 0
                Slot 0   Online
                  PIC 0  Online       4x 10GE XFP
                  PIC 2  Online       MS-MIC-8G

        Output::

            {
                'pic': {
                    '0': {
                        'type': '4x 10GE XFP',
                        'state': 'Online'
                    },
                    '2': {
                        'type': 'MS-MIC-8G',
                        'state': 'Online'
                    }
                },
                'descr': {}
            }

        """

        fpc_slot = kwargs.get('fpc_slot', self.fpc_slot)

        cmd = "show chassis fpc pic-status {}".format(fpc_slot)
        if self.is_vc:
            cmd += " member " + str(self._vc_mbr_id)

        # self.dh.cli(command=cmd)
        inf = self.get_xml_output(cmd=cmd)

        if self.is_vc:
            inf = inf['multi-routing-engine-results']['multi-routing-engine-item']

        info = inf['fpc-information']['fpc']
        data = {}
        if 'description' in info:
            data['descr'] = info['description']
        if 'state' in info:
            data['fpc'] = {}
            data['fpc']['state'] = info['state']

        # Continue only if pic slot data is available in the output
        if 'pic' not in info:
            return data

        info = info['pic']
        entries = []
        if isinstance(info, list):
            entries.extend(info)
        else:
            entries.append(info)
        data['pic'] = {}
        for iter_nt in entries:
            data['pic'][iter_nt['pic-slot']] = {}
            if 'pic-type' in iter_nt:
                data['pic'][iter_nt['pic-slot']]['type'] = iter_nt['pic-type']
            if 'pic-state' in iter_nt:
                data['pic'][iter_nt['pic-slot']]['state'] = iter_nt['pic-state']

        return data

    #def check_pic_state(self, **kwargs):
    def check_pic_state(self, **kwargs):
        """Return state of PIC.

        :param string timeout:
            **OPTIONAL** Max wait time. Default is '60

        :param string state:
            **OPTIONAL** Pic state. Default is 'online'

        :return: True if successful else False

        :rtype: bool

        Example::

          Python:
            check_pic_state()

          Robot:
            Check Pic State
        """

        return self.check_fpc_pic_status(fpc=self.fpc_slot, pic=self.pic_slot, **kwargs)

    def login_to_pic(self, **kwargs):
        """Login to Pic

        :param string err_lvl:
            **OPTIONAL** Error level at which the fail conditions need to be printed.
            Default is ERROR

        :param bool login_to_ok:
            **OPTIONAL** Is it ok to timeout during login. Default is False

        :param int login_to:
            **OPTIONAL** Timeout for login. Default is 120

        :param bool mspmand_to_ok:
            **OPTIONAL** Is it ok to timeout while logging in to MSPMAND. Default is False

        :param int mspmand_to:
            **OPTIONAL** Timeout for logging into MSPMAND. Default is 60

        :return: True if successful else False

        :rtype: bool

        Example::

          Python:
            login_to_pic()

          Robot:
            Login To Pic
        """
        return self._login(**kwargs)

    def logout_from_pic(self):
        """logout for MPSDK Pic

        :return: True if successful else False

        :rtype: bool

        Example::

          Python:
            logout_from_pic()

          Robot:
            Logout From Pic
        """

        return self._logout()

    # For external usage
    def execute_command_on_pic(self, cmd=None, **kwargs):
        """Return output of the command executed

        :param string cmd:
            **REQUIRED** command to be executed

        :return: Output of the command

        :rtype: string

        Example::

          Python:
            execute_command_on_pic("clear msp pkt-cntrs")

          Robot:
            Execute Command On Pic   clear msp pkt-cntrs
        """

        if cmd is None:
            self.log('ERROR', "Missing mandatory parameter, cmd")
            raise TypeError("Missing mandatory parameter, cmd")

        return self._cmd(**kwargs)

    def execute_commands_on_pic(self, **kwargs):
        """Return output of the commands executed

        :param list cmds:
            **REQUIRED** List of commands to be executed

        :return: Output of the command

        :rtype: dict

        Example::

          Python:
            execute_commands_on_pic(cmds=["clear msp pkt-cntrs", "clear msp plugins pkt-cntrs"])

          Robot:
            @{cmd_list}   clear msp pkt-cntrs   clear msp plugins pkt-cntrs
            Execute Commands On Pic   cmds=@{cmd_list}
        """
        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'cmds' : []
                                           })

        self._login(**kwargs)

        output = {}

        for cmd in this['cmds']:
            self.log('INFO', "Executing {} ..".format(cmd))
            if self.is_mpsdk:
                resp = self.dh.cli(command=cmd, pattern=r"MSPMAND-CLI>").response()
            elif self.is_media:
                resp = self.dh.vty(name="fpc" + str(self.fpc_slot), command=cmd).response()
            else:
                resp = self.dh.cli(command=cmd, pattern=r".*#.*").response()

            output[cmd] = resp
            self.log("DEBUG", "output for {} is {}".format(cmd, output[cmd]))

        self._logout()

        return output


    @classmethod
    def reboot_pics(cls, **kwargs):
        """Reboot multiple pics

        """
        pass

    ################################################################
    # Get/Verify methods
    ################################################################
    def get_pic_memory_snapshot(self, **kwargs):
        """Return memory snapshot of the Pic as dict

        This routine takes a snapshot of the memory.
        It takes memory snapshot by executing 'show msp shm',
        'show msp shm jnx-msp-shm-data objcache', 'show msp shm mum' on the Pic and stores the
        output as hash.
        When daemon_list(optional) is mentioned, it takes the current memory for the daemons from
        'show system processes extensive | match <DaemonName>'

        :param string daemon_list:
            **OPTIONAL** List of Daemons for which memory leak has to be verified

        :return: Dictionary containing the memory snapshot

        :rtype: dict

        Example::

          Python:
            get_pic_memory_snapshot()

          Robot:
            Get Pic Memory Snapshot
        """

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'daemon_list' : []
                                           })
        self._login(**kwargs)

        self.log('INFO', "Taking Memory snapshot")
        shm_out = self.dh.cli(command="show msp mem usage",
                              pattern='MSPMAND-CLI>').response().split('\n')

        obj_out = self.dh.cli(command="show msp mem ocwm jnx-msp-shm-data mum objcache",
                              pattern="MSPMAND-CLI>").response().split('\n')

        mum_out = self.dh.cli(command="show msp mem ocwm jnx-msp-shm-data mum",
                              pattern="MSPMAND-CLI>").response().split('\n')

        #data = {}
        #data['shm'] = {}
        #data['objcache'] = {}
        #data['mum'] = {}
        #data['daemon'] = {}
        data = {'shm': {}, 'objcache': {}, 'mum': {}, 'daemon': {}}

        self.log('INFO', "Parsing command outputs")
        for line in shm_out:
            if re.search(r"SHM.*Allocated|\-{2,}", line, re.IGNORECASE):
                continue

            line = re.sub(r"\s{2,}", " ", line)
            #line = re.sub(r"-", "_", line)
            #out = line.split(" ")
            out = re.sub(r"-", "_", line).split(' ')
            data['shm'][out[0] + "_alloc"] = out[1]
            data['shm'][out[0] + "_free"] = out[2]
            data['shm'][out[0] + "_total"] = out[3]

        for line in obj_out:
            if re.search(r"Object cache.*Size|\-{2,}", line, re.IGNORECASE):
                continue
            line = re.sub(r"\s{2,}", " ", line)
            line = re.sub(r"-", "_", line)
            out = line.split(" ")
            data['objcache'][out[0] + "_alloc"] = out[3]


        for line in mum_out:
            if re.search(r"actual free space\s*=\s*(\d+)", line):
                data['mum']['act_free_space'] = out[3]

        self._logout()

        #if daemon_list is not None:
            #for dmn in daemon_list:
        for dmn in this['daemon_list']:
            resp = self.dh.cli(
                command="show system processes extensive | match {}".format(dmn)).response()
            output = resp.split("\n")
            for line in output:
                if "grep" in line:
                    continue
                if dmn in line:
                    line = re.sub(r"\s{2,}", " ", line)
                    info = line.split(" ")
                    match = re.search(r"(\d+)K$", info[6])
                    match1 = re.search(r"(\d+)M$", info[6])

                    if match:
                        data['daemon'][dmn + "_res"] = match.group(1) * 1024
                    elif match1:
                        data['daemon'][dmn + "_res"] = match1.group(1) * 1024

        self.log('INFO', "Memory snapshot : {} ".format(str(data)))

        return data

    def verify_pic_memory_snapshot(self, **kwargs):
        """Verify memory snapshot

        For a given memory snapshot taken before (ideally before the start of the testcase),
        this routine compares this with the current memory snapshot.

        :param dict before:
            **REQUIRED** Memory snapshot taken before, by calling get_pic_memory_snapshot

        :param list daemon_list:
            **OPTIONAL** List of Daemons for which memory leak has to be verified

        :param list ignore_list:
            **OPTIONAL** List of objs to be ignored while verifying the objs in use

        :param bool verify_shm:
            **OPTIONAL** Enable shm verification. Default is True

        :param bool verify_mum:
            **OPTIONAL** Enable mum verification. Default is True

        :param int tol_perc:
            **OPTIONAL** Tolerance percentage in verifying. Default is 1

        :param int tol_shm:
            **OPTIONAL** Tolerance value in verifying shm. Default is 0

        :return: Dictionary containing the memory snapshot

        :rtype: dict

        Example::

          Python:
            verify_pic_memory_snapshot()

          Robot:
            Verify Pic Memory Snapshot
        """

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'daemon_list': [],
                                               'ignore_list': [],
                                               'verify_shm': True,
                                               'verify_mum': True,
                                               'tol_shm': 0,
                                               'tol_perc': 1,
                                           })

        before = kwargs.get('before', {})

        #options = {}
        #if this['daemon_list']:
            #options['daemon_list'] = this['daemon_list']

        #after = self.get_pic_memory_snapshot(**options)
        after = self.get_pic_memory_snapshot(**kwargs)

        result = True
        _cmp_msg = "Comparing before and current memory snapshots"
        if this['verify_shm']:
            self.log('INFO', "{} for shm".format(_cmp_msg))
            result &= utils.cmp_dicts(exp_data=before['shm'], act_data=after['shm'],
                                      tol_perc=this['tol_shm'])

        if this['ignore_list']:
            for obj in before['objcache']:
                _msg = "For obj, {}, Objs in use".format(obj)
                if obj in this['ignore_list']:
                    self.log('INFO', "{}, Before : {}".format(_msg, before['objcache'][obj]))
                    self.log('INFO', "{}, Current : {}".format(_msg, after['objcache'][obj]))
                _msg += " before and current memory snapshots"
                if before['objcache'][obj] < after['objcache'][obj]:
                    self.log('ERROR', "{} are **NOT** same".format(_msg))
                    result &= False
                else:
                    self.log('ERROR', "{} **ARE** same".format(_msg))
        else:
            result &= utils.cmp_dicts(exp_data=before['objcache'], act_data=after['objcache'],
                                      tol_perc=this['tol_perc'])

        if this['verify_mum']:
            self.log('INFO', "{} for mum".format(_cmp_msg))
            result &= utils.cmp_dicts(exp_data=before['mum'], act_data=after['mum'],
                                      tol_perc=this['tol_perc'])

        if this['daemon_list']:
            self.log('INFO', "{} for daemons: {}".format(_cmp_msg, this['daemon_list']))
            result &= utils.cmp_dicts(exp_data=before['daemon'], act_data=after['daemon'],
                                      tol_perc=this['tol_perc'])

        return result


    def check_fpc_pic_status(self, **kwargs):
        """Check fpc pic status

        :param list fpc_list:
            **OPTIONAL** List of fpc's to be checked. Default is []

        :param list pic_list:
            **OPTIONAL** List of pic's to be checked. Default is []

        :param string state:
            **OPTIONAL** The expected state to be checked. Default is 'online|empty|spare'

        :param int timeout:
            **OPTIONAL** Total time to wait. Default is 0

        :param int interval:
            **OPTIONAL** interval to time to wait before next iteration . Default is True

        :param int node:
            **OPTIONAL** Speicific slot to be checked. Default is None

        :param string ignore:
            **OPTIONAL** The string based on which line to be ignored in the show command output.
                Default is 0

        :return: Dictionary containing the fpc and pic status and the veification status

        :rtype: tuple containing (bool, dict)

        Example::

          Python:
            check_fpc_pic_status()

          Robot:
            Check Fpc Pic Status
        """
        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'fpc_list': [],
                                               'pic_list': [],
                                               'state': 'online|empty|spare',
                                               'timeout':  0,
                                               'interval': 10,
                                               'node': None,
                                               'ignore': None,
                                           })
        self.log("INFO", "Checking FPC pic status")

        fpc_slot = this['fpc_list']
        pic_slot = this['pic_list']
        timeout = this['timeout']
        cmd = "show chassis fpc pic-status node " + \
            this['node'] if this[
                'node'] is not None else "show chassis fpc pic-status"
        if this['ignore'] is not None:
            match = re.search(r'\w+', this['ignore'])
            if match:
                cmd += ' | except "' + this['ignore']+'"'
        self.log("INFO", "Chechking for atleast one pic per each fpc slots")

        pic_interval = 20
        pic_timeout = this['timeout'] if this['timeout'] else 120
        while pic_timeout >= 0:
            online, offline = (0, 0)
            offline_slots = []
            pic_array = self.dh.cli(command=cmd).response()
            pic_array = pic_array.splitlines()
            iter_ii = 0
            while iter_ii < len(pic_array):
                tmp_iter_ii = iter_ii
                iter_ii += 1
                if pic_array[tmp_iter_ii] and re.search(r'^Slot (\d+)', pic_array[tmp_iter_ii]):
                    match = re.search(r'^Slot (\d+)', pic_array[tmp_iter_ii])
                    fpc_sl = match.group(1)
                    if fpc_slot:
                        if int(fpc_sl) not in fpc_slot:
                            continue
                    try:
                        if pic_array[tmp_iter_ii + 1] and re.search(r'PIC\s+(\d+)\s+(\w+)',
                                                                    pic_array[tmp_iter_ii + 1]):
                            online += 1
                    except IndexError:
                        self.log("INFO", "fpc slot {} does not have any pics available\
                            ".format(fpc_sl))
                        offline += 1
                        offline_slots.append(fpc_sl)

            if online and not offline:
                break
            pic_timeout = pic_timeout - pic_interval
            if pic_timeout >= 0 and offline:
                self.log("INFO", "Continue checking pics. Expire in ({}). seconds\
                    ".format(pic_timeout + pic_interval))
                time.sleep(pic_interval)
            elif offline:
                self.log("INFO", "fpc slots '{}' does not have any pics comeup, ingoring the slots\
                    ".format((",").join(offline_slots)))

        while timeout >= 0:
            slot = {}
            online, offline = (0, 0)
            fpc = ''
            # populate all PIC status info
            output = self.dh.cli(command=cmd).response()
            for line in output.splitlines():
                match = re.search(r'^Slot (\d+)', line)
                match1 = re.search(r'PIC\s+(\d+)\s+(\w+)', line)
                if match:
                    fpc = match.group(1)
                elif match1:
                    if fpc not in slot:
                        slot[fpc] = {}
                    slot[fpc][match1.group(1)] = match1.group(2)
            # check all PIC
            if not fpc_slot and not pic_slot:
                self.log("INFO", "Checking all pic slots")
                for fpc_sl in sorted(slot):
                    for pic_sl in sorted(slot[fpc_sl]):
                        match = re.search(
                            r''+this['state']+'', slot[fpc_sl][pic_sl], re.IGNORECASE)
                        if match:
                            self.log("DEBUG", "FPC {} PIC slot {} is {}\
                                ".format(fpc_sl, pic_sl, slot[fpc_sl][pic_sl]))
                            online += 1
                        else:
                            self.log("WARN", "FPC {} PIC slot {} is {}\
                                ".format(fpc_sl, pic_sl, slot[fpc_sl][pic_sl]))
                            offline += 1

            # check all pics from specified FPC slot(s)
            elif fpc_slot and not pic_slot:
                self.log(
                    "INFO", "Checking all pics from fpc slot {}".format(fpc_slot))
                for fpc_sl in sorted(slot):
                    if int(fpc_sl) not in fpc_slot:
                        continue
                    for pic_sl in sorted(slot[fpc_sl]):
                        match = re.search(
                            r''+this['state']+'', slot[fpc_sl][pic_sl], re.IGNORECASE)
                        if match:
                            self.log("DEBUG", "FPC {} PIC slot {} is {}\
                                ".format(fpc_sl, pic_sl, slot[fpc_sl][pic_sl]))
                            online += 1
                        else:
                            self.log("WARN", "FPC {} PIC slot {} is {}\
                                ".format(fpc_sl, pic_sl, slot[fpc_sl][pic_sl]))
                            offline += 1

            # check pic status from specified fpc(s) and pic slot(s)
            elif fpc_slot and pic_slot:
                self.log("INFO", "Checking pic {} from fpc {}".format(
                    pic_slot, fpc_slot))
                for fpc_sl in fpc_slot:
                    for pic_sl in pic_slot:
                        try:
                            match = re.search(r''+this['state']+'', slot[str(fpc_sl)][str(pic_sl)],
                                              re.IGNORECASE)
                            if match:
                                self.log("DEBUG", "FPC {} PIC slot {} is {}\
                                    ".format(fpc_sl, pic_sl, slot[str(fpc_sl)][str(pic_sl)]))
                                online += 1
                            else:
                                self.log("WARN", "FPC {} PIC slot {} is {}\
                                    ".format(fpc_sl, pic_sl, slot[str(fpc_sl)][str(pic_sl)]))
                                offline += 1
                        except KeyError:
                            self.log("WARN", "FPC {} PIC slot {} is not valid\
                                ".format(fpc_sl, pic_sl))
            if online and not offline:
                break
            timeout = timeout - this['interval']
            if timeout < 0:
                break
            self.log("TRACE", "Continue checking states. Expire in {} seconds\
                ".format(timeout + this['interval']))
            time.sleep(this['interval'])

        if online and not offline:
            self.log("INFO", "All found matching {}".format(this['state']))
            return (True, slot)
        elif offline:
            self.log("ERROR", " {} pics not matching  {}".format(
                offline, this['state']))
        # Removing below 2 lines Not offline and not online condition will never hit as
        # if a pic is not in the given state it is automatically offline
        # else :
        #     self.log("WARN", "No information found" )
        return (False, slot)

    ################################################################
    # local methods
    ################################################################
    def _login(self, **kwargs):
        """Local method to login to the pic"""

        def _chk_status(self, status, err_lvl):
            if not status:
                self.is_connected = False
                self.log(err_lvl, "Unable to login to {}".format(self.ifname))
                if 'ERROR' in err_lvl.upper():
                    raise RuntimeError("Unable to login to {}".format(self.ifname))

        if self.is_media:
            # Nothing to do here for media pic
            return True

        this = utils.update_opts_from_args(kwargs,
                                           defaults={
                                               'err_lvl': 'ERROR',
                                               'login_to_ok': False,
                                               'login_to': 120,
                                               'mspmand_to_ok': False,
                                               'mspmand_to': 60,
                                           })

        status = True

        self.log('INFO', "Logging on to MSPIC")
        if self.is_vmsmpc:
            cmd = "ssh routing-instance __juniper_private1__ {}".format(self._ri_ip)
            status &= self.dh.shell(cmd='rm -f /var/home/regress/.ssh/known_hosts').status()
            status &= self.dh.cli(command=cmd, pattern=r'.*Are you sure.*|.*password:.*/',
                                  timeout=this['login_to'],
                                  timeout_ok=this['login_to_ok']).status()
            #if not status:
                #self.log(this['err_lvl'], "Unable to login to {}".format(self.ifname))
                #return False
            _chk_status(self, status, this['err_lvl'])
            status &= self.dh.cli(cmd="yes", pattern=r'.*password:.*', timeout=20).status()
        else:
            cmd = "telnet routing-instance __juniper_private1__ {}".format(self._ri_ip)
            status &= self.dh.cli(command=cmd, pattern=r'.*login:.*',
                                  timeout=this['login_to'],
                                  timeout_ok=this['login_to_ok']).status()
        #if not status:
            #self.is_connected = False
            #self.log(this['err_lvl'], "Unable to login to {}".format(self.ifname))
            #return False

        _chk_status(self, status, this['err_lvl'])

        status &= self.dh.cli(command="root", pattern=r'root.*').status()
        #if status:
            #self.is_connected = True

        self._kill_mspdbg()

        if self.is_mpsdk_dbgm:
            self.cmd = 'mspdbg-cli -s'
            status &= self.dh.cli(command=self.cmd, pattern=r"MSP-DEBUG>",
                                  timeout=this['mspmand_to'],
                                  timeout_ok=this['mspmand_to_ok']).status()
        elif self.is_vmsmpc:
            tmp = " mspmand" if self.is_qosmos else ""
            self.cmd = "/usr/share/pfe/" + "mspdbg-cli -p" + tmp + " -s"
            status &= self.dh.cli(command=self.cmd, pattern=r"MSPMAND-CLI>",
                                  timeout=this['mspmand_to'],
                                  timeout_ok=this['mspmand_to_ok']).status()
        else:
            tmp = " mspmand" if self.is_qosmos else ""
            self.cmd = "mspdbg-cli -p" + tmp + " -s"
            status &= self.dh.cli(command=self.cmd, pattern=r"MSPMAND-CLI>",
                                  timeout=this['mspmand_to'],
                                  timeout_ok=this['mspmand_to_ok']).status()

        #if not status:
            #self.log(this['err_lvl'], "Unable to login to {}".format(self.ifname))
            #if 'ERROR' in this['err_lvl'].upper():
                #raise RuntimeError("Unable to login to {}".format(self.ifname))

        _chk_status(self, status, this['err_lvl'])

        self.is_connected = True
        self.log('INFO', "Logged in to {}".format(self.ifname))
        self.is_loggedin = True

        return True

    def _logout(self):
        if self.is_media:
            # Nothing to do here for media pic
            return True

        if self.is_mpsdk:
            self.log('INFO', "Logging out from MPSDK-PIC")
            if self.is_loggedin:
                self.dh.cli(command='quit', pattern=r'root.*')
        else:
            self.log('INFO', "Logging out from PIC")

        if self.is_connected:
            return self.dh.cli(command="exit")
        else:
            return True

    def _cmd(self, cmd=None, **kwargs):
        """Return output of the command executed"""

        timeout = kwargs.get('timeout', 180 if 'mx80' in self._dut_model else 60)

        if not self._login(**kwargs):
            return None

        prompt = 'sp' + str(self.fpc_slot) + str(self.pic_slot)

        self.log('INFO', "Executing {} ..".format(self.cmd))

        if self.is_mpsdk_dbgm:
            output = self.dh.cli(command=cmd, timeout=timeout,
                                 pattern=r'MSP-DEBUG>').response()
        elif self.is_mpsdk:
            output = self.dh.cli(command=cmd, timeout=timeout,
                                 pattern=r'MSPMAND-CLI>').response()
        elif self.is_media:
            output = self.dh.vty(name="fpc"+ str(self.fpc_slot),
                                 timeout=timeout, cmd=cmd).response()
        else:
            output = self.dh.cli(command=cmd, timeout=timeout,
                                 pattern=prompt + r".*#.*").response()
        self.log("DEBUG", "output in _cmd is {}".format(output))

        self._logout()

        return output

    def _kill_mspdbg(self):
        """Kill mspdbg process"""

        self.dh.cli(command="ps -a | grep mspdbg-cli", pattern=r"root.*", wait=2)
        output = self.dh.cli(command="ps -a | grep mspdbg-cli",
                             pattern=r"root.*", wait=2).response()
        output = output.splitlines()
        for line in output:
            if 'grep' in line:
                continue
            if 'mspdbg-cli' in line:
                line = re.sub(r"\s{2,}", "", line)
                line = re.sub(r"^\s", "", line)
                info = line.split(' ')
                pid = info[0]
                self.log("Going to kill mspdbg with pid {}".format(pid))
                self.dh.cli(command="kill -9 "+str(pid), pattern=r'root.*')

    def _update(self, **kwargs):
        """Update the object with the parameters passed"""

        for attr in kwargs:
            self.ptr[attr] = kwargs[attr]
