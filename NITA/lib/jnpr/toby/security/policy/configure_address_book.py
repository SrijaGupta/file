# coding: UTF-8
"""Functions/Keywords to Configure Address-book"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements


__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_address_book(device=None, address_book_name=None, addresses=None, address_set_name=None,
                           address_set=None, attach_zone=None, logical_systems=None, commit=False):
    """
    Configuring an address-book(set security address-book...)
                               (set logical-systems lsys1 security address-book...)

    :Example:

    python:  configure_address_book(device=r0, address_book_name='global',
                                    addresses={'source': '10.10.10.2/32', 'dest': '20.20.20.2/32'}, commit=False)

             configure_address_book(device=r0, address_book_name='global', address_set_name='v4_set',
                                    address_set=['source1', 'source2', 'source3'], commit=False)

             configure_address_book(device=r0, address_book_name='global', attach_zone='trust', commit=False)

             configure_address_book(device=r0, address_book_name='global', logical_systems='LSYS1',
                                    addresses={'source': '10.10.10.2/32', 'dest': '20.20.20.2/32'}, commit=False)

    robot:  &{addresses} =    Create Dictionary    source=10.10.10.2/32    dest=20.20.20.2/32
            Configure Address Book    device=${r0}    address_book_name=global    addresses=${addresses}
            ...    attach_zone=trust    commit=${True}

            ${address_set} =    Create List    trust_a_v4_spec_0    trust_a_v4_spec_1    source    dest
            Configure Address Book    device=${r0}    address_book_name=global    address_set_name='trust_a_addset_v4'
            ...    address_set=${address_set}

    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str address_book_name:
        **REQUIRED**  Name of the address_book.
    :param dict addresses:
        *OPTIONAL*  Addresses to be configured into address-book. Default value: addresses=None
                    key should be the address name and value should be the ip address.
    :param str address_set_name:
        *OPTIONAL*  Name of address set to be configured. Default value: address_set_name=None
    :param list address_set:
        *OPTIONAL*  Name of addresses to be configured in address set. Default value: address_set=None
                    This option is required to configure address-set. Should contain list of address names.
    :param str attach_zone:
        *OPTIONAL*  Zone to be attached. Default value: attach_zone=None
    :param str logical_systems:
        *OPTIONAL*  Logical System name. Default value: logical_systems=None
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when address-book configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring an application")
    if address_book_name is None:
        device.log(level="ERROR", msg="'address_book_name' is a mandatory parameter for configuring an address-book")
        raise Exception("'address_book_name' is a mandatory parameter for configuring an address-book")

    commands = []

    if logical_systems is not None:
        cmd_prefix = 'set logical-systems ' + logical_systems + ' security address-book ' + address_book_name + ' '
    else:
        cmd_prefix = 'set security address-book ' + address_book_name + ' '

    if addresses is not None:
        if isinstance(addresses, dict):
            for key, value in addresses.items():
                commands.append(cmd_prefix + 'address ' + key + ' ' + value)
        else:
            device.log(level="ERROR", msg="'addresses' parameter should be a dictionary")
            raise Exception("'addresses' parameter should be a dictionary")

    if attach_zone is not None:
        commands.append(cmd_prefix + 'attach zone ' + attach_zone)

    if address_set_name is not None:
        if address_set is not None and isinstance(address_set, list):
            for address_name in address_set:
                commands.append(cmd_prefix + 'address-set ' + address_set_name + ' address ' + address_name)
        else:
            device.log(level="ERROR", msg="'address_set' parameter should be a list of address names "
                                          "when configuring address-set")
            raise Exception("'address_set' parameter should be a list of address names "
                            "when configuring address-set")
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
