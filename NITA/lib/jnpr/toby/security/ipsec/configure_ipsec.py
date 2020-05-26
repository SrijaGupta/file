# coding: UTF-8
"""Functions/Keywords to Configure IP Security on SRX/VSRX devices"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_ipsec(device=None, policy=None, policy_proposal=None, policy_proposal_set=None, pfs_keys=None,
                    proposal=None, auth_algo=None, enc_algo=None, lifetime_kb=None,lifetime_sec=None, protocol=None,
                    security_association=None,
                    vpn=None, bind_interface=None, copy_outer_dscp=False, df_bit=None, establish_tunnels=None,
                    ike_gateway=None, ike_idle_time=None, ike_install_interval=None, ike_ipsec_policy=None,
                    ike_no_anti_replay=False, ike_proxy_id=None, manual=None,
                    traffic_selector=None, local_ip=None, remote_ip=None,
                    vpn_monitor_optimized=False, vpn_monitor_dst_ip=None, vpn_monitor_src_interface=None,
                    vpn_monitor_interval=None, vpn_monitor_threshold=None,
                    commit=False):
    """
    Configuring IPSEC for srx/vsrx series(set security ipsec...)

    :Example:

    python: configure_ipsec(device=r0, policy='p1', commit=False)


    :param Device device: Handle of the device on which configuration has to be executed.
        **REQUIRED**
    :param str policy: Policy Name
        *OPTIONAL*
    :param str policy_proposal:  Use with ``policy`` parameter
        *OPTIONAL*
    :param str policy_proposal_set:  Use with ``policy`` parameter
        *OPTIONAL*
    :param str pfs_keys:  Use with ``policy`` parameter
        *OPTIONAL*
    :param str proposal: Proposal Name
        *OPTIONAL*
    :param str auth_algo: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str enc_algo: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str lifetime_kb: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str lifetime_sec: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str protocol: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str security_association: Security association set command options
        *OPTIONAL*
    :param str vpn: VPN name
        *OPTIONAL*
    :param str bind_interface: Use with ``vpn`` parameter
        *OPTIONAL*
    :param bool copy_outer_dscp: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str df_bit: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str establish_tunnels: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str ike_gateway: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str ike_idle_time: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str ike_install_interval: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str ike_ipsec_policy: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str book ike_no_anti_replay: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str ike_proxy_id: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str manual: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str traffic_selector:  Use with ``vpn`` parameter
        *OPTIONAL*
    :param str local_ip: Use with ``vpn`` & ``traffic_selector`` parameter
        *OPTIONAL*
    :param str remote_ip: Use with ``vpn`` & ``traffic_selector`` parameter
        *OPTIONAL*
    :param bool vpn_monitor_optimized: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str vpn_monitor_dst_ip: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str vpn_monitor_src_interface: Use with ``vpn`` parameter
        *OPTIONAL*
    :param str vpn_monitor_interval: VPN Monitor Interval
        *OPTIONAL*
    :param str vpn_monitor_threshold: VPN Monitor Threshold
        *OPTIONAL*
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when correct configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring routing options")

    commands = []
    prefix = 'set security ipsec '

    if policy is not None:
        cmd_prefix = prefix + 'policy ' + policy + ' '
        commands.append(cmd_prefix)
        if policy_proposal is not None:
            commands.append(cmd_prefix + 'proposals ' + policy_proposal)
        if policy_proposal_set is not None:
            commands.append(cmd_prefix + 'proposal-set ' + policy_proposal_set)
        if pfs_keys is not None:
            commands.append(cmd_prefix + 'perfect-forward-secrecy keys ' + pfs_keys)

    if proposal is not None:
        cmd_prefix = prefix + 'proposal ' + proposal + ' '
        commands.append(cmd_prefix)
        if auth_algo is not None:
            commands.append(cmd_prefix + 'authentication-algorithm ' + auth_algo)
        if enc_algo is not None:
            commands.append(cmd_prefix + 'encryption-algorithm ' + enc_algo)
        if lifetime_kb is not None:
            commands.append(cmd_prefix + 'lifetime-kilobytes ' + lifetime_kb)
        if lifetime_sec is not None:
            commands.append(cmd_prefix + 'lifetime-seconds ' + lifetime_sec)
        if protocol is not None:
            commands.append(cmd_prefix + 'protocol ' + protocol)

    if security_association is not None:
        cmd_prefix = prefix + 'security-association ' + security_association + ' '
        commands.append(cmd_prefix)

    if vpn is not None:
        cmd_prefix = prefix + 'vpn ' + vpn + ' '
        if bind_interface is not None:
            commands.append(cmd_prefix + 'bind-interface ' + bind_interface)
        if copy_outer_dscp:
            commands.append(cmd_prefix + 'copy-outer-dscp ')
        if df_bit is not None:
            commands.append(cmd_prefix + 'df-bit ' + df_bit)
        if establish_tunnels is not None:
            commands.append(cmd_prefix + 'establish-tunnels ' + establish_tunnels)
        if ike_gateway is not None:
            commands.append(cmd_prefix + 'ike gateway ' + ike_gateway)
        if ike_idle_time is not None:
            commands.append(cmd_prefix + 'ike idle-time ' + ike_idle_time)
        if ike_install_interval is not None:
            commands.append(cmd_prefix + 'ike install-interval ' + ike_install_interval)
        if ike_ipsec_policy is not None:
            commands.append(cmd_prefix + 'ike ipsec-policy ' + ike_ipsec_policy)
        if ike_no_anti_replay:
            commands.append(cmd_prefix + 'ike no-anti-replay ')
        if ike_proxy_id is not None:
            commands.append(cmd_prefix + 'ike proxy-identity ' + ike_proxy_id)
        if manual is not None:
            commands.append(cmd_prefix + 'manual ' + manual)
        if traffic_selector is not None:
            cmd_prefix = cmd_prefix + 'traffic-selector ' + traffic_selector + ' '
            commands.append(cmd_prefix)
            if local_ip is not None:
                commands.append(cmd_prefix + 'local-ip ' + local_ip)
            if remote_ip is not None:
                commands.append(cmd_prefix + 'remote-ip ' + remote_ip)
        if vpn_monitor_optimized:
            commands.append(cmd_prefix + 'vpn-monitor optimized ')
        if vpn_monitor_dst_ip is not None:
            commands.append(cmd_prefix + 'vpn-monitor destination-ip ' + vpn_monitor_dst_ip)
        if vpn_monitor_src_interface is not None:
            commands.append(cmd_prefix + 'vpn-monitor source-interface ' + vpn_monitor_src_interface)

    if vpn_monitor_interval is not None:
        commands.append(prefix + 'vpn-monitor-options interval ' + vpn_monitor_interval)
    if vpn_monitor_threshold is not None:
        commands.append(prefix + 'vpn-monitor-options threshold ' + vpn_monitor_threshold)

    # Executing the config commands
    if len(commands) != 0:
        device.log(level='DEBUG', message='Configuration commands gathered from the function: ')
        device.log(level='DEBUG', message=commands)
        device.config(command_list=commands)

        # Committing the config if asked by user
        if commit:
            return device.commit(timeout=60)
        else:
            return True
    else:
        device.log(level='ERROR', message='Incorrect set of parameters are provided. '
                                          'Kindly go through the documentation and examples.')
        raise Exception(
            'Incorrect set of parameters are provided. Kindly go through the documentation and examples.')
