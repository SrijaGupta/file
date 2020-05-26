"""
NFX related keywords
"""
import re



def get_flowd_mapping(device=None):
    """
    To get mapping from heth-x-x to ge-x/x/x on Porter box according to the configuration.
    Example -
        get_flowd_mapping(device=dut)

    ROBOT Example:
        Get Flowd Mapping    device=${dut}

    :param str device:
         **REQUIRED** Device handle for Linux host
    :returns: dictionary with mapping (key-heth-x-x, value-ge-x/x/x)
    :rtype: dict
    """
    if device is None:
        raise ValueError("device is a mandatory argument")

    if not re.search(".*NFX.*", device.get_model().upper(), re.DOTALL):
        device.log(level="ERROR", message="This keyword is only for NFX box")
        raise ValueError("This keyword is only for NFX box")

    status = device.cli(command="show configuration | display set | no-more | grep virtualization-options")\
        .response()

    mapping_dict = {}
    for line in status.splitlines():
        match = re.search(".*interfaces\\s(.*)\\smapping\\sinterface\\s(.*)", line, re.DOTALL)
        if not match:
            continue
        mapping_dict[match.group(2)] = match.group(1)

    if not mapping_dict:
        device.log(level="INFO", message="No mapping found from heth to ge-x/x/x, "
                                         "returning Empty dictionary")
    return mapping_dict
