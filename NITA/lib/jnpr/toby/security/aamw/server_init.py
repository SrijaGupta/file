import ipaddress

import jnpr.toby.security.aamw.setup.protocol_server_init as protocol_init


SERVER_DICT = {
    'http': protocol_init.init_http_server,
    # 'https': server_init,
    'smtp': protocol_init.init_smtp_server,
    'smtps': protocol_init.init_smtps_server,
    'smtp_tls': protocol_init.init_smtp_tls_server,
    'imap': protocol_init.init_imap_server,
    'imaps': protocol_init.init_imaps_server,
    'imap_tls': protocol_init.init_imap_tls_server,
}

SAMPLE_IP_CONFIG = {
    'h0_r0_if': 'eth1',
    'h0_r0_ip': '13.0.0.1',
    'h0_r0_ipv6': '',

    'r0_h0_if': '',
    'r0_h0_ip': '13.0.0.254',
    'r0_h0_ipv6': '',

    'h1_r0_if': 'eth1',
    'h1_r0_ip': '14.0.0.1',
    'h1_r0_ipv6': '',

    'r0_h1_if': '',
    'r0_h1_ip': '14.0.0.254',
    'r0_h1_ipv6': '',

    'ip_mask': 8,
    'ipv6_mask': 64,
}


def init_aamw_linux(client_handle, server_handle, protocol='http',
                    ip_v6=False, ip_config_dict=None, **kwargs):
    """
    """
    # init ip and route
    _pc_init_network(client_handle, server_handle, inet6=ip_v6,
                     ip_config_dict=ip_config_dict)

    # set server
    server_init_func = SERVER_DICT.get(protocol.lower(), None)
    assert server_init_func, \
        'Invalid protocol name: {protocol}. Valid protocols ' \
        '{servers}'.format(protocol=protocol, servers=str(list(SERVER_DICT)))
    server_init_func(server_handle, **kwargs)
    server_handle.log('Server initiation completed')


def _pc_init_network(client_handle, server_handle,
                     inet6=False, ip_config_dict=None):
    """"""
    if not ip_config_dict:
        client_handle.log('Not finding IP config. Using default config.')
        ip_config_dict = SAMPLE_IP_CONFIG
    client_handle.log('IP config: %s' % ip_config_dict)
    if inet6:
        _single_init_network(client_handle,
                             src_if=ip_config_dict['h0_r0_if'],
                             src_ipv4=ip_config_dict['h0_r0_ip'],
                             src_ipv6=ip_config_dict['h0_r0_ipv6'],
                             dest_ipv4=ip_config_dict['h1_r0_ip'],
                             dest_ipv6=ip_config_dict['h1_r0_ipv6'],
                             gw_ipv4=ip_config_dict['r0_h0_ip'],
                             gw_ipv6=ip_config_dict['r0_h0_ipv6'],
                             ipv4_mask=ip_config_dict['ip_mask'])
        _single_init_network(server_handle,
                             src_if=ip_config_dict['h1_r0_if'],
                             src_ipv4=ip_config_dict['h1_r0_ip'],
                             src_ipv6=ip_config_dict['h1_r0_ipv6'],
                             dest_ipv4=ip_config_dict['h0_r0_ip'],
                             dest_ipv6=ip_config_dict['h0_r0_ipv6'],
                             gw_ipv4=ip_config_dict['r0_h1_ip'],
                             gw_ipv6=ip_config_dict['r0_h1_ipv6'],
                             ipv4_mask=ip_config_dict['ip_mask'])
    else:
        _single_init_network(client_handle,
                             src_if=ip_config_dict['h0_r0_if'],
                             src_ipv4=ip_config_dict['h0_r0_ip'],
                             dest_ipv4=ip_config_dict['h1_r0_ip'],
                             gw_ipv4=ip_config_dict['r0_h0_ip'],
                             ipv4_mask=ip_config_dict['ip_mask'],
                             ipv6_mask=ip_config_dict['ipv6_mask'])
        _single_init_network(server_handle,
                             src_if=ip_config_dict['h1_r0_if'],
                             src_ipv4=ip_config_dict['h1_r0_ip'],
                             dest_ipv4=ip_config_dict['h0_r0_ip'],
                             gw_ipv4=ip_config_dict['r0_h1_ip'],
                             ipv4_mask=ip_config_dict['ip_mask'],
                             ipv6_mask=ip_config_dict['ipv6_mask'])
    return True


