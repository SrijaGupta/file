from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.utils.linux import email_traffic
from jnpr.toby.hldcl.host import upload_file
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.utils.response import Response

# To return response of vty() mehtod

class Response:

    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp

class UnitTest(unittest.TestCase):


    # Mocking the handle and its methods
    mocked_obj = MagicMock(spec=UnixHost)
    mocked_obj.log = MagicMock()
    mocked_obj.execute = MagicMock()
    upload_file = MagicMock()

    def test_smtp_send_mail_exception(self):
        try:
            email_traffic.smtp_send_mail()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device argument is mandatory")

    def test_smtp_send_mail_exception_no_server_toaddress(self):
        try:
            email_traffic.smtp_send_mail(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "server and to_address are mandatory argument")
        
    def test_smtp_send_mail_success(self):
        lst = [Response("QUIT")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        upload_file = MagicMock()
        self.assertEqual(
             email_traffic.smtp_send_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           to_address="abc@xyz.com",
                           auth_type="login",
                           user="test",
                           password="netscreen",
                           from_address="xyz@abc.com",
                           cc_address="test@abc.com",
                           bcc_address="test1@abc.com",
                           subject="test",
                           mail_message="test",
                           attachment="test",
                           encoding="base64"),
                           True)

    def test_smtp_send_mail_success_no_auth(self):
        lst = [Response("QUIT")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.mocked_obj.upload_file = MagicMock(side_effect=["done"])
        self.assertEqual(
             email_traffic.smtp_send_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           to_address="abc@xyz.com",
                           from_address="xyz@abc.com",
                           cc_address="test@abc.com",
                           bcc_address="test1@abc.com",
                           subject="test",
                           mail_message="test",
                           attachment="test",
                           encoding="base64"),
                           True)

    def test_smtp_send_mail_failure(self):
        lst = [Response("")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        
        try:
            email_traffic.smtp_send_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           to_address="abc@xyz.com",
                           from_address="xyz@abc.com",
                           cc_address="test@abc.com",
                           bcc_address="test1@abc.com",
                           subject="test",
                           mail_message="test",
                           attachment="test",
                           encoding="base64")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Failed to send mail")

    def test_smtp_send_mail_failure_exception(self):
        try:
             email_traffic.smtp_send_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           to_address="abc@xyz.com",
                           auth_type="login",
                           from_address="xyz@abc.com",
                           cc_address="test@abc.com",
                           bcc_address="test1@abc.com",
                           subject="test",
                           mail_message="test",
                           attachment="test",
                           encoding="base64")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "user and password is mandatory with auth_type")

#----------------------------------------------------------------

    def test_imap_fetch_mail_exception(self):
        try:
            email_traffic.imap_fetch_mail()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_imap_fetch_mail_exception_no_server_user(self):
        try:
            email_traffic.imap_fetch_mail(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "server ,user_name and password are mandatory arguments")

    def test_imap_fetch_mail_success(self):
        lst = [Response("MAIL FETCHED")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             email_traffic.imap_fetch_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           user_name="test",
                           password="netscreen",
                           starttls="yes"),
                           True)

    def test_imap_fetch_mail_failure(self):
        lst = [Response("Unable to fetch mail")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            email_traffic.imap_fetch_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           user_name="test",
                           password="netscreen",
                           starttls="yes")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Failed to fetch mail")

#-------------------------------------------------------------------------------------------

    def test_pop3_fetch_mail_exception(self):
        try:
            email_traffic.pop3_fetch_mail()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

    def test_pop3_fetch_mail_exception_no_server_user(self):
        try:
            email_traffic.pop3_fetch_mail(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "server ,user_name and password are mandatory arguments")

    def test_pop3_fetch_mail_success(self):
        lst = [Response("FETCHED MAIL")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             email_traffic.pop3_fetch_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           user_name="test",
                           password="netscreen",
                           starttls="yes"),
                           True)

    def test_pop3_fetch_mail_failure(self):
        lst = [Response("Unable to fetch mail")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            email_traffic.pop3_fetch_mail(
                           device=self.mocked_obj,
                           server="5.0.0.1",
                           user_name="test",
                           password="netscreen",
                           starttls="yes")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Failed to fetch mail")

#---------------------------------------------------------------------

    def test_execute_interactive_commands_exception(self):
        try:
            email_traffic.execute_interactive_commands()
        except Exception as err:
            self.assertEqual(
                err.args[0], 
                 "device is mandatory argument") 

        try:
            email_traffic.execute_interactive_commands(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "command and pattern are mandatory argument")

    def test_execute_interactive_commands_success_running(self):
        lst = [Response("250")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        command = ["MAIL FROM: <abc@xyz.com>"]
        pattern = ["250"]
        self.assertEqual(
             email_traffic.execute_interactive_commands(
                    device=self.mocked_obj,
                    command=command,
                    pattern=pattern),
                    True)

    def test_execute_interactive_commands_fail(self):
        command = ["MAIL FROM: <abc@xyz.com>"]
        pattern = ["250","354"]
        try:
            email_traffic.execute_interactive_commands(
                    device=self.mocked_obj,
                    command=command,
                    pattern=pattern)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Number of command and pattern should be same")

if __name__ == '__main__':
    unittest.main() 
