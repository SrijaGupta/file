"""
Time utility
"""

import re
import pytz
import datetime
from time import ctime
from ntplib import NTPClient
from jnpr.toby.exception.toby_exception import TobyException

def convert_datetime_to_gmt(time_zone=None, date_time=None):
    """
    This function is used to convert 2 different datetime format to GMT
    :param date_time:
        **REQUIRED** Datetime which has to be converted to GMT format
        Supported formats are '%Y%m%d %H:%M:%S.%f' and '%b %d %H:%M %Y'
    :param time_zone:
        **REQUIRED** Timezone of the date_time passed as an argument
        Supported values are 'PST' and 'IST'
    :returns: Returns GMT time in the format of '%Y%m%d%H%M'
    """
    gmt_time = None
    if time_zone == "PST":
        local = pytz.timezone("America/Los_Angeles")
    elif time_zone == "IST":
        local = pytz.timezone("Asia/Kolkata")
    elif time_zone == "EST" or time_zone == "EDT":
        local = pytz.timezone("US/Eastern")
    elif time_zone == "PDT":
        local = pytz.timezone("US/Pacific")
    elif time_zone == "CST":
        local = pytz.timezone("Asia/Shanghai")
    elif time_zone == "UTC":
        local = pytz.timezone("UTC")
    elif time_zone == "GMT":
        local = pytz.timezone("GMT")
    elif time_zone == "MDT":
        local = pytz.timezone("America/Boise")
    elif time_zone == "MST":
        local = pytz.timezone("America/Creston")
    elif time_zone == "CET":
        local = pytz.timezone("Europe/Copenhagen")
    elif time_zone == "AST":
        local = pytz.timezone("Asia/Kuwait")
    elif time_zone == "AEST":
        local = pytz.timezone("Australia/ACT")
    else:
        raise TobyException("Invalid Time Zone")

    try:
        if re.search(r'^\s*\d+', date_time, re.I):
            naive = datetime.datetime.strptime(date_time, "%Y%m%d %H:%M:%S.%f")
        else:
            naive = datetime.datetime.strptime(date_time, "%b %d %H:%M %Y")
    
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
    
        gmt_time = utc_dt.strftime("%Y%m%d%H%M")

    except ValueError:
        raise TobyException('Invalid format received')

    return gmt_time

def fetch_time_from_ntp(server=None):
    """
    Function to fetch the time stamp from an NTP server.

    Author: Sudhir Akondi (sudhira@juniper.net)

    Python Example:
        _ntp_server_ = "10.215.194.50"
        _datetime_, _epoch_secs_ = fetch_time_from_ntp(server=_ntp_server_)

    :param str server:
      **REQUIRED** IPv4 / IPv6 Address of the NTP server

    :returns:
      tuple containing two values;
        1. readable format of the date time string
        2. epoch seconds - elapsed since 1 Jan 1970
    """
    try:
        if server is None or server == "":
            raise Exception("fetch_time_from_ntp: Argument server is mandator")

        _client_ = NTPClient()

        _response_ = _client_.request(server)

        if _response_ is not None:
            return ctime(_response_.tx_time), _response_.tx_time
        else:
            raise Exception("No response from NTP server @ %s" % server)

    except Exception as _exception_:
        raise Exception("Exception raised in fetch_time_from_ntp: %s : %s"
                        % (type(_exception_), _exception_))
