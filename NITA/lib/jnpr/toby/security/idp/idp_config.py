"""
IDP configuration
"""


def configure_idp_security_package(device=None, mode="set", commit=True, **kwargs):
    """
    Configure the idp security package
    Example :-
        idp_configure_security_package(device=dh, url="https://devdb.juniper.net/cgi-bin/index.cgi")
        idp_configure_security_package(device=dh, ignore_version_check=True,
                source_address="srxdpi-vsrx17", automatic="enable", start_time="2016-09-08.12:10",
                interval="200", commit=False)
        idp_configure_security_package(device=dh, mode="delete")

    ROBOT Example:
        IDP Configure Security Package   device=${dh}   url=https://devdb.juniper.net/index.cgi
        IDP Configure Security Package   device=${dh}   ignore_version_check=${True}
                source_address=srxdpi-vsrx17   automatic=enable   start_time=2016-09-08.12:10
                interval=200   commit={False}
        IDP Configure Security Package   device=${dh}   mode=delete

    :param Device device:
        **REQUIRED** Device Handle of the DUT
    :param str mode:
        *OPTIONAL* Configuration mode
        ``Supported values``: set or delete
        ``Default value``   : set
    :param str url:
        *OPTIONAL* URL of idp custom signature package. Default is to use URL defined in the
        topology file, otherwise configuration ignored
    :param str source_address:
        *OPTIONAL* Source address to be used for sending download request.
    :param bool ignore_version_check:
        *OPTIONAL* Enabling install ignore-version-check, configured if it is True
    :param str automatic:
        *OPTIONAL* Enabling the automatic download of signature update.
        ``Supported values``: "enable"
    :param str start_time:
        *OPTIONAL* Automatic signature udpate start time passed in the format YYYY-MM-DD.HH:MM
    :param str interval:
        *OPTIONAL* Automatic update interval in hours (24...336)
    :param bool commit:
        *OPTIONAL* To commit the configuration.
        ``Supported values``: True and False
        ``Default value``   : True
    :return returns True if successful
    :rtype bool
    """
    if device is None:
        raise ValueError("Argument: device is mandatory")

    # Initialize variables
    url = kwargs.get('url', "")
    source_address = kwargs.get('source_address', "")
    start_time = kwargs.get('start_time', "")
    interval = kwargs.get('interval', "")
    ignore_version_check = kwargs.get('ignore_version_check', False)
    automatic = kwargs.get('automatic', "")
    # Set configurations as empty values if delete has to be performed.
    if mode == "delete":
        url = ""
        source_address = ""
        start_time = ""
        interval = ""

    cfg_node = mode + " security idp security-package "
    cmdlist = []
    if url != "" or (url == "" and mode == "delete" and 'url' in kwargs):
        device.log(level="INFO", message="idp URL is %s" % url)
        cmdlist.append(cfg_node + "url " + url)
    if 'source_address' in kwargs:
        cmdlist.append(cfg_node + "source-address " + source_address)
    if ignore_version_check is True:
        cmdlist.append(cfg_node + "install ignore-version-check")
    if 'automatic' in kwargs:
        cmdlist.append(cfg_node + "automatic " + automatic)
    if 'start_time' in kwargs:
        cmdlist.append(cfg_node + "automatic start-time " + start_time)
    if 'interval' in kwargs:
        cmdlist.append(cfg_node + "automatic interval " + interval)

    # delete complete secuirty-package node if no specific configuration is available
    if mode == "delete" and len(cmdlist) == 0:
        cmdlist = [cfg_node]

    # Configure and commit the configuration
    device.config(command_list=cmdlist)
    if commit is True and len(cmdlist) != 0:
        device.commit()
    return True
