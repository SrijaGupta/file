"""
 DESCRIPTION:   Keyword for UTM feature.
      AUTHOR:   Suchi Pallai, spallai@juniper.net
     COMPANY:   Juniper Networks
"""


def check_utm_ewf_status(device=None, server="juniper_enhanced", status="UP"):
    """
    To check web-filtering status in UTM.
    Example:
        check_web_filtering_status(device=device)

    Robot Example:
        check web filtering status    device=${dut)    status=DOWN
        check web filtering status    device=${dut)    server=websense_redirect

    :param Device device:
        **REQUIRED** Device handle for junox box

    :param str server:
        *OPTIONAL* UTM server. Valuses are "junper_enahanced", "juniper_local" "websense_redirect"
        ``Default Value``: juniper_enhanced

    :return: On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    device_resp = device.cli(command="show security utm web-filtering status | match "
                                     "Server").response()

    if server == "juniper_enhanced":
        if "Juniper Enhanced" in device_resp:
            if status in device_resp:
                device.log(level="INFO", message="websense server is " + status)
            else:
                device.log(level="Error", message="websense server is  not " + status)
                raise Exception("UTM status is not expected here")
        else:
            device.log(level="Error", message="Juniper Enhanced profile is not enabled")
            raise Exception("Juniper Enhanced profile is not enabled")
    elif server == "websense_redirect":
        if "Websense Redirect" in device_resp:
            if status in device_resp:
                device.log(level="INFO", message="websense server is " + status)
            else:
                device.log(level="Error", message="websense server is  not " + status)
                raise Exception("UTM status is not expected here")
        else:
            device.log(level="Error", message="Websense Redirect profile is not enabled")
            raise Exception("Websense Redirect profile is not enabled")
    elif server == "juniper_local":
        if "Juniper local" in device_resp:
            device.log(level="INFO", message="Juniper local is up")
        else:
            device.log(level="Error", message="Juniper Local is not up")
            raise Exception("UTM status is not expected here")
    return True


def clear_utm_cache(device=None):
    """
    TO clear utm cache in device
    Example:
        clear_utm_cache(device=device)

    Robot Example:
        clear utm cache    device=${dut}

    :param Device device:
        **REQUIRED** Device handle for junox box

    :return:  On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    device_resp = device.cli(command="request security utm web-filtering juniper-enhanced cache "
                                     "flush").response()

    if "Flush cache OK" in device_resp:
        device.log(level="INFO", message="UTM cache is flushed successfully")
    else:
        device.log(level="Error", message="UTM cache is not being flushed: " + device_resp)
        raise Exception("UTM cache is not being flushed")
    return True


def clear_utm_statistics(device=None):
    """
    To clear utm web-filtering statistics
    Example :-
        clear_utm_statistics(device=device)

    Robot Example:
        Clear Utm Statistics    device=${dut}

    :param Device device:
        **REQUIRED** Device handle for junox box

    :return:  On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    device.cli(command="clear security utm web-filtering statistics")
    return True


### looks for element in intrest from ike xml output
def _check_recur(root, key, dic=None):

    if dic is None:
        dic = {}
    if root.tag.title().lower() == key.lower():
        dic[key] = root.attrib.get('name', root.text.strip('\n'))
    else:
        for elem in root.getchildren():
            _check_recur(elem, key, dic)
    return dic


def get_utm_statistics(device=None, **kwargs):
    """
    To fetch utm web-filtering statistics
    Example :-
        get_utm_statistics(device=device)

    Robot Example:-
        set test variable  @{key}  esp-encrypted-packets  esp-decrypted-packets  ah-input-packets
        Get Utm Statistics    device=${dut}    key=@{key}

    :param device_handle:
        **REQUIRED**  device handle

    :param key:
        **REQUIRED**  Single value or list of values from show output

    :return: Dictonary of requested values
    :rtype: dict
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    key = kwargs.get('key')
    if key is None:
        device.log(level='ERROR', message="key is mandatory argument")
        raise ValueError("key is mandatory argument")

    keys = []
    if isinstance(key, str):
        keys.append(key)
    else:
        keys = key

    stats_output = device.get_rpc_equivalent(command="show security utm web-filtering statistics")
    elements = device.execute_rpc(command=stats_output).response()

    stats_dict = {}
    for element in keys:
        stats_dict.update(_check_recur(elements, element))
    return stats_dict


