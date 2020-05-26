import unittest2 as unittest
from mock import MagicMock
from mock import patch
from jnpr.toby.hldcl.unix.unix import UnixHost
from jnpr.toby.utils.linux import l4_session
from jnpr.toby.utils.linux.l4_session import *



# To return response of shell() mehtod
class Response:
    def __init__(self, x=""):
        self.resp = x

    def response(self):
        return self.resp



class UnitTest(unittest.TestCase):

    # Mocking the L4_Session handle and its methods
    mocked_obj = MagicMock(spec=L4_Session)
    mocked_obj.dh = MagicMock()
    mocked_obj.sessionid = MagicMock()
    mocked_obj.pktSent = MagicMock()

    # only for one test (test_keyword_create_l4_session_object()
    mocked_obj2 = MagicMock(spec=UnixHost)


    def test_check_status(self):
        lst = Response(" 1125 ")
        self.mocked_obj.dh.shell = MagicMock(return_value=lst)
        self.assertEqual(L4_Session.check_status(self.mocked_obj, sessid=100), True)


        lst = Response("")
        self.mocked_obj.dh.shell.return_value = lst
        self.assertEqual(L4_Session.check_status(self.mocked_obj, state="absence"), True)


    def test_check_status_exception(self):
        self.mocked_obj.dh.shell = MagicMock(return_value=Response(" "))
        try:
            L4_Session.check_status(self.mocked_obj, state="abc")
        except Exception as err:
            self.assertEqual(err.args[0],
                             'Unsupported value for STATE. Supported values are "presence" or "absence"')

        try:
            L4_Session.check_status(self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "L4_Session utility is not running.Presence is not found in output")

        lst = Response(" 1035 ")
        self.mocked_obj.dh.shell.return_value = lst
        try:
            L4_Session.check_status(self.mocked_obj, state="absence", sessid=10)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "L4_Session utility is not running. Absence is not found in output")


    def test_check_data_received(self):
        lst = Response("1")
        self.mocked_obj.dh.shell = MagicMock(return_value=lst)
        self.assertEqual(L4_Session.check_data_received(self.mocked_obj),True)

        lst = Response("0")
        self.mocked_obj.dh.shell.return_value = lst
        self.assertEqual(L4_Session.check_data_received(self.mocked_obj, state="dropped"), True)


    def test_check_data_received_exception(self):
        try:
            L4_Session.check_data_received(self.mocked_obj, state="abc")
        except Exception as err:
            self.assertEqual(err.args[0], 'Unsupported values for STATE. Supported values are "received" or "dropped"')

        lst = Response("")
        self.mocked_obj.dh.shell = MagicMock(return_value=lst)
        try:
            L4_Session.check_data_received(self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Packet not Received")

        lst = Response("")
        self.mocked_obj.dh.shell.return_value = lst
        try:
            L4_Session.check_data_received(self.mocked_obj, state="dropped")
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Packet received, not Expected for drop")


    def test_start(self):

        lst = Response("Cannot start session and Cannot bind ")
        self.mocked_obj.dh.shell = MagicMock(return_value=lst)
        self.assertEqual(
            L4_Session.start(self.mocked_obj, mode="server", server_ip="5.0.0.1",
                                  server_port=500,
                                  client_port=100), 0)

        self.assertEqual(
            L4_Session.start(self.mocked_obj, mode="server", server_ip="5.0.0.1",
                                  server_port=500,
                                  client_port=100, protocol="udp"), 0)

        self.assertEqual(
            L4_Session.start(self.mocked_obj, mode="client", server_ip="5.0.0.1",
                                  server_port=500,
                                  client_ip="4.0.0.1", client_port=100, protocol="udp"), 0)

        self.assertEqual(
            L4_Session.start(self.mocked_obj, mode="client", server_ip="5.0.0.1",
                                  server_port=500,
                                  client_port=100, protocol="udp"), 0)

    def test_start_exception(self):
        try:
            L4_Session.start(self.mocked_obj, mode="abcd", server_ip="5.0.0.1", server_port=80)
        except Exception as err:
            self.assertEqual(err.args[0],
                             "Unsupported value for mode. Supported values are client and server")

        try:
            L4_Session.start(self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "server_ip and server_port are mandatory arguments")


    def test_send_pkt(self):

        self.assertEqual(
            L4_Session.send_data(self.mocked_obj, data="1234", hex_format=True, ipv6=True),
            None)
        self.assertEqual(L4_Session.send_data(self.mocked_obj, data="1234"), None)

        try:
            L4_Session.send_data(self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "data is a mandatory argument")

    def test_close_pkt(self):

        self.assertEqual(L4_Session.close(self.mocked_obj, sessid=10), None)
        self.assertEqual(L4_Session.close(self.mocked_obj, ipv6=True, sessid=10), None)

        self.mocked_obj.sessionid = 0
        self.assertEqual(L4_Session.close(self.mocked_obj), None)


    #@patch('jnpr.toby.utils.linux.l4_session.upload_file')
    def test_keyword_create_l4_session_object(self):
        self.mocked_obj2.upload_file = MagicMock()
        x = create_l4_session_object(device_handle=self.mocked_obj2)
        self.assertEqual(isinstance(x, L4_Session), True)


    def test_keyword_check_l4_session_status(self):
        self.mocked_obj.check_status = MagicMock()
        x = check_l4_session_status(self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)


    def test_keyword_check_l4_session_packet_received(self):
        self.mocked_obj.check_data_received = MagicMock()
        x = check_l4_session_packet_received(self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)


    def test_keyword_l4_session_start(self):
        self.mocked_obj.start = MagicMock()
        x = l4_session_start(self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)


    def test_keyword_l4_session_close(self):
        self.mocked_obj.close = MagicMock()
        x = l4_session_close(self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)


    def test_keyword_l4_session_send_data(self):
        self.mocked_obj.send_data = MagicMock()
        x = l4_session_send_data(self.mocked_obj)
        self.assertEqual(isinstance(x, MagicMock), True)



    def test_keyword_l4_session_start_server(self):
        l4_session.l4_session_start = MagicMock(return_value=10)
        self.assertEqual(l4_session_start_server(self.mocked_obj), 10)

        l4_session.l4_session_start.return_value = 0

        try:
            l4_session_start_server(l4_session_object=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Server failed to start")



    def test_keyword_l4_session_start_client(self):
        l4_session.l4_session_start = MagicMock(return_value=10)
        self.assertEqual(l4_session_start_client(self.mocked_obj), 10)

        l4_session.l4_session_start.return_value = 0

        try:
            l4_session_start_client(l4_session_object=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "Client failed to start")


    def test_keyword_l4_session_start_connection(self):
        l4_session.l4_session_start_server = MagicMock(return_value=2)
        l4_session.l4_session_start_client = MagicMock(return_value=5)
        x = l4_session_start_connection(self.mocked_obj, self.mocked_obj)
        self.assertEqual(x['server'], 2)
        self.assertEqual(x['client'], 5)


    def test_keyword_close_connection(self):
        l4_session.l4_session_close = MagicMock()
        self.assertEqual(l4_session_close_connection(self.mocked_obj, self.mocked_obj), None)




if __name__ == '__main__':
    unittest.main()
