"""
Linux Traffic Utils keywords
"""
import time
import re
import yaml
from jnpr.toby.utils.linux.linux_network_config import get_ip_address_type

from urllib import parse

def check_ping_connection(device=None, destination=None, source=None, count="5", **kwargs):
    """
    To check connectivity between two linux host using ping
    Example:
    check_ping_connection(device=linux, destination="4.0.0.1", source="4.0.0.2", count="10")
    check_ping_connection(device=linux, destination="2004::1", source ="2004::254",count="5")
    check_ping_connection(device=linux, destination="4.0.0.1", count="2", source="4.0.0.2", \
                          packetsize="64", ttl="60", strict_check="no")
    Robot Example:
    check ping connection  device=$(linux)  destination=4.0.0.1  source=4.0.0.2
                           count=10  packetsize=64  ttl=60  strict_check=no
    check ping connection  device=$(linux)  destination=2004::1  source =2004::254
                             count=5
     :param str device:
         **REQUIRED**  device handle for linux host
     :param str destination:
         **REQUIRED** Target IPv4/IPv6 address
     :param str source:
         *OPTIONAL* Source IPv4/IPv6 address
     :param str count:
         *OPTIONAL* Count number , Number of time ping request to be send
     :param str packetsize:
          *OPTIONAL* Packet size of ICMP packet
     :param str donotfrag:
          *OPTIONAL* mtu discovery hint
          ``Supported Value`` do, want and dont
     :param bool rapid_ping:
       *OPTIONAL* Pass true if you want rapid ping. By default it is False.
     :param str interval:
       *OPTIONAL* Wait interval seconds between sending each packet.  The default is to wait for 
       one second between each  packet normally, or not to wait in rapid ping mode.
     :param str ttl:
              *OPTIONAL* TTL value for ping
     :param bool strict_check:
                   *OPTIONAL* Flag , default value is True
                              if True will check 100% success,
                              if False keyword would return True untill 100% packet loss
     :param negative:
            *OPTIONAL* option to veify negative scenario where ping should fail
     :param loss_tolerance:
            *OPTIONAL* option to specify packet loss tolerance 			

     :return: Returns the whole response if True.
                 In all other cases Exception is raised
     :rtype: str
    """
    if device is None:
        raise ValueError("device is mandatory argument")
    if destination is None:
        device.log(level='ERROR', message="destination is mandatory argument")
        raise ValueError("destination is mandatory argument")
    strict_check = kwargs.get('strict_check', True)
    negative = kwargs.get('negative', False)
    rapid_ping = kwargs.get('rapid_ping', False)
    
    ip_type = get_ip_address_type(destination)
    if ip_type == "ipv6":
        cmd = "ping6 "
    else:
        cmd = "ping "
    if source is not None:
        cmd = cmd + " " + "-I" + " " + source
    if 'packetsize' in kwargs:
        packetsize = kwargs.get('packetsize')
        cmd = cmd + " " + "-s" + " " + packetsize
    if 'ttl' in kwargs:
        ttl = kwargs.get('ttl')
        cmd = cmd + " " + "-t" + " " + ttl
    if 'donotfrag' in kwargs:
        donotfrag = kwargs.get('donotfrag')
        cmd = cmd + " -M " + donotfrag

    cmd = cmd + " " + "-c" + " " + str(count)  + " " + destination
    if rapid_ping:
        cmd = cmd + " " + "-f"
    if 'interval' in kwargs:
        interval = kwargs.get('interval')
        cmd = cmd + " -i " + interval
    
    # Execute ping command and check for ping success
    response = device.shell(command=cmd)
    if re.search(".* Cannot assign requested address", response.response()):
        device.log(level='INFO', message="Ping failed with error Cannot assign requested address")
        raise Exception("Ping failed with error Cannot assign requested address")
    if re.search('.* 100% packet loss', response.response()):
        device.log(level='INFO', message="All packets lost, Ping unsuccessful for %s"
                   % (destination))
        if negative:
            return response.response()
        else:
            raise Exception("All packets lost, Ping unsuccessful")
    elif re.search('.*received, 0% packet loss', response.response()):
        if negative:
            raise Exception("no packet loss, Ping successful")
        else:
            return response.response()
    # Handling case where ping output has 1% to 99% packet loss
    elif re.search('.*% packet loss', response.response()):
        if negative:
            raise Exception("few packets received, Ping successful")
        if 'loss_tolerance' in kwargs:
            loss = re.findall(r'\d+%', response.response())
            if int(loss[0].strip('%')) in range(0, int(kwargs.get('loss_tolerance'))):
                device.log(level='INFO', message="packet loss is with in tolerance level")
                return response.response()
            else:
                device.log(level='ERROR', message="packet loss is more than tolerance level")
                raise Exception("packet loss is more than tolerance level")			
        if strict_check:
            device.log(level='ERROR', message="All packets not received, Ping unsuccessful \
                                               for %s" % (destination))
            raise Exception("All packets not received, Ping unsuccessful")
        

