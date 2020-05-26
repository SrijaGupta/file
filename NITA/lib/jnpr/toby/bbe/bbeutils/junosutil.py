"""This module defines a class for retrieving DUT subscriber information and other system properties
from devices running JUNOS.
"""

import re
import time
import collections
from jnpr.toby.bbe.version import get_bbe_version
from jnpr.toby.bbe.errors import BBEDeviceError

__author__ = ['Yong Wang']
__contact__ = 'ywang@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'
__version__ = get_bbe_version()

# For robot framework
ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
ROBOT_LIBRARY_VERSION = get_bbe_version()


_SubscribersCount = collections.namedtuple('SubscribersCount', 'total, \
                                                               active')
_SubscribersCount.__doc__ = """Junos device subscribers count.

Subscribers count data returned by 'show subscribers count <options>'
E.g.,
root@r100mx960wf> show subscribers count
Total subscribers: 40000, Active Subscribers: 40000

Fields:
    total: integer, Total subscribers.
    active: integer, Active Subscribers.
"""


class BBEJunosUtil:
    """Junos utility class

    """
    # default is r0
    DEFAULT_DEVICE = 'r0'

    # Junos device handle
    router_handle = None

    @classmethod
    def _check_handle(cls):
        """Check device handle.

        When the class is loaded, device handle may not be available from
        initialization. No problem. Each method call MUST check handle first.
        If handle is not set yet, obtain the handle from t and set it.

        By default, this class uses device 'r0' handle. If another handle
        is desired, call set_handle() to set it explicitly.

        :return: None
        """
        if not cls.router_handle:
            handle = t.get_handle(resource=cls.DEFAULT_DEVICE)
            if not handle:
                raise BBEDeviceError('Failed to obtain device handle for {}'.format(cls.DEFAULT_DEVICE))
            cls.router_handle = handle

    @classmethod
    def set_bbe_junos_util_device_handle(cls, handle):
        """Set Junos device handle object.

        By default this class uses 'r0' handle. This method can be used
        to explicitly let the class use another device handle.

        The method name is made verbose intentionally to avoid Robot keyword conflict.

        :param h: Junos device handle object
        :return: None
        """
        cls.router_handle = handle

    @classmethod
    def get_subscriber_count(cls, **kwargs):
        """Get subscribers count.

        Note:
        There is trade-off for functionality and ease-of-use here. This method
        use kwargs to support almost all options to get subscribers, but care need to
        be taken when passing parameters with hyphen in them.
        As junos keywords may contain hyphen (-), such as 'client-type',
        but Python does not allow hyphen in keywords, you should use the following
        extra step and syntax to workaround:
            - create a dictionary for your parameters, e.g.,
                sub_dict = {'client-type':'dhcp', 'routing-instance':'retailer1'}
            - pass the dict as parameter to the call, e.g.
                count = BBEJunosUtil.get_subscriber_count(**sub_dict)

        Usage example:
            # Get subscribers count for dhcp in retailer1 routing instance
            >>> from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
            >>> sub_dict = {'client-type':'dhcp', 'routing-instance':'retailer1'}
            >>> count = BBEJunosUtil.get_subscriber_count(**sub_dict)
            >>> count.active
            1000
            >>> count.total
            1000

            # Get subscribers count for all subscribers, you don't need to pass in anything
            >>> from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil
            >>> count = BBEJunosUtil.get_subscriber_count()
            >>> count.total
            40000
            >>> count.active
            40000
            >>> count
            SubscribersCount(total=40000, active=40000)

        :param kwargs: Optional. Junos compatible completions and values after 'show subscribers count'
        :return: Instance of namedtuple _SubscribersCount.
        """
        cls._check_handle()

        # create command
        rpc_cmd = '<get-subscribers><count/>'
        for (key, value) in kwargs.items():
            rpc_cmd += '<{}>{}</{}>'.format(key, value, key)
        rpc_cmd += '</get-subscribers>'

        # execute command
        resp = cls.router_handle.execute_rpc(command=rpc_cmd).resp

        # process response
        total = resp.findtext('subscriber/number-of-subscribers').strip()
        total = int(total) if total else 0
        active = resp.findtext('subscriber/number-of-active-subscribers').strip()
        active = int(active) if total else 0

        return _SubscribersCount(total, active)

    @classmethod
    def get_pppoe_subscriber_count(cls, routing_instance=None):
        """Get pppoe subscribers count

        Very convenient method.
        This method calls get_subscriber_count(). Please refer detailed doc there.

        :param ri: String. Optional. Routing instance name.
        :return:
        """
        client_type = {'client-type': 'pppoe'}

        if routing_instance:
            client_type['routing-instance'] = routing_instance

        return cls.get_subscriber_count(**client_type)

    @classmethod
    def get_dhcp_subscriber_count(cls, routing_instance=None):
        """Get dhcp subscribers count

        Very convenient method.
        This method calls get_subscriber_count(). Please refer detailed doc there.

        :param ri: String. Optional. Routing instance name.
        :return:
        """
        client_type = {'client-type': 'dhcp'}

        if routing_instance:
            client_type['routing-instance'] = routing_instance

        return cls.get_subscriber_count(**client_type)

    @classmethod
    def get_vlan_subscriber_count(cls, routing_instance=None):
        """Get vlan subscribers count

        Very convenient method.
        This method calls get_subscriber_count(). Please refer detailed doc there.

        :param ri: String. Optional. Routing instance name.
        :return:
        """
        client_type = {'client-type': 'vlan'}

        if routing_instance:
            client_type['routing-instance'] = routing_instance

        return cls.get_subscriber_count(**client_type)

    @classmethod
    def get_vlan_oob_subscriber_count(cls, routing_instance=None):
        """Get l2bsa subscribers count

        Very convenient method.
        This method calls get_subscriber_count(). Please refer detailed doc there.

        :param ri: String. Optional. Routing instance name.
        :return:
        """
        client_type = {'client-type': 'vlan-oob'}

        if routing_instance:
            client_type['routing-instance'] = routing_instance

        return cls.get_subscriber_count(**client_type)

    @classmethod
    def get_l2tp_subscriber_count(cls, routing_instance=None):
        """Get l2tp subscribers count

        Very convenient method.
        This method calls get_subscriber_count(). Please refer detailed doc there.

        :param ri: String. Optional. Routing instance name.
        :return:
        """
        client_type = {'client-type': 'l2tp'}

        if routing_instance:
            client_type['routing-instance'] = routing_instance

        return cls.get_subscriber_count(**client_type)

    @classmethod
    def get_subscriber_count_by_state(cls, state='active', client_type=None, routing_instance=None):
        """Get subscribers count by subscriber-state

        Very convenient method.
        This method calls get_subscriber_count(). Please refer detailed doc there.

        subscriber-state:
            Possible completions:
              active               ACTIVE state only
              configured           CONFIGURED state only
              init                 INIT state only
              terminated           TERMINATED state only
              terminating          TERMINATING state only

        client-type:
            Possible completions:
              dhcp                 DHCP clients only
              dot1x                Dot1x clients only
              essm                 ESSM clients only
              fwauth               FwAuth clients only
              l2tp                 L2TP clients only
              mlppp                MLPPP clients only
              ppp                  PPP clients only
              pppoe                PPPoE clients only
              static               Static clients only
              vlan                 VLAN clients only
              vpls-pw              VPLS-PW clients only
              xauth                XAuth clients only

        Usage example:
            >>> c = BBEJunosUtil.get_subscriber_count_by_state(state='configured')
            >>> c.total
            0

            >>> terming = BBEJunosUtil.get_subscriber_count_by_state('terminating')
            >>> terming.total
            0

        :param state: String. Optional. Default to 'active'
        :param ri: String. Optional. Routing instance name.
        :return:
        """
        subs_state = {'subscriber-state': state}

        if client_type:
            subs_state['type'] = client_type
        if routing_instance:
            subs_state['routing-instance'] = routing_instance

        return cls.get_subscriber_count(**subs_state)

    @classmethod
    def cpu_settle(cls, cpu_threshold=50, idle_min=50, dead_time=600, interval=10):
        """Check and wait device CPU to settle down to specified utilization level.

        CPU is considered settle if 2 consecutive checks all satisfy the given condition.

        On a multiple CPU system, 'idle' utilization is scaled down to 100% by the
        factor of number of CPUs. For example, on a 4 CPU RE, if 'idle' is 360%,
        it is scaled down to 360/4 = 90%. This scaled down value is compared with
        idle_min to check satisfaction of the condition.

        Other process's CPU util value is not scaled down to compare with cpu_threshold.

        TODO:
            EssThree cpu_settle allow output to to file. This feature will be implemented
            if required in the future.

        Usage example:
            from jnpr.toby.bbe.bbeutils.junosutil import BBEJunosUtil

            # Use all default settings
            BBEJunosUtil.cpu_settle()

            # Use customized settings
            BBEJunosUtil.cpu_settle(cpu_threshold=10, idle_min=90, dead_time=1200, interval=20)

        :param cpu_threshold: integer percentage. The maximum ANY process running can consume.
        :param idle_min: integer percentage. The minimum amount of idle CPU available.
        :param dead_time: integer in seconds. Max amount of time to wait for cpu to settle or cpu to idle.
        :param interval: integer in seconds. Interval between cpu utilization checks.
        :param write_data_file: boolean.
        :return: None. May raise BBEDeviceError if CPU settle failed.
        """
        cls._check_handle()

        # shell command used to check number of RE CPUs
        # example output: 'hw.ncpu: 4'
        cmd_n_cpu = 'sysctl hw.ncpu'
        # cli command to check processes
        cmd_proc = 'show system processes extensive | no-more'
        # maximum rounds of CPU check
        n_rounds = int(dead_time / interval)
        # cpu settel log messages prefix
        log_prefix = '[CPU SETTLE]'
        # re to match process
        proc_re = re.compile(r'(\d+\.\d+)\%\s+(\w+)')

        t.log('{} Started'.format(log_prefix))

        # Check number of CPUs on the system (RE)
        try:
            ncpu_query = cls.router_handle.shell(command=cmd_n_cpu).resp
            number_of_cpus = int(ncpu_query.split()[1])
            t.log('{} Found {} CPUs'.format(log_prefix, number_of_cpus))
        except:
            raise BBEDeviceError('Failed to find number of CPUs on RE by {}'.format(cmd_n_cpu))

        # CPU is considered settle if 2 consecutive checks all satisfy the given condition
        start_time = time.time()
        idle_satisfied = 0
        proc_satisfied = 0

        # show processes to extract CPU utils
        while n_rounds > 0:
            n_rounds -= 1
            idle_resp = cls.router_handle.cli(command='show system processes extensive | grep idle |count').resp
            idle_count = int(idle_resp.split()[1])
            procs = cls.router_handle.cli(command=cmd_proc).resp
            procs_list = procs.split('\r\n')

            # find process and idle
            idle_found = False
            proc_found = False
            idle_cpu = 0
            for process in procs_list:
                match = proc_re.search(process)
                if match:
                    proc_cpu = float(match.groups()[0])
                    proc_name = match.groups()[1]
                    if proc_name == 'idle':
                        idle_count -= 1
                        idle_found = True
                        idle_cpu += int(proc_cpu/number_of_cpus)
                        if idle_count > 0:
                            continue
                        if idle_cpu >= idle_min:
                            idle_satisfied += 1
                            t.log('{} idle is using {:.2f} cpu, satisfied idle min {}'.format(log_prefix,
                                                                                              idle_cpu,
                                                                                              idle_min))
                        else:
                            idle_satisfied = 0
                            proc_satisfied = 0
                            t.log('{} idle is using {:.2f} cpu, dissatisfied idle min {}'.format(log_prefix,
                                                                                                 proc_cpu,
                                                                                                 idle_min))
                    else:
                        proc_found = True
                        if proc_cpu <= cpu_threshold:
                            if idle_satisfied:
                                proc_satisfied += 1
                            t.log('{} {} is using {:.2f} cpu, satisfied threshold {}'.format(log_prefix,
                                                                                             proc_name,
                                                                                             proc_cpu,
                                                                                             cpu_threshold))
                        else:
                            idle_satisfied = 0
                            proc_satisfied = 0
                            t.log('{} {} is using {:.2f} cpu, dissatisfied threshold {}'.format(log_prefix,
                                                                                                proc_name,
                                                                                                proc_cpu,
                                                                                                cpu_threshold))

                    # both idle and the highest cpu process are processed
                    if idle_found and proc_found:
                        break

            # stop checking as condition is satisfied, idle maybe larger than proc if proc is checked first
            if idle_satisfied >= 2 and proc_satisfied == 2:
                break
            t.log('current idle_satisfied value is {} , proc_satisfied value is {}'.format(idle_satisfied, proc_satisfied))
            t.log('{} Wait {} seconds and check again'.format(log_prefix, interval))
            time.sleep(interval)

        # finally check if cpu settle is successful or out of time
        if idle_satisfied >= 2 and proc_satisfied == 2:
            settle_time = int(time.time() - start_time)
            t.log('{} CPU settle successfully in {} seconds'.format(log_prefix, settle_time))
        else:
            t.log('{} CPU failed to settle'.format(log_prefix))
            raise BBEDeviceError('CPU settle failed')
