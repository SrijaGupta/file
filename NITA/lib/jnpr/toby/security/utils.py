"""
Utilities
"""

import re


def get_vty_counters_as_dictionary(device=None, command=None, pic_name=None):
    """
    To return the dictionary for counter names and their hit counts, from a VTY output
    Example:
        get_vty_counters_as_dictionary(device=device, pic_name="fpc0.pic1",
                                   command="show usp jsf counters junos-ssl-policy")

    ROBOT Example:
        Get vty counters as Dictionary   device=${device}   pic_name=fpc0.pic1
                                        command=${"show usp jsf counters junos-ssl-policy"}

    :param device:
        **REQUIRED** Device handle of the DUT
    :param command:
        **REQUIRED** Command which returns the Output as Counter names and hit counts
    :param pic_name:
        *OPTIONAL* To get the Counter values from a particular PIC. If not provided, Added value of
        hit counts from all the PICs will be returned.
    :return: Dictionary (key=counter name, value=hit count)
    :rtype: dict
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if command is None:
        device.log(level="ERROR", message="'command' is a mandatory argument")
        raise ValueError("'command' is a mandatory argument")

    pic_to_be_parsed = []
    dict_to_return = {}

    if pic_name is not None:
        pic_to_be_parsed.append(pic_name)
    else:
        pic_to_be_parsed = device.get_srx_pfe_names()

    # Once all the keys in the dictionary are created, this becomes 1
    flag = 0

    for pic in pic_to_be_parsed:
        response = device.vty(command=command, destination=pic).response().splitlines()
        for line in response:
            match = re.search("(^\\s+)?(.*)\\s+:\\s+([0-9]+)$", line, re.DOTALL)
            if not match:
                match = re.search("(^\\s+)?(.*):\\s+([0-9]+)$", line, re.DOTALL)
                if not match:
                    match = re.search("(^\\s+)?(.*)\\s+([0-9]+)$", line, re.DOTALL)


            if match:
                counter_name = match.group(2).strip()
                hit_count = int(match.group(3))
                if flag == 1:
                    dict_to_return[counter_name] = hit_count + dict_to_return[counter_name]
                else:
                    dict_to_return[counter_name] = hit_count
        flag = 1

    return dict_to_return