def config_utm_url_pattern(device=None, mode="set", **kwargs):
    """
    To configure url-pattern in UTM
    Example :-
        config_utm_url_pattern(device=None, url_name="mail", value="gmail.com")

    Robot Example:-
        Config Utm Url Pattern    device=${dut}    url_name=mail     value=gmail.com

    :param device_handle:
        **REQUIRED**  device handle

    :param str mode:
        *OPTIONAL* mode of the cli.
        ``Supported Values`` set, delete, delete_all

    :param str url_name:
        *OPTIONAL*  name of the url-pattern
        ``Default Value`` url1

    :param str value:
        **REQUIRED** value as IP/hostname

    :param bool commit:
        *OPTIONAL* Commit the config or not
        ``Default Value`` True
        ``Supported Value`` True and False

    :return: On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    url_name = kwargs.get('url_name', "url1")
    value = kwargs.get('value', None)
    commit = kwargs.get('commit', True)

    cmdlst = []
    if mode == "delete_all":
        cmd = "delete security utm custom-objects url-pattern"
    else:
        if value is None:
            device.log("ERROR", message="Value is mandatory")
            raise Exception("Value is the mandatory argument")
        else:
            cmd = "%s security utm custom-objects url-pattern %s value %s" % (mode,
                                                                              url_name, value)
    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if commit is True:
        device.commit()


def config_utm_custom_url_category(device=None, mode="set", **kwargs):
    """
    To configure url-pattern in UTM
    Example :-
        config_utm_url_pattern(device=None, category_name="url1", value=None)

    Robot Example:-
        Config Utm Custom Url Category    device=${dut}    cateoory_name=cat1    value=mail

    :param device_handle:
        **REQUIRED**  device handle

    :param str mode:
        *OPTIONAL* mode of the cli.
        ``Supported Values`` set, delete, delete_all

    :param str category_name:
        *OPTIONAL*  name of the custom url category
        ``Default Value`` cat1

    :param str value:
        **REQUIRED** value refers to url-pattern names

    :param bool commit:
        *OPTIONAL* Commit the config or not
        ``Default Value`` True
        ``Supported Value`` True and False

    :return: On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    category_name = kwargs.get('category_name', "cat1")
    value = kwargs.get('value', None)
    commit = kwargs.get('commit', True)

    cmdlst = []

    if mode == "delete_all":
        cmd = "delete security utm custom-objects custom-url-category"
    else:
        if value is None:
            device.log("ERROR", message="Value is mandatory")
            raise Exception("Value is the mandatory argument")
        else:
            cmd = "%s security utm custom-objects custom-url-category %s value %s" % (
                mode, category_name, value)
    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if commit is True:
        device.commit()


def config_utm_custom_message(device=None, **kwargs):
    """
    To configure url-pattern in UTM
    Example :-
        config_utm_custom_message(device=None, message_name="msg1",
        message_type="redirect-url", message_content="gmail.com")

    Robot Example:-
        Config Utm Custom Message    device=${dut}    message_name=msg1
        message_type=user-message
                                message_content="custom message defined by users"
    :param device_handle:
        **REQUIRED**  device handle

    :param str mode:
        *OPTIONAL* mode of the cli.
        ``Supported Values`` set, delete, delete_all

    :param str message_name:
        *OPTIONAL*  name of the custom message
        ``Default Value`` msg1

    :param str message_type:
        **REQUIRED** value can only be redirect-url or user-message

    :param str message_content:
        **REQUIRED** Either URL or custom message
    :param bool commit:
        *OPTIONAL* Commit the config or not
        ``Default Value`` True
        ``Supported Value`` True and False

    :return: On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    mode = kwargs.get('mode', "set")
    message_name = kwargs.get('message_name', "msg1")
    message_type = kwargs.get('message_type', None)
    message_content = kwargs.get('message_content', None)
    commit = kwargs.get('commit', True)

    cmdlst = []
    if mode == "delete_all":
        cmd = "delete security utm custom-objects custom-message"
    else:
        if message_type is None or message_content is None:
            device.log("ERROR", message="message_type and message_content are mandatory arguments")
            raise Exception("message_type and message_content are mandatory arguments")
        else:
            cmd = "%s security utm custom-objects custom-message %s type %s content %s" \
                % (mode, message_name, message_type, message_content)

    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if commit is True:
        device.commit()


def config_utm_profile(device=None, mode="set", **kwargs):
    """
    To configure ewf profile in UTM
    Example :-
        config_utm_ewf(device=None, profile_name="ewf1", category_name="cat1")
        config_utm_ewf(device=None, profile_name="ewf1", category_name="cat1", action="quarantine")

    Robot Example:-
        Config Utm profile   device=${dut}    profile_name=ewf1     category_name=cat1
        action=quarantine     message=msg1

    :param device_handle:
        **REQUIRED**  device handle

    :param str mode:
        *OPTIONAL* mode of the cli.
        ``Supported Values`` set, delete, delete_all

    :param str profile:
        *OPTIONAL* profile name to configure respective profile
        ``Default Value`` juniper_enhanced
        ``Supported Value`` juniper_enhanced, juniper_local, websense_redirect

    :param str profile_name:
        *OPTIONAL*  name of the ewf profile
        ``Default Value`` ewf1

    :param str  category_name:
        **REQUIRED** value can only be redirect-url or user-message

    :param str action:
        *OPTIONAL* action of the profile
        ``Default Value`` block
        ``Supported Value`` block and quarantine

    :param str message:
        *OPTIONAL* Either URL or custom message

    :param bool commit:
        *OPTIONAL* Commit the config or not
        ``Default Value`` True
        ``Supported Value`` True and False

    :return:On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    profile = kwargs.get('profile', "juniper_enhanced")
    profile_name = kwargs.get('profile_name', "ewf1")
    category_name = kwargs.get('category_name', "Enhanced_Social_Web_Youtube")
    action = kwargs.get('action', "block")
    message = kwargs.get('message', None)
    commit = kwargs.get('commit', True)

    cmdlst = []
    if mode == "delete_all":
        if profile == "juniper_enhanced":
            cmd = "delete security utm feature-profile web-filtering juniper-enhanced profile %s" % (
                profile_name)
        elif profile == "juniper_local":
            cmd = "delete security utm feature-profile web-filtering juniper-local profile %s" % (
                profile_name)
        elif profile == "websense_redirect":
            cmd = "delete security utm feature-profile web-filtering websense-redirect profile %s" % (
                profile_name)
    else:
        if profile == "juniper_enhanced":
            cmd = "%s security utm feature-profile web-filtering juniper-enhanced profile %s category %s action %s " % (
                mode, profile_name, category_name, action)
        elif profile == "juniper_local":
            cmd = "%s security utm feature-profile web-filtering juniper-local profile %s category %s action %s " % (
                mode, profile_name, category_name, action)
        elif profile == "websense_redirect":
            cmd = "%s security utm feature-profile web-filtering websense-redirect profile %s category %s action %s " % (
                mode, profile_name, category_name, action)
        if message is not None:
            cmd = cmd + " custom-message " + message

    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if commit is True:
        device.commit()