def check_traceroute_connection(device=None, host=None, check_hop_ip=None, max_hop="5",
                                wait_time="2"):
    """
    To check traceroute of the host given.
    If 'check_hop_ip' is provided, it'll check the presence of the hop in the traceroute response.
    Example:
        check_traceroute_connection(device=linux, host="youtube.com")
        check_traceroute_connection(device=linux, host="youtube.com", check_hop_ip="5.0.0.1")
    Robot Example:
        check traceroute connection     device=${client}    host=youtube.com
        check traceroute connection     device=${client}    host=youtube.com    check hope
        ip=5.0.0.1

    :param Device device:
        **REQUIRED** Linux device handle
    :param str host:
        **REQUIRED** Host/IP address for traceroute
    :param str check_hop_ip:
        *OPTIONAL* to check the presence of the hop in the traceroute response.
    :param str max_hop:
        *OPTIONAL* Set the max number of hops (max TTL to be reached).
        ``Default value`` 5
    :param str wait_time:
        *OPTIONAL* Set the number of seconds to wait for response to a probe. Non-integer (float
                              point) values allowed too
        ``Default value`` 2
    :return:True on success
    :rtype: Bool
    """
    if device is None:
        raise Exception("Linux handle is a mandatory argument")
    if host is None:
        device.log(level='ERROR', message="host is a mandatory argument")
        raise Exception("host is a mandatory argument")

    resp = device.shell(command="traceroute -n %s -m %s -w %s" %(host, max_hop,
                                                                 wait_time)).response()
    if check_hop_ip is not None:
        if re.search(check_hop_ip, resp):
            device.log(level='INFO', message="Expected hop ip is found in traceroute output")
        else:
            device.log(level='ERROR', message="Expected hop ip is not found in traceroute output")
            raise Exception("Expected hop ip is not found in traceroute output")
    else:
        return resp


