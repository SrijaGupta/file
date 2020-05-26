#! /usr/bin/python3
"""
Keyword to configure or delete global address book for security
"""

def address_book_config(device=None, mode="set", **kwargs):
    """
    To configure and delete address book config.
    Example:
        address_book_config(device=srx, addr_name="addr_name", ip_prefix="5.0.0.1/32", commit=False)
        address_book_config(device=srx, addr_name="addr_name", ip_prefix="2002::1/128")
        address_book_config(device=srx, mode="delete", addr_name="addr_name",ip_prefix="5.0.0.1/32")
        address_book_config(device=srx, addr_set="addr_name", addr_set_name="addrsetname")
        address_book_config(device=srx, mode="delete")
    Robot Example:
        address book config    device=${dut}    addr_name=addr_name    ip_prefix=6.0.0.1/32
            commit=${False}
        address book config    device=${dut}    addr_name=addrname    domain_name=facebook.com
        address book config    device=${dut}    addr_set=addrset    addr_set_name=addrsetname

    :param Device device:
        **REQUIRED** Device handle for srx
    :param str mode:
        *OPTIONAL* Device configuration mode
            ``Supported values``: set or delete
            ``Default value``   : set
    :param str addr_name:
        **REQUIRED** security address name for address
    :param str addr_set:
        **REQUIRED** security address-set name for address-set
    :param str ip_prefix:
        **REQUIRED** ip address with prefix is required for the address
    :param list addr_set_name:
        **REQUIRED** address-set-name list is required for the address-set
        Address_set profile list should be configured earlier to before calling here
    :return:True on Success
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    addr_name = kwargs.get('addr_name', None)
    addr_set = kwargs.get('addr_set', None)
    ip_prefix = kwargs.get('ip_prefix', None)
    addr_set_name = kwargs.get('addr_set_name', [])
    domain_name = kwargs.get('domain_name', None)
    commit = kwargs.get('commit', True)

    cmdlist = []
    cmd = mode + ' security address-book global'
    if mode == "delete" and addr_name is None and addr_set is None:
        cmdlist.append(cmd)
    else:
        if addr_name is not None:
            if ip_prefix is not None:
                cmdlist.append(cmd +' address ' + addr_name + ' ' + ip_prefix)
            elif domain_name is not None:
                cmdlist.append(cmd + ' address ' + addr_name + ' dns-name ' + domain_name)
            else:
                device.log(level="Error", message="Either ip_prefix or domain_name is a mandatory"
                           " argument for addr_name")
                raise Exception("Either ip_prefix or domain_name is a mandatory argument"
                                " for addr_name")
        if addr_set is not None:
            if len(addr_set_name) != 0:
                for name in addr_set_name:
                    cmdlist.append(cmd + ' address-set ' + addr_set + ' address-set ' + name)
            else:
                device.log(level="Error", message="addr_set_name is a mandatory argument"
                           " for addr_set")
                raise Exception("addr_set_name is a mandatory argument for addr_set")

    device.config(command_list=cmdlist)
    if commit is True:
        device.commit()