def config_utm_profile_global(device=None, mode="set", **kwargs):
    """
    To configure different profile global in UTM
    Example :-
        config_utm_ewf(device=None, profile_name="ewf1", category_name="cat1")
        config_utm_ewf(device=None, profile_name="ewf1", category_name="cat1", action="quarantine")

    Robot Example:-
        Config Utm Profile Global    device=${dut}    profile_name=ewf1     category_name=cat1
        action=quarantine     message=msg1

    :param device_handle:
        **REQUIRED**  device handle

    :param str mode:
        *OPTIONAL* mode of the cli.
        ``Supported Values`` set, delete

    :param str profile:
        *OPTIONAL* profile name to configure respective profile
        ``Default Value`` juniper_enhanced
        ``Supported Value`` juniper_enhanced, juniper_local, websense_redirect

    :param str profile_name:
        *OPTIONAL*  name of the ewf profile
        ``Default Value`` jnpr_enhanced

    :param str default:
        *OpTIONAL* EWF profile default value
        ``Supported Value`` block, log-and-permit and permit

    :param str block_message:
        *OPTIONAL* EWF block message settings
        ``Supported Value`` Type

    :param str quarantine_message:
        *OPTIONAL* EWF quarantine message settings
        ``Supported Value`` Type

    :param str custom_block_message:
        *OPTIONAL* EWF custom block message

    :param str quarantine_custom_message:
        *OPTIONAL* EWF quarantine custom message

    :param str url:
        *OPTIONAL* url name
        **REQUIRED** Required for block_message and quarantine_message

    :param bool commit:
        *OPTIONAL* Commit the config or not
        ``Default Value`` True
        ``Supported Value`` True and False

    :return: On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    profile = kwargs.get('profile', "juniper_enhanced")
    profile_name = kwargs.get('profile_name', "jnpr_enhanced")
    default = kwargs.get('default', None)
    block_message = kwargs.get('block_message', None)
    quarantine_message = kwargs.get('quarantine_message', None)
    custom_block_message = kwargs.get('custom_block_message', None)
    quarantine_custom_message = kwargs.get('quarantine_custom_message', None)
    url = kwargs.get('url', None)
    commit = kwargs.get('commit', True)

    cmdlst = []
    if profile == "juniper_enhanced":
        cmd = "%s security utm feature-profile web-filtering juniper-enhanced profile %s " % (
            mode, profile_name)
    elif profile == "juniper_local":
        cmd = "%s security utm feature-profile web-filtering juniper-local profile %s " % (
            mode, profile_name)
    elif profile == "websense_redirect":
        cmd = "%s security utm feature-profile web-filtering websense-redirect profile %s " % (
            mode, profile_name)
    else:
        device.log("Error", message="Unknown profile name to configure in UTM profile")
        raise Exception("Unknown profile name to configure in UTM profile")

    if default is not None:
        cmd = cmd + " default " + default
    if custom_block_message is not None:
        cmd = cmd + " custom-block-message " + custom_block_message
    if quarantine_custom_message is not None:
        cmd = cmd + " quarantine-custom-message " + quarantine_custom_message
    if block_message is not None:
        if url is None:
            device.log("Error", message="URL is required for block_message")
            raise Exception("URL is required for block_message")
        else:
            cmd = cmd + "  block-message type custom-redirect-url url " + url
    if quarantine_message is not None:
        if url is None:
            device.log("Error", message="url is required for redirect type")
            raise Exception("url is required for redirect type")
        else:
            cmd = cmd + " quarantine-message type custom-redirect-url url " + url

    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if commit is True:
        device.commit()


def config_utm_wf_type(device=None, mode="set", **kwargs):
    """
    To configure different profile global in UTM
    Example :-
        config_utm_wf_type(device=None, profile_name="ewf1", category_name="cat1")
        config_utm_wf_type(device=None, profile_name="ewf1", category_name="cat1",
        action="quarantine")

    Robot Example:-
        Config Utm Wf Type    device=${dut}    profile=juniper_enhanced    server=116.50.57.140

    :param device_handle:
        **REQUIRED**  device handle

    :param str mode:
        *OPTIONAL* mode of the cli.
        ``Supported Values`` set, delete

    :param str profile:
        *OPTIONAL*  name of the ewf profile
        ``Default Value`` uniper_enhanced
        ``Supported Values`` uniper_enhanced, juniper_local, websense_redirect

    :param str  server:
        *OPTIONAL* value can only be redirect-url or user-message

    :param bool commit:
        *OPTIONAL* Commit the config or not
        ``Default Value`` True
        ``Supported Value`` True and False

    :return: On success True, in failure it'll raise exception.
    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    profile = kwargs.get('profile', "juniper_enhanced")
    server = kwargs.get('server', None)
    commit = kwargs.get('commit', True)

    cmdlst = []
    cmdlst1 = []

    if profile == "juniper_enhanced":
        cmd = "%s security utm feature-profile web-filtering type juniper-enhanced" % (mode)
    elif profile == "juniper_local":
        cmd = "%s security utm feature-profile web-filtering type juniper-local" % (mode)
    elif profile == "websense_redirect":
        cmd = "%s security utm feature-profile web-filtering type websense-redirect" % (mode)
    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if server is not None and profile is "juniper_enhanced":
        cmd1 = "%s security utm feature-profile web-filtering juniper-enhanced server host %s" % (
            mode, server)
        cmdlst1.append(cmd1)
        device.config(command_list=cmdlst1)
    if commit is True:
        device.commit()