def openssl_traffic(client=None, server=None, **kwargs):
    """
    Generate certificate and key
    Example :-
        openssl_traffic(client=unix2, server=unix1, operation="resumption",
                 server_cert_path="/tmp/server-1024.crt", server_key_path="/tmp/server-1024.key",
                 serverip="5.0.0.1")
        openssl_traffic(client=unix2, server=unix1, operation="renegotiation",
                 server_cert_path="/tmp/server-1024.crt", server_key_path="/tmp/server-1024.key",
                 serverip="5.0.0.1")
        openssl_traffic(client=unix2, server=unix1, operation="httpget",
                 server_cert_path="/tmp/server-1024.crt", server_key_path="/tmp/server-1024.key",
                 serverip="5.0.0.1")
        openssl_traffic(client=unix2, server=unix1, operation="prompt",
                 server_cert_path="/tmp/server-1024.crt", server_key_path="/tmp/server-1024.key",
                 serverip="5.0.0.1",
                 command_pattern=["{'command':'R', 'pattern':'RENEGOTIATING'}",
                                "{'command':'R', 'pattern':'RENEGOTIATING'}",
                                "{'command':'GET /index.html HTTP1.1', 'pattern':'ok'}",
                                "{'command':'Q', 'pattern':'DONE'}"])
    Robot example :-
        openssl traffic    client=unix2    server=unix1    operation=resumption    serverip=5.0.0.1

    :param Device client:
        *OPTIONAL* Client device handle
    :param Device server:
        *OPTIONAL* Server device handle
    :param str serverip:
        *REQUIRED* Server ip address to which the openssl client instance will connect
    :param str server_openssl_path:
        *OPTIONAL* openssl binary path on server pc
            ``Default value``   : openssl
    :param int server_port:
        *OPTIONAL* openssl server side port number
            ``Default value``   : 443
    :param str server_cert_path:
        *OPTIONAL* server certificate path
            ``Default value``   : /tmp/server.crt
    :param str server_key_path:
        *OPTIONAL* server key path
            ``Default value``   : /tmp/server.key
    :param str server_transport_protocol:
        *OPTIONAL* server side transport protocol
            ``Supported value`` : tls1, tls1_1 or tls1_2
            ``Default value``   : tls1
    :param str server_cipher:
        *OPTIONAL* server side cipher suite value
            ``Default value``   : RC4-MD5
    :param str operation:
        *OPTIONAL* type of operation
            ``Supported value`` : normal, resumption, renegotiation, httpget, prompt,
            ``Default value``   : normal
    :param str sni_name:
        *OPTIONAL* sni value
    :param str client_openssl_path:
        *OPTIONAL* client side openssl binary path
            ``Default value``   : openssl
    :param str client_port:
        *OPTIONAL* client side port used to connect to openssl server instance
            ``Default value``   : 443
    :param str client_transport_protocol:
        *OPTIONAL* client side transport protocol
            ``Supported value`` : tls1, tls1_1 or tls1_2
            ``Default value``   : tls1
    :param str client_cipher:
        *OPTIONAL* client side cipher suite values
            ``Default value``   : RC4-MD5
    :param str ca_bundle:
        *OPTIONAL* CA bundle path
            ``Default value``   : /tmp/all.pem
    :param list(dic) command_pattern:
        *OPTIONAL* command and pattern are mandatory argument when operation is "prompt".
                    it has to be passed as list(dictionary)
            ``Default value``   : list(dic)
                Eg.,command_pattern=["{'command':'R', 'pattern':'RENEGOTIATING'}",
                                    "{'command':'R', 'pattern':'RENEGOTIATING'}",
                                    "{'command':'Q', 'pattern':'DONE'}"]
    :param int timeout:
        *OPTIONAL* prompt command execution timeout
            ``Default value``   : 20 secs
    :param int session_in:
        *OPTIONAL* session id input file path
    :param int session_out:
        *OPTIONAL* session id output file path
    :param int kill_server_openssl:
        *OPTIONAL* flag to kill openssl instance on server
    :param int kill_client_openssl:
        *OPTIONAL* flag to kill openssl instance on client
    :param str client_cert_auth
        *OPTIONAL* client certificate authentication
    :param str get_response:
           *OPTIONAL* Respond to a 'GET
           -www          - Respond to a 'GET /' with a status page
           -WWW          - Respond to a 'GET /<path> HTTP/1.0' with file ./<path>
           -HTTP         - Respond to a 'GET /<path> HTTP/1.0' with file ./<path>
                           with the assumption it contains a complete HTTP response.
    :param str server_cert2_path
           *OPTIONAL* str server certificate2 path
    :param str server_key2_path:
        *OPTIONAL* str server key path

    :return: Returns return_stdout_stderr
    :rtype: list
    """

    cserverip = kwargs.get('serverip')
    server_openssl_path = kwargs.get('server_openssl_path', "openssl").lower()
    server_port = kwargs.get('server_port', "443").lower()
    server_cert_path = kwargs.get('server_cert_path', "/tmp/server.crt").lower()
    server_key_path = kwargs.get('server_key_path', "/tmp/server.key").lower()
    server_transport_protocol = kwargs.get('server_transport_protocol', "tls1").lower()
    server_cipher = kwargs.get('server_cipher', "RC4-MD5")
    operation = kwargs.get('operation', "normal").lower()
    sni_name = kwargs.get('sni_name', None)
    client_openssl_path = kwargs.get('client_openssl_path', "openssl").lower()
    client_port = kwargs.get('client_port', "443").lower()
    client_transport_protocol = kwargs.get('client_transport_protocol', "tls1").lower()
    client_cipher = kwargs.get('client_cipher', "RC4-MD5")
    ca_bundle = kwargs.get('ca_bundle', "/tmp/all.pem")
    values = kwargs.get('command_pattern', None)
    timeout = kwargs.get('timeout', 20)
    session_in = kwargs.get('session_in', None)
    session_out = kwargs.get('session_out', None)
    kill_server_openssl = kwargs.get('kill_server_openssl', None)
    kill_client_openssl = kwargs.get('kill_client_openssl', None)
    client_cert_auth = kwargs.get('client_cert_auth', None)
    get_response =  kwargs.get('get_response', "www")
    server_cert2_path = kwargs.get('server_cert2_path', None)
    server_key2_path = kwargs.get('server_key2_path', None)

    if cserverip is None and client is not None:
        client.log(level="ERROR", message="cserverip is REQUIRED key argument")
        raise ValueError("cserverip is REQUIRED key argument")

    if operation == "prompt" and values is None:
        client.log(level="ERROR", message="command_pattern is REQUIRED key argument when "
                                          "operation is prompt")
        raise ValueError("command_pattern is REQUIRED key argument when operation is prompt")

    return_stdout_stderr = []
    cabundle_append = ""
    sni_name_append = ""
    client_cipher_append = ""
    session_in_append = ""
    session_out_append = ""
    server_cipher_append = ""
    client_cert_auth_append = ""
    server_cert2_append = ""
    server_key2_append = ""
    if server_cipher is not None and server_cipher != "None":
        server_cipher_append = " -cipher " + server_cipher
    if server_cert2_path is not None:
        server_cert2_append = " -dcert " +  server_cert2_path
    if server_key2_path is not None:
        server_key2_append = " -dkey " + server_key2_path
    if ca_bundle is not None:
        cabundle_append = " -CAfile " + ca_bundle + " "
    if sni_name is not None:
        sni_name_append = " -servername " + sni_name + " "
    if client_cipher is not None and client_cipher != "None":
        client_cipher_append = " -cipher " + client_cipher
    if session_in is not None:
        session_in_append = " -sess_in " + session_in
    if session_out is not None:
        session_out_append = " -sess_out " + session_out
    if client_cert_auth is not None:
        client_cert_auth_append = " -Verify depth "
    if server is not None:
        if kill_server_openssl is not None:
            server.shell(command="killall openssl")
            time.sleep(2)

        server.log(level='INFO', message="******************************************************"
                                         "******")
        server.log(level='INFO', message="Server Openssl binary path: %s" % server_openssl_path)
        server.log(level='INFO', message="Server Port number: %s" % server_port)
        server.log(level='INFO', message="Server certificate: %s" % server_cert_path)
        server.log(level='INFO', message="Server key: %s" % server_key_path)
        server.log(level='INFO', message="Server Transport protocol: %s" % \
                                         server_transport_protocol)
        server.log(level='INFO', message="Server Cipher suite: %s" % server_cipher)
        server.log(level='INFO', message="Server Openssl operation type: %s" % operation)
        server.log(level='INFO', message="Server SNI Name: %s" % sni_name)
        server.log(level='INFO', message="Respond to a GET: %s" % get_response)

        server.log(level='INFO', message="*******************************************************"
                                         "*****")
        if server_cipher is not None:
            serverstdout = "/tmp/" + "server-" + operation + "-" + server_transport_protocol + "-"\
                           + server_cipher + "-" + "STDOUT"
            serverstderr = "/tmp/" + "server-" + operation + "-" + server_transport_protocol + "-"\
                           + server_cipher + "-" + "STDERR"
        else:
            serverstdout = "/tmp/" + "server-" + operation + "-" + server_transport_protocol + "-"\
                           + "nonecipher" + "-" + "STDOUT"
            serverstderr = "/tmp/" + "server-" + operation + "-" + server_transport_protocol + "-"\
                           + "nonecipher" + "-" + "STDERR"
        return_stdout_stderr.append(serverstdout)
        return_stdout_stderr.append(serverstderr)
        server.log(level='INFO', message="Openssl server STDOUT : %s" % serverstdout)
        server.log(level='INFO', message="Openssl server STDERR : %s" % serverstderr)
        server.log(level='INFO', message="*******************************************************"
                                         "*****")

        cmd = "(" + server_openssl_path + " s_server -debug -accept " + server_port + " -cert " + \
                server_cert_path + " -key " + server_key_path + sni_name_append + " -" + \
                server_transport_protocol + " -no_dhe " + "-" + get_response + server_cipher_append +\
                client_cert_auth_append + server_cert2_append + server_key2_append + " 1" + str(">") + serverstdout + \
                " 2" + str(">") + serverstderr + " &" + ")"
        server.log(level='INFO', message="Openssl cmd : %s" % cmd)
        server.shell(command=cmd)

    if client is not None:
        if kill_client_openssl is not None:
            client.shell(command="killall openssl")
            time.sleep(2)

        client.log(level='INFO', message="******************************************************"
                                         "******")
        client.log(level='INFO', message="Openssl client operation type: %s" % operation)
        client.log(level='INFO', message="Client Openssl binary path: %s" % client_openssl_path)
        client.log(level='INFO', message="Client Port number: %s" % client_port)
        client.log(level='INFO', message="Client Transport protocol: %s" % \
                                         client_transport_protocol)
        client.log(level='INFO', message="Client Cipher suite: %s" % client_cipher)
        client.log(level='INFO', message="CA bundle: %s" % ca_bundle)
        client.log(level='INFO', message="Server IP address: %s" % cserverip)
        client.log(level='INFO', message="Server SNI Name: %s" % sni_name)
        client.log(level='INFO', message="********************************************************"
                                         "****")
        if client_cipher is not None:
            clientstdout = "/tmp/" + "client-" + operation + "-" + client_transport_protocol +\
                           "-" + client_cipher + "-" + "STDOUT"
            clientstderr = "/tmp/" + "client-" + operation + "-" + client_transport_protocol +\
                           "-" + client_cipher + "-" + "STDERR"
        else:
            clientstdout = "/tmp/" + "client-" + operation + "-" + client_transport_protocol + "-"\
                           + "nonecipher" + "-" + "STDOUT"
            clientstderr = "/tmp/" + "client-" + operation + "-" + client_transport_protocol + "-"\
                           + "nonecipher" + "-" + "STDERR"
        client.log(level='INFO', message="Openssl client STDOUT : %s" % clientstdout)
        client.log(level='INFO', message="Openssl client STDERR : %s" % clientstderr)
        client.log(level='INFO',
                   message="************************************************************")
        return_stdout_stderr.append(clientstdout)
        return_stdout_stderr.append(clientstderr)
        cmd = []

        if operation == "normal":
            cmd = "(sleep 3; echo Q;) | " + client_openssl_path + " s_client -connect " + \
                  cserverip + ":" + client_port + " -" + client_transport_protocol + \
                  cabundle_append + sni_name_append + client_cipher_append + session_in_append\
                  + session_out_append + " 1" + str(">") + clientstdout + " 2" + str(">") +\
                  clientstderr + "; echo"
            client.log(level='INFO', message="Openssl cmd : %s" % cmd)
        elif operation == "resumption":
            cmd = "(sleep 5; echo Q;) | " + client_openssl_path + " s_client -reconnect -connect "\
                  + cserverip + ":" + client_port + " -" + client_transport_protocol + \
                  cabundle_append  + sni_name_append + client_cipher_append + " 1" + str(">") +\
                  clientstdout + " 2" + str(">") + clientstderr + "; echo"
            client.log(level='INFO', message="Openssl cmd : %s" % cmd)
        elif operation == "renegotiation":
            cmd = "( sleep 1; echo R; sleep 1; echo R; sleep 1; echo R; sleep 1; echo R; " + \
                  "sleep 1; echo R; sleep 1;echo Q;) | " + client_openssl_path + \
                  " s_client -connect " + cserverip + ":" + client_port + " -" + \
                  client_transport_protocol + cabundle_append + sni_name_append + \
                  client_cipher_append + session_in_append + session_out_append + \
                  " 1" + str(">") + clientstdout + " 2" + str(">") + clientstderr + "; echo"

            client.log(level='INFO', message="Openssl cmd : %s" % cmd)
        elif operation == "httpget":
            cmd = "( sleep 2; echo 'GET \index.html HTTP1.1'; sleep 5;echo Q;) | " +\
                  client_openssl_path + " s_client -connect " + cserverip + ":" + client_port +\
                  " -" + client_transport_protocol + cabundle_append + sni_name_append +\
                  client_cipher_append + session_in_append + session_out_append + " 1" +\
                  str(">") + clientstdout + " 2" + str(">") + clientstderr + "; echo"
            client.log(level='INFO', message="Openssl cmd : %s" % cmd)

        if operation != "prompt":
            client.shell(command=cmd)

        if operation == "prompt":
            cmd = client_openssl_path + " s_client -connect " + cserverip + ":" + client_port +\
                  " -" + client_transport_protocol + cabundle_append  + sni_name_append +\
                  client_cipher_append + session_in_append + session_out_append
            client.shell(command=cmd, pattern='---', timeout=timeout)
            for clientside_inputs in values:
                clientside_inputs = yaml.load(str(clientside_inputs))
                client.log(level='INFO', message="command: %s" % clientside_inputs['command'])
                client.log(level='INFO', message="pattern: %s" % clientside_inputs['pattern'])
                client.shell(command=clientside_inputs['command'],\
                             pattern=clientside_inputs['pattern'], timeout=timeout)
                time.sleep(2)
    return return_stdout_stderr


