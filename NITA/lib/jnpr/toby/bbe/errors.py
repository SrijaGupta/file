#  Copyright 2016- Juniper Networks

"""Exceptions used for Toby BBE internally.

External libraries should not used exceptions defined here.

You can create a new subclass of BBEError when you need new
exception type.
"""

class BBEError(Exception):
    """Base class for BBE errors.

    Do not raise this method but use more specific errors instead.
    """

    def __init__(self, message='', details=''):
        Exception.__init__(self, message)
        self.details = details

    @property
    def message(self):
        """Return the error message
        """
        return str(self)


class BBECommonError(BBEError):
    """Used for BBE errors that do not fall into other categories.
    """
    pass


class BBEVarError(BBEError):
    """Used when bbevar operation fails.
    """
    pass


class BBEInitError(BBEError):
    """Used when BBE initialization goes to unexpected state.
    """
    pass


class BBEConfigError(BBEError):
    """Used when BBE test configuration goes to unexpected state.
    """
    pass


class BBESubscriberError(BBEError):
    """Used when BBE subscribers goes to unexpected state.
    """
    pass


class BBEDeviceError(BBEError):
    """Used when BBE test devices goes to unexpected state.
    """
    pass