def config_utm_policy(device=None, mode="set", **kwargs):
    """
    To configure ewf profile in UTM
    Example :-
        config_utm_policy(device=None, policy_name="utmpolicy, http_profile="ewf1")

    Robot Example:-
        Config Utm Policy    device=${dut}    policy_name=utmpolicy     http_profile=ewf1

    :param device_handle:
        **REQUIRED**  device handle

    :param str mode:
        *OPTIONAL* mode of the cli.
        ``Supported Values`` set, delete

    :param str policy_name:
        *OPTIONAL*  name of the utm policy
        ``Default Value`` utmpolicy

    :param str  http_profile:
        **REQUIRED** http profile to enable in UTM policy

    :param bool commit:
        *OPTIONAL* Commit the config or not
        ``Default Value`` True
        ``Supported Value`` True and False

    :return: On success True, in failure it'll raise exception.

    :rtype: bool
    """
    if device is None:
        raise Exception("Device handle is a mandatory argument")

    policy_name = kwargs.get('policy_name', "utmpolicy")
    http_profile = kwargs.get('http_profile', None)
    commit = kwargs.get('commit', True)

    if http_profile is None:
        device.log("ERROR", message="http profile is the mandatory argument")
        raise Exception("http profile is the mandatory argument")

    cmdlst = []
    cmd = "%s security utm utm-policy %s web-filtering http-profile %s" % (mode, policy_name,
                                                                           http_profile)
    cmdlst.append(cmd)
    device.config(command_list=cmdlst)
    if commit is True:
        device.commit()