def wget_session(device=None, url=None, path_to_file=None, service="http", **kwargs):
    """
    To download a file using wget.
    Example:
        wget_session(device=dh, url="5.0.0.1", path_to_file="ishan/arora/abc.txt", retry_count=5,
                     limit_rate="9999999", service="https, header="host:facebook.com")
        wget_session(device=dh, url="5::1", path_to_file="ishan/arora/abc.txt", service="ftp",
                     ftp_user="ishan", ftp_pass="1234", destination_port=2121, 
                     misc_option="--no-glob")

    ROBOT Example:
        Wget Session   device=${dh}   url=5.0.0.1   path_to_file=ishan/arora/abc.txt
                       retry_count=${5}   limit_rate=9999999   service=https
                       header=host:facebook.com
        Wget Session   device=${dh}   url=5::1   path_to_file=ishan/arora/abc.txt   service=ftp
                       ftp_user=ishan   ftp_pass=1234   destination_port=${2121}
                       misc_option=--no-glob

    :param Device device:
        **REQUIRED** Device handle of the Linux PC
    :param str url:
        **REQUIRED** URL of the remote server from where the file has to be downloaded
    :param str path_to_file:
        *OPTIONAL* THIS PATH is from /var/www/html/ (RELATIVE TO THIS PATH)
    :param str service:
        *OPTIONAL* The service which needs to be used in the wget session.
            ``Supported values``: "http", "https", "ftp"
            ``Default value``   : "http"
    :param int destination_port:
        *OPTIONAL* Destination Port
    :param int retry_count:
        *OPTIONAL* No. of retries a wget sesssion should do (-t option)
    :param str limit_rate:
        *OPTIONAL* Data rate of the session in bytes/sec
    :param str ftp_user:
        *OPTIONAL* Username for the ftp session to be created
    :param str ftp_pass:
        *OPTIONAL* Password for the ftp session to be created
    :param int timeout:
        *OPTIONAL* No. of seconds in which wget times out (--timeout= option)
    :param str source_address:
        *OPTIONAL* Source address to be bound with the wget session
    :param str header:
        *OPTIONAL* Header option in wget
    :param str misc_option:
      *OPTIONAL* Any wget options can be given which will be appended with the command.
    :param str : https_web_proxy
        *OPTIONAL* Pass the https external web proxy address with port
            ``Supported values``: "X.X.X.X:YYYY" - X.X.X.X is proxy server IP address and YYYY is port address
    :param str : http_web_proxy
        *OPTIONAL* Pass the http external web proxy address with port
            ``Supported values``: "X.X.X.X:YYYY" - X.X.X.X is proxy server IP address and YYYY is port address
    :param bool background_session:
        *OPTIONAL* Pass true if you want to have background session. In this case, only Process ID
        will be returned (str). By default it is False.
    :returns: Dictionary regarding details of the wget session
    :rtype: dict
    """

    if device is None:
        raise ValueError("'device' is a mandatory argument")
    if url is None:
        device.log(level="ERROR", message="'url ia a mandatory argument")
        raise ValueError("'url ia a mandatory argument")

    destination_port = kwargs.get('destination_port')
    retry_count = kwargs.get('retry_count', 1)
    limit_rate = kwargs.get('limit_rate', '100000000')
    ftp_user = kwargs.get('ftp_user', "root")
    ftp_pass = kwargs.get('ftp_pass', "Embe1mpls")
    timeout = kwargs.get('timeout', 300)
    source_address = kwargs.get('source_address')
    background_session = kwargs.get('background_session', False)
    header = kwargs.get('header')
    misc_option = kwargs.get('misc_option', None)
    https_web_proxy = kwargs.get('https_web_proxy', None)
    http_web_proxy = kwargs.get('http_web_proxy', None)

    if 'destination_port' not in kwargs:
        if service == "https":
            destination_port = 443
        elif service == "ftp":
            destination_port = 21
        else:
            destination_port = 80

    wget_mode = "wget "

    #Checking if IPv6 address or not
    if re.match(".*:.*", url, re.DOTALL):
        wget_mode = wget_mode + "-6 "
        url = "[" + url + "]" + ":" + str(destination_port)
    elif https_web_proxy is not None:
        url = url + " -e use_proxy=yes -e https_proxy=https://" + https_web_proxy
        service = "https"
    elif http_web_proxy is not None:
        url = url + " -e use_proxy=yes -e http_proxy=http://" + http_web_proxy
        service = "http"
    else:
        url = url + ":" + str(destination_port)

    if path_to_file is not None:
        if service == "ftp":
            url = url + "/../var/www/html/" + path_to_file
        else:
            url = url + "/" + path_to_file

    if 'header' in kwargs:
        wget_mode = wget_mode + "--header='" + header + "' "
    if 'source_address' in kwargs:
        wget_mode = wget_mode + "--bind-address=" + source_address + " "

    if service == "https":
        cmd = wget_mode + "https://" + url + " --no-check-certificate"
    elif service == "ftp":
        cmd = wget_mode + "ftp://" + url + " --ftp-password=" + ftp_pass + " --ftp-user=" + ftp_user
    else:
        cmd = wget_mode + "http://" + url
    

    cmd = cmd + " -t " + str(retry_count) + " --limit-rate=" + limit_rate + " --timeout=" + \
          str(timeout)
    
    if misc_option is not None:
        cmd = cmd + " " + misc_option
 
    # If background session is True, only Process ID is returned
    if background_session is True:
        cmd = cmd + " -bq"
        pid_status = device.shell(command=cmd).response()
        match = re.search(".*pid\\s*([0-9]+).*", pid_status, re.DOTALL)
        if match:
            pid = match.group(1)
            return pid
        else:
            device.log(level="ERROR", message="PID could not be fetched, returning '0'")
            return "0"

    cmd = "time " + cmd + " |& tee /tmp/output.txt"

    time_status = device.shell(command=cmd, timeout=300).response()
    status = device.shell(command="cat /tmp/output.txt").response()
    device.shell(command="rm -rf /tmp/output.txt")

    if re.match(".*100%.*", status, re.DOTALL):
        device.log(level="INFO", message="File downloaded successfully")
    else:
        device.log(level="INFO", message="File could not be downloaded completely")

    #Flags regarding File name and time taken found in the Output
    file_name_found = 0
    time_taken_found = 0
    file_size_found = 0
    percentage_completed = None
    size_of_file_downloaded = None
    dict_to_return = {}
    file_name = None
    #Looking Downloaded File name and time taken for 100% download
    for stat in status.splitlines():
        #Looking for File Name in case of Non-FTP
        if file_name_found == 0 and service != "ftp":
            match = False
            if re.search(".*Saving\\s*to:\\s*\\“(.*)\\”", stat, re.DOTALL):
                match = re.search(".*Saving\\s*to:\\s*\\“(.*)\\”", stat, re.DOTALL)
            elif re.search(".*Saving\\s*to:\\s*\\‘(.*)\\’.*", stat, re.DOTALL):
                match = re.search(".*Saving\\s*to:\\s*\\‘(.*)\\’.*", stat, re.DOTALL)
            if match:
                file_name_found = 1
                file_name = match.group(1)
        #Looking for File name in case of FTP
        if file_name_found == 0 and service == "ftp":
            match = re.search(".*\\“(.*)\\”\\s* saved.*", stat, re.DOTALL)
            if match:
                file_name_found = 1
                file_name = match.group(1)
        if file_size_found == 0:
            match = re.search(".*saved\\s*\\[([0-9]+)/.*", stat, re.DOTALL)
            if match:
                file_size_found = 1
                size_of_file_downloaded = match.group(1)

    match = re.search(".*\\s+([0-9]+)%.*", status, re.DOTALL)
    if match:
        percentage_completed = int(match.group(1))

    match = re.search(".*real\\s*([0-9]+)m([0-9]+)\\..*", time_status, re.DOTALL)
    if match:
        time_taken_found = 1
        mins_taken = int(match.group(1))
        secs_taken = int(match.group(2))

    if file_name_found == 0:
        device.log(level="ERROR", message="File name could not be fetched")
        file_name = None

    else:
        path = device.shell(command="pwd").response().strip()
        file_name = path + "/" + file_name

    if time_taken_found == 0:
        device.log(level="ERROR", message="Time taken could not be fetched")
        secs_taken = None
    else:
        secs_taken = secs_taken + 60*mins_taken

    if size_of_file_downloaded is not None:
        size_of_file_downloaded = int(size_of_file_downloaded)

    #Creating a dictionary to return
    dict_to_return['file_name'] = file_name
    dict_to_return['time_taken_in_seconds'] = secs_taken
    dict_to_return['file_transfer_percentage'] = percentage_completed
    dict_to_return['file_size'] = size_of_file_downloaded

    return dict_to_return


