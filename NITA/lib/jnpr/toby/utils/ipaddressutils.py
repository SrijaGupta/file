"""This module contains methods for various IP address operations.

"""

from ipaddress import ip_network
from jnpr.toby.engines.config.config_utils import make_list

__author__ = ['Dan Bond']
__contact__ = 'dbond@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2016'


def generate_host_address(subnet_address: str, number_of_addresses: int, address_option=None, no_mask=False, mask=None,
                          return_iterator=False):
    """Returns the first or last host address of a given subnet.

    :param subnet_address:
        **REQUIRED** The subnet address for which you want to retrieve host addresses.
    :param number_of_addresses:
        **REQUIRED** The number of host addresses desired. Cannot exceed the maximum number of hosts possible within
        a given subnet_address, else the function returns False
    :param address_option:
        **REQUIRED** String value of either "first" or "last". This option forces the method to return the first or last
        available host address in the given subnet_address.
    :param no_mask:
        *OPTIONAL* If set to true, returns any addresses without their subnet masks attached.
    :param mask:
        *OPTIONAL* User can set mask explicitly, else IPv4 defaults to 24 and IPv6 defaults to 64.
    param return_iterator:
        *OPTIONAL* Method will return an iterator rather than a list. An iterator will not be returned when the user
        sets the address_option parameter because this parameter implies a single address return value
    :return:
        Returns False if user requested too many addresses
                A list OR iterator of all host addresses in subnet_address if user sets address_option=None
                The first host address in subnet_address if address_option="first"
                The last host address in subnet_address of address_option="last"
    """

    # Assign default values for the mask based on what type of address was passed (IPv6 will contain a ':')
    if mask is None:
        if ':' in subnet_address:
            # IPv6 address
            mask = 64
        else:
            # IPv4 address
            mask = 24

    # Make sure requested number of addresses doesn't exceed address space of the subnet
    if ':' in subnet_address:
        # IPv6 address
        number_of_host_bits = 128 - mask
    else:
        # IPv4 address
        number_of_host_bits = 32 - mask

    total_available_host_addresses = 2 ** number_of_host_bits - 2

    if number_of_addresses > total_available_host_addresses:
        # Error case where user requests more addresses than available in the designated subnet
        t.log('error', "Please request a valid number of host addresses from your subnet.\n"
                       "Subnet: {}\nRequested number of addresses: {}\nNumber of addresses available in subnet:"
                       " {}".format(subnet_address, number_of_addresses, total_available_host_addresses))
        return False

    # Append the mask to the base address
    my_ip_address = subnet_address + "/" + str(mask)

    ip_array = [str(x) for x in ip_network(my_ip_address).hosts()]

    # Slice list based on desired number_of_addresses
    ip_array = ip_array[0:number_of_addresses]

    # Add masks to addresses if no_mask == False
    if not no_mask:
        ip_array = [str(x) + "/" + str(mask) for x in ip_array]

    # Process address_options
    if address_option == "first":
        return ip_array[0]
    if address_option == "last":
        return ip_array[-1]

    # Convert list to iterator if user prefers
    if return_iterator:
        return iter(ip_array)
    else:
        return ip_array


def generate_subnet_addresses(first_address: str, number_of_addresses: int, mask=None, return_iterator=False):
    """Generates a list or iterator of subnet address strings from first_address.

    :param first_address:
        **REQUIRED** The the first subnet address you want. Subsequent subnets are added in-order based on
        number_of_addresses requested by user
    :param number_of_addresses:
        **REQUIRED** The number of subnets, starting from the first_address, that you want returned
    :param mask:
        *OPTIONAL* The mask for your desired subnets. IPv4 default is 24. IPv6 default is 64.
    :param return_iterator:
        *OPTIONAL* If set to true, list of subnet strings is converted to an iterator before returning.
    :return: An iterator or list containing the number of subnet strings requested by the user.
    """

    # Set default mask values if needed
    if mask is None:
        if ':' in first_address:
            # IPv6 address
            mask = 64
        else:
            # IPv4 address
            mask = 24

    address_with_mask = first_address + "/" + str(mask)
    subnet_ip_generator = make_list(first=address_with_mask, count=number_of_addresses, step=None, last=None,
                                    repeat=1, cycle=number_of_addresses)

    if return_iterator:
        return iter(subnet_ip_generator)
    else:
        return list(subnet_ip_generator)

def __ip_to_int(ip):
    '''
    This method convert ip address to integer
    :param:
        REQUIRED ip: ip address value to be converted
    :return:
        Returns integer value of given ip address
    Example:
        __ip_to_int('192.168.1.1')
    '''

    ip_add = ip.split('.')
    ip_add = list(map(int, ip_add))
    if len(ip_add) < 4:
        print("Invalid ip address: %s" % ip)
        return None
    _int = ip_add[0] * 16777216 + ip_add[1] * 65536 \
        + ip_add[2] * 256 + ip_add[3]
    return _int

def mask2cidr(mask):
    '''
    This method convert mask to cidr
    :param:
        REQUIRED mask: subnet mask value to be converted
    :return:
        cidr value of given mask
    '''

    if mask == '0.0.0.0':
        return 0
    return (sum([bin(int(x)).count("1") for x in mask.split(".")]))
