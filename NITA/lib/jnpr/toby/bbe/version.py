#  Copyright 2016- Juniper Networks

"""Toby BBE version module.

This module could be used to easily set BBE libraries version.
Robot tools could use either __version__ or ROBOT_LIBRARY_VERSION
to track and document libraries.

Example usage in module bbeinit.py:

__version__ = get_bbe_version()

class BBEInit():
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

The following lines are excerpt from Robot user guide --

Specifying library version
When a test library is taken into use, Robot Framework tries to determine its version.
This information is then written into the syslog to provide debugging information.
Library documentation tool Libdoc also writes this information into the keyword
documentations it generates. Version information is read from attribute ROBOT_LIBRARY_VERSION,
similarly as test library scope is read from ROBOT_LIBRARY_SCOPE. If ROBOT_LIBRARY_VERSION does
not exist, information is tried to be read from__version__ attribute. These attributes must be
class or module attributes, depending whether the library is implemented as a class or a module.
"""

import traceback

from jnpr.toby.bbe.errors import BBECommonError

BBE_RELEASE_NAME = "TOBY BBE"
BBE_RELEASE_TYPE = "RELEASE"    # ALPHA or BETA or RELEASE
BBE_RELEASE_VERSION = '1.0'


def get_bbe_version():
    """Get BBE version number only.

    :return: BBE version number
    """
    return BBE_RELEASE_VERSION


def get_bbe_full_version():
    """Get BBE full version, including version name, type, and number.

    :return: BBE full version
    """
    version = '%s %s %s' % (BBE_RELEASE_NAME,
                            BBE_RELEASE_TYPE,
                            BBE_RELEASE_VERSION)
    return version


def log_bbe_version():
    """Log BBE full version.

    :param log: A logger object. Use Robot logger at info level by default
    :return: None. The return value is not meat to be used.
    :exception: Raise BBECommonError is the log param failed to log message.

    """
    try:
        t.log('info', get_bbe_full_version() + '\n')
    except Exception as err:
        raise BBECommonError("log_bbe_version() failed: %s\nTraceback:\n%s"
                             % (str(err), traceback.extract_tb(err.__traceback__)))



