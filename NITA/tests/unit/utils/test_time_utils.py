
from jnpr.toby.utils.time_utils import convert_datetime_to_gmt
from jnpr.toby.utils.time_utils import fetch_time_from_ntp
import unittest
from mock import MagicMock, patch
from ntplib import NTPClient, NTPStats

class TestTime(unittest.TestCase):

    def setUp(self):
        import builtins
        builtins.t = MagicMock()
        builtins.t.log = MagicMock()

    def test_convert_datetime_to_gmt(self):
        convert_datetime_to_gmt(time_zone="PST",date_time="20170519 10:12:12.1")
        convert_datetime_to_gmt(time_zone="IST",date_time="May 02 13:05 2017")
        convert_datetime_to_gmt(time_zone="EST",date_time="20170519 10:12:12.1")
        convert_datetime_to_gmt(time_zone="PDT",date_time="20170519 10:12:12.1")
        convert_datetime_to_gmt(time_zone="CST",date_time="20170519 10:12:12.1")
        convert_datetime_to_gmt(time_zone="UTC",date_time="20170519 10:12:12.1")
        convert_datetime_to_gmt(time_zone="GMT",date_time="20170519 10:12:12.1")
        try :
            convert_datetime_to_gmt(date_time="20170519 10:12:12.1")
        except :
            pass

    @patch('ntplib.NTPClient.request', return_value=MagicMock(NTPStats))
    def test_fetch_time_from_ntp(self, patch1):
        fetch_time_from_ntp(server="10.1.1.1")
        try:
            fetch_time_from_ntp(server="")
            fetch_time_from_ntp(server="10.1.1.1")
        except:
            pass

if __name__ =='__main__':
    unittest.main()
