"""
Enable or Disable AppID Application Service
"""

__author__ = ['Sasikumar Sekar']
__contact__ = 'sasik@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def enable_or_disable_appid_application(device=None, mode=None, application=None):
    """
    Enable or Disable AppID Application Service
    request services application-identification application disable junos:HTTP

    :Example:

    python: enable_or_disable_appid_application(device=router_handle, mode=enable,
     application=junos:HTTP)

    robot:

    Enable or Disable Appid Application    device=${dh}    mode=enable    application=junos:HTTP

    :param Device device:
        **REQUIRED** Device Handler.
    :param str mode:
        **REQUIRED** Disable/Enable a predefined application.
    :param str/list application:
        **REQUIRED** Predefined application name. It can be list of application or
         single application.
    :return:
        * ``Status`` whether it is enabled or disabled
    :raises Exception: when mandatory parameter is missing
    """

    if device is None:
        raise Exception("'device' is mandatory parameter device handle")

    if mode is None:
        device.log(level="ERROR", msg="'mode' is mandatory parameter. Ex.mode=enable/disable")
        raise Exception("'mode' is mandatory parameter. Ex.mode=enable/disable")

    if application is None:
        device.log(level="ERROR", msg="'application' is mandatory parameter."
                                      " Ex.application=junos:HTTP")
        raise Exception("'application' is mandatory parameter. Ex.application=junos:HTTP")

    if device is not None and mode is not None and application is not None:

        cmd = 'request services application-identification application ' + mode

        if isinstance(application, list):
            for temp in application:
                search_string_enable1 = 'Application ' + temp + ' is already enabled'
                search_string_enable2 = 'Enable application (' + temp + ') succeed'
                search_string_disable1 = 'Application ' + temp + ' is already disabled'
                search_string_disable2 = 'Disable application (' + temp + ') succeed'
                result = device.cli(command=cmd + ' ' + temp, timeout=100).response()
                if ((mode == 'enable') and (result.find(search_string_enable1) != -1)) or\
                        (result.find(search_string_enable2) != -1):
                    device.log(message=temp + ' is enabled or already enabled', level='INFO')
                elif ((mode == 'disable') and (result.find(search_string_disable1) != -1)) or\
                        (result.find(search_string_disable2) != -1):
                    device.log(message=temp + ' is disabled or already disabled', level='INFO')
                else:
                    device.log(message='Application package is unavailable', level='ERROR')
                    raise Exception('Application package is unavailable')
        else:
            search_string_enable1 = application + ' is already enabled'
            search_string_enable2 = 'Enable application (' + application + ') succeed'
            search_string_disable1 = 'Application ' + application + ' is already disabled'
            search_string_disable2 = 'Disable application (' + application + ') succeed'
            result = device.cli(command=cmd + ' ' + application).response()
            if ((mode == 'enable') and (result.find(search_string_enable1) != -1)) or\
                    (result.find(search_string_enable2) != -1):
                device.log(message=application + ' is enabled or already enabled', level='INFO')
            elif ((mode == 'disable') and (result.find(search_string_disable1) != -1)) or\
                    (result.find(search_string_disable2) != -1):
                device.log(message=application + ' is disabled or already disabled', level='INFO')
            else:
                device.log(message='Application package is unavailable', level='ERROR')
                raise Exception('Application package is unavailable')
