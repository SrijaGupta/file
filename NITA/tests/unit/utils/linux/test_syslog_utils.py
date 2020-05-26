
import unittest2 as unittest


from mock import MagicMock
from jnpr.toby.utils.linux import syslog_utils
from jnpr.toby.hldcl.unix.unix import UnixHost



# To return response of shell() mehtod
class Response():
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp


class UnitTest(unittest.TestCase):


    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()

    def test_check_syslog_exception(self):

        try:
            syslog_utils.check_syslog()
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument: 'device' need to be passed")

        try:
            syslog_utils.check_syslog(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument: 'pattern' need to be passed")


    def test_check_syslog_true(self):
        lst = [Response(""), Response(""), Response("5"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(syslog_utils.check_syslog(device=self.mocked_obj, pattern="abc",count=5, case_insensitive=True), True)

        lst = [Response(""), Response(""), Response("0"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(syslog_utils.check_syslog(device=self.mocked_obj, pattern="def", syslog_src_ip="4.0.0.1", negate=True), True)

        lst = [Response(""), Response(""), Response("3"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(syslog_utils.check_syslog(device=self.mocked_obj, pattern="abc", syslog_src_ip="4.0.0.1"), True)

    def test_check_syslog_false(self):

        lst = [Response(""), Response(""), Response("5"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            syslog_utils.check_syslog(device=self.mocked_obj, pattern="def", negate=True, case_insensitive=True)
        except Exception as err:
            self.assertEqual(err.args[0], "String *def* is found 5 no of times, Expected : 0 times")


        lst = [Response(""), Response(""), Response("0"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        try:
            syslog_utils.check_syslog(device=self.mocked_obj, pattern="abc", syslog_src_ip="4.0.0.1")
        except Exception as err:
            self.assertEqual(err.args[0], "String is found 0 times, Expected : 1 or more times")


        lst = [Response(""), Response(""), Response("1"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        try:
            syslog_utils.check_syslog(device=self.mocked_obj, pattern="abc", syslog_src_ip="4.0.0.1", count=3)
        except Exception as err:
            self.assertEqual(err.args[0], "String *abc* is found 1 times, Expected : 3 times")


    def test_configure_syslogd_exception(self):
        try:
            syslog_utils.configure_syslogd()
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument: 'device' need to be passed")

        lst = [Response(""), Response(""), Response(""), Response("")]
        self.mocked_obj.shell.side_effect = lst
        try:
            syslog_utils.configure_syslogd(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Syslogd couldn't start back")



    def test_configure_syslogd(self):

        lst = [Response(".*rsyslog.*"), Response(""), Response(""), Response("rsyslogd (pid  31557) is running...")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(syslog_utils.configure_syslogd(device=self.mocked_obj), True)



    def test_clear_syslog_exception(self):
        try:
            syslog_utils.clear_syslog()
        except Exception as err:
            self.assertEqual(err.args[0], "Mandatory argument: 'device' need to be passed")

        lst = [Response(""), Response(""), Response(""), Response(""), Response(""), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            syslog_utils.clear_syslog(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Syslogd couldn't start back")


    def test_clear_syslog(self):
        lst = [Response("abcrsyslogabc"), Response(""), Response(""), Response(""), Response("Active: active (running) since "), Response("CentOS Linux release 7.6.1810 (Core) "), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(syslog_utils.clear_syslog(device=self.mocked_obj), True)

        self.assertEqual(syslog_utils.clear_syslog(device=self.mocked_obj, restart_server=False), True)




if __name__ == '__main__':
    unittest.main()




