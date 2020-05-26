# coding: UTF-8
"""Functions/Keywords to Configure IKE on SRX/VSRX devices"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_ike(device=None, gateway=None, gw_address=None, gw_advpn=None, gw_dead_peer=None, gw_dynamic=None,
                  gw_ext_interface=None, gw_general_ikeid=False, gw_ike_policy=None, gw_local_address=None,
                  gw_local_id=None, gw_nat_keepalive=None, gw_no_nat_traversal=False, gw_remote_identity=None,
                  gw_v1_only=False, gw_v2_only=False, gw_xauth_profile=None,
                  policy=None, certificate=None, mode=None, proposal_set=None, proposals=None, pre_shared_key=None,
                  reauth_frequency=None,
                  proposal=None, auth_algo=None, auth_method=None, dh_group=None, enc_algo=None, lifetime_sec=None,
                  respond_bad_spi=None, commit=False):
    """
    Configuring IKE for srx/vsrx series(set security ike...)

    :Example:

    python: configure_ike(device=r0, gateway='gw1', gw_address='10.10.10.10')


    :param Device device: Handle of the device on which configuration has to be executed.
        **REQUIRED**
    :param str gateway: Gateway name
        *OPTIONAL*
    :param str gw_address: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_advpn: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_dead_peer: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_dynamic: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_ext_interface: Use with ``gateway`` parameter
        *OPTIONAL*
    :param bool gw_general_ikeid: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_ike_policy: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_local_address: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_local_id: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_nat_keepalive: Use with ``gateway`` parameter
        *OPTIONAL*
    :param bool gw_no_nat_traversal: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_remote_identity: Use with ``gateway`` parameter
        *OPTIONAL*
    :param bool gw_v1_only: Use with ``gateway`` parameter
        *OPTIONAL*
    :param bool gw_v2_only: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str gw_xauth_profile: Use with ``gateway`` parameter
        *OPTIONAL*
    :param str policy: Policy Name
        *OPTIONAL*
    :param str certificate: Use with ``policy`` parameter
        *OPTIONAL*
    :param str mode: Use with ``policy`` parameter
        *OPTIONAL*
    :param str proposal_set: Use with ``policy`` parameter
        *OPTIONAL*
    :param str proposals: Use with ``policy`` parameter
        *OPTIONAL*
    :param str pre_shared_key: Use with ``policy`` parameter
        *OPTIONAL*
    :param str reauth_frequency: Use with ``policy`` parameter
        *OPTIONAL*
    :param str proposal: Proposal Name
        *OPTIONAL*
    :param str auth_algo: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str auth_method: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str dh_group: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str enc_algo: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str lifetime_sec: Use with ``proposal`` parameter
        *OPTIONAL*
    :param str respond_bad_spi: Respond to IPSec packets with bad SPI values
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
    prefix = 'set security ike '

    if gateway is not None:
        cmd_prefix = prefix + 'gateway ' + gateway + ' '
        if gw_address is not None:
            commands.append(cmd_prefix + 'address ' + gw_address)
        if gw_advpn is not None:
            commands.append(cmd_prefix + 'advpn ' + gw_advpn)
        if gw_dead_peer is not None:
            commands.append(cmd_prefix + 'dead-peer-detection ' + gw_dead_peer)
        if gw_dynamic is not None:
            commands.append(cmd_prefix + 'dynamic ' + gw_dynamic)
        if gw_ext_interface is not None:
            commands.append(cmd_prefix + 'external-interface ' + gw_ext_interface)
        if gw_general_ikeid:
            commands.append(cmd_prefix + 'general-ikeid')
        if gw_ike_policy is not None:
            commands.append(cmd_prefix + 'ike-policy ' + gw_ike_policy)
        if gw_local_address is not None:
            commands.append(cmd_prefix + 'local-address ' + gw_local_address)
        if gw_local_id is not None:
            commands.append(cmd_prefix + 'local-identity ' + gw_local_id)
        if gw_nat_keepalive is not None:
            commands.append(cmd_prefix + 'nat-keepalive ' + gw_nat_keepalive)
        if gw_no_nat_traversal:
            commands.append(cmd_prefix + 'no-nat-traversal')
        if gw_remote_identity is not None:
            commands.append(cmd_prefix + 'remote-identity ' + gw_remote_identity)
        if gw_xauth_profile is not None:
            commands.append(cmd_prefix + 'xauth access-profile ' + gw_xauth_profile)
        if gw_v1_only:
            commands.append(cmd_prefix + 'version v1-only')
        if gw_v2_only:
            commands.append(cmd_prefix + 'version v2-only')

    if policy is not None:
        cmd_prefix = prefix + 'policy ' + policy + ' '
        commands.append(cmd_prefix)
        if certificate is not None:
            commands.append(cmd_prefix + 'certificate ' + certificate)
        if mode is not None:
            commands.append(cmd_prefix + 'mode ' + mode)
        if proposal_set is not None:
            commands.append(cmd_prefix + 'proposal-set ' + proposal_set)
        if proposals is not None:
            commands.append(cmd_prefix + 'proposals ' + proposals)
        if pre_shared_key is not None:
            commands.append(cmd_prefix + 'pre-shared-key ' + pre_shared_key)
        if reauth_frequency is not None:
            commands.append(cmd_prefix + 'reauth-frequency ' + reauth_frequency)

    if proposal is not None:
        cmd_prefix = prefix + 'proposal ' + proposal + ' '
        commands.append(cmd_prefix)
        if auth_algo is not None:
            commands.append(cmd_prefix + 'authentication-algorithm ' + auth_algo)
        if auth_method is not None:
            commands.append(cmd_prefix + 'authentication-method ' + auth_method)
        if dh_group is not None:
            commands.append(cmd_prefix + 'dh-group ' + dh_group)
        if enc_algo is not None:
            commands.append(cmd_prefix + 'encryption-algorithm ' + enc_algo)
        if lifetime_sec is not None:
            commands.append(cmd_prefix + 'lifetime-seconds ' + lifetime_sec)

    if respond_bad_spi is not None:
        commands.append(prefix + 'respond-bad-spi ' + respond_bad_spi)

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