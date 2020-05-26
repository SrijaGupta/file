from mock import patch
import unittest2 as unittest
from mock import MagicMock
import unittest
from jnpr.toby.utils.linux.linux_traffic_utils import check_ping_connection, \
    check_traceroute_connection, openssl_traffic, wget_session, execute_curl
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


    def test_check_check_ping_connection_exception(self):
        try:
            check_ping_connection()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "device is mandatory argument")

        try:
            check_ping_connection(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "destination is mandatory argument")
        lst = [Response("4 packets transmitted, 4 received, 0% packet loss, time 3806ms")]
        _get_ip_address_type = MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
            check_ping_connection(
                device=self.mocked_obj,
                destination="4.0.0.1",
                source=None,
                count="5", strict_check=False),
            "4 packets transmitted, 4 received, 0% packet loss, time 3806ms")

    def test_check_check_ping_connection_ipv4_success(self):
        lst = [Response("4 packets transmitted, 4 received, 0% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             check_ping_connection(
                     device=self.mocked_obj,
                     destination="4.0.0.1",
                     source="4.0.0.2", rapid_ping=True, interval="5",
                     count="5"),
                     "4 packets transmitted, 4 received, 0% packet loss, time 3806ms")


    def test_check_check_ping_connection_ipv6_success(self):
        lst = [Response("4 packets transmitted, 4 received, 0% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             check_ping_connection(
                     device=self.mocked_obj,
                     destination="2005::1",
                     source="2004::1"),
                     "4 packets transmitted, 4 received, 0% packet loss, time 3806ms")

    def test_check_check_ping_connection_negative_success(self):
        lst = [Response("5 packets transmitted, 0 received, 100% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             check_ping_connection(
                     device=self.mocked_obj,
                     destination="2005::1",
                     source="2004::1",
                     negative=True),
                     "5 packets transmitted, 0 received, 100% packet loss, time 3806ms")

    def test_check_check_ping_connection_ipv6_success_1(self):
        lst = [Response("4 packets transmitted, 4 received, 0% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv6")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(
             check_ping_connection(
                     device=self.mocked_obj,
                     destination="2005::1",
                     source="2004::1",
                     packetsize="8972",
                     donotfrag="do"),
                     "4 packets transmitted, 4 received, 0% packet loss, time 3806ms")

    def test_check_check_ping_connection_unsuccess(self):
        lst = [Response("4 packets transmitted, 0 received, 100% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    count="5")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "All packets lost, Ping unsuccessful")

    def test_check_check_ping_connection_negative_unsuccess_1(self):
        lst = [Response("4 packets transmitted, 4 received, 0% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    negative=True,
                    count="5")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "no packet loss, Ping successful")

    def test_check_check_ping_connection_negative_unsuccess_2(self):
        lst = [Response("4 packets transmitted, 2 received, 50% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    negative=True,
                    count="5")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "few packets received, Ping successful")

    def test_check_check_ping_connection_unsuccess_2(self):
        lst = [Response("bind Cannot assign requested address")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    count="5")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Ping failed with error Cannot assign requested address")


    def test_check_check_ping_connection_unsuccess_3(self):
        lst = [Response("4 packets transmitted, 2 received, 50% packet loss, time 3806ms")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    count="5",
                    packetsize="64",
                    ttl="10")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "All packets not received, Ping unsuccessful")

    def test_check_check_ping_connection_unsuccess_4(self):
        lst = [Response("abcdef")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    count="5",
                    packetsize="64",
                    ttl="10")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "Unable to get ping status, Ping unsuccessful")

    def test_check_check_ping_connection_unsuccess_5(self):
        lst = [Response("Network is unreachable")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    count="5",
                    packetsize="64",
                    ttl="10")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "No route to host")

    def test_check_check_ping_connection_unsuccess_6(self):
        lst = [Response("No route to host")]
        _get_ip_address_type=MagicMock(side_effect="ipv4")
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
            check_ping_connection(
                    device=self.mocked_obj,
                    destination="4.0.0.1",
                    source="4.0.0.2",
                    count="5",
                    packetsize="64",
                    ttl="10")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                "No route to host")

    def test_check_traceroute_connection_exception(self):
        try:
           check_traceroute_connection()
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Linux handle is a mandatory argument")

        try:
           check_traceroute_connection(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "host is a mandatory argument")


        lst = [Response("a")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        try:
           check_traceroute_connection(device=self.mocked_obj, host="youtube.com", check_hop_ip="5.0.0.1")
        except Exception as err:
            self.assertEqual(
                err.args[0],
                 "Expected hop ip is not found in traceroute output")


    def test_check_traceroute_connection_execution_1(self):
        lst = [Response("xyz")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(check_traceroute_connection(device=self.mocked_obj, host="youtube.com"), "xyz")

    def test_check_traceroute_connection_execution_2(self):
        lst = [Response("5.0.0.1")]
        self.mocked_obj.shell = MagicMock(side_effect=lst)
        self.assertEqual(check_traceroute_connection(device=self.mocked_obj, host="youtube.com", check_hop_ip="5.0.0.1"), None)

    mocked_obj_client = MagicMock(spec=UnixHost)
    mocked_obj_server = MagicMock(spec=UnixHost)

    def test_openssl_traf(self):
        try:
            openssl_traffic(client=self.mocked_obj_client, serverip=None)
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'cserverip is REQUIRED key argument')

        try:
            openssl_traffic(client=self.mocked_obj_client, serverip="5.0.0.1", operation="prompt",
                            command_pattern=None)
        except ValueError as err:
            self.assertTrue(err.args[0],
                            'command_pattern is REQUIRED key argument when operation is prompt')

        return_value = ['/tmp/server-normal-tls1-RC4-MD5-STDOUT',
                        '/tmp/server-normal-tls1-RC4-MD5-STDERR',
                        '/tmp/client-normal-tls1-RC4-MD5-STDOUT',
                        '/tmp/client-normal-tls1-RC4-MD5-STDERR']
        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=self.mocked_obj_server,
                            operation="normal", serverip="5.0.0.1"), return_value)
        return_value_resump = ['/tmp/server-resumption-tls1-RC4-MD5-STDOUT',
                               '/tmp/server-resumption-tls1-RC4-MD5-STDERR',
                               '/tmp/client-resumption-tls1-RC4-MD5-STDOUT',
                               '/tmp/client-resumption-tls1-RC4-MD5-STDERR']
        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=self.mocked_obj_server,
                            operation="resumption", serverip="5.0.0.1"), return_value_resump)
        return_value_renego = ['/tmp/server-renegotiation-tls1-RC4-MD5-STDOUT',
                               '/tmp/server-renegotiation-tls1-RC4-MD5-STDERR',
                               '/tmp/client-renegotiation-tls1-RC4-MD5-STDOUT',
                               '/tmp/client-renegotiation-tls1-RC4-MD5-STDERR']
        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=self.mocked_obj_server,
                            operation="renegotiation", serverip="5.0.0.1"), return_value_renego)
        return_value_http = ['/tmp/server-httpget-tls1-RC4-MD5-STDOUT',
                             '/tmp/server-httpget-tls1-RC4-MD5-STDERR',
                             '/tmp/client-httpget-tls1-RC4-MD5-STDOUT',
                             '/tmp/client-httpget-tls1-RC4-MD5-STDERR']
        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=self.mocked_obj_server,
                            operation="httpget", serverip="5.0.0.1"), return_value_http)
        return_value_prompt = ['/tmp/server-prompt-tls1-RC4-MD5-STDOUT',
                               '/tmp/server-prompt-tls1-RC4-MD5-STDERR',
                               '/tmp/client-prompt-tls1-RC4-MD5-STDOUT',
                               '/tmp/client-prompt-tls1-RC4-MD5-STDERR']
        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=self.mocked_obj_server,
                            operation="prompt", serverip="5.0.0.1",
                            command_pattern=["{'command':'R', 'pattern':'RENEGOTIATING'}",
                                             "{'command':'Q', 'pattern':'DONE'}"]),
            return_value_prompt)
        return_value_nocipher = ['/tmp/server-normal-tls1-nonecipher-STDOUT',
                                 '/tmp/server-normal-tls1-nonecipher-STDERR',
                                 '/tmp/client-normal-tls1-nonecipher-STDOUT',
                                 '/tmp/client-normal-tls1-nonecipher-STDERR']
        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=self.mocked_obj_server,
                            operation="normal", serverip="5.0.0.1", client_cipher=None,
                            server_cipher=None),
            return_value_nocipher)
        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=self.mocked_obj_server,
                            operation="normal", serverip="5.0.0.1", sni_name="test",
                            ca_bundle="test", session_in="test", session_out="test",
                            client_cert_auth="yes", kill_server_openssl="yes",
                            kill_client_openssl="yes"), return_value)

        return_value_client = ['/tmp/client-normal-tls1-RC4-MD5-STDOUT',
                        '/tmp/client-normal-tls1-RC4-MD5-STDERR']

        return_value_server = ['/tmp/server-normal-tls1-RC4-MD5-STDOUT',
                        '/tmp/server-normal-tls1-RC4-MD5-STDERR']

        self.assertEqual(
            openssl_traffic(client=self.mocked_obj_client, server=None,
                            operation="normal", serverip="5.0.0.1", sni_name="test",
                            ca_bundle=None, session_in="test", session_out="test",
                            client_cert_auth="yes", kill_server_openssl="yes",
                            kill_client_openssl="yes", get_response="WWW"), return_value_client)

        self.assertEqual(
            openssl_traffic(client=None, server=self.mocked_obj_server,
                            operation="normal", serverip="5.0.0.1", sni_name="test",
                            ca_bundle=None, session_in="test", session_out="test",
                            client_cert_auth="yes", kill_server_openssl="yes",
                            kill_client_openssl="yes", get_response="WWW"), return_value_server)

    def test_wget_session_exception(self):
        try:
            wget_session()
        except Exception as err:
            self.assertEqual(err.args[0], "'device' is a mandatory argument")

        try:
            wget_session(device=self.mocked_obj)
        except Exception as err:
            self.assertEqual(err.args[0], "'url ia a mandatory argument")

    def test_wget_session(self):

        dict_to_return = {'file_name': "/root/abc.txt",
                          'time_taken_in_seconds': 100,
                          'file_transfer_percentage': 100,
                          'file_size': 123456}

        resp = 'HTTP request sent, awaiting response... 200 OK \n.. saved [123456/123456] \nLength: 25027096 (24M) [application/x-msdos-program]\nLength: 25027096 (24M) [application/x-msdos-program]\nSaving to: “abc.txt”\n100%[==============================================================================>]  123456   200KB/s   in 1m 40s  '
        self.mocked_obj.shell = MagicMock(side_effect=[Response("real  1m40."), Response(resp), Response(""), Response("/root")])
        self.assertEqual(wget_session(device=self.mocked_obj, url="5::1",
                                                          path_to_file="abc.txt", header="host:facebook.com",
                                                          source_address="4::1"), dict_to_return)

        dict_to_return2 = {'file_name': "/root/abc.txt",
                           'time_taken_in_seconds': 40,
                           'file_transfer_percentage': 80,
                           'file_size': 123456}
        resp2 = 'HTTP request sent, awaiting response... 200 OK \n.. saved [123456/123456]\nLength: 25027096 (24M) [application/x-msdos-program]\nLength: 25027096 (24M) [application/x-msdos-program]\nSaving to: ‘abc.txt’\n80%[==============================================================================>]  123456   200KB/s   in 40s  '
        self.mocked_obj.shell.side_effect = [Response("real  0m40."), Response(resp2), Response(""), Response("/root")]
        self.assertEqual(wget_session(device=self.mocked_obj, url="5.0.0.1", path_to_file="abc.txt", service="https", source_address="4.0.0.1", misc_option="abc"), dict_to_return2)

        resp3 = 'HTTP request sent, awaiting response... 200 OK \n.. saved [123456/123456] \nLength: 25027096 (24M) [application/x-msdos-program]\nLength: 25027096 (24M) [application/x-msdos-program]\n “abc.txt” saved\n100%[==============================================================================>]  123456   200KB/s   in 1m 40s  '
        self.mocked_obj.shell.side_effect = [Response("real  1m40."), Response(resp3), Response(""), Response("/root")]
        self.assertEqual(
            wget_session(self.mocked_obj, url="5.0.0.1", service="ftp",
                                             path_to_file="abc.txt", ), dict_to_return)

        dict_to_return3 = {'file_name': None,
                           'time_taken_in_seconds': None,
                           'file_transfer_percentage': None,
                           'file_size': None}
        self.mocked_obj.shell.side_effect = [Response(""), Response(""), Response(""), Response("")]
        self.assertEqual(wget_session(device=self.mocked_obj, url="5::1"),
                         dict_to_return3)

        self.mocked_obj.shell.side_effect = [Response(" pid 1234 ")]
        self.assertEqual(wget_session(device=self.mocked_obj, url="5::1", background_session=True), "1234")

        self.mocked_obj.shell.side_effect = [Response(" pi ")]
        self.assertEqual(wget_session(device=self.mocked_obj, url="5::1", background_session=True),
                         "0")


    def test_execute_curl(self):
        str = "< HTTP/1.0 302 Moved Temporarily\n"
        str = str + '<Location: http://www.google.com/?JNI_URL=gmail.com/&JNI_REASON=BY_USER_DEFINED&JNI_CATEGORY=cat1&JNI_REPUTATION=BY_SITE_REPUTATION_NULL_REPUTATION&JNI_POLICY=ewf1&JNI_SRCIP=4.0.0.1&JNI_SRCPORT=57441&JNI_DSTIP=216.58.220.37&JNI_DSTPORT=80'
        return_dict = {'JNI_DSTIP': ['216.58.220.37'], 'JNI_DSTPORT': ['80'], 'JNI_SRCPORT': ['57441'], 'JNI_REPUTATION': ['BY_SITE_REPUTATION_NULL_REPUTATION'], 'JNI_SRCIP': ['4.0.0.1'], 'JNI_URL': ['gmail.com/'], 'REDIRECT_URL': ' http://www.google.com/','JNI_CATEGORY': ['cat1'], 'JNI_REASON': ['BY_USER_DEFINED'], 'JNI_POLICY': ['ewf1']}

        self.mocked_obj.shell = MagicMock(side_effect=[Response(str)])
        #redirect=1
        self.assertEqual(execute_curl(device=self.mocked_obj, url="https://gmail.com", redirect=1), return_dict)

        #pattern
        str = '* Closing connection 0\n'
        str = str + 'HTML><HEAD><TITLE>Juniper Web Filtering</TITLE></HEAD><BODY>***USER-MESSAGE***<br>CATEGORY: cat1 REASON: BY_USER_DEFINED</br></BODY></HTML>'
        self.mocked_obj.shell = MagicMock(side_effect=[Response(str)])
        self.assertTrue(execute_curl(device=self.mocked_obj, url="https://gmail.com", pattern='USER-MESSAGE'))

        
        try:
            execute_curl()
        except Exception as err:
            self.assertEqual(err.args[0], "mandatory arguments are missing")

        self.mocked_obj.shell = MagicMock(side_effect=[Response('curl body')])
        self.assertTrue(execute_curl(device=self.mocked_obj, url="https://gmail.com", bg=1))
       



if __name__ == '__main__':
    unittest.main()
