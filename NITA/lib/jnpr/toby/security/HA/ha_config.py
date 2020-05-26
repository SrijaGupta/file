# coding: UTF-8
"""Functions/Keywords to Configure redundancy groups and reth interfaces"""

__author__ = ['Usha Kiran']
__contact__ = 'ushak@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_redundancy_group(device=None, reth_count=None, redundancy_group=None,
                               node0_priority=None, node1_priority=None, preempt=False,
                               interface_monitor=None, interface_weight=None, ip_monitoring=None,
                               global_weight=None, global_threshold=None, retry_interval=None,
                               retry_count=None, ipmonitor_address=None, ip_weight=None,
                               interface_name=None, secondary_ip_address=None, commit=False):
    """

    :param device:
    :param reth_count:
    :param redundancy_group:
    :param node0_priority:
    :param node1_priority:
    :param preempt:
    :param interface_monitor:
    :param interface_weight:
    :param ip_monitoring:
    :param global_weight:
    :param global_threshold:
    :param retry_interval:
    :param retry_count:
    :param ipmonitor_address:
    :param ip_weight:
    :param interface_name:
    :param secondary_ip_address:
    :param commit:
    :return:
    """

    if device is None:
        raise Exception("'device' is mandatory parameter device handle")
    if redundancy_group is None:
        raise Exception("'redundancy group' is mandatory parameter device handle")
    if device is not None and reth_count is not None:
        device.config(command_list=['set chassis cluster reth-count ' + str(reth_count)])
    if redundancy_group is not None:
        cmd = 'set chassis cluster redundancy-group ' + str(redundancy_group)
    if preempt:
        device.config(command_list=[cmd + ' preempt'])

    if node0_priority is not None and node1_priority is not None:
        device.config(command_list=[cmd + ' node 0 priority ' + str(node0_priority),
                                    cmd + ' node 1 priority ' + str(node1_priority)])

    if interface_monitor is not None and interface_weight is not None:
        device.config(command_list=[cmd + ' interface-monitor ' + interface_monitor +
                                    ' weight ' + str(interface_weight)])

    if ip_monitoring:
        cmd_ip = 'set chassis cluster redundancy-group ' + str(redundancy_group) + ' ip-monitoring'

    if retry_count is not None and retry_interval is not None and global_weight is not None\
            and global_threshold is not None:
        device.config(command_list=[cmd_ip + ' retry-count ' + str(retry_count) + ' retry-interval '
                                    + str(retry_interval) + ' global-weight ' + str(global_weight) +
                                    ' global-threshold ' + str(global_threshold)])

    if ipmonitor_address is not None and ip_weight is not None and interface_name is not None\
            and secondary_ip_address is not None:
        device.config(command_list=[cmd_ip + ' family inet ' + ipmonitor_address + ' weight '
                                    + str(ip_weight) + ' interface ' + interface_name +
                                    ' secondary-ip-address ' + secondary_ip_address])

        # Committing the config if asked by user

    if commit is True:
        return device.commit(timeout=60)
    else:
        return True

def configure_reth(device=None, node0_link=None, node1_link=None, reth_interface_name=None,
                   reth_address=None, redundancy_group=None, unit='0',
                   vlan_tagging=False, vlan_id=None,
                   inet_mode='inet', commit=False):
    """
    :param device:
    :param node0_link:
    :param node1_link:
    :param reth_interface_name:
    :param reth_address:
    :param redundancy_group:
    :param vlan_tagging:
    :param vlan_id:
    :param unit:
    :param inet_mode:
    :param commit:
    :return:
    """
    if device is None:
        raise Exception("'device' is mandatory parameter")

    if device is not None:
        cmd = 'set interfaces '

    if node0_link is not None and node1_link is not None and reth_interface_name is not None:
        device.config(command_list=[cmd + node0_link + ' gigether-options redundant-parent '
                                    + reth_interface_name, cmd + node1_link +
                                    ' gigether-options redundant-parent ' + reth_interface_name])

    if reth_address is not None and unit is not None and redundancy_group is not None\
            and inet_mode is not None:
        device.config(command_list=[cmd + reth_interface_name + ' unit ' + unit +
                                    ' family ' + inet_mode + ' address ' + reth_address,
                                    cmd + reth_interface_name + ' redundant-ether-options'
                                                                ' redundancy-group '
                                    + str(redundancy_group)])
    if vlan_tagging:
        device.config(command_list=[cmd + reth_interface_name + ' vlan-tagging'])
    if vlan_id is not None:
        device.config(command_list=[cmd + reth_interface_name + ' unit ' + unit +
                                    ' vlan-id ' + vlan_id])
        # Committing the config if asked by user

    if commit is True:
        return device.commit(timeout=60)
    else:
        return True