def _single_init_network(client_handle, src_if,
                         src_ipv4, dest_ipv4, gw_ipv4, ipv4_mask,
                         src_ipv6=None, dest_ipv6=None,
                         gw_ipv6=None, ipv6_mask=None):
    """"""
    # check input valid
    src_ipv4 = str(ipaddress.IPv4Address(src_ipv4))
    dest_ipv4 = str(ipaddress.IPv4Network(dest_ipv4 + '/' + str(ipv4_mask),
                                          strict=False))
    gw_ipv4 = str(ipaddress.IPv4Address(gw_ipv4))

    # set route
    client_handle.su()
    client_handle.log('Restart network...')
    client_handle.shell(command='/sbin/ifconfig %s down' % src_if, timeout=300)
    client_handle.log('Config IP and route...')
    client_handle.shell(command='/sbin/ifconfig {interface} {ipv4} up'.format(
        interface=src_if, ipv4=src_ipv4), timeout=300)
    client_handle.shell(command='/sbin/route add -net {dest_ipv4} gw '
                        '{gw_ipv4}'.format(dest_ipv4=dest_ipv4,
                                           gw_ipv4=gw_ipv4),
                        timeout=300)
    if all([src_ipv6, dest_ipv6, gw_ipv6, ipv6_mask]):
        # check input valid
        src_ipv6 = str(ipaddress.IPv6Address(src_ipv6))
        dest_ipv6 = str(ipaddress.IPv6Network(dest_ipv6 + '/' + str(ipv6_mask),
                                              strict=False))
        gw_ipv6 = str(ipaddress.IPv6Address(gw_ipv6))

        # set route
        client_handle.log('Config IPv6 and route...')
        client_handle.shell(command='/sbin/ifconfig {interface} inet6 add '
                            '{ipv6}'.format(interface=src_if,
                                            ipv6=src_ipv6),
                            timeout=300)
        client_handle.shell(command='/sbin/route -A inet6 add {dest_ipv6} gw '
                            '{gw_ipv6}'.format(dest_ipv6=dest_ipv6,
                                               gw_ipv6=gw_ipv6),
                            timeout=300)
    client_handle.log('Network configuration done')
    return True


def init_argon_devices(client_handle, client_config, 
                       server_handle, server_config, 
                       protocol='http', **kwargs):
    """
    """
    # init ip and route
    _init_device_network(client_handle, client_config)
    _init_device_network(server_handle, server_config)

    # set server
    server_init_func = SERVER_DICT.get(protocol.lower(), None)
    if server_init_func is None:
        err_msg = 'Invalid protocol name: {protocol}. Valid protocols ' \
                  '{servers}'.format(protocol=protocol,
                                     servers=str(list(SERVER_DICT)))
        server_handle.log('ERROR', err_msg)
        raise ValueError(err_msg)
    server_init_func(server_handle, **kwargs)
    server_handle.log('Server initiation completed')


def _init_device_network(device_handle, device_config):
    """"""
    device_handle.log('IP config: %s' % device_config)

    src_if = device_config['src_if']
    src_ipv4 = device_config['src_ipv4']
    dests_ipv4 = device_config['dests_ipv4']
    gw_ipv4 = device_config['gw_ipv4']
    ipv4_mask = device_config['ipv4_mask']

    # check input valid
    src = str(ipaddress.IPv4Address(src_ipv4))
    device_handle.log('%r' % src)
    dests = [str(ipaddress.IPv4Network(
        dest + '/' + str(ipv4_mask), strict=False)) for dest in dests_ipv4]
    device_handle.log('%r' % dests)
    gw = str(ipaddress.IPv4Address(gw_ipv4))
    device_handle.log('%r' % gw)

    # set route
    device_handle.su()
    device_handle.log('Restart network...')
    device_handle.shell(command='/sbin/ifconfig %s down' % src_if, timeout=300)
    device_handle.log('Config IP and route...')
    device_handle.shell(
        command='/sbin/ifconfig {interface} {ipv4} up'.format(
            interface=src_if, ipv4=src), timeout=300)
    for dest in dests:
        device_handle.shell(
            command='/sbin/route add -net {dest} gw {gw}'.format(
                dest=dest, gw=gw), timeout=300)

    return True