def execute_curl(device=None, url=None, options=[], **kwargs):
    """
        Runs curl command and extracts the output based on the inputs provided

        :param device:
            **REQUIRED**  linux handle

        :param url:
            **REQUIRED**  http url

        :param options:
            **OPTIONAL**  any option supported by curl

        :param extract:
            **OPTIONAL** extract the  provided pattern from curl output.
            Default: 1, Supported values 1/0

        One of them should be provided if u want to extract output of curl: redirect or pattern

        :param redirect:
            **OPTIONAL**  gets redirect url details

            Supported value:1

        :param pattern:
            **OPTIONAL**  pattern/string in curl output

        :param bg:
            **OPTIONAL** Run curl in background and redirect to /dev/null
            
            Supported value: 1

        :return:
            If 'redirect' option is provided

                Success:  Returns dictonary of redirected url

                Failure: False

            Other than redirect
                Success:  Returns matched line form curl output

                Failure: False

        :EXAMPLE::

            PYTHON:

                ret = execute_curl(device=linux_handle, url='http://gmail.com', options=['-k', '-v', '-l'], redirect=1)

            ROBOT:

                @{opts} =  Create List  -k -v -l

                ${ret} =  execute curl  device={linux_handle}  url=http://gmail.com  options=@{opts}  redirect=1


    """
    if device is None or url is None:
        raise ValueError("mandatory arguments are missing")

    extract = kwargs.get('extract', 1)
    err_level = kwargs.get('err_level', 'ERROR')
    return_value = False
    cmd = 'curl '
    for opt in options:
        cmd = "%s %s " % (cmd, opt)
    cmd = cmd + ' ' + url

    if 'bg' in kwargs:
        cmd = cmd + ' > /dev/null 2>&1'

    device.log("Running: %s" %cmd)
    result = device.shell(command=cmd, raw_output=True).response()
    if re.search('Failed to connect', result):
        device.log(level=err_level, message="Failed to conenct :%s" %result)
        return return_value

    print(result)
    device.log("Response form curl:%s" % result)
    if extract:
        output = result.splitlines()
        pattern = ''
        if 'redirect' in kwargs:
            pattern = 'HTTP.*Moved .*'
        elif 'pattern' in kwargs:
            pattern = kwargs.get('pattern')
        for line in output:
            if re.search(r"%s" % pattern, line):
                if 'redirect' in kwargs:
                    index = output.index(line)
                    if output[index + 1]:
                        return _get_redirect_dict(output[index + 1])
                    else:
                        return _get_redirect_dict(output[index + 2])
                else:
                    return_value = True
                    break
        return return_value
    else:
        return_value = True
        return return_value


def _get_redirect_dict(url_string):
    """
       Internal function called by execute_curl to extract url into dict

       http://www.google.com/?JNI_URL=gmail.com/&JNI_REASON=BY_USER_DEFINED&JNI_CATEGORY=cat1&J
       NI_REPUTATION=BY_SITE_REPUTATION_NULL_REPUTATION&JNI_POLICY=ewf1&JNI_SRCIP=4.0.0.1&
       JNI_SRCPORT=57441&JNI_DSTIP=216.58.220.37&JNI_DSTPORT=80

       :param url_string:

       :return:  dict
    """
    url = re.search("(.*Location:)(.*)", url_string).groups()[1]
    #import sys, pdb
    #pdb.Pdb(stdout=sys.__stdout__).set_trace()
    #query = urlsplit(url).query
    r1 = parse.urlsplit(url)
    params = parse.parse_qs(r1.query)
    params['REDIRECT_URL'] = r1.path
    return params
