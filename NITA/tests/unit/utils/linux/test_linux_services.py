from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.utils.linux import linux_services
from jnpr.toby.hldcl.unix.unix import UnixHost

# To return response of shell() mehtod
class Response:

    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):

    # Mocking the tcpdump handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()


    def test_check_linux_running_service_exception(self):
        try:
            linux_services.check_linux_running_service()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

        try:
            linux_services.check_linux_running_service(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "service argument is mandatory")

    def test_check_linux_running_service_success_running(self):
        lst = [Response("httpd service is running")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd"),
                    True)

    def test_check_linux_running_service_success_start(self):
        lst = [Response("httpd service is stopped"),Response(""),Response("httpd service is running")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd"),
                    True)

    def test_check_linux_running_service_success_start_2(self):
        lst = [Response("Active: inactive dead"),Response(""),Response("Active: active running")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd"),
                    True)

    def test_check_linux_running_service_failure(self):
        lst = [Response("httpd unrecognized service")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Service is not installed")

    def test_check_linux_running_service_failure_2(self):
        lst = [Response("service could not be found")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Service is not installed")

    def test_check_linux_running_service_failure_start(self):
        lst = [Response("httpd service is stopped"),Response(""),Response("httpd service is stopped")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Service is not running")

    def test_check_linux_running_service_failure_start_2(self):
        lst = [Response("Active: inactive dead"),Response(""),Response("Active: inactive dead")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Service is not running")

    def test_check_linux_running_service_failure_start_wrong_output(self):
        lst = [Response("httpd service not known")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            linux_services.check_linux_running_service(
                    device=self.mocked_obj,
                    service="httpd")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Unable to get service status")

    def test_stop_services(self):
        try:
            linux_services.stop_services()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            linux_services.stop_services(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],"'service' is a mandatory argument" )

        lst = [Response("vsftpd is running .... httpd is running.... xinetd"), Response(" OK "), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(linux_services.stop_services(device=self.mocked_obj, service=["ftp", "httpd", "telnet", "abc"]), False)

        lst = [Response("vsftpd is running"), Response("OK")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(linux_services.stop_services(device=self.mocked_obj, service=["ftp"]), True)

        self.mocked_obj.shell = MagicMock()
        self.assertEqual(linux_services.stop_services(device=self.mocked_obj, service=["ftp"], dont_check=True),True)


    def test_start_services(self):
        try:
            linux_services.start_services()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            linux_services.start_services(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],"'service' is a mandatory argument" )

        lst = [Response("vsftpd is running"), Response("OK"), Response("unrecognized service"), Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(linux_services.start_services(device=self.mocked_obj,
                                                      service=["ftp", "telnet", "abc", "httpd"]), False)

        lst = [Response(""), Response("OK"), Response("unrecognized service"), Response("")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(linux_services.start_services(device=self.mocked_obj,
                                                      service=["ftp", "abc", "telnet"], restart=True), False)

        lst = [Response("vsftpd is running")]
        self.mocked_obj.shell.side_effect = lst
        self.assertEqual(linux_services.start_services(device=self.mocked_obj,
                                                      service=["ftp"]), True)

        self.mocked_obj.shell = MagicMock()
        self.assertEqual(linux_services.start_services(device=self.mocked_obj,
                                                       service=["ftp"], dont_check=True), True)



    def test_kill_process_exception(self):
        try:
            linux_services.kill_process()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            linux_services.kill_process(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Either pids or process_names has to be passed")


    @patch('jnpr.toby.utils.linux.linux_services.get_pid')
    def test_kill_process(self, patched_get_pid):

        self.mocked_obj.shell = MagicMock()
        patched_get_pid.return_value = ["123"]

        self.assertEqual(linux_services.kill_process(device=self.mocked_obj, pids=["123"], process_names=["abc"]), None)
        self.assertEqual(linux_services.kill_process(device=self.mocked_obj,
                                                     process_names="abc"), None)
        self.assertEqual(linux_services.kill_process(device=self.mocked_obj, pids="123"), None)


    def test_get_pid(self):
        try:
            linux_services.get_pid()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            linux_services.get_pid(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "process_name has to be passed")

        response = "tcpdump  26684  0.1  0.5  23320  6056 pts/0    S    16:48   0:00 tcpdump -i eth1\n" \
                    "abc     26685  1.0  0.1 110244  1148 pts/0    R+   16:48   0:00 hping -au"

        self.mocked_obj.shell = MagicMock(return_value=Response(response))
        list_to_return = ["26684", "26685"]

        self.assertEqual(linux_services.get_pid(device=self.mocked_obj, list_of_process_name=["tcpdump", "hping", "hping3"]), list_to_return)

if __name__ == '__main__':
    unittest.main()
