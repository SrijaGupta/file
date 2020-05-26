# coding: UTF-8
"""Functions/Keywords to Configure Schedulers(set schedulers scheduler...)"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements


__author__ = ['Revant Tiku']
__contact__ = 'rtiku@juniper.net'
__copyright__ = 'Juniper Networks Inc.'
__date__ = '2017'


def configure_scheduler(device=None, scheduler_name=None, day=None, start_time=None, stop_time=None, commit=False):
    """
    Configuring a scheduler(set schedulers scheduler ...)

    :Example:

    python:  configure_scheduler(device=None, scheduler_name='DAILY_AT_8', day='daily', start_time='2007-03-04.08:01',
                                 stop_time='2007-03-04.08:03')

    robot:  Configure Scheduler    device=${r0}    scheduler_name=DAILY_AT_8    day=daily    start_time=2007-03-04.08:01
            ...    stop_time=2007-03-04.08:03    commit=${True}


    :param Device device:
        **REQUIRED**  Handle of the device on which configuration has to be executed.
    :param str scheduler_name:
        **REQUIRED**  Name of the scheduler.
    :param str day:
        **REQUIRED**  Interval day. Available options:
                *  daily
                *  monday
                *  tuesday
                *  wednesday
                *  thursday
                *  friday
                *  saturday
                *  sunday
    :param str start_time:
        **REQUIRED**  Start date and time ([YYYY-]MM-DD.hh:mm)
    :param str stop_time:
        **REQUIRED**  Stop date and time ([YYYY-]MM-DD.hh:mm)
    :param bool commit:
        *OPTIONAL* Whether to commit at the end or not. Default value: commit=False
    :return:
        * ``True`` when scheduler configuration is entered
    :raises Exception:
        *  When mandatory parameters are missing
        *  Commit fails(when **commit** is True)
        *  Device behaves in an unexpected way while in config/cli mode
        *  Device handle goes bad(device disconnection).
    """

    if device is None:
        raise Exception("'device' is mandatory parameter for configuring a scheduler")
    if scheduler_name is None:
        device.log(level="ERROR", msg="'scheduler_name' is a mandatory parameter "
                                      "for configuring a scheduler")
        raise Exception("'scheduler_name' is a mandatory parameter for configuring a scheduler")
    if start_time is None:
        device.log(level="ERROR", msg="'start_time' is a mandatory parameter "
                                      "for configuring a scheduler")
        raise Exception("'start_time' is a mandatory parameter for configuring a scheduler")
    if stop_time is None:
        device.log(level="ERROR", msg="'stop_time' is a mandatory parameter "
                                      "for configuring a scheduler")
        raise Exception("'stop_time' is a mandatory parameter for configuring a scheduler")

    device.config(command_list=['set schedulers scheduler ' + scheduler_name + ' ' + day + ' start-date ' + start_time +
                                ' stop-date ' + stop_time])

    if commit:
        return device.commit(timeout=60)
    else:
        return True
