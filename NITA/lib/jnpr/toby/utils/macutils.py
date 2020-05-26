"""This module contains methods for various MAC address related operations

"""

import re

#__author__ = ['Sudhir Akondi']
#__contact__ = 'sudhira@juniper.net'
#__copyright__ = 'Juniper Networks Inc.'
#__date__ = '2017'

def generate_mac_addresses(first_mac=None, number_of_macs=None):
    """Generates a list of MAC addresses incrementally from a base mac address

    Python Example:
      mac = "e8:b6:c2:cc:7c:40"
      list_of_mac = generate_mac_addresses(first_mac=mac, number_of_macs=10)

    Robot Example:
      ${mac}        Set Variable  e8:b6:c2:cc:7c:40
      ${list_mac}   Generate MAC Addresses   first_mac=${mac}  number_of_macs=${10}

    :param first_mac:
        **REQUIRED** The the first mac address in the list.
    :param number_of_macs:
        **REQUIRED** The number of mac addresses, starting from the first_mac, that you want returned
    """

    _match_ = re.match(r"\S\S:\S\S:\S\S:\S\S:\S\S:\S\S", first_mac)
    if _match_ is None:
        raise Exception("Format of option first_mac is not a valid mac address")

    number_of_macs = int(number_of_macs)
    if number_of_macs < 0:
        raise Exception("Option number_of_macs must be greater than 0")

    flat_first_mac = "0x" + first_mac.replace(":","")
    integer_first_mac = int(flat_first_mac,0)

    _return_list_ = []
    while number_of_macs > 0:

        hex_mac = hex(integer_first_mac)[2:].zfill(12)

        if hex_mac == 'ff:ff:ff:ff:ff:ff' :
            raise Exception("List of MACs hit the end limit ff:ff:ff:ff:ff:ff. Please specify a lesser number")

        _return_list_.append("{}{}:{}{}:{}{}:{}{}:{}{}:{}{}".format(*hex_mac))

        integer_first_mac += 1
        number_of_macs = number_of_macs - 1

    return _return_list_

